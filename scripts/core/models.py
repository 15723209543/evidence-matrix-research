# 用途：定义来源文档、文本片段、证据和冲突记录的数据模型。
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class SourceDocument:
    source_id: str
    title: str
    locator: str
    source_type: str
    text: str
    fingerprint: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["text"] = self.text[:1000]
        return data


@dataclass
class Chunk:
    chunk_id: str
    source_id: str
    source_title: str
    locator: str
    text: str
    fingerprint: str
    position: int
    score: float = 0.0
    features: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Conflict:
    conflict_id: str
    kind: str
    subject: str
    left: dict[str, Any]
    right: dict[str, Any]
    severity: float
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
