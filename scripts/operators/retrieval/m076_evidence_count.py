# 用途：计算“证据数量充足度”指标，为语义检索判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M076', 'name': '证据数量充足度', 'category': 'retrieval', 'signal': 'evidence_count', 'mode': 'count', 'target': 8}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
