# 用途：按 Astron SkillHub 当前公开校验规则检查待上传 Skill 源目录或 ZIP 包。
from __future__ import annotations

import argparse
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable


MAX_FILE_COUNT = 500
MAX_SINGLE_FILE_SIZE = 10 * 1024 * 1024
MAX_TOTAL_PACKAGE_SIZE = 100 * 1024 * 1024
REQUIRED_ENTRY = "SKILL.md"
ALLOWED_EXTENSIONS = {
    ".md", ".txt", ".json", ".yaml", ".yml", ".html", ".css", ".csv", ".pdf",
    ".toml", ".xml", ".xsd", ".xsl", ".dtd", ".ini", ".cfg", ".env",
    ".js", ".cjs", ".mjs", ".ts", ".py", ".sh", ".rb", ".go", ".rs", ".java", ".kt",
    ".lua", ".sql", ".r", ".bat", ".ps1", ".zsh", ".bash",
    ".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp", ".ico",
    ".doc", ".xls", ".ppt", ".docx", ".xlsx", ".pptx",
}
TEXT_EXTENSIONS = {
    ".md", ".txt", ".json", ".yaml", ".yml", ".html", ".css", ".csv", ".toml", ".xml",
    ".xsd", ".xsl", ".dtd", ".ini", ".cfg", ".env", ".js", ".cjs", ".mjs", ".ts", ".py",
    ".sh", ".rb", ".go", ".rs", ".java", ".kt", ".lua", ".sql", ".r", ".bat", ".ps1",
    ".zsh", ".bash", ".svg",
}
PLACEHOLDER = re.compile(
    r"(?i).*(your|example|sample|placeholder|changeme|replace|dummy|mock|test|fake|todo|xxx|redacted).*"
)
SECRET_RULES = (
    (re.compile(r"AKIA[0-9A-Z]{16}"), "云访问密钥"),
    (re.compile(r"ghp_[A-Za-z0-9]{20,}"), "代码托管令牌"),
    (re.compile(r"sk-[A-Za-z0-9]{20,}"), "API 密钥"),
    (
        re.compile(
            r"(?i)(?:api[_-]?key|access[_-]?key|secret|password|token)\s*[:=]\s*['\"]?([A-Za-z0-9_\-]{12,})"
        ),
        "密钥或令牌",
    ),
)


@dataclass(frozen=True)
class Entry:
    path: str
    content: bytes


def _normalize_path(raw_path: str) -> str:
    path = raw_path.replace("\\", "/").strip()
    if not path or path.startswith("/") or ":" in path:
        raise ValueError(f"非法包路径：{raw_path}")
    pure = PurePosixPath(path)
    if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
        raise ValueError(f"非法包路径：{raw_path}")
    return pure.as_posix()


def _read_directory(root: Path) -> list[Entry]:
    return [
        Entry(path.relative_to(root).as_posix(), path.read_bytes())
        for path in sorted(root.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    ]


def _read_zip(path: Path) -> list[Entry]:
    entries: list[Entry] = []
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            with archive.open(info) as stream:
                entries.append(Entry(info.filename, stream.read(MAX_SINGLE_FILE_SIZE + 1)))
    return entries


def _frontmatter_errors(content: str) -> list[str]:
    if not content.startswith("---"):
        return ["SKILL.md 缺少 frontmatter 起始分隔线"]
    match = re.match(r"^---\s*\n(.*?)\n---(?:\s*\n|$)", content, re.DOTALL)
    if not match:
        return ["SKILL.md frontmatter 未正确闭合"]
    fields: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        if ":" not in raw_line or raw_line.lstrip().startswith("#"):
            continue
        key, value = raw_line.split(":", 1)
        fields[key.strip()] = value.strip().strip("'\"")
    errors = []
    for key in ("name", "description"):
        if not fields.get(key):
            errors.append(f"SKILL.md frontmatter 缺少非空字段：{key}")
    version = fields.get("version")
    if version and not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", version):
        errors.append("SKILL.md version 不是语义化版本号")
    return errors


def _secret_warnings(path: str, text: str) -> Iterable[str]:
    for line_number, line in enumerate(text.splitlines(), 1):
        for rule, label in SECRET_RULES:
            match = rule.search(line)
            if not match:
                continue
            value = match.group(match.lastindex or 0)
            if PLACEHOLDER.fullmatch(value) or set(value) <= {"x", "X", "*", "-"}:
                continue
            yield f"{path}:{line_number} 疑似包含{label}"
            break


def validate(entries: list[Entry]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    normalized: dict[str, Entry] = {}
    total_size = 0

    if len(entries) > MAX_FILE_COUNT:
        errors.append(f"文件数 {len(entries)} 超过上限 {MAX_FILE_COUNT}")

    for entry in entries:
        try:
            normalized_path = _normalize_path(entry.path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if normalized_path in normalized:
            errors.append(f"包内路径重复：{normalized_path}")
            continue
        normalized[normalized_path] = entry
        size = len(entry.content)
        total_size += size
        if size > MAX_SINGLE_FILE_SIZE:
            errors.append(f"单文件超过 10MB：{normalized_path}")

        suffix = PurePosixPath(normalized_path).suffix.lower()
        if suffix not in ALLOWED_EXTENSIONS:
            warnings.append(f"扩展名不在 Astron SkillHub 允许清单：{normalized_path}")
        if suffix in TEXT_EXTENSIONS:
            try:
                text = entry.content.decode("utf-8")
            except UnicodeDecodeError:
                errors.append(f"文本文件不是 UTF-8：{normalized_path}")
            else:
                warnings.extend(_secret_warnings(normalized_path, text))

    if total_size > MAX_TOTAL_PACKAGE_SIZE:
        errors.append(f"包内文件总大小超过 100MB：{total_size} 字节")
    if REQUIRED_ENTRY not in normalized:
        errors.append("ZIP 根目录缺少大写 SKILL.md")
    else:
        try:
            skill_text = normalized[REQUIRED_ENTRY].content.decode("utf-8-sig")
        except UnicodeDecodeError:
            errors.append("SKILL.md 不是 UTF-8")
        else:
            errors.extend(_frontmatter_errors(skill_text))
    return errors, warnings


def main() -> int:
    default_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description="检查 Astron SkillHub Skill 源目录或 ZIP 包")
    parser.add_argument("target", nargs="?", type=Path, default=default_root)
    args = parser.parse_args()
    target = args.target.resolve()

    if target.is_dir():
        entries = _read_directory(target)
    elif target.is_file() and target.suffix.lower() == ".zip":
        entries = _read_zip(target)
    else:
        print(f"错误：目标不是 Skill 目录或 ZIP：{target}", file=sys.stderr)
        return 2

    errors, warnings = validate(entries)
    print(f"Astron SkillHub 自检：文件 {len(entries)} 个，错误 {len(errors)} 个，警告 {len(warnings)} 个")
    for item in errors:
        print(f"[错误] {item}")
    for item in warnings:
        print(f"[警告] {item}")
    if not errors and not warnings:
        print("通过：包结构与公开校验规则一致。")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
