# 用途：计算“消解建议完整度”指标，为矛盾消解判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M161', 'name': '消解建议完整度', 'category': 'contradiction', 'signal': 'reconciliation_hint_ratio', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
