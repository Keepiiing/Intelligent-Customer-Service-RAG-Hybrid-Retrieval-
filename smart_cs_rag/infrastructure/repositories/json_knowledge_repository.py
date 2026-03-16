from __future__ import annotations

import json
from pathlib import Path
from typing import List

from smart_cs_rag.domain.models import KnowledgeDocument


class JsonKnowledgeRepository:
    """从种子文件加载知识库。

    这个仓储负责“知识从哪里读”。
    以后换成数据库或搜索引擎时，只需要替换这一层。
    """

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path
        self._documents = self._load()

    def _load(self) -> List[KnowledgeDocument]:
        raw_items = json.loads(self._file_path.read_text(encoding="utf-8"))
        return [KnowledgeDocument(**item) for item in raw_items]

    def list_documents(self) -> List[KnowledgeDocument]:
        return list(self._documents)

    def get_by_id(self, doc_id: str) -> KnowledgeDocument | None:
        for document in self._documents:
            if document.id == doc_id:
                return document
        return None
