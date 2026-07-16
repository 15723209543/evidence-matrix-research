# 用途：计算“危险扩展名阻断度”指标，为质量与安全判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M207', 'name': '危险扩展名阻断度', 'category': 'quality_safety', 'signal': 'unsafe_extension_block', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
