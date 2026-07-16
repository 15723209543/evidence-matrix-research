# 用途：计算“新增信息增益”指标，为信息去重判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M134', 'name': '新增信息增益', 'category': 'deduplication', 'signal': 'information_gain', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
