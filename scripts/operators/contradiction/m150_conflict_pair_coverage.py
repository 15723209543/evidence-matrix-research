# 用途：计算“来源配对覆盖率”指标，为矛盾消解判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M150', 'name': '来源配对覆盖率', 'category': 'contradiction', 'signal': 'conflict_pair_coverage', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
