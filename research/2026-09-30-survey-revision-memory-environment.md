# 方法问题定义、更新公式与环境规则闭环补核

日期：2026-09-30。用途：为主报告第4–5节补充精确方法解释，并审查第8–9节的新颖性边界。本文不新增全局证据编号，不修改主报告、旧支持文件或筛查表。页码均为所列版本 PDF 页码；“原式”指论文直接给出的数学式，“本报告重述”指根据算法压缩表达的解释，不冒充论文公式。

本轮复核范围：Metis §§2–3/Algorithm 1；SpeedRunner §§2–3/Algorithm 1/Appendix I；MemRL §§3–4/Appendix G；AWM §§2–4/Appendix F；ReasoningBank §§3.1–3.3/Appendices D–E；MobileGPT §§3–5/§9；ActionEngine v2 §§3–4/Appendices A–B/失败分析；WALT 正式版 §§3.1–3.4/结论；WorldEvolver §§3.1–3.3/Algorithm 1/Appendices D–E；GLoW §§3.1–3.2/Appendix C。MemRL p5、WALT p5、WorldEvolver p5、GLoW p3 的公式另核 PDF 渲染页，避免文本层错读上下标。

## 1. 用户的两个方向应怎样区分

方向(a)是**用过去的执行经验改进以后怎样做任务**：例如记住一个更好步骤、生成一个程序技能，或者学会该选哪条记忆。

方向(b)是**通过交互弄清环境怎样运行，再利用反馈检验、修正这种认识，减少重复犯错**。这里环境知识可以是可用动作与前置条件、页面状态与转移、搜索参数含义、物品之间的依赖、执行后的状态变化，或执行某动作时哪些属性保持不变。它不一定叫 world model，也不一定是一段独立文字；规则可以进入代码的条件分支、输入 schema、状态图、预测器上下文和错误修复器。

两方向会重叠。Metis 的环境 facts/pitfalls、SpeedRunner 的观察检查与恢复代码、WALT 的网站参数及约束、ActionEngine 的状态机，都比“只是记忆成功轨迹”更接近(b)。因此不宜把(a)只归给 memory/skills、把(b)只归给带 world model 名称的论文。相反，GLoW 虽名为 world model，核心是探索状态的价值判断与动作策略反思，不是显式预测下一观察。

一个可核查的(b)闭环至少应说明：**观测到什么 → 形成什么环境假设或约束 → 它怎样改变下一次预测/行动 → 用什么实际反馈检验 → 矛盾时怎样更新**。仅把一条轨迹塞回 prompt，或仅保存成功代码，尚不足以证明该闭环。

| 方法 | 实际改进对象 | 与(b)的关系 | 不应外推的部分 |
|---|---|---|---|
| AWM | 参数化文字工作流 | 工作流含观察与动作上下文，可能携带环境经验 | 默认并非转移规则模型，也无逐条规则证伪机制 |
| ReasoningBank | 成败轨迹中的策略、教训 | 可记环境操作陷阱，以之后任务反馈继续补充 | 默认 consolidation 是追加，不等于对旧规则做证据维护 |
| MemRL | 记忆的检索效用数值 | 学“哪段经验有用”，反馈来自环境 reward | 不直接学习状态转移或给出失败原因 |
| Metis | 环境 facts、pitfalls、plans 与工具 | 有环境探查、规则纠正和失效替换；直接重叠 | plan 被选择的频率不是成功因果证据；编译通过不是语义证明 |
| SpeedRunner | 可编辑的观察驱动程序技能 | 从错误响应总结适用条件、检查、恢复；直接重叠 | 无独立环境预测模型；新技能不要求环境回放验收 |
| MobileGPT | 页面功能、子任务转移与可适配动作 | 学页面可执行条件，失配回退，吸收人工修正 | 初次错误修正并非全自主；匹配后仍有参数填充 LLM 调用 |
| ActionEngine | GUI 状态机、操作语义与程序 | 观察搜索/分页行为、状态约束与持久修复；直接重叠 | 主实验关闭 Patcher，未用主结果量化持续在线修复价值 |
| WALT | 网站功能工具、参数 schema、执行实现 | 探索参数语义并由测试反馈修正；直接重叠 | 运行时 fallback 不自动等于已验证的长期在线工具更新 |
| WorldEvolver | 下一观察预测的检索与规则上下文 | 显式预测—实际观察误差驱动更新；最直接的预测闭环 | 当前语义提取实现专注 preservation rules，不能说已学齐一般转移/因果规律 |
| GLoW | 探索状态价值/潜力及文本动作优势 | 学环境中的瓶颈和有效策略，重复试验促修正 | 不是显式下一状态预测器；优势/UCB是启发，不是参数化 RL 更新 |

## 2. 一个统一表达，但它是本报告的研究问题重述

记固定模型为 \(\pi_\theta\)，任务为 \(q_i\)，当前交互历史为 \(h_t\)，外部可变知识为 \(K_i\)。一般形式可写成：

\[
a_t\sim\pi_\theta(\cdot\mid q_i,h_t,K_i),\qquad
K_{i+1}=U(K_i,\tau_i,f_i),\qquad \theta\text{ 固定}.
\]

这只是跨论文共性的本报告重述；\(f_i\) 可是任务成功信号、环境错误、预测误差或人工修正，各篇并不相同。模型固定不等于系统没有学习：文字、程序、图结构和表格效用值仍会更新。尤其 MemRL 有数值学习，但并不更新语言模型权重。

若我们的目标确实是加速/降本，一个待检验目标可以是：在成功率不劣于规定基线的约束下，降低同一任务流的总成本，包含探索、构造、检索/管理、任务执行、验证、修复。此目标是**我们拟采用的评价与研究定义**，不能写成所有下述论文都在优化的原式。WALT 给了工具级成本代理目标；MemRL 优化的是预期 reward；GLoW 关注探索分数及样本效率；WorldEvolver 关注预测与规划效果。它们解决了加速可能需要的不同子问题。

## 3. Metis：什么经验保留为文字，什么经验值得编程

**问题定义。** 固定 ReAct 执行器连续接收任务；过去经历形成模型外记忆。问题不是单纯“多存一点记忆”，而是区分经验的表示形式及维护/复用方式：环境性质和常见错误通常作为文字建议，反复出现的可执行过程才转成工具。[R1] §§2.1–3.3，pp3–7。

**原式/原算法。** §2.2 写 \(M_k=\operatorname{Reflect}(M_{k-1},\tau^{(k)})\)。§3.1 写 \(M=(M_{text},M_{code})\)；§3.2 写：

\[
M_{text}=M_{env}\cup M_{pit}\cup M_{plan},\quad
m=(body,\kappa,v),\quad \kappa\in\{env,pit,plan\}.
\]

其中 \(v\) 是 invalidation bit；旧项被纠正/合并时 \(v:0\to1\)，另追加修订项，旧项不再检索。Pitfall 的内容包含 trigger、mistake、consequence。反思器可访问执行器相同环境和工具；失败时探查原因，成功时也寻找无效重试与多余探索。

Algorithm 1（p7）使用计划被选择的任务索引集合 \(B(p)\)：

\[
B(p)\leftarrow B(p)\cup\{i\}\quad(p\in S_i^{plan}),
\qquad |B(p)|\ge\theta\Longrightarrow\operatorname{Codify}.
\]

**任务不必成功。** 这是 recurrence evidence，论文明确不把它当作该计划导致成功的证据。Codifier 输入计划和相关 queries，**刻意不输入原始候选轨迹**；工具要求至少由两个结构不同的 query 支持，并把变量暴露为参数。依赖与编译通过后接纳；消耗的 buffer 折入有限历史后清空。

§3.5（p8）给出依赖闭包：

\[
U_0=S_i^{tool}\cup\bigcup_{m\in S_i^{text}}Ref(m),\quad
U_{r+1}=U_r\cup\bigcup_{t\in U_r}Dep(t).
\]

达到不动点得到 \(U_i^\star\)。接纳 guard 为 \(Compile(impl(t),Close(\varnothing,\{t\}))=1\)。编译失败允许一轮纠正，再失败拒绝。它不是显式最小化任务秒数或美元的优化式；复用阈值是程序化门槛。

**环境规则闭环。** 原文机制为“轨迹暴露失败/冗余 → reflector 再访问环境定位原因 → 形成 env/pit 条目 → 后续任务检索为建议 → 新证据显示旧结论不准时 invalidate-and-replace”。这已经涵盖用户想法(b)的主要环节。与强约束的区别：论文明确文字是 advice，执行器可以忽略，不能声称它硬性阻止了重复错误。

**主报告需改。** “plan 被不同结构 query 反复使用达到条件”应拆开写：先依据**选中频次**触发，再要求生成工具有至少两个结构不同 query 的支持；不能把二者揉成“反复验证成功后才固化”。也不宜重复论文“文字错误最多是被忽略建议”的绝对语气：我们应说文字能被执行器重新解释，但错误建议仍可能诱导错误（这是我们的判断）。

## 4. SpeedRunner：把历史日志中的环境反馈变成会检查、会分支的代码

**问题定义。** POMDP 中连续到达的在线任务，环境动作不要求可撤回或重做，任务结束后不能用修改后的策略重新跑该任务做验收。Rollout 为 \(\tau=(o_1,a_1,\ldots,o_T,a_T,R)\)。技能是有文档、可调用 primitive 或其他技能的可执行函数。Actor 与 coding-agent inducer 均不训练权重。[R2] §§2–3，pp2–4。

**原算法。** 论文显式定义 \(g:L\times H\to L\)。Algorithm 1（p4）的核心是：wake 用当前 \(\pi_L\) 产生轨迹 batch；sleep 用历史轨迹及其库版本编辑技能库。压缩成**本报告重述**：

\[
B\leftarrow\{\tau_i\sim\pi_L(q_i)\}_{i=1}^k,\quad
H\leftarrow H\cup\{(B,L)\},\quad L\leftarrow g(L,H).
\]

Inducer 可增、删、改 public skills 与 private helpers；代码解释器用于查询日志、统计调用栈、测试代码假设。方法节没有给出一个可微分的“最小 API 成本”训练损失；它以编码代理的分析/编辑协议实现改进，并以实验成本衡量结果。

**真实论文案例：观察 → 规则/控制策略 → 反馈 → 修正。** Figure 2、Appendix I.2/Table 4（pp3、23）记载：

1. 多批日志反复出现 `travel_to_visible_resource` 的 `not_found`；该函数在较后批次被调用116–250次。
2. Inducer 查询失败目标和调用树，判断是“资源不在可见范围”而非简单导航 bug。
3. 新增 `_bounded_exploration`：在局部邻域移动并持续读观察，发现目标后停止，仍找不到才返回失败。
4. 后续 actor 调用更新后的技能；有观察的有界搜索替代反复执行同一个注定找不到资源的调用。

这里学习的是带状态反馈的控制逻辑，不只是把成功动作录制成宏。Appendix I.1/Table 3 还给出 w/o-CI 版本在目标隐藏、阻塞、横向偏移失败后逐轮添加 guard；I.3/Table 5 给出电导实验先读灯是否亮再决定物体分类，并在重试间清空电路。应注明某个案例属于完整方法还是消融，不把消融发现全归给完整版本。

**验证边界。** Pure online 是不要求把旧环境任务 replay 一遍以决定是否接受库更新，**不是没有任何验证**。Appendix I.1 用历史 mission 字符串运行 parser 验证语序；I.3 有 code-tested normalization。原报告“不依赖重新回放环境或额外验证”应改成“不要求环境回放验收；coding agent 仍可做代码执行、统计和局部测试”。

## 5. MemRL：学经验的效用，未直接学环境转移规则

**问题定义。** 冻结生成模型，让检索成为受反馈影响的决策：相似经验不一定能帮助完成任务，应根据曾经使用的结果决定下次取谁。[R3] §§3–4，pp3–5。

**原式。** Eq.(1) 对检索记忆边缘化：

\[
\pi(a\mid s,M)=\sum_{m\in M}\mu(m\mid s,M)p_{LLM}(a\mid s,m).
\]

生成模型 \(p_{LLM}\) 固定；改变的是 retrieval policy \(\mu\)。Eq.(2) 用 \(\arg\max_{m\in M}Q(s,m)\) 表示选择高效用记忆的目标（原文将该 argmax 写作 \(\mu^*\)，应理解为贪心选择规则，不必把它当作完整概率分布定义）。Eq.(3) 给一般 TD 形式：

\[
Q(s,m)\leftarrow Q(s,m)+\alpha[r+\gamma\max_{m'}Q(s',m')-Q(s,m)].
\]

**实际实现使用 Eq.(4) 的终止状态/Monte-Carlo 式更新**：

\[
Q_{new}=Q_{old}+\alpha(r-Q_{old}).
\]

外部条目为 Eq.(5) 的 \(M=\{(z_i,e_i,Q_i)\}\)，分别是 intent、经验、效用。这里存的是每条经验的 \(Q_i\)，对相近 intent 的期望回报做近似，并非完整维护每个环境状态–动作的神经 Q 网络。

Eq.(6–7) 的两阶段检索：先对 intent embedding 做相似度阈值 \(\delta\) 与 top-\(k_1\) 过滤，再按

\[
score(s,z_i,e_i)=(1-\lambda)\widehat{sim}(Emb(s),Emb(z_i))+\lambda\widehat Q_i
\]

取 top-\(k_2\)。帽号是 **z-score 标准化**。无候选时回退到冻结模型。实际注入上下文的所有经验均用结果 reward 更新，再把新轨迹摘要作为新条目追加。

**和(b)的区别。** 它可以让总导致失败的相似经验被降权，从而减少重犯；但机制本身没有回答“失败是哪个前置条件不满足”或“动作怎样改变状态”。多条记忆共享同一结果也带来归因问题。若我们把 token/秒/钱写入 reward，那是对 MemRL 的**新改动和新评价目标**，不是该论文已经证明的成本优化。

**理论措辞。** §4.4/Appendix A 的稳定性依赖冻结模型、平稳任务分布及其其他假设；不要写成“任意漂移环境下必然持续改进”。作者自己在 §6/Appendix G 讨论长轨迹更新噪声、多人记忆归因、低任务相似性、反馈/奖励错误。

## 6. AWM 与 ReasoningBank：都从轨迹提炼文字，但反馈协议不同

### AWM

**问题定义/原式。** 原文以网站导航为例，\(L(q,M,o_i)\to a_i\)、\(T(s_i,a_i)\to s_{i+1}\)。给定经验集合 \(E\)，诱导模块 \(I(E)\to W=\{(d_j,P_j^d)\}\)，其中工作流包含用途、环境状态描述、推理和动作；然后 \(M+W\to M_w\)，未来用 \(L(q,M_w,o)\to a\)。这些是 §§2.1–2.3（pp2–3）的原始映射，**不是损失函数**。[R4]

Offline 从已有示例一次诱导；online 顺序做任务，成功评估后诱导和累积。对象参数会被抽象，例如具体商品名替换为 `{product-name}`。默认方法是把工作流作为上下文指导逐步行动；单次可执行宏是另一个实验，不应混淆。

**(b)覆盖。** 工作流可以含“当前是某页面时做哪步”，但没有单独维护“对某规则的支持/矛盾证据”，也没有对每一步预测未来状态并比对。§3.2.1 作者发现需要偏离工作流时仍会过度服从，§3.2.2 说明 online 生成轨迹可能错误并污染工作流。因此只能说它学习了可迁移过程经验，不能说已形成可靠环境规律。

### ReasoningBank

**问题定义/原式。** §3.1（p4）定义任务顺序到达、未知未来 query、test-time 无 ground truth，只能使用自己的轨迹和自我验证：\(\pi_L(o_{0:t},a_{0:t};M,A)\to a_{t+1}\)。AWM online 也使用 LM judge；这里的关键区别在于 ReasoningBank 同时利用被判成功与失败的轨迹，而非只从被判成功的轨迹诱导工作流。[R5]

**更新协议。** §3.2（p5）没有标量优化目标：检索相似记忆 → 完成任务 → LLM-as-judge 判成败 → 从成功抽策略，从失败抽教训 → 将 title/description/content 条目追加。用 **本报告重述** 写成

\[
\hat y_i=Judge(q_i,\tau_i),\quad
\Delta M_i=Extract(q_i,\tau_i,\hat y_i),\quad
M_i=M_{i-1}\cup\Delta M_i.
\]

默认 consolidation 是简单 addition，不能说它默认自动发现矛盾、合并和删除过时规则。MaTTS 另外花推理预算生成同题多条轨迹，再 self-contrast 或 sequential self-refine 以产生更有信息的记忆；它是增加经验信号的预算选择，不是免费降低成本。

**真实论文案例。** Appendix D Figure17（p30）中，找 Sony 蓝牙耳机的任务不断翻“下一页”直至超预算；抽出“优化查询、调高每页条数、使用过滤器”。这是“执行遇到无关对象/太多页面 → 诊断 → 操作策略 → 后续复用”的具体实例，直接涉及加速。但图没有提供逐条规则预测和证伪记录，不能据此包装成显式动力学模型。

## 7. MobileGPT：页面功能与动作适配，错误纠正可以来自人

**问题定义。** 在手机应用上首次完成自然语言任务较慢、不稳定；以后同类任务参数或 UI 内容改变时，希望保留已掌握的子任务执行方式。核心是每个 app 共用的页面–子任务图，而非每道任务单独缓存完整路径。[R6] §§3–5，pp4–8。

**原文使用结构与算法协议，没有显式数学优化目标。** 图的 node 由页面能提供的 subtask 集合定义；edge 是实现 subtask 的 primitive action 序列；task 是 node/subtask 对的序列。§4.2 先用关键 UI 属性检查当前屏幕是否具备已知子任务所需元素；不匹配才 Explore，并用子任务相似性再次查重。§5.1 的**原文变换例**是：

\[
click(index=5)\to click(id=contact,text=Bob)
\to click(id=contact,text=[contact\_name]).
\]

新参数为 Alice 时反向绑定，按当前页面属性找到 index=6。匹配索引由当前 UI 决定，不沿用历史位置。

**闭环。** 首次观察页面并学子任务 → 保存关键 UI 要求和动作属性模式 → 下次检查适用性并绑定参数 → 匹配失败时调用 LLM 重推；提供上次正确动作作为 few-shot，其中可含用户 HITL 改正的动作 → 用这些例子避免重复相同错误（§5.2）。这是学习环境的可用操作和适配条件，不是显式下一状态预测。

**边界。** §5.1 明说重放整个任务也会在每个子任务前问 LLM 做参数 slot filling，未知参数还会询问用户。因此“记忆命中=零 LLM”不成立。§7.3 的 warm-start 消融在 cold-start 失败后先人工修复；这属于作者实验协议，不能用“我们的局限推断”把它弱化成猜测。

## 8. ActionEngine：状态约束和操作语义怎样进入可执行程序

**问题定义。** 黑盒网站、无源码，通过 UI 探索获得可供规划的结构化知识；新任务时尽量一次生成程序，并用确定性执行替代大量逐步 LLM 决策。[R7] §§3–4，pp3–7。

**原结构。** State Machine Graph \(M=(S,O,T)\)。\(S\) 为稳定 GUI 页面模板而非每个内容实例，\(O\) 是有 input/source/destination/动作实现/输出描述与示例的操作，\(T\) 记录状态间转移。Appendix A 说明输入输出并非严格类型化，由自然语言说明和示例辅助 Planner 使用。列表项数和内容变化不必生成新状态；读数据的操作可为 self-loop。存的是访问实时数据的方法，不是把旧数据当答案。

**原文没有总成本最小化公式，用探索、编译和修复协议定义。** 离线 crawler 以导航结构和代表性控件探索页面，实际探查搜索是 exact/fuzzy/prefix、分页默认排序/条数、下拉选项等，丰富操作描述；编译时 BFS 找到前后操作之间的导航路径，并补入循环所需返回路径。可以用**本报告重述**说编译器在满足 `dst(previous)=src(next)` 的条件下连接操作，但论文不是据此训练一套模型。

**闭环实例（根据原文机制组合的说明，不是声称某条 benchmark 真实轨迹）。**

- 观察：某论坛页面和另一论坛有相同导航/列表结构；读取帖子与打开帖子操作的起止页面不同。
- 知识：它们属于同一页面模板；“读列表”产出实时数据，“打开帖子”需要指定帖子，执行后到帖子页。
- 约束：程序循环打开多个帖子时，编译器插入所需的返回列表路径；运行时从输出填参数。
- 反馈：若执行 locator 失败，Patcher 看实际页面重新定位；若错误是图中的通用 locator/描述，则持久修复记忆；若仅是本题程序逻辑则只修本题，并从受影响区域恢复。

以上出自 §§3–4 与 Appendices A–B（operations、sketch/compilation、node-level patching）。它非常接近用户的(b)，不是纯“缓存一条成功动作序列”。但**主评测把图经每种 task template 一题预热/完善后冻结，并关闭 Patcher**；主表收益支持准备好环境知识后的程序执行，不直接验证持续在线规则修复效果。

**已给出的实际反例。** Appendix 失败分析 p19：GitLab 查 `OPT model` 没返回，因为实际标题为 `OPT-175B inference` 等；Reddit `machine learning` 对不上 `MachineLearning` 的 exact-string 查询。作者将其归因于规划时先固定关键词却未见结果，并指出开启 Patcher 可按结果迭代，但该闭环未在主实验中启用。这比泛泛说“动态网站可能失败”更具体。

## 9. WALT：探索网站参数规律，并用执行测试反复修正

**问题定义。** 将浏览器 primitive actions 扩展为来自网站实际功能的高层操作。§3.1（pp3–4）把工具定义为 \(u:\mathcal S\to Goal\)；此处 \(\mathcal S\) 是**结构化输入参数空间**，不是环境状态集合。Candidate \(\tilde u=(s_i,E_i,G_i)\) 中 \(s_i\) 是 start URL、\(E_i\) 是交互元素、\(G_i\) 是目标。[R8]

**确有显式优化式。** §3.3 Eq.(1–3)，p5：

\[
\tilde u\xrightarrow{B_{browser}}\mathcal X
\xrightarrow{B_{tool}}(u,I_{test}),
\]

\[
\min\ \operatorname{FailRate}(u,I_{test})
+\operatorname{StepCount}(u)
+\operatorname{AgenticRatio}(u).
\]

三项分别是测试失败比例、primitive 操作数、需要 LLM 推理的步骤比例。原文直接相加，未给出归一化权重；实现是 agent 的 demonstrate–generate–optimize–test 循环与预算终止，不是对这三个量做可微分梯度下降。因此应称“工具正确性与执行成本的代理目标”，不能把它当作统一美元最优解。

**原文具体闭环。** §3.4（p5）的 search-listings 示例：

1. 浏览器实际用 bicycle、bikes 做搜索，记录输入/选项/提交与 URL 变化。
2. 从观察归纳 URL 中查询与类别参数含义，以及 Bikes=7、Cars+trucks=10 等枚举；生成有类型与可选字段的 schema。
3. 原多次 UI 操作被替换为参数化 URL 导航；schema 约束输入，工具说明记录 precondition 与 outcome。
4. 用多个真实测试输入执行；若缺类别、locator漂移、时序问题或语义不符，反馈给 builder。
5. 修改 schema、定位或执行脚本；过度 URL promotion 可以退回较保守实现，直到通过或预算耗尽。

这学习了“网站接受哪些参数、这些参数怎样影响结果”的环境规律，并检验它们，不能仅称动作压缩。§3.3 的 runtime fallback 是在意外失败时启用 fresh agent；结论 p10 将**长期 online tool patching**列为未来工作。不要把 fallback 等同已经评测成熟的跨任务持续修复。

## 10. WorldEvolver：预测误差更新上下文；实际语义规则范围要说准

**问题定义。** 在部分可观察交互中，冻结 agent 与 world-model LLM，让后者根据文本历史与候选 action 预测下一观察，部署时只更新外部记忆。§3.1 以 \((S,A,O,T)\) 表示环境，但符号 \(s_t\) 实际指 agent 可见的文本历史，不能将其解释成可直接访问真实隐藏状态。[R9] pp3–6。

**原式与原算法。** §3.2 的 episodic memory 记录真实转移 \((o_i,a_i,o_{i+1})\)，按当前动作和旧动作的 token-set Jaccard 相似度取 top-k；不是用 learned dynamics 检索下一状态。

\[
M_E^{t+1}=M_E^t\cup\{(o_t,a_t,o_{t+1})\}.
\]

Semantic memory 为 \(M_S^t=\{(r_i,e_i)\}\)。先把预测和真实观察分别转换成对象/关系/属性三元组 \(\hat z_{t+1}=g(\hat o_{t+1})\)、\(z_{t+1}=g(o_{t+1})\)。不一致触发 critic 产生规则；证据分初始1，随后依支持/矛盾加减 \(1/|M_S|\)，仅 \(e_i>0\) 的规则进入上下文。原文写 \(M_S^{t+1}=M_S^t\cup\Delta M_S^t\)，其中 \(\Delta\) 包含规则与证据更新，应理解为增量维护，不能误解成旧证据值永远不变的简单集合并集。

Selective foresight 的原式（p5）为：

\[
\ell_t=\frac1n\sum_{i=1}^n\log p_\theta(y_i\mid y_{<i},s_t,a_t,M_t),
\quad q_t=e^{\ell_t},\quad
F_t=\begin{cases}\hat o_{t+1},&q_t\ge\tau\\ \varnothing,&q_t<\tau.\end{cases}
\]

\(q_t\) 是生成 token 概率的几何平均，不是经过保证的真实世界正确率。Algorithm 1 先产生 draft action、预测并过滤，再用预测辅助生成 executed action。若执行动作变了，**重新预测执行动作的后果**再与实测对比，避免把另一个动作的预测误差拿来学规则。此协议有额外模型调用；效果与成本需分别评估。

**最重要的措辞边界：正文泛称 rule revision；附录实现限定 preservation rules。**

- 正文 §3.2 pp4–5 将 mismatches→candidate textual rules/heuristics 描述得较宽，并称 semantic memory 为将失败转成可检查知识的分支。
- Appendix E，Figure25，**p25** 的实际 extractor prompt 只收集“某动作后不应该改变的事实”，要求如果没有这种可复用规则就输出空列表。示例为 `examine.object_location`：检查对象不会移动对象。
- Figure22（p23）与 Figure23（p24）把这些规则命名为 frame axioms/persistence rules，要求 world model 不预测规则声明不变的属性发生变化。Figure23 同时明确：**episodic transitions 用作哪些东西会变化的类比，preservation rules 过滤虚假的变化**。

因此准确说法是：**WorldEvolver 整体仍利用真实转移与冻结模型知识预测 action effects；当前显式语义规则提取器实现主要学习持久性/不变性约束。** 这不是证明论文“完全不学因果/变化”，也不是正文逻辑矛盾；它是正文一般方法叙述与附录具体实现范围的差别。不得把 semantic 分支说成已自动发现各种因果机制、所有操作前置条件。

**闭环示例（本报告演示，依据 Fig.25 的规则模板；不是论文报告的 benchmark 轨迹）。** 当前观察“杯子在台面”，执行 examine；预测误以为杯子被移动，但实际观察仍在台面。三元组差异触发“examine 不改变物体位置”规则。下次 world model 检查同类动作时，规则约束其不要编造位置变化。之后实际观察支持/矛盾时更新证据分，证据非正则不再注入。这清楚展示了用户(b)，但它是 prompt 约束，不是程序证明或硬动作屏蔽。

**作者真实失败案例不得补写成成功修复。** Appendix D Table15（p18）中拿 soapbottle 时预测成功而实际 `Nothing happens`；Table16 的电路连接预测成功而实际无法匹配命令。作者用它们说明 action-based retrieval 得到相关领域却遗漏细粒度可执行条件；论文没在这些表中证明最终学出哪个正确前置条件。不能替作者编造因果解释与修复结局。

## 11. GLoW：全球探索价值与局部动作优势，不等同下一观察预测

**问题定义。** Jericho 文字游戏中稀疏奖励、局部最优、很大的状态动作空间使探索低效。GLoW 从存档选一个值得继续探索的状态，返回它，再从同一起点做多次局部试探；固定 LLM 从这些经验总结下一步何处/怎样探索。[R10] §§3.1–3.2，pp3–5。

**原式。** 轨迹价值取最大前缀累计奖励，而非简单末尾 reward：

\[
v(\tau)=\max_{t\in[1,T]}\sum_{j=1}^{t}r_j,
\qquad \mathcal F_{t+1}=top\text{-}k(\mathcal F_t\cup\{\tau_{new}\},v).\tag{原Eq.1}
\]

\[
W_{global}=g_{LLM}(\mathcal F)=\{(s_i,v_i,v_i')\}.\tag{原Eq.2}
\]

\(v_i\) 是已达到价值，\(v_i'\) 是 LLM 从失败瓶颈推测的未来潜力；后者**不是实际计算的 UCB 置信上界**，UCB 只用来解释 exploitation/exploration 的启发。Figure1（p4）用 \(align_{LLM}(s,W_{global})\) 给 archive 状态评分并 argmax 选择，再 replay 保存动作序列回到选中状态。

Figure2 的局部更新为 \(\mathcal T_s\leftarrow\mathcal T_s\cup\{\tau_i\}\)，\(W_{local}\leftarrow MAR(\mathcal T_s,\mathcal F)\)；下条轨迹用上条反思。Eq.(3)：

\[
\pi_{explore}(a\mid s_t,h_t)=Agent_{LLM}(s_t,h_t,W_{local},\mathcal T_s,\mathcal F).
\]

原文写 \(A(s,a)=Q(s,a)-V(s)\) 来动机说明比较同起点多路径为何有用，但 MAR 输出**文本 semantic advantages**：哪些动作有益、为什么、在何条件下；它不对每个动作估计数值优势后做 PPO/TRPO 参数更新。

**原文示意例。** §3.2 p5：多条路径到 cellar 后因没剑卡在 troll；全局分析判断 cellar 未来潜力高，返回该状态；局部试探比较后发现 take sword 虽无立即奖励但帮助通过瓶颈。这包含环境中的条件/策略认识与反馈，却没有 \(\hat o_{t+1}=W(s_t,a_t)\) 这样的显式预测—误差规则更新链。

**与(b)及加速关系。** 它是探索策略学习参考，尤其有助于问“值得补探索哪个状态”。但实验依赖能返回状态、合法动作接口（对 LLM 是 soft guidance），环境交互样本效率不等于部署延迟或总 API 费。不要用论文题名中的 world models 替代方法辨析。

## 12. 作者自述局限与我们的证据解释分开写

| 方法 | 作者明确自述/原实验协议及定位 | 本报告可作的推断或尚未证明之处 |
|---|---|---|
| Metis | §1 表示研究指出代码构造贵、跨任务较脆；§3.3 接纳依据 recurrence 而非成功归因；§3.5 admitted guard 为依赖/编译；本文未见单列 Limitations 节 | 复用门槛未显式优化净美元收益；编译通过不保证语义；环境变化后的大规模维护效益未量化。这些是我们的边界解释，不能加引号冒充作者限制清单 |
| SpeedRunner | p10 Limitations：因预算未测旗舰模型、SWE-bench/Terminal-bench；在线技能学习存在大误差条和不稳定；未研究 inducer 自身元学习 | 纯在线不回放的设定下，部署错误技能的代价与恢复可另设实验；不能称“作者证明所有业务任务最优” |
| MemRL | §6 p8、Appendix G pp25–26：长轨迹高方差、多个 memory 的信用归因、低相似性退化、reward/verifier 错误、共享记忆选择等 | 将 cost 纳入 utility 是我们可能扩展；该扩展需新的公平对照，不是简单改个奖励就保证降本 |
| AWM | §3.2.1 p6：难以适时偏离工作流；§3.2.2：在线错误轨迹会带来错误工作流；Appendix F Table13/Fig6 p15：动作宏任务成功率由4.8降至3.6，缺少中间弹窗观察会造成问题；该表旁文字另称“same…3.2”，与表不一致，应按表并披露不一致 | 需要显式适用条件、失效检测是一种归纳；不能声称 AWM 完全没有观察/适配，也不能说文字工作流自动保证泛化。不要把 §4.2 Table7 的文字动作表示实验误当宏实验：两表恰有相同4.8/3.6数值 |
| ReasoningBank | Appendix E pp29–30：检索/合并刻意简单，没全面比较其他记忆架构，LLM judge 有噪声 | 没有默认旧条目证伪/删除机制；动作步数下降不保证总费用下降。这两项分别来自方法/成本证据解释，而非全都来自作者 Limitations |
| MobileGPT | §5.2 p8：无关键属性、属性歧义、app变化会使匹配失败；§7.3 人工修复协议；§9 p13：缺文本表示/图像型界面不支持，跨 app 为扩展方向，VLM 增延迟 | 收益包含首次可靠路径来源，不能外推为全自主；大规模持续漂移下维护/修复回本仍需验证 |
| ActionEngine | §5.4、Appendix p19：搜索关键词必须事先选好，未见运行时结果会失败；主评估明确关闭 Patcher；预热/固定 SMG 是实验协议 | 主指标未验证线上持续修复；跨新模板/动态环境的结论要缩窄。这不是假想风险，是对评估适用范围的判断 |
| WALT | 结论 p10：站点探索/验证前期开销、发现范围依赖站点功能；动态UI/A-B/CAPTCHA/反自动化限制；罕见参数/重设计漂移；某些交互仍需agentic；在线 patch 为未来方向 | 运行 fallback 的存在不能证明工具库持续学习收益；成本回本要算新工具的边际执行成本 |
| WorldEvolver | Limitations p10：仅 ALFWorld/ScienceWorld 两个文本环境；token概率有些API不给；置信度与正确率关系可能依环境/模型变化。Appendix D p18：细粒度可执行条件仍会预测错 | preservation 是当前 extractor 范围，不是“没有任何变化/因果知识”；规则作为 prompt constraint 无形式正确性保证；额外预测/反思成本不一定由少走弯路抵消 |
| GLoW | §§3.1–3.2 明示重放/同状态多次探索与软合法动作；Appendix C.1 报成本；本文未见单列作者 Limitations 节 | 可重置/可枚举前提在企业网页未必可用，LLM反思可能误归因；这些是我们的迁移判断，不应写成作者已经验证的局限 |

## 13. 主报告可直接采用的实质修订

1. §4 Metis：明确“选中次数触发程序化”与“至少两个结构不同 query 支持工具”是不同条件，且候选任务不必成功；补原 Algorithm1。不要描述为每次都验证成功后提炼稳定工具。
2. §4 SpeedRunner：把“不依赖重新回放环境或额外验证”改为“不要求环境回放验收，但仍使用代码执行/测试分析日志”；增加它从环境错误推断规则并写入 guard/recovery 的真实案例。其与用户(b)有直接重合。
3. §4 MemRL：给实际 Eq.(4) 与 Eq.(7)，说明学习的是记忆效用与检索，不是环境动作 Q 网络；成功 reward 与成本 reward 区别保留。
4. §5 MobileGPT/ActionEngine/WALT：除效率数字外，各补一种知识形式及反馈：页面子任务适用性、状态前后置/操作语义、参数 schema+执行测试。这样用户可明白环境探索具体学到了什么。
5. §5 原“GLoW 与 WorldEvolver 学的是环境规律”宜改为“探索策略知识与环境预测模型是两条不同路线”，分述 GLoW 的价值/语义优势和 WorldEvolver 的预测误差更新。
6. WorldEvolver：正文保留整体预测能力，并限定当前 semantic extractor 主要抽保持不变的属性规则；不要反向扩大成“论文完全不学因果”。定位为 §3.2 vs Appendix E Figs22–25。
7. §8–9：用户的新方向不能只定义为“历史经验+环境规则+反馈”，这些元素已有重合。更具体的可测问题是：在目标任务流和环境变化条件下，何种表示/检查/修复及探测投入，能以相同成功要求取得更低**包含学习维护**的总成本。它仍是待验证的问题界定，不能先宣称组合新颖。

## 参考文献

[R1] Zijie Dai; Siuhin He; Hui Li; Qihui Zhou; Jiajun Li; Mingcong Song; Guoping Long; Hongjie Si; Xin Yao; Lin Zhang; James Cheng; Xiao Yan. **Metis: Bridging Text and Code Memory for Self-Evolving Agents**. 2026. arXiv:2606.24151v1，预印本（PDF 标注 Work in progress）。[所读版本](https://arxiv.org/pdf/2606.24151v1)。

[R2] Zixi Huang; Xiheng Wang; Andrew Wang; William Jurayj; Bernal Jiménez Gutiérrez; Daniel Khashabi; Nicholas Andrews. **Better, Faster, Stronger: Programmatic Skill Learning Best Reduces Agent Cost**. 2026. arXiv:2608.11338v1，预印本，方法名 SpeedRunner。[所读版本](https://arxiv.org/pdf/2608.11338v1)。

[R3] Shengtao Zhang; Jiaqian Wang; Ruiwen Zhou; Junwei Liao; Yuchen Feng; Zhuo Li; Yujie Zheng; Weinan Zhang; Ying Wen; Zhiyu Li; Feiyu Xiong; Yutao Qi; Bo Tang; Muning Wen. **MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory**. 2026. arXiv:2601.03192v2，预印本。[所读版本](https://arxiv.org/pdf/2601.03192v2)。

[R4] Zora Zhiruo Wang; Jiayuan Mao; Daniel Fried; Graham Neubig. **Agent Workflow Memory**. ICML 2025, Proceedings of Machine Learning Research 267:63897–63911. 本轮读正式 PMLR 版。[正式论文页](https://proceedings.mlr.press/v267/wang25bx.html)。

[R5] Siru Ouyang; Jun Yan; I-Hung Hsu; Yanfei Chen; Ke Jiang; Zifeng Wang; Rujun Han; Long T. Le; Samira Daruki; Xiangru Tang; Vishy Tirumalashetty; George Lee; Mahsan Rofouei; Hangfei Lin; Jiawei Han; Chen-Yu Lee; Tomas Pfister. **ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory**. 2025. arXiv:2509.25140v2，预印本。[所读版本](https://arxiv.org/pdf/2509.25140v2)。

[R6] Sunjae Lee; Junyoung Choi; Jungjae Lee; Munim Hasan Wasi; Hojun Choi; Steven Y. Ko; Sangeun Oh; Insik Shin. **MobileGPT: Augmenting LLM with Human-like App Memory for Mobile Task Automation**. ACM MobiCom 2024. DOI:10.1145/3636534.3690682。所读 arXiv:2312.03003v3，其 PDF 为正式标题；abs/早期版本题名不同。[所读版本](https://arxiv.org/pdf/2312.03003v3)。

[R7] Hongbin Zhong; Fazle Faisal; Luis França; Tanakorn Leesatapornwongsa; Adriana Szekeres; Kexin Rong; Suman Nath. **ActionEngine: From Reactive to Programmatic Web Agents via State Machine Memory**. 2026. arXiv:2602.20502v2，2026-09-28，预印本。[所读版本](https://arxiv.org/pdf/2602.20502v2)。

[R8] Viraj Prabhu; Yutong Dai; Matthew Fernandez; Krithika Ramakrishnan; Jing Gu; Yanqi Luo; Silvio Savarese; Caiming Xiong; Junnan Li; Zeyuan Chen; Ran Xu. **WALT: Web Agents that Learn Tools**. ICLR 2026. 本轮读会议正式 camera-ready，非旧 arXiv v1。[正式论文页与PDF入口](https://proceedings.iclr.cc/paper_files/paper/2026/hash/5b175f9e93873e3a10a6ce43dbb82e05-Abstract-Conference.html)。

[R9] Xuan Zhang; Wenxuan Zhang; See-Kiong Ng; Yang Deng. **Self-Evolving World Models for LLM Agent Planning**. 2026. arXiv:2606.30639v2，预印本，方法名 WorldEvolver。[所读版本](https://arxiv.org/pdf/2606.30639v2)。

[R10] Minsoo Kim; Seung-won Hwang. **Dual-Scale World Models for LLM Agents Towards Hard-Exploration Problems**. 2025. arXiv:2509.24116v2，2025-09-30，预印本，方法名 GLoW。[所读版本](https://arxiv.org/pdf/2509.24116v2)。
