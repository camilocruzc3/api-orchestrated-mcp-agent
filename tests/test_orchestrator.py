import asyncio
import json
import unittest
from types import SimpleNamespace

from api_orchestrated_agent.orchestrator.agent_loop import AgentOrchestrator


class FakeResponses:
    def __init__(self, responses):
        self._responses = iter(responses)
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return next(self._responses)


class FakeOpenAI:
    def __init__(self, responses):
        self.responses = FakeResponses(responses)


class FakeGateway:
    def __init__(self):
        self.calls = []

    async def list_openai_tools(self):
        return [
            {
                "type": "function",
                "name": "create_task",
                "description": "Create a task",
                "parameters": {"type": "object", "properties": {}},
            },
            {
                "type": "function",
                "name": "request_human_review",
                "description": "Request review",
                "parameters": {"type": "object", "properties": {}},
            },
        ]

    async def call_tool(self, name, arguments):
        self.calls.append((name, arguments))
        return {"ok": True, "tool": name}


class OrchestratorTests(unittest.TestCase):
    def test_executes_allowed_tool_and_returns_final_text(self):
        first = SimpleNamespace(
            id="response-1",
            output=[
                SimpleNamespace(
                    type="function_call",
                    name="create_task",
                    arguments=json.dumps({"data_complete": True, "amount": 25}),
                    call_id="call-1",
                )
            ],
            output_text="",
        )
        final = SimpleNamespace(id="response-2", output=[], output_text='{"status":"done"}')
        gateway = FakeGateway()
        orchestrator = AgentOrchestrator(FakeOpenAI([first, final]), gateway)

        result = asyncio.run(orchestrator.process_text_async("Create the demo task", "test.txt"))

        self.assertEqual(result, '{"status":"done"}')
        self.assertEqual(gateway.calls[0][0], "create_task")

    def test_redirects_sensitive_tool_call_to_human_review(self):
        first = SimpleNamespace(
            id="response-1",
            output=[
                SimpleNamespace(
                    type="function_call",
                    name="create_task",
                    arguments=json.dumps({"data_complete": True, "sensitive": True}),
                    call_id="call-1",
                )
            ],
            output_text="",
        )
        final = SimpleNamespace(id="response-2", output=[], output_text='{"status":"review"}')
        gateway = FakeGateway()
        orchestrator = AgentOrchestrator(FakeOpenAI([first, final]), gateway)

        asyncio.run(orchestrator.process_text_async("Sensitive demo request", "test.txt"))

        self.assertEqual(gateway.calls[0][0], "request_human_review")
        self.assertIn("Sensitive", gateway.calls[0][1]["reason"])


if __name__ == "__main__":
    unittest.main()
