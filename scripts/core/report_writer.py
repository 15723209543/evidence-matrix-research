# 用途：生成带证据、冲突、指标分数和复现信息的 Markdown/JSON 双格式报告。
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def _escape(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def write_reports(output_dir: Path, payload: dict) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "report.json"
    md_path = output_dir / "report.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    evidence = payload["evidence"]
    conflicts = payload["conflicts"]
    metrics = payload["metrics"]
    lines = [
        "# 证据矩阵检索研判报告", "", f"- 查询：{payload['query']}", f"- 综合质量分：{payload['overall_score']:.2f}/100",
        f"- 置信等级：{payload['confidence_label']}", f"- 有效来源：{payload['summary']['source_count']} 个",
        f"- 证据片段：{len(evidence)} 条", f"- 矛盾项：{len(conflicts)} 项", f"- 生成时间：{payload['generated_at']}", "",
        "## 结论摘要", "",
    ]
    if evidence:
        for item in evidence[:5]:
            lines.append(f"- {_escape(item['text'][:260])} [{item['source_id']}#{item['chunk_id']}]")
    else:
        lines.append("当前材料不足以支持结论。请补充与查询相关的来源文件或公开网页。")
    lines += ["", "## 关键证据", "", "| 排名 | 得分 | 来源 | 片段 | 证据摘录 |", "|---:|---:|---|---|---|"]
    for index, item in enumerate(evidence, start=1):
        lines.append(f"| {index} | {item['score']:.3f} | {_escape(item['source_title'])} | {item['chunk_id']} | {_escape(item['text'][:320])} |")
    lines += ["", "## 矛盾与口径差异", ""]
    if conflicts:
        for item in conflicts:
            lines += [
                f"### {item['conflict_id']} {item['kind']}：{_escape(item['subject'])}", "",
                f"- 证据 A：{_escape(item['left'].get('quote', ''))} [{item['left'].get('source_id')}#{item['left'].get('chunk_id')}]",
                f"- 证据 B：{_escape(item['right'].get('quote', ''))} [{item['right'].get('source_id')}#{item['right'].get('chunk_id')}]",
                f"- 研判：{item['explanation']}", "",
            ]
    else:
        lines.append("未发现达到规则阈值的显式矛盾；这不等于来源之间必然一致。")
    lines += ["", "## 信息缺口", ""]
    if payload["gaps"]:
        lines.extend(f"- {gap}" for gap in payload["gaps"])
    else:
        lines.append("- 当前检索覆盖未显示明显结构性缺口。")
    lines += ["", "## 指标概览", "", "| 指标 | 类别 | 得分 | 影响系数 | 加权贡献 |", "|---|---|---:|---:|---:|"]
    for item in sorted(metrics, key=lambda row: (-row["weight"], row["score"]))[:25]:
        lines.append(f"| {item['id']} {item['name']} | {item['category_zh']} | {item['score']:.2f} | {item['weight']:.2f} | {item['contribution']:.4f} |")
    lines += ["", "## 告警", ""]
    lines.extend(f"- {warning}" for warning in payload["warnings"]) if payload["warnings"] else lines.append("- 无。")
    lines += ["", "## 来源清单", ""]
    for source in payload["sources"]:
        lines.append(f"- {source['source_id']}｜{source['title']}｜{source['locator']}｜指纹 {source['fingerprint']}")
    lines += ["", "---", "指标影响系数在本次执行开始时从 `references/metrics/参考指标配置.xlsx` 第一列读取。"]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return md_path, json_path
