# 用途：计算“不确定性表达度”指标，为矛盾消解判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M154', 'name': '不确定性表达度', 'category': 'contradiction', 'signal': 'uncertainty_disclosure', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
