# 用途：计算“编码解析成功率”指标，为来源接入判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M045', 'name': '编码解析成功率', 'category': 'source_ingestion', 'signal': 'encoding_success_ratio', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
