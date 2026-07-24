# Architecture

## Components

### Python orchestrator

The orchestrator owns the execution loop. It loads configuration, discovers MCP tools, calls the OpenAI Responses API, validates function-call arguments and decides whether a requested action may run.

### OpenAI Responses API

The model classifies the request, extracts structured information and proposes tool calls. It does not connect directly to the local MCP server and does not have final authorization over side effects.

### Local MCP client

The client opens a session with the MCP server, retrieves tool schemas and converts them into function-tool definitions accepted by the model API. It also executes approved tool calls and normalizes their results.

### Local MCP server

The server exposes narrowly scoped operational capabilities. Public demo tools use local or simulated effects so the repository can be executed safely without external business systems.

### Execution policy

The policy is deterministic Python code. It checks side-effecting tool requests for completeness, sensitivity and configurable thresholds. A blocked request is redirected to `request_human_review`.

## Orchestration loop

```text
1. Receive input
2. Discover MCP tools
3. Send input and tool schemas to the model
4. Read function calls
5. Parse and validate JSON arguments
6. Apply local execution policy
7. Execute approved MCP tools or request human review
8. Return tool outputs to the model
9. Repeat until a final response or the tool-call limit is reached
```

## Trust boundary

The model is treated as a planner, not as an authority. Prompts influence behavior, while local code enforces authorization, limits and fallback paths.
