# Environment Costs of LLM Computer-Use and Web Agents

Research snapshot: **September 27, 2026 (America/New_York)**  
Currency: **USD**  
Scope: sandbox VMs, containers, cloud browsers, and benchmark environment hosting, distinguished from model API expenditure.

This document exports the preceding research response. Source citations are ordinary Markdown links so that they remain usable outside ChatGPT. “Not found” means not found in the sources examined; it is not proof that no disclosure exists anywhere.

## 1. Evidence table

Each row identifies one source. Dates are publication/version dates when available; otherwise the access date is stated. Vendor prices are retail charges, not evidence of vendors’ underlying infrastructure costs. Calculated figures are explicitly marked.

| ID / source | Figure / finding | Exact definition and inclusions | Exact URL | Date | Primary / secondary |
|---|---|---|---|---|---|
| S01 — OSWorld paper | **No separate environment dollar cost found.** | Describes VM creation, snapshots, task initialization and parallel execution. Infrastructure description is not a per-task hosting bill. See §2.2 and Appendix A.1. | <https://arxiv.org/html/2404.07972v2> | 2024-05-30, v2 | Primary—paper |
| S02 — OSWorld-Verified announcement | **No environment dollar cost found.** | Reports migration to AWS and increased evaluation parallelism; does not attach a VM cost per task or per evaluation run. | <https://xlang.ai/blog/osworld-verified> | 2025-07-28 | Primary—benchmark authors |
| S03 — OSWorld AWS infrastructure guide | Controller: `t3.medium` for fewer than **5** environments; `t3.large` for fewer than **15**. Proxy: approximately **$1/GB**. | Controller instance is **additional to the client VMs** where tasks run. Proxy figure is traffic pricing, not VM compute or cost/task. No complete infrastructure bill provided. | <https://timothyxxx.github.io/OSWorld/user_guides/run_public_evaluation.html> | Undated; accessed 2026-09-27 | Primary—project docs; quoted third-party proxy price |
| S04 — OSWorld 2.0 paper | **≈$72.4/task** for batched Claude Opus 4.8; default environment instance `t3.2xlarge`. **No separate VM cost found.** | Table 3 reports average cost/task. Infrastructure notes specify AWS `us-east-1`, larger instances when needed, residential proxies, and model-based evaluation/user simulation. These components are not separately priced in the results. | <https://arxiv.org/html/2606.29537v1> | 2026-06-28, v1 | Primary—paper |
| S05 — HAL paper | Approximately **$40,000 across 21,730 rollouts**. | Aggregate evaluation expenditure described as compute cost. Describes Azure VM orchestration but does **not provide an environment-versus-API dollar breakdown per task**. Do not interpret the aggregate as a VM bill. | <https://arxiv.org/html/2510.11977v1> | 2025-10-13 | Primary—paper |
| S06 — HAL leaderboard cost definition | “Cost” means **total API cost across all tasks**. | Leaderboard tooltip explicitly defines the metric as API expenditure; it is not an environment-compute metric. | <https://hal.cs.princeton.edu/online_mind2web> | Undated; accessed 2026-09-27 | Primary—official leaderboard |
| S07 — AgentSysBench | **Yes: estimated per-request cost decomposition.** Sandbox charges exceed **99%** for Pi-AutoR. | §4.5/Figure 8 separates LLM APIs, sandbox execution and other components using public-cloud prices, including E2B and Firecrawl. The cited percentage concerns **GPU-accelerated scientific-simulation containers**, not ordinary browser sessions. Figure 8 reports percentage shares rather than a tabulated pair of absolute environment/API dollars per task. | <https://arxiv.org/html/2608.15127v1#S4.SS5> | 2026-08-15 | Primary—paper; authors’ pricing estimate |
| S08 — TheAgentCompany paper | **No environment compute dollars in its cost metric.** | §4.1 defines cost/instance as input and output token charges for querying LLM APIs, assuming no prompt caching. | <https://arxiv.org/html/2412.14161v3> | 2025-09-10, v3 | Primary—paper |
| S09 — TheAgentCompany setup docs | Baseline infrastructure: **EC2 `t3.2xlarge`**; **30+ GB** free disk. | Hosts the simulated company’s services; task execution also uses Docker images. No measured infrastructure cost/task or allocation across concurrent tasks is supplied. | <https://github.com/TheAgentCompany/TheAgentCompany> | Living docs; accessed 2026-09-27 | Primary—project docs |
| S10 — WebArena hosting docs | Recommended website host: **`t3a.xlarge` + 1,000 GB EBS**. Optional self-hosted map backend: another **`t3a.xlarge` + 1,000 GB**. | These are **website/backend hosting resources**, not merely the agent’s browser. Docs provide deployment requirements, not a dollar cost/task. | <https://github.com/web-arena-x/webarena/blob/main/environment_docker/README.md> | Living docs; accessed 2026-09-27 | Primary—project docs |
| S11 — Browserbase pricing | Developer: **$20/month**, includes **100 browser-hours**, then **$0.12/hour**. Startup: **$99/month**, includes **500 hours**, then **$0.10/hour**. | Proxy allowances are **1/5 GB**, then **$12/$10 per GB**, respectively. Hourly rates are **overage rates**, not subscription-inclusive average costs. Runtime is included; model usage is separately priced. | <https://www.browserbase.com/pricing> | Accessed 2026-09-27 | Primary—vendor pricing |
| S12 — Browserbase billing definitions | Browser time billed by minute, with a **one-minute minimum**; proxy bandwidth billed by MB, with a **one-MB minimum per session**. | Monthly browser/proxy allocations are followed by overage charges. Hosted Functions are included. | <https://docs.browserbase.com/account/billing/plans> | Accessed 2026-09-27 | Primary—vendor docs |
| S13 — Browser Use Cloud | **$0.02/browser-hour**; residential traffic **$5/GB**, or direct/own-proxy traffic **$0.20/GB**. | Browser infrastructure for your own agent; no subscription, **$5 minimum top-up**. Time rounds up to whole minutes. Proxies enabled by default. Managed agents additionally charge model cost plus a **20% service fee**; that fee is not browser rent. | <https://browser-use.com/pricing> | Accessed 2026-09-27 | Primary—vendor pricing |
| S14 — E2B | **$0.000014/vCPU-second + $0.0000045/GiB-second**. Default **2 vCPU + 4 GiB = $0.1656/hour**, **own calculation**. | Running sandbox resources, billed per second. Hobby has no subscription fee and includes **10 GiB storage**; Pro costs **$150/month plus usage**, with **20 GiB storage** included. Model API charges are separate. | <https://e2b.dev/pricing> | Accessed 2026-09-27 | Primary—vendor pricing; derived hourly total |
| S15 — Daytona pricing | **$0.0504/vCPU-hour + $0.0162/GiB-hour**; disk **$0.000108/GiB-hour** after first **5 GiB**. | Resource charges, calculated per second. **2 vCPU + 4 GiB = $0.1656/hour before chargeable disk**, own calculation. Windows adds **$0.0858/vCPU-hour**. | <https://www.daytona.io/pricing> | Accessed 2026-09-27 | Primary—vendor pricing; derived total |
| S16 — Daytona lifecycle billing | Running: CPU + RAM + disk. Stopped/paused: **disk only**. | Charges depend on reserved resources and lifecycle state. Transition states remain fully billed; paused VM memory state is not separately billed. Relevant when an agent waits for model responses or human input. | <https://www.daytona.io/docs/en/billing/> | Accessed 2026-09-27 | Primary—vendor docs |
| S17 — Modal pricing | **$0.00003942/physical-core-second + $0.00000667/GiB-second**. A physical core equals **2 vCPUs**. | Sandbox/notebook CPU and memory rates. **2 vCPU + 4 GiB = $0.23796/hour**, own calculation, before applicable additional charges. This uses Modal’s sandbox rate, not an assumed per-vCPU rate. | <https://modal.com/pricing> | Accessed 2026-09-27 | Primary—vendor pricing; derived total |
| S18 — Modal metering docs | Billed per second on **max(requested resources, actual usage)**. | Reserving CPU/RAM creates a billing floor; bursting can increase charges. “Pay for use” does not mean an idle but reserved sandbox is automatically free. | <https://modal.com/docs/guide/sandbox-resources> | Accessed 2026-09-27 | Primary—vendor docs |
| S19 — Anthropic computer-use reference container | **No hosted environment tariff stated.** | A Docker reference environment with a Linux desktop, display server, applications and tool implementations. Your application executes tool calls in infrastructure you control. Hosting cost depends on where you run it; the Claude API bill is separate. | <https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool> | Accessed 2026-09-27 | Primary—vendor docs |
| S20 — AWS EC2 | Official T3 page lists **t3.medium: $0.0418/hour, 2 vCPU/4 GiB**; **t3.xlarge: $0.1670/hour, 4 vCPU/16 GiB**. | Linux/Unix On-Demand, **US East/N. Virginia**, instance compute. A self-configured desktop host; storage, networking and desktop setup are not an all-inclusive service. Burstable T3 Unlimited can add CPU-credit charges. See discrepancy note under S26. | <https://aws.amazon.com/ec2/instance-types/t3/> | Accessed 2026-09-27 | Primary—vendor pricing |
| S21 — GCP Compute Engine | **e2-standard-2: $0.06701142/hour, 2 vCPU/8 GiB**; **e2-standard-4: $0.13402284/hour, 4 vCPU/16 GiB**. | On-demand machine prices in the published **Iowa/us-central1** table. Base VM compute; disks, networking and premium OS licences are additional. Compute Engine rates, not Cloud Workstations prices. Retrieved from the indexed official pricing table; direct page retrieval failed. | <https://cloud.google.com/products/compute/pricing/general-purpose> | Accessed 2026-09-27 | Primary—vendor pricing, search-index retrieval |
| S22 — OpenAI Operator | Own browser confirmed; **per-session environment cost/price: not stated**. | Announcement describes a browser the agent controls. Exact VM/container allocation, resource size and per-user versus per-session lifecycle are **not stated** there. | <https://openai.com/index/introducing-operator/> | 2025-01-23 | Primary—vendor announcement |
| S23 — OpenAI ChatGPT agent | Own virtual computer confirmed; **per-session environment cost/price: not stated**. | Includes visual/text browsers and a terminal sharing task context. Exact infrastructure allocation, hardware size and persistent-per-user versus per-task provisioning are **not stated** in the announcement. | <https://openai.com/index/introducing-chatgpt-agent/> | 2025-07-17 | Primary—vendor announcement |
| S24 — Anthropic Claude in Chrome | User-browser extension; **dedicated cloud browser/VM allocation: not stated**. | Controls the user’s Chrome. Current docs also describe cloud Cowork sessions, but do not specify a dedicated VM allocation for Chrome use. Available through paid plans; no separate environment price/session stated. | <https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome> | 2026-08-26 | Primary—vendor docs |
| S25 — Meta Muse | **Dedicated cloud VM with its own browser explicitly stated**; **per-session environment cost/price: not stated**. | Meta describes a person’s agent and data residing in its own isolated cloud computer. Announcement offers free use plus subscription options without assigning a dollar amount to VM runtime. Architecture/security statements are **vendor claims**, not an independent infrastructure audit. | <https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/> | 2026-09-08 | Primary—vendor announcement |
| S26 — AWS pricing discrepancy | Official guidance lists **$0.0416/hour** for `t3.medium`, versus **$0.0418/hour** on the T3 product page. | This is an unresolved disagreement between official pages. S20 uses the T3 product page as retrieved. Neither AWS figure is used in the task-cost calculations below. | <https://docs.aws.amazon.com/prescriptive-guidance/latest/optimize-costs-microsoft-workloads/right-size-selection.html> | Accessed 2026-09-27 | Primary—vendor guidance |

Access dates identify the pricing snapshot, not a guarantee that a rate remained unchanged historically. Living documentation may change after this research snapshot.

## 2. Answers to the four questions

### (a) Do published benchmarks report environment compute alongside API cost?

**AgentSysBench provides the clearest affirmative evidence, with a limitation:** it estimates a component-level cost breakdown per request rather than publishing an audited cloud bill or a table of absolute environment/API dollar pairs. Its extreme sandbox-cost example is a GPU scientific workload; it does not establish that ordinary web or desktop environments generally dominate frontier-model API bills. [S07](https://arxiv.org/html/2608.15127v1#S4.SS5)

For **OSWorld, OSWorld-Verified, OSWorld 2.0, HAL, TheAgentCompany and WebArena hosting docs**, no separately itemized environment-compute dollar cost per task was found in the examined materials. TheAgentCompany explicitly defines its cost metric through API token charges; HAL’s leaderboard explicitly labels API expenditure. OSWorld 2.0’s cost/task column does not supply the accounting detail needed to identify an environment component. [S01](https://arxiv.org/html/2404.07972v2), [S02](https://xlang.ai/blog/osworld-verified), [S04](https://arxiv.org/html/2606.29537v1), [S05](https://arxiv.org/html/2510.11977v1), [S06](https://hal.cs.princeton.edu/online_mind2web), [S08](https://arxiv.org/html/2412.14161v3), [S10](https://github.com/web-arena-x/webarena/blob/main/environment_docker/README.md)

There is a meaningful distinction between **the agent’s desktop/browser** and **the websites used by the benchmark**. WebArena’s application servers—and TheAgentCompany’s simulated company services—are additional infrastructure whose cost must be allocated across tasks or concurrent agents. Pricing only a browser session would omit them. [S09](https://github.com/TheAgentCompany/TheAgentCompany), [S10](https://github.com/web-arena-x/webarena/blob/main/environment_docker/README.md)

### (b) What do environment services charge?

The evidence shows three purchasing models:

- **Browser rental:** browser time plus traffic, with a subscription minimum at Browserbase. [S11](https://www.browserbase.com/pricing), [S12](https://docs.browserbase.com/account/billing/plans), [S13](https://browser-use.com/pricing)
- **Managed sandbox rental:** CPU and RAM, sometimes storage and lifecycle-dependent charges. [S14](https://e2b.dev/pricing), [S15](https://www.daytona.io/pricing), [S16](https://www.daytona.io/docs/en/billing/), [S17](https://modal.com/pricing), [S18](https://modal.com/docs/guide/sandbox-resources)
- **Self-hosting:** a cloud VM plus the additional resources and software needed for the desktop or benchmark. [S19](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool), [S20](https://aws.amazon.com/ec2/instance-types/t3/), [S21](https://cloud.google.com/products/compute/pricing/general-purpose)

These are not interchangeable configurations. Browser Use’s browser-only price does not establish what a full OSWorld desktop with applications would cost. Its traffic charge is also separate. The term “cheapest” below means the cheapest quoted paid browser-time option in this comparison, excluding promotional credits and free tiers; it is not a claim about the cheapest possible computing configuration worldwide. [S13](https://browser-use.com/pricing)

### (c) Which products explicitly allocate an environment?

**Meta Muse explicitly states a dedicated cloud VM.** ChatGPT agent confirms its own virtual computer, and Operator confirms its own browser, but the cited announcements do not disclose the precise allocation lifecycle. Claude in Chrome confirms operation in the user’s browser; cloud session support does not, by itself, establish a dedicated cloud browser or VM. **None of these sources gives a separately priced environment session or the provider’s actual environment cost/session.** [S22](https://openai.com/index/introducing-operator/), [S23](https://openai.com/index/introducing-chatgpt-agent/), [S24](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome), [S25](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)

Product allocation statements are vendor disclosures. Their safety or security characterizations are vendor claims, not independent audit findings. A subscription price or free consumer tier does not disclose the vendor’s infrastructure cost.

### (d) Own calculations: task runtime cost and ratio to the stipulated API bills

Inputs:

- **Cheapest quoted paid browser-time option:** Browser Use, **$0.02/hour**, excluding traffic. [S13](https://browser-use.com/pricing)
- **Representative managed sandbox:** E2B’s default **2 vCPU + 4 GiB**, calculated as **$0.1656/hour**. “Representative” means its documented default configuration, not a measured market median. [S14](https://e2b.dev/pricing)
- **API comparison bills:** **$7.87/task** and **$72.40/task**, supplied by the user as calculation assumptions. This comparison does not independently establish that the OSWorld 2.0 reported figure is an audited exclusively-model bill.
- **Durations:** **15 minutes** and **1 hour**, as requested.

Formulas:

```text
Environment runtime cost = hourly rate × allocated hours
Ratio = environment runtime cost / API bill
Percentage = ratio × 100

E2B hourly rate
  = (2 × $0.000014 + 4 × $0.0000045) × 3,600
  = $0.1656/hour
```

| Option | Task duration | Environment runtime cost — own calculation | Environment / $7.87 API bill | Environment / $72.40 API bill |
|---|---:|---:|---:|---:|
| Browser Use | 15 minutes | **$0.0050** | **0.000635× = 0.0635%** | **0.0000691× = 0.00691%** |
| Browser Use | 1 hour | **$0.0200** | **0.002541× = 0.2541%** | **0.000276× = 0.0276%** |
| E2B default sandbox | 15 minutes | **$0.0414** | **0.005260× = 0.5260%** | **0.000572× = 0.0572%** |
| E2B default sandbox | 1 hour | **$0.1656** | **0.021042× = 2.1042%** | **0.002287× = 0.2287%** |

These are **own calculations**, not measured benchmark bills. They assume one environment continuously allocated for the stated duration, with no additional startup/idle time, retries, free credits or subscription allocation. They exclude separately hosted benchmark application servers.

For Browser Use, the actual environment-service bill also includes traffic:

```text
Direct / own proxy:
  C = $0.02 × t + $0.20 × B

Residential proxy:
  C = $0.02 × t + $5.00 × B

t = billed browser hours, subject to whole-minute rounding
B = billed GB
```

An external proxy provider may charge separately when using your own proxy. Thus the browser-time figures are **runtime components, not complete session invoices**. [S13](https://browser-use.com/pricing)

Other hourly conversions shown in the evidence table are also own calculations:

```text
Daytona, 2 vCPU + 4 GiB:
  2 × $0.0504 + 4 × $0.0162 = $0.1656/hour
  (before chargeable disk and any Windows charge)

Modal, 1 physical core = 2 vCPU, plus 4 GiB:
  ($0.00003942 + 4 × $0.00000667) × 3,600
  = $0.23796/hour
  (before applicable additional charges; actual metering can exceed reservations)
```

Sources: [Daytona pricing](https://www.daytona.io/pricing), [Modal pricing](https://modal.com/pricing), [Modal metering](https://modal.com/docs/guide/sandbox-resources).

## 3. What could not be found or fully verified

- A separately itemized environment-compute **$/task** for the requested benchmarks other than AgentSysBench’s estimated component shares.
- Absolute environment/API dollar pairs for AgentSysBench’s web and GUI workloads that could be quoted without estimating values from a figure.
- A disclosed actual VM/browser **cost/session**, or a separate environment **price/session**, for ChatGPT agent, Operator, Claude in Chrome or Muse.
- Exact VM specifications and allocation lifecycles for ChatGPT agent/Operator; dedicated cloud VM allocation details for Claude in Chrome.
- A complete benchmark environment cost including controllers, application servers, storage, proxies, initialization, idle capacity and failed runs.
- Direct retrieval of GCP’s full general-purpose pricing page; the quoted rates were available in the search index of the **official page**. [S21](https://cloud.google.com/products/compute/pricing/general-purpose)
- Reconciliation of the AWS pricing discrepancy: official guidance shows **$0.0416/hour** for `t3.medium`, while its T3 product page shows **$0.0418/hour**. The evidence table uses the latter. [S20](https://aws.amazon.com/ec2/instance-types/t3/), [S26](https://docs.aws.amazon.com/prescriptive-guidance/latest/optimize-costs-microsoft-workloads/right-size-selection.html)

These gaps should not be replaced by inferred VM prices attributed to benchmark authors or product vendors. Calculating runtime × a public infrastructure rate is a separate estimate and should be labeled accordingly.
