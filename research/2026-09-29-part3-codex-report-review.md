# 第三部分研究计划报告（Codex 稿）的独立审阅

2026-09-29，Claude Code 会话。审阅对象：`notes/part3/2026-09-29-part3-research-plan-report-zh.md`（333 行，提交 83aaaa0，sha256 前 16 位 ce2edbbc7f3fbdc8）及其支持记录 `research/2026-09-29-part3-report-support.md`。审阅回答 Edwin 提出的四个问题：两个研究方向是否表达准确；相关工作的描述是否准确、候选贡献是否与已有研究重叠；第七章与 Time、Money 公式的衔接是否成立；哪些建议保留、修改或需要讨论。

**结论先行。** (1) 两个方向和总目标表达准确。要改的是几处归属：规则手册出题是 Edwin 的设想；“以质量为前提”“可重置的起点环境”“第一阶段只用既有日志”是方案建议，不是 Edwin 的要求（1.1）。(2) 对文献的描述大体可靠：23 篇文献的 147 处陈述里，3 处写错或只部分成立，另有 5 处是段末引用的位置问题，其中 4 处容易让方案自己的规则被读成文献结论；报告低估了与已有研究的重叠：问题一的大部分对照已有人做过，这些对照缺的是“相同且报告出来的改进资源”，而修改去向包含新 action 和环境条件、按实际耗时排序的诊断，在已核对的文献里没有找到（1.2 的 C1、1.3、D335）。(3) 第七章与 Time、Money 公式的衔接成立；要补的是账本边界和防重复计数的规则（1.4）。(4) 保留、修改、讨论各项见 1.5。所有“修改”都写进我方下一稿方案（`notes/part3/2026-09-29-part3-plan-claude-zh.md`），不改 Codex 报告。

**做了什么。** (1) 报告引用的 23 篇文献逐篇保存全文并重读，报告中关于文献的 147 处陈述逐条对照原文；(2) 第七章由两名互不知情的读者对照 `slides/build_deck.py` 和 `research/2026-09-28-problem-definition.md` 检查；(3) 三个研究问题分别对照本会话的核对库（读过全文的工作 314 项，其中 247 项符合来源规则并通过审计，共 2,923 条证据）查重叠。本文引用的每条文献细节都锁定到所读版本的具体行，先由脚本核对行内文字和数字，再由另一名读者独立尝试推翻；只有两步都通过的条目才进入第 1.6 节的证据表并获得 E 编号。本文写成后又经两轮独立审阅（对照条目、对照仓库、对照 Edwin 的原话），按其意见修改。

**没做什么。** 没有修改 Codex 的报告、slides 或 canonical dossier；没有计算预算；没有复现任何实验。没有单独评估报告第 41–47 行对“自进化改的是什么、做到哪一步”的回答，这个问题在我方方案稿第 3 节直接回答。

**引文方式。** 本仓库规则要求核对表给出原文引句。本文只给所读版本的章节、表号和行号，不抄录原文句子；逐条的原文锚点保存在仓库外的核对库中（位置见第 4 节）。这一点与规则有出入，在 Edwin 决定之前，本文按“只给位置”的方式提交，是否补引句由 Edwin 决定。

**来源类别。** 下文用四个标签区分说法的来源：**用户要求**（Edwin 在本会话或此前明确说过）、**Codex 建议**（报告作者的方案设计）、**文献结论**（论文自己报告的结果；表格中跟有证据编号的分句陈述的是文献结果，同一格里的判断、含义和建议属于我方建议）、**我方建议**（本审阅提出的修改；“修改”各行一律属于这一类）。Codex 直接从 Edwin 处确认过两个方向和“先定方案再算预算”（`research/2026-09-29-part3-claude-draft-crosscheck.md:17–19`，D314）；Edwin 在本会话中的其他说法（规则手册出题、权重不能改、只做过一轮等），Codex 只能通过我方前稿的转述和它自己的交叉核对看到，下文的归属判断以此为背景。

## 1 Verification table

### 1.1 两个研究方向是否表达准确

结论：两个方向和总目标表达准确，没有发现与 Edwin 意图相反的写法。有一处归属在压缩时丢失（规则手册出题的想法来自 Edwin），另有几处是 Codex 的方案设计，报告正文没有标明，容易被读成既定要求。

| 编号 | 报告位置与写法 | 来源类别 | 判断 |
|---|---|---|---|
| I1 | 第 9 行：两个方向（自动改进循环；从轨迹学环境并做成可复用 action），目标是在保持质量的前提下降低时间和费用 | 用户要求（两个方向，降低时间和费用）＋ Codex 建议（“保持质量的前提下”） | 两个方向准确。“以质量为前提”是方案建议，我方前稿也这样建议过，Edwin 没有明确说过；列入 1.5 的讨论项和第 4 节第 6 项。 |
| I2 | 第 13 行：Concur 或其他报销、申请、理赔平台都可作候选，研究对象是这类重复交互任务；建议从相对稳定、可重置、带明确业务规则的 Web 工作流开始 | 用户要求（Concur 只是例子）＋ Codex 建议（可重置的起点环境） | 前半准确，与 Edwin 的说明一致。后半要求一个可重置的环境，这正是 Edwin 质疑的“为什么需要专门的测试环境”，见 1.5“循环在哪个环境里跑”。 |
| I3 | 第 13、47、235 行：第一版固定任务模型权重；是否训练外层优化器留到后面；强化学习不排除 | 用户要求（权重不能改）＋ Codex 建议（分阶段） | 准确。Edwin 说强化学习是随口一提的想法、权重改不了；报告没有把强化学习写成既定路线，也没有排除。 |
| I4 | 第 21 行：人工分析轨迹后有时能找出问题并改好，但不能据此声称自动循环已经跑通 | 用户要求（背景） | 准确。Edwin 的背景是：在 Claude Code 里做过一轮，能找出问题并改掉；只做了一轮；暂不展示数字。报告没有引用数字，处理得当。 |
| I5 | 第 23 行：既读失败任务，也读成功但昂贵或缓慢的任务 | 用户要求 | 准确。Edwin 列举的错误包括明显的、经常犯的、最耗时间和费用的。 |
| I6 | 第 25 行：自动化的对象是改进流程中的人工干预；业务上必须问用户的询问另算 | Codex 建议，与用户要求一致 | 保留。Edwin 说过有些事情固定不成代码，每次都要询问或规划；这一行把两种“人的参与”分开，避免靠省略必要询问制造加速。Edwin 没有说询问的对象是谁（模型、环境或用户），我方方案稿把它列为待定。 |
| I7 | 第 79–87 行：修改位置表，含“保留运行时判断或询问” | 用户要求（四类去向）＋ Codex 建议（“补充或拆分环境条件”一行） | 准确。除“补充或拆分环境条件”一行外，其余四类去向与 Edwin 的说法对应；环境条件一行是 Codex 把方向二接进同一张表。另注：报告给“生成参数化 action”写的触发条件是“稳定操作重复触发逐步推理”，Edwin 说的理由是现有 action 要先失败才能到达，两者不同，我方下一稿两种都写。 |
| I8 | 第 31、93–99 行：固定环境不等于状态相同；区分“实际观察”与“归纳规则”；未观察到的保留为未知；第一阶段只用既有日志；显式图不是前提 | 用户要求（从轨迹提取环境知识）＋ Codex 建议（其余各点） | 内容合理。从轨迹里学到哪个按钮打开什么、字段有哪些选项，是 Edwin 的出发点；把第一阶段限定为只用既有日志、探索另设条件，是方案建议：我方前稿先提出“从已有轨迹开始、是否补做探索另定”（`research/2026-09-29-part3-claude-draft-crosscheck.md:25`），Codex 报告把它写成第一阶段的限定；需要 Edwin 决定。 |
| I9 | 第 105 行：规则手册支持测试构造，“这是另一份讨论草稿提供的候选思路” | 用户要求（报告标为另一份草稿的思路） | 归属需要改正。这个想法是 Edwin 提出的（由模型从规则手册推出情境和边角案例，例如规则禁止的 Airbnb 收据，生成数据，人工简单确认），我方草稿转述了它。Codex 的交叉核对已把这一项记为“草稿转述的新增用户设想”（`research/2026-09-29-part3-claude-draft-crosscheck.md:22`，D314），报告正文和 `research/2026-09-29-part3-report-support.md:34` 压缩时丢了这层归属，更正记入 D326。Edwin 同时强调它只检验对错，不是更新机制；报告把它放在验证层，与此一致。 |
| I10 | 第 107 行：用于开发和筛选的测试反馈属于优化信号，最终测试另行保留 | Codex 建议 | 保留。它与 I9 不矛盾：答案不是梯度，但用通过与否来决定保留或回滚，就已经在按这套题选版本，所以最终测试必须是没参与过选择的题。报告段末的 [20] 跟在“抽样核对判分”一句之后，支持的是判分器会误判（见 C11），不涉及这条规则；这条规则是方案自己的方法要求，见 1.2 的 N6。 |
| I11 | 第 15、174、235 行：现阶段不填预算 | 用户要求 | 准确。 |
| I12 | 第 237 行：不预先承诺全自动持续优化的通用平台 | Codex 建议 | 与 Edwin 的目标不冲突。Edwin 要的“全自动”指分析、修改、重试这个循环不用人；报告第 25 行的范围与此相同。我方下一稿写明这一点，避免读者以为目标降低了；Codex 报告不改。 |

### 1.2 对相关工作的描述是否准确

**总体。** 报告标为正式发表的 10 篇在会议官方页面上确认；其余 13 篇报告按预印本列出，其中 SOPBench [21] 已列入 EMNLP 2026 主会官方日程（论文集尚未出版），报告的“正式发表未独立确认”需要更新。147 处陈述中，83 处成立，56 处成立但缺少会改变读法的条件，8 处需要修改：3 处是文献描述写错或只部分成立（N1–N3）；5 处是段末引用的位置问题（N4–N8），其中 4 处挂在报告自己标明的方案规则或候选思路上，容易被读成文献结论，1 处（N4）把 ReasoningBank 的 [17] 挂在 SoL-Pi 和 RRSI 一句后面；这 5 处报告的说法本身没有错。10 篇正式发表中，LearnAct 的“main conference”限定未核实（第 4 节）。需加条件的 56 处中，对方案影响最大的列在其后。

**逐篇统计。**

| 报告文献 | 工作 | 本次所读版本 | 发表信息 | 成立 | 需加条件 | 需要修改 |
|---|---|---|---|---|---|---|
| [1] | AgentOptimizer | arXiv v4 | ICML 2024（PMLR 235），官方页面已核 | 6 | 1 | 0 |
| [2] | GEPA | arXiv v2 | ICLR 2026 主会（Oral），官方页面已核 | 3 | 2 | 0 |
| [3] | Darwin Gödel Machine | arXiv v2（另对照 v3） | ICLR 2026 主会（Poster），官方页面已核 | 4 | 2 | 0 |
| [4] | HarnessFix | arXiv v2 | 预印本，已核 | 9 | 3 | 0 |
| [5] | StarHarness | arXiv v1 | 预印本，已核 | 6 | 5 | 0 |
| [6] | DarwinX | arXiv v1 | 预印本，已核 | 4 | 1 | 0 |
| [7] | Harness-R1 | arXiv v1 | 预印本，已核 | 2 | 1 | 0 |
| [8] | AutoManual | arXiv v4 | NeurIPS 2024 主会，官方页面已核 | 2 | 4 | 0 |
| [9] | AutoGuide | arXiv v2 | NeurIPS 2024 主会，官方页面已核 | 3 | 1 | 0 |
| [10] | Agent Workflow Memory | arXiv v1（另对照 ICML 正式版） | ICML 2025（PMLR 267），官方页面已核 | 2 | 3 | 1 |
| [11] | LearnAct | arXiv v2 | COLM 2024，官方录用名单已核；“main conference”未核实 | 2 | 2 | 0 |
| [12] | WALT | arXiv v1（另对照 ICLR 正式版） | ICLR 2026 主会（Poster），官方页面已核 | 5 | 3 | 0 |
| [13] | SkillWeaver | arXiv v1 | 预印本，已核 | 2 | 2 | 0 |
| [14] | ActionEngine | arXiv v2 | 预印本，已核 | 5 | 3 | 0 |
| [15] | AppAgentX | arXiv v3 | 预印本，已核 | 4 | 2 | 0 |
| [16] | SpeedRunner | arXiv v1 | 预印本，已核 | 5 | 4 | 1 |
| [17] | ReasoningBank | arXiv v2 | ICLR 2026 主会（Poster），官方页面已核 | 3 | 1 | 2 |
| [18] | SoL-Pi | arXiv v1 | 预印本，已核 | 2 | 1 | 0 |
| [19] | RRSI | arXiv v2 | 预印本，已核 | 2 | 2 | 0 |
| [20] | AgentRewardBench | arXiv v2 | COLM 2025，官方录用名单已核 | 3 | 2 | 1 |
| [21] | SOPBench | arXiv v2 | 预印本；已列入 EMNLP 2026 主会官方日程，论文集尚未出版 | 2 | 5 | 2 |
| [22] | LogiSafetyGen / LogiSafetyBench | arXiv v1 | 预印本，已核 | 6 | 3 | 1 |
| [23] | On the Fragility of Self-Improving Agents | arXiv v2 | 预印本，已核 | 1 | 3 | 0 |

**需要修改的 8 处。**

| 编号 | 报告位置与写法 | 原文实际情况（所读版本与位置） | 判断 |
|---|---|---|---|
| N1 | 第 51 行：AWM“将历史流程转成可调用的文字工作流”[10] | 标准 AWM 把工作流加进提示中的记忆，动作仍由模型逐步生成 [E324]；只有变体 AWM_AS 把工作流封装成可调用的高层动作，在 Mind2Web（gpt-4）上只在 18.5% 的任务中被调用，步骤成功率略升，任务成功率没有提高（正文与表的数字不一致）[E325]；工作流含自然语言描述和推理，每步动作默认写成程序格式 [E326]，在 Mind2Web cross-task 上，把动作改写成文字的变体与默认格式的表现没有实质差别 [E327] | 部分成立。“可调用”不对；“文字”只对一部分。报告同句后半（文字工作流不等于可执行程序，不能省去模型推理）与原文一致。 |
| N2 | 第 57 行：因为 SpeedRunner，“画累计成本曲线”不是空白 [16] | 论文报告的是每条轨迹的成本，归纳调用按所在批次摊入其中 [E328]；主要结果图 3 的效率口径前后不一致：§4.3 定义为每条轨迹的输出 token，附录 A.3 说图 3 用按公开价格折算的美元 [E329] [E330]（与 D172 一致）。我在所读版本中没有找到累计成本曲线 | 对 [16] 不成立。“每条轨迹平均成本随学习下降”在三个非网页基准上有先例 [E331]；“累计投入对累计节省”的曲线在所读版本（arXiv v1）中没有找到。回本核算在别的工作里有，但都是一次性建设或设计成本 [E332] [E333] [E334]。 |
| N3 | 第 61 行：ReasoningBank 的结果说明“记忆构建、检索和额外上下文也会产生开销”[17] | 成本表中多出来的 token 来自判分和经验提取两类调用 [E335]；动作生成一栏低于无记忆基线 [E335] [E336]；成本表只有动作生成、判分、经验提取和合计四栏，没有检索一栏 [E336]，表注也没有写明基准和模型 [E335] | 部分成立。“记忆构建（判分和提取调用）带来开销”成立；检索和额外上下文没有单列，动作生成一栏反而更低，不能说它们带来了可见的净开销。 |
| N4 | 第 61 行段末引用 [17][18][19] | 报告这一句已点名 SoL-Pi 和 RRSI；ReasoningBank 的记忆只追加不删减 [E337]，按成本选取记忆被作者列为未来方向 [E338] | 引用位置可改进，说法本身成立：把 [17] 移到 ReasoningBank 那一句后面更清楚。 |
| N5 | 第 105 行：“由模型提出覆盖不同条件的案例”，段末 [21][22] | 报告已写明这是另一份讨论草稿的候选思路。SOPBench 中“模型生成案例、程序校验、人工复核”的分工成立 [E339] [E340]，但要覆盖哪些条件组合由程序枚举 [E341]；LogiSafetyGen 中模型从法规文本提取候选规则并撰写指令 [E342]，合规的参考轨迹由逻辑引导的搜索程序生成 [E343] [E344] | 引用位置需要调整，说法本身没有错。两篇都不是由模型直接提出覆盖不同条件的案例；Edwin 设想的“模型从规则手册推出情境和边角案例，人工简单确认”在这两篇里只有部分对应，在已核对的文献里没有完整先例。 |
| N6 | 第 107 行：段末引用 [20]，段中含“最终测试必须另行保留”的规则 | [20] 紧跟“抽样核对判分”一句，支持的是判分器会误判 [E345] [E346]；AgentRewardBench 为评测判分器划分了开发集和测试集 [E347] | 引用位置有歧义。留出规则是方案自己的方法要求，不是 [20] 的结论，写明即可。 |
| N7 | 第 105 行：“生成器不能修改已确认的规则、判分程序或预期答案”，段末 [21][22] | 两篇是构造基准，不涉及改进循环 [E348] [E349]；SOPBench 中生成的数据须通过固定的校验程序，不符合就重新生成或人工修正 [E350]，与这条规则一致 | 引用范围问题，说法本身没有错：这是方案自己的设计规则，与 SOPBench 的分工一致，写明即可。 |
| N8 | 第 105 行：预期结果“也可以包含”必须询问、必须拒绝、不得跳过，段末 [21][22] | “必须拒绝”和“不得跳过”有部分对应 [E351] [E352]；“必须询问”在两篇中都没有：SOPBench 的用户请求在开头一次给出，之后只在 agent 停止调用工具时重发用户已知信息 [E353]；LogiSafetyBench 中被测模型的任务是生成一段 Python 程序 [E354]，规则模板只约束 API 调用的先后顺序 [E355] | 引用位置问题。报告说的是方案设计；其中“必须询问”与 Edwin 说的“有些事每次都要询问或规划”一致（询问对象未定，见 1.5），属于用户要求。“必须询问”的检查要我方自己设计。 |

**成立但缺少关键条件的陈述（节选，按对方案的影响排序）。**

| 编号 | 报告位置与写法 | 缺少的条件（所读版本与位置） | 对方案的含义 |
|---|---|---|---|
| C1 | 第 119 行：问题一“首先是目标场景中的前置验证，因为 HarnessFix 已有明确的诊断和修改路由” | HarnessFix 在 GAIA、SWE、AppWorld、TB2 上（GPT-5 mini）做过相近的对照：只改提示、去掉基于轨迹的诊断、去掉验收检查，三者都低于完整方法 [E356] [E357]；诊断质量对照人工标注有测量（每个基准 20 条失败轨迹）[E358]；相对通用修改器 Meta-Harness，任务完成率高 2.6–5.0 个百分点，离线修复 token 更少 [E359] | 在这四个基准上，问题一的大部分对照已有人做过；剩下的是“相同改进资源”这个条件，所引条目没有报告各消融变体的资源用量。其余缺口见 1.3。 |
| C2 | 第 43 行：HarnessFix“通过验证集回归检查筛选修改”[4] | 失败识别用到外部评测结果 [E360]；候选补丁要在留出的验证集上重跑，达到目标改善且退化不超限才接受 [E361]。另一项工作里，没有单元测试反馈时执行框架演化没有胜过直接采样 [E362] | 这类循环依赖可靠的对错信号，正是 Edwin 的答案库要提供的东西。 |
| C3 | 第 43 行：StarHarness“在企业任务中演化执行框架”[5] | AutomationBench 是 47 个模拟应用上的财务流程任务，按环境状态的程序断言评分 [E363]；EnterpriseOps-Gym 上的修补针对 MCP 参数处理和接口 schema [E364]。失败诊断由提议模型读搜索任务的轨迹和结果来做 [E365]；作者说明在 AutomationBench 上无法分离单个工具的贡献 [E366] | 它是企业场景的近邻。按我的阅读，它的三个基准都不是浏览器页面操作；论文没有报告诊断准不准。 |
| C4 | 第 45 行：StarHarness“部署 API 费用另行报告”[5] | 报告的是按公开价格估算的每任务推理费用，三个基准上分别降低 17%、53%、29% [E367]；选择目标是平均任务分数，论文把它叫作 cost function [E368]；在 EnterpriseOps-Gym 的全部 103 题（含演化用题）上，这个只看分数的循环同时把每题轮数从 18.12 降到 9.87、工具调用从 29.53 降到 16.83 [E369] | 针对耗时和费用的诊断要比的对手，是一个只看分数却已经顺带省钱的循环。 |
| C5 | 第 47 行：Harness-R1 说明强化学习是可选路线 [7] | 它依赖基准自带的奖励 [E370]、上万条训练任务 [E371]、教师模型冷启动 [E372] 和 GPU 训练 [E373]；拿来比较的不训练的编辑模型都不重跑目标 agent [E374]；在留出任务协议下（冻结的 Qwen3.5-9B 目标，每个编辑器看同样 10 条失败写一个补丁，三个种子），Qwen3.5-397B 和 DeepSeek-V4-Pro 作编辑器的平均变化为 −4.3±2.5 和 −0.4±3.6 个百分点，Harness-R1 为 +8.9±1.5 [E375] | “第一版不训练”是方案自己的选择，[7] 没有检验过它够不够用。 |
| C6 | 第 53 行：WALT 和 SkillWeaver“学习、测试并修复可复用工具”[12][13] | WALT 的工具在离线探索网站时构建：先由 agent 演示每项功能，再从演示轨迹生成工具 [E376] [E377]；测试输入由构建工具的 agent 从演示轨迹中取出 [E378]，失败反馈用来修选择器、输入 schema 和脚本 [E379]；上线后的在线修补列为未来工作 [E380]。SkillWeaver 的“通过验证”指调用时不抛异常，作者报告这有时让屏蔽了异常的坏函数也被标为通过 [E381] | 两篇都不是“从任务轨迹诊断后再改”，与方向一只部分重叠；“测试通过”不等于业务正确。 |
| C7 | 第 55 行：ActionEngine“构建环境状态机记忆”[14] | 状态机来自对线上应用的离线爬取，构建时不看后面要做的任务 [E382]（预热和关闭 Patcher，报告第 55 行已写明 [E383] [E384]） | 报告把 ActionEngine 对应“环境表示”，没有说它来自既有轨迹；要补的是它靠专门探索建模型，不是“从既有轨迹建环境模型”的先例。 |
| C8 | 第 55、219 行：AppAgentX“构建参数化快捷动作”“支持程序化动作”[15] | 是否生成快捷动作由模型判断 [E385]；论文描述的唯一反馈是运行时条件不满足或出错就退回基本动作 [E386]；快捷动作在记忆里存成带顺序的基本动作及其参数 [E387]，每次使用时由模型判断能否执行并生成执行模板 [E388] | 论文没有描述“验证后才采用”的步骤。 |
| C9 | 第 57 行：SpeedRunner“考虑技能归纳成本的摊销”[16] | 实验在 ScienceWorld、BabyAI、Crafter 三个基准上 [E331] [E389]，作者说明因为费用没有在 SWE-Bench、Terminal-Bench 这类更贵的基准上评测 [E390]；轨迹是 agent 自己的在线运行，每 10 次运行做一次技能更新 [E329]；不回放任务，也没有用留出的运行来评价技能更新，是否退化交给归纳模型对照按版本存储的轨迹判断 [E391]；主要结果图 3 的成本口径论文前后不一致（输出 token 或按公开价格折算的美元）[E329] [E330] | 所读版本里没有网页任务上的结果，也没有基于留出运行的验收门。 |
| C10 | 第 61 行：SoL-Pi 和 RRSI 已把质量与效率约束纳入改进过程 [18][19] | SoL-Pi 的质量约束是容忍度 [E392]，被接受的完整组合在 EdgeBench 和 Terminal-Bench 4 上得分低于基线 [E393] [E394]，作者说明完整的搜索循环计算开销很大 [E395]；RRSI 只接受演化集收益超过噪声带、且 token 增幅不超过随收益放宽的上限的候选 [E396]，在 agentic-workspace 实例上没有哪个演化后的版本比初始版本省 token [E397]；两者的效率指标都是 token 或费用 [E392] [E396] | “按效率筛选”有先例，但 SoL-Pi 允许质量在容忍度内下降，RRSI 允许 token 随收益增加，都不保证执行成本低于基线；用墙钟时间做筛选条件的，在已核对的文献里没有找到。 |
| C11 | 第 63、107 行：AgentRewardBench 显示自动判分器会误判 [20] | 模型判分器倾向于高估成功 [E345]，基于规则的判分倾向于低估 [E346]；标准答案是专家对全部轨迹的标注，不是抽样 [E347] | 抽样复核是方案自己的设计，[20] 没有检验过抽样是否足够。 |
| C12 | 第 63 行：SOPBench 为从规则构造测试情境提供了参考 [21] | 服务函数、约束和校验程序都由人工设计并写成程序 [E340] [E398]；只覆盖能写成代码的前置校验 [E399]；预期结果由程序执行得出 [E400] | 从自然语言规则手册到可判分的答案，中间把规则写成服务函数、约束和校验程序的一步，在这篇里是人写的。 |
| C13 | 第 154 行：已有研究指出自改进评估对顺序、方差和未明确条件敏感 [23] | 主要实验比较的是 AWM 和 ReasoningBank 两种基于记忆的方法，每个实验重复三次 [E401] [E402]；默认顺序下 ReasoningBank 略有提升，打乱顺序后变成下降 [E403]；记忆构建时给的是真值奖励 [E404] | [23] 支持这一句的方差和顺序部分 [E401] [E403]；它指出的顺序效应是默认顺序隐含着由易到难的安排 [E403]。前一句“恰好先遇到关键页面”没有引用，是报告自己的例子。 |
| C14 | 第 41 行：GEPA“根据执行反馈演化提示”[2] | 反馈是反馈函数给出的分数和文字，评分对照的是标准答案、评分细则或单元测试 [E405] [E406]；优化器可以使用训练集的全部内容和标注 [E407]；修改对象只有提示 [E408] | 第 39 行的小标题“已扩展到可执行系统”不适用于 GEPA。 |
| C15 | 第 218 行：WALT“已包含学习过程和建设代价”[12] | 报告所读的 arXiv v1 只把逐站探索和验证的开销列为局限，没有给数字 [E409]；数字在 ICLR 正式版中 [E333] | 版本问题，见 D327。 |

### 1.3 候选贡献与已有研究的重叠

报告对重叠的总体判断是对的：宽泛的说法不能当创新点。问题在于它低估了重叠的程度，因为有几项最接近的工作没有进入报告，其中 ASI、EchoPath 和预算对齐研究就在当前 PPT 的主线上；主线上的页面裁剪程序按来源规则暂缓，报告不引用它与来源规则一致。

**报告没有提到的近邻。**

| 工作 | 在哪里 | 与哪个研究问题重叠 |
|---|---|---|
| ASI | PPT 主线 t04（`slides/build_deck.py:1423`），E229 | 方向二：从 agent 的运行轨迹归纳程序技能，用改写后的轨迹重跑同一查询，只有模型裁判判为完成、新技能被调用且调用改变了环境时，才把实际被调用的技能加入 action [E410] [E411] |
| EchoPath | PPT 主线 t03（`:1409`）、附录 b1-1（`:1634`） | 方向二：只有通过外部评测的首次运行轨迹才存成带参数的可调用记忆，回放前做兼容性检查，不兼容就拒绝并给出原因 [E412] [E413] [E414] |
| AutoSaddler | 核对库 w006 | 问题一：诊断加补丁，在测试集上对照 GEPA 和 Meta-Harness [E415]；在 GAIA2 开发集上（每种方法一次优化运行，Meta-Harness 的优化集包含开发集），AutoSaddler 约 1,000 次任务执行达到 72.3%，GEPA 和 Meta-Harness 约 2,800 次后停在 64.6% 和 61.5% [E416] |
| Agentic Harness Engineering（AHE） | 核对库 w009 | 问题一：由模型选择修改层级（提示、工具、中间件）[E417]，对照 ACE 和 Training-Free GRPO [E418] |
| Meta-Harness | 核对库 w004 | 问题一的“通用修改器”对照组；在文本分类任务的执行框架搜索中（USPTO、Symptom2Disease、LawBench），给提议模型看完整执行轨迹时候选的中位准确率为 50.0，只看分数加摘要时为 34.9 [E419] |
| 对 harness 演化的重新评测 | 核对库 n004 | 问题一、三：在 Terminal-Bench 2.1 上，各方法的轮数和每题采样数相同（K=5，m=1；未报告 token、金额或时间）[E420]；在 34 道留出测试题上，演化出的 harness 相对初始版本只高 +1.2（Claude Opus 4.6）和 +0.0（GPT-5.4）个百分点 [E421]；用单元测试作反馈和最终挑选时，并行采样的平均 pass@1 更高 [E422] |
| SKILL.nb | 核对库 w035 | 问题二：带门控条件的可执行步骤加文字回退 [E423]，有维护 token [E424] 和版本漂移实验 [E425] |
| 环境探测整理记忆 | 核对库 w054 | 问题二：经环境核实的记忆对比只靠轨迹的记忆 [E426]；整理开销没有计入 [E427] |
| 预算对齐研究 | PPT 主线 t04（`:1425`，“Plain agent, 15 steps”一行），D171；核对库 w013 | 问题二、三：在 WebArena 四个站点上，与在线的技能和记忆模块相比，放宽步数上限并加了规则页面裁剪的普通 agent 在三个模型上平均成功率都最高，在 Gemini 3 Flash 上每题 token 也最少 [E428] [E429]；预算只按步数上限近似对齐 [E428]；作者说明结论只针对在线模块 [E430] |
| PolicyBank | 核对库 n016 | 问题二：带触发条件和前置条件的记忆条目 [E431] 对比文字经验 [E432]；对象是客服政策，不是环境 |
| CostCraft | 核对库 g037 | 问题一：去掉成本归因的消融 [E433] |
| 开放式优化（OEO）与 CASD | 核对库 g049、g047 | 问题一：在一项技能优化研究里（GPT-5.5 作优化器，每个设置只跑一次），不规定流程的做法在多数比较中胜过规定流程的方法 [E434]；换成中等模型，在仅有的两个任务上相反 [E435]。另一项工作里，现成的 coding agent 在数据有限的设置下平均增益高于两种搜索方法 [E436] |
| 元 agent 的经济性 | 核对库 g118 | 问题三：计入设计成本后，只有少数设置能回本 [E334] |
| WALT 正式版的建设成本 | PPT 主线 t04（`:1424`）已采用；核对库 h008 | 问题三：一次性建设的回本点，只针对 Online-Mind2Web [E333] |

**逐个研究问题的判断。**

| 研究问题 | 已有人做过的部分 | 在已核对的文献里没有找到的部分 | 对报告写法的意见 |
|---|---|---|---|
| 问题一：按轨迹证据选择修改位置是否有价值 | 自动选择修改位置并对照人工标注量过准确度 [E358]；同一系统内去掉轨迹诊断的消融 [E356]；只改文字的对照基线和去掉失败定位的消融都低于完整方法（MiniWoB，两种模型）[E437]；与只改文字的方法和通用修改器的跨系统对照 [E359] [E415] [E418]；按频率和失败率选目标 [E438]；去掉成本归因的消融，单个种子 [E433] | (a) 固定循环、提议模型、轨迹访问权限和预算，只开关“选位置”这一项（同一系统内去掉诊断或失败定位的消融已有 [E356] [E437]，但所引条目没有报告资源用量）；(b) 修改去向里包含新 action、环境条件、留给运行时或询问；(c) 按实际耗时排序的诊断；(d) 以墙钟时间或金额计的“多快找到不退化的版本”；(e) 有状态、受规则约束的网页填报流程 | 第 11 行把“能否选对修改位置”写成开放问题，偏弱：在 GAIA、SWE、AppWorld、TB2 上，这一步已被自动化，并对照人工标注测量过 [E358]；第 45 行问的是针对耗时和费用的诊断：按费用归因已有一项单种子的消融 [E433]，按实际耗时排序的诊断在已核对的文献里没有找到，这部分可以保留。第 119 行只提 HarnessFix，应同时说明对照已有人做过（但系统之间的差别不止一处），并写出反面证据：一项 2024 年的提示词优化研究里（BigBench 四个任务，Llama-2-70B-chat 为目标模型，GPT-4 为优化器），假的错误样本在其中三个任务上与真的效果相当 [E439]；在一项技能优化研究里（GPT-5.5 作优化器，每个设置只跑一次），不规定流程的做法在多数比较中胜出 [E434]。 |
| 问题二：显式环境条件是否值得维护 | 带条件的记忆条目 [E431]；使用前按出处核对（GitHub 官方博客，非同行评审）[E440]；整理记忆时用环境探测核实 [E441]；门控代码加文字回退 [E423]；在 OSWorld-W 上用 GPT-5 时，把导航知识写进提示词成功率无显著变化（42% 对 44%），作者据此认为增益主要来自声明式接口 [E442]；在三种专用 harness 配置上，agent 自写并单独使用的技能低于不用技能 [E443] | (a) 同一批日志上三组对照（文字经验、直接技能、带出处和条件的知识层）；(b) 把“错误复用”和“无效往返”定义成指标；(c) 把“未知”作为知识的一个字段；(d) “知识只来自任务轨迹、持续维护的开销与运行节省对齐比较”的组合。单独从任务轨迹学习已有先例 | 第 57 行的差异表述偏强：SKILL.nb、w054、PolicyBank、Copilot 已各做到其中一部分（Copilot 一项的来源资格待定，见第 4 节第 9 项）。报告第 142 行的“直接生成技能”对照已保留同样验证与基础回退，这一点是对的；还缺的是预算对齐的普通 agent 对照，即把改进投入换成更宽的步数上限或页面裁剪的同一 agent [E428] [E429]。 |
| 问题三：自动改进是否带来可持续的净收益 | 一次性建设或设计的回本点 [E332] [E333] [E334]（ActionEngine 的回本点不含预热修正的开销，而主要结果用的是预热后的状态机 [E383]）；任务流中每次成功的维护 token [E424]；版本升级后沿用旧知识对比从头开始 [E425]；注入数据结构变更的任务流 [E444]；把构造或修改改动的调用与任务运行分开计 token，候选验证的运行记在任务运行一边 [E445] [E446] | 同时做到以下几点的工作：沿任务流累计改进开销（含持续维护）和执行开销；与预算对齐的同一 agent 比较；以金额报告回本任务数；用户等待时间单独报告；环境或规则变更后重新测量回本点 | 报告第 11 行已限定为“已评测设定”，并在同段和第 65 行把净收益列为未回答的问题。要补的是：限定为有可靠对错信号的设定；计入改进自身开销的报告很少，其中一次性建设有回本点 [E332] [E333]，自动设计 agent 只在少数设置里回本 [E334]；持续运行的改进循环连同维护开销能否回本，在已核对的文献里没有找到，见 D334。第 123 行没有写出近邻，也没有定义“合理使用量”。 |

说明：核对库中 PRISM、DARC、REBASE 等几项工作与问题一、二直接相关，但按 Edwin 的来源规则被判为暂缓或排除（作者全部来自普通公司，或未核到合格机构），本文不把它们用作依据。

### 1.4 第七章与 Time、Money 公式的衔接

结论：衔接成立。两条公式与 `slides/build_deck.py` 中的写法符号和结构相同，只差排版间距（`:136`、`:141`），符号解释与第 2、3 页和附录 A0 相符，表中每项工作在 PPT 里的位置都核对无误；没有强行让方案覆盖公式的每一项。要补的是记账：报告第 199–203 行已提醒不同粒度的描述不能相加，但还缺防重复计数的具体规则（F3–F5、F7）；代价一列缺 action 内部的模型调用，并把单次执行开销和知识维护混在一起（F4、F6）；三个账本的边界还不能保证每个数字只进一次（F1）。

| 编号 | 报告位置 | 问题 | 依据 | 严重程度 |
|---|---|---|---|---|
| F1 | 第 170 行（三个账本） | 账本已命名，但规则留下了可以进两本账或一本都不进的数字：“学习维护或执行开销”中的“或”；“准备”在分子里但不属于任何账本；对照组自己的学习开销是否计入；在真实业务任务上运行的候选版本既产出结果又做验证；同一套规则测试既用于验收又用于最终测试；人工小时没有账本 | 报告第 105、107、166、170、209 行；`build_deck.py:1767–1768` | **必须补**。问题三的净收益结论依赖这些边界。 |
| F3 | 第 194 行（第一行） | 表中“无效 N”和“轮内重试 Jᵢ”指的是不同的调用，不重复；报告第 199–203 行也已说明这张表是因果路径，并提醒了成功率这条关联。还缺一条记账规则：少走错误路径同时降低每次尝试的开销、提高成功率时，每成功收益只用全部尝试的实测总额除以成功数，不把两项估计相加（D332 第 2 条） | `build_deck.py:909`；`problem-definition.md:216`、`:333–334` | 应补规则。 |
| F4 | 第 196 行（第三行） | 避免一次试探性操作，通常整轮都消失，不只是非模型时间；这笔节省又已被第一行的“少走错误路径”认领。代价一列把每次执行内的开销和“知识维护”（学习账本）混在一起 | `build_deck.py:455–460`；报告第 207–209 行 | 应改。 |
| F5 | 第 195、197 行（第二、四行） | 一个 action 执行多次点击并返回紧凑结果时，第二行（少了中间调用）和第四行（上下文变短）认领的是同一批输入 token | `build_deck.py:1447`；`problem-definition.md:308–316` | 应改。 |
| F6 | 第 194–197 行 | 代价一列已列出更长提示、额外裁判调用、条件检查与回退的费用、工具说明与记忆增大上下文、修改前缀影响缓存。缺的是 action 内部的模型调用（例如费用归类判断，报告第 113 行在例子里提到了，表里没有），以及回退时恢复所需的额外轮次记在哪一行 | `build_deck.py:1416`、`:1423`；报告第 113 行 | 应补。 |
| F7 | 第 199 行 | “减少调用会省去被移除调用的耗时”只在调用串行时成立。D 和 E 是时长相加，并行调用之间重叠的时间记在 T_saving 里；删掉一个并行调用，墙钟时间可能几乎不变 | `build_deck.py:892`、`:460`；`problem-definition.md:33` | 应改。第 188 行也没有解释 T_saving。 |
| F8 | 第 123 行（问题三） | “时间与费用抵消”只能用金额定义。离线改进耗时不是用户等待时间，报告自己的第 168 行也这样说 | 报告第 166、168、174 行；`build_deck.py:1768` | 应改。 |
| F9 | 第 168、174 行 | 没有考虑后台学习的墙钟时间：一轮改进在跑的时候，任务仍按旧版本到达。如果模拟时默认每轮改进在下一个任务前生效，早期节省会被高估。这一条是我方推理，仓库文件里没有直接依据 | 报告第 154、168、174 行 | 应补。 |
| F10 | 第 166 行 | 每成功费用按研究用判分器统计的成功数来除，而部署系统没有这样的判分器；失败任务是重试还是交人工，决定了每成功费用是否等于每任务费用；零成功时，PPT 公式的来源文档 F15 定义为无穷大，PPT 页面没有写这一情形，报告写的是“未定义” | `build_deck.py:909`、`:1768`；`problem-definition.md:210`、`:507`、`:515` | 应改。 |
| F11 | 第 215–221 行（近邻位置表） | 位置都对，但漏了 PPT 主线上的 ASI、EchoPath 和预算对齐研究（`:1425`）（页面裁剪程序按来源规则暂缓，不算遗漏）；AutoDroid-V2 被写成“学过的脚本”，而 PPT 写的是依据离线构建的应用文档、每个任务现写一个脚本 | `build_deck.py:1423`、`:1409`、`:1425`、`:1408`、`:1633` | 应改。见 D333、D331。 |
| F12 | 第 162 行 | 运行费用一行没有列出按用量计费的环境 x_env·c_env；候选验证用的可重置测试环境应记入学习维护账本 | `build_deck.py:141`、`:732` | 可选。 |
| F13 | 第 176、180、188 行 | 公式属于第一部分，第二部分沿用；报告写成“前两部分的框架” | `build_deck.py:1396` | 可选。 |

编号从 F1 跳到 F3：原 F2 不是报告的问题，移到下面。

顺带发现（不属于报告的问题）：

- 报告对 i = 0 的读法与 PPT 页面一致，没有问题；冲突在仓库文件内部：`research/2026-09-28-problem-definition.md` 的 F1(e) 把“摊销的学习调用”放进 i = 0，F14(g) 又把它排除在费用之外，见 D321。
- PPT 第二部分第 3 页的面包屑（`build_deck.py:1401`）和附录 b0-3 的 LATM 一行（`:1620`）仍指向“第 14 页”，而第二部分的第 14 页现在是参考文献页。本次没有修改 slides。

### 1.5 保留、修改、需要讨论

说明：本节“修改”指我方下一稿采用这些内容时的改法，不改 Codex 报告。“来源类别”一栏标的是报告原内容的出处，“修改”各行一律为我方建议；“说明”一栏中带证据编号的分句是文献结论，判断和建议是我方建议。

| 类别 | 内容 | 报告位置 | 来源类别 | 说明 |
|---|---|---|---|---|
| 保留 | 自动化对象是改进流程中的人工干预，业务询问另算 | 第 25 行 | Codex 建议 | 见 I6。 |
| 保留 | 分析器输出的是待验证的假设，附支持轨迹、反例和能区分不同原因的检查 | 第 73 行 | Codex 建议 | 与 HarnessFix 的做法相容；HarnessFix 的定位准确度有测量但不是满分 [E358]。 |
| 保留 | 设置通用修改器对照；只有专门的诊断在相同资源下更有效，才保留分类和路由 | 第 89、137 行 | Codex 建议 | 我方建议对照组要给同样的原始轨迹访问权限，否则比的是信息量：在一项文本分类的执行框架搜索里，看完整轨迹的提议模型得到的候选更好 [E419]。分类是 Edwin 要求的一环，对照组同样好时是否仍保留，由 Edwin 决定。 |
| 保留 | 区分实际观察与归纳规则，记录出处；没观察到的保留为未知 | 第 93 行 | Codex 建议 | 在已核对的文献里没有找到把“未知”作为一个字段来测量效果的工作；这只说明已核对范围内没有先例，不作为新颖性的依据。 |
| 保留 | action 契约：输入参数、适用条件、执行过程、预期效果、异常出口；动态数据存读取方法 | 第 95 行 | Codex 建议 | 近邻有 ContractSkill [E437] 和 SKILL.nb [E423]。 |
| 保留 | 开发、筛选、最终测试三类任务分开；学习曲线用事先冻结的检查点统一测 | 第 150 行 | Codex 建议 | 与 I10 的关系：Edwin 说答案库只检验对错，按通过与否选版本仍然会影响留下哪个版本，所以最终测试用例不参与任何选择。一项工作里，不留出时选择分数是满分，测试成功率只有三分之二；严格留出时测试成功率几乎相同，差别在于前者的内部分数严重高估 [E447]。 |
| 保留 | 部署执行、学习维护、研究测评三个账本 | 第 170 行 | Codex 建议 | 方向对，边界需要按 F1 补全。 |
| 保留 | 分四个阶段，每阶段有继续或停下的判断；强化学习放在第四阶段 | 第 229–235 行 | Codex 建议 | 与 Edwin “先定方案再谈预算”一致。 |
| 保留 | 粒度陷阱：轮数变少和保留步骤上调用数为零是同一批调用的两种描述 | 第 201 行 | Codex 建议 | PPT 自己的归类就是例证（`build_deck.py:1401`、`:1416`）。 |
| 修改 | 规则手册出题的归属 | 第 105 行 | 我方建议 | 改为用户要求，见 I9。 |
| 修改 | 3 处文献描述、5 处段末引用 | 见 N1–N8 | 我方建议 | 建议写法见第 3c 节。 |
| 修改 | “文献已足以支持可行性” | 第 11 行 | 我方建议 | 报告已限定为“已评测设定”，并在同段和第 65 行把净收益列为未回答的问题；我方下一稿再补两点：限定为有可靠对错信号的设定，并写明计入改进开销后是否划算，在已核对的文献里证据很少，有利和不利的都有，见 D334。 |
| 修改 | 问题一的写法 | 第 11、45、119 行 | 我方建议 | 只检验“选位置”这一项，其他条件固定，改进资源相同并报告出来；修改去向包含新 action 和环境条件；见 1.3 和 D335。 |
| 修改 | 问题二的写法 | 第 57、121、142 行 | 我方建议 | 差异表述收窄为 1.3 列出的四点；加预算对齐的普通 agent 对照。 |
| 修改 | 问题三的写法 | 第 123 行 | 我方建议 | 写出近邻；“合理使用量”改为事先声明的变更间隔和其中的预期任务数；以金额算回本、以任务数报告，见我方方案稿第 8.3 节。 |
| 修改 | 第七章对应表和账本规则 | 第 170、192–199、207 行 | 我方建议 | 见 F1–F10。 |
| 修改 | 补入遗漏的近邻 | 第 43、51–61、215–225 行 | 我方建议 | 见 1.3 的第一张表。 |
| 讨论 | 第一阶段是否只用既有日志 | 第 97 行 | 用户要求（从轨迹提取）＋ 方案建议（第一阶段只用既有日志、探索另设条件：我方前稿提出，Codex 采纳） | 从轨迹提取环境知识是 Edwin 的出发点；要定的是轨迹不够时是否专门加跑。已核实条目中，ActionEngine 的状态机来自离线爬取 [E382] [E448]，MobileGPT 的页面条目来自随机探索和用户操作记录 [E449]，AutoDroid-V2 的应用文档来自应用探索历史 [E450]；这说明先例多靠探索，不能证明只用任务轨迹不够。需要 Edwin 决定。 |
| 讨论 | 答案库怎么建、由谁确认 | 第 105 行 | 用户要求 | SOPBench 由程序枚举约束条件组合 [E451]，服务函数、约束和校验程序由人工设计并写成程序 [E340] [E398]，原始代码充当判分器 [E452]；LogiSafetyGen 由模型从法规文本提出候选规则，作者三轮一致审核后保留 73.9%（候选数未报告）[E342] [E453] [E454]。“模型推情境、人工简单确认”的人工工作量，在已核对的文献里没有数字，需要自己测。 |
| 讨论 | 是否训练辅助模型 | 第 47、235 行 | Codex 建议 | Harness-R1 的条件见 C5。 |
| 讨论 | 循环在哪个环境里跑（团队现有系统、复制品或两层）、是否停在最终提交之前 | 第 13、103、229 行只要求“可重置”的环境 | Codex 建议（可重置的环境）＋ 我方建议（真实系统还是复制品、是否停在提交之前） | 报告要求可重置的环境，但没有说是真实系统还是复制品，也没有说是否停在提交之前。Edwin 说过不需要专门为 Concur 搭测试环境；先由团队确认手头环境能否重跑和清理，再由 Edwin 决定。 |
| 讨论 | 业务正确性与成本哪个优先 | 第 103、172 行 | Codex 建议 | 报告建议以质量为约束；一项工作的验收允许能力指标在事先定好的容忍度内下降 [E455]。Edwin 没有明确说过（见 I1）。 |
| 讨论 | “询问或规划”里问的是谁 | 第 25、87 行 | 用户要求（每次运行时询问或规划）；对象未定 | 报告默认问用户；Edwin 没有说明。影响评分、时间口径和人工环节的定义，见我方方案稿第 11 节。 |

### 1.6 本文新引用的证据

下表列出本文引用的每一条文献细节。每条都锁定到所读版本的行，并通过了脚本核对和独立审计。“P3 记录”一列是核对库中的条目号。

| E 编号 | 核对库条目 | 文献 | 陈述（完整的五项信息见证据台账） |
|---|---|---|---|
| E324 | x010#0 | [h004] Agent Workflow Memory | In standard AWM, induced workflows are added to the agent's original memory as auxiliary memory (M + W -> M_w), and the LM backbone still produces the actions from the instruction, the workflow-augmented memory and the observation, L(q, M+W, o) -> a. Footnote 1 (line 104) says memory is usually implemented as a system prompt or auxiliary information in the main prompt context. |
| E325 | x010#8 | [h004] Agent Workflow Memory | AWM_AS wraps each workflow as a high-level action that runs a pre-determined series of primitive actions; the agent may call primitive or workflow actions at each step. On Mind2Web (gpt-4, Table 9) it raises step SR by 1.3 points over memory-only AWM (46.4 vs 45.1, lines 516 and 521), and agents called workflow actions in only 18.5% of tasks. For task SR the text says AWM_AS gets 'the same overal… |
| E326 | x010#2 | [h004] Agent Workflow Memory | A workflow is an NL description d (a summary of its function, extracted heuristically from instructions or summarized by an LM) plus a series of steps. Each step has (1) an NL description of the current environment state, e.g. 'Order {id} is shown', (2) the agent's reasoning, and (3) an action written as an executable program over the environment, e.g. stop(). In LM-based induction, example-speci… |
| E327 | x010#15 | [h004] Agent Workflow Memory | AWM represents workflow steps in a program format by default (line 440). A variant whose actions are verbalized into NL by gpt-3.5-turbo (AWM_text) gets 0.6 higher element accuracy and 0.3 higher step SR but 1.2 lower task SR on Mind2Web cross-task (Table 7, AWM_text task SR 3.6), and the authors find no substantial performance difference between text and code formats. |
| E328 | x016#5 | [h010] Better, Faster, Stronger: Programmatic Skill Learning Best Reduces Ag… | Per-episode inference cost is priced from the uncached input, cached input and output tokens summed over all LLM calls in the episode. The sum includes the actor's calls during the rollout and the sleep-time inducer calls, amortized over the rollouts in the inducer batch those calls belong to. |
| E329 | x016#3 | [h010] Better, Faster, Stronger: Programmatic Skill Learning Best Reduces Ag… | All experiments use gpt-5.4-mini as both actor and inducer. Each run has 200 online rollouts with a sleep cycle every 10 rollouts. A fixed held-out test set of 30 episodes per benchmark, shared across all methods and checkpoints, is evaluated every 50 training rollouts. Results are the mean and +/-1 sd over 3 seeds. The two axes are task progression (benchmark-specific success or achievement rate… |
| E330 | x016#6 | [h010] Better, Faster, Stronger: Programmatic Skill Learning Best Reduces Ag… | The cost uses published API prices as of 6 May 2026. For gpt-5.4-mini these are $0.75 for input, $0.075 for cached input and $4.50 for output, per million tokens. The authors state that this dollar-cost accounting is used in Figure 3 (l.717). |
| E331 | x016#7 | [h010] Better, Faster, Stronger: Programmatic Skill Learning Best Reduces Ag… | With GPT-5.4-mini, SpeedRunner is the only method whose cost decreases over training, and this holds on all three benchmarks. On BabyAI, its final usage falls to roughly an eighth of the ReAct baseline. ASI's cost grows on every benchmark as its library accumulates. OPO stays close to ReAct on ScienceWorld and BabyAI but grows substantially on Crafter. |
| E332 | w016#6 | [w016] ActionEngine: From Reactive to Programmatic Web Agents via State Mach… | Across the four WebArena applications, the one-time offline crawl takes 36-260 minutes and costs $11.6-$37.2 per application; relative to Claude Code, ActionEngine's lower per-task execution cost recovers it after 39-101 tasks. |
| E333 | h008#8 | [h007] WALT: Web Agents that Learn Tools | On Online-Mind2Web WALT attempts 305 tool candidates across 139 websites, validates 252 (82.6%) in an average of 1.75 attempts per tool (avg. 1.81 tools/site). Per-tool generation cost, using GPT-5 pricing as an example, is $1.67: proposal $0.26 (amortized across tools per site), demonstration $0.87, generation $0.46, testing $0.08. With baseline inference at $0.12/task, break-even occurs after a… |
| E334 | g118#9 | [g118] Inefficiencies of Meta Agents for Agent Design | Counting fixed design cost C0 (all sampling and evaluation during design) plus per-example inference cost, the designed agent reaches a lower cost per correct response than the best initial-library agent only for DROP and MMLU with parallel curation, at approximately n = 15,000 test examples; for the other datasets and curation methods the gains never justify the cost at any scale. |
| E335 | x017#0 | [w052] ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory | In App. C.2, Table 5, ReasoningBank uses 53054.5 tokens per task in total: 49306.1 for action generation, 2186.3 for the LLM-as-a-Judge and 1562.1 for memory extraction. The authors state that, compared with No Memory, total token consumption rises only about 4.3% while overall performance rises 20.5%, and call ReasoningBank cost-effective. |
| E336 | x017#1 | [w052] ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory | Table 5 has four columns: Action Generation, LLM-as-a-Judge, Memory Extraction and Total. The No Memory row prints 50847.4 action-generation tokens and 50847.4 in total, with dashes in the judge and extraction columns. |
| E337 | x017#8 | [w052] ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory | After each query the trajectory goes through the extraction pipeline and the new memory items are appended to the memory pool; consolidation is deliberately minimal, adding items directly without pruning, and merging or forgetting are left to future work. Retrieved items are concatenated into the agent's system prompt (line 1216). |
| E338 | x017#15 | [w052] ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory | As future directions the authors name composition-aware retrieval and consolidation that would let the agent combine complementary memory items or form reusable macros (line 1344), and retrieval controllers that condition selection on uncertainty, recency and cost instead of embedding similarity alone (line 1347). |
| E339 | n009#3 | [n009] SOPBench: Evaluating Language Agents at Following Standard Operating… | GPT-4o generates realistic test cases for the predefined constraint conditions, and the oracle code validates them. |
| E340 | x021#4 | [n009] SOPBench: Evaluating Language Agents at Following Standard Operating… | Curation has three stages: (1) manual design of each domain's service functions, constraints, SOPs, verification programs, helper functions and database schemas; (2) LLM generation of test cases by permuting constraint combinations, with automated validation by format checkers and constraint verifiers; (3) a manual review of each test case for quality and relevance. |
| E341 | n009#2 | [n009] SOPBench: Evaluating Language Agents at Following Standard Operating… | Constraint outcomes are permuted with k=1: one unsatisfied constraint in a failing AND constraint and one satisfied constraint in a succeeding OR constraint, to reduce redundancy among similar cases. |
| E342 | n035#2 | [n035] Evaluating Implicit Regulatory Compliance in LLM Tool Invocation via… | GPT-5-Mini is the backbone LLM that proposes candidates for policy extraction (oracle construction) and instruction synthesis, chosen for its balance of reasoning capability and cost efficiency. |
| E343 | x022#5 | [n035] Evaluating Implicit Regulatory Compliance in LLM Tool Invocation via… | Ground-truth traces are built by a safety-constrained fuzzer of about 3600 lines of code. It treats trace construction as a bounded search that iteratively proposes candidate actions and rejects any that fail the formal specifications. Each sampled action must pass two checks: a precondition check (executable in the current state) and a safety check (a runtime LTL monitor confirms that the extend… |
| E344 | x022#6 | [n035] Evaluating Implicit Regulatory Compliance in LLM Tool Invocation via… | When the fuzzer tries a business action that violates an LTL constraint, the monitor prunes that path and the search backtracks until it selects the mandatory safety operation. The search repeats until the target trace length is reached. The resulting ground-truth trace wraps every user action in the necessary safety checks, which the authors say makes the test case solvable, executable and stric… |
| E345 | w091#5 | [w091] AgentRewardBench: Evaluating Automatic Evaluations of Web Agent Traje… | No LLM judge exceeds 70% precision on success; the authors read this as 30% of trajectories being erroneously marked successful. |
| E346 | w091#6 | [w091] AgentRewardBench: Evaluating Automatic Evaluations of Web Agent Traje… | The benchmarks' official rule-based evaluation reaches 83.8 precision but 55.9 recall (67.1 F1) on success against expert labels, i.e. it rejects many valid trajectories. |
| E347 | w091#4 | [w091] AgentRewardBench: Evaluating Automatic Evaluations of Web Agent Traje… | 1302 trajectories (196 development, 1106 test) were labelled, giving 3906 binary annotations; a second annotator on the GPT-4o agent's WebArena trajectories gave 89.3% inter-annotator agreement on success. |
| E348 | n009#1 | [n009] SOPBench: Evaluating Language Agents at Following Standard Operating… | The method's output is test data: 903 test cases, each containing a user request, an initial database state, a user goal, and the SOP directed action graph. |
| E349 | n035#0 | [n035] Evaluating Implicit Regulatory Compliance in LLM Tool Invocation via… | LogiSafetyGen takes tool specifications and regulation documents as input and automatically generates test scenarios with explicit, verifiable safety constraints; it is described as a framework for synthesizing test cases (L67). |
| E350 | n009#4 | [n009] SOPBench: Evaluating Language Agents at Following Standard Operating… | A case whose constraint outcomes do not match the specification is regenerated and re-verified until it matches or a predetermined retry limit is reached; beyond the limit the data is fixed by hand. No retry-limit value or counts are given. |
| E351 | n009#6 | [n009] SOPBench: Evaluating Language Agents at Following Standard Operating… | A trajectory passes only if it satisfies all three checks: action permissibility, database outcome matching against the oracle, and procedure completeness. |
| E352 | n035#7 | [n035] Evaluating Implicit Regulatory Compliance in LLM Tool Invocation via… | A model under test succeeds on a case only if it passes two oracles: the functional oracle (its final state matches the state derived from the ground-truth trace) and the safety oracle (its execution trace satisfies all hidden LTL constraints). |
| E353 | x021#10 | [n009] SOPBench: Evaluating Language Agents at Following Standard Operating… | Section 3 places the natural-language user request at the beginning of the interaction 'without further user input'; the agent makes tool calls and ends by calling exit_conversation, otherwise the interaction is terminated when the number of turns exceeds the maximum of 20. Each case is run up to 5 times until a completely finished trajectory is obtained. App. D.2 adds that when the agent stops m… |
| E354 | x022#0 | [n035] Evaluating Implicit Regulatory Compliance in LLM Tool Invocation via… | LogiSafetyGen converts unstructured regulations into Linear Temporal Logic oracles and uses logic-guided fuzzing to synthesize valid, safety-critical traces. On it the authors build LogiSafetyBench: 240 human-verified tasks in which LLMs must generate Python programs that satisfy both functional objectives and latent compliance rules. They evaluate 13 state-of-the-art LLMs. |
| E355 | x022#14 | [n035] Evaluating Implicit Regulatory Compliance in LLM Tool Invocation via… | Because the oracles are restricted to two templates, they capture only the temporal ordering of API calls. This limits analysis of specific function arguments, for example whether a transfer amount is within a safe limit or whether a valid call carries a malicious payload. Policies that need deep semantic inspection of parameter values, or probabilistic judgment, cannot be formalized. The authors… |
| E356 | x004#8 | [w003] From Failed Trajectories to Reliable LLM Agents: Diagnosing and Repai… | In Table VI, prompt-only repair (prompt updates only, runtime harness changes disabled) scores 50.6 / 48.3 / 37.4 / 18.6 on GAIA / SWE / AppWorld / TB2. The variant without trace-grounded diagnosis (Section III-B removed; repair context taken from raw trajectory summaries, l.386) scores 51.1 / 50.7 / 38.1 / 21.6. Both are below the full HarnessFix row of the same table. |
| E357 | x004#7 | [w003] From Failed Trajectories to Reliable LLM Agents: Diagnosing and Repai… | In the RQ3 ablation (Table VI, TCR on GAIA / SWE / AppWorld / TB2), removing the validation-set acceptance checks for target-flaw reduction and new regressions (definition l.386) lowers TCR from 61.7 / 57.3 / 43.0 / 26.5 for full HarnessFix to 55.6 / 53.3 / 39.3 / 24.5. |
| E358 | w003#9 | [w003] From Failed Trajectories to Reliable LLM Agents: Diagnosing and Repai… | Diagnosis quality with the full HTIR against human gold labels: 85.0% step accuracy, 81.3% implementation-anchor accuracy, 86.2% harness-layer macro-F1 (82.5% repair-operator accuracy); raw-trace input gives 55.0% step accuracy (Table V, l.793-794). |
| E359 | w003#8 | [w003] From Failed Trajectories to Reliable LLM Agents: Diagnosing and Repai… | Against Meta-Harness, the strongest automated baseline, HarnessFix is 2.6 to 5.0 points higher in task completion rate while using fewer offline repair tokens (Meta-Harness uses 63.5% to 100.5% more, l.782). |
| E360 | x004#0 | [w003] From Failed Trajectories to Reliable LLM Agents: Diagnosing and Repai… | The diagnosis stage starts from a failed execution trace (l.311). Its first step, symptom localization, decides what failed from the external evaluation result together with the final TraceStep's diagnostic evidence (step details, links, implementation anchors and mapped harness layers). |
| E361 | x004#1 | [w003] From Failed Trajectories to Reliable LLM Agents: Diagnosing and Repai… | A candidate patch first goes through pre-validation: conformance to the repair specification plus syntax and static-analysis checks (l.351). It is then run on a held-out validation set to check that it mitigates the target flaw without unacceptable regressions on tasks the original harness already solved (l.352), and it is accepted only if it reaches the target improvement and stays within the re… |
| E362 | n004#6 | [w102] Rethinking the Evaluation of Harness Evolution for Agents | Without unit tests, Harness Evolution fails to beat direct sampling on average, and on GPT-5.4 pass@1 drops from 75.3 (initial harness) to 69.7. |
| E363 | x005#14 | [w036] StarHarness: Evolving Harnesses with Stratified Search for Enterprise… | AutomationBench Finance as used here has 100 finance workflow tasks (AP/AR, expenses, reporting, bookkeeping) across 47 simulated SaaS applications, graded by programmatic assertions on environment state; the score is the share of the domain's objectives achieved, and a guardrail violation scores the task zero. The Finance-100 subset and Stirrup harness differ from the benchmark paper's default s… |
| E364 | x005#9 | [w036] StarHarness: Evolving Harnesses with Stratified Search for Enterprise… | Under 'Interface repair', EnterpriseOps-Gym evolution repaired MCP argument handling, preserved compound schemas, pruned misleading fields and added linkage and self-reference cues, without changing task data or verifier; AutomationBench gained structured row operations that replaced fragile raw spreadsheet edits. |
| E365 | x005#1 | [w036] StarHarness: Evolving Harnesses with Stratified Search for Enterprise… | The authors call the method benchmark-assisted environment adaptation: the proposer may inspect search-task trajectories and their evaluation outcomes to diagnose recurring failures, while guardrails prevent it from encoding task-specific solutions. Failure diagnosis is thus described as something the proposer does from traces and outcomes. |
| E366 | x005#13 | [w036] StarHarness: Evolving Harnesses with Stratified Search for Enterprise… | For AutomationBench, the evolved harness places triage before mutation, anchors dates to the sandbox clock and delegates arithmetic and spreadsheet operations to deterministic tools; the authors state that they cannot isolate the contribution of any individual tool from these records. |
| E367 | x005#7 | [w036] StarHarness: Evolving Harnesses with Stratified Search for Enterprise… | The score gains coincide with lower estimated GPT-5.4 inference cost per task at OpenAI's published rates: StarHarness reduces cost by 17% on ITBench, 53% on EnterpriseOps-Gym and 29% on AutomationBench relative to the baseline harness. |
| E368 | x005#2 | [w036] StarHarness: Evolving Harnesses with Stratified Search for Enterprise… | The paper names J(h;D) 'the cost function' but defines it as the mean task score obtained by running model M with harness h on benchmark D, where higher is better; the target (Eq. 1) is the harness that maximizes J on the held-out tasks, approximated during search with proposer-visible search tasks and proposer-hidden selection tasks where applicable. |
| E369 | x005#8 | [w036] StarHarness: Evolving Harnesses with Stratified Search for Enterprise… | On EnterpriseOps-Gym with GPT-5.4 over all 103 tasks, the evolved harness cut turns per task from 18.12 to 9.87 and tool calls from 29.53 to 16.83, while full-benchmark task success rose from 23.3% to 43.7% (Table 4). |
| E370 | x007#2 | [w010] Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent… | The task reward inside the engineer reward comes from the benchmarks themselves: WebShop supplies a shaped environment reward and ALFWorld and DBBench supply binary success. No format-validity bonus and no explicit KL loss are added to the GRPO objective. |
| E371 | x007#9 | [w010] Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent… | Table D.1 gives the task-level splits summed over WebShop, ALFWorld and DBBench: 9,071 SFT-train tasks and 8,772 RL-train tasks (disjoint partitions), 17,843 training tasks in total, 299 validation tasks and 1,300 test tasks. |
| E372 | x007#5 | [w010] Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent… | For cold-start SFT, GPT-5.5 generates candidate patches from failure packets in the SFT task split. A candidate is kept only if it is executable, completes the same-batch rerun and gives a non-negative task-reward change. This yields 877 examples (381 WebShop, 248 ALFWorld, 248 DBBench), described as approximately 1K. |
| E373 | x007#8 | [w010] Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent… | Cold-start SFT, online GRPO and direct target-agent SFT each run on a single node with eight NVIDIA H800 GPUs. |
| E374 | x007#13 | [w010] Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent… | The authors state that the prompted frontier models used as harness editors never rerun the target, so they cannot tell whether an edit actually raises task success, and their gains are unstable. Two lines later they report that the trained 9B engineer surpasses the strongest of them: GLM-5.2 averages 48.8% against 53.6% for Harness-R1. |
| E375 | x007#12 | [w010] Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent… | Held-out test: for each benchmark and seed, each engineer sees the same 10 failures of the frozen Qwen3.5-9B target, writes one benchmark-specific patch, and the patch is applied to all remaining tasks. The pooled held-out set contains 1,270 tasks across WebShop, ALFWorld and DBBench (versus the 1,300-task full split that includes the ten evidence tasks), and the protocol is repeated over three m… |
| E376 | x012#0 | [h007] WALT: Web Agents that Learn Tools | Tools are built per website by a demonstrate-generate-validate loop: a web agent demonstrates each identified functionality, a tool generation agent maps the execution traces to structured tools, and a test agent verifies them against pre-vetted test inputs (line 63). The authors state that tool discovery and optimization happen offline during website exploration (line 64). |
| E377 | x012#1 | [h007] WALT: Web Agents that Learn Tools | Stage 1 (Tool Discovery) prompts a web agent to navigate to key user-facing sections of a site (content, discovery, communication areas), discover interactive elements by targeted interactions such as hovering over dropdowns and clicking menus, and then propose a list of reusable tool candidates that maximise coverage and minimise redundancy. |
| E378 | x012#2 | [h007] WALT: Web Agents that Learn Tools | For each candidate the browser agent first demonstrates the functionality to produce an execution trace, and a separate tool construction agent analyses that trace to synthesise both the executable tool and its associated test inputs. Algorithm 1 (line 560) likewise has the tool agent extract the test inputs from the trace and the inferred schema. |
| E379 | x012#4 | [h007] WALT: Web Agents that Learn Tools | The tool is registered and executed end to end by a new browser agent over the pre-vetted test inputs. Failures produce structured feedback (selector drift, uncovered enum values, timing issues, semantic mismatches after URL promotion), which the tool agent uses to refine selectors, amend the input schema or edit the action script. |
| E380 | x012#9 | [h007] WALT: Web Agents that Learn Tools | Future work named by the authors: online tool patching as selectors and schemas drift over time, extracting canonical web patterns for common functionalities, and hybrid integration with official APIs, external MCP servers and more agent-accessible observation spaces. |
| E381 | x013#5 | [h009] SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Sk… | A function counted as 'verified' if it could be called without producing an exception. The authors report that this let malfunctioning APIs occasionally be marked verified because they silenced all exceptions, and call it an evaluation measure with unintended consequences; in their example (line 899) the LLM added 'if' statements so that no atomic action raised an error, which reduced exceptions… |
| E382 | x014#0 | [w016] ActionEngine: From Reactive to Programmatic Web Agents via State Mach… | The Crawling Agent builds the state-machine graph (SMG) automatically by exploring the live application with black-box UI access only (no source code, no existing model), then executes the discovered operations against the live application to validate them and enrich their descriptions. Initial construction is task-independent: the crawler observes only the application and its interactions, not t… |
| E383 | x014#1 | [w016] ActionEngine: From Reactive to Programmatic Web Agents via State Mach… | The initial crawler SMG is refined in a separate warm-up phase that generates and executes one task per WebArena task template, with the Patcher updating the SMG when execution exposes missing or incorrect application knowledge; warm-up uses the task templates but not the evaluation task instances or their instantiated parameters. The Patcher is disabled during evaluation, so each reported task i… |
| E384 | x014#4 | [w016] ActionEngine: From Reactive to Programmatic Web Agents via State Mach… | With the crawler-only SMG, ActionEngine reaches 73.1% overall success on the 655 WebArena tasks; warm-up refinement improves all four domains, by 18.1 percentage points on average as printed: Shopping Admin 74.0% to 95.3%, GitLab 55.0% to 89.0%, Reddit 89.0% to 95.0%, Shopping 80.7% to 87.0%. Both SMG variants run the same pipeline with the Patcher disabled during evaluation, which the authors sa… |
| E385 | x015#0 | [g065] AppAgentX: Evolving GUI Agents as Proficient Smartphone Users | Shortcut creation is gated in two stages: initially an LLM, drawing on prior knowledge, determines whether a given task contains repetitive patterns that may be optimized through shortcut nodes; if the task is deemed to contain such patterns, the next step is to inspect the actual trajectory data (lines 134-136). |
| E386 | x015#3 | [g065] AppAgentX: Evolving GUI Agents as Proficient Smartphone Users | If the conditions for a high-level action are not met, or execution errors occur due to incorrect shortcut-node matching or unexpected UI responses, the agent reverts to selecting actions from the basic action space (fallback strategy). |
| E387 | x015#4 | [g065] AppAgentX: Evolving GUI Agents as Proficient Smartphone Users | In the graph memory, a shortcut node is linked to element nodes by COMPOSED_OF edges carrying three attributes: order (integer execution sequence), atomic_action (type of basic action, e.g. click or text input) and action_params (JSON, potentially including input text and click parameters); their stated purpose is to define how a composite action consists of elements and steps executed in a speci… |
| E388 | x015#2 | [g065] AppAgentX: Evolving GUI Agents as Proficient Smartphone Users | At run time the system matches parsed page elements to stored element nodes by comparing visual embeddings, checks whether those element nodes are associated with shortcut nodes, and then uses the LLM to decide, from the shortcut node's description and the current task context, whether the high-level action can be executed; if so, the LLM generates an action execution template with the low-level… |
| E389 | x016#8 | [h010] Better, Faster, Stronger: Programmatic Skill Learning Best Reduces Ag… | With GPT-5.4-mini, SpeedRunner achieves the strongest final performance on all three benchmarks. On BabyAI it climbs from the ~67% ReAct baseline to near-perfect performance. On ScienceWorld it ties OPO. On Crafter every method ends below 30% mean progression, with SpeedRunner still leading. Per two-sided paired t-tests, SpeedRunner significantly outperforms all baselines in performance and cost… |
| E390 | x016#13 | [h010] Better, Faster, Stronger: Programmatic Skill Learning Best Reduces Ag… | The authors name their limits. Because of cost, they did not benchmark flagship models, and they did not evaluate on more expensive benchmarks such as SWE-Bench or Terminal-Bench (l.415). They also state that skill learning at test time is unstable, as the large error bars for all methods show (l.417). |
| E391 | x016#2 | [h010] Better, Faster, Stronger: Programmatic Skill Learning Best Reduces Ag… | Skill updates are learned purely online: tasks cannot be replayed with an updated policy (§2 l.155-158), and there is no held-out set of episodes used to evaluate skill-update quality for hill-climbing. Checking for regressions is left to the inducer, which is given the stored trajectories indexed by the library version that generated them (§3 Harness l.250-255). |
| E392 | x018#0 | [n026] SoL-Pi: Recursively Scaling Auto-Research Loops for Efficient Agent H… | Before the search starts, capability metrics, acceptable tolerances and efficiency metrics are fixed, stay unchanged, and are kept outside the optimizing agent's control. A candidate passes two sequential gates (every capability metric within its predeclared tolerance; at least one declared efficiency metric improved), and among candidates passing both the nondominated ones are retained. |
| E393 | x018#2 | [n026] SoL-Pi: Recursively Scaling Auto-Research Loops for Efficient Agent H… | On EdgeBench with GPT-5.6 Sol, the complete four-mechanism stack (SoL-Pi [Efficiency]) uses 1.10 B recorded tokens, 49.0% fewer than Pi, with 33.2% lower token cost, while scoring 42.0 vs. 44.8 (93.7% of Pi's average score). The SoL-Pi [Performance] point (47.2 vs. 44.8, token traffic -6.1%) is the single-mechanism configuration with the highest average score, selected per backend from Table 4 (l… |
| E394 | x018#5 | [n026] SoL-Pi: Recursively Scaling Auto-Research Loops for Efficient Agent H… | On 63 CPU-only Terminal-Bench 4 tasks, Codex and Pi each solve 18 tasks and SoL-Pi solves 15; against Pi, SoL-Pi reduces total model cost by 26.3% ($211.12 vs. $286.45) and cost per solved task by 11.6% ($14.07 vs. $15.91). The Table 3 note (line 575) states that GPU-dependent Terminal-Bench 4 tasks were excluded due to infrastructure limits. |
| E395 | x018#13 | [n026] SoL-Pi: Recursively Scaling Auto-Research Loops for Efficient Agent H… | The authors state that running complete auto-research loops in their environment is computationally expensive, which makes controlled comparisons of search breadth and depth under a fixed budget particularly challenging; they leave scaling laws along these dimensions to future work. |
| E396 | x019#0 | [w048] RRSI: Regularized Recursive Self-Improvement of Agent Harnesses | When a candidate's measured evolve-set gain exceeds the noise band (Delta S > delta), RRSI admits it only if its relative change in mean policy-token cost satisfies Delta C <= beta0 + beta1 * Delta S (Eqs. 6-7), with beta0 and beta1 chosen on the evolve set and kept fixed; the authors state that policy-token cost is used as a common measurable proxy for the harness's aggregate resource footprint,… |
| E397 | x019#1 | [w048] RRSI: Regularized Recursive Self-Improvement of Agent Harnesses | On the agentic-workspace instance, no evolved harness is as cheap as the unevolved base harness H0, which runs at 1.56 million policy tokens and 21.2 steps per trial; RRSI's final harness runs 26.3 steps per trial against 27.3 to 34.6 for the four prior methods, and the authors write that evolution buys part of its gain with test-time compute (Table 2 prints 2.42 M tokens/trial for RRSI). |
| E398 | x021#5 | [n009] SOPBench: Evaluating Language Agents at Following Standard Operating… | The manual design process yielded 7 domains with database templates, 97 services (each with service functions, constraints and SOPs), 165 constraints each with a dedicated verifier program, and 70 helper functions. Line 722 says services and constraint verifiers were implemented as Python programs and that the design was iteratively refined throughout development. |
| E399 | x021#12 | [n009] SOPBench: Evaluating Language Agents at Following Standard Operating… | Section 5: the benchmark evaluates one type of SOP, verification constraints that must be satisfied before executing target actions (line 471); it does not include other conditional workflows such as IF-THEN-ELSE logic patterns, and its method relies on procedures that can be explicitly implemented in code, which may not be feasible for all domains or SOP types. |
| E400 | x021#6 | [n009] SOPBench: Evaluating Language Agents at Following Standard Operating… | The expected outcome is computed by code: the executable code oracle processes the same user request u with the same initial database state s0, verifies each constraint and executes the service function only when all constraints are satisfied, producing the oracle final database state s*; Dimension 2 requires the agent's final database state to match s* (line 172). |
| E401 | x023#7 | [h011] On the Fragility of Self-Improving Agents: Variance, Task Order, and… | Table 1 (GPT-5-mini, default order, 3 runs, 12 domains of WebArena, VisualWebArena and SCUBA, each for AWM and RBank): the memory-based methods increase across-run variance in 17 of 24 cases (about 71%), and in 11 of these the relative increase exceeds 50%. |
| E402 | x023#3 | [h011] On the Fragility of Self-Improving Agents: Variance, Task Order, and… | Each experiment of interest is repeated as three identical self-improving runs; the reported metrics are run-level: average pass rate (pass@1) per domain, its standard deviation across the three runs, and the best-worst gap among the three runs. Footnote 2 (line 127) defines one run as evolving over all tasks in the sequence. |
| E403 | x023#8 | [h011] On the Fragility of Self-Improving Agents: Variance, Task Order, and… | Under the default task order the ReasoningBank agent gains 1.5% on average over the baseline, but under randomly shuffled task orders it shows a 4.5% degradation. The preceding sentence (line 88) states that the default order in prior works imposes an implicit easy-to-hard curriculum that acts as a hidden prerequisite for these methods to succeed. |
| E404 | x023#1 | [h011] On the Fragility of Self-Improving Agents: Variance, Task Order, and… | Unless otherwise specified, GPT-5-mini is both the agent backbone and the memory construction model, and the memory construction step is deliberately given the ground-truth reward r, unlike prior works that use a proxy reward from an LLM judge, which the authors found to be noisy. |
| E405 | x002#0 | [w011] GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learni… | Each task instance pairs an input x with evaluator metadata m (for example gold answers, evaluation rubrics or code unit tests); a metric mu scores the system output against m on [0,1] (for example exact match, F1 or pass rate), and the optimization target is the expected mu over the task distribution (Eq. 1, line 128). |
| E406 | x002#4 | [w011] GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learni… | Per iteration, GEPA runs the selected candidate on a sampled training minibatch, calls mu_f for a numeric score plus evaluation text, picks the module to update by a round-robin policy, and has a reflection LM propose revised instructions from (current prompt, trajectory, score, feedback); the updated program is re-evaluated on the same minibatch and added to the candidate pool only if the score… |
| E407 | x002#1 | [w011] GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learni… | In the Sec. 4 evaluation the authors adopt a standard train/validation/test split; optimizers have full access to the train split including text and labels, may monitor candidate scores on the validation set (e.g. for early stopping), but direct access to the content of validation instances is restricted (lines 402-404). The Sec. 5.1 inference-time-search experiments instead put the full task set… |
| E408 | x002#3 | [w011] GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learni… | GEPA takes as input a system instantiated with simple prompts, a training set, the task metric mu, a feedback function mu_f and a total rollout budget B, and evolves only the set of module prompts while the underlying LLM weights stay fixed. |
| E409 | x012#8 | [h007] WALT: Web Agents that Learn Tools | The authors state that offline tool discovery incurs an exploration and validation cost per website, which the paragraph gives without any figure. Further stated limitations: tool quality depends on what exploration uncovers and what the site exposes; highly dynamic interfaces, A/B experiments, CAPTCHAs and heavy anti-automation can reduce determinism or block URL promotion; schemas may miss rare… |
| E410 | h014#0 | [h014] Inducing Programmatic Skills for Agentic Tasks | ASI induces and applies programmatic skills while solving the stream of user web-navigation queries: for each query the agent first generates a trajectory attempting to solve it with built-in primitive actions (e.g. click, scroll; later also previously learned skills), then induces higher-level skills as executable programs that wrap primitive actions or prior skills, each accompanied by test tra… |
| E411 | h014#4 | [h014] Inducing Programmatic Skills for Agentic Tasks | Candidate skills are tested by executing an LLM-rewritten, truncated skill-using trajectory prefix and letting the agent finish the same query; they are kept only if (1) the LLM evaluator judges the task solved, (2) at least one new skill is called, and (3) every skill-calling action changes the environment. Only the skills actually called are added to the library. |
| E412 | h032#1 | [h032] EchoPath: Execution-Level Replayable Memory for GUI Agents | What the method builds and edits is an external store: a validated GUI trajectory is converted into a standardized, parameter-controlled callable memory, analogous to an MCP-style tool call, exposing intent keys, preconditions, typed modifiable parameters, visual evidence and validation/lifecycle metadata. |
| E413 | h032#2 | [h032] EchoPath: Execution-Level Replayable Memory for GUI Agents | A completed first-run trace is eligible for memory construction only when the external artifact evaluator V passes on the final artifact or task output (V(y_T, tau) = 1). |
| E414 | h032#0 | [h032] EchoPath: Execution-Level Replayable Memory for GUI Agents | Replay swaps fresh per-step GUI planning and grounding for a compatibility-gated instantiation of a stored action trajectory; the output is either a bound replay program or a rejection with a cause (state mismatch, missing target, parameter conflict, unsupported or unsafe action). |
| E415 | w006#0 | [w006] AutoSaddler: Automatic Harness Optimization with Durable Updates from… | Intro (line 128): AutoSaddler beats the base harness by 9.0 pp on GAIA2, 9.6 on SWE-Bench Pro and 10.0 on Terminal-Bench 2.0, and beats the strongest automated baseline (GEPA on GAIA2 and SBP, Meta-Harness on TB2) by 7.4, 4.4 and 6.7 points. The abstract (line 120) gives only the base-harness gains, and the conclusion (line 401) gives both sets. Section 5.2 (line 366) prints different values (+8.… |
| E416 | w006#7 | [w006] AutoSaddler: Automatic Harness Optimization with Durable Updates from… | On GAIA2, AutoSaddler reaches 72.3% dev accuracy with about 1,000 total task executions, while GEPA and Meta-Harness saturate at 64.6% and 61.5% after about 2,800. Counted by execution rollouts leveraged for optimization, AutoSaddler's best dev score comes after 147 traces, against 1,400 for Meta-Harness (~10x fewer). |
| E417 | w009#4 | [w009] Agentic Harness Engineering: Observability-Driven Automatic Evolution… | The Evolve Agent is instructed to group failures into pattern classes, find the root cause of each pattern and choose the fix level: prompt, tool, middleware or any other component. |
| E418 | w009#0 | [w009] Agentic Harness Engineering: Observability-Driven Automatic Evolution… | Terminal-Bench 2 (89 tasks, GPT-5.4 high): the NexAU0 bash-only seed scores 69.7% pass@1 and AHE 77.0%, above the human-designed Codex harness (71.9%) and the self-evolving baselines ACE (68.9%, below the seed) and Training-Free GRPO (72.3%). AHE is the best configuration of one ten-iteration campaign. By tier AHE trails Codex on Hard (53.3% vs 56.7%). |
| E419 | w004#9 | [w004] Meta-Harness: End-to-End Optimization of Model Harnesses | Ablation of what the proposer can read: scores only reaches 34.6 median / 41.3 best accuracy, scores plus LLM-generated summaries 34.9 / 38.7, and full access to execution traces 50.0 / 56.7; the authors conclude raw traces are the most important part of the interface. |
| E420 | n004#5 | [w102] Rethinking the Evaluation of Harness Evolution for Agents | Every method gets a compute budget of K=5; for AHE one rollout is sampled per task for each harness (m=1) to match the rollout budget across methods; all methods start from AHE's initial harness. |
| E421 | n004#8 | [w102] Rethinking the Evaluation of Harness Evolution for Agents | On disjoint tasks (45 train, 10 validation, 34 test), the harness evolved on the training set with unit tests and selected on validation gains +1.2 pass@1 on Claude Opus 4.6, +0.0 on GPT-5.4, +0.6 on average over the initial harness. |
| E422 | n004#7 | [w102] Rethinking the Evaluation of Harness Evolution for Agents | With unit tests, Harness Evolution reaches pass@1 73.0 (Claude Opus 4.6) and 78.6 (GPT-5.4), average 75.8, and pass@5 83.2 / 89.3, average 86.2; this is below Parallel Sampling's 86.0 average pass@1 and Sequential Refinement's 91.8 average pass@5 (line 282). |
| E423 | w035#0 | [w035] SKILL.nb: Selective Formalization and Gated Execution for Durable Age… | Gate-conditioned execution: each workflow step runs its executable code when its gates validate, and otherwise falls back locally to the NL procedure or the step intent when drift invalidates the code. |
| E424 | w035#6 | [w035] SKILL.nb: Selective Formalization and Gated Execution for Durable Age… | In the component ablation the full SKILL.nb uses 36k SKILL.nb-internal maintenance/update tokens per success, the lowest of the five variants: NL-only 57k, code-only 42k, no gates 45k, no demote 47k. |
| E425 | w035#9 | [w035] SKILL.nb: Selective Formalization and Gated Execution for Durable Age… | Under real GitLab version drift, reusing the frozen state learned on the source version keeps performance: on the latest target 110/180 fresh-start vs 111/180 frozen-state successes (61.1% vs 61.7%); on the intermediate target 108/180 frozen vs 111/180 fresh. |
| E426 | w054#7 | [w054] Grounding Agent Memory: Environment-Probing Curation for Enterprise A… | Without schema drift, probing raises mean reward over trajectory-only memory from 0.673 to 0.748 on Sonnet 4.6 and from 0.696 to 0.721 on Opus 4.7. |
| E427 | w054#8 | [w054] Grounding Agent Memory: Environment-Probing Curation for Enterprise A… | The cost of the improvement step itself is not reported: task-agent cost excludes the separately tracked curation phase, and memory-management calls are excluded from the tool-call count. |
| E428 | w013#0 | [w013] Are Online Skill and Memory Modules Always Worth Their Tokens? A Budg… | The budget-matched control, Vanilla-IB, is a vanilla actor (same base LLM) with no auxiliary modules, its horizon extended to 15 steps, and rule-based accessibility-tree pruning that makes no LLM calls (lines 179-181). It shares the unified codebase, prompts and temperature 0 of AWM and ASI. ReasoningBank runs on its own codebase at temperature 0.7 (App. A, lines 928-933). In the main experiments… |
| E429 | w013#8 | [w013] Are Online Skill and Memory Modules Always Worth Their Tokens? A Budg… | Gemini 3 Flash, WebArena four-domain average: Vanilla-IB reaches 44.78% success at 73.6K total tokens per task, the highest success rate and lowest token count of the four configurations for this model; the text states Vanilla-IB has the best average success rate for all three models (line 356). |
| E430 | w013#7 | [w013] Are Online Skill and Memory Modules Always Worth Their Tokens? A Budg… | The authors limit their budget-matching argument to online augmentation; offline methods such as SkillWeaver and WALT amortize skill-discovery cost over many uses and need different accounting. |
| E431 | n016#1 | [n016] PolicyBank: Evolving Policy Understanding for LLM Agents | What the loop changes is the memory bank: each entry is a tuple of a capability identifier and a semi-structured Spec_NL text (TRIGGER, PRECONDITIONS, ELIGIBILITY, ACTION, KEY INSIGHT). Model weights, the written policy and the tools are not what is updated. |
| E432 | n016#6 | [n016] PolicyBank: Evolving Policy Understanding for LLM Agents | Airline domain, Gemini-3-Pro task agent, sister (policy-gap) tasks: PolicyBank pass^1 0.74 vs ReasoningBank 0.23 (No memory 0.01 in the same table block, line 249). On the original tasks the two are equal at pass^1 0.70. |
| E433 | g037#5 | [g037] ClawTrace: Cost-Aware Tracing for LLM Agent Skill Distillation | On the SpreadsheetBench held-out set, removing prune patches (No-prune) tripled regressions at seed 0 from 4 to 13 with comparable median cost, and stripping cost from TraceCards (No-cost-attribution) raised the median cost uplift on successful tasks from +22% to +49% and regressions from 4 to 6; pooled over two seeds Full CostCraft vs No-prune is 5 vs 14 regressions (2.8x). |
| E434 | g049#6 | [g049] Rethinking Self-Evolving Agents: Do We Still Need Prescribed Optimiza… | With GPT-5.5 as optimizer, OEO records 7 wins and 1 tie against SkillOpt across 8 benchmark-target settings, and 5 wins in 6 confirmatory settings against GEPA, whose only lead is 0.21 percentage points (together: 12 wins, 1 tie, 1 loss over 14 comparisons, per the abstract). OEO improves all 8 initial skills. |
| E435 | g049#8 | [g049] Rethinking Self-Evolving Agents: Do We Still Need Prescribed Optimiza… | Delegation depends on optimizer capability: with protocols frozen, a medium optimizer (Qwen3.5-27B) makes SkillOpt lead OEO by 9.68 pp on LiveMath and 3.50 pp on SearchQA; a weak optimizer (Qwen3.5-4B) emits non-executable actions under the unchanged OEO interface so no rollout occurs, while the SkillOpt runner completes by supplying the control sequence externally (weak-optimizer SkillOpt still… |
| E436 | g047#7 | [g047] Coding Agents are Strong Prompt Optimizers | Limited-data regime (every optimizer sees only the same static pool): CASD lifts the no-skill baseline by +16.6 points on average versus +10.9 for GEPA and +5.3 for SkillOpt; on telecom GEPA falls below the baseline (17.5 vs 19.2) while CASD gains +20.0 points. |
| E437 | w059#7 | [w059] ContractSkill: Repairable Contract-Based Skills for Multimodal Web Ag… | MiniWoB ablation: full ContractSkill 77.5% (GLM) / 81.0% (Qwen); Text-Only Rewrite 62.0% / 60.5%; No Failure Localization 65.0% / 70.0%; Unconstrained Repair 68.5% / 70.5%. |
| E438 | w039#6 | [w039] Aegis: Taxonomy and Optimizations for Overcoming Agent-Environment Fa… | Optimization targets are picked by plotting each subtask's failure rate against its frequency; subtasks that are both common and brittle are the highest-leverage targets. |
| E439 | n028#7 | [n028] Are Large Language Models Good Prompt Optimizers? | Replacing real error examples with pseudo errors (all predictions uniformly flipped) gave results, including the optimization trend, comparable to real errors on navigate, question_selection and snarks; on object_counting Pseudo was slightly lower but the highest test scores were close. |
| E440 | n052#1 | [n052] Building an agentic memory system for GitHub Copilot | Just-in-time verification: when an agent meets a stored memory it checks the citations in real time against the current branch before using it; the post says this is a small number of simple read operations adding no significant latency 'in our testing' (no figure given). |
| E441 | w054#0 | [w054] Grounding Agent Memory: Environment-Probing Curation for Enterprise A… | After each task the curator agent proposes a candidate memory, makes targeted read-only tool calls to the environment to investigate specific uncertainties, then uses the observations to create, revise, narrow, delete or skip the record (propose-probe-commit). |
| E442 | w065#7 | [w065] From Imperative to Declarative: Towards LLM-friendly OS Interfaces fo… | Ablation: giving the baseline the DMI navigation forest in the prompt, with the declarative interface disabled, gives no significant change for GPT-5 (SR 42% vs 44%, steps 8.41 vs 8.16, normalized steps 8.58 vs 7.94); the authors conclude the declarative interface, not the static knowledge, is the primary source of the gain. For GPT-5-mini the forest alone helps modestly (17.3% to 23.5%), full DM… |
| E443 | w062#1 | [w062] SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse T… | Self-generated Skills (authored by the agent with Anthropic's skill-creator, then used alone) land below the no-Skills baseline on all three dedicated-harness configurations, while curated Skills add +18.2 to +24.8 pp on the same configurations. |
| E444 | w054#5 | [w054] Grounding Agent Memory: Environment-Probing Curation for Enterprise A… | On the CLBench drift schedule, probing raises strict pass rate from 39% to 73% and total pass-discounted reward from 8.60 to 22.60, while task-agent SQL queries fall from 8.8 to 4.7 per question and task-agent cost for a 40-question run falls from $3.38 to $1.68, versus no memory. |
| E445 | n024#8 | [n024] Beyond Endpoint Performance: Process-Level Evaluation of Self-Evolvin… | The main experiments on both API backbones (Qwen3.8-Max and Kimi-K3) consumed 1.838 billion tokens in total; direct evolution calls that construct or revise artifacts account for 106.34M tokens, the rest is task execution and candidate validation. Table 12 lists 1,586.49K calls in total (802.21K Qwen3.8-Max, 784.29K Kimi-K3). (A list-price money estimate in the same paragraph is not recorded, bud… |
| E446 | g041#6 | [g041] SEAGym: An Evaluation Environment for Self-Evolving LLM Agents | Main AHE training run (DeepSeek-V4-Flash, batch 20, 5 epochs, 20 updates, 720 task rows) recorded 1053.8M rollout tokens, 78.1M update tokens and 14h06m runtime. |
| E447 | w089#2 | [w089] Recursive Self-Evolving Agents via Held-Out Selection | Selection ablation: re-running the evolution with no held-out split (selecting on the evolve set itself) gives a perfect in-sample selection score but only 66.7% on test, a 33-point train-test gap, versus 67.3% for RSEA with the strict held-out gate and 63.6% for ReAct. |
| E448 | w016#5 | [w016] ActionEngine: From Reactive to Programmatic Web Agents via State Mach… | The state-machine graph is constructed offline through a fully automated crawl-and-validate pipeline starting from a seed state. |
| E449 | w070#2 | [w070] MobileGPT: Augmenting LLM with Human-like App Memory for Mobile Task… | Candidate page entries are produced offline: a random explorer and a user trace monitor visit app screens, and for each screen the LLM generates the list of available sub-tasks, which is cached for the Select phase; unexplored screens are analysed on demand. |
| E450 | h015#0 | [h015] AutoDroid-V2: Boosting SLM-based GUI Agents via Code Generation | Two stages. Offline, AutoDroid-V2 builds an app document from the app exploration history (line 139) and uses it to synthesize large-scale user tasks for fine-tuning the local LLM, with sandbox validation and tree-based search for data quality (line 140). Online, for each user task request the customized local LLM generates a multi-step script that a domain-specific interpreter executes (line 141… |
| E451 | x021#0 | [n009] SOPBench: Evaluating Language Agents at Following Standard Operating… | The construction procedure itself enumerates the test conditions: for each action all required constraints are kept and all 2^n subsets of its n customizable constraints are iterated (line 728); for each resulting dependency the outcome of each constraint is permuted, with a constant k=1 meaning one unsatisfied constraint in a failing AND and one satisfied constraint in a succeeding OR, set 'to r… |
| E452 | n009#0 | [n009] SOPBench: Evaluating Language Agents at Following Standard Operating… | Each service-specific SOP code program is turned into a directed graph of executable functions that agents must call from natural-language SOP descriptions; the original code serves as the oracle rule-based verifier. |
| E453 | n035#4 | [n035] Evaluating Implicit Regulatory Compliance in LLM Tool Invocation via… | All authors independently reviewed every safety-oracle (LTL) candidate across three rounds, retaining only candidates with unanimous agreement. |
| E454 | n035#5 | [n035] Evaluating Implicit Regulatory Compliance in LLM Tool Invocation via… | The oracle-construction pipeline achieved an aggregate human acceptance rate of 73.9% across the three domains. |
| E455 | n026#3 | [n026] SoL-Pi: Recursively Scaling Auto-Research Loops for Efficient Agent H… | Capability metrics, tolerances and efficiency metrics are fixed before experimentation and kept out of the optimizing agent's control; a candidate must pass two sequential gates (every capability metric within its predeclared tolerance; at least one declared efficiency metric improved), and among candidates passing both gates the nondominated results are retained. |
| E456 | n035#3 | [n035] Evaluating Implicit Regulatory Compliance in LLM Tool Invocation via… | Candidate LTL formulas pass through a deterministic Signature Validator that eliminates any formula containing predicates not defined in the API schema (e.g., a hallucinated verify_user versus the real check_auth). |
| E457 | h005#6 | [h004] Agent Workflow Memory | Appendix D (camera-ready only; arXiv v1 ends at Appendix C) reports per AWM step the input, output and per-step tokens, the average occurrences per task, and the average total tokens per task (Table 11). Action generation: 5,663 input + 52.0 output = 5,715 per step, 5.9 occurrences, 33,718.5 total. Trajectory evaluation: 306.8 + 82.8 = 389.6 per step, 5.9 occurrences, 2298.6 total. Workflow induc… |
| E458 | h005#9 | [h004] Agent Workflow Memory | Mind2Web, gpt-4 (camera-ready Table 4). Cross-task step SR: AWM_offline 45.1 and AWM_online 43.6 vs MindAct* 36.2 (45.1/36.2 = +24.6% relative, calc.; the headline 24.6%). Offline workflows are induced from the Mind2Web training set; online workflows only from the test queries (lines 410-424, 476-482). Cross-domain step SR: AWM_online 35.5 and AWM_offline 32.6 vs MindAct* 26.4. The MindAct* cross… |
| E459 | x003#5 | [w050] Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents | App. C.2: parents are sampled with replacement from archive agents whose performance score is not yet perfect, with weight = sigmoid-scaled performance (lambda=10, midpoint alpha0=0.5) times a novelty bonus 1/(1+n), n = number of children with codebase-editing functionality; the text says this favours agents with high performance and fewer existing children and keeps every agent's sampling probab… |
| E460 | x005#15 | [w036] StarHarness: Evolving Harnesses with Stratified Search for Enterprise… | Across the three evolution runs, 21 patches were accepted: 4 for ITBench, 12 for EnterpriseOps-Gym and 5 for AutomationBench; on EnterpriseOps-Gym, 8 came from the tree-search exploration stage and 4 from the subsequent hill-climbing stage. |
| E461 | g065#3 | [g065] AppAgentX: Evolving GUI Agents as Proficient Smartphone Users | The gate for creating a shortcut is an LLM judgement from prior knowledge that a task contains repetitive patterns; only then is the trajectory inspected. No post-creation keep/discard test is described. |
| E462 | g065#4 | [g065] AppAgentX: Evolving GUI Agents as Proficient Smartphone Users | The only feedback described is at run time: if a shortcut's conditions are not met, or execution errors occur from incorrect shortcut matching or unexpected UI responses, the agent falls back to the basic action space. No signal scores whether a new shortcut is better. |
| E463 | h015#1 | [h015] AutoDroid-V2: Boosting SLM-based GUI Agents via Code Generation | The on-device model's weights are changed: the local LLMs (Llama-3.1) are fine-tuned on an 8 x A100 80GB server for 1 epoch, about 2.5 GPU hours. (The fine-tuning is supervised fine-tuning on the automatically generated task-solution set, line 393.) The app document is a second, separately built artifact (see mechanism item). |
| E464 | n025#6 | [n025] AgentStream: How Well Do Self-Evolving LLM Agents Perform Under Strea… | Average evolution gain over vanilla, averaged over the 5 methods: GPT-5.4 is negative in all three scenarios (2/5, 1/5, 1/5 methods above vanilla, i.e. 4 of 15 configurations); Gemini 3.1 Pro +2.71 / +1.98 / +2.41 (5/5, 4/5, 5/5); Claude Opus 4.7 +1.75 / +1.05 / +0.90 (5/5, 4/5, 4/5), for Isolated / Sequential / Interleaved. |
| E465 | x017#2 | [w052] ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory | Table 1 (WebArena, 684 tasks overall; Gemini-2.5-flash backbone): the No Memory agent's overall success rate is 40.5 with 9.7 average steps. |
| E466 | x017#3 | [w052] ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory | Table 1 (WebArena, 684 tasks overall; Gemini-2.5-flash backbone): ReasoningBank's overall success rate is 48.8 with 8.3 average steps, against 40.5 and 9.7 for No Memory (lines 221-222). |
| E467 | x021#2 | [n009] SOPBench: Evaluating Language Agents at Following Standard Operating… | Given each task and its specified constraint outcome, an LLM attempts to generate the 'surrounding information' intended to simulate that outcome; the authors name the initial database, user-known information and other parameter values as these surrounding values. Whether the generated data actually produce the intended outcome is checked afterwards by the oracle verifiers (App. C.2.3). |
| E468 | x021#9 | [n009] SOPBench: Evaluating Language Agents at Following Standard Operating… | Dimension 1, action permissibility: the rule-based verifier gives a binary oracle permissibility outcome for each service function the agent invokes, and invoking a function whose oracle permissibility is 0 is recorded as a permissibility violation; the check can run in real time during the interaction or after the trajectory has finished. |
| E469 | x021#8 | [n009] SOPBench: Evaluating Language Agents at Following Standard Operating… | Dimension 3, procedure completeness: to prevent agents from bypassing verification steps and guessing permissibility, the evaluation checks that the service function is preceded by all required helper functions that check its constraints according to the SOP's directed action graph. A trajectory passes only when it satisfies all three verification methods (line 176). |

## 2 D-ledger additions

编号接续仓库当前最大值 D320（提交前已用 `git fetch` 和全文检索复核）。“已记录的写法”一列引用的是仓库文件或 Codex 报告中的原句位置；“原文或依据”一列给出所读版本和位置，对应证据见第 1.6 节。“处理”一栏中的“改写为”“改为”指仓库台账和我方下一稿的写法，Codex 报告不改；涉及仓库现有行的替换文字在第 3 节。

| ID | 涉及 | 已记录的写法 | 原文或依据 | 处理 |
|---|---|---|---|---|
| D321 | 公式中 i = 0 的含义 | `research/2026-09-28-problem-definition.md:34`（F1(e)）：i = 0 收纳不属于任何一步的调用和区间，列举中包含“摊销的学习调用”。同一文件 `:205`（F14(g)）：费用公式不包含 SpeedRunner 的摊销归纳调用；`:269` 的符号表：i = 0 是每次尝试内、任何一步之外的调用和区间。Codex 报告第 207 行：学习投入不能放进 i = 0 | PPT 页面的写法：`slides/build_deck.py:501`（第 3 页，i = 0 是任何一步之外的调用，例如开头的规划）、`:1401`（建设成本在公式之外）、`:1573` 和 `:1767`（附录 B8，v_n = C_setup/n + C/R，建设费不除以 R） | F1(e) 与 F14(g)、`:269`、PPT 页面和 B8 冲突。采用后者：i = 0 只含本次尝试内、不属于任何一轮的调用和区间（开头的规划、一次性检索、登录或重置）；摊销的学习调用不进 i = 0，只记在学习维护账本。两处同时计入会把同一笔建设费乘以 1/R 并与 C_setup/n 重复。F1(e) 的替换文字见第 3a 节，v3.1 合并时应用。不改 slides。 |
| D322 | Agent Workflow Memory 的表示形式 | Codex 报告第 51 行：“可调用的文字工作流”；`research/2026-09-29-part3-related-work-survey.md:75`：“文字 workflow”；`research/2026-09-29-part3-report-support.md:23`：“AWM 为文字工作流”；dossier v3 D41（`Agent-Acceleration-Consolidated-Dossier-v3-2026-09-27.md:1005`）：“Text workflow memory improves success but does not replace calls” | arXiv v1：工作流每一步包含当前状态的文字描述、推理和写成程序的动作，归纳时具体值换成命名占位符 [E326]；在 Mind2Web cross-task 上，把动作改写成文字的变体与默认格式的表现没有实质差别 [E327]；工作流加进记忆（提示上下文），动作仍由模型逐步给出 [E324]；只有变体 AWM_AS 把它封装成可调用的高层动作，调用比例和任务成功率见 [E325] | D41 中“does not replace calls”成立，“Text workflow”按本条限定。改写为：AWM 从过往轨迹归纳带命名占位符的子流程（自然语言描述加程序格式的动作步骤），默认放进提示作为参考，每一步仍由模型决定；只有变体 AWM_AS 把工作流封装为可调用动作。E272、survey 第 75 行和 report-support 第 23 行的替换文字见第 3 节。 |
| D323 | SpeedRunner 的成本曲线 | Codex 报告第 57 行：“画累计成本曲线”不是空白；D317：“E271/SpeedRunner 已有按学习进度的效率评估曲线”；D172（`research/2026-09-28-part2-acceleration-by-term.md:350`）：口径有歧义 | arXiv v1：成本按每条轨迹计，归纳调用按所在批次摊入 [E328]；§4.3 把效率定义为每条轨迹的输出 token，附录 A.3 又说图 3 用的是按公开价格折算的美元成本，两处口径不一致（同 D172）[E329] [E330]；固定的留出测试集每个基准 30 条，每 50 次训练运行测一次，只用于报告 [E329]；实验在 ScienceWorld、BabyAI、Crafter 上 [E389]；技能更新纯在线，不回放任务，没有留出集用来决定更新取舍，回归检查交给归纳模型 [E391]。所读版本中没有找到累计成本曲线 | D317 和 D172 的说法都成立（按学习进度的效率曲线已有先例；口径有歧义）；报告第 57 行的“累计成本曲线”在所读版本（arXiv v1）中没有找到。沿任务流累计投入与累计节省的曲线，核对库中只有一次性建设或设计成本的回本点 [E332] [E333] [E334]。E271 追加说明，见第 3 节。 |
| D324 | ReasoningBank 的开销来源 | Codex 报告第 61 行：“记忆构建、检索和额外上下文也会产生开销”；E321（`research/2026-09-29-part3-related-work-survey.md:174`）：“所报 actor 执行减少不等于含判断与记忆提炼的总 token 降低”；同文件 `:93`：执行 steps 或 actor tokens 降低不等于含判断/提炼的总开销下降 | arXiv v2 附录 C.2 表 5：多出的 token 来自判分和经验提取调用，动作生成一栏低于无记忆基线 [E335] [E336]；成本表的四栏是动作生成、判分、经验提取和合计，单位是 token，没有检索一栏 [E336]。表 5 对应哪个基准和模型，所读版本中没有找到说明 | E321 的写法成立。报告第 61 行中“记忆构建”部分成立，“检索和额外上下文”的部分没有出处。另注：这是每任务（每次尝试）的口径；作者以总 token 约升 4.3%、表现升 20.5% 为由称该方法划算 [E335]。E321 追加条件，见第 3 节。 |
| D325 | 引用挂在方案自己的规则上 | Codex 报告第 105 行段末 [21][22]（生成器不得修改规则、判分程序和答案）；第 107 行段末 [20]（段中含“最终测试另行保留”） | [20] 紧跟判分器误判一句，对那一句成立 [E345] [E346]，AgentRewardBench 只为评测判分器划分了开发集和测试集 [E347]；[21][22] 是基准构造，没有改进循环 [E348] [E349]，SOPBench 的分工与该规则一致 [E350] | 这些规则是方案自己的设计，在我方下一稿标为 Codex 建议或我方建议，不挂文献引用；规则本身保留。第 61 行不属于方案规则：该句是关于 SoL-Pi 和 RRSI 的文献陈述，保留 [18][19]，只把 [17] 移到 ReasoningBank 一句后面，见 N4。另注：报告第 154 行的 [23] 跟在“已有研究指出自改进评估对顺序、方差和未明确条件敏感”之后，[23] 支持其中的方差和顺序部分 [E401] [E403]；前一句“恰好先遇到关键页面”没有引用，是报告自己的例子；[23] 指出的顺序效应是默认顺序隐含由易到难的安排 [E403]。 |
| D326 | 从规则构造测试的先例与归属 | Codex 报告第 105 行：由模型提出覆盖不同条件的案例，再由程序约束和人工确认形成可信的预期结果，“这是另一份讨论草稿提供的候选思路”；`research/2026-09-29-part3-report-support.md:34`：规则派生用例记为“跨会话候选建议”；`research/2026-09-29-part3-claude-draft-crosscheck.md:22`（D314）：“草稿转述的新增用户设想” | SOPBench 是程序枚举条件组合、模型只生成数据、人工逐条复查 [E341] [E339] [E340]，预期结果由程序执行得出 [E400]，服务函数、约束和校验程序由人工设计并写成程序 [E340] [E398]，只覆盖能写成代码的前置校验 [E399]；LogiSafetyGen 由模型从法规文本提出候选规则，经校验器和作者三轮一致审核（保留 73.9%，候选数未报告），再由搜索程序生成合规参考轨迹 [E342] [E456] [E453] [E454] [E343] [E344]；两篇都没有用户中途回答问题的设置：SOPBench 的用户请求在开头一次给出，之后只在 agent 停止调用工具时重发用户已知信息 [E353]，LogiSafetyBench 的被测模型生成一段程序 [E354] | 归属：这个想法是 Edwin 提出的，D314 的记录正确，report-support 第 34 行和报告第 105 行的“候选建议”与之不符，以 D314 为准（第 34 行的替换文字见第 3a 节）。先例：Edwin 设想的“模型从规则手册推出情境和边角案例并生成数据、人工简单确认”，在已核对的文献里没有直接先例：LogiSafetyGen 由模型提规则，但情境由程序生成，审核是三轮一致同意。列入待定事项：人工确认的工作量要自己测。 |
| D327 | WALT 的建设成本随版本不同 | E230（`research/2026-09-28-part2-acceleration-by-term.md:1022`）：“camera-ready not readable”“Discovery cost per site not quantified”；D168（同文件 `:346`）：“Discovery cost unquantified. ICLR 2026 camera-ready not readable (challenge page)”；E230 recheck（`research/2026-09-29-part3-evidence.md:17`）：本轮未读 camera-ready；Codex 报告第 218 行：WALT“已包含学习过程和建设代价”，所读版本为 arXiv v1 | arXiv v1 只把逐站探索和验证的开销列为局限，没有费用数字 [E409]；ICLR 2026 正式版给出了 Online-Mind2Web 上每个工具的建设费用和回本所需的使用次数，没有给 VisualWebArena 和 WebArena 的费用 [E333]。`research/2026-09-29-deck-audit.md:22`（AU6）已记录同一组数字，PPT 第二部分第 4 页已采用 | E230 的“camera-ready not readable”和 D168 中同一句已过时，由本条补充，D168 原文不改；对 E230 所记的 VisualWebArena Classifieds，建设成本仍未量化。替换文字见第 3 节。引用 WALT 的建设成本时必须写明：出自 ICLR 正式版，只针对 Online-Mind2Web，按 GPT-5 价格示例计价（论文未说明 token 用量是实测还是估算），没有给时间数字。 |
| D328 | AWM 两个版本的差异 | Codex 报告文献 [10]：正式引用 ICML 2025，实际核读 arXiv v1；E272 的来源一栏同时列出两个版本 | ICML 正式版增加了 token 开销的附录 D（arXiv v1 只到附录 C）[E457]；正式版表 4 中 MindAct* 基线的跨域数值与 arXiv v1 不同，而正式版自己的表 10 和正文中的跨域增益仍对应 v1 的数值 [E458] | 引用 AWM 的开销数字以正式版附录 D 为准，合计 10.8% 不受影响，但正文对判分和归纳两项的分配与表 11 相反 [E457]；引用跨域结果时写明版本和所用基线数值。补充 D201（模型名称的版本差异和 10.8% 已在 D201 记录，原文不改）：本条新增的是表 4 基线数值和正文对表 11 两项分配的差异。E272 已写明开销数字出自正式版附录 D，不需要改数字。 |
| D329 | Darwin Gödel Machine 的版本 | Codex 报告文献 [3]：正式引用 ICLR 2026，实际核读 arXiv v2 | v2 正文和附录 A.3 对父代选择的说法，与附录 C.2 给出的权重公式方向不一致 [E459]。核对库 w050 读的是 v3 | 报告引用的内容不受这一点影响。引用父代选择规则时以附录 C.2 的公式为准；后续引用以 v3 为准。 |
| D330 | StarHarness 的费用口径 | Codex 报告第 45 行：“部署 API 费用另行报告”；`research/2026-09-29-part3-report-support.md:10`（V2）：“任务分数目标与部署 API 费用分别描述”（D319 只写了保留“StarHarness 的任务分数目标”口径） | arXiv v1：报告的是按 OpenAI 公开价格估算的每任务推理费用 [E367]；选择目标是平均任务分数 [E368]；关于演化过程，论文给出的是被接受的补丁数 [E460]；作者说明在 AutomationBench 上无法分离单个工具的贡献 [E366] | “部署 API 费用”改为“按公开价格估算的每任务推理费用”（report-support 第 10 行的替换文字见第 3a 节）。所读版本中没有找到演化过程自身的 token、金额或耗时，所以不能从中推出回本点。 |
| D331 | 环境知识的来源 | Codex 报告第 55 行把 ActionEngine 和 AppAgentX 同列为“环境表示和历史轨迹复用”的近邻；第 217 行把 AutoDroid-V2 写成“学过的脚本” | ActionEngine 的初始状态机来自离线爬取，构建时不看后面的任务 [E382]，主要结果用的是预热后的状态机：按评测任务模板各生成并执行一个任务，由 Patcher 修正 [E383] [E384]；AppAgentX 从 agent 自己的运行轨迹生成快捷动作，论文没有描述生成后的保留或丢弃检验 [E461] [E462]；AutoDroid-V2 的应用文档来自应用探索历史，每个任务由经过微调的本地模型现写一个脚本 [E450] [E463]，与 PPT 的描述一致（`slides/build_deck.py:1408`、`:1633`） | 三者分开写：专门探索建模型（ActionEngine、AutoDroid-V2 的应用文档）；从自身轨迹生成快捷动作但论文没有描述检验（AppAgentX）；从任务轨迹学习并检验后采用（已有 ASI，检验由模型裁判判定 [E410] [E411]；本方案要做的是用答案库检验）。已核实条目中，ActionEngine 和 AutoDroid-V2 的环境知识来自爬取或探索 [E382] [E450]，MobileGPT 的页面条目来自随机探索和用户操作记录 [E449]。 |
| D332 | 第七章对应表的记账 | Codex 报告第 192–203 行和 D320（`research/2026-09-29-part3-report-support.md:30`）：“宏动作可能只移除中间模型决策，不能同时计两次收益” | 本审阅 1.4 节 F3–F7：报告第 199–203 行已提醒表中各行是因果路径、不能相加，但还缺具体规则：整轮消失与其中调用、步数下降与成功率上升、中间调用与上下文变短，这三对都可能被分别估算再相加；方案自己带来的开销缺 action 内部的模型调用和回退的恢复轮次 | D320 的原则保留，补充三条规则：(1) 报告收益时以不随粒度改变的计数为准（总模型调用、总非模型时间、底层操作数）；(2) 每成功收益只用全部尝试的实测总额除以成功数，不把分项估计相加；(3) 每次版本切换后部署运行里多出的缓存写入计入部署账本。 |
| D333 | 报告没有提到的 PPT 主线近邻 | Codex 报告第 215–225 行和 D320：“现有 Part 2 已含多篇近邻” | PPT 主线上的 ASI（`:1423`）和 EchoPath（`:1409`、`:1634`）没有出现在报告中。ASI 从 agent 的运行轨迹归纳程序技能，用改写后的轨迹重跑同一查询，只有模型裁判判为完成、新技能被调用且调用改变了环境时才加入 action [E410] [E411]；EchoPath 只把通过外部评测的首次运行轨迹存成带参数的可调用记忆，回放前做兼容性检查 [E412] [E413] [E414] | 补入近邻表，两项都属于方向二。PPT 主线上的页面裁剪程序（`:1453`）也没有出现在报告中，但那项工作的作者单位只有一家公司的研发部门，按来源规则暂缓，报告不引用它与来源规则一致；PPT 的历史引用没有按新规则重审，是否保留由 Edwin 决定。 |
| D334 | “文献已足以支持可行性” | Codex 报告第 11 行（已限定为“已评测设定中的可行性”，同段把净收益列为未回答的问题） | 在 Terminal-Bench 2.1 上，各方法的轮数预算相同（K=5，没有报告 token 或金额总量）[E420]，harness 演化在 34 个留出任务上的收益为 +0.0 到 +1.2 个百分点 [E421]，没有单元测试反馈时 GPT-5.4 的成绩下降 [E362]，用单元测试作反馈和挑选时并行采样的成绩更高 [E422]；在六个基准组成的流式任务上，五种自进化方法对 GPT-5.4 的平均收益在三种场景下都为负，对另两个模型为 +0.9 到 +2.7 个百分点 [E464]；在 WebArena 上，步数上限放宽到 15 步并加了基于规则的页面裁剪的普通 agent，成功率高于在线的技能和记忆模块 [E428] [E429]；自动设计 agent 计入设计成本后只有少数设置能回本 [E334]；一次性建设的环境模型和工具有回本点的报告，ActionEngine 的回本点不含预热修正的开销 [E332] [E333] | 改为两句：在有可靠对错信号的已评测设定中，两个方向都有做得成的先例；计入改进自身开销的报告很少，其中一次性离线建设有回本点 [E332] [E333]，自动设计 agent 只在少数设置里回本 [E334]，在线的技能和记忆模块不如步数放宽并加裁剪的普通 agent [E429]，另有几项工作的改进收益本身就很小或为负 [E421] [E464]；持续运行的改进循环连同维护开销能否回本，在已核对的文献里没有找到。 |
| D335 | 问题一的对照已有人做过 | Codex 报告第 119 行：只说 HarnessFix 已有诊断和修改路由；D319（`research/2026-09-29-part3-report-support.md:28`）：“诊断路由、可执行框架修改、环境惯例工具化和多轮筛选均已有近邻” | HarnessFix 的消融已在同一系统内去掉基于轨迹的诊断（修复上下文改用原始轨迹摘要），在 GAIA、SWE、AppWorld、TB2 上的完成率都低于完整方法，但所引条目没有报告各变体的改进资源用量 [E356]；ContractSkill 在 MiniWoB 上去掉失败定位的消融也低于完整方法 [E437]；与通用修改器、只改文字的方法做的跨系统比较中，系统之间的差别不止一处 [E359] [E415] [E418]，其中 AHE 只报告了一次演化，演化和报告用的是同一组任务 [E418]，AutoSaddler 的开销曲线每种方法只有一次优化 [E416]；另外，在一项文本分类的执行框架搜索里，提议模型能否看到完整轨迹会明显改变结果 [E419]，所以对照组的轨迹访问权限也要固定 | 本条补充 D319，D319 原文不改。问题一写明：要补的是在相同且报告出来的改进资源下只开关“选位置”的对照，并让修改去向包含新 action 和环境条件。 |

## 3 E-ledger patches

本节只给台账条目的替换或追加文字。canonical v3 不改；以下补丁在合并 v3.1 时应用，本次没有改动任何现有文件。Codex 报告本身不改。每条补丁的“把 X 替换为 Y”中，X 是现有行里的原句（已核对在该文件中唯一出现）。3a 前五条是 E 条目的补丁，其后四条是其他研究文件里的行；3c 是供我方下一稿使用的写法，放在这里便于与 N1–N8 对照。

### 3a 现有条目的替换文字

**E230（WALT）**，`research/2026-09-28-part2-acceleration-by-term.md:1022`，依据 D327：

- 来源一栏：把 `(ICLR 2026 poster; camera-ready not readable)` 替换为 `(ICLR 2026 poster; construction cost from the camera-ready, https://proceedings.iclr.cc/paper_files/paper/2026/hash/5b175f9e93873e3a10a6ce43dbb82e05-Abstract-Conference.html, §4.6, read 2026-09-29, primary, peer-reviewed; D327)`。
- 备注一栏：把 `Discovery cost per site not quantified; "1.3–1.4×" is a per-split range (D168)` 替换为 `arXiv v1 names a per-site exploration and validation cost without a figure [E409]. The ICLR 2026 camera-ready (§4.6) gives it for Online-Mind2Web only, not for VisualWebArena (this row): 305 tool candidates on 139 websites, 252 validated (82.6%), 1.75 attempts per tool on average; $1.67 per tool priced at GPT-5 rates used as an example (proposal $0.26, amortised across the tools of a site; demonstration $0.87; generation $0.46; testing $0.08); the paper does not say which model ran construction or whether token counts were measured; break-even after about 14 uses per tool against a baseline inference cost of $0.12 per task (authors' arithmetic); no time figure is given [E333] (D327). "1.3–1.4×" is a per-split range (D168)`。

**E271（SpeedRunner）**，同文件 `:1063`，依据 D323：

- 备注一栏：把 `| P2C | D172 |` 替换为 `| P2C | D172; the paper's cost figures (Figure 3, gpt-5.4-mini) are per episode on the 30-episode held-out test set at training checkpoints, with inducer calls amortised over the rollouts of their batch; §4.3 calls the metric output tokens and App. A.3 dollars (D172); no cumulative-cost plot was found in v1; evaluated on ScienceWorld, BabyAI and Crafter only; updates are learned online with no task replay and no held-out set deciding an update, regression checks being left to the inducer (D323) [E328] [E329] [E389] [E391] |`（`| P2C | D172 |` 在该文件中只出现一次，第 1063 行）。
- 待查：本行现有的数字是 App. G.2 中 Gemini-3-Flash 下的模型调用次数，而 [E329] 写明主实验用 gpt-5.4-mini；两者的关系本次没有核清，列入第 4 节。

**E272（Agent Workflow Memory）**，同文件 `:1064`，依据 D322、D328：

- 备注一栏：把 `D41, D201` 替换为 `D41, D201; a workflow holds program-format action steps with named placeholders and is placed in the prompt as guidance, and only the AWM_AS variant wraps workflows as callable actions (D322) [E324] [E326] [E325]; the overhead figure is in the ICML version only, whose text assigns the evaluation and induction shares the other way round from its Table 11 (D328) [E457]`。

**E321（ReasoningBank）**，`research/2026-09-29-part3-related-work-survey.md:174`，依据 D324：

- 把 `所报 actor 执行减少不等于含判断与记忆提炼的总 token 降低。` 替换为 `所报 actor 执行减少不等于含判断与记忆提炼的总 token 降低。成本指每任务平均 token，没有金额和时间；多出的 token 来自判分和经验提取调用，检索开销没有单列；成本表没有写明对应的基准和模型（D324）[E335] [E336]。`

**E323（On the Fragility of Self-Improving Agents）**，同文件 `:176`，依据 D325：

- 把 `检验多次运行和任务顺序对记忆方法的影响；` 替换为 `检验多次运行和任务顺序对两种基于记忆的方法（AWM、ReasoningBank）的影响，每个实验三次运行；ReasoningBank 在默认顺序下比无记忆基线高 1.5 个百分点，打乱顺序后低 4.5 个百分点（该句未写基准）；作者认为默认顺序隐含由易到难的安排（D325）[E402] [E401] [E403]；`

**AWM 的表示形式（两处）**，依据 D322：

- `research/2026-09-29-part3-related-work-survey.md:75`：把 `不能把文字 workflow 当无需模型介入的可执行 macro。` 替换为 `workflow 由自然语言描述加程序格式的动作步骤组成，默认放进提示作为参考，每一步仍由模型决定；只有变体 AWM_AS 把它封装为可调用动作（D322）。`
- `research/2026-09-29-part3-report-support.md:23`：把 `AWM 为文字工作流；` 替换为 `AWM 的 workflow 放进提示作为参考，每一步仍由模型决定，只有变体 AWM_AS 可调用（D322）；`

**StarHarness 的费用口径**，`research/2026-09-29-part3-report-support.md:10`，依据 D330：

- 把 `任务分数目标与部署 API 费用分别描述。` 替换为 `任务分数目标与按公开价格估算的每任务推理费用分别描述（D330）。`

**规则派生用例的归属**，`research/2026-09-29-part3-report-support.md:34`，依据 D326：

- 把 `规则派生用例在读者报告中明确记为跨会话候选建议，` 替换为 `规则派生用例是 Edwin 的设想（D314、D326），读者报告曾记为跨会话候选建议，`

**F1(e)（step 0）**，`research/2026-09-28-problem-definition.md:34`，依据 D321：

- 把 `OSWorld-Human S2's "retrieval (once)", pre-task planning, and amortised learning calls.` 替换为 `OSWorld-Human S2's "retrieval (once)" and pre-task planning. Amortised learning calls are not in step 0; they sit outside the per-attempt formula, as C_setup/n in Part 2 Appendix B8 or in the learning-and-maintenance ledger (D321).`

### 3b 新增条目

新增条目为第 1.6 节证据表中的 E324–E643，每条含数字、测量定义、来源网址与版本、日期和一手或二手标签。合并 v3.1 时整表追加。

### 3c 供我方下一稿使用的写法

下列写法对应第 1.2 节需要修改的 8 处。它们写进我方下一稿方案，不用于改写 Codex 报告。

| 对应 | 建议写法 |
|---|---|
| N1 | AWM 从过往轨迹归纳带命名占位符的子流程，默认放进提示作为参考，每一步仍由模型决定 [E324] [E326]；把工作流封装成可调用动作的变体在 Mind2Web（gpt-4）上只在少部分任务中被调用，任务成功率没有提高 [E325]。 |
| N2 | SpeedRunner 在 ScienceWorld、BabyAI、Crafter 上（gpt-5.4-mini）报告，它是唯一在训练过程中每轨迹成本下降的方法，成本在固定的留出测试集上按检查点测量，归纳调用按批次摊入 [E331] [E329] [E328]；论文对这一成本是输出 token 还是美元前后说法不一 [E329] [E330]。沿任务流的累计投入与累计节省，已核实的工作中只有一次性建设或设计成本的回本分析 [E332] [E333] [E334]。 |
| N3 | ReasoningBank 的每任务 token 比无记忆基线高约 4.3%，多出的部分来自判分和经验提取调用，动作生成一栏低于基线（该表未写明基准和模型）[E335] [E336]；在 WebArena、Gemini-2.5-flash 上，平均步数从 9.7 降到 8.3 [E465] [E466]。 |
| N4 | 引用 [17] 只跟在 ReasoningBank 一句后面；“把质量和 token 约束纳入改进过程”只引 SoL-Pi 和 RRSI [E392] [E396]。 |
| N5 | SOPBench 由程序按约束条件枚举组合，模型只为每个指定组合生成具体数据 [E451] [E467]；LogiSafetyGen 由模型从法规文本提出候选规则，经校验器和作者审核后，由搜索程序生成合规轨迹 [E342] [E456] [E453] [E343]；由模型从规则手册推出情境和边角案例、人工简单确认，是 Edwin 的设想，由我方检验。 |
| N6、N7 | 最终测试另行保留、生成器不得修改规则和答案，是本方案自己的设计规则；后者与 SOPBench 的分工一致 [E350]。 |
| N8 | SOPBench 检查不得执行不被允许的操作、不得跳过规定的前置校验 [E468] [E469]；“必须询问”对应 Edwin 说的每次运行时询问或规划（对象未定），检查需要我方自己设计。 |

## 4 Still open

**需要 Edwin 决定的事项**

1. 引文方式：本文只给原文的章节、表号和行号，不抄录原文句子。仓库规则要求核对表带原文引句，是否接受这种写法；不接受的话，由核对库的锚点补入。
2. 第一阶段提取环境知识时是否只用既有日志（我方前稿提出、Codex 报告采纳的方案建议）。已核实条目中，ActionEngine 的状态机来自离线爬取 [E382] [E448]，MobileGPT 的页面条目来自随机探索和用户操作记录 [E449]，AutoDroid-V2 的应用文档来自应用探索历史 [E450]；AppAgentX 从自身运行轨迹生成快捷动作，但论文没有描述生成后的检验 [E461] [E462]。
3. 答案库怎么建、由谁确认。SOPBench 的条件由程序枚举、校验程序由人编写 [E451] [E340]；LogiSafetyGen 由模型提出候选规则、作者三轮一致审核，保留 73.9% [E342] [E453] [E454]；两篇都没有给出人工确认的工作量，“模型推情境、人工简单确认”的工作量要自己测。
4. 是否把训练辅助模型（例如单独的编辑模型）列入范围，还是留到后面的阶段。
5. 改进循环在哪个环境里运行（团队现有系统、复制品或两层），是否在最终提交前停下。
6. 业务正确性与成本的优先顺序，以及是否允许以容忍度的形式接受小幅质量下降。
7. “询问或规划”里问的是模型、环境还是用户。
8. SAP Concur 的产品文档在来源筛选中被判为不合格（属于普通公司的产品文档）。“循环在哪里跑”需要的是团队所用系统的事实，由团队自己确认即可，不必作为文献引用。
9. GitHub 的官方工程文章是否算头部公司的官方材料。本文和方案稿都按“算”处理，并标为非同行评审的官方博客。
10. PPT 主线上的页面裁剪程序一项（Enomoto 等，作者单位为 NEC）按新的来源规则暂缓。PPT 的历史引用没有按新规则重审，是否保留由 Edwin 决定。

**文献方面尚未核清的事项**

- LearnAct 的“COLM 2024 main conference”中“main conference”这一限定没有核实：COLM 官方录用名单上有这篇论文，但 OpenReview 页面被人机验证拦截。
- SOPBench 已列入 EMNLP 2026 主会官方日程，论文集尚未出版；正式发表信息待论文集上线后补全。
- HarnessFix 的消融表没有写明用的是哪个数据划分，也没有报告各消融变体的资源用量。
- ReasoningBank 的成本表没有写明对应的基准和模型。
- AWM arXiv v1 中 AWM_AS 的任务成功率，表与正文不一致；ICML 正式版表 4 的 MindAct* 跨域基线与其表 10 和正文不一致。
- E271 现有的数字是 App. G.2 中 Gemini-3-Flash 下的模型调用次数，而所引条目写明主实验用 gpt-5.4-mini；两者的关系没有核清。
- 与问题一、二直接相关但按来源规则暂缓或排除的工作：PRISM、DARC、REBASE、“Where Does Harness-Optimization Value Live?”、“Do Agent Optimizers Compound?”。它们在正式发表或补上合格机构署名后可以重新纳入。

**仓库方面**

- 第 3a 节的补丁（E230、E271、E272、E321、E323，survey 第 75 行，report-support 第 10、23、34 行，problem-definition 第 34 行）在 v3.1 合并时应用。本次没有改动这些文件。
- PPT 中两处过时的页码指向（`slides/build_deck.py:1401`、`:1620`）没有修改，留给负责 slides 的会话。
- 核对库（所存全文、逐条锚点、审计记录）保存在仓库之外：`~/.claude/projects/-Users-edwin-projects-agent-acceleration-research/part3-verification/`。核对脚本随本文一并提交到 `tools/evidence-check/`。
- 我方方案稿见 `notes/part3/2026-09-29-part3-plan-claude-zh.md`；预算按 Edwin 的要求暂不计算。

## References

### A. Codex 报告引用的 23 篇（沿用报告的编号 [1]–[23]）

以下条目照录自 `notes/part3/2026-09-29-part3-research-plan-report-zh.md` 的参考文献。本次审阅逐条核对了作者、题目、发表信息和所读版本：正式发表的条目在会议官方页面上确认，预印本条目确认 arXiv 记录中没有发表信息。

[1] Shaokun Zhang; Jieyu Zhang; Jiale Liu; Linxin Song; Chi Wang; Ranjay Krishna; Qingyun Wu (2024). *Offline Training of Language Model Agents with Functions as Learnable Weights*. ICML 2024, main conference; Proceedings of Machine Learning Research 235:60315–60335。[论文](https://proceedings.mlr.press/v235/zhang24cd.html)。

实际核读版本：[arXiv 2402.11359v4](https://arxiv.org/html/2402.11359v4)。

[2] Lakshya A Agrawal; Shangyin Tan; Dilara Soylu; Noah Ziems; Rishi Khare; Krista Opsahl-Ong; Arnav Singhvi; Herumb Shandilya; Michael J Ryan; Meng Jiang; Christopher Potts; Koushik Sen; Alex Dimakis; Ion Stoica; Dan Klein; Matei Zaharia; Omar Khattab (2026). *GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning*. ICLR 2026, main conference。[论文](https://proceedings.iclr.cc/paper_files/paper/2026/hash/0e9e708b6f48e14fd0ac29e167413f76-Abstract-Conference.html)。

实际核读版本：[arXiv 2507.19457v2](https://arxiv.org/pdf/2507.19457v2)。

[3] Jenny Zhang; Shengran Hu; Cong Lu; Robert Lange; Jeff Clune (2026). *Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents*. ICLR 2026, main conference Poster。[论文](https://iclr.cc/virtual/2026/poster/10007327)。

实际核读版本：[arXiv 2505.22954v2](https://arxiv.org/html/2505.22954v2)。

本次审阅补充：核对库读的是 arXiv v3（2026-03-12），与 ICLR 正式版更接近；两版差异见 D329。

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

本次审阅补充：另读了 ICML 2025 正式版 PDF（PMLR 267）；两版差异见 D328。

[11] Haiteng Zhao; Chang Ma; Guoyin Wang; Jing Su; Lingpeng Kong; Jingjing Xu; Zhi-Hong Deng; Hongxia Yang (2024). *Empowering Large Language Model Agents through Action Learning*. Conference on Language Modeling (COLM 2024), main conference。[论文](https://openreview.net/forum?id=KqK5XcgEhR)。

实际核读版本：[arXiv 2402.15809v2](https://arxiv.org/html/2402.15809v2)。

本次审阅补充：“main conference”这一限定未能核实，见第 4 节。

[12] Viraj Prabhu; Yutong Dai; Matthew Fernandez; Krithika Ramakrishnan; Jing Gu; Yanqi Luo; Silvio Savarese; Caiming Xiong; Junnan Li; Zeyuan Chen; Ran Xu (2026). *WALT: Web Agents that Learn Tools*. International Conference on Learning Representations (ICLR 2026), Conference / poster。[论文](https://proceedings.iclr.cc/paper_files/paper/2026/hash/5b175f9e93873e3a10a6ce43dbb82e05-Abstract-Conference.html)。

实际核读版本：[arXiv 2510.01524v1](https://arxiv.org/html/2510.01524v1)。

本次审阅补充：另读了 ICLR 2026 正式版 PDF；建设成本只在正式版中，见 D327。

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


### B. 本审阅补充引用的文献（按核对库记录号）

每条给出正式引用和实际核读的版本。来源等级按 Edwin 2026-09-29 的来源规则（D313）判定：顶刊顶会优先；其次是头部 AI 公司的官方技术材料；知名高校和成熟研究机构的预印本作为补充。作者自述的录用不算已确认发表。方括号里是核对库的记录号。

**[g118] Batu El; Mert Yuksekgonul; James Zou (2025).** *Inefficiencies of Meta Agents for Agent Design*. Findings of the Association for Computational Linguistics: EMNLP 2025 (Findings track), pages 20815-20824, Suzhou, China, November 2025; DOI 10.18653/v1/2025.findings-emnlp.1135。[正式引用](https://aclanthology.org/2025.findings-emnlp.1135/)。

实际核读版本：[arXiv v1 (HTML full text; PDF text also saved at 2510.06711…](https://arxiv.org/html/2510.06711v1)。来源等级：顶刊顶会。机构：Stanford University (all three authors)

**[w102] Yike Wang; Huaisheng Zhu; Zhengyu Hu; Yige Yuan; Zhengyu Chen; Shakti Senthil; Hannaneh Hajishirzi; Yulia Tsvetkov; Pradeep Dasigi; Teng Xiao (equal contribution: Yike Wang, Huaisheng Zhu, Teng Xiao) (2026).** *Rethinking the Evaluation of Harness Evolution for Agents*. arXiv 预印本，未核到正式发表。[正式引用](https://arxiv.org/abs/2607.12227)。

实际核读版本：[v2 (arXiv HTML; tables cross-checked against the v2 PDF tex…](https://arxiv.org/html/2607.12227v2)。来源等级：合格机构补充。机构：Allen Institute for AI (Yike Wang, Pradeep Dasigi, Teng Xiao); University of Washington (Yike Wang, Zhengyu Hu, Yige Yuan, Shakti Senthil, Hannaneh Hajishirzi, Yulia Tsvetkov); Independent (Huaisheng Zhu, Zhengyu Chen) 另有一份独立记录 n004。

**[h014] Zora Zhiruo Wang; Apurva Gandhi; Graham Neubig; Daniel Fried (2025).** *Inducing Programmatic Skills for Agentic Tasks*. COLM 2025 (Conference on Language Modeling), accepted paper, main conference (listed on the official "COLM 2025: Accepted Papers" page without a Spotlight badge)。[正式引用](https://openreview.net/forum?id=lsAY6fWsog)。

实际核读版本：[v2](https://arxiv.org/pdf/2504.06821v2)。来源等级：顶刊顶会。机构：Carnegie Mellon University (all four authors)

**[h032] Yao Zhao; Aditya Shanmugham; Swastik Roy; Yanxun Xu (2026).** *EchoPath: Execution-Level Replayable Memory for GUI Agents*. arXiv 预印本，未核到正式发表。[正式引用](https://arxiv.org/abs/2609.16635v1)。

实际核读版本：[v1 (the only version; arXiv HTML, cross-checked against the…](https://arxiv.org/html/2609.16635v1)。来源等级：合格机构补充。机构：Johns Hopkins University (Department of Applied Mathematics and Statistics; Division of Quantitative Sciences, Department of Oncology, Johns Hopkins University School of Medicine); Amazon AGI

**[w006] Sungho Park; Wonjoong Kim; Rongyuan Tan; Jue Zhang; Wook-Shin Han; Pengfei Gao; Chanyoung Park; Yongqiang Yao; Rao Fu; Elsie Nallipogu; Qingwei Lin; Saravan Rajmohan; Dongmei Zhang (2026).** *AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces*. arXiv 预印本，未核到正式发表。[正式引用](https://arxiv.org/abs/2608.23041v1)。

实际核读版本：[v1](https://arxiv.org/html/2608.23041v1)。来源等级：合格机构补充。机构：POSTECH; KAIST; Southern University of Science and Technology; Microsoft. The HTML only partly maps authors to institutions. The first three authors did the work as Microsoft interns; the corresponding authors are Jue Zhang (Microsoft) and Wook-Shin Han (POSTECH).

**[w009] Jiahang Lin; Shichun Liu; Chengjun Pan; Lizhi Lin; Shihan Dou; Zhiheng Xi; Xuanjing Huang; Hang Yan; Zhenhua Han; Tao Gui; Yu-Gang Jiang (2026).** *Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses*. arXiv 预印本，未核到正式发表。[正式引用](https://arxiv.org/abs/2604.25850)。

实际核读版本：[v4 (arXiv PDF text; the v4 HTML text, sources/2604.25850v4.…](https://arxiv.org/pdf/2604.25850v4)。来源等级：合格机构补充。机构：Fudan University; Peking University; Shanghai Qiji Zhifeng Technology Co., Ltd. (precedent E320; the v4 PDF title block spells it 'Shanghai Qiji Zhifeng Co., Ltd')

**[w004] Yoonho Lee; Roshen Nair; Qizheng Zhang; Kangwook Lee; Omar Khattab; Chelsea Finn (2026).** *Meta-Harness: End-to-End Optimization of Model Harnesses*. COLM 2026 (Conference on Language Modeling), conference paper. OpenReview gives venue "COLM 2026", venueid colmweb.org/COLM/2026/Conference, publication date 2026-07-08. The official "COLM 2026 Accepted Papers" page lists it as a poster (Grand Ballroom, Poster Session 3, #123).。[正式引用](https://openreview.net/forum?id=tmbOUyFx3R)。

实际核读版本：[v1 (arXiv HTML, only version listed)](https://arxiv.org/html/2603.28052v1)。来源等级：合格机构补充。机构：Stanford University; KRAFTON; Massachusetts Institute of Technology

**[w035] Amine El Hattami; Nicolas Chapados; Christopher Pal (2026).** *SKILL.nb: Selective Formalization and Gated Execution for Durable Agent Workflows*. FAGEN@ICML 2026 Poster (ICML 2026 workshop, venueid ICML.cc/2026/Workshop/FAGEN; not the ICML main conference)。[正式引用](https://arxiv.org/abs/2606.08049)。

实际核读版本：[v1 (arXiv HTML)](https://arxiv.org/html/2606.08049v1)。来源等级：合格机构补充。机构：ServiceNow Research (all three); Mila and Polytechnique Montréal (El Hattami, Pal); Canada CIFAR AI Chair (Pal)

**[w054] Susheel Suresh; Hazel Mak; Sahil Bhatnagar; Chhaya Methani; Alejandro Gutierrez Munoz (2026).** *Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents*. arXiv 预印本，未核到正式发表。[正式引用](https://arxiv.org/abs/2609.11060)。

实际核读版本：[v1](https://arxiv.org/html/2609.11060v1)。来源等级：合格机构补充。机构：Microsoft Corporation, One Microsoft Way, Redmond, WA (the only affiliation block, covering all five authors; not labelled Microsoft Research)

**[w013] Sina Hajimiri; Masih Aminbeidokhti; Jose Dolz; Ismail Ben Ayed; Issam H. Laradji; Spandana Gella; Nicolas Gontier (2026).** *Are Online Skill and Memory Modules Always Worth Their Tokens? A Budget-Constrained Study of Web Agents*. EMNLP 2026 (The 2026 Conference on Empirical Methods in Natural Language Processing), main conference, paper ID 4950-MAIN, poster (Session 4, Poster Session B, 2026-10-25)。[正式引用](https://arxiv.org/abs/2606.15017)。

实际核读版本：[v2 (arXiv HTML; v1 HTML also saved and diffed for version c…](https://arxiv.org/html/2606.15017v2)。来源等级：顶刊顶会。机构：ServiceNow AI Research; ÉTS Montréal; University of British Columbia; McGill University

**[n016] Jihye Choi; Jinsung Yoon; Long T. Le; Somesh Jha; Tomas Pfister (2026).** *PolicyBank: Evolving Policy Understanding for LLM Agents*. arXiv 预印本，未核到正式发表。[正式引用](https://arxiv.org/abs/2604.15505)。

实际核读版本：[v1 (arXiv HTML, all sections, Tables 1-8 text and Appendix…](https://arxiv.org/abs/2604.15505v1)。来源等级：合格机构补充。机构：Google Cloud (Choi, Yoon, Le, Pfister); University of Wisconsin-Madison (Choi, Jha). Choi's work was done as a research intern at Google Cloud.

**[g037] Boqin Yuan; Yue Su; Renchu Song; Sen Yang; Jing Qin (2026).** *ClawTrace: Cost-Aware Tracing for LLM Agent Skill Distillation*. Agent Skills '26 Workshop at ACM CAIS 2026 (ACM Conference on AI and Agentic Systems), San Jose, May 26, 2026; OpenReview venue 'AgentSkills 2026 Oral'; workshop is non-archival。[正式引用](https://arxiv.org/abs/2604.23853)。

实际核读版本：[v2 (arXiv HTML; appendix C prompts checked in the v2 PDF te…](https://arxiv.org/html/2604.23853v2)。来源等级：合格机构补充。机构：University of California San Diego (Boqin Yuan, ucsd.edu); Carnegie Mellon University and Epsilla (Yue Su, andrew.cmu.edu; work done during an internship at Epsilla); Epsilla, Union City, NJ (Renchu Song, Sen Yang, Jing Qin)

**[g049] Hui Xue; Fan Yang (2026).** *Rethinking Self-Evolving Agents: Do We Still Need Prescribed Optimization Pipelines?*. arXiv 预印本，未核到正式发表。[正式引用](https://arxiv.org/abs/2608.09629)。

实际核读版本：[v1](https://arxiv.org/html/2608.09629v1)。来源等级：合格机构补充。机构：Microsoft Research (both authors)

**[g047] Agamdeep Singh; Srishti Gautam; Priyanshu Gupta; Nikita Mehrotra; Tanmay Bakshi; Sumit Gulwani (2026).** *Coding Agents are Strong Prompt Optimizers*. arXiv 预印本，未核到正式发表。[正式引用](https://arxiv.org/abs/2609.26261)。

实际核读版本：[v1 (arXiv HTML; PDF of v1 also saved and used only for the…](https://arxiv.org/html/2609.26261v1)。来源等级：合格机构补充。机构：Microsoft (all six authors; microsoft.com addresses, two with intern-style 't-' prefixes; the paper says 'Microsoft', not 'Microsoft Research')

**[w059] Zijian Lu; Yiping Zuo; Yupeng Nie; Xin He; Weibei Fan; Lianyong Qi; Shi Jin (2026).** *ContractSkill: Repairable Contract-Based Skills for Multimodal Web Agents*. arXiv 预印本，未核到正式发表。[正式引用](https://arxiv.org/abs/2603.20340)。

实际核读版本：[v3 (arXiv HTML, arXiv:2603.20340v3 [cs.SE])](https://arxiv.org/html/2603.20340v3)。来源等级：合格机构补充。机构：Nanjing University of Posts and Telecommunications (Lu, Zuo, Nie, He, Fan); China University of Petroleum (East China) (Qi); Southeast University (Shi Jin)

**[w039] Kevin Song; Anand Jayarajan; Yaoyao Ding; Qidong Su; Zhanda Zhu; Sihang Liu; Gennady Pekhimenko (2025).** *Aegis: Taxonomy and Optimizations for Overcoming Agent-Environment Failures in LLM Agents*. arXiv 预印本，未核到正式发表。[正式引用](https://arxiv.org/abs/2508.19504)。

实际核读版本：[v1 (arXiv HTML; the only version listed)](https://arxiv.org/html/2508.19504v1)。来源等级：合格机构补充。机构：University of Toronto and Vector Institute (Song, Jayarajan, Ding, Su, Zhu, Pekhimenko); University of Waterloo (Sihang Liu)

**[n028] Ruotian Ma; Xiaolei Wang; Xin Zhou; Jian Li; Nan Du; Tao Gui; Qi Zhang; Xuanjing Huang (2024).** *Are Large Language Models Good Prompt Optimizers?*. arXiv 预印本，未核到正式发表。[正式引用](https://arxiv.org/abs/2402.02101)。

实际核读版本：[v1 (only version listed)](https://arxiv.org/html/2402.02101v1)。来源等级：合格机构补充。机构：School of Computer Science, Fudan University; Institute of Modern Languages and Linguistics, Fudan University; Tencent AI Lab

**[n052] Tiferet Gazit (2026).** *Building an agentic memory system for GitHub Copilot*. The GitHub Blog (official GitHub engineering/product blog, not peer reviewed), January 15, 2026。[正式引用](https://github.blog/ai-and-ml/github-copilot/building-an-agentic-memory-system-for-github-copilot/)。

实际核读版本：[GitHub blog post as served on 2026-09-29; page dated Januar…](https://github.blog/ai-and-ml/github-copilot/building-an-agentic-memory-system-for-github-copilot/)。来源等级：头部公司官方材料。机构：GitHub (a Microsoft subsidiary). The author is a principal machine learning engineer at GitHub.

**[w065] Yuan Wang; Mingyu Li; Haibo Chen (2026).** *From Imperative to Declarative: Towards LLM-friendly OS Interfaces for Boosted Computer-Use Agents*. EuroSys 2026 (21st European Conference on Computer Systems, Edinburgh, April 27-30, 2026), main conference; Proceedings pages 296-310; DOI 10.1145/3767295.3803576。[正式引用](https://doi.org/10.1145/3767295.3803576)。

实际核读版本：[v2](https://arxiv.org/html/2510.04607v2)。来源等级：顶刊顶会。机构：Key Laboratory of System Software (Chinese Academy of Sciences) and Institute of Software, Chinese Academy of Sciences; University of Chinese Academy of Sciences; Shanghai Jiao Tong University

**[w062] Xiangyi Li; Yimin Liu; Wenbo Chen; Bingran You; Zonglin Di; Yifeng He; Shenghan Zheng; Kyoung Whan Choe; Jiankai Sun; Shuyi Wang; Chujun Tao; Binxu Li; Xuandong Zhao; Hejia Geng; Xiaojun Wu; Junwei Zhou; Xiaokun Chen; Hanwen Xing; Yubo Li; Qunhong Zeng; Di Wang; Yuanli Wang; Roey Ben Chaim; Penghao Jiang; Haotian Shen; Luyang Kong; Xinyi Liu; Runhui Wang; Xuanqing Liu; Jiachen Li; Xin Lan; Yueqian Lin; Wengao Ye; Junwei He; Songlin Li; Yue Zhang; Yipeng Gao; Yijiang Li; Ze Ma; Liqiang Jing; Tianyu Wang; Kaixin Li; Yiqi Xue; Haoran Lyu; Yizhuo He; Yuchen Tian; Shutong Wu; Bowei Wang; Yixuan Gao; Bo Chen; Litong Liu; Sikai Cheng; Jiajun Bao; Shuaicheng Tong; Shuwen Xu; Terry Yue Zhuo; Tinghan Ye; Qi Qi; Miao Li; Longtai Liao; Zelin Tan; Chang Shi; Xilin Tang; Srinath Tankasala; Boqin Yuan; Yaoyao Qian; Jianhong Tu; Chenguang Wang; Yizhou Sun; Wei Wang; Aaron Taylor; Ziyue Yang; Changkun Guan; Zhikang Dong; Xinyu Zhang; Steven Dillmann; Han-chung Lee; Dawn Song (2026).** *SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks*. arXiv 预印本，未核到正式发表。[正式引用](https://arxiv.org/abs/2602.12670)。

实际核读版本：[v4](https://arxiv.org/html/2602.12670v4)。来源等级：合格机构补充。机构：Lead affiliation BenchFlow (first author). Others: OSU, Amazon, UC Berkeley (Bingran You, Xuandong Zhao, Dawn Song), UC Santa Cruz, UC Davis, Dartmouth, RLWRLD, Independent, Princeton, Oxford, Stanford, USC, CMU, Foxconn, BU, Zenity, UNSW, UT Austin, MSU, Duke, ByteDance, UT Dallas, UC San Diego, Columbia, University of Rochester, Cornell Tech, Georgia Tech, Cornell, NEU, UCLA, Snap Inc., Fanshawe College, USTC, HKUST(GZ), Anyscale

**[n024] Hongqiang Lin; Chao Liu; Xiaofan Bai; Xuan Jin; Yuhong Li; Nenggan Zheng; Xipeng Cao (2026).** *Beyond Endpoint Performance: Process-Level Evaluation of Self-Evolving Agents*. arXiv 预印本，未核到正式发表。[正式引用](https://arxiv.org/abs/2609.24663)。

实际核读版本：[v1 (the only version listed)](https://arxiv.org/html/2609.24663v1)。来源等级：合格机构补充。机构：Zhejiang University (Hongqiang Lin, Nenggan Zheng); Alibaba Group (Chao Liu, Xiaofan Bai, Xuan Jin, Yuhong Li, Xipeng Cao). Lin and Liu carry an asterisk whose meaning is not stated; Zheng and Cao are corresponding authors.

**[g041] Congjie Zheng; Chuanyi Xue; Bin Liang; Jun Yang; Changshui Zhang (2026).** *SEAGym: An Evaluation Environment for Self-Evolving LLM Agents*. arXiv 预印本，未核到正式发表。[正式引用](https://arxiv.org/abs/2606.17546)。

实际核读版本：[v1 (arXiv HTML)](https://arxiv.org/html/2606.17546v1)。来源等级：合格机构补充。机构：Department of Automation, Tsinghua University; Beijing National Research Center for Information Science and Technology (BNRist), Tsinghua University

**[w089] Michael Nguyen; Quoc Nguyen; Paul Vuong (2026).** *Recursive Self-Evolving Agents via Held-Out Selection*. arXiv 预印本，未核到正式发表。[正式引用](https://arxiv.org/abs/2606.28374)。

实际核读版本：[v1 (arXiv HTML; PDF text of v1 also saved at sources/2606.2…](https://arxiv.org/html/2606.28374v1)。来源等级：合格机构补充。机构：School of Information Technology, Monash University Malaysia

**[w070] Sunjae Lee; Junyoung Choi; Jungjae Lee; Munim Hasan Wasi; Hojun Choi; Steven Y. Ko; Sangeun Oh; Insik Shin (2024).** *MobileGPT: Augmenting LLM with Human-like App Memory for Mobile Task Automation (arXiv listing title: Explore, Select, Derive, and Recall: Augmenting LLM with Human-like Memory for Mobile Task Automation)*. Proceedings of the 30th Annual International Conference on Mobile Computing and Networking (ACM MobiCom 2024), research paper, pp. 1119-1133。[正式引用](https://doi.org/10.1145/3636534.3690682)。

实际核读版本：[v3 (arXiv HTML text; the v3 PDF text was also saved at sour…](https://arxiv.org/html/2312.03003v3)。来源等级：顶刊顶会。机构：KAIST School of Computing; Simon Fraser University; Korea University; Fluiz Corp. (Insik Shin, listed with KAIST) 另有一份独立记录 h034，读的是同一版本。

**[h015] Hao Wen; Shizuo Tian; Borislav Pavlov; Wenjie Du; Yixuan Li; Ge Chang; Shanhui Zhao; Jiacheng Liu; Yunxin Liu; Ya-Qin Zhang; Yuanchun Li (2025).** *AutoDroid-V2: Boosting SLM-based GUI Agents via Code Generation*. Proceedings of the 23rd Annual International Conference on Mobile Systems, Applications and Services (ACM MobiSys '25), June 23-27, 2025, Anaheim, CA, USA; main research-paper track (listed on the official MobiSys 2025 Accepted Papers page, with a Best Artifact Award); pp. 223-235。[正式引用](https://doi.org/10.1145/3711875.3729134)。

实际核读版本：[arXiv v3 (HTML full text; PDF v3 also saved at sources/2412…](https://arxiv.org/html/2412.18116v3)。来源等级：顶刊顶会。机构：Institute for AI Industry Research (AIR), Tsinghua University; Shanghai Artificial Intelligence Laboratory; Beijing Academy of Artificial Intelligence (BAAI)

**[n025] Dong Yan; Jian Liang; Dapeng Hu; Ran He; Nicholas Jing Yuan; Qi Zhang; Tieniu Tan (2026).** *AgentStream: How Well Do Self-Evolving LLM Agents Perform Under Streaming Tasks?*. arXiv 预印本，未核到正式发表。[正式引用](https://arxiv.org/abs/2608.00155)。

实际核读版本：[v2 (PDF text; the v2 HTML text was also saved and read, but…](https://arxiv.org/pdf/2608.00155v2)。来源等级：合格机构补充。机构：School of Artificial Intelligence, University of Chinese Academy of Sciences; Microsoft; Institute of Automation, Chinese Academy of Sciences; Nanjing University (first author: work done during an internship at Microsoft)

