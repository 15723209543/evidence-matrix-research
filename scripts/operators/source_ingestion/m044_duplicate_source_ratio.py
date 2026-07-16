# 用途：计算“重复路径抑制度”指标，为来源接入判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M044', 'name': '重复路径抑制度', 'category': 'source_ingestion', 'signal': 'duplicate_source_ratio', 'mode': 'inverse_ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
