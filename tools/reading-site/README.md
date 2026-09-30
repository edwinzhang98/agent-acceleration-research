# Research reading site

Public site: <https://edwinzhang98.github.io/agent-acceleration-research/>

`docs/index.html` is the shared reading index. Reports live in `docs/reports/`; slide presentations live in `docs/slides/`. The reader-facing source documents remain in `notes/`, while `research/` holds evidence, audits, and revision records. Long-form reports are kept separate from slides.

## Included material and scope

| Material | Rendering method and status |
|---|---|
| Codex report on fixed-weight agent acceleration | Reuses the complete interactive reader from `tools/survey-reader/`, with links to the reading index and Markdown source. |
| Reviewed edition of Claude's survey report | Reuses `tools/survey-mining-reader/`, preserving its review patches, evidence lookup, and complete bibliography. This is not a new audit of every cited paper. |
| Latest report on how the literature defines the problem | Converts the full text. The source distinguishes targeted reading, anchor checks, and independent audits; its synthesis remains a discussion draft. |
| Formula reference for speed and cost | Converts the full text and renders LaTeX blocks. Prices reflect the September 28 snapshot. The source's truncated AQuaUI table row in section 6 remains incomplete; no missing text is reconstructed. |
| Codex research plan and Claude's sixth draft | Converts both documents in full and labels them as September 29 discussion drafts. They do not yet incorporate all conclusions from the September 30 follow-up review. |
| Part 1–2 slide presentation | Adds a small link to the reading index while preserving the original HTML presentation. |

The first set adds the problem-definition report, formula reference, and two plans to connect three questions: what to study, how to measure it, and what to test next. The older `research-proposal` has been superseded by the detailed plans and is not listed alongside them. The Part 1 analysis of slowness and cost and the Part 2 acceleration literature review are candidates for a later addition. The former is missing a loop diagram in its source snapshot; both require their historical versions and source rules to remain clear. Large evidence ledgers and historical dossiers remain available through repository links rather than being duplicated as individual articles.

This publishing pass does not rewrite research conclusions or modify the source Markdown. `math-formatting.json` only converts unambiguous plain-text mathematical expressions to LaTeX; prose summaries in the original evidence appendices are preserved. Known relative-link errors are corrected only when the intended target can be confirmed in the repository. HTML comments in the source are omitted from the visible article, and other raw HTML is escaped. Equations and fonts are embedded, with no external rendering CDN.

## Build and check

Use Node.js 24. The lockfile pins the Markdown dependency. KaTeX is reused from `tools/survey-reader/vendor/katex/`, and its license is retained in the generated pages.

```sh
npm ci --prefix tools/reading-site --ignore-scripts --no-audit --no-fund
node tools/reading-site/build.mjs --rebuild
node tools/reading-site/check.mjs
```

`--rebuild` rebuilds the two custom reports before generating the entire site. Running either original report generator also updates its copy in `docs/reports/`; run the full site build to refresh the reading index and hash manifest. Set `SURVEY_READER_NODE_MODULES` to use a specific directory of installed Node modules, or `SURVEY_READER_QA_DIR` to choose the directory for intermediate verification output.

`catalog.json` defines titles, sources, status labels, and output paths. New entries can point to Markdown or reuse an existing custom HTML report through `htmlSource`. `site-manifest.json` records hashes for the Markdown source, original HTML, and published output, together with math-formatting and document-structure statistics. If source changes cause an exact math-formatting replacement to stop matching, the build fails so the formatting change cannot silently disappear.

Optional browser checks require Playwright and Chromium to be installed:

```sh
PLAYWRIGHT_NODE_MODULES=/path/to/node_modules node tools/reading-site/verify.mjs
```

The browser checks cover layout at four viewport widths, search, the table of contents, font sizing, print expansion, script errors, and external resource requests. Screenshots go to `/tmp/reading-site-qa/` by default. This is local QA and is not required by the deployment workflow.

## Publish and update

Set the repository's **Settings → Pages** publishing source to **GitHub Actions**. `.github/workflows/reading-site.yml` runs when relevant sources, templates, slides, or docs change on main: install pinned dependencies → rebuild → run static validation → upload `docs/` → deploy. The **Publish research reading site** workflow can also be started manually from Actions.

Only `docs/` is published. Research sources, evidence, and source tools are accessible through GitHub links. To update the site, edit a source or template, rebuild, and commit the generated output. Direct edits to `docs/` will be overwritten by the next build. Confirm publication through the Actions deployment result and a check of the live pages.
