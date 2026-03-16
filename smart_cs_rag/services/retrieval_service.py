from __future__ import annotations

from smart_cs_rag.domain.models import RetrievalHit
from smart_cs_rag.infrastructure.repositories.json_knowledge_repository import (
    JsonKnowledgeRepository,
)
from smart_cs_rag.infrastructure.search.simple_hybrid_search_engine import (
    SimpleHybridSearchEngine,
)


class RetrievalService:
    """检索服务。

    当前实现只有一个简化搜索引擎，但接口已经按企业项目的思路抽象开了：
    - search engine 负责打分
    - repository 负责拿知识详情
    - retrieval service 负责组合策略和输出格式
    """

    def __init__(
        self,
        search_engine: SimpleHybridSearchEngine,
        repository: JsonKnowledgeRepository,
    ) -> None:
        self._search_engine = search_engine
        self._repository = repository

    def retrieve(self, question: str, route: str) -> list[RetrievalHit]:
        top_k = 5 if route != "default_route" else 3
        hits = self._search_engine.search(question, top_k=top_k)

        # 这里保留一次 repository 读取，模拟真实系统中“索引命中后再回源取详情”。
        hydrated_hits: list[RetrievalHit] = []
        for hit in hits:
            document = self._repository.get_by_id(hit.doc_id)
            if document is None:
                continue
            hydrated_hits.append(
                RetrievalHit(
                    doc_id=document.id,
                    title=document.title,
                    source_type=document.source_type,
                    content=document.content,
                    reference=document.reference,
                    score=hit.score,
                )
            )
        return hydrated_hits
