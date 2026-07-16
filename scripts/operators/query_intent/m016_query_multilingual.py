# 用途：计算“中英文混合可解释度”指标，为查询意图判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M016', 'name': '中英文混合可解释度', 'category': 'query_intent', 'signal': 'query_multilingual', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
