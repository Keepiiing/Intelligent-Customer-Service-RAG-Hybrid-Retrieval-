from __future__ import annotations

import uuid

from smart_cs_rag.domain.models import AnswerSource, QueryResult, UserQuery
from smart_cs_rag.services.audit_service import AuditService
from smart_cs_rag.services.compliance_service import ComplianceService
from smart_cs_rag.services.generation_service import GenerationService
from smart_cs_rag.services.query_routing_service import QueryRoutingService
from smart_cs_rag.services.retrieval_service import RetrievalService


class QueryWorkflow:
    """问答主工作流。

    企业级系统里最核心的不是单个函数，而是“链路编排”。
    这个类负责把路由、检索、生成、合规、审计串起来。
    """

    def __init__(
        self,
        routing_service: QueryRoutingService,
        retrieval_service: RetrievalService,
        generation_service: GenerationService,
        compliance_service: ComplianceService,
        audit_service: AuditService,
    ) -> None:
        self._routing_service = routing_service
        self._retrieval_service = retrieval_service
        self._generation_service = generation_service
        self._compliance_service = compliance_service
        self._audit_service = audit_service

    def handle(self, query: UserQuery) -> QueryResult:
        trace_id = uuid.uuid4().hex
        route = self._routing_service.decide_route(query.question)
        retrieval_hits = self._retrieval_service.retrieve(query.question, route)
        answer_text = self._generation_service.generate(query, retrieval_hits)
        compliance_passed, filtered_answer = self._compliance_service.review(answer_text)

        result = QueryResult(
            answer=filtered_answer,
            route=route,
            compliance_passed=compliance_passed,
            trace_id=trace_id,
            sources=[
                AnswerSource(
                    doc_id=hit.doc_id,
                    title=hit.title,
                    source_type=hit.source_type,
                    score=hit.score,
                )
                for hit in retrieval_hits
            ],
        )
        self._audit_service.record(trace_id=trace_id, query=query, result=result)
        return result
