# 用途：计算“内网访问阻断度”指标，为质量与安全判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M205', 'name': '内网访问阻断度', 'category': 'quality_safety', 'signal': 'private_network_block', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
