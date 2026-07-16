# 用途：计算“答案承载句识别度”指标，为信息抽取判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M111', 'name': '答案承载句识别度', 'category': 'extraction', 'signal': 'answer_sentence_ratio', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
