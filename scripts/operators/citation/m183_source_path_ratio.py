# 用途：计算“来源路径完整度”指标，为溯源引用判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M183', 'name': '来源路径完整度', 'category': 'citation', 'signal': 'source_path_ratio', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
