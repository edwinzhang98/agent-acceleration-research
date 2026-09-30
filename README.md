# Agent Acceleration Research

Evidence base for a research investigation into why LLM computer-use / web agents are too slow and too expensive for real work, and into the 2023–2026 research landscape on accelerating them. Groundwork for (1) a paper on accelerating repetitive enterprise web workflows (SAP Concur expense reports) and (2) a slide deck for a senior ML audience.

## Read online

**[Open the research reading site](https://edwinzhang98.github.io/agent-acceleration-research/)** — chapter navigation, search, rendered equations, and mobile layouts. The HTML files can also be downloaded for offline reading. The reports and reading-site interface are in Chinese; the slide deck is in English.

| Reading material | Scope |
|---|---|
| [Agent Acceleration and Self-Improvement with Fixed Model Weights](https://edwinzhang98.github.io/agent-acceleration-research/reports/fixed-weight-agent-acceleration.html) (Chinese) | Codex review of mechanisms, trajectory learning, environment exploration, and cost evaluation. |
| [Self-Improving Agents: Literature and Acceleration](https://edwinzhang98.github.io/agent-acceleration-research/reports/self-improvement-survey.html) (Chinese) | Codex-reviewed edition of Claude's literature report: methods, results, conditions, limitations, and searchable evidence. Complements the report above. |
| [How the Literature Defines Agent Acceleration](https://edwinzhang98.github.io/agent-acceleration-research/reports/how-literature-defines-acceleration.html) (Chinese) | Problem-framing discussion draft with two batches of independent record audits; the source explains their scope and open decisions. |
| [Formulas for Speed and Cost](https://edwinzhang98.github.io/agent-acceleration-research/reports/formulas-for-speed-and-cost.html) (Chinese) | Equations and notation reference; snapshot dated 2026-09-28. |
| [Codex Research Plan](https://edwinzhang98.github.io/agent-acceleration-research/reports/trajectory-research-plan.html) · [Claude Research Plan, Draft 6](https://edwinzhang98.github.io/agent-acceleration-research/reports/claude-part3-plan.html) (Chinese) | Discussion drafts dated 2026-09-29. Methods, experiments, and budgets are undecided; later review findings have not all been incorporated. |
| [Agent Acceleration Slide Deck](https://edwinzhang98.github.io/agent-acceleration-research/slides/agent-acceleration.html) (English) | Slide-by-slide presentation of Parts 1–2. |

Source reports are in `notes/`, reviews and evidence in `research/`, and presentation sources in `slides/`. The generated reading site is in `docs/`. The four additional report editions are presentation conversions, not new paper audits. See the [reading-site guide](tools/reading-site/README.md) for building and maintenance.

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

- Keep repository README documentation in English. Label links to Chinese reports explicitly; provide a separate language edition if bilingual documentation is needed.
- Cite by the dossier's IDs (E-, D-, §). Extend the dossier by patches; do not re-derive it.
- Every new number carries: figure, exact measurement definition, source URL, date, primary/secondary label.
- Conflicts with the dossier become new D-entries and new evidence new E-entries, continuing the numbering (current ranges in `STATUS.md`).
- Distinguish model calls / tool calls / steps / turns; inference time / wall-clock; cost per attempt / per success; author estimate / stopwatch; arXiv version.
- Source eligibility (Edwin, 2026-09-29): prioritize top journals/conferences, then official technical material from leading AI companies (OpenAI, Anthropic, Google/DeepMind, Groq and peers); allow preprints from strong universities or established research laboratories. Exclude ordinary-company blogs and other sources outside these categories. Verify venue/track or institutional affiliation, and append complete references with actual reading versions. Details in `CLAUDE.md`; [Part 3 source audit](research/2026-09-29-part3-source-filter.md) covers its 51 candidates, with 48 retained. Historical deck references have not all been re-audited against this updated rule.

## Roadmap

v2 → v2.1 (verification queue in Part VIII §8.2 resolved) → v3 (current; six follow-up investigations in §8.3 merged) → slides.
