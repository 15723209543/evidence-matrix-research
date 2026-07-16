# 用途：执行中文友好的查询扩展、BM25 召回、去重与确定性重排。
from __future__ import annotations

import math
import re
from collections import Counter, defaultdict

from core.models import Chunk, SourceDocument
from core.text_tools import ACTION_WORDS, content_fingerprint, jaccard, split_chunks, tokenize


SYNONYMS = {
    "风险": ["隐患", "不确定性", "威胁"], "比较": ["对比", "差异", "优劣"], "原因": ["成因", "驱动因素"],
    "影响": ["作用", "后果", "效果"], "政策": ["规定", "规范", "制度"], "价格": ["费用", "成本", "报价"],
    "企业": ["公司", "机构"], "数据": ["指标", "数值", "统计"], "证据": ["依据", "出处", "来源"],
}


def expand_query(query: str) -> dict:
    terms = tokenize(query)
    expanded = list(terms)
    matched = 0
    for key, values in SYNONYMS.items():
        if key in query:
            matched += 1
            for value in values:
                expanded.extend(tokenize(value))
    subquestions = [part.strip() for part in re.split(r"[？?；;\n]|以及|并且|同时", query) if part.strip()]
    return {"terms": list(dict.fromkeys(terms)), "expanded_terms": list(dict.fromkeys(expanded)), "subquestions": subquestions, "synonym_matches": matched}


def build_chunks(documents: list[SourceDocument]) -> list[Chunk]:
    chunks: list[Chunk] = []
    for document in documents:
        for position, text in enumerate(split_chunks(document.text), start=1):
            chunks.append(Chunk(
                chunk_id=f"{document.source_id}-C{position:03d}", source_id=document.source_id, source_title=document.title,
                locator=document.locator, text=text, fingerprint=content_fingerprint(text), position=position,
            ))
    return chunks


def _bm25(chunks: list[Chunk], terms: list[str]) -> list[float]:
    frequencies = [Counter(tokenize(chunk.text)) for chunk in chunks]
    lengths = [sum(freq.values()) for freq in frequencies]
    average = sum(lengths) / max(1, len(lengths))
    doc_frequency = defaultdict(int)
    for freq in frequencies:
        for term in set(terms) & set(freq):
            doc_frequency[term] += 1
    scores: list[float] = []
    for freq, length in zip(frequencies, lengths):
        score = 0.0
        for term in terms:
            count = freq.get(term, 0)
            if not count:
                continue
            inverse = math.log(1 + (len(chunks) - doc_frequency[term] + 0.5) / (doc_frequency[term] + 0.5))
            score += inverse * count * 2.5 / (count + 1.5 * (1 - 0.75 + 0.75 * length / max(1, average)))
        scores.append(score)
    return scores


def retrieve(query: str, chunks: list[Chunk], top_k: int = 12) -> tuple[list[Chunk], dict]:
    expansion = expand_query(query)
    terms = expansion["expanded_terms"]
    raw_scores = _bm25(chunks, terms)
    query_lower = query.lower()
    query_tokens = set(expansion["terms"])
    for chunk, raw in zip(chunks, raw_scores):
        tokens = set(tokenize(chunk.text))
        overlap = len(tokens & query_tokens) / max(1, len(query_tokens))
        phrase = 1.0 if len(query) >= 4 and query_lower in chunk.text.lower() else 0.0
        title_hit = len(set(tokenize(chunk.source_title)) & query_tokens) / max(1, len(query_tokens))
        proximity = 0.0
        positions = [chunk.text.lower().find(term) for term in expansion["terms"] if chunk.text.lower().find(term) >= 0]
        if len(positions) >= 2:
            proximity = 1 / (1 + (max(positions) - min(positions)) / 80)
        chunk.features = {"bm25": raw, "overlap": overlap, "phrase": phrase, "title": title_hit, "proximity": proximity}
        chunk.score = raw + overlap * 2.0 + phrase * 1.2 + title_hit * 0.8 + proximity * 0.6
    ranked = sorted(chunks, key=lambda item: (-item.score, item.source_id, item.position))
    selected: list[Chunk] = []
    for candidate in ranked:
        if candidate.score <= 0 and selected:
            continue
        if any(jaccard(candidate.text, kept.text) >= 0.92 for kept in selected):
            continue
        selected.append(candidate)
        if len(selected) >= top_k:
            break
    max_score = max((item.score for item in selected), default=1.0)
    for item in selected:
        item.score = round(item.score / max_score, 6) if max_score else 0.0
    return selected, expansion
