# 用途：计算“引文可追溯度”指标，为溯源引用判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M186', 'name': '引文可追溯度', 'category': 'citation', 'signal': 'quote_traceability', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
