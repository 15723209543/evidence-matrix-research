# 用途：计算“误报抑制度”指标，为矛盾消解判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M159', 'name': '误报抑制度', 'category': 'contradiction', 'signal': 'conflict_false_positive_control', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
