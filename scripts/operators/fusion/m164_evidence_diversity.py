# 用途：计算“证据类型多样性”指标，为多源融合判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M164', 'name': '证据类型多样性', 'category': 'fusion', 'signal': 'evidence_diversity', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
