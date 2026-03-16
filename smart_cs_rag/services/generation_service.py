from __future__ import annotations

from smart_cs_rag.domain.models import RetrievalHit, UserQuery


class GenerationService:
    """答案生成服务。

    这里先用模板式生成来保证开箱即用。
    将来接入真实 LLM 时，这层仍然保留不变，只替换内部实现。
    """

    def generate(self, query: UserQuery, hits: list[RetrievalHit]) -> str:
        if not hits:
            return "抱歉，当前知识库中没有足够依据回答这个问题，建议转人工客服进一步处理。"

        top_hit = hits[0]
        candidate_titles = "；".join(hit.title for hit in hits)
        summary = top_hit.content[:120] + ("..." if len(top_hit.content) > 120 else "")

        # 明确输出结构，模拟企业项目中 Prompt 约束后的回答格式。
        return (
            f"核心结论：针对“{query.question}”，当前最相关的知识是：{summary}\n"
            f"分点说明：\n"
            f"1. 系统根据问题特征优先命中了《{top_hit.title}》。\n"
            f"2. 当前回答只使用已检索到的内部知识，不使用未验证的外部信息。\n"
            f"3. 如果问题涉及实时账户状态，建议结合工具服务或人工客服进一步核实。\n"
            f"来源依据：{top_hit.reference}\n"
            f"推理路径：问题预处理 -> 路由判定 -> 混合检索 -> 回答生成 -> 合规校验。\n"
            f"候选知识：{candidate_titles}"
        )
