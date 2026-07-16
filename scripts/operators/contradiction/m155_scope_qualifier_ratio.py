# 用途：计算“适用范围限定度”指标，为矛盾消解判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M155', 'name': '适用范围限定度', 'category': 'contradiction', 'signal': 'scope_qualifier_ratio', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
