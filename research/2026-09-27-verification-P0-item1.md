# Verification — P0 item 1: OSWorld-Human "$2.43 per task" vs Table 3 (D7, E45)

**Date:** 2026-09-27 · **Scope:** dossier Part VIII §8.2, P0 item 1 only · **Dossier base:** `Agent-Acceleration-Consolidated-Dossier-v2-2026-09-26.md`

**Sources checked**

| Label | Source | Version / date | How it was read |
|---|---|---|---|
| v2 | https://arxiv.org/html/2506.16042v2 — Abhyankar, Qi, Zhang, "OSWorld-Human: Benchmarking the Efficiency of Computer-Use Agents" | arXiv v2, 18 May 2026 | Web fetch of the HTML (primary) |
| MLSys | https://proceedings.mlsys.org/paper_files/paper/2026/file/5edb57c05c81d04beb716ef1d542fe9e-Paper-Conference.pdf | MLSys 2026 proceedings (camera-ready) | Web fetch of the PDF (primary) |
| v1 | https://arxiv.org/html/2506.16042v1 | arXiv v1, 19 Jun 2025 | Web fetch of the HTML (primary), to date when the cost figure first appeared |
| repo | https://github.com/WukLab/osworld-human | fetched 2026-09-27 | README and top-level file listing |

**Access note.** Direct download of both PDFs with `curl` was refused by this environment's network proxy (HTTP 403 on CONNECT). The text below was obtained through a web-fetch tool that extracts page text; every quote was requested as an exact quote, and the key sentences and Table 3 came back **word-for-word identical from two independent fetches (v2 HTML and MLSys PDF)**. The PDF page number (p. 10) is as reported by the fetch tool and was not checked visually. The table layout was not inspected as an image.

---

## 1. Verification table

| ID | Claim as recorded in dossier | What the primary source says (verbatim, location) | Verdict |
|---|---|---|---|
| P0-1a | E45: "OSWorld-Human GTA1/o3: $2.43 per task (planning 87%, judging 13%, grounding <1%)" | v2 §3.4 "Detailed Cost and Failure Analysis" and MLSys §3.4 (identical): *"On average, a task costs $2.43, with planning, judging, and grounding being responsible for 87%, 13%, and less than 1%, respectively."* | ✅ **Quoted correctly.** The paper does print $2.43 and 87/13/<1. |
| P0-1b | E45/D7: Table 3 token totals imply ≈$307 total ≈ $7.9/task | Table 3, both versions, identical. Caption: *"Cost Analysis of Different Types of LLM Calls. Unit price using billing from TogetherAI"* (MLSys adds *"(Together AI, 2025)"*).<br>`Planning (o3) | 87.34 × 10⁶ | $2 per mil | $174.69 | 10.29 × 10⁶ | $8 per mil | $82.35`<br>`Judging (o3) | 17.94 × 10⁶ | $2 per mil | $35.89 | 1.59 × 10⁶ | $8 per mil | $12.76`<br>`Grounding (GTA1-7B) | 3.77 × 10⁶ | $0.30 per mil | $1.13 | 0.02 × 10⁶ | $0.30 per mil | $0.006`<br>(columns: Model, Prompt Tokens, Prompt Price, Prompt Cost, Output Tokens, Output Price, Output Cost) | ✅ **Confirmed.** Sum of the six printed cost cells = **$306.83**; ÷ 39 = **$7.87/task** (calc.). Recomputing from the token counts × printed prices gives $7.87/task as well (calc.). |
| P0-1c | D7 open question: "whether Table 3 spans multiple runs" | v2 and MLSys §3.4: *"Table 3 shows the total cost and prompt count breakdown across different steps (across all 39 tasks)."* Setup (§3, both versions): *"We utilize the OSWorld-provided subset of 39 tasks, or 10% of the entire benchmark."* / *"We then run Agent S2 and GTA1 on each of the tasks and collect detailed timing and token traces."* No sentence in either version mentions repeated runs, trials or seeds. | ✅ **Resolved: Table 3 is a total over the 39 profiled tasks, with no repeated runs stated.** The multi-run explanation for the gap is not supported by the text. $306.83 would equal $2.43/task only over ≈126 tasks (calc.), which matches no task count in the paper (39 profiled; 369 in the benchmark). |
| P0-1d | (new) Where $2.43 comes from | Not stated by the authors. **Output-token cost only** reproduces every figure in the $2.43 sentence and the "6×" sentence (all calc. from Table 3):<br>• output cost $95.12 ÷ 39 = **$2.439/task** (printed $2.43; recomputed from tokens $2.437)<br>• output-cost shares: planning **86.6%**, judging **13.4%**, grounding **0.01%** → "87%, 13%, less than 1%"<br>• planning ÷ judging output cost = **6.45×** → *"Planning costs over 6× more than judging because in each planning step, GTA1 makes 4 parallel calls to o3."* (v2 §3.4)<br>By contrast, total cost gives shares 83.8% / 15.9% / 0.4% and a 5.28× ratio; prompt cost alone gives $5.43/task, 82.5% / 17.0% / 0.5%, 4.87×. | ⚠ **Inferred, not confirmed by the authors.** Three independent figures match output-only cost and none matches total cost, so the most likely explanation is that the $2.43 sentence (and the "6×" sentence) were computed from the output-cost column only. |
| P0-1e | E45: "one grounding loop cost $8.47 and 27 min (18 wasted steps)" | v2 §3.4: *"This loop costed $8.47 and 27 minutes of wall-clock time."* (sic, "costed"); preceding sentence: *"The planner's reflections in successive steps repeatedly noted 'still showing the same engines', yet the grounding model never corrected."* | ✅ Quoted correctly (the 18-step count was not re-checked in this pass). Note: a single loop costing $8.47 is itself more than 3× the claimed $2.43 average, which is consistent with the $7.87 total-cost reading. |
| P0-1f | E45: "cost accumulates quadratically over steps" | v2 and MLSys §3.4: *"The quadratic increase contributes to the drastic cost difference between the planning and judging models compared to the grounding model."* | ✅ Quoted correctly. |
| P0-1g | E45 date "2026" | v1 (19 Jun 2025) contains **no** dollar figures and no token-cost table; it profiles *"the OSWorld-provided subset of 37 tasks"*. The cost analysis first appears in v2 (18 May 2026) / MLSys 2026. | ✅ Date correct; cite v2 or MLSys, never v1, for any cost number. |
| P0-1h | Cost scope | v2 §3.4: *"we perform a cost analysis of GTA1"*; §3.4 contains no mention of prompt caching or cached-token discounts (the only caching mention is "prefix caching" in §5.3 future work). | ✅ Table 3 is GTA1 only (o3 planner/judge, GTA1-7B grounder) at list prices with no cache discount. It says nothing about Agent S2's cost. |
| P0-1i | Artifact availability | repo README and top-level listing: folders per application plus `score.py`; no token traces, pricing or cost scripts visible. | ⚠ The $2.43 derivation cannot be checked against released code or traces. |

---

## 2. D-ledger additions

| ID | Topic | Positions | Resolution / action |
|---|---|---|---|
| D56 | OSWorld-Human "planning costs over 6× more than judging" | Paper text (v2 §3.4): "over 6×"; Table 3 totals (calc.): $257.04 vs $48.65 = **5.28×**; Table 3 output cost only (calc.): **6.45×** | Same root cause as D7: the text's ratio matches output-only cost, not total cost. If a ratio is needed, cite "≈5.3× (calc. from Table 3 totals)" and note the paper's "over 6×". |

---

## 3. E-ledger patches (exact replacement text)

**E45** (dossier line 142) — replace the whole row with:

```
| E45 | **OSWorld-Human GTA1/o3, 39 profiled tasks: Table 3 totals $306.83 at list price = $7.87 per task (calc.); planning 83.8%, judging 15.9%, grounding 0.4% of total cost (calc.). The paper's text says "$2.43" per task with shares 87% / 13% / <1%, which match output-token cost only ($95.12 ÷ 39 = $2.44, calc.). Cost accumulates quadratically over steps; one grounding loop cost $8.47 and 27 min (18 wasted steps); in failed >50-step tasks 66% of steps are wasted in loops** | GTA1 only (o3 planner/judge at $2/$8 per M tokens, GTA1-7B grounder at $0.30/$0.30); totals across all 39 tasks, one run per task as far as stated, no cache discount; cost per attempt, not per success | OSWorld-Human v2 §3.4 and Table 3, https://arxiv.org/html/2506.16042v2 ; identical in MLSys 2026 PDF §3.4 | 2026 (absent from v1) | Primary; per-task totals calc. | C, O; verified 2026-09-27 (research/2026-09-27-verification-P0-item1.md) | ✅ Table verified. **D7 resolved:** cite $7.87/task (calc. from Table 3). If $2.43 is quoted, say it reproduces output-token cost only (inferred, not author-confirmed). "Planning over 6× judging" is 5.3× on total cost (D56). |
```

**D7** (dossier line 787) — replace the whole row with:

```
| D7 | OSWorld-Human cost per task | Paper text: $2.43 (87/13/<1 split); C: Table 3 tokens imply ≈$7.9/task; O (doc 4): "dollar aggregates … internally unclear" | **Resolved 2026-09-27.** Table 3 is a total "across all 39 tasks" with no repeated runs stated: $306.83 ÷ 39 = $7.87/task (calc.). $2.43, the 87/13/<1 split and the "over 6×" planning/judging ratio all match output-token cost only (calc.; inferred, not author-confirmed). Cite $7.87 (calc.) with the caveat. See research/2026-09-27-verification-P0-item1.md and D56 |
```

**§4 "Numbers not to put on a slide" paragraph** (dossier line 236) — replace the fragment

`OSWorld-Human's $2.43/task (E45, internal inconsistency);`

with

`OSWorld-Human's $2.43/task (E45/D7: matches output-token cost only; use $7.87/task, calc. from Table 3 totals);`

**Benchmark-reporting table, OSWorld-Human row** (dossier line 580) — replace the fragment

`totals NR; $ aggregates internally unclear`

with

`totals NR; text's $2.43/task = output-token cost only, Table 3 totals give $7.87/task (calc., D7)`

**§8.2 P0 item 1** (dossier line 871) — replace the whole line with:

```
1. ~~OSWorld-Human v2 Table 3 vs the "$2.43/task" figure (D7); confirm whether Table 3 spans multiple runs.~~ **Done 2026-09-27** (research/2026-09-27-verification-P0-item1.md): Table 3 = 39 tasks, one run stated; $7.87/task (calc.); $2.43 = output-token cost only (inferred). D7 resolved, D56 added.
```

---

## 4. Still-open

1. **Author confirmation of the output-only explanation.** The match is exact on three figures but is my inference; only the authors (UCSD WukLab) or an erratum can confirm it. No traces or cost scripts are in the public repo.
2. **Pricing source.** Table 3's caption says prices are "using billing from TogetherAI", yet o3 is an OpenAI model; $2 / $8 per M matches o3's list price as I recall it, but I did not verify the price on a primary pricing page or TogetherAI's catalog in this pass. The $7.87 figure is at those printed prices with no cached-input discount; actual spend could be lower if caching applied.
3. **Agent S2 cost.** The paper gives no dollar cost for Agent S2 (GPT-4.1); only GTA1 was costed.
4. **"18 wasted steps"** in E45 was not re-checked in this pass (only the $8.47 / 27 min sentence was).
5. **Visual check of the MLSys PDF.** Page number (p. 10) and table layout came from text extraction; a human glance at the PDF would close this.
