from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class AskRequestSchema(BaseModel):
    question: str = Field(..., min_length=1, description="用户输入的问题")
    language: str = Field(default="zh", description="问题语言")
    session_id: Optional[str] = Field(default=None, description="会话 ID")
    history: List[str] = Field(default_factory=list, description="最近几轮历史消息")


class SourceItemSchema(BaseModel):
    doc_id: str
    title: str
    source_type: str
    score: float


class AskResponseSchema(BaseModel):
    answer: str
    route: str
    compliance_passed: bool
    trace_id: str
    sources: List[SourceItemSchema]


class FeedbackRequestSchema(BaseModel):
    session_id: str = Field(..., min_length=1)
    question: str = Field(..., min_length=1)
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(default="")
    route: str = Field(default="unknown")


class FeedbackResponseSchema(BaseModel):
    message: str
    feedback_id: str
