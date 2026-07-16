# 用途：计算“检索时延可控度”指标，为语义检索判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M090', 'name': '检索时延可控度', 'category': 'retrieval', 'signal': 'retrieval_latency_ms', 'mode': 'inverse_count', 'target': 2500}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
