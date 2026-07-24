# Limitations

This repository is a portfolio-oriented public reconstruction, not a production automation platform.

Current limitations include:

- The complete private business workflow is intentionally not published.
- Public MCP tools use generic or simulated effects.
- Authentication and per-user authorization are not yet implemented.
- There is no durable queue, retry scheduler or distributed worker model.
- Evaluation currently focuses on deterministic policy tests rather than a full model-quality benchmark.
- The public version does not include production monitoring, tracing or cost dashboards.
- Human review is represented as a controlled fallback contract, not a complete review application.
- Model outputs remain probabilistic and must be evaluated with representative datasets before production use.
