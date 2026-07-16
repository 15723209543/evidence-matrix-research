# 用途：计算“空内容抑制度”指标，为来源接入判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M043', 'name': '空内容抑制度', 'category': 'source_ingestion', 'signal': 'empty_source_ratio', 'mode': 'inverse_ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
