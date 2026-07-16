# 用途：计算“告警可操作度”指标，为质量与安全判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M201', 'name': '告警可操作度', 'category': 'quality_safety', 'signal': 'actionable_warning_ratio', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
