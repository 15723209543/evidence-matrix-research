# 用途：计算“独立证据加权度”指标，为智能重排判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M097', 'name': '独立证据加权度', 'category': 'reranking', 'signal': 'unique_evidence_ratio', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
