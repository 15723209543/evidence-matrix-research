# 用途：计算“路径穿越阻断度”指标，为质量与安全判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M206', 'name': '路径穿越阻断度', 'category': 'quality_safety', 'signal': 'path_traversal_block', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
