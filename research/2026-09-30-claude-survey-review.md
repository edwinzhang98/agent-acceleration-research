# Claude 综述挖掘稿：HTML 阅读版与审核记录

2026-09-30，Codex。对象：[Claude 原稿](../notes/part3/2026-09-30-self-improvement-survey-mining-zh.md)；成品：[HTML 阅读版](../notes/part3/2026-09-30-self-improvement-survey-mining-zh.html)。原 Markdown 未修改，HTML 的实质改句可在“审核”标签逐条查看。

报告提供了有价值的方法与实验线索，多项主要数字核查后可以保留。影响研究建议的主要问题，是把“没有每次成功指标”推成“没有加速目标”、遗漏 ReAP 的直接加速数据，以及少数训练边界和指标量纲混用。修订后，应先比较文字记忆与代码技能两条基线，并把 SICA、SEDM、SpeedRunner 纳入最近邻；当前证据不支持把每次成功口径或成本感知记忆本身称为新方法。

本轮逐段审读报告，三路回查关键论文的方法、结果表及相关附录，并做结构与引用链检查。没有重新全文审计所有 82 篇，也没有复现实验；沿用原稿的“已审计”标签仅表示 Claude 原有记录。本轮 primary-paper 核查深度和版本分别见[记忆/提示](2026-09-30-claude-survey-audit-memory.md)、[工具/框架](2026-09-30-claude-survey-audit-tools.md)、[环境/评测](2026-09-30-claude-survey-audit-environment.md)；[结构核查](2026-09-30-claude-survey-audit-structure.md)包含候选明细、计数与截断检查。

## 1. 核验表：原判断、证据位置与处理

| ID | 核查项 | 原文依据 / 定位 | 判定与处理 |
|---|---|---|---|
| D595 | 缺报每次成功指标，不等于没有加速目标 | [SICA v2 · §3、Table 1](https://arxiv.org/pdf/2504.15228v2)；[SEDM v3 · §3 Eq.3–7](https://arxiv.org/pdf/2509.09498v3)；[SpeedRunner v1 · §3–4、Appendix A](https://arxiv.org/pdf/2608.11338v1) | 保留每次成功的统计口径；研究区别应落在正确性约束、完整预算、适用条件与任务流协议，并进一步与已有方法实测比较。 |
| D596 | ReAP 被漏掉了直接加速结果 | [ReAP v1 · §4–5、Tables 1–2](https://arxiv.org/pdf/2506.02158v1) | 相似新任务 Reflection：221k→83k token、682→327 秒、11.92→8.45 步，成功率 +11 点。文本记忆也可能直接加速；需计入建库并在我们的任务上复验。 |
| D597 | 成本感知记忆效用已有直接先例 | [SEDM v3 · §3 Eq.3–7](https://arxiv.org/pdf/2509.09498v3) | C4 改为验证和扩展已有方法；SEDM 未报告实测延迟，机制存在和收益已被验证须分开。 |
| D598 | HGM 的 CPU 小时不等于墙钟重叠 | [HGM v3 · §2–4、Table 2](https://arxiv.org/pdf/2510.21614v3) | 保留 HGM 的搜索资源效率结果，撤回把它直接映射到时间重叠项的判断。 |
| D599 | 冻结任务 LLM 与全流程免训练要分开 | [PROMST v4 §3.2](https://arxiv.org/html/2402.08702v4)；[Memento v2 §4.2、§5.3](https://arxiv.org/html/2508.16153v2)；[Continual Harness v1 · §3.3、4.5、Figure 17](https://arxiv.org/pdf/2605.09998v1) | 第一版免训练基线应按实验分支筛选；保留冻结模型分支，明确排除训练分支，不必整篇排除。 |
| D600 | 累计 token、工具调用和单次上下文不能混用 | [Continual Harness v1 · §3.3、4.5、Figure 17](https://arxiv.org/pdf/2605.09998v1)；[Adaptive Auto-Harness v2 Tables 5、14](https://arxiv.org/pdf/2606.01770v2) | 保留费用和总量的原始测量；停止从累计量推出单次上下文缩短，或从工具调用直接推出模型步数下降。 |
| D601 | 环境模型的训练边界、错误率与额外调用需拆开 | [WMA v2 · §6.2、Figure 7](https://arxiv.org/pdf/2410.13232v2)；[WorldEvolver v2 · Algorithm 1、Tables 12–13](https://arxiv.org/pdf/2606.30639v2) | 采用逐方法、逐实验口径；保留混合的规划收益和组件开销，不作端到端加速保证。 |
| D602 | WALT 的约 14 次是粗略摊销，不是净回本 | [WALT ICLR 2026 正式稿 §4.6](https://proceedings.iclr.cc/paper_files/paper/2026/file/5b175f9e93873e3a10a6ce43dbb82e05-Paper-Conference.pdf) | 保留作者估算并说明遗漏项；我们的累计净收益需包括构造、选择、复用执行及维护。 |
| D603 | 文本梯度是反馈与编辑机制，不是数值求导 | [TextGrad v1 §1–3.3、附录 A](https://arxiv.org/html/2406.07496v1) | 解释反向传递文字反馈的流程，并把验证集采纳门限定到相应提示优化实验。 |
| D604 | 每次成功是均摊口径；公式缩写应标明 | 报告及本轮上下文/结构检查；不是论文实验结论 | 补足均摊、任务分布及维护成本条件；“照抄原式”改为“按定义重排并标明缩写”。 |
| D605 | 项目页分区名称不能代替训练状态判断 | [WorldEvolver v2 · Algorithm 1、Tables 12–13](https://arxiv.org/pdf/2606.30639v2)；[综述项目页](https://selfimproving-agent.github.io/#overview) | 保留 77 这个目录条目数；按具体方法及实验分支判断是否训练，不推算未经逐篇核验的“76 篇训练”。 |
| D606 | 跨论文不能排出“最稳定”和“最不可靠” | [ReAP v1 · §4–5、Tables 1–2](https://arxiv.org/pdf/2506.02158v1)；[Metis v1 Table 1–2](https://arxiv.org/pdf/2606.24151v1)；[RQGM v2 Figure 9](https://arxiv.org/pdf/2606.26294v2) | 将最强判断改为候选优先级和局部证据，新增统一预算与任务流下的对照实验。 |
| D607 | 工具化对非模型时间的作用取决于实现 | [SkillWeaver v1 §3](https://arxiv.org/pdf/2504.07079v1)；[SpeedRunner v1 · §3–4、Appendix A](https://arxiv.org/pdf/2608.11338v1) | 把“非模型时间不变或上升”的全称判断改为条件分析，不用宏动作数直接替代耗时。 |
| D608 | 反复使用真值的选择集不是独立最终测试 | [CoEvoSkills v3 Algorithm 1](https://arxiv.org/pdf/2604.01687v3) | 允许真值参与开发验收时，必须另设独立最终测试；在账本中分开开发、选择与最终评测。 |
| D609 | SICA 数值可保留，准确率分母未说明 | [SICA v2 · §3、Table 1](https://arxiv.org/pdf/2504.15228v2) | 不判定原论文数字错误；保留表值、最佳与最终轮区别，标出无法还原成功数。 |
| D610 | GenericAgent 的首末改善不是代码化单独贡献 | [GenericAgent v1 §4.4、Table 8](https://arxiv.org/pdf/2604.17091v1) | 保留首末数值和单条序列限定；不将 token 全额合计等同于实际账单。 |
| D611 | 训练选项的用户归因尚未核实 | 报告及本轮上下文/结构检查；不是论文实验结论 | 将训练部分标为原稿提出的扩展选项，免训练仍为当前范围。无需为完成 HTML 而等待这项偏好确认。 |
| D612 | 目录记录数与独立论文数要分别读 | 报告及本轮上下文/结构检查；不是论文实验结论 | HTML 明示 421 个候选目录记录、336 条摘要细目与 88 条书目，不将这些数都叫独立论文数。5 条筛选状态及 55 条截断核读标签仍按原记录保留，最终论文计数需统一去重键后重算。 |

## 2. D 台账追加（D595–D612）

这些 D 编号记录报告层面的解释、遗漏及信息组织问题。D598/HGM、D600/累计 token 落实已有 D536/D545 的边界，不再把原论文数字重复判成错误。

- **D595 — 缺报每次成功指标，不等于没有加速目标。** 原稿从“未按每次成功报告”推到了“没有加速为主目标”，且把指标称作新想法。SICA 的原文效用已包含费用和墙钟，SpeedRunner 是原稿 §9 承认但未展开的成本导向近邻。 处理：保留每次成功的统计口径；研究区别应落在正确性约束、完整预算、适用条件与任务流协议，并进一步与已有方法实测比较。
- **D596 — ReAP 被漏掉了直接加速结果。** 原稿只保留 ReAP 重做旧任务的步数，漏掉 §5 新任务实验的时间和 token。原论文的表 1 还报告重复旧任务 Summary 的 token 221k→58k、时间 682→334 秒；不能把两种记忆和协议混成一行。 处理：相似新任务 Reflection：221k→83k token、682→327 秒、11.92→8.45 步，成功率 +11 点。文本记忆也可能直接加速；需计入建库并在我们的任务上复验。
- **D597 — 成本感知记忆效用已有直接先例。** SEDM v3 Eq.3–7 的准入分同时含性能、延迟和 token；记忆初始权重来自该分数，检索时结合相似度与权重。原稿只讨论了准入，导致 C4 新颖性判断偏强。 处理：C4 改为验证和扩展已有方法；SEDM 未报告实测延迟，机制存在和收益已被验证须分开。
- **D598 — HGM 的 CPU 小时不等于墙钟重叠。** 517/1,231 的表值正确；量纲是分配 CPU 小时。没有同步 HGM 对异步 HGM 的消融，也不能反向断言收益主要由预算分配造成。此项落实原台账 D536 的已有边界。 处理：保留 HGM 的搜索资源效率结果，撤回把它直接映射到时间重叠项的判断。
- **D599 — 冻结任务 LLM 与全流程免训练要分开。** PROMST 的评分器、Memento 的参数化检索、Harness-R1 的编辑器涉及辅助训练；Continual Harness 另有更新任务模型的实验分支。 处理：第一版免训练基线应按实验分支筛选；保留冻结模型分支，明确排除训练分支，不必整篇排除。
- **D600 — 累计 token、工具调用和单次上下文不能混用。** Continual Harness Figure 17 纵轴为按角色累计的近似 token，原文自己的每步解释也存在量纲张力；Adaptive 的工具调用均值与整个任务流 token 合计属于不同分母。 处理：保留费用和总量的原始测量；停止从累计量推出单次上下文缩短，或从工具调用直接推出模型步数下降。
- **D601 — 环境模型的训练边界、错误率与额外调用需拆开。** WMA 与 WorldEvolver 方法不同。42% 的分母是 WMA 抽查的 50 个错误预测；WorldEvolver 的预测模块可能重复调用。置信区间重叠也不是差异不显著的充分判据。 处理：采用逐方法、逐实验口径；保留混合的规划收益和组件开销，不作端到端加速保证。
- **D602 — WALT 的约 14 次是粗略摊销，不是净回本。** WALT 正式稿 §4.6 用工具构建价除基线执行价估算约 14 次，没有给出扣除复用运行成本后的同口径净回本。 处理：保留作者估算并说明遗漏项；我们的累计净收益需包括构造、选择、复用执行及维护。
- **D603 — 文本梯度是反馈与编辑机制，不是数值求导。** 原稿没有直接误称可微，但没有解答用户“为什么文本可以找梯度”的关键问题。原论文明确使用梯度作为语言反馈的比喻。 处理：解释反向传递文字反馈的流程，并把验证集采纳门限定到相应提示优化实验。
- **D604 — 每次成功是均摊口径；公式缩写应标明。** 固定任务窗口中的总成本除成功数，与同题重试到成功的期望花费不是无条件相同；原表部分公式省略了条件与求和范围。 处理：补足均摊、任务分布及维护成本条件；“照抄原式”改为“按定义重排并标明缩写”。
- **D605 — 项目页分区名称不能代替训练状态判断。** 原稿 §1.3 已正确写明 WorldEvolver 不训练，其他位置仍把 Foundation Model 目录的 77 条统一叫作改参数。 处理：保留 77 这个目录条目数；按具体方法及实验分支判断是否训练，不推算未经逐篇核验的“76 篇训练”。
- **D606 — 跨论文不能排出“最稳定”和“最不可靠”。** 任务、模型、重复次数、分母均不同。Metis 内部消融可比较文本与代码，但不能推出跨任务全局排名。RQGM 和 JudgeFlow 两个拆分也不能概括所有改进循环。 处理：将最强判断改为候选优先级和局部证据，新增统一预算与任务流下的对照实验。
- **D607 — 工具化对非模型时间的作用取决于实现。** 把多个动作包成一个工具，可能只减少模型参与，也可能同步删除重复导航和数据处理。反之，技能校验或恢复也会增加开销。 处理：把“非模型时间不变或上升”的全称判断改为条件分析，不用宏动作数直接替代耗时。
- **D608 — 反复使用真值的选择集不是独立最终测试。** CoEvoSkills 的真值成败反馈继续影响改进，并保留最佳真值检查点。原稿已写同题构建与计分，但借鉴建议需要带上这条边界。 处理：允许真值参与开发验收时，必须另设独立最终测试；在账本中分开开发、选择与最终评测。
- **D609 — SICA 数值可保留，准确率分母未说明。** 费用和时间公式、主要数字均得到支持，但作者称固定抽取 50 题；若按二值通过率解释，其表中 17%、53%、51% 的统计分母未解释。 处理：不判定原论文数字错误；保留表值、最佳与最终轮区别，标出无法还原成功数。
- **D610 — GenericAgent 的首末改善不是代码化单独贡献。** 九轮过程中任务实例和经验状态一起变化，前几轮主要是文字 SOP；代码阶段不应包揽全部降幅。 处理：保留首末数值和单条序列限定；不将 token 全额合计等同于实际账单。
- **D611 — 训练选项的用户归因尚未核实。** 本轮可见用户请求强调模型训练以外的工作。不能据此确认另一会话中的“小规模辅助训练”授权；也不能断言作者凭空添加，因为可能存在其他上下文。 处理：将训练部分标为原稿提出的扩展选项，免训练仍为当前范围。无需为完成 HTML 而等待这项偏好确认。
- **D612 — 目录记录数与独立论文数要分别读。** 附录 C 汇总 421 条候选，细表实际 336 条：64 条新读记录和 21 条复用主条目移到正文/阅读记录，另外 2 条复用仍留在 C.1，所以少 85 条不是 HTML 丢失。88 条书目减综述 1 条、暂缓排除 5 条等于 82 条合格书目；但复用记录含同文重复，深读记录与最终引用集也不完全相同。 处理：HTML 明示 421 个候选目录记录、336 条摘要细目与 88 条书目，不将这些数都叫独立论文数。5 条筛选状态及 55 条截断核读标签仍按原记录保留，最终论文计数需统一去重键后重算。

## 3. E 台账与精确文本修订

本轮没有覆盖原 E669–E1313 台账，也没有将旧条目的“已审计”标签改成本轮全量复核。主要问题发生在从证据到报告的推论阶段，E669（SICA 目标）、E1095（HGM CPU 小时）、E1307（累计 token）等数值本身保留。ReAP 表2、WorldEvolver 表13、辅助模型架构等补充证据以本审核 D 条目所附一手版本定位；没有给它们冒用旧 E 编号。

HTML 的实质改动以 [audit.json](../tools/survey-mining-reader/audit.json) 为机器可校验的精确补丁：每条 `old` 必须在当时文本中恰好出现一次才构建，`new` 是完整替换文本。下面逐项列出。公式的等义 LaTeX 排版另存 math-replacements.json；不与事实修订混为一类。

### D595 缺报每次成功指标，不等于没有加速目标

**1. 原文**

```text
**要点（我的判断，详见第 8.1 节）。**（1）自改进文献优化的是成功率，时间和费用只作预算或副作用。在本文核对过的 82 篇（去重）里，没有一项以每次成功的时间和费用为目标；把时间或费用写进选择或准入规则的有 SICA（选择效用含费用和墙钟，每题按尝试计）[E669] 和 SEDM（准入分含延迟和 token 项，但全文没有报告延迟值）[E670, E671]，按每次成功计费用的一项都没有（第 6.2 节）。（2）在本文核对过的文献里，把重复流程做成可调用的代码或可回放的 action，是同时降调用数或步数和 token 最稳定的做法：GenericAgent 从第 1 轮到跑代码化 SOP 的第 9 轮，LLM 调用 32→5、token 222,203→23,010（单条序列，无重复）[E672]；Metis 的代码工具由模型直接调用，执行者 token 和轮次下降 [E673, E674]；MobileGPT 的回放报告的是时延和费用下降 [E675]。只把经验写进上下文时，token 或时间常常上升（WebCoach、Meta-TTL、CTIM-Rover）[E676, E677, E678]；反例是 Metis 的纯文本记忆也降了 token 和步数：附录剖析实验（共同解出的子集，代码记忆指按任务的代码反思，不是 Metis 的代码化器）里文本 −38%/−27%，代码 −54%/−46% [E679]；开发集消融里纯文本的 token 反而少于纯代码（55.6K 对 58.7K），轮次略多（9.25 对 8.89）[E680]。（3）判断对错不可靠：LLM 判官与真值一致 72.7%（ReasoningBank，WebArena-Shopping，Gemini-2.5-flash）[E681]，自写测试对真值的精确率 56.9%（OpenSkill，84 题）[E682]；在报告了开销拆分的两项工作里，改进过程的钱主要花在评估候选上（RQGM 验证评估占混合 token 的 65–69%；JudgeFlow 一轮优化评估 $0.45、判官 $0.01）[E683, E684]。（4）方向 (a)、(b) 都有可直接借用的做法；第三部分新增的是每次成功的口径，以及以时间和费用为准的验收。
```

**替换**

```text
**要点（我的判断，详见第 8.1 节）。**（1）自改进描述更新机制，加速描述目标；已有工作直接把费用、墙钟或成本感知记忆写入目标。在本文核对过的 82 篇（去重）里，没有一项以每次成功的时间和费用为目标；把时间或费用写进选择或准入规则的有 SICA（选择效用含费用和墙钟，每题按尝试计）[E669] 和 SEDM（准入分含延迟和 token 项，但全文没有报告延迟值）[E670, E671]，按每次成功计费用的一项都没有（第 6.2 节）。（2）在本文核对过的文献里，把重复流程做成可调用的代码或可回放的 action，是值得优先验证的一类加速做法，但不同论文的设置不足以支持跨方法“最稳定”的排名：GenericAgent 从第 1 轮到跑代码化 SOP 的第 9 轮，LLM 调用 32→5、token 222,203→23,010（单条序列，无重复）[E672]；Metis 的代码工具由模型直接调用，执行者 token 和轮次下降 [E673, E674]；MobileGPT 的回放报告的是时延和费用下降 [E675]。只把经验写进上下文时，token 或时间常常上升（WebCoach、Meta-TTL、CTIM-Rover）[E676, E677, E678]；反例是 Metis 的纯文本记忆也降了 token 和步数：附录剖析实验（共同解出的子集，代码记忆指按任务的代码反思，不是 Metis 的代码化器）里文本 −38%/−27%，代码 −54%/−46% [E679]；开发集消融里纯文本的 token 反而少于纯代码（55.6K 对 58.7K），轮次略多（9.25 对 8.89）[E680]。（3）判断对错不可靠：LLM 判官与真值一致 72.7%（ReasoningBank，WebArena-Shopping，Gemini-2.5-flash）[E681]，自写测试对真值的精确率 56.9%（OpenSkill，84 题）[E682]；在报告了开销拆分的两项工作里，改进过程的钱主要花在评估候选上（RQGM 验证评估占混合 token 的 65–69%；JudgeFlow 一轮优化评估 $0.45、判官 $0.01）[E683, E684]。（4）方向 (a)、(b) 都有可直接借用的做法；第三部分采用每次成功的口径，以及正确性约束下的时间、费用验收；这些评测选择本身不构成已确认的新颖性。
```

**2. 原文**

```text
### 2.1 目标函数不同：他们优化能力，成本是约束或副作用
```

**替换**

```text
### 2.1 自改进是更新机制，加速是可以显式设定的目标
```

**3. 原文**

```text
自改进文献的目标量是能力 $m_t$（成功率或分数），成本 $b_t$ 是预算约束。
```

**替换**

```text
综述这一形式化以能力 $m_t$（成功率或分数）为目标、以成本 $b_t$ 为预算约束；不能据此概括所有一手方法，SICA 已将费用和墙钟直接写入选择效用 [E669]。
```

**4. 原文**

```text
所以"加速"不是自改进的一个子类，而是把自改进文献里当作副作用或预算的量（每次运行的时间、token、费用）当作主目标，并且要求改进自身的开销也进账。
```

**替换**

```text
因此，加速与自改进是两个相交的维度：前者描述目标，后者描述根据反馈更新系统的机制。我们的选择是在正确性约束下优化时间与费用，并把改进自身的开销计入；这不是把已有文献从未考虑过的成本首次加入目标。
```

**5. 原文**

```text
所以在本文核对过的范围内，没有找到以加速为主目标的自改进循环。这只说明检索范围，不作新颖性依据。
```

**替换**

```text
不能由缺少每次成功指标推出“没有以加速为目标的自改进循环”。SICA 已直接联合优化性能、费用与墙钟，SEDM 也有成本感知准入和检索。每次成功口径是本研究采用的评价定义，尚不能据此声称新颖性。另有本轮综述清单之外的直接近邻 [SpeedRunner](https://arxiv.org/pdf/2608.11338v1)：冻结模型，从历史轨迹归纳程序技能，以降低推理成本为问题，并将技能构建调用按批次摊入每回合美元成本；应纳入后续代码技能基线。
```

**6. 原文**

```text
类别：验收门本身是验证已有做法；"每次成功"的口径是新想法（本文核对过的文献里没有找到）。
```

**替换**

```text
类别：验收门和效率评价属于已有思路的组合验证；每次成功口径是本文采用的统计定义，不能由当前文献缺报判定其为新想法。
```

### D596 ReAP 被漏掉了直接加速结果

**1. 原文**

```text
- **ReAP（预印本）**：WebArena 上重做做过的任务，用失败轨迹的反思使先前失败的任务成功率 +20 点，先前成功的任务上最好也只到 84%（负迁移）；平均步数 11.92→10.08 [E879, E880]。反思模板显式问五类问题，含"更少步数的捷径"和"网站功能限制" [E815]。
```

**替换**

```text
- **ReAP（预印本）**：WebArena 上重做做过的任务，用失败轨迹的反思使先前失败的任务成功率 +20 点，先前成功的任务上最好也只到 84%（负迁移）；平均步数 11.92→10.08 [E879, E880]。反思模板显式问五类问题，含"更少步数的捷径"和"网站功能限制" [E815]。 另有相似新任务实验：已有轨迹按 80%/20% 分割、检索 top-5；Reflection 的成功率提高 11 个百分点。表 2 标注 70 个 WebArena 任务，平均总 token 221k→83k、执行时间 682→327 秒、步数 11.92→8.45（AgentOccam-Judge 成本表，GPT-4o 执行器）。未计建库和生成反思成本，也未报告重复运行方差。[本轮回查：ReAP §5、表 2](https://arxiv.org/pdf/2506.02158v1)。
```

**2. 原文**

```text
执行 token 和轮次都下降的是 Metis（把重复计划固化成工具）[E673]
```

**替换**

```text
执行 token 与步数同时下降的例子包括 Metis [E673]，以及 ReAP 的相似新任务 Reflection 设置；后者还报告时间下降（见上文表 2）。两者的任务、基线和成本范围不同，不能直接比较幅度
```

**3. 原文**

```text
| ReAP | 重做任务平均步数 11.92→10.08 | 时间 I；费用 I、II | [E880] |
```

**替换**

```text
| ReAP | 重做旧任务 Reflection：步数 11.92→10.08；相似新任务 Reflection（80/20 分割、top-5）：总 token 221k→83k、执行时间 682→327 s、步数 11.92→8.45，成功率 +11 点；成本表未含建库，无重复方差 | 同时报告任务执行时间、token 和步数；不能只归为步数代理指标 | [E880]；[原文 §5、Table 2](https://arxiv.org/pdf/2506.02158v1) |
```

**4. 原文**

```text
文字经验也能同时降，但幅度较小（Metis 附录剖析
```

**替换**

```text
文字经验也能同时降；ReAP 的新任务 Reflection 设置已报告 token、时间和步数同时下降。Metis 内部比较中，文本降幅较小（Metis 附录剖析
```

### D597 成本感知记忆效用已有直接先例

**1. 原文**

```text
把效用的奖励换成时间和费用，在本文核对过的文献里没有找到。位置：方案稿第 11 节新增待决项。类别：新想法。
```

**替换**

```text
SEDM 已按性能、延迟和 token 的加权净收益初始化记忆权重，并把权重用于检索，随后依据使用反馈调整。因此“成本感知记忆效用”已有先例；可以验证以实测美元/墙钟、正确性约束及维护成本改写效用是否更有效，但目前不能称为新的方法类别。位置：方案稿第 11 节候选项。类别：验证和扩展已有做法。
```

### D598 HGM 的 CPU 小时不等于墙钟重叠

**1. 原文**

```text
重叠（V）有数字的只有 HGM 的改进循环：800 次评估分配 CPU 小时 517 对 DGM 1,231（SWE-Verified-60；不是墙钟；作者把节省归因于异步并行扩展和评估）[E1095]
```

**替换**

```text
HGM 在同为 800 次任务评估的 SWE-Verified-60 设置下，分配 CPU 小时为 517 对 DGM 1,231。作者将优势归因于异步扩展与评估，但该比较没有隔离异步机制，也没有给出可计算墙钟重叠节省的测量；应计入改进搜索资源账，不能作为重叠（V）的定量证据 [E1095]
```

**2. 原文**

```text
用"团簇元生产力"（子树合并通过率）抽样父代、按单任务粒度评估并早停
```

**替换**

```text
用团簇元生产力的经验代理——子树累计成功评估数除以累计评估数——指导父代抽样，动态分配单任务评估预算；理论 CMP 是该子树最终可返回 agent 的期望效用，不能与经验通过率等同
```

**3. 原文**

```text
方案稿第 8.3 节把开销分成部署执行、学习维护、研究测评三个账本。对照上面的文献：(1) "改进过程的钱主要花在评估"这一条直接支持把验收重跑单独记账，并且要控制评估量，做法与 8.2 A4 相同的五种：更小或动态的验证子集（GEPA）[E753]、先用轻量检查挡住昂贵评估（综述）[E712]、单任务粒度评估并早停（HGM）[E1093]、分阶段评估先小集再扩大（DGM、GEA、Hyperagents）[E1077, E1162, E1163]、搜索期用便宜模型（RQGM）[E1132]。(2) "都按尝试计"意味着本文核对过的文献里没有现成的每次成功口径，我们要自己算。(3) AWM/ReasoningBank 把判官和抽取的 token 计入每任务 token 的做法，对应我们把"系统自己判断成败的检查"计入部署执行账本。(4) 在本文核对过的文献里，只有 SICA 在选择效用里同时放了美元费用和墙钟时间（SEDM 的准入分含延迟和 token 项，但没有报告任何延迟值 [E670, E671]），而且 SICA 的 token 升、费用和时间降 [E669, E1100]。这说明只看 token 会得出相反的结论，我们的验收要以时间和费用为准，token 只做记录。
```

**替换**

```text
方案稿第 8.3 节把开销分成部署执行、学习维护、研究测评三个账本。对照上面的文献：(1) "改进过程的钱主要花在评估"这一条直接支持把验收重跑单独记账，并且要控制评估量，做法与 8.2 A4 相同的五种：更小或动态的验证子集（GEPA）[E753]、先用轻量检查挡住昂贵评估（综述）[E712]、单任务粒度自适应分配评估预算（HGM）[E1093]、分阶段评估先小集再扩大（DGM、GEA、Hyperagents）[E1077, E1162, E1163]、搜索期用便宜模型（RQGM）[E1132]。(2) "都按尝试计"意味着本文核对过的文献里没有现成的每次成功口径，我们要自己算。(3) AWM/ReasoningBank 把判官和抽取的 token 计入每任务 token 的做法，对应我们把"系统自己判断成败的检查"计入部署执行账本。(4) 在本文核对过的文献里，只有 SICA 在选择效用里同时放了美元费用和墙钟时间（SEDM 的准入分含延迟和 token 项，但没有报告任何延迟值 [E670, E671]），而且 SICA 的 token 升、费用和时间降 [E669, E1100]。这说明只看 token 会得出相反的结论，我们的验收要以时间和费用为准，token 只做记录。
```

### D599 冻结任务 LLM 与全流程免训练要分开

**1. 原文**

```text
一个训练出来的分数预测器
```

**替换**

```text
在线微调的 Longformer-base（148M）评分器
```

**2. 原文**

```text
Q 用二元任务奖励训练，成败怎么判定文中未写 [E888]
```

**替换**

```text
参数化版本把 Q 实现为两层 MLP，以二元任务奖励的交叉熵损失训练，基础 LLM 不更新；成败判定细节仍未写清 [E888]。它与 MemRL/MemQ 对记忆条目的标量效用更新不同
```

**3. 原文**

```text
它们都不改任务模型的参数，主要改综述所说的记忆 m
```

**替换**

```text
本节冻结的是任务 LLM；Memento 的参数化读取另训辅助 Q 网络。各方法主要改综述所说的记忆 m
```

**4. 原文**

```text
在本节核对过的文献里，θ 在绝大多数工作里不变；例外是 Harness-R1 训练一个单独的"harness 工程师"（目标 agent 不动）[E1051]。
```

**替换**

```text
本节主要比较固定任务模型的实验分支。Harness-R1 训练外层编辑器，目标 agent 不动 [E1051]；Continual Harness 同篇另有 SFT/GRPO 预热、在线 SFT 的模型与 harness 共同更新分支（§3.3、§4.5、附录 D）。本文引用其固定 Gemini 模型分支的效率结果，不将训练分支纳入免训练证据。
```

**5. 原文**

```text
- 文献里训练了什么：任务模型权重（SEAgent 用 GRPO 加对抗模仿）
```

**替换**

```text
- 文献里训练了什么：PROMST 微调 148M Longformer 评分器，Memento 的参数化读取训练两层 MLP；Continual Harness 同篇有 SFT/GRPO 与在线 SFT 分支，不能把整篇视为免训练。任务模型权重方面（SEAgent 用 GRPO 加对抗模仿
```

### D600 累计 token、工具调用和单次上下文不能混用

**1. 原文**

```text
每次运行费用；子 agent 上下文低一个数量级对应 t11
```

**替换**

```text
每次运行 API 费用；Figure 17 另报按角色累计的估计输入 token（字符数÷4），不能据此确认单次上下文低一个数量级或量化 t11
```

**2. 原文**

```text
时间 I（工具调用轮次）、费用 II；方向随任务流相反
```

**替换**

```text
每题工具调用均值、任务流输入 token 合计、逐任务耗时之和；工具调用数不能直接当作模型决策步数，方向随任务流相反
```

**3. 原文**

```text
FutureX：每题工具调用 13.4→4.2、输入 token 55.5M→25.6M
```

**替换**

```text
FutureX：每题工具调用均值 13.4→4.2、整个任务流输入 token 合计 55.5M→25.6M
```

**4. 原文**

```text
效率方向随任务流不同：FutureX 上工具调用 13.4→4.2/题、输入 token 55.5M→25.6M；PolyBench 相反，1.0→5.4、35.3M→233.2M
```

**替换**

```text
Full System 相对 Sonnet（no-evo）的效率方向随任务流不同：FutureX 工具调用均值 13.4→4.2/题，整条任务流输入 token 合计 55.5M→25.6M；PolyBench 两项分别为 1.0→5.4/题、35.3M→233.2M
```

### D601 环境模型的训练边界、错误率与额外调用需拆开

**1. 原文**

```text
- B5 **环境模型这条路**（WMA、WorldEvolver）需要训练辅助模型或每步多一次预测，预测错误里四成是编造元素 [E1183]；在我们的设定下不作为第一版（我的建议）。位置：方案稿 6.3 节"显式的环境模型不是前提"。类别：已有做法，暂不采用。
```

**替换**

```text
- B5 **环境模型这条路**：WMA 训练辅助世界模型与价值函数；WorldEvolver 冻结模型，通过情节和语义记忆改预测上下文。WMA 抽查的 50 个错误预测中，42% 属于反事实编造，不能外推为全部预测的错误率，也不能套给 WorldEvolver [E1183]。WorldEvolver 的规划环有预测、筛选、可能重选/重预测及记忆更新，并非严格每步只多一次调用；表 13 报告的是组件调用及检索开销，不是端到端时间/费用。第一版暂不采用是研究预算选择，不是“两者都需训练”的判断。位置：方案稿 6.3 节。类别：已有做法，暂不采用。
```

**2. 原文**

```text
预测错误里四成是编造元素；不训练的版本（WorldEvolver）目前只在文字游戏环境上提高了预测精度，下游成功率的提升在置信区间内与基线分不开。
```

**替换**

```text
在抽查的 50 个错误预测中，42% 属于反事实编造（不是全部预测错误率）。不训练的 WorldEvolver 在文字环境上提高预测精度，但规划收益随模型、环境和指标变化；部分 best-of-5 置信区间重叠、ALFWorld 首次成功率下降。单组区间重叠本身不能代替配对差值检验，也不能证明无效或等效。
```

**3. 原文**

```text
规划运行的时间在本节核对过的条目里没有记录 [E1187]。
```

**替换**

```text
规划运行的端到端时间在原稿条目里没有记录 [E1187]。本轮补核表 13：Gemma-4-26B-A4B、无置信度过滤的规划变体，每步世界模型模块调用约 2.054–2.157，其中 LLM 调用约 1.609–1.874；检索每次 10.100–18.335 ms，峰值世界模型提示 2,726–4,324 token。这些是四组组件统计，不能当端到端加速或套给另一过滤变体。[原文 Table 13](https://arxiv.org/pdf/2606.30639v2)。
```

### D602 WALT 的约 14 次是粗略摊销，不是净回本

**1. 原文**

```text
方案稿已有的 ActionEngine 和 WALT 回本次数 [E332] [E333] 不变。
```

**替换**

```text
ActionEngine 的既有回本记录见 [E332]。WALT 作者称约 14 次可摊销，来自造工具 $1.67 除以基线每题 $0.12；未扣除复用后的执行费用，不能作为净回本次数 [E333]。按我们的账本，应另检验 $N(C_{\mathrm{base}}-C_{\mathrm{reuse}})\ge C_{\mathrm{build}}+C_{\mathrm{select}}+C_{\mathrm{maint}}(N)$（本文记账式，N 为复用次数；C_base、C_reuse 为每次执行费用，其余项为截至第 N 次的累计构造、选择及维护费用；不是 WALT 原式）。
```

### D603 文本梯度是反馈与编辑机制，不是数值求导

**1. 原文**

```text
文本梯度这一支。
```

**替换**

```text
这里的“梯度”是自然语言反馈的比喻，不是对离散文本算出的数值导数。TextGrad 把提示、中间输出与评价连成计算图；评价 LLM 指出问题，反向调用结合节点上下文与下游反馈把建议传给上游提示，再由优化器 LLM 写出候选文本。这是语义反馈与候选编辑，不构成真实链式求导或性能单调提高的保证。[TextGrad 原文 §1–2、附录 A](https://arxiv.org/html/2406.07496v1)。
```

**2. 原文**

```text
TextGrad（验证集变好才更新）
```

**替换**

```text
TextGrad 的提示优化实验（§3.3，验证集变好才更新）
```

### D604 每次成功是均摊口径；公式缩写应标明

**1. 原文**

```text
同一个循环，换了目标量和约束的位置。
```

**替换**

```text
同一个循环，换了目标量和约束的位置。 这里采用同一任务分布和统计窗口下的均摊口径：全部尝试的总时间或总费用除以成功数；不自动等于对同一道题不断重试到成功的期望成本。持续学习时要说明是否冻结记忆，构造、选择和维护成本另计或按明确使用量摊销。
```

**2. 原文**

```text
公式照抄论文自己的定义并逐个解释符号
```

**替换**

```text
公式按论文定义重排并逐个解释符号（压缩式不宣称逐字照抄）
```

**3. 原文**

```text
下表照抄各论文自己的定义
```

**替换**

```text
下表按各论文定义重排，部分求和范围或条件有缩写
```

**4. 原文**

```text
公式和符号照抄论文自己的定义
```

**替换**

```text
公式和符号按论文定义重排，部分条件与求和范围有缩写
```

**5. 原文**

```text
公式和符号照抄各文条目
```

**替换**

```text
公式和符号按各文条目重排，压缩式不视为逐字原式
```

**6. 原文**

```text
有公式的照录公式并逐个解释符号
```

**替换**

```text
有公式的按原定义重排并逐个解释符号（有压缩，不保证逐字照录）
```

### D605 项目页分区名称不能代替训练状态判断

**1. 原文**

```text
77 条改模型参数，176 条改执行框架
```

**替换**

```text
77 条位于项目页 Foundation Model 目录，176 条位于执行框架目录
```

**2. 原文**

```text
改模型参数的 77 条只读摘要（用户要求）
```

**替换**

```text
项目页 Foundation Model 目录的 77 条按摘要筛选（目录归类不等于每篇都训练参数）
```

**3. 原文**

```text
改模型参数的 77 条（用户要求只读摘要；
```

**替换**

```text
项目页 Foundation Model 目录的 77 条（按摘要筛选，WorldEvolver 等需逐篇修正训练边界；
```

**4. 原文**

```text
### C.1 改模型参数的 77 条
```

**替换**

```text
### C.1 项目页 Foundation Model 目录的 77 条（不代表全部训练）
```

### D606 跨论文不能排出“最稳定”和“最不可靠”

**1. 原文**

```text
把重复流程做成可调用的代码或已存的动作序列，是同时降步数和 token 最稳定的做法
```

**替换**

```text
把重复流程做成可调用代码或已存动作序列，是值得优先测试的一类加速方法；当前跨论文结果不能建立“最稳定”的排名
```

**2. 原文**

```text
"判断对错"仍是最不可靠的一环（我的判断）
```

**替换**

```text
"判断对错"是已有实测暴露的重要瓶颈（当前没有统一对照证明它是最不可靠的一环）
```

**3. 原文**

```text
4. 改进过程的开销（7.2）跨度从几美元到两万美元，主要花在评估候选；这决定了方案稿里验收重跑的规模是预算的主项。
```

**替换**

```text
4. 改进过程的开销（7.2）跨度从几美元到两万美元。RQGM 与 JudgeFlow 的已报告拆分中，候选评估占比较大；不能外推到全部方法。我们的验收重跑是否为预算主项，应先剖析小规模实验。
```

**4. 原文**

```text
**改进过程的开销主要花在评估候选上**
```

**替换**

```text
**已报告成本拆分的部分方法中，候选评估占比较大**
```

**5. 原文**

```text
所以方案稿的验收设计决定预算的主项
```

**替换**

```text
因此方案稿应单独计候选评估预算，并测量它在我们设置中的占比
```

**6. 原文**

```text
单任务粒度早停、分阶段评估
```

**替换**

```text
单任务粒度自适应分配评估预算、分阶段评估
```

**7. 原文**

```text
加入"改进开销主要在评估候选"的文献依据
```

**替换**

```text
加入“部分方法的候选评估占比较大”的文献依据，避免预设我们的预算主项
```

### D607 工具化对非模型时间的作用取决于实现

**1. 原文**

```text
I 步数；II 每步调用数（不经模型时为零）；IV 非模型时间不变或上升
```

**替换**

```text
I/II：可能减少模型参与的决策或调用；IV：若原子操作不变，主要省模型开销；若同时省掉重复观察、导航或处理，非模型时间也可能下降。构造、验证和恢复另计
```

### D608 反复使用真值的选择集不是独立最终测试

**1. 原文**

```text
代理测试的可靠度要单独测 [E986, E953, E962, E682]。
```

**替换**

```text
代理测试的可靠度要单独测 [E986, E953, E962, E682]。 CoEvoSkills 的真值结果参与后续迭代与最佳版本选择，因此这些调用属于开发/选择反馈；“少量真值”不等于独立最终测试。若用于我们的持续改进，需要另外保留没有参与候选选择的最终测试任务，并计入真值调用预算。
```

### D609 SICA 数值可保留，准确率分母未说明

**1. 原文**

```text
50 题 SWE-bench 子集 17%→53%，但 53% 是第 14 轮，第 13 轮跌到 27%，打分与挑选用同一批题 [E1102]。
```

**替换**

```text
作者称固定抽取 50 题 SWE-bench 子集；表 1 第 0、14、15 轮的准确率为 17%、53%、51%，最高表值不是最终轮。它们不是 50 题二值通过率应有的 2 点整数倍，原文未解释归一化或重复统计分母，不能反推解出题数；打分与选择使用同一批题 [E1102]。
```

**2. 原文**

```text
——费用 −11%、时间 −12%、token +25% [E1099, E1100]
```

**替换**

```text
——费用约 −11%、时间约 −12%、token +25%（calc.，按四舍五入表值计算）[E1099, E1100]
```

### D610 GenericAgent 的首末改善不是代码化单独贡献

**1. 原文**

```text
同一任务族九轮：运行时间 7m30s→1m38s，LLM 调用 32→5，总 token 222,203→23,010（单条序列，缓存读取全额计入）
```

**替换**

```text
同一任务族九轮：运行时间 7m30s→1m38s，LLM 调用 32→5，总 token 222,203→23,010（单条序列，每轮新任务实例，缓存读取 token 按原数全额相加；首末差不是隔离代码化的因果实验，也不是美元同比降幅）
```

### D611 训练选项的用户归因尚未核实

**1. 原文**

```text
### 8.4 训练模型这个选项（用户要求：有理由、并且小规模可行才考虑）
```

**替换**

```text
### 8.4 训练模型的扩展选项（原稿建议；本次范围仍以免训练为主）
```

**2. 原文**

```text
用户要求：这一半只读摘要；训练模型只有在有理由、并且小规模实验上可行时才作为选项。
```

**替换**

```text
原稿对这一目录采用摘要级筛选，并建议把有理由且小规模可行的辅助训练留作后续选项。本轮可见请求强调训练以外的工作；“允许辅助训练”的用户归因尚未核实，不把原稿的扩展建议当作已确认要求。
```

**3. 原文**

```text
不满足 Edwin"有理由、并且小规模可行"的条件
```

**替换**

```text
不满足原稿提出的“有理由、并且小规模可行”的条件（该条件是否为用户原话，本轮未核实）
```

## 4. 仍待处理与完整参考文献

- 82 是原稿最终合格、非综述书目条数；87 次深读/复用流水账的独立论文数还需按统一标识去重。s057 等已读未引用工作不等于正文漏引，需完善索引，不能由现有数字认证全覆盖。
- 421 候选中 336 行摘要细目、85 条深读主条目移至其他记录；5 条“略过/摘要”状态口径不一致。55 条核读标签和 8 条发表说明有截断，版本 URL 完整不等于原审计语境完整。
- 未核实另一会话是否曾授权辅助模型训练；本轮按用户当前可见请求，以免训练工作为主，不将原稿建议升级为用户要求。
- HGM 的异步独立贡献、SICA 准确率分母、Continual Harness 既有统计冲突，不能从这次阅读中补算出来。
- 泛化、漂移、全生命周期净收益仍需实验。没有给代码技能、文字记忆或验证器可靠性作跨基准排行榜。
- 没有变更 Claude 的方案稿或 canonical dossier；研究建议仍需与既有协议做受控比较。原稿某些引用资格与训练选项的待决项保留为作者观点，不影响本次阅读版完成。

**本轮实际回查的原文（完整署名、版本与定位）。** 下列发表身份注明“沿用账本”时，本轮没有重新核验会议官方目录。HTML 原稿的 88 条书目保持完整，另附此补核书目，不把目录记录数误称为全部重新精读篇数。

1. Zhe Ren; Yimeng Chen; Dandan Guo; Guowei Rong; Tonghui Li; R. B. Xiong; Qingfeng Lan; Wenyi Wang; Li Nanbo; Yibo Yang; Mingchen Zhuge; Jürgen Schmidhuber. *Self-Improvements in Modern Agentic Systems: A Survey*. arXiv:2607.13104v1, 2026. [原文](https://arxiv.org/html/2607.13104v1)。核 §3–4；本地 `.../part3-verification/survey2607/sources/2607.13104v1.html/.txt`。

2. Ruhana Azam; Aditya Vempaty; Ashish Jagmohan. *Reflection-Based Memory For Web navigation Agents*. arXiv:2506.02158v1, 2025. [PDF](https://arxiv.org/pdf/2506.02158v1)。核 §3–5、Algorithm 1、表 1–2；实际读取官方 PDF 文字层及官方 HTML 缓存；网页截图接口返回 cache miss，未声称完成该 PDF 的图像核对。

3. Mert Yuksekgonul; Federico Bianchi; Joseph Boen; Sheng Liu; Zhi Huang; Carlos Guestrin; James Zou. *TextGrad: Automatic “Differentiation” via Text*. arXiv:2406.07496v1, 2024. [核查版本](https://arxiv.org/html/2406.07496v1)。正式期刊版另题为 *Optimizing generative AI by backpropagating language model feedback*, Mert Yuksekgonul; Federico Bianchi; Joseph Boen; Sheng Liu; Pan Lu; Zhi Huang; Carlos Guestrin; James Zou, *Nature* 639, 609–616 (2025), [DOI](https://doi.org/10.1038/s41586-025-08661-4)。本次机制和门规则以 v1 §1–3.3/附录 A 核，不把正式版新增作者套在 v1 上。

4. Yongchao Chen; Jacob Arkin; Yilun Hao; Yang Zhang; Nicholas Roy; Chuchu Fan. *PRompt Optimization in Multi-Step Tasks (PROMST): Integrating Human Feedback and Heuristic-based Sampling*. EMNLP 2024, pp. 3859–3920. [正式论文](https://aclanthology.org/2024.emnlp-main.226/)。核查 [arXiv:2402.08702v4](https://arxiv.org/html/2402.08702v4)，§3–4。

5. Huichi Zhou; Yihang Chen; Siyuan Guo; Xue Yan; Kin Hei Lee; Zihan Wang; Ka Yiu Lee; Guchun Zhang; Kun Shao; Linyi Yang; Jun Wang. *Memento: Fine-tuning LLM Agents without Fine-tuning LLMs*. arXiv:2508.16153v2, 2025. [原文](https://arxiv.org/html/2508.16153v2)，§4.2、§5.3。

6. Shengtao Zhang; Jiaqian Wang; Ruiwen Zhou; Junwei Liao; Yuchen Feng; Zhuo Li; Yujie Zheng; Weinan Zhang; Ying Wen; Zhiyu Li; Feiyu Xiong; Yutao Qi; Bo Tang; Muning Wen. *MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory*. arXiv:2601.03192v2, 2026. [原文](https://arxiv.org/pdf/2601.03192v2)。核 §3–4、附录 F；本地 `/private/tmp/memory-papers/2601.03192.pdf`。

7. Junwei Liao; Haoting Shi; Ruiwen Zhou; Jiaqian Wang; Shengtao Zhang; Wei Zhang; Ying Wen; Zhiyu Li; Feiyu Xiong; Bo Tang; Weinan Zhang; Muning Wen. *MemQ: Integrating Q-Learning into Self-Evolving Memory Agents over Provenance DAGs*. arXiv:2605.08374v3, 2026. [原文](https://arxiv.org/html/2605.08374v3)，§3–5.2、表 1。

8. Zora Zhiruo Wang; Jiayuan Mao; Daniel Fried; Graham Neubig. *Agent Workflow Memory*. ICML 2025, PMLR 267:63897–63911. [正式论文](https://proceedings.mlr.press/v267/wang25bx.html)。实际核正式 PDF 附录 D/F、表 11/13；本地 `/private/tmp/memory-papers/awm-icml2025.pdf`。

9. Siru Ouyang; Jun Yan; I-Hung Hsu; Yanfei Chen; Ke Jiang; Zifeng Wang; Rujun Han; Long T. Le; Samira Daruki; Xiangru Tang; Vishy Tirumalashetty; George Lee; Mahsan Rofouei; Hangfei Lin; Jiawei Han; Chen-Yu Lee; Tomas Pfister. *ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory*. ICLR 2026. 核查 [arXiv:2509.25140v2](https://arxiv.org/pdf/2509.25140v2)，附录 C.2/表 5；本地 `/private/tmp/memory-papers/2509.25140.pdf`。

10. Mirac Suzgun; Mert Yuksekgonul; Federico Bianchi; Dan Jurafsky; James Zou. *Dynamic Cheatsheet: Test-Time Learning with Adaptive Memory*. EACL 2026, pp. 7080–7106. [正式论文](https://aclanthology.org/2026.eacl-long.333/)。实际核 [arXiv:2504.07952v1](https://arxiv.org/pdf/2504.07952v1)，§4.1、§5/脚注 13；本地 `/private/tmp/memory-papers/2504.07952.pdf`。

11. Igor Bogdanov; Chung-Horng Lung; Thomas Kunz; Jie Gao; Adrian Taylor; Marzia Zaman. *FORGE: Self-Evolving Agent Memory With No Weight Updates via Population Broadcast*. ACM CAIS 2026, pp. 292–310, [DOI](https://doi.org/10.1145/3786335.3813155)。实际核 [arXiv:2605.16233v1](https://arxiv.org/html/2605.16233v1)，§3–4/表 2。

12. Wenyi Wang, Piotr Piękos, Li Nanbo, Firas Laakom, Yimeng Chen, Mateusz Ostaszewski, Mingchen Zhuge, and Jürgen Schmidhuber. **Huxley-Gödel Machine: Human-Level Coding Agent Development by an Approximation of the Optimal Self-Improving Machine.** ICLR 2026（正式身份沿用已核账本；本轮不重验 Oral）。实读 arXiv:2510.21614v3，2025-10-29。[PDF](https://arxiv.org/pdf/2510.21614v3)。原文机构：KAUST。重点复核 pp.4–10、p.18。

13. Seth Karten, Joel Zhang, Tersoo Upaa Jr., Ruirong Feng, Wenzhe Li, Chengshuai Shi, Chi Jin, and Kiran Vodrahalli. **Continual Harness: Online Adaptation for Self-Improving Foundation Agents.** 2026，预印本。实读 arXiv:2605.09998v1，2026-05-11。[PDF](https://arxiv.org/pdf/2605.09998v1)。原文机构：Princeton University、ARISE Foundation、Google DeepMind；按强机构预印本纳入。重点复核 pp.3–8、23、25–28。

14. Zewen Liu, Zhan Shi, Yisi Sang, Bing He, Minhua Lin, Tianxin Wei, Dakuo Wang, Benoit Dumoulin, Wei Jin, and Hanqing Lu. **Adaptive Auto-Harness: Sustained Self-Improvement for Agentic System Deployment on Open-Ended Task Streams.** 2026，预印本。实读 arXiv:2606.01770v2，2026-06-03。[PDF](https://arxiv.org/pdf/2606.01770v2)。原文机构：Emory University、Amazon、Pennsylvania State University、UIUC、Northeastern University；按高校研究预印本纳入，不凭普通公司博客资格。重点复核方法定义、p.13 Table 5、p.19 Table 14。

15. Maxime Robeyns, Martin Szummer, and Laurence Aitchison. **A Self-Improving Coding Agent.** 2025。ICLR 2025 Workshop “Self-Improving Foundation Models Without Human Supervision”（workshop 身份沿用账本，非 ICLR 主会）；按 University of Bristol 机构资格纳入。实读 arXiv:2504.15228v2，2025-05-16。[PDF](https://arxiv.org/pdf/2504.15228v2)。重点复核 pp.3–7，尤其 Eq.1–2、Table 1。

16. Advantage AI Agent Lab (A3 Lab). **GenericAgent: A Token-Efficient Self-Evolving LLM Agent via Contextual Information Density Maximization (V1.0).** 2026，预印本。首页以团队署名；§8 列贡献者：Jiaqing Liang, Jinyi Han, Weijia Li, Xinyi Wang, Zhoujia Zhang, Zishang Jiang, Ying Liao, Tingyun Li, Ying Huang, Hao Shen, Hanyu Wu, Fang Guo, Keyi Wang, Zhonghua Hong, Zhiyu Lu, Lipeng Ma, Sihang Jiang, Yanghua Xiao。实读 arXiv:2604.17091v1，2026-04-18。[PDF](https://arxiv.org/pdf/2604.17091v1)。§8 明示两位项目负责人为 Fudan University 教师，按高校研究补充资格纳入；不把团队公司背景单独当资格。重点复核 pp.20–23、p.31 作者贡献。

17. Zijie Dai, Siuhin He, Hui Li, Qihui Zhou, Jiajun Li, Mingcong Song, Guoping Long, Hongjie Si, Xin Yao, Lin Zhang, James Cheng, and Xiao Yan. **Metis: Bridging Text and Code Memory for Self-Evolving Agents.** 2026，预印本（首页标 Work in progress）。实读 arXiv:2606.24151v1，2026-06-23。[PDF](https://arxiv.org/pdf/2606.24151v1)。原文机构：The Chinese University of Hong Kong、Huawei、Wuhan University；按高校研究预印本纳入。重点复核 pp.6–12，Table 1–4。

18. Jenny Zhang, Shengran Hu, Cong Lu, Robert Lange, and Jeff Clune. **Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents.** ICLR 2026（会议身份沿用已核账本；本轮 PDF 首页亦标会议论文，但未重新查官方日程）。实读 arXiv:2505.22954v3，2026-03-12。[PDF](https://arxiv.org/pdf/2505.22954v3)。机构：University of British Columbia、Vector Institute、Sakana AI、Canada CIFAR AI Chair。重点复核 pp.4–6、10、32。

19. Alex Iacob, Andrej Jovanović, William F. Shen, Daniel Burkhardt, Meghdad Kurmanji, Nurbek Tastan, Lorenzo Sani, Niccolò Alberto Elia Venanzi, Ambroise Odonnat, Zeyu Cao, Bill Marino, Xinchi Qiu, and Nicholas D. Lane. **The Red Queen Gödel Machine: Co-Evolving Agents and Their Evaluators.** 2026，预印本（作者称初步实证）。实读 arXiv:2606.26294v2，2026-06-29。[PDF](https://arxiv.org/pdf/2606.26294v2)。机构：University of Cambridge、NVIDIA、Flower Labs、MBZUAI、Inria；按强高校/研究机构预印本纳入。重点复核 pp.7、12、22、25。

20. Boyuan Zheng, Michael Y. Fatemi, Xiaolong Jin, Zora Zhiruo Wang, Apurva Gandhi, Yueqi Song, Yu Gu, Jayanth Srinivasa, Gaowen Liu, Graham Neubig, and Yu Su. **SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills.** 2025，本文按实读预印本引用，不重验后续 venue。实读 arXiv:2504.07079v1，2025-04-09。[PDF](https://arxiv.org/pdf/2504.07079v1)。机构：The Ohio State University、University of Virginia、Purdue University、Carnegie Mellon University、Cisco Research；高校研究资格。重点复核 pp.4–6、34。

21. Zixi Huang, Xiheng Wang, Andrew Wang, William Jurayj, Bernal Jiménez Gutiérrez, Daniel Khashabi, and Nicholas Andrews. **Better, Faster, Stronger: Programmatic Skill Learning Best Reduces Agent Cost.** 2026，预印本（方法名 SpeedRunner）。实读 arXiv:2608.11338v1，2026-08-11。[PDF](https://arxiv.org/pdf/2608.11338v1)。机构：Johns Hopkins University。重点复核 pp.2–6、10、14。

22. Haoran Xu, Jiacong Hu, Ke Zhang, Lei Yu, Yuxin Tang, Xinyuan Song, Yiqun Duan, Lynn Ai, and Bill Shi. 2025. *SEDM: Scalable Self-Evolving Distributed Memory for Agents*. arXiv:2509.09498, v3（2025-09-26）。实际读取 v3 PDF；既有记录标注 SEA@NeurIPS 2025 workshop，本轮未另核会议页面，不当作 NeurIPS 主会。作者单位包含 Gradient、Zhejiang University、University of Toronto、Rice University 等。[原文](https://arxiv.org/pdf/2509.09498v3)。

23. Xuan Zhang, Wenxuan Zhang, See-Kiong Ng, and Yang Deng. 2026. *Self-Evolving World Models for LLM Agent Planning*. arXiv:2606.30639, v2。National University of Singapore / Singapore University of Technology and Design / Singapore Management University。实际读取 v2 PDF；Findings of EMNLP 2026 是被审报告记录的作者声明，本轮未核实正式 proceedings，按预印本引用。[原文](https://arxiv.org/pdf/2606.30639v2)。

24. Hyungjoo Chae, Namyoung Kim, Kai Tzu-iunn Ong, Minju Gwak, Gwanwoo Song, Jihoon Kim, Sunghwan Kim, Dongha Lee, and Jinyoung Yeo. 2025. *Web Agents with World Models: Learning and Leveraging Environment Dynamics in Web Navigation*. International Conference on Learning Representations (ICLR 2025)。Yonsei University。实际读取 arXiv:2410.13232v2 PDF，首页标注 ICLR 2025。[原文](https://arxiv.org/pdf/2410.13232v2)。

25. Viraj Prabhu, Yutong Dai, Matthew Fernandez, Krithika Ramakrishnan, Jing Gu, Yanqi Luo, Silvio Savarese, Caiming Xiong, Junnan Li, Zeyuan Chen, and Ran Xu. 2026. *WALT: Web Agents that Learn Tools*. International Conference on Learning Representations (ICLR 2026)。实际读取正式会议 camera-ready；不是旧 arXiv 2510.01524v1。[正式 PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/5b175f9e93873e3a10a6ce43dbb82e05-Paper-Conference.pdf)。

26. Hanrong Zhang, Shicheng Fan, Henry Peng Zou, Yankai Chen, Zhenting Wang, Jiayu Zhou, Chengze Li, Wei-Chieh Huang, Yifei Yao, Kening Zheng, Xue (Steve) Liu, Xiaoxiao Li, and Philip S. Yu. 2026. *CoEvoSkills: Self-Evolving Agent Skills via Co-Evolutionary Verification*. arXiv:2604.01687, v3。实际读取 v3 PDF，页眉标注 COLM 2026；本轮未另核正式会议记录。[原文](https://arxiv.org/pdf/2604.01687v3)。
