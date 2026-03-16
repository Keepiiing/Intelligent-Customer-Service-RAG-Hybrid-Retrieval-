from __future__ import annotations

from dataclasses import dataclass

from smart_cs_rag.common.settings import AppSettings
from smart_cs_rag.infrastructure.repositories.json_feedback_repository import (
    JsonFeedbackRepository,
)
from smart_cs_rag.infrastructure.repositories.json_knowledge_repository import (
    JsonKnowledgeRepository,
)
from smart_cs_rag.infrastructure.search.simple_hybrid_search_engine import (
    SimpleHybridSearchEngine,
)
from smart_cs_rag.orchestration.query_workflow import QueryWorkflow
from smart_cs_rag.services.audit_service import AuditService
from smart_cs_rag.services.compliance_service import ComplianceService
from smart_cs_rag.services.feedback_service import FeedbackService
from smart_cs_rag.services.generation_service import GenerationService
from smart_cs_rag.services.query_routing_service import QueryRoutingService
from smart_cs_rag.services.retrieval_service import RetrievalService


@dataclass
class ApplicationContainer:
    """集中管理服务依赖。

    企业项目通常会用 IoC 容器或依赖注入框架，
    这里用 dataclass 实现一个简单、透明、易读的版本。
    """

    settings: AppSettings
    query_workflow: QueryWorkflow
    feedback_service: FeedbackService

    @classmethod
    def bootstrap(cls) -> "ApplicationContainer":
        settings = AppSettings.from_env()

        knowledge_repository = JsonKnowledgeRepository(settings.knowledge_base_path)
        feedback_repository = JsonFeedbackRepository(settings.feedback_log_path)
        search_engine = SimpleHybridSearchEngine(knowledge_repository.list_documents())

        routing_service = QueryRoutingService()
        retrieval_service = RetrievalService(search_engine, knowledge_repository)
        generation_service = GenerationService()
        compliance_service = ComplianceService(settings.blocked_terms)
        audit_service = AuditService(settings.audit_log_path)
        feedback_service = FeedbackService(feedback_repository)

        workflow = QueryWorkflow(
            routing_service=routing_service,
            retrieval_service=retrieval_service,
            generation_service=generation_service,
            compliance_service=compliance_service,
            audit_service=audit_service,
        )
        return cls(
            settings=settings,
            query_workflow=workflow,
            feedback_service=feedback_service,
        )
