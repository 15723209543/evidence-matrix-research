# 用途：计算“覆盖增益”指标，为智能重排判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M099', 'name': '覆盖增益', 'category': 'reranking', 'signal': 'coverage_gain', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
