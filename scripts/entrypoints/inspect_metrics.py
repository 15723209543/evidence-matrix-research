# 用途：读取 Excel 并按类别或影响系数查看当前启用的参考指标。
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

from core.config_loader import load_metric_config


def main() -> int:
    skill_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description="查看参考指标")
    parser.add_argument("--config", default=str(skill_root / "references" / "metrics" / "参考指标配置.xlsx"))
    parser.add_argument("--category", default="")
    parser.add_argument("--top", type=int, default=30)
    args = parser.parse_args()
    config = load_metric_config(args.config)
    rows = [{"id": key, **value} for key, value in config.items() if value["enabled"] and (not args.category or args.category in value["category"])]
    rows.sort(key=lambda item: (-item["weight"], item["id"]))
    print(json.dumps(rows[:max(1, args.top)], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
