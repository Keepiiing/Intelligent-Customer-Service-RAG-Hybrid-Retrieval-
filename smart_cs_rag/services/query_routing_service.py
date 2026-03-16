from __future__ import annotations


class QueryRoutingService:
    """根据问题特征决定检索路径。"""

    def decide_route(self, question: str) -> str:
        if any(keyword in question for keyword in ("费率", "返现", "活动", "还款")):
            return "faq_hybrid_route"
        if any(keyword in question for keyword in ("合规", "隐私", "监管", "跨境")):
            return "policy_hybrid_route"
        return "default_route"
