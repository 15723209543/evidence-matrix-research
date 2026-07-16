# 用途：计算“否定约束识别度”指标，为查询意图判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M012', 'name': '否定约束识别度', 'category': 'query_intent', 'signal': 'query_negative', 'mode': 'presence', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
