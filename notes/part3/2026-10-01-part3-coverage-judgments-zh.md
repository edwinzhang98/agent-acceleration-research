# 第三部分 slides：逐篇“做到什么程度”判定（初判）

2026-10-01 · Claude Code 会话 · 数据来源：[两方向文献文档](2026-10-01-two-directions-literature-zh.md) §6 附表（102 行，一行一项工作）。本文件是 [合并大纲](2026-10-01-part3-standalone-slides-outline-v3-zh.md) 两张总表后三列的依据。

**口径（calc.，本会话按附表单元格判定，未回读全文；做页前对代表工作和存疑项逐篇复核）：**

- **执行的时间或费用**：是 = 报告了用上学到的东西之后，执行任务的实测秒数或美元；部分 = 只有 token、步数、调用数或作者估计；否 = 都没有。
- **学习投入**：是 = 报告了学习、构建、优化或维护的实测量（token、美元、时间、算力或 rollout 数之一）；部分 = 只有作者估计、迭代次数，或明确漏掉一部分；否 = 未报告。
- **没见过的任务**：是 = 在没有参与学习或挑选的任务上测；部分 = 在线任务流（边做边学）、同一流程换参数，或划分没交代清；否 = 同题重试、逐题修改或同一批任务重跑。
- 分类沿用附表第一列；附表后段自由写法的类别按 [合并大纲](2026-10-01-part3-standalone-slides-outline-v3-zh.md) §4 的映射归入；跨类工作在每个所属类别各计一次。

| # | 工作 | 发表情况 | 所属类别 | 执行时间/费用 | 学习投入 | 没见过的任务 | 附表行 |
|---|---|---|---|---|---|---|---|
| 0 | Reflexion | NeurIPS 2023 | 提示与上下文 | 否 | 否 | 否 | L478 |
| 1 | Self-Refine | NeurIPS 2023 | 提示与上下文 | 否 | 否 | 否 | L479 |
| 2 | TextGrad | Nature 2025；正式题名 *Optimizing generative AI by backpropagating language model feedback* | 提示与上下文 | 否 | 部分 | 部分 | L480 |
| 3 | MIPRO | EMNLP 2024 | 提示与上下文 | 否 | 部分 | 是 | L481 |
| 4 | ProTeGi | EMNLP 2023 | 提示与上下文 | 否 | 部分 | 部分 | L482 |
| 5 | Semantic Backpropagation | 预印本 | 提示与上下文 | 否 | 部分 | 是 | L483 |
| 6 | Trace / OptoPrime | NeurIPS 2024 | 提示与上下文；整体框架 | 否 | 是 | 是 | L484 |
| 7 | PROMST | EMNLP 2024 | 提示与上下文 | 否 | 否 | 部分 | L485 |
| 8 | Dynamic Cheatsheet | EACL 2026 | 提示与上下文；经验记忆 | 部分 | 否 | 部分 | L486 |
| 9 | GPTSwarm | ICML 2024 主会 | 提示与上下文；整体框架 | 是 | 是 | 部分 | L487 |
| 10 | AvaTaR | NeurIPS 2024 | 提示与上下文 | 否 | 否 | 是 | L488 |
| 11 | DSPy | ICLR 2024 | 提示与上下文 | 否 | 部分 | 部分 | L489 |
| 12 | GEPA | ICLR 2026 | 提示与上下文 | 否 | 是 | 是 | L490 |
| 13 | ACE | ICLR 2026 | 提示与上下文；经验记忆 | 部分 | 是 | 是 | L491 |
| 14 | Agent Workflow Memory（AWM） | ICML 2025 | 经验记忆 | 部分 | 是 | 是 | L492 |
| 15 | ExpeL | AAAI 2024 | 经验记忆 | 否 | 否 | 是 | L493 |
| 16 | MemRL | 预印本 | 经验记忆 | 部分 | 部分 | 是 | L494 |
| 17 | MemQ | 预印本 | 经验记忆 | 否 | 否 | 是 | L495 |
| 18 | AEL | EMNLP 2026 Findings 待刊 | 整体框架；经验记忆 | 否 | 部分 | 部分 | L496 |
| 19 | Metis | 预印本 | 技能与工具；经验记忆；文字说明、事实与前提；按最终状态判分的环境 | 部分 | 否 | 是 | L497 |
| 20 | Mem²Evolve | ACL 2026 | 技能与工具；经验记忆 | 部分 | 否 | 部分 | L498 |
| 21 | FORGE | ACM CAIS 2026 | 经验记忆 | 否 | 是 | 部分 | L499 |
| 22 | G-Memory | NeurIPS 2025 | 经验记忆 | 部分 | 否 | 部分 | L500 |
| 23 | CTIM-Rover | ACL 2025 REALM workshop | 经验记忆；文字说明、事实与前提；页面与地点结构 | 部分 | 否 | 是 | L501 |
| 24 | EvolveMem | 预印本 | 整体框架；经验记忆 | 部分 | 是 | 部分 | L502 |
| 25 | DecentMem | 预印本 | 经验记忆 | 部分 | 否 | 部分 | L503 |
| 26 | EXG | 预印本 | 经验记忆 | 是 | 否 | 是 | L504 |
| 27 | Meta-TTL | ICML 2026 AIWILD workshop，早期题名 *Learning to Learn-at-Test-Time* | 经验记忆；文字说明、事实与前提；按最终状态判分的环境 | 是 | 否 | 是 | L505 |
| 28 | SEDM | NeurIPS 2025 SEA workshop | 整体框架；经验记忆 | 部分 | 否 | 部分 | L506 |
| 29 | Agent S | ICLR 2025 | 技能与工具；经验记忆；文字说明、事实与前提；主动探索与练习 | 否 | 否 | 部分 | L507 |
| 30 | SE-Agent | NeurIPS 2025 | 经验记忆 | 否 | 否 | 否 | L508 |
| 31 | WebCoach | ICLR 2026 MemAgents workshop | 经验记忆；文字说明、事实与前提 | 是 | 否 | 部分 | L509 |
| 32 | ReasoningBank | ICLR 2026 | 经验记忆 | 部分 | 否 | 部分 | L510 |
| 33 | ReAP | 预印本 | 经验记忆 | 部分 | 部分 | 是 | L511 |
| 34 | Memento | 预印本 | 经验记忆 | 部分 | 否 | 是 | L512 |
| 35 | MobileGPT | ACM MobiCom 2024 | 经验记忆；页面与地点结构 | 是 | 是 | 部分 | L513 |
| 36 | SkillWeaver | 预印本 | 技能与工具；主动探索与练习 | 否 | 部分 | 是 | L514 |
| 37 | Voyager | TMLR 2024；ICLR 2025 Journal Track | 技能与工具；主动探索与练习 | 部分 | 否 | 是 | L515 |
| 38 | MetaAgent | 预印本 | 技能与工具；文字说明、事实与前提 | 否 | 否 | 否 | L516 |
| 39 | SkillOpt | 预印本 | 技能与工具 | 否 | 是 | 是 | L517 |
| 40 | VASO | 预印本 | 技能与工具 | 否 | 部分 | 部分 | L518 |
| 41 | AgentOrchestra | 预印本 | 技能与工具 | 部分 | 否 | 部分 | L519 |
| 42 | GenericAgent | 预印本 | 技能与工具；整体框架；文字说明、事实与前提；主动探索与练习 | 是 | 部分 | 部分 | L520 |
| 43 | STELLA | 预印本 | 技能与工具 | 否 | 部分 | 部分 | L521 |
| 44 | DRAFT／From Exploration to Mastery | ICLR 2025 | 技能与工具；文字说明、事实与前提 | 否 | 否 | 部分 | L522 |
| 45 | CODESKILL | 预印本 | 技能与工具 | 部分 | 是 | 部分 | L523 |
| 46 | LATM | ICLR 2024 主会 | 技能与工具 | 否 | 部分 | 是 | L524 |
| 47 | Alita-G | 预印本 | 技能与工具 | 部分 | 否 | 否 | L525 |
| 48 | OS-Copilot／FRIDAY | ICLR 2024 LLMAgents workshop | 技能与工具；主动探索与练习 | 是 | 否 | 是 | L526 |
| 49 | OpenAgent | ACL 2025 主会 | 技能与工具 | 否 | 否 | 部分 | L527 |
| 50 | OpenSkill | EMNLP 2026 主会已列日程、待刊 | 技能与工具 | 是 | 是 | 部分 | L528 |
| 51 | CoEvoSkills | COLM 2026 主会 | 技能与工具 | 否 | 部分 | 部分 | L529 |
| 52 | AgentDistill | 预印本 | 技能与工具 | 部分 | 否 | 部分 | L530 |
| 53 | CRAFT | ICLR 2024 主会 | 技能与工具 | 否 | 部分 | 部分 | L531 |
| 54 | Symbolic Learning | AI Open 2025 正式期刊，非顶会等级 | 整体框架 | 否 | 否 | 部分 | L532 |
| 55 | ADAS | ICLR 2025 主会 | 整体框架 | 否 | 部分 | 是 | L533 |
| 56 | MOSS | 预印本 | 整体框架 | 否 | 部分 | 否 | L534 |
| 57 | RewardHarness | COLM 2026 主会 | 整体框架 | 否 | 部分 | 部分 | L535 |
| 58 | STOP | COLM 2024 主会 | 整体框架 | 否 | 部分 | 是 | L536 |
| 59 | Huxley-Gödel Machine / HGM | ICLR 2026 主会 | 整体框架 | 否 | 是 | 部分 | L537 |
| 60 | Gödel Agent | ACL 2025 主会 | 整体框架 | 否 | 部分 | 是 | L538 |
| 61 | JudgeFlow | 预印本 | 整体框架 | 否 | 是 | 部分 | L539 |
| 62 | Adaptive Auto-Harness | 预印本 | 整体框架 | 是 | 否 | 部分 | L540 |
| 63 | Continual Harness | 预印本 | 整体框架；页面与地点结构 | 是 | 部分 | 部分 | L541 |
| 64 | Red Queen Gödel Machine / RQGM | 预印本 | 整体框架 | 否 | 是 | 部分 | L542 |
| 65 | Group-Evolving Agents / GEA | 预印本 | 整体框架 | 否 | 部分 | 部分 | L543 |
| 66 | Hyperagents / DGM-H | 预印本 | 整体框架 | 否 | 部分 | 部分 | L544 |
| 67 | SICA | ICLR 2025 Self-Improving Foundation Models Without Human Supervision workshop | 整体框架 | 是 | 部分 | 否 | L545 |
| 68 | Harness-R1 | 预印本 | 整体框架 | 否 | 部分 | 部分 | L546 |
| 69 | AgentDevel | 预印本 | 整体框架 | 否 | 部分 | 部分 | L547 |
| 70 | Darwin Gödel Machine / DGM | ICLR 2026 主会 | 整体框架 | 否 | 部分 | 部分 | L548 |
| 71 | Live-SWE-agent | 预印本 | 整体框架 | 是 | 部分 | 部分 | L549 |
| 72 | RSEA | 预印本 | 整体框架 | 否 | 部分 | 是 | L550 |
| 73 | WMA | ICLR 2025 | 预测行动后果 | 是 | 部分 | 部分 | L551 |
| 74 | MrSteve | ICLR 2025 | 页面与地点结构 | 部分 | 部分 | 部分 | L552 |
| 75 | Curious Causality-Seeking Agents／MCG | NeurIPS 2025 | 预测行动后果 | 否 | 部分 | 是 | L553 |
| 76 | AppWorld | ACL 2024 主会 | 按最终状态判分的环境 | 部分 | 不适用 | 是 | L554 |
| 77 | Planning to Explore／CovQValue | 预印本 | 主动探索与练习 | 否 | 否 | 否 | L555 |
| 78 | SEAgent | ICML 2026 主会 | 主动探索与练习 | 否 | 部分 | 部分 | L556 |
| 79 | WorldEvolver | 预印本；Findings 声称未正式核实 | 预测行动后果 | 部分 | 是 | 部分 | L557 |
| 80 | ActionEngine | 预印本 | 技能与工具；页面与地点结构 | 是 | 部分 | 部分 | L558 |
| 81 | WALT | ICLR 2026 主会 | 技能与工具；主动探索与练习 | 部分 | 是 | 是 | L559 |
| 82 | SpeedRunner | 预印本 | 技能与工具 | 部分 | 是 | 部分 | L560 |
| 83 | ASI | COLM 2025 主会 | 技能与工具 | 部分 | 否 | 部分 | L561 |
| 84 | HarnessFix | 预印本 | 整体框架 | 否 | 是 | 部分 | L562 |
| 85 | StarHarness | 预印本 | 整体框架 | 部分 | 否 | 部分 | L563 |
| 86 | AutoDroid-V2 | ACM MobiSys 2025 | 文字说明、事实与前提 | 部分 | 部分 | 部分 | L564 |
| 87 | AppAgentX | 预印本 | 技能与工具；页面与地点结构 | 是 | 否 | 部分 | L565 |
| 88 | Growing Harness | 预印本 | 整体框架 | 是 | 否 | 部分 | L566 |
| 89 | TraceCompiler | 预印本 | 技能与工具 | 部分 | 否 | 部分 | L567 |
| 90 | EchoPath | 预印本 | 技能与工具；文字说明、事实与前提 | 是 | 是 | 否 | L568 |
| 91 | Unbrowse／Shadow APIs | 预印本 | 文字说明、事实与前提 | 是 | 是 | 部分 | L569 |
| 92 | SKILL.nb | ICML 2026 FAGEN workshop | 技能与工具；文字说明、事实与前提 | 部分 | 部分 | 部分 | L570 |
| 93 | Grounding Agent Memory | 预印本 | 经验记忆；文字说明、事实与前提 | 是 | 否 | 部分 | L571 |
| 94 | Are Online Skill and Memory Modules Always Worth Their Tokens? | EMNLP 2026 主会（日程已列） | 技能与工具；经验记忆 | 部分 | 部分 | 部分 | L572 |
| 95 | ClawTrace／CostCraft | ACM CAIS 2026 Agent Skills workshop，非归档 | 技能与工具 | 是 | 否 | 是 | L573 |
| 96 | ESPO | EMNLP 2026 Findings（日程已列） | 提示与上下文 | 否 | 是 | 是 | L574 |
| 97 | SoL-Pi | 预印本 | 整体框架 | 部分 | 否 | 部分 | L575 |
| 98 | AXIS | ACL 2025 主会 | 技能与工具；主动探索与练习 | 是 | 否 | 部分 | L576 |
| 99 | Agent JIT Compilation | ICML 2026 | 整体框架 | 是 | 否 | 部分 | L577 |
| 100 | Skim | 资格记录标EuroSys 2027 | 技能与工具；页面与地点结构 | 是 | 否 | 部分 | L578 |
| 101 | Space | EMNLP 2026 Findings | 技能与工具 | 部分 | 部分 | 部分 | L579 |

## 按类汇总

| 类别 | 篇数 | 执行时间/费用：是／部分 | 学习投入：是／部分 | 没见过的任务：是／部分 |
|---|---|---|---|---|
| 方向一·提示与上下文 | 15 | 1／2 | 5／5 | 7／6 |
| 方向一·经验记忆 | 26 | 5／15 | 5／4 | 11／14 |
| 方向一·技能与工具 | 34 | 9／14 | 6／11 | 8／23 |
| 方向一·整体框架 | 30 | 8／4 | 7／16 | 5／23 |
| 方向二·预测行动后果 | 3 | 1／1 | 1／2 | 1／2 |
| 方向二·文字说明、事实与前提 | 13 | 6／4 | 2／3 | 3／8 |
| 方向二·页面与地点结构 | 7 | 5／2 | 1／3 | 1／6 |
| 方向二·主动探索与练习 | 9 | 3／2 | 1／3 | 4／4 |
| 方向二·按最终状态判分的环境（不学习，单列） | 3 | 1／2 | 0／0 | 3／0 |
| 方向一合计（去重） | 93 | 21／28 | 19／33 | 28／57 |
| 方向二合计（去重，不含判分环境） | 29 | 14／8 | 5／10 | 8／18 |

三列都为“是”的工作：无。执行时间/费用和学习投入同时为“是”的：GPTSwarm, MobileGPT, OpenSkill, EchoPath, Unbrowse／Shadow APIs。
