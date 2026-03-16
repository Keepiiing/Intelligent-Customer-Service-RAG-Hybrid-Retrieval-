from __future__ import annotations

from fastapi import FastAPI

from apps.api.routers import feedback, health, query

app = FastAPI(
    title="Smart Customer Service RAG",
    version="1.0.0",
    description="企业风格的智能客服 RAG 单仓库示例项目。",
)
app.include_router(health.router)
app.include_router(query.router)
app.include_router(feedback.router)
