<!-- Exported from the Claude Doc 《Agent 慢和贵的逻辑链》 (https://claude.ai/code/artifact/3282af0d-4a36-4d10-97b7-8dfc09dcc449), rev 81, on 2026-09-28. The Claude Doc is the working copy Edwin comments on; this file is a snapshot for the repo and for Claude Code. Embedded diagrams/charts appear as '[embedded content: …]' placeholders; formulas are ```latex blocks. -->

# Agent 慢和贵的逻辑链

Sep 27, 2026 · @Edwin

这份是给 Edwin 自己读的，目的只有一个：把"agent 为什么慢、为什么贵、两者怎么连"这条链从头理顺。先不管 slides 怎么排。所有数字带文献引用（第一作者 et al., 年份；完整条目在文末第六节参考文献）、dossier v3 台账的 \[E/D 号\]，和来源类型（会议或期刊论文 / 预印本，标机构 / 厂商一手资料 / 行业报告 / 代码）；我自己算的标 calc.；我的推断标"推断"。

## 零、先把循环讲清楚（前提）

一个 agent 做一个任务，就是把同一个循环转 N 圈；每圈至少调一次模型，而每次调用内部又分排队、读、写三段。后面所有"慢"和"贵"的原因，都是这个循环里的某一项。

&#91;embedded content: agent 的一圈 · 四个环节，决定这一环拆成三段\]

读和写的区别要记住：读是把整段提示并行处理，每个 token 很快；写是一个 token 一个 token 往外生成，每个 token 十几毫秒（Claude Opus 5.5 实测输出 81.7 token/s，Artificial Analysis, 2026 \[E208\]，第三方测量），而且写的单价是读的 5 倍。

把这一圈写成式子，时间和钱各一个：

```latex
T_{task} \approx \sum_{k=1}^{N} \Big[\, c_k \big( t_{queue} + t_{read}(R_k) + t_{write}(W_k) \big) + t_{obs} + t_{act} + t_{wait} \Big]
```

```latex
Cost_{task} \approx \sum_{k=1}^{N} c_k \big( R_k \cdot p_{read} + W_k \cdot p_{write} \big), \qquad Cost_{success} = \frac{Cost_{task}}{\text{success rate}}
```

| 符号 | 意思 | 谁决定它 |
| --- | --- | --- |
| N | 步数：循环转了几圈 | 任务长度、动作粒度、有没有空转 |
| c\_k | 第 k 步调了几次模型 | 框架：一次调用，还是规划 + 判断 + 反思 |
| R\_k | 第 k 次调用读了多少 token | 历史有多长、截图多大；**随 k 增长** |
| W\_k | 第 k 次调用写了多少 token | 思考模式、模型大小 |
| p\_read、p\_write | 读、写的单价；命中缓存的读按 0.1 倍计 | 模型档位、fast mode、缓存 |
| t\_obs、t\_act、t\_wait | 观察、执行、等待的时间 | 浏览器、桌面 sandbox、固定停顿 |

读为什么随步数平方增长、写为什么线性增长，直接从钱的式子看：每步写的 W\_k 大致固定，N 步加起来是 N × W，线性；每步读的 R\_k 却随 k 增长，因为第 k 步的提示要包含前面 k−1 步的截图和历史，R\_k ≈ k × 每步新增的 token（一张截图 1,000–1,800 tokens）。N 步加起来是 (1 + 2 + … + N) × 每步新增 ≈ N² / 2 × 每步新增，平方。算个数：10 步要读 55 份历史，20 步要读 210 份，步数翻一倍，读的量翻近四倍；写的量只从 10 份到 20 份。前提是每步把全部历史重发、且没有缓存：裁剪历史会把它压到平方以下，缓存把读的单价打一折但不改形状。OSWorld-Human 在真实运行里测到的就是这个形状（“成本随步数二次增长”，Abhyankar et al., 2026）\[E45\]。

两个式子放在一起看，有一个后面反复用到的差别：**环境时间（观察、执行、等待）和排队只进时间的式子，不进钱的式子**；读和写的 token 两个式子都进。这就是"慢和贵怎么连"的全部底层结构。

## 一、慢在哪：所有原因，分五类

慢的原因一共五类，前四类各自是时间式子里的一项，第五类（串行）是把前四类**加起来而不是取最大值**的结构性原因。每张表的后三列：「证据与引用」里括号是文献（第一作者 et al., 年份，完整条目在文末参考文献），方括号是 dossier v3 台账的条目号，回查原始数字和测量口径用；「来源类型」是文献的种类（会议或期刊论文 / 预印本，标机构 / 厂商一手资料 / 行业报告 / 代码）；「主要出现在哪种 agent」是第二节的三种 agent：截图型桌面 agent、文本型 web agent、带缓存的 coding agent。

### 第一类：做的步数多（N 大）

| 编号 | 原因 | 机制 | 证据与引用 | 来源类型 | 主要出现在哪种 agent |
| --- | --- | --- | --- | --- | --- |
| I-1 | 任务本身长 | 小时级任务要几百圈 | OSWorld 2.0 的 108 个长任务上，Claude Opus 4.7 开最大思考、每步只允许一个动作、上限 500 步时，平均每个任务 318 次工具调用，也就是 318 步；允许一步批量执行多个动作后，Opus 4.8 用 103 步（481.8 次调用）、GPT-5.5 用 95.2 步（149.8 次调用）（XLANG Lab, 2026）\[E6\] | 预印本，香港大学 XLANG Lab | 截图型、文本型 |
| I-2 | 一步只做一个动作 | 每点一下就是一整圈：一次观察、一次模型调用、一次等待 | OSWorld 2.0 上，单动作设置下 Opus 4.7 要 318 步；批量动作设置下同一个 Opus 4.7 降到 160.7 步，Opus 4.8 降到 103 步（XLANG Lab, 2026）\[E6\] | 预印本 | 截图型、文本型 |
| I-3 | 纯导航的步也要过一遍模型 | 翻页、滚动、进入下一页这类不需要思考的步，照样付一次调用 | Skim 在 151 个 WebVoyager 真实网站任务上剖析三个文本型 web agent（Browser-Use、AgentOccam、WebVoyager，模型 GPT-4o），中位任务里 66.7% 的步是纯导航（Wong et al., 2026）\[E17\] | 预印本，Princeton + Microsoft Research | 文本型 |
| I-4 | 空转和死循环 | 定位不到元素、反复重试，步数白涨 | OSWorld-Human 剖析 GTA1 框架（o3 做规划和判断、GTA1-7B 做界面定位）在 39 个 OSWorld 桌面任务上的记录：失败且超过 50 步的任务里 66% 的步是无效重复；其中一次界面定位死循环——同一步重复 18 次——花了 27 分钟、按挂牌价 $8.47（无缓存）（Abhyankar et al., 2026）\[E45\] | 会议论文，MLSys 2026 | 截图型 |
| I-5 | 按过期状态行动，返工 | 截图拍早了，页面还没变，agent 按旧画面点，之后要纠错 | OSWorld 2.0 记录了 "stale interface state" 这一失败模式（XLANG Lab, 2026）\[§1.8\] | 预印本 | 截图型 |

### 第二类：每步调用的次数多（c 大）

| 编号 | 原因 | 机制 | 证据与引用 | 来源类型 | 主要出现在哪种 agent |
| --- | --- | --- | --- | --- | --- |
| II-1 | 多调用框架 | 一步 = 规划 + 判断 + 反思，几次调用串起来 | OSWorld-Human 剖析的两个框架：GTA1 每一步由 4 个并行规划器各出一个候选、失败最多重试 3 轮、再由 1 次判断调用挑选，所以每 1 次判断对应 4–12 次规划调用 \[E25\]；Agent S2 每步除规划外还有一次反思调用，总时间里规划占 53%、反思占 34% \[E22\]（Abhyankar et al., 2026） | 会议论文，MLSys 2026 | 截图型 |
| II-2 | 多采样换准确率 | 每步生成 5–20 个候选再挑 | 同一个模型和框架（gpt-oss-120b，ReAct）在 165 个 WebArena-Lite 任务上，每步候选从 1 个加到 10 个，成功率 38.8% → 43.2%，每任务 token 9.6 万 → 92 万，即 9.6 倍 token 换 4.4 个点（Lee et al., 2026）\[E44\] | 预印本，UC Berkeley | 文本型 |
| II-3 | coding agent 一轮多次调用 | 一个用户回合内模型来回调 | GitHub Copilot coding agent 的生产遥测（2026 年 6 月第一周，1,350 万个 session）里，每个用户回合平均 6.6 次模型调用（Liu et al., 2026）\[E20\] | 预印本，UIUC + Microsoft Azure Research；数据是 GitHub Copilot 的生产遥测 | 缓存型 coding |

### 第三类：每次调用慢

| 编号 | 原因 | 机制 | 证据与引用 | 来源类型 | 主要出现在哪种 agent |
| --- | --- | --- | --- | --- | --- |
| III-1 | 排队 | 请求在提供商那里等；不花钱，但算进"模型时间" | 从客户端测 15 个模型、5 家提供商的 API：同样长度的请求，延迟随发出时间不同最多差 69 倍（Bian et al., 2025）\[E101\] | 预印本，UW–Madison + University of Toronto + NVIDIA | 全部 |
| III-2 | 读得多（prefill） | 每次调用把历史全部重读；截图越多越慢 | OSWorld-Human 的多调用框架里，越靠后的步越慢，最多 3 倍，因为第 k 步的提示包含前 k−1 步的截图，作者明说"由 prefill 主导"（Abhyankar et al., 2026）\[E23\]；一张截图 1,000–1,800 tokens（Anthropic, 2026a）\[E31\]；AgentSysBench 的 WebArena web agent（Kimi-K2.6）把观察从单一格式换成 AXTree + HTML + 截图，输入 4.8 倍，模型时间占比 46.9% → 61.6%（Chang et al., 2026）\[E98\]；负载高时缓存被挤掉、重读：SWE-Agent / OpenHands 在 8 张 H100 上跑 GLM-4.6 做 SWE-bench Lite，并发一多 KV 缓存抖动，请求延迟最多升到 7.14 倍（Kang et al., 2026）\[E108\] | 会议论文；厂商工程文档；预印本（HKUST）；预印本（Georgia Tech + CMU + UIUC + Together AI） | 截图型；文本型（观察大时）；缓存型（负载高时） |
| III-3 | 写得多（decode） | 逐 token 生成，串行 | 本地跑 Qwen3.6-27B / Gemma4-31B（vLLM，2 张 H100）的 ReAct agent 在五个 benchmark 上，缓存不被挤时 decode 占模型时间 91–98.6%（Yuan et al., 2026）\[E29\]；Windows 桌面 agent UFO2（GPT-4o / o1 API）每次模型调用约 10 秒，在每种配置里都是每步最大的一项（Zhang et al., 2025）\[E94\] | 预印本（UIUC + Intel + Gimlet Labs）；预印本（Microsoft） | 缓存型；截图型（单次调用的） |
| III-4 | 思考模式和大模型 | 开"思考"就写得更多，大模型每 token 更慢 | OSWorld 2.0 同一批任务上，Claude Opus 4.8 每任务输出 22.4 万 token，GPT-5.5 输出 3.7 万（XLANG Lab, 2026）\[E41\]；HAL 在 9 个 benchmark、21,730 次运行里比较推理强度，调高后 36 组里 21 组准确率反而下降（Kapoor et al., 2025）\[E43\] | 预印本（香港大学）；预印本（Princeton 等） | 全部 |

### 第四类：环境慢

| 编号 | 原因 | 机制 | 证据与引用 | 来源类型 | 主要出现在哪种 agent |
| --- | --- | --- | --- | --- | --- |
| IV-1 | 生成观察 | 抽 AXTree、跑元素检测都要时间 | OSWorld 的桌面应用里生成一次 AXTree 要 3–26 秒 \[E24\]；截图本身在总任务时间里不到 2% \[E22\]（Abhyankar et al., 2026）；UFO2 里 OmniParser 元素检测每步约多花 1 秒（Zhang et al., 2025）\[E94\] | 会议论文；预印本（Microsoft） | 截图型 |
| IV-2 | 浏览器执行和页面加载 | 点了要等页面回来 | 151 个 WebVoyager 真实网站任务上，每步中位数：浏览器动作 6.6 秒 vs 模型 4.7 秒（Wong et al., 2026）\[E17\]；WebArena 上 GenericAgent + Claude 3.5 Sonnet 每步 12.2 秒里 7.6 秒在浏览器（Le Sellier De Chezelles et al., 2025，此数未复核）\[E26\] | 预印本（Princeton + Microsoft Research）；预印本（ServiceNow Research 等，机构待核） | 文本型 |
| IV-3 | 固定停顿 | agent 不知道页面什么时候准备好，只能睡固定秒数 | OSWorld 环境代码默认每步动作后停 2 秒（xlang-ai, 2026）\[E111\]；OSWorld 2.0 规定停 3 秒，318 步就是约 16 分钟纯等待（calc.）；AgentSysBench 里只调一次模型的 GUIAgent（ReAct，Kimi-K2.6 API）在 OSWorld 上 70% 以上的执行时间在桌面 sandbox（Chang et al., 2026）\[E97\] | 代码；预印本（HKUST） | 截图型（测试框架造成） |
| IV-4 | 工具长尾 | 跑测试、编译一等就是几分钟 | TraceLab 记录 43 位开发者 4,265 个 Claude Code / Codex session（2025 年 9 月到 2026 年 6 月）：超过 1 分钟的工具调用只占 4% 次数，却占 85% 工具时间 \[E19\]；每个请求平均 4.3 分钟里工具 2.5 分钟（59.8%）、模型 1.7 分钟（41.0%）\[E105\]（Zhu et al., 2026） | 预印本，University of Washington | 缓存型 coding |

### 第五类：串行（结构性乘数）

四个环节严格按顺序，互不重叠；一轮内的并发只有 1.15（Liu et al., 2026）\[E20\]。所以任务时间是上面所有项的**和**，不是**最大值**。修好任何一项，只省它自己那一份——这也是为什么必须先知道各项占比（第二节）才能谈加速。

另有一项不算 agent 的慢，但会把统计搅浑：coding agent 的一个 session 里 80–92% 的 wall-clock 是人在思考（Zhu et al., 2026 \[E105\]；Liu et al., 2026 \[E106\]）。看"总时长"的数字时要先剔掉它。

## 二、慢的箭头最后归到哪

五类原因都存在，但哪一类是大头，三种 agent 不一样；唯一对三种都成立的乘数是步数 N。表里每个原因先写名称，括号里是它在第一节表中的编号（如“读得多（III-2）”），每个数字都写明谁测的、在什么上测的、测的是什么。

|  | 截图型桌面 agent（多调用框架） | 文本型 web agent | 带缓存的 coding agent |
| --- | --- | --- | --- |
| 最重的项 | 读得多（III-2）× 每步调用多（II-1）× 步数多（I-1）。OSWorld-Human 在 39 个 OSWorld 桌面任务上逐步计时，两个多调用框架（GTA1、Agent S2）的总任务时间里有 87%–97% 花在模型的规划、判断、反思调用上，截图和执行动作合计不到 3.5%（Abhyankar et al., 2026，会议论文）\[E22\]。 | 浏览器执行和页面加载（IV-2）加上等待（IV-3）。Skim 在 151 个 WebVoyager 真实网站任务上测了三个文本型 web agent（模型 GPT-4o），每一步的中位数是浏览器动作 6.6 秒、模型调用 4.7 秒，浏览器一侧更长（Wong et al., 2026，预印本）\[E17\]。 | 写得多（III-3），或者工具长尾（IV-4），看工具轻重。开了上下文缓存后，逐 token 生成（decode）占模型时间的 91%–98.6%（Yuan et al., 2026，本地模型上测的，预印本）\[E29\]；在 Claude Code / Codex 的真实使用记录里，每个请求的时间 59.8% 在工具、41.0% 在模型（Zhu et al., 2026，预印本）\[E105\]；而工具轻的 GitHub Copilot 里，agent 时间中模型占 13.7%、工具只占 2%（Liu et al., 2026，预印本）\[E106\]。 |
| 次重的项 | 写得多（III-3）：开思考模式后每步生成的推理 token 变多，逐 token 生成的时间随之变长。 | 读得多（III-2）：观察一大就翻转成大头。AgentSysBench 里同一个 web agent 把观察从单一格式换成 AXTree + HTML + 截图，输入量变成 4.8 倍，模型时间占比从 46.9% 升到 61.6%（Chang et al., 2026，预印本）\[E98\]；Browser-Use 框架的延迟有 73% 在模型调用（Winston et al., 2026，ICML 2026 会议论文）\[E100\]。 | 读得多（III-2）：负载一高、缓存被挤掉，就得把整段上下文重读。ThunderAgent 测到缓存抖动时请求延迟最多升到 7.14 倍（Kang et al., 2026，预印本）\[E108\]。 |
| 几乎不重 | 生成观察（IV-1）和执行动作：截图加动作合计不到总任务时间的 3.5%（Abhyankar et al., 2026）\[E22\]。 | 没有可以忽略的项：模型和浏览器的分量接近，谁大取决于观察多大、模型多快。 | 纯导航的步（I-3）：coding agent 没有页面要翻，这一类不存在。 |
| 反例 | 单次调用型 agent 不一样：AgentSysBench 里只调一次模型的 GUIAgent（模型 Kimi-K2.6）在 OSWorld 上 70% 以上的执行时间花在桌面 sandbox 里（Chang et al., 2026，预印本）\[E97\]，因为测试框架在每一步动作后固定停顿：OSWorld 代码默认 2 秒（xlang-ai, 2026）\[E111\]，OSWorld 2.0 规定 3 秒（XLANG Lab, 2026）\[E6\]。 | Browser-Use 框架里 73% 的延迟在模型调用，浏览器不是大头（Winston et al., 2026，ICML 2026 会议论文）\[E100\]。 | 两份真实记录方向相反：工具重的 Claude Code / Codex 记录里工具 59.8% 大于模型 41.0%（Zhu et al., 2026）\[E105\]；工具轻的 Copilot 记录里模型 13.7% 大于工具 2%（Liu et al., 2026）\[E106\]。差别来自工具的种类（跑测试、编译 vs 读文件），不是矛盾。 |
| 一句话 | 慢在读：每一步都把之前的截图历史重读一遍，越到后面读得越多。 | 慢在环境（浏览器和页面等待）；但观察一大，就又变成慢在读。 | 读的部分被缓存省掉了，剩下的慢在写（decode）和工具（跑测试、编译）。 |

两个结论：

- **决定大头的不是 agent 的种类，是跑它的那套框架**：每步调几次模型、观察多大、有没有固定停顿、缓存开没开。同一种 agent 换一套框架，大头就翻转（D95、D96、D99）。所以"agent 慢是因为推理慢"这句话只对多调用的截图型 agent 成立。
- **步数 N 乘在所有项前面**：不管大头是读、是浏览器还是工具，少转一圈就少付一整圈的钱和时间。这是唯一对三种 agent 都成立的杠杆，也是 OSWorld 2.0 作者把"减少环境回合"单独列为目标的原因（§1.8）。

## 三、贵在哪：所有原因，分六类

钱只有两个来源：读的 token 和写的 token，各乘单价。其余四类是把这两项放大的乘数（调用次数、失败重试、单价）和没人算的部分。单价的三个比例先记住：写是读的 5 倍；命中缓存的读是正常读的 0.1 倍；fast mode 一律 2 倍（Anthropic, 2026b；OpenAI, 2026——2026 年 9 月的定价页）。

### 第一类：读的 token 多

| 编号 | 原因 | 机制 | 证据与引用 | 来源类型 |
| --- | --- | --- | --- | --- |
| Ⅰ-1 | 历史每次重发 | 第 k 次调用读前 k−1 步的全部内容，总读量 ≈ 步数的平方 | "成本随步数二次增长"（Abhyankar et al., 2026）\[E45\] | 会议论文，MLSys 2026 |
| Ⅰ-2 | 截图大 | 一张图 1,000–1,800 tokens，100 张就撞满 200K 上下文 | （Anthropic, 2026a）\[E31\] | 厂商工程文档 |
| Ⅰ-3 | 观察格式丰富 | AXTree + HTML + 截图一起送，输入 4.8 倍 | （Chang et al., 2026）\[E98\] | 预印本，HKUST |
| Ⅰ-4 | 多采样 | 每步多个候选，token 以读为主 | gpt-oss-120b + ReAct 在 165 个 WebArena-Lite 任务上，每步候选 1 → 10 个，每任务 9.6 万 → 92 万 tokens（Lee et al., 2026）\[E44\] | 预印本，UC Berkeley |
| Ⅰ-5 | 缓存不是万能 | 命中率再高，历史太长时读仍是大头；一旦不命中就全量重读 | TraceLab 的 4,265 个 Claude Code / Codex session 里，前缀缓存命中 95.7%，prefix token 仍占挂牌价成本的 59.5%；命中失败时 prefill 量是真正新内容的 3.8 倍（Zhu et al., 2026）\[E19\] | 预印本，University of Washington |

### 第二类：写的 token 多（单价 5 倍）

| 编号 | 原因 | 机制 | 证据与引用 | 来源类型 |
| --- | --- | --- | --- | --- |
| Ⅱ-1 | 思考模式 | 思考的 token 按输出计费，关不掉时就是固定开销 | OSWorld 2.0 同一批任务上，Claude Opus 4.8 每任务输出 22.4 万 token、GPT-5.5 输出 3.7 万（XLANG Lab, 2026）\[E41\]；Opus 5.5 "thinking cannot be disabled and is billed as output"（Anthropic, 2026b） | 预印本；厂商定价页 |
| Ⅱ-2 | 但写不一定是大头 | 在无缓存的截图型 agent 里，输出只占总费用的 31% | 论文正文 $2.43 = 只算输出；Table 3 全算 $7.87（Abhyankar et al., 2026）\[D7\] | 会议论文 |

### 第三类：调用次数多

步数 N 乘以每步调用次数 c，把前面两类（第一类：读的 token 多；第二类：写的 token 多）整体放大：任务有多少步、每步调几次模型，读和写的账单就乘以多少。两个例子。一是多调用框架：OSWorld-Human 测的 GTA1 框架里，每走一步先由 4 个并行的规划器各给一个候选动作，失败了最多重试 3 轮，再由一次判断调用挑选，所以每 1 次判断对应 4 到 12 次规划调用，一步的模型调用次数是单调用框架的 5 到 13 倍（Abhyankar et al., 2026）\[E25\]（倍数为 calc.）。二是多采样：Agentic Test-Time Scaling 让 agent 每一步生成 5 到 20 个候选再挑一个，每步的调用量按候选数成倍增加（Lee et al., 2026）\[E44\]。这两个乘数和“慢”的第一类（做的步数多）、第二类（每步调用的次数多）是同一件事：同一批多出来的调用，既花时间也花钱。

### 第四类：失败和重试（从"每次尝试"到"每次成功"）

| 编号 | 原因 | 机制 | 证据与引用 | 来源类型 |
| --- | --- | --- | --- | --- |
| Ⅳ-1 | 失败的尝试也要付费 | 每次成功的成本 = 每次尝试 ÷ 成功率 | OSWorld 2.0 报告最好的 agent（Claude Opus 4.8）每次尝试约 $72.4、完成率 20.6%（XLANG Lab, 2026）\[E41\]；两者相除，每次成功平均摄约 $351，这个除法是我们自己算的（calc.）。它是账面折算，不是“把同一个任务重试到成功”的真实价格。 | 预印本 + 我们的计算 |
| Ⅳ-2 | 空转的步照付 | 死循环里每一圈都是完整的读 + 写 | 一次死循环 $8.47：OSWorld-Human 剖析 GTA1 框架（o3 做规划和判断、GTA1-7B 做界面定位）在 39 个 OSWorld 桌面任务上的记录里，有一次界面定位死循环，同一步重复了 18 次，这一段花了 27 分钟、按挂牌价 $8.47（无缓存）；同一批记录里，失败且超过 50 步的任务有 66% 的步是这类无效重复（Abhyankar et al., 2026）\[E45\] | 会议论文 |
| Ⅳ-3 | 评测本身贵到跑不起 | 单次运行、无重复 | HAL 跑 9 个 benchmark、21,730 次运行、每种配置只跑一次，总花费约 $40,000；Online-Mind2Web 上 Claude Opus 4.1 因估计要 $20,000 直接没跑（Kapoor et al., 2025）\[E43\] | 预印本，Princeton 等 |

### 第五类：单价

| 编号 | 原因 | 数字 | 引用 | 来源类型 |
| --- | --- | --- | --- | --- |
| Ⅴ-1 | 模型档位 | Opus 5.5 $4 / $20 vs GPT-6 Luna $0.10 / $0.50（读 / 写，每百万 token） | Anthropic, 2026b；OpenAI, 2026 | 厂商定价页 |
| Ⅴ-2 | fast mode | 一律 2 倍价；切换速度还会使缓存失效 | Anthropic, 2026b \[E190\]；OpenAI, 2026 \[E192\] | 厂商文档 |
| Ⅴ-3 | 缓存的写和读 | 写入缓存 1.25 倍，读缓存 0.1 倍 | Anthropic, 2026b；OpenAI, 2026 | 厂商定价页 |
| Ⅴ-4 | 长上下文加价 | OpenAI 超过 272K 的请求读价 2 倍 | OpenAI, 2026 | 厂商定价页 |

### 第六类：环境机器的钱（benchmark 不报，但可以自己算）

跑 sandbox、浏览器、桌面虚拟机的机器费用，benchmark 里没有一篇报出美元数，所有“每任务多少钱”都只是 API 账单；但按小时定价可以自己算。三家 AI 按同一份 prompt 各查了一遍（2026-09-27），一手定价页的数字互相一致；下表的每任务金额和占比是我们自己算的（calc.：小时价 × 时长，只算按量计费部分）。

| 环境 | 计价（一手定价页，2026-09-27 读取） | 1 小时任务 | 15 分钟任务 | 占 $7.87 API 账单（1 小时） | 占 $72.4（1 小时） |
| --- | --- | --- | --- | --- | --- |
| Browser Use Cloud 云浏览器 | $0.02 / 浏览器小时，按分钟计、最短 1 分钟；流量另计（住宅代理 $5/GB，直连 $0.20/GB）；单次会话上限 240 分钟（Browser Use, 2026） | $0.020 | $0.005 | 0.25% | 0.03% |
| AWS t3.medium（2 vCPU / 4 GiB，Linux，us-east-1） | $0.0418 / 小时（AWS T3 产品页；另一个官方页写 $0.0416，差 0.5%）（AWS, 2026） | $0.042 | $0.010 | 0.5% | 0.06% |
| Browserbase 云浏览器 | $20/月含 100 小时、超出 $0.12/小时；$99/月含 500 小时、超出 $0.10/小时；按分钟计，每会话最短 1 分钟（Browserbase, 2026） | $0.12 | $0.03 | 1.5% | 0.17% |
| E2B / Daytona 沙箱（2 vCPU / 4 GiB） | E2B $0.000014 / vCPU·秒 + $0.0000045 / GiB·秒；Daytona $0.0504 / vCPU·时 + $0.0162 / GiB·时；两家算出来都是 $0.1656 / 小时（E2B, 2026；Daytona, 2026） | $0.166 | $0.041 | 2.1% | 0.23% |
| Modal 沙箱（1 物理核 = 2 vCPU，4 GiB） | $0.00003942 / 核·秒 + $0.00000667 / GiB·秒 → $0.238 / 小时；按“申请量和实际用量取大”计费（Modal, 2026） | $0.238 | $0.060 | 3.0% | 0.33% |
| AWS t3.2xlarge（8 vCPU / 32 GiB，OSWorld 2.0 的默认实例） | $0.3341 / 小时（AWS, 2026；XLANG Lab, 2026） | $0.334 | $0.084 | 4.2% | 0.46% |
| OpenAI 托管容器（Hosted Shell / Code Interpreter，4 GB） | $0.12 / 20 分钟会话 → $0.36 / 小时；1 GB $0.03、16 GB $0.48、64 GB $1.92 每 20 分钟（OpenAI, 2026 定价页） | $0.36 | $0.12 | 4.6% | 0.50% |

- 结论：CPU 环境的机器钱是 API 账单的零头——1 小时任务占 $7.87 账单的 0.3–4.6%，占 $72.4 账单的 0.03–0.5%。第四节里“环境等待只慢不贵”对机器这一侧成立。
- 四个例外会把它放大：（1）固定月费——Browserbase $20/月、E2B Pro $150/月，跑不满小时数时摄到每任务比按量费高得多；（2）流量——住宅代理 $5–12/GB，1 GB 流量抵 Browser Use 40 小时的浏览器时间；（3）按 wall-clock 计费而 agent 大部分时间在等——AgentSysBench 的生产记录里，中位数会话只有 20% 的存活时间在执行（Chang et al., 2026）；（4）GPU 沙箱——Daytona 的 H100 按需 $3.95/小时，1 小时就是 $7.87 账单的一半；AgentSysBench 里跑科学模拟的 GPU 容器，沙箱费占每请求成本 99% 以上。
- benchmark 怎么处理：OSWorld、OSWorld-Verified、OSWorld 2.0、TheAgentCompany、WebArena 都写了用什么机器（t3.medium / t3.large 控制器、t3.2xlarge、托管网站的 t3a.xlarge + 1000 GB 磁盘），但没有一份给机器的美元数。OSWorld 2.0 的 “Cost/task”（$72.4）没说是否含 AWS 和代理费，从它随输出 token 变化看基本是 API 账单（XLANG Lab, 2026）；HAL 的约 $40,000 是按每 token 价格算的 API 费用，排行榜的 “Cost” 明确定义为 API 总费用（Kapoor et al., 2025）；TheAgentCompany 的成本指标明确定义为 token 费用。只有 AgentSysBench 把沙箱费单列，但只给百分比不给美元（Chang et al., 2026，§4.5 Fig. 8）。
- 产品怎么处理：Meta Muse（2026-09-08 发布）明说“跑在一台专属的云端电脑上，有自己的浏览器”（Meta, 2026）；OpenAI 的 ChatGPT agent 说“用自己的虚拟电脑”、Operator 说“用自己的浏览器”（Operator 已于 2025-08-31 停用，agent 并入 ChatGPT Work）；Claude in Chrome 跑在用户自己的 Chrome 里，没有厂商虚拟机。没有一家公布每个会话的环境成本或价格；订阅价（Muse 免费 / $20 / $100 每月）不是环境成本。
- 三家报告的分歧和我的核对：Gemini 那份说 Browser Use 会话上限 15 分钟、没找到 Meta 的产品，两条都不对（Browser Use 的 API 文档写 240 分钟；Meta 新闻稿我们直接读过）；它独有的 “Windows Agent Arena 全部虚拟机约 $8” 在 arXiv 正文里没有，待核；OpenAI 托管容器的定价只有 Gemini 提到，已到 OpenAI 定价页核实。

### 四种口径，选错差 30 倍

| 口径 | 例子 | 差多少 |
| --- | --- | --- |
| 只算写 vs 读写全算 | OSWorld-Human 的 GTA1 框架（o3 做规划和判断，按 o3 挂牌价读 $2 / 写 $8 每百万 token，无缓存）在 39 个 OSWorld 任务上：论文正文说每任务 $2.43，这个数只算了输出 token；把他们 Table 3 的输入和输出全算上是每任务 $7.87（Abhyankar et al., 2026；核对过程见 D7） | 3.2 倍：同一次运行、同一批任务，只是算不算读的 token |
| 每次尝试 vs 每次成功 | OSWorld 2.0 的 108 个长任务上，Claude Opus 4.8（批量动作设置）每次尝试约 $72.4、完成率 20.6%（XLANG Lab, 2026）\[E41\]；$72.4 ÷ 20.6% ≈ $351，除法是我们自己算的（calc.） | 4.9 倍：同一个模型、同一批任务，分母从“每次尝试”换成“每次成功”；是账面折算，不是把同一个任务重试到成功的真实花费 |
| 无缓存 vs 有缓存 | 定价页上命中缓存的读是正常读的 0.1 倍（Anthropic, 2026b；OpenAI, 2026）；但 TraceLab 记录的 4,265 个 Claude Code / Codex session 里，前缀缓存命中 95.7%，prefix token 仍占挂牌价成本的 59.5%——因为每步要读十几万 token 的历史，打一折之后仍是大头（Zhu et al., 2026）\[E19\] | 读的单价差 10 倍；整张账单省多少取决于读占多大比例、命中多少：截图型 agent 的测量都没报缓存状态 \[D101\]，coding agent 的实际省幅远小于 10 倍 |
| 标准 vs fast mode | Anthropic fast mode：Opus 5.5 从读 $4 / 写 $20 变成 $8 / $40，Opus 5 和 Opus 4.8 从 $5 / $25 变成 $10 / $50（每百万 token），厂商自述输出速度最多 2.5 倍、不改首个 token 的等待，切换速度会使缓存失效（Anthropic, 2026b）\[E190\]；OpenAI fast mode：所有列出模型一律 2 倍挂牌价，“最多 2.5 倍”的速度只对 GPT-5.6 Sol 公布（OpenAI, 2026）\[E192\] | 2 倍：同一模型、同样的 token 数，只换速度档；买到的只是“写”的速度，“读”和排队不变 |

老板问"一个任务多少钱"，正确的回答是先问哪种口径。

## 四、慢和贵怎么连起来

慢和贵高度相关但不是同一件事：第零节的两个式子共用"读的 token"和"写的 token"两项，而环境时间和排队只在时间的式子里。由此每个原因和慢、贵的关系只有三种：「同源」——同一个原因同时进两个式子，比如多读的 token 既让模型多花时间也让 API 多收钱，修掉它时间和钱一起省；「只慢不贵」——只进时间的式子，比如排队和等页面加载，不产生 token；「用钱换时间或换准确率」——两个式子反向，花更多钱买更快或更准。

| 原因 | 对时间 | 对钱 | 关系 |
| --- | --- | --- | --- |
| 步数多 N | 大致随步数线性增长：多一步就多一次模型调用和一次等待（靠后的步因为读得多会再慢一些，最多 3 倍 \[E23\]） | 写的 token 随步数线性增长；读的 token 随步数平方增长，因为每一步都把之前全部历史重读一遍 \[E45\] | **同源**：步数多既慢又贵，但钱涨得比时间快：步数翻一倍，时间大约翻一倍，读的 token 账单大约翻四倍（无缓存时） |
| 每步调用多 c | 线性 | 线性 | **同源** |
| 读得多（历史、截图、丰富观察） | prefill 时间，越后越慢（Abhyankar et al., 2026）\[E23\] | 读的 token 钱（同上）\[E45\] | **同源**：同一批 token 既花时间又花钱 |
| 写得多（思考） | decode 时间，每 token 十几毫秒 | 写的 token 钱，单价 5 倍 | **同源**，而且是最贵的时间：写是每 token 最慢、每 token 最贵的那部分 |
| 缓存命中 | 省 prefill 时间 | 读价 0.1 倍 | **同源**，但脆：改历史、切换 fast mode 都会失效（Anthropic, 2026b）\[E190\] |
| 排队 | 慢 | 不花钱 | **只慢不贵**；想不排队得买 fast / priority，2 倍价 |
| 环境等待（页面加载、固定停顿） | 慢 | 不花 API 的钱；机器按小时计费，CPU 沙箱 $0.02–0.36 / 小时，通常不到 API 账单的 5%（第三节第六类） | **只慢不贵** |
| 工具长尾（测试、编译） | 慢 | 不花 API 的钱 | **只慢不贵** |
| 失败、空转、重试 | 慢 | 贵 | **同源**，而且把"每次尝试"变成"每次成功" |
| fast mode | 写快最多 2.5 倍（厂商自述），读不变 | 2 倍价 | **用钱换时间** |
| 更大的模型、更多思考 | 更慢 | 更贵 | **用钱和时间换准确率**，而且越往上越贵——成本随准确率的曲线是凸的（convex），意思是每多提高一个百分点，要花的钱比上一个点更多（同一模型上每提高一个点的边际 token 从 10.1 万涨到 57.5 万，5.7 倍，Lee et al., 2026 \[E44\]）：6×（XLANG Lab, 2026 \[E41\]）/ 9×（Kapoor et al., 2025 \[E43\]）/ 9.6×（Lee et al., 2026 \[E44\]）；多思考还不一定更准（Kapoor et al., 2025）\[E43\] |
| 更小的模型 | 更快 | 更便宜 | 但准确率掉 → 步数和重试涨 → 可能又慢又贵（推断，无直接证据） |

你举的例子——思考得久所以 token 多——就是"同源"关系的典型：思考 = 写的 token，逐个生成所以慢，单价最高所以贵，一个原因同时进两个式子。

### 时间–钱–准确率三角

三个量两两相连：

- 时间和钱：同源部分（token）一起涨跌；只慢不贵的部分（等待）可以花钱买短。
- 钱和准确率：凸的——每多一个点越来越贵（XLANG Lab, 2026 原话：每多一个点约 25–30K tokens）\[E41\]。
- 时间和准确率：双向——多思考未必更准（Kapoor et al., 2025）\[E43\]；反过来，慢本身会降准确率：页面在变，截图拍早了就按错（XLANG Lab, 2026 的 stale-state 失败模式，§1.8）。

### 从这张表能推出"修什么能省什么"

| 如果做的是 | 省时间 | 省钱 | 代价 |
| --- | --- | --- | --- |
| 少转圈（减少步数、批量动作、跳过导航步） | 是 | 是，而且是平方项 | 要知道哪些步不用想 |
| 少读（裁历史、压截图、缓存） | 是 | 是 | 裁多了会忘；裁历史本身会打掉缓存 |
| 少写（关思考、换小模型） | 是 | 是 | 准确率可能掉 |
| 少调（去掉判断 / 反思调用） | 是 | 是 | 靠这些调用纠错的任务会变差 |
| 把等待重叠起来（预加载、并行工具、事件驱动代替固定停顿） | 是 | 不省 | 只对环境为大头的 agent 有用 |
| 买 fast / priority | 是（只提写速） | 反而贵 2 倍 | 读不变快；切换会丢缓存 |
| 不重试失败（早停、识别死循环） | 是 | 是 | 会错杀还能成功的尝试 |

一句话收住：**出在 token 上的原因，修了时间和钱一起省；出在等待上的原因，修了只省时间；花钱买速度只买得到写的那一段。**

## 五、这条链上还没有人测清楚的

这些是证据的缺口，不是"研究空白"；它们决定了哪些话在 slides 上只能说到什么程度。

| 缺口 | 现状 | 后果 |
| --- | --- | --- |
| 前沿 API 模型的读 / 写时间拆分 + 缓存命中率 | 没有任何一个测量同时报告这两项；唯一的读 / 写拆分是本地 27–31B 模型（Yuan et al., 2026）\[E29\]；截图型 agent 的测量都没报缓存状态 \[D101\] | "87–97% 在模型"里多少是读、多少是写、开缓存后剩多少，都不知道 |
| agent 比人慢多少 | 17 个 benchmark 里没有一个在同一批任务上同时测 agent 和人的 wall-clock；最接近的是 AXIS 的用户研究，界面 agent 比人手动慢 1.69 倍（Lu et al., 2025，ACL 2025 会议论文，样本小）\[E161\] | "比人慢 X 倍"这句话放不上 slides |
| 环境机器的钱 | benchmark 不报美元数，只有 AgentSysBench 给了比例；产品不公布每会话成本。但按实例类型 × 时长 × 定价可以算：CPU 环境通常是 API 账单的 0.3–5%（第三节第六类） | 所有 benchmark 的成本数字都只是 API 账单；对 CPU 环境漏掉的是零头，对 GPU 沙箱和长时间空转的会话则不是 |
| OSWorld-Human 的"动作"是否包含每步 2 秒停顿 | 未报告（xlang-ai, 2026 \[E111\]，待定）；如果包含，动作占不到 2% 就意味着每步平均超过 100 秒（calc.） | "环境不到 3.5%"可能低估了等待 |
| 小模型换准确率的反弹 | 没有直接证据说明准确率掉了之后步数和重试涨多少 | 第四节最后一行只能标"推断" |
| 慢对准确率的影响有多大 | 只有 OSWorld 2.0 记录了 stale-state 这一失败模式（XLANG Lab, 2026），没有它占失败的比例 | 只能说"存在"，不能说"多大" |

## 六、参考文献

正文的引用写法是作者–年份：（第一作者 et al., 年份），机构作者就写机构名（XLANG Lab, 2026；Anthropic, 2026a）；后面的 \[E 号\] 是 dossier v3 台账的条目号，回查原始数字和测量口径用，不是文献。每条末尾标来源类型（对应我们之前的 A–D：会议或期刊论文 = 原 A；厂商一手资料 = 原 B；行业报告 = 原 C；预印本 = 原 D）和它支撑的台账条目。厂商营销数字不作来源。作者、机构、版本和日期均于 2026-09-27 核对过 arXiv / ACL Anthology 页面；标“待核”的除外。

- Abhyankar, R., Qi, Q., & Zhang, Y. (2026). OSWorld-Human: Benchmarking the efficiency of computer-use agents. In *Proceedings of the 9th Conference on Machine Learning and Systems (MLSys 2026)*, Bellevue, WA. arXiv:2506.16042v2 (18 May 2026). UC San Diego. — 会议论文。支撑 E22–E25、E45、D7。
- Anthropic. (2026a, May 13). *Best practices for computer and browser use with Claude*. https://claude.com/blog/best-practices-for-computer-and-browser-use-with-claude — 厂商工程文档。支撑 E31。
- Anthropic. (2026b). *Claude API pricing*; *Fast mode* (developer docs, read 27 Sep 2026). https://platform.claude.com/docs/en/about-claude/pricing ; https://platform.claude.com/docs/en/build-with-claude/fast-mode — 厂商定价页 / 文档。支撑 E190 和定价表。
- Artificial Analysis. (2026). *Claude Opus 5.5 (high): model page* and *Methodology* (read Sep 2026). https://artificialanalysis.ai/models/claude-opus-5-5-high ; https://artificialanalysis.ai/methodology — 第三方测量。支撑 E208。
- Bian, S., Yan, M., Jayarajan, A., Pekhimenko, G., & Venkataraman, S. (2025). What limits agentic systems efficiency? arXiv:2510.16276v1 (18 Oct 2025). University of Wisconsin–Madison; University of Toronto; NVIDIA. — 预印本。支撑 E27、E101。
- Chang, C., Zhou, Y., Fu, K., An, D., Feng, T., Lu, H., Yao, S., Guo, P., Yu, Y., Shan, Y., Li, B., Yuan, B., & Wang, W. (2026). From LLM inference to agentic workloads: Characterization and implications for serving systems (AgentSysBench). arXiv:2608.15127v1 (15 Aug 2026). Hong Kong University of Science and Technology; Alibaba Group; ByteDance. — 预印本。支撑 E97–E99。
- Gartner. (2026a, March 25). *Gartner predicts that by 2030, performing inference on an LLM with 1 trillion parameters will cost GenAI providers over 90 percent less than in 2025* \[Press release\]. https://www.gartner.com/en/newsroom/press-releases/2026-03-25-gartner-predicts-that-by-2030-performing-inference-on-an-llm-with-1-trillion-parameters-will-cost-genai-providers-over-90-percent-less-than-in-2025 — 行业报告（分析师判断）。支撑 E62。
- Gartner. (2026b, August 17). *Gartner predicts AI inference costs per agentic workflow will increase more than fivefold through 2028* \[Press release\]. https://www.gartner.com/en/newsroom/press-releases/2026-08-17-gartner-predicts-ai-inference-costs-per-agentic-workflow-will-increase-more-than-fivefold-through-2028 — 行业报告。支撑 E55。
- Kang, H., Li, Z., Xu, W., Yang, X., Chen, Y., Wang, J., Chen, B., Krishna, T., Xu, C., & Arora, S. (2026). ThunderAgent: A simple, fast and program-aware agentic inference system. arXiv:2602.13692v3 (30 Jun 2026). Georgia Institute of Technology; University of Illinois Urbana-Champaign; Carnegie Mellon University; Together AI. — 预印本。支撑 E108。
- Kapoor, S., Stroebl, B., Kirgis, P., Nadgir, N., Siegel, Z. S., Wei, B., … Narayanan, A. (2025). Holistic Agent Leaderboard: The missing infrastructure for AI agent evaluation. arXiv:2510.11977v1 (13 Oct 2025). Princeton University et al. — 预印本。支撑 E43。
- Le Sellier De Chezelles, T., Gasse, M., Drouin, A., Caccia, M., Boisvert, L., Thakkar, M., … Lacoste, A. (2025). The BrowserGym ecosystem for web agent research. arXiv:2412.05467v4 (28 Feb 2025). ServiceNow Research 等（机构待核）. — 预印本，数字未复核。支撑 E26。
- Lee, N., Erdogan, L. E., John, C. J., Krishnapillai, S., Mahoney, M. W., Keutzer, K., & Gholami, A. (2026). Agentic test-time scaling for WebAgents. arXiv:2602.12276v2 (Feb 2026). UC Berkeley. — 预印本。支撑 E44。
- Liu, B., Qiu, H., Goiri, Í., Fonseca, R., Bianchini, R., & Choukse, E. (2026). Agentic coding in the wild: Characterizing GitHub Copilot at production scale. arXiv:2608.00101v1 (30 Jul 2026). University of Illinois Urbana-Champaign; Microsoft Azure Research. — 预印本（数据是公司一手遥测）。支撑 E20、E106。
- Lu, J., Zhang, Z., Yang, F., Zhang, J., Wang, L., Du, C., Lin, Q., Rajmohan, S., Zhang, D., & Zhang, Q. (2025). AXIS: Efficient human-agent-computer interaction with API-first LLM-based agents. In *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, 7711–7743. https://doi.org/10.18653/v1/2025.acl-long.381 . Microsoft. — 会议论文。支撑 E161、D92。
- OpenAI. (2026). *API pricing*; *API changelog* (Fast mode, 30 Jul 2026; Ultrafast, 13 Aug 2026) (read 27 Sep 2026). https://developers.openai.com/api/docs/pricing ; https://developers.openai.com/api/docs/changelog — 厂商定价页 / 文档。支撑 E192、E194 和定价表。
- OpenRouter. (2026, August 25). *GPT-5.6 discounts and the Jevons paradox* \[Blog, router telemetry\]. https://openrouter.ai/blog/insights/gpt-5-6-discounts-jevons-paradox/ — 厂商一手流量数据。支撑 E211。
- Winston, C., Wang, R. Y., Mirhoseini, A., & Kozyrakis, C. (2026). Agent JIT compilation for latency-optimizing web agent planning and scheduling. In *Proceedings of the 43rd International Conference on Machine Learning (ICML 2026)*, PMLR 306. arXiv:2605.21470. Stanford University. — 会议论文（页首标注 ICML 2026；dossier 里仍记为预印本，待更新）。支撑 E18、E100。
- Wong, M., Hsieh, K., Nath, S., & Netravali, R. (2026). Skim: Speculative execution for fast and efficient web agents. arXiv:2605.16565v2 (19 May 2026). Princeton University; Microsoft Research. — 预印本。支撑 E17。
- xlang-ai. (2026). *OSWorld* \[Source code\]: desktop\_env/desktop\_env.py and run.py at commit b138d348. https://github.com/xlang-ai/OSWorld — 代码。支撑 E111。
- XLANG Lab. (2026). OSWorld 2.0: Benchmarking computer use agents on long-horizon real-world tasks. arXiv:2606.29537v2 (13 Jul 2026). The University of Hong Kong（作者署名为 XLANG Lab and Collaborators，完整名单在论文附录 A）. — 预印本。支撑 E5、E6、E41。
- Yuan, Y., Nayak, A., Kundu, S., & Talati, N. (2026). Agentic AI workload characteristics. arXiv:2605.26297v1 (25 May 2026). University of Illinois Urbana-Champaign; Gimlet Labs; Intel. — 预印本。支撑 E29。
- Zhang, C., Huang, H., Ni, C., Mu, J., Qin, S., He, S., … Zhang, D. (2025). UFO2: The desktop AgentOS. arXiv:2504.14603v2 (25 Apr 2025). Microsoft. — 预印本。支撑 E94。
- Zhu, K., Jacob, M., Ma, C., Pan, Y., Wang, S., Krishnamurthy, A., & Kasikci, B. (2026). TraceLab: Characterizing coding agent workloads for LLM serving. arXiv:2606.30560v2 (30 Jun 2026). University of Washington. — 预印本。支撑 E19、E105。
- Agent Acceleration Consolidated Dossier v3 (2026-09-27). 我们自己的证据台账；\[D 号\]（D7、D92、D95、D96、D99、D101）指它的差异表，§1.8 指它的三种 agent 综述。

环境机器成本部分的来源（三家 AI 调查交叉一致，定价页均于 2026-09-27 读取；Meta、OpenAI 定价、Browser Use 三页我们另外直接读过）：

- AWS. (2026). *Amazon EC2 T3 instances* (on-demand prices, Linux, US East). https://aws.amazon.com/ec2/instance-types/t3/ ；另一官方页 https://docs.aws.amazon.com/prescriptive-guidance/latest/optimize-costs-microsoft-workloads/right-size-selection.html 写 $0.0416。— 厂商定价页。
- Browser Use. (2026). *Pricing*; *Create browser session* (API v4 docs). https://browser-use.com/pricing ；https://docs.browser-use.com/cloud/api-v4/browsers/create-browser-session — 厂商定价页 / 文档。
- Browserbase. (2026). *Pricing*; *Plans* (billing docs). https://www.browserbase.com/pricing ；https://docs.browserbase.com/account/billing/plans — 厂商定价页 / 文档。
- Daytona. (2026). *Pricing*; *Billing* docs. https://www.daytona.io/pricing ；https://www.daytona.io/docs/en/billing/ — 厂商定价页。
- E2B. (2026). *Pricing*. https://e2b.dev/pricing — 厂商定价页。
- Modal. (2026). *Pricing*; *Sandbox resources* docs. https://modal.com/pricing ；https://modal.com/docs/guide/sandbox-resources — 厂商定价页。
- OpenAI. (2026). *API pricing*, “Tools → Containers” 行：Hosted Shell and Code Interpreter 1 GB $0.03 / 4 GB $0.12 / 16 GB $0.48 / 64 GB $1.92 per 20-minute session per container. https://developers.openai.com/api/docs/pricing — 厂商定价页。
- OpenAI. (2025). *Introducing Operator* (2025-01-23); *Introducing ChatGPT agent* (2025-07-17). https://openai.com/index/introducing-operator/ ；https://openai.com/index/introducing-chatgpt-agent/ — 厂商公告（架构表述，无环境价格）。
- Meta. (2026, September 8). *Introducing Muse: The world’s first personal AI agent built for everyone*. https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/ — 厂商公告（“专属云端电脑”为厂商自述）。
- Anthropic. (2026c). *Get started with Claude in Chrome* (support doc, 2026-08-26); *Computer use tool* (platform docs). https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome ；https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool — 厂商文档。
- XLANG Lab. (2025, July 28). *Introducing OSWorld-Verified*. https://xlang.ai/blog/osworld-verified ；OSWorld 公开评测指南 https://timothyxxx.github.io/OSWorld/user\_guides/run\_public\_evaluation.html — benchmark 作者文档（只有实例类型，无美元数）。
- TheAgentCompany. (2025). 论文 arXiv:2412.14161v3 (2025-09-10) §4.1 成本定义；仓库 README / SETUP.md. https://arxiv.org/html/2412.14161v3 ；https://github.com/TheAgentCompany/TheAgentCompany — 预印本 + 仓库文档（作者待核）。
- WebArena. (2026). *environment\_docker/README.md*. https://github.com/web-arena-x/webarena/blob/main/environment\_docker/README.md — 仓库文档。
- HAL 排行榜. (2026). Online-Mind2Web 页面的 “Cost” 定义（total API cost across all tasks）. https://hal.cs.princeton.edu/online\_mind2web — 官方排行榜。
- Chang et al. (2026) AgentSysBench §4.5 Fig. 8（沙箱 / LLM / 搜索的每请求成本占比）— 见上方条目。
- 待核：Windows Agent Arena 的 “全部虚拟机约 $8”（Gemini 报告引 OpenReview t9JUTS9ADL；arXiv 2409.08264 正文未见）；GCP e2 官方定价表（三家均为聚合站或搜索索引数据）。
