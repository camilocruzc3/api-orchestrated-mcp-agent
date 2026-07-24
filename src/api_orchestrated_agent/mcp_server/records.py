"""Local JSON persistence for sanitized demo execution records."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from api_orchestrated_agent.config import get_settings


def append_record(record: dict[str, Any], path: Path | None = None) -> dict[str, Any]:
    target = path or get_settings().records_file
    try:
        records = json.loads(target.read_text(encoding="utf-8"))
        if not isinstance(records, list):
            records = []
    except (OSError, json.JSONDecodeError):
        records = []

    records.append(record)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    return record
