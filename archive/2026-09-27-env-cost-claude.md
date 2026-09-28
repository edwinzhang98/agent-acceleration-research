# The Environment Side of Computer-Use Agents: What Sandboxes, Cloud Browsers and VMs Cost Compared with the API Bill

At today's list prices, the environment an agent runs in costs one to two orders of magnitude less than the model API bill. A 1-hour task on a typical 2-vCPU sandbox costs about $0.17, which is about 2% of a $7.87 API bill and about 0.2% of a $72.4 API bill. However, almost no benchmark reports this cost next to its API cost. The one exception I found is AgentSysBench, which reports it only as a percentage share.

## TL;DR

- **Benchmarks:** OSWorld, OSWorld-Verified, OSWorld 2.0, TheAgentCompany and WebArena all document their infrastructure but give no dollar figure for it. The infrastructure includes the AWS instance types (t3.medium/t3.large, t3.2xlarge, t3a.xlarge), Docker/QEMU, VMware/VirtualBox and AMIs. OSWorld 2.0 reports a per-task "Cost" (≈$72.4 for Claude Opus 4.8) that tracks token usage, but the paper does not say whether it includes the AWS instances. The HAL paper reports a ≈$40,000 total, which it says is computed from tracked "token usage and costs" at "per-token costs as of September 24, 2025". Ndzomga's "Efficient Benchmarking of AI Agents" (arXiv 2603.23749, 2026) describes HAL's per-run costs as API fees. AgentSysBench (an arXiv preprint, HKUST/Alibaba/ByteDance) is the only document I found that estimates sandbox cost alongside LLM cost, and it gives only percentage shares. For its GPU-heavy Pi-AutoR application, sandbox charges are over 99% of cost.
- **Prices (accessed 2026-09-27):** Browser Use Cloud charges $0.02 per browser-hour, billed per minute with a 1-minute minimum. Browserbase includes 100 or 500 browser-hours in its $20 and $99 plans, then charges $0.12 or $0.10 per browser-hour. E2B and Daytona both charge $0.0504 per vCPU-hour plus $0.0162 per GiB-hour, billed per second; a 2 vCPU/4 GiB sandbox therefore costs $0.1656 per hour. Modal Sandboxes charge $0.00003942 per physical core per second (1 core = 2 vCPU) plus $0.00000667 per GiB per second. The official AWS T3 page lists t3.medium at $0.0418/h, t3.xlarge at $0.1670/h and t3.2xlarge at $0.3341/h. GCP e2-standard-2 is $0.0670/h (third-party figure). Anthropic publishes no hosting price for its computer-use reference container; it is a self-hosted Docker image.
- **Products:** OpenAI (Operator and ChatGPT agent) and Meta (Muse, launched 2026-09-08) say their agents run on the agent's "own" virtual computer or browser. Meta describes Muse's VM as "dedicated". Neither company states a per-session environment cost. Claude in Chrome runs in the user's own local Chrome, so there is no vendor VM for that product. My own calculation puts environment cost at 0.006% to 4.2% of the API bill across the options, task lengths and API bills modelled.

---

## 1. Source table (one row per source)

| # | Figure(s) | Exact definition / unit / what is included | URL | Date (published / accessed) | Primary / secondary |
|---|---|---|---|---|---|
| 1 | Browserbase: Free $0/mo (1 browser hour, 3 concurrent, 15 min/session); Developer $20/mo (100 browser hours, then $0.12/browser hr; 1 GB proxy then $12/GB); Startup $99/mo (500 browser hours, then $0.10/browser hr; 5 GB proxy then $10/GB); Scale custom\[1\] | Per browser-hour after included hours. Proxies, Fetch/Search calls and model tokens are billed as separate meters. Plan fee is monthly. | https://www.browserbase.com/pricing | accessed 2026-09-27 | Primary (vendor pricing page) |
| 2 | Browserbase: "Browser time is billed by the minute and proxy bandwidth by the MB, rounded, with a one-minute and one-MB minimum per session." Session caps: 15 min (Free), 6 h (Developer and Startup). Concurrency: 3 / 25 / 100 | Per-session minimum billing increment | https://docs.browserbase.com/account/billing/plans | accessed 2026-09-28 | Primary (vendor billing docs) |
| 3 | Browser Use Cloud: $0.02/browser-hour; managed residential proxy $5/GB; direct/BYO-proxy egress $0.20/GB; one-time $15 free credit; no subscription\[2\] | Per browser-hour. "Metered by the minute… one-minute minimum and rounds partial minutes up." Credits for the requested timeout are reserved upfront and the unused portion is refunded.\[2\] | https://browser-use.com/pricing.md | page says "Last verified… September 3, 2026" / accessed 2026-09-27 | Primary (vendor pricing file) |
| 4 | Browser Use: max session timeout 240 min (4 h); $0.02/hour, rounded up to the minute\[3\] | Per session (API doc) | https://docs.browser-use.com/cloud/api-v4/browsers/create-browser-session | accessed 2026-09-27 | Primary (vendor docs) |
| 5 | E2B: vCPU $0.000014/s per vCPU (2 vCPU default = $0.000028/s); RAM $0.0000045/GiB/s (4 GiB default = $0.0000180/s); Hobby free with $100 one-time credit, sessions ≤1 h, 20 concurrent; Pro $150/mo, sessions ≤24 h, 100 concurrent (expandable to 1,100 for +$500 or +$1,000/mo); Enterprise $3,000/mo minimum\[4\] | Per second of a running sandbox (wall-clock). Storage free up to 10 GiB (Hobby) or 20 GiB (Pro).\[4\] | https://e2b.dev/pricing | accessed 2026-09-27 | Primary (vendor pricing page) |
| 6 | Daytona: vCPU $0.0504/h; memory $0.0162/GiB/h; storage $0.000108/GiB/h after first 5 GiB free; Windows $0.0858/vCPU/h; GPUs (e.g., H100 $2.27/h preemptible, $3.95/h on-demand); $200 free compute\[5\] | "All billing is calculated per second."\[5\] | https://www.daytona.io/pricing | accessed 2026-09-27 | Primary (vendor pricing page) |
| 7 | Modal Sandboxes: CPU $0.00003942/physical core/s (1 core = 2 vCPU equivalent; minimum 0.125 cores); memory $0.00000667/GiB/s. Standard Functions: $0.0000131/core/s, $0.00000222/GiB/s. Starter $0 + $30/mo free compute; Team $250/mo + $100/mo free compute; region selection 1.15–1.75× base; non-preemptible 3× base\[6\] | Per second. Modal docs: billed on "whichever is higher: your request or actual usage".\[7\] | https://modal.com/pricing ; https://modal.com/docs/guide/resources | accessed 2026-09-27 | Primary (vendor pages) |
| 8 | Anthropic computer-use demo: Docker image `ghcr.io/anthropics/anthropic-quickstarts:computer-use-demo-latest`; "deliberately minimal, containerized reference… Linux desktop in Docker with X11 + VNC." No hosting price. | Self-hosted container. No per-hour price published in the README. | https://github.com/anthropics/anthropic-quickstarts/blob/main/computer-use-demo/README.md | accessed 2026-09-27 | Primary (vendor repo) |\[8\]
| 9 | AWS T3 on-demand, Linux, us-east-1: t3.medium (2 vCPU/4 GiB) $0.0418/h; t3.large (2/8) $0.0835/h; t3.xlarge (4/16) $0.1670/h; t3.2xlarge (8/32) $0.3341/h; T3 Unlimited surplus $0.05/vCPU-hour | "On-Demand Price/hr… Linux/Unix in US East (Northern Virginia)"\[9\] | https://aws.amazon.com/ec2/instance-types/t3/ | page updated 2026-09-25 / accessed 2026-09-27 | Primary (official), but conflicts with row 10 |\[9\]
| 10 | AWS t3.medium $0.0416/h; t3.large $0.0832/h; t3.xlarge $0.1664/h; m7i.large (2 vCPU/8 GiB) $0.1008/h; m7i.xlarge $0.2016/h\[10\]\[11\]\[12\] | Per hour, on-demand Linux, us-east-1 | https://instances.vantage.sh/aws/ec2/t3.medium ; https://instances.vantage.sh/aws/ec2/m7i.large ; https://www.devzero.io/instances/aws/m7i.large | accessed 2026-09-27 | Secondary (aggregators) |\[10\]\[13\]\[14\]\[15\]
| 11 | AWS Windows on-demand: t3.medium $0.0602/h; t3.xlarge $0.2406/h (Linux shown at the time: $0.0418 / $0.1670) | Per hour, Windows license included. 2018 launch prices. | https://aws.amazon.com/blogs/aws/new-t3-instances-burstable-cost-effective-performance | 2018 / accessed 2026-09-27 | Primary but dated |\[16\]
| 12 | AWS billing: "by the hour or second (minimum of 60 seconds)"; per-second for Linux and Windows | Billing increment | https://aws.amazon.com/ec2/pricing/on-demand/ | accessed 2026-09-27 | Primary (official) |\[17\]
| 13 | GCP e2-standard-2 (2 vCPU/8 GB) $0.0670/h; e2-standard-4 $0.134/h, on-demand, us-central1\[18\]\[19\] | Per hour, Linux | https://calculator.holori.com/gcp/vm/e2-standard-2 ; https://www.economize.cloud/resources/gcp/pricing/compute-engine/e2-standard-4/ | Sep 2026 / accessed 2026-09-27 | Secondary (aggregators; official E2 table not read) |\[20\]\[21\]
| 14 | GCP Windows Server image: "$0.046 USD/hour per visible vCPU" (f1-micro/g1-small $0.023/h); billing "minimum of 1 minute… after 1 minute… 1 second increments" | Per vCPU-hour license premium, added to the VM price | https://cloud.google.com/compute/all-pricing ; https://cloud.google.com/products/compute/pricing | accessed 2026-09-27 | Primary (official; license text via search snippet) |\[22\]\[23\]
| 15 | OSWorld: providers VMware/VirtualBox (desktop), Docker with QEMU/KVM (servers), AWS, Azure\[24\] | Infrastructure only, no $ | https://github.com/xlang-ai/osworld | accessed 2026-09-27 | Primary (benchmark repo; paper at NeurIPS 2024) |\[25\]
| 16 | OSWorld-Verified: "VMware/Docker → AWS, 50x parallelization"; "up to 50 environments simultaneously"; delays tuned for `t3.medium`, `t3.large`; VM image compressed "from 50GB down to 25GB… while also reducing costs"\[26\] | Infrastructure only, no $ | https://xlang.ai/blog/osworld-verified | 2025-07-28 | Primary (benchmark authors' blog) |
| 17 | OSWorld 2.0: runs "headlessly on AWS CPU instances in us-east-1, defaulting to t3.2xlarge and using larger types when needed"; residential proxy; Table 3 "Cost/task": ∼$72.4 (Claude Opus 4.8, batched), ∼$33.6 (Opus 4.7 batched), ∼$25.5 (GPT-5.5), ∼$76.1 (Opus 4.8 single), ∼$2.4 (MiniMax M3) | Per-task average over 108 tasks. The paper does not say whether AWS or proxy costs are included. | https://arxiv.org/html/2606.29537v1 | 2026-06-28 | Primary (arXiv preprint, XLANG Lab, University of Hong Kong) |\[27\]
| 18 | HAL: "orchestrates parallel evaluations across hundreds of VMs"; "support for many execution environments (local, Docker, and Azure VMs)"; 21,730 rollouts, 9 models, 9 benchmarks, "total cost of about $40,000"; "The system automatically tracks token usage and costs… We… use the per-token costs as of September 24, 2025." | Total evaluation cost, priced from per-token rates. No Azure VM line given. | https://arxiv.org/abs/2510.11977 ; https://proceedings.iclr.cc/paper_files/paper/2026/file/a0928f924a344aaebbb7f6cd8d56e34c-Paper-Conference.pdf | arXiv 2025-10-13; ICLR 2026 | Primary (peer-reviewed, ICLR 2026; Princeton-led) |
| 19 | HAL per-run costs: "Costs reflect API fees"; e.g., SWE-bench Verified median $163/run, $3.26/task; ≈$46,000 across 242 runs "consistent with HAL's reported estimate of ~$40,000";\[28\] HAL "required roughly $40,000 to evaluate agents on nine benchmarks" | Per run / per task, API fees | https://arxiv.org/pdf/2603.23749 | 24 Mar 2026 | Secondary (Franck Ndzomga, "Efficient Benchmarking of AI Agents," arXiv 2603.23749v1, analysing HAL data) |
| 20 | AgentSysBench: records "monetary cost when available"; Figure 8 "estimated per-request pay-as-you-go cost breakdown" across LLM APIs, sandbox (E2B), search (Firecrawl); Pi-AutoR "sandbox charges constitute over 99% of the per-request cost"; GUIAgent desktop sandbox ">70% of total execution time"; sandbox peak DRAM median 0.8 GB, peak 28 GB; production median session "executes for only 20% of its lifetime"\[29\] | Per-request cost *shares* (percent), not dollars | https://arxiv.org/abs/2608.15127 ; https://arxiv.org/pdf/2608.15127v1 | 2026-08-15 | Primary (arXiv preprint; HKUST, Alibaba, ByteDance) |
| 21 | TheAgentCompany: "docker and docker compose… 30+ GB of free disk space… as a reference, we used Amazon EC2 t3.2xlarge instances for baselines"\[30\] | Infrastructure only, no $ | https://github.com/TheAgentCompany/TheAgentCompany/blob/main/README.md ; https://github.com/TheAgentCompany/TheAgentCompany/blob/main/docs/SETUP.md | accessed 2026-09-27 | Primary (benchmark repo) |
| 22 | WebArena: public AMI `ami-08a862bf98e3bd7aa` in us-east-2 (Ohio); "recommended type: t3a.xlarge, 1000GB EBS root volume"; Elastic IP; optional self-hosted map backend on t3a.xlarge/1000 GB\[31\] | Infrastructure only, no $ | https://github.com/web-arena-x/webarena/blob/main/environment_docker/README.md | accessed 2026-09-27 | Primary (benchmark repo) |
| 23 | OpenAI Operator: "Using its own browser"; users "take over control of the remote browser"; initially Pro users in U.S.; folded into ChatGPT agent 2025-07-17 | Product architecture statement; no environment price | https://openai.com/index/introducing-operator/ | 2025-01-23 (updated 2025-07-17) | Primary (official) |\[32\]\[33\]
| 24 | ChatGPT agent: "carries out these tasks using its own virtual computer"; tools: "visual browser, text-based browser, terminal, and direct API access"\[34\]\[35\] | Product architecture statement; no environment price | https://openai.com/index/introducing-chatgpt-agent/ | 2025-07-17 | Primary (official) |\[34\]
| 25 | Operator shutdown "August 31, 2025"; ChatGPT Work uses "a persistent cloud-based virtual machine that runs on OpenAI's servers"\[36\] | Product architecture (press report) | https://venturebeat.com/orchestration/openai-introduces-chatgpt-work-a-cloud-based-ai-agent-that-manages-tasks-across-email-slack-and-calendars | 2026 | Secondary (press) |
| 26 | Claude in Chrome: "browser extension that allows Claude to read, click, and navigate websites alongside you";\[37\] "available for all paid plans (Pro, Max, Team, and Enterprise)"; on Max/Team the side panel "runs as a Claude Cowork session" | Local extension in user's browser; no environment price | https://support.anthropic.com/en/articles/12012173-getting-started-with-claude-for-chrome (redirects to support.claude.com) | 2026-08-26 | Primary (official support doc) |\[37\]
| 27 | Meta Muse: "runs on Muse Secure VM, a dedicated secure computer with its own browser"; "Muse Confidential VM" planned "later this year" | Product architecture; no environment price | https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/ | 2026-09-08 | Primary (official newsroom; quoted text from search snippet, page fetch truncated) |\[38\]
| 28 | Muse "runs on a dedicated virtual machine in Meta's cloud, using a built-in browser"; free tier plus $20/mo and $100/mo subscriptions | Subscription price (not a per-session environment cost) | https://www.axios.com/2026/09/08/meta-debuts-muse-personal-ai-agent | 2026-09-08 | Secondary (press) |\[39\]

---

## 2. The four questions

### (a) Do benchmarks report environment compute cost next to API cost?

In the documents I checked, only one gives any estimate of environment cost, and it gives percentages rather than dollars. Classification:

| Benchmark | Documents checked | VM / env spec | Hosting method | Environment $ reported? | Class |
|---|---|---|---|---|---|
| OSWorld [Xie et al., NeurIPS 2024] | GitHub README | Ubuntu VM image; Docker path needs KVM | VMware Workstation/Fusion, VirtualBox, Docker (QEMU in Docker), AWS, Azure\[24\] | No | (i) infra documented, no cost |\[25\]
| OSWorld-Verified [XLANG Lab blog, 2025] | Blog post; README update note | t3.medium / t3.large mentioned; VM image 50 GB → 25 GB\[26\] | AWS AMI/EBS, up to 50 parallel environments\[26\] | No. Says the image shrink was "also reducing costs" but gives no figure | (i) |
| OSWorld 2.0 [XLANG Lab, arXiv 2026] | arXiv HTML (setup, Table 3) | t3.2xlarge default, larger when needed; residential proxy | AWS us-east-1, headless | Reports "Cost/task" (e.g., ∼$72.4) but does not define it. It scales with output tokens, so it is most likely API cost; whether AWS is included is **not stated** | (i), with an undefined cost column |\[27\]
| HAL [Kapoor et al., ICLR 2026] | arXiv abstract/intro; ICLR PDF snippets; about page | "hundreds of VMs"\[40\] | "local, Docker, and Azure VMs" (HAL paper) | Total "about $40,000", which the paper says comes from tracked "token usage and costs" at "per-token costs as of September 24, 2025". Ndzomga [arXiv 2603.23749, 2026] says HAL costs "reflect API fees". The paper gives no Azure VM line | (i). I did not read the HAL cost-accounting appendix in full, so this is a narrow finding |
| AgentSysBench [Chang et al., arXiv 2026; HKUST/Alibaba/ByteDance] | Full PDF | Docker containers per module; GPU server; E2B pricing used for sandbox estimate | Docker, controlled deployment | **Yes, as shares**: Fig. 8 splits per-request cost into LLM, sandbox (E2B rates) and search (Firecrawl). No absolute $/task in the text\[29\] | (ii) partial: gives cost shares, not dollars |
| TheAgentCompany | README, SETUP.md (paper not checked) | Docker Compose services (GitLab, Plane, ownCloud, RocketChat); 30+ GB disk\[30\] | Docker on EC2 t3.2xlarge "for baselines"\[30\] | No | (i). Paper not examined |
| WebArena | environment_docker/README.md | 1000 GB EBS | Public AMI in us-east-2, t3a.xlarge recommended; Docker alternative\[31\] | No | (i) |

Interpretation:
- The benchmarks tell you *which* machine to run but not *what it costs*. You can price the environment yourself from the instance type (see d).
- AgentSysBench is the only source I found that treats sandbox cost as a first-class metric. Its main finding runs against the "environment is negligible" conclusion in some cases. Where a session holds a GPU sandbox (Pi-AutoR), the sandbox is over 99% of cost. Its production traces also show idle-but-live sessions, with the median session active for only 20% of its lifetime.\[29\] If the environment is billed on wall-clock time, cost therefore scales with session lifetime, not with active steps.
- Weighting: HAL is peer-reviewed (ICLR 2026) and OSWorld is peer-reviewed (NeurIPS 2024). OSWorld 2.0 and AgentSysBench are arXiv preprints.\[25\]\[27\]

### (b) What sandbox and cloud-browser services charge

| Service | Unit | Tiers / free tier | Minimum increment | Price for a 2 vCPU / 4 GiB (or 1 browser) hour |
|---|---|---|---|---|
| Browser Use Cloud | per browser-hour ($0.02), plus traffic per GB\[2\] | No subscription; $15 one-time credit; concurrency tiers by lifetime spend (10 → 1,000)\[2\] | Per minute, 1-minute minimum, round up\[2\] | $0.02 |
| Browserbase | per browser-hour after included hours | Free (1 h, 15 min/session); Developer $20 (100 h, then $0.12); Startup $99 (500 h, then $0.10); Scale custom\[1\] | Billed by the minute with "a one-minute and one-MB minimum per session" (Browserbase billing docs); session caps 15 min (Free) and 6 h (Developer/Startup) | $0.12 / $0.10 overage; $0.20 effective if the $20 plan's 100 h are fully used ($20 ÷ 100) — my calculation |
| E2B | per vCPU-second + per GiB-second | Hobby free ($100 credit, ≤1 h sessions); Pro $150/mo (≤24 h); Enterprise ≥$3,000/mo\[4\] | Per second | 2×$0.000014 + 4×$0.0000045 = $0.000046/s → $0.1656/h\[41\] |
| Daytona | per vCPU-hour + per GiB-hour + storage GiB-hour, billed per second | $200 free compute; startups up to $50k\[5\] | Per second | 2×$0.0504 + 4×$0.0162 = $0.1656/h\[41\] |
| Modal Sandboxes | per physical-core-second (1 core = 2 vCPU) + per GiB-second\[6\] | Starter $0 (+$30/mo credit); Team $250/mo (+$100 credit)\[6\] | Per second; billed on max(request, usage)\[7\] | 1 core × $0.00003942 × 3600 = $0.1419; 4 GiB × $0.00000667 × 3600 = $0.0960; total $0.2379/h (before any region multiplier) |
| Anthropic computer-use reference container | — | Self-hosted Docker image; **no hosting price published** | — | = whatever host you run it on |\[8\]
| AWS t3.medium (2 vCPU/4 GiB), us-east-1, Linux | per hour | On-demand | Per second, 60-s minimum | $0.0418 (official T3 page) vs $0.0416 (aggregators)\[11\] |\[9\]
| AWS t3.xlarge (4 vCPU/16 GiB) | per hour | On-demand | Per second, 60-s minimum | $0.1670 (official) vs $0.1664 (aggregators)\[12\] |\[12\]
| AWS m7i.large (2 vCPU/8 GiB, non-burstable) | per hour | On-demand | Per second | $0.1008 (aggregator only)\[10\] |\[10\]
| GCP e2-standard-2 (2 vCPU/8 GB), us-central1 | per hour | On-demand; E2 has no sustained-use discount | 1-minute minimum, then per second | $0.0670 (aggregator)\[19\] |\[20\]\[42\]
| GCP e2-standard-4 (4 vCPU/16 GB) | per hour | On-demand | Same | $0.134 (aggregator)\[18\] |\[21\]

Windows and GPU needs:
- **Windows:** AWS's 2018 launch table priced t3.medium at $0.0602/h on Windows vs $0.0418/h on Linux. GCP adds $0.046 per visible vCPU per hour for Windows Server images.\[16\]\[23\] Daytona lists Windows sandboxes at $0.0858/vCPU/h vs $0.0504 on Linux.\[5\] None of the benchmark docs I read require Windows: OSWorld and OSWorld 2.0 use Ubuntu images, and WebArena and TheAgentCompany are Linux services.
- **GPU:** None of the GUI-agent benchmark docs state that the environment needs a GPU. OSWorld 2.0 explicitly uses "AWS CPU instances".\[27\] AgentSysBench's >99% sandbox-cost case comes from "GPU-accelerated containers for scientific simulations", not from GUI rendering.\[29\]
- **AWS conflict:** The official T3 page (updated 2026-09-25) shows $0.0418, $0.0835, $0.1670 and $0.3341. Aggregators that draw on the AWS Price List API show $0.0416, $0.0832 and $0.1664.\[9\]\[15\] The difference is about 0.5%. I use the official page and flag the conflict; it does not change any conclusion.

### (c) Products that allocate a dedicated VM or browser, and any per-session cost

| Product | What the primary source says about the environment | Dedicated per user/session? | Per-session environment cost or price |
|---|---|---|---|
| OpenAI Operator (Jan 2025; shut down Aug 31, 2025 per VentureBeat)\[36\] | "Using its own browser"; user can "take over control of the remote browser" | OpenAI's primary source states only a remote browser. VentureBeat (Jul 2025, secondary) describes "a private 'headless browser,' that is, a cloud-based custom web browser that OpenAI itself maintained and offered for each Operator session" | **Not stated** |
| OpenAI ChatGPT agent (Jul 2025) | "using its own virtual computer"; visual browser, text browser, terminal, APIs\[34\]\[35\] | "Its own virtual computer" is stated; whether it is dedicated vs. shared at the infrastructure level is **not stated** | **Not stated** |\[34\]
| OpenAI ChatGPT Work (2026, secondary only) | "persistent cloud-based virtual machine that runs on OpenAI's servers" (VentureBeat)\[36\] | Persistent VM per the press report; no OpenAI primary source checked | **Not stated** |
| Anthropic Claude in Chrome | Browser extension in the user's own Chrome; on Max/Team the side panel runs as a Cowork session;\[37\]\[43\] Cowork also has a built-in browser in Claude Desktop | Runs locally in the user's browser, so there is no vendor-hosted VM for the extension. Cowork's cloud environment internals are **not stated** in the doc read | **Not stated** (included in paid plans) |\[37\]
| Meta Muse (Sep 8, 2026) | "Muse Secure VM, a dedicated secure computer with its own browser"; Axios: "dedicated virtual machine in Meta's cloud" | **Yes, "dedicated" is stated by Meta** | **Not stated** per session; Axios reports free, $20/mo and $100/mo subscription tiers |\[38\]\[39\]

A Meta computer-use/browser agent product does exist: Muse. Meta's newsroom text is quoted from a search snippet because my page fetch was truncated. TechCrunch (secondary) reports that a Mac version can "operate any app on a user's desktop".\[44\]

### (d) Environment cost of 15-minute and 1-hour tasks vs. $7.87 and $72.4 API bills — my own calculation

Method: environment cost = hourly rate × hours. Ratio = environment cost ÷ API bill. The calculation uses metered usage only; plan fees, proxies, storage and idle time are excluded. $72.4 matches OSWorld 2.0's Opus 4.8 batched Cost/task;\[27\] I could not locate the source of $7.87, so I treat it as user-supplied.

Hourly rates used:
- **Cheapest browser:** Browser Use Cloud, $0.02/browser-hour (row 3).\[2\]
- **Cheapest desktop VM:** AWS t3.medium, $0.0418/h (row 9).\[9\]
- **Typical cloud browser:** Browserbase Developer overage, $0.12/browser-hour (row 1).\[1\]
- **Typical sandbox:** E2B or Daytona, 2 vCPU/4 GiB: 2 × $0.0504 + 4 × $0.0162 = $0.1008 + $0.0648 = $0.1656/h (rows 5–6).\[45\]\[46\]
- **Benchmark-matched VM:** AWS t3.2xlarge, $0.3341/h, OSWorld 2.0's default (rows 9, 17).\[9\]\[27\]

Step-by-step:
- Browser Use: 15 min = 0.25 h × $0.02 = **$0.0050**; 1 h = **$0.0200**
- t3.medium: 0.25 × $0.0418 = **$0.01045**; 1 h = **$0.0418**
- Browserbase: 0.25 × $0.12 = **$0.0300**; 1 h = **$0.1200**
- E2B/Daytona: $0.000046/s × 900 s = **$0.0414**; × 3,600 s = **$0.1656**
- t3.2xlarge: 0.25 × $0.3341 = **$0.0835**; 1 h = **$0.3341**

| Option (source price) | 15-min env cost | ÷ $7.87 | ÷ $72.4 | 1-h env cost | ÷ $7.87 | ÷ $72.4 |
|---|---|---|---|---|---|---|
| Browser Use $0.02/h | $0.0050 | 0.064% | 0.0069% | $0.0200 | 0.25% | 0.028% |
| AWS t3.medium $0.0418/h | $0.0105 | 0.13% | 0.014% | $0.0418 | 0.53% | 0.058% |
| Browserbase $0.12/h | $0.0300 | 0.38% | 0.041% | $0.1200 | 1.5% | 0.17% |
| E2B/Daytona 2 vCPU/4 GiB $0.1656/h | $0.0414 | 0.53% | 0.057% | $0.1656 | 2.1% | 0.23% |
| AWS t3.2xlarge $0.3341/h | $0.0835 | 1.06% | 0.12% | $0.3341 | 4.2% | 0.46% |

Example arithmetic: $0.1656 ÷ $7.87 = 0.0210 (2.1%); $0.1656 ÷ $72.4 = 0.00229 (0.23%); $0.3341 ÷ $7.87 = 0.0425 (4.2%).

What this means:
- On metered compute alone, the environment is between about 1/15,000 and 1/24 of the API bill.
- For low-volume users, fixed fees dominate. Browserbase's $20 plan or E2B Pro's $150/month floor dwarfs per-task metered cost unless you run hundreds of hours.
- Proxy bandwidth can also exceed browser time. At $5–12/GB, 1 GB costs more than 40 hours on Browser Use.
- Wall-clock billing matters. If a session is left alive while waiting, which AgentSysBench found is the production norm (median 20% active),\[29\] multiply the figures above accordingly.
- The environment becomes material only with GPU sandboxes. At Daytona's H100 rate of $3.95/h,\[5\] a 1-hour task would be 50% of a $7.87 bill (my calculation: $3.95 ÷ $7.87 = 0.502).\[45\]

**Recommendation:** When reporting per-task cost, add one line for the environment: instance type × wall-clock hours × list price, plus proxy GB. For CPU-only GUI and web agents, expect it to add under 5% to a $7.87 API bill and under 0.5% to a $72.4 bill. Spend engineering effort on idle-session teardown and proxy usage, not on hunting for cheaper vCPUs.

---

## 3. What I could not find

- **Any dollar figure for environment compute** in the OSWorld README, the OSWorld-Verified blog, OSWorld 2.0's setup section and Table 3, the TheAgentCompany README/SETUP, the WebArena environment README, or the HAL sections I read.
- **OSWorld 2.0's definition of "Cost/task"**, in particular whether it includes AWS or residential-proxy charges. I did not read the full appendix, the project website (osworld-v2.xlang.ai) or the OSWorld-V2 GitHub README.
- **A separate VM cost line in HAL.** The HAL paper lists "local, Docker, and Azure VMs" and says its ≈$40,000 comes from tracked "token usage and costs" at "per-token costs as of September 24, 2025". It gives no Azure VM line. I did not read Appendix A2 or the HAL website methodology page in full.
- **AgentSysBench's absolute per-request dollar values.** Figure 8 is presented as percentages, and the code is "will be released", so it is not yet available.\[29\]
- **TheAgentCompany paper** (not examined) and the WebArena paper's hosting notes (not examined). I also did not find a t3a.xlarge us-east-2 price.
- **Official current prices** for AWS m7i and Windows T3, and for GCP E2 per-hour and per-vCPU rates. These came from aggregators or dated official pages.
- **Browserbase's per-session minimum billing** is now resolved: Browserbase's billing docs (docs.browserbase.com/account/billing/plans) state "Browser time is billed by the minute and proxy bandwidth by the MB, rounded, with a one-minute and one-MB minimum per session."
- **A per-session cost on OpenAI's help-center page for ChatGPT agent** (help.openai.com/en/articles/11752874, fetched 2026-09-28). The page says "ChatGPT agent is no longer available. Use ChatGPT Work for longer, multi-step tasks." It gives no per-session environment cost. Its archived limits are "Plus: 40 messages/month; Pro: 400 messages/month; …flexible pricing: 30 credits/message". It also says the agent "uses screenshots of its virtual browser window" and that "Cookies persist across sessions."
- **Any per-session environment cost** for ChatGPT agent/Operator, Claude in Chrome/Cowork, or Meta Muse. None is stated in the sources checked.
- **The source of the $7.87 API figure.**

## Caveats

- Several documents are future-dated relative to common knowledge (e.g., OSWorld 2.0, AgentSysBench, Muse, Claude in Chrome GA). I report them as the pages state and did not independently verify them.
- Vendor pages are primary for their own prices but self-interested. Browser Use's "ranked first" stealth claims are vendor marketing and are not used as evidence. Browserbase's statement that 100 hours is "roughly 3,000 page-level tasks" is also a vendor claim.\[1\]\[2\]
- Prices change often; all were accessed on 2026-09-27.

## Sources

1. [Browserbase Pricing: Free, \$20, \$99, or Custom](https://www.browserbase.com/pricing)
2. [BROWSER USE](https://browser-use.com/pricing.md)
3. [Create Browser Session - Browser Use](https://docs.browser-use.com/cloud/api-v4/browsers/create-browser-session)
4. [Pricing | E2B — The AI Agent Cloud](https://e2b.dev/pricing)
5. [Daytona - Secure Infrastructure for Running AI-Generated Code](https://www.daytona.io/pricing)
6. [Plan Pricing](https://modal.com/pricing)
7. [Configuring CPU, memory, and disk | Modal Docs](https://modal.com/docs/guide/resources)
8. [claude-quickstarts/computer-use-demo/README.md at main · anthropics/claude-quickstarts](https://github.com/anthropics/anthropic-quickstarts/blob/main/computer-use-demo/README.md)
9. [Amazon EC2 T3 Instances – Amazon Web Services (AWS)](https://aws.amazon.com/ec2/instance-types/t3/)
10. [m7i.large — AWS EC2 Instance Pricing & Specs | DevZero](https://www.devzero.io/instances/aws/m7i.large)
11. [Understanding AWS Pricing for EC2, S3, EBS, RDS, & More](https://www.finout.io/blog/understanding-aws-pricing)
12. [t3.xlarge pricing and specs - Amazon EC2 Instance Comparison](https://instances.vantage.sh/aws/ec2/t3.xlarge)
13. [m7i.4xlarge pricing and specs - Vantage](https://instances.vantage.sh/aws/ec2/m7i.4xlarge)
14. [m7i.xlarge pricing and specs - Vantage](https://instances.vantage.sh/aws/ec2/m7i.xlarge)
15. [t3.medium pricing and specs - Vantage](https://instances.vantage.sh/aws/ec2/t3.medium)
16. [AWS News Blog](https://aws.amazon.com/blogs/aws/new-t3-instances-burstable-cost-effective-performance)
17. [EC2 On-Demand Instance Pricing](https://aws.amazon.com/ec2/pricing/on-demand/)
18. [Google Compute Engine pricing (2026): CUDs, SUDs, Spot](https://www.usage.ai/blogs/gcp/compute-engine/)
19. [GCP e2-standard-2 Pricing & Specs: 2 vCPU, 8 GiB — \$48.92/mo (July 2026)](https://spendark.com/instances/e2-standard-2/)
20. [e2-standard-2 pricing and specs - Google Cloud | Holori](https://calculator.holori.com/gcp/vm/e2-standard-2)
21. [GCP e2-standard-4 Pricing | Economize](https://www.economize.cloud/resources/gcp/pricing/compute-engine/e2-standard-4/)
22. [VM instance pricing](https://cloud.google.com/products/compute/pricing)
23. [Pricing | Compute Engine: Virtual Machines (VMs) | Google Cloud](https://cloud.google.com/compute/all-pricing?authuser=0)
24. [GitHub - X5-main/OSWorld: \[NeurIPS 2024\] OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments · GitHub](https://github.com/X5-main/OSWorld)
25. [GitHub - xlang-ai/OSWorld: \[NeurIPS 2024\] OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments](https://github.com/xlang-ai/osworld)
26. [Introducing OSWorld-Verified](https://xlang.ai/blog/osworld-verified)
27. [OSWorld 2.0: Benchmarking Computer Use Agents on Long-Horizon Real-World Tasks](https://arxiv.org/html/2606.29537v1)
28. [Efficient Benchmarking of AI Agents](https://arxiv.org/pdf/2603.23749)
29. [From LLM Inference to Agentic Workloads: Characterization and Implications for Serving Systems](https://arxiv.org/pdf/2608.15127v1)
30. [TheAgentCompany/README.md at main · TheAgentCompany/TheAgentCompany](https://github.com/TheAgentCompany/TheAgentCompany/blob/main/README.md)
31. [webarena/environment\_docker/README.md at main · web-arena-x/webarena](https://github.com/web-arena-x/webarena/blob/main/environment_docker/README.md)
32. [Introducing\_Operator\_research\_preview\_\_OpenAI\_1 | annotated by Harry](https://readwise.io/reader/shared/01jjb2091v23ej4mkw6k6tpbrm/)
33. [Introducing Operator | OpenAI](https://openai.com/index/introducing-operator/)
34. [Introducing ChatGPT agent: bridging research and action | OpenAI](https://openai.com/index/introducing-chatgpt-agent/)
35. [OpenAI (@OpenAI) on X](https://x.com/OpenAI/status/1945904743148323285)
36. [OpenAI introduces ChatGPT Work, a cloud-based AI agent that manages tasks across email, Slack and calendars | VentureBeat](https://venturebeat.com/orchestration/openai-introduces-chatgpt-work-a-cloud-based-ai-agent-that-manages-tasks-across-email-slack-and-calendars)
37. [12012173 getting started with claude for chrome](https://support.anthropic.com/en/articles/12012173-getting-started-with-claude-for-chrome)
38. [Introducing Muse: The World’s First Personal AI Agent Built for Everyone](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)
39. [Meta debuts Muse, its long-planned personal AI agent](https://www.axios.com/2026/09/08/meta-debuts-muse-personal-ai-agent)
40. [\[2510.11977\] Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation](https://arxiv.org/abs/2510.11977)
41. [Daytona's \$3.95/hr H100 vs Owning the Card: The Breakeven Math for GPU Agent Sandboxes | bex.co](https://bex.co/blog/2026/09/09/daytona-h100-sandbox-hours-vs-owning-gpu)
42. [General-purpose machine family for Compute Engine | Google Cloud Documentation](https://docs.cloud.google.com/compute/docs/general-purpose-machines)
43. [Claude Cowork can now run in a Chrome sidebar - Engadget](https://www.engadget.com/2235919/claude-cowork-can-now-run-in-a-chrome-sidebar/)
44. [Everything new coming to Meta's AI agent Muse | TechCrunch](https://techcrunch.com/2026/09/23/everything-new-coming-to-metas-ai-agent-muse/)
45. [E2B Pricing Explained (2026): Tiers, Limits, and Cheaper Alternatives | Beam](https://www.beam.cloud/blog/e2b-pricing-explained)
46. [E2B vs Modal vs Daytona: AI Sandbox Pricing 2026](https://tech-insider.org/e2b-vs-modal-vs-daytona-2026/)
