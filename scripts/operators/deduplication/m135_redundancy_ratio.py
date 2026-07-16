# 用途：计算“冗余预算合理度”指标，为信息去重判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M135', 'name': '冗余预算合理度', 'category': 'deduplication', 'signal': 'redundancy_ratio', 'mode': 'inverse_ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
