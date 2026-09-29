# 第三部分研究计划报告支持记录

2026-09-29。对应读者报告：`notes/2026-09-29-part3-research-plan-report-zh.md` / `.docx`。本轮把已有调查综合成可讨论的研究计划，补读三篇最近邻，并按用户新增要求，在计划形成后回看当前 PPT 的公式与文献位置。Word 经 bundled LibreOffice 渲染为 17 页并逐页检查，中文字体、两条可编辑公式、五张表和引用链接已核对；文献引用共 23 条且与正文编号一致。未运行方法复现，未批准方案或预算，未修改前两部分 slides 或 canonical dossier。

## 1 Verification table

| ID | 待核判断 | 一级来源与定位 | 结论 |
|---|---|---|---|
| V1 | 诊断与修改路由是待补的全领域空白 | HarnessFix v2 §III-C “maps each flaw record to applicable repair operators”；§IV-B “training, validation, and held-out test sets”；§V-A “offline evolving/repair tokens”。[原文](https://arxiv.org/html/2606.06324v2) | 否。已有从失败轨迹定位代码、跨任务合并、修复算子路由与验证的近邻。报告将其作为强参照，不将新增分类直接称为贡献；其 token 指标不能当部署推理节省。 |
| V2 | 企业环境知识形成确定性工具是未覆盖方向 | StarHarness v1 §3.1 “mean task score”；§5–5.1 环境惯例、schema、表格、日期与财务计算工具。[原文](https://arxiv.org/html/2608.24804v1) | 已有直接重叠。显式条件表示相对直接生成补丁的增量才是候选问题；任务分数目标与部署 API 费用分别描述。 |
| V3 | 多轮演化累计指标可直接当经济净收益 | DarwinX v1 §2.1 “cumulative lineage gain”；§3、§6、§8–9、App. B/E。[原文](https://arxiv.org/html/2608.07545v1) | 不成立，指标为解题率改善。按各实验区别同集演化与留出，不把所有结果都写成同一种泛化；本报告不引用其 headline 数字。 |
| V4 | 计划没有攻击公式中的一个项 因而与前文脱节 | 当前 `slides/build_deck.py` 的 EQ/FX、s02–s04、A0，以及下表真实页面；D157–D160、D161–D288 的既有边界 | 计划首先改变 m；被采纳的执行改动才影响 ΣJ、tokens、无效 N、ΣE、R。属于交叉组织轴，不能用外层学习排除 WALT/SpeedRunner 等直接近邻。 |
| V5 | 一个大动作同时等比例减少 N J 和底层环境操作 | 当前 s02 定义 N 为 observe–decide–act–wait，J 为轮内所有模型调用 | 不成立。粒度变化可能是同一收益的不同描述；必须分别保存外层轮次、全部模型调用、底层动作与时间区间。非模型检查归 E，模型 helper/fallback 归 D 和费用。 |
| V6 | 单次执行费用足以评价持续学习 | 当前 B8 已有固定 setup 摊销；i=0 是本次 attempt 内的前置调用 | 不足。生命周期需计入后续学习、验证、探索与维护；部署、学习维护、研究测评三账本分开。新账本定义是研究建议，不是新的实证结果。 |

### 当前 PPT 的交叉定位

| 当前来源 | 实际包含内容 | 报告采用边界 |
|---|---|---|
| `slides/build_deck.py:136`、`:450`、`:490`、`:909` | 时间、费用、符号、重试条件 | 公式为既有分析改编与补充，非一篇文献原式；固定版本 C/R 与变化中的实际任务流区分。 |
| `t03` Calls per step；`t04` Number of steps | AutoDroid-V2、MobileGPT；WALT | 主线已有学习与复用，不说此前只研究执行而无人研究学习。 |
| `b1-1` Compile or replay | ActionEngine、AppAgentX 等 | ActionEngine 当前行主体仍有 v1 混模型结果，附 v2 setup 提示；报告的机制比较按已核 v2，不拼接数字。 |
| `b2-1` Fewer steps；`b0-3`、`b8-1` | AWM、SpeedRunner；费用来源与摊销 | AWM 为文字工作流；SpeedRunner 已含技能归纳及摊销，不能把曲线作为新颖性依据。 |
| `research/2026-09-28-part2-acceleration-by-term.md` D167 | SkillWeaver 前期核查 | 当前生成器没有 SkillWeaver 条目，区分前期查过与 PPT 展示。旧研究文档的 t14/部分条目位置已变化，以当前生成器为准。 |

## 2 D-ledger additions

**D319 — 补读三个直接近邻并约束贡献主张。** 在 D318 的来源资格筛查后，本轮实际核读 HarnessFix v2、StarHarness v1、DarwinX v1 的方法与相关实验。诊断路由、可执行框架修改、环境惯例工具化和多轮筛选均已有近邻；报告将成本热点与复用优先级、显式条件层和净收益作为待检验问题，不把组合自动等同创新。HarnessFix 的离线修复 token、StarHarness 的任务分数目标、DarwinX 的累计解题率改变量分别保留口径。代码仅查看部分 README/目录，未复现。

**D320 — 区分执行分解与学习设计并核对现有 PPT 覆盖。** 研究计划先独立展开，再由公式审查执行变化：改变 m 后才可能影响 N/J/tokens/E/R，模型单价、TPOT、并发抵扣不自动改善。宏动作可能只移除中间模型决策，不能同时计两次收益；学习验证开销需要独立生命周期账本。现有 Part 2 已含多篇近邻，但分散在机制页和附录，不能用此叙事差异建立领域空白。计划尚无实验结果，也未决定预算。

## 3 E-ledger patches

不新增性能数字，不改 canonical 的 E 条目。报告沿用 E304–E308、E314–E317、E271–E272、E230、E321、E323 等已有证据和 D313–D318 的来源/范围校正。新增三个近邻继续使用跨会话映射 w003、n006、w080，不把外部编号擅自转成 E 编号。本文不将外部草稿记载的团队背景、作者方法建议和论文结论混为同一来源；规则派生用例在读者报告中明确记为跨会话候选建议，相关冲突继续见 `2026-09-29-part3-claude-draft-crosscheck.md`。

## 4 Still open

- 选定工作流、日志、可重置环境与可靠的业务判据；训练外层优化器并未被排除。
- 在共同修改权限与资源下选择可复现的近邻；组件对照不冒充完整论文复现。
- 根据实际想声称的贡献增加对照：专门诊断、成本优先级、环境条件层、持续维护不能靠一个整体比较分别归因。
- 正式样本量、质量容差、优化限额与预算须待试跑和方案选择；不从本报告推导已证实的收益。

## References

本记录新增方法核查的完整引用如下。其余已核来源、正式 venue 与实际版本见读者报告文末 23 条完整引用，以及 `2026-09-29-part3-source-filter.md`、`2026-09-29-part3-claude-draft-crosscheck.md`。来源均为一级论文；资格不代替结果验证。

Mengzhuo Chen; Junjie Wang; Zhe Liu; Yawen Wang; Haiming Zheng; Qing Wang (2026). *From Failed Trajectories to Reliable LLM Agents: Diagnosing and Repairing Harness Flaws*. arXiv 预印本，正式发表未独立确认。实际核读：[固定版本](https://arxiv.org/html/2606.06324v2)。机构：State Key Laboratory of Complex System Modeling and Simulation Technology, Beijing, China; Institute of Software, Chinese Academy of Sciences, Beijing, China; University of Chinese Academy of Sciences, Beijing, China; School of Computer Science and Technology, Tianjin University, Tianjin, China。

Esakkivel Esakkiraja; Denis Akhiyarov; Vikas Yadav; Sai Rajeswar; Patrice Bechard; Sridhar Nemala; Sagar Davasam (2026). *StarHarness: Evolving Harnesses with Stratified Search for Enterprise Environments*. arXiv 预印本，正式发表未独立确认。实际核读：[固定版本](https://arxiv.org/pdf/2608.24804v1)。机构：ServiceNow; Mila; Université de Montréal。

Yifan Zhang; Yutong Dai; Juntao Tan; Luyu Yang; Rishi Mullur; Thai Hoang; Zhiyuan Hu; James Zhu; Phil Mui; Silvio Savarese; Ran Xu; Zeyuan Chen (2026). *DarwinX: Evolving Agent Harnesses Through Natural Selection*. arXiv 预印本，正式发表未独立确认。实际核读：[固定版本](https://arxiv.org/pdf/2608.07545v1)。机构：Salesforce AI Research; Salesforce Agentforce。

