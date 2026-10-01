# 第三部分：两张具体实验页的支持稿

2026-10-01 · 中文供审阅，英文用于正式 Slides · 拟议实验，尚未实施

首轮固定模型权重，使用 Web Agent。两个方向分别实验，不要求组合。本稿每个方向只设两个比较组、只允许一种产物更新，先回答“这条路线在选定场景能否带来收益”；已有方法比较和新算法贡献留给后续实验。

## 共同场景：同一网站，同一流程，输入不同

用可重置的沙箱工单网站作讲解例子，最终应用仍可替换。每个任务都是：**根据给定信息创建一张支持工单，并确认保存结果。** 输入包括标题、类别、说明和该类别所需信息。不同工单是不同任务实例，工作流程保持一致；这不是要求使用报销应用，也不在第一轮声称跨网站泛化。

- 示例交互规律：选 `Type = Bug` 后，`Steps to reproduce` 成为必填字段。这是虚构沙箱规则，和机制示意页保持一致。
- 示例任务：`Create a Bug ticket. Title: Cannot sign in. Description: The page returns an error. Steps to reproduce: Open Portal and click Sign in.`
- 输入提供完成任务所需信息；不把“信息缺失时如何追问”混入这轮实验。
- 以上页面行为是用于说明实验的假设，选定真实沙箱后必须核实。若自己构建环境，交互规律由环境实现，不能故意只放有利于学习组的机关。

同站不同操作、网站改版和规则变化分别作为后续扩展。第一轮测试是同一流程中的新输入，不把这一级别的结果写成新流程或新环境泛化。

**统一划分：** `Development → Validation → Locked test`。Development 承担通常所说的训练/开发集作用，但不训练模型权重：探索方向在其中交互并写知识；轨迹方向在其中收集记录并改提示。Validation 用于决定候选是否保留；Locked test 在产物和实验设置冻结后才运行。

## Slide A — Can Exploration Make Later Web Tasks Cheaper?

### 英文上屏短文

**Same website. Same workflow. New ticket inputs. Frozen model weights.**

| Input | What changes? | What stays fixed? |
|---|---|---|
| Development cases, browser observations, action outcomes | `site-guide.md`: verified facts about fields and operations | Model, policy prompt, browser tools, control loop |

**Example discovery**

`Type = Bug requires Steps to reproduce. Select Type before checking required fields.`

**Two groups**

- **Baseline:** execute with an empty site guide.
- **Explore + guide:** probe the website, write the guide, then execute.

**Develop → Validate → Freeze → Test new inputs**

**Measure:** task correctness, end-to-end latency, and cumulative cost including exploration and guide use.

**Budget & feedback:** same total cost cap; baseline may spend more on execution; no hidden test feedback.

### 页面图解方案

横向主流程，沿用网站小示意图；不放抽象模块墙。

```text
DEVELOPMENT                  VALIDATION                LOCKED TEST

Probe the website
  Type → Bug              ┌→ Keep or reject guide ─→ [Frozen guide] ─┐
  Observe new field       │                                        │
          ↓               │                                        ▼
 Write site-guide.md ─────┘                           Same Web Agent + new inputs
                                                               ↓
 Empty guide ──────────────────────────────────────→ Baseline execution
                                                               ↓
                                                    Correctness | Latency | Cost
```

正式排版用上下两条对齐的执行支路：上方有探索和知识产物，下方没有；右侧共享同一批测试任务和外部评分框。`site-guide.md` 卡片用强调色，其他模块保持同色，直接说明唯一变动处。知识文件旁给出上面的实际候选句子；不是画一个没有内容的“Memory”框。

### 中文讲述与实验约束

探索 Agent 在开发环境中尝试类别选择、字段填写和保存，依据可见反馈提出网站知识。它可以换开发输入核实发现，再将可重复观察到的规律写入 `site-guide.md`。正式执行者每次通过同一加载入口读取该文件；基线加载空文件。因此“固定提示”指任务指令与策略提示固定，**额外知识文本及其读取 token 是有意改变且要计费的部分**。

首轮不同时改技能代码、执行提示或 harness。机制页与实验页均使用 `site-guide.md` 表示网站知识文件。后续可把经验证的操作写成 `create_ticket.py` 并注册为浏览器工具，但不放进首轮两组比较。选择文字文件是为了容易看清“到底学到了什么、有没有被用上”，不是认定文字是最优表示。Validation 在开发结束后检查候选是否值得保留；进入测试前冻结文件，测试期间不继续写入新经验。基线在对应开发和验证阶段确定其固定执行设置，不获取隐藏测试信息。

这是探索方向的可行性实验：有用的结果是新输入上的正确性达标，且学习后的运行节省足以覆盖前期投入。它**不能单独证明我们的探索方式优于已有方法**。若有效，下一步保持相同执行者、知识格式与预算，再加入一个代表探索基线，比较一个具体新增机制，例如如何选择下一次探索；此时才讨论研究增量。

## Slide B — Can Trajectory Feedback Improve the Execution Policy?

### 英文上屏短文

**Same website. Same workflow. New ticket inputs. Frozen model weights.**

| Input | What changes? | What stays fixed? |
|---|---|---|
| Development traces: observations, actions, outcomes, cost | `policy-prompt.md`: instructions for future execution | Model, site knowledge, browser tools, control loop |

**Example edit**

Before: `Fill the supplied fields and save.`

After: `Select Type first. Inspect the updated form, fill required fields, then save.`

**Two groups**

- **Baseline:** keep the original policy prompt.
- **Trace → edit:** diagnose traces, propose one prompt revision, validate it.

**Collect traces → Edit → Validate → Freeze → Test new inputs**

**Measure:** task correctness, retries, end-to-end latency, and cumulative cost including editing and validation.

**Budget & feedback:** same total cost cap; baseline may spend more on execution; no hidden test feedback.

### 页面图解方案

左侧放一条短轨迹，中间放提示 diff，右侧放两组测试输出。听众应直接看到被替换的是执行策略提示。

```text
DEVELOPMENT                   VALIDATION                 LOCKED TEST

Original Agent runs
         ↓
Trace: fill → select Bug      Edited policy ─→ Keep/reject ─→ [Frozen prompt]
→ save → missing Steps             ↑                              │
→ fill Steps → save                │                              ▼
         ↓                         │                    Same Agent + new inputs
Diagnose repeated rework ─→ Edit policy-prompt.md                   │
                                                                  ▼
Original prompt ──────────────────────────────────────→ Baseline execution
                                                                  ↓
                                              Correctness | Retries | Latency | Cost
```

正式图把轨迹中的“返工”用一处强调色标出；提示卡用两行 before/after 展示具体改动。右侧测试支路与 Slide A 相同，让观众能比较两个实验，而不是重新理解一种画法。

### 中文讲述与实验约束

先让相同初始 Agent 执行开发任务，记录成功与失败轨迹及开销。修改器读取这些轨迹和允许的开发反馈，产生一个策略提示候选；首轮不搜索大量版本。上面的 edit 只是供讲解的假设候选，实验时应由修改器根据实际记录提出，不能把人工写好的答案当成自动学习结果。开发迭代可以继续，但次数必须预先限定并计费。

这轮仅更新 `policy-prompt.md`；知识文件为空或使用两组共同的固定初始内容，浏览器工具与控制代码不改，也不加入主动探索模块。候选在独立 Validation 用例上检查质量和开销；不过关就保留原提示。通过后冻结提示，在未用于提出或选择修改的新输入上测试。此轮不声称已经证明工具或 harness 自动修改有效；那些仍属于完整轨迹学习方向，后续可单独扩展可编辑对象。

这是轨迹学习的可行性实验。若通过，下一步再加入一个简单的“直接总结经验并追加提示”基线，或一个已有轨迹修改器，与一个明确的新机制比较。比较问题定位时固定提示编辑器与验收器，比较编辑策略时固定轨迹输入与评分；不要一次改动多个环节再把收益归给某个模块。

## 两页共享的预算与独立评测口径（讲述/附录）

1. **相同总体费用上限，允许实际花费不同。** 预先确定测试任务序列和总费用上限。学习组从中支付实际需要的探索或轨迹收集、整理/修改、准入验证，以及测试执行和知识读取；基线没有这些学习投入，可以把余额用于较充分的执行、检查或重试。总上限相同不表示强迫两组花完，也不保证每次执行的上限相同；分配办法在 Validation 阶段确定后冻结。
2. **原始任务执行与学习开销只计一次。** 若开发轨迹来自原本就会执行的业务任务，记在业务执行账；若专门为学习额外采样，记在学习账。结果应明确采用哪种场景。研究者为并列比较各组而额外运行的外部测试单列为研究费用，不混入实际部署费用；实际准入验证不能借此漏算。
3. **等预算重试不读取隐藏评分。** 重试只依据正常允许的网页报错、可见状态和超时等反馈，不能由隐藏答案或最终裁判告知“这题错了，再试一次”。基线增大执行预算也采用相同反馈规则。
4. **外部裁判与学习模块隔离。** 裁判检查已保存记录是否匹配任务、字段是否完整、是否产生额外记录或非预期修改。标准答案、隐藏状态检查与最终测试结果不回流学习模块。Validation 可给预先约定的汇总评分/开销以保留或拒绝候选；不能拿最终测试反复挑版本。
5. **先看质量，再解释节省。** 同时报成功率、端到端用户等待、累计费用；轨迹、调用数、token 和返工次数用于解释机制。少完成任务带来的低费用不能算加速。阶段试验先报告冻结成果后的新输入表现；持续更新、环境变化是独立扩展。
6. **图上不编实验成绩。** 两页右侧用带名字的测量输出框说明将得到什么；有实测后再替换为表格或曲线。提前写入质量要求、任务划分和预算分配规则，避免见到结果后改变成功标准。

本稿属于候选实验设计，没有新文献结论、没有实验数据，也不确定最终网站或算法。支撑方向与比较边界沿用[当前大纲](2026-10-01-part3-standalone-slides-outline-v2-zh.md)和[相关研究分析](2026-10-01-agent-acceleration-related-work-analysis-zh.md)。
