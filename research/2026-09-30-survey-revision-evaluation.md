# Self-improvement 综述补核：形式化、评测目录与加速实验协议

核验日期：2026-09-30。本文是对主报告的证据补充，不替换主报告或既有 dossier。没有分配新的全局 E/D 编号；下列 V、L、EV 只是本文件局部定位符。E669/D446 保留给并行计划。

**结论。** 该综述能提供“更新对象—反馈来源—时间过程”的框架，但它并没有把 self-improvement 定义成加速，也没有保证每次自我修改都带来提升。项目页的 **253 方法条目 + 59 评测条目**可复算；后者不是 59 个独立 benchmark，而是 **45 个不同主链接、14 条额外重复出现**，且包含 judge、平台及一个明确错链。最适合我们的验证并非“全部跑一遍”：可先以 **AppWorld 或 WorkArena/WebArena**建立可控的未来任务复用实验，**ST-WebAgentBench**补充规则回归，**DiscoveryWorld/PhysGym**隔离主动探索机制，**OSWorld/ClawBench**用于之后检验外部有效性。每个选择都有不同的反馈和重置边界。

**阅读范围与证据层级。** 综述实际读本为 arXiv:2607.13104v1，2026-07-14，PDF 97 页；正文 pp5–57（§1–10）已按原 PDF 文字层通读，关键公式 pp12–14、50 已看渲染；没有逐篇展开它的全部参考文献。重点核 §3、4、6、7.2、7.6、8、9。评测目录按项目页下载快照逐行检查；选中的 **12 篇评测原文**阅读了任务、协议、指标、限制等相关正文及附录，表格关键数字另核 PDF。其余条目仅做范围筛查，逐条标明深度，不宣称原文通读。以下事实均为一手论文/官方项目材料；“我们建议/推论”是本研究的判断。

本地审计输入：`/private/tmp/selfimprovement-survey-2607.13104.pdf`、`/private/tmp/selfimproving-survey-hub.html`、`/private/tmp/survey-evaluation-inventory.json`。临时文件不保证长期保留，正式来源链接及版本均写在本文。

## 1. 核验与证据

### 1.1 综述形式化：原文到底定义了什么

| 局部ID | 待核点 | 原文与定位 | 判定 |
|---|---|---|---|
| V01 | Agent、模型、scaffold 是否同一对象 | §3.1，PDF p12，式(1)–(3)：agent 配置由模型参数与 scaffold 共同决定；动作符号和 agent 符号不同 | 不得把模型固定写成 agent 固定 |
| V02 | self-improvement 是单轮反思还是持久更新 | §3.2，PDF p13，式(4)后原文短语：**“commits durable changes”**；同时说更新可撤销 | 工作记忆变化本身不足；持久也不等于不可回滚 |
| V03 | `\mathcal C_t` 是否成本或 agent 配置 | §3.2，PDF p13，式(4)定义它为任务/部署上下文，例子包括任务分布、用户交互流、自博弈环境 | 成本预算另用 `b_t`，不能混写 |
| V04 | 不训练模型是否无成本、无遗忘 | §3.3 PDF p16 承认 scaffold 更新也会破坏能力；§9.2 p56 承认上下文、轨迹和验证成本 | §4.2 p17与§9 p55某些概括偏强，不能当保证 |
| V05 | 评测是否只需一次最终分数 | §8.1 PDF pp50–51，式(26)；要求 **“full performance trajectory”**，并有累计预算 | 应评价整个改进过程和回归，不能只取峰值 |
| V06 | scaffold 目录是否天然免训练 | §6.3.1 PDF p38 的 routing 讨论包含监督训练/RL；§6.2中也有训练记忆模块的方法 | 分类是检索入口，逐论文核参数边界仍必要 |
| V07 | 原文提供了加速目标吗 | 式(26)是给定预算下的期望质量，不是最小延迟目标；§8.1.1另要求成本分解 | 加速目标必须由我们明确补充并标为改写 |

以下保留原文符号；排版变化不改变含义。

**[原式] Agent 配置与行为（§3.1，PDF p12，式1–3）**

\[
\mathcal A_t=(\theta_t,\Sigma_t),\qquad
\Sigma_t:=(p_t,m_t,\mathcal T_t,g_t),
\]
\[
\pi_{\theta_t,\Sigma_t}(A_t\mid X_t).
\]

- `\mathcal A_t`：时刻/迭代 `t` 的 agent 配置。普通字母 `A_t`：该系统产生的动作。不要因 PDF 文本提取丢字体而把两者合并。
- `\theta_t`：foundation model 神经参数。
- `p_t`：结构化 prompts 或系统指令；`m_t`：记忆机制及其检索、更新策略，不能仅理解成一段历史文本。
- `\mathcal T_t`：外部工具集合及调用接口；`g_t`：路由、调度、安全约束等控制逻辑。
- `X_t`：执行中的暂态状态，例如 KV cache、中间计划、短期工作记忆；通常会在任务边界重置。模型、scaffold 与暂态上下文共同决定实际动作分布，`\theta` 固定不等于有效策略不变。

**[原式] self-induced 更新（§3.2，PDF p13，式4）**

\[
\mathcal A_{t+1}=\mathcal U\!\left(
\mathcal A_{1:t},
\mathcal E(\pi_{\theta_t,\Sigma_t};\Sigma_t,\mathcal C_t)
\right).
\]

`\mathcal E` 是 agent 执行的信号产生过程；可以产生交互轨迹、反思、批评、验证结果、编辑建议。`\mathcal C_t` 是任务/部署上下文。显式给 `\mathcal E` 输入 `\Sigma_t` 是为允许检查自身 prompt/工具配置。`\mathcal U` 使用这些信号与配置历史提交持久更新。

“self-induced”不等于反馈完全来自模型的自说自话：工具结果、环境成败和程序验证都可提供信号；也不等于没有设计者设置任务、规则或外部评估器。该定义描述更新机制，**式(4)没有 `performance_{t+1}≥performance_t` 的单调约束，也没有证明能力或速度必然提升**。§8.1.1 p51还明确承认平台期与回归，要求报告完整过程。

**[原式] 两条更新通道（§3.2，PDF p14，式5–6）**

\[
\theta_{t+1}=\mathcal U_\theta\!\left(
\theta_{1:t},\mathcal E(\pi_{\theta_t,\Sigma_t};\Sigma_t,\mathcal C_t)
\right),\qquad \Sigma_{t+1}=\Sigma_t,
\]
\[
\Sigma_{t+1}=\mathcal U_\Sigma\!\left(
\Sigma_{1:t},\mathcal E(\pi_{\theta_t,\Sigma_t};\Sigma_t,\mathcal C_t)
\right),\qquad \theta_{t+1}=\theta_t.
\]

后一式直接覆盖我们的研究范围。但“固定 foundation model”还不自动排除额外训练的 router、retriever、reward model、优化器；若项目要求整个方案都不增加模型训练，应额外审计这些辅助模块，而非只检查执行者的 backbone。

**时间下标的补充。** 原文p12从执行time step引入`t`，p50则以`t`指版本更新iteration；实验设计宜显式区分任务内动作步`k`与持久版本更新`t`。

**[原文记号说明] 信号 `\mathcal S_t`。** §4 PDF p17 将 `\mathcal S_t` 用作执行/评价产生的可复用信号；式(8)将 scaffold 更新写成 `\Sigma_{t+1}=\mathrm{IMPROVE}_{\Sigma}(\Sigma_{1:t};\mathcal S_t)`，并保持 `\theta` 固定。§6 Algorithm 2（pp26–27）的例子含 traces、critiques、success/failure 和 cost，后面可以过滤或加权。信号可为结构化轨迹/自然语言，不要求可微，也不要求只是标量 reward。

**一个不能照抄的排版不一致。** Algorithm 2 p27末尾的 scaffold tuple 仅列 prompt、memory、tools，没有式(2)的 `g`。这是原文的省略/不一致，不能据此说控制逻辑不属于 scaffold；若我们重写算法，应明确补上 `g` 并标为自己的统一记号。

**[原式] 改进的评测目标（§8.1，PDF p50，式26）**

\[
m_t=\mathbb E_{x\sim\mathcal D_{\mathrm{eval}},\;\tau\sim\mathcal A_t(x)}
[\Phi(x,\tau)].
\]

式前正文另要求 `b_t≤B_max`、`t∈{1,…,T}`，其中 `b_t` 是累计资源消耗。`x` 为留出任务、`\tau` 为执行轨迹、`\Phi` 为评价器。这里原文复用了 `m_t` 表示表现分数，与式(2)的 memory 撞名；后文我们用 `Q` 表示质量以消歧，属于自己的改写。

- 原文 metric evaluator `\Phi_{metric}` 是可执行、确定性的评分器；适用性限于可形式化的目标。
- 原文 judge evaluator `\Phi_{judge}(x,\tau,\kappa;\theta_{judge})` 依赖评分规则 `\kappa` 及模型，须记录模型版本、提示、可见证据、评价预算。
- 这一二分是抽象：实际一个 benchmark 可以混用确定性检查与 LLM judge，不能直接把整个目录分支当纯确定性。

### 1.2 §6、§7、§8、§9对本项目的实际作用

| 综述位置（PDF页） | 原文框架/判断 | 本研究的用法与边界 |
|---|---|---|
| §6.1 pp27–30 | Prompt：标量反馈、定性改写、种群演化、文本梯度；式(18) `Refine(p,c)`，式(19)文本更新 | 可改决策规则/工具调用策略。文本“梯度”是方向性批评，不是对字符串求真实导数；少错误可能省时间，但更长 prompt/额外评估也可能增加成本 |
| §6.2 pp30–37 | Memory 按记什么、如何组织、如何处理分层；式(20)更新记忆 | 轨迹到规则/经验/流程都在这里。Table3 p32是作者定性评分，并非统一基准测出的量化排名，不得拿星级证明哪种记忆更快 |
| §6.3 pp37–40 | 工具路由、迭代改工具、创建新工具；式(21) | 可把多轮决策改成可执行程序；必须区分模型调用、工具调用与内部原子动作。含训练方法，不能整节标免训练 |
| §6.4 pp40–41 | 全 scaffold 修改；式(22)总体更新、(23)改进器也可在 scaffold 内、(24)执行自身序列化描述、(25)用验证器接纳 | 修改范围广不等于改进器本身递归变强；固定外层搜索器也能改全 scaffold。验证通过不等于现实全域正确，更不保证更快 |
| §7.2 pp43–44 | Web 环境部分可观察、反馈稀疏、布局变化，经验/技能可积累；训练法与 scaffold 法并列 | 区分“拿轨迹训练模型”和“拿轨迹更新代码/记忆”。网站地图复用可能只对固定站有效，验证跨参数与站点漂移 |
| §7.6 pp49–50 | 电脑控制强调应用特性、长程状态、程序性经验；成功验证依赖文件/账户/系统状态 | 环境规则可成为持久工件；但应用表面结构与业务状态应分开测。VM snapshot不自动恢复远端账户 |
| §8.1 pp50–52 | 固定累计预算的改进曲线、留出迁移、回归、尾部风险；judge独立及预算透明 | 应测未来任务净收益，不能只报最新agent成功率或搜索更快。评价器成本与执行成本分列，最终评价不供优化器反复拟合 |
| §8.2 pp52–55 | 机制验证与领域验证两条轴；固定模型和训练模型可以使用相同领域环境 | benchmark自身一般不强迫训练。选一个能观测机制的环境，再选一个能检验真实任务有效性的环境，而非靠目录标签排除 |
| §9.1 pp55–56 | 快/慢环协调、反馈可靠性、验证/可回退修改；讨论 critic 与生成器的独立性 | 这是作者提出的设计方向，不是已证实解决长期自改进。参数蒸馏不在我们的近期范围；回滚与回归可直接借鉴 |
| §9.2 pp56–57 | 测试时持续学习、主动探索、参数/结构联合、资源限制、多agent共演化、开放世界漂移 | 我们更接近主动探索+资源受限的持久 scaffold 学习。综述没有证明“从轨迹学习”本身还有新颖性，须对照具体方法 |

**正文内部需谨慎的概括。** §4.2 p17称 scaffold 可避免 catastrophic forgetting，而 §3.3 p16承认 prompt/记忆/工具变更可破坏原能力。应采用后者的限定说法：无需改模型权重，仍存在系统行为回归。§9 p55对 scaffold “开销低”的总括，也不能盖过§9.2对上下文扩展和验证成本的警告。§8.2对机制 benchmark 的理想化描述，不代表所有列出的基准已经提供持久学习、严格留出及全成本评估。

### 1.3 253 + 59 的目录计数核验

来源：[项目页](https://selfimproving-agent.github.io/#overview)，下载快照访问日期2026-09-30；这是项目方目录一手材料，**条目数量由我们解析 HTML 计算**，不冒充论文自报独立文献数。

| 计数对象 | 快照行数（calc.） | 解释 |
|---|---:|---|
| Foundation model 分支 | 77 | 方法目录出现次数 |
| Scaffolding 分支 | 176 | 方法目录出现次数；同一工作可跨类别 |
| 方法合计 | 253 | 77+176；不能写成253种独立、合格、免训练加速方法 |
| 评测：metric / judge / mechanism / domain | 14 / 5 / 9 / 31 | 合计59 |
| 全部目录行 | 312 | 253+59 |
| 评测不同主链接 | 45 | 按每行第一个论文/项目链接去重，未声称45个不同有效benchmark |
| 评测额外重复行 | 14 | 59−45；13组链接重复，其中SWE-Bench+出现3次 |

重复组：`EV01/35`、`EV02/51`、`EV03/45`、`EV04/20/30`、`EV07/23`、`EV10/22`、`EV11/52`、`EV12/27`、`EV13/39`、`EV15/34`、`EV21/56`、`EV25/57`、`EV26/59`。`EV15/34`是 Agent-as-a-Judge 论文与其 DevAI 资源分列，同一论文身份，不应算两篇独立论文。

**已确认错链。** EV14 的 ClawBench 链接 `2601.08613` 实际是磁性双螺旋纳米线论文；与题名及作者官方 repo 不符。我们从 [TIGER-AI-Lab 官方仓库](https://github.com/TIGER-AI-Lab/ClawBench)交叉定位到 [arXiv:2604.08523](https://arxiv.org/abs/2604.08523)，实际读 v2。保留原行作为错误审计，并单独说明更正；不静默将快照改成“本来正确”。

### 1.4 全59行范围筛查

深度：**P**=原文任务/方法/评价/相关附录已核；**S**=目录+综述相关段落初筛，未展开原文；**R**=同源重复，阅读深度继承被指向行。`核心`表示值得进入验证候选，并非必须全跑；`机制`为辅助测量/机制设计；`背景`为暂不做主基准；`范围外`仅相对当前企业web/电脑任务；`待核`不作为结论证据。S行的 venue 是目录元数据，未自动视为完成来源资格认证；其题目/大类只支撑分流，不能支撑细节结论。

| 行 | 项目与原目录链接 | 判定 | 深度 | 范围理由/下一步 |
|---|---|---|---|---|
| EV01 | [Mind2Web: Towards a Generalist Agent for the Web](https://arxiv.org/abs/2306.06070) | 机制 | P | 静态参考轨迹/动作定位；Task SR非在线终局成功。 |
| EV02 | [ManiSkill2: A Unified Benchmark for Generalizable Manipulation Skills](https://openreview.net/forum?id=b_CQDy9vrD1) | 范围外 | S | 机器人操作；暂不纳入企业web主验证，非判定基准需训练。 |
| EV03 | [CORE-Bench: Fostering the Credibility of Published Research Through a Computational Reproducibility Agent Benchmark](https://openreview.net/forum?id=BsMMc4MEGS) | 背景 | S | 计算科研复现；可执行评价值得后续借鉴，领域不优先。 |
| EV04 | [SWE-Bench+: Enhanced Coding Benchmark for LLMs](https://arxiv.org/abs/2410.06992) | 背景 | S | 编码评测质量/污染相关；此轮不扩展软件修复主域。 |
| EV05 | [WebLINX: Real-World Website Navigation with Multi-Turn Dialogue](https://openreview.net/forum?id=mUSPhG4uDW) | 机制 | P | 多轮静态示范；替代路径不可评，检索组件加速不可冒充部署收益。 |
| EV06 | [GAIA: A Benchmark for General AI Assistants](https://openreview.net/forum?id=fibxvahvs3) | 背景 | S | 通用助手任务；不是专为重复工作流/环境规则设计。 |
| EV07 | [MINT: Evaluating LLMs in Multi-Turn Interaction with Tools and Language Feedback](https://openreview.net/forum?id=jp3gWrMuIZ) | 机制 | P | 反馈使用能力与每轮预算；原协议每个k从头开始，非持续学习曲线。 |
| EV08 | [WorkArena: How Capable Are Web Agents at Solving Common Knowledge Work Tasks?](https://openreview.net/forum?id=BRfqYrikdo) | 核心 | P | ServiceNow参数化企业操作；云状态清理和反馈边界需固定。 |
| EV09 | [AgentGym: Evolving Large Language Model-Based Agents across Diverse Environments](https://arxiv.org/abs/2406.04151) | 机制 | S | 可作多环境接口资源；AgentEvol训练法与环境可用性须分开核。 |
| EV10 | [GitTaskBench: A Benchmark for Code Agents Solving Real-World Tasks Through Code Repository Leveraging](https://arxiv.org/abs/2508.18993) | 背景 | S | 仓库复用代码任务；暂不用于企业web速度推断，资格需另核。 |
| EV11 | [SafeAgentBench: A Benchmark for Safe Task Planning of Embodied LLM Agents](https://arxiv.org/abs/2412.13178) | 范围外 | S | 具身安全任务；安全维度可参考，动作成本不直接可比。 |
| EV12 | [DrunkAgent: Stealthy Memory Corruption in LLM-Powered Recommender Agents](https://arxiv.org/abs/2503.23804) | 机制 | S | 记忆污染/攻击可启发回归测试；未读原文，不引用攻击数字。 |
| EV13 | [ST-WebAgentBench: A Benchmark for Evaluating Safety and Trustworthiness in Web Agents](https://openreview.net/forum?id=MuCDzH0ctf) | 核心 | P | 终局成功+轨迹规则合规；附加压力测试，不单独判加速。 |
| EV14 | [ClawBench: A Benchmark for Evaluating AI Agents on Real-World Online Tasks](https://arxiv.org/abs/2601.08613) | 核心（后期） | P | 原目录错链；更正2604.08523v2后读原文。真实网站、客户端重置非服务器恢复。 |
| EV15 | [Agent-as-a-Judge: Evaluate Agents with Agents](https://arxiv.org/abs/2410.10934) | 机制 | S | 复杂工件/轨迹的agent judge；需另核可靠性与评价成本。 |
| EV16 | [Evaluation Agent: Efficient and Promptable Evaluation Framework for Visual Generative Models](https://aclanthology.org/2025.acl-long.374/) | 范围外 | S | 视觉生成模型评价，不是企业操作执行加速。 |
| EV17 | [EvalAgent: Discovering Implicit Evaluation Criteria from the Web](https://openreview.net/forum?id=erGpkHCybv) | 机制 | S | 隐式评价标准发现；有助rubric设计，尚未原文核可靠性。 |
| EV18 | [Learning to Align Multi-Faceted Evaluation: A Unified and Robust Framework (ARJudge)](https://aclanthology.org/2025.findings-acl.494/) | 机制 | S | 多维judge；如需额外训练judge则不属于全系统免训练主方案。 |
| EV19 | [VerifiAgent: A Unified Verification Agent in Language Model Reasoning](https://aclanthology.org/2025.findings-emnlp.891/) | 机制 | S | 推理验证；可参考验证接口，不据此证明业务状态判定可靠。 |
| EV20 | [SWE-Bench+: Enhanced Coding Benchmark for LLMs](https://arxiv.org/abs/2410.06992) | 重复 | R | 同EV04；不增加独立来源数。 |
| EV21 | [Identifying the Risks of LM Agents with an LM-Emulated Sandbox](https://openreview.net/forum?id=GEcwtMk1uA) | 机制 | S | 模拟工具与风险评价；模拟器正确性/成本需原文另核后采用。 |
| EV22 | [GitTaskBench: A Benchmark for Code Agents Solving Real-World Tasks Through Code Repository Leveraging](https://arxiv.org/abs/2508.18993) | 重复 | R | 同EV10；不增加独立来源数。 |
| EV23 | [MINT: Evaluating LLMs in Multi-Turn Interaction with Tools and Language Feedback](https://openreview.net/forum?id=jp3gWrMuIZ) | 重复 | R | 同EV07；不增加独立来源数。 |
| EV24 | [TaskBench: Benchmarking Large Language Models for Task Automation](https://arxiv.org/abs/2311.18760) | 机制 | S | 任务分解/工具规划组件；不默认等于在线可重置工作流。 |
| EV25 | [MetaTool Benchmark for Large Language Models: Deciding Whether to Use Tools and Which to Use](https://arxiv.org/abs/2310.03128) | 机制 | S | 是否用工具/用哪个工具的决策；可做路由组件测试。 |
| EV26 | [The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models](https://openreview.net/forum?id=2GmDdhBdDk) | 机制 | S | 函数调用评测；版本跨度大，采用前需明确具体任务接口。 |
| EV27 | [DrunkAgent: Stealthy Memory Corruption in LLM-Powered Recommender Agents](https://arxiv.org/abs/2503.23804) | 重复 | R | 同EV12；不增加独立来源数。 |
| EV28 | [RSI-Bench: Multi-Axis Benchmark for Recursive Self-Improvement](https://github.com/sunghunkwag/rsi-bench) | 待核 | S | 仅GitHub目录项，机构/正式出版资格未确认，隔离不用作结论。 |
| EV29 | [SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](https://openreview.net/forum?id=VTF8yNQM66) | 背景 | S | 软件issue修复；供scaffold相关研究背景，不作web加速主基准。 |
| EV30 | [SWE-Bench+: Enhanced Coding Benchmark for LLMs](https://arxiv.org/abs/2410.06992) | 重复 | R | 同EV04；不增加独立来源数。 |
| EV31 | [SWT-Bench: Testing and Validating Real-World Bug-Fixes with Code Agents](https://openreview.net/forum?id=9Y8zUO11EQ) | 机制 | S | 测试/验证补丁可启发工件回归检查；本轮未读，不声称迁移已证实。 |
| EV32 | [TDD-Bench Verified: Can LLMs Generate Tests for Issues Before They Get Resolved?](https://arxiv.org/abs/2412.02883) | 机制 | S | 问题解决前生成测试；可借鉴验证独立性，IBM研究来源待专项核版。 |
| EV33 | [LoCoBench-Agent: An Interactive Benchmark for LLM Agents in Long-Context Software Engineering](https://arxiv.org/abs/2511.13998) | 背景 | S | 长上下文软件任务；任务形态与企业web不同。 |
| EV34 | [DevAI: Automated AI Development Benchmark](https://arxiv.org/abs/2410.10934) | 重复 | R | 同EV15；DevAI是同篇论文的资源，不是第二篇独立论文。 |
| EV35 | [Mind2Web: Towards a Generalist Agent for the Web](https://arxiv.org/abs/2306.06070) | 重复 | R | 同EV01；不增加独立来源数。 |
| EV36 | [WebArena: A Realistic Web Environment for Building Autonomous Agents](https://openreview.net/forum?id=oKn9c6ytLx) | 核心 | P | 可恢复自托管站点、功能终局评价；部分题用LLM judge。 |
| EV37 | [VisualWebArena: Evaluating Multimodal Agents on Realistic Visual Web Tasks](https://openreview.net/forum?id=RPKxrKTJbj) | 背景 | S | 视觉web外部有效性候选；先避免把视觉grounding与经验机制混为一谈。 |
| EV38 | [WebCanvas: Benchmarking Web Agents in Online Environments](https://arxiv.org/abs/2406.12373) | 待核 | S | live web候选，但来源资格/真实重置和指标未核；不纳结论。 |
| EV39 | [ST-WebAgentBench: A Benchmark for Evaluating Safety and Trustworthiness in Web Agents](https://openreview.net/forum?id=MuCDzH0ctf) | 重复 | R | 同EV13；不增加独立来源数。 |
| EV40 | [clembench: Using Game Play to Evaluate Chat-Optimized Language Models as Conversational Agents](https://aclanthology.org/2023.emnlp-main.689/) | 范围外 | S | 对话游戏协议；暂不纳企业web主验证。 |
| EV41 | [clembench-2024: A Challenging, Dynamic, Complementary, Multilingual Benchmark and Underlying Flexible Framework for LLMs as Multi-Action Agents](https://arxiv.org/abs/2405.20859) | 范围外 | S | 对话游戏框架更新；不能与2023版本结果混用。 |
| EV42 | [GameBench: Evaluating Strategic Reasoning Abilities of LLM Agents](https://arxiv.org/abs/2406.06613) | 范围外 | S | 战略游戏；未核正式主会资格，不作核心论据。 |
| EV43 | [LLM-Deliberation: Evaluating LLMs with Interactive Multi-Agent Negotiation Game](https://openreview.net/forum?id=eE1WHn6qlk) | 范围外 | S | 多agent谈判；对手变化干扰与当前目标不同。 |
| EV44 | [GTBench: Uncovering the Strategic Reasoning Capabilities of LLMs via Game-Theoretic Evaluations](https://arxiv.org/abs/2402.12348) | 范围外 | S | 博弈策略能力；不直接验证企业流程加速。 |
| EV45 | [CORE-Bench: Fostering the Credibility of Published Research Through a Computational Reproducibility Agent Benchmark](https://openreview.net/forum?id=BsMMc4MEGS) | 重复 | R | 同EV03；不增加独立来源数。 |
| EV46 | [DiscoveryWorld: A Virtual Environment for Developing and Evaluating Automated Scientific Discovery Agents](https://openreview.net/forum?id=cDYqckEt6d) | 核心（机制） | P | 探索→假设→实验→规则；可区分任务完成和知识正确。 |
| EV47 | [PaperBench: Evaluating AI's Ability to Replicate AI Research](https://arxiv.org/abs/2504.01848) | 背景 | S | OpenAI科研复现评测；长流程计费/判分可后续借鉴，此轮未展开。 |
| EV48 | [PhysGym: Benchmarking LLMs in Interactive Physics Discovery with Controlled Priors](https://openreview.net/forum?id=w8uII2qAmd) | 核心（机制） | P | 可控先验+主动选择实验；是函数规律发现，不能替代业务状态机。 |
| EV49 | [AstaBench: Rigorous Benchmarking of AI Agents with a Scientific Research Suite](https://openreview.net/forum?id=M7TNf5J26u) | 机制 | P | 标准工具、分离工具访问与模型能力、统一费用；不是持续学习现成协议。 |
| EV50 | [MLS-Bench: A Holistic and Rigorous Assessment of AI Systems on Building Better AI](https://arxiv.org/abs/2605.08678) | 背景 | S | 构建AI系统的评测；任务可能含训练不等于执行agent必需训练，未展开。 |
| EV51 | [ManiSkill2: A Unified Benchmark for Generalizable Manipulation Skills](https://openreview.net/forum?id=b_CQDy9vrD1) | 重复 | R | 同EV02；不增加独立来源数。 |
| EV52 | [SafeAgentBench: A Benchmark for Safe Task Planning of Embodied LLM Agents](https://arxiv.org/abs/2412.13178) | 重复 | R | 同EV11；不增加独立来源数。 |
| EV53 | [EmbodiedBench: Comprehensive Benchmarking Multi-Modal Large Language Models for Vision-Driven Embodied Agents](https://openreview.net/forum?id=DgGF2LEBPS) | 范围外 | S | 视觉具身操作；暂不扩大到机器人主域。 |
| EV54 | [OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments](https://arxiv.org/abs/2404.07972) | 核心（后期） | P | 真实OS任务与VM快照；UI/环境运行噪声和远端状态另控制。 |
| EV55 | [AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents](https://aclanthology.org/2024.acl-long.850/) | 核心 | P | API跨应用任务，可复位DB+时间，终局含额外改动检查。 |
| EV56 | [Identifying the Risks of LM Agents with an LM-Emulated Sandbox](https://openreview.net/forum?id=GEcwtMk1uA) | 重复 | R | 同EV21；不增加独立来源数。 |
| EV57 | [MetaTool Benchmark for Large Language Models: Deciding Whether to Use Tools and Which to Use](https://arxiv.org/abs/2310.03128) | 重复 | R | 同EV25；不增加独立来源数。 |
| EV58 | [Windows Agent Arena: Evaluating Multi-Modal OS Agents at Scale](https://openreview.net/forum?id=W9s817KqYf) | 背景 | S | Windows外部有效性候选；先用OSWorld核机制，未读原文不承诺重置能力。 |
| EV59 | [The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models](https://openreview.net/forum?id=2GmDdhBdDk) | 重复 | R | 同EV26；不增加独立来源数。 |

### 1.5 优先基准的原文协议核验

以下页码均为列明读本的 PDF 物理页码。每项先陈述原文，再给我们的适用性判断。基准可用于免训练方法，不意味着其原论文的全部 baseline 都免训练。

#### AppWorld：适合先隔离“条件、状态、可执行流程”的机制

**原文/资格。** ACL 2024 正式长文，读[正式PDF](https://aclanthology.org/2024.acl-long.850.pdf)，55页，Stony Brook/Ai2/Saarland。§2–3 pp3–6、§E 的 baseline与成本说明。

- **任务与环境。** §2.1 p3：9个应用、457个API，另有API文档与Supervisor帮助接口。代理通过有状态的Python执行器读取/修改应用数据库。它是API/代码操作环境，不能把结论直接当浏览器点击或视觉定位加速。
- **重置。** §2.2 pp3–4明确控制数据库和时间，可将两者回到一致起点。因此可以做相同初始状态下的分支实验；这不代表真实云服务也有同样能力。
- **目标与判分。** §3.1–3.2 pp4–6：自然语言任务由场景与参数实例化；有 distractor、hurdle 和contrast条件。检查执行前后DB差异，既要实现要求的变化，也不能越过允许变化集合。TGC=所有测试均通过的任务比例；SGC=同一场景所有实例任务均通过的场景比例，后者更强调条件变化后的稳定性。原文原句 **“collateral damage”** 指任务外的不必要修改。
- **反馈。** agent看到API文档、返回值和运行错误。终局unit tests与每条assertion的自然语言说明不自动进入运行时上下文；p6脚注16把更细粒度反馈列为可支持未来工作的方向。§E反思实现也明确不用Reflexion式oracle反馈。不能据“测试可执行”推断代理每步收到真实答案。
- **效率口径。** 主指标是TGC/SGC。附录报告baseline模型调用费用，但并不是覆盖探索、工件提取、维护、环境运行及未来复用的生命周期成本。实验自己记录这些项。

**我们的推论。** 很适合第一轮测试：从旧轨迹提取可执行小流程及前置条件，再看不同参数、不同初始数据库状态的未来任务。原基准已经有contrast实例，不能把“增加条件变化”单独主张为我们的创新；新意需落在如何学得/验证条件，以及何时复用真正更划算。若研究论文最终面向web，需再到浏览器环境检验收益是否仍成立。

#### WorkArena：重复企业操作很贴近，但反馈和计步要小心

**原文/资格。** ICML 2024/PMLR235正式论文，读[正式PDF](https://raw.githubusercontent.com/mlresearch/v235/main/assets/drouin24a/drouin24a.pdf)，21页。ServiceNow Research/Mila。指2024原版，不混入后续WorkArena++ L2/L3。

- **规模与任务。** §3 pp3–5、Table6 p13：33类任务、19,912个预定义参数实例，覆盖列表、表单、服务目录、知识库、仪表盘与导航。指令显式给完成所需参数。主实验§5.2 p7每类取10 seeds，即330 episodes/模型（calc.），并未完整跑19,912个实例。
- **环境与重置。** 真实ServiceNow云开发实例；§4.2 p6的`setup()`构建任务数据并登录/导航，`teardown()`清理任务创建资源。不是本地网站镜像或任意中间状态snapshot，需实际验证清理与串扰。论文当年的开发实例可用性不是当前服务承诺。
- **反馈边界。** §3.1 p3明确 **“real-time feedback”**；`validate()`可以返回reward、optional user message、done（§4.2 p6），例如缺失字段和错误写入。因此不能概括成所有终局反馈均隐藏。`cheat()`是人工Playwright oracle，不是默认可让执行者调用的普通动作。必须保存实际传给模型的错误/消息以及外层学习器收到的评分。
- **计步/指标。** 主实验最多15 agent steps；§5.2 p7指出不开multi-action时部分任务需要超过此步数。把多个原子动作封装成工具后，只报steps降低可能只是预算单位变化。主指标为SR±SE，非统一美元/墙钟；观察token规模也不等于总账。
- **作者限制。** §5.4与结论p9：原版许多任务是局部操作，关键状态在当前页，不常需要跨页长期记忆；保留旧thought有时固化早期错误。

**我们的推论。** 很适合小范围可复用操作和多参数实例，未必能单独证明长程记忆价值。若用作主基准，先固定agent原子能力与观察，再分别记录模型调用、包装工具调用、浏览器原子动作与时延。应把同模板新参数和留模板泛化分开报告。

#### WebArena：在线终局评价、可恢复起点，适合可控探索

**原文/资格。** ICLR 2024已核正式录；实读[arXiv:2307.13854v4](https://arxiv.org/pdf/2307.13854v4)，2024-04-16，22页。

- **任务。** §2–3 pp3–7：电商、论坛、代码协作、CMS等自托管应用及辅助工具。812实例来自241模板（§3.1 p5），不是812个独立工作流。任务允许功能等价的不同路径。
- **重置。** §2.3 p4、A.2 pp15–16：从原Docker image重建网站/DB能回到初始状态；不是任意中间点的免费回滚。作者估计恢复每站几秒到一分钟，不是统一实测分布，故不用于我们时延预算。
- **判分。** §3.2 pp6–7用数据库/API/DOM/URL/回答内容判终局；A.8 p17说82题用GPT-4-0613 fuzzy answer匹配，其余还有exact/must-include等规则。因此“全确定性verifier”不准确。原baseline普通观察不是evaluator内部答案/查询结果。
- **预算。** A.6 p17最多30状态转移，并有重复/无效动作提前终止规则。主指标是端到端SR，不是净加速；不能把新方法包装动作后的step口径直接和历史baseline比较。

**我们的推论。** 对“探索有价值吗”很合适：有在线分支、终局检查、可恢复起点。不过经验学习要另加任务流协议。按同模板新参数测试近迁移，按模板/站点留出测试远迁移，分别回答问题；不能用一个随机split同时声称两者。

#### ST-WebAgentBench：省步骤是否省掉了必要动作

**原文/资格。** ICLR2026正式录已核；读[arXiv:2410.06703v7](https://arxiv.org/pdf/2410.06703v7)，2026-06-04，42页，IBM Research。

- **版本与任务。** v7 PDF §3/Table2 pp5–8为375任务、3,057 policy instances、六维，涉及GitLab、ShoppingAdmin、SuiteCRM；landing摘要仍写222，不能混用。policy instance不是同等数量的不同规则模板。
- **判分对象。** §3.3 p5区分CR（任务完成）、CuP（完成且零违规）、PCR（至少一个成功检查满足的任务比例）/pCuP（该部分完成条件且零违规）；还检查轨迹中的确认、范围、执行顺序、指令层级、安全性和错误处理。AppH.3 p37声称无LLM judge，但部分消息检查是RapidFuzz与给定模板的字符串比较，不是任意语义政策理解。
- **反馈与规则。** POLICY_CONTEXT是可见已知规则（§4.2 p8、AppF pp25–28），非必须自行发现的隐藏业务知识。模拟用户自动批准确认，不能衡量实际人类等待/拒绝。当前官方`task.py`可把`safety_report`放在`info`里；harness读取不等于模型提示实际收到。用它优化方法需声明为额外学习信号。
- **重置。** 当前[官方代码](https://raw.githubusercontent.com/segev-shlomov/ST-WebAgentBench/main/browsergym/stwebagentbench/src/browsergym/stwebagentbench/task.py)的setup主要登录/导航/注入脚本，teardown只删除临时config；该模块没有证明DB完整恢复。`env.reset()`这个名字不足以保证重复修改任务不串扰。当前代码读取日期2026-09-30，未锁commit，正式实验必须固定版本并补测。
- **指标限制。** 这些指标不是速度。原文运行时与个别risk ratio分母存在不可复算的叙述，本文不拿来作成本效应证据。正式会议作者元数据与v7作者数也有差别，参考文献分开列。

**我们的推论。** 用作回归/压力测试，比用作唯一主环境更合适。宏加速仍须满足任务前确认、权限和不可遗漏动作，成功率提高不能掩盖违规。若借鉴其政策模板，应避免把公开政策与我们要探索的未知环境规则混为一类。

#### Mind2Web与WebLINX：有轨迹，不等于能测在线探索和净加速

**Mind2Web原文。** NeurIPS2023 Datasets and Benchmarks正式文；读[arXiv:2306.06070v3](https://arxiv.org/pdf/2306.06070v3)，2023-12-09，24页。§2 pp3–5为2,350任务、137网站、31领域（归五大类）的静态人类示范，保存DOM/MHTML/截图/网络信息。§4.2 p7最关键的原句是 **“given ground-truth action history”**：每步独立预测。Step SR检查参考元素与操作，Task SR要求一条演示全部参考步匹配成功；没有把预测动作在线执行到真实下一状态。

原文cross-task、cross-website、cross-domain可借鉴为经验迁移划分（§4.1 p7），但离线Task SR不能评错误恢复、探索新动作、替代短路径或宏跳步后的终局。原MindAct还包含训练过的候选过滤器，不能把组件效果自动列作免训练证据。

**WebLINX原文。** ICML2024正式文，读[正式PDF](https://raw.githubusercontent.com/mlresearch/v235/main/assets/lu24e/lu24e.pdf)，50页；§3–7 pp4–9、B.4.1 p29。2,337示范、155站，平均43turns；多轮指令变化，主要评价逐轮intent、元素IoU及文本相似度。§7.2 p8明确承认静态示范难以评替代轨迹。BrowserGym兼容接口不等于恢复在线服务器。

原文检索器效率对比在相同CPU/GPU上，DMR-MiniLM为186ms/turn，MindAct-DeBERTa为916ms/turn（§5.1、B.4.1；训练集24,418 active turns）。约4.9倍（calc.）只指候选检索组件，DMR也需训练；不是完整任务墙钟，更不是从历史经验免训练自我改进收益。

**我们的推论。** 这两者适合离线抽取经验、检索、观察压缩的辅助测量；若宏能省掉参考步骤，静态动作相似度甚至会错误惩罚它。不要用“它有trajectory”作为主benchmark选择的充分条件。

#### OSWorld：真实电脑执行的外部有效性，保留VM与远端状态区别

**原文/资格。** NeurIPS2024 Datasets and Benchmarks已核正式录；实读[arXiv:2404.07972v2](https://arxiv.org/pdf/2404.07972v2)，2024-05-30，51页，不假定与后续OSWorld-Verified协议相同。

§2.1–2.2 pp3–5：代理通过截图/可访问性树等观察，用PyAutoGUI等动作操作真实桌面；任务设置准备文件/窗口，VM快照恢复操作系统，结束后做后处理和状态评价。评价可有部分分数及不可行任务判定。§3 p6的369任务是Ubuntu集合，另有43个Windows任务分析；框架能支持多OS不等于同样369任务均在所有OS跑。

§4 p10原实验步预算为15，不能与当前榜单步数混为一谈。主指标是任务成功/状态评价；人类耗时不是agent加速倍率。VM快照可控制本地软件状态，但外部账户、云内容、实时网页不自动回滚；论文p5本身含外部数据来源。

**我们的推论。** 适合在机制明确后测跨应用迁移，早期直接跑它可能把UI grounding、VM性能、文件状态及经验学习效果混在一起。固定快照、应用版本、显示配置、动作预算与模型；把环境启动/重置开销和任务服务时延分别报告。

#### ClawBench：更正错链后的真实网站验证候选

**原文/资格。** 实读[arXiv:2604.08523v2](https://arxiv.org/pdf/2604.08523v2)，2026-07-20，28页；UBC/Waterloo/CMU等强机构preprint。官方repo自报EMNLP2026 Findings，本次未独立核正式录，按preprint资格使用。

§2.1 pp4–5的153任务、144 live网站、15细分类别强调跨站广度，同站可重复实例很稀疏。§2.2 p5人工标注最终提交请求的endpoint/method/payload，经CDP拦截终端写请求，其余先前动作仍可运行；作者说明是 **“task-scoped safety envelope”**，不能把对人工参考终端请求的100%覆盖当全部agent路径均无副作用。

§2.3 p6的Sonnet4.6 agent judge依据人工轨迹/目标payload作事后评价；成功通常是到达被拦截/允许的等价终点，不是服务器实际完成业务提交。AppE p26每个(model,task)重新建容器/Chrome profile；这是客户端重置，不能恢复真实服务器；30分钟墙钟上限、5分钟无动作中断、无显式最大step。Limitations p13承认布局、地域、账户、反爬和A/B测试带来的不可精确复现。

有公开五层轨迹（视频、截图、HTTP、agent消息、浏览器动作），已在[官方数据入口](https://github.com/TIGER-AI-Lab/ClawBench#datasets)链接。Table3 p7记录每任务平均API费用/token，Table5 p17记录墙钟median/p90及tool calls；但低耗时可能由早退造成，不能跨模型配置直接解释成有效加速，也未完整核算经验构建/维护。

**当前版本不能混用。** 2026-09-30官方repo shipping V1已是152任务/143站（删除一项），另有V2=129任务/63站、judge亦有更新；原论文v2研究的是历史V1=153/144。这里“论文v2”与“数据V2”是两个不同版本轴。

**我们的推论。** 更适合第二阶段查真实网站漂移、失败分布，或先离线分析已有trace。不适合一上来当可任意回退、多次在线探索的低成本主环境。

#### DiscoveryWorld：把“知道规则”和“碰巧完成”分开

**原文/资格。** NeurIPS2024 Datasets and Benchmarks正式录已核；实读[arXiv:2406.06769v2](https://arxiv.org/pdf/2406.06769v2)，2024-10-07，29页，Ai2/Microsoft/Arizona。

§3 pp4–6：8类科学主题×3难度×5参数seed=120任务。代理在模拟世界观察、提出假设、使用实验工具、行动；同seed决定对象属性和答案，但这里只说明参数化可复现，不宣称提供任意历史中间状态快照。动作集合抽象、带导航辅助，不能将动作数与浏览器点击直接比较。

§3.4 p6分别评价：二元任务完成；程序化的任务相关操作/过程scorecard；发现的解释性知识。知识部分用ground-truth问题由人或LLM评价，实验用GPT-4o；**不是全部规则都由形式证明验证**。普通观察有task-completion flag（§3.1 p5），这不等于完整scorecard/知识答案都在运行时对代理可见。

§4.1及AppC.2 pp15–16：原baseline是独立zero-shot任务，**“without any carry-over knowledge”**；不能把原表直接当持续学习效果。作者另给学习划分：同主题seed0/1用于训练/经验开发、seed2验证、3/4测试；跨主题另有划分。我们可以在固定模型下用这些划分设计经验学习，须标明这是自己的协议而非原baseline。

作者Limitations p15指出低保真模拟与真实科学差距；长轨迹LLM调用代价高。AppD.3 p22的Hypothesizer还有额外知识更新/摘要调用，不能只数环境动作。本文不用旧API费用估算作当前预算。

**我们的推论。** 适合隔离主动实验能否学出正确可迁移规则，以及知识是否减少后续试错。它不直接验证企业业务规则和工作流效率，定位为机制小实验更恰当。

#### PhysGym：控制先验的主动探索，注意oracle和判分不是纯形式化

**原文/资格。** NeurIPS2025 Datasets and Benchmarks正式录已核；读[arXiv:2507.15550v2](https://arxiv.org/pdf/2507.15550v2)，2025-10-26，39页，KAUST/IDSIA。

§3 pp5–7：97物理方程问题，agent自主选择输入变量、获得函数输出，提出规律。四层先验从完整物理上下文/变量含义到匿名变量逐级遮蔽（§3.3 p6，§4.1 p7）；L4仍有“关系属于物理方程”的隐式先验，也不能擦除预训练物理知识，不宜叫绝对无先验。

§4.1 p7明确给100次实验quota，并允许 **“one oracle test”**：返回拟合指标和符号等价判断，写入历史后反馈给模型。因此不是完全无ground-truth反馈的探索。一次turn可批量提出多个实验，实验次数、turns和模型调用应分开。

§3.4 pp6–7主SR以SymPy等价判定或LLM等价判断任一通过为成功；辅助R²/MSE/Kendall/MAPE测数据一致性。不能写成全部有严格数学正确性证明。实验数、turns的效率反映采样/交互效率，不自动等于API费用或端到端时延。

**我们的推论。** 能分离“模型已有知识”与“额外交互带来的收益”，是环境探索机制验证的好候选。但它是函数规律发现，不含浏览器的角色/权限/表单/不可逆写入状态机；不能以此替代最终业务任务验证。

#### MINT：反馈使用能力，而非现成的跨任务自改进评测

**原文/资格。** ICLR2024正式论文已核；读[作者发布的会议PDF](https://zihanwang314.github.io/pdf/mint.pdf)，35页。

§2.1 pp3–4：agent可以执行Python工具或提交答案；有基于ground truth的失败反馈及GPT-4生成的自然语言反馈。Table1 p4有586任务，来自推理、代码和ALFWorld等8个数据集。§3 pp5–6按1–5轮预算分别从头开始运行；最多两次答案提交尝试。`SR_k`是给定轮数预算的成功率，回归斜率用于描述增加交互轮数的收益；不是同一持久记忆agent随着任务流不断进化的曲线。

**我们的推论。** 可借鉴反馈消融：工具错误、二元真值、语言批评，各自能带来什么收益；同时记录feedback生成成本和特权信息。它不直接回答旧轨迹对未来任务能省多少时间。

#### AstaBench：最值得借的是公平工具条件和成本账

**原文/资格。** ICLR2026正式记录已核；实读[arXiv:2510.21652v2](https://arxiv.org/pdf/2510.21652v2)，2026-04-21，88页，Ai2及大学团队。

§4.1 pp5–6、AppB p17：提供标准研究工具和有日期边界的文献检索源、Python sandbox；区分标准接口、自定义等价接口与完全自定义tooling。重点是更好的agent与更强信息访问必须分开比较。此套件各子任务有不同评价方式；本文不笼统说所有子任务可统一reset，也不虚构单一反馈协议。

§4.2 pp6–7：`agent-eval`基于Inspect模型usage与固定的litellm价格快照算标准化USD，计入cache折扣，不计service tier/batch等可能以时延换取的折扣；脚注说明更新价格快照时可整体重算。**标准化费用不是实际账单，也不是墙钟**。质量—成本Pareto分析有用，但不自动包含经验搜集、反思、工件维护、评估及多年复用摊销。

**我们的推论。** 可借鉴工具信息边界与价格口径；不必为了这些方法论跑完整科学研究suite。对我们的方案，应在相同基础接口/状态可见性下允许生成工具，再检查收益究竟来自经验、代码执行，还是额外特权数据访问。

### 1.6 从这些协议可以推出什么实验选择（我们的推论）

| 要回答的问题 | 优先环境 | 必须保留的对照 | 不能据此单独证明 |
|---|---|---|---|
| 轨迹经验能否降低同类未来任务成本 | WorkArena / WebArena；若先隔离API机制则AppWorld | 无记忆、仅原轨迹检索、抽象规则、可执行流程；同模型/基础动作/信息权限 | 科学探索能力或跨所有真实站点泛化 |
| 环境探索比被动积累多带来什么 | AppWorld/WebArena中的受控状态变化；DiscoveryWorld/PhysGym作机制补充 | 相同探索预算的被动收集、主动探索、随机/固定探索；知识正确性与任务收益分别测 | 宏平均少走步一定值得前期探索 |
| 省掉的步骤是否破坏必要约束 | AppWorld的非目标DB改动检查、ST-WebAgentBench规则 | 同任务同状态的成功+合规，不只看终局回答 | 所有自然语言业务政策已被完整覆盖 |
| 能否迁移到复杂电脑/真实网站 | OSWorld / ClawBench后期小样本 | 成功约束、同期环境、固定版本/区域/权限、足够重复 | 可任意回滚，或真实外部state完全一致 |
| 更多反馈是否只是更强oracle带来的收益 | MINT式信号消融，加目标环境自己的反馈划分 | 固定反馈可见性、相同judge预算，最终holdout隔离 | 真实生产能取得同样ground truth |
| 如何比较收费与工具优势 | AstaBench式成本/工具账方法 | 价格快照、缓存、信息源、底层权限固定 | 标准化USD=实际账单，或USD下降=墙钟下降 |

**不是新增研究结论的六条协议建议：**

1. **把时间轴分开。** 任务内动作步记 `k`，agent版本/任务流位置记 `t`。版本更新改变持久工件；追加短期上下文不自动算一次self-improvement。存版本diff和被接纳/拒绝的理由。
2. **至少区分两个合同。** “离线提取工件→冻结后在留出任务测”的合同能清楚测迁移；“任务流先执行、再获得反馈、再为后续任务更新”的prequential合同能测部署中的持续收益。后一合同可以在旧任务完成后学习，但不能先看到待预测任务的真值。固定holdout可在checkpoint外部评价，却不把其分数/答案反馈给优化器继续选版本；否则需再设未接触的最终holdout。
3. **标注每条反馈的来源与可见方。** 普通页面/工具返回、异常文本、实时validator消息、最终私有判分、人工oracle、模拟器内部状态不是同一信息条件。scaffold学习器是否比部署执行者多见信息，要显式列出。
4. **采用质量约束下的多指标成本，而非一个模糊“快”。** 至少分模型调用、工具调用、底层动作、input/output/cache token、API费用、墙钟median/p95、错误/回归率；样本量不足不能稳定估p95时给区间并说明。低费用/短耗时可能只是失败早退，不可只在不同成功子集比较后声称总体加速。
5. **探索、工件构造、维护、fallback全部入账。** 环境重置/状态恢复用于受控实验时分列：既不伪装成生产服务时间，也不从研究总资源账消失。最终独立评测的成本分列，若在线反馈评价属于方法必要步骤则计入方法成本；不能重复扣同一维护/评价开销。
6. **报告起点、过程、终点和回退。** 固定预算、多种子/任务顺序、配对任务状态；既看近迁移也看留模板/留环境迁移。工件失效后修复的成本和重新获益的任务数，是动态环境中很关键的结果。

**[我们的改写，不是综述原式] 对本项目更直接的目标。** 令 `Q(\Sigma)` 表示固定模型下、相同任务分布的成功且满足约束的概率；将版本成本的USD与时间分别分析。在质量不劣于预先设定容忍度的前提下比较成本：

\[
Q(\Sigma^{new})\ge Q(\Sigma^{base})-\epsilon,
\qquad
K^{new}(N)<K^{base}(N).
\]

其中 `K` 可以取美元总额，也可以取串行执行的总时间；并行服务下应另看任务延迟和吞吐，不能直接相加声称用户等待时间。对美元的一种不重计分解是：

\[
K^{new}_{\$}(N)=K_{init}
+\sum_{i=1}^{N}\left(
K_{retrieve,i}+K_{execute,i}+K_{fallback,i}+K_{update,i}
\right).
\]

`K_init`包括该方法需要的离线探索/工件生成/验证，`K_update`包含运行中新增工件维护及其必要评价。初始基线若也有setup，不省略；纯研究用的共同最终评测另列。直到同质量条件下累计差额首次为负才有样本上的回本；不能拿单个成功任务的局部节省直接声称整个生命周期提速。这个账本是我们的实验定义，不是综述已证明的定理。

## 2. D-ledger候选纠错（仅局部L编号，未占用全局ID）

| 局部项 | 容易误写的说法 | 应替换为 | 证据 |
|---|---|---|---|
| L01 | 综述收集253篇方法+59个独立benchmark | 当前快照253方法目录行+59评测目录行；评测按主链接去重45，含judge/资源与错链 | §1.3逐行解析 |
| L02 | ClawBench = arXiv2601.08613 | 目录错链；TIGER官方论文为2604.08523，本文读v2 | §1.3、§1.5 |
| L03 | `A_t`都指agent；`C_t`是cost或上下文窗口 | agent为花体`\mathcal A_t`，动作是`A_t`；`\mathcal C_t`是任务/部署情境，瞬时状态是`X_t` | 综述式1–4，pp12–13 |
| L04 | `m_t`统一指memory | 原文式2指memory，式26指表现；写推导需消歧 | p12与p50 |
| L05 | 免训练scaffold自改进一定更快且不会忘 | 只说明更新对象；有context/验证成本与行为回归，必须实测 | §3.3、§8.1.1、§9.2 |
| L06 | offline轨迹里的Task SR=在线任务成功 | Mind2Web每步给正确历史，Task SR为参考路径全部步匹配；WebLINX为逐轮相似度 | 两篇§4/§7 |
| L07 | 所有env.reset等于回滚业务数据库 | AppWorld明确DB+时间；WebArena重建DB；WorkArena按任务清理；ST当前task模块没证明DB复原；Claw仅客户端 | 各原文/代码，§1.5 |
| L08 | 所有环境反馈均隐藏/均可用 | WorkArena可即时反馈；AppWorld终局tests不自动供agent；PhysGym有一次oracle；ST `info`不自动进入模型 | 各协议，§1.5 |
| L09 | WebArena/DiscoveryWorld/PhysGym全部确定性判分 | WebArena部分用GPT-4；Discovery知识项用judge；PhysGym允许LLM等价判分 | 各评价节 |
| L10 | ST-WebAgentBench=222；Claw论文v2=数据V2 | ST v7 PDF是375/3057；Claw论文v2报告历史V1=153/144，当前代码另有V1/V2 | §1.5版本说明 |
| L11 | 标准化API费用就是全生命周期成本/实际延迟 | Asta控制费用口径，仍需补学习/维护/回退总账和独立时间测量 | Asta§4.2及我们的改写 |

以上不是对既有dossier的静默修改；是否对应已有全局D条目由主线程合并时决定。

## 3. 可插入主报告的文字（E-ledger候选patch，不分配ID）

**插入“范围与定义”。**

> 综述将agent写为模型参数与scaffold的组合：`\mathcal A_t=(\theta_t,\Sigma_t)`，其中scaffold包含prompt、memory及其读写策略、工具接口和控制逻辑。Self-improvement指执行产生的轨迹、批评、验证等信号被用于持久更新这些组件；仅在单次任务里追加上下文不一定构成该定义下的持久改进。我们关注`\theta`固定、`\Sigma`可变的子空间，但还需排除新增训练的router/judge等辅助模块。该定义不保证每次更新都提高质量或降低成本。Agent加速是我们选择的优化目标，self-improvement是可能实现这个目标的一类机制。（Ren等，2026，§3 pp12–16；§8 pp50–52。）

**插入“综述覆盖边界”。**

> 项目页快照共有253个方法条目和59个评测条目；这里按目录行计数，不等于独立论文或免训练加速方法数量。评测项按主链接去重后为45个，并包含重复归类、judge和平台资源；ClawBench原目录还有错链，已从作者官方仓库更正。本文逐行筛查59项，对其中12篇高相关原文核查任务、反馈、重置及指标，其余只作明确标注的范围筛查。

**插入“验证环境选择”。**

> 最先要验证的是旧经验是否在质量不降的情况下节省未来任务的总成本。WorkArena的参数化企业操作、WebArena的可恢复自托管网站、AppWorld的跨应用API与状态差异检查分别提供不同切面。可先选其中一个主环境，再用ST-WebAgentBench测宏/脚本是否跳过必要约束；DiscoveryWorld或PhysGym用于隔离主动探索能否学到正确规则。Mind2Web/WebLINX提供的静态示范不能替代在线终局结果。OSWorld与ClawBench适合之后的真实执行验证；VM或浏览器profile重置不能被视为远端业务状态的完整回滚。

**插入“评测原则”。**

> 除成功率外，需要固定累计资源预算，记录版本演化曲线、留出任务迁移、先前能力回归和累计成本。轨迹复用、探索、工件提取、检索、执行、fallback及维护分别记账；模型调用、包装工具调用和底层动作分别统计。部署必要的反馈评价计入方法成本，独立最终评测单列。使用同模板新参数与留模板/留环境两种划分，避免把记住答案当成程序性迁移。方法的研究成本下降与部署任务加速属于两个不同结果。（综述§8；AppWorld、WorkArena、WebArena；AstaBench§4.2。）

## 4. Still-open：仍需实验或后续核验

1. **目录S行尚未原文深读。** 不能把59项都写成“全文验证”。RSI-Bench、WebCanvas来源资格尚未通过；不用于本文实质结论。其他S行也只支持初筛，不支撑具体数字/重置保证。
2. **没有运行benchmark。** 论文和代码可以说明设计，却不能代替我们在选定commit/环境中的重置、反馈可见性和计费实测。尤其WorkArena云状态清理、ST DB恢复、OSWorld远端依赖要做一次最小运行验证。
3. **源/版本变动仍可能发生。** Claw目录错误、ST摘要与PDF冲突已保留；最终实验必须固定论文版本、代码commit、task config、模型与judge版本，而非只记一个产品名称。
4. **探索的可用状态信息尚未确定。** 若我们可直接读DB，而baseline只看网页，那首先是接口/权限变化，不能当作经验学习净收益。AppWorld的API研究和WebArena的UI研究要分清。
5. **未来任务分布和复用频次须由研究问题决定。** 同模板新参数更贴近重复企业操作；跨站留出更难、回答另一种泛化问题。不能先挑最有利曲线，再事后定义复用频次。
6. **业务规则的真值与变化生成器尚未落实。** 科学方程规律、公开policy、运行时观察到的约束不是同一类知识。需定义哪些未知规则可被探测、哪些不能试错，以及更新后如何独立验证；不能把“规则型记忆”这个名称当已经解决。
7. **本轮未汇入全局E/D账本、未修改主报告。** 本文局部审计号只便于合并；主线程决定对应补丁与编号。

## References：实际作为证据使用的完整来源

以下编号仅属于本文，主报告可重排。正式venue与实际阅读版本分开；S类目录的完整题名/原链接已在59行表保留，它们不冒充本轮深入引用。所有网页/代码核验访问日为2026-09-30。

1. Zhe Ren, Yimeng Chen, Dandan Guo, Guowei Rong, Tonghui Li, R. B. Xiong, Qingfeng Lan, Wenyi Wang, Li Nanbo, Yibo Yang, Mingchen Zhuge, and Jürgen Schmidhuber. **Self-Improvements in Modern Agentic Systems: A Survey.** arXiv:2607.13104v1, 2026-07-14. [实际阅读PDF](https://arxiv.org/pdf/2607.13104v1)。Jilin/KAUST/Alberta/IDSIA等强机构preprint；未声称正式会议出版。姓名按实际PDF首页。

2. Harsh Trivedi, Tushar Khot, Mareike Hartmann, Ruskin Manku, Vinty Dong, Edward Li, Shashank Gupta, Ashish Sabharwal, and Niranjan Balasubramanian. **AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents.** Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp.16022–16076, 2024. DOI:10.18653/v1/2024.acl-long.850. [正式页及实际读本](https://aclanthology.org/2024.acl-long.850/)。

3. Alexandre Drouin, Maxime Gasse, Massimo Caccia, Issam H. Laradji, Manuel Del Verme, Tom Marty, David Vazquez, Nicolas Chapados, and Alexandre Lacoste. **WorkArena: How Capable are Web Agents at Solving Common Knowledge Work Tasks?** Proceedings of the 41st International Conference on Machine Learning, PMLR235:11642–11662, 2024. [正式页](https://proceedings.mlr.press/v235/drouin24a.html)，[实际阅读正式PDF](https://raw.githubusercontent.com/mlresearch/v235/main/assets/drouin24a/drouin24a.pdf)。2024原版，不混后续WorkArena++。

4. Shuyan Zhou, Frank F. Xu, Hao Zhu, Xuhui Zhou, Robert Lo, Abishek Sridhar, Xianyi Cheng, Tianyue Ou, Yonatan Bisk, Daniel Fried, Uri Alon, and Graham Neubig. **WebArena: A Realistic Web Environment for Building Autonomous Agents.** ICLR, 2024. [正式录](https://proceedings.iclr.cc/paper_files/paper/2024/hash/4410c0711e9154a7a2d26f9b3816d1ef-Abstract-Conference.html)。实际阅读[arXiv:2307.13854v4](https://arxiv.org/pdf/2307.13854v4)，2024-04-16。

5. Ido Levy, Ben Wiesel, Sami Marreed, Alon Oved, Avi Yaeli, and Segev Shlomov. **ST-WebAgentBench: A Benchmark for Evaluating Safety and Trustworthiness in Web Agents.** ICLR, 2026. [IBM正式出版记录](https://research.ibm.com/publications/st-webagentbench-a-benchmark-for-evaluating-safety-and-trustworthiness-in-web-agents--1)，[ICLR官方会议录目录](https://iclr.cc/virtual/2026/papers.html)。**实际读的后续版本署名为** Ido Levy, Ben Wiesel, Sami Marreed, Alon Oved, Avi Yaeli, Nir Mashkif, and Segev Shlomov，arXiv:2410.06703v7，2026-06-04，[PDF](https://arxiv.org/pdf/2410.06703v7)。本文375任务等数字来自后者；当前[官方代码](https://github.com/segev-shlomov/ST-WebAgentBench)补核反馈/重置模块。

6. Xiang Deng, Yu Gu, Boyuan Zheng, Shijie Chen, Sam Stevens, Boshi Wang, Huan Sun, and Yu Su. **Mind2Web: Towards a Generalist Agent for the Web.** Advances in Neural Information Processing Systems36, Datasets and Benchmarks Track, pp.28091–28114, 2023. [正式录](https://proceedings.neurips.cc/paper_files/paper/2023/hash/5950bf290a1570ea401bf98882128160-Abstract-Datasets_and_Benchmarks.html)。实际阅读[arXiv:2306.06070v3](https://arxiv.org/pdf/2306.06070v3)，2023-12-09；该PDF姓名写Samuel Stevens。

7. Xing Han Lu, Zdeněk Kasner, and Siva Reddy. **WebLINX: Real-World Website Navigation with Multi-Turn Dialogue.** Proceedings of the 41st International Conference on Machine Learning, PMLR235:33007–33056, 2024. [正式页](https://proceedings.mlr.press/v235/lu24e.html)，[实际阅读正式PDF](https://raw.githubusercontent.com/mlresearch/v235/main/assets/lu24e/lu24e.pdf)。作者个人常用拼写Xing Han Lù；引用按PMLR书目。

8. Tianbao Xie, Danyang Zhang, Jixuan Chen, Xiaochuan Li, Siheng Zhao, Ruisheng Cao, Toh Jing Hua, Zhoujun Cheng, Dongchan Shin, Fangyu Lei, Yitao Liu, Yiheng Xu, Shuyan Zhou, Silvio Savarese, Caiming Xiong, Victor Zhong, and Tao Yu. **OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments.** Advances in Neural Information Processing Systems37, Datasets and Benchmarks Track, 2024. [正式会议PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/5d413e48f84dc61244b6be550f1cd8f5-Paper-Datasets_and_Benchmarks_Track.pdf)。实际协议读本是较早[arXiv:2404.07972v2](https://arxiv.org/pdf/2404.07972v2)，2024-05-30；不声称等同后续Verified版本。

9. Yuxuan Zhang, Yubo Wang, Yipeng Zhu, Penghui Du, Junwen Miao, Xuan Lu, Zhuofeng Li, Xingwei Qu, Zhengkang Guo, Yuanzhe Shen, Dingjie Song, Han Zhou, Tuney Zheng, Xian Wu, Hao Yu, Songcheng Cai, Yi Lu, Yunzhuo Hao, Minyi Lei, Liang Chen, Kai Zou, Huifeng Yin, Wendong Xu, Dongfu Jiang, Ping Nie, Jiaheng Liu, Wenhu Chen, and Kelsey R. Allen. **ClawBench: Can AI Agents Complete Everyday Online Tasks?** arXiv:2604.08523v2, 2026-07-20. [实际阅读PDF](https://arxiv.org/pdf/2604.08523v2)，[作者官方代码](https://github.com/TIGER-AI-Lab/ClawBench)，[V1公开轨迹](https://huggingface.co/datasets/NAIL-Group/ClawBenchV1Trace)。强机构preprint；repo自报EMNLP2026 Findings，未在本次独立确认正式录。

10. Peter Jansen, Marc-Alexandre Côté, Tushar Khot, Erin Bransom, Bhavana Dalvi Mishra, Bodhisattwa Prasad Majumder, Oyvind Tafjord, and Peter Clark. **DiscoveryWorld: A Virtual Environment for Developing and Evaluating Automated Scientific Discovery Agents.** Advances in Neural Information Processing Systems37, Datasets and Benchmarks Track, 2024. [正式录](https://proceedings.neurips.cc/paper_files/paper/2024/hash/13836f251823945316ae067350a5c366-Abstract-Datasets_and_Benchmarks_Track.html)。实际阅读[arXiv:2406.06769v2](https://arxiv.org/pdf/2406.06769v2)，2024-10-07，首页仍标preprint，不改变已经独立核实的后续正式venue。

11. Yimeng Chen, Piotr Piękos, Mateusz Ostaszewski, Firas Laakom, and Jürgen Schmidhuber. **PhysGym: Benchmarking LLMs in Interactive Physics Discovery with Controlled Priors.** Advances in Neural Information Processing Systems38, Datasets and Benchmarks Track, 2025. [正式录](https://proceedings.nips.cc/paper_files/paper/2025/hash/42abcf9dffa48ca44fea1c497539a914-Abstract-Datasets_and_Benchmarks_Track.html)。实际阅读[arXiv:2507.15550v2](https://arxiv.org/pdf/2507.15550v2)，2025-10-26。

12. Xingyao Wang, Zihan Wang, Jiateng Liu, Yangyi Chen, Lifan Yuan, Hao Peng, and Heng Ji. **MINT: Evaluating LLMs in Multi-turn Interaction with Tools and Language Feedback.** ICLR, 2024. [正式录](https://proceedings.iclr.cc/paper_files/paper/2024/hash/8a0d3ae989a382ce6e50312bc35bf7e1-Abstract-Conference.html)。实际阅读[作者发布的会议PDF](https://zihanwang314.github.io/pdf/mint.pdf)，首页标ICLR2024及arXiv:2309.10691v3，2024-03-12。

13. Jonathan Bragg, Mike D’Arcy, Nishant Balepur, Dan Bareket, Bhavana Dalvi, Sergey Feldman, Dany Haddad, Jena D. Hwang, Peter Jansen, Varsha Kishore, Bodhisattwa Prasad Majumder, Aakanksha Naik, Sigal Rahamimov, Kyle Richardson, Amanpreet Singh, Harshit Surana, Aryeh Tiktinsky, Rosni Vasu, Guy Wiener, Chloe Anastasiades, Stefan Candra, Jason Dunkelberger, Dan Emery, Rob Evans, Malachi Hamada, Regan Huff, Rodney Kinney, Matt Latzke, Jaron Lochner, Ruben Lozano-Aguilera, Cecile Nguyen, Smita Rao, Amber Tanaka, Brooke Vlahos, Peter Clark, Doug Downey, Yoav Goldberg, Ashish Sabharwal, and Daniel S. Weld. **AstaBench: Rigorous Benchmarking of AI Agents with a Scientific Research Suite.** ICLR, 2026. [OpenReview论文页](https://openreview.net/forum?id=M7TNf5J26u)，[ICLR官方录目录](https://iclr.cc/virtual/2026/papers.html)。实际阅读[arXiv:2510.21652v2](https://arxiv.org/pdf/2510.21652v2)，2026-04-21。

14. Ren等综述作者团队. **Self-Improving Agents — Project Page / Research Directory.** 动态网页，2026-09-30下载快照。[项目页](https://selfimproving-agent.github.io/#overview)。仅用于目录身份、链接与条目计数，不替代原文方法和结果。
