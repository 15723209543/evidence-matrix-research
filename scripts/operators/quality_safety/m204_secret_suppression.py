# 用途：计算“敏感信息抑制度”指标，为质量与安全判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M204', 'name': '敏感信息抑制度', 'category': 'quality_safety', 'signal': 'secret_suppression', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
