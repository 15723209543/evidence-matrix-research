# 用途：计算“唯一引用比例”指标，为溯源引用判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M188', 'name': '唯一引用比例', 'category': 'citation', 'signal': 'unique_citation_ratio', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
