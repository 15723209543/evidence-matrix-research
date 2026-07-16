# 用途：计算“缩写展开覆盖”指标，为查询扩展判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M021', 'name': '缩写展开覆盖', 'category': 'query_expansion', 'signal': 'expansion_acronym', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
