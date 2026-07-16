# 用途：计算“冲突感知度”指标，为智能重排判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M098', 'name': '冲突感知度', 'category': 'reranking', 'signal': 'conflict_awareness', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
