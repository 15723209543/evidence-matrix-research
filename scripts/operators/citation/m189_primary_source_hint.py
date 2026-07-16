# 用途：计算“一手来源提示度”指标，为溯源引用判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M189', 'name': '一手来源提示度', 'category': 'citation', 'signal': 'primary_source_hint', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
