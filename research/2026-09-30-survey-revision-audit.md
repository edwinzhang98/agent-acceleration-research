# 固定权重 Agent 加速报告的需求对照与修订核验

日期：2026-09-30。输入是用户提供的 Claude Code 工作计划，作为需求检查清单，不是已完成的研究或证据。修订对象为 `notes/part3/2026-09-30-self-improvement-agent-acceleration-review-zh.md` 及同名 Word，并扩展原筛查索引。前一版依据为 E644–E668、D436–D445。

并行研究计划拟从 E669/D446 编号，本轮采用 SR2 局部标识，待统一入账时映射，不抢占全局编号，也不重写 canonical dossier。下列结论的来源均为原论文，核验日期统一为2026-09-30；数量来自网页快照解析的条目标为 calc.。本轮没有复现实验。

## 1 核验表

| 局部ID | 前版或待核说法 | 一手证据与位置 | 处理 |
|---|---|---|---|
| SR2-E01 | 只有修改对象分类，没有说明持久更新的边界 | Survey v1 §3.2式4，PDF p13，短语“commits durable changes”；§8.1式26要求整个过程的表现与预算。详见补充核验文件V01–V07。 | 主文§一补配置、暂态、持久更新和评价定义；明确没有单调提升保证。 |
| SR2-E02 | 253方法行之后未筛59评测行 | 项目网站快照解析：253+59=312行；59行45个不同主链接、14额外重复；EV14原错链2601.08613。详见evaluation补充§1.3–1.4。 | calc.，补59逐条筛查、阅读深度及原错链/更正来源，不能称312篇全文阅读。 |
| SR2-E03 | TextGrad讲了直觉，缺形式化 | [TextGrad v1](https://arxiv.org/pdf/2406.07496v1) §2式4–11，PDF pp4–5；已看p4公式渲染。文字反馈与TGD更新明确分开。 | 用Critique/Backward/Edit改写并标明非原符号；不把字符串当可微参数。 |
| SR2-E04 | “参数”可能被误读为LLM权重 | [Trace v2](https://arxiv.org/pdf/2406.16218v2) §2.1 PDF p4：“parameters … can be heterogeneous”；OPTO=(Θ,ω,T)，τ=(f,g)。§3.2 p5讨论图粒度。 | 补原定义，θ可为代码/提示，反馈不必标量。 |
| SR2-E05 | GEPA预算和加速目标容易混淆 | [GEPA v2](https://arxiv.org/pdf/2507.19457v2) §2式1–2，PDF p4；优化任务得分，rollout预算B。 | 将一般模型+提示目标限制到固定权重，明确为本文改写；没有部署时间惩罚。 |
| SR2-E06 | SkillOpt的learning rate与选择集未形式化 | [SkillOpt v2](https://arxiv.org/pdf/2605.23904v2) §3.1式1–3，PDF pp4–6；已看p5渲染。 | 补固定harness与模型、候选生成/选择/测试集合；LR是文字编辑预算。 |
| SR2-E07 | ACE缺更新对象定义 | [ACE v3](https://arxiv.org/pdf/2510.04618v3) §3 PDF pp4–5。 | Merge/Dedup为本文对算法的改写，不伪造数值最优化原式。 |
| SR2-E08 | Meta-TTL最终评估统称“未见任务或域”过宽 | [Meta-TTL v4](https://arxiv.org/pdf/2604.00830v4) §3式1–4 PDF p4、§4.1 p5：Jericho ID为相同游戏，其他ID留出实例，另有OOD；p4公式已看渲染。 | 修正划分，解释加权回报曲线和episode重置；φ是文字meta-prompt。 |
| SR2-E09 | HGM只解释潜力概念，没有区分定义和估计器 | [HGM v3](https://arxiv.org/pdf/2510.21614v3) §3.2–3.3 PDF pp5–7，p6已看渲染：CMP目标为搜索后分支最佳者效用期望，估计汇总clade成功/失败计数。 | 补定义、剩余预算与策略依赖；不宣称估计器无偏或实际全局最优。 |
| SR2-E10 | 全框架目标可能被误读成资源成本最小化 | [StarHarness v1](https://arxiv.org/html/2608.24804v1) §3.1式1，HTML L79–88：“mean task score”；J虽称cost function但越高越好。 | 主文明确J不是美元；holdout是目标评价，搜索实际用开发/选择集。 |
| SR2-E11 | 验证门禁与最终留出关系需更清楚 | [HarnessFix v2](https://arxiv.org/html/2606.06324v2) §III-D L218–223；[AgentDevel v1](https://arxiv.org/html/2601.04620v1) §2.1式1–2、§2.4 L191–201。 | 补候选验收、P2F/F2P集合；AgentDevel gate用同一开发集，不称独立最终测试。 |
| SR2-E12 | 环境模型和规范/反馈机制未分开 | [VASO v1](https://arxiv.org/pdf/2606.05395v1) §3–4 PDF pp4–5，p4已看渲染。 | G、ψ、C、L、A_plan、M逐一定义，M为预定义环境动态，自动命题映射是保证的前提。 |
| SR2-E13 | 没有单列无训练造数据 | [SkillWeaver v1](https://arxiv.org/pdf/2504.07079v1) §2.1–2.3 pp3–5；[OpenSkill v1](https://arxiv.org/pdf/2606.06741v1) §2.1–2.2 pp3–5、式2–5；VASO §4。 | 分练习/输入生成、外部锚定代理测试、真实反例；数据用途决定是否出训练边界。 |
| SR2-E14 | 作者自述不足与本文推论容易混读 | OpenSkill §2.2.2 p4：“overfit the virtual tests”；Trace §3.2 p5论抽象粒度；其他作者限制见memory/evaluation补充。 | 主文建立标识约定；未标“作者自述”的缺少成本/泛化证据解释，不冒充作者承认。 |
| SR2-E15 | 未清楚区分环境动作价值和状态预测 | GLoW/WorldEvolver/SpeedRunner/ActionEngine原方法及附录，见memory-environment补充。 | 在主文更正GLoW无显式下一状态预测、WorldEvolver规则提取器的preservation限制；SpeedRunner无回放验收不等于无代码检查。 |

## 2 D ledger 待映射项

- **SR2-D01（补充覆盖，不撤销原计数）**：前版253仅为方法行。本轮追加59评测行，保留253方法分类计数；新总312也是目录行，不能改称独立论文数。
- **SR2-D02（正文修正）**：Meta-TTL的Jericho域内评估包含meta-training同游戏；删除“最终都在未见任务”这一宽泛暗示。
- **SR2-D03（正文限定）**：WorldEvolver预测与规则提取是不同部件，具体提取器偏preservation/frame rules；GLoW是探索价值/动作优势知识，不能统称完整环境动态学习。
- **SR2-D04（术语修正）**：SpeedRunner不要求环境回放验收，不表示完全没有代码分析/测试。SkillWeaver已记录前置条件，不能把“有条件技能”本身包装成创新。
- **SR2-D05（外部目录错链）**：ClawBench原目录链接2601.08613不相关，更正来源为作者官方仓库与2604.08523v2；原行保留。
- **SR2-D06（需求补齐）**：增加公式解释、造数据、机制与外部有效性评测、两条主线之外的方案；不把Claude计划里“已读314篇”继承为本轮阅读成果。

## 3 E ledger 补丁与正文落点

不修改旧E条目和canonical dossier。本轮为读者报告的增量：

- §一：正式分类、配置/暂态与持久更新、信号来源与更新对象为两条轴；评价曲线不自动保证速度。
- §二：253方法+59评测的真实覆盖、错链和阅读深度；作者限制/本文解释分界。
- §三：TextGrad/Trace/GEPA/SkillOpt/ACE/Meta-TTL的定义、符号与预算口径，修正Meta-TTL ID划分。
- §四–五：轨迹记忆与技能、环境规律的不同表示、预测与反馈闭环，以及方法原式的限制，详见memory-environment支持文件。
- §六：HarnessFix/StarHarness目标与接纳，HGM CMP目标与估计器分开。
- §七：AgentDevel/VASO定义、无训练造数据分支、评测选择及协议。
- §九：复现/迁移验证、场景证据补充、候选方法假设分别表述；增加记忆选择、外层搜索预算、工具说明与固定系统改进；质量约束下成本目标为本文提议。
- 筛查索引：保留原253方法行，追加EV01–EV59，旁列深度与更正说明。

## 4 仍未完成的核验

1. 253方法行中41条仍为待核；本次不是对所有相关论文逐页逐句全量审计。已经读方法/实验/相关附录的工作也不宣称每页所有论断均核过。
2. 评测12篇为任务与协议选读，不是12篇所有引用的全文复核；其余目录级项目不得被用作方法效果证据。
3. 候选新方法仍需选定实现后沿代码和引用链核新颖性；不以“未报告我们想要的数值”证明空白。
4. 固定权重实验没有运行，质量阈值、任务流、真实业务环境权限、预算均未假设已获决定。
5. 全局SR2→E/D编号映射待并行文献补充汇合；不在本轮占用另一计划已声明的起点。

## References

完整作者、正式发表与实际阅读版本见主报告末尾[1]–[53]；本文中的同名方法对应同一版本。[主报告](../notes/part3/2026-09-30-self-improvement-agent-acceleration-review-zh.md)。原文局部定位及评测完整参考文献另见[形式化与评测核验](2026-09-30-survey-revision-evaluation.md)、[轨迹与环境核验](2026-09-30-survey-revision-memory-environment.md)。本文件只做修订审计，不引入另一套独立论文计数。
