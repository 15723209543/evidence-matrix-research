# 用途：计算“截断风险抑制度”指标，为信息抽取判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M123', 'name': '截断风险抑制度', 'category': 'extraction', 'signal': 'truncation_ratio', 'mode': 'inverse_ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
