# Claude 综述挖掘报告复核：技能、工具与 harness

审阅日：2026-09-30。对象：`notes/part3/2026-09-30-self-improvement-survey-mining-zh.md` 的 §3.3–3.4 全文、§7 对应成本行；连带核查 §2.3 的工具映射和 §8.1 的研究结论。以下仅使用 CT 局部编号，不分配全局 E/D 编号，不修改原报告。

本轮完整读了上述报告范围，并对照 `research/2026-09-30-part3-survey-mining-ledger.md`、`research/2026-09-30-part3-records-s.md` 及既有原文证据。对十篇核心论文重新读取缓存中的原始 PDF 方法、实验和相关附录；不是对报告所列 82 篇重新全文审查。SICA Table 1、HGM Table 2、GenericAgent Table 8、Metis Table 1、RQGM Figure 9 和 Continual Harness Figure 17 另用原始 PDF 页面图核对。定位均为 PDF 文件页，从第一页计数；论文页码一致时不另列。下述数字均为一手论文数据，版本日期在 References 列明，核查日期统一为 2026-09-30；百分比计算另标 calc.。

## 1. 核查表与原文证据

| 局部 ID | 对应原报告 / 账本 | 判定 | 对研究判断的影响 |
|---|---|---|---|
| CT01 | §7.3(1)，E1095 / D536 | 必须改：分配 CPU 小时不能量化墙钟重叠 | HGM 支持改进搜索资源效率，不直接支持部署并行节省 |
| CT02 | §3.4 首段，s048#12–13 | 必须补实验分支边界 | Continual Harness 也包含参数训练，不能把整篇算作全流程免训练 |
| CT03 | §7.1 Continual 行，E1307 / D545 | 必须改：累计量被写成每次上下文量 | 图不能证明单次模型输入缩短一个数量级 |
| CT04 | §3.4、§7.1 Adaptive 行，E1116–1117 | 数字支持；单位和映射须改 | 工具调用不等于模型决策步数；token 是任务流合计 |
| CT05 | §2.3 工具行 | 必须加条件 | 工具化后非模型时间可能下降，也可能上升 |
| CT06 | §3.4 HGM 代表性段，E1057、E1093 | 精确化术语 | 理论 CMP 与经验估计不同；动态分配评估不等于任务执行早停 |
| CT07 | §3.4 SICA，E669、E1099–1102 | 主要数字、公式支持；补原文口径未解释处 | 最高准确率不是最后一轮；不能从 17%/53% 反推 50 题解出数 |
| CT08 | §3.3、§7.1 GenericAgent，E672 | 数字支持；保留顺序案例限定 | 首末变化不能被读作独立、因果隔离的代码化收益 |
| CT09 | §3.3、§7 Metis，E673–674、E904 | 支持现有主要边界 | 执行器 token 节省不是全系统部署美元或净回本 |
| CT10 | §3.4、§7 DGM / RQGM，E1088–1090、E683、E1132 | 支持；补混合 token 定义 | 搜索预算、价格折算不能当成最终 agent 推理加速 |
| CT11 | §3.3 SkillWeaver，E956、E963、E1210 | 支持 | 已有前置条件与失败测试，不能把条件化技能作为空白；160 次是探索迭代 |
| CT12 | §8.1 与 §9.1，SpeedRunner 已被列为未展开近邻 | 应补重要近邻，不是 82 篇范围内的事实纠错 | 已有以成本为主问题、部分摊销构建调用的代码技能方法 |

### CT01 — HGM：allocated CPU-hours 不能作为时间 V 的量化证据

**原句（§7.3(1)）**：

> 重叠（V）有数字的只有 HGM 的改进循环：800 次评估分配 CPU 小时 517 对 DGM 1,231（SWE-Verified-60；不是墙钟；作者把节省归因于异步并行扩展和评估）[E1095]

**建议新句**：

> HGM 报告了异步改进搜索的资源总量：在 SWE-Verified-60、同为 800 次任务评估的设置下，分配的 CPU 小时为 517，对照 DGM 为 1,231。作者将优势归因于异步扩展与评估，但该比较没有隔离异步机制，也没有报告可直接计算墙钟重叠节省的测量。因此这些数字应计入改进搜索资源账，不能作为时间 V 的定量证据。[E1095]

**原文核查**：[HGM v3](https://arxiv.org/pdf/2510.21614v3)，pp.7–9，§3.3、§4.2、Table 2。表述为 “allocated CPU-hours time required for 800 evaluations”。Table 2 的 517 / 1,231 和 56.7% / 53.3% 均核对无误。作者的确将资源优势解释为异步扩展和评估，并非报告凭空添加这一解释；问题在于报告进一步把它放进“重叠有数字”的类别。不同方法还改变了选择、扩展和评估调度，原表没有同步 HGM 对异步 HGM 的隔离消融。也不能反向断言节省主要由自适应评估预算造成——论文没有给出这一贡献分解。

**判定 / 范围**：实质性量纲和因果归类错误；无需删除 HGM 的搜索效率结果。§7.2 的资源账位置正确。此项也重申既有 D536，不新建全局差异编号。

### CT02 — Continual Harness 的固定模型分支与训练分支必须分开

**原句（§3.4 首段）**：

> 在本节核对过的文献里，θ 在绝大多数工作里不变；例外是 Harness-R1 训练一个单独的“harness 工程师”（目标 agent 不动）[E1051]。

**建议新句**：

> 本节主要比较固定任务模型的实验分支。Harness-R1 训练外层 harness 编辑器，因此不是全流程免训练；Continual Harness 同篇也包含模型与 harness 共同更新的分支，使用 SFT/GRPO 预热及在线 SFT。本节关于 Continual Harness 的效率结果仅引用其固定 Gemini 模型下的 harness 适配实验，不将训练分支纳入免训练证据。[E1051；s048#12–13]

**原文核查**：[Continual Harness v1](https://arxiv.org/pdf/2605.09998v1)，p.5 §3.3、p.7 §4.5、pp.25–28 Appendix D。原文明确：“Both the model weights θ and the harness state Ht are updated by this loop”。这不是只训练旁边一个记忆索引器，而是模型权重随外层迭代更新。固定 Gemini 的实验仍然可用于本研究；不应因此排除整篇。模型名称在原文 Gemini 3 / 3.1 之间有冲突，既有 D544 已记录，不宜在改句中自行统一成一个精确型号。

**判定 / 范围**：必须补分支边界；§8.4 的训练例外列表也应同步。此处不重审 Harness-R1 的训练细节，仅检查“唯一例外”是否成立。

### CT03 — Continual Harness：累计估计 token 不是单次上下文缩减倍数

**原句（§7.1 对应行）**：

> 每次运行费用；子 agent 上下文低一个数量级对应 t11

**建议新句**：

> 每次运行 API 费用；另有按角色累计的估计输入 token 曲线，子 agent 的累计量较低。Figure 17 的纵轴是累计量，且以提示字符数除以 4 估计 token，不能据此确认单次上下文缩短一个数量级，也不能单独量化 t11 的贡献。[E1140、E1307；D545]

**原文核查**：[Continual Harness v1](https://arxiv.org/pdf/2605.09998v1)，p.23 Figure 17(a)、§C.1.3，已查看页面图。图题写 “Cumulative approximate tokens by role”；纵轴也是累计 token。正文却把两条曲线约一数量级之差解释成每步节省。这是原文内部量纲张力，账本 D545 已注意到，报告成本映射中没有保留。角色的累计量还取决于调用频次，不能据此分离每次调用输入长度。

**判定 / 范围**：必须降格。每 24 小时运行的 Pro $130（100% 里程碑）对最小 harness $215（98%）可保留为原文对应实验结果，不能因这一 token 图的缺陷一并删掉；也不是“同成功率下完成全任务所需墙钟”的测量。

### CT04 — Adaptive Auto-Harness：工具调用、总 token 和总任务耗时分清

**原句（§7.1）**：

> FutureX：每题工具调用 13.4→4.2、输入 token 55.5M→25.6M、各任务耗时之和 34.2→6.6 h（不是墙钟，不含编排开销）；PolyBench 相反：1.0→5.4、35.3M→233.2M、25.6→59.5 h（同口径）

**原映射**：

> 时间 I（工具调用轮次）、费用 II；方向随任务流相反

**建议新句**：

> Full System 对 Sonnet (no-evo) 基线：FutureX 每题工具调用均值 13.4→4.2；整个任务流输入 token 合计 55.5M→25.6M；逐任务耗时相加为 34.2→6.6 h。PolyBench 三项分别为 1.0→5.4、35.3M→233.2M、25.6→59.5 h。耗时和不是整场实验墙钟，亦不含演化器编排开销；演化器 token 未被完整记录。工具调用减少不能不经定义就等同于模型决策步数 N 或每步模型调用数 J_i；输入 token 合计可记入对应费用项。[E1116–1117]

**原文核查**：[Adaptive Auto-Harness v2](https://arxiv.org/pdf/2606.01770v2)，p.13 Table 5 与其口径说明；p.19 Table 14。后者明确：“A turn is one tool call, including the final submit”。数字均支持。§3.4 的简略列举也应加上“输入 token 为整条任务流合计”，否则与前面的“每题”并列容易被读成每题 token。

**判定 / 范围**：数字正确，度量到 Part 1 分解的映射过强。不是要求删除时间 I，而是先核对轨迹中一步与工具调用如何对应，再判断哪些分项确实下降。

### CT05 — 工具封装对非模型时间的作用不是单向的

**原句（§2.3 工具行）**：

> I 步数；II 每步调用数（不经模型时为零）；IV 非模型时间不变或上升

**建议新句**：

> I/II：可能减少需要模型参与的决策或调用；IV：取决于封装后仍执行哪些原子操作。若原操作完全保留，主要省模型开销；若代码同时省掉重复观察、页面导航或数据处理，非模型时间也可能下降；生成、校验和失败恢复则可能增加开销。

**证据 / 推论边界**：这是本文的条件分析，不能标作某篇论文已经测出的普遍效应。SkillWeaver 的 Playwright API 和 SpeedRunner 的可执行技能允许技能内部执行多个操作；它们没有证明“所有工具化都保持或增加 IV”。反之，宏动作数变少也不直接证明 IV 减少。原句把可能出现的一种实现条件写成全称。

**判定 / 范围**：应改概念映射，不需新增数字或主张宏动作自动带来墙钟加速。

### CT06 — HGM：CMP 的定义与实际估计、评估调度与执行早停

**原句（§3.4 代表性工作）**：

> 用“团簇元生产力”（子树合并通过率）抽样父代、按单任务粒度评估并早停

**建议新句**：

> 用团簇元生产力的经验估计——子树累计成功评估数除以累计评估数——指导父代抽样，并把扩展与单任务评估解耦，动态地少评估不被看好的候选。理论 CMP 描述搜索结束后该子树可返回 agent 的期望效用，经验合并通过率是代理估计，不是理论量本身。[E1057、E1093]

**原文核查**：[HGM v3](https://arxiv.org/pdf/2510.21614v3)，pp.4–7，§2–3。理论部分的期望最终效用与实际累计成功率不能合并成一个定义；报告问题定义表给出的理论式本身基本清楚。这里的“早停”如果指少给低潜力节点更多任务预算，方向成立；若读者理解成提前终止单个部署任务或明确的阈值验收拒绝，则不是该结果。

**判定 / 范围**：术语精确化。§8.1 的“单任务粒度早停”亦宜改成“单任务粒度自适应分配评估预算”。

### CT07 — SICA：效用及费用数字正确，准确率分母需保留未解释处

**原句（§3.4）**：

> 50 题 SWE-bench 子集 17%→53%，但 53% 是第 14 轮，第 13 轮跌到 27%，打分与挑选用同一批题 [E1102]。

**建议新句**：

> 作者称使用固定随机抽取的 50 题 SWE-bench Verified 子集；Table 1 的 Benchmark Accuracy 列在第 0、14、15 轮分别为 0.17、0.53、0.51，53% 是最高表值而非最终轮。表值并非 50 题二值通过率应有的 2 个百分点整数倍，文中没有解释归一化或重复统计口径，不能据此还原解出题数；同一批题用于打分和选择。[E1102]

**原文核查**：[SICA v2](https://arxiv.org/pdf/2504.15228v2)，pp.4–6，Eq.1–2、实验设置、Table 1；p.6 表格图已核。表头为 “Average Metrics (per benchmark problem)”，正文称 “fixed random subset of 50 questions”。这一分母疑点已在 s063 记录中提示，报告缩写时遗漏。

**已支持部分，无需改值**：效用式的分数、费用、墙钟权重为 0.5 / 0.25 / 0.25，费用截断上限 $10、时间上限 300 s，超时再乘惩罚因子 0.5。四类基准按题统计的第 0 / 15 轮费用 $1.91 / $1.70、时间 130.2 / 114.5 s、token 0.24M / 0.30M，报告的约 −11% / −12% / +25% 是根据已四舍五入表值计算，应加 calc.。第 14 轮最高准确率行的费用是 $2.20，不能把最终轮费用配成“53% 且 $1.70”的同一实验端点。报告目前把轮次分开了，应保留。15 轮约 $7,000 是该次改进运行的 API 费用，非部署单题费用。

**判定 / 范围**：公式与主要成本结果支持；准确率分母属原文未解释处，不判断作者数字一定错误。缓存占比有记录不意味着已隔离证明费用下降由缓存导致。

### CT08 — GenericAgent：真实的九轮案例，不能升级成隔离因果实验

**原句（§7.1）**：

> 同一任务族九轮：运行时间 7m30s→1m38s，LLM 调用 32→5，总 token 222,203→23,010（单条序列，缓存读取全额计入）

**建议新句**：保留原句，并补：

> 每轮采用该任务族中的新实例；任务实例与经验状态随序列一起变化，因此首末差不能全部归因于代码化。总 token 包含按原始数量全额相加的缓存读取 token，也不是等额美元账单的降幅。

**原文核查**：[GenericAgent v1](https://arxiv.org/pdf/2604.17091v1)，pp.20–22 §4.4、Table 8，表格图已核。原文：“Each round operates on a new task instance”。第 1 轮为初始状态，第 2–5 轮主要文本 SOP，第 6–9 轮为代码 SOP；没有为这条演化曲线提供多条独立重复和冻结学习的配对序列对照。数值及单条序列限定正确。八个网页任务的三次重复是另一组协议，不应与九轮实验合成一个跨任务留出结论；报告 §8.2 A2 已正确保留这点。

**判定 / 范围**：保留现有证据，强化因果限定；不把该方法说成没有效率测量，也不把所有效率变化判作代码化造成。

### CT09 — Metis：主要数字与排除项支持

**核查对象**：§3.3 指向 §4 的 Metis 机制，以及 §7 的执行成本、反思成本。

**建议**：保留当前“执行器”和“不含轨迹生成”的限定；若压缩为表格，建议写：

> Metis 的执行 token 与轮数按 AppWorld 切分分别比较；它不是整条系统所有模型调用的总成本。一次性反思开销在官方切分 / 重采样切分分别为 7.9M / 11.8M token，不含轨迹生成。没有在这里报告完整生命周期美元净回本。[E673–674、E904]

**原文核查**：[Metis v1](https://arxiv.org/pdf/2606.24151v1)，pp.8–11，方法角色、实验设置、Table 1–2；p.10 表格图已核。原文成本限定：“trajectory-generation cost is excluded for all methods”。GPT-4o 执行器、Claude Sonnet 4.6 反思者设置下，官方切分执行器 token 112.6K→97.4K、轮数 14.55→11.25；重采样切分为 101.7K→78.5K、13.92→10.32。共同解出 62 题的比较另有 Table 2，不应和全测试集均值混用。单纯文本记忆本身也能减少 token；报告已有这一反例，应保留，不能用 Metis 支持“唯有代码能省成本”。

**判定 / 范围**：未发现上述主数据的新错误。代码化触发、编译检查与少量运行校验是具体机制，不等于函数语义在全部未来状态上已被证明正确。

### CT10 — DGM / RQGM：搜索成本的现有边界基本正确

**DGM 原句（§7.2）**：

> 一次 SWE-bench 运行约 $22,000（作者估计）、约 2 周

**建议**：保留并明确“改进搜索运行”。[DGM v3](https://arxiv.org/pdf/2505.22954v3)，pp.4–6、p.10 局限、p.32 Appendix E.1。其开放式搜索依赖冻结基础模型，修改自身仓库；入档条件包括可编译且保留自改代码能力，不是必须超过父代。成本讨论明确是 “is about USD 22,000”。原文的 SWE-bench 20%→50%、Polyglot 50 题子集 14%→38% 是不同评测条件，报告已分开。HGM 重新实现的 DGM 对照不应与原始 DGM 的价格和准确率当成同一运行。

**RQGM 原句（§3.4）**：

> 验证评估占搜索混合 token 的 65–69% [E683]；论文评审领域的消融里，搜索期把 task agent 换成 Nemotron 3 Ultra（元 agent 仍为 GPT-5.5），按 GPT-5.5 价格折算搜索费用降约 13 倍（价格折算，不是账单；作者预期收益因领域而异）[E1132]。

**建议新句**：保留，给“混合 token”加定义：

> 此处混合 token = 输入 token + 5×输出 token，统计改进搜索中的生成与评估调用；65–69% 是验证评估在该加权总量中的占比，训练侧评估另占 12–14%。约 13 倍是特定论文评审实验中更换搜索期任务模型后的价格等价估计，不是最终 agent 单题推理提速，也不是实付账单。[E683、E1132]

**原文核查**：[RQGM v2](https://arxiv.org/pdf/2606.26294v2)，p.7 成本定义、p.12 讨论、p.22 Appendix C、p.25 Figure 9（图已核）；原文加权口径：“output weighted at 5× input cost”。正文与附录仍称这是一项初步实证，单次运行及价格换算假设应保留。报告没有把 13 倍写成部署提速，这一边界正确。

### CT11 — SkillWeaver：验证漏洞、前置条件与探索迭代均有原文支持

**原句（§3.3）**：

> SkillWeaver 的“不抛异常即通过”放过了吞掉异常的坏函数 [E963]

**建议**：保留。也保留报告建议“验证最终状态”的表述，但不要说前置条件、参数化 API、条件匹配检索是我们新提出的空白。

**原文核查**：[SkillWeaver v1](https://arxiv.org/pdf/2504.07079v1)，pp.4–6 方法与设置、p.34 §D.2.1。作者指出 “malfunctioning APIs could be marked as verified”。API 文档已有初始页面等前置条件，选择候选 API 时会参考这些条件；错误处理可能吞掉异常，使验证标记不代表任务语义正确。每站 160 次是探索迭代预算，可包含技能练习或测试，不是 160 次模型调用，也不是墙钟或美元量。对应强模型构建、弱模型复用的成功率结果，不应自动转成净部署成本结论。

**判定 / 范围**：主要机制和漏洞描述支持。本轮检查上述方法和附录，没有宣称重新穷尽全文所有潜在成本描述；成本缺报的广泛结论应保留原审计的实际阅读深度。

### CT12 — SpeedRunner 是会影响研究建议的成本导向近邻

**原句（§8.1）**：

> 所以在本文核对过的范围内，没有找到以加速为主目标的自改进循环。这只说明检索范围，不作新颖性依据。

**建议新句**：不把上述有范围限定的句子判成错误；随后补充：

> 但本次综述条目范围之外、已在第 9.1 节提及的直接近邻 SpeedRunner，明确以降低 agent 推理成本为研究问题，并把技能归纳器调用按批次摊入每回合美元成本。它在三个模拟环境里从历史轨迹修改程序技能，模型参数不变。后续计划应将其纳入代码技能基线，不能把“由能力目标改为成本目标”本身当成尚无工作的空白；其论文也未完成企业网页环境或全生命周期净回本验证。

**原文核查**：[SpeedRunner v1](https://arxiv.org/pdf/2608.11338v1)，pp.2–6 方法与实验、p.10 局限、p.14 Appendix A.1–A.3。每回合成本按未缓存输入、缓存输入、输出分别乘 API 单价；计入 “sleep-time inducer calls amortized over the rollouts”。这超过“只报告部署 token、不记构建调用”的证据强度，但仍不是包含环境执行、失败恢复、维护、硬件及未来任务流的完整生命周期账。

**实验边界**：主实验所有角色为 GPT-5.4-mini；每任务族 200 次在线 rollout、每 10 次触发技能归纳、每 50 次在 30 个留出测试回合评估；每设置 3 个种子。这里的 training rollout 是经验收集/技能修改，不是基础模型权重训练。它没有独立候选技能的重放验证门，不等于研究实验没有留出测试集。成本图使用附录美元计算口径；不把图中笼统的 cost 直接写成墙钟。本文无需新增一个跨论文降幅排行榜。

**判定 / 范围**：重要近邻补充、研究建议补丁，不是要求改变原 82 篇的检索计数。来源机构为 Johns Hopkins University，符合强机构预印本补充资格。

## 2. 差异清单（仅局部 CT，不新建全局 D）

- **明确要改**：CT01、CT02、CT03、CT05。
- **保留数据并改度量映射**：CT04；现有 E1116–1117 数字不需重写。
- **原文口径应进一步说清**：CT06、CT07；CT07 为作者统计细节不明，并非已证实数据错误。
- **原结论主体支持**：CT08–CT11；保留其限制语比删掉结果更准确。
- **影响下一步方案的遗漏近邻**：CT12。原报告承认该文未在本轮展开，不能据此指控原报告虚报全文阅读。

CT01、CT03 与原账本 D536、D545 已有结论一致，是正文没有完整保留审计限定；无需重复创建全局冲突条目。CT02 的训练分支也已在 s048 记录中，不是新发现的模型训练方法。

## 3. 可直接应用的补丁索引

各 CT 条目上方已给出“精确原句 → 建议新句”，不另复写主报告。建议按以下顺序处理：

1. E1095 对应 §7.3(1)：使用 CT01，删除“重叠（V）有数字的只有 HGM”；§7.2 HGM 行保留。
2. §3.4 首段及 §8.4 训练边界：使用 CT02，添加 Continual Harness 训练分支排除条件。
3. E1307 对应 §7.1：使用 CT03，按累计估计 token 解释 Figure 17。
4. E1116–1117 对应 §3.4 和 §7.1：使用 CT04，补对照、合计量和工具调用定义。
5. §2.3 工具行：使用 CT05，把 IV 的方向改为实现相关。
6. E1057/E1093 对应 HGM 机制概述及 §8.1：使用 CT06，区分 CMP 与估计、动态评估与执行早停。
7. E1102 对应 SICA：使用 CT07，补分母未解释处；E1099–1100 的降幅标 calc.。
8. GenericAgent、Metis、DGM、RQGM、SkillWeaver：按 CT08–CT11 保留已核数字与限定；RQGM 补混合 token 定义即可。
9. §8.1 / §9.1：以 CT12 补一个范围外直接近邻，保持原检索范围计数不变。

## 4. 仍未解决的事项与阅读范围

- 没有从 HGM 已读原文得到异步机制的独立贡献或实际墙钟重叠数据；不能用分配 CPU 小时倒推出该量。
- SICA 固定 50 题而 accuracy 非 2% 整数倍的问题，原文方法段和 Table 1 没解释。要消除此疑点需作者协议/代码或补充说明；本轮不补猜测。
- Continual Harness 原文模型名称、里程碑和 Figure 17 量纲冲突已有 D543–D545。本文只修影响免训练和成本口径的两处，不以局部核查证明其全部实验协议清楚。
- Adaptive Auto-Harness 的工具调用和模型决策对应关系，需执行日志才能代入 N、J_i；聚合表本身不够。其未完整记录的 evolver 成本不能补算为零。
- GenericAgent 九轮案例没有隔离经验、任务实例、代码化阶段的各自贡献；Metis 的完整维护/管理器调用账也未由执行器 token 表补齐。
- 本轮未对 LATM、CRAFT、SkillOpt、OpenSkill、CoEvoSkills、Alita-G、AgentDistill、VASO、RewardHarness 等全部重新读原始 PDF；这些条目的正文已阅读，但原文结论只沿用旧审计，**不作本轮重新通过的声明**。
- 原式标签：本轮直接核对 SICA 效用式、HGM 理论与经验 CMP 的区分、RQGM 计量定义。没有复核整张问题定义表所有符号，故不为“公式全部照抄原文”背书。排版有等价改写的式子宜写“按原文等价转写”，而不是保证逐字符照录。

## References（完整书目信息与实际阅读版本）

以下论文均按原始 PDF 读取；正式发表身份与本轮实读的预印本版本分开写。正式会议信息若注明“沿用账本”，表示本轮没有再次浏览大会日程；本轮技术结论仍定位到所列 PDF。未确认正式发表的条目一律按机构预印本引用。

1. Wenyi Wang, Piotr Piękos, Li Nanbo, Firas Laakom, Yimeng Chen, Mateusz Ostaszewski, Mingchen Zhuge, and Jürgen Schmidhuber. **Huxley-Gödel Machine: Human-Level Coding Agent Development by an Approximation of the Optimal Self-Improving Machine.** ICLR 2026（正式身份沿用已核账本；本轮不重验 Oral）。实读 arXiv:2510.21614v3，2025-10-29。[PDF](https://arxiv.org/pdf/2510.21614v3)。原文机构：KAUST。重点复核 pp.4–10、p.18。
2. Seth Karten, Joel Zhang, Tersoo Upaa Jr., Ruirong Feng, Wenzhe Li, Chengshuai Shi, Chi Jin, and Kiran Vodrahalli. **Continual Harness: Online Adaptation for Self-Improving Foundation Agents.** 2026，预印本。实读 arXiv:2605.09998v1，2026-05-11。[PDF](https://arxiv.org/pdf/2605.09998v1)。原文机构：Princeton University、ARISE Foundation、Google DeepMind；按强机构预印本纳入。重点复核 pp.3–8、23、25–28。
3. Zewen Liu, Zhan Shi, Yisi Sang, Bing He, Minhua Lin, Tianxin Wei, Dakuo Wang, Benoit Dumoulin, Wei Jin, and Hanqing Lu. **Adaptive Auto-Harness: Sustained Self-Improvement for Agentic System Deployment on Open-Ended Task Streams.** 2026，预印本。实读 arXiv:2606.01770v2，2026-06-03。[PDF](https://arxiv.org/pdf/2606.01770v2)。原文机构：Emory University、Amazon、Pennsylvania State University、UIUC、Northeastern University；按高校研究预印本纳入，不凭普通公司博客资格。重点复核方法定义、p.13 Table 5、p.19 Table 14。
4. Maxime Robeyns, Martin Szummer, and Laurence Aitchison. **A Self-Improving Coding Agent.** 2025。ICLR 2025 Workshop “Self-Improving Foundation Models Without Human Supervision”（workshop 身份沿用账本，非 ICLR 主会）；按 University of Bristol 机构资格纳入。实读 arXiv:2504.15228v2，2025-05-16。[PDF](https://arxiv.org/pdf/2504.15228v2)。重点复核 pp.3–7，尤其 Eq.1–2、Table 1。
5. Advantage AI Agent Lab (A3 Lab). **GenericAgent: A Token-Efficient Self-Evolving LLM Agent via Contextual Information Density Maximization (V1.0).** 2026，预印本。首页以团队署名；§8 列贡献者：Jiaqing Liang, Jinyi Han, Weijia Li, Xinyi Wang, Zhoujia Zhang, Zishang Jiang, Ying Liao, Tingyun Li, Ying Huang, Hao Shen, Hanyu Wu, Fang Guo, Keyi Wang, Zhonghua Hong, Zhiyu Lu, Lipeng Ma, Sihang Jiang, Yanghua Xiao。实读 arXiv:2604.17091v1，2026-04-18。[PDF](https://arxiv.org/pdf/2604.17091v1)。§8 明示两位项目负责人为 Fudan University 教师，按高校研究补充资格纳入；不把团队公司背景单独当资格。重点复核 pp.20–23、p.31 作者贡献。
6. Zijie Dai, Siuhin He, Hui Li, Qihui Zhou, Jiajun Li, Mingcong Song, Guoping Long, Hongjie Si, Xin Yao, Lin Zhang, James Cheng, and Xiao Yan. **Metis: Bridging Text and Code Memory for Self-Evolving Agents.** 2026，预印本（首页标 Work in progress）。实读 arXiv:2606.24151v1，2026-06-23。[PDF](https://arxiv.org/pdf/2606.24151v1)。原文机构：The Chinese University of Hong Kong、Huawei、Wuhan University；按高校研究预印本纳入。重点复核 pp.6–12，Table 1–4。
7. Jenny Zhang, Shengran Hu, Cong Lu, Robert Lange, and Jeff Clune. **Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents.** ICLR 2026（会议身份沿用已核账本；本轮 PDF 首页亦标会议论文，但未重新查官方日程）。实读 arXiv:2505.22954v3，2026-03-12。[PDF](https://arxiv.org/pdf/2505.22954v3)。机构：University of British Columbia、Vector Institute、Sakana AI、Canada CIFAR AI Chair。重点复核 pp.4–6、10、32。
8. Alex Iacob, Andrej Jovanović, William F. Shen, Daniel Burkhardt, Meghdad Kurmanji, Nurbek Tastan, Lorenzo Sani, Niccolò Alberto Elia Venanzi, Ambroise Odonnat, Zeyu Cao, Bill Marino, Xinchi Qiu, and Nicholas D. Lane. **The Red Queen Gödel Machine: Co-Evolving Agents and Their Evaluators.** 2026，预印本（作者称初步实证）。实读 arXiv:2606.26294v2，2026-06-29。[PDF](https://arxiv.org/pdf/2606.26294v2)。机构：University of Cambridge、NVIDIA、Flower Labs、MBZUAI、Inria；按强高校/研究机构预印本纳入。重点复核 pp.7、12、22、25。
9. Boyuan Zheng, Michael Y. Fatemi, Xiaolong Jin, Zora Zhiruo Wang, Apurva Gandhi, Yueqi Song, Yu Gu, Jayanth Srinivasa, Gaowen Liu, Graham Neubig, and Yu Su. **SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills.** 2025，本文按实读预印本引用，不重验后续 venue。实读 arXiv:2504.07079v1，2025-04-09。[PDF](https://arxiv.org/pdf/2504.07079v1)。机构：The Ohio State University、University of Virginia、Purdue University、Carnegie Mellon University、Cisco Research；高校研究资格。重点复核 pp.4–6、34。
10. Zixi Huang, Xiheng Wang, Andrew Wang, William Jurayj, Bernal Jiménez Gutiérrez, Daniel Khashabi, and Nicholas Andrews. **Better, Faster, Stronger: Programmatic Skill Learning Best Reduces Agent Cost.** 2026，预印本（方法名 SpeedRunner）。实读 arXiv:2608.11338v1，2026-08-11。[PDF](https://arxiv.org/pdf/2608.11338v1)。机构：Johns Hopkins University。重点复核 pp.2–6、10、14。
