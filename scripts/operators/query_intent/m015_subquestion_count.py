# 用途：计算“子问题可分解度”指标，为查询意图判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M015', 'name': '子问题可分解度', 'category': 'query_intent', 'signal': 'subquestion_count', 'mode': 'range', 'target': 3}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
