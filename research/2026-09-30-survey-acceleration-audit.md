# Self Improvement 与 Agent 加速的筛查及证据审计

核查日期统一为2026-09-30。主报告为 [固定模型权重下的 Agent 加速与自我改进](../notes/part3/2026-09-30-self-improvement-agent-acceleration-review-zh.md)。以下均为原作者一级来源（primary）的结果核查，未复现实验；本报告的研究建议属于推论。E644–E668、D436–D445为新增审计记录，不覆盖已有dossier条目。

## 1 证据表与筛查覆盖

网站方法表共253行，含foundation model77、prompt39、memory65、tool51、full scaffold21。按目录行决策：core15、method47、background63、exclude70、uncertain41、duplicate17。原始快照结构化在 `2026-09-30-survey-source-inventory.json`；逐行阅读深度、更正及原因在 `2026-09-30-survey-screening.json`。253不是全文读过的独立论文数，17是明确标注重复的行，也不是全库语义去重的穷尽结果。尚未全文读过的疑似训练条目保留目录级证据标签，排除仅表示本轮不纳核心。

综述网站只作为导航；指标从所列实际版本正文和表图核查。报告还补充不在对应分支表中的直接近邻。各分支文件保存更详细的实验条件、模型、局限与完整作者引用。主报告40篇论文引用另加1份公开分享字幕来源。

| ID | 核实结果和精确测量口径 | 原文短引及定位 | 一级来源与判定 |
|---|---|---|---|
| E644 | ACE离线AppWorld适配53,898→9,517秒；另一附录设置部署160题，input26.96M→58.62M、output251,442→270,652 | “Adaptation-Stage”；Table4 p10；Tables12–15 p19 | [2510.04618v3](https://arxiv.org/pdf/2510.04618v3)。适配效率与部署开销分开；不得混设置 |
| E645 | SkillOpt Spreadsheet提示224→1,995 tokens，搜索21.4M tokens；修改文本skill而非直接执行代码 | “Optimization Cost”；Table6 p14、§3 | [2605.23904v2](https://arxiv.org/pdf/2605.23904v2)。无新增部署optimizer调用≠零额外token |
| E646 | Meta-TTL每个含6 episodes的Jericho会话，3runs平均：Static593.2s/196K tokens/231calls，方法860.9s/364K/204 | “Inference efficiency comparison”；Table6 p9 | [2604.00830v4](https://arxiv.org/pdf/2604.00830v4)。少调用但更慢；另有离线搜索 |
| E647 | VASO手工映射SS97.2/TC85.3，自动映射SS96.8/TC86.5；SS是规范满足比例，不是端到端正确率 | “automatic prop align”；Table1 p8、§7 | [2606.05395v1](https://arxiv.org/pdf/2606.05395v1)。保证依赖未验证映射；正文96.6与表冲突不用 |
| E648 | Metis固定GPT-4o、AppWorld官方划分TGC51.8→60.1%，executor112.6K→97.4K tokens/task，14.55→11.25 turns；reflection7.9M | “No Memory”；Tables1–2 pp10–11 | [2606.24151v1](https://arxiv.org/pdf/2606.24151v1)。构造排除训练轨迹生成，非完整净成本 |
| E649 | ReasoningBank AppC.2总token50,847.4→53,054.5；calc. +4.3%，含action generation、judge、extraction | “Token”；Table5 p27 | [2509.25140v2](https://arxiv.org/pdf/2509.25140v2)。该表模型未单独明示，不能自行认定跨模型均值 |
| E650 | AWM-AS宏消融Mind2Web step SR45.1→46.4，task SR4.8→3.6；正式版正文局部另有3.2冲突 | “AWM-AS”；AppF Table13 | [ICML2025正式版](https://proceedings.mlr.press/v267/wang25bx.html)。宏可损害整体成功率 |
| E651 | MobileGPT八应用80任务消融，warm vs Derive延迟−62.5%、API费−68.8%；cold+3.9%/+0.6% | “warm-start”；§7.3.4–5、Fig7 pp12–13 | [2312.03003v3](https://arxiv.org/pdf/2312.03003v3)。该消融含人工纠正冷启动失败路径 |
| E652 | WALT在VisualWebArena-Classifieds，同GPT-5-mini text/self：SR57.5→61.5%、steps8.9→6.5；构造每tool $1.67 | “Tool construction and costs”；§4.4 Table2、§4.6 | [ICLR2026正式版](https://proceedings.iclr.cc/paper_files/paper/2026/hash/5b175f9e93873e3a10a6ce43dbb82e05-Abstract-Conference.html)。14次使用是构造费÷基线费，非净差回本 |
| E653 | ActionEngine同Opus4.6、655题：SR82.7→91.2%，87→27s，估算API $0.40→$0.05/task | “Patcher”；§5.1–5.3 Tables1–2、Fig4 | [2602.20502v2](https://arxiv.org/pdf/2602.20502v2)。每模板一个warm-up；正式评测关闭Patcher；费用含缓存效果 |
| E654 | SpeedRunner固定GPT-5.4-mini，200学习episodes、每50条30题评估、3seeds；BabyAI约67→近100%，成本约ReAct的1/8 | “sleep”；Fig3、AppA.3 | [2608.11338v1](https://arxiv.org/pdf/2608.11338v1)。曲线近似，已摊inducer并计input/cache/output；无秒级8倍结论 |
| E655 | MUSE共75题但仅47有可用skill；该子集中位729.3→434.7s，构造另156.3s；全集53.42%而非85.24% | “covered”；§4.3 Tables4、6 | [2605.27366v2](https://arxiv.org/pdf/2605.27366v2)。同题重跑/成功覆盖选择，延迟不含verifier |
| E656 | OpenSkill Opus4.6在线mean465.0→845.4s，median347.6→368.2；均未含skill构造；proxy precision56.9% | “Precision”；Table3、AppE Table8 | [2606.06741v1](https://arxiv.org/pdf/2606.06741v1)。能力提高但更慢，88.9%是另一意图覆盖测量 |
| E657 | StarHarness GPT-5.4、103题全benchmark：SR23.3→43.7%，turns18.12→9.87，估算API$1.23→$0.58/task | “full-benchmark”；Tables2、4 pp7–8 | [2608.24804v1](https://arxiv.org/pdf/2608.24804v1)。holdout只有成功率另报，未分费用和搜索回本 |
| E658 | Adaptive FutureX求解端逐题elapsed之和34.2→6.6h；PolyBench25.6→59.5h | “excludes orchestration overhead”；AppB Table5 pp12–13 | [2606.01770v2](https://arxiv.org/pdf/2606.01770v2)。缺evolver tokens与编排，非并发总工期 |
| E659 | Continual Gemini3.1Pro/Emerald每seed24h：from-scratch median$130/100%里程碑，minimal$215/98% | “API spend”；§4.4 Fig6 | [2605.09998v1](https://arxiv.org/pdf/2605.09998v1)。固定模型分支、作者计费口径；不是完整游戏快40% |
| E660 | HarnessFix GPT-5-mini，AppWorld90题test、3runs平均TCR36.7→43.0%；repair37.2M vs Meta-Harness74.6M tokens | “offline evolving/repair tokens”；Tables3–4 p9 | [2606.06324v2](https://arxiv.org/pdf/2606.06324v2)。后者为优化费用，不能代替部署费用 |
| E661 | HGM扩展GPT-5、评估GPT-5-mini，60题/800evaluations：CPU-hours1231→517，best-belief53.3→56.7% | “required for 800 evaluations”；§4.2 Table2 p9 | [2510.21614v3](https://arxiv.org/pdf/2510.21614v3)。2.38×是搜索资源比，不是每题速度 |
| E662 | ALITA工具给ODR-smolagents/GPT-4o复用，GAIA27.88→33.94%；不是在线速度实验 | “With Alita MCPs”；§5.1.2 Table2 p8 | [2505.20286v1](https://arxiv.org/pdf/2505.20286v1)。和每任务重置工具库主比较区分 |
| E663 | A-Mem演化笔记内容及链接；主要评估长对话QA，不能直接视作学到执行技能 | “Note Construction”；§3.1–3.4；§4 | [NeurIPS2025](https://proceedings.neurips.cc/paper_files/paper/2025/hash/19909c36f51abc4856b4560aff3d36d6-Abstract-Conference.html)。per-question与per-operation成本措辞有差异，不引净业务加速 |
| E664 | GLoW GPT-4.1-mini、1000交互、3runs：Zork1预算内最高分均值73.0 vs ICRL51.7；RL对比100–800×是交互数 | “Steps”；§4.2 Table1 p7、AppC.1 | [2509.24116v2](https://arxiv.org/pdf/2509.24116v2)。不是100–800×延迟或金额 |
| E665 | WorldEvolver Table2 best-of-5：Gemma ReAct ScienceWorld44.44→52.22%；GPT5.4mini65.56→63.33%；跨任务记忆消融只0.5–1.1pp | “best-of”；§4.1、Tables2/4、AppTables12/13 | [2606.30639v2](https://arxiv.org/pdf/2606.30639v2)。另有first-trial统计；总收益不能全归跨任务历史 |
| E666 | ExpeL ALFWorld动作14.82→14.30，trajectory tokens2051.49→2856.70 | “tokens”；AppJ Table6 p38 | [2308.10144v3](https://arxiv.org/pdf/2308.10144v3)。字符串token不等于API累计账单 |
| E667 | SEDM FEVER输入tokens：no-memory1.65M、G-Memory3.62M、SEDM2.47M；节省基线是G-Memory | “Prompt”；Tables2–4 p10 | [2509.09498v3](https://arxiv.org/pdf/2509.09498v3)。paired replay/选择开销不在推理表内 |
| E668 | CTIM-Rover 45题/7仓库：base42%、full40%、仅CTIM31% | “CTIM”；Table1 p4 | [2505.23422v1](https://arxiv.org/pdf/2505.23422v1)。小样本负结果，不能推广为所有记忆无效 |

## 2 D ledger additions

| ID | 需要防止的混淆或待修订口径 | 处理 |
|---|---|---|
| D436 | 加速目标与self-evolution机制、优化阶段与部署阶段混为一类 | 主报告分三种效率；不把HGM搜索比当部署速度 |
| D437 | 无权重等于无学习/无RL；看到training一词就排除 | MemRL外部标量学习与Meta-TTL文字搜索保留；Harness-R1训练editor排除 |
| D438 | ACE适配快推出执行token少；SkillOpt部署无optimizer调用推出零额外开销 | E644–646单列阶段与上下文增长 |
| D439 | AWM/ReasoningBank/ExpeL少步数推出总体省钱 | E649–650、E666；不同量纲分别报告，不改写成统一speedup |
| D440 | WALT旧版未报构建成本，或正式版14次使用就是严格净回本 | 使用camera-ready新增§4.6；净回本分母应为每任务实际差额，标为本报告核算 |
| D441 | ActionEngine主结果来自纯无任务先验探索，或包含在线Patcher维修性能 | 保留模板warm-up、关闭Patcher、缓存与成本拆分限制 |
| D442 | MUSE成功覆盖子集85.24%代替全集；OpenSkill88.9%当验证准确率 | E655–656给正确分母、指标与负面延迟 |
| D443 | 形式验证等于整个业务端到端保证，或隐藏测试实现等于未参与优化 | VASO映射假设；selection反馈与真正final test分开；在线先评分后学习另设协议 |
| D444 | 目录题名/URL/会议信息可以直接引用 | DC、SEDM、WizardLM错配单列；ADAS正式ICLR2025；Meta-TTL新标题；保留实际阅读版本 |
| D445 | 253行等于253篇全文审计，或者补充成本/回退就是首创 | 明示41条待核、目录与深读分层；SpeedRunner已有摊销，相关性不是新颖性证明 |

## 3 E ledger patches

不改canonical dossier、旧计划或旧E行。E644–E668是本次补充验证，可在后续授权合并时按相同对象/版本对照旧条目。没有将近期方法的数字直接加入原有“加速排行榜”。

本轮新增阅读证据还包括TextGrad §2（文字梯度类比）、Trace §2/§6（执行图优化）、GEPA §2–3/Fig18（提示搜索与提示长度）、FORGE §3/5/7（群体记忆、冻结与成本）；完整引用和限制见 `2026-09-30-survey-prompt-world-evidence.md` 与主报告。FORGE Mixed图文数值冲突未采用，SkillOpt cost/point分母未清不采用。

## 4 Still open

- 41个uncertain目录项没有完成方法/效率或来源资格核验，不能据此断言没有其他更近工作。全部名单可在merged JSON检索。
- 本轮从目录初筛选择强相关原文，没有读完97页综述的每一条引用，也未复现代码、核对所有原始日志。
- ActionEngine warm-up是否全计入回本、Continual所有Refiner费用覆盖、Adaptive缺失evolver tokens，仍需代码/日志或作者澄清。
- WebArena等受控环境与真实业务工作流的可重置性、权限、任务重复度、规则执行差异需要实测。
- 建议的适用条件与定向探测是候选假设，需先与Metis、SpeedRunner、WALT、ActionEngine、HarnessFix、StarHarness做同预算比较；本报告没有认定新颖性。
- 字幕用于解释作者分类与关切；实验效应仍以论文核查为准，未把自动转写用作原文引文。

完整参考文献见[主报告末尾](../notes/part3/2026-09-30-self-improvement-agent-acceleration-review-zh.md#参考文献)。筛查中的排除条目仅作为审计轨迹，不在主报告中用于支持性能结论。
