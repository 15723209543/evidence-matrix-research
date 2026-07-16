# 用途：计算“冲突证据绑定度”指标，为矛盾消解判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M151', 'name': '冲突证据绑定度', 'category': 'contradiction', 'signal': 'conflict_citation_ratio', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
