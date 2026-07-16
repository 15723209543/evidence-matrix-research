# 用途：计算“可行动洞察度”指标，为多源融合判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M177', 'name': '可行动洞察度', 'category': 'fusion', 'signal': 'actionable_insight_ratio', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
