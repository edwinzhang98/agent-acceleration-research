# Part 2 source checks, 28 September 2026 (verbatim records)

Provenance for `research/2026-09-28-part2-acceleration-by-term.md`. The read-only workflow `wf_eae7c559` produced these 156 records by re-reading each primary source. They appear here as returned, one per work, with these fields:
- **read:** the URL and version read;
- **verdict:** confirmed, corrected, could not read, or not found;
- **effect:** the figures with their location and quotes;
- **mechanism and term;**
- **authors and venue;**
- **formula.**

They are raw inputs: the deck uses only the numbers listed in the research file's verification table.

## 0. TokenPilot

**read:** https://arxiv.org/html/2606.17016v2 and https://arxiv.org/pdf/2606.17016v2 (v2, 28 Aug 2026). I read the full text, including Tables 1–10 and App. A.1–A.5. I also opened the v1 PDF (15 Jun 2026) to compare the headline numbers and the code link.

**verdict:** confirmed

**effect:**

Abstract (v2): "reduces costs by 61% and 56% in isolated mode, and 61% and 87% in continuous mode". The v1 numbers are the same.

Table 1, PinchBench: 123 tasks in 11 categories, a frozen snapshot at commit 0347a7f (App. A.1).
- Isolated: Vanilla scores 80.5 at $8.31; TokenPilot scores 81.0 at $3.22 (−61.3%, calc.).
- Continuous: 79.2 at $7.24 → 81.3 at $2.79 (−61.5%, calc.).

Table 2, Claw-Eval (General group, 161 tasks):
- Isolated: 64.5 at $5.16 → 63.1 at $2.27 (−56.0%, calc.).
- Continuous: 63.4 at $81.52 → 60.8 at $10.58 (−87.0%, calc.).

Models and settings:
- §4.1: "All evaluated methods utilize GPT-5.4-mini as the agent backbone."
- The estimator is Qwen3.5-35B-A3B, run every B=3 turns (App. A.4). Its cost over the continuous PinchBench stream is "less than $0.03" (§3.3).

How cost is computed:
- App. A.2, Eq. (11): p_hit = $0.075/M, p_miss = $0.75/M, p_out = $4.50/M, "Following the official pricing tiers of GPT-5.4-mini".
- Token counts are "gathered directly from the explicit metadata fields returned by the provider APIs" (§4.1). So this is billing cost, not GPU cost.
- Recomputing from Table 2's tokens (709.845M hit, 21.981M miss, 2.622M out) gives $81.52 (calc.). The table totals therefore use the backbone's tokens only.

Conditions the recorded claim leaves out:
- The baseline is not a bare agent. App. A.3: "Vanilla runs on OpenClaw without any extra context management, with a maximum context window of 500k tokens and a compaction trigger ratio of 0.5." §4.3 confirms it has built-in compaction.
- Continuous mode puts same-category tasks in one session (App. A.1), which favours cache reuse.
- v2 adds mixed-category streams (App. A.5, Table 9): the 123 tasks shuffled with seed 42 into 10 sessions. Vanilla 68.77 at $21.16 → TokenPilot 69.10 at $4.83 (−77%, calc.).
- Scores give partial credit; they are not binary success rates. Claw-Eval Eq. (10): s_safe × (0.80·s_comp + 0.20·s_rob).
- The number of runs per setting is not stated.
- No latency or wall-clock time is measured anywhere.

Where the savings come from:
- Table 4 (PinchBench isolated): stable placeholders alone take $8.31 → $4.35; adding the reduction pass gives $2.87.
- Table 3 (PinchBench continuous): the global level gives $4.22; adding the local level gives $2.79, and cache-hit tokens fall from 26.716M to 8.551M.
- §4.4: the macro cache hit rate "rises from 38.7% to 79.2% on PinchBench, and from 67.2% to 83.1% on Claw-Eval".

**mechanism and term:**

The recorded mapping is mostly right. Refined by component:

1. Prefix stabilization (App. A.4). Changing fields (working-directory paths, timestamps, session IDs) are replaced by static placeholders, and tool definitions move to the end of the system prompt. Term: money by billing class, cache miss → cache hit.

2. Observation reduction at ingestion. It removes duplicate repeated reads by hash, cuts long outputs to a 600/400-character preview, slims HTML, downsamples images and cleans formatting. A recovery tool can fetch the full payload. Term: smaller observation tokens o_k, so context grows more slowly per pass.

3. Lifecycle-aware eviction. Every B=3 turns, an estimator LLM labels each segment active, completed or evictable, and evictable segments are removed in one pass. Term: this changes the shape of context growth, because completed segments leave the prompt and it stops growing monotonically. It trades against cache continuity: B=1 inflates misses (Fig. 6).

Corrections:
- "Prefill smaller" is inferred from fewer miss tokens. It is not measured: the paper reports tokens and dollars only, no time.
- Other terms move too. The estimator adds one side-model call every 3 turns (c_k slightly larger, on Qwen3.5-35B-A3B), and the recovery tool can add tool calls.
- Success-rate term: PinchBench +0.5 / +2.1 points; Claw-Eval −1.4 / −2.6 points.
- The workloads are PinchBench and Claw-Eval under OpenClaw, not GUI tasks.

**authors and venue:**

Confirmed:
- Authors: 15, from Buqiang Xu to Ningyu Zhang (corresponding).
- v2 affiliations: Zhejiang University; University of Electronic Science and Technology of China; "Xi'an University of Electronic Science and Technology" (Xidian); HomologyAI.

Venue:
- arXiv v1 (15 Jun 2026) had the comment "LightMem Series: Work in Progress".
- v2 (28 Aug 2026) has the comment "EMNLP 2026 Findings". v2 also adds thanks to anonymous reviewers and the mixed-category analysis.
- I found no official EMNLP 2026 accepted list: 2026.emnlp.org/program/accepted_findings/ returned 404 on 28 Sep 2026. Keep it as a preprint and quote the arXiv comment.

Corrections:
- The code link changed from github.com/zjunlp/LightMem2 (v1) to github.com/zjunlp/LightRSI (v2). Dossier §3.2 row l.495 still says LightMem2.
- The credibility note is out of date. references.md l.119 lists TokenPilot under 'Module 2 additions' with 'Backs E174', not as a qualitative-use entry. It passes the rule.

**formula:**

- §2 Eq. (1): max_M Σ_{m∈C'} Û(m|C') / K(C').
- Eq. (2): K(C') = α·|C'_hit| + |C'_miss|, with α ≪ 1 and |C'| = |C'_hit| + |C'_miss|.
- App. A.2 Eq. (11): Cost = |C'_hit|·p_hit + |C'_miss|·p_miss + H_out·p_out, where H_out is the length of the generated responses.

There is no cache-write term and no time formula.

## 1. MemRefine, SRMT (qualitative only)

**read:** - MemRefine: https://arxiv.org/html/2606.13177v1 (v1, 11 Jun 2026, the only version). Full text read, including App. B.
- SRMT: only the abs page, https://arxiv.org/abs/2501.13200 (latest v2, 24 Aug 2026). Full text not read.
- Provenance: the yxf203/Awesome-Efficient-Agents README (main branch) lists both only as title plus link. The descriptions 'compressed cheatsheets', 'high token savings' and 'maintains success' come from the Gemini run in archive/Agent Acceleration Research Landscape.md l.36–37, not from the papers.

**verdict:** corrected

**effect:**

MemRefine reports no token, latency or cost number. It compresses a memory store that has already been built so that it fits a storage budget. Abstract: MemRefine "consistently meets target budgets while preserving downstream performance".

Setup (Table 1, App. B): LoCoMo, 10 samples, 1,986 questions. The judge and merge model is gpt-5-mini, the retriever takes top-k=10, and memory size is the JSON-serialized store.

Table 1 results, from the uncompressed store to the 70% and 30% budgets:
- A-MEM-style graph, F1: 0.4013 → 0.4014 (70%) → 0.3628 (30%).
- Mem0, F1: 0.2827 → 0.2888 (70%) → 0.2510 (30%).

LongMemEval-S (60 questions, GPT-4o-mini as judge):
- A-MEM: 0.5833, highest 0.6167 at the 50% budget.
- Mem0: 0.5167 → 0.4000 at 30%.

App. B: "All reported results are from a single compression and evaluation run".

SRMT, per its abstract, is a multi-agent reinforcement-learning method for partially observable multi-agent pathfinding (POGEMA, Bottleneck task). It has no LLM, token or cost figure.

The dossier's 'High token savings; maintains success' is supported by neither paper.

**mechanism and term:**

Neither work traces to a term of our formulas. Recommend dropping both from Part 2.

MemRefine:
- It is an offline compressor of the memory store, run after the store is built. Similarity proposes pairs of entries, and an LLM judge decides delete, merge or keep until size(M') ≤ ρ·size(M0).
- Its judge and merge calls run "during memory maintenance rather than at query time" (§3.2).
- Retrieval stays at top-k=10, so the prompt tokens per query (the prefill term) are neither targeted nor measured. It also adds offline LLM calls.
- It is not 'compressed cheatsheets'.

SRMT is not an LLM agent at all.

**authors and venue:**

MemRefine:
- Authors: Minjae Kim, Jinheon Baek, Soyeong Jeong, Sung Ju Hwang (Korea University, KAIST, DeepAuto.ai).
- arXiv v1 of 11 Jun 2026, no venue comment, so a preprint.
- It names public benchmarks with counts and the model, so it would pass the credibility rule, but it has no term.

SRMT:
- Authors: Alsu Sagirova, Yuri Kuratov, Mikhail Burtsev.
- arXiv v1 22 Jan 2025, v2 24 Aug 2026; comment "16 pages, 11 figures".
- Affiliations not checked (abs page only). It is out of scope either way.

**formula:**

- MemRefine §3.1 Eq. (1): max_{M'∈F(M0)} min_{q∈Q} U(q,M') subject to size(M') ≤ ρ·size(M0). This is about storage, not time or money.
- SRMT: not read.

## 2. Don't Break the Cache

**read:** https://arxiv.org/html/2601.06007v2 (v2, 31 Jan 2026). Full text read, including App. A–C. I also opened the v1 PDF (9 Jan 2026) to compare versions.

**verdict:** corrected

**effect:**

Abstract (v2): "prompt caching reduces API costs by 41-80% and improves time to first token by 13-31% across providers".

Setup (§3.1–§3.4):
- Benchmark: DeepResearch Bench (100 tasks), with a Deep Agents (LangChain) research agent that calls a web-search tool.
- Models: GPT-5.2, Claude Sonnet 4.5, Gemini 2.5 Pro, GPT-4o.
- "40 independent agent sessions per cache condition" per model, with a 10,000-token system prompt.
- Four conditions (no cache, full context, system prompt only, exclude tool results), so 4 × 4 × 40 = 640 sessions (calc.). The paper says "over 500".
- Baseline: a UUID prepended to the system prompt forces the model to recompute every token.
- Cost: API-reported standard, cache-read and cache-write tokens × January 2026 list prices (App. A Table 3), per session.
- TTFT is measured from streaming. Means are compared with t-tests, n=40.

Table 1 (best mode per model):

| Model | Cost | TTFT |
|---|---|---|
| GPT-5.2 | −79.6% | −13.0% |
| Sonnet 4.5 | −78.5% | −22.9% |
| Gemini 2.5 Pro | −41.4% | −6.1% |
| GPT-4o | −45.9% | −30.9% |

Corrections:
- The paper's own table gives a TTFT range of 6–31%. §4.1 says "time to first token improvements range from 6% to 31%"; the abstract's 13–31% leaves out Gemini.
- Across all modes (Table 2), cost falls 27.8–81.4%. TTFT changes range from −8.8% (GPT-4o full context, i.e. slower) and −2.9% (Gemini, exclude tool results) to 30.9%. The claim that caching "can paradoxically increase latency" rests only on GPT-4o full context.
- §4.2: "the primary driver of cost reduction is caching the large system prompt".
- No task-quality or success metric is reported.
- Version change: the v1 abstract said "45-80%". v1 has no ablation study.

Ablation, §6.1 (v2): with 50,000-token prompts, GPT-5.2 saves 89% ($0.253 → $0.029), Sonnet 4.5 88% and GPT-4o 54%. GPT-4o's TTFT falls 60% (4,290 → 1,699 ms).

**mechanism and term:**

This is a measurement study, not a method. Its rules for controlling cache boundaries:
- put static content first;
- put dynamic values at the end of the system prompt;
- keep a fixed tool set instead of dynamic function calling;
- insert a UUID break after each tool result.

The term mapping is right, with two refinements:
1. Money by billing class is not only miss → hit. It also means fewer cache-write (store) tokens: the paper explains the full-context regressions by cache writes "for dynamic tool calls and results" (§4.3).
2. TTFT through a public API measures queueing and prefill together, not prefill alone.

The success-rate term is not measured. Savings are measured against an artificially forced no-cache baseline, within single sessions, with the 10K system prompt dominating. Not a GUI workload.

**authors and venue:**

Confirmed:
- Authors: Elias Lumer, Faheem Nizar, Akshaya Jangiti, Kevin Frank, Anmol Gulati, Mandar Phadate, Vamse Kumar Subbiah.
- All are at PricewaterhouseCoopers, U.S. (correspondence elias.lumer@pwc.com).

Venue: arXiv v1 9 Jan 2026, v2 31 Jan 2026; comment "16 pages, 9 figures". No venue, so an industry preprint without peer review.

The public benchmark, models and session counts are stated, so it passes the rule as recorded (order-of-magnitude use).

**formula:**

No equation. §3.3 describes the cost in words: each token type (standard input, cached input or cache read, cache creation or write) × the provider price, summed over all API calls in a session.

App. A Table 3 lists the prices. It notes that Google's cache storage fee ($4.50 per M tokens per hour) is "accounted for separately".

## 3. AgentReuse

**read:** - https://arxiv.org/html/2512.21309v2 (v2, 25 Dec 2025). Full text read.
- The CRAD page https://crad.ict.ac.cn/en/article/doi/10.7544/issn1000-1239.202440380: metadata and abstract only. The Chinese full text was not read.

**verdict:** corrected

**effect:**

Abstract: "reducing latency by 93.12% compared with baselines without using the reuse mechanism"; F1 0.9718, accuracy 0.9459, "93% effective plan reuse rate".

§6.5 shows the −93.12% is computed, not measured end to end:
- "We assume a plan generation latency of 31.8s and that all non-True Positive cases require plan generation".
- Execution latency is excluded.

The §6.5 arithmetic:
- No reuse: 2,644 × 31.8 s = 84,079.2 s.
- AgentReuse: 2,644 × 23.489 ms + 180 × 31.8 s = 5,786.1 s, hence −93.12%.
- GPTCache: 2,183 true positives and 461 others give 14,690.28 s, hence −60.61% for AgentReuse. The §6 intro misstates this as "60.61 percentage points".

Where the inputs come from:
- The 31.8 s is the mean of "100 tests" on the Open-Assistant dataset with AutoGen + GPT-4 API (§4). That is a different dataset from the SMP set that produced the true-positive counts.
- The request count is inconsistent: §6.1 says SMP2019 "contains 2,664 task requests" (23 intents), but §6.5 uses 2,644 (2,464 + 180).

Similarity results (Table 1, γ = 0.75):
- AgentReuse: F1 0.9718, precision 0.9931, recall 0.9513, accuracy 0.9459.
- GPTCache: F1 0.9100, accuracy 0.8366.

Effective reuse (§6.3): 20 requests × 5 runs; 93 of the 100 responses matched a fresh AutoGen run.

Overhead (§6.4): 23.489 ms per request, measured over 50 tests, and about 500 MB of VRAM, on an A100 80GB.

**mechanism and term:**

The term is right, with corrections.

On a hit, the single planning LLM call is skipped. In the paper's example this GPT-4 call takes about 25 s, of which "plan generation latency is about 24 seconds". It is replaced by BERT intent classification, m3e-small embedding and a FAISS search (about 23.5 ms).

Term: c_k smaller. This removes that call's queueing, prefill and decode time and its tokens. The only cost figure is one example (2,015 tokens, $0.073); no aggregate cost is measured.

The execution time t_e (environment) is unchanged and excluded. The workload is one plan per request, not an iterative loop and not GUI.

Success-rate term:
- '≈5% wrong' = 1 − 0.9459 = 5.41% (calc.). Most of these are missed reuses (recall 0.9513), which cost latency, not correctness.
- Wrong reuse is bounded by precision 0.9931, about 0.7% of reuse decisions (calc.).
- The only end-to-end check is 93 of 100 identical responses.

Label the −93.12% as an author estimate modelled from measured components, not a stopwatch measurement.

**authors and venue:**

arXiv:
- Authors: Guopeng Li, Ruiqi Wu, Haisheng Tan (corresponding), all at the University of Science and Technology of China, Hefei.
- v1 24 Dec 2025, v2 25 Dec 2025. The comment says it is the English version of a 2024 CRAD paper.

The CRAD page confirms the journal paper:
- Authors: Li Guopeng, Wu Ruiqi, Tan Haisheng, Chen Guoliang.
- Journal of Computer Research and Development, 2024, Vol. 61, Issue 11, pp. 2706–2720, DOI 10.7544/issn1000-1239.202440380.
- Online 17 Jul 2024, in the AIoT special issue.

Cite the journal paper; Chen is missing from the arXiv author list. The work is not in references.md. As a journal paper with a public dataset (SMP2019) and a named model, it is citable.

**formula:**

- §3: t = t_p + t_e. t_p is the plan generation latency, from receiving the request to <EOS>; t_e is the execution latency. Reuse "can eliminate the plan generation latency t_p".
- §5.1 Eq. (1): cosine similarity.
- §6.5 gives the latency model in words: total = N_requests × 23.489 ms + N_non-TP × 31.8 s.

## 4. ToolCaching

**read:** https://arxiv.org/html/2601.15335v1 (v1, 20 Jan 2026, the only version). Full text read, including App. A–C, plus the PDF.

**verdict:** corrected

**effect:**

Abstract: "up to 11% higher cache hit ratios and 34% lower latency compared to standard policies". The body separates the two numbers.

The −34% is measured against no caching, not against standard policies. §6.4: "compare the performance of ToolCaching with the baseline LLM Compiler framework without caching".

Table 4:
- Movie Recommendation (LLMCompiler dataset, 500 examples, 8-way parallel), cache size 100% of calls: 16.2 s → 10.7 s at hit ratio 0.514 (−33.95%, calc.). At 20% the latency is 13.81 s; at 50%, 11.88 s.
- ParallelQA (113 questions): 15.9 s → 12.18 s at 100% (−23%).

Setup: DeepSeek V3 (cloud) serves both LLMCompiler and feature extraction. The cache server has 16 GB RAM and 8 CPUs.

Not stated or not reported:
- whether latency is per query or a total;
- task accuracy;
- whether the cache starts warm.

Table 4's 'Improvement' column (1.34×, 1.23×) is 1 + the fractional reduction, not a speedup. The actual ratio is 16.2/10.7 = 1.51× (calc.).

Against standard policies (CACA, LRU), there are synthetic results only (§6.2): 3 workloads of 1,000 requests over 6 tools (Zipf α=1.1, shifting hotspot, uniform), with cache sizes of 10–90% of unique requests.
- Hit ratio up to 11% higher; the paper does not say whether that is points or relative.
- Under Zipf, total latency up to −17.3% and resource cost −6.4% (Fig. 4).

Other numbers:
- 10 simulated users: grouping by user gives +21.3% hit ratio and −7.1% latency (Table 3).
- Overhead: about 15% CPU and 10% memory (§6.5).
- Feature extraction on 50 BFCL requests: request-type accuracy 0.980, TTL accuracy 0.920 (Table 2).

**mechanism and term:**

The term is right: environment. On a cache hit, the tool's run and wait time (network plus execution) is removed.

Only informational calls whose TTL is over 60 s can be cached. Command calls never are (§5.2).

Refinements:
- Each new tool request also gets a DeepSeek V3 call to extract semantic features, so c_k is larger on misses. The cost of that call is not reported.
- Per-call tool fees (Table 1) are an environment cost that falls outside our tokens × price formula.
- The risk to success rate from stale results is not measured; no task accuracy is reported.
- The workload is LLMCompiler tool calling, not an iterative GUI loop.

**authors and venue:**

Authors now verified: Yi Zhai, Dian Shen, Junzhou Luo, Bin Yang, School of Computer Science and Engineering, Southeast University, Nanjing (seu.edu.cn emails). Condition (i) is met.

Venue: arXiv v1 of 20 Jan 2026 only, no comment. The PDF carries an unfilled ACM template header ("Woodstock, NY", 2018, DOI XXXXXXX). No venue, so a preprint.

The −34%-vs-no-cache figure uses public benchmarks with counts (LLMCompiler Movie Recommendation 500, ParallelQA 113) and a named model (DeepSeek V3), so it passes the rule. The comparison against standard policies is synthetic only.

**formula:**

- Eq. (1): min-max normalization.
- Eq. (2): caching value v_i = λ1·NormLatency_i + λ2·NormCost_i/NormSize_i − λ3·e^(−TTL_i/τ). §6.2 uses λ1 = 0.8, λ2 = 0.2, λ3 = 0.2.
- Eq. (3): bandit reward F_i = log(H_i+δ1)·log(L_i+δ2)·log(V_i+δ3) / log(C_i+δ4), solved with UCB1.
- Eq. (4): eviction score e_i = log(v_i + h_i + δ5).

There is no speedup or cost formula.

## 5. AgentRR (qualitative only)

**read:** https://arxiv.org/html/2505.17716v1 (v1, 23 May 2025, the only version). Full text read.

**verdict:** confirmed

**effect:**

Confirmed: there is no quantitative result for AgentRR.

- §5, the case study (web form filling), gives no AgentRR measurement. Its only number is about another system: "OpenAI's CUA requires approximately three minutes to process this form", and CUA still falls short of completing the task.
- Table 2 is a qualitative High/Low comparison ("High (Exceeds human speed)"), not measured.
- The introduction's Manus figure, "on the order of $2 USD" per task, is reported second-hand ("reportedly") and is not about AgentRR.

**mechanism and term:**

How it works: it records a trace, summarises it into multi-level experiences (high-level procedural knowledge; low-level scripts or API calls) with check functions, then replays them.

Terms, all claimed and none measured:
- c_k smaller: low-level replay runs recorded scripts without an LLM call per step. §1: "the number of calls or the capability required by the LLM is drastically decreased".
- Price/tier: in 'Large Model Record, Small Model Replay' a small or local model does the replay.
- N: the same actions are replayed, so N is in principle unchanged. The paper gives no N figure.
- Success rate: check functions act as guardrails, and replay falls back from low-level to high-level experience when it fails.

Keep it as a pointer only. It fails condition (iii): no numbers.

**authors and venue:**

Authors now verified: Erhu Feng, Wenbo Zhou, Zibin Liu, Le Chen, Yunpeng Dong, Cheng Zhang, Yisheng Zhao, Dong Du, Zhichao Hua, Yubin Xia (corresponding), Haibo Chen. All are at the Institute of Parallel and Distributed Systems (IPADS), Shanghai Jiao Tong University, per the paper's front matter. The dossier's 'believed SJTU' is confirmed.

Venue: arXiv v1 only, no comment. It is a vision/position preprint.

**formula:**

None for speed or cost. The paper only has state-transition notation: S →(A) S', and a trajectory S0 →(A1) S1 … →(An) Sn (§3.4).

## 6. SkillWeaver

**read:** arXiv:2504.07079v1 (9 Apr 2025; the only version), PDF via pdftotext, plus arXiv HTML v1 for Table 1. https://arxiv.org/pdf/2504.07079v1

**verdict:** confirmed

**effect:**

The recorded numbers match the paper. Conditions below were missing from the record. Table 1 (p.7), WebArena, GPT-4o (gpt-4o-2024-08-06, temp 0.3): AVG success 22.6 -> 29.8 with +Skills, 'Δ ↑32%'. Abstract: 'relative success rate improvements of 31.8% and 39.8%' (WebArena / real-world). Conditions: (a) The WebArena run covers the 5 single-site domains only. App. B lists Gitlab 180, Map 109, Shopping 187, CMS 182, Reddit 106 = 764 tasks (calc.), not 812. AVG is task-weighted; the per-site values reproduce 22.65 / 29.81 (calc.). (b) 'Online-Mind2Web' means a 57-task, 4-website subset of its 300 tasks (Drug, Flight, Cooking, Car), manually evaluated (§3.2). Table 2: 40.2 -> 56.2, 'Δ ↑40%'. (c) Max 10 steps per iteration (§3.3). (d) Before evaluation, APIs come from 160 exploration iterations per website with GPT-4o (§3.4). (e) Transfer: GPT-4o-synthesised APIs used by a GPT-4o-mini agent, 9.2 -> 14.1. Internal inconsistencies: Table 1 prints 'Δ ↑45%' for this row, the abstract and conclusion say 54.3%, and 14.1/9.2 = +53.3% (calc.). §4.1 also says '39.8% on average' for the GPT-4o WebArena agent, contradicting the abstract's 31.8% (D-candidate). No latency, token or $ figure anywhere, and the exploration cost is mentioned only qualitatively (§3.2 'Considering the cost of exploration').

**mechanism and term:**

Correct as 'intended N and c_k smaller, only success measured'. Each skill is an async Playwright function that runs several browser actions with no LLM call per action. One API call can therefore replace several LLM-chosen passes, but the paper never counts steps, calls, tokens or time. Two additions for the term map: (1) a one-off pre-deployment exploration cost (160 GPT-4o iterations per site) sits outside the per-task sum, like PANDO's C_pre; (2) the retrieved API signatures and docstrings, plus an 'API selection module' that filters the library, add prefill per call. Success rate is the only term measured.

**authors and venue:**

Authors (11) and institutions confirmed on the PDF title block: Zheng, Fatemi, Jin, Wang, Gandhi, Song, Gu, Srinivasa, Liu, Neubig, Su. Affiliations: Ohio State, U. Virginia, Purdue, CMU, Cisco Research; Cisco gift acknowledged. Preprint: arXiv has only v1 with no journal-ref, OpenReview search returns only a 'CoRR 2025' record, and the GitHub README names no venue. The record's label 'preprint, institutions verified' is right.

**formula:**

None. The paper gives no formula for speedup or cost.

## 7. WALT (Web Agents that Learn Tools)

**read:** arXiv:2510.01524v1 (1 Oct 2025; the only arXiv version; its PDF header reads 'Preprint. Under review.'), PDF, plus the Figure 3-right image from arXiv HTML v1. The ICLR camera-ready PDF on OpenReview (id cgIDqcJcoI) could not be read: openreview.net returned a challenge page. Its numbers may differ from v1.

**verdict:** corrected

**effect:**

Table 2 (p.8), 'Ablations on VisualWebArena-Classifieds', column 'browser LLM' = gpt-5-mini: none/text/self 8.9 steps, 57.5% SR. Discovered tools 6.5 (−27.0%), 61.5% (+7.0%). Human-demo tools 7.4 (−16.9%), 66.0% (+16.2%). Full WALT (discovered/multimodal/external) 7.0 (−21.3%), 64.1% (+11.5%). All record values confirmed. Corrections: (1) Model: gpt-5-mini is only the browser executor. §4.3: 'we pair a VLM planner (GPT-5 OpenAI (2025)) with a browser action executor (GPT-5-mini)', at most 30 steps, replanning every 15, GPT-5-mini as verifier. Classifieds = 234 tasks (§4.2). (2) '1.3–1.4x fewer steps on average' (§1) comes from Figure 3-right, labelled 'faster' though it measures average #steps, not time. Per split: 7.9 -> 6.1 '1.3x', 10.2 -> 7.3 '1.4x', 8.3 -> 6.4 '1.3x'. Rows are unlabelled; by SR they are presumably Classifieds, Shopping, Reddit. So 1.3–1.4x is a range across splits, not an average. (3) Figure 3-right's Classifieds row (64.1 vs 57.5 SR, 6.1 vs 7.9 steps; 7.9/6.1 = 1.30x, calc.) disagrees with Table 2 for the same SRs (7.0 vs 8.9 steps; 1.27x, calc.). Its other WALT SRs (53.7, 40.0) also differ from Figure 3-left (Shopping 53.4, Reddit 39.0) (D-candidate). Headline SRs: VWA 52.9% (910 tasks), WebArena 50.1% (812). No wall-clock, token or $ figure: the text claims tools 'run faster and with fewer LLM calls' (§3) without measuring either. Limitations: 'Offline tool discovery incurs an exploration and validation cost per-website' (§6), unquantified.

**mechanism and term:**

Mostly right, with additions. Tools are schema-checked action scripts that WALT promotes to deterministic URL operations where possible; agentic steps are rare, only 3 of 9 Classifieds tools (§4.5). This shrinks N (steps) and lifts success. It also lowers c_k per step, since deterministic script steps need no LLM call, but that is claimed, not measured. A one-off pre-deployment discovery cost (C_pre) is added and unreported in the paper. PANDO App. H estimates it from WALT's released logs at 1.42e7 input + 2.1e6 output tokens, 'approximately $43.7', and gives WALT's released per-task cost as $0.593 on VWA. Both are secondary, not from the WALT paper. Adding the external verifier raises steps (Table 2: 11.0 steps, +23.6%), so one component increases N.

**authors and venue:**

The ICLR 2026 claim holds. The OpenReview search API returns venue 'ICLR 2026 Poster', venueid ICLR.cc/2026/Conference, with bibtex booktitle 'The Fourteenth International Conference on Learning Representations'. The OpenReview author order puts Ramakrishnan before Gu; arXiv puts Gu first, as references.md already notes. Institution: Salesforce AI Research (PDF title block). arXiv v1 itself is the under-review preprint.

**formula:**

None for speedup or cost. The method has an attempt budget N_max in its Algorithm (appendix) but no cost equation.

## 8. CoAct-1

**read:** arXiv:2508.03923v3 (20 Feb 2026, latest), PDF. v1 (5 Aug 2025) PDF also read for comparison. https://arxiv.org/pdf/2508.03923v3

**verdict:** confirmed

**effect:**

The recorded numbers match v3, with added conditions. Table 1 (p.7), 'OSWorld verified benchmark', 100 steps: GTA-1-7B w/ o3 53.07 -> CoAct-1 59.93 (Avg. SR %). §4.5 and Figure 3a ('Average steps per passed task with 100 step budget'): CoAct-1 10.15 vs GTA-1 15.22 vs UI-TARS 14.90 vs OpenAI CUA 4o 6.14. 'OpenAI CUA 4o averages fewer steps (6.14)' at 31.40% vs 59.93% SR. Conditions and caveats: (1) The baseline is GTA-1-7B with o3 as planner. (2) The abstract headline is 60.76% (rounded to 60.8% in the v3 abstract) at a 150-step budget; only CoAct-1 was run at 150. (3) Table 4 pairs 'Avg. Steps' 10.15 with the 60.76% (150-step) configuration, while Figure 3a labels 10.15 as the 100-step budget. The paper uses both, so the budget behind 10.15 is ambiguous (D-candidate). (4) Table 4 defines steps differently in its own text: 1.14 'steps per success' (Programmer-only) vs 11.20 'steps per task' (GUI-only). (5) Task count: §4.1 says 'OSWorld comprises 369 tasks', but Table 1's category counts sum to 355 (104+78+48+24+101, calc.). (6) Setup: Orchestrator o3-2025-04-16, Programmer o4-mini-2025-04-16, GUI Operator computer-use-preview-2025-03-11, o4-mini summarizer; maxima of 15 Orchestrator rounds, 25 GUI steps and 20 Programmer rounds. v3 adds WindowsAgentArena: 52.5% at 100 steps (154 tasks). No time, token or $ figure (confirmed).

**mechanism and term:**

'N smaller, success up' is right, with two corrections. (1) A 'step' is 'the number of system interactions' (§4.3), i.e. GUI actions or script executions, not model calls. Each subtask also needs Orchestrator calls and a summarizer call, so model calls per step (c_k) rise; fewer steps does not by itself mean fewer calls or less time. (2) Memory design: executor histories are cleared after each subtask and the Orchestrator sees only summaries plus the latest screenshot (§3). That is a structural change to context growth (the N² term), but the paper does not measure it. One script can replace many GUI passes, which cuts both N and environment act/wait time; neither time nor money is measured.

**authors and venue:**

The ICLR 2026 claim holds. The v3 PDF header reads 'Published as a conference paper at ICLR 2026', and the OpenReview search API returns 'ICLR 2026 Poster', with bibtex booktitle 'The Fourteenth International Conference on Learning Representations', 2026. Authors (12): Linxin Song, Yutong Dai, Viraj Prabhu, Jieyu Zhang, Taiwei Shi, Li Li, Junnan Li, Silvio Savarese, Zeyuan Chen, Jieyu Zhao, Ran Xu, Caiming Xiong. Institutions: University of Southern California, Salesforce, University of Washington (v3 title block). The credibility status can move from 'to check' to 'passes: conference paper'.

**formula:**

No speedup or cost formula. It has only a problem definition: policy π(a_t | H_t, G) with H_t = (o_1, a_1, ..., o_{t-1}, a_{t-1}, o_t), and hybrid action space A = A_GUI ∪ A_Code (§3.1). The step upper bound of 375 is stated in text only (§4.3).

## 9. ASI (Inducing Programmatic Skills)

**read:** arXiv:2504.06821v2 (29 Aug 2025, latest; PDF header 'Published as a conference paper at COLM 2025'), PDF. For the Hajimiri et al. claim: arXiv:2606.15017v2 (30 Aug 2026) and v1, PDFs.

**verdict:** corrected

**effect:**

Table 1 (p.5), WebArena (812 examples), Claude rows: Vanilla 5.6 steps, 32.7 SR; AWM 5.9, 36.3; ASI 5.0, 40.4. Model: 'claude-3.5-sonnet' for the policy, the neural evaluator and the induction module. Framework: BrowserGym with accessibility-tree observations. Abstract: '23.5% and 11.3% in success rate' (relative) and 'reducing 10.7–15.3% of the steps'. Corrections: (1) Scaled-up tasks, Table 4 (p.7): the '6.6–14.6 and 4.0–8.4% fewer steps' sentence (§4) actually gives absolute step reductions, not percentages. The Table 4 differences are 6.6–14.6 steps vs vanilla and 4.0–8.4 vs AWM (calc.), and the intro says 'by 9.5 and 5.6 average steps'. In percent that is 31–59% fewer than vanilla and 22–51% fewer than AWM (calc.). These tasks are about 25 (5 per website, Tables 9–13, calc.), scored by % of checkpoints reached. (2) §3.2 text swaps the baselines ('15.3% and 10.6% than vanilla and AWM'). Table 1 gives −10.7% vs vanilla (5.0 vs 5.6) and −15.3% vs AWM (5.0 vs 5.9) (calc.). The record's pairing follows the table and is right. No wall-clock, token or $ figure anywhere. The paper reports only a per-step thought shortening from 87.9 to 13.4 tokens in the episode-cleaning input to induction (§2.3). Secondary claims: SpeedRunner §5 says 'ASI moves in the opposite direction on every benchmark, with cost growing as the library accumulates'. That was measured on ScienceWorld, BabyAI and Crafter with GPT-5.4-mini, using an adapted ASI whose verification step was removed (§4.1). Hajimiri et al.: the numbers in references.md l.111 are from v1 (3 WebArena domains; Gemini 3 Flash Vanilla-IB 50.74% / 71.9K vs ASI 47.86% / 107.1K tokens per task). v2 (30 Aug 2026; 4 domains, 655 tasks, calc.; 3 runs) gives Vanilla-IB 44.78% / 73.6K vs ASI 41.02% / 107.3K (Table 1). Same direction, so this is a D-candidate version change. Vanilla-IB uses a 15-step horizon vs 10 for ASI.

**mechanism and term:**

'N and c_k smaller, success up' is right for the task-solving loop: a skill call runs several primitive actions from one LLM decision. Additions: (1) Online induction adds model calls and passes per task that '# Steps' does not count: a neural evaluator per episode, the induction module, and a verification re-run of the task with the skill prefix (§2.3). This is C_induce in PANDO's notation and is unreported. (2) The paper does not say skills add prefill as the library grows, but skills enter the action space shown to the model (A_t ∪ {d_t} -> A_{t+1}). SpeedRunner (§3) cites Wang et al. 2025a: an unbounded library puts 'too many functions in context'. So 'library adds prefill' is supported secondarily, not by ASI's own measurements.

**authors and venue:**

The COLM 2025 claim holds: the v2 PDF header reads 'Published as a conference paper at COLM 2025', and the OpenReview search returns venue 'COLM 2025' (colmweb.org/COLM/2025/Conference). Authors Zora Zhiruo Wang, Apurva Gandhi, Graham Neubig, Daniel Fried, Carnegie Mellon University (title block). Hajimiri et al.: ServiceNow AI Research, ÉTS Montréal, UBC, McGill; the arXiv comment reads 'Accepted to EMNLP 2026'.

**formula:**

None for speedup or cost. There is only notation for induction: I(e) -> D, M_t ∪ {d_t} -> M_{t+1} for AWM, A_t ∪ {d_t} -> A_{t+1} for ASI (§2.2).

## 10. SpeedRunner

**read:** arXiv:2608.11338v1 (11 Aug 2026; the only version), PDF, plus arXiv HTML v1 for the cost formula. https://arxiv.org/pdf/2608.11338v1

**verdict:** confirmed

**effect:**

(1) BabyAI 1/8: §5 says 'final usage falls to roughly an eighth of the ReAct baseline', and App. G.4 says 'final per-eval-epoch output reaches roughly an eighth of the ReAct baseline'. ReAct is at about 67%, SpeedRunner 'near-perfect'. The ratio is read from figures (Fig. 3/8); no table value. It applies only to the BabyAI subtask pick_up_seq_go_to (BALROG BabyAI-Text), with a 30-LLM-call budget per episode. (2) '2–8×' vs ASI: §6.2.2 says 'explaining SpeedRunner's 2–8× token reduction over ASI', with no per-benchmark breakdown. The ASI here is adapted, with its replay verification removed (§4.1, App. E). App. G.3 (ScienceWorld task 3): about 65% fewer output tokens than both ASI and ASI with replay. (3) Crafter −94%: App. G.2 says 'Gemini-3-Flash reduces LLM calls by 94% over training'. In the same passage the authors say SpeedRunner 'can over-compress a capable actor', and it is significantly worse than OPO in SR with Gemini on all benchmarks. Missing conditions (§4.3, App. A–D): actor and inducer are both gpt-5.4-mini (main results); 200 online training rollouts with a sleep cycle every 10; a fixed held-out test set of 30 episodes per benchmark (30 ScienceWorld test variations per task family, 30 BabyAI test seeds, 30 Crafter test worlds), evaluated every 50 rollouts; 3 seeds, mean ±1 s.d. across seed-level values; 30-minute wall-clock cap per rollout, with wall-clock never reported as a result. Benchmarks are text-only: ScienceWorld tasks 3 (Electricity) and 4 (Classification) with a 100-LLM-call budget, and Crafter with a 2,000-action budget and 22 achievements. Metric ambiguity (D-candidate): §4.3 defines efficiency as 'output tokens per episode', and the Fig. 3 caption says 'output-token cost'. Yet App. A.3 says Figure 3 uses the full $ cost (uncached input + cached input + output) including amortised inducer calls. Also §6.4 (ScienceWorld shift): SpeedRunner −27.1% inference cost on task 3 after task-4 training; ASI +40.6%.

**mechanism and term:**

The mechanism is right: a coding-agent 'inducer' edits an executable skill library in wake–sleep cycles, analysing the saved trajectories with a code interpreter. The term mapping needs two additions. (1) The drops in LLM calls and output tokens come from the actor finishing episodes 'with one or two high-level calls' (§6.2.2). That shrinks N and c_k and hence decode; prefill falls too, because fewer calls re-read the full in-episode history (kept with no sliding window, App. B.3/C.3). (2) The method adds a sleep-phase inducer cost, amortised into the per-rollout $ (App. A.3), and it caps prompt growth from the library by hiding helper functions as private (§3). Money is accounted by billing class (see formula). Robustness caveat: in the paper's own tests SpeedRunner beat OPO on SR only with GPT-5.4-mini; with Gemini-3-Flash and in one Qwen setting, OPO won on SR.

**authors and venue:**

Confirmed. Zixi Huang, Xiheng Wang, Andrew Wang, William Jurayj, Bernal Jiménez Gutiérrez, Daniel Khashabi, Nicholas Andrews, all Johns Hopkins University (@jhu.edu); preprint (PDF footer 'Preprint.', no arXiv journal-ref). It passes the references.md rule: public benchmarks, named models, and task counts (30 test episodes per benchmark, 200 training rollouts) that are now in the record.

**formula:**

App. A.3, 'Cost Accounting': cost = p_in N_in^uncached + p_cache N_in^cached + p_out N_out. The Ns are summed over all LLM calls in the episode, including actor calls and 'sleep-time inducer calls amortized over the rollouts in the corresponding inducer batch'. Prices are the published API prices as of 6 May 2026. gpt-5.4-mini: p_in = $0.75, p_cache = $0.075, p_out = $4.50 per 1M tokens. gemini-3-flash-preview: p_in = $0.35, p_cache = $0.0875, p_out = $1.05. The paper also defines call-graph density |E|/(|V|(|V|−1)) (§6.2.1), which is not a cost formula.

## 11. PANDO

**read:** arXiv:2605.24785v2 (26 May 2026, latest), PDF plus arXiv HTML v2 for the equations. v1 (24 May 2026) PDF also read: its text is identical except the arXiv stamp.

**verdict:** corrected

**effect:**

Table 2 (p.7), 'full VisualWebArena benchmark (910 tasks)', one run in a fixed stream order (seed 42). PANDO (Opus 4.6 + GPT-5.2): SR 58.3, Steps 9.3, Tokens 115K, Time 240.0 s, Cache 72.4%. SGV (Gemini Flash): 54.0 / 13.5 / 275K / 392.1 s / 45.1%. WALT (Sonnet-4 + thinking, their reproduction): 45.2 / 10.5 / 294K / 531.3 s / 38.6%. Abstract: '58% fewer tokens than SGV and 61% fewer than WALT' (115/275 = −58.2%, 115/294 = −60.9%, calc.). Corrections and conditions: (1) The 58–61% applies to SGV and a WALT reproduction only, not to 'baselines' in general. Against the GPT-5.2 Text-Only row (132K) PANDO uses 12.9% fewer tokens (calc.). The WALT reproduction reaches 45.2%, not the 52.9% WALT reports (D-candidate). (2) 'Tokens' means prompt + completion + reasoning per task, cached tokens included (§5). The backbones differ per system, so raw token counts are not like for like. (3) The paper does report wall-clock and dollars, which the record omits. Time is 'wall-clock seconds from environment reset to terminal verdict': PANDO 240.0 s vs SGV 392.1 (−38.8%, calc.) and WALT 531.3 (−54.8%, calc.). PANDO is not the fastest row (GPT-5.2 + SoM 181.5 s). Per-task $ at April-2026 API prices (App. I, Table 8): PANDO $0.085, SGV $0.371, WALT $0.592 ($0.641 amortised); $/success PANDO $0.146 vs WALT $1.310. (4) The claim of 'no pre-evaluation discovery budget' is accurate, but the library starts from hand-given seeds: 'Seed routines / benchmark 12' and 'Seed rules (universal + site) 8+6' (Table 6). (5) 'Steps' counts each LLM call (Planner, Reflector, Actor), each routine invocation and each primitive action (§5). (6) Table 3 (VWA-300 ablation) shows routing, compression and cache-aware prompting cut tokens 147K -> 117K and raise cache 69.3% -> 72.0%. Table 4: per-task tokens fall from 143K (tasks 1–100) to 103K (601–910). A 16-worker shared-library run: 58.1% SR, wall-clock 48.2 h -> 3.1 h (parallelism across tasks). Internal inconsistencies (D-candidate): Table 2 labels the baseline 'GPT-5.2 Text-Only' but Table 5 lists GPT-4o-mini. WALT's backbone is 'Sonnet-4 + thinking' in Table 2 but Claude Sonnet 4.5 in Table 5. Tables 3 and 9 add the components in different orders from different baselines, and Table 9 claims 'the same final PANDO SR' for 59.0 vs 58.3. WALT's discovery cost '$43.7' cannot be reproduced from the stated 1.42e7 input + 2.1e6 output tokens at the paper's own Sonnet 4.5 prices: Table 5 gives $0.30 cached = 0.1x base, so base $3.00, output $15, which bounds the cost at $35.8–$74.1 (calc.). WALT's per-task cost appears as $0.593 (App. H) and $0.592 (Table 8).

**mechanism and term:**

The record's mapping is right but incomplete. (1) prefill: visual compression, with β = E[q̃_vis/q_vis] ≈ 0.6 on the actor's visual tokens. (2) N: rules stop repeat-action loops (ARR 39.1% -> 9.4% in Table 3), and routines replace multi-step subgoals ('3.7 fewer primitive browser actions and 41K fewer tokens' per routine-backed subgoal). (3) c_k and the price/tier term: hierarchical routing sends planning and reflection to an expensive model (κ_H) used sparsely, with the Reflector firing every k_R = 3 actions or on an error, and sends high-frequency actions to a cheaper actor (κ_L). This is a per-call model-choice mechanism, not only a skills effect. (4) Money by billing class: a cache-aware prompt layout puts stable instructions, schemas and skill summaries before volatile history, raising the cache share. (5) Success rate up. (6) It pays C_induce inside the task stream instead of C_pre before it. Reported cost falls along the stream: per-task $0.164 at task 1 -> $0.062 at task 910 (App. I.3).

**authors and venue:**

Four authors: Yubo Li, Yidi Miao, Yuntian Shen, Yuxin Liu (Shen and Liu marked co-third authors). The PDF has no affiliation line, only e-mails {yubol, yidim, yuntian2, yuxinli2}@andrew.cmu.edu. CMU can therefore be inferred only from the e-mail domain. Preprint: PDF footer 'Preprint.', no arXiv comment or journal-ref; v1 24 May, v2 26 May 2026 with identical text. Against the references.md rule: public benchmark (VWA, 910 tasks) and named models (Table 5) pass. Institution is verifiable only by e-mail domain, and the paper has several internal inconsistencies (listed under effect). Suggested label if used: 'preprint; institution from e-mail domain (CMU); internal inconsistencies noted'.

**formula:**

§3: Eq. 1 SR(π) = (1/|B|) Σ_{τ∈B} y(ξ_τ). Per-task cost: C_task(τ; π) = N_rollout(τ) C_exec(τ) + C_verify(τ) + C_induce(τ). Eq. 2: C_total(π; B) = C_pre(π; B) + Σ_{τ∈B} C_task(τ; π). Eq. 3 (Proposition 1, 'Per-task cost identity'): C̄(π; B) := C_total/|B| = C_pre/|B| [amortized pre-eval] + mean(N_rollout C_exec) + mean(C_verify) + mean(C_induce). Overhead ρ(π) := C̄(π; B) / C̄(π_0; B). Eq. 4: C_task^SGV(τ) = C_exec(τ) + C_verify(τ) ≈ 2.2 C_exec(τ), ρ^SGV ≈ 2.2. Eq. 5: C_pre^WALT ≳ 100 K κ, ρ^WALT = 1 + C_pre^WALT / (|B| mean(C_exec)). Eq. 12 (§4 and App. A): C_exec(τ) = κ_H (|Plan(ξ_τ)| q^plan + ⌊T/k_R⌋ q^reflect) + κ_L T q^act, with κ_H > κ_L and k_R = 3. Eq. 13: cache utilisation U = Σ_i |P_i^cached| / Σ_i |P_i| (App. E: summed over Planner, Actor and Reflector calls, 'price-agnostic'). App. H: cost_amortized = 0.593 + 43.7/|B| ($0.641 at 910 tasks). Also Eq. 10 (demotion) and Eq. 11 (reflector firing: Reflect = 1[i mod k_R = 0] ∨ 1[err(a_{i−1})]).

## 12. SPORK (self-speculative forking)

**read:** arXiv:2607.03333v1 (3 Jul 2026; the abs page lists only v1, checked 28 Sep 2026). Full PDF read: https://arxiv.org/pdf/2607.03333v1 (16 pp. incl. App. A-H). Equations taken from https://arxiv.org/html/2607.03333v1. Scratch copies are in scratchpad/wf-part2/v6.

**verdict:** confirmed

**effect:**

All recorded numbers are in the paper. Paraphrased below; figures are exact.
(1) GAIA p95 131.9 -> 108.1 s (-18%) and p50 34.7 -> 31.2 s (-10%). Sources: Abstract; §1 p.2; §6.2; Figs. 10 and 12. Conditions: GAIA N=165 with real web search and page-browse tools (mean T_tool 4.8 s, Table 2); Qwen3-32B self-hosted on vLLM 0.19.1, TP=1, NVIDIA H20-3e, bf16, greedy (temp 0, seed 42), thinking mode on; full engine configuration D1+D2+D3; metric is per-query end-to-end wall-clock time. MISSING CONDITION: the baseline is the same vLLM running its built-in ngram speculative decoding (§6.1, Table 3), not plain serial decoding. Ngram alone already took P50 from 50.5 to 34.7 s (-31%, §6.4), so the -18% comes on top of it.
(2) tau2-bench 1.09x -> 1.18x. Sources: §1 p.2 and §6.6. This is a MEAN speedup (not P95) from a latency sweep over the airline domain with SIMULATED tool-latency floors of 0.5 s to 5 s. EQ1 predicts the observed speedups within 1.84%. Two problems: the intro gives N=43 but the Fig. 14 caption gives N=155, and neither sentence names the model.
(3) alpha ~0.37. Sources: §4.2 'Effect on EQ1' and §6.4. Setting: GAIA, Qwen3-32B, strict gate, D1+D2 (101 accepted, vs 49 accepted and alpha ~0.22 with D1 alone). Alpha is counted per tool-call turn. Dispatched probes were 2124 (D1+D2) vs 434 (D1). The gate threshold theta=0.90 was chosen on 997 probes, GAIA N=127: precision 88%, recall 100%, F1 0.937 (Fig. 8).
(4) Quality. EM stays within 1 pp of baseline on every benchmark and model (§6.3, Fig. 11). HotpotQA (N=200, Qwen3-32B): +1.5 pp EM, +0.012 F1, P95 speedup 1.06x. tau2 quality is identical by construction because the DB tools return canned results.
(5) Limits (§8 Limitations): needs open-weight models on an engine that exposes per-token logprobs and a completion endpoint; closed APIs cannot host the fork thread; the benefit shrinks under heavy batching. With no-think mode, tau2 slows down to 0.79x (§6.6).
Other results: Qwen3.5-35B-A3B (HTTP D1+D2 vs a serial baseline) cuts P95 by 16% on tau2 (59.4 -> 49.8 s, N=155), 16% on GAIA (222.4 -> 187.3 s, N=53, D1 only) and 20% on HotpotQA (18.9 -> 15.2 s, N=200). Qwen3-4B: tau2 1.15x mean at the 2 s floor, GAIA 1.03x, HotpotQA 1.00x (Table 4).
Proposed D-entry: the E128 and §3.3 row should add 'baseline = vLLM ngram spec-dec' and 'tau2 = mean speedup at simulated floors'. Record the internal N=43 vs N=155 inconsistency.

**mechanism and term:**

The recorded mechanism is right in substance. Precise version: after the main stream's first streaming token, SPORK sends a separate raw /v1/completions request with a forced <tool_call> prefix. That request reuses the main request's prefix KV cache through the engine's prefix caching, so its prefill is a cache hit (~0.05 s vs ~1.3 s). It is re-issued as the CoT grows (retry cadence). The predicted call is dispatched once the minimum top-1 probability over the tool-name span reaches theta=0.90. The pre-computed result is used only on an exact name+arguments match; otherwise the turn falls back to serial execution. Only tools marked read-only in a manifest are speculated; write and non-idempotent tools always run serially (§5).
TERM MAPPING:
(a) Main term: overlap saving is introduced. The environment wait (tool run) of pass k overlaps the remaining decode of the same pass's model call. Per turn this is bounded by min(T_tool, decode still remaining). Overall it is capped at S_max = 1/(1 - f_tool); on BrowseComp, f_tool = 0.366 gives 1.58x. It needs thinking-mode CoT to have anything to overlap.
(b) Secondary term: decode is smaller on rejected turns. D3 feeds the rejected probe's verified prefix to the engine as speculative-decoding draft tokens: about 0.6 s saved per rejected turn, about 0.31 s per turn amortized (offline BrowseComp analysis, App. B).
(c) Terms it makes worse, which Part 2 should show: more model calls per pass (c_k up; 2124 probes dispatched on GAIA for D1+D2), each with a cache-hit prefill and <=50 decode tokens; under 0.3% TPOT overhead on the main stream (Fig. 7); plus wasted speculative tool runs (extra environment work). On a self-hosted engine this costs GPU time, not API billing.
Success rate unchanged (within 1 pp). N and context growth unchanged.

**authors and venue:**

Confirmed. Authors: Huajun Bai (Tsinghua University), Weiwei Lv (Meituan), Huichuan Zheng (Tsinghua), Youyou Lu (Tsinghua), Jiwu Shu (Tsinghua, corresponding author). arXiv cs.DC, v1 3 Jul 2026, the only version; arXiv comment '16 pages, 15 figures'. No venue appears anywhere in the PDF, so this is a preprint. Code: github.com/baihuajun24/spork. It passes the source-credibility rule: authors and institutions are verifiable, and GAIA, HotpotQA and tau2-bench are public benchmarks with N and model stated. The tau2 sweep's model is not named.

**formula:**

EQ1 (§2.2, boxed): Ratio = T_base / (T*_base - alpha*t_overlap + T_oh). Speculation helps when Ratio >= 1, which approximately requires alpha*t_overlap >= T_oh.
Full derivation (App. A):
- T_base = T_dec + T_tool
- T_hit = T_base - t_overlap
- T_miss = T*_base + T_oh, with T*_base = T_base - T_D3
- E[T] = alpha*T_hit + (1-alpha)*T_miss
- S = T_base / (T_base - alpha*t_overlap + (1-alpha)*(T*_base - T_base + T_oh))
- Break-even: alpha*t_overlap >= (1-alpha)(T*_base - T_base + T_oh); without D3 this reduces to alpha*t_overlap >= (1-alpha)*T_oh.
- Ceiling: S_max = (T_dec + T_tool)/T_dec = 1/(1 - f_tool), with f_tool = T_tool/T_base.
Eq. 2 (gate confidence): c = min over i=2..L of exp(l_i).
Symbols: alpha = fraction of tool-call turns accepted; t_overlap = mean realised overlap per accepted turn; T_oh = per-turn overhead from probes and wasted executions.

## 13. AOSpec (action and observation co-speculation)

**read:** arXiv:2608.00881v1 (1 Aug 2026; the only version). Full PDF read (8 pp.): https://arxiv.org/pdf/2608.00881v1. Equations taken from https://arxiv.org/html/2608.00881v1.

**verdict:** corrected

**effect:**

The numbers are right, but the recorded conditions are incomplete or misleading. Paraphrased; figures exact.
(1) -11.8% to -32.5% (Abstract; §1; §5.2). This is the MEAN latency saving over nine equally weighted (harness, actor) configurations. The range runs over SIMULATED actor decode speed, not over harnesses or models: 11.8% at 20 ms/token TPOT and 32.5% at 1 ms/token. The strongest baseline gets 4.3% and 12.2% at the same two speeds.
Measurement is trace replay (§5.1): every method is replayed on identical recorded actor trajectories. Actor latency is computed as recorded output-token counts x a swept TPOT of {20, 15, 10, 5, 1} ms. Tools run on an Azure Standard_D4s_v5 VM (4 vCPU, 16 GiB); the drafters run on 2x H200 under vLLM.
Benchmark: Terminal-Bench 2.0, split into disjoint train and test task sets; the number of test tasks is NOT stated.
There are 4 harnesses and 5 actors but only 9 pairs, not 20 (Fig. 4): mini-swe-agent x {Sonnet 4.5, Gemini 2.5 Pro, GPT-5 mini}; OpenHands x {the same three}; Gemini CLI x Gemini 2.5 Pro; Judy x {Opus 4.6, Gemini 3.1 Pro}.
Defaults: 5 observation branches and 8 action forks; observation drafter Qwen3-0.6B fine-tuned per harness; action drafter Qwen3.6-35B-A3B-FP8 with no training.
(2) p99 -42.8% holds at 10 ms TPOT only (Table 1, trial-level latency: 7780 -> 4449 s). Same row: p50 -10.7%, p90 -10.5%, p95 -30.3%.
(3) Exact hit 33.3% and 27.1% of tool time hidden: Table 2, the observation-model input ablation on mini-swe-agent x Sonnet 4.5 with full context. The caption states no TPOT or candidate width.
Related figures: fine-tuning raises the 0.6B observation model's top-1 accuracy from 2.4% to 29.1% (Fig. 7b). At 10 ms, observation speculation alone saves 12.0%, action speculation alone 7.1%, both together 17.0% (§5.5). Transfer to SWE-bench Verified saves 18.9% vs 4.2% for the best baseline at 1 ms TPOT (§5.3).
(4) Extra compute: not reported anywhere in v1 (no tokens, GPU-hours or dollars). Confirmed.
(5) Non-filesystem inputs and effects are excluded (§4.3). Confirmed.
(6) Task success is not measured: the method is lossless by construction, and trace replay forces the same trajectory.
Proposed D-entry: the E123 and §3.3 row gives the range without 'trace replay, simulated TPOT 20 -> 1 ms', and gives the p99 figure without '10 ms TPOT'.

**mechanism and term:**

The recorded mechanism is correct but incomplete: there are two levels of speculation.
(a) Observation speculation (EVD). While a tool call runs, a small drafter proposes candidate observations ranked by probability x estimated tool time. Each draft that finishes starts a provisional actor continuation. A continuation is kept only if its drafted observation is byte-identical to the real one.
Term: overlap saving. The NEXT pass's model call (prefill and decode) runs during this pass's environment wait.
(b) Action speculation. Latency-critical target actions are launched early, possibly several steps ahead, in copy-on-write filesystem forks. JASV reuses a fork only if its action equals the emitted action AND the fork's origin environment version equals the committed version.
Term: overlap saving. The environment act and wait of a later pass runs alongside earlier passes' decode and tool time (runway R_{j,i}). Environment time is hidden, not made smaller.
Terms it makes worse (the paper does not quantify them):
- More model calls per pass: drafter calls, plus up to 5 speculative actor continuations. Those are extra actor tokens, which would be billed if the actor were an API model.
- More environment machine time: up to 8 forks.
Success rate is unchanged by construction (lossless) and not measured. N and context growth are unchanged.
Scope: effects that cannot be isolated are ineligible. The CoW runtime is taken from concurrent work under anonymous review.

**authors and venue:**

Confirmed. Authors: Hao (Mark) Chen, Jinnan Guo, Wayne Luk, Hongxiang Fan, all Imperial College London, UK. arXiv cs.LG, v1 1 Aug 2026, the only version, no arXiv comment. The PDF (8 pp., AAAI-style author-year references) states no venue, so this is a preprint. Credibility rule: authors and institutions pass; the benchmarks are public (Terminal-Bench 2.0, SWE-bench Verified) and the models are named, but the test-task count is not stated, so clause (iii) is only partly met.

**formula:**

§3 serial latency: sum over i of (D_i + T_i), where D_i is actor generation time and T_i is tool time at step i. An action speculated when its issuing decode starts can hide at most min(D_i, T_i).
Eq. 1: L_obs(theta) = - sum over (H_t, a_t, o_t) in D of log p_theta(o | H_t, a_t).
Eq. 2: T_hat(c) = sum_j K(c, o_j) T_j / sum_j K(c, o_j).
Eq. 3: V_o(c) = p_theta(c | H_t, a_t) * T_hat(c). This is the proxy for expected tool time hidden.
Eq. 4: ValidAct(f, a_i, S_i) = [a_hat_f = a_i] AND [nu(S_f) = nu(S_i)].
Eq. 5: runway R_{j,i} = sum_{k=j..i} D_k + sum_{k=j..i-1} T_k. An action issued at step i and launched at boundary j hides up to min(T_i, R_{j,i}).

## 14. TClone

**read:** arXiv:2605.17320v1 (17 May 2026; the only version). Full PDF read (14 pp.): https://arxiv.org/pdf/2605.17320v1.

**verdict:** corrected

**effect:**

The recorded numbers are in the paper, but the headline factor is an 'up to' figure that matches a single task. Paraphrased; figures exact.
(1) 1.9x / 1.5x lower total task latency vs KVM / CRIU.
- The abstract gives it unqualified, for 'our end-to-end agent-loop measurement'. §1 attributes it to CUA tasks with GPT-5.5 model calls.
- §5.2 says 'up to' 1.9x vs KVM and 1.5x vs CRIU, in the Agent S3 on OSWorld setup, where gains were largest and the biggest improvements were on short tasks.
- §2.3 and Fig. 2 give the same factors from the latency breakdown of Agent S3 running ONE OSWorld task, all model calls GPT-5.5. Full execution took 1002 s (KVM), 777 s (CRIU) and 531 s (TClone); calc. 1.89x and 1.46x.
- No mean or median over tasks is given as a number; Fig. 7 is only a CDF.
- Hardware: desktop Intel Core i5-13400, 32 GB DDR4.
- Setups: AgentLoop on GTA (the paper calls GTA's 229 items 'tools'; GTA1 test-time-scaling setup) and Agent S3 on OSWorld (369 tasks). The intro says '>600 tasks' in total. Neither the number of tasks run per system nor the number of forks per task in the end-to-end runs is stated.
(2) Fork up to 4.9x / 3.4x faster (§1, §2.3). This is container clone time at one branch point (Fig. 2a): 18.2 s KVM, 12.8 s CRIU, 3.7 s TClone (calc. 4.9x and 3.5x).
(3) 16 concurrent clones (§5.3.1). Latency: CRIU over 50 s vs TClone about 10 s, roughly a 5x gap (Fig. 9). Memory: about 9 GB vs about 14 GB (Fig. 10). The workspace used for Figs. 9-10 is not stated; the ablation (Fig. 11) uses a Chromium workspace with 168 processes.
(4) No speculation hit rate and no task-success metric reported. Confirmed.
Proposed D-entry: change E121 to 'up to 1.9x / 1.5x (Agent S3 on OSWorld, GPT-5.5; same factors as the one-task breakdown in Fig. 2b)'. The recorded '598+ tasks' is calc. (229 + 369); the paper itself says '>600' and calls the 229 GTA items tools.

**mechanism and term:**

The recorded mechanism is correct.
How it works:
- It freezes the source container briefly (metadata only) and rebuilds the process tree in a sibling container with fresh namespaces.
- Anonymous memory is shared copy-on-write through a kernel module.
- A lazy CoW page cache sits over block-CoW filesystem layers.
- The Wayland compositor runs inside the container.
- Durable checkpointing is asynchronous and off the critical path.
- Network: loopback connections are re-established with TCP repair. External connections are CLOSED at fork, and each branch reconnects on its own. External side effects are not committed, merged or rolled back; they are a policy boundary.
TERM MAPPING:
- Environment: the clone time at each branch point, part of per-pass environment time when an agent branches, becomes smaller (18.2 s / 12.8 s -> 3.7 s).
- Environment machine memory per concurrent clone is smaller (about 9 vs 14 GB at 16 clones).
- It creates no overlap itself. It lowers the cost of branching, so it is an enabler for speculation and tree search, which are what change overlap or success rate.
- The end-to-end speedup is only relative to agents that already clone on the critical path.
- Success rate is not measured.

**authors and venue:**

Confirmed. Authors: Yutong Huang, Vikranth Srivatsa, Alex Asch, Hansin Tushar Patwa (UC San Diego) and Yiying Zhang (UC San Diego and GenseeAI). arXiv cs.OS, v1 17 May 2026, the only version. No venue; the paper says the code will be released upon acceptance. So this is a preprint. Credibility: authors and institutions pass; OSWorld and GTA are public and GPT-5.5 is named. But no per-run task count and no quality metric are given.

**formula:**

None.

## 15. DeltaBox

**read:** arXiv:2605.22781v2 (8 Jun 2026). PDF https://arxiv.org/pdf/2605.22781v2: body pp. 1-12 read in full. Also read the v1 PDF (21 May 2026) for comparison. Also checked the abs page https://arxiv.org/abs/2605.22781v2.

**verdict:** corrected

**effect:**

Paraphrased; figures exact.
(1) Checkpoint ~10.83 ms and rollback ~1.86 ms (v2 Abstract; §1; Table 2 weighted average of per-event mean blocking time; Table 4).
- Workload: SWE-bench Verified MCTS trajectories from Qwen3-Coder-30B, four archetypes contributing 4/4/10/6 trajectories, each replayed twice.
- Sandbox: Firecracker microVM with 4 vCPU and 8 GB.
- The checkpoint figure is the API call-to-return blocking time, excluding the asynchronous CRIU dump. It overlaps the LLM call, so the agent sees 0 blocking.
- 1.86 ms is the fast path (template hit). The slow path, used after template eviction, takes 9.29 ms.
- Baseline restore times per event: E2B (diff) 899.7 ms, CRIU+cp 811.4 ms, FC-Diff+dm 3429 ms, replay+cp 27694 ms.
(2) 64-way fork p50 5.47 ms / p99 14.74 ms / 165.9 forks/s (Table 3). This is the RAW kernel fork() on one host, with no VM, overlayfs or CRIU. Values are per-trajectory medians over 18 SWE-bench MCTS trajectories (Qwen3-Coder-30B and MiMo V2.5-Pro, from Django, SymPy and Xarray, 5 reps each). At the sandbox level (Fig. 7a) the paper only says DeltaBox is an order of magnitude or more faster than CubeSandbox and E2B.
(3) Slowdown 1.01-1.02x vs 1.30-1.93x (§6.2.1, Fig. 6). This is SWE-bench MCTS ONLY, not RL fan-out: 30-iteration MCTS trajectories (Qwen3-Coder-30B) replayed across the four archetype groups, each system normalised to its own LLM+action time. The E2B baseline is self-hosted e2b-infra with incremental snapshots. Same passage: state management takes 23-48% of total time on E2B (diff) vs 1-2% on DeltaBox.
The RL fan-out result is a different metric: expected synchronous GPU occupation of 95-97% (DeltaBox), 77-80% (CubeSandbox) and 29-36% (E2B) at N in {16, 64} for Qwen2.5-7B. The paper computes this from Figs. 7a-b (§6.2.2).
(4) No agent success metric: confirmed. The pass rates in Fig. 1 are cited from other papers as motivation.
(5) No network I/O rollback: confirmed (§4.2.3).
(6) v1 vs v2 (both now read):
- v1 Table 1: checkpoint 14.57 ms; fast-path restore 5.14 ms; slow path 8.04 ms.
- v1 Fig. 7: 100-iteration MCTS on five SWE-bench Verified instances; DeltaBox 1.03-1.06x vs FC-Diff+dm 1.87-3.84x and CHV+dm 2.62-4.29x; state management 47-77% vs 3-6%.
- v2 changes the baselines, the workload and the figures.
NEW DISCREPANCY: the abstract on the arXiv v2 abs page still says 14 ms and 5 ms, but the v2 PDF abstract says ~10.83 ms and ~1.86 ms. Anyone citing the abs page gets the v1 figures.
Proposed D-entry: record the abs-page vs PDF mismatch; restrict E122's slowdown figure to MCTS; label the 64-way fork figure 'raw kernel fork()'. Reading both versions also clears D140's 'not re-verified'.

**mechanism and term:**

The recorded mechanism is correct.
How it works:
- DeltaFS: an ioctl on overlayfs freezes the writable upper layer into a read-only lower and inserts a fresh upper, without unmounting. So a checkpoint is a layer insert and a rollback is a layer switch. It runs over XFS reflink for 4 KB copy-on-write.
- DeltaCR: every checkpoint runs an asynchronous CRIU dump plus a fork() that leaves a frozen template. Restore forks the template (fast path) or falls back to CRIU lazy-pages.
- A Network Proxy Daemon owns the LLM SDK connections so that templates stay safe to fork.
TERM MAPPING:
- Environment: checkpoint/restore (state-management) time per pass becomes smaller.
- Overlap: checkpoint work runs during the model call (inference-masked), so only the millisecond restore stays on the critical path.
- In RL training, smaller fan-out latency means less idle GPU time. That is an environment-machine / GPU-hour cost effect.
- It enables tree search and speculation by making branching and rollback cheap. It does not speed up a linear agent.
- Success rate is not measured.
- Memory: the template pool is bounded, and reachability-aware GC cuts dump storage by 46-63% (§6.3.4).

**authors and venue:**

Confirmed. Authors: Yunpeng Dong, Jingkai He, Shiqi Liu, Yuze Hou, Dong Du (corresponding), Zhonghu Xu, Si Yu, Baochuan Yang, Yubin Xia, Haibo Chen. Institutions: IPADS, Shanghai Jiao Tong University; Engineering Research Center for Domain-specific Operating Systems, Ministry of Education, China; Huawei Technologies. arXiv cs.OS, v1 21 May 2026 and v2 8 Jun 2026. v2 states no venue, so this is a preprint. Cite v2 and give the version with every number.

**formula:**

No speedup formula. Fig. 7(c) caption: expected sync GPU occupation = (T_gen + T_train) / (sandbox + T_gen + T_train). §6.2.2: a synchronous training step takes sandbox + T_gen + T_train. The Fig. 6 metric is end-to-end time divided by LLM+action latency (1.0x = LLM round-trip time + action work).

## 16. Atomix (safety enabler, not a speed-up)

**read:** arXiv:2602.14849v2 (29 May 2026). PDF https://arxiv.org/pdf/2602.14849v2: read §1-§4, App. B.1-B.4, C.1 and C.5, and Tables 1-3, 5, 6 and 17. Checked the Table 3 cells in https://arxiv.org/html/2602.14849v2. Searched the v1 PDF (16 Feb 2026) for comparison.

**verdict:** corrected

**effect:**

Paraphrased; figures exact.
(1) Leaks (Table 2, §3.4). Tx-Full 0/500 (95% CI [0, 0.74]); Saga-Compensation 400/500 (80%); Checkpoint-Replay 200/500 (40%); TCC-Confirm 0/500; Mutex+WAL+Rollback 0/500; No-Tx 500/500; Atomix with misclassified irreversible effects 300/500 (60%).
Conditions: a mixed reversible/irreversible workflow writing to a real append-only SMTP/webhook sink. 5 abort sources (tool failure, losing speculation, stale read, pre-commit veto, timeout) x 100 trials. Every baseline delivered all 500 paired valid sends.
TCC and Mutex+WAL+Rollback reach 0 only because they are fully wired for the email tool: 50 and 30 LOC per tool, vs 17 LOC per Atomix adapter.
Verdict: confirmed.
(2) Clean task success at fp=0.30 (§3.2, Fig. 2, Table 6).
Conditions: tau-bench retail, GPT-4.1, max 30 steps, N=30 tasks per cell (the first 30 of 38 retail tasks). fp is a per-call Bernoulli fault probability over five fault classes; the authors call it a stress knob, not a production rate.
Results: Tx-Full 57% [37, 75]; TCC 3%; Saga 7%; Mutex+WAL+Rollback 3%; No-Frontier 3%; No-Tx 0%; OCC 7%.
CORRECTION: Checkpoint-Replay reaches 53% (16/30 vs 17/30, Fisher p=1.0), which is statistically tied with Atomix. On the full pool (N=114, fp=0.10) it is 58.8% vs 53.5%, p~0.50 (App. C.1). The abstract itself says every NON-Checkpoint-Replay baseline falls to 0-7%. So the §3.3 row's '57% vs 0-7% for baselines' overstates the result.
E114 said App. C.1 was not extracted; it now is (Table 5). WebArena (GPT-5, 10 tasks): Tx-Full 73.0 / 57.2 vs Checkpoint-Replay 68.0 / 53.2 at fp 0.10 / 0.30. OSWorld (Claude Sonnet 4, 7 tasks): 63.0 / 37.0 vs 62.0 / 37.1.
(3) Overhead (App. C.5).
- Tx-Full adds 7.7 us per step vs 0.8 us for No-Tx, under 0.01% of typical tool latency (50 ms-10 s).
- On real tau-bench with no faults: 163.9 s (Tx-Full) vs 171.2 s (No-Tx).
- Speculation commit costs about 1 ms at K=16 branches (Table 17: 1025 us mean, p99 23198 us from GC pauses).
- CORRECTION to E116's '10.1 ms'. In the combined-stress test (Table 3, mixed faults, fp=0.10), Tx-Full waits 0.1 ms vs 95.9 ms for Mutex-Workflow, and the §3.5 text says Tx-Full reports 0 ms wait. The HTML cell carries a '1' marker right before '0.1', which is likely where 10.1 came from.
(4) v1 differs substantially (for example, v1 reports 37-57% task success vs 0-7%). Always cite v2.

**mechanism and term:**

The recorded mechanism is correct.
How it works:
- Adapters record read and effect scopes for each transaction, and the orchestrator seals the transaction.
- Commit happens only after per-resource frontiers certify that no earlier conflicting work can still arrive.
- At commit: bufferable (staged) effects are released, irreversible effects leave the gate, and reversible effects that were already externalised are accepted as final.
- At abort: unreleased effects are suppressed and externalised reversible effects are compensated where possible.
- Each speculative branch is its own transaction; the winner commits and the losers abort.
TERM MAPPING:
- No time term is reduced. It costs microseconds per step, and about 1 ms per commit at K=16.
- It changes the success-rate term under injected faults (clean task success).
- It is a safety enabler that makes speculation (the overlap term) admissible for side-effecting tools. That holds only if the adapter metadata is right: a misclassified effect class leaks 60%, too-narrow scopes give 66/200 invariant violations, and calls that bypass the adapters are outside the boundary.
Part 2 should classify it as a success-rate / safety enabler, not as an acceleration.

**authors and venue:**

Confirmed. Authors: Bardia Mohammadi (MPI-SWS), Nearchos Potamitis (Aarhus University), Lars Klein (EPFL), Akhil Arora (Aarhus), Laurent Bindschaedler (MPI-SWS). arXiv v1 16 Feb 2026 and v2 29 May 2026 (cs.LG). The v2 PDF is marked 'Preprint.', so this is a preprint. Code: github.com/mpi-dsg/atomix. Credibility: tau-bench retail (N=30 per cell, GPT-4.1) passes. The WebArena and OSWorld rows rest on only 10 and 7 tasks.

**formula:**

None for speed or cost in the sections read (§1-§4, App. C.1, C.5). The settlement rule is stated in prose: seal, plus a per-resource frontier predicate, plus effect-class commit.

## 17. AAPT (pre-compiled policy trees)

**read:** arXiv:2607.28399v1 (30 Jul 2026; the only version). PDF https://arxiv.org/pdf/2607.28399v1: read the body §1-§7 plus App. 18.3 and 19. Equations taken from https://arxiv.org/html/2607.28399v1.

**verdict:** corrected

**effect:**

Paraphrased; figures exact.
(1) Headline (Abstract; §5.1 'Declared-primary confirmation'). AAPT (condition T2) succeeded on 33/42 trials (0.79) vs the reactive baseline R0 on 21/42 (0.50); exact two-sided McNemar p = 1.8x10^-3.
- Window: 650 ms, declared primary before data collection, fresh seeds.
- Model: frozen Holo-3.1-35B-A3B as both planner and observer.
- Benchmark: key_prompt, the authors' OWN timed GUI benchmark. A transient prompt appears after a fixed 750 ms delay and asks for one of three keys; scoring is deterministic and server-side.
- 42 per-seed paired trials; 0 incorrect actions; tree validity 1.0; observer branch accuracy 0.86-0.93.
- The pre-registered primary was 700 ms, where R0 was near ceiling and not significant (p=0.25); the paper reports this as a deviation.
- The metric is success before the deadline, not latency.
- Self-hosted on 1-2 RTX 6000 Ada GPUs (vLLM with guided JSON).
(2) Replications (§5.3).
- Qwen3.6-35B-A3B, an untuned generalist, at a declared 600 ms primary: 126 pooled pairs, 0.778 vs 0.341, 60/5 discordant pairs, p = 4.9x10^-13.
- Holo on fresh seeds at 550 ms: 84 pairs, 0.619 vs 0.143, p = 1.8x10^-12.
(3) DynaCU (§5.5): 39 deterministic, deadline-focused DynaCU-Bench tasks, majority of 3 runs. Reactive 7/39 vs AAPT 6/39, 5/4 discordant, p = 1.0. So the tie has AAPT ONE TASK LOWER. AAPT wins only on deadlines whose responses can be listed in advance: it fires 140-215 ms after the gated frame vs a reactive round trip of about 437 ms.
(4) CORRECTION to 'no hit rate'. There is no speculation acceptance rate, but the paper does report:
- observer branch-routing accuracy: 0.86-0.93 (Holo), 0.969 (Qwen3.6), 0.39 (UI-Venus) (Table 2);
- planner outcome recall: 0.59 vs 0.22 (UI-Venus, §5.4);
- 1.27 trees compiled per successful trigger (App. 18.3).
(5) MISSING COST (§5.1, App. 18.3).
- AAPT generates 3.2x the reactive baseline's completion tokens per trial: 342.8 vs 105.8.
- Tree compilation: 283.5 tokens, p50 1.81 s.
- Observer call: 59.3 tokens vs 105.8 for the reactive baseline's decisive call.
- Critical path per decision (§5.2): AAPT observer 273 ms / 30 tokens vs reactive 411 ms / 48 tokens; open-loop 459 ms / 60; predict-and-replan 484 ms / 66.
(6) Scope (Limitations): the positive result is confined to two Qwen3.5-MoE-class checkpoints and one scenario family.

**mechanism and term:**

The recorded mechanism is correct; additions below.
How it works:
- During quiet screen time, the same frozen model compiles a bounded, flat policy tree: observable guards, pre-authorised actions, per-branch deadlines and confidences. The tree is sized so that T_cover >= L_p95 + M.
- At event time, a 30 FPS pixel-difference change gate and a single low-token observer call route the frame to a branch.
- The branch fires only if its id is eligible, its stored confidence clears tau_m, and the decision is within its deadline. Otherwise it is suppressed and the agent replans.
- Nothing executes speculatively.
TERM MAPPING:
- The planning model call's decode moves off the decision-time critical path into the environment's idle/wait time: an overlap saving with idle time.
- The model call left on the critical path becomes a short observer decode: 30 vs 48 tokens, 273 vs 411 ms.
- The MEASURED effect is on the success-rate term under a deadline, not on task time.
- The money term goes UP: 3.2x completion (output) tokens per trial.
- Model calls: one tree compilation plus observer call(s), vs R0's two calls (a WAIT, then the decisive action).
- It applies only when the candidate actions can be listed in advance.

**authors and venue:**

Confirmed. Authors: Zihan Dong (Georgia Institute of Technology), Rui Qian (Fudan University), Qishi Zhan (Marquette University), Dongshen Peng (UNC Chapel Hill), Kaixin Li (National University of Singapore), Yu Li (Southeast University, Nanjing). arXiv cs.LG, v1 30 Jul 2026, the only version, no arXiv comment. Page 1 carries the AAAI template line '(c) 2027 AAAI', and the appendix mentions a 'Round-1 revision cycle', but there is no acceptance statement. So this is a preprint. The headline rests on the authors' own key_prompt benchmark, and the paper states no code or benchmark release, so clause (iii) of the credibility rule fails for the headline. The external DynaCU result (39 tasks) is a tie. Keep 'qualitative use only'.

**formula:**

Eq. 1: T_cover >= L_p95 + M. L_p95 is the 95th-percentile end-to-end planner latency; M is a 500 ms safety margin. The measured crossover lies around L_p95 + M ~ 2.4 s.
Horizon: n ~ ceil(T_cover / E[dt]).
Eq. 2 (branching factor):
- K_v = 1 if confidence >= tau_c and risk <= tau_r;
- K_v = min(K_max, m_v) if the outcome is uncertain;
- K_v = 0 if a safe fallback or replan is required.
Eq. 3: m_v = min{K : sum over i=1..K of P(s_{v,i}) >= rho}.
Success = correct action AND action before deadline. §6 factorises it: the success event is contained in {valid tree} ∩ {true outcome covered} ∩ {correct route} ∩ {route before deadline}.

## 18. Agent JIT Compilation (JIT-Planner / JIT-Scheduler)

**read:** https://arxiv.org/pdf/2605.21470v2 (v2, 29 May 2026, the latest version; the dossier cites v1). I also compared v1 (20 May 2026): the headline numbers are the same. The ICML 2026 listing was checked at icml.cc/static/virtual/data/icml-2026-orals-posters.json (poster id 66062).

**verdict:** corrected

**effect:**

Table 1 (p.5), GPT-4.1 row: Browser-Use 150.1 s, 61%. Browser-Use +cache 105.2 s, 88%. JIT-Planner 15.4 s, printed as (9.7x) in the table, range 93.7 s, 90% (+29%). The 9.7x is therefore the paper's own table figure, not calc. Other model rows: Gemini-2.5-Flash 100.3 -> 7.2 s (14.0x), 59 -> 94%; Gemini-2.5-Pro 115.9 -> 12.6 s (9.2x), 77 -> 97%. The per-application rows are averaged over the three models, not GPT-4.1 alone: Dashdish 8.2x, GitLab 14.6x, Gomail 12.9x, Omnizon 7.4x, Reddit 18.9x. The 10.4x headline (abstract; section 5.1 RQ3, p.7) is also an average over the three models: JIT-Planner 11.7 s vs Browser-Use 122.1 s, and 6.8x vs Browser-Use +cache 80.1 s. On the same page, LLM calls are 73% of Browser-Use latency (Fig. 6 breakdown). Table 6 (p.12) gives 10.4x with 95% CI [9.0, 12.8] and +28 pp accuracy with CI [+19, +34], over 111 task-model configurations. Conditions: 37 tasks in 5 apps. The three REAL apps (Dashdish, Gomail, Omnizon) have 9 tasks each: 3 taken from the benchmark and 6 written by the authors, so 18 of the 37 tasks are author-curated (App. D, p.13). The two WebArena apps (GitLab, Reddit) have 5 randomly chosen tasks each and are run with the planner only. Each task is run 3 times. Latency is wall-clock from task submission to completion, including planning (App. H, p.17). The baseline is Browser-Use v0.7.10 with the same models, on an AWS m8i.xlarge (4 vCPU). Offline set-up is excluded: 25-90 min of tool synthesis plus 25-45 min of trace collection per app (section 6, p.9), with GPT-4.1 used for all offline stages. JIT-Scheduler (section 5.2 RQ3, p.9; Table 7, p.12) was run on the 27 REAL tasks with a 4-vCPU budget. The 2.4x [1.8, 3.1] compares Gemini-2.5-Pro JIT-Scheduler (109.9 s, 86.4%) with OpenAI CUA (computer-use-preview-2025-03-11: 258.7 s, 77.8%), so the models differ. The same comparison gives 1.8x with GPT-4.1 and 2.2x with Gemini-2.5-Flash. Against Anthropic CUA (Claude Sonnet 4: 141.7 s, 79.0%) the speed-up is only 1.3x. The '+9' is 8.6 pp (calc.). Internal inconsistencies: the App. B Table 2 Overall row gives Browser-Use 118.5 s and JIT-Planner 10.9 s, not 122.1 / 11.7 s; the Table 4 Omnizon CUA values (190.2 / 113.9) do not match Table 2 (325.9 / 190.2). The paper reports no token counts or dollar costs anywhere.

**mechanism and term:**

The mechanism needs a correction: the Monte Carlo step belongs to JIT-Scheduler, not to plan selection. JIT-Planner samples code plans in parallel until k=32 valid candidates exist (with early acceptance). Each plan is checked statically against the tools' pre/postconditions on a control-flow graph, and the plan with the lowest CFG cost estimate is chosen. That estimate is a weighted count, not Monte Carlo. JIT-Scheduler is a separate component. It picks Serial, Parallel (task parallelism over n workers) or Hedge (n=4 copies of the full serial plan, first to finish wins) by Monte Carlo sampling from learned latency distributions for each DOM element. The 10.4x headline is JIT-Planner alone, without the scheduler. Terms: (1) N and c_k, structure change: confirmed, since per-step LLM decisions are replaced by one planning phase plus code execution. But c_k is not 1: planning makes many concurrent LLM calls, and plans keep ai_eval LLM calls where runtime judgement is needed. This is why Omnizon has the lowest speed-up (7.4x). (2) Environment: confirmed. The Browser-Use +cache ablation isolates the cached tools (122.1 -> 80.1 s, 1.5x); the remaining 6.8x is credited to planning. (3) Overlap saving: comes from the scheduler's Parallel and Hedge strategies and from parallel plan generation, but the scheduler results (2.4x) are separate from the 10.4x. (4) Environment machine hours: Hedge runs up to 4 isolated browser contexts on one 4-vCPU machine. Machine hours, tokens and dollars are not reported, so 'raises machine hours' is our inference and must be labelled as such; the money term cannot be placed by measurement. (5) Success rate up: confirmed (61 -> 90% with GPT-4.1). The pre/postcondition protocol raises the valid-plan rate from 77.1% to 90.6% (App. C.3).

**authors and venue:**

Caleb Winston, Ron Yifeng Wang, Azalia Mirhoseini and Christos Kozyrakis, all at Stanford University (PDF p.1). The arXiv comment says 'Accepted at ICML 2026'. The PDF footer reads Proceedings of the 43rd ICML, Seoul, PMLR 306, 2026. The icml.cc 2026 data lists it as a Poster (id 66062) and gives the last author as 'Christoforos Kozyrakis'. It passes as a conference paper. The dossier's E18/E100 label 'primary preprint' should become 'conference paper (ICML 2026 poster)', and the dossier cites v1 while the latest version is v2 (numbers unchanged).

**formula:**

Algorithm 1 (p.4): for each tool call at CFG depth d, cost += C_tool·γ^d; for each ai_eval call, cost += C_eval·γ^d; the plan returned is the argmin over valid plans. App. H sets C_tool=0.1, C_eval=10.0, γ=10. Algorithm 2 (p.4): S(U) = Σ_{e∈U} Σ_{i=1}^{count(e)} sample(D_e). Serial: ℓ = S(U_σ). Hedge: ℓ = min_{w=1..n} S(U_σ) + δ_h. Parallel: ℓ = S(U_σ^seq) + max_{w=1..n} S_w(U_{σ,w}) + δ_p. The strategy is argmin_σ of the mean L̄_σ over N_MC=1000 trials, with δ_p = 20-30 s, δ_h = 5-15 s and n=4. App. G adds (1 + num navigations)·C_read (5-10 s) and a fixed C_repeat (5-7 s) for repeated interactions. App. H says the cost model is used only to rank plans, with three tiers: cached tool about 0.5-2 s, ai_eval about 5-15 s, agentic sub-loop about 30-60 s or more. The Hedge and Parallel expressions are the paper's own overlap terms.

## 19. EchoPath

**read:** https://arxiv.org/pdf/2609.16635v1 (v1, 15 Sep 2026, the only version). The code link https://github.com/JackZhao1998/EchoPath still returned HTTP 404 on 2026-09-28; the user page returns 200.

**verdict:** confirmed

**effect:**

Table 1 (p.8), second-pass replay results. codex-gpt-5.5-medium: 91.2%, execution tokens 20,370 [674-245,736], second-pass time 127.5 s [14.5-529.3]. claude-sonnet-5-medium: 92.8%, 30,503 tokens, 139.3 s. kimi-K3-medium: 87.3%, 19,928 tokens, 130.5 s. Synapse (codex-gpt-5.5-medium): 91.8%, 586,386 [164,997-1,625,940] tokens, 315.7 s [110.1-1,272.5]. Text on p.8: with Codex the expected memory was recalled for all 159 tasks, and 145/159 were completed. The text says the values are medians; the Table 1 caption does not define the bracketed intervals (Fig. 3 uses 0.025-0.975 quantiles). The abstract claims median tokens down by more than 90% and median time down by about 60% without naming the baseline; against Synapse this is -96.5% tokens and -59.6% time (calc.). Conditions: OSWorld-Verified, paired two-pass design. The pool is 159 active executable memories after the first pass; how many tasks the first pass attempted, and its success rate, are not reported. First pass: median about 572k tokens and about 4.5 min per task; consolidation removed about 30% of exploration steps (p.8). The second pass changes the resolution from 1920x1080 to 1600x900 (p.7). Synapse, a trajectory-as-exemplar planning baseline, was run only with the Codex host, and the authors call it a naive comparison. Workers are AWS t3.large (2 vCPU) (Supp. C). There is no live drift experiment; the Discussion (p.11) says robustness to broad interface drift is not yet established. E92: the start-state gate rejects 39/50 incompatible starts (78%), so 22% are falsely accepted (calc.); it accepts 98% of compatible and 92% of partially changed starts (Table 3, p.10).

**mechanism and term:**

The mechanism is correct. Validated trajectories become callable memories m = (K, u, Π, A, E, B, v, r, ℓ). Replay binds each stored action through ρ, with image-based target re-aiming (IBTR). A local failure triggers a bounded LLM grounding repair; a structural failure falls back to fresh planning. The lifecycle operations (promotion, branching, repair, merge, deprecation, quarantine) are described but not evaluated; only retrieval, IBTR, the gate, flexible rebinding and storage are tested, and those offline. Terms: c_k -> 0 for directly replayed steps is right, because both the planning F_θ and the grounding G_φ are skipped. But the task still uses tokens: a median of 20k remains (host agent, flexible-input reasoning, repairs and fallbacks; the split is not reported, E132). Prefill and decode tokens fall: confirmed. Context growth: removed for replayed steps, since they make no model calls. Environment: unchanged. GUI actions and waits still run, with a median of 127.5 s, so time falls much less than tokens (-60% vs -96%, calc.). Success rate: about unchanged vs Synapse. Guard: the start-state gate. For cost per success, the first-pass construction cost (about 572k tokens and 4.5 min per task) is a set-up cost to amortize; it is not in the second-pass figures.

**authors and venue:**

Yao Zhao (JHU Applied Mathematics and Statistics); Aditya Shanmugham and Swastik Roy (Amazon AGI); Yanxun Xu (JHU AMS and JHU School of Medicine, Oncology). No venue and no arXiv comment. It passes source-credibility conditions (i)-(iv): OSWorld-Verified, a 159-task pool, and the models are named.

**formula:**

No speed-up or cost formula. The formalism (sections 2.1-2.2, pp.3-6) defines the fresh loop as o_t = O(x_t), p_t = F_θ(q, h_{t−1}, o_t), â_t = G_φ(p_t, o_t), (x_{t+1}, z_t) = W(x_t, â_t). Replay replaces planning and grounding with the binding ρ(a_t, o'_t, e_t, Π_{m*}, B_{m*}, ξ') ∈ {(ã_t, κ_t, δ_t), reject}. The repair is â_t^gnd = ψ_ground(a_t, e_t, o'_t, Π_{m*}, ξ') and the fallback is π_plan = F_θ(q', h'_t, o'_t, χ_{m*}).

## 20. GPA (GUI Process Automation from demonstrations)

**read:** https://arxiv.org/pdf/2604.01676v2 (v2, 4 Apr 2026, the latest version). Compared with v1 (2 Apr 2026): the first-page differences are only the date and reference numbering; Table 2 is the same.

**verdict:** confirmed

**effect:**

Table 2 (p.7), pilot results. Simple tasks (average demo 10.80 steps): GPA 100%, 17.84 s; Gemini 3 pro 93.2%, 210.66 s. Hard tasks (27.27 steps): GPA 100%, 40.96 s; Gemini 87.64%, 383.24 s. Average (22.13 steps): GPA 100%, 33.74 s; Gemini 89.38%, 329.31 s. The paper says roughly 10x faster; 329.31/33.74 = 9.76x (calc.). Conditions (section 3, p.7): a small-scale pilot of 16 desktop GUI tasks. The task list gives 5 simple and 11 hard tasks, and the Average row matches that 5/11 weighting (calc.). The tasks include drafting an email, downloading a receipt, flight search and booking, Google Calendar, two Agentforce tasks, reimbursement submission with and without receipt retrieval, two SAP ERP form-filling tasks and two HR workflows. The baseline is the Gemini computer-use agent (gemini-3-pro), given the same demonstration video converted to text. Metrics are wall-clock runtime and success rate. The paper does not report runs per task, variance, or demonstration and build time. The tasks do not come from a public benchmark.

**mechanism and term:**

The mechanism is correct in essence. One demonstration is compiled into a workflow of UI-graph steps. At run time each target is located with local models (UI detector, OCR, IconCLIP) and Sequential Monte Carlo graph matching, with readiness (confidence) gating and bounded retries. No LLM or VLM is called at run time (Table 1, p.2: tiny local models only). Terms: (1) c_k (LLM calls) -> 0, a structure change: confirmed. (2) N is not reduced: the runner still steps through every demonstrated action, with a screenshot and a local parse per step. (3) Price/tier: everything runs locally, so there are no API tokens. (4) Overlap saving: missing from the record. The App. C precheck pipeline (p.17) processes step N+1 speculatively while the environment settles; its effect is not measured separately. (5) Success rate up: confirmed (100% vs 89.38%) in the pilot. Like RPA it follows a fixed plan, and deviations beyond the bounded retries fail explicitly.

**authors and venue:**

Zirui Zhao, Jun Hao Liew, Yan Yang, Wenzhuo Yang, Ziyang Luo, Doyen Sahoo, Silvio Savarese and Junnan Li, all at Salesforce AI Research (p.1). No venue. Conditions (i), (ii) and (iv) pass; (iii) FAILS. The numbers come from an author-built 16-task desktop pilot, not a public benchmark, even though the model is named. Under the references.md rule its numbers should go under 'Not used'; only a qualitative mention is allowed.

**formula:**

None for speed-up or cost. The only formal model is the SMC posterior over the target position, with likelihood p(Z|θ) from target and neighbour matches (section 2 and appendices), which is not a cost formula.

## 21. ActionEngine

**read:** https://arxiv.org/pdf/2602.20502v1 (v1, 24 Feb 2026, the only version).

**verdict:** confirmed

**effect:**

Table 1 (p.9), WebArena Reddit subset, 106 tasks, AOccam (GPT-4-Turbo) vs AEngine (Claude 4.5 [Sonnet]). Success 66 vs 95%. Average latency 237 vs 118 s (2.01x). Average cost per task $0.71 vs $0.06 (11.83x). Average input tokens 62.3k vs 8.1k (7.69x); output 3.0k vs 2.3k (1.30x). Average LLM calls 10.2 vs 1.8 (5.67x). Table 2, All(106) row (p.10): 0.66 / 0.95, 237.48 / 118.26 s, 62.26k / 8.14k input, 3.03k / 2.3k output, 10.16 / 1.76 calls. Cost (section 6.1, p.9) is total API cost per task, computed as input/output tokens × list price. The Table 1 caption gives Claude 4.5 Sonnet at $3/M input and $15/M output, and GPT-4-Turbo at $10/M and $30/M. So cost is an estimate, not a bill, and no cache price is applied even though the text mentions prompt caching. Latency is end-to-end execution time, including computation and API calls. The paper does not state runs per task, or whether AgentOccam was re-run or its numbers taken from its own paper. The cost and time of the offline, semi-automated crawl are not reported. calc.: pricing ActionEngine's tokens at GPT-4-Turbo rates (8.1k × $10/M + 2.3k × $30/M) gives about $0.15 per task. Token reduction alone is therefore about 4.7x; the rest of the 11.8x (about 2.5x) comes from the cheaper model's price.

**mechanism and term:**

The mechanism is correct. Offline, a semi-automated, MLLM-assisted Crawling Agent builds a state-machine graph: page states are nodes and validated operations are edges. At run time, the Execution Agent's LLM writes a sketch program in one call. A compiler grounds it by graph search into an execution plan run with Playwright. On failure, vision-based re-grounding repairs the step and updates the graph. Terms: (1) c_k and N: a structure change, since the per-step loop becomes one planning call plus small validation/repair calls (10.2 -> 1.8 calls). (2) Prefill: input tokens -87%, because the baseline's repeated context passing (context growth) is gone. (3) Decode: output tokens -23%. (4) Price/tier: this term ALSO changes (GPT-4-Turbo -> Claude Sonnet 4.5) and must be listed as a changed term and a confound; it accounts for about 2.5x of the 11.8x (calc.). (5) Money per task: smaller, but estimated from list prices. (6) Success rate: 66 -> 95%, confounded by the model change.

**authors and venue:**

Hongbin Zhong and Kexin Rong (Georgia Tech); Fazle Faisal, Luis França, Tanakorn Leesatapornwongsa, Adriana Szekeres and Suman Nath (Microsoft Research). No venue on the arXiv page or in the PDF. It passes conditions (i)-(iv): WebArena Reddit, 106 tasks, models named.

**formula:**

No explicit equation. The paper makes an asymptotic claim: the Fig. 1 caption (p.1) says the approach replaces O(N) visual inferences with a single O(1) planning phase, and section 6.2 (p.9) says reactive agents need O(N) LLM inferences for an N-step task. Cost is defined as token usage × model pricing (section 6.1).

## 22. SkillDroid

**read:** https://arxiv.org/pdf/2604.14872v1 (v1, 16 Apr 2026, the only version).

**verdict:** corrected

**effect:**

Table 3 (p.7), 150 rounds, gpt-4o-mini, SkillDroid vs baseline: success 128/150 (85.3%) vs 93/150 (62.0%); mean LLM calls per round 5.8 vs 11.3; mean latency per round 69.0 s vs 84.1 s; pure replay rounds with 0 LLM calls: 35 (23.3%). Table 2 (p.6), by execution path (n, success, mean LLM calls, mean latency): pure L2 replay 35, 100%, 0.0, 36.0 s. L2 + semantic match 32, 100%, 1.0, 54.7 s. L2 + step-level fallback 12, 100%, 5.0, 50.9 s. All L2 79, 100%, 1.2, 45.1 s. L2 -> L1 fallback 29, 75.9%, 10.1, 113.2 s. Fresh L1 42, 64.3%, 11.6, 84.0 s. All rounds 150, 85.3%, 5.8, 69.6 s. The section 5.1 text (p.6) gives 35.4 s for the 35 pure-replay rounds and calls it 2.4x the baseline's overall mean of 84.1 s. Conditions: 15 Android task types defined by the authors (Contacts, Clock, Chrome, Settings toggles, Keep Notes and others; App. A Table 8), run as 150 rounds in 5 phases with 4 instruction-variation levels and perturbations in phase 4. The setup is an Android emulator (Pixel 9a, API 35) on Windows 11, driven over ADB (about 100 ms per tap) with DroidRun v0.5, using gpt-4o-mini at T=0.2. A supplementary 75 rounds with gpt-4o reach 90.7%, with pure replay at 29.0 s. Success is checked by programmatic ADB checkers. There is one baseline: the same stack with Layer 1 only. Corrections to the record: (a) '84.1 -> 35.4 s (2.4x)' compares the 35 pure-replay rounds with the baseline's mean over all rounds. These are not matched tasks, and it does not follow the paper's own speed-up definition (same task type). (b) Table 2 lists 36.0 s where the text says 35.4 s, and 69.6 s for all rounds where Table 3 says 69.0 s. (c) The like-for-like aggregate is 84.1 -> 69.0 s, 1.22x (calc.). (d) '100% over 79 rounds' only counts rounds where replay did not fall back fully; the 29 that did fall back succeeded 75.9% of the time. (e) '+23 pp' is against a single stateless baseline, not several. (f) No public benchmark; the model is gpt-4o-mini.

**mechanism and term:**

The mechanism is correct. Successful Layer 1 trajectories are compiled into parameterized templates (weighted element locators, typed slots) stored in SQLite. A matching cascade tries regex, then embeddings (all-MiniLM-L6-v2), then an app filter. Replay runs over ADB, with step-level LLM fallback (at most 2 consecutive, 5 in total), a full Layer 1 fallback, and recompilation driven by failure learning. Terms: (1) c_k -> 0 only in the pure-replay rounds (23% of rounds); a semantic match costs 1 LLM call; overall LLM calls per round fall 49%. (2) N (steps) is unchanged: replay still performs every UI action. (3) Environment: the paper names ADB actuation (about 100 ms per tap) as the limit, and replay rounds still average 36-55 s. (4) Success rate up +23.3 pp, partly because the baseline degrades across phases (80% -> 44%).

**authors and venue:**

Qijia Chen and Giulio Jacucci (University of Helsinki), Andrea Bellucci (Universidad Carlos III de Madrid), Zhida Sun (Shenzhen University). arXiv cs.HC, no comment. The PDF uses the ACM template placeholder (Conference'17, Washington DC; DOI nnnnnnn), so there is no venue, and the code is promised upon acceptance. Conditions (i), (ii) and (iv) pass; (iii) FAILS. The numbers come from an author-built suite of 15 task types, not a public benchmark, even though the model and round count are stated. Under the references.md rule it goes under 'Not used'.

**formula:**

App. D (p.12): Speedup = L̄_L1 / L̄_L2, the ratio of mean Layer 1 latency to mean Layer 2 latency for the same task type. C_LLM = 0 for pure L2 replay, 1 for semantic match + replay, and in [5, 15] for full L1 execution. Section 3.4 (p.5): r_fail = n_fail / (n_succ + n_fail), with recompilation flagged when r_fail > 0.5. The reported 2.4x does not follow the paper's own same-task-type definition.

## 23. AutoDroid-V2

**read:** https://arxiv.org/pdf/2412.18116v3 (v3, 6 May 2025, the latest version, carrying the MobiSys ACM block). Compared with v1: the 669.2 / 46.3 s, 93.1%, 43.9% and 54.4% figures are the same. Crossref DOI 10.1145/3711875.3729134 checked.

**verdict:** confirmed

**effect:**

Section 4.3 (p.9), Fig. 4a: average LLM inference latency per task is 46.3 s for AutoDroid-V2 vs 669.2 s for the baseline AutoDroid (step-wise) on a Snapdragon 8 Gen 2 (OnePlus ACE 2 Pro). The paper reports a 93.1% reduction; the ratio is 14.45x (calc.). Both use fine-tuned Llama-3.1-8B, quantized to 8-bit, run with llama.cpp. Section 4.1 (p.9) defines inference latency as running from when the model receives the prompt to its final output token. It is not end-to-end: GUI execution over ADB is excluded. Table 2 (p.10), DroidTask average success rate: AutoDroid-V2 (Llama-3-8B-ft) 54.4% vs AutoDroid (Llama-3-8B-ft) 43.9%, +10.5 pp. DroidTask has 158 tasks across 13 apps (p.8). A task counts as a success when the ground-truth action sequence is a subsequence of the agent's actions. Table 4 (p.10), tokens per task: AutoDroid input 3452.5 (431.3 cached, 3021.2 remaining), output 832.4; AutoDroid-V2 input 2828.0 (2760.1 cached, 67.9 remaining), output 122.9. Prefill takes 14.0 s vs 85.3 s per prompt. Excluded offline costs: GPT-4o at $4.11 per app for document generation, $7.83 for data synthesis and $70.48 for solution validation ($82.42 per app in total, calc.), plus about 2.5 GPU-hours of fine-tuning on 8×A100. Internal inconsistency: the paper's own summary (p.2) claims 5.7-13.4x lower LLM inference latency and 43.5x / 5.8x fewer runtime input/output tokens. That range does not contain the 14.45x implied by 669.2/46.3, and the basis of the range is not stated. AitW-subset (68 tasks): 47.1% vs 36.7%.

**mechanism and term:**

The mechanism is correct. Offline, GPT-4o builds a UI-centric app document from exploration traces and synthesizes and validates task-script training data. The on-device SLM is fine-tuned on this data. At run time it generates one multi-step script per task, executed by an interpreter with dependency-aware element locating; a runtime failure triggers script regeneration. Terms: (1) N and c_k, a structure change: confirmed (one script query per task plus regeneration on error, instead of one query per step). (2) Price/tier is WRONG for this comparison. The baseline AutoDroid runs the same local fine-tuned Llama-3.1-8B on the same phone, so price/tier does not change; remove it, or mark it as the paper's motivation only. (3) Prefill is missing from the record. The static document prefix (97.6% of the prompt) is KV-cached, uncached input per task falls from 3021.2 to 67.9 tokens, and prefill falls from 85.3 s to 14.0 s per prompt. (4) Decode is missing: output tokens per task fall from 832.4 to 122.9. (5) Success rate up: confirmed. (6) Environment time is not measured.

**authors and venue:**

Hao Wen, Shizuo Tian, Borislav Pavlov, Wenjie Du, Yixuan Li, Ge Chang, Shanhui Zhao, Jiacheng Liu, Yunxin Liu, Ya-Qin Zhang and Yuanchun Li. All are at Tsinghua AIR; Yunxin Liu and Yuanchun Li also list Shanghai AI Lab, and Yuanchun Li also BAAI. MobiSys '25 is confirmed by the PDF's ACM block and by Crossref: Proceedings of the 23rd Annual International Conference on Mobile Systems, Applications and Services, June 2025, pp. 223-235. It passes.

**formula:**

No speed-up or cost equation. Section 4.3 (p.10) splits LLM inference latency qualitatively into a prefill phase and a decode phase, and says each response's latency depends mainly on the remaining (uncached) input tokens and the output tokens. It also defines the metric RRR = n/k (reversed redundancy ratio, section 4.1).

## 24. AppAgentX

**read:** https://arxiv.org/pdf/2503.02268v3 (v3, 15 Apr 2025, latest). Also diffed against v2 (13 Apr 2025): the body text and all numbers are identical. Only the title-block affiliations changed.

**verdict:** corrected

**effect:**

Numbers exact. Table 2, p. 9, AndroidWorld, 116 tasks, AppAgent -> AppAgentX: Task Time 147.17 -> 59.74 s, Tokens 18.9k -> 6.2k, SR 41.7% -> 62.5%. The same table also gives DroidTask (158 tasks): 106.24 -> 56.29 s, 11.5k -> 5.1k, 46.3% -> 88.2%; and A3 (201 tasks): 134.67 -> 48.12 s, 19.2k -> 4.7k, 10.3% -> 39.3%. Conditions, paraphrased from §5.1 (p. 6) and §5.2 (p. 7). (a) Model: GPT-4o is the default model unless otherwise stated, and Table 2 states no other, so the model is GPT-4o. The record's 'model not recorded' is wrong. (b) Task Time runs from the start of task execution until the agent decides the task is complete (wall-clock per task). (c) Time comparisons use only tasks that every method completed. (d) Tokens are prompt plus completion tokens, averaged over all tasks. (e) Runs: §5.1 says each task is repeated five times by default, but §5.2 says five experiments for the baseline comparison and two for the large datasets. Table 2 is the large-dataset table, so it rests on two runs, not one. The record's 'single run' is wrong. (f) The baseline is AppAgent (Zhang et al., 2023), rerun by the authors. Per-step data (Table 1, p. 7) come from the AppAgent benchmark (50 tasks, GPT-4o), not AndroidWorld: chain memory with the basic action space vs with basic+evolved actions gives 9.1 -> 5.7 steps, 23 -> 16 s per step, 9.26k -> 4.94k tokens, SR 70.8% -> 71.4%. Table 4 (p. 12) gives per-step time with GPT-4o: 20.3 s (AppAgent) vs 17.5 s (ours). calc.: AndroidWorld 2.46x faster per task, 3.05x fewer tokens, +20.8 pp SR.

**mechanism and term:**

Mechanism confirmed. Repetitive low-level action sequences found in the execution history become 'shortcut nodes', i.e. high-level actions. The LLM still decides once whether a shortcut applies and fills an execution template with arguments. The low-level actions then run through page matching and retrieval, with no per-step LLM reasoning. If a shortcut fails to match or execute, the agent falls back to the basic action space (§4.2-4.3). Term mapping, corrected in part: (1) N (LLM-reasoned passes) smaller. This is quantified only on the AppAgent benchmark (Table 1, 9.1 -> 5.7 steps); AndroidWorld reports no steps. (2) Tokens per task are smaller, but the paper reports prompt+completion as one total, so the saving cannot be split into prefill vs decode. (3) Per-step time also falls (23 -> 16 s) because shortcut steps skip LLM reasoning. The environment term is not reduced: every low-level action still runs on the device. (4) Success rate: the AndroidWorld gain (41.7 -> 62.5%) compares the full AppAgentX (chain memory + evolution) against AppAgent. The Table 1 ablation credits SR mainly to memory (AppAgent 69.7% -> chain memory 70.8%), and the evolution/shortcut step adds only 70.8 -> 71.4%. So 'success rate up' should not be credited to the shortcut mechanism. Classify AppAgentX under N (and tokens) smaller. Caveat: the time figures cover only tasks every method solved.

**authors and venue:**

Authors confirmed in v3: Wenjia Jiang (Westlake U; Henan U), Yangyang Zhuang, Chenxi Song, Chi Zhang (Westlake U), Xu Yang (Southeast U), Joey Tianyi Zhou (IHPC and CFAR, A*STAR). The IHPC/CFAR detail appears only in v3; v2 prints just 'A*STAR'. references.md l.113 therefore cites v2 but uses v3's affiliations: cite v3. No venue: the arXiv page carries no journal-ref or comment, and a web search found no acceptance. It stays a preprint. It passes the credibility rule: institutions are verifiable, and the benchmark is public with task count (116) and model (GPT-4o default) stated.

**formula:**

No speedup or cost formula. The only equation is the action-space definition A_evolved = A_basic ∪ {ã} (Eq. 2, §4.2, p. 5), where ã is a high-level action abstracted from a sequence of low-level actions in A_basic.

## 25. UFO2 (GUI + native API, multi-action)

**read:** https://arxiv.org/pdf/2504.14603v2 (v2, 25 Apr 2025; latest arXiv version). The TMLR camera-ready (https://openreview.net/pdf?id=iAuZVWCduc) could NOT be read: OpenReview returned a browser-verification page. All numbers below are from arXiv v2 only. TMLR acceptance confirmed on the TMLR accepted-papers list, https://jmlr.org/tmlr/papers/ (read 2026-09-28).

**verdict:** corrected

**effect:**

GUI+API, Table 5 (§6.4, p. 18). ACS = average number of LLM-involved action-inference steps per task, computed on the tasks both configurations complete (subset size not given). o1: SR 16.3% -> 24.5%, ACS 16.0 -> 6.6. GPT-4o: SR 16.3% -> 22.4%, ACS 13.8 -> 12.9. The text gives the step savings as 6.5% (GPT-4o) and 58.5% (o1). calc.: 58.75%. Setup: 12 hand-built APIs for Word, Excel and PowerPoint, built around the 27 office-related OSWorld tasks. No APIs for WAA. The SR values equal the OSWorld-W full-benchmark figures in Tables 1 and 6, and they fit 49 tasks (8, 11 and 12 of 49), not 27 (calc.). So the record's 'Office tasks' label is right for the step counts but not for the SR. Multi-action, Table 7 (§6.6, p. 19), single -> speculative, ACS on each common-success subset. WAA (154 tasks): GPT-4o 10.00 -> 8.78, SR 23.4% -> 23.4% (subset 30 tasks); o1 9.95 -> 8.85, SR 25.3% -> 24.7% (subset 32). OSWorld-W (49 tasks): GPT-4o 13.30 -> 7.40, SR 22.4% -> 24.5% (subset 10); o1 6.80 -> 3.30, SR 24.5% -> 26.5% (subset 10). The record's multi-action numbers are the o1 rows and must say so. The OSWorld-W step counts rest on only 10 tasks. Every SR change is a single task (calc.). The text says steps fall 'by up to 10% on WAA'; calc. gives 11.1% (o1) and 12.2% (GPT-4o). Summary list (§6, p. 14): 'lowering inference cost by up to 51.5%'. That equals the o1 OSWorld-W step cut (6.80 -> 3.30 = -51.5%, calc.). No $ or tokens were measured. Table 8 (§6.8, p. 21), full UFO2 vs UFO2-base, total steps on tasks all configurations solved: o1 WAA 9.14 -> 6.05 (34 tasks), o1 OSWorld-W 11.33 -> 5.50 (8 tasks), GPT-4o WAA 10.32 -> 10.21 (31 tasks). E94 confirmed (§6.8, Latency Breakdown, Fig. 24, p. 21): LLM inference dominates total latency at about 10 s per inference in every configuration. The paper also puts tasks at about 1 minute. No wall-clock comparison exists for GUI+API or for multi-action.

**mechanism and term:**

Two mechanisms, and they map to different terms. (A) GUI+API: one native API call (for example save_as) replaces a sequence of GUI steps, so N (LLM inference steps) is smaller. This is measured only as ACS and depends heavily on the model: o1 -58.8%, GPT-4o -6.5% (calc.). SR rises by 3-4 tasks out of 49 (calc.). The environment term (fewer UI actions and waits) plausibly shrinks too, but is not measured. (B) Speculative multi-action (§3.7, Algorithm 1): one LLM call predicts a batch of k actions. Each action is checked through UIA (IsEnabled/IsVisible) just before execution; the batch stops at the first failed check and the agent replans. This lowers the number of model calls per task and raises the actions per call. The environment term is unchanged: every action still runs, plus one UIA check each. Decode per call presumably grows, but this is not measured. SR changes by one task either way, so the record's 'mixed on WAA' is correct. 'Up to 51.5% lower inference cost' is the authors restating a step count as cost, on a 10-task subset, not a cost measurement. Label it as an author claim. The record's 'N smaller; success rate up (mixed on WAA)' holds once it is split by mechanism and by model. The ≈0 overlap term is untouched: the actions run in sequence.

**authors and venue:**

Venue confirmed: TMLR, May 2026. The jmlr.org/tmlr list shows 22 authors (Bo Qiao included, 'Paul Jiang'), with an openreview/pdf/bib link to id iAuZVWCduc. The arXiv v2 PDF itself also prints 22 names, including Bo Qiao and 'Zhao Jiang'. Only the arXiv abstract-page metadata lists 21 names (no Bo Qiao). Refine references.md l.50 accordingly. Affiliations in the v2 PDF: Microsoft (most authors), ZJU-UIUC Institute (Chiming Ni), Nanjing University (Jian Mu), Peking University (Jiaxu Qian). The PDF header 'Conference'17, July 2017, Washington, DC' is template text, not a venue. doc2's 'preprint' label is out of date. Credibility: passes as a journal paper.

**formula:**

No speedup or cost formula. §3.7 gives Algorithm 1 (speculative multi-action execution): A ← LLM_Predict(C0, k); for i = 1..k: break if not UIA_IsEnabled(ctrl, C) or not UIA_IsVisible(ctrl, C); Execute(ctrl, op); C ← UIA_GetContext(); if |Executed| < k: ReportPartial, Replan(C). The step-to-cost link is stated only in words (§6.6): every step needs an LLM call, so fewer steps means lower latency and cost.

## 26. ComputerRL (API-GUI action space)

**read:** https://arxiv.org/pdf/2508.14040v2 (v2, 21 Oct 2025, latest). Also the ICLR 2026 camera-ready: https://proceedings.iclr.cc/paper_files/paper/2026/file/28707388472adc117714e83d44bfaebb-Paper-Conference.pdf (header 'Published as a conference paper at ICLR 2026'), cross-checked with the poster page https://iclr.cc/virtual/2026/poster/10007435 (found via search).

**verdict:** confirmed

**effect:**

Framework ablation, Table 3 and §4.3 (arXiv v2 p. 8-9; the same numbers are in the ICLR version). The run is labelled 'Framework Ablation (w/ GPT-4o)': an untrained, prompted GPT-4o, not the RL-trained agent. OSWorld average SR: GUI-only 11.2% vs API-GUI 26.2% (+134% relative, as the paper states). Office domain 6.2 -> 27.9%; Professional 14.3 -> 41.6%. Main result, Table 1 (captioned 'updated in 2025.08'): GLM-4.1V-9B-Thinking 48.9±0.5 on OSWorld and 48.0 on OSWorld-Verified; GLM-4-9B-0414 48.1±1.0 and 47.3. OSWorld is described as 369 tasks in the paper's related-work section. §4.1 claims the agent completes tasks in at most 1/3 of the strongest baseline's steps. Neither arXiv v2 nor the ICLR camera-ready gives any step counts, step table or step budget. The ICLR Appendix E plots 'Average Turns' only as a training-curve indicator, not as an evaluation comparison. No time or $ is reported. Naming: arXiv v2 calls the agent AutoGLM-OS-9B; the ICLR camera-ready calls it GLM-ComputerRL-9B.

**mechanism and term:**

Mechanism confirmed. An LLM-driven workflow builds application APIs automatically (requirement analysis, implementation, test generation, §2.1). These APIs are merged with GUI actions into one API-GUI action space, and the policy is trained by step-level GRPO online RL alternating with SFT (Entropulse) on thousands of parallel VMs. Term mapping confirmed: N claimed smaller, but only as an unquantified author statement (D93 stands); success rate up. The API-GUI SR gain (11.2 -> 26.2%) is measured with prompted GPT-4o, so it belongs to the action-space change, not to RL. The distributed RL infrastructure speeds up training throughput, not per-task inference, so it maps to no term in the per-task time/cost formula. Do not count it as agent acceleration. The 9B policy suggests a cheaper price/tier, but the paper reports no inference cost, so do not claim it.

**authors and venue:**

Authors confirmed: Hanyu Lai, Xiao Liu, Yanxiao Zhao, Han Xu, Hanchen Zhang, Bohao Jing, Yanyu Ren, Shuntian Yao, Yuxiao Dong, Jie Tang. Institutions corrected: Tsinghua University, Z.AI, AND University of Chinese Academy of Sciences (Yanxiao Zhao). references.md l.77 omits UCAS. Several authors interned at Z.AI. Venue confirmed: ICLR 2026 (conference PDF header and ICLR virtual poster page). The arXiv page itself carries no venue note. Credibility: passes as a conference paper; the step reduction is not quantified.

**formula:**

No speedup or cost formula. The only formula is the training objective J_StepGRPO(θ): a clipped policy ratio times step-level advantages A_{i,j}, minus β·D_KL(π_θ || π_ref) (§3.2).

## 27. AXIS (API-first agent)

**read:** https://aclanthology.org/2025.acl-long.381.pdf (published ACL 2025 version; the footer reads Proceedings of the 63rd Annual Meeting of the ACL (Volume 1: Long Papers), pages 7711–7743).

**verdict:** confirmed

**effect:**

Numbers exact. Table 1 (§5.2, p. 7716), 50 Microsoft Word tasks taken from the wikiHow 'Use Microsoft Word' page and the official Word site; UI Agent = UFO; LLM backend GPT-4o version 20240513. Time 59.5 -> 29.9 s, SR 52.0 -> 84.0%, steps 3.2 -> 2.0, cost $0.4 -> $0.2. All pairwise differences are significant (p < 0.001; steps p < 0.01). The text calls AXIS twice as fast on average. Table 2: total UI actions 103 -> 48; API actions 9 -> 39. User study (§6, Tables 3-4, p. 7718): 20 participants (App. C.2, p. 7726), 5 Word tasks, L1/L2. Time: manual 61.8/167.6 s, UI agent 104.6/155.5 s, AXIS 18.2/57.1 s. SR: manual 100/97.5%, UI agent 75/45%, AXIS 98.3/95.0%. Steps: UI agent 6.4/11.1 vs AXIS 1.0/4.2. Cost: $0.6/$0.9 vs $0.07/$0.3. The user-study backend is printed as 'GPT-4, version 20240513' (§6.1). The abstract's 65-70% time cut is AXIS-assisted vs manual human work (D92 stands). calc.: agent vs agent 1.99x faster; cost per success $0.77 (UFO) vs $0.24 (AXIS). One application (Word) only.

**mechanism and term:**

Mechanism confirmed. AXIS prefers API calls ('skills') over UI actions. It grows its skill library by exploring the application: 347 seed files yielded 73 skills, and a Translator agent converts UI-operation code into API calls, which dynamic validation then checks. Term mapping confirmed: N smaller (3.2 -> 2.0 steps); environment smaller (UI actions 103 -> 48 over 50 tasks, measured as action counts, not wait time); money smaller ($0.4 -> $0.2 per task on average); success rate up (52 -> 84%). The per-task time comes from one app and 50 tasks, and the paper does not define how agent execution time was timed. Cite the -65-70% only against manual work, never as an agent-vs-agent speedup.

**authors and venue:**

Authors confirmed (10): Junting Lu, Zhiyang Zhang, Fangkai Yang, Jue Zhang, Lu Wang, Chao Du, Qingwei Lin, Saravan Rajmohan, Dongmei Zhang, Qi Zhang. Institutions corrected: Peking University (Lu), Nanjing University (Zhang) and Microsoft (the rest). The first two are marked equal contribution, work done during an internship. references.md l.40 lists Microsoft only. Venue confirmed: ACL 2025 Long, pp. 7711–7743, doi 10.18653/v1/2025.acl-long.381. Credibility: passes as a conference paper.

**formula:**

None. The paper gives no speedup or cost formula.

## 28. Beyond Browsing (API-based web agent)

**read:** https://arxiv.org/pdf/2410.16464v3 (v3, 16 Jun 2025, latest) and the published version https://aclanthology.org/2025.findings-acl.577.pdf (Findings of ACL 2025, pp. 11066–11085). The numbers are identical in both.

**verdict:** corrected

**effect:**

Table 2 (§6.1, ACL p. 11072), WebArena, GPT-4o base LLM, OpenHands framework. Average SR: Browsing Agent 14.8%, API-Based Agent 29.2%, Hybrid Agent 38.9%. The abstract calls the Hybrid gain 'more than 24.0%' absolute; calc. +24.1 pp. Reddit rows use APIs the authors built themselves. Task count: I did not find it stated in the text. Table 6's per-choice counts sum to 812, and 316/812 = 38.9% (calc.). CORRECTION: steps and $ ARE reported, contrary to the record. Table 7 (App. A.4, ACL p. 11082) gives average steps and cost in USD: Browsing 8.4 steps, $0.1; API-Based 7.8 steps, $1.2; Hybrid 8.5 steps, $1.4. Per-website: GitLab Browsing 9.4 steps/$0.2 vs Hybrid 8.1/$2.0. The appendix text says the API-Based agent takes the fewest steps, the Hybrid agent the most, and browsing is much cheaper because API prompts are far longer (GitLab exposes 988 endpoints). §6.3: API-solvable tasks need 2.1 API calls on average, yet the API-Based agent's 7.8 steps go mostly to fetching docs, fixing errors and verifying output. The paper does not say whether the averages include failed tasks. Wall-clock time is not reported. calc.: cost per success Browsing ≈ $0.68, Hybrid ≈ $3.60, API-Based ≈ $4.11. Because costs are printed to one decimal, Hybrid's cost per success is roughly 3-11x Browsing's.

**mechanism and term:**

Mechanism confirmed. A Hybrid agent (OpenHands CodeAct plus BrowsingAgent) interleaves Python API calls with browser actions. For sites with more than 100 endpoints it retrieves documentation in two stages. Term mapping WRONG in the record. N is not smaller for the Hybrid agent: 8.5 vs 8.4 average steps. Only the API-only agent is slightly lower, at 7.8. Money is much LARGER (about 12-14x per attempt at the rounded values, calc.) because API documentation inflates the prompt: the prefill tokens per call grow. Only the success rate improves (14.8 -> 38.9%). Reclassify: success rate up, while prefill/money go up. Part 2 should present this work as a counter-example. Replacing GUI steps with APIs does not cut cost when the API documentation sits in context. Cost per success rises too (calc.).

**authors and venue:**

Authors confirmed: Yueqi Song, Frank Xu, Shuyan Zhou, Graham Neubig, all Carnegie Mellon University (the only affiliation printed). Venue confirmed: Findings of ACL 2025, pp. 11066–11085, from the ACL Anthology PDF footer (aclanthology.org/2025.findings-acl.577). Credibility: passes as a conference paper. The record's 'efficiency not reported' is wrong: steps and $ are in Appendix Table 7.

**formula:**

None. The paper gives no speedup or cost formula.

## 29. ECLAIR (qualitative only)

**read:** https://arxiv.org/pdf/2405.03710v1 (v1, 3 May 2024, the only version) and the published https://www.vldb.org/pvldb/vol17/p2805-wornow.pdf (PVLDB 17(11): 2805–2812, 2024; doi 10.14778/3681954.3681964).

**verdict:** corrected

**effect:**

Figures confirmed; conditions added. Test set (§4, PVLDB p. 2808): 30 WebArena workflows (GitLab and Adobe Magento) that the WebArena GPT-4 baseline failed. Human annotators recorded demonstrations and wrote SOPs; the model is GPT-4. The 93% figure (Table 1, p. 2808) is SOP correctness, not an agent run. GPT-4 wrote SOPs from the workflow description, key frames and action trace (WD+KF+ACT), and a human judged them correct enough to complete 93% of workflows. With WD+KF the figure is 0.90; with WD, 0.60. The 40% figure (Table 2, p. 2809) is GPT-4 'Overall Workflow Completion Acc.': 0.40 with SOP vs 0.17 without; next-action accuracy 0.92 vs 0.83. Setup (§4.2.1, paraphrased): at each step the model receives the ground-truth action history, the full SOP and the current GUI, and a human judges each suggested action. So the setting is teacher-forced, not a free-running end-to-end run, and the paper does not define how workflow completion is computed from the per-step judgements. The introduction presents it as 0% -> 40% over the WebArena GPT-4 baseline. No per-run time, token or $ figure is reported. The paper's $ figures ($150k vendor + $100k consultants, over 12 months, 2 FTEs) come from interviews in RPA case studies, not agent measurements.

**mechanism and term:**

Positioning confirmed. ECLAIR uses a multimodal foundation model (FM) for all three RPA stages: demonstrate, execute and validate. In execution the FM suggests and grounds an action at every step of every run, so the LLM stays in the loop and c_k is kept. What it lowers is set-up and maintenance effort (human workflow encoding, versus RPA scripting), and that is not a term in the per-run time/cost formula. Classification 'none reduced (counter-positioning)' is correct. Note that the 40% is teacher-forced and must not be compared with live end-to-end success rates such as WebArena's.

**authors and venue:**

Citation corrected: Wornow, M., Narayan, A., Opsahl-Ong, K., McIntyre, Q., Shah, N. H., & Ré, C. (2024). Automating the Enterprise with Foundation Models. PVLDB 17(11): 2805–2812. All six authors are at Stanford University. 'Stanford Hazy Research' is Ré's lab and the code repository's owner (github.com/HazyResearch/eclair-agents), not the byline. Venue confirmed from the PVLDB Reference Format block and doi in the published PDF. The arXiv page carries no journal-ref. Credibility: passes (published venue; authors and institutions verified). It is not yet in references.md.

**formula:**

No speedup or cost formula. §2.2 (Problem Formulation) states the aim, end-to-end automation of enterprise workflows at minimal cost, and defines a workflow as an alternating state-action sequence w = (s, a, s′, a′′, …), w ∈ W, s ∈ S, a ∈ A.

## 30. Speculative Actions

**read:** arXiv:2510.04371v2 PDF (23 Apr 2026), full text: https://arxiv.org/pdf/2510.04371v2 ; arXiv HTML v2 for the formulas: https://arxiv.org/html/2510.04371v2 ; ICLR 2026 camera-ready PDF: https://proceedings.iclr.cc/paper_files/paper/2026/file/fb279d7a134ad6fead7953ac7fd77fc4-Paper-Conference.pdf (all percentages are identical to v2) ; OpenReview API record P0GOk5wslg (venue field). The OpenReview PDF returned 403 behind a bot challenge, which I did not attempt to get past.

**verdict:** confirmed

**effect:**

Chess (§3.1.2, Fig. 2): 3 predictions give an average time saving of 19.5% and an average prediction accuracy of 54.7%, averaged over 5 runs of 30 steps. The other settings are 1 prediction 11.8% / 31.3% and 2 predictions 15.0% / 41.3%. Time saved = (T_seq − T_s)/T_seq. Setup: TextArena, two-player game. The Actor is GPT-5 with high reasoning effort; the Speculator is GPT-5 with low reasoning effort and a move-prediction system prompt (§3.1.1). The baseline is the same game played sequentially. The authors note that live-API latency varies, so the results are not perfectly reproducible (§3.1.2).

E-commerce (§3.2.2, Fig. 3): 22–38% of API calls are correctly predicted. The metric is 'APIs prediction accuracy': the share of speculative API calls that match the ground-truth APIs needed for the user's query. Benchmark: τ-bench retail, which defines 115 tasks and 15 APIs (App. B.1); the number of tasks actually evaluated is not stated. Speculators: gpt-5-nano/-mini/-5 and gemini-2.5-flash at 1024/2048/4096-token budgets, alone or combined. The paper turns this into 'roughly one third of turns' answered faster, using a 2–3 s speculation time taken from a third-party leaderboard against ~30 s of assumed user typing time. This is not a measured speed-up.

HotpotQA (§3.3, App. B.2, Fig. 4): up to 46% top-3 accuracy of the predicted next API call. Actor: gemini-2.5-flash. Speculators: GPT-5-nano, GPT-4.1-nano, Gemini-2.5-flash. Matching is strict (same call and same parameter); the question count is not stated.

OS tuning (§4) is lossy (last-write-wins). Its p95 latency is 37.93 ms vs 54.00 ms for Actor-only, and cost is 0.17 vs 2.18 cents.

Abstract: arXiv v2 says 'up to 55%' accuracy and 'up to 20%' latency reduction; the ICLR camera-ready abstract replaces 'up to 20%' with 'substantial latency reductions'. The paper has no side-effect audit (an absence, not a measured zero).

**mechanism and term:**

Mostly right; one refinement. Mechanism (§2, Alg. 1): the Actor and the Speculator run in parallel. For each of the k guessed responses the next API call is pre-launched and cached. A cache hit on the next step skips the real call and awaits the pending one. Safety comes from semantic guards, an idempotent/reversible/sandboxed envelope and rollback (§1, §2).

Terms:
- Overlap saving introduced: yes. In chess, the out-of-turn player's analysis overlaps the in-turn player's call.
- Money larger: yes. Theorem 3 gives the extra-token ratio and Fig. 6 plots extra tokens against time.

Correction to 'proves single-step speculation saves at most 50%': the 50% bound comes from Proposition 1's stochastic model of the breadth-focused one-step scheme (Alg. 1). The model assumes Exp(α) speculator latency and Exp(β) API latency with β<α, independent hits, and negligible f and π. The paper says Proposition 1 'suggests' the bound, reached at p=1, α=∞. It is not a general theorem about all single-step speculation. §5.3's depth-focused variant gives a saving of p(1−b/a) instead, and the OS extension is lossy, not lossless.

**authors and venue:**

Confirmed: Ye, Ahuja, Liargkovas, Lu (equal contribution), Kaffes and Peng, all at Columbia University (PDF author block). Venue: ICLR 2026 Oral (OpenReview venue field 'ICLR 2026 Oral', id P0GOk5wslg). The ICLR proceedings index title is '…Faster AI Agents', but the camera-ready PDF itself keeps the arXiv title '…Faster Agentic Systems'. It is a conference paper, so it passes the source-credibility rule.

**formula:**

Prop. 1 (§2): E[T_s]/E[T_seq] = 1 − (1/T)·(α/(α+β))·[ (T−1)p(k)/(1+p(k)) + p(k)²/(1+p(k))² − p(k)²/(1+p(k))²·(−p(k))^(T−1) ] → (T→∞) 1 − p(k)/(1+p(k)) · α/(α+β). Here p(k) = 1−(1−p)^k, speculator latency ~ Exp(α) and API latency ~ Exp(β).

Theorem 3 (§5.1, cost): E[M_spec − M_seq]/E[M_seq] = k̃ − (1/T)(k̃ + α/(α+β))·[same bracket] → k̃ − (k̃ + α/(α+β))·p(k)/(1+p(k)), where k̃ = the number of distinct speculated actions.

Theorem 4 (§5.2): m*_t(p) ∈ argmax_{m∈{0..k}} { q(m;p)·Δ_t − c·m }, with q(m;p) = 1 − Π_{j=1..m}(1 − p_(j)), Δ_T = 0 and a backward recursion for Δ_t.

Depth-focused (§5.3): E[T_seq − T_spec]/E[T_seq] = ((T−1)/T)·p·(1 − b/a) and E[M_spec − M_seq]/E[M_seq] ≈ ((T−1)/T)·((1−p)(a/(2b) − 1/2) + p). Here a and b are the actor and speculator latencies.

Chess metric (§3.1.2): time saved = (T_seq − T_s)/T_seq.

## 31. Interactive Speculative Planning (ISP)

**read:** ICLR 2025 camera-ready PDF: https://proceedings.iclr.cc/paper_files/paper/2025/file/25458943db16e0f78f748ca5bc34fff6-Paper-Conference.pdf ; arXiv:2410.00079v1 PDF (30 Sep 2024, the only arXiv version): https://arxiv.org/pdf/2410.00079v1 . Table 2, Table 3 and the TravelPlanner appendix numbers are identical in the two. OpenReview API record BwR8t91yqh (venue field).

**verdict:** confirmed

**effect:**

OpenAGI (ICLR §4.1, Table 2): 117 multi-step tasks (§3 Benchmarks). k = 4.
- Setting 3: approximation A = CoT on GPT-4-turbo; target T = multi-agent debate (2 agents × 2 rounds) on GPT-4-turbo.
  - Average total time (TT): 105.42±50.84 vs 182.70±421.49 for normal (sequential) planning. The paper reports a total-time cut of 42.30% and a stepwise cut of 38.29%.
  - Cost per plan: $0.2973±0.1387 vs $0.2160±0.0795.
- Setting 1 (A = direct generation, T = ReAct; both GPT-4-turbo): TT 33.91 vs 43.63 (−22.27%); cost $0.122 vs $0.0713.
- Setting 2 (T = CoT): −28.32%; cost $0.074 vs $0.044.
- Setting 4 (A = GPT-3.5-turbo, T = GPT-4-turbo, both direct generation): −20.37% at ~$0.0012 for both.
- The ICLR text puts the cost increase at about 70% for Settings 1–2, 37% for Setting 3, and almost none for Setting 4. The ICLR version says time is recorded in seconds and the cost row carries $.
- Caveat: the sequential MAD baseline's SD (421.49) is about 2.3× its mean (calc.), so the −42.30% average is outlier-sensitive.
- Calc.: MAD cost +37.6%, ReAct +71.1%, CoT +68.2%.
- Maximum concurrent API calls (MC): 4.53–4.66 in Settings 1–3 and 4.05 in Setting 4 (OpenAGI), vs 1 for sequential.

TravelPlanner validation (Table 3; task count not stated in the paper): total time −21.43% (S1), −19.18% (S2), −25.46% (S3); MC = 5. Actions are accepted when the function name matches exactly and the parameters' Levenshtein distance is < 0.3. The Commonsense Constraint Micro Pass Rate (ICLR App. D) drops in all three settings: S1 48.6→41.7%, S2 41.7→34.7%, S3 54.3→48.6%. The Delivery Rate is unchanged at 55.6% in all three. The recorded '48.6→41.7' is Setting 1 only.

**mechanism and term:**

Right, with one refinement. The approximation agent A runs ahead, generating up to k=4 consecutive steps. The target T starts a verification thread for each drafted step concurrently. On the first mismatch, later threads are cancelled and T's step is adopted. Users can interrupt and supply steps (§3).

Terms:
- Overlap saving: introduced.
- c_k larger: yes. Peak concurrency MC is 4–5 vs 1, and total generated tokens rise (e.g. MAD 6781 vs 4075; +66%, calc.).
- Money larger: yes.
- Success rate: unchanged on OpenAGI, where exact match keeps the output identical. On TravelPlanner, soft matching lowers micro pass by 5.7–7.0 pp (calc.) in every setting, while the delivery rate is unchanged.

**authors and venue:**

Authors confirmed: Hua, Wan, Vadrevu, Nadel, Zhang, Wang. Correction: there are three institutions, not two — Rutgers (Hua, Zhang), Microsoft (Wan, Vadrevu, Nadel) and Google DeepMind (Chi Wang), per the ICLR and arXiv author blocks. Venue: ICLR 2025 Poster (OpenReview venue field; the camera-ready PDF header carries the ICLR 2025 marking). It is a conference paper, so it passes the source-credibility rule.

**formula:**

ICLR §3, Time Efficiency Analysis:
- Without speculation, time = Σ_{i≤n} (time(T,s_i) + e(s_i)).
- With speculation, Eq. (1): Σ_{B_i ∈ B[:−1]} max{ end_time(T,s_j) | B_i+1 ≤ j ≤ B_{i+1} }. B is the list of breaking steps: a mismatch, or k consecutive speculative steps.
- Best case, Eq. (2): Σ_{i ∈ {i mod k = 0 | i<n}} max_{i≤j<i+k} end_time(T,s_j).
- Worst case, Eq. (3): Σ_{0≤i≤n−1} (time(T,s_i) + e(s_i)).
These are repeated in App. C.1 as Eqs. (4)–(6).

Tokens (App. C.2, Eqs. 7–8): T_{B_i} = Σ_{j=B_i+1}^{B_{i+1}} (token(A,s_j) + token(T,s_j)) + Σ_{j=B_{i+1}+1}^{M_i} (token(A,s_j) + token(T,s_j)), where the second sum is the wasted tokens; total = Σ_{B_i∈B[:−1]} T_{B_i}.

## 32. Dynamic Speculative Agent Planning (DSP)

**read:** ICLR 2026 camera-ready PDF: https://proceedings.iclr.cc/paper_files/paper/2026/file/0d1986a61e30e5fa408c81216a616e20-Paper-Conference.pdf ; arXiv:2509.01920v3 PDF (21 Sep 2025): https://arxiv.org/pdf/2509.01920v3 . The table values are identical; the tables are renumbered in the camera-ready. OpenReview API record YZ5k2dVj6O (venue field).

**verdict:** corrected

**effect:**

The recorded effect mixes two settings and two different baselines.

(1) −37.09% latency at +62.99% cost. This is OpenAGI Setting 2 (CoT-MAD), GPT backbone (GPT-4.1-mini, $0.40/$1.60 per 1M prompt/generation tokens), Dyn. (offset=2). Location: arXiv v3 §5.2.2 Table 4; ICLR camera-ready App. A.3 Table 3.
- ΔT is the per-task mean of (1 − T_SP/T_seq) against sequential planning.
- ΔCost is measured against sequential planning of both the target AND the approximation agent (App./§5.1: that sum is the minimum cost of any speculation). So +62.99% is overhead on top of T+A's sequential cost, not the increase over a plain target-only agent. The latter is larger and is not reported.
- Same table: Fix(k=6) gives −37.21% latency at +134.38% cost.

(2) '0.90× latency at 34.9% lower cost (1.25 vs 1.92)'. This is OpenAGI Setting 1 (Direct-ReAct), not CoT-MAD. Location: Table 1 (§5.1.1 in the camera-ready).
- The ratios are normalised to Fix(k=2), not to sequential.
- Dyn.(offset=2): T 0.90×, Cost 1.25×. Dyn.(τ=0.99): 0.91×, 1.25×. Fix(k=6): 0.90×, 1.92×.
- In Setting 2 the matching comparison is Dyn.(offset=2) 0.80×/1.27× vs Fix(k=6) 0.81×/1.77×; the paper calls this a 28.25% token-cost reduction.

Benchmarks: OpenAGI 312 multi-step tasks; TravelPlanner 180 tasks. DeepSeek settings 3–4 use A = DeepSeek-chat and T = DeepSeek-reasoner. The abstract headline is 'reducing total cost by 30% and unnecessary cost up to 60%'. The paper reports no task-success figure; it asserts losslessness because T's actions define the output.

**mechanism and term:**

Right. Mechanism: ISP-style speculative planning, with a DistilBERT predictor of the speculation depth k per state. The predictor is trained online and asynchronously by TD(λ) value learning (§4.1–4.2). The latency–cost trade-off is steered either by expectile regression τ or by an inference-time offset β (§4.3).

Terms:
- Overlap saving: introduced and tuned (depth k per step).
- Money: larger than sequential, lower than fixed deep k.
- c_k: peak concurrency MC ranges 3.00 (Fix k=2) to 6.44 (Fix k=6); dynamic variants stay below 6.
- Success rate: not changed by design; not measured separately.

**authors and venue:**

Authors confirmed (arXiv and ICLR camera-ready): Guan, Lan, Sun, Ding, Acharya, Wang, Wang, Hua. Correction: add Avey Research Center (Acharya). The full list is JHU, U Alberta, UBC, Avey Research Center, Google DeepMind and UCSB; Fei Sun has no affiliation marker, and Hua's contact email is microsoft.com. Venue: ICLR 2026 Poster (OpenReview venue field; camera-ready header marked as an ICLR 2026 conference paper). Cite the ICLR version; table numbers differ from arXiv v3. It is a conference paper, so it passes the source-credibility rule.

**formula:**

§5.1 / App. A:
- ΔTime = (1/N) Σ_{i=1}^{N} (1 − T_i^SP / T_i^seq) × 100%
- ΔP = (1/N) Σ (p_i^SP / p_i^seq − 1) × 100%, with p_i^seq = p_i^target + p_i^approx; ΔG is analogous
- ΔCost = (1/N) Σ ((PC_i^SP + GC_i^SP)/(PC_i^seq + GC_i^seq) − 1) × 100%
- PC_i^SP = ap_i^SP·cost_ap + tp_i^SP·cost_tp and GC_i^SP = ag_i^SP·cost_ag + tg_i^SP·cost_tg (seq analogues)
- T(×) = T^current/T^{k=2}, Cost(×) = C^current/C^{k=2}
- MC = (1/N) Σ MC_i; K = (1/M) Σ k_i

Predictor: L_θ = E_τ[(G_t^λ − V_θ(s_t))²] (Eq. 1), with the λ-return G_t^λ (Eq. 2). Expectile variant: L_2^τ(u) = |τ − 1(u<0)|·u². Offset: k = max(1, k̂ + β).

## 33. PASTE (pattern-aware speculative tool execution)

**read:** arXiv:2603.18897v3 PDF (16 Jun 2026): https://arxiv.org/pdf/2603.18897v3 ; v1 PDF (19 Mar 2026) for comparison: https://arxiv.org/pdf/2603.18897v1

**verdict:** confirmed

**effect:**

v3 abstract: average task completion time −43.5% and observed tool latency lower by 1.8×.

§6.2 (Fig. 10) phrases the headline as maxima: average latency reduced 'by up to 43.5%', p99 by up to 55.4%. The comparison is against vLLM, Agentix, ORION and SpecFaaS on the same hardware. The paper does not say which agent/benchmark/baseline gives the maximum.

§6.3 (tool side, vs ORION and SpecFaaS): average tool latency up to −55.2%, p99 tool latency up to −60.6%; pooled 1.71× over ORION and 1.83× over SpecFaaS.

§6.5 (sweep of arrival rate / concurrent sessions): at least 1.27× over vLLM and 1.24× over Agentix at each concurrency; pooled 1.50× and 1.30×.

§6.6 ablation (Fig. 17): E2E 270 s for PASTE vs 419 s Tool-Only and 342 s LLM-Only; LLM queueing 45 s vs 65 s.

§6.8 side effects: 602 potentially side-effecting speculative actions blocked out of >20,000; no task's final result differs from the baselines.

§6.9 resources: 1–3 idle CPU cores and 250 MB memory at a moderate budget.

Setup (Table 1, §6.1):
- 4 nodes × 8 A100-80GB (32 GPUs), vLLM.
- Models: Qwen-DeepResearch-30B (deep research) and Qwen3-30B-A3B (coding/science).
- Agents: gemini-cli, Qwen Deep Research, VirtualLab.
- Benchmarks: DeepResearchBench, SWE-bench, ScholarQA.
- Arrivals: Azure Functions trace replay.
- Patterns are mined from historical tasks disjoint from the test tasks.
- Task counts are NOT stated in v3 (or v1). No task-success rate is reported.

v1 comparison: v1 gave −48.5% and p95/p99 −48.6%/−61.9% (D13).

**mechanism and term:**

Right. Mechanism:
- The Pattern Analyzer mines control-flow and data-flow patterns and instantiates concrete predicted invocations.
- The Tool Speculation Scheduler admits a candidate only if it is executable, policy-safe, … (§4.2). A later authoritative call reuses a completed canonicalised match, promotes an in-flight one, or falls back.
- The LLM–Tool Co-Scheduler paces returning sessions into vLLM (§4.3).

Terms:
- Overlap saving introduced: tool execution overlaps LLM generation.
- Environment wait: exposed tool time hidden.
- Queueing: yes, via the co-scheduler's admission and load shaping. The ablation shows speculation alone raises queueing (65 s) and E2E (419 s).
- Money: small extra CPU/memory for speculative tool runs (§6.9).
- Success rate: final results unchanged per the §6.8 audit.

Scope: tool-calling agents on self-hosted models, not GUI agents.

**authors and venue:**

Authors and institutions confirmed from the v3 PDF author block: Sui, Zhao, Ma, He, Wang, Xu, Chen, Li, Yang — SJTU, Microsoft Research, Stevens Institute of Technology, Google (Xu), HKUST (Xu, Chen). This is a preprint; no venue appears on the arXiv page or in the PDF (running head 'arXiv preprint, 2026').

Credibility flag: criterion (iii) requires the task count, and neither v3 nor v1 states the number of tasks evaluated per benchmark. The benchmarks and models are stated. Under a strict reading of the rule, PASTE's numbers do not qualify until a task count is found; Edwin to decide.

**formula:**

No speedup or cost formula. The scheduling rules (§4.3) are:
- priority(i) = ExposedToolGain(i) / LLMPressure(i, load) + Aging(i)
- EnginePressure(B) = DecodeLoad(B) + γ·KVLoad(B), kept within P_low ≤ EnginePressure(B) ≤ P_high

## 34. DualSpec

**read:** arXiv:2603.07416v1 PDF (8 Mar 2026; the only version): https://arxiv.org/pdf/2603.07416v1

**verdict:** corrected

**effect:**

Table 2 (§6.3.1) figures are confirmed. The table's stated purpose is to fix verification and vary only the drafting scheme; 'Heterogeneous' is DualSpec's drafting.
- MiroThinker 72B+8B, GAIA: Origin (base model with full reasoning) 63.1 acc / 1041 latency → 63.1 / 605.
- MiroThinker 72B+8B, XBench: 66 / 1007 → 66 / 480.
- Qwen3 32B+4B, GAIA: 29.1 / 80 → 30.1 / 46.
- Qwen3 32B+4B, XBench: 27 / 69 → 27 / 41.

Table 2 does not state the latency unit or whether it is a per-task mean; Fig. 7's axes are labelled 'Latency (s)'. Calc. speed-ups: 1.72×, 2.10×, 1.74×, 1.68×.

Correction: 'up to 3.28×' is the paper's own claim, not only Gemini's. It appears in the abstract, the Fig. 7 caption (1.33–3.28×, about 2× on average) and §6.2. Per model pair, §6.2 gives 1.8× for 72B+8B, 2.6× for 72B+30B-A3B and 1.5× for Qwen3-32B+4B. The configuration that reaches 3.28× is shown only in Fig. 7 and not named in the text.

Setup (§6.1):
- One A100 per model, batch size 4, SGLang.
- MiroThinker quantised to 4-bit; Qwen in native FP8.
- Search via the Bing API; Visit via Jina; MiroMind framework over MCP.
- Benchmarks: GAIA-Text-103, XBench-DeepSearch and Seal-0. Task counts for the last two are not stated.
- The verifier threshold τ was tuned on a held-out GAIA split for about 20% intervention.
- Accuracy is pass@1; cost and tokens are not reported.

**mechanism and term:**

Corrected: the recorded 'overlap saving introduced' is not the main mechanism.

At each step, two drafts are produced in parallel (§5.1–5.2):
- a System-2 draft: a small model WITH reasoning, kept for Search actions;
- a System-1 draft: the large base model SKIPPING reasoning, used for Visit.
If the small model's reasoning trace exceeds τ_think, its full draft is kept.

The chosen draft is then judged by the base model acting as a Yes/No critic. The score is log p_acc − log p_rej, and the draft is accepted if the score ≥ τ. Otherwise the step falls back to full-reasoning regeneration (§5.3).

The paper frames the saving as removing large-model reasoning from the critical path (§7). It does not describe overlapping tool execution with model reasoning.

Term mapping:
- Decode smaller: the base model's long reasoning is skipped on roughly 80% of steps.
- Price/tier (model choice): a small model drafts Search steps.
- c_k larger: two drafts plus a critic call per step, plus fallback on about 20% of steps.
- Success rate at risk: semantic acceptance is lossy, so accepted actions can differ from the base model's; pass@1 is reported as comparable (e.g. 63.1 → 63.1).
- Overlap: only between the two drafts.

**authors and venue:**

Authors confirmed on the arXiv PDF: Zhong (work done as an intern at Microsoft Research), Lu, Chen, Liu, Yang, Li. Institutions: Peking University, Microsoft Research and Microsoft. This is a preprint with no venue ('Preprint. March 10, 2026').

Credibility check (not in doc2 or references.md):
- (i), (ii) and (iv) pass.
- (iii) passes for GAIA-Text-103 (103 tasks, model stated).
- For XBench-DeepSearch and Seal-0 the task count is not stated in the paper, so under a strict reading the XBench 1,007→480 row fails (iii) unless the count is sourced elsewhere.

**formula:**

No speedup or cost formula. The paper's formulas are an entropy proxy and the verifier score:
- mean token-level entropy H̄(a|s) = (1/n) Σ_{i=1}^{n} (−log p(t_i | s, t_<i)) (Eq. 2)
- E[H̄(a|s) | a∈A_SEARCH] > E[H̄(a|s) | a∈A_VISIT] (Eq. 3)
- E_{z∼π(·|s)}[H(π(·|s,z))] ≤ H(π(·|s)) (Eq. 5)
- score(s_t, z_t, a_t) = log p_acc(s_t, z_t, a_t) − log p_rej(s_t, z_t, a_t) (Eq. 6)
- accept if score ≥ τ (Eq. 7)

## 35. Speculative Macro Commit (SMC)

**read:** arXiv:2609.03236v1 PDF (3 Sep 2026; the only version): https://arxiv.org/pdf/2609.03236v1 ; arXiv abs page comments field ; MLSP 2026 searchable schedule data https://neuroneural.net/mlsp2026schedule/data/papers.json , linked from the official https://mlsp26.ieeesps.org/detailed-schedule/ (read 28 Sep 2026). OpenReview (MLSP 2026 group) returned a bot challenge, which I did not attempt to get past.

**verdict:** confirmed

**effect:**

Table 1 (§4.2): latency is average seconds per task; Δ is relative to the sequential baseline.
- τ² Telecom: Baseline 99.52 / 27.60 s; SA 99.47 / 25.03 (−9.31%); SMC 99.52 / 22.47 (−18.59%). SMC is −10.23% vs SA.
  - Per-task outcomes are identical to the sequential run: 2,274 correct and 11 incorrect in both, so 2,285 tasks (calc.).
  - Relative to SA, SMC fixes 1 task and regresses none.
- AppWorld: Baseline 41.67 TGC / 355.7 s; SA 41.67 / 212.1 (−40.37%); SMC 40.48 / 195.9 (−44.93%).
  - Task-goal completion falls from 70/168 to 68/168 tasks (−1.19 pp, calc.).
  - SMC vs SA is −7.64% in §4.2 and the contributions list, and '7.7%' in the abstract. Note that most of the AppWorld gain comes from single-step SA.
- Table 3: on the 143 same-accuracy AppWorld tasks, SMC vs SA is −13.5%; NTC-free subset −10.7%.

Table 2 (coverage): commit rate 62.0% (AppWorld) / 86.2% (Telecom). Macro hits 219 / 3,352; skipped steps 512 / 7,154; skip density 3.81% / 3.91% (= skipped steps ÷ (tasks × max_steps)). §4.3 defines commit rate as a task share: "SMC commits at least one macro on 62.0% of tasks". This quote replaces E124's 'tool paraphrase' caveat.

Table 5 (100 held-out τ² Telecom tasks, event-level exact match): library match alone 681/1,968 (34.6%); + drafter-executed 70.6%; + verified anchor 87.9%; + depth guard (L_min=1) 90.4%; actually fired 158/158 outcome-preserving.

Table 4 (single GPU): passive commit −11.34% latency but accuracy 96.48%; AWO-like meta-tools +1.05% latency.

Setup (§4.1): actor Qwen3.5-27B INT4, drafter Qwen3.5-4B, greedy decoding. The sequential baseline uses 1 GPU. SA and SMC use 3 GPUs: the actor, an actor-class replica serving speculative requests, and the drafter. GPU type and serving engine are not stated.

Correction to 'vs Speculative Actions': SA here is SMC's own 'SA-only' configuration — the same executor with the macro-commit rule disabled, on the same 3 GPUs (§3.1). It is not Ye et al.'s implementation.

**mechanism and term:**

Right. The drafter runs ahead and executes a draft chain in an isolated draft state. Recurring skeletons are mined offline and filtered by a Beta-posterior lower quantile. When the actor's next call matches q1 (the anchor), q2…qℓ are committed with their observations, without actor confirmation, if the depth floor and online checks pass. In AppWorld those checks include API-name rules that reject irreversible or unknown calls, and a live-state replay for forkable mutations (§3.2–3.3).

Terms:
- Overlap saving introduced: the drafter's pre-execution overlaps the actor's decisions.
- N (actor passes) smaller: ℓ−1 actor decisions are skipped per commit, but only 3.8–3.9% of the step budget.
- Environment wait hidden: already-returned tool results are not waited for again.
- Money: GPU-hours larger (3 GPUs vs 1 for sequential; equal hardware vs SA).
- Success rate: unchanged on τ² Telecom; −2 of 168 tasks on AppWorld.

SMC is approximate, not lossless; the authors say so explicitly (§1–2).

**authors and venue:**

Authors confirmed: Zeyu Liu and Peter A. Beerel (University of Southern California), Souvik Kundu (Intel Labs, San Diego).

Venue: now confirmed as IEEE MLSP 2026 (IEEE International Workshop on Machine Learning for Signal Processing, Atlanta, 28 Sep–1 Oct 2026), poster. Evidence:
- The arXiv abs comment reads 'Accepted in MLSP2026'. This field was unreadable when the 27 Sep check ran (dossier §6 item 13d).
- The PDF carries the MLSP 2026 running head and an IEEE copyright line (979-8-3195-0884-3/26/$31.00 ©2026 IEEE).
- The official schedule lists submission #184 in Poster Session 3, Thu 1 Oct 2026, 13:00–15:00, theme 'Agentic & Multimodal Learning', with an OpenReview forum Rzj4sZ6h8H.

Under references.md's rule ('the official venue page or the arXiv page'), this counts. Re-label SMC as a workshop paper (IEEE MLSP 2026) rather than a preprint. IEEE Xplore proceedings are not yet checked. It passes the source-credibility rule either way.

**formula:**

No speedup or cost formula. The formulas given are:
- Macro reliability (§3.2, Eq. 1): p_m = F^{-1}_{Beta(k_m+1, n_m−k_m+1)}(δ), with m retained only if n_m ≥ n_min and p_m ≥ τ. Here n_m = labelled opportunities and k_m = correct drafter proposals.
- Commit depth (§3.3): skips ℓ−1 actor decisions, with the candidate requirement ℓ−1 ≥ L_min.
- Skip density (Table 2): skipped steps ÷ (tasks × max_steps).

## 36. AgenticCache

**read:** https://arxiv.org/pdf/2604.24039v1 (v1, 27 Apr 2026, the only version), read in full. I also read the MLSys 2026 camera-ready PDF https://proceedings.mlsys.org/paper_files/paper/2026/file/c66a9db149261435664284a20b6f1d42-Paper-Conference.pdf. Its text matches arXiv v1 except for line breaks in the references. The proceedings abstract page (the dossier's link) was read on 2026-09-28.

**verdict:** confirmed

**effect:**

All numbers match exactly; conditions added below. Source: Table 2 (§5.3, p. 6), GPT-5 planner, warm start ('Ours+'). Caption: 'SR: success rate; L: latency (hours); T: token usage; C: cost (USD)'. TDW-COOK: synchronous Baseline 94.44% / 12.86 h / 3.3M / $21.0 -> AgenticCache 100% / 1.75 h / 675K / $4.4. TDW-MAT: 90.23% / 41.34 h / 5.8M / $40.5 -> 88.64% / 22.27 h / 4.1M / $27.7. §5.3 prose: 'latency drops from 12.86 hours to 1.75 hours (7.4×)' and cost '$21.0 to $4.4 (4.8×)'. TDW-MAT works out to 1.86x on latency and 1.46x on cost (calc.). CONDITIONS. Evaluation set (§5.1): 18 episodes on TDW-COOK and 44 on TDW-MAT. The cache is prefilled from 2 and 4 disjoint training episodes, using GPT-5 trajectories on out-of-distribution tasks (§4.3). Both tasks run 2 decentralized agents in ThreeDWorld (Table 1). The baselines are the authors' own reimplementations: a streamlined COMBO (one VLM call and one diffusion call instead of beam search) and CoELA with ReCA's planning-then-communication. 'L' is 'simulation latency' (abstract), which includes environment execution. The paper does not say whether it is summed over the evaluation episodes. Cost is 'measured input and output token counts multiplied by OpenAI's listed per-token prices' (October 2025). Hardware: one RTX 4090 plus a Ryzen 9 7950X workstation. Headline over 12 configurations (abstract): task success rate +22% on average, 'reduces simulation latency by 65%', tokens -50%. Cache hit rate on TDW-COOK is only 39-46% (§5.5), and each miss costs 9-29 s of fallback on TDW. Cold start with no prefill (Tables 3-4, CoELA): standard tasks, GPT-5: 5.06 -> 2.63 h, $5.32 -> $3.94, success 90.0 -> 93.3%. Long-horizon tasks, GPT-5: success 82.2 -> 80.6%.

**mechanism and term:**

The mechanism is correct. Each agent keeps a 2-gram plan-transition cache, filtered by metadata ranges and scored by count × importance. A background Cache Updater queries the LLM from time to time, confirms or corrects the cached choice, and can replace the plan being executed. Further queries are suppressed after a confirmation or a correction. On a cache miss, planning pauses and the LLM is called synchronously. TERMS. (1) c_k smaller: correct in the sense of blocking calls. On a hit the agent does not wait for any model call. (2) Overlap saving: correct, and the central mechanism. The updater's LLM call runs while cached plans execute (Fig. 3d). (3) Money smaller: correct. Tokens fall 3.3M -> 675K on TDW-COOK with GPT-5 and by -50% on average. (4) Success rate: not uniformly preserved. TDW-MAT drops for every model (GPT-5 -1.59 pp, GPT-5-mini -1.13 pp, GPT-5-nano -3.64 pp; calc.), and GPT-5 long-horizon cold start drops -1.6 pp. So write 'success rate mostly kept, up on TDW-GAME and BEHAVIOR-1K', not 'kept'. N (the number of plan executions) and prefill/decode per call do not change. The 7.4x on TDW-COOK is the best case; TDW-MAT is 1.86x. The domain is embodied multi-agent simulation (ThreeDWorld, BEHAVIOR-1K), not web or GUI. Proposed D-entry (next free D157 per STATUS.md; git fetch before allocating): the §3.2 row should state 'simulation latency, unit hours, per-episode or total not stated; the authors' reimplemented baselines; success −1.1 to −3.6 pp on TDW-MAT'.

**authors and venue:**

Confirmed. Hojoon Kim (Seoul National University), Yuheng Wu and Thierry Tambe (Stanford University), per the paper's affiliation footnote and the arXiv metadata. arXiv comment: 'Accepted at MLSys 2026'. The official proceedings page lists it under 'Proceedings of Machine Learning and Systems 8 (MLSys 2026)', Conference track, with the same three authors. It is a conference paper, so the preprint rule does not apply; cite the proceedings version. Code: github.com/hojoonleokim/MLSys26_AgenticCache. It is not in references.md yet.

**formula:**

There is no speedup or cost formula. The paper gives only the cache's selection rule (§4.1): P* = argmax_{Pj∈F(Pi)} S(Pi→Pj), with S(Pi→Pj) = C(Pi→Pj) · I(Pj) and I(Pj) = N_conf(Pj)/N_cand(Pj). The feasible set is F(Pi) = {Pj | s_t ∈ [s_ij^min, s_ij^max], h_t ∈ [h_ij^min, h_ij^max]}. Table 5 caption gives the cache size as N × (4 + Σ_{i=1}^{M} s_i) bytes. Cost is defined in words only (§5.1): measured tokens × OpenAI list prices.

## 37. Executable Agentic Memory for GUI Agents (EAM)

**read:** https://arxiv.org/pdf/2605.12294v1 (v1, 12 May 2026, the only version), read with pdftotext. Page 6 was rendered to read Eq. 14.

**verdict:** corrected

**effect:**

The numbers are right; the condition 'aggregated across mobile benchmarks' is not in the paper. Table 2 (§6.2, p. 7): 'Latency (s)' is defined as 'average execution time per step'. 'API Tokens Cost (K)' is 'total token consumption (in thousands) per step for LLM API calls'. GPT-4o: 9.3 s / 50.8K; EAM: 2.8 s / 8.3K. Text: 'average latency of 2.8 s and token cost of 8.3K per step', and 'reducing token cost by approximately 6× compared to GPT-4o (50.8K)'. The paper never says which benchmark, or which mix, Table 2 was measured on, and gives no run count for it. Success rates (Table 1, 'averaged over three independent runs'; SoM input): AndroidWorld (116 tasks, 20 apps) GPT-4o 34.5% -> EAM 52.6%; MobileMiniWob++ (92 web tasks) 56.5 -> 76.1%; DroidTask (158 tasks, 13 apps) 57.0 -> 86.1%. Baselines that beat EAM: AppAgentX (GPT-4o) scores 62.5% on AndroidWorld, above EAM. AutoDroid-V2 is faster per step (2.1 s). M3A scores 40.5% at 16.9 s. The abstract's 'up to 19.6%' is percentage points versus UI-TARS-7B (52.6 − 33.0). EAM configuration: UI-TARS-2B as the local executor, a fine-tuned Qwen2.5-Instruct path extractor (0.5B, 1.5B or 3B), GPT-4o for exploration and knowledge mining, and one cloud call per task to filter the extracted paths. Inference runs on one RTX 4090; training used 4×A800 for 4 self-training rounds. The cost and time of exploration, graph construction and training are not reported anywhere, so 'prep excluded' is accurate but should read 'not reported'. A table quirk: UI-TARS-7B shows 32.7K API tokens although the caption says local models are marked '-'.

**mechanism and term:**

The mechanism is correct. State-aware DFS exploration and BPE-style action-group mining build an app-wise GUI knowledge graph. MCTS over that graph, steered by a Q-model, extracts the top-K paths. A single cloud LLM call filters and parameterizes the plan, and a local 2B model executes it (plan-then-execute). TERMS, corrected. (1) c_k: cloud model calls go from one per step to one per task. That is a structure change, not just a smaller number. (2) Price/tier: missing from the given mapping, and the main lever. Per-step decisions move from GPT-4o to small local models. (3) Prefill: API tokens per step fall from 50.8K to 8.3K. How one call per task is turned into a per-step figure is not stated. (4) Per-step time: 9.3 -> 2.8 s (3.3x, calc.), benchmark unstated. (5) Success rate: up against the plain GPT-4o agent, but not the best in the table (AppAgentX 62.5%). N: action groups compress multi-step routines, but no step counts are reported. The setting is mobile Android GUI, not web. Limitations section: the method assumes a relatively static UI, and the graph goes stale when apps update. Proposed D-entry: the §3.2 row should replace '(aggregated across mobile benchmarks; prep excluded)' with 'per-step, benchmark not stated; offline exploration/training cost not reported; AndroidWorld SR 52.6% < AppAgentX 62.5%'.

**authors and venue:**

Zerui Qin, Sheng Yue, Xingyuan Hua, Yongjian Fu and Ju Ren. Institutions per the paper's marks: 1 = Tsinghua University (Qin, Hua, Fu, Ren), 2 = Sun Yat-sen University (Yue). The arXiv metadata lists the same five authors. It is a preprint ('Preprint. May 13, 2026'), with no arXiv comment and no venue. Credibility rule: (i) and (ii) pass. (iii) passes for the success rates (public benchmarks, task counts and models stated). The latency and token numbers must carry the note 'benchmark not stated'. (iv) passes. It is not in references.md yet.

**formula:**

There is no speedup or cost formula, only a bound on search cost. Theorem 5.3, Eq. 14 (p. 6): n ≥ 32(K−1)c² ln(Hn/δ) / Δ_eff² + 2(K−1)(2N₀ + π²/3) MCTS simulations per node. This gives a total complexity N_total = O(HKc² ln(Hn/δ) / (Δ*_min − 2ε_bias)²) + O(HKN₀). Symbols: Δ_eff := Δ*_min − 2ε_bias; K = max_s |A(s)|; c is the UCT exploration constant; N₀ is a burn-in threshold. The bias bound ε_bias is Eq. 13.

## 38. Speculate with Memory

**read:** https://arxiv.org/pdf/2607.12236v1 (v1, 14 Jul 2026, the only version), read in full including Appendices A.4, A.9 and B.4.

**verdict:** confirmed

**effect:**

All numbers match; one figure needs a label (next paragraph). Abstract: '19–39% relative accuracy improvement on action prediction' and 'up to a 2.5× increase on observation prediction tasks'. Table 2 (k=1): WebArena (812 tasks) read-only action match 19.8 -> 23.7% (+19.7% relative, calc.). VWA (910) 12.5 -> 17.4% (+39.2%). ALFWorld (134 valid_unseen) observation exact match 16.3 -> 40.0% (2.45x). PDDL (60) 17.6 -> 33.8%. τ²-bench retail+airline (164) 12.7 -> 19.9%. HotpotQA (300) 20.5 -> 27.5%. Table 2 caption: all improvements significant, 'p < 0.001, McNemar's test over all evaluation steps'. Setup (§3.1): 'Actor trajectories are collected once and replayed.' Actor is GPT-5.4 on ALFWorld, PDDL, τ²-bench and HotpotQA, and GPT-5-mini on WebArena and VWA. The speculator is GPT-4.1-mini, with n = 3 instances per setting. Fig. 1 (right): an ALFWorld 'estimated latency reduction', 'counting each correct speculation as hiding the latency of one actor LLM call', rises from ~28% (stateless) to over 50% after 120 episodes. §4.3 live validation, HotpotQA: actor median 4.9 s, speculator 1.7 s, 40.0% hit rate over 610 speculated steps, 'yielding a 1.05× analytical speedup and saving 892 s over a 19,024 s baseline' (−4.7%, calc.). ALFWorld live: 44.9% observation hit rate over 1,638 steps. NEW: in App. A.9 the authors measure ALFWorld latencies and compute end-to-end speedup analytically for an injected environment delay: 1.003x at 2 s, 1.085x at 5 s, 1.119x at 7 s, 1.128x at 10 s (the peak), 1.095x at 20 s. Proposed D-entry: Fig. 1's '>50%' is the share of actor-call latency hidden. It is not wall-clock time. The paper's own end-to-end figure peaks at 1.128x, an 11.3% reduction (calc.). The deck must not show '>50%' as a wall-clock result. App. B.4 still says a live study 'is necessary' (the dossier already records this inconsistency).

**mechanism and term:**

The mechanism is correct. A contrastive transition table, an episodic memory (including miss episodes) and a confusion tracker, all updated online after each task, give the speculator better predictions. Commit only on an exact match; Types 1 and 3 may pre-launch only whitelisted read-only actions. TERMS. (1) Overlap saving: correct. A higher hit rate raises the fraction of steps whose action (Type 1) or next actor call (Type 2) was pre-launched during idle time. The saving per hit is capped by the min(...) terms, so it is bounded by the idle window. (2) Success rate: preserved by design in replay, because the actor's trajectory is identical. B.4 notes that in a live deployment the changed timing could alter the context. (3) CORRECTION: money goes up, not flat. Every step adds speculator calls, and memory adds 200–500 input tokens per call (+$0.01–0.02 per 100 steps, A.4). For Types 2 and 3 each miss wastes a pre-launched actor call. The paper gives the 'net expected additional cost' as k·C_S + (1 − acc)·C_act. At acc ≈ 40% that is roughly 0.6·C_act extra (calc.). (4) Price/tier: the speculator is a cheaper model, and a speculator call is '10–70× cheaper than the actor call'. N, c_k, prefill and decode of the actor do not change.

**authors and venue:**

Confirmed. Yu Li, Qinyuan Ye, Prafulla Kumar Choubey, Jiaxin Zhang and Chien-Sheng Wu, all Salesforce Research (salesforce.com addresses on the paper). This matches the arXiv metadata and references.md l.80 (full title: 'Speculate with Memory: Lossless Acceleration for LLM Agents'). Preprint, no venue. The rule passes (public benchmarks with task counts and models stated). All speed figures are replay-based estimates, or analytical figures built on measured per-call latencies, and must be labelled that way.

**formula:**

§2.1: the realized saving per hit is min(ℓ_env, ℓ_LLM − ℓ_spec) for action prediction (Type 1) and min(ℓ_LLM, ℓ_env − ℓ_spec) for observation prediction (Type 2). For chained prediction (Type 3) it is 'up to ℓ_LLM + ℓ_env'. With k parallel speculators, best-of-k. §4.3: net expected additional cost = k·C_S + (1 − acc)·C_act (Types 2 and 3). App. A.4 (Table 6, per 100 steps): estimated latency reduction = acc × ℓ_hit × 100. There ℓ_hit is set to ℓ_env for Type 1, min(ℓ_LLM, ℓ_env − ℓ_spec) for Type 2, and ℓ_LLM − ℓ_spec for Type 3. The Type 1 and Type 3 settings differ from the §2.1 forms. App. A.9: 'per-hit savings, defined as min(ℓenv − ℓspec, ℓactor)'.

## 39. Log2Plan

**read:** https://arxiv.org/pdf/2509.22137v1 (v1, 26 Sep 2025, the only version), read with pdftotext; pages 6 (Table 1) and 8 (Figure 6) were rendered and viewed. I also read the Crossref metadata for DOI 10.1145/3746059.3747663. The ACM DL version of record could not be read (HTTP 403 via curl and via WebFetch).

**verdict:** confirmed

**effect:**

The conflict is real as recorded. Table 1 (p. 6), columns 'Execution Time ↓ (sec/task)' and 'Success Rate ↑ (%)': React-style Planner 28.6 / 18.0; UFO2 118.2 / 46.5; Log2Plan w/o TM 44.2 / 28.0; Log2Plan 80.0 / 61.7. The §5.2 prose says 'highest success rate (80.0%)' with 'reasonable completion time (61.7 sec)'. CONDITIONS (§5.1): 200 real-world GUI tasks, made of 100 in-house tasks plus 50 sampled from the Skyvern dataset (639 total) and 50 from ScreenAgent (70 sessions). They cover Windows desktop, web, app and cross-app tasks. GPT-4o is the planner. Task mining uses about 20 h of the authors' own GUI logs (141 log files). UFO2's backing model and the number of runs are not stated. Table 2: average subtask completion 93.4% for Log2Plan versus 62.8% for UFO2. NEW EVIDENCE (calc., read off Figure 6 on p. 8; approximate). The bins by low-level action count hold 2 / 27 / 65 / 51 / 32 / 18 / 5 = 200 tasks. Log2Plan's success is at least 60% in every bin, and roughly 90–100% in the three shortest bins (94 tasks). The weighted mean is therefore about 80% (lower bound about 74%). That fits 80.0% and cannot give 61.7%. The same read-off gives a mean time of about 67 s, closer to 61.7 than to 80.0. Read the same way, UFO comes out at ~47% and ReAct at ~18%, matching Table 1, which checks the read-off method. So Table 1's Log2Plan row is probably transposed and the prose is right. This is not confirmed, because the ACM version could not be read. Either way, Log2Plan is slower than the ReAct-style planner (28.6 s) and than its own ablation without task mining (44.2 s). It is faster only than UFO2: −48% if 61.7 s, −32% if 80.0 s (calc.). The Conclusion's 'faster execution times than the baseline models' holds only against UFO2.

**mechanism and term:**

The mechanism is correct. Offline, GPT-4o segments and labels user GUI logs into a task dictionary (task mining). The GlobalPlanner turns a command into a task list using retrieved task groups. The LocalPlanner grounds each task block into low-level actions for the current screen, and PyWinAuto/PyAutoGUI execute them. TERMS, corrected. (1) The primary effect is success rate: 18.0–46.5% for the baselines against 80.0% (or 61.7%, given the conflict). (2) 'N smaller' is plausible from the design, since the model is called per task block and not per low-level action. But the paper reports no step, call or token counts, so this is an inference, not a measurement. (3) Time falls against UFO2 but rises against a ReAct planner. So as an acceleration work it is a success-rate method with a time benefit only against UFO2. (4) Money: no cost is reported, and neither is the cost of the offline mining. Proposed D-entry: record the Figure 6 evidence (calc.) in favour of the prose; keep the item open until the ACM version of record can be read.

**authors and venue:**

Seoyoung Lee, Seobin Yoon, Seongbeen Lee, Hyesoo Kim and Joo Yong Sim, all Sookmyung Women's University. This is per the arXiv author block and the Crossref affiliations (departments: Software Convergence, Data Science, Mechanical Systems Engineering, CSE). The venue is confirmed by Crossref: DOI 10.1145/3746059.3747663, 'Proceedings of the 38th Annual ACM Symposium on User Interface Software and Technology' (UIST '25, Busan), pp. 1–13, published 27 Sep 2025. The arXiv PDF's ACM block has placeholders (ISBN 978-1-4503-XXXX-X/2018/06, DOI XXXXXXX) and the arXiv page has no comment, so the venue rests on Crossref and ACM DL, not on the template. It is a conference paper, so the preprint rule does not apply. Note that half of the 200 tasks are in-house and not public. It is not in references.md yet.

**formula:**

None. The only structural notation is the task tuple g_i = [user-assist, high-level action, object]. No time or cost formula appears.

## 40. Skim / Accio

**read:** https://arxiv.org/pdf/2605.16565v2 (v2, 19 May 2026, the latest), read in full. I compared it with v1 (https://arxiv.org/pdf/2605.16565v1, 15 May 2026, titled 'Accio: …'). v2 renames Accio to Skim and rewrites the abstract; the headline numbers are the same in both.

**verdict:** corrected

**effect:**

The headline is confirmed; the aggregate-mode figure and the task count need conditions. v2 abstract: 'Skim reduces median per-task cost by 1.9x and latency by 33.4% with no accuracy loss'. The paired backends are WebVoyager, AgentOccam and BrowserUse. §1 adds that aggregate mode lifts accuracy 'by up to 16.7 percentage points (4.2 pp with majority vote)'. §5.2 narrows this to WebVoyager with AgentOccam, about 4 extra trajectories per task, and 16.7 pp as 'upper-bound wins (i.e., assuming oracle selection of the best trial)'. SETUP (§4, §5.1). Benchmarks: WebVoyager (15 live sites) and WebShop, 'a representative subset of 300+ tasks randomly drawn across the two benchmarks'. The exact count and the split between benchmarks are not stated. Each task runs on every backend, and the backends use GPT-4o. The fast path and the verifier run Qwen2.5-14B-Instruct locally on vLLM. Latency and cost are 'measured over complete task executions including failures and cascades'. I found no statement of how local-model inference is priced. Table 2 accuracy, Skim versus the default agent: WebVoyager 40.6 vs 37.6; AgentOccam 52.0 vs 49.6; BrowserUse 45.6 vs 45.0. §2.2: hand-engineered programs for 'nine representative tasks' in WebVoyager are 66.7–94.9% faster and 17.7–100.7x cheaper. §2.3: naive substitution 'drops average task success by 60%'; whether that is relative or percentage points is not stated. E17 is re-confirmed (§2.2): 151 WebVoyager tasks, 3 agents, median delays of 4.7 s LLM and 6.6 s browser, 66.7% of steps purely navigational for the median task. One text quirk: 'median task takes 4 steps with 80% of tasks requiring at least 7 steps' is internally inconsistent. Verifier (§5.3): 82.0% precision and 86.2% recall, measured against a frontier-model verifier. Offline profiling takes about 6–24 s per site (Fig. 21) and is not included in the per-task numbers. Scope: read-only information retrieval only; state-mutating tasks go straight to ReAct.

**mechanism and term:**

The mechanism is correct. An offline per-site profile records URL templates, search semantics and answer schemas. At run time Skim routes the task, synthesizes the URL, fetches it over HTTP, cleans the HTML and extracts with a small model. A verifier checks the result; on rejection the task escalates to full ReAct, warm-started at the fast path's URL. TERMS, corrected. (1) 'Overlap (speculative execution)' is WRONG. Skim's speculation is a sequential cascade: guess, verify, then fall back. The text describes nothing running concurrently in accelerate mode (it never says 'parallel' or 'concurrent'), so the overlap saving does not change. A misspeculation adds the fast-path and verifier time (~3 s routing, 2–3 s URL synthesis, ~1 s verification) before the fallback. (2) N smaller: correct. The navigation passes collapse into one synthesized fetch. (3) Environment smaller: correct. An HTTP fetch takes 100–300 ms instead of browser rendering, with fewer page loads. (4) Price/tier: correct. Qwen2.5-14B runs locally instead of GPT-4o for extraction and verification. (5) Prefill smaller: extraction reads condensed HTML. (6) Success preserved (Table 2). Aggregate mode instead spends the savings on success rate: +4.2 pp by majority vote, 16.7 pp only as an oracle upper bound. Proposed D-entry: '+16.7 pp' must be labelled as an oracle upper bound; drop 'overlap' from Skim's terms; the task count is '300+'.

**authors and venue:**

Mike Wong and Ravi Netravali (Princeton University); Kevin Hsieh and Suman Nath (Microsoft Research, Seattle). Confirmed on the arXiv metadata and the PDF. It is a preprint. The PDF header 'Conference'17, July 2017, Washington, DC, USA' is an ACM template placeholder, not a venue. The v1 title was 'Accio: Speculative Execution for Fast and Efficient Web Agents'. Credibility rule: (i), (ii) and (iv) pass. For (iii), the benchmarks are public and the model is stated, but the task count is only '300+'. E17's 151 tasks is an exact count. references.md l.45 is correct.

**formula:**

None. The paper gives no speedup or cost formula, only medians and CDFs (Figs. 15–16).

## 41. PEEK orientation cache

**read:** https://arxiv.org/pdf/2605.19932v1 (v1, 19 May 2026, the only version), read in full including App. C (Tables 4–7), G and H.

**verdict:** corrected

**effect:**

The numbers are confirmed. The units, the comparator and the cost against the base agent need fixing. Abstract: 'improves over strong baselines by 6.3–34.0% while using 93–145 fewer iterations and incurring 1.7–5.8× lower cost than the state-of-the-art prompt-learning framework, ACE'. On CL-bench: '6.0–14.0% and 7.8–12.1%' (solving rate / rubric accuracy) 'at 1.4× lower cost than ACE'. Table 1 uses GPT-5-mini-2025-08-07, with every method built on RLM. RLM / ACE / PEEK: TREC-coarse 30.3 / 48.8 / 58.1; AGNews 46.5 / 61.6 / 69.4; Yahoo 23.0 / 42.0 / 57.0; CL-bench solve 14.0 / 20.0 / 26.0 and rubric 54.5 / 53.5 / 63.4. The caption calls the subscripts 'absolute improvement', so the '%' figures are percentage points. The 6.3 is PEEK minus RAG on AGNews; the 34.0 is PEEK minus RLM on Yahoo. Iterations (App. C, 'Total # iterations', summed over all tasks of a split; RLM caps each task at 30 iterations): ACE 523 / 491 / 487 against PEEK 378 / 398 / 349 on TREC / AGNews / Yahoo. That is 145 / 93 / 138 fewer; base RLM is 394 / 496 / 347. Cost ('execution cost and method-specific overhead'; GPT-5-mini at $0.25 / $2.00 per 1M tokens): ACE vs PEEK is $29.42 vs $5.10 on TREC (5.8x), $5.20 vs $2.30 on AGNews (2.3x, calc.), $4.10 vs $2.39 on Yahoo (1.7x, calc.) and $2.63 vs $1.88 on CL-bench (1.4x). NEW: against the base RLM with no memory, PEEK costs more on all four: $5.10 vs $5.02, $2.30 vs $2.24, $2.39 vs $0.93, $1.88 vs $1.57. That is 1.02–2.57x (calc. from Tables 4–7). Map maintenance adds $0.22–0.43 per benchmark run. The number of tasks and contexts per split is not stated anywhere I searched. No wall-clock time is measured. The default map budget is B = 1024 tokens, and the map is updated only for the first m ≤ 4 queries.

**mechanism and term:**

The mechanism is correct. A Distiller reads each trajectory, a Cartographer turns that into ADD / DELETE / REPLACE edits, and a priority Evictor enforces a hard token budget B. The map sits in the system message of every run on the same recurring external context. TERMS, corrected. (1) Context growth: WRONG as a 'structure change'. Within a task, RLM still appends each REPL result (truncated to 20,000 chars) to its history. The map only replaces cross-query carried history, and only relative to the Shared Chat baseline, whose input tokens inflate 10.1x on TREC. Against the base RLM it adds B tokens to every prompt, so it does not remove N² growth. (2) N smaller: correct against ACE (93–145 fewer iterations on OOLONG). Against the base RLM the drop is small (−4.1%, −19.8%, −2.9%, and +0.6% on Yahoo; calc.). The mechanism is skipping the 'first several iterations' spent orienting in a known context. (3) Success rate up: correct, and the main effect. (4) Money: lower only than ACE or Shared Chat. It is higher than the base agent, because of the maintenance calls and the map tokens. The domain is long-context document QA through a REPL agent, not GUI or web. Proposed D-entry, extending D125: '%' means points; cost against the no-memory agent is +2% to +157%; the context map is not a history replacement.

**authors and venue:**

Zhuohan Gu, Omar Khattab and Samuel Madden (MIT CSAIL); Qizheng Zhang (Stanford University). This is per the paper's affiliation block (1 = MIT CSAIL, 2 = Stanford), so write 'MIT/Stanford', with three of the four authors at MIT. The arXiv metadata lists the same four names. Preprint, no venue. Code: github.com/zhuohangu/peek. Credibility rule: (i), (ii) and (iv) pass. For (iii), the benchmarks are public (OOLONG splits trec_coarse, agnews and yahoo; CL-bench) and the model is stated (GPT-5-mini), but the task and context counts are not. As the rule is written, it fails (iii) unless named benchmark splits are accepted as enough; Edwin should decide. It is not in references.md yet.

**formula:**

There is no speed or cost formula. The only formulas are OOLONG's scoring rule, taken from the original paper, score(ŷ) = 0.75^|y−ŷ| for numerical answers and exact match otherwise (§4.1), and Algorithm 1, the cache-policy loop over n tasks with budget B and m evolve steps. Cost is computed from token counts × the listed per-model prices in App. H, stated in words.

## 42. Qwen-UI-Agent

**read:** arXiv:2607.28227v1 (30 Jul 2026), PDF https://arxiv.org/pdf/2607.28227v1 via pdftotext, plus the project-page PDF https://tongyi-mai.github.io/Qwen-UI-Agent/Qwen-UI-Agent-Technical-Report.pdf (dated 2026-07-29, stamped arXiv:submit/7884825). A diff of the two shows only three differences: the abstract wording, the batched share in the intro bullet (project PDF says more than 30%, arXiv v1 says over 40%), and one OSWorld-v2 figure in the conclusion (40.2 vs 40.0). Quotes are paraphrased because of a quoting limit; all figures are exact.

**verdict:** corrected

**effect:**

Primary model is Qwen-UI-Agent-27B; 35B-A3B and 4B variants also exist. MobileWorld 82.1%: GUI-only subset of 117 tasks, standard 50-step budget (Table 2, p.22). It rises to 85.5% at 100 steps; the 35B-A3B scores 65.0%. OSWorld-Verified 79.5% (Table 4, p.25), second behind Opus 4.8 at 83.4%. The text says this benchmark measures partial progress over 361 tasks, while the table header says success rate. WebArena 73.6% (Table 6, p.27): before scoring, the authors manually corrected wrong reference answers and errors in the official evaluation scripts (p.26), and they re-ran the starred baselines under that setup. So it is not comparable to official-scorer WebArena numbers, and no task count is given there. Batched share: the intro bullet (p.4, arXiv v1) says over 40% of action outputs are batched; the 29 Jul project PDF says more than 30%. Table 11 (p.35), action level: 39.6% of actions batched on OSWorld-Verified and 41.6% on OSWorld-v2. Tasks using batching: 62.1% and 88.9%. Mean batch size: 3.1 primitive actions. CLI share: 40.7% and 55.1% of actions. The only step measurement is OSWorld-v2 Table 5 (p.25), steps per task: Qwen-UI-Agent (batched) 135.8, MiniMax M3 326.7 and Qwen 3.7 Plus 173.5 (single-action); these give the intro's 58.4% and 21.7% fewer steps. Opus 4.8 (103.0) and GPT-5.5 (95.2), also batched, use fewer steps. This is a cross-model comparison; there is no batching on/off ablation. No wall-clock, latency, token or dollar figure is reported, and §7 (p.44) names interaction latency as a major remaining obstacle. The 10,000 concurrent environments are RL rollout infrastructure (training), not inference.

**mechanism and term:**

'N smaller' is the right intended term: K_t > 1 means fewer model decision steps per task, and CLI commands replace GUI sequences. But the report never measures it in a controlled way, so on slides it should read 'N smaller (claimed; not measured in isolation)'. Batching does not reduce the environment actions; the primitive actions still run. It only removes the observe-plus-model-call overhead between them. The Action RL analysis (§4.3) reports reasoning tokens -21.3% (smaller decode) but interaction steps +8.4% (larger N). It uses internal error-pattern test sets, not a public benchmark, so it cannot be used. The 10,000 concurrent environments speed up training rollouts and change no term of the per-task formula: remove them from the mechanism or label them 'training only'. Proposed D-entries: (a) the '~40% batched output' figure differs by version (project PDF >30%, arXiv v1 >40%, Table 11 39.6/41.6% at action level); (b) WebArena 73.6% uses corrected references and scripts; (c) the only step-count evidence is cross-model.

**authors and venue:**

This is no longer only a vendor PDF: it is on arXiv as 2607.28227v1 (30 Jul 2026), with no journal or conference venue in the arXiv comment. Authors on arXiv: Hanzhang Zhou, Panrong Tong, Xu Zhang, Quyu Kong, Chenglin Cai, Tianyu Xia, Gongjie Zhang, Jianan Zhang, Long Li, Long Chen, Lei Wang, Gaole Dai, Pengxiang Li, Liangyu Chen, Yue Wang, Steven Hoi; 11 further contributors are listed in §8. The byline reads 'MAI-UI Team', with the affiliation line printed as 'Alibaba Token Hub, Alibaba Group'; the project page is tongyi-mai.github.io. It continues MAI-UI (arXiv 2512.22047). Under the credibility rule it passes (i)-(iv) as an industry-lab preprint: named authors, a company research group, and public benchmarks with task counts and model stated. Label it 'industry technical report (self-evaluated own model)', not vendor marketing. Change the citation from 'Tongyi MAI (2026)' to Zhou et al. (2026), arXiv:2607.28227v1, Alibaba Group. It is not in references.md or the ledger.

**formula:**

Eq. (4), §2.1.1, p.6: a_t = (a_t^(1), ..., a_t^(K_t)), with a_t^(k) in A_t. K_t = 1 is single-action execution; K_t > 1 is a batched sequence run consecutively in one decision step. The text says this cuts unnecessary inference and observation steps. Eq. (3): (r_t, a_t) = pi_theta(I, o_t, h_t). The report gives no speed-up or cost formula.

## 43. CUA-Universe / CUA-Verse

**read:** arXiv:2609.05374v1 (4 Sep 2026; the only version), abs page and PDF https://arxiv.org/pdf/2609.05374v1 via pdftotext. Quotes are paraphrased; figures are exact.

**verdict:** corrected

**effect:**

Abstract (p.1) gives separate figures per benchmark for 'our 9B model' (Qwen3.5-9B + LoRA, trained on 4,923 verified episodes rolled out by Kimi K2.5): CUA-Verse score +39.3 pts, -37% steps, -60% tokens; OSWorld SR +16.8 pts, -57% steps, -44% tokens; OSWorld-MCP score +7.84 pts, -27% steps, -30% tokens. Table 1 (p.6), CUA-Verse: this is the authors' own benchmark of 160 held-out tasks (8 in-domain apps x 20), scored by a GPT-5.4 VLM judge. Ours: 0.582 score, 35.2 steps, 255K tokens per episode. Untuned Qwen3.5-9B: 0.189, 56.2 steps, 643K tokens. That comparison is where '60% fewer tokens vs base' comes from. OSWorld: a controlled 244-task subset that excludes the os and multi-app splits, scored by the official verifier, with a 60-step budget and a 3-frame history. Ours GUI-only 23.4% vs Ours GUI+CLI 40.2%: the +16.8 pts is the same trained model with the CLI tool added, not a comparison with the base. Over all tasks, mean steps go 39.6 -> 28.6 and tokens per task 325.7K -> 286.5K. Step Gain 2.35x and Token Gain 1.79x are mean per-task GUI/GUI+CLI ratios over jointly solved tasks only; these are the abstract's -57% and -44% (1-1/2.35 and 1-1/1.79, calc.). Definitions (p.6): Steps = mean number of model decision calls per trajectory; Token/task = mean input+output tokens per task. Adding the CLI to other models gains only +2 to +8 tasks. OSWorld-MCP (Table 2, 244 tasks, max 50 steps): ACS 27.25 vs 37.22 and tokens 87.95M vs 125.68M against the base. SR is 28.69 vs 20.90, a 7.79-pt difference (calc.), whereas the abstract says +7.84. There is no inference wall-clock or dollar figure. The Table 3 per-task costs ($0.31 -> $0.26 with Path-Steer) are for data-generation rollouts by Kimi K2.5.

**mechanism and term:**

The dossier row mixes two benchmarks and two baselines. The 60% token saving is on CUA-Verse against the untuned base. The +16.8 pp is on OSWorld, GUI-only vs GUI+CLI with the same fine-tuned model, and on OSWorld the token saving is 44% on jointly solved tasks or 12% over all 244 tasks (calc.). Terms: N (model calls per task) smaller, tokens per task smaller, success rate up. The paper reports input+output tokens combined, so the saving cannot be split into prefill vs decode; map it to 'tokens per pass x N', not to prefill/decode separately. The mechanism has two parts: a CLI tool added to the action space (structure), and fine-tuning on synthesized hybrid trajectories. The paper shows the CLI alone helps untrained models little. Proposed D-entry: the dossier line conflates CUA-Verse vs base with OSWorld GUI vs GUI+CLI.

**authors and venue:**

Authors: Haoting Shi, Wenhao Wang, Weicheng Fang, Yaozhong Liang, Tian Jin, Pengxiang Zhao, Guangyi Liu, Siheng Chen, Yanfeng Wang. The arXiv abs page lists names only; the institutions come from the paper's author block: Shanghai Jiao Tong University and Zhejiang University. No venue; the arXiv comment is '21 pages, 9 figures'. Code and data are promised ('will release'). Rule (i), (ii), (iv) pass. Rule (iii) passes for OSWorld and OSWorld-MCP (public, 244 tasks, model stated). CUA-Verse is the authors' own benchmark and not yet released, so slides should cite the OSWorld figures, not the CUA-Verse 60%. It is not in references.md.

**formula:**

§4.2, p.6: Success gain = (SR_GUI+CLI - SR_GUI) x 244. Step Gain and Token Gain = mean per-task ratio of GUI to GUI+CLI cost over jointly solved tasks (k x = k times fewer). App. H, p.16, rollout wall-clock = N*t_bar/P, with t_bar about 5 min per rollout, N about 10^4 rollouts and P = floor(128/4) = 32 environments per 128-core server. So N*t_bar is about 50,000 VM-minutes, or about 1,560 min of wall-clock. This is the cost of generating training data, not inference.

## 44. SPACE (skill-guided adaptive action chunking)

**read:** arXiv:2609.02042v1 (2 Sep 2026; the only version), PDF https://arxiv.org/pdf/2609.02042v1 via pdftotext and the abs page. A web search on 28 Sep 2026 found no official EMNLP 2026 listing. Quotes are paraphrased; figures are exact.

**verdict:** corrected

**effect:**

Table 1 (p.7), ALFWorld: a text-based household environment on the official seen/unseen split. The paper does not print the evaluation task count; its hyperparameter table lists a validation set size of 128. The metric is success rate (SR) plus average LLM rounds per episode. Qwen3-4B unseen: SPACE 96.9% / 4.4 rounds; GiGPO 72.7 / 21.7; Multi-action GRPO 81.3 / 20.9; GRPO 54.7 / 32.3; ReAct 40.6 / 36.2. The table's own deltas for that cell (+15.6 SR, -16.5 rounds) are against the best baseline in each column, which is Multi-action GRPO (81.3%, 20.9 rounds), not GiGPO. Qwen3-4B seen: 99.2% / 3.7 vs GiGPO 85.2 / 15.9. Llama-3.1-8B: seen 96.1 / 5.0, unseen 94.5 / 5.2, vs GiGPO 89.1 / 14.5 and 83.6 / 18.8, and vs Multi-action GRPO 71.1 / 5.4 and 65.6 / 5.5. Table 2 (p.8), ScienceWorld, Llama-3.1-8B only (tasks with an oracle solution over 100 steps are excluded, App. A.2): SPACE 67.2 / 5.2 seen and 61.7 / 5.8 unseen, vs GiGPO 35.9 / 10.2 and 34.4 / 10.1, i.e. +31.3 and +27.3 pts. The abstract's success gain of 7.0%-31.3% is in absolute points over the strongest baseline per setting, and its 'up to 78.9%' fewer rounds is 20.9 -> 4.4 vs Multi-action GRPO (calc.); the intro gives a 7.4%-78.9% range. Table 4 (p.8), Best-of-N with N=8 on a hard ScienceWorld subset: 48.3 vs 74.9 LLM calls per episode. No wall-clock, token or cost figures; the Limitations section (p.8) says text environments only.

**mechanism and term:**

'N (model calls per episode) smaller; success rate up' is correct. The environment actions are not reduced: the same primitives run, only chunked. Decode per call is presumably larger (several actions per output) but is not measured. Correction 1: the dossier pair (rounds 21.7 -> 4.4, success 72.7 -> 96.9) is real but is a comparison with GiGPO. The paper's strongest-baseline pair for that cell is 81.3 -> 96.9 (+15.6 pp) and 20.9 -> 4.4 rounds (-78.9%). The dossier's -79.7% is calc. vs GiGPO and should be labelled that way. Correction 2: '+7.0-31.3 pp ScienceWorld' is wrong. That range spans both benchmarks: ALFWorld is +7.0 to +15.6 pp, ScienceWorld +27.3 to +31.3 pp.

**authors and venue:**

Authors: Yanting Yang, Can Jin, Jinman Zhao, Jiahao Wu, Yang Zhou, Zhepeng Wang, Zhendong Wang, Mu Zhou, Dimitris N. Metaxas. Institutions: Rutgers; U Toronto; PolyU; Amazon; Microsoft. Both confirmed. The only venue evidence is the arXiv comment 'EMNLP 2026 Camera Ready'; it is not confirmed on an official list, so keep it as a preprint. Credibility rule: passes (i), (ii), (iv), and the models and public benchmarks are stated. The caveat for (iii) is that the evaluation task counts are not printed in the paper.

**formula:**

No speed-up or cost formula. §3.4 gives a training objective only: L(theta) = L_on(theta) + lambda_off * L_off(theta). There, u_i = (a_i,1, ..., a_i,l_i) is the action chunk at round i and M_tau is the number of LLM rounds in a trajectory.

## 45. Foundations: LATM, DiLogics, ALLOY, Voyager, WebAgent/HTML-T5 (qualitative only)

**read:** LATM: arXiv 2305.17126v2 (11 Mar 2024) PDF. DiLogics: UIST '23 PDF from https://web.eecs.umich.edu/~xwangsd/pubs/uist23b.pdf. ALLOY: arXiv 2510.10049v1 PDF. Voyager: arXiv 2305.16291v2 PDF; the OpenReview record (forum ehfRiF0R3a) could not be read because it returned a challenge page. WebAgent: arXiv 2307.12856v4 PDF. Quotes are paraphrased; figures are exact.

**verdict:** corrected

**effect:**

LATM, Table 2 (p.7): six BIG-Bench tasks, GPT-4 as tool maker. GPT-3.5 Turbo as tool user with LATM matches or beats CoT (e.g. Dyck 92.2 vs 20.4, Word Sorting 98.3 vs 59.2). Cost appears only in O-notation. The caption defines C as one GPT-4 call and c as one GPT-3.5 Turbo call, with C over 15x c at the time of writing. No measured dollars or time. DiLogics: a usability study with 10 participants on four data-entry tasks; qualitative, no speed or accuracy figures. ALLOY: 12 participants rating on 7-point Likert and NASA-TLX scales (pp.12-14); no task accuracy or timing. Voyager, Table 1 (p.7): Minecraft, gpt-4-0314, 3 trials, cap of 160 prompting iterations. The wooden tool takes 6+-2 iterations vs AutoGPT's 92+-72, so '15.3x faster' is counted in prompting iterations, not time. Voyager without the skill library needs 7+-2 for wooden and 9 vs 11 for stone, so the library does not drive that ratio; the authors credit the curriculum. They also note GPT-4 is 15x more expensive than GPT-3.5. WebAgent, Table 1 (p.5): three real websites (real estate, social media, map), 20 instructions each, Flan-U-PaLM 540B as programmer with HTML-T5 for planning and summarization. Success is 65/70/80% vs 10/20/10% for Flan-U-PaLM alone, so 'over 50%' means +50 to +70 absolute points (calc.). MiniWoB++ (p.8-9, Table 3): 56 tasks x 100 episodes with 12K demonstrations, HTML-T5-XL 67.1% vs WebN-T5-XL 48.4%, so '18.7%' is +18.7 absolute points. No token or time figures.

**mechanism and term:**

LATM: correct as price/tier. The n repeated calls cost c instead of C, and the one-time tool-making cost C is spread over the n requests (a fixed-plus-per-instance structure). It is not an agent loop and nothing was measured. DiLogics and ALLOY: demonstration -> reusable program or workflow. Conceptually this lowers N at replay, but nothing is measured, and ALLOY's workflow nodes are still LLM sub-agents, so c_k is not removed. Lineage only. Voyager: an executable skill library conceptually lowers N (iterations to a milestone). But the 15.3x is measured against AutoGPT and mainly reflects the curriculum; no time or token figures. WebAgent: 'prefill smaller via HTML summarization' is correct for the large programmer model; the paper's motivation is context length, since real-site HTML is far longer. The caveat is that it adds an HTML-T5 call per step (c_k +1, on a cheaper tier), and the net cost is not measured. The dossier's +18.7% and '>50%' should be restated as absolute percentage points with the conditions above.

**authors and venue:**

LATM: ICLR 2024 (PDF header). Tianle Cai, Xuezhi Wang, Tengyu Ma, Xinyun Chen, Denny Zhou; Google DeepMind, Princeton, Stanford. DiLogics: UIST '23, ACM, DOI 10.1145/3586183.3606822. Kevin Pu, Jim Yang, Angel Yuan, Minyi Ma, Rui Dong, Xinyu Wang, Yan Chen, Tovi Grossman; U Toronto, U Michigan, Virginia Tech. ALLOY: preprint only (arXiv v1, 11 Oct 2025; ACM template with a placeholder DOI, no venue). Jiawen Li, Zheng Ning, Yuan Tian, Toby Jia-jun Li; U Michigan, U Notre Dame, Purdue; it passes the author and institution check required for a qualitative mention. Voyager: Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, Anima Anandkumar; NVIDIA, Caltech, UT Austin, Stanford, UW Madison. The TMLR 2024 venue comes only from a web-search snippet; the OpenReview page could not be opened. Confirm it on jmlr.org/tmlr before citing a venue; otherwise cite arXiv v2 (2023). WebAgent/HTML-T5: ICLR 2024 (Oral), per the arXiv comment and PDF header. Izzeddin Gur, Hiroki Furuta, Austin Huang, Mustafa Safdari, Yutaka Matsuo, Douglas Eck, Aleksandra Faust; Google DeepMind, U Tokyo. None of the five is in references.md or the ledger yet.

**formula:**

LATM, Table 2 last column (p.7), cost for n samples: O(nc) for GPT-3.5 with CoT; O(nc + C) for LATM with a GPT-3.5 tool user; O(nC) for GPT-4. C = cost of one GPT-4 call, c = cost of one GPT-3.5 Turbo call, C > 15c at the time of writing. Voyager gives only a prose remark (GPT-4 15x the price of GPT-3.5). DiLogics, ALLOY and WebAgent give no formula.

## 46. Agent Workflow Memory (AWM)

**read:** arXiv:2409.07429v1 (11 Sep 2024; the only arXiv version) PDF. ICML 2025 version: PMLR v267 pp. 63897-63911, PDF https://raw.githubusercontent.com/mlresearch/v267/main/assets/wang25bx/wang25bx.pdf, with metadata from proceedings.mlr.press/v267/wang25bx.html. Also ASI arXiv 2504.06821v2 (COLM 2025) for the D41 re-run. Quotes are paraphrased; figures are exact.

**verdict:** corrected

**effect:**

Table 1 (arXiv p.5; same figures in ICML Table 1): WebArena, 812 tasks, BrowserGym framework with accessibility-tree-only input (the BrowserGym_ax-tree baseline), online AWM on test queries only, temperature 0. Total SR 15.0% -> 35.5%; # Steps 7.9 -> 5.9. The headline +12.0 absolute and 51.1% relative is against plain BrowserGym (23.5%, HTML+AXTree, no step count reported), not the ax-tree run. The paper calls the step metric the average number of steps to solve a task; the abstract speaks of tasks solved successfully, so it is unclear whether failed tasks are included. Model: arXiv v1 body says gpt-4-0613, but the ICML body (p.4) says GPT-4o (gpt-4o-2024-05-13); both Table 1 captions say gpt-4. ICML App. D, Table 11 (p.14), tokens per task: action generation 5,663 input + 52.0 output per step x 5.9 = 33,718.5; trajectory evaluation 389.6 x 5.9 = 2,298.6; workflow induction 635.5 x 2.1 = 1,344.6. The text says this adds 10.8% computation overhead for a 51.5% accuracy increase (the main text says 51.1%). ASI re-run (claude-3.5-sonnet, WebArena): vanilla 5.6 steps / 32.7%, AWM 5.9 / 36.3%, ASI 5.0 / 40.4%. No runtime or wall-clock anywhere.

**mechanism and term:**

Mostly correct. N is intended to shrink (7.9 -> 5.9 vs the ax-tree baseline), but ASI's controlled Claude re-run does not reproduce it (D41). Prefill is larger because workflows are injected into the prompt; the baseline's per-step input tokens are not reported, so the increase cannot be quantified. Add c_k larger: AWM adds LLM calls for trajectory evaluation and workflow induction, about 10.8% extra tokens by the authors' Table 11, and that 10.8% excludes the workflow text in the action prompt. Success rate up. Proposed D-entry: the model identity differs between arXiv v1 (gpt-4-0613) and the ICML text (gpt-4o-2024-05-13), while the ICML table caption still says gpt-4. Cite the ICML version and state the model as reported inconsistently.

**authors and venue:**

ICML 2025, PMLR v267 pp. 63897-63911. Zora Zhiruo Wang, Jiayuan Mao, Daniel Fried, Graham Neubig; CMU and MIT. Confirmed against the PMLR metadata and the paper.

**formula:**

No explicit formula. ICML Table 11 implies total tokens per task = tokens per step x occurrences per task, summed over the three modules.

## 47. Agentic Plan Caching (APC)

**read:** arXiv:2506.14852v2 (26 Jan 2026) PDF https://arxiv.org/pdf/2506.14852v2 via pdftotext, plus the NeurIPS proceedings page https://proceedings.neurips.cc/paper_files/paper/2025/hash/9549f7d06700f0966d5f938f1d11022a-Abstract-Conference.html

**verdict:** corrected

**effect:**

Setup (pp.6-7): Minion Plan-Act architecture with at most 10 iterations. Large planner GPT-4o; small planner and actor LLaMA-3.1-8B; keyword extraction and cache generation by GPT-4o-mini; GPT-4o as judge. Cost = input/output tokens x API prices (OpenAI, TogetherAI). The baseline, 'Accuracy-Optimal', uses no cache and always calls the large planner. There are five workloads: FinanceBench (200 sampled questions), QASPER, TabMWP (200), AIME 2024+2025, and GAIA. The paper states averages of cost -50.31% and 96.61% of accuracy-optimal. Table 1 (p.8) and Table 9 (p.25), accuracy-optimal -> APC: FinanceBench $4.03 / 91.0% -> $1.86 / 85.5% (-5.5 pts); TabMWP $3.35 / 83.0% -> $2.03 / 82.0%; QASPER $2.14 / 58.0% -> $0.78 / 57.0%; AIME24 $1.14 / 64.52% -> $0.85 / 61.29%; AIME25 $1.34 / 61.29% -> $0.81 / 58.06%. GAIA used Open Deep Research (smolagents) with GPT-4o large and GPT-4o-mini small: $69.02 / 37.58% -> $16.27 / 36.97% (-76.42%, -0.61 pts); the GAIA split and task count are not stated. Latency (§4.3, Table 3, p.9) comes from a single microbenchmark: 100 random FinanceBench queries at a 46% hit rate, total wall-clock 1,959.24 s -> 1,424.82 s. Components: plan 1,813.41 -> 1,011.82 s; act 94.39 -> 131.44 s; keyword extraction 42.29 s; lookup <1 s; cache generation 215.80 s (3.99 s per entry). Paper, p.8: "APC reduces end-to-end latency by 27.28% on this workload". Cache overhead of 1.04% is the mean of FinanceBench 1.15% and TabMWP 0.93% (Table 2); worst case at a 0% hit rate is 1.31%. A query-level semantic cache (GPTCache-style, similarity thresholds 0.8-0.9) loses accuracy through false-positive hits (§4.2).

**mechanism and term:**

Price/tier is correct: on a cache hit, the large-planner call is replaced by a small-planner adaptation. 'c_k about the same' needs a correction: every query adds a GPT-4o-mini keyword-extraction call, and every miss adds a cache-generation call (+42 s and +216 s in Table 3). So c_k rises slightly while spending shifts to cheaper tiers; plan time falls and act time rises (+37 s). 'Success slightly lower' is true on average (96.61%), but per workload the drop reaches -5.5 pts (FinanceBench) and -3.2 pts (AIME). Main correction: -27.28% latency is not an average over five workloads, despite the abstract's 'on average'. It is one FinanceBench microbenchmark (100 queries, 46% hit rate); latency was not measured on the other workloads. Also, the averages cannot be reproduced from the tables: over six columns the mean cost cut is 49.70% and the mean accuracy ratio 96.52% (calc.). Proposed D-entry: 'latency -27.28% averaged over 5 workloads' -> a single FinanceBench workload.

**authors and venue:**

NeurIPS 2025, main conference track. The proceedings page lists Qizheng Zhang, Michael Wornow and Kunle Olukotun; arXiv v2 adds Gerry Wan. Stanford University. Confirmed.

**formula:**

None. Cost is computed as tokens x per-token API price (App. Table 8).

## 48. Revisable by Design (qualitative only)

**read:** https://arxiv.org/pdf/2604.23283v1 (v1, 25 Apr 2026, the only version on the abs page on 28 Sep 2026). Read with pdftotext -layout: sec. 3-8, Tables 1, 2, 7 and 8, App. A, I and K. Text: scratchpad/wf-part2/g6/2604.23283v1.txt

**verdict:** corrected

**effect:**

The numbers are correct, but the effect is on wasted acts, not on steps or cost. Source: Table 1 (p. 8), with Table 8 in App. I giving all 7 policies. Setup: DeepSeek-V3 (deepseek-chat, T=0.2) primary grid, n=1,008 runs, 144 per method. StreamBench is the authors' own benchmark: 3 scenarios of 12-15 steps (Event Planning, Travel Arrangement, Report & Publish), 4 reversibility ratios rho in {1.0, 0.75, 0.5, 0.25} and 5 revision types. Its tools are simulated (sec. 7 'Benchmark'; sec. 8 limitations). The revision is injected right after the agent's first K- or X-class action and contradicts it (App. A). Absorber vs Full-Restart: Quality (1-5, scored by a separate DeepSeek-Chat judge at T=0, three scorings averaged) 3.07+-0.86 vs 3.17+-0.85. Wasted acts (pre-injection acts later discarded) 0.78 vs 11.41 = 14.6x. Comp. (K compensations + R inversions) 0.78 vs 3.44. Total steps 27.6 vs 30.2. Tokens (k, summed over agent, judge and compatibility check) 136.8 vs 116.6. The 'equal quality' claim is Table 2, on the combined real-LLM corpus n=1,161: quality delta -0.11, d=-0.12, bootstrap 95% CI [-0.27, +0.05]; waste delta -10.00, CI [-10.89, -9.15]. Cross-LLM, Table 7: Claude Haiku 4.5 1.00 vs 13.57 wasted (13.6x, 60 runs per method); GPT-4o-mini 1.00 vs 10.76 (10.8x, 17-36 per method). Oracle: 18.0 steps, 77.1k tokens. Total API cost about $70 (App. A). Calc. vs Full-Restart: total steps -8.6% (27.6/30.2); tokens +17% (136.8/116.6); compensations 4.4x fewer.

**mechanism and term:**

The mechanism is described correctly: the I/R/K/X taxonomy (Def. 3), Earliest-Conflict Rollback (Thm 3) and Algorithm 1. Algorithm 1 keeps the prefix up to k*=i_bad-1, inverts R actions, compensates K actions, runs XFALLBACK for X actions, truncates the context to E_k* and re-plans. The term mapping 'N smaller' is WRONG as stated. (1) The trigger is a user revision injected mid-run, and Part 1's formulas have no term for it. (2) The 14.6x applies to discarded pre-injection acts, a subset of the steps, not to N: total steps fall only 30.2 -> 27.6 (-8.6%, calc.). (3) Tokens RISE 116.6k -> 136.8k (+17%, calc.; this count includes the judge and the IsCompatible LLM calls), so the money term goes up, not down. Suggested classification: 'rework after a mid-task spec change: fewer discarded environment actions and compensations (act term) at statistically indistinguishable quality; tokens higher'. Keep it qualitative (own benchmark, simulated tools). D-candidate: the deck and E135 must not present this as an N or cost reduction. E135's lower bound ≥(1−ρ)·n is correct; note that it is an expected count (Corollary 2).

**authors and venue:**

Confirmed. Zhiyuan Zhai (Fudan University), Ming Li (Guangming Lab; u.nus.edu email) and Xin Wang (Fudan University); Li and Wang are co-corresponding. First page: 'Preprint.'; cs.LG; v1 only. Code and benchmark are on github.com/zhiyuanZhai20/stream-agent.

**formula:**

No speed or time formula; there is a cost model. Eq. (1): rho(T) = |{a in A_T : class(a) in {I,R}}| / |A_T|. Eq. (2), Def. 5: AdaptCost(k*, rho, pi') = C_comp(rho) + C_waste(tau_{k*+1:n}), i.e. compensation plus abandoned work, in abstract additive cost units. Note that rho here is the compensation program; the paper uses the same symbol for the ratio. Corollary 2: the expected number of unavoidable-cost actions is >= (1 - rho(T))*n. Thm 3: k* = i_bad - 1 minimises C_comp + C_waste under Assumptions 1-3. Sec. 6: Step 1 needs at most m LLM calls, where m = number of K/X actions.

## 49. Safe to Resume? (negative security result)

**read:** https://arxiv.org/pdf/2608.29381v1 (v1, 29 Aug 2026, the only version; cs.CR). Read with pdftotext -layout: sec. I-IX, Tables II, IV and V. Text: scratchpad/wf-part2/g6/2608.29381v1.txt

**verdict:** confirmed

**effect:**

Microbenchmark, Table IV (sec. VII, Observation 3, pp. 12-13): 96 persistent external-action workflows built by the authors on Terminal-Bench action patterns (Payment 30, Message 31, Resource change 35). A recoverable failure is injected between the external effect and the checkpoint update, and the run resumes from the latest checkpoint through the framework's native recovery. A failure means an effect is repeated or skipped. Execute->Commit fails 90 (93.8%); Commit->Execute fails 93 (96.9%). SF5, Table II (sec. VI.C): unrecorded external effects in 40 of 1,735 framework-task executions (2.3%). The corpus is 347 traces (241 Terminal-Bench plus 106 AgentBench OS/DB/ALFWorld) run on 5 frameworks (LangGraph, CrewAI, Hermes, Cline, E2B). Backend LLM DeepSeek-v4; one random checkpoint per trace; SF4 replay repeated 3x. Other rates: SF1 1,166 (67.2%), SF4 1,174 (67.7%), SF2 489, SF3 198. Detector check, Table V: overall precision 98.7%, recall 99.9%, but SF5 recall is 90.0%, so 40 may undercount. Duplicate payment (sec. V Case 3): a LangGraph invoice-payment workflow following AgentDojo Banking; rollback re-executes the payment node, and the payment service commits a second payment. The other two end-to-end attacks: Hermes (malware-verification bypass) and Cline (unauthorised mail forwarding). Of 30 sampled findings turned into attacks, all 30 succeeded.

**mechanism and term:**

The mapping is correct: this is not a speed-up. It constrains any rollback, speculation or overlap scheme with external side effects; checkpoint ordering alone cannot close the gap, and the paper points to idempotency keys, transactions or durable effect records. Term: none (it bounds safe overlap and rollback). Minor location fix for E136: the explanation of why SF5 is rare (most tasks run on local files, databases or simulated environments) is in sec. VI.C RQ1, the SF5 bullet, not in the Limitations paragraph. The 'removes the internal record' wording is the SF5 definition in sec. IV.E (verified).

**authors and venue:**

Confirmed. Guanlong Wu, Dahui Li, Ke Jiang and Yinqian Zhang (Southern University of Science and Technology); Jianyu Niu and Cong Wang (City University of Hong Kong). Author order as cited. Preprint, v1 only, no venue.

**formula:**

None for speed or cost. It gives only a formal execution model: events e_i = <op_i, In_i, Out_i, ND_i> and conditions SF1-SF5.

## 50. RAC (Robust Agent Compensation) (qualitative only)

**read:** https://arxiv.org/pdf/2605.03409v2 (v2, 18 May 2026; v1 was 5 May 2026). The PDF is the ACM CAIS '26 camera-ready (DOI 10.1145/3786335.3813141, CC BY 4.0). Read with pdftotext -layout: sec. 1-7, Algorithms 1-3, Tables 1-4. Text: scratchpad/wf-part2/g6/2605.03409v2.txt

**verdict:** corrected

**effect:**

The paper does state speed and cost numbers, so 'no numbers' is not what the paper says. The abstract and the Conclusion say RAC is 1.5-8x better in latency and token economy than state-of-the-art LLM-based recovery (SagaLLM); the sec. 1 contribution list says 1.5-3x. Setup (sec. 5): gemini-2.5-flash unless stated otherwise; each problem repeated 3 times; 1M-token cap; SagaLLM capped at 3 planning iterations; M3 Pro laptop. SagaLLM is the authors' modified reimplementation, because the original code failed and its authors did not reply (sec. 5.1). Example values: Table 2 (REALM-Bench) P5 SagaLLM 250k tokens / 646 s vs RAC 10k / 15 s; P6 238k / 579 s vs 9k / 15 s. Table 3 (dynamic failures) P13 SagaLLM 2/3, 80k, 202 s vs RAC 3/3, 76k, 58 s; P14 RAC 2/3, 189k, 74 s vs SagaLLM 1/3, 95k, 173 s. Table 1, tau2-bench Telecom: RAC 99% success, 58 s, 176k tokens vs SagaLLM 100%, 32 s, 100k; RAC is slower and uses more tokens here. Calc.: per-problem ratios against SagaLLM run from about 1x to over 40x, so the 1.5-8x band is not derivable from the tables. Keep 'numbers not used', but correct the reason given in E137. The paper does define Success % (completed or abstained without side effects) and Compl. % (fully completed) in sec. 5.3.1. The real problems are these: the ranges are inconsistent (1.5-8x vs 1.5-3x); the baseline is a reimplementation; there are only 3 runs; RAC's Compl. % comes from internal logs (*); Table 2 has a likely typo (RAC_M '29' tokens); and Table 4 labels H as 'GPT-5' while the text says GPT-5.4. D-candidate.

**mechanism and term:**

The mechanism is described correctly but can be made more precise. Tool calls are logged in a Transaction Log (Alg. 1). On an error the system retries with backoff for transient errors, then tries an LLM-found alternative, then rolls back (Alg. 2). Rollback (Alg. 3) rebuilds the execution graph from the log and topologically sorts it so dependents are compensated before parents; the Conclusion calls this LIFO rollback. Compensations are looked up in this order: framework API config, then the MCP tool annotation (x-compensation-tool), then an LLM prompt. If none is found, RAC assumes the tool has no side effects (sec. 3.1 and sec. 6), so it fails open. The current implementation rolls back everything (sec. 6). The mapping 'none (safety)' is acceptable. At most, against an LLM-replanning recovery baseline it would cut model calls during failure recovery; the numbers are not usable.

**authors and venue:**

Confirmed. Srinath Perera, Kaviru Hapuarachchi and Rania Khalaf (WSO2, Santa Clara) and Frank Leymann (University of Stuttgart). ACM Conference on AI and Agentic Systems (CAIS '26), May 26-29, 2026, San Jose; 10 pages; DOI 10.1145/3786335.3813141. The arXiv comment reads 'Accepted at ACM CAIS 2026'.

**formula:**

None.

## 51. LLMCompiler

**read:** arXiv:2312.04511v3 PDF (5 Jun 2024), which carries the ICML 2024 / PMLR 235 header (Vienna). Read with pdftotext -layout: sec. 1-6, Tables 1-3, App. A, B, C.1, D and E. The PMLR page itself was not opened. Text: scratchpad/wf-part2/g6/2312.04511v3.txt

**verdict:** confirmed

**effect:**

Table 1 (p. 6), Movie Recommendation: 500 examples, an 8-way embarrassingly parallel pattern. GPT = gpt-3.5-turbo (1106), per App. D. Baseline ReAct† is ReAct with extra prompting against looping and early stopping. Accuracy 72.47 -> 77.13%, latency 20.47 -> 5.47 s, 3.74x. With LLaMA-2 70B (2x A100-80GB, vLLM): 70.60 -> 77.80%, 33.37 -> 11.83 s, 2.82x. HotpotQA (comparison dev set, 1.5k questions, 2-way), GPT: 62.47 -> 62.00% (a slight drop), 7.12 -> 3.95 s, 1.80x; LLaMA 1.40x. OpenAI parallel FC: Movie Rec 7.42 s, HotpotQA 4.42 s. 'Up to 35%' faster than it matches 7.42/5.47 = 1.36x (calc.). Table 2 (p. 6), Movie Rec: input/output tokens ReAct 20000/230 vs LLMCompiler 2800/115; column 'Cost ($/1k)' 20.46 -> 3.04 (6.73x). The paper does not define '1k'. Calc.: assuming gpt-3.5-turbo-1106 list prices of $0.001 input / $0.002 output per 1K tokens (not stated in the paper), 20,000 + 230 tokens = $0.02046 per query, i.e. $20.46 per 1,000 queries. So 'per 1,000 tasks' is our reading, and it should be labelled calc. Other tasks: ParallelQA (113 examples, gpt-4-turbo) 2.15x, cost 4.65x, 89.09 -> 89.38%. Game of 24 (100 instances, gpt-4-0613) vs Tree-of-Thoughts 2.89x, 74.00 -> 75.33%. Regressions: HotpotQA accuracy -0.47 pp vs ReAct†. WebShop (Table 3, 500 instructions) is SLOWER than ReAct (gpt-3.5: 5.98 -> 10.48 s; gpt-4: 19.90 -> 26.73 s) but has higher success (19.8 -> 48.2%; 35.2 -> 55.6%). Game of 24 LLaMA speed-up is 2.09x in Table 1 but 2.01x in the text. Setup (App. D): temperature 0; accuracy averaged over 3 runs; runs in Nov 2023.

**mechanism and term:**

The mechanism is correct. The Planner LLM emits a DAG with placeholder variables; the Task Fetching Unit dispatches tasks whose dependencies are resolved; the Executor runs them in parallel. An optional streamed planner overlaps planning with execution (Table C.1: 1.01-1.30x). Terms: (a) overlap saving among tool executions, where the sum of T_E becomes a max. This is environment-wait overlap, not decode-tool overlap, except for the streaming variant. (b) Fewer model calls per task (one plan plus the final answer instead of one call per tool): c_k*N smaller. (c) Far fewer prompt tokens per task (Movie Rec input 20,000 -> 2,800), because the planner's examples hold plans, not observations: the context-growth and prefill term, which the paper also credits for the cost saving. (d) Money lower. (e) The success gain comes mainly from avoiding ReAct's repeated calls and early stopping (App. A: ~85% early stopping on Movie Rec). Symbol clash: the paper's N is the number of planned tasks (function calls), not the deck's passes. Citation fix: add ICSI and LBNL to the institutions.

**authors and venue:**

Sehoon Kim* and Suhong Moon* (equal contribution), Ryan Tabrizi, Nicholas Lee, Michael W. Mahoney, Kurt Keutzer and Amir Gholami. Affiliations: UC Berkeley (all); ICSI (Mahoney, Gholami); LBNL (Mahoney). ICML 2024, PMLR 235 (arXiv comment 'ICML 2024'). The recorded 'UC Berkeley' is incomplete.

**formula:**

App. E.1, embarrassingly parallel case, N = number of tasks: (1) T^R = sum_{i=1..N} (T_P^R(P_i) + T_E(E_i)); (2) T^C = sum_{i=1..N} T_P^C(P_i) + max_{k in 1..N} T_E(E_k); (3) streaming: T^SC = sum_{i=1..N} T_P^C(P_i) + T_E(E_N), with T^SC <= T^C; (4) gamma = T^R / T^C; (5) gamma_max ≈ sum_i T_E(E_i) / max_k T_E(E_k) = N when executor latency dominates and all latencies are equal; (6) gamma_min ≈ sum_i T_P^R(P_i) / sum_i T_P^C(P_i) ≈ 1 when planning dominates. Measured on Movie Rec: planner overhead 1.88 s plus answer 1.62 s, more than half of the total latency; the slowest search takes 1.13 s vs a 0.61 s mean.

## 52. AsyncFC (future-based asynchronous function calling)

**read:** arXiv:2605.15077v1 PDF (14 May 2026, the only version), read with pdftotext -layout, plus the Fig. 3 image from https://arxiv.org/html/2605.15077v1 (the BFCL v3 bar labels are only in the image). Text: scratchpad/wf-part2/g6/2605.15077v1.txt; image: afc_fig3.png

**verdict:** corrected

**effect:**

The numbers are right, but one is mislabelled and the headline result is missing. Fig. 3 (p. 7), BFCL v4 Web Search: real backend latency; the 100 raw cases are composed pairwise, and results are on the matched non-overflow subset (n=31 for Sequential FC, n=29 for Parallel FC); GPT-4o. Seq FC 54.8% -> AsyncFC(S) 53.2%, 1.26x. Par FC 50.0% -> AsyncFC(P) 50.0%, 1.12x; this is the one comparison whose latency reduction is NOT statistically significant. BFCL v3 Multi-Turn: n=150 after filtering, 5 s delay injected per function, GPT-4o. Bar labels from the image, relative to Sequential FC: Par FC 1.06x, AsyncFC(S) with no annotation 1.10x, AsyncFC(S) 1.25x, AsyncFC(P) 1.26x; accuracy 68.0 / 67.3 / 70.7 / 69.3 / 66.0%. Fig. 5 (p. 9), HotpotQA 'asynchronous thinking': external reasoning turns are treated as tool calls; 100 raw tasks composed into 50 paired workloads; GPT-4o; 75.0 -> 75.0%, 1.24x. SWE-bench Lite: n=300, GPT-5.2 in SWE-agent, tool latencies scaled 2x. Resolution: SWE baseline 47.6%, +Par.FC 47.6% at 1.21x, +AsyncFC 44.3% at 1.44x vs the SWE-agent baseline. This 1.44x is the paper's second headline and is missing from the record. Gemini 3.1 Pro on BFCL v3 (10 s delay): 62.0 -> 65.3%, 1.17x. App. C: LLM-written annotations (Claude 4.6 Opus) give 1.22x vs Par FC at 68.0 -> 68.0%. Statistics: one-sided paired t-test on log speed-ups; McNemar test for accuracy, reported as 'no evidence of significant difference', which is not equivalence. Optional parallel decoding is disabled. Calc.: SWE-bench AsyncFC vs +Par.FC 1.44/1.21 = 1.19x with -3.3 pp resolution; BFCL v3 AsyncFC(P) vs Par FC 1.26/1.06 = 1.19x.

**mechanism and term:**

The mechanism is correct but incomplete. Function schemas are auto-transformed so calls return future placeholders at once, and the model resolves them with await_future. Results are merged into the context at turn boundaries. A scheduler serialises by default (root-level read/write sets) and allows parallel functions when developer or LLM-written resource annotations permit. Term: overlap saving introduced, with TWO parts per the paper's decomposition: decode-execution overlap (Delta_D||E) and inter-function parallelism (Delta_F||F). Fig. 4: decode overlap drives the first gains; parallelism dominates at larger tool delays. Side effects: decoding per turn can grow and extra turns can occur (App. B.1, sec. 6), so c_k and decode may rise. No token or money result is reported. Correction: the 'composed HotpotQA 1.24x' overlaps LLM reasoning calls, not environment time. 'Some experiments inject tool delays' should read: BFCL v3 5 s (GPT-4o) / 10 s (Gemini) injected; SWE-bench latencies x2; BFCL v4 real backend.

**authors and venue:**

Confirmed. Guangyu Feng, Huanzhi Mao, Prabal Dutta and Joseph E. Gonzalez, all at UC Berkeley. First page: 'Preprint.'; cs.CL; v1 only.

**formula:**

Eq. (1), repeated as Eq. (2) in App. B: R = (T_LLM + T_tool) / max(T_LLM, T_cp). This is the theoretical maximum speed-up. T_tool is the total function time over the dependency-DAG nodes, T_cp the function time along the critical path, and T_LLM the total decoding time. App. B.1, with decode overhead alpha: R = (T_LLM + T_tool)/T_cp if T_cp >= (1+alpha)T_LLM; otherwise (T_LLM + T_tool)/((1+alpha)T_LLM). App. B.2: T_saving := S(M) + S(E) - D(M ∪ E) = Delta_F||F + Delta_D||E, with Delta_F||F = S(E) - D(E) and Delta_D||E = D(M) + D(E) - D(M ∪ E). S is the summed interval length and D the length of the union, over the decoding intervals M and execution intervals E. App. B Table 1 lists the operating regimes (sweet spot: T_LLM ≈ T_cp and T_tool >> T_cp). This is the source of the deck's T_saving.

## 53. AsyncLM

**read:** arXiv:2412.07017v1 PDF (9 Dec 2024), the only version on the abs page on 28 Sep 2026; a web search found no published version. Read with pdftotext -layout: sec. 1-6, Figs 5, 6 and 8, Table 1. Text: scratchpad/wf-part2/g6/2412.07017v1.txt

**verdict:** corrected

**effect:**

Workloads (sec. 6): BFCL v1-parallel plus v2-parallel-live (400 parallel scenarios), v3-base-multi-turn (200), and the authors' own v3-multi-step-parallel (200 scenarios, each combining 3 multi-step samples). Of the 800 samples, 200 are used for fine-tuning and 600 for evaluation; per-figure counts are not given. Measured function time is 30-500 ms, mean 110 ms. Latency is the time from the first to the last generated token. A cheat sheet of ground-truth answers is put in the prompt so the calls stay fixed across runs. Local: fine-tuned Llama-3.2 3B/1B on one RTX 4090 with TGI. Cloud: GPT-4o/4o-mini with few-shot prompts; cloud Async latency is EMULATED from an average 5 ms per output token (OpenAI API statistics). Fig. 5 (parallel sets): Async vs Sync (sequential) 1.6x local, 2.1x cloud; Sync-Parallel 1.3x local, 1.7x cloud. Fig. 6 (multi-step-parallel): Async up to 5.4x vs Sync, Sync-Parallel 3.2x; the bar-label order (as in Fig. 5) implies these are cloud, and the local labels are 2.4x and 1.6x. So '1.6-5.4x' mixes measured local numbers (1.6-2.4x) with emulated cloud numbers (2.1-5.4x) and two datasets. 'Up to 2.1x vs sync-parallel' appears only in the sec. 1 introduction, whereas sec. 6.1's 2.1x is against sequential Sync. From the bar labels, Async / Sync-Parallel is 1.24x (Fig. 5 cloud), 1.23x (Fig. 5 local), 1.69x (Fig. 6 cloud) and 1.5x (Fig. 6 local) (calc.). Only Fig. 8 (user-triggered interrupts arriving at 0/200/400 ms) exceeds 2x: Async 2.4x vs Sync-Parallel 1.1x gives about 2.2x (calc.). D-candidate. Async-Naive on the plain OpenAI API is 1.5x SLOWER than Sync-Parallel on GPT-4o, because every interrupt is a new API call (average TTFT 310 ms). Accuracy, Table 1 (AST match, multi-step parallel): GPT-4o 57.84 -> 59.61%; GPT-4o-mini 55.08 -> 41.44%; fine-tuned Llama-3B 57.33 -> 65.97% (Sync written in CML: 66.07%); few-shot Llama-3B 16.98 -> 5.46%.

**mechanism and term:**

The mechanism is correct but needs additions. Interrupt tokens are injected into the token stream, using a CML domain-specific language for calls and interrupts. The model must be fine-tuned (Llama) or given few-shot prompts (GPT-4o). The serving system is co-designed: a token monitor, interrupt insertion, and a trap handler that keeps, swaps or recomputes the KV cache while waiting; calls are scheduled longest-first (LPT). Term: overlap saving introduced (decode overlaps tool execution, and cross-call parallelism comes without a pre-declared DAG). On stateless hosted APIs each interrupt becomes a new call, adding prefill and queueing (TTFT), and that erases the gain. The cloud benefit therefore needs a provider-side change and stays emulated. Label all cloud numbers 'emulated', and note that the measured calls were held fixed by the cheat sheet.

**authors and venue:**

Confirmed. In Gim, Seung-seob Lee and Lin Zhong, Department of Computer Science, Yale University. First page: 'Preliminary work. Under review.'; cs.CL; v1 only; no venue found.

**formula:**

Sec. 6.3, for a set F of independent calls, with G(f) the token-generation latency and E(f) the execution time. L_Sync(F) = sum_{f in F} G(f) + sum_{f in F} E(f). L_Sync-Parallel(F) = sum_{f in F} G(f) + max_{f in F} E(f). L_Async(F) = max_{f in F} (E(f) + sum_{g in pred(f,F)} G(g)), with pred(f,F) = {g in F | E(f) <= E(g)} (LPT order). Thm 6.1: L_Async(F) <= L_Sync-Parallel(F) < L_Sync(F). Thm 6.2: L_Sync / L_Async ≈ 1 + E/G, with error O((E/G)^2) for large |F|, where E is the mean execution time, G the mean generation time, and E is assumed normally distributed. Thm 6.3: no deviation from LPT lowers total latency (independent calls).

## 54. Helium

**read:** arXiv:2603.16104v1, the only version (17 Mar 2026). Full PDF https://arxiv.org/pdf/2603.16104v1 read through pdftotext, plus the abs page metadata.

**verdict:** corrected

**effect:**

The numbers are right, but 1.56x and 1.34x are each the largest gain over one baseline, KVFlow. They are not a gain over all six baselines. Quotes: Abstract, "up to 1.56× speedup over state-of-the-art agent serving systems"; §7.1, "Helium outperforms KVFlow by up to 1.56×"; §7.2, "Helium outperforms KVFlow by up to 1.34×".

Metric (§7.1 'Evaluation metrics'): end-to-end latency, defined as "total wall-clock time for query batch preparation and execution". For Helium it includes optimization and scheduling time.

Set-up: one batch; greedy sampling; vLLM v0.16.0 with automatic prefix caching and chunked prefill; one model instance per GPU on 2x 94 GB H100 NVL.

Primitive workflows (Fig. 5 caption: 'with Qwen3-8B'):
- MapRed and Debate: 200 MMLU questions and 100 TAT-QA contexts of 6 questions each.
- Reflect: 200 TAT-QA contexts.
- Iterative: 200 Amazon Reviews items. Parallel: 100 items. Each item has 60 reviews in 6 chunks.

Table 2, latency of each system divided by Helium's (max / average):
- vLLM: 100.92 / 66.27
- OpWise: 1.58 / 1.25
- LangGraph: 1.83 / 1.28
- AgentScope: 4.32 / 2.10
- Parrot: 2.21 / 1.44
- KVFlow: 1.56 / 1.32

Trading workflow (§7.2, Fig. 7):
- 19 agents and 88 LLM operators.
- Self-built dataset of 100 stocks over two days; day 1 warms up the system, day 2 is evaluated.
- Qwen3-8B and Qwen3-14B, batch sizes 8 to 80 queries.
- Largest gains: 39.50x over vLLM, 4.25x OpWise, 1.49x LangGraph, 1.46x AgentScope, 2.51x Parrot, 1.34x KVFlow.

Llama-3.1-8B and Qwen3-32B appear only in the sensitivity study against LangGraph (Fig. 9a). They are not part of the headline comparisons.

Accuracy is not measured. The design is described as semantics-preserving (§2 'Scope').

Ablation (Table 3; Trading, batch 16, Qwen3-8B): latency rises by 23.35% without plan pruning, 17.66% without cache-aware scheduling, 13.56% without the prompt cache and 3.55% without proactive KV caching.

Corrections to E173 and the §3.4 row:
- 1.56x and 1.34x are the maxima against KVFlow, not the gain over the best baseline on each workload. OpWise and Parrot come within 1.02x on some workloads.
- The headline models are Qwen3-8B, and Qwen3-14B for Trading only.

**mechanism and term:**

The mechanism is confirmed; the term mapping needs one addition.

1. Prefill (confirmed). Proactive KV caching keeps the KV cache of static prompt prefixes in GPU memory across batches. Scheduling puts calls that share a prefix next to each other on the same worker. Fewer prompt tokens therefore miss the cache.

2. Model calls per pass, c_k, get smaller (missing from the record, and the larger effect). Common-subgraph elimination runs a repeated sub-plan once. A global prompt/output cache replaces a deterministic LLM operator with a CacheFetch, so the whole model call is skipped. In the ablation, plan pruning (23.35%) and the prompt cache (13.56%) matter more than KV reuse (3.55%).

3. Queueing/scheduling (confirmed). A cost-based schedule minimises makespan and adds precedence delays so dependent calls are interleaved with independent ones, which raises the batch size.

Scope caveats:
- The gain is batch wall-clock over many queries on self-hosted GPUs, not the latency of one interactive agent task.
- There is no environment term and no GUI or browser workload.
- Money changes only indirectly, as GPU time.

**authors and venue:**

Authors: Noppanat Wadlom, Junyi Shen, Yao Lu, all National University of Singapore (PDF header and arXiv metadata). arXiv v1, 17 Mar 2026, cs.MA. The title carries '(Extended)'. No venue appears on the arXiv page or in the PDF, so this is a preprint. Code: github.com/mlsys-io/helium_demo.

Credibility rule:
- Authors and institution: verifiable, university.
- Primitive workflows: public datasets (MMLU, TAT-QA, Amazon Reviews), with item counts and models stated.
- Trading workflow: runs on a self-built dataset.

Verdict: passes. Not yet in references.md.

**formula:**

Yes. §5 'Scheduling Problem Formulation' (pp. 5-6) models cost in 'token steps', its unit of time:
- u_p(i,j) = Σ_{v∈path(r,l^i_j)} ω(v) if j=1; otherwise Σ_{v∈LCApath(l^i_{j−1}, l^i_j)} ω(v). This is the prefill usage: prompt tokens not shared with the previous call on the same worker.
- u_d(i,j) = ½·len_out(l^i_j)·(len_out(l^i_j)+1). This is the decode usage.
- u(i,j) = α_i·(len_out(l^i_j)×u_p(i,j) + u_d(i,j)), with α_i = 1/M_i for identical workers, where M_i is the worker's KV-cache capacity in tokens.
- d(i,j) = α_i·M_i×len_out(l^i_j). This is the precedence delay.
- Minimize T(σ) = max c(i,j), subject to b(i,j) ≥ c(i′,j′) + d(i′,j′) for every dependency edge, and c(i,j) = b(i,j) + u(i,j).

§7.3 also defines Gap(%) = (T(σ) − T(σ*)) / T(σ*) × 100. The paper gives no closed-form speedup formula.

## 55. LLM-Tool Compiler

**read:** arXiv:2405.17438v1, the only version (7 May 2024). Full PDF https://arxiv.org/pdf/2405.17438v1 read through pdftotext -layout.

**verdict:** corrected

**effect:**

The paper states its headline numbers inconsistently:
- Abstract: "reducing token costs and latency by up to 40% and 12%, respectively" and "up to four times more parallel calls".
- Introduction: token costs and latency both reduced "by 12%".
- Fig. 1 caption: "up to five times" more parallel calls.

Table 1 (GeoLLM-Engine; GPT-3.5 Turbo 0125 and GPT-4 Turbo 0125; CoT and ReAct, zero- and few-shot):
- Against the in-context baseline, tokens per task fall 1.20-1.35x (GPT-3.5) and 1.33-1.41x (GPT-4).
- Time per task falls 1.36-1.59x (GPT-3.5) and 1.19-1.21x (GPT-4).

Calc. against the OpenAI parallel-function-calling baseline:
- Time per task: −9.6% to −12.4% (GPT-4) and −20.3% to −26.5% (GPT-3.5).
- Tokens per task: −9.8% to −16.9%.

The largest token cut in any table is −29.2% (the 1.41x factor, calc.). No cell shows a 40% reduction, so the '40%' appears to be the 1.4x factor.

Success rate is reported (Tables 1-2):
- GPT-3.5: 5.7 to 7.6 points lower than the OpenAI parallel baseline (calc.), e.g. 65.93 → 58.59.
- GPT-4: 0.5 to 1.6 points lower, e.g. 84.29 → 82.68.

'Parallel calls' (Table 3) is the parallelization rate: the share of calls an oracle could group that are actually grouped. For GPT-4 filter operations it rises from 17.04-36.01% to 97.02-99.41%.

What was measured:
- Latency: average time per task, timed in Python over hundreds of isolated GPT endpoints, dropping outliers beyond 2σ.
- 'Token cost': average tokens per task, not dollars; the unit is not stated.
- Task count: not stated in the text. Fig. 2 names 'GeoLLM-Engine-5k'; the Table 3 oracle counts are 1,971 and 4,039 questions.

The recorded 'accuracy not reported' is wrong.

**mechanism and term:**

Mechanism: before the agent runs, a GPT 'fuser' call groups similar tools into fused functions. The agent selects a fused tool, and an executor splits it back into the original tools. It runs independent tools at the same time and dependent ones in order.

The paper's own footnote defines 'parallel' as several tools returned per API call, not tools running at the same time.

Corrected terms:
1. Main term: N (passes/steps) gets smaller, so there are fewer model calls and fewer re-reads of the growing prompt, hence fewer tokens. Quote: "the primary speed-up results from the reduction in the number of steps".
2. Secondary term: overlap in the environment. Table 4, time reduction against the in-context baseline:
   - GPT-4: fused only 7.3-9.0%; fused plus concurrent tool runs 16.2-17.7%.
   - GPT-3.5: 14.4-22.5% versus 26.3-37.1%.
3. c_k rises by one call per task: the fuser.
4. Success rate falls by about 6-8 points on GPT-3.5 and is about unchanged on GPT-4.
5. Money is reported only as a token count.

'More parallel calls' should not be filed under overlap on its own.

**authors and venue:**

Authors:
- Simranjit Singh, Microsoft Corporation
- Andreas Karatzas, Southern Illinois University
- Michael Fore, Microsoft
- Iraklis Anagnostopoulos, Southern Illinois University
- Dimitrios Stamoulis, Microsoft

This resolves 'authors unverified'. arXiv v1, 7 May 2024, cs.PL; no venue on the arXiv page or in the PDF, so it is a preprint.

Credibility rule:
- (i), (ii) and (iv): pass.
- (iii): weak. The benchmark, GeoLLM-Engine, is the authors' own (ref [34]: Singh, Fore & Stamoulis, CVPR 2024 EarthVision workshop). The evaluated task count is not stated in the text; only the name 'GeoLLM-Engine-5k' appears in a figure caption. Models are stated.

Edwin to decide between 'passes with caveat' and 'Not used'.

**formula:**

None for speedup or cost. The paper defines, in words only:
- Parallelization rate (§4 Metrics): the average number of tools called 'in parallel' per API call; §4.2 restates it as a percentage of the calls an oracle could group.
- A look-up-table latency model (§4.2 'Latency Analysis'): the sum of average per-tool and per-API-component runtimes. No equation is given; its modelling error is 14.28% and 17.46%.

## 56. ParaGUI / ParaGUIBench

**read:** arXiv:2607.22689v1, the only version (17 Jul 2026). Full PDF https://arxiv.org/pdf/2607.22689v1 read through pdftotext; not the alphaXiv page.

**verdict:** confirmed

**effect:**

Abstract: ParaGUI reaches a 46.4% success rate, beating Claude Sonnet 4.6 "by 12.9 points while using roughly half the steps and less than half the tokens".

Table III (ParaGUIBench, 233 tasks), ParaGUI vs Claude Sonnet 4.6:
- Success: 46.4% vs 33.5%.
- Average critical-path steps: 38.7 vs 75.9.
- Average tokens per task: 0.81M vs 2.03M.

Set-up:
- Planner GPT-5.4; workers Doubao Seed-1.8; N = 5 workers.
- Each worker runs in an isolated Docker container with 4 GiB RAM and 2 vCPU. Baselines run one GUI-only agent in one such container.
- Worker cap 25 steps; global budget 200 GUI steps; temperature 0, seed 42.
- Each model keeps its own screenshot history: Seed-1.8 keeps 3, Claude up to 10.
- Tokens count the planner plus all workers "with no prompt-cache savings".
- Critical-path steps count worker GUI steps only and exclude planner reasoning and aggregation calls.

Against Seed-1.8, the same worker backbone:
- Steps: 38.7 vs 36.7.
- Tokens: 0.81M vs 0.38M, about 2.1x.
- Success: 46.4% vs 27.9%.

Other results:
- Paired both-correct tasks vs Claude (Table V): 2.7-3.1x fewer steps at 0.26-0.36x the tokens.
- Overall parallelism degree P = 2.13.
- Per-task wall-clock time is not reported. One case study gives a parallel round of 288 s.

Calc.:
- S vs Claude = 1.96.
- Tokens = 0.40x Claude's.
- Total worker steps ≈ 2.13 × 38.7 ≈ 82, more than Claude's 75.9.

**mechanism and term:**

Mechanism: a planner, in one inference, emits parallel tool calls. Each call sends a self-contained sub-task to one of up to 5 GUI workers on separate desktops. Rounds are synchronous, and the planner sees text summaries only, never screenshots.

Terms:
1. Overlap is introduced, a structural change. The critical path becomes the sum over rounds of the slowest worker's steps. Confirmed.
2. N on the critical path is smaller against Claude (1.96x, calc.) but not against the same-backbone Seed-1.8 (38.7 vs 36.7).
3. Total GUI steps across workers are not reduced: about 82, calc.
4. Planner calls add model calls that the step count leaves out.
5. 'Under half the tokens' is mostly a comparison between backbones and screenshot histories, as the paper itself says. Against Seed-1.8 the token count is 2.1x higher.
6. Environment machine hours rise: 5 containers run at once. Not measured.
7. Success rate rises.
8. Time is measured only as a step proxy; no wall-clock per task.

**authors and venue:**

Authors: Zedong Yu*, Qianxing Li*, Zhi Gao†, Liuyu Xiang, Chenrui Shi, Yang Liu, Huiming Wu, Yujie Wei, Yuhao Fei, Yubo Fu, Zhaofeng He†.

Institutions: Beijing University of Posts and Telecommunications; BIGAI (State Key Laboratory for General AI); China University of Geosciences (Beijing); Beijing Institute of Technology.

The paper is a preprint ("PREPRINT, JULY 2026"), submitted to the IEEE with no venue. arXiv v1, 17 Jul 2026, cs.AI. Benchmark and code: github.com/pkgunboat/ParaGUIBench.

Credibility rule: passes. Authors and institutions are verified, and the numbers come from a public benchmark with 233 tasks and stated models.

This resolves 'authors unverified'. Replace the alphaXiv link with the arXiv one.

**formula:**

Yes, §III-C 'Evaluation System' (p. 4):
- L_serial = |τ_serial| = T
- L_parallel = Σ_{r=1}^{R} max_{k∈{1,…,K_r}} s_{r,k}  (Eq. 1)
- S ≜ L_serial / L_parallel
- L_total = Σ_{r=1}^{R} Σ_{k=1}^{K_r} s_{r,k}
- P ≜ L_total / L_parallel

S and P are reported across the whole benchmark as a ratio of means.

## 57. SEAR, DREAM-Chunk (off-topic)

**read:** SEAR: arXiv:2603.01891v2 PDF (13 Aug 2026; v1 was 2 Mar 2026). DREAM-Chunk: arXiv:2606.18589v1 PDF (17 Jun 2026). Abstracts, introductions and metadata read. Numbers were not extracted because both works are off-topic.

**verdict:** corrected

**effect:**

SEAR (abstract): an off-policy reinforcement-learning algorithm that learns with action chunks. It outperforms SimbaV2 on Metaworld manipulation tasks and improves the offline-to-online method QC on OGBench cube-triple. The abstract gives no number.

DREAM-Chunk (abstract): a test-time scaling method for vision-language-action robot policies. It samples several candidate action chunks and picks one using a small latent world model. It improves robustness under action noise on Kinetix and on four manipulation tasks across two robot platforms.

Neither paper measures the time or cost of an LLM agent. The recorded 'sample efficiency' fits SEAR only; DREAM-Chunk is about robustness, and it adds computation at inference.

**mechanism and term:**

Both are robotics work. An 'action chunk' here is a sequence of low-level robot actions run open-loop. There are no LLM calls, prompts, tokens, GUI or web.

Neither changes any term of our formulas, so both should be left out of Part 2. The loose analogy to fewer passes (N) should not be used: DREAM-Chunk increases compute per decision, and SEAR is about how many environment samples RL training needs.

**authors and venue:**

SEAR: C. F. Maximilian Nagy, Onur Celik, Emiliyan Gospodinov, Florian Seligmann, Weiran Liao, Aryan Kaushik, Gerhard Neumann. Autonomous Learning Robots, Karlsruhe Institute of Technology, and FZI Forschungszentrum Informatik. cs.LG; marked 'Preprint'.

DREAM-Chunk: Wenxi Chen, Kaidi Zhang, Chi Lin, Zhiyuan Zhang, Yu She, Yuejiang Liu, Raymond A. Yeh, Shaoshuai Mou, Yan Gu. Purdue University and Stanford University. cs.RO; marked 'Preprint'.

Both author lists are credible, but the works are off-topic. Keep them under 'Not used / off-topic'.

**formula:**

None relevant to agent speed or cost; not extracted.

## 58. Budget-Aware Agentic Routing (BoPO)

**read:** arXiv:2602.21227v1, the only version (arXiv date 4 Feb 2026; the PDF footer says 'Preprint. February 26, 2026'). Full PDF https://arxiv.org/pdf/2602.21227v1 read through pdftotext.

**verdict:** confirmed

**effect:**

The recorded row is BoPO with the small λ. Table 1 is the hard-budget setting: K is the maximum number of large-model calls per task, and 'Use%' = average large calls ÷ K.

AppWorld, K = 15 (success rate %, Use%):
- Always-Large: 66.7, 125. The paper lists it "only for reference and it can exceed the budget".
- BoPO (small λ): 66.5, 88.
- BoPO (large λ): 65.0, 60.

Calc.: large calls per task fall from 18.75 to 13.2, which is −29.6%.

Set-up:
- AppWorld test set: 168 tasks, at most 40 steps each (Table 3).
- Small model GPT-4.1 mini, large model GPT-4.1; router Qwen2.5-1.5B; ReAct prompting.
- Averaged over three seeds; budget-constrained decoding applied to BoPO.

"the computational cost of the router itself is excluded" (§5.1).

Dollars appear only in the soft-budget setting (Fig. 1). They use OpenAI list prices per 1M tokens: GPT-4.1 $2.00 in / $8.00 out, mini $0.40 / $1.60. The only number in the text is ALFWorld above 63% success at $0.125 per task.

The latency analysis is the authors' estimate from assumed token speeds (80 and 90 tok/s for the agent models, 180 tok/s for the router). It puts router overhead under 0.2 s, below 2% of latency. This is not measured.

**mechanism and term:**

Mechanism: at each step a router picks the small or the large model. It is trained first on fine-tuning data built from the always-small and always-large runs, then with RL (BoPO). A hard budget is enforced at inference by budget-constrained decoding.

Terms:
1. Price/tier, chosen per step: confirmed.
2. Success rate about unchanged at K = 15: confirmed.
3. Addition: the paper reports cost inversions (Fig. 5 and the appendix). A small model can cost more per task than the large one when it loops, so passes (N) and tokens can grow when routing down.
4. The hard-budget metric counts only large-model calls: no total dollars, tokens or wall-clock.
5. The router adds one small model call per step, which the metrics exclude.

**authors and venue:**

Authors: Caiqi Zhang (University of Cambridge); Menglin Xia, Xuchao Zhang, Daniel Madrigal, Ankur Mallick, Samuel Kessler, Victor Rühle, Saravan Rajmohan (M365 Research, Microsoft). Corresponding author: Menglin Xia.

arXiv v1, cs.CL; no venue, so it is a preprint.

Credibility rule: passes. This matches references.md.

**formula:**

Yes:
- Eq. (1): J_soft(θ) = E_{τ∼πθ}[ I(success(τ)) − λ Σ_{t=0}^{|τ|−1} c(a_t) ]
- Eq. (2): max_π E_{τ∼π}[I(success(τ))] subject to Σ_{t=0}^{|τ|−1} c(a_t) ≤ B_max
- Eq. (6): C_norm(τ,x) = clip( (C(τ) − C_min(x)) / (C_max(x) − C_min(x) + ε), 0, 1 ), with C(τ) = Σ_t c(a_t)
- Average cost = E_τ[Σ_t c(a_t)]
- Use% = Avg.#LargeCalls / K
- Budget-constrained decoding (§4.4; cited as Eq. (9)): with remaining budget b_t = B_max − Σ_i c(a_i), the router must pick the small model if c(M_large) ≥ b_t.

## 59. WebRouter

**read:** arXiv:2510.11221v1, the only arXiv version (13 Oct 2025). Full PDF https://arxiv.org/pdf/2510.11221v1 read through pdftotext. The published ICASSP version on IEEE Xplore was not read; its metadata was taken from the Crossref API on 28 Sep 2026.

**verdict:** confirmed

**effect:**

Abstract: WebRouter "reduces operational costs by a striking 87.8% compared to a GPT-4o baseline, while incurring only a 3.8% accuracy drop". The 3.8 is percentage points.

Table 1, average over five WebVoyager sites (Apple, Arxiv, Coursera, Google, Huggingface):
- browser-use with GPT-4o: 7.63 steps, 86.1% accuracy, $0.98 per task.
- WebRouter: 8.38 steps, 82.3% accuracy, $0.12 per task.

Set-up:
- Agent: browser-use.
- Model pool: Gemini-2.5 Flash, GPT-4.1 mini and GPT-4o, all through OpenRouter.
- Price = tokens × OpenRouter list rates per 1M tokens: GPT-4o $5 in / $15 out, 4.1 mini $0.40 / $1.60, 2.5 Flash $0.30 / $2.50.
- "each website contains at least 46 distinct tasks for evaluation".
- Router: mDeBERTaV3-base trained on 11,800 samples, β = 0.3, λ = 0.2.

Fig. 5a: prompt tokens are over 70% of the price for every model. Fig. 5b and text: WebRouter is about 14% slower in running time than the GPT-4o baseline.

Calc.: price −87.8%; steps +9.8%; accuracy −3.8 points, or −4.4% relative.

**mechanism and term:**

The terms are confirmed; one point needs to be made precise. A 'query' is the prompt of one step: goal, action history and current web state. So the router chooses a model per call, like BoPO, not per task.

Terms:
1. Price/tier smaller: confirmed.
2. N larger (7.63 → 8.38 steps): confirmed.
3. Success lower (86.1% → 82.3%): confirmed.
4. Addition: wall-clock per task is about 14% longer (Fig. 5b).
5. The router's own call is not reported separately.

**authors and venue:**

Authors: Tao Li (NUAA, College of AI); Jinlong Hu (HKBU); Yang Wang (Beihang, SKLCCSE Lab); Junfeng Liu (Pengcheng Laboratory); Xuejun Liu (NUAA).

The arXiv v1 header says it was under review at ICASSP 2026. Crossref confirms publication:
- ICASSP 2026, Barcelona, 3-8 May 2026, pp. 4086-4090.
- DOI 10.1109/ICASSP55912.2026.11464950, published 3 May 2026.
- Same five authors and affiliations.

It is a conference paper, so doc2's 'preprint' label is out of date. The numbers were checked against arXiv v1 only.

**formula:**

Yes:
- Eq. (2): C(q_i, M_t) = n_p·c_p^(t) + n_c·c_c^(t), where n_p and n_c are prompt and completion tokens.
- Eq. (3): s_i^(t) = P(q_i, M_t) × S_cost(C_i^(t)). S_cost is U(c) = exp(−c), min-max normalised across models.
- Eq. (6): L_ca-VIB = (1/N) Σ_i E[−log p_φ(y_i|z_i)] + β·KL[p_θ(m_i|q_i) || r(m_i)] + λ·E[Σ_t p_φ(y_t|z_i)·C(M_t)]. Here C(M_t) is a fixed per-token unit cost of the model, e.g. c_p + c_c.

The paper gives no speedup formula.

## 60. W&D (scaling parallel tool calling)

**read:** https://arxiv.org/abs/2602.07359 (only version: v1, submitted 7 Feb 2026) and https://arxiv.org/pdf/2602.07359v1 (PDF header dated 2026-02-10), read in full with pdftotext. Paper sentences are paraphrased here because of a quoting limit; all figures are exact.

**verdict:** confirmed

**effect:**

§3.2 'Main result', p.4, the paragraph under 'Tool call scaling' (it refers to Fig. 3a / Table 1). Benchmark: BrowseComp, first 100 samples; model GPT-5, medium reasoning effort. With single tool calling the agent reaches 66% accuracy, costs $102.5 for the 100 tasks ('tool calling and LLM API fees') and averages 1522.6 s per trace. With parallel tool calling at 3 tool calls per turn it reaches 68% at $65.7 per 100 tasks (paper: 35.9% reduction) and 904.2 s wall-clock (paper: 40.6% reduction).

Conditions the claim omits:
(a) Tools (§3.1): Serper Google search plus a Jina scraping tool whose page content is summarised by Gemini-2.5-Flash (thinking off), run on the MCP-Universe framework. The $ figure therefore includes search, scrape and summariser fees, not LLM tokens only.
(b) The number of calls is forced by a user message before every call: at least m and at most m+1 calls (Fig. 2). '3 tools' means 3–4 calls per turn. A countdown message and a forced-answer message at the turn limit are also used (App. A, Figs. 10–11).
(c) Table 1 has 1 tool at 66% (45.7 avg turns, 100-iteration limit). 3 tools reach 68% twice: 16.0 turns at the 25-iteration limit and 23.8 turns at the 100-iteration limit (Table 3 'Constant 3 Tools' 68 (23.8)). The text does not say which 3-tool run the $65.7 / 904.2 s belong to.
(d) No token counts are reported.
(e) 66→68% is 2 questions out of 100, one run, no significance test (calc.).

Calc.: cost per correct answer $1.55 → $0.97 (−37.8%).

**mechanism and term:**

Mechanism correct: the model's native parallel function calling, with the count forced per turn by a prompt and depth capped by a max-turn limit. The paper treats step, iteration and turn as the same thing (footnote 4).

How it maps to the terms:
- N smaller: 45.7 → 23.8 (or 16.0) turns, with one model call per turn, so model calls fall with N.
- Overlap saving: introduced within a pass. The m calls are executed in parallel, so each pass's tool wait becomes roughly the slowest call rather than the sum.
- Decode per task smaller: an author argument, not measured.
- Context growth: each pass now appends m observations, so growth per pass is larger but there are fewer passes.
- Money: mixed. Total tool calls per task probably rise (≈46 → ≈71–95, calc. from turns × 3–4), so tool fees rise while LLM fees fall; the published $ mixes the two.
- Success rate: +2 pp, not significant.

Does not generalise to open models (Table 2): Qwen3-235B-A22B-Thinking went from 8% at 18.5 turns to 11% at 52.1 turns, so turns went UP; DeepSeek-V3.2 went from 38% at 78.0 turns to 39% at 52.5.

Workload caveat: deep-research search/scrape calls are read-only and independent, which is what makes parallel calls safe; not a GUI or form-filling workload.

The fuller term list is right: overlap saving + N smaller + money smaller. Add decode smaller (claimed, not measured) and the tool-fee caveat.

**authors and venue:**

Correct. Xiaoqiang Lin* and Jun Hao Liew* (equal contribution), Silvio Savarese, Junnan Li; Salesforce AI Research (arXiv abs page and PDF p.1). arXiv shows no comments or journal reference, so it is a preprint with no venue. It passes the references.md rule: a company research group, public benchmark (first 100 BrowseComp questions), model stated. arXiv title spacing: 'W&D:Scaling Parallel Tool Calling for Efficient Deep Research Agents'. Other result in the paper: 62.2% on the full BrowseComp with GPT-5-medium and parallel calls, against OpenAI's reported 54.9% for GPT-5-High (a different setting).

**formula:**

§2.1, Eqs. (1)–(3) define traces, not a speedup or cost formula.
- Eq. (1): τ_seq = X, (R_1,A_1,O_1), …, (R_{T−1},A_{T−1},O_{T−1}), (R_T, Ŷ), with R_t, A_t = f_θ(⟨X, (R_1,A_1,O_1), …, (R_{t−1},A_{t−1},O_{t−1})⟩).
- Eq. (2): τ_par is the same trace with A_t^par = {A_t^(1),…,A_t^(m)} and O_t^par = {O_t^(1),…,O_t^(m)}.
- Eq. (3) adds a user message U_t before each step.
- Eqs. (4)/(5), §5 schedulers: Ascending sets m_t = 1 for t≤25, 2 for 25<t≤50 and 3 for t>50; Descending reverses it.

The efficiency argument (§2.1) is only verbal: one R_t replaces m reasoning traces (fewer decode tokens), and calls in a turn run concurrently (less environment wait).

## 61. TPS-Bench (dependency-aware tool scheduling)

**read:** Published version: ACL Anthology https://aclanthology.org/2026.acl-long.1614/ and its PDF (Proc. ACL 2026 Vol. 1 Long Papers, pp. 34949–34961, DOI 10.18653/v1/2026.acl-long.1614), read in full. For comparison: arXiv:2511.01527v1 (3 Nov 2025, the only arXiv version), PDF read.

**verdict:** corrected

**effect:**

ACL Table 3, p. 34956: Qwen3-1.7B on TPS-Bench-Hard (100 tasks, App. C), origin → GRPO:
- Tool selection score: 65.26% → 82.34%
- Task completion rate: 26.75% → 35.17%
- Input tokens: 7.8k → 7.5k
- Output tokens: 2.2k → 1.6k
- Turns: 2.4 → 1.9
- Time: 42.0 → 34.8 (seconds per task, as in Table 1)
Calc.: −17.1% time, +8.42 pp completion.

The paper's own text gives smaller figures: a 6% completion gain and a 14% time reduction with 597 samples (abstract; intro p. 34950; §5 'Result Analysis' p. 34956).

The source of the conflict is now identified. arXiv v1 Table 3, with 100 RL samples, has GRPO at 81.18% / 33.13% / 7.3k / 1.0k / 2.1 turns / 36.1, which gives −14.0% and +6.38 pp (calc.). So 14% / 6% are v1 figures that were left in the ACL text after the table was re-run on 597 samples. Cite the ACL Table 3 values and label the % as calc.

Conditions:
- Time for Qwen3-1.7B is measured locally on vLLM with four NVIDIA A100s (Table 1 note, §3.3). Other models are timed through their APIs.
- Completion rate is an LLM-as-judge score (Gemini-2.5-Flash): the task is split into subtasks and the rate is the share judged completed. It is partial credit, not binary success.
- Training (§5): GRPO, 597 samples kept separate from the 200 evaluation tasks (App. C), 5 epochs, actor lr 1e-6, 5 rollouts per sample, veRL defaults, 125 iterations (intro). The reward comes from Gemini-2.5 Flash scoring task completion and the degree of parallelism.
- The GRPO row has no $ cost.

**mechanism and term:**

Mechanism correct: an RL-trained scheduling policy that runs independent subtasks' tool calls in parallel in one turn and dependent ones sequentially.

Terms:
- Overlap saving: more independent calls issued per turn.
- N smaller: turns 2.4 → 1.9.
- Decode smaller: output tokens 2.2k → 1.6k.
- Prefill slightly smaller: input 7.8k → 7.5k.
- Success rate up, but it is a judged completion fraction.

The claim's 'overlap saving; success rate up' is right but incomplete: add N and decode.

Scale caveat: a 1.7B model going from 26.75% to 35.17%, far below the benchmark's best (GLM-4.5, 64.72%).

The benchmark itself is also useful evidence. Table 1 shows the trade-off: GPT-4o schedules in parallel (2.5 turns, 76.84 s, 45.08%) while GLM-4.5 is sequential (35.0 turns, 217.8 s, 64.72%) on Hard. Fig. 6 compares parallel against sequential scheduling for four models. Workload: 141 MCP tools on 15 servers, not GUI.

**authors and venue:**

Venue confirmed: ACL 2026 main conference, long paper, San Diego, July 2026 (ACL Anthology page). Authors in the ACL version: Hanwen Xu*, Xuyao Huang*, Yuzhe Liu, Zhijie Deng†; School of Computer Science, Shanghai Jiao Tong University. Note that arXiv v1 lists five authors, adding Kai Yu as 4th; cite the ACL author list. It is a conference paper, so it passes. It is indeed absent from references.md (grep). A web-search summary called it ICLR 2026; nothing supports that, and the ACL Anthology is authoritative.

**formula:**

§4.2 'Cost', p. 34953–34954:
- Eq. (1): v(m,t) = C_m(t) / R_m(t). This is cost-of-pass: the cost of completing task t once with model m, divided by the task completion rate.
- Eq. (2): C_m(t) = n_in(m,t)·c_in(m) + n_out(m,t)·c_out(m), with n_in and n_out the input and output tokens and c_in and c_out their per-token prices.

This is exactly our 'cost per success = cost per attempt ÷ success rate', with only two billing classes (no cache classes). Table 2 gives Qwen3-1.7B on Hard a cost of 1.3×10⁻³ $ and a cost-of-pass of 4.9×10⁻³ $.

## 62. OSWorld 2.0 batched-action setting

**read:** https://arxiv.org/abs/2606.29537 (v1 28 Jun 2026; v2 13 Jul 2026). PDF v2 (header dated 2026-07-15) read in full. PDF v1 Table 3 compared: identical to v2.

**verdict:** confirmed

**effect:**

Table 3, §3.2 p.8. Per-task averages over the 108 tasks, 500-step budget, highest thinking level (max for Claude).

Batched:

| Model | Binary | Partial | Cost/task | Tool calls | Output tokens | Steps |
|---|---|---|---|---|---|---|
| Opus 4.8 | 20.6% | 54.8% | ~$72.4 | 481.8 | 224K | 103 |
| Opus 4.7 | 18.2% | 48.91% | ~$33.6 | 597.1 | 150K | 160.7 |
| GPT-5.5 | 13.0% | 49.5% | ~$25.5 | 149.8 | 37.1K | 95.2 |

Single action:

| Model | Binary | Partial | Cost/task | Tool calls | Output tokens | Steps |
|---|---|---|---|---|---|---|
| Opus 4.8 | 18.5% | 49.3% | ~$76.1 | 190.5 | 259.5K | 190.5 |
| Opus 4.7 | 13.9% | 49.1% | ~$35.8 | 318.4 | 150.5K | 318.4 |

The claim's numbers are correct. It omits Opus 4.8 single-action steps (190.5) and the cost columns.

Setup (§3.1, p.8):
- Screenshot observations; Claude acts through the native claude_computer_use tool.
- Claude batches only when the batch tool is explicitly enabled. GPT-5.5 always batches, so there is no single-action GPT-5.5 run.
- 16K output cap; a 3 s pause after each action.
- AWS t3.2xlarge in us-east-1; the evaluator and the user simulator are Claude Sonnet 4.6; release v2026.06.24.
- No wall-clock time per task anywhere in the paper (searched).

The §3.2 text disagrees with Table 3 in three places. It says Opus 4.7 needs ~190 turns for 18.2% (the table has 160.7; 190.5 is Opus 4.8 single). It gives Opus 4.8 as 20.5% (table 20.6%) and its partial as 54.2% (table 54.8%). Use Table 3.

Calc.:
- Steps: −45.9% (4.8), −49.5% (4.7).
- Tool calls: ×2.53 and ×1.88.
- Actions per step: ≈4.7 and ≈3.7.
- Cost per task: −4.9% and −6.1%.
- Cost per success: $411 → $351 (−14.6%) for 4.8; $258 → $185 (−28.3%) for 4.7.

**mechanism and term:**

Mechanism mostly right, but one detail is not in the paper. It defines 'batched' only as multiple tool calls per step, one step being one observe-and-act cycle. It does not state the execution order inside a batch or whether screenshots are taken between batched actions. Reword to: 'one model call per step emits several tool calls; the next observation comes at the next step.'

Terms:
- N smaller: steps, i.e. model calls, per task roughly halve.
- Success rate up in binary terms: +2.1 pp for 4.8, +4.3 pp for 4.7. Partial: +5.5 pp for 4.8, flat for 4.7 (49.1 → 48.91).
- Money slightly lower: ~$76.1 → ~$72.4 and ~$35.8 → ~$33.6. Output tokens 259.5K → 224K for 4.8, flat for 4.7.
- Environment act/wait per task probably GROWS. Tool calls rise ×1.9–2.5 and a 3 s pause follows each action. If the pause applies per tool call, that adds ≈874 s for 4.8 and ≈836 s for 4.7 (calc., assumption). So the direction of task time is unmeasured.

One run per configuration on 108 tasks, so the success differences are about 2–5 tasks (calc.).

The claim's 'N smaller; success rate up' is right. Add 'money slightly smaller' and 'environment actions per task larger; no wall-clock'.

**authors and venue:**

Correct. The paper is signed 'XLANG Lab and Collaborators'. The arXiv metadata lists 36 authors, led by Mengqi Yuan, Zilong Zhou and Xinzhuang Xiong (equal contribution, per the arXiv comments), with Tao Yu as corresponding author. App. A gives affiliation 1 as XLANG Lab, University of Hong Kong; others include UCSD, Columbia, UCSB, Mila, Uniphore, Snorkel AI, UW–Madison, Alibaba Qwen, Ohio State, Simular and NeoCognition. It is a preprint: arXiv comments read '68 pages, 42 figures', with no venue. Passes.

**formula:**

None. The paper defines turns as the number of times an agent observes and acts against the environment, and argues in words that each turn adds latency (§3.2, discussion of Fig. 6). It gives no formula for speed or cost.

## 63. OSWorld-Human grouped-action bound

**read:** https://arxiv.org/abs/2506.16042 (v1 19 Jun 2025; v2 18 May 2026). PDF v2 read in full; HTML v2 (https://arxiv.org/html/2506.16042v2) read for the exact formula notation. MLSys page https://mlsys.org/virtual/2026/poster/3642 opened.

**verdict:** confirmed

**effect:**

Table 4 'Average Steps per Trajectory by Application', §4. LibreOffice Calc: 13.2 steps single-action, 4.5 grouped. Correct.

Definitions (§4.2): a grouped-action trajectory is made of groups of actions that can be executed correctly from the same screenshot. Each group counts as one step; single-action trajectories use one step per action. The trajectories are human-constructed and verified references for all 369 OSWorld tasks (§4.1).

Other rows, single → grouped: OS 3.9→2.0, Thunderbird 6.7→3.8, VS Code 3.6→2.0, Writer 7.5→3.2, VLC 5.1→3.7, GIMP 2.8→2.0, Impress 7.8→4.0, Chrome 5.8→4.3.

Calc.: the ratio ranges from 1.35× (Chrome) to 2.93× (Calc). The browser row, the one closest to web workflows, has the SMALLEST headroom; Calc is the best case, not typical.

Table 5 (same paper): the best agent, Agent S2 with Gemini 2.5 (50 steps), scores 41.4% success but 15.6% single-action WES and 9.6% grouped-action WES.

**mechanism and term:**

The term is correct: N, that is passes and model calls. §4.2 says the grouped trajectory implies one observation plus one model call per group.

Calling it a 'bound' is our reading. The paper calls these the minimal humanly-perceived steps and notes that an agent can beat the human reference (WES⁺ can exceed 1). Say 'human reference / headroom estimate', not a strict upper bound.

It is not an accelerator: no system is evaluated with grouping. §5.3 lists action grouping as future work and warns that content newly appearing on screen can invalidate the queued actions (stale state).

**authors and venue:**

Confirmed. Reyna Abhyankar* and Qi Qi* (equal contribution), Yiying Zhang; University of California, San Diego (Zhang also GenseeAI, Inc.). The PDF footer reads Proceedings of the 9th MLSys Conference, Bellevue, WA, USA, 2026. The MLSys 2026 virtual poster page lists the same three authors with creditText 'MLSys 2026'. Conference paper; passes.

**formula:**

§5.1:
- WES⁺ = (1/n) Σ_t^n r_t · t_human / t_agent, where r_t = 1 for success and 0 for failure.
- WES = WES⁺ · (1 − t̄_fail / S), where t̄_fail is the mean steps over failed tasks and S the step budget.

This is an efficiency score, not a speedup formula. §4.2 states that one observation and one model call per group would cut steps and latency; that is a qualitative statement.

## 64. OS-Catalyst (pointer only)

**read:** Could not read.
- OpenReview forum https://openreview.net/forum?id=QpKXNYtF3x and the OpenReview API (api and api2 notes?id=QpKXNYtF3x) returned a browser-verification challenge: HTTP 403 ChallengeRequiredError to curl, and a 'Verifying your browser' page to WebFetch.
- The PDF link found by web search (https://openreview.net/pdf/359b888c9ee42ff45ecefac907b19167c8354e39.pdf) returned the same challenge page. The challenge was not bypassed.
- The Wayback availability API and the Semantic Scholar API both returned HTTP 429.
- Two web searches found no arXiv version.

**verdict:** could not read

**effect:**

Not verified. A search-engine summary, not the paper itself, describes the method as predicting a sequence of actions per observation, with a dataset and models built in WorkArena, 'up to 50%' lower task execution time than step-by-step, and the PDF as under double-blind review. None of this may be used. I could also not confirm that this PDF belongs to forum QpKXNYtF3x.

**mechanism and term:**

The intended term (N: fewer observations and model calls per task, several actions per call) is plausible but unverified. Keep it as a pointer only; do not put it on slides.

**authors and venue:**

Not verified. If the OpenReview PDF is an anonymous double-blind submission, as the search summary suggests, 'Yuan et al.' cannot be checked against it. It then fails credibility rule (i) until a de-anonymised version (camera-ready or arXiv) is read. Venue and decision status are unknown.

**formula:**

Could not read.

## 65. SpecBox

**read:** https://arxiv.org/abs/2607.23933 (v1 27 Jul 2026; v2 5 Aug 2026). PDF v2 read in full. PDF v1 diffed against v2: the only change is a figure legend ('Laplace' became 'PredBox'); all numbers are identical.

**verdict:** corrected

**effect:**

Abstract p.1: P99 end-to-end latency is up to 2.9× lower relative to the ON-DEMAND sandbox baseline, and peak memory is 45.9% lower compared to permanently RESERVED sandbox deployments. Each number has its own baseline; the claim's 'vs always-warm and on-demand' blurs this.

Conditions:
- 2.9× (§5.2.2, Fig. 10a): P99 of per-session end-to-end latency at the highest load, QPS=20. SpecBox 88.7 s against On-demand 257.2 s (calc. 2.90×). The text calls the system 'Laplace' here, a leftover name.
- 45.9% (§5.2.3, Fig. 10d): Reserved peaks at 80.6 GiB, On-demand stays between 24.3 and 40.4 GiB, SpecBox tops out at 49.4 GiB. From these stated peaks, 1 − 49.4/80.6 = 38.7% (calc.), so the 45.9% cannot be reproduced. SpecBox's peak memory is also ABOVE On-demand's.
- Other results: cumulative sandbox provisioning latency 4.53× lower than On-demand and within 10.6% of Reserved (§5.2.1). Peak CPU 22.8–23.3% lower than both baselines (about 12.2 cores against 15.8–15.9). Semantic cache: waiting latency 412.78 → 141.93 ms (2.91×) at a 37.4% hit rate. The conclusion's '97.9% prewarming hit rate' appears in no table (Table 2 gives a top-3 hit rate of 0.992 for Retrieval).

Setup (§5.1):
- One server with a 16-core CPU, 256 GiB RAM and 2 TB NVMe; Docker containers; AgentScope; Qwen3.5-Max through the DashScope production API.
- 200 multi-turn trajectories generated by an LLM planner from MCP-Bench [40] tools on 32 MCP servers (Playwright, Jupyter, Neo4j, and others). Sessions are 1–10 steps, 20 traces per length, averaging 6.4 steps per session and 2.96 tools per step; replay uses seed 0.
- At low QPS, mean provisioning latency was under 4 s for all three modes.
- No task-quality or success metric; no code or data release statement.

**mechanism and term:**

Mechanism correct: streaming-intent prewarm, stochastic prefetch over a sandbox dependency graph, semantic result cache, zero-copy out-of-band transport.

Terms:
- Environment wait smaller: sandbox cold start (T_env_prep), plus T_data_io and T_sandbox_exec on cache hits.
- Overlap saving: prewarm during decode and during the previous step; the paper itself uses 'overlapping'.
- Money, environment machine resources: peak memory lower than Reserved but higher than On-demand; peak CPU lower than both.
- It does not change N, tokens or success, and quality is not measured.

The gains are tail and concurrency effects (P99 at QPS=20). A single session at low load gains little.

Fix the claim's 'not a browser': Playwright MCP is among the 32 servers. Say 'MCP tool servers (incl. Playwright MCP); no GUI or web-task benchmark and no success metric.'

This resolves dossier E176's open point: the 2.9× is against On-demand.

**authors and venue:**

Confirmed. Yihui Zhang, Tianyu Wo, Jinghao Wang, Xiaoyang Sun, Menghao Zhang, Cangzhou Yuan, Li Li, Chunming Hu, Albert Y. Zomaya, Renyu Yang (corresponding). Affiliations: Beihang University; University of Leeds (Sun); The University of Sydney (Zomaya). These are shown on the arXiv abs page and PDF p.1.

The PDF header 'Conference'17, July 2017, Washington, DC, USA' is an unfilled ACM template, so there is no venue: it is a preprint.

Credibility rule (iii) is borderline. The numbers come from a trace set the authors built from MCP-Bench tools with an LLM planner (200 trajectories, model named), not from a released public task set. Flag this in references.md next to 'Backs E176'.

**formula:**

§2.3, Eq. (1): T_step^(N) = T_context^(N) + T_generation^(N) + T_env_prep^(N) + T_data_io^(N) + T_sandbox_exec^(N).

The first two terms are LLM inference (context processing, token generation). The other three are the runtime's share: getting the sandbox ready, exchanging inputs and results, and running the tool.

How SpecBox acts on it:
- It overlaps T_env_prep with the rest of T_generation within a step.
- It prefetches step N+1's sandbox during step N.
- Cache hits skip T_sandbox_exec.
- Out-of-band shared memory makes T_data_io independent of payload size.

Mapping to our loop: T_context ≈ prefill, T_generation ≈ decode, and the other three terms ≈ the environment part of a pass.

## 66. SpecHop (arXiv:2605.21965)

**read:** https://arxiv.org/pdf/2605.21965v1 (v1, 21 May 2026, the only version; pdftotext). Formulas checked against https://arxiv.org/html/2605.21965v1. Project repo github.com/mehrdadsaberi/spechop (README only). Local copy: scratchpad/wf-part2/2605.21965v1.pdf

**verdict:** corrected

**effect:**

The dossier had no verified number. The abstract says latency falls by up to 40% in some settings. §4.2 and Table 1 give the source: RelLat = 0.60, a 40% cut in total execution time, against an oracle bound RelLat* = 0.50.

Conditions for the 0.60:
- Benchmark: 2WikiMultihopQA, validation split, 2–4 hops plus 2 extra hops of budget.
- Target tool: web search (DuckDuckGo, 5 results, 3-second page-fetch timeout).
- Speculator: GPT-4o (p̂ 0.68, α̂ 0.19, β̂ 0.10).
- Generator: CoRAG-Llama3.1-8B-MultihopQA.
- Threads: k → ∞ (no limit on active threads).
- Hardware: two NVIDIA L40 48GB.
- Baseline: standard sequential multi-hop execution with the same generator and tool.

How latency was measured (App. D.1): the calls were run sequentially and each stage's wall-clock time was recorded. RelLat then comes from a deterministic discrete-event simulator that replays the continuous-speculation schedule over those times. It is a simulated schedule on measured stage times, not a live concurrent run.

Task count: not stated anywhere in v1. I searched the PDF text and the HTML.

Absolute times (Table 2, Llama 3.1 8B speculator):
- Web search: 21.13→16.10 s (2Wiki), 15.59→11.17 s (MuSiQue), 20.17→15.07 s (DeepResearch-9K, train split, difficulty 2, 10-hop budget).
- E5 retrieval: 3.81→3.47, 3.89→3.37 and 5.49→4.83 s.
- Accuracy holds: EM 68.7→69.3 on 2Wiki with web search.

Cost (Fig. 2 and §4.2; DeepResearch-9K, GPT-4o speculator, web search, k = 3): RelLat 0.75 (0.71 at k → ∞). Target-tool calls per query go 5.48→10.69 and generator calls 5.48→17.83. App. E says the method 'generally' raises overall computation cost.

Cache speculator (Fig. 3): a cache holding 25% of the index gives web-search RelLat 0.64.

**mechanism and term:**

The row's mechanism is wrong for this paper. 'n-gram tool predictors' belongs only to the speculative-tools GitHub repo.

What SpecHop does: a fast speculator predicts each tool observation. It is either a small LLM answering the sub-question from memory or a small cached E5 index. The agent carries on from the predicted observation in extra threads while the real tool runs. A rule-based verifier then commits or rolls back (normalisation, numeric match, ≥72% token coverage or Jaccard ≥0.55). A human check of 100 verifier decisions gave 100% precision and 96.2% recall (App. C.3).

Term changed: overlap saving. The wait on the tool is overlapped with the next hops' decode and the next tool calls, i.e. pipelining across passes.

Side effects:
- Model calls c_k go up about 3.3× at k = 3 (calc., 17.83/5.48).
- Tool calls go up about 2× (calc., 10.69/5.48).
- Money therefore goes up.
- Success rate is unchanged (EM/F1 within noise, Tables 2 and 4).

Scope: read-only retrieval QA only; no web or GUI actions.

Proposed D-entry: the dossier §3.3 row groups four unrelated works under one mechanism. The row should be split, and the 40% labelled a simulated replay.

**authors and venue:**

Mehrdad Saberi and Keivan Rezaei (equal contribution) and Soheil Feizi, University of Maryland, College Park. arXiv cs.CL; the abs page has no comments or journal-ref, and I found no OpenReview record. It is a preprint.

Credibility rule: (i), (ii) and (iv) pass. (iii) fails as written: the benchmarks and models are public and stated, but the task count is not. Under the rule it goes to 'Not used' unless Edwin relaxes the task-count condition.

**formula:**

All in the paper's own symbols. Note that α and β here are SpecHop's ratios, not the deck's symbols.
- §3: T_hop = T_seg + T_target; expected total N·E[T_hop].
- Obs. 1: E[T_hop^spec] = E[T_seg] + p·E[T_spec] + (1−p)·E[T_target].
- Cor. 1: RelLat* = 1 − p(1−α)/(1+β), with α ≜ E[T_spec]/E[T_target] and β ≜ E[T_seg]/E[T_target].
- Thm 2: L_k(N) = N(E[T_seg] + ((μ_k−1)/μ_k)·E[T_spec] + (1/μ_k)·E[T_target]) + O(1), where μ_k = (1−p^k)/(1−p).
- Cor. 3: RelLat_k = (β + α + (1−α)(1−p)/(1−p^k))/(1+β).
- Thm 4: P_starve(k) ≤ Φ(((1+β) − k(α+β)) / (ν·√(kα² + (k−1)β² + 1))); k* = ⌈(1+β)/(α+β)⌉ gives P_starve ≤ 0.5.

## 67. IdleSpec (arXiv:2605.22154)

**read:** https://arxiv.org/pdf/2605.22154v1 (v1, 21 May 2026, the only version). Local copy: scratchpad/wf-part2/2605.22154v1.pdf

**verdict:** corrected

**effect:**

The dossier had no number and filed this under overlap saving. It is an accuracy method, not a speed-up.

Accuracy (abstract and Table 1):
- Gemini-2.5-Flash: average accuracy over GAIA Levels 1–3 and FRAMES goes 50.5 → 55.6. The '+5.1%' is +5.1 percentage points.
- Gemma4-E4B: 30.9 → 35.5. Qwen3.5-4B: 33.2 → 40.0.
- Conditions: GAIA full validation split, 165 tasks (53/86/26 by level); FRAMES first 50 samples; mean of 3 seeds; OAgents framework.
- Baseline: vanilla, with no computation during idle time.

MLE-Bench Lite (Table 2): 22 competitions, 24-hour budget per task, single seed, OpenHands, Gemini-2.5-Flash. Any Medal goes 36.4% → 45.5% (+9.1 points).

Wall-clock (App. B.3, Table 8): full GAIA, Gemini-2.5-Flash, single fixed seed, isolated environment, per-task latency.
- Level 1: 107 → 99 s.
- Level 2: 191 → 196 s.
- Level 3: 374 → 376 s.
So wall-clock is roughly unchanged.

Tokens (Table 3; GAIA Level 2, Qwen3.5-4B, output tokens): vanilla 7,126 at test time; IdleSpec 5,284 during idle time plus 5,966 at test time = 11,250. That is about +58% output tokens (calc.).

Latency comparison (Fig. 3; vLLM on an A6000): Sequential Revision is about 1.30× and Planning about 1.33× slower than vanilla; IdleSpec stays close to 1×.

Idle share (Fig. 2a): reasoning is 19.0% / 10.27% / 7.40% of time on GAIA / FRAMES / MLE-Bench. §3.1 says tool execution is more than 12.5× reasoning time on MLE-Bench. The model behind Fig. 2 is not stated in §3.1.

**mechanism and term:**

Correction: this is not speculative tool execution and not an n-gram predictor.

What IdleSpec does: while a tool runs, the agent repeatedly drafts candidate plans. Drafts are either 'progressive' (assume the observation helps) or 'recovery' (assume it fails), chosen by Thompson sampling from a Beta posterior, with at most 5 kept. Drafting stops when the observation arrives, and the drafts are fed into the next reasoning step.

Term changed: success rate goes up. The method introduces overlap but spends it on extra decode rather than on saving time: overlap saving ≈ 0 and wall-clock is about the same. Output tokens and money go up; App. A.7 notes the higher monetary cost on metered APIs.

For Part 2 it belongs under the success-rate term: cost per success improves through the denominator. It should not sit under overlap saving.

**authors and venue:**

- Daewon Choi, Kyunghyun Park, Woomin Song, Jinwoo Shin: KAIST.
- Sai Muralidhar Jayanthi, Aram Galstyan: Amazon AGI.
- Saket Dingliwal: Together AI (work done at Amazon).

arXiv cs.AI, no venue on the abs page. Passes (i)–(iv): public benchmarks, task counts and models all stated.

**formula:**

There is no speed-up or cost formula. The paper defines:
- Idle-time utilisation (App. B.1, Eq. 5): ITU_task = Σ_k t^(k)_LLM-on-idle / Σ_k t^(k)_idle ∈ [0, 1]. IdleSpec reaches 34.6% on GAIA with Qwen3.5-4B, against 13.2% for Sleep-Time Compute.
- The strategy posterior (Eqs. 2–4): p = Pr(ℓ = PROG), p ~ Beta(α, β), with a count update after each forecast.

## 68. Speculative tool calls (arXiv:2512.15834)

**read:** https://arxiv.org/pdf/2512.15834v1 (v1, 17 Dec 2025, the only version). Equations checked against https://arxiv.org/html/2512.15834v1, and pages 1 and 11 rendered to read Figs 1, 6, 7 and 8. Local copy: scratchpad/wf-part2/2512.15834v1.pdf

**verdict:** corrected

**effect:**

The abstract claims throughput gains of 'several hundred tokens per second'. The largest gain plotted is +196.4 tok/s (Fig. 1, star label). Its caption says up to 196 tok/s for 32 gpt-oss-120b agents sharing one vLLM server. The point is at 2.0 s average tool latency: about 1,130 vs 935 tok/s, read off the plot. Throughput is tokens generated per second per agent, averaged over agents (§5). Which variant Fig. 1 shows is not stated; engine-side results exist only for one agent, so it is presumably client-side (inference).

The dossier should record +196.4 tok/s (Fig. 1) instead of the abstract's wording.

Time saved, client-side (Fig. 6, Observation 2): 6–21% of per-agent end-to-end time.
- 32 async agents, xLAM-2-8B speculator, one speculation per generation, average tool latency 0.5–3 s.
- xLAM-2-1B saves only about 1.5–5% (read from Fig. 6).

Time saved, engine-side (Fig. 8, Observation 3): 2–3% more than client-side. This was run with one async agent only, because vLLM's speculative decoding had high overhead at batch size > 1. The gain is best for tools of 0–1 s.

Commercial models (Fig. 7): gpt-5 as the main model with gpt-5-nano speculating.
- One speculation: about 9.5% time saved for about 4% extra cost per 100 turns (main-model cost $0.606 per 100 turns).
- Nine speculations: about 13.4% saved for 25–30% of the main generation's cost (text).
- The task count for this run is not stated.

Setup (§4):
- BFCL prompts and tool specifications.
- Tools are not executed. Pre-computed outputs come from an in-memory cache, with latencies drawn from normal distributions (means 0–0.5 s and 0–3 s).
- Each agent completes 32 tasks; M ∈ {1, 8, 32} agents; each configuration run 5 times.
- Main model on one A100 80GB; xLAM-2 1B/3B/8B speculators on three A100s. xLAM-2-8B hits α ≈ 0.8.
- Baseline: standard vLLM inference without speculation.

**mechanism and term:**

The mechanism is not 'n-gram' prediction. A small tool-calling model (xLAM) predicts the next tool call from the same prompt, and the predicted tool is launched at once. Only stateless, cheap tools are speculated (§3.1).

Three optimisations, each mapping to a term:
- O1, overlap saving: tool time is hidden behind main-model generation. This is the primary effect.
- O2, decode: the engine-side tool cache drafts the tool-call tokens, which are verified in one forward pass, saving δ(t_i − 1) per turn.
- O3, queueing/overhead: the sequence stays resident, so the eviction and re-scheduling overhead 2Ko is avoided and prefix reuse is forced, which cuts re-prefill.

Money goes up from the speculator calls (+4% with one gpt-5-nano speculation).

The 'engine-resident' label is right for the engine-side variant only. Side-effecting web actions are out of scope by construction.

**authors and venue:**

The affiliations are printed on the paper, not inferred:
- Daniel Nichols, Charles Jekel, Harshitha Menon: Lawrence Livermore National Laboratory.
- Prajwal Singhania, Abhinav Bhatele: University of Maryland.

arXiv cs.PL, no venue. The acknowledgment carries LLNL-CONF-2014336-DRAFT; OpenReview/dblp list it as CoRR only.

Credibility: passes (i), (ii) and (iv). For (iii), the benchmark (BFCL), the model and 32 tasks per agent are stated. Label the numbers as measured with synthetic tool latencies and cached tool outputs.

**formula:**

All in the paper's own symbols.

Client-side model (§3.1.1):
- Eq. 1: T_standard = N(G+T); T_spec = αN·max{G, g+T} + (1−α)N(G+T). G = mean main-model generation time, g = mean speculator generation time, T = mean tool time, α = acceptance rate.
- Eq. 2: S_spec = (G+T)/(α·max{G, g+T} + (1−α)(G+T)).
- Lemma 1: S_max = (G+T)/max{G, g+T} ≤ 2(G+T)/(G+g+T) = 2 − 2g/(G+g+T) < 2, i.e. a 2× cap.

Engine-side model (§3.2.1):
- Eq. 4: T_vanilla = 2Ko + ϕ·Σ_{i=1..K} X_i + δ·Σ(R_i + t_i) + Σ T_i, with X_{i+1} = X_i + t_i + t_{o,i} and X_1 = initial prompt tokens.
- Symbols: o = API/eviction overhead, ϕ = prefill s/token, δ = decode s/token, R_i = reasoning tokens, t_i = tool-call tokens, t_{o,i} = tool-output tokens, T_i = tool time, K = turns.
- Eq. 5: T_cached = 2Ko + ϕ(X_1 + Σ(t_i + t_{o,i})) + δ·Σ(R_i + t_i) + Σ T_i.
- Eq. 6: T*_spec = (1−α)·2Ko + ϕ(X_1 + Σ(t_i + t_{o,i})) + δ(αK + Σ R_i + (1−α)Σ t_i) + (1−α)Σ T_i. At α = 1 this saves 2Ko + δ(Σ t_i − K) + Σ T_i over T_cached.

Eq. 4 is a close source form for the deck's Part 1: queueing overhead, prefill of a prompt that grows each turn (quadratic without a cache), decode, and tool wait.

## 69. speculative-tools GitHub repo (joelvarun/speculative-tools)

**read:** https://github.com/joelvarun/speculative-tools, README.md on the master branch, plus repo and owner metadata from the GitHub API (read 28 Sep 2026)

**verdict:** not found

**effect:**

The repo reports no measured effect. The README only shows demo code that prints a hit rate and 'latency saved' for simulated tools (asyncio.sleep).

Repo facts: created and last pushed on 6 May 2026, 1 star, 0 forks, MIT licence. It lists Speculative Actions, PASTE and 2512.15834 as inspiration.

**mechanism and term:**

This repo is where the dossier row's 'n-gram tool predictors' comes from. It uses an n-gram model over tool-name sequences plus a majority vote over past arguments to predict the next call, pre-runs predicted calls as background asyncio tasks, keeps results in a TTL cache (30 s default), and lets tools be marked speculative=False.

Term: overlap saving, claimed only. Nothing is measured.

The mechanism does not describe SpecHop, IdleSpec or 2512.15834.

**authors and venue:**

An individual GitHub account: no name, no institution, location Bangalore, 149 public repos. It fails the author/institution check that applies even to qualitative mentions.

Recommendation: drop it from the dossier §3.3 row and from the deck. At most, keep it as unlabelled source code with no measurements.

**formula:**

none

## 70. Cost-Aware Speculative Execution for LLM-Agent Workflows (Fareed, arXiv:2606.07846)

**read:** https://arxiv.org/pdf/2606.07846v1 (v1, 5 Jun 2026, the only version). Local copy: scratchpad/wf-part2/2606.07846v1.pdf

**verdict:** confirmed

**effect:**

Confirmed: there are no empirical results.
- App. D is a synthetic validation of five seeded experiments at 'AutoReply' parameters, with no dataset and no LLM call (App. D intro).
- D.6 says the experiments test the method against its own equations; a real-deployment evaluation is left as the next step.
- §14.2 says capacity contention and the runtime overhead of the speculation machinery are not measured, and that App. D is synthetic.
- §10.1 is an illustrative worked example, not a measurement: C_spec $0.0165, L_value $0.05, P 0.733, α 0.5 → speculate.

New finding (calc.): App. D.2 is inconsistent with the paper's own rule.
- D.2 prints a break-even P* = C_spec/(L_value + α·C_spec) ≈ 0.191 at α = 0.5, with L_value $0.064 and C_spec $0.0135.
- Its plotted EVs (P = 0.20 → +$0.0007, 0.47 → $0.0198, 0.62 → $0.0304) equal P·(L_value − α·C_spec) − (1−P)·C_spec.
- Under the §6.1 rule (EV = P·L_value − (1−P)·C_spec ≥ (1−α)·C_spec), break-even is (2−α)·C_spec/(L_value + C_spec) = 0.261 (calc.).
- At P = 0.20, §6.1 gives EV $0.0020 against a threshold of $0.00675, i.e. WAIT, whereas D.2 calls it borderline SPECULATE.
- §7.6's k_crit agrees with §6.1.
Proposed D-entry.

**mechanism and term:**

The row's mechanism is correct. It is a decision rule: speculate iff EV ≥ (1−α)·C_spec, and only when the action passes an admissibility precondition (side-effect-free, idempotent, or stageable behind a commit barrier). Irreversible actions are never speculated, whatever the EV (§3).

Terms: overlap saving (gated) and money (C_spec, priced at separate input and output rates).

Caution: its α is an operator's latency-vs-cost preference dial. It is not an acceptance rate as in 2512.15834 or SpecHop.

It is theory only and cannot back any effect.

**authors and venue:**

Faisal Fareed, AWS. The PDF header shows a single author. arXiv cs.DC, no venue.

It fails rule condition (iv) (single-author industry report) and (iii) (no benchmark). It is not one of the four 'Not used' entries in slides/references.md (Chundru, Li B., Wang X. et al., Iyamu), and references.md does not mention it anywhere.

Recommendation: add it as a fifth 'Not used' entry. Dossier E131 and D109 stay as the record.

**formula:**

All in the paper's own symbols.
- §6.1: L_value = L·λ; C_spec = input_tokens·input_price + output_tokens·output_price; EV = P·L_value − (1−P)·C_spec; threshold = (1−α)·C_spec; speculate iff EV ≥ threshold.
- §4, self-hosted models: C_spec = (unit_price·num_gpus·output_tokens)/(throughput·utilization).
- §7.5: P_lower = Beta⁻¹(γ; α₀+s, β₀+f); speculate iff P_lower·L_value − (1−P_lower)·C_spec ≥ (1−α)·C_spec.
- §7.6: k_crit(α) = (L_value + C_spec)/((2−α)·C_spec).
- App. D.2: P* = C_spec/(L_value + α·C_spec). This one is inconsistent with §6.1; see above.

## 71. Cordon: Semantic Transactions for Tool-Using LLM Agents (arXiv:2606.17573)

**read:** https://arxiv.org/pdf/2606.17573v1 (v1, 16 Jun 2026, the only version). Local copy: scratchpad/wf-part2/2606.17573v1.pdf

**verdict:** corrected

**effect:**

Containment (§6.2): plain execution commits the risky effect in all 45 cases. Adapters built from existing defences prevent 14 before commit, miss 26, and catch 5 only after commit. Cordon intercepts all 45 before commit.

The suite is 45 author-built workflows: 9 defence-boundary categories × 5 risk families, in coding, incident response, documents, office, support and data analysis. There are no web or GUI tasks.

End-to-end (Table 4): 45 workflows; task times include the wait for human approval; model DeepSeek-V4-Pro inside a commercial runtime called 'Agent-H'.

| Mode | Mean task time | LLM calls | Tokens | Approvals |
|---|---|---|---|---|
| Plain | 25.55 s | 162 | 1.89M | 0 |
| Approve-all | 31.35 s | 119 | 1.36M | 45 |
| Reject | 23.64 s | 125 | 1.42M | 36 |
| Mixed | 31.12 s | 127 | 1.45M | 40 |

Two corrections and one addition to the dossier:
- Label: §6.3 states +22.7% for approve-all (+5.80 s) itself, as well as +21.8% for mixed and −7.5% for reject. The dossier marks +22.7% as calc.; relabel it as the paper's figure.
- Tokens: −23.6–28.4%, as the paper states.
- New claim: §1 says that with approval wait excluded, mean task time falls 24.6–27.9% against plain execution. This is not in the dossier, and no table in v1 gives the underlying means.

Why time and tokens fall (§6.3): validation stops risky flows early, cutting off long unsafe executions before more model calls pile up. The tasks take fewer steps; the steps are not faster.

Other results:
- Table 6: τ-bench 87.5% → 90.0%; Terminal-Bench 100% → 100%. These are 'benign benchmark subsets' and the subset sizes are not stated.
- Table 5: rollback median 4.17 ms over 15 trials; recovery median 178.95 ms; resume 15/15. These are deterministic trajectories with no LLM calls.
- Fig. 9, excluding approval: provider latency is 62.3–63.6% of runtime, agent plus tool 14.2–14.4%, and Cordon's own control path 22.2–23.4%.

**mechanism and term:**

The mechanism is correct: local mutations run in shadow state and can be rolled back; external effects wait in an outbox until validation or approval releases them.

Term mapping:
- Not a speed-up.
- It is an enabling condition, a commit barrier, that makes overlap or speculation possible for side-effecting actions.
- Wall-clock goes up when approval wait is counted (+22.7%).
- The fall in passes N, model calls c_k and tokens comes from aborting risky tasks on an adversarial suite. Do not classify that as acceleration.
- The control path itself is about 22–23% of measured runtime excluding approval.

**authors and venue:**

- Zheng Chen, Dong Dong, Jialin Li, Jidong Zhai: Tsinghua University.
- Hanqing Liu: Shanghai Jiao Tong University.
- Duling Xu: Renmin University of China.
- Bangzheng Pu: AetherHeart Tech Co., Ltd.
The order matches references.md.

Venue: 'EuroSys '27, April 19–24, 2027, Rabat' appears only as the ACM template's running header. The arXiv abs page has no comments or journal-ref, so under the rule it is not a venue; it is a preprint.

Credibility: (i), (ii) and (iv) pass. (iii) is doubtful:
- The 45 workflows are author-built, and v1 gives no code or data link.
- The τ-bench and Terminal-Bench subset sizes are not stated.
- The model is stated.
Strictly, it fails (iii). Flag for Edwin.

**formula:**

None for speed or cost. The only formal item is the validity predicate valid(T, C_t) that decides commit or abort.

## 72. ToolSpec (arXiv:2604.13519)

**read:** https://arxiv.org/pdf/2604.13519v2 (v2, 28 May 2026; v1 of 15 Apr 2026 not read). Local copy: scratchpad/wf-part2/2604.13519v2.pdf

**verdict:** corrected

**effect:**

The dossier had no numbers.

The abstract claims up to 4.2×. §5.2 and Table 3 give 3.5×–4.2× overall wall-clock speed-up against plain autoregressive decoding. 'Overall' means across API-Bank, ToolAlpaca and BFCLv2:
- Qwen2.5-7B: 3.67×.
- Qwen2.5-14B: 3.48×.
- LLaMA-3.1-8B: 4.19×.
- LLaMA-3.2-3B: 3.66×.

Per dataset, the maximum is 4.45× (LLaMA-3.1-8B on API-Bank: #MAT 5.80, 28.21 → 125.59 tok/s). Against the best previous plug-and-play method (TR) it goes 2.45× → 4.19×, +71% relative.

Conditions (App. B.2):
- Batch size 1; speculative-sampling acceptance; Hugging Face transformers; 2× A100-PCIE 40GB.
- What is measured is the speed of generating tool calls (decode). It is not end-to-end task time.
- Table 2 lists instances: API-Bank 5,221, ToolAlpaca 3,938, BFCLv2 2,251. The paper does not say explicitly that Table 3 uses all of them.
- ToolBench single-tool subset with ToolLLaMA: about 3.7×.
- Accuracy is unchanged (App. B.3, Table 5).
- Drafting overhead is about 5.7–6% of runtime (Fig. 11).

Motivating measurement (Fig. 2; ToolBench, Qwen2.5 series): generating the tool call takes up to 96% of end-to-end latency for Qwen2.5-72B, and about 80% (roughly 4× tool time) for 14B.

**mechanism and term:**

The mechanism is confirmed and more specific than recorded. Two parts:
- Schema-aware drafting: a finite-state machine fills schema tokens and tool/parameter names as drafts.
- Retrieval-augmented speculation: similar past tool calls are reused as drafts.
The target model verifies the drafts, so the output is lossless.

Term: decode. It needs fewer target forward passes per output token (#MAT 4.02–5.80). Prefill, environment wait and the number of passes N are unchanged.

It is relevant to repetitive workflows: on repeated calls it averages 9.3 accepted tokens per step and about 5.5× (Fig. 8).

**authors and venue:**

- Heming Xia, Yongqi Li (corresponding), Cunxiao Du, Wenjie Li: The Hong Kong Polytechnic University.
- Mingbo Song: Peking University.

arXiv cs.CL, no venue on the abs page, and I found no OpenReview record. Code is at github.com/hemingkx/ToolSpec.

Passes (i), (ii) and (iv). (iii) passes: public benchmarks and models are stated, with instance counts in Table 2.

**formula:**

None for speed-up or cost. The only formal item is the FSM definition F = (Q, Σ_schema, δ, q0) (Eq. 1). The speed-up is a measured wall-clock ratio.

## 73. Ghost Tool Calls (arXiv:2606.02483)

**read:** https://arxiv.org/pdf/2606.02483v1 (v1, 1 Jun 2026, the only version). Local copy: scratchpad/wf-part2/2606.02483v1.pdf

**verdict:** confirmed

**effect:**

Speculation volume (§5 Setup, App. B.20): the planner issues a median of 8 speculative candidates per task, and on average 82–89% are abandoned ('ghost' calls), depending on the corpus.

Leakage (RQ1, Table 6): 30 hand-crafted tasks with fixed plans, 3 seeds, Claude Opus 4.7 as adversary.
- Recovery of the user's hidden intent: 0.44 without speculation, 0.97 with naive speculation.
- Late-Scrub, the read-only restriction (SIA) and ACL all stay at 0.97. Only Rewrite (0.53) and Shadow (0.42) reduce it.
- Provider-visible calls per task: 4.03 naive vs 1.03 for no speculation or Shadow.

AgentDojo (Table 3): a 66-task subset, one seed, Haiku-4.5 as planner and adversary. Naive and SIA tie at 0.75.

Task success (Table 4): 30-task stratified subset, 3 seeds (n = 90 per policy), Haiku-4.5 as judge. Naive 0.783, no speculation 0.833, Shadow 0.794; all confidence intervals overlap.

Latency (Table 14, App. B.9): DuckDuckGo, 30 tasks × 3 seeds (n = 90).
- p50: 8.39 s without speculation vs 7.94 s with naive async speculation (−5.4%).
- p99 gets worse: 11.56 → 14.22 s.
- Multi-tool (App. B.17): an author-built 30-task corpus with ≥3 parallel speculative calls; p50 5.00 → 4.38 s (−12.3%).

The Limitations section itself calls the latency numbers ordinal policy costs rather than production speed-ups. The static experiments use simulated per-tool latencies (web 200 ms, etc.). The planner is Claude Opus 4.7.

**mechanism and term:**

The row is correct. Terms:
- Overlap saving: measured, and small. It is capped by the overlap window max(t_speculate_dispatch, t_commit_plan).
- Tool/provider calls: about 3.9× more (calc.).
- Success rate: unchanged within the confidence intervals.
- Adds a privacy constraint on what may be speculated.

One correction to the input: the 4.03 vs 1.03 counts provider-visible tool calls, not model calls c_k.

**authors and venue:**

- Bardia Mohammadi, Laurent Bindschaedler: Max Planck Institute for Software Systems.
- Lars Klein: EPFL.
- Akhil Arora: Aarhus University.

arXiv cs.CR, no venue. Artifacts are released at github.com/mpi-dsg/ghost-tool-calls.

Passes (i), (ii) and (iv). (iii): most corpora are author-generated but released, plus the public AgentDojo 66-task subset, and the models are stated. It passes if a released author corpus counts as public; the AgentDojo result passes either way.

**formula:**

App. B.9 gives the overlap window as max(t_speculate_dispatch, t_commit_plan), with per-stage means t_propose 5,481 ms, t_speculate_dispatch 351 ms and t_commit_plan 2,501 ms (naive async, n = 90). The paper gives no closed-form speed-up.

## 74. WebOperator (arXiv:2512.12692)

**read:** https://arxiv.org/pdf/2512.12692v1 (v1, 14 Dec 2025, the only version). Venue status from the OpenReview API, read 28 Sep 2026. Local copy: scratchpad/wf-part2/2512.12692v1.pdf

**verdict:** confirmed

**effect:**

Success rate (abstract, §4.2, Tables 2 and 3): 54.6% on WebArena (812 tasks) with gpt-4o ('gpt-4o-2025-01-01' in §4.1).
- Search budget 20 steps; depth factor 5; frontier budget 4; branching factor 3; built on BrowserGym.
- With budgets of 5, 10 and 15 it reaches 24.4%, 42.7% and 48.4%.
- The baselines' numbers are copied from their own papers, not re-run.

Backtracking (§4.3, Fig. 4): about 40% of successful tasks needed at least one backtrack (60.5% needed none). Fewer than 3% needed five or more.

Destructive-action check (§4.4, Fig. 5): only about 37% of the actions flagged as destructive before execution were confirmed destructive after execution. The Map site is excluded.

The paper reports no time, token or cost figures.

**mechanism and term:**

The row is correct.

Terms:
- Success rate goes up.
- Passes N and model calls c_k go up: several action candidates per step from different prompts, reward scoring, and replay-based backtracking.
- No speed number.

For Part 2, the relevant item is its pre-execution safe/destructive gate with about 37% precision. It is prior art for gating speculation (D104).

**authors and venue:**

- Mahir Labib Dihan, Tanzima Hashem: BUET. Dihan's work was done as a remote research assistant at QCRI.
- Mohammed Eunus Ali: Monash University.
- Md Rizwan Parvez: QCRI.

The arXiv comment reads 'Under review at ICLR 2026'. OpenReview, read 28 Sep 2026:
- ICLR 2026: venueid Rejected_Submission.
- ICML 2026: Rejected_Submission.
- TMLR: under review.
It is a preprint only. Passes (i)–(iv).

**formula:**

none

## 75. RouteLLM and FrugalGPT (single-turn routing)

**read:** RouteLLM: arXiv:2406.18665v4 (23 Feb 2025), PDF https://arxiv.org/pdf/2406.18665v4 (header 'Published as a conference paper at ICLR 2025'). FrugalGPT: arXiv:2305.05176v1 (9 May 2023; the only arXiv version), PDF https://arxiv.org/pdf/2305.05176v1. Could not read the TMLR camera-ready (OpenReview cSimKw5p6R): openreview.net returned a 403 'Challenge verification required' page, which I did not bypass. FrugalGPT numbers below are from arXiv v1 only.

**verdict:** corrected

**effect:**

RouteLLM section 5.4, Table 6 ('Cost saving ratio of our best performing routers over GPT-4'): at CPT(50%), MT Bench 3.66 (95% GPT-4 quality), MMLU 1.41 (92%), GSM8K 1.49 (87%); at CPT(80%), 2.49 / 1.14 / 1.27. The section 5.4 text defines the ratio as the inverse of the GPT-4 calls of the best router 'relative to the random baseline'. So 3.66x is the ratio of GPT-4 call shares against a RANDOM router at equal PGR (50%). It is not measured against always calling GPT-4. calc. check: MT Bench, Matrix Factorization router trained on Arena+Djudge, 13.40% vs random 49.03% (Table 1) gives 3.66; MMLU, SW ranking 35.40% vs 50.07% (Table 2) gives 1.41; GSM8K, causal LLM 33.64% vs 50.00% (Table 3) gives 1.49. Conditions: strong model gpt-4-1106-preview, weak model Mixtral 8x7B. MT Bench has 160 questions, scored by an LLM judge (8.8 vs GPT-4 9.3). MMLU has 14,042 questions (5-shot). GSM8K has 'over 1,000' problems (8-shot). Cost is proxied by the GPT-4 call share, at $24.7 vs $0.24 per 1M tokens (App. D, a blend of gpt-4-1106's $10/$30 at 95:264 input:output tokens). App. D also assumes 'short prompts in a single turn setting'. Router overhead is at most 0.4% of GPT-4 generation cost (section 5.5, Table 7). Abstract: costs reduced 'by over 2 times without sacrificing response quality'. FrugalGPT v1, abstract: 'up to 98% cost reduction' while matching the best individual LLM. Table 3, cost to reach the same accuracy: HEADLINES (gold-price trend from financial news titles; 10,000 examples; 8 in-context examples) GPT-4 33.1 -> FrugalGPT 0.6 (98.3%); OVERRULING (2,400) GPT-4 9.7 -> 2.6 (73.3%); COQA (7,982) GPT-3 72.5 -> 29.6 (59.2%). Setup: 12 commercial APIs from OpenAI, AI21, CoHere, Textsynth and ForeFrontAI at 2023 prices (Table 1); cascade length 3; DistilBERT scorer; random train/test split. Fig. 3 case study: budget $6.5, accuracy 0.872 vs GPT-4 0.857 at $33.1 (-80%). The paper's text says savings 'range from 50% to 98%', but Table 3's minimum is 59.2%. Both works are single-query, not agent loops.

**mechanism and term:**

RouteLLM: correct. A win-probability model P(win_strong|q) plus a threshold alpha sends each query to exactly one model. Term: price/tier (share of calls at the expensive price). Added cost: a small router computation per call; MF, SW and BERT are not LLM calls, the causal-LLM router is Llama-3-8B. Quality falls slightly (PGR 50% = 95% of GPT-4's MT-Bench score). FrugalGPT: price/tier is the main term, with one correction: a cascade also raises c_k for escalated queries, with up to 3 sequential LLM calls plus a scorer per stage, and therefore raises latency for those queries. RouteLLM section 2 says cascades 'rely on multiple LLM queries, which can increase latency'. Accuracy is equal or higher at the reported points. Proposed D-entry (next free after D156 per STATUS.md; fetch first): 'RouteLLM 3.66x is against a random router at equal PGR, not against all-GPT-4'.

**authors and venue:**

RouteLLM: Isaac Ong*, Amjad Almahairi*, Vincent Wu, Wei-Lin Chiang, Tianhao Wu, Joseph E. Gonzalez, M Waleed Kadous, Ion Stoica; UC Berkeley, Anyscale, Canva (v4 p.1). ICLR 2025 is confirmed by the v4 header and OpenReview 8sSqNntaMr ('ICLR 2025 Poster'). The OpenReview title reads '...from Preference Data'; arXiv reads '...with Preference Data'. FrugalGPT: Lingjiao Chen, Matei Zaharia, James Zou; Stanford University (v1 p.1). TMLR is confirmed by an OpenReview API search: note cSimKw5p6R, venue 'Accepted by TMLR'. There is also a rejected ICLR 2024 submission (XUZ2S0JVJP). The TMLR PDF was not read.

**formula:**

RouteLLM: Eq.2 R^alpha(q) = M_weak if P(win_s|q) < alpha, else M_strong. Eq.4 c(M_R^alpha) = (1/|Q|) sum_q I{R^alpha(q) = M_strong}. Eq.6 PGR = (r(M_R^alpha) - r(M_w)) / (r(M_s) - r(M_w)). Eq.7 APGR = integral_0^1 PGR d(c), approximated by (1/10) sum_i PGR (Eq.8). CPT(x%) = minimum % of strong-model calls needed to reach PGR x%. App. D: blended price (95*10 + 264*30)/(95+264), about 24.7 USD per 1M tokens. FrugalGPT section 3: max_{L,tau} E[r(a, f_Lz(q))] s.t. E[ sum_{i=1..z} ( c~_{Li,2}||f_Li(q)|| + c~_{Li,1}||q|| + c~_{Li,0} ) ] <= b, with z = argmin_i g(q, f_Li(q)) >= tau_i. The three terms per stage are output-length price, prompt-length price and fixed per-query fee. Section 2 states the budget problem as E[c(s,q)] <= b. Section 1 example: 360 x ($0.03 x 1800 + $0.06 x 80), about $21.2K per month.

## 76. FocusAgent

**read:** arXiv:2510.03204v2 (29 Aug 2026), PDF https://arxiv.org/pdf/2510.03204v2. Also arXiv v1 (3 Oct 2025), PDF, for the version comparison.

**verdict:** corrected

**effect:**

v2 Table 2 (section 4.4). Setup (section 4.2-4.3): GPT-4.1 backbone. WorkArena L1: 330 = 33 tasks x 10 seeds, max 15 steps. WebArena: BrowserGym test split of 381 tasks x 1 seed, max 30 steps. Max context 40k. Cost counts input tokens only, 'The cost of the end-to-end processing of input tokens is reported in USD', summed over all LLM calls of the benchmark run at $2/1M (backbone) and $0.4/1M (GPT retriever). Baseline GenericAgent-BT: WA 53.6+-2.7%, $55.6; WebA 36.5+-2.5%, pruning 2%, $59.0. FocusAgent with 4.1-mini retriever: WA 51.5%, pruning 51%, $45.1 (-19%); WebA 32.3%, pruning 59%, $44.0. The paper prints -26% for WebA; the ledger's '-25%, calc.' is -25.4%. FocusAgent with 5-mini retriever: WA 53.2%, pruning 61%, $38.1. Table 2 prints -30%, Table 1 prints -31%, calc. is -31.5%. WebA 39.6%, pruning 53%, $46.2 (-21.7%). GenericAgent-BT (5k): WA 44.5%, pruning 44%, $28.3 (-49%); WebA 29.1%, 38%, $43.5 (-27%). Claude-3.7-Sonnet backbone with 4.1-mini retriever: WA 56.7 -> 52.7%, $55.4 -> $46.9 (-16%); WebA 44.6 -> 39.9%, $58.2 -> $42.6 (-27%). Table 1 splits the 4.1-mini cost into backbone 33.8 + retriever 11.3. Latency (App. D, Table 11): GPT-4.1 backbone, 4.1-mini retriever, run on 'all 33 WorkArena L1 tasks with a fixed random seed', sequentially. It times only the LLM API calls (perf_counter around each call, retries included), no environment time. Total per step 2.5+-1.2 s (p95 4.8) -> 10.1+-4.1 s (p95 17.4); the retriever adds 7.6 s mean. No latency is given for the 5-mini retriever. Inconsistencies inside v2: (a) for FocusAgent(4.1-mini) on WA, Table 1 prints pruning 56% and Table 2 prints 51%, with the same SR 51.5 and cost 45.1; (b) App. Table 8 keeps the v1 values (baseline 53.0%, 5k 41.8%/46%/$28.6, 5-mini 51.8%) and prints '38.1 (-46%)' for 5-mini. Version note on D48: v1 App. Table 5 already had a GPT-5-mini retriever row on WorkArena (51.8%, pruning 61%). v1 had no cost columns and no WebArena 5-mini result. So 'v1 had only the 4.1-mini retriever' holds for WebArena only.

**mechanism and term:**

Mechanism correct. Stage 1: a retriever LLM reads the goal and the current AxTree (no history) and returns the relevant lines. Stage 2: the actor acts on the pruned AxTree. Terms: the actor call's prefill is smaller (observation -51% to -61% per step). c_k is +1: a retriever call per step, which itself reads the FULL AxTree at the cheap price. Total input tokens therefore go up; money goes down only through the price gap (Eq.1). Per-step LLM latency is about 4x higher (2.5 -> 10.1 s, 4.1-mini retriever). Money: input dollars only; output tokens and caching are not counted. Success rate: -2.1 to -4.8 pp with 4.1-mini (GPT-4.1 and Claude backbones); -0.4 pp WA and +3.1 pp WebA with 5-mini. Context growth is unchanged, because only the current observation is pruned. Proposed D-entry (next free after D156): 'FocusAgent v2: the -26% and -30%/-31% are printed by the paper, not calc.; Table 1 vs Table 2 pruning 56% vs 51%; App. Table 8 still has the v1 numbers and a wrong -46%; v1 had a 5-mini row on WorkArena'. This also closes STATUS.md's open item 'FocusAgent Table 1 pruning'.

**authors and venue:**

v2 p.1: Imene Kerboua, Sahar Omidi Shayegan, Megh Thakkar, Xing Han Lu, Leo Boisvert, Massimo Caccia, Jeremy Espinas, Alexandre Aussem, Veronique Eglin, Alexandre Lacoste. Affiliations: Esker, INSA Lyon, ServiceNow Research, Mila, McGill, Polytechnique Montreal, Lyon 1 Universite (LIRIS/CNRS footnote). The citation omits Polytechnique Montreal and Universite Lyon 1. TMLR is confirmed by the arXiv comment 'TMLR 08/2026' and by OpenReview mINaJKSy7A ('Accepted by TMLR'). OpenReview also lists an ICLR 2026 LLA workshop poster and a rejected ICLR 2026 main-track submission.

**formula:**

Section 4.3: Pruning(o_i) = 1 - |o_r|/|o_i|. App. H.1 (Eq.1): FocusAgent cost = C_S*|o_i| + C_L*|o_r|; GenericAgent cost = C_L*|o_i|. FocusAgent is cost-effective iff C_S|o_i| + C_L|o_r| <= C_L|o_i|. With |o_r| = alpha|o_i| this gives alpha <= (C_L - C_S)/C_L. With C_S = 0.4 and C_L = 2 USD/1M, alpha <= 0.8, i.e. pruning of at least 20%. The paper says this estimate does not account for API latencies or the full prompt processing.

## 77. Revisiting Observation Reduction for Web Agents (MFS + GEPA-optimized pruning)

**read:** arXiv:2605.29397v1 (28 May 2026; the only version), PDF https://arxiv.org/pdf/2605.29397v1.

**verdict:** corrected

**effect:**

Abstract and section 4.2. Method: the 'GEPA (ratio=0.2)' pruning program. Policy model: Qwen3.5-122B-A10B, served with vLLM 0.17.0 on 8x A100 with TP8 (App. C). WorkArena L1: 33 tasks (one seed per task type); success averaged over two independent runs. Average wall-clock latency per step drops 'from 65.7s to 30.2s (2.2x faster)' while retaining 84% of the original success rate. WebLinx: '300 instances sampled from the test-iid split'. WebLinx is a step-wise benchmark 'that evaluates single-step action prediction' (section 3.1), so these are 300 single-step instances, not 300 tasks. Result there: 3.1x latency reduction, 89% of success retained. Latency definition (Fig. 4 caption): per-step wall-clock that 'includes reduction and policy model inference; WorkArena additionally includes web access latency'. Baseline: the same policy with the full HTML ('Original (HTML)'). The program keeps a reduction ratio of about 0.2 (HTML characters retained). Absolute success rates appear only in Fig. 4; I did not read them numerically. MiniMax-M2.5 shows only 'consistent trends' (App. E, Fig. 8); the paper gives no 2.2x/3.1x figures for it. Also measured in this paper (Table 2): reimplemented LLM-based reducers using Qwen3.5-397B-A17B take 105.69 s (FocusAgent-style) and 28.32 s (Prune4Web-style) per WorkArena observation, and 'exceed the latency of the no-reduction baseline in some configurations'.

**mechanism and term:**

The recorded mechanism is wrong. The MFS (the minimal set of HTML (element, attribute) pairs whose removal causes task failure) is not found by GEPA. It is built offline by intervention on successful trajectories: agent self-reports, then ddmin with a proxy oracle. It serves as an evaluation proxy ('coverage') and as training data. GEPA (Agrawal et al., 2025) then evolves a Python pruning program to maximize MFS coverage under a reduction ratio of at most 0.2 (or 0.6). At run time the program keeps about 20% of the HTML characters (a superset of the MFS, not only the MFS) in 0.10 s, with no LLM call. Terms: prefill smaller (observation about 20% of characters), so per-call latency is lower. c_k is unchanged: no extra model call, unlike FocusAgent and Prune4Web. Success rate is lower (84% and 89% of original). There is a one-off offline cost outside the per-task formula: MFS construction took 2,729 inferences on WorkArena (about 68K input / 366 output tokens each) and 2,196 on WebLinx. The programs are benchmark-specific. Proposed D-entry (next free after D156): 'WebLinx 300 = single-step instances; WorkArena per-step latency includes web access; headline numbers are Qwen3.5-122B only; GEPA optimizes a coverage-maximizing pruning program, it does not search for the MFS'.

**authors and venue:**

Masafumi Enomoto, Ryoma Obara, Haochen Zhang, Masafumi Oyamada; NEC Corporation (nec.com addresses), v1 p.1. Preprint; the arXiv comment gives only '22 pages, 8 figures, 4 tables'. It passes the preprint rule: company research group, public benchmarks with counts and models stated. D146 stands: 'Agrawal et al.' in the section 3.5 row is the GEPA citation, not this paper's authors.

**formula:**

Section 2.1: f(X) = 1 if removing X from H_s causes failure. MFS X* = argmin_{X subset of H_s, f(X)=1} |X|. Coverage(R) = |{d in D : X^ subset of R(H_s)}| / |D|. RR(R) = (1/|D|) sum_{d in D} |R(H_s)|/|H_s|, measured in characters. App. D: ddmin needs O(log|C|) to O(|C|^2) oracle calls. No speedup or cost formula.

## 78. Prune4Web

**read:** arXiv:2511.21398v1 (26 Nov 2025; the only version), PDF https://arxiv.org/pdf/2511.21398v1. Crossref metadata for DOI 10.1609/aaai.v40i41.40772. The ojs.aaai.org page returned compressed binary content, which I did not parse.

**verdict:** corrected

**effect:**

46.8% -> 88.28% is grounding accuracy in Table 2: 'Performance with Ground-truth (GT) low-level sub-tasks on our custom grounding benchmark'. The test set is 1,101 steps: App. B.4 re-annotates 5,503 Multimodal-Mind2Web steps with an 80/20 split (the caption says '1101 trajectories'). Baseline 46.80%: fine-tuned Qwen2.5VL-3B-Instruct given the GT sub-task plus the original HTML, no pruning. 88.28%: GT sub-task + Programmatic Element Filter + Action Grounder, with fine-tuned Qwen2.5-0.5B-Instruct or Qwen2.5VL-3B-Instruct (both 88.28%). Oracle pruning (GT element guaranteed in the top 20) with the fine-tuned 3B model: 90.28%. GPT-4o with the Prune4Web filter: 80.65%. The planner is bypassed (GT sub-tasks). The '25~50 times reduction' (abstract, section 1) counts candidate ELEMENTS, not tokens. Fig. 1 is only an illustration: >500 DOM elements and 10,000-100,000 tokens -> <20 elements and 400-4,000 tokens. Top-N defaults to 20 (section 3.2). The paper measures no latency or token counts; 'significantly reduces inference latency' (section 3.2) is unquantified. Task level (Table 3): 30 online tasks (Mind2Web-live / WebVoyager sites), completion judged by GPT-4o. GPT-4o-mini goes from 26.3% (LLM top-N selection) to 31.6% (Prune4Web filter); GPT-4o stays at 42.1 -> 42.1. MM2W Cross-Task Step SR of the unified 3B model: 52.4%.

**mechanism and term:**

Refine. The filter LLM does not write a free-form Python script. It fills keywords and base weights into a fixed heuristic scoring template (Alg. 1), working from the low-level sub-task only and never reading the DOM. The program scores a rule-pre-filtered DOM and passes the top 20 elements to the grounder. The per-step pipeline is Planner (screenshot + history) -> Filter -> Grounder; the unified model runs it as a two-turn dialogue. Terms: the grounding call's prefill is smaller (candidate list instead of full DOM). c_k is larger: planner and filter generations come on top of the grounder, though none of them reads the DOM. Success rate is up: grounding 46.8 -> 88.28 with GT sub-tasks, and +5.3 pp online completion for GPT-4o-mini (0 for GPT-4o, 30 tasks). The paper measures no time or cost. The MFS paper's reimplementation (Qwen3.5-397B-A17B) took 28.32 s per WorkArena observation and sometimes exceeded the no-reduction latency, so the direction of the time effect is not established.

**authors and venue:**

Jiayuan Zhang*, Kaiquan Chen*, Zhihao Lu, Enshen Zhou, Qian Yu, Jing Zhang (corresponding). The arXiv v1 PDF p.1 reads 'School of Software & QRI, Beihang University, Beijing, China', with buaa.edu.cn emails. This confirms the affiliation from the paper itself (references.md says 'no affiliations on the arXiv page': the abs page lacks them, the PDF has them). arXiv comment: 'Paper accepted to AAAI 2026'. Crossref: Proceedings of the AAAI Conference on Artificial Intelligence, vol. 40, no. 41, pp. 34710-34718, published 2026-03-14, same six authors.

**formula:**

No speedup or cost formula. Alg. 1 scoring template: S[e] <- S[e] + W[k]*alpha*beta. Match quality: alpha1 > alpha2 > alpha3 > alpha4 (exact > phrase > word > fuzzy). Attribute priority: beta1 > beta2 > beta3 (visible text > trusted attribute > other attribute). Top-N selection with N = 20.

## 79. AgentOccam

**read:** arXiv:2410.13825v2 (24 May 2025), PDF https://arxiv.org/pdf/2410.13825v2 (header 'Published as a conference paper at ICLR 2025').

**verdict:** corrected

**effect:**

+26.6 pp confirmed. Abstract: 'boosts the success rate by 26.6 points (+161%) over similar plain web agents'. Table 2: WebArena, all 812 tasks, gpt-4-turbo-2024-04-09. WebArena-replication 16.5% -> AgentOccam 43.1%. Against SteP-replication 33.3%: +9.8 (+29.4%). Against WebPilot (GPT-4o, reported numbers) 37.2%: +5.9 (+15.8%). Efficiency figures DO exist, from the same runs. Table 4, average observation tokens per step (GPT-2 tokenizer): vanilla 2,210.2 -> AgentOccam 2,930.9 (+32.6%, calc.); intermediate stages 'Above + X Scrolling' 3,376.2 and 'Above + Obs Opt.' 2,891.1. Table 5, average steps per task: 6.2 -> 9.0 (+45%, calc.). The paper reports no dollar or time figures. Crude calc. (observation tokens only, product of means, illustrative): per task 13.7K -> 26.4K; per success 83K -> 61K (about -26%).

**mechanism and term:**

Partly wrong. Mechanism, in four parts: (1) prune the action space (drop rarely used actions; disable scrolling so the whole page is passed); (2) simplify the observation (merge text with interactive elements; tables and lists to Markdown); (3) replay only the 'pivotal' nodes of past pages; (4) keep a planning tree whose branch/prune actions drop the steps of earlier sub-plans from the prompt. Term mapping: success rate up (the main effect). Context growth is reduced by the history rules, a structural change to the history term. But observation tokens per step go UP against the plain agent (whole page instead of scrolling), and N (steps per task) goes UP from 6.2 to 9.0. So 'prefill smaller' holds only against its own no-scrolling intermediate stage, not against the baseline. Cost per success may fall, but the paper does not measure it. FocusAgent and the MFS paper only cite it; neither runs it as an experimental baseline. Proposed D-entry (next free after D156): 'AgentOccam raises tokens per step (+33%) and steps per task (+45%) vs vanilla; its gain is success rate'.

**authors and venue:**

Ke Yang (UIUC; work done as an Amazon intern), Yao Liu, Sapana Chaudhary, Rasool Fakoor, Pratik Chaudhari, George Karypis, Huzefa Rangwala (Amazon), v2 p.1. ICLR 2025 is confirmed by the v2 header and OpenReview oWdzUpOlkX ('ICLR 2025 Poster').

**formula:**

none

## 80. SWE-Pruner

**read:** arXiv:2601.16746v4 (7 May 2026), PDF https://arxiv.org/pdf/2601.16746v4. Also v1 (23 Jan 2026), v2 (4 Feb 2026) and v3 PDFs, for the version comparison.

**verdict:** corrected

**effect:**

The ledger had no numbers. v4 Table 1: SWE-Bench Verified (500 issues), Mini SWE Agent, max 250 rounds, temperature 0. Claude Sonnet 4.5: rounds 51.0 -> 41.7; solved 353 -> 360/500 (70.6 -> 72.0%); tokens per instance 0.911M -> 0.701M (-23.1%); 'API Cost ($)' 0.504 -> 0.369 (-26.8%). The pricing basis and caching are not stated. GLM-4.6: rounds 49.3 -> 36.6; 277 -> 283/500 (55.4 -> 56.6%); 0.791M -> 0.488M (-38.3%); $0.055 -> $0.035 (-36.4%). SWE-QA (OpenHands, 3 repos): tokens -8.9/-19.9/-20.5% with Claude and -54.4/-28.9/-33.7% with GLM; GLM's rounds rise 29-41%. Table 3 (random 50-task SWE-Bench subset; backbone not stated in the text): 62% -> 64%, 0.972M -> 0.670M (-31%). Single-turn Long Code QA (Qwen2.5-Coder-7B): 14.84x compression under the 8x constraint, accuracy 58.71% vs full context 54.05%. Skimmer TTFT: 102 ms at 8,192 tokens (Table 6); the paper states the 40-50 ms overhead is under 10% of an API round trip. Version drift: v1 Table 1 had 351/500 = 70.2% (Claude) and 274/500 = 54.8% (GLM), i.e. -0.4 and -0.6 pp, described as 'maintaining nearly identical success rates'. v2-v4 show 360/500 and 283/500 (+1.4 / +1.2 pp), with identical token and cost figures. Inconsistencies inside v4: for Claude, the Fig. 7 caption (prompt -38.7%, total -39.2%, rounds -18.3%) and the panel labels (-40.0 / -40.5 / -20.2%) disagree with Table 1 (total -23.1%, rounds -18.2%). The abstract's '23-54%' combines SWE-Bench (23-38%) with GLM on SWE-QA (29-54%); Claude on SWE-QA is only 8.9-20.5%.

**mechanism and term:**

Mechanism confirmed and sharpened. A 0.6B neural skimmer (Qwen3-Reranker-0.6B backbone with a CRF head) keeps the lines of file-read tool output (cat/grep) that match a goal hint, which the agent writes each round. It sits as middleware in Mini SWE Agent. Terms: prefill smaller (observation tokens; read operations are 76.1% of tokens, Fig. 2). Context growth has a smaller slope, since the pruned reads persist in history; it is not a structural removal. N (rounds) falls 18-26% on SWE-Bench but rises 29-41% for GLM on SWE-QA. Decode: completion tokens also fall (Fig. 7). There is a small extra model call per read (40-50 ms), plus the goal-hint output tokens. Money: -26.8% / -36.4% per instance. Success rate: +1.2/+1.4 pp in v2+ vs -0.4/-0.6 pp in v1. Proposed D-entry (next free after D156): 'SWE-Pruner v1 -> v2 success rates changed sign at identical token and cost figures; Fig. 7 vs Table 1 disagree; the 23-54% range mixes benchmarks and models'.

**authors and venue:**

Yuhang Wang*, Yuling Shi*, Mo Yang, Rongrui Zhang, Shilin He, Heng Lian, Yuting Chen, Siyu Ye, Kai Cai, Xiaodong Gu (corresponding). Affiliations: LLMSE Lab, Shanghai Jiao Tong University; Sun Yat-sen University; Douyin Group (v4 p.1). Preprint: the arXiv comment gives only the code link, and Semantic Scholar lists the venue as arXiv only. It passes the preprint rule: universities plus a company research group; public benchmarks with task counts and models stated.

**formula:**

Eq.1 s_i = F(q, x_i | C; theta). Eq.2 line score s-bar_j = (1/|T_j|) sum_{t in T_j} s_t; a line is kept if s-bar_j > tau (tau = 0.5). Section 4.3: compression ratio 1/tau = |C_original|/|C_compressed| (tau is reused for this). Training uses a CRF-NLL loss. No speedup or cost formula.

## 81. SimpAgent (Less is More)

**read:** arXiv PDF https://arxiv.org/pdf/2507.03730v1 (v1, 4 Jul 2025; the only version) and the ICCV 2025 CVF open-access PDF (https://openaccess.thecvf.com/content/ICCV2025/papers/Chen_Less_is_More_Empowering_GUI_Agent_with_Context-Aware_Simplification_ICCV_2025_paper.pdf); Crossref metadata for DOI 10.1109/ICCV51701.2025.00558. Tables 1, 3, 5, 6 and 7 carry the same numbers in both versions.

**verdict:** confirmed

**effect:**

Figures confirmed; the mechanism attached to them needs correcting (see next field). Table 5 (ablation), Qwen2-VL-2B, LoRA-fine-tuned: FLOPs 11.90 -> 8.71 T (-27%). Step SR on AITW 69.0 -> 71.3; on GUI-Odyssey 74.9 -> 76.0. The same step SR values are in Table 3 (Qwen2VL row vs SimpAgent row). Conditions: the baseline is the same model, fine-tuned on the same data in the '4AO' format, i.e. the current screenshot plus 4 previous screenshots and 4 previous actions (Table 1: 1551 tokens, FLOPs 11.90 All / 4.12 LLM). History images are scaled to a longest side of 512 px (App. B). AITW uses SeeClick's instruction-wise split (App. A). The metric is offline step success rate, not task success. FLOPs are 'All' (vision encoder + LLM) per decision step. No wall-clock time is measured anywhere. The paper states no test-split sizes; Table 2 gives dataset-level counts (AITW 2,939 tasks, GUI-Odyssey 7,735). Decomposition in Table 5: compression alone gives 8.71 T with 67.3 / 71.8 (-1.7 / -3.1). Adding the consistency loss gives 68.9 / 73.7. Adding masking gives 71.3 / 76.0. The accuracy gain therefore comes from the masking, the FLOPs cut from the compression. Drop layer k=3 (Table 6; k=1 gives 8.49 T, -29%). calc.: 11.90 - 4.12 = 7.78 T of the baseline is vision encoding, which the method does not touch.

**mechanism and term:**

Corrected. (1) The 'masking of irrelevant screenshot regions' is training-time data augmentation only. §4.1: "At inference, the masking operation is omitted". It changes no inference term; it raises success rate (+2.4 AITW / +2.3 GUI-Odyssey in Table 5). The 'SimpAgent-M' rows in Tables 3 and 4 are masking alone, described there as having no inference FLOPs reduction. (2) The FLOPs cut comes from consistency-guided history compression: all history vision tokens are dropped after LLM layer k=3 inside a fine-tuned model, with a KL loss to a full-history branch at training time. History screenshots are still encoded and still enter the prompt and the first 3 layers. So the prompt token count and billing class are unchanged. What shrinks is prefill compute per history token (self-hosted, model-internal). 'Context growth smaller' is inaccurate: the setup uses a fixed window of 4 past screenshots, so there is no growth with N to remove. Correct mapping: prefill compute smaller (history visual tokens beyond layer 3; open weights plus fine-tuning required); success rate up (from the training-time masking). Authors, venue: Chen, G., Zhou, X., Shao, R., Lyu, Y., Zhou, K., Wang, S., Li, W., Li, Y., Qi, Z., & Nie, L. Harbin Institute of Technology (Shenzhen) and Huawei Noah's Ark Lab. ICCV 2025, pp. 5901-5911, confirmed by Crossref and CVF; the arXiv comment also says 'Accepted to ICCV 2025'. As a conference paper it may be cited with numbers. references.md l.125 calls it qualitative use while doc2 §2.3 quotes numbers; this should be reconciled (candidate D-entry).

**authors and venue:**

Confirmed: 10 authors in the order above. HIT Shenzhen (Chen, Zhou, Shao, Lyu, Nie) and Huawei Noah's Ark Lab (Zhou, Wang, Li, Li, Qi). ICCV 2025 (CVF open access; Crossref container '2025 IEEE/CVF ICCV', pp. 5901-5911).

**formula:**

No speedup or cost formula. Eq. (1) is the training loss L(pi_theta) = -sum_t log pi_theta(a_t | o_t, H_t, G). Eq. (2) is the masking operator o_t^m = M(o_t). Eq. (3) is the training objective with a KL consistency term between the truncated branch (H_t^c) and the full branch (H_t). FLOPs are reported only as measured totals (Tables 1, 5, 6, 7).

## 82. ShowUI

**read:** CVPR 2025 CVF open-access PDF https://openaccess.thecvf.com/content/CVPR2025/papers/Lin_ShowUI_One_Vision-Language-Action_Model_for_GUI_Visual_Agent_CVPR_2025_paper.pdf (watermark: identical to the accepted version) plus the CVF BibTeX page. arXiv abs 2411.17465 (v1 only, 26 Nov 2024, comment 'Technical Report') checked for authors.

**verdict:** corrected

**effect:**

Abstract and Fig. 2 (right), built on Qwen2-VL-2B: UI-guided token selection removes 33% of redundant visual tokens during training, with a 1.4x training speed-up. Fig. 2 plots 1344 vs 900 visual tokens. Both are training-time figures. The with/without-selection delta the dossier says was 'not extracted' is in Table 7a (ablation on the ScreenSpot desktop subset; sample count not stated): baseline 1344.0 average visual tokens across layers, ScreenSpot 70.8. Token Selection (UI-Graph) gives 947.4 tokens and a 1.5x training speed-up. Accuracy is 70.4 when selection is used only in training and 64.9 when it is also applied at test time. The text attributes the test-time drop to resolution loss. Table 7c: selection ratio 0.5 is the chosen trade-off (ratio 1.0 gives 762.1 tokens and 64.5). 75.1% is ShowUI-2B's zero-shot ScreenSpot average (Table 2, 256K training samples). The paper does not say whether test-time selection was on for that number. No inference latency is reported anywhere. calc.: 947.4/1344 = -29.5% average visual context. Third-party check (AQuaUI, arXiv 2605.19260v1, Table 1): ShowUI's selection at inference on Qwen2-VL-7B with Transformers gives 27.55% compression, -5.95 pts average accuracy and +0.31 s latency (slower); on ShowUI-2B, 27.78%, -5.04 pts, +0.07 s.

**mechanism and term:**

Corrected. The mechanism is a UI-connected graph over patches (same-colour neighbouring patches form components). Tokens within a component are randomly skipped inside self-attention layers (Mixture-of-Depth style, cross-layer insertion) with positions kept. It is designed and reported as a training-efficiency method; §2.1 says selection is applied at a set ratio in training and is optional at inference. The headline 33% and 1.4x are training cost, which is not a term of the per-task formula. If applied at inference it maps to 'prefill smaller (visual tokens)' with success rate lower (70.8 -> 64.9, Table 7a), and no measured latency gain. AQuaUI's measurement even shows higher latency. Recommend recording ShowUI in Part 2 as training-time only, or as 'prefill smaller at an accuracy cost, latency not shown'.

**authors and venue:**

Lin, K. Q., Li, L., Gao, D., Yang, Z., Wu, S., Bai, Z., Lei, S. W., Wang, L., & Shou, M. Z. (2025). CVPR 2025, pp. 19498-19508 (CVF BibTeX). Show Lab, National University of Singapore (Lin, Gao, Wu, Bai, Lei, Shou) and Microsoft (Li, Yang, Wang). Conference paper; the venue is confirmed on the CVF page.

**formula:**

None for speedup or cost. The method is described by an algorithm (UI connected graph construction) and ablation tables. No equation for token savings.

## 83. GoClick

**read:** arXiv PDF https://arxiv.org/pdf/2604.23941v1 (v1, 27 Apr 2026; the only version; comment 'Technical Report'; Springer 'Noname manuscript' template).

**verdict:** confirmed

**effect:**

Table 3: ShowUI (2B) has TTFT 79.7 ms, TPOT 14.7 ms/token, ScreenSpot 76.1, ScreenSpot-v2 77.4. GoClick-B (0.2B, 230M) has TTFT 37.7 ms, TPOT 4.1 ms/token, ScreenSpot 74.1, ScreenSpot-v2 75.2. Speed conditions (§4.1.2): 'conditions simulating mobile device usage'. Each model processes one input image (height 780, width 360) and a median-length prompt drawn from the grounding test samples, 2000 times, and the TTFT and TPOT are averaged. One NVIDIA L20 GPU, batch size 1, HF Transformers with FlashAttention where supported, BF16, temperature 0. This is a microbenchmark with no task count. Accuracy is click accuracy (point inside the target box, Eq. 3); the ScreenSpot sample counts are not stated in the paper. ShowUI's accuracy here (76.1) is GoClick's own re-evaluation and differs from ShowUI's self-reported 75.1. The comparison is across models (different architectures and training data), not a controlled ablation. The paper's own summary vs 7B models: about 1/30 of the parameters, 1/3 of the TTFT and 1/5 of the TPOT. calc.: vs ShowUI, TTFT -53%, TPOT -72%.

**mechanism and term:**

Confirmed with a qualification. The mechanism is a Florence-2-based encoder-decoder grounding VLM (0.2B / 0.8B), trained on a 3.8M-sample core set filtered from 10.8M raw samples. As a replacement for a large grounding model it maps to price/tier (a smaller model) and to lower prefill (TTFT) and decode-per-token time, with slightly lower success. In the paper's agent use (§4.4, Tables 8-11) it is not a replacement. GoClick-L (0.8B, not B) is added as a second call per pass behind a cloud GPT-4o planner (device-cloud split), so the calls per pass go from 1 to 2. Step SR rises (e.g. AITW overall 27.2 -> 48.9 vs GPT-4o alone; 4,663 samples from 584 trajectories, SeeClick split; offline evaluation), but no latency or cost is reported for the agent setup. The agent evaluation is offline, and past screenshots are not given to the planner.

**authors and venue:**

Li, H., Chen, Y., & Zhang, Z. (2026). Hongxin Li: University of Chinese Academy of Sciences and the NLPR / State Key Lab of Multimodal AI Systems, Institute of Automation, CAS. Yuntao Chen: Hong Kong Institute of Science & Innovation, CAS. Zhaoxiang Zhang: UCAS and CASIA. Chen and Zhang are corresponding authors. No venue: a preprint (technical report). Not in references.md. Rule check: authors and institutions are verifiable and public benchmarks are used with the model stated. The headline ScreenSpot comparison gives no sample count, and the latency figure is a single-prompt microbenchmark, so condition (iii) is only partly met.

**formula:**

Eq. (4) (printed as 'TPOP'), in the paper's own symbols: TPOT = (e2e latency - TTFT) / (Total output tokens - 1), following NVIDIA NIM's definition. Eq. (3): Acc = sum_{i=1..N} 1(pred_i inside GT bbox_i) / N x 100. Eq. (5)-(6): Step SR = sum_i delta(Action_i, GT_i) / N x 100. TTFT is defined in words (time from query submission to first token).

## 84. TRACE

**read:** arXiv PDF https://arxiv.org/pdf/2609.10297v1 (v1, 9 Sep 2026; the only version; 'TECHNICAL REPORT' header), main text §4.3 plus Appendix B.4 (Tables 22, 23), Appendix A.2 (Eq. 8) and Appendix C.

**verdict:** corrected

**effect:**

Model is GUI-Owl-1.5-8B, not a generic GUI-Owl. OmniGUI (Henry et al., 2026), mild budget: 50% of the current frame's visual tokens kept, 10% of each history frame's. One 'CUDA-synchronized GPU'; the GPU model is not stated. The baseline is dense 'stateless' re-prefill: every step re-encodes and re-prefills the current frame plus up to H history frames, with no KV reuse. Table 23 (a separate, strictly serial measurement round), per-step: TTFT 1116.8 -> 452.7 ms; end-to-end 3014.7 -> 2298.9 ms; decode total 1794.3 -> 1711.0 ms. MKC (cache reuse) alone gives TTFT 487.4 ms and end-to-end 2399.8 ms, with the visual KV at 100%; §4.3 says 'at unchanged accuracy'. The tight budget (25% / 5%) gives 397.8 ms TTFT and 2291.5 ms end-to-end. Table 22 (first measurement round) gives TTFT 1102.6 -> 453.9 ms, end-to-end 2958.2 -> 2295.8 ms, input tokens 4892 -> 2011, GFLOPs 73,385 -> 30,170, visual KV 697 -> 292 MB. Step SR 52.45 -> 48.91 (93.3% retained; Tables 1 and 22). The paper notes the two rounds differ; the dossier mixes Table 23 latencies with Table 22 accuracy, so each figure should be labelled by table. OmniGUI has 2,572 steps (App. C, UI-TARS transfer paragraph). The number of timed steps is not stated. calc.: TTFT -59%, end-to-end -24%. MKC alone accounts for 95% of the TTFT saving and 86% of the end-to-end saving. §4.3: TRACE is 2.4x faster than dense re-prefill (TTFT). Fig. 24: at step 5 the dense TTFT is 5.1x TRACE's.

**mechanism and term:**

Corrected. Two parts with different terms. (a) MKC, monotone KV contraction: each screenshot is encoded and prefilled once, and later steps reuse its KV rows instead of re-prefilling history. This moves history tokens from 'prefill of tokens not in cache' to cache reuse. It is lossless (a byte-exact no-op test at the 100% budget) and gives most of the gain. (b) Visual-token admission (layout prior, instruction relevance, novelty ordering and coverage repair) plus contraction of retired frames to a smaller history budget. This makes prefill smaller (fewer visual tokens) and context growth smaller: the visual KV grows as O(k_c + H k_h) instead of re-encoding O(HN). It costs success rate (52.45 -> 48.91). Decode is barely changed, so end-to-end falls far less than TTFT. Our note, not the paper's: the dense baseline has no prefix caching, whereas API users with provider prompt caching already get part of (a). Training-free, self-hosted. Evaluation is offline step SR, and the episodes are short (the paper's C.1 says most benchmarks keep at most 2-3 history frames; its setting uses 5-6).

**authors and venue:**

Wang, Y., Qiao, M., Zhang, X., Zhuge, Y., Zhang, L., & Lu, H. (2026). Dalian University of Technology (Wang, Qiao, Zhuge, Lu); OPPO Research Institute (Zhang X., Zhang L.); The Hong Kong Polytechnic University (Zhang L.). Preprint (technical report), no venue. Matches references.md.

**formula:**

Eq. (8), in the paper's symbols: Len_t^enc = k_c; L_t^KV = T_t + k_h + k_c; |KV_visual| = O(k_c + H k_h). Here T_t is the prefix length at step t and H the number of retained history frames. The paper says this replaces the repeated O(HN) visual encoding of dense history frames. Eq. (1), lifecycle constraints: (i) S_t^cur = sigma(A_t), (ii) S_t^hist ⊆ S_t^cur, (iii) S_t^cur, S_t^hist ⊆ {1..N}. Measured unit costs: one contraction takes 6.4 ms per transition vs 90.8 ms to encode one screenshot (App. A.2).

## 85. GUIPruner

**read:** arXiv PDF https://arxiv.org/pdf/2602.23235v1 (v1, 26 Feb 2026; the only version; ACM template with placeholder venue).

**verdict:** confirmed

**effect:**

Table 2 (§5.4): Qwen2-VL-2B on AITW with 4 history frames, one NVIDIA RTX 4090 (24 GB), history retention 0.1 and current retention 0.75. The dossier's 'aggressive' is the paper's Setting III. Tokens 1320 -> 310; FLOPs 11.5 -> 3.4 T (3.4x, aggregated over vision encoding, prefill and decoding); encoder time 87.9 -> 26.6 ms (3.3x); prefill time 47.5 -> 24.1 ms (1.9x); GPU memory 8956 -> 5902 MB. Table 1, Setting III: AITW step SR 69.5 -> 65.3 (the upper bound is the same model fine-tuned on the target data). AITW uses SeeClick's instruction-wise split (App. A); the test-set size is not stated. GUI-Odyssey is evaluated on a random one-third of its test set. Decode time and end-to-end step latency are not reported. 7B (App. E, Table 6, Qwen2.5-VL-7B, same setting): FLOPs 27.5 -> 8.9 T, encoder 308.7 -> 97.7 ms (3.2x), prefill 156.3 -> 52.8 ms (3.0x). The 7B AITW step SR under Setting III is 71.2 -> 66.8 (Table 1). calc.: tokens -76.5%; encoder + prefill 135.4 -> 50.7 ms (2.7x).

**mechanism and term:**

Confirmed with precision added. Training-free, applied to an SFT'd open model. There are two parts. TAR downsamples history frames by bilinear resizing, under a global history budget distributed with a linear temporal decay so that recent frames get more tokens. SSP prunes current-frame tokens at a shallow LLM layer (L=2), keeping foreground (edge-detected interactive regions), salient background and a uniform grid. Terms: prefill smaller, covering both vision-encoder time (fewer pixels in history frames) and LLM prefill. Success rate is lower. 'Context growth smaller' holds only as a per-frame constant: the history budget is bounded by N_budget = floor(T x N_orig x lambda), and the evaluated window is a fixed T=4, so no N^2 growth is removed in the experiment. The method does not reduce the calls per pass or decode time.

**authors and venue:**

Xu, Z. (Zhou Xu), Zhou, B., Wang, Q., Feng, S., & Xiao, J. (2026). Tsinghua University, Shenzhen (Xu, Zhou, Feng); Xidian University (Wang); The Chinese University of Hong Kong (Xiao, corresponding). No venue: the ACM template carries placeholder text ('Conference acronym XX', 2018), which is not a venue. Preprint. Matches references.md. Rule check: model and public benchmarks are stated, but the AITW test-set size is not, so condition (iii) is only partly met; consistent with its 'qualitative use only' status.

**formula:**

Token-budget formulas, none for speedup or cost. Eq. (1): N_budget = floor(T x N_orig x lambda), with N_orig = HW/P^2. Eq. (2): w_k = gamma + (1-gamma)(T-k)/(T-1); n_k = N_budget · w_k / sum_{j=1..T} w_j. Eq. (3): s_k = sqrt(n_k / N_orig), the resize factor for frame X_{t-k}. SSP: K_total = floor(|T| x mu); Eq. (4)-(6) cover top-k foreground, background top mu·rho and uniform-grid sampling for the residual K_res.

## 86. AQuaUI

**read:** arXiv PDF https://arxiv.org/pdf/2605.19260v1 (v1, 19 May 2026; the only version; marked 'Preprint').

**verdict:** corrected

**effect:**

Abstract: on GUI-Owl-1.5-32B-Instruct, up to 13.22% speed-up and 29.52% fewer visual tokens while retaining 99.06% of full-token performance. Table 2 conditions: vLLM backend, five grounding benchmarks (ScreenSpot-Pro, ScreenSpot-V2, OSWorld-G, UI-Vision, MMBench-GUI), click accuracy, per-request latency in seconds. Average latency change -0.22 s, compression 29.52%. The GPU is not stated, and no benchmark sample counts are stated. calc. from Table 2: mean accuracy 71.284 -> 70.614 = 99.06% (matches). Mean latency 1.664 -> 1.446 s = -13.1%. The abstract's 13.22% cannot be reproduced exactly from the rounded table values. These are single-screenshot grounding requests, not end-to-end tasks. On small models latency rises: Qwen3-VL-2B +0.02 s, MAI-UI-2B +0.01 s. On Qwen2-VL-7B and ShowUI-2B (post-ViT path, Table 1) latency rises by +0.02 s and +0.10 s, with accuracy -3.29 and -4.70 pts. Navigation: on AndroidWorld (online, seed 30, Table 4), task success is UI-Voyager 70.69 -> 68.10% and MAI-UI-8B 57.76 -> 56.03% at about 31.9% compression. No latency is reported there, and the task count is not stated. On AndroidControl (Table 3), Qwen3-VL-2B/8B lose 0.56 / 0.24 pts.

**mechanism and term:**

Confirmed with qualifications. The method is training-free and inference-time. It builds an adaptive quadtree per screenshot and keeps one merged token per leaf, injecting the true positions into (M-)RoPE. A conditional quadtree reuses the previous screenshot's tree within a request (static / shifted / replaced regions). On Qwen3-VL the reduction runs before the ViT, cutting both encoder and LLM tokens. On Qwen2-VL it runs after the ViT, cutting LLM tokens only. Term: prefill smaller (visual tokens per screenshot, about 30%), with success rate slightly lower. The speed gain appears only on larger backbones (8B and up); on 2B models the reduction overhead cancels it (the paper's Limitations say the same). Because the cut applies to every screenshot, it lowers context growth only by a constant factor, not structurally. Requires model-specific patches of the serving stack (vLLM).

**authors and venue:**

Li, Y., Zhu, T., Son, H. M., Zhao, Z., Liu, X., & Chen, M. (2026). All six authors are at UC Davis. Preprint, no venue. Matches references.md. Rule check: models and public benchmarks are named, but no sample or task counts are given, so condition (iii) is only partly met; consistent with its 'qualitative use only' status.

**formula:**

None for speedup or cost. The method's equations cover region similarity for the static / shifted modes (thresholds tau_static = 0.97, tau_shift = 0.94, gamma = 0.03) and, in App. A.5.1, the Qwen2-VL patch index k = (y_rep · w + x_rep) · m^2 with I_rep = {k, ..., k + m^2 - 1} (m = 2).

## 87. GUI-KV

**read:** arXiv:2510.00536v1 PDF https://arxiv.org/pdf/2510.00536v1 (1 Oct 2025; v1 is the only version) + abs page; TMLR list https://jmlr.org/tmlr/papers/ and BibTeX https://jmlr.org/tmlr/papers/bib/qaJECugPzr.bib (read 28 Sep 2026). I could not read the TMLR camera-ready PDF (openreview.net/pdf?id=qaJECugPzr returns a browser-challenge page), so all numbers below come from arXiv v1 and may differ from the published version.

**verdict:** corrected

**effect:**

The record said 'numbers not extracted'. The paper reports these. Main number (§4.3 Table 2 with Table 1): UI-TARS-1.5-7B on AgentNetBench, offline step-level action prediction on pre-collected trajectories, 5 screenshots in context (current + previous), budget gamma = 40% of KV kept per layer. MFLOPs per decoded token: full cache 290.4 -> GUI-KV 177.4 (-38.9%). Step accuracy: 17.5 -> 21.6 (Table 1 AgentNetBench, UI-TARS row, 100% vs 40%). That is +4.1 points absolute; the abstract and §1 call it +4.1%. Other Table 2 cells: 5 screenshots, gamma 20%: 139.5 (-52.0%); 3 screenshots: 213.2 -> 123.6 (20%, -42.0%) and 145.3 (40%, -31.8%); 10 screenshots: 471.5 -> 175.3 (20%, -62.8%) and 249.9 (40%, -47.0%). Prefill overhead is an increase of <0.29% in all settings (§4.3). Online result (Table 1, OSWorld-Verified success rate, UI-TARS-1.5-7B): full cache 26.0, GUI-KV 25.1 at 40%, 20.7 at 20%, 16.1 at 10%. With OpenCUA-7B: 21.4 full, 1.7 at 40%, 17.5 at 80%. Baselines are SnapKV, PyramidKV and VL-Cache; the average gain over the best baseline is +0.2 to +3.6 points. Not measured: wall-clock time, latency and GB of memory for GUI-KV. The only timing and memory figures are the §1 motivation for the uncompressed baseline: UI-TARS-1.5-7B with HF inference, bf16 and FlashAttention-2, 5 screenshots, takes more than 15 s per OSWorld-Verified step on an H200 on average, and uses more than 80 GB of GPU memory with 5 screenshots at max 50 steps. The paper gives no task counts per benchmark and does not say which operations the FLOP count covers. 290.4 MFLOPs per token is far below the roughly 14 GFLOPs per token of a 7B model's weight matmuls (2 x 7e9, calc.), so the figure is probably attention-only. That is our inference; the paper does not say so.

**mechanism and term:**

The mechanism is correct: training-free KV-cache eviction with a uniform budget gamma across layers. Each head keeps the top-scoring tokens: for current-frame visual tokens the score is attention plus alpha times an L2-norm saliency, and tokens from previous frames are kept only if they lie outside a rank-r QR subspace of the last frame's keys. The term mapping is WRONG. It is not 'prefill (KV) smaller': the full prompt is still prefilled at every step, and prefill FLOPs rise by <0.29%. What shrinks is the KV cache kept after prefill. That lowers decode cost per output token (attention over gamma*n cached tokens) and GPU memory. The number of output tokens is unchanged. It is lossy/approximate: accuracy depends on gamma, and online OSWorld success falls at budgets of 20% or less. No money or wall-clock effect is measured. Classify it as decode (per-token compute) smaller plus memory, lossy, FLOPs only. Separately, dossier l.625 (§3.6) lists GUI-KV among the 'approximate sharers'. That is wrong: GUI-KV does no cross-agent or cross-request sharing; it is single-request KV eviction. Proposed D-entry (provisional D157; STATUS lists D156 as the last ID, so re-check for collisions): dossier §3.5 row l.579 'arXiv 2025 / numbers not extracted', and the term 'prefill smaller', vs the paper: TMLR 2026; decode FLOPs -38.9% with step accuracy +4.1 pts at 5 screenshots and gamma 40%; prefill +<0.29%; no wall-clock.

**authors and venue:**

Authors (arXiv abs and PDF) are Kung-Hsiang Huang, Haoyi Qiu, Yutong Dai, Caiming Xiong and Chien-Sheng Wu. All are Salesforce AI Research except Qiu (UCLA; the work was done during an internship at Salesforce). The TMLR venue is confirmed: jmlr.org/tmlr/papers lists the paper as 'June 2026', and the BibTeX gives journal = Transactions on Machine Learning Research, year 2026, URL openreview qaJECugPzr. The OpenReview search API also shows ICLR 2026 Submission20434 reviews for this title; I did not check that outcome, so do not cite ICLR. The dossier §3.5 row (l.579, 'arXiv 2025') is out of date; references.md l.112 and ledger Huang2026b are correct. As a journal paper it passes the credibility rule. Benchmarks and models are stated, but task counts are not.

**formula:**

There is no speedup or cost formula. Selection rule, Eq. (1)/(10): C_psi = {i in C : |{j in C : psi(i) > psi(j)}| < ceil(gamma*n)} (keep the top ceil(gamma*n) tokens per head). Spatial saliency, Eq. (4): S_i = softmax[(r - mu_r)/((sigma_r + eps)*tau)]_i with r_i = ||x_i||_2. Eq. (5): psi_i^h = A_i^h + alpha*S_i for current visual tokens, A_i^h for text tokens. Temporal redundancy, Eqs. (6)-(7): (K^h_{I_t})^T ~ Q_t^h R_t^h and rho_i^h = ||k_i^h (I - P_t^h)||_2 with P_t^h = Q_t^h Q_t^hT. Eq. (8): a percentile threshold rho~^h. Eq. (9): combined score psi^_i^h. Cost statement in §4.3: the QR step costs O(d_h^2 n_t) per head, against O(n^2 d_h) per head for prefill attention.

## 88. Agent-X

**read:** arXiv:2605.10380v1 PDF https://arxiv.org/pdf/2605.10380v1 (11 May 2026; v1 is the only version) + abs page (comment 'Accepted for publication at MobiSys-2026'); Crossref metadata for DOI 10.1145/3745756.3809195 (read 28 Sep 2026).

**verdict:** confirmed

**effect:**

1.61x average end-to-end task-latency speedup (abstract; §1; §5.4 Fig. 18). PromptWeaver alone gives 1.16x and ExSpec alone 1.43x. Stage speedups: prefill 1.97x, decode 1.73x (§1). Setup (§5.1, §3.1): TinyAgent, an LLMCompiler-based macOS agent with a Planner LLM and an Arbiter LLM and up to 16 tools. Backend is TinyAgent-7B (fine-tuned WizardLM-2-7B). Workload is 1,022 examples from the TinyAgent fine-tuning test split. Hardware: Apple Mac mini M4 Pro, 64 GB. Software: MLX v0.25.2, modified MLX-LM v0.25.1 and MLX-engine, with the page cache flushed before each task. Baseline: unmodified TinyAgent on the same stack, averaging 35.4 s per task (§3.1). Accuracy (§5.2, Fig. 14a): Planner accuracy is a DAG match against ground truth. Baseline 0.836; PromptWeaver 0.832 at K=0 and 0.841 at K=1 (the setting adopted). ExSpec's speculative decoding is verified by the target model and the paper claims no accuracy loss. Prefill details: uncacheable Planner tokens fall from 1,711 to 519 (-70%). Planner prefill is 1.57x faster (uncached tokens -49.6%) and Arbiter prefill 4.35x (uncached -88.9%). Loading KV from SSD takes 5.8% (Planner) and 11.7% (Arbiter) of prefill latency. Storage is 6.26 GB for 15 clusters, covering 74.4% of examples. Side effects (§5.5): average input tokens grow from 1,739 to 3,790, and TPOT rises from 122 to 125 ms (+2.2%). SpecDec with a Llama-3.2-1B draft ran slower than the baseline. On TinyAgent-1.1B: prefill 1.62x, decode 1.42x, with no end-to-end figure. The workload is text tool-calling (API), not GUI.

**mechanism and term:**

The mechanism is correct: PromptWeaver reorders and rebuilds the prompt so that most of it is a static prefix whose KV cache is precomputed offline and loaded from SSD; ExSpec is speculative decoding with a trigram lookup table built from the prompt's few-shot examples and the user query, falling back to plain decoding when the table has no entry. The term mapping is PARTLY WRONG: 'money: billing class' does not apply. Everything runs locally, with no API price and no billing; the 'cache' is a local prefix KV cache. In our formula the correct terms are: (1) prefill smaller, because prompt tokens not in the cache fall 70% even though the prompt itself grows 2.2x; (2) decode faster per output token, while the output stays the same. N and c_k are unchanged (one Planner call and one Arbiter call). Costs added: 6.26 GB of SSD and +2.2% TPOT. If the page puts this under money, label it an analogy: in API terms it would move tokens from cache-miss to cache-hit (our inference, not measured). Proposed D-entry (provisional D158): the term label 'money: billing class' vs on-device prefill and decode time only.

**authors and venue:**

Authors are Jinha Chung, Byeongjun Shin, Jiin Kim and Minsoo Rhu, all KAIST (Daejeon) per the PDF author block. MobiSys 2026 is confirmed. The arXiv comment says it was accepted at MobiSys-2026. Crossref gives the container as the Proceedings of the 24th Annual International Conference on Mobile Systems, Applications and Services (MobiSys '26), published 2026-06-20, with the same four authors. It is a conference paper and passes the rule. Cite the DOI version. It is not yet in references.md; ledger key Chung2026 is at references-ledger.md l.119.

**formula:**

There is no closed-form speedup formula. §3.2 describes the 'theoretical max. speedup' of each draft model in prose: it is computed analytically by assuming decode is memory-bandwidth bound with latency proportional to model size, then combining that with draft-token accuracy (Table 2: 0.96-1.59x; 0.57-1.20x 'with tax'). Multi-token tax: 131 ms per token vs 244 ms to verify 2 tokens (1.86x). §4.2: including all tool descriptions costs 120*t tokens; all combinations of tool-use examples number 2^t - 1, with memory proportional to 2^t. §5.3: building the lookup table is O(N) in input length N (83 ms per query).

## 89. The Complexity Trap (observation masking)

**read:** arXiv:2508.21433v3 PDF https://arxiv.org/pdf/2508.21433v3 (27 Oct 2025, latest; v3 adds the OpenHands probe and the hybrid strategy); v1 PDF compared for the abstract; abs page (read 28 Sep 2026).

**verdict:** corrected

**effect:**

Table 1 (§4): SWE-agent on SWE-bench Verified, 500 instances (per the Fig. 2 caption's '$15 across 500 instances'). Model: Qwen3-Coder-480B-A35B-Instruct-FP8, self-hosted on vLLM on 8x H200. Turn limit 250; masking window M = 10; agent temperature 0.8; 95% bootstrap CIs. Raw Agent: solve rate 53.4 +/-4.3%, cost $1.29 +/-0.26 per instance. Observation Masking: 54.8 +/-4.4, labelled '(+2.6%)'. That +2.6% is RELATIVE: +1.4 pp (calc.), and not marked significant. Its cost is $0.61 +/-0.06 (-52.7%, marked significant). LLM-Summary (N=21, M=10): 53.8, $0.64 (-50.4%). Other configurations, Raw -> Masking: Gemini 2.5 Flash 32.8 -> 35.6, $0.41 -> $0.18 (-56.1%); Gemini 2.5 Flash thinking 40.4 -> 36.4 (-9.9% relative, significant), $0.56 -> $0.24; Qwen3-32B 17.0 -> 15.0, $1.12 -> $0.55; Qwen3-32B thinking 23.0 -> 24.6, $0.51 -> $0.46 (-9.8%, not significant). 'Costs can more than double without context management': confirmed (§1, pointing to Table 1). How cost is defined (App. A): for Gemini it is the cost returned by the Vertex AI API; for Qwen it is observed per-turn token counts x the official Alibaba API list price, computed after the fact (the self-hosted runs were not billed). Qwen3-32B list pricing has no cache-hit/miss split, which inflates that model's cost. Hybrid (§5.3, Fig. 5b): Qwen3-Coder 480B, SWE-agent, on the 50-instance SWE-bench Verified-50 subset only, with N = 43 and M = W = 10. Cost is -7% vs Observation Masking and -11% vs LLM-Summary, and solve rate is +2.6 percentage points vs the Raw Agent (per the Fig. 5b caption). With the naive setting N = 21 the hybrid became less cost-efficient. No wall-clock is reported. Version note: the v1 abstract gave 53.8% as the raw agent's solve rate, but in the table 53.8 is LLM-Summary; v3 dropped this. Use Table 1.

**mechanism and term:**

The mechanism is correct: observations older than M = 10 turns are replaced by a placeholder, and all reasoning and actions are kept. The term is PARTLY WRONG. Context growth is smaller: each observation is dropped once it is M turns old, and observations are about 84% of a turn's tokens (§1, App. D.4, SWE-bench Lite-50). But the structure does NOT change: the paper says masking "does not solve the issue of indefinite growth" (§3.1). Total tokens read stay ~N^2 with a smaller coefficient; only LLM-Summary bounds the context. Money is smaller as a consequence. There is also a cache side effect: App. D notes masking's worse cache behavior (hit -> miss), the same conflict as AgentDiet. For LLM-Summary the other terms move the opposite way: extra summarizer calls (c_k up) cost up to 7.2% of instance cost (Table 2); N grows about 15% vs Raw for Qwen3-Coder and Gemini 2.5 Flash (§4.4, 'trajectory elongation'). Success rate is mixed across models. Proposed D-entry (provisional D159): the record's 'solve 53.4->54.8%' is fine, but '+2.6%' is relative, not pts; the hybrid's +2.6 pts is on 50 instances and vs the Raw Agent; Qwen dollar costs are list-price calculations, not bills; masking changes the coefficient, not the N^2 structure.

**authors and venue:**

Authors: Tobias Lindenbauer (JetBrains Research and TU Munich), Igor Slinko, Egor Bogomolov and Yaroslav Zharov (JetBrains Research), and Ludwig Felder (TU Munich, School of Computation, Information and Technology). The venue is confirmed by the arXiv v3 comment and the PDF footer: the 4th DL4C workshop, Deep Learning for Code in the Agentic Era, at NeurIPS 2025. It is a workshop paper; ledger Lindenbauer2025 treats it as non-archival (class D). Judged as a preprint it still passes the rule: authors and institutions are verifiable, and the benchmark is public (SWE-bench Verified, 500 instances) with the models stated.

**formula:**

§3.1, Eqs. (1)-(6). Trajectory: tau_{t-1} = (o_sys, o_user, T_1, ..., T_{t-1}) with T_i = (r_i, a_i, o_i). Masking: o'_i = p_i if i < t - M, else o_i. LLM-Summary: s_t ~ pi'(.|o_si, T_sum) and t_last = t - 1 - M, giving tau'_{t-1} = (o_sys, o_user, s_t, T_{t-M}, ..., T_{t-1}); it is triggered when N + M turns have accumulated. App. D, Eq. (7): mean tokens per turn type x_bar = (1/T_total) * sum_i sum_j sum_k x_ijk for x in {r, a, o}, used to simulate long trajectories. There is no closed-form cost formula: cost is the API bill (Gemini) or tokens x list price (Qwen).

## 90. AgentDiet (trajectory reduction)

**read:** arXiv:2509.23586v2 PDF https://arxiv.org/pdf/2509.23586v2 (15 Mar 2026, latest; the header carries the PACMSE citation); v1 PDF compared (same headline ranges); Crossref for DOI 10.1145/3797084 (read 28 Sep 2026).

**verdict:** confirmed

**effect:**

Abstract, §5.2.1 Finding 1 and Table 4. Setup: Trae Agent; agent LLMs Claude 4 Sonnet and Gemini 2.5 Pro; reflection LLM GPT-5 mini; theta = 500, a = 2, b = 1; step limit 50 on SWE-bench Verified and 100 on Multi-SWE-bench Flash. Benchmarks: 200 SWE-bench Verified instances drawn at random from the 400 not used for analysis or tuning, plus all 300 Multi-SWE-bench Flash instances (7 languages). Results vs the Original agent: input tokens -39.9% to -59.7% (1 - I); agent cost -28.6% to -44.1%; final cost including the reflection step -21.1% to -35.9%. Per-instance US$ (Original -> AgentDiet): SWE-bench Verified + Claude $0.535 -> $0.422; SWE-bench Verified + Gemini $0.385 -> $0.285; Multi-SWE-bench Flash + Claude $1.277 -> $0.933; Multi-SWE-bench Flash + Gemini $0.701 -> $0.449. Pass% in the same order: 64.5 -> 66.5, 50.5 -> 52.0, 40.0 -> 39.0, 21.7 -> 22.7 (-1.0 to +2.0 pp; single run, no CIs). Mean steps are about unchanged except Multi-SWE-bench Flash + Gemini (57.20 -> 43.90). Cost definition: Table 1 list prices x tokens, with the cached-input discount applied to input. Reflection overhead ($+) is 0.055-0.118 of the Original cost; §6.1.2 rounds this to 5%-10%. Latency (§6.1.1): not compared, because commercial API latency is unstable; the reflection step adds latency and could run in parallel. Total LLM spend was about US$2,000 (§6.2). Correction to the recorded conditions: the 100 SWE-bench Verified instances were used for manual analysis (§2.2) and hyperparameter selection (§4.2) and are excluded. The headline ranges come from the 200 + 300 instances only.

**mechanism and term:**

The mechanism is correct. A separate, cheaper LLM (GPT-5 mini) rewrites step s-a (a = 2), seeing only steps s-a-b to s, and only when that step exceeds theta = 500 tokens. It removes useless, redundant and expired content and applies the change only when the saving reaches the threshold. Terms: (1) context growth smaller; each pass's increment shrinks after a 2-step delay, which lowers the coefficient but not the N^2 structure; (2) prefill smaller; (3) the billing-class conflict is confirmed by the paper: §2.1 and §2.3.3 say modifying a step invalidates the cache for all later tokens, and §5.2.1 attributes the smaller dollar saving to output tokens and invalidated KV caches. Missing from the record: c_k goes up, with one extra call per reduced step to a cheaper model (5-12% of cost), and serial time is added per step (unmeasured). N is roughly unchanged. Success rate stays within +/-2 pp. Proposed D-entry (provisional D160): dossier l.760 and doc2 list '100 tuning + 200 + 300' as the evaluation; the headline ranges use only the 200 + 300. The overhead is 5.5-11.8% in Table 4 vs '5%-10%' in §6.1.2.

**authors and venue:**

Authors: Yuan-An Xiao and Yingfei Xiong (Peking University, Key Lab of HCST, MOE) and Pengfei Gao and Chao Peng (ByteDance). Published in Proc. ACM Softw. Eng. 3, FSE, Article FSE056 (July 2026), DOI 10.1145/3797084. Crossref confirms the authors and PACMSE, and the arXiv v2 comment says 'accepted for FSE 2026'. Conference paper; passes.

**formula:**

There is no closed-form speedup or cost formula. §4.2.4: Keep% = sum l_reduced / sum l_orig x 100. I, O, $ and $+ are normalized so that Original = 1. $ covers input tokens (with the KV-cache discount) and output tokens at Table 1 list prices. Alg. 1: reflection is skipped if l_orig <= theta, and the reduction is applied only if the benefit reaches theta. §2.3.3: token usage per reduction step is capped at a + 1 + b steps.

## 91. LLMLingua

**read:** arXiv:2310.05736v2 PDF https://arxiv.org/pdf/2310.05736v2 (6 Dec 2023, latest) + abs page (comment 'Accepted at EMNLP 2023'); Crossref for DOI 10.18653/v1/2023.emnlp-main.825 (read 28 Sep 2026).

**verdict:** confirmed

**effect:**

Abstract: up to 20x compression with little performance loss, across GSM8K, BBH, ShareGPT and Arxiv-March23. The 20x point is Table 2 (§5.2): GSM8K, quarter-shot constraint. Target LLM GPT-3.5-Turbo-0301 (greedy, temperature 0); compressor Alpaca-7B. EM 77.33 with 117 prompt tokens vs full-shot 78.85 with 2,366 tokens (-1.52 EM). At 14x (half-shot) EM is 77.41 (-1.44). BBH loses more: -8.5 EM at 5x and -13.2 EM at 7x. The GSM8K test set is about 1,300 problems (App. A.1); the paper does not say whether all were used. End-to-end latency (Table 6, GSM8K, V100-32G GPU): 8.6 s without compression; with it, 4.9 s (1.7x) at 2x, 2.3 s (3.3x) at 5x and 1.3 s (5.7x) at 10x. The compression itself takes 0.8, 0.3 and 0.2 s. Table 7: estimated GPT-3.5-Turbo cost for GSM8K at list price, $5.2 -> $0.5. Single prompts only (CoT demonstrations and contexts); no agent loop, as recorded.

**mechanism and term:**

The mechanism is correct: coarse-to-fine prompt compression. A budget controller allocates the ratio across instruction, demonstrations and question; demonstrations are dropped at the coarse level; then an iterative token-level pass removes low-perplexity tokens using a small aligned LM. 'Prefill smaller' is right: fewer prompt tokens. Two further effects: an extra small-model pass (the overhead term in Eq. 9), and slightly shorter outputs at high compression (Fig. 2, decode). It is lossy. In an agent loop, compressing each prompt changes the prefix and so conflicts with prefix caching (hit -> miss); the paper does not study this (our inference). In agent papers it appears only as a baseline (LLMLingua-2 in AgentDiet; TokenPilot, E174). The dossier row should name the authors (Jiang et al., 2023).

**authors and venue:**

Authors are Huiqiang Jiang, Qianhui Wu, Chin-Yew Lin, Yuqing Yang and Lili Qiu, all Microsoft Corporation. EMNLP 2023 main conference is confirmed: the arXiv comment says so, and Crossref gives the Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pp. 13358-13376, DOI 10.18653/v1/2023.emnlp-main.825. Conference paper; passes. It is not agentic, so use it only as background for 'prefill smaller'.

**formula:**

§5.4, Eq. (9): c = (L + kL/tau + L/tau) * c_small + (L/tau) * c_LLMs, where c_small ~ 7/175 c_LLMs = 1/25 c_LLMs. At tau = 5 this gives c ~ 0.264 * L * c_LLMs ~ 1/4 * L * c_LLMs, i.e. nearly 4x compute saving. §3: compression rate tau = L~/L in [0,1]; compression ratio = 1/tau.

## 92. Fara-7B

**read:** arXiv:2511.19663v1 PDF https://arxiv.org/pdf/2511.19663v1 (24 Nov 2025; v1 is the only version; the report is dated 2025-11-26 with the header 'AI Frontiers'), including Appendix A 'Token Pricing' after the references; abs page (read 28 Sep 2026).

**verdict:** confirmed

**effect:**

Table 10 (WebVoyager, per task): OpenAI computer-use-preview $0.913, 70.9%, 38.0 +/- 34.2 actions, 295k input / 2.3k output tokens. UI-TARS-1.5-7B $0.082, 66.4%, 41.3 +/- 37.2 actions, 408k / 2.2k. Fara-7B $0.025, 73.5%, 16.5 +/- 21.1 actions, 124k / 1.1k. Table 9: Online-Mind2Web: Fara-7B 34.1, computer-use-preview 42.9, UI-TARS 31.3. DeepShop: 26.2 vs 24.7. WebTailBench: 38.4 vs 25.7. Protocol (§5.1.1): live websites through Browserbase; about 48 impossible WebVoyager tasks removed and 50 re-dated (the final task count is not stated in the paper); up to 5 retries, only on environment errors, for all models; 3 independent runs averaged; 100-step cap. Judges: GPT-4o for WebVoyager and DeepShop, o4-mini for Online-Mind2Web and WebTailBench. Pricing (App. A; Fig. 1 caption): OpenAI list prices; Qwen2.5-VL (Fara-7B and UI-TARS) at $0.20/$0.20 per M input/output tokens from OpenRouter. The paper does not say 'cheapest' (that word comes from the Microsoft blog) and gives no cached-input price; cost = tokens x price per token. The 36.5x ratio is calc. Human evaluation (§5.1.2): Browserbase used Microsoft's released harness and Fara-7B endpoints on Azure Foundry, on the filtered and refreshed WebVoyager tasks, with human verification: 62%. No wall-clock: §5.1.3 treats steps as a good proxy for latency.

**mechanism and term:**

The mechanism is correct: a 7B model (Qwen2.5-VL base) that sees screenshots only and predicts coordinates, trained by SFT on about 145K synthetic FaraGen trajectories. Terms: (1) price/tier: a 7B model at $0.20/M in and out vs OpenAI list prices; (2) N smaller vs computer-use-preview (16.5 vs 38.0 actions) and vs UI-TARS (41.3), but not vs the SoM GPT-5 agent (16.6); (3) context growth, which is MISSING from the record: Fara-7B keeps only the most recent N = 3 screenshots plus all thoughts and actions (§3.2 after Eq. 3), an observation-masking design that helps explain 124k vs 295k input tokens; (4) decode: fewer output tokens (1.1k vs 2.3k). Success rate is mixed, as recorded. Corrections to the dossier: (a) E90's caveat 'the paper's Appendix A pricing was not present in any extraction' is wrong; Appendix A is in the v1 PDF and gives the $0.20/$0.20 OpenRouter price, and GLM at $0.34/$0.34. (b) D54 and D91 contrast 'retries vs mean of 3 runs', but the paper's own 73.5% protocol also retries up to five times on environment errors (§5.1.1). The documented difference is the judge (human vs GPT-4o) and a 3-run mean vs a single pass. Proposed D-entry (provisional D161): E90 caveat and D54/D91 protocol wording vs §5.1.1 and App. A; plus the N = 3 screenshot window as a context-growth term.

**authors and venue:**

There are 12 authors, listed alphabetically: Ahmed Awadallah (senior author), Yash Lara, Raghav Magazine, Hussein Mozannar, Akshay Nambi, Yash Pandya, Aravind Rajeswaran, Corby Rosset, Alexey Taymanov, Vibhav Vineet, Spencer Whitehead and Andrew Zhao. Core contributors are marked: Mozannar, Rosset, Taymanov, Whitehead. The list matches the arXiv abs page. No affiliation line is printed; the header reads 'AI Frontiers' and the links point to aka.ms/msaif, Microsoft Foundry and github.com/microsoft/fara, so the institution is Microsoft (Microsoft Research AI Frontiers). It is a preprint with no venue on the arXiv page. It passes the rule: a company research group, and public benchmarks (WebVoyager, Online-Mind2Web, DeepShop) with the models stated. One caveat: the paper gives no exact WebVoyager task count, and the '595' in D54 comes from the blog / Browserbase.

**formula:**

There is no speedup formula. Cost is described in prose (Fig. 1 caption): the number of input and output tokens times the price per token, with the prices in App. A. §3.2 Eqs. (1)-(3): the policy P(r_t, a_t | q_0, {o_0, r_0, a_0}, ..., {o_{t-1}, r_{t-1}, a_{t-1}}) conditions on the full history, which is then truncated to the most recent N = 3 observations.

## 93. FireAct and Octopus v2

**read:** FireAct: https://arxiv.org/pdf/2310.05915v1 (only version, 9 Oct 2023), full text via pdftotext. Octopus v2: https://arxiv.org/pdf/2404.01744v7 (latest, 11 Sep 2026), full text. I also compared v5 (16 Apr 2024): Table 1 numbers are identical. Both abs pages were checked for version history.

**verdict:** corrected

**effect:**

FIREACT. The 9.0 -> 2.7 s/trial figure is for GPT-3.5, not Llama-2-7B. Table 3 (p.6), 'Cost per trial': fine-tuned GPT-3.5 (FireAct) $2.2e-3 and 2.7 s, against few-shot ReAct-prompted GPT-3.5 at $2.6e-3 and 9.0 s. Text in §5.1 (p.5): 'the inference time is reduced by 70% (9.0s to 2.7s per trial), and the inference cost is reduced even though fine-tuned inference is charged 8× expensive'. Conditions: HotpotQA, 500 random dev questions (§5 default); EM 31.4 -> 39.2; fine-tuned on 500 GPT-4 ReAct trajectories; OpenAI ChatCompletion, July-Sept 2023. The authors' caveat: 'these costs will vary by conditions (e.g., parallelism implementation)'. Money per trial falls about 15% (calc.). The +77% is a separate result. Table 2 (p.5): Llama-2-7B HotpotQA EM 14.8 (few-shot ReAct) -> 26.2 (fine-tuned), '+11.4 / 77%'. No time or cost is reported for Llama. There is an internal inconsistency: the intro (p.2) says 'fine-tuning reduces inference time by 4x', but Table 3 gives 3.3x (calc. 9.0/2.7).
OCTOPUS V2 (v7). Table 1 (p.6) reports per-call accuracy and latency on the 'Android function-call evaluation set': Llama-7B+RAG 68.095% / 13.46 s; GPT-3.5+RAG 98.095% / 1.97 s; GPT-3.5 with all 20 functions in context 97.143% / 1.18 s; GPT-4 98.571% / 1.02 s; Octopus-0 (Gemma-2B, 1K samples per API) 99.524% / 0.38 s. The 35x is 13.46/0.38 = 35.4 (calc.). Abstract: 'Compared to Llama-7B with a RAG-based function calling mechanism, our method improves latency by 35-fold'. Conditions: 20 Android APIs (§4.1, p.7). The queries were 'sampled' with Google Gemini and hand-labelled; this is a private set whose size is not stated (all accuracies are multiples of 1/210, calc.). Llama-7B and Octopus ran on 'a single NVIDIA A100' with flash attention, no quantization and model loading excluded. GPT-3.5 and GPT-4 were called through the API (gpt-3.5-turbo-0125, gpt-4-0125-preview), 'evaluated on March 18 at 2 PM PDT'. On a phone (quantized, prefix precomputed) a call takes 1.1-1.7 s, with no on-device baseline. The -95% context is a claim only: abstract 'reducing the context length by 95%', §1 'saving over 95% context length'. No token counts are reported.

**mechanism and term:**

FireAct: the recorded mapping is wrong for the time number. The 9.0 -> 2.7 s is the same model (GPT-3.5), fine-tuned, with an 8x higher per-token price. So price per token went UP. The saving comes from removing the few-shot examples from every prompt: prefill is smaller, and context growth is smaller. The paper says this matters 'especially for agentic applications where the context is iteratively accumulated'. The Llama-2-7B +77% belongs to the success-rate term: it is what makes a small-model price/tier move viable, but it has no time or cost measurement. Octopus v2: price/tier (a 2B model, versus 7B+RAG or GPT-4) is right, and prefill is smaller because learned 'functional tokens' replace function descriptions and RAG context. Two additions: decode is shorter (a function name is one token), and a retrieval step is removed (the paper says retrieval took 'a significant portion of the time' for GPT-3.5+RAG). This is single-call function calling, not an agent loop, so N and c_k are not measured.

**authors and venue:**

FireAct: Baian Chen (System2 Research), Chang Shu and Nigel Collier (University of Cambridge), Ehsan Shareghi (Monash University), Karthik Narasimhan and Shunyu Yao (PLI, Princeton), per the p.1 author block. arXiv v1 only; Crossref (28 Sep 2026) shows no venue. It passes the preprint rule: university authors, public HotpotQA with 500 dev questions, models stated. references-ledger.md has Chen2023 (class D); it is not in references.md. Octopus v2: Wei Chen and Zhiyuan Li, both listed as Stanford University on v7 p.1, marked 'Preprint. Under review.' Versions run v1 (2 Apr 2024) to v7 (11 Sep 2026); Crossref shows no venue. It FAILS rule (iii): the numbers come from an in-house evaluation set (Gemini-generated, hand-labelled, 20 APIs) whose task count is not stated. Its numbers should go under 'Not used'. A qualitative mention is allowed because the author/institution check passes. It is not in references-ledger.md (arXiv ID not found).

**formula:**

FireAct: none. Octopus v2 has no speedup or cost formula. It gives model objectives: Eq. (2) 'P(f, params|q) = P(f|q; π)P(params|f, q; π)' (p.3) and weighted cross-entropy Eqs. (3)-(4). It also has two pieces of arithmetic in the §1 intro. Energy: 0.1 J per token for 1B-parameter models [23], so a 7B RAG call is about 700 J, '1.4% of a 50kJ iPhone battery', or about 71 calls. Money: RAG function calling 'requires processing about 1000 tokens for each call, resulting in costs of approximately 0.01 USD'.

## 94. StepWise (step-level small -> large cascade)

**read:** https://arxiv.org/pdf/2604.27151v1 (only version, 29 Apr 2026; abs page checked), full text including Appendices A and B.

**verdict:** corrected

**effect:**

All recorded numbers match. Two conditions need correcting.

Table 1 (p.6), OSWorld. Columns are 'Lat./Req.', 'Cost/Task', Acc. and Avg Step.
- Claude Sonnet 4.5 alone: 6.4 s, $0.881, 58.1%, 25.4 steps.
- Kimi K2.5 alone: 8.3 s, $0.132, 60.1%, 22.4 steps.
- EvoCUA-8B + Sonnet 4.5: 4.1 s, $0.224, 55.4%, 26.2 steps. Switched 168 (46.8%); A2 share (steps on the large model) 39.4%.
- EvoCUA-8B + Kimi K2.5: 4.5 s, $0.051, 58.2%, 25.2 steps. Switched 173 (48.2%); A2 40.5%.
- Qwen3-VL-8B + Kimi K2.5: 6.5 s, $0.078, 59.3%.
- Qwen3-VL-8B + Sonnet 4.5: 5.2 s, $0.423, 54.3%.

Table 2 (p.7), web.
- GPT-5.2 alone: 19.6 s, $0.335, 60.1%, 9.9 steps.
- gpt-oss-20b + GPT-5.2: 12.2 s, $0.211, 57.8%, 10.3 steps; A2 66.9%.
- AgentTrek-32B + GPT-5.2: 13.4 s, $0.208, 58.8%.

Conditions (p.6): 'Reported latency is measured from our local deployment using 2× H100 GPUs'. Open-weight model costs are 'reference cost estimates using OpenRouter pricing', and fine-tuned models are priced as their base model.

Correction 1: the web benchmark is WebArena-Verified. App. A.2 (p.11): 'we use the ServiceNow webarena-verified release'.
Correction 2: the 'up to' figures are in §1, contribution 3 (p.3), not the abstract: 'reducing inference cost by up to 74.6% and latency by up to 45.8%'. Neither the PDF abstract nor the abs-page abstract contains numbers.

Task counts are not printed. From the Switched column (calc.): about 359 OSWorld tasks and about 812 WebArena-Verified tasks.

Per-task wall-clock is not reported. WebArena changes (calc.): cost -37.0%, latency per request -37.8%.

**mechanism and term:**

The mechanism is confirmed. A small policy runs by default. A ModernBERT-base (149M) Stuck Monitor reads a window of the last reasoning-action pairs; when its score passes θs, control switches to the large model. A Milestone Monitor triggers a verification call to the stronger model, using the before and after screenshots. Terms:
- price/tier per step: correct. About 40% of steps run on the large model in the OSWorld EvoCUA cascades, and 56-67% on WebArena.
- Latency per request: this is an average over both models' requests, not a speedup of either model.
- c_k goes up on milestone steps (extra verifier calls), plus a tiny per-step encoder call that is not an LLM call.
- N goes up slightly: average steps 25.4 -> 26.2 (Sonnet), 22.4 -> 25.2 (Kimi), 9.9 -> 10.3 (GPT-5.2).
- success rate goes down: -1.9 to -2.7 pp on OSWorld and -1.3 to -2.3 pp on WebArena-Verified, against the always-large baseline.

**authors and venue:**

Confirmed on v1 p.1: Jinbiao Wei, Yilun Zhao, Guo Gan and Arman Cohan (Yale NLP Lab); Kangqi Ni (University of North Carolina at Chapel Hill). The corresponding addresses are yale.edu. arXiv only, with no journal-ref; Crossref (28 Sep 2026) shows no venue. It passes the preprint rule, with one flag: task counts are not printed, only derivable. The references.md l.93 entry is correct.

**formula:**

There is no cost or speedup formula, only the routing rule (p.5): 'E_{t+1} = I(p^stuck_t ≥ θ_s)'; m_t = π_large if E_t = 1, π_small otherwise. Monitors (p.4): 'p^stuck_t = S_φ(w_t), p^mile_t = M_ψ(u, w_t)', where w_t is the last K (rationale, action) pairs.

## 95. SLMs are the Future of Agentic AI (qualitative only)

**read:** https://arxiv.org/pdf/2506.02153v3 (latest, 22 Sep 2026; abs page shows v1 2 Jun 2025, v2 15 Sep 2025, v3 22 Sep 2026), full text including Appendix B.

**verdict:** confirmed

**effect:**

There are no new measurements. The paper contains two kinds of number, neither usable as evidence.
(a) A claim cited from others. §3.2 (p.4): 'Serving a 7bn SLM is 10–30× cheaper (in latency, energy consumption, and FLOPs) than a 70–175bn LLM', citing [70, 68, 36, 53]. This is a secondary figure.
(b) Author estimates, not measurements, from Appendix B case studies (pp.16-17). The share of LLM queries that 'could be reliably handled by appropriately specialized SLMs' is 'about 60%' for MetaGPT, 'about 40%' for Open Operator and 'about 70%' for Cradle. No benchmark or task count is given.

**mechanism and term:**

The mapping is correct: it is a position paper arguing for the price/tier term. Its argument is to route most agent invocations to specialized small models, build heterogeneous agents, and use an LLM-to-SLM conversion algorithm. Nothing is measured.

**authors and venue:**

Peter Belcak, Greg Heinrich, Shizhe Diao, Yonggan Fu, Xin Dong, Saurav Muralidharan and Pavlo Molchanov are at NVIDIA Research. Yingyan Celine Lin is at NVIDIA Research and Georgia Tech. Source: v3 p.1, marked 'Preprint. Under review.' No venue on the arXiv page or in Crossref. It passes the author/institution check, so a qualitative mention is allowed; its percentages must not be used as numbers. It is not in references-ledger.md (arXiv ID not found).

**formula:**

None.

## 96. Self-Guide, VITA-VLA, m2mKD, SMART, SkillReducer, ToolSEE/Dynamic ReAct

**read:** arXiv PDFs read in full or searched:
- Self-Guide: 2604.03098v1 (3 Apr 2026)
- VITA-VLA: 2510.09607v2
- SMART: 2502.11435v2, plus the ACL Anthology page 2025.findings-acl.239
- SkillReducer: 2603.29919v2 (24 Jun 2026)
- Dynamic ReAct: 2509.20386v1
- AgentSysBench: 2608.15127v1, the cited source of the schema-token figure
- m2mKD: 2402.16918v3, abs page only
ToolSEE: arXiv API title, abstract and all-field searches returned nothing, so it could not be located.

**verdict:** not found

**effect:**

None of the three recorded figures is in its primary source.

(1) Self-Guide, '+22% incremental tasks': not in the text. Self-Guide is Wang et al., 'Co-Evolution of Policy and Internal Reward for Language Agents'. Its own number, from the abstract: GRPO co-evolution 'brings further improvements (8%) over baselines trained solely with environment reward'. §1 (p.2): 'with Qwen3-4B, our method achieves around 8% average improvement over GRPO'. Setting: ALFWorld, ScienceWorld and WebShop, text-only. No time or cost is measured. §4.5 reports that self-guidance distilled from Qwen3-32B into Qwen3-1.7B 'does not transfer reliably'.

(2) VITA-VLA, '-76% compute': not in the text. The paper is robot manipulation, with results LIBERO 97.3%, LIBERO-LONG 93.5% and real-world 82.0%. Its efficiency claim concerns training cost.

(3) '2,000-8,000 tool-schema tokens per turn': the string is not in AgentSysBench v1, which is where the archived Gemini document puts it. Its nearest measurement comes from one production session (§7.2). Step 1: system messages are 99.7% of the input. Step 261: 'the model emits only 151 tokens for its next action but must first process 166,721 context tokens'.

Usable numbers found:
- SMART, Table 3, SMART-ER in-domain test set (MATH, FreshQA, Intention-in-Interaction), 5 open models from 7B to 70B, compared with the best baseline: 'Tool Used Macro-Average Decrease (%) 24.00' and 'Performance Macro-Average Increase (%) 37.10'. For example, Mistral-7B on MATH: tool calls per query 3.90 -> 0.60, accuracy 13.25 -> 22.75%.
- SkillReducer, abstract: '48% description compression and 39% body compression while improving functional quality by 2.8%', on 600 skills plus SkillsBench, across five models.
- Dynamic ReAct: 'reduces tool loading by up to 50%', on an internal test suite.

**mechanism and term:**

This row groups unrelated works and should be split.
- SMART: fewer tool calls per task, a 7B model trained to answer from its own knowledge. Terms: environment act/wait and N.
- SkillReducer: coding-agent skill and instruction tokens compressed. Term: prefill smaller.
- Dynamic ReAct: only the relevant MCP tool schemas are loaded. Term: prefill smaller. It fails the credibility rule (see authors).
- Self-Guide: RL training that raises the success rate; it is not an acceleration method and has no efficiency measurement.
- VITA-VLA (robotics) and m2mKD (modular vision transformers, ImageNet): off-topic.
Drop the +22%, -76% and 2,000-8,000 figures.

**authors and venue:**

- Self-Guide: Xinyu Wang, Hanwei Wu, Jingwei Song, Shuyuan Zhang, Jiayi Zhang, Fanqi Kong, Tung Sum Thomas Kwok, Xiao-Wen Chang, Yuyu Luo, Chenglin Wu, Bang Liu. Institutions: McGill, McMaster, HKU, HKUST (Guangzhou), PKU, UCLA, DeepWisdom, Université de Montréal, Mila. Marked 'Preprint. Under review.'
- VITA-VLA: Nanjing University, Tencent Youtu Lab, CASIA. Preprint.
- m2mKD: Lo et al., 2024. Preprint.
- SMART: Qian, Acikgoz, Wang, Chen, Sil, Hakkani-Tür, Tur, Ji. UIUC and IBM Research AI. Findings of ACL 2025, confirmed by the ACL Anthology page and the arXiv comment.
- SkillReducer: Gao, Li, Yuan, Ji, Ma, Wang. HKUST, Tsinghua, Zhejiang University of Technology. Preprint; passes the rule, but it is about coding agents.
- Dynamic ReAct: Gaurav, Akarsh, Ranjan, Bajaj. Only agentr.dev e-mail addresses, no institution or research group, internal evaluation. Fails rules (ii) and (iii), so Not used.
- ToolSEE: not found.
- AgentSysBench: HKUST, Alibaba, ByteDance. Preprint.

**formula:**

None relevant to speedup or cost in any of these papers.

## 97. AutoTool and Signal-Driven Observation

**read:** AutoTool: https://arxiv.org/pdf/2511.14650v1 (only version, 18 Nov 2025), full text, plus the published AAAI-26 PDF https://ojs.aaai.org/index.php/AAAI/article/download/40389/44350 (Table 3 identical). Signal-Driven Observation: https://arxiv.org/pdf/2606.06708v2 (4 Aug 2026), full text. v1 (4 Jun 2026) was diffed word by word: v2 only adds the workshop footer.

**verdict:** corrected

**effect:**

AUTOTOOL. The numbers were previously recorded as 'not extracted'; they are now extracted.
Setup: Llama4-Scout-17B, temperature 0, 4x V100. Metric: AgentBoard progress rate (PR). Runs start cold, and 'inertial' calls are capped at 30% of operations with no two in a row. The hyperparameters were 'tuned to achieve a 10-30% reduction in LLM calls'.
Table 3 (p.6), ReAct -> ReAct+AutoTool:
- AlfWorld: PR 0.394 -> 0.531; input tokens 6560 -> 4110; output tokens 2310 -> 804; LLM calls 24.1 -> 20.4 (1.18x).
- ScienceWorld: PR 0.716 -> 0.708; input tokens 9574 -> 7377; LLM calls 23.3 -> 17.8 (1.31x).
- ToolQuery-Academia: PR 0.901 -> 0.895; LLM calls 7.58 -> 6.32.
Counter-case: Reflexion+AutoTool on ScienceWorld raises input tokens 7282 -> 7842 (0.93x).
Text: 'reduces the LLM call count by 15% to 25% and the total token consumption by 10% to 40%'. Abstract: 'reduces inference costs by up to 30%'.
No wall-clock comparison with the baseline: LLM calls are used 'as a robust, hardware-agnostic proxy for temporal efficiency'. AutoTool's own overhead is 1.21-4.16% of task time (Table 4). Task counts are not stated.

SIGNAL-DRIVEN OBSERVATION. Confirmed: v2 p.7 says 'this paper does not include experiments'. The '20,000 to 80,000 tokens' accessibility-tree size (p.1) is an illustration, not a measurement.

**mechanism and term:**

AutoTool: the recorded mechanism is WRONG. It is not schema reduction or cheap tool selection before the main call. It builds a Tool Inertia Graph from the agent's own earlier trajectories. At each step it first tries an 'inertial call': the tool comes from graph search and the parameters from non-LLM filling ('bypassing a costly LLM call'). If that fails, it falls back to the LLM. Terms: c_k = 0 on inertial passes (at most 30% of them), which also lowers total prefill and output tokens. N changes only indirectly (AlfWorld progress rate rises).
Signal-Driven Observation: the root model plans a sequence of actions and replans only when a signal fires. Signals are zero-LLM-cost: URL change, a new ARIA element, an action failure, or an exogenous event. A separate sub-call reads the full DOM and returns a compact task-relevant observation. Terms, all claimed and unmeasured:
- c_k = 0 between signals, plus one sub-call per signal;
- smaller prefill per root call;
- slower context growth (the root keeps compact observations and one-line actions);
- observation work only on signals.
N (the number of actions) is unchanged, so the recorded 'N' should be c_k.

**authors and venue:**

AutoTool: Jingyi Jia and Qinbin Li, School of Computer Science and Technology, Huazhong University of Science and Technology. Venue confirmed as AAAI-26: Proceedings of the AAAI Conference on Artificial Intelligence 40(37), pp. 31265-31273, DOI 10.1609/aaai.v40i37.40389, published 14 Mar 2026 (Crossref and the AAAI OJS PDF). The arXiv comment also says 'Accepted by AAAI 2026'. It is a conference paper, but it is missing from references-ledger.md. Signal-Driven Observation: Shubham Gaur and Ian Lane, CSE, UC Santa Cruz. The arXiv comment and the v2 footer both say it was accepted to the Failure Modes in Agentic AI (FAGEN) Workshop at ICML 2026. So it is a workshop paper per the arXiv page; references.md l.109 says only 'preprint'. The dossier row links v1; it should link v2.

**formula:**

AutoTool, Eq. (1) (p.5): 'CIPS = (1 − α) · Score_freq + α · Score_ctx', with α = 0.5 and threshold θ_inertial = 0.1. This is a tool-selection score, not a speedup formula. The Table 3 'SpeedUp' row is baseline ÷ AutoTool for each metric (caption: 'SpeedUp row shows the cost reduction ratio'; calc. check 6560/4110 = 1.60). Signal-Driven Observation: none (notation T, O_t, H only).

## 98. ScreenSpot-Pro / ScreenSeekeR (counterexample)

**read:** https://arxiv.org/pdf/2504.07981v1 (only arXiv version, 4 Apr 2025), full text. The published ACM MM version (DOI 10.1145/3746027.3755688) could not be read (ACM DL returned 403); its venue metadata comes from Crossref.

**verdict:** confirmed

**effect:**

Table 4 (p.8), 'Comparison of methods on ScreenSpot-Pro with OS-Atlas-7B': OS-Atlas-7B alone averages 18.9%; ScreenSeekeR reaches '48.1 +29.2'. Abstract: best model 'achieving only 18.9%'; ScreenSeekeR 'achieving state-of-the-art performance with 48.1% without any additional training'. Conditions: 1,581 instructions, 'each in a unique screenshot' (p.2); 23 applications, 5 industries, 3 operating systems. A prediction counts if it falls inside the ground-truth box. The planner is GPT-4o (p.7) and the grounder OS-Atlas-7B. Comparison points: ReGround (no planner, one crop, 1024x1024) scores 40.2%, and ScreenSeekeR without recursive search scores 41.9%. The '0.07%' describes the benchmark, not the method (p.5): targets 'occupy 0.07% of the screenshot area on average', against 2.01% in ScreenSpot. The paper reports no call counts, latency or cost for any method.

**mechanism and term:**

The mechanism is confirmed. GPT-4o proposes candidate regions and nearby elements; the grounder's boxes vote; the crops are scored and searched recursively; the grounder runs once a patch is at most 1280 px (p.6). Terms:
- c_k larger (planner and grounder calls at each recursion level): this is read from Algorithm 1 and is NOT measured.
- Prefill per GROUNDER call is limited by the crop size; the planner still sees the screenshot.
- Success (grounding accuracy) goes up.
Useful for the counterexample slide: ReGround gets most of the gain (18.9 -> 40.2%) with one extra grounder call and no planner.

**authors and venue:**

Kaixin Li, Zhiyong Huang and Tat-Seng Chua (National University of Singapore); Ziyang Meng (East China Normal University); Hongzhan Lin, Ziyang Luo, Yuchen Tian and Jing Ma (Hong Kong Baptist University). The dossier's 'NUS/HKBU' leaves out ECNU. Venue confirmed: Proceedings of the 33rd ACM International Conference on Multimedia (MM 2025), pp. 8778-8786, DOI 10.1145/3746027.3755688, 27 Oct 2025 (Crossref). It is a conference paper. references-ledger.md row Li2025c is already correct; it is not in references.md.

**formula:**

There is no cost or speedup formula, only the patch-scoring function in Eqs. (1)-(2), p.6: s = exp(−((x′−0.5)² + (y′−0.5)²)/(2σ²)) if the point is inside the patch, otherwise 0. Here x′ = (x − x1)/(x2 − x1) and y′ = (y − y1)/(y2 − y1), with σ = 0.3.

## 99. Survey second-hand: Aguvis (as quoted by Bai et al. 2026, arXiv:2609.02309v1)

**read:** Survey: https://arxiv.org/pdf/2609.02309v1 (v1, 2 Sep 2026; §3 p.4 and appendix Table 2). Primary: https://arxiv.org/pdf/2412.04454v2 (v2, 5 May 2025, ICML 2025 camera-ready footer). Wording below is paraphrased; numbers and conditions are exact.

**verdict:** corrected

**effect:**

Primary §4.4 (p.7): the pure-vision agent uses a constant 1,196 tokens per 720p screenshot, while HTML-based agents need about 4,000 tokens per interaction. Against GPT-4o on Mind2Web-Live, this gives 70% fewer input tokens per step and 93% lower cost (Figure 3, Table 4). §2 (p.2) gives the 4k-6k tokens per interaction range for text agents (HTML per Fig. 3; AXTree per Xie et al. 2024). Conditions: Mind2Web-Live has 104 tasks (App. D.3) and was run in BrowserGym with an adapted evaluation. Baseline: GPT-4o planner on HTML with 'Choice' grounding (Table 4: SR 22.1%, $0.142 per successful step). Aguvis: AGUVIS-72B as both planner and grounder on screenshots (SR 27.1%, $0.012 per successful step). calc.: 1 - 1196/4000 = 70.1%; 1 - 0.012/0.142 = 91.5%, so Table 4 alone does not give 93% (the figure was not read off). How the self-hosted 72B model's USD cost was priced was not found in the passages read. The survey (§3 and Table 2) pairs the 4k-6k range with the 70%, but the paper computes 70% against GPT-4o's ~4,000 HTML tokens.

**mechanism and term:**

Wrong family label. Aguvis does not reduce visual tokens: it swaps the observation modality (HTML/AXTree text becomes one screenshot of fixed size) and also swaps the model (GPT-4o becomes self-hosted AGUVIS-72B). Terms: observation tokens per pass (o_k) smaller, so prefill is smaller; price/tier also changes (cheaper self-hosted open model), so the 93% cost figure mixes both effects. Success rate rises (22.1 to 27.1 on Mind2Web-Live). Vision-encoder time is not reported. Credibility: passes (conference paper, HKU + Salesforce Research, public benchmark with task count and model).

**authors and venue:**

Yiheng Xu, Zekun Wang, Junli Wang, Dunjie Lu, Tianbao Xie, Amrita Saha, Doyen Sahoo, Tao Yu, Caiming Xiong. Affiliations: University of Hong Kong and Salesforce Research. Venue: ICML 2025 (arXiv comment 'ICML 2025'; PDF footer: Proceedings of the 42nd ICML, Vancouver, PMLR 267). The survey's 'arXiv'24' venue is outdated.

**formula:**

Table 4 caption: Cost = the model's total inference cost in USD / number of successful steps. No speedup formula.

## 100. Survey second-hand: ST-Lite (as quoted by Bai et al. 2026, arXiv:2609.02309v1)

**read:** Primary: https://arxiv.org/pdf/2603.00188v3 (v3, 26 Aug 2026, camera-ready for Findings of EMNLP 2026), compared with https://arxiv.org/pdf/2603.00188v1 (v1, 27 Feb 2026). Survey: 2609.02309v1 §4 and Table 3. Paraphrased; numbers exact.

**verdict:** corrected

**effect:**

The survey's 2.45x decode and 1.40x end-to-end are v1 numbers, although v2 (25 Aug) and v3 (26 Aug) predate the survey (2 Sep). v1 §5.4 Table 2 and App. E Table 3: 10 screenshots, prefill 4685.3 to 4732.6 ms, decode 4501.1 to 1837.2 ms, on selected long-horizon AgentNetBench samples with more than 15 frames. v1 does not state the model or GPU in the passages read. v3 supersedes this. v3 abstract: up to 2.35x decoding speedup at fivefold compression. v3 §4.5 and Table 2 (KV budget beta = 20%): 10 screenshots give 2.35x decode and 1.80x end-to-end with prefill 0.99x; 5 screenshots give 1.95x/1.55x; 3 give 1.55x/1.30x; prefill 0.97-0.99x; single 48 GB GPU. v3 App. U Table 30: complete AgentNetBench evaluation set, image_slots = 10, UI-TARS-1.5-7B, bf16 + FlashAttention 2, mean of 3 runs after 2 warm-ups (std <= 4%). Per call: Full Cache 2417 + 8494 = 10911 ms; ST-Lite 2440 + 3618 = 6058 ms. Table 31 covers 92 steps. OpenCUA-32B (Table 32): 1.94x decode, 1.48x end-to-end, prefill 0.98x. 'End-to-end' means one model call's prefill + decode latency, not task wall-clock. Accuracy at beta = 20% (Table 1, UI-TARS-1.5-7B), ST-Lite vs Full Cache: ScreenSpot-Pro 42.2 vs 42.3; AITW 20.1 vs 18.2; AgentNet 17.0 vs 17.5.

**mechanism and term:**

Term mapping is wrong. ST-Lite compresses the KV cache after prefill: TSG drops redundant history-frame KV, CSS keeps tokens at UI-element boundaries, and every layer gets the same budget. The term it changes is DECODE (each output token attends over a 5x smaller cache, so memory-bound decoding is faster), not prefill. Prefill is 0.97-0.99x, slightly slower, and the prompt tokens read are unchanged. It needs KV access, so it applies only to self-hosted models. Dossier fix: 'decode faster (self-hosted), prefill unchanged'. Credibility: passes (Tsinghua Shenzhen, Zhejiang University, CUHK; the arXiv comment gives EMNLP 2026 Findings; public benchmarks; model named).

**authors and venue:**

v3: Bowen Zhou, Zhou Xu, Wanli Li, Jingyu Xiao, Pingan Gan, Haoqian Wang (v1 did not list Pingan Gan). Affiliations: Tsinghua University (Shenzhen), Zhejiang University, The Chinese University of Hong Kong. Venue: arXiv comment 'Accepted to Findings of EMNLP 2026. Camera-ready version.' The v1 title was 'Efficient Long-Horizon GUI Agents via Training-Free KV Cache Compression'; the survey cites this title (Zhou et al. 2026a). The current title is 'ST-Lite: Training-Free KV Cache Compression with Spatio-Trajectory Guidance for Long-Horizon GUI Agents'.

**formula:**

No speedup formula; speedup is Full-Cache latency / method latency (Table 30). §R complexity: CSS O(N_v * D); TSG O(N_hist * N_cur * D); prefill self-attention O(L^2 * D) with L = N_hist + N_cur + N_text; compressed cache O(B * D * L_layers).

## 101. Survey second-hand: LineRetriever (as quoted by Bai et al. 2026, arXiv:2609.02309v1)

**read:** Primary: https://arxiv.org/pdf/2507.00210v1 (v1, 30 Jun 2025; only version). Survey Table 2 row. Paraphrased; numbers exact.

**verdict:** confirmed

**effect:**

Table 1 and §5: LineRetrieverAgent, with a GPT-4.1-mini retriever and a GPT-4.1 agent, cuts the AxTree observation by 61% on WorkArena L1, 72% on WebLINX and 73% on WebArena (the survey's 61/72/73% matches). Reduction counts the observation only, not the whole prompt (§4.4). Task counts (§4.4): WorkArena L1 has 330 runs (10 seeds per task); WebLINX test-iid has 2,650; WebArena has 381 (BrowserGym test split). Limits: 15 steps on WorkArena and 30 on WebArena; context capped at 40k tokens (10K for the truncation baseline). Success rate against GenericAgent-4.1 with bottom truncation: WorkArena L1 44.8+-2.7 vs 52.7+-2.7; WebArena 24.9+-2.2 vs 32.3+-2.4; WebLINX 14.1+-0.6 vs 13.9+-0.6. The structure-preserving variant reduces only 30/18/24% with SR 49.1/13.7/30.2. No latency, wall-clock or dollar cost was measured.

**mechanism and term:**

This is text (AxTree) filtering, not a visual-token reduction. Each step, a lightweight LLM reads the full observation with numbered lines and returns line ranges; the agent model then reads only those lines. Terms: main-model prefill smaller (observation tokens o_k). But c_k rises by one: an extra retriever call per pass that still reads the full observation, at the price of a cheaper model. Success rate falls 7-8 pp on WorkArena L1 and WebArena. Credibility: passes as a preprint (INSA Lyon, Esker, ServiceNow Research, Mila, McGill, Universite Claude Bernard Lyon 1 / LIRIS; public benchmarks with task counts; GPT-4.1 named). No venue.

**authors and venue:**

Imene Kerboua, Sahar Omidi Shayegan, Megh Thakkar, Xing Han Lu, Massimo Caccia, Veronique Eglin, Alexandre Aussem, Jeremy Espinas, Alexandre Lacoste. Affiliations: INSA Lyon, Esker, ServiceNow Research, Mila, McGill, UCBL Lyon 1, LIRIS. arXiv preprint only (no venue on the arXiv page).

**formula:**

§4.4: Reduction(o_i) = 1 - |o_r| / |o_i|, where o_r is the retrieved observation and o_i the original, measured in tokens.

## 102. Survey second-hand: AdaGUI-R1 (as quoted by Bai et al. 2026, arXiv:2609.02309v1)

**read:** OpenReview note Ric2If6Xur (metadata and abstract via api2.openreview.net search, 28 Sep 2026). The PDF (openreview.net/pdf?id=Ric2If6Xur and the /pdf/de272b91... path) returned HTTP 403 (login/challenge), and the forum API requires challenge verification. I did not try to get past it. The arXiv API (title and all-field searches) finds no arXiv version. Survey: 2609.02309v1 §6 p.6 and Table 5.

**verdict:** could not read

**effect:**

Only the abstract could be read (paraphrased): 40% fewer unnecessary reasoning tokens and 5% higher action accuracy. The abstract gives no benchmark, task count, model or baseline. The survey's further figure (23.5% more FLOPs under the harder-example schedule) could not be checked against the paper.

**mechanism and term:**

Difficulty-aware reasoning depth: SFT on self-generated, difficulty-aware reasoning traces, then GAPO RL with an adaptive thought reward and a difficulty-aware exploration reward. The term is DECODE (fewer output/thinking tokens), not prefill or observation. Its grouping in the dossier row under 'observation / visual-token reductions' is wrong. Credibility: fails the source-credibility rule. OpenReview venueid ICLR.cc/2026/Conference/Rejected_Submission (the survey says 'submitted to ICLR 2026'); no arXiv page; the note shows no institutions; the benchmark, task count and model behind its numbers could not be read. It belongs under 'Not used'.

**authors and venue:**

Jiafu Chen, Rui Lv, Hongyi Jing, Ziqiang Dang, Shuo Fang, Chenguang Ma, Lei Zhao, Jiajie Teng (OpenReview author list; institutions not shown). Venue: rejected ICLR 2026 submission. Not a publication.

**formula:**

could not read (PDF inaccessible)

## 103. SGLang / RadixAttention

**read:** https://arxiv.org/pdf/2312.07104v2 (v2, 6 Jun 2024; its footer says 'Preprint. Under review.') and the NeurIPS 2024 camera-ready https://proceedings.neurips.cc/paper_files/paper/2024/file/724be4472168f31ba1c9ac630f15dec8-Paper-Conference.pdf (same 6.4x / 3.7x and setup). Paraphrased; numbers exact.

**verdict:** confirmed

**effect:**

Abstract: up to 6.4x higher throughput than state-of-the-art inference systems. §6.2: on open-weight models, throughput up to 6.4x and latency down up to 3.7x (Figs. 5-6: Llama-7B on one A10G 24GB, App. C). Baselines (§6.1): vLLM v0.2.5 (an earlier version, before RadixAttention was partially integrated into vLLM), Guidance v0.1.8 (llama.cpp backend), LMQL v0.7.3 (HF Transformers). Twelve workloads: 5-shot MMLU, 20-shot HellaSwag, ReAct agents and generative agents (traces taken from the original papers and replayed), Tree-of-Thought on GSM-8K, Skeleton-of-Thought, LLM judge (branch-solve-merge), JSON decoding, multi-turn chat (short and long), DSPy RAG. Throughput = programs per second at maximum batch; latency = one program at a time without batching, averaged. Optimizations that would change outputs were off unless stated, so all systems compute the same results: quality is equal by design and was not measured. Cache hit rate 50-99%; cache-aware scheduling reaches ~96% of the optimal hit rate. Mixtral-8x7B (8 A10G) and Llama-70B (4 A100) show similar trends; multimodal up to 6x (Table 2). The text does not say which workload gives the 6.4x / 3.7x maxima (the bar charts are normalized).

**mechanism and term:**

The dossier's mapping (prefill smaller; queueing) is right but incomplete: the 6.4x combines several mechanisms. (a) RadixAttention exact prefix reuse: cached tokens are not recomputed (prefill), and shared KV saves memory, allowing larger batches (queueing/throughput). (b) Cache-aware, longest-shared-prefix-first scheduling raises the hit rate. (c) Frontend fork parallelism overlaps calls within a program (ToT, SoT). (d) Compressed FSM decodes several tokens per step for constrained output (decode; 1.6x throughput in the JSON ablation, §6.3). (e) API speculative execution cuts model calls c_k (input-token cost about 3x lower on a 3-field GPT-3.5 extraction, §6.2). Vs vLLM v0.2.5, the baseline had no prefix caching. Credibility: passes.

**authors and venue:**

Lianmin Zheng, Liangsheng Yin, Zhiqiang Xie, Chuyue Sun, Jeff Huang, Cody Hao Yu, Shiyi Cao, Christos Kozyrakis, Ion Stoica, Joseph E. Gonzalez, Clark Barrett, Ying Sheng. Affiliations: Stanford, UC Berkeley, SJTU, Texas A&M, Independent Researcher. NeurIPS 2024 Main Conference Track confirmed on the proceedings page (Advances in NeurIPS 37, DOI 10.52202/079017-2000).

**formula:**

§3: cache hit rate = number of cached prompt tokens / number of prompt tokens. Theorem 3.1: for a batch, visiting the radix tree in DFS order achieves the optimal cache hit rate when cache size >= the maximum request length. No speedup formula.

## 104. Parrot

**read:** https://www.usenix.org/system/files/osdi24-lin-chaofan.pdf (OSDI '24 proceedings version). Paraphrased; numbers exact.

**verdict:** confirmed

**effect:**

§8.4 and Fig. 18a: multi-agent programming built with MetaGPT. An Architect designs the files and APIs; several Coders each write one file; Reviewers comment; Coders revise; review-revise runs three times. One A100-80GB running LLaMA 13B; 4-16 files; metric = end-to-end latency to deliver the final code. Parrot is up to 11.7x faster than the latency-centric baseline and up to 2.45x faster than the throughput-centric baseline (both maxima at 16 files in Fig. 18a). Prompt-structure sharing contributes 2.35x; Parrot's shared-prefix kernel adds 1.2x at 16 files over vLLM PagedAttention. Baselines (§8.1): apps written with LangChain and served through FastChat onto vLLM or HuggingFace engines. Latency-centric = capped engine capacity; throughput-centric = deliberately large batches. §8.1 also injects a random 200-300 ms delay per request to emulate Internet overhead, and length-matches the LLaMA outputs to recorded GPT-4 responses, so output quality is not measured. §1 headline: up to 11.7x speedup or 12x higher throughput (the 12x is GPTs-app serving on 4x A6000 with LLaMA 7B, §8.3).

**mechanism and term:**

Mostly right, but incomplete. Semantic Variables expose the request DAG to the service, which enables: (a) server-side execution of dependent requests, removing the client round-trip between calls (the injected 200-300 ms per request) and the re-queueing of each call; (b) deducing each request's performance objective from end-to-end goals, for batching and scheduling (queueing); (c) prefix sharing, including dynamically generated shared context (prefill and KV memory); (d) a shared-prefix attention kernel (decode, 1.2x); (e) co-locating an app's requests (cluster queueing and cache locality). Terms: queueing, prefill (shared prefixes), plus decode (kernel) and the inter-call wait. Credibility: passes (OSDI 2024 proceedings; SJTU + Microsoft Research); it still needs a references.md entry.

**authors and venue:**

Chaofan Lin (SJTU), Zhenhua Han, Chengruidong Zhang, Yuqing Yang, Fan Yang (Microsoft Research), Chen Chen (SJTU), Lili Qiu (Microsoft Research). 18th USENIX OSDI, July 10-12, 2024, Santa Clara. Code: github.com/microsoft/ParrotServe.

**formula:**

none for speedup or cost found

## 105. Preble

**read:** https://arxiv.org/pdf/2407.00023v2 (v2, 3 Oct 2024) and the ICLR 2025 camera-ready https://proceedings.iclr.cc/paper_files/paper/2025/file/5bc342f48de8264779952fac378f96dc-Paper-Conference.pdf. Paraphrased; numbers exact.

**verdict:** confirmed

**effect:**

Abstract: 1.5x to 14.5x better average latency and 2x to 10x better p99 latency than state-of-the-art serving systems. §1 and §4.3: the main comparison is data-parallel SGLang (a round-robin load balancer over per-GPU SGLang instances), with a similar result against vLLM (App. C). Five workloads: tool use (ToolBench), embodied agent in a virtual environment, program generation, video QA, long-document QA (LooGLE). Poisson arrivals at swept RPS, plus a mixed workload on the Azure trace. Models: Mistral 7B and Llama-3 70B. Hardware: two servers with 2 A6000 each, and one 8x H100 server. Metric: end-to-end request latency, including scheduling, queueing, prefill and decode; p99. The smallest gain is on programming (1.56-1.8x average, 3-4x p99), because decoding dominates there. These are per-request latencies, not workflow completion times. Serving is exact, so quality does not apply.

**mechanism and term:**

Correct. The E2 scheduler reuses a cached prefix on the GPU that holds it when the matched prefix is longer than the remaining tokens; otherwise it explores the GPU with the lowest prompt-aware load cost. It also balances prefill and decode per GPU, uses priority quotas for fairness, and has a global/local scheduler hierarchy. Terms: prefill (more cache hits across a GPU cluster: only missed tokens are prefilled) and queueing (load balance). Credibility: passes (ICLR 2025 confirmed on proceedings.iclr.cc; UCSD). The arXiv v2 PDF's running header wrongly says 'ICLR 2024'; that is a template line, and the camera-ready says ICLR 2025.

**authors and venue:**

Vikranth Srivatsa, Zijian He, Reyna Abhyankar, Dongming Li, Yiying Zhang; University of California, San Diego (code at github.com/WukLab/preble). ICLR 2025 (proceedings page lists International Conference on Learning Representations 2025).

**formula:**

§3.2 load cost for assigning request R_k to GPU_i: L_i = sum over r in W of (PT_r + DT_r) (prefill time of r's tokens not matching a prefix on GPU_i, plus decode time, over the window H); M_i = sum over j in E of PT_j x N_j (eviction cost: prefill time of the evicted node times its share of requests); P_i = prefill time of R_k's missed tokens. R_k goes to the GPU with minimum L_i + M_i + P_i.

## 106. InferCept

**read:** ICML 2024 PMLR page https://proceedings.mlr.press/v235/abhyankar24a.html and its PDF (raw.githubusercontent.com/mlresearch/v235/main/assets/abhyankar24a/abhyankar24a.pdf). Paraphrased; numbers exact.

**verdict:** corrected

**effect:**

Abstract: 1.6x-2x higher serving throughput and 2x more completed requests per second than state-of-the-art systems; recomputing already-computed context takes 37-40% of total model forwarding time. §1: 1.6x-2x higher serving load than vLLM at similar per-token latency. §3.2: this 37-40% (and 27% GPU resource wastage in GB x min) is measured for vLLM's Discard on the mixed workload of all six augmentations. §5.1, request rate sustained at the same normalized latency vs vLLM: GPT-J-6B on 1 A100 up to 1.6x (normalized latency 1.9-5.7x lower at the same rate); Vicuna-13B on 1 A100 up to 1.25x; Vicuna-13B on 2 A100 (TP) up to 1.8x (1.6-10x); Llama3-70B on 4 A100 (TP) 2x (1.3-12x). Normalized latency = median over requests of end-to-end latency / output length, with the intercepted (tool) time removed. The mixed workload samples uniformly from six augmentations: math, QA, virtual environment (ALFWorld), chatbot, image generation, TTS. Correction: the abstract's 1.6-2x leaves out the 13B single-GPU result of 1.25x. The 37-40% is the baseline's recompute share, not a measured InferCept saving.

**mechanism and term:**

Mapping is right. During an interception (tool call, environment step or human turn), InferCept decides per request whether to keep the KV on the GPU, swap it to CPU (budgeted and pipelined), or discard and recompute it (in chunks), choosing whichever wastes least GPU memory. The freed memory then serves more requests. Terms: prefill (no recompute of already-computed context after the tool returns, i.e. cache hits survive the environment wait) and queueing (more concurrent load). Tool/wait time itself is not reduced and is excluded from the metric. Self-hosted only. Credibility: passes.

**authors and venue:**

Reyna Abhyankar, Zijian He, Vikranth Srivatsa, Hao Zhang, Yiying Zhang; UC San Diego. ICML 2024, PMLR 235:81-95 (Vienna). Code: github.com/WukLab/InferCept.

**formula:**

GPU-memory waste per request i at interception j (§3.2 and §4.2-4.3): Eq.1 WasteDiscard = T_fwd(C_i^j) x C_i^j x M + T_fwd(C_i^j) x C_other x M; Eq.2 WastePreserve = T_INT^j x C_i^j x M; Eq.3 WasteSwap = 2 x T_swap(C_i^j) x C_batch x M; Eq.4 WasteChunkD = T_fwd(C_i^j) x C_i^j x M / 2 + n x T_fwd(C_i^j / n) x C_other x M; Eq.5 Waste = min(WastePreserve, WasteChunkD). Here C = context tokens, M = memory per token, T_fwd = added forward time, T_INT = interception duration (estimated online as t_now - t_call, §4.4).

## 107. Agentix (formerly Autellix)

**read:** https://www.usenix.org/system/files/nsdi26-luo.pdf (NSDI '26 proceedings version). Paraphrased; numbers exact.

**verdict:** confirmed

**effect:**

Abstract (also §1 and §7): program throughput 4-15x higher at the same latency than state-of-the-art systems such as vLLM. §6.3: ShareGPT/BFCL up to 8x vLLM, 2x vLLM-opt and 1.5x MLFQ at high load; LATS 5x vLLM, 2.5x MLFQ, 2x vLLM-opt; Mixed up to 15x vLLM, 5.5x MLFQ, 5x vLLM-opt. Tail: up to 1.7x throughput at P95/P99 in 7 of 8 scenarios. §6.4 multi-engine (four LLaMA3.1-8B replicas and two 70B replicas; ShareGPT and LATS): up to 1.4x over naive load balancers, close to Preble. §6.2 setup: LLaMA-3.1-8B, 70B and Falcon-180B on 1, 4 and 8 GPUs; GCP a2-ultragpu-8g with 8x A100-SXM4-80GB. Baselines: vLLM v0.6.1 (FCFS), vLLM-opt (chunked prefill + prefix caching + multi-step scheduling), MLFQ (on vLLM-opt); all use the same max batch size. Metric: program-level token latency = average total program response time / tokens generated (for multi-threaded programs, critical-path time / total tokens across threads), stated to be proportional to JCT. Workloads: ShareGPT (chatbot), BFCL v3 (ReAct), LATS on HotpotQA (MCTS), Mixed; Poisson program arrivals. §3.2: within one program, cache-hit rate stays above 90%. No accuracy is reported (scheduling only). The paper gives no code link. All dossier figures match.

**mechanism and term:**

Correct, with one nuance. PLAS (single-threaded) and ATLAS (multi-threaded) schedule preemptively by the service each program has already received, cutting head-of-line blocking at call and program level (queueing). Preempted calls are swapped with custom kernels. Load balancing is data-locality-aware, keeping a program's calls on the engine that holds its KV (prefill via KV hits). Nuance: the paper says plain vLLM trails partly because it lacks a prefix cache, so part of the 8-15x over vLLM comes from prefix caching itself. The scheduling-only effect is the 2-5x over vLLM-opt. Credibility: passes.

**authors and venue:**

Michael Luo (UC Berkeley and Google DeepMind), Xiaoxiang Shi (SJTU), Colin Cai, Tianjun Zhang, Justin Wong, Yichuan Wang (UC Berkeley), Chi Wang, Yanping Huang, Zhifeng Chen (Google DeepMind), Joseph E. Gonzalez, Ion Stoica (UC Berkeley). 23rd USENIX NSDI, May 4-6, 2026, Renton WA. Matches references.md l.84.

**formula:**

PLAS, Eq.1: p(c_j) = sum over k<j with c_k.id = c_j.id of t_k (the PDF text renders the subscript as c_i.id; larger value = lower priority). ATLAS, Eq.2: p(c_j) = 0 if c_j is a root; otherwise max over parents c_k in P(c_j) of {p(c_k) + t_k}. Metric (§6.2, footnote 4): program-level token latency = total program response time / tokens generated, averaged; for multi-threaded programs, critical-path response time / total tokens across threads.

## 108. Vendor reasoning-effort controls

**read:** (1) Anthropic, 'Best practices for computer and browser use with Claude', https://claude.com/blog/best-practices-for-computer-and-browser-use-with-claude, dated May 13, 2026, section 'Tuning thinking effort for computer use' (curl, 28 Sep 2026). (2) Anthropic, 'Introducing Claude Opus 4.5', https://www.anthropic.com/news/claude-opus-4-5, dated Nov 24, 2025: section 'New on the Claude Developer Platform' and the 'Methodology' note. (3) OpenAI, 'Introducing GPT-5 for developers', dated August 7, 2025. openai.com returned a 403 bot-challenge page, so I read the Wayback snapshot http://web.archive.org/web/20260921161042/https://openai.com/index/introducing-gpt-5-for-developers/ (Coding section and the SWE-bench chart caption). (4) Anthropic effort docs, https://platform.claude.com/docs/en/build-with-claude/effort (undated, fetched 28 Sep 2026). I did not read the per-level values in the chart images on (2) and (3).

**verdict:** confirmed

**effect:**

All the recorded numbers are on the sources. Conditions that the record leaves out:

**(1) Anthropic blog (E81).**
- The medium-vs-high claim sits in the 'Claude 4.6 models' subsection. The scope note says the advice covers the 4.6 family (Opus 4.6, Sonnet 4.6, Haiku 4.5) and Opus 4.7.
- Wording: medium 'achieves close to the highest task success rate while using roughly half the output tokens of high'. With retries, medium and high 'converge to the same success rate'.
- Test set: 'a suite of end to end UI automation tasks spanning desktop applications, browsers, and multi-application workflows'. The post gives no task count, no success rates and no token counts. Its only basis is internal experimentation.
- Same subsection: low uses fewer total output tokens than thinking disabled, which the post attributes to fewer mistakes and retry cycles. Max gives 'no accuracy benefit over high'.
- The Opus 4.7 subsection is different: high uses roughly half the output tokens of max. On OSWorld Verified, Opus 4.7 at low 'scores similarly to Sonnet 4.6 on max, while using ~1/10th the tokens per task'.

**(2) Opus 4.5 launch (E88).**
- Quote: 'Set to a medium effort level, Opus 4.5 matches Sonnet 4.5's best score on SWE-bench Verified, but uses 76% fewer output tokens.'
- Also: 'At its highest effort level, Opus 4.5 exceeds Sonnet 4.5 performance by 4.3 percentage points—while using 48% fewer tokens.'
- Methodology note: all evals were averaged over 5 trials with a 200K context. SWE-bench Verified was run with no thinking budget.
- The text gives no per-level scores.

**(3) GPT-5 developer post (E88).**
- SWE-bench Verified: GPT-5 74.9% vs o3 69.1%. Quote: 'relative to o3 at high reasoning effort, GPT‑5 uses 22% fewer output tokens and 45% fewer tool calls'.
- Chart caption: the scores omit 23 of 500 problems, so 477 were scored. GPT-5 was given a short prompt that emphasised verifying its solutions, and the post says 'the same prompt did not benefit o3'.
- GPT-5's own effort level in this comparison appears only in the chart labels, which I did not read.

**(4) Effort docs (E88).**
- The page has no per-level numbers: it contains no percentage figures.
- Qualitative statements only: 'Lower effort also means fewer and terser tool calls', and 'Effort is a behavioral signal, not a strict token budget'.
- Defaults: high on most models; Claude Opus 5.5 defaults to medium.

**mechanism and term:**

The mapping is partly right: 'decode smaller' is correct for the effort knob itself, because the docs say effort applies to all output tokens (text, tool-call arguments, thinking).

**Corrections**
- Only E81, the Anthropic blog, compares effort levels on the same model. Both E88 numbers compare different models: Opus 4.5 at medium vs Sonnet 4.5's best, and GPT-5 vs o3 at high. They belong under the model-choice part of the price/tier term, not under the effort knob, and should not be cited as effort effects.
- 'Tool calls fewer' as an effect of effort is qualitative only (the Anthropic docs). The 45% figure is GPT-5 vs o3, across models.
- A success-rate/N interaction must be added. Per the blog, medium matches high only when retries are allowed, so first-attempt success is lower. That can raise the number of attempts, and cost per success has to count them.
- Too little thinking also raises retries: low effort uses fewer output tokens than thinking disabled. So N can move either way.

**Correct classification:** decode smaller per call. N (steps and retries) can move either way. Success rate is held only with retries. The time and money savings are not quantified at a stated scale.

**Credibility:** E81 is a vendor engineering doc (vendor-stated, internal tests, sample undisclosed). E88 is vendor launch claims, to be labelled vendor-stated/marketing.

**Proposed new D-entry:** E88's two numbers are model-choice effects, not effort ablations.

**authors and venue:**

All are vendor primary pages; the dates were checked on the pages. The Anthropic blog is dated May 13, 2026, as E81 says. The Opus 4.5 post is dated Nov 24, 2025. The GPT-5 developer post is dated August 7, 2025 (read via the 21 Sep 2026 Wayback copy). The effort docs are undated. The docs now list Claude Opus 5.5 as defaulting to medium, which postdates E88.

**formula:**

None. No source gives a formula for the saving.

## 109. Are Online Skill and Memory Modules Always Worth Their Tokens? (counter-evidence)

**read:** arXiv:2606.15017v2 PDF (30 Aug 2026), converted with pdftotext -layout: Tables 1–5, §3–§8. Also the v1 PDF (12 Jun 2026) to trace the recorded numbers, and the arXiv abs page (metadata and comment).

**verdict:** corrected

**effect:**

**The recorded numbers are from v1, not the current v2.**
- v1 Table 1 covers three WebArena domains (Shopping, Reddit, Admin; 475 tasks, calc.) with Gemini 3 Flash: Vanilla-IB 50.74% / 71.9K vs ASI 47.86% / 107.1K.
- v2 adds GitLab (180 tasks), giving four domains: Shopping 187, Reddit 106, Admin 182, GitLab 180 (655 tasks, calc.).

**v2 Table 1 (p. 6), Gemini 3 Flash.** Values are the mean of 3 runs, 'task-weighted mean over tasks of all four domains'. Tok = total tokens per task (K), counting prompt and completion tokens of all LLM calls, actor and modules.

| Method | Success rate | Tokens per task |
|---|---|---|
| Vanilla-IB | 44.78% | 73.6K |
| ASI | 41.02% | 107.3K |
| AWM | 39.34% | 99.3K |
| ReasoningBank | 39.33% | 82.6K |

- Vanilla-IB is a 15-step actor with rule-based pruning of the accessibility tree. The augmented actors are capped at 10 steps.
- Other models in v2, best augmented method on success rate:
  - GPT-5.4-mini: Vanilla-IB 32.67% / 90.2K vs ASI 29.00% / 99.8K.
  - Qwen 3.6-27B: Vanilla-IB 42.14% / 95.5K vs ASI 40.15% / 125.8K.

**WorkArena-L1 is not Gemini 3 Flash.** Table 2 (33 task types × 3 seeds) uses Qwen 3.6-27B only, and §8 confirms this.

| Method | Success rate | Tokens per task |
|---|---|---|
| Vanilla-IB | 55.56±2.9% | 109.4K |
| AWM | 53.53% | 102.8K |
| ASI | 48.49% | 113.8K |
| ReasoningBank | 55.56% | 120.3K |

On WorkArena, Vanilla-IB uses more tokens than AWM.

**What is not measured:** no dollars, no cache-hit/miss split and no wall-clock time.

**mechanism and term:**

'Prefill larger; success rate lower' is right, but incomplete.

**Mechanism**
- Augmentation (AWM, ASI, ReasoningBank) adds extra LLM module calls: workflow induction, skill synthesis, retrieval and verification. So model calls per pass (c_k) go up.
- It also injects the retrieved workflows or skills into the actor prompt at every step, so each pass reads more prompt tokens (prefill larger). The paper calls this a 'double cost'.
- Table 3 (Gemini 3 Flash, Shopping): actor prompt 45.2K for Vanilla-IB vs 64.1K for AWM and 61.8K for ASI; ASI's module prompts add 20.0K.
- The budget-matched baseline changes two terms. N goes up (horizon 10 → 15). The pruning makes the per-step observation text smaller, which lowers prefill and context growth.
- Table 5 separates them: the longer horizon drives the success gain, and the pruning drives the token saving.

**Classification:** counter-evidence to the 'skills/memory cut passes' route. ASI's skills are meant to lower N, but under online token accounting they raise c_k and prefill without raising success.
- §5.2 adds that ASI's skills break when the accessibility-tree IDs change.
- §6 notes that online memory makes tasks depend on each other in sequence, which rules out running tasks in parallel. That is a structural cost the other methods avoid.

**authors and venue:**

Authors confirmed on the v2 abs page and PDF p. 1: Hajimiri, Aminbeidokhti, Dolz, Ben Ayed, Laradji, Gella, Gontier. Gella and Gontier are marked as equal advising. Affiliations: ServiceNow AI Research, ÉTS Montreal, University of British Columbia, McGill University.

The v2 comment reads 'Accepted to EMNLP 2026'. A web search on 28 Sep 2026 found no official EMNLP page listing it, so it stays a flagged preprint. It passes the credibility rule: verifiable authors and institutions, a public benchmark, task counts and models stated.

Cite v2, not v1. Proposed new D-entry: the v1 → v2 change of numbers and domains, and the WorkArena model mix-up.

**formula:**

No formula for cost or speedup. The nearest is §6 'Parallelism': Vanilla-IB has no cross-task state, so with N workers the end-to-end wall-clock drops 'by up to a factor of N'. Here N means workers, not passes, which clashes with our N.

## 110. AI Agents That Matter (joint cost-accuracy optimization)

**read:** arXiv:2407.01502v1 PDF (1 Jul 2024; the only arXiv version), converted with pdftotext -layout: §2–3, Tables A1–A3, Figs A1, A3, A5 and A6, Appendices A.1 and B.1. Also the TMLR BibTeX and listing at jmlr.org/tmlr (bib/Zy4uFzMviZ.bib; listing 'June 2025'). I could not read the TMLR camera-ready PDF on OpenReview (403 browser-challenge), so the numbers are checked against arXiv v1 only.

**verdict:** confirmed

**effect:**

**HotPotQA, Table A3 (p. 23), GPT-3.5.**
- Setup: gpt-3.5-turbo-0125 via Azure, May 2024 prices $0.5/$1.5 per 1M input/output tokens. Optimised on 100 training samples, evaluated on 200. Metric: retrieval accuracy, meaning all ground-truth documents were retrieved. Mean of 5 runs.
- DSPy random search: accuracy 0.495, variable cost $0.376 per 100 inferences, fixed cost $2.696.
- Joint optimization: accuracy 0.509, variable cost $0.174, fixed cost $2.714.
- §3.2 says '53% lower variable cost with similar accuracy' against both default DSPy versions.
- Llama-3-70B: 41% lower ($0.643 → $0.374), but accuracy falls from 0.617 to 0.601.

**HumanEval, Table A1 (p. 20).**
- Setup: 164 problems, LDB's modified version. gpt-4-turbo-2024-04-09 at April 2024 prices. Cost is the total over all 164 problems, mean of 5 runs.
- Warming (GPT-4): 93.2%, $2.45.
- LATS (GPT-4): 88.0%, $134.50.
- §2.3 says LATS costs 'over 50 times more'. The 54.9× ratio is calc.

**Correction to the recorded '95% t-CIs':** the parentheses in both tables are minimum–maximum ranges. The 95% Student-t intervals appear only as error bars in Figs A1 and A5.

**mechanism and term:**

'Money and success rate (cost-per-success frontier)' is right as a framing, but name the terms.

**HotPotQA.**
- Joint optimization uses Optuna to search the temperature and the number and choice of few-shot examples, and whether to include formatting instructions.
- That shortens the input prompt, so prefill (uncached input tokens) goes down, and so does the money per attempt, at similar success.
- In exchange it adds a one-time fixed optimization cost that sits outside the per-task formula.
- Break-even against DSPy few-shot: after 1,275 inferences (GPT-3.5) and 1,332 (Llama-3-70B), per Fig. A6. The text rounds this to 1,350 tasks.

**HumanEval.**
- The simple baselines (retry and warming, at most 5 calls) beat LATS tree search mainly on the number of model calls and tokens: N and c_k go down.

**Caveats**
- Neither benchmark is web or computer-use: one is code generation, the other multi-hop retrieval QA.
- The paper's time axis (Fig. A3) is the sum of API inference times, not wall-clock.
- It is a measurement-method paper with an optimization example.

**authors and venue:**

Authors confirmed in v1: Kapoor and Stroebl (equal contribution), Siegel, Nadgir and Narayanan, all Princeton University. The venue is confirmed by the jmlr.org TMLR BibTeX (TMLR, 2025, OpenReview id Zy4uFzMviZ, same five authors in the same order), and the TMLR listing says 'June 2025'. The published PDF could not be read.

**formula:**

No equation. Stated in words:
- §3: total cost = fixed cost (one-time optimization) + variable cost (per run, depends on input and output tokens).
- Footnote 2: the Pareto frontier is kept convex because agents A and B can be mixed by calling A with probability p and B with probability 1−p.
- The break-even is shown only as a graph (Fig. A6). Our check: (2.714 − 0.029) / (0.00384 − 0.00174) ≈ 1,279 inferences for GPT-3.5 (calc.).

## 111. UiPath Healing Agent (vendor, qualitative)

**read:** docs.uipath.com, Agents user guide for Healing Agent (undated), fetched with curl on 28 Sep 2026: /licensing, /what-is-healing-agent, /deterministic-recovery-strategies and /frequently-asked-questions. A web search the same day found only the per-tenant Insights Healing Agent dashboard. I did not read the 'Configuring LLMs for your product' page that the FAQ points to for the model used.

**verdict:** confirmed

**effect:**

**No effect number.** None of these pages publishes a heal success rate, a heal latency or a cost per success, which confirms E160.

**Pricing (licensing page)**
- 'One charge equals 3 Platform Units.'
- You are charged once per recommendation or once per self-healing action, at the same price either way. Failed self-healing actions are not charged. Within one job, an activity is charged once.
- 'Healing information from a previous run is not retained in the next run', so the next job run heals again and is charged again.
- The 5,000 heals/year are included only in Unified Pricing Enterprise and the Flex Advanced platform SKU. Other plans need a paid add-on that includes 5,000 heals/year (Standard) or a consumable add-on (Basic).
- Flex overage is 15 Agent Units per recommendation or heal. The 60-day trial includes 200 heals.
- No USD price per Platform Unit is given.

**mechanism and term:**

**Mechanism: corrected.**
- The strategies page does not list '8 deterministic strategies plus AI'.
- Five come before the 'AI-based recovery strategies' heading: target definition change, dynamic timing, anchor vs target position change, AppCard title, and Semantic Selector.
- Three come under that heading: overlay or pop-up, semantic targeting, and Computer Vision.
- The outcomes are compared through a 'multi-strategy voting system' (FAQ). With AI turned off, it falls back to Levenshtein text matching.
- Trigger: a UI Automation (Modern) activity fails at runtime, followed by 'Just-in-Time' analysis.
- Write-back is not automatic. A licensed user imports the recommendations into Studio and applies them. Self-healing fixes are not kept for the next run.

**Terms: corrected.** 'N and c_k → 0' is wrong for N.
- On a normal run the robot still executes every step, so N and the environment terms (observe, act, wait) stay.
- Only the model terms go to zero: c_k = 0, so no queueing, prefill or decode, and no context growth.
- On failure, model calls happen only at the failing step. There is also a per-heal licence charge that recurs on every run until a developer applies the fix.
- Success-rate risk (wrong element) is handled by voting and the recommendations-only mode; no number is given.

**Credibility:** vendor primary docs; mechanism and price only.

**authors and venue:**

Vendor primary docs, all undated, fetched 28 Sep 2026.

**formula:**

None.

## 112. Microsoft Power Automate self-healing / Repair with Copilot (vendor, qualitative)

**read:** Two pages, both fetched with curl on 28 Sep 2026: https://learn.microsoft.com/en-us/power-automate/desktop-flows/self-healing (ms.date 2026-06-30, updated 2026-07-11) and https://learn.microsoft.com/en-us/power-automate/faqs-repair-copilot (ms.date 2026-01-16).

**verdict:** confirmed

**effect:**

**No numbers.**
- The self-healing page gives no success rate or latency.
- The Repair with Copilot FAQ describes its evaluation only in words (quantitative and qualitative metrics 'we're tracking') and discloses no figures.

**Price.** Self-healing 'is currently available for organization premium accounts at no additional cost. Usage may be subject to service limits or changes.'

**mechanism and term:**

**Corrected: the recorded row merges two different features.**

**(a) Self-healing (preview, 2026).**
- Triggers on 'Element not found' or 'Window not found'.
- Runs after the retry policy. The order is Retry policy → Self-healing → Set variable/Run subflow rules → Continue/Throw.
- Sends a screenshot of the missing element, the parent-window title and the full desktop image.
- Uses 'GPT‑4.1 mini and Claude Sonnet 4.5' in combination.
- Runtime only; single-element actions only; no user approval.
- The page does not say the repaired selector is saved. It logs the attempt as repairWithAIInfo and expects a manual fix of the flow later.
- It warns the model 'might occasionally identify an unintended UI element'.

**(b) Repair with Copilot at runtime (earlier; preview, US and English only).**
- Input is the old selectors plus the UI hierarchy tree, not a screenshot; output is an element ID.
- The user must approve the repair, and 'can ... save the repaired selector for future execution'.
- So the optional save belongs to (b), and the two LLMs and the screenshot belong to (a).

**Terms:** same as UiPath. c_k = 0 on normal runs; N and the environment terms are unchanged, so 'N → 0' is wrong; a model call happens only at the failing step. The success-rate risk of a silent wrong-element heal is admitted by the vendor but not quantified.

**Proposed D-entry:** separate the two features in E151/E152 wherever they are summarised together.

**authors and venue:**

Microsoft Learn primary docs. The dates come from the pages' metadata: self-healing ms.date 2026-06-30 (updated 2026-07-11); Repair with Copilot FAQ ms.date 2026-01-16.

**formula:**

None.

## 113. Automation Anywhere Generative Recorder (vendor)

**read:** (1) https://www.automationanywhere.com/products/automator-ai (undated, curl, 28 Sep 2026). (2) Community Product Club recap 'Generative Recorder and Resilient Automation | April 2024', dated May 13, 2024 and posted by 'Automation Anywhere Team' (hosts include Rajendra Vijay, Director of Product Management), https://community.automationanywhere.com/generative-recorder-85080/generative-recorder-and-resilient-automation-april-2024-88211. (3) The docs pages docs.automationanywhere.com/r/automation-360/generative-ai-based-fallback and /gr-overview are rendered by JavaScript. curl returned only a loader, and WebFetch returned only the trigger sentence, so I could not read the full docs pages.

**verdict:** confirmed

**effect:**

**Marketing page (1).**
- Exact wording: 'Build automations that fix themselves. With GenAI fallback, workflows stay on track, reducing execution failures by over 60%'.
- The same page also claims '60% greater accuracy', '60% higher resiliency' and 'Speed up development by 30%'.
- None of these gives a baseline, task set, period or definition. They are vendor marketing (E150) and not evidence.

**New vendor-stated number in the recap (2).**
- Quote: 'In customer previews, we've observed nearly 50% success rate for automation failures that are addressed by Generative Recorder.'
- It gives no count of failures, no customers, no period and no definition, so it is vendor-stated and not a measurement.
- It qualifies E160's absolute statement that no vendor publishes a heal success rate. Proposed D-entry: E160 should say no vendor publishes a defined, sampled rate, and should mention AA's undefined 'nearly 50%'.

**mechanism and term:**

**Mechanism: confirmed, with details from the recap and the docs' trigger sentence.**
- Trigger: the object is not detected within the time-out. Then one of two fallbacks runs:
  - Native fallback uses design-time data, such as multiple paths to the element.
  - Generative AI-based fallback uses live application data. It extracts only the element's source with its parent and child, anonymises business data, and prompts a generative model.
- A developer pop-up offers 'Stop Automation', 'Skip update' or 'Update value'. 'Update value' rewrites the DOMXPath; in A.32 only the DOMXPath is updated.
- An auto-update is recommended only at '100% confidence'.
- The fallback wait is configurable: 'say 30 or maximum 60 seconds'.
- The LLM is not named.

**Terms: corrected like the other RPA rows.**
- c_k = 0 on normal replay; N and the environment terms stay, so 'N → 0' is wrong.
- On failure there is a model call at that step, plus up to the configured fallback wait.
- Once the developer accepts 'Update value', later runs return to c_k = 0 for that step.

**Credibility:** the mechanism comes from a vendor community post (primary); the 60% claims are marketing, not to be cited; the 50% is vendor-stated and undefined.

**authors and venue:**

Vendor sources. The community recap is dated 13 May 2024 and presented by AA product managers. The marketing page is undated. The docs pages could not be read beyond their trigger sentence.

**formula:**

None.

## 114. Think Twice, Click Once (FOCUS)

**read:** https://arxiv.org/pdf/2503.06470v1 (v1, 9 Mar 2025; the only version), read in full with pdftotext; the arXiv abs page was used for authors and version history

**verdict:** corrected

**effect:**

The numbers are right, but the baseline is not what the row implies. App. A.2 ('Ablation Studies On α') and Fig. 4: the baseline 'w/o α' is the same FOCUS model (Qwen2-VL-2B-Instruct, fine-tuned). A.2 says it 'automatically switches between systems based on initial token probabilities', reaching 74.8% accuracy at 3.2 s average processing time. At α = 0.6 it reaches 77.4% at 2.6 s. Fig. 4 caption: '+2.6% accuracy improvement while reducing processing time by 0.6s compared to baseline'. The same caption calls this baseline 'without Adaptive System Switching', which does not match A.2. Slow-only (α = 1.0, §3.3.2) gives 73.4% at 5.4 s. The fast system handles 66.5% of samples (Fig. 5: text 76.9% fast, icon/widget 43.7% slow, n = 1,272). Conditions: ScreenSpot, 1,272 samples (§3.1); one A100 40GB; HF Transformers; bf16; max output 4,096 tokens (App. A.3). '−18.75%' is calc. (0.6/3.2). 's/sample' is our reading: the paper says only 'Average Time (s)' / 'processing time'. Fast-only (α = 0) accuracy and time appear only as plotted points in Fig. 4, not in the text. α was chosen by a sweep on ScreenSpot itself, and no separate validation split is reported. Against slow-only, the saving is 5.4 → 2.6 s (calc. −52%) with accuracy 73.4 → 77.4%.

**mechanism and term:**

'Calibrated confidence' is wrong. Nothing is calibrated. The switch (§2.3, Eqs. 2–3) compares the first-token probabilities of the slow-start token and the grounding-start token, weighted by a hand-set α: p_slow = α·p(t=t_s|s,i) and p_fast = (1−α)·p(t=t_g|s,i). The mode with the higher value wins. Proposed wording: 'fast/slow grounding switch on α-weighted first-token probabilities (α = 0.6)'. Term: decode smaller within a single grounding call, because only about a third of samples generate the three-stage slow chain (interface summary + focused analysis + coordinates). N and c_k do not change. This is single-step grounding, not an end-to-end agent task. D-ledger candidate: dossier §3.7 row and the §3 'Early exit' row (3.2→2.6 s) need the baseline stated as 'same model, unweighted switching', not a non-adaptive or fast-only model.

**authors and venue:**

arXiv abs page lists 10 authors: Fei Tang, Yongliang Shen, Hang Zhang, Siqi Chen, Guiyang Hou, Wenqi Zhang, Wenqiao Zhang, Kaitao Song, Weiming Lu, Yueting Zhuang. PDF affiliations: Zhejiang University (nine authors) and Microsoft Research Asia (Kaitao Song). There is only v1, with no comments and no journal-ref, and a web search found no venue. It is a preprint. Credibility rule: passes (i) authors and institutions on the arXiv PDF, (ii) university plus company lab, (iii) public benchmark ScreenSpot with 1,272 samples and the model stated (Qwen2-VL-2B-Instruct base), (iv) not a single-author industry report. It can go into references.md as a preprint.

**formula:**

No speedup or cost formula. The only equations are the switching rule, Eq. (2) p_slow(t|s,i) = α·p(t = t_s|s,i) and Eq. (3) p_fast(t|s,i) = (1−α)·p(t = t_g|s,i), with the higher one activated (§2.3). Eq. (1) is the training-data accuracy criterion.

## 115. GUI-G1

**read:** https://arxiv.org/pdf/2505.15810v2 (v2, 22 May 2025, latest arXiv) plus the NeurIPS 2025 camera-ready https://papers.nips.cc/paper_files/paper/2025/file/89dcbea9f19960edd7765068adb13b1d-Paper-Conference.pdf. The numbers are identical in both. The token table is App. D.2 Table 7 in arXiv v2 and App. D.3 Table 10 in the camera-ready.

**verdict:** confirmed

**effect:**

Table 4 (ScreenSpot, Avg.): InfiGUI-R1-3B 87.5 (32K training samples) vs GUI-G1-3B 90.3 (17K). Table 7 (arXiv) / Table 10 (NeurIPS), captioned 'Average number of output tokens generated per example on ScreenSpot during inference', Mobile/Desktop/Web: InfiGUI-R1-3B 107/107/114, GUI-G1-3B 37/39/39. App. D.2 says 'approximately one-third as many on average'. Conditions the row should carry: (1) baseline accuracies are cross-paper. §4 says they compare 'using results reported in their original papers', so 87.5 was not re-run. (2) How the InfiGUI-R1-3B token counts were measured is not described. (3) The comparison is between two differently trained models (different data, reward and objective), not a same-model reasoning on/off ablation. (4) The ScreenSpot sample count is not stated in the paper. (5) Latency and wall-clock are not reported anywhere; no timing was found in either version. ScreenSpot-Pro: 37.1% vs 35.7% for InfiGUI-R1-3B and UI-TARS-7B.

**mechanism and term:**

Broadly right, but GUI-G1 is a training recipe, not an inference switch. RL on Qwen2.5-VL-3B-Instruct combines (a) a 'Fast Thinking Template' with no <think> section, (b) Hit+IoU reward plus a box-size term against reward hacking, and (c) GRPO with length normalisation removed (|o_i| → Max_Tokens) and a difficulty weight w_p. Term: decode smaller (output tokens per grounding call about 1/3). The accuracy gain cannot be attributed to dropping reasoning alone. The paper's own supporting evidence is §3.1 / Fig. 2: longer reasoning chains lower grounding accuracy on ScreenSpot. Single-step grounding only.

**authors and venue:**

Yuqi Zhou, Sunhao Dai, Shuai Wang, Kaiwen Zhou, Qinglin Jia, Jun Xu. Affiliations: Gaoling School of Artificial Intelligence, Renmin University of China, and Huawei Noah's Ark Lab. NeurIPS 2025 is confirmed on the official page https://neurips.cc/virtual/2025/poster/120227 (poster; same six authors) and in the camera-ready footer ('39th Conference on Neural Information Processing Systems (NeurIPS 2025)'). Because the work is published, the preprint rule does not apply. The references.md entry should cite the NeurIPS version.

**formula:**

No speed or cost formula. §3.1 defines a text ratio (n_ins + n_think)/(n_img + n_ins + n_think), where n_think is the number of output reasoning tokens. §3.3 / Table 2 modify the GRPO objective (|o_i| → Max_Tokens; J_GRPO → w_p·J_GRPO). Both are analysis or training quantities, not cost models.

## 116. TAB (Turn-Adaptive Budgets; 'Not All Turns Are Equally Hard')

**read:** https://arxiv.org/pdf/2604.05164v3 (v3, 8 Aug 2026, latest), read in full. For version comparison also read https://arxiv.org/pdf/2604.05164v1 (6 Apr 2026) and https://arxiv.org/pdf/2604.05164v2 (14 Apr 2026).

**verdict:** corrected

**effect:**

The agentic numbers are confirmed, but only in v3. §4.2 and the Fig. 2 caption: TAB saves 'up to 20% of Budgeter and Solver tokens over Static and LLM-Judge baselines' on BFCLv4 Multi-Turn, Tau-Bench (retail and banking subsets) and TerminalBench 1.0 (medium). Fig. 3 caption: 'up to 15% in overall system latency', after the Budgeter's own inference overhead is counted. Conditions: the Budgeter is Qwen3-4B, LoRA+GRPO-trained on MATH Level-5 only (zero-shot transfer to the agent benchmarks). The Solver is L1-Qwen3-8B-Exact hosted locally for BFCL (budgets {256…4096}) and the GPT-5.4-nano API for Tau-Bench and Terminal-Bench (budgets = reasoning effort {none, low, medium, high}). The User LLM is Qwen3-8B for BFCL and GPT-5.4-nano for Tau-Bench. Baselines: Static, LLM-Judge Individual, LLM-Judge Multi-Turn. Global budgets B ∈ {3k, 5k, 8k, 10k}. No task counts are given for any agentic benchmark, and no hardware is given. Accuracy appears only as frontier curves (Figs. 2–3), so there is no numeric paired accuracy delta, and the 'up to' values are frontier maxima. The 35% tokens (User+Budgeter+Solver) and 30% latency come from 5 math datasets (MATH-500, AMC23, MATH Level-5, OlympiadBench, AIME25) with a Qwen3-1.7B Budgeter (Fig. 4, Fig. 5, §4.2). Yet the v3 abstract says 'Our experiments on diverse agentic benchmarks' show 35% and 30%. v1 and v2 contain no BFCL, Tau-Bench, Terminal-Bench or latency results. Their abstracts say 'Our experiments on mathematical reasoning benchmarks … saving up to 35% tokens'. 'Tau-Bench' is cited to Barres et al. 2026, τ²-bench (ICML 2026).

**mechanism and term:**

Mechanism correct. A GRPO-trained Budgeter picks the per-turn budget b_t from the history x_{1:t−1} and the current turn q_t, under a soft global per-problem budget B. Terms: (1) decode smaller: Solver output and thinking tokens per turn. (2) One extra small-model Budgeter call per turn (c_k +1); its tokens and latency are inside the reported 20% and 15%. (3) Secondary: smaller context growth, because each y_t is appended to the trajectory; the paper argues this in §1. For GPT-5.4-nano the lever is the vendor's per-turn reasoning-effort setting. D-ledger candidates: (a) extend D50. The agentic 20%/15% figures exist only in v3, so pin the dossier URL to v3. The v3 abstract now attributes the math-derived 35%/30% to 'diverse agentic benchmarks'. (b) The dossier's 'τ-bench' is τ²-bench retail+banking per the paper.

**authors and venue:**

Neharika Jali, Anupam Nayak, Gauri Joshi; Carnegie Mellon University (PDF header and @andrew.cmu.edu emails). arXiv cs.LG with 3 versions, no comments or journal-ref, no venue. It is a preprint. Credibility rule: (i), (ii) and (iv) pass. (iii) is only partly met: the public benchmarks and models are stated, but no task count is given for BFCL Multi-Turn, the Tau-Bench subsets or Terminal-Bench medium, so it fails (iii) as literally written. That needs Edwin's decision: 'Not used', or cited with an explicit 'task counts not stated' caveat.

**formula:**

Eq. (1): π*_φ = argmax_π E_{x,π}[ acc(x) − λ·max(0, Σ_{t=1}^{T} b_t − B) ], where acc(x) = 1{y_T = y*_T}, B is the global per-problem token budget and λ the violation penalty. Eq. (2): the same form as the terminal GRPO reward r^(i,g) = acc(x^(i,g)) − λ·max(0, Σ_t b_t^(i,g) − B), with λ = 0.001 (§4.1). Footnote 1: training uses the tokens the Solver actually used, not the allotted b_t. Eq. (3) is the clipped GRPO objective. The speedup itself has no formula.

## 117. TSDS (Think Short, Defer Smart, Act, and Repeat)

**read:** https://arxiv.org/pdf/2607.26865v3 (v3, 25 Sep 2026, latest), read in full. Also read https://arxiv.org/pdf/2607.26865v2 (26 Aug 2026), the version the dossier cites.

**verdict:** corrected

**effect:**

The MBPP numbers are in both v2 and v3, App. G.4 Table 3, 'averaged over 50 random 60/40 calibration–test splits, with n_test = 103 problems per split' (257 evaluation problems). Policy: R̂ / Ĉ_D / Ĉ_L tokens. E-ReAct 0.719 / 0.000 / 1183. Cloud ReAct 0.810 / 1.000 / —. E-ReAct-TC (λL = 0.80) 0.620 / 0.000 / 422. ReDAct-CD (λL = ∞) 0.779 / 0.786 / 1206. TSDS 0.714 / 0.346 / 422. §5.2: '64% fewer thought tokens than E-ReAct and ReDAct-CD'; App. G.4: 'approximately 65% (422 versus 1206)'. Conditions the row lacks: (1) the edge model is DeepSeek-R1-Distill-Qwen-7B and the cloud model DeepSeek-R1-Distill-Qwen-32B, with L_max 2048, R_min 0.69, C_D^max 0.70, δ = 0.10, |Λ| = 45. (2) Ĉ_L counts only edge thinking tokens; App. G.4 says cloud-generated tokens are not included. (3) §5.2 calls MBPP 'a single-step setting, i.e., T = 1'. (4) ReDAct-CD violates the deferral budget (0.786 > 0.70). (5) No latency or wall-clock is reported. Version change: the '22/50 certified splits' condition exists only in v2 App. G.4 ('TSDS certifies in 22/50 splits; across those 22 splits…'). v3 replaces it with 'Reported means and standard deviations are computed across the 50 partitions', keeping the same values (0.714 ± 0.026; 422 ± 118). v3 §3 also says an empty certified set falls back to E-ReAct with full thought (~1183 tokens), which is hard to square with a 422 ± 118 mean over all 50 splits. This is unresolved. For a multi-step agentic figure, see App. G.3 (HotpotQA, T_max = 7, 250 validation problems, 50 random 75/25 splits, edge 7B / cloud 14B): 'approximately 43% fewer thinking tokens (742 versus 1312)' than ReDAct-CD, at higher test reward (reward values shown only in the figure). The abstract claims 43%–65% over deferral-only baselines across HotpotQA, MBPP and household robot.

**mechanism and term:**

Partly right. Two parts, jointly calibrated with Learn-Then-Test (finite-sample guarantees on reward and cloud-call rate). (a) An EMA convergence probe on hidden states (layer ℓ = 5, queried every 16 thought tokens) halts edge thinking once the intended action has stabilised. (b) A perplexity-based rule defers uncertain actions to a cloud model. Terms: decode smaller on the edge. For price/tier and c_k, deferred steps add a call to a larger cloud model (34.6% of MBPP problems), whose tokens are outside Ĉ_L. The row's 'success lower' holds only against ReDAct-CD (−6.5 pp calc.), which breaks the deferral cap. Against E-ReAct (no deferral, full thought) success is 0.719 → 0.714 (−0.5 pp calc.) at 1183 → 422 edge thinking tokens (−64% calc.). MBPP is not an agentic multi-step task. D-ledger candidate: the v2 → v3 change ('22/50 certified splits' dropped; same numbers now described as over all 50 splits).

**authors and venue:**

Amirmohammad Farzaneh, Osvaldo Simeone; Institute for Intelligent Networked Systems (INSI), Northeastern University London (PDF header and @nulondon.ac.uk emails). arXiv stat.ML with 3 versions, no comments or journal-ref, no venue. It is a preprint. Credibility rule: passes (i) and (ii) (university), (iii) (MBPP 257 evaluation problems, HotpotQA 250 validation problems, models named) and (iv) (two academic authors). The dossier row omits the institution.

**formula:**

Eq. (2): L_t = min{ argmin_i { i : C_{t,i} > λ_L }, L_max }, the stopping position. Eq. (3): C_D(λ) = E[(1/T) Σ_{t=1}^{T} D_t] (deferral rate) and C_L(λ) = E[Σ_{t=1}^{T} L_t] (thinking cost). The text also defines C_S(λ) = E[T] (episode length). Eq. (4): min_λ C_L(λ) subject to R(λ) ≥ R_min and C_D(λ) ≤ C_D^max. Eq. (8), Proposition 1: P(R(λ̂) ≥ R_min and C_D(λ̂) ≤ C_D^max) ≥ 1 − δ.

## 118. EET (Experience-Driven Early Termination)

**read:** https://arxiv.org/pdf/2601.05777v2 (v2, 20 Apr 2026, latest arXiv) and the published version https://aclanthology.org/2026.findings-acl.1652.pdf (Findings of ACL 2026, pp. 33008–33024). Table 1 values are identical in both.

**verdict:** confirmed

**effect:**

Table 1 (RQ1), GPT-5-mini, Agentless: 33.2% resolved, 4,500 API calls, 35,919,315 input tokens, 1,861,379 output tokens, $13.77. With EET: 41.0%, 3,310, 17,306,929, 912,076, $6.18. Change: +7.8% (the caption says resolved changes are absolute differences), −26.4%, −51.8%, −51.0%, −55.1%. §4.5 defines Total Cost as the total 'across the benchmark', i.e. SWE-bench Verified, 500 tasks (§4.2), so the $ figures are totals, not per task (calc. $0.0275 → $0.0124 per task). The other configuration is Trae Agent / DeepSeek-V3.2 at 70.2% → 70.0% (−0.2 pp); McNemar p = 0.460, not significant (§5.1). Six-config averages: cost −31.8% (range 19.3–55.1%), API calls −20.8%, input tokens −29.9%, output tokens −25.1%; early termination on 11.3% of issues (Table 2). Conditions the row lacks: (1) for Agentless, EET is applied only to patch selection (§4.3). (2) The experience base comes from 207 SWE-bench Lite tasks after removing overlap with Verified (§4.2). (3) Its one-time offline generation cost, $4.3 for Agentless/GPT-5-mini (App. J, Table 16), is excluded from Table 1; calc.: $6.18 + $4.3 = $10.48 vs $13.77 (−23.9%) if charged to this one run. (4) Thresholds τ_sim = 0.15, τ_gen = 90, τ_upper = 90, τ_lower = 40 were tuned on 100 SWE-bench issues outside Verified and Lite. (5) The price basis (per-token prices, caching) is not stated. (6) Wall-clock time is not reported.

**mechanism and term:**

Right in substance. TF-IDF retrieval picks the top-1 structured experience (from successful past resolutions only) and injects it into the prompt. During patch generation, an LLM-scored confidence at milestones (after a code edit and after a test run) stops generation above τ_gen. After each patch, a confidence score above τ_upper or below τ_lower stops further candidate patches ('good enough' or 'hopeless'). Terms: N smaller (fewer iterations and fewer candidate patches; for Agentless, only fewer candidates), so fewer model calls (−26.4%) and fewer input and output tokens. That lowers money, even though EET adds experience text and confidence prompts to calls (included in the totals). Success rises for Agentless (+7.8 pp GPT-5-mini, +7.2 pp DeepSeek-V3.2) and changes by −0.2 to +1.0 pp for the autonomous agents. Environment-machine hours are not measured.

**authors and venue:**

Yaoqi Guo, Ying Xiao, Jie M. Zhang, Mark Harman, Yiling Lou, Yang Liu, Zhenpeng Chen (corresponding). Affiliations: Nanyang Technological University, King's College London, University College London, University of Illinois Urbana-Champaign, Tsinghua University. Findings of ACL 2026 is confirmed on the ACL Anthology page https://aclanthology.org/2026.findings-acl.1652/ (pp. 33008–33024) and in the arXiv comments ('Accepted by … ACL 2026 Findings Track'). It is published, so the preprint rule does not apply. The dossier gives no institutions; add them.

**formula:**

None. The efficiency metrics are plain totals across the benchmark (# API calls, # input tokens, # output tokens, total cost in USD, §4.5). There is no speedup or cost formula and no per-token price table.

## 119. Does Chain-of-Thought Reasoning Help Mobile GUI Agents? An Empirical Study

**read:** https://aclanthology.org/2026.findings-acl.392.pdf (Findings of ACL 2026, pp. 7981–7996; the published version), read in full with pdftotext. The ACL Anthology landing page was checked for title and pages.

**verdict:** corrected

**effect:**

Table 4 (§4.4), 'Performance of GLM-4.6V on AndroidControl under different reasoning token budgets', using the step-instruction prompt configuration. Budget: action-type accuracy / action accuracy (%). 0 (no reasoning) 76.83 / 70.32. 128 77.81 / 71.55. 256 77.65 / 71.00. 512 77.12 / 70.38. 1,024 76.98 / 70.33. Unconstrained 76.90 / 70.41. The paper compares against no reasoning: the 128-token budget 'yields a 0.98% improvement in action type accuracy and 1.23% improvement in action accuracy over the non-reasoning baseline'. The row's +1.14 pp vs unconstrained is calc.; also calc., no reasoning vs unconstrained is −0.09 pp. Conditions: the number of AndroidControl evaluation samples is not stated (the dataset is described as 'more than 14K tasks'); there are no repeated runs or significance tests; token counts per budget are not reported for GLM-4.6V; latency is never measured. Output tokens are reported for Claude 3.7 Sonnet only: reasoning uses at least 3.11× and up to 14.78× the output tokens of the base model (Fig. 4), and on ScreenSpot (mobile subset) 37.6 → 238.5 tokens.

**mechanism and term:**

This is an empirical study, not a proposed method. It compares six base vs reasoning-enabled VLM pairs on ScreenSpot (mobile subset), AndroidControl and AndroidWorld (116 tasks), and sweeps reasoning budgets for GLM-4.6V on AndroidControl only. Term: decode smaller (reasoning tokens capped or disabled), with no loss of success on this static, single-step action-prediction benchmark. Caveat for the classification: on interactive AndroidWorld, Claude 3.7 Sonnet with thinking scores 64.7%, 6.3 pp above its non-reasoning version with set-of-mark prompting (§1). So disabling reasoning is not shown to be free in interactive settings, and the budget sweep was not run there.

**authors and venue:**

Li Zhang (Beijing University of Posts and Telecommunications; Tsinghua University), Longxi Gao (BUPT), Mengwei Xu (BUPT, corresponding); Zhang and Gao contributed equally. Findings of ACL 2026 is confirmed on the ACL Anthology page https://aclanthology.org/2026.findings-acl.392/ (pp. 7981–7996) and in the PDF footer ('July 2-7, 2026'). It is published, so the preprint rule does not apply. The dossier's 'BUPT/Tsinghua' is correct.

**formula:**

None. The paper reports token ratios (3.11×–14.78×) and accuracies but gives no speed or cost formula.

## 120. CacheScout

**read:** https://arxiv.org/abs/2608.14624 (v1 is the only version, 16 Jul 2026); PDF https://arxiv.org/pdf/2608.14624v1 read in full via pdftotext; HTML https://arxiv.org/html/2608.14624v1 used for Eq. 9. Wording below is paraphrased because of quote limits; numbers, conditions and locations are exact.

**verdict:** corrected

**effect:**

The numbers are confirmed, but the stated baseline and some conditions need correcting. Abstract (p.1) and §1 'Summary of results' (p.2): KV hit rate +10–18 pp (reaching 81–85%), mean TTFT −18–45%, mean per-turn latency −29–38%, peak throughput +19–57% (the abstract says 'up to 57%'). At the same latency budget it sustains 1.7–12× the load of vanilla vLLM and 4.2–16× that of Continuum (§5.2). BASELINE: §5.2 ties the +10–18 pp explicitly to vanilla vLLM (prefix caching with LRU). The TTFT, per-turn and throughput ranges are given without naming a comparator: Figs 8b and 10 show one % per workload, most likely against vLLM. Continuum (TTL 0.3 s) is a second plotted baseline, not the reference for these ranges. So 'vs vLLM and Continuum' should read 'vs vanilla vLLM (Continuum also plotted)'. SETUP (§5.1): Llama-3.1-8B-Instruct on 8× NVIDIA RTX PRO 6000 Blackwell (96 GB), vLLM v0.11 V1. Four workloads (GSM8K, MT-Bench, GAIA, SWE-bench) all run on one six-agent supervisor framework using AutoGen SelectorGroupChat, with the LLM choosing the route. METRICS (§5.1): hit rate = cached prompt tokens / all prompt tokens. TTFT = arrival to first token. Per-turn latency = end-to-end latency of one agent invocation, prefill plus decode; this is the latency of one call, not the task. Throughput = completed agent turns/s. Median TTFT −14–52%; P99 TTFT −21–52% on three of the four workloads. LARGER MODEL (§5.4, Fig. 13): Qwen3-235B-A22B-FP8 with TP over 4× H200 (141 GB), compared with vanilla vLLM only because Continuum's fork does not support it. Hit rate +7–13 pp on all four workloads. On SWE-bench only, at 0.2–2.0 sessions/s: mean TTFT −33–54%, per-turn −26–36%, throughput 5.2 to 7.2 turns/s (+37%). The paper never gives the number of tasks or sessions per benchmark. Task quality is not measured. Code: §7 says it will be open-sourced with the benchmark suite; v1 has no link.

**mechanism and term:**

MECHANISM correct. It fingerprints each request's prompt prefix to identify the agent, learns an online first-order Markov chain of agent transitions, and turns BFS hop distance on the thresholded transition graph into a survival score. The eviction score multiplies survival, recency and block size. Between turns it sends a background warm-up request (max_tokens=1) for the predicted next agent's fixed prefix (the paper's 'anchor'), gated on predictability R ≥ R_min. Ablation (§5.3): predictive eviction alone gives +18–22 pp hit rate; prefetch alone adds ≤1 pp. TERMS: prefill smaller, because prompt tokens move from cache miss to cache hit; the target is the recurring fixed context (system prompt, tools, examples), which is 53–62% of prompt tokens (Fig. 2). Queueing smaller, because it sustains higher load and throughput. Decode is unchanged, though it is inside the per-turn metric. The N² growth is untouched: session history is not targeted. N, c_k, environment and success rate are unchanged. It is a self-hosted serving change; for an API user it would correspond to a larger cache-hit share, not something they can switch on. CAVEATS: (1) dossier E189's 'range covers both baselines' is not supported by the text. (2) Third-party check, different setting: UNISON (arXiv:2609.09643v1, Table II) re-ran CacheScout in its single-agent two-tier trace harness and got hit rates below LRU (e.g., 2.6% vs 20.7% on SWE/Qwen3-Coder-30B). The likely reason is that those single-agent traces have no recurring multi-agent prefixes.

**authors and venue:**

Authors and institutions match the arXiv page and PDF. UC Santa Cruz: Rui Zhang, Chaeeun Kim, Yi Zhong, Cheng-Wei Ching, Liting Hu. U Washington: Shaoting Feng. U Chicago: Kuntai Du, Yuhan Liu, Junchen Jiang. arXiv cs.AI, v1 16 Jul 2026, ID assigned Aug 2026. No venue: the ACM template placeholder ('Conference'17 … Washington, DC', DOI nnnnnnn) does not count. CREDIBILITY FLAG: criteria (i), (ii) and (iv) pass. Criterion (iii) is only partly met: the benchmarks are public and the model is stated, but no task count is given for any workload. references.md l.101 currently lists it as passing, so this needs Edwin's decision.

**formula:**

No speedup or cost formula. Eviction score, Eq. 9 (HTML): Score(b) = (p̃_surv(a_b)+δ)·(e^{−λ·age(b)}+δ)·|b|, with |b| = tokens cached in block b. The authors read it as the expected prefill work lost by evicting b. Supporting definitions: Eq. 8, p̃_surv(a) = 1 − min(E[a],E_max)/E_max, where E[a] is the BFS hop distance; Eq. 3, P_ij = (C_ij+ε)/Σ_k(C_ik+ε); Eq. 11, prefetch gate R ≥ R_min, where R (Eq. 2) is an entropy reduction. §5.1 defines hit rate = total_cached_tokens / total_prompt_tokens.

## 121. AsymCache

**read:** https://arxiv.org/abs/2606.02964 (v1 is the only version, 1 Jun 2026); PDF https://arxiv.org/pdf/2606.02964v1 read in full via pdftotext; HTML https://arxiv.org/html/2606.02964v1 used for the equations. Figure bar labels were decoded from garbled PDF glyphs. Wording is paraphrased; numbers and locations are exact.

**verdict:** corrected

**effect:**

The paper's own numbers are inconsistent. The abstract says TTFT is reduced 'by up to' 1.90–2.03× and TPOT by 1.62–1.71× over the latest baselines. The §8 Conclusion calls the same ranges 'average' improvements. The §1 Intro says up to 1.86× TTFT and up to 1.62× TPOT under realistic multi-session workloads. §6.2 is the only text that gives conditions: with Llama-3.1-70B, TTFT is reduced by up to 1.86× vs vLLM-LRU, 1.91× vs Max-Score and 1.86× vs Pensieve+MSA, and TPOT by up to 1.62×, 1.63× and 1.71× respectively. The 1.90–2.03× values appear only as TTFT bar labels in Fig. 11 (low-dispersion), apparently the Llama-3.1-8B + LooGLE panel; the figure text is garbled, so that panel attribution is uncertain. The dossier's E178 note calling '1.86×' a garbled fetch is wrong: 1.86× is in the paper's own text (§1, §6.2). Under queuing (LongBench, qps 0.04) with the chunk scheduler, §6.2 reports TTFT −60% vs vLLM-LRU and −70% vs Pensieve+MSA, TPOT −62%/−71%. SETUP (§6.1): 4× NVIDIA H20 96 GB (8B on 1 GPU, 70B TP on 4), Llama-3.1-8B/70B-Instruct, all systems using POD-Attention. LongBench and LooGLE are each limited to 300 requests, turned into multi-turn conversations. Average input/output lengths are 34.8K/2.6K and 24.4K/0.7K tokens. Outputs are pre-generated and replayed, so output length is fixed. Arrivals follow a Gamma process, with 5:1 (low) and 10:1 (high) inter- to intra-session dispersion. Metrics are average TTFT and TPOT. AGENT PART (§6.5, Fig. 15): BFCL v4 Web Search, with outputs pre-generated by GPT-5.1; Llama-3.1-8B and 70B; varying QPS; no task count. Vs vLLM-LRU alone, average job latency is only 0.4–4.2% lower, with hit rates nearly equal or worse. Built on top of Continuum, average job latency is 4.4–18.1% lower and P90 job latency 6.8–16.6% lower than Continuum alone. Quality: lossless by construction (bitwise-equivalent outputs), not measured.

**mechanism and term:**

MECHANISM correct. It is a lossless KV-block evictor that ranks blocks by f_B(t)·ΔT_B, i.e. reuse frequency × a position-dependent recompute cost from a fitted attention-latency model. A Multi-Segment Attention kernel handles non-contiguous cached segments, which makes suffix caching possible. An adaptive chunked-prefill scheduler completes the system. TERMS: prefill smaller, because it lowers the compute cost of the tokens that miss (it keeps later-position blocks, which cost more to recompute); it does not raise the hit rate, which §6.2 says is comparable or slightly lower than LRU. The TPOT gain is system-level: less prefill work competes in mixed prefill/decode batches. It is not a faster decode step. Queueing is reduced by the chunk scheduler under load. N, c_k, context growth, environment and success are unchanged. So 'prefill (TTFT) and decode (TPOT) smaller' is acceptable only if the decode effect is labelled as reduced batch contention. For agents the standalone gain is small (0.4–4.2% vs LRU); the 18.1% is incremental over Continuum.

**authors and venue:**

All authors are at Peking University: Chunan Shi, Yilei Chen, Yilin Chen, Xupeng Miao* and Bin Cui* (corresponding). 'Shi et al. (2026), PKU' is correct. The arXiv title is 'Multi-Segment Attention: Enabling Efficient KV-Cache Management for Faster Large Language Model Serving'; AsymCache is the system name. arXiv cs.AR, v1 1 Jun 2026, no venue. CREDIBILITY: passes the rule. Authors and university are verifiable, and LongBench and LooGLE are public with 300 requests each and the models stated. The BFCL agent part has no task count. It is not in references.md yet.

**formula:**

Eq. 3: block_id ← argmin_B E(B,t) = argmin_B f_B(t)·ΔT_B, the least-expected-recomputation-latency criterion. Eq. 4, two-segment latency model: T(l1,q1,l2,q2) = k1·l1 + k2·q1 + k3·l2 + k4·q2 + k5·q1(l1+q1) + k6·q2(l1+q1+l2+q2) + β, with l = cached segment lengths and q = query/recomputed segment lengths (Fig. 6). Eq. 5: ΔT_B = T(l1,q1+1,l2−1,q2) − T(l1,q1,l2,q2) = k5·(l1+2q1) + (k2−k3+k5). Eqs 6–7 approximate this as ΔT_B = 2k5·(l1+q1) + (k2−k3+k5). Eq. 9: f_B(t) = min(exp(−τ_B(t)/α), exp(−(τ_B(t)−τ0)/β)). The online eviction weight is λ·f_B(t)·ΔT_B. There is no end-to-end speedup formula.

## 122. AgentKVShift

**read:** https://arxiv.org/abs/2607.21604 (v1 is the only version; the abstract page dates v1 15 May 2026 despite the 2607 ID); PDF https://arxiv.org/pdf/2607.21604v1 read in full via pdftotext; HTML https://arxiv.org/html/2607.21604v1 used for the equations. Wording is paraphrased; numbers and locations are exact.

**verdict:** corrected

**effect:**

Abstract and §1 item 3 claim near-full-recompute quality while refreshing 10–30% of the cache, up to 5× less recompute than prior methods (which need 45–55% refresh), 2–3.5× prefill speedup over no KV reuse on a single A100, and within 1.5–6% relative F1 of full recompute at 10% refresh. The pairing in the dossier is wrong: 2–3.5× belongs to 10% refresh (r = 0.1), not to '10–30%'. QUALITY AT r = 0.1 (LoCoMo, §4.2.1, Table 1; Qwen2.5-3B, Qwen3-4B, Mistral-7B on A100): relative F1 drop 1.5–6%. Examples: AMem + Qwen2.5-3B 0.319 vs 0.339 (−5.9%); LiCoMemory 1.5% (Qwen2.5-3B), 2.5% (Qwen3-4B), 3.5% (Mistral-7B). QUALITY AT r = 0.3 (AMA-Bench-Recall, Table 2; Qwen3-32B on H200, GPT-4o judge): weighted F1 0.284 vs 0.296 (96.0%), judge accuracy 0.279 vs 0.287 (97.2%). SPEED comes from a separate prefill-throughput profiling, not from the benchmark runs (§4.4, Fig. 4 at 4,096 tokens/request × batch 16). At r = 0.1 it is about 3.3× (Qwen2.5-3B, A100-40GB) and about 3.6× (Qwen3-32B, H200); at r = 0.3 it is only about 1.5–1.6×. Table 3 (r = 0.1, 2K–16K tokens/request, batch 1–16) ranges from 0.94× (3B, 2,048 tokens, batch 1, i.e. slower than no reuse) to 4.13× (32B, 2,048 tokens, batch 16); 16,384 tokens at batch 16 runs out of memory. The baseline is full recompute (no KV reuse), not prefix caching. CacheBlend and ProphetKV reach similar or slightly higher speedups at the same r (Table 3). TASK COUNTS: LoCoMo = 10 long multi-session conversations with QA; the number of QA items and the AMA-Bench question count are not stated. HARDWARE: Table 3 says A100-40GB, Appendix A.1 says A100 80GB.

**mechanism and term:**

MECHANISM correct. Each retrieved memory unit has KV states computed out of context. The method recomputes a small probe/refresh fraction r, estimates the memory-level residual (mean of fresh minus reused KV over the probe set), and adds it to every reused token (mean-shift correction). It needs no training. TERMS: prefill smaller, because non-prefix, position-shifted memory chunks become reusable and fewer prompt tokens are recomputed. These are not provider prefix-cache hits, so the R^hit billing class does not apply. The reuse is approximate, so the success/quality term drops slightly: 1.5–6% relative F1 at r = 0.1, and about 3–4% at r = 0.3 on AMA-Bench-Recall. N, c_k, decode, context growth and environment are unchanged. The workload is agent-memory QA, not a web/GUI agent. It composes with 2- and 4-bit KV quantization (Tables 4 and 8).

**authors and venue:**

All authors are at UC San Diego (one affiliation line on p.1): Nilesh Prasad Pandey (corresponding), Jason Kong, Lanxiang Hu, Quanling Zhao, Yujie Zhao, Onat Gungor, Hao Zhang, Tajana Rosing. 'Pandey et al., UCSD' is correct. arXiv cs.AI. The page footer only says 'Preprint.'; no venue. No code link. CREDIBILITY: criteria (i), (ii) and (iv) pass. Criterion (iii) is borderline: the benchmarks are public and the models stated, but only LoCoMo's 10 conversations are counted, not the QA items or AMA-Bench questions. It is not in references.md yet.

**formula:**

There is no speedup formula; r (recompute ratio) is the refresh fraction. Correction: r_i^K = k_i* − k_i^reuse; μ̂_K = (1/b)·Σ_{j∈S} r_j^K over b probe tokens; k_i^corr = k_i^reuse + μ̂_K (V is handled the same way). Error bounds: ||y^reuse − y*|| ≤ U_reuse = B + N_n, with common bias B = C_K||μ_K|| + C_V||μ_V|| and N_n = (C_Kσ_K + C_Vσ_V)√(2 log(4n/δ)). ||y^corr − y*|| ≤ U_corr = N'_n + E_b, with E_b = (C_Kσ_K + C_Vσ_V)√(2 log(8/δ)/b). If B > E_b + (N'_n − N_n), then U_corr < U_reuse.

## 123. DualPath

**read:** https://arxiv.org/abs/2602.21548 (v1 25 Feb 2026, v2 26 Feb 2026). Latest PDF https://arxiv.org/pdf/2602.21548v2 read in full via pdftotext, diffed against v1; HTML https://arxiv.org/html/2602.21548v2 used for the formulas. Wording is paraphrased; numbers and locations are exact.

**verdict:** corrected

**effect:**

Abstract, §1 and §10: offline inference throughput up to 1.87× and online serving throughput 1.96× on average without violating the SLO. BASELINE — the recorded baseline is wrong. The baseline for these numbers is 'Basic', the authors' own unmodified in-house inference framework (§7.2). The paper says comparing with SGL(MC) (SGLang commit 19089aa + HiCache + Mooncake Store + 3FS + Mooncake Transfer Engine) is unfair because of implementation differences, so it reports gains only from Basic to DualPath. 'vs SGLang + HiCache + Mooncake + 3FS' is therefore wrong. OFFLINE (§7.3, Fig. 7): the metric is job completion time (JCT) for n agents rolled out at once (RL rollout). The 1.87× is DS 660B over Basic (default 2P4D). DS 27B reaches up to 1.78× but stays 1.09–1.85× slower than the zero-I/O Oracle. A P/D-ratio sweep on DS 27B averages 1.64× (up to 2.46×); an append-length sweep gives 1.82–1.99× (DS 660B, 64K context, 1,024 agents). ONLINE (§7.4, Fig. 10): Poisson agent arrivals, SLO TTFT ≤ 4 s and TPOT ≤ 50 ms. APS (agents per second) capacity is 1.67× (DS 27B) and 2.25× (DS 660B) over Basic; the '1.96× average' equals their mean (calc.: (1.67+2.25)/2 = 1.96). The online test ran only on DS 27B and DS 660B. TTST is comparable and TPOT unchanged. WORKLOAD (§7.2, Table 2): three trace sets from the authors' production agentic-RL training, 500 trajectories each. MaxLen is 32K/48K/64K, with an average of 60/106/157 turns, 608/474/429 appended tokens and 148/172/176 generated tokens per turn. The replay assumes zero inter-arrival time and zero tool-call latency (§8.2). TESTBED: servers with 8 NVIDIA Hopper GPUs, 8× 400 Gbps RDMA NICs and 1 storage NIC; 3FS without DRAM cache. MODELS: DeepSeek-V3.2 660B, an internal 27B scaled-down DS model, and Qwen2.5-32B. ABLATION (DS 660B, 64K context): JCT vs Basic falls 17.21% with layerwise prefill, 38.19% with dual-path loading added, 45.62% with scheduling added. SCALE: up to 1,152 GPUs (48P96D, 48K agents, JCT 3,201 s vs 3,167 s at 2P4D with 2K agents). v1 to v2: the abstract's 'production agentic workloads' became 'realistic agentic workloads'; the numbers did not change.

**mechanism and term:**

MECHANISM correct. In prefill/decode-disaggregated serving, the KV cache of hit tokens is loaded from distributed storage either straight into the prefill engine or through the decode engine's otherwise idle storage NIC, then sent over RDMA to the prefill engine. It adds traffic isolation centred on the compute NIC, a global scheduler that picks the path and balances prefill and decode engines, and layerwise prefill. TERMS AND A NOTATION GAP: it shortens the time to load cache-hit tokens (storage I/O). The Part 1 prefill definition ('reading the prompt tokens not in the cache') has no term for this. At the ≥95% hit rates of agent workloads (98.7% in their traces), the per-hit-token load time dominates. Part 1 therefore needs a hit-token load term (e.g. t_hit·R^hit) next to miss-token compute. DualPath shrinks that term and queueing (higher APS capacity under the SLO), and for self-hosted operators it cuts GPU machine-hours per job. Decode is unchanged. Tool waits are zero in the replay, so the environment term is absent. It is not a lever for API users.

**authors and venue:**

Authors and affiliations. PKU: Yongtong Wu, Yinmin Zhong, Rilin Huang, Xin Jin. Tsinghua: Shaoyuan Chen, Mingxing Zhang. DeepSeek-AI: Yixuan Tan, Wentao Zhang, Liyue Zhang, Shangyan Zhou, Yuxuan Liu, Shunfeng Zhou, Panpan Huang; Wu, Chen and Zhong also list DeepSeek-AI. arXiv cs.DC; v2 (26 Feb 2026) is the latest, while dossier E180 cites v1. No venue. CREDIBILITY FLAG: criteria (i), (ii) and (iv) pass. Criterion (iii) fails as written: the workload is internal production agentic-RL traces, not a public benchmark, and one of the three models is internal. Edwin must decide whether to keep it under a production-trace exception (as for the Copilot-telemetry paper) or list it as 'Not used'.

**formula:**

Bandwidth model (§4.2). Symbols: P, D = prefill and decode nodes; g = GPUs per node; B = compute NIC bandwidth; s×B = storage bandwidth per machine; M = memory bandwidth. Per-pair traffic is T_p = Bs/(Dg²) on the prefill-engine path and T_c = Bs/(Pg²) on the decode-engine path. Eqs 1–8 give Eq. 9: s/(g−s) ≤ P/D ≤ min{(g−2s)/s, (g−s)/(2s), (M/Bs−3)/2}. For g = 8, s = 1, M ≈ 500 GB/s and Bs ≈ 50 GB/s, the bottleneck-free range is 1/7 ≤ P/D ≤ 7/2. §3 defines the cache-compute ratio as KV bytes to load ÷ computation: about 22 GB/PFLOP for DeepSeek-V3.2 at 32.7K context with append 429, and 13–36 GB/PFLOP over 16K–64K (Table 1). §8.2: KV working set ≈ λ·T̄·total_len_avg/2, with λ = new trajectories/s and T̄ = mean JCT. There is no speedup formula.

## 124. PBKV

**read:** https://arxiv.org/abs/2605.06472 (v1 is the only version, 7 May 2026); PDF https://arxiv.org/pdf/2605.06472v1 read in full via pdftotext, including Appendix A Table 2; HTML https://arxiv.org/html/2605.06472v1 used for the equations. Wording is paraphrased; numbers and locations are exact.

**verdict:** confirmed

**effect:**

Abstract: up to 1.85× speedup over LRU on dynamic workflows, and up to 1.26× over KVFlow on the static workflow. §1 adds hit rate up to 2.55× over LRU, and 1.26× latency and 1.39× hit rate vs KVFlow on the static workflow. CONDITIONS (§6.1–6.2, Tables 1 and 2): the metric is end-to-end workflow latency (submission to final completion), mean of 10 runs, on 8× NVIDIA RTX A6000 48 GB (NVLink) with Qwen3-14B and Qwen3-32B (TP = 2). The LRU baseline is SGLang + HiCache (HICACHE_RATIO=1). Settings K = 3, γ = 0.7. The 1.85× is HoVer + LangChain (dynamic, iterative refinement loops) with Qwen3-32B at concurrency 72: 189.66 ± 4.70 s to 102.60 ± 7.28 s (calc. 1.85×). In the same run, per-agent TTFT falls from 16.65 to 8.22 s (2.03×) and hit rate rises from 27.09% to 69.10%. Other dynamic cells (calc.): HoVer with Qwen3-14B 1.83×; SWE-bench + AutoGen (retry loops, concurrency 24) 1.70× (32B) and 1.81× (14B). The 1.26× is FinanceBench + CrewAI (static, concurrency 48) with Qwen3-32B: KVFlow 101.57 s vs PBKV 80.53 s; with 14B it is 1.23× (calc.). The number of tasks or workflows per benchmark is not stated. The predictor is trained on 1K offline HoVer traces and reaches 0.94 top-1 at 1 step and 0.77 at 3 steps on a 500-trace test set (§4.1). Task quality is not reported (only predictor accuracy); prefix reuse is exact.

**mechanism and term:**

MECHANISM correct, with one precision: the predictor is not purely online. It is a GraphSAGE model over the global agent call graph, fused with the current request's prefill embedding and trained offline on historical traces (1K), unlike CacheScout's online Markov chain. Eviction is lifecycle-aware first: retired caches of finished workflows go first, ranked by how many workflows used them. Hierarchical eviction by Score(c) follows. Prefetch is conservative: it runs from host memory (HiCache) only during pure-decode batches, within idle GPU space and the PCIe budget. Ablation: most of the gain comes from lifecycle-aware plus hierarchical eviction; prefetch adds little. TERMS: prefill smaller, because shared workflow context moves from cache miss to cache hit across agents; queueing is also smaller under the high concurrency used. Decode is inside the end-to-end metric but unchanged. N, c_k, context growth, environment and success are unchanged.

**authors and venue:**

Wuhan University: Haoyu Zheng, Hao Wang, Yuanyuan Zhu, Xiao Yan, Jiawei Jiang* (corresponding). Dameng Database: Yongqiang Zhang. SJTU: Fangcheng Fu. Macquarie University: Jia Wu. HKUST: Binhang Yuan. The citation 'Wuhan U, SJTU, HKUST' omits Dameng Database (a company) and Macquarie University. arXiv cs.LG; the footer only says 'Preprint.'; no venue. The paper refers to 'supplementary code' but gives no public link. CREDIBILITY: criteria (i), (ii) and (iv) pass. Criterion (iii) is borderline: HoVer, SWE-bench and FinanceBench are public and the models are stated, but task and workflow counts are not. It is not in references.md yet.

**formula:**

Eq. 1, one-step reuse value: Value(c) = Σ_{w∈W^act(c)} A_w(c)·P_w. Eq. 2: Score(c) = Σ_{k=1}^{K} γ^{k−1} Σ_{w∈W^act(c)} s_w^(k)·A_w(c)·P_w^(k), where s_w^(k) = probability that workflow w survives to step k, A_w(c) = per-workflow agent-access indicator of cache node c, and P_w^(k) = predicted agent distribution at step k. Eq. 8 proves Score(c) equals the expected discounted number of misses on c. Prefetch budget: S = min{S_a, S_bw}, with S_bw = Bandwidth·StepDuration. Regret bound: R(B) ≤ (1−γ^K)/(2(1−γ))·Σ ε_c^γ. There is no end-to-end speedup formula; the speedup is a latency ratio.

## 125. UNISON

**read:** https://arxiv.org/abs/2609.09643 (v1 is the only version, 9 Sep 2026); PDF https://arxiv.org/pdf/2609.09643v1 read in full via pdftotext; HTML https://arxiv.org/html/2609.09643v1 read for Table II, Table V and the equations. Wording is paraphrased; numbers and locations are exact.

**verdict:** corrected

**effect:**

Abstract, §1 contributions and the conclusion claim the joint policy is the best non-oracle entry on hit rate and AMAT on every trace, with hit rate up 0.3% to 23.1%, AMAT down 22% to 51%, and TTFT down 58% to 89% on the long-horizon traces. What the body supports (§V-A, Table II): a trace-driven simulation of six traces, SWE-bench and GAIA × Qwen3-Coder-30B, Devstral-24B and Gemma4-E4B. The traces total 1,415 sessions and 33,596 turns; the authors generated them with an Ollama/litellm harness (Fig. 2). Runs cover six SRAM+HBM capacity envelopes. HR is the arithmetic mean over envelopes; AMAT/LRU and TTFT/LRU are geomean ratios vs LRU; TTFT is p50 at 4× load. HIT RATE is in percentage points, not percent: from +0.3 pp (GAIA/Devstral, 83.3 to 83.6) to +23.1 pp (SWE/Qwen3, 20.7 to 43.8). AMAT/LRU ranges from 0.78 (SWE/Devstral) to 0.49 (GAIA/Qwen3). TTFT: Table II gives only an aggregate TTFT/LRU of 0.64 (calc. −36%), slightly worse than the AGSERVE estimator (0.63); the Bélády oracle is 0.43. I could not find the per-trace values behind the 58–89% in any body text or table; they appear only in the abstract, contributions and conclusion. The text also says policy order stops affecting TTFT on the queue-bound SWE/Qwen3 and SWE/Devstral traces. Mean AMAT reduction over 36 comparisons is 34.8%; Bélády ratio 0.93. REAL-SERVER CHECK (§V-G, Table V): only SPEAR is tested (TIDE is not evaluated), in the vLLM v1 prefix cache, replaying the GAIA/Qwen3 trajectory at 32-way concurrency and temperature 0, against paired LRU. Cache-bound case (Qwen2.5-1.5B, 60K-token pool, tight gaps): +3.4 pp hit rate, mean TTFT −35%, p99 end-to-end −72%. Capacity-stressed case (1.5B, 30K pool, loose gaps): +2.5 pp, −6%, −4%. Native model (Qwen3-Coder-30B-AWQ, 60K pool, tight gaps): +1.6 pp, −1%, −3%. Not tabulated: GAIA/Devstral with a halved pool and tight schedule loses 6.6 pp hit rate; GAIA/Gemma4 (128 sessions) is noisy; SWE/Qwen3 is GPU-bound with no gain. INTERNAL INCONSISTENCIES: Fig. 2 says 1,451 sessions and Gemma4-27B; the text and Table II say 1,415 and Gemma4-E4B. Dossier E181's 'p50 at 4×4 load' should read 'p50 at 4× load', and its 'fetch summary 1–35%' should be replaced by the Table V values above.

**mechanism and term:**

MECHANISM correct. UNISON is an event-driven near-memory hardware scheduler, a control plane beside the SRAM/HBM KV tiers, that ranks live agent sessions. SPEAR evicts by a score built from an EMA of the return gap and a turn-indexed hazard, so a session waiting on a tool counts as likely to return. TIDE spends the observed tool-wait window as a DMA budget (gap × bandwidth) to move sessions between HBM and SRAM. TERMS: prefill smaller, because the growing session prefix stays cached across tool waits (miss to hit) and hits are served from the fast tier rather than the slow one. Overlap is introduced, because TIDE hides KV migration inside the environment wait. Like DualPath it acts on per-hit-token cost, which the Part 1 prefill definition does not show; its AMAT (Eq. 27) prices SRAM hits, HBM hits and misses separately. The headline numbers come from simulation plus synthesis of a 28-nm core (0.169 mm², 13.6 mW, 150 MHz, 64 sessions). Measured vLLM gains are small except in the small-model, cache-bound case. N, c_k, decode, context growth and success are unchanged.

**authors and venue:**

Fan He, Yan Li (corresponding; Member, IEEE) and Xiaoyang Zeng (Senior Member, IEEE), all at the State Key Laboratory of Integrated Chips and Systems, Fudan University; funded by NSFC grant 62574049. 'He, Li & Zeng (2026), Fudan' is correct. arXiv cs.AR; IEEE-journal template with no venue named. CREDIBILITY: criteria (i), (ii) and (iv) pass. Criterion (iii) passes formally: the task suites are public (SWE-bench, GAIA) and the session count and models are stated. However, the traces were generated by the authors and the headline numbers are simulated, so keep a 'simulation' label. It is not in references.md yet.

**formula:**

Eq. 7, SPEAR score: score(s) = S_max if session s has completed, else g_s/σ(t) + (1−σ(t))·P. Here g_s is an EMA of the return gap (Eq. 4: g_s ← (3·g_{s,k} + 7·g_s)/10), σ(t) = max(ε, 1 − h(min(t,50))) is a survival term from the turn-indexed hazard h(t) = d(t)/n(t) (Eqs 5–6), and P is a penalty. Eq. 8, TIDE budget: 𝓑 = Δ·B (tool-gap length × DMA bandwidth). Eq. 27: HR = (H_S + H_H)/R and AMAT = (1/R)·Σ_i ℓ_i·{t_s on an SRAM hit, t_h on an HBM hit, t_p on a miss}. Eq. 28: PreRED = 1 − Σ ℓ_i^comp / Σ ℓ_i. Eq. 29: BR = HR/HR*. Eq. 24: decision latency τ(N) = (N+5)/f_clk. There is no end-to-end speedup formula.

## 126. KVFlow

**read:** arXiv:2507.07400v1 (10 Jul 2025, the only arXiv version), PDF https://arxiv.org/pdf/2507.07400v1. NeurIPS 2025 camera-ready PDF https://proceedings.neurips.cc/paper_files/paper/2025/file/b7971d31a7d5eb0f1eed2f8f6f368195-Paper-Conference.pdf (20 pp. including the checklist). Poster page https://neurips.cc/virtual/2025/poster/119883. Crossref for DOI 10.52202/085713-4208.

**verdict:** corrected

**effect:**

Abstract (both versions): up to 1.83x for single workflows with large prompts and up to 2.19x with many concurrent workflows, both against SGLang with hierarchical radix cache (HiCache).

(a) Where the 1.83x comes from: v1 §4.1 only. Llama-3.1-8B on one A10G (24 GB, 2 GB/s PCIe), a synthetic 10-agent sequential workflow with random-token prompts, batch size 1, at 8192/32/32 fixed/dynamic/output tokens. It is 1.83x vs HiCache and 2.91x vs GPU-only SGLang. The metric is end-to-end workflow latency, averaged over 10 runs after cache warm-up.

(b) The NeurIPS camera-ready drops the A10G setup. Its §4.1 (p. 8) uses only Qwen2.5-32B on one H100, with branches=1 and branches=2, and adds vLLM as a baseline. It reports:
- 1.24x vs HiCache and 1.42x vs SGLang at 4096/32/32 (branches=1);
- average 1.30x at fixed=8192 and 1.22x at fixed=4096 (v1 said 1.48x and 1.28x);
- over HiCache on average, eviction alone gives 1.11x and eviction plus prefetch gives 1.29x.
In the camera-ready, 1.83x appears only in the abstract and the contributions list, not in the body. Reading the Fig. 4a bars at 8192/32/32 gives KVFlow about 1.4 and HiCache about 0.8 relative to SGLang (our approximate reading).

(c) The 2.19x, §4.2 in both versions:
- Setting: one H100, independent non-sharing sequential workflows, dynamic and output lengths fixed at 256.
- Configurations (camera-ready Fig. 5): Qwen2.5-32B at 512/20 and 1024/10; Llama-3.1-8B at 512/128 and 1024/64 (fixed tokens / concurrent workflows).
- KVFlow is at most 1.25x over GPU-only SGLang.
- HiCache falls to 0.57x of SGLang at 1024 fixed tokens with 64 concurrent workflows, and KVFlow is up to 2.19x over HiCache. calc.: 1.25 / 0.57 = 2.19, so the 2.19x is measured against a baseline that is itself slower than SGLang without a CPU cache.

(d) PEER, §4.2 'Realistic Workflow Simulation' (camera-ready Fig. 7; v1 Fig. 8):
- Setting: four-agent PEER workflows whose agent prompts an LLM generates from sampled roles and instructions; inputs from PEER's Financial QA dataset; prompts range from a few dozen to several hundred tokens.
- Result: up to 1.12x over SGLang and 1.08x over HiCache. The panels are labelled Qwen/16-Task and Llama/128-Task.
- Not stated: the number of questions; the hardware is not restated (the section's setting is one H100).

(e) No accuracy is measured; the authors argue the outputs are unchanged. So the recorded '1.08x on PEER' holds only vs HiCache; the figure vs SGLang is 1.12x.

**mechanism and term:**

Mechanism correct: workflow-aware eviction by steps-to-execution at the KV-node level, proactive CPU->GPU prefetch, and status-aware scheduling.

'Prefill smaller' is correct: the fixed-prompt prefix KV stays resident, so there are fewer recomputes and reloads.

'Overlap' holds only in a narrow sense: the prefetch overlaps the next agent's CPU->GPU KV transfer with the current agent's GPU compute. That hides reload time which would otherwise sit inside the next call's prefill. It is not the LLM-vs-environment overlap of the deck's overlap term. Suggested mapping: prefill (cache-miss recompute and reload time) goes down; queueing is touched secondarily, because the scheduler skips requests whose KV is still loading.

The gain applies only to self-hosted serving under GPU-memory pressure with repeated fixed prompts. It does not change API-billed tokens. The camera-ready's new §3.4 says that when future agents cannot be predicted, KVFlow falls back to SGLang's default behaviour.

**authors and venue:**

arXiv v1 (header 'Preprint. Under review.'): Pan, Patel, Hu (corresponding), Shen, Guan, Li, Qin, Wang, Ding; all UCSD except Yida Wang (AWS). Confirmed.

NeurIPS 2025 is confirmed:
- Main Conference poster (neurips.cc poster/119883);
- Advances in NeurIPS 38, pp. 139912-139931, DOI 10.52202/085713-4208 (Crossref).

The published author order is Pan, Patel, Shen, Hu, Guan, Li, Qin, Wang, Ding, which matches references.md l.87.

Passes as a conference paper. Under the 'published version cited' rule, numbers must come from the camera-ready, which no longer contains the A10G experiment behind 1.83x. This warrants a new D-entry.

**formula:**

No speedup or cost formula. The only rule is the step aggregation for steps-to-execution (§3.1, Fig. 3a in v1 / Fig. 2a in the camera-ready):
- a node that needs both inputs gets max(E1, E2) + 1;
- a node that needs either input gets min(E1, E2) + 1.
A shared cache node takes the minimum (least evictable) priority among its children.

## 127. Continuum (KV cache time-to-live)

**read:** arXiv:2511.02230v7 (8 Sep 2026), PDF https://arxiv.org/pdf/2511.02230v7 (14 pp.). The abs page was checked for the version history v1-v7. Fig. 12 and eq. 1-2 were checked on the rendered pages.

**verdict:** confirmed

**effect:**

(a) v7 §1: across three hardware and model setups, delay falls 1.12x-3.66x and throughput rises 1.10x-3.22x on multi-turn agentic workloads. The baseline is not named in that sentence.

Setup (§6.1): trace replay with Poisson arrivals of workloads collected by running GPT-5 (footnote 2):
- mini-swe-agent on SWE-Bench (100 traces analysed in §3.1);
- BFCL V4 Web Search (100 traces, scaled by 0.4 to fit Llama-3.1's 128k window);
- OpenHands on multi-SWE-bench (Go).
Replay models: Llama-3.1-8B, Llama-3.1-70B, Gemma-3-12B. Hardware: A100-SXM (Runpod), H100 (AWS, 'Company A'), B200 (on-prem). Baselines: vLLM 0.10.2 (chunk size 2048), LMCache 0.3.7 CPU offloading (100 GB on A100, 200 GB per GPU on B200/H100), Autellix PLAS (plus Autellix+ with LMCache), InferCept. Metric: average job delay / job completion time vs jobs per second; there is no quality metric in replay. §6.2 adds: with Llama-3.1-8B, up to 2x lower average response time vs vanilla vLLM.

(b) v7 abstract: average job completion time improves by over 8x. The abstract's model list now also names GLM-4.5 355B, which is used only in the RL micro-benchmark. §1: delay for real SWE-agent workloads on Company A's internal testbed falls by up to 8.18x (the footnote says Company A is an inference startup anonymised for double-blind review).

§6.2 real run:
- 500 SWE-Bench-Verified tasks on Company A's internal H100 testbed;
- Poisson job distributor, session-aware routing;
- baselines SGLang 0.5.5.post3 and NVIDIA Dynamo 0.7.0.post1 (1P1D);
- metrics: per-job finish time and pass rate.
The LLM used in this run is not named anywhere in v7. The paper also does not say which baseline or load point gives 8.18x. Our reading of Fig. 12 is that the largest gap is vs Dynamo at low jobs per second.

(c) Pass rate. The text says Continuum's pass rate is higher because baseline runs over 15 minutes are pre-empted and counted as failures. Fig. 12, read visually: about 7% Continuum, about 7% SGLang, about 3% Dynamo. So the pass rate is higher only vs Dynamo; vs SGLang it is at parity. D61 stands, with this refinement.

(d) Table 5, RL micro-benchmark: OpenHands with GLM-4.5-fp8 on Multi-SWE-bench, one 8xH100 node. Steps per minute: vLLM 93.4, ThunderAgent 114.8 (as reported by the ThunderAgent paper), Continuum 144.9 (1.55x vs vLLM, calc.). Table 4 gives a scheduler overhead of about 1-2.3 ms.

**mechanism and term:**

Mechanism correct. After a request that produces a tool call, Continuum pins its KV in GPU memory for a time-to-live tau. It chooses tau per tool from a cost-benefit model (eq. 1-2). It then schedules by program-level FCFS: pre-empted requests first, then pinned requests within their TTL, then program arrival order.

Both recorded terms are correct:
- prefill smaller: there is no re-prefill or CPU reload when the tool returns within tau;
- queueing smaller: this is explicit as OutofOrderCost, the per-turn queueing delay after eviction.

Continuum does not shorten the environment wait; it bridges it. Pinning has a cost: the pinned memory delays other requests (Cost(tau, r)), so the gains are loaded-server job-completion-time and throughput gains, and apply to self-hosted serving only. The 'higher pass rate' comes from the 15-minute timeout, not from model behaviour.

**authors and venue:**

Authors (v7): Hanchen Li, Runyuan He and Qiuyang Mang (equal contribution), Huanzhi Mao, Alvin Cheung, Joseph Gonzalez and Ion Stoica (UC Berkeley); Qizheng Zhang and Xiaokun Chen (Stanford); Hangrui Zhou and Huanchen Zhang (Tsinghua). So UC Berkeley, Stanford and Tsinghua is confirmed.

The v7 header is still the unfilled PVLDB template (PVLDB 20(1): XXX-XXX, 2027; doi:XX.XX/XXX.XX), so it stays a preprint. D153 stands, and doc2's 'journal per header' reading is out of date. The PDF spells the system 'Continnum' throughout; the arXiv title says 'Continuum'.

Credibility rule:
- The trace-replay range passes: public benchmarks, models named.
- The real-run '>8x' / '8.18x' fails condition (iii), because no model is stated for that run. Cite it only with that flag, or drop it.

**formula:**

§4.1-4.2, notation in Table 3 (calligraphic 𝒫, 𝒯, ℳ in the PDF):
- Cost(τ, r) = MemUsage(r)/ℳ × τ
- Benefit(r) = CacheMissCost(r) + OutofOrderCost(r)
- CacheMissCost(r) = MemUsage(r) × Prefill-Reload(r) / ℳ
- η = −Corr(k, N − k), where N = requests per program and k = requests already served
- OutofOrderCost(r) = 𝒯/ℳ × MemUsage(r) × η, where 𝒯 = average queueing delay
- τ* = argmax_τ 𝒫(τ, f) × Benefit(r) − Cost(τ, r)   (1)
- equivalently argmax_τ 𝒫(τ, f) × (𝒯·η + Prefill-Reload(r)) − τ   (2)
- 𝒫(τ, f) = (1/|S[f]|) · Σ_{t∈S[f]} 𝕀[t ≤ τ], the empirical CDF of past durations of tool f

Cold start uses T_default, derived assuming Exp(1) tool durations and η = 1; the threshold is K = 100. There is no closed-form speedup formula.

## 128. Pie

**read:** arXiv:2510.24051v1 (28 Oct 2025, the only version), PDF https://arxiv.org/pdf/2510.24051v1 (16 pp., the SOSP '25 camera-ready format with the ACM reference block). Venue checked on https://sigops.org/s/conferences/sosp/2025/accepted.html and on Crossref for DOI 10.1145/3731569.3764814.

**verdict:** confirmed

**effect:**

(a) §7.1 (pp. 9-10, Fig. 6): three agents written as inferlets:
- ReACT (web API interactions);
- CodeACT (code execution);
- Swarm (inter-agent messages).
Baselines: the same logic in vLLM and SGLang as Python client scripts, best-effort and with parallel client requests.
Model and workload: Llama 3 1B; 8 external I/Os per agent for ReACT and for CodeACT, 32 for Swarm.
Hardware: one NVIDIA L4 24 GB (GCP g2-standard-32), BF16; end-to-end latency measured from a remote Python client on a campus network.

Pie's absolute figures: 4.27 s, 3.18 s and 6.14 s latency and 29.94, 40.18 and 5.21 agents/s. On ReACT, Pie cuts latency by up to 15% and raises throughput by up to 30%. There is no gap below two external interactions, and the gap grows linearly with their number.

This is not a public benchmark: no task count and no success-rate metric.

(b) §1 and the abstract give 1.1x-2.4x lower latency and 1.3x-3.4x higher throughput on 'advanced tasks like Graph-of-Thought and agentic workflows'. That range mixes reasoning strategies with agents.

(c) §7.2, Fig. 7: a hypothetical API-calling agent with three stacked, application-specific optimisations:
- #1 retain the KV of frequently used API docs (export_kvpage);
- #2 call an API as soon as its signature appears in the generated tokens;
- #3 drop the KV of API specs used only once (mask_kvpage).
Result: 3.5x throughput over the Python workflow on vLLM, for 1-128 agents; the model is not restated. The text says 3.5x while the abstract says 3.4x, a minor inconsistency.

(d) Overhead: 3-12% latency on plain text completion.

**mechanism and term:**

Mechanism correct: programmable inferlets (Wasm) control KV pages, the generation loop and I/O inside the server.

The term mapping recorded for the ReAct 15% / 30% figure ('overlap (async tool I/O)') is wrong. §7.1 gives two causes:
- For 1B and 3B models, the main gain is removing the client<->server round trip per external interaction (tens of ms, against a few ms per token). That shrinks the per-interaction overhead in the environment act/observe path, plus the per-call request overhead.
- For 8B and larger, the main gain is keeping KV across external interactions, which avoids re-prefill (prefill smaller).

The overlap term appears only in the §7.2 Fig. 7 composite: #2 launches tool calls concurrently with generation. The same composite also shrinks prefill (#1) and removes tokens from later context (#3, context growth).

The core preserves logic; #3 changes the context, so its outputs are not automatically preserved.

**authors and venue:**

In Gim, Zhiyao Ma, Seung-seob Lee, Lin Zhong, all Yale University. Confirmed.

SOSP 2025 is confirmed:
- listed on the SOSP 2025 accepted-papers page;
- Crossref: Proceedings of the ACM SIGOPS 31st Symposium on Operating Systems Principles, pp. 415-430, DOI 10.1145/3731569.3764814, published 12 Oct 2025;
- the arXiv comment says 'SOSP 2025'.

Passes as a conference paper. Not yet in references.md; add it.

**formula:**

None. The paper gives no speedup or cost formula, only API code listings.

## 129. CacheBlend

**read:** arXiv:2405.16444v3 (3 Apr 2025; the camera-ready with the EuroSys '25 ACM reference block), PDF https://arxiv.org/pdf/2405.16444v3. Also checked: Crossref for DOI 10.1145/3689031.3696098, and the awards page https://2025.eurosys.org/awards.html.

**verdict:** confirmed

**effect:**

Abstract, §1 and §8: compared with full KV recompute, TTFT falls 2.2-3.3x and throughput rises 2.8-5x without compromising generation quality.

Setup (§7.1):
- Models: Mistral-7B, Yi-34B and Llama-70B, with 8-bit quantisation for the two larger models.
- Hardware: Runpod, 2x A40, 128 GB RAM, 1 TB NVMe SSD at a measured 4.8 GB/s; one GPU for Mistral and Yi, two for Llama-70B.
- Datasets: 2WikiMQA (200 cases), Musique (150), SAMSum (200), MultiNews (60); 512-token chunks, top-6 chunks per query.
- Quality metrics: F1 for QA, Rouge-L for summarisation.

TTFT (§7.2, Fig. 12): quality stays within 0.02 F1 / Rouge-L of full recompute and prefix caching, while TTFT falls 2.2-3.3x across all models and datasets.

Throughput (Fig. 14) is measured on 'Musique extended' and '2WikiMQA extended'. These are synthetic reuse sets: 1,500 original queries each plus 4,500 GPT-4-generated similar queries, with the first 1K queries skipped. There CacheBlend gives lower delay with 2.8-5x higher throughput than all baselines. The key takeaways put it at up to 5x vs full recompute and 3.3x vs prefix caching; the prefix-caching baseline was given an idealised zero loading delay.

Other results: vs full KV reuse, quality is 0.15-0.35 higher. At 5-18% recompute, the loss is at most 0.002 (Fig. 16, Yi-34B).

The setting is RAG, not agents.

**mechanism and term:**

Mechanism correct. CacheBlend reuses the precomputed KV of non-prefix chunks and recomputes about 15% of tokens (the high-KV-deviation tokens, filtered layer by layer) to restore cross-attention between chunks. The recompute of one layer is pipelined with loading the next layer's KV from storage.

'Prefill smaller' is correct.

Two additions:
- It is approximate, so the success rate can drop slightly: up to 0.02 F1 / Rouge-L in its RAG tests.
- The pipelining is an overlap of KV loading and recompute inside one call, not the deck's LLM-vs-environment overlap.

It has not been evaluated on agents. For agents it would apply to context chunks that are re-inserted or reordered.

**authors and venue:**

Authors: Jiayi Yao (UChicago / CUHK Shenzhen); Hanchen Li, Yuhan Liu, Siddhant Ray, Yihua Cheng, Kuntai Du and Junchen Jiang (UChicago); Qizheng Zhang (Stanford); Shan Lu (Microsoft Research / UChicago).

EuroSys '25 (Rotterdam, 30 Mar - 3 Apr 2025), pp. 94-109, DOI 10.1145/3689031.3696098 (Crossref). The EuroSys 2025 Best Paper (spring submissions) is confirmed on the official awards page.

Passes as a conference paper.

**formula:**

§5.1, footnotes 5-6:
- T_recompute(r%, LLM, L) = r% × Prefill(LLM, L), with Prefill(LLM, L) profiled offline;
- T_load(LLM, L, storage_device) = PerTokenKVSize(LLM) × L / Throughput(storage_device).
The loading controller picks the r% at which T_recompute equals T_load, then uses max(r%, r*%). Here r*% = 15%, the minimal recompute ratio with negligible quality drop (from Fig. 16).

## 130. KVCOMM

**read:** arXiv:2510.12872v2 (1 Nov 2025), PDF https://arxiv.org/pdf/2510.12872v2 (40 pp.). Cross-checked against v1 and the NeurIPS camera-ready https://papers.neurips.cc/paper_files/paper/2025/file/1a074a28c3a6f2056562d00649ae6416-Paper-Conference.pdf; Tables 1-3 are identical in all three. Poster page https://neurips.cc/virtual/2025/poster/115164.

**verdict:** confirmed

**effect:**

(a) Abstract: over 70% reuse rate; up to 7.8x speedup over the standard prefill pipeline, with TTFT from about 430 ms to about 55 ms, when each fully-connected agent receives 1K input tokens with 512 prefix tokens and 512 output tokens, five agents.

(b) Table 2 (§4.3): Llama-3.1-8B-Instruct, single H100, HuggingFace framework (not a serving engine).
- Original TTFT per agent: 125.8 / 192.4 / 258.3 / 330.9 / 428.6 ms.
- KVCOMM, agent 5: 17.5 ms prefill + 21.1 ms first-token decode + 16.2 ms other = 54.8 ms (calc.).
- Speedup ranges from 1.11x (agent 1) to 7.82x (agent 5).
A footnote says the original submission left out the first-token decode, and the final version fixes this.

Tables 2-3 name no dataset; the inputs are length-controlled. In Table 3 (3 agents), mean TTFT speedup runs from 2.24x (prefix 64, output 128) to 6.72x (1024/1024). The '~6.7x average prefill speed-up' in §1 is that longest setting.

(c) Quality, Table 1:
- Tasks: MMLU and GSM8K with Llama-3.1-8B-Instruct; HumanEval with Qwen-2.5-Coder-7B.
- Setup: 2-5 agents, max generation 512 tokens, γ=0.3, V=20.
- Baselines: no reuse ('Original') and CacheBlend reimplemented with top-20% recompute.

Reuse rate is defined as how often agents reuse all their KV caches, not a token share. It ranges 67.6-87.6%; the 5-agent MMLU cell (67.6%) is below the '>70%' headline.

Accuracy vs Original (calc.):
- GSM8K: −0.4 to −2.1 pp;
- HumanEval: −4.9 pp at 2 agents (86.3 -> 81.4), then −0.7, −1.3 and −1.9 pp;
- MMLU: equal or higher.

(d) The '<2.5% drop at 95% reuse' is a §1 claim backed by Table 6: 4-agent GSM8K at γ=0.5 gives 94.9% reuse and 80.0% accuracy vs 82.1% for Original (−2.1 pp, calc.). The 1,319 samples are GSM8K's test set, as §1 states.

**mechanism and term:**

Mechanism correct. KVCOMM is training-free. When the same text follows different prefixes in different agents, it estimates each agent's KV offset from an online pool of 'anchors' (deviations stored under earlier prefixes), and applies key rotation for positional alignment. The result is approximate.

'Prefill smaller' is correct: prefill of text shared across agents is skipped. The paper notes that total prefill across M fully-connected agents grows as O(M²), so it structurally targets a cross-agent analogue of context growth.

'Success rate slightly lower' is correct, but one HumanEval cell drops by up to 4.9 pp, more than the headline's 2.5%. The abstract's 'without quality degradation' is the authors' claim, with no non-inferiority test.

Scope: multi-agent text pipelines on HuggingFace; no serving engine and no GUI. A single-agent loop with an unchanged prefix gains nothing beyond ordinary prefix caching.

**authors and venue:**

Authors: Hancheng Ye, Mingyuan Ma, Qinsi Wang, Yuzhe Fu, Ming-Yu Chung, Yueqian Lin, Jianyi Zhang, Danyang Zhuo and Yiran Chen (Duke University); Zhengqi Gao (MIT); Zhijian Liu (NVIDIA). Correct 'Duke, MIT et al.' to 'Duke, MIT, NVIDIA'.

NeurIPS 2025 poster is confirmed:
- neurips.cc poster page;
- arXiv comment 'Accepted for publication in NeurIPS2025';
- camera-ready in the NeurIPS proceedings files.

Passes as a conference paper. Not yet in references.md; add it.

**formula:**

No speedup or cost formula. The paper states:
- §1: if each of M agents receives messages from all peers, total prefill complexity scales as O(M²);
- §3: prefilling N tokens costs O(N²d) multiply-adds per layer.

Offset approximation, Eq. 6: (k̂/v̂)^ϕ_(m,i) = (k/v)^ϕ_(m,i) + Σ_{ψ∈A_ϕ(m,i)} w_ϕ(m,i)→ψ · Δ(k/v)^ϕ_(m,ψ). Here w is the softmax of −‖h_ϕ(m,i) − h_ψ‖ over the anchor dimension. Eq. 7 is the same for prefix segments p(m,i).

## 131. DroidSpeak

**read:** NSDI '26 published PDF https://www.usenix.org/system/files/nsdi26-liu-yuhan.pdf (Proceedings of the 23rd USENIX NSDI, page footers 319-338). Presentation page https://www.usenix.org/conference/nsdi26/presentation/liu-yuhan. Compared with arXiv:2411.02820v4 (14 Jul 2025): the headline numbers are identical.

**verdict:** corrected

**effect:**

(a) Abstract: up to 4x throughput and about 3.1x faster prefill (TTFT), with negligible quality loss in F1, Rouge-L or code-similarity score, vs a baseline with no sharing across models.

(b) §5 takeaways and §5.2: across eight model pairs, each on three datasets, prefill delay falls 1.7-3.1x vs full prefill (average 2.1x) without compromising quality. Vs CacheBlend, quality is 5-33% higher (average 16%) at similar prefill latency.

Setup (§5.1):
- Models: fine-tuned variants of Mistral-7B, Mistral-24B, Llama-3.1-8B, Llama-3-8B, Phi-3.5-mini-instruct, Llama-3-70B and Llama-3.1-70B; the 70B models run 4-bit AWQ on one A100.
- Hardware: two Standard_ND96amsr_A100_v4 VMs with 8x A100 80 GB each, linked by 200 Gbps HDR InfiniBand. v4 says 'Azure'; the NSDI text keeps only the SKU name.
- Datasets (Appendix Table 2): HotpotQA 300, 2wikimQA 200, multifieldQA_en 200, multi_news 200, lcc 200, repobench-p 200.
- Recompute layers are profiled on 50 HotpotQA contexts to stay within a 5% quality drop.

(c) Throughput (§5.3):
- Setup: Kubernetes with vLLM Production Stack, 2 nodes x 8 A100, 8 replicas per model, Poisson arrivals, HotpotQA, four pairs shown, configurations within 1% accuracy drop.
- Result: under an SLO that avoids full prefill's queueing knee, DroidSpeak supports 2-4x higher throughput.

(d) Agentic case study (§5.4): a MetaGPT coder/tester pair. The coder uses the evolcode model and the tester the tool-8b model; they receive HumanEval problems at several rates (the problem count is not stated). TTFT improves 2.7x and E2E delay falls (Fig. 12). So the recorded 'not agent tasks' should be corrected: there is one agentic case study, with no agent success rate reported.

**mechanism and term:**

Mechanism correct. For two models fine-tuned from the same base (same architecture), the receiver reuses the sender's KV cache for a shared prefix. It recomputes only the 'critical' layer groups (often about 10% of layers), starting from the transferred E-cache (embeddings) of the transition layer, and pipelines the remote KV transfer with that recompute.

'Prefill smaller (approximate)' is correct. Two additions:
- The success-rate risk is bounded by construction: within 1-5% quality by configuration.
- The transfer/recompute pipelining is an overlap inside one call, not the LLM-vs-environment overlap.

It applies only when several fine-tuned variants read the same context, not to a single-model web agent.

**authors and venue:**

Authors: Yuhan Liu, Yuyang Huang, Jiayi Yao, Shaoting Feng, Zhuohan Gu, Kuntai Du, Hanchen Li, Yihua Cheng and Junchen Jiang (University of Chicago); Shan Lu, Madan Musuvathi and Esha Choukse (Microsoft). So 'UChicago, Microsoft' is confirmed.

NSDI 2026 (4-6 May 2026, Renton WA) is confirmed by the USENIX presentation page and the proceedings PDF.

The published title differs from arXiv v4: it is 'DroidSpeak: KV Cache Sharing Across Fine-tuned Model Variants'. Cite that title; the dossier row uses the arXiv title.

Passes as a conference paper. Not yet in references.md; add it.

**formula:**

None. §4.3, Fig. 9 gives only an illustrative unit-time timeline: TTFT is 47 when all layers load before recompute, 30 when only the reused layers load, and 17 with pipelining, about 2x better than the second case.

## 132. AgentServe

**read:** https://arxiv.org/pdf/2603.10342v1 (v1, 11 Mar 2026; the abs page lists only v1), read in full with pdftotext on 2026-09-28; abs page https://arxiv.org/abs/2603.10342

**verdict:** corrected

**effect:**

The paper's numbers are right, but the dossier's attribution is wrong: both 'up to' maxima are measured against llama.cpp, the weakest baseline. Against SGLang the gains are at most 1.3x.

Abstract: "up to 2.8x TTFT improvement and 2.7x TPOT improvement over state-of-the-art baselines across different settings".

§IV-B TTFT paragraph (p.9):
- vs SGLang: median TTFT 'typically 1.1-1.3x faster'; p95 'up to 1.3x'.
- vs vLLM: '1.5-1.8x'.
- vs llama.cpp: 'reaching up to 2.8x faster in heavy-load conditions'.

§IV-B TPOT paragraph:
- Median: 1.1-1.2x vs SGLang, 1.3-1.8x vs vLLM, more than 1.5x vs llama.cpp.
- p95: 'up to 1.3x compared with SGLang, nearly 2.0x compared with vLLM, and up to 2.7x compared with llama.cpp'.

Throughput (output tokens/s across sessions): 1.2-1.5x vs vLLM, 1.3-1.5x vs SGLang, up to 2.0-2.2x vs llama.cpp.

Conditions (§IV-A):
- One GPU: RTX A5000 24 GB or RTX 5090 32 GB.
- Models: Qwen2.5-3B, Qwen2.5-7B, LLaMA-3-8B.
- Workloads 'construct[ed] from ToolBench', in ReAct and Plan-and-Execute modes, with 3 to 6 concurrent agents.
- Baselines SGLang, vLLM and llama.cpp, all with prefix caching; AgentServe is built on llama.cpp.
- SLO thresholds are set per model-device pair by profiling times a constant.

What the paper does not report: the number of ToolBench tasks or sessions, any task-quality metric, and code.

**mechanism and term:**

The mechanism is described correctly. On one consumer GPU it:
- keeps cold prefills (long system prompts) and resume prefills (tool outputs appended to cached context) apart from short decodes;
- gives resume prefills a dynamic token budget;
- splits the GPU's SMs through ten pre-created CUDA Green Contexts, re-bound by TPOT signals.

The term mapping needs a correction. AgentServe does not reduce prefill or decode work. It reduces contention between them: head-of-line blocking that inflates TTFT (queueing plus prefill) and TPOT (decode slowed by interference) when 3 to 6 agents share one GPU. Correct mapping: queueing, made smaller under concurrency, with decode interference as the secondary effect. Its throughput gain would lower money only for self-hosted GPU time; it does not apply to API-hosted agents.

Credibility rule (slides/references.md):
- (i) and (ii) pass: all four authors are at the University of Sydney.
- (iv) passes: not a single-author report.
- (iii) fails as written: ToolBench is public and the models are named, but no task or session count is given.
- There is no venue: the 'JOURNAL OF LATEX CLASS FILES, VOL. 14' header is a template, not a venue.

Recommendation: 'Not used', or a qualitative mention only; Edwin to decide.

**authors and venue:**

Authors: Yuning Zhang, Yan Yan, Nan Yang, Dong Yuan. All four are at the School of Electrical and Computer Engineering, The University of Sydney (p.1 footnote); the corresponding author is D. Yuan.

Version and venue: arXiv 2603.10342v1 (cs.DC, 11 Mar 2026) is the only version. There is no venue; the IEEE LaTeX template header is not one.

**formula:**

No speedup or cost formula. The analysis bounds how much prefill throughput is kept under a decode SLO:
- Eq. (1): mu_P(R,t) = eta_t * mu_C(R) + (1 - eta_t) * mu_R(R). Effective prefill throughput with R SMs, mixing cold (C) and resume (R) prefill.
- Eq. (2): mu_D(R_pi(t)) >= r_min, with r_min = 1000/tau_max (decode-SLO feasibility).
- Eq. (3): pi* = argmax over pi in Pi_SLO of Sum_t mu_P(S - R_pi(t), t) * Delta_t.
- Theorem 1, Eq. (11): rho_t = W_A(t)/W_pi*(t) >= (1 - eps_bar) * mu_P(S - R_g* - delta, t) / mu_P(S - R_g*, t).

## 133. ThunderAgent

**read:** https://arxiv.org/pdf/2602.13692v3 (v3, 30 Jun 2026; the latest of v1-v3), read in full with pdftotext; pages 9 and 11 rendered to images to read the Fig. 4 and Fig. 6 labels. ICML page https://icml.cc/virtual/2026/poster/62040, read 2026-09-28.

**verdict:** corrected

**effect:**

The dossier's scope is wrong in two places:
- The 'at 96 parallel programs' scope holds only for panels (a), (b) and (e).
- The paper's own lower bound of 1.48x vs vLLM leaves out panel (f), which reads 1.24x.

§5.2 text: 'superior throughput at high concurrency levels (e.g., 96 parallel programs), achieving a 1.48-3.58x speedup over vLLM and 1.17-3.31x speedup over Continuum'.

Abstract: '1.5-3.6x throughput improvements in serving, 1.8-3.9x in RL rollout, and up to 4.2x disk memory savings'.

Metric (§5.1): 'steps per minute as our throughput metric, where one step includes a reasoning and acting period'.

Fig. 4 (p.9), label values at each panel's right-most point, given as ThunderAgent/vLLM and Continuum/vLLM:
- (a) SWEAgent-GLM4.6 at 96 programs: 2.65x and 1.52x.
- (b) OpenHands-GLM4.6 at 96: 3.58x and 1.08x.
- (c) ToolOrchestra(HLE)-Qwen3-8B at 48: 1.48x and 0.65x.
- (d) SWEAgent-Qwen3-235B at 192: 3.02x and 1.44x.
- (e) OpenHands-Qwen3-235B at 96: 2.43x and 1.22x.
- (f) ScienceAgent-GLM4.6 at 120: 1.24x and 1.06x.

From these labels (calc.):
- ThunderAgent/Continuum = 1.74, 3.31, 2.28, 2.10, 1.99, 1.17, so the text's 1.17-3.31x is correct.
- ThunderAgent/vLLM spans 1.24-3.58x.
- The caption instead says 'up to 2.43-3.56x' for panels (a, b, d, e).

Setup (§5.1):
- GLM-4.6 (355B) and Qwen-3 (235B), FP8, TP8 on 8xH100 nodes.
- ToolOrchestra uses 'Qwen3-8B with FP16 precision hosted on one RTX 5090', not H100.
- Benchmarks: SWE-bench Lite (OpenHands, mini-SWEAgent), HLE (ToolOrchestra), ScienceAgentBench (OpenHands).
- Docker environments run on a separate CPU cluster; ThunderAgent is built on vLLM with Delta-t = 5 and f(t) = 2^-t.

RL rollout, Table 2 (GLM-4.6, N = 144, two 8xH100 nodes, vs vLLM + SGLang Gateway):
- mini-SWEAgent: 375.4 to 671.8 steps/min (1.79x).
- OpenHands: 69.1 to 270.8 (3.92x).

Fig. 6a (OpenHands rollouts):
- Average end-to-end latency 58 s to 12 s.
- Environment time 4.8 s to 0.3 s.
- Disk 3.3 TB to 0.8 TB (4.1x, calc.; the paper says 4.2x).
- The tool-resource policy 'contributes approximately 10% to the latency improvement'.

§3.1 / Fig. 1b: thrashing raises end-to-end latency 'by up to 7.14x' (GLM-4.6, 8xH100).

Not reported: the number of tasks and any success or quality metric.

**mechanism and term:**

The mechanism is described correctly: the LLM program is the scheduling unit, with a program-aware waiting queue (pause/restore, shortest-first eviction, decay f(t)) and a tool-resource manager.

Term mapping, completed:
- Queueing: the global program queue under memory pressure.
- Prefill: it avoids re-prefilling evicted KV after tool waits (Cost_recompute), which on self-hosted serving keeps a step's context in the cache-hit class.
- Environment wait, via an overlap the dossier missed: asynchronous environment preparation restores the sandbox before GPU memory is allocated, so the overlap saving applies to environment set-up (4.8 s to 0.3 s in Fig. 6a).
- Environment machine resources: 4.2x less disk, plus network ports.

The headline metric is throughput in steps/min, so the main effect is on money for self-hosted GPUs (machine-hours per step), not on single-task time. Per-step latency appears only in App. E and Fig. 6a. Success rate is not reported. Credibility passes (ICML 2026).

**authors and venue:**

arXiv v3 authors and affiliations:
- Georgia Tech: Hao Kang, Tushar Krishna.
- Individual Researcher: Ziyang Li. This affiliation is missing from references.md.
- UIUC: Weili Xu, Yinfang Chen.
- CMU: Xinyu Yang, Beidi Chen.
- Together AI: Junxiong Wang, Chenfeng Xu, Simran Arora.

Venue: the ICML page is 'ICML Poster ThunderAgent: A Fast, Simple, and Program-Aware Agentic Inference System' (creditText ICML 2026; datePublished 2026-05-05). Its author order is Kang, Li, Yang, Xu, which matches references.md. Venue confirmed.

**formula:**

All of these are already in the formula scan:
- §4.2 Eq. (2): Cost_x = integral from 0 to t_x of M_x(t) dt. This is the space-time product, with M the KV token count; the paper attributes it to Belady 1966, which was not opened.
- Eq. (3): Cost_total ≈ Cost_decode + Cost_prefill + Cost_recompute + Cost_unused + Cost_caching.
- Lemma 4.1, Eq. (8): Cost_recompute = integral of c_i(t) dt, proportional to c_i^2.
- Definition 4.1: choose the eviction set S to minimise Sum over S of c_i^2, subject to Sum over S of c_i >= Delta-C.

## 134. ConServe (§3.6 group row: ConServe / Workflow-Aware Prefix-State Scheduling / Stateful Inference / AAFLOW+ / SmoothAgent)

**read:** https://arxiv.org/pdf/2606.01839v1 (v1, 1 Jun 2026; the only version), read in full with pdftotext on 2026-09-28; abs page

**verdict:** corrected

**effect:**

The dossier records this row as 'Not verified'; it is now verified. The title is 'Observation, Not Prediction: Conversation-Level Disaggregated Scheduling for Agentic Serving'; the system is called ConServe.

Abstract: 'Against a per-turn prediction baseline, ConServe reduces p95 time-to-first-effective-token ... by 51.08% and improves energy efficiency by 7.51% while preserving last-turn TBT and SLOs'. Heterogeneous GPU tiers 'adds a further 22.75% in energy efficiency'.

§5.2: 'reducing up to 19.17% and +51.08% on geometric mean and p95 TTFET' vs AMPD.

Conditions (§5.1):
- Traces 'generated from SWE-bench bm25 13K with swe-agent, using Qwen3-Coder-30B-A3B-Instruct as the trace-generation model'.
- Replayed on 4x NVIDIA A40 serving Qwen3-0.6B (bf16), with 1 prefiller and 3 decoders.
- Heterogeneity is simulated by power-capping 3 GPUs to 2/3 of TDP.
- vLLM with LMCache; Poisson arrivals of 0.5-1.5 conversations/s, plus a synthetic 1.634 conversations/s at saturation.
- Baselines: Collocated, Full Disaggregation, and AMPD (He et al., 2026). AMPD is re-implemented 'at our best effort', with simulated KV-transfer latency and a fixed injected 10% wrong-prediction rate.
- The evaluation runs 'a finite trace subset'; the count is not given.

No task-quality metric (it is a serving system). TTFET is the latency to the conversation's first user-visible output.

**mechanism and term:**

The dossier's 'PD-disaggregated pinning' is right. Only the turn-1 prefill goes to a high-throughput prefiller; the KV cache is transferred once; the conversation is then pinned to one decoder, so prefills from turn 2 on stay local cache hits.

Terms:
- Queueing: the prefiller's load is bounded by conversation arrivals.
- Prefill: the first-turn placement, and later turns kept in the hit class.
- Money for self-hosted GPUs: energy efficiency.
- Structure: the scheduling unit moves from turn to conversation.

This is self-hosted serving only.

Credibility:
- (i), (ii) and (iv) pass: University of Chicago, five authors.
- (iii) is weak: SWE-bench is public and the models are named, but the task or conversation count is not stated. The served model is 0.6B, and the baseline is a reimplementation with an injected error rate.

Recommendation: qualitative mention only, unless Edwin accepts it without a task count.

**authors and venue:**

Authors: Jianru Ding, Ryien Hosseini, Pouya Mahdi Gholami, Mingyuan Xiang, Henry Hoffmann — University of Chicago (p.1). No venue.

**formula:**

- Fig. 2, fitted uncached prefill latency: '1.47 ns·L^2 + 10.5 µs·L + 13.8 ms (R^2=1.000)'. The median prefill with a prefix-cache hit is 27 ms.
- KV transfer: 'linear 0.98 µs/tok + 5.3 ms'.
- §4, Eq. (1): N·T_d >= R·L_d (throughput).
- Eq. (2): N·B >= R·W (memory).
- The prefiller saturates at R* = T_p/L_in.

## 135. Workflow-Aware Prefix-State Scheduling = TOPAS (§3.6 group row)

**read:** https://arxiv.org/pdf/2608.25523v1 (v1, 26 Aug 2026; the only version; arXiv comment '8 pages'), read in full with pdftotext on 2026-09-28

**verdict:** corrected

**effect:**

The dossier records this row as 'Not verified'; it is now verified. The full title is 'TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving'.

Abstract: 'Compared with the best-performing baseline for each workload and metric, TOPAS reduces the mean/p99 JCT by up to 39.8%/49.4% on the synthetic workloads, while lowering mean JCT by 9.8% on MetaGPT-SOP and mean/p99 JCT by 22.0%/26.6% on MetaGPT-TL.'

§V-B results, mean/p99 JCT reductions:
- Chain-3: 27.5% / 31.7%.
- DAG-4: 39.8% / 49.4%.
- DAG-10-Wide: 27.7% / 30.8%.
- MetaGPT-SOP vs SPF: 9.8% / 4.5%, with request throughput +6.7%.
- MetaGPT-TL vs SPF (mean) and Parrot-FCFS (p99): 22.0% / 26.6%.

Conditions (§V-A):
- SGLang v0.5.3 on a single NVIDIA A100 80GB, serving Qwen2.5-32B-Instruct.
- Poisson task arrivals.
- Synthetic DAGs use 'fixed-length user queries constructed for the evaluation'.
- The MetaGPT workloads use 'real prompts sampled from the MetaGPT SoftwareDev dataset'.
- Baselines: FCFS, LPM, Parrot-FCFS, Autellix-LAS, SPF/SRPT.
- Each metric is averaged over the reported operating points.
- Scheduler overhead: 1.9 ms per decision, 0.31% of wall time.

Not reported: the task count and any quality metric.

**mechanism and term:**

The dossier's 'prefix-state scheduling' is right. TOPAS decides jointly which agent system-prompt prefixes stay resident in GPU KV and which requests are admitted, under one KV budget.

Terms:
- Queueing (admission order).
- Prefill: whether a resident prefix is a hit, or has to be moved or recomputed.

This applies to multi-agent DAG workflows on self-hosted serving, not to single-agent GUI work.

Credibility:
- (i), (ii) and (iv) pass.
- (iii) fails as written: the synthetic DAGs are not a public benchmark, and no task count is given for the MetaGPT SoftwareDev prompts.

Recommendation: qualitative mention only.

**authors and venue:**

Authors: Hongqiu Ni, Han Tian, Guopeng Li, Haisheng Tan (University of Science and Technology of China); Chi Zhang (Hefei University of Technology). No venue.

**formula:**

§IV Eq. (3): U_base(S'|S_t) = J_admit - J_move - J_redo - J_revoke. All terms are in seconds: J_admit is the reduction in the admitted requests' task-level remaining paths, and the other terms charge prefix movement and preemption.

## 136. Stateful Inference for Low-Latency Multi-Agent Tool Calling (§3.6 group row)

**read:** https://arxiv.org/pdf/2605.26289v1 (v1, 25 May 2026; the only version), read with pdftotext on 2026-09-28

**verdict:** not found

**effect:**

Abstract: the reference implementation is '2.1x faster per turn on a 6-turn agentic workflow and 4.2x on the median turn of a 35-turn one, halving end-to-end wall time', against vLLM and SGLang 'on novel, fully-generated workloads'.

No public benchmark is used. It is recorded here only so that nobody re-adds the paper.

**mechanism and term:**

Mechanism: a persistent per-session KV cache that ingests only the new tokens each turn (the paper's O(n_t) to O(Delta_t)), a radix prefix cache across agents, a response cache, and prompt-lookup speculative decoding.

Terms: prefill (delta-only) and decode (speculative).

Credibility: it fails (iv), being a single-author industry preprint (Victor Norgren, LayerScale, Inc.), and it fails (iii), with self-generated workloads and no public benchmark. Treat it as 'Not used': not in evidence tables, slides or reference list.

**authors and venue:**

Single author: Victor Norgren, LayerScale, Inc. (layerscale.ai). No venue.

**formula:**

- Eq. (3): C_standard = Sum_t O(n_t) = O(T·n_bar).
- Eq. (4): C_cached = O(n_1) + Sum_t O(Delta_t) = O(n_1 + T·Delta_bar).

Here n_t is the tokens in the prompt at turn t and Delta_t the new tokens at turn t. This is the paper's own per-turn prefill cost model.

## 137. AAFLOW+ (§3.6 group row)

**read:** https://arxiv.org/pdf/2607.10987v1 (v1, 13 Jul 2026; the only version; arXiv comment '21 pages, 10 Figures, 12 Tables'), read in full with pdftotext on 2026-09-28

**verdict:** corrected

**effect:**

The dossier's 7.60x is correct for Mistral-7B, but every number here is an analytical extrapolation, not a measurement.

Abstract: 'reduces TTFT by up to 50.2x, achieves up to 7.63x reduced multi-agent compute cost at 16-agent scale, reduces KV memory by 1.72-6.10x, and increases throughput by more than 7.74x, based on an analytical cost model parameterized by empirical hardware microbenchmarks.'

§6.7: 'we extrapolate aggregate multi-agent compute time using an analytical cost model parameterized by empirical microbenchmarks'.

Table 3 (HF backend, 16 agents):
- Mistral: AAFLOW+ 224.399 s vs SGLang prefix 1704.865 s, i.e. 7.60x (the dossier's number).
- Llama3: 220.052 s vs 1679.815 s, i.e. 7.63x (the abstract's number).

§6: workloads are 'deterministic synthetic prompts and natural questions datasets and a trace-driven analytical model'.

Models are Mistral-7B and Llama-3-8B. Hardware is 4-16 nodes with A100 80/40 GB GPUs and InfiniBand. KV memory (Table 4): 1.72x smaller than vLLM local prefix and up to 6.10x smaller than DistServe-style.

**mechanism and term:**

The dossier's 'zero-copy distributed KV' is right. The KV cache becomes a first-class distributed object (materialize, transfer, fork, compose, evict), so agents that share a context receive KV state instead of text and do not re-prefill it.

Terms: prefill across agents. In multi-agent fan-out this is a structural change: k prefills become 1 prefill plus k transfers. It does not apply to single-agent GUI work.

Credibility:
- (i), (ii) and (iv) pass: University of Virginia, Rutgers, PPPL.
- (iii) fails for the numbers, which are analytical extrapolations on synthetic prompts and Natural Questions, not end-to-end measurements on an agent benchmark.
- The 'PVLDB Reference Format ... PVLDB, 14(1)' block is the VLDB template, not a venue.

Recommendation: qualitative mention only; label any number as modeled.

**authors and venue:**

University of Virginia (Biocomplexity Institute): Arup Kumar Sarker, Alexander James Halpern, Mills Staylor, Gregor von Laszewski, Geoffrey Fox, Yue Cheng. Rutgers University and Princeton Plasma Physics Laboratory: Aymen Alsaadi, Shantenu Jha. No venue; the PVLDB 14(1) line is template text. Code: github.com/arupcsedu/AAFLOW.

**formula:**

- §6.2: TTFT = T_prefill + T_queue + Omega.
- TTFT_text is proportional to L; TTFT_state ≈ T_transfer + T_resume.
- For k branches: T_state^k ≈ T_prefill + k·T_decode.

## 138. SmoothAgent (§3.6 group row)

**read:** https://arxiv.org/pdf/2607.00151v1 (v1, 30 Jun 2026; the only version), read with pdftotext on 2026-09-28

**verdict:** corrected

**effect:**

This is not a measurement study. The title is 'SmoothAgent: Efficient Long-Horizon LLM-Based Agent Serving with Lookahead Context Engineering'.

Abstract: 'our approach effectively eliminates transformation overhead and reduces TTFT by up to 11.9x.'

§6.2 results:
- Summarization gives the largest gain, 'up to 11.9x TTFT improvement'.
- PD co-located: tail TTFT at transformation points falls by 62.0% on average (Qwen3-8B) and 61.5% (Qwen3-32B).
- PD disaggregated (4 prefill + 4 decode H100, Qwen3-8B, up to 64 concurrent agents): average reduction of 64.5%.

Conditions (§6.1):
- H100 80GB; Qwen3-8B on 1 H100, Qwen3-32B on 4 H100 (TP=4); 1-16 concurrent agents at fixed concurrency; SGLang backend.
- Workload: each agent runs a 28-step code-analysis task that reads the MiniAgent codebase through shell commands, adding about 600-650 tokens per step.
- Baseline 'sync': the same strategies (offloading, keep-recent-K, summarization, sub-agent isolation) run on the critical path.

No public benchmark and no task-quality metric.

**mechanism and term:**

Corrected. SmoothAgent is a system: a lookahead programming model plus a lookahead-aware scheduler. Context transformations (offload, trim, summarize, isolate) run asynchronously ahead of time, and the transformed KV is committed without blocking.

Terms:
- Overlap saving introduced: the transformation and its re-prefill, including the summarization model call, run concurrently with ongoing turns.
- Prefill: the re-prefill spike at the transformation point leaves the critical path.

The context-growth term itself is reduced by the context-engineering strategy, not by SmoothAgent; SmoothAgent hides that strategy's cost.

Credibility:
- (i), (ii) and (iv) pass: UC San Diego, eight authors.
- (iii) fails: the workload is self-built (28-step MiniAgent code analysis), not a public benchmark.

Recommendation: qualitative mention only.

**authors and venue:**

Authors: Zaifeng Pan, Qianxu Wang, Zhengding Hu, Chang Chen, Yue Guan, Yanbo Zhou, Steven Swanson, Yufei Ding — University of California, San Diego. The VLDB copyright text on p.1 is a template, not a venue. Code: github.com/PanZaifeng/SmoothAgent.

**formula:**

- §3.1: segment-decomposability, T(C) = T(S_1) || T(S_2) || ... || T(S_n), where || is concatenation.
- §5, Eq. (1): EstBatchLatency(B) = T_GEMM(M) + alpha_d · Sum over j in B_decode of L_j + alpha_p · Sum over j in B_prefill of A_j.

## 139. Provider prompt caching and cache prices (vendor docs)

**read:** All read 2026-09-28:
- Anthropic prompt caching (.md): https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md
- Anthropic fast mode: https://platform.claude.com/docs/en/build-with-claude/fast-mode.md
- Anthropic mid-conversation system messages: https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages.md
- OpenAI Prompt Caching 201 cookbook: https://developers.openai.com/cookbook/examples/prompt_caching_201 (the page shows Feb 18, 2026)
- OpenAI API prompt-caching guide: https://developers.openai.com/api/docs/guides/prompt-caching
- OpenAI pricing: https://developers.openai.com/api/docs/pricing
- DeepSeek pricing: https://api-docs.deepseek.com/quick_start/pricing
- Google Gemini pricing: https://ai.google.dev/gemini-api/docs/pricing
- xAI Grok 4.7: https://docs.x.ai/developers/models/grok-4.7

**verdict:** corrected

**effect:**

The Anthropic figures are confirmed. OpenAI is corrected: the cookbook's 'no additional fees' is outdated for GPT-5.6 and later, which now carry a 1.25x cache-write charge.

Anthropic:
- 'Cache read tokens are 0.1 times the base input tokens price (see the table footnote for per-model exceptions)'. Footnotes: 0.05x on Opus 5.5 ($4 input, $0.20 cache hit); 0.025x on Fable 5.1 and Mythos 5.1.
- Cache writes are 1.25x (5-minute) and 2x (1-hour).
- 'By default, the cache has a 5-minute lifetime. The cache is refreshed for no additional cost each time the cached content is used.'
- Invalidation table: changing tool definitions invalidates the entire cache. Switching speed (fast vs standard) invalidates the system and message caches; the tools cache stays valid. Changing tool_choice or images invalidates messages. Changing thinking or effort settings always invalidates messages, plus tools/system on some models.
- Mid-conversation system messages keep the cache on Fable 5.1, Mythos 5.1, Fable 5, Mythos 5, Opus 5.5, Opus 4.8 and Opus 5, but not Sonnet 5.
- Tool changes (tool_addition / tool_removal) now use the 'inline-tools-2026-09-15' beta header on the Claude API. 'The mid-conversation-tool-changes-2026-07-01 header works for changes that name a tool by reference' on the Claude API, Bedrock and Google Cloud.
- Fast mode: 'up to 2.5x higher output tokens per second' on Opus 5.5, Opus 5 and Opus 4.8; its benefit is 'not time to first token'; caching multipliers apply on top.

OpenAI cookbook: 'Prompt Caching can reduce time-to-first-token latency by up to 80% and input token costs by up to 90%'; 'has no additional fees'. The same page reports the author's own test: 2,300 runs, 1,024-token prompts 7% faster, 150k+ tokens 67% faster TTFT; the model is not stated.

OpenAI API guide (current):
- 'For GPT-5.6 and later, cache writes cost 1.25x the standard, uncached input-token rate'; reads cost 0.1x.
- Lifetime: 'At least 30 minutes after the latest write or reuse'; ttl is '30m' or '24h'.
- Earlier models: 'No additional cache-write charge', with a model-dependent read discount (cookbook table: gpt-4o 50%, gpt-4.1 75%, gpt-5.x 90%).

OpenAI pricing, per 1M tokens (input / cached input / cache write / output):
- gpt-6-sol: $2.00 / $0.20 / $2.50 / $10.00.
- gpt-6-luna: $0.10 / $0.01 / $0.125 / $0.50.
- gpt-6-astra: $10 / $1.00 / $12.50 / $50.

DeepSeek, per 1M tokens:
- V4.1-Flash: cache hit $0.006 peak / $0.003 off-peak; miss $0.3 / $0.15; output $1.2 / $0.6. Hit/miss is 0.02x (calc.).
- V4-Pro: hit $0.044 vs miss $1.32 at peak, 0.033x (calc.).
- 'Off-peak rates are half of the peak rates'; there is no write or storage charge on the page.

Google Gemini 3.8 Flash: input $0.75 and context caching $0.075 (0.1x), plus '$0.50 / 1,000,000 tokens per hour (storage price)' through 31 Dec 2026. From 1 Jan 2027: $1.50 / $0.15 / $1.00.

xAI Grok 4.7: input $2.00, cached $0.50 (0.25x), output $6.00. No write price is shown.

**mechanism and term:**

The mechanism is described correctly: the provider keeps an exact-prefix KV cache.

Terms:
- Money by billing class: a hit is cheaper; a write or store is an extra class. Write/store charges: Anthropic 1.25x (5-min) / 2x (1-h) write; OpenAI GPT-5.6+ 1.25x write; Google per-token-hour storage. DeepSeek and xAI show no write charge.
- Prefill time on the cached part (TTFT).

It changes the price and time per token, not the ~N^2 token volume: the constant, not the shape.

Keep-alive rules are part of the term: Anthropic refreshes the cache free on each use; OpenAI GPT-5.6+ keeps it at least 30 minutes.

Anthropic's mid-conversation system messages and tool_addition/tool_removal keep calls in the hit class; that is a structural fix against cache breaks. Switching fast mode, thinking or effort breaks the message cache, which interacts with per-step effort routing such as Ares.

OpenAI's 80%/90% are vendor-stated maxima; label them as such.

**authors and venue:**

Vendor primary docs; prices are citable. The OpenAI cookbook's TTFT test is vendor-run, with the model unstated.

**formula:**

OpenAI guide: 'Writing a prefix once and fully reusing it once costs 1.35x its ordinary input cost, compared with 2x ... one write and nine full reads cost 2.15x, compared with 10x without caching.' The closed form, 1.25 + 0.1(n-1) vs n in units of uncached input, is calc.

DeepSeek: 'The expense = number of tokens x price.'

Anthropic: mixed-TTL billing positions A/B/C, with 1-hour writes charged for (B - A) and 5-minute writes for (C - B).

Google: storage is billed per token-hour, a time-based unit unlike the per-token hit/miss prices.

## 140. TraceLab dashboard counterfactual

**read:** - Dashboard https://tracelab.cs.washington.edu (main page) and the detail page https://tracelab.cs.washington.edu/exp/prefix_cache/human_idle_cache_counterfactual, both read 2026-09-28.
- arXiv PDFs https://arxiv.org/pdf/2606.30560v2 (30 Jun 2026) and v1 (29 Jun 2026), §7.3-7.6, Tables 12-13.

**verdict:** corrected

**effect:**

The dashboard numbers are confirmed and unchanged since 2026-09-27. The provenance recorded in E187 is wrong: the same counterfactual is in the paper, with a different number.

Dashboard main page: 'Append reduction 2.70B | Cost reduction $14,333 | Final cost saved 15.8%', 'Upper-bound savings if user-initiated steps kept their prefix cache.'

Dashboard data snapshot: 52 users, 8,058 sessions, 665,453 agent steps, 743,819 tool calls, Sep 23 2025 - Jul 24 2026. A banner reads 'SyFI Coding Trace v2 is live'.

Detail page, Table 1:
- 71,364 user-initiated steps with a predecessor (Claude 38,543; Codex 32,821).
- Observed append 5.01B, falling to 2.30B with retained cache: -2.70B (54.0%).
- Observed total cost $90,888, falling to $76,556: -$14,333 (15.8%) 'over priced rounds'.
- Claude -$12,427 (20.3%); Codex -$1,906 (6.4%).
- Prices: 'pricing.json prices as of 2026-07'.
- 'This is an upper-bound savings estimate, not an observed cache metric.'

Scope of the 15.8%: the 5.01B equals the snapshot's total append across all steps. The 15.8% is therefore a share of the whole priced bill; only the user-initiated steps change.

The same analysis is in the paper, v1 and v2, §7.5 Table 13:
- 33,960 user steps with a predecessor.
- Append 2.34B to 1.26B: -1.07B (45.9%).
- Cost $40,431 to $35,242: -$5,189 (12.8%) 'over priced rounds' at 'current list prices'.
- Claude 16.2%; Codex 8.5%.

E187's 'not in the paper' is therefore wrong: the paper's versioned figure is 12.8%, and the dashboard's 15.8% applies the same method to a larger, later dataset.

**mechanism and term:**

The mechanism is described correctly: it is a counterfactual, not a system.

Term: money by billing class. The re-sent context of user-initiated steps is re-billed from the miss/write class to the hit class across human think time. It is an upper bound because it assumes every shifted token is served at the cache-read rate.

The lever it bounds is the cache TTL or keep-alive (paper §7.6: harnesses 'can periodically refresh the cache'). It trades storage for hits: raising the eviction timeout from 1 min to 1 h lifts the hit rate from 85.4% to 98.6% and the storage ratio R from 0.74 to 5.07 (paper §7.4).

The idle gap here is human time, not environment wait. For autonomous enterprise runs without human gaps the term is about 0.

The traces are coding agents (Claude Code, Codex), not GUI agents.

Credibility: passes as third-party measurement plus a preprint. Cite the paper's Table 13 figure (12.8%) as the versioned figure, and the dashboard's 15.8% as a dated live figure.

**authors and venue:**

Authors: Kan Zhu, Mathew Jacob, Chenxi Ma, Yi Pan, Stephanie Wang, Arvind Krishnamurthy, Baris Kasikci.
- University of Washington, all authors except as noted below.
- Chenxi Ma: Wuhan University of Technology (work done while interning at UW).
- Yi Pan: Shanghai Jiao Tong University.

This matches references.md. arXiv v2 is dated 30 Jun 2026. No venue.

**formula:**

Dashboard method, stated on the detail page:
- total_input(S) = prefix_tokens(S) + newly_append_tokens(S)
- context_growth(S) = max(0, total_input(S) - total_input(P))
- append_after_retained_cache(S) = min(newly_append_tokens(S), context_growth(S))
- prefix_after_retained_cache(S) = total_input(S) - append_after_retained_cache(S)
- Shifted tokens are billed at the cache-read price; the remaining Claude cache-creation tokens at the 5-minute write rate.

Paper:
- §7.5 caps append at max(0, L_S - L_P), with L = prefix + append.
- §7.4: the actively decoding fraction ≈ B·T_generation/(T_human + T_tool + T_generation), and the storage ratio R = (T_human + T_tool)/T_generation, with times capped by the eviction time.
- §7.3, Table 12: prefill amplification = append tokens / fresh tokens = 1/(fresh % of append).

## 141. Ares (adaptive reasoning effort)

**read:** https://arxiv.org/pdf/2603.07915v1 (v1, 9 Mar 2026; the only version; no arXiv comment or venue), read in full with pdftotext on 2026-09-28

**verdict:** confirmed

**effect:**

Table 1 (p.7; 'using gpt-oss-20b as the backbone LLM'). Columns are success rate, steps S, T_total, T_task and T_step:
- WebArena High: 45.0%, S 10.0, T_total 2763k, T_task 21424, T_step 2154.
- WebArena ARES: 46.5%, 8.9, 1512k, 11723, 1324.
- WebArena Low: 37.4%, 8.9, 67k, 520.
- TAU-Bench Retail High: 54.8, 13.8, 1007k, 8756.
- TAU-Bench Retail ARES: 54.8, 14.6, 652k, 5677.
- TAU-Bench Retail Low: 35.0.
- TAU-Bench Airline: High 38.0 / 873k; ARES 36.0 / 678k; Medium 42.0.
- BrowseComp-Plus: High 42.7 / 1841k; ARES 41.3 / 1071k.

§4.2: 'approximately 35.2% on TAU-Bench (Retail), 41.8% on BrowseComp-Plus, and 45.3% on WebArena in total reasoning token consumption (T_total)'. The paper says 35.2%; 1 - 652/1007 = 35.25% (calc.).

The abstract's 'up to 52.7%' is the RL-trained router on Retail (Table 2: 1007k to 476k, success 54.8 to 58.5), not the SFT router of Table 1.

What the metrics mean:
- WebArena reports task success rate, TAU-Bench average reward, and BrowseComp-Plus accuracy judged by GPT-4o.
- The WebArena agent is AgentOccam; train-test splits follow prior work.
- Test-set sizes are not stated. T_total/T_task gives about 129 (WebArena), 115 (Retail), 50 (Airline) and 150 (BrowseComp-Plus) tasks (calc.).

Uniform low effort: Retail 35.0% (-19.8 pp vs High). WebArena 37.4% is -7.6 pp vs High (calc.); the table's '↑9.1' arrow is measured relative to ARES.

Steps: WebArena 10.0 to 8.9, but Retail 13.8 to 14.6 (more steps).

Not reported: wall-clock time, and the router's own token or latency overhead.

**mechanism and term:**

The mechanism is described correctly: a Qwen3-1.7B router, fine-tuned by SFT and optionally GRPO, picks the lowest sufficient effort (low, medium or high) before every step of a gpt-oss-20b agent.

Terms:
- Decode: thinking tokens per call are smaller.
- Success rate: kept by the adaptive router (within 1.5 pp on Retail and WebArena; -2.0 pp Airline; -1.4 pp BrowseComp-Plus) and lowered by uniform low effort.
- Model calls per pass: one extra small-model call per step (the router, with a 3-5 sentence rationale); its overhead is unmeasured.
- Passes N change only slightly, in either direction.

The paper says the approach can 'preserve and reuse the KV cache across different reasoning effort levels'. That holds for its self-hosted gpt-oss-20b. On the Claude API, changing effort between steps invalidates the message cache unless the change is sent as a per-message-effort system message (Anthropic prompt-caching docs, 'What invalidates the cache', read 2026-09-28). The decode saving could then be offset by cache misses; this is a cross-source caution, not something Ares measured.

Credibility passes: UCSB and Accenture, public benchmarks, model stated.

**authors and venue:**

Authors:
- UC Santa Barbara (Department of Computer Science): Jingbo Yang, Bairu Hou, Shiyu Chang.
- Accenture (Center for Advanced AI): Wei Wei, Yujia Bao.

Bao and Chang are equal advisors. This matches references.md. It is a preprint; no venue is stated.

**formula:**

Already in the formula scan:
- §3.1 Eq. (2): max over theta of E over x, tau ~ T(theta, phi) of [V(tau, x) - lambda · Sum_{t=1..T} cost(e_t)], where cost(e_t) is all tokens the agent generates at turn t, thinking plus action.
- Eq. (4): R(tau) = R_out + R_cost + R_form if the task succeeds, otherwise R_out + R_form.
- Eq. (5): R_out = +5.0 on success, else 0.
- Eq. (6): c(e_t) = -0.2 / -0.5 / -1.0 for low / mid / high effort.
- R_cost = (1/T) · Sum of c(e_t).

## 142. Efficient Agents

**read:** https://arxiv.org/pdf/2508.02694v1. v1 of 24 Jul 2025 is the only version; the arXiv comment is 'Work in progress'. Crossref shows no venue.

**verdict:** confirmed

**effect:**

Table 7 ('Results on Different Agents', p. 8), 'all' columns. OWL: cost-of-pass 0.75, accuracy 53.33%, $0.398 per task, 189K tokens. Efficient Agent (ours): cost-of-pass 0.55, 51.52%, $0.285, 127K tokens. The Level-1 cost is $0.228 for Efficient Agent against $0.248 for OWL. Section 4 calls 28.4% a 'cost reduction', and 0.398 -> 0.285 is -28.4% (calc.). The abstract joins OWL's overall $0.398 to Efficient Agent's Level-1 $0.228 and calls the 28.4% a cost-of-pass gain. The actual cost-of-pass change is 0.75 -> 0.55 = -26.7% (calc.), or -25.9% from unrounded values (calc.). The Conclusion (p. 9) still has an unfilled placeholder ('reducing the operational cost by xx times'). CONDITIONS: GAIA 'development set' with Levels 1-3. The paper never states the task count: 165 is calc., because 53.33% = 88/165 and 51.52% = 85/165. The Efficient Agent backbone is GPT-4.1 (Table 6); the backbones and configurations of OWL and SmolAgents are not stated. Metric is pass@1, one run, with no repeats or CIs. Input and output token prices come from provider docs 'as of May 2025', and the prices themselves are not listed. There is no cache class, and no time is measured. Accuracy falls by 1.81 pp, about 3 of 165 tasks (calc.).

**mechanism and term:**

Partly wrong. The final configuration (Table 6) differs from the paper's own default (Table 8, App. A) in only three settings: max steps 8 instead of 12, 'Multi' search sources instead of 'Simple', and 5 search results instead of 10. Plan interval (1, i.e. replan every step), best-of-N (1) and memory (Simple) stay at their defaults. So replanning and sampling were ablated but not changed. Terms: N gets a smaller cap (12 -> 8 steps). Observation tokens per pass fall (5 vs 10 search results), which slows context growth (tokens/task 189K -> 127K against OWL). Money is lower and success rate slightly lower. 'c_k smaller' is not supported, because the paper reports no call counts. The headline also compares against a different framework (OWL), not an ablation, so the gain cannot be assigned to a single term. Time is not measured.

**authors and venue:**

The PDF byline is 'OPPO AI Agent Team', with @oppo.com correspondence addresses (He Zhu, Wangchunshu Zhou). The arXiv metadata and the PDF Contributions page list the same 14 names: Ningning Wang, Xavier Hu, Pai Liu, He Zhu, Yue Hou, Heyuan Huang, Shengyu Zhang, Jian Yang, Jiaheng Liu, Ge Zhang, Changwang Zhang, Jun Wang, Yuchen Eleanor Jiang, Wangchunshu Zhou. No venue. It is a preprint and passes the credibility rule, with the caveat that the GAIA task count is inferred, not stated.

**formula:**

Sec. 2.2 (p. 3), cost-of-pass after Erol et al.: v(m,p) = C_m(p) / R_m(p), with C_m(p) = n_in(m,p)·c_in(m) + n_out(m,p)·c_out(m). n_in and n_out are input and output tokens, c_in and c_out per-token prices, R_m(p) the success rate. The formula has no cache term.

## 143. Runaway is Ashamed, But Helpful

**read:** arXiv:2505.17616v2 PDF (22 Sep 2025), and the published ACL Anthology PDF 2025.findings-emnlp.1304, whose Table 1 values match v2. v1 (23 May 2025) was compared: its Redundant Steps values differ.

**verdict:** corrected

**effect:**

The 50-70% redundant-step reduction covers only the three embodied environments (ALFWorld, BabyAI, ScienceWorld). Sec. 4 (i) applies 'approximately 50% to 70%' to 'all three embodied environments'. For PDDL and Jericho, Sec. 4 (v) says the reduction is 'generally below 50%'. So the dossier's 'across ALFWorld/BabyAI/ScienceWorld/PDDL/Jericho' is wrong. ALFWorld with Llama3.1-70B-Instruct (Table 1) is confirmed. ReAct: SR 76.1, PR 81.1, RS 7.2, Steps 19.0. Extrinsic exit: SR 70.2, PR 79.3, RS 3.8, PD 8.7, Steps 13.4. For this representative row, RS falls 47% (calc.), below the 50-70% range; steps fall 29.5% (calc.) and SR 5.9 pp. RS changed between versions (v1 ReAct RS 2.3 -> v2 7.2; footnote 5 says the RS implementation was corrected); SR and Steps did not change. CONDITIONS: ALFWorld has 134 tasks with a 40-step limit, run in AgentBoard. The 70B model is 4-bit AWQ. Temperature 0.1, at most 256 tokens per turn, two A100 80GB GPUs with vLLM. The verifier runs every step (k=1) with the same backbone. Hybrid Int+Ext on the same row: SR 80.6 at 17.0 steps. No money or wall-clock is reported.

**mechanism and term:**

The mechanism is right. Intrinsic: an exit instruction is added to the prompt (an EXIT action). Extrinsic: the same LLM acts as a YES/NO verifier after every action and observation. Terms: N (passes per task) smaller, and success rate usually lower (the hybrid is sometimes higher). Add that the extrinsic variant adds one model call per pass (c_k + 1), whose prefill reads the whole trajectory. The paper calls the verifier's token cost negligible, but its token counts look output-only: 622 tokens per environment at about 26 steps (Table 3; calc. inference, since the paper does not define the count). The verifier's prefill is therefore not captured.

**authors and venue:**

Qingyu Lu, Liang Ding, Siyi Cao, Xuebo Liu, Kanjian Zhang, Jinxia Zhang, Dacheng Tao. Affiliations: Southeast University; The University of Sydney; SEU Shenzhen Research Institute; Harbin Institute of Technology (Shenzhen); Nanyang Technological University. Venue confirmed on the ACL Anthology: Findings of the ACL: EMNLP 2025, Suzhou, pp. 24014–24027, DOI 10.18653/v1/2025.findings-emnlp.1304. It is a conference paper (class A), not a preprint, and passes the rule. Add it to references.md.

**formula:**

No speedup or cost formula. Metric definitions only: Eq. 6, RS = n_total − n_subgoal. Eq. 7, PD = max(PR_ref − PR_exit, 0). Eqs. 2-4, u_intrinsic = concat(u, u_exit) and v_θ(·|e_t, u_extrinsic) ∈ {0,1}.

## 144. DARE, Budget-Aware Value Tree Search, OSWorld 2.0 thinking-level sweeps (qualitative only)

**read:** DARE: arXiv:2605.09188v1 PDF (9 May 2026), found through the arXiv API; the dossier cited only a homepage. BAVT: arXiv:2603.12634v1 PDF (13 Mar 2026). OSWorld 2.0: arXiv:2606.29537v2 PDF (13 Jul 2026).

**verdict:** corrected

**effect:**

DARE does have numbers, but none on an agent task. It is RL training for math reasoning. Table 3, MATH-500 with Qwen2.5-Math-1.5B, GRPO -> DARE: overall 67.40% / 627 output tokens -> 72.60% / 601 (-4%, calc.). Level 5 tokens rise 812 -> 912. BAVT: Sec. 4.2, OSS-20B mean EM 0.338 at the Low tier (5 tool calls) vs the baseline's 0.334 at the High tier (20 calls), and 0.194 at Low. Baseline is budget-matched parallel sampling with majority vote. Benchmarks: HotpotQA, 2Wiki, MuSiQue, Bamboogle. Models: GPT-OSS-20B and Qwen3-30B-A3B-Instruct-2507. Tiers are 5/10/20 tool calls, with 2k/4k/8k (reasoning) or 1k/2k/4k (instruct) output tokens. The number of evaluation questions is NOT stated. OSWorld 2.0 is a benchmark, not a method. Sec. 3.1: 108 tasks, 500 steps, screenshots, 16K output cap, a 3 s pause after each action. Thinking levels swept: low/medium/high/xhigh (+max for Opus), Sonnet 4.6 at medium and max. The 'plateau' sentence is about GPT-5.5's step budgets (150/300/500 steps all near ~14%), not thinking levels. The frontier runs ~14% at ~37K output tokens (GPT-5.5) -> 18.2% at ~150K (Opus 4.7) -> 20.5% at ~225K (Opus 4.8), about 25-30K extra output tokens per point. That frontier is across models.

**mechanism and term:**

'Difficulty-adaptive compute' fits only DARE, and DARE is not an agent work: RL training changes output tokens per call (decode) on single-turn math. Leave it out of the agent classification or label it non-agent. BAVT is budget-aware tree search, not difficulty-adaptive. Every step the same LLM is prompted again as a critic, adding a call per expansion (c_k larger; Sec. 6 admits the overhead). A remaining-budget exponent then prunes tool calls, so environment actions and N are capped and success rises at equal budget. BAVT fails rule (iii) because the task counts are missing, so use it qualitatively only. OSWorld 2.0 measures decode versus success; it is not an acceleration method.

**authors and venue:**

DARE: Yang Zhou, Can Jin, Zihan Dong, Zhepeng Wang, Yanting Yang, Shiyu Zhao, Lei Li, Runxue Bao, Yaochen Xie, Dimitris N. Metaxas. Affiliations: Rutgers, Amazon, Washington University, Google. Preprint with no venue. The dossier's 'Rutgers (homepage)' citation should become arXiv:2605.09188v1. BAVT: Yushu Li, Wenlong Deng, Jiajin Li, Xiaoxiao Li. Affiliations: University of British Columbia and Vector Institute. Preprint with no venue; it passes the author check and fails the task-count test. OSWorld 2.0 is already in references.md (XLANG Lab, HKU).

**formula:**

BAVT, Sec. 3: b_{t+1} = b_t − C(a_t) with C(a_t) = (C_tool, C_token); r_t = min(b_tool,t / B_tool, b_token,t / B_token); α_t = 1/r_t; w_{n_i} = V(n_i)^{α_t}. Baseline (Eq. 14): Σ_{i=1}^{K} C(τ_i) ≤ B. App. B.2 cost estimate: input tokens assumed 10× output, search $0.005 per query, search is over 90% of cost (Table 3, e.g. Low tier ≤ $0.02588 per sample with GPT-OSS). DARE and OSWorld 2.0 give no speedup formula relevant here.

## 145. The Danger of Overthinking

**read:** https://arxiv.org/pdf/2502.08235v1. v1 of 12 Feb 2025 is the only version. Crossref shows no venue.

**verdict:** corrected

**effect:**

$800 is the cost of two low-effort runs, then picking the one with the lower overthinking score; it is not the cost of 'low effort'. Sec. 1 (p. 2) and Sec. 5.6: o1 at high effort solves 29.1% for $1,400. o1 at low effort solves 21.0% for $400 (3.5× cheaper). Two low-effort samples plus selection give 27.3% for $800 total. With three samples the paper reports 30.3% vs 29.1% while 'still saving $200'. The $1,200 figure is never printed: it is calc. (3 × $400, or $1,400 − $200). The Fig. 3 caption rounds that saving to '15%'; it is 14.3% (calc.). CONDITIONS: SWE-bench Verified, with the task count not stated (the benchmark defines 500). OpenHands CodeAct. o1 (Dec 2024) without native function calling; with FC, o1-high reaches 47.7% (Sec. 6.1). Dollar figures are totals for the run, not per task. The selection judge is Claude 3.5 Sonnet at temperature 0; its cost is apparently excluded, since $800 = 2 × $400 (calc.). Figure 3 uses 90% Wilson CIs. The abstract's '~30% better, 43% cheaper' combines two baselines: +30% is relative to the $400 low-effort run (calc.), -43% relative to the $1,400 high-effort run. The Conclusion says +25% instead. Trajectory counts also disagree: 4,018 (abstract) vs 3,908 (Conclusion).

**mechanism and term:**

Decode per call is smaller (low reasoning effort). 'c_k larger with multiple samples' is imprecise. The paper does not add calls per pass: it runs k whole-task attempts (k = 2 or 3) plus one judge call per trajectory, which is best-of-k at the attempt level. Money falls 43% at k=2 for -1.8 pp success; at k=3 money falls 14% (calc.) and success rises 1.2 pp. Time is not measured.

**authors and venue:**

The authors match references.md l.68. Affiliations from the PDF: UC Berkeley EECS; ETH Zurich; UIUC; CMU. No venue was found, so it stays a preprint. It passes rules (i), (ii) and (iv); for (iii), the benchmark and model are named but the task count is only implied.

**formula:**

None for cost or speedup. Metrics only: Pass@k, Lowest Overthinking@k, and a linear regression of resolution rate on overthinking score (Table 1).

## 146. Budget Tracker / BATS

**read:** arXiv:2511.17006v2 PDF (17 Aug 2026). v1 (21 Nov 2025) was compared and has the same Tables 2, 3 and 9 values. OpenReview lists the paper under venue COLM 2026.

**verdict:** corrected

**effect:**

Budget Tracker figures are confirmed. Table 2 uses Gemini-2.5-Pro; App. Table 5 shows the dataset is BrowseComp. ReAct at budget 100: 12.6%, 14.24 search calls, 1.36 browse calls, 9.9¢ per question. With Budget Tracker at budget 10: 12.8%, 8.48 search, 1.09 browse, 6.8¢. The text gives -40.4% search, -19.9% browse, -31.3% cost. Table 1 values are 3-run means; Table 2 entries have no error bars. BATS at 24.6% vs 12.6% is confirmed (Table 3: 'budget of 100 tool uses per tool', Gemini-2.5-Pro, BrowseComp with 1,266 questions; BrowseComp-ZH 289 questions, 46.0 vs 31.5; HLE-Search 200 questions, 27.0 vs 20.5). BATS does NOT save resources against ReAct. Table 9 (BrowseComp) shows BATS using 87.3 search calls, 13.6 browse calls and $1.1 per question. That is about 6× the search calls and 11× the cost of ReAct@100 (calc.). Cost per success is $4.47 vs $0.79 (calc.). BATS's efficiency claim holds only against parallel majority voting at equal cost (Fig. 7, 200-question BrowseComp subset). CONDITIONS: tool calls are priced at a flat $0.001 each, a rate derived post hoc. Tokens are billed at Gemini list prices as input/output/cache-hit. Gemini-2.5-Pro thinking budget 1024; temperature 0.7.

**mechanism and term:**

Budget Tracker: tool calls, N and money are smaller at equal success rate. Most of the saving comes from lowering the cap from 100 to 10; the tracker is what keeps accuracy at the lower cap (ReAct at 10 gets 10.3%). BATS is different: N, tool calls and money go up, and success rate goes up. BATS also drops earlier tool responses from context (cache tokens 39.3 vs 91.8 ×10^4, Table 9), which slows context growth. 'Money smaller' must not be applied to BATS.

**authors and venue:**

Tengxiao Liu, Zifeng Wang, Jin Miao, I-Hung Hsu, Jun Yan, Jiefeng Chen, Rujun Han, Fangyuan Xu, Yanfei Chen, Ke Jiang, Samira Daruki, Yi Liang, William Yang Wang, Tomas Pfister, Chen-Yu Lee. Affiliations: UC Santa Barbara, Google Cloud AI Research, Google DeepMind, and New York University (Fangyuan Xu); the citation omits NYU. Venue: COLM 2026. The arXiv comment says 'Accepted to COLM 2026', and OpenReview lists it as COLM 2026 (venueid colmweb.org/COLM/2026/Conference). It is a conference paper and passes.

**formula:**

Eq. 2 (Sec. 3.2): C_unified(x;π) = c_token(x;π) + Σ_{i=1}^{K} c_i(x;π)·P_i. c_token covers input, output and cache-hit tokens at provider prices; c_i is the invocation count of tool t_i; P_i its price per call.

## 147. TTI ('Thinking vs. Doing') (counterpoint)

**read:** arXiv:2506.07976v2 PDF (10 Jun 2025), and the NeurIPS 2025 camera-ready PDF (proceedings.neurips.cc, hash f7c4783621a20f5f11a316cd249e0252). The camera-ready's Table 3 and 4 values and the <3% sentence match v2.

**verdict:** corrected

**effect:**

The paper says '<3%', not 'about 3%', and the claim covers both budget forcing and best-of-n, in an untrained prompting analysis. Sec. 1: at equivalent compute, forcing longer thinking or best-of-n 'yields less than a 3% gain'. Sec. 4.2 adds that budget forcing plateaus around 0.26. The setting is a prompted Gemma 3 12B base on 62 randomly sampled WebArena tasks with h = 30, averaged over 3 runs, from a CoT baseline of 23.81%. Compute is measured as tokens per trajectory. Main results are confirmed. Table 3, WebVoyager (427 tasks in 13 domains, Bing instead of Google): TTI 64.8 vs fixed h=10 59.1, zero-shot 55.8. Table 4, full WebArena (812 tasks): TTI 26.1 vs fixed h=10 23.8, zero-shot 18.3. Both are Gemma 3 12B, trained on 128K (WebVoyager) or 11K (WebArena) synthetic tasks with a Gemma 3 27B evaluator. No cost, wall-clock or tokens per task are reported for these runs.

**mechanism and term:**

Right. Curriculum online RL (filtered BC) raises the maximum horizon h from 10 to 30. N (steps per task) gets larger, and success rate rises. Figure 6c shows decode per call falling (per-step CoT tokens drop), but only normalized, on a held-out WebVoyager subset, with no absolute number. Treat it as a counterpoint: it trades more passes for less thinking per pass, and its effect on time and money is not measured.

**authors and venue:**

Junhong Shen, Hao Bai, Lunjun Zhang, Yifei Zhou, Amrith Setlur, Shengbang Tong (listed as 'Peter Tong' in the proceedings), Diego Caples, Nan Jiang, Tong Zhang, Ameet Talwalkar, Aviral Kumar. Affiliations: CMU, Scribe, UIUC, U Toronto, UC Berkeley, The AGI Company, NYU. Venue: NeurIPS 2025, Advances in NeurIPS 38, pp. 187840–187881, DOI 10.52202/085713-5647, under the title 'Thinking vs. Doing: Improving Agent Reasoning by Scaling Test-Time Interaction'. It is a conference paper and passes. Cite the NeurIPS version rather than 'CMU et al. preprint'.

**formula:**

No speedup formula. Sec. 4.2 states the cost of per-step best-of-n in its own symbols: '(n · h more expensive than the baseline per rollout)', where n is samples per step and h the horizon.

## 148. Google Gemini Priority inference and Microsoft Foundry priority processing

**read:** All read 28 Sep 2026 with curl, raw HTML converted to text. Google: https://ai.google.dev/gemini-api/docs/priority-inference (last updated 2026-09-23 UTC); https://ai.google.dev/gemini-api/docs/pricing (last updated 2026-09-24 UTC); launch post https://blog.google/innovation-and-ai/technology/developers-tools/introducing-flex-and-priority-inference/ (2 Apr 2026). Microsoft: https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/priority-processing (ms.date 2026-09-22); Azure pricing page https://azure.microsoft.com/en-us/pricing/details/azure-openai/. The Azure page builds its prices with JavaScript, so its prices were taken from the page's data-amount attributes (US East region). That extraction was done by our tool; no one read the rendered page. The dossier says this page was not read. Scratch copies are in .../scratchpad/wf-part2/vendor/.

**verdict:** confirmed

**effect:**

GOOGLE (docs, section 'How Priority inference works', comparison table). Pricing row: "75-100% more than Standard". Latency row: Seconds for Priority, Seconds to minutes for Standard, Minutes (1-15 min target) for Flex, Up to 24 hours for Batch. The Pricing section repeats the 75-100% premium, billed per token. The page also states:
- Priority requests go to high-criticality compute queues and are served ahead of Standard and Flex traffic.
- Priority traffic is non-sheddable.
- When Priority limits are exceeded, overflow requests are downgraded to Standard (not failed with 503/429) and billed at the Standard rate.
- Default Priority rate limits are 0.3x the standard rate limit.
- NEW, not in E197: the page header marks the Priority API as Preview.
- The launch post frames the tier around reliability: the request is not preempted at peak. It is available to Tier 2/3 paid projects.
GOOGLE LIST PRICES (pricing page; ratios are calc.). Every model that has a Priority table is exactly 1.80x Standard on input, output and the context-caching (cached-read) price. Cache storage per hour is unchanged. Examples:
- 3.8 Flash: $1.35/$6.75/$0.135 vs $0.75/$3.75/$0.075 through 31 Dec 2026; $2.70/$13.50 vs $1.50/$7.50 from 1 Jan 2027.
- 3.7 Flash and 3.6 Flash: same prices as 3.8 Flash.
- 3.5 Flash: $2.70/$16.20 vs $1.50/$9.00.
- 3.5 Flash-Lite: $0.54/$4.50 vs $0.30/$2.50.
- 3.1 Flash-Lite: $0.45/$2.70 vs $0.25/$1.50.
- 3.1 Pro Preview: $3.60/$21.60 vs $2/$12.
- 2.5 Pro, 2.5 Flash and 2.5 Flash-Lite: also 1.8x.
The prose says 75-100% more, but every listed price is +80%.
MICROSOFT (docs, section 'Latency target'). The target is defined as p50 request latency on a per 5-minute basis, expressed as a percentile threshold. Example given: '99% > 50 TPS' means 99% of requests are processed at more than 50 tokens per second. Per-model targets (all confirmed):
- gpt-6-sol 2026-09-22: 99% > 80 TPS
- gpt-5.6-terra: 70
- gpt-5.6-sol: 80
- gpt-5.5: 50
- gpt-5.4-mini: 100
- gpt-5.4 2026-03-05: 50 (footnote 1)
- gpt-5.2: 50
- gpt-5.1: 50
- gpt-4.1 2025-04-14: 80 (footnote 1)
Footnote 1: requests estimated to exceed 128k prompt tokens are downgraded to standard and charged at the standard rate. Section 'Limitations': requests may be re-routed to standard when traffic rises by more than 50% tokens per minute in under 15 minutes, and during peak priority demand. Priority uses the same quota as standard. The target is a vendor target, not a measurement. The page does not say whether TPS counts output tokens only, or whether time to first token or queue time is included.
NEW (Azure pricing page, Global, US East; extracted by our tool). Priority price vs Standard price, input/output per 1M tokens:
- GPT-5.6-sol $8/$40 vs $4/$20 (2x)
- GPT-5.6-terra $4/$24 vs $2/$12 (2x)
- GPT-5.4 (<272k) $5/$30 vs $2.5/$15 (2x)
- GPT-5.4 mini $1.5/$9 vs $0.75/$4.5 (2x)
- GPT-5.2 $3.5/$28 vs $1.75/$14 (2x)
- GPT-5.1 $2.5/$20 vs $1.25/$10 (2x)
- GPT-5.5 $12.5/$75 vs $5/$30 (2.5x)
- GPT-4.1 $3.5/$14 vs $2/$8 (1.75x)
- GPT-4.1-mini: 1.75x
Cached input is multiplied by the same factor. The GPT-6 Sol, Luna and Astra rows show Priority as N/A, although the docs list a latency target for gpt-6-sol. That is a conflict between the two Microsoft pages. The ratios are calc.

**mechanism and term:**

Largely right, with two corrections.
(1) Google: 'queueing smaller' is supported by the docs (high-criticality queues, served ahead of Standard and Flex). No numeric queue or latency figure is published; there is only the 'Seconds' class. Non-sheddable serving and downgrade-instead-of-503/429 also reduce failed calls, and so reduce retries. That is a secondary effect on calls and time, not on success rate as defined. Price/tier larger: +80% on every token class, including the cache-hit price. The cache-hit billing class is multiplied too, not only fresh tokens.
(2) Microsoft: the stated guarantee is a per-request token-rate floor (tokens/s), so it maps to per-call generation speed (decode rate, possibly including prefill and queue; the page does not say). It does not map to queueing as such. The mechanism behind it is not described. Price/tier larger: 1.75-2.5x by model (calc., from the pricing page's HTML).
For both vendors the latency benefit is conditional. Overflow, ramp-rate, peak-demand and >128k-prompt (footnoted Microsoft models only) requests fall back to Standard at Standard price. Neither vendor publishes a measured latency or task-time effect. Label: vendor docs, qualitative class or target only.

**authors and venue:**

Vendor documentation (primary for prices and tier rules). Google docs carry no author. The launch post is on blog.google, 2 Apr 2026; the author byline was not extracted. Microsoft Learn page, no named author. The Azure pricing page is vendor pricing. No third-party measurement of either tier was found.

**formula:**

Google: none. Only a percentage premium ('75-100% more') and per-token list prices. Microsoft: a definition, not a speedup formula. The latency target is p50 request latency per 5-minute window, expressed as a percentile threshold, e.g. '99% > 50 TPS' = 99% of requests processed at >50 tokens/s (section 'Latency target'). As written, this mixes a p50 and a 99th-percentile statement. Neither vendor gives a formula for time or cost savings.

## 149. Vendor move to smaller models for computer use (Claude in Chrome Haiku 4.5; Gemini computer use in Flash / Flash-Lite)

**read:** All read 28 Sep 2026 with curl, full raw HTML.
Anthropic:
- https://support.claude.com/en/articles/12138966-release-notes (JSON-LD dateModified 2026-09-25)
- https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome (dateModified 2026-08-26)
- https://www.anthropic.com/news/claude-haiku-4-5 (15 Oct 2025)
X posts, read through the public mirror api.fxtwitter.com (third-party mirror; X itself is robots-blocked):
- x.com/gabemulley/status/2026041548429828101
- x.com/trq212/status/2026110215561822374
- the post it quotes, x.com/DaLucasGonzalez/status/2026083348096180696
The secondary page pasqualepillitteri.it/en/news/346/... was unreachable (curl connection failure).
Google:
- blog.google posts: gemini-computer-use-model (7 Oct 2025); introducing-computer-use-gemini-3-5-flash (24 Jun 2026); gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber (21 Jul 2026); 3-8-flash-and-3-8-flash-cyber (2 Sep 2026)
- https://ai.google.dev/gemini-api/docs/computer-use (last updated 2026-09-23)
- https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite
- https://ai.google.dev/gemini-api/docs/pricing (2026-09-24)
- https://storage.googleapis.com/deepmind-media/gemini/computer_use_eval_additional_info.pdf (7 Oct 2025, read with pdftotext)
- https://www.browserbase.com/blog/evaluating-browser-agents (7 Oct 2025)
Third party: https://artificialanalysis.ai/models/gemini-3-5-flash-lite (read 28 Sep 2026, undated).

**verdict:** corrected

**effect:**

(a) CLAUDE IN CHROME DEFAULT. CORRECTION to E210/D136: the entry is still on the release-notes page. Under October 15, 2025 it says Claude in Chrome now defaults to Haiku 4.5 for a faster, more responsive experience, and users can switch back to Sonnet 4.5. The dossier's 'no longer visible, earliest entry 16 Jan 2026' was almost certainly a truncated fetch; the full HTML carries entries back to Aug 2025. Timeline on the same page:
- 29 Sep 2025: default is Sonnet 4.5.
- 15 Oct 2025: default is Haiku 4.5.
- 24 Nov 2025: users choose Haiku 4.5 (for speed), Sonnet 4.5 or Opus 4.5.
The current help article states no default: available on all public models (section 'Model selection'). The current default remains unknown. No task-speed number is on any Anthropic page. The Haiku 4.5 launch post (15 Oct 2025) makes a vendor-marketing claim: Sonnet 4-level coding at one-third the cost and more than twice the speed. The speed metric is undefined. Price $1/$5 per M.
(b) QUICK MODE. CORRECTION: the '~3x' is not in the Mulley or Thariq posts.
- Mulley, 23 Feb 2026 21:08 UTC: rolls out an experimental Quick Mode to all users. No multiplier; pairs it with Opus 4.6 fast mode or Haiku 4.5.
- Thariq, 24 Feb 2026 01:41 UTC: 'significantly faster'. No multiplier.
- The '3x faster than before' claim comes from the post Thariq quotes: Lucas Gonzalez (X bio: model PM at Anthropic), 23 Feb 2026 23:54 UTC. It comes with a 58-second race video.
No task, model, metric or baseline is stated. The '4+ minutes to under 2' wording and the single-letter command-language mechanism exist only on the secondary site, which was unreachable.
(c) GEMINI 3.5 FLASH-LITE. The model page lists Computer use as 'Supported (Preview)', Stable: gemini-3.5-flash-lite, latest update July 2026. CORRECTION on labelling: the 350 t/s is not Google's own measurement. The 21 Jul 2026 post (Tulsee Doshi) attributes it twice to Artificial Analysis: 350 output tokens/s 'according to the Artificial Analysis Index' and 'As measured by Artificial Analysis'. AA's page read 28 Sep 2026 shows 337.5 output tokens/s, rank #5 of 175, measured on Google's API for the reasoning variant. AA defines speed as tokens/s after the first chunk. The dossier's 349 t/s is superseded: AA's number drifts, so it must be cited with the read date. The same AA page (FAQ) gives TTFT 10.20 s, versus a 2.18 s median for its price tier. The post also claims (vendor, no conditions) OSWorld-Verified 74.0% for 3.5 Flash-Lite vs 65.1% for 3 Flash, at $0.30/$2.50.
(d) LINE-UP. The docs' 'Model versions' section now says in its own text:
- gemini-3.8-flash is the recommended model for computer use.
- gemini-3.5-flash-lite is a low-latency, cost-effective model supporting computer use.
- gemini-2.5-computer-use-preview-10-2025 is a legacy preview model.
E198's 'tool-extracted' caveat can be dropped. The pricing page's tools table charges computer use as regular tokens at the model's price and refers to the 2.5 CU table for legacy rates ($1.25/$10 up to 200k). The 3.5 Flash post (24 Jun 2026) says computer use was previously only a standalone 2.5 model and is now native in Flash. That post gives no speed figure.
(e) 2.5 CU CHART. The alt text is confirmed verbatim: 70%+ accuracy, about 225 sec latency, Browserbase harness, Online-Mind2Web. Google's evaluation PDF says Browserbase measured accuracy and latency with identical harnesses per API, but never defines latency. The same PDF self-reports Online-Mind2Web success of 69.0% (pass@1, temperature 1, majority of 3 human judges, validated by the benchmark organizers). Browserbase labels its chart 'OnlineMind2Web @ 50 steps', with the same step limits and timeouts for every model; the chart images were not read. The 2.5 CU model is built on Gemini 2.5 Pro.

**mechanism and term:**

Partly right, with corrections.
(1) Model-tier moves (Haiku 4.5 default; computer use native in Flash and Flash-Lite in place of the Pro-based 2.5 CU model). These change the price per token: the 2.5 CU legacy output price is $10 vs $2.50 for Flash-Lite and $3.75 for 3.8 Flash introductory (calc.: 4x and 2.7x). They also change decode speed (tokens/s). Nothing shows that per-call time or task time falls. AA's figures show Flash-Lite pairs fast decode with a long TTFT (10.2 s), and the thinking level is a separate decode-token lever that the docs expose. So decode rate alone does not fix per-call time.
(2) A smaller model can change the success rate. The only evidence is vendor benchmark claims (OSWorld-Verified 74.0% for Flash-Lite, no conditions). The goal (cost per success without losing success) is not shown by any vendor source.
(3) Google's recommended computer-use model is 3.8 Flash, not Flash-Lite, so 'move to smaller' should read 'move from a specialised Pro-derived model to Flash-class models'.
(4) Quick Mode is not a model or tier change. It is a harness change. Per the secondary only, it uses a compact action language, which would mean fewer output (decode) tokens per action. The primary sources give only 'faster' or '3x' with no definition. Classify it under decode tokens per call, marked unverified, not under price/tier.

**authors and venue:**

Vendor primary: the Anthropic release notes and help article (no author) and the Anthropic news post of 15 Oct 2025. Staff social posts, whose text was read through a third-party mirror:
- Thariq, bio 'Claude Code @anthropicai'.
- Lucas Gonzalez, bio 'model PM at anthropic'.
- Gabe Mulley: bio empty in the mirror, so his affiliation is not confirmed from the post itself.
Google posts:
- 2.5 CU: byline Google DeepMind, 7 Oct 2025.
- 3.5 Flash CU: Mateo Quiros, Product Manager, Google DeepMind, 24 Jun 2026.
- 3.6 Flash/3.5 Flash-Lite: Tulsee Doshi, Senior Director, Product Management, 21 Jul 2026.
The Google DeepMind evaluation PDF of 7 Oct 2025 has a long contributor list. The Browserbase post is by Miguel Gonzalez and Sean McGuire, 7 Oct 2025 (a partner, not independent). Artificial Analysis is a third-party measurement. All speed claims are vendor-stated or vendor-quoted. None is an independent task-level measurement.

**formula:**

No vendor source gives a speedup or cost formula. The only formulas are Artificial Analysis metric definitions on the Flash-Lite page:
- Output Speed = tokens/s received after the first chunk.
- Time per Intelligence Index task = output tokens per task ÷ output speed. AA says this excludes TTFT and overhead.
- End-to-End Response Time = seconds to output 500 tokens, from time to first token, 'thinking' time and output speed.
These are third-party definitions, not the vendors'.

## 150. Browserbase Stagehand cache (vendor)

**read:** All fetched 28 Sep 2026 with curl; the plain text is saved under /private/tmp/claude-501/-Users-edwin-projects-agent-acceleration-research/7deb32b8-8e56-4ffc-8813-5ea7da470b16/scratchpad/wf-part2/v/ (bb_*.txt, sh_*.txt, bb_v3_notion_table.tsv). Sources: the caching blog https://www.browserbase.com/blog/stagehand-caching (24 Feb 2026); the v3 caching docs https://docs.stagehand.dev/v3/best-practices/caching; the v4 caching docs https://docs.stagehand.dev/v4/best-practices/caching; the v3 blog https://www.browserbase.com/blog/stagehand-v3 (29 Oct 2025) and the eval page it links, https://browserbase.notion.site/Stagehand-v3-benchmarking-2963c11b661480648b12fbd4885c3b10. That page is rendered by JavaScript, so I read its Summary table through Notion's public loadCachedPageChunkV2 API. The eval runs inside its toggles returned 403 and were not read. Also: the v4 blog https://www.browserbase.com/blog/stagehand-v4 (10 Aug 2026); https://www.browserbase.com/changelog (entries of 28 Jul, 10 Aug and 21 Aug 2026) with /changelog/stagehand-v4 and /changelog/model-router; https://docs.stagehand.dev/v3/configuration/models (Model Router); https://www.browserbase.com/pricing.

**verdict:** corrected

**effect:**

(a) Cache "~80%" (caching blog, intro, bb_caching.txt l.117; section 'Measuring performance', l.207). The figure is a best case ('as high as'). It is defined as the % speedup from run 1 to run 2 when the SAME ACTION is run twice in a row: run 1 writes the cache entry, run 2 reads it and makes no LLM call. The blog says the number varies heavily by workload. It gives no task set, n, model or absolute times. CORRECTION: this is a per-action figure, not a 'second cached run' of a whole workflow.
(b) v3 '44.11% faster' (v3 blog l.119; l.155 says '44%+'). It compares v3 with v2 on iframe and shadow-root interactions. The linked Notion Summary table lists 10 evals (iframe_form_filling … spif_in_osr) with a v2 and a v3 value each; units are not stated. 44.11% is reproduced exactly as the mean over the 10 evals of (v2/v3 − 1), calc. In time-saved terms, the mean per-eval reduction is 28.0% and the reduction in total time is 28.4% (calc.). The page does not state the model, the runs per eval, or whether LLM time is included. The figure comes from an SDK/driver rewrite (CDP instead of Playwright), not from caching.
(c) v4 (changelog 10 Aug 2026, bb_changelog.txt l.221): '2x faster than Playwright' and '~80% more token efficient'. No method, workload or token baseline is given, and Playwright itself makes no model calls. The v4 blog does not repeat these figures. Its only measurement (bb_v4.txt l.208) is one 50-action Wikipedia crawl: experimentalBatch took 14,221.7 ms and Playwright 22,650.3 ms, both completed 50/50 actions, i.e. 3.52 vs 2.21 actions/s, a 1.59× difference, with 44.0 ms overhead for the batch call. Per-action medians: waitForSelector 493.2→237.6 ms, click 628.1→323.1 ms, goBack 139.5→17.5 ms. Client-to-remote round trip: 42.2 ms. The blog itself calls this one run on one route, not a benchmark.
(d) Model Router (changelog 28 Jul 2026; models docs l.305): teams 'typically' see 30–40% lower inference cost than pinning one model for every call. No task set, success rate or period is given.
(e) Price (pricing page, read 28 Sep 2026; vendor primary). Developer: $20/mo with 100 browser hours included, then $0.12 per browser hour. Startup: $99/mo with 500 h included, then $0.10 per browser hour. Free plan: 1 h. Scale plan: usage-based. Model tokens are billed at market price through Model Gateway. Proxies: $12/GB (Developer), $10/GB (Startup). So $0.10–0.12 is the rate charged above the hours included in the plan.
The effect numbers stay labelled vendor-marketing (not cited). The v4 1.59× is a single vendor-run measurement.

**mechanism and term:**

Partly wrong; four corrections.
(1) What is cached is the result of one Stagehand primitive call: act(), and since v4 also observe() and extract(). For an action that is the resolved selector plus the action config (caching blog l.117). It is not the agent's whole trajectory.
(2) The pre-check. In the Feb 2026 (v3-era) design, the cache key is a sha256 of the method, normalized URL, DOM hash, project scope and a few method-specific fields. Before replay, the current page's snapshot fingerprint is compared passively against the one recorded with the entry, using an undisclosed safety threshold; drift makes the request a cache miss (blog l.156). The v4 docs (21 Aug 2026) build the key from the instruction, page content and options, and leave model configuration out of it. v4 serves a hit only after a configurable number of identical results (the hit-count threshold). v4 also adds a post-hoc check: a cached act() is replayed with self-healing turned off, and if the recorded selector no longer resolves Stagehand falls back to full inference (sh_v4_caching.txt l.436, l.569).
(3) On a miss, only that one call runs with normal LLM inference and writes a new entry. The full agent does not redo the step. The doc2 §1.5 table row '完整 agent 重做这一步并刷新缓存' should read '这一次 act()/observe()/extract() 调用照常调模型，并写入新缓存'.
(4) v4 removed client-side caching (cacheDir). E153's 'local cacheDir variant' is v3-only. The server cache needs a Browserbase browser; with a local browser every call runs inference. Locator-scoped calls are not cached. The blog describes entries as project-scoped and valid for 48 h; the v4 docs do not restate the 48 h.

TERMS. On a hit, c_k → 0 for that call: no queueing, prefill or decode at the model and zero tokens in every billing class, replaced by a cache lookup at Browserbase. Environment observe/act/wait is unchanged; the blog says browser execution time remains. N is unchanged. On the success-rate term, the blog says it favours accuracy over hit rate, but it publishes no replay error rate.
The vendor's other items map to other terms. v3 44% and the v4 1.59× → environment act time (fewer client–browser round trips). v3 may also cut prompt tokens through its 'context builder', but the two effects cannot be separated. Model Router 30–40% → price per token (model choice per call). The browser-hour price → the environment machine-hours term.

D-CANDIDATES (allocate IDs after a git fetch):
- E203/E154: 44.11% is a mean of speed ratios, not 44% less time (28% mean time saved, calc.).
- E154/D114: the ~80% is a per-action best case.
- E153: cacheDir is v3-only; v4 uses a hit-count threshold plus a selector-resolve fallback.
- doc2 §1.5: the '完整 agent' wording.

**authors and venue:**

Vendor engineering blog, changelog and docs from Browserbase, Inc.; no peer review. Caching blog: Sameel Arif, 24 Feb 2026. v3 blog: Miguel Gonzalez and Harsehaj Dhami, 29 Oct 2025. v4 blog: Miguel Gonzalez, Sean McGuire, Sam Finton and Harsehaj Dhami, 10 Aug 2026. Changelog entries: 28 Jul, 10 Aug and 21 Aug 2026. The docs pages are undated. The credibility labels stand: effect numbers are vendor-marketing; the pricing is vendor primary.

**formula:**

No formula with symbols. The caching blog defines its metric only in words: % speedup from run 1 to run 2 of the same action; it does not say whether that is (t1−t2)/t1 or t1/t2−1. The Notion eval page gives no formula; mean_i(t_v2,i / t_v3,i − 1) over the 10 evals reproduces 44.11% exactly (calc., our reconstruction). The v4 blog shows only arithmetic in prose: actions/s = 50 ÷ wall-clock (3.52 and 2.21) and 1.59 as their ratio. Pricing is given as a table: plan fee plus overage × the browser hours above the plan's included hours.

## 151. Skyvern code cache (vendor, qualitative)

**read:** https://www.skyvern.com/docs/developers/features/code-caching and https://skyvern.mintlify.app/developers/optimization/cost-control, fetched 28 Sep 2026 with curl (both undated). Text saved as .../scratchpad/wf-part2/v/sky_codecache.txt and sky_cost.txt.

**verdict:** confirmed

**effect:**

No measured number, as E158/E160 say.
The code-caching page (sky_codecache.txt l.254–275) calls cached runs faster, cheaper and deterministic, with no figure. The cost-control page says cached code runs are significantly cheaper, again with no figure.
Plans on the cost-control page: Free $0, ~200 actions; Hobby $29, ~1,200; Pro $149, ~6,200; Enterprise custom. That is about $0.024 per action (29/1,200 ≈ 149/6,200, calc.). Whether a cached-code step uses an action credit is not stated.

**mechanism and term:**

Mechanism confirmed; the term mapping needs one correction.
How it works: the first run with run_with="agent" records the successful actions and generates code from them. Later runs with run_with="code" replay that code with no screenshots and no LLM reasoning. If the replay hits a layout change, a new field or a missing element, Skyvern re-runs with the full agent and regenerates the cache.
Details the dossier row lacks: a task caches its full action sequence; an agent (workflow) caches per block, so it can be partly cached; caching builds up across conditional branches ('progressive caching'); conditional-evaluation, wait and code blocks are never cached and always run live.

TERM CORRECTION. 'N → 0' is wrong in our notation. A replay still performs every environment action: act, wait and page loads remain. What goes to zero is c_k for every replayed pass, and with it queueing, prefill and decode time, all token billing classes, and the context-growth term (no prompt is built). The observation cost shrinks too (no screenshot analysis). On a fallback, the full agent reruns; the docs do not say whether a task restarts from the failing step or from the start. So cost per attempt = partial replay + full agent run + cache regeneration, and it enters cost per success through the fallback rate, which is unpublished. The uncached conditional blocks may still call a model; the docs do not say.

**authors and venue:**

Vendor product docs (Skyvern), undated, no named author. Vendor primary for the mechanism, with no effect number; the credibility label is correct.

**formula:**

None. Price is given only as a plan table (price and actions included).

## 152. Hyperbrowser HyperAgent action cache (vendor, qualitative)

**read:** https://www.hyperbrowser.ai/docs/hyperagent/action-cache and https://raw.githubusercontent.com/hyperbrowserai/HyperAgent/main/README.md (main branch), fetched 28 Sep 2026 with curl. Text saved as .../scratchpad/wf-part2/v/hb_actioncache.txt and hb_readme.txt.

**verdict:** confirmed

**effect:**

No numbers.
The docs' comparison table under 'Why Use Action Caching?' (hb_actioncache.txt ~l.300–310) is qualitative vendor-marketing: without caching, an LLM call on every run and higher latency; with caching, one LLM call then free replay, 'near-instant replay', and pay once.
The docs' own section 'Monitoring Fallback Rates' (l.548–561) concedes that a fallback adds latency and cost.
No replay success rate, fallback rate, latency or $ figure is published. The README (l.410) says replay tries XPath first with no LLM calls and falls back to the LLM only if the page structure has changed.

**mechanism and term:**

Mechanism confirmed, with two corrections.
Replay order, as documented: cached XPath first; retry up to maxXPathRetries; then an LLM fallback using the cached instruction; replay stops on the first failure by default.
(1) '3 retries' is the value used in the docs' and README's example config (maxXPathRetries: 3). The default value is not stated.
(2) The LLM fallback happens only if the step carries a performInstruction ('Monitoring Fallback Rates').
Failure is detected after the fact, when the XPath does not resolve; there is no check that the page is the same before replay. A cache can also be exported as a standalone script (createScriptFromActionCache).

TERM CORRECTION. Not 'N → 0': the environment actions still run. On an XPath hit c_k → 0: no prefill, decode or tokens, and no context growth. On a miss there is one LLM call per failing step, to re-find the element from the cached instruction; this is not a full-agent rerun. Because replay stops on the first failure by default, a failed step ends the attempt, which feeds the success-rate term.

**authors and venue:**

Vendor docs and the open-source repo hyperbrowserai/HyperAgent, both undated, no named author. Vendor primary for the mechanism; 'near-instant replay' is vendor-marketing. The labels are correct.

**formula:**

None.

## 153. Anthropic fast mode

**read:** https://platform.claude.com/docs/en/build-with-claude/fast-mode and https://platform.claude.com/docs/en/about-claude/pricing (§Fast mode pricing, and the model price table), fetched 28 Sep 2026 with curl. Text saved as .../scratchpad/wf-part2/v/an_fast.txt and an_pricing.txt. I also ran one web search on 28 Sep 2026 for an independent measurement of fast-mode speed and found none.

**verdict:** confirmed

**effect:**

Page intro and §How fast mode works: up to 2.5× higher output tokens per second than standard speed, on Claude Opus 5.5, Opus 5 and Opus 4.8.
§How fast mode works and §Considerations: the gain is focused on output tokens per second (OTPS), not time to first token (TTFT). The model weights and behaviour are the same.
Availability: research preview, access through an account manager or a waitlist, on the Claude API only (including Claude Managed Agents). Not on Bedrock, Claude Platform on AWS, Google Cloud or Microsoft Foundry. Opus 4.7 returns an error; Opus 4.6 silently runs at standard speed and standard price.
§Pricing: Opus 5.5 $8/MTok input and $40/MTok output; Opus 5 and Opus 4.8 $10/$50. Standard Opus 5.5 is $4/$20 on the pricing page, so fast mode costs 2.0× (calc.).
No TTFT figure and no task-time figure are given. No independent measurement was found (E209's absence finding, re-checked by one search only).

**mechanism and term:**

Confirmed, with refinements.
Decode term: the claimed gain is output tokens/s. That output includes thinking tokens under our definition; the docs do not mention thinking separately, so this is our inference. Prefill and queueing gains are not claimed, since TTFT is explicitly excluded.
Price/tier: 2× on input and output, across the full context window. The docs say prompt-caching and data-residency multipliers apply on top of the fast price, so cache-hit, cache-write and miss prices all double too (calc.: an Opus 5.5 cache hit is 0.05× of $8 = $0.40 vs $0.20 at standard).
Billing class: switching speed invalidates the prompt cache, including the documented client-side fallback from fast to standard on a 429. Hits then become misses: on money, R^hit → R^miss; on time, an extra prefill.
Other conditions: a dedicated rate limit (429 with retry-after, or 529 at capacity); not available with the Batch API or a Priority Tier commitment.
Net effect on task time: at most the decode share of per-call time is cut; the environment terms are untouched.

**authors and venue:**

Vendor developer docs (Anthropic). The pages are undated; the beta header is fast-mode-2026-02-01. The reference 'Anthropic (2026b)' is correct. The 2.5× is a vendor-stated maximum.

**formula:**

No speed formula. The pricing is stated in words: fast mode is a multiplier on standard rates across the full context window, and the prompt-caching and data-residency multipliers stack on top of it. The pricing page's cache multipliers (hit 0.05× base on Opus 5.5; 5-minute write 1.25×, 1-hour write 2×) therefore apply to the fast base price.

## 154. OpenAI Fast mode, Flex and Batch

**read:** All fetched 28 Sep 2026 with curl; text saved under .../scratchpad/wf-part2/v/ (oa_*.txt). Sources: https://developers.openai.com/api/docs/changelog (entries of 27 Jun 2025, 30 Jul 2026 and 5 Aug 2026); https://developers.openai.com/api/docs/guides/fast-mode (a live guide not yet cited in the dossier; D132 recorded only that the old priority-processing URL is dead); https://developers.openai.com/api/docs/pricing (the flagship Standard, Batch, Flex and Fast tables); https://developers.openai.com/api/docs/guides/flex-processing; https://developers.openai.com/api/docs/guides/batch. The pricing page's 'All models' tables are not in the static HTML and were NOT read.

**verdict:** corrected

**effect:**

Changelog, 30 Jul 2026: Fast mode replaces Priority Processing, and requests tagged priority now use Fast. For GPT-5.6 Sol it delivers speeds up to 2.5× faster than standard processing, at twice the price.
Changelog, 5 Aug 2026 — a separate entry; E192 wrongly dates it to 30 Jul. Fast mode now takes long-context (>272K) prompts for GPT-5.6 Sol, Terra AND Luna, again at speeds up to 2.5× faster than Standard. So the 2.5× wording is not limited to Sol, which corrects E192's 'only for GPT-5.6 Sol'.
Fast mode guide: up to 2.5× faster speeds 'and more consistent latency'. A note says the speed rise to 2.5× was made for gpt-5.6-sol. The guide never defines 'speed' (tokens/s or latency).
- Ramp rule: once traffic reaches 1M input TPM, raise it by no more than 50% per 15 minutes; otherwise some Fast requests are downgraded to standard speed and charged standard rates.
- FAQ: GPT-5.6 Sol Fast costs twice Standard ($8/$40 per 1M tokens short context, $16/$60 long context). Fast for GPT-6 Astra has no latency SLA. Cached-input discounts still apply in Fast.
Pricing page, flagship tables (read 28 Sep): Fast is 2.00× Standard in every cell for gpt-6-astra, gpt-6-sol and gpt-6-luna, short and long context (calc.; e.g. gpt-6-sol $4 / $0.40 / $5 / $20 vs $2 / $0.20 / $2.50 / $10 for input, cached input, cache write and output). Batch = Flex = 0.50× Standard for the same three (calc.; gpt-6-sol $1 / $0.10 / $1.25 / $5).
- CORRECTION to E193: gpt-6-astra now has a Flex row ($5 / $0.50 / $6.25 / $25), and the Flex guide uses gpt-6-astra as its example.
- I could not check 'every listed model' beyond these three and gpt-5.6-sol (via the guide), because the other rows were not in the page I fetched.
Flex guide: lower cost in exchange for slower response times and occasional resource unavailability; tokens priced at Batch rates, plus caching discounts; in beta with limited models. When resources are short it returns 429 Resource Unavailable and does not charge; the guide suggests retrying on standard. The SDK default timeout is 10 minutes, and the examples raise it to 15. No latency number.
Batch guide: 50% discount; each batch completes within 24 h, and the completion window can only be set to 24h.
Changelog, 27 Jun 2025: Priority processing was described as giving lower and more consistent latency than Standard (paraphrase).

**mechanism and term:**

Mostly right; corrections:
(1) OpenAI never says what its 'speed' multiplier measures. Unlike Anthropic, it never says TTFT is unchanged. So doc2 §2.6's '不改首 token 等待' holds for Anthropic only. Map OpenAI Fast to 'per-call model time, split between queueing, prefill and decode unspecified; vendor-stated up to 2.5× (GPT-5.6 Sol; and long-context Sol, Terra and Luna)'. The 'more consistent latency' wording points at lower queueing variance, but that is vendor wording, not a measurement.
(2) Price/tier: Fast is 2× on every billing class, including cached input and cache writes. Flex and Batch are 0.5× on every class.
(3) OpenAI does not say that switching tier invalidates the prompt cache; it says cached-input discounts apply in Fast. Anthropic's cache caveat is therefore not established for OpenAI.
(4) Queueing: Flex is slower by an unquantified amount, and its 429s bring retries, which hit both the time and the success terms. Batch can take up to 24 h, which does not fit an interactive loop pass; it suits only work that does not need an immediate answer (our reading).
(5) Because of the ramp-rate downgrade, some Fast requests can silently run at standard speed and standard price.
D-CANDIDATES:
- E192: the long-context entry is dated 5 Aug and covers Sol, Terra and Luna.
- E193: gpt-6-astra now has a Flex row.
- E77/D132: add the live guide /api/docs/guides/fast-mode.
- doc2 §2.6: the TTFT wording applied to OpenAI.

**authors and venue:**

Vendor docs, changelog and pricing page (OpenAI); the reference 'OpenAI (2026)' is fine. Add the Fast mode guide URL. The speed figures are vendor-stated maxima.

**formula:**

Stated in words only. Fast mode guide FAQ: GPT-5.6 Sol Fast costs twice the corresponding Standard rate, with $ figures. Flex: tokens at Batch API rates, plus caching discounts. Batch: 50% discount compared with the synchronous APIs. No speed formula.

## 155. OpenAI Ultrafast on Cerebras

**read:** OpenAI:
- changelog entry of 13 Aug 2026 (curl);
- launch post https://openai.com/index/previewing-ultrafast/ — returns 403 to curl and WebFetch; I read it in the desktop app's built-in browser on 28 Sep 2026 (E194 lists it as unread);
- staff community post, read through Discourse's JSON: https://community.openai.com/t/ultrafast-mode-preview-gpt-5-6-sol-at-up-to-14x-the-speed-in-the-api/1390344.json.
Cerebras (with their chart images, which I viewed):
- https://www.cerebras.ai/blog/accelerating-gpt-5-6-sol-ultrafast-with-openai (13 Aug 2026), two images;
- https://www.cerebras.ai/blog/the-rise-of-slow-personal-assistants (24 Sep 2026), seven images.
Text and images saved under .../scratchpad/wf-part2/v/ (cb_ultra.txt, cb_slow.txt, cb_img*.png, slow*.png).

**verdict:** corrected

**effect:**

OpenAI (changelog, launch post, staff post): Ultrafast is a new service tier that runs GPT-5.6 Sol up to 14× faster than Standard processing, at up to 750 output tokens/s. It is powered by Cerebras and is a limited preview for select customers. The launch post gives no price, no TTFT and no task time; it has only a side-by-side demo video (building a 3D warehouse simulator) and customer quotes. E194 is confirmed.
Cerebras blog, 13 Aug 2026 (author Joyce Er).
- Chart 1: Ultrafast 14×, 'GPT-5.6 Sol Priority' 2.5×, Standard 1×.
- '11× faster than Fable 5' and '5× faster than Opus 4.8 on Fast mode' are output-speed comparisons. The text says: "Compared with output speeds reported by Artificial Analysis" (§Frontier Intelligence at Unprecedented Speed). This corrects E195, which says the speed definition is not stated.
- HLE: Cerebras ran all 2,500 questions. GPT-5.6 Sol Ultrafast with Codex at xhigh reasoning (run 10 July) took 11 h 11 min. Claude Fable 5 with Claude Code at xhigh (13–15 July) took 78 h 27 min. The blog calls this comparable accuracy, nearly 7× faster (calc.: 4,707 / 671 min = 7.0×). No accuracy values are given in the text, and model and harness both differ.
- GDPval: a 5.6× end-to-end speedup with no quality degradation. Conditions in the text: run by Cerebras on 31 July 2026, GPT-5.6 Sol vs GPT-5.6 Sol Ultrafast, medium reasoning, inside Codex. The chart 'Inference vs. Non-Inference — GDP-Val' shows mean wall-clock components across 6 quality-matched tasks:
  • Ultrafast: 83.0 s total = 68.1 s model request + 14.9 s non-inference.
  • Standard: 7.7 min total = 7.5 min model request + 14.2 s non-inference.
  • calc.: 462 / 83.0 = 5.57× end-to-end; model request 450 / 68.1 = 6.6×; the non-inference share rises from 3% to 18%.
  So 'end-to-end' IS defined, as mean wall-clock over 6 tasks, which corrects the 'undefined' in E195 and in the claim. How the 6 tasks were chosen and how many runs per task are not stated.
- Footer: the comparisons come from third-party benchmarking or internal testing, and results may vary.
Cerebras 'slow personal assistants', 24 Sep 2026 (Sarah Chieng, Sherif Cherfa) — E201:
- 22 s is the median of two successful attempts (chart caption). Set-up: Qwen 3.8 27B on Cerebras, the Pi harness, a site skill written before the timed run (in their test it cut tool calls by more than 80%), and parallel availability checks.
- Baselines: Meta Muse 4 min 36 s (nine direct OpenTable API calls), Claude Cowork 6 min 25 s (57 tool calls), Grok Bot 7 min 40 s. Each made a correct reservation. A manual booking takes 37 s (no protocol given).
- '19× faster than existing assistants' has no stated baseline (calc. 12.5–20.9×).
- Chart 'Where the recorded time went' (model & orchestration + browser & API): Grok 3:09 + 4:31, Cowork 3:03 + 3:22, Muse 2:30 + 2:06.
Corrections to E201:
(i) The page does not say how many runs the three commercial assistants got; it calls them recorded runs, not a general ranking. E201's 'single runs' is an inference.
(ii) The page contradicts itself. The text says the browser/API part of the optimized run took 6.8 s (≈40× less than 4:31). Its chart 'Inside the 22 second run' shows 3.63 s model & orchestration, 17.53 s browser & API and 0.45 s other overhead. Its step timeline shows 3.74 s reasoning & orchestration (17%), 4.15 s site API calls (19%) and 13.74 s browser sessions (64%). By the chart the ratio is 4:31 / 17.53 s = 15.5× (calc.).
(iii) E201's calc that browser/API is ~59% of the Grok trace is confirmed by the chart: 271 / 460 s = 58.9% (calc.).
Everything here is vendor-run by Cerebras, OpenAI's hardware partner → vendor-marketing.

**mechanism and term:**

Mechanism: a serving tier for one model (GPT-5.6 Sol) on Cerebras wafer-scale hardware. Per Cerebras, each chip holds 44 GB of SRAM and the weights stay on-chip.
TERMS
- The headline claims (14×, 750 tokens/s, 11× and 5× against Artificial Analysis output speeds) are output-token speed → the decode term.
- The GDPval chart is the only vendor figure found that splits model-request time from non-inference time. It fits our formula: only the model-call part shrinks (6.6×, calc.), non-inference stays at about 14–15 s, and so end-to-end is 5.6×, well below 14×.
- The HLE comparison changes model and harness at once; it is not a tier effect.
- Price/tier: no public price on any of the four pages (confirmed).
E201's 22 s run is NOT the Ultrafast tier: it uses Qwen 3.8 27B on Cerebras, not GPT-5.6 Sol. It changes several terms at once:
- model choice (a 27B open model) → price/tier;
- hardware decode speed → decode;
- the pre-built skill (fewer tool calls) → fewer passes N and smaller c_k;
- parallel independent checks → an overlap saving above 0.
The page itself says the comparison bundles changes to the model, the harness and the execution path. So the 22 s cannot be credited to any single term or to Ultrafast. With the claimed environment speedup inconsistent on the page (6.8 s vs 17.53 s), the environment share is unclear too.

**authors and venue:**

OpenAI: launch post (author 'OpenAI', 13 Aug 2026); changelog; community post by Sukhman Preet Singh Jawa (flagged staff, 13 Aug 2026). Cerebras: blog by Joyce Er (13 Aug 2026); blog by Sarah Chieng and Sherif Cherfa (24 Sep 2026). No peer review; vendor and hardware-partner marketing. The label 'not cited as evidence of task speed' stands. If Edwin wants a labelled vendor example of the environment term staying constant, the GDPval chart (6 tasks, mean wall-clock, same model and harness) is the best-specified of these numbers.

**formula:**

No formula in words. The GDPval chart presents total wall-clock = model-request (inference) time + non-inference time: 83.0 = 68.1 + 14.9 s, and 7.7 min = 7.5 min + 14.2 s. The 22 s chart presents total = model & orchestration + browser & API + other overhead (3.63 + 17.53 + 0.45 s). The HLE speedup is implicitly a ratio of total times. OpenAI's pages give none.
