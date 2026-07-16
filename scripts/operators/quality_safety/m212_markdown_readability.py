# 用途：计算“Markdown可读度”指标，为质量与安全判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M212', 'name': 'Markdown可读度', 'category': 'quality_safety', 'signal': 'markdown_readability', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
