# 用途：计算“空输入处理度”指标，为质量与安全判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M202', 'name': '空输入处理度', 'category': 'quality_safety', 'signal': 'empty_input_handling', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
