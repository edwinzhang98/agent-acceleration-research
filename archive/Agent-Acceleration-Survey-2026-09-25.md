# Agent acceleration: research landscape, 2023–2026
Evidence cutoff: **25 September 2026**. Primary-source survey emphasizing web, GUI, computer-use and long multi-step agents.

The most convincing opportunities are eliminating repeated reasoning through executable routines, exploiting independent work, and reusing exact inference state. Learned routing, observation compression, and shorter reasoning can also help, but often trade away quality. Reported improvements are not interchangeable: fewer steps, lower time-to-first-token, higher server throughput, and shorter completed-task latency measure different things.

**Labels:** S = structurally/conditionally semantics-preserving; E = measured aggregate quality preserved or improved, not a losslessness proof; L = observed quality decline at the cited setting; NR = numerical quality or efficiency comparison not reported/verified. SR = success rate; pp = percentage points. Unless explicitly called calculated, numbers below are paper table values or reported results. Dollar amounts use the paper's prices. An arXiv label means a refereed venue was not verified.

## 1. Fewer model calls: skills, macros, APIs and compiled demonstrations

| Paper; authors/lab; venue/year | Mechanism | Verified efficiency and accuracy | Status/limits |
|---|---|---|---|
| [AutoDroid-V2: Boosting SLM-based GUI Agents via Code Generation](https://arxiv.org/html/2412.18116v3) — Hao Wen et al.; Tsinghua AIR; MobiSys 2025, preprint 2024 | Generate a complete executable GUI script from learned app documentation. | DroidTask: AutoDroid→V2 model-inference time **669.2→46.3 s/task (−93.1%)**; SR **43.9→54.4%**. Table 2, §4.3. | E; inference time, not full wall clock; preparation/training excluded. |
| [AppAgentX: Evolving GUI Agents as Proficient Smartphone Users](https://arxiv.org/html/2503.02268v2) — Wenjia Jiang et al.; Westlake/A*STAR collaborators; arXiv 2025 | Turn recurring action chains into parameterized shortcuts with atomic-action fallback. | AndroidWorld, AppAgent→AppAgentX: **147.17→59.74 s/task**, **18.9K→6.2K tokens**, SR **41.7→62.5%**. Table 2. | E; timing uses tasks successfully completed by every compared method. |
| [UFO2: The Desktop AgentOS](https://arxiv.org/html/2504.14603v2) — Chaoyun Zhang et al.; Microsoft; [TMLR 2026](https://www.microsoft.com/en-us/research/publication/ufo2-the-desktop-agentos/), preprint 2025 | Combine Windows GUI control with native application APIs. | o1 GUI-only→GUI+API: **16.0→6.6 completion steps**, SR **16.3→24.5%**; API ablation using Office-related OSWorld tasks, Table 5. | E; steps on common-success tasks; no isolated wall-clock/cost result. |
| [GPA: Learning GUI Process Automation from Demonstrations](https://arxiv.org/pdf/2604.01676) — Zirui Zhao et al.; Salesforce AI Research; arXiv 2026 | Compile a demonstration into locally matched GUI transitions, avoiding runtime LLM decisions. | Desktop pilot: Gemini 3 Pro→GPA **329.31→33.74 s**, SR **89.38→100%**; **16 tasks**, Table 2. | E; small repeated-workflow pilot; not general decision-making or lossless equivalence. |
| [Agent JIT Compilation for Latency-Optimizing Web Agent Planning and Scheduling](https://arxiv.org/html/2605.21470v1) — Caleb Winston, Ron Yifeng Wang, Azalia Mirhoseini, Christos Kozyrakis; Stanford; arXiv 2026 | Compile tasks into latency-selected code plans using reusable tools with state pre/postconditions. | GPT-4.1, Browser-Use→JIT-Planner: **150.1→15.4 s (9.7×)**; SR **61→90%**. Table 1; **37 tasks across 5 web apps**. | E; selected REAL/WebArena-derived tasks; offline tool creation/trace collection excluded. |

Foundations: [Large Language Models as Tool Makers (LATM)](https://arxiv.org/html/2305.17126v2), Tianle Cai et al., Google DeepMind/Princeton/Stanford, arXiv 2023 / ICLR 2024, established reusable generated Python tools and cheap tool users. Its model-price ratio is not a measured task speedup.

HCI lineage: [DiLogics: Creating Web Automation Programs with Diverse Logics](https://web.eecs.umich.edu/~xwangsd/pubs/uist23b.pdf), Kevin Pu et al., UIST 2023, and [ALLOY: Generating Reusable Agent Workflows from User Demonstration](https://arxiv.org/html/2510.10049v1), Jiawen Li et al., arXiv 2025, inform demonstration-to-program design. Comparable agent runtime/cost-versus-success numbers were not verified; ALLOY's user ratings are not objective task accuracy.

## 2. Cross-task plan, workflow and trajectory caching

| Paper; authors/lab; venue/year | Mechanism | Verified efficiency and accuracy | Status/limits |
|---|---|---|---|
| [Agent Workflow Memory](https://proceedings.mlr.press/v267/wang25bx.html) — Zora Zhiruo Wang, Jiayuan Mao, Daniel Fried, Graham Neubig; CMU/MIT; ICML 2025, preprint 2024 | Extract abstract workflows from successful trajectories and retrieve them for later tasks. | WebArena/GPT-4, accessibility-tree BrowserGym→AWM: **7.9→5.9 steps**, SR **15.0→35.5%**. [Table 1](https://arxiv.org/html/2409.07429v1). | E; textual guidance, not automatic executable replay; runtime NR. |
| [Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents](https://arxiv.org/html/2506.14852v2) — Qizheng Zhang, Michael Wornow, Kunle Olukotun; Stanford; [NeurIPS 2025](https://papers.nips.cc/paper_files/paper/2025/hash/9549f7d06700f0966d5f938f1d11022a-Abstract-Conference.html) | Retrieve plan templates and adapt them with a cheaper planner. | GAIA/Open Deep Research: total benchmark cost **$69.02→$16.27 (−76.42%)**; accuracy **37.58→36.97% (−0.61 pp)**. Table 1. | L; costs are benchmark totals, not per task. |
| [AgenticCache: Cache-Driven Asynchronous Planning for Embodied AI Agents](https://arxiv.org/html/2604.24039v1) — Hojoon Kim, Yuheng Wu, Thierry Tambe; SNU/Stanford; [MLSys 2026](https://proceedings.mlsys.org/paper_files/paper/2026/hash/c66a9db149261435664284a20b6f1d42-Abstract-Conference.html) | Reuse cached plan transitions while an asynchronous updater validates/refines them. | GPT-5, TDW-COOK: **12.86→1.75 h**, **$21.0→$4.4**, SR **94.44→100%**. TDW-MAT: **41.34→22.27 h**, SR **90.23→88.64%**. Table 2. | E/L by workload; warm cache; embodied simulation totals, not GUI-task timing. |
| [Executable Agentic Memory for GUI Agent](https://arxiv.org/html/2605.12294v1) — Zerui Qin et al.; Tsinghua/Sun Yat-sen; arXiv 2026 | Retrieve executable paths from a persistent GUI transition graph using a small value model. | GPT-4o→EAM: average per-step **9.3→2.8 s**, **50.8K→8.3K API tokens**; AndroidWorld SR **34.5→52.6%**. Tables 1–2. | E; efficiency aggregated across evaluated mobile benchmarks; preparation costs excluded. |

Plan reuse is approximate semantic reuse; prefix caching in family 6 reuses exact model computation. Their correctness conditions differ.

## 3. Speculative actions and planning

| Paper; authors/lab; venue/year | Mechanism | Verified efficiency and accuracy | Status/limits |
|---|---|---|---|
| [Speculative Actions: A Lossless Framework for Faster Agentic Systems](https://arxiv.org/html/2510.04371v2) — Naimeng Ye et al.; Columbia; ICLR 2026, preprint 2025 | Stage predicted actions and commit only after authoritative actor agreement. | Chess/GPT-5: **19.5% lower mean execution time**; next-action prediction accuracy **54.7%**; paired task-success percentage NR. §3.1.2. | Conditional S; prediction accuracy is not task success; separate OS-tuning extension is lossy. |
| [Dynamic Speculative Agent Planning](https://arxiv.org/html/2509.01920v1) — Yilin Guan et al.; academic/Microsoft/DeepMind collaboration; ICLR 2026, preprint 2025 | Learn speculation depth online to balance waiting against wasted draft/verification work. | OpenAGI, GPT/CoT-MAD, offset=2: **37.09% latency reduction**, but **62.99% higher monetary cost** than sequential. Table 4. | Conditional S under target verification; task-success delta NR; faster does not mean cheaper. |
| [Act While Thinking: Accelerating LLM Agents via Pattern-Aware Speculative Tool Execution (PASTE)](https://arxiv.org/html/2603.18897v1) — Yifan Sui et al.; SJTU/Microsoft/Stevens; arXiv 2026 | Predict tool calls from recurring patterns, execute early, and promote exact matches. | DeepResearchBench/SWE-bench/ScholarQA workloads: **1.25× vs ORION**, **1.32× vs SpecFaaS**; audited final-result divergences **0**. §§7.2,7.6. | Conditional S plus empirical audit; task-success percentages NR. |
| [Speculative Macro Commit for Faster Tool-Using Agents](https://arxiv.org/html/2609.03236v1) — Zeyu Liu, Souvik Kundu, Peter A. Beerel; USC/Intel; arXiv 2026 | After verifying a draft's first action, commit a matching pre-executed macro. | τ² Telecom: **27.60→22.47 s (−18.59%)**, SR **99.52→99.52%**. AppWorld: **355.7→195.9 s (−44.93%)**, TGC **41.67→40.48%**. Table 1. | E on Telecom, L on AppWorld; verifying a macro's first action does not prove the rest equivalent. |

Lossless speculation requires valid isolation, matching, commit and recovery semantics. Merely adding a verifier does not establish this.

## 4. Parallelism, asynchronous calls and action batching

| Paper; authors/lab; venue/year | Mechanism | Verified efficiency and accuracy | Status/limits |
|---|---|---|---|
| [An LLM Compiler for Parallel Function Calling](https://proceedings.mlr.press/v235/kim24y.html) — Sehoon Kim et al.; Berkeley/SqueezeAILab; ICML 2024, preprint 2023 | Build a function-dependency DAG and dispatch independent calls concurrently. | Movie Recommendation/GPT-3.5: ReAct†→LLMCompiler **20.47→5.47 s (3.74×)**; accuracy **72.47→77.13%**. [Table 1](https://arxiv.org/pdf/2312.04511). | E on this pair; no unconditional losslessness; other workloads show small regressions. |
| [Concurrency without Model Changes: Future-based Asynchronous Function Calling for LLMs (AsyncFC)](https://arxiv.org/html/2605.15077v1) — Guangyu Feng et al.; Berkeley; arXiv 2026 | Return futures immediately so decoding and independent tool execution overlap. | Composed HotpotQA: **1.24× speedup**, accuracy **75.0→75.0%**. BFCL-v4 Web Search: **1.26×**, **54.8→53.2%**. | E/L; composed workloads; other experiments inject tool delays. |
| [Act More, Decide Less: Skill-Guided Adaptive Action Chunking for Long-Horizon LLM Agents (SPACE)](https://arxiv.org/html/2609.02042v1) — Yanting Yang et al.; Rutgers/Toronto/PolyU collaborators; arXiv 2026 | Train an agent to emit variable-length action chunks rather than individual actions. | ALFWorld unseen/Qwen3-4B, GiGPO→SPACE: **21.7→4.4 model rounds**, SR **72.7→96.9%**. Table 1. | E; fewer calls, not a measured wall-clock gain; text-based embodied environment. |
| [UFO2, multi-action ablation](https://arxiv.org/html/2504.14603v2) — Chaoyun Zhang et al.; Microsoft; TMLR 2026 | Batch predictable GUI actions before requesting another observation/decision. | o1, OSWorld-W: **6.80→3.30 steps**, SR **24.5→26.5%**. WindowsAgentArena: **9.95→8.85 steps**, SR **25.3→24.7%**. Table 7. | E/L; common-success step counts; not a draft-target losslessness protocol. |

## 5. Cheaper calls: routing, small action models and observation compression

| Paper; authors/lab; venue/year | Mechanism | Verified efficiency and accuracy | Status/limits |
|---|---|---|---|
| [Budget-Aware Agentic Routing via Boundary-Guided Training](https://arxiv.org/html/2602.21227v1) — Caiqi Zhang et al.; Cambridge/Microsoft M365; arXiv 2026 | Route each step between small and large models using trajectory-aware training. | AppWorld, large-call cap 15: always-large→BoPO uses **125%→88% of cap**, SR **66.7→66.5%**. Approximately **29.6% fewer expensive calls**, calculated from rounded Table 1. | L; not total dollar savings; router overhead excluded. |
| [FocusAgent: Simple Yet Effective Ways of Trimming the Large Context of Web Agents](https://arxiv.org/html/2510.03204v2) — Imene Kerboua et al.; LIRIS/Esker/ServiceNow/Mila; TMLR 2026, preprint 2025 | A smaller retriever selects relevant accessibility-tree lines for the actor. | WebArena/GPT-4.1: input-token cost **$59.0→$46.2 (−21.7%)**, SR **36.5→39.6%**. WorkArena: **$55.6→$38.1**, SR **53.6→53.2%**. Table 2. | E/L; includes retriever input charges but excludes output charges; not total bill. |
| [GoClick: Lightweight Element Grounding Model for Autonomous GUI Interaction](https://arxiv.org/html/2604.23941v1) — Hongxin Li, Yuntao Chen, Zhaoxiang Zhang; CAS; arXiv 2026 | Use a compact encoder-decoder for GUI grounding. | ShowUI→GoClick-B: TTFT **79.7→37.7 ms**, time/output-token **14.7→4.1 ms**; ScreenSpot **76.1→74.1%**, ScreenSpot-v2 **77.4→75.2%**. Table 3. | L on these benchmarks; single-L20, fixed-image grounding microbenchmark, not full tasks. |
| [TRACE: Trajectory-robust Admission with Evidence Ordering for Efficient GUI Agents](https://arxiv.org/html/2609.10297v1) — Yuhao Wang et al.; Dalian UT/OPPO/PolyU; arXiv 2026 | Select visual tokens and progressively compact reusable screenshot history. | OmniGUI/GUI-Owl: TTFT **1116.8→452.7 ms**, per-step inference **3014.7→2298.9 ms**; step SR **52.45→48.91%**. Tables 1,23. | L; cache-only ablation reaches **487.4 ms TTFT at unchanged accuracy**. |

Lower screenshot resolution and token pruning must be evaluated against small-text and coordinate errors. Grounding accuracy is not complete-task success. Exact prompt/prefix caching belongs in family 6 and should not be confused with dropping visual evidence.

## 6. Serving support: prefix/KV reuse and agent-aware scheduling

| Paper; authors/lab; venue/year | Mechanism | Verified efficiency | Accuracy/losslessness |
|---|---|---|---|
| [SGLang: Efficient Execution of Structured Language Model Programs](https://arxiv.org/html/2312.07104v2) — Lianmin Zheng et al.; Stanford/Berkeley/SJTU/TAMU; NeurIPS 2024, preprint 2023 | RadixAttention reuses exact prefixes across calls and branches. | Up to **6.4× throughput**, **3.7× lower single-program latency** across its LM-program suite, including agent traces, versus vLLM/Guidance/LMQL. §6. | S for exact-prefix reuse; task-success delta NR; suite maxima, not GUI-task speedups. |
| [Parrot: Efficient Serving of LLM-based Applications with Semantic Variable](https://arxiv.org/html/2405.19888v1) — Chaofan Lin et al.; SJTU/Microsoft; OSDI 2024 | Expose inter-call dependencies and shared prefixes for application-aware scheduling. | MetaGPT-style coding: up to **11.7× faster** than latency-centric and **2.45×** than throughput-centric baselines. §8.4. | S mechanism; quality NR; uses recorded response lengths for system-performance evaluation. |
| [Preble: Efficient Distributed Prompt Scheduling for LLM Serving](https://arxiv.org/html/2407.00023v2) — Vikranth Srivatsa et al.; UCSD WukLab; ICLR 2025 | Balance distributed prefix-cache locality against GPU load. | **1.5–14.5× lower mean request latency**, **2–10× lower p99**, across tool/embodied/code/video/long-context workloads. §4. | S mechanism; task-success delta NR; request latency, not workflow completion. |
| [Agentix: An Efficient Serving Engine for LLM Agents as General Programs](https://www.usenix.org/system/files/nsdi26-luo.pdf) — Michael Luo et al.; Berkeley/DeepMind/SJTU; NSDI 2026; formerly Autellix | Schedule at program level with preemption and locality-aware routing. | Mixed workload: up to **15× throughput vs vLLM**, **5× vs optimized vLLM**, at matched program-level normalized latency. §6.3. | S mechanism; accuracy NR; normalized latency = response time/generated tokens. |
| [Continuum: Efficient and Robust Multi-Turn LLM Agent Scheduling with KV Cache Time-to-Live](https://arxiv.org/html/2511.02230v7) — Hanchen Li et al.; Berkeley/Stanford/Tsinghua; arXiv 2025, revised September 2026 | Preserve KV state across tool waits using cost-aware TTL and program scheduling. | Replay workloads: **1.12–3.66× lower delay**, **1.10–3.22× throughput**, across SWE-Bench/BFCL/OpenHands. | S mechanism; real SWE-bench evaluation reports same-or-higher pass rates, but exact numerical delta not verified. |

Scheduling and exact reuse preserve the intended computation; absence of a quality evaluation still must not be reported as measured zero loss. Loaded-server gains may differ greatly from isolated-user latency gains.

## 7. Reasoning-budget control

| Paper; authors/lab; venue/year | Mechanism | Verified efficiency and accuracy | Status/limits |
|---|---|---|---|
| [Ares: Adaptive Reasoning Effort Selection for Efficient LLM Agents](https://arxiv.org/html/2603.07915v1) — Jingbo Yang et al.; UCSB/Accenture; arXiv 2026 | Select low/medium/high reasoning effort at each step with a learned router. | WebArena, fixed-high→Ares: **21,424→11,723 reasoning tokens/task**, SR **45.0→46.5%**. BrowseComp-Plus: **−41.8% tokens**, accuracy **42.7→41.3%**. Table 1. | E/L; token savings, wall-clock gain NR. |
| [Think Twice, Click Once: Enhancing GUI Grounding via Fast and Slow Systems](https://arxiv.org/html/2503.06470v1) — Fei Tang et al.; Zhejiang/MSRA; arXiv 2025 | Switch between direct grounding and a slower visual-reasoning path. | ScreenSpot: nonadaptive→adaptive **3.2→2.6 s/sample**, accuracy **74.8→77.4%**. Appendix A.2. | E; single-step grounding, not full workflow. |
| [GUI-G1: Understanding R1-Zero-Like Training for Visual Grounding in GUI Agents](https://arxiv.org/html/2505.15810v2) — Yuqi Zhou et al.; Renmin/Huawei Noah's Ark; NeurIPS 2025 | Train concise grounding without verbose reasoning. | InfiGUI-R1→GUI-G1, ScreenSpot accuracy **87.5→90.3%**; mobile/desktop/web output tokens **107/107/114→37/39/39**. Tables 4,7. | E; different training/model configurations; measured latency NR. |
| [Think Short, Defer Smart, Act, and Repeat: Calibrated Reasoning and Uncertainty-Aware Deferral for Edge LLM Agents](https://arxiv.org/html/2607.26865v2) — Amirmohammad Farzaneh, Osvaldo Simeone; Northeastern London/INSI; arXiv 2026 | Stop thinking when actions stabilize and defer uncertain cases under calibrated constraints. | MBPP: ReDAct-CD reports **1,206 thought tokens / 77.9% reward**; TSDS **422 / 71.4%** on its **22/50 certified splits**. Appendix Table 3/G.4. | Not lossless; these are unequally conditioned means, not a clean paired reduction. Full matched accuracy/cost delta NR. |
| [Efficient Agents: Building Effective Agents While Reducing Cost](https://arxiv.org/html/2508.02694v1) — Ningning Wang, Xavier Hu et al.; OPPO collaborators; arXiv 2025 | Tune step limits, replanning, search breadth and sampling to task needs. | GAIA, OWL→Efficient Agent: **$0.398→$0.285/task**, accuracy **53.33→51.52%**, cost/pass **$0.75→$0.55**. Table 7. | L; abstract's $0.228 overall-cost claim conflicts with Table 7; use table. |

## 8. Efficiency benchmarks and metrics

Benchmark papers do not necessarily introduce an acceleration method; the missing speedup or quality delta is N/A rather than zero.

| Paper; authors/lab; venue/year | Contribution and exact evidence | Interpretation |
|---|---|---|
| [OSWorld-Human: Benchmarking the Efficiency of Computer-Use Agents](https://arxiv.org/html/2506.16042v2) — Reyna Abhyankar, Qi Qi, Yiying Zhang; UCSD/GenseeAI; MLSys 2026, preprint 2025 | Human reference trajectories and success-weighted step efficiency. Agent S2/Gemini: original SR **41.4%**, single-action WES **15.6%**, grouped WES **9.6%**. Table 5. | Different metrics on the same agent, not an accuracy decline. No acceleration claim. |
| [AI Agents That Matter](https://arxiv.org/html/2407.01502v1) — Sayash Kapoor et al.; Princeton; TMLR 2025, preprint 2024 | Joint cost/accuracy optimization. HotPotQA retrieval, GPT-3.5 DSPy random-search→joint: cost **$0.376→$0.174 per 100 inferences**, retrieval accuracy **49.5→50.9%**. Appendix B/Table A3. | E for this comparison; one-time optimization costs excluded; empirical, not lossless. |
| [Cost-of-Pass: An Economic Framework for Evaluating Language Models](https://proceedings.iclr.cc/paper_files/paper/2026/hash/399d54cce01e782192b3d7ecbe607a96-Abstract-Conference.html) — Mehmet Hamza Erol, Batu El, Mirac Suzgun, Mert Yuksekgonul, James Zou; Stanford; ICLR 2026, preprint 2025 | Formalizes expected expenditure to obtain a correct solution and the frontier across models/human expertise. | Measurement framework, not an agent accelerator; paired agent speedup/accuracy N/A. |
| [Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation](https://arxiv.org/html/2510.11977v1) — Sayash Kapoor, Benedikt Stroebl et al.; Princeton-led collaboration; ICLR 2026, preprint 2025 | Standardized model–scaffold–benchmark evaluation and cost–accuracy frontiers: **21,730 rollouts**, **9 benchmarks**; higher effort fails to improve accuracy in **21/36 comparisons**. | Evaluation infrastructure, not agent-task acceleration. Published study's caching-cost limitations matter. |

A useful evaluation bundle reports success rate; all-attempt monetary/compute cost; complete-task median and tail latency; failure/retry costs; model calls, tokens and tool time; cache-hit rate and warm/cold results. For a fixed evaluation set, realized cost per success is total cost over all attempts divided by successful tasks. This accounting ratio is not automatically the expected cost of repeatedly retrying a particular task: retries can be correlated and verification can be imperfect. Keep the full cost–latency–success Pareto frontier.

## What remains open

1. **Safe abstraction and invalidation.** Determine when a skill still applies after UI, data or permission changes; validate preconditions and return to observation when needed.
2. **Full lifecycle economics.** Include demonstration, exploration, compilation, training, warm-up, verification and repair. Reuse pays only after those fixed costs are amortized.
3. **Joint control.** Optimize model choice, reasoning effort, screenshot detail, action-chunk length and speculation together; isolated savings may interact or cancel.
4. **Real GUI speculation.** Shared state, rollback, asynchronous updates and irreversible effects limit which branches can be safely pre-executed.
5. **End-to-end evidence.** Test on held-out long workflows with paired task outcomes, uncertainty estimates, deadlines and recovery. Grounding scores and successful-only latency are insufficient.
6. **Serving–agent co-design.** Expose dependencies and likely tool-wait times to runtimes while accounting for tool rate limits, multi-user load and tail latency.

These are synthesis judgments grounded in the cited mechanisms and evaluation limitations.

## Active research clusters

“Leading” here means recurring, relevant primary contributions, not a bibliometric ranking.

| Cluster | Evidence-backed focus |
|---|---|
| Stanford: Olukotun; Mirhoseini/Kozyrakis; systems collaborators | Plan caching, JIT compilation, SGLang and Continuum. |
| Berkeley: Gonzalez, Stoica, Dutta; SqueezeAILab | LLMCompiler, AsyncFC, Agentix, SGLang. |
| UCSD WukLab: Yiying Zhang | Preble and OSWorld-Human; cache-aware serving and efficiency evaluation. |
| CMU/MIT: Neubig, Fried, Mao collaborators | AWM; workflow reuse and agent interfaces. |
| Columbia: Kaffes/Peng | Guarded action speculation and cost–latency trade-offs. |
| Princeton SAgE: Kapoor, Stroebl, Narayanan | Cost-aware evaluation, reproducibility and HAL. |
| Microsoft Research/M365 with academic partners | UFO2, routing, PASTE, Parrot and speculative planning. |
| Salesforce AI Research | Demonstration compilation and local GUI replay through GPA. |
| Tsinghua AIR; Westlake | AutoDroid and AppAgentX; mobile scripts and learned macros. |
| ServiceNow/Mila/LIRIS; OPPO collaborators; CAS | Observation selection, visual-token efficiency and compact GUI grounding. |
| Google DeepMind; Huawei Noah's Ark; Accenture collaborators | Reusable tools/speculation; concise grounding; reasoning-effort routing, respectively. |

## Recent surveys

| Survey | Authors/date/status | Best use |
|---|---|---|
| [Toward Efficient Agents: A Survey of Memory, Tool Use, and Planning](https://arxiv.org/html/2601.14192v2) | Xiaofang Yang et al.; January 2026, revised July; arXiv | General taxonomy, agent memory/tool/planning trade-offs and efficiency evaluation. |
| [Efficient GUI Agents: A Systems Survey of Observation, Memory, Action, and Runtime Optimization](https://arxiv.org/html/2609.02309v1) | Bizhe Bai et al.; Fudan/Shanghai Innovation Institute; September 2026; arXiv | Closest match for GUI-specific observation, memory, action and runtime optimization. |
| [How to Make Tool-Using LLM Agents Efficient? A Survey](https://www.preprints.org/manuscript/202608.0365) | Yunuo Hu et al.; August 2026; unreviewed preprint | Tool context, invocation, reasoning and execution; check original papers before reusing numerical claims. |

## Verification notes

- Preprint and publication dates are distinguished where relevant; no acceptance is inferred from a manuscript template.
- Agentix's published NSDI version replaces the older Autellix numbers.
- OSWorld-Human and FocusAgent use revised pre-cutoff versions.
- Some surveys cite older versions; original tables take priority.
- Quality preservation in aggregate is not per-instance preservation or statistical equivalence.
- Sources lacking exact comparable measurements remain explicitly marked NR/N/A; no values were supplied by interpolation from unclear plots.
