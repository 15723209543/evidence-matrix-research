# 用途：计算“指标配置加载度”指标，为质量与安全判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M213', 'name': '指标配置加载度', 'category': 'quality_safety', 'signal': 'config_loaded', 'mode': 'presence', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
