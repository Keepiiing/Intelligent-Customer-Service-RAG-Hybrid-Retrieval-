from __future__ import annotations

import json
from pathlib import Path

from smart_cs_rag.domain.models import FeedbackRecord


class JsonFeedbackRepository:
    """把反馈写入 JSON Lines 文件。

    企业项目里这里通常会接 MySQL、PostgreSQL 或消息队列，
    这里保留同样的接口职责，但实现换成最容易跑起来的文件存储。
    """

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path
        self._file_path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, record: FeedbackRecord) -> FeedbackRecord:
        payload = {
            "feedback_id": record.feedback_id,
            "session_id": record.session_id,
            "question": record.question,
            "rating": record.rating,
            "comment": record.comment,
            "route": record.route,
            "created_at": record.created_at,
        }
        with self._file_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
        return record
