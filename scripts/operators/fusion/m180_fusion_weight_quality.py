# 用途：计算“融合加权合理度”指标，为多源融合判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M180', 'name': '融合加权合理度', 'category': 'fusion', 'signal': 'fusion_weight_quality', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
