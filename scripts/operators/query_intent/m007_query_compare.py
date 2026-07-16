# 用途：计算“比较对象完整度”指标，为查询意图判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M007', 'name': '比较对象完整度', 'category': 'query_intent', 'signal': 'query_compare', 'mode': 'presence', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
