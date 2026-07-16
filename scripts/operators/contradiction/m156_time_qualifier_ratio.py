# 用途：计算“时间口径限定度”指标，为矛盾消解判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M156', 'name': '时间口径限定度', 'category': 'contradiction', 'signal': 'time_qualifier_ratio', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
