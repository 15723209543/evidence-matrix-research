# 用途：计算“前五条查询覆盖”指标，为语义检索判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M074', 'name': '前五条查询覆盖', 'category': 'retrieval', 'signal': 'top_query_coverage', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
