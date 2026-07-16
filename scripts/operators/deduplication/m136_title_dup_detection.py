# 用途：计算“标题重复识别度”指标，为信息去重判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M136', 'name': '标题重复识别度', 'category': 'deduplication', 'signal': 'title_dup_detection', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
