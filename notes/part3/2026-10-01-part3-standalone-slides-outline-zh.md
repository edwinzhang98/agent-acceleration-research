# 第三部分独立 slides 大纲：我们要做什么

2026-10-01 · 讨论稿，仅规划，不生成或改动 slides 文件。

独立成篇，面向资深 ML 背景听众。正文严格为 **12 页**：问题定义 → 现有研究做到哪 → 我们准备做什么。第一、二部分 deck 作为补充背景。每页的“页面内容”是上屏正文，控制在250字的量以内；“依据与口径”供制作时核对，不上屏。附录保留逐篇条件与完整书目，表格和参考文献可按版面续页。

文中 Agent 指根据观察继续决策并调用工具完成任务的系统；留出任务指未参与学习或挑版本的最终评测任务；token 是模型处理文本的片段计数，不能直接换算成时间或费用。所有数字沿用指定文档，类别篇数仅按其中清单计数（calc.）。缺失与边界均限定为已核对材料，本文不作新颖性判断。

## 第 1 页　问题：同样的任务，在做对的前提下更快、更省

**一句话主张：** 在相同任务和可比权限下，先满足正确性与执行约束，再改善完成时间与费用。

**页面内容：**

- 时间、费用分别报：更快可能更贵，不能随意加成一分。
- 会学习的系统按一串任务算总账：执行、探索、学习、验证、维护各计一次，失败与回退也算。
- 用户等待、离线适配工期、计算资源占用分开记。
- 第一版固定模型权重，只改提示、记忆、工具和控制流程；这只是实验范围。

**参考文献：** [Kapoor, Sayash et al., 2025](#ref-ai-agents-that-matter)（TMLR 2025）；[Maxime Robeyns et al., 2025](#ref-a-self-improving-coding-agent)（ICLR 2025 自改进 workshop）；[Zixi Huang et al., 2026](#ref-better-faster-stronger-programmatic-skill-learning-best-reduces-agent-cost)（arXiv 预印本）。

**依据与口径：** [问题定义第一节](2026-09-30-agent-acceleration-problem-framing-zh.md#一-从完成任务定义加速)。

## 第 2 页　为什么难：五个相互牵连的挑战

**一句话主张：** 省掉一步计算或观察，既可能消除浪费，也可能把代价推到后面。

**页面内容：**

1. 瓶颈由整个执行过程决定：少调用不一定更快。
2. 哪些交互必要，常要做了才知道：少看可能误操作。
3. 看见慢或失败，不等于知道该改什么。
4. 经验要跨任务有效，也要便宜地使用和维护。
5. 证明节省本身也花钱：要检查做对了、旧能力没退步、总投入能收回。

**参考文献：** [Abhyankar, Reyna et al., 2026](#ref-osworld-human-benchmarking-the-efficiency-of-computer-use-agents)（MLSys 2026）；[Changle Qu et al., 2025](#ref-from-exploration-to-mastery-enabling-llms-to-master-tools-via-self-driven-interactions)（ICLR 2025 主会）；[Mengzhuo Chen et al., 2026](#ref-from-failed-trajectories-to-reliable-llm-agents-diagnosing-and-repairing-harness-flaws)（arXiv 预印本）；[Zijie Dai et al., 2026](#ref-metis-bridging-text-and-code-memory-for-self-evolving-agents)（arXiv 预印本）；[Harsh Trivedi et al., 2024](#ref-appworld-a-controllable-world-of-apps-and-people-for-benchmarking-interactive-coding-agents)（ACL 2024 主会）。

**依据与口径：** [问题定义第三节](2026-09-30-agent-acceleration-problem-framing-zh.md#三-通用挑战与持续改进带来的附加挑战)；五项是本项目综合，不是某一论文的统一分类。

## 第 3 页　加速与自改进：有交集，目标不同

**一句话主张：** 学习描述系统怎样更新，加速描述希望取得什么效果。

**页面内容：**

在已核对的178项Agent方法工作中：

| 运行时间是否主要目标 | 用学习机制 | 不用 |
|---|---:|---:|
| 是 | 16 | 30 |
| 否 | 88 | 44 |

- 学习机制包括经验复用、环境探索、持续改提示或工具等；不等于训练模型。
- “现有自改进都只看成功率”不成立：SICA选择时计质量、费用和实际经过的时间；SpeedRunner把技能归纳的模型服务费用分摊到执行账中。
- 这描述已收集文献；运行时间也不全是端到端时间。

**参考文献：** [Maxime Robeyns et al., 2025](#ref-a-self-improving-coding-agent)（ICLR 2025 自改进 workshop）；[Zixi Huang et al., 2026](#ref-better-faster-stronger-programmatic-skill-learning-best-reduces-agent-cost)（arXiv 预印本）。

**依据与口径：** [校准报告交集表与补读结果](2026-09-30-agent-literature-calibration-zh.md#加速与经验改进的交集)；统计日期2026-09-30，本项目对已核对一手材料的二次编码，不代表全领域比例。墙钟时间指从开始到结束实际经过的时间。

## 第 4 页　方向一已有进展：从轨迹改模型外部

**一句话主张：** 提示、记忆、工具和框架都能自动改进，但收益依赖反馈、任务和成本边界。

**页面内容：**

| 改什么／核对篇数 | 有效条件 | 共同问题 | 时间、费用 |
|---|---|---|---|
| 提示14 | 同类可评分任务 | 反馈能力；验证贵 | 多测搜索，部署常缺 |
| 记忆24 | 相关任务反复出现 | 错误传播；迁移失效 | 有增有减，建库常漏 |
| 技能工具21 | 可编程且可检查 | 验证误判；工具难用 | 有升有降，学习常漏 |
| 代码框架25 | 可批量评分 | 验证贵；挑选过拟合 | 少数报时费，离线多缺 |

篇数按分节清单计算；跨类重复，含另训辅助模型的边界对照，不能相加。

**参考文献：** [Krista Opsahl-Ong et al., 2024](#ref-optimizing-instructions-and-demonstrations-for-multi-stage-language-model-programs)（EMNLP 2024 主会）；[Lakshya A Agrawal et al., 2026](#ref-gepa-reflective-prompt-evolution-can-outperform-reinforcement-learning)（ICLR 2026 主会）；[Andrew Zhao et al., 2024](#ref-expel-llm-agents-are-experiential-learners)（AAAI 2024）；[Boyuan Zheng et al., 2025](#ref-skillweaver-web-agents-can-self-improve-by-discovering-and-honing-skills)（arXiv 预印本）；[Maxime Robeyns et al., 2025](#ref-a-self-improving-coding-agent)（ICLR 2025 自改进 workshop）。

**依据与口径：** [两方向文献第二节](2026-10-01-two-directions-literature-zh.md#2-方向一不训练模型改进模型外部的系统)。篇数为对该节明确列名逐篇计数（calc.），不是从代表引文数推算；各行“共同问题”均有多篇支持。

## 第 5 页　方向二已有进展：环境知识有不同形态

**一句话主张：** 学到页面、文字规则或行动后果，不等于已经拥有可靠的完整环境规则库。

**页面内容：**

| 保存什么／核对篇数 | 有效条件 | 共同问题 | 时间、费用 |
|---|---|---|---|
| 行动后果3 | 可观测状态 | 预测不可信 | 部分测，学习漏项 |
| 工具说明2 | 有真实返回 | 原信息不足 | 未测实耗 |
| 自拟练习7 | 可练可反馈 | 裁判误判 | 部分测，学习常漏 |
| 页面地点4 | 可匹配结构 | 受观察形式限制 | 部分测，范围不同 |
| 文字事实6 | 相关且会取用 | 噪声与读取负担 | 有变慢的结果 |
| 规则判分1+2 | 可查终态 | 不报错不等于对 | 检查器与执行分开 |

末行是核心1篇、对照2篇；各类重叠，含训练边界。

**参考文献：** [Hyungjoo Chae et al., 2025](#ref-web-agents-with-world-models-learning-and-leveraging-environment-dynamics-in-web-navigation)（ICLR 2025 主会）；[Xuan Zhang et al., 2026](#ref-self-evolving-world-models-for-llm-agent-planning)（arXiv 预印本；Findings声称未正式核实）；[Changle Qu et al., 2025](#ref-from-exploration-to-mastery-enabling-llms-to-master-tools-via-self-driven-interactions)（ICLR 2025 主会）；[Hongjin Qian et al., 2025](#ref-metaagent-toward-self-evolving-agent-via-tool-meta-learning)（arXiv 预印本）；[Boyuan Zheng et al., 2025](#ref-skillweaver-web-agents-can-self-improve-by-discovering-and-honing-skills)（arXiv 预印本）；[Guanzhi Wang et al., 2024](#ref-voyager-an-open-ended-embodied-agent-with-large-language-models)（TMLR 2024；ICLR 2025 Journal Track）；[Sunjae Lee et al., 2024](#ref-mobilegpt-augmenting-llm-with-human-like-app-memory-for-mobile-task-automation)（ACM MobiCom 2024）；[Junyeong Park et al., 2025](#ref-mrsteve-instruction-following-agents-in-minecraft-with-what-where-when-memory)（ICLR 2025 主会）；[Zijie Dai et al., 2026](#ref-metis-bridging-text-and-code-memory-for-self-evolving-agents)（arXiv 预印本）；[Genglin Liu et al., 2025](#ref-webcoach-self-evolving-web-agents-with-cross-session-memory-guidance)（ICLR 2026 MemAgents workshop；元数据年份2025）；[Harsh Trivedi et al., 2024](#ref-appworld-a-controllable-world-of-apps-and-people-for-benchmarking-interactive-coding-agents)（ACL 2024 主会）。

**依据与口径：** [两方向文献第三节](2026-10-01-two-directions-literature-zh.md#3-方向二从交互中保存环境知识)。篇数为分节清单计数（calc.）；规则判分是评测基础设施。最后一行的共同问题结合该节引用的技能验证失败实例，不把它计成新增核心工作。

## 第 6 页　和我们方向最相近的工作：已经能做什么，还要在哪些条件下验证

**一句话主张：** 先保留近邻已有的功能，再检验新增决策能否带来净收益。

**页面内容：**

| 工作 | 做到什么 | 条件 | 未证明什么 |
|---|---|---|---|
| ActionEngine | 图转程序 | 模板预热、关闭修补 | 完整维护收益 |
| WALT | 探索造工具 | 网站内验证 | 部署后修补 |
| SpeedRunner | 改技能库 | 游戏任务流 | 独立验收稳定性 |
| Metis | 文字转代码 | 已见应用留出题 | 完整费用收益 |
| HarnessFix | 定位并修补 | 可回归验证 | 部署时费收益 |
| SKILL.nb | 检查后复用 | 重复网页、版本变化 | 时间费用净收益 |

已有自动循环、留出收益和局部节省；局部检查不保证任务正确，环境知识的适用范围与全成本长期收益仍须分别验证。

**参考文献：** [Hongbin Zhong et al., 2026](#ref-actionengine-from-reactive-to-programmatic-web-agents-via-state-machine-memory)（arXiv 预印本）；[Viraj Prabhu et al., 2026](#ref-walt-web-agents-that-learn-tools)（ICLR 2026 主会）；[Zixi Huang et al., 2026](#ref-better-faster-stronger-programmatic-skill-learning-best-reduces-agent-cost)（arXiv 预印本）；[Zijie Dai et al., 2026](#ref-metis-bridging-text-and-code-memory-for-self-evolving-agents)（arXiv 预印本）；[Mengzhuo Chen et al., 2026](#ref-from-failed-trajectories-to-reliable-llm-agents-diagnosing-and-repairing-harness-flaws)（arXiv 预印本）；[Amine El Hattami et al., 2026](#ref-skill-nb-selective-formalization-and-gated-execution-for-durable-agent-workflows)（ICML 2026 FAGEN workshop）。

**依据与口径：** [两方向文献第四、五节](2026-10-01-two-directions-literature-zh.md#4-和我们方向最相近的工作)，以及[校准报告补读结果](2026-09-30-agent-literature-calibration-zh.md#补读改变了哪些判断)。WALT正式版已有工具构建费用及简化回本估计；SpeedRunner已有执行者与技能归纳者摊销账，均不能概括成“未算学习成本”。“留出题”指未用于学习或挑版本的最终评测题；“回归验证”指检查原本会做的题是否退步。

## 第 7 页　我们准备做什么：两个可以否定的研究问题

**一句话主张：** 把“自动改进”和“学环境”收窄到具体的选择与验证决策。

**页面内容：**

- 方向一：同样轨迹和改进预算下，按可避免的耗时、费用选改哪里，是否优于按失败次数或任务得分选？要包括成功但浪费的轨迹，并比简单的“发生频次×损失”排序。
- 方向二：经历有限、环境会变时，怎样用最少新增观察，判断已学操作是否仍适用？决定直接复用、先检查、局部修复或恢复逐步执行。
- 两者关系：方向一发现并实施有价值的修改；方向二补足其环境证据。先分开测，不要求两者同时提出新算法。

**参考文献：** [Mengzhuo Chen et al., 2026](#ref-from-failed-trajectories-to-reliable-llm-agents-diagnosing-and-repairing-harness-flaws)（arXiv 预印本）；[Viraj Prabhu et al., 2026](#ref-walt-web-agents-that-learn-tools)（ICLR 2026 主会）；[Zijie Dai et al., 2026](#ref-metis-bridging-text-and-code-memory-for-self-evolving-agents)（arXiv 预印本）；[Amine El Hattami et al., 2026](#ref-skill-nb-selective-formalization-and-gated-execution-for-durable-agent-workflows)（ICML 2026 FAGEN workshop）。

**依据与口径：** [问题定义第四节](2026-09-30-agent-acceleration-problem-framing-zh.md#四-我们已有的两个方向怎样进入这个框架)；两项是待验证假设，不是已取得的结果。

## 第 8 页　哪些经验写成代码，哪些保留模型判断

**一句话主张：** 能明确检查的稳定操作可固化；需要语义和上下文判断的部分继续交给模型。

**页面内容：**

| 经验性质 | 第一版处理 |
|---|---|
| 字段依赖、算术、格式、明确前提、稳定点击序列 | 参数化代码；执行前检查适用条件 |
| 票据归类、费用是否合理、信息不足是否问人 | 文字规则与证据，保留模型判断 |
| 后果尚不清楚的不可撤回操作 | 不据单条轨迹自动固化 |

- 用真实执行证据决定固化、修复或退回；次数多本身不证明安全。
- 文字会有读取负担，代码也会失效；哪种划算需要比较，不能断言只有代码才省。

**参考文献：** [Laizhen Li et al., 2026](#ref-grow-the-harness-not-the-context-from-strategy-free-scaffolds-to-reusable-specialist-agents)（arXiv 预印本）；[Zijie Dai et al., 2026](#ref-metis-bridging-text-and-code-memory-for-self-evolving-agents)（arXiv 预印本）；[Amine El Hattami et al., 2026](#ref-skill-nb-selective-formalization-and-gated-execution-for-durable-agent-workflows)（ICML 2026 FAGEN workshop）；[Salma El Yadouni et al., 2026](#ref-tracecompiler-skill-guided-mining-and-compilation-of-llm-agent-traces-into-mostly-deterministic-workflows)（arXiv 预印本）。

**依据与口径：** [旧大纲第六页](2026-09-30-part3-slides-outline-zh.md)及两方向文献中的近邻证据；票据、费用与提交是我们的拟议工作流例子。

## 第 9 页　怎么判断做对了：固定答案库，独立裁判

**一句话主张：** 答案库由书面规则生成、经人确认，只负责判对错。

**页面内容：**

- 书面规则→生成用例与答案→人确认；分开发、筛选、最终测试三份，即训练／验证／测试。答案仅供裁判、不作经验输入；答案、规则、评分器均不可由改进循环改动。

| 文献中的判法 | 可靠性边界 |
|---|---|
| 标准答案、单测、终态检查 | 依赖规则覆盖；须查不应发生的变化 |
| 另一个模型裁判 | 会误判成功，要抽样人工复核 |
| 不报错、可编译 | 只证明能运行，不保证目标正确 |
| 模型自写测试 | 可漏边角或迎合测试，仍需独立答案 |

最终测试隔离到方案定稿后；规则变更须另立版本。

**参考文献：** [Harsh Trivedi et al., 2024](#ref-appworld-a-controllable-world-of-apps-and-people-for-benchmarking-interactive-coding-agents)（ACL 2024 主会）；[Siru Ouyang et al., 2026](#ref-reasoningbank-scaling-agent-self-evolving-with-reasoning-memory)（ICLR 2026 主会）；[Boyuan Zheng et al., 2025](#ref-skillweaver-web-agents-can-self-improve-by-discovering-and-honing-skills)（arXiv 预印本）；[Zhiling Yan et al., 2026](#ref-openskill-open-world-self-evolution-for-llm-agents)（EMNLP 2026 主会日程已列，论文集待刊）；[Hanrong Zhang et al., 2026](#ref-coevoskills-self-evolving-agent-skills-via-co-evolutionary-verification)（COLM 2026 主会）。

**依据与口径：** [旧大纲第七页](2026-09-30-part3-slides-outline-zh.md)。三份隔离按用户指定的训练／验证／测试含义执行；开发可读允许的判错反馈，标准答案不作为经验输入。

## 第 10 页　跟谁比：排除“看起来在学习”的三种假象

**一句话主张：** 必须胜过花同样多钱的不学习方案，并证明新增环节有贡献。

**页面内容：**

- 对照：原系统、文字经验、通用轨迹修改器、完整近邻、我们的方案；另给不学习的原系统同样总预算，多试几次或多走几步。
- 假象一：多花钱买来更高分。把探索、生成与验证也算入预算；方向二对齐历史信息与环境访问量。
- 假象二：反复挑版本把那批题做熟。最终测试不参与改进或筛选；另测真实填报及状态、规则变化。
- 假象三：复杂部件没有贡献。消融即关掉一个环节、其余不变；分别去掉分类选改法、成本排序、环境知识，多次重跑。

**参考文献：** [Sina Hajimiri et al., 2026](#ref-are-online-skill-and-memory-modules-always-worth-their-tokens-a-budget-constrained-study-of-web-agents)（EMNLP 2026 主会日程已列，论文集待刊）；[Michael Nguyen et al., 2026a](#ref-recursive-self-evolving-agents-via-held-out-selection)（arXiv 预印本）；[Yuxu Ge, 2026](#ref-coverage-not-credit-failure-credit-routing-of-zeroth-order-perturbation-budgets-does-not-improve-on-pool-sample-efficiency-for-llm-agents)（arXiv 预印本）。

**依据与口径：** [旧大纲第九页](2026-09-30-part3-slides-outline-zh.md)与问题定义第四节。等费用及等环境访问是拟议实验控制；现有token预算近似匹配实验不能写成已完成严格等美元比较。

## 第 11 页　怎么实验：四阶段推进，分别记账

**一句话主张：** 每阶段都检验是否值得继续，节省必须覆盖学习与维护。

**页面内容：**

1. 选可重置填报流程；造答案库、独立评分，测瓶颈；不可重跑或判对错就先停。
2. 分测两方向：读轨迹、提改动、重测；比较文字、代码与带条件知识。改动难通过或简单办法已够用就停。
3. 合并测连续任务和规则变化；稳定期内不能回本就停。
4. 可选Harness-R1式小编辑模型：仅当验证大模型提案过贵、且积累了已验证补丁时考虑训练；须比“大模型提案＋筛选”。

三本费用账：业务运行；学习、验收与维护；研究测评。每笔只计一次。报成功率、累计费用、延迟分布及回本；用户等待、离线工期、算力占用分报。

**参考文献：** [Shuai Shao et al., 2026](#ref-harness-r1-learning-to-edit-executable-runtime-harnesses-from-agent-failure-trajectories)（arXiv 预印本）；[Kapoor, Sayash et al., 2025](#ref-ai-agents-that-matter)（TMLR 2025）；[Zixi Huang et al., 2026](#ref-better-faster-stronger-programmatic-skill-learning-best-reduces-agent-cost)（arXiv 预印本）。

**依据与口径：** [旧大纲第十页](2026-09-30-part3-slides-outline-zh.md)与问题定义第一节。Harness-R1训练独立编辑模型，是固定全部权重主方案之外的可选分支；已有留出增益不能替代与大模型加筛选的比较。

## 第 12 页　资源：钱与算力

**一句话主张：** 先按阶段填预算，再决定规模；本页保留待填框。

**页面内容：**

| 资源 | 待填内容 |
|---|---|
| 钱 | 运行调用［待填］；探索、生成修改与验收［待填］；维护［待填］；研究测评［待填］ |
| 算力 | 可重置环境数量［待填］；并发与占用时长［待填］；若训练小编辑模型，硬件与训练时长［待填］ |

估算须与上一页费用口径对应；填写后分阶段申请，不预设未经测量的金额或机器数量。

**参考文献：** [Shuai Shao et al., 2026](#ref-harness-r1-learning-to-edit-executable-runtime-harnesses-from-agent-failure-trajectories)（arXiv 预印本）。

**依据与口径：** [旧大纲资源页](2026-09-30-part3-slides-outline-zh.md)及用户要求；此页是资源规划，文献只说明可选训练分支。

## 附录　逐篇总表摘录（每篇一行）

**一句话主张：** 同一方法的效果、比较条件和成本边界必须一起读，不能拼接不同论文的最好数字。

**页面内容：** 选取正文近邻及表示选择所用的代表工作；保留一篇一行，制作时按版面续页。本表不是全库排名，数字都是论文报告，并非我们的复现。

| 工作 | 保存或修改什么；怎么验收 | 条件 | 效果与时间、费用范围 | 尚未支持的结论 |
|---|---|---|---|---|
| ActionEngine | 网页状态—操作图转程序；基准评分并人工复核失败 | WebArena，Claude Opus 4.6；按模板预热，关闭在线修补 | 每任务27秒对87秒、$0.05对$0.40，相对Claude Code；未含探索和预热 | 探索回本估计漏预热；未证明未见模板及完整维护收益 |
| WALT | 探索后造带输入约束工具；测试通过才开放 | 网页任务，GPT-5规划、GPT-5-mini执行；解析器与检查器同时改变 | 读到的早期版本报告步骤；校准补读正式版已报告构建成本与简化回本 | 不能把整套收益归给造工具；部署后修补仍待研究 |
| SpeedRunner | 从执行反馈增删改代码技能；无独立重放验收 | ScienceWorld、BabyAI、Crafter；gpt-5.4-mini；在线后留出测试 | 校准确认API账含执行者及摊销的归纳者；原文某图token／美元口径冲突，不引用倍数 | 在线学习不稳定；未证明长期维护后净收益 |
| Metis | 环境事实留文字，重复计划转代码；准入检查依赖与编译 | AppWorld，GPT-4o执行、Sonnet 4.6整理；训练后冻结记忆测已见应用内留出题 | 正式划分每题执行token 112.6K→97.4K；未含管理者与检索，未测执行时间或费用 | 构建费不含轨迹生成；未测未见应用；编译通过不等于任务正确 |
| HarnessFix | 轨迹定位故障及实现位置，局部修补；验证集检查目标与退化 | GPT-5 mini；GAIA、SWE-bench Verified、AppWorld、Terminal-Bench；三次运行均值 | 完成率增6.3–18.4个百分点；AppWorld离线修补37.2M tokens；部署时费未报 | 不能用离线token代替部署提速或回本；验收阈值未记录 |
| MobileGPT | 保存页面—子任务图及动作路径；部分路径经人工修复 | 换参数的第二条指令；与同提示Derive-only比；按应用等权平均 | 暖启动延迟降62.5%、费用降68.8%；含人工修复，不能套给全自主学习 | 依赖文字界面结构；暖路径复用不等于新规则泛化 |
| SKILL.nb | 文字、代码、前后检查及版本维护；失效时局部退回 | WebArena-Verified，gpt-5.3-codex；推理强度不同；含GitLab版本变化测试 | 单轮成功率53.7%；内部维护更新36k tokens/成功任务，是否含执行不清；未量美元和时间 | 已有选择性固化与维护；仍依赖可靠检查、元数据和重复结构 |
| Growing Harness | 函数级失败定位，共享执行代码；独立验收集防退化 | BrowseComp-Plus、WebArena-Verified及三个部署模型 | 部署推理费用降74.4–98.6%，不含离线优化者／评估者；六组中一组成功率低0.7个百分点 | 未给全成本回本；不能写成所有条件严格保质量 |

**参考文献：** [Hongbin Zhong et al., 2026](#ref-actionengine-from-reactive-to-programmatic-web-agents-via-state-machine-memory)（arXiv 预印本）；[Viraj Prabhu et al., 2026](#ref-walt-web-agents-that-learn-tools)（ICLR 2026 主会）；[Zixi Huang et al., 2026](#ref-better-faster-stronger-programmatic-skill-learning-best-reduces-agent-cost)（arXiv 预印本）；[Zijie Dai et al., 2026](#ref-metis-bridging-text-and-code-memory-for-self-evolving-agents)（arXiv 预印本）；[Mengzhuo Chen et al., 2026](#ref-from-failed-trajectories-to-reliable-llm-agents-diagnosing-and-repairing-harness-flaws)（arXiv 预印本）；[Sunjae Lee et al., 2024](#ref-mobilegpt-augmenting-llm-with-human-like-app-memory-for-mobile-task-automation)（ACM MobiCom 2024）；[Amine El Hattami et al., 2026](#ref-skill-nb-selective-formalization-and-gated-execution-for-durable-agent-workflows)（ICML 2026 FAGEN workshop）；[Laizhen Li et al., 2026](#ref-grow-the-harness-not-the-context-from-strategy-free-scaffolds-to-reusable-specialist-agents)（arXiv 预印本）。

**依据与口径：** [两方向文献逐篇总表](2026-10-01-two-directions-literature-zh.md#6-附表逐篇证据与测量边界)与[校准报告补读结果](2026-09-30-agent-literature-calibration-zh.md#补读改变了哪些判断)。WALT的“早期版本未量化”与正式版的构建费用报告按版本分开；SpeedRunner的部分学习摊销不扩成全部学习、验证、维护成本。数字出处、所读版本和日期见下列完整书目，均为一手论文报告。

## References

正文与附录实际引用的工作才列在这里。正式发表信息和证据库实际阅读版本分开保留；缺字段标“未记录”，不根据年份或链接推测。书目信息来自证据库（仓库外，见 [research/2026-09-30-framing-ledger.md](../../research/2026-09-30-framing-ledger.md) 的说明）的已核对记录。校准报告补读的正式版范围已在对应页面说明，不将初读版的材料缺口外推到全部版本。

<a id="ref-osworld-human-benchmarking-the-efficiency-of-computer-use-agents"></a>

- **Abhyankar, Reyna et al., 2026** — Abhyankar, Reyna; Qi, Qi; Zhang, Yiying. 2026. OSWorld-Human: Benchmarking the Efficiency of Computer-Use Agents. Proceedings of Machine Learning and Systems 8 (MLSys 2026). 正式引用链接：未记录. 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2506.16042v2)（v2，版本日期：2026-05-18；初版日期：2025-06-19）. 来源等级：顶级会议／期刊。

<a id="ref-skill-nb-selective-formalization-and-gated-execution-for-durable-agent-workflows"></a>

- **Amine El Hattami et al., 2026** — Amine El Hattami; Nicolas Chapados; Christopher Pal. 2026. SKILL.nb: Selective Formalization and Gated Execution for Durable Agent Workflows. FAGEN@ICML 2026 Poster (ICML 2026 workshop, venueid ICML.cc/2026/Workshop/FAGEN; not the ICML main conference). [正式引用链接](https://arxiv.org/abs/2606.08049). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2606.08049v1)（v1，版本日期：2026-06-06；初版日期：2026-06-06）. 来源等级：合格机构补充。

<a id="ref-expel-llm-agents-are-experiential-learners"></a>

- **Andrew Zhao et al., 2024** — Andrew Zhao; Daniel Huang; Quentin Xu; et al. 2024. ExpeL: LLM Agents Are Experiential Learners. Proceedings of the AAAI Conference on Artificial Intelligence, Vol. 38 No. 17: AAAI-24 Technical Tracks 17, AAAI Technical Track on Natural Language Processing II, pp. 19632-19642 (published 2024-03-24), DOI 10.1609/aaai.v38i17.29936. [正式引用链接](https://doi.org/10.1609/aaai.v38i17.29936). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2308.10144v3)（v3，版本日期：2024-12-20；初版日期：2023-08-20）. 来源等级：顶级会议／期刊。

<a id="ref-skillweaver-web-agents-can-self-improve-by-discovering-and-honing-skills"></a>

- **Boyuan Zheng et al., 2025** — Boyuan Zheng; Michael Y. Fatemi; Xiaolong Jin; et al. 2025. SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills. arXiv 预印本. [正式引用链接](https://arxiv.org/abs/2504.07079v1). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2504.07079v1)（v1，版本日期：2025-04-09；初版日期：2025-04-09）. 来源等级：合格机构补充。

<a id="ref-from-exploration-to-mastery-enabling-llms-to-master-tools-via-self-driven-interactions"></a>

- **Changle Qu et al., 2025** — Changle Qu; Sunhao Dai; Xiaochi Wei; et al. 2025. From Exploration to Mastery: Enabling LLMs to Master Tools via Self-Driven Interactions. ICLR 2025 (International Conference on Learning Representations 2025), main conference (proceedings 'Conference' track); decision Accept (Oral), Oral Session 4B, also Poster Session 3. [正式引用链接](https://proceedings.iclr.cc/paper_files/paper/2025/hash/8c22e5e918198702765ecff4b20d0a90-Abstract-Conference.html). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2410.08197v2)（v2，版本日期：2025-02-26；初版日期：2024-10-10）. 来源等级：顶级会议／期刊。

<a id="ref-webcoach-self-evolving-web-agents-with-cross-session-memory-guidance"></a>

- **Genglin Liu et al., 2025** — Genglin Liu; Shijie Geng; Sha Li; et al. 2025. WebCoach: Self-Evolving Web Agents with Cross-Session Memory Guidance. ICLR 2026 Workshop on Memory for LLM-Based Agentic Systems (MemAgents), workshop paper in Poster and Discussion Session 1. [正式引用链接](https://arxiv.org/abs/2511.12997). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2511.12997v2)（v2，版本日期：2026-07-22；初版日期：2025-11-17）. 来源等级：合格机构补充。 年份字段记为 2025，发表处字段包含 2026；沿用原记录，不据发表处推改年份。

<a id="ref-voyager-an-open-ended-embodied-agent-with-large-language-models"></a>

- **Guanzhi Wang et al., 2024** — Guanzhi Wang; Yuqi Xie; Yunfan Jiang; et al. 2024. Voyager: An Open-Ended Embodied Agent with Large Language Models. Transactions on Machine Learning Research (TMLR), March 2024, journal paper (ISSN 2835-8856); certifications J2C (Journal to Conference) with event certification iclr.cc/ICLR/2025/Journal_Track. [正式引用链接](https://openreview.net/forum?id=ehfRiF0R3a). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2305.16291v2)（v2，版本日期：2023-10-19；初版日期：2023-05-25）. 来源等级：顶级会议／期刊。

<a id="ref-coevoskills-self-evolving-agent-skills-via-co-evolutionary-verification"></a>

- **Hanrong Zhang et al., 2026** — Hanrong Zhang; Shicheng Fan; Henry Peng Zou; et al. 2026. CoEvoSkills: Self-Evolving Agent Skills via Co-Evolutionary Verification. COLM 2026 (Conference on Language Modeling), main conference paper; OpenReview venue 'COLM 2026', venueid colmweb.org/COLM/2026/Conference, publication date 2026-07-08; official COLM 2026 Accepted Papers page lists it as a poster (Imperial Ballroom, Poster Session 3, #38). [正式引用链接](https://openreview.net/forum?id=gQjmJIichQ). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2604.01687v3)（v3，版本日期：2026-08-10；初版日期：2026-04-02）. 来源等级：顶级会议／期刊。

<a id="ref-appworld-a-controllable-world-of-apps-and-people-for-benchmarking-interactive-coding-agents"></a>

- **Harsh Trivedi et al., 2024** — Harsh Trivedi; Tushar Khot; Mareike Hartmann; et al. 2024. AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents. ACL 2024: Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), main conference, pages 16022-16076, Bangkok, Thailand, August 2024; Anthology ID 2024.acl-long.850; DOI 10.18653/v1/2024.acl-long.850. [正式引用链接](https://aclanthology.org/2024.acl-long.850/). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2407.18901v1)（v1，版本日期：2024-07-26；初版日期：2024-07-26）. 来源等级：顶级会议／期刊。

<a id="ref-actionengine-from-reactive-to-programmatic-web-agents-via-state-machine-memory"></a>

- **Hongbin Zhong et al., 2026** — Hongbin Zhong; Fazle Faisal; Luis França; et al. 2026. ActionEngine: From Reactive to Programmatic Web Agents via State Machine Memory. arXiv 预印本. [正式引用链接](https://arxiv.org/abs/2602.20502). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2602.20502v2)（v2，版本日期：2026-09-28；初版日期：2026-02-24）. 来源等级：合格机构补充。

<a id="ref-metaagent-toward-self-evolving-agent-via-tool-meta-learning"></a>

- **Hongjin Qian et al., 2025** — Hongjin Qian; Zheng Liu. 2025. MetaAgent: Toward Self-Evolving Agent via Tool Meta-Learning. arXiv 预印本. [正式引用链接](https://arxiv.org/abs/2508.00271). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2508.00271v2)（v2，版本日期：2025-09-01；初版日期：2025-08-01）. 来源等级：合格机构补充。

<a id="ref-web-agents-with-world-models-learning-and-leveraging-environment-dynamics-in-web-navigation"></a>

- **Hyungjoo Chae et al., 2025** — Hyungjoo Chae; Namyoung Kim; Kai Ong; et al. 2025. Web Agents with World Models: Learning and Leveraging Environment Dynamics in Web Navigation. International Conference on Learning Representations 2025 (ICLR 2025), Conference. [正式引用链接](https://proceedings.iclr.cc/paper_files/paper/2025/hash/a00548031e4647b13042c97c922fadf1-Abstract-Conference.html). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2410.13232v2)（v2，版本日期：2025-03-29；初版日期：2024-10-17）. 来源等级：顶级会议／期刊。

<a id="ref-mrsteve-instruction-following-agents-in-minecraft-with-what-where-when-memory"></a>

- **Junyeong Park et al., 2025** — Junyeong Park; Junmo Cho; Sungjin Ahn. 2025. MrSteve: Instruction-Following Agents in Minecraft with What-Where-When Memory. International Conference on Learning Representations 2025 (ICLR 2025), Conference (main), poster. [正式引用链接](https://proceedings.iclr.cc/paper_files/paper/2025/hash/2af7168a1f19e0ae61134f89eb238e57-Abstract-Conference.html). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2411.06736v5)（v5，版本日期：2025-04-11；初版日期：2024-11-11）. 来源等级：顶级会议／期刊。

<a id="ref-ai-agents-that-matter"></a>

- **Kapoor, Sayash et al., 2025** — Kapoor, Sayash; Stroebl, Benedikt; Siegel, Zachary S.; et al. 2025. AI Agents That Matter. Transactions on Machine Learning Research. 正式引用链接：未记录. 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2407.01502v1)（v1，版本日期：2024-07-01；初版日期：2024-07-01）. 来源等级：顶级会议／期刊。

<a id="ref-optimizing-instructions-and-demonstrations-for-multi-stage-language-model-programs"></a>

- **Krista Opsahl-Ong et al., 2024** — Krista Opsahl-Ong; Michael J Ryan; Josh Purtell; et al. 2024. Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs. EMNLP 2024: Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing (main conference), pages 9340-9366, Miami, Florida, USA, November 2024; Anthology ID 2024.emnlp-main.525; DOI 10.18653/v1/2024.emnlp-main.525. [正式引用链接](https://aclanthology.org/2024.emnlp-main.525/). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2406.11695v2)（v2，版本日期：2024-10-06；初版日期：2024-06-17）. 来源等级：顶级会议／期刊。

<a id="ref-grow-the-harness-not-the-context-from-strategy-free-scaffolds-to-reusable-specialist-agents"></a>

- **Laizhen Li et al., 2026** — Laizhen Li; Jiarui Li; Juanjuan Zhao; et al. 2026. Grow the Harness, Not the Context: From Strategy-Free Scaffolds to Reusable Specialist Agents. arXiv 预印本. [正式引用链接](https://arxiv.org/abs/2609.26760v2). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2609.26760v2)（v2，版本日期：2026-09-24；初版日期：2026-09-22）. 来源等级：合格机构补充。

<a id="ref-gepa-reflective-prompt-evolution-can-outperform-reinforcement-learning"></a>

- **Lakshya A Agrawal et al., 2026** — Lakshya A Agrawal; Shangyin Tan; Dilara Soylu; et al. 2026. GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning. ICLR 2026, main conference; decision 'Accept (Oral)' (ICLR.cc/2026/Conference). [正式引用链接](https://proceedings.iclr.cc/paper_files/paper/2026/hash/0e9e708b6f48e14fd0ac29e167413f76-Abstract-Conference.html). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2507.19457v2)（v2，版本日期：2026-02-14；初版日期：2025-07-25）. 来源等级：顶级会议／期刊。

<a id="ref-a-self-improving-coding-agent"></a>

- **Maxime Robeyns et al., 2025** — Maxime Robeyns; Martin Szummer; Laurence Aitchison. 2025. A Self-Improving Coding Agent. ICLR 2025 Workshop 'Self-Improving Foundation Models Without Human Supervision', Oral in Workshop (workshop paper, not ICLR main conference). [正式引用链接](https://arxiv.org/abs/2504.15228). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2504.15228v2)（v2，版本日期：2025-05-16；初版日期：2025-04-21）. 来源等级：合格机构补充。

<a id="ref-from-failed-trajectories-to-reliable-llm-agents-diagnosing-and-repairing-harness-flaws"></a>

- **Mengzhuo Chen et al., 2026** — Mengzhuo Chen; Junjie Wang; Zhe Liu; et al. 2026. From Failed Trajectories to Reliable LLM Agents: Diagnosing and Repairing Harness Flaws. arXiv 预印本. [正式引用链接](https://arxiv.org/abs/2606.06324v2). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2606.06324v2)（v2，版本日期：2026-07-02；初版日期：2026-06-04）. 来源等级：合格机构补充。

<a id="ref-recursive-self-evolving-agents-via-held-out-selection"></a>

- **Michael Nguyen et al., 2026a** — Michael Nguyen; Quoc Nguyen; Paul Vuong. 2026. Recursive Self-Evolving Agents via Held-Out Selection. arXiv 预印本. [正式引用链接](https://arxiv.org/abs/2606.28374). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2606.28374v1)（v1，版本日期：2026-06-17；初版日期：2026-06-17）. 来源等级：合格机构补充。

<a id="ref-tracecompiler-skill-guided-mining-and-compilation-of-llm-agent-traces-into-mostly-deterministic-workflows"></a>

- **Salma El Yadouni et al., 2026** — Salma El Yadouni; Guanyi Li. 2026. TraceCompiler: Skill-Guided Mining and Compilation of LLM Agent Traces into Mostly Deterministic Workflows. arXiv 预印本. [正式引用链接](https://arxiv.org/abs/2608.02680). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2608.02680v1)（v1，版本日期：2026-08-03；初版日期：2026-08-03）. 来源等级：合格机构补充。

<a id="ref-harness-r1-learning-to-edit-executable-runtime-harnesses-from-agent-failure-trajectories"></a>

- **Shuai Shao et al., 2026** — Shuai Shao; Kangning Zhang; Qingyao Li; et al. 2026. Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories. arXiv 预印本. [正式引用链接](https://arxiv.org/abs/2608.02276). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2608.02276v1)（v1，版本日期：2026-08-03；初版日期：2026-08-03）. 来源等级：合格机构补充。

<a id="ref-are-online-skill-and-memory-modules-always-worth-their-tokens-a-budget-constrained-study-of-web-agents"></a>

- **Sina Hajimiri et al., 2026** — Sina Hajimiri; Masih Aminbeidokhti; Jose Dolz; et al. 2026. Are Online Skill and Memory Modules Always Worth Their Tokens? A Budget-Constrained Study of Web Agents. EMNLP 2026 (The 2026 Conference on Empirical Methods in Natural Language Processing), main conference, paper ID 4950-MAIN, poster (Session 4, Poster Session B, 2026-10-25). [正式引用链接](https://arxiv.org/abs/2606.15017). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2606.15017v2)（v2，版本日期：2026-08-30；初版日期：2026-06-12）. 来源等级：顶级会议／期刊。

<a id="ref-reasoningbank-scaling-agent-self-evolving-with-reasoning-memory"></a>

- **Siru Ouyang et al., 2026** — Siru Ouyang; Jun Yan; I-Hung Hsu; et al. 2026. ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory. ICLR 2026, main conference, poster. [正式引用链接](https://openreview.net/forum?id=jL7fwchScm). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2509.25140v2)（v2，版本日期：2026-03-16；初版日期：2025-09-29）. 来源等级：顶级会议／期刊。

<a id="ref-mobilegpt-augmenting-llm-with-human-like-app-memory-for-mobile-task-automation"></a>

- **Sunjae Lee et al., 2024** — Sunjae Lee; Junyoung Choi; Jungjae Lee; et al. 2024. MobileGPT: Augmenting LLM with Human-like App Memory for Mobile Task Automation. Proceedings of the 30th Annual International Conference on Mobile Computing and Networking (ACM MobiCom 2024), research paper, pp. 1119-1133. [正式引用链接](https://doi.org/10.1145/3636534.3690682). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2312.03003v3)（v3，版本日期：2024-10-16；初版日期：2023-12-04）. 来源等级：顶级会议／期刊。 arXiv 页面登记题名：Explore, Select, Derive, and Recall: Augmenting LLM with Human-like Memory for Mobile Task Automation；所读 v3 正文采用 MobileGPT 题名。

<a id="ref-walt-web-agents-that-learn-tools"></a>

- **Viraj Prabhu et al., 2026** — Viraj Prabhu; Yutong Dai; Matthew Fernandez; et al. 2026. WALT: Web Agents that Learn Tools. International Conference on Learning Representations 2026 (ICLR 2026), Conference track (proceedings pp. 55589-55607); OpenReview venue field: "ICLR 2026 Poster". [正式引用链接](https://proceedings.iclr.cc/paper_files/paper/2026/hash/5b175f9e93873e3a10a6ce43dbb82e05-Abstract-Conference.html). 实际读的版本：[版本链接（PDF）](https://arxiv.org/pdf/2510.01524v1)（v1，版本日期：2025-10-01；初版日期：2025-10-01 (Wed, 1 Oct 2025 23:41:47 UTC)）. 来源等级：顶级会议／期刊。 校准补读：[ICLR 2026 正式版 PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/5b175f9e93873e3a10a6ce43dbb82e05-Paper-Conference.pdf)（正式版；正文未印发布日期；PDF 元数据创建日期：2026-02-23；获取日期：2026-09-29）。

<a id="ref-self-evolving-world-models-for-llm-agent-planning"></a>

- **Xuan Zhang et al., 2026** — Xuan Zhang; Wenxuan Zhang; See-Kiong Ng; et al. 2026. Self-Evolving World Models for LLM Agent Planning. arXiv 预印本. [正式引用链接](https://arxiv.org/abs/2606.30639). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2606.30639v2)（v2，版本日期：2026-09-01；初版日期：2026-06-29）. 来源等级：合格机构补充。

<a id="ref-coverage-not-credit-failure-credit-routing-of-zeroth-order-perturbation-budgets-does-not-improve-on-pool-sample-efficiency-for-llm-agents"></a>

- **Yuxu Ge, 2026** — Yuxu Ge. 2026. Coverage, Not Credit: Failure-Credit Routing of Zeroth-Order Perturbation Budgets Does Not Improve On-Pool Sample Efficiency for LLM Agents. arXiv 预印本. [正式引用链接](https://arxiv.org/abs/2608.28011). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2608.28011v1)（v1，版本日期：2026-08-28；初版日期：2026-08-28）. 来源等级：合格机构补充。

<a id="ref-openskill-open-world-self-evolution-for-llm-agents"></a>

- **Zhiling Yan et al., 2026** — Zhiling Yan; Dingjie Song; Hanrong Zhang; et al. 2026. OpenSkill: Open-World Self-Evolution for LLM Agents. EMNLP 2026 (The 2026 Conference on Empirical Methods in Natural Language Processing), main conference, paper ID 3199-MAIN, virtual presentation (session 'Virtual 2', 2026-10-25, 18:00-19:30 CET, presenter Zhiling Yan), per the official detailed program linked from 2026.emnlp.org/program/. The ACL Anthology EMNLP 2026 volume is not yet published. [正式引用链接](https://arxiv.org/abs/2606.06741). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2606.06741v1)（v1，版本日期：2026-06-04；初版日期：2026-06-04）. 来源等级：顶级会议／期刊。

<a id="ref-metis-bridging-text-and-code-memory-for-self-evolving-agents"></a>

- **Zijie Dai et al., 2026** — Zijie Dai; Siuhin He; Hui Li; et al. 2026. Metis: Bridging Text and Code Memory for Self-Evolving Agents. arXiv 预印本. [正式引用链接](https://arxiv.org/abs/2606.24151). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2606.24151v1)（v1，版本日期：2026-06-23；初版日期：2026-06-23）. 来源等级：合格机构补充。

<a id="ref-better-faster-stronger-programmatic-skill-learning-best-reduces-agent-cost"></a>

- **Zixi Huang et al., 2026** — Zixi Huang; Xiheng Wang; Andrew Wang; et al. 2026. Better, Faster, Stronger: Programmatic Skill Learning Best Reduces Agent Cost. arXiv 预印本. [正式引用链接](https://arxiv.org/abs/2608.11338v1). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2608.11338v1)（v1，版本日期：2026-08-11；初版日期：2026-08-11）. 来源等级：合格机构补充。
