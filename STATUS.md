# STATUS — read this first

**Last updated:** 2026-09-27, by Claude (project thread, P0 items 2–7 and P1 items 8–13f; permission allow list) · **Canonical document:** `Agent-Acceleration-Consolidated-Dossier-v2-2026-09-26.md` · **Current milestone:** v2 done → working toward **v2.1**

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
- [x] P0 items 2–7 and P1 items 8–13, 13a–13f verified: `research/2026-09-27-verification-P0-P1.md` (D57–D94, E91–E93; patch index by dossier line in §3). Patches not yet applied to a v2.1 copy.

## Next (in order)

1. **Build v2.1.** Apply the patches in `research/2026-09-27-verification-P0-item1.md` and `research/2026-09-27-verification-P0-P1.md` to a copy named `Agent-Acceleration-Consolidated-Dossier-v2.1-<date>.md` (line numbers refer to v2 at c18e2fe; use the patch index), then update the "Canonical document" line above. Human-only checks listed in the P0-P1 file's §4 (two LinkedIn posts behind E58/E59, MAP v4 appendix B.4.2, PASTE Fig. 10, FocusAgent Table 1 pruning, Temporal Chart 3.4 options) can follow v2.1. Re-check dated items later: SMC at MLSP 2026 (after 1 Oct), SPACE at EMNLP 2026 (after 29 Oct), AAPT at AAAI-27 (after 30 Nov), EchoPath code link.
2. **Six follow-up investigations → v3.** Prompts are in dossier Part VIII §8.3 (1 latency decomposition by architecture; 2 speculation safety semantics — add EchoPath and Cordon to its scope; 3 enterprise RPA + LLM fallback products; 4 human-time baselines; 5 2026 agent-serving papers; 6 vendor speed tiers). One thread each, output to `research/`, patch format. Merge into v3.
3. **Slides** for a senior ML professor, built from v3 only. Not before v3.

## Open questions parked (do not re-research; decide when relevant)

- Whether SAP Concur exposes an API for the target workflow — affects the "why click at all?" objection in dossier §5.5.
- Which of the two dossier framings (JIT-with-deoptimization vs branch-prediction-for-stateful-UIs) leads the paper — dossier §5.6 recommends both in one MLSys submission.

## Log (newest first; one line per thread)

- 2026-09-27 — project thread — Added `.claude/settings.json` allow list (WebFetch, WebSearch, read-only shell and git read commands) to cut approval prompts in future threads; no ask/deny rules, so git push behaviour is unchanged.
- 2026-09-27 — project thread — P0 2–7, P1 8–13f verified (`research/2026-09-27-verification-P0-P1.md`, D57–D94, E91–E93). No Top-10 number changed; ranks 6, 9, 10 reworded (OpenRouter 15× is per request; MAP "can operate" async; Gartner >90% is provider cost). Main corrections: FocusAgent no sign flip (D48), TraceLab 5.3× not in paper, Continuum not version drift, AXIS −65–70% is vs humans, EchoPath 87.3–92.8% with Synapse at 91.8%.
- 2026-09-27 — project thread — P0 item 1: D7 resolved. Table 3 = GTA1 totals over 39 tasks, no repeat runs stated → $7.87/task (calc.); the paper's $2.43 and 87/13/<1 split match output-token cost only (inferred). D56 added ("6×" planning/judging = 5.3× on totals). Patches for E45, D7, lines 236/580/871 in `research/2026-09-27-verification-P0-item1.md`.
- 2026-09-26 — cowork session — Dossier v2 built and pushed; README, .gitignore, STATUS.md added. Next: verification pass (P0 1–7).

## How to update this file

At the end of every thread: (a) add one log line, (b) tick or add items under Done/Next, (c) if you produced a new dossier version, change the "Canonical document" line, (d) bump "Last updated". Keep the whole file under ~60 lines; move anything longer into `research/`.
