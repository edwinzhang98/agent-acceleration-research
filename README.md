# Agent Acceleration Research

Evidence base for a research investigation into why LLM computer-use / web agents are too slow and too expensive for real work, and into the 2023–2026 research landscape on accelerating them. Groundwork for (1) a paper on accelerating repetitive enterprise web workflows (SAP Concur expense reports) and (2) a slide deck for a senior ML audience.

## Layout

| Path | What it is |
|---|---|
| `CLAUDE.md` | Rules every Claude session follows in this repo (auto-loaded by Claude Code; the Claude Project's instructions point here). Single source of truth for the working rules below. |
| `STATUS.md` | **Start here.** One-screen index: current canonical version, what is done, what the next thread should do, log. Updated at the end of every thread. |
| `research/` | Thread outputs (verification results, follow-up research), one file per thread in patch format. Created on first use. |
| `Agent-Acceleration-Consolidated-Dossier-v3-2026-09-27.md` | **Canonical document.** Cross-validated synthesis of all 16 research outputs plus the six follow-up investigations: evidence ledger (E1–E211), inference→agent mapping, 8-family landscape, evaluation protocol and API budget, novelty assessment, discrepancy ledger (D1–D140), provider scorecard, verification queue and follow-up research prompts. |
| `slides/` | Slide deck built from dossier v3 (`agent-acceleration.html`, generator `build_deck.py`, conventions in `slides/README.md`) and its references: `references.md` is the deck's curated list (author–year scheme, source-credibility rule); `references-ledger.md` maps every URL and E/D row of the dossier to one reference (classes A–D citable, E excluded; short tags, ACM references, verification notes); `references.bib` is BibTeX with the ledger keys; `check_references.py` re-checks the ledger file and the BibTeX against the dossier. |
| `archive/` | The 16 raw deep-research outputs the dossier merges: 5 prompts × (Claude / ChatGPT / Gemini), plus the Project's P3 landscape survey. Provenance only — superseded by the dossier. |

## Working rules

- Cite by the dossier's IDs (E-, D-, §). Extend the dossier by patches; do not re-derive it.
- Every new number carries: figure, exact measurement definition, source URL, date, primary/secondary label.
- Conflicts with the dossier become new D-entries and new evidence new E-entries, continuing the numbering (current ranges in `STATUS.md`).
- Distinguish model calls / tool calls / steps / turns; inference time / wall-clock; cost per attempt / per success; author estimate / stopwatch; arXiv version.

## Roadmap

v2 → v2.1 (verification queue in Part VIII §8.2 resolved) → v3 (current; six follow-up investigations in §8.3 merged) → slides.
