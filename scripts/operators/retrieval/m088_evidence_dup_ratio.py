# 用途：计算“前列重复抑制度”指标，为语义检索判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M088', 'name': '前列重复抑制度', 'category': 'retrieval', 'signal': 'evidence_dup_ratio', 'mode': 'inverse_ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
