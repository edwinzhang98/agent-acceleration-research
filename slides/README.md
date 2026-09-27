# slides/ — the boss deck

`agent-acceleration.html` is a self-contained HTML deck (open the file in a browser; ← → or click to move, N toggles the Chinese speaker notes, `#sN` deep-links a slide). It is built from dossier v3 only.

Citations (agreed 2026-09-27, replaces the A–E class letters): author–year tags on the slide — `(Abhyankar et al., 2026)`, `(XLANG Lab, 2026)`, `(Anthropic, 2026a)` — with the dossier ledger ID in square brackets `[E22]` for traceability, and a full reference list per module (clickable or an appendix when the slide has no room). Source types are written in words: conference/journal paper, preprint (institution shown), vendor primary material, industry report, code, third-party measurement, our own calculation (calc.); vendor marketing is not cited. The verified list, with what each entry backs, is `references.md`. The current draft deck still uses the old class badges and must be reworked to this scheme.

## Structure (six modules)

1. The problem.
2. How agents run today and where each kind breaks.
3. What existing work did about each of those breaks, and how far it got.
4. What that leaves open → the problem we take, in one sentence (derived from 2–3, never asserted).
5. How we would do it.
6. Experiments and cost (money and compute only).

## State (2026-09-27)

Module 1 draft (9 slides, s0–s8) is in the file. Edwin's verdict: it does not explain the problem — it is a stack of evidence cards built outward from the ledger, not inward from the reader's questions. Rework plan, agreed in discussion: Module 1 must make the reader believe five things, in this order.

| # | The reader must believe | Evidence (dossier IDs) | Class |
|---|---|---|---|
| 1 | What the thing is and what it is for: a model looping look → think → act, one full model call per step, tens to hundreds of steps per real task; one generic example of a repeated web workflow (not ExpenseAI — Edwin's decision 2026-09-27: the deck does not use the Concur self-measurement as evidence or as its running example) | none needed; a loop diagram | — |
| 2 | Today it is slow, expensive and unreliable: hour-scale tasks take ~318 calls (mean), the best agent completes ~20%, ≈$72 per attempt ≈ $351 per success (calc.) | E6/D3, E41, E5/D2 (1.6 h is an annotator estimate) | D (OSWorld team) |
| 3 | Why, and why waiting for faster models is not enough: the time and cost come from the loop's structure (serial round-trips, history re-sent every step → quadratic growth, convex cost of accuracy), not from one slow part | E22, E45 (A); 6× / 9× / 9.6× (three D-class) | A + D |
| 4 | This is not small: agents are the majority workload; speed is already sold as a paid tier | OpenRouter (B), Gartner (C), MAP (A); fast-tier existence and pricing (B), multipliers labelled vendor-stated | A/B/C |
| 5 | The problem definition: agent acceleration = lower wall-clock per task and cost per success at fixed accuracy, above all for repeated workflows; agent-vs-human wall-clock is unmeasured (AXIS user study is the closest, E161) | §0.3 measurement rules as a footnote; E161 (A) | A |

Changes to the draft: s1 (measurement rules) → footnote/backup; s2 → one slide with the three numbers and what each means; s3 latency decomposition and the contrary sandbox measurement (E97/D95) → Module 2; s4 folded into point 3 with the conclusion "you cannot buy reliability"; s5+s6 merged; s7 slogan dropped. Open: whether the boss hears the deck or reads it alone (decides text density per slide).
