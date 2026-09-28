<!-- Exported from the Claude Doc 《Agent 加速：别人做到哪了》 (https://claude.ai/code/artifact/78792e6b-fdae-4009-a8fc-a880e7e00645), rev 19, on 2026-09-28. The Claude Doc is the working copy Edwin comments on; this file is a snapshot for the repo and for Claude Code. Embedded diagrams/charts appear as '[embedded content: …]' placeholders; formulas are ```latex blocks. -->

# Agent 加速：别人做到哪了

Sep 27, 2026 · @Edwin

这是第二份文档，只回答一个问题：把 agent 做快、做便宜这件事，现有文献已经做到什么程度。每一篇文献都讲清楚它的思路、它改的是第一份文档《Agent 慢和贵的逻辑链》里的哪个环节（用那份文档的编号，对不上的就说对不上）、效果是多少以及在什么条件下测的。引用写法和第一份一样：（第一作者 et al., 年份）+ \[dossier v3 台账条目号\]，来源类型用文字（会议或期刊论文 / 预印本，标机构 / 厂商一手资料 / 行业报告 / 代码），厂商营销数字不作来源，我自己算的标 calc.。

## 零、怎么读这份文档

现有文献的加速思路归成三条路线，每条对应第一份文档里一组慢的原因。这个对应是我用来整理的框架，不是文献自己的分类；对不上的地方会明说。

| 路线 | 一句话 | 对应的慢的原因（第一份文档编号） | 对应的贵的原因 | 典型做法 |
| --- | --- | --- | --- | --- |
| 路线一：少转圈、少调模型 | 同样的任务，让模型少出场几次 | 做的步数多（I-1 到 I-5）、每步调用多（II-1 到 II-3） | 调用次数多（第三类），连带读写都少 | 把做过的任务编译成脚本重放；把走过的路存成可调用的“技能”；能调应用的 API 就不点界面；一次调用输出多个动作；厂商的录制回放加失败时叫模型修 |
| 路线二：每次调用更快、更便宜 | 模型还是每步都出场，但每次读得少、写得少、或者换个便宜的模型 | 读得多（III-2）、写得多（III-3）、排队（III-1）、思考模式和大模型（III-4） | 读的 token 多（第一类）、写的 token 多（第二类）、单价（第五类） | 缓存提示前缀；裁掉页面里无关的部分；裁掉或压缩历史截图；小模型做简单步、大模型做难步；控制思考长度；买厂商的速度档；专门为 agent 设计的推理服务系统（工具调用期间把缓存留在显存里、按整个程序调度） |
| 路线三：把等待重叠起来 | 不减少工作量，让环境和模型同时干活 | 环境慢（IV-1 到 IV-4）、串行（第五类） | 不省钱，往往还多花钱（猜错的那些调用照付） | 猜下一步先做（speculation）；多个工具并行；模型一边写一边让工具先跑；预加载页面；以及“猜错了怎么撤销”的安全机制 |

“做到什么程度”用三把尺子量，每篇文献都按这三项写：

- 效果：时间或钱省了多少，准确率变了多少。两个数必须一起看：只报加速不报准确率的，按“准确率未报告”记。
- 条件：在什么任务、什么模型、什么设置下测的；比的基线是谁；是真实网站、本地模拟站点还是文字游戏。同一个数字换个条件就不成立。
- 适用范围：对哪种 agent 有效（截图型桌面 / 文本型 web / 带缓存的 coding / 只调 API 的工具型），以及它自己声明的前提（比如“只对只读操作”“需要能快照的环境”）。

来源类型的分布先说在前面：这个领域的工作大多是 2025–2026 年的预印本，已经进了会议的是少数（ICLR 2025 / 2026、ICML 2024 / 2025 / 2026、NeurIPS 2024 / 2025、NSDI 2026、MLSys 2026、ACL 2025、COLM 2025 各几篇）。下面每篇都标了；在 slides 上优先用进了会议的。

**来源可信度规则（2026-09-27 起，全文按此执行）**

1. 会议或期刊论文：直接用，写会议或期刊名和年份。
2. 预印本：同时满足四条才当证据用——作者姓名和机构在 arXiv 页面上核过；机构是大学、国家实验室或有研究部门的公司；数字在公开 benchmark 上测、任务数和模型写明；不是单作者的公司报告。满足的写成“预印本，机构”。
3. 不满足的预印本一律不当证据：不进各节的表、不进第四节总表、不上 slides，也不列入第六节参考文献；只在第五节“不采用或待核的来源”表里留一行写明原因，等于当作没有这个信息源。本次据此撤下 4 篇：Agentic Compilation（Selfotix，单作者）、PreAct（Pine AI，单作者）、LOOP（蚌埠医科大学 + 一家生物技术公司，标题即宣传语）、Activity Frames（独立研究者）。
4. 只借用思路、不用数字的工作，同样要核过作者和机构才保留，并在参考文献里注明“只用定性信息”。
5. 会议或期刊的录用只认官方页面或 arXiv 页面上的标注；论文页首的模板版权栏（如 “AAAI 2027”）或“在审”不算录用，按预印本处理。
6. 第三方机构（如 Gemini、ChatGPT 的调研）报出来的署名和结论一律回到 arXiv 页面核对；本次核出一处署名错误（第 2.2 节，D146）。

## 一、路线一：少转圈、少调模型

这条路线的共同想法：模型不必每一步都出场。五种做法，按“模型退得多彻底”排序：把做过的任务编译成脚本重放（模型只在第一次和失败时出场）；把走过的路存成技能或记忆（模型还在，但少走弯路）；能调应用的 API 就不点界面；一次调用输出多个动作；厂商的录制回放加失败时叫模型修。它们改的都是第一份文档里的“步数多（I）”和“每步调用多（II）”，所以时间和钱一起省（同源）。

### 1.1 把做过的任务编译成脚本重放

| 文献 | 思路 | 改的环节 | 效果和条件 | 来源类型 |
| --- | --- | --- | --- | --- |
| Agent JIT Compilation（Winston et al., 2026）\[E18、E100；§3.1\] | 把任务指令“编译”成一段代码计划，代码调用的是事先建好并缓存的网站工具（每个工具带前置 / 后置条件检查）；再用一个蒙特卡洛调度器在多个候选计划里挑延迟最低的，并同时跑几个以防万一（hedging） | 整个任务变成一段程序：步数多（I-1）、纯导航的步（I-3）、每步调用（II）一起消失 | 在 37 个任务、5 个网站应用（从 REAL / WebArena 派生）上，模型 GPT-4.1：Browser-Use 每任务 150.1 秒 → JIT-Planner 15.4 秒（我们算是 9.7 倍，论文标题写 10.4 倍，各应用 7.4–18.9 倍，D43），成功率 61% → 90%；JIT-Scheduler 比 OpenAI 的 CUA 快 2.4 倍、准 9 个点。离线建工具的时间不计入；样本小 | 会议论文（ICML 2026），Stanford |
| EchoPath（Zhao et al., 2026）\[§3.2；D82、D83、D85\] | 第一次做任务时，把验证过的 GUI 轨迹存成“可调用的记忆”：带前置条件、参数范围、视觉重新定位，以及提升 / 修复 / 隔离三种生命周期状态（描述了，没评测）；第二次直接重放，不调模型 | 步数（I-1）和每步调用（II）：重放的那些步不再调模型 | 在 OSWorld-Verified 上，第一遍跑出来、筛选后的 159 条“可执行记忆”（第一遍尝试了多少次没报），第二遍中位数执行 token 20,370、时间 127.5 秒、成功率 91.2%（Codex，gpt-5.5-medium）；基线 Synapse（同一模型，把轨迹当示例塞进提示）586,386 token、315.7 秒、91.8%。两遍之间只换了屏幕分辨率（1920×1080 → 1600×900），没测应用版本变化；作者自述“尚未建立界面漂移下的鲁棒性”；代码链接 2026-09-27 返回 404 | 预印本，Johns Hopkins + Amazon AGI |
| GPA（Zhao et al., 2026）\[§3.1\] | 把一次人类演示编译成局部匹配的 GUI 转移序列，运行时没有任何 LLM 决策 | I、II 全消 | 桌面试点：Gemini 3 Pro 每任务 329.31 秒 → GPA 33.74 秒，成功率 89.38% → 100%。只有 16 个重复工作流任务 | 预印本，Salesforce |
| ActionEngine（Zhong et al., 2026）\[§3.1\] | 把网站学成一张状态机记忆，由它合成可执行的工作流，带修复 | I-1、II | WebArena Reddit 106 个任务：237 → 118 秒，$0.71 → $0.06 / 任务，10.2 → 1.8 次调用，成功率 66% → 95%。但基线和方法用了不同模型（AgentOccam + GPT-4-Turbo vs ActionEngine + Claude 4.5 Sonnet），比较有混杂 | 预印本，Georgia Tech + Microsoft Research |
| SkillDroid（Chen et al., 2026）\[§3.1\] | 把成功的 GUI 轨迹编译成参数化技能模板（正则 + 语义匹配），重放不调 LLM | I、II | Android 上 79 轮重放成功率 100%；平均延迟 84.1 → 35.4 秒（2.4 倍）；比无状态基线 +23 pp。单一来源，只有手机 | 预印本，U Helsinki + Shenzhen U + UC3M |
| AutoDroid-V2（Wen et al., 2025）\[§3.1\] | 小模型从学到的应用文档直接生成一整段可执行的 GUI 脚本 | I、II | DroidTask：推理时间 669.2 → 46.3 秒 / 任务（−93.1%），成功率 43.9% → 54.4%。推理时间不是全流程 wall-clock，训练不计；手机 | 会议论文（MobiSys 2025），Tsinghua AIR |
| AppAgentX（Jiang et al., 2025）\[§3.1\] | 反复出现的动作链变成参数化快捷方式，带原子回退 | I-1 | AndroidWorld：147.17 → 59.74 秒 / 任务，18.9K → 6.2K tokens，41.7% → 62.5%。只对所有方法都做成的任务计时；单次运行 | 预印本，Westlake + Henan U + Southeast U + A\*STAR（IHPC / CFAR） |

### 1.2 把走过的路存成技能或记忆（模型还在，但少走弯路）

| 文献 | 思路 | 改的环节 | 效果和条件 | 来源类型 |
| --- | --- | --- | --- | --- |
| Agent Workflow Memory（Wang, Mao, Fried, Neubig, 2025）\[§3.2；D41\] | 从成功轨迹里归纳出文字形式的“工作流”，下次检索出来放进提示里指导 agent | 意图是 I-1（少走弯路） | WebArena（GPT-4，AXTree）：7.9 → 5.9 步，15.0% → 35.5%。但在 ASI 的受控复现里 AWM 5.9 步 vs 原版 5.6 步：文字工作流指导 agent，但不替代它的调用 | 会议论文（ICML 2025），CMU + MIT |
| ASI: Inducing Programmatic Skills（Wang, Gandhi, Neubig, Fried, 2025）\[§3.1\] | 从自己的成功轨迹在线归纳可执行的 Python 技能（重跑验证），一次技能调用替代几步 LLM 决策 | I-1、II | WebArena 40.4% vs 原版 32.7%；步数少 10.7–15.3%（5.0 vs 5.6）。没有 wall-clock 和美元；界面变了技能要改；SpeedRunner 指出技能库越积越多，成本随之增长 | 会议论文（COLM 2025），CMU |
| SkillWeaver（Zheng et al., 2025）\[§3.1\] | agent 自主探索网站、练习并测试可复用的 Playwright 函数 | I、II | WebArena / GPT-4o 22.6% → 29.8%；技能可迁移给更弱的 agent（+54.3%）。延迟和成本没报 | 预印本，Ohio State + Virginia + Purdue + CMU + Cisco Research |
| WALT（Prabhu et al., 2026）\[§3.1；D42\] | 从探索或演示里学出验证过的工具，包括确定性的 URL / API 操作 | I-1、I-3 | VWA-Classifieds（GPT-5-mini）：无工具 8.9 步、57.5% → 完整 WALT 7.0 步、64.1%；“少 1.3–1.4 倍步”是跨 split 的平均。步数不是时间 | 会议论文（ICLR 2026），Salesforce AI Research |
| SpeedRunner（Huang et al., 2026）\[§3.1\] | 让一个 coding agent 当“归纳器”，在 wake–sleep 周期里重构可执行技能库；以成本为第一目标 | II、写的 token | BabyAI 上输出 token 约为 ReAct 的 1/8，成功率接近满分（GPT-5.4-mini）；比 ASI 省 2–8 倍 token；Crafter 里 LLM 调用 −94%（Gemini-3-Flash）；3 个种子。文字游戏，没有延迟；作者自己说可能“过度压缩一个能干的 actor” | 预印本，Johns Hopkins |
| Agentic Plan Caching（Zhang, Wornow, Wan, Olukotun, 2025）\[§3.2\] | 从过去的计划里抽模板，关键词匹配，命中后用一个便宜的规划器把模板适配到新任务 | II（大模型的规划调用换成小模型） | 5 个工作负载平均成本 −50.31%、延迟 −27.28%，达到最优的 96.61%；GAIA / ODR $69.02 → $16.27，准确率 37.58% → 36.97%；缓存开销占成本 1.04%。命中后仍要一次 LLM；论文同时证明基于 embedding 相似度的语义缓存会因误命中掉准确率 | 会议论文（NeurIPS 2025），Stanford |
| Are Online Skill and Memory Modules Always Worth Their Tokens?（Hajimiri et al., 2026）\[§3.8\] | 把“技能模块”和一个预算对齐的基线公平比 | —（反证） | WebArena 475 任务 + WorkArena-L1，Gemini 3 Flash：原版（预算对齐）50.74% / 71.9K tokens vs ASI 47.86% / 107.1K tokens——技能模块可以比它省下的还贵 | 预印本，ServiceNow AI Research + ÉTS Montréal + UBC + McGill |

### 1.3 能调 API 就不点界面

| 文献 | 思路 | 改的环节 | 效果和条件 | 来源类型 |
| --- | --- | --- | --- | --- |
| AXIS（Lu et al., 2025）\[E161；D92\] | API 优先：能用应用 API 完成的就不走界面序列；agent 自己探索应用来扩充 API 集 | I-1（一次 API 调用抵多步点击）、IV-2 | 50 个 Word 任务上对比界面 agent UFO：59.5 → 29.9 秒（约 2 倍），3.2 → 2.0 步，$0.4 → $0.2，成功 52% → 84%；20 人、5 个 Word 任务的用户研究里比人手动快 65–70%。只有一个应用 | 会议论文（ACL 2025），Microsoft |
| ComputerRL（Lai et al., 2025）\[D93\] | 统一的 API–GUI 动作空间（自动为应用建 API），大规模在线 RL 训练 | I-1 | 框架消融（提示模型，不是 RL 训练后的 agent）：API–GUI 26.2% vs 只 GUI 11.2%；论文说“最多只需最强基线 1/3 的步”，但 v2 全文没有任何步数表 | 会议论文（ICLR 2026 poster），Tsinghua + Z.AI |
| UFO2（Zhang et al., 2025）\[E94；D46\] | Windows 桌面 agent：GUI 控制加原生应用 API；一次调用可以执行多个动作，每个动作前用 OS API 验证 | I-1、I-2 | GUI-only → GUI+API（o1）：Office 任务 16.0 → 6.6 步，成功 16.3% → 24.5%；多动作：OSWorld-W 6.80 → 3.30 步（24.5% → 26.5%）。步数不是 wall-clock；“最多低 51.5% 推理成本”是作者声称 | 预印本 v2，Microsoft（dossier 记为 TMLR 2026，待核） |
| Beyond Browsing（CMU, 2025）\[§3.1\] | API 和浏览混合的 agent | I-1 | WebArena 38.9%，比纯浏览 +24.0 pp；步数没量化 | 会议论文（Findings of ACL 2025） |

### 1.4 一次调用做多个动作

| 证据 | 思路 | 改的环节 | 效果和条件 | 来源类型 |
| --- | --- | --- | --- | --- |
| OSWorld 2.0 的批量动作设置（XLANG Lab, 2026）\[E6；D46\] | 一次模型调用输出一串动作，连续执行后再观察 | I-2 | 同一批 108 个任务：Opus 4.8 批量 20.6% vs 单动作 18.5%；Opus 4.7 批量 18.2% vs 13.9%；步数 Opus 4.7 从 318 降到 160.7，Opus 4.8 批量 103 步（481.8 次调用）。没有 wall-clock | 预印本，香港大学 XLANG Lab |
| UFO2 多动作消融（见 1.3） | 同上，但每个动作前用 OS API 校验 | I-2 | OSWorld-W 6.80 → 3.30 步，24.5% → 26.5%；WAA 9.95 → 8.85 步，25.3% → 24.7% | 预印本，Microsoft |
| SPACE（Yang et al., 2026）\[§3.1\] | 训练 agent 输出变长的动作块 | I-2 | ALFWorld unseen / Qwen3-4B：模型回合 21.7 → 4.4（约 −79.7%），成功 72.7% → 96.9%。文字环境；回合不是 wall-clock；Gemini 说的“EMNLP 2026”没有依据 | 预印本，Rutgers 等 |
| 上限：OSWorld-Human 的人类轨迹（Abhyankar et al., 2026）\[§3.8\] | 人把动作分组后，LibreOffice Calc 任务只要 4.5 步，单动作要 13.2 步 | — | 这是“一次调用多个动作”能省多少圈的上限估计；代价是不重新观察就行动，可能按过期状态操作（I-5） | 会议论文（MLSys 2026） |

### 1.5 厂商的录制回放，失败时叫模型修

这是企业自动化厂商（RPA 公司和浏览器 agent 公司）在 2026 年的默认做法，思路分三步：

1. **录**：第一次做任务时，把每一步点了哪个元素记下来（记的是元素的选择器、XPath 或一段代码）。这一次可以是人操作，也可以是模型操作。
2. **回放**：以后再做同样的任务，直接按记录重放，不调模型。所以正常情况下一次模型调用都没有（步数多、调用多这两类原因全消）。
3. **失败了叫模型修**：页面改版、元素找不到时，才把当前页面交给模型，让它重新找元素或重做这一步；有的产品会把修好的选择器写回记录，下次就不用再修。

各家产品只在细节上不同（追加调查 3，E139–E160）：

| 产品 | 录什么 | 怎么发现回放失败 | 失败了谁来修 | 修好后写回记录？ |
| --- | --- | --- | --- | --- |
| UiPath Healing Agent | 选择器 | 事后：元素在超时内没找到 | 8 种确定性策略加 AI 策略逐个试 | 可选 |
| Microsoft Power Automate（self-healing / Repair with Copilot） | 选择器 | 事后：元素或窗口没找到 | GPT-4.1 mini + Claude Sonnet 4.5 看截图重新找元素 | 可选（“save the repaired selector”） |
| Automation Anywhere Generative Recorder | 选择器 | 事后 | 模型重新找元素 | 可选（DOMXPath “Update value”） |
| Browserbase Stagehand 缓存 | 模型上次选的动作 | **事前**：回放前先比对页面指纹（DOM 哈希），变了就不回放 | 完整 agent 重做这一步并刷新缓存 | 是 |
| Skyvern 代码缓存 | 生成的代码 | 事后：遇到意外页面 | 完整 agent 重跑 | 是 |
| Hyperbrowser HyperAgent 动作缓存 | XPath | 事后：重试 3 次仍失败 | 用缓存的指令叫模型 | — |

做到什么程度，答案是“不知道”：没有一家发布过三个关键数字——回放成功率、修复成功率、每次成功的成本（E160）。能找到的只有营销话（Automation Anywhere “执行失败少 60% 以上”、Stagehand “第二次缓存运行最高快 80%”），按我们的规则不作来源。价格倒是一手资料：UiPath 每修一次收 3 个 Platform Unit（每年含 5,000 次）；Power Automate 的自动修复不另收费（需 premium 许可）；Browserbase 每浏览器小时 $0.10–0.12。研究界有一篇声称“99% 成功、省 99% token”的系统论文（LOOP），按零节的来源规则已撤下、不作来源，原因见第五节。所以这一条的结论是：“回放 + 失败叫模型”这个机制本身已经是商品，不新鲜；但它到底多可靠、多便宜，公开资料里没有任何测得的数字。

### 路线一做到哪了

- 在重复任务上，编译 / 重放能把时间压到 1/2.4 到 1/14（SkillDroid 2.4 倍、Agent JIT 9.7 倍、GPA 约 10 倍、AutoDroid-V2 约 14 倍），把钱压到 1/10 以下（ActionEngine $0.71 → $0.06），准确率不降反升。但样本小（16–106 个任务）、多为单次运行、不少只报步数或推理时间而非 wall-clock、离线建工具的成本不计。
- 在公开的 computer-use benchmark 上做带守卫的 GUI 轨迹重放，只有 EchoPath 一篇（预印本），且没有测界面变化后的重放成功率——这是作者自己写明的。
- “能调 API 就不点界面”是最干净的少转圈（AXIS 约 2 倍，会议论文），前提是应用有 API。
- 厂商产品已把“回放 + 失败叫模型”当默认，但不发布任何测得的成功率和成本。

## 二、路线二：每次调用更快、更便宜

这条路线不减少模型出场的次数，而是让每一次出场读得少、写得少、或者换一个更便宜的模型、更快的档位、更聊明的推理服务器。它对应第一份文档里“每次调用慢（III）”的四条，和贵的前两类加单价。六种做法。

### 2.1 缓存提示前缀（读的那一段不重算）

原理：连续几次调用的提示开头都一样（system prompt、工具定义、前面的历史），提供商把这一段的中间结果（KV cache）存下来，下次直接用，读的单价打一折、首 token 等待缩短。不改任何输出，所以是“无损”的。改的环节：读得多（III-2）和读的 token 钱（贵的第一类）。

| 文献 | 思路 | 效果和条件 | 来源类型 |
| --- | --- | --- | --- |
| Don't Break the Cache（Lumer et al., 2026）\[§3.2\] | 在长任务 agent 会话上实测三家提供商的提示缓存，并总结怎么用才不把缓存打掉 | 500 多个 DeepResearch 会话、10K token 的 system prompt，OpenAI / Anthropic / Google：成本 −41–80%，首 token 等待 −13–31%；天真地把全部上下文都标成缓存反而可能变慢；工具返回的动态内容要排除在缓存块之外 | 预印本，PricewaterhouseCoopers（PwC）——工业测量，未经同行评审，未见复现；所以只当“缓存能省这个量级”的一手测量，不当精确数 |
| TraceLab 仪表盘（Zhu et al., 2026）\[E187\] | 反事实估算：如果在人思考的间隙里也把前缀缓存留住，能省多少 | 665,453 步、8,058 个 session、52 个用户的 Claude Code / Codex 真实记录：“最终成本省 15.8%”，是上限估计，不是部署系统 | 第三方实测数据的反事实估算，University of Washington |
| 提供商文档（Anthropic, 2026b；OpenAI, 2026）\[E83、E84\] | 缓存的规则：前缀必须逐字相同；中途改 system prompt 或工具定义、切换 fast mode 都使缓存失效 | 缓存读 0.1 倍价，写入 1.25 倍；这也是为什么“裁历史”和“缓存”两个手段会互相打架 | 厂商文档 |

### 2.2 裁掉页面里无关的部分（观察裁剪）

原理：文本型 web agent 每步要读整个页面的 AXTree 或 DOM，其中大部分和当前一步无关；用一个小模型或一段程序先挑出相关的行，再给大模型。改的环节：III-2、贵的第一类。

| 文献 | 思路 | 效果和条件 | 来源类型 |
| --- | --- | --- | --- |
| FocusAgent（Kerboua et al., 2026）\[§3.5；D48、D58–D60\] | 一个小的检索模型从 AXTree 里选出与任务相关的行，只把这些行给执行模型 | 执行模型 GPT-4.1，输入 token 成本按整个 benchmark 求和（330 个 WorkArena L1 回合 / 381 个 WebArena 任务）。用 GPT-4.1-mini 做检索：WorkArena L1 裁掉 51%，成本 $55.6 → $45.1（−19%），成功率 53.6% → 51.5%；WebArena 裁 59%，$59.0 → $44.0，36.5% → 32.3%；每步延迟 2.5 → 10.1 秒（变慢）。用 GPT-5-mini 做检索：WorkArena −31% 成本、53.6% → 53.2%；WebArena −21.7% 成本、36.5% → 39.6%。粗暴地截断到 5k token：成本 −49%，但 53.6% → 44.5%。成本只算输入；效果的正负取决于检索器（v1 只有 4.1-mini，v2 加了 5-mini） | 期刊论文（TMLR 2026，arXiv v2 2026-08-29），ESKER + INSA Lyon + ServiceNow Research + Mila |
| Prune4Web（Zhang et al., 2025）\[§3.5\] | 让模型写一段 Python 打分脚本去过滤 DOM 候选，而不是读整个 DOM | 10 万 token 的 DOM 压到不到 20 个可操作候选（25–50 倍）；定位准确率 46.8% → 88.28%——是准确率提升，不只是省 | 会议论文（AAAI 2026，AAAI 官网论文页 40772）；作者机构未在 arXiv 页列出 |
| Revisiting Observation Reduction for Web Agents（Enomoto et al., 2026）\[§3.5；D146\]——即 dossier §3.5 里的“Minimal Failure Set / GEPA pruning”，那里误署为 Agrawal et al.；GEPA 只是它用的优化器（Agrawal et al., 2025） | 用进化算法找“去掉就会失败”的最小 HTML 子集，只保留它 | WorkArena L1 的 33 个任务：每步延迟快 2.2 倍、保留原成功率的 84%；WebLinx 测试集抽样的 300 个任务：快 3.1 倍、保留 89%。agent 模型 Qwen3.5-122B-A10B（另有 MiniMax-M2.5），基线是不裁剪的同一 agent；量的是每步延迟，不是每任务 wall-clock。单一来源，未复现 | 预印本，NEC Corporation（arXiv:2605.29397v1，2026-05-28，作者与机构已在 arXiv 页核过） |
| AgentOccam（2025）\[§5.3\] | 精简观察和动作空间 | WebArena +26.6 pp；是裁剪类方法的常用基线 | 会议论文（ICLR 2025） |

### 2.3 裁掉或压缩历史（包括历史截图）

原理：第 k 步不必带着前 k−1 步的全部内容；把旧的观察遮掉、把历史截图降分辨率或只保留结构锚点。这是直接对着“读随步数平方增长”去的。改的环节：III-2、贵的第一类。

| 文献 | 思路 | 效果和条件 | 来源类型 |
| --- | --- | --- | --- |
| The Complexity Trap（Lindenbauer et al., 2025）\[§3.5\] | 把旧的观察直接遮掉，而不是让 LLM 总结 | SWE-agent + Qwen3-Coder：每个实例 $1.29 → $0.61（−52.7%），解决率 53.4% → 54.8%；不做任何上下文管理时成本可能翻倍以上 | 研讨会论文（NeurIPS 2025 DL4Code workshop），JetBrains Research + TU Munich |
| AgentDiet（Xiao et al., 2026）\[§3.5\] | 删掉轨迹里无用、重复、过期的内容 | 输入 token −39.9–59.7%，总成本 −21.1–35.9%，成功率 −1 到 +2 pp；约 $2,000 实验花费；作者因为 API 延迟不稳故意不比延迟；并指出删历史会使 KV 缓存失效 | 会议论文（FSE 2026，PACMSE），Peking U + ByteDance |
| TokenPilot（Xu et al., 2026）\[E174\] | 知道提供商前缀缓存规则的压缩：稳定前缀、占位符、按生命周期逐出 | API 美元成本 −61% / −56%（孤立）和 −61% / −87%（连续），PinchBench / Claw-Eval，GPT-5.4-mini；准确率 80.5 → 81.0 / 64.5 → 63.1 等，小幅波动 | 预印本，Zhejiang U + UESTC + Xidian + HomologyAI（作者与机构已在 arXiv 页核过） |
| 视觉 token 压缩一类：SimpAgent（ICCV 2025）、GUIPruner、TRACE、AQuaUI、GUI-KV \[§3.5\] | 遮掉截图里无关区域、降低历史截图分辨率、按四叉树合并视觉 token | SimpAgent：Qwen2-VL-2B 计算量 −27%，AITW 步准确率 69.0% → 71.3%；GUIPruner：编码 3.3 倍、prefill 1.9 倍快，步准确率 69.5% → 65.3%；TRACE：首 token 1116.8 → 452.7 ms，步成功 52.45% → 48.91%。都是本地小模型、单步指标；多数有小幅掉点 | SimpAgent：会议论文（ICCV 2025），HIT 深圳 + 华为诺亚方舟实验室；GUIPruner：预印本，清华深圳 + 西安电子科技大学 + 港中文；TRACE：预印本，大连理工 + OPPO 研究院 + 港理工；AQuaUI：预印本，UC Davis；GUI-KV：预印本，Salesforce AI Research + UCLA。五篇的作者与机构都在 arXiv 页核过 |

### 2.4 换便宜的模型：小模型、按步路由

原理：大多数步不需要最强的模型；要么训一个专门的小模型替掉大模型，要么每步先让小模型试、卡住了再叫大模型。改的环节：III-3、III-4、单价（贵的第五类）。

| 文献 | 思路 | 效果和条件 | 来源类型 |
| --- | --- | --- | --- |
| StepWise（Wei et al., 2026）\[§3.5；D47\] | 每步先用 8B 小模型，配一个“卡住监测器”和“里程碑监测器”，必要时升级到大模型 | OSWorld：EvoCUA-8B + 选择性的 Claude Sonnet 4.5 vs 全程 Sonnet 4.5：$0.881 → $0.224 / 任务（−74.6%），每次请求 6.4 → 4.1 秒，成功率 58.1% → 55.4%；EvoCUA-8B + Kimi K2.5 vs 全程 Kimi：$0.132 → $0.051，8.3 → 4.5 秒 / 请求，60.1% → 58.2%。摘要里的“最多 −74.6% 成本 / 最多 −45.8% 延迟”来自不同配置；计时是每次请求不是每个任务 | 预印本，Yale NLP + UNC |
| Fara-7B（Awadallah et al., 2025）\[§3.5；D54\] | 用合成的网页轨迹训一个 7B 的纯截图模型，整个替掉前沿模型循环 | WebVoyager：对比 OpenAI computer-use-preview，每任务 $0.025 vs $0.913（约 36 倍，calc.），16.5 vs 38.0 个动作，73.5% vs 70.9%；但 Browserbase 的独立人工核验只得 62%；Online-Mind2Web 34.1%（computer-use-preview 42.9%）。成本按 OpenRouter 最便宜的 7B 价格估算，无缓存，无 wall-clock | 预印本，Microsoft |
| WebRouter（Li et al., 2025）\[§3.5\] | 按查询难度选模型的路由器（变分信息瓶颈） | Browser-use，5 个 WebVoyager 站点：$0.98 → $0.12 / 任务（−87.8%），成功率 86.1% → 82.3%（步数变多） | 预印本（页首写“在审 ICASSP 2026”），NUAA 等 |
| Budget-Aware Agentic Routing / BoPO（Zhang et al., 2026）\[§3.5\] | 在“大模型调用次数上限”下训练逐步大 / 小路由 | AppWorld，上限 15 次：全用大模型超预算 25% → BoPO 用 88%，成功率 66.7% → 66.5%。路由器自身开销不计 | 预印本，Cambridge + Microsoft |
| RouteLLM（Ong et al., 2024）、FrugalGPT（Chen, Zaharia & Zou, 2023）\[§3.5\] | 单轮问答的路由 / 级联 | 最高 3.66 倍成本节省保 95% GPT-4 质量。不是 agent 循环 | 会议论文（RouteLLM：ICLR 2025，UC Berkeley 等）；期刊论文（FrugalGPT：TMLR 2024，Stanford） |

### 2.5 控制思考长度和提前停

原理：写的 token 里很大一块是“思考”，很多步不需要那么多；按步选推理强度，或者发现在空转时早点停。改的环节：III-3、III-4、I-4、贵的第二类和第四类。

| 文献 | 思路 | 效果和条件 | 来源类型 |
| --- | --- | --- | --- |
| Ares（Yang et al., 2026）\[§3.7；D49\] | 一个 Qwen3-1.7B 的路由器每步给 gpt-oss-20b 选最低够用的推理强度（低 / 中 / 高） | WebArena（AgentOccam，约 129 个任务）：固定高强度 → Ares，推理 token 21,424 → 11,723 / 任务（−45.3%），成功率 45.0% → 46.5%；TAU-Bench Retail −35.3% token、成功率不变。但一律用低强度：Retail −19.8 pp、WebArena −7.6 pp——要自适应地减，不能一刀切。没有 wall-clock | 预印本，UCSB + Accenture |
| The Danger of Overthinking（Cuadron et al., 2025）\[§3.7\] | 给轨迹打“过度思考”分，低强度多采样、留最不过度思考的那条 | o1 在 SWE-bench Verified：$800 vs 高强度 $1,400（−43%），27.3% vs 29.1%；采 3 次后 30.3% 且只要 $1,200（又好又便宜） | 预印本，Berkeley + ETH + UIUC + CMU |
| Efficient Agents（Wang et al., 2025）\[§3.7；D9\] | 调步数上限、重规划、搜索宽度、采样 | GAIA：OWL → Efficient Agent $0.398 → $0.285 / 任务，53.33% → 51.52%；摘要里的 $0.228 只是 Level-1 | 预印本，OPPO |
| 厂商的 effort 旋钮（E81、E88） | 提供商自己的数据 | Anthropic：中等 effort 约为高 effort 一半的输出 token，重试后最终成功相同；Opus 4.5 中等 effort 以少 76% 输出 token 追平 Sonnet 4.5 最佳 SWE-bench。跨代比较，没有同模型在 agent benchmark 上的消融 | 厂商文档 |

### 2.6 买速度档，或专门为 agent 做的推理服务系统

两件事。一是花钱买速度：Anthropic 和 OpenAI 的 fast mode 一律 2 倍价、厂商自述输出速度最多 2.5 倍、不改首 token 等待（Anthropic, 2026b \[E190\]；OpenAI, 2026 \[E192\]）；OpenAI 的 Ultrafast（Cerebras 硬件）声称最多 14 倍，预览、没有公开价格 \[E194\]；Google Priority 加价 75–100%。这些只提“写”的速度（III-3），没有第三方测过端到端的任务时间 \[E209\]。产品侧的同类动作：Claude in Chrome 曾把默认模型换成更小的 Haiku 4.5（2025-10-15），Google 把 computer use 放进 Flash / Flash-Lite \[E210、§1.7\]——厂商自己也在用“换小模型”这条。

二是推理服务系统（自己部署模型时才用得上）。原理：agent 的一次调用结束后要等工具跑完才有下一次，普通服务器在等待期间把它的 KV 缓存逐出，下次得重读；这些系统把“整个 agent 程序”当调度单位，等工具时把缓存留住或按预测预取。改的环节：III-2（负载高时的重读）、III-1。

| 系统 | 思路 | 效果和条件 | 来源类型 |
| --- | --- | --- | --- |
| SGLang / RadixAttention（Zheng et al., 2024）\[§3.6\] | 用基数树精确共享前缀，跨调用和分支复用 | 在其 LM 程序套件（含 agent 轨迹）上吞吐最高 6.4 倍、单程序延迟 3.7 倍低。精确复用，任务成功率变化没报 | 会议论文（NeurIPS 2024），Stanford + Berkeley |
| InferCept（Abhyankar et al., 2024）\[§3.6\] | 工具中断时按预期浪费决定 KV 保留 / 换出 / 丢弃 | 1.6–2 倍服务负载；在此之前 KV 重算占前向时间 37–40% | 会议论文（ICML 2024），UCSD |
| Agentix（Luo et al., 2026）\[E185\] | 按“程序已获得服务量”调度，可抢占，按缓存位置路由 | “同样延迟下”程序吞吐 4–15 倍于 vLLM 类系统（15 倍是 Mixed 负载的最大值）；LLaMA-3.1 8B/70B、Falcon-180B，1–8 张 A100；延迟定义是“程序响应时间 ÷ 生成 token 数”；准确率没报；无代码链接 | 会议论文（NSDI 2026），Berkeley + Google DeepMind + SJTU |
| Continuum（Li et al., 2026）\[D61、D129\] | 工具调用期间给 KV 缓存一个成本感知的“存活时间”，加程序级先来先服务 | 受控的轨迹回放（SWE-Bench / BFCL / OpenHands，Llama-3.1 8B/70B、Gemma-3 12B，A100/H100/B200）：延迟低 1.12–3.66 倍、吞吐 1.10–3.22 倍；摘要的“>8 倍”是真实 SWE-agent 上的最好情况（500 个任务，合作方 H100）。两个数都在 v7 里；通过率“高于基线”因为基线超 15 分钟算失败 | v7 页首标 PVLDB Vol. 20（期刊论文，待核），Berkeley + Stanford + Tsinghua |
| ThunderAgent（Kang et al., 2026）\[E108、E186\] | 把“LLM 程序”当调度单位，统一管 KV 缓存、工具资源（磁盘、端口）和阶段 | 96 个并行程序下步吞吐 1.48–3.58 倍于 vLLM、1.17–3.31 倍于 Continuum（GLM-4.6 355B、Qwen-3 235B，8×H100；SWE-bench Lite 等）；Continuum 自己的微基准里排序相反（D129） | 会议论文（ICML 2026 poster），Georgia Tech + UIUC + CMU + Together AI |
| CacheScout（Zhang et al., 2026）\[E172\] | 在线学 agent 的执行转移，用来指导逐出和预取 | 对比 vLLM（LRU）和 Continuum：命中率 +10–18 pp，首 token 等待 −18–45%，每轮延迟 −29–38%；Llama-3.1-8B 在 8×RTX PRO 6000；任务质量没报；代码未放 | 预印本，UC Santa Cruz + U Washington + UChicago |
| KVFlow（Pan et al., 2025）\[§3.6\] | 按“距离下次执行还有几步”逐出，CPU → GPU 预取 | 合成负载 1.83 倍 / 2.19 倍；真实的 PEER Financial-QA 只有 1.08 倍 | 会议论文（NeurIPS 2025），UCSD |

一句要紧的话（追加调查 5 逐篇核过 15 个系统）：**没有任何一个 agent 推理服务系统在 GUI / computer-use 负载上评测过**——它们用的是 SWE-bench、BFCL、GAIA、ShareGPT、ToolBench 这类代码和工具负载；15 个里只有 3 个报了任务质量的变化，6 个放了代码；各家的倍数基线和硬件不同，不能互比 \[E172–E186；§3.6\]。

### 路线二做到哪了

- 缓存是最确定的一项：无损、厂商已提供、实测省 41–80% 成本；但它和“裁历史”、“切速度档”、“改工具定义”互相打架，而且截图型 agent 的测量都没报缓存状态。
- 裁观察、裁历史、换小模型、控思考，各自能省 20–75% 的钱，代价是 0 到 4 个点的准确率，而且省幅常小于裁剪幅（FocusAgent 裁 51% 只省 19%）、有时反而变慢（FocusAgent 每步 2.5 → 10.1 秒）。一刀切的做法（粗暴截断、一律低思考）都会明显掉点。
- 专门的服务系统在代码 / 工具负载上有 1.1–3.6 倍的受控结果（更大的倍数是最好情况或合成负载），但没有一个在 GUI 负载上测过。

## 三、路线三：把等待重叠起来

这条路线不减少工作量，而是让环境和模型同时干活，直接对着第一份文档里的“串行（第五类）”和“环境慢（IV）”。它不省钱，往往还多花钱（猜错的那些调用照付），换的是时间。三种做法，再加一个绕不过去的安全问题。

### 3.1 猜下一步先做（speculation）

原理：大模型在想的时候，用一个便宜的预测器猜它下一步会做什么，先把那一步的工具调用或页面加载跑起来；大模型想完后如果和猜的一致，结果直接用，不一致就丢掉。和处理器的分支预测、LLM 的 speculative decoding 是同一个思路。改的环节：串行（第五类）、IV-2、IV-4。

| 文献 | 思路 | 效果和条件 | 来源类型 |
| --- | --- | --- | --- |
| Speculative Actions（Ye et al., 2026）\[E126；D51\] | 预测器提前发出候选动作，只在权威模型同意时提交；只允许幂等、可逆或沙箱内的副作用；证明了单步推测最多只能省 50% 的延迟 | 国际象棋 + GPT-5，3 个分支：平均执行时间 −19.5%，预测准确率 54.7%；电商任务里 22–38% 的 API 调用被正确预测；HotpotQA 最高 46% top-3（这些是命中率，不是加速）；没有报副作用事故（“没报”不等于“测到零”） | 会议论文（ICLR 2026 Oral），Columbia |
| Interactive Speculative Planning（Hua et al., 2025）\[§3.3\] | 一个快的近似 agent 先起草 4 步，目标模型并行验证，用户可打断 | OpenAGI：182.70 → 105.42 秒（−42.30%，MAD 目标）；但成本 $0.2160 → $0.2973，4–5 个并发 API 调用；TravelPlanner 用模糊匹配时常识微通过率 48.6% → 41.7% | 会议论文（ICLR 2025），Microsoft + Rutgers |
| Dynamic Speculative Agent Planning（Guan et al., 2026）\[§3.3\] | 用在线 RL 学“推测多深” | OpenAGI：延迟 −37.09%，成本 +62.99%（相对顺序执行）；比固定深度 6 同样延迟但成本低 34.9%；任务成功率变化没报 | 会议论文（ICLR 2026），JHU + UCSB + Google DeepMind 等 |
| PASTE（Sui et al., 2026）\[E127；D13、D63、D64\] | 挖出反复出现的工具调用模式（比如 Edit 后必 Verify，Search 后必 Visit），提前执行，精确匹配就采纳；工具和模型联合调度 | v3：平均任务完成时间最多 −43.5%，p99 最多 −55.4%（v1 写 −48.5%，版本间改过）；>20,000 个推测动作里 602 个可能有副作用的被拦下，没有任务结果改变；本地 Qwen 30B 在 4×8 A100。工具型 agent，不是 GUI | 预印本 v3，SJTU + Microsoft Research + Stevens |
| Speculative Macro Commit（Liu, Kundu, Beerel, 2026）\[E124、E125\] | 把反复出现的多步骨架挖成隐藏的宏库；小草稿模型在隔离的草稿状态里预执行；主模型的第一步一旦匹配就把后缀整段提交 | τ²-bench Telecom：27.60 → 22.47 秒（−18.59%）、成功率不变；AppWorld：355.7 → 195.9 秒（−44.93%）、成功率 −1.19 pp；提交率 86.2% / 62.0%；光靠宏库匹配只有 34.6% 能复现真实后续步，所以必须有守卫；顺序版 1 张 GPU vs 推测版 3 张；Qwen3.5-27B + 4B 草稿。需要能隔离的草稿状态 | 预印本，USC + Intel Labs |
| AOSpec（Chen et al., 2026）\[E123\] | 同时推测下一步动作和它的观察结果；推测动作在写时复制的文件系统分叉里跑，动作和起始状态都匹配才提交 | Terminal-Bench（4 个框架、5 个模型）：平均端到端延迟 −11.8–32.5%，p99 最多 −42.8%；观察预测精确命中 33.3%；非文件系统的副作用一律不推测 | 预印本，Imperial College London |
| SPORK（Bai et al., 2026）\[E128\] | 不用额外模型：把目标模型自己的 KV 缓存分叉，在推理继续的同时先发一个探针工具调用；只探只读工具，写操作一律串行 | GAIA（Qwen3-32B）：p95 131.9 → 108.1 秒（−18%），p50 −10%；τ²-bench 1.09–1.18 倍；每轮采纳率约 0.37。需要能拿到 logprob 的开源引擎，闭源 API 用不了 | 预印本，Tsinghua + Meituan |
| Speculate with Memory（Li et al., 2026）\[§3.3\] | 用转移表 + 情节记忆 + 混淆跟踪器来做预测；精确匹配才提交；只读白名单 | 动作预测准确率相对 +19–39%；ALFWorld 估计延迟下降 28% → >50%；HotpotQA 实际只省 1.05 倍（分析值）。不是六个 benchmark 上实测的 wall-clock | 预印本，Salesforce |
| Skim / Accio（Wong et al., 2026）\[E17；§3.2\] | 离线给每个站点建“档案”（URL 模板、答案结构）；运行时直接合成 URL 跳过导航，小模型抽取，验证器把关，不行就回退到带热启动的 ReAct | WebVoyager、WebShop（三个文本型 agent 后端）：中位成本低 1.9 倍，延迟 −33.4%，准确率不掉；手工优化的程序能快 66.7–94.9%；天真地换便宜模型成功率 −60%。只读的信息检索任务 | 预印本，Princeton + Microsoft Research |

### 3.2 多个工具并行，模型一边写一边让工具先跑

原理：一步里如果要调好几个互不依赖的工具，不必一个一个等；或者模型写到一半就把已确定的工具调用发出去。改的环节：串行、IV-4。适用范围：搜索、检索这类独立调用；GUI 动作通常前后依赖，并行不起来。

| 文献 | 思路 | 效果和条件 | 来源类型 |
| --- | --- | --- | --- |
| LLMCompiler（Kim et al., 2024）\[§3.4\] | 规划器先把函数调用画成依赖图，执行器并发发出 | Movie Recommendation / GPT-3.5：ReAct 20.47 → 5.47 秒（3.74 倍），每千任务 $20.46 → $3.04，准确率 72.47% → 77.13%；HotpotQA 最高 1.80 倍。其他任务有小幅回退 | 会议论文（ICML 2024），UC Berkeley |
| AsyncFC（Feng et al., 2026）\[§3.4\] | 工具调用立即返回一个 future，模型继续写，到依赖点再等 | 组合 HotpotQA 1.24 倍（75.0% → 75.0%）；BFCL-v4 Web Search 1.26 倍（54.8% → 53.2%）；样本小，部分实验人为注入工具延迟 | 预印本，UC Berkeley（v1，2026-05-14） |
| AsyncLM（Gim, Lee, Zhong, 2024）\[§3.4\] | 模型不停地生成，工具完成时中断它 | BFCL 600 样本：端到端 1.6–5.4 倍于同步。云端延迟是模拟的（每输出 token 5 ms） | 预印本，Yale（v1，2024-12-09；页首自述“初步工作，在审”） |
| W&D: Scaling Parallel Tool Calling（Lin, Liew, Savarese & Li, 2026）\[§3.4\] | 每轮多发几个原生工具调用，控制深度 | BrowseComp 前 100 题（GPT-5-medium），每轮 1 → 3 个工具：1,522.6 → 904.2 秒（−40.6%），$102.5 → $65.7，66% → 68% | 预印本，Salesforce AI Research（v1，2026-02-07） |

### 3.3 等页面的时间：预加载、事件驱动代替固定停顿

这是针对文本型 web agent 的大头（IV-2、IV-3）最直接的一条，但我们的证据里几乎没有专门的测量：Skim 的 URL 合成是“跳过导航”（见 3.1）；SpecBox（2026）预分配沙箱、让 p99 会话延迟低到 1/2.9，但对象是 MCP 工具服务器不是浏览器 \[E176\]；Signal-Driven Observation（Gaur & Lane, 2026，UC Santa Cruz）提出只在有信号时才重新观察，但该文自述不含任何实验，只算提法、不算证据 \[§3.5\]。“用页面就绪事件代替每步固定停 2–3 秒”这件事，没有找到专门测过的工作——这是一个窄而具体的空白，不是“没人研究过加速”。

### 3.4 绕不过去的问题：猜错了怎么撤销（在真实网站上）

推测要成立，前提是猜错的那一步能当作没发生。在本地文件系统或模拟器里可以快照、分叉、回滚；在真实的 SaaS 网站上，一次点击发出的 POST 到了对方服务器，收不回来。追加调查 2 把 2026 年的工作按“靠什么保证安全”分五类（E113–E138）：

| 机制 | 代表工作 | 它假设什么 | 在无法快照的真实 SaaS 上行不行 | 实测的安全数据 |
| --- | --- | --- | --- | --- |
| 分叉 / 快照环境 | TClone（Huang et al., 2026，UCSD）\[E121\]、DeltaBox（Dong et al., 2026，SJTU + Huawei）\[E122\]、AOSpec、SMC 的草稿状态 | 本地状态能复制；TClone 分叉时关掉对外连接，DeltaBox 明写“不支持网络 I/O 回滚” | 不行：服务器端状态复制不了；本地浏览器能分叉，但分叉里的请求会真的发到服务器 | TClone：总任务延迟比 KVM / CRIU 低 1.9 / 1.5 倍，但没有推测命中率和任务成功率；DeltaBox：检查点 ≈10.83 ms、回滚 ≈1.86 ms，无任务质量指标 |
| 只读 / 白名单推测 | SPORK、Skim、Speculate with Memory | 推测的调用不改状态 | 对状态行；对可观测性和负载不行 | Ghost Tool Calls（Mohammadi et al., 2026，MPI-SWS + EPFL + Aarhus）\[E129、E130\]：被放弃的推测调用在发出时就被提供商看见；只读限制泄露的意图和不限制一样多（0.97 vs 0.97）；推测把提供商调用量变成 4.03 vs 1.03 每任务（约 3.9 倍，calc.） |
| 先暂存，确认后才放出（commit barrier） | Cordon（Chen et al., 2026，Tsinghua + SJTU）\[E117–E120\]、Atomix（Mohammadi et al., 2026）\[E113–E116\]、PASTE 的 dry-run | 效果能被扣住稍后再放：运行时自己的发件箱，或一个暂存资源 | 只在网站自己提供暂存态时行（未保存的表单、已保存未提交的草稿；推断）；一次会发 POST 的点击扣不住 | Cordon：45 个作者自建的高风险工作流全部在提交前拦下（45/45 vs 现有防御 14 拦 / 26 漏），代价时间 +22.7%；没有 web / GUI 工作流。Atomix：500 次无效发送里门控提交泄漏 0/500 |
| 事后补偿 | Atomix 的可逆类、Speculative Actions 的修复路径、Revisable by Design（模拟工具）、RAC | 存在语义上的逆操作，且效果日志不会被回滚抹掉 | 只对可补偿的动作行（删一行草稿）；对提交、审批、付款这类不可逆动作不行 | Atomix：Saga 式补偿泄漏 400/500（80%），检查点重放 200/500；Safe to Resume（Wu et al., 2026）\[E136\]：常见框架的回滚会抹掉对外效果的记录，两种提交顺序在 90/96 和 93/96 个微基准上失败，能导致重复付款 |
| 行动前先分类（门控） | WebOperator（Dihan et al., 2025，BUET + Monash + QCRI）\[E133；D104\]、AAPT、EchoPath 的起始状态门、SMC 的 API 名规则 | 一个谓词能判断这一步可不可以提前做 | 行，而且上面每一行都需要它；但现有的精度低 | WebOperator 把按钮当潜在破坏性、链接当安全，事后按 GET / POST 判定：预判为破坏性的动作只有约 37% 真的是；EchoPath 的门错放 22% 的不兼容起始状态 |

三个 2026 年的结果把设计空间定了边：放出前门控胜过事后补偿（Atomix 0% vs 80% 泄漏）；只回滚 agent 自己这侧会抹掉对外效果的记录（Safe to Resume）；“只读”推测不是隐形的（Ghost Tool Calls）。**没有任何一篇在真实的、不能分叉的商业 SaaS 后端上评测过推测**，也没有任何一篇同时报了 web 界面动作的可逆性分类、推测命中率、准确率影响和副作用事故——这两句是从这些工作自己声明的范围里推出来的（§3.3、§5.4 (b)）。

### 路线三做到哪了

- 在工具型 agent（搜索、终端、API）上，推测能省 12–45% 的任务时间，其中两篇是 ICLR 论文（Speculative Actions、DSP），代价是多花 30–60% 的钱（ISP、DSP）或多用 GPU（SMC）；单步推测的理论上限是省 50%。
- 并行工具在独立调用多的任务上有 1.2–3.7 倍，对前后依赖的 GUI 动作基本无效。
- 在 GUI / 真实网站上，推测只有只读的（Skim）和本地可分叉的（TClone、AOSpec）；对会改服务器状态的点击，没有人做过，且已知的补偿、回滚、只读三条路各有实测的漏洞。

## 四、做到什么程度了

总表只收“进了会议或期刊”或“在公开 computer-use / web benchmark 上有完整数字”的工作，每行一个最能代表它的数。全部细节在前三节。

| 文献 | 路线 | 改的环节 | 代表性效果 | 在什么上测的 | 来源类型 |
| --- | --- | --- | --- | --- | --- |
| Agent JIT（Winston et al., 2026） | 一 | I、II | • 每任务时间：150.1 → 15.4 秒（约 9.7 倍，calc.）<br>• 成功率：61% → 90% | • 在哪测：37 个 web 任务，5 个网站应用（从 REAL / WebArena 派生）<br>• 模型：GPT-4.1<br>• 基线：Browser-Use 框架跑同一模型<br>• 量的是：每任务 wall-clock 秒数和成功率<br>• 注意：离线建工具的时间不计 | ICML 2026 |
| AXIS（Lu et al., 2025） | 一 | I-1 | • 每任务时间：59.5 → 29.9 秒（约 2 倍）<br>• 成功率：52% → 84% | • 在哪测：Microsoft Word 里的 50 个任务<br>• 基线：界面 agent UFO，跑同一模型<br>• 量的是：每任务秒数、步数、美元和成功率<br>• 注意：只有一个应用 | ACL 2025 |
| ComputerRL（Lai et al., 2025） | 一 | I-1 | • 成功率：API–GUI 动作空间 26.2% vs 只用 GUI 11.2% | • 在哪测：OSWorld<br>• 设置：提示模型的框架消融，不是 RL 训练后的 agent<br>• 比的是：API–GUI 动作空间 vs 只用 GUI<br>• 量的是：成功率<br>• 注意：步数没有表，时间没有报 | ICLR 2026 |
| AWM（Wang et al., 2025） | 一 | I-1 | • 步数：7.9 → 5.9<br>• 成功率：15.0% → 35.5%<br>• 但：ASI 的受控复现里步数 5.9 vs 5.6，不减 | • 在哪测：WebArena<br>• 模型：GPT-4，AXTree 文本观察<br>• 基线：没有工作流记忆的同一 agent<br>• 量的是：平均步数和成功率<br>• 注意：ASI 在同设置下的受控复现里步数 5.9 vs 5.6，不减 | ICML 2025 |
| ASI（Wang et al., 2025） | 一 | I、II | • 步数：少 10.7–15.3%（5.0 vs 5.6）<br>• 成功率：40.4% vs 32.7% | • 在哪测：WebArena<br>• 比的是：同一 agent 有 / 无在线技能归纳<br>• 量的是：平均步数和成功率<br>• 注意：没有 wall-clock，没有美元 | COLM 2025 |
| WALT（Prabhu et al., 2026） | 一 | I-1、I-3 | • 步数：8.9 → 7.0<br>• 成功率：57.5% → 64.1% | • 在哪测：VisualWebArena 的 Classifieds 站点<br>• 模型：GPT-5-mini<br>• 基线：不带工具的同一 agent<br>• 量的是：平均步数和成功率<br>• 注意：步数不是时间 | ICLR 2026 |
| Agentic Plan Caching（Zhang et al., 2025） | 一 | II | • 成本：−50.31%（5 个负载平均）<br>• 延迟：−27.28%<br>• 准确率：GAIA / ODR 上 37.58% → 36.97%（−0.61 pp） | • 在哪测：5 个工作负载（含 GAIA 的 Open Deep Research、FinanceBench 等）<br>• 基线：不缓存计划的同一 agent<br>• 量的是：美元成本、延迟和准确率的平均变化<br>• 注意：命中后仍要一次小模型调用 | NeurIPS 2025 |
| AutoDroid-V2（Wen et al., 2025） | 一 | I、II | • 推理时间：669.2 → 46.3 秒 / 任务（−93.1%）<br>• 成功率：43.9% → 54.4% | • 在哪测：DroidTask（Android 手机任务）<br>• 基线：逐步调用 LLM 的 agent<br>• 量的是：推理时间（不是全流程 wall-clock）和成功率<br>• 注意：训练时间不计 | MobiSys 2025 |
| EchoPath（Zhao et al., 2026） | 一 | I、II | • 第二遍 token：中位 20,370 vs 586,386<br>• 第二遍时间：127.5 vs 315.7 秒<br>• 成功率：91.2% vs 91.8% | • 在哪测：OSWorld-Verified，第一遍跑出并筛选出 159 条可执行记忆，第二遍重放<br>• 模型：Codex（gpt-5.5-medium）<br>• 基线：Synapse（同一模型，把轨迹当示例放进提示）<br>• 量的是：第二遍的中位 token、秒数和成功率<br>• 注意：两遍之间只换了屏幕分辨率，没测界面变化 | 预印本（JHU + Amazon） |
| OSWorld 2.0 批量动作（XLANG Lab, 2026） | 一 | I-2 | • 步数：Opus 4.7 单动作 318 → 批量 160.7<br>• 成功率：Opus 4.8 批量 20.6% vs 单动作 18.5%；Opus 4.7 18.2% vs 13.9% | • 在哪测：OSWorld 2.0 的 108 个任务<br>• 比的是：同一模型批量动作 vs 单动作<br>• 量的是：步数和成功率<br>• 注意：没有 wall-clock | 预印本（HKU） |
| FocusAgent（Kerboua et al., 2026） | 二 | III-2 | • 裁掉的观察：51–61%<br>• 输入 token 成本：−19% 到 −31%<br>• 成功率：−2.1 到 +3.1 pp，正负取决于检索模型 | • 在哪测：WorkArena L1（330 回合）和 WebArena（381 任务）<br>• 模型：执行 GPT-4.1，检索 GPT-4.1-mini 或 GPT-5-mini<br>• 基线：不裁剪的同一 agent<br>• 量的是：整套 benchmark 的输入 token 成本和成功率<br>• 注意：每步延迟反而变长（2.5 → 10.1 秒） | TMLR 2026 |
| Prune4Web（Zhang et al., 2025） | 二 | III-2 | • 候选元素：少 25–50 倍（10 万 token 的 DOM → 不到 20 个候选）<br>• 定位准确率：46.8% → 88.28% | • 在哪测：论文自设的低层 DOM 元素定位任务<br>• 比的是：让 LLM 直接读整个 DOM<br>• 量的是：定位准确率和候选元素数<br>• 注意：不是任务时间 | AAAI 2026 |
| AgentDiet（Xiao et al., 2026） | 二 | III-2 | • 输入 token：−39.9% 到 −59.7%<br>• 总成本：−21.1% 到 −35.9%<br>• 解决率：−1 到 +2 pp | • 在哪测：coding agent：100 个调参任务 + 200 个 SWE-bench Verified + 300 个 Multi-SWE-bench Flash<br>• 基线：不删轨迹的同一 agent<br>• 量的是：输入 token、含压缩器在内的美元总成本和解决率<br>• 注意：作者因 API 延迟不稳定而故意不比时间 | FSE 2026 |
| StepWise（Wei et al., 2026） | 二 | III-3、III-4 | • 每任务成本：$0.881 → $0.224（−74.6%）<br>• 每次请求时间：6.4 → 4.1 秒<br>• 成功率：58.1% → 55.4% | • 在哪测：OSWorld<br>• 比的是：EvoCUA-8B 小模型加选择性升级到 Claude Sonnet 4.5 vs 全程 Sonnet 4.5<br>• 量的是：每任务美元、每次请求的秒数和成功率<br>• 注意：计时是每次请求，不是每个任务 | 预印本（Yale） |
| Fara-7B（Awadallah et al., 2025） | 二 | III-4、单价 | • 每任务成本：$0.025 vs $0.913（约 36 倍，calc.）<br>• 动作数：16.5 vs 38.0<br>• 成功率：73.5% vs 70.9%；Browserbase 独立人工复核只得 62% | • 在哪测：WebVoyager（真实网站）<br>• 比的是：Fara-7B vs OpenAI computer-use-preview<br>• 量的是：每任务美元、动作数和成功率<br>• 注意：成本按 OpenRouter 最便宜的 7B 价格估算、无缓存；无 wall-clock | 预印本（Microsoft） |
| Ares（Yang et al., 2026） | 二 | III-3 | • 每任务推理 token：21,424 → 11,723（−45.3%）<br>• 成功率：45.0% → 46.5% | • 在哪测：WebArena（AgentOccam 框架，约 129 个任务）和 TAU-Bench Retail<br>• 模型：gpt-oss-20b，路由器 Qwen3-1.7B<br>• 基线：固定高推理强度<br>• 量的是：每任务推理 token 和成功率<br>• 注意：没有 wall-clock | 预印本（UCSB） |
| Don't Break the Cache（Lumer et al., 2026） | 二 | III-2 | • API 成本：−41% 到 −80%<br>• 首 token 时间：−13% 到 −31% | • 在哪测：500 多个 DeepResearch 会话，10K token 的 system prompt<br>• 提供商：OpenAI / Anthropic / Google 三家 API<br>• 比的是：同一会话开 / 不开提示缓存<br>• 量的是：API 账单成本和首 token 时间 | 预印本（PwC，工业测量，未见复现） |
| SGLang（Zheng et al., 2024） | 二 | III-2 | • 吞吐：最高 6.4 倍<br>• 单程序延迟：最多低 3.7 倍 | • 在哪测：作者自建的 LM 程序套件（含 agent 轨迹、few-shot、树搜索等）<br>• 模型：自己部署的开源模型<br>• 基线：vLLM 等推理引擎<br>• 量的是：吞吐和单程序延迟<br>• 注意：任务成功率没报 | NeurIPS 2024 |
| Agentix（Luo et al., 2026） | 二 | III-1、III-2 | • 同样延迟下的程序吞吐：4–15 倍（15 倍是 Mixed 负载的最大值） | • 在哪测：ShareGPT / BFCL / LATS 三类负载<br>• 模型：LLaMA-3.1 8B / 70B 和 Falcon-180B，1–8 张 A100，自己部署<br>• 基线：vLLM 类系统<br>• 量的是：“同样延迟下的程序吞吐”，延迟定义为程序响应时间 ÷ 生成 token 数<br>• 注意：准确率没报 | NSDI 2026 |
| ThunderAgent（Kang et al., 2026） | 二 | III-2 | • 步吞吐：1.48–3.58 倍于 vLLM<br>• 步吞吐：1.17–3.31 倍于 Continuum | • 在哪测：SWE-bench Lite 等 coding agent 负载，96 个并行程序<br>• 模型：GLM-4.6 355B / Qwen-3 235B，8×H100<br>• 基线：vLLM 和 Continuum<br>• 量的是：步吞吐<br>• 注意：任务质量没报 | ICML 2026 |
| Speculative Actions（Ye et al., 2026） | 三 | 串行 | • 平均执行时间：−19.5%<br>• 下一步预测准确率：54.7% | • 在哪测：国际象棋对局（3 个推测分支）<br>• 模型：GPT-5<br>• 基线：不推测的同一 agent<br>• 量的是：平均执行时间和预测准确率<br>• 注意：电商 API 任务和 HotpotQA 只报命中率；副作用事故没报 | ICLR 2026 Oral |
| ISP（Hua et al., 2025） | 三 | 串行 | • 每任务时间：182.70 → 105.42 秒（−42.30%）<br>• 每任务成本：$0.2160 → $0.2973（+38%） | • 在哪测：OpenAGI benchmark<br>• 模型：MAD 目标 agent<br>• 基线：顺序执行<br>• 量的是：每任务秒数和美元<br>• 注意：TravelPlanner 上用模糊匹配时通过率下降 | ICLR 2025 |
| DSP（Guan et al., 2026） | 三 | 串行 | • 延迟：−37.09%<br>• 成本：+62.99% | • 在哪测：OpenAGI benchmark<br>• 基线：顺序执行<br>• 量的是：延迟和成本的相对变化<br>• 注意：任务成功率变化没报 | ICLR 2026 |
| LLMCompiler（Kim et al., 2024） | 三 | 串行 | • 每任务时间：20.47 → 5.47 秒（3.74 倍）<br>• 每千任务成本：$20.46 → $3.04<br>• 准确率：72.47% → 77.13% | • 在哪测：Movie Recommendation 任务<br>• 模型：GPT-3.5<br>• 基线：ReAct<br>• 量的是：每任务秒数、每千任务美元和准确率<br>• 注意：HotpotQA 上只有 1.80 倍 | ICML 2024 |
| PASTE（Sui et al., 2026） | 三 | 串行、IV-4 | • 平均任务完成时间：最多 −43.5%<br>• p99：最多 −55.4% | • 在哪测：工具型 agent 负载（代码、搜索类，不是 GUI）<br>• 模型：本地部署 Qwen 30B，4×8 A100<br>• 基线：不推测的同一 agent<br>• 量的是：平均任务完成时间和 p99<br>• 注意：v3 的数（v1 写 −48.5%） | 预印本（SJTU + MSR） |
| Atomix（Mohammadi et al., 2026） | 三（安全） | — | • 门控提交：泄漏 0/500<br>• Saga 式补偿：泄漏 400/500（80%）<br>• 检查点重放：泄漏 200/500（40%） | • 在哪测：500 次“无效发送”试验（5 种中止来源 × 100）<br>• 汇点：真实的 SMTP / webhook<br>• 比的是：门控提交 vs Saga 式补偿 vs 检查点重放<br>• 量的是：不可逆效果的泄漏次数<br>• 注意：不是加速数字 | 预印本（MPI-SWS） |

### 从这些工作本身能推出的“还没做到”

每一条都指向具体工作自己声明的范围，不是“没人研究过”那种大话。

| 还没做到 | 依据 | 为什么重要 |
| --- | --- | --- |
| 重放 / 技能在界面变化后还能不能用，没有人跨版本、跨时间测过 | EchoPath 的作者自己写“尚未建立界面漂移下的鲁棒性”，唯一的扰动是换分辨率；ASI 说界面变了技能要改；厂商不发布修复成功率（E160）\[§3.9 第 11 条\] | 路线一的所有收益都建在“下次还能重放”上 |
| 在不能快照的真实 SaaS 上推测会改状态的点击 | TClone 关掉对外连接、DeltaBox 不支持网络回滚、AOSpec 排除非文件系统效果（E121–E123）；Cordon 没有 web / GUI 工作流；WebOperator 分类器 37% 精度 | 路线三在 GUI 上只剩只读部分 |
| agent 推理服务系统在 GUI 负载上的效果 | 15 个系统逐篇核过，没有一个用浏览器、OSWorld 或 WebArena 负载（E172–E186） | 路线二的服务系统部分对截图型 agent 是未知数 |
| 前沿 API 模型上“读写时间拆分 + 缓存命中率”的测量 | 第一份文档第五节；截图型 agent 的所有分解都没报缓存状态（D101） | 不知道缓存对截图型 agent 到底省多少 |
| 多个手段叠加后的总效果 | 裁历史打掉缓存（AgentDiet 自己指出）；路由器和验证器吃掉延迟（FocusAgent 变慢）；推测抬高 API 成本（ISP、DSP）；没有一篇在 computer-use benchmark 上把无损服务 + 少调用 + 有损手段端到端地一起测过（§3.9 第 3、13 条） | 各家的倍数不能相乘 |
| 一个统一的记账单位（每个成功任务的调用数 + prefill token + 回合 + 工具时间） | 没有一篇提出；WES（OSWorld-Human）和 cost-of-pass 是最接近的候选（§3.9 第 10 条） | 没有它，“做到什么程度”这个问题本身无法横向回答 |

## 五、数字不能直接拿来用的地方

| 问题 | 例子 | 怎么处理 |
| --- | --- | --- |
| “加速”的口径不一样 | AutoDroid-V2 的 14 倍是推理时间不是 wall-clock；StepWise 的 −45.8% 是每次请求不是每个任务；Agentix 的 4–15 倍是“同样延迟下的吞吐”，延迟定义是响应时间 ÷ 生成 token 数；AsyncLM 的 1.6–5.4 倍是模拟的云端延迟；Artificial Analysis 的“每任务时间”只算 decode（追加调查 6，DF6-4） | 每个倍数旁边写“比的是什么”；不同口径的倍数不放同一张图 |
| 版本间改过的数 | PASTE v1 −48.5% → v3 −43.5%（D13）；FocusAgent v1 只有 4.1-mini 检索器，v2 加了 5-mini 才有 +3.1 pp（D48）；Continuum 摘要 “>8 倍” 和正文 1.12–3.66 倍同时存在（D61）；Agent JIT 标题 10.4 倍、表里算出 9.7 倍（D43）；TraceLab 的 “5.3 倍” 在论文里不存在（D65） | 引用时写明版本号和页码 |
| 基线和方法用了不同模型 | ActionEngine（AgentOccam + GPT-4-Turbo vs 自己 + Claude 4.5 Sonnet）；OSWorld 2.0 的 6 倍 output token 是 GPT-5.5 vs Opus 4.8 | 只当“存在这样的系统”的证据，不当方法本身的效果 |
| 基线是另一个强方法，不是“什么都不做” | EchoPath 比的是 Synapse（轨迹当示例），不是无记忆的 agent；SMC 比的是 Speculative Actions | 写清基线是谁 |
| 厂商自述、建模推算、分析值 | Automation Anywhere “少 60% 失败”、Stagehand “快 80%”、OpenAI Ultrafast “14 倍”、Cerebras “11 倍”、Speculate with Memory 的 ALFWorld “>50%”（估计）、UFO2 “低 51.5% 成本”（作者声称）；Agentic Compilation 的 “1500 倍”（建模）和 LOOP 的 “99%”（推算）连同来源一起撤下，见下表 | 不作来源；只能说“厂商声称” |
| 样本小、单次运行 | GPA 16 个任务；Agent JIT 37 个；AppAgentX 单次运行；HAL 每配置只跑一次 | 引用时带上样本量 |
| 只报加速不报准确率 | 服务系统里 15 个只有 3 个报了任务质量；TClone、DeltaBox 没有任务指标 | 按“准确率未报告”记，不写成“无损” |
| 推测的“没出事” | Speculative Actions 没有报副作用事故 | “没报”不等于“测到零” |

**不采用或待核的来源（按零节的可信度规则，2026-09-27 逐一到 arXiv 页面核过）**

| 来源 | 它是什么 | 为什么不采用或待核 | 处理 |
| --- | --- | --- | --- |
| Agentic Compilation（Chundru, 2026，arXiv:2604.09718v2，Selfotix） | 把清洗后的 DOM 编译成确定性 JSON 工作流，元素找不到时叫 LLM 修选择器 | 单作者的公司预印本；只在内部站点上测，没有公开 benchmark；“1500 倍”成本下降是建模推算不是测量 | 不采用。已从 1.1 表和参考文献撤下；dossier E145 保留作“有人这样声称”的记录 |
| PreAct（Li, B., 2026，arXiv:2606.17929v1，Pine AI） | 成功的运行编译成带守卫条件的重放程序，守卫不匹配就回退给 agent | 单作者的公司预印本，未经同行评审；WebArena 上的 8.5–13 倍无人复现 | 不采用。已从 1.1 表和参考文献撤下；若日后进了会议再收回 |
| LOOP（Wang, X. et al., 2026，arXiv:2605.14237；蚌埠医科大学人工智能研究中心 + CHARMMIRAEL Biotech） | 录制工具调用序列后确定性重放，失败只记日志 | 标题即宣传语（“99% 成功、省 99% token”）；“99%”是推算不是实测（D110）；作者机构与主题无关 | 不采用。已从 1.5 产品表、正文和参考文献撤下；dossier E140 保留作记录 |
| Activity Frames（Iyamu, 2026，arXiv:2608.05784，独立研究者） | 把屏幕活动确定性地编译成 agent 记忆 | 单作者、无机构、私有语料 | 不采用。已从参考文献撤下 |
| “Minimal Failure Set / GEPA pruning（Agrawal et al.）”的署名 | arXiv:2605.29397 | dossier §3.5 沿用了 Gemini 调研的署名；arXiv 页面实为 Enomoto, Obara, Zhang & Oyamada（NEC Corporation），GEPA（Agrawal et al., 2025）只是它用的优化器 | 已改正（2.2 表）；新增 D146 |
| UFO2 的 “TMLR 2026” | arXiv:2504.14603 | dossier 记自二手来源；arXiv v2（2025-04-25）无期刊标注 | 按预印本（Microsoft）处理；待核 |
| Continuum 的 PVLDB | arXiv:2511.02230v7 | v7 页首标 PVLDB Vol. 20 No. 1；VLDB 官网未核 | 按“期刊论文（据 v7 页首）”处理；待核 |
| Prune4Web 的机构 | arXiv:2511.21398 | AAAI 2026 有官网论文页（40772）；arXiv 页不列作者机构 | 会议论文；机构待核 |
| Cordon 的 “EuroSys 2027”、AAPT 的 “AAAI 2027” | 论文页首的模板或版权栏 | 模板不等于录用 | 按预印本处理 |
| Signal-Driven Observation（Gaur & Lane, 2026，UC Santa Cruz） | 只在有信号时重新观察 | 该文自述不含实验 | 只作提法（3.3），不作证据 |
| RAC（Perera, Leymann, Hapuarachchi & Khalaf, 2026） | agent 的补偿机制 | 页首为 ACM CAIS '26 版权栏（WSO2 + University of Stuttgart），会议页面未核 | 会议论文（据版权栏）；本文只用定性 |
| RouteLLM 和 AgentOccam 的 ICLR 2025，SimpAgent 的 ICCV 2025 | — | arXiv 页无会议标注，会议信息来自 dossier；本次未能访问 OpenReview 核实 | 保留标注，注明“据 dossier” |

## 六、参考文献

写法同第一份文档：作者（年份）。题目。会议或 arXiv 编号、版本、日期。机构。— 来源类型。作者、机构、版本都在 2026-09-27 到 arXiv 页面核过；会议或期刊的录用只认官方页面或 arXiv 页面的标注，只有 dossier 记录、本次未能核实的，注明“据 dossier”。按零节的可信度规则不采用的来源（Agentic Compilation、PreAct、LOOP、Activity Frames）不列在这里，只列在第五节的表里。厂商文档和只用了定性信息的工作放在末尾。

- Abhyankar, R., Qi, Q., & Zhang, Y. (2026). OSWorld-Human: Benchmarking the efficiency of computer-use agents. *MLSys 2026*. arXiv:2506.16042v2. UC San Diego. — 会议论文。
- Abhyankar, R., et al. (2024). InferCept: Efficient intercept support for augmented large language model inference. *ICML 2024*. UC San Diego. — 会议论文（待核全部作者）。
- Enomoto, M., Obara, R., Zhang, H., & Oyamada, M. (2026). Revisiting observation reduction for web agents: Comprehensive evaluation with a lightweight framework. arXiv:2605.29397v1 (28 May 2026). NEC Corporation. — 预印本。（dossier §3.5 误署为 “Agrawal et al.”，GEPA 只是它用的优化器；见 D146）
- Awadallah, A., Lara, Y., Magazine, R., Mozannar, H., Nambi, A., Pandya, Y., Rajeswaran, A., Rosset, C., Taymanov, A., Vineet, V., Whitehead, S., Zhao, A., et al. (2025). Fara-7B: An efficient agentic model for computer use. arXiv:2511.19663v1 (Nov 2025). Microsoft. — 预印本。
- Bai, H., Lv, W., Zheng, H., Lu, Y., & Shu, J. (2026). SPORK: Self-speculative forking to accelerate agentic LLM inference. arXiv:2607.03333v1 (3 Jul 2026). Tsinghua University; Meituan. — 预印本。
- Chen, H. (M.), Guo, J., Luk, W., & Fan, H. (2026). AOSpec: Action and observation co-speculation for low-latency agent serving. arXiv:2608.00881v1 (1 Aug 2026). Imperial College London. — 预印本。
- Chen, Q., Sun, Z., Bellucci, A., & Jacucci, G. (2026). SkillDroid: Compile once, reuse forever. arXiv:2604.14872v1 (Apr 2026). University of Helsinki; Shenzhen University; Universidad Carlos III de Madrid. — 预印本。
- Chen, Z., Dong, D., Liu, H., Li, J., Zhai, J., Xu, D., & Pu, B. (2026). Cordon: Semantic transactions for tool-using LLM agents. arXiv:2606.17573v1 (16 Jun 2026). Tsinghua University; Shanghai Jiao Tong University; Renmin University; AetherHeart. — 预印本（页首写 EuroSys 2027，录用未确认）。
- Cuadron, A., Li, D., Ma, W., Wang, X., Wang, Y., Zhuang, S., Liu, S., Gaspar Schroeder, L., Xia, T., Mao, H., Thumiger, N., Desai, A., Stoica, I., Klimovic, A., Neubig, G., & Gonzalez, J. E. (2025). The danger of overthinking: Examining the reasoning-action dilemma in agentic tasks. arXiv:2502.08235v1 (12 Feb 2025). UC Berkeley; ETH Zurich; UIUC; CMU. — 预印本。
- Dihan, M. L., Hashem, T., Ali, M. E., & Parvez, M. R. (2025). WebOperator: Action-aware tree search for autonomous agents in web environment. arXiv:2512.12692v1 (14 Dec 2025). BUET; Monash University; QCRI. — 预印本。
- Dong, Y., He, J., Liu, S., Hou, Y., Du, D., Xu, Z., Yu, S., Yang, B., Xia, Y., & Chen, H. (2026). DeltaBox: Scaling stateful AI agents with millisecond-level sandbox checkpoint/rollback. arXiv:2605.22781v2 (8 Jun 2026). Shanghai Jiao Tong University IPADS; Huawei. — 预印本。
- Feng, G., Mao, H., Dutta, P., & Gonzalez, J. E. (2026). Concurrency without model changes: Future-based asynchronous function calling for LLMs (AsyncFC). arXiv:2605.15077v1 (14 May 2026). University of California, Berkeley. — 预印本。
- Gim, I., Lee, S., & Zhong, L. (2024). Asynchronous LLM function calling (AsyncLM). arXiv:2412.07017v1 (9 Dec 2024). Yale University. — 预印本（页首自述“初步工作，在审”）。
- Guan, Y., Lan, Q., Sun, F., Ding, D., Acharya, D., Wang, C., Wang, W. Y., & Hua, W. (2026). Dynamic speculative agent planning. *ICLR 2026*. arXiv:2509.01920v3. Johns Hopkins; University of Alberta; UBC; Google DeepMind; UC Santa Barbara. — 会议论文。
- Hua, W., Wan, M., Vadrevu, S., Nadel, R., Zhang, Y., & Wang, C. (2025). Interactive speculative planning: Enhance agent efficiency through co-design of system and user interface. *ICLR 2025*. arXiv:2410.00079. Microsoft; Rutgers. — 会议论文。
- Huang, Y., Srivatsa, V., Asch, A., Patwa, H. T., & Zhang, Y. (2026). TClone: Low-latency forking of live GUI environments for computer-use agents. arXiv:2605.17320v1 (17 May 2026). UC San Diego; GenseeAI. — 预印本。
- Huang, Z., Wang, X., Wang, A., Jurayj, W., Jiménez Gutiérrez, B., Khashabi, D., & Andrews, N. (2026). Better, faster, stronger: Programmatic skill learning best reduces agent cost (SpeedRunner). arXiv:2608.11338v1 (11 Aug 2026). Johns Hopkins University. — 预印本。
- Jiang, W., Zhuang, Y., Song, C., Yang, X., Zhou, J. T., & Zhang, C. (2025). AppAgentX: Evolving GUI agents as proficient smartphone users. arXiv:2503.02268v2. Westlake University; Henan University; Southeast University; A\*STAR (IHPC, CFAR). — 预印本。
- Kang, H., Li, Z., Xu, W., Yang, X., Chen, Y., Wang, J., Chen, B., Krishna, T., Xu, C., & Arora, S. (2026). ThunderAgent: A simple, fast and program-aware agentic inference system. *ICML 2026* (poster). arXiv:2602.13692v3 (30 Jun 2026). Georgia Tech; UIUC; CMU; Together AI. — 会议论文。
- Kapoor, S., Stroebl, B., Kirgis, P., Nadgir, N., Siegel, Z. S., Wei, B., … Narayanan, A. (2025). Holistic Agent Leaderboard. arXiv:2510.11977v1 (13 Oct 2025). Princeton University et al. — 预印本。
- Kerboua, I., Omidi Shayegan, S., Thakkar, M., Lù, X. H., Boisvert, L., Caccia, M., Espinas, J., Aussem, A., Eglin, V., & Lacoste, A. (2026). FocusAgent: Simple yet effective ways of trimming the large context of web agents. *Transactions on Machine Learning Research* (Aug 2026). arXiv:2510.03204v2 (29 Aug 2026). Esker; INSA Lyon; ServiceNow Research; Mila; McGill. — 期刊论文。
- Kim, S., Moon, S., Tabrizi, R., Lee, N., Mahoney, M. W., Keutzer, K., & Gholami, A. (2024). An LLM compiler for parallel function calling. *ICML 2024*. arXiv:2312.04511. UC Berkeley. — 会议论文。
- Lai, H., Liu, X., Zhao, Y., Xu, H., Zhang, H., Jing, B., Ren, Y., Yao, S., Dong, Y., & Tang, J. (2025). ComputerRL: Scaling end-to-end online reinforcement learning for computer use agents. *ICLR 2026* (poster). arXiv:2508.14040v2 (21 Oct 2025). Tsinghua University; Z.AI. — 会议论文。
- Li, H., He, R., Mang, Q., Zhang, Q., Mao, H., Chen, X., Zhou, H., Zhang, H., Cheung, A., Gonzalez, J., & Stoica, I. (2026). Contin*uum: Efficient and robust multi-turn LLM agent scheduling with KV cache time-to-live. arXiv:2511.02230v7 (8 Sep 2026)；v7 页首标 PVLDB Vol. 20 No. 1，VLDB 官网未核. UC Berkeley; Stanford; Tsinghua. — 期刊论文（据 v7 页首，*待核）。
- Li, T., Hu, J., Wang, Y., Liu, J., & Liu, X. (2025). WebRouter: Query-specific router via variational information bottleneck for cost-sensitive web agent. arXiv:2510.11221v1 (Oct 2025). NUAA; HKBU; Beihang; Pengcheng Laboratory. — 预印本（页首：在审 ICASSP 2026）。
- Li, Y., Ye, Q., Choubey, P. K., Zhang, J., & Wu, C.-S. (2026). Speculate with memory: Lossless acceleration for LLM agents. arXiv:2607.12236v1 (Jul 2026). Salesforce Research. — 预印本。
- Lin, X., Liew, J. H., Savarese, S., & Li, J. (2026). W&D: Scaling parallel tool calling for efficient deep research agents. arXiv:2602.07359v1 (7 Feb 2026). Salesforce AI Research. — 预印本。
- Lindenbauer, T., Slinko, I., Felder, L., Bogomolov, E., & Zharov, Y. (2025). The complexity trap: Simple observation masking is as efficient as LLM summarization for agent context management. *NeurIPS 2025 Workshop on Deep Learning for Code*. arXiv:2508.21433v3 (27 Oct 2025). JetBrains Research; TU Munich. — 研讨会论文。
- Liu, Z., Kundu, S., & Beerel, P. A. (2026). Speculative macro commit for faster tool-using agents. arXiv:2609.03236v1 (Sep 2026). USC; Intel Labs. — 预印本。
- Lu, J., Zhang, Z., Yang, F., Zhang, J., Wang, L., Du, C., Lin, Q., Rajmohan, S., Zhang, D., & Zhang, Q. (2025). AXIS: Efficient human-agent-computer interaction with API-first LLM-based agents. *ACL 2025* (Long Papers), 7711–7743. Microsoft. — 会议论文。
- Lumer, E., Nizar, F., Jangiti, A., Frank, K., Gulati, A., Phadate, M., & Subbiah, V. K. (2026). Don't break the cache: An evaluation of prompt caching for long-horizon agentic tasks. arXiv:2601.06007v2 (31 Jan 2026). PricewaterhouseCoopers (PwC). — 预印本（工业测量，未经同行评审）。
- Luo, M., Shi, X., Cai, C., Zhang, T., Wong, J., Wang, Y., Wang, C., Huang, Y., Chen, Z., Gonzalez, J. E., & Stoica, I. (2026). Agentix: An efficient serving engine for LLM agents as general programs. *NSDI 2026*. UC Berkeley; Google DeepMind; Shanghai Jiao Tong University. — 会议论文。
- Mohammadi, B., Potamitis, N., Klein, L., Arora, A., & Bindschaedler, L. (2026). Atomix: Timely, transactional tool use for reliable agentic workflows. arXiv:2602.14849v2 (29 May 2026). MPI-SWS; Aarhus University; EPFL. — 预印本。
- Mohammadi, B., Klein, L., Arora, A., & Bindschaedler, L. (2026). Ghost tool calls: Issue-time privacy for speculative agent tools. arXiv:2606.02483v1 (1 Jun 2026). MPI-SWS; EPFL; Aarhus University. — 预印本。
- Pan, Z., Patel, A., Hu, Z., Shen, Y., Guan, Y., Li, W.-L., Qin, L., Wang, Y., & Ding, Y. (2025). KVFlow: Efficient prefix caching for accelerating LLM-based multi-agent workflows. *NeurIPS 2025*. arXiv:2507.07400. UC San Diego. — 会议论文。
- Prabhu, V., Dai, Y., Fernandez, M., Gu, J., Ramakrishnan, K., Luo, Y., Savarese, S., Xiong, C., Li, J., Chen, Z., & Xu, R. (2026). WALT: Web agents that learn tools. *ICLR 2026*. arXiv:2510.01524v1. Salesforce AI Research. — 会议论文。
- Song, Y., Xu, F. F., Zhou, S., & Neubig, G. (2025). Beyond browsing: API-based web agents. *Findings of ACL 2025*. arXiv:2410.16464. CMU. — 会议论文（作者待核）。
- Sui, Y., Zhao, H., Ma, R., He, Z., Wang, H., Xu, K., Chen, K., Li, J., & Yang, Y. (2026). Parallelizing tool execution and LLM generation for low-latency agent serving (PASTE). arXiv:2603.18897v3 (16 Jun 2026). Shanghai Jiao Tong University; Microsoft Research; Stevens; HKUST. — 预印本。
- Wang, N., Hu, X., Liu, P., Zhu, H., Hou, Y., Huang, H., Zhang, S., Yang, J., Liu, J., Zhang, G., Zhang, C., Wang, J., Jiang, Y. E., & Zhou, W. (2025). Efficient agents: Building effective agents while reducing cost. arXiv:2508.02694v1 (24 Jul 2025). OPPO. — 预印本。
- Wang, Z. Z., Mao, J., Fried, D., & Neubig, G. (2025). Agent workflow memory. *ICML 2025*. arXiv:2409.07429. CMU; MIT. — 会议论文。
- Wang, Z. Z., Gandhi, A., Neubig, G., & Fried, D. (2025). Inducing programmatic skills for agentic tasks (ASI). *COLM 2025*. arXiv:2504.06821v2. CMU. — 会议论文。
- Wei, J., Ni, K., Zhao, Y., Gan, G., & Cohan, A. (2026). Step-level optimization for efficient computer-use agents (StepWise). arXiv:2604.27151v1 (29 Apr 2026). Yale NLP Lab; UNC Chapel Hill. — 预印本。
- Wen, H., Tian, S., Pavlov, B., Du, W., Li, Y., Chang, G., Zhao, S., Liu, J., Liu, Y., Zhang, Y.-Q., & Li, Y. (2025). AutoDroid-V2: Boosting SLM-based GUI agents via code generation. *MobiSys 2025*. arXiv:2412.18116v3. Tsinghua AIR; Shanghai AI Lab; BAAI. — 会议论文。
- Winston, C., Wang, R. Y., Mirhoseini, A., & Kozyrakis, C. (2026). Agent JIT compilation for latency-optimizing web agent planning and scheduling. *ICML 2026*, PMLR 306. arXiv:2605.21470. Stanford. — 会议论文。
- Wong, M., Hsieh, K., Nath, S., & Netravali, R. (2026). Skim: Speculative execution for fast and efficient web agents. arXiv:2605.16565v2 (19 May 2026). Princeton; Microsoft Research. — 预印本。
- Wu, G., Li, D., Jiang, K., Niu, J., Wang, C., & Zhang, Y. (2026). Safe to resume? Breaking execution continuity of agent execution via rollback. arXiv:2608.29381v1 (29 Aug 2026). Southern University of Science and Technology; City University of Hong Kong. — 预印本。
- Xiao, Y.-A., Gao, P., Peng, C., & Xiong, Y. (2026). Reducing cost of LLM agents with trajectory reduction (AgentDiet). *Proceedings of the ACM on Software Engineering* 3 (FSE 2026). arXiv:2509.23586v2. Peking University; ByteDance. — 会议论文。
- XLANG Lab (2026). OSWorld 2.0: Benchmarking computer use agents on long-horizon real-world tasks. arXiv:2606.29537v2 (13 Jul 2026). The University of Hong Kong. — 预印本。
- Yang, J., Hou, B., Wei, W., Bao, Y., & Chang, S. (2026). ARES: Adaptive reasoning effort selection for efficient LLM agents. arXiv:2603.07915v1 (9 Mar 2026). UC Santa Barbara; Accenture. — 预印本。
- Yang, Y., Jin, C., Zhao, J., Wu, J., Zhou, Y., Wang, Z., Wang, Z., Zhou, M., & Metaxas, D. N. (2026). Act more, decide less: Skill-guided adaptive action chunking for long-horizon LLM agents (SPACE). arXiv:2609.02042v1 (2 Sep 2026). Rutgers; University of Toronto; PolyU; Amazon; Microsoft. — 预印本。
- Ye, N., Ahuja, A., Liargkovas, G., Lu, Y., Kaffes, K., & Peng, T. (2026). Speculative actions: A lossless framework for faster agentic systems. *ICLR 2026* (Oral). arXiv:2510.04371v2 (23 Apr 2026). Columbia University. — 会议论文。
- Zhang, C., Huang, H., Ni, C., Mu, J., Qin, S., He, S., … Zhang, D. (2025). UFO2: The desktop AgentOS. arXiv:2504.14603v2 (25 Apr 2025). Microsoft. — 预印本（dossier 记 TMLR 2026，来自二手来源；arXiv 页无期刊标注，待核）。
- Zhang, J., Chen, K., Lu, Z., Zhou, E., Yu, Q., & Zhang, J. (2025). Prune4Web: DOM tree pruning programming for web agent. *AAAI 2026*（AAAI 官网论文页 40772）. arXiv:2511.21398v1 (26 Nov 2025). — 会议论文（作者机构未在 arXiv 页列出）。
- Zhang, Q., Wornow, M., Wan, G., & Olukotun, K. (2025). Agentic plan caching: Test-time memory for fast and cost-efficient LLM agents. *NeurIPS 2025*. arXiv:2506.14852v2. Stanford. — 会议论文。
- Zhang, R., Kim, C., Feng, S., Du, K., Liu, Y., Zhong, Y., Ching, C.-W., Jiang, J., & Hu, L. (2026). Learning agent execution for KV-cache management in agentic serving (CacheScout). arXiv:2608.14624v1 (16 Jul 2026). UC Santa Cruz; University of Washington; University of Chicago. — 预印本。
- Zhao, Y., Shanmugham, A., Roy, S., & Xu, Y. (2026). EchoPath: Execution-level replayable memory for GUI agents. arXiv:2609.16635v1 (15 Sep 2026). Johns Hopkins University; Amazon AGI. — 预印本。
- Zhao, Z., Liew, J. H., Yang, Y., Yang, W., Luo, Z., Sahoo, D., Savarese, S., & Li, J. (2026). GPA: Learning GUI process automation from demonstrations. arXiv:2604.01676v2 (4 Apr 2026). Salesforce. — 预印本。
- Zheng, B., Fatemi, M. Y., Jin, X., Wang, Z. Z., Gandhi, A., Song, Y., Gu, Y., Srinivasa, J., Liu, G., Neubig, G., & Su, Y. (2025). SkillWeaver: Web agents can self-improve by discovering and honing skills. arXiv:2504.07079v1 (Apr 2025). The Ohio State University; University of Virginia; Purdue University; Carnegie Mellon University; Cisco Research. — 预印本。
- Zheng, L., et al. (2024). SGLang: Efficient execution of structured language model programs. *NeurIPS 2024*. arXiv:2312.07104v2. Stanford; UC Berkeley. — 会议论文（全部作者待核）。
- Zhong, H., Leesatapornwongsa, T., Faisal, F., Szekeres, A., Nath, S., França, L., & Rong, K. (2026). ActionEngine: From reactive to programmatic GUI agents via state machine memory. arXiv:2602.20502v1 (Feb 2026). Georgia Tech; Microsoft Research. — 预印本。
- Zhu, K., Jacob, M., Ma, C., Pan, Y., Wang, S., Krishnamurthy, A., & Kasikci, B. (2026). TraceLab: Characterizing coding agent workloads for LLM serving. arXiv:2606.30560v2 (30 Jun 2026); TraceLab dashboard, tracelab.cs.washington.edu (accessed 2026-09-27). University of Washington. — 预印本；仪表盘为第三方实测数据。
- 厂商一手资料：Anthropic (2026b) 定价与 fast mode 文档；OpenAI (2026) 定价与 changelog；UiPath Healing Agent、Microsoft Power Automate self-healing / Repair with Copilot、Automation Anywhere Generative Recorder、Browserbase Stagehand、Skyvern、Hyperbrowser HyperAgent 的产品文档（具体 URL 和读取日期在 dossier E139–E160）。— 厂商文档；其中的效果数字不作来源。
- 本文提到但只用了定性信息的工作（作者与机构 2026-09-27 在 arXiv 页核过；不采用的已移到第五节的表）：AgentOccam — Yang, K., Liu, Y., Chaudhary, S., Fakoor, R., Chaudhari, P., Karypis, G., & Rangwala, H. (2024). AgentOccam: A simple yet strong baseline for LLM-based web agents. arXiv:2410.13825v2. Amazon; UIUC. — 会议论文（ICLR 2025，据 dossier）；RouteLLM — Ong, I., Almahairi, A., Wu, V., Chiang, W.-L., Wu, T., Gonzalez, J. E., Kadous, M. W., & Stoica, I. (2024). RouteLLM: Learning to route LLMs with preference data. arXiv:2406.18665v4 (23 Feb 2025). UC Berkeley; Anyscale; Canva. — 会议论文（ICLR 2025，据 dossier）；FrugalGPT — Chen, L., Zaharia, M., & Zou, J. (2023). FrugalGPT: How to use large language models while reducing cost and improving performance. arXiv:2305.05176; Transactions on Machine Learning Research (12/2024). Stanford. — 期刊论文；TokenPilot — Xu, B., Xue, Z., Chen, D., Fu, C., Wu, C., Huang, C., Jiang, C., Fang, J., Deng, X., Chen, Y., Yao, Y., Wang, X., Shang, J., Yu, G., & Zhang, N. (2026). TokenPilot: Cache-efficient context management for LLM agents. arXiv:2606.17016. Zhejiang University; UESTC; Xidian University; HomologyAI. — 预印本；SpecBox — Zhang, Y., Wo, T., Wang, J., Sun, X., Zhang, M., Yuan, C., Li, L., Hu, C., Zomaya, A. Y., & Yang, R. (2026). SpecBox: Speculative sandbox scheduling for efficient LLM agent serving. arXiv:2607.23933v2 (5 Aug 2026). Beihang University; University of Leeds; University of Sydney. — 预印本；Signal-Driven Observation — Gaur, S., & Lane, I. (2026). Signal-driven observation for long-horizon web agents. arXiv:2606.06708v2 (4 Aug 2026). UC Santa Cruz. — 预印本，自述不含实验；Are Online Skill and Memory Modules Always Worth Their Tokens? — Hajimiri, S., Aminbeidokhti, M., Dolz, J., Ben Ayed, I., Laradji, I. H., Gella, S., & Gontier, N. (2026). arXiv:2606.15017. ServiceNow AI Research; ÉTS Montréal; UBC; McGill. — 预印本（1.2 表用了它的数字）；Revisable by Design — Zhai, Z., Li, M., & Wang, X. (2026). Revisable by design: A theory of streaming LLM agent execution. arXiv:2604.23283v1 (25 Apr 2026). Fudan University; Guangming Lab. — 预印本；RAC — Perera, S., Leymann, F., Hapuarachchi, K., & Khalaf, R. (2026). Robust Agent Compensation (RAC): Teaching AI agents to compensate. arXiv:2605.03409；页首为 ACM CAIS '26 版权栏. WSO2; University of Stuttgart. — 会议论文（据版权栏）；AAPT — Dong, Z., Qian, R., Zhan, Q., Peng, D., Li, K., & Li, Y. (2026). Why are GUI agents correct but late? Decode on the decision-time critical path, tested with pre-compiled policy trees. arXiv:2607.28399. Georgia Tech; Fudan; Marquette; UNC Chapel Hill; NUS; Southeast University. — 预印本（AAAI 2027 模板，录用未确认）；SimpAgent — Chen, G., Zhou, X., Shao, R., Lyu, Y., Zhou, K., Wang, S., Li, W., Li, Y., Qi, Z., & Nie, L. (2025). Less is more: Empowering GUI agent with context-aware simplification. arXiv:2507.03730. Harbin Institute of Technology (Shenzhen); Huawei Noah's Ark Lab. — 会议论文（ICCV 2025，据 dossier）；GUIPruner — Xu, Z., Zhou, B., Wang, Q., Feng, S., & Xiao, J. (2026). Spatio-temporal token pruning for efficient high-resolution GUI agents. arXiv:2602.23235v1 (26 Feb 2026). Tsinghua University (Shenzhen); Xidian University; CUHK. — 预印本；TRACE — Wang, Y., Qiao, M., Zhang, X., Zhuge, Y., Zhang, L., & Lu, H. (2026). TRACE: Trajectory-robust admission with evidence ordering for efficient GUI agents. arXiv:2609.10297. Dalian University of Technology; OPPO Research Institute; Hong Kong Polytechnic University. — 预印本；AQuaUI — Li, Y., Zhu, T., Son, H. M., Zhao, Z., Liu, X., & Chen, M. (2026). AQuaUI: Visual token reduction for GUI agents with adaptive quadtrees. arXiv:2605.19260v1 (19 May 2026). UC Davis. — 预印本；GUI-KV — Huang, K.-H., Qiu, H., Dai, Y., Xiong, C., & Wu, C.-S. (2025). GUI-KV: Efficient GUI agents via KV cache with spatio-temporal awareness. arXiv:2510.00536v1 (1 Oct 2025). Salesforce AI Research; UCLA. — 预印本；BoPO — Zhang, C., Xia, M., Zhang, X., Madrigal, D., Mallick, A., Kessler, S., Rühle, V., & Rajmohan, S. (2026). Budget-aware agentic routing via boundary-guided training. arXiv:2602.21227v1 (4 Feb 2026). University of Cambridge; Microsoft (M365 Research). — 预印本。
- Agent Acceleration Consolidated Dossier v3 (2026-09-27)：我们自己的台账；\[E 号\] 指证据表，\[D 号\] 指差异表，§3.x 指第三部分的文献表。
