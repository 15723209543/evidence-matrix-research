# 用途：计算“信息缺口识别度”指标，为多源融合判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M178', 'name': '信息缺口识别度', 'category': 'fusion', 'signal': 'gap_detection', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
