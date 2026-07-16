# 用途：计算“来源多样性加权度”指标，为智能重排判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M094', 'name': '来源多样性加权度', 'category': 'reranking', 'signal': 'evidence_diversity', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
