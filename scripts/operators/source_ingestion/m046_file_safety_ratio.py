# 用途：计算“文件大小安全度”指标，为来源接入判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M046', 'name': '文件大小安全度', 'category': 'source_ingestion', 'signal': 'file_safety_ratio', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
