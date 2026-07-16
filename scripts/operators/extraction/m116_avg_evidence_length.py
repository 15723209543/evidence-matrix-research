# 用途：计算“引文长度适宜度”指标，为信息抽取判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M116', 'name': '引文长度适宜度', 'category': 'extraction', 'signal': 'avg_evidence_length', 'mode': 'range', 'target': 260}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
