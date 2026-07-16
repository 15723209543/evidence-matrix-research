# 用途：计算“无崩溃稳定度”指标，为质量与安全判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M200', 'name': '无崩溃稳定度', 'category': 'quality_safety', 'signal': 'no_crash', 'mode': 'presence', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
