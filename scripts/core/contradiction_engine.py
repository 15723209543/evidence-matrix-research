# 用途：识别跨来源的数值、日期和肯否冲突，并保留双方证据。
from __future__ import annotations

import re
from collections import defaultdict

from core.models import Chunk, Conflict
from core.text_tools import tokenize


NUMBER_PATTERN = re.compile(r"(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>%|亿元|万元|元|万人|人|万家|家|万项|项|倍|GB|MB)")
DATE_PATTERN = re.compile(r"(?P<label>[\u4e00-\u9fffA-Za-z]{2,16})[^。！？\n]{0,16}?(?P<value>20\d{2}[年/-]\d{1,2}(?:[月/-]\d{1,2}日?)?)")
NEGATIVE = {"不是", "没有", "未", "否认", "下降", "减少", "不支持", "禁止"}
POSITIVE = {"是", "具有", "支持", "上升", "增加", "允许", "确认"}


def _anchor(label: str) -> str:
    tokens = tokenize(label)
    return "|".join(tokens[-3:]) if tokens else label[-6:]


def detect_conflicts(evidence: list[Chunk]) -> list[Conflict]:
    conflicts: list[Conflict] = []
    buckets: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for chunk in evidence:
        for match in NUMBER_PATTERN.finditer(chunk.text):
            context_start = max(0, match.start() - 50)
            context_end = min(len(chunk.text), match.end() + 20)
            context_text = chunk.text[context_start:context_end]
            context_tokens = set(tokenize(re.sub(r"\d+(?:\.\d+)?", "", context_text)))
            buckets[("数值冲突", match.group("unit"))].append({
                "value": match.group("value") + match.group("unit"), "numeric": float(match.group("value")),
                "tokens": sorted(context_tokens), "source_id": chunk.source_id, "chunk_id": chunk.chunk_id,
                "locator": chunk.locator, "quote": context_text[:180],
            })
        for match in DATE_PATTERN.finditer(chunk.text):
            buckets[("日期冲突", _anchor(match.group("label")))].append({
                "value": match.group("value"), "source_id": chunk.source_id, "chunk_id": chunk.chunk_id,
                "locator": chunk.locator, "quote": match.group(0)[:180],
            })
    serial = 1
    for (kind, subject), claims in buckets.items():
        for left_index, left in enumerate(claims):
            for right in claims[left_index + 1:]:
                related = True
                if kind == "数值冲突":
                    left_tokens, right_tokens = set(left.get("tokens", [])), set(right.get("tokens", []))
                    related = len(left_tokens & right_tokens) / max(1, min(len(left_tokens), len(right_tokens))) >= 0.2
                if left["source_id"] != right["source_id"] and left["value"] != right["value"] and related:
                    left_view = {key: value for key, value in left.items() if key not in {"tokens", "numeric"}}
                    right_view = {key: value for key, value in right.items() if key not in {"tokens", "numeric"}}
                    conflicts.append(Conflict(
                        conflict_id=f"X{serial:03d}", kind=kind, subject=subject or "同类主张", left=left_view, right=right_view,
                        severity=0.8 if kind == "数值冲突" else 0.7, explanation="不同来源对同一近似主张给出不同取值，需要核对口径、时间和来源层级。",
                    ))
                    serial += 1
    for left_index, left in enumerate(evidence):
        left_tokens = set(tokenize(left.text))
        left_neg = any(word in left.text for word in NEGATIVE)
        left_pos = any(word in left.text for word in POSITIVE)
        for right in evidence[left_index + 1:]:
            if left.source_id == right.source_id:
                continue
            overlap = len(left_tokens & set(tokenize(right.text))) / max(1, len(left_tokens))
            right_neg = any(word in right.text for word in NEGATIVE)
            right_pos = any(word in right.text for word in POSITIVE)
            if overlap >= 0.35 and ((left_neg and right_pos) or (left_pos and right_neg)):
                conflicts.append(Conflict(
                    conflict_id=f"X{serial:03d}", kind="肯否冲突", subject="相近语义主张",
                    left={"source_id": left.source_id, "chunk_id": left.chunk_id, "locator": left.locator, "quote": left.text[:180]},
                    right={"source_id": right.source_id, "chunk_id": right.chunk_id, "locator": right.locator, "quote": right.text[:180]},
                    severity=0.6, explanation="两条相近语义证据出现相反极性，请人工复核适用范围。",
                ))
                serial += 1
    return conflicts[:50]
