# 无权重更新的提示与环境知识改进 原文核查

核查日期：2026-09-30。供主报告使用的证据笔记。网页集合是发现入口；以下结论来自所列原论文的方法、实验及相关附录。数字不跨模型、数据集、阶段拼接。未运行论文代码。`深读`表示方法、实验设计、结果、相关附录和局限实读，不表示逐字读完所有参考文献与提示模板。

## 1 证据与核查表

| 工作与原文 | 修改对象及方法 | 可核实效果与边界 | 阅读定位 |
|---|---|---|---|
| [ACE](https://arxiv.org/pdf/2510.04618v3)，ICLR 2026 | 固定模型，Generator 执行，Reflector 从轨迹提炼条目，Curator 生成增量更新；条目有 ID 和有用/有害计数，确定性合并而非全文重写 | Table 4 的 AppWorld 53,898→9,517 秒是离线适配，相对 GEPA；附录另一设置的部署评估输入 token 26,960,675→58,623,267，输出 251,442→270,652，rollout 2,470→2,354。因此不能把适配加速宣称为运行省 token。缓存研究的账单下降是有缓存相对无缓存，不是 ACE 相对其他方法 | §§3–4，Table 4 p10；App A.3 pp18–19，Tables 12–15。Table 4、14 已视觉核对 |
| [GEPA](https://arxiv.org/pdf/2507.19457v2)，ICLR 2026 Oral | 读取完整轨迹和环境反馈，反思模块提示；小批筛选后验证，保留按任务表现互补的候选，可合并；此处 Pareto 不是时间金钱 Pareto | Qwen3-8B IFBench 的最优检查点用 678 rollout，不等于整轮搜索只花 678（该设置总预算 3,593）。Fig18 的最高 9.2 倍是 PUPA 上 Qwen3-8B 的提示长度压缩，相对 MIPROv2；不是整任务时间。大量预算用于验证 | §§2–3 pp4–5，Tables1–2 p8，Obs4 p11，AppE.3 p25，Fig18 p31（视觉核对） |
| [SkillOpt](https://arxiv.org/pdf/2605.23904v2)，Microsoft 等预印本 | 优化自然语言 skill 文档；成功失败轨迹驱动受限增删改，独立 selection set 严格择优，拒绝编辑缓存和慢速 meta 指导；不是自动编译执行宏 | Table6：Spreadsheet 224→1,995 prompt tokens，优化开销 21.4M tokens；SearchQA 16→857，213.8M。部署不多一个 optimizer 调用不等于没有新增推理成本。§4.5 某电子表格策略按 grader 读数行为输出静态值，提醒核验真实任务语义与测试语义是否一致 | §§3–4；Table6 p14（视觉核对）；§4.5 p16。未使用存在口径疑问的 cost/point 指标 |
| [Trace](https://arxiv.org/pdf/2406.16218v2)，NeurIPS 2024 | OPTO 将反馈、执行图、可改变量交给 OptoPrime；变量可为提示或代码，非可微算子也可优化 | Table2 的分钟数包含优化、验证、测试，不是最终 Agent 单次服务时间。限制包括 DAG 表示、状态内原地修改、较大图的上下文开销；当时实现不支持分布式并行图 | §2，Table2 p10，§6 limitations；首页正式会议页眉确认 |
| [GLoW](https://arxiv.org/pdf/2509.24116v2)，SNU 预印本版本 | 全局选择潜力状态，通过动作 replay 返回；同一起点多个局部轨迹形成文字优势，改进后续探索；固定 LLM | Table1：10 个 Jericho 游戏，LLM 方法每个 1,000 interactions、3 runs；GPT-4.1-mini 的 Zork1 在预算内最高游戏分数均值73.0 vs ICRL51.7。100–800 倍指相对部分 RL 方法的交互预算差；非延迟/费用。AppC.1 每1,000步 API $4–6，LLM 方法间费用差很小。全部基线可用 valid-action 接口 | §§3–4，Table1 p7（视觉核对），AppC.1 p16。检查使用的是 arXiv v2，未把后续会议信息当作版本替代 |
| [WorldEvolver](https://arxiv.org/pdf/2606.30639v2)，NUS/SUTD/SMU 预印本 | 执行转移 episodic memory，预测与实测差异提炼带证据分的语义规则；低置信预测不送给 actor；actor 和 world-model 权重都固定 | Table2：Gemma ReAct ScienceWorld 44.44→52.22%；但 GPT-5.4-mini 65.56→63.33%。指标是每题 5 次 trial 的 best-of-5，不是单次成功率。跨任务记忆消融只损失0.5–1.1pp（Table4，Gemma、无置信门禁）；不可把整体收益归因跨任务积累。App Table13另报调用与上下文开销，仍无端到端省钱证据；算法每步增加预测和再决策，动作改变可能再预测 | §3 Algorithm1 pp4–6；§4.1 p6；Table2 p7（视觉核对）；limitations p10 |
| [FORGE](https://arxiv.org/pdf/2605.16233v1)，Carleton 等，首页 ACM CAIS 2026 | 失败轨迹生成规则或示例，多实例分阶段探索，把冠军记忆广播给其余实例；达到阈值冻结以节省适配 | §5.1/Fig4：Gemini Rules 106M vs Examples 约177M total tokens，含 learning+eval，不能说相对不学习基线便宜40%。冻结会提前终止有益学习，取消冻结对某些模型更好。Fig4 Mixed 标168.8M而正文写约188M，本报告不采用该数字 | §§3–5 pp3–8，Fig4 p7（视觉核对），§7 p9。单一 CAGE-2 B_line、30步设置，跨环境未验证 |
| [VASO](https://arxiv.org/pdf/2606.05395v1)，UT Austin/Iowa State 预印本 | 两级形式验证：先检查规则可满足，再将计划转状态机；model checker 反例变文字反馈，修改 skill 契约，权重固定，global specifications 保持固定 | Table1：手工 proposition mapping SS97.2/TC85.3，自动 mapping SS96.8/TC86.5。正文又有96.6表述，以表为准。不能把97.2说成端到端正确率或自动mapping值；Safety 是满足规范的比例。Fig6 training time 属于技能适配不是机器人执行速度 | §§3–5 pp4–8，Table1/Fig6 p8（视觉核对），§7 limitations：映射未经验证、只顺序技能；形式保证依赖映射正确 |
| [Meta-TTL](https://arxiv.org/pdf/2604.00830v4)，NUS 预印本 | 外循环反思并优化指导改进的 meta-prompt；内循环每次 episode 后改 actor prompt。两个层次均可纯文本、固定权重；不是看到 meta-training 就排除 | Table6 每个含6个episode的Jericho TTL session，3 runs平均：Static593.2秒/196K tokens；Meta-TTL860.9秒/364K；调用231→204。比 TextGrad1205.5秒更快，但比静态 agent 更慢。离线 meta-search 每benchmark $30–70。质量指标 W-AUC 加权后期表现，不等于省时间 | §§3–4 pp3–9，Table6 p9；最新v4标题已从集合中的 Learning to Learn-at-Test-Time 改名，2026-09-28 |

补充边界核查：集合 foundation-model 类的 [Adaptive Self-improvement for ML Library Development](https://arxiv.org/html/2502.02534) 实际用成功示例选择和 test-time compute 扩张，不可单凭分类排除。相反 [EVE-Agent](https://arxiv.org/html/2605.22905) §4.1 明确双policy梯度更新；[Socratic-SWE](https://arxiv.org/html/2606.07412) §§11–13 明确 GRPO/GDPO 和 AdamW；二者不属于本次严格无权重核心。

## 2 D ledger additions

本文件先使用描述性键，主研究审计统一分配 D 编号，避免多 agent 并行冲突。

- ACE_STAGE：82.3%是适配阶段时间减少；独立部署 token 表反而增加。表4和附录12不是同一设置。
- SKILL_ARTIFACT：SkillOpt 的 skill 是自然语言，不能与 SpeedRunner 的可执行代码技能合并理解。
- META_TTL_VERSION：集合旧标题对应 v4 的 Meta-TTL；无权重 meta-search 不等于神经网络 meta-training。
- VASO_MAPPING：97.2为手工映射安全分；自动96.8；映射未验证时保证有条件。
- FORGE_COUNTER：Rules相对Examples的40%不是相对静态Agent，Mixed正文/图冲突未采用。
- WORLD_MODEL_CATEGORY：有非参数 world model，按集合 fm 标签整体排除会漏文献。

## 3 E ledger patches

不直接改写 canonical E ledger。以上是本轮补充验证，主报告明确计算阶段和统计口径。

## 4 Still open

- 多数方法未给完整失败尝试、环境费用、探索与维护的统一成本；不由未报告推断为零。
- GLoW 后续会议版未在本轮替换所读 arXiv v2，避免混版。
- FORGE Mixed token 图文冲突、SkillOpt cost/point 分母问题没有作者澄清，数字不用于结论。
- 本轮未复现实验，也没有获得用户实际任务流数据；后续方案是待验证研究假设。

## References

1. Qizheng Zhang, Changran Hu, Shubhangi Upasani, Boyuan Ma, Fenglu Hong, Vamsidhar Kamanuru, Jay Rainton, Chen Wu, Mengmeng Ji, Hanchen Li, Urmish Thakker, James Zou, Kunle Olukotun. Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models. ICLR, 2026. arXiv:2510.04618v3. https://arxiv.org/abs/2510.04618v3
2. Lakshya A. Agrawal, Shangyin Tan, Dilara Soylu, Noah Ziems, Rishi Khare, Krista Opsahl-Ong, Arnav Singhvi, Herumb Shandilya, Michael J. Ryan, Meng Jiang, Christopher Potts, Koushik Sen, Alexandros G. Dimakis, Ion Stoica, Dan Klein, Matei Zaharia, Omar Khattab. GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning. ICLR, 2026. arXiv:2507.19457v2. https://arxiv.org/abs/2507.19457v2
3. Yifan Yang, Ziyang Gong, Weiquan Huang, Qihao Yang, Ziwei Zhou, Zisu Huang, Yan Li, Xuemei Gao, Qi Dai, Bei Liu, Kai Qiu, Yuqing Yang, Dongdong Chen, Xue Yang, Chong Luo. SkillOpt: Executive Strategy for Self-Evolving Agent Skills. 2026. arXiv:2605.23904v2. https://arxiv.org/abs/2605.23904v2
4. Ching-An Cheng, Allen Nie, Adith Swaminathan. Trace is the Next AutoDiff: Generative Optimization with Rich Feedback, Execution Traces, and LLMs. NeurIPS, 2024. arXiv:2406.16218v2. https://arxiv.org/abs/2406.16218v2
5. Minsoo Kim, Seung-won Hwang. Dual-Scale World Models for LLM Agents Towards Hard-Exploration Problems. 2025. arXiv:2509.24116v2. https://arxiv.org/abs/2509.24116v2
6. Xuan Zhang, Wenxuan Zhang, See-Kiong Ng, Yang Deng. Self-Evolving World Models for LLM Agent Planning. 2026. arXiv:2606.30639v2. https://arxiv.org/abs/2606.30639v2
7. Igor Bogdanov, Chung-Horng Lung, Thomas Kunz, Jie Gao, Adrian Taylor, Marzia Zaman. FORGE: Self-Evolving Agent Memory With No Weight Updates via Population Broadcast. ACM Conference on AI and Agentic Systems, 2026. DOI:10.1145/3786335.3813155. https://arxiv.org/abs/2605.16233v1
8. Yunhao Yang, Neel P. Bhatt, Kevin Wang, Samuel Tetteh, Zhangyang Wang, Ufuk Topcu. VASO: Formally Verifiable Self-Evolving Skills for Physical AI Agents. 2026. arXiv:2606.05395v1. https://arxiv.org/abs/2606.05395v1
9. Zhanzhi Lou, Hui Chen, Yibo Li, Qian Wang, Bryan Hooi. Meta-TTL: Meta-Learning Self-Improvement Policies for Language Agents. 2026. arXiv:2604.00830v4. https://arxiv.org/abs/2604.00830v4
