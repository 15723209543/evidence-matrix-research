# 用途：计算“列表项完整度”指标，为信息抽取判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M121', 'name': '列表项完整度', 'category': 'extraction', 'signal': 'list_item_integrity', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
