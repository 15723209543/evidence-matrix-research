# 用途：计算“标题加权有效度”指标，为智能重排判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M092', 'name': '标题加权有效度', 'category': 'reranking', 'signal': 'title_hit', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
