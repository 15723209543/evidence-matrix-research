# 用途：计算“不确定性披露度”指标，为多源融合判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M168', 'name': '不确定性披露度', 'category': 'fusion', 'signal': 'uncertainty_disclosure', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
