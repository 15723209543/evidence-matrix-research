# 用途：计算“证据密度”指标，为信息抽取判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M126', 'name': '证据密度', 'category': 'extraction', 'signal': 'evidence_density', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
