# 用途：计算“罕见词保护度”指标，为查询意图判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M017', 'name': '罕见词保护度', 'category': 'query_intent', 'signal': 'query_rare_density', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
