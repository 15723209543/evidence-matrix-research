# 用途：计算“时间范围明确度”指标，为查询意图判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M005', 'name': '时间范围明确度', 'category': 'query_intent', 'signal': 'query_time', 'mode': 'presence', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
