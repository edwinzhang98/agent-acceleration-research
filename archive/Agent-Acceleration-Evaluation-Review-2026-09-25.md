**Evaluating agent acceleration: evidence and a practical protocol**

Research cutoff: September 25, 2026. Sources were checked on September 26, 2026. This is a targeted primary-source review, not an exhaustive systematic review. NR means not reported in the inspected paper/version, not zero. All dollar figures are USD.

The strongest evaluation treats correctness, wall-clock time, and total cost as joint outcomes. The literature contains useful precedents, but many “same performance” claims rely on single-run point estimates. A 25-task experiment can establish a useful workload-specific speedup; it cannot, by itself, establish a narrow accuracy-preservation guarantee across web workflows.

**What representative papers actually report**

| Paper / version | Benchmark and subset | Metrics and correctness claim | Repetitions and statistical reporting | Reported resources or spending |
|---|---|---|---|---|
| [AI Agents That Matter](https://arxiv.org/html/2407.01502v1), 2024 | HumanEval 164; HotPotQA 100 optimization + 200 evaluation examples; NovelQA case study | Accuracy–dollar Pareto frontiers; API-call time; fixed optimization vs variable inference cost. Maintaining accuracy is empirical. API-call time is not necessarily full task wall time. | Five evaluation runs for HumanEval/HotPotQA; Student-t 95% CIs and min–max. CIs exclude optimization/resampling uncertainty. NovelQA once due cost. | API-only inference; total project bill NR. Example HotPotQA joint optimization: fixed $2.714 and $0.174 per 100 inferences for GPT-3.5. |
| [τ-bench](https://arxiv.org/html/2406.12045v1), 2024 | 115 retail + 50 airline tasks | Final database state plus required answer content; pass^1, pass^k, pass@k. Final-state reward can miss policy violations. | Main table: at least three trials/task; 30-action cap. Reliability curves through k=8, but exact n for those curves not located. Construction validation used >40 GPT-4-turbo trials per retail task. No CIs located. | GPT-4o retail agent $0.38/task plus user simulator $0.23/task. Whole-study spend NR. Separate “~$200 per trial” wording is not reconciled with these components. |
| [Agent Workflow Memory](https://arxiv.org/html/2409.07429v1), 2024 | WebArena 812; Mind2Web cross-task/site/domain | Task SR and steps; Mind2Web element accuracy/action F1/step SR. WebArena matched accessibility-tree baseline: 15.0→35.5% SR and 7.9→5.9 steps. No strict lossless claim. | Temperature zero; repeated benchmark runs, CIs and tests NR. Online memory depends on earlier tasks. | Total spend NR. Action-step reduction does not count all workflow induction and trajectory-evaluation calls. |
| [Interactive Speculative Planning](https://proceedings.iclr.cc/paper_files/paper/2025/file/25458943db16e0f78f748ca5bc34fff6-Paper-Conference.pdf), ICLR 2025 | OpenAGI 117; TravelPlanner validation 180 | Total/stepwise generation time, tokens, peak concurrent API calls, dollars. OpenAGI MAD example: 182.70→105.42 seconds, but $0.2160→$0.2973 per plan. This is planning-time acceleration, not necessarily full browser-task latency. | Dataset means/variation; main evaluation repeat count NR. Five simulations apply to user-interruption experiments, not whole-benchmark replication. | Per-plan costs reported; total project spend NR. Exact action verification on OpenAGI; fuzzy parameter verification on TravelPlanner explicitly removes the identical-result guarantee. |
| [Efficient Agents](https://arxiv.org/html/2508.02694v1), 2025 | GAIA full 165-item development set, three difficulty levels | Accuracy, tokens, dollars, cost-of-pass. Table 7: OWL 53.33%, $0.398, 189K tokens; proposed system 51.52%, $0.285, 127K. This accepts a quality tradeoff. | Repeats/CIs NR; no prespecified noninferiority margin. | Total study spend NR. Abstract's $0.228 is the level-1 figure, not overall. Table 7 supports 28.4% per-attempt cost reduction; rounded CoP .75→.55 implies about 26.7% reduction. |
| [HAL](https://arxiv.org/html/2510.11977v1), 2025 | Nine benchmarks; 21,730 rollouts across nine models | Accuracy, tokens, dollar costs and Pareto frontiers; full traces for behavioral audits. | Most configurations single-run without statistical validation, explicitly because repetitions were too expensive. | Approximately $40,000 total compute; 2.5B logged LLM tokens. This is reported aggregate spending. |
| [OSWorld-Human](https://arxiv.org/html/2506.16042v2), 2025 / MLSys 2026 v2 | Profiling on 39 tasks with Agent S2/GTA1; separate analysis of released trajectories for 16 agents on 369 tasks | Wall-clock phases, per-call tokens/cost, steps, success, human-referenced Weighted Efficiency Score. It diagnoses inefficiency, rather than demonstrating a lossless intervention. | Repeat count NR; reported ± quantities not clearly identified as SD/SE in inspected text. Do not confuse the 16-agent trajectory collection with repeated experiments. | Grounding on one NVIDIA A6000/SGLang. Whole-study spend NR. Version 1 used 37 tasks; do not mix versions. Dollar aggregates in v2 are internally unclear, so not used here. |
| [AgentDiet](https://arxiv.org/html/2509.23586v2), FSE 2026 | 100 separate tuning cases; 200 held-out SWE-bench Verified; all 300 Multi-SWE-bench Flash | Input/output tokens; actor and compressor costs; pass rate; mean steps for all/successful tasks. 39.9–59.7% fewer input tokens; 21.1–35.9% lower total cost. | Repeats/CIs/noninferiority test NR. Reported SR changes −1 to +2 pp. “Same performance” is a point-estimate claim. Explicitly avoids quantitative latency comparison because commercial API latency is unstable. | Approximately $2,000 LLM expenditure. Cost accounting includes compressor calls and cache effects. |
| [Cost-of-Pass](https://arxiv.org/html/2504.13359v2), 2025 / February 2026 revision | Up to 128 items per reasoning/QA dataset; agent extension uses 8 airline + 8 retail τ-bench tasks | Expected taskwise cost per correct solution and frontier cost-of-pass; all turns billed for agents. | Eight attempts/model/item in main evaluation; four trials for agent extension. 95% bootstrap percentile CIs with 10,000 samples for frontier estimates. | Whole-study spend NR. Human wage comparisons are estimated costs, not paid study expenditure. |
| [PASTE / Act While Thinking](https://arxiv.org/html/2603.18897v1), March 2026 | DeepResearchBench, SWE-bench, ScholarQA; exact subset counts NR | Arrival-to-final-response latency, p95/p99, throughput, tool stalls/overlap, speculation hit rate, resource overhead. Up to 48.5% mean latency reduction; up to 48.6%/61.9% p95/p99 reduction. | Repetitions/CIs NR. Audit of >20,000 speculative actions: 602 potentially side-effecting actions blocked; no differing final task results observed. This supports correctness but is not a statistical equivalence test. | Four nodes, 32 A100 80GB GPUs; GPT-5.2/Gemini 2.5 Pro APIs and local Qwen model. GPU-hours/total API bill NR. Hardware inventory is not consumed compute. |
| [Are Online Skill and Memory Modules Always Worth Their Tokens?](https://arxiv.org/html/2606.15017v1), June 2026 | WebArena Shopping 187 + Reddit 106 + Admin 182 = 475; WorkArena-L1 33 task types, three seeds/type | Success, total actor plus auxiliary tokens, component breakdown, Any-of-3/All-of-3. Strong budget-aware baseline. Matching budgets by 10 vs 15 actor steps is explicitly approximate. | Three independent WebArena runs per domain/model; mean±SD. WorkArena three seeds/type. Reports task-level instability. | Total bill NR. Gemini 3 Flash example: Vanilla-IB 50.74%/71.9K tokens vs ASI 47.86%/107.1K. Scope is online augmentation, not every offline skill method. |
| [PreAct](https://arxiv.org/html/2606.17929v1), June 2026 | AndroidWorld 15; OSWorld 6; WebArena shopping_admin 12 | Paired cold/warm success, latency, tokens, replay coverage, compile/verification overhead. 8.5–13× applies to served WebArena replays, not unconditional task speedup. | Main Android comparison three seeds; gate studies five Android/OSWorld repetitions and four per Web condition; means±SD, sign tests. Verify-after-reset rejects programs that execute but fail the evaluator. | Approximately $30–35 LLM spend and 50 container-hours. Verify-replay adds median +162% Android/+217% OSWorld overhead per successful compilation cycle. Small subsets and seen-task reuse limit generalization. |

HAL's exact benchmark coverage is important when comparing its budget with a smaller project: AssistantBench 33/214; CORE-Bench Hard 45-paper public test set; GAIA 165 validation tasks; Online Mind2Web 300 tasks/136 sites; SciCode 65 main problems/338 subproblems; ScienceAgentBench 102; SWE-bench Verified Mini 50; τ-bench Airline 50; USACO 307. These were heterogeneous evaluations, not one uniform replicated factorial design. [HAL Appendix A10](https://arxiv.org/html/2510.11977v1)

Two additional methodological examples are worth keeping in the reading list:

- [On the Reliability of Computer Use Agents](https://arxiv.org/html/2604.17849v1), April 2026: 361 OSWorld tasks, generally three repetitions, pass^1/pass^3, paired McNemar tests on consistently solved tasks and Wilcoxon tests on per-task success counts. Total study spend NR.
- [Speculate with Memory](https://arxiv.org/html/2607.12236v1), July 2026: replay on WebArena 812, VisualWebArena 910, ALFWorld 134, PDDL 60, τ²-bench 164 and HotpotQA 300. Main metric is speculation prediction accuracy. For Types 1/2, “three” means parallel speculators in one run; Type 3 uses three task orderings. Reports mean±SD and step-level McNemar tests. Limited live timing is converted to analytical speedups; §4.3 and Appendix B.4 are inconsistent about live evaluation. Do not describe this as six-benchmark measured wall-clock acceleration. Whole-study bill NR.

**What “lossless” should mean**

Three different claims should remain separate:

1. Behavioral preservation by construction: authoritative model decisions remain unchanged, speculative results are accepted only under exact validation, and incorrect work cannot alter externally visible state. State the assumptions, including deterministic/replayable observations, isolation, cache freshness and resource contention. ISP's exact OpenAGI verification is a useful example; its fuzzy TravelPlanner verification explicitly loses the identical-result guarantee.
2. Statistical noninferiority: task success or field accuracy may differ, but a prespecified one-sided confidence bound excludes degradation beyond an acceptable margin. This is “noninferior within X percentage points,” not literal losslessness.
3. No observed degradation: equal or slightly improved point estimates. This does not establish either of the previous claims. A nonsignificant difference is not evidence of equivalence.

A replay completing every action is not proof that the requested fields are correct. PreAct documents cases with 100% coverage but evaluator score zero. Conversely, equal final answers do not prove the same policy compliance or absence of unwanted side effects. A web-agent answer key should therefore check both requested values and state invariants.

**Recommended protocol for the proposed first paper**

The following is a recommendation, not a claim that all papers above follow it.

1. Freeze the tasks and evaluator before the main run. Use 25 held-out tasks spanning several workflow families and a range of horizons, with separate development tasks. Publish task IDs, application snapshot, required fields, reference values, expected primitive-action lengths and inclusion/exclusion rules. Select tasks by a documented sampling/stratification process rather than selecting only baseline successes. Split task templates/workflow families to prevent near-duplicate leakage.

2. Make the per-field key the main correctness advantage. Define field normalization in advance: exact identifiers, canonical dates/units, tolerance for numeric fields and order rules for lists. Use deterministic scoring wherever possible. Macro field accuracy first averages fields within a task, then tasks, so a form with 100 easy fields does not dominate one with five difficult fields. Also report strict task success: every required field correct, all required actions committed and all invariants satisfied. Report missing, incorrect, extra and critical-field errors separately. Keep test keys outside agent-accessible storage and out of memory creation, routing and verifier prompts. An oracle-key-assisted variant is an upper bound, not the deployable method.

3. Keep the six conditions and three repeats controlled. A useful allocation is unchanged agent, simple batched-action baseline, full method, and three algorithm-specific ablations selected before evaluation. Hold actor snapshot, tool access, observation format/resolution, reasoning budget, retries and maximum wall time fixed except where the intervention explicitly changes them. Randomize/interleave conditions within task/model/time blocks. Identical seeds do not guarantee identical hosted-model randomness. Reset application state before each trial.

4. Separate cold-start, seen-workflow reuse and unseen-workflow transfer. If skills or caches are created from prior executions, start each independent repetition from the same corpus state. Charge learning/compilation/verification costs. Report deployment cost after N uses as C_build + N*C_run and the break-even reuse count. A warmed repeated-task result is not evidence of unseen-task generalization. Additional cold/warm experiments beyond the six defined conditions must be added to the budget.

5. Instrument the whole system, not just the actor.

| Measurement | Recommended definition/reporting |
|---|---|
| End-to-end wall time | Request accepted to final committed state/answer. Mean, median, p90/p95; show uncertainty and tail sample counts. With only 75 episodes/condition/model, tail estimates are unstable. |
| Success within time | Fraction correctly completed by each elapsed-time threshold. For a complementary deadline-adjusted time metric, assign failures the common deadline H. This prevents fast failures appearing as wins. |
| Model calls | Separate actor/planner, draft, verifier, compressor, memory builder and retry calls; total physical calls and critical-path sequential depth. |
| Environment actions | Primitive browser actions, tool RPCs, screenshots and observations; distinguish several actions in one tool call from several tool calls in one model response. |
| Tokens | Per-model input, cache read/write, visible output, billable reasoning and image usage. Save raw provider usage to allow repricing. |
| Dollars | All attempts, failed branches, retries, auxiliary models and separately tool/search/VM charges. Publish list-price-normalized and actual paid amounts if credits/discounts differ. |
| Reliability | pass^1, pass^3 (all three pass), pass@3 (any of three passes), per-task outcome matrix. pass@3 is oracle-observed coverage unless a deployable verifier can choose the correct attempt. |
| Quality–efficiency | Success vs dollars; success vs wall time; field accuracy vs dollars; cost/latency at matched quality. Mark dominated points and display CIs. |
| Mechanism | Acceptance/cache hit/fallback rates, wasted speculative work, call reduction, context growth, phase timings and side-effect/invariant violations. |

For serial execution, phase totals help explain latency. For asynchronous execution, use a timestamped critical-path trace; summing overlapping call durations overstates end-to-end time. Log client-side model request duration, time-to-first-token if available, tool time, observation processing and rate-limit waiting. Do not call these server-side prefill/decode measurements unless the provider exposes them.

The pooled metric

dollars per successful completion = total dollars spent on all attempts / number of successful attempts

is useful, but differs from the taskwise Cost-of-Pass quantity average_i(C_i/p_i). With only three trials, individual p_i estimates are too unstable for credible inverse-probability estimates; zero observed successes must not be silently dropped. Use the clearly named pooled ratio, task-clustered uncertainty and success rate side by side. If no successes occur, report the ratio as undefined/infinite.

6. Predeclare inference and claim thresholds. Make full method vs unchanged baseline the three primary comparisons, one per model. Resample task IDs jointly across methods/models/repeats (e.g., 10,000 paired cluster-bootstrap samples); never treat fields, steps or the 1,350 runs as independent tasks. Report mean paired differences and 95% intervals, per-task regressions and discordant pairs. Use prespecified multiple-comparison control for the primary claims; treat other ablations as exploratory or define a separate family. If claiming noninferiority, require the lower one-sided bound to exceed -delta, where delta is justified before results. Illustrative margins are 2 pp strict task success and 1 pp macro field accuracy; both quality gates must pass. Report latency/cost improvement separately.

The 25-task design is a pilot-sized generalization test. Even zero observed regressions in 25 independent task draws leaves a one-sided 95% binomial upper bound of 1 - 0.05^(1/25) = 11.3% on the chosen task-level regression event. Under the same simplified independent-event model, zero regressions would require 149 independent tasks to put that upper bound below 2%. This is not a power calculation for the proposed paired success-rate test. Repeats and correlated fields cannot substitute for independent tasks. Identical paired outcomes can also make an empirical bootstrap interval degenerate; that does not prove zero unseen-task risk. If the 25 tasks are handpicked, intervals do not repair selection bias.

The best next expenditure is more held-out tasks for baseline vs full method, after retaining three repeats across the six pilot conditions. A defensible paper claim is “X× faster and Y% cheaper on this task distribution, with estimated quality difference Δ and interval [L,U].” Use “lossless” only for a rigorously delimited preservation mechanism or clearly state that it means no observed degradation.

7. Handle failures transparently. Apply identical deadlines; count timeouts as failures and retain their time/cost. Report all-attempt and success-conditioned latency, plus success-within-time curves. A common-success subset is a useful diagnostic but is selected after treatment. Predefine when infrastructure failures are rerun, preserve both records, and report sensitivity with/without them. Do not rerun only unfavorable agent outcomes.

8. Release reproducibility artifacts. Include scorer code/tests, task manifests, model/provider/version, evaluation dates, reasoning settings, prompts, environment/container versions, task-order seeds, raw traces, usage ledger and aggregate analysis. Publish the actual full-project spend including unsuccessful development experiments. Distinguish API bills, hardware inventory, GPU-hours and human annotation labor.

**September 2026 API budget**

The factorial design is:

25 tasks × 6 conditions × 3 models × 3 repeats = 1,350 episodes.
At 100 model calls per episode: 135,000 calls total, or 45,000 calls per model.

One hundred calls must include auxiliary calls if the following estimates are meant to cover the complete agent. If it means 100 actor calls plus draft/compressor/verifier calls, add those separately.

Selected standard online list prices, USD per million tokens:

| Model | Ordinary input | Cache read | Cache write | Output |
|---|---:|---:|---:|---:|
| GPT-6 Astra | 10.00 | 1.00 | 12.50 | 50.00 |
| GPT-6 Sol | 2.00 | 0.20 | 2.50 | 10.00 |
| GPT-6 Luna | 0.10 | 0.01 | 0.125 | 0.50 |
| Claude Sonnet 5 | 2.00 | 0.20 | 2.50 (5-minute) | 10.00 |
| Claude Opus 5.5 | 4.00 | 0.20 | 5.00 (5-minute) | 20.00 |
| Claude Haiku 4.5 | 1.00 | 0.10 | 1.25 (5-minute) | 5.00 |
| Gemini 3.5 Flash-Lite | 0.30 | 0.03 | Ordinary input plus applicable storage | 2.50 |

Sources: [OpenAI prices](https://developers.openai.com/api/docs/pricing), [OpenAI dated changelog](https://developers.openai.com/api/docs/changelog), [OpenAI cache accounting](https://developers.openai.com/api/docs/guides/prompt-caching), [Anthropic prices](https://platform.claude.com/docs/en/about-claude/pricing), [Anthropic dated release notes](https://platform.claude.com/docs/en/release-notes/overview), [Google prices](https://ai.google.dev/gemini-api/docs/pricing), [Google dated release notes](https://ai.google.dev/gemini-api/docs/changelog).

The OpenAI rows use prompts at or below 272K input tokens; longer prompts have higher rates. Anthropic one-hour writes cost more than the five-minute rates above. Gemini explicit caching has storage charges ($1 per million token-hours for Flash-Lite). These are standard online rates, not batch, fast/priority or negotiated prices. Dated sources establish availability before the cutoff: Astra September 3; Sol/Luna September 22; Opus 5.5 September 22; Sonnet 5's $2/$10 became permanent August 10; Flash-Lite 3.5 reached GA July 21.

A practical comparison is Sol + Sonnet 5 + Luna. Replacing Sol with Astra is a more expensive flagship validation. Alternatively, replacing Luna with Flash-Lite gives three-provider coverage.

The estimates below assume 500 TOTAL billable output tokens per call, including reasoning. Input counts include repeated context and token-equivalent image usage as billed by each model. The “80% cache” scenario means 80% of aggregate input is billed as cache reads and 20% as cache writes; these are disjoint categories and writes include cache population. It is a sensitivity assumption, not a measured hit-rate forecast.

| Average input tokens/call | Sol + Sonnet 5 + Luna: no cache | Same: 80% reads / 20% writes | Astra + Sonnet 5 + Luna: no cache | Same: 80% reads / 20% writes |
|---|---:|---:|---:|---:|
| 5,000 | $1,383.75 | $765.68 | $4,083.75 | $2,259.68 |
| 20,000 | $4,151.25 | $1,678.95 | $12,251.25 | $4,954.95 |
| 50,000 | $9,686.25 | $3,505.50 | $28,586.25 | $10,345.50 |

For each model m, with 45,000 calls, average input I and output O:

C_m = 45,000 / 1,000,000 × [I_u P_input + I_r P_read + I_w P_write + O P_output],
where I_u + I_r + I_w = I.

At 20K input/500 output, the practical mix splits into $2,025 Sol + $2,025 Sonnet + $101.25 Luna without caching; with the stated cache mix, $819 + $819 + $40.95. Replacing Luna with Flash-Lite costs $326.25 rather than $101.25 uncached, giving $4,376.25 for the three-provider mix.

Every additional 1,000 billable output tokens per call adds $922.50 to the practical mix or $2,722.50 to the Astra mix. Thus 2,000 rather than 500 output tokens raises the 20K-input practical estimate to $5,535 uncached or $3,062.70 cached. Visible action JSON length is not total billed reasoning/output.

An illustrative 100-call task starting with 5K input tokens and adding 500 new context tokens per call consumes 100×5K + 500×100×99/2 = 2.975M input tokens before cache discounts: an average of 29,750 input tokens/call. The final context length alone is therefore not the task's billed input volume.

For a first study, reserve about $5.4K for the practical 20K/500 no-cache scenario plus 30% development/retry allowance. If a pilot verifies the 80%-read cache mix, that corresponding allowance is about $2.2K. The Astra substitution requires about $15.9K or $6.4K under those respective assumptions. These are planning allowances, not vendor charges. VM/browser/search fees, extra experimental conditions, evaluator-model calls, data generation and training are additional unless explicitly included.

A pilot should estimate actual per-model token usage, average and p95 calls, cache categories and reasoning output before committing the full sweep. Hosted interfaces and tokenizers can differ. OpenAI's September 25 changelog explicitly reports an image-encoding fix affecting Sol/Luna computer-use evaluations; pin evaluation timing and rerun affected pre-fix results. [Dated change](https://developers.openai.com/api/docs/changelog)

