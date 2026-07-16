# 用途：计算“来源元数据完整度”指标，为来源接入判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M051', 'name': '来源元数据完整度', 'category': 'source_ingestion', 'signal': 'metadata_coverage', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
