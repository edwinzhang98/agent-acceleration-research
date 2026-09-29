# 从执行轨迹学习的 Agent 加速研究计划

研究目标 相关工作与实验方案

2026年9月29日

## 一 研究目标与核心判断

我们希望让 agent 在反复执行同类任务时，能够自动利用过去的执行记录，减少下一次的错误、重复推理和无效操作。这项研究包含两个相互配合的方向：一是把目前由人完成的“看轨迹、找原因、改程序或提示、重新测试”变成自动改进循环；二是从轨迹中积累对环境交互的认识，把已经理解、可以检查适用条件的操作做成可复用 action。最终目标是在保持任务质量的前提下，降低实际完成工作的时间和费用。

**现有文献已经足以支持这两个方向在已评测设定中的可行性，但也说明它们的宽泛表述不能直接作为创新点。** 自动修改 agent 的提示、工具和代码，从交互中学习规则或动作，以及用程序技能减少模型推理，都已有很接近的研究。我们需要回答更具体的问题：面对一段有问题的轨迹，系统能否选对修改位置；从有限记录得到的环境知识，能否支持可靠复用；计入分析、生成、验证和维护以后，改进是否仍有净收益。

本计划建议从一个相对稳定、可重置、带明确业务规则的 Web 工作流开始。Concur 或其他报销、申请、理赔平台都可以作为候选；这里的研究对象是这类重复交互任务，而不是某一个产品。第一版保持任务执行模型的权重固定，先研究外部提示、程序、工具及环境知识如何改变。是否训练外层优化器，留作后续选择。

下文先独立说明问题、文献与候选方法，再回到前两部分的 Time 和 Money 框架审查其解释力。文中的“拟”“建议”和研究假设均是待实验检验的方案；文献结果不等于我们已经复现的结果。当前阶段不填写预算金额，也不预先承诺加速比例。

## 二 我们究竟要把什么过程自动化

### 从人工修补到可以反复运行的改进循环

我们已有的观察是：人在分析 agent 轨迹后，有时可以找出经常犯的错误、重复消耗最多的步骤，或适合交给程序完成的操作，再通过修改 prompt、code 或 action 改善系统。这说明轨迹可能提供有用的改进信号，但目前还不能据此声称一个自动循环已经跑通，更不能把一次修补的效果当成长期收益。

本研究拟让系统接管这个分析与试验过程。它不仅应读取失败任务，也应读取成功但昂贵或缓慢的任务；输出不只是“下次注意”的反思，而是一个可执行、可验证、可撤销的候选修改。之后系统自行选择相关测试，运行修改前后的版本，决定保留、继续修改或回滚，并把结果用于下一轮。

这里的自动化对象是**改进流程中的人工干预**。业务执行中有些信息本来就只有用户知道，有些决定需要授权，这些询问可以是正确行为。实验需要分别记录“为了修系统而让人写提示或改代码”和“按业务要求向用户补充询问”，不能靠省略必要询问制造加速。

### 从经历过页面到学会环境交互

第二个方向来自另一种重复消耗：agent 即使多次到过同一个系统，也可能仍要重新辨认页面、寻找入口、猜测字段和试探选项。过去的轨迹其实已经包含“在什么条件下，执行哪个操作，会出现什么结果”的信息。我们拟把这些信息保存下来，并用于后续执行。

但“固定环境”不意味着每次看到的状态都相同。同一页面可能受账号权限、审批状态、先前选择和后台数据影响。有限日志只能证明某些交互被观察过，不能证明整个环境已被测量完毕。因此，本计划从局部、带适用条件的知识开始，不预设必须还原完整状态图，也不把每条成功路径都直接固化成脚本。

### 两个方向共用一个验证过程

轨迹分析发现的问题，可能需要修改提示、修复代码，也可能需要补充环境知识或创造一个新 action；学到的 action 在新任务上失败，又为下一轮诊断提供材料。因此，两者可以共用轨迹记录、候选版本、测试和回滚机制。它们是否组合后优于各自单独使用，需要通过实验回答，不能由流程图推导出来。

## 三 相关研究已经做到什么程度

### 自动改进已经从提示扩展到可执行系统

在正式发表的工作中，AgentOptimizer 已把函数作为可修改对象，根据执行历史添加、删除或调整函数描述与实现；GEPA 根据执行反馈演化提示；Darwin Gödel Machine 则研究通过评测推动 agent 代码的持续改进。它们说明，轨迹或执行反馈驱动的自动修改已不局限于“写一段反思”，也不要求修改任务模型本身的权重。[1][2][3]

与我们最接近的近期预印本把这个过程进一步具体化。HarnessFix 从失败轨迹定位到代码位置，合并跨任务反复出现的问题，选择修复算子，并通过验证集回归检查筛选修改。StarHarness 在企业任务中演化执行框架，论文示例已经包括环境惯例、API schema 修复以及专用的表格和日期计算工具。DarwinX 通过候选继承与选择演化执行框架。这些工作直接覆盖“轨迹归因、改 code 或工具、自动重跑”的主要组成部分。[4][5][6]

我们不能因此把一个通用的自动修补循环当成充分的新贡献。更有价值的研究问题是：在我们的工作流中，针对耗时和费用的诊断，是否能比通用修改器更有效地选择修改位置；某种结构化的环境知识是否值得维护；筛选机制是否真的保住业务正确性。还需避免把论文中的不同成本混为一谈，例如 HarnessFix 的相关 token 表记录的是离线演化和修复开销，不能直接解释为部署推理节省；StarHarness 的选择目标定义为平均任务分数，部署 API 费用另行报告；名称中的 cost function 不等于实际金额。[4][5]

强化学习也是可选路线。Harness-R1 从失败材料和重新执行得到的反馈训练单独的框架编辑器，说明“执行模型权重固定”与“外层改进过程可以学习”并不矛盾。第一版采用无需训练的搜索与验证，是为了先验证反馈和修改空间是否有用；它是实施建议，不是对强化学习的排除。[7]

### 环境经验可以保存为文字 规则或可执行动作

AutoManual 已通过成功和失败经验维护带条件的操作规则；AutoGuide 从离线轨迹产生与当前上下文匹配的指导；Agent Workflow Memory 将历史流程转成可调用的文字工作流。这些正式发表的工作支持“过去的交互可以帮助后续任务”，但文字工作流并不自动等于可执行程序，也不意味着每次复用都可以省去模型推理。[8][9][10]

另一组工作直接学习动作。LearnAct 根据反馈改进程序化 action 及其使用说明；WALT 和 SkillWeaver 学习、测试并修复可复用工具，其中 WALT 已允许确定性操作与需要模型判断的步骤组合。对我们而言，这说明“能写代码的部分固定下来、语义判断留在运行时”已有研究基础，不能单独作为新概念。[11][12][13]

环境表示和历史轨迹复用也已有直接近邻。ActionEngine 构建环境状态机记忆并支持程序化执行与修复；AppAgentX 从移动端历史交互构建参数化快捷动作。ActionEngine 主要评测使用任务模板预热，并关闭了在线 Patcher，因而不能从主要结果直接推出持续维护已在真实任务流中得到验证。AppAgentX 所在的移动 GUI 场景也不能直接替代 Web 业务流程的实证。[14][15]

SpeedRunner 更直接研究从历史轨迹持续学习程序技能来降低 agent 成本，报告随学习进度变化的表现，并考虑技能归纳成本的摊销。因此，“从旧轨迹生成技能”“越做越便宜”或“画累计成本曲线”本身都不是尚无人涉足的空白。我们拟研究的较窄问题，是有限业务日志中的条件知识，在复杂规则和未知状态下是否能支持更可靠、更划算的复用。这个差异目前只是一项待检验的假设。[16]

### 质量保证与经济收益都需要独立证据

减少执行步骤不必然减少总费用。ReasoningBank 的相关结果就提醒我们：记忆可以改善执行，但记忆构建、检索和额外上下文也会产生开销；不能只看 actor 少走了几步就得出整体更便宜的结论。已有 SoL-Pi 和 RRSI 等近期工作也把质量约束、效率或 token 约束纳入改进过程，因此“筛掉不划算的修改”不能直接声称为新的研究范式。[17][18][19]

可靠验证同样不是现成答案。AgentRewardBench 显示自动判分器会误判 Web 轨迹。SOPBench 以及关于隐含规则合规性的逻辑引导合成研究，为从规则构造测试情境提供了参考，但其流程包含程序检查和人工审核，并不支持“让模型读规则然后自评即可得到可信标准”的说法。[20][21][22]

这些文献共同支持一个判断：我们已有足够的组成方法开始搭建实验，但尚无证据保证任意组合就有收益。当前最需要补上的，是目标工作流中修改选择、环境复用可靠性以及完整成本之间的实证关系。

## 四 建议采用的研究方案

### 先建立可以定位问题的轨迹记录

每次执行至少记录任务输入、可见环境状态、模型调用、工具调用、前后观察、重试和失败位置，并关联结果检查、时间戳与实际计费信息。模型调用、工具调用、环境操作和业务任务分别编号，避免把“动作数量”当成所有开销的共同单位。提示版本、代码版本和 action 版本也应随记录保存，以便复现和比较。

分析器从这些记录中提出改进假设，而不是直接宣布根因。例如，“找不到按钮”可能来自定位器失效，也可能来自未满足前置条件、错误页面状态或模型选错路径。每个候选问题应附上支持轨迹、反例、可能影响的任务、预期改善的行为，以及能够区分不同原因的检查。如果证据不够，就输出待验证假设或请求补充运行。

初期可按问题重复频率、累计耗时、实际费用和后续复用机会排序。这个排序帮助把有限改进资源花在更值得处理的地方，但不能用一个事后编出的分数替代实际比较。候选修补需要在真实执行中证实它确实改变了预期行为。

### 根据原因选择修改位置

建议让外层改进器在一个明确的修改空间内工作，起初只开放足够回答研究问题的模块。它可以修改提示与经验、修复工具实现、添加高层 action，或更新环境条件；不应因为所有问题都进入同一个循环，就强迫所有问题产生同一种修改。

| 轨迹中观察到的现象 | 候选修改 | 需要保留的检查 |
|---|---|---|
| 反复误解同一规则或工具用法 | 调整提示或可检索经验 | 新情境中是否仍正确理解 |
| 定位 操作顺序或参数处理反复出错 | 修复代码或工具接口 | 参数变化与相关功能回归 |
| 稳定操作重复触发逐步推理 | 生成参数化 action | 前置条件 结果读回与异常出口 |
| 相似页面在不同条件下结果不同 | 补充或拆分环境条件 | 是否错误合并了隐藏状态 |
| 当前信息不足以唯一决定 | 保留运行时判断或询问 | 询问是否必要且符合业务规则 |

为避免把人的经验分类当成研究结论，第一轮可以从这组可解释分类开始，同时设置通用修改器对照。只有它在相同资源条件下产生更有效的修改，才有理由保留复杂的分类和路由机制。

### 从有出处的交互知识生成 action

环境知识层拟区分“实际观察”与“归纳规则”。例如，“这些轨迹中选择某类费用后出现了某字段”是观察；“此费用类型总需要该字段”是尚待验证的规则。知识记录可以关联原始步骤、已知账号或会话条件、应用版本、支持实例和反例。没有观察到的条件保留为未知，而不是补出看似完整的环境模型。

一个可复用 action 应具备输入参数、适用条件、执行过程、预期效果和异常出口。历史金额、对象 ID、当前可选项目等动态数据不能固化为常量；应保存其读取方法，运行时重新取得。适用条件不满足、控件或选项发生变化、执行后缺少预期效果时，action 返回失败位置和当前观察，交回原有 agent 处理。

第一阶段建议限定为：提取知识时只使用既有业务日志。这样可以单独检验旧日志的价值，但验证生成的 action 仍需要环境运行。若日志覆盖不足，可在后续独立条件中加入定向探索，并单列探索成本；不能把补采数据后的效果仍归因于“只用历史日志”。

显式图结构不是前提。若有条件的记录和动作契约已经足够，就不必先构建完整状态机。反过来，如果相似页面的隐藏条件导致大量错误复用，结构化表示才可能值得投入。实验应允许简单文字经验或直接技能生成成为更好的方案。

### 用独立检查决定保留 回滚或继续试验

候选版本先经过静态和局部检查，再在可重置的环境中运行相关任务与回归任务。筛选同时关注业务结果和运行开销。一个修改可能减少模型调用，却增加环境操作或验证负担；是否接受，取决于事先明确的质量条件和主要优化目标，而不是要求所有指标每轮都下降。

规则手册可以支持测试构造：由模型提出覆盖不同条件的案例，再由程序约束和人工确认形成可信的预期结果。这是另一份讨论草稿提供的候选思路，本计划把它放在验证层。生成器不能修改已确认的规则、判分程序或预期答案；预期结果不仅包含最终表单或数据库状态，也可以包含必须询问、必须拒绝以及不得跳过的程序要求。[21][22]

可用于开发和筛选的测试反馈属于优化信号。真正的最终测试必须另行保留，在方案和版本选择结束后使用；不能一边根据其结果调整系统，一边称其为未见测试。为避免评测器自身的偏差，需抽样核对成功、失败以及争议轨迹，并报告判分误差对结论的影响。[20]

### 一个贯穿两个方向的例子

假设在一个可重置的费用申报测试环境中，轨迹反复出现：agent 先填写普通费用页面，提交时才发现某个条件要求补充材料，随后返回修改。这是示意情境，具体规则应由实际业务材料确认。

分析器首先检查触发条件。若是已有规则没有传达给执行者，可修改提示；若是检查和填充步骤稳定，可生成带条件检测的 action；若系统只在某账号或审批状态下出现该要求，则补充相应环境条件。action 可以读取页面、填入已知值并核对保存结果，但费用归类或材料真实性仍可能需要模型判断或用户输入。

验证器随后比较新旧版本在相关及不相关条件下的行为。若新版本确实避免返回修改，而且没有漏问、漏填或违反规则，才支持保留。如果它只是在原始实例上更快，或者因为跳过检查而省时，就应被拒绝。这个例子说明：优化可能来自避免一整段错误路径，也可能来自把路径中的多次推理改为程序执行；两者需要分别测量。

## 五 需要回答的研究问题

**问题一 诊断和修改选择是否有价值。** 与仅更新文字提示、以及不使用专门诊断结构的通用自动修改器相比，按轨迹证据选择修改位置，能否在相同改进资源下更快找到有效且不退化的版本？这首先是目标场景中的前置验证，因为 HarnessFix 已有明确的诊断和修改路由。若进一步主张利用成功但高成本轨迹、按实际开销与复用机会排序更有效，还需与使用相同诊断但不含这一机制的版本比较。如果通用修改器已经达到同样效果，就不应把额外的诊断分类作为必要贡献。

**问题二 显式环境条件是否值得维护。** 与同样日志产生的文字经验、以及直接从轨迹生成技能相比，带出处、适用条件和未知状态的环境知识，能否减少错误复用和无效回退？其检查与维护开销会不会抵消收益？这里考察的是这一中间层的增量价值，而不是笼统证明“记忆有用”。

**问题三 自动改进是否带来可持续的净收益。** 改进投入能否被后续工作节省的时间与费用抵消，何时抵消，在任务变化或环境变化后是否仍成立？如果只有运行阶段便宜、但在合理使用量内无法收回学习和验证投入，就应报告其适用边界。

这三项问题对应可被推翻的假设，不预设答案。只有在明确对照上得到稳定证据，才把诊断选择、环境表示或接受机制中的有效部分提炼为方法贡献。若组合系统只有工程整合效果，也应如实表述。

## 六 实验如何支撑这些判断

### 从最小对照开始 再增加必要消融

主实验建议先比较下列条件。每组使用同一任务执行模型、基础工具、原始日志和任务分布；外层调用、环境交互与重试额度有共同上限，同时记录实际消耗。共同上限保证机会可比，实际消耗用于检验效率。

| 条件 | 核心配置 | 主要回答的问题 |
|---|---|---|
| 当前系统 | 不加入新的跨任务改进机制 | 相对现状是否有效 |
| 文字经验 | 同批轨迹形成提示或检索经验 | 仅增加经验能得到多少收益 |
| 通用自动修改 | 同样修改权限与外部验证 不增加本方案专门诊断和环境结构 | 通用自动优化能覆盖多少效果 |
| 完整候选方案 | 诊断选择 环境知识 动作生成与统一验证 | 组合方案是否有额外净收益 |

这些对照首先检验完整系统是否值得做，不能单独分解两个方向的贡献。若要声称某一方向有独立价值，需增加仅诊断修复、仅环境学习以及两者组合的组件比较，并让它们共用验证设施。诊断修复模块仍可直接生成工具；关闭环境知识层不能同时剥夺它写 action 的权限。

随后根据观察选择消融。若主张环境层有价值，需要增加“直接生成技能，保留同样验证与基础回退，但去掉独立环境知识层”的对照；若主张持续维护，则比较冻结知识和允许更新；若主张定向探索更划算，则另设相同额外交互额度的探索比较。不要通过取消对照组的基本错误检测或给完整方案更多机会制造优势。

若要识别诊断结构的增量，还需在保持环境模块相同的情况下开关诊断模块；若要识别成本优先级，则保留相同诊断，只去掉该优先级。先依据具体主张决定这些对照，不一次铺开全部组合。

近期论文可以作为实现参考，但上述条件首先是组件对照，不冒充完整复现论文系统。若正式研究要声称优于某篇最近邻，需要再核对代码、模型、任务和资源条件，完成可比复现或清楚说明适配差异。

### 让数据隔离对应实际声称的泛化

建议区分开发与搜索任务、候选筛选任务和最终测试任务。前两者的反馈会参与优化，不能被当作最终无偏估计。最终测试在搜索停止、候选选择完成后使用。若需要学习过程曲线，可预先保存若干检查点，待冻结后统一运行最终测试，避免曲线结果反过来决定下一轮修改。

同模板的新参数，只能支持实例泛化。若希望声称学会了新流程或新规则组合，应另留出相应结构；若只在一个系统验证，就不能直接推广到所有 Web agent。日志、规则案例和测试任务之间也要检查是否共享答案、对象或近乎相同的执行路径。

持续学习另设按时间顺序到达的任务流：当前任务只能利用过去已经允许看到的运行反馈，未来任务及其答案不提前暴露。报告不同任务顺序和随机重复下的变化，避免把恰好先遇到关键页面的一种顺序当成普遍效果。已有研究专门指出自改进评估对顺序、方差和未明确条件的敏感性。[23]

### 同时报运行效果与完整投入

| 指标 | 建议口径 | 防止哪种误读 |
|---|---|---|
| 任务质量 | 正确完成率 关键规则符合率 必要询问与人工接管 | 少做检查也被当作加速 |
| 运行时间 | 所有尝试的端到端时间及尾部情况 模型与环境等待分项 | 只统计成功运行或只算模型时间 |
| 运行费用 | 所有尝试的实际费用 输入 输出 缓存与工具费分项 | 用 token 总数代替不同单价下的金额 |
| 行为变化 | 模型调用 工具调用 环境操作 重试与回退分别统计 | 高层 action 变少就被说成环境步骤变少 |
| 完整投入 | 分析 生成 探索 验证 失败运行 维护及业务执行分别记账 | 把运行节省当成净收益 |

执行账本的总费用除以正确完成的任务数，给出包含失败尝试的每成功执行费用。另在指定使用窗口内，将准备、执行及学习维护费用合计后除以正确完成数，得到生命周期的每成功费用；研究用的额外对照和最终测评费用不进入这个分子。若没有成功任务，这些指标应报告为未定义，不能记为零。还应同时报告成功率与每次尝试费用，避免一个比值掩盖质量变化。人工整理、规则确认和额外接管时间单列，不默认其免费，也不随意折算为金额。

时间需要区分用户等待与离线改进耗时。后台优化所用的总计算时长不能直接加成每次任务的用户等待；若优化阻塞服务，则应计入相应关键路径。费用可累计计账，时间则应明确串并行和是否阻塞，不用一个含混的“总成本”包办二者。

还应把部署执行、学习维护和研究测评分成三个账本。额外的对照实验与最终测评进入研究预算，不自动成为部署每个任务的负担；系统实际需要的回归、重学和运行检查则必须进入学习维护或执行开销。各组共用准备工作的分摊口径一致，不能默认基线没有准备和维护成本。

质量接受条件与统计精度应在小规模试验后、正式比较前确定。建议以业务质量为约束，明确主要优化目标，并同时展示时间与费用的取舍。一次点估计“不下降”不足以证明无退化；需要任务级配对、适当重复和不确定性报告。若效率收益只存在于少数模板或成功子集，应按范围报告。

净收益应沿同一任务序列比较累计实际投入。学习阶段可能先更贵，后续才逐渐收回；若累计节省始终未覆盖额外的学习与维护投入，就报告未收回。预算计算将建立在这些实测字段和最终选定的任务规模上，而不是现在预填一个看似精确的总数。

## 七 回到前两部分的时间与费用框架

### 框架能解释改进结果 但不直接给出学习方法

前两部分的模型与本计划有关联，割裂感主要来自讨论层次不同。Time 和 Money 公式描述一个既定 agent 设计如何产生执行开销；本计划研究怎样利用历史执行，把这个设计改得更好。按照 PPT 的记号，设计 m 包含模型与执行框架，任务是 p。我们首先改变的是 m，随后才观察公式中的哪些项改变。轨迹分析本身不会使任何执行项自动下降。

沿用当前 PPT 对一次任务尝试的定义：

$$T_{\mathrm{attempt}}=\sum_{i=0}^{N}(D_i+E_i)-T_{\mathrm{saving}},\qquad D_i=\sum_{j=1}^{J_i}\ell_{ij}$$

$$c_m(p)=\sum_{i=0}^{N}\sum_{j=1}^{J_i}\sum_{\kappa\in K}n^{\kappa}_{ij}c_\kappa(\mu_{ij})+x_{\mathrm{env}}c_{\mathrm{env}}$$

这里 N 是 observe–decide–act–wait 的轮数，Jᵢ 是该轮所有模型调用数，Dᵢ 是模型时间，Eᵢ 是观察、操作、等待和框架处理等非模型时间。费用由各类 token 用量及对应单价、再加被计费的环境用量构成。上述是前两部分从文献改编和补充的分析表达，并非声称某篇论文原样提出了整套公式；来源与改编边界保留在 PPT 附录 A0。具体符号与页面依据见仓库的[公式衔接核查](../research/2026-09-29-part3-report-support.md)。

### 具体修改通过什么行为影响哪些项

| 计划中的修改 | 可能改变的执行行为与公式项 | 同时需要检查的代价 |
|---|---|---|
| 修提示 代码或决策流程 | 少走错误路径 可减少无效 N 和轮内重试 Jᵢ 也可能提高成功率 Rₘ(p) | 更长提示 额外裁判调用 或过早停止 |
| 把已知操作交给参数化 action | 少做重复模型决策 总调用数 ΣᵢJᵢ 及总输入输出 token 可能下降 | 底层操作仍需执行 条件检查与回退仍有费用 |
| 用环境条件选入口和读取路径 | 减少试探和无效操作时 才可能减少总非模型时间 ΣᵢEᵢ | 检索 检测 动态参数处理和知识维护 |
| 用结构化结果替代重复读整页 | 可减少观察与历史上下文长度 进而减少输入 token 和部分预填充时间 | 工具说明与记忆增大上下文 修改前缀可能影响缓存 |

这张表给出的是可检验的因果路径，不是预先承诺的下降箭头。减少调用会省去被移除调用的耗时；总模型时间是否下降，还取决于剩余调用的延迟，以及是否新增了模型检查。非模型检查也可能抵消端到端时间收益。在保持同一模型和服务档位时，本计划并不直接降低 token 单价或 TPOT；若没有专门改变调度，也不应主张并发增加更多时间抵扣。我们没有必要让方案覆盖公式中的每个项。

尤其要分清动作粒度。假设一次模型决策调用一个 action，action 内仍执行原来的多次点击。从外层轮数看，N 可能变小，每轮的环境工作却变多；若保留原来的细粒度检查点，也可以把内部纯代码步骤记成 Jᵢ = 0。这可能是同一批被省掉的模型调用的两种描述，不能当成两个独立收益相乘。底层点击数量是否减少，必须另行记录。若还避免了错误导航、重复截图或等待，才有额外的环境开销收益。

成功率是另一条关联。修复可能主要提高 Rₘ(p)，并不降低单次尝试的时间或费用，却减少完成任务所需的失败尝试。PPT 的每成功口径可以解释这一点，但固定设计下的 Cₘ(p) / Rₘ(p) 及相应时间表达有重试假设。持续更新版本、任务不相同或失败相互关联时，应以实际任务流计账，不能把一个固定比值直接当成在线完成成本预测。

### 学习本身需要扩展观察窗口

单次执行公式能解释“改好的版本为什么可能更快、更便宜”，但无法单独回答“花钱把它改好是否值得”。跨任务的轨迹分析、知识构建、代码生成、候选验证和探索属于额外投入，不能都塞进单次尝试的 i = 0。i = 0 在现有框架里容纳的是本次尝试内、未归某个行动轮的调用，例如开头的规划。

本计划因此保留原公式，并增加生命周期账本：在同一批业务任务上，累计准备费用、实际执行费用，以及期间发生的学习、验证、探索和维护费用。各项只记一次，与基线采用相同边界。PPT 附录 B8 已讨论一次性建设费用的摊销；持续改进则需要把后续维护和再次学习也计入。这个补充是扩大测量范围，不是另造一个执行瓶颈，也不是方法创新本身。

### 前两部分其实已经包含了直接近邻

重新核对当前 PPT 后，不能说此前遗漏了整个方向。它按“执行时减少哪个项”组织文献，把学习机制分散在编译、复用、技能与附录中；第三部分按“从什么反馈学习、学成什么、怎样验证和更新”组织，于是同一批工作显得像另一条线。

| 相关工作 | 当前 PPT 中的实际位置 | 与本计划的关系 |
|---|---|---|
| AutoDroid V2 与 MobileGPT | 主线 Calls per step 及附录 B1 | 学过的脚本或子任务替代重复模型决策 |
| WALT | 主线 Number of steps | 探索环境并生成工具 已包含学习过程和建设代价 |
| ActionEngine 与 AppAgentX | 附录 B1 Compile or replay | 环境状态机或历史交互支持程序化动作 |
| AWM 与 SpeedRunner | 附录 B2 Fewer steps | 从经验归纳工作流 或由 coding agent 更新程序技能 |
| SpeedRunner 的开销核算 | 附录 B0 与 B8 | 已涉及技能归纳费用的摊销 |

SkillWeaver 在前期配套研究中已有核查，但当前 PPT 生成器没有对应条目，应区分“查过”与“已经展示”。本表只定位现有内容，不沿用各行中不同版本、模型或统计口径的数字来拼接新结论。

因此，第三部分可以自然承接为：**前两部分解释了哪些执行工作耗时花钱、已有机制怎样改变这些工作；我们要研究 agent 能否从自己的轨迹自动发现值得改的地方，形成合适的提示、代码或动作，并在可靠验证后持续采用这些改进。** WALT、SpeedRunner、ActionEngine 以及新补读的自动框架优化工作都是这一计划的近邻，不能用“我们在外层学习”把它们排除。公式用来追踪最终收益和失败原因，文献与对照实验用来判断所提方法是否有增量价值。

## 八 分阶段开展与判断是否继续

**第一阶段 建立可复现的观察。** 选择可访问、可重置且有可靠结果依据的工作流，整理成功和失败轨迹，测量现有系统的时间与费用组成，确认是否存在高频错误或可复用操作。产出应包括基础执行器、记录格式、质量检查和数据划分。如果任务无法复现、结果无法独立判断，先解决实验基础，不急于让修改循环自动运行。

**第二阶段 分别验证两类改进。** 先运行轨迹诊断到候选修改的最小循环，再验证同批日志得到的文字经验、直接技能与环境条件层的差别。产出有效与无效修改案例、组件对照以及每轮实际开销。若简单方法已经足够，保留简单方法；若生成的动作大多不能通过验证，先定位原因，不用增加自主循环次数掩盖问题。

**第三阶段 检验组合与长期投入。** 在两个组件均能稳定运行、记录和评价后，运行组合系统和必要消融，检验跨参数、跨流程或连续任务流的效果。若要讨论环境变化后的修复或额外探索，再加入对应实验。产出质量约束下的时间与费用结果、累计收益曲线和失败范围。

**第四阶段 决定扩展与预算。** 根据前三阶段实测，决定是否引入训练过的外层编辑器、第二个环境或更广泛任务。强化学习只有在反馈可信、修改空间明确、重复搜索值得摊销时，才成为有理由投入的候选。此时再根据任务运行、候选数量、重复实验、验证与维护等开销计算预算。

本计划最先需要确定的是目标工作流及日志可用性、第一轮优先检验的假设，以及质量依据和允许的改动范围。这些选择决定实验规模与预算。现阶段值得推进的是一个能检验上述问题的最小系统，而不是预先承诺一个覆盖所有环境、全自动持续优化的通用平台。

## 参考文献

以下仅列正文实际引用的文献。正式发表的工作给出发表信息；未独立确认正式发表的近期工作按预印本列出，并注明符合来源要求的机构。正式引用与实际核读版本分开，方法比较以列出的阅读版本为准。本报告没有把机构资质等同于结论可靠性，也没有把论文报告的效果当作已复现结果。

[1] Shaokun Zhang; Jieyu Zhang; Jiale Liu; Linxin Song; Chi Wang; Ranjay Krishna; Qingyun Wu (2024). *Offline Training of Language Model Agents with Functions as Learnable Weights*. ICML 2024, main conference; Proceedings of Machine Learning Research 235:60315–60335。[论文](https://proceedings.mlr.press/v235/zhang24cd.html)。

实际核读版本：[arXiv 2402.11359v4](https://arxiv.org/html/2402.11359v4)。

[2] Lakshya A Agrawal; Shangyin Tan; Dilara Soylu; Noah Ziems; Rishi Khare; Krista Opsahl-Ong; Arnav Singhvi; Herumb Shandilya; Michael J Ryan; Meng Jiang; Christopher Potts; Koushik Sen; Alex Dimakis; Ion Stoica; Dan Klein; Matei Zaharia; Omar Khattab (2026). *GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning*. ICLR 2026, main conference。[论文](https://proceedings.iclr.cc/paper_files/paper/2026/hash/0e9e708b6f48e14fd0ac29e167413f76-Abstract-Conference.html)。

实际核读版本：[arXiv 2507.19457v2](https://arxiv.org/pdf/2507.19457v2)。

[3] Jenny Zhang; Shengran Hu; Cong Lu; Robert Lange; Jeff Clune (2026). *Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents*. ICLR 2026, main conference Poster。[论文](https://iclr.cc/virtual/2026/poster/10007327)。

实际核读版本：[arXiv 2505.22954v2](https://arxiv.org/html/2505.22954v2)。

[4] Mengzhuo Chen; Junjie Wang; Zhe Liu; Yawen Wang; Haiming Zheng; Qing Wang (2026). *From Failed Trajectories to Reliable LLM Agents: Diagnosing and Repairing Harness Flaws*. arXiv 预印本，正式发表未独立确认。[论文](https://arxiv.org/html/2606.06324v2)。

实际核读版本：[arXiv 2606.06324v2](https://arxiv.org/html/2606.06324v2)。 机构：State Key Laboratory of Complex System Modeling and Simulation Technology, Beijing, China; Institute of Software, Chinese Academy of Sciences, Beijing, China; University of Chinese Academy of Sciences, Beijing, China; School of Computer Science and Technology, Tianjin University, Tianjin, China。

[5] Esakkivel Esakkiraja; Denis Akhiyarov; Vikas Yadav; Sai Rajeswar; Patrice Bechard; Sridhar Nemala; Sagar Davasam (2026). *StarHarness: Evolving Harnesses with Stratified Search for Enterprise Environments*. arXiv 预印本，正式发表未独立确认。[论文](https://arxiv.org/pdf/2608.24804v1)。

实际核读版本：[arXiv 2608.24804v1](https://arxiv.org/pdf/2608.24804v1)。 机构：ServiceNow; Mila; Université de Montréal。

[6] Yifan Zhang; Yutong Dai; Juntao Tan; Luyu Yang; Rishi Mullur; Thai Hoang; Zhiyuan Hu; James Zhu; Phil Mui; Silvio Savarese; Ran Xu; Zeyuan Chen (2026). *DarwinX: Evolving Agent Harnesses Through Natural Selection*. arXiv 预印本，正式发表未独立确认。[论文](https://arxiv.org/pdf/2608.07545v1)。

实际核读版本：[arXiv 2608.07545v1](https://arxiv.org/pdf/2608.07545v1)。 机构：Salesforce AI Research; Salesforce Agentforce。

[7] Shuai Shao; Kangning Zhang; Qingyao Li; Shijian Wang; Hao Wang; Wenxiang Jiao; Yuan Lu; Yi Guo; Weiwen Liu; Weinan Zhang (2026). *Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories*. arXiv 预印本，正式发表未独立确认。[论文](https://arxiv.org/pdf/2608.02276v1)。

实际核读版本：[arXiv 2608.02276v1](https://arxiv.org/pdf/2608.02276v1)。 机构：Shanghai Jiao Tong University; Southeast University; Xiaohongshu Inc.。

[8] Minghao Chen; Yihang Li; Yanting Yang; Shiyu Yu; Binbin Lin; Xiaofei He (2024). *AutoManual: Constructing Instruction Manuals by LLM Agents via Interactive Environmental Learning*. Advances in Neural Information Processing Systems 37 (NeurIPS 2024), Main Conference Track。[论文](https://proceedings.neurips.cc/paper_files/paper/2024/hash/0142921fad7ef9192bd87229cdafa9d4-Abstract-Conference.html)。

实际核读版本：[arXiv 2405.16247v4](https://arxiv.org/html/2405.16247v4)。

[9] Yao Fu; Dong-Ki Kim; Jaekyeom Kim; Sungryull Sohn; Lajanugen Logeswaran; Kyunghoon Bae; Honglak Lee (2024). *AutoGuide: Automated Generation and Selection of Context-Aware Guidelines for Large Language Model Agents*. Advances in Neural Information Processing Systems 37 (NeurIPS 2024), Main Conference Track。[论文](https://proceedings.neurips.cc/paper_files/paper/2024/hash/d8efbb5dd415974eb095c3f06bff1f48-Abstract-Conference.html)。

实际核读版本：[arXiv 2403.08978v2](https://arxiv.org/html/2403.08978v2)。

[10] Zora Zhiruo Wang; Jiayuan Mao; Daniel Fried; Graham Neubig (2025). *Agent Workflow Memory*. Proceedings of the 42nd International Conference on Machine Learning (ICML 2025), PMLR 267:63897–63911。[论文](https://proceedings.mlr.press/v267/wang25bx.html)。

实际核读版本：[arXiv 2409.07429v1](https://arxiv.org/html/2409.07429v1)。

[11] Haiteng Zhao; Chang Ma; Guoyin Wang; Jing Su; Lingpeng Kong; Jingjing Xu; Zhi-Hong Deng; Hongxia Yang (2024). *Empowering Large Language Model Agents through Action Learning*. Conference on Language Modeling (COLM 2024), main conference。[论文](https://openreview.net/forum?id=KqK5XcgEhR)。

实际核读版本：[arXiv 2402.15809v2](https://arxiv.org/html/2402.15809v2)。

[12] Viraj Prabhu; Yutong Dai; Matthew Fernandez; Krithika Ramakrishnan; Jing Gu; Yanqi Luo; Silvio Savarese; Caiming Xiong; Junnan Li; Zeyuan Chen; Ran Xu (2026). *WALT: Web Agents that Learn Tools*. International Conference on Learning Representations (ICLR 2026), Conference / poster。[论文](https://proceedings.iclr.cc/paper_files/paper/2026/hash/5b175f9e93873e3a10a6ce43dbb82e05-Abstract-Conference.html)。

实际核读版本：[arXiv 2510.01524v1](https://arxiv.org/html/2510.01524v1)。

[13] Boyuan Zheng; Michael Y. Fatemi; Xiaolong Jin; Zora Zhiruo Wang; Apurva Gandhi; Yueqi Song; Yu Gu; Jayanth Srinivasa; Gaowen Liu; Graham Neubig; Yu Su (2025). *SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills*. arXiv 预印本，正式发表未独立确认。[论文](https://arxiv.org/html/2504.07079v1)。

实际核读版本：[arXiv 2504.07079v1](https://arxiv.org/html/2504.07079v1)。 机构：The Ohio State University; University of Virginia; Purdue University; Carnegie Mellon University; Cisco Research。

[14] Hongbin Zhong; Fazle Faisal; Luis França; Tanakorn Leesatapornwongsa; Adriana Szekeres; Kexin Rong; Suman Nath (2026). *ActionEngine: From Reactive to Programmatic Web Agents via State Machine Memory*. arXiv 预印本，正式发表未独立确认。[论文](https://arxiv.org/html/2602.20502v2)。

实际核读版本：[arXiv 2602.20502v2](https://arxiv.org/html/2602.20502v2)。 机构：Georgia Institute of Technology; Microsoft。

[15] Wenjia Jiang; Yangyang Zhuang; Chenxi Song; Xu Yang; Joey Tianyi Zhou; Chi Zhang (2025). *AppAgentX: Evolving GUI Agents as Proficient Smartphone Users*. arXiv 预印本，正式发表未独立确认。[论文](https://arxiv.org/html/2503.02268v3)。

实际核读版本：[arXiv 2503.02268v3](https://arxiv.org/html/2503.02268v3)。 机构：Westlake University AGI Lab; Henan University; Southeast University; A\*STAR Institute of High Performance Computing (IHPC); A\*STAR Centre for Frontier AI Research (CFAR)。

[16] Zixi Huang; Xiheng Wang; Andrew Wang; William Jurayj; Bernal Jiménez Gutiérrez; Daniel Khashabi; Nicholas Andrews (2026). *Better, Faster, Stronger: Programmatic Skill Learning Best Reduces Agent Cost*. arXiv 预印本，正式发表未独立确认。[论文](https://arxiv.org/html/2608.11338v1)。

实际核读版本：[arXiv 2608.11338v1](https://arxiv.org/html/2608.11338v1)。 机构：Johns Hopkins University。

[17] Siru Ouyang; Jun Yan; I-Hung Hsu; Yanfei Chen; Ke Jiang; Zifeng Wang; Rujun Han; Long T. Le; Samira Daruki; Xiangru Tang; Vishy Tirumalashetty; George Lee; Mahsan Rofouei; Hangfei Lin; Jiawei Han; Chen-Yu Lee; Tomas Pfister (2026). *ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory*. ICLR 2026, main conference, poster。[论文](https://iclr.cc/virtual/2026/poster/10007887)。

实际核读版本：[arXiv 2509.25140v2](https://arxiv.org/pdf/2509.25140v2)。

[18] Haozhe Liu; Tian Ye; Sensen Gao; Qihang Cao; Yitong Li; Mingchen Zhuge; Duomin Wang; Ruihua Zhang; Ping Luo; Jiawang Bian; Lei Zhu; Ligeng Zhu; Enze Xie; Song Han (2026). *SoL-Pi: Recursively Scaling Auto-Research Loops for Efficient Agent Harness*. arXiv 预印本，正式发表未独立确认。[论文](https://arxiv.org/html/2609.20519v1)。

实际核读版本：[arXiv 2609.20519v1](https://arxiv.org/html/2609.20519v1)。 机构：NVIDIA; NTU; MIT。

[19] Peng Xia; Rujun Han; Zifeng Wang; Yanfei Chen; Yufan Zhuang; Yoonho Lee; Chengsong Huang; Han Yu; Zhongying CuiZhu; Yifei Ming; Huaxiu Yao; Burak Gokturk; Tomas Pfister; Chen-Yu Lee (2026). *RRSI: Regularized Recursive Self-Improvement of Agent Harnesses*. arXiv 预印本，正式发表未独立确认。[论文](https://arxiv.org/html/2609.24972v2)。

实际核读版本：[arXiv 2609.24972v2](https://arxiv.org/html/2609.24972v2)。 机构：Google Cloud AI Research; Stanford University; Washington University in St. Louis; UNC-Chapel Hill。

[20] Xing Han Lù; Amirhossein Kazemnejad; Nicholas Meade; Arkil Patel; Dongchan Shin; Alejandra Zambrano; Karolina Stanczak; Peter Shaw; Christopher Pal; Siva Reddy (2025). *AgentRewardBench: Evaluating Automatic Evaluations of Web Agent Trajectories*. COLM 2025，主会；作者按官方名单。[论文](https://openreview.net/forum?id=fQcUZMPIvu)。

实际核读版本：[arXiv 2504.08942v2](https://arxiv.org/html/2504.08942v2)。

[21] Zekun Li; Shinda Huang; Jiangtian Wang; Nathan Zhang; Antonis Antoniades; Wenyue Hua; Kaijie Zhu; Sirui Zeng; Chi Wang; William Yang Wang; Xifeng Yan (2025). *SOPBench: Evaluating Language Agents at Following Standard Operating Procedures and Constraints*. arXiv 预印本，正式发表未独立确认。[论文](https://arxiv.org/html/2503.08669v2)。

实际核读版本：[arXiv 2503.08669v2](https://arxiv.org/html/2503.08669v2)。 机构：University of California, Santa Barbara; Google DeepMind。

[22] Da Song; Yuheng Huang; Boqi Chen; Tianshuo Cong; Randy Goebel; Lei Ma; Foutse Khomh (2026). *Evaluating Implicit Regulatory Compliance in LLM Tool Invocation via Logic-Guided Synthesis*. arXiv 预印本，正式发表未独立确认。[论文](https://arxiv.org/html/2601.08196v1)。

实际核读版本：[arXiv 2601.08196v1](https://arxiv.org/html/2601.08196v1)。 机构：Shandong University; The University of Tokyo; McGill University; University of Alberta; Polytechnique Montréal。

[23] Qinyuan Ye; Yu Li; Yada Pruksachatkun; Jiaxin Zhang; Chien-Sheng Wu (2026). *On the Fragility of Self-Improving Agents: Variance, Task Order, and Underspecification*. arXiv 预印本，正式发表未独立确认。[论文](https://arxiv.org/pdf/2608.18066v2)。

实际核读版本：[arXiv 2608.18066v2](https://arxiv.org/pdf/2608.18066v2)。 机构：Salesforce AI Research。
