# 用途：计算“冲突信息分离度”指标，为多源融合判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M175', 'name': '冲突信息分离度', 'category': 'fusion', 'signal': 'conflict_separation', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
