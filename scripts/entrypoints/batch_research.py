# 用途：按 JSONL 查询清单批量执行检索研判并汇总每个任务的结果路径。
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
    parser = argparse.ArgumentParser(description="批量证据矩阵研判")
    parser.add_argument("--tasks", required=True, help="每行一个 JSON：query/sources/urls")
    parser.add_argument("--output", required=True)
    parser.add_argument("--config", default=str(skill_root / "references" / "metrics" / "参考指标配置.xlsx"))
    args = parser.parse_args()
    results = []
    for index, line in enumerate(Path(args.tasks).read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        task = json.loads(line)
        target = Path(args.output) / f"task-{index:03d}"
        try:
            payload = run_pipeline(task["query"], task.get("sources", []), task.get("urls", []), target, Path(args.config), int(task.get("top_k", 12)))
            results.append({"index": index, "ok": True, "score": payload["overall_score"], "report": payload["report_md"]})
        except Exception as exc:
            results.append({"index": index, "ok": False, "error": str(exc)})
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0 if all(item["ok"] for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
