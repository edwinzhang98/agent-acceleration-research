# Web Agent 独立实验演示大纲 第二版

2026 年 10 月 1 日 · 英文 HTML Slides：开场 6 页及附录 A1、A2 已制作，后续内容仍为拟议大纲

这份演示讲清楚我们准备怎样研究 Agent 的环境探索与自我改进。面向有机器学习背景的听众，按独立演示组织；正式标题、页眉和页脚均不写“Part 3”，也不要求先读其他部分。本稿保留两个完整方向：**主动探索环境，形成后续任务能用的知识与操作；从执行轨迹中学习，修改 Agent 自己的做法。** 两个方向分别实验，各自回答能否改善后续任务；组合不是必做内容。首轮研究同一网站、同一种流程的新输入，明确固定模型权重。

**当前结构为 6 页已制作开场，加上暂列第 7–14 页的后续内容；页数不是硬限制。** 先把问题、定义、研究问题和实验范围讲清，再用具体图例解释机制。已有好图保留在有助理解的位置，避免图例代替研究内容，也避免不同页面重复同一说明。后续页面可按内容需要拆分或合并。

**正式交付为英文 HTML Slides，包括标题、正文、图示文字、图例和附录，支持离线浏览。** 本稿的中文仅用于审阅内容，不能直接搬上正式页面。每页“上屏内容”是待译成英文的拟议正文，“图示与讲述”说明怎样把内容讲具体，“制作依据”保存来源和必要边界。公式只用于精确定义研究目标或计量方法，每个符号就地解释，不为装饰增加公式。

首轮明确使用 Web Agent。浏览器工具是它操作网站的接口，不另开一条通用工具使用任务线。具体网站尚未选定；以下用创建支持工单作说明，报销仍可作为另一种应用选择。示例中的网页规则是虚构的，不代表已选定基准。

开场 6 页及两个可跳转附录见[连续英文 HTML Slides](../../slides/part3-preview/output/web-agent-experiments.html)。主文先按类别概括相关研究，再用代表论文支持；逐篇条件、详表与完整书目放附录。附录保留返回进入页的操作，参考既有演示的跳转方式，但不把既有演示作为阅读前提。

## 全篇结构

| 页码 | 英文页面标题 | 听众应当理解什么 | 制作状态 |
|---|---|---|---|
| 1 | Research problem and objective | 为什么需要跨任务学习，质量约束下怎样分别衡量时间和费用 | 已制作 |
| 2 | Task, environment and learning | 任务、环境、执行轨迹和学习的工作定义 | 已制作 |
| 3 | Two independent research questions | 两个研究问题、拟议假设与首轮单变量对照 | 已制作 |
| 4 | What changes between tasks—and what stays fixed? | 首轮任务范围、控制条件和数据划分 | 已制作 |
| 5 | What changes when model weights stay fixed? | 更新哪些模型外部对象，下一次通过什么接口使用 | 已制作 |
| 6 | Environment exploration | 主动交互、验证、保存知识和后续复用的具体机制 | 已制作 |
| 7 | Environment Exploration: What Is Learned? | 按学习产物分类，每类如何做，有什么共同困难 | 拟议，未制作 |
| 8 | Evaluating Environment Exploration | 探索在什么条件下有用，怎样与已有方法比较 | 拟议，未制作 |
| 9 | Improving the Agent from Execution Trajectories | 怎样从失败和低效执行中提出、验证并保留修改 | 拟议，未制作 |
| 10 | Trajectory-Based Improvement: What Changes? | 按修改对象分类，每类如何做，有什么共同困难 | 拟议，未制作 |
| 11 | Evaluating Improvements Learned from Trajectories | 自动修改是否改善后续任务，新增方法有何贡献 | 拟议，未制作 |
| 12 | Checking Success and Measuring Time and Cost | 怎样确认做对了，怎样测耗时和费用 | 拟议，未制作 |
| 13 | First Experiments and Next Steps | 首轮能回答什么，何时进一步比较已有方法 | 拟议，未制作 |
| 14 | Resources and Initial Deliverables | 钱和算力用在哪里，先支持哪一阶段 | 拟议，未制作 |
| A1 | Measurement protocol | 成功、实际耗时、学习投入与费用的操作定义及对照口径 | 已制作，可跳转并返回 |
| A2 | Engineering objects | 各更新对象的内容、加载入口、验证方式及首轮范围 | 已制作，可跳转并返回 |

## 第 1 页 研究问题与目标

**英文标题：** Research problem and objective

**制作状态：** 已制作。

**上屏内容：**

研究问题：过去的交互经验，能否帮助 Web Agent 在保持任务正确性的前提下，降低后续任务的耗时与费用？

- 重复任务可能反复发现环境信息、做相似决策或处理同类错误；这些工作中哪些能避免，需要实验确认。
- 学习本身也花时间和钱：获取、检查、保存与读取知识的开销可能超过后续节省。
- 先满足预先确定的任务质量要求，再分别报告时间与累计费用，不临时把二者加权成一个分数。
- 对照同一批留出输入上的原系统；失败和重试也进入统计，少做成任务不能算效率收益。

**图示与讲述：** 正文先解释问题、意义与评估单位。目标区分别定义成功率、包含失败与重试的实际任务耗时，以及学习/验证投入加后续执行的累计费用。质量要求相对基线预先设定，费用公式只表达累计口径。两个独立研究方向在第 3 页展开。

**制作依据：** [问题定义](2026-09-30-agent-acceleration-problem-framing-zh.md)、[最新相关工作分析](2026-10-01-agent-acceleration-related-work-analysis-zh.md)与[已制作页面源](../../slides/part3-preview/deck/slide01.html)。通过页内链接进入[附录 A1：Measurement protocol](../../slides/part3-preview/output/web-agent-experiments.html#a01)，查看测量与比较口径后返回本页。这里陈述研究目标，没有本项目实验收益。

## 第 2 页 任务、环境与学习的工作定义

**英文标题：** Task, environment and learning

**制作状态：** 已制作。

**上屏内容：**

| 概念 | 本研究中的含义 |
|---|---|
| Web task | 目标、输入数据和初始状态，加上一个外部的任务完成检查 |
| Environment | 网站界面、规则及允许的动作；同一个网站不意味着运行时页面和记录状态不变 |
| Execution trajectory | 一次运行中按顺序记录的观察、动作、工具反馈，以及关联的结果、实际耗时和费用 |
| Learning | 产生可在后续任务复用的持久更新；本研究首轮固定模型权重，更新知识、提示或程序等外部对象 |

小实例：创建一张 Bug 工单；输入为上传失败的描述与复现步骤；从重置并登录的网站状态开始；外部检查保存字段是否符合请求，以及是否存在重复记录或无关改动。

**图示与讲述：** 左侧给紧凑定义，右侧用一个小任务实例把各概念对应到具体内容。短执行链仅帮助解释“轨迹”是发生过的观察、操作和反馈，不代替完整方法流程。底部点明跨任务保留更新才属于这里讨论的学习，并区分可见网页反馈与隐藏测试评分。数据划分和完整控制设置留第 4 页。

**制作依据：** [已制作页面源](../../slides/part3-preview/deck/slide02.html)与[实验设计支持稿](2026-10-01-part3-experiment-design-zh.md)。轨迹关联的外部结果日志不表示测试中的 Agent 可以读取隐藏评分；运行时仍只获得允许的网页和工具反馈。这是本研究的工作定义，不宣称覆盖所有 Agent 学习研究。

## 第 3 页 两个独立研究问题

**英文标题：** Two independent research questions

**制作状态：** 已制作。

**上屏内容：**

| | A：环境探索 | B：从执行轨迹学习 |
|---|---|---|
| 研究问题 | 在有限探索预算内，怎样选择并核验能用于后续任务的网站知识？ | 怎样从轨迹发现并验证可以消除可避免工作、同时控制性能退步的修改？ |
| 拟议假设 | 经检查的知识可能减少重复发现和错误恢复，足以抵销获取与读取投入 | 根据轨迹修订的执行指令可能在保持质量要求的同时，减少新任务中的可避免工作 |
| 首轮唯一更新对象 | `site-guide.md`，作为上下文加载 | `policy-prompt.md`，作为执行指令加载 |
| 首轮比较 | 空说明与学习后的说明 | 原提示与根据轨迹修订的提示 |
| 保持固定 | 模型、执行策略、工具与控制循环 | 模型、网站知识、工具与控制循环 |

两个实验独立：分别从开发交互或开发轨迹产生候选，经验证后冻结，再测试未参与学习的新输入。任务质量、实际耗时与累计费用分别报告，包含学习与验证投入。

**图示与讲述：** 采用两个并列研究分支，每个先讲研究问题与假设，再显示首轮可解释的单变量对照。图中不画强制汇合。知识文件与提示文件只是首轮实现，两个完整方向仍可研究记忆、技能和控制代码等其他产物。首轮检验可行性；有效后还需与已有方法比较，才能讨论新增机制的贡献。

**制作依据：** [已制作页面源](../../slides/part3-preview/deck/slide03.html)与[实验设计支持稿](2026-10-01-part3-experiment-design-zh.md)。两条假设均未验证；首轮单变量控制不等于已经证明因果机制或新颖性。

## 第 4 页 不同任务之间 哪些改变、哪些固定

**英文标题：** What changes between tasks—and what stays fixed?

**制作状态：** 已制作。

**上屏内容：**

第一轮的不同任务，是同一网站、同一流程中的新请求和新输入。

| 实验组成 | 首轮设置 | 用途 |
|---|---|---|
| 任务输入 | 工单标题、描述和复现步骤不同，创建流程共用 | 检验跨请求复用，不只是重复播放已完成任务 |
| 环境 | 网站版本、布局、规则和权限相同，执行前恢复可比初态 | 分开学习更新的作用与环境或已有记录变化 |
| Agent 与执行 | 模型、浏览器工具和运行设置相同；A 只改说明，B 只改提示 | 使首轮比较可以解释 |
| 数据划分 | 开发产生候选，验证选择版本，最终测试使用冻结更新 | 避免按最终测试结果适配 |
| 对照 | 配对输入与初态，匹配执行限制，预先约定停止规则 | 两组都计入失败和重试，外部评分器保持独立 |

“登录失败”与“上传失败”是两张输入不同的 Bug 工单。网页运行状态会随操作改变，但网站规则和权限在首轮固定。新流程、网站改版和跨网站迁移分别扩展测试。

**图示与讲述：** 以设置表格为主，具体工单对只用于解释“新任务实例”。不再另加重复的任务示意图。匹配执行限制的效应比较，与允许原系统使用剩余学习预算的等总费用比较，在附录 A1 分开说明。

**制作依据：** [已制作设置页源](../../slides/part3-preview/deck/setting.html)与[附录 A1](../../slides/part3-preview/output/web-agent-experiments.html#a01)。具体网站未定；本页不承诺跨网站或任意任务泛化。

## 第 5 页 不训练模型时 实际更新什么

**英文标题：** What changes when model weights stay fixed?

**制作状态：** 已制作。

**上屏内容：**

| 更新对象 | 工程上的例子 | 下一次怎样使用 | 首轮范围 |
|---|---|---|---|
| 网站知识 | `site-guide.md` | 把相关说明加入模型上下文 | 实验 A |
| 执行提示词 | `policy-prompt.md` | 作为 Agent 的执行指令加载 | 实验 B |
| 可调用操作 | `create_ticket.py` | 注册成 Agent 可以调用的浏览器技能 | 后续可选研究 |
| 控制程序 | `runner.py` | 改变观察、执行、检查与重试的顺序 | 后续可选研究 |

模型权重保持不变。两个方向都可能产生上述修改，但第一轮各只改一个对象，便于解释结果。

**图示与讲述：** 采用已制作的加载接口图：知识文件作为上下文、提示文件作为指令，分别影响同一个冻结模型；模型选择浏览器动作，网页和工具返回观察。外围标出负责运行该循环的控制程序。A 与 B 是两个独立实验，连线不是要求一次同时加载两个新产物。技能与控制程序放在“后续可选”区。harness 解释为模型外围组织执行的程序，避免用统称替代具体对象。

**制作依据：** [已制作接口图源](../../slides/part3-preview/deck/implementation.html)与[文献分类及工程对象](2026-10-01-part3-literature-map-zh.md)。通过页内链接进入[附录 A2：Engineering objects](../../slides/part3-preview/output/web-agent-experiments.html#a02)，查看具体内容、验证和复用方式后返回。探索与轨迹学习按证据获取和使用方式区分，产物可以重叠。

## 第 6 页 方向一 探索网站后保存什么

**英文标题：** Environment exploration

**制作状态：** 已制作，保留已认可的环境探索图。

**上屏内容：**

1. **Explore and check.** 改变工单类型，观察网页反馈，再换开发输入验证。
2. **Save what was learned.** 在 `site-guide.md` 写入带适用范围的已核实说明，例如 Bug 工单必须填写复现步骤。
3. **Run the next task.** 同一个 Web Agent 把说明加入上下文，完成另一张工单。

这一页先演示知识文件。上半页用两张网页示意图展示主动切换工单类型后出现必填条件，并明确用新开发输入和其他类型验证；中间画知识文件中的条件规则，右侧表示新任务、当前网页与保存说明共同进入同一个 Web Agent。下半页并排画有无说明的示意执行路径，标出可能避免的返工，不展示虚构性能数值。

**图示与讲述：** 本页承接前文定义与研究问题，用已认可的图把机制讲具体；不重新代替前文讲研究意义。默认展示完整图，也可逐步高亮。完整实验协议留第 8 页和附录 A1。可调用技能和网站操作图属于同方向的其他产物，在第 7 页分类说明。连续演示中的第 6 页与[独立英文 HTML 示意页](../../slides/part3-preview/output/environment-exploration-example.html)、[预览图](../../slides/part3-preview/output/environment-exploration-example.png)对应。

**制作依据：** [SkillWeaver](#ref-skillweaver)、[WALT](#ref-walt)、[Grounding Agent Memory](#ref-grounding)及[实验设计支持稿](2026-10-01-part3-experiment-design-zh.md)。示例规则是虚构的；一次报错只能产生候选规则，需经开发交互验证，不能把人工写好的规则当成自动学习结果，也不能把示意路径当成本项目成绩。

## 第 7 页 环境探索的相关研究与候选问题

**制作状态：** 拟议内容，尚未制作。

**上屏内容：**

| 学到的产物 | 代表与做法 | 这一类需要解决什么 |
|---|---|---|
| 网站或工具说明、使用条件 | DRAFT：试调用，按返回修订说明（工具场景参照） | 有限观察怎样成为适用范围明确的规则 |
| 页面、状态与操作路径 | ActionEngine：探索网页建图，再按图执行（Web） | 怎样识别当前状态，判断旧路径还能否使用 |
| 可以直接调用的操作函数 | WALT：探索功能，写成工具并测试（Web） | 怎样验证函数做对了，并收回构建与维护投入 |

共同困难：在有限预算内探索有用内容，验证发现的适用范围，并让后续节省抵销学习投入。

**图示与讲述：** 延续上一页的知识文件，旁边补出网站操作图和可调用函数，分别对应三行。每类挑一篇解释，不把任意三篇当作全部相关研究。同类补充和逐篇映射放附录：说明类补充 Grounding Agent Memory；结构类补充 MobileGPT（移动端）；操作类补充 SkillWeaver。DRAFT 的工具调用结果不能替代 Web 任务效果，页面保留领域标注。

**制作依据：** [DRAFT](#ref-draft)、[ActionEngine](#ref-actionengine)、[WALT](#ref-walt)，以及[文献分类稿](2026-10-01-part3-literature-map-zh.md)中的选择依据、交叉支持和114条映射。该映射整理既有比较稿，不宣称重新全文审核了整个文献库。“共同困难”是对相关研究的综合，也约束我们的实验；不等于已经确认的研究空白。首轮先测文字说明，后续再比较具体探索策略。

## 第 8 页 实验一 有网站说明以后会不会更好

**制作状态：** 拟议内容，尚未制作。

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

## 第 9 页 方向二 执行轨迹怎样变成一次修改

**制作状态：** 拟议内容，尚未制作。

**上屏内容：**

轨迹记录：网页观察、Agent 的动作、工具返回、结果及开销。

例子：先填字段，再改工单类型，提交时报缺少复现步骤，返回补填后再次提交。

修改器从多条轨迹发现重复返工，提出修改 `policy-prompt.md`：

- 修改前：填写给定字段并提交。
- 候选修改：先选择类型，观察更新后的表单，再填写必填字段并提交。

在独立验证用例上重跑，有帮助才保留；下一次加载新的提示词。模型权重不变。

**图示与讲述：** 左边画一段有返工的短轨迹，中间用 before/after 展示提示词的实际变化，右边画验证后保留或撤回。此处是完整方向中的一个容易检查的首轮实现；后续还可分别研究记忆、技能代码或控制程序的修改。候选提示必须由轨迹修改器产生，图中文字只作示意。

**制作依据：** [HarnessFix](#ref-harnessfix)、[Growing Harness](#ref-growing)和[实验 B](2026-10-01-part3-experiment-design-zh.md)。诊断原因是待验证判断；不能用模型写出一段解释代替修改前后的实际比较。

## 第 10 页 轨迹学习的相关研究与候选问题

**制作状态：** 拟议内容，尚未制作。

**上屏内容：**

| 修改的对象 | 代表与做法 | 这一类需要解决什么 |
|---|---|---|
| 提示词与策略说明 | GEPA：读轨迹反馈，生成并筛选候选提示 | 修改在新任务上是否仍有效，筛选候选花多少成本 |
| 可检索的经验与工作流 | AWM：从轨迹归纳文字工作流，后续加载使用 | 检索到的经验是否有用，会不会传播错误或增加阅读负担 |
| 可执行技能代码 | ASI：从成功轨迹写 Python 技能，重跑验证 | 从旧轨迹抽出的函数能否正确处理新输入 |
| 执行框架与控制代码 | HarnessFix：诊断失败，局部修补并做回归检查 | 能否定位真正原因，修改后会不会损坏已有能力 |

共同困难：把轨迹中的问题变成具体修改，验证新版本在新任务上有效，并计入修改与验证投入。成功但浪费的执行也要分析。

**图示与讲述：** 用“修改对象、代表、共同难点”三列，四行覆盖四类工程对象。同类补充 ACE、ReasoningBank、SpeedRunner 和 Growing Harness 放附录。正文代表优先让听众看懂产物和修改过程，并保留任务领域、正式发表或预印本边界。首轮高亮提示词这一行，说明第 11 页实验从这里开始；不把整个方向缩成改提示。

**制作依据：** [GEPA](#ref-gepa)、[AWM](#ref-awm)、[ASI](#ref-asi)、[HarnessFix](#ref-harnessfix)，分类及证据边界见[文献分类稿](2026-10-01-part3-literature-map-zh.md)。GEPA 不作为完整 Web 效率证明；AWM、ASI 的步骤下降也不等于实际耗时或全投入下降。已有方法是实验起点，自动循环本身不是新贡献。

## 第 11 页 实验二 从轨迹改提示会不会更好

**制作状态：** 拟议内容，尚未制作。

**上屏内容：**

先让原始 Agent 完成开发任务，保存成功、失败与返工轨迹，再比较：

| 原系统 | 轨迹学习后系统 |
|---|---|
| 继续使用原提示词 | 根据轨迹提出一份候选提示 |
| 不改提示 | 验证通过后换入新提示，未通过则保留原版 |

冻结后，两组执行同一批新工单。网站说明、浏览器工具、控制程序及模型权重相同。

测任务正确性、返工次数、耗时与累计费用，并计入轨迹采集、修改和验证投入。

**图示与讲述：** 左侧由共同的初始 Agent 产生开发轨迹，只有学习支路读取轨迹并改提示；基线保留原提示，不加载历史轨迹。中间显示提示词差异，右侧接同一组测试任务和外部评分器。与第 8 页保持同一种比较图，换成明确高亮的 `policy-prompt.md`。完整英文文案和流程见[实验 B](2026-10-01-part3-experiment-design-zh.md)。

**制作依据：** 首轮不加入额外环境探索，也不同时修改代码。等总费用上限，原系统可用于更多合理执行或重试，触发依据仅限正常可见反馈。有效后再加入简单经验总结或已有轨迹修改器，验证新增机制是否优于已有办法。

## 第 12 页 怎样确认做对了 怎样量时间和费用

**制作状态：** 拟议内容，尚未制作。

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

## 第 13 页 首轮结果怎样决定下一步

**制作状态：** 拟议内容，尚未制作。

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

## 第 14 页 资源与第一阶段交付物

**制作状态：** 拟议内容，尚未制作。

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

正文保留理解结论必需的口径，详细表格通过可点击链接展开；每个附录页均提供返回进入页的操作。当前已制作：

- **[A1 Measurement protocol](../../slides/part3-preview/output/web-agent-experiments.html#a01)。** 成功率、实际任务耗时、学习投入、执行费用与累计费用的操作定义；区分匹配执行限制的比较与等总预算的比较；说明测试隔离、失败/重试、维护和研究测评费用。正文第 1 页提供入口，后续实验页可复用，避免多处重复完整协议。
- **[A2 Engineering objects](../../slides/part3-preview/output/web-agent-experiments.html#a02)。** 知识文件、提示文件、技能和控制程序分别保存什么，后续怎样使用，如何验证，以及哪些属于首轮。正文第 5 页提供入口。

后续按讲述需要扩展，不预设附录页数：

- **相关工作与完整条件。** 主文第 7、10 页先按类别总结，每类由代表论文支持；机制、任务、模型、验证与费用范围的逐篇详表放附录。代表选择依据和逐篇映射见[文献分类稿](2026-10-01-part3-literature-map-zh.md)。主文分类行可跳转到对应详表，再返回原页。
- **实验与评分协议。** 在 A1 基础上补充用例划分、允许反馈、持续学习顺序、状态变化类型、质量阈值及重复运行安排。
- **时间与费用口径。** 用户等待、离线适配工期、资源占用分别统计；按需要扩展累计开销与回本的计算，不拼接不同论文的最佳数字。
- **候选研究问题。** 探索选择与停止、知识表示、修改优先级、环境变化后的复查均标为候选；小编辑模型训练为后续可选分支。
- **延展阅读。** 通用加速背景、方法全景与本次详细文献比较，正文无需先读这些材料。

## 制作约定

正式交付采用可离线浏览的 HTML Slides，页面全部为英文，采用上表的英文标题；正文和全部图中文字译成自然英文后再排版。已有 PPTX 仅为早期原型，不再生成新的 PowerPoint 交付。正文先清楚交代问题、定义、假设和实验范围，图示用于具体解释机制、工程对象和比较关系。保留有用的图与内容，按讲述顺序逐步展开；不硬塞固定页数，也不以重复页面增加篇幅。相关研究主文先按类别总结，再由代表论文支持，多篇比较与完整映射放可跳转并返回的附录。每页只把“上屏内容”的英文版及必要图中文字排入版面，其他段落用于制作时核对。引用使用作者年份，完整条目放末尾；文献的关键测量条件在相应页面保留。 公式只在精确定义研究目标或计量方法时使用，符号当页说明；能用准确文字或表格表达的内容，不为装饰增加公式。图示中的工作流属于拟议设计，实验页展示比较方法和要测的量，不生成模拟实验成绩，也不以空结果图充当内容。

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
