# 用途：计算“数值单位归一度”指标，为查询扩展判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M033', 'name': '数值单位归一度', 'category': 'query_expansion', 'signal': 'normalization_numeric', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
