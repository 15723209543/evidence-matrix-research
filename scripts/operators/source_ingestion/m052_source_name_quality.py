# 用途：计算“来源名称可辨识度”指标，为来源接入判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M052', 'name': '来源名称可辨识度', 'category': 'source_ingestion', 'signal': 'source_name_quality', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
