# 用途：计算“查询长度适宜度”指标，为查询意图判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M002', 'name': '查询长度适宜度', 'category': 'query_intent', 'signal': 'query_length', 'mode': 'range', 'target': 36}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
