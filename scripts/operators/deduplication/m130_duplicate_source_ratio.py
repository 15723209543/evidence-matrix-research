# 用途：计算“来源重复抑制度”指标，为信息去重判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M130', 'name': '来源重复抑制度', 'category': 'deduplication', 'signal': 'duplicate_source_ratio', 'mode': 'inverse_ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
