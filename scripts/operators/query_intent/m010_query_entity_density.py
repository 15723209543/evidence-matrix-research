# 用途：计算“实体信息密度”指标，为查询意图判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M010', 'name': '实体信息密度', 'category': 'query_intent', 'signal': 'query_entity_density', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
