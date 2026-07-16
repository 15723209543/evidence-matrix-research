# 用途：计算“头部差距合理度”指标，为智能重排判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M107', 'name': '头部差距合理度', 'category': 'reranking', 'signal': 'score_margin', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
