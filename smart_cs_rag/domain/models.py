from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class KnowledgeDocument:
    """知识库中的基础文档实体。"""

    id: str
    title: str
    source_type: str
    language: str
    tags: List[str]
    content: str
    reference: str


@dataclass(frozen=True)
class UserQuery:
    """问答入口的标准查询对象。"""

    question: str
    language: str = "zh"
    session_id: Optional[str] = None
    history: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class RetrievalHit:
    """检索命中的单条知识。"""

    doc_id: str
    title: str
    source_type: str
    content: str
    reference: str
    score: float


@dataclass(frozen=True)
class AnswerSource:
    """返回给前端的来源摘要。"""

    doc_id: str
    title: str
    source_type: str
    score: float


@dataclass(frozen=True)
class QueryResult:
    """问答流程的最终产物。"""

    answer: str
    route: str
    compliance_passed: bool
    trace_id: str
    sources: List[AnswerSource]


@dataclass(frozen=True)
class FeedbackRecord:
    """用户反馈实体。"""

    feedback_id: str
    session_id: str
    question: str
    rating: int
    comment: str
    route: str
    created_at: str
