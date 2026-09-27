# Reference list for the slide deck (from dossier v3)

Built on 27 Sep 2026 from `Agent-Acceleration-Consolidated-Dossier-v3-2026-09-27.md` (Appendix A plus every URL in the E1–E211 and D1–D140 rows). No new research beyond verifying authors, venues and institutions. One entry per work; a preprint and its published version are one entry (the published version is cited and the arXiv ID noted).

Classes: **A** peer-reviewed venue · **B** primary data, research or official documentation/pricing from a lab or company · **C** industry analyst or survey report · **D** arXiv (or other) preprint not published at a verified venue (institutions from the paper) · **E** vendor marketing, tracker sites, secondary news and social posts (not citable; see the Excluded table).

## Counts

| Class | Entries |
|---|---|
| A | 78 |
| B | 46 |
| C | 8 |
| D | 100 |
| E (excluded URLs) | 52 |
| Citable total (A–D) | 232 |

## Check result

Output of `python3 slides/check_references.py` (re-run it after any edit):

<!-- CHECK-START -->
```
Dossier URLs (Appendix A + E/D rows): 351; mapped to a key: 299; mapped to Excluded: 52; unmapped or duplicated: 0.
Dossier rows: 351 (E 211, D 140); relying on at least one key: 324; with no citable source (listed below): 27.
Entries per class: A 78, B 46, C 8, D 100 (citable 232); E (excluded URLs) 52. BibTeX entries: 232.
Failures: 0
```
<!-- CHECK-END -->

## Entries whose authors, venue or date could not be fully verified

| Key | Class | What could not be verified |
|---|---|---|
| DeChezelles2025 | A | Venue confirmed on the official page; authors from arXiv. Listed on jmlr.org/tmlr/papers; OpenReview not readable, so authors are from arXiv. |
| Huang2026b | A | Venue confirmed on the official page; authors from arXiv. Listed on jmlr.org/tmlr/papers (acceptance year not shown on the list page; OpenReview not readable). Authors from arXiv. |
| Kapoor2025 | A | Venue confirmed on the official page; authors from arXiv. Listed on jmlr.org/tmlr/papers; OpenReview itself not readable from this environment, so authors are from arXiv. |
| Zhang2026h | A | Venue confirmed on the official page; authors from arXiv. Listed on jmlr.org/tmlr/papers (year of acceptance not shown on the list page; OpenReview not readable). Authors from arXiv. |
| OpenAI2025 | B | UNVERIFIED on the page: openai.com returns 403; title and date (23 Jan 2025) from dossier D33, which quotes the page. |
| OpenAI2026g | B | UNVERIFIED on the page: help.openai.com returns 403 to automated fetch; title from dossier E39. |
| OpenAI2026h | B | UNVERIFIED on the page: help.openai.com returns 403 to automated fetch; title from dossier E39. |
| Gartner2025 | C | gartner.com blocks automated fetch (bot wall); title and date from the URL and dossier E72. |
| Gartner2026a | C | gartner.com blocks automated fetch; title and date from the URL and dossier E62 [V]. |
| Gartner2026b | C | gartner.com blocks automated fetch; title and date from the URL and dossier E73 [V]. |
| Gartner2026c | C | gartner.com blocks automated fetch; title and date from the URL and dossier E55 [V]. |
| HUMANSecurity2026 | C | humansecurity.com returns 403 to automated fetch; title and date from dossier E65 [V, vendor]. |
| Chen2026b | D | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. HTML header names EuroSys 2027 (Rabat, April 2027); acceptance not confirmed on an official EuroSys page (dossier E117). |
| Dihan2025 | D | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. arXiv comment: "Under review at ICLR 2026"; not on the ICLR 2026 accepted list. |
| Hajimiri2026 | D | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. arXiv comment: "Accepted to EMNLP 2026"; 2026.emnlp.org has no accepted-paper list yet (checked 27 Sep 2026). |
| Hu2026 | D | UNVERIFIED: preprints.org returns 403 to automated fetch; title and first author taken from dossier §3.11 only. Not an arXiv preprint. |
| Jin2025 | D | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. The dossier cites an OpenReview PDF (id Kdc8aiKxF6); openreview.net is not readable from here, so the venue of that submission is not verified. The arXiv version has the same title and contains the 113.48× figure (E50). |
| Li2025a | D | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. English version of a 2024 paper in Journal of Computer Research and Development (CRAD) 61(11); the CRAD page (crad.ict.ac.cn) was unreachable and the DOI returned no Crossref record, so the journal version is not verified. |
| Liu2026d | D | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. PDF header and arXiv comment: IEEE MLSP 2026 (28 Sep–1 Oct 2026); the MLSP 2026 site failed TLS from here, so not verified. |
| Xu2026b | D | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. arXiv comment: "EMNLP 2026 Findings"; not verifiable on 2026.emnlp.org yet. |
| Yang2026a | D | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. arXiv comment: "EMNLP 2026 Camera Ready"; not verifiable on 2026.emnlp.org yet. |

Institution caveats (class D tags and the institution column):

| Key | Institution as recorded |
|---|---|
| Kapoor2026 | Princeton University (contact); per-author affiliations only on hal.cs.princeton.edu |
| Li2026f | no affiliation printed in the arXiv author block |
| Awadallah2025 | Microsoft (no affiliation line printed; Microsoft Research AI Frontiers report) |
| GonzalezPumariega2026 | Simular (inferred from corresponding-author e-mail; no affiliation printed) |
| Hu2026 | not verified |
| Li2026c | Carnegie Mellon University (inferred from andrew.cmu.edu e-mail; no affiliation line printed) |
| Ndzomga2026 | no affiliation printed (single author) |
| Sun2026 | UC Berkeley ("leading institution"; full affiliations only on the project site) |

## Dossier rows with no citable source

These rows rely only on excluded sources, on a source the row names without a URL, or on nothing (gap statements). They must not carry a citation on a slide; restate them with the dossier caveat or drop them.

| Row | Why no citable key |
|---|---|
| D1 | Relies only on excluded source(s) X8, X9. |
| D12 | The cited "paper" does not exist (dossier verdict: remove). |
| D28 | Relies only on excluded source(s) X34. |
| D34 | Secondary blog (zylos.ai) named without URL; dossier says drop or verify. |
| D40 | Relies only on excluded source(s) X8. |
| D71 | Relies only on excluded source(s) X42, X44. |
| E21 | Relies only on excluded source(s) X22. |
| E32 | Relies only on excluded source(s) X9. |
| E33 | Secondary blog (zylos.ai) named without URL; low confidence in the dossier. |
| E34 | Artificial Analysis named without URL (tracker site, class E). |
| E47 | Relies only on excluded source(s) X10, X11. |
| E58 | Relies only on excluded source(s) X42, X44. |
| E59 | Relies only on excluded source(s) X43, X45. |
| E63 | Relies only on excluded source(s) X36. |
| E64 | CEO statements via NBC News and event talks, no URL in the row; not citable. |
| E67 | Gap statement (no source by design). |
| E75 | Gap statement (no source by design). |
| E82 | Relies only on excluded source(s) X21. |
| E85 | Relies only on excluded source(s) X8, X9. |
| E109 | Relies only on excluded source(s) X1. |
| E159 | Relies only on excluded source(s) X41. |
| E201 | Relies only on excluded source(s) X16. |
| E202 | Relies only on excluded source(s) X10. |
| E204 | Relies only on excluded source(s) X19. |
| E205 | Relies only on excluded source(s) X17, X18. |
| E207 | Relies only on excluded source(s) X2, X4. |
| E208 | Relies only on excluded source(s) X5, X6. |

## Mapping notes

- A row maps to a key when it contains one of that work's URLs, its arXiv ID, or its name (e.g. "OSWorld-Human", "WebArena"). Rows whose Source cell says "same" or "as above" take the keys of the row above.
- Rows with no source of their own take the keys of the E rows they cite: D133, D134, D135, D136, D137, D139, D74, E206.
- Hand-mapped rows (the row names its source only in words): E41 → Yuan2026b; D3 → Yuan2026b; D38 → Yuan2026b; D39 → Abhyankar2026; D18 → OpenRouter2026a; D19 → OpenRouter2026a; D21 → OpenRouter2026a; D70 → OpenRouter2026a; D72 → OpenRouter2026a; D20 → Gartner2026a; D22 → OpenAI2026c, Anthropic2026b; D29 → OpenAI2026h; D76 → OpenAI2026h; D75 → Google2026b; D77 → Anthropic2026e; D132 → OpenAI2026a, OpenAI2026c, OpenAI2026d.
- Code repositories, project pages, venue pages and web versions of a paper map to the paper's key (see the URL map).
- Entries with "none; cited in §…" in the E/D column are cited only in dossier prose or Appendix A, not in an evidence row.

## References (A–D, sorted by class then key)

| Key | Class | Short tag | Full reference (ACM) | Institution | E/D IDs | Verification |
|---|---|---|---|---|---|---|
| Abhyankar2024 | A | [Abhyankar et al., ICML 2024] | Reyna Abhyankar, Zijian He, Vikranth Srivatsa, Hao Zhang, and Yiying Zhang. 2024. InferCept: Efficient Intercept Support for Augmented Large Language Model Inference. In Proceedings of the 41st International Conference on Machine Learning (ICML 2024), PMLR 235. Also arXiv:2402.01869. https://proceedings.mlr.press/v235/abhyankar24a.html | UC San Diego | E184, E189 | Venue and authors from the official ICML page. |
| Abhyankar2026 | A | [Abhyankar et al., MLSys 2026] | Reyna Abhyankar, Qi Qi, and Yiying Zhang. 2026. OSWorld-Human: Benchmarking the Efficiency of Computer-Use Agents. In Proceedings of Machine Learning and Systems 8 (MLSys 2026). Also arXiv:2506.16042. https://proceedings.mlsys.org/paper_files/paper/2026/hash/5edb57c05c81d04beb716ef1d542fe9e-Abstract-Conference.html | UC San Diego; GenseeAI | D5, D6, D7, D39, D56, D95, D101, E1, E2, E3, E4, E22, E23, E24, E25, E45, E111, E112 | Venue confirmed on the official page; authors from arXiv. MLSys proceedings page lists the same 3 authors. |
| Barres2026 | A | [Barres et al., ICML 2026] | Victor Barres, Honghua Dong, Soham Ray, Xujie Si, and Karthik Narasimhan. 2026. τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment. In Proceedings of the 43rd International Conference on Machine Learning (ICML 2026). Also arXiv:2506.07982. https://icml.cc/virtual/2026/poster/64377 | Sierra; University of Toronto; Vector Institute | E54, E137 | Venue and authors from the official ICML page. |
| Boisvert2024 | A | [Boisvert et al., NeurIPS 2024] | Léo Boisvert, Megh Thakkar, Maxime Gasse, Massimo Caccia, Thibault de Chezelles, Quentin Cappart, Nicolas Chapados, Alexandre Lacoste, and Alexandre Drouin. 2024. WorkArena++: Towards Compositional Planning and Reasoning-based Common Knowledge Work Tasks. In Advances in Neural Information Processing Systems 37 (NeurIPS 2024), Datasets and Benchmarks Track. Also arXiv:2407.05291. https://neurips.cc/virtual/2024/poster/97713 | ServiceNow Research; Mila; Polytechnique Montréal; Chandar Research Lab | D30, E16 | Venue and authors from the official NeurIPS page. DOI 10.52202/079017-0195 |
| Chen2025 | A | [Chen et al., ICCV 2025] | Gongwei Chen, Xurui Zhou, Rui Shao, Yibo Lyu, Kaiwen Zhou, Shuai Wang, Wentao Li, Yinchuan Li, Zhongang Qi, and Liqiang Nie. 2025. Less is More: Empowering GUI Agent with Context-Aware Simplification. In 2025 IEEE/CVF International Conference on Computer Vision (ICCV 2025). Also arXiv:2507.03730. https://openaccess.thecvf.com/content/ICCV2025/html/Chen_Less_is_More_Empowering_GUI_Agent_with_Context-Aware_Simplification_ICCV_2025_paper.html | Harbin Institute of Technology (Shenzhen); Huawei Noah’s Ark Lab | none; cited in §2.2, §3.5, App. A | Venue, DOI and authors from publisher DOI metadata (Crossref, 10.1109/iccv51701.2025.00558); author list identical to arXiv. |
| Chung2026 | A | [Chung et al., MobiSys 2026] | Jinha Chung, Byeongjun Shin, Jiin Kim, and Minsoo Rhu. 2026. Agent-X: Full Pipeline Acceleration of On-device AI Agents. In Proceedings of the 24th Annual International Conference on Mobile Systems, Applications and Services (MobiSys 2026). Also arXiv:2605.10380. https://doi.org/10.1145/3745756.3809195 | KAIST | none; cited in §3.5, §3.10, App. A | Venue, DOI and authors from publisher DOI metadata (Crossref, 10.1145/3745756.3809195); author list identical to arXiv. |
| DeChezelles2025 | A | [De Chezelles et al., TMLR 2025] | Thibault Le Sellier De Chezelles, Maxime Gasse, Alexandre Drouin, Massimo Caccia, Léo Boisvert, Megh Thakkar, Tom Marty, Rim Assouel, Sahar Omidi Shayegan, Lawrence Keunho Jang, Xing Han Lù, Ori Yoran, Dehan Kong, Frank F. Xu, Siva Reddy, Quentin Cappart, Graham Neubig, Ruslan Salakhutdinov, Nicolas Chapados, and Alexandre Lacoste. 2025. The BrowserGym Ecosystem for Web Agent Research. In Transactions on Machine Learning Research (TMLR). Also arXiv:2412.05467. https://openreview.net/forum?id=5298fKGmv3 | ServiceNow Research; Mila; Polytechnique Montréal; CMU; McGill; Tel Aviv University; Université de Montréal; iMean AI | D41, E11, E26 | Venue confirmed on the official page; authors from arXiv. Listed on jmlr.org/tmlr/papers; OpenReview not readable, so authors are from arXiv. |
| Drouin2024 | A | [Drouin et al., ICML 2024] | Alexandre Drouin, Maxime Gasse, Massimo Caccia, Issam Laradji, Manuel Del Verme, Tom Marty, David Vazquez, Nicolas Chapados, and Alexandre Lacoste. 2024. WorkArena: How Capable Are Web Agents at Solving Common Knowledge Work Tasks?. In Proceedings of the 41st International Conference on Machine Learning (ICML 2024). Also arXiv:2403.07718. https://icml.cc/virtual/2024/poster/34722 | ServiceNow Research; Mila; Polytechnique Montréal; McGill University; Université de Montréal | D15, D58, D59, D60, D119, E11, E16, E30 | Venue and authors from the official ICML page. Venue author list differs from arXiv (9 vs 12 names or order); venue list used. |
| Erol2026 | A | [Erol et al., ICLR 2026] | Mehmet Hamza Erol, Batu El, Mirac Suzgun, Mert Yuksekgonul, and James Y Zou. 2026. Cost-of-Pass: An Economic Framework for Evaluating Language Models. In The Fourteenth International Conference on Learning Representations (ICLR 2026). Also arXiv:2504.13359. https://iclr.cc/virtual/2026/poster/10006834 | Stanford University | E52 | Venue and authors from the official ICLR page. |
| Gill2025 | A | [Gill et al., IPDPS 2025] | Waris Gill, Mohamed Elidrisi, Pallavi Kalapatapu, Ammar Ahmed, Ali Anwar, and Muhammad Ali Gulzar. 2025. MeanCache: User-Centric Semantic Caching for LLM Web Services. In 2025 IEEE International Parallel and Distributed Processing Symposium (IPDPS 2025). Also arXiv:2403.02694. https://doi.org/10.1109/IPDPS64566.2025.00117 | Virginia Tech; Cisco; University of Minnesota | E188 | Venue, DOI and authors from publisher DOI metadata (Crossref, 10.1109/ipdps64566.2025.00117); author list identical to arXiv. |
| Gim2025 | A | [Gim et al., SOSP 2025] | In Gim, Zhiyao Ma, Seung-seob Lee, and Lin Zhong. 2025. Pie: A Programmable Serving System for Emerging LLM Applications. In Proceedings of the ACM SIGOPS 31st Symposium on Operating Systems Principles (SOSP 2025). Also arXiv:2510.24051. https://doi.org/10.1145/3731569.3764814 | Yale University | none; cited in §2.2, §3.6, §3.10, App. A | Venue, DOI and authors from publisher DOI metadata (Crossref, 10.1145/3731569.3764814); author list identical to arXiv. |
| Gou2025 | A | [Gou et al., NeurIPS 2025] | Boyu Gou, Zanming Huang, Yuting Ning, Yu Gu, Michael Lin, Weijian Qi, Andrei Kopanev, Botao Yu, Bernal Jimenez Gutierrez, Yiheng Shu, et al. (26 authors in total). 2025. Mind2Web 2: Evaluating Agentic Search with Agent-as-a-Judge. In Advances in Neural Information Processing Systems 38 (NeurIPS 2025), Datasets and Benchmarks Track. Also arXiv:2506.21506. https://neurips.cc/virtual/2025/poster/121798 | The Ohio State University; Amazon AGI | D116, D118, D121, E14 | Venue and authors from the official NeurIPS page. DOI 10.52202/085713-5778 |
| Guan2026 | A | [Guan et al., ICLR 2026] | Yilin Guan, Qingfeng Lan, Fei Sun, Dujian Ding, Devang Acharya, Chi Wang, William Wang, and Wenyue Hua. 2026. Dynamic Speculative Agent Planning. In The Fourteenth International Conference on Learning Representations (ICLR 2026). Also arXiv:2509.01920. https://iclr.cc/virtual/2026/poster/10008884 | University of British Columbia; University of Alberta; UC Santa Barbara; Google DeepMind; Avey Research Center | D103 | Venue and authors from the official ICLR page. Venue author list differs from arXiv (8 vs 8 names or order); venue list used. |
| Guo2026 | A | [Guo et al., Findings ACL 2026] | Yaoqi Guo, Ying Xiao, Jie M. Zhang, Mark Harman, Yiling Lou, Yang Liu, and Zhenpeng Chen. 2026. EET: Experience-Driven Early Termination for Cost-Efficient Software Engineering Agents. In Findings of the Association for Computational Linguistics: ACL 2026. Also arXiv:2601.05777. https://aclanthology.org/2026.findings-acl.1652/ | King’s College London; UCL; UIUC; Nanyang Technological University; Tsinghua University | none; cited in §2.2, §3.7, App. A | Venue, DOI and authors from publisher DOI metadata (Crossref, 10.18653/v1/2026.findings-acl.1652); author list identical to arXiv. |
| Hu2025 | A | [Hu et al., ACL 2025] | Xueyu Hu, Tao Xiong, Biao Yi, Zishu Wei, Ruixuan Xiao, Yurun Chen, Jiasheng Ye, Meiling Tao, Xiangxin Zhou, Ziyu Zhao, et al. (29 authors in total). 2025. OS Agents: A Survey on MLLM-based Agents for Computer, Phone and Browser Use. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers) (ACL 2025). https://aclanthology.org/2025.acl-long.369/ |  | none; cited in §3.11, App. A | Authors, venue and DOI 10.18653/v1/2025.acl-long.369 from the ACL Anthology page. |
| Hua2025 | A | [Hua et al., ICLR 2025] | Wenyue Hua, Mengting Wan, Jagannath Vadrevu, Ryan Nadel, Yongfeng Zhang, and Chi Wang. 2025. Interactive Speculative Planning: Enhance Agent Efficiency through Co-design of System and User Interface. In The Thirteenth International Conference on Learning Representations (ICLR 2025). https://proceedings.iclr.cc/paper_files/paper/2025/hash/25458943db16e0f78f748ca5bc34fff6-Abstract-Conference.html |  | none; cited in §0.4, §2.2, §3.3, §3.10, §4.1, §4.2, §5.4, App. A | Authors and venue from the ICLR 2025 proceedings abstract page (citation meta tags). Affiliations not collected (class A). |
| Huang2026b | A | [Huang et al., TMLR 2026] | Kung-Hsiang Huang, Haoyi Qiu, Yutong Dai, Caiming Xiong, and Chien-Sheng Wu. 2026. GUI-KV: Efficient GUI Agents via KV Cache with Spatio-Temporal Awareness. In Transactions on Machine Learning Research (TMLR). Also arXiv:2510.00536. https://openreview.net/forum?id=qaJECugPzr | Salesforce AI Research; UCLA | D127 | Venue confirmed on the official page; authors from arXiv. Listed on jmlr.org/tmlr/papers (acceptance year not shown on the list page; OpenReview not readable). Authors from arXiv. |
| Kang2026 | A | [Kang et al., ICML 2026] | Hao Kang, Ziyang Li, Xinyu Yang, Weili Xu, Yinfang Chen, Junxiong Wang, Beidi Chen, Tushar Krishna, Chenfeng Xu, and Simran Arora. 2026. ThunderAgent: A Fast, Simple, and Program-Aware Agentic Inference System. In Proceedings of the 43rd International Conference on Machine Learning (ICML 2026). Also arXiv:2602.13692, titled "ThunderAgent: A Simple, Fast and Program-Aware Agentic Inference System". https://icml.cc/virtual/2026/poster/62040 | Georgia Tech; CMU; UIUC; Together AI | D14, D62, D100, D129, E108, E184, E186, E189 | Venue and authors from the official ICML page. Venue author list differs from arXiv (10 vs 10 names or order); venue list used. ICML title: "ThunderAgent: A Fast, Simple, and Program-Aware Agentic Inference System". |
| Kapoor2025 | A | [Kapoor et al., TMLR 2025] | Sayash Kapoor, Benedikt Stroebl, Zachary S. Siegel, Nitya Nadgir, and Arvind Narayanan. 2025. AI Agents That Matter. In Transactions on Machine Learning Research (TMLR). Also arXiv:2407.01502. https://openreview.net/forum?id=Zy4uFzMviZ | Princeton University | D26, E53, E89 | Venue confirmed on the official page; authors from arXiv. Listed on jmlr.org/tmlr/papers; OpenReview itself not readable from this environment, so authors are from arXiv. |
| Kapoor2026 | A | [Kapoor et al., ICLR 2026] | Sayash Kapoor, Benedikt Stroebl, Peter Kirgis, Nitya Nadgir, Zachary Siegel, Boyi Wei, Tianci Xue, Ziru Chen, Felix Chen, Saiteja Utpala, et al. (31 authors in total). 2026. Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation. In The Fourteenth International Conference on Learning Representations (ICLR 2026). Also arXiv:2510.11977. https://iclr.cc/virtual/2026/poster/10006806 | Princeton University (contact); per-author affiliations only on hal.cs.princeton.edu | D31, E43, E88 | Venue and authors from the official ICLR page. Leaderboard at hal.cs.princeton.edu. |
| Kerboua2026 | A | [Kerboua et al., TMLR 2026] | Imene Kerboua, Sahar Omidi Shayegan, Megh Thakkar, Xing Han Lù, Léo Boisvert, Massimo Caccia, Jérémy Espinas, Alexandre Aussem, Véronique Eglin, and Alexandre Lacoste. 2026. FocusAgent: Simple Yet Effective Ways of Trimming the Large Context of Web Agents. In Transactions on Machine Learning Research (TMLR). Also arXiv:2510.03204. https://openreview.net/forum?id=mINaJKSy7A | ServiceNow Research; Mila; Polytechnique Montréal; McGill; INSA Lyon; Esker | D15, D48, D53, D58, D59, D60, E30 | Venue confirmed on the official page; authors from arXiv. Listed on jmlr.org/tmlr/papers; arXiv comment "TMLR 08/2026". Authors from arXiv. |
| Kim2024 | A | [Kim et al., ICML 2024] | Sehoon Kim, Suhong Moon, Ryan Tabrizi, Nicholas Lee, Michael Mahoney, EECS Kurt Keutzer, and Amir Gholaminejad. 2024. An LLM Compiler for Parallel Function Calling. In Proceedings of the 41st International Conference on Machine Learning (ICML 2024). Also arXiv:2312.04511. https://icml.cc/virtual/2024/poster/32829 | UC Berkeley; ICSI; LBNL | none; cited in §0.4, §2.2, §3.4, §3.10, §4.1, App. A | Venue and authors from the official ICML page. Venue author list differs from arXiv (7 vs 7 names or order); venue list used. |
| Kim2026a | A | [Kim et al., MLSys 2026] | Hojoon Kim, Yuheng Wu, and Thierry Tambe. 2026. AgenticCache: Cache-Driven Asynchronous Planning for Embodied AI Agents. In Proceedings of Machine Learning and Systems 8 (MLSys 2026). Also arXiv:2604.24039. https://proceedings.mlsys.org/paper_files/paper/2026/hash/c66a9db149261435664284a20b6f1d42-Abstract-Conference.html | Seoul National University; Stanford University | none; cited in §2.2, §3.2, App. A | Venue confirmed on the official page; authors from arXiv. MLSys proceedings page lists the same 3 authors. |
| Kim2026b | A | [Kim et al., HPCA 2026] | Jiin Kim, Byeongjun Shin, Jinha Chung, and Minsoo Rhu. 2026. The Cost of Dynamic Reasoning: Demystifying AI Agents and Test-Time Scaling from an AI Infrastructure Perspective. In 2026 IEEE International Symposium on High Performance Computer Architecture (HPCA 2026). Also arXiv:2506.04301. https://doi.org/10.1109/HPCA68181.2026.11408569 | KAIST | D8, D35, D57, E49 | Venue, DOI and authors from publisher DOI metadata (Crossref, 10.1109/hpca68181.2026.11408569); author list identical to arXiv. |
| Kwa2025 | A | [Kwa et al., NeurIPS 2025] | Thomas Kwa, Ben West, Joel Becker, Amy Deng, Katharyn Garcia, Max Hasin, Sami Jawhar, Megan Kinniment, Nate Rush, Sydney Von Arx, et al. (25 authors in total). 2025. Measuring AI Ability to Complete Long Software Tasks. In Advances in Neural Information Processing Systems 38 (NeurIPS 2025). Also arXiv:2503.14499. https://neurips.cc/virtual/2025/poster/119302 | METR (Model Evaluation & Threat Research) | D116, E166 | Venue and authors from the official NeurIPS page. Venue author list differs from arXiv (25 vs 26 names or order); venue list used. DOI 10.52202/085713-3086 |
| Lai2026 | A | [Lai et al., ICLR 2026] | Hanyu Lai, Xiao Liu, Yanxiao Zhao, Han Xu, Hanchen Zhang, Bohao Jing, Yanyu Ren, Shuntian Yao, Yuxiao Dong, and Jie Tang. 2026. ComputerRL: Scaling End-to-End Online Reinforcement Learning for Computer Use Agents. In The Fourteenth International Conference on Learning Representations (ICLR 2026). Also arXiv:2508.14040. https://iclr.cc/virtual/2026/poster/10007435 | Tsinghua University; Z.AI; University of Chinese Academy of Sciences | D93 | Venue and authors from the official ICLR page. |
| Lee2025 | A | [Lee et al., UIST 2025] | Seoyoung Lee, Seobin Yoon, Seongbeen Lee, Hyesoo Kim, and Joo Yong Sim. 2025. Log2Plan: An Adaptive GUI Automation Framework Integrated with Task Mining Approach. In Proceedings of the 38th Annual ACM Symposium on User Interface Software and Technology (UIST 2025). Also arXiv:2509.22137. https://doi.org/10.1145/3746059.3747663 | Sookmyung Women’s University | none; cited in §3.2, §3.12, §8.2, App. A | Venue, DOI and authors from publisher DOI metadata (Crossref, 10.1145/3746059.3747663); author list identical to arXiv. |
| Li2025c | A | [Li et al., ACM MM 2025] | Kaixin Li, Ziyang Meng, Hongzhan Lin, Ziyang Luo, Yuchen Tian, Jing Ma, Zhiyong Huang, and Tat-Seng Chua. 2025. ScreenSpot-Pro: GUI Grounding for Professional High-Resolution Computer Use. In Proceedings of the 33rd ACM International Conference on Multimedia (MM 2025). Also arXiv:2504.07981. https://doi.org/10.1145/3746027.3755688 | National University of Singapore; East China Normal University; Hong Kong Baptist University | none; cited in §2.2, §3.5, §5.8, App. A | Venue, DOI and authors from publisher DOI metadata (Crossref, 10.1145/3746027.3755688); author list identical to arXiv. |
| Li2026f | A | [Li et al., ICASSP 2026] | Tao Li, Jinlong Hu, Yang Wang, Junfeng Liu, and Xuejun Liu. 2026. WebRouter: Query-specific Router via Variational Information Bottleneck for Cost-sensitive Web Agent. In ICASSP 2026, IEEE International Conference on Acoustics, Speech and Signal Processing. Also arXiv:2510.11221. https://doi.org/10.1109/ICASSP55912.2026.11464950 | no affiliation printed in the arXiv author block | none; cited in §2.2, §3.5, §5.4, App. A | Venue, DOI and authors from publisher DOI metadata (Crossref, 10.1109/icassp55912.2026.11464950); author list identical to arXiv. |
| Lin2024 | A | [Lin et al., OSDI 2024] | Chaofan Lin, Zhenhua Han, Chengruidong Zhang, Yuqing Yang, Fan Yang, Chen Chen, and Lili Qiu. 2024. Parrot: Efficient Serving of LLM-based Applications with Semantic Variable. In 18th USENIX Symposium on Operating Systems Design and Implementation (OSDI 24). https://www.usenix.org/conference/osdi24/presentation/lin-chaofan |  | E173 | Authors and venue from the USENIX OSDI 24 presentation page. |
| Lin2025 | A | [Lin et al., CVPR 2025] | Kevin Qinghong Lin, Linjie Li, Difei Gao, Zhengyuan Yang, Shiwei Wu, Zechen Bai, Stan Weixian Lei, Lijuan Wang, and Mike Zheng Shou. 2025. ShowUI: One Vision-Language-Action Model for GUI Visual Agent. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR 2025). https://openaccess.thecvf.com/content/CVPR2025/html/Lin_ShowUI_One_Vision-Language-Action_Model_for_GUI_Visual_Agent_CVPR_2025_paper.html |  | none; cited in §2.2, §3.5, §3.10, App. A | Authors and venue from the CVF Open Access page (citation meta tags). |
| Liu2026b | A | [Liu et al., COLM 2026] | Tengxiao Liu, Zifeng Wang, Jin Miao, I-Hung Hsu, Jun Yan, Jiefeng Chen, Rujun Han, Fangyuan Xu, Yanfei Chen, Ke Jiang, Samira Daruki, Yi Liang, William Yang Wang, Tomas Pfister, and Chen-Yu Lee. 2026. Budget-Aware Tool Use Enables Effective Agent Scaling. In Third Conference on Language Modeling (COLM 2026). Also arXiv:2511.17006. https://colm.cc/Conferences/2026/AcceptedPapers | Google Cloud AI Research; Google DeepMind; UC Santa Barbara; NYU | none; cited in §2.2, §3.7, §3.9, §3.10, §3.12, §5.5, §5.8, App. A | Venue confirmed on the official page; authors from arXiv. On the official COLM 2026 accepted-papers page with the same 15 authors. |
| Liu2026c | A | [Liu et al., NSDI 2026] | Yuhan Liu, Yuyang Huang, Jiayi Yao, Shaoting Feng, Zhuohan Gu, Kuntai Du, Hanchen Li, Yihua Cheng, Junchen Jiang, Shan Lu, Madan Musuvathi, and Esha Choukse. 2026. DroidSpeak: KV Cache Sharing Across Fine-tuned Model Variants. In 23rd USENIX Symposium on Networked Systems Design and Implementation (NSDI 26). https://www.usenix.org/conference/nsdi26/presentation/liu-yuhan |  | D127 | Authors and venue from the USENIX NSDI 26 presentation page. |
| Lu2025a | A | [Lu et al., ACL 2025] | Junting Lu, Zhiyang Zhang, Fangkai Yang, Jue Zhang, Lu Wang, Chao Du, Qingwei Lin, Saravan Rajmohan, Dongmei Zhang, and Qi Zhang. 2025. AXIS: Efficient Human-Agent-Computer Interaction with API-First LLM-Based Agents. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers) (ACL 2025). https://aclanthology.org/2025.acl-long.381/ |  | D92, D116, D119, D121, E161 | Authors, venue and DOI 10.18653/v1/2025.acl-long.381 from the ACL Anthology page. |
| Lu2025b | A | [Lu et al., Findings EMNLP 2025] | Qingyu Lu, Liang Ding, Siyi Cao, Xuebo Liu, Kanjian Zhang, Jinxia Zhang, and Dacheng Tao. 2025. Runaway is Ashamed, But Helpful: On the Early-Exit Behavior of Large Language Model-based Agents in Embodied Environments. In Findings of the Association for Computational Linguistics: EMNLP 2025. Also arXiv:2505.17616. https://aclanthology.org/2025.findings-emnlp.1304/ | Southeast University; Harbin Institute of Technology (Shenzhen); Nanyang Technological University; University of Sydney | none; cited in §2.2, §3.7, App. A | Venue, DOI and authors from publisher DOI metadata (Crossref, 10.18653/v1/2025.findings-emnlp.1304); author list identical to arXiv. |
| Luo2026 | A | [Luo et al., NSDI 2026] | Michael Luo, Xiaoxiang Shi, Colin Cai, Tianjun Zhang, Justin Wong, Yichuan Wang, Chi Wang, Yanping Huang, Zhifeng Chen, Joseph E. Gonzalez, and Ion Stoica. 2026. Agentix: An Efficient Serving Engine for LLM Agents as General Programs. In 23rd USENIX Symposium on Networked Systems Design and Implementation (NSDI 26). https://www.usenix.org/conference/nsdi26/presentation/luo |  | D52, D63, D128, E185 | Authors and venue from the USENIX NSDI 26 presentation page. |
| Mialon2024 | A | [Mialon et al., ICLR 2024] | Grégoire Mialon, Clémentine Fourrier, Thomas Wolf, Yann LeCun, and Thomas Scialom. 2024. GAIA: a benchmark for General AI Assistants. In The Twelfth International Conference on Learning Representations (ICLR 2024). Also arXiv:2311.12983. https://iclr.cc/virtual/2024/poster/18176 | Meta (FAIR, GenAI); Hugging Face; AutoGPT | E29, E48, E107, E128, E170, E172, E181, E189 | Venue and authors from the official ICLR page. Venue author list differs from arXiv (5 vs 6 names or order); venue list used. |
| Nguyen2025 | A | [Nguyen et al., Findings ACL 2025] | Dang Nguyen, Jian Chen, Yu Wang, Gang Wu, Namyong Park, Zhengmian Hu, Hanjia Lyu, Junda Wu, Ryan Aponte, Yu Xia, et al. (30 authors in total). 2025. GUI Agents: A Survey. In Findings of the Association for Computational Linguistics: ACL 2025. Also arXiv:2412.13501. https://aclanthology.org/2025.findings-acl.1158/ | Adobe Research; UC San Diego; CMU; University of Maryland; others (10 institutions) | none; cited in §3.11, App. A | Venue confirmed on the official page; authors from arXiv. ACL Anthology lists the same 30 authors. |
| Ong2025 | A | [Ong et al., ICLR 2025] | Isaac Ong, Amjad Almahairi, Vincent Wu, Wei-Lin Chiang, Tianhao Wu, Joseph E Gonzalez, M Kadous, and Ion Stoica. 2025. RouteLLM: Learning to Route LLMs from Preference Data. In The Thirteenth International Conference on Learning Representations (ICLR 2025). Also arXiv:2406.18665, titled "RouteLLM: Learning to Route LLMs with Preference Data". https://iclr.cc/virtual/2025/poster/30737 | UC Berkeley; Anyscale; Canva | none; cited in §2.2, §3.5, §5.3, §5.4, §5.5, App. A | Venue and authors from the official ICLR page. ICLR title: "RouteLLM: Learning to Route LLMs from Preference Data". |
| Pan2025 | A | [Pan et al., NeurIPS 2025] | Zaifeng Pan, AJJKUMAR DAHYALAL PATEL, Yipeng Shen, Zhengding Hu, Yue Guan, Wan-Lu Li, Lianhui Qin, Yida Wang, and Yufei Ding. 2025. KVFlow: Efficient Prefix Caching for Accelerating LLM-Based Multi-Agent Workflows. In Advances in Neural Information Processing Systems 38 (NeurIPS 2025). Also arXiv:2507.07400. https://neurips.cc/virtual/2025/poster/119883 | UC San Diego; AWS | E173, E182 | Venue and authors from the official NeurIPS page. Venue author list differs from arXiv (9 vs 9 names or order); venue list used. DOI 10.52202/085713-4208 |
| Pan2026a | A | [Pan et al., ICML 2026] | Melissa Pan, Negar Arabzadeh, Riccardo Cogo, Yuxuan Zhu, Alexander Xiong, Lakshya A Agrawal, Huanzhi Mao, Emma Shen, Sid Pallerla, Liana Patel, et al. (25 authors in total). 2026. Characterizing Agents in Production. In Proceedings of the 43rd International Conference on Machine Learning (ICML 2026), Oral. Also arXiv:2512.04123, titled "Measuring Agents in Production". https://icml.cc/virtual/2026/poster/61834 | UC Berkeley; Stanford; UIUC; IBM Research; Intesa Sanpaolo | D25, D79, D80, D81, E69 | Venue and authors from the official ICML page. ICML title: "Characterizing Agents in Production" (arXiv: "Measuring Agents in Production"). |
| Patwardhan2026 | A | [Patwardhan et al., ICLR 2026] | Tejal Patwardhan, Rachel Dias, Elizabeth Proehl, Grace Kim, Michele Wang, Olivia Watkins, Simon Fishman, Marwan Aljubeh, Phoebe Thacker, Laurance Fauconnet, Natalie Kim, Samuel Miserendino, Gildas Chabot, David Li, Patrick Chao, Michael Sharman, Alexandra Barr, Amelia Glaese, and Jerry Tworek. 2026. GDPval: Evaluating AI Model Performance on Real-World Economically Valuable Tasks. In The Fourteenth International Conference on Learning Representations (ICLR 2026). Also arXiv:2510.04374. https://iclr.cc/virtual/2026/poster/10008039 | OpenAI | D119, D121, D135, E164, E165, E195, E206 | Venue and authors from the official ICLR page. Venue author list differs from arXiv (19 vs 19 names or order); venue list used. Also published as an OpenAI web page (openai.com/index/gdpval). |
| Perera2026 | A | [Perera et al., CAIS 2026] | Srinath Perera, Kaviru Hapuarachchi, Frank Leymann, and Rania Khalaf. 2026. Robust Agent Compensation (RAC): Teaching AI Agents to Compensate. In Proceedings of the ACM Conference on AI and Agentic Systems (CAIS 2026). Also arXiv:2605.03409. https://doi.org/10.1145/3786335.3813141 | WSO2; University of Stuttgart | D107, E137 | Venue, DOI and authors from publisher DOI metadata (Crossref, 10.1145/3786335.3813141); author list identical to arXiv. Also on caisconf.org/program/2026/papers. |
| Prabhu2026 | A | [Prabhu et al., ICLR 2026] | Viraj Prabhu, Yutong Dai, Matthew Fernandez, Krithika Ramakrishnan, Jing Gu, Yanqi Luo, silvio savarese, Caiming Xiong, Junnan Li, Zeyuan Chen, and Ran Xu. 2026. WALT: Web Agents that Learn Tools. In The Fourteenth International Conference on Learning Representations (ICLR 2026). Also arXiv:2510.01524. https://iclr.cc/virtual/2026/poster/10008481 | Salesforce AI Research | D42 | Venue and authors from the official ICLR page. Venue author list differs from arXiv (11 vs 11 names or order); venue list used. |
| Qin2026 | A | [Qin et al., ICML 2026] | Zerui Qin, Sheng Yue, Xingyuan Hua, Yongjian Fu, and Ju Ren. 2026. Executable Agentic Memory for GUI Agent. In Proceedings of the 43rd International Conference on Machine Learning (ICML 2026). Also arXiv:2605.12294. https://icml.cc/virtual/2026/poster/65931 | Sun Yat-sen University; Tsinghua University | none; cited in §2.2, §3.2, §3.10, App. A | Venue and authors from the official ICML page. |
| Shen2025 | A | [Shen et al., NeurIPS 2025] | Junhong Shen, Hao Bai, Lunjun Zhang, Yifei Zhou, Amrith Setlur, Peter Tong, Diego Caples, Nan Jiang, Tong Zhang, Ameet Talwalkar, and Aviral Kumar. 2025. Thinking vs. Doing: Improving Agent Reasoning by Scaling Test-Time Interaction. In Advances in Neural Information Processing Systems 38 (NeurIPS 2025). Also arXiv:2506.07976, titled "Thinking vs. Doing: Agents that Reason by Scaling Test-Time Interaction". https://neurips.cc/virtual/2025/poster/115466 | Carnegie Mellon University; UC Berkeley; NYU; UIUC; University of Toronto; others | none; cited in §2.2, §3.7, §3.9, §3.12, §5.8, App. A | Venue and authors from the official NeurIPS page. NeurIPS title: "Thinking vs. Doing: Improving Agent Reasoning by Scaling Test-Time Interaction". |
| Shome2026 | A | [Shome et al., CAIS 2026] | Pradyumna Shome, Sashreek Krishnan, and Sauvik Das. 2026. Why Johnny Can't Use Agents: Industry Aspirations vs. User Realities with AI Agents. In Proceedings of the ACM Conference on AI and Agentic Systems (CAIS 2026). Also arXiv:2509.14528. https://doi.org/10.1145/3786335.3813140 | Carnegie Mellon University | E71 | Venue, DOI and authors from publisher DOI metadata (Crossref, 10.1145/3786335.3813140); author list identical to arXiv. Also on caisconf.org/program/2026/papers. |
| Song2025 | A | [Song et al., Findings ACL 2025] | Yueqi Song, Frank F. Xu, Shuyan Zhou, and Graham Neubig. 2025. Beyond Browsing: API-Based Web Agents. In Findings of the Association for Computational Linguistics: ACL 2025. Also arXiv:2410.16464. https://aclanthology.org/2025.findings-acl.577/ | Carnegie Mellon University | none; cited in §2.2, §3.1, §5.3, §5.5, §5.8, App. A | Venue, DOI and authors from publisher DOI metadata (Crossref, 10.18653/v1/2025.findings-acl.577); author list identical to arXiv. |
| Song2026 | A | [Song et al., ICLR 2026] | Linxin Song, Yutong Dai, Viraj Prabhu, Jieyu Zhang, Taiwei Shi, Li Li, Junnan Li, silvio savarese, Zeyuan Chen, Jieyu Zhao, Ran Xu, and Caiming Xiong. 2026. CoAct-1: Computer-using Multi-Agent System with Coding Actions. In The Fourteenth International Conference on Learning Representations (ICLR 2026). Also arXiv:2508.03923. https://iclr.cc/virtual/2026/poster/10007725 | University of Southern California; Salesforce; University of Washington | none; cited in §3.1, §3.10, App. A | Venue and authors from the official ICLR page. |
| Srivatsa2025 | A | [Srivatsa et al., ICLR 2025] | Vikranth Srivatsa, Zijian He, Reyna Abhyankar, Dongming Li, and Yiying Zhang. 2025. Preble: Efficient Distributed Prompt Scheduling for LLM Serving. In The Thirteenth International Conference on Learning Representations (ICLR 2025). Also arXiv:2407.00023. https://iclr.cc/virtual/2025/poster/28456 | UC San Diego | E185 | Venue and authors from the official ICLR page. |
| Wadlom2026 | A | [Wadlom et al., SIGMOD 2026] | Noppanat Wadlom, Junyi Shen, and Yao Lu. 2026. Efficient LLM Serving for Agentic Workflows: A Data Systems Perspective. In Proceedings of the ACM on Management of Data 4 (SIGMOD 2026). Also arXiv:2603.16104. https://doi.org/10.1145/3802046 | National University of Singapore | E173 | Venue, DOI and authors from publisher DOI metadata (Crossref, 10.1145/3802046); author list identical to arXiv. Journal: Proc. ACM Manag. Data (PACMMOD). |
| Wang2025a | A | [Wang et al., ICML 2025] | Zhiruo Wang, Jiayuan Mao, Daniel Fried, and Graham Neubig. 2025. Agent Workflow Memory. In Proceedings of the 42nd International Conference on Machine Learning (ICML 2025). Also arXiv:2409.07429. https://icml.cc/virtual/2025/poster/45496 | Carnegie Mellon University; MIT | D41 | Venue and authors from the official ICML page. |
| Wang2025c | A | [Wang et al., COLM 2025] | Zora Zhiruo Wang, Apurva Gandhi, Graham Neubig, and Daniel Fried. 2025. Inducing Programmatic Skills for Agentic Tasks. In Second Conference on Language Modeling (COLM 2025). Also arXiv:2504.06821. https://openreview.net/forum?id=lsAY6fWsog | Carnegie Mellon University | D41 | Venue confirmed on the official page; authors from arXiv. On colmweb.org/2025/AcceptedPapers.html with the same 4 authors. |
| Wen2025 | A | [Wen et al., MobiSys 2025] | Hao Wen, Shizuo Tian, Borislav Pavlov, Wenjie Du, Yixuan Li, Ge Chang, Shanhui Zhao, Jiacheng Liu, Yunxin Liu, Ya-Qin Zhang, and Yuanchun Li. 2025. AutoDroid-V2: Boosting SLM-based GUI Agents via Code Generation. In Proceedings of the 23rd Annual International Conference on Mobile Systems, Applications and Services (MobiSys 2025). Also arXiv:2412.18116. https://doi.org/10.1145/3711875.3729134 | Tsinghua University (AIR); Shanghai AI Laboratory; BAAI | none; cited in §0.4, §3.1, §3.10, App. A | Venue, DOI and authors from publisher DOI metadata (Crossref, 10.1145/3711875.3729134); author list identical to arXiv. |
| Winston2026 | A | [Winston et al., ICML 2026] | Caleb Winston, Ron Yifeng Wang, Azalia Mirhoseini, and Christoforos Kozyrakis. 2026. Agent JIT Compilation for Latency-Optimizing Web Agent Planning and Scheduling. In Proceedings of the 43rd International Conference on Machine Learning (ICML 2026). Also arXiv:2605.21470. https://icml.cc/virtual/2026/poster/66062 | Stanford University | D43, D96, D97, E18, E100, E101 | Venue and authors from the official ICML page. |
| Wornow2024 | A | [Wornow et al., PVLDB 2024] | Michael Wornow, Avanika Narayan, Krista Opsahl-Ong, Quinn McIntyre, Nigam Shah, and Christopher Ré. 2024. Automating the Enterprise with Foundation Models. In Proceedings of the VLDB Endowment 17 (PVLDB). Also arXiv:2405.03710. https://doi.org/10.14778/3681954.3681964 | Stanford University | E148 | Venue, DOI and authors from publisher DOI metadata (Crossref, 10.14778/3681954.3681964); author list identical to arXiv. |
| Xia2025 | A | [Xia et al., FSE 2025] | Chunqiu Steven Xia, Yinlin Deng, Soren Dunn, and Lingming Zhang. 2025. Demystifying LLM-Based Software Engineering Agents. In Proceedings of the ACM on Software Engineering 2, FSE (FSE 2025). Also arXiv:2407.01489, titled "Agentless: Demystifying LLM-based Software Engineering Agents". https://doi.org/10.1145/3715754 | University of Illinois Urbana-Champaign | E51 | Venue, DOI and authors from publisher DOI metadata (Crossref, 10.1145/3715754); author list identical to arXiv. Published title: "Demystifying LLM-Based Software Engineering Agents". |
| Xiao2026 | A | [Xiao et al., FSE 2026] | Yuan-An Xiao, Pengfei Gao, Chao Peng, and Yingfei Xiong. 2026. Reducing Cost of LLM Agents with Trajectory Reduction. In Proceedings of the ACM on Software Engineering 3, FSE (FSE 2026). Also arXiv:2509.23586. https://doi.org/10.1145/3797084 | Peking University; ByteDance | none; cited in §2.2, §3.5, §4.1, §5.4, App. A | Venue, DOI and authors from publisher DOI metadata (Crossref, 10.1145/3797084); author list identical to arXiv. Also on the FSE 2026 research-papers track page (conf.researchr.org). |
| Xie2024 | A | [Xie et al., NeurIPS 2024] | Tianbao Xie, Danyang Zhang, Jixuan Chen, Xiaochuan Li, Siheng Zhao, Ruisheng Cao, Jing Hua Toh, Zhoujun Cheng, Dongchan Shin, Fangyu Lei, Yitao Liu, Yiheng Xu, Shuyan Zhou, Silvio Savarese, Caiming Xiong, Victor Zhong, and Tao Yu. 2024. OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments. In Advances in Neural Information Processing Systems 37 (NeurIPS 2024), Datasets and Benchmarks Track. Also arXiv:2404.07972. https://neurips.cc/virtual/2024/poster/97468 | The University of Hong Kong; CMU; Salesforce Research; University of Waterloo | D33, D46, D47, D83, D95, D104, D116, D117, D119, E3, E5, E6, E7, E12, E22, E24, E39, E91, E94, E97, E111, E114, E115, E116 | Venue and authors from the official NeurIPS page. Venue author list differs from arXiv (17 vs 17 names or order); venue list used. DOI 10.52202/079017-1650 |
| Xu2025 | A | [Xu et al., NeurIPS 2025] | Frank (Fangzheng) Xu, Yufan Song, Boxuan Li, Yuxuan Tang, Kritanjali Jain, Mengxue Bao, Zora Wang, Xuhui Zhou, Zhitong Guo, Murong Cao, et al. (21 authors in total). 2025. TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks. In Advances in Neural Information Processing Systems 38 (NeurIPS 2025), Datasets and Benchmarks Track. Also arXiv:2412.14161. https://neurips.cc/virtual/2025/poster/121705 | Carnegie Mellon University; Duke University | D17, D37, E10 | Venue and authors from the official NeurIPS page. DOI 10.52202/085713-0315 |
| Xu2026c | A | [Xu et al., ACL 2026] | Hanwen Xu, Xuyao Huang, Yuzhe Liu, and Zhijie Deng. 2026. TPS-Bench: Evaluating AI Agents’ Tool Planning & Scheduling Abilities in Compounding Tasks. In Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers) (ACL 2026). https://aclanthology.org/2026.acl-long.1614/ |  | none; cited in §2.2, §3.4, §3.12, App. A | Authors, venue and DOI 10.18653/v1/2026.acl-long.1614 from the ACL Anthology page. |
| Xue2025 | A | [Xue et al., COLM 2025] | Tianci Xue, Weijian Qi, Tianneng Shi, Chan Hee Song, Boyu Gou, Dawn Song, Huan Sun, and Yu Su. 2025. An Illusion of Progress? Assessing the Current State of Web Agents. In Second Conference on Language Modeling (COLM 2025). Also arXiv:2504.01382. https://openreview.net/forum?id=6jZi4HSs6o | The Ohio State University; UC Berkeley | D133, E13, E36, E37, E43, E46, E90, E199 | Venue confirmed on the official page; authors from arXiv. On colmweb.org/2025/AcceptedPapers.html with the same 8 authors. |
| Yang2024 | A | [Yang et al., NeurIPS 2024] | John Yang, Carlos Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, and Ofir Press. 2024. SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering. In Advances in Neural Information Processing Systems 37 (NeurIPS 2024). Also arXiv:2405.15793. https://neurips.cc/virtual/2024/poster/93753 | Princeton University | D14, D61, E51 | Venue and authors from the official NeurIPS page. DOI 10.52202/079017-1601 |
| Yang2025 | A | [Yang et al., ICLR 2025] | Ke Yang, Yao Liu, Sapana Chaudhary, Rasool Fakoor, Pratik A Chaudhari, George Karypis, and Huzefa Rangwala. 2025. AgentOccam: A Simple Yet Strong Baseline for LLM-Based Web Agents. In The Thirteenth International Conference on Learning Representations (ICLR 2025). Also arXiv:2410.13825. https://iclr.cc/virtual/2025/poster/28353 | University of Illinois Urbana-Champaign; Amazon | E17 | Venue and authors from the official ICLR page. |
| Yao2025a | A | [Yao et al., EuroSys 2025] | Jiayi Yao, Hanchen Li, Yuhan Liu, Siddhant Ray, Yihua Cheng, Qizheng Zhang, Kuntai Du, Shan Lu, and Junchen Jiang. 2025. CacheBlend: Fast Large Language Model Serving for RAG with Cached Knowledge Fusion. In Proceedings of the Twentieth European Conference on Computer Systems (EuroSys 2025). Also arXiv:2405.16444. https://doi.org/10.1145/3689031.3696098 | University of Chicago; Microsoft Research; Stanford University; CUHK-Shenzhen | E179 | Venue, DOI and authors from publisher DOI metadata (Crossref, 10.1145/3689031.3696098); author list identical to arXiv. An extended version also appears in ACM TOCS (DOI 10.1145/3790254, 2026). |
| Yao2025b | A | [Yao et al., ICLR 2025] | Shunyu Yao, Noah Shinn, Pedram Razavi, and Karthik Narasimhan. 2025. τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains. In The Thirteenth International Conference on Learning Representations (ICLR 2025). Also arXiv:2406.12045. https://iclr.cc/virtual/2025/poster/28170 | Sierra | D27, E54, E114, E115, E116, E119, E120 | Venue and authors from the official ICLR page. |
| Ye2025 | A | [Ye et al., NeurIPS 2025] | Hancheng Ye, Zhengqi Gao, Mingyuan Ma, Qinsi Wang, Yuzhe Fu, Ming-Yu Chung, Yueqian Lin, Zhijian Liu, Jianyi Zhang, Danyang Zhuo, and Yiran Chen. 2025. KVCOMM: Online Cross-context KV-cache Communication for Efficient LLM-based Multi-agent Systems. In Advances in Neural Information Processing Systems 38 (NeurIPS 2025). Also arXiv:2510.12872. https://neurips.cc/virtual/2025/poster/115164 | Duke University; MIT; NVIDIA | D94, D127 | Venue and authors from the official NeurIPS page. DOI 10.52202/085713-0605 |
| Ye2026 | A | [Ye et al., ICLR 2026] | Naimeng Ye, Arnav Ahuja, Georgios Liargkovas, Yunan Lu, Kostis Kaffes, and Tianyi Peng. 2026. Speculative Actions: A Lossless Framework for Faster AI Agents. In The Fourteenth International Conference on Learning Representations (ICLR 2026), Oral. Also arXiv:2510.04371, titled "Speculative Actions: A Lossless Framework for Faster Agentic Systems". https://iclr.cc/virtual/2026/oral/10009727 | Columbia University | D23, D51, D90, D103, E126 | Venue and authors from the official ICLR page. ICLR title: "Speculative Actions: A Lossless Framework for Faster AI Agents" (arXiv: "...Faster Agentic Systems"). Poster page 10009726. |
| Yehudai2026 | A | [Yehudai et al., Findings ACL 2026] | Asaf Yehudai, Lilach Eden, Alan Li, Guy Uziel, Yilun Zhao, Roy Bar-Haim, Arman Cohan, and Michal Shmueli-Scheuer. 2026. A Survey on Evaluation of LLM-based Agents. In Findings of the Association for Computational Linguistics: ACL 2026. https://aclanthology.org/2026.findings-acl.1330/ |  | none; cited in §3.8, §3.11, App. A | Authors, venue and DOI 10.18653/v1/2026.findings-acl.1330 from the ACL Anthology page. |
| Zhang2025 | A | [Zhang et al., NeurIPS 2025] | Qizheng Zhang, Michael Wornow, and Kunle Olukotun. 2025. Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents. In Advances in Neural Information Processing Systems 38 (NeurIPS 2025). Also arXiv:2506.14852. https://neurips.cc/virtual/2025/poster/116166 | Stanford University | D10 | Venue and authors from the official NeurIPS page. Venue author list differs from arXiv (3 vs 4 names or order); venue list used. DOI 10.52202/085713-3451 |
| Zhang2026c | A | [Zhang et al., Findings ACL 2026] | Li Zhang, Longxi Gao, and Mengwei Xu. 2026. Does Chain-of-Thought Reasoning Help Mobile GUI Agents? An Empirical Study. In Findings of the Association for Computational Linguistics: ACL 2026. https://aclanthology.org/2026.findings-acl.392/ |  | none; cited in §3.7, App. A | Authors, venue and DOI 10.18653/v1/2026.findings-acl.392 from the ACL Anthology page. |
| Zhang2026d | A | [ZHANG et al., ICML 2026] | ZHIXIANG ZHANG, Zesen Liu, Yuchong Xie, Quanfeng Huang, and Dongdong She. 2026. From Similarity to Vulnerability: Key Collision Attack on LLM Semantic Caching. In Proceedings of the 43rd International Conference on Machine Learning (ICML 2026). Also arXiv:2601.23088. https://icml.cc/virtual/2026/poster/65663 | HKUST; Fudan University | none; cited in §3.9, §3.12, §8.2, App. A | Venue and authors from the official ICML page. |
| Zhang2026f | A | [Zhang et al., AAAI 2026] | Jiayuan Zhang, Kaiquan Chen, Zhihao Lu, Enshen Zhou, Qian Yu, and Jing Zhang. 2026. Prune4Web: DOM Tree Pruning Programming for Web Agent. In Proceedings of the AAAI Conference on Artificial Intelligence 40(41) (AAAI 2026). Also arXiv:2511.21398. https://ojs.aaai.org/index.php/AAAI/article/view/40772 | Beihang University | none; cited in §2.2, §3.5, §3.12, §5.8, §8.2, App. A | Venue, DOI and authors from publisher DOI metadata (Crossref, 10.1609/aaai.v40i41.40772); author list identical to arXiv. DOI 10.1609/aaai.v40i41.40772 |
| Zhang2026h | A | [Zhang et al., TMLR 2026] | Chaoyun Zhang, He Huang, Chiming Ni, Jian Mu, Si Qin, Shilin He, Lu Wang, Fangkai Yang, Pu Zhao, Chao Du, et al. (21 authors in total). 2026. UFO2: The Desktop AgentOS. In Transactions on Machine Learning Research (TMLR). Also arXiv:2504.14603. https://openreview.net/forum?id=iAuZVWCduc | Microsoft; Peking University; Nanjing University; ZJU-UIUC Institute | D46, E94 | Venue confirmed on the official page; authors from arXiv. Listed on jmlr.org/tmlr/papers (year of acceptance not shown on the list page; OpenReview not readable). Authors from arXiv. |
| Zheng2024 | A | [Zheng et al., NeurIPS 2024] | Lianmin Zheng, Liangsheng Yin, Zhiqiang Xie, Chuyue (Livia) Sun, Jeff Huang, Cody Hao Yu, Shiyi Cao, Christos Kozyrakis, Ion Stoica, Joseph Gonzalez, Clark Barrett, and Ying Sheng. 2024. SGLang: Efficient Execution of Structured Language Model Programs. In Advances in Neural Information Processing Systems 37 (NeurIPS 2024). Also arXiv:2312.07104. https://neurips.cc/virtual/2024/poster/94872 | Stanford University; UC Berkeley; Shanghai Jiao Tong University; Texas A&M University | E22, E173, E180, E182, E183, E184, E186, E189 | Venue and authors from the official NeurIPS page. DOI 10.52202/079017-2000 |
| Zhou2024 | A | [Zhou et al., ICLR 2024] | Shuyan Zhou, Frank F Xu, Hao Zhu, Xuhui Zhou, Robert Lo, Abishek Sridhar, Xianyi Cheng, Tianyue Ou, Yonatan Bisk, Daniel Fried, Uri Alon, and Graham Neubig. 2024. WebArena: A Realistic Web Environment for Building Autonomous Agents. In The Twelfth International Conference on Learning Representations (ICLR 2024). Also arXiv:2307.13854. https://iclr.cc/virtual/2024/poster/17826 | Carnegie Mellon University | D33, D45, D48, D49, D58, D87, D104, D116, D117, D119, E11, E12, E16, E18, E26, E39, E44, E98, E114, E115, E116, E133, E185 | Venue and authors from the official ICLR page. |
| Zhou2025 | A | [Zhou et al., NeurIPS 2025] | Yuqi Zhou, Sunhao Dai, Shuai Wang, Kaiwen Zhou, Qinglin Jia, and Jun Xu. 2025. GUI-G1: Understanding R1-Zero-Like Training for Visual Grounding in GUI Agents. In Advances in Neural Information Processing Systems 38 (NeurIPS 2025). Also arXiv:2505.15810. https://neurips.cc/virtual/2025/poster/120227 | Renmin University of China; Huawei Noah’s Ark Lab | none; cited in §2.2, §3.7, §3.10, App. A | Venue and authors from the official NeurIPS page. DOI 10.52202/085713-3201 |
| Zhu2025 | A | [Zhu et al., NeurIPS 2025] | Yuxuan Zhu, Tengjun Jin, Yada Pruksachatkun, Andy Zhang, Shu Liu, Sasha Cui, Sayash Kapoor, Shayne Longpre, Kevin Meng, Rebecca Weiss, et al. (26 authors in total). 2025. Establishing Best Practices in Building Rigorous Agentic Benchmarks. In Advances in Neural Information Processing Systems 38 (NeurIPS 2025), Datasets and Benchmarks Track. Also arXiv:2507.02825, titled "Establishing Best Practices for Building Rigorous Agentic Benchmarks". https://neurips.cc/virtual/2025/poster/121769 | UIUC; Stanford; UC Berkeley; Princeton; MIT; Yale; Oxford; UK AISI; Amazon; others | none; cited in §3.8, §4.1, §4.3, App. A | Venue and authors from the official NeurIPS page. Venue author list differs from arXiv (26 vs 25 names or order); venue list used. NeurIPS title: "Establishing Best Practices in Building Rigorous Agentic Benchmarks"; DOI 10.52202/085713-5547. |
| Anthropic2026a | B | [Anthropic, 2026] | Anthropic. 2026. Fast mode (research preview) — Claude Platform Docs. Official documentation. https://platform.claude.com/docs/en/build-with-claude/fast-mode (accessed 27 Sep 2026) | Anthropic | D137, E76, E190 | Page reachable and title read on 27 Sep 2026. |
| Anthropic2026b | B | [Anthropic, 2026] | Anthropic. 2026. Pricing — Claude Platform Docs. Official documentation. https://platform.claude.com/docs/en/about-claude/pricing (accessed 27 Sep 2026) | Anthropic | D22, E86 | Page reachable and title read on 27 Sep 2026. |
| Anthropic2026c | B | [Anthropic, 2026] | Anthropic. 2026. Prompt caching — Claude Platform Docs. Official documentation. https://platform.claude.com/docs/en/build-with-claude/prompt-caching (accessed 27 Sep 2026) | Anthropic | E84 | Page reachable and title read on 27 Sep 2026. |
| Anthropic2026d | B | [Anthropic, 2026] | Anthropic. 2026. Effort — Claude Platform Docs. Official documentation. https://platform.claude.com/docs/en/build-with-claude/effort (accessed 27 Sep 2026) | Anthropic | E88 | Page reachable and title read on 27 Sep 2026. |
| Anthropic2026e | B | [Anthropic, 2026] | Anthropic. 2026. Mid-conversation system messages and tool changes — Claude Platform Docs. Official documentation. https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages (accessed 27 Sep 2026) | Anthropic | D77, E83 | Page reachable and title read on 27 Sep 2026. |
| Anthropic2026f | B | [Anthropic, 2026] | Anthropic. 2026. Service tiers — Claude Platform Docs. Official documentation. https://platform.claude.com/docs/en/api/service-tiers (accessed 27 Sep 2026) | Anthropic | D137, E191 | Page reachable and title read on 27 Sep 2026. |
| Anthropic2026g | B | [Anthropic, 2026] | Anthropic. 2026. Best practices for computer and browser use with Claude. Official documentation. https://claude.com/blog/best-practices-for-computer-and-browser-use-with-claude (accessed 27 Sep 2026) | Anthropic | E31, E81 | Page reachable and title read on 27 Sep 2026. |
| Anthropic2026h | B | [Anthropic, 2026] | Anthropic. 2026. Release notes — Claude Help Center. Official documentation. https://support.claude.com/en/articles/12138966-release-notes (accessed 27 Sep 2026) | Anthropic | D136, E80, E210 | Page reachable and title read on 27 Sep 2026. |
| Anthropic2026i | B | [Anthropic, 2026] | Anthropic. 2026. Get started with Claude in Chrome — Claude Help Center. Official documentation. https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome (accessed 27 Sep 2026) | Anthropic | D136, E38, E80, E210 | Page reachable and title read on 27 Sep 2026. |
| AutomationAnywhere2026a | B | [Automation Anywhere, 2026] | Automation Anywhere. 2026. Generative AI-based fallback — Automation 360 documentation. Official documentation. https://docs.automationanywhere.com/r/automation-360/generative-ai-based-fallback (accessed 27 Sep 2026) | Automation Anywhere | D115, D139, E149, E150, E160 | Page reachable and title read on 27 Sep 2026. |
| AutomationAnywhere2026b | B | [Automation Anywhere, 2026] | Automation Anywhere. 2026. Generative Recorder overview — Automation 360 documentation. Official documentation. https://docs.automationanywhere.com/r/automation-360/gr-overview (accessed 27 Sep 2026) | Automation Anywhere | E149 | Page reachable and title read on 27 Sep 2026. |
| Browserbase2026a | B | [Browserbase, 2026] | Browserbase. 2026. Caching Actions — Stagehand documentation. Official documentation. https://docs.stagehand.dev/v3/best-practices/caching (accessed 27 Sep 2026) | Browserbase | D113, D114, D115, D135, D138, D139, E87, E153, E154, E203 | Page reachable and title read on 27 Sep 2026. |
| Browserbase2026b | B | [Browserbase, 2026] | Browserbase. 2026. Browserbase Pricing. Official documentation. https://www.browserbase.com/pricing (accessed 27 Sep 2026) | Browserbase | E155 | Page reachable and title read on 27 Sep 2026. |
| Browserbase2026c | B | [Browserbase, 2026] | Browserbase. 2026. Changelog — Browserbase. Official documentation. https://www.browserbase.com/changelog (accessed 27 Sep 2026) | Browserbase | D135, E87, E203 | Page reachable and title read on 27 Sep 2026. |
| BrowserUse2025 | B | [Browser Use, 2025] | Browser Use. 2025. workflow-use (GitHub repository README). Official documentation. https://github.com/browser-use/workflow-use (accessed 27 Sep 2026) | Browser Use | E157 | Page reachable and title read on 27 Sep 2026. |
| BrowserUse2026a | B | [Browser Use, 2026] | Browser Use. 2026. Rerunnable scripts — Browser Use Cloud documentation. Official documentation. https://docs.browser-use.com/cloud/agent/cache-script (accessed 27 Sep 2026) | Browser Use | E156 | Page reachable and title read on 27 Sep 2026. |
| BrowserUse2026b | B | [Browser Use, 2026] | Browser Use. 2026. Skills — Browser Use documentation. Official documentation. https://docs.browser-use.com/concepts/skills (accessed 27 Sep 2026) | Browser Use | E156 | Page reachable and title read on 27 Sep 2026. |
| Google2026a | B | [Google, 2026] | Google. 2026. Computer use — Gemini API docs. Official documentation. https://ai.google.dev/gemini-api/docs/computer-use (accessed 27 Sep 2026) | Google | D74, D134, E79, E198 | Page reachable and title read on 27 Sep 2026. |
| Google2026b | B | [Google, 2026] | Google. 2026. Gemini 3.5 Flash-Lite — Gemini API docs. Official documentation. https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite (accessed 27 Sep 2026) | Google | D74, D75, D134, E79 | Page reachable and title read on 27 Sep 2026. |
| Google2026c | B | [Google, 2026] | Google. 2026. Gemini Developer API pricing. Official documentation. https://ai.google.dev/gemini-api/docs/pricing (accessed 27 Sep 2026) | Google | D137, E197, E198 | Page reachable and title read on 27 Sep 2026. |
| Google2026d | B | [Google, 2026] | Google. 2026. Priority inference — Gemini API docs. Official documentation. https://ai.google.dev/gemini-api/docs/priority-inference (accessed 27 Sep 2026) | Google | D137, E197 | Page reachable and title read on 27 Sep 2026. |
| Hadfield2025 | B | [Anthropic, 2025] | Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, and Daniel Ford. 2025. How we built our multi-agent research system. Anthropic Engineering blog, 13 June 2025. https://www.anthropic.com/engineering/multi-agent-research-system (accessed 27 Sep 2026) |  | E60 | Byline and date read on the page (27 Sep 2026). |
| Hyperbrowser2026 | B | [Hyperbrowser, 2026] | Hyperbrowser. 2026. Action Caching — HyperAgent documentation. Official documentation. https://www.hyperbrowser.ai/docs/hyperagent/action-cache (accessed 27 Sep 2026) | Hyperbrowser | D110, D112, D115, D139, E139, E158, E160 | Page reachable and title read on 27 Sep 2026. |
| Johnston2026 | B | [OpenAI, 2026] | Drew Johnston, David Holtz, Alex Martin Richmond, Christopher Ong, Prasanna Tambe, and Aaron Chatterji. 2026. The Shift to Agentic AI: Evidence from Codex. OpenAI research report (PDF), June 2026. https://cdn.openai.com/pdf/5d1e1489-21c0-43e4-9d42-f87efdbf0082/the-shift-to-agentic-ai-evidence-from-codex.pdf (accessed 27 Sep 2026) | OpenAI; Columbia Business School; Wharton; Duke Fuqua | E61 | Authors read from PDF page 1; PDF creation date 24 Jun 2026 (dossier E61 gives 25 Jun 2026). |
| Lu2026 | B | [Microsoft Research, 2026] | Yadong Lu, Lingrui Xu, Chao Huang, and Ahmed Awadallah. 2026. Webwright: A Terminal Is All You Need For Web Agents. Microsoft Research article, 4 May 2026. https://www.microsoft.com/en-us/research/articles/webwright-a-terminal-is-all-you-need-for-web-agents/ (accessed 27 Sep 2026) | Microsoft Research; The University of Hong Kong | E46 | Byline and date read on the page. |
| Microsoft2026a | B | [Microsoft, 2026] | Microsoft. 2026. Enable priority processing for Microsoft Foundry Models — Microsoft Learn. Official documentation. https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/priority-processing (accessed 27 Sep 2026) | Microsoft | D131, D137, D139, E76, E78, E190, E196, E209 | Page reachable and title read on 27 Sep 2026. |
| Microsoft2026b | B | [Microsoft, 2026] | Microsoft. 2026. Self-healing (preview) — Power Automate, Microsoft Learn. Official documentation. https://learn.microsoft.com/en-us/power-automate/desktop-flows/self-healing (accessed 27 Sep 2026) | Microsoft | D113, E151 | Page reachable and title read on 27 Sep 2026. |
| Microsoft2026c | B | [Microsoft, 2026] | Microsoft. 2026. Set fallback mechanism for UI elements — Power Automate, Microsoft Learn. Official documentation. https://learn.microsoft.com/en-us/power-automate/desktop-flows/ui-elements-fallback-mechanism (accessed 27 Sep 2026) | Microsoft | E152 | Page reachable and title read on 27 Sep 2026. |
| Microsoft2026d | B | [Microsoft, 2026] | Microsoft. 2026. FAQ for Repair with Copilot at runtime in Power Automate desktop — Microsoft Learn. Official documentation. https://learn.microsoft.com/en-us/power-automate/faqs-repair-copilot (accessed 27 Sep 2026) | Microsoft | E152 | Page reachable and title read on 27 Sep 2026. |
| OpenAI2025 | B | [OpenAI, 2025] | OpenAI. 2025. Computer-Using Agent. OpenAI research page. https://openai.com/index/computer-using-agent/ (accessed 27 Sep 2026) |  | D33, E39 | UNVERIFIED on the page: openai.com returns 403; title and date (23 Jan 2025) from dossier D33, which quotes the page. |
| OpenAI2026a | B | [OpenAI, 2026] | OpenAI. 2026. Fast mode (priority processing) — OpenAI API docs. Official documentation. https://developers.openai.com/api/docs/guides/priority-processing (accessed 27 Sep 2026) | OpenAI | D132, D137, E77, E192 | developers.openai.com page reachable (HTTP 200, 27 Sep 2026); title as recorded in the dossier. |
| OpenAI2026b | B | [OpenAI, 2026] | OpenAI. 2026. Flex processing — OpenAI API docs. Official documentation. https://developers.openai.com/api/docs/guides/flex-processing (accessed 27 Sep 2026) | OpenAI | D137, E77, E193 | developers.openai.com page reachable (HTTP 200, 27 Sep 2026); title as recorded in the dossier. |
| OpenAI2026c | B | [OpenAI, 2026] | OpenAI. 2026. Pricing — OpenAI API docs. Official documentation. https://developers.openai.com/api/docs/pricing (accessed 27 Sep 2026) | OpenAI | D22, D132, D137, E77, E192 | developers.openai.com page reachable (HTTP 200, 27 Sep 2026); title as recorded in the dossier. |
| OpenAI2026d | B | [OpenAI, 2026] | OpenAI. 2026. Changelog — OpenAI API docs. Official documentation. https://developers.openai.com/api/docs/changelog (accessed 27 Sep 2026) | OpenAI | D132, D137, E77, E192, E194, E206 | developers.openai.com page reachable (HTTP 200, 27 Sep 2026); title as recorded in the dossier. |
| OpenAI2026e | B | [OpenAI, 2026] | OpenAI. 2026. Prompt caching — OpenAI API docs. Official documentation. https://developers.openai.com/api/docs/guides/prompt-caching (accessed 27 Sep 2026) | OpenAI | E112 | developers.openai.com page reachable (HTTP 200, 27 Sep 2026); title as recorded in the dossier. |
| OpenAI2026f | B | [OpenAI, 2026] | OpenAI. 2026. Prompt Caching 201 — OpenAI Cookbook. Official documentation. https://developers.openai.com/cookbook/examples/prompt_caching_201 (accessed 27 Sep 2026) | OpenAI | E84 | developers.openai.com page reachable (HTTP 200, 27 Sep 2026); title as recorded in the dossier. |
| OpenAI2026g | B | [OpenAI, 2026] | OpenAI. 2026. ChatGPT agent — OpenAI Help Center. Official documentation. https://help.openai.com/en/articles/11752874-chatgpt-agent (accessed 27 Sep 2026) | OpenAI | E39 | UNVERIFIED on the page: help.openai.com returns 403 to automated fetch; title from dossier E39. |
| OpenAI2026h | B | [OpenAI, 2026] | OpenAI. 2026. ChatGPT agent release notes — OpenAI Help Center. Official documentation. https://help.openai.com/en/articles/11794368-chatgpt-agent-release-notes (accessed 27 Sep 2026) | OpenAI | D29, D76, E39 | UNVERIFIED on the page: help.openai.com returns 403 to automated fetch; title from dossier E39. |
| OpenRouter2026a | B | [OpenRouter, 2026] | OpenRouter. 2026. DeepSeek V4 Is Earning Agentic Token Share. OpenRouter Insights blog, 30 June 2026. https://openrouter.ai/blog/insights/deepseek-v4-adoption/ (accessed 27 Sep 2026) |  | D18, D19, D21, D70, D72, E57 | Title and date read on the page. |
| OpenRouter2026b | B | [OpenRouter, 2026] | OpenRouter. 2026. GPT 5.6 Discounts & Jevons Paradox. OpenRouter Insights blog, 25 August 2026. https://openrouter.ai/blog/insights/gpt-5-6-discounts-jevons-paradox/ (accessed 27 Sep 2026) |  | E211 | Title and date read on the page. |
| OpenRouter2026c | B | [OpenRouter, 2026] | OpenRouter. 2026. OpenRouter model and pricing listings. openrouter.ai. https://openrouter.ai/ (accessed 27 Sep 2026) |  | E90 | Site reachable; used for a price assumption (E90). |
| Skyvern2026a | B | [Skyvern, 2026] | Skyvern. 2026. Code Caching — Skyvern documentation. Official documentation. https://www.skyvern.com/docs/developers/features/code-caching (accessed 27 Sep 2026) | Skyvern | D115, D139, E158, E160 | Page reachable and title read on 27 Sep 2026. |
| Skyvern2026b | B | [Skyvern, 2026] | Skyvern. 2026. Cost Control — Skyvern documentation. Official documentation. https://skyvern.mintlify.app/developers/optimization/cost-control (accessed 27 Sep 2026) | Skyvern | E158 | Page reachable and title read on 27 Sep 2026. |
| UiPath2026a | B | [UiPath, 2026] | UiPath. 2026. What is Healing Agent? — UiPath Agents documentation. Official documentation. https://docs.uipath.com/agents/automation-cloud/latest/user-guide-ha/what-is-healing-agent (accessed 27 Sep 2026) | UiPath | D113, D139, E146, E147, E148, E160 | Page reachable and title read on 27 Sep 2026. |
| UiPath2026b | B | [UiPath, 2026] | UiPath. 2026. Licensing — UiPath Healing Agent documentation. Official documentation. https://docs.uipath.com/agents/automation-cloud/latest/user-guide-ha/licensing (accessed 27 Sep 2026) | UiPath | E147 | Page reachable and title read on 27 Sep 2026. |
| UiPath2026c | B | [UiPath, 2026] | UiPath. 2026. ScreenPlay — UiPath UI Automation activities documentation. Official documentation. https://docs.uipath.com/activities/other/latest/ui-automation/screenplay (accessed 27 Sep 2026) | UiPath | E148 | Page reachable and title read on 27 Sep 2026. |
| Gartner2025 | C | [Gartner, 2025] | Gartner. 2025. Gartner Predicts Over 40% of Agentic AI Projects Will Be Canceled by End of 2027. Gartner, 25 June 2025. https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027 (accessed 27 Sep 2026) | Gartner | E72 | gartner.com blocks automated fetch (bot wall); title and date from the URL and dossier E72. |
| Gartner2026a | C | [Gartner, 2026] | Gartner. 2026. Gartner Predicts That by 2030, Performing Inference on an LLM With 1 Trillion Parameters Will Cost GenAI Providers Over 90% Less Than in 2025. Gartner, 25 March 2026. https://www.gartner.com/en/newsroom/press-releases/2026-03-25-gartner-predicts-that-by-2030-performing-inference-on-an-llm-with-1-trillion-parameters-will-cost-genai-providers-over-90-percent-less-than-in-2025 (accessed 27 Sep 2026) | Gartner | D20, D68, E62 | gartner.com blocks automated fetch; title and date from the URL and dossier E62 [V]. |
| Gartner2026b | C | [Gartner, 2026] | Gartner. 2026. Gartner Says Artificial Intelligence Projects in Infrastructure and Operations Stall Ahead of Meaningful ROI Returns. Gartner, 7 April 2026. https://www.gartner.com/en/newsroom/press-releases/2026-04-07-gartner-says-artificial-intelligence-projects-in-infrastructure-and-operations-stall-ahead-of-meaningful-roi-returns (accessed 27 Sep 2026) | Gartner | D69, E73 | gartner.com blocks automated fetch; title and date from the URL and dossier E73 [V]. |
| Gartner2026c | C | [Gartner, 2026] | Gartner. 2026. Gartner Predicts AI Inference Costs per Agentic Workflow Will Increase More Than Fivefold Through 2028. Gartner, 17 August 2026. https://www.gartner.com/en/newsroom/press-releases/2026-08-17-gartner-predicts-ai-inference-costs-per-agentic-workflow-will-increase-more-than-fivefold-through-2028 (accessed 27 Sep 2026) | Gartner | E55 | gartner.com blocks automated fetch; title and date from the URL and dossier E55 [V]. |
| HUMANSecurity2026 | C | [HUMAN Security, 2026] | HUMAN Security. 2026. 2026 State of AI Traffic & Cyberthreat Benchmark Report. HUMAN Security, 26 March 2026. https://www.humansecurity.com/learn/resources/2026-state-of-ai-traffic-cyberthreat-benchmarks/ (accessed 27 Sep 2026) | HUMAN Security | E65 | humansecurity.com returns 403 to automated fetch; title and date from dossier E65 [V, vendor]. |
| LangChain2026 | C | [LangChain, 2026] | LangChain. 2026. State of Agent Engineering. LangChain, page byline 12 June 2026. https://www.langchain.com/state-of-agent-engineering (accessed 27 Sep 2026) | LangChain | D24, E68 | Page reachable (27 Sep 2026); byline date per dossier E68. |
| MenloVentures2025 | C | [Menlo Ventures, 2025] | Menlo Ventures. 2025. 2025: The State of Generative AI in the Enterprise. Menlo Ventures, 9 December 2025. https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise/ (accessed 27 Sep 2026) | Menlo Ventures | E66 | Title and date read on the page. |
| Temporal2026 | C | [Temporal, 2026] | Temporal. 2026. The State of Development 2026. Temporal, 25 August 2026. https://temporal.io/reports/state-of-development-2026 (accessed 27 Sep 2026) | Temporal | D78, E70 | Title read on the page; date per dossier E70. |
| Abuzakuk2026 | D | [Abuzakuk et al., arXiv Jan 2026 · EPFL] | Sami Abuzakuk, Anne-Marie Kermarrec, Rishi Sharma, Rasmus Moorits Veski, and Martijn de Vos. 2026. Optimizing Agentic Workflows using Meta-tools. arXiv preprint arXiv:2601.22037 (January 2026). https://arxiv.org/abs/2601.22037 | EPFL | D45, D86, E93 | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. |
| Aubakirova2026 | D | [Aubakirova et al., arXiv Jan 2026 · OpenRouter Inc.] | Malika Aubakirova, Alex Atallah, Chris Clark, Justin Summerville, and Anjney Midha. 2026. State of AI: An Empirical 100 Trillion Token Study with OpenRouter. arXiv preprint arXiv:2601.10088 (January 2026). https://arxiv.org/abs/2601.10088 | OpenRouter Inc.; a16z (Andreessen Horowitz) | E56, E74 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Awadallah2025 | D | [Awadallah et al., arXiv Nov 2025 · Microsoft (no affiliation line printed] | Ahmed Awadallah, Yash Lara, Raghav Magazine, Hussein Mozannar, Akshay Nambi, Yash Pandya, Aravind Rajeswaran, Corby Rosset, Alexey Taymanov, Vibhav Vineet, Spencer Whitehead, and Andrew Zhao. 2025. Fara-7B: An Efficient Agentic Model for Computer Use. arXiv preprint arXiv:2511.19663 (November 2025). https://arxiv.org/abs/2511.19663 | Microsoft (no affiliation line printed; Microsoft Research AI Frontiers report) | D54, D91, E90 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Bai2026a | D | [Bai et al., arXiv Sep 2026 · Fudan University] | Bizhe Bai, Jiakang Yuan, Hongming Wu, Xinyue Wang, Jie Ren, Siyao Chen, Yuchen Ya, Fan Bai, Pai Peng, Huafeng Qin, and Tao Chen. 2026. Efficient GUI Agents: A Systems Survey of Observation, Memory, Action, and Runtime Optimization. arXiv preprint arXiv:2609.02309 (September 2026). https://arxiv.org/abs/2609.02309 | Fudan University; Shanghai Innovation Institute; Chongqing Technology and Business University | none; cited in §3.11, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. arXiv comment: accepted at an EMNLP 2026 workshop (non-archival; kept in D). |
| Bai2026b | D | [Bai et al., arXiv Jul 2026 · Tsinghua University] | Huajun Bai, Weiwei Lv, Huichuan Zheng, Youyou Lu, and Jiwu Shu. 2026. SPORK: Self-Speculative Forking to Accelerate Agentic LLM Inference. arXiv preprint arXiv:2607.03333 (July 2026). https://arxiv.org/abs/2607.03333 | Tsinghua University; Meituan | D103, D106, E128, E138 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Bian2025 | D | [Bian et al., arXiv Oct 2025 · UW-Madison] | Song Bian, Minghao Yan, Anand Jayarajan, Gennady Pekhimenko, and Shivaram Venkataraman. 2025. What Limits Agentic Systems Efficiency?. arXiv preprint arXiv:2510.16276 (October 2025). https://arxiv.org/abs/2510.16276 | UW-Madison; University of Toronto; NVIDIA | D98, E27 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Chang2026 | D | [Chang et al., arXiv Aug 2026 · HKUST] | Chaokun Chang, Yukun Zhou, Kaihua Fu, Dakai An, Tianyu Feng, Hanfeng Lu, Sheng Yao, Pu Guo, Yinghao Yu, Yizhou Shan, Bo Li, Binhang Yuan, and Wei Wang. 2026. From LLM Inference to Agentic Workloads: Characterization and Implications for Serving Systems. arXiv preprint arXiv:2608.15127 (August 2026). https://arxiv.org/abs/2608.15127 | HKUST; Alibaba Group; ByteDance | D95, D96, E28, E97, E98, E99 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Chen2023 | D | [Chen et al., arXiv Oct 2023 · System2 Research] | Baian Chen, Chang Shu, Ehsan Shareghi, Nigel Collier, Karthik Narasimhan, and Shunyu Yao. 2023. FireAct: Toward Language Agent Fine-tuning. arXiv preprint arXiv:2310.05915 (October 2023). https://arxiv.org/abs/2310.05915 | System2 Research; University of Cambridge; Monash University; Princeton University | none; cited in §2.2, §3.5, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Chen2026a | D | [Chen et al., arXiv Aug 2026 · Imperial College London] | Hao Mark Chen, Jinnan Guo, Wayne Luk, and Hongxiang Fan. 2026. AOSpec: Action and Observation Co-Speculation for Low-Latency Agent Serving. arXiv preprint arXiv:2608.00881 (August 2026). https://arxiv.org/abs/2608.00881 | Imperial College London | D103, E123 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Chen2026b | D | [Chen et al., arXiv Jun 2026 · Tsinghua University] | Zheng Chen, Hanqing Liu, Duling Xu, Dong Dong, Jialin Li, Bangzheng Pu, and Jidong Zhai. 2026. Cordon: Semantic Transactions for Tool-Using LLM Agents. arXiv preprint arXiv:2606.17573 (June 2026). https://arxiv.org/abs/2606.17573 | Tsinghua University; Shanghai Jiao Tong University; Renmin University; AetherHeart Tech | D105, E117, E118, E119, E120 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. HTML header names EuroSys 2027 (Rabat, April 2027); acceptance not confirmed on an official EuroSys page (dossier E117). |
| Chen2026c | D | [Chen et al., arXiv Apr 2026 · Shenzhen University] | Qijia Chen, Andrea Bellucci, Zhida Sun, and Giulio Jacucci. 2026. SkillDroid: Compile Once, Reuse Forever. arXiv preprint arXiv:2604.14872 (April 2026). https://arxiv.org/abs/2604.14872 | Shenzhen University; University of Helsinki; Universidad Carlos III de Madrid | none; cited in §2.2, §3.1, §3.12, §5.2, §5.3, §5.4, §5.5, §5.6, §5.8, §8.2, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Choi2026 | D | [Choi et al., arXiv Sep 2026 · Korea University] | Wonmi Choi, Minuk Park, Zhixiong Niu, Yongqiang Xiong, Chuck Yoo, and Gyeongsik Yang. 2026. Not All AI Agents Are Equal: Characterizing Resource and Performance Dynamics. arXiv preprint arXiv:2609.19947 (September 2026). https://arxiv.org/abs/2609.19947 | Korea University; Microsoft Research Asia | E102, E103, E104 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Chundru2026 | D | [Chundru, arXiv Apr 2026 · Selfotix] | Jagadeesh Chundru. 2026. Agentic Compilation: Mitigating the LLM Rerun Crisis for Minimized-Inference-Cost Web Automation. arXiv preprint arXiv:2604.09718 (April 2026). https://arxiv.org/abs/2604.09718 | Selfotix | D110, D113, E145 | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. |
| Conn2026 | D | [Conn, arXiv Sep 2026 · Conn Castle Studios] | Nicholas J. Conn. 2026. DeltaSelect: Affordable A/B Testing for Coding Agents. arXiv preprint arXiv:2609.19607 (September 2026). https://arxiv.org/abs/2609.19607 | Conn Castle Studios | none; cited in §3.8, §4.1, §5.8, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Cristescu2025 | D | [Cristescu et al., arXiv Nov 2025 · UiPath] | Horia Cristescu, Charles Park, Trong Canh Nguyen, Sergiu Talmacel, Alexandru-Gabriel Ilie, and Stefan Adam. 2025. UI-CUBE: Enterprise-Grade Computer Use Agent Benchmarking Beyond Task Accuracy to Operational Reliability. arXiv preprint arXiv:2511.17131 (November 2025). https://arxiv.org/abs/2511.17131 | UiPath | D116, E15 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Cuadron2025 | D | [Cuadron et al., arXiv Feb 2025 · UC Berkeley] | Alejandro Cuadron, Dacheng Li, Wenjie Ma, Xingyao Wang, Yichuan Wang, Siyuan Zhuang, Shu Liu, Luis Gaspar Schroeder, Tian Xia, Huanzhi Mao, Nicholas Thumiger, Aditya Desai, Ion Stoica, Ana Klimovic, Graham Neubig, and Joseph E. Gonzalez. 2025. The Danger of Overthinking: Examining the Reasoning-Action Dilemma in Agentic Tasks. arXiv preprint arXiv:2502.08235 (February 2025). https://arxiv.org/abs/2502.08235 | UC Berkeley; ETH Zurich; CMU; UIUC | none; cited in §2.2, §3.7, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Dihan2025 | D | [Dihan et al., arXiv Dec 2025 · BUET] | Mahir Labib Dihan, Tanzima Hashem, Mohammed Eunus Ali, and Md Rizwan Parvez. 2025. WebOperator: Action-Aware Tree Search for Autonomous Agents in Web Environment. arXiv preprint arXiv:2512.12692 (December 2025). https://arxiv.org/abs/2512.12692 | BUET; Monash University; QCRI | D104, E133 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. arXiv comment: "Under review at ICLR 2026"; not on the ICLR 2026 accepted list. |
| Dong2026a | D | [Dong et al., arXiv Sep 2026 · Georgia Tech] | Zihan Dong, Yuanzhe Liu, Zhiyuan Ma, Qishi Zhan, Dehan Kong, Guohao Li, and Kaixin Li. 2026. CADWorld: Computer-Use Benchmark for Long-Horizon Computer-Aided Design. arXiv preprint arXiv:2609.16251 (September 2026). https://arxiv.org/abs/2609.16251 | Georgia Tech; NUS; CAMEL-AI/Eigent.AI; others | D116, D119, D121, E162 | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. |
| Dong2026b | D | [Dong et al., arXiv May 2026 · Shanghai Jiao Tong University] | Yunpeng Dong, Jingkai He, Shiqi Liu, Yuze Hou, Dong Du, Zhonghu Xu, Si Yu, Baochuan Yang, Yubin Xia, and Haibo Chen. 2026. DeltaBox: Scaling Stateful AI Agents with Millisecond-Level Sandbox Checkpoint/Rollback. arXiv preprint arXiv:2605.22781 (May 2026). https://arxiv.org/abs/2605.22781 | Shanghai Jiao Tong University (IPADS); Huawei | D102, D126, D140, E122, E123, E177 | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. |
| Dong2026c | D | [Dong et al., arXiv Jul 2026 · Georgia Tech] | Zihan Dong, Rui Qian, Qishi Zhan, Dongshen Peng, Kaixin Li, and Yu Li. 2026. Why Are GUI Agents Correct but Late? Decode on the Decision-Time Critical Path, Tested with Pre-Compiled Policy Trees. arXiv preprint arXiv:2607.28399 (July 2026). https://arxiv.org/abs/2607.28399 | Georgia Tech; Fudan; Marquette; UNC Chapel Hill; NUS; Southeast University | D88, E95, E134 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Enomoto2026 | D | [Enomoto et al., arXiv May 2026 · NEC Corporation] | Masafumi Enomoto, Ryoma Obara, Haochen Zhang, and Masafumi Oyamada. 2026. Revisiting Observation Reduction for Web Agents: Comprehensive Evaluation with a Lightweight Framework. arXiv preprint arXiv:2605.29397 (May 2026). https://arxiv.org/abs/2605.29397 | NEC Corporation | none; cited in §2.2, §3.5, §3.12, §5.2, §5.3, §5.4, §5.8, §8.2, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Fareed2026 | D | [Fareed, arXiv Jun 2026 · AWS] | Faisal Fareed. 2026. Cost-Aware Speculative Execution for LLM-Agent Workflows: An Integrated Five-Dimension Method. arXiv preprint arXiv:2606.07846 (June 2026). https://arxiv.org/abs/2606.07846 | AWS | D106, D109, E131, E138 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Farzaneh2026 | D | [Farzaneh and Simeone, arXiv Jul 2026 · Northeastern University London] | Amirmohammad Farzaneh and Osvaldo Simeone. 2026. Think Short, Defer Smart, Act, and Repeat: Calibrated Reasoning and Uncertainty-Aware Deferral for Edge LLM Agents. arXiv preprint arXiv:2607.26865 (July 2026). https://arxiv.org/abs/2607.26865 | Northeastern University London | none; cited in §3.7, App. A | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. |
| Feng2025 | D | [Feng et al., arXiv May 2025 · Shanghai Jiao Tong University] | Erhu Feng, Wenbo Zhou, Zibin Liu, Le Chen, Yunpeng Dong, Cheng Zhang, Yisheng Zhao, Dong Du, Zhichao Hua, Yubin Xia, and Haibo Chen. 2025. Get Experience from Practice: LLM Agents with Record & Replay. arXiv preprint arXiv:2505.17716 (May 2025). https://arxiv.org/abs/2505.17716 | Shanghai Jiao Tong University (IPADS) | none; cited in §2.2, §3.2, §3.12, §8.2, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Feng2026 | D | [Feng et al., arXiv May 2026 · UC Berkeley] | Guangyu Feng, Huanzhi Mao, Prabal Dutta, and Joseph E. Gonzalez. 2026. Concurrency without Model Changes: Future-based Asynchronous Function Calling for LLMs. arXiv preprint arXiv:2605.15077 (May 2026). https://arxiv.org/abs/2605.15077 | UC Berkeley | none; cited in §2.2, §3.4, §3.10, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Gim2024 | D | [Gim et al., arXiv Dec 2024 · Yale University] | In Gim, Seung-seob Lee, and Lin Zhong. 2024. Asynchronous LLM Function Calling. arXiv preprint arXiv:2412.07017 (December 2024). https://arxiv.org/abs/2412.07017 | Yale University | none; cited in §2.2, §3.4, §3.10, §3.12, §4.1, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| GonzalezPumariega2026 | D | [Gonzalez-Pumariega et al., arXiv Apr 2026 · Simular (inferred from corresponding-author e-mail] | Gonzalo Gonzalez-Pumariega, Saaket Agashe, Jiachen Yang, Ang Li, and Xin Eric Wang. 2026. On the Reliability of Computer Use Agents. arXiv preprint arXiv:2604.17849 (April 2026). https://arxiv.org/abs/2604.17849 | Simular (inferred from corresponding-author e-mail; no affiliation printed) | none; cited in §3.8, §4.1, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Gu2026 | D | [Gu et al., arXiv May 2026 · Stanford University] | Zhuohan Gu, Qizheng Zhang, Omar Khattab, and Samuel Madden. 2026. PEEK: Context Map as an Orientation Cache for Long-Context LLM Agents. arXiv preprint arXiv:2605.19932 (May 2026). https://arxiv.org/abs/2605.19932 | Stanford University; MIT CSAIL | D125, E175 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Hajimiri2026 | D | [Hajimiri et al., arXiv Jun 2026 · ServiceNow AI Research] | Sina Hajimiri, Masih Aminbeidokhti, Jose Dolz, Ismail Ben Ayed, Issam H. Laradji, Spandana Gella, and Nicolas Gontier. 2026. Are Online Skill and Memory Modules Always Worth Their Tokens? A Budget-Constrained Study of Web Agents. arXiv preprint arXiv:2606.15017 (June 2026). https://arxiv.org/abs/2606.15017 | ServiceNow AI Research; ÉTS Montréal; UBC; McGill University | none; cited in §3.8, §4.1, App. A | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. arXiv comment: "Accepted to EMNLP 2026"; 2026.emnlp.org has no accepted-paper list yet (checked 27 Sep 2026). |
| He2026 | D | [He et al., arXiv Sep 2026 · Fudan University] | Fan He, Yan Li, and Xiaoyang Zeng. 2026. UNISON: A Co-Designed Near-Memory Scheduler of Session KV Residency for LLM Agents. arXiv preprint arXiv:2609.09643 (September 2026). https://arxiv.org/abs/2609.09643 | Fudan University | D127, D130, E181, E189 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Hu2026 | D | [Yunuo Hu et al., Preprints.org Aug 2026] | Yunuo Hu et al.. 2026. How to Make Tool-Using LLM Agents Efficient? A Survey. Preprints.org manuscript 202608.0365 (August 2026). https://www.preprints.org/manuscript/202608.0365 (accessed 27 Sep 2026) | not verified | none; cited in §3.11, App. A | UNVERIFIED: preprints.org returns 403 to automated fetch; title and first author taken from dossier §3.11 only. Not an arXiv preprint. |
| Huang2026a | D | [Huang et al., arXiv Aug 2026 · Johns Hopkins University] | Zixi Huang, Xiheng Wang, Andrew Wang, William Jurayj, Bernal Jiménez Gutiérrez, Daniel Khashabi, and Nicholas Andrews. 2026. Better, Faster, Stronger: Programmatic Skill Learning Best Reduces Agent Cost. arXiv preprint arXiv:2608.11338 (August 2026). https://arxiv.org/abs/2608.11338 | Johns Hopkins University | none; cited in §3.1, §3.9, §3.10, §5.2, §5.3, §5.4, §5.5, §5.6, §5.8, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Huang2026c | D | [Huang et al., arXiv May 2026 · HKUST] | Runxi Huang, Liyu Zhang, Shengzhong Liu, and Xiaomin Ouyang. 2026. MobileExplorer: Accelerating On-Device Inference for Mobile GUI Agents via Online Exploration. arXiv preprint arXiv:2605.26546 (May 2026). https://arxiv.org/abs/2605.26546 | HKUST; Shanghai Jiao Tong University | E96 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Huang2026d | D | [Huang et al., arXiv May 2026 · UC San Diego] | Yutong Huang, Vikranth Srivatsa, Alex Asch, Hansin Tushar Patwa, and Yiying Zhang. 2026. TClone: Low-Latency Forking of Live GUI Environments for Computer-Use Agents. arXiv preprint arXiv:2605.17320 (May 2026). https://arxiv.org/abs/2605.17320 | UC San Diego; GenseeAI | E121 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Iyamu2026 | D | [Iyamu, arXiv Aug 2026 · Independent researcher] | Nossa Iyamu. 2026. Activity Frames: Deterministic Screen-Activity Compilation for Agent Memory and Replay. arXiv preprint arXiv:2608.05784 (August 2026). https://arxiv.org/abs/2608.05784 | Independent researcher | D112, E144 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Jali2026 | D | [Jali et al., arXiv Apr 2026 · CMU] | Neharika Jali, Anupam Nayak, and Gauri Joshi. 2026. Not All Turns Are Equally Hard: Adaptive Thinking Budgets For Efficient Multi-Turn Reasoning in Agents. arXiv preprint arXiv:2604.05164 (April 2026). https://arxiv.org/abs/2604.05164 | Carnegie Mellon University | D50 | Authors and dates from the arXiv abs page (latest v3); institutions from the paper's author block. |
| Jang2026 | D | [Jang et al., arXiv Apr 2026 · CMU] | Lawrence Keunho Jang, Jing Yu Koh, Daniel Fried, and Ruslan Salakhutdinov. 2026. Odysseys: Benchmarking Web Agents on Realistic Long Horizon Tasks. arXiv preprint arXiv:2604.24964 (April 2026). https://arxiv.org/abs/2604.24964 | Carnegie Mellon University | none; cited in §3.8, §4.1, §5.8, §8.2, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Jiang2025 | D | [Jiang et al., arXiv Mar 2025 · Westlake University] | Wenjia Jiang, Yangyang Zhuang, Chenxi Song, Xu Yang, Joey Tianyi Zhou, and Chi Zhang. 2025. AppAgentX: Evolving GUI Agents as Proficient Smartphone Users. arXiv preprint arXiv:2503.02268 (March 2025). https://arxiv.org/abs/2503.02268 | Westlake University; Southeast University; Henan University; A*STAR | D44 | Authors and dates from the arXiv abs page (latest v3); institutions from the paper's author block. |
| Jin2025 | D | [Jin et al., arXiv May 2025 · Harvard University] | Yunho Jin, Gu-Yeon Wei, and David Brooks. 2025. The Energy Cost of Reasoning: Analyzing Energy Usage in LLMs with Test-time Compute. arXiv preprint arXiv:2505.14733 (May 2025). https://arxiv.org/abs/2505.14733 | Harvard University | E50 | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. The dossier cites an OpenReview PDF (id Kdc8aiKxF6); openreview.net is not readable from here, so the venue of that submission is not verified. The arXiv version has the same title and contains the 113.48× figure (E50). |
| Khanal2026 | D | [Khanal et al., arXiv Mar 2026 · Northern Kentucky University] | Aaditya Khanal, Yangyang Tao, and Junxiu Zhou. 2026. Beyond pass@1: A Reliability Science Framework for Long-Horizon LLM Agents. arXiv preprint arXiv:2603.29231 (March 2026). https://arxiv.org/abs/2603.29231 | Northern Kentucky University | none; cited in §3.8, §4.1, §5.8, §8.2, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Krumdick2026 | D | [Krumdick et al., arXiv Apr 2026 · Kensho Technologies] | Michael Krumdick, Varshini Reddy, Shivani Chaudhary, William Day, Maarij Ahmed, Hayan Haqqi, Muhammad Ahsen Fahim, Hanzallah Amjad, Ahmad Orakzai, Aqsa Gul, and Chris Tanner. 2026. FrontierFinance: A Long-Horizon Computer-Use Benchmark of Real-World Financial Tasks. arXiv preprint arXiv:2604.05912 (April 2026). https://arxiv.org/abs/2604.05912 | Kensho Technologies (S&P Global); MIT | D116, D119, D121, E163, E167 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Lee2026 | D | [Lee et al., arXiv Feb 2026 · UC Berkeley] | Nicholas Lee, Lutfi Eren Erdogan, Chris Joseph John, Surya Krishnapillai, Michael W. Mahoney, Kurt Keutzer, and Amir Gholami. 2026. Agentic Test-Time Scaling for WebAgents. arXiv preprint arXiv:2602.12276 (February 2026). https://arxiv.org/abs/2602.12276 | UC Berkeley; ICSI; LBNL | E44 | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. |
| Li2025a | D | [Li et al., arXiv Dec 2025 · University of Science and Technology of China] | Guopeng Li, Ruiqi Wu, and Haisheng Tan. 2025. A Plan Reuse Mechanism for LLM-Driven Agent. arXiv preprint arXiv:2512.21309 (December 2025). https://arxiv.org/abs/2512.21309 | University of Science and Technology of China | E188 | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. English version of a 2024 paper in Journal of Computer Research and Development (CRAD) 61(11); the CRAD page (crad.ict.ac.cn) was unreachable and the DOI returned no Crossref record, so the journal version is not verified. |
| Li2025b | D | [Li et al., arXiv Nov 2025 · Stanford University] | Hanchen Li, Runyuan He, Qiuyang Mang, Qizheng Zhang, Huanzhi Mao, Xiaokun Chen, Hangrui Zhou, Huanchen Zhang, Alvin Cheung, Joseph Gonzalez, and Ion Stoica. 2025. Continuum: Efficient and Robust Multi-Turn LLM Agent Scheduling with KV Cache Time-to-Live. arXiv preprint arXiv:2511.02230 (November 2025). https://arxiv.org/abs/2511.02230 | Stanford University; UC Berkeley; Tsinghua University | D14, D55, D61, D62, D122, D129, E172, E178, E184, E186, E187, E189 | Authors and dates from the arXiv abs page (latest v7); institutions from the paper's author block. |
| Li2026a | D | [Li et al., arXiv May 2026 · UC Davis] | Yuankai Li, Tinghui Zhu, Ha Min Son, Zhe Zhao, Xin Liu, and Muhao Chen. 2026. AQuaUI: Visual Token Reduction for GUI Agents with Adaptive Quadtrees. arXiv preprint arXiv:2605.19260 (May 2026). https://arxiv.org/abs/2605.19260 | UC Davis | none; cited in §2.2, §3.5, §5.8, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Li2026b | D | [Li et al., arXiv Apr 2026 · Institute of Automation, CAS] | Hongxin Li, Yuntao Chen, and Zhaoxiang Zhang. 2026. GoClick: Lightweight Element Grounding Model for Autonomous GUI Interaction. arXiv preprint arXiv:2604.23941 (April 2026). https://arxiv.org/abs/2604.23941 | Institute of Automation, CAS; University of Chinese Academy of Sciences; HKISI-CAS | none; cited in §2.2, §3.5, §3.10, §5.8, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Li2026c | D | [Li et al., arXiv May 2026 · CMU (inferred from andrew.cmu.edu e-mail] | Yubo Li, Yidi Miao, Yuntian Shen, and Yuxin Liu. 2026. PANDO: Efficient Multimodal AI Agents via Online Skill Distillation. arXiv preprint arXiv:2605.24785 (May 2026). https://arxiv.org/abs/2605.24785 | Carnegie Mellon University (inferred from andrew.cmu.edu e-mail; no affiliation line printed) | none; cited in §2.2, §3.1, §3.12, §5.2, §5.3, §5.4, §5.5, §5.8, §8.2, App. A | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. |
| Li2026d | D | [Li, arXiv Jun 2026 · Pine AI] | Bojie Li. 2026. PreAct: Computer-Using Agents that Get Faster on Repeated Tasks. arXiv preprint arXiv:2606.17929 (June 2026). https://arxiv.org/abs/2606.17929 | Pine AI | none; cited in §2.2, §3.2, §3.9, §4.1, §4.2, §5.8, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Li2026e | D | [Li et al., arXiv Jul 2026 · Salesforce Research] | Yu Li, Qinyuan Ye, Prafulla Kumar Choubey, Jiaxin Zhang, and Chien-Sheng Wu. 2026. Speculate with Memory: Lossless Acceleration for LLM Agents. arXiv preprint arXiv:2607.12236 (July 2026). https://arxiv.org/abs/2607.12236 | Salesforce Research | D11, D106 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Lin2026 | D | [Lin et al., arXiv Feb 2026 · Salesforce AI Research] | Xiaoqiang Lin, Jun Hao Liew, Silvio Savarese, and Junnan Li. 2026. W&D:Scaling Parallel Tool Calling for Efficient Deep Research Agents. arXiv preprint arXiv:2602.07359 (February 2026). https://arxiv.org/abs/2602.07359 | Salesforce AI Research | none; cited in §2.2, §3.4, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Lindenbauer2025 | D | [Lindenbauer et al., arXiv Aug 2025 · JetBrains Research] | Tobias Lindenbauer, Igor Slinko, Ludwig Felder, Egor Bogomolov, and Yaroslav Zharov. 2025. The Complexity Trap: Simple Observation Masking Is as Efficient as LLM Summarization for Agent Context Management. arXiv preprint arXiv:2508.21433 (August 2025). https://arxiv.org/abs/2508.21433 | JetBrains Research; Technical University of Munich | none; cited in §2.2, §3.5, §3.10, App. A | Authors and dates from the arXiv abs page (latest v3); institutions from the paper's author block. arXiv v3 comment: DL4C workshop at NeurIPS 2025 (non-archival workshop, kept in D). |
| Liu2026a | D | [Liu et al., arXiv Jul 2026 · Microsoft Azure Research] | Banruo Liu, Haoran Qiu, Íñigo Goiri, Rodrigo Fonseca, Ricardo Bianchini, and Esha Choukse. 2026. Agentic Coding in the Wild: Characterizing GitHub Copilot Traces at Production Scale. arXiv preprint arXiv:2608.00101 (July 2026). https://arxiv.org/abs/2608.00101 | Microsoft Azure Research; UIUC | E20, E106 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Liu2026d | D | [Liu et al., arXiv Sep 2026 · University of Southern California] | Zeyu Liu, Souvik Kundu, and Peter A. Beerel. 2026. Speculative Macro Commit for Faster Tool-Using Agents. arXiv preprint arXiv:2609.03236 (September 2026). https://arxiv.org/abs/2609.03236 | University of Southern California; Intel Labs | D103, D108, E124, E125, E138 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. PDF header and arXiv comment: IEEE MLSP 2026 (28 Sep–1 Oct 2026); the MLSP 2026 site failed TLS from here, so not verified. |
| Lumer2026 | D | [Lumer et al., arXiv Jan 2026 · PricewaterhouseCoopers] | Elias Lumer, Faheem Nizar, Akshaya Jangiti, Kevin Frank, Anmol Gulati, Mandar Phadate, and Vamse Kumar Subbiah. 2026. Don't Break the Cache: An Evaluation of Prompt Caching for Long-Horizon Agentic Tasks. arXiv preprint arXiv:2601.06007 (January 2026). https://arxiv.org/abs/2601.06007 | PricewaterhouseCoopers (PwC U.S.) | E84 | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. |
| Luo2025 | D | [Luo et al., arXiv Mar 2025 · Peking University] | Junyu Luo, Weizhi Zhang, Ye Yuan, Yusheng Zhao, Junwei Yang, Yiyang Gu, Bohan Wu, Binqi Chen, Ziyue Qiao, Qingqing Long, et al. (26 authors in total). 2025. Large Language Model Agent: A Survey on Methodology, Applications and Challenges. arXiv preprint arXiv:2503.21460 (March 2025). https://arxiv.org/abs/2503.21460 | Peking University; University of Illinois Chicago; Great Bay University; CAS; Nanyang Technological University; others | none; cited in §3.11, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Mazeika2025 | D | [Mazeika et al., arXiv Oct 2025 · Center for AI Safety] | Mantas Mazeika, Alice Gatti, Cristina Menghini, Udari Madhushani Sehwag, Shivam Singhal, Yury Orlovskiy, Steven Basart, Manasi Sharma, Denis Peskoff, Elaine Lau, et al. (47 authors in total). 2025. Remote Labor Index: Measuring AI Automation of Remote Work. arXiv preprint arXiv:2510.26787 (October 2025). https://arxiv.org/abs/2510.26787 | Center for AI Safety; Scale AI | E171 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Miller2024 | D | [Miller, arXiv Nov 2024 · Anthropic] | Evan Miller. 2024. Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations. arXiv preprint arXiv:2411.00640 (November 2024). https://arxiv.org/abs/2411.00640 | Anthropic | none; cited in §3.8, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Mohammadi2026a | D | [Mohammadi et al., arXiv Feb 2026 · MPI-SWS] | Bardia Mohammadi, Nearchos Potamitis, Lars Klein, Akhil Arora, and Laurent Bindschaedler. 2026. Atomix: Timely, Transactional Tool Use for Reliable Agentic Workflows. arXiv preprint arXiv:2602.14849 (February 2026). https://arxiv.org/abs/2602.14849 | MPI-SWS; EPFL; Aarhus University | D104, D107, E113, E114, E115, E116, E129, E130 | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. |
| Mohammadi2026b | D | [Mohammadi et al., arXiv Jun 2026 · MPI-SWS] | Bardia Mohammadi, Lars Klein, Akhil Arora, and Laurent Bindschaedler. 2026. Ghost Tool Calls: Issue-Time Privacy for Speculative Agent Tools. arXiv preprint arXiv:2606.02483 (June 2026). https://arxiv.org/abs/2606.02483 | MPI-SWS; EPFL; Aarhus University | D106, E129, E130 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Ndzomga2026 | D | [Ndzomga, arXiv Mar 2026 · affiliation not stated] | Franck Ndzomga. 2026. Efficient Benchmarking of AI Agents. arXiv preprint arXiv:2603.23749 (March 2026). https://arxiv.org/abs/2603.23749 | no affiliation printed (single author) | none; cited in §3.8, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Nichols2025 | D | [Nichols et al., arXiv Dec 2025 · Lawrence Livermore National Laboratory] | Daniel Nichols, Prajwal Singhania, Charles Jekel, Abhinav Bhatele, and Harshitha Menon. 2025. Optimizing Agentic Language Model Inference via Speculative Tool Calls. arXiv preprint arXiv:2512.15834 (December 2025). https://arxiv.org/abs/2512.15834 | Lawrence Livermore National Laboratory; University of Maryland | none; cited in §2.2, §3.3, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Pan2026b | D | [Pan et al., arXiv Jun 2026 · UC San Diego] | Zaifeng Pan, Qianxu Wang, Zhengding Hu, Chang Chen, Yue Guan, Yanbo Zhou, Steven Swanson, and Yufei Ding. 2026. SmoothAgent: Efficient Long-Horizon LLM-Based Agent Serving with Lookahead Context Engineering. arXiv preprint arXiv:2607.00151 (June 2026). https://arxiv.org/abs/2607.00151 | UC San Diego | E35 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Pandey2026 | D | [Pandey et al., arXiv May 2026 · UC San Diego] | Nilesh Prasad Pandey, Jason Kong, Lanxiang Hu, Quanling Zhao, Yujie Zhao, Onat Gungor, Hao Zhang, and Tajana Rosing. 2026. AgentKVShift: Efficient KV Cache Reuse for Agentic Memory Systems. arXiv preprint arXiv:2607.21604 (May 2026). https://arxiv.org/abs/2607.21604 | UC San Diego | D127, E179 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Shi2026 | D | [Shi et al., arXiv Jun 2026 · Peking University] | Chunan Shi, Yilei Chen, Yilin Chen, Xupeng Miao, and Bin Cui. 2026. Multi-Segment Attention: Enabling Efficient KV-Cache Management for Faster Large Language Model Serving. arXiv preprint arXiv:2606.02964 (June 2026). https://arxiv.org/abs/2606.02964 | Peking University | D127, E178, E189 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Singh2024 | D | [Singh et al., arXiv May 2024 · Microsoft] | Simranjit Singh, Andreas Karatzas, Michael Fore, Iraklis Anagnostopoulos, and Dimitrios Stamoulis. 2024. An LLM-Tool Compiler for Fused Parallel Function Calling. arXiv preprint arXiv:2405.17438 (May 2024). https://arxiv.org/abs/2405.17438 | Microsoft; Southern Illinois University Carbondale | none; cited in §2.2, §3.4, §3.12, §5.8, §8.2, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Sui2026 | D | [Sui et al., arXiv Mar 2026 · HKUST] | Yifan Sui, Han Zhao, Rui Ma, Zhiyuan He, Hao Wang, Jianxun Li, Kaiqiang Xu, Kai Chen, and Yuqing Yang. 2026. Parallelizing Tool Execution and LLM Generation for Low-Latency Agent Serving. arXiv preprint arXiv:2603.18897 (March 2026). https://arxiv.org/abs/2603.18897 | HKUST; Microsoft Research; Shanghai Jiao Tong University; Google; Stevens Institute of Technology | D13, D63, D64, D103, E28, E127 | Authors and dates from the arXiv abs page (latest v3); institutions from the paper's author block. |
| Sun2026 | D | [Sun et al., arXiv Jun 2026 · UC Berkeley ("leading institution"] | Yiyou Sun, Xinyang Han, Weichen Zhang, Yuanbo Pang, Tianyu Wang, Yuhan Cao, Yixiao Huang, Chris Duroiu, Haoyun Zhang, Jeffrey Lin, et al. (310 authors in total). 2026. Agents' Last Exam. arXiv preprint arXiv:2606.05405 (June 2026). https://arxiv.org/abs/2606.05405 | UC Berkeley ("leading institution"; full affiliations only on the project site) | E168 | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. |
| Tang2025 | D | [Tang et al., arXiv Mar 2025 · Microsoft Research Asia] | Fei Tang, Yongliang Shen, Hang Zhang, Siqi Chen, Guiyang Hou, Wenqi Zhang, Wenqiao Zhang, Kaitao Song, Weiming Lu, and Yueting Zhuang. 2025. Think Twice, Click Once: Enhancing GUI Grounding via Fast and Slow Systems. arXiv preprint arXiv:2503.06470 (March 2025). https://arxiv.org/abs/2503.06470 | Microsoft Research Asia; Zhejiang University | none; cited in §2.2, §3.7, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Vidgen2026 | D | [Vidgen et al., arXiv Jan 2026 · Mercor] | Bertie Vidgen, Austin Mann, Abby Fennelly, John Wright Stanly, Lucas Rothman, Marco Burstein, Julien Benchek, David Ostrofsky, Anirudh Ravichandran, Debnil Sur, et al. (24 authors in total). 2026. APEX-Agents. arXiv preprint arXiv:2601.14242 (January 2026). https://arxiv.org/abs/2601.14242 | Mercor | D116, D120, E167 | Authors and dates from the arXiv abs page (latest v3); institutions from the paper's author block. |
| Wang2025b | D | [Wang et al., arXiv Jul 2025 · OPPO] | Ningning Wang, Xavier Hu, Pai Liu, He Zhu, Yue Hou, Heyuan Huang, Shengyu Zhang, Jian Yang, Jiaheng Liu, Ge Zhang, Changwang Zhang, Jun Wang, Yuchen Eleanor Jiang, and Wangchunshu Zhou. 2025. Efficient Agents: Building Effective Agents While Reducing Cost. arXiv preprint arXiv:2508.02694 (July 2025). https://arxiv.org/abs/2508.02694 | OPPO (OPPO AI Agent Team) | D9, E48 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Wang2026a | D | [Wang et al., arXiv May 2026 · Bengbu Medical University] | Xiaohua Wang, Kai Yu, XuXiao Liang, Liang Wang, and Chao Han. 2026. Good to Go: The LOOP Skill Engine That Hits 99% Success and Slashes Token Usage by 99% via One-Shot Recording and Deterministic Replay. arXiv preprint arXiv:2605.14237 (May 2026). https://arxiv.org/abs/2605.14237 | Bengbu Medical University; CHARMMIRAEL Biotech | D110, D111, D112, E140, E141, E142, E143 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Wang2026b | D | [Wang et al., arXiv Sep 2026 · NVIDIA] | Zhilin Wang, Shaokun Zhang, Yifan Zhang, Hao Zhang, Jin Xu, Binfeng Xu, Jian Hu, Yunheng Zou, Karan Sapra, Andrew Tao, Jan Kautz, and Yi Dong. 2026. OSWorld-Pro: Process-based Evaluation for Computer Use Agents. arXiv preprint arXiv:2609.24890 (September 2026). https://arxiv.org/abs/2609.24890 | NVIDIA | none; cited in §3.8, §5.7, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Wang2026c | D | [Wang et al., arXiv Jan 2026 · Shanghai Jiao Tong University] | Yuhang Wang, Yuling Shi, Mo Yang, Rongrui Zhang, Shilin He, Heng Lian, Yuting Chen, Siyu Ye, Kai Cai, and Xiaodong Gu. 2026. SWE-Pruner: Self-Adaptive Context Pruning for Coding Agents. arXiv preprint arXiv:2601.16746 (January 2026). https://arxiv.org/abs/2601.16746 | Shanghai Jiao Tong University; Sun Yat-sen University; Douyin Group | none; cited in §2.2, §3.5, §3.12, §5.8, §8.2, App. A | Authors and dates from the arXiv abs page (latest v4); institutions from the paper's author block. |
| Wang2026d | D | [Wang et al., arXiv Sep 2026 · Dalian University of Technology] | Yuhao Wang, Mu Qiao, Xindong Zhang, Yunzhi Zhuge, Lei Zhang, and Huchuan Lu. 2026. TRACE: Trajectory-robust Admission with Evidence Ordering for Efficient GUI Agents. arXiv preprint arXiv:2609.10297 (September 2026). https://arxiv.org/abs/2609.10297 | Dalian University of Technology; OPPO Research Institute; PolyU | none; cited in §2.2, §3.5, §3.10, §5.8, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Wei2025 | D | [Wei et al., arXiv Apr 2025 · OpenAI] | Jason Wei, Zhiqing Sun, Spencer Papay, Scott McKinney, Jeffrey Han, Isa Fulford, Hyung Won Chung, Alex Tachard Passos, William Fedus, and Amelia Glaese. 2025. BrowseComp: A Simple Yet Challenging Benchmark for Browsing Agents. arXiv preprint arXiv:2504.12516 (April 2025). https://arxiv.org/abs/2504.12516 | OpenAI | D87, E169 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Wei2026 | D | [Wei et al., arXiv Apr 2026 · Yale University] | Jinbiao Wei, Kangqi Ni, Yilun Zhao, Guo Gan, and Arman Cohan. 2026. Step-level Optimization for Efficient Computer-use Agents. arXiv preprint arXiv:2604.27151 (April 2026). https://arxiv.org/abs/2604.27151 | Yale University; UNC Chapel Hill | D47 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Wong2026 | D | [Wong et al., arXiv May 2026 · Microsoft Research] | Mike Wong, Kevin Hsieh, Suman Nath, and Ravi Netravali. 2026. Skim: Speculative Execution for Fast and Efficient Web Agents. arXiv preprint arXiv:2605.16565 (May 2026). https://arxiv.org/abs/2605.16565 | Microsoft Research; Princeton University | D96, E17 | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. |
| Wu2026a | D | [Wu et al., arXiv Feb 2026 · Peking University] | Yongtong Wu, Shaoyuan Chen, Yinmin Zhong, Rilin Huang, Yixuan Tan, Wentao Zhang, Liyue Zhang, Shangyan Zhou, Yuxuan Liu, Shunfeng Zhou, Mingxing Zhang, Xin Jin, and Panpan Huang. 2026. DualPath: Breaking the Storage Bandwidth Bottleneck in Agentic LLM Inference. arXiv preprint arXiv:2602.21548 (February 2026). https://arxiv.org/abs/2602.21548 | Peking University; Tsinghua University; DeepSeek-AI | D127, E180 | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. |
| Wu2026b | D | [Wu et al., arXiv Aug 2026 · SUSTech] | Guanlong Wu, Dahui Li, Ke Jiang, Jianyu Niu, Cong Wang, and Yinqian Zhang. 2026. Safe to Resume? Breaking Execution Continuity of Agent Execution via Rollback. arXiv preprint arXiv:2608.29381 (August 2026). https://arxiv.org/abs/2608.29381 | SUSTech; City University of Hong Kong | D107, E136 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Xu2026a | D | [Xu et al., arXiv Feb 2026 · CUHK] | Zhou Xu, Bowen Zhou, Qi Wang, Shuwen Feng, and Jingyu Xiao. 2026. Spatio-Temporal Token Pruning for Efficient High-Resolution GUI Agents. arXiv preprint arXiv:2602.23235 (February 2026). https://arxiv.org/abs/2602.23235 | CUHK; Tsinghua University (Shenzhen); Xidian University | none; cited in §2.2, §3.5, §3.12, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Xu2026b | D | [Xu et al., arXiv Jun 2026 · Zhejiang University] | Buqiang Xu, Zirui Xue, Dianmou Chen, Chenyang Fu, Chiyu Wu, Caiying Huang, Chen Jiang, Jizhan Fang, Xinle Deng, Yijun Chen, Yunzhi Yao, Xuehai Wang, Jin Shang, Gong Yu, and Ningyu Zhang. 2026. TokenPilot: Cache-Efficient Context Management for LLM Agents. arXiv preprint arXiv:2606.17016 (June 2026). https://arxiv.org/abs/2606.17016 | Zhejiang University; UESTC; Xi’an University of Electronic Science and Technology; HomologyAI | D124, E174 | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. arXiv comment: "EMNLP 2026 Findings"; not verifiable on 2026.emnlp.org yet. |
| Yang2026a | D | [Yang et al., arXiv Sep 2026 · Rutgers University] | Yanting Yang, Can Jin, Jinman Zhao, Jiahao Wu, Yang Zhou, Zhepeng Wang, Zhendong Wang, Mu Zhou, and Dimitris N. Metaxas. 2026. Act More, Decide Less: Skill-Guided Adaptive Action Chunking for Long-Horizon LLM Agents. arXiv preprint arXiv:2609.02042 (September 2026). https://arxiv.org/abs/2609.02042 | Rutgers University; Amazon; Microsoft; PolyU; University of Toronto | D89 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. arXiv comment: "EMNLP 2026 Camera Ready"; not verifiable on 2026.emnlp.org yet. |
| Yang2026b | D | [Yang et al., arXiv Mar 2026 · UC Santa Barbara] | Jingbo Yang, Bairu Hou, Wei Wei, Yujia Bao, and Shiyu Chang. 2026. Ares: Adaptive Reasoning Effort Selection for Efficient LLM Agents. arXiv preprint arXiv:2603.07915 (March 2026). https://arxiv.org/abs/2603.07915 | UC Santa Barbara; Accenture | D49, D87 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Yang2026c | D | [Yang et al., arXiv Jan 2026 · Shanghai AI Laboratory] | Xiaofang Yang, Lijun Li, Heng Zhou, Tong Zhu, Xiaoye Qu, Yuchen Fan, Qianshan Wei, Rui Ye, Li Kang, Yiran Qin, Daizong Liu, Qi Li, Ning Ding, Siheng Chen, and Jing Shao. 2026. Toward Efficient Agents: Memory, Tool learning, and Planning. arXiv preprint arXiv:2601.14192 (January 2026). https://arxiv.org/abs/2601.14192 | Shanghai AI Laboratory; Fudan; SJTU; Tsinghua; others | none; cited in §3.11, App. A | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. |
| Yu2026 | D | [Yu et al., arXiv Jul 2026 · BUPT] | Zedong Yu, Qianxing Li, Zhi Gao, Liuyu Xiang, Chenrui Shi, Yang Liu, Huiming Wu, Yujie Wei, Yuhao Fei, Yubo Fu, and Zhaofeng He. 2026. Beyond Sequential Interaction: Benchmarking Parallel Execution and Coordination for GUI Agents. arXiv preprint arXiv:2607.22689 (July 2026). https://arxiv.org/abs/2607.22689 | BUPT; BIGAI; Beijing Institute of Technology; China University of Geosciences | none; cited in §2.2, §3.4, §3.12, §5.8, §8.2, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Yuan2026a | D | [Yuan et al., arXiv May 2026 · UIUC] | Yichao Yuan, Ankita Nayak, Souvik Kundu, and Nishil Talati. 2026. Agentic AI Workload Characteristics. arXiv preprint arXiv:2605.26297 (May 2026). https://arxiv.org/abs/2605.26297 | UIUC; Gimlet Labs; Intel | D36, D73, D99, E29, E107 | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. |
| Yuan2026b | D | [Yuan et al., arXiv Jun 2026 · XLANG Lab  and collaborators] | Mengqi Yuan, Zilong Zhou, Xinzhuang Xiong, Weiming Wu, Jiayang Sun, Jiamin Song, Kaiqian Cui, Bowen Wang, Haoyuan Wu, Yitong Li, et al. (36 authors in total). 2026. OSWorld 2.0: Benchmarking Computer Use Agents on Long-Horizon Real-World Tasks. arXiv preprint arXiv:2606.29537 (June 2026). https://arxiv.org/abs/2606.29537 | XLANG Lab (The University of Hong Kong) and collaborators | D2, D3, D4, D8, D32, D38, D46, D119, E5, E6, E7, E8, E9, E40, E41, E42, E200 | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. |
| Zhai2026a | D | [Zhai et al., arXiv Apr 2026 · Fudan University] | Zhiyuan Zhai, Ming Li, and Xin Wang. 2026. Revisable by Design: A Theory of Streaming LLM Agent Execution. arXiv preprint arXiv:2604.23283 (April 2026). https://arxiv.org/abs/2604.23283 | Fudan University; Guangming Lab | E135 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Zhai2026b | D | [Zhai et al., arXiv Jan 2026 · Southeast University] | Yi Zhai, Dian Shen, Junzhou Luo, and Bin Yang. 2026. ToolCaching: Towards Efficient Caching for LLM Tool-calling. arXiv preprint arXiv:2601.15335 (January 2026). https://arxiv.org/abs/2601.15335 | Southeast University | none; cited in §2.2, §3.2, §3.12, §5.8, §8.2, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Zhang2026a | D | [Zhang et al., arXiv Mar 2026 · The University of Sydney] | Yuning Zhang, Yan Yan, Nan Yang, and Dong Yuan. 2026. AgentServe: Algorithm-System Co-Design for Efficient Agentic AI Serving on a Consumer-Grade GPU. arXiv preprint arXiv:2603.10342 (March 2026). https://arxiv.org/abs/2603.10342 | The University of Sydney | D127, E183 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Zhang2026b | D | [Zhang et al., arXiv Feb 2026 · Microsoft] | Caiqi Zhang, Menglin Xia, Xuchao Zhang, Daniel Madrigal, Ankur Mallick, Samuel Kessler, Victor Ruehle, and Saravan Rajmohan. 2026. Budget-Aware Agentic Routing via Boundary-Guided Training. arXiv preprint arXiv:2602.21227 (February 2026). https://arxiv.org/abs/2602.21227 | Microsoft (M365 Research); University of Cambridge | none; cited in §2.2, §3.5, §3.10, §5.4, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Zhang2026e | D | [Zhang et al., arXiv Jul 2026 · UC Santa Cruz] | Rui Zhang, Chaeeun Kim, Shaoting Feng, Kuntai Du, Yuhan Liu, Yi Zhong, Cheng-Wei Ching, Junchen Jiang, and Liting Hu. 2026. Learning Agent Execution for KV-Cache Management in Agentic Serving. arXiv preprint arXiv:2608.14624 (July 2026). https://arxiv.org/abs/2608.14624 | UC Santa Cruz; University of Washington; University of Chicago | D55, D122, D123, E172, E181, E189 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Zhang2026g | D | [Zhang et al., arXiv Jul 2026 · Beihang University] | Yihui Zhang, Tianyu Wo, Jinghao Wang, Xiaoyang Sun, Menghao Zhang, Cangzhou Yuan, Li Li, Chunming Hu, Albert Y. Zomaya, and Renyu Yang. 2026. SpecBox: Speculative Sandbox Scheduling for Efficient LLM Agent Serving. arXiv preprint arXiv:2607.23933 (July 2026). https://arxiv.org/abs/2607.23933 | Beihang University; University of Leeds; The University of Sydney | E138, E176 | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. |
| Zhao2026a | D | [Zhao et al., arXiv Sep 2026 · Johns Hopkins University] | Yao Zhao, Aditya Shanmugham, Swastik Roy, and Yanxun Xu. 2026. EchoPath: Execution-Level Replayable Memory for GUI Agents. arXiv preprint arXiv:2609.16635 (September 2026). https://arxiv.org/abs/2609.16635 | Johns Hopkins University; Amazon AGI | D82, D83, D84, D85, E91, E92, E132 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Zhao2026b | D | [Zhao et al., arXiv Apr 2026 · Salesforce AI Research] | Zirui Zhao, Jun Hao Liew, Yan Yang, Wenzhuo Yang, Ziyang Luo, Doyen Sahoo, Silvio Savarese, and Junnan Li. 2026. GPA: Learning GUI Process Automation from Demonstrations. arXiv preprint arXiv:2604.01676 (April 2026). https://arxiv.org/abs/2604.01676 | Salesforce AI Research | none; cited in §0.4, §3.1, §3.10, App. A | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. |
| Zheng2025 | D | [Zheng et al., arXiv Apr 2025 · The Ohio State University] | Boyuan Zheng, Michael Y. Fatemi, Xiaolong Jin, Zora Zhiruo Wang, Apurva Gandhi, Yueqi Song, Yu Gu, Jayanth Srinivasa, Gaowen Liu, Graham Neubig, and Yu Su. 2025. SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills. arXiv preprint arXiv:2504.07079 (April 2025). https://arxiv.org/abs/2504.07079 | The Ohio State University; CMU; Purdue University; University of Virginia; Cisco Research | none; cited in §3.1, §3.12, §5.3, §5.4, §5.5, §5.7, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Zheng2026 | D | [Zheng et al., arXiv May 2026 · Shanghai Jiao Tong University] | Haoyu Zheng, Fangcheng Fu, Jia Wu, Binhang Yuan, Yongqiang Zhang, Hao Wang, Yuanyuan Zhu, Xiao Yan, and Jiawei Jiang. 2026. Efficient Serving for Dynamic Agent Workflows with Prediction-based KV-Cache Management. arXiv preprint arXiv:2605.06472 (May 2026). https://arxiv.org/abs/2605.06472 | Shanghai Jiao Tong University; HKUST; Wuhan University; Macquarie University; Dameng Database | D127, E182 | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Zhong2026a | D | [Zhong et al., arXiv Feb 2026 · Georgia Tech] | Hongbin Zhong, Fazle Faisal, Luis França, Tanakorn Leesatapornwongsa, Adriana Szekeres, Kexin Rong, and Suman Nath. 2026. ActionEngine: From Reactive to Programmatic GUI Agents via State Machine Memory. arXiv preprint arXiv:2602.20502 (February 2026). https://arxiv.org/abs/2602.20502 | Georgia Tech; Microsoft Research | none; cited in §3.1, §3.5, §3.10, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Zhong2026b | D | [Zhong et al., arXiv Mar 2026 · Peking University] | Shuzhang Zhong, Baotong Lu, Qi Chen, Chuanjie Liu, Fan Yang, and Meng Li. 2026. DualSpec: Accelerating Deep Research Agents via Dual-Process Action Speculation. arXiv preprint arXiv:2603.07416 (March 2026). https://arxiv.org/abs/2603.07416 | Peking University; Microsoft Research | none; cited in §2.2, §3.3, §3.10, §8.2, App. A | Authors and dates from the arXiv abs page (latest v1); institutions from the paper's author block. |
| Zhu2026 | D | [Zhu et al., arXiv Jun 2026 · University of Washington] | Kan Zhu, Mathew Jacob, Chenxi Ma, Yi Pan, Stephanie Wang, Arvind Krishnamurthy, and Baris Kasikci. 2026. TraceLab: Characterizing Coding Agent Workloads for LLM Serving. arXiv preprint arXiv:2606.30560 (June 2026). https://arxiv.org/abs/2606.30560 | University of Washington; Shanghai Jiao Tong University; Wuhan University of Technology | D16, D65, D66, D67, D99, E19, E20, E105, E110, E187 | Authors and dates from the arXiv abs page (latest v2); institutions from the paper's author block. |

## Excluded (class E, not citable)

| # | URL | Source | Reason | E/D rows that cite it |
|---|---|---|---|---|
| X1 | https://artificialanalysis.ai/articles/aa-briefcase-time-per-task | Artificial Analysis, "Measuring time per task in AA-Briefcase" (24 Jun 2026) | Benchmark tracker site (independent vendor); not peer-reviewed. Dossier D-follow-up 6 shows "time per task" is decode time only. | E109 |
| X2 | https://artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v4-1 | Artificial Analysis, Intelligence Index v4.1 article (15 Jun 2026) | Benchmark tracker site. | E207 |
| X3 | https://artificialanalysis.ai/articles/gemini-3-8-flash | Artificial Analysis, Gemini 3.8 Flash article (2 Sep 2026) | Benchmark tracker site. | D74, E79 |
| X4 | https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index | Artificial Analysis Intelligence Index page | Benchmark tracker site (live page). | D134, E207 |
| X5 | https://artificialanalysis.ai/methodology | Artificial Analysis methodology page | Benchmark tracker site (method page for its own tracker). | E208 |
| X6 | https://artificialanalysis.ai/models/claude-opus-5-5-high | Artificial Analysis model page, Claude Opus 5.5 | Benchmark tracker site (live page). | E208 |
| X7 | https://artificialanalysis.ai/models/gemini-3-8-flash | Artificial Analysis model page, Gemini 3.8 Flash | Benchmark tracker site (live page). | D74, E79 |
| X8 | https://browser-use.com/posts/llm-gateway | Browser Use blog, "The Fastest Web Agent in the World" (8 Oct 2025) | Vendor blog quoting its own speed numbers; no independent method. | D1, D40, D133, E36, E85 |
| X9 | https://browser-use.com/posts/speed-matters | Browser Use blog, "Speed Matters" (9 Oct 2025) | Vendor blog quoting its own speed numbers. | D1, E32, E36, E85 |
| X10 | https://browser-use.com/posts/ai-browser-agent-benchmark | Browser Use blog, "Browser Agent Benchmark" (31 Jan 2026) | Vendor-run benchmark blog. | E47, E202 |
| X11 | https://browser-use.com/benchmarks/agents | Browser Use web-agent benchmark page | Vendor-run leaderboard (tracker). | E47 |
| X12 | https://www.browserbase.com/blog/stagehand-caching | Browserbase blog, "How Caching Works in Stagehand (and Where It Breaks)" (24 Feb 2026) | Vendor blog; the citable product behaviour is in the Stagehand docs (Browserbase2026a). | E153, E154 |
| X13 | https://www.browserbase.com/blog/stagehand-v3 | Browserbase blog, "Stagehand v3" (29 Oct 2025) | Vendor product-launch blog. | E87, E154, E203 |
| X14 | https://www.browserbase.com/blog/training-computer-use-models-in-the-real-world-with-microsoft | Browserbase blog, "Evaluating computer use models with Microsoft" | Vendor blog (the Fara-7B numbers are cited from the Fara-7B report instead). | E90 |
| X15 | https://www.cerebras.ai/blog/accelerating-gpt-5-6-sol-ultrafast-with-openai | Cerebras blog, GPT-5.6 Sol Ultrafast | Vendor marketing (speed claim). | E87, E195 |
| X16 | https://www.cerebras.ai/blog/the-rise-of-slow-personal-assistants | Cerebras blog, "Why AI Assistants Are Slow" | Vendor marketing blog. | E201 |
| X17 | https://sambanova.ai/blog/the-premium-inference-moment-is-here | SambaNova blog, "Premium Inference" | Vendor marketing blog. | E87, E205 |
| X18 | https://sambanova.ai/blog/first-disaggregated-inference-demo-for-ai-agents-live | SambaNova blog, disaggregated inference demo | Vendor marketing blog. | E205 |
| X19 | https://nvidianews.nvidia.com/news/nvidia-groq-3-lpx-now-in-full-production-with-world-class-speed-for-agentic-ai | NVIDIA Newsroom, Groq 3 LPX press release | Product launch press release. | E87, E204 |
| X20 | https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/ | OpenAI, GPT-5.6 price-performance launch page | Product launch page (also 403 to automated fetch). | E77 |
| X21 | https://openai.com/index/introducing-the-agents-api/ | OpenAI, "Introducing the Agents API" (10 Sep 2026) | Product launch page. | E82 |
| X22 | https://openai.com/index/introducing-chatgpt-agent/ | OpenAI, "Introducing ChatGPT agent" (17 Jul 2025) | Product launch page. | E21, E39 |
| X23 | https://openai.com/index/introducing-operator/ | OpenAI, "Introducing Operator" | Product launch page. | Appendix A only |
| X24 | https://openai.com/index/introducing-gpt-5-for-developers/ | OpenAI, "Introducing GPT-5 for developers" | Product launch page (vendor effort claims). | E88 |
| X25 | https://openai.com/index/gpt-6-astra/ | OpenAI, GPT-6 Astra launch page | Product launch page; 403, not read (dossier E200 relies on secondary copies). | E200 |
| X26 | https://openai.com/index/previewing-ultrafast/ | OpenAI, "Previewing Ultrafast" | Product launch page. | E194 |
| X27 | https://community.openai.com/t/ultrafast-mode-preview-gpt-5-6-sol-at-up-to-14x-the-speed-in-the-api/1390344 | OpenAI Developer Community post, Ultrafast mode preview (13 Aug 2026) | Forum announcement quoting a vendor speed-up without method. | E77, E194 |
| X28 | https://www.anthropic.com/news/claude-opus-4-5 | Anthropic, "Introducing Claude Opus 4.5" | Product launch page (vendor effort claims). | E88 |
| X29 | https://www.anthropic.com/news/claude-opus-4-8 | Anthropic, "Introducing Claude Opus 4.8" | Product launch page. | E83 |
| X30 | https://www.anthropic.com/claude/opus | Anthropic, Claude Opus product page | Product marketing page. | E76 |
| X31 | https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-computer-use-model/ | Google, "Introducing the Gemini 2.5 Computer Use model" (7 Oct 2025) | Product launch page. | D133, E37, E199 |
| X32 | https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-computer-use-gemini-3-5-flash/ | Google, "Introducing computer use in Gemini 3.5 Flash" (24 Jun 2026) | Product launch page. | E79 |
| X33 | https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/ | Google, "Gemini 3.5" (19 May 2026) | Product launch page. | E79 |
| X34 | https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/ | Google, "3.6 Flash, 3.5 Flash-Lite, and 3.5 Flash Cyber" (21 Jul 2026) | Product launch page. | D28, E79 |
| X35 | https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/ | Google, "Introducing Gemini 3.8 Flash and 3.8 Flash Cyber" (2 Sep 2026) | Product launch page. | E79 |
| X36 | https://blog.google/innovation-and-ai/sundar-pichai-io-2026/ | Google, I/O 2026 keynote post (19 May 2026) | Keynote/product announcement quoting usage figures without method. | E63 |
| X37 | https://blog.google/innovation-and-ai/technology/developers-tools/introducing-flex-and-priority-inference/ | Google, "Flex and Priority tiers in the Gemini API" (2 Apr 2026) | Product launch post (the citable terms are in the Gemini API docs, Google2026c/d). | E197 |
| X38 | https://www.automationanywhere.com/products/automator-ai | Automation Anywhere, Automator AI product page | Vendor marketing page (dossier already labels it vendor-marketing). | E150 |
| X39 | https://community.automationanywhere.com/generative-recorder-85080/generative-recorder-and-resilient-automation-april-2024-88211 | Automation Anywhere community post (13 May 2024) | Vendor community/marketing post. | E149 |
| X40 | https://www.uipath.com/blog/product-and-updates/technical-tuesday-how-healing-agent-solves-ui-automation-challenges | UiPath blog, "How UiPath Healing Agent solves UI automation's biggest challenges" (22 Jul 2025) | Vendor blog. | E146 |
| X41 | https://www.notte.cc/blog/browser-agent-stack-2026 | Notte blog, "The browser automation stack in 2026" (12 Mar 2026) | Vendor blog, no numbers (dossier E159 labels it vendor-marketing). | E159 |
| X42 | https://the-decoder.com/ai-is-becoming-ais-biggest-customer-as-agentic-token-usage-jumps-14x-on-openrouter/ | the-decoder (23 Aug 2026) | Secondary news report of a LinkedIn post. | D71, E58 |
| X43 | https://the-decoder.com/openrouters-staggering-token-chart-is-the-ai-bubble-debate-in-a-single-image/ | the-decoder (17 Sep 2026) | Secondary news report of a LinkedIn post. | E59 |
| X44 | https://www.linkedin.com/feed/update/urn:li:activity:7493029883191681024/ | Peter Walker (OpenRouter), LinkedIn post (11 Aug 2026) | Social-media post; not machine-retrievable; numbers without method. | D71, E58 |
| X45 | https://www.linkedin.com/feed/update/urn:li:activity:7506103118410072064/ | Peter Walker (OpenRouter), LinkedIn post (16 Sep 2026) | Social-media post; not machine-retrievable; numbers without method. | E59 |
| X46 | https://x.com/gabemulley/status/2026041548429828101 | Anthropic staff post on X (23 Feb 2026) | Social-media post quoting a speed-up without method. | E210 |
| X47 | https://x.com/trq212/status/2026110215561822374 | Anthropic staff post on X (24 Feb 2026) | Social-media post quoting a speed-up without method. | E210 |
| X48 | https://tokencost.app/blog/llm-fast-mode-latency-pricing | TokenCost blog (1 Aug 2026) | Secondary tracker/blog. | E209 |
| X49 | https://pasqualepillitteri.it/en/news/346/claude-chrome-quick-mode-fast-browsing-guide | pasqualepillitteri.it blog | Secondary blog. | E210 |
| X50 | https://www.datacamp.com/blog/gpt-6-astra | DataCamp blog, GPT-6 Astra | Secondary blog quoting vendor numbers. | E200 |
| X51 | https://www.vellum.ai/blog/gpt-6-astra-benchmarks-explained | Vellum blog, GPT-6 Astra benchmarks (3 Sep 2026) | Secondary blog quoting vendor numbers. | E200 |
| X52 | https://github.com/argszero/silicon-science-cs/issues/50 | GitHub issue #50 in argszero/silicon-science-cs (simulation write-up) | Non-paper GitHub issue; no review, author pseudonymous (dossier E138 labels it non-paper). | E138 |

## URL map

Every URL in Appendix A and in the E/D rows, with the one key (or excluded entry X#) it maps to. `slides/check_references.py` reads this table.

| URL | Maps to |
|---|---|
| https://2027.eurosys.org/cfp.html | Chen2026b |
| https://a16z.com/state-of-ai/ | Aubakirova2026 |
| https://aclanthology.org/2025.acl-long.369/ | Hu2025 |
| https://aclanthology.org/2025.acl-long.381.pdf | Lu2025a |
| https://aclanthology.org/2025.acl-long.381/ | Lu2025a |
| https://aclanthology.org/2025.findings-acl.577/ | Song2025 |
| https://aclanthology.org/2026.acl-long.1614.pdf | Xu2026c |
| https://aclanthology.org/2026.findings-acl.1330/ | Yehudai2026 |
| https://aclanthology.org/2026.findings-acl.392.pdf | Zhang2026c |
| https://ai.google.dev/gemini-api/docs/computer-use | Google2026a |
| https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite | Google2026b |
| https://ai.google.dev/gemini-api/docs/pricing | Google2026c |
| https://ai.google.dev/gemini-api/docs/priority-inference | Google2026d |
| https://artificialanalysis.ai/articles/aa-briefcase-time-per-task | X1 |
| https://artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v4-1 | X2 |
| https://artificialanalysis.ai/articles/gemini-3-8-flash | X3 |
| https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index | X4 |
| https://artificialanalysis.ai/methodology | X5 |
| https://artificialanalysis.ai/models/claude-opus-5-5-high | X6 |
| https://artificialanalysis.ai/models/gemini-3-8-flash | X7 |
| https://arxiv.org/abs/2307.13854 | Zhou2024 |
| https://arxiv.org/abs/2402.01869 | Abhyankar2024 |
| https://arxiv.org/abs/2405.03710 | Wornow2024 |
| https://arxiv.org/abs/2405.16444 | Yao2025a |
| https://arxiv.org/abs/2405.17438 | Singh2024 |
| https://arxiv.org/abs/2409.07429 | Wang2025a |
| https://arxiv.org/abs/2410.13825 | Yang2025 |
| https://arxiv.org/abs/2410.16464 | Song2025 |
| https://arxiv.org/abs/2412.13501 | Nguyen2025 |
| https://arxiv.org/abs/2412.14161 | Xu2025 |
| https://arxiv.org/abs/2502.08235 | Cuadron2025 |
| https://arxiv.org/abs/2503.21460 | Luo2025 |
| https://arxiv.org/abs/2504.06821 | Wang2025c |
| https://arxiv.org/abs/2504.07981 | Li2025c |
| https://arxiv.org/abs/2505.17716 | Feng2025 |
| https://arxiv.org/abs/2506.04301 | Kim2026b |
| https://arxiv.org/abs/2506.07976 | Shen2025 |
| https://arxiv.org/abs/2506.14852 | Zhang2025 |
| https://arxiv.org/abs/2506.16042 | Abhyankar2026 |
| https://arxiv.org/abs/2506.21506 | Gou2025 |
| https://arxiv.org/abs/2507.02825 | Zhu2025 |
| https://arxiv.org/abs/2510.11977 | Kapoor2026 |
| https://arxiv.org/abs/2510.12872 | Ye2025 |
| https://arxiv.org/abs/2511.21398 | Zhang2026f |
| https://arxiv.org/abs/2512.04123 | Pan2026a |
| https://arxiv.org/abs/2512.15834 | Nichols2025 |
| https://arxiv.org/abs/2601.06007 | Lumer2026 |
| https://arxiv.org/abs/2601.10088 | Aubakirova2026 |
| https://arxiv.org/abs/2601.15335 | Zhai2026b |
| https://arxiv.org/abs/2601.16746 | Wang2026c |
| https://arxiv.org/abs/2601.22037 | Abuzakuk2026 |
| https://arxiv.org/abs/2603.16104 | Wadlom2026 |
| https://arxiv.org/abs/2605.29397 | Enomoto2026 |
| https://arxiv.org/abs/2606.02964 | Shi2026 |
| https://arxiv.org/abs/2607.21604 | Pandey2026 |
| https://arxiv.org/abs/2607.28399 | Dong2026c |
| https://arxiv.org/abs/2608.14624 | Zhang2026e |
| https://arxiv.org/html/2307.13854v4 | Zhou2024 |
| https://arxiv.org/html/2310.05915v1 | Chen2023 |
| https://arxiv.org/html/2311.12983v1 | Mialon2024 |
| https://arxiv.org/html/2312.07104v2 | Zheng2024 |
| https://arxiv.org/html/2403.02694v4 | Gill2025 |
| https://arxiv.org/html/2403.07718v5 | Drouin2024 |
| https://arxiv.org/html/2404.07972 | Xie2024 |
| https://arxiv.org/html/2404.07972v2 | Xie2024 |
| https://arxiv.org/html/2405.15793v2 | Yang2024 |
| https://arxiv.org/html/2406.12045v1 | Yao2025b |
| https://arxiv.org/html/2407.00023v2 | Srivatsa2025 |
| https://arxiv.org/html/2407.01489v2 | Xia2025 |
| https://arxiv.org/html/2407.01502 | Kapoor2025 |
| https://arxiv.org/html/2407.01502v1 | Kapoor2025 |
| https://arxiv.org/html/2407.05291v2 | Boisvert2024 |
| https://arxiv.org/html/2411.00640v1 | Miller2024 |
| https://arxiv.org/html/2412.05467v4 | DeChezelles2025 |
| https://arxiv.org/html/2412.07017v1 | Gim2024 |
| https://arxiv.org/html/2412.18116v3 | Wen2025 |
| https://arxiv.org/html/2503.02268v2 | Jiang2025 |
| https://arxiv.org/html/2503.06470v1 | Tang2025 |
| https://arxiv.org/html/2503.14499v4 | Kwa2025 |
| https://arxiv.org/html/2504.01382v4 | Xue2025 |
| https://arxiv.org/html/2504.07079v1 | Zheng2025 |
| https://arxiv.org/html/2504.12516v1 | Wei2025 |
| https://arxiv.org/html/2504.13359v2 | Erol2026 |
| https://arxiv.org/html/2504.14603v2 | Zhang2026h |
| https://arxiv.org/html/2505.15810v2 | Zhou2025 |
| https://arxiv.org/html/2506.04301v2 | Kim2026b |
| https://arxiv.org/html/2506.16042v1 | Abhyankar2026 |
| https://arxiv.org/html/2506.16042v2 | Abhyankar2026 |
| https://arxiv.org/html/2506.21506v2 | Gou2025 |
| https://arxiv.org/html/2507.03730v1 | Chen2025 |
| https://arxiv.org/html/2507.07400v1 | Pan2025 |
| https://arxiv.org/html/2508.02694v1 | Wang2025b |
| https://arxiv.org/html/2508.03923v3 | Song2026 |
| https://arxiv.org/html/2508.14040v2 | Lai2026 |
| https://arxiv.org/html/2508.21433v3 | Lindenbauer2025 |
| https://arxiv.org/html/2509.01920v3 | Guan2026 |
| https://arxiv.org/html/2509.14528v1 | Shome2026 |
| https://arxiv.org/html/2509.22137v1 | Lee2025 |
| https://arxiv.org/html/2509.23586v2 | Xiao2026 |
| https://arxiv.org/html/2510.00536v1 | Huang2026b |
| https://arxiv.org/html/2510.01524v1 | Prabhu2026 |
| https://arxiv.org/html/2510.03204v2 | Kerboua2026 |
| https://arxiv.org/html/2510.04371v2 | Ye2026 |
| https://arxiv.org/html/2510.04374v1 | Patwardhan2026 |
| https://arxiv.org/html/2510.11221v1 | Li2026f |
| https://arxiv.org/html/2510.16276v1 | Bian2025 |
| https://arxiv.org/html/2510.24051v1 | Gim2025 |
| https://arxiv.org/html/2510.26787v1 | Mazeika2025 |
| https://arxiv.org/html/2511.02230v7 | Li2025b |
| https://arxiv.org/html/2511.17006 | Liu2026b |
| https://arxiv.org/html/2511.17131v1 | Cristescu2025 |
| https://arxiv.org/html/2511.19663v1 | Awadallah2025 |
| https://arxiv.org/html/2512.12692 | Dihan2025 |
| https://arxiv.org/html/2512.21309v2 | Li2025a |
| https://arxiv.org/html/2601.05777v2 | Guo2026 |
| https://arxiv.org/html/2601.14192v2 | Yang2026c |
| https://arxiv.org/html/2601.22037v1 | Abuzakuk2026 |
| https://arxiv.org/html/2601.23088v1 | Zhang2026d |
| https://arxiv.org/html/2602.07359v1 | Lin2026 |
| https://arxiv.org/html/2602.12276v2 | Lee2026 |
| https://arxiv.org/html/2602.13692 | Kang2026 |
| https://arxiv.org/html/2602.13692v3 | Kang2026 |
| https://arxiv.org/html/2602.14849v2 | Mohammadi2026a |
| https://arxiv.org/html/2602.20502 | Zhong2026a |
| https://arxiv.org/html/2602.21227v1 | Zhang2026b |
| https://arxiv.org/html/2602.21548v1 | Wu2026a |
| https://arxiv.org/html/2602.23235v1 | Xu2026a |
| https://arxiv.org/html/2603.07416v1 | Zhong2026b |
| https://arxiv.org/html/2603.07915v1 | Yang2026b |
| https://arxiv.org/html/2603.10342v1 | Zhang2026a |
| https://arxiv.org/html/2603.16104v1 | Wadlom2026 |
| https://arxiv.org/html/2603.18897v1 | Sui2026 |
| https://arxiv.org/html/2603.18897v3 | Sui2026 |
| https://arxiv.org/html/2603.23749v1 | Ndzomga2026 |
| https://arxiv.org/html/2603.29231v1 | Khanal2026 |
| https://arxiv.org/html/2604.05164 | Jali2026 |
| https://arxiv.org/html/2604.05912v1 | Krumdick2026 |
| https://arxiv.org/html/2604.09718v2 | Chundru2026 |
| https://arxiv.org/html/2604.14872v1 | Chen2026c |
| https://arxiv.org/html/2604.17849v1 | GonzalezPumariega2026 |
| https://arxiv.org/html/2604.23283v1 | Zhai2026a |
| https://arxiv.org/html/2604.23941v1 | Li2026b |
| https://arxiv.org/html/2604.24039v1 | Kim2026a |
| https://arxiv.org/html/2604.24964v1 | Jang2026 |
| https://arxiv.org/html/2604.27151v1 | Wei2026 |
| https://arxiv.org/html/2605.03409 | Perera2026 |
| https://arxiv.org/html/2605.06472v1 | Zheng2026 |
| https://arxiv.org/html/2605.10380v1 | Chung2026 |
| https://arxiv.org/html/2605.12294v1 | Qin2026 |
| https://arxiv.org/html/2605.15077v1 | Feng2026 |
| https://arxiv.org/html/2605.16565v2 | Wong2026 |
| https://arxiv.org/html/2605.17320 | Huang2026d |
| https://arxiv.org/html/2605.19260v1 | Li2026a |
| https://arxiv.org/html/2605.19932v1 | Gu2026 |
| https://arxiv.org/html/2605.21470v1 | Winston2026 |
| https://arxiv.org/html/2605.22781 | Dong2026b |
| https://arxiv.org/html/2605.22781v1 | Dong2026b |
| https://arxiv.org/html/2605.22781v2 | Dong2026b |
| https://arxiv.org/html/2605.24785v2 | Li2026c |
| https://arxiv.org/html/2605.26297v1 | Yuan2026a |
| https://arxiv.org/html/2605.26546v1 | Huang2026c |
| https://arxiv.org/html/2606.02483 | Mohammadi2026b |
| https://arxiv.org/html/2606.02964v1 | Shi2026 |
| https://arxiv.org/html/2606.05405v1 | Sun2026 |
| https://arxiv.org/html/2606.07846 | Fareed2026 |
| https://arxiv.org/html/2606.15017v1 | Hajimiri2026 |
| https://arxiv.org/html/2606.17016v1 | Xu2026b |
| https://arxiv.org/html/2606.17573v1 | Chen2026b |
| https://arxiv.org/html/2606.17929v1 | Li2026d |
| https://arxiv.org/html/2606.29537v2 | Yuan2026b |
| https://arxiv.org/html/2606.30560v2 | Zhu2026 |
| https://arxiv.org/html/2607.00151v1 | Pan2026b |
| https://arxiv.org/html/2607.03333 | Bai2026b |
| https://arxiv.org/html/2607.03333v1 | Bai2026b |
| https://arxiv.org/html/2607.12236v1 | Li2026e |
| https://arxiv.org/html/2607.21604v1 | Pandey2026 |
| https://arxiv.org/html/2607.23933v1 | Zhang2026g |
| https://arxiv.org/html/2607.26865v2 | Farzaneh2026 |
| https://arxiv.org/html/2607.28399 | Dong2026c |
| https://arxiv.org/html/2607.28399v1 | Dong2026c |
| https://arxiv.org/html/2608.00101v1 | Liu2026a |
| https://arxiv.org/html/2608.00881 | Chen2026a |
| https://arxiv.org/html/2608.05784v1 | Iyamu2026 |
| https://arxiv.org/html/2608.14624 | Zhang2026e |
| https://arxiv.org/html/2608.14624v1 | Zhang2026e |
| https://arxiv.org/html/2608.15127v1 | Chang2026 |
| https://arxiv.org/html/2608.29381 | Wu2026b |
| https://arxiv.org/html/2609.02042v1 | Yang2026a |
| https://arxiv.org/html/2609.02309v1 | Bai2026a |
| https://arxiv.org/html/2609.03236v1 | Liu2026d |
| https://arxiv.org/html/2609.09643v1 | He2026 |
| https://arxiv.org/html/2609.10297v1 | Wang2026d |
| https://arxiv.org/html/2609.16251v2 | Dong2026a |
| https://arxiv.org/html/2609.16635v1 | Zhao2026a |
| https://arxiv.org/html/2609.19947 | Choi2026 |
| https://arxiv.org/html/2609.24890v1 | Wang2026b |
| https://arxiv.org/pdf/2312.04511 | Kim2024 |
| https://arxiv.org/pdf/2406.18665 | Ong2025 |
| https://arxiv.org/pdf/2504.14603v2 | Zhang2026h |
| https://arxiv.org/pdf/2505.17616 | Lu2025b |
| https://arxiv.org/pdf/2506.07982 | Barres2026 |
| https://arxiv.org/pdf/2511.17131 | Cristescu2025 |
| https://arxiv.org/pdf/2601.14242v3 | Vidgen2026 |
| https://arxiv.org/pdf/2602.21548 | Wu2026a |
| https://arxiv.org/pdf/2604.01676 | Zhao2026b |
| https://arxiv.org/pdf/2605.14237v1 | Wang2026a |
| https://arxiv.org/pdf/2608.00881 | Chen2026a |
| https://arxiv.org/pdf/2608.05784 | Iyamu2026 |
| https://arxiv.org/pdf/2608.11338 | Huang2026a |
| https://arxiv.org/pdf/2609.19607 | Conn2026 |
| https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/ | X35 |
| https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/ | X33 |
| https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/ | X34 |
| https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-computer-use-gemini-3-5-flash/ | X32 |
| https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-computer-use-model/ | X31 |
| https://blog.google/innovation-and-ai/sundar-pichai-io-2026/ | X36 |
| https://blog.google/innovation-and-ai/technology/developers-tools/introducing-flex-and-priority-inference/ | X37 |
| https://browser-use.com/benchmarks/agents | X11 |
| https://browser-use.com/posts/ai-browser-agent-benchmark | X10 |
| https://browser-use.com/posts/llm-gateway | X8 |
| https://browser-use.com/posts/speed-matters | X9 |
| https://cdn.openai.com/pdf/5d1e1489-21c0-43e4-9d42-f87efdbf0082/the-shift-to-agentic-ai-evidence-from-codex.pdf | Johnston2026 |
| https://claude.com/blog/best-practices-for-computer-and-browser-use-with-claude | Anthropic2026g |
| https://colmweb.org/2025/AcceptedPapers.html | Wang2025c |
| https://community.automationanywhere.com/generative-recorder-85080/generative-recorder-and-resilient-automation-april-2024-88211 | X39 |
| https://community.openai.com/t/ultrafast-mode-preview-gpt-5-6-sol-at-up-to-14x-the-speed-in-the-api/1390344 | X27 |
| https://crad.ict.ac.cn/en/article/doi/10.7544/issn1000-1239.202440380 | Li2025a |
| https://developers.openai.com/api/docs/changelog | OpenAI2026d |
| https://developers.openai.com/api/docs/guides/flex-processing | OpenAI2026b |
| https://developers.openai.com/api/docs/guides/priority-processing | OpenAI2026a |
| https://developers.openai.com/api/docs/guides/prompt-caching | OpenAI2026e |
| https://developers.openai.com/api/docs/pricing | OpenAI2026c |
| https://developers.openai.com/cookbook/examples/prompt_caching_201 | OpenAI2026f |
| https://docs.automationanywhere.com/r/automation-360/generative-ai-based-fallback | AutomationAnywhere2026a |
| https://docs.automationanywhere.com/r/automation-360/gr-overview | AutomationAnywhere2026b |
| https://docs.browser-use.com/cloud/agent/cache-script | BrowserUse2026a |
| https://docs.browser-use.com/concepts/skills | BrowserUse2026b |
| https://docs.stagehand.dev/v3/best-practices/caching | Browserbase2026a |
| https://docs.uipath.com/activities/other/latest/ui-automation/screenplay | UiPath2026c |
| https://docs.uipath.com/agents/automation-cloud/latest/user-guide-ha/licensing | UiPath2026b |
| https://docs.uipath.com/agents/automation-cloud/latest/user-guide-ha/what-is-healing-agent | UiPath2026a |
| https://github.com/Hanchenli/vllm-continuum | Li2025b |
| https://github.com/JackZhao1998/EchoPath | Zhao2026a |
| https://github.com/JackZhao1998/EchoPath.git | Zhao2026a |
| https://github.com/SEED-VT/MeanCache | Gill2025 |
| https://github.com/ThunderAgent-org/ThunderAgent | Kang2026 |
| https://github.com/WukLab/osworld-human | Abhyankar2026 |
| https://github.com/argszero/silicon-science-cs/issues/50 | X52 |
| https://github.com/browser-use/workflow-use | BrowserUse2025 |
| https://github.com/dongyunpeng-sjtu/deltabox | Dong2026b |
| https://github.com/hyperbrowserai/HyperAgent | Hyperbrowser2026 |
| https://github.com/mlsys-io/helium_demo | Wadlom2026 |
| https://github.com/xlang-ai/OSWorld | Xie2024 |
| https://github.com/zjunlp/LightMem2 | Xu2026b |
| https://hal.cs.princeton.edu/ | Kapoor2026 |
| https://hal.cs.princeton.edu/online_mind2web | Kapoor2026 |
| https://help.openai.com/en/articles/11752874-chatgpt-agent | OpenAI2026g |
| https://help.openai.com/en/articles/11794368-chatgpt-agent-release-notes | OpenAI2026h |
| https://iclr.cc/virtual/2026/oral/10009727 | Ye2026 |
| https://iclr.cc/virtual/2026/poster/10006806 | Kapoor2026 |
| https://iclr.cc/virtual/2026/poster/10007435 | Lai2026 |
| https://iclr.cc/virtual/2026/poster/10008481 | Prabhu2026 |
| https://icml.cc/virtual/2026/poster/61834 | Pan2026a |
| https://icml.cc/virtual/2026/poster/62040 | Kang2026 |
| https://jmlr.org/tmlr/papers/ | Kerboua2026 |
| https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/priority-processing | Microsoft2026a |
| https://learn.microsoft.com/en-us/power-automate/desktop-flows/self-healing | Microsoft2026b |
| https://learn.microsoft.com/en-us/power-automate/desktop-flows/ui-elements-fallback-mechanism | Microsoft2026c |
| https://learn.microsoft.com/en-us/power-automate/faqs-repair-copilot | Microsoft2026d |
| https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise/ | MenloVentures2025 |
| https://mlanthology.org/iclr/2026/erol2026iclr-costofpass/ | Erol2026 |
| https://mlanthology.org/tmlr/2025/kapoor2025tmlr-ai/ | Kapoor2025 |
| https://neurips.cc/virtual/2025/poster/115164 | Ye2025 |
| https://nvidianews.nvidia.com/news/nvidia-groq-3-lpx-now-in-full-production-with-world-class-speed-for-agentic-ai | X19 |
| https://ojs.aaai.org/index.php/AAAI/article/view/40772 | Zhang2026f |
| https://openaccess.thecvf.com/content/CVPR2025/html/Lin_ShowUI_One_Vision-Language-Action_Model_for_GUI_Visual_Agent_CVPR_2025_paper.html | Lin2025 |
| https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/ | X20 |
| https://openai.com/index/computer-using-agent/ | OpenAI2025 |
| https://openai.com/index/gdpval/ | Patwardhan2026 |
| https://openai.com/index/gpt-6-astra/ | X25 |
| https://openai.com/index/introducing-chatgpt-agent/ | X22 |
| https://openai.com/index/introducing-gpt-5-for-developers/ | X24 |
| https://openai.com/index/introducing-operator/ | X23 |
| https://openai.com/index/introducing-the-agents-api/ | X21 |
| https://openai.com/index/previewing-ultrafast/ | X26 |
| https://openreview.net/pdf?id=Kdc8aiKxF6 | Jin2025 |
| https://openreview.net/pdf?id=lsAY6fWsog | Wang2025c |
| https://openrouter.ai/ | OpenRouter2026c |
| https://openrouter.ai/blog/insights/deepseek-v4-adoption/ | OpenRouter2026a |
| https://openrouter.ai/blog/insights/gpt-5-6-discounts-jevons-paradox/ | OpenRouter2026b |
| https://openrouter.ai/state-of-ai | Aubakirova2026 |
| https://osu-nlp-group.github.io/Mind2Web-2/ | Gou2025 |
| https://osworld-v2.xlang.ai/ | Yuan2026b |
| https://papers.nips.cc/paper_files/paper/2025/file/0d744742f6fac4d1134c019b7cef3c8a-Paper-Datasets_and_Benchmarks_Track.pdf | Xu2025 |
| https://pasqualepillitteri.it/en/news/346/claude-chrome-quick-mode-fast-browsing-guide | X49 |
| https://platform.claude.com/docs/en/about-claude/pricing | Anthropic2026b |
| https://platform.claude.com/docs/en/api/service-tiers | Anthropic2026f |
| https://platform.claude.com/docs/en/build-with-claude/effort | Anthropic2026d |
| https://platform.claude.com/docs/en/build-with-claude/fast-mode | Anthropic2026a |
| https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages | Anthropic2026e |
| https://platform.claude.com/docs/en/build-with-claude/prompt-caching | Anthropic2026c |
| https://proceedings.iclr.cc/paper_files/paper/2025/file/25458943db16e0f78f748ca5bc34fff6-Paper-Conference.pdf | Hua2025 |
| https://proceedings.mlr.press/v235/abhyankar24a.html | Abhyankar2024 |
| https://proceedings.mlsys.org/paper_files/paper/2026/file/5edb57c05c81d04beb716ef1d542fe9e-Paper-Conference.pdf | Abhyankar2026 |
| https://sambanova.ai/blog/first-disaggregated-inference-demo-for-ai-agents-live | X18 |
| https://sambanova.ai/blog/the-premium-inference-moment-is-here | X17 |
| https://skyvern.mintlify.app/developers/optimization/cost-control | Skyvern2026b |
| https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome | Anthropic2026i |
| https://support.claude.com/en/articles/12138966-release-notes | Anthropic2026h |
| https://temporal.io/reports/state-of-development-2026 | Temporal2026 |
| https://the-decoder.com/ai-is-becoming-ais-biggest-customer-as-agentic-token-usage-jumps-14x-on-openrouter/ | X42 |
| https://the-decoder.com/openrouters-staggering-token-chart-is-the-ai-bubble-debate-in-a-single-image/ | X43 |
| https://tokencost.app/blog/llm-fast-mode-latency-pricing | X48 |
| https://tracelab.cs.washington.edu | Zhu2026 |
| https://www.alphaxiv.org/abs/2607.22689 | Yu2026 |
| https://www.anthropic.com/claude/opus | X30 |
| https://www.anthropic.com/engineering/multi-agent-research-system | Hadfield2025 |
| https://www.anthropic.com/news/claude-opus-4-5 | X28 |
| https://www.anthropic.com/news/claude-opus-4-8 | X29 |
| https://www.automationanywhere.com/products/automator-ai | X38 |
| https://www.browserbase.com/blog/stagehand-caching | X12 |
| https://www.browserbase.com/blog/stagehand-v3 | X13 |
| https://www.browserbase.com/blog/training-computer-use-models-in-the-real-world-with-microsoft | X14 |
| https://www.browserbase.com/changelog | Browserbase2026c |
| https://www.browserbase.com/pricing | Browserbase2026b |
| https://www.cerebras.ai/blog/accelerating-gpt-5-6-sol-ultrafast-with-openai | X15 |
| https://www.cerebras.ai/blog/the-rise-of-slow-personal-assistants | X16 |
| https://www.datacamp.com/blog/gpt-6-astra | X50 |
| https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027 | Gartner2025 |
| https://www.gartner.com/en/newsroom/press-releases/2026-03-25-gartner-predicts-that-by-2030-performing-inference-on-an-llm-with-1-trillion-parameters-will-cost-genai-providers-over-90-percent-less-than-in-2025 | Gartner2026a |
| https://www.gartner.com/en/newsroom/press-releases/2026-04-07-gartner-says-artificial-intelligence-projects-in-infrastructure-and-operations-stall-ahead-of-meaningful-roi-returns | Gartner2026b |
| https://www.gartner.com/en/newsroom/press-releases/2026-08-17-gartner-predicts-ai-inference-costs-per-agentic-workflow-will-increase-more-than-fivefold-through-2028 | Gartner2026c |
| https://www.humansecurity.com/learn/resources/2026-state-of-ai-traffic-cyberthreat-benchmarks/ | HUMANSecurity2026 |
| https://www.humansecurity.com/newsroom/2026-state-of-ai-traffic-cyberthreat-benchmark-report/ | HUMANSecurity2026 |
| https://www.hyperbrowser.ai/docs/hyperagent/action-cache | Hyperbrowser2026 |
| https://www.langchain.com/state-of-agent-engineering | LangChain2026 |
| https://www.linkedin.com/feed/update/urn:li:activity:7493029883191681024/ | X44 |
| https://www.linkedin.com/feed/update/urn:li:activity:7506103118410072064/ | X45 |
| https://www.microsoft.com/en-us/research/articles/webwright-a-terminal-is-all-you-need-for-web-agents/ | Lu2026 |
| https://www.microsoft.com/en-us/research/blog/fara-7b-an-efficient-agentic-model-for-computer-use/ | Awadallah2025 |
| https://www.notte.cc/blog/browser-agent-stack-2026 | X41 |
| https://www.preprints.org/manuscript/202608.0365 | Hu2026 |
| https://www.skyvern.com/docs/developers/features/code-caching | Skyvern2026a |
| https://www.uipath.com/blog/product-and-updates/technical-tuesday-how-healing-agent-solves-ui-automation-challenges | X40 |
| https://www.usenix.org/conference/nsdi26/presentation/liu-yuhan | Liu2026c |
| https://www.usenix.org/conference/osdi24/presentation/lin-chaofan | Lin2024 |
| https://www.usenix.org/system/files/nsdi26-luo.pdf | Luo2026 |
| https://www.usenix.org/system/files/osdi24-lin-chaofan.pdf | Lin2024 |
| https://www.vellum.ai/blog/gpt-6-astra-benchmarks-explained | X51 |
| https://x.com/gabemulley/status/2026041548429828101 | X46 |
| https://x.com/trq212/status/2026110215561822374 | X47 |

## Row map

Every E and D row with the keys it relies on. `slides/check_references.py` reads this table.

| Row | Keys | Excluded sources |
|---|---|---|
| D1 | — | X8, X9 |
| D2 | Yuan2026b |  |
| D3 | Yuan2026b |  |
| D4 | Yuan2026b |  |
| D5 | Abhyankar2026 |  |
| D6 | Abhyankar2026 |  |
| D7 | Abhyankar2026 |  |
| D8 | Kim2026b, Yuan2026b |  |
| D9 | Wang2025b |  |
| D10 | Zhang2025 |  |
| D11 | Li2026e |  |
| D12 | — |  |
| D13 | Sui2026 |  |
| D14 | Kang2026, Li2025b, Yang2024 |  |
| D15 | Drouin2024, Kerboua2026 |  |
| D16 | Zhu2026 |  |
| D17 | Xu2025 |  |
| D18 | OpenRouter2026a |  |
| D19 | OpenRouter2026a |  |
| D20 | Gartner2026a |  |
| D21 | OpenRouter2026a |  |
| D22 | Anthropic2026b, OpenAI2026c |  |
| D23 | Ye2026 |  |
| D24 | LangChain2026 |  |
| D25 | Pan2026a |  |
| D26 | Kapoor2025 |  |
| D27 | Yao2025b |  |
| D28 | — | X34 |
| D29 | OpenAI2026h |  |
| D30 | Boisvert2024 |  |
| D31 | Kapoor2026 |  |
| D32 | Yuan2026b |  |
| D33 | OpenAI2025, Xie2024, Zhou2024 |  |
| D34 | — |  |
| D35 | Kim2026b |  |
| D36 | Yuan2026a |  |
| D37 | Xu2025 |  |
| D38 | Yuan2026b |  |
| D39 | Abhyankar2026 |  |
| D40 | — | X8 |
| D41 | DeChezelles2025, Wang2025a, Wang2025c |  |
| D42 | Prabhu2026 |  |
| D43 | Winston2026 |  |
| D44 | Jiang2025 |  |
| D45 | Abuzakuk2026, Zhou2024 |  |
| D46 | Xie2024, Yuan2026b, Zhang2026h |  |
| D47 | Wei2026, Xie2024 |  |
| D48 | Kerboua2026, Zhou2024 |  |
| D49 | Yang2026b, Zhou2024 |  |
| D50 | Jali2026 |  |
| D51 | Ye2026 |  |
| D52 | Luo2026 |  |
| D53 | Kerboua2026 |  |
| D54 | Awadallah2025 |  |
| D55 | Li2025b, Zhang2026e |  |
| D56 | Abhyankar2026 |  |
| D57 | Kim2026b |  |
| D58 | Drouin2024, Kerboua2026, Zhou2024 |  |
| D59 | Drouin2024, Kerboua2026 |  |
| D60 | Drouin2024, Kerboua2026 |  |
| D61 | Li2025b, Yang2024 |  |
| D62 | Kang2026, Li2025b |  |
| D63 | Luo2026, Sui2026 |  |
| D64 | Sui2026 |  |
| D65 | Zhu2026 |  |
| D66 | Zhu2026 |  |
| D67 | Zhu2026 |  |
| D68 | Gartner2026a |  |
| D69 | Gartner2026b |  |
| D70 | OpenRouter2026a |  |
| D71 | — | X42, X44 |
| D72 | OpenRouter2026a |  |
| D73 | Yuan2026a |  |
| D74 | Google2026a, Google2026b | X3, X7 |
| D75 | Google2026b |  |
| D76 | OpenAI2026h |  |
| D77 | Anthropic2026e |  |
| D78 | Temporal2026 |  |
| D79 | Pan2026a |  |
| D80 | Pan2026a |  |
| D81 | Pan2026a |  |
| D82 | Zhao2026a |  |
| D83 | Xie2024, Zhao2026a |  |
| D84 | Zhao2026a |  |
| D85 | Zhao2026a |  |
| D86 | Abuzakuk2026 |  |
| D87 | Wei2025, Yang2026b, Zhou2024 |  |
| D88 | Dong2026c |  |
| D89 | Yang2026a |  |
| D90 | Ye2026 |  |
| D91 | Awadallah2025 |  |
| D92 | Lu2025a |  |
| D93 | Lai2026 |  |
| D94 | Ye2025 |  |
| D95 | Abhyankar2026, Chang2026, Xie2024 |  |
| D96 | Chang2026, Winston2026, Wong2026 |  |
| D97 | Winston2026 |  |
| D98 | Bian2025 |  |
| D99 | Yuan2026a, Zhu2026 |  |
| D100 | Kang2026 |  |
| D101 | Abhyankar2026 |  |
| D102 | Dong2026b |  |
| D103 | Bai2026b, Chen2026a, Guan2026, Liu2026d, Sui2026, Ye2026 |  |
| D104 | Dihan2025, Mohammadi2026a, Xie2024, Zhou2024 |  |
| D105 | Chen2026b |  |
| D106 | Bai2026b, Fareed2026, Li2026e, Mohammadi2026b |  |
| D107 | Mohammadi2026a, Perera2026, Wu2026b |  |
| D108 | Liu2026d |  |
| D109 | Fareed2026 |  |
| D110 | Chundru2026, Hyperbrowser2026, Wang2026a |  |
| D111 | Wang2026a |  |
| D112 | Hyperbrowser2026, Iyamu2026, Wang2026a |  |
| D113 | Browserbase2026a, Chundru2026, Microsoft2026b, UiPath2026a |  |
| D114 | Browserbase2026a |  |
| D115 | AutomationAnywhere2026a, Browserbase2026a, Hyperbrowser2026, Skyvern2026a |  |
| D116 | Cristescu2025, Dong2026a, Gou2025, Krumdick2026, Kwa2025, Lu2025a, Vidgen2026, Xie2024, Zhou2024 |  |
| D117 | Xie2024, Zhou2024 |  |
| D118 | Gou2025 |  |
| D119 | Dong2026a, Drouin2024, Krumdick2026, Lu2025a, Patwardhan2026, Xie2024, Yuan2026b, Zhou2024 |  |
| D120 | Vidgen2026 |  |
| D121 | Dong2026a, Gou2025, Krumdick2026, Lu2025a, Patwardhan2026 |  |
| D122 | Li2025b, Zhang2026e |  |
| D123 | Zhang2026e |  |
| D124 | Xu2026b |  |
| D125 | Gu2026 |  |
| D126 | Dong2026b |  |
| D127 | He2026, Huang2026b, Liu2026c, Pandey2026, Shi2026, Wu2026a, Ye2025, Zhang2026a, Zheng2026 |  |
| D128 | Luo2026 |  |
| D129 | Kang2026, Li2025b |  |
| D130 | He2026 |  |
| D131 | Microsoft2026a |  |
| D132 | OpenAI2026a, OpenAI2026c, OpenAI2026d |  |
| D133 | Xue2025 | X8, X31 |
| D134 | Google2026a, Google2026b | X4 |
| D135 | Browserbase2026a, Browserbase2026c, Patwardhan2026 |  |
| D136 | Anthropic2026h, Anthropic2026i |  |
| D137 | Anthropic2026a, Anthropic2026f, Google2026c, Google2026d, Microsoft2026a, OpenAI2026a, OpenAI2026b, OpenAI2026c, OpenAI2026d |  |
| D138 | Browserbase2026a |  |
| D139 | AutomationAnywhere2026a, Browserbase2026a, Hyperbrowser2026, Microsoft2026a, Skyvern2026a, UiPath2026a |  |
| D140 | Dong2026b |  |
| E1 | Abhyankar2026 |  |
| E2 | Abhyankar2026 |  |
| E3 | Abhyankar2026, Xie2024 |  |
| E4 | Abhyankar2026 |  |
| E5 | Xie2024, Yuan2026b |  |
| E6 | Xie2024, Yuan2026b |  |
| E7 | Xie2024, Yuan2026b |  |
| E8 | Yuan2026b |  |
| E9 | Yuan2026b |  |
| E10 | Xu2025 |  |
| E11 | DeChezelles2025, Drouin2024, Zhou2024 |  |
| E12 | Xie2024, Zhou2024 |  |
| E13 | Xue2025 |  |
| E14 | Gou2025 |  |
| E15 | Cristescu2025 |  |
| E16 | Boisvert2024, Drouin2024, Zhou2024 |  |
| E17 | Wong2026, Yang2025 |  |
| E18 | Winston2026, Zhou2024 |  |
| E19 | Zhu2026 |  |
| E20 | Liu2026a, Zhu2026 |  |
| E21 | — | X22 |
| E22 | Abhyankar2026, Xie2024, Zheng2024 |  |
| E23 | Abhyankar2026 |  |
| E24 | Abhyankar2026, Xie2024 |  |
| E25 | Abhyankar2026 |  |
| E26 | DeChezelles2025, Zhou2024 |  |
| E27 | Bian2025 |  |
| E28 | Chang2026, Sui2026 |  |
| E29 | Mialon2024, Yuan2026a |  |
| E30 | Drouin2024, Kerboua2026 |  |
| E31 | Anthropic2026g |  |
| E32 | — | X9 |
| E33 | — |  |
| E34 | — |  |
| E35 | Pan2026b |  |
| E36 | Xue2025 | X8, X9 |
| E37 | Xue2025 | X31 |
| E38 | Anthropic2026i |  |
| E39 | OpenAI2025, OpenAI2026g, OpenAI2026h, Xie2024, Zhou2024 | X22 |
| E40 | Yuan2026b |  |
| E41 | Yuan2026b |  |
| E42 | Yuan2026b |  |
| E43 | Kapoor2026, Xue2025 |  |
| E44 | Lee2026, Zhou2024 |  |
| E45 | Abhyankar2026 |  |
| E46 | Lu2026, Xue2025 |  |
| E47 | — | X10, X11 |
| E48 | Mialon2024, Wang2025b |  |
| E49 | Kim2026b |  |
| E50 | Jin2025 |  |
| E51 | Xia2025, Yang2024 |  |
| E52 | Erol2026 |  |
| E53 | Kapoor2025 |  |
| E54 | Barres2026, Yao2025b |  |
| E55 | Gartner2026c |  |
| E56 | Aubakirova2026 |  |
| E57 | OpenRouter2026a |  |
| E58 | — | X42, X44 |
| E59 | — | X43, X45 |
| E60 | Hadfield2025 |  |
| E61 | Johnston2026 |  |
| E62 | Gartner2026a |  |
| E63 | — | X36 |
| E64 | — |  |
| E65 | HUMANSecurity2026 |  |
| E66 | MenloVentures2025 |  |
| E67 | — |  |
| E68 | LangChain2026 |  |
| E69 | Pan2026a |  |
| E70 | Temporal2026 |  |
| E71 | Shome2026 |  |
| E72 | Gartner2025 |  |
| E73 | Gartner2026b |  |
| E74 | Aubakirova2026 |  |
| E75 | — |  |
| E76 | Anthropic2026a, Microsoft2026a | X30 |
| E77 | OpenAI2026a, OpenAI2026b, OpenAI2026c, OpenAI2026d | X20, X27 |
| E78 | Microsoft2026a |  |
| E79 | Google2026a, Google2026b | X3, X7, X32, X33, X34, X35 |
| E80 | Anthropic2026h, Anthropic2026i |  |
| E81 | Anthropic2026g |  |
| E82 | — | X21 |
| E83 | Anthropic2026e | X29 |
| E84 | Anthropic2026c, Lumer2026, OpenAI2026f |  |
| E85 | — | X8, X9 |
| E86 | Anthropic2026b |  |
| E87 | Browserbase2026a, Browserbase2026c | X13, X15, X17, X19 |
| E88 | Anthropic2026d, Kapoor2026 | X24, X28 |
| E89 | Kapoor2025 |  |
| E90 | Awadallah2025, OpenRouter2026c, Xue2025 | X14 |
| E91 | Xie2024, Zhao2026a |  |
| E92 | Zhao2026a |  |
| E93 | Abuzakuk2026 |  |
| E94 | Xie2024, Zhang2026h |  |
| E95 | Dong2026c |  |
| E96 | Huang2026c |  |
| E97 | Chang2026, Xie2024 |  |
| E98 | Chang2026, Zhou2024 |  |
| E99 | Chang2026 |  |
| E100 | Winston2026 |  |
| E101 | Winston2026 |  |
| E102 | Choi2026 |  |
| E103 | Choi2026 |  |
| E104 | Choi2026 |  |
| E105 | Zhu2026 |  |
| E106 | Liu2026a |  |
| E107 | Mialon2024, Yuan2026a |  |
| E108 | Kang2026 |  |
| E109 | — | X1 |
| E110 | Zhu2026 |  |
| E111 | Abhyankar2026, Xie2024 |  |
| E112 | Abhyankar2026, OpenAI2026e |  |
| E113 | Mohammadi2026a |  |
| E114 | Mohammadi2026a, Xie2024, Yao2025b, Zhou2024 |  |
| E115 | Mohammadi2026a, Xie2024, Yao2025b, Zhou2024 |  |
| E116 | Mohammadi2026a, Xie2024, Yao2025b, Zhou2024 |  |
| E117 | Chen2026b |  |
| E118 | Chen2026b |  |
| E119 | Chen2026b, Yao2025b |  |
| E120 | Chen2026b, Yao2025b |  |
| E121 | Huang2026d |  |
| E122 | Dong2026b |  |
| E123 | Chen2026a, Dong2026b |  |
| E124 | Liu2026d |  |
| E125 | Liu2026d |  |
| E126 | Ye2026 |  |
| E127 | Sui2026 |  |
| E128 | Bai2026b, Mialon2024 |  |
| E129 | Mohammadi2026a, Mohammadi2026b |  |
| E130 | Mohammadi2026a, Mohammadi2026b |  |
| E131 | Fareed2026 |  |
| E132 | Zhao2026a |  |
| E133 | Dihan2025, Zhou2024 |  |
| E134 | Dong2026c |  |
| E135 | Zhai2026a |  |
| E136 | Wu2026b |  |
| E137 | Barres2026, Perera2026 |  |
| E138 | Bai2026b, Fareed2026, Liu2026d, Zhang2026g | X52 |
| E139 | Hyperbrowser2026 |  |
| E140 | Wang2026a |  |
| E141 | Wang2026a |  |
| E142 | Wang2026a |  |
| E143 | Wang2026a |  |
| E144 | Iyamu2026 |  |
| E145 | Chundru2026 |  |
| E146 | UiPath2026a | X40 |
| E147 | UiPath2026a, UiPath2026b |  |
| E148 | UiPath2026a, UiPath2026c, Wornow2024 |  |
| E149 | AutomationAnywhere2026a, AutomationAnywhere2026b | X39 |
| E150 | AutomationAnywhere2026a | X38 |
| E151 | Microsoft2026b |  |
| E152 | Microsoft2026c, Microsoft2026d |  |
| E153 | Browserbase2026a | X12 |
| E154 | Browserbase2026a | X12, X13 |
| E155 | Browserbase2026b |  |
| E156 | BrowserUse2026a, BrowserUse2026b |  |
| E157 | BrowserUse2025 |  |
| E158 | Hyperbrowser2026, Skyvern2026a, Skyvern2026b |  |
| E159 | — | X41 |
| E160 | AutomationAnywhere2026a, Hyperbrowser2026, Skyvern2026a, UiPath2026a |  |
| E161 | Lu2025a |  |
| E162 | Dong2026a |  |
| E163 | Krumdick2026 |  |
| E164 | Patwardhan2026 |  |
| E165 | Patwardhan2026 |  |
| E166 | Kwa2025 |  |
| E167 | Krumdick2026, Vidgen2026 |  |
| E168 | Sun2026 |  |
| E169 | Wei2025 |  |
| E170 | Mialon2024 |  |
| E171 | Mazeika2025 |  |
| E172 | Li2025b, Mialon2024, Zhang2026e |  |
| E173 | Lin2024, Pan2025, Wadlom2026, Zheng2024 |  |
| E174 | Xu2026b |  |
| E175 | Gu2026 |  |
| E176 | Zhang2026g |  |
| E177 | Dong2026b |  |
| E178 | Li2025b, Shi2026 |  |
| E179 | Pandey2026, Yao2025a |  |
| E180 | Wu2026a, Zheng2024 |  |
| E181 | He2026, Mialon2024, Zhang2026e |  |
| E182 | Pan2025, Zheng2024, Zheng2026 |  |
| E183 | Zhang2026a, Zheng2024 |  |
| E184 | Abhyankar2024, Kang2026, Li2025b, Zheng2024 |  |
| E185 | Luo2026, Srivatsa2025, Zhou2024 |  |
| E186 | Kang2026, Li2025b, Zheng2024 |  |
| E187 | Li2025b, Zhu2026 |  |
| E188 | Gill2025, Li2025a |  |
| E189 | Abhyankar2024, He2026, Kang2026, Li2025b, Mialon2024, Shi2026, Zhang2026e, Zheng2024 |  |
| E190 | Anthropic2026a, Microsoft2026a |  |
| E191 | Anthropic2026f |  |
| E192 | OpenAI2026a, OpenAI2026c, OpenAI2026d |  |
| E193 | OpenAI2026b |  |
| E194 | OpenAI2026d | X26, X27 |
| E195 | Patwardhan2026 | X15 |
| E196 | Microsoft2026a |  |
| E197 | Google2026c, Google2026d | X37 |
| E198 | Google2026a, Google2026c |  |
| E199 | Xue2025 | X31 |
| E200 | Yuan2026b | X25, X50, X51 |
| E201 | — | X16 |
| E202 | — | X10 |
| E203 | Browserbase2026a, Browserbase2026c | X13 |
| E204 | — | X19 |
| E205 | — | X17, X18 |
| E206 | OpenAI2026d, Patwardhan2026 |  |
| E207 | — | X2, X4 |
| E208 | — | X5, X6 |
| E209 | Microsoft2026a | X48 |
| E210 | Anthropic2026h, Anthropic2026i | X46, X47, X49 |
| E211 | OpenRouter2026b |  |
