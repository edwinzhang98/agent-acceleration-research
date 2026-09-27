# Evaluating Acceleration of Long-Horizon Web Agents: Literature Survey, Recommended Protocol, and API Budget (September 2026)

Recent agent-efficiency papers mostly report cost in dollars or tokens plus a single-run success rate, and rarely measure wall-clock time under controlled conditions or repeat runs. The strongest "lossless" claims (Speculative Actions, Speculate-with-Memory) use a construction guarantee: commit only on an exact action match, and speculate only on read-only actions.\[1\]\[2\]\[3\] They do not rely on a statistical equivalence test. A first paper can therefore stand out by combining both: a verifiable construction guarantee, plus a pre-registered paired non-inferiority test on per-field F1, run with 3 repeats over 25 tasks. At current (26 Sep 2026) list prices, the proposed 1,350-task-run design costs about **$2.4k–$7k for a frontier/mid/small trio at a medium 20k-input/400-output token profile** (with vs. without prompt caching). An all-top-tier trio (Fable 5.1 + GPT-6 Astra + Gemini Pro) costs about **$8k–$22k**, and up to about $43k in the high-token scenario.

## TL;DR
- **Evaluation practice is uneven.** HAL (about $40,000 total for 21,730 rollouts across 9 models and 9 benchmarks, with 2.5B tokens of LLM calls shared; one run per configuration) and "AI Agents That Matter" (5 runs, 95% t-CIs, cost- and time-accuracy Pareto frontiers) are the reference points for cost-aware evaluation. τ-bench's pass^k is the standard reliability metric, and cost-of-pass (Erol et al., ICLR 2026) is spreading (e.g., OPPO's Efficient Agents). Most acceleration papers still report one run, few report measured wall-clock time, and prices are often undated.
- **Recommended protocol.** Define "lossless" two ways. First, trajectory/answer equivalence to the unaccelerated baseline, guaranteed by verify-before-commit. Second, a pre-registered paired non-inferiority test on per-field F1 (for example, margin δ = 5 pp, one-sided α = 0.05, task-clustered paired bootstrap), reported with success rate, pass^k, wall-clock time, number of LLM calls, input/output/cached tokens, dollar cost at dated list prices, cost-of-pass, and Pareto plots.
- **Budget.** At ≈45,000 calls per model, per-model spend ranges from about $16 (GPT-6 Luna, low tokens, cached) to about $19k (Fable 5.1 / GPT-6 Astra, 40k-input, uncached). A realistic mixed trio costs about $2.4k–$6.9k at medium tokens. Acceleration conditions that cut calls by 30% lower the total by about 25%. Plan roughly 16 sequential days of agent time, or about 2 days with 10-way parallelism.

## Key Findings

1. **Cost is now routinely reported; wall-clock time and repeats are not.** HAL reports that its harness "automatically tracks token usage and costs" and cost $13 to over $450 per benchmark evaluation.\[4\]\[5\] However, a March 2026 follow-up by Franck Ndzomga notes that HAL "required roughly $40,000… despite considering at most two scaffolds per benchmark and only one run per scaffold–model configuration" (Efficient Benchmarking of AI Agents, arXiv 2603.23749). Efficient Agents reports pass@1 with no stated run count or error bars. Agentless reports one final run.
2. **"Lossless" is used in three very different senses.**
   - (a) *Construction-level equivalence*, where the actor's trajectory is identical to non-speculative execution. Examples: Speculative Actions (commit only when predictions match, plus guards and rollback) and Speculate-with-Memory (exact match of action type and all arguments, read-only whitelist).\[2\]\[3\]
   - (b) *Empirical "comparable accuracy"*, such as Efficient Agents' "96.7% of OWL's performance", which works out to 51.52% vs. 53.33% on GAIA, about 3 tasks.\[6\]
   - (c) *No claim at all*, only speedup plus accuracy.
   - No surveyed acceleration paper runs a formal non-inferiority or equivalence test on end-task quality.
3. **Headline numbers need auditing.** The subagent's reading of Efficient Agents found that the abstract's "$0.228" is the Level-1 cost (the overall cost is $0.285). It also found that "28.4%" is the cost reduction, not the cost-of-pass improvement (cost-of-pass 0.75→0.55 is ≈26.7%). This is a concrete reason to publish per-task logs and arithmetic.
4. **Pricing in Sept 2026 is volatile and tier-dependent.** Gemini 3.8 Flash's $0.75/$3.75 price is introductory "through December 31, 2026" and doubles on 1 Jan 2027.\[7\]\[8\] GPT-5.6 Sol's $4/$20 price is promotional "at least through November 21, 2026".\[9\]\[10\] Claude Sonnet 5's $2/$10 price became permanent. Anthropic's 4.7+ tokenizer "produces approximately 30% more tokens for the same text".\[11\] Dated price snapshots are therefore mandatory.

---

## Part 1 — Literature Survey

### 1.1 Survey table

| Paper (ID) | Year / venue | Domain | Benchmark & subset | Efficiency metrics | Quality metrics | "Lossless" definition / check | Runs & statistics | Reported budget |
|---|---|---|---|---|---|---|---|---|
| **AI Agents That Matter** — Kapoor, Stroebl, Siegel, Nadgir, Narayanan (arXiv 2407.01502) | 2024 arXiv; TMLR 2025 | Coding, web, QA | HumanEval (main); re-analysis of WebArena, HotPotQA, NovelQA | Total API cost (USD), inference time; accuracy–cost and accuracy–time Pareto curves with convex hull | Accuracy | N/A (argues simple baselines like retry/warming/escalation Pareto-dominate Reflexion, LDB, LATS) | **5 runs per agent**; 95% CIs via Student's t plus min/max for both accuracy and cost | Costs per agent in USD (exact totals not retrieved) |\[12\]\[13\]\[14\]
| **HAL: Holistic Agent Leaderboard** — Kapoor et al. (arXiv 2510.11977) | 2025 arXiv | Coding, web, science, customer service | 9 benchmarks incl. SWE-bench Verified, Online Mind2Web, GAIA, AssistantBench, τ-bench Airline, CORE-Bench Hard, USACO, SciCode, ScienceAgentBench | Token usage and dollar cost tracked automatically (Weave + LiteLLM); eval time "weeks to hours" via parallel VMs | Accuracy per benchmark; cost–accuracy frontiers | N/A | **One run per scaffold–model config** (per Ndzomga, arXiv 2603.23749) | **21,730 rollouts, 9 models, ≈$40,000 total**; $13 (ScienceAgentBench) to >$450 (Online Mind2Web) per evaluation |
| **Cost-of-Pass** — Erol, El, Suzgun, Yuksekgonul, Zou (arXiv 2504.13359) | 2025 arXiv; ICLR 2026 | LLM reasoning/knowledge (not agents) | MATH500, AIME 2024 and others | **Cost-of-pass** = expected $ cost per correct solution; frontier cost-of-pass incl. human-expert baseline | Accuracy | N/A | Not retrieved | Frontier cost-of-pass on MATH500 halved every ≈2.6 months (May 2024–Feb 2025); AIME every 7.1 months; inference-time techniques "typically increase the cost-of-pass" |
| **Efficient Agents** — OPPO (arXiv 2508.02694) | 2025 arXiv | General assistant / web | **GAIA dev (validation) set, levels 1–3**; 165 tasks inferred (53/86/26) from reported percentages | Cost-of-pass, $ cost, total tokens; prices "from official provider documentation as of May 2025" (prices not listed) | pass@1 accuracy | "Comparable performance": 51.52% vs. OWL 53.33% (reported as 96.7% retention) | **No run count, no std/CI** stated; appears single run | Per-task cost $0.285 (Efficient Agents) vs. $0.398 (OWL) vs. $3.104 (SmolAgents); cost-of-pass 0.55 vs. 0.75 vs. 5.82 |
| **Speculative Actions** — Ye, Ahuja, Liargkovas, Lu, Kaffes, Peng (arXiv 2510.04371) | 2025 arXiv; ICLR 2026 | Chess, e-commerce (τ-bench), multi-hop web search (HotpotQA), OS tuning | τ-bench e-commerce, HotpotQA, chess; OS setting (lossy) | Latency reduction (up to 20%), next-action prediction accuracy (up to 55%), cost–latency tradeoff model of speculative breadth | Final outcomes vs. sequential agent | **Construction guarantee**: "committing only when predictions match"; semantic guards, idempotent/reversible/sandboxed side effects, rollback; explicit lossy OS extension | Not retrieved | Cost–latency analysis; totals not retrieved |\[2\]
| **Speculate with Memory** — Li, Ye, Choubey, Zhang, Wu (Salesforce; arXiv 2607.12236) | 2026 arXiv | Web, embodied, planning, customer service, QA | **WebArena 812, VisualWebArena 910, ALFWorld 134 (valid_unseen), PDDL 60, τ²-bench 164 (retail+airline), HotpotQA 300** | Speculation hit accuracy; *estimated* latency reduction (each correct speculation hides one actor call): ALFWorld ≈28%→>50% | Actor trajectory unchanged | **"The actor's trajectory is identical to non-speculative execution"**; full exact match of action type and all parameters; static read-only whitelist | Actor trajectories collected once and **replayed**; n=3 speculator instances, best-of-k; **McNemar's test, p<0.001** | Actor GPT-5.4 / GPT-5-mini; speculator GPT-4.1-mini; totals not retrieved |\[3\]
| **LLMCompiler** — Kim et al. (arXiv 2312.04511) | ICML 2024 (PMLR 235) | Parallel function calling | HotpotQA, Movie Recommendation, ParallelQA, Game of 24 | Latency speedup (up to 3.7×; 1.80× HotpotQA), cost reduction (up to 6.7×), input/output tokens, $ at GPT pricing | Accuracy (up to ~9% better than ReAct) | Accuracy parity/improvement vs. ReAct; no formal equivalence | Not retrieved | Estimated $ from GPT pricing tables |\[15\]\[16\]\[17\]
| **AsyncLM** — Gim, Lee, Zhong (Yale; arXiv 2412.07017) | 2024 arXiv (preliminary) | Tool use | BFCL: 800 samples (v1-parallel + v2-parallel-live 400, v3-base-multi-turn 200, new v3-multi-step-parallel 200); 200 fine-tune / **600 eval** | End-to-end task latency: **1.6×–5.4×** vs. sync; up to 2.1× vs. sync-parallel | Call correctness held fixed | Ground-truth "cheat sheet" answers put in the prompt to keep generated calls consistent across latency runs | Error bars = 10th–90th percentile; cloud async latency **emulated** at 5 ms/output token | Not reported |
| **Agentless** — Xia, Deng, Dunn, Zhang (arXiv 2407.01489) | 2024 arXiv (v2) | SWE | **SWE-bench Lite, 300** | Avg. $ cost per issue ($0.70), avg. tokens (78,166) | Resolve rate 32.00% (96/300) | N/A | **Single final run**; greedy + temperature-0.8 sampling (40 patches/bug) | $0.70/issue (≈$210 total by our arithmetic; not stated in paper) |
| **OSWorld-Human** — Abhyankar, Qi, Zhang (arXiv 2506.16042) | ICML 2025 CUA workshop; MLSys 2026 oral | Computer use | OSWorld, all **369** tasks with human reference trajectories | End-to-end latency, per-step latency, prompt tokens, steps vs. human, **Weighted Efficiency Score (WES)** | Success | N/A | 16 agents analysed from public trajectories | Later steps take up to 3× longer than early ones; v1 (19 Jun 2025) reports "even the highest-scoring agents on OSWorld take 1.4−2.7× more steps than necessary" (v2 abstract says 2.7–4.3×, a version discrepancy) |
| **τ-bench** — Yao, Shinn, Razavi, Narasimhan (arXiv 2406.12045) | 2024 arXiv | Tool-agent-user | Retail, airline | — | Final DB-state match; **pass^k** (succeed on all k trials) | N/A | Multiple trials per task by design | gpt-4o succeeds on <50% of tasks |\[18\]
| **τ²-bench** — Barres, Dong, Ray, Si, Narasimhan (arXiv 2506.07982) | 2025 arXiv | Dual-control customer service | Telecom (+ retail/airline) | — | pass^k; Dec-POMDP with user tools | N/A | Multiple trials | — |\[19\]
| **Agentic Benchmark Checklist (ABC)** — Zhu et al. (arXiv 2507.02825) | NeurIPS 2025 | Benchmark methodology | 17 benchmarks used by top providers (Jan 2024–Mar 2025) | — | Task validity / outcome validity | — | Recommends reporting | SWE-bench Verified has insufficient tests; TAU-bench counts empty responses as success; errors up to 100% relative; ABC cut CVE-Bench overestimation by 33% |
| **Adding Error Bars to Evals** — Miller (Anthropic; arXiv 2411.00640) | 2024 arXiv | Eval statistics | — | — | — | — | CLT SEs, clustered SEs, resampling, **question-level paired differences**, power analysis; advises against lowering temperature to cut variance | — |
| **Mind2Web 2** — OSU NLP (arXiv 2506.21506) | NeurIPS 2025 (D&B) | Agentic/deep-research search | **130** long-horizon tasks, ≥1,000 h of human labour | — | **Agent-as-a-Judge** with tree-structured rubric; Extractor + Verifier per leaf criterion; correctness + source attribution | N/A | Not retrieved | Abstract: the best system, OpenAI Deep Research, "can already achieve 50-70% of human performance while spending half the time" |
| **Efficient Benchmarking of AI Agents** — Ndzomga (arXiv 2603.23749) | 2026 arXiv | Eval cost reduction | Terminal-Bench 2.0 (89 tasks × 5 attempts/agent, 101 agents) + 7 HAL benchmarks: "eight benchmarks, 33 agent scaffolds, and 70+ model configurations" | Task-subset selection to cut eval cost; mid-range (30–70% pass-rate) filter "reduces the number of evaluation tasks by 44–70%" | Rank preservation | — | Uses fractional success over 5 attempts | Cites HAL's ≈$40k as a barrier |
| **UI-CUBE** (arXiv 2511.17131) | 2025 arXiv | Enterprise computer use | 136 simple + 90 complex tasks | Steps vs. human, duration | Success | — | — | Agents need 1.5–3.3× more steps than humans on simple tasks, 1.2–2.1× on complex |\[20\]

Related 2025–2026 speculation work that we identified but whose metrics we did not verify: SpecHop (arXiv 2605.21965, multi-hop retrieval agents), SPORK self-speculative forking (arXiv 2607.03333), IdleSpec (arXiv 2605.22154), speculative tool calls (Nichols et al., arXiv 2512.15834), Interactive Speculative Planning (Hua et al., ICLR 2025), and DeltaSelect, which reports "score and recorded model cost for every completed evaluation" for A/B tests of coding agents (arXiv 2609.19607).\[21\]

### 1.2 Synthesis: common practice, best practice, gaps

**Metrics.** Dollar cost and tokens are now standard, driven by HAL and "AI Agents That Matter". Cost-of-pass has entered agent papers through Efficient Agents.\[6\] Speedup ratios dominate the systems-style papers (LLMCompiler, AsyncLM, Speculative Actions). Wall-clock time is the weakest link. AsyncLM *emulates* cloud latency,\[22\] and Speculate-with-Memory *estimates* latency by counting hidden actor calls instead of measuring end-to-end time.\[3\] Only OSWorld-Human and "AI Agents That Matter" treat time as a first-class Pareto axis. Number of LLM calls and step counts appear mostly in computer-use efficiency work (OSWorld-Human WES, UI-CUBE step ratios).\[20\]\[23\]

**Lossless.** The most defensible definition is the construction one used by Speculative Actions and Speculate-with-Memory: verify the speculated action (exact match on type and arguments) before commit, and restrict speculation to side-effect-free operations.\[2\]\[3\] That guarantees the committed trajectory equals the baseline trajectory *given the same actor outputs*. The guarantee does not cover end-to-end nondeterminism. Sampling variance, live-web drift, and timing-dependent page states can all change outcomes even when speculation is correct. Replaying fixed actor trajectories, as Speculate-with-Memory does, sidesteps this but does not measure it.\[3\] Quality-only claims ("comparable", "no significant drop") are typically single-run point comparisons with no margin and no test.

**Repeats and statistics.** Practice ranges from single runs (HAL, Agentless, apparently Efficient Agents), to 5 runs with t-based CIs ("AI Agents That Matter"), to per-step McNemar tests (Speculate-with-Memory).\[3\]\[12\]\[24\]\[25\] We found no acceleration paper that pre-registers a non-inferiority margin, clusters standard errors by task as Miller recommends, or reports pass^k for accelerated vs. baseline agents.

**Benchmarks and subsets.** Full sets appear where they are cheap or replayable (WebArena 812, VWA 910, SWE-bench Lite 300, OSWorld 369).\[3\]\[26\] Live-web benchmarks are the costliest: HAL's Online Mind2Web evaluation exceeded $450.\[4\]\[27\] Subsets are commonly justified by cost; the Efficient Benchmarking paper exists precisely because HAL's ≈$40k is "a barrier for independent researchers and small labs".\[25\]

**Budget reporting.** Totals are rare (HAL's ≈$40k is the exception). Per-task averages are common (Agentless $0.70, Efficient Agents $0.285).\[27\]\[28\]\[29\] Price dates are rarely stated; Efficient Agents' "as of May 2025" is a good example, but it still omits the actual prices.\[6\]

---

## Part 2 — Recommended Evaluation Protocol (per-field answer key, long-horizon web agents)

### 2.1 Design
- **Factors:** 25 tasks × 6 conditions (1 unaccelerated baseline + 5 acceleration variants/ablations) × 3 models × 3 repeats = 1,350 task-runs.
- **Pairing:** Every accelerated run is paired with the baseline on the same task, model, and repeat index. Where possible, use the same seed and the same environment snapshot.
- **Pre-registration:** Before running, record the non-inferiority margin, primary metric, analysis code, and exclusion rules (e.g., infra failures). Put them in the repo with a timestamp. This follows ABC's emphasis on reporting and "AI Agents That Matter"'s warning about the lack of holdout sets.

### 2.2 Metrics (use these names in the paper)
**Primary**
1. **Per-field F1** (micro over all fields, plus macro per task), with exact-match per field. Normalize values with a pre-declared normalizer (numbers, dates, casing, units). Where fields are free text, use an LLM or agent judge following Mind2Web 2's rubric-tree approach, and report judge–human agreement on a sample.\[30\]
2. **Wall-clock time** per task-run (end-to-end), plus per-step latency split into LLM time, environment time, and overlap/hidden time.

**Secondary**
- **Success rate** (all fields correct).
- **pass^k reliability** for k = 1..3 (probability all k repeats succeed) and pass@k.
- **Number of LLM calls** (actor and speculator/auxiliary counted separately).
- **Tokens**: input, output (including reasoning/thinking tokens), cached-read, and cache-write.
- **Dollar cost** at dated list prices.
- **Cost-of-pass** = mean cost per run ÷ success rate, and a field-level variant: cost per correct field.
- **Speedup ratio** (baseline time ÷ accelerated time, computed per pair and then aggregated as a geometric mean).
- Speculation hit rate and wasted-speculation cost.

**Pareto frontiers**
- Cost vs. per-field F1, and wall-clock time vs. per-field F1, per model.
- Show the convex hull as in "AI Agents That Matter".\[12\]

### 2.3 Defining and testing "lossless"
Use a two-tier claim:
- **Tier 1: construction losslessness (mechanism).**
  - Speculated actions commit only on an exact match of action type and all arguments with the actor's decision.\[3\]
  - Pre-launched actions are restricted to a read-only whitelist (navigation, GET-style fetches), as in Speculate-with-Memory.\[3\]
  - Every commit/rollback is logged.
  - Verify with a **trajectory-equivalence audit**: with actor outputs held fixed (replay mode, or temperature-0 cached responses), the committed action sequence and final answer must be byte-identical to the baseline for 100% of runs. Report any violations.
- **Tier 2: statistical non-inferiority (outcome, live execution).**
  - H0: F1_accel − F1_base ≤ −δ, with a pre-registered **δ = 5 pp** (or tighter).
  - Compute the task-level paired difference (average over the 3 repeats within each task and model).
  - Use a **paired bootstrap over tasks** (≥10,000 resamples; resample tasks, not runs, which matches Miller's clustering advice). Declare non-inferiority if the one-sided 95% lower bound exceeds −δ.
  - Also report **final-answer equivalence rate** (the share of paired runs whose field sets match exactly) and McNemar's test on success.
  - For "equivalent" (two-sided) claims, use TOST with ±δ.
- **Power check (planning arithmetic).** n ≈ ((z₀.₉₅ + z₀.₈₀)·σ_d/δ)² = ((1.645+0.84)·0.10/0.05)² ≈ 24.7. So **25 tasks give 80% power at δ = 5 pp only if the task-level paired SD σ_d ≤ 0.10.** Estimate σ_d from a pilot and report it. If σ_d is larger, widen δ honestly or add tasks.

### 2.4 Repeats and statistical reporting
- Report mean ± 95% CI over **3 repeats × 25 tasks** per model and condition. CIs come from the task-clustered bootstrap; also show the naive vs. clustered SE, following Miller.
- Give a per-model breakdown (never pool models for the headline claim), and apply Holm correction across the 5 accelerated conditions.
- Keep temperature fixed at the model default. Do not lower it just to reduce variance, per Miller. Record seeds where APIs support them, and record reasoning-effort settings.
- For time, report the median plus IQR and p90 in addition to the mean, because latency is heavy-tailed.

### 2.5 What to log (per call, per step, per run)
- **Per call:** request/response timestamps (send, first token, last token), model ID and **version snapshot string**, provider region/tier, token counts (input, cached-read, cache-write, output, reasoning), HTTP status, retries/429s with the retry-after value, and computed cost using a frozen price table.
- **Per step:** observation size (accessibility-tree or screenshot tokens), action, speculation prediction, hit/miss, commit/rollback, and environment latency.
- **Per run:** final field values vs. answer key, per-field correctness, total time, and environment snapshot hash.
- **Environment nondeterminism:** page-content hashes on each fetch, so that live-web drift can be detected and runs flagged.

### 2.6 Confound control
- **Environment:** Prefer replayable or self-hosted sites (a WebArena-style Docker stack, or a record-and-replay proxy for live sites), reset state before every run, and pin the browser version.
- **Model version pinning:** Use dated snapshot IDs (e.g., `claude-haiku-4-5-20251001`) and record the run dates.\[31\] Run baseline and accelerated conditions **interleaved in time** (randomized order within task), so provider load and drift affect both arms equally.
- **Rate limits and network:** Fix the concurrency level per condition and log 429s. Report wall-clock time both *including* and *excluding* rate-limit back-off. Run from one region and measure network RTT. Do not mix standard, fast, and priority tiers across conditions: OpenAI renamed Priority to "Fast mode" on 30 Jul 2026 at 2× price, and Anthropic's fast mode "has a dedicated rate limit".\[10\]\[32\]\[33\] Either tier changes latency.
- **Speculator overhead:** Count speculator calls and tokens in cost, even when they are "hidden" in time.

### 2.7 Budget reporting
- Report the total spend, per-model spend, per-condition spend, and per-task-run spend.
- Include a **frozen price table with retrieval date and URL**, plus the tokenizer caveat (Claude 4.7+ ≈30% more tokens).\[11\]
- Report how many runs were discarded or re-run and what they cost.
- Report pilot/debug spend separately.

### 2.8 Presentation
- **Table 1:** per model × condition, showing per-field F1 (±CI), success rate, pass^3, wall-clock median (IQR), speedup, LLM calls, tokens (in/cached/out), $ per run, and cost-of-pass.
- **Table 2:** the non-inferiority results (Δ F1, one-sided lower bound, δ, verdict) and trajectory-equivalence audit rates.
- **Figures:** cost-vs-F1 and time-vs-F1 Pareto plots per model with convex hulls, and a per-step latency breakdown (stacked LLM / env / hidden).

### 2.9 Checklist mapping
- **ABC (Zhu et al. 2025):** Ensure the answer key cannot be trivially satisfied (e.g., empty or default field values must score 0, cf. TAU-bench counting empty responses as success).\[34\] Validate the scorer on adversarial answers. Report benchmark limitations.
- **Miller (2024):** Use clustered SEs, paired differences, power analysis, and no temperature games.\[35\]\[36\]
- **Kapoor et al. (2024/2025):** Use cost-controlled comparison, accuracy–cost Pareto frontiers, simple strong baselines (e.g., a cheaper model alone, or retry), and standardized harness logging of tokens and cost.\[13\]\[14\]

---

## Part 3 — API Spend Estimate

### 3.1 Official list prices (USD per 1M tokens; retrieved 26 Sep 2026)

| Provider / model | Input | Cached input (read) | Cache write | Output | Source URL (retrieved 2026-09-26) |
|---|---|---|---|---|---|
| Anthropic Claude Fable 5.1 | $10 | $0.25 | $12.50 (5-min) | $50 | https://platform.claude.com/docs/en/about-claude/pricing.md |\[11\]
| Anthropic Claude Mythos 5.1 (limited availability, Project Glasswing) | $10 | $0.25 | $12.50 | $50 | same |\[11\]
| Anthropic Claude Opus 5.5 | $4 | $0.20 | $5.00 | $20 | same |\[11\]\[37\]
| Anthropic Claude Opus 5 | $5 | $0.50 | $6.25 | $25 | same |\[11\]\[38\]
| Anthropic Claude Sonnet 5 | $2 | $0.20 | $2.50 | $10 | same (introductory price made standard) |\[11\]
| Anthropic Claude Haiku 4.5 | $1 | $0.10 | $1.25 | $5 | same |\[11\]
| OpenAI gpt-6-astra | $10 | $1.00 | $12.50 | $50 | https://developers.openai.com/api/docs/pricing.md |\[10\]
| OpenAI gpt-6-sol | $2 | $0.20 | $2.50 | $10 | same |\[10\]\[39\]
| OpenAI gpt-6-luna | $0.10 | $0.01 | $0.125 | $0.50 | same |\[10\]
| OpenAI gpt-5.6-sol (promo ≥ 21 Nov 2026) | $4 | $0.40 | $5.00 | $20 | same |\[10\]
| OpenAI gpt-5.6-terra | $2 | $0.20 | $2.50 | $12 | same |\[10\]
| OpenAI gpt-5.4-mini | $0.75 | $0.075 | — | $4.50 | same |\[10\]
| Google Gemini 3.8 Flash (intro through 31 Dec 2026; $1.50/$7.50 from 1 Jan 2027) | $0.75 | $0.075 (+$0.50/1M tok/hr storage) | — | $3.75 | https://ai.google.dev/gemini-api/docs/pricing.md.txt |\[7\]
| Google Gemini 3.5 Flash | $1.50 | $0.15 | — | $9.00 | same |\[7\]
| Google Gemini 3.1 Pro (≤200K) | $2 | not verified | — | $12 | **Secondary only** (benchlm.ai/google/api-pricing); the official Pro row was not retrieved |\[8\]\[40\]
| Google Flash-Lite tier | conflicting: 3.5 Flash-Lite $0.30/$2.50 (BenchLM) vs. $0.15/$0.60 (aipricing.guru); 3.1 Flash-Lite $0.25/$1.50 | — | — | — | Secondary; **unverified** |\[8\]\[40\]\[41\]

Price modifiers from the same pages:
- OpenAI: long context (>272K) is billed at 2× input; Batch/Flex are 50% off; Fast mode is 2×.\[10\]\[32\]\[42\]
- Anthropic: US-only inference is 1.1×; the Batch API is 50% off; fast mode for Opus 5 is $10/$50.\[11\]\[38\]\[43\]
- Gemini: the Batch API is 50% off.\[7\]\[44\]

Batch pricing is unsuitable for interactive agent loops and for wall-clock measurement. DeepSeek, xAI, Mistral, and open-weight provider prices were **not retrieved** in this research and are excluded.

### 3.2 Token assumptions
| Scenario | Input tokens/call | Output tokens/call | Rationale |
|---|---|---|---|
| Low | 8,000 | 200 | Pruned accessibility tree, short history |
| Medium | 20,000 | 400 | Full AX tree + growing history |
| High | 40,000 | 600 | Screenshots/large DOM + long history |

**Cached variant:** We assume 80% of input tokens are prefix cache hits and 20% are new tokens written to cache at 1.25× base (Anthropic and OpenAI GPT-6/5.6). For Google, the 20% is billed at base and storage fees are ignored.
Effective cached input prices ($/1M):
- Fable 5.1: 0.8×0.25 + 0.2×12.50 = **2.70**
- Opus 5.5: 0.16 + 1.00 = **1.16**
- Sonnet 5: 0.16 + 0.50 = **0.66**
- Haiku 4.5: 0.08 + 0.25 = **0.33**
- GPT-6 Astra: 0.80 + 2.50 = **3.30**
- GPT-6 Sol: **0.66**
- GPT-6 Luna: 0.008 + 0.025 = **0.033**
- GPT-5.6 Sol: 0.32 + 1.00 = **1.32**
- Gemini 3.8 Flash: 0.06 + 0.15 = **0.21**
- Gemini 3.1 Pro: **0.56**, assuming a 10% cache rate (unverified)

### 3.3 Cost arithmetic (per call → per task-run [×100] → per model [×45,000 calls])

Per-call cost = input tokens × input price / 10⁶ + output tokens × output price / 10⁶.

| Model | Low uncached: call / run / model | Medium uncached | High uncached | Low cached (model) | Medium cached: call / model | High cached (model) |
|---|---|---|---|---|---|---|
| Fable 5.1 | 0.080+0.010 = $0.090 / $9.00 / **$4,050** | 0.20+0.02 = $0.220 / $22.00 / **$9,900** | 0.40+0.03 = $0.430 / $43.00 / **$19,350** | $1,422 | 0.054+0.02 = $0.074 / **$3,330** | $6,210 |
| GPT-6 Astra | $0.090 / $9.00 / **$4,050** | $0.220 / $22.00 / **$9,900** | $0.430 / $43.00 / **$19,350** | $1,638 | 0.066+0.02 = $0.086 / **$3,870** | $7,290 |
| Opus 5.5 | 0.032+0.004 = $0.036 / $3.60 / **$1,620** | 0.08+0.008 = $0.088 / $8.80 / **$3,960** | 0.16+0.012 = $0.172 / $17.20 / **$7,740** | $597.60 | 0.0232+0.008 = $0.0312 / **$1,404** | $2,628 |
| GPT-5.6 Sol | $0.036 / $3.60 / **$1,620** | $0.088 / $8.80 / **$3,960** | $0.172 / $17.20 / **$7,740** | — | 0.0264+0.008 = $0.0344 / **$1,548** | $2,916 |
| Gemini 3.1 Pro (secondary price) | 0.016+0.0024 = $0.0184 / $1.84 / **$828** | 0.04+0.0048 = $0.0448 / $4.48 / **$2,016** | 0.08+0.0072 = $0.0872 / $8.72 / **$3,924** | $309.60 | $0.016 / **$720** | $1,332 |
| Sonnet 5 | 0.016+0.002 = $0.018 / $1.80 / **$810** | 0.04+0.004 = $0.044 / $4.40 / **$1,980** | 0.08+0.006 = $0.086 / $8.60 / **$3,870** | $327.60 | 0.0132+0.004 = $0.0172 / **$774** | $1,458 |
| GPT-6 Sol | $0.018 / $1.80 / **$810** | $0.044 / $4.40 / **$1,980** | $0.086 / $8.60 / **$3,870** | $327.60 | $0.0172 / **$774** | $1,458 |
| Haiku 4.5 | 0.008+0.001 = $0.009 / $0.90 / **$405** | 0.02+0.002 = $0.022 / $2.20 / **$990** | 0.04+0.003 = $0.043 / $4.30 / **$1,935** | $163.80 | 0.0066+0.002 = $0.0086 / **$387** | $729 |
| Gemini 3.8 Flash | 0.006+0.00075 = $0.00675 / $0.675 / **$303.75** | 0.015+0.0015 = $0.0165 / $1.65 / **$742.50** | 0.03+0.00225 = $0.03225 / $3.225 / **$1,451.25** | $109.35 | 0.0042+0.0015 = $0.0057 / **$256.50** | $479.25 |
| GPT-6 Luna | 0.0008+0.0001 = $0.0009 / $0.09 / **$40.50** | $0.0022 / $0.22 / **$99** | $0.0043 / $0.43 / **$193.50** | $16.38 | $0.00086 / **$38.70** | $72.90 |

### 3.4 Totals for model trios (1,350 task-runs, 135,000 calls)

| Trio | Low uncached | **Medium uncached** | High uncached | Low cached | **Medium cached** | High cached |
|---|---|---|---|---|---|---|
| A. Anthropic ladder: Opus 5.5 + Sonnet 5 + Haiku 4.5 | $2,835 | **$6,930** | $13,545 | $1,089 | **$2,565** | $4,815 |
| B. Cross-vendor frontier/mid/small: Opus 5.5 + GPT-6 Sol + Gemini 3.8 Flash | $2,733.75 | **$6,682.50** | $13,061.25 | $1,034.55 | **$2,434.50** | $4,565.25 |
| C. All top-tier: Fable 5.1 + GPT-6 Astra + Gemini 3.1 Pro | $8,928 | **$21,816** | $42,624 | $3,369.60 | **$7,920** | $14,832 |
| D. Practical frontier: Opus 5.5 + GPT-5.6 Sol + Gemini 3.1 Pro | $4,068 | **$9,936** | $19,404 | — | **$3,672** | $6,876 |
| E. Budget: Haiku 4.5 + GPT-6 Luna + Gemini 3.8 Flash | $749.25 | **$1,831.50** | $3,579.75 | $289.53 | **$682.20** | $1,281.15 |

### 3.5 Sensitivity
- **Acceleration reduces calls.** 100 calls/task is the baseline upper bound. Suppose the 5 accelerated conditions average 30% fewer actor calls. Calls then fall to 25×3×3×(100 + 5×70) = 101,250, which is 75% of the upper bound: medium-uncached Trio B goes from $6,682.50 to ≈$5,012. If accelerated conditions average 50% fewer calls, the total falls to 58.3% (≈$3,898). **Speculator calls add back cost.** For example, a GPT-6 Luna speculator on every step at medium tokens adds ≈$0.0022 per step, about $0.22 per task-run.
- **Tokenizer.** If the token assumptions are measured with a non-Claude tokenizer, Claude 4.7+ models may bill ≈30% more tokens.\[11\]\[45\] Trio A medium uncached would then rise from $6,930 to ≈$9,009.
- **Reasoning tokens.** Opus 5.5 "thinking can't be disabled" and thinking is billed as output.\[37\]\[38\] At 2,000 output tokens per call instead of 400, Opus 5.5 medium rises from $0.088 to $0.120 per call, i.e. +$1,440 per model.
- **Price expiry.** Gemini 3.8 Flash doubles on 1 Jan 2027, and GPT-5.6 Sol's promo runs "at least through November 21, 2026".\[7\]\[10\] Finish runs before those dates or re-price.
- **Contingency.** Add 20–30% for pilots, re-runs after infra failures, and judge-model calls (if an LLM judge scores free-text fields).

### 3.6 Wall-clock and rate limits
- **Assumption:** ≈10 s per step (LLM + browser). This fits the published timings. OSWorld-Human (Abhyankar, Qi, Zhang, arXiv 2506.16042) reports that changing the line spacing of two paragraphs "takes 12 minutes for a computer-use agent" when it "should take under 30 seconds", with planning and reflection calls taking "75% to 94% of the total latency". Speculative Actions' Table 1 (arXiv 2510.04371v2) estimates 10–20 min for OS tasks, 5–30 min for Deep Research, 30–45 min for data pipelines, and 1 hour for a Kaggle chess game.
- At 100 steps, that is ≈17 min per task-run. 1,350 task-runs take ≈382 h sequential, ≈16 days. With 10 concurrent workers it is ≈1.6 days, and ≈4 days if runs are split by condition.
- **Throughput needed:** At medium tokens with 10 concurrent runs at ~6 calls/min each, you need about 60 requests/min and ≈1.2M input tokens/min per provider. Check your organization's tier limits before starting. We did not retrieve per-tier RPM/TPM tables.
- **Tier choice:** Use one tier consistently. Anthropic's fast mode returns 429 with retry-after on its separate limit. OpenAI's Fast mode costs 2×. Gemini has Standard/Flex/Priority tiers.\[10\]\[33\]\[44\] Mixing tiers would confound wall-clock comparisons.

## Caveats
- Several numbers come from secondary sources and are flagged in place:
  - The official Gemini Pro and Flash-Lite pricing rows were not retrieved.
  - The Mind2Web 2 performance figure is the relative claim from its abstract (50–70% of human performance); we did not verify absolute success rates.
  - The OSWorld-Human step-ratio range differs between paper versions.
  - Agentless v1 figures (≈27.33%, ≈$0.34) are unverified; this report uses v2 ($0.70, 32.00%).
- Efficient Agents' task count (165) is inferred from its percentages, and its reported costs are internally inconsistent across tables.
- Run counts and budgets for Cost-of-Pass, Speculative Actions, and LLMCompiler were not retrieved; "not retrieved" means unknown, not "none".
- All cost estimates assume the per-call token profiles above. Measure real per-call tokens in a 1-task pilot per model, then re-run the Section 3.3 arithmetic. Actual accessibility-tree sizes vary by more than 5× across sites.

## Sources

1. [\[2510.04371\] Speculative Actions: A Lossless Framework for Faster Agentic Systems](https://arxiv.org/abs/2510.04371)
2. [Speculative Actions: A Lossless Framework for Faster Agentic Systems](https://arxiv.org/html/2510.04371)
3. [Speculate with Memory: Lossless Acceleration for LLM Agents](https://arxiv.org/html/2607.12236)
4. [Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation | alphaXiv](https://www.alphaxiv.org/abs/2510.11977)
5. [Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation](https://arxiv.org/html/2510.11977.pdf)
6. [Efficient Agents: Building Effective Agents While Reducing Cost](https://arxiv.org/html/2508.02694v1)
7. <https://ai.google.dev/gemini-api/docs/pricing.md.txt>
8. [Gemini API Pricing (September 2026): Model & Token Costs | BenchLM.ai](https://benchlm.ai/google/api-pricing)
9. [OpenAI API Pricing (September 2026): Model & Token Costs | BenchLM.ai](https://benchlm.ai/openai/api-pricing)
10. <https://developers.openai.com/api/docs/pricing.md>
11. [--- title: Pricing url: https://platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing.md)
12. [AI Agents That Matter](https://arxiv.org/pdf/2407.01502)
13. [AI Agents That Matter — Lacuna](https://lacuna.tiptreesystems.com/work/ai-agents-that-matter/wrk_5fadaa13ed8be20303ff07ad592a452f)
14. [\[2407.01502\] AI Agents That Matter](https://arxiv.org/abs/2407.01502)
15. [\[Quick Review\] An LLM Compiler for Parallel Function Calling](https://liner.com/review/llm-compiler-for-parallel-function-calling)
16. [An LLM Compiler for Parallel Function Calling](https://arxiv.org/pdf/2312.04511)
17. [An LLM compiler for parallel function calling | Proceedings of the 41st International Conference on Machine Learning](https://dl.acm.org/doi/abs/10.5555/3692070.3693047)
18. [τ-bench: Tool-Agent-User Interaction Benchmark](https://www.emergentmind.com/papers/2406.12045)
19. [Tau2-Bench: Multi-Domain Benchmark Suite](https://www.emergentmind.com/topics/tau2-bench)
20. [UI-CUBE: Enterprise-Grade Computer Use Agent Benchmarking Beyond Task Accuracy to Operational Reliability](https://arxiv.org/pdf/2511.17131)
21. [DeltaSelect: Affordable A/B Testing for Coding Agents](https://arxiv.org/pdf/2609.19607)
22. [1Introduction](https://arxiv.org/html/2412.07017v1)
23. [1 Introduction](https://arxiv.org/html/2506.16042v2)
24. <https://arxiv.org/pdf/2407.01489>
25. [Efficient Benchmarking of AI Agents](https://arxiv.org/html/2603.23749v1)
26. [OSWorld-Human: Benchmarking the Efficiency of Computer-Use Agents](https://arxiv.org/pdf/2506.16042)
27. [Agentless : Demystifying LLM-based Software Engineering Agents](https://arxiv.org/html/2407.01489v2)
28. <https://arxiv.org/pdf/2508.02694>
29. [\[2510.11977\] Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation](https://arxiv.org/abs/2510.11977)
30. [Mind2Web 2: Evaluating Agentic Search with Agent-as-a-Judge](https://openreview.net/pdf/4ea1b7f691ba5c571c395a674a6d7997b5aa32be.pdf)
31. [Claude API Pricing (September 2026): \$1–\$50 per 1M Tokens | BenchLM.ai](https://benchlm.ai/anthropic/api-pricing)
32. [OpenAI ChatGPT API Pricing Calculator (Sep 2026)](https://costgoat.com/pricing/openai-api)
33. [Fast mode (research preview) - Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/fast-mode)
34. [\[2507.02825\] Establishing Best Practices for Building Rigorous Agentic Benchmarks](https://arxiv.org/abs/2507.02825)
35. [Adding Error Bars to Evals:](https://arxiv.org/pdf/2411.00640)
36. [Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations](https://arxiv.org/html/2411.00640v1)
37. [Claude Opus 5.5 - Claude Platform Docs](https://platform.claude.com/docs/en/models/opus-5-5/overview)
38. [What's new in Claude Opus 5 - Claude Platform Docs](https://platform.claude.com/docs/en/models/opus-5/whats-new-opus-5)
39. [OpenAI releases GPT-6 Sol and Luna models, slashing API costs 50% or more | VentureBeat](https://venturebeat.com/technology/openai-releases-gpt-6-sol-and-luna-models-slashing-api-costs-50-or-more)
40. [Gemini API Pricing Calculator & Cost Guide (Sep 2026)](https://costgoat.com/pricing/gemini-api)
41. [Google AI Pricing: Gemini API & WeatherNext Costs](https://www.aipricing.guru/google-ai-pricing/)
42. [GPT-6 Sol Model | OpenAI API](https://developers.openai.com/api/docs/models/gpt-6-sol)
43. [Claude API Pricing 2026: Rates, Cost Examples & Credits | Credit for Startups](https://creditforstartups.com/pricing/claude-api-pricing)
44. [Gemini API optimization and inference | Google AI for Developers](https://ai.google.dev/gemini-api/docs/optimization)
45. [What's new in Claude Sonnet 5 - Claude Platform Docs](https://platform.claude.com/docs/en/models/sonnet-5/whats-new-sonnet-5)
