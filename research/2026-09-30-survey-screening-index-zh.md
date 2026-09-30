# Self-Improvement Survey 文献筛查索引

本索引汇总方法筛查数据与评测补核，供查阅与审计；不新增研究结论。

**本索引覆盖253条方法记录与59条评测记录，共312条目录行；不等于312篇独立论文，也不代表每篇都已全文阅读。** 方法253行的原分类保留如下；本次新增的评测59行位于文末。 目录存在跨分类重复、题名与链接不一致等情况。阅读深度按实际记录区分目录初筛、摘要／元数据、方法核验与深读；“深读”表示读取了研究所需的方法、实验及相关附录，不表示逐页逐句审核所有内容。仅作去重的条目不继承另一条目的阅读深度。

修订后的主报告引用 **40篇原有论文及12篇新增评测论文，并参考用户提供的演讲字幕**；这是有范围限定的研究整理，不是完整系统综述。排除项和待核项仅为审计记录，不构成对论文全部内容、质量或效果的背书；排除也不等于原论文没有价值。

| 处理 | 目录记录数 | 含义 |
|---|---:|---|
| 核心证据 | 15 | 筛查记录将其列为本研究问题的核心证据 |
| 方法相关 | 47 | 方法与目标有关，但不自动意味着已有净加速证据 |
| 背景参考 | 63 | 提供相邻机制或研究背景 |
| 范围排除 | 70 | 按本次研究范围排除，详见各行原因和阅读深度 |
| 重复记录 | 17 | 同文献的重复目录记录，不重复计为独立论文 |
| 待核 | 41 | 当前证据不足以完成相关性、训练边界等判断 |
| 合计 | 253 | 按原始目录逐条计数 |

题名优先采用 JSON 已记录的实际落地题名；链接优先采用已记录的 `canonical_url`，否则沿用原 `url`。目录原题名与实际落地题名不同时，会同时保留原题名。缺少 URL 的条目不补造链接。原因保留 JSON 的筛查判断，不因本索引的呈现方式扩展其结论。

## 1.1 Intrinsic Generative Demonstrations · 内生生成式示范

共 23 条目录记录。

| 目录行 ID | 题名 | 处理 | 阅读深度 | 原因 |
|---:|---|---|---|---|
| 1 | [Self-Instruct: Aligning Language Models with Self-Generated Instructions](https://arxiv.org/abs/2212.10560) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 2 | [Large Language Models Can Self-Improve](https://arxiv.org/abs/2210.11610) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 3 | [Orca: Progressive Learning from Complex Explanation Traces of GPT-4](https://arxiv.org/abs/2306.02707) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 4 | [SELF: Self-Evolution with Language Feedback](https://arxiv.org/abs/2310.00533) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 5 | [SELF-GUIDE: Better Task-Specific Instruction Following via Self-Synthetic Finetuning](https://arxiv.org/abs/2407.12874) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 6 | [Improving Model Alignment Through Collective Intelligence of Open-Source LLMS](https://arxiv.org/abs/2505.03059) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 7 | [Superficial Self-Improved Reasoners Benefit from Model Merging](https://arxiv.org/abs/2503.02103) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 8 | [Will Pre-Training Ever End? A First Step Toward Next-Generation Foundation MLLMs via Self-Improving Systematic Cognition](https://arxiv.org/abs/2503.12303) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 9 | [TaskCraft: Automated Generation of Agentic Tasks](https://arxiv.org/abs/2506.10055) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 10 | [Iterative Tool Usage Exploration for Multimodal Agents via Step-wise Preference Tuning](https://arxiv.org/abs/2504.21561) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 11 | [Maximizing Confidence Alone Improves Reasoning](https://arxiv.org/abs/2505.22660) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 12 | [DIVE: Diversified Iterative Self-Improvement](https://arxiv.org/abs/2501.00747) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 13 | [Self-Adapting Language Models](https://arxiv.org/abs/2506.10943) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 14 | [First SFT, Second RL, Third UPT: Continual Improving Multi-Modal LLM Reasoning via Unsupervised Post-Training](https://arxiv.org/pdf/2505.22453) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 15 | [LADDER: Self-Improving LLMs Through Recursive Problem Decomposition](https://arxiv.org/abs/2503.00735) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 16 | [Self-Consistency Preference Optimization](https://arxiv.org/abs/2411.04109) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 17 | [Adapting While Learning: Grounding LLMs for Scientific Problems with Tool Usage Adaptation](https://arxiv.org/abs/2411.00412) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 18 | [Reinforcing General Reasoning Without Verifiers](https://arxiv.org/abs/2505.21493) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 19 | [SAGE: Multi-Agent Self-Evolution for LLM Reasoning](https://arxiv.org/abs/2603.15255) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 20 | [ANDES: Agent Native Data Evolving Synthesis Tool for Autonomous Instruction Alignment](https://arxiv.org/abs/2606.01279) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 21 | [EvoGround: Self-Evolving Video Agents for Video Temporal Grounding](https://arxiv.org/abs/2605.13803) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 22 | [From Self-Evolving Synthetic Data to Verifiable-Reward RL: Post-Training Multi-turn Interactive Tool-Using Agents](https://arxiv.org/abs/2601.22607) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 23 | [RAGShaper: Eliciting Sophisticated Agentic RAG Skills via Automated Data Synthesis](https://arxiv.org/abs/2601.08699) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |

## 1.2 Intrinsic Evaluative Feedback · 内生评估反馈

共 21 条目录记录。

| 目录行 ID | 题名 | 处理 | 阅读深度 | 原因 |
|---:|---|---|---|---|
| 24 | [STRIVE: Structured Reasoning for Self-Improvement in Claim Verification](https://arxiv.org/abs/2502.11959) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 25 | [Beyond Accuracy: The Role of Calibration in Self-Improving Large Language Models](https://arxiv.org/abs/2504.02902) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 26 | [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 27 | [ReST meets ReAct: Self-Improvement for Multi-Step Reasoning LLM Agent](https://arxiv.org/abs/2312.10003) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 28 | [Self-Evolved Reward Learning for LLMs](https://arxiv.org/abs/2411.00418) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 29 | [Sample, Predict, then Proceed: Self-Verification Sampling for Tool Use of LLMs](https://arxiv.org/abs/2506.02918v1) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 30 | [RLSR: Reinforcement Learning from Self Reward](https://arxiv.org/abs/2505.08827) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 31 | [Right Question is Already Half the Answer: Fully Unsupervised LLM Reasoning Incentivization](https://arxiv.org/abs/2504.05812) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 32 | [TTRL: Test-Time Reinforcement Learning](https://arxiv.org/abs/2504.16084) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 33 | [Can Large Reasoning Models Self-Train?](https://arxiv.org/abs/2505.21444) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 34 | [Self Rewarding Self Improving](https://arxiv.org/abs/2505.08827v1) | 重复记录 | 目录／综述初筛 | 与前行重复或题名/URL冲突，保留原始行供复核；不能当独立证据。 |
| 35 | [Self-Evolving Curriculum for LLM Reasoning](https://arxiv.org/abs/2505.14970) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 36 | [Reflect, Retry, Reward: Self-Improving LLMs via Reinforcement Learning](https://arxiv.org/abs/2505.24726) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 37 | [Adaptive Self-improvement LLM Agentic System for ML Library Development](https://arxiv.org/abs/2502.02534) | 方法相关 | 深读（方法与实验） | 固定模型的成功示例筛选/难度课程；扩大test-time compute，3.9倍是完成题数比例，不是agent速度。 |
| 38 | [Learning to Reason without External Rewards](https://arxiv.org/abs/2505.19590) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 39 | [Structured Reasoning for Large Language Models](https://arxiv.org/abs/2601.07180) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 40 | [iReasoner: Trajectory-Aware Intrinsic Reasoning Supervision for Self-Evolving Large Multimodal Models](https://arxiv.org/abs/2601.07180) | 待核 | 目录／综述初筛 | 与前行重复或题名/URL冲突，保留原始行供复核；不能当独立证据。 |
| 41 | [STRIVE: Structured Reasoning for Self-improvement in Claim Verification](https://link.springer.com/article/10.1007/s11633-025-1598-5) | 重复记录 | 目录／综述初筛 | 与前行重复或题名/URL冲突，保留原始行供复核；不能当独立证据。 |
| 42 | [UniCorn: Towards Self-Improving Unified Multimodal Models through Self-Generated Supervision](https://arxiv.org/abs/2601.03193) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 43 | [Retrospective Progress-Aware Self-Refinement for LLM Agent Training](https://arxiv.org/abs/2606.14302) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 44 | [EVE-Agent: Evidence-Verifiable Self-Evolving Agents](https://arxiv.org/abs/2605.22905) | 范围排除 | 深读（方法与实验） | EVE-Agent §4.1：Qwen2.5-3B proposer/solver做policy-gradient训练，不符合本轮权重固定范围。 |

## 1.3 Extrinsic Exploratory Experience · 外部探索经验

共 33 条目录记录。

| 目录行 ID | 题名 | 处理 | 阅读深度 | 原因 |
|---:|---|---|---|---|
| 45 | [RoboCat: A Self-Improving Generalist Agent for Robotic Manipulation](https://arxiv.org/abs/2306.11706) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 46 | [Tool-Star: Empowering LLM-Brained Multi-Tool Reasoner via Reinforcement Learning](https://arxiv.org/abs/2505.16410) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 47 | [CodeARC: Benchmarking Reasoning Capabilities of LLM Agents for Inductive Program Synthesis](https://arxiv.org/abs/2503.23145) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 48 | [LLMs are Greedy Agents: Effects of RL Fine-tuning on Decision-Making Abilities](https://arxiv.org/abs/2504.16078) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 49 | [Agent-RLVR: Training Software Engineering Agents via Guidance and Environment Rewards](https://arxiv.org/abs/2506.11425) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 50 | [WebRL: Training LLM Web Agents via Self-Evolving Online Curriculum Reinforcement Learning](https://arxiv.org/abs/2411.02337) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 51 | [Self-Improving Language Models for Evolutionary Program Synthesis: A Case Study on ARC-AGI](https://arxiv.org/abs/2507.14172) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 52 | [DeepResearcher: Scaling Deep Research via Reinforcement Learning in Real-world Environments](https://arxiv.org/abs/2504.03160) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 53 | [Agentic Reasoning and Tool Integration for LLMs via Reinforcement Learning](https://arxiv.org/abs/2505.01441v1) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 54 | [UI-Genie: A Self-Improving Approach for Iteratively Boosting MLLM-based Mobile GUI Agents](https://arxiv.org/abs/2505.21496) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 55 | [RAGEN: Understanding Self-Evolution in LLM Agents via Multi-Turn Reinforcement Learning](https://arxiv.org/abs/2504.20073) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 56 | [SEAgent: Self-Evolving Computer Use Agent with Autonomous Learning from Experience](https://arxiv.org/abs/2508.04700) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 57 | [WebGym: Scaling Training Environments for Visual Web Agents with Realistic Tasks](https://arxiv.org/abs/2601.02439) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 58 | [Kevin: Multi-Turn RL for Generating CUDA Kernels](https://arxiv.org/abs/2507.11948) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 59 | [Tool-R0: Self-Evolving LLM Agents for Tool-Learning from Zero Data](https://arxiv.org/abs/2602.21320) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 60 | [Socratic-SWE: Self-Evolving Coding Agents via Trace-Derived Agent Skills](https://arxiv.org/abs/2606.07412) | 范围排除 | 深读（方法与实验） | Socratic-SWE §§11–13：GRPO/GDPO、AdamW更新solver；trace-derived skills参与训练，不可误纳免训练。 |
| 61 | [Self-evolving LLM Agents with In-Distribution Optimization](https://arxiv.org/abs/2606.07367) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 62 | [Skill Self-Play: Pushing the Frontier of LLM Capability with Co-Evolving Skills](https://arxiv.org/abs/2607.22529) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 63 | [Language Models Meet World Models: Embodied Experiences Enhance Language Models](https://arxiv.org/abs/2305.10626) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 64 | [Agent Planning with World Knowledge Model](https://arxiv.org/abs/2405.14205) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 65 | [Web Agents with World Models: Learning and Leveraging Environment Dynamics in Web Navigation](https://arxiv.org/abs/2410.13232) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 66 | [Understanding World or Predicting Future? A Comprehensive Survey of World Models](https://arxiv.org/abs/2411.14499) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 67 | [General agents contain world models](https://arxiv.org/abs/2506.01622) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 68 | [WebEvolver: Enhancing Web Agent Self-Improvement with Coevolving World Model](https://arxiv.org/abs/2504.21024) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 69 | [WebSynthesis: World-Model-Guided MCTS for Efficient WebUI-Trajectory Synthesis](https://arxiv.org/abs/2507.04370) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 70 | [GAWM: Global-Aware World Model for Multi-Agent Reinforcement Learning](https://arxiv.org/abs/2501.10116) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 71 | [WMPO: World Model-based Policy Optimization for Vision-Language-Action Models](https://arxiv.org/abs/2511.09515) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 72 | [Internalizing World Models via Self-Play Finetuning for Agentic RL](https://arxiv.org/abs/2510.15047) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 73 | [AlignUSER: Human-Aligned LLM Agents via World Models for Recommender System Evaluation](https://arxiv.org/abs/2601.00930) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 74 | [Self-Evolving World Models for LLM Agent Planning](https://arxiv.org/abs/2606.30639) | 方法相关 | 深读（方法与实验） | WorldEvolver v2：actor和world model固定权重；转移记忆/文字规则/置信门禁。深读表2为best-of-5质量，未证明净加速。 |
| 75 | [NavMorph: A Self-Evolving World Model for Vision-and-Language Navigation in Continuous Environments](https://arxiv.org/abs/2506.23468) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |
| 76 | [EvoWorld: Evolving Panoramic World Generation with Explicit 3D Memory](https://arxiv.org/abs/2510.01183) | 待核 | 目录／综述初筛 | 集合归在foundation-model，但题名不足以确认训练边界；未全文核验，不据此宣称该工作不相关或无加速。 |
| 77 | [RISE: Self-Improving Robot Policy with Compositional World Model](https://arxiv.org/abs/2602.11075) | 范围排除 | 目录／综述初筛 | 目录与综述初筛为SFT/RL/模型能力训练分支；本轮不纳入免训练核心，未对全部附录作独立审核。 |

## 2.1 Prompt Optimization · 提示优化

共 39 条目录记录。

| 目录行 ID | 题名 | 处理 | 阅读深度 | 原因 |
|---:|---|---|---|---|
| 78 | [Large Language Models Are Human-Level Prompt Engineers](https://arxiv.org/abs/2211.01910) | 背景参考 | 目录／综述初筛 | APE候选提示搜索；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 79 | [Large Language Models as Optimizers](https://arxiv.org/abs/2309.03409) | 背景参考 | 目录／综述初筛 | OPRO分数反馈搜索；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 80 | [Prompt Refinement with Image Pivot for Text-to-Image Generation](https://arxiv.org/abs/2407.00247) | 背景参考 | 目录／综述初筛 | 图像生成提示优化；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 81 | [Learning from Contrastive Prompts: Automated Optimization and Adaptation](https://arxiv.org/abs/2409.15199) | 背景参考 | 目录／综述初筛 | 对比提示优化；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 82 | [PRompt Optimization in Multi-Step Tasks (PROMST): Integrating Human Feedback and Heuristic-based Sampling](https://arxiv.org/abs/2402.08702) | 背景参考 | 目录／综述初筛 | 多步任务prompt优化PROMST；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 83 | [The Prompt Alchemist: Automated LLM-Tailored Prompt Optimization for Test Case Generation](https://arxiv.org/abs/2501.01329) | 背景参考 | 目录／综述初筛 | 测试样例生成prompt优化；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 84 | [DRO-InstructZero: Distributionally Robust Prompt Optimization for Large Language Models](https://arxiv.org/abs/2510.15260) | 背景参考 | 目录／综述初筛 | 鲁棒prompt优化；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 85 | [CoolPrompt: Automatic Prompt Optimization Framework for Large Language Models](https://ieeexplore.ieee.org/document/11239071) | 背景参考 | 目录／综述初筛 | 通用prompt优化；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 86 | [SePO: Self-Evolving Prompt Agent for System Prompt Optimization](https://arxiv.org/abs/2606.04465) | 背景参考 | 目录／综述初筛 | SePO优化prompt-agent自身提示；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 87 | [SAGE: Stochastic Prompt Optimization via Agent-Guided Exploration](https://arxiv.org/abs/2606.18902) | 背景参考 | 目录／综述初筛 | SAGE随机prompt搜索；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 88 | [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651) | 背景参考 | 目录／综述初筛 | 单次输出自纠正Self-Refine；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 89 | [Chain of Hindsight Aligns Language Models with Feedback](https://arxiv.org/abs/2302.02676) | 范围排除 | 目录／综述初筛 | Chain of Hindsight通过带反馈序列微调；不作为全流程无训练方法。 |
| 90 | [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) | 方法相关 | 目录／综述初筛 | 跨重试保留语言反思的基础方法；本轮以新方法原文中的同模型对照检验其效率，未重新精读全部原文。 |
| 91 | [Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate](https://arxiv.org/abs/2305.19118) | 背景参考 | 目录／综述初筛 | 多agent辩论/推理；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 92 | [Self-Improving Customer Review Response Generation Based on LLMs](https://arxiv.org/abs/2405.03845) | 背景参考 | 目录／综述初筛 | 客户回复质量优化；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 93 | [Prompt Optimization with Human Feedback](https://arxiv.org/abs/2405.17346) | 背景参考 | 目录／综述初筛 | 人类反馈prompt优化；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 94 | [Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs](https://arxiv.org/abs/2406.11695) | 背景参考 | 目录／综述初筛 | MIPRO指令与示例优化；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 95 | [CriSPO: Multi-Aspect Critique-Suggestion-guided Automatic Prompt Optimization for Text Generation](https://arxiv.org/abs/2410.02748) | 背景参考 | 目录／综述初筛 | 多维文字批评；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 96 | [Boosting Private Domain Understanding of Efficient MLLMs: A Tuning-free, Adaptive, Universal Prompt Optimization Framework](https://arxiv.org/abs/2412.19684) | 背景参考 | 目录／综述初筛 | 多模态私域理解；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 97 | [GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning](https://arxiv.org/abs/2507.19457) | 方法相关 | 深读（方法与实验） | GEPA深读；反思轨迹优化提示，样本效率和prompt长度不等于任务端到端加速。 |
| 98 | [FORGE: Self-Evolving Agent Memory With No Weight Updates via Population Broadcast](https://arxiv.org/abs/2605.16233) | 方法相关 | 深读（方法与实验） | FORGE深读；群体广播文字记忆；省40%是Rules相对Examples的学习加评估tokens，不是静态baseline。 |
| 99 | [EvoPrompt: Connecting LLMs with Evolutionary Algorithms Yields Powerful Prompt Optimizers](https://arxiv.org/abs/2309.08532) | 背景参考 | 目录／综述初筛 | EvoPrompt进化搜索；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 100 | [WizardLM: Empowering large pre-trained language models to follow complex instructions](https://arxiv.org/abs/2304.12244) | 范围排除 | 目录／综述初筛 | WizardLM的Evol-Instruct生成数据用于模型微调；提示演化不代表整套方案不训练。 |
| 101 | [Tournament of Prompts: Evolving LLM Instructions Through Structured Debates and Elo Ratings](https://arxiv.org/abs/2506.00178v2) | 背景参考 | 目录／综述初筛 | prompt tournament；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 102 | [Promptbreeder: Self-Referential Self-Improvement Via Prompt Evolution](https://arxiv.org/abs/2309.16797) | 背景参考 | 目录／综述初筛 | Promptbreeder任务与变异提示共同演化；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 103 | [DelvePO: Direction-Guided Self-Evolving Framework for Flexible Prompt Optimization](https://arxiv.org/abs/2510.18257) | 背景参考 | 目录／综述初筛 | DelvePO方向引导搜索；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 104 | [How to Auto-optimize Prompts for Domain Tasks? Adaptive Prompting and Reasoning through Evolutionary Domain Knowledge Adaptation](https://arxiv.org/abs/2510.21148) | 背景参考 | 目录／综述初筛 | 领域知识prompt适应；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 105 | [Automatic Prompt Optimization with "Gradient Descent" and Beam Search](https://arxiv.org/abs/2305.03495) | 背景参考 | 目录／综述初筛 | ProTeGi文字批评+beam search；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 106 | [How to Correctly do Semantic Backpropagation on Language-based Agentic Systems](https://arxiv.org/abs/2412.03624) | 背景参考 | 目录／综述初筛 | 语义反传与LLM-AutoDiff；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 107 | [Trace is the Next AutoDiff: Generative Optimization with Rich Feedback, Execution Traces, and LLMs](https://arxiv.org/abs/2406.16218) | 方法相关 | 深读（方法与实验） | Trace深读；可改prompt/代码，表2分钟数包括优化验证测试；不是部署延迟。 |
| 108 | [TextGrad: Automatic "Differentiation" via Text](https://arxiv.org/abs/2406.07496) | 方法相关 | 深读（方法与实验） | TextGrad原始方法与Nature发表信息核查；文字批评沿图分配，非数值导数；能力优化参考。 |
| 109 | [metaTextGrad: Automatically optimizing language model optimizers](https://arxiv.org/abs/2505.18524) | 背景参考 | 目录／综述初筛 | 优化TextGrad的优化器；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 110 | [MAPGD: Multi-Agent Prompt Gradient Descent for Collaborative Prompt Optimization](https://openreview.net/pdf?id=FywYwwH5z9) | 背景参考 | 目录／综述初筛 | 多agent prompt梯度；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 111 | [Scaling Textual Gradients via Sampling-Based Momentum](https://arxiv.org/abs/2506.00400) | 背景参考 | 目录／综述初筛 | 文字梯度momentum；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 112 | [Pick Your Textual Gradients](https://openreview.net/pdf?id=ydTwv5D536) | 背景参考 | 目录／综述初筛 | 文字梯度选择；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 113 | [SkillOpt: Executive Strategy for Self-Evolving Agent Skills](https://arxiv.org/abs/2605.23904) | 方法相关 | 深读（方法与实验） | SkillOpt深读；修改自然语言skill，离线优化和新增prompt成本显著；不应称代码编译加速。 |
| 114 | [VASO: Formally Verifiable Self-Evolving Skills for Physical AI Agents](https://arxiv.org/abs/2606.05395) | 方法相关 | 深读（方法与实验） | VASO深读；形式反例改技能契约，保证依赖未验证的命题映射；优化效率非执行加速。 |
| 115 | [Learning to Evolve: A Self-Improving Framework for Multi-Agent Systems via Textual Parameter Graph Optimization](https://arxiv.org/abs/2604.20714) | 背景参考 | 目录／综述初筛 | 多agent文字参数图优化；目录/综述层面保留背景，未核部署净收益，不能当作已证实加速。 |
| 116 | [Learning to Learn-at-Test-Time: Language Agents with Learnable Adaptation Policies](https://arxiv.org/abs/2604.00830) | 方法相关 | 深读（方法与实验） | 原链接v4改名Meta-TTL；纯prompt的meta-learning，Table6少调用但较Static更慢、更耗tokens。 |

## 2.2 Memory · 记忆

共 65 条目录记录。

| 目录行 ID | 题名 | 处理 | 阅读深度 | 原因 |
|---:|---|---|---|---|
| 117 | [Learning to Reason and Memorize with Self-Notes](https://arxiv.org/abs/2305.00833) | 背景参考 | 摘要／元数据筛查 | 上下文内边读边记 Self-Notes；不是历史行动经验部署加速，未用摘要效果作净效率判断。 |
| 118 | [ExpeL: LLM Agents Are Experiential Learners](https://arxiv.org/abs/2308.10144) | 方法相关 | 深读（方法与实验；表图已视觉核验） | 成功/失败轨迹蒸馏和示例检索为核心前作；原文显示动作略少但 trajectory token 明显增加，不能列为净节省。 |
| 119 | [A Human-Inspired Reading Agent with Gist Memory of Very Long Contexts](https://arxiv.org/abs/2402.09727) | 背景参考 | 摘要／元数据筛查 | 长文档 gist memory 与按需回看；有上下文压缩意义，但非历史 task trajectory 或环境探索复用。 |
| 120 | [CodeAgent: Enhancing Code Generation with Tool-Integrated Agent Systems for Real-World Repo-level Coding Challenges](https://arxiv.org/abs/2401.07339) | 背景参考 | 摘要／元数据筛查 | 代码工具集成和 repo 内信息导航；目录/摘要未显示跨任务经验自我改进，作为工具使用背景。 |
| 121 | [MEMORYLLM: Towards Self-Updatable Large Language Models](https://arxiv.org/abs/2402.04624) | 范围排除 | 摘要／元数据筛查 | 原文摘要明确引入可自更新参数与 transformer 内部 latent memory；不符合冻结 API 外部记忆约束。 |
| 122 | [Agent Workflow Memory](https://arxiv.org/abs/2409.07429) | 核心证据 | 深读（方法与实验；表图已视觉核验） | 成功轨迹抽象 workflow，WebArena 步数减少；已深读方法、实验、成本和宏执行附录，净总成本未证实。 |
| 123 | [ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory](https://arxiv.org/abs/2509.25140) | 核心证据 | 深读（方法与实验；表图已视觉核验） | 成败经验减少后续交互步数；含 judge/extraction 总 token 增约4.3%，需保留成本限定。 |
| 124 | [Seeing, Listening, Remembering, and Reasoning: A Multimodal Agent with Long-Term Memory](https://arxiv.org/abs/2508.09736) | 范围排除 | 摘要／元数据筛查 | 摘要明确 M3-Agent 经 reinforcement learning 训练；完整方法不属于无需模型训练的筛选主线。 |
| 125 | [Learning to Reason and Memorize with Self-Notes](https://arxiv.org/abs/2504.07952)；目录原题：Dynamic Cheatsheet: Test-Time Learning with Adaptive Memory | 重复记录 | 目录／标识去重；阅读见对应原记录 | 标题是 Dynamic Cheatsheet，链接却是 Self-Notes；按标题更正后与 row170 重复。 |
| 126 | [PRIME: Planning and Retrieval-Integrated Memory for Enhanced Reasoning](https://arxiv.org/abs/2509.22315) | 背景参考 | 摘要／元数据筛查 | 快慢多智能体推理和按需检索路由；摘要未建立跨任务 trajectory 复用或部署成本实证，不当核心加速证据。 |
| 127 | [Contextual Memory Reweaving in Large Language Models Using Layered Latent State Reconstruction](https://arxiv.org/abs/2502.02046) | 范围排除 | 目录／综述初筛（题名） | 目录无链接；补查 2502.02046。题目/摘要是 latent state 内部重构，不满足仅在黑盒 API 外部更新的范围；来源资格未核。 |
| 128 | [MemGen: Weaving Generative Latent Memory for Self-Evolving Agents](https://arxiv.org/abs/2509.24704) | 范围排除 | 方法核验（含所标记附录／训练边界，非全部实验审阅） | reasoner 冻结但原文 Appendix B/C 明确训练 memory weaver 与 trigger，含 SFT/GRPO；排除严格无需辅助神经训练设定。 |
| 129 | [M+: Extending MemoryLLM with Scalable Long-Term Memory](https://arxiv.org/abs/2502.00592) | 范围排除 | 摘要／元数据筛查 | 摘要明确 MemoryLLM latent pool 与 co-trained retriever；不属于仅外部非参数状态更新。 |
| 130 | [Seeing, Listening, Remembering, and Reasoning: A Multimodal Agent with Long-Term Memory](https://arxiv.org/abs/2508.09736) | 重复记录 | 目录／标识去重；阅读见对应原记录 | 与 row124 相同标题和 arXiv。 |
| 131 | [Thought-Retriever: Don't Just Retrieve Raw Data, Retrieve Thoughts for Memory-Augmented Agentic Systems](https://arxiv.org/abs/2604.12231) | 方法相关 | 摘要／元数据筛查 | 复用历史查询的中间 thoughts、过滤/组织再检索，与经验复用相关；本次仅摘要筛查，未证明动作或时间成本下降。 |
| 132 | [Better with Experience: Self-Evolving LLM Agents for Evidence-Grounded Health Community Notes](https://arxiv.org/abs/2606.02215) | 背景参考 | 摘要／元数据筛查 | EvoNote 由历史纠错轨迹提行动经验；摘要所报时间对比是人工 Community Notes 流程而非同 agent 有无记忆，不能当记忆加速归因。 |
| 133 | [Agon: An Autonomous Large-Scale Omnidisciplinary Research System Built on Prompt Economy](https://arxiv.org/abs/2606.24177) | 背景参考 | 方法及相关实验／成本部分核验 | 原文§2.1、Table2与§3.9核查：Prompt Economy主要衡量角色提示与交接协议维护/复用；有项目成本记录，无同任务部署加速对照。保留研究编排背景，非直接加速近邻。 |
| 134 | [XMem: Long-Term Video Object Segmentation with an Atkinson-Shiffrin Memory Model](https://arxiv.org/abs/2207.07115) | 范围排除 | 摘要／元数据筛查 | XMem 是视频目标分割模型的特征记忆；不是 LLM agent 历史轨迹学习的部署加速。 |
| 135 | [Generative Agents: Interactive Simulacra of Human Behavior](https://dl.acm.org/doi/10.1145/3586183.3606763) | 背景参考 | 目录／综述初筛（题名） | Generative Agents 为人类行为模拟的记忆/反思机制；作为背景，未核部署加速。 |
| 136 | [MemoryBank: Enhancing Large Language Models with Long-Term Memory](https://arxiv.org/abs/2305.10250) | 背景参考 | 摘要／元数据筛查 | 长期个性化对话和遗忘机制；与记住事实相关，不直接证明任务行动效率，且应用中还有对话微调。 |
| 137 | [MovieChat: From Dense Token to Sparse Memory for Long Video Understanding](https://arxiv.org/abs/2307.16449) | 范围排除 | 摘要／元数据筛查 | MovieChat 面向长视频理解的 token/特征记忆，不是目标范围的任务经验学习。 |
| 138 | [Explore, Select, Derive, and Recall: Augmenting LLM with Human-like Memory for Mobile Task Automation](https://arxiv.org/abs/2312.03003) | 核心证据 | 深读（方法与实验；表图已视觉核验） | MobileGPT 先探索应用、再复用子任务和动作；实际测量 warm-start latency/API美元成本，需注明人工修复和冷启动条件。 |
| 139 | [Scene-Driven Multimodal Knowledge Graph Construction for Embodied AI](https://arxiv.org/abs/2311.03783) | 背景参考 | 摘要／元数据筛查 | 场景知识图谱与机器人环境知识；摘要主要是知识构建和质量，未证明学习轨迹后的部署净加速。 |
| 140 | [SCM: Enhancing Large Language Model with Self-Controlled Memory Framework](https://arxiv.org/abs/2304.13343) | 背景参考 | 摘要／元数据筛查 | SCM 用外部记忆处理长对话/书和会议摘要；非任务 workflow 学习。 |
| 141 | [Hierarchical Memory for High-Efficiency Long-Term Reasoning in LLM Agents](https://arxiv.org/abs/2507.22925) | 背景参考 | 摘要／元数据筛查 | H-MEM 的层次检索主要用于长对话/推理记忆；仅摘要筛查，不能从 high-efficiency 标题推出 agent 行动加速。 |
| 142 | [SALM: A Multi-Agent Framework for Language Model-Driven Social Network Simulation](https://arxiv.org/abs/2505.09081) | 背景参考 | 摘要／元数据筛查 | 社会网络模拟中的记忆/通信优化；目标是模拟，不是当前工具任务或环境探索，摘要 token 数不作净加速证据。 |
| 143 | [Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory](https://arxiv.org/abs/2504.19413) | 背景参考 | 摘要／元数据筛查 | Mem0 可作为对话上下文压缩/检索成本背景；已核 ECAI2025 正式录用，未在本分支深读效率实验，不引用宣传比例。 |
| 144 | [G-Memory: Tracing Hierarchical Memory for Multi-Agent Systems](https://arxiv.org/abs/2506.07398) | 方法相关 | 方法核验（含所标记附录／训练边界，非全部实验审阅） | 已深读正式 NeurIPS2025 方法和成本实验；多智能体经验图改善质量/成本权衡，但相对无记忆仍增加 token。 |
| 145 | [Zep: A Temporal Knowledge Graph Architecture for Agent Memory](https://arxiv.org/abs/2501.13956) | 背景参考 | 摘要／元数据筛查 | Zep 为对话事实的时序知识图谱；普通公司预印本资格未满足项目核心来源门槛，留背景不支撑核心效果。 |
| 146 | [SGMem: Sentence Graph Memory for Long-Term Conversational Agents](https://arxiv.org/abs/2509.21212) | 背景参考 | 摘要／元数据筛查 | SGMem 面向长期会话句子图检索；不是 task strategy/action trajectory 复用，摘要初筛。 |
| 147 | [CausalRAG: Integrating Causal Graphs into Retrieval-Augmented Generation](https://arxiv.org/abs/2503.19878) | 背景参考 | 摘要／元数据筛查 | CausalRAG 主要是外部知识的因果图检索；非 agent 执行轨迹自我改进，摘要初筛。 |
| 148 | [GraphVideoAgent: Enhancing Long-form Video Understanding with Entity Relation Graphs](https://dl.acm.org/doi/abs/10.1145/3746027.3755537) | 背景参考 | 目录／综述初筛（题名） | GraphVideoAgent 为长视频实体关系推理；目录级排为背景，未读付费 ACM 全文。 |
| 149 | [Decentralizing AI Memory: SHIMI, a Semantic Hierarchical Memory Index for Scalable Agent Reasoning](https://arxiv.org/abs/2504.06135) | 待核 | 摘要／元数据筛查 | SHIMI 去中心化语义索引可能与检索成本相关，但来源资格及 task trajectory 成本证据未核，不以摘要判断性能。 |
| 150 | [From Knowledge to Noise: CTIM-Rover and the Pitfalls of Episodic Memory in Software Engineering Agents](https://arxiv.org/abs/2505.23422v1) | 核心证据 | 深读（方法与实验；表图已视觉核验） | 直接研究代码仓库经验记忆，45样本实验无提升/退化；是重要负结果，需保留样本限制。 |
| 151 | [In Prospect and Retrospect: Reflective Memory Management for Long-term Personalized Dialogue Agents](https://arxiv.org/abs/2503.08026) | 背景参考 | 摘要／元数据筛查 | RMM 为长期个性化对话，含在线 RL 式 retrieval refinement；不据名称判神经训练与否，因任务不符暂列背景。 |
| 152 | [MrSteve: Instruction-Following Agents in Minecraft with What-Where-When Memory](https://arxiv.org/abs/2411.06736v5) | 方法相关 | 方法核验（含所标记附录／训练边界，非全部实验审阅） | PEM/访问计数探索与目标相关；方法§3.2另用 PPO/LoRA 训练 VPT-Nav，完整系统不属于零训练，只借鉴外部记忆探索组件。 |
| 153 | [EvolveMem:Self-Evolving Memory Architecture via AutoResearch for LLM Agents](https://arxiv.org/abs/2605.13941)；目录原题：EvolveMem: Self-Evolving Memory Architecture via AutoResearch for LLM Agents | 方法相关 | 摘要／元数据筛查 | EvolveMem 让 LLM 根据失败日志迭代 retrieval 配置，涉及 harness 自我改进；摘要筛查，未核成本与回本。 |
| 154 | [SAGE: A Self-Evolving Agentic Graph-Memory Engine for Structure-Aware Associative Memory](https://arxiv.org/abs/2605.12061) | 范围排除 | 摘要／元数据筛查 | 摘要明确 Graph Foundation Model reader 的训练与反馈；不是无需辅助训练的外部记忆方案。 |
| 155 | [Prism: An Evolutionary Memory Substrate for Multi-Agent Open-Ended Discovery](https://arxiv.org/abs/2604.19795) | 待核 | 方法及相关实验／成本部分核验 | 核§3.5、§5：有扣除成本的VoI检索和对话QA延迟/Savings表，非trajectory到程序技能；全生命周期Savings与记忆构造成本不清。首页机构不足以确认本仓库来源资格，继续待核，不纳主报告效果证据。 |
| 156 | [Self-Evolving Multi-Agent Systems via Decentralized Memory](https://arxiv.org/abs/2605.22721)；目录原题：DecentMem: Self-Evolving Multi-Agent Systems via Decentralized Memory | 核心证据 | 深读（方法与实验；表图已视觉核验） | DecentMem 报告较 G-Memory 少 token，但仍高于无记忆；已核方法、图与基线，是条件性多智能体效率证据。 |
| 157 | [EXG: Self-Evolving Agents with Experience Graphs](https://arxiv.org/abs/2605.17721) | 核心证据 | 深读（方法与实验；表图已视觉核验） | EXG 报告少 calls/低 LLM latency，token 依任务与基线变化；已深读协议和成本附录。 |
| 158 | [CLAG: Adaptive Memory Organization via Agent-Driven Clustering for Small Language Model Agents](https://arxiv.org/abs/2603.15421) | 背景参考 | 摘要／元数据筛查 | CLAG 局部聚类记忆缓解小模型上下文噪声，QA 验证；仅摘要，未建立复杂 agent 部署效率。 |
| 159 | [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) | 重复记录 | 目录／标识去重；阅读见对应原记录 | 与 row135 Generative Agents 相同作品，arXiv/ACM 两种链接。 |
| 160 | [SEDM: Scalable Self-Evolving Distributed Memory for Agents](https://arxiv.org/abs/2304.12244)；目录原题：WizardLM: Empowering large pre-trained language models to follow complex instructions | 范围排除 | 摘要／元数据筛查 | 标题 WizardLM 的实际工作是 instruction evolution 后训练模型；网站URL却错指SEDM。按标题归类，纠正URL2304.12244；不把SEDM数据归给WizardLM。 |
| 161 | [EvoPrompt: Connecting LLMs with Evolutionary Algorithms Yields Powerful Prompt Optimizers](https://arxiv.org/abs/2509.09498v3)；目录原题：SEDM: Scalable Self-Evolving Distributed Memory for Agents | 方法相关 | 深读（方法与实验；表图已视觉核验） | SEDM 实际为2509.09498；原链接2309.08532属于EvoPrompt。已深读A/B replay与成本表；相对无记忆更贵，仅较G-Memory省。 |
| 162 | [MemInsight: Autonomous Memory Augmentation for LLM Agents](https://arxiv.org/abs/2503.21760) | 背景参考 | 摘要／元数据筛查 | MemInsight 增强对话推荐、QA和事件摘要记忆的语义属性；背景，未验证 trajectory acceleration。 |
| 163 | [MemGen: Weaving Generative Latent Memory for Self-Evolving Agents](https://arxiv.org/abs/2509.24704) | 重复记录 | 目录／标识去重；阅读见对应原记录 | 与 row128 MemGen 相同。 |
| 164 | [A-MEM: Agentic Memory for LLM Agents](https://arxiv.org/abs/2502.12110) | 背景参考 | 深读（主报告补核：NeurIPS2025 PDF §§3–4，Tables1–3；问答上下文效率与完整Agent轨迹学习不同。） | A-Mem 的记忆组织/链接/更新主要验证 long-conversation QA；主agent另行核查，本分支不伪称重新精读或据摘要推速度。 |
| 165 | [G-Memory: Tracing Hierarchical Memory for Multi-Agent Systems](https://arxiv.org/abs/2506.07398) | 重复记录 | 目录／标识去重；阅读见对应原记录 | 与 row144 G-Memory 相同。 |
| 166 | [Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory](https://arxiv.org/abs/2504.19413) | 重复记录 | 目录／标识去重；阅读见对应原记录 | 与 row143 Mem0 相同。 |
| 167 | [Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG](https://arxiv.org/abs/2501.09136) | 背景参考 | 摘要／元数据筛查 | Agentic RAG 综述是二级检索入口，不作为原始实验效率证据。 |
| 168 | [Memory OS of AI Agent](https://arxiv.org/abs/2506.06326) | 背景参考 | 摘要／元数据筛查 | MemoryOS 的分层记忆用于 LoCoMo 个性化对话；不是 task workflow 学习，摘要初筛。 |
| 169 | [SCM: Enhancing Large Language Model with Self-Controlled Memory Framework](https://arxiv.org/abs/2304.13343) | 重复记录 | 目录／标识去重；阅读见对应原记录 | 与 row140 SCM 相同。 |
| 170 | [Dynamic Cheatsheet: Test-Time Learning with Adaptive Memory](https://arxiv.org/abs/2504.07952) | 方法相关 | 深读（方法与实验；表图已视觉核验） | Dynamic Cheatsheet 适合经验学习基线，但所报 AIME token 高于无记忆；方法/实验/局限已读。 |
| 171 | [MLC-Agent: Cognitive Model based on Memory-Learning Collaboration in LLM Empowered Agent Simulation Environment](https://arxiv.org/abs/2507.20215) | 背景参考 | 摘要／元数据筛查 | MLC-Agent 面向人工社会模拟与认知拟人性；非工具任务经验加速，摘要初筛。 |
| 172 | [MemInsight: Autonomous Memory Augmentation for LLM Agents](https://arxiv.org/abs/2503.21760) | 重复记录 | 目录／标识去重；阅读见对应原记录 | 与 row162 MemInsight 相同。 |
| 173 | [PBFT-Backed Semantic Voting for Multi-Agent Memory Pruning](https://arxiv.org/abs/2506.17338) | 待核 | 摘要／元数据筛查 | PBFT pruning 为多智能体分布式共享记忆治理；有 DistilBERT 模块，训练边界/来源资格/部署任务效果未核，不当核心证据。 |
| 174 | [Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models](https://arxiv.org/abs/2510.04618) | 核心证据 | 摘要／元数据筛查 | ACE 与可演化上下文直接相关；主agent负责原文证据，本分支仅登记，最终效果需以主报告为准。 |
| 175 | [MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory](https://arxiv.org/abs/2601.03192) | 方法相关 | 深读（方法与实验；表图已视觉核验） | MemRL 更新外部标量 Q，LLM 冻结符合范围；已读成本附录，同预算质量提升不等于净加速。 |
| 176 | [Scaling Self-Evolving Agents via Parametric Memory](https://arxiv.org/abs/2606.04536)；目录原题：TMEM: Scaling Self-Evolving Agents via Parametric Memory | 范围排除 | 摘要／元数据筛查 | TMEM 摘要明确在线更新 LoRA fast weights、并训练初始策略；不符合当前不训练模型约束。 |
| 177 | [MemQ: Integrating Q-Learning into Self-Evolving Memory Agents over Provenance DAGs](https://arxiv.org/abs/2605.08374) | 方法相关 | 方法及相关实验／成本部分核验 | MemQ 的标量 Q/TD credit 沿记忆来源DAG传播，与效用检索相关；已看方法/实验协议但未深核成本，不能把学习曲线提升作部署速度。 |
| 178 | [Memory Beyond Recall: A Dual-Process Cognitive Memory System for Self-Evolving LLM Agents](https://arxiv.org/abs/2606.09483) | 背景参考 | 方法及相关实验／成本部分核验 | DCPM 已读方法/实验，主要是长期对话事实、异步抽象与检索；无任务trajectory执行加速对照。 |
| 179 | [AEL: Evolving Agent Harness in Open-Ended Environments](https://arxiv.org/abs/2604.21725)；目录原题：AEL: Agent Evolving Learning for Open-Ended Environments | 方法相关 | 摘要／元数据筛查 | AEL 用 Thompson Sampling 选检索策略、LLM reflection 扩展策略池；harness适应相关，当前仅摘要和版本核对，无效率结论。 |
| 180 | [Metis: Bridging Text and Code Memory for Self-Evolving Agents](https://arxiv.org/abs/2606.24151) | 核心证据 | 深读（方法与实验；表图已视觉核验） | Metis 反复复用文本经验后编译工具，AppWorld executor tokens/turns下降；已深读所有关键方法、表格、消融，建设总成本不完整。 |
| 181 | [Mem$^2$Evolve: Towards Self-Evolving Agents via Co-Evolutionary Capability Expansion and Experience Distillation](https://arxiv.org/abs/2604.10923)；目录原题：Mem^2Evolve: Towards Self-Evolving Agents via Co-Evolutionary Capability Expansion and Experience Distillation | 方法相关 | 方法及相关实验／成本部分核验 | Mem²Evolve 工具资产和经验共同演化；已读方法/实验协议，效率主要是工具创建修复次数，不能视为完整任务延迟下降。 |

## 2.3 Tool · 工具

共 51 条目录记录。

| 目录行 ID | 题名 | 处理 | 阅读深度 | 原因 |
|---:|---|---|---|---|
| 182 | [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291) | 方法相关 | 深读（方法与实验） | 冻结模型的探索—成功轨迹—可执行技能循环；15.3×指 prompting iterations，不是墙钟时间；对探索基线重要。 |
| 183 | [ToolNet: Connecting Large Language Models with Massive Tools via Tool Graph](https://arxiv.org/abs/2403.00839) | 核心证据 | 深读（方法与实验） | 工具图限制每步工具描述/候选范围，有 token 消耗比较；经验更新图边，但不是 GUI 技能编译；使用已有受训检索器，未见本方法新训 LLM。 |
| 184 | [AgentOrchestra: Orchestrating Hierarchical Multi-Agent Intelligence with the Tool-Environment-Agent(TEA) Protocol](https://arxiv.org/abs/2506.12508) | 背景参考 | 目录／综述初筛 | 目录初筛：TEA 协议与分层多智能体编排，可能改善工具组织；未全文核实历史学习及净执行成本，不能据此称加速证据。 |
| 185 | [MetaAgent: Toward Self-Evolving Agent via Tool Meta-Learning](https://arxiv.org/abs/2508.00271) | 方法相关 | 方法核验（含所标记附录／训练边界，非全部实验审阅） | 原文 §2.2 冻结权重，通过工具求助与经验证的反思进入知识库；已核方法，未核执行成本实验。 |
| 186 | [OrchDAG: Complex Tool Orchestration in Multi-Turn Interactions with Plan DAGs](https://arxiv.org/abs/2510.24663) | 范围排除 | 方法及相关实验／成本部分核验 | 原文§3.2/4.2确认对Qwen2.5做GRPO，奖励为图编辑距离；主表评估DAG预测正确率。排除于全流程固定权重范围，无持久技能免训练部署降本证据。 |
| 187 | [AutoTIR: Autonomous Tools Integrated Reasoning via Reinforcement Learning](https://arxiv.org/abs/2507.21836) | 范围排除 | 目录／综述初筛（题名） | 标题明确通过强化学习进行工具集成推理；严格不训练范围先排除，未全文审阅全部推理消融。 |
| 188 | [MCP-Flow: Facilitating LLM Agents to Master Real-World, Diverse and Scaling MCP Tools](https://arxiv.org/abs/2510.24284) | 待核 | 目录／综述初筛 | 目录中 MCP 工具掌握框架；训练依赖与持久经验积累未核，不将其当成参数外加速证据。 |
| 189 | [In-the-Flow Agentic System Optimization for Effective Planning and Tool Use](https://arxiv.org/abs/2510.05592) | 范围排除 | 方法核验（含所标记附录／训练边界，非全部实验审阅） | AgentFlow 原文训练 planner，Flow-GRPO；附录有 8×A100 训练配置，其他组件冻结不使整体成为 training-free。 |
| 190 | [MassTool: A Multi-Task Search-Based Tool Retrieval Framework for Large Language Models](https://arxiv.org/abs/2507.00487) | 待核 | 目录／综述初筛（题名） | 多任务工具检索可能降低工具上下文成本；未核检索器训练和历史学习机制。 |
| 191 | [AgentOrchestra: Orchestrating Multi-Agent Intelligence with the Tool-Environment-Agent(TEA) Protocol](https://arxiv.org/abs/2506.12508) | 重复记录 | 目录／标识去重；阅读见对应原记录 | 同一 arXiv ID，重复 row 184；不重复计文献。 |
| 192 | [Iterative Tool Usage Exploration for Multimodal Agents via Step-wise Preference Tuning](https://arxiv.org/abs/2504.21561) | 范围排除 | 目录／综述初筛（题名） | 标题明确 step-wise preference tuning；超出严格无模型训练范围，未全文核全部消融。 |
| 193 | [Tool-Star: Empowering LLM-Brained Multi-Tool Reasoner via Reinforcement Learning](https://arxiv.org/abs/2505.16410) | 范围排除 | 目录／综述初筛（题名） | 标题明确 reinforcement learning；超出严格无模型训练范围。 |
| 194 | [MCP-Zero: Active Tool Discovery for Autonomous LLM Agents](https://arxiv.org/abs/2506.01056v4) | 背景参考 | 方法核验（含所标记附录／训练边界，非全部实验审阅） | 主动工具发现/逐级检索是工具上下文选择，未核为跨任务经验学习；不能把工具描述压缩直接等同端到端加速。 |
| 195 | [AskToAct: Enhancing LLMs Tool Use via Self-Correcting Clarification](https://arxiv.org/abs/2503.01940) | 待核 | 目录／综述初筛（题名） | 澄清和自纠错可能节约失败调用，也可能增加交互；未核方法/成本，不据标题判断训练自由。 |
| 196 | [MemTool: Optimizing Short-Term Memory Management for Dynamic Tool Calling in LLM Agent Multi-Turn Conversations](https://arxiv.org/abs/2507.21428) | 背景参考 | 深读（方法与实验） | 原文聚焦会话内工具增删和短期记忆容量管理；与持久历史轨迹学技能不同，未见完整墙钟/账单证据。 |
| 197 | [Tool-Planner: Task Planning with Clusters across Multiple Tools](https://arxiv.org/abs/2406.03807) | 背景参考 | 目录／综述初筛 | 工具聚类规划属于工具选择的相邻方法；未深读，不把其当作自进化或经验复用的实证。 |
| 198 | [Tool-to-Agent Retrieval: Bridging Tools and Agents for Scalable LLM Multi-Agent Systems](https://arxiv.org/abs/2511.01854) | 待核 | 目录／综述初筛（题名） | 工具到 agent 检索；训练依赖与跨任务经验、加速口径待核。 |
| 199 | [ToolGen: Unified Tool Retrieval and Calling via Generation](https://arxiv.org/abs/2410.03439) | 待核 | 目录／综述初筛（题名） | 生成式工具检索/调用，可能需要模型适配；未核原文，不纳入严格冻结权重证据。 |
| 200 | [ToolACE-R: Model-aware Iterative Training and Adaptive Refinement for Tool Learning](https://arxiv.org/abs/2504.01400) | 范围排除 | 目录／综述初筛（题名） | 标题明确 iterative training；超出严格无模型训练范围。 |
| 201 | [DeepAgent: A General Reasoning Agent with Scalable Toolsets](https://arxiv.org/abs/2510.21618) | 待核 | 目录／综述初筛 | 通用 reasoning agent/可扩展工具集；是否训练、是否有持久学习和全成本比较待原文核。 |
| 202 | [DeepEyesV2: Toward Agentic Multimodal Model](https://arxiv.org/abs/2511.05271) | 待核 | 目录／综述初筛（题名） | agentic multimodal model；未核训练依赖，不纳入冻结模型结论。 |
| 203 | [In-the-Flow Agentic System Optimization for Effective Planning and Tool Use](https://arxiv.org/abs/2510.05592) | 重复记录 | 目录／标识去重；阅读见对应原记录 | 同一 arXiv ID，重复 row 189；不重复计文献。 |
| 204 | [GenericAgent: A Token-Efficient Self-Evolving LLM Agent via Contextual Information Density Maximization](https://arxiv.org/abs/2604.17091) | 核心证据 | 深读（方法与实验） | 冻结模型的分层 SOP/代码记忆；有九轮同族任务时间/token/call 下降，但评测小、人工整理影响、非严格持出泛化。 |
| 205 | [ANDES: Agent Native Data Evolving Synthesis Tool for Autonomous Instruction Alignment](https://arxiv.org/abs/2606.01279) | 范围排除 | 目录／综述初筛（题名） | 标题为数据演化合成及 instruction alignment；主要产物面向模型对齐训练，非本次冻结模型执行加速。 |
| 206 | [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291) | 重复记录 | 目录／标识去重；阅读见对应原记录 | 同一 arXiv ID，重复 row 182；不重复计文献。 |
| 207 | [STELLA: Self-Evolving LLM Agent for Biomedical Research](https://arxiv.org/abs/2507.02004) | 方法相关 | 目录／综述初筛 | 生物医学 self-evolving 工具能力相邻；当前只有目录/综述定位，未核原文成本，不承担加速结论。 |
| 208 | [SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills](https://arxiv.org/abs/2504.07079) | 方法相关 | 深读（方法与实验） | 自主探索网站、从成功轨迹生成/测试 Playwright 技能；强探索最近邻，但主实验只有成功率，无秒/美元净收益。 |
| 209 | [PyVision: Agentic Vision with Dynamic Tooling](https://arxiv.org/abs/2507.07998) | 背景参考 | 目录／综述初筛 | 动态视觉工具生成属于同任务能力扩展；持久库学习及加速证据未核，目录级背景。 |
| 210 | [From Exploration to Mastery: Enabling LLMs to Master Tools via Self-Driven Interactions](https://arxiv.org/abs/2410.08197) | 方法相关 | 深读（方法与实验） | DRAFT 通过试调用反馈更新工具文档，模型冻结；提高任务完成/调用序列匹配，不报告净加速。 |
| 211 | [LLMLOOP: Improving LLM-Generated Code and Tests Through Automated Iterative Feedback Loops](https://ieeexplore.ieee.org/document/11185878) | 背景参考 | 目录／综述初筛（题名） | 代码/测试生成的单任务迭代反馈循环；尚无原文证明跨任务持久经验和净加速。 |
| 212 | [Helping LLMs Improve Code Generation Using Feedback from Testing and Static Analysis](https://arxiv.org/abs/2412.14841) | 背景参考 | 目录／综述初筛（题名） | 测试和静态分析反馈改善代码生成；目录级，不把单任务纠错视为跨任务自进化加速。 |
| 213 | [RewardHarness: Self-Evolving Agentic Post-Training](https://arxiv.org/abs/2605.08703) | 范围排除 | 目录／综述初筛（题名） | 标题明确 agentic post-training；严格无模型训练范围先排除。 |
| 214 | [MUSE-Autoskill: Self-Evolving Agents via Skill Creation, Memory, Management, and Evaluation](https://arxiv.org/abs/2605.27366) | 核心证据 | 深读（方法与实验） | MUSE 由成功轨迹建 skills 并生命周期维护，有构建成本/重复执行秒/token；需区分 47 覆盖子集和 75 全集、同题重跑与新实例泛化。 |
| 215 | [CODESKILL: Learning Self-Evolving Skills for Coding Agents](https://arxiv.org/abs/2605.25430) | 范围排除 | 方法核验（含所标记附录／训练边界，非全部实验审阅） | 下游 coding actor 冻结，但 skill manager 先 SFT/LoRA 后 GRPO；不满足整个方案不训练模型。 |
| 216 | [PFAgent: A Tractable and Self-Evolving Power-Flow Agent for Interactive Grid Analysis](https://arxiv.org/abs/2604.10846) | 待核 | 目录／综述初筛（题名） | 电网分析领域的 self-evolving 工具 agent；成本、任务复用及训练自由未核。 |
| 217 | [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291) | 重复记录 | 目录／标识去重；阅读见对应原记录 | 同一 arXiv ID，重复 row 182；不重复计文献。 |
| 218 | [Alita: Generalist Agent Enabling Scalable Agentic Reasoning with Minimal Predefinition and Maximal Self-Evolution](https://arxiv.org/abs/2505.20286) | 方法相关 | 深读（主报告补核：arXiv2505.20286v1 §§3–5；Table2视觉核查；工具复用质量结果不等于运行加速。） | ALITA 按需生成/封装 MCP 工具并入库；已有主线程原文核验可复用，本子任务不新增未核数字。 |
| 219 | [Large Language Models as Tool Makers](https://arxiv.org/abs/2305.17126) | 核心证据 | 深读（方法与实验） | LATM 一次强模型造工具、后续弱模型复用；明确服务成本摊销机制，但理论/模型单价口径不等于端到端实测速度。 |
| 220 | [Alita-G: Self-Evolving Generative Agent for Agent Generation](https://arxiv.org/abs/2510.23601) | 待核 | 目录／综述初筛 | 生成 agent 的自进化框架；是否减少同类任务执行成本及训练依赖待核。 |
| 221 | [LLM Agents Making Agent Tools](https://arxiv.org/abs/2502.11705) | 方法相关 | 目录／综述初筛 | LLM 制造 agent tools 与可复用程序方向近；仅目录初筛，不把尚未读的效果写作实证。 |
| 222 | [OS-Copilot: Towards Generalist Computer Agents with Self-Improvement](https://arxiv.org/abs/2402.07456) | 方法相关 | 目录／综述初筛 | OS-Copilot 的工具/操作知识积累是桌面领域近邻；当前未深读，不能列作已证实净加速。 |
| 223 | [Advanced Tool Learning and Selection System (ATLASS): A Closed-Loop Framework Using LLM](https://arxiv.org/abs/2503.10071) | 待核 | 目录／综述初筛（题名） | 闭环工具学习/选择，尚未核权重更新、学习信号和加速效果。 |
| 224 | [Code2MCP: Transforming Code Repositories into MCP Services](https://arxiv.org/abs/2509.05941) | 背景参考 | 目录／综述初筛（题名） | 代码仓库转 MCP 服务是工具封装基础设施；未核为从历史任务学习或有净加速实验。 |
| 225 | [STELLA: Self-Evolving LLM Agent for Biomedical Research](https://arxiv.org/abs/2507.02004) | 重复记录 | 目录／标识去重；阅读见对应原记录 | 同一 arXiv ID，重复 row 207；不重复计文献。 |
| 226 | [PyVision: Agentic Vision with Dynamic Tooling](https://arxiv.org/abs/2507.07998) | 重复记录 | 目录／标识去重；阅读见对应原记录 | 同一 arXiv ID，重复 row 209；不重复计文献。 |
| 227 | [AgentOrchestra: Orchestrating Multi-Agent Intelligence with the Tool-Environment-Agent(TEA) Protocol](https://arxiv.org/abs/2506.12508) | 重复记录 | 目录／标识去重；阅读见对应原记录 | 同一 arXiv ID，重复 row 184；不重复计文献。 |
| 228 | [Enhancing Open-Domain Task-Solving Capability of LLMs via Autonomous Tool Integration from GitHub](https://arxiv.org/abs/2312.17294) | 方法相关 | 目录／综述初筛 | 从 GitHub 自主整合工具属于开放世界获取能力；未全文核执行加速，不承担核心结论。 |
| 229 | [OpenSkill: Open-World Self-Evolution for LLM Agents](https://arxiv.org/abs/2606.06741) | 方法相关 | 深读（方法与实验） | OpenSkill 用外部资源构造技能与独立 proxy verifier；准确率提高但运行时间增加，是独立验证近邻而非加速正证据。 |
| 230 | [EvoDS: Self-Evolving Autonomous Data Science Agent with Skill Learning and Context Management](https://arxiv.org/abs/2606.03841) | 范围排除 | 方法及相关实验／成本部分核验 | 原文§4.4/6.1.3确认共享Qwen3-8B SFT+联合RL（4×A800）；Table2无训练消融仅质量，§6.6为RL过程上下文token。排除于全流程固定权重范围。 |
| 231 | [Autonomous Evolution of EDA Tools: Multi-Agent Self-Evolved ABC](https://arxiv.org/abs/2604.15082) | 待核 | 目录／综述初筛（题名） | EDA 工具自身进化可能优化被调用工具运行效率；未核 agent 执行成本、训练依赖与本研究直接关系。 |
| 232 | [CoEvoSkills: Self-Evolving Agent Skills via Co-Evolutionary Verification](https://arxiv.org/abs/2604.01687) | 方法相关 | 深读（方法与实验） | 冻结 generator/verifier，技能和代理测试协同演化；优化中反复用 GT pass/fail oracle，非无监督验证，未报告执行加速。 |

## 2.4 Full Scaffolding · 整体 Agent 框架

共 21 条目录记录。

| 目录行 ID | 题名 | 处理 | 阅读深度 | 原因 |
|---:|---|---|---|---|
| 233 | [Language Agents as Optimizable Graphs](https://arxiv.org/abs/2402.16823) | 方法相关 | 方法／范围筛读：PDF首页/方法结构筛读；PMLR正式出版元数据 | 把节点 prompt 和图连接当可优化对象；非部署加速主证据。图结构参数优化不等于训练底层 LLM。 |
| 234 | [Self-Taught Optimizer (STOP): Recursively Self-Improving Code Generation](https://arxiv.org/abs/2310.02304) | 方法相关 | 方法／范围筛读：PDF首页/算法筛读；未审全实验 | 自我改写程序优化器；固定LM调用、utility选择。适合作为递归改进概念背景，未在本轮核端到端Agent加速。 |
| 235 | [Automated Design of Agentic Systems](https://arxiv.org/abs/2408.08435) | 方法相关 | 方法／范围筛读：PDF首页/主方法筛读；正式会议元数据 | Meta Agent Search搜索可执行agent程序；与自动改harness重合；本站标NeurIPS不准，正式为ICLR 2025。 |
| 236 | [Symbolic Learning Enables Self-Evolving Agents](https://arxiv.org/abs/2406.18532) | 方法相关 | 摘要／元数据筛查：arXiv v1首页；期刊元数据与作者机构；未精读新版实验 | 符号梯度更新prompt/tools/pipeline，非LLM参数训练；本轮只做机制背景，不引用效果数值。 |
| 237 | [Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents](https://arxiv.org/abs/2505.22954) | 方法相关 | 深读：§§3–4、App D/E成本与评测；PDF p6视觉核 | 固定FM的轨迹诊断+自改代码+archive；直接方法近邻，但主要提高成功率，作者承认改进后推理可更贵。 |
| 238 | [Huxley-Gödel Machine: Human-Level Coding Agent Development by an Approximation of the Optimal Self-Improving Machine](https://arxiv.org/abs/2510.21614) | 方法相关 | 深读：§§3–4/Table2；已视觉核表 | CMP和expand/evaluate调度降低搜索CPU小时；2.38x不是部署任务加速。 |
| 239 | [Gödel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement](https://arxiv.org/abs/2410.04444) | 方法相关 | 方法／范围筛读：PDF首页/方法筛读；ACL正式元数据 | monkey-patching修改agent逻辑，属于结构自改背景；本轮不引用效果。 |
| 240 | [AlphaEvolve: A coding agent for scientific and algorithmic discovery](https://arxiv.org/abs/2506.13131) | 背景参考 | 方法／范围筛读：PDF首页及方法/任务分类筛读 | 进化优化算法/基础设施程序；程序变快不等于trajectory驱动的agent部署变快。 |
| 241 | [ShinkaEvolve: Towards Open-Ended And Sample-Efficient Program Evolution](https://arxiv.org/abs/2509.19349) | 方法相关 | 方法／范围筛读：PDF首页/方法和任务列表筛读；正式会议元数据 | 程序进化parent采样/novelty/bandit降低样本成本；有reasoning-harness应用，主要提供外层搜索效率思路。 |
| 242 | [Live-SWE-agent: Can Software Engineering Agents Self-Evolve on the Fly?](https://arxiv.org/abs/2511.13646) | 核心证据 | 深读：§§2–4、Table1/2、弱模型消融；PDF表视觉核 | 任务进行中从轨迹识别需求并创建脚本工具；免offline evolution但非零推理开销；有每题API费用且各模型不一致。 |
| 243 | [AgentDevel: Reframing Self-Evolving LLM Agents as Release Engineering](https://arxiv.org/abs/2601.04620) | 方法相关 | 深读：§§2–3、App A；Table1/2视觉核 | implementation-blind critic→可执行诊断→单候选→pass/fail flip gate；直接关联A和C但未证明加速。 |
| 244 | [JudgeFlow: Agentic Workflow Optimization via Block Judge](https://arxiv.org/abs/2601.07477) | 方法相关 | 深读：§3及§4.4案例、优化成本；其余结果筛读 | 失败轨迹归因到逻辑block并定向编辑；报告优化sample/cost效率，不是任务部署时间证明。 |
| 245 | [RoboPhD: Self-Improving Text-to-SQL Through Autonomous Agent Evolution](https://arxiv.org/abs/2601.01126) | 范围排除 | 摘要／元数据筛查：PDF首页/摘要资格筛查，未用于结论 | PDF作者仅Independent Researchers，未核实符合当前来源资格的机构/顶会；仅保留审核记录。 |
| 246 | [Adaptive Auto-Harness: Sustained Self-Improvement for Agentic System Deployment on Open-Ended Task Streams](https://arxiv.org/abs/2606.01770) | 核心证据 | 深读：§§3–4/§6、App B/Table5及Table14定义；Table5视觉核 | 跨批轨迹→stateful multi-agent构建harness tree→任务router；有solver-only时间/token且跨域增减不同，evolver成本缺失。 |
| 247 | [MOSS: Self-Evolution through Source-Level Rewriting in Autonomous Agent Systems](https://arxiv.org/abs/2605.22794) | 方法相关 | 方法／范围筛读：PDF§§1–3及案例/限制筛读 | 生产轨迹→source patch→回放→部署rollback；固定外层pipeline，案例规模小，不能据此声称全新source-level范式。 |
| 248 | [Recursive Self-Evolving Agents via Held-Out Selection](https://arxiv.org/abs/2606.28374) | 方法相关 | 方法／范围筛读：PDF首页/方法与评估分割筛读 | 冻结policy更新strategy/skills/playbook并held-out keep-better；实质context/prompt演化，非任意源码改写；选择gate不是最终测试。 |
| 249 | [Continual Harness: Online Adaptation for Self-Improving Foundation Agents](https://arxiv.org/abs/2605.09998) | 核心证据 | 深读：§§2–4.4/§6/App A；Fig5/6视觉核；训练部分仅边界审核 | reset-free在线轨迹改prompt/subagents/skills/memory，§4.3–4.4固定模型符合；§4.5 SFT/GRPO/co-learning排除。 |
| 250 | [The Red Queen Gödel Machine: Co-Evolving Agents and Their Evaluators](https://arxiv.org/abs/2606.26294) | 方法相关 | 方法／范围筛读：PDF§3方法/实验范围筛读，未核数值结果 | 修改agent及evaluator代码，epoch内冻结judge并用GT anchor选更换；关联评估偏移，不证明部署加速。 |
| 251 | [Group-Evolving Agents: Open-Ended Self-Improvement via Experience Sharing](https://arxiv.org/abs/2602.04837) | 方法相关 | 方法／范围筛读：PDF§§3–4.3及结果条件筛读 | 跨agent分支共享代码patch/失败反思；比较等生成agent数，并在进化中换Haiku/Sonnet，非单一backbone恒定或等dollar实验。 |
| 252 | [Hyperagents](https://arxiv.org/abs/2603.19461) | 方法相关 | 方法／范围筛读：PDF§§3–5及成本/任务边界筛读 | task agent+meta agent同一可改程序，改进器本身可改；FM冻结，但robotics reward设计任务内还含下游policy训练，不能全篇称无任何训练。 |
| 253 | [Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories](https://arxiv.org/abs/2608.02276) | 范围排除 | 方法／范围筛读：PDF§§1–2/Fig2、方法边界核验 | 固定的是target，外层9B harness engineer显式SFT+GRPO；不满足全流程不训练约束。保留作边界和机制近邻。 |

## 报告与原文证据

完整学术引用集中在主报告的参考文献部分；本索引中的排除项、待核项与重复项仅保留目录审计入口。

- [主报告及参考文献](/Users/edwin/projects/agent-acceleration-research/notes/2026-09-30-self-improvement-agent-acceleration-review-zh.md:272)
- [提示优化与环境模型证据](/Users/edwin/projects/agent-acceleration-research/research/2026-09-30-survey-prompt-world-evidence.md)
- [记忆分支证据](/Users/edwin/projects/agent-acceleration-research/research/2026-09-30-survey-memory-evidence.md)
- [工具与技能分支证据](/Users/edwin/projects/agent-acceleration-research/research/2026-09-30-survey-tools-evidence.md)
- [整体 Agent 框架分支证据](/Users/edwin/projects/agent-acceleration-research/research/2026-09-30-survey-scaffold-evidence.md)
- [本索引的数据源：逐条筛查 JSON](/Users/edwin/projects/agent-acceleration-research/research/2026-09-30-survey-screening.json)

## 3 评测目录补筛

59条目录记录按主链接去重为45个不同链接，14条为额外重复；其中包含judge、平台和错链，不是45个有效且互异的benchmark。12篇选读原文的任务、方法、评价与相关附录；33条仅目录/综述初筛；14条重复仅指向原行，不增加阅读数量。所有计数均为2026-09-30快照解析（calc.）。

EV14原ClawBench链接2601.08613实际指向磁性纳米线论文。更正为[ClawBench 2604.08523v2](https://arxiv.org/pdf/2604.08523v2)，由[作者官方仓库](https://github.com/TIGER-AI-Lab/ClawBench)交叉定位；下表保留原错链用于审计。目录初筛不等于来源资格认证，待核项不用于主文的实质结论。

| 行 | 项目与原目录链接 | 判定 | 阅读深度 | 范围理由与下一步 |
|---|---|---|---|---|
| EV01 | [Mind2Web: Towards a Generalist Agent for the Web](https://arxiv.org/abs/2306.06070) | 机制 | 原文任务与协议核验 | 静态参考轨迹/动作定位；Task SR非在线终局成功。 |
| EV02 | [ManiSkill2: A Unified Benchmark for Generalizable Manipulation Skills](https://openreview.net/forum?id=b_CQDy9vrD1) | 范围外 | 目录与综述初筛 | 机器人操作；暂不纳入企业web主验证，非判定基准需训练。 |
| EV03 | [CORE-Bench: Fostering the Credibility of Published Research Through a Computational Reproducibility Agent Benchmark](https://openreview.net/forum?id=BsMMc4MEGS) | 背景 | 目录与综述初筛 | 计算科研复现；可执行评价值得后续借鉴，领域不优先。 |
| EV04 | [SWE-Bench+: Enhanced Coding Benchmark for LLMs](https://arxiv.org/abs/2410.06992) | 背景 | 目录与综述初筛 | 编码评测质量/污染相关；此轮不扩展软件修复主域。 |
| EV05 | [WebLINX: Real-World Website Navigation with Multi-Turn Dialogue](https://openreview.net/forum?id=mUSPhG4uDW) | 机制 | 原文任务与协议核验 | 多轮静态示范；替代路径不可评，检索组件加速不可冒充部署收益。 |
| EV06 | [GAIA: A Benchmark for General AI Assistants](https://openreview.net/forum?id=fibxvahvs3) | 背景 | 目录与综述初筛 | 通用助手任务；不是专为重复工作流/环境规则设计。 |
| EV07 | [MINT: Evaluating LLMs in Multi-Turn Interaction with Tools and Language Feedback](https://openreview.net/forum?id=jp3gWrMuIZ) | 机制 | 原文任务与协议核验 | 反馈使用能力与每轮预算；原协议每个k从头开始，非持续学习曲线。 |
| EV08 | [WorkArena: How Capable Are Web Agents at Solving Common Knowledge Work Tasks?](https://openreview.net/forum?id=BRfqYrikdo) | 核心 | 原文任务与协议核验 | ServiceNow参数化企业操作；云状态清理和反馈边界需固定。 |
| EV09 | [AgentGym: Evolving Large Language Model-Based Agents across Diverse Environments](https://arxiv.org/abs/2406.04151) | 机制 | 目录与综述初筛 | 可作多环境接口资源；AgentEvol训练法与环境可用性须分开核。 |
| EV10 | [GitTaskBench: A Benchmark for Code Agents Solving Real-World Tasks Through Code Repository Leveraging](https://arxiv.org/abs/2508.18993) | 背景 | 目录与综述初筛 | 仓库复用代码任务；暂不用于企业web速度推断，资格需另核。 |
| EV11 | [SafeAgentBench: A Benchmark for Safe Task Planning of Embodied LLM Agents](https://arxiv.org/abs/2412.13178) | 范围外 | 目录与综述初筛 | 具身安全任务；安全维度可参考，动作成本不直接可比。 |
| EV12 | [DrunkAgent: Stealthy Memory Corruption in LLM-Powered Recommender Agents](https://arxiv.org/abs/2503.23804) | 机制 | 目录与综述初筛 | 记忆污染/攻击可启发回归测试；未读原文，不引用攻击数字。 |
| EV13 | [ST-WebAgentBench: A Benchmark for Evaluating Safety and Trustworthiness in Web Agents](https://openreview.net/forum?id=MuCDzH0ctf) | 核心 | 原文任务与协议核验 | 终局成功+轨迹规则合规；附加压力测试，不单独判加速。 |
| EV14 | [ClawBench: A Benchmark for Evaluating AI Agents on Real-World Online Tasks](https://arxiv.org/abs/2601.08613) | 核心（后期） | 原文任务与协议核验 | 原目录错链；更正2604.08523v2后读原文。真实网站、客户端重置非服务器恢复。 |
| EV15 | [Agent-as-a-Judge: Evaluate Agents with Agents](https://arxiv.org/abs/2410.10934) | 机制 | 目录与综述初筛 | 复杂工件/轨迹的agent judge；需另核可靠性与评价成本。 |
| EV16 | [Evaluation Agent: Efficient and Promptable Evaluation Framework for Visual Generative Models](https://aclanthology.org/2025.acl-long.374/) | 范围外 | 目录与综述初筛 | 视觉生成模型评价，不是企业操作执行加速。 |
| EV17 | [EvalAgent: Discovering Implicit Evaluation Criteria from the Web](https://openreview.net/forum?id=erGpkHCybv) | 机制 | 目录与综述初筛 | 隐式评价标准发现；有助rubric设计，尚未原文核可靠性。 |
| EV18 | [Learning to Align Multi-Faceted Evaluation: A Unified and Robust Framework (ARJudge)](https://aclanthology.org/2025.findings-acl.494/) | 机制 | 目录与综述初筛 | 多维judge；如需额外训练judge则不属于全系统免训练主方案。 |
| EV19 | [VerifiAgent: A Unified Verification Agent in Language Model Reasoning](https://aclanthology.org/2025.findings-emnlp.891/) | 机制 | 目录与综述初筛 | 推理验证；可参考验证接口，不据此证明业务状态判定可靠。 |
| EV20 | [SWE-Bench+: Enhanced Coding Benchmark for LLMs](https://arxiv.org/abs/2410.06992) | 重复 | 重复，见原行；不增加阅读篇数 | 同EV04；不增加独立来源数。 |
| EV21 | [Identifying the Risks of LM Agents with an LM-Emulated Sandbox](https://openreview.net/forum?id=GEcwtMk1uA) | 机制 | 目录与综述初筛 | 模拟工具与风险评价；模拟器正确性/成本需原文另核后采用。 |
| EV22 | [GitTaskBench: A Benchmark for Code Agents Solving Real-World Tasks Through Code Repository Leveraging](https://arxiv.org/abs/2508.18993) | 重复 | 重复，见原行；不增加阅读篇数 | 同EV10；不增加独立来源数。 |
| EV23 | [MINT: Evaluating LLMs in Multi-Turn Interaction with Tools and Language Feedback](https://openreview.net/forum?id=jp3gWrMuIZ) | 重复 | 重复，见原行；不增加阅读篇数 | 同EV07；不增加独立来源数。 |
| EV24 | [TaskBench: Benchmarking Large Language Models for Task Automation](https://arxiv.org/abs/2311.18760) | 机制 | 目录与综述初筛 | 任务分解/工具规划组件；不默认等于在线可重置工作流。 |
| EV25 | [MetaTool Benchmark for Large Language Models: Deciding Whether to Use Tools and Which to Use](https://arxiv.org/abs/2310.03128) | 机制 | 目录与综述初筛 | 是否用工具/用哪个工具的决策；可做路由组件测试。 |
| EV26 | [The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models](https://openreview.net/forum?id=2GmDdhBdDk) | 机制 | 目录与综述初筛 | 函数调用评测；版本跨度大，采用前需明确具体任务接口。 |
| EV27 | [DrunkAgent: Stealthy Memory Corruption in LLM-Powered Recommender Agents](https://arxiv.org/abs/2503.23804) | 重复 | 重复，见原行；不增加阅读篇数 | 同EV12；不增加独立来源数。 |
| EV28 | [RSI-Bench: Multi-Axis Benchmark for Recursive Self-Improvement](https://github.com/sunghunkwag/rsi-bench) | 待核 | 目录与综述初筛 | 仅GitHub目录项，机构/正式出版资格未确认，隔离不用作结论。 |
| EV29 | [SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](https://openreview.net/forum?id=VTF8yNQM66) | 背景 | 目录与综述初筛 | 软件issue修复；供scaffold相关研究背景，不作web加速主基准。 |
| EV30 | [SWE-Bench+: Enhanced Coding Benchmark for LLMs](https://arxiv.org/abs/2410.06992) | 重复 | 重复，见原行；不增加阅读篇数 | 同EV04；不增加独立来源数。 |
| EV31 | [SWT-Bench: Testing and Validating Real-World Bug-Fixes with Code Agents](https://openreview.net/forum?id=9Y8zUO11EQ) | 机制 | 目录与综述初筛 | 测试/验证补丁可启发工件回归检查；本轮未读，不声称迁移已证实。 |
| EV32 | [TDD-Bench Verified: Can LLMs Generate Tests for Issues Before They Get Resolved?](https://arxiv.org/abs/2412.02883) | 机制 | 目录与综述初筛 | 问题解决前生成测试；可借鉴验证独立性，IBM研究来源待专项核版。 |
| EV33 | [LoCoBench-Agent: An Interactive Benchmark for LLM Agents in Long-Context Software Engineering](https://arxiv.org/abs/2511.13998) | 背景 | 目录与综述初筛 | 长上下文软件任务；任务形态与企业web不同。 |
| EV34 | [DevAI: Automated AI Development Benchmark](https://arxiv.org/abs/2410.10934) | 重复 | 重复，见原行；不增加阅读篇数 | 同EV15；DevAI是同篇论文的资源，不是第二篇独立论文。 |
| EV35 | [Mind2Web: Towards a Generalist Agent for the Web](https://arxiv.org/abs/2306.06070) | 重复 | 重复，见原行；不增加阅读篇数 | 同EV01；不增加独立来源数。 |
| EV36 | [WebArena: A Realistic Web Environment for Building Autonomous Agents](https://openreview.net/forum?id=oKn9c6ytLx) | 核心 | 原文任务与协议核验 | 可恢复自托管站点、功能终局评价；部分题用LLM judge。 |
| EV37 | [VisualWebArena: Evaluating Multimodal Agents on Realistic Visual Web Tasks](https://openreview.net/forum?id=RPKxrKTJbj) | 背景 | 目录与综述初筛 | 视觉web外部有效性候选；先避免把视觉grounding与经验机制混为一谈。 |
| EV38 | [WebCanvas: Benchmarking Web Agents in Online Environments](https://arxiv.org/abs/2406.12373) | 待核 | 目录与综述初筛 | live web候选，但来源资格/真实重置和指标未核；不纳结论。 |
| EV39 | [ST-WebAgentBench: A Benchmark for Evaluating Safety and Trustworthiness in Web Agents](https://openreview.net/forum?id=MuCDzH0ctf) | 重复 | 重复，见原行；不增加阅读篇数 | 同EV13；不增加独立来源数。 |
| EV40 | [clembench: Using Game Play to Evaluate Chat-Optimized Language Models as Conversational Agents](https://aclanthology.org/2023.emnlp-main.689/) | 范围外 | 目录与综述初筛 | 对话游戏协议；暂不纳企业web主验证。 |
| EV41 | [clembench-2024: A Challenging, Dynamic, Complementary, Multilingual Benchmark and Underlying Flexible Framework for LLMs as Multi-Action Agents](https://arxiv.org/abs/2405.20859) | 范围外 | 目录与综述初筛 | 对话游戏框架更新；不能与2023版本结果混用。 |
| EV42 | [GameBench: Evaluating Strategic Reasoning Abilities of LLM Agents](https://arxiv.org/abs/2406.06613) | 范围外 | 目录与综述初筛 | 战略游戏；未核正式主会资格，不作核心论据。 |
| EV43 | [LLM-Deliberation: Evaluating LLMs with Interactive Multi-Agent Negotiation Game](https://openreview.net/forum?id=eE1WHn6qlk) | 范围外 | 目录与综述初筛 | 多agent谈判；对手变化干扰与当前目标不同。 |
| EV44 | [GTBench: Uncovering the Strategic Reasoning Capabilities of LLMs via Game-Theoretic Evaluations](https://arxiv.org/abs/2402.12348) | 范围外 | 目录与综述初筛 | 博弈策略能力；不直接验证企业流程加速。 |
| EV45 | [CORE-Bench: Fostering the Credibility of Published Research Through a Computational Reproducibility Agent Benchmark](https://openreview.net/forum?id=BsMMc4MEGS) | 重复 | 重复，见原行；不增加阅读篇数 | 同EV03；不增加独立来源数。 |
| EV46 | [DiscoveryWorld: A Virtual Environment for Developing and Evaluating Automated Scientific Discovery Agents](https://openreview.net/forum?id=cDYqckEt6d) | 核心（机制） | 原文任务与协议核验 | 探索→假设→实验→规则；可区分任务完成和知识正确。 |
| EV47 | [PaperBench: Evaluating AI's Ability to Replicate AI Research](https://arxiv.org/abs/2504.01848) | 背景 | 目录与综述初筛 | OpenAI科研复现评测；长流程计费/判分可后续借鉴，此轮未展开。 |
| EV48 | [PhysGym: Benchmarking LLMs in Interactive Physics Discovery with Controlled Priors](https://openreview.net/forum?id=w8uII2qAmd) | 核心（机制） | 原文任务与协议核验 | 可控先验+主动选择实验；是函数规律发现，不能替代业务状态机。 |
| EV49 | [AstaBench: Rigorous Benchmarking of AI Agents with a Scientific Research Suite](https://openreview.net/forum?id=M7TNf5J26u) | 机制 | 原文任务与协议核验 | 标准工具、分离工具访问与模型能力、统一费用；不是持续学习现成协议。 |
| EV50 | [MLS-Bench: A Holistic and Rigorous Assessment of AI Systems on Building Better AI](https://arxiv.org/abs/2605.08678) | 背景 | 目录与综述初筛 | 构建AI系统的评测；任务可能含训练不等于执行agent必需训练，未展开。 |
| EV51 | [ManiSkill2: A Unified Benchmark for Generalizable Manipulation Skills](https://openreview.net/forum?id=b_CQDy9vrD1) | 重复 | 重复，见原行；不增加阅读篇数 | 同EV02；不增加独立来源数。 |
| EV52 | [SafeAgentBench: A Benchmark for Safe Task Planning of Embodied LLM Agents](https://arxiv.org/abs/2412.13178) | 重复 | 重复，见原行；不增加阅读篇数 | 同EV11；不增加独立来源数。 |
| EV53 | [EmbodiedBench: Comprehensive Benchmarking Multi-Modal Large Language Models for Vision-Driven Embodied Agents](https://openreview.net/forum?id=DgGF2LEBPS) | 范围外 | 目录与综述初筛 | 视觉具身操作；暂不扩大到机器人主域。 |
| EV54 | [OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments](https://arxiv.org/abs/2404.07972) | 核心（后期） | 原文任务与协议核验 | 真实OS任务与VM快照；UI/环境运行噪声和远端状态另控制。 |
| EV55 | [AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents](https://aclanthology.org/2024.acl-long.850/) | 核心 | 原文任务与协议核验 | API跨应用任务，可复位DB+时间，终局含额外改动检查。 |
| EV56 | [Identifying the Risks of LM Agents with an LM-Emulated Sandbox](https://openreview.net/forum?id=GEcwtMk1uA) | 重复 | 重复，见原行；不增加阅读篇数 | 同EV21；不增加独立来源数。 |
| EV57 | [MetaTool Benchmark for Large Language Models: Deciding Whether to Use Tools and Which to Use](https://arxiv.org/abs/2310.03128) | 重复 | 重复，见原行；不增加阅读篇数 | 同EV25；不增加独立来源数。 |
| EV58 | [Windows Agent Arena: Evaluating Multi-Modal OS Agents at Scale](https://openreview.net/forum?id=W9s817KqYf) | 背景 | 目录与综述初筛 | Windows外部有效性候选；先用OSWorld核机制，未读原文不承诺重置能力。 |
| EV59 | [The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models](https://openreview.net/forum?id=2GmDdhBdDk) | 重复 | 重复，见原行；不增加阅读篇数 | 同EV26；不增加独立来源数。 |

具体原文位置、版本、反馈/重置协议与完整参考文献见[评测补核](2026-09-30-survey-revision-evaluation.md)。主报告新增参考文献[42]–[53]与这12篇原文对应。
