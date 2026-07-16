# 用途：计算“问题拆解覆盖”指标，为查询扩展判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M030', 'name': '问题拆解覆盖', 'category': 'query_expansion', 'signal': 'subquestion_count', 'mode': 'count', 'target': 3}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
