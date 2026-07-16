# 用途：计算“链接重复识别度”指标，为信息去重判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M137', 'name': '链接重复识别度', 'category': 'deduplication', 'signal': 'url_dup_detection', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
