# Evidence on the Speed and Cost Bottlenecks of Computer-Use and Web Agents

The evidence supports **a serious speed–cost–reliability bottleneck for long, interactive computer-use workflows**. It supports a narrower claim than “all agents are too slow and expensive for real work”: asynchronous deployments can already be useful, and newer systems substantially improve efficiency.

**Evidence cutoff: September 25, 2026.** Below, *primary* means original measurements, research, surveys, or vendor statements; vendor claims are identified separately from independent research. Historical results describe the named system at that date.

For the time comparisons, three distinctions matter: **model calls ≠ tool calls ≠ environment steps; inference time ≠ end-to-end time; cost per attempted task ≠ cost per successful outcome.**

## 1. Wall-clock time, calls, and human comparisons

| Benchmark/system | What was measured | Human comparison and limitations | Source, date, type |
|---|---|---|---|
| **OSWorld-Human: Agent S2 and GTA1** | On one successful SSH configuration task, S2 took **over 40 minutes and 50 environment steps**; GTA1 took **54 steps and almost twice as long**. Total model calls were not reported. | Human reference trajectories cover 369 tasks, but this is not a controlled, matched human-versus-agent timing experiment. | [OSWorld-Human, §3](https://arxiv.org/html/2506.16042v2), **2026-05-18 revision; MLSys 2026; primary research**. |
| **WebArena: BrowserGym + Claude 3.5 Sonnet** | Approximately **82.5 seconds/task**, **6.8 environment steps**, **$0.171/task**, **36.2% success**. | Means include failed attempts; no matched human timing in this experiment. | [BrowserGym, Tables 2 and 7](https://arxiv.org/html/2412.05467v4), **2025-02-28; primary research**. Time and cost/task are **derived** from published totals across 812 episodes. |
| **WorkArena L1**, same agent | **89.5 seconds/task**, **9.0 steps**, **$0.303/task**, **56.4% success**; 330 episodes. | No matched timed human baseline. | Same [BrowserGym source](https://arxiv.org/html/2412.05467v4); **derived means**. |
| **WorkArena L2**, same agent | **361.5 seconds/task**, **33.8 steps**, **$1.274/task**, **39.1% success**; 235 episodes. | More complex enterprise workflows; steps are not guaranteed model-call counts. | Same [BrowserGym source](https://arxiv.org/html/2412.05467v4); **derived means**. |
| **WorkArena L3**, same agent | **246.6 seconds/task**, **25.0 steps**, **$0.815/task**, **0.4% success**; 235 episodes. | The shorter runtime than L2 accompanies near-total failure, illustrating why runtime alone is misleading. | Same [BrowserGym source](https://arxiv.org/html/2412.05467v4); **derived means**. |
| **Online-Mind2Web: Operator** | **Up to 44 minutes** on challenging tasks; on successful tasks, **2.6× the human-reference action count**. | The 44 minutes is an upper-end observation, not a mean; the 2.6× ratio measures actions, not time or model calls. | [An Illusion of Progress?, §5.1](https://arxiv.org/html/2504.01382v4), **2025-10-08 revision; COLM 2025; primary research**. |
| **TheAgentCompany: Gemini 2.5 Pro/OpenHands** | **27.2 LLM calls/task** across 175 professional tasks. Unlike many benchmarks, the paper explicitly defines “steps” as LLM calls. | No formal human timing baseline or agent wall-clock table; feasibility testing did not collect human performance data. | [TheAgentCompany, Table 1 and Appendix J](https://arxiv.org/html/2412.14161v3), **2025-09-10 revision; primary research**. |
| **OSWorld 2.0** | Reports turns, tool calls, tokens and dollars; **does not tabulate agent wall-clock time**. | Human task duration has a median around **1.6 hours**, derived from annotators’ estimated time ranges—not precise stopwatch measurements. | [OSWorld 2.0](https://arxiv.org/html/2606.29537v2), **2026-07-13 revision; primary preprint**. |

There **are actual timed human baselines**, but they should not be divided into unrelated agent measurements. The original OSWorld study timed computer-science students and reported a **111.94-second median on OSWorld**, versus **35.38 seconds on 100 sampled WebArena tasks**; success was **72.36% and 88%**, respectively. This is primary research, [OSWorld §3.4, May 30, 2024 revision](https://arxiv.org/html/2404.07972). Different samples, models, and mean-versus-median statistics prevent a clean slowdown ratio against the later results above.

For WorkArena++, a **15-person study covering 98 instances** found **93.9% human success**, but I did not locate a numerical human completion-time table. It is capability evidence, rather than a usable timing denominator. [WorkArena++](https://arxiv.org/html/2407.05291v2), **2024; primary research**.

The product evidence requires additional care:

| Product evidence | Number and exact meaning | Source, date, type |
|---|---|---|
| **Gemini 2.5 Computer Use, Claude computer use, OpenAI CUA** | Approximately **220s, 285s, 295s and 325s** for Gemini, Sonnet 4.5, Sonnet 4 and OpenAI CUA, respectively. These are **average accumulated LLM inference seconds per run**, read approximately from the chart—not task wall-clock times. | [Google’s computer-use announcement](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-computer-use-model/), **2025-10-07; primary vendor/Browserbase evaluation**, Online-Mind2Web harness. |
| **Browser Use BU 1.0** | **68 seconds of inference per trajectory**, versus approximately **225–330 seconds** for comparators; reported **65.7% success**. | [Gateway announcement](https://browser-use.com/posts/llm-gateway), **2025-10-08; primary competing-vendor claim**. Its judge was modified to incorporate DOM information alongside screenshots. See also [Speed matters](https://browser-use.com/posts/speed-matters). |
| **ChatGPT agent / ChatGPT Work cloud browser** | I did not find a representative public dataset jointly reporting **wall-clock time, model calls, tokens and dollars/task**. Subscription quotas are not inference-call counts. | [ChatGPT agent launch](https://openai.com/index/introducing-chatgpt-agent/), **2025-07-17**, and [cloud-browser documentation](https://help.openai.com/en/articles/20001280-using-cloud-browser-in-chatgpt), updated approximately **August 2026; primary product documentation**. |
| **Claude in Chrome** | The official documentation does not provide a representative per-task timing/call/token-cost benchmark. Its speed-oriented model switch is documented below. | [Official product guide](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome), **August 2026 documentation; primary**. |

The often-repeated “225–330 seconds per task” product comparison is therefore **not valid evidence of measured end-to-end runtime**.

The latency breakdowns identify several distinct bottlenecks:

| Measurement | What it establishes | Source, date, type |
|---|---|---|
| **S2: 53.47% planning + 33.56% reflection; GTA1: 74.59% planning + 22.53% judging** | Across 39 profiled tasks, approximately **87% and 97%** of elapsed time went to these model-driven stages. | [OSWorld-Human, Table 1](https://arxiv.org/html/2506.16042v2), **2026-05-18; primary research**. |
| **Later calls up to 3× slower than early calls** | Latency increased as trajectory history accumulated. This is an observed within-trajectory effect, not “every step is three times slower than the immediately previous step.” | Same [paper](https://arxiv.org/html/2506.16042v2), **§3.2**. |
| **18 wasted steps, 27 minutes, $8.47** | One GTA1 loop repeatedly mislocated a control while changing Chrome’s default search engine. A concrete failure case, not an average. | Same [paper](https://arxiv.org/html/2506.16042v2), **§3.4**. |
| **WebArena: 7.6 of 12.2 seconds/step spent in the environment** | Browser/environment overhead can dominate; accelerating inference alone does not eliminate task latency. | [BrowserGym, Table 7](https://arxiv.org/html/2412.05467v4), **2025-02-28; primary research**. |
| **FocusAgent: 7.6s retrieval + 2.5s action-model call = 10.1s/step** | On 33 WorkArena L1 tasks, the additional GPT-4.1-mini retrieval stage consumed approximately **75% of model-call latency**; baseline GenericAgent needed 2.5s. Browser time excluded; retries included. | [FocusAgent, Appendix D](https://arxiv.org/html/2510.03204v2), **2026-08-29; TMLR; primary research**. |
| **1,000–1,800 tokens/screenshot; a 200K window fills in well under 100 screenshots** | Screenshot history plus instructions, tools and text creates substantial context pressure. This is token accounting, not a measured latency curve. | [Anthropic computer-use guidance](https://claude.com/blog/best-practices-for-computer-and-browser-use-with-claude), **2026-05-13; primary vendor engineering guidance**. |

## 2. Dollars, tokens, and the price of additional accuracy

The clearest recent long-workflow cost table is **OSWorld 2.0**: 108 tasks, maximum reasoning effort, a 500-step protocol, and batched actions. All figures below are **means per attempted task**, including failures.

| Model | Full completion | Estimated $/task | Output tokens/task | Tool calls/task | Turns/task |
|---|---:|---:|---:|---:|---:|
| Claude Opus 4.8 | **20.6%** | **$72.4** | **224K** | 481.8 | 103.0 |
| Claude Opus 4.7 | 18.2% | $33.6 | 150K | 597.1 | 160.7 |
| GPT-5.5 | 13.0% | $25.5 | 37.1K | 149.8 | 95.2 |

Source: [OSWorld 2.0, Table 3](https://arxiv.org/html/2606.29537v2), **2026-07-13; primary preprint**. Turns and tool calls are separately reported; neither is an independently audited total of all backend model requests.

Using the rounded figures, **$72.4 ÷ 0.206 ≈ $351 of total benchmark spending per observed full success**. That is an aggregate accounting ratio, not an estimate that repeatedly retrying any task will solve it for $351. The authors estimate **25–30K additional output tokens per accuracy point** near the frontier; this compares configurations/models and is not a universal scaling law. [Source](https://arxiv.org/html/2606.29537v2).

TheAgentCompany provides cleaner **model-call counts**, although its tasks and pricing assumptions differ:

| Model in OpenHands | Full success | LLM calls/task | API cost/attempt |
|---|---:|---:|---:|
| Gemini 2.5 Pro | 30.3% | 27.2 | $4.20 |
| Claude 3.5 Sonnet | 24.0% | 29.2 | $6.30 |
| Gemini 2.0 Flash | 11.4% | 39.9 | $0.60 |

These are 175-task averages using token prices **without prompt caching**, not total ownership costs. Source: [TheAgentCompany, Table 1](https://arxiv.org/html/2412.14161v3), **2025-09-10; primary research**. The cheaper model uses more calls while succeeding less often.

A particularly persuasive **controlled accuracy–token experiment** holds the model and agent architecture fixed:

| Candidate actions sampled at each step | WebArena-Lite success | Total input + output tokens/task |
|---|---:|---:|
| 1 | 38.8% | 96K |
| 5 | 42.4% | 460K |
| 10 | 43.2% | 920K |
| 20 | 43.0% | 1.8M |

Source: [Agentic Test-Time Scaling for WebAgents, Table 1](https://arxiv.org/html/2602.12276v2), **2026-08-14; primary preprint**; gpt-oss-120b/ReAct, 165 WebArena-Lite tasks, three seeds. Tokens sum all model calls and are predominantly input tokens.

My calculations from that table:

- **1 → 10 candidates:** **9.6× tokens** for **4.4 percentage points** more success.
- **1 → 5:** approximately **101K extra tokens per additional accuracy point**.
- **5 → 10:** approximately **575K per point**, a **5.7× increase in marginal token cost**.
- Further doubling to 20 candidates provides no improvement.

This diagnoses inefficient uniform sampling; the paper’s adaptive method improves the tradeoff, so the result is not evidence that such spending is unavoidable. [Source](https://arxiv.org/html/2602.12276v2).

A useful counterexample prevents overgeneralizing the expensive results: Microsoft’s **Webwright** reports **$2.37/task at 86.7% success with GPT-5.4**, and **$6.09 at 84.7% with Opus 4.7**, on Online-Mind2Web. These use programmatic browser interaction and automated judging, not exclusively screenshot clicking. Source: [Microsoft Research](https://www.microsoft.com/en-us/research/articles/webwright-a-terminal-is-all-you-need-for-web-agents/), **2026-05-04; primary vendor research**.

## 3. Agentic token consumption: share and growth

The strongest available numbers are platform-specific. **I did not find a defensible measurement of agents’ share of all worldwide LLM tokens.**

| Number | Exactly what it measures—and what it does not | Source, date, type |
|---|---|---|
| **Agents ≈4× chat tokens; multi-agent systems ≈15×** | Anthropic’s operational comparison. No matched-task sample or distribution is disclosed; not specifically GUI agents. | [Multi-agent research engineering report](https://www.anthropic.com/engineering/multi-agent-research-system), **2025-06-13; primary vendor statement**. |
| **Programming: ~11% → >50% of token volume during 2025** | OpenRouter’s 100T-token study. **Programming is a proxy, not an agent classification**; code chat also counts. | [State of AI](https://openrouter.ai/state-of-ai), **December 2025; primary platform study**. |
| **Agentic requests ≈15× human-request tokens; agentic volume overtook human volume around early February 2026** | OpenRouter logs covering **450T+ input/output tokens, January 1–June 14**. API keys classified Agentic/Mixed/Human using seven behavioral signals. Surpassing “Human” does not necessarily mean exceeding half of all traffic because “Mixed” exists. | [OpenRouter analysis](https://openrouter.ai/blog/insights/deepseek-v4-adoption/), **2026-06-30; primary vendor telemetry**. |
| **Agentic tokens grew 14× in roughly six months; human tokens grew 2.8×** | Same platform’s classified traffic; **nearly 70% of agentic tokens were cached prompt tokens**. Consequently, 14× tokens does not mean 14× expenditure or computation. | [Peter Walker, OpenRouter Head of Insights](https://www.linkedin.com/feed/update/urn:li:activity:7493029883191681024/), **August 2026; primary vendor telemetry statement**. |
| **Codex: 63.3% of organizational output tokens; 16.5% of individual output tokens** | Share of **Codex + ChatGPT output tokens**, preceding 28 days through June 11, 2026. Excludes input tokens and other providers; Codex is a product proxy for agency. | [The Shift to Agentic AI: Evidence from Codex](https://cdn.openai.com/pdf/5d1e1489-21c0-43e4-9d42-f87efdbf0082/the-shift-to-agentic-ai-evidence-from-codex.pdf), **2026-06-25; primary vendor research**. |
| **5–30× tokens/task relative to standard GenAI chatbots** | Gartner’s analyst estimate; the public release does not disclose a reproducible task sample. It is not a measured global share. | [Gartner release](https://www.gartner.com/en/newsroom/press-releases/2026-03-25-gartner-predicts-that-by-2030-performing-inference-on-an-llm-with-1-trillion-parameters-will-cost-genai-providers-over-90-percent-less-than-in-2025), **2026-03-25; primary publication of an analyst estimate**. |

These establish the **scale and growth of the efficiency problem**. High consumption alone does not establish poor economic value.

## 4. Deployment and adoption evidence

| Finding | Sample, question and interpretation | Source, date, type |
|---|---|---|
| **20% named latency as their biggest production barrier**, second behind quality | **1,340 respondents**; fieldwork November 18–December 2, 2025. This directly connects latency to production difficulty, although the sample is technology-heavy. | [LangChain State of Agent Engineering](https://www.langchain.com/state-of-agent-engineering), [resource listing dated 2026-02-25](https://www.langchain.com/resources/state-of-agent-engineering); **primary vendor survey**. |
| **79.8% said agent operating cost was a meaningful factor in usage decisions** | **554 agent-using engineers/leaders**; fieldwork April 29–May 25, 2026. Mostly coding-related usage. **This does not mean 79.8% could not deploy**; the same survey reports 91.1% perceived productivity improvements. | [Temporal State of Development](https://temporal.io/reports/state-of-development-2026), **2026-08-25; primary commissioned survey**. |
| **31 users, 62 task attempts** exposed frustration with slow Operator/Manus execution | Think-aloud study spanning holiday planning, slides and stipend budgeting. Participants described manual browser actions as faster; delays, hangs and recovery impeded interaction. **Qualitative evidence**, not a quantified abandonment rate. | [Why Johnny Can’t Use Agents](https://arxiv.org/html/2509.14528v1), **2025-09-18 preprint; primary academic user study**. |
| **14.8% considered latency critical; 59.3% considered it marginal but deployable** | Important counterevidence: **27 deployed-agent responses** to the latency question; **15/20 interviewed systems operated asynchronously**. Deployment selection and task type matter. | [Measuring Agents in Production](https://arxiv.org/html/2512.04123v4), **2026-06-04 revision; ICML 2026; primary research**. |

For a professor-facing argument, the survey evidence supports **“latency materially restricts deployment and interaction design.”** It does not establish that most deployed agents are unusable.

## 5. Vendor moves explicitly targeting speed and cost

| Move | Quantified claim or product decision | Source, date, type |
|---|---|---|
| **Claude in Chrome defaulted to Haiku 4.5** | Anthropic explicitly changed the default for faster, more responsive browsing. **No numerical task-speed improvement disclosed.** | [Official release notes](https://support.claude.com/en/articles/12138966-release-notes), **2025-10-15; primary product record**. |
| **Lower reasoning effort for Claude computer use** | Internal tests found **medium effort used roughly half the output tokens of high**, with the same eventual success when retries were allowed. | [Computer-use best practices](https://claude.com/blog/best-practices-for-computer-and-browser-use-with-claude), **2026-05-13; primary vendor experiments**, incomplete sample details. |
| **Gemini 3.5 Flash-Lite with native computer use** | **$0.30/M input tokens and $2.50/M output tokens**; advertised **350 output tokens/second**. Throughput is not task-completion speed. | [Google launch](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/), **2026-07-21; primary product/pricing source; secondary attribution to Artificial Analysis for throughput**. |
| **OpenAI Fast mode replaced Priority Processing** | GPT-5.6 Sol: **up to 2.5× speed at 2× price**, with unchanged intelligence. Explicit monetization of lower latency; not a browser-task benchmark. | [OpenAI price-performance announcement](https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/), **2026-07-30; primary vendor claim**. |
| **Agent orchestration improvements** | OpenAI-hosted customer reports: Ciridae **4× latency reduction**, evaluation **0.71→0.85**; SafetyKit **60% lower cost/case** with maintained performance. | [Agents API launch](https://openai.com/index/introducing-the-agents-api/), **2026-09-10; primary customer testimonials hosted by vendor**. No disclosed sample or absolute runtime; not specifically GUI workflows. |
| **Claude Opus 5.5 Fast mode** | **Up to 2.5× speed**; fast input/output pricing **$8/$40 per million**, versus standard **$4/$20**. | [Anthropic launch](https://www.anthropic.com/claude-opus-5-5), **2026-09-22; primary vendor claim**. Service/generation acceleration, not demonstrated 2.5× end-to-end browser acceleration. |

These moves are strong evidence that vendors consider latency and efficiency commercially important. Their reported improvements also mean that 2025 measurements should not be presented as measurements of every September 2026 product.

## Five numbers for a senior ML professor

The **five numbers I would put in front of a senior ML professor** are:

1. **Approximately 87–97% of execution time went to planning/reflection/judging in the OSWorld-Human profiling study**—this identifies a concrete, measurable systems bottleneck that task-success leaderboards hide. [Source](https://arxiv.org/html/2506.16042v2).
2. **OSWorld 2.0’s strongest tested configuration spent about $72.40 per attempt while fully completing only 20.6% of tasks**—this directly couples inference expenditure with the reliability of realistic long workflows. [Source](https://arxiv.org/html/2606.29537v2).
3. **WebArena-Lite required 9.6× more tokens for just 4.4 additional accuracy points under uniform action sampling**—the controlled experiment demonstrates sharply diminishing returns without changing the base model. [Source](https://arxiv.org/html/2602.12276v2).
4. **OpenRouter’s agentic token volume grew 14× in roughly six months**—platform telemetry shows why agent efficiency has become consequential at scale, even after accounting for substantial caching. [Source](https://www.linkedin.com/feed/update/urn:li:activity:7493029883191681024/).
5. **20% of 1,340 LangChain survey respondents named latency their biggest production barrier**—this connects the technical bottleneck to a reported deployment obstacle in a large practitioner sample. [Source](https://www.langchain.com/state-of-agent-engineering).
