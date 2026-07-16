# 用途：围绕同一问题比较两个来源目录并重点输出跨来源矛盾和覆盖差异。
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
    parser = argparse.ArgumentParser(description="比较两组来源")
    parser.add_argument("--query", required=True)
    parser.add_argument("--left", required=True)
    parser.add_argument("--right", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--config", default=str(skill_root / "references" / "metrics" / "参考指标配置.xlsx"))
    args = parser.parse_args()
    result = run_pipeline(args.query, [args.left, args.right], [], Path(args.output), Path(args.config), 20)
    print(json.dumps({"ok": True, "conflicts": result["conflicts"], "report": result["report_md"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
