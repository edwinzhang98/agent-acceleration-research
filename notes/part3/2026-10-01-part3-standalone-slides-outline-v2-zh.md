# 第三部分独立演示大纲 第二版

2026 年 10 月 1 日 · 供敲定内容后制作英文 HTML Slides

这份演示讲清楚我们准备怎样研究 Agent 的环境探索与自我改进。面向有机器学习背景、未读过前两部分的听众，前两部分作为延展阅读。本稿保留两个完整方向：**主动探索环境，形成后续任务能用的知识与操作；从执行轨迹中学习，修改 Agent 自己的做法。** 两个方向分别实验，各自回答能否改善后续任务；组合不是必做内容。首轮研究同一网站、同一种流程的新输入，明确固定模型权重。

正文共 **12 页，第 1 页兼作封面**；完整参考文献和细节附录另列。**正式交付为英文 HTML Slides，包括标题、正文、图示文字、图例和附录，支持离线浏览。** 本稿的中文仅用于审阅内容，不能直接搬上正式页面。每页“上屏内容”是待译成英文的拟议正文，“图示与讲述”说明怎样把内容讲具体，“制作依据”保存来源和必要边界。

首轮明确使用 Web Agent。浏览器工具是它操作网站的接口，不另开一条通用工具使用任务线。具体网站尚未选定；以下用创建支持工单作说明，报销仍可作为另一种应用选择。示例中的网页规则是虚构的，不代表已选定基准。

## 全篇结构

| 页码 | 英文页面标题 | 听众应当理解什么 |
|---|---|---|
| 1 | Agent Acceleration through Environment Exploration and Self-Improvement | 研究对象、目标和两个方向 |
| 2 | Same Website, Same Workflow, New Inputs | 为什么不同任务可能共享经验，困难在哪里 |
| 3 | What Changes When Model Weights Stay Fixed? | 实际保存或修改什么文件，下一次怎样使用 |
| 4 | Learning Environment Knowledge and Reusable Operations | 主动交互怎样形成可用的环境知识和操作 |
| 5 | Environment Exploration: What Is Learned? | 按学习产物分类，每类如何做，有什么共同困难 |
| 6 | Evaluating Environment Exploration | 探索在什么条件下有用，怎样与已有方法比较 |
| 7 | Improving the Agent from Execution Trajectories | 怎样从失败和低效执行中提出、验证并保留修改 |
| 8 | Trajectory-Based Improvement: What Changes? | 按修改对象分类，每类如何做，有什么共同困难 |
| 9 | Evaluating Improvements Learned from Trajectories | 自动修改是否改善后续任务，新增方法有何贡献 |
| 10 | Checking Success and Measuring Time and Cost | 怎样确认做对了，怎样测耗时和费用 |
| 11 | First Experiments and Next Steps | 首轮能回答什么，何时进一步比较已有方法 |
| 12 | Resources and Initial Deliverables | 钱和算力用在哪里，先支持哪一阶段 |

## 第 1 页 我们要做什么

**英文标题：** Agent Acceleration through Environment Exploration and Self-Improvement

**上屏内容：**

我们研究 Web Agent 能否利用过去获得的知识与经验，在把任务做对的前提下，让后续任务更快、累计费用更低。

- 探索环境：主动交互，学习功能、操作条件和行为规律。
- 从执行轨迹学习：分析失败与低效执行，修改提示、工具或执行流程。
- 首轮固定模型权重，先测同一网站、同一流程的新输入。时间与费用分别评估，学习投入也计入。

**图示与讲述：** 连续展示两张工单：标题和内容不同，创建流程相同。下方标出主动探索与轨迹学习两条独立路线；说明这是研究目标，尚无本项目的实验收益。

**制作依据：** [问题定义](2026-09-30-agent-acceleration-problem-framing-zh.md)与[最新相关工作分析](2026-10-01-agent-acceleration-related-work-analysis-zh.md)。这里给项目定位，不把重复任务或固定模型定义成整个 Agent 加速领域的范围。

## 第 2 页 先把任务和环境说清楚

**上屏内容：**

第一轮：同一个网站，同一种流程，换新的输入。

| 保持相同 | 每项任务改变 |
|---|---|
| 网站的界面、规则、权限和创建工单流程 | 工单标题、类别、描述及该类别需要的信息 |

例如，先创建“登录失败”工单，再创建“上传失败”工单。它们是不同任务实例，不是两个不同网站。

先测这一范围。新流程、网站改版、跨网站迁移分别作为后续实验。

**图示与讲述：** 并排画两张工单输入，共同指向同一个网站。执行前恢复到可比初态；网页运行状态会随操作变化，但网站规则和布局在首轮固定。若换回报销例子，就是同一个系统中填不同报销单。

**制作依据：** 这是实验设置的提案。具体网站未定，首轮不承诺跨网站或任意任务泛化。

## 第 3 页 不训练模型时 实际更新什么

**上屏内容：**

| 更新对象 | 工程上的例子 | 下一次怎样使用 |
|---|---|---|
| 网站知识 | `site-guide.md` | 把有关的说明加入模型上下文 |
| 执行提示词 | `policy-prompt.md` | 作为 Agent 的执行指令加载 |
| 可调用操作 | `create_ticket.py` | 注册成 Agent 可以调用的浏览器工具 |
| 控制程序 | `runner.py` | 改变观察、执行、检查与重试的顺序 |

模型权重保持不变。两个方向都可能产生上述修改，但第一轮各只改一个对象，便于解释结果。

**图示与讲述：** 中间画同一个冻结权重的模型，周围标出具体文件及加载入口。harness 指模型外围组织执行的程序；讲每个方法时直接说改了哪个文件或组件，不用这个统称替代具体解释。文件名均为拟议示例。

**制作依据：** [文献分类与工程对象](2026-10-01-part3-literature-map-zh.md)。探索方向关注怎样主动获得环境信息，轨迹方向关注怎样利用已有执行记录改进做法；分类轴不同，产物可以重叠。

## 第 4 页 方向一 探索网站后保存什么

**上屏内容：**

英文示意页按三个步骤展开：

1. **Explore and check.** 改变工单类型，观察网页反馈，再换输入验证。
2. **Save what was learned.** 在 `site-guide.md` 写入已核实的说明，例如 Bug 工单必须填写复现步骤。
3. **Run the next task.** 同一个 Web Agent 把说明加入上下文，完成另一张工单。

这一页先演示知识文件。上半页用两张网页示意图展示主动切换工单类型后出现必填条件，并明确用新开发输入和其他类型验证；中间画知识文件中的条件规则，右侧用图标和连线表示新任务、当前网页与保存的说明共同进入同一个 Web Agent。下半页并排画有无说明的执行路径，用虚线框标出可能避免的返工，不展示虚构性能数值。可逐步高亮三个环节，默认展示完整图；完整实验协议留第 6 页。可调用技能和网站操作图是同方向的其他产物，在文献分类页说明。

**图示与讲述：** 使用[英文 HTML 示意页](../../slides/part3-preview/output/environment-exploration-example.html)和[预览图](../../slides/part3-preview/output/environment-exploration-example.png)。图上直接展示网站、文件内容、加载入口和后续执行。示例规则是虚构的；实际探索产物必须由交互证据形成，不能把人工写好的规则当成自动学习结果。

**制作依据：** [SkillWeaver](#ref-skillweaver)、[WALT](#ref-walt)、[Grounding Agent Memory](#ref-grounding)及[实验设计支持稿](2026-10-01-part3-experiment-design-zh.md)。这是拟议机制示意，不是本项目实验成绩。

## 第 5 页 环境探索的相关研究与候选问题

**上屏内容：**

| 学到的产物 | 代表与做法 | 这一类需要解决什么 |
|---|---|---|
| 网站或工具说明、使用条件 | DRAFT：试调用，按返回修订说明（工具场景参照） | 有限观察怎样成为适用范围明确的规则 |
| 页面、状态与操作路径 | ActionEngine：探索网页建图，再按图执行（Web） | 怎样识别当前状态，判断旧路径还能否使用 |
| 可以直接调用的操作函数 | WALT：探索功能，写成工具并测试（Web） | 怎样验证函数做对了，并收回构建与维护投入 |

共同困难：在有限预算内探索有用内容，验证发现的适用范围，并让后续节省抵销学习投入。

**图示与讲述：** 延续上一页的知识文件，旁边补出网站操作图和可调用函数，分别对应三行。每类挑一篇解释，不把任意三篇当作全部相关研究。同类补充和逐篇映射放附录：说明类补充 Grounding Agent Memory；结构类补充 MobileGPT（移动端）；操作类补充 SkillWeaver。DRAFT 的工具调用结果不能替代 Web 任务效果，页面保留领域标注。

**制作依据：** [DRAFT](#ref-draft)、[ActionEngine](#ref-actionengine)、[WALT](#ref-walt)，以及[文献分类稿](2026-10-01-part3-literature-map-zh.md)中的选择依据、交叉支持和114条映射。该映射整理既有比较稿，不宣称重新全文审核了整个文献库。“共同困难”是对相关研究的综合，也约束我们的实验；不等于已经确认的研究空白。首轮先测文字说明，后续再比较具体探索策略。

## 第 6 页 实验一 有网站说明以后会不会更好

**上屏内容：**

同一个 Web Agent，比较两个版本：

| 原系统 | 探索后系统 |
|---|---|
| 网站说明为空 | 在开发阶段探索，生成 `site-guide.md` |
| 保留原模型、提示和代码 | 只新增这份说明，其余相同 |

验证后冻结说明，两组执行同一批未参与探索的新工单。

比较做对的比例、端到端耗时和累计费用；探索、整理、验证和读取说明的开销全部计入。同一总费用上限下，原系统可把余额用于执行。

**图示与讲述：** 两条水平支路共用右侧测试任务与评分框。上支路多出“探索网站、写说明、验证后冻结”，下支路使用空说明。强调的是文件这一处差异，不能只画抽象的学习模块。完整英文文案和流程见[实验 A](2026-10-01-part3-experiment-design-zh.md)。

**制作依据：** 首轮只验证路线在该场景是否有用，不主张新颖性。开发、验证、测试任务分开；两组均不能读取隐藏测试评分再决定重试。若有效，下一步加入已有探索方法，在相同知识形式和预算下比较新的探索策略。

## 第 7 页 方向二 执行轨迹怎样变成一次修改

**上屏内容：**

轨迹记录：网页观察、Agent 的动作、工具返回、结果及开销。

例子：先填字段，再改工单类型，提交时报缺少复现步骤，返回补填后再次提交。

修改器从多条轨迹发现重复返工，提出修改 `policy-prompt.md`：

- 修改前：填写给定字段并提交。
- 候选修改：先选择类型，观察更新后的表单，再填写必填字段并提交。

在独立验证用例上重跑，有帮助才保留；下一次加载新的提示词。模型权重不变。

**图示与讲述：** 左边画一段有返工的短轨迹，中间用 before/after 展示提示词的实际变化，右边画验证后保留或撤回。此处是完整方向中的一个容易检查的首轮实现；后续还可分别研究记忆、技能代码或控制程序的修改。候选提示必须由轨迹修改器产生，图中文字只作示意。

**制作依据：** [HarnessFix](#ref-harnessfix)、[Growing Harness](#ref-growing)和[实验 B](2026-10-01-part3-experiment-design-zh.md)。诊断原因是待验证判断；不能用模型写出一段解释代替修改前后的实际比较。

## 第 8 页 轨迹学习的相关研究与候选问题

**上屏内容：**

| 修改的对象 | 代表与做法 | 这一类需要解决什么 |
|---|---|---|
| 提示词与策略说明 | GEPA：读轨迹反馈，生成并筛选候选提示 | 修改在新任务上是否仍有效，筛选候选花多少成本 |
| 可检索的经验与工作流 | AWM：从轨迹归纳文字工作流，后续加载使用 | 检索到的经验是否有用，会不会传播错误或增加阅读负担 |
| 可执行技能代码 | ASI：从成功轨迹写 Python 技能，重跑验证 | 从旧轨迹抽出的函数能否正确处理新输入 |
| 执行框架与控制代码 | HarnessFix：诊断失败，局部修补并做回归检查 | 能否定位真正原因，修改后会不会损坏已有能力 |

共同困难：把轨迹中的问题变成具体修改，验证新版本在新任务上有效，并计入修改与验证投入。成功但浪费的执行也要分析。

**图示与讲述：** 用“修改对象、代表、共同难点”三列，四行覆盖四类工程对象。同类补充 ACE、ReasoningBank、SpeedRunner 和 Growing Harness 放附录。正文代表优先让听众看懂产物和修改过程，并保留任务领域、正式发表或预印本边界。首轮高亮提示词这一行，说明第 9 页实验从这里开始；不把整个方向缩成改提示。

**制作依据：** [GEPA](#ref-gepa)、[AWM](#ref-awm)、[ASI](#ref-asi)、[HarnessFix](#ref-harnessfix)，分类及证据边界见[文献分类稿](2026-10-01-part3-literature-map-zh.md)。GEPA 不作为完整 Web 效率证明；AWM、ASI 的步骤下降也不等于实际耗时或全投入下降。已有方法是实验起点，自动循环本身不是新贡献。

## 第 9 页 实验二 从轨迹改提示会不会更好

**上屏内容：**

先让原始 Agent 完成开发任务，保存成功、失败与返工轨迹，再比较：

| 原系统 | 轨迹学习后系统 |
|---|---|
| 继续使用原提示词 | 根据轨迹提出一份候选提示 |
| 不改提示 | 验证通过后换入新提示，未通过则保留原版 |

冻结后，两组执行同一批新工单。网站说明、浏览器工具、控制程序及模型权重相同。

测任务正确性、返工次数、耗时与累计费用，并计入轨迹采集、修改和验证投入。

**图示与讲述：** 左侧由共同的初始 Agent 产生开发轨迹，只有学习支路读取轨迹并改提示；基线保留原提示，不加载历史轨迹。中间显示提示词差异，右侧接同一组测试任务和外部评分器。与第 6 页保持同一种比较图，换成明确高亮的 `policy-prompt.md`。完整英文文案和流程见[实验 B](2026-10-01-part3-experiment-design-zh.md)。

**制作依据：** 首轮不加入额外环境探索，也不同时修改代码。等总费用上限，原系统可用于更多合理执行或重试，触发依据仅限正常可见反馈。有效后再加入简单经验总结或已有轨迹修改器，验证新增机制是否优于已有办法。

## 第 10 页 怎样确认做对了 怎样量时间和费用

**上屏内容：**

| 要测什么 | 怎样测 |
|---|---|
| 是否完成任务 | 外部评分器核对保存的工单及字段，检查重复记录或误修改 |
| 用户等了多久 | 从接收任务到完成或失败，记录实际经过的时间，包含重试 |
| 总共花了多少钱 | 累加执行、探索或改进、必要验证和维护费用 |

标准答案和测试评分器不交给学习模块。开发用于学习，验证用于挑选版本，最终测试只用于报告结果。

成功率和开销同时报告，避免把少做成任务误认为更省。

**图示与讲述：** 左边是两组 Agent 的执行，右边是系统外的检查器、计时器和费用账。外部评分器的判断不回流最终测试中的 Agent。研究专用重复测评费用另列预算；真正部署需要的准入验证必须计入学习投入。首轮冻结学习产物，持续学习评测另放扩展实验。

**制作依据：** [AppWorld](#ref-appworld)、[AI Agents That Matter](#ref-agents-matter)、[预算对照研究](#ref-budget-study)及[完整实验约定](2026-10-01-part3-experiment-design-zh.md)。独立性、重复运行、质量阈值和数据划分细节放附录。

## 第 11 页 首轮结果怎样决定下一步

**上屏内容：**

| 首轮结果 | 接下来做什么 |
|---|---|
| 文件没有学对或没有被使用 | 检查交互证据、提示和文件加载方式 |
| 后续运行有改善，但投入收不回 | 检查学习次数、读取负担和预计复用量 |
| 在新输入上稳定改善且值得投入 | 与已有方法比较，再研究具体的新机制 |

两个方向各自推进，可以只继续其中一个。

新流程、网站变化与跨站迁移属于扩展实验。只有明确需要二者配合时才研究组合，组合不作为必达目标。

**图示与讲述：** 两列并排列出环境探索与轨迹学习各自的“首轮证据、继续研究的问题”，不画强制汇合的流程。若本页与实验页重复，正式制作时可压缩并入资源页，不为了页数增加阶段。

**制作依据：** 本项目阶段安排。首轮可行性实验不替代与已有方法的研究比较；相关候选问题见[文献分类稿](2026-10-01-part3-literature-map-zh.md)。

## 第 12 页 资源与第一阶段交付物

**上屏内容：**

| 资源 | 用途 | 估算依据 |
|---|---|---|
| 模型调用费用 | 业务执行、环境探索、轨迹分析、候选修改与验证 | 各阶段次数及试点实测单次费用 |
| 环境与算力 | 可重置实例、并发运行、日志与结果存储 | 并发规模、占用时长及存储需求 |
| 研究测评费用 | 对照实验、重复运行和变化测试 | 比较组、任务规模与重复次数 |

首批资源支持瓶颈测量和两个最小实验，交付可复现环境、独立评分与结果比较。金额和规模由小规模试点估算，再安排后续投入。

**图示与讲述：** 资源表下方连接第一阶段交付物，说明每笔投入用于回答什么问题。正式资源页根据试点填入费用范围和环境并发数量；当前不编金额或 GPU 型号。人工确认规则与抽查评分属于实施依赖，本页按既定要求只列钱与算力。

**制作依据：** 本项目资源规划。预算区分业务执行、学习维护和研究测评，避免同一验证调用在多个栏目重复计费。即使暂时没有实测金额，仍可先制作页面结构；具体数字属于后续可替换内容。

## 附录安排

- **相关工作与完整条件。** 按类别列出已有研究的机制、任务、模型、验证方式及费用范围；代表选择依据和逐篇映射见[文献分类稿](2026-10-01-part3-literature-map-zh.md)，按版面续页。
- **实验与评分协议。** 用例划分、允许反馈、持续学习顺序、状态变化类型、质量阈值及重复运行安排。
- **时间与费用口径。** 用户等待、离线适配工期、资源占用分别统计；展示累计开销与回本的计算方式，不拼接不同论文的最佳数字。
- **候选研究问题。** 探索选择与停止、知识怎样表示、修改优先级、环境变化后的复查，均标为候选；小编辑模型训练为后续可选分支。
- **延展阅读。** 第一、二部分的通用加速背景与方法全景，以及本次详细文献比较。正文无需先读这些材料。

## 制作约定

正式交付采用可离线浏览的 HTML Slides，页面全部为英文，采用上表的英文标题；正文和全部图中文字译成自然英文后再排版。已有 PPTX 仅为早期原型，不再生成新的 PowerPoint 交付。正文以实际文件、提示修改和对照流程图为主。两页相关研究先按工程产物分类，每类选代表，多篇比较与完整映射放附录。每页只把“上屏内容”的英文版及必要图中文字排入版面，其他段落用于制作时核对。引用使用作者年份，完整条目放末尾；文献的关键测量条件在相应页面保留。图示中的工作流属于拟议设计，实验页展示比较方法和要测的量，不生成模拟实验成绩，也不以空结果图充当内容。

本版以既有文献审查为依据重新组织内容，没有新增实验结果或重新审计全部论文。主要内容依据为[最新分析](2026-10-01-agent-acceleration-related-work-analysis-zh.md)、[逐篇比较](2026-10-01-agent-acceleration-paper-comparisons-zh.md)和[两方向文献稿](2026-10-01-two-directions-literature-zh.md)。文献类别篇数和交集统计不占正文页面。

## 参考文献

以下条目沿用现有文献稿的书目信息，正式发表与实际阅读版本分别注明。正文和附录规划中的进一步选读可从上述逐篇比较进入。

<a id="ref-skillweaver"></a>

- **Boyuan Zheng et al., 2025** — Boyuan Zheng; Michael Y. Fatemi; Xiaolong Jin; et al. 2025. SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills. arXiv 预印本. [正式引用链接](https://arxiv.org/abs/2504.07079v1). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2504.07079v1)（v1，版本日期：2025-04-09；初版日期：2025-04-09）. 来源等级：合格机构补充。

<a id="ref-walt"></a>

- **Viraj Prabhu et al., 2026** — Viraj Prabhu; Yutong Dai; Matthew Fernandez; et al. 2026. WALT: Web Agents that Learn Tools. International Conference on Learning Representations 2026 (ICLR 2026), Conference track (proceedings pp. 55589-55607); OpenReview venue field: "ICLR 2026 Poster". [正式引用链接](https://proceedings.iclr.cc/paper_files/paper/2026/hash/5b175f9e93873e3a10a6ce43dbb82e05-Abstract-Conference.html). 实际读的版本：[版本链接（PDF）](https://arxiv.org/pdf/2510.01524v1)（v1，版本日期：2025-10-01；初版日期：2025-10-01 (Wed, 1 Oct 2025 23:41:47 UTC)）. 来源等级：顶级会议／期刊。 校准补读：[ICLR 2026 正式版 PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/5b175f9e93873e3a10a6ce43dbb82e05-Paper-Conference.pdf)（正式版；正文未印发布日期；PDF 元数据创建日期：2026-02-23；获取日期：2026-09-29）。

<a id="ref-grounding"></a>

- **Susheel Suresh et al., 2026** — Susheel Suresh; Hazel Mak; Sahil Bhatnagar; et al. 2026. Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents. arXiv 预印本. [正式引用链接](https://arxiv.org/abs/2609.11060). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2609.11060v1)（v1，版本日期：2026-09-10；初版日期：2026-09-10）. 来源等级：合格机构补充。

<a id="ref-harnessfix"></a>

- **Mengzhuo Chen et al., 2026** — Mengzhuo Chen; Junjie Wang; Zhe Liu; et al. 2026. From Failed Trajectories to Reliable LLM Agents: Diagnosing and Repairing Harness Flaws. arXiv 预印本. [正式引用链接](https://arxiv.org/abs/2606.06324v2). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2606.06324v2)（v2，版本日期：2026-07-02；初版日期：2026-06-04）. 来源等级：合格机构补充。

<a id="ref-growing"></a>

- **Laizhen Li et al., 2026** — Laizhen Li; Jiarui Li; Juanjuan Zhao; et al. 2026. Grow the Harness, Not the Context: From Strategy-Free Scaffolds to Reusable Specialist Agents. arXiv 预印本. [正式引用链接](https://arxiv.org/abs/2609.26760v2). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2609.26760v2)（v2，版本日期：2026-09-24；初版日期：2026-09-22）. 来源等级：合格机构补充。

<a id="ref-speedrunner"></a>

- **Zixi Huang et al., 2026** — Zixi Huang; Xiheng Wang; Andrew Wang; et al. 2026. Better, Faster, Stronger: Programmatic Skill Learning Best Reduces Agent Cost. arXiv 预印本. [正式引用链接](https://arxiv.org/abs/2608.11338v1). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2608.11338v1)（v1，版本日期：2026-08-11；初版日期：2026-08-11）. 来源等级：合格机构补充。

<a id="ref-clawtrace"></a>

- **Boqin Yuan et al., 2026** — Boqin Yuan; Yue Su; Renchu Song; et al. 2026. ClawTrace: Cost-Aware Tracing for LLM Agent Skill Distillation. Agent Skills '26 Workshop at ACM CAIS 2026 (ACM Conference on AI and Agentic Systems), San Jose, May 26, 2026; OpenReview venue 'AgentSkills 2026 Oral'; workshop is non-archival. [正式引用链接](https://arxiv.org/abs/2604.23853). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2604.23853v2)（v2，版本日期：2026-05-25；初版日期：2026-04-26）. 来源等级：合格机构补充。

<a id="ref-appworld"></a>

- **Harsh Trivedi et al., 2024** — Harsh Trivedi; Tushar Khot; Mareike Hartmann; et al. 2024. AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents. ACL 2024: Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), main conference, pages 16022-16076, Bangkok, Thailand, August 2024; Anthology ID 2024.acl-long.850; DOI 10.18653/v1/2024.acl-long.850. [正式引用链接](https://aclanthology.org/2024.acl-long.850/). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2407.18901v1)（v1，版本日期：2024-07-26；初版日期：2024-07-26）. 来源等级：顶级会议／期刊。

<a id="ref-agents-matter"></a>

- **Kapoor, Sayash et al., 2025** — Kapoor, Sayash; Stroebl, Benedikt; Siegel, Zachary S.; et al. 2025. AI Agents That Matter. Transactions on Machine Learning Research. 正式引用链接：未记录. 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2407.01502v1)（v1，版本日期：2024-07-01；初版日期：2024-07-01）. 来源等级：顶级会议／期刊。

<a id="ref-budget-study"></a>

- **Sina Hajimiri et al., 2026** — Sina Hajimiri; Masih Aminbeidokhti; Jose Dolz; et al. 2026. Are Online Skill and Memory Modules Always Worth Their Tokens? A Budget-Constrained Study of Web Agents. EMNLP 2026 (The 2026 Conference on Empirical Methods in Natural Language Processing), main conference, paper ID 4950-MAIN, poster (Session 4, Poster Session B, 2026-10-25). [正式引用链接](https://arxiv.org/abs/2606.15017). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2606.15017v2)（v2，版本日期：2026-08-30；初版日期：2026-06-12）. 来源等级：顶级会议／期刊。

<a id="ref-draft"></a>

- **Changle Qu et al., 2025** — Changle Qu; Sunhao Dai; Xiaochi Wei; et al. 2025. From Exploration to Mastery: Enabling LLMs to Master Tools via Self-Driven Interactions. ICLR 2025 (International Conference on Learning Representations 2025), main conference (proceedings 'Conference' track); decision Accept (Oral), Oral Session 4B, also Poster Session 3. [正式引用链接](https://proceedings.iclr.cc/paper_files/paper/2025/hash/8c22e5e918198702765ecff4b20d0a90-Abstract-Conference.html). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2410.08197v2)（v2，版本日期：2025-02-26；初版日期：2024-10-10）. 来源等级：顶级会议／期刊。

<a id="ref-actionengine"></a>

- **Hongbin Zhong et al., 2026** — Hongbin Zhong; Fazle Faisal; Luis França; et al. 2026. ActionEngine: From Reactive to Programmatic Web Agents via State Machine Memory. arXiv 预印本. [正式引用链接](https://arxiv.org/abs/2602.20502). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2602.20502v2)（v2，版本日期：2026-09-28；初版日期：2026-02-24）. 来源等级：合格机构补充。

<a id="ref-gepa"></a>

- **Lakshya A Agrawal et al., 2026** — Lakshya A Agrawal; Shangyin Tan; Dilara Soylu; et al. 2026. GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning. ICLR 2026, main conference; decision 'Accept (Oral)' (ICLR.cc/2026/Conference). [正式引用链接](https://proceedings.iclr.cc/paper_files/paper/2026/hash/0e9e708b6f48e14fd0ac29e167413f76-Abstract-Conference.html). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2507.19457v2)（v2，版本日期：2026-02-14；初版日期：2025-07-25）. 来源等级：顶级会议／期刊。

<a id="ref-awm"></a>

- **Zora Zhiruo Wang et al., 2025a** — Zora Zhiruo Wang; Jiayuan Mao; Daniel Fried; et al. 2025. Agent Workflow Memory. Proceedings of the 42nd International Conference on Machine Learning (ICML 2025), PMLR 267:63897-63911, 2025 (the PMLR page names no track; conference proceedings volume). [正式引用链接](https://proceedings.mlr.press/v267/wang25bx.html). 实际读的版本：[版本链接（HTML）](https://arxiv.org/html/2409.07429v1)（v1，版本日期：2024-09-11；初版日期：2024-09-11）. 来源等级：顶级会议／期刊。 校准补读：[ICML 2025／PMLR 267 正式版 PDF](https://raw.githubusercontent.com/mlresearch/v267/main/assets/wang25bx/wang25bx.pdf)（正式版；PMLR 页面记录的发表日期：2025-10-06；获取日期：2026-09-29）。

<a id="ref-asi"></a>

- **Zora Zhiruo Wang et al., 2025b** — Zora Zhiruo Wang; Apurva Gandhi; Graham Neubig; et al. 2025. Inducing Programmatic Skills for Agentic Tasks. COLM 2025 (Conference on Language Modeling), accepted paper, main conference (listed on the official "COLM 2025: Accepted Papers" page without a Spotlight badge). [正式引用链接](https://openreview.net/forum?id=lsAY6fWsog). 实际读的版本：[版本链接（PDF）](https://arxiv.org/pdf/2504.06821v2)；[版本链接（HTML）](https://arxiv.org/html/2504.06821v2)（v2，版本日期：2025-08-29；初版日期：2025-04-09）. 来源等级：顶级会议／期刊。 证据定位于 PDF；另读同版 HTML，但其缺少附录 A.2 提示。
