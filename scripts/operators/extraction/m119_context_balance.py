# 用途：计算“上下文窗口均衡度”指标，为信息抽取判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M119', 'name': '上下文窗口均衡度', 'category': 'extraction', 'signal': 'context_balance', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
