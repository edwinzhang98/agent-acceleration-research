# **The Economics of Agentic Environments: Disentangling Compute from Inference in AI Workloads**

The transition from single-turn conversational artificial intelligence to autonomous, long-running agentic workflows has introduced a fundamental architectural shift in the underlying unit of computing. Traditional large language model serving treats a stateless token-generation request as the primary unit of work and the dominant cost center. However, as autonomous agents interact with web browsers, terminal interfaces, code interpreters, and file systems, a secondary, parallel infrastructure is required: the agent execution environment. This encompasses the virtual machines, containers, sandboxes, and cloud browsers in which the agent physically operates, executes code, and observes state changes.  
The following analysis investigates the specific costs associated with the environment side of computer-use and web agents. It strictly isolates the cost of sandbox virtual machines, software containers, and cloud browsers from the mathematical model API billing. The report addresses critical questions regarding benchmark transparency, commercial service pricing, consumer product architecture, and the ratio between infrastructure and inference in modern agent deployments.

## **Foundational Cost Data and Source Index**

The table below compiles the specific figures, exact definitions, and origins of the primary and secondary pricing data analyzed throughout this report, fulfilling the requirement for a consolidated source index.

| Figure | Exact Definition (Per Task / Per Hour / Per Session / Included Elements) | URL | Date | Primary or Secondary |
| :---- | :---- | :---- | :---- | :---- |
| \~\$8.00 | Total VM infrastructure cost for all machines running in parallel for the duration of an OSWorld benchmark evaluation; excludes API costs. | https://openreview.net/forum?id=t9JUTS9ADL | N/A | Primary |
| \<\$100.00 | Total cloud computing cost to generate the WebArena environment within a ten-hour setup pipeline. | https://webarena.dev/webarena-infinity/ | N/A | Primary |
| \$20.00 | Browserbase Developer Plan base price per month; includes 100 browser hours and 1 GB of proxy bandwidth. | https://docs.browserbase.com/account/billing/plans | N/A | Primary |
| \$0.12 | Browserbase Developer Plan overage rate per browser hour. | https://docs.browserbase.com/account/billing/plans | N/A | Primary |
| \$99.00 | Browserbase Startup Plan base price per month; includes 500 browser hours and 5 GB of proxy bandwidth. | https://docs.browserbase.com/account/billing/plans | N/A | Primary |
| \$0.02 | Browser Use Cloud execution cost per browser hour; utilizes Firecracker microVMs. | https://browser-use.com/posts/firecracker-browser-infra | N/A | Primary |
| \$0.000028 | E2B computing rate per second for a 2 vCPU allocation. | https://github.com/ghuntley/how-to-ralph-wiggum/blob/main/references/sandbox-environments.md | N/A | Secondary |
| \$0.000018 | E2B computing rate per second for a 4 GiB of RAM allocation. | https://tokencost.app/blog/openai-agents-api-hosted-sandbox-pricing | N/A | Secondary |
| \$0.0504 | Daytona compute rate per vCPU-hour. | https://www.daytona.io/pricing | N/A | Primary |
| \$0.0162 | Daytona memory rate per GiB-hour. | https://www.daytona.io/pricing | N/A | Primary |
| \$0.00003942 | Modal sandbox computing rate per physical core (equivalent to 2 vCPUs) per second. | https://modal.com/products/notebooks | N/A | Primary |
| \$0.00000667 | Modal sandbox memory rate per GiB per second. | https://modal.com/products/notebooks | N/A | Primary |
| \$0.00 | Anthropic Computer Use Reference Container software cost; user must provide their own underlying compute infrastructure. | https://github.com/anthropics/anthropic-quickstarts/pkgs/container/anthropic-quickstarts | N/A | Primary |
| \$0.0416 | AWS EC2 Linux On-Demand rate per hour for t3.medium (2 vCPU, 4 GiB RAM) in the us-east-1 region. | https://calculator.holori.com/aws | N/A | Secondary |
| \$0.0832 | AWS EC2 Linux On-Demand rate per hour for t3.large (2 vCPU, 8 GiB RAM) in the us-east-1 region. | https://www.doit.com/compute/compute/aws/us-east-2/t3.large | N/A | Secondary |
| \$0.0670 | GCP Compute Engine On-Demand rate per hour for e2-standard-2 (2 vCPU, 8 GiB RAM). | https://cloudprice.app/providers/gcp | N/A | Secondary |
| \$0.1344 | GCP Compute Engine On-Demand rate per hour for e2-standard-4 (4 vCPU, 16 GiB RAM). | https://www.finout.io/blog/google-cloud-pricing | N/A | Secondary |
| \$0.12 | OpenAI Agents API hosted sandbox rate per 20-minute session for a 4 GB container. | https://developers.openai.com/api/docs/pricing | N/A | Primary |
| \$200.00 | OpenAI Operator consumer agent subscription price per month. | https://coasty.ai/blog/computer-use-agent-pricing-comparison-2026-20260519 | May 19, 2026 | Secondary |

## **The Benchmark Blind Spot: Environment Compute Versus API Inference**

As autonomous systems migrate from theoretical research to practical application, the measurement of agent efficacy relies heavily on standardized capability benchmarks. However, a systemic blind spot exists within the academic and commercial evaluation ecosystems: the obfuscation of the execution environment's compute cost. The critical question is whether any published agent benchmarks or academic papers report the environment compute cost directly next to the API cost per task.  
An exhaustive analysis of the infrastructure notes from the industry's leading evaluation frameworks reveals that they overwhelmingly fail to report the per-task environment computing cost alongside the model API bill. The underlying infrastructure costs are often treated as invisible overhead, while the token costs take center stage.

### **OSWorld, OSWorld-Verified, and OSWorld 2.0**

The OSWorld suite represents a flagship benchmark for computer-use artificial intelligence, focusing on open-ended tasks in real computer environments spanning Ubuntu, Windows, and macOS1. The fundamental architecture of OSWorld relies on executing tasks within a virtual machine. The virtual machine provides an isolated, safe environment that allows agents to interact with graphical user interfaces via mouse and keyboard commands, preventing irreversible damage to the host machine2. The benchmark evaluates success by utilizing a custom script to inspect the final state of the virtual machine1.  
Despite this heavy reliance on virtualization, the exact environment compute cost per task is not reported next to the API token cost. The authors of the OSWorld extension for Windows note that their open-sourced repository provides a bulk cost estimate for the infrastructure, stating that the virtual machine cost is roughly \$8.00 for all machines running in parallel for the duration of the entire evaluation4. This bulk figure is presented collectively alongside model costs ranging from \$0 to \$100 depending on the language model selected4.  
In OSWorld 2.0, cost-aware evaluations explicitly highlight the token cost, reporting that the agent "Sai" achieved a 73.0% partial score at \$15.70 per task, outperforming Claude Opus 5 at \$23.70 per task and GPT-5.6 Sol at \$26.62 per task5. However, these reported figures represent only the API inference expense5. Furthermore, leaderboards for OSWorld 2.0 and OSWorld-Verified universally display the "Est. Cost" or "Cost per 1M tokens" (such as reporting \$1.88K for GPT-5.5) without appending or separating the virtual machine hosting cost required to conduct the evaluation6. The OSWorld benchmarks do not report the environment compute cost next to the API cost per task.

### **The Holistic Agent Leaderboard (HAL)**

Princeton University's Holistic Agent Leaderboard (HAL) was specifically designed to be a standardized, cost-aware, third-party leaderboard that evaluates agents across three orthogonal axes: models, scaffolds, and benchmarks8. The infrastructure behind HAL provisions Azure virtual machines to automate large-scale agent rollouts, migrating evaluation from manual execution to a cloud-orchestrated process8.  
Despite its emphasis on cost-controlled evaluations, HAL focuses predominantly on the token cost incurred by the language model. The framework utilizes W\&B Weave for detailed cost tracking of token usage with minimal edits to the agent code11. The project validated its infrastructure via 21,730 agent rollouts over nine models and nine benchmarks at an aggregate compute cost of approximately \$40,0008. Nevertheless, the published leaderboard metrics present single dollar amounts for agent performance (for instance, o3 Medium at \$15.15 and Claude Opus 4.5 at \$87.16) representing the model cost9. There is no explicit column or data point in the primary leaderboards that delineates the Azure virtual machine environment compute cost per task next to the API cost.

### **AgentSysBench**

AgentSysBench directly critiques the paradigm of treating model inference as the sole cost center, pointing out that agentic workflows are long-running and stateful13. The paper conducts extensive profiling of the serving stack, noting that sandbox working-set memory peaks at 28 GB per session and that non-LLM components dominate latency in half of the tested applications14. The authors highlight severe architectural inefficiencies, identifying an "eviction tax" where idle but live sessions lose their KV cache, accounting for 31.5% of aggregate monetary cost15.  
While AgentSysBench is unparalleled in its granular measurement of system resources, sandbox latency, and memory spikes, the published research does not provide a benchmark table that reports the exact dollar cost of the environment per task alongside the API cost. It analyzes the impact of environmental inefficiencies on monetary cost, but it stops short of providing a direct, per-task financial ledger pairing environment dollars against inference dollars13.

### **TheAgentCompany and WebArena**

WebArena evaluates agents on long-horizon tasks across self-hosted replicas of web applications, including e-commerce sites, forums, and collaborative development platforms17. The documentation for WebArena-Infinity notes that generating the environment takes ten hours at a pipeline cost of under \$10019. However, WebArena benchmark results center on success rates and step counts, omitting the per-task hosting cost of the Docker containers required to execute each run18.  
TheAgentCompany expands this concept into a simulated software company environment, providing agents with web browsers, code editors, and communication tools to mimic digital workers20. While the research discusses cost—such as the Finance Agent Benchmark noting an API cost of \$3.7861 per query for the o3 model—it similarly omits the computing cost of the underlying simulation virtual machines on a per-task basis21.  
In summary, across all examined benchmarks and papers—OSWorld, OSWorld-Verified, OSWorld 2.0, HAL, AgentSysBench, TheAgentCompany, and WebArena—no published source reports the environment compute cost directly next to the API cost per task.

## **The Market Landscape: Sandbox and Cloud-Browser Services**

To understand the actual financial weight of the execution environment, one must examine the pricing models of the infrastructure providers that host these agents. The landscape is divided into managed cloud browsers, isolated code sandboxes, and pure Infrastructure-as-a-Service virtual machines. The pricing structures reveal deep variations in isolation architecture, cold-start latency, and active versus idle billing.

### **Managed Cloud Browsers**

Agents interacting with the open web require headless browsers that can handle authentication, dynamic rendering, and CAPTCHA evasion, often demanding sophisticated anti-detect mechanisms to prevent the target website from blocking the automated traffic.  
Browserbase provides managed cloud browsers specifically built for artificial intelligence agents. The platform operates on a tiered subscription model combined with usage overages23. The Free Plan costs \$0 per month but strictly limits sessions to a maximum of 15 minutes, with only 60 minutes of total browser operation per month and three concurrent sessions23. The Developer Plan costs \$20 per month and includes 100 browser hours and 1 GB of proxy bandwidth, with overage browser hours billed at \$0.12 per hour23. The Startup Plan scales to \$99 per month, including 500 browser hours, 5 GB of proxy bandwidth, and 100 concurrent sessions, with overages billed at \$0.10 per hour23. Browser time is metered by the minute with a one-minute minimum per session23.  
Browser Use Cloud represents an open-source framework with an accompanying managed cloud product. The platform overhauled its infrastructure to utilize Firecracker microVMs to isolate browsers, enabling sub-second cold starts while maintaining strict security boundaries27. Browser Use Cloud employs aggressive usage-based pricing, charging a flat rate of \$0.02 per browser hour27. Network traffic is billed separately at \$5.00 per GB for managed proxies or \$0.20 per GB for proxyless connections29. Cloud sessions on this platform are currently hard-limited to 15 minutes of runtime28.

### **Code Execution and Agent Sandboxes**

Agents that write code, interact with terminals, or require isolated Linux environments rely on specialized sandboxing providers. These providers optimize for rapid provisioning and secure multi-tenancy.  
E2B utilizes Firecracker microVMs to provide ephemeral, hardware-isolated sandboxes with cold starts under 200 milliseconds30. The pricing is strictly usage-based, metered by the second. The base compute rate is \$0.000014 per vCPU per second, resulting in \$0.000028 per second for the default 2 vCPU configuration32. Memory is billed separately at \$0.0000045 per GiB per second, which equates to \$0.000018 per second for a 4 GiB allocation32. Therefore, a standard 2 vCPU, 4 GiB sandbox equates to approximately \$0.1656 per hour. E2B also requires a base subscription for extended workloads: the Hobby tier at \$0 per month limits continuous runtime to 1 hour, while the Pro tier at \$150 per month extends this to 24 hours35.  
Daytona positions itself as an AI-first workspace infrastructure. Unlike the ephemeral microVMs of E2B, Daytona focuses on stateful persistence using Docker and OCI containers36. Daytona bills strictly by the second with a pay-as-you-go model. Compute is priced at \$0.0504 per vCPU-hour, and memory at \$0.0162 per GiB-hour36. A Linux sandbox with 2 vCPUs and 4 GiB of memory costs \$0.1656 per hour. If the agent requires a Windows environment, which is crucial for benchmarks like OSWorld, Daytona charges an additional operating system license fee of \$0.0858 per vCPU-hour36.  
Modal operates on a serverless architecture leveraging gVisor for user-space container isolation32. Modal's pricing methodology bills by the physical core, where one physical core is equivalent to 2 vCPUs32. The rate is \$0.00003942 per core per second, mapping to \$0.1419 per hour41. Memory is billed at \$0.00000667 per GiB per second, which equals \$0.0240 per hour41. A standard 2 vCPU, 4 GiB configuration on Modal effectively costs \$0.2379 per active hour.

### **Infrastructure-as-a-Service and Self-Hosted Containers**

For developers managing their own orchestration, base cloud computing rates establish the absolute cost floor for agent environments.  
Anthropic released a reference architecture for its computer-use capabilities via a Docker container hosted at ghcr.io/anthropics/anthropic-quickstarts:computer-use-demo-latest43. This image is entirely open-source. Anthropic does not charge a managed hosting fee for the environment; developers run it on their own hardware or cloud infrastructure, absorbing only the underlying compute costs of their chosen host43.  
Amazon Web Services (AWS) provides Elastic Compute Cloud (EC2) instances. A standard desktop-equivalent virtual machine on AWS, such as the t3.medium with 2 vCPUs and 4 GiB of RAM, is priced at \$0.0416 to \$0.0418 per hour for Linux On-Demand in the us-east-1 region46. The t3.large instance, which provides 2 vCPUs and 8 GiB of RAM, scales to \$0.0832 per hour47. If a Windows Server license is required, the t3.medium cost increases to \$0.0602 per hour49.  
Google Cloud Platform (GCP) offers Compute Engine instances. On GCP, the e2-standard-2 instance providing 2 vCPUs and 8 GiB of RAM costs \$0.0670 per hour under on-demand pricing50. The larger e2-standard-4 instance with 4 vCPUs and 16 GiB of RAM costs approximately \$0.1344 per hour52.

## **Consumer Agent Products and Internal Provisioning**

The underlying economics shift drastically when environmental infrastructure is bundled into consumer-facing software products. The architectural specifics—whether these products allocate a dedicated virtual machine, an isolated container, or a shared browser instance per user or per session—are closely guarded by the respective vendors.  
OpenAI recently introduced Operator, a research preview of an agent capable of utilizing its own browser to execute multi-step web tasks54. The product is positioned as a premium offering for Pro users and requires an aggressive \$200 per month subscription54. However, the internal infrastructure mechanisms of Operator—specifically whether it allocates a dedicated virtual machine or a dedicated cloud browser per user or per session—are not stated in the official documentation or release notes. The consumer is abstracted away from the compute footprint, trading visibility for managed execution.  
Conversely, for developers using the OpenAI Agents API, the architecture and pricing are transparent. OpenAI utilizes hosted sandboxes built on the same container infrastructure that powers the Code Interpreter56. These sandboxes are billed per 20-minute session based on memory allocation. A 1 GB container costs \$0.03, a 4 GB container costs \$0.12, a 16 GB container costs \$0.48, and a 64 GB container costs \$1.92 per session57.  
Anthropic's implementation of the Claude computer-use agent in consumer products, such as potential Chrome integrations, remains opaque. While third-party providers like Agent 37 offer persistent Claude Code hosting from \$3.99 per month for a dedicated instance58, Anthropic's own first-party consumer product internals regarding dedicated virtual machine or browser allocation per session are not stated.  
At the time of this research, no distinct consumer-facing Meta agent product offering dedicated desktop or web-browser control per session exists within the evaluated literature. While Meta's language models frequently appear in agent benchmarks21, the internal architecture of any first-party Meta agent product allocating dedicated virtual machines or browsers is not stated.

## **Calculating the True Cost: Environment-to-API Ratios**

To fully contextualize the financial weight of the execution environment, we must calculate the exact cost of hosting an agent for specific time horizons and compare it mathematically to the API inference bill. The API bills provided for this analysis are \$7.87 and \$72.40 per task. The task durations analyzed are 15 minutes (0.25 hours) and 1 hour. We utilize the cheapest managed service and a typical developer-oriented managed sandbox from the previously established market rates.  
Selection of services for calculation:

* Cheapest Option: Browser Use Cloud at a flat rate of \$0.02 per browser hour27.  
* Typical Option: E2B Sandbox with a standard footprint of 2 vCPUs and 4 GiB of RAM. The compute calculation is 2 vCPU (\$0.000028/s) plus 4 GiB (\$0.000018/s), equaling \$0.000046 per second. The hourly equivalent is \$0.000046 multiplied by 3600 seconds, resulting in \$0.1656 per hour32.

### **My own calculation: 15-Minute Task Execution**

**Environment Costs:**

* Cheapest Option (Browser Use Cloud): \$0.02 / 4 \= \$0.005  
* Typical Option (E2B): \$0.1656 / 4 \= \$0.0414

**Ratios to an API Bill of \$7.87:**

* Cheapest Option: \$0.005 / \$7.87 \= 0.000635 (The environment costs roughly 1/1,574th of the API bill).  
* Typical Option: \$0.0414 / \$7.87 \= 0.00526 (The environment costs roughly 1/190th of the API bill).

**Ratios to an API Bill of \$72.40:**

* Cheapest Option: \$0.005 / \$72.40 \= 0.000069 (The environment costs roughly 1/14,480th of the API bill).  
* Typical Option: \$0.0414 / \$72.40 \= 0.000571 (The environment costs roughly 1/1,748th of the API bill).

### **My own calculation: 1-Hour Task Execution**

**Environment Costs:**

* Cheapest Option (Browser Use Cloud): \$0.02  
* Typical Option (E2B): \$0.1656

**Ratios to an API Bill of \$7.87:**

* Cheapest Option: \$0.02 / \$7.87 \= 0.00254 (The environment costs roughly 1/393rd of the API bill).  
* Typical Option: \$0.1656 / \$7.87 \= 0.0210 (The environment costs roughly 1/47th of the API bill).

**Ratios to an API Bill of \$72.40:**

* Cheapest Option: \$0.02 / \$72.40 \= 0.000276 (The environment costs roughly 1/3,620th of the API bill).  
* Typical Option: \$0.1656 / \$72.40 \= 0.00228 (The environment costs roughly 1/437th of the API bill).

The calculations reveal a staggering economic asymmetry. In scenarios involving highly capable frontier models, which incur massive API bills due to immense context windows, visual grounding tokens, and continuous reasoning loops, the cost of the underlying compute environment is mathematically trivial. Even operating a relatively expensive managed sandbox for a full hour represents only a fraction of a percent of the API cost. However, as open-weight models become smaller and more efficient, the inference cost will inevitably compress. When inference becomes commoditized, the absolute cost floor of executing an autonomous agent will be dictated entirely by the compute, memory, and networking fees of the execution environment.

## **Information Gaps and Unstated Metrics**

Despite an exhaustive review of the provided research material, specific data points were entirely absent from the literature and market documentation. The following table identifies the critical information gaps that could not be found.

| Missing Information | Context and Relevance |
| :---- | :---- |
| Explicit Environment Cost per Task in Benchmarks | No published agent benchmark or corresponding research paper, including OSWorld, OSWorld-Verified, OSWorld 2.0, HAL, AgentSysBench, TheAgentCompany, and WebArena, contains a data table or leaderboard that explicitly reports the localized environment compute or virtual machine cost next to the API inference cost on a strict per-task basis. |
| Consumer Architecture Internals | The internal infrastructure mechanics of OpenAI's Operator, Anthropic's consumer Claude in Chrome, and Meta's agent products are strictly proprietary. It is not stated whether these commercial applications allocate a dedicated virtual machine, an isolated container, or a shared browser instance per user or per session. |
| Per-Session Consumer Infrastructure Cost | The exact per-session infrastructure cost incurred by vendors like OpenAI to operate premium consumer agents, such as Operator, is not stated, with all infrastructure pricing obscured behind flat monthly subscription tiers. |

The architecture of agentic artificial intelligence represents a fundamental departure from traditional software systems. A language model operates merely as the cognitive engine; the sandbox, virtual machine, or cloud browser serves as the physical chassis through which it interacts with the digital world. The current landscape heavily obscures the financial realities of this chassis. Academic benchmarks consistently treat cloud compute as an invisible, sunk cost, focusing exclusively on token efficiency. Meanwhile, commercial infrastructure providers have adopted hyper-granular, per-second billing models utilizing advanced micro-virtual machine isolation to minimize cold-start latency and prevent memory leakage. As the cost of intelligence approaches marginal utility, the fundamental economics of autonomous agents will ultimately be decided by the efficiency, density, and orchestration of the virtual environments they inhabit.

#### **Works cited**

> 1. OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks, [https://arxiv.org/abs/2404.07972](https://arxiv.org/abs/2404.07972)  
> 2. OSWORLD: Benchmarking Multimodal Agents for Open-Ended, [https://rhythmcao.github.io/publication/2024-osworld/2024-osworld.pdf](https://rhythmcao.github.io/publication/2024-osworld/2024-osworld.pdf)  
> 3. OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks, [https://phdfordummies.com/papers/osworld](https://phdfordummies.com/papers/osworld)  
> 4. Windows Agent Arena: Evaluating Multi-Modal OS Agents at Scale, [https://openreview.net/forum?id=t9JUTS9ADL](https://openreview.net/forum?id=t9JUTS9ADL)  
> 5. Sai tops OSWorld 2.0, beating GPT and Opus with lower costs, [https://www.simular.ai/articles/sai-tops-osworld-2-0](https://www.simular.ai/articles/sai-tops-osworld-2-0)  
> 6. OSWorld 2.0: Long-Horizon Computer-Use Benchmark | Snorkel AI, [https://snorkel.ai/leaderboard/os-world-2-0/](https://snorkel.ai/leaderboard/os-world-2-0/)  
> 7. OSWorld-Verified Leaderboard \- LLM Stats, [https://llm-stats.com/benchmarks/osworld-verified](https://llm-stats.com/benchmarks/osworld-verified)  
> 8. HAL: Holistic Agent Leaderboard Framework \- Emergent Mind, [https://www.emergentmind.com/topics/holistic-agent-leaderboard-hal](https://www.emergentmind.com/topics/holistic-agent-leaderboard-hal)  
> 9. Holistic Agent Leaderboard: HAL, [https://hal.cs.princeton.edu/](https://hal.cs.princeton.edu/)  
> 10. HOLISTIC AGENT LEADERBOARD: \- OpenReview, [https://openreview.net/pdf/883b2b5c3ac94b0fb53ec7fc88c5bea0c59653f6.pdf](https://openreview.net/pdf/883b2b5c3ac94b0fb53ec7fc88c5bea0c59653f6.pdf)  
> 11. Agent Evaluation: Holistic Agent Leaderboard (HAL) \- Sulbha Jain, [https://sulbhajain.medium.com/agent-evaluation-holistic-agent-leaderboard-hal-cc20ab62cb88](https://sulbhajain.medium.com/agent-evaluation-holistic-agent-leaderboard-hal-cc20ab62cb88)  
> 12. princeton-pli/hal-harness \- Holistic Agent Leaderboard \- GitHub, [https://github.com/princeton-pli/hal-harness](https://github.com/princeton-pli/hal-harness)  
> 13. From LLM Inference to Agentic Workloads \- arXiv, [https://arxiv.org/pdf/2608.15127](https://arxiv.org/pdf/2608.15127)  
> 14. \[2608.15127\] From LLM Inference to Agentic Workloads \- arXiv, [https://arxiv.org/abs/2608.15127](https://arxiv.org/abs/2608.15127)  
> 15. LRU is harder to beat than the KV-cache papers suggest \- GitHub, [https://github.com/gauravapiscean/agentic-kv-cache](https://github.com/gauravapiscean/agentic-kv-cache)  
> 16. From LLM Inference to Agentic Workloads: Characterization ... \- arXiv, [https://arxiv.org/html/2608.15127v1](https://arxiv.org/html/2608.15127v1)  
> 17. (PDF) WebArena: A Realistic Web Environment for Building, [https://www.researchgate.net/publication/372654539\_WebArena\_A\_Realistic\_Web\_Environment\_for\_Building\_Autonomous\_Agents](https://www.researchgate.net/publication/372654539_WebArena_A_Realistic_Web_Environment_for_Building_Autonomous_Agents)  
> 18. WebArena: A Realistic Web Environment for Building Autonomous, [https://arxiv.org/html/2307.13854v4](https://arxiv.org/html/2307.13854v4)  
> 19. WebArena-Infinity: Generating Browser Environments with Verifiable, [https://webarena.dev/webarena-infinity/](https://webarena.dev/webarena-infinity/)  
> 20. TheAgentCompany: LLM Agent Benchmarking | PDF \- Scribd, [https://www.scribd.com/document/898753976/Agent-Benchmark-Paper](https://www.scribd.com/document/898753976/Agent-Benchmark-Paper)  
> 21. Benchmarking LLMs on Real-world Financial Research Tasks \- arXiv, [https://arxiv.org/html/2508.00828v1](https://arxiv.org/html/2508.00828v1)  
> 22. Wayne Chi \- alphaXiv, [https://www.alphaxiv.org/@wayne-chi](https://www.alphaxiv.org/@wayne-chi)  
> 23. Plans \- Browserbase Documentation, [https://docs.browserbase.com/account/billing/plans](https://docs.browserbase.com/account/billing/plans)  
> 24. Browserbase Pricing: Free, \$20, \$99, or Custom, [https://www.browserbase.com/pricing](https://www.browserbase.com/pricing)  
> 25. Residential proxies for Browserbase \- DataImpulse, [https://dataimpulse.com/tutorials/residential-proxies-for-browserbase/](https://dataimpulse.com/tutorials/residential-proxies-for-browserbase/)  
> 26. The Browserbase Free Plan: Build Browser Agents for Free, [https://www.browserbase.com/blog/free-plan](https://www.browserbase.com/blog/free-plan)  
> 27. How We Made Cloud Browsers 3x Cheaper and Faster, [https://browser-use.com/posts/firecracker-browser-infra](https://browser-use.com/posts/firecracker-browser-infra)  
> 28. browser-use/CLOUD.md at main \- GitHub, [https://github.com/browser-use/browser-use/blob/main/CLOUD.md](https://github.com/browser-use/browser-use/blob/main/CLOUD.md)  
> 29. Models \- Browser-use docs, [https://docs.browser-use.com/cloud/agent/models](https://docs.browser-use.com/cloud/agent/models)  
> 30. E2b breakdown \- Dwarves Memo, [https://memo.d.foundation/breakdown/e2b](https://memo.d.foundation/breakdown/e2b)  
> 31. Best AI Agent Runtime Tools & Platforms 2026 | Orca Security, [https://orca.security/resources/blog/best-ai-agent-runtime-tools-platforms/](https://orca.security/resources/blog/best-ai-agent-runtime-tools-platforms/)  
> 32. sandbox-environments.md \- how-to-ralph-wiggum \- GitHub, [https://github.com/ghuntley/how-to-ralph-wiggum/blob/main/references/sandbox-environments.md](https://github.com/ghuntley/how-to-ralph-wiggum/blob/main/references/sandbox-environments.md)  
> 33. Top OpenSandbox alternatives for managed AI sandbox ... \- Northflank, [https://northflank.com/blog/opensandbox-alternatives](https://northflank.com/blog/opensandbox-alternatives)  
> 34. E2B Alternatives for Self-Hosted AI Sandboxes 2026 \- Temps, [https://temps.sh/blog/best-e2b-alternatives-ai-sandboxes-2026](https://temps.sh/blog/best-e2b-alternatives-ai-sandboxes-2026)  
> 35. Billing & limits \- E2B Docs, [https://docs.e2b.dev/billing](https://docs.e2b.dev/billing)  
> 36. Daytona \- Secure Infrastructure for Running AI-Generated Code, [https://www.daytona.io/](https://www.daytona.io/)  
> 37. Daytona vs E2B in 2026: which sandbox for AI code execution? | Blog, [https://northflank.com/blog/daytona-vs-e2b-ai-code-execution-sandboxes](https://northflank.com/blog/daytona-vs-e2b-ai-code-execution-sandboxes)  
> 38. Secure Infrastructure for Running AI-Generated Code \- Daytona, [https://www.daytona.io/pricing](https://www.daytona.io/pricing)  
> 39. Where Should Your AI Agent Run Code: E2B vs Daytona vs Modal, [https://www.developersdigest.tech/blog/ai-agent-code-sandbox-comparison-2026](https://www.developersdigest.tech/blog/ai-agent-code-sandbox-comparison-2026)  
> 40. AI Sandbox pricing comparison (2026) | Blog \- Northflank, [https://northflank.com/blog/ai-sandbox-pricing](https://northflank.com/blog/ai-sandbox-pricing)  
> 41. Products \- Notebooks \- Modal, [https://modal.com/products/notebooks](https://modal.com/products/notebooks)  
> 42. Products \- Sandboxes | Modal, [https://modal.com/products/sandboxes](https://modal.com/products/sandboxes)  
> 43. claude-quickstarts/computer-use-demo/README.md at main \- GitHub, [https://github.com/anthropics/anthropic-quickstarts/blob/main/computer-use-demo/README.md](https://github.com/anthropics/anthropic-quickstarts/blob/main/computer-use-demo/README.md)  
> 44. anthropic-quickstarts versions \- GitHub, [https://github.com/orgs/anthropics/packages/container/anthropic-quickstarts/607088044?tag=computer-use-demo-latest](https://github.com/orgs/anthropics/packages/container/anthropic-quickstarts/607088044?tag=computer-use-demo-latest)  
> 45. anthropic-quickstarts computer-use-demo-5264b72 Public Latest, [https://github.com/anthropics/anthropic-quickstarts/pkgs/container/anthropic-quickstarts](https://github.com/anthropics/anthropic-quickstarts/pkgs/container/anthropic-quickstarts)  
> 46. AWS EC2 Pricing | Compare Instance Prices \- Holori Calculator, [https://calculator.holori.com/aws](https://calculator.holori.com/aws)  
> 47. Amazon EC2 T3 Instances \- AWS, [https://aws.amazon.com/ec2/instance-types/t3/](https://aws.amazon.com/ec2/instance-types/t3/)  
> 48. AWS EC2 t3.large Specs & Pricing in us-east-2 | DoiT Compute, [https://www.doit.com/compute/compute/aws/us-east-2/t3.large](https://www.doit.com/compute/compute/aws/us-east-2/t3.large)  
> 49. New T3 Instances – Burstable, Cost-Effective Performance \- AWS, [https://aws.amazon.com/blogs/aws/new-t3-instances-burstable-cost-effective-performance/](https://aws.amazon.com/blogs/aws/new-t3-instances-burstable-cost-effective-performance/)  
> 50. Google Cloud Pricing 2026: VM & Server Prices \- cloudprice, [https://cloudprice.app/providers/gcp](https://cloudprice.app/providers/gcp)  
> 51. e2-standard-2 pricing: \$48.92 monthly | GCP Compute Engine, [https://www.economize.cloud/resources/gcp/pricing/compute-engine/e2-standard-2/](https://www.economize.cloud/resources/gcp/pricing/compute-engine/e2-standard-2/)  
> 52. Google Cloud Pricing Models and Examples for 11 Services \[2026\], [https://www.finout.io/blog/google-cloud-pricing](https://www.finout.io/blog/google-cloud-pricing)  
> 53. AWS & GCP instance idle costs — 135 types priced \- Idlefy, [https://idlefy.com/cloud-costs/](https://idlefy.com/cloud-costs/)  
> 54. Introducing Operator \- OpenAI, [https://openai.com/index/introducing-operator/](https://openai.com/index/introducing-operator/)  
> 55. Why AI Computer Use Is \$200/Month and You Should Pay It (Or Not), [https://coasty.ai/blog/computer-use-agent-pricing-comparison-2026-20260519](https://coasty.ai/blog/computer-use-agent-pricing-comparison-2026-20260519)  
> 56. OpenAI Agents API Pricing: The Sandbox Is the Fee | TokenCost, [https://tokencost.app/blog/openai-agents-api-hosted-sandbox-pricing](https://tokencost.app/blog/openai-agents-api-hosted-sandbox-pricing)  
> 57. Pricing | OpenAI API, [https://developers.openai.com/api/docs/pricing](https://developers.openai.com/api/docs/pricing)  
> 58. Claude Code Hosting in 2026: Agent 37 vs E2B & VPS, [https://www.agent37.com/blog/what-is-the-best-claude-code-hosting-in-2026](https://www.agent37.com/blog/what-is-the-best-claude-code-hosting-in-2026)  
> 59. LLM Leaderboard \- Vellum, [https://www.vellum.ai/llm-leaderboard](https://www.vellum.ai/llm-leaderboard)