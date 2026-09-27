# Verification — P0 items 2–7 and P1 items 8–13, 13a–13f (dossier Part VIII §8.2)

**Date:** 2026-09-27 · **Scope:** §8.2 P0 items 2–7 and P1 items 8–13, 13a–13f (13a and 13b done first among P1). P0 item 1 is in `research/2026-09-27-verification-P0-item1.md` (D56). · **Dossier base:** `Agent-Acceleration-Consolidated-Dossier-v2-2026-09-26.md` at commit c18e2fe (1,015 lines; all line numbers below refer to it) · **New IDs:** D57–D94, E91–E93

**How this was done.** Primary sources were read through a web-fetch tool that extracts page text; `curl` to arXiv, OpenReview, LinkedIn and most hosts is refused by this environment's proxy (HTTP 403), as in the item-1 pass. Every quote was requested verbatim. Seven parallel checks each covered a group of items, and the lead re-fetched five load-bearing sources independently before merging: Gartner 25 Mar 2026 (the >90% and "not fully passed on" sentences), the OpenRouter blog of 30 Jun 2026 (15× per request, "right around February 1st", "early June"), FocusAgent v2 Table 2 (all six GPT-4.1 cells), EchoPath v1 Table 1 and its resolution-shift and code-link sentences, and the EchoPath GitHub link (404). All matched, apart from one EchoPath min–max bound noted in place. Figures, tables and PDF page layout were not inspected as images. Every "replace the fragment" patch in §3 was machine-checked to occur verbatim in v2, and every whole-row patch was checked to sit at the stated line.

**Verdict labels:** ✅ CONFIRMED · ⚠ CORRECTED / PARTIALLY CONFIRMED · ❌ CORRECTED (the dossier's figure or attribution is wrong) · ❓ UNRESOLVABLE (reason stated). "(calc.)" = computed here. "(inferred)" = reasoning, not a source statement.

### Verdict summary (one line per item; details in §1)

| Item | Dossier IDs | Verdict | What changes |
|---|---|---|---|
| P0-2 Cost of Dynamic Reasoning | E49, D35 | ⚠ PARTIALLY CONFIRMED | HPCA 2026 (HPCA-32) and all four figures confirmed in v2 (and v1). But 62.1–136.5× is HotpotQA, one request served alone, max-accuracy Reflexion/LATS on Llama-3.1-70B vs one ShareGPT inference, not "agentic vs chatbot" in general (D57). 71.0 = LLM calls. |
| P0-3 FocusAgent WorkArena | D15, E30 | ⚠ CORRECTED (resolved) | Configuration, not version: $45.1 / 51.5% = GPT-4.1-mini retriever; $38.1 / 53.2% = GPT-5-mini retriever, both in v2 Table 2. Dollars are input-token totals over 330 episodes. Dossier lines 262/398 mix the two (D58). |
| P0-4 Continuum, PASTE | D13, D14, E28 | ❌ CORRECTED | Continuum: not version drift. v7 still has ">8×" (real SWE-agent, "up to 8.18×") and 1.12–3.66× (trace replay) (D61); 144.9/93.4 is an RL-rollout microbenchmark (D62). PASTE: 48.5% (v1) and 43.5% / 55.4% (v3, "up to") confirmed; "1.25× vs ORION / 1.32× vs SpecFaaS" not found (v3: 1.71× / 1.83×) (D63); hardware and tool-share figures changed between versions (D64). |
| P0-5 TraceLab | D16, E19 | ❌ CORRECTED (resolved) | 119K/875/214 (all steps) and 126k/857/252 (Claude-only Table 8) are both in the paper. "Prefill amplification 5.3×" is in neither version; the paper says 3.8× with a different definition (D65–D67). |
| P0-6 Gartner | E55, E62, E73; Top-10 #10 | ⚠ CONFIRMED + CORRECTED | 17 Aug 2026 release confirmed (>5× per agentic workflow through 2028; no baseline year). The ">90% by 2030" is providers' cost for a 1T-parameter LLM, "not fully passed on to enterprise customers", not unit price (D68). E73 is "28% of AI use cases in I&O", fieldwork Nov–Dec 2025, release 7 Apr 2026 (D69). Client-only research notes ❓. |
| P0-7 OpenRouter | E57, E58, E59, D18; Top-10 #6 | ⚠ PARTIALLY CONFIRMED / ❓ | Primary confirms "right around February 1st" and "about 15x more per request". 14× / 2.8× and the 25,000% chart come from LinkedIn posts that cannot be fetched (secondary only). Cached share 70% vs >85% conflict (D71); 15× per request vs ≈5× aggregate (D70). "39%→66% Chinese share" has no source and conflicts with the primary (D72). |
| P1-13a EchoPath | Part III/V rows | ⚠ PARTIALLY CONFIRMED / CORRECTED | Token and time medians confirmed; Synapse baseline confirmed on the same model and scored **91.8%**, above EchoPath-Codex's 91.2%. EchoPath's range is 87.3–92.8%, not 91.2–92.8% (D82). "159" is a post-selection pool of active memories (D83). The only drift is a resolution shift; the lifecycle is not evaluated (D84). Code link 404 (D85). |
| P1-13b FocusAgent WebArena | D48 | ❌ CORRECTED | No sign flip. 32.3% (GPT-4.1-mini retriever) is unchanged v1→v2; 39.6% is the GPT-5-mini retriever added in v2 (D58, D60). |
| P1-8 HUMAN Security | E65 | ⚠ PARTIALLY CONFIRMED / ❓ | "Traffic from AI agents and agentic browsers grew 7,851% year over year" confirmed (vendor). Sample = >1 quadrillion interactions on HUMAN's own platform in 2025. Baseline, agent definition and base volume not published. First release 26 Mar 2026. |
| P1-9 2605.26297 / AgentRace | E29, D36 | ✅ CONFIRMED (numbers) / ⚠ title | 84.6–99.5% and 91.0–98.6% confirmed in v1. Title is "…Characteristics"; abs page lists no v2 (D73). AgentRace is a different, anonymous paper. |
| P1-10 Gemini | D28, E79 | ✅ D28 / ❌ E79 | Slug and model name correct (joint post, 21 Jul 2026). 3.8 Flash "~305 tok/s, fastest measured by AA" is beam.ai's wording; AA says ≈300 t/s at launch and 329.7 t/s, #2 of 211, when read 27 Sep (D74). Flash-Lite computer use is "Preview" (D75). |
| P1-11 Operator, Opus 4.8 | D29, D33, E39, E83 | ⚠ CORRECTED / ❓ | OpenAI notice 17 Jul 2025; the stated reason is integration into ChatGPT agent, and latency is never given as a reason. The 31 Aug 2025 date is secondary only (D76). The Opus 4.8 post covers instructions only; tool changes are a separate beta docs feature (D77). |
| P1-12 Temporal, LangChain | E70, E68, D24 | ✅ / ⚠ | Question behind 79.8%: "Is the cost of running AI agents a meaningful factor in your decision to use AI agents?"; the report's headline overstates it (D78). The LangChain page is dated 12 Jun 2026, but the report existed by Mar 2026 (≈Dec 2025, inferred). |
| P1-13 MAP | E69, D25; Top-10 #9 | ⚠ PARTIALLY CONFIRMED | 66% / 17% (N=53), 5/20 and "negligible" confirmed in v4. It says 15/20 "can operate asynchronously"; only 5/20 are background async processes (D80). 14.8% / 59.3% read in v2 with caption "N=27–29" (D79). Venue: ICML 2026 Oral, as "Characterizing Agents in Production" (D81). |
| P1-13c Ares, StepWise, AWO, WALT | D42, D45, D47, D49 | ✅ resolved / ❌ Ares C15, line 49 | All four D-entries were configuration mix-ups and are resolved row by row. Ares "16.4→17.2%" is not in the paper. New error at line 49: AWO's GPT-5.1 call counts are paired with Claude's times (D86). Ares token cuts differ by benchmark (D87). |
| P1-13d venues | D51 | ✅ / ⚠ / ❓ | Speculative Actions = ICLR 2026 **Oral** (D51 resolved; title differs, D90). AAPT has AAAI-27 formatting only; decisions are due 30 Nov 2026 (D88). SPACE "EMNLP 2026" has no primary support (D89). SMC "MLSP 2026" ❓ (program page needs JavaScript). |
| P1-13e Fara-7B, AXIS, ComputerRL | E90, D54 | ✅ / ❌ AXIS / ⚠ ComputerRL | Fara-7B priced at the cheapest OpenRouter Qwen-2.5-VL-7B rate ($0.2/$0.2 per M); 36.5× (calc.). The 62% vs 73.5% gap comes from the judge and protocol, not the harness (D91). AXIS's −65–70% is vs **manual human** work; vs a UI agent it is ≈2× (D92). ComputerRL "≤1/3 steps" is unquantified (D93); venue ICLR 2026 poster. |
| P1-13f KVCOMM, DroidSpeak, AgentReuse | Part III rows | ⚠ / ✅ / ⚠ | KVCOMM's abstract says "without quality degradation", but the body reports a <2.5% accuracy drop at 95% reuse (D94). DroidSpeak's "negligible" loss is measured on F1/Rouge-L/code similarity on non-agent datasets. AgentReuse figures confirmed; SMP2019 is a Chinese assistant-command set and the 93% reuse rests on 20 requests × 5 runs. |

### Effect on the §1.9 Top-10 (lines 223–234)

No ranked **number** changes value in this pass. The wording changes on three ranks (patches in §3):
- **Rank 6 (OpenRouter).** "≈15×" is tokens per request (primary). 14× / 2.8× come only from secondary reports of a LinkedIn post. The cached-share caveat becomes 70–85% (conflicting).
- **Rank 9 (MAP).** 14.8% and 20% / 1,340 stand. "15/20 run asynchronously" becomes "15 of 20 can operate asynchronously". The blocker question has N≈27 (caption "N=27–29").
- **Rank 10 (Gartner).** 5–30× confirmed. ">90% unit token cost" becomes providers' cost for a 1T-parameter LLM, "not fully passed on to enterprise customers". Adds the 17 Aug 2026 ">5× per agentic workflow through 2028".
- Ranks 1–5, 7 and 8 are outside this pass. The "not on a slide" paragraph (line 236) changes for E49, now verified but conditioned.

---

## 1. Verification table

### Sources checked and access notes (per group of items)

#### P0 items 2 and 5 — "The Cost of Dynamic Reasoning" (D35, E49); TraceLab (D16, E19)

| Label | Source | Version / date | How it was read |
|---|---|---|---|
| DR-abs | https://arxiv.org/abs/2506.04301 (Kim, Shin, Chung, Rhu; KAIST) | v1 4 Jun 2025; v2 7 Jan 2026 | Web fetch (submission history, Comments field) |
| DR-v2 | https://arxiv.org/html/2506.04301v2 and https://arxiv.org/pdf/2506.04301v2 | v2, 7 Jan 2026 | Web fetch of HTML (four passes) and PDF (one pass) |
| DR-v1 | https://arxiv.org/html/2506.04301v1 | v1, 4 Jun 2025 | Web fetch of HTML, to check version differences |
| HPCA-prog | https://2026.hpca-conf.org/program/program-hpca-2026/ and https://conf.researchr.org/track/hpca-2026/hpca-2026-main-conference | fetched 2026-09-27 | Web fetch (official conference site) |
| KAIST-VIA | https://sites.google.com/view/kaist-via/publications | fetched 2026-09-27 | Web fetch (authors' lab page; supporting only) |
| TL-abs | https://arxiv.org/abs/2606.30560 (Zhu, Jacob, Ma, Pan, Wang, Krishnamurthy, Kasikci) | v1 29 Jun 2026; v2 30 Jun 2026 | Web fetch |
| TL-v2 | https://arxiv.org/html/2606.30560v2 | v2, 30 Jun 2026 | Web fetch of HTML (six passes) |
| TL-v1 | https://arxiv.org/html/2606.30560v1 | v1, 29 Jun 2026 | Web fetch of HTML (one pass; same numbers as v2) |
| TL-site | https://tracelab.cs.washington.edu/ and https://tracelab.cs.washington.edu/exp/prefix_cache/redundant_prefill/ | fetched 2026-09-27; no "last updated" date shown | Web fetch (the authors' live dashboard, a growing dataset) |

**Access notes.** `curl` to arxiv.org is blocked by the environment proxy, so all text comes from a web-fetch tool that extracts page text. Every quote was requested verbatim. Key sentences came back identical across several fetches and, for DR, across the v2 HTML and v2 PDF. **Subsection labels are less reliable than the quotes.** For the Wikipedia 1.2 s sentence, the v2 PDF pass and one v2 HTML pass gave §IV-A, one v2 HTML pass gave §IV-B, and the v1 pass gave §III. I record §IV-A (two agreeing v2 passes). No figure was inspected as an image. IEEE Xplore (document 11408569, seen only as a search result) returned an empty page, and the IEEE CSDL table-of-contents page showed no entries. Wayback Machine is blocked in this environment, so earlier snapshots of the TraceLab dashboard could not be checked.

#### P0 item 3 and P1 item 13b — FocusAgent (D15, D48, D53, E30)

| Label | Source | Version / date | How it was read |
|---|---|---|---|
| v1 | https://arxiv.org/html/2510.03204v1 (Kerboua, Omidi Shayegan, Thakkar, Lù, Boisvert, Caccia, Espinas, Aussem, Eglin, Lacoste, "FocusAgent: Simple Yet Effective Ways of Trimming the Large Context of Web Agents") | arXiv v1, October 2025 (from the ID prefix 2510; exact day not retrieved) | Web fetch of the HTML (primary), 4 separate fetches |
| v2 | https://arxiv.org/html/2510.03204v2 | arXiv v2. The unversioned HTML (https://arxiv.org/html/2510.03204) is v2 and shows the stamp "arXiv:2510.03204v2 [cs.CL] 29 Aug 2026", so v2 is the latest version | Web fetch of the HTML (primary), 9 separate fetches |
| TMLR | https://jmlr.org/tmlr/papers/ (official TMLR accepted-papers list) | fetched 2026-09-27 | Web fetch |
| OpenReview | https://openreview.net/forum?id=mINaJKSy7A (located by web search) | not readable | Browser-verification page, then HTTP 403 on the forum, the PDF and the API |

**Access notes.**
- The arXiv **abs** pages (`/abs/2510.03204`, `…v1`, `…v2`) and the PDFs came back through the fetch tool as "PDF empty / no machine-readable text". export.arxiv.org and the arXiv API are blocked by robots.txt. So I could **not read the submission-history block**. That leaves two gaps: v1's exact date, and whether any version lies between v1 and v2. v3 does not exist as the latest version: the unversioned HTML resolves to v2. A fetch of `/html/2510.03204v3` was refused by the proxy (HTTP 429), so I could not test that URL directly.
- OpenReview blocked every request (browser check or 403). TMLR acceptance is confirmed from the official TMLR list at jmlr.org, **month only** ("August 2026"). The exact decision date is unresolved.
- The fetch tool extracts text with a small model. **One fetch refused to reproduce Table 1 in full on copyright grounds.** Every cell below was therefore collected through targeted per-row fact-check fetches. Each key cell ($55.6, $45.1, $38.1, 51.5, 53.2, 32.3, 39.6, $59.0, $44.0, $46.2) came back identical in **at least two independent fetches**. The one exception is the WebArena cost cells of Table 2, which one fetch returned in full and a second fetch returned for the 5-mini row only. The percentage annotations printed next to costs, such as "(-19%)", "(-30%)" and "(-21.7%)", came back only once each and are not relied on. I recomputed all such percentages below (calc.).

#### P0 item 4, P1 items 9 and 13f — Continuum, PASTE (D13, D14); 2605.26297 / AgentRace (D36); KVCOMM, DroidSpeak, AgentReuse

| Label | Source | Version / date | How read |
|---|---|---|---|
| CONT-abs | https://arxiv.org/abs/2511.02230 | history v1 4 Nov 2025; v2 20 Dec 2025; v3 30 Jan 2026; v4 4 May 2026; v5 11 May 2026; v6 25 May 2026; v7 8 Sep 2026 | WebFetch |
| CONT-v1/v2/v3/v4/v5/v6/v7 | https://arxiv.org/html/2511.02230vN | per version | WebFetch of HTML. v7 HTML is **truncated by the fetch tool before §6** (only headings visible), so v7 §6 / Table 5 could not be read; v6 §6 was readable |
| PASTE-abs | https://arxiv.org/abs/2603.18897 | v1 19 Mar 2026 (555 KB); v2 13 Jun 2026 (436 KB); v3 16 Jun 2026 (436 KB) | WebFetch |
| PASTE-v1 / v3 | https://arxiv.org/abs/2603.18897v1 ; https://arxiv.org/html/2603.18897v1 ; https://arxiv.org/html/2603.18897v3 | v1, v3 | WebFetch. **v2 HTML: HTTP 429 (rate-limited), not read** |
| AAWC | https://arxiv.org/abs/2605.26297 ; https://arxiv.org/html/2605.26297v1 | abs page lists **only v1, 25 May 2026** | WebFetch. **abs/2605.26297v2: HTTP 429, not read** |
| AgentRace | https://agent-race.github.io/ , /home ; OpenReview PDFs openreview.net/pdf/1996a013… and /pdf/ea7bb853… ; forum pages | fetched 2026-09-27 | project pages read; **both OpenReview PDFs HTTP 403; OpenReview forum pages show only a browser-verification wall** |
| KVCOMM | https://arxiv.org/abs/2510.12872 (v1 14 Oct 2025, v2 1 Nov 2025); https://arxiv.org/html/2510.12872v2 ; https://neurips.cc/virtual/2025/poster/115164 | v2 | WebFetch; main results table not reachable (fetch truncated) |
| DroidSpeak | https://www.usenix.org/conference/nsdi26/presentation/liu-yuhan ; https://arxiv.org/abs/2411.02820 (v1 5 Nov 2024 … v4 14 Jul 2025); https://arxiv.org/html/2411.02820v4 | NSDI 2026 page; arXiv v4 | WebFetch |
| AgentReuse | https://arxiv.org/abs/2512.21309 (v1 24 Dec 2025, v2 25 Dec 2025); https://arxiv.org/html/2512.21309v2 ; https://crad.ict.ac.cn/en/article/doi/10.7544/issn1000-1239.202440380 | arXiv v2; CRAD 61(11), 1 Nov 2024 | WebFetch |

**Access note.** All arXiv **PDF** URLs returned "empty / no machine-readable text" through the fetch tool, so every arXiv quote below is from the HTML rendering. Quotes were requested verbatim; where the fetch tool returned a paraphrase rather than a quote I say so ("fetch summary"). One fetch of Continuum v1 returned contradictory output (it listed "1.12" as NOT FOUND and then quoted a sentence containing it); a second, verbatim fetch of the whole v1 Introduction contains no numeric headline, so I rely on the second fetch and flag the conflict.

#### P0 items 6, 7 and P1 item 8 — Gartner (E55, E62, E73), OpenRouter (E57–E59, D18), HUMAN Security (E65)

| Label | Source | Date | How read |
|---|---|---|---|
| G-Aug | Gartner press release "Gartner Predicts AI Inference Costs Per Agentic Workflow Will Increase More Than Fivefold Through 2028", https://www.gartner.com/en/newsroom/press-releases/2026-08-17-gartner-predicts-ai-inference-costs-per-agentic-workflow-will-increase-more-than-fivefold-through-2028 | STAMFORD, Conn., August 17, 2026 | WebFetch, 3 passes (primary) |
| G-Mar | Gartner press release, 25 Mar 2026 (URL as in E62) | March 25, 2026 | WebFetch, 2 passes (primary) |
| G-Apr | Gartner press release "Gartner Says AI Projects in I&O Stall Ahead of Meaningful ROI Returns", https://www.gartner.com/en/newsroom/press-releases/2026-04-07-gartner-says-artificial-intelligence-projects-in-infrastructure-and-operations-stall-ahead-of-meaningful-roi-returns | STAMFORD, Conn., April 7, 2026 | WebFetch, 2 passes (primary) |
| OR-blog | OpenRouter, "DeepSeek V4 Is Earning Agentic Token Share", https://openrouter.ai/blog/insights/deepseek-v4-adoption/ | 6/30/2026 | WebFetch (primary) |
| OR-rank | https://openrouter.ai/rankings ; https://openrouter.ai/data ; OpenRouter blog posts of 27 Jun and 25 Aug 2026 | fetched 2026-09-27 | WebFetch (primary; live pages) |
| LI-1 | Peter Walker, LinkedIn, https://www.linkedin.com/feed/update/urn:li:activity:7493029883191681024/ (alt. slug URL `…/posts/peterjameswalker_february-6th-2026-potentially-the-last-share-7493029881841344512-IK89/`) | 11 Aug 2026 19:45 UTC (calc. from the activity ID's 41-bit timestamp) | **Not retrievable**: WebFetch refused ("URL is disallowed by robots.txt rules") for both URLs |
| LI-2 | Peter Walker, LinkedIn, https://www.linkedin.com/feed/update/urn:li:activity:7506103118410072064/ (cited by the-decoder for the 25,000% chart) | 16 Sep 2026 21:34 UTC (calc. from activity ID) | Not fetched (same robots block) |
| dec-14 | the-decoder, M. Bastian, "AI is becoming AI's biggest customer as agentic token usage jumps 14x on OpenRouter" | 23 Aug 2026 | WebFetch (secondary; quotes LI-1) |
| dec-25k | the-decoder, M. Bastian, "OpenRouter's staggering token chart is the AI bubble debate in a single image" | 17 Sep 2026 | WebFetch (secondary; cites LI-2) |
| ppc | ppc.land, "Agents burn 5x more tokens than humans as Zapier traffic drops" (reports a16z "Charts of the Week", M. Sternstein, 21 Aug 2026, charts credited to Peter Walker) | 21 Aug 2026 | WebFetch (secondary); the a16z newsletter itself was not located; a16z's X post was robots-blocked (search snippet only) |
| H-news | HUMAN Security newsroom, https://www.humansecurity.com/newsroom/2026-state-of-ai-traffic-cyberthreat-benchmark-report/ | NEW YORK, NY — March 26, 2026 | WebFetch, 2 passes (primary, vendor) |
| H-blog | HUMAN blog, J. Edwards, https://www.humansecurity.com/learn/blog/ai-traffic-growth-2025-key-findings/ | March 26, 2026 | WebFetch (primary, vendor) |
| H-land | Report landing page (URL in E65) | undated | WebFetch, 2 passes (primary, vendor) |
| H-GNW | GlobeNewswire release, https://www.globenewswire.com/news-release/2026/04/09/3270682/0/en/human-security-s-2026-state-of-ai-traffic-cyberthreat-benchmark-report-signals-a-new-internet-era-automation-growth-now-outpaces-humans.html | LONDON, April 09, 2026 | WebFetch, 2 passes (vendor's own release on a wire) |

**Access notes.** LinkedIn and X refused automated fetching (robots.txt), so the Walker posts (E58, and the chart behind the 25,000% figure) could not be read; figures attributed to them below rest on secondary reports and are marked so. WebFetch paraphrased when asked for full bodies; only sentences returned in quotation marks from targeted "quote verbatim" prompts are used as quotes below. The HUMAN report itself (PDF) was not found: the landing page shows headline stats and a "Request a Demo" button, no download form or PDF link was visible to the fetch tool.

#### P1 items 13a and 13c — EchoPath; Ares (D49), StepWise (D47), AWO (D45), WALT (D42)

| Label | Source | Version / date | How it was read |
|---|---|---|---|
| EP | https://arxiv.org/html/2609.16635v1 — Zhao, Shanmugham, Roy, Xu, "EchoPath: Execution-Level Replayable Memory for GUI Agents" | v1, 15 Sep 2026 (from the page's own line "arXiv:2609.16635v1 [cs.AI] 15 Sep 2026") | Web fetch of HTML, five separate fetches (primary) |
| EP-repo | https://github.com/JackZhao1998/EchoPath (URL printed in EP) | fetched 2026-09-27 | Web fetch (HTTP 404) + GitHub API repository search of user `JackZhao1998` |
| ARES | https://arxiv.org/html/2603.07915v1 — Yang, Hou, Wei, Bao, Chang, "Ares: Adaptive Reasoning Effort Selection for Efficient LLM Agents" | v1, 9 Mar 2026 (only version per abs page) | abs page + three HTML fetches (primary) |
| SW | https://arxiv.org/html/2604.27151v1 — Wei, Ni, Zhao, Gan, Cohan, "Step-level Optimization for Efficient Computer-use Agents" (StepWise) | v1, 29 Apr 2026 (only version per abs page) | abs page + two HTML fetches (primary) |
| AWO | https://arxiv.org/html/2601.22037v1 (and v2) — Abuzakuk, Kermarrec, Sharma, Veski, de Vos, "Optimizing Agentic Workflows using Meta-tools" | v1 29 Jan 2026; v2 2 Feb 2026 (both 1,269 KB) | abs page; v1 HTML four fetches (appendix tables read from v1); v2 HTML three fetches (appendix tables not visible — see access note) |
| WALT | https://arxiv.org/html/2510.01524v1 — Prabhu et al., "WALT: Web Agents that Learn Tools" | v1 (date not captured) | Two HTML fetches (primary) |

**Access notes (honest record).**
- `arxiv.org/abs/2609.16635` (and `…v1`) returned no extractable text through the fetch tool on two attempts, so EchoPath's submission history and Comments field were not read; the version/date come from the HTML page's own identifier line. A fetch of `arxiv.org/html/2609.16635v2` was **refused by the proxy (HTTP 429, rate-limited)** — whether a v2 exists is unchecked.
- `arxiv.org/abs/2510.01524` returned only the abstract text (no metadata); `export.arxiv.org` is robots-blocked; `arxiv.org/html/2510.01524v2` was **refused (HTTP 429)**. WALT's version history is therefore unchecked; everything below is v1, which is the version the dossier cites.
- AWO v2 HTML: three fetches showed Tables 1–3 and Figures 5–7 but not the appendix Tables 7–9 that hold the per-task numbers; the fetch appeared truncated after Appendix B. Numbers below are from **v1**. v1 and v2 have identical file size (1,269 KB), suggesting a minor revision, but that is not verified.
- Ares Table 1: the first fetch reported the HTML table as "severely corrupted"; later fetches returned the WebArena High and ARES rows character-for-character with 10 cells each, and the four key numbers (45.0, 46.5, 21424, 11723) appeared identically in all three fetches. Rows other than High/ARES (Low, Medium, Random, GPT-5, Gemini 3 Pro) came from one fetch only.
- All quotes were requested verbatim from a text-extraction fetch tool; table layout was not inspected as an image.

#### P1 items 10–13 — Gemini (D28, E79), Operator (D29, E39), Opus 4.8 (E83), Temporal (E70), LangChain (D24, E68), MAP (E69, D25)

| Label | Source | Version / date shown | How read |
|---|---|---|---|
| G-FL | https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/ — "Introducing Gemini 3.6 Flash, 3.5 Flash-Lite, and 3.5 Flash Cyber", Tulsee Doshi | 21 Jul 2026 | WebFetch (primary, vendor) |
| G-CU35 | https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-computer-use-gemini-3-5-flash/ — "Introducing computer use in Gemini 3.5 Flash", Mateo Quiros | 24 Jun 2026 | WebFetch (primary, vendor) |
| G-35 | https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/ — "Gemini 3.5: frontier intelligence with action", Kavukcuoglu, Dean, Vinyals, Shazeer | 19 May 2026 | WebFetch (primary, vendor) |
| G-38 | https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/ — "Introducing Gemini 3.8 Flash and 3.8 Flash Cyber", Doshi & Popa | 2 Sep 2026 | WebFetch (primary, vendor) |
| G-25CU | https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-computer-use-model/ — "Introducing the Gemini 2.5 Computer Use model" | 7 Oct 2025 | WebFetch (primary, vendor) |
| G-docs | https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite ; https://ai.google.dev/gemini-api/docs/computer-use | model page "Latest update: July 2026"; CU page undated | WebFetch (primary docs) |
| AA-38 | https://artificialanalysis.ai/models/gemini-3-8-flash — "Gemini 3.8 Flash (high)" | **no measurement / "last updated" date shown**; read 2026-09-27 | WebFetch, two fetches (primary for AA's own measurement) |
| AA-38a | https://artificialanalysis.ai/articles/gemini-3-8-flash — "Google has released Gemini 3.8 Flash, its fourth Flash model in under four months" | 2 Sep 2026 | WebFetch |
| AA-FL | https://artificialanalysis.ai/models/gemini-3-5-flash-lite | no measurement date shown | WebFetch |
| beam | https://beam.ai/agentic-insights/gemini-3-8-flash-ai-agents | 2 Sep 2026 | WebFetch (secondary; origin of "305 tok/s, fastest") |
| OA-agent | https://openai.com/index/introducing-chatgpt-agent/ | 17 Jul 2025 | WebFetch (primary) |
| OA-op | https://openai.com/index/introducing-operator/ (editor's note "July 17, 2025 update") | 23 Jan 2025 page | WebFetch (primary) |
| OA-cua | https://openai.com/index/computer-using-agent/ | 23 Jan 2025 | WebFetch (primary) |
| OA-rn | https://help.openai.com/en/articles/11794368-chatgpt-agent-release-notes | entries 17 Jul 2025, 8 Aug 2025 | WebFetch (primary) |
| OA-help | https://help.openai.com/en/articles/11752874-chatgpt-agent | "Updated: 12 days ago" (≈15 Sep 2026, calc.) | WebFetch (primary) |
| OA-oprn | https://help.openai.com/en/articles/10561834(-operator-release-notes) | **404** (both URL forms); Wayback Machine copy **blocked** by fetch tool | — |
| A-48 | https://www.anthropic.com/news/claude-opus-4-8 — "Introducing Claude Opus 4.8" | 28 May 2026 | WebFetch ×2 (primary) |
| A-docs | https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages — "Mid-conversation system messages and tool changes" | undated; read 2026-09-27 | WebFetch (primary docs) |
| T | https://temporal.io/reports/state-of-development-2026 — "The State of Development Report 2026" | "Published August 25, 2026" | WebFetch ×2 (primary) |
| LC | https://www.langchain.com/state-of-agent-engineering — H1 "State of Agent Engineering"; `<title>`/og:title "State of AI Agents" | byline date "12 June, 2026" | WebFetch ×3 (primary); curl blocked (403) |
| MAP-abs | https://arxiv.org/abs/2512.04123 | v1 2 Dec 2025; v2 30 Jan 2026; v3 3 Feb 2026; v4 4 Jun 2026 | WebFetch |
| MAP-v4 | https://arxiv.org/html/2512.04123v4 | v4, 4 Jun 2026 | WebFetch ×6 — **main text readable; appendix truncated by the fetch tool** |
| MAP-v2 | https://arxiv.org/html/2512.04123v2 | v2, 30 Jan 2026 | WebFetch ×2 — appendix B.4.2 and Fig. 12 readable |
| MAP-v1 | https://arxiv.org/html/2512.04123v1 | v1, 2 Dec 2025 | WebFetch ×2 (truncated at §7) |
| ICML | https://icml.cc/virtual/2026/poster/61834 | ICML 2026, Oral 6B "Agentic Systems"; poster Wed 8 Jul 2026 | WebFetch (official venue page) |
| IBM | https://research.ibm.com/publications/measuring-agents-in-production | "for ICLR 2026", 23 Apr 2026 | WebFetch (institutional listing, secondary for venue) |

**Access notes.** `curl` to arxiv.org, langchain.com, openreview.net, icml.cc and web.archive.org was refused by the proxy (403). OpenReview forum pages (`mWxEAgz3xu`, `AsvLggSOvS`) returned only a browser-verification page. arXiv PDFs (v2, v4) came back as "no machine-readable text" from the fetch tool. The v4 HTML was readable only up to §8 and the appendix headings; the v4 appendix body text (B.4.2) could not be read, so the 14.8% / 59.3% sentence is quoted from **v2**. All quotes below were requested verbatim; they are text extractions, not visual checks.

#### P1 items 13d and 13e — venues (D51; AAPT, SMC, SPACE); Fara-7B (D54, E90), AXIS, ComputerRL

| Label | Source | Version / date | How it was read |
|---|---|---|---|
| SA-arXiv | https://arxiv.org/html/2510.04371v2 (Ye et al., "Speculative Actions: A Lossless Framework for Faster Agentic Systems") | identifier line: "arXiv:2510.04371v2 [cs.AI] 23 Apr 2026" (also the version served at the unversioned URL) | WebFetch of HTML |
| SA-ICLR-oral | https://iclr.cc/virtual/2026/oral/10009727 | ICLR 2026 virtual site | WebFetch |
| SA-ICLR-poster | https://iclr.cc/virtual/2026/poster/10009726 | ICLR 2026 virtual site | WebFetch |
| SA-anth | https://mlanthology.org/iclr/2026/ye2026iclr-speculative/ | ML Anthology (secondary index) | WebFetch |
| AAPT | https://arxiv.org/html/2607.28399v1 and https://arxiv.org/html/2607.28399 (unversioned) — Dong et al., "Why Are GUI Agents Correct but Late? …" | v1 identifier: "arXiv:2607.28399v1 [cs.LG] (30 July 2026)" | WebFetch of HTML (two fetches disagree, see below) |
| AAAI-27 | https://aaai.org/conference/aaai/aaai-27/main-technical-track-call/ | official call | WebFetch |
| SMC | https://arxiv.org/html/2609.03236v1 (Liu, Kundu, Beerel, "Speculative Macro Commit for Faster Tool-Using Agents") | "arXiv:2609.03236v1 [cs.AI] 03 Sep 2026" | WebFetch of HTML |
| MLSP-26 | https://mlsp26.ieeesps.org/ , /call-for-papers/ , /conference-program/ , /detailed-schedule/ ; https://neuroneural.net/mlsp2026schedule/ | official site | WebFetch; paper list is JavaScript-only, not readable |
| SPACE | https://arxiv.org/html/2609.02042v1 (Yang et al., "Act More, Decide Less: Skill-Guided Adaptive Action Chunking for Long-Horizon LLM Agents") | "arXiv:2609.02042v1 [cs.LG] 02 Sep 2026" | WebFetch of HTML |
| EMNLP-26 | https://2026.emnlp.org/ , https://2026.emnlp.org/program/ | official site | WebFetch |
| Fara-arXiv | https://arxiv.org/html/2511.19663v1 and https://arxiv.org/pdf/2511.19663v1 | arXiv v1 (Nov 2025) | WebFetch of HTML and PDF; appendices not present in either extraction |
| Fara-MSR-PDF | https://www.microsoft.com/en-us/research/wp-content/uploads/2025/11/Fara-7B-An-Efficient-Agentic-Model-for-Computer-Use.pdf | MSR-hosted copy | WebFetch |
| Fara-blog | https://www.microsoft.com/en-us/research/blog/fara-7b-an-efficient-agentic-model-for-computer-use/ | "Published November 24, 2025" | WebFetch |
| BB-blog | https://www.browserbase.com/blog/training-computer-use-models-in-the-real-world-with-microsoft | Nov 24, 2025, Miguel Gonzalez | WebFetch (vendor blog) |
| AXIS | https://aclanthology.org/2025.acl-long.381/ and .pdf — Lu et al., "AXIS: Efficient Human-Agent-Computer Interaction with API-First LLM-Based Agents", ACL 2025 (Vol. 1: Long Papers), pp. 7711–7743 | camera-ready | WebFetch of anthology page and PDF |
| CRL-arXiv | https://arxiv.org/html/2508.14040v2 (Lai et al., "ComputerRL: Scaling End-to-End Online Reinforcement Learning for Computer Use Agents") | v2 (also served at the unversioned URL); v2 date not readable | WebFetch of HTML |
| CRL-ICLR | https://iclr.cc/virtual/2026/poster/10007435 | ICLR 2026 virtual site | WebFetch |

**Access failures (recorded honestly).**
- **arXiv abs pages (Comments field and submission history) could not be read for any of the six papers.** `https://arxiv.org/abs/<id>` and `/abs/<id>vN` (also `www.arxiv.org`) returned, via the fetch tool, only "[This PDF is empty or contains no machine-readable text]". `export.arxiv.org/abs`, the arXiv API and `arxiv.org/search` are disallowed by robots.txt for the fetch tool; `curl` is blocked by the proxy (403). The arXiv monthly listing pages load but ignore `skip`, so only the first 50 entries were visible. Therefore **no Comments-field verdict is given for any paper**; version identifiers and dates come from the HTML identifier line.
- `https://arxiv.org/html/2510.04371v3` and `https://arxiv.org/html/2607.28399v2` were refused by the fetch proxy (HTTP 429, rate limit, "do not fetch again"). So I could not check whether a v3 of Speculative Actions or a v2 of AAPT exists.
- OpenReview forum pages (`openreview.net/forum?id=P0GOk5wslg`) returned only a browser-verification page; the OpenReview PDF and API returned 403.
- The MLSP 2026 paper list (neuroneural.net/mlsp2026schedule) is rendered by JavaScript; the static page says "This schedule requires JavaScript for search and filtering" and "100 papers" / "30 oral talks" but lists no titles.
- EMNLP 2026: no accepted-papers page exists at the URLs tried (`/program/accepted_main_conference/`, `/program/accepted_papers/` → 404); the program page links only tutorials, workshops, industry, keynotes, welcome reception. The acl-org/emnlp-2026 GitHub repo is outside this session's allowed repos and robots-disallowed for the fetch tool.
- All quotes come from a text-extraction fetch tool asked for verbatim text; tables were not inspected as images.

### P0 item 2 — "The Cost of Dynamic Reasoning" (arXiv 2506.04301; D35, E49)

| ID | Claim as recorded in dossier | What the primary source says (verbatim, location) | Verdict |
|---|---|---|---|
| P0-2a | E49 (line 146): "(Gemini: HPCA 2026)"; D35 (line 815): "HPCA 2026" | DR-abs Comments: *"Accepted for publication at the 32nd IEEE International Symposium on High-Performance Computer Architecture (HPCA-32), 2026"*. HPCA-prog (researchr main-conference track) lists: *"The Cost of Dynamic Reasoning: Demystifying AI Agents and Test-Time Scaling from an AI Infrastructure Perspective   Main Conference   Jiin Kim, Byeongjun Shin, Jinha Chung, Minsoo Rhu"*, in session "LLM Inference Serving Systems", 15:10–15:30. HPCA 2026 ran 31 Jan–4 Feb 2026 in Sydney. KAIST-VIA: *"…(HPCA-32), Sydney, Australia, Feb. 2026, with a 20% acceptance rate (119 among 602 submissions)."* | ✅ **CONFIRMED: HPCA 2026 (HPCA-32), main conference.** Two fetches gave different days for the session (Mon 2 Feb vs Tue 3 Feb), which does not affect the venue. IEEE Xplore page numbers and DOI were not reachable. |
| P0-2b | E49: "Agentic queries consume 62.1–136.5× more GPU energy than chatbot queries" | DR-v2 §VI "AI Infrastructure Implications": *"Reflexion consumes 41.53 Wh and 348.41 Wh per query when using Llama-3.1-Instruct 8B and 70B as backend LLMs, whereas LATS consumes 22.76 Wh and 158.48 Wh. By contrast, a conventional single-turn LLM inference (ShareGPT) requires only 0.32 Wh (8B) and 2.55 Wh (70B) per query. These figures correspond to a 62.1×–136.5× increase in GPU energy per query under agent-based test-time scaling (vs. single-turn LLM inference)."* Table III caption: *"Accuracy, latency, and GPU energy consumption when servicing a single agent request on HotpotQA."* Table III rows (Energy Wh/query): 8B ShareGPT 0.32 (1×); 8B Reflexion 41.53 (130.9×); 8B LATS 22.76 (71.7×); 70B ShareGPT 2.55 (1×); **70B Reflexion 348.41 (136.5×)**; **70B LATS 158.48 (62.1×)**. Configuration: *"Reflexion and LATS design points were selected based on the highest-accuracy configurations in Figure 17."* Hardware (§III): 8B on *"a single NVIDIA A100 40GB GPU"* (GCP a2-highgpu-1g); 70B on *"8 NVIDIA A100 40GB GPUs"* (a2-highgpu-8g). Serving: vLLM 0.6.6 with prefix caching. v1 (§VI): same numbers, but says *"per request"* and omits "(vs. single-turn LLM inference)". | ⚠ **PARTIALLY CONFIRMED.** The range is printed in both versions. The ends are **LATS-70B (62.1×)** and **Reflexion-70B (136.5×)**; the 8B values (71.7×, 130.9×) fall inside the range. The scope is much narrower than "agentic vs chatbot queries": one benchmark (HotpotQA), a single request served alone (no batching), the highest-accuracy test-time-scaling configurations, and Llama-3.1 on A100-40GB, compared with a ShareGPT single-turn request. The source does not state how energy was measured (DCGM is cited only for GPU utilization). |
| P0-2c | E49: "LATS averages 71 LLM calls per request" | DR-v2 §IV-A "Overall Workflow of AI Agents": *"Figure 4 shows the average number of LLM and tool invocations per request across benchmarks. While CoT performs only a single LLM inference per request, tool-augmented agentic systems require significantly more LLM calls, averaging 9.2 times more than CoT. Among these, LATS exhibits the highest LLM invocation count, with an average of 71.0 LLM calls per request."* Fig. 4 caption: *"Average number of LLM and tool invocations per request."* Default model (§III): *"We use Llama-3.1-8B-Instruct as the default backend LLM."* v1: same figure. | ✅ **CONFIRMED as LLM (model) calls, not tool calls.** Fig. 4 reports LLM and tool invocations separately. Still open: whether 71.0 is averaged over all benchmarks LATS was run on or is one benchmark's bar. The text says "across benchmarks", and Fig. 4 was not inspected visually. |
| P0-2d | E49: "ReAct throughput 2.6 QPS vs chatbot 6.4 QPS on identical hardware" | DR-v2 §IV-C "AI Agent Serving Characteristics": *"While ShareGPT can sustain up to 6.4 QPS, ReAct supports only 2.6 QPS on HotpotQA and 1.2 QPS on WebShop, even with prefix caching enabled."* Fig. 11 caption: *"95th percentile latency for chatbot (ShareGPT) and ReAct-based AI agents (HotpotQA and WebShop) as QPS rates increase, with (solid line) and without (dashed line) prefix caching enabled."* Definition: *"The peak throughput is measured as the maximum sustainable QPS at the knee of the tail latency curve."* Setup: Llama-3.1-8B on one A100 40GB. v1: same numbers, without "even with prefix caching enabled" in the extracted sentence. | ✅ **CONFIRMED.** The dossier omits the WebShop figure (1.2 QPS), the definition (p95 latency knee) and the setup (8B, one A100-40GB, prefix caching on). "Chatbot" is the paper's own label for ShareGPT (Fig. 11). |
| P0-2e | E49: "tool waits (e.g., 1.2 s Wikipedia API) leave GPUs idle but powered" | DR-v2 §IV-A: *"In contrast, HotpotQA relies on the Wikipedia API, where individual calls take an average of 1.2 seconds."* and *"In contrast, HotpotQA and MATH employ tools that operate on local CPUs or external systems, leading to substantial GPU idle periods that account for up to 54.5% of total execution time, resulting in significantly lower GPU utilization compared to CoT."* v1 §IV-A: *"As a result, the GPU typically remains idle during tool-calling periods, leading to as much as 54.5% of the execution time being idle."* | ⚠ **PARTIALLY CONFIRMED.** The 1.2 s and GPU-idle figures are in the paper, with up to 54.5% of execution time idle (a number the dossier lacks). "But powered" is an interpretation: no quoted sentence gives idle power draw. The subsection label varied between fetches (see access notes). |
| P0-2f | E49: "numbers via themoonlight.io review"; "Primary paper, figures via secondary" | All figures above were read in the paper itself (v2, cross-checked in v1). | ✅ The secondary-source label can be removed. The figures are now sourced from the primary paper. |
| P0-2g | D8 (line 788): Gemini attributed "each extra point of accuracy costs disproportionately more tokens" to this paper "(HPCA)" | Venue confirmed (P0-2a). The misattribution itself was already resolved in D8 (it is OSWorld 2.0's §3.2 heading) and was not re-checked here. | No change to D8. |

### P0 item 3 (and P1 item 13b) — FocusAgent (arXiv 2510.03204; D15, D48, D53, E30)

#### Where each number lives (v2 = TMLR camera-ready text, 29 Aug 2026)

v2 **Table 2** (main results). Caption: *"Success Rates (SR) with Standard Error (±SE) and average pruning (Prun.) of the AxTree compared to the original for a baseline agent and our approach on WorkArena L1 and WebArena benchmarks, with variant backbone models."* Column groups: **WorkArena L1 (330 tasks)**: SR (%) | Prun. (%) | Cost (USD); **WebArena (381 tasks)**: SR (%) | Prun. (%) | Cost (USD). The rows, as returned:

```
Backbone          | Agent                   | WA-L1 SR   | Prun | Cost | WebArena SR | Prun | Cost
GPT-4.1           | GenericAgent-BT         | 53.6±2.7   | 0    | 55.6 | 36.5±2.5    | 2    | 59.0
GPT-4.1           | GenericAgent-BT (5k)    | 44.5±2.7   | 44   | 28.3 | 29.1±2.3    | 38   | 43.5
GPT-4.1           | FocusAgent(4.1-mini)    | 51.5±2.7   | 51   | 45.1 | 32.3±2.4    | 59   | 44.0
GPT-4.1           | FocusAgent(5-mini)      | 53.2±2.7   | 61   | 38.1 | 39.6±2.5    | 53   | 46.2
Claude-3.7-Sonnet | GenericAgent-BT         | 56.7±2.7   | 0    | 55.4 | 44.6±2.5    | 2    | 58.2
Claude-3.7-Sonnet | FocusAgent(4.1-mini)    | 52.7±2.7   | 50   | 46.9 | 39.9±2.5    | 51   | 42.6
Qwen3-235B-A22B   | GenericAgent-BT         | 27.0±2.4   | 0    |  —   | 22.0±2.1    | 4    |  —
Qwen3-235B-A22B   | FocusAgent(4.1-mini)    | 33.9±2.6   | 58   |  —   | 22.0±2.1    | 63   |  —
Qwen3-235B-A22B   | FocusAgent(5-mini)      | 38.2±2.7   | 59   |  —   | 21.8±2.1    | 63   |  —
Qwen3-235B-A22B   | FocusAgent(qwen3.5-9b)  | 34.2±2.6   | 63   |  —   |  —          |  —   |  —
```
(I did not ask for the Qwen cost cells. The Qwen rows came from one fetch only.)

v2 **Table 1** (WorkArena L1 retriever ablation). Caption: *"Success Rates (SR) and Standard Error (±SE) of agents leveraging different retrieval methods and models, average pruning (Prun.) and cost breakdown achieved on WorkArena L1 using GPT-4.1 as the backbone model for all agents, including FOCUSAGENT."* Rows returned:
- `GenericAgent-BT | 53.6 ± 2.8 | 0 | total 55.6`
- `FocusAgent (4.1-mini) | 51.5 ± 2.7 | 56 | Backbone 33.8 | Retriever 11.3 | Total 45.1`
- `FocusAgent (5-mini) | 53.2 ± 2.7 | 61 | Backbone 26.7 | Retriever 11.4 | Total 38.1`
- others: GenericAgent-BT (5k tokens) 44.5 / 44 / $28.3; BM25Agent-400 53.3 / 32 / $34.3; EmbeddingAgent (embed-3-large)-400 46.4 / 31 / $36.2; FocusAgent (qwen3-235b-a22b) 51.5 / 58 / backbone $28.4, retriever "*".

v2 **Tables 15 / 16** (appendix, input-token cost breakdown). Caption (Table 15): *"Input tokens processing cost breakdown in US dollars (USD) for the WorkArena benchmark Large models pricing is set to 2 USD/1M tokens and the small models are at 0.4 USD/1M tokens."* Table 16 has the same caption for WebArena. Table 15 totals are GPT-4.1 GenericAgent $55.6, 4.1-mini $45.1, 5-mini $38.1; Claude-3.7 $55.4 and $46.9. Table 16 rows: `GPT-4.1 | GenericAgent | 59.0 | — | 59.0 | 0.019`; `GPT-4.1 | FocusAgent(4.1-mini) | 32.1 | 11.9 | 44.0 | 0.010 (-48%)`; `Claude-3.7 | GenericAgent | 58.2 | — | 58.2 | 0.019`; `Claude-3.7 | FocusAgent(4.1-mini) | 30.6 | 12.0 | 42.6 | 0.012 (-37%)` (columns: Backbone LLM, Retriever LLM, Total, Avg. Per Step). **Table 16 has no 5-mini row**, so the $46.2 WebArena figure appears only in Table 2.

**Cost definition** (v2, verbatim): *"The cost of the end-to-end processing of input tokens is reported in US dollars (USD), with backbone models priced at 2$/1M tokens, GPT LLM retriever models at 0.4$/1M tokens."* All dollar figures are therefore **input-token cost only**, at the paper's assumed list prices, and are **totals over the whole benchmark run**: 330 WorkArena L1 episodes or 381 WebArena tasks. They are costs per attempt, not per success, and not per task. The "Avg. Per Step" column of Table 16 is the only per-unit figure the paper prints.

**v1 (Oct 2025) Table 2**. Caption: *"Success Rates (SR) with Standard Error (±SE) and average pruning (Prun.) of the AxTree compared to the original for a baseline agent and our approach on WorkArena L1 and WebArena benchmarks, with variant backbone models and GPT-4.1-mini as the retrieval model."* It has **no cost columns**, and v1 contains no dollar table at all. Rows:
```
GPT-4.1           | GenericAgent-BT      | 53.0 ±2.7 | -  | 36.5 ±2.5 | -
Claude-Sonnet-3.7 | GenericAgent-BT      | 56.7 ±2.7 | -  | 44.6 ±2.5 | -
GPT-4.1           | GenericAgent-BT (5k) | 41.8 ±2.7 | 46 | 29.1 ±2.3 | 38
GPT-4.1           | FocusAgent           | 51.5 ±2.7 | 51 | 32.3 ±2.4 | 59
Claude-Sonnet-3.7 | FocusAgent           | 52.7 ±2.7 | 50 | 39.9 ±2.5 | 51
```
v1 Appendix B, Table 5 (WorkArena L1 only, no WebArena columns): `GPT-4.1 | FocusAgent (4.1-mini) | 51.5 ±2.7 | 51` and `FocusAgent (5-mini) | 51.8 ±2.8 | 61`. Body text: *"Table 5 shows that using FocusAgent with two small models (SR 51.5% and 51.8%) yield to close performance as using a large model with the full tree (SR 53.0%) with GPT-4.1."* One fetch also returned a Claude 5-mini row with identical cells (51.8 ±2.8 | 61). That row may be an extraction artifact, and I do not rely on it.

#### Verdicts

| ID | Claim as recorded in dossier | What the primary source says (verbatim, location) | Verdict |
|---|---|---|---|
| P0-3a | D15 (l. 795): "O (doc 2): $55.6→$38.1, 53.6→53.2%; O (doc 3), C (doc 6): $55.6→$45.1, 53.6→51.5% (Aug-2026 main table)"; "Config/version-dependent" | v2 Table 2 prints **both** rows side by side, GPT-4.1 backbone, WorkArena L1: `FocusAgent(4.1-mini) | 51.5±2.7 | 51 | 45.1` and `FocusAgent(5-mini) | 53.2±2.7 | 61 | 38.1`. Baseline `GenericAgent-BT | 53.6±2.7 | 0 | 55.6`. Table 1 and Table 15 give the same totals. | **RESOLVED: config, not version.** $45.1 / 51.5% = **GPT-4.1-mini retriever**. $38.1 / 53.2% = **GPT-5-mini retriever**. Both numbers come from the same v2 table, and the backbone is GPT-4.1 in both. Neither is "older". |
| P0-3b | D15 resolution: "use $45.1 / 51.5%" | See above. The v2 body text (*"pruning rates of 51% (GPT-4.1) … translating to cost reductions of approximately 19%"*) and the latency study (Table 11) both describe the 4.1-mini configuration. The 5-mini configuration gets a larger saving (−31.5%, calc.) and costs 0.4 pp of accuracy. | **PARTIALLY CONFIRMED.** $45.1 / 51.5% is the paper's primary configuration and the one E30's latency applies to. It is not the best row, though, and it should be cited together with its retriever name. $38.1 / 53.2% is equally valid for GPT-5-mini. |
| P0-3c | Dollar-figure definition (l. 398 "input costs exclude output") | v2: *"The cost of the end-to-end processing of input tokens is reported in US dollars (USD), with backbone models priced at 2$/1M tokens, GPT LLM retriever models at 0.4$/1M tokens."* Table 15/16 caption: *"Input tokens processing cost breakdown in US dollars (USD) for the WorkArena benchmark …"* | ✅ **CONFIRMED.** Input tokens only, at assumed prices, **total over the benchmark** (330 WorkArena L1 episodes / 381 WebArena tasks), retriever cost included. Per episode: $0.168 baseline, $0.137 (4.1-mini), $0.115 (5-mini) on WorkArena L1; $0.155, $0.115 and $0.121 on WebArena (all calc.). |
| P0-3d | l. 262 / l. 398 / l. 558 / D15 (doc 3): "Aug-2026 main table replaces its appendix values"; the appendix "retains older values" | v2 appendix Table 15 totals ($55.6 / $45.1 / $38.1) match Table 2. The only internal disagreement found is the **pruning rate for 4.1-mini on WorkArena L1: 56% in Table 1 vs 51% in Table 2** (and 51% in the body text). The Table 1 value came back as 56 in two fetches, the Table 2 value as 51 in three. | ⚠ **NOT CONFIRMED as stated.** No stale appendix *cost* values were found. There is a Table 1 vs Table 2 pruning mismatch (56% vs 51%). Drop "replaces its appendix values" or re-scope it to that mismatch. |
| P1-13b-i | D48 (l. 829): "v1 (Oct 2025; C15): 36.5→**32.3%** (−4.2 pp)" | v1 Table 2, *"… with variant backbone models and GPT-4.1-mini as the retrieval model"*: `GPT-4.1 | FocusAgent | 51.5 ±2.7 | 51 | 32.3 ±2.4 | 59`; baseline `36.5 ±2.5`. | ✅ **CONFIRMED.** 32.3% is GPT-4.1 backbone with a **GPT-4.1-mini** retriever. |
| P1-13b-ii | D48: "v2 / TMLR (Aug 2026; O2, O3): 36.5→**39.6%** (+3.1 pp)"; "**Sign flip between versions**" | v2 Table 2: `GPT-4.1 | FocusAgent(5-mini) | 53.2±2.7 | 61 | 38.1 | 39.6±2.5 | 53 | 46.2`. The same v2 table **still prints** `GPT-4.1 | FocusAgent(4.1-mini) | 51.5±2.7 | 51 | 45.1 | 32.3±2.4 | 59 | 44.0`. v1 has no WebArena result for 5-mini: v1 Table 5 is WorkArena-only. | **CORRECTED.** 39.6% is real, but it belongs to a **different retriever (GPT-5-mini)**, added to the WebArena evaluation in v2. The GPT-4.1-mini result (32.3%, −4.2 pp) is **unchanged** between v1 and v2. There is no sign flip for any single configuration. The WebArena effect depends on the retriever: −4.2 pp (4.1-mini) vs +3.1 pp (5-mini), within one version. Each gap is about 1.2–1.7 SE (calc., SE ≈ 2.4–2.5 pp). |
| P1-13b-iii | l. 398: "v1 … WorkArena 53.0→51.5%" | v1 Table 2 baseline `53.0 ±2.7`, FocusAgent `51.5 ±2.7`. v2 baseline `53.6±2.7`, FocusAgent(4.1-mini) `51.5±2.7`. | ✅ **CONFIRMED.** What changed between versions is the **baseline**: WorkArena L1 53.0 → 53.6, and the 5k-truncation baseline 41.8 → 44.5. The 4.1-mini FocusAgent row did not change. The v1 5-mini WorkArena result (51.8%, App. B Table 5) became 53.2% in v2. |
| P1-13b-iv | l. 398 / l. 262: WebArena "$59.0→$46.2 (−21.7%), SR 36.5→39.6%" | v2 Table 2, 5-mini row: WebArena cost 46.2, SR 39.6. The 4.1-mini row: 44.0, SR 32.3. Table 16 (4.1-mini only): `44.0 | 0.010 (-48%)`. Body text: *"On Web Arena, Focus Agent attains pruning rates of 59% (GPT-4.1) … yielding cost savings of 26% …"*, which matches 4.1-mini ($44.0 = −25.4%, calc.). | ⚠ **CORRECT numbers, mixed configurations in the dossier.** $46.2 / 39.6% is 5-mini. Lines 262 and 398 pair it with WorkArena $45.1 / 51.5% (4.1-mini) and with "−59% observation (WebArena)" (4.1-mini; 5-mini prunes 53%). The combination does not exist in the paper. |
| P0-3e | l. 398: "naive 5k truncation −49% cost, 53.6→44.5%" | v2 Table 2: `GPT-4.1 | GenericAgent-BT (5k) | 44.5±2.7 | 44 | 28.3 | 29.1±2.3 | 38 | 43.5` | ✅ **CONFIRMED** (v2): $28.3 / $55.6 = −49.1% (calc.). In v1 the same baseline read 41.8%. |
| E30 | l. 103: "Baseline 2.5 s/step model latency → 10.1 s/step with a GPT-4.1-mini retriever (7.6 s retrieval)"; "browser time excluded; retries included" | v2 Table 11, caption *"Agent latency breakdown for both agents using GPT-4.1 as backbone on WorkArena L1."* Setup: *"wall-clock LLM latency"* measured *"by wrapping each agent's LLM callables with a timing decorator"*. Retriever (GPT-4.1-mini) mean 7.6 s. Backbone 2.5 s in both agents. v1 has no latency table. | ✅ **CONFIRMED** (v2 only; absent from v1). The "33 tasks" subset size was not re-checked: the fetch paraphrased the scope as "the full evaluation set". Applies to the 4.1-mini config only; **no latency figure exists for 5-mini**. |
| D53 | l. 834: "TMLR 2026 (O2, O3) vs 'ICLR 2026 workshop per snippet' (C15)" | jmlr.org/tmlr/papers: *"FocusAgent: Simple Yet Effective Ways of Trimming the Large Context of Web Agents Imene Kerboua, Sahar Omidi Shayegan, Xing Han Lù, Léo Boisvert, Megh Thakkar, Massimo Caccia, Jérémy Espinas, Alex Aussem, Véronique Eglin, Alexandre Lacoste, August 2026 [openreview] [pdf] [bib] [code]"* | ✅ **TMLR confirmed, August 2026** (official TMLR list). The exact decision date is unresolved because OpenReview returned 403. The ICLR 2026 workshop claim was not checked. |

### P0 item 4 — Continuum (D14) and PASTE (D13)

| ID | Claim as recorded (dossier line) | What the primary source says (verbatim, location, version) | Verdict |
|---|---|---|---|
| 4-C1 | D14 (l.794): C/G ">8× average JCT" vs O "v7 1.12–3.66× delay, 1.10–3.22× throughput"; resolution "Version drift; cite the Sep-2026 v7 numbers". l.558: "Continuum's v7 replaces '>8×'". l.434: "earlier versions: '>8× average JCT'" | **v7 abstract** (HTML v7, 8 Sep 2026): *"Evaluations on real-world agents (SWE-Bench, BFCL, OpenHand) with Llama-3.1 8B/70B, Gemma-3 12B, and GLM-4.5 355B shows that Continnum improves the average job completion times by over 8x while improving throughput."* (sic "Continnum"). **v7 §1:** *"Across three hardware and model setups, we show that Continnum reduces delay by 1.12x to 3.66x and improves throughput by 1.10x to 3.22x on multi-turn agentic workloads."* and *"Moreover, we evaluated Continnum on Company A's internal testbed and show it can reduce delay for real SWE-agent workloads by up to 8.18x."* The unversioned abs page (= v7) shows the same ">8x" abstract sentence. | ❌ **CORRECTED.** Not version drift: v7 carries **both** numbers. ">8×" is still v7's abstract headline; it comes from the real SWE-agent deployment (8.18× delay). 1.12–3.66× / 1.10–3.22× is the trace-replay range across three setups. |
| 4-C2 | (history) when each number appeared | **v1** (4 Nov 2025) abstract has no number: *"…shows that Continuum significantly improves the average job completion times, and remains performant across different hardware setups and DRAM offloading schemes."* v1 §6.2: *"For instance, with the Llama-3.1-8B model, Continuum achieves up to a 2x reduction in average response time compared to the vanilla vLLM baseline."* **v2** (20 Dec 2025) abstract: *"…shows that Continuum significantly improves the average job completion times and its improvement scales with turn number increase."*; v2 §1 has the 1.12–3.66× / 1.10–3.22× sentence and *"…on Tensormesh's internal testbed … by up to 8.18x."* **v3** (30 Jan 2026): same abstract as v2; §1 has 1.12–3.66× and *"We demonstrate that Continuum achieves up to 8.18x improvements in both latency and throughput over previous methods in both emulated and real cases."* **v4** (4 May 2026), title *"CacheTTL: Efficient and Robust Multi-Turn LLM Agent Scheduling with KV Cache Time-to-Live"*: abstract first says *"…CacheTTL improves the average job completion times by over 8x while improving throughput."*; §1 keeps 1.12–3.66× and 8.18× (*"Company A's … Inference startup anonymized for double-blind"*). **v5, v6, v7**: title back to Continuum/Continnum; abstract ">8x"; §1 1.12–3.66× and 8.18×. | ✅ History established. ">8×" entered the **abstract** in v4 and never left; the 1.12–3.66× range is in §1 from v2 (possibly v1, see access note). The dossier's "v4 was titled CacheTTL" is confirmed. |
| 4-C3 | l.434, l.257: "v7 1.12–3.66× lower delay, 1.10–3.22× throughput (SWE-Bench/BFCL/OpenHands; Llama-3.1 8B/70B, Gemma-3 12B, GLM-4.5 355B)" — what is measured | v6 §6.1 (v7 §6 not readable): *"Model and Hardware: We evaluate Continuum with Llama-3.1-8B, Llama-3.1-70B, and Gemma-3-12B. We use A100-SXM GPU from Runpod, H100 from AWS and Tensormesh, and B200 GPU from on-prem servers."* *"Datasets: For results other than the real SWE-Bench experiments in Figure 12, we evaluate on two collected workloads running GPT-5 … and using poisson distribution for the arrival pattern of agent programs"* — SWE-Bench (mini-swe-agent), BFCL V4 Web Search (*"scaled down the workload by 0.4"*), OpenHands (*"multi-SWE-bench … for the Go language"*). Baselines: *"Vanilla vLLM … vllm 0.10.2"*, *"CPU DRAM offloading … vllm 0.10.2 with LMCache 0.3.7"* (list truncated in fetch; v1 also lists Autellix/PLAS and InferCept). v6 §6.2: *"We conduct the trace replay experiments for SWE-Bench, BFCL, and OpenHands workloads."* | ⚠ **PARTIALLY CONFIRMED.** Figures correct, but the range is **trace replay** (agent traces collected with GPT-5, replayed with Poisson arrivals on Llama/Gemma), measuring average program delay / JCT and throughput under load — not end-to-end agents running open models. GLM-4.5 355B is **not** in the §6.1 model list; it appears in the abstract and in the Table 5 microbenchmark (GLM-4.5-fp8). No formal definition of "delay" found (fetch: "The paper does not formally define these metrics in a single dedicated section"). |
| 4-C4 | l.434 / l.257 / D14: "144.9 vs 93.4 inference steps/min (≈1.55×) on Multi-SWE-bench with GLM-4.5-fp8 on 8×H100" | **v6 Table 5:** `| | vLLM | ThunderAgent | Continuum |` / `| Throughput (Steps Per Min) | 93.4 | 114.8 | 144.9 |`. Text: *"We also conducted a micro-benchmark for potential reinforcement learning use of Continuum. We tested the OpenHands Agent with GLM-4.5-fp8 training on Multi-SWE bench [83] for rollout generation. The hardware setup is an 8xH100 node. We compared with the concurrent RL work ThunderAgent [36] on inference steps per minute, as reported by the original paper. As demonstrated by Table 5, Continuum achieves higher throughput for single node rollout."* Not visible in v2/v4/v5 fetches; v7 §6 unreadable. | ✅ **CONFIRMED in v6** (25 May 2026). 144.9/93.4 = 1.55× vs vLLM; 144.9/114.8 = 1.26× vs ThunderAgent (calc.). Caveats the dossier omits: it is an **RL rollout-throughput microbenchmark** (steps/min, single node), the comparator column includes ThunderAgent, and the baseline figures are "as reported by the original paper" (i.e. possibly not re-run). Presence in v7 not verified. |
| 4-C5 | ">8×": what it measures | v6 Fig. 12 caption: *"Continuum improves delay under the pass rate for real SWE-agents in distributed settings."* Text: *"We test Continuum running real SWE agent for 500 tasks in SWE-Bench-Verified in Tensormesh's internal H100 testbed. We set up our agent client environment by adding a job distributor for the SWE-Bench platform that distributes agents in poisson distribution. We use a simple session aware routing for Continuum and compare against other distributed inference solutions."* | ✅ ">8×" / 8.18× = **reduction in average delay (JCT)**, real SWE-agent on 500 SWE-Bench-Verified tasks, H100 testbed of an inference startup (Tensormesh, anonymized as "Company A" in v4+), vs unnamed "other distributed inference solutions" (model not identified in the fetched text). It is a best case ("up to"). |
| 4-C6 | l.434: "same-or-higher pass rates claimed, exact delta not verified" | v6: *"Notice that Continuum actually has higher pass rate than baselines. This is due to SWE-Bench's time limit for environment dockers to prevent hanging."* | ✅ Claim confirmed (v6); delta still not extracted. The higher pass rate is attributed to timeouts, not to scheduling changing agent behavior. |

| ID | Claim as recorded (dossier line) | What the primary source says (verbatim, location, version) | Verdict |
|---|---|---|---|
| 4-P1 | D13 (l.793): v1 48.5%; v3 43.5% mean / 55.4% p99 | **v1 abstract** (19 Mar 2026): *"Experimental results against state of the art baselines show that PASTE reduces average task completion time by 48.5% and improves tool execution throughput by 1.8x."* **v3 abstract** (16 Jun 2026): *"Across deep research, coding, and scientific-agent workloads, PASTE reduces average task completion time by 43.5% and lowers observed tool latency by 1.8x."* **v3 §6.2:** *"Across all agents, PASTE consistently reduces E2E latency relative to vLLM, Agentix, ORION, and SpecFaaS. PASTE reduces average latency by up to 43.5%, with p99 tail latency improving by up to 55.4%."* | ✅ **CONFIRMED with qualifiers.** Both are "up to" figures in §6.2 (best agent/baseline pair), not means across all settings; the dossier's "43.5% mean" should read "average latency, up to 43.5%". The 1.8× also changed meaning: v1 "tool execution throughput", v3 "observed tool latency". |
| 4-P2 | l.361: "PASTE: Act While Thinking … arXiv Mar 2026 (v3 later)" | v1 title: *"Act While Thinking: Accelerating LLM Agents via Pattern-Aware Speculative Tool Execution"*. v3 (and current abs page) title: *"Parallelizing Tool Execution and LLM Generation for Low-Latency Agent Serving"*. Authors (abs): Yifan Sui, Han Zhao, Rui Ma, Zhiyuan He, Hao Wang, Jianxun Li, Kaiqiang Xu, Kai Chen, Yuqing Yang. No Comments/venue field. | ⚠ **CORRECTED:** v3 is retitled; v3 dated 16 Jun 2026 (v2 13 Jun 2026). |
| 4-P3 | l.256 / l.361: "1.25× vs ORION, 1.32× vs SpecFaaS" | Strings "1.25" and "1.32" **NOT FOUND** in v1 or v3 (visible text); ORION/SpecFaaS absent from v1. v3 §6.3 (fetch summary with inline quotes): *"PASTE reduces average tool latency by up to 55.2% and p99 tool latency by up to 60.6%"*; tool-side speedups *"1.71× over ORION and 1.83× over SpecFaaS"*; *"97% above 1×"*. v3 §6.5: *"At each concurrency, PASTE sustains at least 1.27× speedup over vLLM and 1.24× over Agentix."* *"Pooled across the sweep, the corresponding speedups are 1.50× and 1.30×."* | ❌ **Not supported by v1 or v3 text.** v3 reports **1.71× (ORION) / 1.83× (SpecFaaS)** tool-side speedups. 1.25×/1.32× may be read off Fig. 10 (E2E) or come from v2 (unread, 429); unresolved → D-entry. |
| 4-P4 | l.256/361/583: audit ">20,000 speculative actions: 602 side-effecting blocked, 0 result divergences" | v3 §6.8: *"Across all workloads, PASTE detects 602 potentially side-effecting speculative actions among over 20,000 speculative actions and prevents them from committing. No task produces a different final result compared with the baselines."* Not in v1. | ✅ **CONFIRMED (v3 only)**; absent from v1. |
| 4-P5 | l.361/583: "4 nodes × 32 A100-80GB"; l.583 "GPT-5.2 / Gemini 2.5 Pro APIs + local Qwen" | v3 Table 1: *"Per-node GPU: 8 GPU, NVIDIA A100 80GB"*; *"Models: Qwen-DeepResearch-30B …, Qwen3-30B-A3B"* (fetch summary: 4 nodes, 32 GPUs total; vLLM serving). v1: *"…with both LLM API (Gemini-2.5, GPT-5.2), and a local deployed Qwen-DeepResearch-30B model on a server with 8 NVIDIA A100-80G GPUs"*. v3: GPT-5.2 NOT FOUND. | ⚠ **CORRECTED.** v3 = 4 nodes × 8 A100-80GB (32 GPUs, not 4×32), local Qwen models only; the API models belong to v1 (8 A100s). l.583 mixes versions. |
| 4-P6 | l.256/361: "Edit→Verify pattern 55%, Search→Visit 51%" | v1 §2.3.1: *"55% of successful file_editor tool calls were immediately followed by a terminal tool call"*; *"51% of tool calls search 10 related results, and then immediately trigger a tool call to visit the top 3-4 URLs"*. v3 (fetch summary): *"55% of successful file_editor calls are followed by terminal execution"*; *"95% of web visits the URL is a strict substring of the preceding search output"*. | ✅ Confirmed (51% confirmed in v1; not checked in v3). |
| 4-P7 | E28 (l.101): "Tool execution 35–61% of total request time (PASTE)" | v1 §1: tool execution accounts for *"35% to 61% of total request time"*; v1 §2.2.1: *"On average, tool execution accounts for 60% of the latency in coding tasks, 50% in deep research tasks, and 36% in scientific tasks"*. v3 §2.2: *"Across the evaluated agents, tool execution accounts for 45%–57% of agent E2E latency."* | ⚠ **Version drift.** 35–61% is v1 only; v3 says 45–57%. |

### P0 item 5 — TraceLab (arXiv 2606.30560; D16, E19)

| ID | Claim as recorded in dossier | What the primary source says (verbatim, location) | Verdict |
|---|---|---|---|
| P0-5a | E19 (line 87) / D16 (line 796), C: median step "≈119K prefix / 875 append / 214 output tokens" | TL-v2 §1 Introduction: *"The median LLM generation workload is about 119K prefix tokens (prefix cache read of history context), 875 append tokens (fresh new input tokens from user or tool results), and 214 output tokens."* Identical in TL-v1. | ✅ **CONFIRMED (v1 and v2).** The paper does not say this is pooled across Claude Code and Codex. Each value lies between the per-agent P50s in Table 8 (below), which suggests a pooled median over all 357,161 steps (inference, not stated). |
| P0-5b | D16, G (via a blog): "126k / 857 / 252" | TL-v2 Table 8 "Per-step prefix, append, and output token length distribution", P50 column: **Prefix: Claude 126,180; Codex 115,584. Append: Claude 857; Codex 886. Output: Claude 252; Codex 184.** §5.1: *"A median Claude step reads back 126k prefix tokens but appends only 857."* §5.2: *"median of only 252 output tokens for Claude and 184 for Codex."* Same P50 cells in TL-v1. | ✅ **CONFIRMED, but it is a different statistic.** 126k/857/252 are **Claude-only** medians; 119K/875/214 are the headline all-steps medians. Neither set is wrong. **D16 resolved.** |
| P0-5c | D16 (G via blog): "prefill amplification 5.3×"; line 279: "3.8× prefill amplification on misses"; E19: "misses cause 3.8× more prefill than unique tokens" | TL-v2 §4.3 "Cost Distribution": *"Overall, cache misses cause 3.8× more tokens to be prefilled than prefills due to truly unique input tokens."* The fetch tool reported that "5.3×" does not appear in v1 or v2. Its only "5.3" match is a tool-time cell in Table 10 (`shell_command \| 6.1k \| 5.3h \| …`). The word "amplification" does not appear in either version. **TL-site** (authors' live dashboard, undated): *"Inverting the fresh fraction gives the prefill amplification factor, how many times more tokens are prefilled than an eviction-free perfect cache would need: 6.3x overall (10.5x Claude, 3.5x Codex)."* The dashboard's dataset is larger than the paper's: *"665,453 agent steps"*, *"8,058"* sessions from *"52"* users, *"Sep 23 2025 — Jul 24 2026"*. It also shows hit rates of 95.2% (Claude) and 96.2% (Codex), and prefix = 58.6% of session cost. | ❌ **"5.3×" CORRECTED (not in the paper).** "Prefill amplification factor" is the dashboard's term, defined as 1 ÷ fresh-token fraction. Its value now reads 6.3× on the dashboard's grown dataset. 5.3× was most likely an earlier dashboard snapshot, but this is inferred and unverifiable because archives are blocked. The paper's number is **3.8×**, with a different definition: tokens prefilled because of cache misses ÷ truly unique input tokens. If "3.8× more" means additional tokens, total prefill ÷ unique ≈ 4.8× (calc., ambiguous). E19's paraphrase is correct. Line 279's "3.8× prefill amplification" borrows the dashboard's term for the paper's metric and should be reworded. |
| P0-5d | E19: "8.8 LLM calls, 10.8 tool calls, 4.3 min per request (p90 >6.4 min)" | TL-v2 §1: *"To complete a user's task, the agent will, on average, carry out 8.8 LLM calls and invoke tools 10.8 times."* and *"It takes on average 4.3 minutes to complete one request, with long tails whose p90 exceeds 6.4 minutes."* Table 7, per request: Avg 4.3m, P50 38.3s, P90 6.4m, P99 43.9m. §4.1 rounds this to *"around 8 steps with 11 tool calls."* | ✅ **CONFIRMED.** These are means per request. Table 7 adds a median of 38.3 s and a p99 of 43.9 min, which are useful because the distribution is very skewed. |
| P0-5e | E19: "95.7% prefix-cache hit rate"; "prefix tokens = 59.5% of cost" | TL-v2 §1: *"The global prefix cache hit rate is 95.7%"*. §4.3 / Table 5: *"…making them 59.5% of total cost, versus 29.2% for append tokens"*; Table 5 splits cost into prefix 59.5%, append 29.2%, output 11.2%. The average session costs $9.70 (P50 $0.61). | ✅ **CONFIRMED.** Costs are at an *"estimated API list-price equivalent"* (Table 1 caption): about $40.4K total, of which Claude about $22.7K and Codex about $17.8K. |
| P0-5f | E19 / line 46 / line 212: "tool calls >1 min are 4% of calls but 85% of tool time" | TL-v2 §1: *"Tool calls longer than 1 min are only 4 percent of all tool calls, but they account for 85% of total tool-call time."* §6.2: *"For Claude, calls under 1 s account for 70% of calls but less than 1% of total tool time, while calls longer than 1 min are only 4.9% of calls but contribute 92% of total tool time."* | ✅ **CONFIRMED for the introduction's all-tools figure.** §6.2 gives a Claude-only version (4.9% / 92%). The two differ in scope and do not contradict each other; see D-entry below. |
| P0-5g | E19: "4,265 real Claude Code/Codex sessions, 357,161 LLM steps, 432,510 tool calls, 43 developers (Sep 2025–Jun 2026)" | TL-v2 Table 1 ("Summary of the collected coding-agent trace…"). Sessions: 2,676 Claude, 1,589 Codex, **4,265** total. Distinct users: 37, 22, **43**. Observation window: Oct 2025–Jun 2026 (Claude), Sep 2025–Jun 2026 (Codex), **Sep 2025–Jun 2026** (total). LLM steps: 140,338, 216,823, **357,161**. Tool calls: 142,388, 290,122, **432,510**. Model mix, Claude: opus-4-7 63.1%, opus-4-6 12.0%, haiku-4-5 7.9%, sonnet-4-6 7.8%, opus-4-8 7.7%, other 1.5%. Model mix, Codex: gpt-5.5 47.5%, gpt-5.4 26.0%, gpt-5.3-codex 13.7%, gpt-5.2-codex 3.4%, other 9.3%. | ✅ **CONFIRMED.** The traces come from the authors' *"own day-to-day use of Claude Code and Codex"* (§1). They are not a random production sample. |
| P0-5h | Appendix A line 491: "UW" | Affiliations as extracted: University of Washington; Wuhan University of Technology; Shanghai Jiao Tong University. arXiv Comments field: none. v1 29 Jun 2026, v2 30 Jun 2026. | ✅ UW-led. No venue is stated. |

### P0 item 6 — Gartner (E55, E62, E73; Top-10 rank 10)

| ID | Claim as recorded in dossier | What the primary source says (verbatim, location) | Verdict |
|---|---|---|---|
| 6a | E55 (l.152): "Gartner (17 Aug 2026 release): inference cost per agentic workflow to rise >5× through 2028"; "Gartner 'Inference Paradox' doc" | G-Aug headline: *"Gartner Predicts AI Inference Costs Per Agentic Workflow Will Increase More Than Fivefold Through 2028"*; lead: *"AI inference costs per agentic workflow will increase more than fivefold through 2028 according to Gartner, Inc."*; *"Compared to a basic chatbot interaction, routing a task to an agentic reasoning model increases provider inference costs by at least five times, and often much more as task complexity grows."*; *"Gartner clients can read more in The Inference Paradox: Inference Tiering Is Critical to Protect Margins."* Analyst: *"Will Sommer, Sr. Director Analyst"*. | ✅ **CONFIRMED** (primary exists, date and figure correct). Caveats: analyst forecast; the release states **no baseline year** for "fivefold" and no sample or method; the ≥5× chatbot comparison is explicitly **provider** inference cost. The "Inference Paradox" is a client-only research note (paywalled; not read). |
| 6b | (context for 6a) three trends / "Inference Paradox" | G-Aug: *"Foundational model cost economics are rapidly improving."* … *"More sophisticated AI workflows use far more tokens than simple chatbot interactions, driving higher overall inference costs."*; Sommer: *"Product leaders cannot rely on more efficient token economics to rationalize AI costs. Each successive generation of AI capability will necessitate more, and often more expensive, tokens."*; *"These dynamics mean that tokens are becoming more cost-efficient, but not as quickly as AI capabilities and the costs associated with those capabilities are increasing."* | ✅ Supports the dossier's framing (l.280, rank 10). |
| 6c | Top-10 rank 10 (l.234) and l.51: agentic models need "5–30× tokens per task vs a chatbot" | G-Mar: *"Agentic models, for example, require between 5-30 times more tokens per task than a standard GenAI chatbot, and can perform many more tasks than a human using GenAI."* | ✅ **CONFIRMED** (re-checked; D20 stands). |
| 6d | Rank 10 (l.234) and l.51: "overall inference cost is expected to rise" | G-Mar: *"While lower token unit costs will enable more advanced GenAI capabilities, these advancements will drive disproportionately higher token demand. As token consumption rises faster than token costs fall, overall inference costs are expected to increase."* | ✅ **CONFIRMED**. |
| 6e | Rank 10 (l.234): "even as **unit token cost** falls >90% by 2030"; l.51: "even as **unit prices** fall >90% by 2030" | G-Mar: *"By 2030, performing inference on a large language model (LLM) with one trillion parameters will cost GenAI providers over 90% less than it did in 2025"*; and *"However, falling GenAI provider token costs will not be fully passed on to enterprise customers."* Also: *"Gartner forecasts LLMs in 2030 will be up to 100 times more cost-efficient than the earliest models of similar size developed in 2022"*. Named notes: "Navigating the Commoditization Trap as Token Costs Fall by Over 90% Through 2030"; "Frontier Scale Models Threaten Software Margins and Solvency" (client-only). | ⚠ **CORRECTED (wording).** The >90% is the **provider's cost** of inference on a 1T-parameter LLM, 2025→2030 — not the unit token price customers pay, which Gartner says will not fall as much ("not fully passed on"). l.51's "unit prices fall >90%" is wrong; rank 10's "unit token cost" is ambiguous and should say provider cost. E62's own wording ("cost providers >90% less") is correct. |
| 6f | l.280: "Gartner expects **per-workflow** inference cost to rise (E62)" | Per-workflow wording is in G-Aug (E55), not G-Mar (E62); G-Mar speaks of "overall inference costs". | ⚠ **CORRECTED (citation)**: cite E55 (per-workflow, 17 Aug 2026) and E62 (overall, 25 Mar 2026). |
| 6g | E73 (l.182): "Only 28% of **AI projects** met ROI expectations; 20% failed outright (782 I&O leaders, **Apr 2026**)"; source olakai.ai, enterprisedna.co (secondary) | G-Apr: *"Only 28% of AI use cases in infrastructure and operations (I&O) fully succeed and meet ROI expectations, while 20% fail outright, according to a Gartner, Inc. survey of 782 I&O leaders in November and December 2025."*; *"For the 57% of I&O leaders who reported at least one failure, many said their AI initiatives failed because they expected too much, too fast."*; *"Thirty-eight percent of I&O leaders who faced setbacks said persistent skill gaps continue to hamper AI success."*; *"I&O leaders most frequently observe AI failures in auto-remediation, self-healing infrastructure, and agent-led management of workflows within and between systems."* Analyst: Melanie Freeze. | ⚠ **CORRECTED.** Numbers 28% / 20% / 782 confirmed, now with a primary URL. Scope is **"AI use cases in I&O"** (as reported by I&O leaders), not "AI projects" in general; fieldwork **Nov–Dec 2025**, release **7 Apr 2026**. The release gives no definition of "fully succeed" or of ROI expectations and no respondent geography. |

### P0 item 7 — OpenRouter (E57, E58, E59, D18; Top-10 rank 6)

| ID | Claim as recorded in dossier | What the primary source says (verbatim, location) | Verdict |
|---|---|---|---|
| 7a | Rank 6 (l.230), E57, l.51: agentic overtook human "~1 Feb 2026" / "right around February 1st" | OR-blog (30 Jun 2026): *"The tokens used by agentic workloads surpassed those used by humans right around February 1st."*; *"We split token traffic at the API key level into three main categories (Agentic, Mixed, and Human)."*; *"Sample size: Over 450 trillion tokens from January 1, 2026 - June 14, 2026."* | ✅ **CONFIRMED** (re-checked). But see 7c: Walker's later LinkedIn post frames the date as 6 Feb (D18 patch). |
| 7b | Rank 6 (l.230): "agentic requests ≈15× human requests"; l.51/E57: "agentic requests use ~15× the tokens of human requests" | OR-blog: *"agentic work burns more tokens than normal human AI usage (about 15x more per request, according to OpenRouter data)."* | ✅ E57 and l.51 **CONFIRMED**. Rank 6's short form "agentic requests ≈15× human requests" is ⚠ **ambiguous** (reads as 15× as many requests); it is 15× **tokens per request**. Distinct from the "nearly 5×" aggregate agent-vs-human token-volume ratio in the a16z chart (7e; D70). |
| 7c | E58 (l.162), rank 6, l.51: "Agentic tokens grew 14× in ~6 months vs 2.8× for human tokens"; source LI-1, dated "Aug 2026" | LI-1 **not retrievable** (robots.txt). The post's URL slug reads "february-6th-2026-potentially-the-last…". Secondary (dec-14, 23 Aug 2026), quoting Walker: *"According to OpenRouter analyst Peter Walker, February 6, 2026, may have been the last day humans consumed more tokens than AI agents. Agentic token usage has grown 14x since then, while human usage is up just 2.8x."* and agent tokens *"jumped from 0.51 trillion to 7.3 trillion tokens"* (period unit of these totals not stated in the fetched text). a16z (via ppc; X-post search snippet): *"Agents burn nearly 5x the tokens people do, up 14x since February"*. Post date 11 Aug 2026 (calc. from activity ID); 6 Feb→11 Aug = 186 days ≈ 6.1 months (calc.); 7.3/0.51 = 14.3× (calc.). | ⚠ **PARTIALLY CONFIRMED / primary UNRESOLVABLE.** Two independent secondaries agree on 14× since early Feb 2026 and the-decoder on 2.8×; the post itself could not be read. Reference point is "since February 6" (a single day's crossover), so "~6 months" is correct (calc.). |
| 7d | E58, rank 6, l.51: "nearly 70% of agentic tokens are cached prompt tokens" | LI-1 not retrievable. dec-14: *"Nearly 70 percent of agent token consumption comes from cached prompts, which are billed at much lower rates, so actual costs aren't rising as fast as the raw numbers suggest."* ppc (reporting a16z Charts of the Week, 21 Aug 2026, "charts credited to Peter Walker"): *"More than 85% of agentic token burn originates in the cached prompt"*; getmegabrain (29 Aug 2026, citing the same a16z issue): *"over 85% of that agentic token burn is cached-prompt tokens"*. | ⚠ **CONFLICT, UNRESOLVABLE from primary.** Secondary reports of Walker's data give ~70% (LinkedIn post, 11 Aug) and >85% (a16z newsletter, 21 Aug). May be different windows or definitions (e.g. share of prompt tokens vs of all tokens); cannot tell without the charts. New D-entry. |
| 7e | (context) agent-vs-human token ratio | ppc: *"Agents on the OpenRouter network consumed close to five times as many tokens as human users"* (aggregate volume, a16z/Walker chart) vs OR-blog *"about 15x more per request"*. | ℹ Not a contradiction — different measures (aggregate volume ratio vs tokens per request). Must not be mixed on a slide. New D-entry. |
| 7f | E59 (l.163): "weekly tokens 0.5T (Jan 2025) → 126.2T (2026), '25,000%'" | OpenRouter primary: the live rankings page shows "Usage data through Sep 25, 2026" and per-model charts but **no platform-total weekly token figure** and no historical total; no OpenRouter blog post found with 0.5T / 126.2T / 25,000%. Secondary dec-25k (17 Sep 2026): *"On OpenRouter, weekly token consumption has surged more than 25,000 percent since January 2025, from 0.5 trillion to 126.2 trillion tokens."* — chart credited to Walker's LinkedIn post LI-2 (16 Sep 2026, calc.), not retrievable. 126.2/0.5 = 252× = +25,140% (calc.; internally consistent). | ⚠ **UNRESOLVABLE (primary)**; numbers are traceable to a named OpenRouter chart via one secondary. Also: the week of the 126.2T figure is not given (only "2026"; source dated mid-Sep 2026). Tokens include reasoning tokens (dec-25k notes "thinking" tokens inflate the count). |
| 7g | E59 (l.163): "Chinese open-weight share 39% → 66%+ (Jan→Apr 2026); US proprietary 61% → 34%" | **No primary found.** Not in OR-blog, OR-rank, OpenRouter's 27 Jun or 25 Aug 2026 posts, dec-25k, getmegabrain (cache article), or datagravity (24 Jun 2026: *"~61% of all tokens consumed on OpenRouter"* for Chinese open-weight models, no date range given). OR-blog (primary, 30 Jun 2026) says instead: *"2025 was the year of American tokens, with models from the US responsible for about 3/4ths of the tokens used. The competition has been far more fierce in 2026, with Chinese models actually surpassing American ones in token share as of early June."* | ❌ **UNRESOLVABLE, and in tension with the primary.** If Chinese share were 66%+ by April, Chinese models would already have surpassed US models before "early June". Possibly a different base (e.g. US-originating traffic, open-weight-only, a single week); cannot tell. New D-entry. Do not use. |
| 7h | E59 "OpenAI projected $14B loss in 2026" | Not checked (outside item 7's scope; no source in this pass contained it). | — Still open. |
| 7i | D19 "88%" | getmegabrain's cache-economics article (29 Aug 2026) does **not** contain "88%" (fetch). | ℹ No change to D19; the 88% remains unsourced. |

### P1 item 13a — EchoPath (arXiv 2609.16635)

| ID | Claim as recorded in dossier | What the primary source says (verbatim, location) | Verdict |
|---|---|---|---|
| 13a-1 | L347/L692: "success 91.2–92.8% on **159 OSWorld-Verified tasks** in a repeat-execution setting" | EP §3.1: *"We therefore use a paired two-pass design on OSWorld-Verified tasks. The first pass constructs candidate memories from fresh GUI execution, while the second pass reruns the same task entries and tests whether the expected memory can be retrieved, gated, rebound, and executed."* … *"The main analysis pool contained 159 active executable memories. Figure 3 summarizes action counts and first-pass construction cost."* Methods: *"Only episodes whose lifecycle state is active are exposed for default replay retrieval."* The paper never states how many OSWorld-Verified tasks were attempted in the first pass, how many failed, or the exclusion criteria; "369" (OSWorld's task count) does not occur. | ⚠ **PARTIALLY CONFIRMED / CORRECTED.** 159 is the number of tasks whose first-pass memory became *active* — a post-selection pool, not an OSWorld-Verified subset chosen in advance. The second pass is measured only on tasks the first pass already solved and validated (selection effect; first-pass attempts and success NR). "Repeat-execution setting" is correct (paired two-pass, same task entries). |
| 13a-2 | L347/L692: "success 91.2–92.8%" | EP **Table 1** "Second-pass memory replay results." (columns: Model / Success Rate / Execution Tokens Consumption / Second-pass time (seconds)):<br>`codex-gpt-5.5-medium | 91.2% | 20,370 [674–245,736] | 127.5 [14.5–529.3]`<br>`claude-sonnet-5-medium | 92.8% | 30,503 [481–111,710] | 139.3 [19.5, 570.7]`<br>`kimi-K3-medium | 87.3% | 19,928 [589–228,419] | 130.5 [15.2–627.6]`<br>`Synapse (codex-gpt-5.5-medium) | 91.8% | 586,386 [164,997–1,625,940] | 315.7 [110.1–1,272.5]` (a lead re-fetch returned the upper time bound as 1,272.3; every other cell identical)<br>Text: *"Codex EchoPath recalled the expected memory for all 159 tasks. It completed 145/159 matched tasks (91.2%)…"*; *"Comparable results were also achieved by Claude Code and Kimi Code."* Brackets = [min–max] across tasks. | ⚠ **CORRECTED.** EchoPath's success across the three host agents is **87.3–92.8%**, not 91.2–92.8% (Kimi-K3 87.3% omitted). The Synapse baseline itself reached **91.8%** — above Codex-EchoPath's 91.2%; the dossier does not record Synapse's success. |
| 13a-3 | L347/L692: "Median tokens **20,370 vs 586,386**; time **127.5 vs 315.7 s** — against a Synapse memory baseline" | Table 1 rows above: Codex-EchoPath (codex-gpt-5.5-medium) vs Synapse run on the **same** model (codex-gpt-5.5-medium). Text: *"As a planning augmentation baseline, Synapse reached comparable success rate at 91.8% but used 586,386 median tokens and 315.7 seconds."* Column name is "Execution Tokens Consumption" (second pass); time column "Second-pass time (seconds)" — the paper does not say explicitly that it is wall-clock, though "median execution time" in the abstract implies per-task elapsed time. | ✅ **CONFIRMED** (numbers, medians, same-model pairing). Reductions: tokens −96.5%, time −59.6% (calc.). Tokens are second-pass execution only; first-pass construction cost is separate (13a-5). |
| 13a-4 | L347/L692/L730/L746: baseline is "a Synapse memory baseline, not a no-memory agent" | EP ref. [15]: *"Longtao Zheng, Rundong Wang, Xinrun Wang, Bo An. Synapse: Trajectory-as-exemplar prompting with memory for computer control. In International Conference on Learning Representations, volume 2024, pages 19036–19066, 2024."* §3.1: *"Synapse [15] which converts action-trajectory to augmented action planner was reported for naive comparison between planning enhancement and our proposed replayable execution methods."* No no-memory second-pass baseline is reported. How Synapse received the first-pass trajectories is not described. | ✅ **CONFIRMED.** Synapse = trajectory-as-exemplar prompting (ICLR 2024), run on codex-gpt-5.5-medium; the authors themselves call it a "naive comparison". |
| 13a-5 | (new) no-memory reference point | Figure 3 caption: *"First-pass memory construction for 159 active OSWorld memories. The histogram shows wrapped GUI action steps per task; the inset reports construction-cost medians and 0.025-0.975 quantiles."* Text: *"Active tasks contained 2–29 recorded GUI actions with most tasks require 4 to 13 steps."* *"The median task token cost is about 572k tokens, and the median execution time is about 4.5 minutes."* *"Consolidation reduced about 30% of the exploration steps to final memory trajectories."* Abstract: *"EchoPath reduced median token cost by more than 90% and median execution time by about 60%."* | ⚠ **New nuance.** The first pass (fresh, memory-less execution of the same 159 tasks) is a de facto no-memory reference: ~572k tokens, ~4.5 min median — but it is the construction run (and only on tasks that ended up active), not a controlled baseline. The abstract does not say what "about 60%" is relative to: vs Synapse 315.7 s → −59.6% (calc.); vs first pass ~270 s → −52.8% (calc.). Tokens: −96.5% vs Synapse, −96.4% vs first pass (calc.). |
| 13a-6 | L510/L718/L746: "no work measures replay success across UI versions over time"; "EchoPath is a repeat-execution setting against a memory baseline" | §3.1: *"To avoid 'coordinate copying' style memory which replays every action simply using the same target coordinately, we intentionally shifted second-pass resolution from 1920 × 1080 in the first-pass to 1600 × 900."* Offline IBTR diagnostics (Table 2): *"Original-screen matching accepted 95.5% of 200 cases, and every accepted match had 0-pixel deviation. Under random scaling, the matcher accepted 190 cases with 188 within 2 pixels, 189 within 5 pixels."* Limitations: *"EchoPath is best suited to stable work environments with controlled application versions, window systems, browser profiles, fonts, themes, and software configurations since replay-time visual reaiming remains vulnerable to toolbar rearrangements, localization, responsive layouts, display scaling, and near-duplicate interface elements. The present diagnostics establish retrieval, offline visual binding, start-state gating, flexible-input enforcement, and storage behavior, but they do not yet establish live robustness under broad interface drift or enterprise-scale deployment."* | ✅ **CONFIRMED with a refinement.** No application-version / UI-layout-over-time experiment exists; the authors say so. But there **is** one controlled perturbation: every second-pass replay ran at a different screen resolution (1920×1080 → 1600×900), plus offline random-scaling tests of re-aiming. The dossier should say "display-resolution shift only". |
| 13a-7 | L347/L692/L718/L683: "lifecycle states (promote / repair / quarantine)"; "the most developed answer so far to 'reuse under drift'" | Methods: *"A validated and viable candidate can be promoted to active memory. If later reuse fails under changed state, the episode can be quarantined or forked into a repaired branch."*; the paper describes *"promotion, repair, branching, deprecation, and quarantine."* No counts of promotions, repairs, branches, deprecations or quarantines are reported anywhere. | ⚠ **PARTIALLY CONFIRMED.** The lifecycle is a described mechanism, **not evaluated**: no experiment exercises repair or quarantine. The "most developed answer to reuse under drift" is a design claim, not a measured one. |
| 13a-8 | (new) guard / gate accuracy — relevant to plan (a) fallback trigger | Table 3 (offline, 50 memories with pointer-action visual evidence): *"State Gate | Compatible start | Accept | 98%"*; *"State Gate | Partially changed start | Accept | 92%"*; *"State Gate | Incompatible start | Reject | 78%"*; flexible rebinding (50 active memories): *"Valid flexible variant | Accept | 100%"*, *"Invalid non-flex mutation | Reject | 100%"*. Retrieval stress test: *"Correct recall stayed at 100% accuracy with no wrong selections or misses as the active repository grew from 159 to 659 memories."* Storage: memory size *"less than 1 MB"* even for long trajectories. | ✅ New evidence (E-candidate). The start-state gate wrongly accepts **22%** of incompatible starts (calc. 100−78) in the offline test — the guard, not replay, is the weak point; directly relevant to plan (a)'s "de-optimize to LLM" trigger. |
| 13a-9 | (new) memory source vs plan (a)'s demo mixing | Limitations: *"memory acquisition currently depends on a first-pass agent attempting the task from the given instruction, rather than an interactive demonstration or user-guided recording procedure. As a result, gathering a replayable memory can still involve exploratory actions, failed attempts, and full task completion before consolidation, which may be inefficient for complex long-trajectory tasks."* | ✅ Confirms the dossier's differentiation "no human demos" (L692, L718, L746) from the authors' own text. |
| 13a-10 | "whether code is released" (§8.2 13a) | EP contributions paragraph: *"The OpenPath package is provided at: https://github.com/JackZhao1998/EchoPath.git"* (sic, "OpenPath"). WebFetch of https://github.com/JackZhao1998/EchoPath on 2026-09-27: **HTTP 404**. GitHub API `user:JackZhao1998` lists 10 public repos (EligMeta, BERT-sentiment, GPT2FineTuning, JackZhao1998, GPT2-TSForecastModel, SectorRotation, RL_BondTrading, PDF-Reader, RISW_Workshop_2026, BayesianWritingEvaluation) — none is EchoPath/OpenPath. A GitHub repository search for "EchoPath GUI agent memory" returned 0 results. | ❌ **Code NOT publicly available as of 2026-09-27** despite the paper's link (private, renamed or not yet pushed). A direct comparison (L730 baseline 12) would currently require re-implementation. |
| 13a-11 | L347/L692: authors "Zhao, Xu (JHU); Shanmugham, Roy (Amazon AGI) — arXiv Sep 2026" | EP title block: Yao Zhao (JHU Applied Mathematics and Statistics), Aditya Shanmugham (Amazon AGI), Swastik Roy (Amazon AGI), Yanxun Xu (JHU AMS; JHU School of Medicine Oncology). Identifier: *"arXiv:2609.16635v1 [cs.AI] 15 Sep 2026"*. | ✅ Confirmed (dossier groups by affiliation; byline order is Zhao, Shanmugham, Roy, Xu). Venue: none stated on the HTML page; abs-page Comments field unread (access note). |
| 13a-12 | (new) host agents and models | *"We use models and coding agent clients including Codex, Claude Code, and Kimi Code to conduct the main experiment."* Which agent built the first-pass memories, and whether each host replayed its own or a shared memory set, is not stated. | ⚠ Record the models as printed (codex-gpt-5.5-medium, claude-sonnet-5-medium, kimi-K3-medium); first-pass agent NR. |

### P1 item 13b — FocusAgent v1 vs TMLR (D48, D15)

Done together with P0 item 3 (same paper, same sources); see rows P1-13b-i to P1-13b-iv in the P0 item 3 block above. Verdict: **CORRECTED — no sign flip.** 32.3% (GPT-4.1 + GPT-4.1-mini retriever) is unchanged between v1 and v2; 39.6% is a different configuration (GPT-5-mini retriever) added in v2.

### P1 item 8 — HUMAN Security (E65)

| ID | Claim as recorded in dossier | What the primary source says (verbatim, location) | Verdict |
|---|---|---|---|
| 8a | E65 (l.169): "7,851% year-over-year growth in agentic web traffic" | H-land: *"7,851% Year-over-year growth in agentic AI traffic"*. H-GNW: *"Agentic AI is a novel category growing at an unprecedented rate."* … *"Traffic from AI agents and agentic browsers grew 7,851% year over year."* … *"And while the majority are exploring product listings, a growing number are accessing user accounts and checkout processes."* H-blog: *"Traffic generated by autonomous systems that can navigate and act on the web grew 7,851% year over year."* | ✅ **Figure CONFIRMED** (vendor). **Definition: PARTIAL** — "traffic from AI agents and agentic browsers" / "autonomous systems that can navigate and act on the web"; no list of agents/browsers, no classification method, no base volume and no share of total traffic on any public page. **Baseline: not stated**; the release frames all findings as 2025 ("In 2025, …"), so 2025 vs 2024 is implied, not explicit. The metric (requests? sessions? interactions?) is not named. Rest **UNRESOLVABLE** (full report not publicly retrievable). |
| 8b | E65: ">1 quadrillion web interactions analyzed" | H-news: *"In 2025, HUMAN's Defense Platform analyzed more than one quadrillion digital interactions, revealing an internet increasingly shaped by the rapid rise of AI-driven traffic—up 187% from January to December—and a growing diversity of automation behind it."* | ✅ **CONFIRMED, scope clarified**: the sample is interactions seen by **HUMAN's Defense Platform** (its customers' properties) during calendar 2025 — not the whole web. |
| 8c | E65: "automated traffic growing ~8× faster than human" | H-news: *"Automation is growing eight times faster than human traffic, …"*; H-GNW: *"In 2025, automated traffic across the internet grew 23.51% year over year, while human traffic increased 3.10% over the same period."* 23.51/3.10 = 7.58× (calc.). | ✅ **CONFIRMED** (vendor rounding of 7.6×, calc.). Note "automated traffic" (all bots) ≠ "agentic traffic". |
| 8d | E65 date "Apr 2026" | H-news and H-blog dated March 26, 2026; H-GNW London re-release April 09, 2026. | ⚠ **CORRECTED (minor)**: first release 26 Mar 2026. |
| 8e | (additional) | H-GNW: *"Monthly AI-driven traffic rates grew 187%, nearly tripling over the calendar year."* | ℹ Jan→Dec 2025 monthly volume, "AI-driven" (broader than agentic). |

### P1 item 9 — "Agentic AI Workload Characterization" (2605.26297) and AgentRace (D36, E29)

| ID | Claim as recorded (dossier line) | What the primary source says | Verdict |
|---|---|---|---|
| 9a | E29 (l.102): "84.6–99.5% KV-cache hit ratio; 91.0–98.6% of LLM time in decode"; source "Agentic AI Workload Characterization … (v2 exists)" | arXiv 2605.26297 **v1** (25 May 2026), Yichao Yuan, Ankita Nayak, Souvik Kundu, Nishil Talati, title *"Agentic AI Workload Characteristics"*. Fig. 8 caption: *"The theoretical cache-hit ratio is consistently high, ranging from 87.9–99.3%, and the empirical cache-hit ratio is similarly high, ranging from 84.6–99.5%."* Fig. 9 caption (fragments returned): *"decode dominates runtime because prefix/context caching turns most of the input into reusable state"*; *"decode accounts for 91.0–98.6% of LLM time"*. Setup: *"two open-weight LLMs: Qwen3.6-27B and Gemma4-31B"*; benchmarks *"ADE-Bench, DABStep, GAIA, SWE-bench Pro, and Terminal-Bench 2.0"*; *"All experiments are conducted on a server equipped with two NVIDIA H100 NVL GPUs"*; *"We serve all models using vLLM v0.20.0"*. Abstract: *"…with effective context caching, most input tokens are reused across turns, making execution decode-dominated while increasing dependence on long-lived KV-cache state."* | ✅ **Numbers CONFIRMED (in v1).** ⚠ **Title corrected** ("Characteristics"). ⚠ **v2 not found:** the abs page on 2026-09-27 lists only v1; the direct v2 URL was rate-limited (429), so "v2 exists" is unconfirmed and the dossier's v2 URLs (l.492, l.925) should point to v1. Workloads are ReAct agents across data-analysis, QA and coding benchmarks, not only coding. |
| 9b | D36 (l.816): G attributes to "AgentRace"; "AgentRace is a different OpenReview paper" | Project page https://agent-race.github.io/ : title *"AgentRace: Benchmarking Efficiency in LLM Agent Frameworks"*; description *"The first benchmark specifically designed to systematically evaluate the efficiency of LLM agent frameworks across representative workloads."* Code link is anonymous (*anonymous.4open.science/r/AgentRace-922A*); no authors or venue on the page. OpenReview PDFs (titled "AGENTRACE: BENCHMARKING EFFICIENCY IN LLM AGENT …" per search index) returned 403; forum pages behind a browser-verification wall. Page text has no KV-cache/cache-hit/decode sentence. | ✅ **Different paper CONFIRMED** (different title, topic = agent-framework efficiency benchmark; anonymous double-blind submission). **Authors/venue UNRESOLVABLE** (anonymous on public pages; OpenReview 403). |

### P1 item 10 — Gemini 3.5 Flash-Lite computer use (D28) and Gemini 3.8 Flash throughput (E79)

| ID | Claim as recorded in dossier | What the primary source says (verbatim, location) | Verdict |
|---|---|---|---|
| P1-10a | D28 (l. 808): "O's slug reads 'gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber'" — "Verify the model name in the primary post" | G-FL title: *"Introducing Gemini 3.6 Flash, 3.5 Flash-Lite, and 3.5 Flash Cyber"*, 21 Jul 2026, Tulsee Doshi. *"3.5 Flash-Lite: Our fastest, most cost-effective 3.5-class model, delivering 350 output tokens per second"*; *"3.5 Flash-Lite is the fastest model in the 3.5 series."* | ✅ **CONFIRMED / D28 resolved.** The slug is correct: one post launched three models; the model is "Gemini 3.5 Flash-Lite". |
| P1-10b | E79 (l. 193): "Gemini 3.5 Flash-Lite native computer use at $0.30/$2.50 per M and ~350 tok/s (21 Jul 2026)" | G-FL: *"Priced at $0.3/1M input tokens and $2.5/1M output tokens"*; *"It also has computer use as a built-in tool to reliably support these agentic tasks"*; *"Computer use is now a built-in client side tool via the Gemini API"*; 350 output tok/s as above. G-docs model page `gemini-3.5-flash-lite`: Computer use *"Supported (Preview)"*; "Latest update: July 2026". AA-FL: *"At 349 tokens per second, Gemini 3.5 Flash-Lite is notably fast"*, speed rank *"#5 / 174"* (no measurement date shown). | ✅ **CONFIRMED** (price, date, built-in computer use). Label "~350 tok/s" as **vendor claim** (Google), independently ≈349 t/s on AA (undated page). Computer use is **Preview** on the model page — "native" is Google's "built-in tool", not GA. |
| P1-10c | E79: "computer use built into Gemini 3.5 Flash (24 Jun 2026)" | G-CU35: *"Introducing computer use in Gemini 3.5 Flash"*, Jun 24, 2026; computer use is *"a built-in tool supported in Gemini 3.5 Flash, delivering our best performance yet for agentic computer use tasks."* The post contains **no** speed, latency or tokens/s statement (benchmarks only in an image). | ✅ CONFIRMED. |
| P1-10d | E79: "'4× faster' claims at 3.5 Flash launch" | G-35 (19 May 2026, model launch — five weeks before computer use was added): *"When looking at output tokens per second, it is 4 times faster than other frontier models."* | ✅ CONFIRMED as **vendor marketing**; it is output tokens/s vs unnamed "other frontier models", not task speed, and it predates the computer-use post. |
| P1-10e | E79: "Gemini 2.5 Computer Use (7 Oct 2025)" | G-25CU: dated *"Oct 07, 2025"*; *"outperforms leading alternatives on multiple web and mobile control benchmarks, all with lower latency."* | ✅ CONFIRMED (date). |
| P1-10f | E79: "Gemini 3.8 Flash ~305 tok/s ('fastest measured by Artificial Analysis')" | AA-38 (model page, read 2026-09-27, **no measurement date shown**; only *"Gemini 3.8 Flash (high) was released on September 2, 2026"*): *"Gemini 3.8 Flash (high) generates output at 329.7 tokens per second (based on Google's API), which is well above average compared to other reasoning models in a similar price tier (median: 77.1 t/s)."* Speed rank shown: *"#2 / 211"*. Definition: *"Tokens per second received while the model is generating tokens (ie. after first chunk has been received from the API for models which support streaming)."* TTFT displayed: *"18.95s"*. AA-38a (2 Sep 2026): *"On high reasoning, Gemini 3.8 Flash averages ~300 output tokens per second"*; *"Time per Task of 2.5 minutes … On low reasoning, Time per Task falls to 0.8 minutes"*. G-38 makes **no** tokens/s or Artificial Analysis claim — only *"at the same speed and low cost of 3.7"*. The "305" and "fastest" wording comes from beam (secondary): *"It runs at about 305 tokens a second, the fastest any independent lab has clocked"*. | ❌ **CORRECTED.** AA's own pages give **~300 t/s at launch (2 Sep 2026)** and **329.7 t/s, rank #2 of 211** on the model page read 27 Sep 2026 (undated). "305" and "fastest measured" are beam.ai's, not AA's, and the current AA rank contradicts "fastest". Variant is "(high)" reasoning; throughput is post-first-chunk decode speed, not task time. |
| P1-10g | E79/l. 644: "$0.75/$3.75 introductory through 31 Dec 2026, then $1.50/$7.50 (2 Sep 2026)" | G-38 (2 Sep 2026): *"$0.75 per million input tokens and $3.75 per million output tokens"*, introductory rate expiring December 31, 2026, after which *"$1.50/1M input tokens and $7.50/1M output tokens."* (the end-date sentence came back paraphrased by the tool; prices verbatim). AA-38a: *"$0.75/$3.75 per 1M input/output tokens through the end of the year"*. | ✅ CONFIRMED. |
| P1-10h | Computer use on 3.8 Flash (implied by E79 heading) | G-38: no sentence mentions computer use. G-docs computer-use page uses *"gemini-3.8-flash"* and *"gemini-3.5-flash"* in code examples and points to "Model versions" for the supported list. | ⚠ Not claimed in the 3.8 launch post; docs examples imply support. Not needed by E79 as worded. |

### P1 item 11 — Operator retirement (D29, E39) and Opus 4.8 cache-preserving updates (E83)

| ID | Claim as recorded in dossier | What the primary source says (verbatim, location) | Verdict |
|---|---|---|---|
| P1-11a | E39 (l. 117) / D29 (l. 809): "standalone Operator retired 31 Aug 2025 into ChatGPT agent"; "find OpenAI's primary notice" | OA-agent (17 Jul 2025): *"The Operator research preview site will remain functional for a few more weeks, after which it will be sunset."* OA-rn, entry **July 17, 2025**: *"With ChatGPT agent's built-in virtual browser, the core functionality of Operator has been integrated. The standalone Operator experience at operator.chatgpt.com will be deprecated in the coming weeks."* OA-op editor's note: *"July 17, 2025 update: Operator is now fully integrated into ChatGPT as ChatGPT agent. … As a result, the standalone Operator site (operator.chatgpt.com) will sunset on in the coming weeks."* (sic). OA-help (current): *"Operator functionality is now integrated into ChatGPT agent mode. The Operator website is no longer accessible."* | ✅ **Primary notice found** (17 Jul 2025). ⚠ **The 31 Aug 2025 date is UNRESOLVABLE from an accessible primary:** no accessible OpenAI page gives a shutdown date. The dedicated "Operator – Release Notes" help article (10561834) now returns 404 and the archive copy was blocked. Wikipedia states "shut down on August 31, 2025" citing that article (secondary). A secondary X post by Niels Rogge dated 1 Aug 2025 (ID-decoded, calc.) says *"Today, OpenAI has sunset their Operator demo"* — conflicting. |
| P1-11b | D29: retired "due to latency" (G via tracker) | OA-agent, OA-rn, OA-op: the only stated rationale is integration (*"the core functionality of Operator has been integrated"*; *"Operator is now fully integrated into ChatGPT as ChatGPT agent"*). OA-agent contains no sentence about speed or latency. | ✅ **Resolved: latency is NOT a stated reason.** OpenAI gives consolidation into ChatGPT agent as the reason; "due to latency" is the tracker's interpretation. |
| P1-11c | E39 / D33: "38.1% OSWorld, 87.0% WebVoyager (Jan 2025)" in "Introducing Operator" | OA-op does **not** print the numbers (only *"sets new state-of-the-art benchmark results in WebArena and WebVoyager"*). OA-cua (23 Jan 2025): *"CUA achieved 38.1% success rate on OSWorld for full computer use tasks, and 58.1% on WebArena and 87% on WebVoyager for web-based tasks."*; table: OSWorld 38.1% vs prior SOTA 22.0%, human 72.4%; WebVoyager 87.0% vs 56.0%. | ✅ Numbers CONFIRMED, **source corrected**: they are in the "Computer-Using Agent" research post, not "Introducing Operator"; they are CUA (the model powering Operator) scores. |
| P1-11d | E83 (l. 197): "Anthropic Opus 4.8 API: update instructions/tools mid-task without breaking the prompt cache" | A-48 (28 May 2026), section "Also launching today": ***"The Messages API now accepts system entries inside the messages array.*** *Developers can update Claude's instructions mid-task without breaking the prompt cache or routing the update through a user turn. This can be used in a given harness to update permissions, token budgets, or environment context as an agent runs."* No sentence in the post ties **tools** / tool definitions to this feature (checked twice). | ⚠ **PARTIALLY CONFIRMED / CORRECTED.** The Opus 4.8 launch covers **instructions** (system messages) only. |
| P1-11e | E83 "tools" part | A-docs, title *"Mid-conversation system messages and tool changes"*; opening: *"Change system instructions or tool availability partway through a conversation without invalidating the cached prefix that came before them."* On tools: *"The `tools` array sits even earlier in the hashed request prefix than the top-level `system` field, so editing it invalidates the prompt cache for the entire conversation. … declare the full tool set in `tools` up front, then use `tool_addition` and `tool_removal` blocks to offer a tool to the model, or withdraw it, from a specific point in the conversation onward. The `tools` array itself never changes, so the cached prefix stays intact."* Availability: *"This feature is available on Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, Claude Opus 5.5, Claude Opus 4.8, and Claude Opus 5. No beta header is required for mid-conversation system messages. This feature is not available on Claude Sonnet 5."* Beta headers listed include `mid-conversation-tool-changes-2026-07-01`. | ✅ Tool changes exist, but as a **separate, later, beta** docs feature (header dated 2026-07-01, inferred from its name) and cache preservation works by **declaring all tools up front and toggling availability**, not by editing tool definitions. Cite the docs page, not the Opus 4.8 post, for tools. |

### P1 item 12 — Temporal wording (E70) and LangChain date (D24, E68)

| ID | Claim as recorded in dossier | What the primary source says (verbatim, location) | Verdict |
|---|---|---|---|
| P1-12a | E70 (l. 179): "79.8% say agent operating cost is a meaningful factor in usage decisions" | T, section "What's holding teams back from using AI agents more?": headline sentence *"79.8% say token and compute costs limit their progress."* followed by *"Companies are realizing with chagrin that in some cases, tokens can be quite expensive. The successful are 1.3x more likely to say cost is at least somewhat of a factor (83.1% vs 65.7%). Everyone else is more likely to say they're unsure (22.1% vs 7.3%)."* Chart title: *"Chart 3.4 — Is the cost of running AI agents a meaningful factor in your decision to use AI agents?"* Answer options and their percentages were **not** rendered as text (chart image). | ✅ **Question wording CONFIRMED** (Chart 3.4). ⚠ The report's own headline reframes the answer as "limit their progress", which is stronger than the question. The "at least somewhat of a factor" wording suggests 79.8% sums more than one answer option (inference; options not visible). |
| P1-12b | E70: "91.1% perceive productivity improvements" | T, section "What effect have AI agents had on you and your organization?": *"91.1% say AI agents have 'improved' or 'revolutionized' their productivity. Nearly everyone agrees that agents make developers more efficient. Only 4.0% said they had no impact and just 1.8% said agents had worsened their productivity."* Chart title: *"Chart 2.1 — How have AI agents altered your own productivity?"* | ✅ CONFIRMED. Self-reported; 91.1% = two top options combined ("improved" + "revolutionized"). |
| P1-12c | E70 sample/date: "554 … 29 Apr–25 May 2026"; "25 Aug 2026" | T: *"Published August 25, 2026"*; *"Between April 29 to May 25, 2026 we commissioned the survey provider Qualtrics to solicit responses from 650 respondents currently using AI agents following strict criteria around role and location. We removed all responses we considered low quality and were left with 554 respondents."* | ✅ CONFIRMED; add: Qualtrics panel, 650 solicited → 554 kept. ("mostly coding usage" not re-checked.) |
| P1-12d | D24 (l. 804) / E68 (l. 177): LangChain publication date "resource listing 25 Feb 2026" vs secondary "23 May 2026" | LC byline, between H1 and introduction: *"12 June, 2026"*. Intro: *"As we enter 2026, organizations are no longer asking whether to build agents, but rather how to deploy them reliably, efficiently, and at scale."* Methodology: *"1340 responses"* collected *"from Nov 18th-Dec 2nd, 2025"*. Barriers: *"one third of respondents cited quality as their primary blocker"*; *"Latency has emerged as second biggest challenge (20%)"*; *"cost is less frequently cited as a concern than in previous years."* No "published"/"updated" label on the date. | ⚠ **PARTIALLY RESOLVED.** The only date on the primary page is **12 June 2026**, which cannot be the first publication date: KDnuggets (secondary, 17 Mar 2026) already calls the report *"recently released"*, and LangChain's own LinkedIn post "state-of-agent-engineering-2025" has an activity ID that decodes to **16 Dec 2025** (calc.; post text not readable, robots-blocked). LangChain's call for responses on X decodes to 18 Nov 2025 (calc.), matching the fielding start. Best reading: first published ≈ mid-Dec 2025 (inferred), page re-dated 12 Jun 2026. Neither 25 Feb nor 23 May 2026 is supported by the primary page. |
| P1-12e | E68: "latency #2 (20%)", "1,340" | as above | ✅ CONFIRMED. "Quality #1 (32%)": page text says *"one third"*; 32% not seen in text (chart) — not re-checked. |

### P1 item 13 — Measuring Agents in Production (E69, D25)

| ID | Claim as recorded in dossier | What the primary source says (verbatim, location) | Verdict |
|---|---|---|---|
| P1-13a | E69 source "v4 Jun 2026" | MAP-abs submission history: *"[v1] Tue, 2 Dec 2025 … (337 KB)"*, *"[v2] Fri, 30 Jan 2026 … (345 KB)"*, *"[v3] Tue, 3 Feb 2026 … (345 KB)"*, *"[v4] Thu, 4 Jun 2026 19:57:38 UTC (340 KB)"*. Comments: *"Accepted to the 43rd International Conference on Machine Learning (ICML 2026) as Oral Presentation"*. | ✅ CONFIRMED (4 versions; v4 = 4 Jun 2026). |
| P1-13b | E69: "14.8% … critical deployment blocker, marginal-but-sufficient for 59.3% (N=27)" | **v2** Appendix B.4.2 "Latency Challenges": *"Figure 12b shows that only 14.8% of deployed survey agents identify latency as a critical deployment blocker requiring immediate resolution, while the majority (59.3%) report it as a marginal issue, where current latency is suboptimal but sufficient for deployment."* Figure 12 caption: *"Supplementary deployment characteristics of agentic systems (N=27–29). (a) Overview of data ingestion … (b) Degree to which latency is reported as a deployment challenge. The results suggest that latency is rarely a strict blocker for most deployed agentic systems."* **v4**: §4.4 still points to the section (*"voice agents operating at human conversation speeds (C04-05), where latency becomes the primary deployment challenge (Section B.4.2)"*) and the appendix lists "B.4.2 Latency Challenges", but the body text could not be read through the fetch tool. **v1** §7 overview: *"Latency impacts only a small subset (15%) of applications as a deployment blocker, and security represents a manageable concern that most deployed agents mitigate through action and environment constraints."* | ⚠ **PARTIALLY CONFIRMED.** 14.8% and 59.3% are verbatim in v2 B.4.2; "(N=27)" is **not printed** — the figure prints "N=27–29" for both panels. 4/27 = 14.8% and 16/27 = 59.3% (calc.), so N=27 for panel (b) is consistent but inferred. Presence of the sentence in v4 **not confirmed** (appendix unreadable). Note: v4 dropped the latency sentence from §7 (its §7 intro lists only reliability, evaluation, security). |
| P1-13c | E69: "66% allow response times of minutes or longer, 17% set no limit (N=53)" | v4 §4.4 "Latency Requirements": *"Survey data shows production agents tolerate surprisingly relaxed latency: 66% allow response times of minutes or longer, and 17% set no explicit limit (Figure 4)."* Figure 4 caption: *"Reported tolerable end-to-end response latency for deployed agentic systems (N=53)."* | ✅ CONFIRMED in v4. |
| P1-13d | E69: "only 5 of 20 interviewed systems need real-time responsiveness; 15/20 run asynchronously" | v4 §4.4: *"Fifteen of 20 case studies can operate asynchronously; some even batch process requests hourly or overnight. For these applications, minute-scale latency beats the alternative human completion time."* and *"Only 5 of 20 cases require real-time responsiveness."* v1 §4.4 (different wording): *"Among our 20 detailed case studies, only 5 require real-time responsiveness. The remaining 15 cases tolerate extended processing times: 7 involve human review with relaxed timing, 5 operate as asynchronous background processes, and 3 have hybrid operation patterns."* | ⚠ **CONFIRMED with a wording correction.** v4 says 15/20 **"can operate asynchronously"**, not "run asynchronously"; v1's breakdown shows only **5 of 20** actually run as asynchronous background processes (7 human-review, 3 hybrid). |
| P1-13e | E69: runtime costs "remain negligible compared to alternative expert labor costs" | v4 §5.1: *"Model selection is based on empirical testing. Engineers evaluate the most powerful accessible models and selecting based on downstream performance. These teams report that runtime costs remain negligible compared to alternative expert labor costs (e.g., medical professionals, senior engineers), justifying the use of expensive frontier models."* (v1 wording: *"runtime costs are negligible compared to the human experts … that the agent augments"*.) | ✅ CONFIRMED (v4 wording). It is teams' report, not a measured cost comparison. |
| P1-13f | E69: "306 practitioners (Jul–Oct 2025) + 20 interviews; 86 in production/pilot" | v4 §3.2: *"… from July 28 to October 29, 2025, targeting practitioners who build agent systems. We received 306 valid responses … and 26 application domains … We filtered responses to 86 data points explicitly in production or pilot phases."* | ✅ CONFIRMED. |
| P1-13g | D25 (l. 805) / E69: venue "PDF header ICML 2026, IBM page says ICLR 2026" | MAP-abs Comments: ICML 2026 Oral. ICML (official virtual site, poster 61834): title *"Characterizing Agents in Production"*, same 25 authors, *"Oral 6B Agentic Systems"*, poster *"Wed, Jul 8, 2026"*; abstract: *"We present the first systematic study of Characterizing Agents in Production (CAP) using first-hand data from agent developers."* OpenReview forum `mWxEAgz3xu` linked. IBM: *"Measuring Agents in Production for ICLR 2026"*, 23 Apr 2026. A separate OpenReview forum titled "Measuring Agents in Production" (`AsvLggSOvS`) exists per search but could not be opened. | ✅ **Resolved: ICML 2026 (Oral).** The ICML version is titled **"Characterizing Agents in Production" (CAP)**. The IBM "ICLR 2026" listing is probably an ICLR 2026 workshop version (unverified: OpenReview blocked). The ICML PDF header itself was not read. |

### P1 item 13c — Ares (D49), StepWise (D47), AWO (D45), WALT (D42)

| ID | Claim as recorded in dossier | What the primary source says (verbatim, location) | Verdict |
|---|---|---|---|
| 13c-A1 | D49 / L452: O2 "WebArena fixed-high→Ares: 21,424→11,723 reasoning tokens/task, SR 45.0→46.5%" | ARES v1 **Table 1**, caption: *"Main evaluation results in TAU-Bench, BrowserComp-Plus, and WebArena, using gpt-oss-20b as the backbone LLM."* Columns per benchmark: Acc. (%), Δ_m Acc, S (steps), T_total, Δ_token, T_task, Δ_token, T_step, Δ_token. WebArena rows:<br>`High | 45.0 | ↑ 1.5 | 10.0 | 2763k | ↓ 1251k | 21424 | ↓ 9701 | 2154 | ↓ 830`<br>`ARES | 46.5 | - | 8.9 | 1512k | - | 11723 | - | 1324 | -`<br>Text: *"ARES surpasses the high effort baseline (46.5% vs. 45.0%)"*. Agent scaffold: AgentOccam. | ✅ **CONFIRMED.** 21,424 / 11,723 are T_task = reasoning tokens **per task**; totals 2,763k → 1,512k. Per-task reduction −45.3% (calc.); steps 10.0 → 8.9. T_total ÷ T_task ≈ 129 tasks (calc., both rows) → a WebArena **subset** of ≈129 of 812 tasks; the subset definition was not captured. |
| 13c-A2 | D49 / L452: C15 "16.4→17.2%" WebArena SR | Searched v1 (only version): the strings "16.4" and "17.2" do not occur. | ❌ **CORRECTED — C15 extraction error.** Not in the paper. Drop. |
| 13c-A3 | L452: C15 "~35–37% [fewer reasoning tokens] on TAU-Bench / BrowseComp-Plus / WebArena" | Table 1 T_total (High → ARES): TAU-Bench Retail 1007k → 652k; Airline 873k → 678k; BrowseComp-Plus 1841k → 1071k; WebArena 2763k → 1512k. Abstract: *"reduces reasoning token usage by up to 52.7% compared to fixed high-effort reasoning, while introducing minimal degradation in task success rates."* | ⚠ **CORRECTED.** Reductions (calc.): Retail −35.3%, Airline −22.3%, BrowseComp-Plus −41.8%, WebArena −45.3%. "~35–37%" fits Retail only. The abstract's "up to 52.7%" was not located in Table 1 (possibly a per-step or other metric) — still open. |
| 13c-A4 | L452: "TAU-Bench Retail 54.8→54.8%; **uniformly low effort drops to 35.0% (≈−20 pp)**" | Table 1, TAU-Bench Retail: Low 35.0% (25k), Medium 47.3%, High 54.8% (1007k), Random 43.5%, GPT-5 40.0%, Gemini 3 Pro 46.1%, ARES 54.8% (652k). WebArena: Low 37.4%, Medium 42.6%, Random 40.3%, GPT-5 41.1%, Gemini 3 Pro 41.9% (single fetch). | ✅ Confirmed for **TAU-Bench Retail** (−19.8 pp, calc.). On WebArena uniform Low costs −7.6 pp (calc.). State the benchmark. |
| 13c-A5 | L452: "BrowseComp-Plus −41.8% tokens, 42.7→41.3%" | Table 1 BrowseComp-Plus: High 42.7% (1841k), ARES 41.3% (1071k). | ✅ CONFIRMED (−41.8% calc. on T_total). |
| 13c-S1 | D47 / L415 / L260: O1 "EvoCUA-8B + selective Sonnet 4.5 vs always-Sonnet: $0.881→$0.224/task (−74.6%), 6.4→4.1 s/request, SR 58.1→55.4%" | SW v1 **Table 1 (OSWorld)**, columns Small / Large / Lat./Req. / Cost/Task / Acc. / Avg Step / Switched / A1 Share / A2 Share:<br>`– | Claude Sonnet 4.5 | 6.4s | $0.881 | 58.1% | 25.4 | – | – | –`<br>`EvoCUA-8B | Claude Sonnet 4.5 | 4.1s | $0.224 | 55.4% | 26.2 | 168 (46.8%) | 60.6% | 39.4%`<br>Abstract: *"reducing inference cost by up to 74.6% and latency by up to 45.8%."* | ✅ **CONFIRMED.** −74.6% cost (calc. 74.57%), −35.9% latency per request (calc.). Latency is **per request**, not per task. |
| 13c-S2 | D47 / L415: C15 "other configurations 58.2–59.3% vs 60.1% always-large ('recovers 95%+'), up to −45.8% latency" | SW Table 1:<br>`– | Kimi K2.5 | 8.3s | $0.132 | 60.1% | 22.4 | – | – | –`<br>`EvoCUA-8B | Kimi K2.5 | 4.5s | $0.051 | 58.2% | 25.2 | 173 (48.2%) | 59.5% | 40.5%`<br>`Qwen3-VL-8B | Kimi K2.5 | 6.5s | $0.078 | 59.3% | 23.7 | 240 (66.9%) | 37.4% | 62.6%`<br>Text: *"EvoCUA-8B + Kimi K2.5 achieves 58.2% success at only $0.051 per task, reducing the cost by 61.4%."* No sentence contains "95%". | ✅ **CONFIRMED, configuration identified.** 58.2–59.3% vs 60.1% are the two **Kimi K2.5** cascades vs always-Kimi K2.5 (OSWorld). "Up to −45.8% latency" = EvoCUA-8B + Kimi K2.5 (4.5 vs 8.3 s/request, calc. 45.8%). "Recovers 95%+" is C15's paraphrase, not the paper's (58.2/60.1 = 96.8%, 59.3/60.1 = 98.7%, calc.). The abstract's two "up to" figures come from **different configurations** (cost: EvoCUA+Sonnet; latency: EvoCUA+Kimi). |
| 13c-S3 | (new) other SW rows | Table 1 also: `EvoCUA-8B | – | 2.6s | $0.022 | 43.3%`; `Qwen3-VL-8B | – | 3.9s | $0.018 | 30.8%`; `Qwen3-VL-8B | Claude Sonnet 4.5 | 5.2s | $0.423 | 54.3%`. **Table 2 (WebArena):** `– | GPT-5.2 | 19.6s | $0.335 | 60.1% | 9.9`; `gpt-oss-20b | GPT-5.2 | 12.2s | $0.211 | 57.8% | 10.3`; `– | GPT-5 mini | 11.1s | $0.053 | 55.0% | 13.8`; `gpt-oss-20b | GPT-5 mini | 8.5s | $0.027 | 51.3% | 12.1`; `AgentTrek-32B | GPT-5.2 | 13.4s | $0.208 | 58.8% | 12.0` (one AgentTrek-32B + GPT-5 mini row came back with a missing cell). | Note: **60.1%** appears twice — always-Kimi K2.5 on OSWorld and always-GPT-5.2 on WebArena; C15's "vs 60.1%" is the OSWorld one (the 58.2/59.3 rows are OSWorld). |
| 13c-W1 | D45 / L49 / L261: O1 "21.8→19.2 calls (−11.9%), 69.6→73.2% (+3.6 pp)" | AWO v1 **Table 9** *"Results for the APPWORLD benchmark."* (columns GPT 5.1 Base / AWO, Claude 4.5 Base / AWO, GPT-OSS Base / AWO):<br>`Task success rate | 69.6% | 73.2% | 89.3% | 85.7% | 14.3% | 16.1%`<br>`Total LLM call count | 3665 | 3229 (-11.90%) | 2801 | 2588 (-7.60%) | 2137 | 2226 (+4.20%)`<br>`E2E latency (hours) | 12.44 | 9.37 | 3.53 | 4.11 | 3.32 | 3.49`<br>`LLM call/task | 21.8 | 19.2 | 16.7 | 15.4 | 13.2 | 12.7`<br>`Task duration (average in seconds) | 266.6 | 200.8 | 75.6 | 88.1 | 71.1 | 74.8` | ✅ **CONFIRMED** as **GPT 5.1 on AppWorld** (Table 9, v1). |
| 13c-W2 | D45: C15 "11.9% fewer calls, **+4.2 pp**" | AWO v1 **Table 7** (overall VisualWebArena task success, Base → AWO): GPT 5.1 20.9% → 21.5%; **Claude 4.5 25.0% → 29.2%**; GPT-OSS 6.1% → 10.9%. Text: *"we observe that AWO improves the task success rates by up to 4.2 percentage points"*; abstract: *"reduces the number of LLM calls up to 11.9% while also increasing the task success rate by up to 4.2 percent points"*; *"This reduction ranges from 5.6% to 10.2% for VISUALWEBARENA and from 7.2% to 11.9% for APPWORLD."* | ✅ **RESOLVED — both correct, different cells.** −11.9% calls = GPT 5.1 / AppWorld; +4.2 pp = **Claude 4.5 / VisualWebArena** (25.0 → 29.2). C15 paired the two abstract "up to" maxima, which come from different model × benchmark cells. Note: GPT-OSS on VWA gains +4.8 pp (calc.), more than "up to 4.2" — the abstract's range apparently covers GPT 5.1 and Claude 4.5 only (inference). "4.20%" also appears in Table 9 as GPT-OSS's call-count **increase** — a different quantity. |
| 13c-W3 | **L49 (Part I key finding 4):** "AWO/meta-tools: calls fall 21.8→19.2 but time rises 75.6→88.1 s with Claude" | Table 9: 21.8 → 19.2 calls/task is **GPT 5.1** (whose duration **falls** 266.6 → 200.8 s); **Claude 4.5**: calls/task 16.7 → 15.4, duration 75.6 → 88.1 s, success 89.3% → 85.7%. | ❌ **CORRECTED — L49 mixes two models.** The Claude counterexample is real, but its calls are 16.7 → 15.4, not 21.8 → 19.2. L261 already states it correctly. |
| 13c-W4 | (new) second fewer-steps-but-slower case | AWO v1 **Table 8** (per-dataset VWA): `Classifieds | GPT 5.1 | 24.5% | 2461 | 8.14 | _` / `GPT 5.1 w/ AWO | 22.9% | 2427 | 11.72 | 17.0%` (columns: Task success rate / Total Steps / Duration (hrs) / Meta-tool Usage). | New supporting datum for "fewer calls ≠ faster": GPT 5.1 on VWA-Classifieds, steps 2461 → 2427, duration 8.14 → 11.72 h (+44%, calc.), success 24.5 → 22.9%. |
| 13c-L1 | D42 / L316: O3 "57.5→61.5% (GPT-5-mini matched), 66.0% with human-demo tools"; "8.9→6.5 steps … human-demo tools 7.4 steps" | WALT v1 **Table 2**, caption: *"Ablations on VisualWebArena-Classifieds showing the impact of different components on success rate (SR) and average number of steps."* Columns: browser LLM / tools / dom-parser / verify / avg #steps (↓) / SR (%) ↑ (subscripts = relative change vs the gpt-5-mini "none/text/self" row):<br>`gpt-5-mini | none | text | self | 8.9 | 57.5`<br>`gpt-5-mini | discovered | text | self | 6.5 (−27.0%) | 61.5 (+7.0%)`<br>`gpt-5-mini | human demo | text | self | 7.4 (−16.9%) | 66.0 (+16.2%)` | ✅ **CONFIRMED.** 61.5% = discovered tools with text DOM parser and self-verification. The "+7.0%" is **relative** (+4.0 pp, calc.); the text's *"GPT-5-mini: 7% higher success rate, 27% fewer steps"* is also relative. |
| 13c-L2 | D42: C15 "57.5→64.1%, 1.3–1.4× fewer steps, −21.3% steps" | Table 2: `gpt-5-mini | discovered | multimodal | external | 7.0 (−21.3%) | 64.1 (+11.5%)` — the **full WALT** configuration; text: *"Impressively, however, WALT is able to recover most of this performance fully autonomously (64.1%), with 5% fewer steps."* Abstract/intro: *"Ablation studies further reveal that our proposed contributions — discovered tools, multimodal DOM parsing, and external verification — yield gains in both success rates (10%-30% across splits) and efficiency (1.3-1.4x fewer steps on average)."* Table 1 (main results) reports WALT 64.1% on VWA Classifieds. | ✅ **RESOLVED — different rows.** 64.1% / 7.0 steps / −21.3% = full WALT (discovered + multimodal + external verifier). "1.3–1.4× fewer steps" is the paper's cross-split average, **not** a Classifieds-row figure (Classifieds full WALT: 8.9/7.0 = 1.27×, calc.). |

### P1 item 13d — venues: Speculative Actions (D51), AAPT, SMC, SPACE

| ID | Claim as recorded in dossier | What the primary source says (verbatim, location) | Verdict |
|---|---|---|---|
| 13d-1 | L358: "Speculative Actions … Columbia — ICLR 2026"; "venue ICLR 2026 per C5/O2/C6, 'unverified' per C15 (D51)"; D51 (L832): "Verify against the ICLR 2026 program" | SA-ICLR-oral: page type **"Oral"**; authors "Naimeng Ye, Arnav Ahuja, Georgios Liargkovas, Yunan Lu, Kostis Kaffes, Tianyi Peng"; "Fri, Apr 24, 2026"; OpenReview link "https://openreview.net/forum?id=P0GOk5wslg". SA-ICLR-poster: page type **"Poster"**, same authors, "Fri, Apr 24, 2026 • 3:15 PM – 5:45 PM -03", same OpenReview link. Title on both ICLR pages: **"Speculative Actions: A Lossless Framework for Faster AI Agents"**; arXiv v2 title (identifier "arXiv:2510.04371v2 [cs.AI] 23 Apr 2026"): "Speculative Actions: A Lossless Framework for Faster **Agentic Systems**". SA-anth: "Venue: International Conference on Learning Representations (ICLR) 2026". (The fetch tool returned the session labels "Oral Session 3A Agents" and "Poster Session 4 Pavilion 3" apparently swapped between the two pages; the oral slot is 11:42–11:52 AM -03 per the oral page.) | ✅ **CONFIRMED — ICLR 2026, accepted as an Oral (with a poster slot).** D51 resolved. Note the ICLR title differs from the arXiv title ("Faster AI Agents" vs "Faster Agentic Systems"). The arXiv Comments field could not be read. |
| 13d-2 | L358: "proves a 50% latency-reduction cap for single-step speculation" | SA-arXiv v2 §2: *"Proposition 1 suggests the end-to-end latency reduction has an upper bound of 50%, occurring when p=1 and α=∞."* | ✅ Confirmed (incidental check). It is an upper bound under the paper's model (p = 1, α = ∞), not a measured cap. |
| 13d-3 | L366: "AAPT … (stated venue AAAI 2027, unverified)"; §8.2 L891 "AAPT 'AAAI 2027'" | AAPT, **unversioned HTML fetch**: *"Copyright © 2027, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved."*; the same fetch found no "Anonymous submission" text and full author names (Georgia Tech, Fudan, Marquette, …). AAPT, **v1 HTML fetch** (identifier "arXiv:2607.28399v1 [cs.LG] (30 July 2026)"): *"No occurrences of 'AAAI' or 'Association for the Advancement' appear in this document"* — **the two fetches disagree**; a v2 could not be checked (429). AAAI-27 official timetable: *"July 28, 2026 - Full papers due"*; *"September 24, 2026 - Notification of Phase 1 rejections"*; *"October 19-25, 2026 - Author feedback window"*; *"November 30, 2026 - Notification of final acceptance or rejection (Main Technical Track)"*; *"February 16-23, 2027 - AAAI-27 Conference"* in Montréal. | ⚠ **CORRECTED to "AAAI-27 author-kit formatting only; not accepted as of 2026-09-27".** AAAI-27 final decisions are not due until 30 Nov 2026, so no acceptance can be public today. The AAAI copyright line is the default footer of the AAAI author kit in non-anonymous mode, so it shows the template used, not acceptance. The arXiv v1 was posted 30 Jul 2026, two days after the AAAI-27 paper deadline (calc. from dates). Cite as "arXiv Jul 2026 (AAAI-27 format)". |
| 13d-4 | L363: "Speculative Macro Commit … USC/Intel — arXiv Sep 2026 (O3: MLSP 2026)"; §8.2 L891/L897 "SMC 'MLSP 2026'" | SMC v1: identifier "arXiv:2609.03236v1 [cs.AI] 03 Sep 2026"; authors Zeyu Liu (USC), Souvik Kundu (Intel Labs), Peter A. Beerel (USC); fetch reports *"No specific conference name or publication venue is mentioned on this page"*, with IEEE-style index terms *"LLM Agents, speculative execution, inference latency."* MLSP-26: *"September 28th – Oct 1st 2026, Atlanta, Georgia, USA"*; CfP: submission *"June 12th , 2026 11:59PM AOE"*, notification *"July 31st, 2026"*, *"6 pages full-length papers, including figures and references."* The schedule page lists no titles in static HTML (JavaScript-only; "100 papers", "30 oral talks"). The code repo named by a secondary index (github.com/zeyuliu1037/speculative-macro-commit) returned 404. | ❓ **UNRESOLVABLE.** Nothing in the paper names MLSP, and the official MLSP 2026 paper list cannot be read without JavaScript. The IEEE-style index terms fit, but do not prove, an IEEE signal-processing venue. Keep "(O3 claims MLSP 2026; unverified)". The MLSP 2026 workshop starts tomorrow (28 Sep), so the program and IEEE Xplore proceedings should settle this soon. |
| 13d-5 | L326: "SPACE … arXiv Sep 2026 (Gemini claims EMNLP 2026)"; §8.2 L891/L896 "SPACE 'EMNLP 2026'" | SPACE v1: identifier "arXiv:2609.02042v1 [cs.LG] 02 Sep 2026"; authors Yanting Yang, Can Jin, Jinman Zhao, Jiahao Wu, Yang Zhou, Zhepeng Wang, Zhendong Wang, Mu Zhou, Dimitris N. Metaxas (Rutgers, Toronto, PolyU, Amazon, Microsoft); fetch: *"I found no instances of 'EMNLP', 'ACL', 'ARR', 'Findings', 'conference', 'under review', or 'preprint'"*. EMNLP-26 official dates: *"ARR submission deadline: May 25, 2026"*; *"EMNLP commitment deadline: August 2, 2026"*; *"Notification of acceptance: August 20, 2026"*; *"Camera-ready papers due: August 30, 2026"*; conference *"October 24 –29, Budapest, Hungary"*. The official site has no public accepted-papers list (see access notes). | ⚠ **UNSUPPORTED / UNRESOLVABLE.** EMNLP 2026 decisions went to authors on 20 Aug 2026, but no official accepted-paper list is public on 2026.emnlp.org. SPACE v1 was posted on 2 Sep, after the camera-ready deadline, and names no venue. No primary source supports "EMNLP 2026", so the claim traces only to Gemini (G13). Cite as "arXiv Sep 2026". |
| 13d-6 | L706 (Top-20 #17): "AAPT — 2607.28399, Jul 2026 [C] … Contested-window success 0.50→0.79" | AAPT v1 abstract: *"AAPT improves the success rate from 0.50 to 0.79 within a contested decision window (p=1.8×10−3), while producing no incorrect actions"*, 650 ms window. On speculation, v1 related work reads: *"Interactive Speculative Planning (Hua et al. 2024), Dynamic Speculative Planning (Guan et al. 2025), Speculative Actions (Ye et al. 2025), and AgenticCache all overlap fast approximate execution with slow verification"*; *"By construction, a branch whose routing decision arrives after its deadline is suppressed rather than executed."* | ✅ 0.50→0.79 confirmed (incidental check). The verbatim phrase "nothing executed speculatively" (L366) was **not found** by the fetch. The closest statements are "producing no incorrect actions" and "suppressed rather than executed". Re-quote rather than keep that phrase in quotation marks. |

### P1 item 13e — Fara-7B (D54, E90), AXIS, ComputerRL

| ID | Claim as recorded in dossier | What the primary source says (verbatim, location) | Verdict |
|---|---|---|---|
| 13e-1 | E90 (L154): "$0.025 vs $0.913 per WebVoyager task against OpenAI computer-use-preview (≈36×, calc.), 16.5 vs 38.0 actions/task, 73.5% vs 70.9% success"; "(reference prices; hosting-cost assumptions unverified)" | Fara-arXiv v1 **Table 10**, caption *"We report per-task WebVoyager statistics for different models, including average number of input and output tokens processed."* Columns: Cost ($) per Task / Accuracy / Actions per Task / Input Tok per Task / Output Tok per Task.<br>`OpenAI computer-use-preview | 0.913 | 70.9 | 38.0 ± 34.2 | 295k ± 324k | 2.3k ± 2.0k`<br>`UI-TARS-1.5-7B | 0.082 | 66.4 | 41.3 ± 37.2 | 408k ± 572k | 2.2k ± 2.8k`<br>`Fara-7B | 0.025 | 73.5 | 16.5 ± 21.1 | 124k ± 202k | 1.1k ± 1.4k`<br>(other rows: SoM Agent GPT-5 0.316 / 91.1 / 16.6; SoM o3 0.514 / 79.3 / 28.3; SoM GPT-4o 0.302 / 65.1 / 16.6; GLM-4.1V-9B-Thinking 0.045 / 66.8 / 42.3).<br>Text (§5): *"Based on market rate token pricing discussed in Appendix A, the average cost per task is $0.025 for Fara-7B, compared to roughly $0.30 for proprietary baselines. In terms of interaction length, Fara-7B completes tasks in 16.5 ± 21.1 actions on average, which is comparable to GPT-4o and GPT-5, but shorter than OpenAI computer-use-preview."* Footnote 3: *"Prices taken from here: https://platform.openai.com/docs/pricing"*. **Appendix A was not present** in the HTML, the arXiv PDF or the MSR PDF as extracted.<br>**Hosting and price assumption (Fara-blog, Figure 1 caption):** *"Cost is computed by multiplying the average number of input and output tokens each model consumes by price per token. Both Fara-7B and UI-TARS-1.5-7B are based on Qwen-2.5-VL-7B, for which the lowest inference price from https://openrouter.ai/ is $0.2/$0.2 per 1M input/output tokens."* The paper does not mention prompt caching or cached-input prices. | ✅ **CONFIRMED, with the assumption now identified.** Fara-7B is priced as a hosted third-party API call at the **lowest OpenRouter price for Qwen-2.5-VL-7B, $0.20/$0.20 per M input/output tokens**, not as self-hosted GPU cost. Reproduced (calc.): 124k × $0.2/M + 1.1k × $0.2/M = **$0.0250**; UI-TARS 408k/2.2k at the same price = **$0.0820**. computer-use-preview's $0.913 is reproduced by **$3/M input + $12/M output**: 295k × 3 + 2.3k × 12 = **$0.9126** (calc.). The paper states only that OpenAI prices come from OpenAI's pricing page, and I did not open that page, so "$3/$12" is inferred from the reproduction. Cost ratio 0.913/0.025 = **36.5×** (calc.). The costs are per attempt, with no caching, and **≈97% of the $0.913 is input tokens (calc.)**. Per success (calc.): $0.034 vs $1.288 = **37.9×**. Actions are model actions per task, not wall-clock time. Averages are over 3 runs: *"we run three independent evaluations for each online benchmark and report the average."* |
| 13e-2 | E90/L413: "Online-Mind2Web only 34.1%" | Fara-arXiv §5 (Table 9 context): *"On Online-Mind2Web, Fara-7B attains 34.1, comparable to GPT-4o (34.6)"*; OpenAI computer-use-preview 42.9. Fara-blog Table 1 (caption: *"… Results are reported as Task Success Rate / Accuracy (%) and are averaged over 3 runs."*): Fara-7B `73.5 | 34.1 | 26.2 | 38.4`; OpenAI computer-use-preview `70.9 | 42.9 | 24.7 | 25.7` (WebVoyager / Online-Mind2Web / DeepShop / WebTailBench). | ✅ **CONFIRMED.** Add that computer-use-preview **beats** Fara-7B on Online-Mind2Web (42.9 vs 34.1). The cost comparison is therefore favourable on WebVoyager and WebTailBench but not on Online-Mind2Web. |
| 13e-3 | E90/D54 (L835): "an independent Browserbase run reported 62% (C15)"; "harness-sensitivity gap" | **Fara-blog:** *"We partnered with a trusted external group, Browserbase, to independently evaluate Fara-7B using human annotators. The model achieved 62% on WebVoyager (see detailed reports in Browserbase blog here). These results were generated in the same environment with identical settings and human verification of each task, making them directly comparable."* **Paper §5.1.2 "Human Evaluation"** (MSR PDF): *"We engaged with a trusted third party, Browserbase, to independently verify Fara-7B with human annotators … They used the inference harness we release in our github to generate trajectories from Fara-7B endpoints hosted on Azure Foundry for our filtered and re-refreshed WebVoyager tasks. They establish 62% accuracy of Fara-7B and other open source models."* (ellipsis introduced by the fetch tool). **BB-blog (vendor):** *"When benchmarked on the publicly available 595-task WebVoyager dataset updated in collaboration with Microsoft and using human-verified scoring, Fara-7B significantly outperformed similar open-source models."*; *"We used pass@1 with up to 5 retries, reflecting real-world deployment patterns for small self-hosted models."*; *"Every task was human-verified, with evaluators reviewing screenshots, full web trajectories, and the final task state to confirm completion."* The 73.5% protocol (paper §5.1.2): *"we retain the same prompts, llm-as-a-judge model type, and procedure published with each benchmark"*, using *"GPT-4o along with the official respective prompts in the LLM-based judge for WebVoyager"*, averaged over 3 runs. | ✅ **CONFIRMED (62% is stated by Microsoft's blog and by the paper itself).** The gap has more causes than harness sensitivity. **Judge:** GPT-4o LLM judge (73.5%) vs human annotators (62%). **Harness and hosting:** Microsoft's harness on Azure Foundry endpoints for both. **Protocol:** average of 3 runs vs "pass@1 with up to 5 retries" (the Browserbase blog does not define whether retries are infrastructure or task retries). **Task set:** filtered/refreshed WebVoyager in both, "595-task" in Browserbase's run. The Browserbase blog, as fetched, printed no number itself. |
| 13e-4 | L312: "AXIS … **Task time −65–70%; cognitive workload −38–53%**; accuracy 97–98% vs a human/UI baseline (not like-for-like)"; L54, L270, L711, L745 cite "AXIS −65–70% task time" | AXIS abstract: *"Our experiments on Microsoft Word demonstrate that AXIS reduces task completion time by 65%-70% and cognitive workload by 38%-53%, while maintaining accuracy of 97%-98% compared to humans."* §7: *"AXIS cuts task completion time by 65%-70% and cognitive workload by 38%-53%, while maintaining human-level accuracy."* User-study design: *"participants are asked to complete specified tasks within an application through three methods: manually, with the assistance of a UI Agent, and with the assistance of AXIS."*; UI Agent = *"UFO (Zhang et al., 2024a) for its superior Word task performance"*; *"20 individuals were randomly selected as participants"*, *"five different tasks in Microsoft Word."* **Table 3** (*"Comparison of Methods on Time and Success Rate in L1 and L2 tasks."*): Time (s) L1 `Manual 61.8 | UI Agent 104.6 | AXIS 18.2`, L2 `167.6 | 155.5 | 57.1`; Success (%) L1 `100.0 | 75.0 | 98.3`, L2 `97.5 | 45.0 | 95.0`. **Table 1** (*"Comparison of the performance of UI Agent and AXIS on 50 tasks."*): Time (s) `59.5 | 29.9`; Success (%) `52.0 | 84.0`; Steps `3.2 | 2.0`; Cost ($) `0.4 | 0.2`. | ⚠ **CORRECTED (baseline definition).** **−65–70% is relative to manual human operation**, not to a UI agent: L1 61.8→18.2 s = −70.6%, L2 167.6→57.1 s = −65.9% (calc.). **"97–98% accuracy" is AXIS's success rate as a fraction of manual success**: 98.3/100 = 98.3%, 95.0/97.5 = 97.4% (calc.). The cognitive-workload figure is NASA-TLX vs manual. **Against the UI agent (UFO)**, AXIS cuts time by 82.6% (L1) and 63.3% (L2) in the user study, and by 49.7% (59.5→29.9 s, ≈2.0×) in the 50-task feasibility study, with 3.2→2.0 steps and $0.4→$0.2 cost (all calc. from Tables 1 and 3). Task times are human-in-the-loop completion times for 20 participants on 5 Word tasks, so they are not agent wall-clock. The objection row (L745) should cite the like-for-like agent comparison (≈2× faster, 3.2→2.0 steps, cost halved), not −65–70%. |
| 13e-5 | L311: "ComputerRL … **At most 1/3 of the steps of the strongest baselines**; AutoGLM-OS-9B 48.9% on OSWorld; API–GUI vs GUI-only **+134% relative**"; "E (steps; time/$ NR)"; "venue unverified"; L54/L270/L711 repeat "≤1/3 the steps", "+134% rel." | CRL-arXiv v2 §4.1: *"The comparative results are in Table 1. Moreover, by employing the API-GUI strategy, AUTOGLM-OS can accomplish tasks using at most 1/3 of the steps required by the strongest baseline approaches, demonstrating remarkable gains in execution efficiency."* **Table 1** (caption *"AUTOGLM-OS performance on OSWorld and OSWorld-Verified (updated in 2025.08). We compare AUTOGLM-OS with state-of-the-art agents, including both proprietary and open models."*) has only the columns Agent Model / #Params / OSWorld / OSWorld-Verified. It has **no step column**. Rows: `w/ GLM-4.1V-9B-Thinking | 9B | 48.9±0.5 | 48.0`; `OpenAI CUA o3 | 42.9 | –`; `UI-TARS-1.5 | 42.5 | –`; `Claude 4.0 Sonnet | 30.7 | 43.9`. No figure caption reports step counts, and no maximum step budget is stated for evaluation. §4.3 Framework Ablation: *"the API-GUI strategy achieves an average success rate of 26.2%, representing a 134% improvement over the GUI-only approach (11.2%). The most significant gains are observed in the Office (27.9% vs. 6.2%) and Professional (41.6% vs. 14.3%) domains, where API-GUI provides 350% and 191% improvements, respectively."* The fetch placed this ablation on GPT-4o. **CRL-ICLR:** page type "Poster", authors "Hanyu Lai, Xiao Liu, Yanxiao Zhao, Han Xu, Hanchen Zhang, Bohao Jing, Yanyu Ren, Shuntian Yao, Yuxiao Dong, Jie Tang", "Friday, April 24, 2026 • 3:15 PM – 5:45 PM -03", OpenReview "https://openreview.net/forum?id=oEVfNf0w4B"; also listed at mlanthology.org/iclr/2026/lai2026iclr-computerrl/ (search result). | ⚠ **PARTIALLY CONFIRMED / CORRECTED.** (a) **"At most 1/3 of the steps" is an unquantified author statement.** v2 reports no step counts, no step table and no step budget, so it cannot be checked and should not be cited as a measured ratio. (b) **+134% is confirmed**: 26.2/11.2 = 2.34× (calc.). It comes from a framework ablation with an untrained prompted model (GPT-4o per fetch), not the RL-trained AutoGLM-OS, and it is a success-rate gain, not a step or time saving. (c) 48.9% (OSWorld) confirmed; 48.0% on OSWorld-Verified. (d) **Venue: ICLR 2026 poster**, confirmed on the official ICLR site. The arXiv v2 date and Comments could not be read. |

### P1 item 13f — KVCOMM, DroidSpeak, AgentReuse

| ID | Claim as recorded (dossier line) | What the primary source says | Verdict |
|---|---|---|---|
| 13f-K1 | l.437: "Approximate — 'no loss reported' on RAG, math, coding"; l.266 "up to 7.8×, 'no loss reported'" | KVCOMM (arXiv v2 1 Nov 2025; Comments: *"Accepted for publication in NeurIPS2025"*; NeurIPS 2025 poster 115164). Abstract: *"KVCOMM achieves over 70% reuse rate across diverse multi-agent workloads, including retrieval-augmented generation, math reasoning, and collaborative coding tasks, all without quality degradation. Particularly, when each fully-connected agent receives 1K input tokens with 512 prefix tokens and 512 output tokens under a five-agent setting, KVCOMM achieves up to 7.8x speedup compared to the standard prefill pipeline, reducing TTFT from ~430 ms to ~55 ms."* Body: *"Meanwhile, as the reuse rate reaches 95% across 1,319 samples in a four-agent system for GSM8K, KVComm achieves comparable performance to the original workload (less than 2.5% accuracy drop)."* Tasks (fetch summary): MMLU, GSM8K, HumanEval; Llama-3.1-8B-Instruct on H100. | ⚠ **PARTIALLY CONFIRMED / CORRECTED.** The abstract says "without quality degradation", but the body reports a **measured accuracy drop of <2.5%** at 95% reuse (GSM8K, 4 agents). "No loss" is an author characterization, not zero measured loss; metric = task accuracy. Per-task baseline vs KVCOMM table not extracted. |
| 13f-D1 | l.438: "Approximate — 'negligible' F1 / Rouge-L loss"; "Up to 4× throughput, ~3.1× faster prefill" | NSDI 2026 page (Liu, Huang, Yao, Feng, Gu, Du, H. Li, Cheng, Jiang — UChicago; Lu, Musuvathi, Choukse — Microsoft): *"Experiments on diverse datasets and model pairs demonstrate that DroidSpeak achieves up to 4x throughput improvement and about 3.1× faster prefill (time to first token), with negligible loss of quality in F1 scores, Rouge-L or code similarity score, compared to the baseline which does not allow any sharing across models."* arXiv v4 (14 Jul 2025): datasets *"six datasets (including HotpotQA, multifieldQA_en, 2wikimQA, multi_news, lcc, and repobench-p)"*; metrics *"F1 score for QA tasks (hotpotQA, 2wikimQA, multifieldQA_en) … Rouge-L score for summarization tasks (multi_news) … code similarity score for code completion tasks (lcc, repobench-p)"*; *"eight pairs of models"*; layer selection criterion *"critical layer group with quality drop within 5% of the original accuracy"*; hardware *"two A100 virtual machines … Standard_ND96amsr_A100_v4, which contains 8×80GB A100 GPUs on each virtual machine"*. arXiv title differs: *"DroidSpeak: KV Cache Sharing for Cross-LLM Communication and Multi-LLM Serving"*. | ✅ **CONFIRMED with scope.** "Negligible" covers F1, Rouge-L **and code similarity**; tasks are long-context QA / summarization / code-completion datasets (LongBench-style), **not agent tasks**; the design tolerates up to 5% quality drop when choosing layers. |
| 13f-A1 | l.348: "AgentReuse … Li, Wu, Tan; USTC — CRAD 2024 / arXiv 2025"; "−93.12% vs no reuse; −60.61% vs GPTCache (SMP dataset, 2,664 requests)"; "reuse-decision accuracy 0.9459, F1 0.9718" | arXiv v2 §6.1: *"the SMP dataset [39], which contains 2,664 task requests for LLM-driven personal agents"*, *"23 intent categories such as 'LAUNCH,' 'QUERY,' and 'ROUTE.'"*; [39] = *"Chinese Information Processing Society of China. The evaluation of chinese human-computer dialogue technology (smp2019). https://conference.cipsc.org.cn/smp2019/evaluation.html, 2019."* Abstract: *"…achieves a 93% effective plan reuse rate, an F1 score of 0.9718, and an accuracy of 0.9459 in evaluating request similarities, reducing latency by 93.12% compared with baselines without using the reuse mechanism."* Setup: *"AutoGen [53] as the agent framework and OpenAI's GPT-4 API as the LLM"*; mean plan generation ≈31.8 s over 100 tests (fetch summary). CRAD page: authors **Li Guopeng, Wu Ruiqi, Tan Haisheng, Chen Guoliang**, J. Computer Research and Development 61(11):2706–2720, 1 Nov 2024. | ✅ **Figures CONFIRMED.** ⚠ CRAD lists 4 authors (arXiv lists 3). |
| 13f-A2 | Representativeness of SMP / 2,664 requests (queue item) | The "~30% duplicates" prior is **not** from SMP: *"Analysis of the personal assistant dataset in [13] and [40] indicates that about 30% of task requests in LLM-driven agents are semantically identical or similar."* ([13] Gill et al., *Privacy-aware semantic cache for large language models*, arXiv 2403.02694; [40] OpenAssistant oasst2). "Effective plan reuse rate": *"In 93 tests, the responses were identical, indicating an effective reuse rate of 93%."* from *"experiments on 20 requests, repeating the experiment 5 times"*. Fetch found **no** description of train/test split, whether the intent classifier was trained on SMP, replay order, or request language; no discussion of the 7 failed reuses. | ⚠ **Representativeness weak.** SMP2019 is a Chinese human-computer-dialogue evaluation set of short intent-labelled assistant commands (23 intents), a near-duplicate-rich workload; the 93% reuse rate rests on 20 requests × 5 runs; the ~30% duplicate prior comes from other datasets. Not transferable to multi-step GUI workflows without new data. |

---

## 2. D-ledger additions (D57 onward)

| ID | Topic | Positions | Resolution / action |
|---|---|---|---|
| D57 | "Cost of Dynamic Reasoning" energy comparison scope | Dossier E49 (from G via themoonlight.io): "agentic queries consume 62.1–136.5× more GPU energy than chatbot queries". Paper v2 §VI / Table III: single request on HotpotQA, highest-accuracy Reflexion/LATS configurations, Llama-3.1-8B/70B on A100-40GB, vs one ShareGPT single-turn request. The ends of the range are the 70B runs (LATS 62.1×, Reflexion 136.5×); v1 says "per request", v2 "per query" | Figures confirmed. The general "agentic vs chatbot" framing overstates them: it is one benchmark, with no batching, at maximum-accuracy configurations. Always state these conditions. The dossier previously marked these numbers as unchecked ("until the paper is checked"); they are now checked, but they stay caveated. |
| D58 | FocusAgent: dossier mixes retriever configurations | Dossier l. 262 and l. 398 pair WebArena $59.0→$46.2, 36.5→39.6% (**GPT-5-mini retriever**) with WorkArena L1 $55.6→$45.1, 53.6→51.5%, "−59% (WebArena)" pruning and the 2.5→10.1 s latency (all **GPT-4.1-mini retriever**). v2 Table 2 reports the two as separate rows. | Always name the retriever. 4.1-mini row: WA-L1 $45.1 / 51.5% / 51% pruning; WebArena $44.0 / 32.3% / 59% pruning; latency 10.1 s/step. 5-mini row: WA-L1 $38.1 / 53.2% / 61%; WebArena $46.2 / 39.6% / 53%; no latency data. |
| D59 | FocusAgent WorkArena L1 pruning for 4.1-mini: v2 Table 1 vs Table 2 | Table 1: 56%. Table 2 and body text: 51%. | Paper-internal inconsistency (text extraction; confirm visually). Cite 51% (main table and text) and note the mismatch. |
| D60 | FocusAgent baselines revised between versions | v1 Table 2: GenericAgent-BT WorkArena L1 53.0%, 5k-truncation 41.8%. v2 Table 2: 53.6% and 44.5%. The 5-mini WorkArena result is 51.8% in v1 (App. B Table 5) and 53.2% in v2. The FocusAgent(4.1-mini) numbers are unchanged (51.5%, 32.3%). | Version-dependent baselines. Any Δ-pp must use baseline and treatment from the same version. |
| D61 | Continuum ">8×" vs "1.12–3.66×" is not version drift | D14/l.558: ">8×" is an earlier-version claim superseded by v7. Primary: v7 (8 Sep 2026) abstract still says *"improves the average job completion times by over 8x"*; §1 carries both the 1.12–3.66× / 1.10–3.22× trace-replay range (since v2, Dec 2025) and "up to 8.18x" delay on a real SWE-agent run (500 SWE-Bench-Verified tasks, internal H100 testbed). ">8x" entered the abstract in v4 (CacheTTL, 4 May 2026). v1 abstract had no number (§6.2: "up to a 2x reduction in average response time" vs vLLM, Llama-3.1-8B). | Supersedes D14's resolution. Cite 1.12–3.66× delay / 1.10–3.22× throughput as the controlled trace-replay range; cite 8.18× only as "up to, real SWE-agent deployment on the authors' partner testbed vs unnamed distributed-inference baselines". Never write that v7 replaced ">8×". |
| D62 | Continuum 144.9 vs 93.4 steps/min | Dossier: agent-serving throughput ≈1.55×. Primary (v6 Table 5): RL-rollout microbenchmark, OpenHands + GLM-4.5-fp8 on Multi-SWE-bench, one 8×H100 node; columns vLLM 93.4 / ThunderAgent 114.8 / Continuum 144.9 "inference steps per minute, as reported by the original paper". | Keep the figure with its scope: 1.55× vs vLLM and 1.26× vs ThunderAgent (calc.); flag that comparator numbers may be taken from ThunderAgent's paper rather than re-run; confirm it survives in v7. |
| D63 | PASTE "1.25× vs ORION, 1.32× vs SpecFaaS" | Dossier l.256/l.361. Primary: not in v1 (no ORION/SpecFaaS at all) nor in v3 text; v3 §6.3 gives tool-side 1.71× over ORION and 1.83× over SpecFaaS; v3 §6.5 gives ≥1.27× vs vLLM and ≥1.24× vs Agentix per concurrency level, pooled 1.50× / 1.30×. | Replace with the v3 §6.3 figures; if 1.25/1.32 came from Fig. 10 or v2, a human should read it off the figure (v2 unread, rate-limited). |
| D64 | PASTE version changes beyond the headline | v1 → v3: title changed ("Act While Thinking…" → "Parallelizing Tool Execution and LLM Generation for Low-Latency Agent Serving"); 1.8× changed from "tool execution throughput" to "observed tool latency"; tool share 35–61% (v1) → 45–57% (v3) (E28); testbed 8 A100 with GPT-5.2 / Gemini-2.5 APIs + local Qwen (v1) → 4 nodes × 8 A100 with local Qwen-DeepResearch-30B / Qwen3-30B-A3B on vLLM (v3); side-effect audit and ORION/SpecFaaS baselines exist only in v3. | Cite v3 for every PASTE number except when explicitly quoting v1; E28 and l.583 patched below. |
| D65 | TraceLab "prefill amplification" | G (via blog): 5.3×. Paper v1/v2 §4.3: "cache misses cause 3.8× more tokens to be prefilled than prefills due to truly unique input tokens" (the word "amplification" is not used). Authors' live dashboard (tracelab.cs.washington.edu, undated, 8,058 sessions to 24 Jul 2026): "prefill amplification factor" = 1 ÷ fresh fraction = 6.3× (10.5× Claude, 3.5× Codex) | 5.3× appears in no version of the paper. It was probably an earlier dashboard snapshot (inferred; unverifiable). Cite only the paper's 3.8× with its definition. Do not call it "prefill amplification". Do not mix dashboard numbers, which come from a growing, larger dataset, with the paper's 4,265-session numbers. |
| D66 | TraceLab long-tool-call share | Paper §1: ">1 min = 4% of all tool calls, 85% of tool time". §6.2: "For Claude … 4.9% of calls but … 92% of total tool time" | Different scopes (all tools vs Claude only), not a contradiction. Cite 4%/85% as the all-agent figure and 4.9%/92% as Claude-only. |
| D67 | TraceLab paper vs live dashboard | Paper (v2, Jun 2026): 4,265 sessions, 43 users, 357,161 steps, 95.7% hit, prefix 59.5% of cost. Dashboard (fetched 2026-09-27): 8,058 sessions, 52 users, 665,453 steps, 95.2%/96.2% hit, prefix 58.6% of session cost, collection to 24 Jul 2026 | The dashboard keeps growing and carries no date. Its figures are not a citable replacement for the paper. If one is used, cite it with the fetch date and label it as author-maintained live data. |
| D68 | Gartner ">90% by 2030" — whose cost | Dossier l.51: "unit prices fall >90%"; rank 10 (l.234): "unit token cost falls >90%"; Gartner 25 Mar 2026: inference on a 1T-parameter LLM "will cost GenAI providers over 90% less than it did in 2025", and "falling GenAI provider token costs will not be fully passed on to enterprise customers" | **Resolved 2026-09-27**: it is provider cost for a 1T-param model (2025→2030), not customer unit price. Reword l.51 and rank 10 (patches below). |
| D69 | Gartner I&O ROI survey scope and date (E73) | Dossier (via olakai/enterprisedna): "28% of AI projects … (782 I&O leaders, Apr 2026)"; Gartner 7 Apr 2026: "28% of AI use cases in infrastructure and operations (I&O) fully succeed and meet ROI expectations … survey of 782 I&O leaders in November and December 2025" | **Resolved 2026-09-27**: scope = AI use cases in I&O; fieldwork Nov–Dec 2025; release 7 Apr 2026. |
| D70 | OpenRouter agent vs human token ratio: 15× vs 5× | OpenRouter blog 30 Jun 2026: "about 15x more per request"; a16z Charts of the Week 21 Aug 2026 via ppc.land: agents "consumed close to five times as many tokens as human users" | Different measures (tokens per request vs aggregate token volume); both can hold. Cite each with its definition; never write "agents use 5–15× more tokens". |
| D71 | OpenRouter cached share of agentic tokens | the-decoder (23 Aug 2026) quoting Walker's LinkedIn post of 11 Aug 2026: "Nearly 70 percent"; ppc.land and getmegabrain reporting a16z (21 Aug 2026, charts credited to Walker): "More than 85%" / "over 85%" | **Open.** Primary charts not retrievable (LinkedIn/X block automated access). Quote as "≈70–85% (secondary reports of OpenRouter charts)" until a human reads both posts. |
| D72 | Chinese share on OpenRouter, 2026 | E59 (secondary, G): Chinese open-weight 39% → 66%+ Jan→Apr 2026; OpenRouter blog 30 Jun 2026 (primary): Chinese models surpassed American ones "in token share as of early June"; datagravity (24 Jun 2026): "~61% of all tokens" | **Open; E59 figure unsupported.** 66% by April is incompatible with a first crossover in early June unless the base differs. Use only the OpenRouter-blog statement. |
| D73 | 2605.26297 title and version | Dossier: "Agentic AI Workload Characterization", "v2 exists", URLs to v2. Primary: title "Agentic AI Workload Characteristics" (Yuan, Nayak, Kundu, Talati); abs page on 2026-09-27 lists only v1 (25 May 2026). | Use the v1 URL and correct title; direct v2 check was rate-limited, so re-check once. Numbers are confirmed in v1 (Fig. 8, Fig. 9). |
| D74 | Gemini 3.8 Flash output speed | E79 (via beam.ai, secondary): "~305 tok/s", "fastest measured by Artificial Analysis"; AA launch article (2 Sep 2026): "~300 output tokens per second" (high reasoning); AA model page (read 27 Sep 2026, undated): 329.7 t/s, speed rank #2 / 211; Google's 3.8 post: no tokens/s claim | Cite AA directly: "≈300 t/s at launch (AA, 2 Sep 2026); 329.7 t/s, #2 of 211 on AA's model page as read 27 Sep 2026". Drop "fastest" and "305". Label as decode throughput after first chunk, "(high)" variant; not task speed |
| D75 | Gemini 3.5 Flash-Lite status | Price table l. 646: "GA 21 Jul 2026", "Native computer use"; Gemini API model page: Computer use "Supported (Preview)"; blog: "built-in tool" | Say "computer use built in (Preview)". GA of the model itself not checked in this pass |
| D76 | Operator shutdown date | Dossier/E39: 31 Aug 2025 (tracker; Wikipedia citing a now-404 OpenAI help article); OpenAI primary (17 Jul 2025): sunset "in the coming weeks"; secondary X post dated 1 Aug 2025 (calc. from ID): "Today, OpenAI has sunset their Operator demo" | Exact date unresolvable from an accessible primary. Cite "announced 17 Jul 2025; site sunset within weeks; now 'no longer accessible' (OpenAI Help)". Use 31 Aug 2025 only with "(secondary)" |
| D77 | Anthropic mid-task cache-preserving updates: scope and source | E83: "instructions/tools" attributed to the Opus 4.8 post; Opus 4.8 post (28 May 2026): instructions only (system entries in the messages array); Anthropic docs: separate "tool changes" feature via `tool_addition`/`tool_removal`, beta header `mid-conversation-tool-changes-2026-07-01`, requires declaring all tools up front | Split E83: instructions = Opus 4.8 launch (GA, no beta header); tools = later beta docs feature. Editing the `tools` array still invalidates the whole cache |
| D78 | Temporal 79.8% framing | Chart 3.4 question: "Is the cost of running AI agents a meaningful factor in your decision to use AI agents?"; report headline: "79.8% say token and compute costs limit their progress"; companion text "at least somewhat of a factor" | Quote the question, not the headline. Treat 79.8% as "cost is at least somewhat a factor" (inferred sum of options; option labels not visible) |
| D79 | MAP latency-question N and version | Dossier: "N=27"; v2 Fig. 12 caption: "N=27–29" (both panels); 14.8% = 4/27, 59.3% = 16/27 (calc.); v4 appendix text unreadable here; v1 §7: "(15%)"; v4 §7 no longer mentions latency | Cite "v2 App. B.4.2 / Fig. 12b, N=27–29 (N=27 for this panel by calc.)". Confirm the v4 appendix by reading the v4 PDF visually |
| D80 | MAP "15/20 run asynchronously" | Dossier (l. 52, 178, 233): "run asynchronously"; v4 §4.4: "can operate asynchronously"; v1 §4.4: of the 15 non-real-time cases, 7 human review, 5 asynchronous background, 3 hybrid | Use "15 of 20 can operate asynchronously (v4); only 5 of 20 are background asynchronous processes (v1 breakdown)" |
| D81 | MAP venue and title | arXiv Comments + ICML virtual site: ICML 2026 Oral, ICML title "Characterizing Agents in Production" (CAP); IBM: "for ICLR 2026" (23 Apr 2026) | Supersedes D25: cite "ICML 2026 (Oral), as 'Characterizing Agents in Production'; arXiv 2512.04123 v4 'Measuring Agents in Production'". ICLR 2026 is likely a workshop version (unverified) |
| D82 | EchoPath success range and baseline success | Dossier (C15): "success 91.2–92.8%"; EP v1 Table 1: EchoPath 87.3% (kimi-K3), 91.2% (Codex), 92.8% (Claude); **Synapse 91.8%** | Cite 87.3–92.8% across three hosts; state Synapse's 91.8% (baseline success ≥ Codex-EchoPath). EchoPath's gain is cost/time at equal success, not success. |
| D83 | EchoPath "159 OSWorld-Verified tasks" | Dossier: 159-task OSWorld-Verified setting; EP v1: "159 active executable memories" after a first pass whose size, success and exclusion rules are not stated | 159 is a post-selection pool (tasks the first pass solved and validated). Second-pass success is conditional on first-pass success; do not compare it to OSWorld-Verified leaderboard success. |
| D84 | EchoPath drift evidence | Dossier: "no work measures replay success across UI versions over time"; EP v1: every second-pass replay ran at a shifted resolution (1920×1080 → 1600×900) + offline random-scaling re-aiming tests; Limitations disclaim "live robustness under broad interface drift" | Both true. Rephrase: EchoPath tests display-resolution shift only; no app-version or layout drift; lifecycle (promote/repair/quarantine) described but not evaluated. |
| D85 | EchoPath code availability | Paper: "The OpenPath package is provided at: https://github.com/JackZhao1998/EchoPath.git"; GitHub 2026-09-27: 404, not among the author's 10 public repos | Treat as not released. Re-check before the paper's related-work freeze; plan (a)'s direct comparison needs re-implementation until then. |
| D86 | AWO "fewer calls ≠ faster" (Part I finding 4, L49) | L49: "calls fall 21.8→19.2 but time rises 75.6→88.1 s with Claude"; AWO v1 Table 9: 21.8→19.2 is GPT 5.1 (time falls 266.6→200.8 s); Claude 4.5 is 16.7→15.4 calls, 75.6→88.1 s, success 89.3→85.7% | L49 mixes models; L261 is correct. Patch L49. The claim itself stands on the Claude row (and on VWA-Classifieds GPT 5.1, Table 8). |
| D87 | Ares token reduction per benchmark | C15: "~35–37% on TAU-Bench / BrowseComp-Plus / WebArena"; ARES v1 Table 1 T_total (calc.): Retail −35.3%, Airline −22.3%, BrowseComp-Plus −41.8%, WebArena −45.3% | C15's range fits Retail only. Cite per-benchmark figures from Table 1 (calc.). Abstract "up to 52.7%" not located in Table 1 — open. |
| D88 | AAPT "AAAI 2027" | Dossier L366: "stated venue AAAI 2027". The unversioned arXiv HTML carries the AAAI author-kit footer "Copyright © 2027, Association for the Advancement of Artificial Intelligence"; a separate v1 fetch reported no AAAI text (fetches disagree). The AAAI-27 timetable puts final decisions on 30 Nov 2026 | Not accepted as of 2026-09-27; "AAAI 2027" can mean at most "submitted / AAAI-27 format". Cite "arXiv Jul 2026 (AAAI-27 format)". Re-check after 30 Nov 2026 |
| D89 | SPACE "EMNLP 2026" (G13) | Gemini: EMNLP 2026. arXiv v1 (2 Sep 2026, after EMNLP camera-ready on 30 Aug): no venue string. The official EMNLP 2026 site has no public accepted-paper list | Unsupported by any primary source; cite "arXiv Sep 2026". Re-check the ACL Anthology EMNLP 2026 volume once published (conference 24–29 Oct 2026) |
| D90 | Speculative Actions title | arXiv v2: "…Faster Agentic Systems"; ICLR 2026 camera-ready and virtual site: "…Faster AI Agents" | Cosmetic. Cite the ICLR title with the arXiv ID; the ICLR presentation is an **Oral** |
| D91 | Fara-7B 73.5% vs Browserbase 62% (extends D54) | D54: a "harness-sensitivity gap". Primary sources: both runs use Microsoft's harness and endpoints (Azure Foundry for the 62% run). They differ in **judge** (GPT-4o LLM judge vs human annotators), **protocol** (mean of 3 runs vs "pass@1 with up to 5 retries") and possibly the task subset ("595-task" refreshed set) | Relabel the D54 cause as "judge and protocol sensitivity (LLM judge vs human verification)", not harness. Report both numbers whenever the 36× cost claim is cited |
| D92 | AXIS "−65–70% task time" baseline | Dossier (L312): vs "a human/UI baseline"; L54/L270/L711/L745 use it as the gain from API access over GUI clicking. AXIS abstract and Table 3: the figure is AXIS-assisted vs **manual human** completion time (61.8→18.2 s, 167.6→57.1 s); "97–98% accuracy" is AXIS success ÷ manual success | Cite −65–70% only as "vs manual human operation". For API-first vs GUI agent (UFO), cite Table 1: 59.5→29.9 s (≈2.0×, −49.7% calc.), 3.2→2.0 steps, $0.4→$0.2, 52→84% success (50 Word tasks); user study −82.6% (L1) and −63.3% (L2) vs UI agent (calc.) |
| D93 | ComputerRL "≤1/3 the steps" | Dossier L54/L270/L311/L711: measured step ratio ("E (steps)"). arXiv v2 §4.1 states it once, with no step counts, step table, figure or step budget anywhere in v2 | Downgrade to "author statement, unquantified". Do not use it as a number on slides. The only quantified ComputerRL efficiency-adjacent figure is +134% relative success (26.2 vs 11.2%) for API-GUI vs GUI-only in a prompted-model ablation, which is a success-rate gain, not a step saving |
| D94 | KVCOMM "without quality degradation" vs measured drop | Abstract: "all without quality degradation"; body: "less than 2.5% accuracy drop" at 95% reuse, 4-agent GSM8K, 1,319 samples. | Report as "author claims no degradation; measured accuracy drop <2.5% at 95% reuse (GSM8K)". Do not call it lossless. |

Existing D-entries resolved or updated in §3 (not re-numbered): D13, D14, D15, D16, D18, D24, D25, D28, D29, D33, D35, D36, D42, D45, D47, D48, D49, D51, D53, D54. Still open: SMC/MLSP venue (13d), exact Operator shutdown date (D76), OpenRouter cached share (D71).

---

## 3. E-ledger and dossier patches (exact replacement text)

All line numbers refer to v2 at commit c18e2fe. Each patch is either a whole-row or whole-line replacement (the row's ID or first cell is shown) or an exact fragment replacement. Where several patches touch one line, they replace different, non-overlapping fragments and can be applied in any order. That covers line 54 (Continuum and AXIS/ComputerRL fragments), line 236 (E49 fragment here plus the OSWorld-Human fragment in the item-1 file) and line 558 (FocusAgent and Continuum fragments). When building v2.1, apply the item-1 file's patches as well.

### Patch index by dossier line

| Dossier line | What is there | Patched by |
|---|---|---|
| 46 | 1. Where the time goes depends on the agent a… | P0-4/9/13f |
| 49 | 4. Fewer model calls does not imply faster. A… | 13a/13c |
| 51 | 6. Demand is exploding and is now agent-domin… | P0-6/7/8 |
| 52 | 7. Survey evidence supports "latency constrai… | P1-10–13 |
| 54 | 9. Landscape (8 families): the largest measur… | 13d/13e, P0-4/9/13f (**two groups; non-overlapping fragments**) |
| 57 | 12. Data hygiene: several widely repeated num… | P0-3/13b |
| 87 | E19 | P0-2/5 |
| 101 | E28 | P0-4/9/13f |
| 102 | E29 | P0-4/9/13f |
| 103 | E30 | P0-3/13b |
| 117 | E39 | P1-10–13 |
| 146 | E49 | P0-2/5 |
| 152 | E55 | P0-6/7/8 |
| 154 | E90 | 13d/13e |
| 162 | E58 | P0-6/7/8 |
| 163 | E59 | P0-6/7/8 |
| 166 | E62 | P0-6/7/8 |
| 169 | E65 | P0-6/7/8 |
| 177 | E68 | P1-10–13 |
| 178 | E69 | P1-10–13 |
| 179 | E70 | P1-10–13 |
| 182 | E73 | P0-6/7/8 |
| 193 | E79 | P1-10–13 |
| 197 | E83 | P1-10–13 |
| 212 | C. Cached long-session coding agents  TraceLa… | P0-4/9/13f |
| 230 | §1.9 Top-10 rank 6 | P0-6/7/8 |
| 233 | §1.9 Top-10 rank 9 | P1-10–13 |
| 234 | §1.9 Top-10 rank 10 | P0-6/7/8 |
| 236 | Numbers not to put on a slide without heavy c… | P0-2/5 |
| 256 | Speculative decoding (draft k tokens, verify … | P0-4/9/13f |
| 257 | KV / prefix caching — exact reuse  Cross-step… | P0-4/9/13f |
| 260 | Distillation / draft models  Small action mod… | 13a/13c: no change needed (checked) |
| 261 | Early exit / adaptive computation  Three form… | 13a/13c |
| 262 | Quantization (weakest analogy; literal weight… | P0-3/13b |
| 266 | - KV / prefix caching, exact → KVCOMM (cross-… | P0-4/9/13f |
| 267 | - KV / prefix caching, semantic → EchoPath (v… | P0-4/9/13f |
| 270 | - Early exit / adaptive computation → API-fir… | 13d/13e |
| 279 | 3. Growing context creates repeated logical i… | P0-2/5 |
| 280 | 4. Token prices are collapsing faster than ta… | P0-6/7/8 |
| 311 | ComputerRL row | 13d/13e |
| 312 | AXIS row | 13d/13e |
| 316 | WALT: Web Agents that Learn Tools row | 13a/13c |
| 326 | SPACE: Skill-Guided Adaptive Action Chunking row | 13d/13e |
| 347 | EchoPath row | 13a/13c |
| 348 | AgentReuse: A Plan Reuse Mechanism for LLM-Dr row | P0-4/9/13f |
| 358 | Speculative Actions row | 13d/13e |
| 361 | PASTE: Act While Thinking row | P0-4/9/13f |
| 363 | Speculative Macro Commit row | 13d/13e |
| 366 | AOSpec row | 13d/13e |
| 398 | FocusAgent row | P0-3/13b |
| 413 | Fara-7B row | 13d/13e |
| 415 | StepWise / Step-level Optimization for Effici row | 13a/13c |
| 434 | Continuum row | P0-4/9/13f |
| 437 | KVCOMM row | P0-4/9/13f |
| 438 | DroidSpeak row | P0-4/9/13f |
| 444 | Provider docs: [Anthropic prompt caching](htt… | P1-10–13 |
| 452 | Ares row | 13a/13c |
| 491 | TraceLab row | P0-2/5 |
| 492 | Agentic AI Workload Characterization row | P0-4/9/13f |
| 510 | 11. Replay under drift and cache poisoning — … | 13a/13c |
| 558 | - Agentix's NSDI numbers replace the older Au… | P0-3/13b, P0-4/9/13f (**two groups; non-overlapping fragments**) |
| 583 | PASTE (Mar 2026)  DeepResearchBench, SWE-benc… | P0-4/9/13f |
| 646 | Google Gemini 3.5 Flash-Lite (GA 21 Jul 2026)… | P1-10–13 |
| 683 | None of the four components is new on its own… | 13a/13c |
| 692 | 3b  EchoPath — Zhao, Xu (JHU), Shanmugham, Ro… | 13a/13c |
| 703 | 14  FocusAgent — ServiceNow/Mila, TMLR 2026 [… | P0-3/13b: no change needed (optional note only) |
| 705 | 16  PASTE — MSR, 2603.18897, Mar 2026 [C]  Pa… | P0-4/9/13f |
| 711 | 21b  API-first and hybrid API+GUI agents — AX… | 13d/13e |
| 718 | (a) Recipes from own runs + human demos, dete… | 13a/13c |
| 745 | "Why click through Concur at all? Use the API… | 13d/13e |
| 746 | "Guarded replay with lifecycle already exists… | 13a/13c |
| 761 | WebArena (812 tasks; or WebArena-Verified Har… | P0-3/13b: no change needed (optional note only) |
| 793 | D13 | P0-4/9/13f |
| 794 | D14 | P0-4/9/13f |
| 795 | D15 | P0-3/13b |
| 796 | D16 | P0-2/5 |
| 798 | D18 | P0-6/7/8 |
| 804 | D24 | P1-10–13 |
| 805 | D25 | P1-10–13 |
| 808 | D28 | P1-10–13 |
| 809 | D29 | P1-10–13 |
| 813 | D33 | P1-10–13 |
| 815 | D35 | P0-2/5 |
| 816 | D36 | P0-4/9/13f |
| 823 | D42 | 13a/13c |
| 826 | D45 | 13a/13c |
| 828 | D47 | 13a/13c |
| 829 | D48 | P0-3/13b |
| 830 | D49 | 13a/13c |
| 832 | D51 | 13d/13e |
| 834 | D53 | P0-3/13b |
| 835 | D54 | 13d/13e |
| 846 | Errors / weaknesses  Mislabeled Browser Use i… | 13a/13c: no change needed (checked) |
| 872 | §8.2 item 2 | P0-2/5 |
| 873 | §8.2 item 3 | P0-3/13b |
| 874 | §8.2 item 4 | P0-4/9/13f |
| 875 | §8.2 item 5 | P0-2/5 |
| 876 | §8.2 item 6 | P0-6/7/8 |
| 877 | §8.2 item 7 | P0-6/7/8 |
| 880 | §8.2 item 8 | P0-6/7/8 |
| 881 | §8.2 item 9 | P0-4/9/13f |
| 882 | §8.2 item 10 | P1-10–13 |
| 883 | §8.2 item 11 | P1-10–13 |
| 884 | §8.2 item 12 | P1-10–13 |
| 885 | §8.2 item 13 | P1-10–13 |
| 888 | §8.2 item 13a | 13a/13c |
| 889 | §8.2 item 13b | P0-3/13b |
| 890 | §8.2 item 13c | 13a/13c |
| 891 | §8.2 item 13d | 13d/13e |
| 892 | §8.2 item 13e | 13d/13e |
| 893 | §8.2 item 13f | P0-4/9/13f |
| 896 | §8.2 item 14 | 13d/13e |
| 897 | §8.2 item 15 | 13d/13e |
| 923 | - TraceLab — https://arxiv.org/pdf/2606.30560… | P0-2/5 |
| 925 | - Agentic AI Workload Characterization — http… | P0-4/9/13f |
| 939 | - The Cost of Dynamic Reasoning — https://arx… | P0-2/5 |
| 941 | - Why Johnny Can't Use Agents — https://arxiv… | P1-10–13 |
| 944 | - Speculative Actions — https://arxiv.org/htm… | 13d/13e, P0-4/9/13f (**two groups; non-overlapping fragments**) |
| 945 | - KVFlow — https://arxiv.org/html/2507.07400v… | P0-4/9/13f |
| 949 | - BoPO — https://arxiv.org/html/2602.21227v1 … | P0-3/13b: no change needed (optional note only) |
| 958 | - OpenRouter Head of Insights post — https://… | P0-6/7/8 |
| 961 | - Gartner 25 Mar 2026 — (URL in E62) [V]; Gar… | P0-6/7/8 |
| 963 | - HUMAN Security 2026 — https://www.humansecu… | P0-6/7/8 |
| 973 | - OpenAI Fast mode — https://developers.opena… | P1-10–13 |
| 975 | - Google Gemini computer use — https://blog.g… | P1-10–13 |
| 981 | - ComputerRL — https://arxiv.org/html/2508.14… | 13d/13e |
| 985 | - EchoPath — https://arxiv.org/html/2609.1663… | 13a/13c |
| 986 | - AgentReuse — https://arxiv.org/html/2512.21… | P0-4/9/13f |
| 987 | - ToolCaching — https://arxiv.org/abs/2601.15… | 13a/13c |
| 990 | - Fara-7B blog (Browserbase 62%) — https://ww… | 13d/13e |
| 992 | - KVCOMM — https://arxiv.org/abs/2510.12872 ;… | P0-4/9/13f |
| 995 | - Vendor effort claims — https://www.anthropi… | P1-10–13: new line added after it |
| 1008 | - Prefill / decode: input-processing vs token… | P0-4/9/13f |

(Line 236 is also patched by `research/2026-09-27-verification-P0-item1.md`.)

### P0 items 2 and 5 — "The Cost of Dynamic Reasoning" (D35, E49); TraceLab (D16, E19)

**E49** (dossier line 146): replace the whole row with:

```
| E49 | **HotpotQA, one request served alone: GPU energy per query 62.1× (LATS, Llama-3.1-70B: 158.48 vs 2.55 Wh) to 136.5× (Reflexion, 70B: 348.41 vs 2.55 Wh) that of a single-turn ShareGPT inference (8B: 71.7× LATS, 130.9× Reflexion); LATS averages 71.0 LLM calls per request (LLM calls, not tool calls; 8B default); peak throughput (p95-latency knee, 8B on one A100-40GB, prefix caching on) ShareGPT 6.4 QPS vs ReAct 2.6 QPS on HotpotQA and 1.2 QPS on WebShop; Wikipedia API calls average 1.2 s and GPU idle periods reach up to 54.5% of execution time** | Infrastructure characterization of agent test-time scaling; energy from Table III (highest-accuracy Reflexion/LATS configurations from Fig. 17; 8B on 1×A100-40GB, 70B on 8×A100-40GB; vLLM 0.6.6 with prefix caching); energy measurement method not stated | "The Cost of Dynamic Reasoning", Kim, Shin, Chung, Rhu (KAIST), https://arxiv.org/html/2506.04301v2 §IV-A, §IV-C, Fig. 4, Fig. 11, §VI, Table III; same numbers in v1; HPCA 2026 (HPCA-32), main conference, per arXiv Comments and the HPCA 2026 program | v1 Jun 2025; v2 Jan 2026; HPCA Feb 2026 | Primary | G; verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) | ✅ Figures and venue verified (D35 resolved; scope D57). Caveat: one benchmark, one request with no batching, maximum-accuracy configurations, A100-40GB; "idle but powered" is our inference, since the paper gives the idle share, not idle power. |
```

**D35** (dossier line 815): replace the whole row with:

```
| D35 | "62.1–136.5× GPU energy; LATS 71 calls; ReAct 2.6 vs 6.4 QPS; HPCA 2026" | G via themoonlight.io review of arXiv 2506.04301 | **Resolved 2026-09-27.** All four confirmed in the paper (v2 §IV-A, §IV-C, §VI, Table III; same numbers in v1); venue HPCA 2026 (HPCA-32) confirmed by the arXiv Comments field and the HPCA 2026 program. The 62.1× and 136.5× ends are LATS-70B and Reflexion-70B on HotpotQA, one request served alone, highest-accuracy configurations, vs a ShareGPT single-turn inference; 71.0 counts LLM calls; QPS is the p95-latency knee on 8B/1×A100-40GB. See research/2026-09-27-verification-P0-P1.md |
```

**E19** (dossier line 87): replace the whole row with:

```
| E19 | **8.8 LLM calls, 10.8 tool calls, 4.3 min per request (mean; median 38.3 s, p90 6.4 min, p99 43.9 min); 95.7% global prefix-cache hit rate; cache misses cause 3.8× more tokens to be prefilled than truly unique input tokens; tool calls >1 min are 4% of calls but 85% of tool time (Claude only: 4.9% / 92%); median step ≈119K prefix / 875 append / 214 output tokens (all steps; Claude-only medians 126,180 / 857 / 252, Codex 115,584 / 886 / 184); prefix tokens = 59.5% of list-price-equivalent cost** | 4,265 Claude Code/Codex sessions, 357,161 LLM steps, 432,510 tool calls, 43 developers (authors' own day-to-day use), Sep 2025–Jun 2026; costs are estimated API list-price equivalents (~$40.4K total) | TraceLab (Zhu et al., UW), https://arxiv.org/html/2606.30560v2 §1, §4.3 and Table 5, Table 7, Table 8, §6.2; same numbers in v1 | Jun 2026 | Primary | C; G via a blog (126k/857/252 = Claude-only Table 8 medians; "prefill amplification 5.3×" is not in the paper); verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) | ✅ Verified; D16 resolved. Do not cite "5.3×" or the authors' live dashboard (6.3× "prefill amplification factor", a different metric on a larger, undated dataset) as paper figures. |
```

**D16** (dossier line 796): replace the whole row with:

```
| D16 | TraceLab median step tokens | C (doc 7, from the paper): 119K prefix / 875 append / 214 output; G (doc 13, via a blog): 126k / 857 / 252; "prefill amplification 5.3×" | **Resolved 2026-09-27.** Both sets are in the paper (v1 and v2): 119K/875/214 is the §1 headline median over all steps; 126,180/857/252 are the Claude-only P50s in Table 8 (Codex 115,584/886/184). "5.3×" is not in any version of the paper; the paper's figure is 3.8× (miss-caused prefill ÷ truly unique input tokens, §4.3); the authors' live dashboard now shows a different metric, "prefill amplification factor" 6.3× (1 ÷ fresh fraction, larger dataset). See research/2026-09-27-verification-P0-P1.md and D65–D67 |
```

**§1.9 "Numbers not to put on a slide" paragraph** (dossier line 236): replace the fragment

`the 62–136× GPU-energy multiplier until the paper is checked (E49);`

with

`the 62–136× GPU-energy multiplier without its conditions (E49: verified, but HotpotQA only, one request served alone, maximum-accuracy Reflexion/LATS, Llama-3.1 on A100-40GB, vs one ShareGPT inference);`

**Part II/III finding 3** (dossier line 279): replace the fragment

`because of 3.8× prefill amplification on misses [C].`

with

`because cache misses cause 3.8× more tokens to be prefilled than truly unique input tokens (TraceLab §4.3) [C].`

**Appendix A table, TraceLab row** (dossier line 491): replace the whole row with:

```
| [TraceLab](https://arxiv.org/html/2606.30560v2) — Zhu et al.; UW — Jun 2026 (v2, 30 Jun 2026) | 4,265 sessions; cache-miss prefill (3.8× unique tokens); tool-latency tails (E19) | Workload characterization; authors' own usage traces; verified 2026-09-27 | C7, G13 |
```

**Appendix A source list** (dossier line 923): replace `- TraceLab — https://arxiv.org/pdf/2606.30560` with `- TraceLab — https://arxiv.org/html/2606.30560v2 (v1 29 Jun 2026, v2 30 Jun 2026; same figures)`.

**Appendix A source list** (dossier line 939): replace the fragment `The Cost of Dynamic Reasoning — https://arxiv.org/abs/2506.04301` with `The Cost of Dynamic Reasoning — https://arxiv.org/abs/2506.04301 (v2 7 Jan 2026; HPCA 2026)`.

**§8.2 P0 item 2** (dossier line 872): replace the whole line with:

```
2. ~~"The Cost of Dynamic Reasoning" (arXiv 2506.04301): venue (HPCA 2026?), the 62.1–136.5× energy range, LATS 71 calls, ReAct 2.6 vs 6.4 QPS (D35).~~ **Done 2026-09-27** (research/2026-09-27-verification-P0-P1.md): HPCA 2026 confirmed; all figures confirmed in v2 (and v1) with narrowed scope (HotpotQA, one request served alone, maximum-accuracy configurations, 70B ends of the range); 71.0 = LLM calls. D35 resolved; D57 added.
```

**§8.2 P0 item 5** (dossier line 875): replace the whole line with:

```
5. ~~TraceLab medians and "prefill amplification 5.3×" (D16).~~ **Done 2026-09-27** (research/2026-09-27-verification-P0-P1.md): 119K/875/214 = all-step medians (§1); 126k/857/252 = Claude-only Table 8 P50s; "5.3×" is not in the paper (paper: 3.8×, different definition; dashboard: 6.3×). D16 resolved; D65–D67 added.
```

Lines checked that need no change: line 46 (4% = 85% of tool time, confirmed), line 212 (Regime C row, confirmed), line 257 (TraceLab lists tool-latency prediction as an opportunity: §1 names *"semantic-aware tool-latency prediction for KV cache eviction policy"*), line 278 (8.8 / 10.8 / 4.3 min, confirmed), line 788 (D8), and line 845 (the "Cost of Dynamic Reasoning energy figures" entry in the list of unique finds).

### P0 item 3 and P1 item 13b — FocusAgent (D15, D48, D53, E30)

**D15** (line 795): replace the whole row with:
```
| D15 | FocusAgent WorkArena L1 | O (doc 2): $55.6→$38.1, 53.6→53.2%; O (doc 3), C (doc 6): $55.6→$45.1, 53.6→51.5% (Aug-2026 main table) | **Resolved 2026-09-27: configuration, not version.** Both are rows of v2 Table 2 (GPT-4.1 backbone; input-token cost summed over all 330 WorkArena L1 episodes): $45.1 / 51.5% / 51% pruning = GPT-4.1-mini retriever; $38.1 / 53.2% / 61% pruning = GPT-5-mini retriever. Cite both with the retriever named; the 4.1-mini row is the one the latency study (E30) measures. No stale appendix cost values found (Table 15 matches); Table 1 gives 56% pruning for 4.1-mini vs 51% in Table 2. See research/2026-09-27-verification-P0-P1.md |
```

**D48** (line 829): replace the whole row with:
```
| D48 | FocusAgent WebArena success | v1 (Oct 2025; C15): 36.5→**32.3%** (−4.2 pp); v2 / TMLR (Aug 2026; O2, O3): 36.5→**39.6%** (+3.1 pp) | **Corrected 2026-09-27: not a sign flip.** 32.3% (GPT-4.1 + GPT-4.1-mini retriever) appears unchanged in both v1 and v2 Table 2; 39.6% is a different configuration (GPT-4.1 + GPT-5-mini retriever), added in v2 and absent from v1's WebArena results. The WebArena effect is retriever-dependent within one version: −4.2 pp (4.1-mini, $44.0) vs +3.1 pp (5-mini, $46.2), each ≈1.2–1.7 SE (calc.). Cite both rows; do not present FocusAgent as either clearly lossy or clearly lossless. See research/2026-09-27-verification-P0-P1.md |
```

**D53** (line 834): replace the whole row with:
```
| D53 | FocusAgent venue | TMLR 2026 (O2, O3) vs "ICLR 2026 workshop per snippet" (C15) | TMLR **August 2026** confirmed on the official TMLR accepted-papers list (https://jmlr.org/tmlr/papers/, fetched 2026-09-27); arXiv v2 dated 29 Aug 2026. Exact decision date not retrieved (OpenReview 403). Workshop claim unchecked. Cite TMLR 2026 |
```

**E30** (line 103): replace the whole row with:
```
| E30 | **Baseline 2.5 s/step model latency → 10.1 s/step with a GPT-4.1-mini retriever (7.6 s retrieval)** | GPT-4.1 backbone on WorkArena L1; "wall-clock LLM latency" from a timing decorator around each LLM callable; browser time excluded; retries included; GPT-4.1-mini retriever only (no latency reported for the GPT-5-mini retriever) | FocusAgent v2 Table 11 (App. D), https://arxiv.org/html/2510.03204v2 (TMLR Aug 2026; arXiv v2 29 Aug 2026; absent from v1) | 2026 | Primary | O; verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) | ✅ An efficiency technique that is slower per step. Subset size ("33 tasks") not re-checked. |
```

**Part III technique table, quantization-analogue row** (line 262): replace the fragment

`FocusAgent: WebArena $59.0→$46.2 (36.5→39.6%); WorkArena L1 51% pruning yields only −19% cost ($55.6→$45.1, 53.6→51.5%, Aug-2026 table); naive 5k truncation −49% cost but 53.6→44.5%; per-step model latency 2.5→10.1 s.`

with

`FocusAgent (TMLR 2026, v2 Table 2, GPT-4.1, input-token cost over the whole benchmark): GPT-4.1-mini retriever, WorkArena L1 51% pruning yields only −19% cost ($55.6→$45.1, 53.6→51.5%), WebArena $59.0→$44.0 (36.5→32.3%); GPT-5-mini retriever, WorkArena L1 $55.6→$38.1 (53.6→53.2%), WebArena $59.0→$46.2 (36.5→39.6%); naive 5k truncation −49% cost but 53.6→44.5%; per-step model latency 2.5→10.1 s (4.1-mini retriever).`

**Part IV FocusAgent row** (line 398): replace the whole row with:
```
| [FocusAgent](https://arxiv.org/html/2510.03204v2) — Imene Kerboua et al.; INSA Lyon/LIRIS/Esker/ServiceNow/Mila — TMLR Aug 2026 (arXiv v2, 29 Aug 2026) | Small retriever selects relevant AXTree lines for the actor | v2 Table 2, GPT-4.1 backbone, input-token cost summed over the benchmark (330 WorkArena L1 episodes / 381 WebArena tasks). **GPT-4.1-mini retriever:** WorkArena L1 **$55.6→$45.1 (−19%), 53.6→51.5%**, pruning 51%; WebArena $59.0→$44.0 (−25%, calc.), **36.5→32.3%**, pruning 59%; latency 2.5→10.1 s/step. **GPT-5-mini retriever:** WorkArena L1 $55.6→$38.1 (−31%, calc.), 53.6→53.2%, pruning 61%; WebArena $59.0→$46.2 (−21.7%), **36.5→39.6%**, pruning 53%; no latency reported. Naive 5k truncation −49% cost, 53.6→44.5%; lowers prompt-injection success. **Version note:** v1 (Oct 2025) had only the 4.1-mini retriever on WebArena (32.3%, unchanged in v2) and a lower WorkArena baseline (53.0%); the +3.1 pp WebArena result is the 5-mini retriever added in v2, not a sign flip (D48) | E/L; **slower per step**; input costs exclude output; effect sign on WebArena depends on the retriever | O2, O3, C6, G13, C15 ✅ verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) (**D15, D48, D53, D58–D60**) |
```

**Executive summary, point 12** (line 57): replace the fragment

`and — added in v2 — FocusAgent's WebArena result flipping sign between v1 (−4.2 pp) and the TMLR revision (+3.1 pp) (D48),`

with

`and — added in v2 — FocusAgent's WebArena result, whose sign depends on the retriever (−4.2 pp with GPT-4.1-mini, unchanged since v1; +3.1 pp with GPT-5-mini, added in the TMLR revision), and which the inputs misreported as a sign flip between versions (D48),`

**Source-hygiene notes** (line 558): replace the fragment

`FocusAgent's Aug-2026 main table replaces its appendix values;`

with

`FocusAgent's Aug-2026 (v2/TMLR) main table replaces v1's (baselines revised 53.0→53.6% and 41.8→44.5%; GPT-5-mini retriever rows added), and every FocusAgent number must name its retriever (D15, D48);`

**Line 761 (benchmark table, WebArena row)**: no change needed. "$59.0 on a 381-task subset (GPT-4.1, 36.5%)" is confirmed. Optionally append "(input tokens only)" after "$59.0".

**Line 703 (related-work row 14)**: no change needed. The figures are correct for the 4.1-mini retriever. Optionally add "(GPT-4.1-mini retriever)" after "−19% cost on WorkArena L1".

**§8.2 P0 item 3** (line 873): replace with:
```
3. ~~FocusAgent Aug-2026 revision: which retriever config gives $38.1/53.2% vs $45.1/51.5% (D15).~~ **Done 2026-09-27** (research/2026-09-27-verification-P0-P1.md): both are rows of v2 Table 2 (GPT-4.1 backbone, input-token cost over 330 episodes): $45.1/51.5% = GPT-4.1-mini retriever; $38.1/53.2% = GPT-5-mini retriever. D15 resolved; D58–D60 added.
```

**§8.2 P1 item 13b** (line 889): replace with:
```
13b. ~~**FocusAgent** v1 vs TMLR: confirm the WebArena sign flip (32.3% vs 39.6%) and which configuration each number belongs to (D48, D15).~~ **Done 2026-09-27** (research/2026-09-27-verification-P0-P1.md): no sign flip. 32.3% = GPT-4.1 + GPT-4.1-mini retriever (v1 and v2 alike); 39.6% = GPT-4.1 + GPT-5-mini retriever (added in v2). D48 corrected.
```

**Appendix A source list** (line 949): no change (v2 URL is correct). Optionally add "TMLR Aug 2026, https://jmlr.org/tmlr/papers/".

### P0 item 4, P1 items 9 and 13f — Continuum, PASTE (D13, D14); 2605.26297 / AgentRace (D36); KVCOMM, DroidSpeak, AgentReuse

**E28** (l.101) — replace the whole row with:

```
| E28 | **Tool execution 35–61% of total request time (PASTE v1) / 45–57% of agent E2E latency (PASTE v3); non-LLM components dominate or co-dominate latency in 50% of ten profiled applications** | Serving-side profiling. PASTE v1 per-domain averages: coding 60%, deep research 50%, scientific 36% (v1 §2.2.1); v3: range across evaluated agents (v3 §2.2) | PASTE v1 §1, §2.2.1 https://arxiv.org/html/2603.18897v1 ; PASTE v3 §2.2 https://arxiv.org/html/2603.18897v3 ; "From LLM Inference to Agentic Workloads" https://arxiv.org/html/2608.15127v1 | 2026 (PASTE v1 19 Mar; v3 16 Jun) | Primary | G; PASTE part verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) | ⚠ Single-source per figure. PASTE range changed between versions (D64): cite v3 45–57%. 2608.15127 part not re-checked. |
```

**E29** (l.102) — replace the whole row with:

```
| E29 | **84.6–99.5% empirical KV-cache hit ratio (theoretical 87.9–99.3%); decode = 91.0–98.6% of LLM time** with context caching | ReAct-style agents on five benchmarks (ADE-Bench, DABStep, GAIA, SWE-bench Pro, Terminal-Bench 2.0); Qwen3.6-27B and Gemma4-31B, reasoning and non-reasoning configurations; vLLM v0.20.0 on 2× H100 NVL; ranges across configurations | Yuan, Nayak, Kundu, Talati, "Agentic AI Workload Characteristics", arXiv 2605.26297v1, Fig. 8 and Fig. 9 captions, https://arxiv.org/html/2605.26297v1 | 25 May 2026 (v1; abs page lists no v2 as of 2026-09-27) | Primary | O, G (G attributes to "AgentRace"); verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) | ✅ Contradicts "agents are prefill-bound" as a universal claim. Title is "…Characteristics" (D73). D36 resolved: AgentRace is a different, anonymous agent-framework efficiency benchmark. |
```

**Prose fragment naming the paper** (line 46) — replace `Agentic AI Workload Characterization` with `Agentic AI Workload Characteristics (2605.26297)`. (Every other occurrence sits in a row or line replaced whole below, or in the l.212 fragment that follows; l.1008 unchanged.)

**§1.8 / regime table** (l.212) — replace the fragment
`Agentic AI Workload Characterization: 84.6–99.5% hits, 91–98.6% of LLM time in decode (E29)`
with
`Agentic AI Workload Characteristics: 84.6–99.5% empirical hits, 91.0–98.6% of LLM time in decode across five ReAct benchmarks, Qwen3.6-27B/Gemma4-31B on 2× H100 NVL (E29)`

**Part II technique table, speculative-decoding row, PASTE fragment** (l.256) — replace
`PASTE: v1 **48.5%** task-time reduction, 1.8× tool throughput; v3 **43.5% mean / 55.4% p99**; 1.25× vs ORION, 1.32× vs SpecFaaS; audit of >20,000 speculative actions: 602 side-effecting blocked, 0 result divergences; Edit→Verify pattern 55%, Search→Visit 51%.`
with
`PASTE: v1 **48.5%** average task-completion-time reduction, 1.8× tool throughput; v3 average latency **up to 43.5%**, p99 **up to 55.4%**, 1.8× lower tool latency; tool-side 1.71× vs ORION, 1.83× vs SpecFaaS (v3 §6.3); v3 audit of >20,000 speculative actions: 602 potentially side-effecting blocked, no task with a different final result; Edit→Verify pattern 55%, Search→Visit 51% (v1).`

**Part II technique table, KV/prefix-caching row, Continuum fragment** (l.257) — replace
`Continuum: v7 **1.12–3.66× lower delay, 1.10–3.22× throughput** (SWE-Bench/BFCL/OpenHands); 144.9 vs 93.4 inference steps/min (≈1.55×) on Multi-SWE-bench with GLM-4.5-fp8 on 8×H100; earlier versions claimed ">8× JCT".`
with
`Continuum: **1.12–3.66× lower delay, 1.10–3.22× throughput** across three hardware/model setups (trace replay of GPT-5-collected SWE-Bench/BFCL/OpenHands traces, Poisson arrivals, Llama-3.1 8B/70B, Gemma-3 12B; §1 since v2); v4–v7 abstract ">8×" average JCT = "up to 8.18x" delay on a real SWE-agent run (500 SWE-Bench-Verified tasks, partner H100 testbed); RL-rollout microbenchmark 144.9 vs 93.4 (vLLM) vs 114.8 (ThunderAgent) steps/min, GLM-4.5-fp8, Multi-SWE-bench, 8×H100 (v6 Table 5; ≈1.55× vs vLLM, calc.).`

**Line 54 (Landscape summary)** — replace the fragment `Continuum v7 1.1–3.7×` with `Continuum 1.1–3.7× delay (trace replay; up to 8.18× on a real SWE-agent run)`.

**Line 266** — replace
`KVCOMM (cross-agent KV reuse via anchor offset correction, up to 7.8×, "no loss reported") and DroidSpeak (KV sharing across fine-tuned variants, NSDI 2026, up to 4×)`
with
`KVCOMM (cross-agent KV reuse via anchor offset correction, up to 7.8×; abstract claims no quality degradation, body reports <2.5% accuracy drop at 95% reuse on GSM8K) and DroidSpeak (KV sharing across fine-tuned variants, NSDI 2026, up to 4×; "negligible" F1/Rouge-L/code-similarity loss on non-agent long-context datasets)`

**Line 267** — replace `AgentReuse (parameterized plan reuse, −93% latency on near-duplicate requests)` with `AgentReuse (parameterized plan reuse, −93% latency on the SMP2019 Chinese assistant-command set of 2,664 requests; 93% reuse rate from 20 requests × 5 runs)`.

**AgentReuse row** (l.348) — replace the whole row with:

```
| [AgentReuse: A Plan Reuse Mechanism for LLM-Driven Agents](https://arxiv.org/html/2512.21309v2) — Li, Wu, Tan (arXiv); Li, Wu, Tan, Chen (CRAD 61(11):2706–2720, 1 Nov 2024); USTC — arXiv v1 24 Dec 2025, v2 25 Dec 2025 (English version of the CRAD paper) | Intent classification + parameter extraction + similarity (γ = 0.75) fills a cached parameterized plan | **−93.12% latency vs no reuse; −60.61% vs GPTCache** (SMP2019 dataset: "2,664 task requests for LLM-driven personal agents", 23 intent categories; AutoGen + GPT-4 API) | Lossy: request-similarity accuracy 0.9459, F1 0.9718 (≈5% wrong similarity decisions); "93% effective plan reuse rate" = 93 identical responses in 100 tests (20 requests × 5 runs) | C15 ✅ verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) ⚠ near-duplicate workload: SMP2019 is a Chinese human-computer-dialogue evaluation set of short assistant commands; the "~30% identical or similar requests" prior comes from other datasets (Gill et al. 2403.02694; OASST2), not SMP; split/replay order not described; not GUI |
```

**PASTE row** (l.361) — replace the whole row with:

```
| [PASTE](https://arxiv.org/html/2603.18897v3) — Yifan Sui et al.; SJTU/Microsoft/Stevens — arXiv v1 19 Mar 2026 ("Act While Thinking: Accelerating LLM Agents via Pattern-Aware Speculative Tool Execution"); v3 16 Jun 2026, retitled "Parallelizing Tool Execution and LLM Generation for Low-Latency Agent Serving" | Mine recurring tool-call patterns; execute early; promote exact matches; joint tool/LLM scheduling | v1: −48.5% average task completion time, 1.8× tool execution throughput; v3: −43.5% average task completion time (abstract; §6.2 "up to 43.5%"), p99 up to −55.4%, 1.8× lower tool latency; tool-side 1.71× vs ORION, 1.83× vs SpecFaaS (v3 §6.3); ≥1.27× vs vLLM and ≥1.24× vs Agentix at each concurrency (v3 §6.5); v3 audit: 602 potentially side-effecting of >20,000 speculative actions blocked, no task with a different final result (§6.8); v3 testbed 4 nodes × 8 A100-80GB, local Qwen-DeepResearch-30B / Qwen3-30B-A3B on vLLM (v1: GPT-5.2 / Gemini-2.5 APIs + local Qwen on 8 A100); patterns: Edit→Verify 55%, Search→Visit 51% (v1 §2.3.1) | S conditional + empirical audit; not a GUI-benchmark result | O1, O2, O4, C6, G9 ✅ verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) (**version drift D13, D63, D64**) |
```

**Continuum row** (l.434) — replace the whole row with:

```
| [Continuum](https://arxiv.org/html/2511.02230v7) — Hanchen Li et al.; Berkeley/Stanford/Tsinghua — arXiv v1 4 Nov 2025; v4 4 May 2026 titled "CacheTTL"; v7 8 Sep 2026 | Cost-aware KV time-to-live across tool calls + program-level FCFS | v7 §1: 1.12–3.66× lower delay, 1.10–3.22× throughput "across three hardware and model setups" (trace replay of GPT-5-collected SWE-Bench / BFCL V4 / OpenHands traces, Poisson arrivals; Llama-3.1 8B/70B, Gemma-3 12B; A100 / H100 / B200; vs vLLM 0.10.2, LMCache offloading and others); v7 abstract: ">8x" average JCT = "up to 8.18x" delay on a real SWE-agent run (500 SWE-Bench-Verified tasks, partner H100 testbed, vs other distributed inference solutions); v6 Table 5 RL-rollout microbenchmark: 144.9 vs 93.4 (vLLM) vs 114.8 (ThunderAgent, "as reported by the original paper") inference steps/min, OpenHands + GLM-4.5-fp8, Multi-SWE-bench, one 8×H100 node (1.55× vs vLLM, calc.) | S; "Continuum actually has higher pass rate than baselines", attributed to SWE-Bench docker time limits (v6); exact delta not verified | O1, O2, C7, G13, C15 ✅ verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) (**D14 corrected by D61: both numbers are in v7**) |
```

**KVCOMM row** (l.437) — replace the whole row with:

```
| [KVCOMM](https://arxiv.org/abs/2510.12872) — Ye et al.; Duke, MIT et al. — NeurIPS 2025 poster (arXiv v2 1 Nov 2025) | Reuses KV for shared text under **different prefixes across agents** via anchor-based offset correction | >70% reuse; **up to 7.8× speedup; TTFT ~430→~55 ms** (five fully-connected agents, 1K input tokens with 512 prefix and 512 output tokens) | **Approximate** — abstract: "all without quality degradation" on RAG, math reasoning and collaborative coding (MMLU, GSM8K, HumanEval; Llama-3.1-8B-Instruct); body: "less than 2.5% accuracy drop" at 95% reuse, 4-agent GSM8K, 1,319 samples. A small measured drop, not zero; no non-inferiority test | C15 ✅ verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md); multi-agent text pipelines, not GUI |
```

**DroidSpeak row** (l.438) — replace the whole row with:

```
| [DroidSpeak](https://www.usenix.org/conference/nsdi26/presentation/liu-yuhan) — Liu et al.; UChicago (Junchen Jiang), Microsoft — NSDI 2026 (arXiv 2411.02820 v4 14 Jul 2025, titled "…KV Cache Sharing for Cross-LLM Communication and Multi-LLM Serving") | Shares KV across fine-tuned variants of one base model, recomputing only selected layers | **Up to 4× throughput, ~3.1× faster prefill (TTFT)** vs no cross-model sharing; eight model pairs; two Azure VMs with 8×A100-80GB each | **Approximate** — "negligible loss of quality in F1 scores, Rouge-L or code similarity score" on six long-context datasets (HotpotQA, 2wikimQA, multifieldQA_en: F1; multi_news: Rouge-L; lcc, repobench-p: code similarity); recomputed layers chosen with "quality drop within 5% of the original accuracy". Not agent tasks | C15 ✅ verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) |
```

**Workload-characterization source row** (l.492) — replace the whole row with:

```
| [Agentic AI Workload Characteristics](https://arxiv.org/html/2605.26297v1) — Yuan, Nayak, Kundu, Talati (May 2026); AgentRace: Benchmarking Efficiency in LLM Agent Frameworks (anonymous OpenReview submission; a different paper) | Cache-hit and decode-share profiles (E29); framework efficiency benchmarking (AgentRace) | Workload characterization | O1, G9 |
```

**Late-revision note** (l.558) — replace the fragment `Continuum's v7 replaces ">8×";` with `Continuum's ">8×" (abstract since v4, still in v7) is a real-SWE-agent best case, and its 1.12–3.66× range is the controlled trace-replay result (D61);`

**PASTE benchmark-reporting row** (l.583) — replace the whole row with:

```
| PASTE (v1 Mar 2026; v3 Jun 2026) | DeepResearchBench, SWE-bench, ScholarQA (subset counts NR) | Arrival-to-final latency, p99, throughput, stalls/overlap, hit rate; average task completion time −48.5% (v1) / up to −43.5% (v3), p99 up to −55.4% (v3) | Repetitions/CIs NR; v3 audit of >20,000 speculative actions (602 blocked, no task with a different final result) | v3: 4 nodes × 8 A100-80GB, local Qwen-DeepResearch-30B / Qwen3-30B-A3B on vLLM; v1: 8 A100 with GPT-5.2 / Gemini-2.5 APIs + local Qwen; GPU-hours NR |
```

**Landscape top-list row 16** (l.705) — replace the fragment `−48.5% (v1) / −43.5% (v3) task time; 1.8× tool throughput` with `−48.5% (v1) / up to −43.5% (v3) task time; 1.8× tool throughput (v1) / 1.8× lower tool latency (v3)`.

**D13** (l.793) — replace the whole row with:

```
| D13 | PASTE headline | G, C (doc 6), O (doc 4): 48.5% (v1); O (doc 1): 43.5% mean / 55.4% p99 (v3) | **Resolved 2026-09-27.** v1 (19 Mar 2026) abstract: 48.5% average task completion time, 1.8× tool execution throughput. v3 (16 Jun 2026, retitled) abstract: 43.5% average task completion time, 1.8× lower tool latency; §6.2 "average latency by up to 43.5%, with p99 tail latency improving by up to 55.4%". Cite v3 as "up to" figures. See research/2026-09-27-verification-P0-P1.md and D63, D64 |
```

**D14** (l.794) — replace the whole row with:

```
| D14 | Continuum headline | C (doc 7), G (doc 13): ">8× average JCT"; O (doc 2): v7 1.12–3.66× delay, 1.10–3.22× throughput; O (doc 1): 144.9 vs 93.4 steps/min ≈1.55× | **Resolved 2026-09-27: not version drift.** v7 (8 Sep 2026) abstract still says ">8x" average JCT (real SWE-agent run, "up to 8.18x" delay); §1 gives 1.12–3.66× / 1.10–3.22× across three trace-replay setups (present since v2). 144.9 vs 93.4 is an RL-rollout microbenchmark (v6 Table 5, also vs ThunderAgent 114.8). Cite the range as the controlled result and 8.18× only with its scope. See D61, D62 |
```

**D36** (l.816) — replace the whole row with:

```
| D36 | Source of "84.6–99.5% cache hits, 91–98.6% decode" | O: Agentic AI Workload Characterization (2605.26297); G: "AgentRace" | **Resolved 2026-09-27.** Numbers are in 2605.26297 v1 (Yuan, Nayak, Kundu, Talati, "Agentic AI Workload Characteristics", 25 May 2026), Fig. 8 and Fig. 9 captions. AgentRace ("Benchmarking Efficiency in LLM Agent Frameworks") is a different, anonymous OpenReview submission with no such figures on its public pages; G's attribution is wrong. No v2 listed on the abs page (D73) |
```

**§8.2 queue** — replace l.874 with:

```
4. ~~Continuum v7 and PASTE v3 headline numbers (D13, D14).~~ **Done 2026-09-27** (research/2026-09-27-verification-P0-P1.md): Continuum v7 carries both ">8×" (abstract, real SWE-agent) and 1.12–3.66× (trace replay), so D14 was not version drift; 144.9/93.4 is an RL-rollout microbenchmark. PASTE v3 retitled; 43.5%/55.4% are "up to" figures; "1.25×/1.32× vs ORION/SpecFaaS" not found (v3 gives 1.71×/1.83×). D13, D14 resolved; D61–D64 added.
```

replace l.881 with:

```
9. ~~"Agentic AI Workload Characterization" v2 numbers and AgentRace's relationship (D36).~~ **Done 2026-09-27** (research/2026-09-27-verification-P0-P1.md): numbers confirmed in v1 (title "…Characteristics"; no v2 listed); AgentRace is a different anonymous framework-efficiency benchmark. D36 resolved; D73 added.
```

replace l.893 with:

```
13f. ~~**KVCOMM** and **DroidSpeak** "no loss" claims — which tasks, which metrics; **AgentReuse** dataset (SMP, 2,664 requests) representativeness.~~ **Done 2026-09-27** (research/2026-09-27-verification-P0-P1.md): KVCOMM abstract "without quality degradation", body <2.5% accuracy drop at 95% reuse (GSM8K); DroidSpeak "negligible" F1/Rouge-L/code-similarity on six non-agent long-context datasets, within-5% layer criterion; AgentReuse SMP2019 = Chinese assistant-command set, 23 intents, 93% reuse from 20 requests × 5. D94 added.
```

**Appendix A** — l.925: replace `https://arxiv.org/html/2605.26297v2` with `https://arxiv.org/html/2605.26297v1` and the label `Agentic AI Workload Characterization` with `Agentic AI Workload Characteristics`. l.944: replace `PASTE — https://arxiv.org/html/2603.18897v1` with `PASTE — https://arxiv.org/html/2603.18897v1 (v1) ; https://arxiv.org/html/2603.18897v3 (v3, cite this)`. l.945 and l.986 and l.992 unchanged (optionally append `; https://arxiv.org/html/2411.02820v4` to the DroidSpeak entry on l.992).

### P0 items 6, 7 and P1 item 8 — Gartner (E55, E62, E73), OpenRouter (E57–E59, D18), HUMAN Security (E65)

**E55** (line 152) — replace the whole row with:

```
| E55 | **Customer-service cost per interaction $0.04 (linear chatbot) → $1.20 (orchestrated agent), 30×** (EY estimate); **Gartner (17 Aug 2026 press release): "AI inference costs per agentic workflow will increase more than fivefold through 2028"; "Compared to a basic chatbot interaction, routing a task to an agentic reasoning model increases provider inference costs by at least five times, and often much more as task complexity grows"**; Gartner research note "The Inference Paradox: Inference Tiering Is Critical to Protect Margins" (client-only, not read); RAG-assistant lifetime TCO $750k–$1M with build only 10–20%; "Uber exhausted its annual AI compute budget by April 2026" | Gartner: analyst forecast; no baseline year, sample or method stated in the release; the ≥5× comparison is provider inference cost vs a basic chatbot interaction. Others: consultant estimates and anecdotes | Gartner (Will Sommer), https://www.gartner.com/en/newsroom/press-releases/2026-08-17-gartner-predicts-ai-inference-costs-per-agentic-workflow-will-increase-more-than-fivefold-through-2028 ; thelec.net (EY, Aug 2026, secondary); atlan.com; enterprisedna.co (secondary) | 17 Aug 2026 (Gartner); 2026 (others) | Gartner: primary (analyst forecast); others secondary | G; Gartner verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) | ✅ Gartner release verified (forecast, baseline year not stated). ⚠ EY/Uber/TCO remain unverified. |
```

**E58** (line 162) — replace the whole row with:

```
| E58 | **Agentic tokens grew 14× since ~6 Feb 2026 (≈6 months to the 11 Aug 2026 post, calc.) vs 2.8× for human tokens; agent tokens 0.51T → 7.3T (period unit not stated); "nearly 70%" of agentic tokens are cached prompt tokens** | OpenRouter classified traffic; reference point is the single-day crossover "February 6, 2026, may have been the last day humans consumed more tokens than AI agents" | Peter Walker (OpenRouter Head of Insights), LinkedIn, https://www.linkedin.com/feed/update/urn:li:activity:7493029883191681024/ (not machine-retrievable: robots.txt); figures as quoted by the-decoder, 23 Aug 2026, https://the-decoder.com/ai-is-becoming-ais-biggest-customer-as-agentic-token-usage-jumps-14x-on-openrouter/ ; 14× "since February" also in a16z Charts of the Week, 21 Aug 2026 (via ppc.land) | 11 Aug 2026 (post; calc. from activity ID) | Primary vendor statement (social post), read only via secondary | O; checked 2026-09-27 (research/2026-09-27-verification-P0-P1.md) | ⚠ 14× tokens ≠ 14× spend or compute. Primary unread. Cached share conflicts: ~70% (this post) vs >85% (a16z, 21 Aug 2026) (D71). |
```

**E59** (line 163) — replace the whole row with:

```
| E59 | **"88% of all token volume on OpenRouter driven by agentic workloads as of May 2026"; weekly tokens 0.5T (Jan 2025) → 126.2T (2026), "more than 25,000 percent" (252×, calc.); Chinese open-weight share 39% → 66%+ (Jan→Apr 2026); US proprietary 61% → 34%; OpenAI projected $14B loss in 2026** | Secondary syntheses of OpenRouter charts | the-decoder, 17 Sep 2026, https://the-decoder.com/openrouters-staggering-token-chart-is-the-ai-bubble-debate-in-a-single-image/ (25,000%; cites Peter Walker, LinkedIn, https://www.linkedin.com/feed/update/urn:li:activity:7506103118410072064/ , not machine-retrievable); getmegabrain.com (88%) | 2026 | Secondary | G; checked 2026-09-27 (research/2026-09-27-verification-P0-P1.md) | ❌/⚠ 88% not in OpenRouter's post [V] (D19). 25,000%: one secondary citing an OpenRouter chart; the rankings page shows no platform total; week of the 126.2T not given. 39%→66% / 61%→34%: no primary found and in tension with OpenRouter's "surpassing American ones in token share as of early June" (D72) — do not use. $14B not checked. |
```

**E62** (line 166) — replace the whole row with:

```
| E62 | **"Agentic models … require between 5-30 times more tokens per task than a standard GenAI chatbot"; "As token consumption rises faster than token costs fall, overall inference costs are expected to increase"; inference on a 1T-parameter LLM to "cost GenAI providers over 90% less" in 2030 than in 2025, but "falling GenAI provider token costs will not be fully passed on to enterprise customers"; LLMs in 2030 up to 100× more cost-efficient than 2022 models of similar size** | Analyst forecast; the 90% is provider cost for a 1T-parameter model, not the customer's price per token | Gartner press release (Will Sommer), https://www.gartner.com/en/newsroom/press-releases/2026-03-25-gartner-predicts-that-by-2030-performing-inference-on-an-llm-with-1-trillion-parameters-will-cost-genai-providers-over-90-percent-less-than-in-2025 | 25 Mar 2026 | Primary (analyst) | O (primary); C (secondary via Medium); re-verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) | ✅ [V] Upgraded from secondary to primary. Pass-through caveat added (D68). |
```

**E65** (line 169) — replace the whole row with:

```
| E65 | **"Traffic from AI agents and agentic browsers grew 7,851% year over year"; HUMAN's Defense Platform "analyzed more than one quadrillion digital interactions" in 2025; automated traffic +23.51% YoY vs human +3.10% ("eight times faster"; 7.6×, calc.); monthly AI-driven traffic +187% Jan→Dec 2025** | Traffic seen on HUMAN's own Defense Platform (its customers' properties), calendar 2025, YoY baseline implied (2024) but not stated; no definition of which agents/browsers count, no classification method, no base volume or share of total traffic on any public page; traffic, not tokens | HUMAN Security newsroom, https://www.humansecurity.com/newsroom/2026-state-of-ai-traffic-cyberthreat-benchmark-report/ ; report page https://www.humansecurity.com/learn/resources/2026-state-of-ai-traffic-cyberthreat-benchmarks/ ; GlobeNewswire release 9 Apr 2026 | 26 Mar 2026 (UK re-release 9 Apr 2026) | Vendor report (press-release level; full report not publicly retrievable) — vendor marketing | G; verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) | ⚠ Single-source vendor figure; growth from an unstated, probably tiny base; sample is one vendor's platform, not the whole web; traffic, not tokens. |
```

**E73** (line 182) — replace the whole row with:

```
| E73 | **Only 28% of AI use cases in infrastructure and operations (I&O) "fully succeed and meet ROI expectations"; 20% "fail outright"; 57% of I&O leaders reported at least one failure (Gartner survey of 782 I&O leaders, Nov–Dec 2025)** | Self-reported survey of I&O leaders about AI use cases in I&O (not all AI projects; not agent-specific); success/ROI criterion not defined in the release | Gartner (Melanie Freeze), https://www.gartner.com/en/newsroom/press-releases/2026-04-07-gartner-says-artificial-intelligence-projects-in-infrastructure-and-operations-stall-ahead-of-meaningful-roi-returns | Fieldwork Nov–Dec 2025; release 7 Apr 2026 | Primary (analyst survey) | G; verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) | ✅ Primary retrieved. Scope corrected from "AI projects" to "AI use cases in I&O"; survey dates Nov–Dec 2025 (D69). |
```

**Line 51 (Part I key finding 6)** — replace the fragment

`agentic tokens grew 14× in ~6 months vs 2.8× for human, but ~70% of agentic tokens are cached prompt tokens. Gartner (primary, 25 Mar 2026): agentic models need 5–30× tokens per task vs a chatbot, and "overall inference costs are expected to increase" even as unit prices fall >90% by 2030 [V].`

with

`agentic tokens grew 14× since ~6 Feb 2026 vs 2.8× for human, but ~70–85% of agentic tokens are cached prompt tokens (secondary reports of OpenRouter charts; D71). Gartner (primary, 25 Mar 2026): agentic models need 5–30× tokens per task vs a chatbot, and "overall inference costs are expected to increase" even as providers' cost of inference on a 1T-parameter LLM falls >90% (2025→2030), savings "not fully passed on to enterprise customers" [V]; Gartner (17 Aug 2026): inference cost per agentic workflow to rise more than fivefold through 2028 [V].`

**Top-10 rank 6** (line 230) — replace the whole row with:

```
| 6 | **Agentic tokens overtook human tokens on OpenRouter ~1 Feb 2026; agentic requests use ≈15× the tokens of human requests; agentic volume grew 14× in ~6 months (human 2.8×)** | Shows the efficiency problem is now the majority workload | One router; "Mixed" category; 70–85% of agentic tokens cached (secondary reports disagree, D71); 14×/2.8× read only via secondary reports of a LinkedIn post; "≈15×" is per request, not aggregate volume (≈5×, D70); not first-party API data | ✅ [V] O, G (Feb 1, 15×); ⚠ 14×/2.8× secondary-only (checked 2026-09-27) |
```

**Top-10 rank 10** (line 234) — replace the whole row with:

```
| 10 | **Gartner (primary): agentic models need 5–30× tokens per task vs a chatbot, and overall inference cost is expected to rise even as providers' cost of inference on a 1T-parameter LLM falls >90% (2025→2030) — savings "not fully passed on to enterprise customers" (25 Mar 2026); inference cost per agentic workflow to rise more than fivefold through 2028 (17 Aug 2026)** | Analyst confirmation that per-token deflation does not solve per-task cost | Analyst forecasts without a disclosed sample, method or baseline year; the 90% is provider cost, not customer price | ✅ [V] O (primary), C; both releases verified 2026-09-27 |
```

**Line 280 (Part II/III point 4)** — replace the fragment

`Gartner expects per-workflow inference cost to *rise* (E62) [G, C].`

with

`Gartner expects inference cost per agentic workflow to *rise* more than fivefold through 2028 (E55, 17 Aug 2026) and overall inference cost to rise (E62) [V].`

**D18** (line 798) — replace the whole row with:

```
| D18 | OpenRouter agentic > human crossover date | G: Feb 6 2026; O: early Feb | **[V] "right around February 1st"** (OpenRouter blog, 30 Jun 2026). Walker's LinkedIn post of 11 Aug 2026 (via the-decoder) frames "February 6, 2026" as possibly "the last day humans consumed more tokens than AI agents", so Feb 6 has an OpenRouter-origin source; cite Feb 1 (blog) and note Feb 6 as the post's framing (checked 2026-09-27) |
```

**§8.2 item 6** (line 876) — replace the whole line with:

```
6. ~~Gartner 17 Aug 2026 release (5× per-workflow inference cost through 2028) — fetch the primary; and the Apr-2026 782-leader ROI survey (E73).~~ **Done 2026-09-27** (research/2026-09-27-verification-P0-P1.md): 17 Aug 2026 release confirmed (>5× per agentic workflow through 2028; no baseline year stated); E73 corrected to "28% of AI use cases in I&O", survey Nov–Dec 2025, release 7 Apr 2026; Top-10 rank 10 reworded (the >90% is provider cost, not unit price).
```

**§8.2 item 7** (line 877) — replace the whole line with:

```
7. ~~OpenRouter primary chart for "25,000%" weekly-token growth and the 39%→66% Chinese share (E59); the LinkedIn 14×/70%-cached statement (E58).~~ **Checked 2026-09-27** (research/2026-09-27-verification-P0-P1.md): 15×/Feb-1 re-confirmed; 14×/2.8× and 25,000% traced to Walker LinkedIn posts (not machine-retrievable; secondary only); cached share 70% vs >85% conflict (D71); 39%→66% unsupported and in tension with OpenRouter's "early June" crossover (D72). A human should open the two LinkedIn posts.
```

**§8.2 item 8** (line 880) — replace the whole line with:

```
8. ~~HUMAN Security 2026 report: 7,851% definition and sample (E65).~~ **Done 2026-09-27** (research/2026-09-27-verification-P0-P1.md): "traffic from AI agents and agentic browsers grew 7,851% year over year"; sample = >1 quadrillion interactions on HUMAN's Defense Platform in 2025; baseline, agent definition and base volume not published (full report not retrievable).
```

**Appendix A** — line 958, replace with:

```
- OpenRouter Head of Insights (Peter Walker) posts — https://www.linkedin.com/feed/update/urn:li:activity:7493029883191681024/ (11 Aug 2026; 14×/2.8×/70% cached) ; https://www.linkedin.com/feed/update/urn:li:activity:7506103118410072064/ (16 Sep 2026; 25,000% chart) — both blocked to automated fetch; read via the-decoder (23 Aug and 17 Sep 2026)
```

line 961, replace with:

```
- Gartner 25 Mar 2026 — (URL in E62) [V]; Gartner 25 Jun 2025 (40% cancellations); Gartner 17 Aug 2026 (5× per-workflow) — https://www.gartner.com/en/newsroom/press-releases/2026-08-17-gartner-predicts-ai-inference-costs-per-agentic-workflow-will-increase-more-than-fivefold-through-2028 [V]; Gartner 7 Apr 2026 (I&O ROI survey, 782 leaders) — https://www.gartner.com/en/newsroom/press-releases/2026-04-07-gartner-says-artificial-intelligence-projects-in-infrastructure-and-operations-stall-ahead-of-meaningful-roi-returns [V]
```

line 963, replace with:

```
- HUMAN Security 2026 — https://www.humansecurity.com/learn/resources/2026-state-of-ai-traffic-cyberthreat-benchmarks/ ; newsroom release 26 Mar 2026 — https://www.humansecurity.com/newsroom/2026-state-of-ai-traffic-cyberthreat-benchmark-report/ [V, vendor]
```

(No change needed to line 845, the provider-comparison table; it lists these items only as Gemini's unique finds.)

### P1 items 13a and 13c — EchoPath; Ares (D49), StepWise (D47), AWO (D45), WALT (D42)

None of these five works has an E-row; the affected lines are Part I, Part III, Part V, Part VI D-rows, §8.2 and Appendix A. New E-rows E91–E93 are proposed at the end.

#### EchoPath (13a)

**L347 (Part III, KV / prefix caching, semantic — EchoPath row)** — replace the whole row with:

```
| [EchoPath](https://arxiv.org/html/2609.16635v1) — Zhao (JHU), Shanmugham, Roy (Amazon AGI), Xu (JHU) — arXiv v1 15 Sep 2026 | **Validated GUI trajectories become callable memories with preconditions, bounded parameters, visual re-aiming and lifecycle states (promote / repair / quarantine — described, not evaluated)** | Second pass, Table 1: Codex (gpt-5.5-medium) median **20,370 execution tokens, 127.5 s, 91.2% (145/159)** vs **Synapse** (trajectory-as-exemplar prompting, same model) **586,386 tokens, 315.7 s, 91.8%**; Claude-sonnet-5 92.8%, Kimi-K3 87.3%. Pool = **159 "active executable memories"** from a first pass on OSWorld-Verified (first-pass attempts/success NR; first pass median ≈572k tokens, ≈4.5 min). Second pass at shifted resolution 1920×1080→1600×900; no app-version drift test | Lossy in principle; action-level replay skips the LLM | C15; verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) ⚠ single-source; code link 404 on 2026-09-27 — **directly overlaps plan (a) in Part V (guarded replay + lifecycle); the most developed design for "reuse under drift", but drift robustness is untested by the authors' own account** |
```

**L692 (Part V §5.3 closest prior works, row 3b)** — replace the whole row with:

```
| 3b | **EchoPath** — Zhao (JHU), Shanmugham, Roy (Amazon AGI), Xu (JHU), arXiv 2609.16635v1, 15 Sep 2026 [C15; verified 2026-09-27] *(added in v2; ranks alongside #3 in proximity)* | Validated GUI trajectories become callable memories with **preconditions, bounded parameters, visual re-aiming and lifecycle states (promote / repair / quarantine)**; replays skip the LLM | Median execution tokens 20,370 vs 586,386; second-pass time 127.5 vs 315.7 s — Codex (gpt-5.5-medium) vs a **Synapse** trajectory-as-exemplar baseline on the same model, not a no-memory agent; success **91.2% vs Synapse 91.8%** (EchoPath 87.3–92.8% across Codex / Claude Code / Kimi Code) on **159 active memories** from a first pass on OSWorld-Verified (post-selection pool; first-pass size NR); offline start-state gate rejects only 78% of incompatible starts | **The most dangerous overlap for the recipe component (plan (a)):** guarded replay + lifecycle management already exists on a public CUA benchmark. Differences to claim: no human demos (authors: memory comes from "a first-pass agent … rather than an interactive demonstration"), no speculation, no field-level accuracy accounting, no write-heavy enterprise portal, no replay-success measurement across UI versions over time (only a 1920×1080→1600×900 resolution shift), lifecycle not evaluated, baseline is another memory system. Code link (github.com/JackZhao1998/EchoPath) returned 404 on 2026-09-27 — plan on re-implementing |
```

**L510 (Part V open problem 11)** — replace the fragment

`EchoPath's lifecycle management (promote / repair / quarantine) is the most developed answer, but **no work measures replay success across UI versions over time**;`

with

`EchoPath's lifecycle management (promote / repair / quarantine) is the most developed design, but it is described, not evaluated, and EchoPath's only perturbation is a display-resolution shift (1920×1080→1600×900); its authors state it does "not yet establish live robustness under broad interface drift" — **no work measures replay success across UI versions over time**;`

**L683 (Part V novelty paragraph)** — replace the fragment

`which already does guarded GUI-trajectory replay with preconditions and a promote/repair/quarantine lifecycle on OSWorld-Verified [C15])`

with

`which already does guarded GUI-trajectory replay with preconditions and a (described, unevaluated) promote/repair/quarantine lifecycle on 159 OSWorld-Verified tasks with active memories [C15; verified 2026-09-27])`

**L718 (plan (a) status)** — replace the fragment

`**no work measures replay success across UI versions over time** (EchoPath is a repeat-execution setting against a memory baseline) [C15];`

with

`**no work measures replay success across UI versions over time** (EchoPath is a paired repeat-execution setting on 159 first-pass-validated tasks, against a Synapse memory baseline, with only a screen-resolution shift between passes; its offline start-state gate rejects 78% of incompatible starts) [C15; verified 2026-09-27];`

**L746 (reviewer-objection table, EchoPath row)** — replace the fragment

`note EchoPath's baseline is another memory system (Synapse), not a no-memory agent |`

with

`note EchoPath's baseline is another memory system (Synapse, 91.8% vs EchoPath-Codex 91.2%), not a no-memory agent; its gain is cost/time at equal success; its code link was 404 on 2026-09-27 |`

**L888 (§8.2 P1 item 13a)** — replace the whole line with:

```
13a. ~~**EchoPath** (2609.16635): confirm the 159-task OSWorld-Verified setting, the Synapse baseline, whether any drift/UI-version experiment exists, and whether code is released — it is now the closest prior work to plan (a).~~ **Done 2026-09-27** (research/2026-09-27-verification-P0-P1.md): v1 (15 Sep 2026) read. 159 = "active executable memories" after a first pass (first-pass size NR; post-selection); Synapse (ICLR 2024 trajectory-as-exemplar, same gpt-5.5 model) 91.8% vs EchoPath-Codex 91.2%, tokens/time confirmed; EchoPath range 87.3–92.8%; only drift = resolution shift 1920×1080→1600×900, lifecycle not evaluated; code link 404 (not released). D82–D85 added.
```

**L985 (Appendix A)** — replace

`- EchoPath — https://arxiv.org/html/2609.16635`

with

`- EchoPath — https://arxiv.org/html/2609.16635v1 (v1, 15 Sep 2026; code link https://github.com/JackZhao1998/EchoPath 404 on 2026-09-27)`

#### Ares (D49)

**L452 (Part III, Ares row)** — replace the whole row with:

```
| [Ares](https://arxiv.org/html/2603.07915v1) — Jingbo Yang et al.; UCSB/Accenture — arXiv v1 9 Mar 2026 (only version) | A Qwen3-1.7B router picks the lowest sufficient effort (low/medium/high) per step for a gpt-oss-20b agent | Table 1 (gpt-oss-20b; WebArena via AgentOccam, ≈129-task subset, calc. from T_total/T_task): fixed-high→Ares **21,424→11,723 reasoning tokens/task (−45.3%, calc.)**, 2,763k→1,512k total, steps 10.0→8.9, SR **45.0→46.5%**; BrowseComp-Plus 1,841k→1,071k tokens (−41.8%), 42.7→41.3%; TAU-Bench Retail 1,007k→652k (−35.3%), 54.8→54.8%; Airline 873k→678k (−22.3%), 38.0→36.0%; abstract "up to 52.7% fewer reasoning tokens". **Uniform low effort: Retail 35.0% (−19.8 pp), WebArena 37.4% (−7.6 pp)** — adaptive, not uniform, cuts | E/L (wall-clock NR) | O2, C15; verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) ✅ (D49 resolved: C15's 16.4→17.2% is not in the paper) |
```

**L830 (D49)** — replace the whole row with:

```
| D49 | Ares WebArena success | O2 (Table 1): 45.0→46.5%, 21,424→11,723 tokens; C15 (automated extraction, self-flagged): 16.4→17.2%, ~35–37% tokens | **Resolved 2026-09-27.** v1 Table 1 (only version): WebArena High 45.0% / T_task 21424 / T_total 2763k; ARES 46.5% / 11723 / 1512k (gpt-oss-20b). "16.4" and "17.2" do not occur in the paper — C15 extraction error. WebArena token cut is −45.3% (calc.), not ~35–37% (that fits TAU-Bench Retail only). See research/2026-09-27-verification-P0-P1.md |
```

**L846 (scorecard, errors row)** — no change needed (already says the C15 Ares numbers are self-flagged automated extraction; D49 now resolved).

#### StepWise (D47)

**L415 (Part III, StepWise row)** — replace the whole row with:

```
| [StepWise / Step-level Optimization for Efficient CUAs](https://arxiv.org/html/2604.27151v1) — Wei, Ni, Zhao, Gan, Cohan; Yale NLP / UNC — arXiv v1 29 Apr 2026 (only version) | Per-step small→large model cascade with stuck and milestone monitors | OSWorld, Table 1: **EvoCUA-8B + selective Sonnet 4.5 vs always-Sonnet 4.5: $0.881→$0.224/task (−74.6%), 6.4→4.1 s/request, SR 58.1→55.4%** [O1]; **EvoCUA-8B + Kimi K2.5 vs always-Kimi K2.5: $0.132→$0.051 (−61.4%), 8.3→4.5 s/request (−45.8%), 60.1→58.2%**; Qwen3-VL-8B + Kimi K2.5: $0.078, 6.5 s, 59.3% [C15]. WebArena, Table 2: gpt-oss-20b + GPT-5.2 vs GPT-5.2: $0.335→$0.211, 19.6→12.2 s/request, 60.1→57.8%. The abstract's "up to 74.6% cost / up to 45.8% latency" come from different configurations; "recovers 95%+" is C15's paraphrase (96.8–98.7%, calc.) | L (per-request timing, not per task; config-dependent) | O1, C15; verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) ✅ (D47 resolved) |
```

**L828 (D47)** — replace the whole row with:

```
| D47 | StepWise results | O1: SR 58.1→55.4%, 6.4→4.1 s/request (−36%); C15: 58.2–59.3% vs 60.1%, up to −45.8% latency | **Resolved 2026-09-27** (v1 Table 1, OSWorld): O1 = EvoCUA-8B + Claude Sonnet 4.5 vs always-Sonnet ($0.881→$0.224, −74.6%). C15 = the two Kimi K2.5 cascades vs always-Kimi K2.5 (60.1%); −45.8% latency = EvoCUA-8B + Kimi K2.5 (8.3→4.5 s/request) at 58.2%, cost −61.4%. The abstract's two "up to" maxima come from different configurations; latency is per request. See research/2026-09-27-verification-P0-P1.md |
```

**L260 (Part II distillation row, StepWise fragment)** — no change needed (numbers confirmed; configuration already named). Optional: append `; latency is per request` after `6.4→4.1 s per request`.

#### AWO (D45)

**L49 (Part I, key finding 4)** — replace the fragment

`AWO/meta-tools: calls fall 21.8→19.2 but time rises 75.6→88.1 s with Claude;`

with

`AWO/meta-tools (AppWorld, Claude 4.5): calls fall 16.7→15.4 per task but time rises 75.6→88.1 s and success drops 89.3→85.7% (with GPT 5.1 the same method cuts calls 21.8→19.2 and time 266.6→200.8 s);`

**L261 (Part II early-exit row, AWO fragment)** — replace the fragment

`**counterexample with Claude: calls fall but time rises 75.6→88.1 s and success declines**`

with

`**counterexample with Claude 4.5: calls 16.7→15.4 but time rises 75.6→88.1 s and success declines 89.3→85.7%** (AWO v1 Table 9)`

**L826 (D45)** — replace the whole row with:

```
| D45 | AWO success gain | O1: 21.8→19.2 calls (−11.9%), 69.6→73.2% (+3.6 pp); C15: 11.9% fewer calls, **+4.2 pp** | **Resolved 2026-09-27** (v1 appendix; v2 appendix not readable): both correct, different cells. −11.9% calls and +3.6 pp = GPT 5.1 on AppWorld (Table 9); +4.2 pp = Claude 4.5 on VisualWebArena overall, 25.0→29.2% (Table 7). C15 paired two "up to" maxima from different model × benchmark cells. On AppWorld, Claude 4.5 loses 3.6 pp (89.3→85.7%). See research/2026-09-27-verification-P0-P1.md |
```

**L987 (Appendix A)** — replace

`AWO — https://arxiv.org/abs/2601.22037`

with

`AWO — https://arxiv.org/abs/2601.22037 (v1 29 Jan 2026, v2 2 Feb 2026; per-task tables 7–9 read in https://arxiv.org/html/2601.22037v1)`

#### WALT (D42)

**L316 (Part III, WALT row)** — replace the whole row with:

```
| [WALT: Web Agents that Learn Tools](https://arxiv.org/html/2510.01524v1) — Viraj Prabhu et al.; Salesforce — ICLR 2026 | Exploration or demos → validated tools incl. deterministic URL/API ops | VWA-Classifieds ablation (Table 2, GPT-5-mini): no tools **8.9 steps, 57.5%** → discovered tools (text DOM, self-verify) **6.5 steps, 61.5%** → full WALT (discovered tools + multimodal DOM + external verifier) **7.0 steps (−21.3%), 64.1%**; human-demo tools 7.4 steps, 66.0%. Table subscripts are relative changes (e.g. +7.0% = +4.0 pp). "1.3–1.4× fewer steps" is the paper's average across splits, not the Classifieds row (1.27×, calc.) | E (steps, not time) | O3, C15; verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) ✅ (D42 resolved; v1 only, later versions unchecked) |
```

**L823 (D42)** — replace the whole row with:

```
| D42 | WALT Classifieds success | O3: 57.5→61.5% (GPT-5-mini matched), 66.0% with human-demo tools; C15: 57.5→64.1%, 1.3–1.4× fewer steps, −21.3% steps | **Resolved 2026-09-27** (v1 Table 2, VWA-Classifieds ablation, GPT-5-mini): 61.5% / 6.5 steps = discovered tools, text DOM, self-verify; 64.1% / 7.0 steps (−21.3%) = full WALT (discovered + multimodal + external verifier); 66.0% / 7.4 = human-demo tools. "1.3–1.4×" is the cross-split average from the abstract, not this row (8.9/7.0 = 1.27×, calc.). Cite the row by its configuration. See research/2026-09-27-verification-P0-P1.md |
```

#### §8.2 queue

**L890 (§8.2 P1 item 13c)** — replace the whole line with:

```
13c. ~~**Ares** WebArena success (45.0→46.5% vs 16.4→17.2%) (D49); **StepWise** configurations (D47); **AWO** +3.6 vs +4.2 pp (D45); **WALT** Classifieds row (D42).~~ **Done 2026-09-27** (research/2026-09-27-verification-P0-P1.md): Ares 45.0→46.5% / 21,424→11,723 tokens per task confirmed (v1 Table 1), 16.4/17.2 not in paper; StepWise O1 = EvoCUA+Sonnet, C15 = Kimi K2.5 cascades; AWO +3.6 pp = GPT 5.1/AppWorld, +4.2 pp = Claude 4.5/VWA; WALT 61.5% = discovered-tools row, 64.1% = full WALT. D42/D45/D47/D49 resolved; L49 AWO numbers corrected (D86); D87 added.
```

#### New E-rows E91–E93 (append to Part I §1.4 / Part III as the merger sees fit)

```
| E91 | **EchoPath second-pass replay (Codex, gpt-5.5-medium): median 20,370 execution tokens and 127.5 s per task at 91.2% (145/159) vs Synapse trajectory-as-exemplar baseline on the same model: 586,386 tokens, 315.7 s, 91.8%** (−96.5% tokens, −59.6% time, calc.) | Paired two-pass design on OSWorld-Verified; 159 tasks with an "active executable memory" after the first pass (first-pass size and success NR); second pass at 1600×900 vs 1920×1080 first pass; medians with [min–max] ranges; one run per task as far as stated; first-pass construction median ≈572k tokens, ≈4.5 min | EP v1 Table 1 and Fig. 3, https://arxiv.org/html/2609.16635v1 | 15 Sep 2026 | Primary; reductions calc. | C15; verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) | ⚠ Single paper, post-selection pool, code link 404; other hosts: Claude-sonnet-5 92.8% / 30,503 / 139.3 s; Kimi-K3 87.3% / 19,928 / 130.5 s |
| E92 | **EchoPath start-state gate (offline, 50 memories): accepts 98% of compatible starts and 92% of partially changed starts, but rejects only 78% of incompatible starts** (22% false accepts, calc.); retrieval recall 100% as the repository grows 159→659 memories | Offline diagnostics on stored visual evidence, not live replay | EP v1 Table 3 and retrieval stress test, https://arxiv.org/html/2609.16635v1 | 15 Sep 2026 | Primary | verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) | Relevant to plan (a)'s guard / de-optimization trigger |
| E93 | **AWO (meta-tools), AppWorld, Claude 4.5: calls/task 16.7→15.4, task duration 75.6→88.1 s, success 89.3→85.7%; GPT 5.1: 21.8→19.2 calls, 266.6→200.8 s, 69.6→73.2%** | Per-task averages over the AppWorld run; "task duration (average in seconds)" is end-to-end task time | AWO v1 Table 9, https://arxiv.org/html/2601.22037v1 | 29 Jan 2026 (v2 2 Feb 2026, appendix not re-read) | Primary | O1, C15; verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) | Supports Part I finding 4 on the Claude row only |
```

### P1 items 10–13 — Gemini (D28, E79), Operator (D29, E39), Opus 4.8 (E83), Temporal (E70), LangChain (D24, E68), MAP (E69, D25)

**E79** (line 193) — replace the whole row with:

```
| E79 | **Google: computer use in Flash-class models** | Gemini 2.5 Computer Use (7 Oct 2025); computer use built into Gemini 3.5 Flash (24 Jun 2026; post gives no speed figure); Gemini 3.5 Flash-Lite (launched in the joint post "Introducing Gemini 3.6 Flash, 3.5 Flash-Lite, and 3.5 Flash Cyber", 21 Jul 2026) with computer use "as a built-in tool" (model page: "Supported (Preview)") at $0.30/$2.50 per M and "350 output tokens per second" (vendor claim; AA model page 349 t/s, undated); Gemini 3.8 Flash (2 Sep 2026) at $0.75/$3.75 introductory through 31 Dec 2026, then $1.50/$7.50; Artificial Analysis: "~300 output tokens per second" on high reasoning at launch (2 Sep 2026) and 329.7 t/s, speed rank #2 of 211 on the model page read 27 Sep 2026 (undated); Gemini 3.5 Flash launch (19 May 2026): "When looking at output tokens per second, it is 4 times faster than other frontier models" (vendor marketing) | https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-computer-use-gemini-3-5-flash/ ; https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/ ; https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/ ; https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/ ; https://ai.google.dev/gemini-api/docs/computer-use ; https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite ; https://artificialanalysis.ai/articles/gemini-3-8-flash ; https://artificialanalysis.ai/models/gemini-3-8-flash | 2025–26 | Primary vendor; throughput via Artificial Analysis (third-party measurement) | C, O, G; verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) | ✅ D28 resolved (model name confirmed). **Corrected:** "~305 tok/s, fastest measured by AA" was beam.ai's wording (secondary); AA's own pages give ≈300 t/s at launch and 329.7 t/s (#2/211) later (D74). AA speed = tokens/s after the first chunk, "(high)" variant. Throughput ≠ task-completion speed. |
```

**Price table, Gemini 3.5 Flash-Lite row** (line 646) — replace the whole row with:

```
| Google Gemini 3.5 Flash-Lite (launched 21 Jul 2026) | $0.30 | $0.03 (+$1/M tok/h storage) | — | $2.50 | Computer use built in (model page: "Supported (Preview)"); 350 output tok/s (Google claim; AA ≈349 t/s) |
```

**D28** (line 808) — replace the whole row with:

```
| D28 | Gemini 3.5 Flash-Lite computer-use launch URL | O's slug reads "gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber" | **Resolved 2026-09-27:** slug is correct — joint post "Introducing Gemini 3.6 Flash, 3.5 Flash-Lite, and 3.5 Flash Cyber" (Tulsee Doshi, 21 Jul 2026) names the model "3.5 Flash-Lite" and says it "has computer use as a built-in tool". See research/2026-09-27-verification-P0-P1.md |
```

**E39** (line 117) — replace the whole row with:

```
| E39 | **Operator (CUA): 38.1% OSWorld, 58.1% WebArena, 87.0% WebVoyager (23 Jan 2025); standalone Operator folded into ChatGPT agent — announced 17 Jul 2025 ("The Operator research preview site will remain functional for a few more weeks, after which it will be sunset"); OpenAI Help now says "The Operator website is no longer accessible"; docs instruct users to monitor, halt and take over for logins/CAPTCHAs** | Product timeline; benchmark scores are for CUA, "the model powering Operator" | OpenAI "Computer-Using Agent", https://openai.com/index/computer-using-agent/ (scores); https://openai.com/index/introducing-chatgpt-agent/ and https://help.openai.com/en/articles/11794368-chatgpt-agent-release-notes (17 Jul 2025 notice); https://help.openai.com/en/articles/11752874-chatgpt-agent (current status); 31 Aug 2025 shutdown date via presenc.ai tracker / Wikipedia (secondary) | 2025–26 | Primary (scores, announcement); secondary (exact shutdown date) | G; verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) | ✅ Scores and announcement primary. ⚠ Exact shutdown date not on any accessible OpenAI page (Operator release-notes article now 404; D76). OpenAI's stated reason is integration into ChatGPT agent; **no latency reason is stated** (D29). |
```

**D29** (line 809) — replace the whole row with:

```
| D29 | Operator retired 31 Aug 2025 "due to latency" | G via presenc.ai tracker | **Resolved 2026-09-27 (reason); date open.** OpenAI's primary notices (17 Jul 2025: ChatGPT agent post, agent release notes, editor's note on "Introducing Operator") give integration into ChatGPT agent as the reason and a sunset "in the coming weeks"; none mentions latency. "Due to latency" is the tracker's interpretation — do not cite. 31 Aug 2025 is secondary only (D76). See research/2026-09-27-verification-P0-P1.md |
```

**D33** (line 813) — replace the whole row with:

```
| D33 | Operator 38.1% OSWorld / 87.0% WebVoyager | G via tracker | **Confirmed 2026-09-27** in OpenAI's "Computer-Using Agent" post (23 Jan 2025): "CUA achieved 38.1% success rate on OSWorld … 58.1% on WebArena and 87% on WebVoyager"; the "Introducing Operator" page does not print the numbers. Cite https://openai.com/index/computer-using-agent/ |
```

**E83** (line 197) — replace the whole row with:

```
| E83 | **Anthropic Opus 4.8 launch (28 May 2026): "The Messages API now accepts system entries inside the messages array. Developers can update Claude's instructions mid-task without breaking the prompt cache or routing the update through a user turn." Tools: a separate docs feature ("Mid-conversation system messages and tool changes") offers/withdraws tools with `tool_addition`/`tool_removal` blocks while the `tools` array stays fixed, because "editing it invalidates the prompt cache for the entire conversation"** | Feature aimed at KV/prompt-cache invalidation in agents; system messages need no beta header (Opus 4.8, Opus 5, Opus 5.5, Fable/Mythos 5–5.1; not Sonnet 5); tool changes use beta header `mid-conversation-tool-changes-2026-07-01` | https://www.anthropic.com/news/claude-opus-4-8 ; https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages | 28 May 2026 (instructions); tool changes later (beta, header dated 2026-07-01) | Primary vendor | G; verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) | ✅ Instructions wording confirmed. ⚠ The Opus 4.8 post does not mention tools; "instructions/tools" merged two features (D77). |
```

**Part III row** (line 444) — replace the fragment

`Anthropic Opus 4.8 cache-preserving tool updates | See E84`

with

`Anthropic mid-conversation system messages (Opus 4.8) and tool changes (docs) | See E83, E84`

**E70** (line 179) — replace the whole row with:

```
| E70 | **79.8% answered that cost is (at least somewhat) a factor to "Is the cost of running AI agents a meaningful factor in your decision to use AI agents?" (Chart 3.4; report headline: "79.8% say token and compute costs limit their progress"); 91.1% say agents "improved" or "revolutionized" their productivity (Chart 2.1, "How have AI agents altered your own productivity?"; 4.0% no impact, 1.8% worse)** | 554 agent-using engineers/leaders kept of 650 solicited via Qualtrics, 29 Apr–25 May 2026; self-reported; mostly coding usage | Temporal State of Development 2026, https://temporal.io/reports/state-of-development-2026 | 25 Aug 2026 | Primary commissioned survey | O; verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) | ✅ Question wording confirmed; answer-option labels not visible as text, so "at least somewhat" is inferred from the report's companion sentence. The headline ("limit their progress") is stronger than the question (D78). "Meaningful factor" ≠ "could not deploy". |
```

**E68** (line 177) — replace the Source and Confidence cells; full row:

```
| E68 | **Quality is the #1 production barrier (32%); latency #2 (20%); cost "less frequently cited than in previous years"; 57% have agents in production; latency is #2 for smaller companies, security for >2,000 employees** | 1,340 respondents, fielded 18 Nov–2 Dec 2025 (self-selected, tech-heavy) | LangChain State of Agent Engineering, https://www.langchain.com/state-of-agent-engineering (page byline "12 June, 2026"; first published ≈16 Dec 2025, inferred); KDnuggets summary | 2025–26 | Primary vendor survey | C, O; latency 20% and N re-checked 2026-09-27 (research/2026-09-27-verification-P0-P1.md) | ✅ Primary text: "Latency has emerged as second biggest challenge (20%)"; quality = "one third of respondents" (32% not seen in text). Publication date: see D24. |
```

**D24** (line 804) — replace the whole row with:

```
| D24 | LangChain report date | O: resource listing 25 Feb 2026; C: secondary says 23 May 2026; primary page byline (read 27 Sep 2026): "12 June, 2026" | **Partly resolved 2026-09-27.** The page's only date is 12 Jun 2026, but the report existed earlier: KDnuggets (17 Mar 2026) calls it "recently released"; LangChain's LinkedIn post "state-of-agent-engineering-2025" decodes to 16 Dec 2025 (calc. from post ID; text not readable). Cite "LangChain, State of Agent Engineering (survey 18 Nov–2 Dec 2025; published ≈Dec 2025, page dated 12 Jun 2026)". See research/2026-09-27-verification-P0-P1.md |
```

**E69** (line 178) — replace the whole row with:

```
| E69 | **Latency is "a critical deployment blocker" for 14.8% of deployed survey agents and "a marginal issue … suboptimal but sufficient for deployment" for 59.3% (Fig. 12b; caption N=27–29; = 4/27 and 16/27, calc.); 66% allow response times of minutes or longer, 17% set no explicit limit (Fig. 4, N=53); only 5 of 20 case studies require real-time responsiveness; 15 of 20 "can operate asynchronously" (v1 breakdown: 7 human review, 5 asynchronous background, 3 hybrid); runtime costs "remain negligible compared to alternative expert labor costs"** | 306 valid survey responses (28 Jul–29 Oct 2025) + 20 case-study interviews; 86 responses in production/pilot; latency-blocker question answered by ~27 | Measuring Agents in Production, https://arxiv.org/abs/2512.04123 — §4.4, §5.1, Fig. 4 in v4 (4 Jun 2026); 14.8/59.3 sentence quoted from v2 (30 Jan 2026) App. B.4.2; ICML 2026 Oral as "Characterizing Agents in Production" (https://icml.cc/virtual/2026/poster/61834) | 2025–26 | Primary, peer-reviewed | C, O; verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) | ✅ 66/17/N=53, 5/20, 15/20, "negligible" confirmed in v4. ⚠ N printed as "N=27–29", not 27; 14.8/59.3 read in v2 (v4 appendix not readable here). "Can operate asynchronously" ≠ "run asynchronously" (D80). The strongest counter-evidence: deployers tolerate latency by going async. Venue: D25, D81. N: D79. |
```

**D25** (line 805) — replace the whole row with:

```
| D25 | MAP venue | PDF header: ICML 2026; IBM listing: ICLR 2026 | **Resolved 2026-09-27:** arXiv Comments ("Accepted to the 43rd International Conference on Machine Learning (ICML 2026) as Oral Presentation") and the ICML 2026 virtual site (Oral 6B "Agentic Systems") confirm ICML 2026, where the paper is titled **"Characterizing Agents in Production"**. IBM's "for ICLR 2026" (23 Apr 2026) is probably a workshop version (unverified). Cite "Pan et al., ICML 2026 (Oral); arXiv 2512.04123 v4" |
```

**§ summary point 7** (line 52) — replace the fragment

`MAP (peer-reviewed): only 14.8% of deployed teams call latency critical; 15/20 systems run asynchronously.`

with

`MAP (ICML 2026 oral): only 14.8% of deployed survey agents report latency as a critical deployment blocker (small N, ≈27); 15 of 20 interviewed systems can operate asynchronously.`

and the fragment

`Temporal: 79.8% say operating cost is a meaningful factor, yet 91.1% report productivity gains.`

with

`Temporal: 79.8% say cost is at least somewhat a factor in their decision to use agents, yet 91.1% report productivity gains.`

**§1.9 Top-10, rank 9** (line 233) — replace the whole row with:

```
| 9 | **Latency is the #2 production barrier (20% of 1,340 practitioners) — but only 14.8% of deployed teams call it a critical blocker and 15 of 20 interviewed systems can operate asynchronously** | Connects the systems problem to deployment while pre-empting the obvious rebuttal | Self-selected samples; the MAP blocker question has N≈27 (caption "N=27–29"); "can operate" asynchronously, only 5/20 are background async processes | ✅ C, O; verified 2026-09-27 |
```

**Appendix A source list** — line 941, replace the fragment

`Measuring Agents in Production — https://arxiv.org/abs/2512.04123`

with

`Measuring Agents in Production — https://arxiv.org/abs/2512.04123 (ICML 2026 Oral as "Characterizing Agents in Production", https://icml.cc/virtual/2026/poster/61834)`

Line 973, replace the fragment

`Operator — https://openai.com/index/introducing-operator/ ;`

with

`Operator — https://openai.com/index/introducing-operator/ ; CUA scores — https://openai.com/index/computer-using-agent/ ; Operator sunset notice — https://help.openai.com/en/articles/11794368-chatgpt-agent-release-notes ;`

Line 975, replace the fragment

`https://ai.google.dev/gemini-api/docs/computer-use ; pricing`

with

`https://ai.google.dev/gemini-api/docs/computer-use ; 3.5 Flash-Lite — https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/ ; 3.8 Flash — https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/ ; Artificial Analysis — https://artificialanalysis.ai/models/gemini-3-8-flash ; pricing`

Add after line 995 (vendor effort claims) or in the Anthropic group:

`- Anthropic mid-conversation system messages and tool changes — https://www.anthropic.com/news/claude-opus-4-8 ; https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages`

**§8.2 P1 queue** — replace lines 882–885 with:

```
10. ~~Gemini 3.5 Flash-Lite computer-use post (D28) and Gemini 3.8 Flash throughput via Artificial Analysis.~~ **Done 2026-09-27** (research/2026-09-27-verification-P0-P1.md): D28 resolved (joint 3.6 Flash / 3.5 Flash-Lite / 3.5 Flash Cyber post, 21 Jul 2026); 3.8 Flash throughput corrected to AA ≈300 t/s at launch, 329.7 t/s (#2/211) on 27 Sep 2026 — "305, fastest" was beam.ai's.
11. ~~OpenAI primary notice on Operator's retirement (D29); Anthropic Opus 4.8 cache-preserving tool updates (E83).~~ **Done 2026-09-27** (research/2026-09-27-verification-P0-P1.md): OpenAI notice 17 Jul 2025, reason = integration, no latency (D29 resolved); exact shutdown date still secondary. E83: Opus 4.8 post covers instructions only; tool changes are a separate beta docs feature.
12. ~~Temporal survey question wording (E70); LangChain publication date (D24).~~ **Done 2026-09-27** (research/2026-09-27-verification-P0-P1.md): Temporal Chart 3.4 / 2.1 wording quoted; LangChain page dated 12 Jun 2026 but first published ≈Dec 2025 (inferred) — D24 partly resolved.
13. ~~MAP N for the latency question (27) and async count (15/20) — confirm in v4 (E69).~~ **Done 2026-09-27** (research/2026-09-27-verification-P0-P1.md): 66/17 (N=53), 5/20, 15/20 "can operate asynchronously", "negligible" confirmed in v4; 14.8/59.3 confirmed in v2 App. B.4.2 with caption "N=27–29"; venue ICML 2026 Oral as "Characterizing Agents in Production" (D25 resolved).
```

### P1 items 13d and 13e — venues (D51; AAPT, SMC, SPACE); Fara-7B (D54, E90), AXIS, ComputerRL

**E90** (line 154) — replace the whole row with:

```
| E90 | **Fara-7B: $0.025 vs $0.913 per WebVoyager task against OpenAI computer-use-preview (36.5×, calc.; 37.9× per success, calc.), 16.5 vs 38.0 actions/task, 73.5% vs 70.9% success (GPT-4o LLM judge, mean of 3 runs)**; Browserbase's independent human-verified run reported **62%**; Online-Mind2Web **34.1% vs 42.9%** for computer-use-preview | Per-attempt API cost = mean input/output tokens per task × list price, no caching. Fara-7B (124k in / 1.1k out) and UI-TARS-1.5-7B priced at "the lowest inference price from https://openrouter.ai/ … $0.2/$0.2 per 1M input/output tokens" for Qwen-2.5-VL-7B (hosted-API assumption, not self-hosted GPU cost); computer-use-preview (295k in / 2.3k out) at OpenAI list price, reproduced by $3/$12 per M (calc.; ≈97% of its cost is input tokens). Actions are model actions per task, not wall-clock | Fara-7B v1 Table 10 and §5/§5.1.2, https://arxiv.org/html/2511.19663v1 ; price assumption in the Figure 1 caption of https://www.microsoft.com/en-us/research/blog/fara-7b-an-efficient-agentic-model-for-computer-use/ (24 Nov 2025) ; Browserbase protocol at https://www.browserbase.com/blog/training-computer-use-models-in-the-real-world-with-microsoft | Nov 2025 | Primary (paper + vendor blog); ratios calc.; Browserbase protocol is vendor blog | C15; O1 gives the UI-TARS comparison; verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) | ⚠ The 36× is a price-list ratio at an assumed cheapest-provider price, not measured wall-clock or self-hosting cost. The paper's "Appendix A" pricing was not present in any extraction. 62% vs 73.5% reflects human vs LLM judge and "pass@1 with up to 5 retries" vs a mean of 3 runs (D54, D91). Fara-7B loses to computer-use-preview on Online-Mind2Web. |
```

**D54** (line 835) — replace the whole row with:

```
| D54 | Fara-7B WebVoyager success | Paper: 73.5% (GPT-4o LLM judge, official WebVoyager judge prompts, mean of 3 runs, filtered/refreshed tasks); Microsoft blog and paper §5.1.2: Browserbase's independent run with human annotators, same Microsoft harness on Azure Foundry endpoints, "pass@1 with up to 5 retries" on the 595-task refreshed set: 62% | **Verified 2026-09-27.** The gap comes from the judge and the protocol (human verification vs LLM judge; retries vs 3-run mean), not the harness. Report both whenever the 36× cost claim is cited. See research/2026-09-27-verification-P0-P1.md |
```

**Fara-7B row, §3.x table** (line 413) — replace the fragment

`an independent Browserbase run reported **62%**; Online-Mind2Web **34.1%** [C15] | E/L (reference prices; no wall-clock; harness-sensitive) | O1, C15 ✅ (D54) |`

with

`an independent Browserbase human-verified run reported **62%**; Online-Mind2Web **34.1%** (computer-use-preview 42.9%) [C15]. Costs price Fara-7B and UI-TARS at the cheapest OpenRouter price for Qwen-2.5-VL-7B ($0.2/$0.2 per M tokens), no caching | E/L (price-list assumption; no wall-clock; judge-sensitive) | O1, C15 ✅ verified 2026-09-27 (D54) |`

**Key finding 9** (line 54) — replace the fragment

`(ASI +23.5% rel., WALT 50.1% WebArena, ComputerRL ≤1/3 the steps and +134% rel., AXIS −65–70% task time)`

with

`(ASI +23.5% rel., WALT 50.1% WebArena, ComputerRL +134% rel. success for API–GUI vs GUI-only [its "≤1/3 the steps" is an unquantified author statement], AXIS ≈2× faster than a UI agent with 3.2→2.0 steps and −65–70% task time vs manual human operation)`

**Part II bullet** (line 270) — replace the fragment

`(AXIS −65–70% task time; ComputerRL ≤1/3 steps; Beyond Browsing +24 pp)`

with

`(AXIS ≈2× faster than a UI agent, −65–70% task time vs manual human work; ComputerRL +134% rel. success, "≤1/3 steps" unquantified; Beyond Browsing +24 pp)`

**ComputerRL row** (line 311) — replace the whole row with:

```
| [ComputerRL](https://arxiv.org/html/2508.14040v2) — Lai et al.; Tsinghua / Z.AI / UCAS — arXiv Aug 2025; **ICLR 2026 poster** | Unified **API–GUI action space** with auto-built app APIs, trained with large-scale online RL | AutoGLM-OS (GLM-4.1V-9B-Thinking) **48.9% OSWorld / 48.0% OSWorld-Verified** (Table 1); API–GUI vs GUI-only **26.2% vs 11.2% (+134% relative)** in the framework ablation (prompted model, not the RL-trained agent); "at most 1/3 of the steps required by the strongest baseline approaches" is stated in §4.1 with **no step counts reported anywhere in v2** | S (success); steps unquantified; time/$ NR | C15; verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md); venue = ICLR 2026 (https://iclr.cc/virtual/2026/poster/10007435) |
```

**AXIS row** (line 312) — replace the whole row with:

```
| [AXIS](https://aclanthology.org/2025.acl-long.381/) — Lu et al.; Microsoft + academic — ACL 2025 | API-first agent: prefers app APIs over UI sequences and grows its API set by exploring the app (MS Word) | **vs a UI agent (UFO), 50 Word tasks (Table 1): 59.5→29.9 s (≈2.0×), 3.2→2.0 steps, $0.4→$0.2, success 52→84%.** User study (20 participants, 5 Word tasks, Table 3): vs **manual human** operation, task time **−65–70%** (61.8→18.2 s L1; 167.6→57.1 s L2) and NASA-TLX workload −38–53%; "97–98% accuracy" = AXIS success ÷ manual success (98.3/100, 95.0/97.5, calc.); vs the UI agent −83% (L1) / −63% (L2) (calc.) | Not lossless: success 98.3 vs 100 (L1), 95.0 vs 97.5 (L2) vs manual; better than the UI agent; one app | C15; verified 2026-09-27 (research/2026-09-27-verification-P0-P1.md) — the strongest form of "eliminate the decision"; see Part V objection "why click at all?" |
```

**Top-20 row 21b** (line 711) — replace the fragment

`AXIS: task time −65–70% (one app); ComputerRL: ≤1/3 the steps, +134% rel.;`

with

`AXIS: ≈2× faster than a UI agent (59.5→29.9 s, 3.2→2.0 steps; one app), −65–70% vs manual human work; ComputerRL: +134% rel. success (API–GUI vs GUI-only), "≤1/3 the steps" unquantified; ICLR 2026;`

**Objection row** (line 745) — replace the fragment

`cite AXIS's −65–70% task time as the ceiling API access buys`

with

`cite AXIS's like-for-like agent comparison (API-first vs UI agent on Word: ≈2× faster, 3.2→2.0 steps, cost halved, 52→84% success) as what API access buys; its −65–70% is against manual human operation`

**SPACE row** (line 326) — replace the fragment

`— arXiv Sep 2026 (Gemini claims EMNLP 2026)`

with

`— arXiv Sep 2026 (v1, 2 Sep 2026; Gemini's "EMNLP 2026" is not supported by the paper or any public EMNLP list as of 2026-09-27)`

**Speculative Actions row** (line 358) — replace the fragment

`— Ye, Ahuja, Liargkovas, Lu, Kaffes, Peng; Columbia — ICLR 2026 |`

with

`— Ye, Ahuja, Liargkovas, Lu, Kaffes, Peng; Columbia — **ICLR 2026 Oral** (ICLR title "…Faster AI Agents") |`

and replace the fragment

`C, O, G, C15 ✅ — venue ICLR 2026 per C5/O2/C6, "unverified" per C15 (D51) |`

with

`C, O, G, C15 ✅ — venue verified 2026-09-27: ICLR 2026 Oral, https://iclr.cc/virtual/2026/oral/10009727 (D51 resolved) |`

**SMC row** (line 363) — replace the fragment

`— arXiv Sep 2026 (O3: MLSP 2026)`

with

`— arXiv Sep 2026 (O3 claims MLSP 2026; unverified 2026-09-27: paper names no venue, MLSP 2026 program not machine-readable)`

**AOSpec/AAPT row** (line 366) — replace the fragment

`AAPT: pre-compiled guarded policy trees during idle screen time with **"nothing executed speculatively"** (0.50→0.79 success in a 650 ms decision window; stated venue AAAI 2027, unverified) [C15];`

with

`AAPT: pre-compiled guarded policy trees during idle screen time; late branches are "suppressed rather than executed", "producing no incorrect actions" (0.50→0.79 success in a 650 ms decision window); arXiv Jul 2026 in AAAI-27 format, **not accepted as of 2026-09-27** (AAAI-27 decisions due 30 Nov 2026) [C15];`

**D51** (line 832) — replace the whole row with:

```
| D51 | Speculative Actions venue | ICLR 2026 (C5, O2, C6) vs "venue unverified" (C15) | **Resolved 2026-09-27: ICLR 2026, Oral** (plus poster), Fri 24 Apr 2026; https://iclr.cc/virtual/2026/oral/10009727 ; OpenReview P0GOk5wslg. ICLR title "…Faster AI Agents" (arXiv v2: "…Faster Agentic Systems"). See research/2026-09-27-verification-P0-P1.md |
```

**§8.2 item 13d** (line 891) — replace the whole line with:

```
13d. ~~**Speculative Actions** venue (ICLR 2026?) (D51); **AAPT** "AAAI 2027"; **SMC** "MLSP 2026"; **SPACE** "EMNLP 2026".~~ **Done 2026-09-27** (research/2026-09-27-verification-P0-P1.md): Speculative Actions = ICLR 2026 Oral (D51 resolved); AAPT = AAAI-27 format only, decisions due 30 Nov 2026 (not accepted); SPACE = no primary support for EMNLP 2026; SMC/MLSP 2026 unresolvable (program JS-only). arXiv Comments fields unreadable. D88–D90 added.
```

**§8.2 item 13e** (line 892) — replace the whole line with:

```
13e. ~~**Fara-7B** cost assumptions and the 62% Browserbase run (D54); **AXIS** baseline definition (human vs UI agent); **ComputerRL** step ratio and venue.~~ **Done 2026-09-27** (research/2026-09-27-verification-P0-P1.md): Fara-7B priced at the cheapest OpenRouter Qwen-2.5-VL-7B price ($0.2/$0.2 per M), 36.5× (calc.); 62% = Browserbase human-verified run (blog + paper §5.1.2), a judge/protocol gap (D54 updated); AXIS −65–70% is vs manual human, ≈2× vs UI agent; ComputerRL "≤1/3 steps" unquantified, venue ICLR 2026 poster. E90, D54 patched; D91–D93 added.
```

**§8.2 item 14** (line 896) — replace the fragment `SPACE "EMNLP 2026", ` with `SPACE "EMNLP 2026" (checked 2026-09-27: unsupported, see 13d), `.

**§8.2 item 15** (line 897) — replace the fragment `SMC "MLSP 2026";` with `SMC "MLSP 2026" (checked 2026-09-27: unresolvable, see 13d);`.

**Appendix A, doc-15 list** (line 981) — replace `- ComputerRL — https://arxiv.org/html/2508.14040` with
`- ComputerRL — https://arxiv.org/html/2508.14040v2 ; ICLR 2026 poster — https://iclr.cc/virtual/2026/poster/10007435`

**Appendix A** (line 990) — replace `- Fara-7B blog (Browserbase 62%) — https://www.microsoft.com/en-us/research/blog/fara-7b-an-efficient-agentic-model-for-computer-use/` with
`- Fara-7B blog (Browserbase 62%; $0.2/$0.2 OpenRouter price assumption) — https://www.microsoft.com/en-us/research/blog/fara-7b-an-efficient-agentic-model-for-computer-use/ ; Browserbase protocol (vendor blog) — https://www.browserbase.com/blog/training-computer-use-models-in-the-real-world-with-microsoft`

**Appendix A, speculation list** (line 944) — replace `Speculative Actions — https://arxiv.org/html/2510.04371v2 ;` with `Speculative Actions — https://arxiv.org/html/2510.04371v2 ; ICLR 2026 Oral — https://iclr.cc/virtual/2026/oral/10009727 ;`

(Lines 256, 586, 699 already say "ICLR 2026" for Speculative Actions, which is correct; no change needed. Line 269's "$0.025 vs $0.913/task" is correct; no change.)

---

## 4. Still-open

### P0 items 2 and 5 — "The Cost of Dynamic Reasoning" (D35, E49); TraceLab (D16, E19)

1. **Scope of LATS "71.0"**: is it averaged over all benchmarks LATS was run on, or one benchmark's bar in Fig. 4? This needs a visual check of Fig. 4 (v2).
2. **Energy measurement method** in "The Cost of Dynamic Reasoning": the extracted text does not say how energy was measured (DCGM sampling or power × time). The subsection label for the 1.2 s Wikipedia sentence varied between fetches (§IV-A in two v2 passes).
3. **The exact Reflexion/LATS configurations** behind Table III ("highest-accuracy configurations in Figure 17"), meaning reflection trials and tree width/depth, were not extracted.
4. **IEEE Xplore record** (document 11408569 per search result): page numbers and DOI were not retrievable. The HPCA session day differed between two program fetches (2 vs 3 Feb 2026).
5. **Origin of "5.3×"**: it is probably an earlier snapshot of the TraceLab dashboard, but the Wayback Machine is blocked, so this cannot be confirmed. The blog G cited was not identified.
6. **Pooled vs per-agent** for the 119K/875/214 medians: the paper does not state it; I inferred "pooled" because each value lies between the two per-agent P50s.

### P0 item 3 and P1 item 13b — FocusAgent (D15, D48, D53, E30)

1. **arXiv submission history.** The abs page could not be read (fetch tool returned an empty PDF; export/API blocked by robots.txt). v1's exact date (October 2025, from the ID prefix) and whether any intermediate version existed are unresolved. v2 = 29 Aug 2026 is latest (unversioned HTML stamp).
2. **TMLR exact acceptance date.** OpenReview (forum mINaJKSy7A) returned a browser check and then 403. The TMLR list gives "August 2026" only.
3. **Table 1 vs Table 2 pruning mismatch (56% vs 51%)** for the 4.1-mini retriever on WorkArena L1. This comes from text extraction and needs a visual check of the v2 PDF.
4. **Printed percentage annotations** next to costs ("(-19%)", "(-30%)" for 5-mini, "(-21.7%)") came back once each. I computed −31.5% for 5-mini, so a printed "-30%" would be a rounding or printing difference; this needs a visual check.
5. **E30 subset size** ("33 WorkArena L1 tasks") was not re-checked. The fetch described the latency scope only as "the full evaluation set".
6. **Qwen3-235B rows and their cost cells** came from one fetch only and are not used in any patch.
7. **v1 Claude + 5-mini row** in App. B Table 5 (identical cells to the GPT-4.1 row) may be an extraction artifact. It is not used.

### P0 item 4, P1 items 9 and 13f — Continuum, PASTE (D13, D14); 2605.26297 / AgentRace (D36); KVCOMM, DroidSpeak, AgentReuse

1. **Continuum v7 §6 not read.** The fetch tool truncates the v7 HTML after the section list and the v7 PDF is not machine-readable through it. Whether Table 5 (144.9/93.4) and the v6 setup text are unchanged in v7 is unverified; v6 (25 May 2026) is the latest version whose §6 was read.
2. **Continuum v1 intro.** One fetch attributed the 1.12–3.66× sentence to v1, while a verbatim copy of the full v1 Introduction has no numbers. Treat "since v2" as likely; a human glance at v1 would settle it.
3. **Continuum metric definitions and the 8.18× baseline/model.** No formal definition of "delay" was found, and the fetched text does not name the model or the "other distributed inference solutions" in the real SWE-agent run.
4. **PASTE 1.25×/1.32×.** Not in v1 or v3 text; may be read off v3 Fig. 10 or from v2 (v2 HTML returned 429). Needs a visual check of Fig. 10 and v2.
5. **PASTE "4 nodes".** The 8 GPUs per node is verbatim (Table 1); "4 nodes, 32 total" came from the fetch summary, not a verbatim quote.
6. **2605.26297 v2.** The abs page lists only v1; the direct v2 URL was rate-limited (429). Re-check once before removing "v2 exists" for good.
7. **AgentRace authors/venue.** Anonymous on its project page and code link; OpenReview PDFs 403 and forum pages behind verification. UNRESOLVABLE from this environment.
8. **KVCOMM per-task accuracy table** (baseline vs KVCOMM on MMLU / GSM8K / HumanEval) not extracted; the MMLU-as-RAG mapping is from a fetch summary, not a verbatim quote.
9. **AgentReuse** train/test split, classifier training data and request language are not described in the fetched text; the 7 failed reuses are not analysed by the authors.
10. "From LLM Inference to Agentic Workloads" (2608.15127) half of E28 not re-checked in this pass.

### P0 items 6, 7 and P1 item 8 — Gartner (E55, E62, E73), OpenRouter (E57–E59, D18), HUMAN Security (E65)

1. **Walker LinkedIn posts** (activity 7493029883191681024, 11 Aug 2026; 7506103118410072064, 16 Sep 2026): a human with a LinkedIn login should read both and record the exact 14× / 2.8× / cached-share wording, the chart window, and whether 126.2T is a weekly total and for which week. Until then E58 and the 25,000% in E59 are secondary-only.
2. **Cached share 70% vs >85%** (D71): needs the a16z "Charts of the Week" of 21 Aug 2026 (M. Sternstein; not located on a16z.news — archive fetch returned only 2025 posts) and the LinkedIn chart.
3. **39%→66% Chinese share / 61%→34% US proprietary** (E59): no source of any kind located; origin unknown.
4. **E59 "OpenAI projected $14B loss in 2026"**: not checked.
5. **Gartner research notes** ("The Inference Paradox…", "Navigating the Commoditization Trap…", "Frontier Scale Models Threaten Software Margins and Solvency"): client-only (paywalled); baseline year and method of the ">5× through 2028" forecast are UNRESOLVABLE from public pages.
6. **HUMAN report body**: definition of "AI agents and agentic browsers", baseline (2024) volume, unit (requests / sessions), and customer mix are UNRESOLVABLE — the landing page shows headline stats and a "Request a Demo" button only; no PDF found.
7. The-decoder's "0.51 trillion to 7.3 trillion" agent tokens — period unit (daily? weekly?) not stated in the fetched text.

### P1 items 13a and 13c — EchoPath; Ares (D49), StepWise (D47), AWO (D45), WALT (D42)

1. **EchoPath abs-page metadata** (submission history, Comments/venue) — the fetch tool returned no text for `arxiv.org/abs/2609.16635`; existence of a v2 is unchecked (`/html/2609.16635v2` refused with HTTP 429). Re-check before citing.
2. **EchoPath first-pass denominator** — how many OSWorld-Verified tasks were attempted, and how many failed or were excluded before the 159-memory pool, is not stated in v1. Only the authors can answer; ask them or wait for code.
3. **EchoPath first-pass agent** — which host built the memories, and whether each host replayed its own memories, is not stated.
4. **EchoPath code** — 404 on 2026-09-27; re-check `github.com/JackZhao1998/EchoPath` periodically.
5. **Ares "up to 52.7%"** (abstract) — not located in Table 1's T_total ratios (max −45.3% on WebArena); may be a per-step or per-configuration figure. Also, the WebArena subset definition (≈129 tasks, calc.) was not quoted from the text.
6. **Ares non-headline rows** (Low / Medium / Random / GPT-5 / Gemini 3 Pro) came from a single fetch of an HTML table the tool first called corrupted; a PDF/visual check would close this. The `/pdf/2603.07915v1` fetch returned no table text.
7. **AWO v2 appendix** — Tables 7–9 were not visible in the v2 HTML fetch (apparently truncated); numbers are from v1. Confirm v2 kept them unchanged.
8. **WALT version history** — abs page gave no metadata; `/html/2510.01524v2` refused (HTTP 429). A later (ICLR camera-ready) arXiv version might change Table 2.
9. **Not checked in this pass:** Ares's router model (Qwen3-1.7B) and the UCSB/Accenture affiliation; StepWise's Yale/UNC affiliation; WALT's Table 1 per-split numbers beyond the Classifieds 64.1%.

### P1 items 10–13 — Gemini (D28, E79), Operator (D29, E39), Opus 4.8 (E83), Temporal (E70), LangChain (D24, E68), MAP (E69, D25)

1. **MAP v4 appendix B.4.2** — the 14.8% / 59.3% sentence and the Fig. 12b caption were read in v2 only; the fetch tool truncated v4 before the appendix and returned no text for any MAP PDF. A human look at https://arxiv.org/pdf/2512.04123v4 (App. B.4.2) closes this, and also the ICML PDF header.
2. **Operator exact shutdown date** — the OpenAI "Operator – Release Notes" help article (10561834) is 404; an archived copy (Wayback) would settle 31 Aug 2025 vs ~1 Aug 2025. Fetch tool blocked web.archive.org.
3. **Temporal answer options** for Chart 3.4 (which options sum to 79.8%) — rendered as an image; needs a visual check of the chart or the PDF report.
4. **LangChain first-publication date** — the Dec 2025 date is inferred from a LinkedIn post ID (calc.) and a KDnuggets "recently released" (Mar 2026); the post text and LangChain's own blog/X announcement were not readable. Also E68's "32%" quality and "57% in production" were not re-checked against the page text (quality appears as "one third").
5. **Gemini 3.5 Flash-Lite GA** (price table l. 646 says "GA 21 Jul 2026") — the blog post and model page were not checked for GA vs preview of the model itself; computer use is "Preview".
6. **AA measurement date** — AA's model pages show no "as of" date; the 329.7 t/s figure is as read on 2026-09-27 and may drift.
7. **Anthropic tool-changes feature date** — "2026-07-01" is inferred from the beta header name; no changelog entry was fetched.
8. **MAP ICLR 2026 listing** — whether an ICLR 2026 workshop version exists (OpenReview forum `AsvLggSOvS`, blocked).

### P1 items 13d and 13e — venues (D51; AAPT, SMC, SPACE); Fara-7B (D54, E90), AXIS, ComputerRL

1. **arXiv Comments fields and full submission histories** for 2510.04371, 2607.28399, 2609.03236, 2609.02042, 2511.19663 and 2508.14040 could not be read (see access notes). Whether any Comments field names a venue ("Accepted at …", "Submitted to AAAI-27") is unknown. A human opening the six abs pages would close this in two minutes.
2. **Speculative Actions v3?** and **AAPT v2?** could not be checked (429). The two AAPT fetches disagree on whether the AAAI-27 footer is present; the unversioned HTML shows it.
3. **SMC at MLSP 2026:** the official schedule is JavaScript-rendered. Check https://neuroneural.net/mlsp2026schedule/ in a browser, or IEEE Xplore after the workshop (28 Sep – 1 Oct 2026).
4. **SPACE at EMNLP 2026:** re-check the ACL Anthology EMNLP 2026 volumes when published, or the conference program (24–29 Oct 2026).
5. **AAPT at AAAI-27:** final decisions are due 30 Nov 2026.
6. **Fara-7B Appendix A** ("market rate token pricing") was absent from every extraction, so the paper's own statement of the Fara-7B per-token price is unread; the $0.2/$0.2 assumption is quoted from the Microsoft Research blog. **OpenAI computer-use-preview's $3/$12 per M** is inferred from reproducing $0.913 and was not read from OpenAI's pricing page. The Browserbase blog's chart numbers (including computer-use-preview under human verification) were not in the text extraction. "Pass@1 with up to 5 retries" is undefined.
7. **ComputerRL:** v2 has no step data. Check whether the ICLR camera-ready (OpenReview oEVfNf0w4B, blocked here) adds a step table, and confirm which model ran the §4.3 framework ablation (the fetch said GPT-4o).
8. **AXIS arXiv version** (2409.17140) was not compared with the ACL camera-ready.

### New leads (unverified)

Works that surfaced while verifying. None was read or verified in this pass; none is added to the E-ledger.

*From P0 items 2 and 5 — "The Cost of Dynamic Reasoning" (D35, E49); TraceLab (D16, E19):*

- The TraceLab live dashboard (tracelab.cs.washington.edu) has an expanded dataset: 8,058 sessions, 52 users, 665,453 steps, through 24 Jul 2026. It also has a "cache optimization could save 15.8%" figure. It may be useful for v3 if a dated snapshot or a paper revision appears.
- "The Energy Cost of Reasoning" (OpenReview Kdc8aiKxF6) is already in Appendix A, line 939; it was not checked here.

*From P0 item 3 and P1 item 13b — FocusAgent (D15, D48, D53, E30):*

- "Read More, Think More: Revisiting Observation Reduction for Web Agents", https://arxiv.org/html/2604.01535. It surfaced in the search for FocusAgent and appears to re-evaluate observation reduction for web agents. It may bear on the FocusAgent and MFS (2605.29397) rows. Not read.

*From P0 item 4, P1 items 9 and 13f — Continuum, PASTE (D13, D14); 2605.26297 / AgentRace (D36); KVCOMM, DroidSpeak, AgentReuse:*

- ThunderAgent (concurrent RL-rollout serving work cited as [36] in Continuum v6; 114.8 steps/min in Table 5).
- Gill et al., "Privacy-aware semantic cache for large language models", arXiv 2403.02694 (the source of AgentReuse's ~30% duplicate-request prior).

*From P0 items 6, 7 and P1 item 8 — Gartner (E55, E62, E73), OpenRouter (E57–E59, D18), HUMAN Security (E65):*

- Gartner, 24 Jun 2026: "Gartner Predicts AI Coding Costs Will Surpass Average Developer's Salary by 2028 as Token Consumption Surges" — https://www.gartner.com/en/newsroom/press-releases/2026-06-24-gartner-predicts-ai-coding-costs-will-surpass-average-developer-salary-by-2028-as-token-consumption-surges
- a16z "Charts of the Week", 21 Aug 2026 (agents ≈5× human token volume; >85% cached) — via ppc.land and a16z's X post https://x.com/a16z/status/2091200032162857328 (robots-blocked).
- getmegabrain, 29 Aug 2026, "AI Agents Are Burning 5x the Tokens Humans Do. The Real Bill Is Up 18%." (secondary cost model built on the cached share).
- OpenRouter blog, 25 Aug 2026, "GPT 5.6 Discounts & Jevons Paradox" (token-usage increases 5.6× / 13.8× after price cuts) — https://openrouter.ai/blog/insights/gpt-5-6-discounts-jevons-paradox/ ; relevant to "cheaper tokens → more tokens".
- HUMAN GlobeNewswire release: automated traffic +23.51% vs human +3.10% YoY (2025) — could replace the rounded "8×".

*From P1 items 10–13 — Gemini (D28, E79), Operator (D29, E39), Opus 4.8 (E83), Temporal (E70), LangChain (D24, E68), MAP (E69, D25):*

- Artificial Analysis "Time per Task" metric: Gemini 3.8 Flash (high) 2.5 min, (low) 0.8 min, vs GPT-5.6 Luna (max) 2.6 min (AA article, 2 Sep 2026) — a third-party end-to-end task-time measure that could be relevant to the "throughput ≠ task speed" argument; definition not checked.
- Gemini 2.5 Computer Use post (7 Oct 2025): "leading quality for browser control at the lowest latency, as measured by performance on the Browserbase harness for Online-Mind2Web" — its chart may carry per-task latency; values not extracted as text (the fetch tool's "~225 s" reading is not a verbatim quote and should not be used).


*From P1 items 13d and 13e — venues (D51; AAPT, SMC, SPACE); Fara-7B (D54, E90), AXIS, ComputerRL:*

- "Ghost Tool Calls: Issue-Time Privacy for Speculative Agent Tools" (arXiv 2606.02483) and "When Does Speculative Tool Execution Pay? Contention Boundaries, Latency Tails, and the Parallelism the Serial Baseline Already Had" (a GitHub issue, argszero/silicon-science-cs #50, not a paper) both appeared in search results next to SMC. They are relevant to the speculation-safety follow-up (§8.3 item 2). "Ghost Tool Calls" is already on the §8.2 P2 list (item 16).
