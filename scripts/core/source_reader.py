# 用途：安全读取多种本地文件和公开网页，并转换为统一来源文档。
from __future__ import annotations

import csv
import io
import json
import re
import urllib.request
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from core.models import SourceDocument
from core.security import MAX_FILE_BYTES, MAX_URL_BYTES, SafetyError, discover_files, validate_url
from core.text_tools import content_fingerprint, normalize_text, redact_secrets, strip_html


TEXT_EXTENSIONS = {".txt", ".md", ".csv", ".tsv", ".json", ".xml", ".yaml", ".yml", ".log"}


def _decode(data: bytes) -> tuple[str, str]:
    for encoding in ("utf-8-sig", "utf-8", "gb18030", "big5", "latin-1"):
        try:
            return data.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace"), "utf-8-replace"


def _docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    return "\n".join("".join(node.text or "" for node in paragraph.iter() if node.tag.endswith("}t")) for paragraph in root.iter() if paragraph.tag.endswith("}p"))


def _xlsx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in archive.namelist():
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared = ["".join(node.text or "" for node in item.iter() if node.tag.endswith("}t")) for item in root if item.tag.endswith("}si")]
        lines: list[str] = []
        for name in sorted(item for item in archive.namelist() if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", item)):
            root = ET.fromstring(archive.read(name))
            for row in (node for node in root.iter() if node.tag.endswith("}row")):
                values: list[str] = []
                for cell in (node for node in row if node.tag.endswith("}c")):
                    value = next((node for node in cell if node.tag.endswith("}v")), None)
                    raw = value.text if value is not None and value.text else ""
                    if cell.attrib.get("t") == "s" and raw:
                        raw = shared[int(raw)]
                    values.append(raw)
                if values:
                    lines.append("\t".join(values))
    return "\n".join(lines)


def _pdf_text(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("缺少可选依赖 pypdf，已跳过 PDF") from exc
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def read_path(path: Path, index: int) -> SourceDocument:
    if path.stat().st_size > MAX_FILE_BYTES:
        raise SafetyError(f"文件超过 20 MB：{path.name}")
    extension = path.suffix.lower()
    encoding = "binary-parser"
    if extension == ".docx":
        text = _docx_text(path)
    elif extension == ".xlsx":
        text = _xlsx_text(path)
    elif extension == ".pdf":
        text = _pdf_text(path)
    else:
        raw, encoding = _decode(path.read_bytes())
        text = strip_html(raw) if extension in {".html", ".htm"} else normalize_text(raw)
    text = redact_secrets(text)
    return SourceDocument(
        source_id=f"S{index:03d}", title=path.stem, locator=str(path), source_type=extension.lstrip("."),
        text=text, fingerprint=content_fingerprint(text), metadata={"encoding": encoding, "size": path.stat().st_size},
    )


def read_url(url: str, index: int) -> SourceDocument:
    validate_url(url)
    request = urllib.request.Request(url, headers={"User-Agent": "EvidenceMatrixSkill/1.0"})
    with urllib.request.urlopen(request, timeout=12) as response:
        final_url = response.geturl()
        validate_url(final_url)
        data = response.read(MAX_URL_BYTES + 1)
        if len(data) > MAX_URL_BYTES:
            raise SafetyError("网页响应超过 5 MB")
        raw, encoding = _decode(data)
    title_match = re.search(r"(?is)<title[^>]*>(.*?)</title>", raw)
    title = strip_html(title_match.group(1)) if title_match else final_url
    text = redact_secrets(strip_html(raw))
    return SourceDocument(
        source_id=f"S{index:03d}", title=title[:160], locator=final_url, source_type="web",
        text=text, fingerprint=content_fingerprint(text), metadata={"encoding": encoding, "size": len(data)},
    )


def load_sources(paths: list[str], urls: list[str]) -> tuple[list[SourceDocument], list[str]]:
    documents: list[SourceDocument] = []
    warnings: list[str] = []
    candidates = discover_files(paths)
    for candidate in candidates:
        try:
            document = read_path(candidate, len(documents) + 1)
            if document.text.strip():
                documents.append(document)
            else:
                warnings.append(f"空内容：{candidate.name}")
        except Exception as exc:
            warnings.append(f"读取失败 {candidate.name}：{exc}")
    for url in urls:
        try:
            documents.append(read_url(url, len(documents) + 1))
        except Exception as exc:
            warnings.append(f"网页读取失败 {url}：{exc}")
    return documents, warnings
