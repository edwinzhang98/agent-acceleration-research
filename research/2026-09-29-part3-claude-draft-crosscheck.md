# 第三部分草稿交叉核对：研究意图、建议与文献证据

核对日期：2026-09-29。对象为另一 Claude Code 会话的[草稿 v3](/Users/edwin/.claude/projects/-Users-edwin-projects-agent-acceleration-research/part3-verification/plan/part3-plan-draft-zh.md)，全文 523 行；本次读取时 SHA-256 为 `aa1e719bc2b0ad0e2e09c67ef7eac3aed103125fdcf7fbecef2b5eacacdef7bd`。行号均指这个快照。原稿保持不动，本记录不代表接受其中方案。

对照材料为本会话的[独立调查](2026-09-29-part3-related-work-survey.md)、[来源筛选 D313](2026-09-29-part3-source-filter.md)，以及草稿相邻目录的 `extracts/plan-cited.json`、`check/consolidated-w.json`、`check/consolidated-n.json`。那些核查记录帮助定位原文；其中“已审计”的标签不直接替代本轮核查。本次完整阅读草稿，针对影响研究意图和结论的争议点回到原文，不宣称重审了对方全部文献或复核全部附录数字。

## 1. 理解与核查表

### 1.1 对研究意图的补充理解

目前较稳妥的理解是：研究要把人工阅读 trajectory、诊断问题、修改 Agent 的试错过程变成可以持续运行的自动流程；同时，把重复环境里的交互经验积累为可复用的知识与动作，减少后续任务的无谓试错。草稿补充了一个关键支撑环节：从业务规则构造可信用例，用来判断候选改动是否保持正确、是否带来实际效率收益。

我暂把它整理为 **A 自动改进、B 环境学习，加上为两者提供反馈的 C 验证机制**。这是本轮的组织建议。“三项工程工作”是否要对外讲成“三个独立研究贡献”，尚未由这些材料确定。

| 草稿中的内容 / 定位 | 应归入什么 | 本轮如何使用 |
|---|---|---|
| 分析明显/高频错误，以及耗时或花费高的步骤，分类后改代码、prompt、新 action，或保留每次询问/规划；§4.1，102–109 行 | **本会话也能直接核实的用户要求** | 作为主目标；包括成功但低效的轨迹，不能提前把所有情况限制为某一种修法。 |
| 环境规律藏在 trajectory 里，提取后落实为更精确的 action；38–39、253 行 | **本会话也能直接核实的用户要求** | 与方向 A 共享轨迹和候选改动，但环境知识的具体表示尚未确定。 |
| 先说明准备做什么，多轮讨论后再算预算；380–382 行 | **已确认的用户要求** | 本轮仍不设实验规模或预算。 |
| 适用场景是依据成文规则进行结构化填报；42 行 | **草稿转述的新增讨论背景** | 把规则约束的填报视为重点候选场景。原对话也强调 Concur 只是例子，不能把特定平台写成方法前提。 |
| 模型经 API 调用，权重不能改；58 行 | **草稿转述的新增约束** | 工作假设为目标执行模型冻结。它没有自行解决“是否允许训练独立辅助模型”这一更细的范围问题。 |
| 模型读规则手册，生成场景/用例，人确认；40、179–185 行 | **草稿转述的新增用户设想** | 纳入对研究意图的理解；这是此前本会话没有讲清楚的反馈来源。尚不能写成已完成的数据集或已验证的轻量人工流程。 |
| 标准答案只用于判断对错，修改来自 trajectory；185 行 | **草稿转述的设计意图，边界需要澄清** | 可理解为不向修改者直接提供答案内容、不用答案做模型微调；通过/失败标签和候选选择仍会影响优化，见下文。 |
| 手动“只跑一轮且有效”；56–57、353 行；暂不展示具体结果，13 行 | **草稿转述的实验背景与展示要求** | 记录为团队经验；本会话原表述是“有一些作用”“还没有完全跑通”。缺少效果定义和实验记录，暂不作为已量化证明。遵循暂不展示具体结果的记载。 |
| 从已有轨迹开始、是否补做探索另定；335、366 行 | **草稿中的方案取向与待定项** | 可以作为低启动成本的起点；不据此把用户目标改成“永远禁止额外探索”。 |

### 1.2 属于作者建议，不能写成已确定要求

以下建议可以讨论，但本会话没有批准它们成为约束：一次只改一处；由人预先固定错误类别并与修法一一对应；正确率优先且四项成本分别受容差约束；排除全部辅助模型训练；只用程序评分；评分代码及答案完全隔离；每个用例固定重复多次；阶段 0–3 的安排；先在隔离环境自动迭代、再人工批准上线；以及§12的 slides 页面安排。

尤其应保留两项区别：**改进循环无人逐轮指导**与**业务执行/上线完全没有人工参与**是不同目标；**执行任务时仍需询问或规划**也不等于**每次都必须向人提问**。草稿在这几种含义之间有切换，后续方案需要分别定义。

### 1.3 交叉检查发现

“需修正”不等于整篇草稿不可用；下表把确定的冲突、定义范围问题和仍未证实的判断分开。引号内为短引，机制证据固定到所列原文版本；核查均为 2026-09-29，primary。

| 项 / 草稿位置 | 核查结果与依据 | 如何处理 |
|---|---|---|
| **C01 · RL 的排除推论**；46、62、71–81 行 | **需修正推论，综述转述本身基本忠实。** [自改进综述](#ref-n001) §3.3 把 scaffold 更新与其采用的固定任务策略优化框架分开；这不是排除所有外层 RL 的定理。[Harness-R1](#ref-e314) v1 §3.1–3.2 明确以冻结目标 Agent 的重跑结果训练独立修改者，使用 SFT + GRPO。不可对离散补丁直接反传，不等于没有可计算目标，也不等于修改者不能学习。草稿自己的 w010 已包含这个例子。 | “本阶段可先做无需训练的搜索循环”是可选实施方案；“不训练辅助模型”保持作者建议身份。用户早先把 RL 当可能性，不能据当前 API 约束直接取消。 |
| **C02 · 答案集只评估、不参与更新**；40、111–112、145、185 行 | **数据角色表述不准确。** 如果按用例对错生成诊断、接受或回滚候选，这些结果已经是外层优化信号。[AutoSaddler](#ref-e309) §§3–4 与 [SoL-Pi](#ref-n026) §2.1 都把开发反馈用于候选选择。隐藏答案内容与完全不利用该数据是两回事。 | 改为“不直接提供标准答案、不让循环改评分器；开发/把关反馈参与系统优化，最终测试不参与”。如果真的要求答案集完全不影响优化，就必须另设候选选择数据。 |
| **C03 · 最终留出集的使用边界**；26、114、219、311–312、332 行 | **数据可见性与评估时点未写清，尚不能说已发生泄漏。** 一处规定留出集只用于最终报告，另一处要求每轮记录它；若逐轮密封记录且不反馈研发选择，两者可以兼容。[Self-Harness](#ref-e310) §§3.3–3.4 的 held-out 参与 gate，在我们 E310 中已按验证集处理；[SoL-Pi](#ref-n026) §2.1 先冻结候选与规则，再作最终留出评价。仅禁止提议模型访问，仍无法防止研究者用曲线早停或调容差。 | 可以固定所有 checkpoint 后统一盲评；若需边跑边看曲线，就把该集合叫验证集，另留最终 test。独立测试也不能自动保证标签正确和任务代表性。 |
| **C04 · “全自动”的范围**；38、109、130、337–351 行 | **作者建议有范围扩张。** 用户明确希望自动化的是分析—修改—再试的循环，也保留每次运行时询问/规划的情况。草稿“目标仍是丙”可能把它扩大为业务提交、部署和必要询问都不经人。原对话不能支持这种扩大。 | 分开定义改进循环、业务执行、部署三个层次的人工角色。询问是否正确取决于用例的预期行为，不能把任何“向人询问”都算成功；询问对象也可能是模型或环境。 |
| **C05 · 环境模型被限定成页面图**；30、234–239、277 行 | **定义过窄。** [WMA](#ref-r14) v2 §4 使用预测状态变化描述的模型；[AutoManual](#ref-e315) v4 §3.3 学规则；[AppAgentX](#ref-r10) v3 §4 学交互链和 shortcut。图只是可能表示，页面也不自动等于完整环境状态。 | 分别比较规则、显式交互结构、预测器和可执行动作。若目标特指显式图，应明确节点、隐藏状态、前置条件和未知交互的处理。 |
| **C06 · “只用任务轨迹建 Web 环境模型”尚未找到**；239、267、277 行 | **较窄问题尚未被直接反驳，宽泛表述需要补近邻。** AutoManual/[AutoGuide](#ref-r15) 有经验到规则；AppAgentX 有执行历史到关系和动作，但在移动端；WMA 的网页转移来自专门收集。它们不能直接证明“纯被动旧 Web 日志建显式图”已完成，也不能在比较中省略。[ActionEngine](#ref-e307) v2 使用主动探索，不能算纯被动路线。 | 明确四个条件：日志是否预先存在、是否额外交互、产物形式、任务平台。既有日志可减少采集时的额外操作，不能保证覆盖完整、归纳正确或后续验证免费。观察记录与推断出的通用规则分开保存。 |
| **C07 · 学习成本曲线的遗漏**；280、282 行 | **重要漏项，非严格同口径反例。** [SpeedRunner](#ref-e271) v1 §4.3、Fig.3、App.A.2–A.3 已按训练 rollout 进度评估固定留出集的表现/成本，并处理技能诱导投入。它不等于逐个在线到达业务任务的实际费用记录，且正文与附录对 token/美元成本的表述须区分。 | 将其加入已有工作。可测的问题是目标 Web 工作负载的累计学习与执行开销；不能把“会画随经验积累的效率曲线”本身当新贡献。 |
| **C08 · token 成本与 FRAMES 把关被简化**；155、196 行 | **两处可定位的原文不符。** 草稿引用的 [FRAMES v1](https://arxiv.org/html/2608.01772v1) §3.1 把 Cost 定义为 “average LLM token consumption per case”，§3.5 用于选择，故不能说其三项中只有 RRSI 明确 token 成本。FRAMES §3.5 / App.A.9.1 的类别门槛允许相对该次演化起始技能集 P0 **5% 相对下降**，不是逐候选相对上一版严格不退步（2026-08-03 v1，primary，未复现）。**该篇当前不通过 D313，仅作草稿出处审计。** | 修正草稿事实描述，再决定是否移出正文。符合来源门槛的 [SoL-Pi](#ref-n026) §2.1 与 [RRSI](#ref-w048) v2 §3.3 可支持质量约束与效率选择已有先例；它们并不验证草稿所提四项门槛。 |
| **C09 · 未找到 wall-clock 保留门槛 → 新贡献**；159、175、279、282、378 行 | **本轮未找到足以推翻该限定检索记录的证据；新颖性推论仍过强。** [Better Harnesses, Smaller Models](#ref-e313) §IV 测量延迟，不等于用延迟决定接收候选。正文在“未核到”后又把右列描述为可做出新东西，会让读者误以为已完成创新性论证。 | 保留为待验证的具体机制或测量设定；不把它、特定业务场景或更窄限制的组合直接列成文献空白。 |
| **C10 · 两道门槛与费用分母**；161–175、313、316–317 行 | **尚未确定的协议，不是文献定理。** 四项分别限幅可能拒绝“多调用一次但总时间与金额下降”的改进。“每次成功的花费”可能指成功运行均值，也可能指所有尝试费用除以成功数，含义不同；相同调用次数也不保证资源相同。草稿已经正确要求把外层消耗分列。 | 保留作者建议标签；明确最终优化量、允许的取舍、失败费用和外层搜索是否计入。此时定义日志和分母即可，无需提前计算项目预算。 |
| **C11 · 程序评分与人工简单确认**；47、181、198–220 行 | **候选方案有依据，可靠性和人工投入未被证明。** [SOPBench](#ref-n009) §2.4/App.C 有模型生成、代码验证、最后人工复核；[Logic-Guided Synthesis](#ref-n035) v1 §4.2 要求 “unanimous agreement” 才保留规则，并另审用例。[AgentRewardBench](#ref-w091) v2 Table1 同时发现模型裁判和规则评分器会错，不能推出换成程序便完全可靠。 | 把“人简单确认”写成希望达到的工作量目标；把“纯程序评分”保留为优先验证方案。字段状态可程序核对，规则解释、提问是否必要等还需有可信标签及评分器审计。 |
| **C12 · 文献资格沿用旧口径**；74、95–96、196、附录B | **与用户最新来源规则冲突。** primary、已经抽取和经过内部审计，都不自动符合 D313。普通公司博客、个人仓库及部分仅公司署名的预印本仍被用来支撑主要判断；“已发表，或自述已录用”也混合了不同证据强度。 | 按下表移出/暂缓；正式 venue、track、确认依据分别列。去掉不合格引用，不代表该工作不存在，更不能据此扩大创新性主张。 |
| **C13 · “学界把全自动看作目标”**；85–90 行 | **自动化层次需要对齐，不能归纳成尚无自动闭环。** 草稿援引的是综述对全生命周期、人类监督或部署权限的分类；本会话的 [AutoSaddler](#ref-e309)、[Self-Harness](#ref-e310) 等则已覆盖实验范围内的自动诊断、修改和选择。一个系统有人确定目标或批准部署，不会因此抹去内部循环的自动化。 | 逐项列明哪些环节需要人，而不以一句“学界未全自动”概括现状。两份调查可能评价的是不同层次，不必把它们判为互相否定。 |

### 1.4 需要补入我方调查的文献

这些是本次交叉检查的增量，不能将“上一轮 48 篇没有收录”当成草稿错误。表内只确认本轮实际检查的范围，不复用对方审计标签来承诺已审过所有实验。

| 新线索 | 本轮已核到的内容 | 接下来如何用 |
|---|---|---|
| [HarnessFix](#ref-w003)，草稿 w003 | 失败轨迹诊断和 harness 修复的直接近邻；v2 署中科院软件所、国科大、天津大学等，满足机构门槛。 | 补入“错误归因—选择修法”的重点对照；草稿所报诊断准确率和效果数字尚未在本轮完整复核。 |
| [StarHarness](#ref-n006)，n006=w036 | 企业环境下的 harness 演化；v1 含 Mila/Université de Montréal 署名，满足机构门槛。 | 补企业环境最近邻；两份记录不能算两篇独立证据。 |
| [DarwinX](#ref-w080)，w080 | Salesforce AI Research 的 harness 演化研究，含网页环境；符合机构门槛。 | 与 DGM 分开比较，不因已收 DGM 就视为覆盖。数字和测试隔离需继续逐项读。 |
| [SoL-Pi](#ref-n026)，n026 | v1 §2.1 两道能力/效率门槛与最终留出隔离；NVIDIA、MIT、NTU 等机构背景已核。 | 对照候选验收与效率目标，避免把报告指标反推为每项 gate 的精确配置。 |
| [RRSI](#ref-w048)，w048 | v2 §3.3 / App.C.3 的噪声控制、token 约束和候选选择；Google/Stanford 等机构背景已核。 | 对照保留质量与成本权衡，不简写为每轮都更便宜。 |
| [SOPBench](#ref-n009)、[Logic-Guided Synthesis](#ref-n035) | 规则到用例和验证器的具体构造方式；UCSB/Google DeepMind、东京大学/McGill/Alberta 等机构已核。 | 补 C 的方法依据；两者不等于已证明真实填报任务上仅需少量人工确认。 |
| [AgentRewardBench](#ref-w091) | COLM 2025 [官方接收列表](https://colmweb.org/2025/AcceptedPapers.html)已确认；v2 Table1 可核评分错误。 | 补验证器本身的评价依据。 |
| [DMI](#ref-dmi)，w065 | EuroSys 2026 [官方论文列表](https://2026.eurosys.org/papers.html)已确认。机制核读 arXiv v2：将导航知识做成可调用接口；不是 AXIS。 | 补“环境知识怎样交给 Agent”的桌面接口近邻；不能直接外推为 Web 日志学习已验证。 |

### 1.5 草稿的来源资格冲突与已有一致处

以下链接只用于审计原稿的出处；“暂不纳入”不表示论文内容被证伪。没有按这些材料提出新的机制或性能结论。

| 草稿材料 | 按 D313 的处理 |
|---|---|
| n017 [LangSmith Engine](https://www.langchain.com/blog/introducing-langsmith-engine)、n018 [OpenClaw Self-learning](https://docs.openclaw.ai/tools/self-learning)、w030 [Factory Signals](https://factory.com/news/factory-signals)、w034 [Skyvern 博文](https://www.skyvern.com/blog/asking-ai-to-build-scrapers-should-be-easy-right/) | 普通公司/项目材料，移出当前正式论据。OpenClaw 不能当成 OpenAI；署名“Research”不自动满足机构门槛。 |
| n049 [karpathy/autoresearch](https://github.com/karpathy/autoresearch) | 个人项目不因作者知名度或过往任职而变成合格厂商官方材料，移出当前正式论据。 |
| n007=w088 [FRAMES](https://arxiv.org/pdf/2608.01772v1) | 有实质相关性，但目前原文仅署 BMO Financial Group，未核到合格正式 venue；暂不作方案论据，不以业务接近代替来源门槛。 |
| w115 [ERPBench](https://arxiv.org/html/2609.17885v2) | v2 全员署 Accenture Agentic AI Center of Excellence，仅自述投稿。当前证据不足以按 D313 纳入；普通企业团队名含 AI 不自动过关。其已存在不能被用来源筛选抹去。 |
| n020 [OpenAI Cookbook](#ref-vendor-openai)、n048 [Anthropic skill-creator](#ref-vendor-anthropic) | 可作头部厂商官方工程材料；前者为归档示例，后者需要固定所读 commit，不视为正式论文。 |
| n052 [GitHub Copilot 工程文章](#ref-vendor-github) | 本轮将 Microsoft/GitHub 官方工程渠道按同级厂商解释，允许作为产品实现事实；这是规则适用判断，不是独立验证或论文发表资格。 |

草稿有几项与我方调查一致，应直接保留：两个方向已经有自动闭环和技能/环境学习的先例；ActionEngine 的预热来自相同任务模板，不能据此宣称新模板泛化；探索与候选验证投入要同运行收益分开；最终研究问题与预算都尚待确定。

ActionEngine 与 DMI 的已抽查数字总体能对上原文，本轮不把它们归为大面积数值错误。需要补的是条件：ActionEngine v2 §5 评估关闭 Patcher，基线为 Claude Code + Playwright MCP；DMI v2 §5 的效率统计限成功运行，§5.5 的 “no significant change” 未见配套统计检验，宜写“平均成功率未提升”。两者均不能提供整个目标方案已经有效的证据。ActionEngine 主表与附录的建模成本实例也须保留各自口径，尚未澄清前不混算。

## 2. D-ledger 增补

**D314 — 区分已确认要求、跨会话转述与作者建议。** 新草稿补入 API 权重限制、规则生成用例和团队手动一轮等背景；本轮将其按草稿转述记录，不冒充已读取完整原讨论。A/B 与预算后置能由本会话直接确认；C 是有价值的新增设想。固定错误分类、一次一改、排除辅助训练、四项门槛和部署审批不是因此自动成立的用户要求。

**D315 — 冻结任务模型不排除外层学习。** 对 n001 综述的转述与对项目的推断需分开。已有 E314/Harness-R1 明确冻结目标模型、训练修改者；以“harness 不可微”或“目标模型 API 权重不可改”排除整个 RL 方向过强。无需训练的外层搜索仍是可选基线，不能反过来把 RL 规定为必须做。

**D316 — 澄清开发反馈、最终测试与数据隔离。** 草稿的“答案集只评估、不参与更新”与反馈驱动的保留/回滚存在定义问题；“留出集只作最终报告”与每轮监测存在协议缺口。未发生实验，不能断言已经泄漏；需明确何时冻结、谁能看到结果、哪些结果能影响搜索。

**D317 — 收窄环境学习和效率研究空白的表述。** 环境规则、显式图、预测模型与可执行动作不同。AutoManual/AppAgentX/WMA 等不能直接反驳“纯被动旧 Web 日志建图”的全部限定，但应进入最近邻。E271/SpeedRunner 已有按学习进度的效率评估曲线，不能把曲线本身写成新贡献；在线实耗与离线评估/摊销仍应分开。本轮未反驳严格限定的 wall-clock 接收门槛检索记录，也未因此确立新颖性。

**D318 — 新草稿未完全执行 D313，且补出了我方近邻遗漏。** 普通厂商博客、个人项目、FRAMES/ERPBench 等不能凭 primary 身份或内部核查记录直接纳入。HarnessFix、StarHarness、DarwinX、SoL-Pi、RRSI 等须加入后续对照。FRAMES 的 token 定义及相对起始版本的容差在草稿中被简化，修正原稿出处描述与是否允许正式引用是两项不同决定。

## 3. 建议替换文本与 E-ledger 影响

本节给出可供下一轮方案使用的文字；不改写原 Claude 草稿，也不改变 canonical v3。

**建议替换研究概述（对应草稿§1；这段是本轮组织建议）：**

> 我们希望让 Agent 根据执行轨迹持续改进：一方面，自动识别高频错误和高成本步骤，选择并实施 prompt、代码或 action 的修改；另一方面，从重复环境中的操作经历提取可复用的交互知识，把它们转成更可靠的动作。规则生成、经人确认的用例可为这两条线提供候选验证。研究要检验这些改动能否在未参与优化的任务上保持正确，并在计入学习和验证开销后减少时间与花费。

**建议替换 RL 结论（对应46、81行）：**

> 在目标执行模型通过 API 调用、权重冻结的设定下，可以先用生成—执行—验证—选择的搜索循环改进 harness。不可微不等于没有可计算目标；是否另行训练修改者或检索器，是需要讨论的研究选项，而非 API 约束自动排除的可能性。

**建议替换答案集与留出集表述（对应26、40、145、185、311行）：**

> 开发/把关用例的对错反馈用于诊断与候选选择，但标准答案内容和评分器不交给修改者改写。最终测试独立于这些选择；若要报告各轮测试曲线，先固定运行协议和所有 checkpoint，结束后统一盲评，测试结果不再影响改动、早停或容差调整。

**建议替换环境模型及空白结论（对应30、277、280、282行）：**

> 环境知识可表示为条件规则、显式交互结构或动作后果预测器，可执行 action 是利用这些知识的一种形式。我们需要验证在目标规则填报场景里，已有轨迹的覆盖是否足够、哪些规律能够可靠复用，以及额外提取、验证和维护是否值得。已有工作提供了规则学习、技能生成、主动建图和随经验积累的效率评估；目标组合是否构成方法贡献，仍需在一致任务与成本口径下比较。

E-ledger：本轮不新增或重写性能数字。E314、E310、E315、E271、E307、E313 的既有边界继续适用；新增文献先以本记录的 n/w 对照号保留，不把外部 n/w 编号直接混入本仓库 E 编号。canonical v3、原 Claude 草稿与 slides 均不改动。

## 4. 仍待明确的问题

1. API 权重限制究竟只针对目标执行模型，还是当前阶段排除一切额外训练；这决定 RL 的实验范围，但不影响继续核对无需训练的基线。
2. 规则生成用例是验证支撑，还是也要作为独立研究贡献；标签质量、规则覆盖与人工确认工作量均未在本项目验证。
3. 从已有轨迹起步是否只是默认路线；哪些未知状态值得补跑，验证新 action 所需执行是否单列。
4. 改进循环、业务执行和部署各自何时需要人；询问/拒绝/提交的正确条件由哪些可验证规则决定。
5. 质量约束与效率目标的优先级、允许的取舍、开发/验证/test 的职责，以及全生命周期成本口径。以上是待讨论事项，本轮不要求用户现在逐项作实施批准。
6. 对新增最近邻继续完成机制和实验边界的同口径比较，尤其不要把“在某种填报场景尚未找到完整组合”当成已证明的新颖性。原草稿全部165篇、附录全部数值与新增预印本的正式发表状态，本轮没有全量重审。

## 5. References

本节仅列本轮实际作为论据使用、且符合 D313 来源门槛的文献。用于指出原稿出处问题的不合格或待核材料，只在核对表中留下审计链接，不作为方案支持证据。

<a id="ref-n001"></a>

**[1] Zhe Ren; Yimeng Chen; Dandan Guo; Guowei Rong; Tonghui Li; R. B. Xiong; Qingfeng Lan; Wenyi Wang; Li Nanbo; Yibo Yang; Mingchen Zhuge; Jürgen Schmidhuber (2026).** *Self-Improvements in Modern Agentic Systems: A Survey*. arXiv preprint. [来源](https://arxiv.org/html/2607.13104v1)。

实际核读版本：[原文](https://arxiv.org/html/2607.13104v1)。 机构：School of Artificial Intelligence, Jilin University; King Abdullah University of Science and Technology (KAUST); Independent Researcher; University of Alberta; The Swiss AI Lab IDSIA/USI/SUPSI。 Li Nanbo、R. B. Xiong 按所读版本署名保留。

<a id="ref-e314"></a>

**[2] Shuai Shao; Kangning Zhang; Qingyao Li; Shijian Wang; Hao Wang; Wenxiang Jiao; Yuan Lu; Yi Guo; Weiwen Liu; Weinan Zhang (2026).** *Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories*. arXiv preprint (formal peer-reviewed venue not verified). [来源](https://arxiv.org/pdf/2608.02276v1)。

实际核读版本：[原文](https://arxiv.org/pdf/2608.02276v1)。 机构：Shanghai Jiao Tong University; Southeast University; Xiaohongshu Inc.。 [机构/发表确认依据](https://arxiv.org/html/2608.02276v1)。

<a id="ref-e309"></a>

**[3] Sungho Park; Wonjoong Kim; Rongyuan Tan; Jue Zhang; Wook-Shin Han; Pengfei Gao; Chanyoung Park; Yongqiang Yao; Rao Fu; Elsie Nallipogu; Qingwei Lin; Saravan Rajmohan; Dongmei Zhang (2026).** *AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces*. arXiv preprint（未核到正式主会/顶刊接收）. [来源](https://arxiv.org/html/2608.23041v1)。

实际核读版本：[原文](https://arxiv.org/html/2608.23041v1)。 机构：POSTECH; KAIST; Southern University of Science and Technology; Microsoft。

<a id="ref-n026"></a>

**[4] Haozhe Liu; Tian Ye; Sensen Gao; Qihang Cao; Yitong Li; Mingchen Zhuge; Duomin Wang; Ruihua Zhang; Ping Luo; Jiawang Bian; Lei Zhu; Ligeng Zhu; Enze Xie; Song Han (2026).** *SoL-Pi: Recursively Scaling Auto-Research Loops for Efficient Agent Harness*. arXiv preprint. [来源](https://arxiv.org/html/2609.20519v1)。

实际核读版本：[原文](https://arxiv.org/html/2609.20519v1)。 机构：NVIDIA; NTU; MIT。

<a id="ref-e310"></a>

**[5] Hangfan Zhang; Shao Zhang; Kangcong Li; Chen Zhang; Yang Chen; Yiqun Zhang; Lei Bai; Shuyue Hu (2026).** *Self-Harness: Harnesses That Improve Themselves*. arXiv preprint（未核到正式主会/顶刊接收）. [来源](https://arxiv.org/html/2606.09498v3)。

实际核读版本：[原文](https://arxiv.org/html/2606.09498v3)。 机构：Shanghai Artificial Intelligence Laboratory。

<a id="ref-r14"></a>

**[6] Hyungjoo Chae; Namyoung Kim; Kai Tzu-iunn Ong; Minju Gwak; Gwanwoo Song; Jihoon Kim; Sunghwan Kim; Dongha Lee; Jinyoung Yeo (2025).** *Web Agents with World Models: Learning and Leveraging Environment Dynamics in Web Navigation*. International Conference on Learning Representations (ICLR 2025), Conference. [来源](https://proceedings.iclr.cc/paper_files/paper/2025/hash/a00548031e4647b13042c97c922fadf1-Abstract-Conference.html)。

实际核读版本：[原文](https://arxiv.org/html/2410.13232v2)。 机构：Yonsei University。 [机构/发表确认依据](https://proceedings.iclr.cc/paper_files/paper/2025/file/a00548031e4647b13042c97c922fadf1-Paper-Conference.pdf)。

<a id="ref-e315"></a>

**[7] Minghao Chen; Yihang Li; Yanting Yang; Shiyu Yu; Binbin Lin; Xiaofei He (2024).** *AutoManual: Constructing Instruction Manuals by LLM Agents via Interactive Environmental Learning*. Advances in Neural Information Processing Systems 37 (NeurIPS 2024), Main Conference Track. [来源](https://proceedings.neurips.cc/paper_files/paper/2024/hash/0142921fad7ef9192bd87229cdafa9d4-Abstract-Conference.html)。

实际核读版本：[原文](https://arxiv.org/html/2405.16247v4)。 机构：Hangzhou Dianzi University; Zhejiang University (State Key Lab of CAD&CG / School of Software Technology); Fullong Inc.; NingBo Port Group。 [机构/发表确认依据](https://proceedings.neurips.cc/paper_files/paper/2024/file/0142921fad7ef9192bd87229cdafa9d4-Paper-Conference.pdf)。

<a id="ref-r10"></a>

**[8] Wenjia Jiang; Yangyang Zhuang; Chenxi Song; Xu Yang; Joey Tianyi Zhou; Chi Zhang (2025).** *AppAgentX: Evolving GUI Agents as Proficient Smartphone Users*. arXiv preprint arXiv:2503.02268 (formal venue not verified). [来源](https://arxiv.org/html/2503.02268v3)。

实际核读版本：[原文](https://arxiv.org/html/2503.02268v3)。 机构：Westlake University AGI Lab; Henan University; Southeast University; A*STAR Institute of High Performance Computing (IHPC); A*STAR Centre for Frontier AI Research (CFAR)。 [机构/发表确认依据](https://appagentx.github.io/)。

<a id="ref-r15"></a>

**[9] Yao Fu; Dong-Ki Kim; Jaekyeom Kim; Sungryull Sohn; Lajanugen Logeswaran; Kyunghoon Bae; Honglak Lee (2024).** *AutoGuide: Automated Generation and Selection of Context-Aware Guidelines for Large Language Model Agents*. Advances in Neural Information Processing Systems 37 (NeurIPS 2024), Main Conference Track. [来源](https://proceedings.neurips.cc/paper_files/paper/2024/hash/d8efbb5dd415974eb095c3f06bff1f48-Abstract-Conference.html)。

实际核读版本：[原文](https://arxiv.org/html/2403.08978v2)。 机构：University of Michigan; LG AI Research。 [机构/发表确认依据](https://proceedings.neurips.cc/paper_files/paper/2024/file/d8efbb5dd415974eb095c3f06bff1f48-Paper-Conference.pdf)。

<a id="ref-e307"></a>

**[10] Hongbin Zhong; Fazle Faisal; Luis França; Tanakorn Leesatapornwongsa; Adriana Szekeres; Kexin Rong; Suman Nath (2026).** *ActionEngine: From Reactive to Programmatic Web Agents via State Machine Memory*. arXiv preprint arXiv:2602.20502 (formal venue not verified). [来源](https://arxiv.org/html/2602.20502v2)。

实际核读版本：[原文](https://arxiv.org/html/2602.20502v2)。 机构：Georgia Institute of Technology; Microsoft。

<a id="ref-e271"></a>

**[11] Zixi Huang; Xiheng Wang; Andrew Wang; William Jurayj; Bernal Jiménez Gutiérrez; Daniel Khashabi; Nicholas Andrews (2026).** *Better, Faster, Stronger: Programmatic Skill Learning Best Reduces Agent Cost*. arXiv preprint（未核到正式主会/顶刊接收）. [来源](https://arxiv.org/html/2608.11338v1)。

实际核读版本：[原文](https://arxiv.org/html/2608.11338v1)。 机构：Johns Hopkins University。

<a id="ref-w048"></a>

**[12] Peng Xia; Rujun Han; Zifeng Wang; Yanfei Chen; Yufan Zhuang; Yoonho Lee; Chengsong Huang; Han Yu; Zhongying CuiZhu; Yifei Ming; Huaxiu Yao; Burak Gokturk; Tomas Pfister; Chen-Yu Lee (2026).** *RRSI: Regularized Recursive Self-Improvement of Agent Harnesses*. arXiv preprint. [来源](https://arxiv.org/html/2609.24972v2)。

实际核读版本：[原文](https://arxiv.org/html/2609.24972v2)。 机构：Google Cloud AI Research; Stanford University; Washington University in St. Louis; UNC-Chapel Hill。 Zhongying CuiZhu 按所读版本署名保留。

<a id="ref-e313"></a>

**[13] Chenyang Yang; Xinran Zhao; Tongshuang Wu; Christian Kästner (2026).** *Better Harnesses, Smaller Models: Building 90% Cheaper Agents via Automated Harness Adaptation*. arXiv preprint（未核到正式主会/顶刊接收）. [来源](https://arxiv.org/html/2607.08938v1)。

实际核读版本：[原文](https://arxiv.org/html/2607.08938v1)。 机构：Carnegie Mellon University。

<a id="ref-n009"></a>

**[14] Zekun Li; Shinda Huang; Jiangtian Wang; Nathan Zhang; Antonis Antoniades; Wenyue Hua; Kaijie Zhu; Sirui Zeng; Chi Wang; William Yang Wang; Xifeng Yan (2025).** *SOPBench: Evaluating Language Agents at Following Standard Operating Procedures and Constraints*. arXiv preprint；本轮未另核正式发表. [来源](https://arxiv.org/html/2503.08669v2)。

实际核读版本：[原文](https://arxiv.org/html/2503.08669v2)。 机构：University of California, Santa Barbara; Google DeepMind。

<a id="ref-n035"></a>

**[15] Da Song; Yuheng Huang; Boqi Chen; Tianshuo Cong; Randy Goebel; Lei Ma; Foutse Khomh (2026).** *Evaluating Implicit Regulatory Compliance in LLM Tool Invocation via Logic-Guided Synthesis*. arXiv preprint；本轮未另核正式发表. [来源](https://arxiv.org/html/2601.08196v1)。

实际核读版本：[原文](https://arxiv.org/html/2601.08196v1)。 机构：Shandong University; The University of Tokyo; McGill University; University of Alberta; Polytechnique Montréal。 本轮回看 v1 缓存原文§4.2及机构页；实时HTML访问不稳定。

<a id="ref-w091"></a>

**[16] Xing Han Lù; Amirhossein Kazemnejad; Nicholas Meade; Arkil Patel; Dongchan Shin; Alejandra Zambrano; Karolina Stanczak; Peter Shaw; Christopher Pal; Siva Reddy (2025).** *AgentRewardBench: Evaluating Automatic Evaluations of Web Agent Trajectories*. COLM 2025，主会；作者按官方名单. [来源](https://openreview.net/forum?id=fQcUZMPIvu)。

实际核读版本：[原文](https://arxiv.org/html/2504.08942v2)。 [机构/发表确认依据](https://colmweb.org/2025/AcceptedPapers.html)。

<a id="ref-w003"></a>

**[17] Mengzhuo Chen; Junjie Wang; Zhe Liu; Yawen Wang; Haiming Zheng; Qing Wang (2026).** *From Failed Trajectories to Reliable LLM Agents: Diagnosing and Repairing Harness Flaws*. arXiv preprint; no independently verified formal venue. [来源](https://arxiv.org/html/2606.06324v2)。

实际核读版本：[原文](https://arxiv.org/html/2606.06324v2)。 机构：State Key Laboratory of Complex System Modeling and Simulation Technology, Beijing, China; Institute of Software, Chinese Academy of Sciences, Beijing, China; University of Chinese Academy of Sciences, Beijing, China; School of Computer Science and Technology, Tianjin University, Tianjin, China。 本轮仅将其纳入来源合格的新近邻，未重审全部方法和实验数字。

<a id="ref-n006"></a>

**[18] Esakkivel Esakkiraja; Denis Akhiyarov; Vikas Yadav; Sai Rajeswar; Patrice Bechard; Sridhar Nemala; Sagar Davasam (2026).** *StarHarness: Evolving Harnesses with Stratified Search for Enterprise Environments*. arXiv preprint; no independently verified formal venue. [来源](https://arxiv.org/pdf/2608.24804v1)。

实际核读版本：[原文](https://arxiv.org/pdf/2608.24804v1)。 机构：ServiceNow; Mila; Université de Montréal。 本轮仅将其纳入来源合格的新近邻，未重审全部方法和实验数字。

<a id="ref-w080"></a>

**[19] Yifan Zhang; Yutong Dai; Juntao Tan; Luyu Yang; Rishi Mullur; Thai Hoang; Zhiyuan Hu; James Zhu; Phil Mui; Silvio Savarese; Ran Xu; Zeyuan Chen (2026).** *DarwinX: Evolving Agent Harnesses Through Natural Selection*. arXiv preprint; no independently verified formal venue. [来源](https://arxiv.org/pdf/2608.07545v1)。

实际核读版本：[原文](https://arxiv.org/pdf/2608.07545v1)。 机构：Salesforce AI Research; Salesforce Agentforce。 本轮仅将其纳入来源合格的新近邻，未重审全部方法和实验数字。 v1元数据日期与HTML题头日期不同，故引用固定版本与年份，不用题头推断发表日。

<a id="ref-dmi"></a>

**[20] Yuan Wang; Mingyu Li; Haibo Chen (2026).** *From Imperative to Declarative: Towards LLM-friendly OS Interfaces for Boosted Computer-Use Agents*. EuroSys 2026，主会；DOI 10.1145/3767295.3803576. [来源](https://doi.org/10.1145/3767295.3803576)。

实际核读版本：[原文](https://arxiv.org/html/2510.04607v2)。 机构：Institute of Software, Chinese Academy of Sciences; University of Chinese Academy of Sciences; Shanghai Jiao Tong University。 [机构/发表确认依据](https://2026.eurosys.org/papers.html)。

<a id="ref-vendor-openai"></a>

**[21] Shikhar Kwatra; Calvin Maguranis; Valentina Frenkel; Fanny Perraudeau; Giorgio Saladino (2025).** *Self-Evolving Agents - A Cookbook for Autonomous Agent Retraining*. OpenAI Cookbook, partner recipe; official vendor technical material, not peer reviewed. [来源](https://developers.openai.com/cookbook/examples/partners/self_evolving_agents/autonomous_agent_retraining)。

实际核读版本：[原文](https://developers.openai.com/cookbook/examples/partners/self_evolving_agents/autonomous_agent_retraining)。 机构：OpenAI; Bain (joint collaboration stated in Contributors)。 2025-11-04；页面已归档，不能保证当前 API 行为；作者合作方为 OpenAI/Bain，不将全部作者都记成 OpenAI 员工。

<a id="ref-vendor-anthropic"></a>

**[22] Anthropic (2026).** *skill-creator (SKILL.md)*. Anthropic official GitHub repository file; not a paper or peer-reviewed venue. [来源](https://github.com/anthropics/skills/blob/b0cbd3df15/skills/skill-creator/SKILL.md)。

实际核读版本：[原文](https://github.com/anthropics/skills/blob/b0cbd3df15/skills/skill-creator/SKILL.md)。 机构：Anthropic。 [机构/发表确认依据](https://github.com/anthropics/skills)。 记录所读版本固定为 2026-03-06 的 commit b0cbd3df15；未执行该文件或脚本。

<a id="ref-vendor-github"></a>

**[23] Tiferet Gazit (2026).** *Building an agentic memory system for GitHub Copilot*. The GitHub Blog; official product engineering article, not peer reviewed. [来源](https://github.blog/ai-and-ml/github-copilot/building-an-agentic-memory-system-for-github-copilot/)。

实际核读版本：[原文](https://github.blog/ai-and-ml/github-copilot/building-an-agentic-memory-system-for-github-copilot/)。 机构：GitHub。 2026-01-15 官方工程文章；仅作产品实现的一手说明。
