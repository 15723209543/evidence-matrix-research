# 用途：从命令行运行一次多源检索、融合、冲突识别和证据评分任务。
from __future__ import annotations

import argparse
import json
import sys
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
    parser = argparse.ArgumentParser(description="证据矩阵检索研判")
    parser.add_argument("--query", required=True, help="需要检索研判的问题")
    parser.add_argument("--sources", action="append", default=[], help="本地文件或目录，可重复传入")
    parser.add_argument("--url", action="append", default=[], help="公开 HTTP/HTTPS 网页，可重复传入")
    parser.add_argument("--output", default=str(Path.cwd() / "evidence-output"), help="报告输出目录")
    parser.add_argument("--config", default=str(skill_root / "references" / "metrics" / "参考指标配置.xlsx"), help="参考指标 Excel")
    parser.add_argument("--top-k", type=int, default=12, help="保留的证据片段数量，1-50")
    args = parser.parse_args()
    if not args.sources and not args.url:
        parser.error("至少提供一个 --sources 或 --url")
    try:
        result = run_pipeline(args.query.strip(), args.sources, args.url, Path(args.output), Path(args.config), max(1, min(50, args.top_k)))
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc), "type": type(exc).__name__}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps({
        "ok": True, "overall_score": result["overall_score"], "confidence": result["confidence_label"],
        "sources": result["summary"]["source_count"], "evidence": len(result["evidence"]), "conflicts": len(result["conflicts"]),
        "report_md": result["report_md"], "report_json": result["report_json"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
