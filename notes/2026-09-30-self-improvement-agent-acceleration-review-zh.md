# 固定模型权重下的 Agent 加速与自我改进

从轨迹学习和环境探索出发的文献评估与研究建议

2026年9月30日

这份报告回答三个问题：不训练模型，Agent 可以怎样从过去的经历中改进；这些改进中，哪些真正降低了执行时间或费用；我们现有的研究计划与它们相比，还能提出什么具体、可检验的问题。它以用户提供的综述、文献网站和讲座字幕为入口，结合第三阶段草稿，核查相关原论文的方法、实验与局限。旧草稿用于理解研究意图，不作为已证实结论。

**核心判断是：方向成立，宽泛想法已有充分先例，研究问题需要进一步收窄。** 从轨迹提炼经验、生成程序技能、探索页面或环境、自动修改 harness，都已经有人做过。一些工作还报告了实际费用下降，并计入了技能构造的摊销。我们的下一步应比较具体机制在目标工作流中的净收益，不能把“历史经验让 Agent 越用越快”本身作为新颖性。

本次修订补充问题定义与符号、环境规律和反馈机制的区别、无权重的数据生成分支、评测目录筛查，以及已有方法验证与候选新问题的分界。下文明确区分三类表达：**原文定义**来自论文公式或算法；**本文改写**只用于统一解释，不能冒充作者公式；**本文判断**是对证据边界和研究价值的分析。限制若未明确标为“作者自述”，均应理解为本文的证据解释，而非作者已经承认的结论。

## 一 加速与 Self Evolve 是什么关系

### 一个是目标 一个是改进过程

Agent 加速关心完成工作用了多少时间和资源；self-improvement 或 self-evolution 关心系统如何从反馈中产生可持续的改变。两者有交集，但不存在必然的包含关系。一个自动演化的 Agent 可以更准确、却更慢；一个不学习的固定程序也可以通过并行执行、缓存或减少上下文实现加速。

本文把我们要做的事情称为**以执行效率为目标的无权重 Agent 改进**：执行模型以及本方法引入的改进模型不做新的参数训练，改变保存在提示、记忆、工具、程序和控制流程中；在业务正确性约束下，检验未来任务是否更快或更便宜。这比“做一个 self-evolving agent”更具体，也与现有第三阶段计划的意图一致。

综述把修改对象分为基础模型与外部 scaffold 两大类。后者再分 prompt、memory、tool 和 full scaffolding。这个分类有用，但四种外部对象可以同时改变：一份经验可能先成为文字规则，再成为可执行工具，最后导致控制逻辑变化。所谓 skill 也可能只是说明文档，不能看到这个词就理解成自动执行的代码。[1](https://arxiv.org/pdf/2607.13104v1)

| 改变对象 | 学到后保留什么 | 可能省下什么 | 可能新增什么 |
|---|---|---|---|
| 提示与策略 | 指令、示例、决策规则 | 错误重试、冗余推理 | 提示长度、候选验证 |
| 经验记忆 | 事实、失败原因、流程及适用条件 | 重复查找与试错 | 检索、总结、上下文和过期处理 |
| 工具与技能 | 函数、脚本、组合操作 | 逐步模型调用、机械操作 | 生成、测试、匹配、维护 |
| 整体执行框架 | 路由、观察处理、工具接口、控制代码 | 多种系统性重复开销 | 搜索、回归评估、复杂度 |

这里的“学”不要求神经网络训练。程序搜索、文字编辑、更新记忆条目的效用分，都可以学习。反过来，“执行模型冻结”也不保证整套方法没有训练：Harness-R1 会训练外层编辑器，因此不能直接作为本次免训练方法。Meta-TTL 虽然使用 meta-training 一词，实际主方法优化的是文字提示，符合范围。必须看更新对象和算法，不能按术语筛选。[7](https://arxiv.org/pdf/2604.00830v4)[38](https://arxiv.org/pdf/2608.02276v1)

### 用定义区分系统配置 执行轨迹和持久改进

综述§3的原式将Agent记为花体A，并写成模型与外部系统的二元组。为避免字体混淆，本文重命名为`Agent_t = (θ_t, Σ_t)`，其中`Σ_t = (p_t, m_t, Tools_t, g_t)`：θ是模型神经参数，p是提示，m是记忆及其检索更新机制，Tools是工具及接口，g是路由、调度等控制逻辑。运行中的观察、临时计划、短期上下文属于暂态X；同一θ在不同Σ和X下仍会产生不同的动作分布。[1](https://arxiv.org/pdf/2607.13104v1)，§3.1、式(1)–(3)

将原文式(4)、(6)写成易读的两步形式，**本文改写**为：`S_t = ExecuteAndEvaluate(Agent_t, Context_t)`，`Σ_(t+1) = Update(Σ_1…Σ_t, S_t)`，并保持`θ_(t+1)=θ_t`。S_t可以包含真实轨迹、成败、程序检查、文字批评和费用；Context_t是任务或部署上下文，**不是成本**。Update产生可在后续使用、也可撤销的持久更新。一次任务内多想几步、却没有保留任何改进产物，不能自动算作这种跨任务自改进。

这个定义不要求反馈全由模型自行产生：环境结果、测试程序、事先设定的规则都可以参与；也不保证每次更新后表现单调上升。“改进”描述的是机制和目标，实际可能回归。全scaffold可修改也不等于改进器本身已经递归变强。我们的(a)主要限定**信号来源为历史轨迹**，(b)主要限定**通过主动交互获取环境知识**；prompt/memory/tool/harness则限定更新对象，是另一条分类轴，不能把它们排成互斥类别。

综述§8.1还要求看整个改进过程。其式(26)可重命名为`q_t = E[Φ(x, τ)]`：x来自留出任务分布，τ由第t版Agent执行产生，Φ是评价器，q_t是期望任务表现；正文另限制累计预算b_t不超过B。它没有直接最小化执行时间，也没有自动计入所有建设费用。我们需要同时观察q_t、累计花费与未来执行节省，而不能只挑最好的一版截图。[1](https://arxiv.org/pdf/2607.13104v1)，§8.1

### 三种速度必须分账

第一种是**改进过程的效率**：用更少候选、样本或 CPU 小时找到更好的 Agent。HGM、GEPA、HarnessFix 有这类结果。第二种是**改进后的执行效率**：部署时完成同类任务更快或更便宜，SpeedRunner、MobileGPT、StarHarness 的部分实验属于这里。第三种是**全流程净收益**：执行节省超过探索、生成、验证、检索、失败回退与维护的总投入。

这三种结果不能互换。ACE 的适配时间明显下降，但独立部署统计的输入 token 增加；Meta-TTL 调用次数少于静态 Agent，但每个含六个episode的Jericho会话总时间更长。我们最终应追求第三种，同时分别报告前两种，才能知道收益来自哪里。

## 二 这次筛查覆盖什么

入口是《Self-Improvements in Modern Agentic Systems: A Survey》的 arXiv v1（2026年7月14日）、持续更新的项目网站，以及郭丹丹的公开分享字幕。网站与 PDF 不是同一天的文献快照。本次在网站方法表中保留了 **253条目录记录**：基础模型77条；外部 scaffold 176条，其中 prompt39、memory65、tool51、full scaffolding21。重复链接和错配条目保留在审计清单中，253不代表253篇独立论文。[1](https://arxiv.org/pdf/2607.13104v1)

我们先逐行做范围筛查，再对直接影响研究判断的工作读方法、评估协议、结果表及相关附录。筛查表明确区分“原文深读”“原文选读”和“目录级待核”，没有把未读全文的条目包装成否定结论。253条中，15条列为直接效率候选、47条为方法参考、63条为背景、70条按范围排除、17条重复、41条仍待核；这些是目录行标签，既不是质量排名，也不是全文阅读数量。正文重点比较约三十余项方法，完整逐项结果与分支证据笔记随报告保存。

本次补筛网站另列的**59条评测目录记录**：按主链接去重只有45个不同链接，14条是额外重复记录，其中还包含judge、平台及题名错链。方法与评测共312行，不能说成312篇独立、有效、已全文读完的论文。12篇重点评测原文另核任务、重置、反馈和指标协议，其余评测行仅做范围筛查。原目录“ClawBench”链接2601.08613实际指向磁性纳米线论文；通过作者官方仓库更正为2604.08523v2，原错链保留在索引供审计。综述正文§1–10已通读并重点核§3、6、7.2、7.6、8、9；没有逐篇展开其全部参考文献。

筛选优先级是：模型是否保持固定；是否从轨迹或环境反馈更新持久状态；是否减少实际执行资源；是否报告构造和验证成本；能否迁移到新任务、任务组合或变化后的环境。正式发表论文与研究机构预印本均可进入分析，但发表状态单独标注，预印本不冒充正式会议结论。补充 SpeedRunner、Metis、WALT、ActionEngine、HarnessFix、StarHarness 等直接近邻，以免被单个综述的目录边界限制。

清单确有需要纠正的地方。例如一个 Dynamic Cheatsheet 条目指向 Self-Notes，另有 WizardLM 和 SEDM 的题名与链接错配；ADAS 的网站会议信息也需要更正。最新 Meta-TTL 链接对应的标题和版本已变化。因此本报告按实际原论文引用，不能直接复制幻灯片上的年份、会议和数字。

字幕的价值在于解释作者的问题意识：他们同样关注改进成本与收益的取舍、环境变化和长期退化后的回滚。字幕存在自动转写错误，因此只用于概念线索；论文的数值和技术细节以原文为准。[41](https://www.bilibili.com/video/BV12yh86kEUS)我们没有复现这些实验，也没有用它们替代我们自己的业务工作流测量。

## 三 提示和文字反馈怎样产生改进

### TextGrad 的文本梯度到底是什么

TextGrad 将系统表示成计算图：提示产生回答，回答再参与下游任务，最后得到评价。反向过程让 LLM 结合某个节点的输入输出和下游批评，写出“这个节点应该怎样改”的反馈，再由另一次调用更新变量。它可以修改 prompt、代码或候选答案，而不需要访问执行模型的内部权重。[2](https://arxiv.org/pdf/2406.07496v1)，§2

**“梯度”在这里是作者明确使用的类比。** 普通梯度是一个数值导数，依赖可微函数和链式法则；文本梯度是一段有上下文的修改建议，没有保证对应某个真实导数，也没有普遍的下降方向或收敛保证。LLM 能提出有用建议，依靠的是它已有的语言、代码和任务推理能力，以及反馈是否准确。计算图帮助把最终错误追溯到可能需要改的组件。

按原文§2、式(4)–(11)简化并重命名符号，这个过程可以写成：`g_y = Critique(y, L)`，`g_x = Backward(x, y, g_y)`，`x_new = Edit(x, g_x)`。这里x是可编辑提示或代码，y是下游输出，L是任务评价，g_y与g_x都是文字反馈；Backward还读取节点关系和上下文。多条下游路径的反馈会汇集，再指导编辑。这是**本文对作者算法的改写**：没有对字符串做数值减法，也没有从文本中恢复模型权重的梯度。有效性最终依靠修改后的独立执行结果，而不依靠“梯度”这个名称。[2](https://arxiv.org/pdf/2406.07496v1)

以我们的问题作一个说明性例子：失败轨迹显示“日期跨月时选择了错误报销周期”。反馈可以沿执行链定位到日期计算的代码或提示，提出补充边界条件、调用日期函数的修改；随后仍要运行独立测试，判断是否修复。这个例子是我们的应用解释，不是 TextGrad 论文里的业务实验。它提供了 A 方向的候选生成方式，并不单独证明加速。

Trace 将类似思路推广到代码、提示和其他可编辑变量：保留程序执行关系、实际中间值与外部反馈，交给 OptoPrime 提出改动。其效果表中的运行分钟数包含优化、验证和测试，不能当作最终 Agent 的服务延迟；较大执行图也会增加上下文负担。[3](https://arxiv.org/pdf/2406.16218v2)，§2、Table2、§6

Trace的**原文问题定义**是OPTO三元组`(Θ, ω, T)`：Θ为可编辑变量空间，ω为固定问题描述，T为提供执行信息的oracle。每轮选择θ∈Θ，得到`τ=(f,g)`，其中g是实际执行DAG，f是某个输出节点的反馈，再据此更新θ。此处θ可以是Python代码或prompt，**不必是模型权重**；f也可以是异常日志或文字批评，作者没有要求每个问题都有一个可微的标量loss。原文§3.2明确讨论了执行图抽象粒度的取舍：过细使图复杂，过粗又丢失定位信息。这正是我们做轨迹诊断时需要验证的表示选择。[3](https://arxiv.org/pdf/2406.16218v2)，§§2.1、3.2

### GEPA 和 SkillOpt 已经把轨迹利用推进到哪里

GEPA 并非只看“这题错了”的分数。它读取执行轨迹、工具错误、评价标准等反馈，反思某个模块的提示，先用小批任务过滤，再在验证集上比较；候选池保留在不同任务上有优势的版本，还可合并它们的改进。这里的 Pareto 指跨任务表现互补，不是时间与费用的折中前沿。[4](https://arxiv.org/pdf/2507.19457v2)，§§2–3

它证明文字反思能够高效搜索提示，但需仔细解释效率数字：IFBench 上678 rollout是达到所选最佳检查点时的消耗，该设置的完整优化预算更大；“最多9.2倍更短”是特定模型和任务的提示长度，相对 MIPROv2，不是任务快9.2倍。GEPA适合做通用文字优化器基线，不能直接替代我们的执行加速证据。[4](https://arxiv.org/pdf/2507.19457v2)，Tables1–2、Fig18

SkillOpt 从成功和失败轨迹中改写一份自然语言 skill，限制每轮编辑量，保存被拒绝的编辑，经过独立选择集才接受更新，并用慢速反思修正优化策略。它已包含我们粗略想法里的“读轨迹、提出有限改动、验证、保留”部分，但输出仍是给模型阅读的策略文档。[5](https://arxiv.org/pdf/2605.23904v2)，§3

其 Table6 很能说明代价：Spreadsheet 的 skill 从224增至1,995 tokens，优化消耗21.4M tokens；SearchQA 从16增至857，优化消耗213.8M。部署时没有额外 optimizer 调用，不代表提示开销为零。它的任务性能有明显提升，但这些数字无法证明业务 Agent 的净加速。论文还出现针对 grader 读取结果的电子表格策略，这提醒我们把“业务要求确实满足”与“测试程序给分”分开核验，而不是仅依赖优化器自己理解评分规则。[5](https://arxiv.org/pdf/2605.23904v2)，Table6、§4.5

两篇论文的目标也需要分清。**GEPA原文式(2)在固定模型权重条件下的改写**是：`Π* = argmax_Π E[μ(Φ(x; Π, Θ_fixed), m)]`，受rollout预算B约束。Φ是由多个模块组成的系统，Π是各模块提示，Θ_fixed是冻结权重，x是任务输入，m是标准答案、rubric或测试等评价资料，μ是任务得分；期望取自任务分布。B限制优化时的执行与评价次数，目标里没有部署时间或费用惩罚。[4](https://arxiv.org/pdf/2507.19457v2)，§2

**SkillOpt原文式(1)–(3)**则把固定模型M和harness h执行任务x、读取skill s得到的轨迹与奖励写成`(τ, r_x(s)) = h(M,x,s)`；我们给r补上x下标以免混淆不同任务。开发集产生候选集合C，选择集决定` s* = argmax_{s∈C} 平均_{x∈D_sel} r_x(s)`，最终只在D_test报告结果。每轮“learning rate”是允许增加、删除、替换的文字编辑预算，不是权重学习率。两者都能帮助我们生成更好的策略，但若目标是加速，还必须另外记录资源代价，不能把奖励上升等同于速度上升。[5](https://arxiv.org/pdf/2605.23904v2)，§3

### ACE 与 Meta-TTL 为什么特别值得比较

ACE 把经验维护拆成执行、反思、整理三个角色，用带 ID 的条目和局部增量更新避免反复重写整份记忆。它是比简单追加反思更完整的上下文维护方法。AppWorld 中相对 GEPA 的离线适配时间从53,898降到9,517秒；但附录另一设置的160个评估任务，ACE输入 token为58.62M，GEPA为26.96M，虽然 rollout从2,470降到2,354。这里体现了**更快学到经验、执行时读更多经验**的取舍；两组实验设置不能拼成一个统一加速数字。[6](https://arxiv.org/pdf/2510.04618v3)，Table4；AppA.3 Tables12–15

ACE的主方法不是数值梯度优化。可用**本文算法改写**概括为`m_new = Dedup(Merge(m, Δ))`：m是带ID和使用统计的playbook，Δ是反思后由curator产生的局部条目更新，Merge应用更新，Dedup处理冗余。其核心研究对象是经验如何增量维护；这与检索时挑选哪条经验、执行时如何把它转成动作是不同问题。[6](https://arxiv.org/pdf/2510.04618v3)，§3

Meta-TTL 进一步学习“怎样根据经历改进”：外循环搜索 meta-prompt，内循环依据它在每次尝试后改 actor prompt，下一次episode重置任务环境但保留改进后的提示。最终固定meta-prompt评估适应能力；Jericho的域内评估仍使用meta-training阶段的游戏，WebArena-lite和τ²的域内评估使用留出实例，另设域外评估，不能统称全部为未见任务。主方法两层都不改模型权重。[7](https://arxiv.org/pdf/2604.00830v4)，§§3、4.1

**Meta-TTL原文式(1)–(4)**的核心是`W-AUC = Σ_k k·J(τ_k) / Σ_k k·J_max(g)`，外循环最大化训练任务上的期望W-AUC。g为任务，τ_k为第k次尝试轨迹，J为回报，J_max(g)为该任务的最大回报，k从1到K。它更重视后期尝试的表现，而不是奖励更短的墙钟时间。内循环`ρ_(k+1) ~ f_φ(· | ρ_k,H_k)`中，ρ是actor prompt，H_k是此前尝试历史，φ是控制改进器的文字meta-prompt；φ也不是神经网络权重。[7](https://arxiv.org/pdf/2604.00830v4)

不过其每个含六次episode的Jericho会话，三次运行平均从静态基线593.2秒、196K tokens，变成860.9秒、364K tokens；调用数却从231降到204。它比若干昂贵的自改进基线快，但比不改进更慢。每个 benchmark 另有约30–70美元离线 meta-search。论文主要证据是加权学习曲线与跨域表现，而不是执行净收益。[7](https://arxiv.org/pdf/2604.00830v4)，§4.4、Table6

FORGE提供另一个有用对照：多个实例把失败转为文字规则或示例，按阶段广播表现最好的记忆，达到阈值就冻结。它把记忆表示与选择机制拆开研究，Rules相对Examples更省token；这个节省不能解释成比静态 Agent便宜。作者也发现过早冻结可能牺牲后续学习，且只在一个网络防御环境和攻击类型下验证。对我们最有帮助的是：经验是否有价值，需要独立选择；保存得越多并不一定越好。[8](https://arxiv.org/pdf/2605.16233v1)，§§3、5、7

## 四 从轨迹记忆到可执行技能

### 记住事实与学会做事需要分开

A-Mem是用户幻灯片中的记忆代表。新交互变成包含内容、时间、关键词、标签和上下文的笔记；系统寻找关联笔记、建立链接，还会根据新信息修改旧笔记的描述。自进化发生在外部记忆的内容与组织上，不是基础模型越来越强。它主要在LoCoMo、DialSim等长对话问答上检验能否更好地找回和关联信息。[12](https://proceedings.neurips.cc/paper_files/paper/2025/hash/19909c36f51abc4856b4560aff3d36d6-Abstract-Conference.html)，§3–4

它与加速的关系主要是减少每次携带的历史上下文。论文报告的token长度和memory operation费用口径并不完全一致，不能直接解释成完整业务任务的长期成本下降。它没有证明从浏览器动作轨迹学到程序技能，因此适合参考记忆组织，不是我们B方向最直接的基线。

AWM更接近执行经验：从成功轨迹抽象子任务，参数化具体对象，存成文字workflow，运行时给Agent参考。正式ICML版本报告WebArena成功率35.5%，成功路径步数约7.9到5.9；但是主要方法仍让模型逐步执行，不能当作宏操作。附录将其改为可执行高层动作AWM-AS后，Mind2Web任务成功率从4.8%降至3.6%，尽管单步指标略升。作者将一部分问题归因于弹窗和状态变化，固定序列跳过了必要观察。Table13邻近文字与表值不一致，此处采用表中4.8%与3.6%。[13](https://proceedings.mlr.press/v267/wang25bx.html)，Table1、AppF Table13/Fig6

ReasoningBank同时从成功与失败中提炼策略，执行前检索；另有扩大多轨迹采样的MaTTS。Gemini-2.5-Flash在去除Map的WebArena上，成功率40.5%到48.8%，steps9.7到8.3；但成本附录的总token统计从50,847.4增至53,054.5，包含judge和记忆提取，约多4.3%。这两张表各有口径，成本表未单独明确模型，不能当成全模型平均收益。[14](https://arxiv.org/pdf/2509.25140v2)，Table1、AppC.2 Table5

两者的**问题定义**都是固定模型借助外部文字经验做未来任务。AWM原文§2写作`I(E)→W`、`M+W→M_w`：E是经验集合，I诱导工作流W，加入原记忆M后得到M_w，执行模型仍逐步根据观察选动作。AWM的online模式也可用LM judge；关键差别在于AWM主要从判定成功的轨迹抽工作流，ReasoningBank同时从成功与失败提炼策略，原文§3明确其运行时不依赖ground truth。后者默认更新可用**本文改写**表示为`M_new = M_old ∪ Extract(task, trajectory, Judge结果)`；默认consolidation是追加，不能描述成已经自动证伪并删除旧规则。作者自述的不足分别包括AWM过度服从不适用工作流，以及ReasoningBank自评噪声、检索与合并机制较简单。[13](https://proceedings.mlr.press/v267/wang25bx.html)，§§2、3.2；[14](https://arxiv.org/pdf/2509.25140v2)，§3、AppE

ExpeL的经验比较与示例检索同样能改善任务表现，却增加经验上下文。ALFWorld平均动作14.82到14.30，trajectory token从2,051.49到2,856.70；这里是轨迹字符串统计，也不等于逐次API累计账单。共同的教训是：文字经验可以减少错误决策，同时让每次决策读得更多。[15](https://arxiv.org/pdf/2308.10144v3)，AppJ

### 如何判断哪条经验值得用

MemRL在每条外部记忆上维护效用分，先按语义筛选，再按经验带来的奖励更新选择。它不反传更新LLM，也不因此需要我们训练模型；这是一种可以在固定API模型上实现的奖励学习。GPT-4o-mini的LifelongAgent OS留出迁移成功率从67.3%到74.6%，但论文没有建立普遍部署净加速。对我们更有帮助的是把“语义相似”与“曾经有效”分开，再检验效用是否应该扣除资源成本。[16](https://arxiv.org/pdf/2601.03192v2)，§3、AppF/G

MemRL**实际实现的原文式(4)**是`Q_new = Q_old + α(r − Q_old)`：Q是外部记忆条目的效用估计，α是更新步长，r是该次任务回报。先按语义相似度筛候选，再按式(7)的`score=(1−λ)·标准化相似度 + λ·标准化Q`取记忆；标准化采用z-score，λ控制两项权重。改变的是检索策略，不是LLM或环境转移模型。论文先给了一般TD式，但不能因此说实现训练了神经Q网络。作者指出长轨迹、多个记忆共享结果时的归因，以及低任务相似性和错误奖励会影响效果；给r加入时间或费用惩罚属于我们要另行验证的扩展。[16](https://arxiv.org/pdf/2601.03192v2)，§§3–4、6、AppG

成本敏感的接纳也已有先例。SEDM提出paired A/B，按奖励增益扣除延迟或token惩罚接纳、删除经验；因此“只有划算才保留”不能作为全新原则。它的主要token优势相对G-Memory，而非无记忆，例如FEVER的输入token由G-Memory3.62M降至2.47M，但无记忆只需1.65M；反复回放的构造开销还需另计。用历史工具响应重放，也不能保证覆盖改变策略后真实环境会给出的反事实响应。[39](https://arxiv.org/abs/2509.09498v3)，§3、Tables2–4

负例CTIM-Rover从仓库轨迹提炼通用与项目经验，却在45个留出软件任务中从原系统42%降到完整记忆版本40%，单加insights为31%。样本小，不能否定全部记忆方法；但它展示了表面相似经验把Agent带向错误位置的具体风险。[40](https://arxiv.org/abs/2505.23422v1)，Table1、§5

### Metis 已经做到先用文字 再把稳定经验变成代码

Metis将历史经验分为plans、环境facts和pitfalls。它先按文字plan在多少个任务中**被选中**来触发程序化，这些任务不必成功；生成工具时再要求至少两个结构不同的query支持，并暴露可变参数。频繁被选中并不证明plan导致了成功。代码通过依赖与编译检查后供后续任务调用，反思既利用失败轨迹，也利用成功但低效的轨迹。[17](https://arxiv.org/pdf/2606.24151v1)，§2–3、Algorithm1

其**原定义**是`M=(M_text,M_code)`、`M_text=M_env ∪ M_pit ∪ M_plan`。第k个任务后`M_k=Reflect(M_(k−1),τ_k)`；τ_k为轨迹。每条文字记忆含内容、类别和失效位，旧规则被纠正时标为失效并追加新条目。触发条件可写为`|B(p)|≥θ`，B(p)是选过计划p的任务索引集合，θ是阈值。Codifier使用plan与相关queries，刻意不输入原始候选轨迹，减少把一次具体执行硬编码进去。反思器还能访问环境调查原因，形成“观察失败—补探查—保存规则—后续检索—新证据使旧规则失效”的闭环。这已直接覆盖(a)和(b)，但文字是建议、编译通过是代码接纳条件，二者都不是业务语义的正确性证明。[17](https://arxiv.org/pdf/2606.24151v1)，§§3.2–3.5

固定GPT-4o执行器、Sonnet4.6反思，在AppWorld官方划分中，无记忆到Metis的TGC由51.8%到60.1%，每任务执行token112.6K到97.4K，ReAct轮数14.55到11.25。另在重采样划分中，No Memory、SkillX、Metis三个方法共同完成的62题上，Metis也降低了token，减少成功题目集合不同造成的混杂。构造反思另需7.9M tokens，但排除了生成训练轨迹的成本，没有完整秒数或美元回本结论。[17](https://arxiv.org/pdf/2606.24151v1)，Tables1–2

作者的更早代码化消融在部分设置下执行更省，却准确率更低、建设更贵。它已经把问题推进到“什么经验值得编译”。我们若继续此方向，需要比较环境条件证据、失败恢复、状态变化以及真实费用，而不是重新提出文字转代码。

### SpeedRunner 已经直接研究历史技能学习如何降本

SpeedRunner让固定模型的actor分批执行，另一个固定模型coding agent读取历史轨迹、工具调用栈和技能版本，新增、修改或删除程序技能，区分公开工具和内部辅助函数。它不要求在旧环境任务上重新回放来验收技能；coding agent仍可执行代码、统计日志和做局部测试。因此它与A方向直接重合，不能将其描述成完全没有验证。[23](https://arxiv.org/pdf/2608.11338v1)，§3、AppI

其**原定义**用`g: L×H→L`表示技能归纳器：L为技能库，H为带库版本的历史轨迹。Algorithm1是执行一批任务、把轨迹和当时版本加入H、再令`L←g(L,H)`，两类模型权重均固定。它不是只将成功动作拼成宏。论文AppI.2的实际案例中，反复出现资源`not_found`错误，归纳器判断目标不在可见范围，加入有界局部探索，边移动边读观察，发现目标即停止。这把环境条件与恢复逻辑写进了程序，也直接涉及(b)。作者自述尚未覆盖旗舰模型和更昂贵的大型基准，在线收益有较大误差条与不稳定，未研究归纳器本身的元学习。[23](https://arxiv.org/pdf/2608.11338v1)，§§2–3、Limitations、AppI.2

ScienceWorld、BabyAI和Crafter实验以200条学习episode、定期留出评估和三次seed考察持续学习；BabyAI曲线显示成功率约从67%接近100%，单轨迹美元成本约为ReAct的八分之一。这里是近似曲线结果、限该环境，不能外推网页或说墙钟时间也快八倍。尤其需要承认：附录已将技能学习费用按batch摊入，并统计输入、缓存输入和输出，不存在“该文完全忽略学习成本”的空白。[23](https://arxiv.org/pdf/2608.11338v1)，Fig3、AppA.3

ASI则采用另一种接纳方法：从成功轨迹归纳代码，把新技能插回源任务进行执行验证。WebArena同Claude3.5 Sonnet对照，无技能32.7%成功率、5.6步，文字AWM36.3%、5.9步，程序技能40.4%、5.0步。一个宏内部可以有多个UI动作，所以5.0不是浏览器事件数，也不是秒；生成、回放和judge还会增加学习开销。它适合做我们“需要验证的程序技能”基线，与SpeedRunner的日志归纳形成有意义的对照。[19](https://arxiv.org/pdf/2504.06821v2)，§2、Table1

### 技能包有实际加速结果 但覆盖和泛化不能省略

MUSE-Autoskill将成功任务沉淀为含说明、脚本、资源和经验的技能包，再在相同任务重用。SkillsBench的75个可运行任务中，只有47题构造出了可用skill。在这个覆盖子集，no-skill的中位729.3秒降至434.7秒，token579K到499K；生成skill另需中位156.3秒和364K tokens。这些延迟不含SkillsBench验证器耗时。全集把未覆盖任务计入后，自制技能得分53.42%，低于人类技能59.67%，不能只引用覆盖题上的85.24%。[24](https://arxiv.org/pdf/2605.27366v2)，§4.3、Tables4、6

它支持特定任务复用可以节省执行，但同题成功轨迹再跑会高估泛化，报告也不覆盖全部失败学习与长期维护。OpenSkill则是另一个提醒：它主动搜索外部知识并生成验证依据，Opus4.6的任务得分25.5%到43.6%，执行均时却465.0到845.4秒，且不含构造。作者测到proxy test precision为56.9%；所谓88.9%是另一项测试意图覆盖评估，不是验证准确率。[25](https://arxiv.org/pdf/2606.06741v1)，Tables1、3、AppE Table8

这些结果说明我们必须同时报覆盖率、正确性和资源量；只统计学会技能的成功子集，会把很容易复用的任务挑出来，形成过于乐观的加速结论。

## 五 环境探索能带来什么

环境探索与历史轨迹学习是两个可以组合的采集渠道。前者主动补充未知条件，后者利用已经支付过成本的交互。我们需要问的不是“要不要探索整个环境”，而是“哪条不确定的环境规律值得额外验证，它会影响多少未来任务”。

### 学到环境规则与建好反馈机制是两件事

“环境规则”可能是字段依赖、可用操作与前置条件、状态转移、搜索参数语义，或动作后哪些属性保持不变。它可以存在文字、schema、状态图、代码guard或预测器上下文里，不要求方法名叫world model。**反馈机制**则回答如何知道刚才做对了：工具错误、页面真实变化、数据库状态差分、业务断言和最终任务评价提供的证据不同。学习器可以改对环境的认识，却不应随意改掉最终正确性标准。

一个有意义的(b)闭环至少要说清：观测到了什么，形成了哪条假设，假设如何改变预测或动作，用什么真实反馈检验，遇到矛盾怎样更新。只保存成功代码，不足以证明学到可修正的规则；但已有代码里的状态检查与恢复也不能被排除在环境学习之外。Metis、SpeedRunner、WALT、MobileGPT和ActionEngine都以不同形式覆盖了这个闭环的若干环节。

### 从自主探索到程序化复用

Voyager提供了早期完整范式：依据Minecraft状态选择学习目标，生成代码，利用环境反馈修复，成功技能进入检索库供后续组合。它表明探索目标本身也可以由Agent决定；但“15.3倍”等结果的横轴是prompting iteration，不能转成实际秒数。技能库并非所有早期里程碑收益的唯一来源。[26](https://arxiv.org/pdf/2305.16291v2)，§3、Table1

SkillWeaver把这条路线带到网页：自动提出短探索任务，执行后抽取参数化Python/Playwright函数，再生成输入测试和修复。每站约160轮探索或测试，意味着明确的前期投入。固定GPT-4o时WebArena成功率22.6%到29.8%；真实网站四站57题为40.2%到56.2%。它有很强的“探索能学会操作”的证据，但没有完整墙钟时间、美元或回本曲线。[20](https://arxiv.org/pdf/2504.07079v1)，§2–3、Tables1–2

WALT进一步利用网站功能本身构造工具，例如把可通过URL参数实现的搜索排序直接变成操作，减少反复点击；工具也可包含确定性步骤与必要的agentic fallback。在VisualWebArena-Classifieds、同GPT-5-mini、text/self的消融中，无工具57.5%成功率、8.9步，有发现工具61.5%、6.5步。完整配置另含多模态DOM解析和外部验证器，不能把其全部提升算作自主学习的贡献。[21](https://proceedings.iclr.cc/paper_files/paper/2026/hash/5b175f9e93873e3a10a6ce43dbb82e05-Abstract-Conference.html)，§4.4、Table2

其正式会议版报告305个候选、252个工具验证成功，构造每工具约1.67美元。作者以基线0.12美元每任务估计约14次使用回本，但严格计算必须用“基线成本减去新方案在线成本”作分母；因此这只是粗略建设投入对比，不是完整净回本点。动态页面、罕见参数和selector漂移仍是主要局限。[21](https://proceedings.iclr.cc/paper_files/paper/2026/hash/5b175f9e93873e3a10a6ce43dbb82e05-Abstract-Conference.html)，§4.6

WALT确实给出**工具级原目标**：`min [FailRate(u,I_test) + StepCount(u) + AgenticRatio(u)]`。u为工具，I_test为测试输入；三项分别为测试失败率、primitive动作数、需要LLM推理的步骤比例。原文直接相加而未给统一单位的归一化权重，实现为演示、生成、优化、测试的循环，不能称为美元成本的精确最优解。§3.4的实例先实际搜索并观察URL，再归纳查询/分类参数，生成带类型的schema，用多组输入执行，失败时修正参数、定位和实现。作者在结论将长期在线tool patching列为未来方向；运行时fallback并不等于已经验证了持续工具库修复。[21](https://proceedings.iclr.cc/paper_files/paper/2026/hash/5b175f9e93873e3a10a6ce43dbb82e05-Abstract-Conference.html)，§§3.3–3.4、结论

MobileGPT也是直接先例：预探索应用并建立页面、子任务和动作记忆，后续可匹配动作直接复用，失配时调用模型适配；高层规划和参数填充仍可能调用模型。其八应用80任务消融中，warm-start相对Derive基线平均延迟减62.5%、API费用减68.8%；但冷启动略增成本，且该消融在冷启动失败后由人修复路径。它证明条件复用可能有大收益，不能被描述成完全自主学习后自然达到同样收益。[18](https://arxiv.org/pdf/2312.03003v3)，§7.3

MobileGPT没有给统一的时间损失函数，问题通过**图结构和适配协议**定义：节点对应页面可提供的子任务，边对应动作序列，执行前检查关键UI属性。原文§5.1把`click(index=5)`先转为按元素属性找联系人Bob，再参数化为`contact_name`；新任务绑定Alice时，重新定位当前页面元素，不沿用旧索引。匹配失败进入LLM适配，历史示例可以包含人的纠正。作者自述图像型、缺乏文本表示的界面和跨应用任务仍有限制。[18](https://arxiv.org/pdf/2312.03003v3)，§§4–5、9

ActionEngine用离线crawler构建状态机记忆，在线据此生成并执行程序。最新v2在四个WebArena域655题、同Claude Opus4.6比较中，成功率82.7%到91.2%，平均延迟87到27秒，估算API费0.40到0.05美元每题，属于这里最直接的时间与费用证据。[22](https://arxiv.org/pdf/2602.20502v2)，Table1、§5.2 Fig4

但主实验在初始探索后，使用每个任务模板的一个生成实例做warm-up，正式评测关闭Patcher；初始知识的成功率73.1%，精炼后91.2%。所以不能说完全任务无关探索直接取得主结果，也不能以此证明在线维护期间依然保持同样加速。作者报告各域36–260分钟、11.6–37.2美元的crawling成本与回本估计，但warm-up是否全包含不够清晰；8倍费用下降还受缓存定价影响。[22](https://arxiv.org/pdf/2602.20502v2)，§5.1–5.3、Table2

ActionEngine的**原结构**是`M=(S,O,T)`：S为稳定页面模板，O为带参数、来源/目标页面、实现和输出schema的操作，T为转移关系。它保存获取实时数据的方法，不是把历史数据当答案。探索还探查搜索的exact/fuzzy/prefix语义与分页行为；编译器插入连接前后操作的导航路径。Patcher可区分本题程序错误和需要持久修改的通用环境知识，但主实验没有开启它。作者的失败分析给出关键词与实际标题不匹配的例子：提前生成整段程序减少模型决策，也可能失去“先看搜索结果再改查询”的适应机会。[22](https://arxiv.org/pdf/2602.20502v2)，§§3–4、AppA.2及失败分析

探索并不一定要立即产代码。DRAFT先实际调用陌生工具，把参数和返回规律写入更准确的文档，再供固定Agent使用；它主要改善正确工具使用，没有证明净时间收益。这个轻量对照可以帮助我们判断，程序化执行究竟比正确的环境说明多带来多少价值。[27](https://arxiv.org/pdf/2410.08197v2)，§3–4

用户所问的ALITA则按任务能力缺口搜索库、生成脚本、配置环境，再包装为MCP工具。GAIA上另一Agent复用其工具时，GPT-4o成功率27.88%到33.94%；主比较的工具库重置与单独复用实验需区分。它展示了能力扩展和工具复用，但没有对应的执行延迟与完整学习费用证据，不能凭“工具可复用”推导出已加速。[28](https://arxiv.org/pdf/2505.20286v1)，§3、§5.1 Table2

LATM更早就提出强模型一次制作工具、较便宜模型反复调用以摊薄服务成本。主要实验为算法与推理任务，不是长期网页操作；不过“一次投入、以后复用”的经济逻辑已经非常明确，我们需要增加的是目标环境下的实测边界。[37](https://arxiv.org/pdf/2305.17126v2)，§2–3

### 探索策略知识与环境预测模型是不同路线

GLoW维护一组有价值的历史轨迹，在全局选择值得继续探索的状态，再通过动作重放返回；局部从同一起点比较几条路径，形成解释哪些动作有效的文字反思。它将“去哪里探索”与“到那里怎么行动”分开，是我们第二个方向有价值的方法参考。[10](https://arxiv.org/pdf/2509.24116v2)，§3

其**原式(1)–(3)**用`v(τ)=max_t Σ_(j≤t) r_j`衡量轨迹的最大前缀累计奖励，保留top-k轨迹档案；全局LLM据此生成状态的已达价值与未来潜力，局部反思生成哪些动作有利的文字建议。τ为轨迹，r_j为第j步环境奖励。作者借`A(s,a)=Q(s,a)−V(s)`解释同起点多路径比较的直觉，但实际输出是文本动作优势，不是用数值优势训练策略。它没有显式下一观察预测器，潜力也不是实算的UCB统计置信上界。[10](https://arxiv.org/pdf/2509.24116v2)，§§3.1–3.2

Jericho实验中同类LLM基线都有1,000次环境交互预算；GPT-4.1-mini在Zork1预算内最高游戏分数的三次运行均值，GLoW为73.0、ICRL为51.7。但所谓100–800倍效率指相对部分RL方法的环境样本预算差，不是省这么多API费或时间。附录给LLM方法每1,000步约4–6美元，费用差较小；环境还允许返回状态并提供有效动作接口。企业网页是否有同样可重置、可枚举的接口，需要重新验证。[10](https://arxiv.org/pdf/2509.24116v2)，Table1、AppC.1

WorldEvolver更接近“预测环境怎样响应操作”：episodic记忆记录真实的观察—动作—新观察，按动作相似度检索；semantic记忆利用预测与实测差异形成带证据分的规则，actor与world model权重均固定。需要注意具体实现：正文泛称textual heuristics，但附录Fig25的该实现的规则提取器只抽取**preservation rules，即执行动作时哪些事实不应改变**。Fig23另让真实转移示例提供“什么会变化”的类比。因此整体仍预测动作后果，不能反过来说它完全不学变化；也不能将语义分支夸大成已学齐一般因果规律和所有操作前置条件。[11](https://arxiv.org/pdf/2606.30639v2)，§3.2、AppE Figs22–25

其**原定义**是`M_E←M_E∪{(o_t,a_t,o_(t+1))}`，其中o为观察、a为动作；语义条目为`(rule,evidence)`，支持或矛盾会增减证据分，只有正分规则进入上下文。预测置信q是生成token概率的几何平均，低于阈值就不交给actor；q不是经保证的真实正确概率。算法先预测草案动作，actor据此重决策，若动作变化则重新预测实际动作再与实测比较。一个**本文说明例**是：检查杯子时预测它移动了，而实测未动，抽取“examine不改变位置”约束，后续继续按证据修正。这是提示中的预测约束，不是硬动作屏蔽或形式证明。[11](https://arxiv.org/pdf/2606.30639v2)，§3、Algorithm1、AppE

其收益并非全面。Table2中Gemma配ReAct在ScienceWorld由44.44%到52.22%，GPT-5.4-mini同列却由65.56%降到63.33%；而且这是每题五次尝试的best-of-5。算法还增加预测、重新决策，动作变化时可能再预测一次。它支持“环境知识能改善部分决策”，尚不支持“加一个world model就能加速”。另一个消融在每题前清空记忆、只保留该题多次尝试间记忆，表现仅下降0.5–1.1个百分点；不能把总收益全部归因于跨任务积累。附录也报告逐步调用和上下文开销，但没有给净执行加速。作者明确限定在两个文本环境，并指出置信估计依赖模型API提供概率信息。[11](https://arxiv.org/pdf/2606.30639v2)，§4.1、Table2、Limitations

### 我们应怎样理解探索的研究价值

以上工作已经超出简单保存轨迹，进入任务选择、状态表示、可执行技能和预测校正。因此“主动探索”本身同样不是空白。更具体的候选问题是：只对高频任务中影响复用安全性或速度的未知条件进行探测，能否比全量预探索、纯被动记忆或遇错即反思更划算？这里的条件可能是字段依赖、账号权限、页面分支、对象状态或API边界。

这只是待检验的问题。某些环境中根本没有足够重复任务，或者维护成本高于节省；此时最好的结论可能是停止构建更多技能。我们不预设一定需要完整状态图，也不预设文字规则必须升级为代码。

## 六 整体 Harness 自改进与我们的自动诊断

### 最接近 A 方向的已经有具体实现

HarnessFix将轨迹转为带依赖关系的中间表示，连接错误现象和harness代码位置，再用受限的修复操作修改系统并验证。它已比“把失败日志交给LLM自由改代码”更深入：我们若研究诊断，应与这样的结构化方法比较。GPT-5-mini在AppWorld的90题test集、三次独立运行平均成功率由36.7%到43.0%；其37.2M相对Meta-Harness74.6M的token，属于离线演化和修复阶段，不能说部署费减半。[29](https://arxiv.org/pdf/2606.06324v2)，§III、Tables3–4

StarHarness直接覆盖“环境经验转代码”：读取轨迹提出有边界的patch，先检查基本可运行性和局部修复，再由隐藏的selection集合择优。演化结果包括API schema修正、业务更新约定、日期财务计算、表格操作等。GPT-5.4在103个ITSM任务上，成功率23.3%到43.7%，turns每题18.12到9.87，估算API费1.23到0.58美元。但费用来自包括演化池的全基准，held-out另报成功率提升15.1个百分点，没有单独held-out费用和完整搜索回本账。[30](https://arxiv.org/pdf/2608.24804v1)，§3、Tables2、4

因此，自动归因、修改工具接口、固化确定性计算，都已有直接先例。我们可以研究“基于成本和条件证据的诊断能否比通用patch搜索更有效”，但不能仅以这几个组件同时出现作为创新。

从**问题定义**看，HarnessFix是有范围限制的补丁生成与验收：候选先符合修复规范和静态检查，再在验证任务上确认目标问题改善、回归不超限；它不是依靠对harness求导来更新。[29](https://arxiv.org/html/2606.06324v2)，§III-D。StarHarness原文式(1)写为`h* = argmax_{h∈H} J(h; D_holdout)`，h是harness、H是允许修改的空间，模型M固定，J是任务平均得分。作者虽把J称作cost function，紧接着明确其值越高越好，**这里不是美元成本函数**。留出结果在搜索时不可见，实际通过search与selection集合近似选择，holdout只做最终评价。[30](https://arxiv.org/html/2608.24804v1)，§3.1

### 在线持续改进有收益 也有明显边界

Adaptive Auto-Harness把学习与运行路由分开：从历史批次分析问题、调查、构建、验证，保留多个harness分支，再按任务选分支。FutureX中求解端每题耗时之和由34.2降到6.6小时，Pass@1从31.0%升至47.3%；同一论文PolyBench的时间却由25.6增到59.5小时。附录明确缺少evolver token和编排开销，这不是全流程墙钟时间或总费用。[31](https://arxiv.org/pdf/2606.01770v2)，§4、AppB Table5

Continual Harness让Actor与Refiner在不重置的长任务中修改提示、记忆、工具和代码。在Pokémon Emerald、Gemini3.1 Pro、每seed24小时设置下，from-scratch harness的中位API费用约130美元、里程碑完成100%，minimal约215美元、98%。这是有力的特定运行费用证据，但不是完成整个游戏时间减少40%；弱模型也可能无法利用复杂组件而退化。其基础接口还提供local text map等信息，不是只看裸截图。它的固定模型实验可以纳入本报告，后半涉及权重训练的分支则应分开。[32](https://arxiv.org/pdf/2605.09998v1)，§§4.3–4.4、Fig6

Live-SWE-agent在当前软件任务中按需创建脚本，说明无需先做庞大的离线系统搜索，也能出现自改进。GPT-5的成功率和平均费从65.0%/0.28美元到68.4%/0.27美元；Gemini3 Pro从74.2%/0.46到77.4%/0.48，费用并不一致下降。这些基线数字沿用既有报告，未全部在统一条件下重新运行；微小费用差不能作为严格受控的因果证据。它主要验证当前任务内的工具创建，还不能直接证明跨任务积累长期省钱。[33](https://arxiv.org/pdf/2511.13646v3)，Table1

### HGM 加快的是寻找好版本

用户幻灯片中的HGM从DGM的版本树出发，区分一个Agent当前做题能力和它产生更好后代的潜力。它利用后代成绩估计分支潜力，自适应决定继续扩展还是增加评估。SWE-bench Verified的60题设置中，用GPT-5扩展、GPT-5-mini做任务评估，同为800次评估，allocated CPU-hours从DGM的1,231降到HGM的517，best-belief成功率从53.3%到56.7%。2.38倍来自前两个CPU小时数字，不能解释成最终Agent每题快2.38倍。[34](https://arxiv.org/pdf/2510.21614v3)，§4.2、Table2

**HGM原文§3.2–3.3**把clade metaproductivity定义为：给定当前版本树T、节点a、搜索策略π和剩余预算B，继续搜索后，在a的后代分支中由评分选出的最佳版本，其真实效用U的期望。这里的“潜力”取决于搜索策略和预算，不能只由当前节点的成功率定义。实现中的近似为`CMP_hat(a)=n_success(C(a)) / [n_success(C(a))+n_fail(C(a))]`；C(a)含a及其后代，计数汇总这整个分支的任务评测成功与失败，再用于Thompson sampling分配扩展机会。它不是对未来最大收益的直接无偏测量；论文关于理想机器的理论条件也不等于实际系统具有全局最优保证。这是**改进搜索预算的分配机制**，并未把用户等待时间写入上述U的实际任务指标。[34](https://arxiv.org/pdf/2510.21614v3)

DGM则证明固定基础模型、修改自身代码并保留候选archive可以提升能力；作者也承认更强版本推理更贵。完整搜索还可能很昂贵。因此我们不宜一开始复制庞大进化树；先用受限修改和清楚的成本目标验证收益，得到足够证据后再决定复杂搜索是否值得。[35](https://arxiv.org/pdf/2505.22954v3)，§4、AppE.1

## 七 正确性评估决定加速结论能否成立

较少调用可能来自跳过必要步骤，较高得分也可能来自适应评测程序的缺口。若目标是按成文规则填写或更新结构化内容，最终结果、业务约束、必要确认和副作用应独立检查，不能让生成修改的Agent同时定义自己的成功条件。

AgentDevel已明确做pass→fail与fail→pass检查；StarHarness也有选择与留出流程。这说明验证门禁不是新的概念。与此同时，proposer看不到selection标签，并不意味着selection没有参与优化：只要多轮根据它接受候选，它就是开发过程的一部分，还需要未参与选择的最终评估。[30](https://arxiv.org/pdf/2608.24804v1)[36](https://arxiv.org/pdf/2601.04620v1)

AgentDevel的**原文式(1)–(2)**定义`P2F={x∈D_train: p_old(x)=1 且 p_new(x)=0}`与`F2P={x∈D_train: p_old(x)=0 且 p_new(x)=1}`；p是单个用例是否通过的指示量。这将“修好了多少”和“弄坏了多少”分开，而不是只看平均分。原方法的版本接纳是在同一开发集D_train上做，不能把这层门禁称为独立的最终测试。我们借鉴的是逐用例回归证据，仍需另设未来任务的验收。[36](https://arxiv.org/html/2601.04620v1)，§§2.1、2.4

VASO给出更具体的借鉴：把技能连接到形式规范，先检查规则是否自相矛盾，再验证生成计划，利用反例改善可复用契约。模型权重保持不变，全局规范固定。然而其命题映射由模型生成且没有被形式验证，保证依赖这个映射正确；当前只处理顺序执行技能。Table1中的97.2是手工映射的安全分，自动映射为96.8，不能说成自动系统97.2%的端到端任务正确率。[9](https://arxiv.org/pdf/2606.05395v1)，§§3–5、Table1、§7

我们的C方向可借鉴“把规范、观察映射和评分程序分开”，但不必强行把全部网页业务写成形式逻辑。第一轮可以从可执行的业务断言、环境真实状态检查和人工确认的小型评估集做起。关键是保留独立的最终标准；模型生成用例只是起点，人类和程序仍需核其覆盖与正确性。

VASO的**原文定义**可进一步说明这个边界。技能含全局规范G、局部目标ψ和可复用契约C；C包括把轨迹观察映射为原子命题的函数L以及文字计划模板。逻辑可行性检查问`是否存在轨迹σ，使 L(σ) 满足 G ∧ ψ`；一般计划验证问`A_plan ⊗ M 是否满足 G ∧ ψ`。A_plan是计划转成的状态系统，M是**预先给定**的环境动态模型，⊗表示组合，∧表示同时满足。作者的具体实现还使用直接检查计划状态系统的形式。因此它不是通过试错自动发现了所有环境规律：规范、环境模型、观察到命题的映射，各自可能是不同的误差来源。验证失败返回的反例可以指导改契约，但正确性保证仍以这些建模前提成立为条件。[9](https://arxiv.org/pdf/2606.05395v1)，§§3–4

### 造数据可以服务于免训练改进

数据生成是否属于本次范围，要看数据最后用来更新什么。生成示范后做SFT或RL更新模型权重，属于综述的基础模型分支，本报告不把它作为可直接采用的方法；生成任务、测试、反例后只修改提示、记忆或代码，则仍在范围内。后一类至少有三个具体用途。

第一是**生成探索任务和测试输入**。Voyager和SkillWeaver自主选择练习内容，SkillWeaver还给生成的API构造参数测试，再实际运行和修复。它产生的是技能学习和验收所需的交互数据，没有必要把这些数据训练进模型。[20](https://arxiv.org/pdf/2504.07079v1)，§§2.1–2.3；[26](https://arxiv.org/pdf/2305.16291v2)，§3。本文判断：自动出题可以降低任务编写成本，但练习分布可能偏向Agent已会完成的操作；生成参数也不保证覆盖权限、状态和边界条件。

第二是**生成有外部依据的代理测试**。OpenSkill将任务指令I、环境E和外部知识K用于构造skill集合S；构造时看不到最终测试T_GT。其原文式(2)–(4)为`S = f(I,E,K)`、`T_proxy = g(I,E,K_verify)`，代理分数是各条代理断言对执行结果的平均通过率。K_verify是文档参考值、数据不变量、标准格式等验证依据；g用隔离的LLM会话生成可执行断言。最终固定S后才用T_GT评价。这清楚地区分了“用代理信号改进”和“最终成功”：**作者明确承认**，代理测试与真实目标不一致时会奖励对代理的过拟合，并专门测量二者一致性。[25](https://arxiv.org/pdf/2606.06741v1)，§§2.1–2.2、4.2

第三是**生成真实失败的反例与回归用例**。VASO的模型检查器在给定规范和模型下给出违例轨迹，AgentDevel保留pass→fail与fail→pass比较；这些证据比让同一个LLM凭空给自己的输出打分更容易追查，但前者仍依赖模型和映射，后者仍依赖原测试的覆盖。[9](https://arxiv.org/pdf/2606.05395v1)，§4；[36](https://arxiv.org/pdf/2601.04620v1)，§3

对我们的实际含义是：先让数据生成支持两条主线，例如给高频操作生成新的参数组合、为怀疑的环境规则设计区分性实验、把真实失败转成回归用例；不必另起一个“造更多训练数据”的项目。必须分别记录用例生成成本、用例有效率、错误接受技能的比例，以及最终留出任务的表现。**生成器产出了很多测试，不等于反馈机制已经可靠；更高代理分数，也不等于业务正确性或净加速。**

### 哪些评测可以真正检验我们的假设

评测目录补筛后，最有用的不是再加一串benchmark名字，而是确定每个环境允许观察什么、什么状态能重置、何种反馈可供学习、最终怎样验收。综述描述的理想持续改进评测，并不意味着目录中每个基准都现成支持这种协议。

**第一轮主环境可从AppWorld、WorkArena、WebArena选一个。** AppWorld提供跨应用API、可恢复的数据库与时间，用状态差分检查必要变化及不应发生的额外变化；它还用同一scenario的全部实例通过来衡量稳健性。它适合隔离流程知识、程序技能和条件变化，但不能替代网页视觉定位问题。[42](https://aclanthology.org/2024.acl-long.850/)，§§2–3、评价附录。WorkArena更贴近企业网页操作，有参数化任务与运行中validate接口；反馈可能实时可见，必须固定是否提供、每次调用成本和任务清理协议，不能笼统假设所有学习信号都是隐藏终局标签。[43](https://proceedings.mlr.press/v235/drouin24a.html)，任务接口与评测设置。WebArena的自托管网站更易恢复状态，终局以功能是否满足来评价，但部分答案题使用LLM judge，也不是全题确定性评分。[44](https://arxiv.org/pdf/2307.13854v4)，§3、AppA.2

**规则遵守要另测。** ST-WebAgentBench把任务完成与轨迹中的策略合规分开，适合检验生成的宏是否跳过必要步骤。它的环境reset接口不能直接当作底层业务数据库已经完整回滚的证明；传回info的内容也不自动等于actor看到了这些反馈，接入时需要实测。它提供的是规则验收协议，本身不证明Agent已经学会未知环境规律。[45](https://arxiv.org/pdf/2410.06703v7)，任务/评价协议及配套代码

**探索机制最好有单独的可控测试。** DiscoveryWorld区分最终完成、有效实验操作与学到正确知识；默认基线不跨题保留知识，若研究经验积累，需要明确采用其seed/theme划分并添加持续记忆协议。[50](https://arxiv.org/pdf/2406.06769v2)，§§3–4。PhysGym通过控制物理规则先验，观察Agent怎样选择实验、提出规律，并提供明确的实验与oracle验证预算；可以减少靠已有常识猜中答案的混杂，但它测的是物理函数规律，不能替代有权限、不可逆操作和部分可见状态的企业流程。[51](https://arxiv.org/pdf/2507.15550v2)，§§3–4。DiscoveryWorld的知识评价、PhysGym的方程评价部分依赖LLM judge；PhysGym的oracle测试结果也会反馈给Agent，不能说成完全无答案反馈。这两类用于验证“怎样学”，主业务环境用于验证“学到后是否实际省资源”。

**静态轨迹和反馈预算曲线不等于在线持续改进。** Mind2Web逐步提供正确历史，Task SR衡量参考路径上的动作是否全部匹配；WebLINX主要对多轮示范做动作与文本匹配，它们适合组件和经验提取研究，不能代替真实在线终局成功。[46](https://arxiv.org/pdf/2306.06070v3)，§4；[47](https://proceedings.mlr.press/v235/lu24e.html)，§7。MINT适合测工具和语言反馈的利用，但原协议对不同交互预算分别从头运行，不是保存前一预算下的经验继续学习，不能把其曲线直接称为跨任务进化收益。[52](https://zihanwang314.github.io/pdf/mint.pdf)，§3

**后期再检验真实系统与费用口径。** OSWorld提供真实电脑环境与可执行检查，VM恢复不自动回滚远端账户；ClawBench包含真实网站操作，重置浏览器或客户端也不等于恢复网站服务器状态。ClawBench还拦截终端提交，其成功评分表示到达规定的拦截或等价终点，不能当作服务器已经完成真实业务写入的证明。两者能检验外部有效性，但第一轮容易混入界面漂移、网络与环境运行噪声。[48](https://arxiv.org/pdf/2404.07972v2)[49](https://arxiv.org/pdf/2604.08523v2)，各自环境与评价协议。AstaBench按固定价格快照、缓存费率和明确工具权限比较质量与费用，这些口径值得借鉴；标准化费用仍不是实际账单，也不包含我们全部探索、构造和维护成本，不能直接当生命周期回本。[53](https://arxiv.org/pdf/2510.21652v2)，§4

采用任何基准前，先做一次小规模协议检查：相同起始状态能否恢复；学习器究竟能看见哪些反馈；最终判分是否覆盖无关副作用；baseline与改进版的观察和权限是否一致。已有AppWorld等已经使用条件变化和副作用检查，所以“增加条件测试”本身也不是新贡献。我们要验证的是特定学习机制在这些约束下的净收益。

## 八 现有工作已经做到什么程度

下面按对我们计划的帮助整理，不按跨数据集的百分比排名。不同模型、工具权限、任务难度和学习预算使那些百分比无法直接比较。

| 要验证的环节 | 最直接的近邻 | 已建立的证据 | 仍需我们测什么 |
|---|---|---|---|
| 从历史轨迹改程序技能 | SpeedRunner、ASI | 技能归纳、编辑、接纳；部分含学习摊销 | 业务规则、状态变化、维护后的净收益 |
| 文字经验何时变代码 | Metis、AWM | 复用门槛与混合表示；宏也可退化 | 条件证据、失效检测及恢复的价值 |
| 探索环境以减少在线决策 | WALT、SkillWeaver、MobileGPT | 自动操作发现、验证、重放 | 探索投入与真实复用率，人工介入比例 |
| 环境记忆支持程序执行 | ActionEngine | 受控网页中的秒数与美元改善 | 无模板预热、新组合和持续变化 |
| 轨迹诊断到代码修复 | HarnessFix、StarHarness | 结构化修复、工具接口演化 | 定向诊断是否优于通用搜索 |
| 自动持续改进 | Adaptive、Continual Harness | 部分任务流的成本改善 | 弱模型、其他域和完整改进账 |
| 策略记忆及选择 | ReasoningBank、MemRL、SEDM | 少步数、效用学习、接纳机制 | 少步数能否抵消更长上下文与评估 |
| 独立验收 | OpenSkill、VASO、AgentDevel | 外部锚点、反例、回归检查 | 误接纳率、业务语义、测试泄露与费用 |

最值得警惕的不是“完全没有相关工作”，而是把已知机制重新组合后，只与很弱的无记忆baseline比较。相反，如果相同轨迹、相同模型、相同权限和预算下，我们能说明某种条件表示或探测策略何时有效、何时无效，并通过留出和变化任务流验证净收益，这才会增加有用的研究证据。

当前文献已经部分解决摊销、回退、轨迹验证和跨环境迁移，不能一概称它们空白。我们发现的是证据还不统一：有的缺全成本，有的依赖同题复用，有的缺动态环境，有的只报能力提升。研究空间必须落实到目标任务、最接近方法及具体尚未验证的组合条件，而不是把别人的未报告项自动宣布为新贡献。

## 九 对下一步研究计划的具体建议

### 把研究问题缩到能够被否证

建议保留两条线，但先集中验证一个交点：**从有限历史轨迹提取带适用条件的操作，按预期净收益决定继续使用文字、生成代码，还是补做环境探测。** 这只是候选研究问题；已有Metis的多层经验与代码、SpeedRunner的技能归纳和摊销、WALT的工具验证、StarHarness的代码修复，都是必须正面对比的近邻。

我们可以把差异落实为两个可检验假设。H1：同样历史记录和改进预算下，显式记录操作适用条件并在不匹配时回退，比直接生成技能库更能保住新组合任务和状态变化后的正确性。H2：按未来复用收益选择少量探测，比固定探索预算或遇错即探索获得更好的累计费用和完成时间。这两点仍可能已被其他工作部分覆盖；实验前需要针对选定实现再查代码和引用链，不能提前宣称首创。

尤其H1不能只对比“完全没有条件检查”的稻草人：SkillWeaver的docstring已记录前置状态，MobileGPT已有适用性检查，SpeedRunner技能会加入guard与恢复。真正可比较的是条件来自什么证据、如何更新、检查覆盖与开销如何，以及它们在环境变化后是否仍划算。“带条件”这三个字本身不是区别。[20](https://arxiv.org/pdf/2504.07079v1)，§2.2；[18](https://arxiv.org/pdf/2312.03003v3)，§§4–5；[23](https://arxiv.org/pdf/2608.11338v1)，AppI

### 先用相同信息比较经验应存成什么

第一阶段固定基础模型、工具权限、可见观察和任务预算，准备可重置、有业务规则的重复工作流。将开发轨迹、候选选择用例、最终测试分开，并按任务模板或操作组合划分，而不只是随机换几个参数。相同任务的重复实例可以研究摊销，但需要与真正未见的组合、状态变化另报。

| 对照 | 保留什么 | 要回答的问题 |
|---|---|---|
| 不学习 | 固定prompt和工具 | 原有耗时、费用与失败在哪里 |
| 文字经验 | 同一批轨迹提炼的规则或流程 | 仅提供知识是否已经足够 |
| 程序技能 | 同一批轨迹生成并验证代码 | 省掉模型决策是否抵消构造与维护 |
| 条件技能与定向探测 | 增加适用条件、触发回退及少量探测 | 这些机制是否有额外净收益 |

为分别检验H1和H2，保留基线已有guard和回退，在同一技能库上比较是否增加由新证据维护的显式条件检查；关闭新增检查只作为消融，并另与完整近邻方法比较。随后在相同检查机制下比较固定预算探索与收益导向探索，避免把全部新增组件的效果混在一起。

对于A方向另设一个小规模诊断实验：同一组成功但昂贵、以及失败的轨迹，比较自由修改、结构化故障定位、按成本和频次定位。每次只允许有限类修改，记录“诊断是否准确”和“修改是否带来实际收益”；二者不要混为一项。人工分析可作为小样本上界，不能假装零人工成本。

### 先验证已有方法 再检验差异化假设

第一组实验应当被明确称为**已有机制的复现或迁移验证**：轨迹文字记忆参考AWM/ReasoningBank，文字到代码参考Metis，直接程序技能参考SpeedRunner/ASI，环境先验参考DRAFT或MobileGPT/ActionEngine，受限harness修改参考HarnessFix/StarHarness。优先从能保持模型、权限、输入和预算一致的实现中选代表；不要求一次复现全部方法，也不应自行弱化baseline后沿用其论文名称。若只实现某一机制，应称“受某文启发的对照”。

第二组是**目标场景下的证据补充**：任务重复度变化、参数与状态组合变化、规则更新后维护、冷启动到回本的累计账。这些实验可能已有相邻先例，价值在于验证目标业务条件下是否成立；不能因为别人的论文没有报告我们的某张表，就宣布发现了新机制。

第三组才是**候选方法假设**：H1的显式条件检查、H2的收益导向探测，以及成本与失败频次共同引导的故障定位。接受为研究贡献之前，必须同时满足：与最接近方法的区别可明确实现；新增组件的消融有收益；收益能在留出或变化任务中保留；建设与验证代价没有吞掉节省。目前这些只是值得检验的问题，尚未建立新颖性。

### 两条主线之外还值得试什么

**经验选择与删除**可以先于更复杂的技能生成。MemRL区分语义相似与奖励效用，SEDM已有成本敏感的接纳与删除；若大部分开销来自读入过多历史，可以固定已有经验集合，只比较检索、压缩和淘汰，检验有多少收益不需要再造工具。[16](https://arxiv.org/pdf/2601.03192v2)[39](https://arxiv.org/abs/2509.09498v3)

**改进搜索与验证预算分配**适合另一种瓶颈：如果寻找好版本本身很贵，而上线后的收益已有证据，可比较GEPA式小批过滤、HGM式自适应评估，以及固定预算候选比较。其目标是降低研发/适配成本，必须单列结果，不与最终执行加速混用。[4](https://arxiv.org/pdf/2507.19457v2)[34](https://arxiv.org/pdf/2510.21614v3)

**工具说明与固定执行结构的修正**是更轻的起点。DRAFT通过交互澄清陌生工具语义，StarHarness修正接口和确定性计算；可能仅改善schema、缩短观察、直接调用已有API就足够，不一定需要长期记忆或自演化循环。[27](https://arxiv.org/pdf/2410.08197v2)[30](https://arxiv.org/pdf/2608.24804v1)若目标瓶颈是网络等待或独立操作串行，则还应做普通缓存和并行对照；这是系统优化方向，不能用上述文献的成功率为其效果背书。

这里所谓“稳妥”，是指机制已有多个独立工作支持、对照容易搭建、失败也能产生清楚结论；不是文献数量上的流行度统计，更不是保证会在我们的任务上加速。按当前证据，先做文字记忆、程序技能和轻量环境说明的受控比较，比一开始启动完整自演化框架更便于判断投入产出。

### 评价同时保留三份账

构造账包括生成历史轨迹、额外探索、反思、写工具与依赖准备；选择账包括候选比较、回归测试和被拒绝修改；执行账包括检索、技能匹配、常规模型调用、环境开销和失败回退。维护成本另列，不计入构造账，以便统计环境变化的代价。历史轨迹如果是既有业务自然产生，可以另报“已有日志可用”的增量场景，但不能把它与从零生成日志的场景混在一起。

下面是本报告的核算定义，不是某篇论文的公式：

可先把选择问题写为：`最小化系统在任务流上的总费用 Cost_total(Σ)`，约束为`Quality(Σ) ≥ Quality(Σ_base) − ε`及`Latency_p95(Σ) ≤ L_limit`。Σ是可修改的外部系统，Σ_base是基线，Quality由预先固定的业务标准评定，ε是预先约定的可接受差异，L_limit是时延要求。费用、时延和质量都在相同任务流、固定模型与权限下测量；ε与L_limit需要实验前确定，不能看结果后调整。如果还没有业务阈值，就先报告质量、时间、费用的联合比较，不把不同单位随意相加为一个“效率分”。

`累计净节省(N) = Σ[基线任务成本 − 改进系统任务成本] − 构造成本 − 选择成本 − 维护成本`

公式的任务成本不含另行列出的构造、选择和维护，以免重复计费；任务成本包含规定预算内所有成功与失败尝试，使用同一批任务流和统一计费方式。若平均执行节省为正且近似稳定，可用 `固定投入 ÷ 平均每任务净节省` 估算回本任务量；若差为零或负，则该条件下不存在有限回本点。WALT将构造费除以基线任务费的估计需要进一步扣除新工具的执行边际成本，不能照抄为净回本。[21](https://proceedings.iclr.cc/paper_files/paper/2026/hash/5b175f9e93873e3a10a6ce43dbb82e05-Abstract-Conference.html)

时间不能简单套金额公式：后台构造可能不在单任务等待路径上，却仍占用资源。分别报用户可见完成时间、端到端实验工期和累计计算/环境占用。部署报告至少保留正确性、p50/p95延迟、每任务费用、全部尝试的总费用与成功数、模型调用、输入/输出/缓存token、工具及环境时间。步数只是解释机制的中间量。

正确性以预先写明的业务检查为门槛，结合置信区间和失败类型，不以一次样本分数“刚好没下降”宣布无退化。先冻结评测规则，再运行学习。冻结产物的held-out实验不允许再用测试反馈调候选；在线任务流则采用先评分、后更新的时间顺序，允许利用已经发生的可见执行反馈，未来任务和隐藏评分依据不向学习器泄露。任务流实验应额外报告学习前期亏损、回本区间，以及环境变化后修复所需的时间和费用。

### 哪些结果会改变我们的方向

如果文字经验已取得大部分收益，代码技能没有额外净节省，就先研究记忆选择与压缩。如果代码只在完全重复任务有效，新参数或状态变化就失败，应研究适用条件和恢复，而不是继续堆技能。如果跨任务重复度低、改进成本收不回来，应保留固定Agent，转向普通系统优化。只有当多轮候选搜索成为主要瓶颈，HGM式预算分配或更复杂的外层优化才值得引入。

因此第一轮最有价值的产出未必是一个更复杂的新Agent，而可能是一张经过实验得到的边界图：任务重复度、状态稳定性、技能覆盖率与构造成本在什么范围内，经验复用确实更划算。这种结论也必须与SpeedRunner等已将学习费用摊入每轨迹成本的工作比较，强调我们的任务条件和受控对照提供了什么额外证据。

## 十 最后再接回我们关于慢与贵的分析

可执行技能最直接减少串行的模型决策次数；环境规则和可靠观察可以减少试错与失败重跑；记忆检索可能减少重新搜索，却增加每次读入的上下文；harness修复可以减少无效工具调用，也可能增加路由、验证或反思。探索和进化则主要新增前期以及维护投入。

这能与已有Time和Money框架对应，但分类不必强行一一匹配。一个机制可能同时改变多个量，方向也可能相反。我们应先用实验判断它在具体工作流里改变了什么，再用原有框架解释收益来源。模型服务层的缓存、并行与推理优化仍然重要，但它们不需要持续学习，也不能由self-evolution论文替代。

对第三阶段草稿的建议是保留A的自动诊断、B的环境经验和C的独立验收，将主张改成“固定模型下、面向重复业务工作流的条件复用与净收益验证”。删除或降低“尚未有人做过这类自动循环”的表述；也不要把无权重方法统一定义成与强化学习无关，因为记忆效用更新等方法会采用非神经参数的奖励学习。当前证据足以支持开始做受控验证，尚不足以承诺新颖性、普遍加速比例或实际回本时间。

## 参考文献

这些条目对应正文实际讨论的论文。正式发表信息与所读预印本版本分开注明；没有确认录用的工作按预印本引用。作者表完整保留，链接指向原始来源。

[1] Zhe Ren; Yimeng Chen; Dandan Guo; Guowei Rong; Tonghui Li; R.B. Xiong; Qingfeng Lan; Wenyi Wang; Li Nanbo; Yibo Yang; Mingchen Zhuge; Jürgen Schmidhuber. **Self-Improvements in Modern Agentic Systems: A Survey.** 2026. arXiv:2607.13104v1，2026-07-14. [原文](https://arxiv.org/pdf/2607.13104v1)。配套[文献集合](https://selfimproving-agent.github.io/#overview)，本次快照2026-09-30。

[2] Mert Yuksekgonul; Federico Bianchi; Joseph Boen; Sheng Liu; Pan Lu; Zhi Huang; Carlos Guestrin; James Zou. **Optimizing generative AI by backpropagating language model feedback.** Nature 639:609–616, 2025. DOI:10.1038/s41586-025-08661-4. [正式论文](https://www.nature.com/articles/s41586-025-08661-4)。方法亦核原始预印本 *TextGrad: Automatic “Differentiation” via Text*, arXiv:2406.07496v1，2024；正式题名与作者表有所更新。

[3] Ching-An Cheng, Allen Nie, Adith Swaminathan. Trace is the Next AutoDiff: Generative Optimization with Rich Feedback, Execution Traces, and LLMs. NeurIPS, 2024. arXiv:2406.16218v2. [原文](https://arxiv.org/abs/2406.16218v2)

[4] Lakshya A. Agrawal, Shangyin Tan, Dilara Soylu, Noah Ziems, Rishi Khare, Krista Opsahl-Ong, Arnav Singhvi, Herumb Shandilya, Michael J. Ryan, Meng Jiang, Christopher Potts, Koushik Sen, Alexandros G. Dimakis, Ion Stoica, Dan Klein, Matei Zaharia, Omar Khattab. GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning. ICLR, 2026. arXiv:2507.19457v2. [原文](https://arxiv.org/abs/2507.19457v2)

[5] Yifan Yang, Ziyang Gong, Weiquan Huang, Qihao Yang, Ziwei Zhou, Zisu Huang, Yan Li, Xuemei Gao, Qi Dai, Bei Liu, Kai Qiu, Yuqing Yang, Dongdong Chen, Xue Yang, Chong Luo. SkillOpt: Executive Strategy for Self-Evolving Agent Skills. 2026. arXiv:2605.23904v2. [原文](https://arxiv.org/abs/2605.23904v2)

[6] Qizheng Zhang, Changran Hu, Shubhangi Upasani, Boyuan Ma, Fenglu Hong, Vamsidhar Kamanuru, Jay Rainton, Chen Wu, Mengmeng Ji, Hanchen Li, Urmish Thakker, James Zou, Kunle Olukotun. Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models. ICLR, 2026. arXiv:2510.04618v3. [原文](https://arxiv.org/abs/2510.04618v3)

[7] Zhanzhi Lou, Hui Chen, Yibo Li, Qian Wang, Bryan Hooi. Meta-TTL: Meta-Learning Self-Improvement Policies for Language Agents. 2026. arXiv:2604.00830v4. [原文](https://arxiv.org/abs/2604.00830v4)

[8] Igor Bogdanov, Chung-Horng Lung, Thomas Kunz, Jie Gao, Adrian Taylor, Marzia Zaman. FORGE: Self-Evolving Agent Memory With No Weight Updates via Population Broadcast. ACM Conference on AI and Agentic Systems, 2026. DOI:10.1145/3786335.3813155. [原文](https://arxiv.org/abs/2605.16233v1)

[9] Yunhao Yang, Neel P. Bhatt, Kevin Wang, Samuel Tetteh, Zhangyang Wang, Ufuk Topcu. VASO: Formally Verifiable Self-Evolving Skills for Physical AI Agents. 2026. arXiv:2606.05395v1. [原文](https://arxiv.org/abs/2606.05395v1)

[10] Minsoo Kim, Seung-won Hwang. Dual-Scale World Models for LLM Agents Towards Hard-Exploration Problems. 2025. arXiv:2509.24116v2. [原文](https://arxiv.org/abs/2509.24116v2)

[11] Xuan Zhang, Wenxuan Zhang, See-Kiong Ng, Yang Deng. Self-Evolving World Models for LLM Agent Planning. 2026. arXiv:2606.30639v2. [原文](https://arxiv.org/abs/2606.30639v2)

[12] Wujiang Xu; Zujie Liang; Kai Mei; Hang Gao; Juntao Tan; Yongfeng Zhang. **A-Mem: Agentic Memory for LLM Agents.** Advances in Neural Information Processing Systems 38, 2025. DOI:10.52202/085713-0593. [正式论文](https://proceedings.neurips.cc/paper_files/paper/2025/hash/19909c36f51abc4856b4560aff3d36d6-Abstract-Conference.html)。本轮所读为该会议版。

[13] Zora Zhiruo Wang; Jiayuan Mao; Daniel Fried; Graham Neubig. **Agent Workflow Memory**. ICML 2025, Proceedings of Machine Learning Research 267:63897–63911. 所读/核查版本：正式PMLR版；另查arXiv:2409.07429v1. [来源](https://proceedings.mlr.press/v267/wang25bx.html)。

[14] Siru Ouyang; Jun Yan; I-Hung Hsu; Yanfei Chen; Ke Jiang; Zifeng Wang; Rujun Han; Long T. Le; Samira Daruki; Xiangru Tang; Vishy Tirumalashetty; George Lee; Mahsan Rofouei; Hangfei Lin; Jiawei Han; Chen-Yu Lee; Tomas Pfister. **ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory**. 预印本（2025）. 所读/核查版本：arXiv:2509.25140v2. [来源](https://arxiv.org/abs/2509.25140)。

[15] Andrew Zhao; Daniel Huang; Quentin Xu; Matthieu Lin; Yong-Jin Liu; Gao Huang. **ExpeL: LLM Agents Are Experiential Learners**. Proceedings of the AAAI Conference on Artificial Intelligence 38(17):19632–19642, 2024. 所读/核查版本：arXiv:2308.10144v3. [来源](https://arxiv.org/abs/2308.10144)。[正式 DOI](https://doi.org/10.1609/aaai.v38i17.29936)

[16] Shengtao Zhang; Jiaqian Wang; Ruiwen Zhou; Junwei Liao; Yuchen Feng; Zhuo Li; Yujie Zheng; Weinan Zhang; Ying Wen; Zhiyu Li; Feiyu Xiong; Yutao Qi; Bo Tang; Muning Wen. **MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory**. 预印本（2026）. 所读/核查版本：arXiv:2601.03192v2. [来源](https://arxiv.org/abs/2601.03192)。

[17] Zijie Dai; Siuhin He; Hui Li; Qihui Zhou; Jiajun Li; Mingcong Song; Guoping Long; Hongjie Si; Xin Yao; Lin Zhang; James Cheng; Xiao Yan. **Metis: Bridging Text and Code Memory for Self-Evolving Agents**. 预印本（2026）. 所读/核查版本：arXiv:2606.24151v1. [来源](https://arxiv.org/abs/2606.24151)。

[18] Sunjae Lee; Junyoung Choi; Jungjae Lee; Munim Hasan Wasi; Hojun Choi; Steven Y. Ko; Sangeun Oh; Insik Shin. **MobileGPT: Augmenting LLM with Human-like App Memory for Mobile Task Automation**. ACM MobiCom 2024. 所读/核查版本：arXiv:2312.03003v3. [来源](https://arxiv.org/abs/2312.03003)。目录/abs仍保留早期标题 Explore, Select, Derive, and Recall；实际PDF正文为正式标题。

[19] Zora Zhiruo Wang, Apurva Gandhi, Graham Neubig, and Daniel Fried. 2025. *Inducing Programmatic Skills for Agentic Tasks*. **COLM 2025**. arXiv:2504.06821, **v2**. [PDF](https://arxiv.org/pdf/2504.06821v2); [OpenReview](https://openreview.net/forum?id=lsAY6fWsog).

[20] Boyuan Zheng, Michael Y. Fatemi, Xiaolong Jin, Zora Zhiruo Wang, Apurva Gandhi, Yueqi Song, Yu Gu, Jayanth Srinivasa, Gaowen Liu, Graham Neubig, and Yu Su. 2025. *SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills*. arXiv:2504.07079, **v1**. 本文未独立核实最终发表 venue；OSU/UVA/Purdue/CMU/Cisco Research. [PDF](https://arxiv.org/pdf/2504.07079v1).

[21] Viraj Prabhu, Yutong Dai, Matthew Fernandez, Krithika Ramakrishnan, Jing Gu, Yanqi Luo, Silvio Savarese, Caiming Xiong, Junnan Li, Zeyuan Chen, and Ran Xu. 2026. *WALT: Web Agents that Learn Tools*. **ICLR 2026**. 实读会议 camera-ready PDF，非旧 arXiv:2510.01524v1；正式 proceedings 核实 venue。[正式论文页及 PDF 入口](https://proceedings.iclr.cc/paper_files/paper/2026/hash/5b175f9e93873e3a10a6ce43dbb82e05-Abstract-Conference.html).

[22] Hongbin Zhong, Fazle Faisal, Luis França, Tanakorn Leesatapornwongsa, Adriana Szekeres, Kexin Rong, and Suman Nath. 2026. *ActionEngine: From Reactive to Programmatic Web Agents via State Machine Memory*. arXiv:2602.20502, **v2, September 28, 2026**. Georgia Tech/Microsoft；本文按预印本补充。[PDF](https://arxiv.org/pdf/2602.20502v2).

[23] Zixi Huang, Xiheng Wang, Andrew Wang, William Jurayj, Bernal Jiménez Gutiérrez, Daniel Khashabi, and Nicholas Andrews. 2026. *Better, Faster, Stronger: Programmatic Skill Learning Best Reduces Agent Cost*. arXiv:2608.11338, **v1**. Johns Hopkins University；预印本，方法名 SpeedRunner。[PDF](https://arxiv.org/pdf/2608.11338v1).

[24] Huawei Lin, Peng Li, Jie Song, Fuxin Jiang, and Tieying Zhang. 2026. *MUSE-Autoskill: Self-Evolving Agents via Skill Creation, Memory, Management, and Evaluation*. arXiv:2605.27366, **v2**（实读 PDF 首页日期 July 7, 2026；不要用原始 arXiv 编号月份代替本版本日期）。ByteDance/Rochester Institute of Technology；预印本补充。[PDF](https://arxiv.org/pdf/2605.27366v2).

[25] Zhiling Yan, Dingjie Song, Hanrong Zhang, Wei Liang, Yuxuan Zhang, Yutong Dai, Lifang He, Philip S. Yu, Ran Xu, Xiang Li, and Lichao Sun. 2026. *OpenSkill: Open-World Self-Evolution for LLM Agents*. arXiv:2606.06741, **v1**. Lehigh/UIC/UBC/Vector/Salesforce/Harvard 等；预印本补充。[PDF](https://arxiv.org/pdf/2606.06741v1).

[26] Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi “Jim” Fan, and Anima Anandkumar. 2024. *Voyager: An Open-Ended Embodied Agent with Large Language Models*. **Transactions on Machine Learning Research (TMLR)**. 实读 arXiv:2305.16291, **v2 (2023)**；会议/期刊最终版与实读版本区分。[PDF](https://arxiv.org/pdf/2305.16291v2); [OpenReview](https://openreview.net/forum?id=ehfRiF0R3a).

[27] Changle Qu, Sunhao Dai, Xiaochi Wei, Hengyi Cai, Shuaiqiang Wang, Dawei Yin, Jun Xu, and Ji-Rong Wen. 2025. *From Exploration to Mastery: Enabling LLMs to Master Tools via Self-Driven Interactions*. **ICLR 2025**. arXiv:2410.08197, **v2**；方法 DRAFT。[PDF](https://arxiv.org/pdf/2410.08197v2); [会议 PDF](https://openreview.net/pdf?id=QKBu1BOAwd).

[28] Jiahao Qiu; Xuan Qi; Tongcheng Zhang; Xinzhe Juan; Jiacheng Guo; Yifu Lu; Yimin Wang; Zixin Yao; Qihan Ren; Xun Jiang; Xing Zhou; Dongrui Liu; Ling Yang; Yue Wu; Kaixuan Huang; Shilong Liu; Hongru Wang; Mengdi Wang. **Alita: Generalist Agent Enabling Scalable Agentic Reasoning with Minimal Predefinition and Maximal Self-Evolution.** 2025. arXiv:2505.20286v1，2025-05-26. [原文](https://arxiv.org/pdf/2505.20286v1)。按实际阅读的预印本版本引用。

[29] Mengzhuo Chen; Junjie Wang; Zhe Liu; Yawen Wang; Haiming Zheng; Qing Wang. **From Failed Trajectories to Reliable LLM Agents: Diagnosing and Repairing Harness Flaws.** ISCAS/UCAS/Tianjin University preprint,2026. 实读[arXiv2606.06324v2](https://arxiv.org/pdf/2606.06324v2)，2026-07-02，13页；方法名HarnessFix。

[30] Esakkivel Esakkiraja; Denis Akhiyarov; Vikas Yadav; Sai Rajeswar; Patrice Bechard; Sridhar Nemala; Sagar Davasam. **StarHarness: Evolving Harnesses with Stratified Search for Enterprise Environments.** ServiceNow/Mila/Université de Montréal preprint,2026. 实读[arXiv2608.24804v1](https://arxiv.org/pdf/2608.24804v1)，2026-08-25，10页。

[31] Zewen Liu; Zhan Shi; Yisi Sang; Bing He; Minhua Lin; Tianxin Wei; Dakuo Wang; Benoit Dumoulin; Wei Jin; Hanqing Lu. **Adaptive Auto-Harness: Sustained Self-Improvement for Agentic System Deployment on Open-Ended Task Streams.** Emory/Amazon/Penn State/UIUC/Northeastern preprint,2026. 实读[arXiv2606.01770v2](https://arxiv.org/pdf/2606.01770v2)，2026-06-03，23页。

[32] Seth Karten; Joel Zhang; Tersoo Upaa Jr; Ruirong Feng; Wenzhe Li; Chengshuai Shi; Chi Jin; Kiran Vodrahalli. **Continual Harness: Online Adaptation for Self-Improving Foundation Agents.** Princeton/ARISE Foundation/Google DeepMind preprint,2026. 实读[arXiv2605.09998v1](https://arxiv.org/pdf/2605.09998v1)，2026-05-11，28页。本文保留固定FM实验，排除其模型训练分支。

[33] Chunqiu Steven Xia; Zhe Wang; Yan Yang; Yuxiang Wei; Lingming Zhang. **Live-SWE-agent: Can Software Engineering Agents Self-Evolve on the Fly?** UIUC preprint,2025. 实读[arXiv2511.13646v3](https://arxiv.org/pdf/2511.13646v3)，2025-11-24，20页。

[34] Wenyi Wang; Piotr Piękos; Li Nanbo; Firas Laakom; Yimeng Chen; Mateusz Ostaszewski; Mingchen Zhuge; Jürgen Schmidhuber. **Huxley-Gödel Machine: Human-Level Coding Agent Development by an Approximation of the Optimal Self-Improving Machine.** ICLR2026，[官方paper list](https://iclr.cc/virtual/2026/papers.html)。实读[arXiv2510.21614v3](https://arxiv.org/pdf/2510.21614v3)，2025-10-29，30页；未把会议版与该预印本假定逐字相同。

[35] Jenny Zhang; Shengran Hu; Cong Lu; Robert Lange; Jeff Clune. **Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents.** ICLR2026, main conference poster. [正式会议信息](https://iclr.cc/virtual/2026/poster/10007327)。实读[arXiv2505.22954v3](https://arxiv.org/pdf/2505.22954v3)，2026-03-12，72页。

[36] Di Zhang. **AgentDevel: Reframing Self-Evolving LLM Agents as Release Engineering.** Fudan University preprint,2026. 实读[arXiv2601.04620v1](https://arxiv.org/pdf/2601.04620v1)，2026-01-08，11页。

[37] Tianle Cai, Xuezhi Wang, Tengyu Ma, Xinyun Chen, and Denny Zhou. 2024. *Large Language Models as Tool Makers*. **ICLR 2024**. arXiv:2305.17126, **v2**；方法 LATM。[PDF](https://arxiv.org/pdf/2305.17126v2); [OpenReview](https://openreview.net/forum?id=qV83K9d5WB).

[38] Shuai Shao; Kangning Zhang; Qingyao Li; Shijian Wang; Hao Wang; Wenxiang Jiao; Yuan Lu; Yi Guo; Weiwen Liu; Weinan Zhang. **Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories.** SJTU/Xiaohongshu/Southeast University preprint,2026. 实读[arXiv2608.02276v1](https://arxiv.org/pdf/2608.02276v1)，2026-08-03，22页，训练边界审核；排除出全流程免训练方法。

[39] Haoran Xu; Jiacong Hu; Ke Zhang; Lei Yu; Yuxin Tang; Xinyuan Song; Yiqun Duan; Lynn Ai; Bill Shi. **SEDM: Scalable Self-Evolving Distributed Memory for Agents**. 预印本（2025）. 所读/核查版本：arXiv:2509.09498v3. [来源](https://arxiv.org/abs/2509.09498v3)。

[40] Tobias Lindenbauer; Georg Groh; Hinrich Schütze. **From Knowledge to Noise: CTIM-Rover and the Pitfalls of Episodic Memory in Software Engineering Agents**. 预印本（2025）. 所读/核查版本：arXiv:2505.23422v1. [来源](https://arxiv.org/abs/2505.23422v1)。

[41] 郭丹丹主讲，NICE学术发布。**RSI Survey：现代智能体系统的自我改进。** 公开学术分享，发布日期本轮未独立确认。[视频来源](https://www.bilibili.com/video/BV12yh86kEUS)。使用用户提供的中文自动字幕作为线索，不作为实验结果的一手来源。

[42] Harsh Trivedi, Tushar Khot, Mareike Hartmann, Ruskin Manku, Vinty Dong, Edward Li, Shashank Gupta, Ashish Sabharwal, and Niranjan Balasubramanian. **AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents.** Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp.16022–16076, 2024. DOI:10.18653/v1/2024.acl-long.850. [正式页及实际读本](https://aclanthology.org/2024.acl-long.850/)。

[43] Alexandre Drouin, Maxime Gasse, Massimo Caccia, Issam H. Laradji, Manuel Del Verme, Tom Marty, David Vazquez, Nicolas Chapados, and Alexandre Lacoste. **WorkArena: How Capable are Web Agents at Solving Common Knowledge Work Tasks?** Proceedings of the 41st International Conference on Machine Learning, PMLR235:11642–11662, 2024. [正式页](https://proceedings.mlr.press/v235/drouin24a.html)，[实际阅读正式PDF](https://raw.githubusercontent.com/mlresearch/v235/main/assets/drouin24a/drouin24a.pdf)。2024原版，不混后续WorkArena++。

[44] Shuyan Zhou, Frank F. Xu, Hao Zhu, Xuhui Zhou, Robert Lo, Abishek Sridhar, Xianyi Cheng, Tianyue Ou, Yonatan Bisk, Daniel Fried, Uri Alon, and Graham Neubig. **WebArena: A Realistic Web Environment for Building Autonomous Agents.** ICLR, 2024. [正式录](https://proceedings.iclr.cc/paper_files/paper/2024/hash/4410c0711e9154a7a2d26f9b3816d1ef-Abstract-Conference.html)。实际阅读[arXiv:2307.13854v4](https://arxiv.org/pdf/2307.13854v4)，2024-04-16。

[45] Ido Levy, Ben Wiesel, Sami Marreed, Alon Oved, Avi Yaeli, and Segev Shlomov. **ST-WebAgentBench: A Benchmark for Evaluating Safety and Trustworthiness in Web Agents.** ICLR, 2026. [IBM正式出版记录](https://research.ibm.com/publications/st-webagentbench-a-benchmark-for-evaluating-safety-and-trustworthiness-in-web-agents--1)，[ICLR官方会议录目录](https://iclr.cc/virtual/2026/papers.html)。**实际读的后续版本署名为** Ido Levy, Ben Wiesel, Sami Marreed, Alon Oved, Avi Yaeli, Nir Mashkif, and Segev Shlomov，arXiv:2410.06703v7，2026-06-04，[PDF](https://arxiv.org/pdf/2410.06703v7)。本文375任务等数字来自后者；当前[官方代码](https://github.com/segev-shlomov/ST-WebAgentBench)补核反馈/重置模块。

[46] Xiang Deng, Yu Gu, Boyuan Zheng, Shijie Chen, Sam Stevens, Boshi Wang, Huan Sun, and Yu Su. **Mind2Web: Towards a Generalist Agent for the Web.** Advances in Neural Information Processing Systems36, Datasets and Benchmarks Track, pp.28091–28114, 2023. [正式录](https://proceedings.neurips.cc/paper_files/paper/2023/hash/5950bf290a1570ea401bf98882128160-Abstract-Datasets_and_Benchmarks.html)。实际阅读[arXiv:2306.06070v3](https://arxiv.org/pdf/2306.06070v3)，2023-12-09；该PDF姓名写Samuel Stevens。

[47] Xing Han Lu, Zdeněk Kasner, and Siva Reddy. **WebLINX: Real-World Website Navigation with Multi-Turn Dialogue.** Proceedings of the 41st International Conference on Machine Learning, PMLR235:33007–33056, 2024. [正式页](https://proceedings.mlr.press/v235/lu24e.html)，[实际阅读正式PDF](https://raw.githubusercontent.com/mlresearch/v235/main/assets/lu24e/lu24e.pdf)。作者个人常用拼写Xing Han Lù；引用按PMLR书目。

[48] Tianbao Xie, Danyang Zhang, Jixuan Chen, Xiaochuan Li, Siheng Zhao, Ruisheng Cao, Toh Jing Hua, Zhoujun Cheng, Dongchan Shin, Fangyu Lei, Yitao Liu, Yiheng Xu, Shuyan Zhou, Silvio Savarese, Caiming Xiong, Victor Zhong, and Tao Yu. **OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments.** Advances in Neural Information Processing Systems37, Datasets and Benchmarks Track, 2024. [正式会议PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/5d413e48f84dc61244b6be550f1cd8f5-Paper-Datasets_and_Benchmarks_Track.pdf)。实际协议读本是较早[arXiv:2404.07972v2](https://arxiv.org/pdf/2404.07972v2)，2024-05-30；不声称等同后续Verified版本。

[49] Yuxuan Zhang, Yubo Wang, Yipeng Zhu, Penghui Du, Junwen Miao, Xuan Lu, Zhuofeng Li, Xingwei Qu, Zhengkang Guo, Yuanzhe Shen, Dingjie Song, Han Zhou, Tuney Zheng, Xian Wu, Hao Yu, Songcheng Cai, Yi Lu, Yunzhuo Hao, Minyi Lei, Liang Chen, Kai Zou, Huifeng Yin, Wendong Xu, Dongfu Jiang, Ping Nie, Jiaheng Liu, Wenhu Chen, and Kelsey R. Allen. **ClawBench: Can AI Agents Complete Everyday Online Tasks?** arXiv:2604.08523v2, 2026-07-20. [实际阅读PDF](https://arxiv.org/pdf/2604.08523v2)，[作者官方代码](https://github.com/TIGER-AI-Lab/ClawBench)，[V1公开轨迹](https://huggingface.co/datasets/NAIL-Group/ClawBenchV1Trace)。强机构preprint；repo自报EMNLP2026 Findings，未在本次独立确认正式录。

[50] Peter Jansen, Marc-Alexandre Côté, Tushar Khot, Erin Bransom, Bhavana Dalvi Mishra, Bodhisattwa Prasad Majumder, Oyvind Tafjord, and Peter Clark. **DiscoveryWorld: A Virtual Environment for Developing and Evaluating Automated Scientific Discovery Agents.** Advances in Neural Information Processing Systems37, Datasets and Benchmarks Track, 2024. [正式录](https://proceedings.neurips.cc/paper_files/paper/2024/hash/13836f251823945316ae067350a5c366-Abstract-Datasets_and_Benchmarks_Track.html)。实际阅读[arXiv:2406.06769v2](https://arxiv.org/pdf/2406.06769v2)，2024-10-07，首页仍标preprint，不改变已经独立核实的后续正式venue。

[51] Yimeng Chen, Piotr Piękos, Mateusz Ostaszewski, Firas Laakom, and Jürgen Schmidhuber. **PhysGym: Benchmarking LLMs in Interactive Physics Discovery with Controlled Priors.** Advances in Neural Information Processing Systems38, Datasets and Benchmarks Track, 2025. [正式录](https://proceedings.nips.cc/paper_files/paper/2025/hash/42abcf9dffa48ca44fea1c497539a914-Abstract-Datasets_and_Benchmarks_Track.html)。实际阅读[arXiv:2507.15550v2](https://arxiv.org/pdf/2507.15550v2)，2025-10-26。

[52] Xingyao Wang, Zihan Wang, Jiateng Liu, Yangyi Chen, Lifan Yuan, Hao Peng, and Heng Ji. **MINT: Evaluating LLMs in Multi-turn Interaction with Tools and Language Feedback.** ICLR, 2024. [正式录](https://proceedings.iclr.cc/paper_files/paper/2024/hash/8a0d3ae989a382ce6e50312bc35bf7e1-Abstract-Conference.html)。实际阅读[作者发布的会议PDF](https://zihanwang314.github.io/pdf/mint.pdf)，首页标ICLR2024及arXiv:2309.10691v3，2024-03-12。

[53] Jonathan Bragg, Mike D’Arcy, Nishant Balepur, Dan Bareket, Bhavana Dalvi, Sergey Feldman, Dany Haddad, Jena D. Hwang, Peter Jansen, Varsha Kishore, Bodhisattwa Prasad Majumder, Aakanksha Naik, Sigal Rahamimov, Kyle Richardson, Amanpreet Singh, Harshit Surana, Aryeh Tiktinsky, Rosni Vasu, Guy Wiener, Chloe Anastasiades, Stefan Candra, Jason Dunkelberger, Dan Emery, Rob Evans, Malachi Hamada, Regan Huff, Rodney Kinney, Matt Latzke, Jaron Lochner, Ruben Lozano-Aguilera, Cecile Nguyen, Smita Rao, Amber Tanaka, Brooke Vlahos, Peter Clark, Doug Downey, Yoav Goldberg, Ashish Sabharwal, and Daniel S. Weld. **AstaBench: Rigorous Benchmarking of AI Agents with a Scientific Research Suite.** ICLR, 2026. [OpenReview论文页](https://openreview.net/forum?id=M7TNf5J26u)，[ICLR官方录目录](https://iclr.cc/virtual/2026/papers.html)。实际阅读[arXiv:2510.21652v2](https://arxiv.org/pdf/2510.21652v2)，2026-04-21。
