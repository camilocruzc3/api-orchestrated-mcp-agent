"""OpenAI Responses API loop with local MCP execution and deterministic policy checks."""
from __future__ import annotations

import asyncio
import json
from typing import Any, Callable, Protocol

from openai import OpenAI

from api_orchestrated_agent.config import get_settings, load_policies, load_prompt
from api_orchestrated_agent.orchestrator.execution_policy import ExecutionPolicy
from api_orchestrated_agent.orchestrator.mcp_client import LocalMCPClient


class MCPGateway(Protocol):
    async def list_openai_tools(self) -> list[dict[str, Any]]: ...
    async def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]: ...


class AgentOrchestrator:
    def __init__(
        self,
        openai_client: Any | None = None,
        mcp_gateway: MCPGateway | None = None,
        event_callback: Callable[[dict[str, Any]], None] | None = None,
    ) -> None:
        settings = get_settings()
        policies = load_policies()
        self.client = openai_client or OpenAI(api_key=settings.openai_api_key)
        self.gateway = mcp_gateway or LocalMCPClient(settings.mcp_server_url)
        self.model = settings.openai_model
        self.max_tool_calls = settings.max_tool_calls
        self.system_prompt = load_prompt()
        self.event_callback = event_callback
        self.policy = ExecutionPolicy(
            review_threshold=settings.review_threshold,
            side_effect_tools=set(policies["side_effect_tools"]),
        )

    def process_text(self, text: str, source_name: str | None = None) -> str:
        return asyncio.run(self.process_text_async(text, source_name))

    def _emit(self, event_type: str, message: str, **detail: Any) -> None:
        if self.event_callback is None:
            return
        try:
            self.event_callback({"type": event_type, "message": message, "detail": detail})
        except Exception:
            pass

    async def process_text_async(self, text: str, source_name: str | None = None) -> str:
        if not text.strip():
            raise ValueError("Input text cannot be empty.")

        tools = await self.gateway.list_openai_tools()
        self._emit("tools_discovered", "MCP tools discovered", count=len(tools))
        response = self.client.responses.create(
            model=self.model,
            instructions=self.system_prompt,
            input=f"Process this request.\nsource_name: {source_name}\n\nText:\n{text}",
            tools=tools,
            parallel_tool_calls=False,
            max_tool_calls=self.max_tool_calls,
        )
        calls_used = 0

        while True:
            calls = [item for item in response.output if getattr(item, "type", None) == "function_call"]
            if not calls:
                return response.output_text

            outputs: list[dict[str, str]] = []
            for call in calls:
                calls_used += 1
                if calls_used > self.max_tool_calls:
                    raise RuntimeError("Maximum tool-call limit reached.")
                result = await self._execute_call(call.name, call.arguments, source_name)
                outputs.append(
                    {
                        "type": "function_call_output",
                        "call_id": call.call_id,
                        "output": json.dumps(result, ensure_ascii=False),
                    }
                )

            response = self.client.responses.create(
                model=self.model,
                previous_response_id=response.id,
                input=outputs,
                tools=tools,
                parallel_tool_calls=False,
                max_tool_calls=max(1, self.max_tool_calls - calls_used),
            )

    async def _execute_call(
        self,
        name: str,
        raw_arguments: str,
        source_name: str | None,
    ) -> dict[str, Any]:
        try:
            arguments = json.loads(raw_arguments or "{}")
            if not isinstance(arguments, dict):
                raise ValueError("Tool arguments must be a JSON object.")
        except (json.JSONDecodeError, ValueError) as exc:
            return {"ok": False, "error": f"Invalid tool arguments: {exc}"}

        decision = self.policy.check(name, arguments)
        if not decision.allowed:
            return await self.gateway.call_tool(
                "request_human_review",
                {
                    "source": source_name,
                    "reason": decision.reason or "Blocked by execution policy.",
                    "category": str(arguments.get("category", "unknown")),
                    "details": arguments,
                },
            )

        try:
            return await self.gateway.call_tool(name, arguments)
        except Exception as exc:
            return {"ok": False, "error": f"Tool execution failed: {exc}"}
