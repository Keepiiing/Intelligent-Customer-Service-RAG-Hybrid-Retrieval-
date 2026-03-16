from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    """最小健康检查接口，用于本地验证和容器探针。"""
    return {"status": "ok"}
