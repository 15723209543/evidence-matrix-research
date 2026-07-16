# 用途：计算“来源差异解释度”指标，为矛盾消解判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M157', 'name': '来源差异解释度', 'category': 'contradiction', 'signal': 'provenance_difference', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
