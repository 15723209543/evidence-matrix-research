# 用途：计算“否定词保留度”指标，为查询扩展判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M029', 'name': '否定词保留度', 'category': 'query_expansion', 'signal': 'query_negative', 'mode': 'presence', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
