# 用途：计算“表格行完整度”指标，为信息抽取判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M120', 'name': '表格行完整度', 'category': 'extraction', 'signal': 'table_row_integrity', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
