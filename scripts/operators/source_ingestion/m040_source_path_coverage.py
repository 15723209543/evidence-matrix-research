# 用途：计算“目录覆盖率”指标，为来源接入判断提供独立评分信号。
from __future__ import annotations

from core.operator_runtime import evaluate_spec


SPEC = {'id': 'M040', 'name': '目录覆盖率', 'category': 'source_ingestion', 'signal': 'source_path_coverage', 'mode': 'ratio', 'target': 1}


def evaluate(context: dict) -> dict:
    return evaluate_spec(SPEC, context)
