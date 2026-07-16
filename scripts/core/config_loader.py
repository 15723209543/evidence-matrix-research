# 用途：每次运行都从 Excel 第一列读取参考指标影响系数并完成严格校验。
from __future__ import annotations

import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main", "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
REL_NS = {"p": "http://schemas.openxmlformats.org/package/2006/relationships"}


class ConfigError(ValueError):
    pass


def _column_index(cell_ref: str) -> int:
    letters = re.match(r"[A-Z]+", cell_ref or "A").group(0)
    result = 0
    for char in letters:
        result = result * 26 + ord(char) - 64
    return result - 1


def _shared_strings(archive: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    return ["".join(node.text or "" for node in item.findall(".//m:t", NS)) for item in root.findall("m:si", NS)]


def _sheet_path(archive: zipfile.ZipFile, wanted: str) -> str:
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    rel_id = None
    for sheet in workbook.findall("m:sheets/m:sheet", NS):
        if sheet.attrib.get("name") == wanted:
            rel_id = sheet.attrib.get(f"{{{NS['r']}}}id")
            break
    if not rel_id:
        raise ConfigError(f"Excel 中缺少工作表：{wanted}")
    rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    for rel in rels.findall("p:Relationship", REL_NS):
        if rel.attrib.get("Id") == rel_id:
            target = rel.attrib["Target"].lstrip("/")
            return target if target.startswith("xl/") else f"xl/{target}"
    raise ConfigError("无法定位参考指标工作表")


def _cell_value(cell: ET.Element, shared: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        return "".join(node.text or "" for node in cell.findall(".//m:t", NS))
    value = cell.find("m:v", NS)
    raw = value.text if value is not None and value.text is not None else ""
    if cell_type == "s" and raw:
        return shared[int(raw)]
    return raw


def load_metric_config(path: str | Path) -> dict[str, dict]:
    config_path = Path(path).expanduser().resolve()
    if not config_path.is_file():
        raise ConfigError(f"参考指标 Excel 不存在：{config_path}")
    with zipfile.ZipFile(config_path) as archive:
        shared = _shared_strings(archive)
        sheet = ET.fromstring(archive.read(_sheet_path(archive, "参考指标")))
        rows: list[list[str]] = []
        for row in sheet.findall(".//m:sheetData/m:row", NS):
            values: list[str] = []
            for cell in row.findall("m:c", NS):
                index = _column_index(cell.attrib.get("r", "A1"))
                while len(values) <= index:
                    values.append("")
                values[index] = _cell_value(cell, shared).strip()
            rows.append(values)
    if not rows:
        raise ConfigError("参考指标工作表为空")
    expected = ["参考指标影响系数", "指标ID", "指标名称", "指标类别", "是否启用"]
    header = rows[0]
    if header[:5] != expected:
        raise ConfigError(f"表头前五列必须为：{'、'.join(expected)}")
    result: dict[str, dict] = {}
    errors: list[str] = []
    for row_number, row in enumerate(rows[1:], start=2):
        row += [""] * (10 - len(row))
        if not any(row):
            continue
        try:
            weight = float(row[0])
        except ValueError:
            errors.append(f"第 {row_number} 行影响系数不是数字")
            continue
        metric_id = row[1].strip()
        if not 0 <= weight <= 10:
            errors.append(f"第 {row_number} 行影响系数 {weight} 超出 0-10")
        if not re.fullmatch(r"M\d{3}", metric_id):
            errors.append(f"第 {row_number} 行指标ID格式错误：{metric_id}")
        if metric_id in result:
            errors.append(f"第 {row_number} 行指标ID重复：{metric_id}")
        enabled = row[4].strip().lower() not in {"否", "false", "0", "停用", "no"}
        result[metric_id] = {
            "weight": weight,
            "name": row[2],
            "category": row[3],
            "enabled": enabled,
            "direction": row[5],
            "threshold": float(row[6] or 60),
            "description": row[7],
            "script": row[8],
            "notes": row[9],
            "row": row_number,
        }
    if errors:
        raise ConfigError("；".join(errors[:20]))
    if len(result) < 200:
        raise ConfigError(f"有效参考指标仅 {len(result)} 个，少于 200 个")
    return result
