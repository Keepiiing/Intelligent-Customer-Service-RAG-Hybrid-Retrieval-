from unittest import TestCase

from smart_cs_rag.bootstrap.container import ApplicationContainer
from smart_cs_rag.domain.models import UserQuery


class QueryWorkflowTestCase(TestCase):
    def setUp(self) -> None:
        self.container = ApplicationContainer.bootstrap()

    def test_workflow_returns_structured_answer(self) -> None:
        result = self.container.query_workflow.handle(
            UserQuery(question="境外消费没有返现怎么办？", session_id="case-001")
        )
        self.assertTrue(result.sources)
        self.assertIn("核心结论", result.answer)
        self.assertEqual(result.route, "faq_hybrid_route")
        self.assertTrue(result.trace_id)

    def test_workflow_returns_fallback_when_not_found(self) -> None:
        result = self.container.query_workflow.handle(
            UserQuery(question="火星殖民地今天几点发下午茶？", session_id="case-002")
        )
        self.assertFalse(result.sources)
        self.assertIn("建议转人工客服", result.answer)


if __name__ == "__main__":
    import unittest

    unittest.main()
