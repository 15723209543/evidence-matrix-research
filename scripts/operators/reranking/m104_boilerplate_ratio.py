# 用途：计算“模板文本惩罚度”指标，为智能重排判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M104', 'name': '模板文本惩罚度', 'category': 'reranking', 'signal': 'boilerplate_ratio', 'mode': 'inverse_ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
