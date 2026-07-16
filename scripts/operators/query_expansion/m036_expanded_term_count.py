# 用途：计算“扩展预算合理度”指标，为查询扩展判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M036', 'name': '扩展预算合理度', 'category': 'query_expansion', 'signal': 'expanded_term_count', 'mode': 'range', 'target': 24}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
