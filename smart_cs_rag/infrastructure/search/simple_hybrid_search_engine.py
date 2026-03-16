from __future__ import annotations

import re
from collections import Counter
from typing import Iterable, List

from smart_cs_rag.domain.models import KnowledgeDocument, RetrievalHit


class SimpleHybridSearchEngine:
    """一个轻量的混合检索引擎。

    它不追求生产级召回效果，目标是用很少的依赖，
    把“关键词 + 语义近似”这种企业项目中的混合检索思想表达清楚。
    """

    def __init__(self, documents: Iterable[KnowledgeDocument]) -> None:
        self._documents = list(documents)

    def search(self, query: str, top_k: int = 3) -> List[RetrievalHit]:
        query_terms = self._tokenize(query)
        hits: List[RetrievalHit] = []

        for document in self._documents:
            # 这里把 tags、title、content 合在一起，模拟多字段检索。
            searchable_text = " ".join([document.title, *document.tags, document.content])
            document_terms = self._tokenize(searchable_text)
            score = self._calculate_score(query_terms, document_terms)
            if score <= 0:
                continue
            hits.append(
                RetrievalHit(
                    doc_id=document.id,
                    title=document.title,
                    source_type=document.source_type,
                    content=document.content,
                    reference=document.reference,
                    score=score,
                )
            )

        hits.sort(key=lambda item: item.score, reverse=True)
        return hits[:top_k]

    def _tokenize(self, text: str) -> Counter[str]:
        raw_terms = re.findall(r"[\u4e00-\u9fff]{1,}|[a-zA-Z0-9_]+", text.lower())
        tokens: list[str] = []
        for term in raw_terms:
            if re.fullmatch(r"[\u4e00-\u9fff]+", term):
                if len(term) == 1:
                    tokens.append(term)
                else:
                    # 2-gram 是这个 demo 中最简单的中文“近似分词”办法。
                    tokens.extend(term[index : index + 2] for index in range(len(term) - 1))
            else:
                tokens.append(term)
        return Counter(tokens)

    def _calculate_score(self, query_terms: Counter[str], document_terms: Counter[str]) -> float:
        overlap = sum(min(count, document_terms.get(term, 0)) for term, count in query_terms.items())
        if overlap == 0:
            return 0.0

        recall = overlap / max(sum(query_terms.values()), 1)
        precision = overlap / max(sum(document_terms.values()), 1)

        # 让 recall 权重更高一些，符合客服问答“先找全，再精排”的偏好。
        return round((recall * 0.7 + precision * 0.3) * 10, 4)
