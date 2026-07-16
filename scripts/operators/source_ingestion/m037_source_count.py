# 用途：计算“来源数量充足度”指标，为来源接入判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M037', 'name': '来源数量充足度', 'category': 'source_ingestion', 'signal': 'source_count', 'mode': 'count', 'target': 5}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
