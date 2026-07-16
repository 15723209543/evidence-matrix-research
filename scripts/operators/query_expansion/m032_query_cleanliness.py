# 用途：计算“模糊拼写容错”指标，为查询扩展判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M032', 'name': '模糊拼写容错', 'category': 'query_expansion', 'signal': 'query_cleanliness', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
