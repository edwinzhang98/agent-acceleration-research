# Agent Acceleration Research

Evidence base for a research investigation into why LLM computer-use / web agents are too slow and too expensive for real work, and into the 2023–2026 research landscape on accelerating them. Groundwork for (1) a paper on accelerating repetitive enterprise web workflows (SAP Concur expense reports) and (2) a slide deck for a senior ML audience.

## 网页阅读

**[打开研究阅读首页](https://edwinzhang98.github.io/agent-acceleration-research/)** — 目录、章节搜索、公式排版和手机阅读；也可下载 HTML 离线打开。

| 阅读材料 | 用途 |
|---|---|
| [固定模型权重下的 Agent 加速与自我改进](https://edwinzhang98.github.io/agent-acceleration-research/reports/fixed-weight-agent-acceleration.html) | Codex 专题报告：机制、轨迹学习、环境探索与成本评测。 |
| [自改进 Agent 的文献与 Agent 加速](https://edwinzhang98.github.io/agent-acceleration-research/reports/self-improvement-survey.html) | Claude 文献报告的 Codex 审核阅读版：方法、效果、条件、局限和证据查询。与上篇互补。 |
| [文献自己怎样定义 Agent 加速](https://edwinzhang98.github.io/agent-acceleration-research/reports/how-literature-defines-acceleration.html) | 较新的问题定义研究；讨论稿，含两批独立记录审计，审计范围和待决事项见原文。 |
| [文献里的公式：算速度和成本的](https://edwinzhang98.github.io/agent-acceleration-research/reports/formulas-for-speed-and-cost.html) | 公式与符号手册；2026-09-28 快照。 |
| [Codex 研究计划](https://edwinzhang98.github.io/agent-acceleration-research/reports/trajectory-research-plan.html) · [Claude 第六稿计划](https://edwinzhang98.github.io/agent-acceleration-research/reports/claude-part3-plan.html) | 2026-09-29 讨论稿，方法、实验及预算尚未定案；尚未合并之后的全部审核。 |
| [Agent Acceleration 演示稿](https://edwinzhang98.github.io/agent-acceleration-research/slides/agent-acceleration.html) | Part 1–2 的按页演示。 |

Markdown 原稿在 `notes/`，审核和证据在 `research/`，演示源稿在 `slides/`；`docs/` 是统一网页入口和生成结果。新增四篇仅转换展示，不代表重新审核论文。构建与维护见 [阅读站说明](tools/reading-site/README.md)。

## Layout

| Path | What it is |
|---|---|
| `CLAUDE.md` | Rules every Claude session follows in this repo (auto-loaded by Claude Code; the Claude Project's instructions point here). Single source of truth for the working rules below. |
| `STATUS.md` | **Start here.** One-screen index: current canonical version, what is done, what the next thread should do, log. Updated at the end of every thread. |
| `research/` | Thread outputs (verification results, follow-up research), one file per thread in patch format. Created on first use. |
| `notes/` | Reader-facing Markdown reports and research-plan drafts, grouped into Part 1 (problem and formulas), Part 2 (acceleration literature), and Part 3 (self-improvement and research plans). |
| `docs/` | Generated GitHub Pages reading site: homepage, six full reports, and the existing slide deck. Sources remain in `notes/` and `slides/`; regenerate with `tools/reading-site/build.mjs`. |
| `Agent-Acceleration-Consolidated-Dossier-v3-2026-09-27.md` | **Canonical document.** Cross-validated synthesis of all 16 research outputs plus the six follow-up investigations: evidence ledger (E1–E211), inference→agent mapping, 8-family landscape, evaluation protocol and API budget, novelty assessment, discrepancy ledger (D1–D140), provider scorecard, verification queue and follow-up research prompts. |
| `slides/` | Slide deck built from dossier v3 (`agent-acceleration.html`, generator `build_deck.py`, conventions in `slides/README.md`) and its references: `references.md` is the deck's curated list (author–year scheme, source-credibility rule); `references-ledger.md` maps every URL and E/D row of the dossier to one reference (classes A–D citable, E excluded; short tags, ACM references, verification notes); `references.bib` is BibTeX with the ledger keys; `check_references.py` re-checks the ledger file and the BibTeX against the dossier. |
| `archive/` | The 16 raw deep-research outputs the dossier merges: 5 prompts × (Claude / ChatGPT / Gemini), plus the Project's P3 landscape survey. Provenance only — superseded by the dossier. |

## Working rules

- Cite by the dossier's IDs (E-, D-, §). Extend the dossier by patches; do not re-derive it.
- Every new number carries: figure, exact measurement definition, source URL, date, primary/secondary label.
- Conflicts with the dossier become new D-entries and new evidence new E-entries, continuing the numbering (current ranges in `STATUS.md`).
- Distinguish model calls / tool calls / steps / turns; inference time / wall-clock; cost per attempt / per success; author estimate / stopwatch; arXiv version.
- Source eligibility (Edwin, 2026-09-29): prioritize top journals/conferences, then official technical material from leading AI companies (OpenAI, Anthropic, Google/DeepMind, Groq and peers); allow preprints from strong universities or established research laboratories. Exclude ordinary-company blogs and other sources outside these categories. Verify venue/track or institutional affiliation, and append complete references with actual reading versions. Details in `CLAUDE.md`; [Part 3 source audit](research/2026-09-29-part3-source-filter.md) covers its 51 candidates, with 48 retained. Historical deck references have not all been re-audited against this updated rule.

## Roadmap

v2 → v2.1 (verification queue in Part VIII §8.2 resolved) → v3 (current; six follow-up investigations in §8.3 merged) → slides.
