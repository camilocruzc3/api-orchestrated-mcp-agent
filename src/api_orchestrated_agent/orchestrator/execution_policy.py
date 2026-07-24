"""Deterministic authorization rules for side-effecting MCP tools."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str | None = None


class ExecutionPolicy:
    """Keep final execution authority in local Python code."""

    def __init__(
        self,
        review_threshold: float = 10_000,
        side_effect_tools: set[str] | None = None,
    ) -> None:
        self.review_threshold = review_threshold
        self.side_effect_tools = side_effect_tools or {"create_task", "send_notification"}

    def check(self, tool_name: str, arguments: dict[str, Any]) -> PolicyDecision:
        if tool_name not in self.side_effect_tools:
            return PolicyDecision(True)

        if arguments.get("sensitive") is True:
            return PolicyDecision(False, "Sensitive requests require human review.")

        if arguments.get("data_complete") is not True:
            return PolicyDecision(False, "Critical data is missing or unconfirmed.")

        amount = self._parse_amount(arguments.get("amount"))
        if amount is not None and amount >= self.review_threshold:
            return PolicyDecision(
                False,
                f"Amount {amount:g} reaches the review threshold {self.review_threshold:g}.",
            )

        return PolicyDecision(True)

    @staticmethod
    def _parse_amount(value: Any) -> float | None:
        if isinstance(value, bool):
            return None
        if isinstance(value, (int, float)):
            return float(value)
        if not isinstance(value, str):
            return None

        normalized = value.strip().replace(" ", "").replace(",", "")
        if not normalized:
            return None
        try:
            return float(normalized)
        except ValueError:
            return None
