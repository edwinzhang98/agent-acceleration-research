# Claude survey mining reader

Builds `notes/part3/2026-09-30-self-improvement-survey-mining-zh.html` from the matching Markdown and full repository evidence ledger. The Markdown stays unchanged.

The HTML has six reading views: guide, complete report, audit, evidence, screening and bibliography. Dense comparison rows can be expanded or switched back to tables. It embeds KaTeX fonts and server-rendered math, needs no CDN, and works as a local file. Paper links still require the internet.

## Inputs and audit boundary

- `audit.json`: 18 review records D595–D612, with exact sequential replacement text. A fact patch must match exactly once or the build fails. Original and revised text appear together in the audit view.
- `math-replacements.json`: 75 presentation-only substitutions for originally unmarked equations and symbols. No model/paper claims are inferred by the renderer. Skipped formatting replacements are listed in the manifest and should be resolved before release.
- `audit-references.md`: complete authors, actual versions and scope for 26 primary sources checked by the review team. This supplements, rather than overwrites, the original 88 bibliography records.
- `research/2026-09-30-claude-survey-review.md` and four supporting audit files explain the evidence and remaining limitations. Original “read/audited” labels are not a claim of a new full audit of all 82 cited papers.

The appendix contains 421 candidate summary entries, but only 336 detailed screening rows; 85 deep-read/reused main entries were intentionally omitted from that detail table. These units are labelled separately. All 645 new-batch evidence records are included, plus six older cross-batch citations. Evidence dialogs pull full ledger fields rather than only the truncated appendix summaries.

## Build and verify

Use Node with `marked` and `playwright` installed. Set `SURVEY_READER_NODE_MODULES` if not using the configured Codex runtime. KaTeX 0.16.11 and its MIT license are reused from `../survey-reader/vendor/katex`.

```sh
node tools/survey-mining-reader/build.mjs
node tools/survey-mining-reader/verify.mjs
python3 tools/survey-mining-reader/serve.py
```

`SURVEY_READER_QA_DIR` defaults to `/private/tmp/survey-mining-reader-qa`. Build writes normalized content fixtures there; verification writes screenshots and a result JSON. These temporary files are not part of the deliverable.

Verification compares every prose/list/table block in all ten chapters and all 88 bibliography entries against the fully transformed source. It checks evidence dialogs, table/card switching, search, pagination, mobile navigation, print visibility, and page overflow at 1440 / 768 / 390 / 320 px. All HTTP(S) requests are blocked during verification; zero external requests and zero JavaScript errors are required. The 645 evidence count and 88 reference count are guarded at build time. All rendered TeX is compiled with errors treated as failures.

The loopback preview serves only the report; it does not publish the repository or expose it outside the local machine. The standalone HTML remains the portable deliverable.
