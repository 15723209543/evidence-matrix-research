# 用途：计算“冲突引用对齐度”指标，为溯源引用判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M194', 'name': '冲突引用对齐度', 'category': 'citation', 'signal': 'conflict_citation_ratio', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
