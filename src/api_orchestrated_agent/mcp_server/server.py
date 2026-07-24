"""FastMCP server exposing narrowly scoped public demo tools."""
from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from api_orchestrated_agent.mcp_server.notifications import send_notification as _send_notification
from api_orchestrated_agent.mcp_server.records import append_record
from api_orchestrated_agent.mcp_server.tasks import create_task as _create_task

server = FastMCP(
    name="api-orchestrated-demo",
    instructions=(
        "Expose safe local tools for a synthetic operational-request demo. "
        "External notifications are simulated."
    ),
)


@server.tool()
def create_task(
    title: str,
    description: str,
    category: str,
    data_complete: bool,
    amount: float | None = None,
    sensitive: bool = False,
    priority: str = "normal",
) -> dict[str, Any]:
    """Create a local demo task after orchestrator policy approval."""
    return _create_task(title, description, priority)


@server.tool()
def send_notification(
    subject: str,
    message: str,
    category: str,
    data_complete: bool,
    amount: float | None = None,
    sensitive: bool = False,
    channel: str = "demo",
) -> dict[str, Any]:
    """Simulate a notification after orchestrator policy approval."""
    return _send_notification(subject, message, channel)


@server.tool()
def save_processing_record(
    source: str | None,
    category: str,
    extracted: dict[str, Any],
    decision: dict[str, Any],
) -> dict[str, Any]:
    """Persist a sanitized local execution record."""
    record = {
        "source": source,
        "category": category,
        "extracted": extracted,
        "decision": decision,
    }
    append_record(record)
    return {"ok": True, "record": record}


@server.tool()
def request_human_review(
    source: str | None,
    reason: str,
    category: str,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Record a pending human-review case without another side effect."""
    record = {
        "source": source,
        "category": category,
        "status": "pending_human_review",
        "reason": reason,
        "details": details or {},
    }
    append_record(record)
    return {"ok": True, "status": "pending_human_review", "record": record}


if __name__ == "__main__":
    server.run(transport="streamable-http")
