# Survey report HTML reader

Compiles the Chinese report at `notes/part3/2026-09-30-self-improvement-agent-acceleration-review-zh.md` into an `.html` file with the same basename. This is a reading edition of the existing report; it adds no research evidence and does not change the Markdown or Word content.

The reader includes six introductory slides, the complete text with three comparison tables, twelve method cards, an equation index, and fifty-three complete references. The equation index links back to each equation in the text, and citation numbers open full source details. It supports a mobile table of contents, filtering, font-size controls, and full-text printing. Open the HTML file directly for offline reading; external source links still require internet access.

## Build

Building requires Node.js and `marked`; browser checks also require `playwright` and Chromium. The scripts default to the configured local Codex bundled runtime. On other machines, set `SURVEY_READER_NODE_MODULES` to the `node_modules` directory containing these two packages.

```sh
node tools/survey-reader/build.mjs
node tools/survey-reader/verify.mjs
```

Local executable: `/Users/edwin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node`. A restricted sandbox may prevent Chromium from registering a macOS process port; run verification in an environment that permits launching a local browser.

`verify.mjs` writes screenshots to `/private/tmp/survey-reader-qa` by default. Override this location with `SURVEY_READER_SHOTS`. The checks cover:

- Comparing all 211 prose, list, and table content blocks between the source Markdown and HTML after reversing presentation-only substitutions; checking ten chapters, forty-seven equations, fifty-three references, and three preserved code identifiers.
- Ensuring that none of the five reading views causes page-wide horizontal overflow at viewport widths of 1440, 768, 390, and 320 px. Wide equations and tables scroll within their own containers.
- Exercising introductory-slide navigation, citation dialogs, method and equation filtering, chapter navigation, and the mobile table of contents; confirming that print mode shows the full text and all references.
- Confirming that the page works with every HTTP(S) request blocked, with zero external resource requests and zero script errors.

## Source files

- `build.mjs`: compilation, content-coverage checks, citation parsing, and font embedding.
- `reader.css` / `reader.js`: layout and local interactions.
- `formulas.json`: 47 exact source strings mapped to LaTeX, with source types and notation explanations.
- `inline-math.json`: mappings for plain-text symbols in 23 specified paragraphs. Longer strings are matched first, code and links are excluded, and ASCII variables require word boundaries.
- `index-symbols.json`: additional symbols used in equation-index explanations, preventing compound subscripts from being only partially rendered.
- `methods.json` / `overview.json`: reading aids distilled only from the existing report. Reported method gains retain their experimental conditions; methods are not ranked across benchmarks.
- `FORMULA_NOTES.md`: notation ambiguities and transcription notes.

KaTeX renders equations to HTML and MathML at build time. CSS and all WOFF2 fonts are embedded in the final HTML. No CDN, server, or runtime math script is needed. The build uses strict compilation and disables trusted HTML extensions. The generated file includes the source Markdown's SHA-256 hash to help detect stale output.

## Third-party dependencies

`vendor/katex/` contains the minified build, CSS, WOFF2 fonts, and original MIT license for **KaTeX 0.16.11**, from the public npm package `https://registry.npmjs.org/katex/-/katex-0.16.11.tgz`. The full license is also included in an HTML comment in the output. The build uses `renderToString` as documented in the [official KaTeX API reference](https://katex.org/docs/api). The pinned version is not claimed to be the latest release.
