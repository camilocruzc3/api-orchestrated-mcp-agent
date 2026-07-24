"""Simulation-only notification adapter for the public repository."""
from __future__ import annotations

from typing import Any


def send_notification(subject: str, message: str, channel: str = "demo") -> dict[str, Any]:
    return {
        "ok": True,
        "notification": {
            "subject": subject,
            "message": message,
            "channel": channel,
            "status": "simulated",
        },
    }
