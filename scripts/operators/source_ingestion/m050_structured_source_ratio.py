# 用途：计算“结构化记录覆盖”指标，为来源接入判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M050', 'name': '结构化记录覆盖', 'category': 'source_ingestion', 'signal': 'structured_source_ratio', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
