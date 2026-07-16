# 用途：计算“抽取覆盖率”指标，为信息抽取判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M125', 'name': '抽取覆盖率', 'category': 'extraction', 'signal': 'extraction_coverage', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
