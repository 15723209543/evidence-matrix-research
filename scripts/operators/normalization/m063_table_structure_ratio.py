# 用途：计算“表格分隔保留度”指标，为内容规范化判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M063', 'name': '表格分隔保留度', 'category': 'normalization', 'signal': 'table_structure_ratio', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
