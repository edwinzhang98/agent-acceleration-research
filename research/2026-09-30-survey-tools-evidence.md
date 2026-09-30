# Tool 分支：固定模型权重、历史轨迹与环境探索的加速证据

日期：2026-09-30。供主报告整合的原文证据备忘录；不是完整综述的替代品。范围为综述网站 TOOL 分支 row 182–232，共 51 条、按 arXiv ID 去重后 44 篇，逐条结果见同目录 `2026-09-30-survey-tools-screen.json`。另深读 ASI、WALT、SpeedRunner、ActionEngine 四篇直接最近邻。本文的 ST 编号是临时引用编号，不替代项目正式文献 ID。

阅读边界：核心卡片实际读取论文方法、实验及有关附录；关键表格/曲线已用 PDF 放大核对，引用的是下面注明的版本。其余目录初筛明确标记为 directory/title/survey only，未据摘要宣称其没有某种机制。最终补核后，剩余 uncertain 条目仍需后续核实，不能由“筛过目录”推出“已穷尽不存在更近研究”。题目中明确 RL、preference tuning、post-training 的条目可以先按研究范围排除；CODESKILL 和 AgentFlow 则实际检查了训练部分。正式 venue 优先；有强高校/研究实验室署名、尚未独立核实发表的工作作为预印本补充，不与正式发表证据等量齐观。

## 1. 最重要的结论

**“从历史轨迹学程序技能”与“主动探索网站后编译操作”都已经形成直接研究路线，不能再作为独立的新颖点。** 前者从 Voyager、ASI 延伸到 SpeedRunner，后者有 SkillWeaver、WALT、ActionEngine。它们共同把未来需要模型反复决定的动作，变成可调用程序或可检索的环境知识；真正改变的是模型外部系统，不是基础模型参数。

两者也不能简化为同一种 memory：

| 路线 | 被保存的对象 | 学习信号 | 代表作 | 已验证到什么程度 |
|---|---|---|---|---|
| 从轨迹归纳程序 | 多步操作函数、参数、辅助函数 | 历史成功/失败、调用栈、回放验证 | ASI、SpeedRunner、Voyager | ASI 有 Web 步数；SpeedRunner 有含学习摊销的美元；Voyager 主要是探索迭代数 |
| 主动探索工具/网站 | 工具说明、UI 操作 API、URL 参数、状态机 | 探索实际结果、调用测试、环境反馈 | DRAFT、SkillWeaver、WALT、ActionEngine | 前两者主要成功率；WALT 步数与构建成本；ActionEngine 直接报告秒和美元 |
| 生命周期技能包 | SKILL.md、脚本、资源、技能经验 | 任务结果、可选测试、跨会话记忆 | MUSE、GenericAgent | 有时间/token，但选择子集、同族重跑、人工干预等边界很重要 |
| 工具候选/上下文缩减 | 工具图、动态工具集合、检索索引 | 当前步骤/工具需求，部分有历史边权 | ToolNet、MCP-Zero、MemTool | 可减少送入模型的工具描述；不自动等于跨任务 self-evolution |
| 自造验证器 | 代理测试与技能共同更新 | 外部知识锚点，或 GT oracle pass/fail | OpenSkill、CoEvoSkills | 有质量改进；OpenSkill 实际运行更慢，CoEvoSkills 优化阶段使用 GT 反馈 |

因此 self-evolution 是**系统如何持续改变**；加速是**改变后优化什么指标**。同一 self-evolution 方法可以增加准确率而变慢。最直接的反例是 OpenSkill：同一 Opus 4.6 上平均运行时间 465.0 秒升到 845.4 秒，且尚未加构建成本。

对我们最需要避免的三个空白声明：

1. 不能说“还没人让 coding agent 分析历史日志、增删重构 skills”——SpeedRunner 已这样做，并把 sleep 学习费用摊入轨迹成本。
2. 不能说“还没人先探索环境再减少在线逐步推理”——SkillWeaver、WALT、ActionEngine 是直接先例；ActionEngine 还覆盖状态机、失败修补和模板 warm-up。
3. 不能说“只要 self-generated verifier 就实现独立验收”——OpenSkill 的 proxy 存在误判；CoEvoSkills 在优化中反复使用 GT pass/fail，不能同时充当一次性的未触碰最终验收集。

## 2. 原文深读证据卡

### ST1. SkillWeaver：自主探索网站并磨练可执行技能

**方法与冻结范围。** 给定网站状态、截图/AXTree 和当前技能库，冻结的 GPT-4o 提出短探索任务，执行后由模型依据轨迹/页面变化判断结果；把成功轨迹抽成参数化 Python/Playwright 函数，再静态检查、生成测试输入、执行/修复。技能可以调用已有技能。论文的“API”是生成的浏览器操作函数，不应误读为网站公开 REST API。每站约 160 轮探索或测试，每轮最多 10 步；这是非零的离线环境与模型开销。

**实验结果。** arXiv v1 §3、Table 1–2，PDF p7：同一 GPT-4o CodeAct+Playwright，WebArena SR 22.6%→29.8%；真实网站实验 4 站共 57 题，40.2%→56.2%。GPT-4o-mini 在 WebArena 为 9.2%→14.1%。前者相对改进按表为约 31.9%，不要将真实网站的 39.8% 误写成 WebArena。论文正文局部相对数值与表/摘要有错位，主报告宜只报原始分数。

**加速与成本边界。** 主实验未提供墙钟时间、美元、总 token 或学习成本回本曲线。它强力证明“探索→程序技能→成功率提升”可行，未证明净执行加速。不能将“程序代替多次推理”的机制推断伪装成实验测得速度。

**局限与我们的关系。** 作者分析包括技能调用选择错误、参数错误，以及探索能力受 teacher 上限制约；部分真实站点没有改善。实验对真实世界危险/副作用动作有人工限制，不证明可对生产写操作任意探索。对企业 Web，它是必须复现/比较的环境探索基线；我们可进一步测重复任务的真实成本与技能失效，但不能声称探索造技能本身新颖。[原文](https://arxiv.org/pdf/2504.07079v1)

### ST2. ASI：在线从执行轨迹诱导、回放验证程序技能

**方法与冻结范围。** Claude 3.5 Sonnet 同时作为 actor、轨迹成功判别器和 skill inducer，权重固定。执行完任务后，过滤无效动作/思考，把成功轨迹抽成函数；用修改后的轨迹前缀在原任务中强制调用新技能并继续执行，要求技能实际调用、改变状态且任务获判成功，才接纳技能。这里的 verification 包含程序执行、状态检查和模型判别，不能写成形式化正确性证明。

**实验结果。** COLM 2025 版本 §3、Table 1，PDF p5：WebArena 上同 Claude backbone，vanilla SR 32.7%、5.6 steps；文字技能 AWM 36.3%、5.9 steps；ASI 40.4%、5.0 steps。根据表计算，相对 vanilla 少 10.7% 步、相对 AWM 少 15.3% 步。主文对两种步数降幅的次序存在表述混淆，宜保留原表。论文按 WebArena 全部样本报告平均分；扩展长任务实验用 checkpoint 完成度，不能直接与二元成功率混用。

**成本与局限。** steps 是 agent 层操作，宏技能的一步内部可以含多个 UI 动作；不等于浏览器事件数，也不是秒。未完整计入在线 induction、源任务回放、judge 成本。作者的跨站迁移实验表明通用操作可迁移，但 dropdown/sidebar 等结构变化会使技能不适用。我们的判断：在可重置测试站，源任务回放是有用 baseline；在有副作用生产环境需另设验证条件。[原文](https://arxiv.org/pdf/2504.06821v2)

### ST3. WALT：把网站自身功能逆向成稳定工具

**方法与冻结范围。** ICLR 2026 camera-ready，与早期 arXiv v1 的分析内容不同。固定 GPT-5/GPT-5-mini 等模型，先探索网站可用功能，再收集不同输入的演示，把目标操作生成带输入 schema 的脚本，包含 navigation、DOM extraction、deterministic UI、必要时 agentic fallback。对可以由 URL 参数实现的搜索/排序等做 URL promotion，减少点击。工具通过预先审查的输入验证和修订；优化中关注失败率、步骤数和 agentic 步比例。

**干净消融。** §4.4、Table 2，PDF p8，在 **VisualWebArena-Classifieds** 的同样 text/self setting、同 GPT-5-mini 上：无工具 57.5% SR、8.9 steps；加入 discovered tools 61.5%、6.5 steps。完整配置还加多模态 DOM 解析和外部验证器（external verification），64.1%、7.0 steps，不可把全部提升归给自主工具学习。Online-Mind2Web 是 139 站，300 个尝试任务中排除 62 个环境问题后评 238 个；表的 SR/steps 差值与正文百分比存在小冲突，主报告优先用干净消融。

**构建成本是有报告的，但“14 次回本”应纠正。** §4.6，PDF p9：305 个工具候选，252 个验证成功（82.6%），平均每工具 1.75 次尝试、每站 1.81 个工具。按 GPT-5 价格举例，每工具构建约 $1.67，分为 proposal $0.26、demonstration $0.87、generation $0.46、testing $0.08。作者以 baseline $0.12/task 得到约 14 次使用回本。

我们的核算判断：$1.67/$0.12≈13.9 只说明构建费用等于约 14 次 baseline 全部费用，省略了工具方案在线仍有的推理/执行成本。严格净回本应是 `N >= C_build / (C_baseline − C_online_with_tools)`；当新方案在线成本为正且低于基线时，所需使用量高于该简单比值估计；若每次净节省非正，则不能靠复用回本。遇到漂移后的修补成本也应加入。故不能说 WALT 完全不报告构建成本，也不能未经修正复述 14 次为严格净成本回本。

**作者局限。** 动态 UI、A/B、CAPTCHA、复杂编辑器/上传、稀有参数与 selector 漂移；online patching 主要列为后续方向。对我们：这是“功能探索→操作编译”的最直接正式发表基线，探测目标和实现方式比普通轨迹宏更贴近企业重复工作流；但论文未证明长期漂移后的 all-in 秒/美元优势。[正式发表页](https://proceedings.iclr.cc/paper_files/paper/2026/hash/5b175f9e93873e3a10a6ce43dbb82e05-Abstract-Conference.html)

### ST4. ActionEngine：环境状态机记忆与一次规划、多步确定执行

**方法与冻结范围。** 固定 Claude Opus 4.6。离线 crawler 以黑盒浏览器探索生成 state-machine graph（SMG），描述共享 UI 模板状态、可用操作、输入/输出及状态转移；保存数据访问路径而非旧业务数据。在线模型依据 SMG 生成程序，然后编译并执行；只有需要语义处理/辅助时再调用模型。Patcher 可修复操作/知识并写回 SMG。

**结果与关键协议。** arXiv v2（2026-09-28），§5.1–5.2、Table 1，PDF p7；四个 WebArena 域共 655 题，同 Claude Opus 4.6，对照 Claude Code+Playwright MCP：成功率 82.7%→91.2%，平均延迟 87→27 秒，API cost $0.40→$0.05/task。作者称 3.2× 速度、8× 成本降低；美元由 token 用量按当时价格估算，含缓存定价，不是独立账单审计。LLM 平均调用并非所有题严格一次（部分域约 1.5–3.5 次）。

**不能略去的 warm-up。** 主实验在任务无关 crawler 后，使用每个 WebArena task template 各一个生成任务做 warm-up/patch；未用最终测试实例及具体参数，但已获得模板级任务信息。正式评测时 Patcher 关闭，每题只有单次执行。初始 SMG 的 SR 73.1%→refined 91.2%，所以主结果不能写成纯无任务先验探索即得，也不能用主实验证明在线自动维修期间仍有 3.2× 速度。

**成本。** §5.3、Table 2，PDF p9：各域 crawling $11.6–37.2、36–260 分钟；作者报告 39–101 tasks 回本。表称 one-time crawling cost，是否完整包含额外 template warm-up 成本没有清楚拆开，应列为待复算。缓存消融平均 cost $0.16→$0.05，表明 8× 效果由环境程序化和缓存共同组成，不能全归因于学习。实验还人工复核所有系统失败样本以修正参考答案格式等误判，应保持同协议复现。

**局限。** 作者列出搜索语义与真实返回不一致、含糊请求等失败。我们的判断：655 个受控题并不等于长期变化的真实企业站点；但它已经将我们的 B 路线推进到明确的秒/美元和成本摊销实验，必须正面比较而非仅当远相关背景。[原文](https://arxiv.org/pdf/2602.20502v2)

### ST5. SpeedRunner：用 coding agent 分析历史轨迹、重构程序技能，直接优化成本

**方法与冻结范围。** actor 和 skill inducer 都固定为 GPT-5.4-mini，actor reasoning=low、inducer=medium。wake 阶段跑一批 10 条轨迹；sleep 阶段 coding agent 读取原始轨迹、工具调用栈和版本化技能库，分析失败/冗余，新增、编辑或删除技能，并区分暴露给 actor 的 public 函数和内部 helper。关键点是**不依靠重新运行环境/replay 或额外验证**也能从日志改代码。它不是每条轨迹仅让 LLM 写一句反思，而是可使用代码搜索和统计的较强分析器。

**评测。** arXiv v1 §§3–5、Fig.3（PDF p6）、Appendix A/G：ScienceWorld 两个任务族、BabyAI 一个困难任务、Crafter；每环境 200 条训练 episode，每 50 条做 30 条 held-out evaluation，3 seeds。BabyAI 中作者报告约从 67% 接近 100%，单轨迹成本降到 ReAct 的约八分之一；这些是曲线/正文的近似描述，不应造出更精细的小数。Crafter 纵轴是成就进度，不是二元成功率。基线包括 ReAct、文字技能和程序技能法；ASI/Voyager 为适配到同 actor/primitive 的版本，ASI 主比较移除了 replay 验证，原样/变体分析另见附录。

**成本口径很重要。** Appendix A.3 明确统计 input、cached input、output，并将 sleep inducer 费用摊到 batch 轨迹；所以“别人没有计学习成本”不是对该文成立的 gap。图注有 output-token cost 的简写，但附录给出更完整美元核算。论文没有报告墙钟吞吐提速，最大执行时限只是预算，不能把约八分之一美元写成 8× 秒级提速。

**作者局限与关系。** 只测试有限模拟环境/模型；附录显示代码过度压缩可能损害原本很强的模型。分布变化下技能维护有实测，但不能推广为无遗忘。我们 A 路线（历史 trajectory→诊断→程序改进）与其重合极大；有价值的后续应在企业 Web 的真实日志、带副作用流程、变更/失效和含维护成本的长期表现上提出具体问题。[原文](https://arxiv.org/pdf/2608.11338v1)

### ST6. GenericAgent：分层记忆/SOP 脚本化有速度结果，但自动性边界明显

**方法。** 冻结模型，九个原子工具；四层记忆为常驻索引、事实、SOP/可执行脚本、原始 session。只在需要时展开；从执行成功的里程碑整理程序化经验，并配合输出截断、历史淘汰和 working checkpoint。学习对象为模型外部上下文和脚本。

**结果。** v1 §4.4、Table 8，PDF p21：Claude Opus 4.6，九轮新的同结构 GitHub/langchain 调研任务，第一轮 450 秒、32 tool calls、222,203 total tokens；第九轮 98 秒、5 calls、23,010 tokens。这是同族任务复用的具体正例。这里 total token 累计包含缓存创建/读，并非按不同价格加权的美元；跨轮输入也不完全相同，不能当成同一题的严格控制因果实验。

**边界。** §3.3 和局限承认部分 self-improvement logs 由人工整理，技能树合并/删除尚依赖手工；自主探索和更广自进化未完整验证。小规模/同族重跑不支持普遍长期企业成功率。我们的判断：可作现实系统设计与 feasibility 补充，证据等级低于独立大样本受控比较，不能称已完成纯自治 skills 生命周期。[原文](https://arxiv.org/pdf/2604.17091v1)

### ST7. MUSE-Autoskill：成功轨迹形成长期技能包，质量/速度需区分覆盖率

**方法。** 固定 GPT-5.5-2026-04-24 等 backbone；按需生成 SKILL.md、脚本/资源和可选测试，在 sandbox 执行，注册 catalog；每技能记录经验，后续任务读入/修补。某些 skill 没有测试文件，只有来源轨迹和运行反馈，不应概括为一律强验证。

**实验与选择效应。** 所读 arXiv v2，§4.3、Table 4：SkillsBench 94 题中 75 个共同可运行任务，每题 5 runs。Phase 1 从一个成功运行抽技能，Phase 2 在同一任务重跑；MUSE 仅为 47/75 题形成 usable skill。覆盖 47 题上的自制技能平均分 85.24% 高于人类技能 81.17%；但严格 75 全集将无技能 28 题记 0 后，自制为 53.42%，低于 human 59.67%，高于 no-skill 46.95%。不要将覆盖子集的 85.24% 当全基准成功率。

**速度和构建成本。** §4.4、Table 6，PDF p13，在同一个 47 题 covered 子集：no-skill median 579k tokens、729.3 秒、20 turns；self-skill 为 499k、434.7 秒、15 turns；生成一份技能的 median 364k tokens、156.3 秒、6 turns。作者估计相对 human-skill setting 的中位数成本约三次复用摊回 token、一次复用摊回时间。此为中位数示意，不是逐题累积全量净成本；延迟不含 SkillsBench verifier。失败探索/未覆盖题、维护与长期漂移不能由该数完整覆盖。

**作者明确的不足。** 同任务成功轨迹再利用可能高估泛化；coverage 限制；可从失败轨迹取部分有效技能；当前 transfer 和重复次数有限。因而它给我们的最佳启发是报告“生成成功覆盖率 × 覆盖题收益”，并同时核验新参数、新模板和失败轨迹利用，而不是只选成功学会的题来算速度。[原文](https://arxiv.org/pdf/2605.27366v2)

### ST8. OpenSkill：学习验证依据，提升正确率却未必加速

**方法。** 固定 Claude Opus 4.6/GPT-5.2，外部研究模块用 Gemini 2.5 Flash；只拿任务输入，主动检索文档/仓库/网页，收集知识与独立 validation anchors（参考值、不变量、格式规则）；生成 skill；隔离 session 依据这些锚点造 deterministic proxy tests，执行修订，区分知识缺失和实现错误，可再次查外部来源。target GT 保留到最终评测，不在迭代中调用。默认最多 3 轮，提交最后一版，而非用 GT 挑 best-of-N。

**结果与反例。** v1 Table 1：Claude Code/Opus4.6，no-skill 25.5%→OpenSkill 43.6%；Codex/GPT5.2 25.0%→42.1%。但 Appendix E、Table 8，PDF p19，Opus 的 no-skill mean/median runtime 为 465.0/347.6 秒，OpenSkill 为 845.4/368.2 秒，**在线均值和中位数均增加，且不含技能构建成本**。因此它是独立验证和开放世界自学习的强方法近邻，不是运行加速成功案例。

**验证器没有神奇获得真值。** §4.2 Table 3（PDF p8）把 GT reward>0 当成功，84 题分析 proxy precision 56.9%、recall 80.5%、agreement 60.7%。88.9% 是随机 15 题中 LLM 判断的 test-intent coverage（120/135），不能解读成“验证正确率 88.9%”。论文自己展示更多迭代会过拟合 proxy，外部信息质量与深层语义仍是局限。

**我们的推断。** 环境探索不只可以产技能，也可以产较独立的验证依据，这是 C 路线可借鉴部分；但应为验证成本设置预算，并用未进入生成闭环的最终判断测 false accept/false reject，不能只报通过自测的比率。[原文](https://arxiv.org/pdf/2606.06741v1)

### ST9. CoEvoSkills：技能和 surrogate tests 同时进化，但有 GT oracle 反馈

**方法核实。** 所读 arXiv v3，PDF 声称 COLM2026，本文未独立核实会议记录，按预印本补充。generator 和 verifier 权重固定，产生多文件技能包及隔离 surrogate tests；若 surrogate pass，则在新环境运行 GT oracle，仅返回 opaque pass/fail；不通过时增加测试难度，继续改 skill。Algorithm 1（PDF p5）设置最多 5 轮 GT oracle、15 次 repair，并按 oracle 分数保存最佳技能。

**结果范围。** SkillsBench 85 题、每题 5 runs，比较 Claude Code/Opus4.6、Codex/GPT5.2，并分析其他 LLM transfer；本证据卡不将其准确率与 OpenSkill 跨协议排名，因为二者学习时可用的监督不同。未见执行秒/美元节省的核心证据。

**重要边界。** “无法看到 GT 测试内容”与“没有 GT 监督”是两回事。此文确实隔离了测试实现，但优化仍利用反复 oracle 信号与 best selection；不能拿同一个 oracle 同时当优化反馈和未触碰的最终 gate。对我们有用的是 adversarial/independent verifier 设计及弱监督信号分析，而非直接加速结论。[原文](https://arxiv.org/pdf/2604.01687v3)

### ST10. DRAFT：先探索工具，把学到的环境行为写回文档

**方法。** 冻结 GPT-4o 等；Explorer 生成 diverse query 与参数实际调用工具，用 embedding 相似度鼓励覆盖；Analyzer 对照真实返回与旧文档找缺漏；Rewriter 更新描述和后续探索方向。最多 5 轮，BLEU 与语义相似度稳定后提前停止。更新的是工具文档，不是模型或工具实现。

**结果。** ICLR2025，§4、Table 1，PDF p7：GPT-4o+ReAct 的 RestTMDB CP 71.00→88.00，Spotify 28.07→70.17，ToolBench 37.00→51.00。CP 检查正确工具序列是否作为 subsequence 出现，允许多余调用，不能当“更短轨迹”。另有模型 judge 的 win rate，不能与确定验收混同。未提供包括探索文档构建的端到端美元/时间收益。

**局限与关系。** 作者发现过度迭代会引入冗余/过拟合，说明探索不是越多越好。对我们的环境探索实验，它是必要的轻量对照：只学更准确的环境说明是否已足够，额外编译程序究竟再省了多少成本。[原文](https://arxiv.org/pdf/2410.08197v2)

### ST11. LATM：强模型一次造工具、弱模型多次调用，明确的服务成本分工

**方法。** ICLR2024；固定 GPT-4 tool maker 依据少量训练样例生成通用 Python 函数，经样例验证；GPT-3.5 tool user 通过示例学习调用；工具缓存支持新请求复用，dispatcher 遇到陌生类任务启动新工具制作。并非模型自训练，也不主要依靠浏览器历史轨迹。部分请求的工具类型判定/标签仍可能依赖强模型或人工。

**结果与成本口径。** 所读 v2 §§2–3，Table 1/2/4：主要是 6 个算法/推理任务，每任务 3 个构建示例、3 个验证示例、约 240 test；展示廉价用户模型+工具的准确率可接近强模型。成本论证是 `O(n*c+C)` 对比每次强模型的 `O(n*C)`，并引用当时每千 token 模型价格；不是完整 Web 执行延迟，也非包含所有工程过程的逐任务实测账单。

**关系。** 它已清楚提出 amortize once-off tool-making 的思路，所以“离线贵一点，未来重复工作更便宜”不是新贡献。作者也指出真实反复人机交互数据/benchmark 不足。我们的工作可把抽象服务成本模型落到多步骤、有错误恢复和环境漂移的真实工作流，但必须提供可比较的质量。[原文](https://arxiv.org/pdf/2305.17126v2)

### ST12. Voyager：自主课程和程序技能库的早期范式，“更快”不是墙钟

**方法。** 固定 GPT-4-0314、GPT-3.5-turbo-0301 等。模型依据当前 Minecraft 状态、成功/失败任务提出下一个探索目标；用 Mineflayer 高级原语写 JS，结合环境反馈、解释器报错、自我评估，最多 4 次修复；成功代码进入 embedding 检索技能库，后续组合调用。课程决定学什么，技能库决定如何复用。

**结果。** 所读 arXiv v2，§3、Table 1，PDF p7；160 prompting iterations 预算、3 次实验。wooden milestone AutoGPT 92±72 次、Voyager 6±2 次，形成 15.3×；但 Voyager without skill library 也约 7±2 次，早期里程碑提速主要不能独归技能库。作者还验证新世界中复用技能解决任务。

**边界。** 横轴是 prompting iteration，不是秒；不同 iteration 内含不同模型调用/动作。API 费用、自判正确性、卡住和环境限制均影响实际可用性。对我们，自动 curriculum 是“主动探索什么才值得”的先例，但它未解决企业工作流的实际净回本/写操作验证。[原文](https://arxiv.org/pdf/2305.16291v2)

### ST13. 训练排除的必要例子：CODESKILL、AgentFlow

CODESKILL 所读 arXiv v2 §3 和训练附录：coding actor 冻结，但 Qwen3.5-4B skill manager 先 SFT/LoRA 再 GRPO，奖励由 skill 质量 rubric 与下游执行组成。因此不能只看“frozen downstream agent”便列入整体 training-free。其 prompt-only baseline 可以单独借鉴，但主方法越界。[原文](https://arxiv.org/pdf/2605.25430v2)

AgentFlow（In-the-Flow Agentic System Optimization）原文方法与 Appendix C：Flow-GRPO 训练 planner，报告 8×A100 训练；其他模块固定同样不代表整个系统不训练。这两例说明筛选轴应是“我们的系统里哪些决策模型新增了训练”，不只是 actor 有没有更新。[原文](https://arxiv.org/html/2510.05592)

## 3. 目录筛查中的相邻效率路线与未决项

ToolNet 的原文 §3–4 把大量工具组织为图，前一次工具调用决定下一次候选工具及送入模型的描述；还可以通过调用反馈调整边权。论文有 token 消耗/质量比较，是工具上下文缩减相关的正例。但其工具检索采用既有受训 BERT，不宜宣传为“没有使用任何训练得到的组件”；新方法本身没有更新 actor 参数，和用户“不在模型训练层做改进”基本兼容。其评测重点 API 选择，不是企业 GUI 操作程序库，完整图构建/评估费用未清楚与在线 token 同算。这里依据 HTML 方法/表格审阅，未将未放大核对的精细数值作为主报告结论。[原文](https://arxiv.org/html/2403.00839v1)

MCP-Zero、MemTool 方法级阅读表明，前者是工具需求驱动的分层主动发现/检索，后者主要是会话内工具集合/短期记忆增删；即使减少工具描述 token，也不能直接归成跨任务 trajectory learning。MetaAgent 的反思知识积累与工具求助与本题接近，但尚未审计净成本实验。AgentOrchestra、OS-Copilot、STELLA、LLM Agents Making Agent Tools、GitHub 工具整合等保留为方法背景；没有读透的论文不报具体收益。其余训练边界未核的系统、EDA 工具进化等仍有 unresolved 候选，已在 JSON 标识，不能以本轮选择性深读宣称整个 TOOL 分支所有相关工作均已穷尽。

### 最终完整性补核：EvoDS 与 OrchDAG

在剩余 uncertain 中，额外检查了题名上最接近“技能学习/上下文效率”与“复杂工具编排”的两篇。结论是：两者的主方法均依赖模型训练，不是遗漏的更直接无训练加速近邻；各 JSON 的状态已由主报告维护者更新，本备忘录不再修改筛查文件。

**EvoDS（原 row 230）。** 实读 arXiv:2606.03841v1 的 §4.2–4.4、§6.1.3–6.6。可执行技能通过合成、实际执行验证、缓存和频率门槛进入持久动作空间；但 §4.4 明确对各角色共享的 Qwen3-8B 先 SFT、再联合 RL，§6.1.3 给出 4×A800 训练。Table 2 有 `w/o train` 的质量消融，并不证明无训练版本取得主方法的收益。§6.6 的效率图反映训练期间的上下文 token 和 reward；没有完整冻结模型的秒／美元净成本比较。因此主方法改为训练范围排除，技能机制可作相邻参考。[原文](https://arxiv.org/html/2606.03841v1)

**OrchDAG（原 row 186）。** 实读 arXiv:2510.24663v1 的 §3.1–3.2、§4.1–4.3。它主要生成带工具依赖 DAG 的多轮合成数据，使用 graph edit distance 形成更稠密的奖励，对 Qwen2.5 进行 GRPO 等 RLVR 训练。主表评估 DAG 预测及工具调用准确率，不能当作固定模型跨任务技能复用的执行加速。标题的“orchestration”容易让它看起来像无训练调度系统，原文实际定位应归入训练范围排除。[原文](https://arxiv.org/html/2510.24663v1)

这次补核未发现应替代 WALT、ActionEngine、SpeedRunner 等直接近邻的工作；它不改变对其余 uncertain 条目尚未全面深读的限定。

## 4. 对第三阶段计划的约束与可检验空间

下列是基于文献的研究判断，不是“已证明没人做过”的新颖性结论。

- **基线需要比文字记忆更强。** A 路线应有 ASI/SpeedRunner 式程序技能；B 路线应有 DRAFT 文档、SkillWeaver/WALT 操作函数、ActionEngine 状态机知识。只与无记忆 ReAct 比，会把已有的机制收益错当成新贡献。
- **把信息来源分开做消融。** 仅历史轨迹、仅额外环境探索、二者结合；同样的最终技能表示、actor、任务分布、学习预算。这样才能知道主动探索是在补轨迹没有覆盖的前置条件/异常分支，还是只是增加样本和计算。
- **明确泛化粒度。** 同题重跑、新参数、同站新模板、跨站、UI/权限/数据模式变化，至少分开报告。MUSE 的覆盖子集与 ActionEngine 的 template warm-up 都说明“test instance 没见过”并不等于“任务结构没见过”。
- **直接优化质量约束下的总成本。** 首次学习、失败探索、verification、warm-up、检索、在线调用、repair、淘汰均计入；报告累计成本随复用次数变化，不只中位数 ratio。SpeedRunner 已做到学习成本摊销，不能声称该原则本身空白；我们的可检验问题是企业 Web 真实成本/维护项是否改变比较结论。
- **验证与生产执行分离。** 比较可重置 sandbox replay、独立 read-only 检查、源系统事后校验、来自外部规范的 proxy。特别记录误接纳率和错误副作用，不能用“skill 自测通过”代替业务结果正确。CoEvoSkills 与 OpenSkill 给出不同的监督假设，必须明确选择。
- **保留原子执行 fallback 并量化触发。** 条件不满足、技能失效、页面漂移应退回一般 agent。分别看快路径命中率、正确率、节省的模型决策次数、维护开销；证明长期收益需要一条变化任务流，不能只在静态成功子集测。

最稳妥的研究切入不是泛化地“做一个会自我进化的 agent”，而是：在固定模型、重复但会变化的企业工作流中，测清哪些历史证据/补充探索足以让程序化快路径可靠复用，以及何时继续学习、何时直接反应式执行的总成本更低。是否足够新颖，仍需结合其他分支近邻再定，不能由本证据备忘录单独断言。

## References

以下为本备忘录实质讨论/原文深读的完整引用；目录级全部 51 条标题与 URL 在配套 JSON 中。预印本身份按所读版本注明；本地 PDF 第一页的 venue 声明未独立核实者保留说明。

[ST1] Boyuan Zheng, Michael Y. Fatemi, Xiaolong Jin, Zora Zhiruo Wang, Apurva Gandhi, Yueqi Song, Yu Gu, Jayanth Srinivasa, Gaowen Liu, Graham Neubig, and Yu Su. 2025. *SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills*. arXiv:2504.07079, **v1**. 本文未独立核实最终发表 venue；OSU/UVA/Purdue/CMU/Cisco Research. [PDF](https://arxiv.org/pdf/2504.07079v1).

[ST2] Zora Zhiruo Wang, Apurva Gandhi, Graham Neubig, and Daniel Fried. 2025. *Inducing Programmatic Skills for Agentic Tasks*. **COLM 2025**. arXiv:2504.06821, **v2**. [PDF](https://arxiv.org/pdf/2504.06821v2); [OpenReview](https://openreview.net/forum?id=lsAY6fWsog).

[ST3] Viraj Prabhu, Yutong Dai, Matthew Fernandez, Krithika Ramakrishnan, Jing Gu, Yanqi Luo, Silvio Savarese, Caiming Xiong, Junnan Li, Zeyuan Chen, and Ran Xu. 2026. *WALT: Web Agents that Learn Tools*. **ICLR 2026**. 实读会议 camera-ready PDF，非旧 arXiv:2510.01524v1；正式 proceedings 核实 venue。[正式论文页及 PDF 入口](https://proceedings.iclr.cc/paper_files/paper/2026/hash/5b175f9e93873e3a10a6ce43dbb82e05-Abstract-Conference.html).

[ST4] Hongbin Zhong, Fazle Faisal, Luis França, Tanakorn Leesatapornwongsa, Adriana Szekeres, Kexin Rong, and Suman Nath. 2026. *ActionEngine: From Reactive to Programmatic Web Agents via State Machine Memory*. arXiv:2602.20502, **v2, September 28, 2026**. Georgia Tech/Microsoft；本文按预印本补充。[PDF](https://arxiv.org/pdf/2602.20502v2).

[ST5] Zixi Huang, Xiheng Wang, Andrew Wang, William Jurayj, Bernal Jiménez Gutiérrez, Daniel Khashabi, and Nicholas Andrews. 2026. *Better, Faster, Stronger: Programmatic Skill Learning Best Reduces Agent Cost*. arXiv:2608.11338, **v1**. Johns Hopkins University；预印本，方法名 SpeedRunner。[PDF](https://arxiv.org/pdf/2608.11338v1).

[ST6] Advantage AI Agent Lab (A3 Lab). 2026. *GenericAgent: A Token-Efficient Self-Evolving LLM Agent via Contextual Information Density Maximization (V1.0)*. arXiv:2604.17091, **v1**. 论文用集体署名，§8 列出全部贡献者：Jiaqing Liang, Jinyi Han, Weijia Li, Xinyi Wang, Zhoujia Zhang, Zishang Jiang, Ying Liao, Tingyun Li, Ying Huang, Hao Shen, Hanyu Wu, Fang Guo, Keyi Wang, Zhonghua Hong, Zhiyu Lu, Lipeng Ma, Sihang Jiang, Yanghua Xiao。深圳企业与复旦成员的联合实验室；预印本补充。[PDF](https://arxiv.org/pdf/2604.17091v1).

[ST7] Huawei Lin, Peng Li, Jie Song, Fuxin Jiang, and Tieying Zhang. 2026. *MUSE-Autoskill: Self-Evolving Agents via Skill Creation, Memory, Management, and Evaluation*. arXiv:2605.27366, **v2**（实读 PDF 首页日期 July 7, 2026；不要用原始 arXiv 编号月份代替本版本日期）。ByteDance/Rochester Institute of Technology；预印本补充。[PDF](https://arxiv.org/pdf/2605.27366v2).

[ST8] Zhiling Yan, Dingjie Song, Hanrong Zhang, Wei Liang, Yuxuan Zhang, Yutong Dai, Lifang He, Philip S. Yu, Ran Xu, Xiang Li, and Lichao Sun. 2026. *OpenSkill: Open-World Self-Evolution for LLM Agents*. arXiv:2606.06741, **v1**. Lehigh/UIC/UBC/Vector/Salesforce/Harvard 等；预印本补充。[PDF](https://arxiv.org/pdf/2606.06741v1).

[ST9] Hanrong Zhang, Shicheng Fan, Henry Peng Zou, Yankai Chen, Zhenting Wang, Jiayu Zhou, Chengze Li, Wei-Chieh Huang, Yifei Yao, Kening Zheng, Xue (Steve) Liu, Xiaoxiao Li, and Philip S. Yu. 2026. *CoEvoSkills: Self-Evolving Agent Skills via Co-Evolutionary Verification*. arXiv:2604.01687, **v3**. PDF 标注 COLM2026；本轮未独立核实会议正式记录，按该预印本版本引用。[PDF](https://arxiv.org/pdf/2604.01687v3).

[ST10] Changle Qu, Sunhao Dai, Xiaochi Wei, Hengyi Cai, Shuaiqiang Wang, Dawei Yin, Jun Xu, and Ji-Rong Wen. 2025. *From Exploration to Mastery: Enabling LLMs to Master Tools via Self-Driven Interactions*. **ICLR 2025**. arXiv:2410.08197, **v2**；方法 DRAFT。[PDF](https://arxiv.org/pdf/2410.08197v2); [会议 PDF](https://openreview.net/pdf?id=QKBu1BOAwd).

[ST11] Tianle Cai, Xuezhi Wang, Tengyu Ma, Xinyun Chen, and Denny Zhou. 2024. *Large Language Models as Tool Makers*. **ICLR 2024**. arXiv:2305.17126, **v2**；方法 LATM。[PDF](https://arxiv.org/pdf/2305.17126v2); [OpenReview](https://openreview.net/forum?id=qV83K9d5WB).

[ST12] Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi “Jim” Fan, and Anima Anandkumar. 2024. *Voyager: An Open-Ended Embodied Agent with Large Language Models*. **Transactions on Machine Learning Research (TMLR)**. 实读 arXiv:2305.16291, **v2 (2023)**；会议/期刊最终版与实读版本区分。[PDF](https://arxiv.org/pdf/2305.16291v2); [OpenReview](https://openreview.net/forum?id=ehfRiF0R3a).

[ST13] Yanzhou Li, Yiran Zhang, Xiaoyu Zhang, Xiaoxia Liu, and Yang Liu. 2026. *CODESKILL: Learning Self-Evolving Skills for Coding Agents*. arXiv:2605.25430, **v2**. NTU/Zhejiang；预印本，主方法因训练 skill manager 排除。[PDF](https://arxiv.org/pdf/2605.25430v2).

[ST14] Xukun Liu, Zhiyuan Peng, Xiaoyuan Yi, Xing Xie, Lirong Xiang, Yuchen Liu, and Dongkuan Xu. 2024. *ToolNet: Connecting Large Language Models with Massive Tools via Tool Graph*. arXiv:2403.00839, **v1**. 实读 HTML 方法/实验；本轮未独立核实最终发表 venue。[原文](https://arxiv.org/html/2403.00839v1).

[ST15] Hongjin Qian and Zheng Liu. 2025. *MetaAgent: Toward Self-Evolving Agent via Tool Meta-Learning*. arXiv:2508.00271, **v2**. Technical report；实读 HTML 方法，未审计净加速。[原文](https://arxiv.org/html/2508.00271v2).

[ST16] Xiang Fei, Xiawu Zheng, and Hao Feng. 2025. *MCP-Zero: Active Tool Discovery for Autonomous LLM Agents*. arXiv:2506.01056, **v4**. 预印本；实读 HTML 方法，仅作主动工具检索背景。[原文](https://arxiv.org/html/2506.01056v4).

[ST17] Elias Lumer, Anmol Gulati, Vamse Kumar Subbiah, Pradeep Honaganahalli Basavaraju, and James A. Burke. 2025. *MemTool: Optimizing Short-Term Memory Management for Dynamic Tool Calling in LLM Agent Multi-Turn Conversations*. arXiv:2507.21428, **v1**. 预印本；实读 HTML 方法/实验，短期工具管理背景，不承担核心研究结论。[原文](https://arxiv.org/html/2507.21428v1).

[ST18] Zhuofeng Li, Haoxiang Zhang, Seungju Han, Sheng Liu, Jianwen Xie, Yu Zhang, Yejin Choi, James Zou, and Pan Lu. 2026. *In-the-Flow Agentic System Optimization for Effective Planning and Tool Use*. arXiv:2510.05592, **v2**. arXiv 作者声明 ICLR2026 Oral，本轮未另核 proceedings；实读 HTML 方法及训练附录，按训练排除。[原文](https://arxiv.org/html/2510.05592v2).

[ST19] Zherui Yang, Fan Liu, Yansong Ning, and Hao Liu. 2026. *EvoDS: Self-Evolving Autonomous Data Science Agent with Skill Learning and Context Management*. arXiv:2606.03841, **v1**. HKUST (Guangzhou)；原文标注 KDD 2026、DOI 10.1145/3770855.3818002，本轮未独立访问 ACM proceedings 核验；实读 HTML 方法、训练与实验，主方法按训练排除。[原文](https://arxiv.org/html/2606.03841v1).

[ST20] Yifu Lu, Shengjie Liu, and Li Dong. 2025. *OrchDAG: Complex Tool Orchestration in Multi-Turn Interactions with Plan DAGs*. arXiv:2510.24663, **v1**. Princeton University/Amazon；预印本，实读 HTML 方法与实验，主方法按 RLVR 训练排除。[原文](https://arxiv.org/html/2510.24663v1).
