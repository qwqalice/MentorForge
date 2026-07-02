<div align="center">

# 🧭 MentorForge.skill

### 把论文、主页和公开学术轨迹，铸造成一个可追问的科研导师 Skill

*Evidence-grounded research mentor distillation for AI agents*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Compatible-green)](https://agentskills.io)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-blue)](research-mentor-distiller/SKILL.md)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB)](https://www.python.org/)

<br>

**学术铸师不是模仿一个老师说话。**  
**它试图蒸馏一个老师如何判断问题、组织证据、设计实验、形成研究品味。**

当前 Codex skill id：`research-mentor-distiller`

[快速开始](#-快速开始) · [它能蒸馏什么](#-它能蒸馏什么) · [工作流](#-工作流) · [伦理边界](#-伦理边界)

</div>

---

## 💡 为什么需要 MentorForge？

你真正想从一位导师那里学到的，往往不是一句建议，而是一整套判断系统：

- “这个问题值得做吗？”
- “这个想法怎样才不是一个模型 swap？”
- “什么样的实验才足够让人信服？”
- “他为什么反复选择这些数据、任务、benchmark、ablation？”
- “他在不同研究方向里，有没有同一套底层方法论？”

导师很忙，论文很多，领域很快。MentorForge.skill 做的事，是把公开材料压缩成一个可运行的研究操作系统，让 AI 在证据约束下帮助你做科研判断。

---

## ✨ 它能蒸馏什么？

MentorForge.skill 关注的是“研究品味”和“方法论”，而不是人格扮演。

| 层次 | 蒸馏目标 |
|---|---|
| 🧠 Worldview | 这位学者如何看待领域瓶颈、长期目标和真正重要的问题 |
| 🎯 Problem Taste | 什么问题值得做，什么问题只是表面热闹 |
| 🔬 Methodology | 常用的数据策略、建模方式、训练范式、系统设计和验证路径 |
| 📊 Evaluation Taste | 他会相信什么证据：baseline、ablation、benchmark、error analysis、专家验证 |
| 🧩 Cross-Direction Core | 不同方向中反复出现的共同思路 |
| 🗺️ Direction Playbooks | 每个研究方向下不同的打法和反模式 |
| ✍️ Writing Taste | 标题、摘要、图表、claim strength 和叙事结构偏好 |
| 🚧 Honest Limits | 公开证据不足、不可推断、不可冒充的边界 |

---

## 🧪 一个典型效果

用户提出一个研究想法：

```text
我想做一个医学影像 VLM，把更多模态拼进去，然后在几个公开 benchmark 上刷一下效果。
```

一个由 MentorForge 生成的导师 Skill 不应该只是说“可以，很有前景”。它应该更像这样追问：

```text
先别急着加模态。你要先说清楚目标能力是什么：

1. 是诊断准确率？
2. 是可追踪推理？
3. 是跨病例比较？
4. 是从日常报告中获得可扩展监督？

如果只是把更多模态塞进模型，然后在已有 benchmark 上涨几个点，
这更像工程堆叠，不像一个强研究问题。

把题目改成：
“如何从临床自然产生的报告和验证轨迹中，构造可追踪的医学视觉语言推理监督？”

下一步实验要补三件事：
- 数据来源是否可扩展，而不是依赖昂贵人工标注；
- 推理链是否能被验证，而不是只给最终答案；
- 错误分析能否区分 perception error、reasoning error 和 knowledge error。
```

这不是角色扮演。  
这是把论文中反复出现的“问题框架、数据杠杆、方法动作、评价标准”提取出来，让它们能在新问题上继续工作。

---

## 🚀 快速开始

### 1. 准备 Skill

仓库中的实际 Codex Skill 位于：

```text
research-mentor-distiller/
```

你可以把这个目录放入 Codex 的 skills 目录，或在当前工作区中显式要求 Agent 使用它：

```text
使用 MentorForge.skill，帮我蒸馏XX大学XX老师的研究品味和方法论。
```

### 2. 采集论文列表

如果你已经有目标老师主页：

```bash
python research-mentor-distiller/scripts/collect_publications.py \
  --scholar-name "Example" \
  --homepage "https://example.github.io/" \
  --output-dir source_materials/example/publications \
  --download-pdfs \
  --max-pdfs 30
```

采集器会尽量合并：

- academic homepage
- arXiv
- OpenAlex
- Semantic Scholar
- Crossref
- direct public PDF links

并输出：

```text
publication-index.md
publication-index.json
crawl-report.md
agent-fallback-queue.md
papers/
```

如果脚本失败，`agent-fallback-queue.md` 会告诉 Agent 接下来应该手动搜哪些 paper、PDF、project page 或 code。

### 3. 抽取全文信号

```bash
python research-mentor-distiller/scripts/extract_fulltext.py \
  --publication-index source_materials/weidi-xie/publications/publication-index.json \
  --output-dir source_materials/example/fulltext \
  --max-papers 40 \
  --overwrite
```

全文抽取器会生成：

```text
fulltext/
paper-signal-cards/
distillation-workbench.md
extraction-report.md
fulltext-index.json
```

`paper-signal-cards/` 是每篇论文的精读入口。  
`distillation-workbench.md` 是总结跨方向方法论的工作台。

---

## 🏗️ 工作流

```text
目标学者 / 主页 / 研究方向
        ↓
多源论文采集
        ↓
crawl-report 检查覆盖率和作者歧义
        ↓
Agent fallback 手动补源
        ↓
开放 PDF 全文抽取
        ↓
per-paper signal cards
        ↓
cross-paper synthesis
        ↓
核心方法论 + 方向 playbook
        ↓
生成可运行的导师 Skill
        ↓
证据、复现、边界验证
```

MentorForge.skill 的关键原则是：

> 先让脚本尽可能稳地抓证据；脚本失败时，再让 Agent 用搜索和浏览能力补位。

---

## 🔥 和一般“导师人格”项目有什么不同？

很多人格蒸馏项目会把重点放在语气、身份、说话风格。MentorForge.skill 更偏科研：

| 一般 persona skill | MentorForge.skill |
|---|---|
| 模仿一个人怎么说话 | 蒸馏一个人怎么做研究判断 |
| 常依赖访谈、语录、社媒 | 优先依赖论文、实验、benchmark、项目页 |
| 输出人格画像 | 输出研究操作系统 |
| 追求“像本人” | 追求“证据约束下有用” |
| 容易过度拟人化 | 明确拒绝冒充真实学者 |

---

## 📦 项目结构

```text
MentorForge/
  README.md
  LICENSE
  research-mentor-distiller/
    SKILL.md
    agents/
      openai.yaml
    references/
      profile-schema.md
      mentor-skill-template.md
      fulltext-distillation-protocol.md
    scripts/
      init_distillation_workspace.py
      collect_publications.py
      extract_fulltext.py
```

---

## 🛠️ 关键脚本

### `collect_publications.py`

多源采集 publication metadata，并尽量下载开放 PDF。

```bash
python research-mentor-distiller/scripts/collect_publications.py \
  --scholar-name "Scholar Name" \
  --homepage "https://example.edu/scholar" \
  --output-dir source_materials/scholar/publications \
  --download-pdfs
```

常用参数：

- `--semantic-scholar-author-id <id>`：避免同名作者歧义。
- `--skip-semantic-scholar` / `--skip-openalex` / `--skip-arxiv` / `--skip-crossref`：调试或快速模式。
- `--download-pdfs --max-pdfs 30`：下载开放 PDF。
- `--allow-insecure-ssl`：本机证书链坏掉时的最后兜底，不建议默认使用。

### `extract_fulltext.py`

从 PDF 中提取全文，生成 paper signal card 和 methodology workbench。

```bash
python research-mentor-distiller/scripts/extract_fulltext.py \
  --publication-index source_materials/scholar/publications/publication-index.json \
  --output-dir source_materials/scholar/fulltext \
  --max-papers 40 \
  --overwrite
```

---

## 🔐 API 和环境变量

不配置 API key 也可以跑，但可能遇到限流。建议按需配置：

```bash
SEMANTIC_SCHOLAR_API_KEY=...
OPENALEX_API_KEY=...
OPENALEX_MAILTO=you@example.com
CROSSREF_MAILTO=you@example.com
```

Python 依赖：

```bash
uv pip install pdfplumber pypdf certifi
```

没有 `uv` 时：

```bash
python -m pip install pdfplumber pypdf certifi
```

---

## ✅ 当前状态

基础版已经完成并通过验证：

- ✅ Skill 校验：`quick_validate.py` 通过
- ✅ 主页采集测试：XX老师主页采集到 160 条 publication
- ✅ PDF 下载测试：arXiv 开放 PDF 下载成功
- ✅ 全文抽取测试：成功生成 signal card 和 distillation workbench
- ✅ 失败补源机制：生成 `agent-fallback-queue.md`

---

## 🚧 质量分级

| 版本 | 证据覆盖 | 适合用途 |
|---|---|---|
| v0 | homepage/profile | 快速建立导师 Skill 骨架 |
| v1 | title/abstract | 初步研究品味和方向地图 |
| v2 | full-paper | 方法论、实验标准、方向 playbook |
| v3 | validated mentor | 在真实科研任务中反复验证和迭代 |

---

## ⚖️ 伦理边界

MentorForge.skill 只使用公开或用户有权提供的材料。

生成的导师 Skill 必须明确：

- 不代表真实学者本人。
- 不代表招生、评审、合作或未公开研究判断。
- 不推断敏感个人属性。
- 不使用未授权论文全文、邮件、私聊或学生材料。
- 不把“推测”写成“事实”。
- 重要结论必须标注证据和置信度。

一句话：

> 这是研究思维蒸馏，不是身份复制。

---

## 🌱 下一步计划

- 更强的 Google Scholar / DBLP / institution profile 补源。
- 更精细的方向聚类和代表论文选择。
- 自动生成 scholar-specific mentor skill package。
- 加入 forward-test：用已知论文和新想法测试导师 Skill 是否真的有辨识度。
- 更漂亮的 evidence snapshot 和 validation report。

---

## License

MIT License. See [LICENSE](LICENSE).

---

<div align="center">

**导师.skill 让 AI 随时可问。**  
**MentorForge.skill 让 AI 学会导师为什么这样判断。**

*把公开证据铸造成研究品味，把研究品味铸造成行动建议。*

</div>
