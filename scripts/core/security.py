# 用途：校验 URL、文件路径、扩展名和输入规模，阻断内网访问及明显越权风险。
from __future__ import annotations

import ipaddress
import socket
from pathlib import Path
from urllib.parse import urlparse


ALLOWED_EXTENSIONS = {".txt", ".md", ".csv", ".tsv", ".json", ".html", ".htm", ".xml", ".yaml", ".yml", ".log", ".docx", ".xlsx", ".pdf"}
MAX_FILE_BYTES = 20 * 1024 * 1024
MAX_URL_BYTES = 5 * 1024 * 1024
MAX_FILES = 500


class SafetyError(ValueError):
    pass


def validate_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise SafetyError("URL 仅允许 http/https 且必须包含主机名")
    if parsed.username or parsed.password:
        raise SafetyError("URL 不得包含用户名或密码")
    host = parsed.hostname.lower()
    if host in {"localhost", "localhost.localdomain"} or host.endswith(".local"):
        raise SafetyError("拒绝访问本机或本地域名")
    try:
        addresses = {item[4][0] for item in socket.getaddrinfo(host, parsed.port or (443 if parsed.scheme == "https" else 80))}
    except socket.gaierror as exc:
        raise SafetyError(f"域名解析失败：{host}") from exc
    for address in addresses:
        ip = ipaddress.ip_address(address)
        if not ip.is_global:
            raise SafetyError(f"拒绝访问非公网地址：{address}")
    return url


def discover_files(inputs: list[str]) -> list[Path]:
    files: list[Path] = []
    seen: set[Path] = set()
    for raw in inputs:
        path = Path(raw).expanduser().resolve()
        candidates = [path] if path.is_file() else sorted(path.rglob("*")) if path.is_dir() else []
        for candidate in candidates:
            if not candidate.is_file() or candidate.is_symlink() or candidate.suffix.lower() not in ALLOWED_EXTENSIONS:
                continue
            resolved = candidate.resolve()
            if resolved not in seen:
                seen.add(resolved)
                files.append(resolved)
            if len(files) >= MAX_FILES:
                return files
    return files
