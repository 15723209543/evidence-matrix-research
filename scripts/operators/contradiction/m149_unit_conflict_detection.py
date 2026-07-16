# 用途：计算“单位冲突识别度”指标，为矛盾消解判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M149', 'name': '单位冲突识别度', 'category': 'contradiction', 'signal': 'unit_conflict_detection', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
