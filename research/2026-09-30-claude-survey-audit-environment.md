# Claude 综述报告审核：环境学习、评测与研究建议

审核日期：2026-09-30。审核对象为 [Claude 报告](/Users/edwin/projects/agent-acceleration-research/notes/part3/2026-09-30-self-improvement-survey-mining-zh.md) 的第 4–6、8–10 节（本轮文件行 345–493、560–689）。为检查前后是否一致，另定位了开头的要点、第 1.3/2.1 节和附录 C.1。没有修改报告或 HTML。

本轮通读上述报告范围，结合 [新增证据台账](/Users/edwin/projects/agent-acceleration-research/research/2026-09-30-part3-survey-mining-ledger.md)、[s 系列原始记录](/Users/edwin/projects/agent-acceleration-research/research/2026-09-30-part3-records-s.md) 和此前的工具证据。对关键疑点回到 WMA、WorldEvolver、SICA、SEDM、WALT、GenericAgent、CoEvoSkills 的原始 PDF，核对方法、公式、表格及附录；密集公式、数表已看渲染页。其余论文没有在本轮重新全文审计，不能把“本轮没有提出问题”解释为又获得一次完整认证。以下 CE 编号是本审核的局部编号。

主要问题集中在从证据推到研究定位的几步，而不是大面积抄错数字：报告已正确记录 SICA/SEDM 的成本信号，却仍推断没有加速目标，并把每次成功口径、成本效用称为新想法；WorldEvolver 在方法段被正确写成不训练，在清单标题里又被算作改参数；WALT 的粗摊销被继续当作完整回本依据。

## CE1｜须改：没有每次成功分母，不能推出没有以加速为目标的自改进

**原句与位置。** 第 8.1 节第 1 条，行 566：“按每次成功计的一项都没有……所以在本文核对过的范围内，没有找到以加速为主目标的自改进循环。”第 8.2 A3，行 579：“‘每次成功’的口径是新想法（本文核对过的文献里没有找到）。”开头要点另写“时间和费用只作预算或副作用”。

**判定。** 推论不成立，且与报告自己的证据及第 9.2 第 10 条相冲突。没有发现某一种报告分母，只能支持该报告口径未见，不能支持没有优化执行成本，更不能据此判定方法新颖。“主目标”若特指质量约束下的成本最小化，应明确这个定义，不能与广义加速混用。

**原文已核。** SICA [R1] 第 3 页第 3 节式 1–2：选择效用的权重分别是任务分数 0.5、美元成本 0.25、墙钟时间 0.25；成本以每题 $10、时间以 300 秒归一并截断，超时另受惩罚。成本和时间是直接影响下一轮父代选择的目标项，非仅外加预算或副作用。原文还明确不改模型权重。第 6 页表 1 的第 0→15 轮，平均费用 $1.91→$1.70、时间 130.2→114.5 秒、token 0.24M→0.30M；这是单次自改运行的每题平均，不是每成功成本，也不能证明质量约束式优化。报告对这些数字的约 −11%、−12%、+25% 计算基本正确。

短引文（R1 全文本审核仅此处引用）：“we are not performing any weight updates”。定位：[SICA v2，第 3 页](https://arxiv.org/pdf/2504.15228v2#page=3)。

**建议替换。** “在本轮核对的来源中，尚未见直接按本文定义的每次成功总时间/总费用报告的实验；但 SICA 已直接联合优化性能、费用与墙钟，SEDM 也有成本感知准入和检索。我们的区别需要落在正确性约束、预算分账、维护开销及任务流协议上。每次成功口径是本研究采用的评价定义，暂不据此声称新颖性。”

**推理边界。** 报告第 2.1 节已把分子定义为含失败的全部尝试期望，定义本身可保留。只是成功率相同时，按尝试成本与成本除以成功率的排序相同；换分母并不自动产生新方法。若声称“加速为唯一主目标”的既有工作缺位，仍需另做按目标函数检索，不能由本次计量筛查替代。

## CE2｜须改：SEDM 已把成本感知效用用于记忆权重和检索，C4 不宜直接标“新想法”

**原句与位置。** 第 8.3 C4，行 597：“记忆条目带效用值、按时间和费用更新……把效用的奖励换成时间和费用，在本文核对过的文献里没有找到……类别：新想法。”

**判定。** 相关先例范围被缩窄了。SEDM 不是只在入口检查一次延迟；它把包含成本的准入分变成条目初始权重，该权重进入检索，随后再按使用与结果更新。报告第 9.2 第 6 条“只有划算才保留不是新原则”正确，应反向约束 C4 的新颖性措辞。

**原文已核。** SEDM [R2] 第 5 页式 3–5：配对回放得到奖励变化、延迟变化和 token 变化，准入分为 `S = ΔR − λL·ΔL − λT·ΔT`；采纳后 `w0(m)=max(0,S)`。第 6 页式 6 用 `sim(q,m)×w(m)` 排检索结果；式 7 与正文描述后续效用权重更新。第 10 页表 2 报 token 和任务表现，不能把这套设计说成已经实测了延迟或美元收益。SEDM 相对 G-Memory 降 token，但相对无记忆增加 token；Claude 报告对此反例的提醒正确。

短引文（R2 仅此处）：“the measured changes in reward and latency”。定位：[SEDM v3，第 5–6 页](https://arxiv.org/pdf/2509.09498v3#page=5)。

**建议替换。** “验证成本感知的记忆价值学习：以 MemRL/MemQ 的效用更新和 SEDM 的成本感知权重作为基线，在正确性约束下测时间与美元净收益。若进一步提出独立的在线美元价值更新规则，再明确它与 SEDM 准入、检索、后续更新的差别。当前类别为已有机制的验证与扩展候选，非已确认的新方法。”

**推理边界。** 本审核没有声称 SEDM 已实现逐次按美元更新，也没有证明其式 7 的具体效用估计与我们将来的实现相同；指出的是现有工作已经覆盖了 C4 目前描述的大范围。没有报告延迟实测，不等于没有成本优化机制。

## CE3｜须改：WorldEvolver 不能随目录分区统称为“改模型参数”

**原句与位置。** 第 10.2 节，行 673：“改模型参数的 77 条……其中 WMA、WorldEvolver、WebRL、SEAgent 四条沿用此前的全文审计记录。”同一称呼也见开头材料说明与附录 C.1 标题。第 1.3 节已经解释 WorldEvolver 虽被项目页归入这一侧，实际不训练；第 4.1 节也写对了。

**判定。** 清单类别与实际训练边界混淆，造成报告内部矛盾。项目页分区名称只能表示目录位置，不能作为这 77 条全部训练参数的事实。

**原文已核。** WorldEvolver [R3] 第 3–5 页的方法只在部署时修订情节/语义记忆与世界模型上下文，策略和世界模型参数冻结。第 5 页算法 1 及配套文字明确把预测误差变成文本规则，未做模型梯度更新。WMA [R4] 则不同：第 7–8 页实验配置训练 Llama-3.1-8B 世界模型和价值函数；第 16 页 C.1.2 有训练设置。仅执行策略冻结，不能使 WMA 整体成为无训练方法。

短引文（R3 本审核英文引文合计不超过 25 词）：“revises world model context at test time”；定位：[WorldEvolver v2，第 9 页结论及第 5 页方法](https://arxiv.org/pdf/2606.30639v2#page=5)。

**建议替换。** “项目页 Foundation Model 一侧的 77 条目录记录；这并不表示每条都更新模型权重。WMA 属训练辅助模型，WorldEvolver 属模型权重冻结、更新上下文的例外，按其真实方法边界另行标注。”77 作为目录条目数可保留；若继续称“改参数方法数”，必须重新核算，不能仅把 WorldEvolver 删掉就推断其余 76 条全部训练。

## CE4｜须补限定：WMA 的错误样本率不能概括两种世界模型；WorldEvolver 不止“一次预测”

**原句与位置。** 第 8.2 B5，行 590：“环境模型这条路（WMA、WorldEvolver）需要训练辅助模型或每步多一次预测，预测错误里四成是编造元素”。

**判定。** 方向建议可以保留，但证据范围和开销描述须拆开。第 4.1 段已正确给出 WMA 的 50 个错误样本条件，后面的压缩总结不应丢失它。42% 既不是所有预测的错误率，也不是 WorldEvolver 的错误率。

**原文已核。** WMA [R4] 第 10 页第 6.2 节、图 7：人工抽取并分类 50 个错误预测，42% 属反事实想象。第 16 页附录推理流程会先从 20 次动作采样中取 3 个候选，再分别预测和评分。

短引文（R4 仅此处）：“we sample 50 erroneous predicted states”。定位：[WMA v2，第 10 页图 7](https://arxiv.org/pdf/2410.13232v2#page=10)。

WorldEvolver [R3] 第 5 页算法 1 包括预测、动作重选、必要时重做预测、真实执行后的记忆更新；不是固定每步仅加一个调用。第 16–18 页附录 C、表 13 还给出规划期组件开销（Gemma-4-26B-A4B，**不带选择性前瞻的 w/o Ft 版本**）：

| 设置 | 世界模型模块调用/agent 步 | LLM 调用/agent 步 | 检索 ms/次 | 单次 WM 调用最大 prompt token |
|---|---:|---:|---:|---:|
| ALFWorld ReAct | 2.086 | 1.609 | 16.244 | 2,982 |
| ALFWorld ReflAct | 2.054 | 1.642 | 18.335 | 2,726 |
| ScienceWorld ReAct | 2.157 | 1.866 | 10.100 | 4,324 |
| ScienceWorld ReflAct | 2.131 | 1.874 | 10.906 | 4,211 |

表中模块调用包含预测与记忆更新；保持作者的两列口径，不把模块调用数等同于底层 LLM 调用数。本表不是任务端到端秒数或美元成本，也不是带 Ft 版本的收益/成本配对实验。第 14 页表 6 的 1.48 对 1.05 秒仍是 Word2World 预测评测，Claude 对此限制写得正确。定位：[WorldEvolver v2，表 13，第 18 页](https://arxiv.org/pdf/2606.30639v2#page=18)。

**建议替换。** “WMA 需训练世界模型和价值函数，并对多个动作候选预测；其抽样的 50 个错误预测中 42% 是反事实想象。WorldEvolver 无训练，但增加预测、检索与记忆更新；附录有组件开销，尚不能据此算任务级净加速。第一版暂不采用是针对我们预算和验证难度的研究选择，不是这两类方法均不满足无训练要求。”

## CE5｜须改：WALT 的约 14 次是粗摊销，不能无条件保留为完整回本次数

**原句与位置。** 第 8.5 第 5 条，行 613：“方案稿已有的 ActionEngine 和 WALT 回本次数 [E332] [E333] 不变。”

**判定。** 至少 WALT 这一半需要改写。E333 忠实转述了作者数字，但作者所称回本的运算没有扣除使用工具后的执行费用；忠实摘录不能代替经济口径审核。

**原文已核。** WALT [R5] 正式 ICLR 2026 版第 9 页第 4.6 节：Online-Mind2Web 上 305 个工具候选、252 个验证成功，按 GPT-5 示例价格每工具构建 $1.67；无工具基线每任务 $0.12；随后称约 14 次回本。`1.67/0.12=13.9` 恰好复现其数字。该段没有提供同一口径下复用后的每任务费用，也未清楚交代全部失败候选成本是否进入每工具 $1.67。

短引文（R5 仅此处）：“break-even occurs after ∼14 uses per tool”。定位：[WALT 正式版，第 9 页](https://proceedings.iclr.cc/paper_files/paper/2026/file/5b175f9e93873e3a10a6ce43dbb82e05-Paper-Conference.pdf#page=9)。

**建议替换。** “WALT 作者的约 14 次是构建成本除以基线费用得到的粗摊销参照，不是包含使用、失败、维护后的实测回本点。在同任务、同正确性要求下，应以 `N·(C基线−C复用) ≥ C构建+C选择+C维护(N)` 判断能否回本。当前报告不足以恢复 WALT 的严格 N。”

**推理边界。** 上式是本审核的账本建议，非 WALT 原式。任务使用多个工具、适用覆盖不全或成功率不同，还需按实际任务流汇总，不能机械使用每工具次数。本项没有重新审计 ActionEngine 全部成本表，不把 WALT 的问题推到 ActionEngine。

## CE6｜建议改：置信区间重叠不等于已经证明“分不开”

**原句与位置。** 第 4.1 节末判断：“不训练的版本（WorldEvolver）目前只在文字游戏环境上提高了预测精度，下游成功率的提升在置信区间内与基线分不开。”

**判定。** 不宜从各方法独立区间的重叠，推出差值不显著或效果等价。谨慎态度合理，统计表述应更窄。

**原文已核。** WorldEvolver [R3] 第 16–17 页表 12，只对 Gemma-4-26B-A4B 给任务级 95% bootstrap 区间，10,000 次重采样，并列 best-of-5 与 Success@1。ALFWorld ReAct best-of-5：基线 23.9 [17,31]，WorldEvolver w/Ft 26.1 [19,34]；Success@1 22.4→19.4。ScienceWorld ReAct best-of-5：44.4 [34,56]→52.2 [42,62]；Success@1 28.9→36.7。它没有在该表提供两方法配对差值区间或等价检验。第 7 页表 2 的 GPT-5.4-mini 结果也非统一提高：ReAct/ScienceWorld 为 65.56→63.33，ReflAct/ALFWorld 为 50.00→47.01。

**建议替换。** “Gemma 的 best-of-5 点估计提高，但作者给出的单方法置信区间重叠，未给配对差值检验；首次成功率及另一骨干模型的结果不一致，因此还不足以认定稳定的下游增益，更不能推出净加速。”

本项是统计解释审核；没有重新进行显著性检验，也没有断言方法无效。

## CE7｜建议降格为假设：“最稳定”“最不可靠”超出了所引比较的范围

**原句与位置。** 第 8.1 第 2、3 条，行 567–568：“把重复流程做成可调用的代码或已存的动作序列，是同时降步数和 token 最稳定的做法”；“‘判断对错’仍是最不可靠的一环”。

**判定。** 所列研究足以支持有前景的候选机制、确有误判风险，但没有共同协议、共同任务分布和跨组件可靠性比较来支持这两个最高级。报告自己已写 GenericAgent 单序列、MobileGPT 热启动且人工修复、Metis 的文本记忆也降 token；这些限制应进入总括句。

**原文已核的局部锚点。** GenericAgent [R6] 第 21 页表 8，九轮 LangChain GitHub 调研任务确实是时间 7m30s→1m38s、**LLM Calls** 32→5、总 token 222,203→23,010。原表不是 tool calls；Claude 此处正确。本表为一条顺序运行轨迹，不能由“九轮”推断跨任务/随机种子的稳定性，也不能把所有收益归因于代码阶段；第 2–5 轮文字 SOP 本身已降很多 token。定位：[GenericAgent v1，第 21 页](https://arxiv.org/pdf/2604.17091v1#page=21)。

**建议替换。** “在几个与重复工作流相关的案例中，可执行复用减少了串行决策和运行开销，值得作为第一组候选验证；相对文字记忆的净优势还需同协议对照。”“评判错误是已有实测反例、需要专门控制的重要瓶颈。”

**核验边界。** 本项对 ReasoningBank/OpenSkill 的原始误判率不做第二轮认证；仅指出不同论文的 agreement 与 precision 不能直接组成跨组件可靠性排名。MobileGPT/Metis 的条件沿用报告与既有证据，不宣称本轮重读两篇。

## CE8｜建议补实验角色：少量真值调用属于开发/选择预算，不能兼任独立最终测试

**原句与位置。** 第 5 节“可借的规则”，行 452：“保留少量真值检查，只在代理测试全过时调用”。

**判定。** 对 CoEvoSkills 的机制转述正确；移植到我们的答案库时需要补清真值扮演的角色。不是要求删除该规则，也不是指控原论文泄漏隐藏测试源码。

**原文已核。** CoEvoSkills [R7] 第 5 页算法 1：代理测试全过才在新环境执行真实 oracle；最多 K=5 次 oracle，按 oracle 分数保留最佳快照；不满分的成败比特进入后续生成上下文。因此 oracle 是优化/选择闭环的一部分，隐藏测试内容和分离 verifier 不会消除反复查询产生的适应。

短引文（R7 仅此处）：“append oracle pass/fail bit to C (no test content)”。定位：[CoEvoSkills v3，第 5 页算法 1](https://arxiv.org/pdf/2604.01687v3#page=5)。

**建议加一句。** “闭环可查询的真值属于开发或选择反馈，次数和费用计入改进预算；最终评价还需另一份不参与迭代的任务/答案，并覆盖副作用和跨任务泛化。”报告第 6.4 节已经区分留出验证与留出测试，直接把这一要求交叉引用到此处即可。

本项是研究协议建议，不是说 CoEvoSkills 已完成上述跨任务独立评价，也不是重新裁定其完整评测协议。

## CE9｜出处待核：辅助模型训练的“用户要求”标签

**原句与位置。** 第 8.4 标题，行 600：“用户要求：有理由、并且小规模可行才考虑”；第 9.2 第 9 条再次称这是 Edwin 的条件；第 10.4 第 6 条提出把小编辑模型提前到第二阶段。第 1.3 节也使用同样用户归因。

**判定。** 本审核可见的人类指令强调模型训练之外的工作，未见“满足理由与小规模即可训练辅助模型”的明确原话。但用户已说 Claude 另会话的 context 更足，故这里只列**出处待核**，不判定该归因虚构，也不据此否定后续选项。

**建议修补。** 若有可信的人类会话记录，附上日期和准确表述，保留标签；否则改为“研究者建议的延后选项，当前研究默认不训练”，把辅助模型微调与冻结 API 执行者明确分开。不要把“任务模型不能训”自动扩大解释为“辅助模型获准训”。此项不由论文证明，没有学术引用；也不要求在已有明确授权时再次向用户索取授权。

## 已核且应保留的限定

- **WMA 训练边界和质量代价**：第 4.1 节对两个 8B 辅助模型、16.6% 对 19.2%、140.3 对 748.3 秒、$0.4 对 $2.7 的区分与原文方法/表 4相符；保留 Tree Search 部分为引自基线论文的说明。不能把这组费用比较说成同成功率加速。训练的“约 3 GPU 小时、8 张 RTX 4090”原文措辞确实有总 GPU 小时与墙钟口径歧义，Claude 在第 8.4 明示不确定比擅算 24 GPU 小时更合适。
- **WorldEvolver 不等于任务级加速**：第 4.1 已区分预测准确率与下游规划、预测秒数与任务秒数；这是正确的主要方向。补表 13，不应把 1.48 秒外推成整个任务的时间。
- **SICA token 不能代替美元**：表 1 确实允许 token 上升而费用和时间下降；第 15 轮与第 14 轮结果不能混用。第 6 页单次 15 轮优化总开销约 $7,000，应与执行费用分开。
- **GenericAgent 条件**：表 8 的 LLM Calls 32→5 是正确读法；单条顺序实例序列、缓存读取计入 total 的限制应保留。
- **CoEvoSkills 条件**：独立验证器与隐藏真值内容确有方法依据，但系统仍通过真值成败反馈优化；需要 CE8 所述的实验角色标注。
- **第 10 节来源资格是规则判断**：本轮没有重新裁定 MUSE 等机构是否达到用户认可门槛。是否计入与论文技术内容是否支持某项结论是两个问题，不能把“暂缓来源”转述成“该机制没有成本证据”。

## 原文核验清单与完整参考文献

页码均为 PDF 印刷页/对应物理页（本轮所列关键页一致）；版本按实际打开的本地缓存标明。会议声明未独立复核者不冒称本轮已确认正式发表。英文短引文每篇合计均不超过 25 词，其余为本审核的转述与推断。

| 文献 | 本轮回原文核验范围 | 使用目的 |
|---|---|---|
| R1 SICA | v2 pp3、6，式1–2、表1及相关讨论 | 无权重更新、成本选择目标、执行与改进成本 |
| R2 SEDM | v3 pp5–6、10，式3–7、表2 | 成本准入、权重检索、更新与未报告延迟的边界 |
| R3 WorldEvolver | v2 pp3–5、7、9、14、16–18，算法1、表2/6/12/13 | 冻结权重、预测与规划区别、误差与开销 |
| R4 WMA | v2 pp7–10、16，表4、图7、附录C | 训练两个辅助模型、错误样本分母、推理与训练成本 |
| R5 WALT | ICLR camera-ready p9 §4.6 | 对作者回本算式重新核账 |
| R6 GenericAgent | v1 p21 §4.4、表8 | LLM调用数及单序列解释 |
| R7 CoEvoSkills | v3 p5 算法1及文字 | 代理测试与可查询真值反馈的角色 |

**[R1]** Maxime Robeyns, Martin Szummer, and Laurence Aitchison. 2025. *A Self-Improving Coding Agent*. arXiv:2504.15228, v2（2025-05-16），预印本；University of Bristol / iGent AI。实际读取 v2 PDF。[原文](https://arxiv.org/pdf/2504.15228v2)。

**[R2]** Haoran Xu, Jiacong Hu, Ke Zhang, Lei Yu, Yuxin Tang, Xinyuan Song, Yiqun Duan, Lynn Ai, and Bill Shi. 2025. *SEDM: Scalable Self-Evolving Distributed Memory for Agents*. arXiv:2509.09498, v3（2025-09-26）。实际读取 v3 PDF；既有记录标注 SEA@NeurIPS 2025 workshop，本轮未另核会议页面，不当作 NeurIPS 主会。作者单位包含 Gradient、Zhejiang University、University of Toronto、Rice University 等。[原文](https://arxiv.org/pdf/2509.09498v3)。

**[R3]** Xuan Zhang, Wenxuan Zhang, See-Kiong Ng, and Yang Deng. 2026. *Self-Evolving World Models for LLM Agent Planning*. arXiv:2606.30639, v2。National University of Singapore / Singapore University of Technology and Design / Singapore Management University。实际读取 v2 PDF；Findings of EMNLP 2026 是被审报告记录的作者声明，本轮未核实正式 proceedings，按预印本引用。[原文](https://arxiv.org/pdf/2606.30639v2)。

**[R4]** Hyungjoo Chae, Namyoung Kim, Kai Tzu-iunn Ong, Minju Gwak, Gwanwoo Song, Jihoon Kim, Sunghwan Kim, Dongha Lee, and Jinyoung Yeo. 2025. *Web Agents with World Models: Learning and Leveraging Environment Dynamics in Web Navigation*. International Conference on Learning Representations (ICLR 2025)。Yonsei University。实际读取 arXiv:2410.13232v2 PDF，首页标注 ICLR 2025。[原文](https://arxiv.org/pdf/2410.13232v2)。

**[R5]** Viraj Prabhu, Yutong Dai, Matthew Fernandez, Krithika Ramakrishnan, Jing Gu, Yanqi Luo, Silvio Savarese, Caiming Xiong, Junnan Li, Zeyuan Chen, and Ran Xu. 2026. *WALT: Web Agents that Learn Tools*. International Conference on Learning Representations (ICLR 2026)。实际读取正式会议 camera-ready；不是旧 arXiv 2510.01524v1。[正式 PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/5b175f9e93873e3a10a6ce43dbb82e05-Paper-Conference.pdf)。

**[R6]** Advantage AI Agent Lab (A3 Lab). 2026. *GenericAgent: A Token-Efficient Self-Evolving LLM Agent via Contextual Information Density Maximization (V1.0)*. arXiv:2604.17091, v1，预印本技术报告。论文为集体署名；§8 贡献者为 Jiaqing Liang, Jinyi Han, Weijia Li, Xinyi Wang, Zhoujia Zhang, Zishang Jiang, Ying Liao, Tingyun Li, Ying Huang, Hao Shen, Hanyu Wu, Fang Guo, Keyi Wang, Zhonghua Hong, Zhiyu Lu, Lipeng Ma, Sihang Jiang, Yanghua Xiao。实际读取 v1 PDF。[原文](https://arxiv.org/pdf/2604.17091v1)。

**[R7]** Hanrong Zhang, Shicheng Fan, Henry Peng Zou, Yankai Chen, Zhenting Wang, Jiayu Zhou, Chengze Li, Wei-Chieh Huang, Yifei Yao, Kening Zheng, Xue (Steve) Liu, Xiaoxiao Li, and Philip S. Yu. 2026. *CoEvoSkills: Self-Evolving Agent Skills via Co-Evolutionary Verification*. arXiv:2604.01687, v3。实际读取 v3 PDF，页眉标注 COLM 2026；本轮未另核正式会议记录。[原文](https://arxiv.org/pdf/2604.01687v3)。
