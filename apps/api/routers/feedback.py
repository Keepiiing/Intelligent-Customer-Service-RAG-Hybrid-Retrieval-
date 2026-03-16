from __future__ import annotations

from fastapi import APIRouter, Depends

from apps.api.dependencies import get_container
from smart_cs_rag.bootstrap.container import ApplicationContainer
from smart_cs_rag.contracts.api import FeedbackRequestSchema, FeedbackResponseSchema

router = APIRouter(prefix="/api/v1", tags=["feedback"])


@router.post("/feedback", response_model=FeedbackResponseSchema)
def submit_feedback(
    payload: FeedbackRequestSchema,
    container: ApplicationContainer = Depends(get_container),
) -> FeedbackResponseSchema:
    """记录用户反馈，模拟企业项目中的闭环运营。"""
    saved = container.feedback_service.save_feedback(
        session_id=payload.session_id,
        question=payload.question,
        rating=payload.rating,
        comment=payload.comment,
        route=payload.route,
    )
    return FeedbackResponseSchema(
        message="反馈已记录",
        feedback_id=saved.feedback_id,
    )
