# 用途：计算“证据引用对齐度”指标，为溯源引用判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M193', 'name': '证据引用对齐度', 'category': 'citation', 'signal': 'evidence_citation_parity', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
