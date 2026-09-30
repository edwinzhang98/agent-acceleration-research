# 2026-09-28 — Problem definition: the formulas of Part 1, checked against the original papers

Trigger: Edwin asked that the formulas defining the problem be taken from the cited literature, not decided by him: a source formula is cited as written (its own symbols) unless it is ambiguous or unsuitable; any adaptation carries a stated reason; anything no source writes as a formula is labelled "our distillation" with the sentences it is distilled from. This replaces the page-2 formulas of commits 7b45a64 and 2ab0360 (T_task, R/W, p_*, Pr[success]).

Method: a read-only workflow (13 agents): six groups read the papers at the source (arXiv HTML/PDF via pdftotext, USENIX PDF, vendor and Artificial Analysis pages; 156 formulas extracted), two independent definers proposed formula sets (cite-as-is; one clean model), one merge, three refuting reviewers (attribution re-read at the source, maths, justification; 49 problems raised), one finalisation. Every quoted sentence was re-checked against the local text layers (§1 below). The formula-scan files (research/2026-09-28-formulas-in-the-literature.md, notes/part1/2026-09-28-doc3-…) were leads only. The six owner choices the workflow left open were taken at their defaults (time per success; retry until verified; AsyncFC intervals widened; Cost-of-Pass price letters c_x(μ); ratio of means for a task mix; page 2 shows the one-call-per-step case of the context row).

Legend and page rows:

Legend. **verbatim** means the formula is quoted exactly as the source writes it. **adapted** means it is the source's formula with stated changes. **our distillation** means no source writes it as a formula. **calc.** marks algebra we did ourselves. All LaTeX below was parsed without error by the pinned matplotlib 3.10.9 mathtext (repo `.venv`, run on 28 Sep 2026). `\triangleq` parses. `\stackrel` does not, so it is not used.

**Page-2 rows** (each row carries its tag):
1. $T_{\mathrm{attempt}}=\sum_{i=0}^{N}(D_i+E_i)-T_{\mathrm{saving}}$, with $D_i=\sum_j\ell_{ij}$ and $\ell_{ij}\approx\mathrm{TTFT}_{ij}+n^{\mathrm{out}}_{ij}\mathrm{TPOT}_{ij}$. The sum is adapted from AOSpec, $T_{\mathrm{saving}}$ is adapted from AsyncFC, $\ell$ is adapted from AA.
2. $|H_{a,i+1}|=|H_{a,i}|+|\Phi(z_{a,i})|+|o_{a,i}|$, which gives $\sum_{i=1}^{N}|H_{a,i}|=N|H_{a,1}|+\frac{N(N-1)}{2}\bar g$. The first part is adapted from Yuan; the sum is calc., our distillation.
3. $c_m(p)=\sum_{i,j}\sum_{x\in X}n^x_{ij}c_x(\mu_{ij})+x_{\mathrm{env}}c_{\mathrm{env}}$. Adapted from Cost-of-Pass Eq. (13) under its App. D.1.
4. $v(m,p)=C_m(p)/R_m(p)$ is verbatim from Cost-of-Pass. The goal (F17) is our distillation.

---

## 0. The definition (canonical for the deck)

### 0.1 Formula set

### F1 The serialised sum of one attempt (no symbol of its own)
- **LaTeX:** `\sum_{i=0}^{N}\left(D_{i}+E_{i}\right)`
- **Plain meaning:** The summed durations over the attempt's N steps of model-call time $D_i$ and non-model time $E_i$, plus a step-0 bucket for calls that belong to no step. For a strictly serial agent this equals the wall-clock time. In general it equals AsyncFC's "serialized baseline" $\mathcal S(\mathcal M)+\mathcal S(\mathcal E)$ of the observed trace (F6).
- **Status:** adapted.
- **Source + location:** Chen, Guo, Luk & Fan (AOSpec), arXiv:2608.00881v1, §3 Motivation (inline, unnumbered).
- **Source form:** "At step i, the actor takes D_i time to generate action a_i, and the runtime takes T_i time to execute it and return observation o_i, yielding serial latency Σ_i(D_i+T_i)."
- **Reasons for change:**
  - (a) **T_i → E_i.** AOSpec's T_i (non-model time of one step) sits beside T_attempt, T_saving and T_seq, which are all totals, and reads as "time of step i". Speculative Actions also uses bare T for the horizon. E follows AsyncLM's E(f) and AsyncFC's ℰ (execution intervals).
  - (b) **Scope of D_i widened.** D_i now covers the J_i model calls of step i (F2), because model calls ≠ steps. It is also full call latency (queue, prefill, network, decode via F3/F4). AOSpec's evaluated D_i is only recorded output tokens × swept TPOT, so AOSpec's savings are not measured on the same D_i.
  - (c) **Scope of E_i widened.** E_i covers every non-model interval of step i: tool/action execution, observation capture, harness overhead, page loads, human or approval waits, rate-limit backoff, and idle gaps inside the step, including gaps between the calls of the decide phase. This makes F7 exact.
  - (d) **Definition of D_i and E_i.** Both are **summed interval lengths, not spans.** A step with three parallel 5 s tools has E_i = 15 s; the overlap goes into T_saving.
  - (e) **Step 0.** i = 0 collects per-attempt calls and intervals that belong to no step: OSWorld-Human S2's "retrieval (once)", pre-task planning, and amortised learning calls.
  - (f) **No symbol.** AOSpec gives the sum no symbol. We do not call it T_seq, because Speculative Actions and Guan use T_seq for a *separate sequential run* (F7b).
  - (g) **Why AOSpec, not other sources.** AOSpec is chosen over LLMCompiler Eq. (1), whose N counts atomic function calls of one plan and which omits the answering step. It is chosen over SpecBox Eq. (1) (F5) for content reasons: SpecBox has no sum over steps, no queue term and no human or approval waits.

### F2 Model time of a step
- **LaTeX:** `D_{i}=\sum_{j=1}^{J_{i}}\ell_{ij}`
- **Plain meaning:** The summed latencies of the step's model calls (planner, retries, judge, grounder, reflection). Overlap between parallel calls is credited in T_saving, not here.
- **Status:** our distillation.
- **Source + location:** extends AOSpec's D_i (one generation per step). The letter ℓ follows Speculate with Memory arXiv:2607.12236v1 §2.1 (ℓ_LLM).
- **Distilled from:**
  - OSWorld-Human arXiv:2506.16042v2 §3.4: "in each planning step, GTA1 makes 4 parallel calls to o3. If any calls fail to generate a valid plan, they will retry that call up to 3 times." and "Hence, for every judging call, there can be between 4 and 12 planning calls." Quote the 4–12 as the paper states it. The retry semantics are ambiguous, and the maximum could be 16; do not re-derive it.
  - §2.3: "These models are called upon for planning, judging, and reflection at each step, and they often involve long prompts, further increasing their computation time."
- **Reason:** J_i replaces the deck's c_k, because c is Cost-of-Pass's cost/price letter. Agentix Eq. (2) and LLMCompiler Eq. (2) take the critical path (max) for parallel calls. We keep D_i a plain sum and credit the overlap to T_saving, so F7 stays exact.

### F3 Latency of one model call
- **LaTeX:** `\ell_{ij}\approx\mathrm{TTFT}_{ij}+n^{\mathrm{out}}_{ij}\,\mathrm{TPOT}_{ij}`
- **Plain meaning:** The time to first token, plus the output tokens times the time per output token after the first.
- **Status:** adapted.
- **Source + location:** Artificial Analysis, https://artificialanalysis.ai/methodology, Definitions, "Total Response Time for 100 Output Tokens" (KaTeX source, read 28 Sep 2026; also on /methodology/performance-benchmarking v2.2.0). Third-party.
- **Source form:** Total Response Time = Time to First Token + 100 / Output Speed.
- **Reasons for change:**
  - (a) AA's fixed 100 becomes the call's actual output tokens n^out_ij, thinking included. TraceLab v2 §3.2 says O "already includes reasoning tokens", and Yuan Eq. (2) includes θ.
  - (b) 1/Output Speed is written as TPOT, AOSpec §5.1's term ("sweep TPOT"). The letter s would clash with the unit "seconds", with the state s_t (Speculative Actions, BoPO) and with AsyncFC's interval start s_i.
  - (c) **"≈", not "=".** AA's Output Speed excludes the first chunk's tokens, and AA uses separate Reasoning and Answer Output Speeds.
  - (d) **Condition: TTFT_ij is the time to the first generated token of any kind, reasoning included.** AA sets TTFT at the first reasoning token only "For reasoning models which return reasoning tokens". For hidden-reasoning models the first visible token arrives after thinking, so plugging a client-measured TTFT into F3 would count thinking twice. In that case use TraceLab §5.4's residual TTFT-hat = (t_reason − t_input) − O_reason·ℓ̂, or AA's End-to-End Response Time form (A0), and say which. AA computes its figure "synthetically based on TTFT and Output Speed".
  - (e) The deck's t_write(W) is dropped, because Anthropic uses "write" for cache storage.

### F4 Inside the first-token time (Appendix A0 or legend only)
- **LaTeX:** `\mathrm{TTFT}_{ij}\approx t^{\mathrm{queue}}_{ij}+t^{\mathrm{net}}_{ij}+t^{\mathrm{prefill}}\left(n^{\mathrm{unc}}_{ij}+n^{\mathrm{w5m}}_{ij}+n^{\mathrm{w1h}}_{ij};\,n^{\mathrm{hit}}_{ij}\right)+t^{\mathrm{first}}_{ij}`
- **Plain meaning:**
  - Engine queue wait.
  - Network time, which grows with request bytes (base64 screenshots are large).
  - Prefill of the input not read from cache, given the cached prefix. Image encoding counts inside prefill.
  - The first decode step.
- **Status:** our distillation.
- **Source + location:** no source writes TTFT as a sum. The closest lumped forms are AA's "Time to First Token = Time of First Token Arrival − Time Request Sent" and TraceLab's TTFT-hat.
- **Distilled from:**
  - Agentix (NSDI '26) §3 intro, p. 2446: "Formally, a single-threaded program's end-to-end latency comprises three components"; waiting time is "the total queuing time of a program's LLM calls on the engine".
  - SPORK arXiv:2607.03333v1 §2.1: "Each turn (re)prefills the context (the user prompt on the first turn, the appended tool result thereafter), decodes the reasoning and tool call, then stalls on the tool wait."
  - AA performance page: TTFT "includes network latency"; "Longer prompts can result in both longer time to first token".
  - TraceLab arXiv:2606.30560v2 §3.2: append tokens include "tokens introduced by prefix-cache misses".
  - Yuan arXiv:2605.26297v2 §V: "the relevant per-turn prefill pressure is better captured by incremental appends rather than the full input sequence".
  - OSWorld-Human v2 §3.2: latency "dominated by the prefill stage".
- **Reason:** this is the only path by which cache classes and context growth reach time. The shape of t^prefill is left unspecified because no verified source gives it. The second argument (attention over the cached prefix) is our reading. Cache-write tokens are prefilled, as in TraceLab's A_Claude = input_tokens + cache_creation_input_tokens.

### F5 SpecBox per-step decomposition (A0 corroboration)
- **LaTeX:** `T_{step}^{(N)}=T_{context}^{(N)}+T_{generation}^{(N)}+T_{env\_prep}^{(N)}+T_{data\_io}^{(N)}+T_{sandbox\_exec}^{(N)}`
- **Plain meaning:** Under a reactive (serial) runtime, the wall-clock time of one step is two model terms plus three sandbox terms.
- **Status:** verbatim.
- **Source + location:** SpecBox arXiv:2607.23933v2 (5 Aug 2026), §2.3 Eq. (1), PDF p. 3. (N) is SpecBox's step index.
- **Reason:** none. Mapping (our reading): T_context + T_generation corresponds to D_i. T_env_prep + T_data_io + T_sandbox_exec is the sandboxed-tool part of E_i. SpecBox has no queue, human-wait or harness-gap term.

### F6 Time saved by concurrency
- **LaTeX:** `T_{\mathrm{saving}}\triangleq\mathcal{S}(\mathcal{M})+\mathcal{S}(\mathcal{E})-\mathcal{D}(\mathcal{M}\cup\mathcal{E})`
- **Plain meaning:** On one observed trace, the summed length of all model-call intervals and all non-model intervals, minus the wall-clock time they cover once merged.
- **Status:** adapted. The formula text, including ≜, is verbatim; the interval sets are widened.
- **Source + location:** AsyncFC arXiv:2605.15077v1, App. B.2 "Saving Decomposition" (unnumbered; HTML alttext).
- **Source form:** T_saving ≜ S(M) + S(E) − D(M∪E) = Δ_{F∥F} + Δ_{D∥E}. Here S(I) = Σ_i(e_i − s_i), D(I) = |∪_i[s_i,e_i]|, and M and E are "the sequence of time intervals for model decoding and function execution".
- **Reason for widening:** ℳ becomes whole model-call intervals (queue, prefill, decode), and ℰ becomes all non-model intervals, including backoff and idle gaps (F1(c)). SPORK §2.1 names (re)prefill as a serial stage of every turn, and the deck's time must include prefill, queue and harness gaps.
- **Consequences, stated on the page and in A0:**
  1. **Not comparable with AsyncFC's reported savings.** The page tag reads "adapted from AsyncFC; intervals widened".
  2. **The Δ decomposition no longer holds as AsyncFC writes it.** A0 prints the three-term identity (calc., each term ≥ 0 by subadditivity): `T_{\mathrm{saving}}=[\mathcal{S}(\mathcal{M})-\mathcal{D}(\mathcal{M})]+[\mathcal{S}(\mathcal{E})-\mathcal{D}(\mathcal{E})]+[\mathcal{D}(\mathcal{M})+\mathcal{D}(\mathcal{E})-\mathcal{D}(\mathcal{M}\cup\mathcal{E})]`. The terms are model∥model, non-model∥non-model (no longer just AsyncFC's tool∥tool: it also includes tool∥human-wait and tool∥harness) and model∥non-model.
  3. **T_saving can include hidden waste.** Extra work that concurrency causes, such as drafter calls, rejected speculative tool runs, extra decoded turns (AsyncFC §6: "may decode more turns than a synchronous baseline") and contention, inflates 𝒮(ℳ)+𝒮(ℰ). So **T_saving is not time saved against a serial run** (F7b).

### F7 Observed time of one attempt
- **LaTeX:** `T_{\mathrm{attempt}}\triangleq t_{\mathrm{end}}-t_{\mathrm{start}}=\mathcal{D}(\mathcal{M}\cup\mathcal{E})=\sum_{i=0}^{N}(D_{i}+E_{i})-T_{\mathrm{saving}},\qquad T_{\mathrm{saving}}\geq 0`
- **Plain meaning:** The wall-clock time from the task being handed to the agent (t_start) to the final result being returned (t_end). It equals the serialised sum minus what ran concurrently. A strictly serial agent has T_saving = 0.
- **Status:** adapted.
- **Source + location:** AsyncFC App. B.2 definition sentence: "The total latency saving, T_saving, defined as the difference between the serialized baseline and the observed end-to-end asynchronous latency". It is combined here with F1.
- **Reasons for change:**
  - The name is T_attempt rather than T_task. It is one attempt, and in Cost-of-Pass's vocabulary a task (problem p) may take several attempts.
  - The **coverage condition**: 𝒟(ℳ∪ℰ) = t_end − t_start iff ℳ∪ℰ covers [t_start, t_end]. Here that holds by construction, because ℰ includes every non-model instant (backoff sleeps, retry waits, orchestration gaps, idle time).
  - A 429-rejected request and its backoff count in ℰ, since no tokens are generated and this is our convention.
  - T_saving ≥ 0 is calc. (subadditivity); AsyncFC does not write it.
  - T_attempt ≥ the length of the dependency critical path is calc. (LLMCompiler Eq. (2), Agentix Eq. (2)).
  - Row (1) is exact with measured ℓ_ij, and approximate once F3 is substituted.

### F7b Speedup against a serial run (solution pages; A0)
- **LaTeX:** `\mathrm{speedup}=\frac{T_{\mathrm{seq}}}{T_{\mathrm{attempt}}}`
- **Plain meaning:** T_seq is the time of a *separate* strictly sequential run of the same agent on the same task.
- **Status:** adapted.
- **Source + location:** Speculative Actions arXiv:2510.04371v2 §3.1.2 ("T_s and T_seq denote speculative and sequential execution times"); Guan arXiv:2509.01920v3 §5.1 (T^seq, ΔTime).
- **Reason:** the ratio replaces their time-saved form (T_seq − T_s)/T_seq. In general **T_seq − T_attempt ≠ T_saving** (F6 point 3).

### F8 Context growth, source form (A0)
- **LaTeX:** `H_{a,i+1}=H_{a,i}\Vert\Phi(\theta_{a,i},\,m_{a,i},\,u_{a,i})\Vert o_{a,i},\qquad C_{a,i}=|H_{a,i}|`
- **Plain meaning:** Before each LLM invocation, the context is the previous context, plus that invocation's templated output (thinking, message and tool-call tokens), plus the tool results it triggered.
- **Status:** verbatim.
- **Source + location:** Yuan, Nayak, Kundu & Talati arXiv:2605.26297v2 (21 Sep 2026), §II-C, Eqs. (1)–(3), with z_{a,i} = (θ_{a,i}, m_{a,i}, u_{a,i}) (2). The text is identical to v1 §2.3.
- **Reason:** none. Scope: in Yuan each step is one LLM invocation, and subagents are folded into a tool call. Yuan §II-B states that thinking tokens "are retained in the evolving context until the current user request is completed". (The "model- and chat-template-dependent" phrase in Yuan concerns the *ordering* of θ, m and u only.)

### F9 Context length per step (page-2 row 2, left)
- **LaTeX (page):** `|H_{a,i+1}|=|H_{a,i}|+|\Phi(z_{a,i})|+|o_{a,i}|`
- **LaTeX (A0, general):** `|H_{a,i+1}|=|H_{a,i}|+|\Phi(z_{a,i})|+|o_{a,i}|+h^{+}_{i}-h^{-}_{i}`
- **Plain meaning:** Each step adds its templated output and its tool-result tokens to the next prompt. In general, harness text and other calls' outputs are also added ($h^+_i$), and replaced observations or compaction remove tokens ($h^-_i$).
- **Status:** adapted.
- **Source + location:** take lengths of Yuan Eq. (3) (calc., not printed in the paper). Corroborated by TraceLab v2 §5.3 (unit example) and the Table 12 fresh-token definition.
- **Reasons:**
  - Concatenation adds lengths, so no "≈" is needed.
  - Φ(z_{a,i}) is **our substitution** of Eq. (2) into Eq. (3). Yuan always writes Φ(θ,m,u). We substitute because m clashes with Cost-of-Pass's pipeline m.
  - The observation is indexed by the issuing step, o_{a,i}, not o_{k+1}.
  - |Φ(z)| ≠ n^out, because of template tokens.
  - **The page form holds exactly only when J_i = 1 and the harness appends the full history (Yuan's scope, h^± = 0).** OSWorld-Human v2 §3.2 shows the multi-call case: the step-10 prompt includes "planning details and reflection feedback", which is other calls' output.
  - The identity breaks at compaction (TraceLab §4.2) and under a sliding window (OSWorld-Human §5.3).

### F10 Input tokens re-read over an attempt (page-2 row 2, right)
- **LaTeX:** `\sum_{i=1}^{N}|H_{a,i}|=N|H_{a,1}|+\sum_{i=1}^{N-1}(N-i)\,g_{i}=N|H_{a,1}|+\frac{N(N-1)}{2}\bar{g}`, where g_i = |Φ(z_{a,i})| + |o_{a,i}| and `\bar{g}\triangleq\frac{\sum_{i=1}^{N-1}(N-i)\,g_{i}}{N(N-1)/2}`
- **A0 additions:**
  - Expected form over random N: `\mathbb{E}\left[\sum_{i=1}^{N}|H_{a,i}|\right]\approx\mathbb{E}[N]\,|H_{a,1}|+\frac{\bar{g}}{2}\left(\mathbb{E}[N]^{2}+\mathrm{Var}[N]-\mathbb{E}[N]\right)`, which treats ḡ and |H_{a,1}| as independent of N.
  - Crossover: `N^{*}=\frac{2|H_{a,1}|}{\bar{g}}+1`.
- **Plain meaning:** Every step re-sends everything before it, so the actor's summed input grows as N². The N² term dominates only beyond N*.
  - Illustration (calc., assumed values): |H_{a,1}| = 6,000 and ḡ = 1,500 give N* = 9.
  - Failures that run to the step cap raise Var[N], so plugging in the mean step count underestimates the expected total.
  - With caching, most re-read tokens are cache hits: cheaper and faster, but not free.
- **Status:** our distillation (calc.).
- **Source form:** none; no source writes this sum.
- **Distilled from:**
  - OSWorld-Human v2 §3.2: "This is due to the prompting mechanism for most CUAs: at each step, the prompt sent to the LLM includes the history of all previous steps."
  - §3.2 also: "the prompt will include the screenshot for steps 1-9, along with planning details and reflection feedback". This supports the accumulation of o.
  - §3.4: "The quadratic increase contributes to the drastic cost difference between the planning and judging models compared to the grounding model." This is about accumulated dollars in Fig. 6, with no formula.
  - §5.3: "naively passing the entire trajectory substantially increases the cost and latency of a request."
  - WebRouter arXiv:2510.11221v1 §3.2: each query concatenates the goal, "the current web representation, and a growing action history from the agent's memory". This supports the Φ(z) part of g_i only; WebRouter keeps only the *current* observation.
  - Counterweight to print beside the row, Yuan v2 §V: "the relevant per-turn prefill pressure is better captured by incremental appends rather than the full input sequence".
- **Reason:**
  - With the weighted ḡ the equality is exact (calc.). With a plain mean it is off by a covariance term.
  - g_N is never needed, which is consistent with a terminal step having o_{a,N} = ∅.
  - The sum covers actor calls only, under the scope J_i = 1 (F9). Dimensions: tokens.

### F11 Tokens per screenshot, Claude only (optional sub-label)
- **LaTeX:** `\lceil width/28\rceil\times\lceil height/28\rceil`
- **Plain meaning:** Visual tokens for one image after any downscaling. For example, 1280×720 gives 46×26 = 1,196 (calc.).
- **Status:** verbatim.
- **Source + location:** Anthropic docs "Vision" → "Resolution and token cost" (read 28 Sep 2026; vendor documentation). The resize rule is on "Coordinates and bounding boxes".
- **Reason:** none. The label must read "Claude (Anthropic)". Other vendors' image-token rules differ and were not checked. Caps: 1568 tokens (standard tier) and 4784 (Claude 4.7 and later). The old (w×h)/750 rule is not on the page.

### F12 Input tokens of a call by billing class
- **LaTeX:** `n^{\mathrm{in}}_{ij}=n^{\mathrm{hit}}_{ij}+n^{\mathrm{w5m}}_{ij}+n^{\mathrm{w1h}}_{ij}+n^{\mathrm{unc}}_{ij}`
- **Plain meaning:** A call's input tokens fall into disjoint, separately billed classes: read from cache, written to the 5-minute cache, written to the 1-hour cache, and uncached.
- **Status:** adapted.
- **Source + location:** Anthropic "Prompt caching" → "Tracking cache performance" (written on the page): `total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens`. The same page gives the usage object `cache_creation: {ephemeral_5m_input_tokens, ephemeral_1h_input_tokens}` and states that "the current `cache_creation_input_tokens` field equals the sum of the values in the `cache_creation` object". Read 28 Sep 2026; vendor documentation. Cross-checked against TraceLab v2 §3.2 (P/A).
- **Reasons:**
  - Vendor-neutral class names. "hit" follows TokenPilot arXiv:2606.17016v2 Eqs. (2) and (11).
  - "unc" (uncached) follows SpeedRunner arXiv:2608.11338v1 App. A.3 (N_in^uncached) rather than "miss". On Anthropic, `input_tokens` are tokens "not read from or used to create a cache", and a *missed cacheable prefix is billed as a cache write*.
  - The write class is split by TTL, because one request can write both.
  - Vendors with no write class have n^w5m = n^w1h = 0 (TraceLab A_Codex).
  - The letter n follows Cost-of-Pass's n_in/n_out.
  - Link to context (ours, scope J_i = 1): n^in_{i1} ≈ |H_{a,i}|, counting the system prompt and tool definitions in H_{a,1}, up to vendor-injected tokens. Anthropic: computer_toolset_20260801 "adds about 4,500 input tokens to a request".

### F13 General per-attempt cost vector (licence for F14; A0)
- **LaTeX:** `C_{m}(p)=w^{\top}x_{m}(p)`
- **Status:** verbatim.
- **Source + location:** Cost-of-Pass arXiv:2504.13359v2, App. D.1 (inline; also in D.2; not in v1). One may include other components "by placing their unit cost in w and their per-attempt quantity in x". The listed extensions include tool fees, "orchestration overhead (e.g. queue time, cold-start penalties, inter-service latency)" and amortised costs including KV caching.
- **Reason:** none.

### F14 Money for one attempt (page-2 row 3)
- **LaTeX:** `c_{m}(p)=\sum_{i=0}^{N}\sum_{j=1}^{J_{i}}\sum_{x\in X}n^{x}_{ij}\,c_{x}(\mu_{ij})+x_{\mathrm{env}}\,c_{\mathrm{env}},\qquad X=\{\mathrm{hit},\mathrm{w5m},\mathrm{w1h},\mathrm{unc},\mathrm{out}\}`
- **Plain meaning:** The realized dollars of one attempt. Each call's tokens in each class are priced at the class price *of the model that served that call* (μ_ij). Billed environment usage is added at its price.
- **Status:** adapted (extended under D.1).
- **Source + location:** base is Cost-of-Pass App. B Eq. (13) (v1 Eq. (14)). A0 shows it as written beside the page row, with "extended under D.1". Verbatim three-class precedents: TokenPilot v2 App. A.2 Eq. (11), the closest written form; SpeedRunner App. A.3. The write classes come from Anthropic pricing and prompt caching. The runtime term comes from Anthropic Managed Agents pricing.
- **Source form:** c_m(p) = n_in(m,p)·c_in(m) + n_out(m,p)·c_out(m).
- **Reasons:**
  - (a) Cost-of-Pass's letters are kept (n for quantities, c for prices, c_m(p) for realized cost per attempt), because F13, F15 and the goal come from the same paper. TokenPilot's p_* would clash with Cost-of-Pass's problem p, its C′ with C_m(p), and its H_out with Yuan's H.
  - (b) **Prices sit inside the sum as c_x(μ_ij).** Harnesses mix models: GTA1 runs o3 and GTA1-7B in one step, and Speculate with Memory's speculator is "10–70× cheaper than the actor call". Summing tokens first is wrong for them. Cost-of-Pass likewise indexes prices by model, c_*(m). The argument also keeps price symbols distinct from the total c_m(p).
  - (c) Input is split into hit, w5m, w1h and uncached. Cached-read multipliers run 0.02x–0.25x by vendor (D156, E224, E225). Anthropic writes are 1.25x (5-minute) and 2x (1-hour).
  - (d) **Environment term: x_env c_env** (renamed from τ p_env). x_env is a component of Cost-of-Pass's x, and τ is BoPO's trajectory and FrugalGPT's threshold. x_env is billed usage under the provider's rule:
    - running-only: Managed Agents, $0.08 per session-hour, "running" status only;
    - minimum increment: code execution, $0.05 per container-hour with "a minimum of 5 minutes";
    - provisioned time: VMs, prewarmed sandboxes.
    So **x_env can be larger or smaller than T_attempt** (billing minimums, parallel containers, prewarm). c_env is the marginal price *after* any free quota (Anthropic: "1,550 free hours" per organization per month). The term is not linear below the quota.
  - (e) "W p_write" for output becomes n^out c_out.
  - (f) **Scope condition:** per-token prices are constant in context length. Verified for Anthropic: "Claude 4.6 and later models … include the full 1M token context window at standard pricing (A 900k-token request is billed at the same per-token rate as a 9k-token request.)" Not checked for other vendors.
  - (g) Not included (further w^⊤x terms): FrugalGPT's fixed per-query fee c̃_{i,0}, tool fees (web search $10 per 1,000), SpeedRunner's amortised inducer calls, and the batch (0.5x), fast-mode (2x price, calc.) and US-only (1.1x) multipliers.
  - Dimensions: tokens × $/token + units × $/unit = $.

### F15 Cost per success (page-2 row 4)
- **LaTeX:** `v(m,p)=\frac{C_{m}(p)}{R_{m}(p)}`
- **Plain meaning:** Expected dollars to get one correct result on task p with pipeline m. It is infinite if R = 0.
- **Status:** verbatim.
- **Source + location:** Cost-of-Pass (ICLR 2026) v2 §2.2 Eq. (2) (v1 Eq. (3)). R_m(p) is "Prob. of m producing a correct answer on p", and C_m(p) is the "Expected cost of one inference attempt by m on p".
- **Reason / conditions stated on the page:**
  - The basis is "the expected number of attempts to obtain the first correct solution is 1/R_m(p)", with "assuming independent trials".
  - Assumptions to print: unlimited retries, i.i.d. attempts, free and immediate success detection.
  - C_m(p) = E[c_m(p)] follows Cost-of-Pass's convention: capital letters for expectations, lowercase for a single run. The expectation is over **all** attempts, failures included. Averages taken over successful attempts only misstate it.
  - A0 (calc.): with a retry cap K, expected cost C(1−(1−R)^K)/R and success probability 1−(1−R)^K. Their ratio is still C/R (Wald).
  - A0 (calc.): with cache-warm retries (attempt 1 pays writes, later attempts read), expected cost to success is `C^{(1)}_{m}(p)+\left(\frac{1}{R_{m}(p)}-1\right)C^{(2+)}_{m}(p)`.
  - Sourced alternative success metric for repetitive workflows: pass^k (Cost-of-Pass C.8 and D.1).

### F16 Time per success
- **LaTeX:** `\frac{\mathbb{E}[T_{\mathrm{attempt}}]}{R_{m}(p)}`
- **Status:** adapted.
- **Source + location:** Cost-of-Pass v2 Eq. (2), with the per-attempt unit changed as App. D.1 allows: "alternative units per attempt (FLOPs, time, latency, energy) may matter more than dollar cost".
- **Reason / conditions:**
  - Same derivation in seconds (calc., Wald). E over all attempts.
  - **Serial retries only.** D.1 gives the counter-case: parallel votes incur "roughly the latency of a single vote".
  - Detection and verification time must be added to each attempt.
  - Correlated failures (the same page fails the same way) and side effects of failed attempts break the i.i.d. idealisation.

### F17 Goal
- **LaTeX:** `\mathrm{Pareto}_{m}\left(\frac{\mathbb{E}[T_{\mathrm{attempt}}]}{R_{m}(p)},\ v(m,p)\right)\quad\mathrm{s.t.}\quad R_{m}(p)\geq R_{0}`
- **Plain meaning:** Among agent designs (model plus harness) that succeed at least a fraction R_0 of the time, find the Pareto set on time per success and money per success, and compare it with the reference point of a person doing the task today.
- **Retry model (stated on the page):** retry until verified success, with verifier time and cost included in each attempt.
- **Status:** our distillation.
- **Source + location:**
  - One-objective core: Cost-of-Pass v2 §2.3 Eq. (3), V_p(ℳ) = min_{m∈ℳ} v(m,p).
  - Human fallback: §2.4 Eqs. (4)–(5), V_p(ℳ∪ℳ_0) = min(V_p(ℳ), v(expert,p)).
  - Dual and scalarised forms for A0: BoPO arXiv:2602.21227v1 §3.2 Eq. (2); FrugalGPT arXiv:2305.05176v1 §2 (prose); Speculative Actions §5.2 (sign as printed).
- **Distilled from:**
  - Kapoor et al. arXiv:2407.01502v1 abstract: "the new goal of jointly optimizing the two metrics".
  - Kapoor et al. §3: "This formalization is fully generalizable to other desiderata of agent design, such as latency."
  - Kapoor et al. §2.3 footnote 2: "We constrain the Pareto frontier to be convex".
  - Cost-of-Pass v2 App. C.8: "an extremely cheap yet essentially random agent can appear economically optimal", and the remedy "(i) explicitly excluding impractical baselines such as random guessers or unreliable systems from the set of strategies considered on the frontier". C.8's alternatives are (iii) pass^k and (iv) "explicit penalties for failed attempts".
  - BoPO §3.2: "maximize success subject to a strict upper bound on the total trajectory cost".
  - FrugalGPT §2: "Our primary goal in this paper is leveraging LLM APIs within a budget constraint."
- **Reasons:**
  - A scalar min of seconds and dollars is not defined, so the goal is written as an explicit Pareto set.
  - The floor is our formal version of C.8 remedy (i). It also guards against imperfect verification.
  - s_0 is renamed R_0, because the floor bounds R_m(p).
  - The min is over m without ℳ (ℳ is AsyncFC's interval set).
  - The human reference point comes from Cost-of-Pass's expert baseline. For Concur, the person doing it today is the bar. No human time or cost figure is sourced yet.
  - Aggregation (stated on the page):
    - One Concur template: per-problem v.
    - A task mix: the ratio of means `\frac{\sum_{p}C_{m}(p)}{\sum_{p}R_{m}(p)}`, which is finite, with the handling of R̂ = 0 reported. By contrast, Cost-of-Pass v2 Eq. (8) averages per-problem *frontier* values V_p over problems, and App. C.1 reports per-model means of R and C separately.

### F18 Overlap speedup ceiling (solution pages 3/7 only)
- **LaTeX:** `R=\frac{T_{\mathrm{LLM}}+T_{\mathrm{tool}}}{\max(T_{\mathrm{LLM}},T_{\mathrm{cp}})}`
- **Status:** verbatim.
- **Source + location:** AsyncFC §4 Eq. (1) (= App. B Eq. (2)).
- **Reason:** none. Keep it away from R_m(p) and R_0. The per-turn analogue is SPORK App. A, S_max = 1/(1 − f_tool).

---

### 0.2 Symbol table

| Symbol | Meaning | Unit | Origin |
|---|---|---|---|
| i, N | Step index (1..N; i = 0 for per-attempt calls and intervals outside any step); number of steps | —; steps | i: AOSpec §3, Yuan §II-C. N: ours. Not LLMCompiler's N or SpecBox's (N). |
| j, J_i | Model-call index; model calls in step i (j = 1 is the actor when J_i = 1) | —; calls | Ours (replaces c_k). Evidence: OSWorld-Human v2 §3.4 |
| a | Agent index | — | Yuan §II-C (never label actions a_i) |
| D_i | Summed latency of step i's model calls (includes TTFT) | s | AOSpec's letter, widened |
| E_i | Summed length of step i's non-model intervals (tools, observation, harness, page loads, human/approval waits, backoff, idle) | s | Ours; letter from AsyncLM E(f) and AsyncFC ℰ (replaces AOSpec T_i and the deck's t_obs, t_act, t_wait) |
| T_attempt | Observed wall-clock of one attempt, t_end − t_start | s | Ours (replaces T_task) |
| t_start, t_end | Task handed to the agent; final result returned | s | Ours |
| T_saving | Time hidden by concurrency on the same trace (can include hidden waste) | s | AsyncFC App. B.2, intervals widened |
| T_seq | Time of a separate strictly sequential run (A0 and solution pages only) | s | Speculative Actions §3.1.2; Guan §5.1 |
| ℳ, ℰ, 𝒮(·), 𝒟(·) | Model-call and non-model intervals; summed length; union length | s | AsyncFC App. B.2 (widened). A0 only |
| ℓ_ij | Latency of model call j in step i | s | Letter from Speculate with Memory ℓ_LLM |
| TTFT_ij | Request sent to first generated token of any kind (reasoning included) | s | AA; TraceLab §5.4 |
| TPOT_ij | Time per output token after the first (= 1/Output Speed) | s/token | AOSpec §5.1 term; AA Output Speed |
| t^queue, t^net, t^prefill(·;·), t^first | Engine queue; network (grows with request bytes); prefill of uncached input given cached prefix; first decode step | s | Ours (F4) |
| n^out_ij | Output tokens of a call, thinking included | tokens | Cost-of-Pass n_out; TraceLab O (replaces W) |
| n^in, n^hit, n^w5m, n^w1h, n^unc | Input tokens: total, cache read, 5-min write, 1-h write, uncached | tokens | Anthropic usage fields; hit from TokenPilot; unc from SpeedRunner (replaces R, R^hit, R^store, R^miss) |
| X | Billing classes {hit, w5m, w1h, unc, out} | — | Ours |
| μ_ij | Model serving call ij | — | Ours |
| c_x(μ) | Price per token of class x on model μ | $/token | Letter from Cost-of-Pass c_in(m); classes from TokenPilot and Anthropic (replaces p_*) |
| x_env, c_env | Billed environment usage (per the provider's rule); marginal price after any free quota | h (or billed units); $/h | x from Cost-of-Pass D.1 (replaces τ, p_env) |
| H_{a,i}, \|H_{a,i}\| | Actor context before invocation i; its length (Yuan's C_{a,i}) | sequence; tokens | Yuan Eqs. (1), (3) |
| z_{a,i} = (θ, m, u), Φ | Output of invocation i (thinking, message, tool-call tokens); chat template | tokens | Yuan Eq. (2); Φ(z) is our substitution |
| o_{a,i} | Tool results appended after step i | tokens | Yuan Eq. (3); AOSpec o_i |
| g_i, ḡ | Per-step increment; (N−i)-weighted mean | tokens/step | Ours (calc.) |
| h^+_i, h^-_i | Tokens added by other calls or harness; tokens removed (A0) | tokens | Ours |
| N* | Step count beyond which the N² term dominates | steps | Ours (calc.) |
| width, height | Image size after downscaling | px | Anthropic Vision |
| m, p | Pipeline (model + prompt + decoding + harness); task instance | — | Cost-of-Pass §2.2, App. B |
| c_m(p), C_m(p) | Realized $ of one attempt; expected $ per attempt | $ | Cost-of-Pass App. B, §2.2 |
| w, x_m(p) | Price vector; quantity vector | — | Cost-of-Pass D.1 |
| R_m(p) | Success probability per attempt | prob. | Cost-of-Pass §2.2 (replaces Pr[success]) |
| v(m,p) | Expected $ per success | $/success | Cost-of-Pass Eq. (2) (replaces Cost_success) |
| R_0 | Success floor | prob. | Ours (replaces s_0) |
| 𝔼[·], Var[·] | Expectation and variance over attempts | — | Standard |

---

### 0.3 Dependencies between variables (with evidence)

1. **Context drives both time and money.**
   - Actor input n^in_{i1} ≈ |H_{a,i}| grows by g_i each step (Yuan Eq. 3). Re-sent input grows as N² beyond N* (F10, calc.).
   - It enters money through c_hit and c_unc/c_w*, and time through t^prefill (F4).
   - Evidence, OSWorld-Human v2: §3.2 "the prompt sent to the LLM includes the history of all previous steps"; §5.3 "substantially increases the cost and latency of a request". The "3× longer" figure is in the abstract only.
2. **The cache-class split is set by harness and provider, not by the model.**
   - Append-only history keeps prefixes reusable. Yuan reports 84.6–99.5% empirical hit rate (E29). Agentix reports >90% within a program, decaying across programs (§3.2, Fig. 7).
   - Editing or compaction and eviction create misses. TraceLab v2 §7.3 reports 5.3× prefill amplification.
   - Whether prior output is re-sent or cached is provider-dependent (TraceLab §5.3).
   - On Anthropic a missed cacheable prefix is billed as a write (1.25x or 2x), not at the uncached rate.
3. **Money depends on elapsed time through the cache TTL (our reading).** Anthropic: "The lifetime is measured from the start of the request that writes or reads the cache entry." The next prefix misses when (start of next call) − (start of the last call touching that prefix) > TTL, i.e. roughly ℓ_last + E_i ≳ TTL for the actor. So slow tools, long thinking and human pauses cost money. TraceLab §7.5: at most 12.8% of cost could be saved if the cache survived human pauses (an upper-bound counterfactual).
4. **Time and money depend on output length, thinking included.** D_i grows with n^out·TPOT. Output is billed at c_out, the highest class.
5. **Model calls ≠ steps ≠ tool calls.**
   - J_i > 1 for planners, retries, judges and grounders (OSWorld-Human §3.4: "between 4 and 12 planning calls" per judging call). These add to D_i and money but not to steps.
   - SpecBox §5.1 reports 2.96 tool invocations per step. They add to E_i; parallel ones reduce time only through T_saving.
6. **Observation size depends on resolution and tier (Claude):** ⌈w/28⌉×⌈h/28⌉, capped at 1568 or 4784. Past screenshots are re-sent on every call that keeps them in history, so |o| enters F10 quadratically.
7. **Price depends on model and billing mode (Anthropic pricing, 28 Sep 2026).**
   - Cache read: 0.1x base input (0.05x on Opus 5.5; 0.025x on Fable 5.1 and Mythos 5.1). Writes: 1.25x (5-minute) and 2x (1-hour).
   - Batch 0.5x; US-only 1.1x; "These multipliers stack". Cross-vendor cached-read range 0.02x–0.25x (D156, E224, E225).
   - Fast mode: $8/$40 against $4/$20 on Opus 5.5 (2x price, calc.). The vendor claims "up to 2.5x higher output tokens per second" and says benefits are "not time to first token" (vendor marketing, not independently measured). It therefore affects TPOT, not TTFT.
   - Context length: flat per-token price for Claude 4.6+; other vendors not checked.
8. **Environment money follows billing rules, not wall-clock.** Running-only (Managed Agents), a 5-minute minimum and per-container billing (code execution), a free quota. x_env ≷ T_attempt.
9. **Success is coupled to steps and cost.**
   - Yuan v2 §IV: "failed tasks can be expensive even when they do not produce useful outcomes".
   - WES penalises failed-task steps via (1 − t̄_fail/S).
   - BoPO trades success against cost (Eqs. 1–2).
   - C.8: a cheap random agent can minimise v.
   - E[c | success] ≠ E[c].
10. **The achievable saving depends on dependency structure and the tool/decode ratio.**
    - AsyncFC Table 1 caption: "under the necessary condition that decode progress does not depend on all executing functions' results". Sweet spot T_tool ≫ T_cp and T_LLM ≈ T_cp.
    - AsyncLM Thm 6.2 (approximation): L_Sync/L_Async ≈ 1 + Ē/Ḡ.
    - SPORK: 1/(1 − f_tool); f_tool = 0.366 gives 1.58× per turn.
    - AOSpec §3.3: a speculative action "can hide at most min(D_i,T_i)" (AOSpec's T_i = our E_i for one step).
    - T_attempt ≥ the critical path (calc.).
11. **Buying time with speculation costs money, and the extra work lands in ℳ/ℰ.**
    - Evidence: Speculative Actions Thm 3/5/7; Speculate with Memory §4.3 k·C_S + (1 − acc)·C_act (Types 2–3); Guan ΔCost; SPORK T_oh.
    - Lossless methods hold R_m(p) fixed, so only T_attempt and c_m(p) move.
    - Speculative Actions models money as proportional to time, so it does not carry over to cache-priced classes.
12. **Queue time depends on server load and co-tenants.** Agentix measures waiting time separately from service time (anti-starvation rule W_total/T_total ≥ β). API-side queue time cannot be separated from TTFT (AA: TTFT "includes network latency").

---

### 0.4 Measurement boundary

Map every published number onto these terms before comparing.

**TIME**
- **AA:** Total and End-to-End Response Time are synthetic single-call ℓ (100 or 500 output tokens, 10k-input default, P50 over 72 h, measured from GCP us-central1). TTFT lumps queue, prefill and network. For hidden-reasoning models, Output Speed uses the last 80% of answer chunks and TTFT absorbs the thinking. The Coding Agent Index execution time is wall-clock per attempt.
- **AsyncLM:** first to last generated token. The cloud Async figures are emulated (5 ms/token).
- **AOSpec:** trace replay. D_i is output tokens × swept TPOT, with no queue, prefill or network.
- **Speculate with Memory:** T_100 from recorded actor latencies. Table 6 figures are estimates (acc × ℓ_hit × 100). A.9 is analytical. Only HotpotQA and ALFWorld were run live.
- **SPORK:** per-query wall-clock, P95 ratio. T_dec is post-prefill, yet App. D's T_base includes "Other (prefill, overhead)" 6.2%.
- **AsyncFC:** mean per-task latency with injected tool delays (5 s per function on BFCL; 2× on SWE-bench Lite). T_saving is measured on the async trace itself.
- **LLMCompiler:** "end-to-end latency", undefined. Eqs. (1)–(3) omit the answering step.
- **SpecBox:** the 4.53× headline is the sum over a session's *tool invocations* of sandbox-initialization delay, i.e. part of Σ_i E_i, not T_attempt.
- **Agentix:** program-level token latency in s/token, a rate. It optimises waiting and execution only.
- **TraceLab:** request response time = generation + tool execution, excluding human thinking time. The step span includes TTFT. The tool overhead R = max(0, T_e2e − T_int) is Codex only.
- **Yuan:** LLM vs tool share of runtime; per-request prefill and decode from vLLM OpenTelemetry.
- **OSWorld-Human:** stopwatch T_attempt on 39 tasks. WES uses steps as a proxy for time.
- **BoPO:** latency is an author estimate from 80 and 90 tok/s.
- **Human and approval waits:** Agentix counts them as "interceptions", TraceLab excludes them, and our E_i includes them.
- **Queue time:** almost never reported separately.

**MONEY**
- **Two classes (input, output), no cache classes:** Cost-of-Pass, WebRouter, Guan, FrugalGPT (plus a fixed per-query fee), OSWorld-Human Table 3. They **overstate cost when cache reads dominate and understate it when writes are billed.**
- **Three classes (hit, miss, out), no write class:** TokenPilot, SpeedRunner (which also amortises inducer calls), AA Cost per Task.
- **Write class included:** AA Coding Agent Index (text only); TraceLab (5-minute tier, an "API list-price equivalent", not a bill).
- **Environment term:** only Anthropic's pricing prices it; no paper includes it. No paper applies batch, fast-mode or region multipliers. Cost-of-Pass D.3 omits "wait times, invocation retries, tool-call charges". BoPO excludes the router's own cost.
- **OSWorld-Human:** $2.43 per task in the text against $7.87 per task from the table (calc.; D7/E45).

**CACHE HIT RATE (different denominators)**
- AA: cached / *cacheable* input tokens.
- TokenPilot: cached / "total ingestion".
- Agentix: "percentage of precomputed input tokens" per incoming call.
- Yuan: empirical vs "theoretical", with no formula.
- The deck's own definition: n^hit / n^in.

**PER ATTEMPT vs PER SUCCESS**
- Almost every published figure is per attempt. AA reports per attempt alongside pass@1.
- Cost-of-Pass averages per-problem frontier values (Eq. 8).
- Lossless speed papers report no task success, so their numbers apply at fixed R_m(p). SPORK reports accuracy only as "within 1 pp".

**UNITS**
- Convert steps (WES), turns (SPORK), and calls (Speculative Actions: one step = one API call, LLM or tool) to our i and j before comparing.

---

### 0.5 Loop-diagram symbol changes

1. **Index:** k → i, "N passes" → "N steps". The top pill becomes "J_i model calls in step i" (call index j). Add a small "step 0: once-per-attempt calls" note, or put it in the legend.
2. **DECIDE box:** title "model call j of J_i".
   - Pills: t^queue; prefill (uncached); n^out·TPOT.
   - A bracket over queue + prefill (+ network, first token) labelled TTFT, so ℓ_ij ≈ TTFT + n^out·TPOT.
   - The decide segment is labelled D_i = Σ_j ℓ_ij.
   - Optional sourced caption: SPORK's "(Re)prefill → Decode → Tool wait".
3. **Observe / Act / Wait:** t_obs, t_act and t_wait are removed. One bracket E_i spans act → wait → observe, with plain-word sub-labels: "ready the machine", "run the action", "return the result", "human or approval wait", "backoff / idle". The legend says E_i also holds gaps between the calls of the decide phase.
4. **Token band:**
   - o_{a,i} tokens go on the loop-back arrow. Optional sub-label "⌈w/28⌉×⌈h/28⌉ per screenshot (Claude)".
   - "|H_{a,i}| read: hit / write / uncached".
   - "n^out output (thinking included)".
   - "× c_x of the serving model".
   - "x_env billed environment usage × c_env".
5. **Next-prompt pill:** |H_{a,i+1}| = |H_{a,i}| + |Φ(z_{a,i})| + |o_{a,i}|, exact, with the note "one call per step, full history".
6. **End node:** R_m(p); v(m,p); R_0; c_m(p) (realized) and C_m(p) (expected); T_attempt.
7. **T_saving pill:** "serialised sum − merged wall-clock (adapted from AsyncFC; intervals widened; not T_seq − T_attempt)".
8. **Never on page 2:** R for tokens, p for prices, a_i for actions, C for context length, T_i, τ, or s for speed.
9. **Global renames** (TERM_IDS, page-2 rows, pages 3/7/9 legends, A0):
   - k→i; c_k→J_i.
   - R, R^hit, R^miss, R^store → |H_{a,i}|, n^hit, n^unc, n^w5m/n^w1h; W→n^out.
   - p_hit, p_miss, p_store, p_write → c_hit, c_unc, c_w5m/c_w1h, c_out; p_env→c_env; τ→x_env.
   - t_obs, t_act, t_wait → E_i. T_task → T_attempt.
   - Pr[success]→R_m(p); Cost_success→v(m,p); s_0→R_0; min(·,·)→Pareto set.
   - The commit message must say why commit 2ab0360's TokenPilot p_* names are reversed: p and C clash with Cost-of-Pass, H_out with Yuan, and per-model pricing needs c_x(μ).
10. **mathtext (matplotlib 3.10.9, repo .venv):** \triangleq, \Vert, \lceil/\rceil, \mathbb{E}, \mathcal{M,E,S,D}, \top, \parallel, \mathrm{env\_prep}, \mathrm{Pareto} and every formula string in §1 parse. \stackrel fails, so do not use it.

---

### 0.6 Changes after the independent review of the deck (28 Sep 2026)

Three reviewers checked the rebuilt Part 1 against this definition (50 findings, all addressed). Notation and wording changes to this definition: the billing-class index is κ ∈ K = {hit, w5m, w1h, unc, out} instead of x ∈ X, because x is Cost-of-Pass's quantity (x_env, x_m(p)); "write" on its own means decoding output tokens and a cache write is always called a cache write (n^w = n^w5m + n^w1h); T_saving is called small, not ≈ 0 — the only evidence is one production trace's intra-turn concurrency of 1.15 (a call count); the strips on deck pages 5, 11 and 13 were corrected to bracket the step sum and the expectation (Σ_i[Σ_j ℓ_ij + E_i] − T_saving; v = 𝔼[c_m(p)]/R_m(p)).

## 1. Verification table

The "Extract" rows were checked by earlier extraction agents against the named arXiv PDF (pdftotext) and the HTML LaTeX alttext, or against the rendered vendor or AA page. "Re-checked" means grepped this pass against the local text layers in the scratchpad (`wf-define/`, `attr/`, `src4/`), fetched again on 28 Sep 2026.

| Item | Where checked | Verdict |
|---|---|---|
| F1 AOSpec "yielding serial latency Σ_i(D_i+T_i)", "the runtime takes" | 2608.00881v1 text layer (re-checked) | Confirmed |
| F2 OSWorld "retry that call up to 3 times", "between 4 and 12 planning calls", §2.3 "called upon for planning, judging, and reflection at each step" | 2506.16042v2 raw text (re-checked) | Confirmed; 4–12 kept as the paper states it |
| F3 AA Total Response Time formula | AA /methodology KaTeX (extract, browser) | Confirmed by extract |
| F3 AA "which return reasoning tokens, this will be the first reasoning token", "calculated synthetically", "last 80% of answer chunks" | AA main and performance pages, server HTML (re-checked) | Confirmed; supports the double-count fix |
| F3 TPOT term | AOSpec "sweep TPOT" (re-checked) | Confirmed |
| F3 TraceLab "already includes reasoning tokens" | 2606.30560v2 raw (re-checked) | Confirmed |
| F4 Agentix "Formally, a single-threaded program…", "the total queuing time of a program…", "Since component (3) is unrelated to LLM serving" | NSDI '26 PDF text (re-checked) | Confirmed |
| F4 SPORK "Each turn (re)prefills the context" | 2607.03333v1 (re-checked) | Confirmed |
| F4 AA "includes network latency", "Longer prompts can result in both longer time to first token" | AA performance page HTML (re-checked) | Confirmed |
| F4 TraceLab "tokens introduced by prefix-cache misses"; Yuan "incremental appends" | text layers (re-checked) | Confirmed |
| F4 OSWorld "dominated by the prefill stage" | 2506.16042v2 raw (re-checked) | Confirmed |
| F5 SpecBox Eq. (1) | 2607.23933v2 PDF + HTML (extract) | Confirmed by extract |
| SpecBox "sum of sandbox initialization delays incurred at each tool invocation within a session"; "rather than placing all of" | 2607.23933v2 raw (re-checked) | Confirmed; the metric is per tool invocation |
| F6 AsyncFC T_saving display with ≜ | 2605.15077v1 HTML alttext (extract) | Confirmed by extract |
| F6/F7 AsyncFC "defined as the difference between the serialized baseline and the observed end-to-end asynchronous latency", "may decode more turns than a synchronous baseline", "partially offset by AsyncFC-specific overhead" | 2605.15077v1 clean text (re-checked) | Confirmed |
| F7b Speculative Actions T_seq; Guan T^seq | 2510.04371v2, 2509.01920v3 (extract) | Confirmed by extract |
| F8 Yuan Eqs. (1)–(3) | 2605.26297v2 PDF + HTML (extract) | Confirmed by extract |
| F8 Yuan "exact ordering is model- and chat-template-dependent" | yuan2 text l. 355 (re-checked) | Confirmed: refers to ordering only (challenge upheld) |
| F8 Yuan "These tokens are retained in the evolving context until the current user request is completed" | yuan2 text l. 197 (re-checked) | Confirmed |
| F9 Φ(z) | Yuan Eq. (3) always writes Φ(θ,m,u) (extract) | Φ(z) is our substitution (challenge upheld) |
| F9/F10 OSWorld "planning details and reflection feedback" | osw_v2 text (re-checked) | Confirmed |
| F10 OSWorld "the prompt sent to the LLM includes the history of all previous steps", "The quadratic increase contributes", "naively passing the entire trajectory substantially increases the cost and latency of a request" | 2506.16042v2 raw (re-checked) | Confirmed |
| F10 WebRouter "a growing action history from the agent's memory" | 2510.11221v1 raw (re-checked) | Confirmed; supports action history only |
| F10 algebra, weighted ḡ, E[N²] form, N* | calc. this pass | Correct |
| F11 Anthropic "Each patch is a 28×28-pixel block of the image" | vision.md (re-checked) | Confirmed |
| F12 total_input_tokens formula; cache_creation = ephemeral_5m + ephemeral_1h; "Mixing different TTLs" | anth_caching.md ll. 830–884 (re-checked) | Confirmed |
| F13 Cost-of-Pass "by placing their unit cost in w and their per-attempt quantity in x" | cop2 text (re-checked) | Confirmed |
| F14 Cost-of-Pass Eq. (13); TokenPilot Eq. (11); SpeedRunner A.3 "summed over all LLM calls in the episode" | extracts; SpeedRunner re-checked | Confirmed |
| F14 Anthropic "billed on two dimensions: tokens and session runtime"; "Execution time has a minimum of 5 minutes"; "1,550 free hours"; "adds about 4,500 input tokens"; "These multipliers stack with other pricing modifiers" | anth_pricing.md (re-checked) | Confirmed |
| F14 long-context flat pricing ("A 900k-token request is billed at the same per-token rate as a 9k-token request") | pricing.md l. 216 (re-checked) | Confirmed; closes the open issue for Anthropic |
| Fast mode "up to 2.5x higher output tokens per second", "not time to first token" | fast-mode.md (re-checked) | Confirmed; vendor marketing |
| F15 Cost-of-Pass Eq. (2), "Expected cost of one inference attempt", "assuming independent trials" | cop2 (re-checked) | Confirmed |
| F15/F17 C.8 remedy "(i) explicitly excluding impractical baselines such as random guessers or unreliable systems…", pass^k, failure penalties | cop2 ll. 2691–2697 (re-checked) | Confirmed |
| F16 D.1 "alternative units per attempt (FLOPs, time, latency, energy)", "roughly the latency of a single vote" | cop2 ll. 2749–2760 (re-checked) | Confirmed |
| F17 Kapoor "the new goal of jointly optimizing the two metrics", "fully generalizable … such as latency" | kap text (re-checked) | Confirmed |
| F17 Kapoor "We constrain the Pareto frontier to be convex" | kap text l. 170: §2.3 footnote 2 (re-checked) | Confirmed; location corrected from A.1 |
| F17 BoPO "maximize success subject to a strict upper bound on the total trajectory cost"; FrugalGPT "Our primary goal…" | raw text layers (re-checked) | Confirmed |
| F17 Cost-of-Pass Eqs. (3)–(5), (8) | extract (v2 PDF + HTML) | Confirmed by extract |
| F18 AsyncFC Eq. (1) | extract | Confirmed by extract |
| Yuan "failed tasks can be expensive"; Anthropic cache-lifetime sentence; TraceLab fresh-token definition | text layers (re-checked) | Confirmed |
| mathtext rendering of every §1 LaTeX string | repo .venv, matplotlib 3.10.9 | All parse; \stackrel fails and is unused |

---

Rejected or partly rejected challenges:

1. **"Under retry-until-verified the floor R_0 is unnecessary" (challenge 2, F17). Partly rejected.** The floor is kept. Cost-of-Pass C.8's own remedy (i) excludes "unreliable systems" from the frontier even in its oracle-graded setting, and the floor also guards against imperfect verification. Both reasons are stated. The retry model itself is now stated explicitly, as the challenge asked.
2. **"Use TokenPilot Eq. (11) as the base" and "rename c_m(p)" (challenge 3). Rejected.** With five classes and per-model prices, neither Eq. (13) nor Eq. (11) survives verbatim. Keeping Cost-of-Pass's notation holds the cost → success chain (F13–F17) in one source's symbols. TokenPilot is cited in A0 as the closest written form. The c_m(p) versus price-letter clash is removed by the argument c_x(μ_ij) instead of a rename.
3. **"Switch F3 to AA's End-to-End form for hidden reasoning" (challenge 3). Partly rejected.** F3 stays, with an explicit TTFT condition. The End-to-End form goes to A0 as the alternative, because its terms (Input Processing Time, Reasoning and Answer Output Speed) are undefined on the AA page.
4. **"Put the E[N²] form on page 2" (challenge 2). Moved to A0.** The page row stays per-attempt with the weighted ḡ, which is exact. The expectation and the crossover go in A0 and the legend.
5. **"Keep T_seq for the observed serialised sum" (the merged definition's own choice).** Not accepted. Speculative Actions and Guan define T_seq as a separate sequential run, so the serialised sum is left symbol-less (as AOSpec left it), and T_seq keeps its source meaning (F7b). This goes further than challenge 2 asked.
6. **"Keep the SpecBox Fig. 2a queue evidence with no attribution" (challenge 3 option).** Rejected. SpecBox is dropped from the queue dependency entirely.

All other challenges were accepted as written.

---

## 2. D-ledger additions

| ID | Claim | Conflict | Resolution |
|---|---|---|---|
| D157 | research/2026-09-28-formulas-in-the-literature.md: "`T_100=TTFT+100/OutputSpeed` is our formalisation; the page states the synthesis in words only" (Artificial Analysis row) | The Artificial Analysis methodology page displays the formula itself (KaTeX): "Total Response Time = Time to First Token + 100 / Output Speed", computed "synthetically based on TTFT and Output Speed" (read 28 Sep 2026) | **It is AA's own formula.** Cite it as AA's (third-party measurement definition); F3 is adapted from it |
| D158 | Dossier E29 / D73 and slides/references.md cite Yuan et al. arXiv:2605.26297v1 §2.3 | A v2 (21 Sep 2026) exists; its arXiv metadata title is unchanged ("Agentic AI Workload Characteristics", checked on the arXiv API on 28 Sep 2026), the section is renumbered §II-C, and Eqs. (1)–(3) are unchanged (the workflow's note of a retitling could not be confirmed and is dropped) | **Cite v2 §II-C Eqs. (1)–(3)**; update the reference entry and the E29/D73 source cells in v3.1 |
| D159 | Deck and dossier use R (tokens), p (prices) and c_k (calls per pass) | Cost-of-Pass, the source of the cost-per-success chain, uses R_m(p) for success probability, p for the task instance and c for prices; keeping both notations on one page is ambiguous | **Deck notation changed** to the source letters (§0.2): n^x for tokens by class, c_x(μ) for prices, J_i for calls per step, R_m(p) for success |
| D160 | Deck page 2 (2ab0360): T_saving as AsyncFC's quantity | AsyncFC defines ℳ as decode intervals and ℰ as function-execution intervals; the deck needs queue, prefill, harness gaps and waits inside the intervals, so the value is not comparable with AsyncFC's reported savings, and T_saving ≠ T_seq − T_attempt | **Labelled "adapted from AsyncFC; intervals widened"** on the page and in A0; speedups against a serial run use T_seq (F7b) |

## 3. E-ledger patches

None applied to the dossier. For v3.1: E29 and D73 source cells → Yuan et al. v2 (21 Sep 2026) §II-C (D158); the remaining candidate patches listed as open issues 7(c)–(j) below were raised by the workflow and are not yet checked against the dossier lines.

## 4. Still open

1. **Owner decisions:**
   - (a) Time objective per success, E[T_attempt]/R (default), or per attempt.
   - (b) Retry model: A (retry until verified; default) or B (no free retry: per-attempt objectives with the floor).
   - (c) Widening AsyncFC's ℳ/ℰ (default), or keeping decode-only ℳ with a gap term.
   - (d) Reversing the p_* names to c_x(μ).
   - (e) The aggregate for a task mix (default: ratio of means).
   - (f) Whether page 2 shows only the J_i = 1 case (default) with the multi-call case in A0.
2. **Unsourced shape:** t^prefill(·;·) has no verified functional form. SPORK App. D gives only a 6.2% share.
3. **No human baseline figures.** The human time and cost per Concur report is unsourced.
4. **Idealisations to label:** i.i.d. attempts, correlated failures on the same page, side effects of failed Concur submissions, and silent failures (no verifier). pass^k (Cost-of-Pass) is the sourced alternative.
5. **Unchecked for vendors other than Anthropic:** context-length price tiers, image-token rules, and fast-mode or tier speed effects.
6. **Symbol clashes to note in A0 legends:**
   - 𝒟 vs D_i; ℰ vs E_i (intended) and 𝔼; ℳ vs Cost-of-Pass's strategy set.
   - AsyncFC's s_i and e_i vs nothing on page 2.
   - N vs n.
   - R_m(p) and R_0 vs AsyncFC's R and TraceLab's two R's.
   - LLMCompiler's E_i (a task) vs our E_i.
   - μ_ij vs Yuan Table III's µ.
   - h^± vs Speculative Actions' h_t.
   - SpecBox (N) vs N.
7. **Candidate D-entries.** Per memory, fetch origin before allocating IDs; none were allocated here.
   - (a) AA displays Total Response Time = TTFT + 100/Output Speed and six more KaTeX formulas; it is a source formula, not ours.
   - (b) Yuan v2 (21 Sep 2026; §2.3 → §II-C; arXiv metadata title unchanged — the "…Characterization" title noted by the workflow is not confirmed, see D158). D73, E29 and slides/references.md need updating.
   - (c) OSWorld-Human's "2.7–4.3× more steps" is OSWorld success rate / WES; patch E3.
   - (d) WES differs between v1 §4.3 and v2 §5.1.
   - (e) SPORK App. A is in the v1 HTML.
   - (f) TokenPilot's latest version is v2 (28 Aug 2026).
   - (g) SpecBox v2 is dated 5 Aug 2026.
   - (h) Speculative Actions' ICLR 2026 label is not confirmed by the v2 source.
   - (i) The deck's R (tokens) and p (prices) clash with Cost-of-Pass.
   - (j) The Anthropic fast-mode speed claim (vendor marketing) and flat long-context pricing for Claude 4.6+.
8. **Unread versions:** FrugalGPT TMLR and Kapoor TMLR (OpenReview 403, not bypassed), the OSWorld-Human MLSys camera-ready, the Agentix prepub PDF, Guan v1/v2, and the ICLR page for Speculative Actions.
9. **Source-internal inconsistencies to note if cited:**
   - SPORK: T_dec is "post-prefill", yet App. D includes prefill in T_base.
   - TraceLab Table 7 sums to 100.8%.
   - Agentix PLAS subscript c_k.id = c_i.id.
   - Guan: β ∈ N, yet negative β values are described.
   - AsyncLM: σ is undefined.
   - OSWorld-Human v2 §5.2 glosses WES+ as an extra-steps count.
10. **Ceilings belong on pages 3 and 7, not page 2:** γ_max = N, 1 + Ē/Ḡ, AsyncFC R, 1/(1 − f_tool), Speculative Actions' 50% breadth ceiling.
11. **Nothing in the repo was changed.** STATUS.md, Appendix A0, slides/references.md and build_deck.py still carry the old notation.

Scratch files, outside the repo: /private/tmp/claude-501/-Users-edwin-projects-agent-acceleration-research/7deb32b8-8e56-4ffc-8813-5ea7da470b16/scratchpad/wf-define/ (chk.py, source text layers, fast.md, pricing.md, aa_perf.html).
