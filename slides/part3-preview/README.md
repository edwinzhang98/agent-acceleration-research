# Web Agent learning experiments

Four standalone English HTML slides introduce two independent experiments. The slides do not use Part 3 labels or depend on an earlier presentation. The ticket website and its validation rule are illustrative, not a selected benchmark or an experimental result.

- [Four-slide HTML deck — primary deliverable](output/web-agent-experiments.html)
- [Four-slide overview](output/web-agent-experiments-overview.png)
- [Environment-exploration page on its own](output/environment-exploration-example.html)
- [Content outline (Chinese)](../../notes/part3/2026-10-01-part3-standalone-slides-outline-v2-zh.md)
- [Experiment design (Chinese)](../../notes/part3/2026-10-01-part3-experiment-design-zh.md)

Open the HTML file directly in a browser for offline viewing. Use the left/right arrows or the page buttons to navigate. Home/End jump to the first/last page; `#s01` through `#s04` link to individual slides. Page 4 has a separate **Walk through** button; W or Space steps through its diagram and Escape restores the full view.

The page order is: research goal and independent experiments, same-website/new-input setup, changes outside fixed model weights, and the environment-exploration mechanism. Edit `deck/slide01–03.html` and their CSS files for the opening pages. Edit `environment-exploration.template.html` for page 4, then run `python3 slides/part3-preview/build_deck_preview.py` from the repository root. `build_preview_html.py` updates the single-page preview. Both outputs embed IBM Plex fonts. No PowerPoint generation is needed. Private drafts, page screenshots and validation records go in `.build/`; deliverables go in `output/`.

The mechanism page shows two schematic webpage states, a checked rule saved in a file, and task/page/guide inputs entering the unchanged agent. Two illustrative execution paths highlight possible rework; they are not measured results. The HTML scales to the viewport and prints one 1280 × 720 page per slide. The mechanism template also loads the repository fonts locally, so it can be previewed directly.

The [earlier PowerPoint prototype](output/environment-exploration-example.pptx) and `build-preview.mjs` are retained as historical prototype material. They are superseded by the HTML delivery and do not need to be regenerated.

Only the requested first four slides are built. Literature, experiment protocols and the remaining outline pages are still to be produced.
