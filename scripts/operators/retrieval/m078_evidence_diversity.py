# 用途：计算“前列来源多样性”指标，为语义检索判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M078', 'name': '前列来源多样性', 'category': 'retrieval', 'signal': 'evidence_diversity', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
