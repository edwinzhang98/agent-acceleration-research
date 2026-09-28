# Part 2 of the deck: acceleration work classified by the Part 1 term it changes

**Date:** 2026-09-28 · **Session:** Claude Code (Opus 5.5), Edwin away; defaults agreed before he left · **Deck:** `slides/build_deck.py` → `slides/agent-acceleration.html`, Part 2 pages t01–t14, references t15–, appendix B0–B10 · **Builds on:** `research/2026-09-28-problem-definition.md` (Part 1’s formulas and symbols, D157–D160).

**Task (Edwin, 2026-09-28):** classify the existing acceleration literature by which term or variable of the Part 1 formulas it changes, or which structure it removes (e.g. the N² term); every variable traces back to Part 1; new formulas only where needed and carefully cited; no hallucination; strict, traceable review; we classify, we do not invent methods.

**Method.**
1. A read-only workflow (`wf_eae7c559`, 28 Sep 2026) listed the works from the Chinese doc《Agent 加速：别人做到哪了》, dossier v3 §3 and `slides/references.md` (146 candidates).
2. It re-read each primary source in 22 parallel groups: 156 source checks, each recording the URL and version read, the figures with their location, a confirmed / corrected / could-not-read verdict, the mechanism and the term it changes, the authors and venue, and any formula.
3. A synthesis step classified the works by term and drafted a page plan.
4. Only numbers with a confirmed or corrected verdict are used, with corrected values replacing the recorded ones.
5. This session mapped the plan to Part 1’s final notation, wrote the pages, and re-read the record behind every main-page number before using it.

The full records are kept verbatim in `research/2026-09-28-part2-source-checks.md` (provenance; quotes and locations for every number).

**Notation mapping (plan → deck):** passes → steps *i*, *N*; calls per pass c_k → *J_i*; prefill → t^prefill and n^unc; decode → n^out·TPOT; environment → *E_i*; overlap saving → T_saving; context growth → |H_a,i|, ḡ, N²; billing class → n^κ; machine hours → x_env c_env; price/tier → c_κ(μ_ij); success rate → R_m(p); cost per success → v(m,p). New in Part 2:
- *v_n(m,p) = C_setup/n + C_m(p)/R_m(p)* (page 14). **Adapted**: the fixed + variable cost split of Kapoor et al. (2025) §3 (in words) and LATM’s O(nc + C) (Table 2), added to Cost-of-Pass Eq. 2. The break-even *n > C_setup/(v_base − v)* is our algebra (calc.).
- The overlap bound on page 9 is AsyncFC’s Eq. 1 **verbatim**, with its symbol R written as “speed-up” to avoid a clash with R_m(p).
- The source formulas in Appendix B0 are **verbatim** in their own symbols, with their mapping onto Part 1 stated.

**Page map.**

| page | Part 1 term | family |
|---|---|---|
| 02 | all | the map |
| 03 | J_i → 0 | compile or replay the loop |
| 04 | N | more work per call, skills |
| 05 | t^queue, t^prefill | agent-aware serving (self-hosted) |
| 06 | \|o_a,i\| → t^prefill | observation reduction |
| 07 | n^out, TPOT | decoding |
| 08 | E_i | environment |
| 09 | T_saving | parallel and asynchronous calls |
| 10 | T_saving | speculation, and transactions for safety |
| 11 | ḡ, N² | context management |
| 12 | n^κ | caching |
| 13 | c_κ(μ_ij) | routing, small models, tiers |
| 14 | R_m(p), set-up | cost per success |

Appendix: B0 source formulas (3 pages), B1 compile or replay (research, products), B2 steps and stopping, B3 serving, B4 prefill, context and decoding, B5 environment and overlap, B6 prices by class and tier, B7 routing, B8 cost per success, B9 works held back or dropped, B10 gaps by term.

## 1. Verification table

One row per work whose numbers the deck uses. Verdict, location and numbers are from the source checks. “calc.” = our arithmetic; vendor = a vendor’s own statement, cited as such and never as a measurement. Quotes are in the source-check records.

| work | numbers used on the deck | verdict | location in the source | source read (28 Sep 2026) | label |
|---|---|---|---|---|---|
| JIT-Planner | 150.1 s/61% → 15.4 s/90%; 9.7×; 37 tasks, 18 author-written; 3 runs; set-up 25–90 + 25–45 min | corrected | v2 Table 1 p.5 (GPT-4.1 row); App. D p.13; App. H p.17; §6 p.9 | https://arxiv.org/pdf/2605.21470v2 | primary |
| ActionEngine | 10.2→1.8 calls; 237→118 s; $0.71→$0.06; 66→95%; 106 tasks; input 62.3k→8.1k; ~2.5× from price (calc.) | confirmed | v1 Table 1 p.9, Table 2 p.10; §6.1 cost = tokens × list price | https://arxiv.org/pdf/2602.20502v1 | primary |
| AutoDroid-V2 | 669.2→46.3 s; uncached input 3,021→68; output 832→123; 43.9→54.4%; 158 tasks; $82.42/app (calc.) | confirmed | v3 §4.3 Fig. 4a; Table 2 p.10; Table 4; offline costs text | https://arxiv.org/pdf/2412.18116v3 | primary |
| EchoPath | 586,386→20,370 tokens; 315.7→127.5 s; 91.8→91.2%; 159-task pool; ~572k tokens, ~4.5 min first pass; 11/50 false accepts; −96.5%/−59.6% (calc.) | confirmed | v1 Table 1 p.8; p.8 text; Table 3 p.10 | https://arxiv.org/pdf/2609.16635v1 | primary |
| AXIS | 3.2→2.0 steps; 59.5→29.9 s; $0.4→$0.2; 52→84%; 50 tasks; UI actions 103→48; $0.77→$0.24 per success (calc.) | confirmed | ACL 2025 Table 1 §5.2 p.7716; Table 2 | https://aclanthology.org/2025.acl-long.381.pdf | primary |
| UFO2 | o1 16.0→6.6; GPT-4o 13.8→12.9 steps | corrected | arXiv v2 Table 5 §6.4 p.18 | https://arxiv.org/pdf/2504.14603v2 | primary |
| OSWorld 2.0 | Opus 4.8 steps 190.5→103, tool calls 190.5→481.8, 18.5→20.6%, ~$76.1→~$72.4; 108 tasks; 3 s pause; ×2.5 calls, $411→$351 per success (calc.) | confirmed | v2 Table 3 §3.2 p.8; §3.1 | https://arxiv.org/abs/2606.29537 | primary |
| SPACE | 20.9→4.4 rounds; 81.3→96.9% | corrected | v1 Table 1 p.7 (Qwen3-4B unseen, Multi-action GRPO column) | https://arxiv.org/pdf/2609.02042v1 | primary |
| CUA-Verse | 23.4→40.2%; steps 39.6→28.6; 244 tasks | corrected | v1 §4.2 p.6 (OSWorld GUI vs GUI+CLI) | https://arxiv.org/pdf/2609.05374v1 | primary |
| OSWorld-Human | 1.35×–2.93× (calc.) | confirmed | v2 Table 4 §4 | https://arxiv.org/abs/2506.16042 | primary |
| ASI | 5.6→5.0 steps (−10.7%, calc.); 32.7→40.4%; 812 tasks | corrected | v2 Table 1 p.5 | arXiv:2504.06821v2 (29 Aug 2025, latest; PDF header 'Published as a conference p | primary |
| WALT | 8.9→7.0 steps; 57.5→64.1%; 234 tasks | corrected | v1 Table 2 p.8; §4.2–4.3 | arXiv:2510.01524v1 (1 Oct 2025; the only arXiv version; its PDF header reads 'Pr | primary |
| SpeedRunner | Crafter LLM calls −94%; 3 seeds | confirmed | v1 App. G.2; §4.3 | https://arxiv.org/pdf/2608.11338v1 | primary |
| Hajimiri et al. | 44.78%/73.6K vs 41.02%/107.3K; 655 tasks; 3 runs | corrected (v2 replaces v1) | v2 Table 1 p.6 | arXiv:2606.15017v2 PDF (30 Aug 2026), converted with pdftotext -layout: Tables 1 | primary |
| AWM | 5.9 vs 5.6 steps (ASI re-run) | corrected | ASI v2 Table 1 p.5 | https://raw.githubusercontent.com/mlresearch/v267/main/assets/wang25bx/wang25bx.pdf | primary |
| Beyond Browsing | $0.1→$1.4; 8.4→8.5 steps; 14.8→38.9%; $0.68 vs $3.60 per success (calc.) | corrected | ACL Findings Table 2 p.11072; Table 7 App. A.4 p.11082 | https://arxiv.org/pdf/2410.16464v3 | primary |
| Agentix | up to 15× vs vLLM; 2–5× vs vLLM-opt | confirmed | NSDI'26 abstract; §6.3 | https://www.usenix.org/system/files/nsdi26-luo.pdf | primary |
| Continuum | 1.12–3.66× lower delay (trace replay) | confirmed | v7 §1, §6.1 | https://arxiv.org/pdf/2511.02230v7 | primary |
| InferCept | 1.6–2× load; 1.25× 13B single GPU; 37–40% recompute | corrected | ICML'24 abstract; §5.1; §3.2 | https://proceedings.mlr.press/v235/abhyankar24a.html | primary |
| ThunderAgent | 1.48–3.58× (text); 1.24× panel f (calc.); env 4.8→0.3 s | corrected | v3 §5.2; Fig. 4 labels; Fig. 6a | https://arxiv.org/pdf/2602.13692v3 | primary |
| FocusAgent | −19%, 53.6→51.5%, 2.5→10.1 s per step (4.1-mini); −30%, 53.2% (5-mini); 330 episodes | corrected | v2 Table 2 §4.4; App. D Table 11 | https://arxiv.org/pdf/2510.03204v2 | primary |
| GEPA pruning (Enomoto) | 65.7→30.2 s (2.2×); 84% retained; 33 tasks | corrected | v1 abstract; §4.2; Fig. 4 caption | https://arxiv.org/pdf/2605.29397v1 | primary |
| Prune4Web | 25–50× fewer candidates; 46.8→88.28% | corrected | v1 abstract/§1; Table 2 | https://arxiv.org/pdf/2511.21398v1 | primary |
| Aguvis | 1,196 vs ~4,000 tokens/step (−70%); 22.1→27.1%; 104 tasks | corrected | v2 §4.4 p.7; Table 4; App. D.3 | https://arxiv.org/pdf/2609.02309v1 | primary |
| AgentOccam | +33% tokens/step, +45% steps (calc.); 16.5→43.1% | corrected | v2 Tables 2, 4, 5 | https://arxiv.org/pdf/2410.13825v2 | primary |
| Ares | 21,424→11,723 (−45%); 45.0→46.5%; −7.6 pp (calc.); ~129 tasks (calc.) | confirmed | v1 Table 1 p.7; §4.2 | https://arxiv.org/pdf/2603.07915v1 | primary |
| Overthinking | $1,400/29.1% vs $800/27.3% | corrected | v1 §1 p.2; §5.6 | https://arxiv.org/pdf/2502.08235v1 | primary |
| GUI-G1 | ~107→~38 tokens; 87.5→90.3% | confirmed | Table 4; App. D.2 Table 7 (NeurIPS Table 10) | https://arxiv.org/pdf/2505.15810v2 | primary |
| ToolSpec | 3.5–4.2× | corrected | v2 §5.2 Table 3 | https://arxiv.org/pdf/2604.13519v2 | primary |
| Anthropic fast mode | up to 2.5× OTPS; 2× price (calc.); cache invalidation on speed switch | confirmed | Fast-mode docs; pricing page; prompt-caching docs | https://platform.claude.com/docs/en/build-with-claude/fast-mode | vendor |
| OpenAI Fast/Flex/Batch | Fast up to 2.5× at 2×; Flex/Batch 0.5×; Batch ≤24 h | corrected | Changelog 30 Jul and 5 Aug 2026; Fast-mode guide FAQ; pricing tables; Batch guide | https://developers.openai.com/api/docs/changelog | vendor |
| Anthropic effort guidance | medium ≈ half the output tokens of high; parity only with retries (vendor) | confirmed | Blog 13 May 2026, "Claude 4.6 models" subsection | https://claude.com/blog/best-practices-for-computer-and-browser-use-with-claude | vendor |
| Skim | 1.9× lower cost; −33.4% latency; E17: 4.7 s vs 6.6 s, 66.7%, 151 tasks | corrected | v2 abstract; §2.2; §4 | https://arxiv.org/pdf/2605.16565v2 | primary |
| ToolCaching | 16.2→10.7 s at hit 0.514; 500 examples | corrected | v1 §6.4 Table 4 | https://arxiv.org/html/2601.15335v1 | primary |
| Browserbase price | $0.10–0.12 per browser hour above plan | corrected (vendor primary) | Pricing page, read 28 Sep 2026 | https://www.browserbase.com/blog/stagehand-caching | vendor |
| LLMCompiler | 20.47→5.47 s (3.74×); −73% (calc.); 72.47→77.13%; 20,000→2,800 tokens; WebShop 5.98→10.48 s | confirmed | v3 Table 1 p.6; Table 2; Table 3 | arXiv:2312.04511v3 PDF (5 Jun 2024), which carries the ICML 2024 / PMLR 235 head | primary |
| W&D | 1,522.6→904.2 s; $102.5→$65.7; 66→68%; $1.55→$0.97 per correct (calc.) | confirmed | v1 §3.2 p.4; Table 1 | https://arxiv.org/abs/2602.07359 | primary |
| AsyncFC | 1.44×, 1.21×; 47.6→44.3%; 300 tasks | corrected | v1 SWE-bench Lite result (Fig./text §5) | https://arxiv.org/html/2605.15077v1 | primary |
| SPORK (page 10 after review) | p50 34.7→31.2 s (−10%); p95 131.9→108.1 s (−18%); EM within 1 pp; 165 tasks; baseline already n-gram speculative decoding | confirmed | v1 abstract; §6.2–6.3 | https://arxiv.org/pdf/2607.03333v1 | primary |
| ParaGUI | 46.4 vs 33.5%; 38.7 vs 75.9 steps; 38.7 vs 36.7 (Seed-1.8); 233 tasks | confirmed | v1 Table III | https://arxiv.org/pdf/2607.22689v1 | primary |
| Speculative Actions | −19.5% time; 54.7% accuracy; ≤50% under Prop. 1 | confirmed | v2 §3.1.2 Fig. 2; §2 Prop. 1 | https://arxiv.org/pdf/2510.04371v2 | primary |
| ISP | 182.70→105.42 s (−42.3%); $0.2160→$0.2973; 117 tasks; SD 421.49 | confirmed | ICLR'25 §4.1 Table 2 | https://proceedings.iclr.cc/paper_files/paper/2025/file/25458943db16e0f78f748ca5bc34fff6-Paper-Conference.pdf | primary |
| DSP | −37.09% at +62.99% cost; 312 tasks | corrected | v3 Table 4 / ICLR App. A.3 Table 3 | https://proceedings.iclr.cc/paper_files/paper/2026/file/0d1986a61e30e5fa408c81216a616e20-Paper-Conference.pdf | primary |
| SMC | 27.60→22.47 s; 2,285 tasks (calc.); 355.7→195.9 s; −2/168; 3 GPUs vs 1 | confirmed | v1 Table 1 §4.2; §4.1 | https://arxiv.org/pdf/2609.03236v1 | primary |
| Ghost Tool Calls | p50 −5.4%; p99 11.56→14.22 s; calls 4.03 vs 1.03; 0.97 vs 0.97 | confirmed | v1 Table 14 App. B.9; Table 6 | https://arxiv.org/pdf/2606.02483v1 | primary |
| Atomix | 0/500 vs 400/500, 200/500; 300/500; 57% vs 53%, 0–7%; ~1 ms at K=16 | corrected | v2 Table 2 §3.4; §3.2 Table 6; App. C.5 Table 17 | https://arxiv.org/pdf/2602.14849v2: | primary |
| Safe to Resume? | 90/96, 93/96; 40/1,735 | confirmed | v1 Table IV §VII; Table II §VI.C | https://arxiv.org/pdf/2608.29381v1 | primary |
| WebOperator | ~37% | confirmed | v1 §4.4 Fig. 5 | https://arxiv.org/pdf/2512.12692v1 | primary |
| TClone | 18.2→3.7 s | corrected | v1 §2.3 Fig. 2a | https://arxiv.org/pdf/2605.17320v1 | primary |
| DeltaBox | 1.86 ms fast-path rollback | corrected | v2 Table 2 / abstract (PDF, not the abs page) | https://arxiv.org/pdf/2605.22781v2: | primary |
| Observation masking | $1.29→$0.61; 53.4→54.8%; 500 instances; summary +15% N | corrected | v3 Table 1 §4; §4.4 | https://arxiv.org/pdf/2508.21433v3 | primary |
| AgentDiet | −39.9 to −59.7% input; −21.1 to −35.9% cost; −1 to +2 pp | confirmed | v2 Table 4; §5.2.1 | https://arxiv.org/pdf/2509.23586v2 | primary |
| TokenPilot | $8.31→$3.22; $81.52→$10.58; 38.7→79.2%; +0.5/+2.1, −1.4/−2.6; $4.22→$2.79; 26.7M→8.6M | confirmed | v2 Tables 1–4; §4.4 | https://arxiv.org/html/2606.17016v2 | primary |
| Vendor cache prices | 0.02×, 0.05×, 0.1×, 0.25×; Fable 5.1 / Mythos 5.1 0.025×; writes 1.25×/2×; Google storage $0.50/1M/h; OpenAI 1.35× vs 2×, 2.15× vs 10× | corrected (OpenAI write) | Anthropic prompt-caching docs; OpenAI prompt-caching guide + pricing; DeepSeek, Google, xAI pricing pages (28 Sep 2026) | https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md | vendor |
| Don't Break the Cache | −41 to −80%; TTFT −6 to −31%; GPT-4o −8.8% (slower); 40 sessions | corrected | v2 Tables 1–2; §4.1 | https://arxiv.org/html/2601.06007v2 | primary |
| TraceLab | 12.8% (paper); 15.8% (dashboard) | corrected | v2 §7.5 Table 13; dashboard detail page (28 Sep 2026) | https://tracelab.cs.washington.edu | primary |
| StepWise | $0.881→$0.224; 58.1→55.4%; 6.4→4.1 s | corrected | v1 Table 1 p.6 | https://arxiv.org/pdf/2604.27151v1 | primary |
| WebRouter | $0.98→$0.12; 86.1→82.3%; 7.63→8.38 steps; ~14% slower | confirmed | v1 Table 1; Fig. 5b | https://arxiv.org/pdf/2510.11221v1 | primary |
| BoPO | −29.6% (calc.); 66.7→66.5%; 168 tasks | confirmed | v1 Table 1 | https://arxiv.org/pdf/2602.21227v1 | primary |
| Fara-7B | $0.913→$0.025; 38.0→16.5; 70.9→73.5%; 62%; 42.9→34.1% | confirmed | v1 Tables 9–10; App. A | https://arxiv.org/pdf/2511.19663v1 | primary |
| APC | −50.31%; 96.61%; −27.28% (one FinanceBench run) | corrected | v2 abstract; §4.3 Table 3 | https://arxiv.org/pdf/2506.14852v2 | primary |
| Google Priority / Microsoft priority | 1.8×; 1.75–2.5× (calc., tool-extracted) | confirmed | Gemini pricing page; Azure pricing HTML (not visually read) | https://ai.google.dev/gemini-api/docs/priority-inference | vendor |
| BATS | $4.47 vs $0.79 per success (calc.); 24.6 vs 12.6% | corrected | v2 Table 3; Table 9; Table 2 | arXiv:2511.17006v2 PDF (17 Aug 2026). v1 (21 Nov 2025) was compared and has the  | primary |
| AI Agents That Matter | 93.2%/$2.45 vs 88.0%/$134.50; 164 problems | confirmed | v1 Table A1 p.20 | arXiv:2407.01502v1 PDF (1 Jul 2024; the only arXiv version), converted with pdft | primary |
| IdleSpec | 50.5→55.6%; wall-clock ~same; +58% tokens (calc.) | corrected | v1 Table 1; App. B.3 Table 8; Table 3 | https://arxiv.org/pdf/2605.22154v1 | primary |
| App. B2: EET | $13.77→$6.18 run total; 33.2→41.0%; offline $4.3 | confirmed | ACL Findings Table 1; App. J Table 16 | https://arxiv.org/pdf/2601.05777v2 | primary |
| App. B2: Runaway | 19.0→13.4 steps; 76.1→70.2% | corrected | EMNLP Findings Table 1 | arXiv:2505.17616v2 PDF (22 Sep 2025), and the published ACL Anthology PDF 2025.f | primary |
| App. B2: Budget Tracker | −31.3% cost; 12.8 vs 12.6% | corrected | v2 Table 2 | arXiv:2511.17006v2 PDF (17 Aug 2026). v1 (21 Nov 2025) was compared and has the  | primary |
| App. B2: Efficient Agents | $0.398→$0.285; 53.33→51.52% | confirmed | v1 Table 7 p.8 | https://arxiv.org/pdf/2508.02694v1 | primary |
| App. B2: CoAct-1 | 53.07→59.93%; steps 10.15 vs 15.22 (different passed-task sets; budget ambiguous) | confirmed | v3 Table 1 p.7; Fig. 3a | https://arxiv.org/pdf/2508.03923v3 | primary |
| App. B2: ComputerRL | 11.2→26.2% (prompted GPT-4o) | confirmed | v2 Table 3 §4.3 | https://arxiv.org/pdf/2508.14040v2 | primary |
| App. B2: UFO2 multi-action | o1 OSWorld-W 6.80→3.30 on 10 tasks | corrected | v2 Table 7 §6.6 | https://arxiv.org/pdf/2504.14603v2 | primary |
| App. B1: AutoTool | LLM calls 24.1→20.4 (AlfWorld); 15–25% per text | corrected | AAAI Table 3 p.6 | https://arxiv.org/pdf/2511.14650v1 | primary |
| App. B1: EAM | AndroidWorld 34.5→52.6% (per-step latency benchmark unstated) | corrected | v1 Table 1 | https://arxiv.org/pdf/2605.12294v1 | primary |
| App. B1: UiPath | 3 Platform Units per heal | confirmed | Licensing page | docs.uipath.com, Agents user guide for Healing Agent (undated), fetched with cur | vendor |
| App. B3: SGLang | up to 6.4× throughput, 3.7× latency vs vLLM v0.2.5, Guidance, LMQL (which gives the maximum not stated) | confirmed | NeurIPS'24 §6.2 | https://arxiv.org/pdf/2312.07104v2 | primary |
| App. B4: Preble | 1.5–14.5× mean latency | confirmed | ICLR'25 abstract | https://arxiv.org/pdf/2407.00023v2 | primary |
| App. B4: Parrot | up to 11.7× (MetaGPT, LLaMA 13B) | confirmed | OSDI'24 §8.4 | https://www.usenix.org/system/files/osdi24-lin-chaofan.pdf | primary |
| App. B4: KVFlow | 1.24× vs HiCache; PEER 1.12×/1.08× | corrected | NeurIPS camera-ready §4.1, §4.2 | https://arxiv.org/pdf/2507.07400v1 | primary |
| App. B4: Helium | up to 1.56× vs KVFlow | corrected | v1 §7.1 Table 2 | https://arxiv.org/pdf/2603.16104v1 | primary |
| App. B4: KVCOMM | 7.82× TTFT at agent 5 (HF, approximate) | confirmed | v2 Table 2 | https://arxiv.org/pdf/2510.12872v2 | primary |
| App. B4: DroidSpeak | prefill 1.7–3.1× | corrected | NSDI'26 §5.2 | https://www.usenix.org/system/files/nsdi26-liu-yuhan.pdf | primary |
| App. B3: AsymCache | with Continuum 4.4–18.1% below Continuum alone; alone 0.4–4.2% below vLLM-LRU | corrected | v1 §6.5 Fig. 15 | https://arxiv.org/abs/2606.02964 | primary |
| App. B4: CacheBlend | TTFT 2.2–3.3× (RAG) | confirmed | EuroSys'25 §7.2 | https://arxiv.org/pdf/2405.16444v3 | primary |
| App. B5: LineRetriever | observation −61%; SR 52.7→44.8% (WorkArena L1) | confirmed | v1 Table 1 | https://arxiv.org/pdf/2507.00210v1 | primary |
| App. B5: SimpAgent | FLOPs 11.90→8.71 T | confirmed | ICCV Table 5 | https://arxiv.org/pdf/2507.03730v1 | primary |
| App. B5: ScreenSeekeR | 18.9→48.1% grounding | confirmed | v1 Table 4 p.8 | https://arxiv.org/pdf/2504.07981v1 | primary |
| App. B6: Think Twice | 3.2→2.6 s; 74.8→77.4%; slow-only 5.4 s; 1,272 samples | corrected | v1 App. A.2 Fig. 4 | https://arxiv.org/pdf/2503.06470v1 | primary |
| App. B6: Does CoT Help | 128-token cap 71.55% vs unlimited 70.41%, none 70.32% | corrected | Findings ACL Table 4 §4.4 | https://aclanthology.org/2026.findings-acl.392.pdf | primary |
| App. B6: TSDS | edge thinking 1,183→422; 0.719→0.714 | corrected | v3 App. G.4 Table 3 | https://arxiv.org/pdf/2607.26865v3 | primary |
| App. B6: GUI-KV | decode MFLOPs −38.9%; OSWorld 26.0→25.1% | corrected | v1 Table 2 §4.3; Table 1 | https://arxiv.org/pdf/2510.00536v1 | primary |
| App. B6: Agent-X | 1.61× on-device; 1,022 examples | confirmed | MobiSys §5.4 Fig. 18 | https://arxiv.org/pdf/2605.10380v1 | primary |
| App. B6: Ultrafast GDPval (vendor) | 7.7 min→83.0 s; non-inference 14.2→14.9 s; 6 tasks | corrected | Cerebras blog, 13 Aug 2026, chart | https://openai.com/index/previewing-ultrafast/ | vendor |
| App. B8: Speculate with Memory | analytical peak 1.128×; HotpotQA 1.05× | confirmed | v1 App. A.9; §4.3 | https://arxiv.org/pdf/2607.12236v1 | primary |
| App. B8: AgenticCache | TDW-COOK 12.86→1.75 h, $21.0→$4.4; TDW-MAT 1.86× (calc.) | confirmed | MLSys'26 Table 2 §5.3 | https://arxiv.org/pdf/2604.24039v1 | primary |
| App. B8: TPS-Bench | 42.0→34.8 s (−17.1%, calc.); 26.75→35.17% | corrected | ACL'26 Table 3 p.34956 | https://aclanthology.org/2026.acl-long.1614/ | primary |
| App. B8: spec. tool calls (Nichols) | 6–21% time saved (synthetic tool latency) | corrected | v1 Fig. 6 | https://arxiv.org/pdf/2512.15834v1 | primary |
| App. B8: AsyncLM | local 1.6–2.4× measured; cloud emulated | corrected | v1 Figs. 5–6 | arXiv:2412.07017v1 PDF (9 Dec 2024), the only version on the abs page on 28 Sep  | primary |
| App. B12: RouteLLM | 3.66× vs a random router (MT-Bench) | corrected | v4 §5.4 Table 6 | https://arxiv.org/pdf/2406.18665v4 | primary |
| App. B12: FrugalGPT | up to 98% (HEADLINES, single-query) | corrected | v1 Table 3 | https://arxiv.org/pdf/2406.18665v4 | primary |
| App. B12: FireAct | 9.0→2.7 s per trial (same GPT-3.5, fine-tuned) | corrected | v1 Table 3 p.6 | https://arxiv.org/pdf/2310.05915v1 | primary |

### 1b. Source formulas used in Appendix B0 (verbatim, own symbols)

| # | Work, location | Source form | Why show it |
|---|---|---|---|
| F1 | LLMCompiler, App. E.1 | T^R = Σ_{i=1..N} (T_P^R(P_i) + T_E(E_i)); T^C = Σ_i T_P^C(P_i) + max_k T_E(E_k); γ = T^R/T^C; γ_max ≈ Σ_i T_E(E_i) / max_k T_E(E_k) = N when executor time dominates and is equal. (Their N = number of planned tasks, not our passes.) | Serial vs parallel environment term |
| F2 | AsyncFC, Eq. 1 and App. B.2 | R = (T_LLM + T_tool) / max(T_LLM, T_cp). T_saving := S(M) + S(E) − D(M ∪ E) = Δ_F‖F + Δ_D‖E | Source of the deck's T_saving: parallel-tools plus decode–tool overlap |
| F3 | Speculative tool calls (Nichols et al.), §3.1.1 and §3.2.1 | S_spec = (G+T) / (α·max{G, g+T} + (1−α)(G+T)). Lemma 1: S_max < 2. Eq. 4: T_vanilla = 2Ko + ϕ·Σ X_i + δ·Σ(R_i + t_i) + Σ T_i, with X_{i+1} = X_i + t_i + t_{o,i} | Eq. 4 is the closest published source form of the whole Part 1 time sum: per-call overhead, growing prefill, decode and tool wait |
| F4 | SPORK, EQ1 and App. A | Ratio = T_base / (T*_base − α·t_overlap + T_oh); S_max = 1/(1 − f_tool) | Amdahl-style cap on overlap |
| F5 | Speculative Actions, Prop. 1 and Thm 3 | E[T_s]/E[T_seq] → 1 − (p(k)/(1+p(k)))·(α/(α+β)), p(k) = 1 − (1−p)^k; the extra-cost ratio → k̃ − (k̃ + α/(α+β))·p(k)/(1+p(k)) | Time saved and money paid from the same guess accuracy. Model-specific (exponential latencies) |
| F6 | Speculate with Memory, §2.1 and §4.3 | Saving per hit = min(ℓ_env, ℓ_LLM − ℓ_spec) for action speculation and min(ℓ_LLM, ℓ_env − ℓ_spec) for observation speculation; net extra cost = k·C_S + (1 − acc)·C_act | The saving per hit is capped by the idle window |
| F7 | ISP, §3, Eqs. 1–3 | Best case Σ over i with i mod k = 0 of max_{i≤j<i+k} end_time(T, s_j); worst case Σ_i (time(T, s_i) + e(s_i)) | Bounds for draft-and-verify |
| F8 | ParaGUI, §III-C | L_parallel = Σ_r max_k s_{r,k}; S = L_serial / L_parallel; P = L_total / L_parallel | Critical path vs total work (the machine-hours trade) |
| F9 | JIT-Scheduler, Alg. 2 | Hedge: ℓ = min_{w=1..n} S(U_σ) + δ_h. Parallel: ℓ = S(U_σ^seq) + max_w S_w(U_{σ,w}) + δ_p | Hedging as overlap bought with machines |
| F10 | TokenPilot, App. A.2 Eq. 11; SpeedRunner, App. A.3 | Cost = \|C′_hit\|·p_hit + \|C′_miss\|·p_miss + H_out·p_out (no write term); cost = p_in·N_in^uncached + p_cache·N_in^cached + p_out·N_out | Billing-class cost as papers actually compute it; both omit the write/store class |
| F11 | FocusAgent, App. H.1 | Cost-effective iff C_S·\|o_i\| + C_L·\|o_r\| ≤ C_L·\|o_i\|, i.e. α ≤ (C_L − C_S)/C_L | When a reader call pays off |
| F12 | LATM, Table 2 | O(nc + C) for LATM vs O(nC) for GPT-4 on every call | One-time expensive set-up amortized over n cheap runs |
| F13 | Continuum, Eqs. 1–2 | τ* = argmax_τ 𝒫(τ, f)·Benefit(r) − Cost(τ, r) | KV time-to-live across a tool wait |
| F14 | InferCept, Eqs. 1–5 | Waste_preserve = T_INT·C·M vs Waste_discard, Waste_swap; pick the minimum | Prefill-vs-memory trade during environment waits |
| F15 | AgentReuse, §3 | t = t_p + t_e (reuse removes t_p) | Minimal "skip the planning call" form. Its −93.12% is a modelled estimate |

Optional, flagged:
- AsyncLM Thm 6.2, L_Sync / L_Async ≈ 1 + E/G (cloud numbers emulated).
- AOSpec Eq. 5 runway, which hides up to min(T_i, R_{j,i}) [iii-pending].
- SpecHop Cor. 1, RelLat* = 1 − p(1−α)/(1+β) [iii-pending].
- PANDO Eq. 3 per-task identity C̄ = C_pre/\|B\| + … (credibility flagged).
- SpecBox Eq. 1, T_step = T_context + T_generation + T_env_prep + T_data_io + T_sandbox_exec [iii-pending].

---


### 1c. Gaps by term (Appendix B10)

- **N, c_k (compile/replay):**
  - No compiled or replayed method is tested against live application drift; EchoPath's only perturbation was a resolution change.
  - No vendor publishes a replay or heal success rate with a sample.
  - Set-up cost is excluded from every headline (JIT, EchoPath, AutoDroid-V2, WALT), so cost per success including amortization is never reported.
  - No work covers a multi-page enterprise form with a final submit.
- **Queueing:**
  - All measured gains are self-hosted throughput under load.
  - API priority tiers publish classes or targets, not measured latency.
  - No work measures the queueing share of API-agent task time.
- **Prefill:**
  - Part 1 has no term for the load time of cache-hit tokens, which DualPath and UNISON target; their evidence is pending or simulated.
  - Observation-reduction papers report per-step or per-call time, never task time with caching on.
  - The interaction between pruning and provider prefix caching is unmeasured in GUI agents.
- **Decode:**
  - Per-step effort routing can invalidate the provider message cache (Anthropic docs); no study measures the net effect.
  - No independent task-level measurement of fast tiers exists.
- **Environment:**
  - Only Skim (read-only) shrinks browser rendering and navigation.
  - No work reduces page-load or wait time for write-heavy web workflows.
  - Batched actions increase environment actions with unmeasured wall-clock.
- **Overlap:**
  - Speculation is evaluated on read-only, sandboxed or replayed tools. Several speed figures are analytical or trace-replay.
  - No live GUI-web speculation exists with side effects gated by a commit barrier.
  - No speculation paper reports cost per success.
- **Context growth:**
  - The retained methods lower the coefficient. Structural removal comes only from compiled plans or bounded windows.
  - No GUI study measures the N² token volume together with cache hit rates.
- **Money:**
  - No GUI or web agent paper reports tokens split by billing class, including writes and storage.
  - TraceLab covers coding agents only.
  - Environment machine hours are priced only by a vendor list price.
- **Price/tier:**
  - Router cost is excluded (BoPO) or not separated (WebRouter).
  - Small-model success losses are measured on public benchmarks, not on enterprise forms.
  - No routing study uses cached prices.
- **Success / cost per success:**
  - Almost no paper reports cost per success; our figures are calc.
  - No work reports all of time, money and success, with set-up included, on one benchmark.

---


### 1d. Works held back or dropped (Appendix B9)

**Not used: fail the credibility rule**
- Octopus v2: in-house set with no task count; qualitative mention allowed.
- GPA, SkillDroid: author-built suites; qualitative only.
- AgentServe: no task count, no venue.
- Stateful Inference (Norgren): single-author industry preprint, self-generated workloads.
- Cost-Aware Speculative Execution (Fareed): single author, no measurements. Proposed as a 5th "Not used" entry.
- Dynamic ReAct: no institution, internal suite.
- AdaGUI-R1: rejected at ICLR 2026, PDF unreadable, institutions unknown.
- speculative-tools GitHub repo: anonymous individual account, no measurements.

**Could not read or not found**
- OS-Catalyst: OpenReview challenge; anonymous submission.
- ToolSEE: not found.
- Self-Guide "+22%", VITA-VLA "−76%", "2,000–8,000 schema tokens": figures not in the sources.

**Off-topic or no term**
- SEAR, DREAM-Chunk: robotics.
- VITA-VLA, m2mKD: not LLM agents.
- SRMT: not an LLM.
- MemRefine: offline storage compression; no per-task term.
- DARE: non-agent math reasoning.
- Self-Guide: RL for success, no efficiency measure.

**Qualitative only (no usable number)**
- ECLAIR: counter-positioning; its 40% is teacher-forced.
- AgentRR, Signal-Driven Observation, SLMs position paper, LATM/DiLogics/ALLOY/Voyager/WebAgent (lineage), RAC, Revisable by Design (own benchmark, simulated tools), AAPT (own benchmark; external result a tie).
- Qwen-UI-Agent: no controlled step or time measurement.
- Log2Plan: unresolved table-vs-prose conflict.
- ConServe, TOPAS, SmoothAgent: condition (iii) not met.
- AAFLOW+: numbers are modelled.
- Vendor cache marketing: Stagehand percentages, Automation Anywhere 60%/"nearly 50%", HyperAgent "near-instant".
- Vendor move to smaller models.
- PEEK: fails (iii), and its "context map" does not remove growth.
- PANDO: institution only from e-mail domain; internal inconsistencies. Kept flagged in the appendix.

**Pending Edwin's decision on condition (iii) (no task count); held off the main pages**
- SpecHop, PASTE, AOSpec, TAB, CacheScout, DualPath (internal traces), PBKV, AgentKVShift, SpecBox, LLM-Tool Compiler, Cordon, GoClick, BAVT.
- DualSpec XBench row (its GAIA-Text-103 row passes).
- Continuum's real-run 8.18× (model not stated; the trace-replay range is used instead).
- Skim headline: "300+" tasks; shown with a flag.

**Numbers superseded by corrections and not used**
- SkillDroid 2.4×.
- AppAgentX "single run / model not recorded" (now GPT-4o, 2 runs; appendix only).
- Hajimiri v1 figures.
- KVFlow 1.83× (absent from the camera-ready body).
- AgentServe 2.8× attributed to SGLang (it is against llama.cpp).
- RouteLLM 3.66× described as "vs GPT-4".
- UFO2 "51.5% lower inference cost" (an author claim restating a step count).
- WALT "1.3–1.4× average" (a range across splits).
### 1e. Independent review of the pages (28 Sep 2026)

**Set-up.** Workflow `wf_202d4d4b` ran three reviewers: numbers against the source records; classification and formulas against Part 1; citations, credibility and wording. Each was followed by a verifier that re-checked every finding. Of 93 findings, 62 were confirmed, 28 partly confirmed (with the fix corrected), and 3 rejected. All 90 confirmed or partly confirmed findings were applied. The pages were then re-measured: all 67 pages fit, and main pages are 189–272 words (pages 03 and 10 are slightly over 250).

**High severity: a wrong number, direction or attribution, or an unsupported claim.**
1. B6: “other Claude models 0.1×” now also lists Fable 5.1 and Mythos 5.1 at 0.025×.
2. Page 12 title: the 87% is TokenPilot’s full system (placeholders + trimming + eviction). It now reads “41–80% against no caching; with trimming and eviction, by up to 87%”.
3. Page 3: JIT-Planner drafts plans in parallel calls, not one call.
4. Page 8: Skim’s “300+”-task headline is now flagged as condition (iii) pending.

**Classification changes.**
- SPORK moved from page 9 (independent calls) to page 10 (speculation). Page 9’s range became 31–73% and page 10’s 5–45%, both calc. from the rows. Ghost Tool Calls’ naive 5.4% is now inside the range.
- ThunderAgent’s environment-time cut (4.8 → 0.3 s) is sandbox preparation overlapped with waiting. It is therefore T_saving, not E_i, and moved from page 8 to B5.
- FireAct moved from B7 (cheaper model) to B4 (shorter prompt). Its price per token rises 8×.
- IdleSpec is marked as a counter case in B5: its tool-wait overlap buys accuracy, not time.

**Formula-strip marks corrected.**
- E_i is no longer marked unchanged on page 3.
- The ḡ ↓ mark is removed on page 6: FocusAgent prunes only the current page.
- Page 9: J_i is marked “↑ or ↓”.
- Page 10: the exchange is in calls and tokens, not in the price.
- Page 11: N² is marked “removed by a plan”, and the money exchange reads “hit → miss, write”.
- Page 12: the mark reads “unc → hit”.
- The time row now starts at i = 0, and its TTFT simplification is stated on page 2.

**Conditions added.**
- FocusAgent’s per-step latency is from 33 tasks with one seed.
- Don’t Break the Cache’s baseline is a forced no-cache run, on a web-search research agent.
- GUI-G1 compares two differently trained models.
- SMC: −40.4% of AppWorld’s −44.9% already comes from one-step guessing; actor and drafter models named.
- AgentDiet: 200 + 300 tasks from two benchmarks.
- The OSWorld 2.0 3-s pause is per action; whether it applies per batched call is not stated.
- Atomix, Safe to Resume? and Ghost Tool Calls use author-built test suites.
- Task counts not printed for ARES, Overthinking, StepWise and Fara-7B. These are listed in a new B9 row, “shown with a flag, pending the same decision”.

**Titles and claims brought in line with the rows.**
- Page 4: 38–46%, not “halves”.
- Page 8: “in one browser-agent study”, with the Browser-Use 73% counter-profile from Winston et al.
- Page 11: “only compiled plans are shown to remove the square”.
- Page 12: “cuts that input’s price by 75–98% (calc.)” replaces “the largest money lever”.
- Page 14: an actual case of a dearer attempt with a cheaper success (Beyond Browsing).
- Page 7: fast tiers labelled vendor.
- Page 9: T_saving is “small today” (as in Part 1), not ≈ 0.
- Page 9: the 2× cap now carries its condition T_cp = T_tool.
- Vendor marketing (Stagehand “~80%”, Automation Anywhere “over 60%”, the Cerebras chart) is no longer shown as a number.
- Gap lines narrowed where a record shows a measurement: a web-search agent’s billing split; set-up included, but only outside web or GUI.

**Appendix B0.** Symbols now explained where the verbatim formulas use them without saying: T*_base, L_serial, L_total, T_s, the limit “→”, C_act, and InferCept’s i and j. Also corrected: InferCept’s Eq. 5 minimum and AsyncFC’s equation location.

**Rejected.**
1. TokenPilot’s local eviction is correctly described.
2. SPORK’s break-even α·t_overlap ≥ T_oh is exact without its third design.
3. The 2× cap is our labelled arithmetic. It is kept, with its condition now stated.

## 2. D-ledger additions

(to follow)

## 3. E-ledger patches

(to follow)

## 4. Still open

(to follow)
