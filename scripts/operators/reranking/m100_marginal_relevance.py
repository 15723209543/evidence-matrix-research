# 用途：计算“边际相关性”指标，为智能重排判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M100', 'name': '边际相关性', 'category': 'reranking', 'signal': 'marginal_relevance', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
