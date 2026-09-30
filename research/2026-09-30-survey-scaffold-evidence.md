# Self-improvement 综述：Full Scaffolding 分支核查

核查日：2026-09-30。范围：项目网站清单 row 233–253，共21条；另补 HarnessFix、StarHarness 两个直接近邻。筛查逐条记录见 `2026-09-30-survey-scaffold-screen.json`。本文以新查原文为证据；旧研究记录只用于发现线索，不视作独立证据。未改 canonical dossier，未分配全局 E/D 编号，未复现实验。

阅读深度分级：**深读**指读方法、实验协议、相关结果与局限，并检查所引表图；不等于通读所有附录或审查完整代码。**选读**指读原文相关章节，不据摘要推断效果。**资格筛查**只决定是否进入引用范围。网页更新清单不等于 PDF 正文参考文献：正文 §6.4 主要覆盖较早工作，部分2026条目来自持续更新的网站。

## 1. 证据表与判断

### 1.1 加速证据的口径

下表均为**一级来源、作者报告**，核查日均为2026-09-30。费用是每次尝试或整次运行的费用，不能自动转换成每成功任务费用。除明确说明外，均没有证明包括改进开销的生命周期净收益。

| 记录 | 主张与实际证据（来源位置、短引文） | 结论 |
|---|---|---|
| S-F01 · StarHarness | GPT-5.4 medium，EnterpriseOps-Gym 的103个ITSM任务，原始 Stirrup→演化harness：成功率23.3%→43.7%，turns/task18.12→9.87，tool calls/task29.53→16.83；估算API费/task $1.23→$0.58，作者报−53%。Table4明确“full-benchmark”，因此含演化池；§4.4/Table2另报held-out成功率+15.1个百分点。 [v1 pp.7–8, Tables2/4](https://arxiv.org/pdf/2608.24804v1) | 有部署调用/费用下降证据，是最直接近邻；没有held-out费用分报，也未给完整搜索投入与回本。 |
| S-F02 · Adaptive Auto-Harness | Sonnet4.6 solver、Opus4.6 evolver，FutureX503题：no-evo→Full System，求解端每题elapsed之和34.2h→6.6h，输入55.5M→25.6M token，输出0.7M→0.5M；Table2 Pass@1 31.0%→47.3%。但PolyBench5075题elapsed合计25.6h→59.5h。Table5注明“excludes orchestration overhead”，且evolver tokens未保存。 [v2 §4, App.B, Table5 pp.12–13](https://arxiv.org/pdf/2606.01770v2) | 特定任务流有部署收益，跨域不一致；该hours是逐任务耗时求和，不能当并发端到端工期或全流程费用。 |
| S-F03 · Continual Harness | Gemini3.1 Pro，在Pokémon Emerald、每seed24小时、31里程碑口径：from-scratch harness单元的median为$130/100%里程碑，minimal为$215/98%；作者报约40%费下降。Fig6横轴为API spend，cached input按25%计价。按键次数另作动作效率指标，明确不是tool calls。 [v1 §§4.3–4.4, Fig5/6, App.A](https://arxiv.org/pdf/2605.09998v1) | 固定模型部分直接有费用与进度证据；不是完成整个游戏时间缩短。弱模型反而下降；成本账是否覆盖每类Refiner调用仍需代码对账。 |
| S-F04 · Live-SWE-agent | SWE-bench Verified500题、单次patch。mini-SWE→Live，GPT-5为65.0%/$0.28→68.4%/$0.27；Gemini3 Pro为74.2%/$0.46→77.4%/$0.48。Table1是“Avg. $ Cost”。§3默认上限250步/$3每题；baseline结果按§3直接沿用，非所有对照重新运行。 [v3 pp.5–6, Table1](https://arxiv.org/pdf/2511.13646v3) | 在线工具构建可提高成功率；成本并非一致下降。没有offline search不等于零在线改进成本，也未证明跨任务累计工具收益。 |
| S-F05 · HGM | SWE-Verified-60，同为800次任务评估，GPT-5扩展、GPT-5-mini评估；DGM/HGM的best-belief成功率53.3%/56.7%，allocated CPU-hours1231/517，作者比值2.38×。Table2写“required for 800 evaluations”。 [v3 §4.2/Table2 p.9](https://arxiv.org/pdf/2510.21614v3) | 是外层版本搜索资源效率；不代表部署agent每题快2.38×，也不是固定成功率达到阈值的严格对照。 |
| S-F06 · DGM | 固定FM，自改代码并保存archive；80轮后SWE-bench选定200题成功20%→50%，不能写成全500题。App.E.1估算一次完整SWE搜索约$22,000，消融约$10,000。作者承认“greater inference costs”。 [ICLR2026版/arXiv v3 §§4.2–4.4, App.E.1 pp.32–33](https://arxiv.org/pdf/2505.22954v3) | 证明自改代码提高能力，非部署降本；强版本有可能更贵。 |
| S-F07 · HarnessFix | GPT-5-mini，AppWorld225题划为90/45/90 train/validation/test；三次独立运行的平均TCR36.7%→43.0%，Table4中离线evolving/repair tokens为37.2M；Meta-Harness为40.4%/74.6M。原文称“offline evolving/repair tokens”。 [v2 §§IV–V, Tables3/4 p.9](https://arxiv.org/pdf/2606.06324v2) | 降低的是相对Meta-Harness的改进搜索token，不是已部署agent每题费用；token是单次还是三次平均原文不够清楚。 |
| S-F08 · AgentDevel | Sonnet4.5+Claude Code，Table1 WebArena基础17.0%→35.5%；§3.1称开发决策只用TrainSet、最终TestSet仅一次。未给充分的具体样本数/分割复現材料；App.A直接承认额外compute/wall-clock。 [v1 §§2–3, Table1 p.7, App.A](https://arxiv.org/pdf/2601.04620v1) | 作为回归门禁方法参考；效果证据透明度弱于上述明确样本协议，不作为加速证据。 |

视觉核查：StarHarness PDF p.8；Adaptive p.13 Table5；Continual p.8 Fig6；Live p.6 Table1/2；HGM Table2；HarnessFix p.9；AgentDevel p.7。DGM p.6核了评估样本与主结果文字，App.E.1费用从PDF文字层核验。临时截图位于 `/private/tmp/scaffold-*.png`，不依赖截图作为永久引文。

### 1.2 直接近邻怎样把轨迹转成改变

**StarHarness：把反复失败的环境交互改成更可靠的接口和确定性操作。** 固定模型，proposer读取search轨迹和持久版本日志，提出一个有边界的git patch；先做scope/import/smoke检查与单题fail→pass测试，再以proposer看不到的selection集合选择，最后报告holdout。它学到的具体内容包括MCP schema/参数清理、关联字段与业务更新约定、日期和财务计算器、结构化表格行操作。作者承认多个patch的单独因果贡献无法拆开，tree→hill climbing是顺序阶段而非独立对照。**我们的判断：A的轨迹诊断与B的环境知识编码已有直接交集；“把知识编译进代码”本身不足以支撑新颖性。** 搜索前使用全基准baseline表现做分层，亦须与完全未触碰测试集区别。[S-F01；§§3、5]

**HarnessFix：先定位运行时缺陷，再做受限修复。** 四阶段为轨迹抽象、诊断、修复、验证；HTIR连接执行步骤、数据/控制依赖和harness代码位置，重复诊断合并成flaw record，映射到受限repair operators，生成具体修改契约，再审范围和回归。它已越过“把失败日志直接丢给LLM改prompt”的粗略做法。作者实验还独立用人工标注失败轨迹评估诊断；不过这里是归因指标，不能当作反事实因果证明。**我们的判断：适合做A的强对照，重点问诊断是否真能选对干预；成本目标需要另加。**[S-F07；§III、RQ2/3]

**Adaptive Auto-Harness：学习构造能力和任务时选择能力分开。** 历史批次触发Analyze→Research→Build→Verify，保留任务板、失败假设、研究日志和测试；建立多个git harness分支，router按当前任务选分支。对延迟反馈只在结果可获得后向evolver开放。还有在经验不包含所需信息时的人类指引通道，但Table2主结果没有HITL。作者把理论loss作为诊断框架，并没有直接估计oracle loss；仅测三类流。**我们的判断：适合研究经验何时泛化、何时应分支，不能先假设分支和router一定更快。**[S-F02；§§3–4、6、App.B]

**Continual Harness：不重置环境，在长轨迹中修补自身。** Actor与Refiner用同一固定模型。每隔一段交互，Refiner诊断导航循环、调用失败、目标停滞等，分别改prompt、子agent定义、可执行skills和memory；成功序列可以固化成代码，陈旧内容可删除。它同时比较from-scratch、继承后冻结、继承后继续更新。作者发现复杂对话/战斗组件仍不易合成，且Flash-Lite无法可靠利用组件。**我们的判断：它确实连接环境探索与在线加速，但可访问emulator text-map/通用状态原语，不能直接类推浏览器中未知企业应用。**[S-F03；§§2–4.4、6、App.A]

**Live-SWE-agent：在当前任务里按需制造工具。** bash-only的mini-SWE-agent通过初始示例和每步环境反馈后的reflection，决定是否写/改脚本。任务专用的文件分析器也允许，不要求所有工具可通用；当前实现重点是工具合成，底层loop保持简单。作者的弱模型消融显示提示自改可能让agent陷入错误循环。**我们的判断：这是比完整harness搜索轻的实施对照；需要另测工具何时值得创建，以及能否跨任务继承。**[S-F04；§§2、4.3]

### 1.3 优化循环本身也有不同目标

**DGM→HGM**：DGM从版本archive挑父代，结合失败日志诊断、编辑自身代码、分阶段评估；开放archive保留可能成为后续改进起点的版本。HGM区分“当前做题好”与“该分支能产生更好的后代”，用后代累计结果估计CMP，并自适应选择扩展或再评估。它们可以帮助A管理候选和评估预算，但目标首先是agent能力提升。把目标替换成正确性约束下的延迟/费用，是我们的设计选择，不能归为作者已经验证。[S-F05/06]

**AgentDevel**：只保留单个canonical版本；看不到实现的critic描述症状，开发器写可执行诊断脚本形成修改规范，候选必须通过pass→fail与fail→pass翻转门禁。作者明说阈值是可配置政策；盲critic仍有LLM评估偏差。它说明“整体分数上升”不足以保证既有行为不退化，但没有证明可靠门禁一定省成本。[S-F08]

**JudgeFlow**把可执行workflow拆成顺序、循环、条件logic blocks，judge从失败trace给block责任排序，optimizer定向修改高责任模块。§4.4例子通过增加self-refine block提高解题质量；这也说明更正确可能需要更多调用。所称效率主要针对优化过程。适合诊断粒度对照，不作为部署加速结论。[12]

**Group-Evolving Agents**把不同分支的patch、失败轨迹和反思汇合，使有用经验能跨分支复用。它匹配的是产生agent数量，实验中Haiku切换到Sonnet，不能读成全过程固定一个backbone或等dollar预算；模型未做参数训练。**Hyperagents**进一步让任务agent和改进器处于同一可编辑程序，使改进策略也可修改；不代表评估目标和外层所有规则都自改。其robotics reward-design任务涉及下游策略学习，应与纯固定FM代码改进任务分开。**RQGM**则改agent与evaluator程序，但在每个epoch冻结当前judge，用ground-truth anchor决定替换并清理不兼容旧分数；固定scoring/orchestration仍存在。它支持“评价器也会成为瓶颈”的研究问题，并不授权让最终验收随被评agent一起变。[18–20]

### 1.4 全21条的筛查结论

| row | 工作 | decision | 阅读/保留理由 |
|---|---|---|---|
|233|GPTSwarm|method|原文方法与正式ICML元数据；优化prompt/图结构，非本轮部署加速证据。|
|234|STOP|method|原文算法筛读；自改程序优化器，作为递归改进历史。COLM2024由PDF标识，官方页本轮受反爬；机构资格仍成立。|
|235|ADAS|method|原文方法与正式会议页；网站写NeurIPS应更正为ICLR2025。|
|236|Agent Symbolic Learning|method|v1原文首页/机制与正式期刊元数据；AI Open2025，Zhejiang作者信息满足机构补充。未精读期刊新版实验。|
|237|DGM|method|深读方法/实验/成本；提高能力而非已证实部署加速。|
|238|HGM|method|深读方法/实验；提高搜索资源效率。|
|239|Gödel Agent|method|原文方法筛读，ACL2025正式版本可查；递归源码修改背景。|
|240|AlphaEvolve|background|原文任务范围筛读；算法/基础设施程序优化，非trajectory复用的agent加速核心。|
|241|ShinkaEvolve|method|原文方法/任务筛读；采样效率和reasoning-harness搜索。正式ICLR2026已核。|
|242|Live-SWE-agent|core|深读；在线工具创建、费用/成功率，有明确失败边界。|
|243|AgentDevel|method|深读；回归门禁强相关，效率未量化。|
|244|JudgeFlow|method|方法/案例/优化成本选读；失败归因改善搜索。|
|245|RoboPhD|exclude|仅原文首页资格筛查：Independent Researchers；无已核实合格机构/顶会，保持审核记录，不支撑结论。|
|246|Adaptive Auto-Harness|core|深读；流式轨迹+分支适应，效率有明确口径缺口。|
|247|MOSS|method|方法与案例选读；生产代码修补、回放、rollback，但案例规模不足以建立普遍加速。|
|248|RSEA|method|方法/协议选读；主要改策略/技能/playbook文本，网站分到full scaffold不等于任意代码自改。|
|249|Continual Harness|core|深读固定模型分支；论文后半训练分支排除。|
|250|RQGM|method|原文方法/任务范围选读；评估器共演化，不作为速度证据。|
|251|Group-Evolving Agents|method|方法/模型日程/比较条件选读；跨分支经验共享。|
|252|Hyperagents|method|方法/实验与任务边界选读；改进器可自改，未核全部图表数字。|
|253|Harness-R1|exclude|原文训练流程核验：target冻结，但9B engineer做SFT+GRPO；不符合全流程免训练范围。|

综述外补充：HarnessFix=method，StarHarness=core。21条网站清单为3 core、15 method、1 background、2 exclude；这些标签是本研究的相关性分类，不是质量排名。详细字段与URL见配套JSON。

### 1.5 对研究计划的影响（本组推论）

1. **“自演化”描述改进过程，“加速”描述资源目标。** 从轨迹生成prompt、记忆、工具或代码，是可用手段；许多self-evolving结果只是正确率提高，并可能增加部署开销。两条轴应分开标。
2. **粗略idea已有成熟近邻。** HarnessFix覆盖轨迹归因到harness修复；StarHarness覆盖环境约定、工具接口和确定性计算；Continual覆盖长轨迹中边探索边修补；这些不能略过后把“历史经验→改进”当新颖性。
3. **较稳妥的第一轮比较应窄而强。** 在同模型、同任务流、同信息权限下，对照不学习、文本经验、可执行工具、受限harness修复。先验证哪类重复浪费可被代码消除，再决定是否引入复杂archive/CMP/router。
4. **尚可研究的空间要按可证伪问题表达。** 例如：明确的失败/成本归因，能否比自由harness搜索用更少改进预算获得更大held-out净收益？环境探测转化的可执行动作，能否在新参数/新版本/新组合任务上稳定复用？答案可能是否，不能当既定文献空白。
5. **评估程序应明确三份账和三种集合。** 搜索/构造、验证/选择、部署执行分别计量；开发、反复选择、最终测试分开。proposer看不到selection标签，不会让selection脱离优化过程。批量求解seconds求和、allocated CPU-hours、API估算费不可相互替代。

[综述§8](https://arxiv.org/pdf/2607.13104)本身也要求固定预算下的曲线、分离held-out、成本构成和回归跟踪；它没有证明其中所有收录论文都达到这些要求。我们借用该评估框架时仍需逐文核查。

## 2. D-ledger 待合并事项（未分配新D编号）

- ADAS的正式venue为ICLR2025，不是网站显示的NeurIPS。DGM/HGM/ShinkaEvolve亦应区分网站旧arXiv标记与正式ICLR2026资料。
- HGM搜索CPU小时与部署加速必须分开；Live-SWE Table2转述HGM为512h，而原HGM v3 Table2为517h。引HGM原文517h，不把转述差异静默合并。
- Harness-R1属于“固定target、训练editor”，不是全系统无训练。Continual Harness反过来必须按实验分支切分，不能因含训练部分把其固定模型费用结果一并排除。
- Full scaffolding网站分组是导航，不是精确可编辑范围证明。Live-SWE实现主攻工具，RSEA主攻文本状态，不能据分类名称称二者可任意改完整运行时代码。
- StarHarness中full-benchmark成本与holdout性能是不同统计口径；Adaptive的solver-only时间缺失evolver/编排开销，均不能称净生命周期降本。

## 3. E-ledger patches

本次不直接修改既有E条目。S-F01–08为独立候选证据记录，交由主报告合并时统一编号；既有E306/DGM需保留版本差异，不能用v3的正式出版身份去暗示所有旧数值已经逐项重新核对。

## 4. Still-open

- StarHarness是否公开完整候选、失败搜索尝试与各类token账；只有heldout准确率不能确定heldout每任务费用改善幅度。
- Continual Harness Fig6 API cost需要进一步从日志/计费代码核实Refiner、失败调用与子agent全覆盖；本文只称作者图中run API spend。
- Adaptive Auto-Harness evolver tokens缺失无法由其Table5恢复；即使FutureX solver快，也不能直接计算break-even任务数。
- HarnessFix需核精确repair budget、token是否跨三seed聚合，以及受限operators是否覆盖我们的环境问题。
- AgentDevel实验样本数、分割清单和复现工件不充分；宜借门禁思路，避免将其headline当最强实验证据。
- 本轮不复现；不宣称“这些方法中没有人做过摊销/跨环境测试”。结论只到已读原文所报告的范围。

## References

以下为完整作者与题名；正式发表信息和本轮实际阅读版本分开。除注明正式venue外，均按预印本/技术报告引用，不能仅因arXiv或网站标签升级为顶会。RoboPhD与Harness-R1只作排除审计。

1. Mingchen Zhuge; Wenyi Wang; Louis Kirsch; Francesco Faccio; Dmitrii Khizbullin; Jürgen Schmidhuber. **GPTSwarm: Language Agents as Optimizable Graphs.** ICML 2024, PMLR235:62743–62767. [正式页](https://proceedings.mlr.press/v235/zhuge24a.html)。实读arXiv2402.16823v3，方法筛读。
2. Eric Zelikman; Eliana Lorch; Lester Mackey; Adam Tauman Kalai. **Self-Taught Optimizer (STOP): Recursively Self-Improving Code Generation.** 2024. 实读[arXiv2310.02304v3](https://arxiv.org/pdf/2310.02304v3)，PDF标COLM2024；本轮官方OpenReview入口受反爬，保留机构补充资格。
3. Shengran Hu; Cong Lu; Jeff Clune. **Automated Design of Agentic Systems.** ICLR2025. [正式页](https://proceedings.iclr.cc/paper_files/paper/2025/hash/36b7acf6f6010652b3f2a433774a66fe-Abstract-Conference.html)。实读缓存conference PDF（对应arXiv2408.08435），方法筛读。
4. Yixin Ou; Wangchunshu Zhou; Shengwei Ding; Long Li; Jialong Wu; Tiannan Wang; Jiamin Chen; Shuai Wang; Xiaohua Xu; Ningyu Zhang; Huajun Chen; Yuchen Eleanor Jiang. **Symbolic learning enables self-evolving agents.** AI Open6 (2025):314–322. DOI[10.1016/j.aiopen.2025.11.004](https://doi.org/10.1016/j.aiopen.2025.11.004)。实读arXiv2406.18532v1首页/机制；正式期刊元数据已核，全文访问403；机构交叉核[作者提交SSRN页面](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5379114)。不引新版效果。
5. Jenny Zhang; Shengran Hu; Cong Lu; Robert Lange; Jeff Clune. **Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents.** ICLR2026, main conference poster. [正式会议信息](https://iclr.cc/virtual/2026/poster/10007327)。实读[arXiv2505.22954v3](https://arxiv.org/pdf/2505.22954v3)，2026-03-12，72页。
6. Wenyi Wang; Piotr Piękos; Li Nanbo; Firas Laakom; Yimeng Chen; Mateusz Ostaszewski; Mingchen Zhuge; Jürgen Schmidhuber. **Huxley-Gödel Machine: Human-Level Coding Agent Development by an Approximation of the Optimal Self-Improving Machine.** ICLR2026，[官方paper list](https://iclr.cc/virtual/2026/papers.html)。实读[arXiv2510.21614v3](https://arxiv.org/pdf/2510.21614v3)，2025-10-29，30页；未把会议版与该预印本假定逐字相同。
7. Xunjian Yin; Xinyi Wang; Liangming Pan; Li Lin; Xiaojun Wan; William Yang Wang. **Gödel Agent: A Self-Referential Agent Framework for Recursively Self-Improvement.** ACL2025. [正式来源](https://aclanthology.org/2025.acl-long.1354/)。实读arXiv2410.04444v4，方法筛读。
8. Alexander Novikov; Ngân Vũ; Marvin Eisenberger; Emilien Dupont; Po-Sen Huang; Adam Zsolt Wagner; Sergey Shirobokov; Borislav Kozlovskii; Francisco J. R. Ruiz; Abbas Mehrabian; M. Pawan Kumar; Abigail See; Swarat Chaudhuri; George Holland; Alex Davies; Sebastian Nowozin; Pushmeet Kohli; Matej Balog. **AlphaEvolve: A coding agent for scientific and algorithmic discovery.** Google DeepMind technical white paper,2025. 实读[arXiv2506.13131v1](https://arxiv.org/pdf/2506.13131v1)，任务范围筛读。
9. Robert Lange; Yuki Imajuku; Edoardo Cetin. **ShinkaEvolve: Towards Open-Ended and Sample-Efficient Program Evolution.** ICLR2026. [正式来源](https://proceedings.iclr.cc/paper_files/paper/2026/hash/7886b9bafe76c52fd568db10ff9772df-Abstract-Conference.html)。实读[arXiv2509.19349v1](https://arxiv.org/pdf/2509.19349v1)，2025，未逐项复核conference新版数据。
10. Chunqiu Steven Xia; Zhe Wang; Yan Yang; Yuxiang Wei; Lingming Zhang. **Live-SWE-agent: Can Software Engineering Agents Self-Evolve on the Fly?** UIUC preprint,2025. 实读[arXiv2511.13646v3](https://arxiv.org/pdf/2511.13646v3)，2025-11-24，20页。
11. Di Zhang. **AgentDevel: Reframing Self-Evolving LLM Agents as Release Engineering.** Fudan University preprint,2026. 实读[arXiv2601.04620v1](https://arxiv.org/pdf/2601.04620v1)，2026-01-08，11页。
12. Zihan Ma; Zhikai Zhao; Chuanbo Hua; Federico Berto; Jinkyoo Park. **JudgeFlow: Agentic Workflow Optimization via Block Judge.** KAIST等preprint,2026. 实读[arXiv2601.07477v2](https://arxiv.org/pdf/2601.07477v2)，2026-02-02，17页，方法/案例选读。
13. Andrew Borthwick; Stephen Ash. **RoboPhD: Self-Improving Text-to-SQL Through Autonomous Agent Evolution.** Independent Researchers preprint,2026. [arXiv2601.01126v2](https://arxiv.org/pdf/2601.01126v2)，2026-01-26；仅资格审核，排除出结论证据。
14. Zewen Liu; Zhan Shi; Yisi Sang; Bing He; Minhua Lin; Tianxin Wei; Dakuo Wang; Benoit Dumoulin; Wei Jin; Hanqing Lu. **Adaptive Auto-Harness: Sustained Self-Improvement for Agentic System Deployment on Open-Ended Task Streams.** Emory/Amazon/Penn State/UIUC/Northeastern preprint,2026. 实读[arXiv2606.01770v2](https://arxiv.org/pdf/2606.01770v2)，2026-06-03，23页。
15. Qianshu Cai; Yonggang Zhang; Xianzhang Jia; Huajiang Zheng; Wei Xue; Jun Song; Xinmei Tian; Yike Guo. **MOSS: Self-Evolution through Source-Level Rewriting in Autonomous Agent Systems.** USTC/HKGAI/HKUST/HKBU preprint,2026. 实读[arXiv2605.22794v2](https://arxiv.org/pdf/2605.22794v2)，2026-05-23，12页，选读。
16. Michael Nguyen; Quoc Nguyen; Paul Vuong. **Recursive Self-Evolving Agents via Held-Out Selection.** Monash University Malaysia preprint,2026. 实读[arXiv2606.28374v1](https://arxiv.org/pdf/2606.28374v1)，方法/评估协议选读。
17. Seth Karten; Joel Zhang; Tersoo Upaa Jr; Ruirong Feng; Wenzhe Li; Chengshuai Shi; Chi Jin; Kiran Vodrahalli. **Continual Harness: Online Adaptation for Self-Improving Foundation Agents.** Princeton/ARISE Foundation/Google DeepMind preprint,2026. 实读[arXiv2605.09998v1](https://arxiv.org/pdf/2605.09998v1)，2026-05-11，28页。本文保留固定FM实验，排除其模型训练分支。
18. Alex Iacob; Andrej Jovanović; William F. Shen; Daniel Burkhardt; Meghdad Kurmanji; Nurbek Tastan; Lorenzo Sani; Niccolò Alberto Elia Venanzi; Ambroise Odonnat; Zeyu Cao; Bill Marino; Xinchi Qiu; Nicholas D. Lane. **The Red Queen Gödel Machine: Co-Evolving Agents and Their Evaluators.** Cambridge/NVIDIA/Flower Labs/MBZUAI/Inria preprint,2026. 实读[arXiv2606.26294v2](https://arxiv.org/pdf/2606.26294v2)，2026-06-29，38页，方法选读。
19. Zhaotian Weng; Antonis Antoniades; Deepak Nathani; Zhen Zhang; Xiao Pu; Xin Eric Wang. **Group-Evolving Agents: Open-Ended Self-Improvement via Experience Sharing.** UCSB preprint,2026. 实读[arXiv2602.04837v1](https://arxiv.org/pdf/2602.04837v1)，2026-02-04，18页，方法/比较条件选读。
20. Jenny Zhang; Bingchen Zhao; Wannan Yang; Jakob Foerster; Jeff Clune; Minqi Jiang; Sam Devlin; Tatiana Shavrina. **Hyperagents.** UBC/Vector/Edinburgh/NYU/FAIR at Meta/Meta Superintelligence Labs preprint,2026. 实读[arXiv2603.19461v1](https://arxiv.org/pdf/2603.19461v1)，2026-03-19，60页，方法/任务边界选读。
21. Shuai Shao; Kangning Zhang; Qingyao Li; Shijian Wang; Hao Wang; Wenxiang Jiao; Yuan Lu; Yi Guo; Weiwen Liu; Weinan Zhang. **Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories.** SJTU/Xiaohongshu/Southeast University preprint,2026. 实读[arXiv2608.02276v1](https://arxiv.org/pdf/2608.02276v1)，2026-08-03，22页，训练边界审核；排除出全流程免训练方法。
22. Mengzhuo Chen; Junjie Wang; Zhe Liu; Yawen Wang; Haiming Zheng; Qing Wang. **From Failed Trajectories to Reliable LLM Agents: Diagnosing and Repairing Harness Flaws.** ISCAS/UCAS/Tianjin University preprint,2026. 实读[arXiv2606.06324v2](https://arxiv.org/pdf/2606.06324v2)，2026-07-02，13页；方法名HarnessFix。
23. Esakkivel Esakkiraja; Denis Akhiyarov; Vikas Yadav; Sai Rajeswar; Patrice Bechard; Sridhar Nemala; Sagar Davasam. **StarHarness: Evolving Harnesses with Stratified Search for Enterprise Environments.** ServiceNow/Mila/Université de Montréal preprint,2026. 实读[arXiv2608.24804v1](https://arxiv.org/pdf/2608.24804v1)，2026-08-25，10页。
