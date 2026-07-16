# 用途：计算“短语保留度”指标，为查询扩展判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M031', 'name': '短语保留度', 'category': 'query_expansion', 'signal': 'query_phrase_density', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
