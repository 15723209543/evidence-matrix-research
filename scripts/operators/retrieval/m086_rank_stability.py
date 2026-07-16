# 用途：计算“排序稳定度”指标，为语义检索判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M086', 'name': '排序稳定度', 'category': 'retrieval', 'signal': 'rank_stability', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
