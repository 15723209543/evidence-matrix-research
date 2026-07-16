# 用途：计算“输出确定性”指标，为质量与安全判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M210', 'name': '输出确定性', 'category': 'quality_safety', 'signal': 'deterministic_output', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
