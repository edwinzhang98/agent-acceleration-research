# 第三部分的相关工作调查：从执行轨迹改进 Agent，及从交互经验学习环境

核查日期：2026-09-29。本文先回答“已有工作做到哪里”，不确定本项目的方法、实验配置或预算。此前的 [研究方向草稿](../notes/2026-09-29-part3-research-proposal-zh.md) 只保留为讨论记录；其最近邻清单不完整，不能据此判定研究空白。本文优先于该草稿的相关工作判断。

## 1. 证据与核查

### 1.1 目前能够得出的结论

**两个方向都有直接先例，而且部分工作已经把它们连接起来。** 第一条线通常称为 automatic agent / harness optimization：根据轨迹修改模型外的指令、工具、记忆和执行逻辑。第二条线跨越 environment learning、workflow induction 和 executable skill learning：把交互经验变成规则、状态关系或可执行动作。只用“从失败中学习”“全自动改 Agent”“生成更精确的 action”来描述贡献，无法与已有研究区分。

这里的 **harness** 指模型周围的执行系统，包括 prompt、工具接口、上下文构造、检查和恢复逻辑；不同论文允许修改的范围不同，不能看到这个词就认为它允许修改全部代码。

尤其需要补入上一轮调查遗漏的三个事实：

- **完整自动闭环已存在。** AutoSaddler、Self-Harness 等已经把诊断、修改、重跑、选择串起来；PRISM 已按失败原因选择改 prompt、工具边界代码或两者。见下表 E309、E310、E312。
- **学习“如何修改 Agent”的 RL 已存在。** Harness-R1 训练的是修改执行系统的模型，奖励来自修改后目标 Agent 的实际表现。这比一般“用 RL 训练执行策略”更接近用户所说的学习试错过程。详见本文的 RL 对照。
- **效率与前期投入也已有直接研究。** Better Harnesses, Smaller Models 测运行费用和延迟，并讨论优化开销；ActionEngine、AutoDroid-V2 也不能仅归为成功率工作。需要逐篇比较计费范围，不能把“计入学习成本”笼统称为无人研究。

这些判断并不意味着没有可做的问题。它们意味着下一步应从具体任务分布、反馈条件、允许的修改和测量目标寻找差别；**本轮不把“尚未在某论文报告”升级为整个领域的研究空白。**

### 1.2 最直接的自动改进工作

以下条目以 primary 原文为依据。A 表示已核查全文的相关方法、实验或限制章节；B 表示仅完成摘要或有限章节筛选。A 不代表复现，更不代表逐字审读全文。表中英文短引只用于定位证据。

| ID / 论文与版本 | 轨迹怎样变成改进 | 验证方式、效率证据与边界 | 原文定位 / 判断 |
|---|---|---|---|
| **E309 · AutoSaddler**，Park et al.，2026-08-24，v1；[全文](https://arxiv.org/html/2608.23041v1) | 用一批成功及失败轨迹和 harness 代码诊断，生成 prompt、tool、middleware 补丁；可新增工具。反思修好、回归和仍失败的案例，存入 EvoDAG 再组合候选。 | 同批重跑筛选，再用 dev 选择；最终 test 不参与修改。以成功表现为主，App. I 分列优化器和任务执行开销。假定训练任务有结果判据，所选编辑空间不包含记忆/技能整理。 | A；§§3–4、Table 1、App. I/R：“structured patch generation that treats the harness as code”。**方向一的完整近邻。** |
| **E310 · Self-Harness: Harnesses That Improve Themselves**，Zhang et al.，2026-08-20，v3；[全文](https://arxiv.org/html/2606.09498v3) | 聚合 verifier 支持的失败模式，由同一冻结模型提出有限的 harness 修改，再回归测试。 | 修改限于声明的配置接口。held-out split 反复参与 promotion gate，功能上是验证集，不能叫最终未使用测试集。主证据为通过率。 | A；§§3.2–3.4、4.1：“verifier-grounded failure signatures”。**高频失败归类与自动保留修改已有实现。** |
| **E311 · Evolving Agents in the Dark: Retrospective Harness Optimization via Self-Preference（RHO）**，Pan et al.，2026-08-29，v3；[全文](https://arxiv.org/html/2606.05922v3) | 选历史任务子集，额外并行重做，以自验证和多轨迹一致性生成指令、skill、工具脚本候选，用自偏好选择。 | 优化不依赖外部标准答案，但仍需额外执行，且自判不是正确性保证。App. G 分析优化阶段开销；一次 agent invocation 不等于一次模型调用。 | A；§4、App. D/G/H：“without claiming an efficiency advantage”。**实际部署难拿标注，也已有专门研究。** |
| **E312 · Beyond Prompts: Measuring and Optimizing LLM Tool-Agent Harnesses（PRISM）**，Zhao et al.，2026-09-09，v2；[全文](https://arxiv.org/html/2609.05736v2) | 对错误聚类，把修复分配给 prompt、middleware 或联合修改；跨代跟踪错误状态，以验证集表现和可靠性维护候选。 | middleware 限于参数修正、报错阻断和前置条件阻断，非任意执行逻辑重写。另设最终 scorecard。费用是搜索诊断量；RelLift 是预算下所选方案相对基线提升的经验低尾估计，非保证或运行加速比。 | A；§§3–4、App. F：“Prompt, Middleware, or Joint”。**“判断该改文字还是代码”已有直接对照。** |
| **E313 · Better Harnesses, Smaller Models: Building 90% Cheaper Agents via Automated Harness Adaptation**，Yang, Zhao, Wu, Kästner，2026-07-09，v1；[全文](https://arxiv.org/html/2607.08938v1) | 把失败模式映射到指令、工具和执行循环的修改，通过 meta-agent 搜索适合小模型的执行系统。重复业务流程是重要适用条件。 | 有 train/validation/test；Table II 同时报准确率、单实例 token 计价费用和端到端延迟，§IV 讨论前期优化投入。主要费用比较包含换模型，不能表述为固定同一模型的等成功率降费。 | A；§§II–IV：“automatically discovers effective adaptations from failure trajectories”。**与重复业务场景和加速动机都直接相关。** |

| **E317 · Offline Training of Language Model Agents with Functions as Learnable Weights（AgentOptimizer）**，Zhang et al.，2024-07-30，v4；[全文](https://arxiv.org/html/2402.11359v4) | 从函数调用等执行历史中新增、删除、修改函数描述与代码，再跑训练任务，支持 rollback / early stop。 | 已覆盖“现有 action 不好用，改或新增 action 再验证”。主要是任务表现，未据所读实验确认部署总费用摊销。早期标题不同，不能算两篇。 | A；§2：“how the agent uses current functions”。**重要的较早直接先例。** |
| **E318 · Symbolic Learning Enables Self-Evolving Agents**，Zhou et al.，2024-06-26，v1；[全文](https://arxiv.org/html/2406.18532v1) | 记录节点输入、输出、prompt 和工具调用，用 language loss / gradient 改 prompt、tool、pipeline，并重新运行及回退。 | 文字“梯度”不是权重反传；部分标准任务实验禁用 tools，不能认为每张结果表都验证了新工具学习。 | A；§3.2：“PromptOptimizer, ToolOptimizer, and PipelineOptimizer”。**多种修改位置不是新的大类。** |
| **E319 · Meta-Harness: End-to-End Optimization of Model Harnesses**，Lee et al.，2026-03-30，v1；[全文](https://arxiv.org/html/2603.28052v1) | coding proposer 自主检索既往源码、分数、原始轨迹，编辑完整 harness 候选并评价。 | 包含准确率—上下文成本的比较，不能直接换成美元或时间。论文所链 repo 主要为最终优化产物，不是已确认完整外层搜索开源。 | A；§§3–4：“source code, scores, and execution traces”。**直接把长期历史交给 coding agent 也是现成基线。** |
| **E320 · Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses（AHE）**，Lin et al.，2026-04-28，v1；[全文](https://arxiv.org/html/2604.25850v1) | 从分层轨迹证据定位问题，修改 prompt、工具、middleware、skills、subagents、记忆等文件，记录预期修复与回归，在下一轮核对。 | §4.4.2 已测修复/回归预测；不是唯一因果证明。演化集与外部任务迁移分别报告。tokens/trial 排除部分超时/中断，不能称所有尝试的平均费用。 | A；§3：“pairs every edit with a self-declared prediction”。**诊断是否正确也已有实测研究。** |
| **既有 E305 · ADIAS: Automated Design of Interactive Agentic Systems**，Jiang et al.，2026-08-03，v1；[全文](https://arxiv.org/pdf/2608.06410v1) | 把真实交互问题保存为带身份、状态、优先级和干预历史的 issue，持续诊断、修改整套代码并评价。 | 有训练/验证/测试分工；效率量为任务得分与环境步数的比值，非墙钟或美元；没有单独测归因标签准确率。 | A；§3.3、App. C/D、Limitations；**跨轮不忘记问题已有直接先例。** |

其余自动优化工作保留作方法来源和比较边界。下面的 R 编号仅是本调查条目号，尚未全部提升为 dossier 的独立 E 条目。

| 调查 ID / 工作及固定阅读版本 | 已核查的作用与边界 | 定位与阅读级别 |
|---|---|---|
| R01 · **Automated Design of Agentic Systems（ADAS）**；[2024 v1](https://arxiv.org/html/2408.08435v1) | 生成 agent 代码，执行、评估、归档并搜索新候选；以任务表现和候选历史为主。附录已报告搜索/评价开销，不等于部署摊销。 | A；§§2–4、App. G |
| R02 · **Trace is the Next AutoDiff: Generative Optimization with Rich Feedback, Execution Traces, and LLMs**；[NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/file/83ba7056bce2c3c3c27e17397cf3e1f0-Paper-Conference.pdf) | 优化计算图里指定的异构变量，包括代码和 prompt；其 trace 常是计算过程，不应等同长期浏览器交互轨迹。 | A；§§1–4 |
| R03 · **TextGrad: Automatic “Differentiation” via Text**；[2024 v1](https://arxiv.org/html/2406.07496v1) | 用文本反馈优化指定变量；单题答案精炼与跨题 prompt 学习要区分，未自动接管全部 Agent 代码。 | A；§§2–3、App. E |
| R04 · **AFlow: Automating Agentic Workflow Generation**；[2025 v4](https://arxiv.org/html/2410.10762v4) | 根据执行反馈搜索代码表示的工作流。报告推理费用与搜索效率；不等于持久 Web 环境知识维护。 | A；§§3–4、App. C/D |
| R05 · **AgentSquare: Automatic LLM Agent Search in Modular Design Space**；[2025 v3](https://arxiv.org/html/2410.06153v3) | 重组及生成 planning/reasoning/tool-use/memory 模块；新模块实跑，已有模块重组可用 surrogate 评价。不是原始失败轨迹的 issue 归因系统。 | A；§§3.4–4.2 |
| R06 · **AutoHarness: improving LLM agents by automatically synthesizing a code harness**；[2026 v1](https://arxiv.org/html/2603.03329v1) | 在 TextArena 用环境失败反馈生成检查器、动作提议器或完整代码策略。只有完整 code policy 才无需在线模型；合成仍有成本。 | A；§§3–4、App. B/C |
| R07 · **MOSS: Self-Evolution through Source-Level Rewriting in Autonomous Agent Systems**；[2026 v1](https://arxiv.org/html/2605.22794v1) | 从失败会话到源码修复、容器试验和判定；实证规模很小，主要同批首轮；生产 apply 仍需用户触发。不能把自动试验等同自动上线。 | A；§§2–4 |
| R08 · **HarnessX: A Composable, Adaptive, and Evolvable Agent Harness Foundry**；[2026 v1](https://arxiv.org/html/2606.14249v1) | 错误聚类后修改组件，也可接 task-model GRPO；有学习 token 与部署摊销讨论。§7.7 明确主结果取演化集 peak，缺未见任务测试，且部分环境每任务 token 增加。 | A；§§4–7、9.2 |
| 既有 E304 · **GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning**；[2026 v2](https://arxiv.org/pdf/2507.19457v2) | 执行轨迹反思、模块修改、候选选择；主论文以 prompt 为主，框架也可用于代码。Pareto 主要指任务表现维度，非时间—费用前沿。 | A；§3、Alg. 1、App. E/I |
| 既有 E306 · **Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents（DGM）**；[2025 v2](https://arxiv.org/html/2505.22954v2) | 从评估日志诊断、改自身代码并保存候选群体；代码任务成绩和研究 API 投入，不等于重复 Web 工作流的净加速。 | A；§§3–4、App. C/E |
| 既有 E271 · **Better, Faster, Stronger: Programmatic Skill Learning Best Reduces Agent Cost（SpeedRunner）**；[2026 v1](https://arxiv.org/html/2608.11338v1) | wake 收集轨迹，sleep 自动增删改代码技能，考虑后续复用及诱导成本；每次在线修改不经过持续 replay gate，论文另做周期评测。 | A；§§2–3、App. A/G；文本交互环境 |

### 1.3 从环境经验到规则、状态和可执行动作

“学习环境”至少有三个不同含义：记住文字规则；掌握什么状态下可以做什么、之后会发生什么；把经验证的操作封装成参数化代码。下面按实际产物区分，不把一段操作说明等同于可执行环境模型。

| ID / 工作与阅读版本 | 经验来源 → 学到的东西 | 与用户设想的关系及证据边界 |
|---|---|---|
| **E315 · AutoManual: Constructing Instruction Manuals by LLM Agents via Interactive Environmental Learning**，Chen et al.；[2024-11-10 v4](https://arxiv.org/html/2405.16247v4) | 做训练任务时的成功、试错和失败 → 条件规则、流程、已修/未修错误及验证日志；会整理和删除冗余。 | A，§3.3；明确区分 **“Imperfect Rules” / “Imperfect Agent”**，再更新规则。初始化仍有人工示例与初始规则；主要产物是手册，非强制执行的 API 或完整环境图。两个方向在此已经相交。 |
| **E316 · Empowering Large Language Model Agents through Action Learning（LearnAct）**，Zhao et al.；[COLM 2024](https://openreview.net/pdf?id=KqK5XcgEhR)、[v2](https://arxiv.org/html/2402.15809v2) | 先生成 Python 高级动作与用法，再运行训练任务，依据失败修动作。 | A，§§3–4；可选择修函数或补使用说明，用执行结果选候选。很接近“现有 action 不够，需要写新 action”；实证为 Robotic Planning / ALFWorld，非真实 Web UI。与同名 2026 移动 GUI LearnAct 区分。 |
| **既有 E308 · SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills**；[2025 v1](https://arxiv.org/html/2504.07079v1) | 主动探索、成功轨迹、额外测试 → 参数化 Playwright API 与前置状态说明。 | A，§2、App. D.2；“description of the prerequisite state”。自动合成、测试、调试；judge 可能被不抛异常的错误代码误导。主要证明任务表现，不能据此推定总费用下降。 |
| **既有 E230 · WALT: Web Agents that Learn Tools**；[2025 arXiv v1](https://arxiv.org/html/2510.01524v1)、[ICLR 2026](https://iclr.cc/virtual/2026/poster/10008481) | 自主功能探索/示范 → 参数 schema、枚举、前置条件、预期结果及工具代码；确定性和需要模型的步骤可混合。 | A，v1 §3：“preconditions, and expected outcomes”。失败修脚本并验证，部署可 fallback。v1 的 steps 非墙钟；本轮终版 PDF 抓取因文件过大失败，正式新增成本数据应沿现有 deck audit 核，不说作者没报。 |
| **既有 E307 · ActionEngine: From Reactive to Programmatic Web Agents via State Machine Memory**；[2026-09-28 v2](https://arxiv.org/html/2602.20502v2) | 额外主动探索 → UI 模板、操作、状态转移和动态数据访问路径；编译成任务程序。 | A，§§3–5；“initial SMG construction is task-independent”。架构有知识回写 Patcher；主评估按任务模板 warm-up，且关闭 Patcher。已报运行效率和探索摊销；不能据主实验宣称新模板泛化或持续维护收益。 |
| **既有 E227 · AutoDroid-V2: Boosting SLM-based GUI Agents via Code Generation**；[2025-05-06 v3](https://arxiv.org/html/2412.18116v3) | 主动探索 → 元素转移图与前后依赖；生成任务/程序并验证，SFT 小模型产 GUI 脚本。 | A，§3.1.3：“Forward and Backward Dependency”。与“把环境规律落实为动作”直接相关。核心时间量是 **LLM inference latency，排除 GUI 执行**；有文档/数据/验证成本，不能说建设成本未报告。 |
| **既有 E229 · Inducing Programmatic Skills for Agentic Tasks（ASI）**；[2025 v2](https://arxiv.org/html/2504.06821v2) | 在线任务中被判成功的轨迹 → 参数化 Python 技能；额外 rollout 验证替换片段是否有效。 | A，§2；“all skill-calling actions cause environment changes”。模型自判不等于外部语义保证；运行 steps 不包含全部归纳验证投入。 |
| **既有 E272 · Agent Workflow Memory（AWM）**；[2024 v1](https://arxiv.org/html/2409.07429v1) | 成功经历归纳为 workflow memory，在后续任务中提供给模型。 | A，既有 Part 2 核查接续；不能把文字 workflow 当无需模型介入的可执行 macro。本文保留仓库 D41/D201 的口径限制，不重报 headline。 |
| R09 · **AppAgent: Multimodal Agents as Smartphone Users**；[所读 v3](https://arxiv.org/html/2312.13771v3) | 主动探索或人类示范 → 页面元素用途和效果的语义文档。 | A，§§3–4；后续仍逐步用模型操作，不等同自动生成代码工具。探索投入与成功任务上的 steps 需要分开。 |
| R10 · **AppAgentX: Evolving GUI Agents as Proficient Smartphone Users**；[2025 v3](https://arxiv.org/html/2503.02268v3) | 运行历史的状态—动作—状态链 → 可参数化的高级 shortcut，运行时检索、判适用、失败回退。 | A，§§4–5；接近被动积累，但仍有分析生成开销。时间比较只统计双方均成功任务，tokens 统计所有任务；未确认系统性的失败归因机制。 |
| R11 · **MobileGPT: Augmenting LLM with Human-like App Memory for Mobile Task Automation**；[2024 v3](https://arxiv.org/html/2312.03003v3) | 随机探索、任务经验和用户输入 → 任务/子任务/动作的层级记忆与参数化回放。 | A，§§2–5、7；有费用和时间实验，但 cold-start 失败经人工修复后入库，warm-start 高成功率不能当作无人自改进证据。 |
| R12 · **AutoDroid: LLM-powered Task Automation in Android**；[2024 v4](https://arxiv.org/html/2308.15272v4) | 离线动态探索 → UI Transition Graph、功能知识和合成任务；还用捷径与等价界面合并。 | A，§3、§6.5；有离线时间和运行调用/token 证据，未据所读实验确认长期失败驱动的持续图维护。 |
| R13 · **Is Your LLM Secretly a World Model of the Internet? Model-Based Planning for Web Agents（WebDreamer）**；[2025 v2](https://arxiv.org/html/2411.06559v2) | 预测动作后的观察变化并打分规划；v2 另收集网页转移数据训练 Dreamer。 | A，§3、§5；这是预测模型，非 action API 库。减少真实树搜索的开销可能仍比 reactive agent 慢，比较基线不能省略。 |
| R14 · **Web Agents with World Models: Learning and Leveraging Environment Dynamics in Web Navigation（WMA）**；[2025 v2](https://arxiv.org/html/2410.13232v2) | 主动/离线网页交互 → 预测状态变化的模型，配合固定 policy 候选及 value 评分。 | A，§§4–5、App. C；训练的是 world model，不是直接训练 task policy；没有输出完整显式状态图或代码工具。运行费用与树搜索相比，未含全部训练投入。 |
| R15 · **AutoGuide: Automated Generation and Selection of Context-Aware Guidelines for Large Language Model Agents**；[2024 v2](https://arxiv.org/html/2403.08978v2) | 好/坏离线经验对照 → 按上下文检索的文字指南。 | A，§3、App. B.4；某些真实站点使用人类正例，非全自主探索；是失败经验和环境知识的近邻，不是可执行动作生成。 |

由此可见，**外部规则、可执行技能、显式状态关系、学习到的预测模型应分开比较**。它们都可能减少重复试错，但需要不同数据，也可能增加每次调用的成本。不能先把“有环境学习”统称为相同能力。

### 1.4 失败经验、记忆与强化学习

| ID / 工作与阅读版本 | 真正更新的对象 | 自动化与评价边界 |
|---|---|---|
| **E314 · Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories**，Shao et al.；[2026-08-03 v1](https://arxiv.org/html/2608.02276v1) | 从失败包生成可执行 hooks，用目标 Agent 重跑结果做 SFT + GRPO，训练独立的 **harness editor**；目标模型冻结。 | A，§3、§4.4、App. F；“persistent patch memory across batches” 是原文明确没有的能力。训练 reward 来自同批重跑；另有未见任务泛化测试，不能说“只测了原任务”。也不是不受限制地改任意代码。 |
| R16 · **ExpeL: LLM Agents Are Experiential Learners**；[2024 v3](https://arxiv.org/pdf/2308.10144v3) | 对比成功与失败轨迹，维护可增删改的跨任务文字 insights，检索给后续任务；模型冻结。 | A，§§3–4；“deterministic environments”。失败经验跨任务复用已有先例，但没有生成新 action 或训练代码修改者。 |
| **E321 · ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory**，Ouyang et al.；[2026-03-16 v2](https://arxiv.org/pdf/2509.25140v2) | 自判轨迹成败，提炼成功策略与失败经验，写入跨任务记忆并检索；actor 冻结。 | A，§3、App. C.2/Table 5；“total token consumption is increased”。执行 steps 或 actor tokens 降低不等于含判断/提炼的总开销下降。 |
| R17 · **Memento: Fine-tuning LLM Agents without Fine-tuning LLMs**；[2025 v2](https://arxiv.org/pdf/2508.16153v2) | 保存案例；非参数版检索，参数版训练独立 Q 网络来选择案例。 | A，§4.2、§5；“online updates a Q-function”。冻结 LLM 不等于所有参数均不训练，也不是学出完整环境转移模型。 |
| R18 · **AgentEvolver: Towards Efficient Self-Evolving Agent System**；[2025 v1](https://arxiv.org/pdf/2511.10395v1) | 自生成探索任务、经验引导 rollout、对动作作贡献归因，然后用过程/结果奖励训练 task-policy GRPO。 | A，§§3–7；归因主要用于训练 credit assignment，非自动修改代码。训练样本效率不能直接写为部署时间下降。 |
| **E322 · EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle**，Wu et al.；[2026-05-16 v3](https://arxiv.org/pdf/2510.16079v3) | 成功/失败经验提炼与筛选，加上检索和 GRPO 更新 **任务 actor 权重**。 | A，§3、App. A：“GRPO”。不是纯冻结模型的反思记忆；主要问答效果，检索延迟与训练投入不能等同端到端加速。 |
| R19 · **Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models（ACE）**；[2026 v3](https://arxiv.org/pdf/2510.04618v3) | Generator / Reflector / Curator 从轨迹和反馈维护 playbook，增量更新、合并与去重。 | A，§3、§4.7、App. F；“context adaptation latency”。错误归因的产物主要是上下文；所报 adaptation 费用/时间不同于最终任务服务延迟。 |
| R20 · **Agent Q: Advanced Reasoning and Learning for Autonomous AI Agents**；[2024 v1](https://arxiv.org/pdf/2408.07199v1) | 搜索成功/失败分支、形成偏好，用 DPO 训练 task actor；可再加在线搜索。 | A，§§3–6；训练后的无搜索结果与推理时搜索结果应分开，需要反馈及可回退环境条件。 |
| R21 · **Reflexion: Language Agents with Verbal Reinforcement Learning**；[2023 v4](https://arxiv.org/pdf/2303.11366v4) | 同任务反馈、反思和 episodic memory，指导后续重试；不改权重。 | A，§3；“not by updating weights”。名称有 RL 不代表梯度式 policy training；主实验不能直接当未见任务的持久系统改进。 |
| R22 · **Self-Refine: Iterative Refinement with Self-Feedback**；[2023 v2](https://arxiv.org/pdf/2303.17651v2) | 对当前答案/程序生成反馈并迭代精炼。 | A，§2；没有核心跨任务持久更新，主要是比较边界。生成的程序运行更快不等于 Agent 自己推理更快。 |
| R23 · **Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models（LATS）**；[2024 v3](https://arxiv.org/pdf/2310.04406v3) | 用反思、模型 value 和环境反馈指导当前任务的树搜索。 | A，§§4–6；无核心跨任务 updater。比某些树搜索节省计算，仍可能比简单 reactive 方法贵。 |
| **E323 · On the Fragility of Self-Improving Agents: Variance, Task Order, and Underspecification**，Ye et al.；[2026-09-06 v2](https://arxiv.org/pdf/2608.18066v2) | 复核 AWM/ReasoningBank 的多次运行与任务顺序，观察记忆中的环境假设。 | A，§§3–4；“provide the ground-truth reward”。为了隔离判断噪声使用真值反馈，非原设定原样复现；提示不能以一次任务顺序的提升宣称稳定泛化，也不能反推所有记忆无效。 |
| R24 · **Co-Harness: Co-Evolving Harnesses and Model Weights for LLM Agents**；[2026 v1](https://arxiv.org/abs/2607.22688v1) | 摘要描述 harness 诊断更新与模型训练交替。 | **B**；未完整核查训练协议和测试隔离，不用于定量比较。仅说明两者联合演化已有明确先例。 |

针对“错误原因本身是否可靠”，另筛到两篇直接相关但本轮仅核摘要的工作：

- R25 · [**Model or Harness? An Interaction-Centric Taxonomy for Localizing Agent Failures**](https://arxiv.org/abs/2607.28802v1)，2026-07-30：把修复责任定位到模型、harness、环境或 grader；是诊断分类证据，不是完整自动修改系统。B。
- R26 · [**Phantom Guardrails: When Self-Improving Agent Harnesses Fix Failures That Never Happened**](https://arxiv.org/abs/2607.13083v1)，2026-07-13：在受控微型实验中观察到优化器给不存在的错误加规则。B；不能把该实验的频率推广到真实 Web 部署。

因此，“RL 可不可以用于这个过程”应进一步区分：**训练执行任务的模型、训练记忆检索器、训练提出修改的模型**。Harness-R1 最直接对应第三种；AutoManual 受 RL 范式启发地更新文字规则，则不等于同一种参数训练。

### 1.5 与前两部分 slides 的关系

前两部分回答“耗时和费用由哪些项构成，以及哪些机制能改变这些项”。本轮相关工作增加的是另一条分类轴：**这些机制由谁、根据什么证据产生和更新。** 自动优化器可能最终生成大动作、代码重放、上下文整理或工具接口改进，因此会与 Part 2 的多个方法家族相交。

| 用户关心的具体过程 | 最直接要比较的既有工作 | 与当前 slides 的连接 |
|---|---|---|
| 高频错误归因，决定修改位置，自动实现并验证 | AutoSaddler、PRISM、Self-Harness、AHE、ADIAS | 一次修改可能同时改变步数、每步模型调用、上下文长度和成功率；“有自动优化器”本身不是某个耗时项的减少。 |
| 从操作经验得到可重用的动作 | LearnAct、SkillWeaver、WALT、SpeedRunner | 主要连接 Part 2 大动作/skills；是否真减少模型决策，要看调用动作时仍需要几轮模型。 |
| 把固定环境的交互结构保存下来并执行 | ActionEngine、AutoDroid-V2、AutoManual | 连接 compile/replay、环境接口和上下文构造；状态图、规则手册、可执行程序需要分开评价。 |
| 让“改进过程”本身学得更好 | Harness-R1；与任务模型 RL 对照 | RL 是产生修改的方式；训练和候选测试的投入应与后续执行收益分列。 |
| 让同类任务越来越便宜 | Better Harnesses, Smaller Models；ActionEngine；SpeedRunner | 对照 Part 1 时间/费用分解与附录的前期投入摊销；不同任务分布、模型替换和成功率不可以混为同一个加速比。 |

当前 deck 中已有 ActionEngine、AWM、SkillWeaver、WALT、SpeedRunner 等相关材料；它们原先按加速机制归类。新增的 harness optimization 文献是为明确第三部分的最近邻，不要求重写已经形成的前两部分结构。原版 GEPA 与 deck 中应用 GEPA 做 pruning 的工作也应分别引用，不能用后者代替前者。

### 1.6 效率证据应怎样阅读

本轮不计算本项目预算，也不拿各论文数字横向排名。主要区别如下。

| 证据 | 能支持什么 | 不能直接推出什么 |
|---|---|---|
| AutoSaddler App. I；RHO App. G | 改进流程本身消耗了多少执行或优化器资源 | 部署后的每个任务必然更便宜 |
| PRISM App. F | 搜索阶段 inner-only 或 all-model 成本；不同口径写得明确 | 全部上线、基础设施及最终测试费用已经包含 |
| Better Harnesses, Smaller Models §IV | 同任务上模型与 harness 的费用、延迟、成功表现，以及搜索投入 | 所有任务保持同等成功率；标题降费幅度来自纯 harness 修改 |
| ActionEngine v2 | 环境预探索、程序执行及部分摊销证据 | 未见过的任务模板泛化；持续 Patcher 在线收益已经由主实验验证 |
| SpeedRunner | 技能诱导和后续复用的摊销值得纳入比较 | 文本交互环境的收益直接等于 Web 操作的美元收益 |
| ReasoningBank 等记忆方法 | 成功和失败经验可以改善后续决策 | 减少交互步骤就必然降低总 token 或端到端时延 |

### 1.7 检索范围与排除原则

检索截止为 2026-09-29。共整理 **51 项比较条目**：48 项核查方法及相关实验/限制章节（含前轮已核材料接续），3 项只作摘要级筛选，逐项标 A/B。本会话没有独立的 Deep Research 调用入口；实际采用三条并行检索、primary 全文核查及参考文献追踪。不是穷尽性或注册式 systematic review。搜索结果页、媒体解读和论文聚合站只用于发现线索，事实判断回到论文、正式会议页面或作者仓库。

主要检索词组包括 `agent trajectory self-improvement latency`、`agent failure harness optimization`、`AgentOptimizer Learning to Optimize`、`AutoManual LearnAct AutoGuide`，以及环境线的 trajectory / environment memory / workflow induction / skill discovery，经验线的 failure reflection / experience memory / agent reinforcement learning。根据 AutoSaddler、Harness-R1 等的 related work 继续追查近邻，并核对 RHO、Self-Harness、PRISM 和 ActionEngine 的版本。

纳入标准是至少明确处理以下一项：轨迹驱动的持久修改；从环境经验提取可复用知识/动作；用执行反馈学习策略或修改策略。仅在单次回答中 self-critique、仅给模型更长思考时间、通用无轨迹的 prompt 搜索、纯 serving 优化，不作为两个方向的完整近邻；有比较价值的保留为边界条目。HARBOR、Continual Harness 及更广的 harness survey 是后续追踪线索，本轮不根据未核全文的内容作方法优劣判断。

代码开放状态仅指访问时看到的内容。本轮未 clone 并执行研究系统，因而不声称“已复现”。论文 self-reported accepted 的会议状态不等于本轮已核到会议终版；方法判断固定到表内明确的原文版本。

## 2. D-ledger 增补

**D312 — Part 3 前一版最近邻调查不足，候选方向尚不能被表述为研究空白。** 2026-09-29 初稿 §五以 GEPA、ADIAS、DGM、SpeedRunner、SkillWeaver、WALT、ActionEngine 等为主要依据；没有覆盖 AutoSaddler、PRISM、Harness-R1、AutoManual、LearnAct、AutoDroid-V2 及成本导向的 harness adaptation。新增证据表明完整闭环、修复位置选择、可执行动作学习、RL 训练修改者均有直接先例。初稿本已把实验机制称为待验证假设，本次不把它误记成“曾宣称首次”；需修订的是最近邻范围和后续立项依据。以本文为相关工作入口，原草稿和 Word 版不视为已确认方案。

## 3. E-ledger 增补与合并补丁

Canonical v3 保持不变。既有 E304–E308 和 D311 保留；以下为新增文献登记及精确追加文本，供后续 v3.1 合并。全文中的 A/B 是阅读深度，所有链接来源仍按 primary 标注；论文报告的结果未经本项目复现。

下表“追加文本”按原样加入新版本证据登记表；没有用这些文字替换 canonical v3 的已有量化结论。

| ID | 精确追加文本 | Primary 来源 / 版本日期 |
|---|---|---|
| E309 | AutoSaddler 从批量执行轨迹诊断并生成 prompt/tool/middleware 补丁，经训练批验证和开发集选择更新 harness，最后单独测试；附录分列优化器与任务 rollout 开销。 | [§§3–4、App. I/R](https://arxiv.org/html/2608.23041v1)，2026-08-24，primary preprint |
| E310 | Self-Harness 用同一冻结模型从失败模式提出有限的 harness 修改，以 held-in/held-out gate 决定接受；该 held-out 参与持续选择，非未使用最终测试集。 | [§§3–4](https://arxiv.org/html/2606.09498v3)，2026-08-20，primary preprint |
| E311 | RHO 从历史任务中选择子集并重做，用自验证、一致性与自偏好选择指令、技能和工具更新；不依赖外部标准答案不等于没有额外执行或已保证正确。 | [§4、App. D/G/H](https://arxiv.org/html/2606.05922v3)，2026-08-29，primary preprint |
| E312 | PRISM 根据失败簇把修复分配给 prompt、工具边界 middleware 或联合编辑，以验证集选择候选；其 middleware 编辑模式受限，费用为搜索诊断口径。 | [§§3–4、App. F](https://arxiv.org/html/2609.05736v2)，2026-09-09，primary preprint |
| E313 | Better Harnesses, Smaller Models 从失败轨迹自动适配小模型的指令、工具和执行循环，报告运行费用、端到端延迟与前期优化投入；主要降费比较含模型替换。 | [§§II–IV、Table II](https://arxiv.org/html/2607.08938v1)，2026-07-09，primary preprint |
| E314 | Harness-R1 用修改后冻结目标 Agent 的执行结果训练独立 harness editor；主训练 reward 来自同批重跑，没有跨批持久补丁记忆，另有未见任务泛化评估。 | [§§3–5、App. F](https://arxiv.org/html/2608.02276v1)，2026-08-03，primary preprint |
| E315 | AutoManual 从训练交互轨迹区分规则缺陷与 Agent 执行错误，更新、合并并整理可跨任务使用的环境规则；主要产物为手册而非完整状态图。 | [§3.3、App. D](https://arxiv.org/html/2405.16247v4)，2024-11-10，primary paper |
| E316 | LearnAct 从失败训练任务修订 Python 高级动作或动作使用说明，并以执行结果选候选；测试在 Robotic Planning / ALFWorld，不能直接视为 Web UI 维护证据。 | [§§3–4](https://openreview.net/pdf?id=KqK5XcgEhR)，COLM 2024，primary conference paper |
| E317 | AgentOptimizer 根据函数使用历史增删改函数描述和实现，通过训练任务重跑、回退及停止策略优化 Agent；属于轨迹到可执行能力修改的较早先例。 | [§§2–3](https://arxiv.org/html/2402.11359v4)，2024-07-30，primary paper |
| E318 | Agent Symbolic Learning 用节点执行记录形成语言反馈，更新 prompt、tool 和 pipeline 并重跑回退；部分标准任务实验禁用工具，框架可表达范围与已验证范围需区分。 | [§3.2、§4.1](https://arxiv.org/html/2406.18532v1)，2024-06-26，primary preprint |
| E319 | Meta-Harness 允许 coding proposer 检索历史源码、分数及轨迹来搜索 harness，包含上下文成本权衡；论文所链最终 artifact 不等于完整搜索循环已公开。 | [§§3–4](https://arxiv.org/html/2603.28052v1)，2026-03-30，primary preprint；[作者 artifact](https://github.com/stanford-iris-lab/meta-harness-tbench2-artifact) |
| E320 | AHE 将轨迹证据连接到文件级 harness 修改，并评估修改者的修复/回归预测；预测与结果相符不构成唯一因果证明，token 均值亦有 trial 排除条件。 | [§3、§4.4.2](https://arxiv.org/html/2604.25850v1)，2026-04-28，primary preprint |
| E321 | ReasoningBank 从自判成功及失败的轨迹积累可检索经验；所报 actor 执行减少不等于含判断与记忆提炼的总 token 降低。 | [§3、App. C.2/Table 5](https://arxiv.org/pdf/2509.25140v2)，2026-03-16，primary paper |
| E322 | EvolveR 联合维护成功/失败经验库并用 GRPO 训练任务 actor，区别于冻结模型的外部记忆，也区别于训练 harness editor。 | [§3、App. A](https://arxiv.org/pdf/2510.16079v3)，2026-05-16，primary paper |
| E323 | On the Fragility of Self-Improving Agents 检验多次运行和任务顺序对记忆方法的影响；实验为隔离判断噪声使用真值 reward，不能当作无标注原设定的完全复现。 | [§§3–4](https://arxiv.org/pdf/2608.18066v2)，2026-09-06，primary preprint |

既有条目仅追加机制说明，不替换原数字：

- **E227 追加：**“AutoDroid-V2 的元素转移图记录前后依赖，用于程序生成和运行恢复；其主要推理时间指标排除 GUI 执行。环境表示机制见 v3 §3.1.3，原数值口径保持。”
- **E230 追加：**“WALT 的工具具备参数 schema、前置条件和预期结果，并可混合确定性与 agentic 步骤。本文按 arXiv v1 核机制；正式 ICLR 2026 的新增成本证据沿 deck audit 分别引用，不能由本轮抓取失败推定缺失。”
- **E307 / E308：**沿用上一轮证据及 D311，不再重复分配新 ID；本轮把环境结构、探索来源和验证条件加入相关工作对照。

## 4. 仍待明确的问题

1. **研究目标需要在最近邻比较后再收窄。** 是学习稳定、跨任务可复用的改动，还是针对当批失败做适配？是生成新 action，还是维护已有 action 的适用条件？这些不是同一个问题。
2. **我们能取得什么反馈仍未知。** 自动判断业务成功、识别数据被正确写入、以及能够重置环境，会改变可采用的优化器；RHO 的自评反馈和 AutoSaddler 的外部结果判据应分别看待。
3. **固定界面不等于已经穷尽环境。** 用户权限、历史、后端状态和异步交互可能使相同界面对应不同结果。这是对任务设定的提醒，不是已经证实的本项目创新点。需要真实轨迹确认哪些状态可观察、哪些操作可重放。
4. **净收益和泛化尚需用同一协议对照。** 前期探索、分析、生成、失败候选和验证投入都要记录；测试已见模板与新模板应分开。已经有摊销研究，所以贡献必须落实到优于什么已有方法、在什么条件下。
5. **本轮没有执行论文代码或训练模型。** 官方仓库可达、论文描述可读与结果可复现是不同状态。摘要级条目和代码开放边界已分别标注；不能拿本轮文献核查替代复现实验。

下一次讨论应先选最接近我们任务条件的几篇做机制级对照，再决定第三部分怎样讲研究目标。预算计算继续留到方法与实验规模明确之后。
