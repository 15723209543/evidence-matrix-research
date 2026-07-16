# 用途：计算“来源召回覆盖率”指标，为语义检索判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M077', 'name': '来源召回覆盖率', 'category': 'retrieval', 'signal': 'source_coverage', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
