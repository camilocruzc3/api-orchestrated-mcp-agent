import unittest

from api_orchestrated_agent.orchestrator.execution_policy import ExecutionPolicy


class ExecutionPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = ExecutionPolicy(review_threshold=10_000)

    def test_allows_non_side_effect_tool(self) -> None:
        decision = self.policy.check("save_processing_record", {})
        self.assertTrue(decision.allowed)

    def test_blocks_incomplete_request(self) -> None:
        decision = self.policy.check("create_task", {"data_complete": False})
        self.assertFalse(decision.allowed)
        self.assertIn("missing", decision.reason.lower())

    def test_blocks_sensitive_request(self) -> None:
        decision = self.policy.check(
            "send_notification",
            {"data_complete": True, "sensitive": True},
        )
        self.assertFalse(decision.allowed)

    def test_blocks_amount_at_threshold(self) -> None:
        decision = self.policy.check(
            "create_task",
            {"data_complete": True, "amount": 10_000},
        )
        self.assertFalse(decision.allowed)

    def test_allows_complete_low_risk_request(self) -> None:
        decision = self.policy.check(
            "create_task",
            {"data_complete": True, "amount": 250},
        )
        self.assertTrue(decision.allowed)


if __name__ == "__main__":
    unittest.main()
