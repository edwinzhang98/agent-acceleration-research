# 第三部分的相关工作调查：从执行轨迹改进 Agent，及从交互经验学习环境

核查日期：2026-09-29；已按用户最新来源规则筛选，并补齐文末 References。本文先回答“已有工作做到哪里”，不确定本项目的方法、实验配置或预算。此前的 [研究方向草稿](../notes/2026-09-29-part3-research-proposal-zh.md) 只保留为讨论记录；其最近邻清单不完整，不能据此判定研究空白。本文优先于该草稿的相关工作判断。

## 1. 证据与核查

### 1.0 本次来源筛选结果与引用规则

按用户 2026-09-29 的要求，复核此前 **51 项**候选：**48 项保留**（26 项以正式顶刊顶会来源优先，22 项按合格高校/实验室背景补充），**3 项不进入正文依据和正式 References**。逐项去留、机构与 venue 证据见 [来源筛选记录](2026-09-29-part3-source-filter.md)。本轮范围是这份第三部分调查；前两部分 slides 的引用未在此轮重新筛查。

1. **优先顶刊、顶会正式发表版本。** 优先来源包括 Nature、NeurIPS、ICML、ICLR、ACL/EMNLP 主会、AAAI、COLM、TMLR，以及相关领域的 CHI、MobiCom、MobiSys。Workshop、Findings、普通期刊不自动等同主会或顶刊；须标具体 track，或另外满足机构门槛。
2. **其次允许头部 AI 厂商的官方技术材料。** OpenAI、Anthropic、Google/DeepMind（Gemini）、Groq 等同级来源可考虑；普通公司博客、营销材料、聚合站不作为论文结论的依据。本次候选均为论文，没有为凑层级补入博客。
3. **高水平高校或研究实验室的预印本可作为补充。** 必须核实论文署名中的机构关系，并列出具体机构；不能把“有大学名字”或“有公司研究组”直接当作通过。未核实正式发表的仍标预印本；若同一研究另有普通期刊或 workshop 版本，标明真实 venue，不升级为顶刊顶会。例如 Symbolic Learning 按浙江大学等机构背景保留，AutoHarness 按 Google DeepMind 背景保留。

正式发表信息与实际核读版本分别记录：References 优先列正式题名、作者顺序和 venue；表内保留所读 arXiv 版本，避免把旧版本的机制或数字假装成终版复核。A/B 继续只表示阅读深度，**不代表来源质量等级**。过滤决定本稿采用哪些证据，不用于推断被移出工作不存在。

### 1.1 目前能够得出的结论

**两个方向都有直接先例，而且部分工作已经把它们连接起来。** 第一条线通常称为 automatic agent / harness optimization：根据轨迹修改模型外的指令、工具、记忆和执行逻辑。第二条线跨越 environment learning、workflow induction 和 executable skill learning：把交互经验变成规则、状态关系或可执行动作。只用“从失败中学习”“全自动改 Agent”“生成更精确的 action”来描述贡献，无法与已有研究区分。

这里的 **harness** 指模型周围的执行系统，包括 prompt、工具接口、上下文构造、检查和恢复逻辑；不同论文允许修改的范围不同，不能看到这个词就认为它允许修改全部代码。

尤其需要补入上一轮调查遗漏的三个事实：

- **完整自动闭环已存在。** AutoSaddler、Self-Harness 等已经把诊断、修改、重跑、选择串起来。按失败证据改函数或多种 harness 组件，可先对照 AgentOptimizer 与 AutoSaddler。见 E317、E309、E310。
- **学习“如何修改 Agent”的 RL 已存在。** Harness-R1 训练的是修改执行系统的模型，奖励来自修改后目标 Agent 的实际表现。这比一般“用 RL 训练执行策略”更接近用户所说的学习试错过程。详见本文的 RL 对照。
- **效率与前期投入也已有直接研究。** Better Harnesses, Smaller Models 测运行费用和延迟，并讨论优化开销；ActionEngine、AutoDroid-V2 也不能仅归为成功率工作。需要逐篇比较计费范围，不能把“计入学习成本”笼统称为无人研究。

这些判断并不意味着没有可做的问题。它们意味着下一步应从具体任务分布、反馈条件、允许的修改和测量目标寻找差别；**本轮不把“尚未在某论文报告”升级为整个领域的研究空白。**

### 1.2 最直接的自动改进工作

以下条目以 primary 原文为依据。A 表示已核查全文的相关方法、实验或限制章节；B 表示仅完成摘要或有限章节筛选。A 不代表复现，更不代表逐字审读全文。表中英文短引只用于定位证据。

| ID / 论文与版本 | 轨迹怎样变成改进 | 验证方式、效率证据与边界 | 原文定位 / 判断 |
|---|---|---|---|
| **E317 · Offline Training of Language Model Agents with Functions as Learnable Weights（AgentOptimizer）**，2024-07-30，v4；[全文](https://arxiv.org/html/2402.11359v4)；[Zhang et al., 2024](#ref-e317) · **顶刊顶会优先** | 从函数调用等执行历史中新增、删除、修改函数描述与代码，再跑训练任务，支持 rollback / early stop。 | 已覆盖“现有 action 不好用，改或新增 action 再验证”。主要是任务表现，未据所读实验确认部署总费用摊销。早期标题不同，不能算两篇。 | A；§2：“how the agent uses current functions”。**重要的较早直接先例。** |
| **E309 · AutoSaddler**，2026-08-24，v1；[全文](https://arxiv.org/html/2608.23041v1)；[Park et al., 2026](#ref-e309) · **合格机构补充** | 用一批成功及失败轨迹和 harness 代码诊断，生成 prompt、tool、middleware 补丁；可新增工具。反思修好、回归和仍失败的案例，存入 EvoDAG 再组合候选。 | 同批重跑筛选，再用 dev 选择；最终 test 不参与修改。以成功表现为主，App. I 分列优化器和任务执行开销。假定训练任务有结果判据，所选编辑空间不包含记忆/技能整理。 | A；§§3–4、Table 1、App. I/R：“structured patch generation that treats the harness as code”。**方向一的完整近邻。** |
| **E310 · Self-Harness: Harnesses That Improve Themselves**，2026-08-20，v3；[全文](https://arxiv.org/html/2606.09498v3)；[Zhang et al., 2026c](#ref-e310) · **合格机构补充** | 聚合 verifier 支持的失败模式，由同一冻结模型提出有限的 harness 修改，再回归测试。 | 修改限于声明的配置接口。held-out split 反复参与 promotion gate，功能上是验证集，不能叫最终未使用测试集。主证据为通过率。 | A；§§3.2–3.4、4.1：“verifier-grounded failure signatures”。**高频失败归类与自动保留修改已有实现。** |
| **E311 · Evolving Agents in the Dark: Retrospective Harness Optimization via Self-Preference（RHO）**，2026-08-29，v3；[全文](https://arxiv.org/html/2606.05922v3)；[Pan et al., 2026](#ref-e311) · **合格机构补充** | 选历史任务子集，额外并行重做，以自验证和多轨迹一致性生成指令、skill、工具脚本候选，用自偏好选择。 | 优化不依赖外部标准答案，但仍需额外执行，且自判不是正确性保证。App. G 分析优化阶段开销；一次 agent invocation 不等于一次模型调用。 | A；§4、App. D/G/H：“without claiming an efficiency advantage”。**实际部署难拿标注，也已有专门研究。** |
| **E313 · Better Harnesses, Smaller Models: Building 90% Cheaper Agents via Automated Harness Adaptation**，2026-07-09，v1；[全文](https://arxiv.org/html/2607.08938v1)；[Yang et al., 2026](#ref-e313) · **合格机构补充** | 把失败模式映射到指令、工具和执行循环的修改，通过 meta-agent 搜索适合小模型的执行系统。重复业务流程是重要适用条件。 | 有 train/validation/test；Table II 同时报准确率、单实例 token 计价费用和端到端延迟，§IV 讨论前期优化投入。主要费用比较包含换模型，不能表述为固定同一模型的等成功率降费。 | A；§§II–IV：“automatically discovers effective adaptations from failure trajectories”。**与重复业务场景和加速动机都直接相关。** |
| **E318 · Symbolic Learning Enables Self-Evolving Agents**，2024-06-26，v1；[全文](https://arxiv.org/html/2406.18532v1)；[Ou et al., 2025](#ref-e318) · **合格机构补充** | 记录节点输入、输出、prompt 和工具调用，用 language loss / gradient 改 prompt、tool、pipeline，并重新运行及回退。 | 文字“梯度”不是权重反传；部分标准任务实验禁用 tools，不能认为每张结果表都验证了新工具学习。 | A；§3.2：“PromptOptimizer, ToolOptimizer, and PipelineOptimizer”。**多种修改位置不是新的大类。** |
| **E319 · Meta-Harness: End-to-End Optimization of Model Harnesses**，2026-03-30，v1；[全文](https://arxiv.org/html/2603.28052v1)；[Lee et al., 2026](#ref-e319) · **合格机构补充** | coding proposer 自主检索既往源码、分数、原始轨迹，编辑完整 harness 候选并评价。 | 包含准确率—上下文成本的比较，不能直接换成美元或时间。论文所链 repo 主要为最终优化产物，不是已确认完整外层搜索开源。 | A；§§3–4：“source code, scores, and execution traces”。**直接把长期历史交给 coding agent 也是现成基线。** |
| **E320 · Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses（AHE）**，2026-04-28，v1；[全文](https://arxiv.org/html/2604.25850v1)；[Lin et al., 2026](#ref-e320) · **合格机构补充** | 从分层轨迹证据定位问题，修改 prompt、工具、middleware、skills、subagents、记忆等文件，记录预期修复与回归，在下一轮核对。 | §4.4.2 已测修复/回归预测；不是唯一因果证明。演化集与外部任务迁移分别报告。tokens/trial 排除部分超时/中断，不能称所有尝试的平均费用。 | A；§3：“pairs every edit with a self-declared prediction”。**诊断是否正确也已有实测研究。** |
| **既有 E305 · ADIAS: Automated Design of Interactive Agentic Systems**，2026-08-03，v1；[全文](https://arxiv.org/pdf/2608.06410v1)；[Jiang et al., 2026](#ref-e305) · **合格机构补充** | 把真实交互问题保存为带身份、状态、优先级和干预历史的 issue，持续诊断、修改整套代码并评价。 | 有训练/验证/测试分工；效率量为任务得分与环境步数的比值，非墙钟或美元；没有单独测归因标签准确率。 | A；§3.3、App. C/D、Limitations；**跨轮不忘记问题已有直接先例。** |

其余自动优化工作保留作方法来源和比较边界。下面的 R 编号仅是本调查条目号，尚未全部提升为 dossier 的独立 E 条目。

| 调查 ID / 工作及固定阅读版本 | 已核查的作用与边界 | 定位与阅读级别 |
|---|---|---|
| R01 · **Automated Design of Agentic Systems（ADAS）**；[2024 v1](https://arxiv.org/html/2408.08435v1)；[Hu et al., 2025](#ref-r01) · **顶刊顶会优先** | 生成 agent 代码，执行、评估、归档并搜索新候选；以任务表现和候选历史为主。附录已报告搜索/评价开销，不等于部署摊销。 | A；§§2–4、App. G |
| R02 · **Trace is the Next AutoDiff: Generative Optimization with Rich Feedback, Execution Traces, and LLMs**；[NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/file/83ba7056bce2c3c3c27e17397cf3e1f0-Paper-Conference.pdf)；[Cheng et al., 2024](#ref-r02) · **顶刊顶会优先** | 优化计算图里指定的异构变量，包括代码和 prompt；其 trace 常是计算过程，不应等同长期浏览器交互轨迹。 | A；§§1–4 |
| R03 · **TextGrad: Automatic “Differentiation” via Text**；[2024 v1](https://arxiv.org/html/2406.07496v1)；[Yuksekgonul et al., 2025](#ref-r03) · **顶刊顶会优先** | 用文本反馈优化指定变量；单题答案精炼与跨题 prompt 学习要区分，未自动接管全部 Agent 代码。 | A；§§2–3、App. E |
| R04 · **AFlow: Automating Agentic Workflow Generation**；[2025 v4](https://arxiv.org/html/2410.10762v4)；[Zhang et al., 2025a](#ref-r04) · **顶刊顶会优先** | 根据执行反馈搜索代码表示的工作流。报告推理费用与搜索效率；不等于持久 Web 环境知识维护。 | A；§§3–4、App. C/D |
| R05 · **AgentSquare: Automatic LLM Agent Search in Modular Design Space**；[2025 v3](https://arxiv.org/html/2410.06153v3)；[Shang et al., 2025](#ref-r05) · **顶刊顶会优先** | 重组及生成 planning/reasoning/tool-use/memory 模块；新模块实跑，已有模块重组可用 surrogate 评价。不是原始失败轨迹的 issue 归因系统。 | A；§§3.4–4.2 |
| 既有 E304 · **GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning**；[2026 v2](https://arxiv.org/pdf/2507.19457v2)；[Agrawal et al., 2026](#ref-e304) · **顶刊顶会优先** | 执行轨迹反思、模块修改、候选选择；主论文以 prompt 为主，框架也可用于代码。Pareto 主要指任务表现维度，非时间—费用前沿。 | A；§3、Alg. 1、App. E/I |
| 既有 E306 · **Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents（DGM）**；[2025 v2](https://arxiv.org/html/2505.22954v2)；[Zhang et al., 2026b](#ref-e306) · **顶刊顶会优先** | 从评估日志诊断、改自身代码并保存候选群体；代码任务成绩和研究 API 投入，不等于重复 Web 工作流的净加速。 | A；§§3–4、App. C/E |
| R06 · **AutoHarness: improving LLM agents by automatically synthesizing a code harness**；[2026 v1](https://arxiv.org/html/2603.03329v1)；[Lou et al., 2026](#ref-r06) · **合格机构补充** | 在 TextArena 用环境失败反馈生成检查器、动作提议器或完整代码策略。只有完整 code policy 才无需在线模型；合成仍有成本。 | A；§§3–4、App. B/C |
| R07 · **MOSS: Self-Evolution through Source-Level Rewriting in Autonomous Agent Systems**；[2026 v1](https://arxiv.org/html/2605.22794v1)；[Cai et al., 2026](#ref-r07) · **合格机构补充** | 从失败会话到源码修复、容器试验和判定；实证规模很小，主要同批首轮；生产 apply 仍需用户触发。不能把自动试验等同自动上线。 | A；§§2–4 |
| 既有 E271 · **Better, Faster, Stronger: Programmatic Skill Learning Best Reduces Agent Cost（SpeedRunner）**；[2026 v1](https://arxiv.org/html/2608.11338v1)；[Huang et al., 2026](#ref-e271) · **合格机构补充** | wake 收集轨迹，sleep 自动增删改代码技能，考虑后续复用及诱导成本；每次在线修改不经过持续 replay gate，论文另做周期评测。 | A；§§2–3、App. A/G；文本交互环境 |

### 1.3 从环境经验到规则、状态和可执行动作

“学习环境”至少有三个不同含义：记住文字规则；掌握什么状态下可以做什么、之后会发生什么；把经验证的操作封装成参数化代码。下面按实际产物区分，不把一段操作说明等同于可执行环境模型。

| ID / 工作与阅读版本 | 经验来源 → 学到的东西 | 与用户设想的关系及证据边界 |
|---|---|---|
| **E315 · AutoManual: Constructing Instruction Manuals by LLM Agents via Interactive Environmental Learning**；[2024-11-10 v4](https://arxiv.org/html/2405.16247v4)；[Chen et al., 2024](#ref-e315) · **顶刊顶会优先** | 做训练任务时的成功、试错和失败 → 条件规则、流程、已修/未修错误及验证日志；会整理和删除冗余。 | A，§3.3；明确区分 **“Imperfect Rules” / “Imperfect Agent”**，再更新规则。初始化仍有人工示例与初始规则；主要产物是手册，非强制执行的 API 或完整环境图。两个方向在此已经相交。 |
| **E316 · Empowering Large Language Model Agents through Action Learning（LearnAct）**；[COLM 2024](https://openreview.net/pdf?id=KqK5XcgEhR)、[v2](https://arxiv.org/html/2402.15809v2)；[Zhao et al., 2024a](#ref-e316) · **顶刊顶会优先** | 先生成 Python 高级动作与用法，再运行训练任务，依据失败修动作。 | A，§§3–4；可选择修函数或补使用说明，用执行结果选候选。很接近“现有 action 不够，需要写新 action”；实证为 Robotic Planning / ALFWorld，非真实 Web UI。与同名 2026 移动 GUI LearnAct 区分。 |
| **既有 E230 · WALT: Web Agents that Learn Tools**；[2025 arXiv v1](https://arxiv.org/html/2510.01524v1)、[ICLR 2026](https://iclr.cc/virtual/2026/poster/10008481)；[Prabhu et al., 2026](#ref-e230) · **顶刊顶会优先** | 自主功能探索/示范 → 参数 schema、枚举、前置条件、预期结果及工具代码；确定性和需要模型的步骤可混合。 | A，v1 §3：“preconditions, and expected outcomes”。失败修脚本并验证，部署可 fallback。v1 的 steps 非墙钟；本轮终版 PDF 抓取因文件过大失败，正式新增成本数据应沿现有 deck audit 核，不说作者没报。 |
| **既有 E227 · AutoDroid-V2: Boosting SLM-based GUI Agents via Code Generation**；[2025-05-06 v3](https://arxiv.org/html/2412.18116v3)；[Wen et al., 2025](#ref-e227) · **顶刊顶会优先** | 主动探索 → 元素转移图与前后依赖；生成任务/程序并验证，SFT 小模型产 GUI 脚本。 | A，§3.1.3：“Forward and Backward Dependency”。与“把环境规律落实为动作”直接相关。核心时间量是 **LLM inference latency，排除 GUI 执行**；有文档/数据/验证成本，不能说建设成本未报告。 |
| **既有 E229 · Inducing Programmatic Skills for Agentic Tasks（ASI）**；[2025 v2](https://arxiv.org/html/2504.06821v2)；[Wang et al., 2025b](#ref-e229) · **顶刊顶会优先** | 在线任务中被判成功的轨迹 → 参数化 Python 技能；额外 rollout 验证替换片段是否有效。 | A，§2；“all skill-calling actions cause environment changes”。模型自判不等于外部语义保证；运行 steps 不包含全部归纳验证投入。 |
| **既有 E272 · Agent Workflow Memory（AWM）**；[2024 v1](https://arxiv.org/html/2409.07429v1)；[Wang et al., 2025a](#ref-e272) · **顶刊顶会优先** | 成功经历归纳为 workflow memory，在后续任务中提供给模型。 | A，既有 Part 2 核查接续；不能把文字 workflow 当无需模型介入的可执行 macro。本文保留仓库 D41/D201 的口径限制，不重报 headline。 |
| R09 · **AppAgent: Multimodal Agents as Smartphone Users**；[所读 v3](https://arxiv.org/html/2312.13771v3)；[Zhang et al., 2025b](#ref-r09) · **顶刊顶会优先** | 主动探索或人类示范 → 页面元素用途和效果的语义文档。 | A，§§3–4；后续仍逐步用模型操作，不等同自动生成代码工具。探索投入与成功任务上的 steps 需要分开。 |
| R11 · **MobileGPT: Augmenting LLM with Human-like App Memory for Mobile Task Automation**；[2024 v3](https://arxiv.org/html/2312.03003v3)；[Lee et al., 2024](#ref-r11) · **顶刊顶会优先** | 随机探索、任务经验和用户输入 → 任务/子任务/动作的层级记忆与参数化回放。 | A，§§2–5、7；有费用和时间实验，但 cold-start 失败经人工修复后入库，warm-start 高成功率不能当作无人自改进证据。 |
| R12 · **AutoDroid: LLM-powered Task Automation in Android**；[2024 v4](https://arxiv.org/html/2308.15272v4)；[Wen et al., 2024](#ref-r12) · **顶刊顶会优先** | 离线动态探索 → UI Transition Graph、功能知识和合成任务；还用捷径与等价界面合并。 | A，§3、§6.5；有离线时间和运行调用/token 证据，未据所读实验确认长期失败驱动的持续图维护。 |
| R13 · **Is Your LLM Secretly a World Model of the Internet? Model-Based Planning for Web Agents（WebDreamer）**；[2025 v2](https://arxiv.org/html/2411.06559v2)；[Gu et al., 2025](#ref-r13) · **顶刊顶会优先** | 预测动作后的观察变化并打分规划；v2 另收集网页转移数据训练 Dreamer。 | A，§3、§5；这是预测模型，非 action API 库。减少真实树搜索的开销可能仍比 reactive agent 慢，比较基线不能省略。 |
| R14 · **Web Agents with World Models: Learning and Leveraging Environment Dynamics in Web Navigation（WMA）**；[2025 v2](https://arxiv.org/html/2410.13232v2)；[Chae et al., 2025](#ref-r14) · **顶刊顶会优先** | 主动/离线网页交互 → 预测状态变化的模型，配合固定 policy 候选及 value 评分。 | A，§§4–5、App. C；训练的是 world model，不是直接训练 task policy；没有输出完整显式状态图或代码工具。运行费用与树搜索相比，未含全部训练投入。 |
| R15 · **AutoGuide: Automated Generation and Selection of Context-Aware Guidelines for Large Language Model Agents**；[2024 v2](https://arxiv.org/html/2403.08978v2)；[Fu et al., 2024](#ref-r15) · **顶刊顶会优先** | 好/坏离线经验对照 → 按上下文检索的文字指南。 | A，§3、App. B.4；某些真实站点使用人类正例，非全自主探索；是失败经验和环境知识的近邻，不是可执行动作生成。 |
| **既有 E308 · SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills**；[2025 v1](https://arxiv.org/html/2504.07079v1)；[Zheng et al., 2025](#ref-e308) · **合格机构补充** | 主动探索、成功轨迹、额外测试 → 参数化 Playwright API 与前置状态说明。 | A，§2、App. D.2；“description of the prerequisite state”。自动合成、测试、调试；judge 可能被不抛异常的错误代码误导。主要证明任务表现，不能据此推定总费用下降。 |
| **既有 E307 · ActionEngine: From Reactive to Programmatic Web Agents via State Machine Memory**；[2026-09-28 v2](https://arxiv.org/html/2602.20502v2)；[Zhong et al., 2026](#ref-e307) · **合格机构补充** | 额外主动探索 → UI 模板、操作、状态转移和动态数据访问路径；编译成任务程序。 | A，§§3–5；“initial SMG construction is task-independent”。架构有知识回写 Patcher；主评估按任务模板 warm-up，且关闭 Patcher。已报运行效率和探索摊销；不能据主实验宣称新模板泛化或持续维护收益。 |
| R10 · **AppAgentX: Evolving GUI Agents as Proficient Smartphone Users**；[2025 v3](https://arxiv.org/html/2503.02268v3)；[Jiang et al., 2025](#ref-r10) · **合格机构补充** | 运行历史的状态—动作—状态链 → 可参数化的高级 shortcut，运行时检索、判适用、失败回退。 | A，§§4–5；接近被动积累，但仍有分析生成开销。时间比较只统计双方均成功任务，tokens 统计所有任务；未确认系统性的失败归因机制。 |

由此可见，**外部规则、可执行技能、显式状态关系、学习到的预测模型应分开比较**。它们都可能减少重复试错，但需要不同数据，也可能增加每次调用的成本。不能先把“有环境学习”统称为相同能力。

### 1.4 失败经验、记忆与强化学习

| ID / 工作与阅读版本 | 真正更新的对象 | 自动化与评价边界 |
|---|---|---|
| R16 · **ExpeL: LLM Agents Are Experiential Learners**；[2024 v3](https://arxiv.org/pdf/2308.10144v3)；[Zhao et al., 2024b](#ref-r16) · **顶刊顶会优先** | 对比成功与失败轨迹，维护可增删改的跨任务文字 insights，检索给后续任务；模型冻结。 | A，§§3–4；“deterministic environments”。失败经验跨任务复用已有先例，但没有生成新 action 或训练代码修改者。 |
| **E321 · ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory**；[2026-03-16 v2](https://arxiv.org/pdf/2509.25140v2)；[Ouyang et al., 2026](#ref-e321) · **顶刊顶会优先** | 自判轨迹成败，提炼成功策略与失败经验，写入跨任务记忆并检索；actor 冻结。 | A，§3、App. C.2/Table 5；“total token consumption is increased”。执行 steps 或 actor tokens 降低不等于含判断/提炼的总开销下降。 |
| R19 · **Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models（ACE）**；[2026 v3](https://arxiv.org/pdf/2510.04618v3)；[Zhang et al., 2026a](#ref-r19) · **顶刊顶会优先** | Generator / Reflector / Curator 从轨迹和反馈维护 playbook，增量更新、合并与去重。 | A，§3、§4.7、App. F；“context adaptation latency”。错误归因的产物主要是上下文；所报 adaptation 费用/时间不同于最终任务服务延迟。 |
| R21 · **Reflexion: Language Agents with Verbal Reinforcement Learning**；[2023 v4](https://arxiv.org/pdf/2303.11366v4)；[Shinn et al., 2023](#ref-r21) · **顶刊顶会优先** | 同任务反馈、反思和 episodic memory，指导后续重试；不改权重。 | A，§3；“not by updating weights”。名称有 RL 不代表梯度式 policy training；主实验不能直接当未见任务的持久系统改进。 |
| R22 · **Self-Refine: Iterative Refinement with Self-Feedback**；[2023 v2](https://arxiv.org/pdf/2303.17651v2)；[Madaan et al., 2023](#ref-r22) · **顶刊顶会优先** | 对当前答案/程序生成反馈并迭代精炼。 | A，§2；没有核心跨任务持久更新，主要是比较边界。生成的程序运行更快不等于 Agent 自己推理更快。 |
| R23 · **Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models（LATS）**；[2024 v3](https://arxiv.org/pdf/2310.04406v3)；[Zhou et al., 2024](#ref-r23) · **顶刊顶会优先** | 用反思、模型 value 和环境反馈指导当前任务的树搜索。 | A，§§4–6；无核心跨任务 updater。比某些树搜索节省计算，仍可能比简单 reactive 方法贵。 |
| **E314 · Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories**；[2026-08-03 v1](https://arxiv.org/html/2608.02276v1)；[Shao et al., 2026](#ref-e314) · **合格机构补充** | 从失败包生成可执行 hooks，用目标 Agent 重跑结果做 SFT + GRPO，训练独立的 **harness editor**；目标模型冻结。 | A，§3、§4.4、App. F；“persistent patch memory across batches” 是原文明确没有的能力。训练 reward 来自同批重跑；另有未见任务泛化测试，不能说“只测了原任务”。也不是不受限制地改任意代码。 |
| R17 · **Memento: Fine-tuning LLM Agents without Fine-tuning LLMs**；[2025 v2](https://arxiv.org/pdf/2508.16153v2)；[Zhou et al., 2025](#ref-r17) · **合格机构补充** | 保存案例；非参数版检索，参数版训练独立 Q 网络来选择案例。 | A，§4.2、§5；“online updates a Q-function”。冻结 LLM 不等于所有参数均不训练，也不是学出完整环境转移模型。 |
| R18 · **AgentEvolver: Towards Efficient Self-Evolving Agent System**；[2025 v1](https://arxiv.org/pdf/2511.10395v1)；[Zhai et al., 2025](#ref-r18) · **合格机构补充** | 自生成探索任务、经验引导 rollout、对动作作贡献归因，然后用过程/结果奖励训练 task-policy GRPO。 | A，§§3–7；归因主要用于训练 credit assignment，非自动修改代码。训练样本效率不能直接写为部署时间下降。 |
| **E322 · EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle**；[2026-05-16 v3](https://arxiv.org/pdf/2510.16079v3)；[Wu et al., 2025](#ref-e322) · **合格机构补充** | 成功/失败经验提炼与筛选，加上检索和 GRPO 更新 **任务 actor 权重**。 | A，§3、App. A：“GRPO”。不是纯冻结模型的反思记忆；主要问答效果，检索延迟与训练投入不能等同端到端加速。 |
| R20 · **Agent Q: Advanced Reasoning and Learning for Autonomous AI Agents**；[2024 v1](https://arxiv.org/pdf/2408.07199v1)；[Putta et al., 2024](#ref-r20) · **合格机构补充** | 搜索成功/失败分支、形成偏好，用 DPO 训练 task actor；可再加在线搜索。 | A，§§3–6；训练后的无搜索结果与推理时搜索结果应分开，需要反馈及可回退环境条件。 |
| **E323 · On the Fragility of Self-Improving Agents: Variance, Task Order, and Underspecification**；[2026-09-06 v2](https://arxiv.org/pdf/2608.18066v2)；[Ye et al., 2026](#ref-e323) · **合格机构补充** | 复核 AWM/ReasoningBank 的多次运行与任务顺序，观察记忆中的环境假设。 | A，§§3–4；“provide the ground-truth reward”。为了隔离判断噪声使用真值反馈，非原设定原样复现；提示不能以一次任务顺序的提升宣称稳定泛化，也不能反推所有记忆无效。 |
| R24 · **Co-Harness: Co-Evolving Harnesses and Model Weights for LLM Agents**；[2026 v1](https://arxiv.org/abs/2607.22688v1)；[Chen et al., 2026](#ref-r24) · **合格机构补充** | 摘要描述 harness 诊断更新与模型训练交替。 | **B**；未完整核查训练协议和测试隔离，不用于定量比较。仅说明两者联合演化已有明确先例。 |

针对“错误原因本身是否可靠”，另保留符合来源门槛、但本轮仅核摘要的相关条目：

- R26 · [**Phantom Guardrails: When Self-Improving Agent Harnesses Fix Failures That Never Happened**](https://arxiv.org/abs/2607.13083v1)，2026-07-13：在受控微型实验中观察到优化器给不存在的错误加规则。B；不能把该实验的频率推广到真实 Web 部署。 [Wang et al., 2026](#ref-r26) · 合格机构补充。

因此，“RL 可不可以用于这个过程”应进一步区分：**训练执行任务的模型、训练记忆检索器、训练提出修改的模型**。Harness-R1 最直接对应第三种；AutoManual 受 RL 范式启发地更新文字规则，则不等于同一种参数训练。


### 1.5 与前两部分 slides 的关系

前两部分回答“耗时和费用由哪些项构成，以及哪些机制能改变这些项”。本轮相关工作增加的是另一条分类轴：**这些机制由谁、根据什么证据产生和更新。** 自动优化器可能最终生成大动作、代码重放、上下文整理或工具接口改进，因此会与 Part 2 的多个方法家族相交。

| 用户关心的具体过程 | 最直接要比较的既有工作 | 与当前 slides 的连接 |
|---|---|---|
| 高频错误归因，决定修改位置，自动实现并验证 | AgentOptimizer、AutoSaddler、Self-Harness、AHE、ADIAS | 一次修改可能同时改变步数、每步模型调用、上下文长度和成功率；“有自动优化器”本身不是某个耗时项的减少。 |
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
| Better Harnesses, Smaller Models §IV | 同任务上模型与 harness 的费用、延迟、成功表现，以及搜索投入 | 所有任务保持同等成功率；标题降费幅度来自纯 harness 修改 |
| ActionEngine v2 | 环境预探索、程序执行及部分摊销证据 | 未见过的任务模板泛化；持续 Patcher 在线收益已经由主实验验证 |
| SpeedRunner | 技能诱导和后续复用的摊销值得纳入比较 | 文本交互环境的收益直接等于 Web 操作的美元收益 |
| ReasoningBank 等记忆方法 | 成功和失败经验可以改善后续决策 | 减少交互步骤就必然降低总 token 或端到端时延 |

### 1.7 检索范围与排除原则

检索截止为 2026-09-29。原始检索有 51 项；按新来源规则保留 **48 项**，其中 46 项核查方法及相关实验/限制章节（含前轮已核材料接续），2 项只作摘要级筛选，逐项标 A/B。本会话没有独立的 Deep Research 调用入口；实际采用三条并行检索、primary 全文核查及参考文献追踪。不是穷尽性或注册式 systematic review。搜索结果页、媒体解读和论文聚合站只用于发现线索，事实判断回到论文、正式会议页面或作者仓库。

主要检索词组包括 `agent trajectory self-improvement latency`、`agent failure harness optimization`、`AgentOptimizer Learning to Optimize`、`AutoManual LearnAct AutoGuide`，以及环境线的 trajectory / environment memory / workflow induction / skill discovery，经验线的 failure reflection / experience memory / agent reinforcement learning。根据 AutoSaddler、Harness-R1 等的 related work 继续追查近邻，并核对 RHO、Self-Harness 和 ActionEngine 的版本。

纳入标准是至少明确处理以下一项：轨迹驱动的持久修改；从环境经验提取可复用知识/动作；用执行反馈学习策略或修改策略。仅在单次回答中 self-critique、仅给模型更长思考时间、通用无轨迹的 prompt 搜索、纯 serving 优化，不作为两个方向的完整近邻；有比较价值的保留为边界条目。未完成来源资格审查的扩展检索线索不进入本文正式 References。

代码开放状态仅指访问时看到的内容。本轮未 clone 并执行研究系统，因而不声称“已复现”。论文 self-reported accepted 的会议状态不等于本轮已核到会议终版；方法判断固定到表内明确的原文版本。

## 2. D-ledger 增补

**D313 — 来源门槛更新。** 用户要求优先顶刊顶会、其次头部 AI 厂商官方材料，并允许高水平高校/实验室的预印本。此前“已读 primary”不足以自动取得引用资格。本次逐项筛选并更新引用，未通过者只在独立筛选记录留存，原 ID 不重新分配。

**D312 — Part 3 前一版最近邻调查不足，候选方向尚不能被表述为研究空白。** 2026-09-29 初稿 §五以 GEPA、ADIAS、DGM、SpeedRunner、SkillWeaver、WALT、ActionEngine 等为主要依据；没有覆盖 AutoSaddler、Harness-R1、AutoManual、LearnAct、AutoDroid-V2 及成本导向的 harness adaptation。新增证据表明完整闭环、修复位置选择、可执行动作学习、RL 训练修改者均有直接先例。初稿本已把实验机制称为待验证假设，本次不把它误记成“曾宣称首次”；需修订的是最近邻范围和后续立项依据。以本文为相关工作入口，原草稿和 Word 版不视为已确认方案。

## 3. E-ledger 增补与合并补丁

Canonical v3 保持不变。既有 E304–E308 和 D311 保留；本节只列通过当前来源门槛的追加文本，暂停的旧条目见 D313 和筛选记录；以下为新增文献登记及精确追加文本，供后续 v3.1 合并。全文中的 A/B 是阅读深度，所有链接来源仍按 primary 标注；论文报告的结果未经本项目复现。

下表“追加文本”按原样加入新版本证据登记表；没有用这些文字替换 canonical v3 的已有量化结论。

| ID | 精确追加文本 | Primary 来源 / 版本日期 |
|---|---|---|
| E309 | AutoSaddler 从批量执行轨迹诊断并生成 prompt/tool/middleware 补丁，经训练批验证和开发集选择更新 harness，最后单独测试；附录分列优化器与任务 rollout 开销。 | [§§3–4、App. I/R](https://arxiv.org/html/2608.23041v1)，2026-08-24，primary preprint |
| E310 | Self-Harness 用同一冻结模型从失败模式提出有限的 harness 修改，以 held-in/held-out gate 决定接受；该 held-out 参与持续选择，非未使用最终测试集。 | [§§3–4](https://arxiv.org/html/2606.09498v3)，2026-08-20，primary preprint |
| E311 | RHO 从历史任务中选择子集并重做，用自验证、一致性与自偏好选择指令、技能和工具更新；不依赖外部标准答案不等于没有额外执行或已保证正确。 | [§4、App. D/G/H](https://arxiv.org/html/2606.05922v3)，2026-08-29，primary preprint |
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

## 5. References

先列正式顶刊顶会来源，再列符合机构门槛的补充文献；每条对应正文作者—年份链接和原 E/R 标识。作者按实际引用版本顺序列出。出版信息核查不等于本轮重新复现或重算终版结果。

<a id="ref-e304"></a>

**[1] Lakshya A Agrawal; Shangyin Tan; Dilara Soylu; Noah Ziems; Rishi Khare; Krista Opsahl-Ong; Arnav Singhvi; Herumb Shandilya; Michael J Ryan; Meng Jiang; Christopher Potts; Koushik Sen; Alex Dimakis; Ion Stoica; Dan Klein; Matei Zaharia; Omar Khattab (2026).** *GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning*. ICLR 2026, main conference. [正式来源](https://proceedings.iclr.cc/paper_files/paper/2026/hash/0e9e708b6f48e14fd0ac29e167413f76-Abstract-Conference.html)。

来源等级：**顶刊顶会优先**；对应 E304。 机构：University of California, Berkeley; Stanford University; BespokeLabs.ai; University of Notre Dame; Databricks; Massachusetts Institute of Technology。 [实际核读版本](https://arxiv.org/pdf/2507.19457v2)。

版本/出处说明：正式会议作者表写 Alex Dimakis；所读 arXiv PDF 写 Alexandros G. Dimakis。

<a id="ref-r14"></a>

**[2] Hyungjoo Chae; Namyoung Kim; Kai Tzu-iunn Ong; Minju Gwak; Gwanwoo Song; Jihoon Kim; Sunghwan Kim; Dongha Lee; Jinyoung Yeo (2025).** *Web Agents with World Models: Learning and Leveraging Environment Dynamics in Web Navigation*. International Conference on Learning Representations (ICLR 2025), Conference. [正式来源](https://proceedings.iclr.cc/paper_files/paper/2025/hash/a00548031e4647b13042c97c922fadf1-Abstract-Conference.html)。

来源等级：**顶刊顶会优先**；对应 R14。 机构：Yonsei University。 [实际核读版本](https://arxiv.org/html/2410.13232v2)。 [机构/资格依据](https://proceedings.iclr.cc/paper_files/paper/2025/file/a00548031e4647b13042c97c922fadf1-Paper-Conference.pdf)。

<a id="ref-e315"></a>

**[3] Minghao Chen; Yihang Li; Yanting Yang; Shiyu Yu; Binbin Lin; Xiaofei He (2024).** *AutoManual: Constructing Instruction Manuals by LLM Agents via Interactive Environmental Learning*. Advances in Neural Information Processing Systems 37 (NeurIPS 2024), Main Conference Track. [正式来源](https://proceedings.neurips.cc/paper_files/paper/2024/hash/0142921fad7ef9192bd87229cdafa9d4-Abstract-Conference.html)。

来源等级：**顶刊顶会优先**；对应 E315。 机构：Hangzhou Dianzi University; Zhejiang University (State Key Lab of CAD&CG / School of Software Technology); Fullong Inc.; NingBo Port Group。 [实际核读版本](https://arxiv.org/html/2405.16247v4)。 [机构/资格依据](https://proceedings.neurips.cc/paper_files/paper/2024/file/0142921fad7ef9192bd87229cdafa9d4-Paper-Conference.pdf)。

<a id="ref-r02"></a>

**[4] Ching-An Cheng; Allen Nie; Adith Swaminathan (2024).** *Trace is the Next AutoDiff: Generative Optimization with Rich Feedback, Execution Traces, and LLMs*. NeurIPS 2024, Main Conference Track; Advances in Neural Information Processing Systems 37. [正式来源](https://proceedings.neurips.cc/paper_files/paper/2024/hash/83ba7056bce2c3c3c27e17397cf3e1f0-Abstract-Conference.html)。

来源等级：**顶刊顶会优先**；对应 R02。 机构：Microsoft Research; Stanford University; Netflix。 [实际核读版本](https://proceedings.neurips.cc/paper_files/paper/2024/file/83ba7056bce2c3c3c27e17397cf3e1f0-Paper-Conference.pdf)。

<a id="ref-r15"></a>

**[5] Yao Fu; Dong-Ki Kim; Jaekyeom Kim; Sungryull Sohn; Lajanugen Logeswaran; Kyunghoon Bae; Honglak Lee (2024).** *AutoGuide: Automated Generation and Selection of Context-Aware Guidelines for Large Language Model Agents*. Advances in Neural Information Processing Systems 37 (NeurIPS 2024), Main Conference Track. [正式来源](https://proceedings.neurips.cc/paper_files/paper/2024/hash/d8efbb5dd415974eb095c3f06bff1f48-Abstract-Conference.html)。

来源等级：**顶刊顶会优先**；对应 R15。 机构：University of Michigan; LG AI Research。 [实际核读版本](https://arxiv.org/html/2403.08978v2)。 [机构/资格依据](https://proceedings.neurips.cc/paper_files/paper/2024/file/d8efbb5dd415974eb095c3f06bff1f48-Paper-Conference.pdf)。

<a id="ref-r13"></a>

**[6] Yu Gu; Kai Zhang; Yuting Ning; Boyuan Zheng; Boyu Gou; Tianci Xue; Cheng Chang; Sanjari Srivastava; Yanan Xie; Peng Qi; Huan Sun; Yu Su (2025).** *Is Your LLM Secretly a World Model of the Internet? Model-Based Planning for Web Agents*. Transactions on Machine Learning Research (TMLR), journal paper, November 2025. [正式来源](https://openreview.net/forum?id=c6l7yA0HSq)；[TMLR 官方录用列表](https://jmlr.org/tmlr/papers/)。

来源等级：**顶刊顶会优先**；对应 R13。 机构：The Ohio State University; Orby AI。 [实际核读版本](https://arxiv.org/html/2411.06559v2)。

<a id="ref-r01"></a>

**[7] Shengran Hu; Cong Lu; Jeff Clune (2025).** *Automated Design of Agentic Systems*. ICLR 2025, main conference. [正式来源](https://proceedings.iclr.cc/paper_files/paper/2025/hash/36b7acf6f6010652b3f2a433774a66fe-Abstract-Conference.html)。

来源等级：**顶刊顶会优先**；对应 R01。 机构：University of British Columbia; Vector Institute; Canada CIFAR AI Chair。 [实际核读版本](https://arxiv.org/html/2408.08435v1)。 [机构/资格依据](https://proceedings.iclr.cc/paper_files/paper/2025/file/36b7acf6f6010652b3f2a433774a66fe-Paper-Conference.pdf)。

<a id="ref-r11"></a>

**[8] Sunjae Lee; Junyoung Choi; Jungjae Lee; Munim Hasan Wasi; Hojun Choi; Steve Ko; Sangeun Oh; Insik Shin (2024).** *MobileGPT: Augmenting LLM with Human-like App Memory for Mobile Task Automation*. Proceedings of the 30th Annual International Conference on Mobile Computing and Networking (ACM MobiCom 2024), research paper. [正式来源](https://doi.org/10.1145/3636534.3690682)。

来源等级：**顶刊顶会优先**；对应 R11。 机构：KAIST School of Computing; Simon Fraser University; Korea University; Fluiz。 [实际核读版本](https://arxiv.org/html/2312.03003v3)。 [机构/资格依据](https://api.crossref.org/works/10.1145/3636534.3690682)。

版本/出处说明：ACM 正式版写 Steve Ko；所读 arXiv v3 写 Steven Y. Ko。

<a id="ref-r22"></a>

**[9] Aman Madaan; Niket Tandon; Prakhar Gupta; Skyler Hallinan; Luyu Gao; Sarah Wiegreffe; Uri Alon; Nouha Dziri; Shrimai Prabhumoye; Yiming Yang; Shashank Gupta; Bodhisattwa Prasad Majumder; Katherine Hermann; Sean Welleck; Amir Yazdanbakhsh; Peter Clark (2023).** *Self-Refine: Iterative Refinement with Self-Feedback*. NeurIPS 2023, main conference track; Advances in Neural Information Processing Systems 36. [正式来源](https://proceedings.neurips.cc/paper_files/paper/2023/hash/91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html)。

来源等级：**顶刊顶会优先**；对应 R22。 机构：Carnegie Mellon University; Allen Institute for AI; University of Washington; NVIDIA; University of California, San Diego; Google DeepMind。 [实际核读版本](https://arxiv.org/pdf/2303.17651v2)。 [机构/资格依据](https://proceedings.neurips.cc/paper_files/paper/2023/file/91edff07232fb1b55a505a9e9f6c0ff3-Paper-Conference.pdf)。

<a id="ref-e321"></a>

**[10] Siru Ouyang; Jun Yan; I-Hung Hsu; Yanfei Chen; Ke Jiang; Zifeng Wang; Rujun Han; Long T. Le; Samira Daruki; Xiangru Tang; Vishy Tirumalashetty; George Lee; Mahsan Rofouei; Hangfei Lin; Jiawei Han; Chen-Yu Lee; Tomas Pfister (2026).** *ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory*. ICLR 2026, main conference, poster. [正式来源](https://iclr.cc/virtual/2026/poster/10007887)。

来源等级：**顶刊顶会优先**；对应 E321。 机构：University of Illinois Urbana-Champaign; Google Cloud AI Research; Yale University; Google Cloud AI。 [实际核读版本](https://arxiv.org/pdf/2509.25140v2)。 [机构/资格依据](https://openreview.net/pdf/25563ee680c408f3ad91eab8c7b4ec9ab05b7193.pdf)。

<a id="ref-e230"></a>

**[11] Viraj Prabhu; Yutong Dai; Matthew Fernandez; Krithika Ramakrishnan; Jing Gu; Yanqi Luo; Silvio Savarese; Caiming Xiong; Junnan Li; Zeyuan Chen; Ran Xu (2026).** *WALT: Web Agents that Learn Tools*. International Conference on Learning Representations (ICLR 2026), Conference / poster. [正式来源](https://proceedings.iclr.cc/paper_files/paper/2026/hash/5b175f9e93873e3a10a6ce43dbb82e05-Abstract-Conference.html)。

来源等级：**顶刊顶会优先**；对应 E230。 机构：Salesforce AI Research。 [实际核读版本](https://arxiv.org/html/2510.01524v1)。

版本/出处说明：正式引用为 ICLR 2026，Krithika Ramakrishnan 排在 Jing Gu 之前；实际核读版本为 2025 年 arXiv v1。

<a id="ref-r05"></a>

**[12] Yu Shang; Yu Li; Keyu Zhao; Likai Ma; Jiahe Liu; Fengli Xu; Yong Li (2025).** *AgentSquare: Automatic LLM Agent Search in Modular Design Space*. ICLR 2025, main conference. [正式来源](https://proceedings.iclr.cc/paper_files/paper/2025/hash/0ae94013da7cd459402fd77874e09ee3-Abstract-Conference.html)。

来源等级：**顶刊顶会优先**；对应 R05。 机构：Tsinghua University, Department of Electronic Engineering; Tsinghua Shenzhen International Graduate School。 [实际核读版本](https://arxiv.org/html/2410.06153v3)。 [机构/资格依据](https://proceedings.iclr.cc/paper_files/paper/2025/file/0ae94013da7cd459402fd77874e09ee3-Paper-Conference.pdf)。

<a id="ref-r21"></a>

**[13] Noah Shinn; Federico Cassano; Ashwin Gopinath; Karthik Narasimhan; Shunyu Yao (2023).** *Reflexion: language agents with verbal reinforcement learning*. NeurIPS 2023, main conference track; Advances in Neural Information Processing Systems 36. [正式来源](https://proceedings.neurips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html)。

来源等级：**顶刊顶会优先**；对应 R21。 机构：Northeastern University; Massachusetts Institute of Technology; Princeton University。 [实际核读版本](https://arxiv.org/pdf/2303.11366v4)。 [机构/资格依据](https://proceedings.neurips.cc/paper_files/paper/2023/file/1b44b878bb782e6954cd888628510e90-Paper-Conference.pdf)。

版本/出处说明：NeurIPS 正式版为五位作者；所读 arXiv v4 为六位作者，另有 Edward Berman。两版作者表不混合。

<a id="ref-e272"></a>

**[14] Zora Zhiruo Wang; Jiayuan Mao; Daniel Fried; Graham Neubig (2025a).** *Agent Workflow Memory*. Proceedings of the 42nd International Conference on Machine Learning (ICML 2025), PMLR 267:63897–63911. [正式来源](https://proceedings.mlr.press/v267/wang25bx.html)。

来源等级：**顶刊顶会优先**；对应 E272。 机构：Carnegie Mellon University; Massachusetts Institute of Technology。 [实际核读版本](https://arxiv.org/html/2409.07429v1)。

<a id="ref-e229"></a>

**[15] Zora Zhiruo Wang; Apurva Gandhi; Graham Neubig; Daniel Fried (2025b).** *Inducing Programmatic Skills for Agentic Tasks*. Conference on Language Modeling (COLM 2025), main conference. [正式来源](https://openreview.net/forum?id=lsAY6fWsog)。

来源等级：**顶刊顶会优先**；对应 E229。 机构：Carnegie Mellon University。 [实际核读版本](https://arxiv.org/html/2504.06821v2)。 [机构/资格依据](https://openreview.net/pdf?id=lsAY6fWsog)。

<a id="ref-r12"></a>

**[16] Hao Wen; Yuanchun Li; Guohong Liu; Shanhui Zhao; Tao Yu; Toby Jia-Jun Li; Shiqi Jiang; Yunhao Liu; Yaqin Zhang; Yunxin Liu (2024).** *AutoDroid: LLM-powered Task Automation in Android*. Proceedings of the 30th Annual International Conference on Mobile Computing and Networking (ACM MobiCom 2024), research paper. [正式来源](https://doi.org/10.1145/3636534.3649379)。

来源等级：**顶刊顶会优先**；对应 R12。 机构：Tsinghua University AIR / Global Innovation Exchange / Department of Automation; Shanghai Artificial Intelligence Laboratory; University of Notre Dame; Microsoft Research。 [实际核读版本](https://arxiv.org/html/2308.15272v4)。

<a id="ref-e227"></a>

**[17] Hao Wen; Shizuo Tian; Borislav Pavlov; Wenjie Du; Yixuan Li; Ge Chang; Shanhui Zhao; Jiacheng Liu; Yunxin Liu; Ya-Qin Zhang; Yuanchun Li (2025).** *AutoDroid-V2: Boosting SLM-based GUI Agents via Code Generation*. Proceedings of the 23rd Annual International Conference on Mobile Systems, Applications and Services (ACM MobiSys 2025), research paper. [正式来源](https://doi.org/10.1145/3711875.3729134)。

来源等级：**顶刊顶会优先**；对应 E227。 机构：Institute for AI Industry Research (AIR), Tsinghua University; Shanghai Artificial Intelligence Laboratory; Beijing Academy of Artificial Intelligence (BAAI)。 [实际核读版本](https://arxiv.org/html/2412.18116v3)。

<a id="ref-r03"></a>

**[18] Mert Yuksekgonul; Federico Bianchi; Joseph Boen; Sheng Liu; Pan Lu; Zhi Huang; Carlos Guestrin; James Zou (2025).** *Optimizing generative AI by backpropagating language model feedback*. Nature 639:609–616, Article; published 19 March 2025. [正式来源](https://doi.org/10.1038/s41586-025-08661-4)。

来源等级：**顶刊顶会优先**；对应 R03。 机构：Stanford University, Department of Computer Science; Stanford University, Department of Biomedical Data Science; Chan Zuckerberg Biohub。 [实际核读版本](https://arxiv.org/html/2406.07496v1)。 [机构/资格依据](https://www.nature.com/articles/s41586-025-08661-4)。

版本/出处说明：TextGrad 的 Nature 正式版改题，并新增作者 Pan Lu；机制核读仍为 arXiv v1。

<a id="ref-e317"></a>

**[19] Shaokun Zhang; Jieyu Zhang; Jiale Liu; Linxin Song; Chi Wang; Ranjay Krishna; Qingyun Wu (2024).** *Offline Training of Language Model Agents with Functions as Learnable Weights*. ICML 2024, main conference; Proceedings of Machine Learning Research 235:60315–60335. [正式来源](https://proceedings.mlr.press/v235/zhang24cd.html)。

来源等级：**顶刊顶会优先**；对应 E317。 机构：Pennsylvania State University; University of Washington; University of Southern California; Microsoft Research。 [实际核读版本](https://arxiv.org/html/2402.11359v4)。 [机构/资格依据](https://raw.githubusercontent.com/mlresearch/v235/main/assets/zhang24cd/zhang24cd.pdf)。

<a id="ref-r04"></a>

**[20] Jiayi Zhang; Jinyu Xiang; Zhaoyang Yu; Fengwei Teng; Xiong-Hui Chen; Jiaqi Chen; Mingchen Zhuge; Xin Cheng; Sirui Hong; Jinlin Wang; Bingnan Zheng; Bang Liu; Yuyu Luo; Chenglin Wu (2025a).** *AFlow: Automating Agentic Workflow Generation*. ICLR 2025, main conference. [正式来源](https://proceedings.iclr.cc/paper_files/paper/2025/file/5492ecbce4439401798dcd2c90be94cd-Paper-Conference.pdf)。

来源等级：**顶刊顶会优先**；对应 R04。 机构：DeepWisdom; Hong Kong University of Science and Technology (Guangzhou); Renmin University of China; Nanjing University; Fudan University; King Abdullah University of Science and Technology; Université de Montréal and Mila; Hong Kong University of Science and Technology。 [实际核读版本](https://arxiv.org/html/2410.10762v4)。 [机构/资格依据](https://proceedings.iclr.cc/paper_files/paper/2025/file/5492ecbce4439401798dcd2c90be94cd-Paper-Conference.pdf)。

<a id="ref-r09"></a>

**[21] Chi Zhang; Zhao Yang; Jiaxuan Liu; Yanda Li; Yucheng Han; Xin Chen; Zebiao Huang; Bin Fu; Gang Yu (2025b).** *AppAgent: Multimodal Agents as Smartphone Users*. Proceedings of the 2025 CHI Conference on Human Factors in Computing Systems (ACM CHI 2025), research paper. [正式来源](https://doi.org/10.1145/3706598.3713600)。

来源等级：**顶刊顶会优先**；对应 R09。 机构：Westlake University; Tencent; Shanghai Supwisdom; University of Technology Sydney; Nanyang Technological University。 [实际核读版本](https://arxiv.org/html/2312.13771v3)。 [机构/资格依据](https://api.crossref.org/works/10.1145/3706598.3713600)。

版本/出处说明：CHI 正式版共九位作者，含 Yanda Li；所读 arXiv v3 共八位作者。正式书目信息和机构依据 ACM 存入 Crossref 的 DOI metadata。

<a id="ref-r19"></a>

**[22] Qizheng Zhang; Changran Hu; Shubhangi Upasani; Boyuan Ma; Fenglu Hong; Vamsidhar Kamanuru; Jay Rainton; Chen Wu; Mengmeng Ji; Hanchen Li; Urmish Thakker; James Zou; Kunle Olukotun (2026a).** *Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models*. ICLR 2026, main conference, poster. [正式来源](https://iclr.cc/virtual/2026/poster/10008343)。

来源等级：**顶刊顶会优先**；对应 R19。 机构：Stanford University; SambaNova Systems Inc.; University of California, Berkeley。 [实际核读版本](https://arxiv.org/pdf/2510.04618v3)。

<a id="ref-e306"></a>

**[23] Jenny Zhang; Shengran Hu; Cong Lu; Robert Lange; Jeff Clune (2026b).** *Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents*. ICLR 2026, main conference Poster. [正式来源](https://iclr.cc/virtual/2026/poster/10007327)。

来源等级：**顶刊顶会优先**；对应 E306。 机构：University of British Columbia; Vector Institute; Sakana AI; Canada CIFAR AI Chair。 [实际核读版本](https://arxiv.org/html/2505.22954v2)。

<a id="ref-e316"></a>

**[24] Haiteng Zhao; Chang Ma; Guoyin Wang; Jing Su; Lingpeng Kong; Jingjing Xu; Zhi-Hong Deng; Hongxia Yang (2024a).** *Empowering Large Language Model Agents through Action Learning*. Conference on Language Modeling (COLM 2024), main conference. [正式来源](https://openreview.net/forum?id=KqK5XcgEhR)。

来源等级：**顶刊顶会优先**；对应 E316。 机构：Peking University; The University of Hong Kong; ByteDance。 [实际核读版本](https://arxiv.org/html/2402.15809v2)。

<a id="ref-r16"></a>

**[25] Andrew Zhao; Daniel Huang; Quentin Xu; Matthieu Lin; Yong-Jin Liu; Gao Huang (2024b).** *ExpeL: LLM Agents Are Experiential Learners*. AAAI 2024, main technical track: Natural Language Processing II; Proceedings 38(17):19632–19642. [正式来源](https://ojs.aaai.org/index.php/AAAI/article/view/29936)。

来源等级：**顶刊顶会优先**；对应 R16。 机构：Tsinghua University, BNRist, Department of Automation; Tsinghua University, BNRist, Department of Computer Science。 [实际核读版本](https://arxiv.org/pdf/2308.10144v3)。 [机构/资格依据](https://ojs.aaai.org/index.php/AAAI/article/view/29936)。

<a id="ref-r23"></a>

**[26] Andy Zhou; Kai Yan; Michal Shlapentokh-Rothman; Haohan Wang; Yu-Xiong Wang (2024).** *Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models*. ICML 2024, main conference; Proceedings of the 41st International Conference on Machine Learning, PMLR 235:62138–62160. [正式来源](https://proceedings.mlr.press/v235/zhou24r.html)。

来源等级：**顶刊顶会优先**；对应 R23。 机构：University of Illinois Urbana-Champaign; Lapis Labs。 [实际核读版本](https://arxiv.org/pdf/2310.04406v3)。

<a id="ref-r07"></a>

**[27] Qianshu Cai; Yonggang Zhang; Xianzhang Jia; Wei Xue; Jun Song; Xinmei Tian; Yike Guo (2026).** *MOSS: Self-Evolution through Source-Level Rewriting in Autonomous Agent Systems*. arXiv preprint（未核到正式主会/顶刊接收）. [预印本](https://arxiv.org/html/2605.22794v1)。

来源等级：**合格机构补充**；对应 R07。 机构：University of Science and Technology of China, MoE Key Laboratory of Brain-inspired Intelligent Perception and Cognition; Hong Kong University of Science and Technology; Hong Kong Baptist University。 [实际核读版本](https://arxiv.org/html/2605.22794v1)。

<a id="ref-r24"></a>

**[28] Zhengyu Chen; Teng Xiao; Huaisheng Zhu; Yige Yuan; Luan Zhang; Jingang Wang (2026).** *Co-Harness: Co-Evolving Harnesses and Model Weights for LLM Agents*. arXiv preprint (formal peer-reviewed venue not verified). [预印本](https://arxiv.org/pdf/2607.22688v1)。

来源等级：**合格机构补充**；对应 R24。 机构：Meituan; Allen Institute for AI; Independent。 [实际核读版本](https://arxiv.org/pdf/2607.22688v1)。

<a id="ref-e271"></a>

**[29] Zixi Huang; Xiheng Wang; Andrew Wang; William Jurayj; Bernal Jiménez Gutiérrez; Daniel Khashabi; Nicholas Andrews (2026).** *Better, Faster, Stronger: Programmatic Skill Learning Best Reduces Agent Cost*. arXiv preprint（未核到正式主会/顶刊接收）. [预印本](https://arxiv.org/html/2608.11338v1)。

来源等级：**合格机构补充**；对应 E271。 机构：Johns Hopkins University。 [实际核读版本](https://arxiv.org/html/2608.11338v1)。

<a id="ref-r10"></a>

**[30] Wenjia Jiang; Yangyang Zhuang; Chenxi Song; Xu Yang; Joey Tianyi Zhou; Chi Zhang (2025).** *AppAgentX: Evolving GUI Agents as Proficient Smartphone Users*. arXiv preprint arXiv:2503.02268 (formal venue not verified). [预印本](https://arxiv.org/html/2503.02268v3)。

来源等级：**合格机构补充**；对应 R10。 机构：Westlake University AGI Lab; Henan University; Southeast University; A*STAR Institute of High Performance Computing (IHPC); A*STAR Centre for Frontier AI Research (CFAR)。 [实际核读版本](https://arxiv.org/html/2503.02268v3)。 [机构/资格依据](https://appagentx.github.io/)。

<a id="ref-e305"></a>

**[31] Lekang Jiang; Bohan Tang; Stephan Goetz; Yiwen Guo (2026).** *ADIAS: Automated Design of Interactive Agentic Systems*. arXiv preprint（未核到正式主会/顶刊接收）. [预印本](https://arxiv.org/pdf/2608.06410v1)。

来源等级：**合格机构补充**；对应 E305。 机构：University of Cambridge（Lekang Jiang, Stephan Goetz）; LIGHTSPEED / Tencent（Bohan Tang）; Independent Researcher（Yiwen Guo）。 [实际核读版本](https://arxiv.org/pdf/2608.06410v1)。

<a id="ref-e319"></a>

**[32] Yoonho Lee; Roshen Nair; Qizheng Zhang; Kangwook Lee; Omar Khattab; Chelsea Finn (2026).** *Meta-Harness: End-to-End Optimization of Model Harnesses*. arXiv preprint；作者项目页自报 COLM 2026，官方接收状态本轮未核实. [预印本](https://arxiv.org/html/2603.28052v1)。

来源等级：**合格机构补充**；对应 E319。 机构：Stanford University; KRAFTON; Massachusetts Institute of Technology。 [实际核读版本](https://arxiv.org/html/2603.28052v1)。

版本/出处说明：作者项目页自报 COLM 2026，本轮未独立核实官方录用；按 Stanford/MIT 预印本保留。

<a id="ref-e320"></a>

**[33] Jiahang Lin; Shichun Liu; Chengjun Pan; Lizhi Lin; Shihan Dou; Xuanjing Huang; Hang Yan; Zhenhua Han; Tao Gui (2026).** *Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses*. arXiv preprint（未核到正式主会/顶刊接收）. [预印本](https://arxiv.org/html/2604.25850v1)。

来源等级：**合格机构补充**；对应 E320。 机构：Fudan University; Peking University; Shanghai Qiji Zhifeng Technology Co., Ltd.。 [实际核读版本](https://arxiv.org/html/2604.25850v1)。

版本/出处说明：作者表固定到实际核读的 v1；不混用后续版本新增作者。

<a id="ref-r06"></a>

**[34] Xinghua Lou; Miguel Lázaro-Gredilla; Antoine Dedieu; Carter Wendelken; Wolfgang Lehrach; Kevin P. Murphy (2026).** *AutoHarness: improving LLM agents by automatically synthesizing a code harness*. ICLR 2026 Workshop on Recursive Self-Improvement, Poster（不是 ICLR 主会）. [正式来源](https://recursive-workshop.github.io/papers.html)。

来源等级：**合格机构补充**；对应 R06。 机构：Google DeepMind。 [实际核读版本](https://arxiv.org/html/2603.03329v1)。

版本/出处说明：官方名单确认的是 ICLR 2026 Workshop on Recursive Self-Improvement poster，非 ICLR 主会。

<a id="ref-e318"></a>

**[35] Yixin Ou; Wangchunshu Zhou; Shengwei Ding; Long Li; Jialong Wu; Tiannan Wang; Jiamin Chen; Shuai Wang; Xiaohua Xu; Ningyu Zhang; Huajun Chen; Yuchen Eleanor Jiang (2025).** *Symbolic learning enables self-evolving agents*. AI Open, Volume 6, pages 314–322, full-length article（正式发表；不据此自动认定为顶刊）. [正式来源](https://doi.org/10.1016/j.aiopen.2025.11.004)。

来源等级：**合格机构补充**；对应 E318。 机构：Zhejiang University（SSRN: Yixin Ou, Ningyu Zhang, Huajun Chen）; University of Copenhagen（SSRN: Shengwei Ding）; Alibaba Group（SSRN: Jialong Wu）; AIWaves Inc.（所读 arXiv v1 总署名）。 [实际核读版本](https://arxiv.org/html/2406.18532v1)。 [机构/资格依据](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5379114)。

版本/出处说明：正式 AI Open 版为 Ou 第一作者、Zhou 第二作者；实际核读 arXiv v1 为 Zhou 第一作者。机构资格依据 SSRN 作者提交页，不把 AI Open 自动视为顶刊。

<a id="ref-e311"></a>

**[36] Wenbo Pan; Shujie Liu; Chin-Yew Lin; Jingying Zeng; Xianfeng Tang; Xiangyang Zhou; Yan Lu; Xiaohua Jia (2026).** *Evolving Agents in the Dark: Retrospective Harness Optimization via Self-Preference*. arXiv preprint（未核到正式主会/顶刊接收）. [预印本](https://arxiv.org/html/2606.05922v3)。

来源等级：**合格机构补充**；对应 E311。 机构：City University of Hong Kong; Microsoft Research Asia。 [实际核读版本](https://arxiv.org/html/2606.05922v3)。

<a id="ref-e309"></a>

**[37] Sungho Park; Wonjoong Kim; Rongyuan Tan; Jue Zhang; Wook-Shin Han; Pengfei Gao; Chanyoung Park; Yongqiang Yao; Rao Fu; Elsie Nallipogu; Qingwei Lin; Saravan Rajmohan; Dongmei Zhang (2026).** *AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces*. arXiv preprint（未核到正式主会/顶刊接收）. [预印本](https://arxiv.org/html/2608.23041v1)。

来源等级：**合格机构补充**；对应 E309。 机构：POSTECH; KAIST; Southern University of Science and Technology; Microsoft。 [实际核读版本](https://arxiv.org/html/2608.23041v1)。

<a id="ref-r20"></a>

**[38] Pranav Putta; Edmund Mills; Naman Garg; Sumeet Motwani; Chelsea Finn; Divyansh Garg; Rafael Rafailov (2024).** *Agent Q: Advanced Reasoning and Learning for Autonomous AI Agents*. arXiv preprint (formal peer-reviewed venue not verified). [预印本](https://arxiv.org/pdf/2408.07199v1)。

来源等级：**合格机构补充**；对应 R20。 机构：The AGI Company (MultiOn); Stanford University。 [实际核读版本](https://arxiv.org/pdf/2408.07199v1)。

<a id="ref-e314"></a>

**[39] Shuai Shao; Kangning Zhang; Qingyao Li; Shijian Wang; Hao Wang; Wenxiang Jiao; Yuan Lu; Yi Guo; Weiwen Liu; Weinan Zhang (2026).** *Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories*. arXiv preprint (formal peer-reviewed venue not verified). [预印本](https://arxiv.org/pdf/2608.02276v1)。

来源等级：**合格机构补充**；对应 E314。 机构：Shanghai Jiao Tong University; Southeast University; Xiaohongshu Inc.。 [实际核读版本](https://arxiv.org/pdf/2608.02276v1)。 [机构/资格依据](https://arxiv.org/html/2608.02276v1)。

<a id="ref-r26"></a>

**[40] Su Wang; Pin Qian; Yifan Lin; Jingzhou Xu; Yihang Chen; Xiaochong Jiang; Lifei Liu; Haoran Yu (2026).** *Phantom Guardrails: When Self-Improving Agent Harnesses Fix Failures That Never Happened*. arXiv preprint (formal peer-reviewed venue not verified). [预印本](https://arxiv.org/pdf/2607.13083v1)。

来源等级：**合格机构补充**；对应 R26。 机构：Carnegie Mellon University (paper-listed; all three corresponding email addresses use alumni.cmu.edu); Corespeed Inc.; Georgia Institute of Technology (paper-listed for Yihang Chen); Independent Researcher。 [实际核读版本](https://arxiv.org/pdf/2607.13083v1)。 [机构/资格依据](https://arxiv.org/html/2607.13083v1)。

版本/出处说明：本次来源资格依据 Yihang Chen 在论文中的 Georgia Tech 署名及 gatech.edu 邮箱；另三位作者的 CMU alumni 邮箱不作为当前在职机构证明。阅读深度仍为摘要级 B。

<a id="ref-e322"></a>

**[41] Rong Wu; Xiaoman Wang; Jianbiao Mei; Pinlong Cai; Daocheng Fu; Cheng Yang; Licheng Wen; Xuemeng Yang; Yufan Shen; Yuxin Wang; Botian Shi (2025).** *EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle*. arXiv preprint; authors report ICML 2026 acceptance, independently unconfirmed. [预印本](https://arxiv.org/pdf/2510.16079v3)。

来源等级：**合格机构补充**；对应 E322。 机构：Zhejiang University; Shanghai Artificial Intelligence Laboratory; East China Normal University; Fudan University; Central South University; Shanghai Innovation Institute; Shanghai Jiao Tong University; University of Science and Technology of China。 [实际核读版本](https://arxiv.org/pdf/2510.16079v3)。

版本/出处说明：作者项目仓库自报 ICML 2026，本轮未独立核实官方录用；按机构预印本保留，引用年份取首次发布的 2025 年。

<a id="ref-e313"></a>

**[42] Chenyang Yang; Xinran Zhao; Tongshuang Wu; Christian Kästner (2026).** *Better Harnesses, Smaller Models: Building 90% Cheaper Agents via Automated Harness Adaptation*. arXiv preprint（未核到正式主会/顶刊接收）. [预印本](https://arxiv.org/html/2607.08938v1)。

来源等级：**合格机构补充**；对应 E313。 机构：Carnegie Mellon University。 [实际核读版本](https://arxiv.org/html/2607.08938v1)。

<a id="ref-e323"></a>

**[43] Qinyuan Ye; Yu Li; Yada Pruksachatkun; Jiaxin Zhang; Chien-Sheng Wu (2026).** *On the Fragility of Self-Improving Agents: Variance, Task Order, and Underspecification*. arXiv preprint (formal peer-reviewed venue not verified). [预印本](https://arxiv.org/pdf/2608.18066v2)。

来源等级：**合格机构补充**；对应 E323。 机构：Salesforce AI Research。 [实际核读版本](https://arxiv.org/pdf/2608.18066v2)。 [机构/资格依据](https://arxiv.org/html/2608.18066v2)。

<a id="ref-r18"></a>

**[44] Yunpeng Zhai; Shuchang Tao; Cheng Chen; Anni Zou; Ziqian Chen; Qingxu Fu; Shinji Mai; Li Yu; Jiaji Deng; Zouying Cao; Zhaoyang Liu; Bolin Ding; Jingren Zhou (2025).** *AgentEvolver: Towards Efficient Self-Evolving Agent System*. arXiv preprint (formal peer-reviewed venue not verified). [预印本](https://arxiv.org/pdf/2511.10395v1)。

来源等级：**合格机构补充**；对应 R18。 机构：Tongyi Lab, Alibaba Group。 [实际核读版本](https://arxiv.org/pdf/2511.10395v1)。 [机构/资格依据](https://arxiv.org/html/2511.10395v1)。

<a id="ref-e310"></a>

**[45] Hangfan Zhang; Shao Zhang; Kangcong Li; Chen Zhang; Yang Chen; Yiqun Zhang; Lei Bai; Shuyue Hu (2026c).** *Self-Harness: Harnesses That Improve Themselves*. arXiv preprint（未核到正式主会/顶刊接收）. [预印本](https://arxiv.org/html/2606.09498v3)。

来源等级：**合格机构补充**；对应 E310。 机构：Shanghai Artificial Intelligence Laboratory。 [实际核读版本](https://arxiv.org/html/2606.09498v3)。

<a id="ref-e308"></a>

**[46] Boyuan Zheng; Michael Y. Fatemi; Xiaolong Jin; Zora Zhiruo Wang; Apurva Gandhi; Yueqi Song; Yu Gu; Jayanth Srinivasa; Gaowen Liu; Graham Neubig; Yu Su (2025).** *SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills*. arXiv preprint arXiv:2504.07079 (formal venue not verified). [预印本](https://arxiv.org/html/2504.07079v1)。

来源等级：**合格机构补充**；对应 E308。 机构：The Ohio State University; University of Virginia; Purdue University; Carnegie Mellon University; Cisco Research。 [实际核读版本](https://arxiv.org/html/2504.07079v1)。 [机构/资格依据](https://osu-nlp-group.github.io/SkillWeaver/)。

<a id="ref-e307"></a>

**[47] Hongbin Zhong; Fazle Faisal; Luis França; Tanakorn Leesatapornwongsa; Adriana Szekeres; Kexin Rong; Suman Nath (2026).** *ActionEngine: From Reactive to Programmatic Web Agents via State Machine Memory*. arXiv preprint arXiv:2602.20502 (formal venue not verified). [预印本](https://arxiv.org/html/2602.20502v2)。

来源等级：**合格机构补充**；对应 E307。 机构：Georgia Institute of Technology; Microsoft。 [实际核读版本](https://arxiv.org/html/2602.20502v2)。

<a id="ref-r17"></a>

**[48] Huichi Zhou; Yihang Chen; Siyuan Guo; Xue Yan; Kin Hei Lee; Zihan Wang; Ka Yiu Lee; Guchun Zhang; Kun Shao; Linyi Yang; Jun Wang (2025).** *Memento: Fine-tuning LLM Agents without Fine-tuning LLMs*. arXiv preprint (formal peer-reviewed venue not verified). [预印本](https://arxiv.org/pdf/2508.16153v2)。

来源等级：**合格机构补充**；对应 R17。 机构：AI Centre, University College London; Huawei Noah’s Ark Lab, UK; Jilin University; Institute of Automation, Chinese Academy of Sciences。 [实际核读版本](https://arxiv.org/pdf/2508.16153v2)。 [机构/资格依据](https://arxiv.org/html/2508.16153v2)。
