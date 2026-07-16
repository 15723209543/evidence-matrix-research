# 用途：计算“冲突严重度识别”指标，为矛盾消解判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M152', 'name': '冲突严重度识别', 'category': 'contradiction', 'signal': 'conflict_severity_quality', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
