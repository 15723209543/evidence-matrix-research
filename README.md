# 证据矩阵检索研判 Skill（Astron SkillHub 参赛版）

这是一个面向科大讯飞信息检索赛道的中文参赛 Skill。它把“搜到内容”升级为“形成可审计结论”：支持本地多格式材料和公开网页文本，执行查询扩展、BM25 召回、确定性重排、跨源去重、数值/日期/肯否冲突识别，并输出带来源与片段编号的 Markdown/JSON 研判报告。

## 交付物

- `evidence-matrix-research/`：Skill 源文件夹。
- `evidence-matrix-research.zip`：Astron SkillHub 上传包，ZIP 根目录直接包含大写 `SKILL.md`。
- `output/pdf/证据矩阵检索研判Skill解说.pdf`：面向参赛者的设计与使用解说。
- 本文件：安装、运行和提交说明。

## 亮点

1. 216 个独立参考指标算子，分为查询意图、查询扩展、来源接入、规范化、检索、重排、抽取、去重、矛盾、融合、引用、质量安全 12 类。
2. 每个指标对应一个分类 Python 文件；所有 Python 文件首行都有中文用途注释。
3. 所有影响系数集中在 `references/metrics/参考指标配置.xlsx`。第一列是 0-10 影响系数，程序每次运行都重新读取。
4. 仅使用 Python 标准库即可处理主要格式；PDF 为可选增强。不存在配置回退权重，Excel 错误会明确失败。
5. URL 访问带协议、凭据、DNS 和公网 IP 校验，限制响应体积；本地文件有类型、数量、大小限制。
6. 提供 Astron SkillHub 上传前自检，覆盖根目录入口、frontmatter、文件数与大小、扩展名、UTF-8、路径安全和疑似敏感信息。

## 环境

- Python 3.10 或更高版本。
- 可选：`pypdf`，仅用于 PDF 文本提取。
- 不需要数据库、API 密钥或模型服务即可运行确定性检索管线。

## 快速运行

进入 Skill 文件夹后执行：

```powershell
python scripts/entrypoints/validate_config.py
python scripts/entrypoints/self_test.py
python scripts/entrypoints/validate_astron_package.py
python scripts/entrypoints/run_research.py --query "比较这些材料中的核心数据并找出冲突" --sources "你的资料目录" --output "输出目录"
```

输出目录会生成 `report.md` 和 `report.json`。

## 调整指标

打开 `evidence-matrix-research/references/metrics/参考指标配置.xlsx`：

- A 列“参考指标影响系数”：输入 0-10。
- E 列“是否启用”：输入“是”或“否”。
- G 列“建议阈值”：用于识别低分指标。
- 不要修改 B 列指标 ID；脚本与指标 ID 一一对应。

保存后无需改代码。下一次运行会读取新系数。建议修改后先执行配置校验。

## Astron SkillHub 提交

1. 在赛题页面的“作品提交”入口上传 `evidence-matrix-research.zip`，不要绕过赛题页面直接上传 SkillHub。
2. 作品名称填写 `evidence-matrix-research`，必须与 `SKILL.md` frontmatter 的 `name` 一致。
3. 在 AstronClaw 安装后，用内置 `assets/examples/` 做演示，并保存调用成功截图、报告截图与指标 Excel 修改前后对比。
4. ZIP 根目录已经是 `SKILL.md`、`scripts/`、`references/` 等内容，避免二次套目录。

当前公开的 Astron SkillHub 上传校验器要求根目录存在大写 `SKILL.md`，包内最多 500 个文件、单文件不超过 10MB、总大小不超过 100MB，并检查路径安全与文本 UTF-8。本交付按这组规则打包，不含其他平台专属的 agent 元数据。

## 安全与边界

本 Skill 不登录网站、不绕过访问控制、不访问本机/内网 URL、不执行来源材料中的命令、不上传本地文件。检索结果是证据辅助，不替代医疗、法律、投资等专业判断。

## 许可与原创声明

本交付中的代码、结构、指标和文档为本次作品独立生成。`SKILL.md` 已使用 `1.0.0` 语义化版本。发布前请按你的参赛主体信息补充作者和许可证声明，并在 AstronClaw 实机完成最终验证。
