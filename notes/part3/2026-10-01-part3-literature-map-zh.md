# 第三部分文献分类图：按学到或改写的工程产物组织

2026 年 10 月 1 日 · 中文制作支持文件；拟用于英文 Slides 的两张分类表及附录

本文件服务于**固定模型权重的 Web Agent** 首轮研究。方向一是主动探索环境，方向二是从 trajectory 学习并改进自己；两方向独立成立，不要求组合。分类目的是解释已有技术与共同困难，不用篇数、分类空格或测量缺失推导新颖性。

## 1. 分类轴、范围与使用规则

- 统一轴是**跨任务留下什么工程产物，或持久改写哪个工程对象**。探索按“环境说明/条件、结构/转移、可调用操作”分三类；轨迹学习按“提示策略、经验记忆、可执行技能、执行框架”分四类。
- “自拟练习、失败诊断、主动查询、验证、维护”是学习过程；“网页、数据库、游戏”是任务环境；“是否训练、离线/在线”是边界。它们不与工程产物并排作类别。
- 探索类要求说明**知识如何从真实交互获得**；只有被动轨迹或预设资产的相关方法，在附表明确标为相邻机制，不能统称主动探索。环境图与经验关系图分别分类：页面—动作转移属于 E2，任务—反思—修复关系属于 T2。
- 技能按实际载体区分：Python函数归 T3；SkillOpt、ClawTrace 等文字技能文档归 T1；可检索的案例/工作流条目归 T2。名称里有 skill 不意味着可执行代码。
- 同一方法可有多个标签；例如 WALT 为 E1/E3，Metis 为 E1/E3 与 T2/T3。标签表示可比较的组成机制，**不表示整篇方法符合首轮全部条件**。
- 本次逐条整理[既有114篇比较稿](2026-10-01-agent-acceleration-paper-comparisons-zh.md)的方法、方向关系和边界；没有新查论文或新增全文阅读。附表覆盖该稿114个编号，不是全领域清单，也不与既有205篇或其他文献库相加。数字114只是清单长度核对（calc.），不是研究结论。
- 本文的“共同挑战”是多篇材料支持的研究综合；具体实验限制归到具体论文，不把全部作者说成提出同一理论。出处均可沿编号回到原条目及其一手来源；来源资格沿用[已有书目](2026-10-01-two-directions-literature-zh.md#references)。

## 2. 方向一：探索环境——按学到的产物分类

可直接改成正文分类表。英文类名保留，解释和边界留作中文审稿依据；每行正文只讲一个代表，其余放该行脚注或附录。

| 类别／英文标签 | 产物与实际工程做法 | 同类工作与正文代表 | 多篇共同挑战；证据边界 |
|---|---|---|---|
| **E1 环境说明与条件规则** / **Documentation & Conditions** | 保存参数含义、必填条件、返回格式、事实与例外；构造不同调用/状态，读取真实反馈，修订可读说明或条件。 | DRAFT (#9)、FormNexus (#16)、Grounding Agent Memory (#109)、Metis (#83)；WorldEvolver (#94) 的文字转移规则为非Web补充。**代表 DRAFT**：说明从调用→报错→新版文档的链条最完整，且为ICLR主会；明确它是工具调用基准，Web落地另验。若必须使用纯Web例子，FormNexus可作机制示意，但它是表单测试，来源资格需从既有审计确认后再上正文。 | **局部反馈不足以推出通用规则，规则增加也可能带来冗余。** DRAFT 有从单次报错过度概括的例子；Grounding 通过补查来缩小记忆范围；Metis 区分事实/陷阱与可编译计划。核实某条事实不等于已覆盖最终业务约束；文字读取与整理也有成本。DRAFT 不提供完整任务耗时证据，Grounding执行者费用漏整理/探测维护，不能写成这一类已证明全面提速。 |
| **E2 页面、状态与转移结构** / **State & Transition Structure** | 保存页面模板、元素/功能关系、状态—动作—下一状态图；后续搜索已有路径、匹配参数，减少重复认路和规划。 | ActionEngine (#1)、MobileGPT (#10)、Web Application Testing / STG (#3)；AppAgentX (#41) 为被动轨迹相邻，Skim (#18) 为模板路径相邻。**代表 ActionEngine**：直接面向Web，说明“建图→程序执行”；MobileGPT以正式MobiCom工作补充路径记忆证据，但移动端条件单列。 | **页面看起来相似不等于状态相同，记录过的路径不等于新条件下仍有效。** ActionEngine 的任务模板预热与关闭修补、MobileGPT 的换参暖启动和人工修复、AppAgentX 的失配回退共同要求分清状态匹配、参数泛化与环境变化。ActionEngine/ MobileGPT 已有时间或费用收益，不能概括成“都没测效率”；收益受预热、重复路径与维护范围约束。 |
| **E3 可调用操作与接口技能** / **Executable Operations** | 把发现的操作写成带参数和适用条件的函数/API封装，通过真实执行检查后供后续任务调用，减少逐步模型决策。 | WALT (#22)、SkillWeaver (#17)、AXIS (#4)、OS-Copilot (#13)、Voyager (#21)、Shadow APIs (#107)。**代表 WALT**：ICLR主会、Web环境，展示从功能探索到工具；SkillWeaver作同类交叉证据。AXIS为Word、Voyager为Minecraft，不作Web效果替代。 | **能运行不等于做对，能在练习题运行不等于后续参数和页面都适用。** SkillWeaver 发现吞异常仍过验的坏函数；WALT 依赖输入约束与测试且部署后修补尚待推进；Voyager亦有目标/裁判误判。SkillWeaver未测实际时费；WALT已报构建费但简化回本不是完整净收益；首次探索、参数测试、使用和维护要一起核算。 |

### 探索方向应从三类归纳的共同问题

1. **探哪些变化才获得有用知识？** 文档类要覆盖参数与错误分支，结构类要覆盖状态/页面，操作类要覆盖可复用功能。三者都要把交互预算花在未来任务可能使用的内容上；不是先假设探索越多越好。（#9、#1、#17、#22）
2. **观察支持的是哪一条规律，其边界在哪里？** 单次成功、无异常、图里存在一条边都不是业务任务的完整正确性保证。要区分事实、预测、局部操作检查和最终状态评分。（#9、#17、#83、#109）
3. **知识是否减少后续实际工作，能否抵销获取与维护成本？** 文档增加读取，图要匹配状态，工具要测试/修复；因此在相同任务质量下比较实际时间和累计费用，分别测换参、新组合和变化。（#1、#10、#22、#109）

这些是三类共享的实验困难，不是三项已经确认空白。我们的探索流程应覆盖“提出探索问题→设计交互→形成/修订产物→独立验证→未来任务使用”；可以选一个环节先改进，但方向不缩成检查已有技能。

## 3. 方向二：从 trajectory 学习——按被改写的工程对象分类

| 类别／英文标签 | 产物与实际工程做法 | 同类工作与正文代表 | 多篇共同挑战；证据边界 |
|---|---|---|---|
| **T1 提示、指令与策略文档** / **Prompts & Policies** | 从执行轨迹的成败和反馈修改指令、示例、固定手册或文字技能；后续模型仍负责解释并执行。 | GEPA (#66)、ACE (#34)、AvaTaR (#44)、MIPRO (#85)、SkillOpt (#96)、ClawTrace (#111)、ESPO (#112)。**代表 GEPA**：ICLR主会，轨迹反馈→候选提示→选择过程清楚；ACE补充运行中的手册更新。 | **反馈归因会错，候选在筛选题上变好未必迁移；优化本身也贵。** GEPA大量rollout用于验证；ACE受伪反馈污染；ESPO依赖错误标签并做稳定选择。改短提示/更少搜索rollout不能直接当部署提速。ESPO已有单样本推理延迟，不能说它只测提示长度，也不能外推为多步Web任务效率。 |
| **T2 经验、案例与工作流记忆** / **Experience Memory** | 把成败轨迹抽象成可检索的建议、案例、文字工作流及效用值；运行时选择读什么，任务后增改删。 | AWM (#31)、ReasoningBank (#87)、ExpeL (#59)、EXG (#58)、SEDM (#92)、WebCoach (#104)、MemRL (#80)。**代表 AWM**：ICML主会、Web任务，具体展示参数化文字工作流；ReasoningBank补充失败经验与检索。 | **错误裁判/坏经验会传播，检索与阅读可能吃掉节省，相关不等于有用。** AWM和ReasoningBank依赖成功/失败判断；ACE也显示反馈质量问题；WebCoach少步骤却更慢；MemRL按实际效用更新。AWM正式版已分列归纳/评估token，不能说完全不计学习；ReasoningBank少步骤与总token增加须分开；WebCoach是直接时间反例。 |
| **T3 可执行技能与工具库** / **Executable Skills** | 将历史轨迹归纳成参数化函数，或根据执行反馈增删改已有函数，后续直接调用；固定执行框架可以不变。 | ASI (#74)、SpeedRunner (#46)、SkillWeaver (#17)、Metis (#83)、CRAFT (#50)、AgentDistill (#33)、SKILL.nb (#108)、TraceCompiler (#106)。**代表 ASI**：COLM主会、Web任务，展示从成功轨迹→Python技能→重跑验收；SpeedRunner补充持续改库和费用目标，但模拟/游戏环境条件单列。 | **怎样保持语义正确、跨参数复用且不过度增加工具选择负担？** ASI重跑检查实际调用及结果；SkillWeaver局部验收可能漏错；Metis编译检查不保证任务达标；SpeedRunner不做独立重放验收。一次技能调用不能当一次底层操作；SpeedRunner账含归纳者摊销而非纯执行者；各方案的构建与维护边界不同。 |
| **T4 执行框架与控制代码** / **Execution Harness** | 按轨迹定位到提示/接口/函数/控制环节，修改编排、上下文、恢复、停止或工具封装；通过回归验收后更新Agent版本。 | HarnessFix (#62)、Growing Harness (#105)、StarHarness (#99)、AgentDevel (#32)、SICA (#24)、SoL-Pi (#113)、Trace (#103)。**代表 HarnessFix**：细粒度诊断到局部修补最清楚；Growing Harness作Web/检索效率同类证据。二者为合格预印本，不能标成主会；SICA为编码任务补充。 | **轨迹症状怎样定位到真实原因，修好一类怎样不伤另一类？** HarnessFix限制补丁并回归检查；AgentDevel检查对→错；Growing Harness验收总体质量但仍有最终退步设置；StarHarness隔离搜索与选择。大量候选测评/回归需计入投入；提高完成率或节省部署调用都不自动证明完整净收益。SoL-Pi费用口径与旧材料不一致，本稿不引用其费用数值或作缺项断言。 |

### 轨迹学习方向应从四类归纳的共同问题

1. **把轨迹里的症状变成可执行修改，而不只生成一段解释。** 同一错误可能来自提示、记忆、工具或框架；GEPA、ASI、HarnessFix分别展示不同修改层级，不能让“反思”包办全部机制。
2. **验证新版本有效且旧能力没有被悄悄损坏。** 提示过拟合、坏记忆传播、坏函数过验、框架回归是不同产物上的同一验收压力；开发、选版、最终测试要分开。（#34、#17、#62、#88）
3. **既看失败，也看成功轨迹中的冗余；最终测实际运行与全投入。** Metis、SpeedRunner、ClawTrace、Growing Harness各有处理浪费的机制；不能把“纳入成功轨迹”当尚无先例。文字、记忆、工具、代码的额外调用负担不同。（#83、#46、#111、#105）

两方向共享验证和成本问题，但无需合并成一个系统。分类页之后，实验页应回答：首轮准备在哪一类产物、哪一个明确环节做比较，以及如何和该类完整方法比较，而不是只列原系统对照。

## 4. 英文正文两张表的建议压缩形式

**Environment Exploration: What Is Learned?**

| Learned artifact | Representative | Shared challenge |
|---|---|---|
| Documentation & conditions | DRAFT; Grounding Agent Memory | Establishing valid conditions from limited interactions |
| State & transition structure | ActionEngine; MobileGPT | Matching states and reusing paths under change |
| Executable operations | WALT; SkillWeaver | Verifying reusable actions and recovering construction cost |

前两行有非Web机制代表，演讲时必须说明范围；如需每行只留一篇，用DRAFT、ActionEngine、WALT，脚注保留同类交叉支持。不能将DRAFT的工具基准结果说成完整Web自动化效果。

**Trajectory-Based Improvement: What Changes?**

| Modified artifact | Representative | Shared challenge |
|---|---|---|
| Prompts & policies | GEPA; ACE | Reliable feedback and generalization beyond selection tasks |
| Experience memory | AWM; ReasoningBank | Useful retrieval without error propagation or excess context |
| Executable skills | ASI; SpeedRunner | Correct abstraction, reuse and maintenance |
| Execution harness | HarnessFix; Growing Harness | Fault localization, regression control and net benefit |

每行代表只是讲解入口。上屏可选一篇，口头用另一篇解释共同挑战或反例；不能先挑喜爱的论文再编类别。正文不放方法篇数或跨论文加速排名。

## 5. 训练边界与不宜硬塞入两方向的工作

- WMA (#114) 训练环境预测器和评分器；AutoDroid-V2 (#2)、ComputerRL (#5)、Fara (#8)、SEAgent (#15)、Space (#26)、FireAct (#60) 训练执行模型；Executable Agentic Memory (#7)、CODESKILL (#47)、Harness-R1 (#70)、PROMST (#86) 训练辅助模型。**执行者冻结不等于整套方案固定权重**，这些不进首轮主方案。
- WorldEvolver (#94) 用冻结模型加文字规则/转移样例更新，不应因为叫world model就误判为训练方法；但它不是Web端到端加速的主证据。Memento (#78)、DSPy (#52) 按无训练/训练分支分开。MemQ (#79)、MemRL (#80) 更新条目效用，不因名称含RL就自动排除。
- 软件测试 (#3、#14、#16) 可借鉴覆盖/约束发现，不直接证明业务Agent跨任务提速；对话记忆、Minecraft、移动端与编码研究用于机制借鉴，不能替代Web实测。
- AI Agents That Matter (#38)、预算对照研究 (#110) 是评价依据，不伪装为新学习算法。计划缓存与推测执行可减重复工作，但是否持续自改、是否主动探索应单独说明（#23、#35、#97、#98）。

## 6. 114篇可追踪映射附表

每篇一行，编号沿用比较稿。E/T标签是**产物关联**，不是合格方法计数；“—”表示未直接落入该方向的产物类。最后一列对主动/被动、任务领域、训练与评价边界作限定。主类与辅类可重叠，本表不用于计算各类占比。每个题名链接到逐篇问题、方法、结果和原文定位；完整发表资格与阅读版本由该记录和既有书目承接。

| 编号与论文（本地可追踪） | 环境产物关联 | 改进对象关联 | 本轮使用边界 |
|---|---|---|---|
| [1. ActionEngine: From Reactive to Programmatic Web Agents via State Machine Memory](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-1) | E2,E3 | T3 | Web；主动建图；在线修补存在但主评测关闭 |
| [2. AutoDroid-V2: Boosting SLM-based GUI Agents via Code Generation](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-2) | E1,E2 | — | 训练边界：移动端执行模型微调 |
| [3. Automated Web Application Testing: End-to-End Test Case Generation with Large Language Models and Screen Transition Graphs](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-3) | E2 | — | Web测试工具；产物是测试图/脚本，非跨任务Agent改进 |
| [4. AXIS: Efficient Human-Agent-Computer Interaction with API-First LLM-Based Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-4) | E3 | T3 | 机制借鉴：Microsoft Word；界面到API技能 |
| [5. ComputerRL: Scaling End-to-End Online Reinforcement Learning for Computer Use Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-5) | — | — | 训练边界：策略RL |
| [6. Dual-Scale World Models for LLM Agents Towards Hard-Exploration Problems](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-6) | E1,E2 | T2 | 机制借鉴：游戏内探索；非独立Web任务迁移 |
| [7. Executable Agentic Memory for GUI Agent](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-7) | E2,E3 | T3 | 训练边界：辅助Q模型；不能当全系统固定权重 |
| [8. Fara-7B: An Efficient Agentic Model for Computer Use](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-8) | — | — | 训练边界：探索轨迹用于模型蒸馏 |
| [9. From Exploration to Mastery: Enabling LLMs to Master Tools via Self-Driven Interactions](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-9) | E1 | T1 | 工具调用基准；主动修订说明；非完整网页工作流证据 |
| [10. MobileGPT: Augmenting LLM with Human-like App Memory for Mobile Task Automation](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-10) | E2,E3 | T3 | 机制借鉴：移动应用；部分人工修复 |
| [11. MrSteve: Instruction-Following Agents in Minecraft with What-Where-When Memory](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-11) | E2 | T2 | 机制借鉴：Minecraft；依赖训练导航器 |
| [12. OpenSkill: Open-World Self-Evolution for LLM Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-12) | E3 | T3 | 资料与自建练习驱动；非真实应用规则验证 |
| [13. OS-Copilot: Towards Generalist Computer Agents with Self-Improvement](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-13) | E3 | T3 | 机制借鉴：桌面/办公应用；自主练习 |
| [14. Planning to Explore: Curiosity-Driven Planning for LLM Test Generation](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-14) | — | — | 机制借鉴：代码覆盖探索；不评跨任务资产复用 |
| [15. SEAgent: Self-Evolving Computer Use Agent with Autonomous Learning from Experience](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-15) | — | — | 训练边界：执行者与界面裁判训练 |
| [16. Semantic Constraint Inference for Web Form Test Generation](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-16) | E1,E2 | — | Web表单测试；约束可借鉴，非端到端Agent加速证据 |
| [17. SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-17) | E3 | T3 | Web；主动练习并更新技能 |
| [18. Skim: Speculative Execution for Fast and Efficient Web Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-18) | E2,E3 | — | Web；离线网站模板复用，持续自改证据有限 |
| [19. STELLA: Self-Evolving LLM Agent for Biomedical Research](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-19) | — | T2,T3 | 机制借鉴：生物医学；模板与工具积累 |
| [20. VASO: Formally Verifiable Self-Evolving Skills for Physical AI Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-20) | — | T3 | 机制借鉴：物理环境；形式化契约不都由探索学出 |
| [21. Voyager: An Open-Ended Embodied Agent with Large Language Models](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-21) | E3 | T3 | 机制借鉴：Minecraft；冻结LLM，主动练习 |
| [22. WALT: Web Agents that Learn Tools](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-22) | E1,E3 | T3 | Web；主动探索造工具；部署后持续修补未充分验证 |
| [23. A Plan Reuse Mechanism for LLM-Driven Agent](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-23) | — | T2 | 计划缓存邻近；不含系统性失败修订 |
| [24. A Self-Improving Coding Agent](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-24) | — | T4 | 机制借鉴：编码Agent；质量/时间/费用用于版本选择 |
| [25. A-Mem: Agentic Memory for LLM Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-25) | — | T2 | 机制借鉴：长期对话；非执行成败驱动 |
| [26. Act More, Decide Less: Skill-Guided Adaptive Action Chunking for Long-Horizon LLM Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-26) | — | — | 训练边界：动作块通过训练写入策略参数 |
| [27. Adaptive Auto-Harness: Sustained Self-Improvement for Agentic System Deployment on Open-Ended Task Streams](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-27) | — | T1,T3,T4 | 持续任务流框架；人工介入及路由条件需保留 |
| [28. AEL: Evolving Agent Harness in Open-Ended Environments](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-28) | — | T4 | 改记忆使用策略；不是环境探索 |
| [29. Agent JIT Compilation for Latency-Optimizing Web Agent Planning and Scheduling](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-29) | E3 | T3,T4 | Web；离线工具与在线调度；非完整持续修补证据 |
| [30. Agent S: An Open Agentic Framework that Uses Computers Like a Human](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-30) | E1 | T2 | 机制借鉴：通用GUI；探索和在线记忆都存在 |
| [31. Agent Workflow Memory](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-31) | — | T2,T3 | Web；主方法文字工作流，程序动作是另测扩展 |
| [32. AgentDevel: Reframing Self-Evolving LLM Agents as Release Engineering](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-32) | — | T1,T3,T4 | 发布/回归验收机制；需按目标Web环境复现 |
| [33. AgentDistill: Training-Free Agent Distillation with Generalizable MCP Boxes](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-33) | — | T3 | 教师到学生的一次工具构建；非持续自改 |
| [34. Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-34) | — | T1,T2 | 固定权重上下文手册；文字条目与提示边界重叠 |
| [35. Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-35) | — | T2 | 计划模板缓存；修复不是主机制 |
| [36. AgenticCache: Cache-Driven Asynchronous Planning for Embodied AI Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-36) | E2 | T2 | 具身任务；被动学动作/状态规律，非主动探索 |
| [37. AgentOrchestra: Orchestrating Multi-Agent Intelligence with the Tool-Environment-Agent(TEA) Protocol](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-37) | — | T1,T3,T4 | 多Agent组件更新；环境接口不等于环境知识 |
| [38. AI Agents That Matter](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-38) | — | — | 评价对照：质量/费用、优化与部署投入 |
| [39. Alita-G: Self-Evolving Generative Agent for Agent Generation](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-39) | — | T3 | 从任务轨迹归纳MCP工具；非主动学环境规则 |
| [40. Alita: Generalist Agent Enabling Scalable Agentic Reasoning with Minimal Predefinition and Maximal Self-Evolution](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-40) | — | T3 | 集成已有软件资源；不等同实验发现规则 |
| [41. AppAgentX: Evolving GUI Agents as Proficient Smartphone Users](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-41) | E2,E3 | T3 | 移动GUI；环境知识来自既往任务，非独立探索器 |
| [42. Automated Design of Agentic Systems](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-42) | — | T4 | 离线Agent代码搜索；不是外部环境探索 |
| [43. AutoTool: Efficient Tool Selection for Large Language Model Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-43) | E2 | T4 | 被动工具转移/参数依赖；自动路由而非主动探索 |
| [44. AvaTaR: Optimizing LLM Agents for Tool Usage via Contrastive Reasoning](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-44) | — | T1 | 工具使用策略提示；固定权重 |
| [45. Better with Experience: Self-Evolving LLM Agents for Evidence-Grounded Health Community Notes](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-45) | — | T2 | 机制借鉴：健康说明；取证不等于环境探索 |
| [46. Better, Faster, Stronger: Programmatic Skill Learning Best Reduces Agent Cost](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-46) | — | T3 | 机制借鉴：文本/游戏任务流；API含归纳者摊销 |
| [47. CODESKILL: Learning Self-Evolving Skills for Coding Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-47) | — | T3 | 训练边界：技能管理模型训练；执行者冻结不够 |
| [48. CoEvoSkills: Self-Evolving Agent Skills via Co-Evolutionary Verification](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-48) | — | T3 | 技能与验证共同迭代；需独立任务正确性检查 |
| [49. Continual Harness: Online Adaptation for Self-Improving Foundation Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-49) | — | T1,T2,T3,T4 | 连续游戏内自改；长回合非独立任务泛化 |
| [50. CRAFT: Customizing LLMs by Creating and Retrieving from Specialized Toolsets](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-50) | — | T3 | 从正确训练解法构建函数库；非主动环境探索 |
| [51. Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-51) | — | T4 | 编码Agent版本搜索；固定模型外部程序演化 |
| [52. DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-52) | — | T1 | 混合边界：只选提示/示例编译，微调分支排除 |
| [53. Dynamic Cheatsheet: Test-Time Learning with Adaptive Memory](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-53) | — | T2,T3 | 机制借鉴：推理题；文字/代码经验增改 |
| [54. EchoPath: Execution-Level Replayable Memory for GUI Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-54) | E1,E3 | T3 | GUI重放；环境前提来自轨迹，非主动规则探索 |
| [55. EET: Experience-Driven Early Termination for Cost-Efficient Software Engineering Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-55) | — | T2,T4 | 机制借鉴：编码任务；经验改变停止决策 |
| [56. Enhancing Open-Domain Task-Solving Capability of LLMs via Autonomous Tool Integration from GitHub](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-56) | — | T2,T3 | 仓库资源集成；持久镜像/工具而非系统规则探索 |
| [57. EvolveMem: Self-Evolving Memory Architecture via AutoResearch for LLM Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-57) | — | T4 | 改记忆检索配置与策略，非只改记忆内容 |
| [58. EXG: Self-Evolving Agents with Experience Graphs](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-58) | — | T2 | 成败/修复关系图；不是环境状态图 |
| [59. ExpeL: LLM Agents Are Experiential Learners](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-59) | — | T1,T2 | 跨任务经验规则与案例；固定权重 |
| [60. FireAct: Toward Language Agent Fine-tuning](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-60) | — | — | 训练边界：轨迹微调模型 |
| [61. FORGE: Self-Evolving Agent Memory With No Weight Updates via Population Broadcast](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-61) | — | T2 | 机制借鉴：网络防御；群体记忆更新 |
| [62. From Failed Trajectories to Reliable LLM Agents: Diagnosing and Repairing Harness Flaws](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-62) | — | T1,T3,T4 | 多基准框架修补；Web部署时费须另测 |
| [63. From Knowledge to Noise: CTIM-Rover and the Pitfalls of Episodic Memory in Software Engineering Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-63) | E1 | T2 | 机制借鉴：代码库；被动结构记忆可误导 |
| [64. G-Memory: Tracing Hierarchical Memory for Multi-Agent Systems](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-64) | — | T2 | 多Agent经验/交互图；不是环境状态图 |
| [65. GenericAgent: A Token-Efficient Self-Evolving LLM Agent via Contextual Information Density Maximization (V1.0)](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-65) | E1,E3 | T2,T3 | 通用电脑任务；知识来自执行，主动探索收益未隔离 |
| [66. GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-66) | — | T1 | 轨迹反馈改提示；优化rollout效率非部署速度 |
| [67. GPTSwarm: Language Agents as Optimizable Graphs](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-67) | — | T1,T4 | 边界：连接概率另做策略优化；不称全系统零训练 |
| [68. Group-Evolving Agents: Open-Ended Self-Improvement via Experience Sharing](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-68) | — | T4 | 编码Agent群体版本搜索；经验共享 |
| [69. Gödel Agent: A Self-Referential Agent Framework for Recursively Self-Improvement](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-69) | — | T4 | 开放源码自改；调用更强模型的配置不满足固定模型比较 |
| [70. Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-70) | — | T4 | 训练边界：独立补丁编辑模型训练 |
| [71. How to Correctly do Semantic Backpropagation on Language-based Agentic Systems](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-71) | — | T1 | 文字反馈/归因框架；非专门Web方法 |
| [72. Huxley-Gödel Machine: Human-Level Coding Agent Development by an Approximation of the Optimal Self-Improving Machine](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-72) | — | T4 | 版本搜索与调度；改进过程效率非部署效率 |
| [73. Hyperagents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-73) | — | T4 | 执行者与改进器程序同时修改；主目标是改进能力 |
| [74. Inducing Programmatic Skills for Agentic Tasks](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-74) | — | T3 | Web；成功轨迹归纳Python技能并重跑验收 |
| [75. JudgeFlow: Agentic Workflow Optimization via Block Judge](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-75) | — | T4 | 轨迹责任归因到逻辑块；非环境规则探索 |
| [76. Large Language Models as Tool Makers](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-76) | — | T3 | 样例到函数；构建/使用分工，非应用探索 |
| [77. Mem^2Evolve: Towards Self-Evolving Agents via Co-Evolutionary Capability Expansion and Experience Distillation](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-77) | — | T2,T3 | 经验库与工具库互促；新增工具由任务需求触发 |
| [78. Memento: Fine-tuning LLM Agents without Fine-tuning LLMs](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-78) | — | T2 | 混合边界：非参数检索可借鉴，训练Q检索器须单列 |
| [79. MemQ: Integrating Q-Learning into Self-Evolving Memory Agents over Provenance DAGs](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-79) | — | T2 | 条目Q值更新；非模型权重训练，不因RL字样排除 |
| [80. MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-80) | — | T2 | 经验效用更新；模型权重固定 |
| [81. Meta-TTL: Meta-Learning Self-Improvement Policies for Language Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-81) | — | T1,T4 | 提示及meta提示更新；内层主要同题重试 |
| [82. MetaAgent: Toward Self-Evolving Agent via Tool Meta-Learning](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-82) | — | T2 | 资料与工具经验；普通信息搜索非规则探测 |
| [83. Metis: Bridging Text and Code Memory for Self-Evolving Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-83) | E1,E3 | T2,T3 | AppWorld；环境探查、文字事实与程序计划并存 |
| [84. MOSS: Self-Evolution through Source-Level Rewriting in Autonomous Agent Systems](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-84) | — | T4 | 源码补丁；含用户确认流程 |
| [85. Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-85) | — | T1 | 指令与示例搜索；固定权重配置优化 |
| [86. PRompt Optimization in Multi-Step Tasks (PROMST): Integrating Human Feedback and Heuristic-based Sampling](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-86) | — | T1 | 训练边界：辅助Longformer评分器微调 |
| [87. ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-87) | — | T2 | Web；成败经验检索；步骤与token不必同向 |
| [88. Recursive Self-Evolving Agents via Held-Out Selection](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-88) | — | T1 | 策略/技能说明文字更新；开发与选版分离 |
| [89. Reflection-Based Memory For Web navigation Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-89) | E1 | T2 | Web；网站限制来自既往轨迹，非独立主动探测 |
| [90. Reflexion: Language Agents with Verbal Reinforcement Learning](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-90) | — | T2 | 同题重试反思；不能替代跨任务持续学习证据 |
| [91. RewardHarness: Self-Evolving Agentic Post-Training](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-91) | — | T3,T4 | 对象边界：评价器自改；下游另有模型训练 |
| [92. SEDM: Scalable Self-Evolving Distributed Memory for Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-92) | — | T2 | 候选记忆配对准入；非真实环境主动探测 |
| [93. Self-Evolving Multi-Agent Systems via Decentralized Memory (DecentMem)](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-93) | — | T2 | 多Agent私有记忆；生成探索候选非真实环境交互 |
| [94. Self-Evolving World Models for LLM Agent Planning](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-94) | E1,E2 | T2 | 固定权重环境预测：文字规则/转移样例；非Web主证据 |
| [95. Self-Taught Optimizer (STOP): Recursively Self-Improving Code Generation](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-95) | — | T4 | 改写改进器；搜索程序而非环境知识 |
| [96. SkillOpt: Executive Strategy for Self-Evolving Agent Skills](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-96) | — | T1 | 文字技能文档补丁；不是新增可执行工具 |
| [97. Speculate with Memory: Lossless Acceleration for LLM Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-97) | E2 | T2,T4 | 运行时邻近：轨迹驱动推测器，不改正式执行者策略 |
| [98. Speculative Macro Commit for Faster Tool-Using Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-98) | E3 | T3,T4 | 运行时邻近：轨迹宏+推测提交；近似而非严格保质量 |
| [99. StarHarness: Evolving Harnesses with Stratified Search for Enterprise Environments](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-99) | — | T1,T3,T4 | 企业环境框架演化；没有独立通用探索器 |
| [100. Symbolic Learning Enables Self-Evolving Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-100) | — | T1,T3,T4 | 提示/工具/连接结构更新；所谓学习非底座训练 |
| [101. TextGrad: Automatic "Differentiation" via Text](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-101) | — | T1 | 通用文字反馈；只将可复用提示优化纳入 |
| [102. The Red Queen Gödel Machine: Co-Evolving Agents and Their Evaluators](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-102) | — | T4 | Agent及评价器换版；对象扩大须独立评分 |
| [103. Trace is the Next AutoDiff: Generative Optimization with Rich Feedback, Execution Traces, and LLMs](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-103) | — | T1,T4 | 运行图反馈优化；可改文字或代码 |
| [104. WebCoach: Self-Evolving Web Agents with Cross-Session Memory Guidance](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-104) | E1 | T2 | Web；被动导航经验；少步骤仍可能更慢 |
| [105. Grow the Harness, Not the Context: From Strategy-Free Scaffolds to Reusable Specialist Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-105) | — | T4 | Web/检索；共享控制代码，离线优化费另计 |
| [106. TraceCompiler: Skill-Guided Mining and Compilation of LLM Agent Traces into Mostly Deterministic Workflows](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-106) | — | T3,T4 | 轨迹依赖编译；实现与案例规模有限 |
| [107. Internal APIs Are All You Need: Shadow APIs, Shared Discovery, and the Case Against Browser-First Agent Architectures](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-107) | E1,E2,E3 | T3 | Web接口发现/目录；并非整体Agent自改 |
| [108. SKILL.nb: Selective Formalization and Gated Execution for Durable Agent Workflows](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-108) | E1,E3 | T1,T3 | Web；步骤文档/代码/条件维护；不是独立主动勘探 |
| [109. Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-109) | E1 | T2 | 企业数据库/文档；针对候选经验主动补查 |
| [110. Are Online Skill and Memory Modules Always Worth Their Tokens? A Budget-Constrained Study of Web Agents](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-110) | — | — | Web评价对照：辅助模块预算与普通执行预算 |
| [111. ClawTrace: Cost-Aware Tracing for LLM Agent Skill Distillation](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-111) | — | T1 | 成本轨迹到文字技能文档；不能按skill名称当代码工具 |
| [112. ESPO: Error-Structured Prompt Optimization via Diagnose, Diversify, and Stabilize](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-112) | — | T1 | 文本预测提示优化；非多步Web执行证据 |
| [113. SoL-Pi: Recursively Scaling Auto-Research Loops for Efficient Agent Harness](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-113) | — | T4 | 编码环境效率框架；质量取舍，完整搜索费未清楚 |
| [114. Web Agents with World Models: Learning and Leveraging Environment Dynamics in Web Navigation](2026-10-01-agent-acceleration-paper-comparisons-zh.md#paper-114) | E2 | — | 训练边界：环境预测器/评分器训练，非全系统固定权重 |

## 7. 来源、尚待确认与制作注意

- 直接整理来源：[逐篇比较（114条）](2026-10-01-agent-acceleration-paper-comparisons-zh.md)、[两方向文献：分类论证与完整 References](2026-10-01-two-directions-literature-zh.md)、[最新研究问题分析](2026-10-01-agent-acceleration-related-work-analysis-zh.md)。本稿没有新实测数字，没有新增E/D证据项，也没有重新判定发表资格。
- 正文代表的资格：DRAFT、GEPA、ACE、ReasoningBank、WALT为ICLR主会；AWM为ICML主会；ASI为COLM主会；MobileGPT为MobiCom；ActionEngine、SkillWeaver、Grounding Agent Memory、HarnessFix、Growing Harness、SpeedRunner为已有规则下的合格预印本。正式引用与实际读的版本见[原有References](2026-10-01-two-directions-literature-zh.md#references)，不把workshop或预印本改称主会。
- WALT依据补读的正式版承认构建费用；AWM依据补读正式版承认归纳/评估token；SpeedRunner承认归纳者API摊销；ESPO承认文本任务推理延迟。不能沿用早期“原文未报告”的绝对说法。
- FormNexus与Web Application Testing用于附录机制映射，不在本文件重新宣布来源资格；若选上正文，先沿已有审计补齐正式出处/机构及已读版本。SoL-Pi新旧总结对API费用描述不同，选为正文量化例子前须回到原文核对，本稿不据其作量化论证。
- 本分类是面向演示的人工归纳；跨类论文保留多个标签，尚未解决的问题仍需在选定方法和实验条件下判断。没有“完整解决所有环境/所有任务”不等于构成一个可发表研究空白。
