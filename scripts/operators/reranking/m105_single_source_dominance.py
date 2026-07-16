# 用途：计算“单源垄断抑制度”指标，为智能重排判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M105', 'name': '单源垄断抑制度', 'category': 'reranking', 'signal': 'single_source_dominance', 'mode': 'inverse_ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
