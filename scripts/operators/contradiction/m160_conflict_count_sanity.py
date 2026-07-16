# 用途：计算“冲突数量合理度”指标，为矛盾消解判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M160', 'name': '冲突数量合理度', 'category': 'contradiction', 'signal': 'conflict_count_sanity', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
