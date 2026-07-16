# 用途：使用内置示例完成配置、检索、冲突识别和报告输出的端到端自检。
from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from core.pipeline import run_pipeline


def main() -> int:
    skill_root = Path(__file__).resolve().parents[2]
    output = Path(tempfile.gettempdir()) / "evidence-matrix-self-test"
    if output.exists():
        shutil.rmtree(output)
    result = run_pipeline(
        "比较两份材料中的年度用户数量，找出冲突并生成带引用的结论报告",
        [str(skill_root / "assets" / "examples")], [], output,
        skill_root / "references" / "metrics" / "参考指标配置.xlsx", 10,
    )
    checks = {
        "operators_at_least_200": result["summary"]["operator_count"] >= 200,
        "metrics_at_least_200": result["summary"]["enabled_metric_count"] >= 200,
        "sources_loaded": result["summary"]["source_count"] >= 2,
        "evidence_created": len(result["evidence"]) >= 2,
        "conflict_detected": len(result["conflicts"]) >= 1,
        "markdown_exists": Path(result["report_md"]).is_file(),
        "json_exists": Path(result["report_json"]).is_file(),
    }
    print(json.dumps({"ok": all(checks.values()), "checks": checks, "output": str(output)}, ensure_ascii=False, indent=2))
    return 0 if all(checks.values()) else 2


if __name__ == "__main__":
    raise SystemExit(main())
