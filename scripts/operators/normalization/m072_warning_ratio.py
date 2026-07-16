# 用途：计算“规范化告警可控度”指标，为内容规范化判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M072', 'name': '规范化告警可控度', 'category': 'normalization', 'signal': 'warning_ratio', 'mode': 'inverse_ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
