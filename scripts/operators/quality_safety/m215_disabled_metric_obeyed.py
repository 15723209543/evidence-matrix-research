# 用途：计算“停用指标遵循度”指标，为质量与安全判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M215', 'name': '停用指标遵循度', 'category': 'quality_safety', 'signal': 'disabled_metric_obeyed', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
