# Computer-Use and Web Agents Are Too Slow and Too Expensive for Real Work: The Citable Evidence (as of 25 Sept 2026)

The strongest primary evidence says the same thing from several angles. On OSWorld, a computer-use agent took 12 minutes to double-space two paragraphs, a task a novice does in under 30 seconds. Large-model calls for planning, judging and reflection account for roughly 76–97% of that wall-clock time. Screenshots and action execution together account for under 3.5%.\[1\] On OSWorld 2.0's human-scale tasks, the best agent completes only about one in five, and it spends about 6× more output tokens than GPT-5.5 (224K vs 37.1K per task, per the paper's Table 3) to gain 7.6 extra points (20.6% vs 13.0%).

## TL;DR
- **Latency is an inference problem, and it compounds.** OSWorld-Human (MLSys 2026) finds that planning plus judging or reflection LLM calls take 87–97% of task time. Later steps take up to 3× longer than early ones because every prompt re-sends the screenshot history. Agents take 2.7–4.3× more steps than a human-annotated trajectory. On live-web tasks (Online-Mind2Web), frontier computer-use models average about 225–330 s per task, according to a vendor measurement by Browser Use.
- **Accuracy gets expensive at the margin.** On OSWorld 2.0 (Table 3, 500 steps, batched tools), GPT-5.5 reaches 13.0% at 37.1K output tokens per task (about $25.5 per task), while Claude Opus 4.8 reaches 20.6% at 224K (about $72.4 per task); the authors state that "each additional point of accuracy costs disproportionately more tokens," put at "roughly 25 to 30K extra tokens for each additional point." On HAL's Online Mind2Web, a 2-point accuracy gain cost 9× more ($1,577 vs $171 per 300-task run). The most expensive model sat on the cost-accuracy frontier in only 1 of 9 benchmarks.
- **Demand is exploding and vendors are pricing speed as a premium.** Google reports 3.2 quadrillion tokens per month (7× year over year). The OpenRouter/a16z study reports that reasoning models' token share went from "effectively a negligible slice of usage in early Q1" to one that "now exceeds fifty percent." It also reports that average prompt tokens per request rose "roughly fourfold from around 1.5K to over 6K." Anthropic and OpenAI both sell "fast mode" at up to 2.5× output speed for a premium; Anthropic's is 2× standard price for Opus 5.5. Survey evidence that latency or cost *blocks* deployment is weaker. Latency is the #2 barrier (20%) in LangChain's survey, but a peer-reviewed practitioner study finds only 14.8% call it a hard blocker.

---

## 1. Wall-clock time and number of model calls: agents vs. humans

### Benchmarks

**OSWorld-Human (Abhyankar, Qi, Zhang; UCSD/GenseeAI)**
Source: "OSWorld-Human: Benchmarking the Efficiency of Computer-Use Agents," https://arxiv.org/abs/2506.16042. First posted June 2025; MLSys 2026 (oral) version at https://arxiv.org/html/2506.16042. **Primary.**
- **Headline anecdote.** "changing the line spacing of two paragraphs in a document to double-spaced takes 12 minutes for a computer-use agent. However, for a human user with introductory computer experience, this task should take under 30 seconds." That is roughly 24× slower. The human figure is the authors' estimate, not a timed human trial.\[1\]
- **Worked example (SSH-user task).** Agent S2 (GPT-4.1 planner) used all 50 of its allowed steps and took "over 40 minutes" end to end. GTA1 (o3 planner and judge) succeeded in 54 steps "whereas the end-to-end latency is almost twice that of Agent S2."\[1\]
- **Setup.** 39-task OSWorld subset (10% of the benchmark), with full timing and token traces collected. Grounding models ran on a single A6000 with SGLang.\[1\]
- **Latency breakdown (Table 1, average % of total task time):**

| Agent | Screenshot | Action exec | Planning (LLM) | Judging (LLM) | Reflection (LLM) | Retrieval (LLM) | Grounding (small VLM) |
|---|---|---|---|---|---|---|---|
| GTA1 | 0.36% | 0.70% | 74.59% | 22.53% | – | – | 1.82% |
| Agent S2 | 1.72% | 1.61% | 53.47% | – | 33.56% | 3.08% | 3.91% |

  By application, planning plus reflection is 76–96% of S2's latency and planning plus judging is 91–96% of GTA1's. The authors conclude: "screenshot and action execution are the least intensive for both agents."\[1\]
- **Why it grows with steps.** "as an agent uses more steps to complete a task, each successive step can take 3× longer than steps at the beginning of a task." The cause is that "at each step, the prompt sent to the LLM includes the history of all previous steps… if the agent is on step 10, the prompt will include the screenshot for steps 1-9." Planning, reflection and judging latency "is dominated by the prefill stage of LLM inference due to the large number of prompt tokens."\[1\]
- **Observation cost.** Generating an accessibility tree takes "anywhere from 3 seconds to 26 seconds" per observation, and the tree adds thousands of prompt tokens per step.\[1\]
- **Number of model calls.** GTA1 makes 4 parallel o3 planning calls per step, with up to 3 retries each, so "for every judging call, there can be between 4 and 12 planning calls."\[1\]
- **Efficiency vs. humans.** Across 16 agents, "even the best agents take 2.7−4.3× more steps than necessary." The best agent (Agent S2 with Gemini 2.5) has a 41.4% OSWorld success rate but only 15.6% on the Weighted Efficiency Score (WES). Human reference trajectories average 2.8–13.2 single actions per task depending on the application. **Contradiction to note:** the earlier arXiv/workshop abstract says "1.4–2.7×"; the MLSys 2026 version says 2.7–4.3×.\[1\]\[2\] Cite the MLSys version and say which one you are using.

**OSWorld 2.0 (XLANG Lab and collaborators)**
Source: "OSWorld 2.0: Benchmarking Computer Use Agents on Long-Horizon Real-World Tasks," https://arxiv.org/abs/2606.29537 (v1 28 June 2026; PDF dated 15 July 2026); leaderboard at https://osworld-v2.xlang.ai/. **Primary.**
- **Task length vs. humans.** 108 tasks. "The median task takes a skilled human about 1.6 hours of active operation, roughly 48× longer than OSWorld 1.0". The OSWorld 1.0 median is about 2 minutes, and 69.6% of OSWorld 2.0 tasks take a skilled human more than an hour. Human times were recorded by two annotators who timed each task.\[3\]\[4\]\[5\]
- **Model calls.** Tasks require "an average of 318 tool calls with Claude Opus 4.7 using maximum thinking, compared with about 30 in OSWorld 1.0". The introduction says "leading agents average more than 300 steps per task", but §2.2.1 gives "more than 250 steps per task under our strongest evaluation setting." In the batched-tool configuration, where several actions can be batched into one step, the paper's Table 3 reports average steps per task of 95.2 for GPT-5.5 and 103 for Opus 4.8.
- **Outcome.** The best configuration, Claude Opus 4.8 with max thinking and batched tools at a 500-step budget, reaches 20.6% binary completion and 54.8% partial score. Completion "falls to zero for every model" on tasks longer than 163 human-minutes.\[4\]\[5\]
- **Latency as a failure mode.** The authors list "Agents fail on time-sensitive tasks when long observation-to-action gaps make their actions target stale interface states." In other words, slowness directly causes errors on streaming or dynamic UIs.\[5\]
- **Gap:** OSWorld 2.0 does **not** report agent wall-clock time. Its efficiency axis is output tokens, turns and steps, so you cannot use it for an agent-vs-human minutes comparison.

**TheAgentCompany (CMU et al.)**
Source: "TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks," https://arxiv.org/html/2412.14161v2; NeurIPS 2025 Datasets & Benchmarks PDF at https://papers.nips.cc/paper_files/paper/2025/file/0d744742f6fac4d1134c019b7cef3c8a-Paper-Datasets_and_Benchmarks_Track.pdf. **Primary.**
- Best model (Gemini 2.5 Pro, OpenHands CodeAct) completes 30.3% of 175 tasks, 39.3% with partial credit. "It requires an average of almost 27 steps and more than $4 to complete each task, making it an expensive model to run both in time and in cost."\[6\]\[7\]
- Gemini 2.0 Flash "requires 40 steps on average… yet only to achieve one-third of the success rate compared to the top-performing model," at under $1 per task.\[8\]
- Earlier version (v1, Dec 2024): Claude 3.5 Sonnet averaged 29.17 steps and $6.34 per task at 24% success.\[9\] This figure is reported via a secondary Medium summary (https://cobusgreyling.medium.com/the-battle-of-ai-agents-comparing-real-world-performance-using-benchmarking-356a8c6e0fcc), so treat it as **secondary** unless you pull the v1 table.
- **Gap:** no wall-clock time per task and no human completion-time baseline are reported.

**Online-Mind2Web wall-clock (via Browser Use)**
Source: "Speed Matters: How Browser Use Achieves the Fastest Agent Execution," https://browser-use.com/posts/speed-matters, 9 Oct 2025. **Primary vendor measurement, and a marketing context:** Browser Use is comparing competitors against its own product.
- Average task completion time on Online-Mind2Web: Gemini 2.5 Computer Use 225 s, Claude Sonnet 4.5 285 s, Claude Sonnet 4 295 s, OpenAI Computer-Using Model 330 s, BU 1.0 (the vendor's own) 68 s at about 3 s per step. On one GitHub lookup task, BU 1.0 took 15 s and Gemini 2.5 CU took 1 min 15 s.\[10\]
- **Definition caveat:** the post does not say whether the times include browser startup or judge time. Browser Use also modified the Online-Mind2Web judge to see the DOM as well as screenshots, so accuracy numbers are not directly comparable to the official judge.\[10\]

**Gaps: WebArena and WorkArena.** I found no primary source reporting per-task wall-clock time or a human-time baseline for current agents on WebArena or WorkArena/WorkArena++. The original WebArena human success rate (about 78%) is a success-rate comparison, not a timing comparison. Treat this as a hole in the evidence.

### Products

- **ChatGPT agent (OpenAI).** Secondary launch coverage (July 2025) reports that task completion time varies, "with some taking 15 to 30 minutes." That quote comes from AlternativeTo, https://alternativeto.net/news/2025/7/openai-launches-a-new-chatgpt-agent-tool-for-autonomous-multi-step-task-completion (**secondary**), and does not appear in OpenAI's own launch post. The quota comes from OpenAI's post "Introducing ChatGPT agent" (17 Jul 2025, **primary**): "Pro users have 400 messages per month, while other paid users get 40 messages monthly."
  - A hands-on review timed a 10-restaurant Google Maps list at about 20–23 minutes with one human intervention for login, and noted that "even simple actions like clicking, selecting elements, and searching can take the agent several seconds—or even minutes."\[11\] Source: "My Honest Review of ChatGPT Agent," https://artificialcorner.com/p/my-honest-review-of-chatgpt-agent, 2025. **Secondary / anecdotal.**
- **Gemini 2.5 Computer Use (Google DeepMind).** Google claims "leading quality for browser control at the lowest latency, as measured by performance on the Browserbase harness for Online-Mind2Web."\[12\] Source: "Introducing the Gemini 2.5 Computer Use model," https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-computer-use-model/, Oct 2025. **Primary vendor claim.**
  - The accompanying chart's figure of about 225 s latency at 70%+ accuracy is reported in secondary coverage (e.g., https://apidog.com/blog/gemini-2-5-computer-use-model/). \[13\] **Secondary.**
  - Browserbase-harness accuracy was 65.7% for Gemini 2.5 CU, 61.0% for Claude Sonnet 4 and 44.3% for the OpenAI agent, per VentureBeat, https://venturebeat.com/ai/googles-ai-can-now-surf-the-web-for-you-click-on-buttons-and-fill-out-forms. \[14\] **Secondary.**
- **Claude computer use / Claude in Chrome; OpenAI Operator; "ChatGPT Work cloud browser."** I found no vendor-published per-task wall-clock or model-call counts. The only timings for Claude and OpenAI computer-use models are the Browser Use competitor figures above (285–330 s). **Evidence missing.**

---

## 2. Token and dollar cost per task, and how cost scales with accuracy

**OSWorld 2.0 cost-accuracy curve (the explicit "marginal point" finding)**
Source: https://arxiv.org/pdf/2606.29537, section headed "Each additional point of accuracy costs disproportionately more tokens," June/July 2026. **Primary.**
- "GPT-5.5 is the most token-efficient agent by a wide margin, reaching ∼14% binary reward at only ∼37K output tokens per task… But GPT-5.5 plateaus there, with its 150-, 300-, and 500-step points all converging near ∼14%… Claude Opus 4.7 reaches 18.2% at around 150K tokens, while Claude Opus 4.8 reaches the best result on the benchmark, 20.5%, at around 225K." The abstract adds that GPT-5.5 plateaus "at under a fifth of Opus's token budget, so higher completion comes only at a steeply rising token cost." The paper's Table 3 (500 steps, batched) gives the raw figures as 13.0% binary at 37.1K output tokens per task for GPT-5.5 and 20.6% at 224K for Opus 4.8.
- **The marginal cost, as the paper states it:** going from GPT-5.5 to Opus 4.8 costs about 6× the output tokens, which the authors put at "roughly 25 to 30K extra tokens for each additional point."
- **Measurement:** Table 3 reports output tokens per task and cost per task: "∼$72.4" for Opus 4.8, "∼$33.6" for Opus 4.7, "∼$25.5" for GPT-5.5 (batched) and "∼$2.4" for MiniMax M3. Input and prompt tokens, which dominate prefill latency in OSWorld-Human, are not broken out in the token figure.
- The authors also report that agents spend "under 7%" of their budget on detecting and repairing their own errors.\[5\]

**Holistic Agent Leaderboard (HAL), Princeton SAgE**
Sources: "Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation," https://arxiv.org/abs/2510.11977 (v1 13 Oct 2025; ICLR 2026); leaderboards at https://hal.cs.princeton.edu/online_mind2web and https://hal.cs.princeton.edu/assistantbench. **Primary.**
- **Measurement definition.** "Total Cost — Total API cost for running the agent on all tasks." Costs are "calculated without accounting for caching benefits." Token prices are as of 24 Sept 2025. Browser-agent rows are single runs, "Verified" by the HAL team. The leaderboard is currently paused.\[15\]\[16\]
- **The key marginal-cost fact.** "on Online Mind2Web, SeeAct with GPT-5 Medium costs $171 while Browser-Use with Claude Sonnet 4 costs $1,577: a 9x difference in cost despite just a two-percentage-point difference in accuracy" (42.33% vs 40.00%).\[15\]\[16\] Divided over 300 tasks, that is about $0.57 vs $5.26 per task (my division).
- **Pareto structure.** "In only 1 of 9 benchmarks do we observe the most costly model run on the Pareto frontier." The team also "did not run Opus 4.1 on Online Mind2Web due to budget limits, as we estimated it would cost about $20,000." Online Mind2Web "averages over $450" per evaluation run, making it HAL's most expensive benchmark.\[16\]\[17\]
- **More compute ≠ more accuracy.** "higher reasoning effort reducing accuracy in the majority of runs"\[17\] (21 of 36).\[16\]
- **Selected per-task costs** (my division of HAL totals; Online Mind2Web n=300, AssistantBench n=33):

| Benchmark | Scaffold + model | Accuracy | Total $ | ≈ $/task |
|---|---|---|---|---|
| Online Mind2Web | SeeAct + GPT-5 Medium | 42.33% | 171.07 | 0.57 |
| Online Mind2Web | Browser-Use + Claude Sonnet 4 | 40.00% | 1,577.26 | 5.26 |
| Online Mind2Web | Browser-Use + Claude Sonnet 4 High | 39.33% | 1,609.92 | 5.37 |
| Online Mind2Web | Browser-Use + Gemini 2.0 Flash | 29.00% | 8.83 | 0.03 |
| AssistantBench | Browser-Use + o3 Medium | 38.81% | 15.15 | 0.46 |
| AssistantBench | Browser-Use + Claude Opus 4.1 High | 13.75% | 779.72 | 23.63 |

  Caveat: HAL's AssistantBench page describes a 214-task benchmark but appears to run a 33-task subset. Opus 4.1's low AssistantBench score is partly an artifact of the "do not guess" prompt, per the paper.\[16\]\[18\]
- **Overall scale.** 21,730 rollouts across 9 models and 9 benchmarks cost "about $40,000."\[16\]\[17\]

**OSWorld-Human cost analysis (GTA1 with o3)**
Source: https://arxiv.org/html/2506.16042 (MLSys 2026). **Primary.**
- "On average, a task costs $2.43, with planning, judging, and grounding being responsible for 87%, 13%, and less than 1%, respectively." Accumulated cost shows a "quadratic increase" over steps because context accumulates.\[1\]
- One failed loop, a grounding error on "set Bing as default search engine," "costed $8.47 and 27 minutes of wall-clock time."\[1\]
- In failed tasks over 50 steps, "66% of steps are wasted by the agent being stuck in a loop."\[1\]
- **Internal inconsistency to flag:** Table 3's token totals across the 39 tasks sum to about $307 (87.34M o3 prompt tokens plus 10.29M output tokens for planning; 17.94M plus 1.59M for judging, priced at Together AI's $2/$8 per million). That is about $7.9 per task, not $2.43. Either the table spans multiple runs or one figure is wrong. Quote the $2.43 as stated, but note the discrepancy.

**TheAgentCompany per-task cost**
Top model: more than $4 per task and about 27 steps at 30.3% success. Gemini 2.0 Flash: under $1 per task, 40 steps, about one-third of the success rate.\[6\]\[8\] The earlier Claude 3.5 Sonnet figure was $6.34 per task.\[9\] Sources as in §1. **Primary** (the v1 Claude figure is secondary).

**Browser Use reports (vendor)**
- **Latency mechanics.** "each screenshot adds ~0.8 seconds to LLM inference latency." On their own models, 1,000 input tokens take 29.1 ms while 10 output tokens take 62.6 ms, so per token, output costs about 215× more time than input.\[10\] Source: https://browser-use.com/posts/speed-matters, 9 Oct 2025. **Primary vendor measurement, not independently replicated.**
- **Throughput.** Their managed agent completes "~14 tasks per hour"; GPT-5 is "the slowest at ~6 tasks per hour." Anthropic's claude-fable-5 scored 80.0% "at $580.87 in API cost per 100-task run," about $5.81 per task.\[19\] Source: "Browser Agent Benchmark," https://browser-use.com/posts/ai-browser-agent-benchmark, updated June 2026. **Primary vendor; marketing context.**
- **Cost per solved task.** Browser Use claims "82% of tasks solved at 17¢ each… 20 points better than Opus 5, which costs 20× more per solved task." Cost is defined as "total recorded spend for the run divided by the number of tasks actually solved" on a 106-task internal set.\[20\] Source: https://browser-use.com/benchmarks/agents, 2026. **Vendor-marketing claim on a private benchmark; do not treat as independent.**

**Gaps.** I found no primary per-task dollar figures for WebArena or WorkArena. OSWorld 2.0 does report dollars per task in its Table 3 (about $72.4 for Opus 4.8, $33.6 for Opus 4.7, $25.5 for GPT-5.5 batched, $2.4 for MiniMax M3). I did not retrieve ARC-AGI cost-per-task data or Browserbase cost reports.

---

## 3. Agentic workloads' share and growth of token consumption (2025–2026)

**OpenRouter × a16z, "State of AI: An Empirical 100 Trillion Token Study"**
Sources: https://arxiv.org/abs/2601.10088 (Dec 2025; arXiv 15 Jan 2026); https://openrouter.ai/state-of-ai; a16z summary at https://a16z.com/state-of-ai/. **Primary** (platform metadata, Nov 2024–Nov 2025).
- Section 4.1 is titled "Reasoning Models Now Represent Half of All Usage." It says reasoning models' token share went from "effectively a negligible slice of usage in early Q1" to one that "now exceeds fifty percent." "The fastest-growing behavior on OpenRouter is what we call agentic inference."
- §4.3: "Average prompt tokens per request have increased roughly fourfold from around 1.5K to over 6K while completions have nearly tripled from about 150 to 400 tokens"; the growth in completions is "mostly due to reasoning tokens"; "programming-related prompts now average 3–4 times the token length of general-purpose prompts."
- Context from the a16z page: "OpenAI's entire API averaged about 8.6 trillion tokens per day in October."\[21\]
- **Caveats:** OpenRouter is one routing platform and not representative of first-party API traffic. Agentic share is inferred from reasoning share, tool-call share and sequence length, not directly measured. "agentic inference will be taking over the majority of the inference" is a forecast, not a measurement.\[22\]

**Google (Sundar Pichai, I/O 2026 keynote)**
Source: https://blog.google/innovation-and-ai/sundar-pichai-io-2026/, 19–20 May 2026. **Primary vendor statement, unaudited.**
- Monthly tokens: "9.7 trillion tokens a month" (May 2024) → "roughly 480 trillion" (May 2025) → "over 3.2 quadrillion per month" (May 2026), a 7× increase year over year and about 330× over two years.\[23\]\[24\]
- "Our model APIs are now processing roughly 19 billion tokens per minute"; "over 375 Google Cloud customers each processed more than one trillion tokens."\[23\]
- Google does **not** break out the agentic share.

**NVIDIA (Jensen Huang)**
- **Feb 2025:** reasoning requires "100 times more" computation than earlier models.\[25\] Source: NBC News, https://www.nbcnews.com/business/business-news/nvidia-ceo-huang-says-ai-100-computation-now-chatgpt-was-released-rcna194081. **Secondary report of a vendor claim.**
- **Morgan Stanley TMT conference, 2026:** "Agentic AI can consume 1 million times more tokens than a standard generative prompt."\[26\] Source: https://www.morganstanley.com/insights/articles/nvidia-jensen-huang-compute-new-economic-engine-tmt-2026. **Secondary (bank summary of a vendor CEO claim; no methodology).**
- **ServiceNow Knowledge, 5 May 2026:** compute for agentic AI "has increased 1,000% compared to generative AI just two years ago."\[27\]\[28\] Source: Fortune, https://fortune.com/2026/05/06/jensen-huang-servicenow-bill-mcdermott-agentic-ai-robos/. **Secondary.**
- These three multipliers (100×, 1,000%, 1,000,000×) are mutually inconsistent, unsourced and made by a seller of compute. Present them as rhetoric, not data.

**Gartner (via secondary)**
Agentic models "can consume 5x to 30x more tokens per task than a standard chatbot."\[29\] This is reported in a Medium post, https://medium.com/@silverag79/the-token-economy-is-here-how-jensen-huang-is-rewriting-the-rules-of-work-83700ddd6e39. **Secondary; I could not verify the original Gartner document.** Use only with that caveat.

**Menlo Ventures, "2025: The State of Generative AI in the Enterprise"**
Source: https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise/, 9 Dec 2025. Survey of 495 US enterprise decision-makers, 7–25 Nov 2025.\[30\] **Primary.**
- Enterprise genAI spend is $37B in 2025 (vs $11.5B in 2024). Foundation-model APIs are $12.5B of that.\[30\]\[31\]
- Only 16% of enterprise deployments and 27% of startup deployments qualify as true agents.\[32\] This last figure comes via the SemanticOS summary, https://semanticos.io/blog/menlo-state-of-genai-enterprise-spend. **Secondary for that figure.**
- This is a spending measure, not a token-share measure.

**Missing.** I found no primary 2025–2026 token-share figures from OpenAI (beyond a16z's 8.6T tokens per day), Anthropic, Microsoft, Cerebras or Groq. I also found none from Sequoia, Morgan Stanley or Goldman Sachs research, Barclays, SemiAnalysis, Epoch AI or Artificial Analysis. **No source I found directly measures "agentic share of all tokens."**

---

## 4. Surveys and user studies: do latency or cost block deployment?

**LangChain, "State of Agent Engineering"**
Source: https://www.langchain.com/state-of-agent-engineering. 1,300+ respondents (reported elsewhere as 1,340), fielded 18 Nov–2 Dec 2025.\[33\]\[34\] **Primary vendor survey, self-selected sample.**
- "Quality remains the biggest barrier to production… one third of respondents cited quality as their primary blocker" (32%).\[33\]
- "Latency has emerged as second biggest challenge (20%)… more capable, multi-step agents can deliver higher quality outputs but often with slower responses."\[33\]
- "In contrast, cost is less frequently cited as a concern than in previous years."\[33\]
- 57% have agents in production.\[33\]
- Secondary coverage (KDnuggets, https://www.kdnuggets.com/the-state-of-agent-engineering-report-overview) says latency is the #2 barrier for smaller companies and security for enterprises with more than 2,000 employees.\[35\]
- **Date conflict:** one secondary source says the report was published 23 May 2026.\[34\] The fielding dates are consistent across sources.

**"Measuring Agents in Production" (MAP)**
Source: https://arxiv.org/abs/2512.04123 (v4 June 2026; the PDF header says ICML 2026, while IBM lists it as ICLR 2026). 306 practitioners surveyed July–Oct 2025 plus 20 interviews; 86 respondents in production or pilot.\[36\] **Primary, peer-reviewed.**
- "only 14.8% of deployed survey agents identify latency as a critical deployment blocker… the majority (59.3%) report it as a marginal issue, where current latency is suboptimal but sufficient for deployment." These percentages are 4, 16 and 7 of N=27 respondents to that question.\[36\]
- "66% allow response times of minutes or longer, and 17% set no explicit limit" (N=53). "Only 5 of 20 cases require real-time responsiveness."\[36\]
- On cost, teams "report that runtime costs remain negligible compared to alternative expert labor costs."\[36\] **There is no cost-blocker percentage in this paper.**
- **Interpretation:** this is the strongest *counter*-evidence to your thesis. Teams that deploy agents route around latency by running them asynchronously and offline.\[36\] The honest reading is that latency constrains *which* tasks are deployable (interactive, customer-facing ones), not whether agents get deployed at all.

**Gartner press release (25 June 2025)**
Source: https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027. **Primary analyst forecast (a prediction, not a measurement).**
- "Over 40% of agentic AI projects will be canceled by the end of 2027, due to escalating costs, unclear business value or inadequate risk controls."\[37\]
- The accompanying poll of 3,412 webinar attendees (Jan 2025) measured investment posture, not blockers.\[37\]
- The claim is often misdated as 2026 news in secondary coverage.\[38\]

**Datadog (via secondary)**
"rate limit errors account for 60% of LLM call failures" because agent loops create concurrency spikes (Datadog 2026 State of AI Engineering).\[39\] Reported by NoCode.Tech, https://www.nocode.tech/article/langchain-report-quality-not-cost-killing-ai-agents. **Secondary; unverified.**

**Missing.** I found no McKinsey, Deloitte, Bain, BCG, KPMG, PwC or Cleanlab figure giving a percentage who cite *latency* or *speed* as a blocker. I also found no academic HCI user study measuring user tolerance of computer-use-agent wait times. The MIT NANDA "95% fail" figure concerns ROI, not latency, and I did not retrieve it.

---

## 5. Vendor product moves that treat speed as the bottleneck

- **Anthropic fast mode.** "Fast mode delivers up to 2.5x higher output tokens per second from Claude Opus 5.5, Claude Opus 5, and Claude Opus 4.8 at premium pricing". "Speed benefits are focused on output tokens per second (OTPS), not time to first token (TTFT)". It uses the "Same model weights". It is a research preview on the Claude API, including Claude Managed Agents.\[40\]
  - Source: Claude Platform Docs, https://platform.claude.com/docs/en/build-with-claude/fast-mode, 2026. **Primary.**
  - Pricing for Opus 5.5 (released 22 Sept 2026) is $8/$40 per million tokens in fast mode vs $4/$20 standard, i.e. 2× price.\[41\]\[42\]\[43\] Source: https://www.anthropic.com/claude/opus. **Primary.**
  - Note: because OSWorld-Human shows latency is dominated by *prefill* of long screenshot-laden prompts, an OTPS-only speedup addresses only part of computer-use latency.
- **OpenAI Priority processing → "Fast mode".** "Priority processing was renamed Fast mode on July 30, 2026. We also increased the speed at which Fast mode operates for gpt-5.6-sol to make it up to 2.5× faster than Standard processing." It is billed "at a premium relative to Standard processing rates."\[44\]\[45\]
  - Sources: https://developers.openai.com/api/docs/guides/priority-processing and https://openai.com/api-priority-processing/. **Primary.**
  - The opposite tier, **Flex processing**, is priced at Batch API rates "in exchange for slower response times and occasional resource unavailability."\[46\] Source: https://developers.openai.com/api/docs/guides/flex-processing. **Primary.**
  - The explicit trade of speed against price is itself evidence that speed is a scarce resource.
- **Microsoft Foundry priority processing.** The latency target is stated as e.g. "99% > 50 Tokens per Second". Requests "estimated to exceed 128k prompt tokens are downgraded to standard processing".\[47\] Long-context agent traces are therefore excluded from the fast tier. Source: https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/priority-processing. **Primary.**
- **Google Gemini Flash computer use.** On 24 June 2026, "Computer use is now a built-in tool supported in Gemini 3.5 Flash… Previously only available as a standalone Gemini 2.5 computer use model."\[48\] Source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-computer-use-gemini-3-5-flash/. **Primary.**
  - Secondary coverage cites about 289 tokens/s and "4x faster" than rival frontier models; these are **vendor-stated and not independently verified at launch.**\[49\]
  - Gemini 3.8 Flash (2 Sept 2026) is reported at about 305 tokens/s, "the fastest output speed Artificial Analysis has measured," at $0.75/$3.75 per million tokens.\[50\] Source: Beam AI, https://beam.ai/agentic-insights/gemini-3-8-flash-ai-agents. **Secondary.**
  - The Gemini API computer-use docs now list Flash models as the supported path: https://ai.google.dev/gemini-api/docs/computer-use. \[51\] **Primary.**
- **Browser Use.** Its speed pitch is: "People want their agents to work at least as fast as humans." The optimizations are KV-cache-friendly prompt ordering (history before the fresh browser state), screenshots only when needed (about 0.8 s saved each), DOM text extraction and 10–15-token actions. The claim is "6x speed."\[10\] Source: https://browser-use.com/posts/speed-matters. **Vendor-marketing claim with some internal measurements.**
- **Anthropic prompt caching** (a latency and cost lever for agent loops). Opus 5.5 cache reads are $0.20 per million tokens, which Anthropic says "account for the majority of agentic and coding work costs."\[52\] Reported by Unite.AI, https://www.unite.ai/anthropic-releases-claude-opus-5-5-with-lower-pricing-and-new-safeguards/. **Secondary report of a vendor statement.**
- **Missing.** I did not retrieve primary Groq, Cerebras or SambaNova agent-speed claims, Browserbase speed claims, or speculative-decoding claims tied specifically to agents.

---

## Top 5 numbers for a senior ML professor

1. **87–97% of computer-use agent wall-clock time is LLM planning, judging or reflection; screenshots plus action execution are under 3.5%** (OSWorld-Human Table 1, MLSys 2026). This is a measured, component-level profile of open agents. It locates the bottleneck squarely in model inference, not in the environment.
2. **Each later step takes up to 3× longer than early steps, because each prompt re-sends all prior screenshots and latency is prefill-bound** (OSWorld-Human). It names a mechanism a systems researcher recognizes (quadratic context growth), which predicts that longer, more realistic tasks get disproportionately slower.
3. **12 minutes for an agent vs under 30 seconds for a novice human to double-space two paragraphs** (OSWorld-Human). A concrete, falsifiable 24× gap on a trivial task is more persuasive than aggregate scores. The professor should know the human side is an estimate, not a timed trial.
4. **On OSWorld 2.0, going from 13.0% to 20.6% completion costs about 6× the output tokens (37.1K → 224K per task, about $25.5 → $72.4 per task); the authors put it at "roughly 25 to 30K extra tokens for each additional point"** (XLANG Lab, 2026, Table 3). It is a direct, author-stated cost-accuracy curve on human-scale (1.6-hour median) tasks, and the best agent still fails four of five.
5. **A 2-point accuracy gain cost 9× more on HAL's Online Mind2Web ($1,577 vs $171 per 300-task run); Opus 4.1 was skipped because it would have cost about $20,000** (HAL, ICLR 2026).\[16\] It comes from an independent, standardized third-party harness, not a vendor, and shows the cost-accuracy frontier is steep enough that researchers themselves cannot afford to evaluate frontier agents.

---

## Caveats

- **Where the evidence is thin or contradictory.**
  - Survey evidence that latency *blocks* adoption is mixed. LangChain says latency is the #2 challenge (20%), while MAP finds only 14.8% of deployed teams call it a hard blocker, and LangChain reports cost concern *falling*.\[36\] Make the claim "too slow for interactive or real-time work," not "too slow to deploy at all."
  - OSWorld-Human's step-overhead factor changed between versions (1.4–2.7× vs 2.7–4.3×). Its $2.43-per-task figure conflicts with its own token table (about $7.9 per task).
- **Human baselines are uneven.** The OSWorld-Human "<30 s" figure is an estimate, while OSWorld 2.0 times are annotator-timed. No benchmark I found reports agent and human wall-clock side by side on identical tasks.
- **Vendor and marketing numbers.** Browser Use timings and cost per solved task, Google's "lowest latency" and "4× faster" claims, Anthropic's and OpenAI's "2.5×," and all NVIDIA token multipliers are vendor claims. Google's 3.2-quadrillion figure is self-reported and unaudited.
- **Model generations move fast.** Most measured latency studies use 2025 models (GPT-4.1, o3, Claude 3.7/4). Today's Flash-class models and fast tiers may shrink absolute times, but none of the sources shows the structural issues (prefill-bound, history-accumulating, step-inefficient loops) have gone away.
- **Not found despite searching:** WebArena and WorkArena wall-clock timings; first-party agentic token-share data from OpenAI, Anthropic or Microsoft; analyst token-share reports (Morgan Stanley, Goldman Sachs, SemiAnalysis, Epoch AI); consulting-firm latency-blocker percentages; HCI wait-tolerance studies for computer-use agents.

## Sources

1. <https://arxiv.org/html/2506.16042>
2. [Paper page - OSWorld-Human: Benchmarking the Efficiency of Computer-Use Agents](https://huggingface.co/papers/2506.16042)
3. [2026-07-15 OSWORLD 2.0: Benchmarking Computer Use Agents on](https://arxiv.org/pdf/2606.29537)
4. [OSWorld 2.0: Benchmarking computer-use agents on long-horizon real-world tasks](https://osworld-v2.xlang.ai/)
5. [OSWorld 2.0: Benchmarking Computer Use Agents on Long-Horizon Real-World Tasks](https://arxiv.org/html/2606.29537v1)
6. [TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks](https://arxiv.org/html/2412.14161v2)
7. [TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks — Lacuna](https://lacuna.tiptreesystems.com/work/theagentcompany-benchmarking-llm-agents-on-consequential-real-world-tasks/wrk_814d2c2e6328efdeadc045634ca14371)
8. [TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks](https://papers.nips.cc/paper_files/paper/2025/file/0d744742f6fac4d1134c019b7cef3c8a-Paper-Datasets_and_Benchmarks_Track.pdf)
9. [The Battle of AI Agents: Comparing Real World Performance Using Benchmarking | by Cobus Greyling | Medium](https://cobusgreyling.medium.com/the-battle-of-ai-agents-comparing-real-world-performance-using-benchmarking-356a8c6e0fcc)
10. [Speed Matters: How Browser Use Achieves the Fastest Agent Execution](https://browser-use.com/posts/speed-matters)
11. [My Honest Review of ChatGPT Agent - by Frank Andrade](https://artificialcorner.com/p/my-honest-review-of-chatgpt-agent)
12. [Introducing the Gemini 2.5 Computer Use model](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-computer-use-model/)
13. [Is Gemini 2.5 Computer Use Model the Future of AI-Driven Interface Control?](https://apidog.com/blog/gemini-2-5-computer-use-model/)
14. [Google's AI can now surf the web for you, click on buttons, and fill out forms with Gemini 2.5 Computer Use | VentureBeat](https://venturebeat.com/ai/googles-ai-can-now-surf-the-web-for-you-click-on-buttons-and-fill-out-forms)
15. [HAL: Online Mind2Web Leaderboard](https://hal.cs.princeton.edu/online_mind2web)
16. <https://arxiv.org/pdf/2510.11977>
17. [Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation](https://arxiv.org/html/2510.11977v1)
18. [HAL: AssistantBench Leaderboard](https://hal.cs.princeton.edu/assistantbench)
19. [Browser Agent Benchmark: Comparing LLM Models for Web Automation](https://browser-use.com/posts/ai-browser-agent-benchmark)
20. [Web Agent Benchmarks - Browser Use](https://browser-use.com/benchmarks/agents)
21. [State of AI: An Empirical 100 Trillion Token Study with OpenRouter | Andreessen Horowitz](https://a16z.com/state-of-ai/)
22. [State of AI:An Empirical 100 Trillion Token Study with OpenRouter](https://arxiv.org/html/2601.10088v1)
23. [Google I/O 2026: Sundar Pichai’s opening keynote](https://blog.google/innovation-and-ai/sundar-pichai-io-2026/)
24. [Google's 3.2Q Token Shock: Inference Demand Goes Vertical | TECHi](https://www.techi.com/google-3-2q-tokens-inference-demand/)
25. [Nvidia CEO Huang says AI has to do '100 times more' computation now than when ChatGPT was released](https://www.nbcnews.com/business/business-news/nvidia-ceo-huang-says-ai-100-computation-now-chatgpt-was-released-rcna194081)
26. [NVIDIA’s Jensen Huang on Compute as a New Economic Engine | Morgan Stanley](https://www.morganstanley.com/insights/articles/nvidia-jensen-huang-compute-new-economic-engine-tmt-2026)
27. [Jensen Huang on why 'agentic' will rewire a \$50 trillion economy: 'operated by robots, managed by more robots, and the entire factory is a robot' | Fortune](https://fortune.com/2026/05/06/jensen-huang-servicenow-bill-mcdermott-agentic-ai-robos/)
28. [Jensen Huang Says Agentic AI Requires 1,000x More Compute Than Generative AI. Here's What That Means. — Glitchwire](https://glitchwire.com/news/jensen-huang-says-agentic-ai-requires-1000x-more-compute-than-generative-ai-here/)
29. [The Token Economy Is Here: How Jensen Huang Is Rewriting the Rules of Work | by BIGEYEs | Medium](https://medium.com/@silverag79/the-token-economy-is-here-how-jensen-huang-is-rewriting-the-rules-of-work-83700ddd6e39)
30. [2025: The State of Generative AI in the Enterprise | Menlo Ventures](https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise/)
31. [TheValueist on X: "\$NVDA Menlo Ventures’ “State of Generative AI in the Enterprise 2025” describes a rapidly scaling but unevenly monetized market. Enterprise generative AI software spend is estimated at \$37B in 2025, up from \$11.5B in 2024 and \$1.7B in 2023, a 3.2x year-on-year increase and more" / X](https://x.com/TheValueist/status/1998461015093293366)
32. [Menlo: Enterprise AI Spend Hits \$37 Billion · SemanticOS](https://semanticos.io/blog/menlo-state-of-genai-enterprise-spend)
33. [State of Agent Engineering](https://www.langchain.com/state-of-agent-engineering)
34. [Your Agent Has Observability. It Doesn't Have Evals. - DEV Community](https://dev.to/jasonl888/your-agent-has-observability-it-doesnt-have-evals-3ce5)
35. [The State of Agent Engineering Report Overview - KDnuggets](https://www.kdnuggets.com/the-state-of-agent-engineering-report-overview)
36. [Measuring Agents in Production](https://arxiv.org/pdf/2512.04123)
37. [Gartner Predicts Over 40% of Agentic AI Projects Will Be Canceled by End of 2027](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027)
38. [Why Agentic AI Projects Get Canceled (and How to Ship)](https://www.digitalapplied.com/blog/agentic-ai-project-cancellations-gartner-40-percent-2026)
39. [The LangChain Report Proves Quality, Not Cost, Is Killing AI Agents in Production | NoCode.Tech](https://www.nocode.tech/article/langchain-report-quality-not-cost-killing-ai-agents)
40. [Fast mode (research preview) - Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/fast-mode)
41. [Claude Opus 5.5: Anthropic's Cheaper, Faster New Flagship | DataCamp](https://www.datacamp.com/blog/opus-5-5)
42. [Claude Opus \\ Anthropic](https://www.anthropic.com/claude/opus)
43. [Anthropic Debuts Claude Opus 5.5, Undercutting Flagship Pricing by 40% — BigGo Finance](https://finance.biggo.com/news/56cae245-3e0c-4db9-ba3f-14e938d16b15)
44. [Fast mode for API Customers | OpenAI](https://openai.com/api-priority-processing/)
45. [Fast mode | OpenAI API](https://developers.openai.com/api/docs/guides/priority-processing)
46. [Flex processing | OpenAI API](https://developers.openai.com/api/docs/guides/flex-processing)
47. [Enable priority processing for Microsoft Foundry Models - Microsoft Foundry | Microsoft Learn](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/priority-processing)
48. [Introducing computer use in Gemini 3.5 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-computer-use-gemini-3-5-flash/)
49. [Gemini 3.5 Flash Computer Use: Agentic Automation 2026](https://www.digitalapplied.com/blog/gemini-3-5-flash-computer-use-agent-automation-2026)
50. [Gemini 3.8 Flash for AI Agents: Early Benchmarks (2026)](https://beam.ai/agentic-insights/gemini-3-8-flash-ai-agents)
51. [Computer use | Gemini API | Google AI for Developers](https://ai.google.dev/gemini-api/docs/computer-use)
52. [Anthropic Releases Claude Opus 5.5 With Lower Pricing and New Safeguards – Unite.AI](https://www.unite.ai/anthropic-releases-claude-opus-5-5-with-lower-pricing-and-new-safeguards/)
