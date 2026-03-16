from __future__ import annotations

from typing import Iterable


class ComplianceService:
    """输出合规检查服务。"""

    def __init__(self, blocked_terms: Iterable[str]) -> None:
        self._blocked_terms = tuple(blocked_terms)

    def review(self, answer: str) -> tuple[bool, str]:
        for term in self._blocked_terms:
            if term in answer:
                return False, "系统检测到潜在敏感信息，当前请求已转人工审核。"
        return True, answer
