"""Run one synthetic request through the API-orchestrated MCP agent."""
from __future__ import annotations

import sys
from pathlib import Path

from api_orchestrated_agent.orchestrator.agent_loop import AgentOrchestrator

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = PROJECT_ROOT / "examples"


def main() -> int:
    filename = sys.argv[1] if len(sys.argv) > 1 else "support_request.txt"
    path = EXAMPLES_DIR / filename
    if not path.exists():
        print(f"Example not found: {path}", file=sys.stderr)
        return 1

    text = path.read_text(encoding="utf-8")
    result = AgentOrchestrator().process_text(text, source_name=filename)
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
