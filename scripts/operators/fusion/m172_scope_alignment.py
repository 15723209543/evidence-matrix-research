# 用途：计算“范围口径对齐度”指标，为多源融合判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M172', 'name': '范围口径对齐度', 'category': 'fusion', 'signal': 'scope_alignment', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
