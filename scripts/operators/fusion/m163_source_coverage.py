# 用途：计算“融合来源覆盖率”指标，为多源融合判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M163', 'name': '融合来源覆盖率', 'category': 'fusion', 'signal': 'source_coverage', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
