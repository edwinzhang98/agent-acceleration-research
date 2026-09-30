<!-- Exported from the Claude Doc 《文献里的公式：算速度和成本的》 (https://claude.ai/code/artifact/177ddf97-a4ed-4217-ab9c-686b5d0df45a), rev 6, on 2026-09-28. The Claude Doc is the working copy Edwin comments on; this file is a snapshot for the repo and for Claude Code. Embedded diagrams/charts appear as '[embedded content: …]' placeholders; formulas are ```latex blocks. -->

# 文献里的公式：算速度和成本的

Sep 28, 2026 · @Edwin

结论：89 个来源里 39 篇论文写了明确的、算时间或成本的公式，3 个厂商或第三方页面有计费或测量定义式，另有 5 个原文是顺着引用找到的（Cost-of-Pass、AndroidArena、Orca、vLLM、Anthropic Vision 页）；其余只报测量数字。时间模型都是"每步 = 模型生成 + 环境执行，串行相加"，加速文献在上面加一项"能重叠掉多少"；成本模型都是"各类 token × 单价"；把成本和准确率合成一个数的只有 WES、Cost-of-Pass 和 APGR。扫描范围：Part 1 和 Part 2 参考文献表（slides/references.md）的全部来源——83 篇 arXiv 论文加 6 个非 arXiv 来源；被可信度规则排除的 4 篇不看；GPA (arXiv:2604.01676) 因 arXiv 限流没读到。公式照原文抄（LaTeX），变量含义和章节跟在后面；一篇文献引用别人的公式时，顺着引用打开原文，公式记在原文名下。

## 一、时间和延迟的公式

写出时间模型的文献都用同一个骨架：每一步的时间 = 模型生成时间 + 工具或环境执行时间，各步串行相加。做加速的文献在这个骨架上加一项"能重叠掉多少"。下面按机制分组，每篇只抄它自己定义的式子。

### 1. 串行基线和并行调用

**Kim, Moon, Tabrizi, Lee, Mahoney, Keutzer & Gholami (2024), An LLM compiler for parallel function calling, ICML 2024, arXiv:2312.04511v3, 附录 E.1, 式 (1)–(6)。** ReAct 串行执行 N 个子任务、LLMCompiler 并行执行、流式规划三种情况的时间，以及加速比的上下界。

```latex
T^{R}=\sum_{i=1}^{N}\left(T_{P}^{R}(P_i)+T_{E}(E_i)\right),\qquad T^{C}=\sum_{i=1}^{N}T_{P}^{C}(P_i)+\max_{k\in 1,\dots,N}T_{E}(E_k),\qquad T^{SC}=\sum_{i=1}^{N}T_{P}^{C}(P_i)+T_{E}(E_N)
```

```latex
\gamma=\frac{T^{R}}{T^{C}}=\frac{\sum_{i=1}^{N}\left(T_{P}^{R}(P_i)+T_{E}(E_i)\right)}{\sum_{i=1}^{N}T_{P}^{C}(P_i)+\max_{k}T_{E}(E_k)},\qquad \gamma_{\max}\approx\frac{\sum_{i}T_{E}(E_i)}{\max_{k}T_{E}(E_k)}=N,\qquad \gamma_{\min}\approx 1
```

变量：N 个子任务；T\_P^R(P\_i)、T\_P^C(P\_i) 是 ReAct 或 LLMCompiler 的规划器生成第 i 个子任务的时间；T\_E(E\_i) 是执行第 i 个子任务的时间。γ\_max = N 要求执行时间远大于规划时间且各任务执行时间相同；γ\_min ≈ 1 是规划时间占主导的情形。

**Gim, Lee & Zhong (2024), Asynchronous LLM function calling (AsyncLM), Yale, arXiv:2412.07017v1（首页写 "under review"）, §6.3。** 同步、同步加并行执行、异步三种调用方式的延迟，以及 |F| 很大时的加速比。

```latex
L_{\mathrm{Sync}}(F)=\sum_{f\in F}G(f)+\sum_{f\in F}E(f),\qquad L_{\mathrm{SyncParallel}}(F)=\sum_{f\in F}G(f)+\max_{f\in F}E(f)
```

```latex
L_{\mathrm{Async}}(F)=\max_{f\in F}\Big(E(f)+\sum_{g\in\mathrm{pred}(f,F)}G(g)\Big),\qquad \mathrm{pred}(f,F)=\{g\in F\mid E(f)\le E(g)\},\qquad \frac{L_{\mathrm{Sync}}}{L_{\mathrm{Async}}}\approx 1+\frac{\overline{E}}{\overline{G}}
```

变量：F 是互不依赖的函数调用集合；G(f) 是生成第 f 个调用所需 token 的时间；E(f) 是执行时间；Ē、Ḡ 是平均执行时间和平均生成时间（定理 6.2，假设 E 服从正态分布、|F| 很大）。定理 6.1：L\_Async ≤ L\_SyncParallel < L\_Sync。

**Feng, Mao, Dutta & Gonzalez (2026), Concurrency without model changes (AsyncFC), UC Berkeley, arXiv:2605.15077v1, §4 与附录 B。** 异步函数调用的加速上限，以及实测节省时间的分解。

```latex
R=\frac{T_{\mathrm{LLM}}+T_{\mathrm{tool}}}{\max(T_{\mathrm{LLM}},\,T_{\mathrm{cp}})},\qquad R=\begin{cases}\dfrac{T_{\mathrm{LLM}}+T_{\mathrm{tool}}}{T_{\mathrm{cp}}}, & T_{\mathrm{cp}}\ge(1+\alpha)T_{\mathrm{LLM}}\\[6pt]\dfrac{T_{\mathrm{LLM}}+T_{\mathrm{tool}}}{(1+\alpha)T_{\mathrm{LLM}}}, & (1+\alpha)T_{\mathrm{LLM}}>T_{\mathrm{cp}}\end{cases}
```

```latex
T_{\mathrm{saving}}\triangleq \mathcal{S}(\mathcal{M})+\mathcal{S}(\mathcal{E})-\mathcal{D}(\mathcal{M}\cup\mathcal{E})=\Delta_{F\parallel F}+\Delta_{D\parallel E}
```

变量：T\_LLM 总解码时间；T\_tool 所有函数执行时间之和；T\_cp 关键路径上的函数执行时间之和；α 是异步执行给解码带来的额外时间比例；S(·) 是若干时间区间的总时长，D(·) 是合并后覆盖的墙钟时长；Δ\_{F∥F} 是函数之间并行省下的，Δ\_{D∥E} 是解码和执行重叠省下的。

### 2. 投机执行：期望时间 = 基线 − 命中率 × 省下的时间 + 开销

**Bai, Lv, Zheng, Lu & Shu (2026), SPORK, 清华大学、美团, arXiv:2607.03333v1, §2.2 与附录 A。** 每一轮工具调用的成本模型。

```latex
\mathrm{Ratio}=\frac{T_{\mathrm{base}}}{T_{\mathrm{base}}^{*}-\alpha\cdot t_{\mathrm{overlap}}+T_{\mathrm{oh}}},\qquad \mathrm{Ratio}\ge 1\ \Leftrightarrow\ \alpha\cdot t_{\mathrm{overlap}}\gtrsim T_{\mathrm{oh}},\qquad S_{\max}=\frac{T_{\mathrm{dec}}+T_{\mathrm{tool}}}{T_{\mathrm{dec}}}=\frac{1}{1-f_{\mathrm{tool}}}
```

```latex
T_{\mathrm{base}}=T_{\mathrm{dec}}+T_{\mathrm{tool}},\qquad T_{\mathrm{hit}}=T_{\mathrm{base}}-t_{\mathrm{overlap}},\qquad T_{\mathrm{miss}}=T_{\mathrm{base}}^{*}+T_{\mathrm{oh}},\qquad \mathbb{E}[T]=\alpha\,T_{\mathrm{hit}}+(1-\alpha)\,T_{\mathrm{miss}}
```

变量：T\_dec 主流解码时间；T\_tool 工具执行时间；α 投机被接受的轮次比例；t\_overlap 每次接受时藏在解码后面的工具时间；T\_oh 每轮的探测和作废开销；T\*\_base 用了前缀恢复后的实际解码时间；f\_tool = T\_tool / T\_base。论文自算：BrowseComp 上 f\_tool = 0.366，上限 1.58×。

**Ye, Ahuja, Liargkovas, Lu, Kaffes & Peng (2026), Speculative actions, Columbia, ICLR 2026 (oral), arXiv:2510.04371v2, §2、§5、附录 A 与 C。** 假设投机器延迟服从 Exp(α)，真实 API 调用延迟服从 Exp(β)，β < α；k 路并行投机至少一路正确的概率是 p(k)。

```latex
p(k)=1-(1-p)^{k},\qquad \frac{E[T_{\mathrm{s}}]}{E[T_{\mathrm{seq}}]}\xrightarrow{T\to\infty}1-\frac{p(k)}{1+p(k)}\cdot\frac{\alpha}{\alpha+\beta}
```

```latex
E[T_{\mathrm{seq}}]=\frac{T}{\beta},\qquad \mathbb{E}[(B-A)_{+}]=\frac{\alpha}{\beta(\alpha+\beta)},\qquad E[T_{\mathrm{s}}]=\frac{T}{\beta}-S_{T-1}\,\frac{\alpha}{\beta(\alpha+\beta)},\qquad S_n=p(k)(1+S_{n-2})+(1-p(k))S_{n-1}
```

深度投机（定理 7；延迟确定：真实 a、投机 b < a，每步猜对的概率 p）：

```latex
\frac{\mathbb{E}[T_{\mathrm{seq}}-T_{\mathrm{spec}}]}{\mathbb{E}[T_{\mathrm{seq}}]}=\frac{T-1}{T}\,p\left(1-\frac{b}{a}\right),\qquad T_{\mathrm{spec}}=aT+(T-1)\,p\,(b-a)
```

选择性投机（定理 4）：每步最优的并行分支数。

```latex
m_t^{\star}(\mathbf{p})\in\arg\max_{m\in\{0,\dots,k\}}\{q(m;\mathbf{p})\,\Delta_t-c\,m\},\qquad q(m;\mathbf{p})=1-\prod_{j=1}^{m}(1-p^{(j)}),\qquad \ell=r\,(a-b)
```

变量：T 步数；S\_n 前 n 轮的期望命中次数；A、B 是投机器和真实调用的延迟；q 命中概率；Δ\_t 继续价值；c 每条分支的成本权重；ℓ 每次命中的延迟收益。token 成本（定理 3、7）在第二节。

**Chen, Guo, Luk & Fan (2026), AOSpec, Imperial College London, arXiv:2608.00881v1, §3–4。**

```latex
T_{\mathrm{serial}}=\sum_i (D_i+T_i),\qquad \widehat{T}(c)=\frac{\sum_j K(c,o_j)\,T_j}{\sum_j K(c,o_j)},\qquad V_o(c)=p_\theta(c\mid H_t,a_t)\,\widehat{T}(c)
```

```latex
R_{j,i}=\sum_{k=j}^{i}D_k+\sum_{k=j}^{i-1}T_k,\qquad \text{hidden}\le\min(T_i,\,R_{j,i})
```

变量：D\_i 第 i 步模型生成时间；T\_i 执行时间；c 候选观察，K 相似度，T̂(c) 用历史执行估的工具时间；p\_θ 观察模型给候选的概率，V\_o 是"期望藏掉的工具时间"；R\_{j,i} 是在边界 j 提前发起第 i 步动作可用的跑道。

**Li, Ye, Choubey, Zhang & Wu (2026), Speculate with memory, Salesforce Research, arXiv:2607.12236v1, §2.1、§4.3。** 三类投机每步最多省的时间。

```latex
\text{Type 1: }\min(\ell_{\mathrm{env}},\ \ell_{\mathrm{LLM}}-\ell_{\mathrm{spec}}),\qquad \text{Type 2: }\min(\ell_{\mathrm{LLM}},\ \ell_{\mathrm{env}}-\ell_{\mathrm{spec}}),\qquad \text{Type 3: }\ell_{\mathrm{LLM}}+\ell_{\mathrm{env}}
```

变量：ℓ\_LLM 主模型推理延迟；ℓ\_env 环境响应延迟；ℓ\_spec 投机器延迟。

**Hua, Wan, Vadrevu, Nadel, Zhang & Wang (2025), Interactive speculative planning, Microsoft、Rutgers, ICLR 2025, arXiv:2410.00079v1, §4.1 式 (1)–(3)。** 以断点 B（近似 agent 与目标 agent 不一致的步）分段，每段取目标 agent 最晚完成的时间。

```latex
T_{\mathrm{total}}=\sum_{B_i\in B[:-1]}\max\{\mathrm{end\_time}(\mathcal{T},s_j)\mid B_i+1\le j\le B_{i+1}\}
```

```latex
T_{\mathrm{best}}=\sum_{i\in\{i \bmod k=0,\ i<n\}}\ \max_{i\le j<i+k}\mathrm{end\_time}(\mathcal{T},s_j),\qquad T_{\mathrm{worst}}=\sum_{0<i<n-1}\left(\mathrm{time}(\mathcal{T},s_i)+e(s_i)\right)
```

变量：n 步数；k 一次最多连续投机的步数；time(𝒯, s\_i) 目标 agent 生成第 i 步的时间；e(s\_i) 执行时间；end\_time 由论文表 1 的递推定义（从上一个断点起累加）。最坏情况退化为顺序执行。

**Guan, Lan, Sun, Ding, Acharya, Wang, Wang & Hua (2026), Dynamic speculative agent planning, ICLR 2026, arXiv:2509.01920v3, §4.3、§5.1。** 投机深度 k = max(1, k̂ + β)，k̂ 是预测值、β 是用户设的偏置；时间指标 ΔTime = (1/N) Σ\_i (1 − T\_i^SP / T\_i^seq) × 100%。

### 3. 每一步时间的分解和调度

**Zhang, Wo, Wang, Sun, Zhang, Yuan, Li, Hu, Zomaya & Yang (2026), SpecBox, 北京航空航天大学等, arXiv:2607.23933v2, 式 (1)。**

```latex
T_{\mathrm{step}}^{(N)}=T_{\mathrm{context}}^{(N)}+T_{\mathrm{generation}}^{(N)}+T_{\mathrm{env\_prep}}^{(N)}+T_{\mathrm{data\_io}}^{(N)}+T_{\mathrm{sandbox\_exec}}^{(N)}
```

前两项是模型（读上下文、生成），后三项是运行时（沙箱准备、数据传输、工具执行）。

**Luo et al. (2026), Agentix, UC Berkeley 等, NSDI 2026, §3、§4.2。** 单线程程序的端到端延迟 = 排队等待 + 模型执行 + 被工具或人打断的等待（文字定义）。调度用"已获得服务"做优先级：

```latex
p(c_j)=\sum_{k<j,\ c_k.\mathrm{id}=c_j.\mathrm{id}}t_k,\qquad p(c_j)=\begin{cases}0 & c_j\ \text{is root}\\ \max_{c_k\in P(c_j)}\{p(c_k)+t_k\} & \text{otherwise}\end{cases},\qquad \frac{W_{\mathrm{total}}}{T_{\mathrm{total}}}\ge\beta
```

第一式是单线程程序的累计服务时间（PLAS），第二式是多线程程序的关键路径估计（ATLAS），第三式是防饥饿条件：等待与服务之比超过 β 就升到最高优先队列。

**Zhu, Jacob, Ma, Pan, Wang, Krishnamurthy & Kasikci (2026), TraceLab, University of Washington, arXiv:2606.30560v2, §5.4、§6.3。** 从客户端时间戳反推解码速度和 TTFT。

```latex
s_{\mathrm{norm}}=\frac{O}{t_{\mathrm{last}}-t_{\mathrm{input}}},\qquad s_{\mathrm{pure\_decode}}=\frac{O_{\mathrm{visible}}}{t_{\mathrm{visible}}-t_{\mathrm{reason}}},\qquad \hat{\ell}_{\mathrm{pure\_decode}}=\frac{\sum(t_{\mathrm{visible}}-t_{\mathrm{reason}})}{\sum O_{\mathrm{visible}}}
```

```latex
\widehat{\mathrm{TTFT}}=(t_{\mathrm{reason}}-t_{\mathrm{input}})-O_{\mathrm{reason}}\,\hat{\ell}_{\mathrm{pure\_decode}},\qquad R=\max(0,\ T_{\mathrm{e2e}}-T_{\mathrm{int}})
```

变量：O 输出 token 数；t\_input 最后一个输入事件的时间戳；t\_last 最后一个模型输出的时间戳；O\_reason 推理 token 数；R 是工具调用的账外开销（端到端跨度减去 runner 报告的内部执行时间）。

**Winston, Wang, Mirhoseini & Kozyrakis (2026), Agent JIT compilation, Stanford, ICML 2026, arXiv:2605.21470v2, §3.3、§5.1。** 用缓存的每个页面元素的延迟分布做蒙特卡洛估计，比较串行、对冲、并行三种执行策略。

```latex
S(U)=\sum_{e\in U}\sum_{i=1}^{\mathrm{count}(e)}\mathrm{sample}(\mathcal{D}_e),\qquad \ell_{\mathrm{serial}}=S(U_\sigma),\qquad \ell_{\mathrm{hedge}}=\min_{w=1}^{n}S(U_\sigma)+\delta_h,\qquad \ell_{\mathrm{parallel}}=S(U_\sigma^{\mathrm{seq}})+\max_{w=1}^{n}S_w(U_{\sigma,w})+\delta_p
```

```latex
\mathrm{Pass}@t=1-\left(1-F(t)\cdot p\right)^{n_{\mathrm{parallel}}}
```

变量：e 页面元素，count(e) 预计的交互次数，𝒟\_e 学到的延迟分布；δ\_h、δ\_p 对冲和并行的开销；F(t) 延迟的累积分布，p 生成有效计划的基础概率，Pass@t 是延迟预算 t 内拿到有效计划的概率。

**Dong, Qian, Zhan, Peng, Li & Li (2026), Why are GUI agents correct but late? (AAPT), arXiv:2607.28399（AAAI 2027 模板，录用未确认）, §3.1 式 (1)。** 预编译策略树要覆盖的时间和树的深度。

```latex
T_{\mathrm{cover}}\ge L_{p95}+M,\qquad n\approx\left\lceil T_{\mathrm{cover}}/\mathbb{E}[\Delta t]\right\rceil
```

L\_p95 规划器端到端延迟的 95 分位；M 安全余量（实验中 500 ms）；E\[Δt\] 期望的状态转移时长。

**Liu, Qiu, Goiri, Fonseca, Bianchini & Choukse (2026), Agentic coding in the wild (GitHub Copilot), UIUC、Microsoft Azure Research, arXiv:2608.00101v1, §9.2。** 用户空闲时间的生存函数，用来决定何时回收资源。

```latex
S(t)=\Pr(\mathrm{idle}>t),\qquad S(t\mid \mathrm{idle}>t_0)=\frac{S(t)}{S(t_0)}
```

**Artificial Analysis 方法页（第三方测量，读于 2026-09-28）。** TTFT = 发出请求到收到第一个 token；输出速度 = 第一个 token 之后每秒收到的 token 数；"100 个输出 token 的总响应时间"由二者合成，页面只说 synthetically based on TTFT and Output Speed，加法形式是我们按定义写出的：

```latex
T_{100}=\mathrm{TTFT}+\frac{100}{\mathrm{OutputSpeed}}
```

**Yu, Jeong, Kim, Kim & Chun (2022), Orca, OSDI 2022（经 InferCept 的引用找到的原文）。** serving 论文常用的归一化延迟 = 每个请求的端到端延迟 ÷ 它生成的 token 数，取中位数；vLLM（Kwon et al., SOSP 2023）用同一定义但取平均数。文字定义，无式子。

## 二、成本的公式：token 和美元

所有写出美元成本的文献都是同一个式子：各类 token 数 × 对应单价再相加。差别只在把 token 分成几类（输入/输出；缓存命中/未命中；投机 agent/目标 agent），以及有没有除以成功率。

### 1. 成本 = token × 单价

**Erol, El, Suzgun, Yuksekgonul & Zou (2025), Cost-of-Pass: An economic framework for evaluating language models, Stanford, arXiv:2504.13359（经 Efficient Agents 的引用找到的原文；v1 式 (3) 和附录 B 式 (14)，v2 为式 (2) 和 (13)）。**

```latex
v(m,p)=\frac{C_m(p)}{R_m(p)},\qquad c_m(p)=n_{\mathrm{in}}(m,p)\,c_{\mathrm{in}}(m)+n_{\mathrm{out}}(m,p)\,c_{\mathrm{out}}(m)
```

v(m,p) 是模型 m 在问题 p 上"得到一个正确答案的期望花费"；C\_m(p) 一次尝试的期望成本；R\_m(p) 一次答对的概率；n 是输入/输出 token 数，c 是单价。Wang et al. (2025, OPPO), Efficient agents, §2.2 原样采用。这就是我们第 8 页"每次尝试 vs 每次成功"那一行的正式定义。

**Chen, Zaharia & Zou (2023), FrugalGPT, Stanford, TMLR 2024, arXiv:2305.05176v1, §2–3。** 单次调用的价、预算约束下的目标、级联路由的目标。

```latex
c_i(p)\triangleq \tilde{c}_{i,2}\,\|f_i(p)\|+\tilde{c}_{i,1}\,\|p\|+\tilde{c}_{i,0},\qquad \max_{s}\ \mathbb{E}_{(q,a)}[r(a,\hat{a}(s,q))]\quad\text{s.t.}\quad \mathbb{E}_{(q,a)}[c(s,q)]\le b
```

```latex
\max_{\mathbf{L},\boldsymbol{\tau}}\ \mathbb{E}[r(a,f_{L_z}(q))]\quad\text{s.t.}\quad \mathbb{E}\Big[\sum_{i=1}^{z}\tilde{c}_{L_i,2}\|f_{L_i}(q)\|+\tilde{c}_{L_i,1}\|q\|+\tilde{c}_{L_i,0}\Big]\le b
```

c̃\_{i,0} 每次调用的固定费，c̃\_{i,1} 输入单价，c̃\_{i,2} 输出单价；‖p‖ 提示长度，‖f\_i(p)‖ 回答长度；b 预算；级联里 z 是停下来的那个 API 的序号。

**Li, Hu, Wang, Liu & Liu (2025), WebRouter, arXiv:2510.11221v1（首页写 under review at ICASSP 2026）, §3 式 (2)(3)(6)。**

```latex
C(\mathbf{q}_i,\mathcal{M}_t)=n_p\,c_p^{(t)}+n_c\,c_c^{(t)},\qquad s_i^{(t)}=P(\mathbf{q}_i,\mathcal{M}_t)\times S_{\mathrm{cost}}\big(C_i^{(t)}\big),\qquad U(c)=e^{-c}
```

n\_p、n\_c 提示和补全 token 数，c 对应单价；P ∈ {0,1} 任务成功；S\_cost 是 U(c) 在各模型间 min-max 归一化后的分。路由器的训练损失（式 (6)）在 VIB 损失上加一项 λ · E\[Σ\_t p\_φ(y\_t|z\_i) · C(M\_t)\]，C(M\_t) 是模型 t 的单位 token 成本。

**Xu et al. (2026), TokenPilot, 浙江大学等, arXiv:2606.17016v1, 式 (1)(2)(11)。**

```latex
\max_{\mathcal{M}}\ \frac{\sum_{m\in\mathcal{C}'}\hat{U}(m\mid\mathcal{C}')}{\mathcal{K}(\mathcal{C}')},\qquad \mathcal{K}(\mathcal{C}')=\alpha\,|\mathcal{C}'_{hit}|+|\mathcal{C}'_{miss}|,\qquad \mathrm{Cost}=|\mathcal{C}'_{hit}|\,p_{hit}+|\mathcal{C}'_{miss}|\,p_{miss}+\mathcal{H}_{out}\,p_{out}
```

α ≪ 1 是缓存命中 token 的折扣；实验取 GPT-5.4-mini 官方价 p\_hit = $0.075、p\_miss = $0.75、p\_out = $4.50 每百万 token。

**Huang, Wang, Wang, Jurayj, Jiménez Gutiérrez, Khashabi & Andrews (2026), SpeedRunner, Johns Hopkins, arXiv:2608.11338v1, 附录 A.3。**

```latex
\mathrm{cost}=p_{\mathrm{in}}\,N_{\mathrm{uncached\_in}}+p_{\mathrm{cache}}\,N_{\mathrm{cached\_in}}+p_{\mathrm{out}}\,N_{\mathrm{out}}
```

token 数是一个 episode 里所有调用之和，含分摊的技能归纳调用；价格同上（GPT-5.4-mini，2026-05-06）。

**Kerboua et al. (2026), FocusAgent, ServiceNow Research 等, TMLR, arXiv:2510.03204v2, 附录 H.1 式 (1)。** 用小模型先裁剪观察，什么时候比直接喂大模型便宜。

```latex
C_S\,|o_i|+C_L\,|o_r|\le C_L\,|o_i|\ \Rightarrow\ \alpha\le\frac{C_L-C_S}{C_L},\qquad |o_r|=\alpha\,|o_i|,\qquad \alpha\le\frac{2-0.4}{2}=0.8
```

C\_S、C\_L 是小/大模型每百万 token 的价（GPT-4.1-mini $0.4，GPT-4.1 $2）；至少裁掉 20% 才不亏。

**Guan et al. (2026), Dynamic speculative agent planning, ICLR 2026, §5.1 式 (5)–(9)。** 投机执行的钱分成近似 agent 和目标 agent 两笔。

```latex
PC_i^{SP}=ap_i^{SP}\,\mathrm{cost}_{ap}+tp_i^{SP}\,\mathrm{cost}_{tp},\qquad GC_i^{SP}=ag_i^{SP}\,\mathrm{cost}_{ag}+tg_i^{SP}\,\mathrm{cost}_{tg},\qquad \Delta\mathrm{Cost}=\frac{1}{N}\sum_{i=1}^{N}\left(\frac{PC_i^{SP}+GC_i^{SP}}{PC_i^{seq}+GC_i^{seq}}-1\right)\times 100\%
```

ap/tp 是近似/目标 agent 的提示 token，ag/tg 是生成 token；seq 是顺序执行的基线。

**Li et al. (2026), Speculate with memory, §4.3。** 每次投机的净额外成本 k · C\_S + (1 − acc) · C\_act：k 个并行投机器各一次调用，猜错时多付一次主模型调用。

**Ye et al. (2026), Speculative actions, 定理 3 与 7。** 投机多花的 token（假设单位时间的 token 数和每 token 单价固定）：

```latex
\frac{\mathbb{E}[M_{\mathrm{spec}}-M_{\mathrm{seq}}]}{\mathbb{E}[M_{\mathrm{seq}}]}\xrightarrow{T\to\infty}\tilde{k}-\Big(\tilde{k}+\frac{\alpha}{\alpha+\beta}\Big)\frac{p(k)}{1+p(k)}\quad\text{(breadth)},\qquad \frac{\mathbb{E}[M_{\mathrm{spec}}-M_{\mathrm{seq}}]}{\mathbb{E}[M_{\mathrm{seq}}]}\approx\frac{T-1}{T}\Big((1-p)\big(\tfrac{a}{2b}-\tfrac12\big)+p\Big)\quad\text{(depth)}
```

k̃ 是 k 条分支里不同动作的个数；其余变量同第一节。

**Hua et al. (2025), Interactive speculative planning, §4.2 式 (4)–(6)、(10)。** 两个断点之间的 token（含浪费的）、最好和最坏情况。

```latex
T_{B_i}=\sum_{j=B_i+1}^{B_{i+1}}\big(\mathrm{token}(\mathcal{A},s_j)+\mathrm{token}(\mathcal{T},s_j)\big)+\sum_{j=B_{i+1}+1}^{M_i}\big(\mathrm{token}(\mathcal{A},s_j)+\mathrm{token}(\mathcal{T},s_j)\big)
```

```latex
\text{best: }\sum_{0<i<n-1}\big(\mathrm{token}(\mathcal{A},s_i)+\mathrm{token}(\mathcal{T},s_i)\big),\qquad \text{worst: }\sum_{i=0}^{n-1}\big((i \bmod k)+1\big)\big(\mathrm{token}(\mathcal{A},s_i)+\mathrm{token}(\mathcal{T},s_i)\big)
```

token(𝒜, s\_j)、token(𝒯, s\_j) 是近似/目标 agent 第 j 步的 token；M\_i 是近似 agent 多跑的浪费步数。

### 2. 带预算约束的目标函数

**Zhang, Xia, Zhang, Madrigal, Mallick, Kessler, Rühle & Rajmohan (2026), Budget-aware agentic routing (BoPO), Cambridge、Microsoft, arXiv:2602.21227v1, §3–4 式 (1)(2)(6)(9)。**

```latex
C(\tau)=\sum_{t=0}^{|\tau|-1}c(a_t),\qquad J_{\mathrm{soft}}(\theta)=\mathbb{E}_{\tau\sim\pi_\theta}\Big[\mathbb{I}(\mathrm{success}(\tau))-\lambda\sum_{t}c(a_t)\Big],\qquad \max_\pi\ \mathbb{E}[\mathbb{I}(\mathrm{success}(\tau))]\ \ \text{s.t.}\ \sum_t c(a_t)\le B_{\max}
```

```latex
\mathcal{C}_{\mathrm{norm}}(\tau,x)=\mathrm{clip}\Big(\frac{C(\tau)-C_{\min}(x)}{C_{\max}(x)-C_{\min}(x)+\epsilon},\,0,\,1\Big),\qquad b_t=B_{\max}-\sum_{i=0}^{t-1}c(a_i)
```

c(a\_t) 每步成本（实验里 = 大模型调用次数；美元按 GPT-4.1 $2/$8、GPT-4.1 mini $0.40/$1.60）；C\_min、C\_max 是两个静态基线的成本；b\_t 剩余预算，不够一次大模型调用就强制用小模型。

**Yang, Hou, Wei, Bao & Chang (2026), ARES, UC Santa Barbara、Accenture, arXiv:2603.07915v1, 式 (2)。**

```latex
\max_\theta\ \mathbb{E}\Big[\mathcal{V}(\tau,x)-\lambda\sum_{t=1}^{T}\mathrm{cost}(e_t)\Big],\qquad \mathrm{cost}(e_t)=\text{tokens generated at turn } t
```

e\_t 是第 t 轮选的推理努力档位；𝒱 任务成功验证函数。

**Winston et al. (2026), Agent JIT, §3.2。** 代码计划的静态成本估计：工具调用 cost += C\_tool · γ^d，LLM 调用 cost += C\_eval · γ^d，γ = 10 惩罚嵌套深度 d，取成本最小的有效计划。

**Zhai, Li & Wang (2026), Revisable by design, 复旦等, arXiv:2604.23283v1, 式 (2)。** 中途修改任务的代价 AdaptCost = C\_comp(ρ) + C\_waste(τ\_{k\*+1:n})：补偿动作的成本加上被丢弃步骤的沉没成本（抽象单位）。

### 3. token 数怎么随步数增长

**Yuan, Nayak, Kundu & Talati (2026), Agentic AI workload characteristics, UIUC、Gimlet Labs、Intel, arXiv:2605.26297v1, 式 (1)–(3)。**

```latex
C_{a,i}=|H_{a,i}|,\qquad z_{a,i}=(\theta_{a,i},\,m_{a,i},\,u_{a,i}),\qquad H_{a,i+1}=H_{a,i}\,\|\,\Phi(\theta_{a,i},\,m_{a,i},\,u_{a,i})\,\|\,o_{a,i}
```

H 是第 i 次调用前的累积上下文，C 是它的 token 长度；每次调用把（思考 θ、消息 m、工具调用 u）的 token 经模板 Φ 格式化后连同工具结果 o 接在后面。这条递推就是我们第 2 页平方项的来源：每步读的 token 是之前所有步的和。

**Wang, Qiao, Zhang, Zhuge, Zhang & Lu (2026), TRACE, 大连理工等, arXiv:2609.10297, 附录 A.2 式 (8)。** 每步的服务成本按 token 计：

```latex
L_t^{\mathrm{enc}}=k_c,\qquad L_t^{\mathrm{KV}}=T_t+k_h+k_c,\qquad |\mathrm{KV}_{\mathrm{visual}}|=\mathcal{O}(k_c+H\,k_h)
```

k\_c 当前帧的视觉 token 预算，k\_h 历史帧预算，H 保留的历史帧数，T\_t 第 t 步的前缀长度。

**Xu, Zhou, Wang, Feng & Xiao (2026), GUIPruner, 清华深圳等, arXiv:2602.23235v1, 式 (1)–(3)。** 历史截图的 token 预算和分配：

```latex
N_{\mathrm{budget}}=\lfloor T\times N_{\mathrm{orig}}\times\lambda\rfloor,\qquad N_{\mathrm{orig}}=\frac{HW}{P^{2}},\qquad w_k=\gamma+(1-\gamma)\frac{T-k}{T-1},\qquad n_k=N_{\mathrm{budget}}\frac{w_k}{\sum_{j=1}^{T}w_j},\qquad s_k=\sqrt{\frac{n_k}{N_{\mathrm{orig}}}}
```

T 时间窗帧数，λ 历史 token 保留比例，P 补丁大小，γ 最远帧的保留因子，s\_k 是第 k 帧的缩放系数。

## 三、效率指标的定义式

把准确率和成本或步数合成一个数的指标只有三个：WES（步数）、Cost-of-Pass（美元）、APGR/CPT（强模型调用比例）；其余都是压缩比。

**Abhyankar, Qi & Zhang (2026), OSWorld-Human, UC San Diego, MLSys 2026, arXiv:2506.16042v2, §5.1。**

```latex
\mathrm{WES}^{+}=\frac{1}{n}\sum_{t=1}^{n}r_t\cdot\frac{t_{\mathrm{human}}}{t_{\mathrm{agent}}},\qquad \mathrm{WES}=\mathrm{WES}^{+}\cdot\Big(1-\frac{\bar{t}_{\mathrm{fail}}}{S}\Big)
```

r\_t 成功指示；t\_human 人完成任务的最少步数；t\_agent agent 实际步数；t̄\_fail 失败任务的平均步数；S 步数上限。取值 0–1。

**Xing, Zhang, Xue, Chen, Yang & Xiao (2024), Understanding the weakness of LLM agents within a complex Android environment (AndroidArena), KDD 2024, arXiv:2402.06596（经 AutoDroid-V2 的引用找到）, §5.1。** RRR = L / L̂，标注动作序列长度 ÷ 实际执行长度，越高越高效。Wen et al. (2025), AutoDroid-V2, MobiSys 2025, §4.1 写作 n/k 采用。

**Erol et al. (2025), Cost-of-Pass**：v(m,p) = C\_m(p) / R\_m(p)，每个正确答案的期望花费（式子在第二节）。

**Ong, Almahairi, Wu, Chiang, Wu, Gonzalez, Kadous & Stoica (2024), RouteLLM, UC Berkeley、Anyscale、Canva, ICLR 2025, arXiv:2406.18665v4, §3.2 式 (4)–(7)。**

```latex
c(M_{R^\alpha})=\frac{1}{|\mathcal{Q}|}\sum_{q\in\mathcal{Q}}\mathbb{I}\{R^\alpha(q)=\mathcal{M}_{\mathrm{strong}}\},\qquad \mathrm{PGR}(M_{R^\alpha})=\frac{r(M_{R^\alpha})-r(M_w)}{r(M_s)-r(M_w)},\qquad \mathrm{APGR}(M_{R^\alpha})=\int_0^1\mathrm{PGR}(M_{R^\alpha})\,d\big(c(M_{R^\alpha})\big)
```

c 是路由到强模型的调用比例（成本的代理）；r 平均回答质量，M\_s、M\_w 强/弱模型；APGR 实际按 10 个比例点取平均；CPT(x%) 是达到 x% PGR 所需的最小强模型比例。附录 D 的混合单价：(95×10 + 264×30)/(95+264) ≈ $24.7 每百万 token（GPT-4 输入 95、输出 264 token 的均值）。

**Guan et al. (2026), Dynamic speculative agent planning, §5.1 式 (3)–(5)、(10)–(11)。** ΔTime、ΔP（提示 token）、ΔG（生成 token）、ΔCost 都是逐任务相对顺序基线的平均变化；平均峰值并发 MC̄ = (1/N) Σ MC\_i，平均投机步 K̄ = (1/M) Σ k\_i。

**压缩比类指标。** Kerboua et al. (2026), FocusAgent, §4.3：Pruning(o\_i) = 1 − |o\_r| / |o\_i|（token）。Enomoto, Obara, Zhang & Oyamada (2026), NEC, arXiv:2605.29397v1, §2.1：

```latex
\mathrm{RR}(\mathcal{R})=\frac{1}{|\mathcal{D}|}\sum_{d\in\mathcal{D}}\frac{|\mathcal{R}(H_s)|}{|H_s|}
```

按字符数计，H\_s 是第 s 步的 HTML 观察，R 是裁剪方法。Xiao, Gao, Peng & Xiong (2026), AgentDiet, 北京大学、字节跳动, FSE 2026, §4.2.4：Keep% = Σ l\_reduced / Σ l\_orig × 100，只在 l\_orig − l\_reduced > θ 时才替换（θ ∈ {0, 250, 500, 1000, 2000}）。SGLang、CacheScout：缓存命中率 = 缓存的 prompt token / 全部 prompt token。

**Chen, Sun, Bellucci & Jacucci (2026), SkillDroid, 附录 D。** 0-LLM 率 = 零次 LLM 调用完成的轮次比例；每轮 LLM 调用数 C\_LLM：纯回放 0，语义匹配加回放 1，全 LLM 执行 5–15；加速比 = L̄\_L1 / L̄\_L2。

## 四、推理服务系统里的公式

这一类的"成本"不是美元，是显存 × 时间：一个请求在等工具回来的时候占着 KV cache，或者被驱逐后要重算。

**Kang, Li, Xu, Yang, Chen, Wang, Chen, Krishna, Xu & Arora (2026), ThunderAgent, Georgia Tech、UIUC、CMU、Together AI, arXiv:2602.13692v3, §4.2–4.3 式 (2)(3)(6)–(9)。** 式 (2) 的"显存 × 时间"引自 Belady (1966), IBM Systems Journal 5(2) 的 space-time product，原文未核。

```latex
\mathrm{Cost}_x=\int_0^{t_x}M_x(t)\,dt,\qquad \mathrm{Cost}_{\mathrm{total}}\approx\mathrm{Cost}_{\mathrm{decode}}+\mathrm{Cost}_{\mathrm{prefill}}+\mathrm{Cost}_{\mathrm{recompute}}+\mathrm{Cost}_{\mathrm{unused}}+\mathrm{Cost}_{\mathrm{caching}}
```

```latex
C_{\mathrm{total}}<\sum_{p\in\mathcal{L},\,\tau=\mathrm{R}}c_p+\sum_{q\in\mathcal{L},\,\tau=\mathrm{A}}c_q\,f(t_q),\qquad \mathrm{Cost}_{\mathrm{recompute}}=\int_0^{t_{\mathrm{recompute}}}c_i(t)\,dt\propto c_i^{2},\qquad \min_{S}\sum_{i\in S}c_i^{2}\ \ \text{s.t.}\ \sum_{i\in S}c_i\ge\Delta C
```

M\_x(t) 过程 x 在 t 时刻的显存；c\_p 程序 p 的上下文长度；τ 阶段（R 推理，A 执行工具）；f(t) = 2^{−t} 时间衰减；C\_total 是 KV 池容量；重算成本随上下文长度平方增长，所以驱逐时选最短的（式 (8)(9) 只在 PDF 里读到，无 alt text）。

**Abhyankar, Qi & Zhang (2024), InferCept, UC San Diego, ICML 2024, arXiv:2402.01869v2, §3.2–4.3 式 (1)–(5)。** 请求被工具调用打断时，丢弃重算、保留、换出三种处理方式的"显存 × 时间"浪费。

```latex
\mathrm{WasteDiscard}_i^j=T_{fwd}(C_i^j)\,C_i^j\,M+T_{fwd}(C_i^j)\,C_{other}\,M,\qquad \mathrm{WastePreserve}_i^j=T_{INT}^j\,C_i\,M,\qquad \mathrm{WasteSwap}_i^j=2\,T_{swap}(C_i^j)\,C_{batch}\,M
```

```latex
\mathrm{WasteChunkD}_i^j=\frac{T_{fwd}(C_i^j)\,C_i^j\,M}{2}+n\,T_{fwd}\Big(\frac{C_i^j}{n}\Big)C_{other}\,M,\qquad \mathrm{Waste}_i^j=\min\big(\mathrm{WastePreserve}_i^j,\ \mathrm{WasteChunkD}_i^j\big)
```

C\_i^j 第 j 次打断时请求 i 的上下文 token 数；M 每 token 的 KV 显存；T\_fwd 一次前向的时间（离线测得）；T\_INT 打断时长；C\_other、C\_batch 同批其他请求的上下文之和；n 分块重算的块数。

**Li, He, Mang, Zhang, Mao, Chen, Zhou, Zhang, Cheung, Gonzalez & Stoica (2026), Continuum, UC Berkeley、Stanford、清华, PVLDB 20(1)（按 v7 页眉）, arXiv:2511.02230v7, §4.1。** 给 KV cache 设保留期限 τ 的代价和收益。

```latex
\mathrm{Cost}(\tau,r)=\frac{\mathrm{MemUsage}(r)}{\mathcal{M}}\,\tau,\qquad \mathrm{Benefit}(r)=\mathrm{CacheMissCost}(r)+\mathrm{OutofOrderCost}(r)
```

```latex
\mathrm{CacheMissCost}(r)=\frac{\mathrm{MemUsage}(r)\times\mathrm{PrefillReload}(r)}{\mathcal{M}},\qquad \mathrm{OutofOrderCost}(r)=\frac{\mathcal{T}}{\mathcal{M}}\times\mathrm{MemUsage}(r)\times\eta,\qquad \eta=-\mathrm{Corr}(k,\,N-k)
```

ℳ 活跃请求的平均显存；PrefillReload(r) 重算或从 CPU 回载的时间；𝒯 平均等待时间；η 是已服务轮数 k 与剩余轮数 N − k 的负相关（无记忆负载时 η = 0）。页面上系统名拼作 Continnum。

**Zheng et al. (2024), SGLang, NeurIPS 2024, arXiv:2312.07104v2, §3 与附录 A.3。** 缓存命中率 = 缓存的 prompt token / 全部 prompt token。定理 3.1：按前缀树的深度优先顺序调度，命中率最优（缓存 ≥ 最长请求）；证明中的下界：

```latex
C\ \ge\ \sum_{e\in\mathrm{edges}(T)}|e|,\qquad \text{hit rate}=1-\frac{C}{\sum_{r\in R}\text{prefill tokens of } r}
```

T 是批内请求的前缀树，|e| 是边 e 对应的 KV 大小，C 是 KV 计算量。

**Zhang, Kim, Feng, Du, Liu, Zhong, Ching, Jiang & Hu (2026), CacheScout, UC Santa Cruz、UW、UChicago, arXiv:2608.14624v1, 式 (1)(6)(8)(9)。**

```latex
\phi=\frac{\text{system prompts}+\text{tool definitions}+\text{skills}+\text{few-shot}}{\text{total prompt tokens}},\qquad \tilde{p}_{\mathrm{surv}}(a)=1-\frac{\min(E[a],E_{\max})}{E_{\max}}
```

```latex
\mathrm{Score}(b)=\big(\tilde{p}_{\mathrm{surv}}(a_b)+\delta\big)\cdot\big(e^{-\lambda\cdot\mathrm{age}(b)}+\delta\big)\cdot|b|
```

Score 读作"驱逐块 b 预计损失的 prefill 工作量"：复用概率 × 新近度 × 块的 token 数；E\[a\] 是执行图上到 agent a 的最小跳数，E\_max 预测视野；age(b) 上次访问以来的调度步数。

**Sui et al. (2026), PASTE, 上海交大、Microsoft Research 等, arXiv:2603.18897v3, §4.3。**

```latex
\mathrm{priority}(i)=\frac{\mathrm{ExposedToolGain}(i)}{\mathrm{LLMPressure}(i,\mathrm{load})}+\mathrm{Aging}(i),\qquad \mathrm{EnginePressure}(B)=\mathrm{DecodeLoad}(B)+\gamma\cdot\mathrm{KVLoad}(B)\in[P_{\mathrm{low}},P_{\mathrm{high}}]
```

ExposedToolGain 是现在放行这一轮能减少的"暴露在关键路径上的工具时间"；LLMPressure 含预计服务时间、队列、上下文长度和 KV 压力。

**Pan et al. (2025), KVFlow, NeurIPS 2025, arXiv:2507.07400v1, §3.1。** 下游 agent 的"距执行步数" = max(E1, E2) + 1（AND 依赖）或 min(E1, E2) + 1（OR 依赖），步数大的先驱逐。

**Luo et al. (2026), Agentix, §4.3。** 负载均衡：调用 ≤ 2048 token 走最空闲引擎，否则钉在程序所在引擎保 KV 缓存局部性；阈值按命中率统计选定。调度优先级式子在第一节。

## 五、厂商定价页的计费公式（读于 2026-09-28）

页面上只有价目表和倍率句子，下面的式子是把它们写成公式；标 calc. 的倍率是从价目行算出来的，页面没有写成句子。

**Anthropic（[定价页](https://platform.claude.com/docs/en/about-claude/pricing)、[prompt caching 页](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)、[fast mode 页](https://platform.claude.com/docs/en/build-with-claude/fast-mode)）**

```latex
C=10^{-6}\big(N_{\mathrm{in}}\,p_{\mathrm{in}}+N_{\mathrm{out}}\,p_{\mathrm{out}}+N_{w5m}\,p_{w5m}+N_{w1h}\,p_{w1h}+N_{\mathrm{hit}}\,p_{\mathrm{hit}}\big)
```

```latex
p_{w5m}=1.25\,p_{\mathrm{in}},\qquad p_{w1h}=2\,p_{\mathrm{in}},\qquad p_{\mathrm{hit}}=0.1\,p_{\mathrm{in}}\ (\text{Opus 5.5: }0.05;\ \text{Fable 5.1, Mythos 5.1: }0.025),\qquad p^{\mathrm{batch}}=0.5\,p,\qquad p^{\mathrm{fast}}=2\,p\ (\text{calc.}),\qquad p^{\mathrm{USonly}}=1.1\,p
```

- 价目（每百万 token，输入 / 输出 / 5 分钟缓存写 / 1 小时缓存写 / 缓存读）：Opus 5.5 $4 / $20 / $5 / $8 / $0.20；Sonnet 5 $2 / $10 / $2.50 / $4 / $0.20；Haiku 4.5 $1 / $5 / $1.25 / $2 / $0.10；Fable 5.1 $10 / $50 / $12.50 / $20 / $0.25。fast mode：Opus 5.5 $8 / $40，Opus 5 和 Opus 4.8 $10 / $50。
- 总输入 token = cache\_read\_input\_tokens + cache\_creation\_input\_tokens + input\_tokens，三类分开计费。缓存 5 分钟（默认）或 1 小时，从写或读它的那次请求开始计，每次命中免费续期；可缓存的最短前缀 512–4096 token 视模型而定。
- fast mode 的倍率叠加在缓存倍率和地域倍率之上（页面原话）；Claude 4.6 及以后 1M 上下文按标准价，无长文本加价。
- 图片 token（[Vision 页](https://platform.claude.com/docs/en/build-with-claude/vision)，经定价页的链接找到）：每 28×28 像素一个视觉 token，上限 1568（标准档）或 4784（Claude 4.7 及以后的高分辨率档），超过则等比缩小；1280×720 的截图 = 46 × 26 = 1,196 token（calc.）。声明 computer\_toolset\_20260801 每次请求约加 4,500 输入 token。

```latex
N_{\mathrm{image}}=\left\lceil\frac{\mathrm{width}}{28}\right\rceil\times\left\lceil\frac{\mathrm{height}}{28}\right\rceil
```

**OpenAI（[定价页](https://developers.openai.com/api/docs/pricing)）**

```latex
C=10^{-6}\big(N_{\mathrm{in}}\,p_{\mathrm{in}}+N_{\mathrm{cached}}\,p_{\mathrm{cached}}+N_{cw}\,p_{cw}+N_{\mathrm{out}}\,p_{\mathrm{out}}\big),\qquad p_{\mathrm{cached}}=0.1\,p_{\mathrm{in}},\qquad p_{cw}=1.25\,p_{\mathrm{in}}\ (\text{calc.})
```

```latex
p^{\mathrm{long}}_{\mathrm{in}}=2\,p^{\mathrm{short}}_{\mathrm{in}},\qquad p^{\mathrm{long}}_{\mathrm{out}}=1.5\,p^{\mathrm{short}}_{\mathrm{out}},\qquad p^{\mathrm{batch}}=0.5\,p,\qquad p^{\mathrm{fast}}=2\,p,\qquad p^{\mathrm{regional}}=1.1\,p\ (\text{calc. except regional})
```

- 价目（输入 / 缓存读 / 缓存写 / 输出）：gpt-6-astra $10 / $1 / $12.50 / $50；gpt-6-sol $2 / $0.20 / $2.50 / $10；gpt-6-luna $0.10 / $0.01 / $0.125 / $0.50。长文本的门槛定价页本身没写（我们此前从 changelog 记的是 272K，E192）。
- 工具：网页搜索 $10 每千次加 token 费；容器 $0.03 (1 GB) – $1.92 (64 GB) 每 20 分钟。

**Artificial Analysis 方法页：** 混合价 = (7 × 缓存命中价 + 2 × 输入价 + 1 × 输出价) / 10。

对我们 Part 1 的影响：第 7 页页首和第 8 页表里写的"a cached read costs 0.1×"是标准倍率，Opus 5.5 实际是 0.05×（$0.20 / $4），档案 E84 已记，页面上要补一句。

## 六、没有公式的文献

这些文献只报测量数字，成本和时间最多用一句话定义；以后找公式不用再翻。

| 类别 | 文献 | 它怎么说成本或时间 |
| --- | --- | --- |
| 基准和测量 | OSWorld 2.0 (XLANG Lab 2026)；OSWorld-Human 除 WES 外；Bian et al. 2025；AgentSysBench (Chang et al. 2026)；HAL (Kapoor et al. 2025)；AI agents that matter (Kapoor et al. 2025)；BrowserGym；Agentic test-time scaling (Lee et al. 2026)；Measuring agents in production (Pan et al. 2026)；UFO2；TraceLab 的成本部分；MAP | 文字："cost per task = 输入输出 token × 列价"；"total token count per task = 所有调用的 prompt + completion token"（Lee et al.）；"固定成本 = 优化费用均值，可变成本 = 每任务推理费用均值"（AI agents that matter 附录 B）；AgentSysBench 只有概念式 Y = Φ(W, S)；OSWorld 2.0 附录 A–H 未读到 |
| 加速系统，只报数 | Skim；DeltaBox；TClone；Cordon；Atomix（§4 后半和附录未读）；Ghost tool calls（附录未读）；Agentic plan caching；KVFlow 除步数外；Lumer et al. (PwC)；W&D；SpecBox 除式 (1) 外 | 加速比、成本降幅、TTFT 都是测量值；Lumer 的成本是"一个会话内所有 API 调用累加"，TTFT 是"发请求到收到第一个响应块" |
| 技能、记忆、流程固化 | Agent workflow memory；ASI 除步数上限外；SkillWeaver；AppAgentX；EchoPath；GPA（限流，未读）；ActionEngine（只有 O(N) vs O(1)）；SpeedRunner 除附录 A.3 外；Hajimiri et al.；WALT（目标 FailRate + StepCount + AgenticRatio，无权重） | 步数、token、美元都是表里的数；Hajimiri 的 token 是"actor 和所有辅助模块调用之和" |
| 观察裁剪、token 削减 | Prune4Web；SimpAgent（FLOPs 无公式）；GUI-KV（只有 KV 预算比 γ）；AQuaUI（只有 | tok\_comp |
| 模型与训练 | ComputerRL；StepWise；SPACE（只有块长上限和回合计数）；The danger of overthinking；Fara-7B（成本 = token × 价，文字）；Beyond browsing；AXIS (ACL 2025) | 成本按列价算，无式子；AXIS 的完成时间和成本只在表里 |
| 可靠性、回滚 | RAC；Safe to resume；Revisable by design 除 AdaptCost 外；WebOperator；SMC（只有 ℓ = K − j） | 时间和 token 是表里的数 |
| 非论文 | Gartner 两份新闻稿；OpenRouter 博客；xlang-ai 代码；Anthropic 博客（每张截图 1,000–1,800 token、200k 上下文不到 100 张截图，都是文字估计） | 未扫描或无公式 |

被可信度规则排除、未扫描的 4 篇：Agentic Compilation、PreAct、LOOP、Activity Frames。

## 七、来源：打开的页面和版本

每篇都用 arXiv HTML 页读，HTML 截断的用 PDF 补；有公式的都用第二次抽取核对过 LaTeX。"未读到"指两种方式都没拿到的部分。

| 文献 | 版本 / 日期 | 读到了什么 |
| --- | --- | --- |
| OSWorld-Human, Abhyankar, Qi & Zhang | 2506.16042v2, 2026-05-18 | 全文 |
| What limits agentic systems efficiency, Bian et al. | 2510.16276v1, 2025-10-18 | 全文含附录 A–G |
| AgentSysBench, Chang et al. | 2608.15127v1, 2026-08-15 | 全文（§6.2 后用 PDF） |
| ThunderAgent, Kang et al. | 2602.13692v3, 2026-06-30 | 式 (8)(9)、§5.1、附录 F 用 PDF；定理 F.1 未读全 |
| HAL, Kapoor et al. | 2510.11977v1, 2025-10-13 | 附录 A4–A10 未读到 |
| AI agents that matter, Kapoor et al. | 2407.01502v1, 2024-07-01 | 附录 E–I 未读到 |
| BrowserGym, Le Sellier De Chezelles et al. | 2412.05467v4, 2025-02-28 | 附录 D–H 未读到（含成本附录 F） |
| Agentic test-time scaling, Lee et al. | 2602.12276v2, 2026-08-14 | 附录 N–O 未读到 |
| Agentic coding in the wild (Copilot), Liu et al. | 2608.00101v1, 2026-07-30 | §8.3 后用 PDF，全文 |
| Measuring agents in production, Pan et al. | 2512.04123v4, 2026-06-04 | 附录 A–G 未读到（PDF 无文本） |
| Agent JIT, Winston et al. | 2605.21470v2, 2026-05-29 | §5.2 至附录 I 未读到 |
| Skim, Wong et al. | 2605.16565v2, 2026-05-19 | 全文 |
| OSWorld 2.0, XLANG Lab | 2606.29537v2, 2026-07-13 | 附录 A–H 未读到 |
| Agentic AI workload characteristics, Yuan et al. | 2605.26297v1, 2026-05-25 | 全文（§5 后用 PDF） |
| UFO2, Zhang et al. | 2504.14603v2（日期未显示） | 全文（§3.7 后用 PDF） |
| TraceLab, Zhu et al. | 2606.30560v2, 2026-06-30 | 全文（§7 后用 PDF） |
| SPORK, Bai et al. | 2607.03333v1, 2026-07-03 | §6 和附录 A–H 用 PDF |
| AOSpec, Chen et al. | 2608.00881v1（日期未显示） | 全文 |
| SkillDroid, Chen et al. | 2604.14872v1, 2026-04-16 | 全文 |
| Cordon, Chen et al. | 2606.17573v1, 2026-06-16 | 全文 |
| The danger of overthinking, Cuadron et al. | 2502.08235v1, 2025-02-12 | 全文 |
| WebOperator, Dihan et al. | 2512.12692v1（日期未显示） | 全文 |
| DeltaBox, Dong et al. | 2605.22781v2, 2026-06-08 | 全文 |
| Dynamic speculative agent planning, Guan et al. | 2509.01920v3, 2025-09-21 | 全文 |
| Interactive speculative planning, Hua et al. | 2410.00079v1, 2024-09-30 | 全文 |
| TClone, Huang et al. | 2605.17320v1, 2026-05-17 | 全文 |
| SpeedRunner, Huang et al. | 2608.11338v1, 2026-08-11 | 附录 A.3 用 PDF |
| FocusAgent, Kerboua et al. | 2510.03204v2（日期未显示） | 全文 |
| LLMCompiler, Kim et al. | 2312.04511v3, 2024-06-05 | 全文 |
| ComputerRL, Lai et al. | 2508.14040v2, 2025-10-21 | 全文 |
| Continuum, Li et al. | 2511.02230v7, 2026-09-08 | 全文；TTL 选择的闭式规则未抽到 |
| WebRouter, Li et al. | 2510.11221v1（日期未显示） | 全文 |
| Speculate with memory, Li et al. | 2607.12236v1（日期未显示） | 全文 |
| The complexity trap, Lindenbauer et al. | 2508.21433v3, 2025-10-27 | 全文（§5.2 后用 PDF） |
| Speculative macro commit, Liu et al. | 2609.03236v1（日期未显示） | 全文 |
| Don't break the cache, Lumer et al. | 2601.06007v2, 2026-01-31 | 全文 |
| Atomix, Mohammadi et al. | 2602.14849v2, 2026-05-29 | §4 后半、§5–6、附录 A–E 未读到 |
| Ghost tool calls, Mohammadi et al. | 2606.02483v1, 2026-06-01 | 附录 A–D 未读到 |
| KVFlow, Pan et al. | 2507.07400v1, 2025-07-10 | 全文 |
| WALT, Prabhu et al. | 2510.01524v1, 2025-10-01 | 全文 |
| PASTE, Sui et al. | 2603.18897v3, 2026-06-16 | 参考文献后的附录未查（PDF 限流） |
| Efficient agents, Wang et al. | 2508.02694v1, 2025-07-24 | 全文（附录用 PDF） |
| Agent workflow memory, Wang et al. | 2409.07429v1, 2024-09-11 | 全文（§3 后用 PDF） |
| ASI, Wang et al. | 2504.06821v2, 2025-08-29 | 附录 B 未确认 |
| StepWise, Wei et al. | 2604.27151v1（日期未显示） | 全文 |
| AutoDroid-V2, Wen et al. | 2412.18116v3（MobiSys 格式，日期未显示） | 全文 |
| AgentDiet, Xiao et al. | 2509.23586v2, 2026-03-15 | 全文（§4.2.5 后用 PDF） |
| ARES, Yang et al. | 2603.07915v1（日期未显示） | 全文（附录用 PDF） |
| SPACE, Yang et al. | 2609.02042v1, 2026-09-02 | 全文（§4 后用 PDF） |
| Speculative actions, Ye et al. | 2510.04371v2, 2026-04-23 | 全文（§3.1 后用 PDF） |
| Prune4Web, Zhang et al. | 2511.21398v1, 2025-11-26 | 全文（附录用 PDF） |
| Agentic plan caching, Zhang et al. | 2506.14852v2（日期未显示） | 全文（附录用 PDF） |
| CacheScout, Zhang et al. | 2608.14624v1（页眉写 2026-07-16） | 全文（§3.4 后用 PDF） |
| EchoPath, Zhao et al. | 2609.16635v1（日期未显示） | 全文 |
| GPA, Zhao et al. | 2604.01676v2 | 未读（arXiv 限流，HTML 和 PDF 都被拒） |
| ActionEngine, Zhong et al. | 2602.20502v1（日期未显示） | 全文 |
| AAPT, Dong et al. | 2607.28399（版本未显示） | 全文 |
| Observation reduction, Enomoto et al. | 2605.29397v1, 2026-05-28 | 全文 |
| AsyncFC, Feng et al. | 2605.15077v1（日期未显示） | 全文 |
| Signal-driven observation, Gaur & Lane | 2606.06708v2（日期未显示） | 全文 |
| AsyncLM, Gim, Lee & Zhong | 2412.07017v1, 2024-12-09 | 全文 |
| Budget-constrained study, Hajimiri et al. | 2606.15017（v2 或更新，v2 为 2026-08-30） | 全文 |
| GUI-KV, Huang et al. | 2510.00536v1（日期未显示） | 全文 |
| AppAgentX, Jiang et al. | 2503.02268v2（日期未显示） | 全文 |
| AQuaUI, Li et al. | 2605.19260v1, 2026-05-19 | 全文 |
| W&D, Lin et al. | 2602.07359v1, 2026-02-07 | 全文 |
| RAC, Perera et al. | 2605.03409（abs 页：v2, 2026-05-18） | 全文 |
| TRACE, Wang et al. | 2609.10297（版本未显示） | 全文 |
| Safe to resume, Wu et al. | 2608.29381v1, 2026-08-29 | 全文 |
| TokenPilot, Xu et al. | 2606.17016v1, 2026-06-15 | 全文 |
| GUIPruner, Xu et al. | 2602.23235v1, 2026-02-26 | 全文 |
| Revisable by design, Zhai, Li & Wang | 2604.23283v1, 2026-04-25 | 全文 |
| BoPO, Zhang et al. | 2602.21227v1, 2026-02-04 | 全文 |
| SpecBox, Zhang et al. | 2607.23933v2（日期未显示） | 全文 |
| SkillWeaver, Zheng et al. | 2504.07079v1, 2025-04-09 | 全文 |
| AgentOccam, Yang et al. | 2410.13825v2, 2025-05-24 | 全文 |
| RouteLLM, Ong et al. | 2406.18665v4, 2025-02-23 | 全文（附录 D 用 PDF） |
| FrugalGPT, Chen, Zaharia & Zou | 2305.05176v1, 2023-05-09 | 全文 |
| SimpAgent, Chen et al. | 2507.03730v1, 2025-07-04 | 全文（附录用 PDF） |
| InferCept, Abhyankar, Qi & Zhang | 2402.01869v2, 2024-05-30 | 全文 |
| SGLang, Zheng et al. | 2312.07104v2, 2024-06-06 | 全文（附录 A.3 用 PDF） |
| Beyond browsing, Song et al. | 2410.16464v3, 2025-06-16 | 全文 |
| Fara-7B, Awadallah et al. | 2511.19663v1, 2025-11-24 | 全文 |
| AXIS, Lu et al. | ACL 2025 PDF (aclanthology.org/2025.acl-long.381) | 全文 |
| Agentix, Luo et al. | NSDI 2026 PDF (usenix.org, nsdi26-luo.pdf) | 全文 |
| Cost-of-Pass, Erol et al.（顺引用找到） | 2504.13359 v1 2025-04-17 和 v2 2026-02-26 | 相关章节 |
| AndroidArena, Xing et al.（顺引用找到） | 2402.06596（最新版，KDD 2024） | 相关章节 |
| Orca, Yu et al.（顺引用找到） | OSDI 2022 PDF (usenix.org) | 相关章节 |
| vLLM, Kwon et al.（顺引用找到） | 2309.06180v1, 2023-09-12 | 相关章节 |
| Belady (1966), IBM Systems Journal（ThunderAgent 引用） | — | 未核，无公开版 |
| Artificial Analysis 方法页 | 读于 2026-09-28 | 全页 |
| Anthropic 定价、prompt caching、fast mode、Vision 页 | 读于 2026-09-28 | 全页 |
| OpenAI 定价页 | 读于 2026-09-28 | 全页；Flex 价行未确认 |
| Anthropic 博客 Best practices for computer and browser use | 2026-05-13，读于 2026-09-28 | 全页 |
