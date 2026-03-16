from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppSettings:
    """集中管理项目配置。

    配置默认值可直接本地运行，也支持通过环境变量覆盖。
    """

    app_name: str
    knowledge_base_path: Path
    feedback_log_path: Path
    audit_log_path: Path
    blocked_terms: tuple[str, ...]

    @classmethod
    def from_env(cls) -> "AppSettings":
        project_root = Path(__file__).resolve().parents[2]
        data_dir = project_root / "data"
        runtime_dir = data_dir / "runtime"
        runtime_dir.mkdir(parents=True, exist_ok=True)

        blocked_terms = tuple(
            item.strip()
            for item in os.getenv(
                "SMART_CS_BLOCKED_TERMS",
                "身份证号,银行卡完整卡号,内部费率底表",
            ).split(",")
            if item.strip()
        )
        return cls(
            app_name=os.getenv("SMART_CS_APP_NAME", "smart-cs-rag"),
            knowledge_base_path=Path(
                os.getenv(
                    "SMART_CS_KNOWLEDGE_BASE_PATH",
                    str(data_dir / "seed" / "knowledge_base.json"),
                )
            ),
            feedback_log_path=Path(
                os.getenv(
                    "SMART_CS_FEEDBACK_LOG_PATH",
                    str(runtime_dir / "feedback.jsonl"),
                )
            ),
            audit_log_path=Path(
                os.getenv(
                    "SMART_CS_AUDIT_LOG_PATH",
                    str(runtime_dir / "audit.log"),
                )
            ),
            blocked_terms=blocked_terms,
        )
