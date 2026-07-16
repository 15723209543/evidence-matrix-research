# 用途：校验参考指标 Excel 的表头、系数范围、指标数量和脚本映射完整性。
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
from core.operator_registry import load_operators


def main() -> int:
    skill_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description="校验参考指标配置")
    parser.add_argument("--config", default=str(skill_root / "references" / "metrics" / "参考指标配置.xlsx"))
    args = parser.parse_args()
    try:
        config = load_metric_config(args.config)
        modules = load_operators(skill_root / "scripts" / "operators")
        script_ids = {module.SPEC["id"] for module in modules}
        config_ids = set(config)
        missing_scripts = sorted(config_ids - script_ids)
        missing_config = sorted(script_ids - config_ids)
        if missing_scripts or missing_config:
            raise ValueError(f"映射不完整：缺脚本 {missing_scripts[:5]}，缺配置 {missing_config[:5]}")
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    enabled = sum(row["enabled"] for row in config.values())
    print(json.dumps({"ok": True, "metrics": len(config), "enabled": enabled, "operators": len(modules), "weight_min": min(row["weight"] for row in config.values()), "weight_max": max(row["weight"] for row in config.values())}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
