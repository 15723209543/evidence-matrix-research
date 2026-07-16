# 用途：计算“多数证据支持度”指标，为多源融合判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M166', 'name': '多数证据支持度', 'category': 'fusion', 'signal': 'majority_support', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
