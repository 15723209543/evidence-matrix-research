# 用途：计算“HTML残留抑制度”指标，为内容规范化判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M060', 'name': 'HTML残留抑制度', 'category': 'normalization', 'signal': 'html_residue_ratio', 'mode': 'inverse_ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
