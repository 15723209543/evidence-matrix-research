# 用途：计算“精确短语加权度”指标，为智能重排判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M093', 'name': '精确短语加权度', 'category': 'reranking', 'signal': 'exact_phrase_hit', 'mode': 'presence', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
