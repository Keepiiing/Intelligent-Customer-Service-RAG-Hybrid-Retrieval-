from pathlib import Path
import unittest
import uuid

from smart_cs_rag.infrastructure.repositories.json_feedback_repository import (
    JsonFeedbackRepository,
)
from smart_cs_rag.services.feedback_service import FeedbackService


class FeedbackServiceTestCase(unittest.TestCase):
    def test_feedback_is_persisted(self) -> None:
        target = Path("data/runtime") / f"test_feedback_{uuid.uuid4().hex}.jsonl"
        service = FeedbackService(JsonFeedbackRepository(target))
        record = service.save_feedback(
            session_id="s-001",
            question="境外消费没有返现怎么办？",
            rating=4,
            comment="回答有帮助",
            route="faq_hybrid_route",
        )

        self.assertTrue(target.exists())
        self.assertTrue(record.feedback_id)
        self.assertIn("境外消费", target.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
