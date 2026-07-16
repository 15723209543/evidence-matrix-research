# 用途：计算“来源可读比例”指标，为来源接入判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M038', 'name': '来源可读比例', 'category': 'source_ingestion', 'signal': 'readable_ratio', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
