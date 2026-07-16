# 用途：计算“实体口径对齐度”指标，为多源融合判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M173', 'name': '实体口径对齐度', 'category': 'fusion', 'signal': 'entity_alignment', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
