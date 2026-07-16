# 用途：计算“无效口语抑制度”指标，为查询意图判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M018', 'name': '无效口语抑制度', 'category': 'query_intent', 'signal': 'query_stopword_ratio', 'mode': 'inverse_ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
