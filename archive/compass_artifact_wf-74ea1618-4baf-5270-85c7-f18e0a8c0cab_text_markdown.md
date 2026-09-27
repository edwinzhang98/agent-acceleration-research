# From Tokens to Steps: Mapping LLM Inference Acceleration onto Agent-Level Acceleration (state of the art, September 2026)

Every major inference-acceleration idea already has a working agent-level analogue in 2023–2026 work, but the verified gains are modest and uneven. Two kinds of work report the largest numbers. Systems work that treats the agent program, not the request, as the scheduling and caching unit reports 2–15× throughput and more than 8× job-completion-time gains. Work that removes model calls outright (plan caching, compiled workflows, early exit) reports 30–70% cost or step reductions. Lossless speculative actions, the most direct analogue of speculative decoding, currently reports only about 20–40% latency reductions.

## TL;DR

- **The cost unit has moved from tokens to steps.** A coding-agent request averages 8.8 LLM calls and 10.8 tool calls (TraceLab: 4,265 sessions, 357,161 LLM steps and 432,510 tool calls from 43 developers). Each step re-prefills an ever-growing context, which makes total input tokens roughly quadratic in trajectory length without caching; even with caching on, TraceLab finds prefix tokens are 59.5% of total cost versus 29.2% for append tokens and only 11.2% for output tokens (median step: about 119K prefix, 875 append and 214 output tokens). Planning and reflection calls take more than half, sometimes close to 75%, of computer-use-agent latency, and later steps take up to 3× longer than early ones (OSWorld-Human).
- **Mapping quality varies.** The strongest analogues are (i) KV/prefix caching → program-aware KV retention and cross-task plan/workflow reuse (KVFlow up to 2.19×; Continuum >8× JCT; Agentic Plan Caching −50.31% cost) and (ii) continuous batching → program-level scheduling and parallel tool calls (Autellix 4–15× throughput; Parrot up to 11.7×; LLMCompiler up to 3.7× latency). Speculative actions and small action models work but deliver smaller or narrower gains. Quantization has no clean analogue. The closest is lossy compression of the context re-read every step (observation masking halves cost; AgentDiet −39.9% to −59.7% input tokens).
- **What is missing is the same across rows:** step-level accounting and benchmarks (calls/task, prefill tokens/task, wall-clock), safety semantics for speculating on side-effecting actions, and verifiers that can tell when a cheaper step (draft, cache hit, compiled script, early exit) is good enough.

## 1. Framing: token-level vs. step-level view

At the inference level, the optimization target is the time and cost of one request: TTFT (prefill-bound), TPOT (decode-bound), and throughput per GPU. Autellix makes the mismatch explicit. Existing serving systems "focus on request-level metrics, such as Time-to-First-Token (TFTT) and Time-per-Output-Token (TPOT)… However, these metrics overlook end-to-end latency for agentic programs."\[1\]

At the agent level, the unit of work is a *step*: one model call plus one or more tool/environment actions, repeated until termination. Task cost is roughly

**Cost(task) ≈ Σ_steps [prefill(context_t) + decode(output_t) + tool_latency_t + queueing_t]**,

where context_t grows with every step. Each inference technique therefore has an agent analogue that attacks one term: fewer steps (early exit, workflow reuse), cheaper steps (small models, routing), less re-read context per step (caching, compression), or overlapped steps (speculation, parallel calls, program-aware scheduling).

## 2. Technique-by-technique mapping

### 2.1 Speculative decoding → speculative / parallel actions

**Inference mechanism.** A cheap draft model proposes k tokens and the target model verifies them in one parallel pass. The output distribution is unchanged (lossless).

**Agent analogue.** A fast "speculator" predicts the next action (or the next tool result) and pre-launches it while the authoritative actor deliberates. The result commits only if it matches. Environment/tool latency plays the role of the memory-bound decode step.

**Implementations and reported gains.**
- *Speculative Actions: A Lossless Framework for Faster Agentic Systems* — Ye et al., Columbia, arXiv 2510.04371 (2025). Faster models predict likely next actions and execute them in parallel, committing only on a match. Across gaming, e-commerce and web-search environments it reaches "up to 55% next-action prediction accuracy, translating into up to 20% latency reductions." A lossy extension is studied in an OS setting. The paper also gives a cost–latency analysis of speculative breadth.\[2\]
- *Speculate with Memory: Lossless Acceleration for LLM Agents* — Li et al., Salesforce Research, arXiv 2607.12236 (2026). Adds online memory to the speculator: a transition table, episodic retrieval and a confusion tracker. It reports a "19–39% relative accuracy improvement on action prediction and up to a 2.5× increase on observation prediction tasks." On ALFWorld, estimated latency reduction grows from about 28% (stateless) to over 50% with memory. That figure is an estimate that counts each hit as hiding one actor LLM call. Pre-launch is restricted to side-effect-free operations.\[3\]
- *Interactive Speculative Planning* — Hua et al., arXiv 2410.00079 (2024). A fast approximation agent drafts steps (k=4) and a target agent verifies them. On OpenAGI, total time fell 22.27% (ReAct target), 28.32% (CoT) and 42.30% (multi-agent debate). On TravelPlanner it fell 19–25%. The paper is explicit about the costs: dollar cost rose ($0.122 vs $0.0713 per task with a ReAct target), it needed about 4–5 concurrent API calls, and fuzzy-match verification on TravelPlanner cut the commonsense micro pass rate from 48.6% to 41.7%.\[4\] It is therefore *not* lossless in that setting.
- *Dynamic Speculative Agent Planning (DSP)* — Guan et al., arXiv 2509.01920 (2025; reported as ICLR 2026). Uses online RL to set how far ahead to speculate. It "achieves comparable efficiency to the fastest lossless acceleration method while reducing total cost by 30% and unnecessary cost up to 60%."\[5\]\[6\]
- *Asynchronous LLM Function Calling (AsyncLM)* — Gim et al., arXiv 2412.07017 (2024). The model keeps generating while calls execute and is notified by interrupts. It reports "1.6x–5.4x" lower end-to-end latency than synchronous function calling on BFCL tasks.\[7\] This is overlap rather than speculation, but it attacks the same serialization bottleneck.

**Interpretation.** Speculative decoding wins because verification is cheap and parallel. In agents, verification is exact-match on an action, so hit rates top out around 55% and gains are about 20–40%. Speculation also costs extra dollars: Interactive Speculative Planning nearly doubled per-task cost.

**Open problems.** (1) Speculating on side-effecting actions: all lossless systems restrict themselves to idempotent or read-only calls, so there is no general rollback or transaction semantics for tools. (2) Semantic rather than exact-match verification with a correctness guarantee. (3) Multi-step speculation trees whose cost is bounded under provider pricing. (4) Draft models trained specifically on the target agent's trajectories. Speculate with Memory is a first step here.

### 2.2 KV / prefix caching → cross-step and cross-task caching

**Inference mechanism.** Reuse computed KV tensors for a shared prefix so later requests skip prefill for that prefix.\[8\]

**Agent analogue, at two levels.**
(a) *Cross-step KV reuse inside a trajectory.* The history at step t is a prefix of step t+1, so keeping the KV across tool-call pauses removes re-prefill.
(b) *Cross-task reuse of outputs.* Cache plans, workflows or skills, not tensors, so whole planning calls are skipped on similar tasks.

**Implementations and reported gains (serving level).**
- *KVFlow: Efficient Prefix Caching for Accelerating LLM-Based Multi-Agent Workflows* — Pan et al., NeurIPS 2025, arXiv 2507.07400. Replaces LRU with a steps-to-execution-aware eviction policy over an "Agent Step Graph," plus overlapped CPU→GPU prefetch. It reports "up to 1.83× speedup for single workflows with large prompts, and up to 2.19× speedup for scenarios with many concurrent workflows" versus SGLang with hierarchical radix cache.\[9\]\[10\]
- *Continuum: Efficient and Robust Multi-Turn LLM Agent Scheduling with KV Cache Time-to-Live* — Li et al. (Stoica group), arXiv 2511.02230 (2025, revised 2026). Pins the KV cache across tool calls with a TTL set by reload cost and queueing delay, combined with program-level FCFS. On SWE-Bench, BFCL and OpenHands with Llama-3.1 8B/70B, Gemma-3 12B and GLM-4.5 355B, it "improves the average job completion times by over 8x while improving throughput."\[11\]
- *CacheBlend* — Yao et al., EuroSys 2025 (Best Paper), arXiv 2405.16444. Non-prefix KV reuse, which matters when retrieved or tool text is re-inserted at different positions. It reports "TTFT by 2.2-3.3x and increases the inference throughput by 2.8-5x from full KV recompute without compromising generation quality." That was measured in a RAG setting, not an agent loop.\[12\]\[13\]
- *AAFLOW+* (arXiv 2607.10987, 2026). A search snippet reports a 7.60× speedup over SGLang prefix caching at 16 agents (Mistral, HF backend).\[14\] I have not verified this beyond the snippet.

**Implementations and reported gains (provider level).**
- Anthropic's prompt-caching docs: "Cache read tokens are 0.1 times the base input tokens price" (exceptions: 0.025× on Claude Fable 5.1 and Claude Mythos 5.1, and 0.05× on Claude Opus 5.5). Cache writes carry a premium: 1.25× base for the 5-minute TTL, and 2× base for the 1-hour TTL.
- OpenAI's Prompt Caching 201 cookbook: caching "can reduce time-to-first-token latency by up to 80% and input token costs by up to 90%," and it is automatic.\[15\]
- *Don't Break the Cache: An Evaluation of Prompt Caching for Long-Horizon Agentic Tasks* — Lumer et al., arXiv 2601.06007 (2026). Covers more than 500 DeepResearch Bench sessions with 10,000-token system prompts across OpenAI, Anthropic and Google. Caching "reduces API costs by 41-80% and improves time to first token by 13-31%." Naive full-context caching "can paradoxically increase latency."\[16\] Excluding dynamic tool results from the cached block works better.\[17\]

**Implementations and reported gains (cross-task output reuse).**
- *Agentic Plan Caching (APC)* — Zhang et al., NeurIPS 2025, arXiv 2506.14852. Extracts plan templates from completed runs, matches new tasks by keyword, and adapts the template with a lightweight model. It reports "reduce costs by 50.31% and latency by 27.28% on average while maintaining performance" (96.61% of optimal application performance across five workloads).\[18\]\[19\]
- *Agent Workflow Memory (AWM)* — Wang et al., ICML 2025, arXiv 2409.07429. Induces reusable workflows. It gives +24.6% and +51.1% relative success on Mind2Web and WebArena, and on WebArena takes "about 2.0 fewer steps per example than the BrowserGym baseline."\[20\]\[21\]

**Open problems.** (1) Tool pauses are variable and heavy-tailed, so retention policies need tool-latency prediction; TraceLab lists "semantic-aware tool-latency prediction" as an opportunity.\[22\] (2) Output caches (plans, workflows) have no staleness or invalidation semantics when the environment changes. (3) Cache economics collide with context management: any compaction or edit of history breaks the prefix, so compression and caching must be co-designed. (4) Cross-model KV sharing for heterogeneous multi-agent systems is immature.

### 2.3 Continuous batching → program-level scheduling, batched/parallel tool calls

**Inference mechanism.** Iteration-level scheduling admits and evicts requests at every decode step, keeping the GPU saturated despite variable lengths.

**Agent analogue.** Scheduling at the level of the agent *program*: prioritize by cumulative program service, avoid head-of-line blocking across calls, and batch or parallelize independent tool calls and LLM calls within a program's DAG.

**Implementations and reported gains.**
- *Autellix: An Efficient Serving Engine for LLM Agents as General Programs* — Luo et al., arXiv 2502.13965 (2025). Program-level attained-service schedulers (PLAS/ATLAS) and a locality-aware load balancer. It "improves throughput of programs by 4-15x at the same latency compared to state-of-the-art systems, such as vLLM," and by up to 1.5× over standard load balancers.\[1\]\[23\]
- *Parrot: Efficient Serving of LLM-based Applications with Semantic Variable* — Lin et al., OSDI 2024, arXiv 2405.19888. Exposes the application dataflow to the service, enabling DAG-aware scheduling, batching and prefix sharing. It reports "up to 11.7× speedup or 12× higher throughput compared with the state-of-the-art solutions."\[24\]\[25\]
- *An LLM Compiler for Parallel Function Calling (LLMCompiler)* — Kim et al., ICML 2024, arXiv 2312.04511. Plans a DAG of function calls and executes independent ones in parallel. It reports "latency speedup of up to 3.7×, cost savings of up to 6.7×, and accuracy improvement of up to ~9%" versus ReAct, and up to 35% faster than OpenAI parallel function calling.\[26\]\[27\]
- Continuum (above) is also a scheduler, using program-level FCFS.\[28\]

**Open problems.** (1) Schedulers are non-clairvoyant about remaining steps. Predicting remaining program length is the agent analogue of output-length prediction and is largely unsolved. (2) Joint scheduling of GPU and tool/sandbox resources: tool calls longer than 1 minute are only 4% of all tool calls but account for 85% of total tool-call time (TraceLab). (3) Stateful APIs: most provider APIs remain stateless, so program-level context (Autellix's sessions, Parrot's semantic variables) is not available on the provider side.

### 2.4 Distillation / draft models → small action models, cascades and routing

**Inference mechanism.** Train a smaller model to imitate a larger one, either as a replacement (distillation) or as a proposer (draft).

**Agent analogue.** Small models specialized on agent trajectories or function calling handle routine steps. Routers or cascades escalate only hard steps to the frontier model.

**Implementations and reported gains.**
- *Small Language Models are the Future of Agentic AI* — Belcak et al., NVIDIA, arXiv 2506.02153 (2025). A **position paper**: it argues SLMs are "sufficiently powerful, inherently more suitable, and necessarily more economical for many invocations in agentic systems." It introduces no new benchmark, so treat it as an argument, not a measurement.\[29\]\[30\]
- *FireAct: Toward Language Agent Fine-tuning* — Chen et al., arXiv 2310.05915 (2023). Fine-tuning Llama-2-7B on 500 GPT-4 trajectories gives "a 77% HotpotQA performance increase." Fine-tuned GPT-3.5 cut inference time about 70% (9.0 s → 2.7 s per trial) versus prompted GPT-3.5, largely because the few-shot context disappears.\[31\]
- *Octopus v2: On-device language model for super agent* — Chen & Li, arXiv 2404.01744 (2024). A 2B function-calling model fine-tuned from Gemma 2B with functional tokens. It claims to beat GPT-4 on its Android-API benchmark in accuracy and latency, save over 95% of context length during inference, and give a 35× latency improvement over Llama-7B+RAG. The benchmark is narrow (about 20 Android APIs).
- *RouteLLM: Learning to Route LLMs with Preference Data* — Ong et al., arXiv 2406.18665 (2024; ICLR 2025). Cost savings "up to 3.66x" on MT-Bench at 95% of GPT-4 quality, but only 1.41× on MMLU and 1.49× on GSM8K.\[32\] This is single-turn, not agentic.
- *FrugalGPT* — Chen et al., arXiv 2305.05176 (2023). An LLM cascade reported to match the best individual LLM with up to 98% cost reduction on its benchmarks.\[33\]\[34\] This is single-query, not agentic.
- *Agentic Plan Caching* (above) uses a lightweight model to adapt cached plans.\[19\] This is the "draft from memory" pattern.

**Interpretation.** The best-evidenced gain from small action models is less context per step (FireAct, Octopus): fine-tuning removes instructions and few-shot examples, so each step's prefill shrinks. Evidence that a small model can run *whole* long-horizon agent trajectories at frontier quality is thin in what I verified. Routing results come mostly from single-turn benchmarks.

**Open problems.** (1) Per-step routing inside trajectories, where one bad cheap step compounds. (2) Distillation targets that preserve recovery behaviour, not just happy paths. (3) Continual re-distillation from production traces (the "data flywheel" NVIDIA argues for) with measured end-to-end cost per solved task.\[35\]

### 2.5 Early exit / adaptive computation → skipping model calls for already-determined steps

**Inference mechanism.** Stop computing (exit layers, stop reasoning) once confidence is high enough, so compute adapts to difficulty.

**Agent analogue.** (a) Early termination of the agent loop. (b) Grouping several actions into one model call. (c) Replacing model calls with deterministic code for steps whose outcome is already determined. (d) Serving whole plans from cache (2.2).

**Implementations and reported gains.**
- *Runaway is Ashamed, But Helpful: On the Early-Exit Behavior of LLM-based Agents in Embodied Environments* — Lu et al., arXiv 2505.17616 (2025). Intrinsic exit prompts and an extrinsic YES/NO verifier reduce redundant steps "by approximately 50% to 70%" across ALFWorld, BabyAI, ScienceWorld, PDDL and Jericho. There is an accuracy cost: on ALFWorld with Llama-3.1-70B, steps fell 19.0 → 13.4 while success fell 76.1 → 70.2.\[36\]
- *OSWorld-Human: Benchmarking the Efficiency of Computer-Use Agents* — Abhyankar et al., arXiv 2506.16042 (MLSys 2026). Human-annotated minimal and "grouped-action" trajectories for all 369 OSWorld tasks. Even top agents take 1.4–2.7× more steps than necessary. Grouping actions that share one observation lets a single planning call cover several actions.\[37\]\[38\] This is a measured *opportunity*, not a deployed system.
- *Compiled AI: Deterministic Code Generation for LLM-Based Workflow Automation* — Trooskens et al., arXiv 2604.05150 (2026; industry preprint, not peer reviewed). On BFCL (n=400) it reports "96% task completion with zero execution tokens," break-even at about 17 transactions, and 57× lower token consumption at 1,000 transactions. Median latency is 4.5 ms vs 2,004 ms.\[39\]
- *Efficient Agents: Building Effective Agents While Reducing Cost* — Wang et al. (OPPO), arXiv 2508.02694 (2025). An ablation on GAIA sizes framework complexity to the task and retains "96.7% of the performance of OWL… while reducing operational costs from $0.398 to $0.228, resulting in a 28.4% improvement in cost-of-pass."\[40\]
- Agentic Plan Caching and AWM (2.2) also belong here: both avoid regenerating plans or steps.

**Open problems.** (1) Calibrated "is this step determined?" signals. Existing early exit trades 5–6 points of success for 30% fewer steps. (2) Automatic, verified compilation of recurring sub-trajectories into code, with a fallback to the LLM when preconditions fail. (3) Deciding at runtime, per step, how much reasoning budget to spend. I found no verified agent-specific study with step-level numbers, so this remains a gap in the evidence I checked.

### 2.6 Quantization → reduced-fidelity context (the weakest analogy)

**Inference mechanism.** Represent weights, activations or KV at lower precision, trading bounded, usually small, accuracy loss for memory bandwidth and throughput on *every* token.

**Candidate agent analogues, evaluated.**
1. **Lossy compression of what is re-read each step (strongest mapping).** Like quantization, it lowers the "precision" of a representation that is touched on every step, it is lossy, and it applies across the whole trajectory.
   - *The Complexity Trap: Simple Observation Masking Is as Efficient as LLM Summarization for Agent Context Management* — Lindenbauer et al. (JetBrains), arXiv 2508.21433 (NeurIPS 2025 DL4Code workshop). On SWE-bench Verified with SWE-agent across five model configurations, masking old observations "halves cost relative to the raw agent while matching, and sometimes slightly exceeding, the solve rate of LLM summarization." Without context management, costs "can more than double." A hybrid cuts a further 7–11% and adds 2.6 points of solve rate.\[41\]\[42\]\[43\]
   - *Reducing Cost of LLM Agents with Trajectory Reduction (AgentDiet)* — Xiao et al., Proc. ACM Softw. Eng. (FSE 2026), arXiv 2509.23586. Removes useless, redundant and expired trajectory content, reducing "input tokens by 39.9%–59.7% and the total computational cost by 21.1%–35.9%, while maintaining the same agent performance."\[44\]\[45\]\[46\]
   - *LLMLingua* — Jiang et al., EMNLP 2023, arXiv 2310.05736. Prompt compression "up to 20x compression with little performance loss" on GSM8K, BBH, ShareGPT and Arxiv.\[47\] This is a single-prompt setting, not agent loops.
2. **Per-step routing to cheaper models (2.4).** This is a closer analogue of "lower precision compute," but it is really a cascade, not a uniform precision reduction.
3. **Reduced-fidelity observations** (accessibility trees vs. screenshots). This is plausible, but I did not verify a controlled cost study, so treat it as unverified.

**Where the analogy breaks.** Quantization error is roughly uniform, local and measurable per layer. Context compression error is *non-local*: a dropped observation can matter 30 steps later. Compression also interacts badly with prefix caching, because every edit invalidates the cached prefix. Quantization keeps the arithmetic; compression changes the information.

**Open problems.** Compression that respects cache boundaries (compress only at cache-epoch boundaries). Learned "precision schedules" for history (recent at full fidelity, old masked). Error bounds on downstream task success.

## 3. The cost-unit shift: evidence that steps, not tokens, dominate

**(a) Latency per step is prefill- and tool-bound.**
- TraceLab (Zhu et al., University of Washington, arXiv 2606.30560, 2026) is a trace of 4,265 real Claude Code/Codex sessions with 357,161 LLM steps and 432,510 tool calls from 43 developers (Sep 2025–Jun 2026). It characterizes coding-agent workloads as "long autonomous loops, long contexts with short outputs, diverse and heavily-tailed tool calls, and high but imperfect prefix cache hit rates": the global prefix cache hit rate is 95.7%, yet cache misses cause 3.8× more tokens to be prefilled than truly unique input tokens do, and tool calls longer than 1 minute are only 4% of calls but 85% of total tool-call time. On average a request takes 8.8 LLM calls, 10.8 tool invocations and 4.3 minutes (p90 above 6.4 minutes). "Long contexts with short outputs" is the key token-vs-step fact: each step is prefill-heavy and decode-light, so decode-side optimizations such as speculative decoding address the smaller term.
- OSWorld-Human (arXiv 2506.16042) finds that planning calls take "more than half, sometimes close to 75% of the total task latency." Judging/reflection take a further 22.5% (GTA1) and 33.6% (Agent S2). "Each successive step can take 3× longer than steps at the beginning of a task," consistent with growing context.\[48\]\[49\]

**(b) Steps per task multiply cost.** Real coding-agent requests average 8.8 LLM calls and 10.8 tool calls (TraceLab). Computer-use agents take 1.4–2.7× more steps than human-minimal trajectories (OSWorld-Human), and a single grounding error can add up to 30 extra steps.\[37\]\[48\] AWM's reuse removes about 2 steps per WebArena task.\[21\] Benchmark-specific turn counts for τ-bench, GAIA and Terminal-Bench were not verified in this research, so I do not quote them.

**(c) Re-reading a growing context is roughly quadratic.** With a fixed prefix P (system prompt plus tools) and d new tokens appended per step, an uncached N-step trajectory processes about N·P + d·N(N−1)/2 input tokens. This is my derivation, not a sourced figure. At 10,000-token prompts over 50 steps, the prefix alone is 500k input tokens. Caching changes the constant, not the shape: the 0.1× read price (Anthropic), up to 90% off and up to 80% lower TTFT (OpenAI), and measured 41–80% cost and 13–31% TTFT reductions on real agent sessions (Don't Break the Cache).\[15\]\[16\]\[17\]\[50\] Context management attacks the quadratic term directly: observation masking halves cost and AgentDiet cuts input tokens 40–60%.\[44\]\[46\]\[51\] A second cost of long histories is quality. Chroma's *Context Rot* technical report (Hong, Troynikov, Huber, July 2025, not peer reviewed) evaluated 18 LLMs, including GPT-4.1, Claude 4, Gemini 2.5 and Qwen3, and found that "model performance consistently degrades with increasing input length," even on simple tasks of fixed difficulty.\[52\]

**(d) Cost-controlled evaluation.** *AI Agents That Matter* (Kapoor et al., arXiv 2407.01502, 2024) argues benchmarks' "narrow focus on accuracy" has made SOTA agents "needlessly complex and costly," and calls for jointly optimizing cost and accuracy.\[53\] Follow-ups operationalize this. Efficient Agents uses *cost-of-pass* (expected dollars per correct solution).\[54\] OSWorld-Human proposes step-efficiency metrics against human-minimal trajectories.\[38\] Autellix and Continuum report program-level JCT instead of TTFT/TPOT. None of the work I verified proposes a standard accounting unit of "model calls per solved task plus prefill tokens per task." That is the gap.

## 4. Summary table

| Inference technique | Agent analogue | Papers (with year) | Reported gains | Open problem |
|---|---|---|---|---|
| Speculative decoding | Speculative / parallel actions; draft agent proposes, actor verifies; async tool calls | Speculative Actions (Ye et al., 2025); Speculate with Memory (Li et al., 2026); Interactive Speculative Planning (Hua et al., 2024); DSP (Guan et al., 2025); AsyncLM (Gim et al., 2024) | Up to 55% action-prediction accuracy → up to 20% latency reduction; memory raises hit rate 19–39% (est. >50% latency reduction on ALFWorld); 19–42% total-time reduction at higher $ cost; −30% total cost vs. fastest lossless; 1.6–5.4× latency on BFCL | Side-effecting actions (rollback); semantic verification; bounded-cost multi-step speculation |
| KV / prefix caching | Program-aware KV retention across tool pauses; provider prompt caching; cross-task plan/workflow reuse | KVFlow (Pan et al., 2025); Continuum (Li et al., 2025); CacheBlend (Yao et al., 2025); Don't Break the Cache (Lumer et al., 2026); Agentic Plan Caching (Zhang et al., 2025); AWM (Wang et al., 2024) | Up to 1.83×/2.19× vs SGLang HiCache; >8× avg JCT; 2.2–3.3× TTFT (RAG); −41–80% cost, −13–31% TTFT; −50.31% cost, −27.28% latency; +51.1% rel. success, ~2 fewer steps (WebArena) | Tool-latency-aware retention; invalidation of cached plans; co-design with context compaction |
| Continuous batching | Program-level scheduling; parallel/batched function calls; DAG-aware serving | Autellix (Luo et al., 2025); Parrot (Lin et al., 2024); LLMCompiler (Kim et al., 2023/2024); Continuum (2025) | 4–15× program throughput at same latency; up to 11.7× speedup / 12× throughput; up to 3.7× latency, 6.7× cost, ~9% accuracy | Predicting remaining steps; joint GPU+tool scheduling; stateful provider APIs |
| Distillation / draft models | Small action models; trajectory fine-tuning; routers/cascades | SLMs are the Future of Agentic AI (Belcak et al., 2025, position); FireAct (Chen et al., 2023); Octopus v2 (Chen & Li, 2024); RouteLLM (Ong et al., 2024); FrugalGPT (Chen et al., 2023) | +77% HotpotQA (Llama-2-7B), −70% inference time; 35× latency, −95% context (narrow API set); up to 3.66× cost saving at 95% GPT-4 quality (single-turn); up to 98% cost reduction (single-query) | Per-step routing inside trajectories; distilling recovery behaviour; end-to-end cost-per-solve evidence |
| Early exit / adaptive computation | Early loop termination; action grouping; compile determined steps to code; plan reuse | Runaway is Ashamed (Lu et al., 2025); OSWorld-Human (Abhyankar et al., 2025); Compiled AI (Trooskens et al., 2026, preprint); Efficient Agents (Wang et al., 2025); APC (2025) | −50–70% redundant steps (with ~6-pt success drop in one setting); agents take 1.4–2.7× more steps than needed; 57× fewer tokens at 1,000 runs, 96% completion; 96.7% of OWL performance at −28.4% cost-of-pass | Calibrated "step is determined" signals; verified auto-compilation with fallback; per-step reasoning budgets |
| Quantization | Lossy compression of re-read context (observation masking, trajectory pruning, prompt compression); cheaper-model routing | Complexity Trap (Lindenbauer et al., 2025); AgentDiet (Xiao et al., 2025/2026); LLMLingua (Jiang et al., 2023) | ~50% cost at equal solve rate (SWE-bench Verified); −39.9–59.7% input tokens, −21.1–35.9% cost; up to 20× compression (single prompts) | Non-local error; conflict with prefix caching; no error bounds on task success |

## 5. Caveats

- Most gains are "up to" figures on the authors' own workloads. Serving numbers (Autellix, Parrot, KVFlow, Continuum) are against specific baselines and hardware and are not additive.
- Several sources are preprints or non-peer-reviewed: Compiled AI (industry preprint), Context Rot (vendor technical report), AAFLOW+ (snippet only). Octopus v2 is evaluated on a narrow API set.
- Candidate leads not verified in this research and therefore omitted: Dynamic Cheatsheet, Voyager, Alita, xLAM, AgentTuning, Agent-FLAN, Teola, KVShare, and benchmark-specific step counts for SWE-bench/τ-bench/GAIA/Terminal-Bench.
- Provider pricing multipliers change often. The docs cited here reflect the pages as retrieved in September 2026.

## 6. Recommendations for researchers

1. Report agent efficiency in step units: model calls per solved task, prefill vs. decode tokens per task, cache-hit rate, and wall-clock split into LLM, tool and queueing time. Pair this with cost-of-pass.
2. Prioritize work that removes or shrinks steps (plan and workflow reuse, compilation, action grouping, context masking) over per-token speedups. The evidence shows prefill-heavy, decode-light steps.
3. Co-design caching with compression: compress only at cache-epoch boundaries and keep dynamic tool results out of cached blocks.\[55\]
4. For speculation, build explicit side-effect semantics (read-only, reversible, transactional) into tool interfaces. Without them, speculative actions stay limited to about 20% gains.

## 7. Single-slide thesis

In agentic workloads the unit of cost is the step, not the token. A coding-agent request averages 8.8 LLM calls and 10.8 tool calls (TraceLab), each call re-prefilling a context that grows every turn, interleaved with heavy-tailed tool latency, so cost grows roughly quadratically in history and linearly in step count. Every classic inference optimization therefore has a step-level twin: speculation over actions, KV and plan caching across steps and tasks, program-level batching and scheduling, small action models, early exit by skipping or compiling determined steps, and lossy compression of the re-read context. The largest verified gains (2–15× serving throughput, 30–70% fewer steps or cost) come from treating the *agent program* as the unit to schedule, cache and prune. The next frontier is step-level accounting plus verifiers that know when a cheaper step is safe.

## Sources

1. [Autellix: An Efficient Serving Engine for LLM Agents as General Programs](https://arxiv.org/html/2502.13965v1)
2. [Speculative Actions: A Lossless Framework for Faster Agentic Systems](https://arxiv.org/pdf/2510.04371)
3. [Speculate with Memory: Lossless Acceleration for LLM Agents](https://arxiv.org/pdf/2607.12236)
4. <https://arxiv.org/pdf/2410.00079>
5. [Published as a conference paper at ICLR 2026 DYNAMIC SPECULATIVE AGENT PLANNING](https://proceedings.iclr.cc/paper_files/paper/2026/file/0d1986a61e30e5fa408c81216a616e20-Paper-Conference.pdf)
6. [Dynamic Speculative Agent Planning](https://arxiv.org/abs/2509.01920)
7. [Asynchronous LLM Function Calling](https://arxiv.org/abs/2412.07017)
8. [Prompt Caching in 2026: Cut Your LLM API Costs by Up to 90% | DevToolLab Blog](https://devtoollab.com/blog/prompt-caching-guide)
9. [KVFlow: Efficient Prefix Caching for Accelerating LLM-Based Multi-Agent Workflows | OpenReview](https://openreview.net/forum?id=5Iw1nDtYmT)
10. [KVFlow: Efficient Prefix Caching for Accelerating LLM-Based Multi-Agent Workflows](https://proceedings.neurips.cc/paper_files/paper/2025/hash/b7971d31a7d5eb0f1eed2f8f6f368195-Abstract-Conference.html)
11. [Continuum: Efficient and Robust Multi-Turn LLM Agent Scheduling with KV Cache Time-to-Live](https://arxiv.org/abs/2511.02230)
12. [CacheBlend: Fast Large Language Model Serving for RAG with Cached Knowledge Fusion](https://arxiv.org/abs/2405.16444)
13. [EuroSys](https://www.eurosys.org/)
14. [\[AAFLOW+\] Stateful Operator Abstraction with Zero-Copy Distributed KV Cache Orchestration for Multi-Agent Workflows](https://arxiv.org/pdf/2607.10987)
15. [Prompt Caching 201](https://developers.openai.com/cookbook/examples/prompt_caching_201)
16. [Prompt Caching in 2026: Cut LLM Costs, Keep Quality](https://www.digitalapplied.com/blog/prompt-caching-2026-cut-llm-costs-engineering-guide)
17. [Don't Break the Cache: An Evaluation of Prompt Caching for Long-Horizon Agentic Tasks](https://arxiv.org/abs/2601.06007)
18. [Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents](https://arxiv.org/pdf/2506.14852)
19. [Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents](https://arxiv.org/abs/2506.14852)
20. [\[2409.07429\] Agent Workflow Memory](https://arxiv.org/abs/2409.07429)
21. [Agent Workflow Memory](https://arxiv.org/pdf/2409.07429)
22. <https://arxiv.org/pdf/2606.30560>
23. [Paper page - Autellix: An Efficient Serving Engine for LLM Agents as General Programs](https://huggingface.co/papers/2502.13965)
24. [GitHub - microsoft/ParrotServe: \[OSDI'24\] Serving LLM-based Applications Efficiently with Semantic Variable · GitHub](https://github.com/microsoft/ParrotServe)
25. [Parrot: Efficient Serving of LLM-based Applications with ...](https://www.usenix.org/system/files/osdi24-lin-chaofan.pdf)
26. [An LLM Compiler for Parallel Function Calling](https://arxiv.org/pdf/2312.04511)
27. [\[2312.04511v2\] An LLM Compiler for Parallel Function Calling](https://arxiv.org/abs/2312.04511v2)
28. [Continuum: Efficient and Robust Multi-Turn LLM Agent Scheduling with KV Cache Time-to-Live - ADS](https://ui.adsabs.harvard.edu/abs/2025arXiv251102230L/abstract)
29. [NVIDIA's Peter Belcak Distills Why Small Language Models are the Future of Agentic AI - Arize AI](https://arize.com/blog/nvidias-small-language-models-are-the-future-of-agentic-ai-paper/)
30. [\[2506.02153\] Small Language Models are the Future of Agentic AI](https://arxiv.org/abs/2506.02153)
31. [FireAct: Toward Language Agent Fine-tuning](https://fireact-agent.github.io/)
32. [RouteLLM: Learning to Route LLMs with Preference Data](https://arxiv.org/pdf/2406.18665)
33. [AI Model Routing: Cost and Quality Optimization Guide | IntuitionLabs](https://intuitionlabs.ai/articles/ai-model-routing-cost-quality)
34. [How Semantic Routing Cut My LLM Costs by 70% Without Touching Model Quality - DEV Community](https://dev.to/robat_das_3c6e956212f6408/how-semantic-routing-cut-my-llm-costs-by-70-without-touching-model-quality-1hdp)
35. [NVIDIA Says Small Language Models Are The Future of Agentic AI](https://cobusgreyling.substack.com/p/nvidia-says-small-language-models)
36. <https://arxiv.org/pdf/2505.17616>
37. [GitHub - WukLab/osworld-human: OSWorld-Human: Benchmarking the Efficiency of Computer-Use Agents · GitHub](https://github.com/WukLab/osworld-human)
38. [1 Introduction](https://arxiv.org/html/2506.16042v2)
39. [Compiled AI: Deterministic Code Generation for LLM-Based Workflow Automation](https://arxiv.org/pdf/2604.05150)
40. [\[2508.02694\] Efficient Agents: Building Effective Agents While Reducing Cost](https://arxiv.org/abs/2508.02694)
41. [The Complexity Trap: Simple Observation Masking Is](https://arxiv.org/pdf/2508.21433)
42. [\[2508.21433\] The Complexity Trap: Simple Observation Masking Is as Efficient as LLM Summarization for Agent Context Management](https://arxiv.org/abs/2508.21433)
43. [GitHub - JetBrains-Research/the-complexity-trap: This repo accompanies the paper "The Complexity Trap: Simple Observation Masking Is as Efficient as LLM Summarization for Agent Context Management" presented at the Fourth Deep Learning for Code (DL4Code) workshop at NeurIPS 2025 and Tobias Lindenbauer's Master's Thesis. · GitHub](https://github.com/JetBrains-Research/the-complexity-trap)
44. [Improving LLM Efficiency via Trajectory Reduction](https://www.emergentmind.com/papers/2509.23586)
45. [Improving the Efficiency of LLM Agent Systems through Trajectory Reduction](https://arxiv.org/html/2509.23586v1)
46. <https://arxiv.org/pdf/2509.23586>
47. [LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models](https://arxiv.org/abs/2310.05736)
48. [OSWorld-Human: Benchmarking the Efficiency of Computer-Use Agents](https://arxiv.org/pdf/2506.16042)
49. [\[2506.16042\] OSWorld-Human: Benchmarking the Efficiency of Computer-Use Agents](https://arxiv.org/abs/2506.16042)
50. [Prompt caching - Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
51. [The Complexity Trap: Simple Observation Masking Is as Efficient as LLM Summarization for Agent Context Management | OpenReview](https://openreview.net/forum?id=OHVzruJl5k)
52. [Context Rot: How Increasing Input Tokens Impacts LLM Performance](https://www.trychroma.com/research/context-rot)
53. [AI Agents That Matter](https://arxiv.org/abs/2407.01502)
54. [Efficient Agents: Building Effective Agents While Reducing Cost](https://arxiv.org/pdf/2508.02694)
55. [Prompt Caching for AI Agents: Architecture Patterns for Cost and Latency Optimization | Zylos Research](https://zylos.ai/research/2026-02-24-prompt-caching-ai-agents-architecture/)
