# CLAUDE.md — rules for working in this repository

This repository is the evidence base for a research investigation into why LLM computer-use / web agents are too slow and too expensive for real work, and into the 2023–2026 research on accelerating them. It feeds (1) a paper on accelerating repetitive enterprise web workflows (SAP Concur expense reports) and (2) a slide deck for a senior ML audience.

## Start and finish every session the same way

1. **Start:** read `STATUS.md` (one screen: canonical version, done / next, parked questions, log). Open only the files it points to.
2. **Finish:** update `STATUS.md` (add a log line; tick or add Done / Next items; change the "Canonical document" line if you produced a new dossier version; bump "Last updated"), then commit. Work that is not committed does not exist.

Repository README documentation defaults to English (Edwin, 2026-09-30). Do not insert Chinese prose into an English README. If bilingual documentation is requested, keep English as the default and put Chinese in a separate language edition. Label links to Chinese research reports explicitly.

## What is canonical

- The canonical document is the dossier named in `STATUS.md` (currently `Agent-Acceleration-Consolidated-Dossier-v3-2026-09-27.md`). Never overwrite it; a new version gets a new filename (`…-v3.1-<date>.md`, `…-v4-<date>.md`).
- `archive/` holds the 16 raw deep-research outputs the dossier merged. They are provenance only — superseded by the dossier. Do not cite them as independent evidence and do not re-merge them.
- Thread / session outputs go in `research/` as `YYYY-MM-DD-<topic>.md`, one file per task.

## Evidence rules

- Cite the ledger IDs (E- and D-, ranges as in `STATUS.md`) and §-numbered sections. Do not re-summarize or re-derive its content; extend it by patches.
- Every new number carries five things: the figure, the exact measurement definition, the source URL, the date, and a primary/secondary label — the same schema as the dossier's evidence tables.
- A conflict with the dossier becomes a new D-entry, never a silent overwrite; new evidence and new discrepancies continue the numbering.
- Always distinguish: model calls ≠ tool calls ≠ steps ≠ turns; inference time ≠ wall-clock; cost per attempt ≠ cost per success; author estimate ≠ stopwatch measurement; arXiv version numbers matter (several headline numbers changed between versions — see D5, D13–D15, D44, D48).
- Prefer primary sources (paper, leaderboard, vendor docs, official survey). If only a secondary source exists, say so. If a source is paywalled or unreachable, report that instead of guessing.
- **Source eligibility, updated by Edwin on 2026-09-29:** prioritize formally published top journals/conferences; next allow official technical material from leading AI companies at the level of OpenAI, Anthropic, Google/DeepMind or Groq. Preprints from strong universities or established research laboratories may supplement these. Ordinary-company blogs and sources outside these categories are not reference material. Verify the venue/track or paper's institutional affiliations; a submission page or author-reported acceptance alone is not confirmed publication. End research documents with complete references and distinguish the formal citation from the version actually read. This supersedes the earlier broad company-research-group rule; the completed audit currently covers the 51 Part 3 candidates only (`research/2026-09-29-part3-source-filter.md`, D313), not all historical deck references.
- **Citation priority, restated by Edwin on 2026-09-30:** when several eligible sources make the same point, cite in this order: (1) papers at top conferences and journals; (2) high-quality preprints from top universities or established laboratories; (3) official technical material of OpenAI/Anthropic/Google-DeepMind-level companies. This ordering (preprints before company material) replaces the order written in `research/2026-09-29-citation-tiers.md`; eligibility itself is unchanged. Ineligible works that are relevant go to a separate "held" list and are not used as evidence.
- Vendor-marketing numbers are labeled as such. Numbers computed by you are labeled "calc.".

## Output format for research and verification tasks

Four sections, in this order, written so they can be merged into the dossier without rewriting it:

1. Verification table or evidence table (ID, claim as recorded, what the primary source says with a verbatim quote and location, verdict).
2. D-ledger additions (next free D-IDs).
3. E-ledger patches: the exact replacement text for each dossier line changed, with its E-ID.
4. Still-open list.

For reader-facing research documents, append a complete References section after these four sections. A source-screening audit can instead link to the accompanying document's References and retain excluded items only as an audit trail.

No prose rewrite of the dossier.

## Roadmap

v3 (current) → slides. Slides are built from v3 only.

## Git conventions

- Commit author email is the GitHub noreply address already set in this repo's config (GitHub blocks pushes that expose the real email).
- Commit messages: what changed and why, one paragraph; mention the dossier IDs touched.
- Do not force-push and do not rewrite history on `main`.
- Slides workflow (Edwin, 2026-10-04): after each completed slide edit, perform the appropriate targeted checks, commit the task files, and push the commit to the existing remote branch. This is standing authorization; do not ask again for each push. Preserve unrelated uncommitted work.
