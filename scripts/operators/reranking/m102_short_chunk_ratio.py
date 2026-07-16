# 用途：计算“过短片段惩罚度”指标，为智能重排判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M102', 'name': '过短片段惩罚度', 'category': 'reranking', 'signal': 'short_chunk_ratio', 'mode': 'inverse_ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
