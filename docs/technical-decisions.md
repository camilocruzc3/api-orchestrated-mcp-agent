# Technical Decisions

## OpenAI Responses API

The model API is called directly by the Python application so the repository demonstrates an application-owned agent loop instead of relying on a desktop MCP client.

## MCP as the tool boundary

MCP provides discoverable tool schemas and a reusable execution interface. The model never connects directly to localhost; the Python process bridges OpenAI function calls and the local MCP session.

## Deterministic policy outside the prompt

Side-effect authorization is implemented in Python. Sensitive, incomplete and threshold-reaching requests are redirected to human review even when the model proposes execution.

## Streamable HTTP transport

The public MCP server uses streamable HTTP so the orchestrator and tool server can run as separate local processes with an explicit endpoint.

## Simulation-first public tools

Notifications are simulated and tasks remain local. This keeps the public project safe and reproducible while preserving the architecture of the private working implementation.

## Standard-library tests

The repository uses `unittest` and fake gateways/model responses for the core tests. Tests do not require network access or consume model tokens.
