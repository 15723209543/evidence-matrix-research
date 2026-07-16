# 用途：计算“同类主张聚合度”指标，为多源融合判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M165', 'name': '同类主张聚合度', 'category': 'fusion', 'signal': 'claim_aggregation', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
