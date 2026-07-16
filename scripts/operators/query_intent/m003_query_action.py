# 用途：计算“任务动词明确度”指标，为查询意图判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M003', 'name': '任务动词明确度', 'category': 'query_intent', 'signal': 'query_action', 'mode': 'presence', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
