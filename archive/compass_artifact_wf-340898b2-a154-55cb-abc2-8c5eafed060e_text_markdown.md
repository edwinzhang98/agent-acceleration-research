# Novelty Assessment: Compiling, Speculating and Cheapening LLM Agents for Repetitive Enterprise Web Workflows (SAP Concur)

**Verdict:** None of the four components is new on its own. Trajectory-to-program skill induction, speculative action execution, observation pruning and model routing, and cost/accuracy Pareto evaluation all have 2024–2026 prior work, and a wave of May–September 2026 preprints sits very close to this plan. What is still open is narrower. First, speculative execution of *state-changing* UI transitions on a live web app that cannot be snapshotted. Second, recipe compilation from a mix of the agent's own runs and a few human demos, with a calibrated LLM fallback, on write-heavy form workflows. Third, a field-level accounting of how much accuracy each acceleration lever costs, over repeated runs, with latency as a third Pareto axis. The paper is publishable if it is framed around those three gaps, measured against the 2026 systems below, and extended beyond Concur to public benchmarks. Framed as "we combined known tricks on SAP Concur", it will be read as an engineering report.

## TL;DR
- **Mostly not novel as components.** Program-level skill induction (ASI, SkillWeaver, SpeedRunner), trajectory/site-derived fast paths with LLM fallback (Skim, Agent JIT Compilation, Agentic Compilation), speculative actions (Speculative Actions, PASTE, Speculative Macro Commit), plan caching (Agentic Plan Caching), pruning (AgentOccam, FocusAgent) and cost-Pareto evaluation (AI Agents That Matter, HAL) all exist. Most of them report 20–50% latency or cost cuts, and some report up to 10×.
- **Genuinely open.** (i) Speculation over irreversible, non-snapshotable UI transitions in a live enterprise portal, with commit/rollback semantics. (ii) Profile-guided recipe compilation with guards and a "deoptimize to LLM" fallback, learned from own runs plus human demos, on write-heavy forms. (iii) Per-lever field-level accuracy-loss attribution and accuracy–latency–cost frontiers over repeated runs.
- **To get past NeurIPS/ICLR/MLSys reviewers:** add WorkArena/WorkArena++, WebArena and τ²-bench (AppWorld as an alternative). Compare directly against ASI/SkillWeaver, Skim/Agent JIT, Speculative Actions/SMC and a pure-RPA replay baseline. Report N≥5 repeated runs. Show that the 57% "page-determined step" statistic generalizes beyond Concur. The public-benchmark bill is roughly $2k–$12k per benchmark for a full ablation grid (my estimate, derived from reported per-run costs).

## Key Findings

1. **The closest prior work appeared in 2026 and is still preprint-only.** Five of the ten closest works were posted to arXiv between April and September 2026: Agentic Compilation (Apr), Skim (May), Agent JIT Compilation (May), SpeedRunner (Aug) and Speculative Macro Commit (Sep). Reviewers in late 2026 will know them. The plan must cite them and ideally beat or complement them experimentally.
2. **Your setting differs from theirs in a way that helps you.** Skim's profiling of WebVoyager tasks found median per-step delays of 4.7 s for LLM inference and 6.6 s for browser actions.\[1\] That is browser-dominated. Your 71% model-wait share means model-side levers (recipes, routing, caching) have more headroom in your setting than in theirs. This is worth stating explicitly as a characterization result.
3. **Prior "fast path" systems are mostly read-only.** Skim targets information retrieval: it synthesizes URLs and extracts answers, and it reports 66.7% of steps as purely navigational for the median task.\[1\] Speculative Actions and SMC speculate on tool calls in environments that can be snapshotted or are side-effect-free.\[2\] Expense filing is write-heavy: it creates reports, attaches receipts and submits. That makes safe speculation and replay a harder and more interesting problem.
4. **Exposing mined macros as tools may not work.** SMC reports that "simply exposing mined action sequences as additional callable tools is unreliable: open models like Qwen3.5-27B rarely select these mined macros".\[3\] SpeedRunner reports that aggressive code delegation can "over-compress a capable actor".\[4\] Both findings argue for runtime-triggered recipes with guards rather than model-selected tools. They also argue for reporting the accuracy cost of over-compression.
5. **Pruning savings are smaller than the pruning rate suggests.** On WorkArena L1 with GPT-4.1, FocusAgent pruned 51% of the observation but cut cost only 19%. Naive truncation to 5k tokens cut cost 49% but dropped success rate from 53.6% to 44.5%.\[5\] Your field-level answer key makes this trade-off measurable per field, which prior work could not do.

## Details

### Task 1 — The 10 closest prior works (ranked by proximity)

| # | Work (date, venue) | What it does | Reported gains (exact setting) | How the plan differs |
|---|---|---|---|---|
| 1 | **Agent JIT Compilation for Latency-Optimizing Web Agent Planning and Scheduling** — Winston, Wang, Mirhoseini, Kozyrakis (Stanford), arXiv 2605.21470, May 2026 (ICML-formatted preprint; venue acceptance not verified) | Compiles the task description into an executable code plan built from cached, reusable tools. Plans may include LLM calls and parallelism. JIT-Planner validates candidate plans against tool specs and picks the minimum-cost one. JIT-Scheduler picks a parallelization/hedging strategy by Monte Carlo over learned latency distributions. Tools carry pre/postcondition invariants.\[6\] | "Across five applications, JIT-Planner achieves 10.4× speedup and 28% higher accuracy over Browser-Use, while JIT-Scheduler achieves 2.4× speedup and 9% higher accuracy over OpenAI CUA." Best vs worst code-plan latency differs by 5.3×.\[6\] | The closest systems analogue. It compiles *per task from the instruction* onto a cached tool library. It does not mine recurring fragments from the agent's own trajectories or human demos. Its speculation is request hedging, not speculative UI transitions. It has no field-level accuracy accounting and no enterprise write workflows. Your "JIT" framing must be positioned explicitly against it. |
| 2 | **Skim (v1 title: Accio): Speculative Execution for Fast and Efficient Web Agents** — Wong, Hsieh, Nath, Netravali (Princeton/MSR), arXiv 2605.16565, May 2026 | Profiles each site offline (URL templates, answer schemas). At runtime it matches queries to templates, synthesizes the destination URL, extracts with a small model, and gates the result with a lightweight verifier. On misspeculation it falls back to the full ReAct agent, warm-started at the fast path's final URL.\[1\] | "Reduces median per-task cost by 1.9× and latency by 33.4% with no accuracy loss" on WebVoyager and WebShop, with BrowserUse, AgentOccam and WebVoyager backends. Aggregate mode gives up to +16.7 pp accuracy (+4.2 pp with majority vote). Hand-optimized programs were 66.7–94.9% faster; naive cheap substitution dropped success by 60%.\[1\] | This is the closest "fast path + verifier + LLM fallback" design. It is read-only retrieval that bypasses the browser via URLs, and it is profiled per site rather than learned from demos. It does not handle multi-page write workflows, speculative UI state transitions, or per-field accuracy. |
| 3 | **Speculative Macro Commit (SMC) for Faster Tool-Using Agents** — Liu et al., arXiv 2609.03236, Sep 2026 | Mines recurring multi-action skeletons from training traces into a hidden macro library. A small drafter pre-executes action chains on an isolated environment snapshot. When the actor's next call matches the first drafted action, the remaining steps are committed.\[2\] The commit is approximate, not lossless.\[3\] | Qwen3.5-27B actor with a Qwen3.5-4B drafter: matches sequential accuracy while cutting latency 18.59% vs sequential and 10.23% vs Speculative Actions on τ²-bench Telecom. On AppWorld, wall time drops 44.9% vs sequential and 7.7% vs SA, "with a small reduction in task completion".\[2\] | This is the closest combination of recipe mining and speculation. It needs environment snapshots, which a live SaaS portal like Concur does not provide. It targets API tool agents, not GUI/web, uses no human demos, and does not replay recipes deterministically without a drafter. |
| 4 | **Better, Faster, Stronger: Programmatic Skill Learning Best Reduces Agent Cost (SpeedRunner)** — Huang, Wang, Wang, Jurayj, Jiménez Gutiérrez, Khashabi, Andrews (JHU), arXiv 2608.11338, Aug 2026 | A coding-agent "inducer" analyzes stored trajectories and refactors a library of executable skills. It runs online in wake–sleep cycles, without replay. Its framing is explicitly cost-first.\[4\] | With GPT-5.4-mini, BabyAI output tokens fall to "roughly an eighth of the ReAct baseline" at near-perfect success. It gives a "2–8× token reduction over ASI". Gemini-3-Flash cuts LLM calls by 94% in Crafter, but can over-compress a capable actor. Reports 3 seeds with ±1 s.d.\[4\] | This is the strongest prior claim that programmatic skills are the best cost lever. It runs on text-embodied games (ScienceWorld, BabyAI, Crafter), not web, and reports no latency measurements, no human demos, no fallback design and no speculation.\[4\] |
| 5 | **Inducing Programmatic Skills for Agentic Tasks (ASI)** — Wang, Gandhi, Neubig, Fried, COLM 2025, arXiv 2504.06821 | Online induction of executable (programmatic) skills from the agent's own successful WebArena trajectories.\[7\] Each skill is verified by re-running it on the inducing task. | +23.5% success rate over its static baseline on WebArena, and 11.3% higher than AWM. Procedures are "10.7–15.3% more efficient" in steps.\[7\] | Plan (a) is ASI-like. ASI verifies skills by replaying them, reports step efficiency rather than wall-clock or $, and has no LLM-fallback-on-guard-failure mechanism or demo mixing. SpeedRunner reports that ASI's cost *grows* as its library accumulates.\[4\] |
| 6 | **SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills** — Zheng et al., arXiv 2504.07079, Apr 2025 | Autonomous exploration proposes skills, practices them, and distills them into tested and debugged Playwright APIs. The APIs transfer across agents.\[8\] | Relative success-rate gains of 31.8% on WebArena and 39.8% on real sites (Online-Mind2Web). APIs from strong agents improve weaker agents by up to 54.3%.\[9\] | SkillWeaver is capability-oriented rather than cost/latency-oriented. Its skills come from exploration, not from the target workflow's own runs or demos, and are invoked by the LLM as APIs. It reports no latency or cost frontiers. |
| 7 | **Agentic Plan Caching (APC): Test-Time Memory for Fast and Cost-Efficient LLM Agents** — Zhang et al., NeurIPS 2025, arXiv 2506.14852 | Extracts plan templates from completed executions, matches new requests by keyword, and adapts templates with a small model.\[10\] | "Reduce costs by 50.31% and latency by 27.28% on average while maintaining" 96.61% of optimal performance across five workloads. Caching overhead is 1.04% of cost.\[11\] | APC caches plans for Plan-Act agents, not GUI action sequences, and still executes through the agent. It is the canonical NeurIPS reference for "reusing past executions to cut serving cost" and a required baseline or citation. |
| 8 | **Speculative Actions: A Lossless Framework for Faster Agentic Systems** — Ye, Ahuja, Liargkovas, Lu, Kaffes, Peng (Columbia), arXiv 2510.04371, ICLR 2026 | A fast speculator predicts next actions and pre-launches them in parallel with the slow actor. Results commit only on a match, restricted to idempotent or reversible actions.\[12\] | "Up to 55% next-action prediction accuracy, translating into up to 20% latency reductions" across gaming, e-commerce, web search and a lossy OS setting. Includes a cost–latency analysis of speculative breadth.\[13\] | This is the canonical action-level speculation baseline. It is general-purpose and not specialized to UI transitions whose probability is about 1.0. Your deterministic transitions should give far higher hit rates than 55%, and you should show that. |
| 9 | **Agentic Compilation: Mitigating the LLM Rerun Crisis for Minimized-Inference-Cost Web Automation** — Chundru (Selfotix), arXiv 2604.09718, Apr 2026 (industry, single author) | A one-shot LLM compiles a sanitized DOM into a deterministic JSON workflow blueprint that runs with zero LLM calls. On selector failure, "lazy replanning" invokes the LLM for selector healing, with a human-in-the-loop gate.\[14\] | Zero-shot compilation success is 80–94%.\[14\] Compilation costs $0.002–$0.092 across five models. The DOM sanitizer compresses HTML "by up to 85%". It claims inference cost moves from O(M×N) to amortized O(1).\[14\] | This is the closest RPA-with-LLM-fallback analogue. The evaluation is light: no standard benchmark, no latency or accuracy frontiers, and it admits that "longitudinal empirical studies are required".\[14\] Treat it as a positioning citation, not a strong baseline. |
| 10 | **Agent Workflow Memory (AWM)** — Wang, Mao, Fried, Neubig, arXiv 2409.07429, Sep 2024 (later OpenReview version, 2025; final venue not verified here) | Induces reusable *textual* workflows from past trajectories, offline or online, and supplies them in context.\[15\] | Online AWM surpasses baselines "from 8.9 to 14.0 absolute points as train-test task distribution gaps widen" (Mind2Web/WebArena).\[16\] | The seminal LLM-mediated workflow memory. The LLM still executes every step, which is the O(M×N) problem that Agentic Compilation critiques.\[14\] It is the natural "text recipes" ablation for plan (a). |

**Next-closest works (lower proximity; cite and use as ablation comparators):**
- **PASTE (Act While Thinking)**, Sui et al., MSR, arXiv 2603.18897, Mar 2026. Pattern-aware speculative tool execution mined from recurring tool-call sequences. It "reduces average task completion time by 48.5% and improves tool execution throughput by 1.8x".\[17\] Its tools are not UI.
- **Speculate with Memory**, Li et al., Salesforce, arXiv 2607.12236, Jul 2026. Adds a transition table, episodic memory and a confusion tracker to the speculator. Action-prediction accuracy improves 19–39% (relative), and observation prediction improves up to 2.5×.\[18\] Estimated ALFWorld latency reduction rises from about 28% to over 50%.\[19\] Its "transition table" directly overlaps your "probability ~1.0 transitions" observation.
- **AAPT (Why Are GUI Agents Correct but Late?)**, Dong et al., arXiv 2607.28399, Jul 2026. Pre-compiles bounded policy trees during idle time. Success within a contested GUI decision window improves from 0.50 to 0.79.\[20\]
- **UFO²**, arXiv 2504.14603. "Speculative multi-action execution" on Windows desktop. It batch-predicts several actions per inference and validates controls through OS APIs before each action.\[21\]
- **FocusAgent**, arXiv 2510.03204. Covered in Key Findings 5 and Task 5.
- **AgentOccam**, Yang et al., ICLR 2025, arXiv 2410.13825. Observation and action-space refinement gives +26.6 pp (+161%) over similar plain agents on WebArena.\[22\]
- **LOOP Skill Engine** (arXiv 2605.14237) and **Activity Frames** (arXiv 2608.05784). Both do deterministic record/replay for agents.
  - LOOP claims 99% success and a 99% token cut.
  - Activity Frames candidly separates a 99% per-covered-step ceiling from realized savings (median guardable fraction 0.415).\[23\]
  - Their own disclosures show the claims are partly modeled rather than measured. Treat them with caution.
- **Hyperbrowser Action Caching**, industry docs. Records XPath actions for LLM-free replay with "LLM Fallback: If XPath fails, falls back to AI".\[24\] This shows replay-with-fallback is already a shipped product pattern, which weakens any novelty claim on the mechanism itself.

### Task 2 — What is done vs. open

**(a) Recipes from own runs plus human demos, deterministic replay, LLM fallback: partially done.**
- *Done:* Executable skills induced from the agent's own trajectories (ASI, SkillWeaver, SpeedRunner). Deterministic compiled blueprints with LLM healing on failure (Agentic Compilation, Hyperbrowser, LOOP). Site-profile fast paths with verifier and fallback (Skim). Hidden mined macros committed at runtime (SMC).
- *Gap that remains:*
  - No work I found combines own-run mining *with* a few human demonstrations and measures the marginal value of each source.
  - None calibrates the fallback trigger (guard/verifier threshold) against a field-level error budget.
  - None evaluates on multi-page, write-heavy enterprise forms with policy constraints.
  - The "deoptimization" semantics are underexplored: what state the LLM resumes from when a guard fails mid-recipe. Skim's warm start at the fast path's final URL is the closest.

**(b) Speculative execution of predictable UI transitions: partially done at the tool level; open for stateful live web UIs.**
- *Done:* Speculative Actions (ICLR 2026), PASTE, SMC, Speculate with Memory, and AOSpec (arXiv 2608.00881, action and observation co-speculation).\[25\]\[26\] SMC and TClone (arXiv 2605.17320, low-latency forking of live GUI environments) supply snapshot/rollback substrates for speculation over side effects.\[27\]
- *Open:* speculating on *UI transitions* in a live, proprietary, non-forkable SaaS web app. Here you cannot snapshot the server state, so correctness requires one of:
  - (i) restricting speculation to reversible or idempotent transitions (navigation, opening modals, pre-rendering),
  - (ii) speculating the *observation*, i.e. predicting the next page, so that the next model call can start early,
  - (iii) explicit compensating actions.

  I found no paper that classifies web UI transitions by reversibility and reports a speculation hit rate and accuracy impact in such a portal. This is the most defensible systems contribution. It is also the component most likely to be scooped soon, given the density of speculation papers in 2026.\[25\]

**(c) Observation pruning, prefix caching, small-model routing: done.**
- Pruning: AgentOccam; FocusAgent (WorkArena/WebArena with costs); Agentic Compilation's DOM sanitizer.
- Small-model routing and cascades: Skim uses small-model extraction plus a judge; APC uses a lightweight adapter model. Skim cites FrugalGPT-style cascades.\[1\]
- Cost studies: Efficient Agents (arXiv 2508.02694) "retains 96.7% of the performance of OWL... while reducing operational costs from $0.398 to $0.228", a 28.4% cost-of-pass improvement on GAIA.\[28\] AgentDiet (arXiv 2509.23586) reduces coding-agent cost 21.1–35.9%.\[29\]
- Prefix/prompt caching is standard in serving systems and priced by providers. SpeedRunner's accounting prices cached input at $0.075 vs $0.75 per M tokens for GPT-5.4-mini.\[4\]
- *Novelty here is near zero.* The only publishable angle is the *interaction*: pruning changes the prefix and invalidates caches, which AgentDiet explicitly notes as a cost ("invalidated KV Caches").\[29\] Routing interacts with recipe coverage. Quantify these interactions rather than claiming the levers themselves.

**(d) Accuracy–latency–cost Pareto frontiers over repeated runs: partially done.**
- *Done:* AI Agents That Matter (Kapoor et al., TMLR, arXiv 2407.01502) argues for cost-controlled evaluation and accuracy–cost Pareto frontiers.\[30\]\[31\] HAL (Kapoor et al., ICLR 2026, arXiv 2510.11977) ran "21,730 agent rollouts across 9 models and 9 benchmarks... with a total cost of about $40,000", with Pareto frontiers, and releases "all agent logs, comprising 2.5B tokens of language model calls". τ-bench introduced pass^k.\[32\] SpeedRunner reports ±1 s.d. over 3 seeds.\[4\]
- *Gap that remains:* HAL's "three-dimensional analysis spanning models, scaffolds, and benchmarks" does not include latency; its frontiers are two-dimensional (accuracy vs $). I found no work reporting *three-way* accuracy–latency–cost frontiers with *field-level* accuracy for form-filling agents over repeated runs, or attributing accuracy loss to each acceleration lever.

**The combination and the setting.**
- The integrated stack (recipes + UI speculation + per-step cheapening + 3-D Pareto) on an enterprise portal is, as far as I found, not published as a unit.
- SAP Concur itself: I found no LLM-agent paper evaluating on SAP Concur or on expense reporting with policy-derived answer keys. The closest are TheAgentCompany, which includes finance/admin tasks, and WorkArena/WorkArena++ on ServiceNow.\[33\]\[34\]\[35\]
- My searches for Concur/expense-report agent papers returned only vendor and marketing pages. This is a real but modest novelty. Reviewers value the answer-key methodology more than the brand.

### Task 3 — Baselines, ablations, objections

**Baselines reviewers will demand**
1. A vanilla ReAct / Browser-Use / BrowserGym GenericAgent on the same model. This is the baseline of Agent JIT, Skim and FocusAgent.
2. AWM (textual workflows) and ASI or SkillWeaver (programmatic skills exposed to the LLM). Together these isolate "deterministic replay" from "skills as tools". SpeedRunner is optional but strong.
3. Pure RPA/scripted replay: a recorded Playwright script from demos with no LLM, plus the same with naive LLM fallback (Hyperbrowser/Agentic-Compilation style). This is the most dangerous baseline. If a script alone reaches 95% field accuracy at near-zero cost, the research question narrows to the residual.
4. Skim-style fast path with verifier and warm-started fallback.
5. Speculative Actions (single-step) and SMC-style macro commit, run on equal hardware. SMC reports gains relative to SA, so do the same.\[36\]
6. APC plan caching.
7. Prompt-caching-only, small-model-only, and a cascade/router (FrugalGPT/RouteLLM-style), each alone.
8. Agent JIT Compilation, if code is available. Otherwise, a reimplementation of its planner idea.

**Ablations**
- Remove each component individually: (a), (b), (c-pruning), (c-caching), (c-routing). Also report the pairwise interactions: caching × pruning, and recipes × routing.
- Recipe source: own runs only vs demos only vs both. Vary the number of demos (0, 1, 3, 5) and the number of own runs.
- Fallback trigger threshold. Sweep the guard/verifier strictness to produce the frontier itself.
- Speculation depth or breadth, and a restriction to reversible transitions only vs all transitions. Report hit rate, wasted calls and any side-effect incidents.
- Pruning aggressiveness vs field accuracy. FocusAgent shows cost savings lag pruning rates.\[5\]
- Variance: N≥5 repeated runs per configuration. Report pass^k-style consistency (τ-bench) and bootstrap CIs on every frontier point.
- Distribution shift: portal UI changes (synthetic DOM perturbations, a real Concur release), new policy rules, and new expense types. Report recipe breakage rate and recovery cost.
- Cost decomposition over time: SpeedRunner-style curves of cost per report vs number of prior reports, including amortized compilation cost.

**Likely objections and how to pre-empt them**

| Objection | Pre-emption |
|---|---|
| Single-domain testbed | Add WorkArena/WorkArena++, WebArena and τ²-bench (Task 5). Show the same lever ranking holds. |
| Live proprietary portal is not reproducible | Release a Concur-like *simulator*, or at least recorded traces, anonymized policies and answer keys. Also release code that runs on public benchmarks. Report portal version and dates. Put the headline claims on public benchmarks and position Concur as the real-world case study. |
| "57% page-determined calls" and "p≈1.0 transitions" are Concur-specific | Measure the same statistics on WorkArena++, WebArena and τ²-bench trajectories. Skim's 66.7% navigational-step figure on WebVoyager is a useful external anchor to cite.\[1\] |
| It's engineering, not research | Contribute (i) a formal model of expected speedup vs recipe coverage, guard precision and speculation hit rate (Speculative Actions gives a template), (ii) a safety semantics for speculation without snapshots, and (iii) a measurement methodology (field-level, 3-D frontiers). |
| Answer-key leakage into recipe learning | Learn recipes only from trajectories and demos, never from answer keys. Use keys solely for evaluation. Use disjoint report sets for learning and testing. Report results when recipe learning uses only self-judged success. |
| Comparison fairness (caching, hardware, provider-side latency) | Report both $ with and without caching. HAL, for instance, reports cost "without accounting for caching benefits".\[37\] Fix region, time of day and model version. Report API latency distributions. Give speculative baselines the same extra compute. |
| Lossy acceleration hides errors | Report per-field error deltas and the worst-case field, not only mean accuracy. Include an "abstain/escalate to human" option in the frontier. |

### Task 4 — Three framings

1. **"Profile-guided tiered compilation for agents" (JIT with deoptimization).** Interpret with the LLM. Detect hot, stable trajectory fragments. Compile them into guarded recipes. Deoptimize to the LLM on guard failure, resuming from the current state.
   - Best venue: **MLSys**, or OSDI/SOSP if the runtime is substantial.
   - Position against Agent JIT Compilation, which compiles from the instruction rather than profiles; Agentic Compilation (no guards/profiling); SpeedRunner and ASI (skills as LLM-called tools); and APC.
   - The distinguishing claim is profile-guided plus guard-based deoptimization with measured coverage and misspeculation cost.
2. **"Branch prediction for stateful UIs": speculative execution without snapshots.** Treat UI transitions like branches. Near-deterministic transitions (p≈1.0) are predicted and executed, or their observations pre-fetched. Transitions are classed by reversibility, with commit and compensation rules.
   - Best venue: **MLSys** or **NeurIPS** (main track, systems-for-ML).
   - Position against Speculative Actions (lossless, general), SMC and TClone (need snapshots), PASTE (tools), Speculate with Memory (transition tables), and Skim (read-only).
   - The distinguishing claim is safe speculation in live, irreversible web apps, with hit-rate and side-effect analysis.
3. **"Where agent time and money go": field-level, three-way Pareto accounting for enterprise automation.** A measurement paper built on answer-key-graded workflows. It decomposes the 13-minute, 100-call run into page-determined vs reasoning steps and reports per-lever accuracy loss. Frontiers use repeated runs and consistency metrics.
   - Best venue: **NeurIPS Datasets & Benchmarks** or **ICLR**. It is strongest if you release a Concur-like simulated environment.
   - Position against AI Agents That Matter, HAL and Efficient Agents (2-D cost–accuracy), τ-bench pass^k, and WorkArena++.

My recommendation is to lead with framing 1 plus 2 as a single MLSys submission and use framing 3's methodology as the evaluation backbone. Framing 3 alone risks reading as a case study unless you release an environment.

### Task 5 — Three public benchmarks and approximate costs

| Benchmark | Why it fits | Size / steps (reported) | Cost per run (reported → my extrapolation) | Full grid (my estimate: ~9 configs × 5 repeats = 45 runs) |
|---|---|---|---|---|
| **WorkArena (L1) + WorkArena++ (L2/L3)** — Drouin et al. 2024; Boisvert et al., NeurIPS 2024 D&B, arXiv 2407.05291 | Enterprise ServiceNow forms and lists with human-coded oracles and validators.\[33\] This is the closest public analogue to Concur and supports the "repetitive enterprise workflow" claim. Instances run on free ServiceNow developer instances.\[33\] | WorkArena++ has 682 tasks. The standard curriculum "yields 235 tasks for each L2 and L3", with 50-step limits. Oracle action counts range up to about 140 per instance (histogram only).\[33\] The L1 evaluation in FocusAgent is 33 tasks × 10 seeds = 330 episodes.\[5\] | **Reported:** WorkArena L1 with the GPT-4.1 GenericAgent cost $55.6 per 330-episode run at 53.6% success rate (FocusAgent, latest arXiv version; v1 reports 53.0%).\[5\]\[38\] **Estimate:** WorkArena++ L2+L3 (470 instances, ≤50 steps) costs about $250–$300 per run at GPT-4.1-class pricing. No dollar cost is published by WorkArena++. | L1: about $2.5k. L2+L3: about $11–14k. Cheaper models cut this 5–10×. |
| **WebArena** — Zhou et al. 2023 | This is where AWM, ASI, SkillWeaver, AgentOccam and FocusAgent report results, so it enables direct comparison with the closest skill-induction baselines. Self-hosted Docker keeps it reproducible. | 812 tasks, 30-step limit (BrowserGym table).\[39\] | **Reported:** GPT-4.1 GenericAgent cost $59.0 on a 381-task subset at 36.5% success rate (FocusAgent).\[5\] **Estimate:** about $125 per full 812-task run. | About $2.7k on the 381 subset, about $5.6k on the full set. |
| **τ²-bench** — Barres et al. 2025, arXiv 2506.07982 (τ-bench: Yao et al. 2024, arXiv 2406.12045) | Policy-constrained multi-turn workflows (airline, retail, telecom) that mirror policy-derived answer keys. The native pass^k metric covers repeated-run consistency, and SMC's τ²-Telecom and HAL's τ-Airline results give ready comparators. | 50 airline, 115 retail and 114 telecom tasks.\[40\] pass^k is "the chance that all k i.i.d. task trials are successful". The original τ-bench abstract reports that gpt-4o agents "succeed on <50% of the tasks, and are quite inconsistent (pass^8 <25% in retail)". | **Reported:** a gpt-4.1 agent+user run of "all domains for 1 trial per task is approximately $40".\[40\] HAL τ-Airline full runs range from $0.31 (Gemini 2.0 Flash, 28%) to $180.49 (Claude Opus 4.1, 54%). o4-mini High reached 56% for $11.36.\[37\]\[41\] | About $1.8k at gpt-4.1 pricing, or $7k+ with 4 trials per task. |

**Alternative third benchmark: AppWorld** (Trivedi et al., arXiv 2407.18901; 750 tasks over "9 day-to-day apps operable via 457 APIs", with Test-Normal 168 and Test-Challenge 417; GPT-4o "solves only ~49% of our 'normal' tasks and ~30% of 'challenge' tasks", and its state-based tests check for "collateral damage", which suits a side-effect metric). Use it if you want the SMC comparison, which reported a 44.9% wall-time cut. No official per-run cost is published; a community estimate is about $0.02–$0.03 per task with a small model, which is unverified.\[42\] **TheAgentCompany** (Xu et al., arXiv 2412.14161; 175 tasks) is realistic but expensive. Its best model, Gemini-2.5-Pro with OpenHands, reached 30.3% success at 27.2 steps and $4.20 per task ("an average of almost 27 steps and more than $4 to complete each task"), which is about $735 per run before repeats. Use a subset at most. OSWorld-Verified (369 tasks) is desktop-oriented and has no published per-run cost.\[43\]\[44\] I would not prioritize it for web workflows.

## Recommendations
1. **Before writing, rerun the novelty search every 2–4 weeks.** Speculative agent execution had at least eight arXiv submissions in mid-2026.\[25\] SMC (Sep 2026) is the most dangerous overlap.
2. **Make the pure-RPA-replay and Skim/Agent-JIT baselines central.** If deterministic scripts alone solve most Concur reports, the contribution is the fallback and speculation logic on the residual. Say so upfront.
3. **Scope speculation to what is safe without snapshots.** That means observation pre-fetch and reversible navigation. Report side-effect incidents as a metric. This is your clearest technical novelty.
4. **Publish the characterization statistics on public benchmarks.** These are the 57% page-determined calls, the p≈1.0 transitions and the 71% model-wait share. They turn a Concur anecdote into a general finding.
5. **Report field-level accuracy loss per lever** with CIs over N≥5 runs and 3-D frontiers. Include cached vs uncached $.

## Caveats
- Many of the closest works (Agent JIT, Skim, SpeedRunner, SMC, Agentic Compilation, Speculate with Memory, AAPT, LOOP, Activity Frames) are **2026 arXiv preprints without verified peer review**. Their numbers are as reported by the authors. Agentic Compilation, LOOP and Activity Frames rely partly on modeled rather than measured savings.
- Leads I **could not verify** in this pass, and therefore do not cite with numbers: Synapse, ExpeL, AutoGuide, Learn-by-Interact, Memp (seen only as a title), ReasoningBank, Agent KB, LLMCompiler, RouteLLM, the SGLang/vLLM prefix-caching papers, ST-WebAgentBench, EnterpriseBench, SmartFlow, FlowMind, and UiPath/Automation Anywhere technical reports. These should be checked before submission. Several, notably LLMCompiler and RouteLLM, are standard baselines reviewers will expect.
- The AWM venue is not confirmed. SpeedRunner cites an OpenReview version dated June 2025.\[4\]
- Cost figures for WorkArena++, full WebArena and the ablation grids are **my extrapolations** from reported per-run costs and 2025-era model prices. HAL figures are frozen at 2025 models and exclude caching.\[37\] The τ-bench paper's own "$200 per trial" statement is inconsistent with its per-task costs ($0.61 × 115 tasks ≈ $70).\[32\]
- My searches found no SAP Concur agent paper, but absence of evidence from a finite search is not proof of absence. Industry blog posts or internal SAP work may exist.

## Sources

1. [Skim: Speculative Execution for Fast and Efficient Web Agents](https://arxiv.org/html/2605.16565v2)
2. [\[2609.03236\] Speculative Macro Commit for Faster Tool-Using Agents](https://arxiv.org/abs/2609.03236)
3. [Speculative Macro Commit for Faster Tool-Using Agents](https://arxiv.org/html/2609.03236)
4. [Better, Faster, Stronger: Programmatic Skill Learning Best Reduces Agent Cost](https://arxiv.org/pdf/2608.11338)
5. [FocusAgent: Simple Yet Effective Ways of Trimming the Large Context of Web Agents](https://arxiv.org/pdf/2510.03204)
6. [Agent JIT Compilation for Latency-Optimizing Web Agent Planning and Scheduling](https://arxiv.org/html/2605.21470)
7. [Inducing Programmatic Skills for Agentic Tasks](https://openreview.net/pdf?id=lsAY6fWsog)
8. [Foundations: SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills · Issue #1418 · jjakimoto/research-issues](https://github.com/jjakimoto/research-issues/issues/1418)
9. [Paper page - SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills](https://huggingface.co/papers/2504.07079)
10. [Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents | OpenReview](https://openreview.net/forum?id=n4V3MSqK77)
11. [Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents](https://openreview.net/pdf?id=n4V3MSqK77)
12. [Speculative Actions: A Lossless Framework for Faster Agentic Systems](https://hungchun0201.github.io/agentic-ai-survey/papers/speculative-actions/index.html)
13. [Speculative Actions: A Lossless Framework for Faster Agentic Systems](https://arxiv.org/pdf/2510.04371)
14. [Agentic Compilation: Mitigating the LLM Rerun Crisis for Minimized-Inference-Cost Web Automation](https://arxiv.org/html/2604.09718v2)
15. [\[2409.07429\] Agent Workflow Memory](https://arxiv.org/abs/2409.07429)
16. [\[PDF\] Agent Workflow Memory | Semantic Scholar](https://www.semanticscholar.org/paper/Agent-Workflow-Memory-Wang-Mao/c68cc84ec7808d7bbd5686a6bd1393752a9d8e8d)
17. [(PDF) Act While Thinking: Accelerating LLM Agents via Pattern-Aware Speculative Tool Execution](https://www.researchgate.net/publication/402860178_Act_While_Thinking_Accelerating_LLM_Agents_via_Pattern-Aware_Speculative_Tool_Execution)
18. [\[2607.12236\] Speculate with Memory: Lossless Acceleration for LLM Agents](https://arxiv.org/abs/2607.12236)
19. [Speculate with Memory: Lossless Acceleration for LLM Agents Yu Li](https://arxiv.org/pdf/2607.12236)
20. [\[2607.28399\] Why Are GUI Agents Correct but Late? Decode on the Decision-Time Critical Path, Tested with Pre-Compiled Policy Trees](https://arxiv.org/abs/2607.28399)
21. [UFO2: The Desktop AgentOS](https://arxiv.org/pdf/2504.14603)
22. [AgentOccam: A Simple Yet Strong Baseline for LLM-Based Web Agents | alphaXiv](https://www.alphaxiv.org/abs/2410.13825)
23. [Activity Frames: Deterministic Screen-Activity Compilation for Agent Memory and Replay](https://arxiv.org/pdf/2608.05784)
24. [Action Caching - Hyperbrowser](https://www.hyperbrowser.ai/docs/hyperagent/action-cache)
25. [\[Submission\] When Does Speculative Tool Execution Pay? Contention Boundaries, Latency Tails, and the Parallelism the Serial Baseline Already Had · Issue #50 · argszero/silicon-science-cs](https://github.com/argszero/silicon-science-cs/issues/50)
26. [AOSpec: Action and Observation Co-Speculation for Low-Latency Agent Serving](https://arxiv.org/pdf/2608.00881)
27. [TClone: Low-Latency Forking of Live GUI Environments for Computer-Use Agents](https://arxiv.org/html/2605.17320)
28. [\[2508.02694\] Efficient Agents: Building Effective Agents While Reducing Cost](https://arxiv.org/abs/2508.02694)
29. [Reducing Cost of LLM Agents with Trajectory Reduction](https://arxiv.org/pdf/2509.23586)
30. [\[2407.01502\] AI Agents That Matter](https://arxiv.org/abs/2407.01502)
31. [AI Agents That Matter](https://arxiv.org/pdf/2407.01502)
32. <https://arxiv.org/pdf/2406.12045>
33. [WorkArena++: Towards Compositional Planning and Reasoning-based Common Knowledge Work Tasks](https://arxiv.org/pdf/2407.05291)
34. [\[2407.05291\] WorkArena++: Towards Compositional Planning and Reasoning-based Common Knowledge Work Tasks](https://arxiv.org/abs/2407.05291)
35. [TheAgentCompany Benchmark: Evaluating LLM Agents](https://www.emergentmind.com/topics/theagentcompany-benchmark)
36. [Speculative Macro Commit for Faster Tool-Using Agents](https://arxiv.org/pdf/2609.03236)
37. [HAL: TAU-bench Airline](https://hal.cs.princeton.edu/taubench_airline)
38. <https://arxiv.org/html/2510.03204v1>
39. <https://arxiv.org/pdf/2412.05467>
40. <https://arxiv.org/pdf/2506.07982>
41. [HAL: Holistic Agent Leaderboard](https://hal.cs.princeton.edu/)
42. [Submit GLM-5.3-Flash + Qwen3.8-Flash AppWorld results by Huanz86251 · Pull Request #23 · StonyBrookNLP/appworld-leaderboard](https://github.com/StonyBrookNLP/appworld-leaderboard/pull/23)
43. [OSWorld and AndroidWorld Benchmarks](https://www.emergentmind.com/topics/osworld-verified-and-androidworld-benchmarks)
44. [Introducing OSWorld-Verified | Papers with Code](https://paperswithcode.co/paper/104223)
