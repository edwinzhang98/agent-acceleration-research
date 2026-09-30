# Memory 分支：冻结模型的经验复用与 Agent 加速——原文证据笔记

后续补核：方法定义、环境知识的具体范围和局限归属以 [2026-09-30补核](2026-09-30-survey-revision-memory-environment.md) 与 [修订审计](2026-09-30-survey-revision-audit.md) 的明确修正为准；下文保留前轮数字和阅读记录。

日期：2026-09-30。范围：网站目录 row 117–181，共 65 条记录；逐条初筛见同目录 `2026-09-30-survey-memory-screen.json`，补核后的最终标签以整合清单 `2026-09-30-survey-screening.json` 为准。本笔记为主报告的证据输入，不代表所有 65 条均全文精读。论文目录、摘要用于初筛；下面核心条目已读原文方法、实验与相关附录。数字从 PDF 文字层核对，并对关键表格/图进行页面放大复核。正文使用局部 M 编号，尚未分配项目 D/E 台账编号。

最直接的结论：**“从 trajectory 学到经验”已有很多工作；“这些经验使部署更快、更省，而且把学习成本也赚回来”是更窄、证据参差不齐的问题。** Metis 和 MobileGPT 最接近执行加速；AWM、ReasoningBank 证明路径可缩短，但这不等于总 token 降低；ExpeL、Dynamic Cheatsheet、G-Memory、SEDM 是明确的反例或条件性证据。冻结模型也不意味着完全没有学习：MemRL 更新外部记忆的标量效用，MemGen 则真的训练辅助神经模块，两者不能混为一谈。

## 1. 证据表与原文核查

| 编号 / 作品 | 实际改变什么 | 效率结论 | 对当前研究的定位 |
|---|---|---|---|
| M01 Metis | 文本经验；反复复用后升级为可执行工具 | 执行 token 与 ReAct 轮数下降；建设成本单列但不含训练轨迹生成 | 最直接重叠，应列强基线 |
| M02 MobileGPT | 应用页面/子任务/动作记忆；条件匹配后重放 | warm-start 延迟与美元成本显著下降；冷启动与人工修复须独立计账 | 环境探索 + 经验复用的直接前作 |
| M03 AWM | 成功轨迹抽象为文本 workflow | 成功路径步数减少；总 token 净节省未建立 | 文本 workflow 基线；执行宏并非自动有效 |
| M04 ReasoningBank | 成败轨迹抽象成策略；可加多轨迹采样 | 步数减少，但含 judge/extraction 总 token 增加约 4.3% | 方法强相关；不能直接宣传净加速 |
| M05 ExpeL | 离线成败对比得到 insights + 成功示例检索 | 动作略少、trajectory token 明显更多 | 经验学习经典基线与成本反证 |
| M06 Dynamic Cheatsheet | 在线更新策略/代码备忘录 | 主要证明准确率；所报 AIME token 高于基线 | 方法参考，不是已证实的加速方案 |
| M07 MemRL | 记忆条目的标量 Q 值与检索选择 | 近似相同 token 预算下提高成功率；未证明部署净加速 | 外部效用学习可在纯 API 约束下用 |
| M08 EXG | 成功、失败、修复经验图及检索提示 | 一些设置 calls/LLM latency 降低；token 效果依基线/任务变化 | 少重试的直接证据，限函数代码/QA |
| M09 G-Memory | 多智能体的交互、任务、insight 三层图 | 相对无记忆更贵；较其他记忆方法改善质量/成本权衡 | 多智能体方法参考 |
| M10 DecentMem | 每个 agent 独立双记忆池与效用路由 | 比 G-Memory 省 token；仍比无记忆多 | 多智能体补充，不直接迁移为单 agent 结论 |
| M11 SEDM | 可回放上下文，paired A/B 接纳，效用调度 | 比 G-Memory 省，较无记忆更贵；回放开销不在推理 token 表内 | 接纳机制值得参考，结论需复核 |
| M12 CTIM-Rover | 软件仓库的通用/仓库级 insights | 小规模实验无收益甚至退化，未测净加速 | 直接相关的负结果 |
| M13 Memory Beyond Recall | 对话事实的同步写入、异步抽象与冲突消解 | 避免在线读记忆时再调用 LLM，但无部署加速对照 | 背景：不能把“记住用户事实”当作学会任务技能 |
| M14 Mem²Evolve | 工具资产 + 经验的共同增长 | 工具创建所需修复迭代下降；非完整任务延迟 | 方法级交叉引用，工具分支继续处理 |

### M01. Metis：最接近“先学文本经验，再把值得的部分编译成动作”

**已读**：arXiv:2606.24151v1，§§2–4、Appendix A；Table 1–4（PDF pp.10–12）已视觉核验。CUHK、Huawei、武汉大学等联合预印本；尚未核到正式录用，不写成顶会论文。

**机制**：固定 GPT-4o ReAct 执行器；Sonnet-4.6 反思失败及低效成功轨迹，整理 plans、环境 facts、pitfalls。不是见一条成功轨迹便直接固化：一个文本 plan 被不同结构的 query 反复选择后，才触发参数化工具生成；codifier 看 plan 与 query 变化，避免照抄原轨迹。检索到的文本与工具 docstring 进入执行上下文；工具作为可调用动作，减少反复读说明、推理、写临时代码。依赖闭包与编译检查为接纳门槛，但不等于证明行为语义正确。

**实验条件与效果**：AppWorld 的官方 train / test-normal 与重采样任务划分；测试时冻结训练得到的记忆。官方划分 No Memory→Metis：TGC **51.8%→60.1%**，执行 token **112.6K→97.4K/任务**，ReAct turns **14.55→11.25**，一次性反思 **7.9M tokens**。重采样划分为 **54.8%→66.1%**、**101.7K→78.5K**、**13.92→10.32**，反思 **11.8M**。Table 2 进一步控制为**重采样划分中 No Memory、SkillX、Metis 三个方法共同完成的 62 个任务**；其中 No Memory→Metis 为 **85.2K→59.6K tokens、12.2→8.6 turns**，减少“所解任务集合不同”的混杂，不能把该子集当作官方划分的结果。

**关键边界**：Table 1 的执行 token 是执行器输入+输出；反思包括文本反思和 codification，**各方法训练轨迹生成成本均排除**。manager/embedding 等开销未得到单独完整账目；没有秒或美元结论。重采样允许任务来自相同 scenario family，比官方 scenario-disjoint 更易复用。§4.3 的 Eager 消融执行更省（49.9K vs full 54.5K），但准确率较差（63.2 vs 66.7），建设更贵（11.6M vs 7.9M），说明“越多代码越快”并非完整目标。

**作者解释**：复用证据可筛掉不值得固化的经验，分布偏移下文本更灵活。**我们的推断**：当前 idea 若仅是“轨迹→经验→工具”，已被推进相当远；更有辨识力的验证是全生命周期成本、工具前置状态/后置状态校验、失效回退与环境变化，而非再做一套经验库。Metis 未展示这些方向的全面解答；这不是新颖性保证。[原文](https://arxiv.org/pdf/2606.24151v1)

### M02. MobileGPT：环境记忆可以直接绕过一部分模型调用

**已读**：arXiv:2312.03003v3 的正文为 ACM MobiCom 2024 版 *MobileGPT: Augmenting LLM with Human-like App Memory for Mobile Task Automation*，§§2–5、7；Fig.7 / §7.3.4–5（PDF pp.12–13）视觉核验。目录沿用早期 *Explore, Select, Derive, and Recall* 标题，不能算两篇。

**机制**：预先探索页面，建立应用功能与子任务图；执行时 Explore→Select→Derive，并把子任务分解与动作记录成记忆。再遇到类似任务时按当前界面属性、任务参数匹配，可匹配的动作直接复用，失配时用 LLM 适配。**命中记忆不等于整项任务零 LLM 调用**：高层规划和参数填充仍可能调用模型。GPT-4-turbo 负责主要推理，参数填充等轻任务使用 GPT-3.5。这里经验能直接替代一部分动作生成，而不仅是附在 prompt 中供模型参考。

**效果和协议**：§7.3 的八应用、80 任务消融，每个高层任务有两个参数不同的指令；warm-start 对比同 prompt 的 Derive 基线，平均延迟降低 **62.5%**、API 美元成本降低 **68.8%**；cold-start 分别增加 **3.9%、0.6%**。**该消融会在冷启动失败后由人修复并保存正确路径**，因此 warm-start 的高成功率含人工修复效果，不能标成完全自主学习。另一个 18 应用、185 任务的系统比较不使用 human-in-the-loop；不能把两个实验的最高准确率和最快加速拼在一起。

**成本/局限**：应用预探索属于额外投入；页面变化、子任务重复率、参数适配影响命中率。作者报告 Gmail 冷启动记忆命中差，说明同一 app 并不保证结构重复。**我们的推断**：这是“环境探索减少以后反复定位”很直接的先例；下一步必须同时对照重放命中率、失效检测与冷启动回本，不能仅用重复任务 warm-start 展示理想加速。[原文](https://arxiv.org/pdf/2312.03003v3)

### M03. Agent Workflow Memory（AWM）：文本工作流能减少步数，但执行宏也可能更脆弱

**已读**：正式 ICML 2025/PMLR 267 版本 §§2–3、Appendices D–F（15 页），另查 arXiv v1。Table 1（p.5）、11（p.14）、13（p.15）已视觉核验。

从成功轨迹中抽取可复用子任务，把具体实体替换成参数，保存文字描述及 state/thought/action 示例，在线模式由 LLM judge 筛出成功轨迹后继续归纳。核心 AWM 把这些 workflow 提供给 agent 参考，仍逐步生成动作，不等价于编译执行。

WebArena Table 1：AWM SR **35.5%**，BrowserGym **23.5%**；统一 AX-tree 对照为 **15.0%**。报告 steps **7.9→5.9**；摘要说成功任务步骤，未控制相同成功任务集合，不能当作严格同题延迟下降。正式版 §3.1 写 GPT-4o-2024-05-13、Table 1 caption 写 gpt-4，arXiv v1 则写 GPT-4-0613，存在模型标注不一致，复现前需查代码配置。

Appendix D/Table 11 的 AWM 自身 action generation 为 **33,718.5 tokens/任务**，trajectory evaluation **2,298.6**、workflow induction **1,344.6**；后两项约为 action generation 的 **10.8%**。这不是 matched baseline 的总 token 节省结果。正文把两项 4.0%/6.8% 的对应关系写反，按表读取。

Appendix F 试把 workflow 包装为可直接执行的高层动作 AWM-AS；Mind2Web Table 13 中 step SR **45.1→46.4**，task SR 却 **4.8→3.6**。作者指出静态 action 序列不能适应 popup/选项变化，需要动态观察与循环；该表旁正文又有 3.2 的不一致。**我们的推断**：是否跳过观察/推理需要前置条件与失败回退，文本复用成功并不能推出宏执行成功。[正式版](https://proceedings.mlr.press/v267/wang25bx.html)

### M04. ReasoningBank：步骤更少，总 token 仍略增

**已读**：arXiv:2509.25140v2 §§3–4、Appendix B/C、limitations；Table 1（p.7）、5（p.27）视觉核验。Google Cloud AI、UIUC、Yale 等；本笔记按预印本引用。

将 self-judged 成功与失败轨迹都整理为 title/description/content 形式的推理策略，按任务检索后用于下一次行动；记忆合并主要是追加。MaTTS 另通过并行多轨迹比较或顺序改进得到更强经验，属于扩大采样预算，应与基本记忆法分开比较。

WebArena 去除 Map 后的 684 个任务，Table 1 中 Gemini-2.5-Flash：无记忆 **40.5% SR / 9.7 steps**，ReasoningBank **48.8% / 8.3**；Pro 与 Claude 也呈步骤下降。**但是** Appendix C.2/Table 5：无记忆总 token **50,847.4**；ReasoningBank action generation **49,306.1** + judge **2,186.3** + extraction **1,562.1** = **53,054.5**，增加约 **4.3%**。该表没有把 dataset/backbone 单独标明，不能随意把它解释为所有模型的均值。

作者报告记忆检索太多会引入噪声，简单追加长期可能膨胀；失败判断来自 LLM，可污染记忆。**我们的推断**：这是质量/成本权衡改善与“加速”必须分开的清楚例子。失败轨迹抽象可能减少重试，但必须把反思、写入、检索 prompt 都记账。[原文](https://arxiv.org/pdf/2509.25140v2)

### M05. ExpeL：不改参数的经验学习不是低成本的同义词

**已读**：arXiv:2308.10144v3 方法、实验、Appendix J；AAAI 2024 正式录用及 DOI 已核。Table 6（p.38）视觉核验。

离线先用 ReAct/Reflexion 收集轨迹，比较 success/failure 成对样本及多个成功样本，LLM 以 ADD/EDIT/UPVOTE/DOWNVOTE 维护 insights；测试时检索成功示例并附上 insights。所谓 training 是记忆构建，不更新 actor 权重。实验 insight model 为 GPT-4-0613，actor 为 GPT-3.5-turbo-0613，须计入离线较强模型费用。

Appendix J：ReAct→ExpeL，HotpotQA 动作 **5.18→4.80**，但平均 trajectory tokens **1,319.75→4,310.06**；ALFWorld 动作 **14.82→14.30**、token **2,051.49→2,856.70**；WebShop **4.47→4.33**、**2,575.41→3,291.31**。Table 6 是字符串经 tiktoken 计算的 trajectory 统计，不应直接当作累计每次 API 输入的账单。

能力提升是真实研究目标，但完整 insights 的 prompt 开销、检索噪声与基础模型能力都构成边界。**我们的推断**：适合当“文本经验法”必要对照；若后续只证明动作变少而总成本上升，结果更像 ExpeL 而非净加速。[正式论文](https://ojs.aaai.org/index.php/AAAI/article/view/29936)；[所读版本](https://arxiv.org/pdf/2308.10144v3)

### M06. Dynamic Cheatsheet：积累可复用策略，主要证据仍是准确率

**已读**：arXiv:2504.07952v1 §§2、4–7，Table 1、4及 p.9 footnote 13；后者视觉核验。Stanford/Chan Zuckerberg Biohub 预印本。row125 链接错指 Self-Notes，正确条目为 row170。

DC-Cu 让模型答题后更新完整 cheatsheet；DC-RS 先检索少量过去问答再合成相关经验。无需标准答案监督，记忆可含策略与 Python 程序，依靠调用模型和代码执行学习。

论文展示数学/推理正确率增益，但效率段须谨慎：p.9 fn.13 在 AIME 2024 上 Claude Sonnet 的平均 token 为基线 **370**、DC-空记忆 **494**、DC-RS **1,035**、DC-Cu **1,831**。这不支持“已经测得总 token 净下降”；统计是否覆盖完整 curator 生命周期亦不明确。

作者局限包括弱模型生成/理解经验能力有限、错经验被强化、全量重写时丢失旧内容、检索噪声、顺序更新不利于批处理。**我们的推断**：可以复用它的在线经验生成思路，但要另做成本门控与缓存/工具化，不能从题目正确率提升直接推出加速。[原文](https://arxiv.org/pdf/2504.07952v1)

### M07. MemRL：RL 更新外部记忆效用，不等于训练 LLM

**已读**：arXiv:2601.03192v2 §§3–5、Appendix F/G，p.24 Table 11/Fig.11 已视觉核验。SJTU 等联合预印本。

每条外部记忆存 intent、experience、utility；先按语义筛，再按相似度与效用选择。得到 verifier reward 后进行 Monte-Carlo 风格的标量 Q 更新。LLM 权重冻结，既无反向传播到 LLM，也无需训练神经检索器；这类“RL”在我们的纯 API 范围内。

区分训练期 final-epoch SR、累积 CSR 与冻结记忆后的 held-out transfer；不能把“多次尝试中过一次”当作部署 pass@1。例：GPT-4o-mini 在 LifelongAgent OS 的 held-out transfer **67.3%→74.6%**（Table 11）。成本附录 HLE：每轮 2,500 问题、共 10 epochs，与 MemP 交互循环相同，平均约 **32K tokens/问**；Fig.11 的主要结论是算法额外开销小，明显耗时波动被作者归因于 API/网络，而不是可泛化的 speedup。

作者指出多记忆贡献分配、缺乏任务重叠、错误反馈等问题。**我们的推断**：用外部效用估计“哪条记忆实际有帮助”比纯语义检索更相关；若目标是加速，reward 应把正确率和真实增量成本都纳入，再验证，不是把成功奖励简单改名效率奖励。[原文](https://arxiv.org/pdf/2601.03192v2)

### M08. EXG：成功、失败与修复之间的链接可减少重试

**已读**：arXiv:2605.17721v1 §§2–4、Appendix C；Table 1/Fig.4（p.6）、Fig.5（p.7）、Fig.7及文字（p.12）视觉核验。UTS/UNSW 预印本。

任务 anchor 下保存 golden/warning case，加入 similarity 与 failed→fixed 的修复关系；检索 seed 后做有界图扩展，用有限预算提示优先注入修复与警示信息。固定模型，每题最多两次尝试；在线按反馈写入，另有 7:3 收集/冻结测试协议。

HumanEval 的 §4.3/Fig.4：EXG 平均 **1.20 calls/任务**，Reflexion **1.83**、SE-Agent **2.21**。LLM inference latency 为 **3,259ms**，相对二者 **3,416ms、4,689ms** 分别下降 **4.6%、30.5%**；检索额外约 **18–22ms**。不能把 LLM latency 当所有系统端到端延迟；EXG-Reflexion 组合反而 **3,943ms > 3,416ms**。效率图没有在 caption 中明确 backbone，不能自行补成跨模型均值。

Appendix C.1：HumanEval 总 token **117,378（Reflexion）→125,304（EXG）**，增加 **6.8%**；MuSiQue **4.07M→3.24M**，下降 **20.4%**。更少调用未必更少输入 token。Table 1 不同方法的 pass@2 也有高低，不能忽略质量约束宣称全面占优。

**我们的推断**：相对于单条成功示例，明确记录“何种失败如何修复”很适合降低重试；目前主要是函数代码与 QA，不能直接外推复杂 UI、仓库或有状态工具执行。[原文](https://arxiv.org/pdf/2605.17721v1)

### M09–M10. G-Memory 与 DecentMem：多智能体经验复用的成本比较要选对基线

**G-Memory 已读**：NeurIPS 2025 正式 PDF §§4–5，尤其 Fig.3/§5.3（p.8），视觉核验。交互图记录 agent 之间细粒度动作与观察，query 图关联任务，insight 图抽象经验；检索后给不同 agent 相关的压缩轨迹/建议，避免同一大段记忆无差别传给所有 agent。其 Fig.3 的 PDDL+AutoGen：相对无记忆提高 **10.32 个百分点**，同时**增加 1.4M tokens**；另一记忆基线为增加 2.2M 换 4.07 点。作者的“token efficiency”是更好的质量/开销权衡，绝非少于无记忆。多 hop/过多 query 会带来不相关经验。[正式论文](https://papers.nips.cc/paper_files/paper/2025/hash/136a45cd9b841bf785625709a19c6508-Abstract-Conference.html)

**DecentMem 已读**：arXiv:2605.22721v1 §§3–4、6–7；Fig.4（p.9）视觉核验。Cambridge/UChicago 预印本。每个 agent 分别维护既有经验 exploitation pool 与新探索 pool，根据分阶段 judge 反馈更新二者的路由权重；模型权重不变。Qwen3-8B+BBH：DyLAN 下 token 从 G-Memory 的 **7.6×10^8→3.9×10^8**（约减 **49%**），accuracy **58.62%→65.52%**；但无记忆为 **3.2×10^8**，所以没有净 token 节省。AgentNet 是 **8.1×10^8→5.5×10^8**（约减 **32%**），图中箭头误写 −42%，按柱值与正文采用 32%。§7.2 未清晰拆开全部 judge/记忆维护成本。所谓学习更快还包括随任务数收敛更快，不能换算为部署延迟。[原文](https://arxiv.org/pdf/2605.22721v1)

**我们的推断**：若当前验证先做单 agent，不必先引入 MAS；它们更适合作为“角色相关检索”与“记忆访问效用路由”的后续参考。

### M11. SEDM：值得借鉴的是经验接纳的 A/B 思路，数字并未证明相对无记忆更便宜

**已读**：arXiv:2509.09498v3 §§3–4、Table 1–4，Table 2–4（p.10）视觉核验；多所高校与 Gradient 联合预印本。目录 row161 错链到 EvoPrompt；row160 标 WizardLM 却链到 SEDM，应按标题纠正，避免三篇混写。

自包含执行上下文 SCEC 保存输入/输出、工具响应摘要、seed/config，再 paired A/B 对照有无记忆，以 reward 增益减 latency/token penalty 接纳、更新、删除经验；语义相似度乘经验效用用于 retrieval。机制比“只检索看起来相似的轨迹”更接近成本敏感学习。

GPT-4o-mini，FEVER Table 2：无记忆 **57 分、1.65M prompt+24K completion**；G-Memory **62、3.62M+109K**；SEDM **66、2.47M+53K**。HotpotQA：无记忆 **34、2.46M+29K**；G-Memory **38、4.63M+114K**；SEDM **39、3.88M+55K**。所以省 token 是对 G-Memory 而非无记忆，且这些是 inference token，不能替代 paired replay/筛选全成本。没有对应秒的受控结果。

**可靠性边界**：论文称 environment-free replay 和跨模型版本 deterministic reproduction，存 seed 与历史工具结果不能保证新策略在真实有状态环境中的反事实结果；这是我们的方法论质疑，不能直接判作者实验无效。另 Table 1 的 open-domain 结果并非 SEDM 所有指标最佳，和笼统正文不符。**我们的推断**：借鉴 A/B utility gate，复现时应在可重置环境配对重跑，而非把工具 transcript replay 当环境等价。[原文](https://arxiv.org/pdf/2509.09498v3)

### M12. CTIM-Rover：已有“代码仓库越做越懂”的相近负结果

**已读**：arXiv:2505.23422v1 §§3–6，Table 1（p.4）视觉核验。TUM/LMU 预印本。

基于 ExpeL 对成功及失败反思轨迹，先提通用软件工程知识，再提仓库级知识，期望复用项目结构、入口、惯例和坑；另外检索相似成功轨迹。o1 蒸馏，GPT-4o 执行；记忆含 236 条成功轨迹来源，测试为 7 仓库的 45 个 held-out SWE-bench Verified 样本。

Table 1：AutoCodeRover **42%**，完整 CTIM-Rover **40%**，只加 CTIM **31%**。定性案例中，表面词语相似的经验把 agent 带往错误函数；模型总结也可能丢失具体可操作信息。作者认为应提升选择性检索、动态推理时机和表示。

**边界**：样本小且仓库分布偏斜，不能证明所有仓库记忆无效；但足以否定“经验越多当然越好”。未给出整体 latency/token 改善。**我们的推断**：仓库/environment 经验要记录适用条件与来源证据，以无记忆、简单检索、全量经验三者作为基线，避免只与弱系统比。[原文](https://arxiv.org/pdf/2505.23422v1)

### M13–M14. 两类相关但不能直接当部署加速的工作

**Memory Beyond Recall / DCPM**（arXiv:2606.09483v1）：已读 §§2–3 与 Table 1。同步根据对话新增/合并/替代事实，异步归纳 schema 与 intentions；读取时用 embedding+引用链而非额外 LLM 整理。实验证明长对话/个性化 QA 的质量，不是历史 task trajectory 学得可执行技能；“不增加读路径 LLM”是架构属性，本笔记不据此推导端到端加速倍数。异步维护仍消耗资源，冲突合并也依赖模型判断。[原文](https://arxiv.org/pdf/2606.09483v1)

**Mem²Evolve**（arXiv:2604.10923v1）：已读 §§3–5、Table 2/4 的文字层，未对 Table 4 做单独图像核验，因此这里不转录精确结果。经验指导新工具创建、测试修复；工具/MCP/专家 agent 配置成为资产，执行成败又产生经验。论文主结果各 run 以基本空记忆开始，跨任务 transfer 是单独协议；工具创建修复迭代下降属于局部开发开销，未建立完整任务 latency/token/API$ 的降低。本条供工具分支交叉引用。[原文](https://arxiv.org/pdf/2604.10923v1)

### 需要严格区分的边界与纠错

- **MrSteve**：原文 §3.2 明确用 PPO 训练 VPT-Nav 的 goal encoder、LoRA、policy/value。PEM 的地点/事件记忆与减少重复探索可借鉴，但完整系统不是“仅调用冻结 API，无辅助训练”。只读了 HTML 方法/局限，没有用其精确结果支撑净加速。[原文](https://arxiv.org/html/2411.06736v5)
- **MemGen**：原文 Appendix B/C 分阶段训练 memory weaver（SFT/GRPO）和 memory trigger；reasoner 冻结不代表整体无需训练。[原文](https://arxiv.org/html/2509.24704v2)
- **MemQ**：在 provenance DAG 上做标量 Q/TD(λ) 信用回传，不因题目含 Q-learning 就排除。当前读到方法与实验协议，未完成效率核查，列 method；其 learning curve 更快不能先当作推理加速。[原文](https://arxiv.org/html/2605.08374v3)
- **A-Mem、Mem0、SCM、MemoryOS、H-MEM 等**：主要处理过去对话/事实的记忆与检索；可以减少上下文负担，但需要另证明“学会任务方法并少执行步骤”。A-Mem 与 ACE 的进一步证据由主报告合并，本笔记不伪称重复全文阅读。Mem0 已核到 ECAI 2025 正式 accepted list/论文 DOI，不应仅因作者是公司就排除；本分支仍按长对话背景处理。[ECAI accepted list](https://ecai2025.org/accepted-papers/)；[Mem0 正式 DOI](https://doi.org/10.3233/FAIA251160)

### 完整性补核：Agon 与 Prism 是否遗漏了更直接的加速近邻

补核了两篇原文 HTML 的方法、评估及成本相关段落，未发现比上述 Metis、MobileGPT 等更直接、应补入主报告的任务执行加速近邻。这里不转录未做 PDF 图像核验的精确数值。

**Agon（row133）**：§2.1 的 Prompt Economy 以角色 prompt 与交接协议的维护量定义复用 ROI；Table 2 比较提示语料规模，§3.9 提供调用成本与时间审计，附录提供研究项目投入。它的核心是复用研究编排流程与生产者—审查者循环，尚未给出同任务 agent 在有无经验改进下的部署降本对照。原文确认作者来自 University of Maryland、CUHK、Stanford，因此原先“机构资格未核”已解决；整合清单改列 **background**，而不是因来源排除。[原文 §§2–3、Appendices A/B](https://arxiv.org/html/2606.24177v1)

**Prism（row155）**：§3.5 明确将记忆的预期信息价值减检索成本作为目标，并更新检索策略权重；Table 1 报告 LoCoMo 的 p95 与 Savings，Table 3 是 TSP、circle packing、kernel 的演化搜索。前者属于对话记忆访问效率，后者主要是搜索改进率；Savings 的完整统计范围和抽取、整合等新增成本仍不清楚。其 VoI 用于**检索记忆**，不能直接视为已验证收益导向的**真实环境探测**。作者信息为 AI Researcher、Basel 及 Roche 邮箱，尚未确认符合项目核心证据的正式发表或强研究机构资格。保留 **uncertain**，但阅读深度已从摘要升级为原文选读。[原文 §3.5、§5、§6.4](https://arxiv.org/html/2604.19795v1)

## 2. 待合并的 D 台账增补（机制，不宣称新颖性）

| 局部建议 | 机制/适用场景 | 原文依据 | 应否进入近期验证 |
|---|---|---|---|
| Memory-01 | 文本经验与执行资产分层；重复命中后才编译 | Metis M01；AWM 宏负结果 M03 | 是，先对照文本、代码、混合 |
| Memory-02 | 记录环境结构并直接重放；失配时才推理 | MobileGPT M02 | 是，必须加入状态适用条件与回退 |
| Memory-03 | 成功/失败/修复关系帮助减少重试 | ReasoningBank M04、EXG M08 | 是，与只存成功轨迹比较 |
| Memory-04 | 语义检索之外学习真实效用 | MemRL M07、SEDM M11；MemQ 待核 | 是，但成本 reward 需实测 |
| Memory-05 | 按角色提取多智能体记忆、按效用选择池 | G-Memory / DecentMem M09–10 | 后续；不要使首次验证复杂化 |
| Memory-06 | 仓库知识的条件、证据与失效管理 | CTIM-Rover M12 | 是，负例必测 |

## 3. 待合并的 E 台账补丁（应收紧的 claim）

1. 将“ReasoningBank 加速”收紧为“报告交互步数下降；所给全 token 表增加约 4.3%”。
2. 将“AWM 节省 25% 成本”收紧为“7.9→5.9 steps；该版本未建立总成本净节省”。
3. 将“Dynamic Cheatsheet 越做越省 token”改为未验证假设；AIME 的报告值更高。
4. 将“G-Memory / DecentMem / SEDM token efficiency”明确基线；它们相对 no-memory 仍有 token 增加的设置。
5. 将“Metis 总成本降低”收紧为“executor tokens 下降，reflection 单列，trajectory generation 排除”；回本量不能只用遗漏成本的分子计算。
6. 将“MobileGPT 自主 warm-start 高准确率”标注实验是否人工修复；区分系统比较与 §7.3 消融。
7. 将“训练以外”拆为（a）完全外部状态更新；（b）基础 LLM 冻结但辅助神经模块训练；（c）在线参数更新。MemRL 属 a，MemGen/MrSteve 含 b，TMEM 属 c。
8. 保留 CTIM-Rover 的负结果，但注明仅 45 样本、7 仓库，不能泛化否定全部记忆方案。

## 4. 尚待解决/建议验证的问题

- **共同成本口径**：分别记录首次探索、轨迹收集、反思、检索、执行、维护/验证/回退的 token、calls、API$、wall-clock；最终给累计成本及回本曲线。现有论文没有统一可横比的总成本表。
- **相同题目/质量下比较**：成功率门槛、共同完成任务集合、固定最大尝试数一起报；避免 agent 早停失败被算“更快”。
- **同环境复用与泛化**：至少区分同模板换参数、同环境新任务、环境界面/API变化；Metis 重采样和 MobileGPT warm-start 不能替代所有设置。
- **验证而非宣称因果**：语义相似检索、效用检索、失败修复记忆、直接执行资产分开消融；静态 transcript replay 不能替代可重置真实环境的 paired trial。
- **最值得先复现的组合**：无记忆 → AWM/ExpeL 式文本经验 → MobileGPT 式有条件重放或 Metis 式工具化；若只有一轮实验预算，优先 Metis/MobileGPT 的执行层思路，而非再验证单纯 memory QA 排行榜。
- 未展开的 Thought-Retriever、EvolveMem、AEL、PRIME 等仍可提供检索/路由线索；当前仅摘要初筛，不做性能判定。Agon 已补核为研究编排背景；Prism 已选读方法与成本表，但完整成本及来源资格仍待核。Prism、SHIMI、PBFT pruning 保持 uncertain，不用未经充分核查的大数字支撑研究计划。

## References

下面为本笔记实质讨论作品的完整作者、标题、版本与来源。版本是实际阅读版本；“预印本”不表示已独立确认所有实验可复现。65 条初筛的原链接及更正链接另见 JSON。

1. Zijie Dai; Siuhin He; Hui Li; Qihui Zhou; Jiajun Li; Mingcong Song; Guoping Long; Hongjie Si; Xin Yao; Lin Zhang; James Cheng; Xiao Yan. **Metis: Bridging Text and Code Memory for Self-Evolving Agents**. 预印本（2026）. 所读/核查版本：arXiv:2606.24151v1. [来源](https://arxiv.org/abs/2606.24151)。

2. Sunjae Lee; Junyoung Choi; Jungjae Lee; Munim Hasan Wasi; Hojun Choi; Steven Y. Ko; Sangeun Oh; Insik Shin. **MobileGPT: Augmenting LLM with Human-like App Memory for Mobile Task Automation**. ACM MobiCom 2024. 所读/核查版本：arXiv:2312.03003v3. [来源](https://arxiv.org/abs/2312.03003)。目录/abs仍保留早期标题 Explore, Select, Derive, and Recall；实际PDF正文为正式标题。

3. Zora Zhiruo Wang; Jiayuan Mao; Daniel Fried; Graham Neubig. **Agent Workflow Memory**. ICML 2025, Proceedings of Machine Learning Research 267:63897–63911. 所读/核查版本：正式PMLR版；另查arXiv:2409.07429v1. [来源](https://proceedings.mlr.press/v267/wang25bx.html)。

4. Siru Ouyang; Jun Yan; I-Hung Hsu; Yanfei Chen; Ke Jiang; Zifeng Wang; Rujun Han; Long T. Le; Samira Daruki; Xiangru Tang; Vishy Tirumalashetty; George Lee; Mahsan Rofouei; Hangfei Lin; Jiawei Han; Chen-Yu Lee; Tomas Pfister. **ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory**. 预印本（2025）. 所读/核查版本：arXiv:2509.25140v2. [来源](https://arxiv.org/abs/2509.25140)。

5. Andrew Zhao; Daniel Huang; Quentin Xu; Matthieu Lin; Yong-Jin Liu; Gao Huang. **ExpeL: LLM Agents Are Experiential Learners**. Proceedings of the AAAI Conference on Artificial Intelligence 38(17):19632–19642, 2024. 所读/核查版本：arXiv:2308.10144v3. [来源](https://arxiv.org/abs/2308.10144)。[正式 DOI](https://doi.org/10.1609/aaai.v38i17.29936)

6. Mirac Suzgun; Mert Yuksekgonul; Federico Bianchi; Dan Jurafsky; James Zou. **Dynamic Cheatsheet: Test-Time Learning with Adaptive Memory**. 预印本（2025）. 所读/核查版本：arXiv:2504.07952v1. [来源](https://arxiv.org/abs/2504.07952)。

7. Shengtao Zhang; Jiaqian Wang; Ruiwen Zhou; Junwei Liao; Yuchen Feng; Zhuo Li; Yujie Zheng; Weinan Zhang; Ying Wen; Zhiyu Li; Feiyu Xiong; Yutao Qi; Bo Tang; Muning Wen. **MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory**. 预印本（2026）. 所读/核查版本：arXiv:2601.03192v2. [来源](https://arxiv.org/abs/2601.03192)。

8. Yuxin Jin; Siyuan Zhang; Hanchen Wang; Lu Qin; Ying Zhang; Wenjie Zhang. **EXG: Self-Evolving Agents with Experience Graphs**. 预印本（2026）. 所读/核查版本：arXiv:2605.17721v1. [来源](https://arxiv.org/abs/2605.17721)。

9. Guibin Zhang; Muxin Fu; Kun Wang; Guancheng Wan; Miao Yu; Shuicheng Yan. **G-Memory: Tracing Hierarchical Memory for Multi-Agent Systems**. Advances in Neural Information Processing Systems 38 (NeurIPS 2025). 所读/核查版本：NeurIPS2025正式PDF；另查arXiv:2506.07398v2. [来源](https://papers.nips.cc/paper_files/paper/2025/hash/136a45cd9b841bf785625709a19c6508-Abstract-Conference.html)。

10. Guangya Hao; Yunbo Long; Zhuokai Zhao. **Self-Evolving Multi-Agent Systems via Decentralized Memory**. 预印本（2026）. 所读/核查版本：arXiv:2605.22721v1. [来源](https://arxiv.org/abs/2605.22721)。

11. Haoran Xu; Jiacong Hu; Ke Zhang; Lei Yu; Yuxin Tang; Xinyuan Song; Yiqun Duan; Lynn Ai; Bill Shi. **SEDM: Scalable Self-Evolving Distributed Memory for Agents**. 预印本（2025）. 所读/核查版本：arXiv:2509.09498v3. [来源](https://arxiv.org/abs/2509.09498v3)。

12. Tobias Lindenbauer; Georg Groh; Hinrich Schütze. **From Knowledge to Noise: CTIM-Rover and the Pitfalls of Episodic Memory in Software Engineering Agents**. 预印本（2025）. 所读/核查版本：arXiv:2505.23422v1. [来源](https://arxiv.org/abs/2505.23422v1)。

13. Tianxiang Fei; Mingyang Song; Mao Zheng; Xiang Yu. **Memory Beyond Recall: A Dual-Process Cognitive Memory System for Self-Evolving LLM Agents**. 预印本（2026）. 所读/核查版本：arXiv:2606.09483v1. [来源](https://arxiv.org/abs/2606.09483)。

14. Zihao Cheng; Zeming Liu; Yingyu Shan; Xinyi Wang; Xiangrong Zhu; Yunpu Ma; Hongru Wang; Yuhang Guo; Wei Lin; Yunhong Wang. **Mem²Evolve: Towards Self-Evolving Agents via Co-Evolutionary Capability Expansion and Experience Distillation**. 预印本（2026）. 所读/核查版本：arXiv:2604.10923v1. [来源](https://arxiv.org/abs/2604.10923)。

15. Guibin Zhang; Muxin Fu; Shuicheng Yan. **MemGen: Weaving Generative Latent Memory for Self-Evolving Agents**. 预印本（2025）. 所读/核查版本：arXiv:2509.24704v2. [来源](https://arxiv.org/abs/2509.24704)。

16. Junwei Liao; Haoting Shi; Ruiwen Zhou; Jiaqian Wang; Shengtao Zhang; Wei Zhang; Ying Wen; Zhiyu Li; Feiyu Xiong; Bo Tang; Weinan Zhang; Muning Wen. **MemQ: Integrating Q-Learning into Self-Evolving Memory Agents over Provenance DAGs**. 预印本（2026）. 所读/核查版本：arXiv:2605.08374v3. [来源](https://arxiv.org/abs/2605.08374)。

17. Prateek Chhikara; Dev Khant; Saket Aryan; Taranjeet Singh; Deshraj Yadav. **Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory**. ECAI 2025. 所读/核查版本：arXiv:2504.19413v1. [来源](https://arxiv.org/abs/2504.19413)。[正式 DOI](https://doi.org/10.3233/FAIA251160)；本分支仅摘要筛查与录用核验。

18. Junyeong Park; Junmo Cho; Sungjin Ahn. **MrSteve: Instruction-Following Agents in Minecraft with What-Where-When Memory**. ICLR 2025（目录及作者实验室公开列表）；本次所读 arXiv:2411.06736v5 HTML 的方法/局限。 [原文](https://arxiv.org/html/2411.06736v5)；原目录 [OpenReview](https://openreview.net/forum?id=CjXaMI2kUH)。

19. Youran Sun; Xingyu Ren; Chugang Yi; Jiaxuan Guo; Kejia Zhang; Jianda Du; Haizhao Yang. **Agon: An Autonomous Large-Scale Omnidisciplinary Research System Built on Prompt Economy**. 预印本（2026）. 所读版本：arXiv:2606.24177v1，HTML 方法与成本相关段落。[原文](https://arxiv.org/html/2606.24177v1)。

20. Suyash Mishra. **Prism: An Evolutionary Memory Substrate for Multi-Agent Open-Ended Discovery**. 预印本（2026）. 所读版本：arXiv:2604.19795v1，HTML 方法、实验表与局限。[原文](https://arxiv.org/html/2604.19795v1)。
