# MentorForge.skill

> 学术铸师：把公开论文和学术轨迹，蒸馏成一个可追问、可批判、可迭代的科研导师 Skill。

MentorForge.skill 是一个面向科研场景的 Agent Skill。它不会把真实学者伪装成聊天角色，而是从公开证据中提取一套可运行的研究操作系统：问题品味、方法论、实验标准、写作偏好、反模式和边界。

当前 Codex skill id：`research-mentor-distiller`

## 它解决什么问题

很多时候，我们真正想学习的不是某位老师说过哪句话，而是：

- 他为什么认为这个问题值得做？
- 他会怎样把一个模糊想法改写成可发表的研究问题？
- 他相信什么样的数据、实验、消融和基线？
- 他在哪些方向上使用同一套底层方法论？
- 他在不同研究方向下又会采用什么不同打法？

MentorForge.skill 的目标是把这些隐含判断显式化，生成一个证据约束下的“赛博导师”。

## 核心能力

- 多源论文采集：主页、arXiv、OpenAlex、Semantic Scholar、Crossref。
- 开放 PDF 下载：优先抓取合法公开 PDF，并记录失败项。
- Agent fallback 队列：脚本失败时生成手动搜索任务，让 Agent 继续补源。
- 全文精度蒸馏：从 PDF 提取全文、section、paper signal card 和 methodology workbench。
- 跨方向方法论总结：提炼不同方向共同出现的问题框架、数据策略、方法模式和验证标准。
- 方向特定 playbook：按研究方向分别总结打法，不强行压成一个泛泛人格。
- 证据置信度标注：区分 direct evidence、strong inference、speculative extension。
- 安全边界：不冒充真实学者，不推断私人观点，不使用未授权材料。

## 快速开始

当前仓库结构中，实际 Skill 位于：

```text
research-mentor-distiller/
```

在 Codex 中使用时，把该目录放入你的 skills 目录，或在当前工作区中让 Agent 显式使用它。

典型请求：

```text
使用 MentorForge.skill，帮我蒸馏上海交通大学谢伟迪老师的研究品味和方法论。
```

如果你已经有目标老师主页：

```bash
python research-mentor-distiller/scripts/collect_publications.py \
  --scholar-name "Weidi Xie" \
  --homepage "https://weidixie.github.io/" \
  --output-dir source_materials/weidi-xie/publications \
  --download-pdfs \
  --max-pdfs 30
```

然后进行全文抽取：

```bash
python research-mentor-distiller/scripts/extract_fulltext.py \
  --publication-index source_materials/weidi-xie/publications/publication-index.json \
  --output-dir source_materials/weidi-xie/fulltext \
  --max-papers 40 \
  --overwrite
```

## 工作流

1. 定义目标：学者、主页、机构、研究方向和使用场景。
2. 自动采集：先跑 `collect_publications.py` 建立 publication index。
3. 检查报告：阅读 `crawl-report.md`，确认作者歧义、源覆盖和 PDF 覆盖。
4. 手动补源：根据 `agent-fallback-queue.md` 让 Agent 用搜索/浏览器补缺。
5. 全文抽取：用 `extract_fulltext.py` 生成全文、信号卡和工作台。
6. 证据蒸馏：先做 per-paper signal，再做 cross-paper synthesis。
7. 生成导师 Skill：输出 grounding contract、research taste、core methodology、direction playbooks 和 task workflows。
8. 验证：做 evidence、recurrence、full-text、generative、boundary 五类检查。

## 输出质量分级

- v0 homepage/profile distillation：可用脚手架，方法论分辨率低。
- v1 title/abstract distillation：能看出研究品味，但实验细节不足。
- v2 full-paper distillation：能可靠总结方法论和评价标准。
- v3 validated cyber mentor：已在已知/未知研究任务上测试过。

## 项目结构

```text
mentor-distiller-skill/
  README.md
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

## 关键脚本

`collect_publications.py`

采集公开 publication metadata，合并主页、arXiv、OpenAlex、Semantic Scholar 和 Crossref，并可下载开放 PDF。输出：

- `publication-index.md`
- `publication-index.json`
- `crawl-report.md`
- `agent-fallback-queue.md`
- `papers/`

`extract_fulltext.py`

从开放 PDF 中提取全文并生成蒸馏材料。输出：

- `fulltext/`
- `paper-signal-cards/`
- `distillation-workbench.md`
- `extraction-report.md`
- `fulltext-index.json`

## API 和环境变量

可选环境变量：

```bash
SEMANTIC_SCHOLAR_API_KEY=...
OPENALEX_API_KEY=...
OPENALEX_MAILTO=you@example.com
CROSSREF_MAILTO=you@example.com
```

脚本默认会优先使用安全 HTTPS 验证和 `certifi`。`--allow-insecure-ssl` 只适合本机证书链损坏时的最后兜底。

## 伦理边界

MentorForge.skill 只使用公开或用户有权提供的材料。生成的导师 Skill 是“研究思维蒸馏”，不是本人分身。

它必须明确：

- 不代表真实学者的私人观点。
- 不代表招生、评审或未公开研究判断。
- 不推断敏感个人属性。
- 不使用未授权论文全文、邮件、私聊或学生材料。
- 重要推断必须标注证据和置信度。

## 当前状态

已完成基础版：

- 主页采集测试：谢伟迪老师主页采集到 160 条 publication。
- PDF 下载测试：arXiv 开放 PDF 下载成功。
- 全文抽取测试：成功生成 signal card 和 distillation workbench。
- Skill 校验：`quick_validate.py` 通过。

## License

MIT License. See `LICENSE`.
