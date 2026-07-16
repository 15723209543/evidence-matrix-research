# 用途：计算“重排一致性”指标，为智能重排判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M108', 'name': '重排一致性', 'category': 'reranking', 'signal': 'rank_stability', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
