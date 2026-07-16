# 用途：计算“完全重复识别率”指标，为信息去重判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M128', 'name': '完全重复识别率', 'category': 'deduplication', 'signal': 'exact_dup_detection', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
