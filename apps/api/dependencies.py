from __future__ import annotations

from functools import lru_cache

from smart_cs_rag.bootstrap.container import ApplicationContainer


@lru_cache
def get_container() -> ApplicationContainer:
    """缓存容器，避免每次请求都重新构造全部服务。"""
    return ApplicationContainer.bootstrap()
