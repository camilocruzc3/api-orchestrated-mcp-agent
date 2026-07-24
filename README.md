# API-Orchestrated MCP Agent

Programmatic AI agent orchestrated through the OpenAI API, with local MCP tools, deterministic execution policies and human-in-the-loop controls.

> **Repository status:** this public portfolio version reconstructs the reusable architecture of a private working implementation. It excludes organization-specific prompts, recipients, thresholds, records, credentials and operational data.

## What this project demonstrates

- A Python application that owns the complete agent execution loop.
- OpenAI Responses API for reasoning and function calling.
- A local MCP server that exposes reusable business tools.
- Runtime discovery and conversion of MCP tools into OpenAI function tools.
- Deterministic policy checks before side-effecting actions.
- Human review fallback for sensitive, incomplete or high-risk requests.
- Controlled tool-call limits, JSON validation and error handling.
- Clear separation between model reasoning, orchestration, policy and tool execution.

## Architecture

```text
Input document or request
          |
          v
Python orchestrator
  |-- loads prompt and policies
  |-- discovers MCP tools
  |-- calls OpenAI Responses API
  |-- receives function calls
  |-- validates arguments
  |-- enforces local execution policy
          |
          v
Local MCP client
          |
          v
Local MCP server
  |-- create_task
  |-- send_notification
  |-- save_processing_record
  `-- request_human_review
```

The language model can propose actions, but it cannot execute them directly. The local orchestrator remains the final authority and may allow, block or redirect each request.

## How this differs from a client-orchestrated MCP assistant

In a desktop-client architecture, ChatGPT, Claude Desktop or another MCP-compatible client manages the reasoning loop and tool selection.

In this project, the Python application itself is the orchestrator. It calls the model API, manages the tool loop and executes approved MCP actions locally. No desktop AI client is required.

## Public demo scenario

The public version processes generic operational requests:

1. Classify the request.
2. Extract structured fields without inventing values.
3. Select an appropriate tool.
4. Apply deterministic policy checks.
5. Execute the tool or request human review.
6. Save a final processing record.

Example tools:

| Tool | Purpose |
| --- | --- |
| `create_task` | Create a local demo task for a complete, low-risk request. |
| `send_notification` | Simulate a controlled notification action. |
| `save_processing_record` | Persist a sanitized execution record locally. |
| `request_human_review` | Redirect incomplete or sensitive cases to a person. |

## Execution policy

Side-effecting tools are checked locally before execution. A request is redirected to human review when, for example:

- Critical data is missing or unconfirmed.
- The request is marked as sensitive.
- Its numeric value reaches the configured review threshold.
- The requested tool is not included in the local allowlist.
- The maximum number of tool calls has been reached.

These controls are implemented in Python rather than relying only on prompt instructions.

## Project structure

```text
README.md
.env.example
requirements.txt
pyproject.toml
assets/
  screenshots/
config/
  prompts.yaml
  policies.json
docs/
  architecture.md
  security.md
  limitations.md
examples/
  standard_request.txt
  sensitive_request.txt
src/api_orchestrated_agent/
  __init__.py
  config.py
  orchestrator/
    execution_policy.py
  mcp_server/
    server.py
tests/
  test_execution_policy.py
```

## Setup

```bash
git clone https://github.com/camilocruzc3/api-orchestrated-mcp-agent.git
cd api-orchestrated-mcp-agent
python -m venv .venv
```

Activate the environment and install dependencies:

```bash
pip install -r requirements.txt
```

Create the environment file:

```bash
cp .env.example .env
```

Set your API key:

```env
OPENAI_API_KEY=your_api_key
```

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## Security and privacy

This repository intentionally excludes:

- Real business records.
- Organization-specific prompts and rules.
- Real email recipients.
- API keys and `.env` files.
- Local execution logs.
- Generated processing records.
- Private repository history.

See [`docs/security.md`](docs/security.md) and [`docs/limitations.md`](docs/limitations.md).

## Portfolio context

This project demonstrates a programmatic agent pattern in which OpenAI provides reasoning while a local Python orchestrator controls tool discovery, validation, authorization and execution through MCP.

## License

MIT License.
