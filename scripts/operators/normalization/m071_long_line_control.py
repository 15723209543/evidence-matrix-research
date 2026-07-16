# 用途：计算“长行切分质量”指标，为内容规范化判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M071', 'name': '长行切分质量', 'category': 'normalization', 'signal': 'long_line_control', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
