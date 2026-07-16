# 用途：计算“BM25分差清晰度”指标，为语义检索判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M075', 'name': 'BM25分差清晰度', 'category': 'retrieval', 'signal': 'score_margin', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
