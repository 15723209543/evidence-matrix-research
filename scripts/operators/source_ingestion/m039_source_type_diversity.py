# 用途：计算“来源类型多样性”指标，为来源接入判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M039', 'name': '来源类型多样性', 'category': 'source_ingestion', 'signal': 'source_type_diversity', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
