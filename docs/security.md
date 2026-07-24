# Security

## Controls represented

- API credentials are loaded from environment variables.
- The model receives tool schemas but cannot execute local functions directly.
- Side-effecting tools are explicitly identified and checked by local policy.
- Tool arguments must decode to a JSON object before execution.
- Sensitive, incomplete or high-value requests are redirected to human review.
- The orchestration loop has a configurable maximum number of tool calls.
- Generated records and local runtime data are excluded from version control.
- Public examples contain synthetic information only.

## Recommended production controls

A production deployment should additionally include authenticated service-to-service communication, authorization by user and tool, encrypted secret storage, immutable audit logs, rate limiting, idempotency controls, structured observability, data-retention rules and independent evaluation of model behavior.

## Prompt injection

Document text and user input must be treated as untrusted data. Tool authorization must never depend only on instructions contained in the prompt or processed document. Local policy and allowlists remain authoritative.

## Privacy boundary

Do not commit real documents, personal data, client names, email recipients, API responses, execution logs or generated records to this repository.
