# 用途：计算“同义词扩展覆盖”指标，为查询扩展判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M019', 'name': '同义词扩展覆盖', 'category': 'query_expansion', 'signal': 'expansion_synonym', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
