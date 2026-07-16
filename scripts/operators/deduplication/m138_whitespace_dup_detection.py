# 用途：计算“空白差异消解度”指标，为信息去重判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M138', 'name': '空白差异消解度', 'category': 'deduplication', 'signal': 'whitespace_dup_detection', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
