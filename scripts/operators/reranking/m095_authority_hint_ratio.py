# 用途：计算“权威来源提示度”指标，为智能重排判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M095', 'name': '权威来源提示度', 'category': 'reranking', 'signal': 'authority_hint_ratio', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
