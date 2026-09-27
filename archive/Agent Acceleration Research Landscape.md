# **Surveying the Research Landscape of Agent Acceleration (2023–2026)**

The transition of Large Language Models (LLMs) from static, single-turn chatbots to dynamic, multi-step autonomous agents has fundamentally redefined the computational economics of artificial intelligence. By late 2026, agents are routinely deployed to interact with web browsers, operating system graphical user interfaces (GUIs), and command-line interfaces (CLIs) over long-horizon workflows. However, this expansion in capability has exposed severe latency and cost bottlenecks. The traditional "ReAct" (Reason-Act) loop—where a model observes an environment, parses a massive context window, reasons step-by-step, executes a single primitive action, and waits for environmental feedback—is computationally exorbitant when scaled to workflows requiring hundreds of steps.  
To bridge the gap between capability and deployability, the research community has pivoted aggressively toward "Agent Acceleration." This report provides an exhaustive, systematic survey of the methodologies developed between 2023 and 2026 to render LLM-based agents faster and cheaper without sacrificing task accuracy. The analysis categorizes the landscape into eight core technique families: macro-actions and hybrid spaces, inter-task caching, speculative execution, parallelism, observation pruning, serving-system optimizations, reasoning-budget controls, and the evolution of efficiency benchmarking.

## **1\. Fewer Model Calls: Skill Discovery, Macro-Actions, and Hybrid Action Spaces**

The most intuitive pathway to accelerating an agent is to reduce the absolute number of inference cycles required to achieve a terminal goal. In complex GUI and web environments, forcing an agent to issue individual primitive commands (e.g., coordinate-level mouse movements, single keystrokes) creates excessive interaction overhead. Recent innovations address this by compiling historically successful trajectories into programmatic "skills" or "macro-actions." Furthermore, by unifying visually heavy GUI operations with highly efficient CLI commands into a single "hybrid" action space, agents can bypass the latency of visual grounding entirely when a backend API or terminal command suffices.  
The underlying mechanism of this family is temporal abstraction. By learning to emit variable-length action chunks rather than single actions, the policy coarsens its own granularity. This drastically reduces the number of times the heavy foundational model must be invoked. The risk, however, is that executing long action sequences open-loop increases the probability of cascading failures if the environment state changes unexpectedly mid-execution.

### **Key Systems and Papers**

| Title | Authors / Lab | Venue / Year | URL | Mechanism (1 Sentence) | Speedup / Cost Reduction | Accuracy Change & Benchmark | Lossy / Lossless |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Qwen-UI-Agent** | Tongyi MAI | arXiv 2026 (Unverified Venue) | [Link](https://tongyi-mai.github.io/Qwen-UI-Agent/Qwen-UI-Agent-Technical-Report.pdf) | Unifies GUI and CLI execution, emitting batched actions per model turn trained via online reinforcement learning over 10,000 concurrent environments. | Substantial interaction overhead reduction via \~40% batched output. | 82.1% MobileWorld, 79.5% OSWorld-Verified, 73.6% WebArena. | Lossy |
| **Act More, Decide Less: Skill-Guided Adaptive Action Chunking (SPACE)** | Yang et al. (Rutgers) | EMNLP 2026 | [Link](https://arxiv.org/abs/2609.02042?utm_source=gemini) | Distills temporal structure from trajectory-induced programmatic skills into a primitive-chunk policy via hybrid on-/off-policy optimization. | Reduces average LLM decision rounds by up to 78.9%. | \+7.0% to \+31.3% success rate (ALFWorld, ScienceWorld). | Lossy |
| **CUA-Universe / CUA-Verse** | (Anonymous/UI Agents) | arXiv 2026 (Unverified Venue) | [Link](https://arxiv.org/abs/2609.05374?utm_source=gemini) | Synthesizes hybrid GUI+CLI task execution data to train agents in cross-modality orchestration over shared application states. | Uses 60% fewer tokens than base model. | \+16.8 success-rate points over GUI-only (OSWorld). | Lossy |
| **MacroPO: Reinforcement Learning that Grows Its Own Action Space** | (Various) | arXiv 2026 (Unverified Venue) | [Link](https://huggingface.co/datasets/humainlab/llm-research-index/blob/89f72a9449e17df29300ef601fab6c4c1e4ac0f8/generation/run-2026-09-16-opus-5-topics-v4.0/reinforcement-learning-for-language-models/idea_17000.md?utm_source=gemini) | Coarsens decision units from BPE tokens to macros via entropy-gated, advantage-weighted mining of recurring rollout segments. | 3–8× fewer decisions per trajectory; faster wall-clock. | Higher pass@1 with pass@64 coverage preserved. | Lossy |

### **Analysis and Open Problems**

**What remains open:** The transition to macro-actions introduces profound challenges in boundary detection and parse ambiguity1. When an agent commits to an extended action sequence, sparse terminal rewards make it difficult to determine precisely which sub-action caused a failure. Standard reinforcement learning objectives fail to learn meaningful chunk boundaries, often causing policies to either collapse back to single-action behavior or over-commit to excessively long, brittle sequences1. Designing robust mid-chunk interruption signals—allowing an agent to detect environmental drift without invoking the full model for continuous verification—remains unsolved. Furthermore, hybrid GUI+CLI environments are notoriously difficult to scale across applications, as they require custom application-specific wrappers3.  
**Leading Groups:** Industrial application of hybrid spaces is heavily championed by Alibaba's Tongyi MAI team4. In academic settings, the Rutgers University Metaxas Lab has produced defining literature on adaptive chunk execution and programmatic skill induction6.  
**Recent Surveys:** The contextualization of macro-actions relies on overarching reviews of agentic methodologies. Notable 2025–2026 surveys include *Large Language Model Agent: A Survey on Methodology, Applications and Challenges* (Luo et al., 2025\)8, which maps evolutionary pathways of agent architectures, and *LLM-based Agentic Reasoning Frameworks: A Survey from Methods to Scenarios* (2025)9, detailing the shift from single-step to multi-step planning.

## **2\. Caching and Reuse Across Tasks**

Standard Key-Value (KV) caching optimizes the token generation process at the infrastructure layer, but it does not prevent the model from wasting compute on redundant reasoning. In enterprise deployment, agentic workloads are highly repetitive; workflows such as booking flights, generating standard reports, or navigating to specific software menus share identical macro-structures even if the precise target variables differ. Agentic plan caching operates at the task or intent level, shifting the paradigm from query-level caching to workflow-level caching10.  
By extracting, storing, and adapting structured plan templates from past successful executions, systems can bypass the expensive "thinking" and "planning" phases of the ReAct loop. Lightweight embedding models match new user requests against this episodic memory bank, retrieving a cached execution graph and adapting its parameters to the new context.

### **Key Systems and Papers**

| Title | Authors / Lab | Venue / Year | URL | Mechanism (1 Sentence) | Speedup / Cost Reduction | Accuracy Change & Benchmark | Lossy / Lossless |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents (APC)** | Zhang et al. | arXiv 2025 (Unverified Venue) | [Link](https://arxiv.org/abs/2506.14852?utm_source=gemini) | Extracts structured plan templates from past executions, using keywords to match and lightweight models to adapt plans to new tasks. | 50.31% cost reduction, 27.28% latency reduction (average). | 0% degradation (lossless accuracy on 5 agent workloads). | Lossy (Execution Path) |
| **MemRefine: LLM-Guided Compression for Long-Term Agent Memory** | (Various) | arXiv 2026 (Unverified Venue) | [Link](https://github.com/yxf203/Awesome-Efficient-Agents?utm_source=gemini) | Compresses historical trajectories into minimal operational cheatsheets to guide future execution without full context loading. | High context window token savings. | Maintains high task success on memory benchmarks. | Lossy |
| **SRMT: Shared Memory for Multi-agent Lifelong Pathfinding** | (Various) | arXiv 2025 (Unverified Venue) | [Link](https://github.com/yxf203/Awesome-Efficient-Agents?utm_source=gemini) | Utilizes a distributed, shared procedural memory cache to bypass redundant pathfinding computations in multi-agent swarms. | Accelerates multi-agent synchronization. | Improves multi-agent pathing success. | Lossy |

### **Analysis and Open Problems**

**What remains open:** The Achilles' heel of workflow caching is cache invalidation in dynamic environments. Traditional semantic caching breaks down when output validity relies on temporal factors, asset updates, or live sensor parameters11. For instance, a cached web-navigation plan will fail catastrophically if the target website updates its DOM structure overnight. Currently, systems lack reliable, computationally cheap proactive invalidation mechanisms; they mostly rely on reactive failure, wherein the agent attempts the cached plan, encounters an error, and must fall back to base reasoning. Determining the optimal abstraction layer for the cache—whether to store exact API calls, semantic sub-goals, or raw code—presents a complex Pareto tradeoff between the cache hit rate and execution robustness.  
**Leading Groups:** Microsoft Research and Stanford University are pioneering test-time memory adaptations, while industrial serving platforms are integrating plan-caching primitives directly into their enterprise frameworks to reduce API costs.  
**Recent Surveys:** Memory integration is extensively tracked in *From storage to experience: a survey on the evolution of llm agent memory* (Ma et al., 2026\)12. Other critical reviews include *A-MEM: Agentic Memory for LLM Agents* (2025)9 and *PlanGenLLMs: A Modern Survey of LLM Planning Capabilities* (2025)9.

## **3\. Speculation: Speculative Actions and Planning**

Derived from speculative decoding at the token level, Speculative Agent Planning applies the concept of "draft and verify" to the multi-step sequential decision-making of autonomous agents13. In highly interactive digital environments, the latency introduced by the environment itself (e.g., waiting for an API response, a script execution, or a web page render) is often longer than the model's inference time. Speculative execution capitalizes on this idle time.  
While the environment is processing step ![][image1], a smaller, cheaper draft model predicts steps ![][image2], ![][image3], and so forth, along with their expected environmental observations. The heavier target model verifies these steps asynchronously. If the predicted trajectory matches the true environment state, the agent commits the entire sequence instantly, achieving lossless acceleration.

### **Key Systems and Papers**

| Title | Authors / Lab | Venue / Year | URL | Mechanism (1 Sentence) | Speedup / Cost Reduction | Accuracy Change & Benchmark | Lossy / Lossless |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Dynamic Speculative Agent Planning (DSP)** | Guan, Lan, et al. (UCSB) | ICLR 2026 | [Link](https://arxiv.org/abs/2509.01920?utm_source=gemini) | Uses asynchronous online RL to dynamically adjust the speculation depth (how far ahead to guess) based on current state confidence. | 30% total cost reduction, 60% redundant compute reduction. | Preserves baseline accuracy (OpenAGI, TravelPlanner). | Lossless |
| **Speculate with Memory: Lossless Acceleration for LLM Agents** | (Various) | arXiv 2026 (Unverified Venue) | [Link](https://arxiv.org/abs/2607.12236?utm_source=gemini) | Equips a stateless speculator with contrastive transition tables and episodic memory to improve action prediction accuracy over time. | Up to 2.5× increase in observation prediction speed. | 19–39% relative accuracy improvement on draft action predictions. | Lossless |

### **Analysis and Open Problems**

**What remains open:** The utility of speculative planning is bounded by the divergence between the draft model's internal world model and the actual environment dynamics. When a speculative trajectory misaligns with reality (a verification failure), the system must execute a rollback. This wastes the compute expended by the draft model and can lead to increased total costs if the speculation step size is poorly calibrated14. While DSP addresses this by framing speculation depth as an online Temporal Difference learning problem to dynamically predict suspension points15, optimizing the target acceptance rate across highly stochastic operating system and live-web environments remains computationally fragile.  
**Leading Groups:** The University of California, Santa Barbara (Wang Lab) and Microsoft Research have aggressively advanced the online RL formulations of dynamic speculation15.  
**Recent Surveys:** While specific surveys solely dedicated to speculative agent planning are currently rare due to the novelty of the field, the core principles are discussed in *Understanding the planning of LLM agents: A survey* (2024)9 and *LLM-based Agentic Reasoning Frameworks: A Survey from Methods to Scenarios* (2025)9.

## **4\. Parallelism and Batching**

Traditional LLM function calling enforces strict synchronous execution semantics: the model decodes an action, execution halts until the environment returns a result, the result is appended to the context, and decoding resumes17. This serialization creates artificial bottlenecks. Parallelism and batching techniques decouple the LLM's decoding process from the physical execution of the tool, importing asynchronous operating system paradigms—such as "Futures" and "Promises"—directly into the agentic loop.  
By exposing symbolic "futures" to the model, an agent can dispatch a function call and immediately continue reasoning about the next necessary action, assuming the future will resolve17. This allows independent tool calls to run concurrently, drastically amortizing the heavy prefill costs associated with long context histories.

### **Key Systems and Papers**

| Title | Authors / Lab | Venue / Year | URL | Mechanism (1 Sentence) | Speedup / Cost Reduction | Accuracy Change & Benchmark | Lossy / Lossless |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Concurrency without Model Changes: Future-based Asynchronous Function Calling for LLMs (AsyncFC)** | Feng, Mao, Dutta, Gonzalez (UC Berkeley) | arXiv 2026 (Unverified Venue) | [Link](https://arxiv.org/abs/2605.15077?utm_source=gemini) | Decouples decoding from execution by automatically transforming function schemas to support future-valued inputs and outputs. | Significantly reduces end-to-end task completion time. | Preserves task accuracy (Software Engineering Benchmarks). | Lossless |
| **Sample Efficient Action Chunking Reinforcement Learning (SEAR)** | Nagy et al. | arXiv 2026 (Unverified Venue) | [Link](https://arxiv.org/abs/2603.01891?utm_source=gemini) | Employs a causal transformer critic trained with multi-horizon targets to parallelize action prediction across entire chunk prefixes. | Accelerates value propagation in RL. | Improves sample efficiency in long-horizon offline RL. | Lossy |
| **Dreamed-state REactive Action Matching for Action Chunking (DREAM-Chunk)** | (Various) | arXiv 2026 (Unverified Venue) | [Link](https://arxiv.org/abs/2606.18589?utm_source=gemini) | Samples candidate action chunks and predicts their latent futures with a lightweight world model for asynchronous execution. | Handles inference latency through asynchronous background checks. | Preserves mode consistency in demonstrations. | Lossy |

### **Analysis and Open Problems**

**What remains open:** The primary limitation of future-based asynchronous decoding is accurate dependency resolution. If Tool B mathematically requires the exact text output of Tool A, parallel execution is impossible. While research demonstrates that modern LLMs possess a native capability to reason over unresolved symbolic futures17, their ability to zero-shot construct complex, multi-hop dependency graphs without hallucinating state resolutions is inconsistent. Teaching models to confidently invoke await\_future functions only when strictly necessary, rather than blocking prematurely or proceeding with hallucinated data, requires further architectural alignment.  
**Leading Groups:** UC Berkeley (Joseph E. Gonzalez's lab) leads the systems-level integration of these asynchronous primitives, heavily bridging the gap between OS scheduling and LLM serving18.  
**Recent Surveys:** Parallel function execution is reviewed as part of broader tool-use studies, including *LLM-Based Agents for Tool Learning: A Survey* (2025)9 and *Tool Learning with Large Language Models: A Survey* (2024)9.

## **5\. Cheaper Calls: Observation Pruning and Context Compression**

For visual and web-based agents, the primary driver of inference cost and latency is the massive scale of the observation state. Raw HTML Document Object Models (DOMs) and accessibility trees (AxTrees) can routinely reach 100,000 to 800,000 tokens per step19. Passing this immense, noisy context to a frontier model for every minor action saturates the context window, triggers prompt-injection vulnerabilities20, and drives up operational costs exponentially.  
The field has moved away from uniform truncation toward programmatic filtering, targeted retrieval, and visual region-focusing. By shifting the burden of observation processing from the expensive root LLM to specialized, lightweight local models or dynamically generated filtering scripts, agents drastically reduce their input token footprint before the main inference phase begins.

### **Key Systems and Papers**

| Title | Authors / Lab | Venue / Year | URL | Mechanism (1 Sentence) | Speedup / Cost Reduction | Accuracy Change & Benchmark | Lossy / Lossless |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Prune4Web: DOM Tree Pruning Programming for Web Agent** | Zhang et al. | arXiv 2025 (Unverified Venue) | [Link](https://arxiv.org/abs/2511.21398?utm_source=gemini) | Shifts DOM processing from LLM reading to a DOM Tree Pruning Programming (DTPP) paradigm using programmatic extraction. | Reduces 100k token DOMs to \<20 actionable candidates. | Maintains grounding accuracy. | Lossy (Context discarded) |
| **FocusAgent: Simple Yet Effective Ways of Trimming the Large Context of Web Agents** | Kerboua et al. (ServiceNow) | TMLR 2026 | [Link](https://arxiv.org/abs/2510.03204?utm_source=gemini) | Uses a lightweight LLM retriever to extract only task-relevant lines from AxTrees, guided by the agent's high-level goals. | Reduces observation size by \>50%. | Matches strong baselines; reduces prompt-injection success rates (WorkArena, WebArena). | Lossy |
| **Minimal Failure Set (MFS) / GEPA Optimization** | Agrawal et al. | arXiv 2026 (Unverified Venue) | [Link](https://arxiv.org/abs/2605.29397?utm_source=gemini) | Evaluates and optimizes HTML pruning programs via an evolutionary framework trained to retain only the Minimal Failure Set of elements. | 2.2× to 3.1× faster per-step latency. | Retains 84% to 89% original success rate (WorkArena L1, WebLinx). | Lossy |
| **SWE-Pruner: Self-Adaptive Context Pruning for Coding Agents** | Wang et al. | arXiv 2026 (Unverified Venue) | [Link](https://arxiv.org/abs/2601.16746?utm_source=gemini) | Performs task-conditioned tool-output pruning in software engineering to extract the minimal verbatim evidence block needed next. | Substantial token footprint reduction. | Prevents disruption of logical structure in code bases. | Lossy |
| **ShowUI / SimpAgent** | (Various) | arXiv 2025 (Unverified Venue) | [Link](https://arxiv.org/html/2609.02309v1?utm_source=gemini) | Applies region-focused visual perception at the token level, selecting UI-relevant visual tokens over full screenshots. | ShowUI: 1.4× training speedup; SimpAgent: 27% FLOP reduction. | ShowUI: 33% redundant visual tokens removed. | Lossy |

### **Analysis and Open Problems**

**What remains open:** The fundamental tradeoff in observation pruning is signal completeness versus cost. Extracting elements based strictly on current task goals often eliminates context necessary for *future* steps, resulting in "semantic error within a state"21. For example, if a filtering algorithm aggressively trims a web page to just a login form, the agent loses peripheral context, such as a "Forgot Password" link or a dynamic banner warning about system maintenance. If the initial action fails, the agent lacks the necessary structural signals to diagnose the semantic drift without requesting a full re-observation21. Balancing observation freshness with call frequency remains an acute optimization problem, particularly in open-ended real-web tasks where task relevance is highly ambiguous21.  
**Leading Groups:** ServiceNow Research has produced highly impactful work on AxTree retrieval pruning20, while independent initiatives (e.g., SentienceAPI) push programmatic structural extraction to local hardware22. In the visual domain, various labs are advancing sub-image partitioning (Ferret-UI) and region-aware grounding objectives (R-VLM) to reallocate visual resolution19.  
**Recent Surveys:**

> 1. *Beyond a Million Tokens: Benchmarking and Enhancing Long-Term Memory in LLMs* (2025)9.  
> 2. *Large Language Model Agent: A Survey on Methodology, Applications and Challenges* (Luo et al., 2025\)8.

## **6\. Serving-System Support for Agentic Workloads**

As agents transition from experimental scripts to production deployments, the underlying hardware serving engines (e.g., vLLM, SGLang) face unique architectural pressures. Traditional chat workloads have steady cadences paced by human typing speeds. Conversely, agentic workloads are defined by "tool waits." An agent generates an action, pauses while the environment processes it (which may take milliseconds or minutes), and then resumes.  
During these unpredictable tool waits, default serving policies—like Least Recently Used (LRU)—typically evict the agent's highly valuable Key-Value (KV) cache prefix to make room for other incoming queries23. When the agent resumes execution, it suffers from massive "prefill amplification." The system is forced to recompute tens of thousands of tokens consisting of system prompts, tool definitions, and the entire historical trajectory. A 2026 trace analysis (TraceLab) covering 350,000 steps of coding agents revealed an astonishing prefill amplification of 5.3× across all sessions, meaning roughly 81% of processed tokens were redundantly recomputed26. Optimizing agent serving requires agent-aware schedulers that leverage proactive caching, time-to-live (TTL) pinning, and workflow transition graphs.

### **Key Systems and Papers**

| Title | Authors / Lab | Venue / Year | URL | Mechanism (1 Sentence) | Speedup / Cost Reduction | Accuracy Change & Benchmark | Lossy / Lossless |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **CacheScout: Learning Agent Execution for KV-Cache Management in Agentic Serving** | Zhang, Kim, et al. | arXiv 2026 (Unverified Venue) | [Link](https://arxiv.org/abs/2608.14624?utm_source=gemini) | Learns agent execution transitions online via Markov chains to guide KV-cache eviction and issue proactive prefetching during idle gaps. | Reduces mean TTFT by 18–45%, per-turn latency by 29–38%; throughput up 19–57%. | Hit rate \+10–18% (Lossless execution). | Lossless |
| **Continuum: Efficient and Robust Multi-Turn LLM Agent Scheduling with KV Cache Time-to-Live** | Li, He, et al. (UC Berkeley) | arXiv 2025 (Unverified Venue) | [Link](https://arxiv.org/abs/2511.02230?utm_source=gemini) | Selectively pins the KV cache in GPU memory with a calculated TTL based on reload cost and predicted queueing delays during tool calls. | Improves average job completion times by over 8×; improves system throughput. | Lossless execution (SWE-Bench, BFCL, OpenHand). | Lossless |
| **Helium: Efficient LLM Serving for Agentic Workflows: A Data Systems Perspective** | Wadlom et al. | arXiv 2026 (Unverified Venue) | [Link](https://arxiv.org/abs/2603.16104?utm_source=gemini) | Integrates proactive caching and a cache-aware cost-based query optimizer across a workflow DAG to bypass redundant operators. | Up to 1.56× speedup over state-of-the-art agent serving systems. | Lossless execution. | Lossless |

### **Analysis and Open Problems**

**What remains open:** There is an inherent, unyielding conflict between prefix residency (holding cache in HBM for an idle agent) and global batch size (admitting new users into the system)27. Pinning the KV cache during unpredictable tool-call latencies risks GPU memory deadlocks and prolonged job completion times for downstream requests27. While Continuum utilizes TTLs29 and CacheScout utilizes learned transition matrices30, predicting exact external IO latency remains a highly stochastic problem that purely deterministic schedulers struggle to manage24. Near-memory schedulers must balance the globally expensive choice of eviction against the locally cheap choice of pinning28.  
**Leading Groups:** UC Berkeley (Ion Stoica and Joseph E. Gonzalez's labs) heavily dominates the foundational serving engine space via continuous architectural improvements to vLLM and SGLang24.  
**Recent Surveys:** While system-level surveys are technically distinct from model-level AI surveys, this specific area is grounded in reviews such as *Efficient memory management for large language model serving with pagedattention* (Kwon et al., 2023\)30, which acts as the foundational retrospective baseline outlining the limitations of reactive, recency-based KV-cache management.

## **7\. Reasoning-Budget Control for Agents**

Acceleration is fundamentally an exercise in controlling the "compute budget" expended per problem. While frontier models are highly capable, applying maximum thinking tokens, elaborate chain-of-thought, and deep self-reflection to simple, routine operations is a massive waste of energy and time. Reasoning-budget control involves dynamic difficulty estimation: granting the agent a long token horizon for complex puzzle-solving (like debugging multi-file code bases) while enforcing early termination, token masking, or fast routing for simple information retrieval.  
Techniques in this family rely on adaptive reinforcement learning or execution heuristics, where the agent is penalized not just for incorrect answers, but for excessive deliberation. The objective is to train the policy to calibrate its own output verbosity based on the perceived difficulty of the instruction.

### **Key Systems and Papers**

| Title | Authors / Lab | Venue / Year | URL | Mechanism (1 Sentence) | Speedup / Cost Reduction | Accuracy Change & Benchmark | Lossy / Lossless |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **DARE: Difficulty-Adaptive Reinforcement Learning with Co-Evolved Difficulty Estimation** | Zhou, Jin, et al. (Rutgers) | arXiv 2026 (Unverified Venue) | [Link](https://jincan333.github.io/?utm_source=gemini) | Co-evolves policy-aligned difficulty estimation with dynamic data selection to adaptively allocate optimization and inference compute. | Improves inference-token efficiency significantly. | Improves final reasoning accuracy. | Lossy |
| **MacroPO: Reinforcement Learning that Grows Its Own Action Space** | (Various) | arXiv 2026 (Unverified Venue) | [Link](https://huggingface.co/datasets/humainlab/llm-research-index/blob/89f72a9449e17df29300ef601fab6c4c1e4ac0f8/generation/run-2026-09-16-opus-5-topics-v4.0/reinforcement-learning-for-language-models/idea_17000.md?utm_source=gemini) | Coarsens the unit of decision from BPE tokens to macro segments via entropy-gated RL, bypassing step-by-step reasoning for known sub-tasks. | 3–8× fewer decisions per trajectory; faster rollouts. | Higher pass@1 with pass@64 coverage preserved. | Lossy |
| **OSWorld 2.0 (Adaptive Thinking Baselines)** | (OSWorld Contributors) | arXiv 2026 (Unverified Venue) | [Link](https://s46486.pcdn.co/wp-content/uploads/2022/01/OSWorld2.0.pdf) | Benchmarks reveal that limiting thinking tokens on simpler sub-tasks optimizes token budgets without hitting the task completion plateau. | Dynamically reallocates token budget to avoid saturation. | Avoids plateauing completion rates under strict token caps. | Lossy |

### **Analysis and Open Problems**

**What remains open:** The core unresolved challenge is the "chicken-and-egg" nature of difficulty estimation. Accurately determining the difficulty of an agentic workflow often requires actually attempting the workflow. If an agent prematurely classifies a task as "easy" and routes to a smaller, faster heuristic model or forces early termination, it may fall into a failure loop requiring expensive recovery actions. Developing reliable, zero-shot difficulty classifiers based purely on prompt semantics and initial state observations is a highly sought-after capability7. Furthermore, current RL formulations struggle with high advantage-gradient variance when verifiable rewards are smeared across thousands of near-deterministic positions2.  
**Leading Groups:** Rutgers University (Metaxas lab) has published extensively on difficulty-adaptive RL and co-evolved difficulty estimation7. Industrial labs like OpenAI and Anthropic natively implement varied reasoning budgets via their commercial APIs (e.g., dynamically controlling "thinking" tokens based on hidden routing protocols).  
**Recent Surveys:**

> 1. *Understanding the planning of LLM agents: A survey* (2024)9.  
> 2. *LLM-based Agentic Reasoning Frameworks: A Survey from Methods to Scenarios* (2025)9.

## **8\. Efficiency Benchmarks and Metrics**

Evaluating agent acceleration is impossible without rigorous, standardized benchmarks. Prior to 2025, agent benchmarks primarily measured static, binary success rates (e.g., "Did the agent successfully click the correct button?"). By 2026, the evaluation paradigm has shifted drastically toward assessing the Pareto frontier of Cost vs. Latency vs. Accuracy. The community recognized that an agent achieving 90% success but requiring 2 hours and \$50 of compute per task is fundamentally un-deployable compared to an agent achieving 85% success in 2 minutes for \$0.10.  
This shift necessitated benchmarks that explicitly measure token expenditure, prefill amplification, and cost-of-pass over extraordinarily long-horizon tasks.

### **Key Systems and Benchmarks**

| Title | Authors / Lab | Venue / Year | URL | Mechanism (1 Sentence) | Scope of Benchmark | Accuracy Change / Findings | Lossy / Lossless |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **OSWorld 2.0** | (OSWorld Contributors) | arXiv 2026 (Unverified Venue) | [Link](https://s46486.pcdn.co/wp-content/uploads/2022/01/OSWorld2.0.pdf) | Introduces 108 long-horizon, real-world computer-use tasks requiring complex interaction and cross-source reasoning. | Median task takes humans 1.6 hours; agents require \~318 tool calls. | Frontier models complete only 20.6% strict binary, 54.8% partial; highlights agent failure to maintain hidden state. | N/A |
| **TraceLab Characterization** | (Various) | 2026 (Unverified Venue) | [Link](https://www.sinanezhadian.com/research/the-cache-expires-while-the-human-thinks?utm_source=gemini) | Profiles 4,300 sessions and 350k steps of real coding-agent use to measure empirical token costs and cache behavior. | Defines "prefill amplification" metric. | Median step carries 126k tokens, appends 857, emits 252; prefill amplification measured at 5.3× overall. | N/A |
| **Survey on Evaluation of LLM-based Agents** | Stroebl et al. | arXiv 2503.16416 (2025) | [Link](https://arxiv.org/abs/2503.16416?utm_source=gemini) | Comprehensive survey analyzing agent evaluation across core capabilities, specific benchmarks, and core dimensions like cost-efficiency. | Identifies critical gaps in assessing cost-efficiency and robustness. | Calls for new paradigms assessing sequential decision-making over static textual outputs. | N/A |
| **HAL (Holistic Agent Leaderboard)** | Stroebl et al. | 2025 (Unverified Venue) | [Link](https://arxiv.org/pdf/2503.16416?utm_source=gemini) | Provides a unified platform for benchmarks across domains, emphasizing cost-of-pass metrics alongside success rates. | Covers coding and web domains. | Standardizes efficiency reporting. | N/A |

### **Analysis and Open Problems**

**What remains open:** A persistent gap exists in evaluating how agents recover from errors efficiently. While benchmarks like OSWorld 2.0 effectively measure whether an agent can maintain state over 300+ steps31, they struggle to isolate the *compute efficiency* of the recovery process itself. Furthermore, current metrics often fail to separate the cost of the underlying model from the efficiency of the agent harness. Benchmarks must co-evolve with agent capabilities, requiring continuous updates to prevent models from overfitting to static, simulated environments33.  
**Leading Groups:** The OSWorld 2.0 contributors remain highly influential in defining long-horizon computer-use evaluation32. Industrial benchmark platforms like Scale's MCP Atlas and the Tool-Decathlon initiative are pushing evaluations to source domains and tools from real, live server environments33.  
**Recent Surveys:**

> 1. *Survey on Evaluation of LLM-based Agents* (2025)34 — provides the first comprehensive breakdown of the shifting evaluation landscape.  
> 2. *Beyond a Million Tokens: Benchmarking and Enhancing Long-Term Memory in LLMs* (2025)9.

#### **Works cited**

> 1. Skill-Guided Adaptive Action Chunking for Long-Horizon LLM Agents, [https://arxiv.org/pdf/2609.02042](https://arxiv.org/pdf/2609.02042)  
> 2. humainlab \- Hugging Face, [https://huggingface.co/datasets/humainlab/llm-research-index/blob/89f72a9449e17df29300ef601fab6c4c1e4ac0f8/generation/run-2026-09-16-opus-5-topics-v4.0/reinforcement-learning-for-language-models/idea\_17000.md](https://huggingface.co/datasets/humainlab/llm-research-index/blob/89f72a9449e17df29300ef601fab6c4c1e4ac0f8/generation/run-2026-09-16-opus-5-topics-v4.0/reinforcement-learning-for-language-models/idea_17000.md)  
> 3. A Scalable and Dynamic Environment for Hybrid GUI+CLI Agents, [https://arxiv.org/html/2609.05374v1](https://arxiv.org/html/2609.05374v1)  
> 4. arXiv:submit/7884825 \[cs.AI\] 29 Jul 2026 \- GitHub Pages, [https://tongyi-mai.github.io/Qwen-UI-Agent/Qwen-UI-Agent-Technical-Report.pdf](https://tongyi-mai.github.io/Qwen-UI-Agent/Qwen-UI-Agent-Technical-Report.pdf)  
> 5. Qwen-UI-Agent Report Claims Lead on Real-Device GUI Benchmarks, [https://aiweekly.co/alerts/qwen-ui-agent-report-claims-lead-on-real-device-gui-benchmarks](https://aiweekly.co/alerts/qwen-ui-agent-report-claims-lead-on-real-device-gui-benchmarks)  
> 6. Skill-Guided Adaptive Action Chunking for Long-Horizon LLM Agents, [https://arxiv.org/abs/2609.02042](https://arxiv.org/abs/2609.02042)  
> 7. Can Jin, [https://jincan333.github.io/](https://jincan333.github.io/)  
> 8. \[2503.21460\] Large Language Model Agent: A Survey on ... \- arXiv, [https://arxiv.org/abs/2503.21460](https://arxiv.org/abs/2503.21460)  
> 9. Awesome Efficient Agents: A Survey of Memory, Tool Use, and, [https://github.com/yxf203/Awesome-Efficient-Agents](https://github.com/yxf203/Awesome-Efficient-Agents)  
> 10. Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient, [https://www.alphaxiv.org/abs/2506.14852](https://www.alphaxiv.org/abs/2506.14852)  
> 11. Evaluating Temporal Semantic Caching and Workflow Optimization, [https://arxiv.org/html/2605.20630v1](https://arxiv.org/html/2605.20630v1)  
> 12. Learning to Curate Task-Adaptive Memory for LLM Agents \- arXiv, [https://arxiv.org/html/2609.27334v1](https://arxiv.org/html/2609.27334v1)  
> 13. Dynamic Speculative Agent Planning \- arXiv, [https://arxiv.org/html/2509.01920v1](https://arxiv.org/html/2509.01920v1)  
> 14. Dynamic Speculative Agent Planning \- arXiv, [https://arxiv.org/pdf/2509.01920](https://arxiv.org/pdf/2509.01920)  
> 15. Dynamic Speculative Agent Planning \- OpenReview, [https://openreview.net/forum?id=YZ5k2dVj6O](https://openreview.net/forum?id=YZ5k2dVj6O)  
> 16. Dynamic Speculative Agent Planning \- Microsoft Research, [https://www.microsoft.com/en-us/research/publication/dynamic-speculative-agent-planning/](https://www.microsoft.com/en-us/research/publication/dynamic-speculative-agent-planning/)  
> 17. Future-based Asynchronous Function Calling for LLMs \- arXiv, [https://arxiv.org/html/2605.15077v1](https://arxiv.org/html/2605.15077v1)  
> 18. Future-based Asynchronous Function Calling for LLMs \- arXiv, [https://arxiv.org/abs/2605.15077](https://arxiv.org/abs/2605.15077)  
> 19. Efficient GUI Agents: A Systems Survey of Observation,Memory, [https://arxiv.org/html/2609.02309v1](https://arxiv.org/html/2609.02309v1)  
> 20. FocusAgent: Simple Yet Effective Ways of Trimming the Large, [https://arxiv.org/abs/2510.03204](https://arxiv.org/abs/2510.03204)  
> 21. Signal-Driven Observation for Long-Horizon Web Agents \- arXiv, [https://arxiv.org/html/2606.06708v1](https://arxiv.org/html/2606.06708v1)  
> 22. I built a DOM-pruning engine to run reliable browser agents ... \- Reddit, [https://www.reddit.com/r/LocalLLaMA/comments/1qcxllu/i\_built\_a\_dompruning\_engine\_to\_run\_reliable/](https://www.reddit.com/r/LocalLLaMA/comments/1qcxllu/i_built_a_dompruning_engine_to_run_reliable/)  
> 23. Learning Agent Execution for KV-Cache Management in ... \- arXiv, [https://arxiv.org/html/2608.14624](https://arxiv.org/html/2608.14624)  
> 24. Efficient and Robust Multi-Turn LLM Agent Scheduling with KV, [https://arxiv.org/html/2511.02230v5](https://arxiv.org/html/2511.02230v5)  
> 25. (PDF) Learning Agent Execution for KV-Cache Management in, [https://www.researchgate.net/publication/412349315\_Learning\_Agent\_Execution\_for\_KV-Cache\_Management\_in\_Agentic\_Serving](https://www.researchgate.net/publication/412349315_Learning_Agent_Execution_for_KV-Cache_Management_in_Agentic_Serving)  
> 26. The cache expires while the human thinks \- Sina Nezhadian, [https://www.sinanezhadian.com/research/the-cache-expires-while-the-human-thinks](https://www.sinanezhadian.com/research/the-cache-expires-while-the-human-thinks)  
> 27. Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving, [https://arxiv.org/html/2608.25523](https://arxiv.org/html/2608.25523)  
> 28. UNISON: A Co-Designed Near-Memory Scheduler of Session KV, [https://arxiv.org/html/2609.09643v1](https://arxiv.org/html/2609.09643v1)  
> 29. Continuum: Efficient and Robust Multi-Turn LLM Agent Scheduling, [https://arxiv.org/html/2511.02230](https://arxiv.org/html/2511.02230)  
> 30. Learning Agent Execution for KV-Cache Management in Agentic, [https://www.alphaxiv.org/abs/2608.14624](https://www.alphaxiv.org/abs/2608.14624)  
> 31. OSWorld 2.0: Benchmarking Computer Use Agents on Long ... \- arXiv, [https://arxiv.org/html/2606.29537v1](https://arxiv.org/html/2606.29537v1)  
> 32. OSWORLD 2.0: Benchmarking Computer Use Agents on Long, [https://s46486.pcdn.co/wp-content/uploads/2022/01/OSWorld2.0.pdf](https://s46486.pcdn.co/wp-content/uploads/2022/01/OSWorld2.0.pdf)  
> 33. Survey on Evaluation of LLM-based Agents \- arXiv, [https://arxiv.org/pdf/2503.16416](https://arxiv.org/pdf/2503.16416)  
> 34. \[2503.16416\] Survey on Evaluation of LLM-based Agents \- arXiv, [https://arxiv.org/abs/2503.16416](https://arxiv.org/abs/2503.16416)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAaCAYAAABVX2cEAAAA3klEQVR4XmNgGAWUgnlA/BmI/0PxAhRZCPjLgJAHYWdUaUyArBgb2AfEKuiC2AAjEG8H4vUMEMOCUKXBAJclGCAfiE2gbFyu+4MugAu8RWJ/YIAYxockpgbEnUh8vADZJaBwAfFvIoktA2IeJD5OAAqvzWhi6F7F5m2sADm8kMVABnRD+b+Q5PCCd+gCUABznTYQt6DJ4QS4vLCbASJ3D4g50eSwAhYg3osuCAVMDJhhhxMwA/EbID6JLoEEvgHxd3RBdLAKiD8yQNIXKF2B8h42oA/E2eiCo2AUDGkAAMruNN36aWNMAAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADYAAAAaCAYAAAD8K6+QAAABUUlEQVR4Xu2WsUoDQRCGR2MjiKTJG4iNhY1vYG/ha6TwJdKI7yBWFjYWFhYSu0ACsQ6CWCRgpaIICqLojLuHc8PumdnTNcV88MHtP7nJDslyB2AYRk720Sf0w3tQqjre4btObpbLWWiC+241fOMhztEVGf4xLXQMP+8tyhx6ih6Du3m7XP5C3ZTRk0ECSYPtoBv+OtbgTQYK+jJIILavSu7Y9QO4BsssW0V32VrLUAYJJA3Gb6BzROtLlh2iS2yt5UIGCagHo/N1IjLZRNUwwL8Mxs8Xz6jJnl+/sloVi+B6SUeBrHBa1IPdy8BTNFpDO6IWg541WwGvAlnhtKgHi334DFztGtwvUYfsf8UFtCtDzzwom1WQdbAGeosOZIHxjL7IMIFsgx2hj+CeX/TconfBEOtoW4YJ1BmM9neDTrx0TdlMUGewmYbOq2EYhmH8Bp82GGKWNqyCfgAAAABJRU5ErkJggg==>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADYAAAAaCAYAAAD8K6+QAAABn0lEQVR4Xu2WvyuFURjHHz8iJSlZTbIYlAw2g5lB+SsMBrMyWOTHaJRSisVgMIhNUcwiGZW6RET5Ec/jed/u836dc70/7tUdzqc+9Z7v03vvc+45p3OJAoHAf7LGPrFfkeuJqvJJ5bo4mizXnBPS771hR6D2J7ZxF4dsL4Y1poV9N+Ml0v6OTFaRBnaP3SF9cSJZ/sE34TSkbgR4ZlcguyXtpQtyJ9PsUPTsW7UPDDJwjEFK4l66TTYVZVsm83Jnnh9IX+wwWR+7YMZZOcUgJYPsImRzpP0tQ+7ErpCcIxlfmGyTbTfjrJxhUIB70v5asYDI+dqFDLeja2tmoVoT6yHtZRULLuz5spl8QLwN3kytEm2kn4WeO7LYLEhPcj2lQpbWRbxq/ew81Hx0suMOrxxZbFrkrp3BsBK+bbZPWrsmXYkiFN2Kl+wYZBswTtDMHmAY0Ui/z1peikxMzv8wZJORTprYEunfFR8v7CuGOcg7sVkq/7iocxdts4+k95fcW/Jf0MUA6YVYlLwTw8lY64K8E6t75LwGAoFAIFANvgHRsmxhcZPFRgAAAABJRU5ErkJggg==>