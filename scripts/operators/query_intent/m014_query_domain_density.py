# 用途：计算“领域术语密度”指标，为查询意图判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M014', 'name': '领域术语密度', 'category': 'query_intent', 'signal': 'query_domain_density', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
