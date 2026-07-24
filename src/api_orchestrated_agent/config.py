"""Application configuration loaded from environment variables and JSON files."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None
    openai_model: str
    mcp_server_url: str
    records_file: Path
    review_threshold: float
    max_tool_calls: int


def load_policies(path: Path | None = None) -> dict[str, Any]:
    policy_path = path or PROJECT_ROOT / "config" / "policies.json"
    defaults: dict[str, Any] = {
        "review_threshold": 10_000,
        "max_tool_calls": 8,
        "side_effect_tools": ["create_task", "send_notification"],
    }
    try:
        defaults.update(json.loads(policy_path.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError):
        pass
    return defaults


def load_prompt(path: Path | None = None) -> str:
    prompt_path = path or PROJECT_ROOT / "config" / "prompts.yaml"
    fallback = (
        "You are an operational request-processing agent. Extract only explicit "
        "facts, use available tools, and redirect risky cases to human review."
    )
    try:
        lines = prompt_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return fallback

    marker = "agent_system_prompt: |"
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == marker) + 1
    except StopIteration:
        return fallback

    block: list[str] = []
    for line in lines[start:]:
        if line and not line[0].isspace():
            break
        block.append(line[2:] if line.startswith("  ") else line.lstrip())
    return "\n".join(block).strip() or fallback


def get_settings() -> Settings:
    policies = load_policies()
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-5"),
        mcp_server_url=os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8000/mcp"),
        records_file=Path(os.getenv("RECORDS_FILE", PROJECT_ROOT / "data" / "records.json")),
        review_threshold=float(os.getenv("REVIEW_THRESHOLD", policies["review_threshold"])),
        max_tool_calls=int(os.getenv("MAX_TOOL_CALLS", policies["max_tool_calls"])),
    )
