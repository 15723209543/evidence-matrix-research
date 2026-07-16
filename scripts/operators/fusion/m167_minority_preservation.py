# 用途：计算“少数意见保留度”指标，为多源融合判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M167', 'name': '少数意见保留度', 'category': 'fusion', 'signal': 'minority_preservation', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
