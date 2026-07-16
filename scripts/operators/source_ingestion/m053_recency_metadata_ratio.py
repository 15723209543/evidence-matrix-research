# 用途：计算“时间元数据覆盖”指标，为来源接入判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M053', 'name': '时间元数据覆盖', 'category': 'source_ingestion', 'signal': 'recency_metadata_ratio', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
