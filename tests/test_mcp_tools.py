import json
import tempfile
import unittest
from pathlib import Path

from api_orchestrated_agent.mcp_server.notifications import send_notification
from api_orchestrated_agent.mcp_server.records import append_record
from api_orchestrated_agent.mcp_server.tasks import create_task


class MCPToolTests(unittest.TestCase):
    def test_create_task_is_local_and_structured(self) -> None:
        result = create_task("Demo task", "Synthetic request")
        self.assertTrue(result["ok"])
        self.assertEqual(result["task"]["status"], "created")

    def test_notification_is_simulated(self) -> None:
        result = send_notification("Demo", "No external message is sent")
        self.assertEqual(result["notification"]["status"], "simulated")

    def test_append_record_persists_json_list(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "records.json"
            append_record({"id": 1}, path)
            append_record({"id": 2}, path)
            records = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual([record["id"] for record in records], [1, 2])


if __name__ == "__main__":
    unittest.main()
