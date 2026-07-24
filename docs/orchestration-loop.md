# Orchestration Loop

The Python application, not a desktop AI client, owns the runtime loop.

```text
request
  -> discover MCP tools
  -> call OpenAI Responses API
  -> inspect function calls
  -> parse JSON arguments
  -> apply local execution policy
  -> execute approved MCP tool
  -> return function_call_output
  -> repeat until final response
```

## Failure handling

- Empty input is rejected before a model call.
- Tool arguments must decode to a JSON object.
- Blocked side effects are redirected to `request_human_review`.
- Tool exceptions are returned as controlled outputs.
- `MAX_TOOL_CALLS` prevents unbounded execution.
- Parallel tool calls are disabled in the public implementation to keep policy evaluation and audit order explicit.

## Trust model

The model is a planner. The orchestrator is the execution authority. The MCP server is an implementation boundary for tools. Prompt instructions improve behavior, but they do not replace local authorization.
