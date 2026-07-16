# 用途：计算“重复信息压缩度”指标，为多源融合判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M174', 'name': '重复信息压缩度', 'category': 'fusion', 'signal': 'unique_evidence_ratio', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
