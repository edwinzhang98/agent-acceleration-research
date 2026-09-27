# STATUS — read this first

**Last updated:** 2026-09-27 04:20 UTC, by Claude (project thread, P0 item 1) · **Canonical document:** `Agent-Acceleration-Consolidated-Dossier-v2-2026-09-26.md` · **Current milestone:** v2 done → working toward **v2.1**

This file is the index for anyone (human or thread) starting with an empty context. Read it, then open only the files it points to. Keep it under one screen. Update it before you finish a thread (see "How to update" at the bottom).

## Where things are

| What | Path | Notes |
|---|---|---|
| Canonical dossier | `Agent-Acceleration-Consolidated-Dossier-v2-2026-09-26.md` | E1–E90 evidence, D1–D55 discrepancies, Parts I–VIII, Appendices A–B. Never overwrite; new versions get new filenames (`…-v2.1-…`, `…-v3-…`). |
| Raw research inputs | `archive/` | 16 deep-research outputs (5 prompts × Claude/ChatGPT/Gemini + the Project's P3 survey). Provenance only — superseded by the dossier. Do not cite them as independent evidence. |
| Thread outputs | `research/` *(create on first use)* | One file per thread: `YYYY-MM-DD-<topic>.md`. Patch format: (1) evidence/verification table, (2) D-ledger additions, (3) E-ledger patches as exact replacement text, (4) still-open list. |
| Rules | `README.md` → Working rules; Project instructions in the Claude Project | ID scheme, measurement distinctions, source labels. |

## Done

- [x] 15 deep-research outputs (5 prompts × 3 providers) + Claude's own P1 report merged into dossier **v1** (2026-09-26).
- [x] Project's P3 survey (doc 15) merged by delta into dossier **v2**; D41–D55 logged; 5 primary sources re-verified (marked [V] in the dossier).
- [x] Repo created and pushed; local clone on Edwin's Mac at `~/projects/agent-acceleration-research`.
- [x] P0 item 1 (OSWorld-Human $2.43 vs Table 3, D7) verified: `research/2026-09-27-verification-P0-item1.md`. Patches not yet applied to a v2.1 copy.

## Next (in order)

1. **Verification pass → v2.1.** Run dossier Part VIII §8.2: P0 items 2–7 (item 1 done), then P1 items 8–13 and 13a–13f (13a EchoPath and 13b FocusAgent v1-vs-TMLR first). Output to `research/2026-MM-DD-verification-P0-P1.md` in patch format. Then apply the patches to a copy named `Agent-Acceleration-Consolidated-Dossier-v2.1-<date>.md` and update the "Canonical document" line above.
2. **Six follow-up investigations → v3.** Prompts are in dossier Part VIII §8.3 (1 latency decomposition by architecture; 2 speculation safety semantics — add EchoPath and Cordon to its scope; 3 enterprise RPA + LLM fallback products; 4 human-time baselines; 5 2026 agent-serving papers; 6 vendor speed tiers). One thread each, output to `research/`, patch format. Merge into v3.
3. **Slides** for a senior ML professor, built from v3 only. Not before v3.

## Open questions parked (do not re-research; decide when relevant)

- Whether SAP Concur exposes an API for the target workflow — affects the "why click at all?" objection in dossier §5.5.
- Which of the two dossier framings (JIT-with-deoptimization vs branch-prediction-for-stateful-UIs) leads the paper — dossier §5.6 recommends both in one MLSys submission.

## Log (newest first; one line per thread)

- 2026-09-27 — project thread — P0 item 1: D7 resolved. Table 3 = GTA1 totals over 39 tasks, no repeat runs stated → $7.87/task (calc.); the paper's $2.43 and 87/13/<1 split match output-token cost only (inferred). D56 added ("6×" planning/judging = 5.3× on totals). Patches for E45, D7, lines 236/580/871 in `research/2026-09-27-verification-P0-item1.md`.
- 2026-09-26 — cowork session — Dossier v2 built and pushed; README, .gitignore, STATUS.md added. Next: verification pass (P0 1–7).

## How to update this file

At the end of every thread: (a) add one log line, (b) tick or add items under Done/Next, (c) if you produced a new dossier version, change the "Canonical document" line, (d) bump "Last updated". Keep the whole file under ~60 lines; move anything longer into `research/`.
