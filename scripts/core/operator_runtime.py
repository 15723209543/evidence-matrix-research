# 用途：按算子声明的信号、模式和目标值计算单项指标得分。
from __future__ import annotations


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def evaluate_spec(spec: dict, context: dict) -> dict:
    raw = context.get("signals", {}).get(spec["signal"], 0.0)
    try:
        value = float(raw)
    except (TypeError, ValueError):
        value = 0.0
    mode = spec.get("mode", "ratio")
    target = max(0.000001, float(spec.get("target", 1)))
    if mode == "ratio":
        normalized = _clamp(value)
    elif mode == "inverse_ratio":
        normalized = _clamp(1 - value)
    elif mode == "count":
        normalized = _clamp(value / target)
    elif mode == "inverse_count":
        normalized = _clamp(1 - value / target)
    elif mode == "range":
        normalized = _clamp(1 - abs(value - target) / target)
    elif mode == "presence":
        normalized = 1.0 if value > 0 else 0.0
    else:
        normalized = _clamp(value)
    return {
        "id": spec["id"], "name": spec["name"], "category": spec["category"],
        "score": round(normalized * 100, 2), "signal": spec["signal"], "signal_value": round(value, 6),
        "mode": mode, "target": target,
    }
