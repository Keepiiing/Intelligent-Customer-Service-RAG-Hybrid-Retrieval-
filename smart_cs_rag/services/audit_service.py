from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from smart_cs_rag.domain.models import QueryResult, UserQuery


class AuditService:
    """记录问答审计日志。

    企业项目里这里通常会写入 ELK、Loki 或审计库。
    这里用文本日志保留同样的职责边界。
    """

    def __init__(self, log_path: Path) -> None:
        self._log_path = log_path
        self._log_path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, trace_id: str, query: UserQuery, result: QueryResult) -> None:
        timestamp = datetime.now(timezone.utc).isoformat()
        line = (
            f"{timestamp} | trace_id={trace_id} | session_id={query.session_id or '-'} "
            f"| route={result.route} | compliance={result.compliance_passed} "
            f"| question={query.question} | sources={len(result.sources)}"
        )
        with self._log_path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
