# Claude 综述挖掘稿局部审核：定义、提示优化与经验记忆

日期：2026-09-30。审核人：Codex / survey_memory。审核对象：`notes/part3/2026-09-30-self-improvement-survey-mining-zh.md`，本次读取时的第 22–212 行（§1、§2、§3.1–3.2）。原稿未改动；以下 CM 编号只在本文件内有效，不占用全局 E/D。

## 核查范围与结论

已逐段读完指定范围，并以 `2026-09-30-part3-survey-mining-ledger.md`、`2026-09-30-part3-records-s.md` 为定位线索。重点回查了综述原始 HTML 的 §3–4，TextGrad 的 §1–3.3，PROMST §3–4，Memento §4.2/5.3，MemQ §3–5.2，ReAP §3–5 和表 1–2，AWM 正式 PDF 的附录 D/F 与表 11/13，ReasoningBank 附录 C.2/表 5，Dynamic Cheatsheet 第 9 页脚注 13，以及 MemRL §3–4/附录 F。FORGE 回查方法和实验协议。不是对本报告全部 82 篇重新全文审核，也没有复现实验。

**发现一项会改变文献判断的实质遗漏：ReAP 的 token、执行时间及新任务迁移结果被漏掉。** 其余重点是需要补明的概念边界：文本梯度的比喻性质、辅助网络训练、公式缩写与每次成功口径。没有发现所核 AWM、ReasoningBank、DC 的主要数值被抄错；这些段落已有的基线、计费范围及版本限定应保留。

## CM-01｜确认，优先修正：遗漏 ReAP 的直接加速证据，造成“只有 Metis”的错误印象

**原稿位置。** 第 182 行只写 ReAP 重做任务的步数；第 196 行称“执行 token 和轮次都下降的是 Metis”；第 509 行效率表也只保留 ReAP 的步数。后两处虽未写“唯一”，上下文会让读者以为文本记忆没有这类结果。

**原文核对。** ReAP v1，PDF 第 3 页表 1、第 4 页表 2；§5 将既有轨迹分为 80% 建库、20% 测试，检索 5 条。表题均标 70 个 WebArena 任务、平均执行成本。官方 PDF 文字层与缓存 HTML 一致：

| 设置 / 变体 | 总 token | 执行时间 Tct（秒） | 步数 |
|---|---:|---:|---:|
| 表 1，重做旧任务，N/A → Summary | 221k → 58k | 682 → 334 | 11.92 → 11.27 |
| 表 2，相似新任务，N/A → Reflection | 221k → 83k | 682 → 327 | 11.92 → 8.45 |

短引文：**“reduces task execution cost while improving SR”**（§5.2，PDF 第 4 页）。[原文 PDF](https://arxiv.org/pdf/2506.02158v1)。§5.1 同时报告新任务设置成功率提高 11 个百分点。

**必须带的限制。** 执行器为 GPT-4o / AgentOccam；成本表标 AgentOccam-Judge。论文未报告跨随机种子的方差，也未把建库、生成反思的成本摊入此表。不是生产网站漂移、跨网站迁移或企业表单实验。作者把节省归因于无效动作导致的重新提示减少；这不是我们已复现的机制归因。

**精确旧 → 新建议。**

- 第 182 行在既有内容后补：
  > 另有相似新任务实验（轨迹 80/20 分割、检索 top-5）：Reflection 的成功率比基线高 11 点；表 2 的平均总 token 为 221k→83k，执行时间 682→327 秒，步数 11.92→8.45。该成本表没有计入建库成本，也没有重复运行方差。
- 第 196 行“执行 token 和轮次都下降的是 Metis（把重复计划固化成工具）” →
  > 执行 token 和步数同时下降的例子包括 Metis，以及 ReAP 的相似新任务 Reflection 设置；后者还报告执行时间下降。两者的任务、基线和成本范围不同，不能直接比幅度。
- 第 509 行同步补上述表 2 结果。第 200 行“没有找到同成功率条件的墙钟对照”不被本结果直接推翻：ReAP 的成功率发生了变化；但不能再由此暗示没有同时改善成功率与时延的文本记忆结果。

## CM-02｜确认，需要解释而非纠错：必须说明“文本梯度”不是真正的数值导数

**原稿位置。** 第 114、125 行将 TextGrad 与其他方法并列，但没有回答用户明确问过的“为什么可以通过文本找梯度”。当前文字没有直接断言数学可微，因此此项是关键解释缺失。

**原文。** TextGrad v1 §1：**“we use differentiation and gradients as a metaphor for textual feedback from LLMs”**。§2 和附录 A 定义的是沿计算图反向生成并聚合自然语言反馈，再让优化器 LLM 根据反馈修改变量。黑盒 API 不需要返回参数梯度。[原文 §1–2](https://arxiv.org/html/2406.07496v1#S2)。

**精确旧 → 新建议。** 第 125 行“文本梯度这一支。” →

> 这里的“梯度”是自然语言修改建议的比喻，不是对离散文本计算出的数值导数。TextGrad 把提示、中间输出和评价连成计算图：评价 LLM 指出输出的问题，反向调用结合该节点的输入、输出和下游反馈，把建议传给上游提示；优化器 LLM 再据此写出候选新提示。这是一种借助模型语义判断的候选生成与信用分配方法，不构成真实链式求导或性能必然单调提高的保证。

可选问题定义公式（**本文流程改写，非论文原式**）：

\[
g_v=\operatorname{Aggregate}_{w\in\operatorname{Succ}(v)}
\operatorname{FeedbackLLM}(v,w,\text{前向上下文},g_w),\qquad
v'=\operatorname{EditLLM}(v,g_v).
\]

其中 \(g_v\) 是文字反馈，\(v'\) 是候选新文本。不应把 \(g_v\) 标成真实导数。

第 118 行“TextGrad（验证集变好才更新）”建议限缩为“TextGrad 的提示优化实验（§3.3，验证集变好才更新）”。该句与原文相符，但不是框架所有应用共同强制的门。§3.3 使用训练样本产生修改，用验证集决定保留；测试集用于报告。

## CM-03｜确认，需要显式区分：基础模型冻结不等于没有辅助模型训练

**原稿位置。** 第 150 行“它们都不改任务模型的参数”是可保留的窄表述；第 187 行把 MemRL / MemQ / Memento 放在同一段，容易让读者把三者的 Q 更新理解为相同操作。第 123 行虽写 PROMST 有训练预测器，但未说明它训练了什么。

| 方法 | 原文证据与定位 | 需要保留的边界 |
|---|---|---|
| MemRL | §3–4，Eq. 4 对记忆的标量效用做 \(Q\leftarrow Q+\alpha(r-Q)\)；Eq. 6–7 用相似度筛选及效用重排 | 不是对 LLM 或新的 Q 神经网络做梯度训练 |
| MemQ | §3、§4.3，Eq. 3/5/6；对记忆条目的 Q 标量和来源 DAG 做更新 | 冻结基础 LLM，近似的记忆信用传播，不应称为训练 LLM |
| Memento 参数化读取 | §4.2 Eq. 14–16：**“Q is implemented as a neural network”**；§5.3：**“two-layer MLP”** | 冻结 LLM 和文本编码器，但另外训练 Q 网络；非参数化读取则用余弦相似度 |
| PROMST | §3.2 Score Prediction Model：**“fine-tune a task-specific bidirectional Longformer-base (148M)”**；每代用新提示—分数对继续更新 | TaskLLM / PromptLLM 不微调，辅助评分模型微调 |

[MemRL](https://arxiv.org/html/2601.03192v2#S4)、[MemQ](https://arxiv.org/html/2605.08374v3#S4)、[Memento](https://arxiv.org/html/2508.16153v2#S4.S2)、[PROMST](https://arxiv.org/html/2402.08702v4#S3.S2)。

**精确旧 → 新建议。**

- 第 187 行“Q 用二元任务奖励训练” → “该参数化版本把 Q 实现为两层 MLP，以二元任务奖励的交叉熵损失训练；基础 LLM 不更新。它与 MemRL、MemQ 的表格式记忆效用更新不同。”
- 第 123 行“一个训练出来的分数预测器” → “在线微调的 Longformer-base（148M）评分器”。
- 第 150 行末补：“本节的冻结指任务 LLM；另训辅助网络的方法会单独注明。”

这不是建议把 Memento 或 PROMST 排除：原稿提出必要时考虑辅助训练（是否来自用户另一会话的授权，本轮未核实）；分类准确后才能判断第一版复现成本。

## CM-04｜口径限定，非公式错误：每次成功的均摊与同题重试到成功不同

**原稿位置。** §2.1 第 56 行，\(T_{success}=\mathbb E[T_{attempt}]/R\)、\(v=C/R\)。

这两个比值可作为**固定评测口径下，总耗时/总费用除以成功数**的总体指标。若解释为“同一道题不断重试，直到成功的期望总耗时/费用”，还需要固定策略、重置方式、尝试分布等额外条件。任务异质、记忆持续更新或失败后改变策略时，不能自动等同。此判断是数学/评测口径审核，不是某论文的实验结论。

项目自己的 `notes/part1/2026-09-27-doc1-agent-slow-and-expensive-zh.md` 第 132、170 行已明确区分账面折算和真实重试花费；建议这里同步带上，避免独立 HTML 读者丢失限定。

**精确补句：**

> 这里先采用同一评测任务分布、同一统计窗口下的均摊口径：全部尝试的总耗时或总费用除以成功数；它不自动等于对同一任务重试到成功的期望成本。持续学习时要说明是否冻结记忆，并把建库与改进成本另计或按明确使用量摊销。

## CM-05｜公式出处与覆盖：少量缩写应标清，重点方法不宜因记录缺项而省略

**确认。** 综述的 \(\mathcal A_t,\Sigma_t,X_t\) 及更新式来自 §3 Eq. 1–6；报告对原文记号冲突的提示可保留。PROMST Eq. 1/2 和 Dynamic Cheatsheet Eq. 1/2 与原文相符；MemQ §3 的独立贡献近似也确实由作者提出，报告没有擅自把它当定理。

**需要收紧的地方。** 第 98/159 行“照抄”过于绝对，表格实际上有删去条件及求和上下限的压缩。例：第 163 行 MemQ 的 \(V^{\pi_{ret}}(M_t)=E[\sum_k\gamma^kr(\tau_{t+k})]\) 源式显式从 \(k=0\) 到无穷、以 \(M_t\) 为条件，并列出 \(s,A,\tau\) 的抽样分布。可改成“按论文原定义重排；缩写不改变含义，另行推导的式子标为本文改写”，或恢复完整原式。

**精确恢复 MemQ 原定义：**

\[
V^{\pi_{\mathrm{ret}}}(\mathcal M_t)=
\mathbb E_{s_k\sim\rho,\,A_k\sim\pi_{\mathrm{ret}},\,\tau_k\sim\pi_{\mathrm{LLM}}}
\left[\sum_{k=0}^{\infty}\gamma^k r(\tau_{t+k})\mid\mathcal M_t\right].
\]

位置：MemQ v3 §3 “Value functions and learning objective”，紧接 Eq. 2 后的无编号式。原文短引文：**“Assuming retrieved memories contribute independently”**。这也限定了后面的每条记忆信用近似；不是无条件因果贡献估计。

第 176 行“MemRL、Memento……没有问题定义条目”准确描述了当前审计记录的覆盖，**不等于论文没有定义**。为了完整回答用户，建议至少补入 MemRL 实际 Eq. 4（见 CM-03）和 Memento 实际 Eq. 15：

\[
\mathcal L(\theta)=\mathbb E_{(s,c,r)}
[-r\log Q(s,c;\theta)-(1-r)\log(1-Q(s,c;\theta))].
\]

这里 \(\theta\) 是 Q 网络参数；\(s\) 是当前任务状态、\(c\) 是候选历史案例、\(r\in\{0,1\}\) 是奖励。**此处 \(\theta\) 不是综述中基础 LLM 的 \(\theta\)**，不能跨行沿用含义。ReAP 也可直接用 Algorithm 1 的建库—检索—拼接协议定义问题，无需发明损失函数。

## 已核支持保留，以及仍须保留的“不确定”

| 结论 | 本次核查结果 | 原文位置 / 短引文 |
|---|---|---|
| AWM 的 35.5 对 23.5，与步数 5.9 对 7.9 不是同一基线行 | 保留原稿的区别。不能把两个改善拼成同一严格配对结果 | 正式稿表 1；附录 D/表 11（PDF 第 14 页） |
| AWM 三项 token 33,718.5 / 2,298.6 / 1,344.6，总额相对自身动作生成项增加约 10.8% | PDF 页面直接核对，数值正确。正文中的“计算”最好继续注明按 token 算，不是实测时延 | 表 11；短引文：“10.8% computation overhead” |
| AWM 动作变体没有改善任务成功率；3.6 对 4.8 | 第 15 页表 13 确认。邻接正文却说相同、写 3.2，这是源文内部矛盾；原稿已提示，保留 | 附录 F / 表 13；其机场弹窗例子确实指出预定序列看不到中间状态 |
| ReasoningBank 总 token 53,054.5 对 50,847.4，约 +4.3% | 表 5 确认。动作生成下降并不等于总 token 下降 | v2 附录 C.2、PDF 第 26–27 页；短引文：“for each task” |
| ReasoningBank 表 5 的模型/基准未明写 | 保留“不明写、与 +20.5% 对应属于推断”。不要擅自升级成同一 Gemini-Flash 运行的确定事实 | 同上 |
| DC 的 370 / 1035 / 1831 | 第 9 页脚注 13 视觉确认；原稿保留未知 token 类型及是否含策展的限制是必要的。不能由此单独断言端到端总费用增至 4.9 倍 | v1 §5、脚注 13；短引文：“Claude Sonnet averaged 370 tokens” |
| DC Game of 24 的 10%→99% | 数值可保留，建议注明 99% 来自 DC-RS；相同生成器提示、空记忆 DC-∅ 为 19%，因此不能把完整 89 点都单独归因于记忆 | v1 §4.1/表 1；这是控制变量限定，不推翻求解器复用机制 |
| MemRL 约 32K token、10 epochs 的统计范围 | 第 24 页附录 F 视觉确认。原稿没有擅自乘/除 10，正确；作者没有给出 MemP 的对应 token 数 | 短引文：“average total token consumption per question” |
| MemRL 的墙钟数据 | 附录 F.2/图 11 确有每轮 2,500 题的小时曲线；不是独立部署任务时延、不是与无记忆的比较。可补说“有整轮学习墙钟图”，不能作为已证实部署加速 | v2 PDF 第 24–25 页；作者把波动归于网络/吞吐，这只是作者解释 |
| MemQ 五个留出基准第一，差距小 | 逐行核表 1，最高其他方法与 MemQ 的差值分别约 .23/.95/.19/.83/0/.99 点，均小于 MemQ 自身所列 ±。但“在 ± 内”不是显著性检验，不应再推导“没有显著效果” | v3 §5.2/表 1，3 seeds；选最佳 epoch 的准则未交代 |
| FORGE 冠军记忆覆盖其他活跃实例 | 原方法明确是整库覆盖，原稿正确；不是合并全体经验。实例数和每实例开销不应被混同成整个种群成本 | §3 “Champion Broadcast”；短引文：“complete memory state replaces the memory” |

**未作保证。** 本次没有重新核查 §3.1–3.2 所有其他工作的每个实验值，也没有证明“所有文献都没有某种目标”这一类全局否定。建议保留“本文核对过的文献/相应版本和设置”限定。ReAP 的遗漏说明，已读过论文或已有审计条目，不自动代表报告提取了所有与加速直接相关的数据。

## 参考文献与实际核查版本

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

上述 `.../part3-verification` 的完整前缀为 `/Users/edwin/.claude/projects/-Users-edwin-projects-agent-acceleration-research/part3-verification`。缓存仅为复核定位；方法与数值判断依据论文正文，不以审计记录或摘要替代原文。
