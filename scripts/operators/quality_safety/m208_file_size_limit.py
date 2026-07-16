# 用途：计算“文件体积限制度”指标，为质量与安全判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M208', 'name': '文件体积限制度', 'category': 'quality_safety', 'signal': 'file_size_limit', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
