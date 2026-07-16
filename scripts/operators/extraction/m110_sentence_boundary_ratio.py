# 用途：计算“句子边界完整度”指标，为信息抽取判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M110', 'name': '句子边界完整度', 'category': 'extraction', 'signal': 'sentence_boundary_ratio', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
