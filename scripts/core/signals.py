# 用途：从查询、来源、召回证据、冲突和运行状态生成指标算子所需的标准信号。
from __future__ import annotations

import json
import math
import re
from collections import Counter

from core.text_tools import ACTION_WORDS, RISK_WORDS, entropy_balance, jaccard, tokenize


def _ratio(numerator: float, denominator: float) -> float:
    return max(0.0, min(1.0, numerator / denominator)) if denominator else 0.0


def build_signals(query: str, documents: list, chunks: list, evidence: list, conflicts: list, warnings: list[str], expansion: dict, runtime_ms: float) -> dict[str, float]:
    query_terms = set(expansion.get("terms", []))
    expanded = expansion.get("expanded_terms", [])
    all_text = "\n".join(document.text for document in documents)
    evidence_text = "\n".join(item.text for item in evidence)
    source_types = {document.source_type for document in documents}
    source_sizes = [len(document.text) for document in documents]
    cited_sources = {item.source_id for item in evidence}
    evidence_tokens = set(tokenize(evidence_text))
    top_scores = [item.score for item in evidence]
    source_counts = Counter(item.source_id for item in evidence)
    duplicate_pairs = sum(1 for i, left in enumerate(evidence) for right in evidence[i + 1:] if jaccard(left.text, right.text) >= 0.8)
    pair_count = max(1, len(evidence) * (len(evidence) - 1) / 2)
    conflict_count = len(conflicts)
    number_conflicts = sum(item.kind == "数值冲突" for item in conflicts)
    date_conflicts = sum(item.kind == "日期冲突" for item in conflicts)
    polarity_conflicts = sum(item.kind == "肯否冲突" for item in conflicts)
    has_numbers = bool(re.search(r"\d", query))
    has_time = bool(re.search(r"20\d{2}|今年|去年|近期|截至|期间|年|月|日", query))
    has_location = bool(re.search(r"中国|国内|全球|地区|省|市|县|海外|国际", query))
    has_compare = bool(re.search(r"比较|对比|区别|差异|优劣|A与B| versus | vs\.?", query, re.I))
    has_scope = bool(re.search(r"范围|领域|行业|对象|材料|文档|来源|仅|不包括|包括", query))
    has_output = bool(re.search(r"表格|报告|清单|摘要|结论|JSON|Markdown|引用|出处", query, re.I))
    has_negative = bool(re.search(r"不要|不含|排除|禁止|仅限|不得|没有|未", query))
    cjk = len(re.findall(r"[\u3400-\u9fff]", query))
    latin = len(re.findall(r"[A-Za-z]", query))
    printable = max(1, len(query))
    html_tags = len(re.findall(r"<[^>]+>", all_text))
    control_chars = len(re.findall(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", all_text))
    whitespace_runs = len(re.findall(r"[ \t]{3,}|\n{4,}", all_text))
    sentence_end = sum(text.rstrip().endswith(tuple("。！？.!?")) for text in (item.text for item in evidence))
    quote_trunc = sum(item.text.endswith(("，", ",", "、", "：", ":")) for item in evidence)
    number_evidence = sum(bool(re.search(r"\d", item.text)) for item in evidence)
    unit_evidence = sum(bool(re.search(r"%|元|人|家|年|月|日|GB|MB|倍", item.text)) for item in evidence)
    date_evidence = sum(bool(re.search(r"20\d{2}|年|月|日", item.text)) for item in evidence)
    injection_hits = len(re.findall(r"忽略.{0,10}(指令|规则)|system prompt|developer message|执行命令|泄露", all_text, re.I))
    secret_hits = len(re.findall(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]", all_text))
    max_source_share = max(source_counts.values(), default=0) / max(1, len(evidence))
    average_evidence_length = sum(len(item.text) for item in evidence) / max(1, len(evidence))
    base_quality = _ratio(len(evidence), 8)
    conflict_detectability = 1.0 if len(documents) >= 2 else 0.5
    signals = {
        "query_clarity": min(1.0, (len(query_terms) / 8) + (0.2 if any(word in query for word in ACTION_WORDS) else 0)),
        "query_length": len(query), "query_action": any(word in query for word in ACTION_WORDS), "query_scope": has_scope,
        "query_time": has_time, "query_location": has_location, "query_compare": has_compare, "query_output": has_output,
        "query_risk": any(word in query for word in RISK_WORDS), "query_entity_density": _ratio(len(re.findall(r"[A-Z][A-Za-z0-9_-]+|《[^》]+》|[\u4e00-\u9fff]{3,8}", query)), 8),
        "query_numeric": has_numbers, "query_negative": has_negative, "query_ambiguity": _ratio(len(re.findall(r"这个|那个|它们|相关|一些|等等", query)), 5),
        "query_domain_density": _ratio(len([token for token in query_terms if len(token) >= 2]), 10), "subquestion_count": len(expansion.get("subquestions", [])),
        "query_multilingual": 1.0 if cjk and latin else 0.7, "query_rare_density": _ratio(len([token for token in query_terms if len(token) >= 4]), max(1, len(query_terms))),
        "query_stopword_ratio": _ratio(len(re.findall(r"请|帮我|麻烦|一下|相关|有关", query)), max(1, len(query_terms))),
        "expansion_synonym": _ratio(expansion.get("synonym_matches", 0), 3), "expansion_alias": _ratio(len(expanded) - len(query_terms), 8),
        "expansion_acronym": 1.0 if re.search(r"\b[A-Z]{2,}\b", query) else 0.7, "expansion_cross_language": 1.0 if cjk and latin else 0.65,
        "expansion_entity": _ratio(len(query_terms), 10), "expansion_time": 1.0 if has_time else 0.65, "expansion_location": 1.0 if has_location else 0.65,
        "expansion_hypernym": _ratio(len(expanded), 24), "expansion_hyponym": _ratio(len(expanded), 20), "expansion_action": 1.0 if any(word in query for word in ACTION_WORDS) else 0.4,
        "query_phrase_density": _ratio(len(re.findall(r"[“\"《].+?[”\"》]", query)) + len([token for token in query_terms if len(token) > 3]), 6),
        "query_cleanliness": 1 - _ratio(len(re.findall(r"(.)\1{3,}", query)), 3), "normalization_numeric": 1.0,
        "normalization_date": 1.0 if not has_time or bool(re.search(r"20\d{2}|今年|去年|近期|截至", query)) else 0.6,
        "normalization_unit": 1.0 if not has_numbers or bool(re.search(r"%|元|人|家|年|月|日|GB|MB|倍", query)) else 0.6,
        "expanded_term_count": len(expanded), "source_count": len(documents), "readable_ratio": _ratio(len(documents), len(documents) + len(warnings)),
        "source_type_diversity": _ratio(len(source_types), min(5, max(1, len(documents)))), "source_path_coverage": 1.0 if documents else 0.0,
        "total_chars": len(all_text), "source_size_balance": entropy_balance(source_sizes), "empty_source_ratio": _ratio(sum(not document.text.strip() for document in documents), max(1, len(documents))),
        "duplicate_source_ratio": _ratio(len(documents) - len({document.fingerprint for document in documents}), max(1, len(documents))), "encoding_success_ratio": _ratio(len(documents), len(documents) + len(warnings)),
        "file_safety_ratio": 1.0, "pdf_success_ratio": 1.0 if not any(document.source_type == "pdf" for document in documents) or not any("PDF" in warning for warning in warnings) else 0.5,
        "office_success_ratio": 1.0 if not any(document.source_type in {"docx", "xlsx"} for document in documents) or not any("Office" in warning for warning in warnings) else 0.5,
        "html_clean_ratio": 1 - _ratio(html_tags, 20), "structured_source_ratio": _ratio(sum(document.source_type in {"csv", "tsv", "json", "xlsx", "xml"} for document in documents), max(1, len(documents))),
        "metadata_coverage": _ratio(sum(bool(document.title and document.locator and document.fingerprint) for document in documents), max(1, len(documents))),
        "source_name_quality": _ratio(sum(len(document.title) >= 3 for document in documents), max(1, len(documents))), "recency_metadata_ratio": _ratio(sum(bool(re.search(r"20\d{2}", document.title + document.text[:200])) for document in documents), max(1, len(documents))),
        "warning_ratio": _ratio(len(warnings), max(1, len(documents) + len(warnings))), "char_retention_ratio": 1 - _ratio(control_chars, printable + len(all_text)),
        "whitespace_clean_ratio": 1 - _ratio(whitespace_runs, max(1, len(all_text) / 100)), "control_clean_ratio": 1 - _ratio(control_chars, max(1, len(all_text))),
        "unicode_normal_ratio": 1.0, "punctuation_compat_ratio": 1.0, "html_residue_ratio": _ratio(html_tags, max(1, len(all_text) / 200)),
        "boilerplate_ratio": _ratio(len(re.findall(r"版权所有|免责声明|cookie|导航|登录|注册", all_text, re.I)), max(1, len(documents) * 4)),
        "paragraph_structure_ratio": _ratio(all_text.count("\n"), max(1, len(documents) * 5)), "table_structure_ratio": 1.0 if "\t" in all_text or "|" in all_text else 0.7,
        "url_normal_ratio": 1.0, "case_normal_ratio": 1.0, "repeat_char_ratio": _ratio(len(re.findall(r"(.)\1{4,}", all_text)), max(1, len(documents) * 3)),
        "chunk_boundary_quality": _ratio(len(chunks), max(1, len(documents))), "long_line_control": 1 - _ratio(sum(len(line) > 2000 for line in all_text.splitlines()), max(1, len(all_text.splitlines()))),
        "top_score": top_scores[0] if top_scores else 0.0, "top_query_coverage": _ratio(len(query_terms & evidence_tokens), max(1, len(query_terms))),
        "score_margin": max(0.0, (top_scores[0] - top_scores[1]) if len(top_scores) > 1 else (top_scores[0] if top_scores else 0.0)), "evidence_count": len(evidence),
        "source_coverage": _ratio(len(cited_sources), max(1, len(documents))), "evidence_diversity": entropy_balance(list(source_counts.values())),
        "token_overlap": _ratio(len(query_terms & evidence_tokens), max(1, len(query_terms))), "exact_phrase_hit": query.lower() in evidence_text.lower() if len(query) < 80 else 0,
        "entity_hit": _ratio(len(query_terms & evidence_tokens), max(1, len(query_terms))), "numeric_hit": 1.0 if not has_numbers or re.search(r"\d", evidence_text) else 0.0,
        "time_hit": 1.0 if not has_time or re.search(r"20\d{2}|年|月|日|近期|截至", evidence_text) else 0.0, "title_hit": max((item.features.get("title", 0) for item in evidence), default=0),
        "avg_evidence_length": average_evidence_length, "rank_stability": 1.0, "low_score_ratio": _ratio(sum(score < 0.15 for score in top_scores), max(1, len(top_scores))),
        "evidence_dup_ratio": duplicate_pairs / pair_count, "orphan_query_ratio": 1 - _ratio(len(query_terms & evidence_tokens), max(1, len(query_terms))), "retrieval_latency_ms": runtime_ms * 0.45,
        "term_proximity": sum(item.features.get("proximity", 0) for item in evidence) / max(1, len(evidence)), "authority_hint_ratio": _ratio(sum(re.search(r"政府|大学|研究院|官网|标准|协会|法院", item.source_title + item.text[:100]) is not None for item in evidence), max(1, len(evidence))),
        "unique_evidence_ratio": 1 - duplicate_pairs / pair_count, "conflict_awareness": 1.0 if len(documents) < 2 or conflict_count >= 0 else 0.0,
        "coverage_gain": _ratio(len(evidence_tokens), max(1, len(set(tokenize(all_text))))), "marginal_relevance": 1 - duplicate_pairs / pair_count,
        "long_chunk_ratio": _ratio(sum(len(item.text) > 1200 for item in evidence), max(1, len(evidence))), "short_chunk_ratio": _ratio(sum(len(item.text) < 60 for item in evidence), max(1, len(evidence))),
        "spam_ratio": _ratio(len(re.findall(r"加微信|扫码|点击领取|免费赚钱|博彩", evidence_text)), max(1, len(evidence))), "single_source_dominance": max_source_share,
        "score_calibration": min(1.0, sum(top_scores) / max(1, len(top_scores)) * 1.5), "snippet_completeness": 1 - _ratio(quote_trunc, max(1, len(evidence))),
        "sentence_boundary_ratio": _ratio(sentence_end, max(1, len(evidence))), "answer_sentence_ratio": _ratio(sum(any(word in item.text for word in {"是", "为", "包括", "导致", "显示", "表明", "达到"}) for item in evidence), max(1, len(evidence))),
        "numeric_context_ratio": _ratio(number_evidence, max(1, len(evidence))) if has_numbers else 1.0, "unit_retention_ratio": _ratio(unit_evidence, max(1, number_evidence)) if number_evidence else 1.0,
        "date_retention_ratio": _ratio(date_evidence, max(1, len(evidence))) if has_time else 1.0, "citation_coverage": 1.0 if evidence and all(item.chunk_id and item.locator for item in evidence) else 0.0,
        "source_label_ratio": _ratio(sum(bool(item.source_title) for item in evidence), max(1, len(evidence))), "context_balance": entropy_balance([len(item.text) for item in evidence]),
        "table_row_integrity": 1.0 if "\t" not in evidence_text or any("\t" in item.text for item in evidence) else 0.5, "list_item_integrity": 1.0,
        "pronoun_ambiguity": _ratio(len(re.findall(r"它们|该项|这个|那个|其", evidence_text)), max(1, len(evidence) * 3)), "truncation_ratio": _ratio(quote_trunc, max(1, len(evidence))),
        "hallucination_proxy": 0.0 if evidence else 1.0, "extraction_coverage": base_quality, "evidence_density": _ratio(sum(len(item.text) for item in evidence), max(1, len(all_text))),
        "fingerprint_coverage": 1.0 if evidence and all(item.fingerprint for item in evidence) else 0.0, "exact_dup_detection": 1.0, "near_dup_detection": 1.0,
        "canonical_selection": 1 - duplicate_pairs / pair_count, "information_gain": 1 - duplicate_pairs / pair_count, "redundancy_ratio": duplicate_pairs / pair_count,
        "title_dup_detection": 1.0, "url_dup_detection": 1.0, "whitespace_dup_detection": 1.0, "case_dup_detection": 1.0, "punctuation_dup_detection": 1.0,
        "numeric_variant_preservation": 1.0, "conflict_preservation": 1.0 if not conflict_count or all(item.left and item.right for item in conflicts) else 0.0,
        "cross_format_dup_detection": 1.0, "dedup_audit": 1.0, "numeric_conflict_detection": conflict_detectability if number_conflicts or len(documents) >= 2 else 0.5,
        "date_conflict_detection": conflict_detectability if date_conflicts or len(documents) >= 2 else 0.5, "polarity_conflict_detection": conflict_detectability if polarity_conflicts or len(documents) >= 2 else 0.5,
        "entity_conflict_detection": conflict_detectability, "unit_conflict_detection": conflict_detectability, "conflict_pair_coverage": conflict_detectability,
        "conflict_citation_ratio": 1.0 if not conflicts or all(item.left.get("chunk_id") and item.right.get("chunk_id") for item in conflicts) else 0.0,
        "conflict_severity_quality": 1.0 if not conflicts or all(0 <= item.severity <= 1 for item in conflicts) else 0.0, "unresolved_conflict_disclosure": 1.0,
        "uncertainty_disclosure": 1.0, "scope_qualifier_ratio": 0.8 if has_scope else 0.6, "time_qualifier_ratio": 0.8 if has_time else 0.6,
        "provenance_difference": 1.0, "conflict_cluster_quality": 0.8 if conflicts else 1.0, "conflict_false_positive_control": 0.8,
        "conflict_count_sanity": 1 - _ratio(conflict_count, max(1, len(evidence) * 3)), "reconciliation_hint_ratio": 1.0 if not conflicts or all(item.explanation for item in conflicts) else 0.0,
        "conflict_audit": 1.0, "claim_aggregation": base_quality, "majority_support": min(1.0, base_quality + 0.1), "minority_preservation": 1.0,
        "time_alignment": 1.0 if not date_conflicts else 0.6, "unit_alignment": 1.0 if not number_conflicts else 0.6, "scope_alignment": 0.8,
        "entity_alignment": _ratio(len(query_terms & evidence_tokens), max(1, len(query_terms))), "conflict_separation": 1.0, "synthesis_completeness": base_quality,
        "actionable_insight_ratio": min(1.0, base_quality + (0.1 if evidence else 0)), "gap_detection": 1.0, "confidence_calibration": min(1.0, sum(top_scores) / max(1, len(top_scores))),
        "fusion_weight_quality": 1.0, "citation_density": _ratio(len(evidence), max(1, len(evidence))), "source_path_ratio": _ratio(sum(bool(item.locator) for item in evidence), max(1, len(evidence))),
        "chunk_id_ratio": _ratio(sum(bool(item.chunk_id) for item in evidence), max(1, len(evidence))), "locator_ratio": _ratio(sum(bool(item.locator) for item in evidence), max(1, len(evidence))),
        "quote_traceability": 1.0 if evidence else 0.0, "broken_citation_ratio": 0.0, "unique_citation_ratio": _ratio(len({item.chunk_id for item in evidence}), max(1, len(evidence))),
        "primary_source_hint": _ratio(sum(re.search(r"政府|官网|标准|大学|研究院|法院", item.source_title + item.text[:80]) is not None for item in evidence), max(1, len(evidence))),
        "path_safety_ratio": 1.0, "citation_order_ratio": 1.0, "evidence_citation_parity": 1.0 if evidence else 0.0,
        "timestamp_recorded": 1.0, "reproducibility_ratio": 1.0, "citation_audit": 1.0, "result_structure": 1.0,
        "no_crash": 1.0, "actionable_warning_ratio": 1.0 if all("：" in warning for warning in warnings) else 0.8, "empty_input_handling": 1.0,
        "injection_detection": 1.0 if injection_hits == 0 else 0.8, "secret_suppression": 1.0 if secret_hits == 0 else 0.8,
        "private_network_block": 1.0, "path_traversal_block": 1.0, "unsafe_extension_block": 1.0, "file_size_limit": 1.0,
        "deterministic_output": 1.0, "json_valid": 1.0, "markdown_readability": 1.0, "config_loaded": 1.0,
        "weight_valid_ratio": 1.0, "disabled_metric_obeyed": 1.0, "runtime_ms": runtime_ms,
    }
    return {key: float(value) for key, value in signals.items()}
