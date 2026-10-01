# Web Agent learning experiments

Six standalone English HTML slides introduce the research problem, definitions and initial design for two independent experiments. Two linked appendices contain the measurement protocol and engineering objects. The ticket website and validation rule are illustrative; a benchmark has not yet been selected and no experimental results are claimed.

- [HTML deck — primary deliverable](output/web-agent-experiments.html)
- [Six-page overview](output/web-agent-experiments-overview.png)
- [Environment-exploration mechanism on its own](output/environment-exploration-example.html)
- [Content outline (Chinese)](../../notes/part3/2026-10-01-part3-standalone-slides-outline-v2-zh.md)
- [Experiment design (Chinese)](../../notes/part3/2026-10-01-part3-experiment-design-zh.md)
- [Literature classification and mapping (Chinese)](../../notes/part3/2026-10-01-part3-literature-map-zh.md)

Open the HTML directly for offline viewing. Left/right arrows or the page buttons move within the main sequence. Home/End select the first/last main slide. Links open appendices; **B** or **Back to discussion** returns to the main page that opened them. Direct links use `#s01` through `#s06`, `#a01` and `#a02`. On page 6, **Walk through**, W or Space highlights the mechanism in three steps; Escape restores the complete diagram. Printing includes all eight pages.

| Page | Content | Source |
|---|---|---|
| 1 | Research problem and objective | `deck/slide01.html` and `.css` |
| 2 | Task, environment and learning | `deck/slide02.html` and `.css` |
| 3 | Two independent research questions | `deck/slide03.html` and `.css` |
| 4 | Initial study setting and controls | `deck/setting.html`, `deck/report.css` |
| 5 | Implementation and loading interfaces | `deck/implementation.html` and `.css` |
| 6 | Environment-exploration mechanism | `environment-exploration.template.html` |
| A1 | Measurement protocol | `deck/appendix-evaluation.html`, `deck/report.css` |
| A2 | Engineering objects and validation | `deck/appendix-objects.html`, `deck/report.css` |

The opening uses definitions, concise prose, bullets and comparison tables before mechanism diagrams. It follows the typography, restrained colors and appendix navigation of the existing survey deck. Formulas are used only for precise accounting; the cost formula is saved as editable-source, pre-rendered SVG in `deck/math/cost.svg` and can be regenerated with `build_math.py` (requires matplotlib). The two pilots hold execution settings fixed when isolating a learned artifact; the separate fixed-total-budget comparison lets the baseline allocate unused learning budget to execution.

Run `python3 slides/part3-preview/build_deck_preview.py` from the repository root to rebuild the deck. `build_preview_html.py` updates the single-page mechanism preview. Both embed IBM Plex fonts and require no external network resources at presentation time. Native HTML/CSS/SVG diagrams remain editable. Private screenshots and validation records go in `.build/`; deliverables go in `output/`.

The scope of this delivery is the opening through the environment mechanism. Subsequent literature sections, detailed experiment pages and resources remain outlined rather than built. Literature pages will summarize categories and representative studies in the main narrative, with linked paper-by-paper tables, conditions and complete references in appendices; slide count is not fixed.

The earlier PowerPoint prototype and `build-preview.mjs` remain historical material. HTML is the requested delivery format.
