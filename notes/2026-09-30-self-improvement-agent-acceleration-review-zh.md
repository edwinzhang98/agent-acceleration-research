# 固定模型权重下的 Agent 加速与自我改进

从轨迹学习和环境探索出发的文献评估与研究建议

2026年9月30日

这份报告回答三个问题：不训练模型，Agent 可以怎样从过去的经历中改进；这些改进中，哪些真正降低了执行时间或费用；我们现有的研究计划与它们相比，还能提出什么具体、可检验的问题。它以用户提供的综述、文献网站和讲座字幕为入口，结合第三阶段草稿，核查相关原论文的方法、实验与局限。旧草稿用于理解研究意图，不作为已证实结论。

**核心判断是：方向成立，宽泛想法已有充分先例，研究问题需要进一步收窄。** 从轨迹提炼经验、生成程序技能、探索页面或环境、自动修改 harness，都已经有人做过。一些工作还报告了实际费用下降，并计入了技能构造的摊销。我们的下一步应比较具体机制在目标工作流中的净收益，不能把“历史经验让 Agent 越用越快”本身作为新颖性。

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

### 三种速度必须分账

第一种是**改进过程的效率**：用更少候选、样本或 CPU 小时找到更好的 Agent。HGM、GEPA、HarnessFix 有这类结果。第二种是**改进后的执行效率**：部署时完成同类任务更快或更便宜，SpeedRunner、MobileGPT、StarHarness 的部分实验属于这里。第三种是**全流程净收益**：执行节省超过探索、生成、验证、检索、失败回退与维护的总投入。

这三种结果不能互换。ACE 的适配时间明显下降，但独立部署统计的输入 token 增加；Meta-TTL 调用次数少于静态 Agent，但六次任务会话的总时间更长。我们最终应追求第三种，同时分别报告前两种，才能知道收益来自哪里。

## 二 这次筛查覆盖什么

入口是《Self-Improvements in Modern Agentic Systems: A Survey》的 arXiv v1（2026年7月14日）、持续更新的项目网站，以及郭丹丹的公开分享字幕。网站与 PDF 不是同一天的文献快照。本次在网站方法表中保留了 **253条目录记录**：基础模型77条；外部 scaffold 176条，其中 prompt39、memory65、tool51、full scaffolding21。重复链接和错配条目保留在审计清单中，253不代表253篇独立论文。[1](https://arxiv.org/pdf/2607.13104v1)

我们先逐行做范围筛查，再对直接影响研究判断的工作读方法、评估协议、结果表及相关附录。筛查表明确区分“原文深读”“原文选读”和“目录级待核”，没有把未读全文的条目包装成否定结论。253条中，15条列为直接效率候选、47条为方法参考、63条为背景、70条按范围排除、17条重复、41条仍待核；这些是目录行标签，既不是质量排名，也不是全文阅读数量。网站另列的评测资源不包含在上述253条计数中；这也不是宣称覆盖综述的每一条参考文献。正文重点比较约三十余项方法，完整逐项结果与分支证据笔记随报告保存。

筛选优先级是：模型是否保持固定；是否从轨迹或环境反馈更新持久状态；是否减少实际执行资源；是否报告构造和验证成本；能否迁移到新任务、任务组合或变化后的环境。正式发表论文与研究机构预印本均可进入分析，但发表状态单独标注，预印本不冒充正式会议结论。补充 SpeedRunner、Metis、WALT、ActionEngine、HarnessFix、StarHarness 等直接近邻，以免被单个综述的目录边界限制。

清单确有需要纠正的地方。例如一个 Dynamic Cheatsheet 条目指向 Self-Notes，另有 WizardLM 和 SEDM 的题名与链接错配；ADAS 的网站会议信息也需要更正。最新 Meta-TTL 链接对应的标题和版本已变化。因此本报告按实际原论文引用，不能直接复制幻灯片上的年份、会议和数字。

字幕的价值在于解释作者的问题意识：他们同样关注改进成本与收益的取舍、环境变化和长期退化后的回滚。字幕存在自动转写错误，因此只用于概念线索；论文的数值和技术细节以原文为准。[41](https://www.bilibili.com/video/BV12yh86kEUS)我们没有复现这些实验，也没有用它们替代我们自己的业务工作流测量。

## 三 提示和文字反馈怎样产生改进

### TextGrad 的文本梯度到底是什么

TextGrad 将系统表示成计算图：提示产生回答，回答再参与下游任务，最后得到评价。反向过程让 LLM 结合某个节点的输入输出和下游批评，写出“这个节点应该怎样改”的反馈，再由另一次调用更新变量。它可以修改 prompt、代码或候选答案，而不需要访问执行模型的内部权重。[2](https://arxiv.org/pdf/2406.07496v1)，§2

**“梯度”在这里是作者明确使用的类比。** 普通梯度是一个数值导数，依赖可微函数和链式法则；文本梯度是一段有上下文的修改建议，没有保证对应某个真实导数，也没有普遍的下降方向或收敛保证。LLM 能提出有用建议，依靠的是它已有的语言、代码和任务推理能力，以及反馈是否准确。计算图帮助把最终错误追溯到可能需要改的组件。

以我们的问题作一个说明性例子：失败轨迹显示“日期跨月时选择了错误报销周期”。反馈可以沿执行链定位到日期计算的代码或提示，提出补充边界条件、调用日期函数的修改；随后仍要运行独立测试，判断是否修复。这个例子是我们的应用解释，不是 TextGrad 论文里的业务实验。它提供了 A 方向的候选生成方式，并不单独证明加速。

Trace 将类似思路推广到代码、提示和其他可编辑变量：保留程序执行关系、实际中间值与外部反馈，交给 OptoPrime 提出改动。其效果表中的运行分钟数包含优化、验证和测试，不能当作最终 Agent 的服务延迟；较大执行图也会增加上下文负担。[3](https://arxiv.org/pdf/2406.16218v2)，§2、Table2、§6

### GEPA 和 SkillOpt 已经把轨迹利用推进到哪里

GEPA 并非只看“这题错了”的分数。它读取执行轨迹、工具错误、评价标准等反馈，反思某个模块的提示，先用小批任务过滤，再在验证集上比较；候选池保留在不同任务上有优势的版本，还可合并它们的改进。这里的 Pareto 指跨任务表现互补，不是时间与费用的折中前沿。[4](https://arxiv.org/pdf/2507.19457v2)，§§2–3

它证明文字反思能够高效搜索提示，但需仔细解释效率数字：IFBench 上678 rollout是达到所选最佳检查点时的消耗，该设置的完整优化预算更大；“最多9.2倍更短”是特定模型和任务的提示长度，相对 MIPROv2，不是任务快9.2倍。GEPA适合做通用文字优化器基线，不能直接替代我们的执行加速证据。[4](https://arxiv.org/pdf/2507.19457v2)，Tables1–2、Fig18

SkillOpt 从成功和失败轨迹中改写一份自然语言 skill，限制每轮编辑量，保存被拒绝的编辑，经过独立选择集才接受更新，并用慢速反思修正优化策略。它已包含我们粗略想法里的“读轨迹、提出有限改动、验证、保留”部分，但输出仍是给模型阅读的策略文档。[5](https://arxiv.org/pdf/2605.23904v2)，§3

其 Table6 很能说明代价：Spreadsheet 的 skill 从224增至1,995 tokens，优化消耗21.4M tokens；SearchQA 从16增至857，优化消耗213.8M。部署时没有额外 optimizer 调用，不代表提示开销为零。它的任务性能有明显提升，但这些数字无法证明业务 Agent 的净加速。论文还出现针对 grader 读取结果的电子表格策略，这提醒我们把“业务要求确实满足”与“测试程序给分”分开核验，而不是仅依赖优化器自己理解评分规则。[5](https://arxiv.org/pdf/2605.23904v2)，Table6、§4.5

### ACE 与 Meta-TTL 为什么特别值得比较

ACE 把经验维护拆成执行、反思、整理三个角色，用带 ID 的条目和局部增量更新避免反复重写整份记忆。它是比简单追加反思更完整的上下文维护方法。AppWorld 中相对 GEPA 的离线适配时间从53,898降到9,517秒；但附录另一设置的160个评估任务，ACE输入 token为58.62M，GEPA为26.96M，虽然 rollout从2,470降到2,354。这里体现了**更快学到经验、执行时读更多经验**的取舍；两组实验设置不能拼成一个统一加速数字。[6](https://arxiv.org/pdf/2510.04618v3)，Table4；AppA.3 Tables12–15

Meta-TTL 进一步学习“怎样根据经历改进”：外循环搜索 meta-prompt，内循环依据它在每次尝试后改 actor prompt。最终固定 meta-prompt，在未见任务或域上测试跨次尝试的适应。主方法两层都不改模型权重，适合解释为什么无训练系统仍能“学会如何学习”。[7](https://arxiv.org/pdf/2604.00830v4)，§3

不过其每个含六次episode的Jericho会话，三次运行平均从静态基线593.2秒、196K tokens，变成860.9秒、364K tokens；调用数却从231降到204。它比若干昂贵的自改进基线快，但比不改进更慢。每个 benchmark 另有约30–70美元离线 meta-search。论文主要证据是加权学习曲线与跨域表现，而不是执行净收益。[7](https://arxiv.org/pdf/2604.00830v4)，§4.4、Table6

FORGE提供另一个有用对照：多个实例把失败转为文字规则或示例，按阶段广播表现最好的记忆，达到阈值就冻结。它把记忆表示与选择机制拆开研究，Rules相对Examples更省token；这个节省不能解释成比静态 Agent便宜。作者也发现过早冻结可能牺牲后续学习，且只在一个网络防御环境和攻击类型下验证。对我们最有帮助的是：经验是否有价值，需要独立选择；保存得越多并不一定越好。[8](https://arxiv.org/pdf/2605.16233v1)，§§3、5、7

## 四 从轨迹记忆到可执行技能

### 记住事实与学会做事需要分开

A-Mem是用户幻灯片中的记忆代表。新交互变成包含内容、时间、关键词、标签和上下文的笔记；系统寻找关联笔记、建立链接，还会根据新信息修改旧笔记的描述。自进化发生在外部记忆的内容与组织上，不是基础模型越来越强。它主要在LoCoMo、DialSim等长对话问答上检验能否更好地找回和关联信息。[12](https://proceedings.neurips.cc/paper_files/paper/2025/hash/19909c36f51abc4856b4560aff3d36d6-Abstract-Conference.html)，§3–4

它与加速的关系主要是减少每次携带的历史上下文。论文报告的token长度和memory operation费用口径并不完全一致，不能直接解释成完整业务任务的长期成本下降。它没有证明从浏览器动作轨迹学到程序技能，因此适合参考记忆组织，不是我们B方向最直接的基线。

AWM更接近执行经验：从成功轨迹抽象子任务，参数化具体对象，存成文字workflow，运行时给Agent参考。正式ICML版本报告WebArena成功率35.5%，成功路径步数约7.9到5.9；但是主要方法仍让模型逐步执行，不能当作宏操作。附录将其改为可执行高层动作AWM-AS后，Mind2Web任务成功率从4.8%降至3.6%，尽管单步指标略升。作者将一部分问题归因于弹窗和状态变化，固定序列跳过了必要观察。[13](https://proceedings.mlr.press/v267/wang25bx.html)，Table1、AppD/F

ReasoningBank同时从成功与失败中提炼策略，执行前检索；另有扩大多轨迹采样的MaTTS。Gemini-2.5-Flash在去除Map的WebArena上，成功率40.5%到48.8%，steps9.7到8.3；但成本附录的总token统计从50,847.4增至53,054.5，包含judge和记忆提取，约多4.3%。这两张表各有口径，成本表未单独明确模型，不能当成全模型平均收益。[14](https://arxiv.org/pdf/2509.25140v2)，Table1、AppC.2 Table5

ExpeL的经验比较与示例检索同样能改善任务表现，却增加经验上下文。ALFWorld平均动作14.82到14.30，trajectory token从2,051.49到2,856.70；这里是轨迹字符串统计，也不等于逐次API累计账单。共同的教训是：文字经验可以减少错误决策，同时让每次决策读得更多。[15](https://arxiv.org/pdf/2308.10144v3)，AppJ

### 如何判断哪条经验值得用

MemRL在每条外部记忆上维护效用分，先按语义筛选，再按经验带来的奖励更新选择。它不反传更新LLM，也不因此需要我们训练模型；这是一种可以在固定API模型上实现的奖励学习。GPT-4o-mini的LifelongAgent OS留出迁移成功率从67.3%到74.6%，但论文没有建立普遍部署净加速。对我们更有帮助的是把“语义相似”与“曾经有效”分开，再检验效用是否应该扣除资源成本。[16](https://arxiv.org/pdf/2601.03192v2)，§3、AppF/G

成本敏感的接纳也已有先例。SEDM提出paired A/B，按奖励增益扣除延迟或token惩罚接纳、删除经验；因此“只有划算才保留”不能作为全新原则。它的主要token优势相对G-Memory，而非无记忆，例如FEVER的输入token由G-Memory3.62M降至2.47M，但无记忆只需1.65M；反复回放的构造开销还需另计。用历史工具响应重放，也不能保证覆盖改变策略后真实环境会给出的反事实响应。[39](https://arxiv.org/abs/2509.09498v3)，§3、Tables2–4

负例CTIM-Rover从仓库轨迹提炼通用与项目经验，却在45个留出软件任务中从原系统42%降到完整记忆版本40%，单加insights为31%。样本小，不能否定全部记忆方法；但它展示了表面相似经验把Agent带向错误位置的具体风险。[40](https://arxiv.org/abs/2505.23422v1)，Table1、§5

### Metis 已经做到先用文字 再把稳定经验变成代码

Metis将历史经验分为plans、环境facts和pitfalls。它先让文字plan被不同结构的query反复使用，达到复用条件后再生成参数化工具；并非每次成功都立即固化代码。代码通过依赖与编译检查后供后续任务调用，反思既利用失败轨迹，也利用成功但低效的轨迹。这与我们的粗略想法重合很高。[17](https://arxiv.org/pdf/2606.24151v1)，§2–3

固定GPT-4o执行器、Sonnet4.6反思，在AppWorld官方划分中，无记忆到Metis的TGC由51.8%到60.1%，每任务执行token112.6K到97.4K，ReAct轮数14.55到11.25。另在重采样划分中，No Memory、SkillX、Metis三个方法共同完成的62题上，Metis也降低了token，减少成功题目集合不同造成的混杂。构造反思另需7.9M tokens，但排除了生成训练轨迹的成本，没有完整秒数或美元回本结论。[17](https://arxiv.org/pdf/2606.24151v1)，Tables1–2

作者的更早代码化消融在部分设置下执行更省，却准确率更低、建设更贵。它已经把问题推进到“什么经验值得编译”。我们若继续此方向，需要比较环境条件证据、失败恢复、状态变化以及真实费用，而不是重新提出文字转代码。

### SpeedRunner 已经直接研究历史技能学习如何降本

SpeedRunner让固定模型的actor分批执行，另一个固定模型coding agent读取历史轨迹、工具调用栈和技能版本，新增、修改或删除程序技能，区分公开工具和内部辅助函数。它主要从日志改进，不依赖重新回放环境或额外验证。因此与我们的A方向——分析trajectory再改代码——是直接近邻。[23](https://arxiv.org/pdf/2608.11338v1)，§3

ScienceWorld、BabyAI和Crafter实验以200条学习episode、定期留出评估和三次seed考察持续学习；BabyAI曲线显示成功率约从67%接近100%，单轨迹美元成本约为ReAct的八分之一。这里是近似曲线结果、限该环境，不能外推网页或说墙钟时间也快八倍。尤其需要承认：附录已将技能学习费用按batch摊入，并统计输入、缓存输入和输出，不存在“该文完全忽略学习成本”的空白。[23](https://arxiv.org/pdf/2608.11338v1)，Fig3、AppA.3

ASI则采用另一种接纳方法：从成功轨迹归纳代码，把新技能插回源任务进行执行验证。WebArena同Claude3.5 Sonnet对照，无技能32.7%成功率、5.6步，文字AWM36.3%、5.9步，程序技能40.4%、5.0步。一个宏内部可以有多个UI动作，所以5.0不是浏览器事件数，也不是秒；生成、回放和judge还会增加学习开销。它适合做我们“需要验证的程序技能”基线，与SpeedRunner的日志归纳形成有意义的对照。[19](https://arxiv.org/pdf/2504.06821v2)，§2、Table1

### 技能包有实际加速结果 但覆盖和泛化不能省略

MUSE-Autoskill将成功任务沉淀为含说明、脚本、资源和经验的技能包，再在相同任务重用。SkillsBench的75个可运行任务中，只有47题构造出了可用skill。在这个覆盖子集，no-skill的中位729.3秒降至434.7秒，token579K到499K；生成skill另需中位156.3秒和364K tokens。这些延迟不含SkillsBench验证器耗时。全集把未覆盖任务计入后，自制技能得分53.42%，低于人类技能59.67%，不能只引用覆盖题上的85.24%。[24](https://arxiv.org/pdf/2605.27366v2)，§4.3、Tables4、6

它支持特定任务复用可以节省执行，但同题成功轨迹再跑会高估泛化，报告也不覆盖全部失败学习与长期维护。OpenSkill则是另一个提醒：它主动搜索外部知识并生成验证依据，Opus4.6的任务得分25.5%到43.6%，执行均时却465.0到845.4秒，且不含构造。作者测到proxy test precision为56.9%；所谓88.9%是另一项测试意图覆盖评估，不是验证准确率。[25](https://arxiv.org/pdf/2606.06741v1)，Tables1、3、AppE Table8

这些结果说明我们必须同时报覆盖率、正确性和资源量；只统计学会技能的成功子集，会把很容易复用的任务挑出来，形成过于乐观的加速结论。

## 五 环境探索能带来什么

环境探索与历史轨迹学习是两个可以组合的采集渠道。前者主动补充未知条件，后者利用已经支付过成本的交互。我们需要问的不是“要不要探索整个环境”，而是“哪条不确定的环境规律值得额外验证，它会影响多少未来任务”。

### 从自主探索到程序化复用

Voyager提供了早期完整范式：依据Minecraft状态选择学习目标，生成代码，利用环境反馈修复，成功技能进入检索库供后续组合。它表明探索目标本身也可以由Agent决定；但“15.3倍”等结果的横轴是prompting iteration，不能转成实际秒数。技能库并非所有早期里程碑收益的唯一来源。[26](https://arxiv.org/pdf/2305.16291v2)，§3、Table1

SkillWeaver把这条路线带到网页：自动提出短探索任务，执行后抽取参数化Python/Playwright函数，再生成输入测试和修复。每站约160轮探索或测试，意味着明确的前期投入。固定GPT-4o时WebArena成功率22.6%到29.8%；真实网站四站57题为40.2%到56.2%。它有很强的“探索能学会操作”的证据，但没有完整墙钟时间、美元或回本曲线。[20](https://arxiv.org/pdf/2504.07079v1)，§2–3、Tables1–2

WALT进一步利用网站功能本身构造工具，例如把可通过URL参数实现的搜索排序直接变成操作，减少反复点击；工具也可包含确定性步骤与必要的agentic fallback。在VisualWebArena-Classifieds、同GPT-5-mini、text/self的消融中，无工具57.5%成功率、8.9步，有发现工具61.5%、6.5步。完整配置另含多模态DOM解析和外部验证器，不能把其全部提升算作自主学习的贡献。[21](https://proceedings.iclr.cc/paper_files/paper/2026/hash/5b175f9e93873e3a10a6ce43dbb82e05-Abstract-Conference.html)，§4.4、Table2

其正式会议版报告305个候选、252个工具验证成功，构造每工具约1.67美元。作者以基线0.12美元每任务估计约14次使用回本，但严格计算必须用“基线成本减去新方案在线成本”作分母；因此这只是粗略建设投入对比，不是完整净回本点。动态页面、罕见参数和selector漂移仍是主要局限。[21](https://proceedings.iclr.cc/paper_files/paper/2026/hash/5b175f9e93873e3a10a6ce43dbb82e05-Abstract-Conference.html)，§4.6

MobileGPT也是直接先例：预探索应用并建立页面、子任务和动作记忆，后续可匹配动作直接复用，失配时调用模型适配；高层规划和参数填充仍可能调用模型。其八应用80任务消融中，warm-start相对Derive基线平均延迟减62.5%、API费用减68.8%；但冷启动略增成本，且该消融在冷启动失败后由人修复路径。它证明条件复用可能有大收益，不能被描述成完全自主学习后自然达到同样收益。[18](https://arxiv.org/pdf/2312.03003v3)，§7.3

ActionEngine用离线crawler构建状态机记忆，在线据此生成并执行程序。最新v2在四个WebArena域655题、同Claude Opus4.6比较中，成功率82.7%到91.2%，平均延迟87到27秒，估算API费0.40到0.05美元每题，属于这里最直接的时间与费用证据。[22](https://arxiv.org/pdf/2602.20502v2)，Table1、§5.2 Fig4

但主实验在初始探索后，使用每个任务模板的一个生成实例做warm-up，正式评测关闭Patcher；初始知识的成功率73.1%，精炼后91.2%。所以不能说完全任务无关探索直接取得主结果，也不能以此证明在线维护期间依然保持同样加速。作者报告各域36–260分钟、11.6–37.2美元的crawling成本与回本估计，但warm-up是否全包含不够清晰；8倍费用下降还受缓存定价影响。[22](https://arxiv.org/pdf/2602.20502v2)，§5.1–5.3、Table2

探索并不一定要立即产代码。DRAFT先实际调用陌生工具，把参数和返回规律写入更准确的文档，再供固定Agent使用；它主要改善正确工具使用，没有证明净时间收益。这个轻量对照可以帮助我们判断，程序化执行究竟比正确的环境说明多带来多少价值。[27](https://arxiv.org/pdf/2410.08197v2)，§3–4

用户所问的ALITA则按任务能力缺口搜索库、生成脚本、配置环境，再包装为MCP工具。GAIA上另一Agent复用其工具时，GPT-4o成功率27.88%到33.94%；主比较的工具库重置与单独复用实验需区分。它展示了能力扩展和工具复用，但没有对应的执行延迟与完整学习费用证据，不能凭“工具可复用”推导出已加速。[28](https://arxiv.org/pdf/2505.20286v1)，§3、§5.1 Table2

LATM更早就提出强模型一次制作工具、较便宜模型反复调用以摊薄服务成本。主要实验为算法与推理任务，不是长期网页操作；不过“一次投入、以后复用”的经济逻辑已经非常明确，我们需要增加的是目标环境下的实测边界。[37](https://arxiv.org/pdf/2305.17126v2)，§2–3

### GLoW 与 WorldEvolver 学的是环境规律

GLoW维护一组有价值的历史轨迹，在全局选择值得继续探索的状态，再通过动作重放返回；局部从同一起点比较几条路径，形成解释哪些动作有效的文字反思。它将“去哪里探索”与“到那里怎么行动”分开，是我们第二个方向有价值的方法参考。[10](https://arxiv.org/pdf/2509.24116v2)，§3

Jericho实验中同类LLM基线都有1,000次环境交互预算；GPT-4.1-mini在Zork1预算内最高游戏分数的三次运行均值，GLoW为73.0、ICRL为51.7。但所谓100–800倍效率指相对部分RL方法的环境样本预算差，不是省这么多API费或时间。附录给LLM方法每1,000步约4–6美元，费用差较小；环境还允许返回状态并提供有效动作接口。企业网页是否有同样可重置、可枚举的接口，需要重新验证。[10](https://arxiv.org/pdf/2509.24116v2)，Table1、AppC.1

WorldEvolver更接近“记住环境怎样响应操作”：记录真实的观察—动作—新观察，用预测与实测的不一致生成带证据分的文字规则，并过滤低置信预测，actor与world model权重均固定。这说明环境模型也可以是检索和文字规则，不必训练一个神经网络。[11](https://arxiv.org/pdf/2606.30639v2)，§3

其收益并非全面。Table2中Gemma配ReAct在ScienceWorld由44.44%到52.22%，GPT-5.4-mini同列却由65.56%降到63.33%；而且这是每题五次尝试的best-of-5。算法还增加预测、重新决策，动作变化时可能再预测一次。它支持“环境知识能改善部分决策”，尚不支持“加一个world model就能加速”。另一个消融在每题前清空记忆、只保留该题多次尝试间记忆，表现仅下降0.5–1.1个百分点；不能把总收益全部归因于跨任务积累。附录也报告逐步调用和上下文开销，但没有给净执行加速。作者明确限定在两个文本环境，并指出置信估计依赖模型API提供概率信息。[11](https://arxiv.org/pdf/2606.30639v2)，§4.1、Table2、Limitations

### 我们应怎样理解探索的研究价值

以上工作已经超出简单保存轨迹，进入任务选择、状态表示、可执行技能和预测校正。因此“主动探索”本身同样不是空白。更具体的候选问题是：只对高频任务中影响复用安全性或速度的未知条件进行探测，能否比全量预探索、纯被动记忆或遇错即反思更划算？这里的条件可能是字段依赖、账号权限、页面分支、对象状态或API边界。

这只是待检验的问题。某些环境中根本没有足够重复任务，或者维护成本高于节省；此时最好的结论可能是停止构建更多技能。我们不预设一定需要完整状态图，也不预设文字规则必须升级为代码。

## 六 整体 Harness 自改进与我们的自动诊断

### 最接近 A 方向的已经有具体实现

HarnessFix将轨迹转为带依赖关系的中间表示，连接错误现象和harness代码位置，再用受限的修复操作修改系统并验证。它已比“把失败日志交给LLM自由改代码”更深入：我们若研究诊断，应与这样的结构化方法比较。GPT-5-mini在AppWorld的90题test集、三次独立运行平均成功率由36.7%到43.0%；其37.2M相对Meta-Harness74.6M的token，属于离线演化和修复阶段，不能说部署费减半。[29](https://arxiv.org/pdf/2606.06324v2)，§III、Tables3–4

StarHarness直接覆盖“环境经验转代码”：读取轨迹提出有边界的patch，先检查基本可运行性和局部修复，再由隐藏的selection集合择优。演化结果包括API schema修正、业务更新约定、日期财务计算、表格操作等。GPT-5.4在103个ITSM任务上，成功率23.3%到43.7%，turns每题18.12到9.87，估算API费1.23到0.58美元。但费用来自包括演化池的全基准，held-out另报成功率提升15.1个百分点，没有单独held-out费用和完整搜索回本账。[30](https://arxiv.org/pdf/2608.24804v1)，§3、Tables2、4

因此，自动归因、修改工具接口、固化确定性计算，都已有直接先例。我们可以研究“基于成本和条件证据的诊断能否比通用patch搜索更有效”，但不能仅以这几个组件同时出现作为创新。

### 在线持续改进有收益 也有明显边界

Adaptive Auto-Harness把学习与运行路由分开：从历史批次分析问题、调查、构建、验证，保留多个harness分支，再按任务选分支。FutureX中求解端每题耗时之和由34.2降到6.6小时，Pass@1从31.0%升至47.3%；同一论文PolyBench的时间却由25.6增到59.5小时。附录明确缺少evolver token和编排开销，这不是全流程墙钟时间或总费用。[31](https://arxiv.org/pdf/2606.01770v2)，§4、AppB Table5

Continual Harness让Actor与Refiner在不重置的长任务中修改提示、记忆、工具和代码。在Pokémon Emerald、Gemini3.1 Pro、每seed24小时设置下，from-scratch harness的中位API费用约130美元、里程碑完成100%，minimal约215美元、98%。这是有力的特定运行费用证据，但不是完成整个游戏时间减少40%；弱模型也可能无法利用复杂组件而退化。其基础接口还提供local text map等信息，不是只看裸截图。它的固定模型实验可以纳入本报告，后半涉及权重训练的分支则应分开。[32](https://arxiv.org/pdf/2605.09998v1)，§§4.3–4.4、Fig6

Live-SWE-agent在当前软件任务中按需创建脚本，说明无需先做庞大的离线系统搜索，也能出现自改进。GPT-5的成功率和平均费从65.0%/0.28美元到68.4%/0.27美元；Gemini3 Pro从74.2%/0.46到77.4%/0.48，费用并不一致下降。这些基线数字沿用既有报告，未全部在统一条件下重新运行；微小费用差不能作为严格受控的因果证据。它主要验证当前任务内的工具创建，还不能直接证明跨任务积累长期省钱。[33](https://arxiv.org/pdf/2511.13646v3)，Table1

### HGM 加快的是寻找好版本

用户幻灯片中的HGM从DGM的版本树出发，区分一个Agent当前做题能力和它产生更好后代的潜力。它利用后代成绩估计分支潜力，自适应决定继续扩展还是增加评估。SWE-bench Verified的60题设置中，用GPT-5扩展、GPT-5-mini做任务评估，同为800次评估，allocated CPU-hours从DGM的1,231降到HGM的517，best-belief成功率从53.3%到56.7%。2.38倍来自前两个CPU小时数字，不能解释成最终Agent每题快2.38倍。[34](https://arxiv.org/pdf/2510.21614v3)，§4.2、Table2

DGM则证明固定基础模型、修改自身代码并保留候选archive可以提升能力；作者也承认更强版本推理更贵。完整搜索还可能很昂贵。因此我们不宜一开始复制庞大进化树；先用受限修改和清楚的成本目标验证收益，得到足够证据后再决定复杂搜索是否值得。[35](https://arxiv.org/pdf/2505.22954v3)，§4、AppE.1

## 七 正确性评估决定加速结论能否成立

较少调用可能来自跳过必要步骤，较高得分也可能来自适应评测程序的缺口。若目标是按成文规则填写或更新结构化内容，最终结果、业务约束、必要确认和副作用应独立检查，不能让生成修改的Agent同时定义自己的成功条件。

AgentDevel已明确做pass→fail与fail→pass检查；StarHarness也有选择与留出流程。这说明验证门禁不是新的概念。与此同时，proposer看不到selection标签，并不意味着selection没有参与优化：只要多轮根据它接受候选，它就是开发过程的一部分，还需要未参与选择的最终评估。[30](https://arxiv.org/pdf/2608.24804v1)[36](https://arxiv.org/pdf/2601.04620v1)

VASO给出更具体的借鉴：把技能连接到形式规范，先检查规则是否自相矛盾，再验证生成计划，利用反例改善可复用契约。模型权重保持不变，全局规范固定。然而其命题映射由模型生成且没有被形式验证，保证依赖这个映射正确；当前只处理顺序执行技能。Table1中的97.2是手工映射的安全分，自动映射为96.8，不能说成自动系统97.2%的端到端任务正确率。[9](https://arxiv.org/pdf/2606.05395v1)，§§3–5、Table1、§7

我们的C方向可借鉴“把规范、观察映射和评分程序分开”，但不必强行把全部网页业务写成形式逻辑。第一轮可以从可执行的业务断言、环境真实状态检查和人工确认的小型评估集做起。关键是保留独立的最终标准；模型生成用例只是起点，人类和程序仍需核其覆盖与正确性。

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

### 先用相同信息比较经验应存成什么

第一阶段固定基础模型、工具权限、可见观察和任务预算，准备可重置、有业务规则的重复工作流。将开发轨迹、候选选择用例、最终测试分开，并按任务模板或操作组合划分，而不只是随机换几个参数。相同任务的重复实例可以研究摊销，但需要与真正未见的组合、状态变化另报。

| 对照 | 保留什么 | 要回答的问题 |
|---|---|---|
| 不学习 | 固定prompt和工具 | 原有耗时、费用与失败在哪里 |
| 文字经验 | 同一批轨迹提炼的规则或流程 | 仅提供知识是否已经足够 |
| 程序技能 | 同一批轨迹生成并验证代码 | 省掉模型决策是否抵消构造与维护 |
| 条件技能与定向探测 | 增加适用条件、触发回退及少量探测 | 这些机制是否有额外净收益 |

为分别检验H1和H2，在同一技能库上先比较有无适用条件检查，再在相同检查机制下比较固定预算探索与收益导向探索，避免把全部新增组件的效果混在一起。

对于A方向另设一个小规模诊断实验：同一组成功但昂贵、以及失败的轨迹，比较自由修改、结构化故障定位、按成本和频次定位。每次只允许有限类修改，记录“诊断是否准确”和“修改是否带来实际收益”；二者不要混为一项。人工分析可作为小样本上界，不能假装零人工成本。

### 评价同时保留三份账

构造账包括生成历史轨迹、额外探索、反思、写工具与依赖准备；选择账包括候选比较、回归测试和被拒绝修改；执行账包括检索、技能匹配、常规模型调用、环境开销和失败回退。维护成本另列，不计入构造账，以便统计环境变化的代价。历史轨迹如果是既有业务自然产生，可以另报“已有日志可用”的增量场景，但不能把它与从零生成日志的场景混在一起。

下面是本报告的核算定义，不是某篇论文的公式：

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
