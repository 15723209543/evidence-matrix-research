# 用途：编排来源接入、检索、矛盾识别、216项指标评分和报告生成的完整流程。
from __future__ import annotations

import time
from datetime import datetime, timezone
from pathlib import Path

from core.config_loader import load_metric_config
from core.contradiction_engine import detect_conflicts
from core.operator_registry import load_operators
from core.report_writer import write_reports
from core.retrieval_engine import build_chunks, retrieve
from core.signals import build_signals
from core.source_reader import load_sources


def _gaps(query: str, documents: list, evidence: list, conflicts: list) -> list[str]:
    gaps: list[str] = []
    if len(documents) < 2:
        gaps.append("来源少于 2 个，无法充分进行跨来源交叉验证。")
    if len(evidence) < 5:
        gaps.append("高相关证据少于 5 条，建议补充更直接的材料或细化查询。")
    if not any("20" in item.text or "年" in item.text for item in evidence) and any(word in query for word in ("最新", "近期", "截至", "今年")):
        gaps.append("查询包含时效要求，但证据中的明确日期不足。")
    if conflicts:
        gaps.append("存在未自动消解的矛盾，需要核对来源权威性、统计口径和发布时间。")
    return gaps


def run_pipeline(query: str, source_paths: list[str], urls: list[str], output_dir: Path, config_path: Path, top_k: int = 12) -> dict:
    started = time.perf_counter()
    config = load_metric_config(config_path)
    documents, warnings = load_sources(source_paths, urls)
    chunks = build_chunks(documents)
    evidence, expansion = retrieve(query, chunks, top_k=top_k) if chunks else ([], {"terms": [], "expanded_terms": [], "subquestions": [], "synonym_matches": 0})
    conflicts = detect_conflicts(evidence)
    runtime_ms = (time.perf_counter() - started) * 1000
    context = {"signals": build_signals(query, documents, chunks, evidence, conflicts, warnings, expansion, runtime_ms)}
    operator_root = Path(__file__).resolve().parents[1] / "operators"
    modules = load_operators(operator_root)
    scored: list[dict] = []
    for module in modules:
        metric_id = module.SPEC["id"]
        if metric_id not in config:
            raise ValueError(f"Excel 缺少指标：{metric_id}")
        row = config[metric_id]
        if not row["enabled"]:
            continue
        result = module.evaluate(context)
        result.update({"weight": row["weight"], "threshold": row["threshold"], "category_zh": row["category"], "name": row["name"] or result["name"]})
        result["contribution"] = round(result["score"] * result["weight"], 4)
        scored.append(result)
    total_weight = sum(item["weight"] for item in scored)
    overall = sum(item["contribution"] for item in scored) / total_weight if total_weight else 0.0
    evidence_quality = sum(item.score for item in evidence) / max(1, len(evidence)) * 100
    volume_quality = min(100.0, len(evidence) / 8 * 100) * 0.55 + min(100.0, len(documents) / 3 * 100) * 0.45
    conflict_penalty = min(25.0, len(conflicts) * 6.0)
    confidence = max(0.0, min(100.0, overall * 0.45 + evidence_quality * 0.30 + volume_quality * 0.25 - conflict_penalty))
    confidence_label = "高" if confidence >= 80 and len(documents) >= 3 and len(evidence) >= 5 and not conflicts else "中" if confidence >= 50 and len(evidence) >= 2 else "低"
    payload = {
        "schema_version": "1.0", "query": query, "generated_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "overall_score": round(overall, 4), "confidence_score": round(confidence, 4), "confidence_label": confidence_label,
        "summary": {"source_count": len(documents), "chunk_count": len(chunks), "operator_count": len(modules), "enabled_metric_count": len(scored), "runtime_ms": round(runtime_ms, 2)},
        "expansion": expansion, "sources": [item.to_dict() for item in documents], "evidence": [item.to_dict() for item in evidence],
        "conflicts": [item.to_dict() for item in conflicts], "gaps": _gaps(query, documents, evidence, conflicts), "warnings": warnings,
        "metrics": scored, "config_source": str(config_path.resolve()),
    }
    md_path, json_path = write_reports(output_dir, payload)
    payload["report_md"] = str(md_path)
    payload["report_json"] = str(json_path)
    return payload
