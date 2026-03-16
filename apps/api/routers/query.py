from __future__ import annotations

from fastapi import APIRouter, Depends

from apps.api.dependencies import get_container
from smart_cs_rag.bootstrap.container import ApplicationContainer
from smart_cs_rag.contracts.api import AskRequestSchema, AskResponseSchema, SourceItemSchema
from smart_cs_rag.domain.models import UserQuery

router = APIRouter(prefix="/api/v1", tags=["query"])


@router.post("/ask", response_model=AskResponseSchema)
def ask_question(
    payload: AskRequestSchema,
    container: ApplicationContainer = Depends(get_container),
) -> AskResponseSchema:
    """问答主入口。

    控制层只做协议转换和依赖注入，真正的业务编排交给 workflow。
    """
    response = container.query_workflow.handle(
        UserQuery(
            question=payload.question,
            language=payload.language,
            session_id=payload.session_id,
            history=payload.history,
        )
    )
    return AskResponseSchema(
        answer=response.answer,
        route=response.route,
        compliance_passed=response.compliance_passed,
        trace_id=response.trace_id,
        sources=[
            SourceItemSchema(
                doc_id=item.doc_id,
                title=item.title,
                source_type=item.source_type,
                score=item.score,
            )
            for item in response.sources
        ],
    )
