# 用途：计算“冲突聚类质量”指标，为矛盾消解判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M158', 'name': '冲突聚类质量', 'category': 'contradiction', 'signal': 'conflict_cluster_quality', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
