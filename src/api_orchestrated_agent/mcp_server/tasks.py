"""Safe local task tool used by the public demo."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def create_task(title: str, description: str, priority: str = "normal") -> dict[str, Any]:
    return {
        "ok": True,
        "task": {
            "title": title,
            "description": description,
            "priority": priority,
            "status": "created",
            "created_at": datetime.now(timezone.utc).isoformat(),
        },
    }
