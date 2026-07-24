"""Adapter between a local MCP server and OpenAI function tools."""
from __future__ import annotations

from contextlib import AsyncExitStack
from typing import Any

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


class LocalMCPClient:
    def __init__(self, server_url: str) -> None:
        self.server_url = server_url

    async def _connect(self, stack: AsyncExitStack) -> ClientSession:
        read_stream, write_stream, _ = await stack.enter_async_context(
            streamable_http_client(self.server_url)
        )
        session = await stack.enter_async_context(ClientSession(read_stream, write_stream))
        await session.initialize()
        return session

    async def list_openai_tools(self) -> list[dict[str, Any]]:
        async with AsyncExitStack() as stack:
            session = await self._connect(stack)
            result = await session.list_tools()
            return [
                {
                    "type": "function",
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": tool.inputSchema,
                }
                for tool in result.tools
            ]

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        async with AsyncExitStack() as stack:
            session = await self._connect(stack)
            result = await session.call_tool(name, arguments)
            payload: Any
            if result.structuredContent is not None:
                payload = result.structuredContent
            else:
                payload = [item.model_dump(mode="json") for item in result.content]
            return {"ok": not bool(result.isError), "result": payload}
