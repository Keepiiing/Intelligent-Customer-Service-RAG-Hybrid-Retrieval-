from __future__ import annotations

import uuid
from datetime import datetime, timezone

from smart_cs_rag.domain.models import FeedbackRecord
from smart_cs_rag.infrastructure.repositories.json_feedback_repository import (
    JsonFeedbackRepository,
)


class FeedbackService:
    """负责反馈入库。

    这一步很重要，因为真实企业项目的优化闭环常常从反馈开始。
    """

    def __init__(self, repository: JsonFeedbackRepository) -> None:
        self._repository = repository

    def save_feedback(
        self,
        session_id: str,
        question: str,
        rating: int,
        comment: str,
        route: str,
    ) -> FeedbackRecord:
        record = FeedbackRecord(
            feedback_id=uuid.uuid4().hex,
            session_id=session_id,
            question=question,
            rating=rating,
            comment=comment,
            route=route,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        return self._repository.save(record)
