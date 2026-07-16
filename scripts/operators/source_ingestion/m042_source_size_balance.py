# 用途：计算“单源规模均衡度”指标，为来源接入判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M042', 'name': '单源规模均衡度', 'category': 'source_ingestion', 'signal': 'source_size_balance', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
