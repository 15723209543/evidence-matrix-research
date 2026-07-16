# 用途：计算“风险敏感度”指标，为查询意图判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M009', 'name': '风险敏感度', 'category': 'query_intent', 'signal': 'query_risk', 'mode': 'presence', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
