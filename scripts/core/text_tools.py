# 用途：提供中文友好的文本清洗、分词、切片、指纹和相似度工具。
from __future__ import annotations

import hashlib
import html
import math
import re
import unicodedata
from collections import Counter


FILLER_WORDS = {"请", "帮我", "麻烦", "一下", "进行", "相关", "有关", "想要", "需要", "看看"}
ACTION_WORDS = {"检索", "查找", "比较", "核对", "分析", "总结", "提取", "判断", "评估", "梳理", "找出", "验证"}
RISK_WORDS = {"风险", "合规", "安全", "医疗", "法律", "财务", "投资", "隐私", "敏感"}


def normalize_text(text: str) -> str:
    value = unicodedata.normalize("NFKC", html.unescape(text or ""))
    value = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", " ", value)
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def strip_html(text: str) -> str:
    value = re.sub(r"(?is)<(script|style|noscript).*?>.*?</\1>", " ", text)
    value = re.sub(r"(?i)<br\s*/?>|</p>|</li>|</tr>|</h[1-6]>", "\n", value)
    value = re.sub(r"(?s)<[^>]+>", " ", value)
    return normalize_text(value)


def tokenize(text: str) -> list[str]:
    value = normalize_text(text).lower()
    latin = re.findall(r"[a-z][a-z0-9_+.-]{1,}|\d+(?:\.\d+)?", value)
    cjk_runs = re.findall(r"[\u3400-\u9fff]+", value)
    cjk: list[str] = []
    for run in cjk_runs:
        if len(run) == 1:
            cjk.append(run)
        else:
            cjk.extend(run[i:i + 2] for i in range(len(run) - 1))
    return [token for token in latin + cjk if token not in FILLER_WORDS]


def content_fingerprint(text: str) -> str:
    canonical = re.sub(r"\W+", "", normalize_text(text).lower(), flags=re.UNICODE)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]


def jaccard(left: str, right: str) -> float:
    a, b = set(tokenize(left)), set(tokenize(right))
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def split_chunks(text: str, target: int = 700, overlap: int = 120) -> list[str]:
    value = normalize_text(text)
    if not value:
        return []
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", value) if part.strip()]
    chunks: list[str] = []
    buffer = ""
    for paragraph in paragraphs:
        pieces = re.split(r"(?<=[。！？!?；;])", paragraph) if len(paragraph) > target else [paragraph]
        for piece in pieces:
            if len(buffer) + len(piece) + 1 <= target:
                buffer = f"{buffer}\n{piece}".strip()
            else:
                if buffer:
                    chunks.append(buffer)
                prefix = buffer[-overlap:] if buffer else ""
                buffer = (prefix + "\n" + piece).strip()
                while len(buffer) > target * 2:
                    chunks.append(buffer[:target])
                    buffer = buffer[max(1, target - overlap):]
    if buffer:
        chunks.append(buffer)
    return chunks


def term_frequencies(text: str) -> Counter:
    return Counter(tokenize(text))


def entropy_balance(values: list[int]) -> float:
    positive = [max(0, value) for value in values if value > 0]
    total = sum(positive)
    if not positive or total == 0:
        return 0.0
    if len(positive) == 1:
        return 1.0
    entropy = -sum((value / total) * math.log(value / total) for value in positive)
    return min(1.0, entropy / math.log(len(positive)))


def redact_secrets(text: str) -> str:
    value = re.sub(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*[^\s,;]+", r"\1=[已脱敏]", text)
    value = re.sub(r"\b1[3-9]\d{9}\b", "[手机号已脱敏]", value)
    value = re.sub(r"\b\d{17}[0-9Xx]\b", "[身份证号已脱敏]", value)
    return value
