# Part 3 mechanism preview

One editable English slide showing a proposed environment-exploration workflow. The ticket website and its validation rule are illustrative, not a selected benchmark or an experimental result.

- [PowerPoint slide](output/environment-exploration-example.pptx)
- [PNG preview](output/environment-exploration-example.png)
- [Content outline (Chinese)](../../notes/part3/2026-10-01-part3-standalone-slides-outline-v2-zh.md)
- [Experiment design (Chinese)](../../notes/part3/2026-10-01-part3-experiment-design-zh.md)

The diagram and text are native PowerPoint objects. `build-preview.mjs` uses the bundled Artifact Tool runtime. Set `RUNTIME_NODE_MODULES`, `RUNTIME_BIN_DIR`, `RUNTIME_PYTHON`, and `PRESENTATIONS_SKILL_DIR` to the paths returned by the workspace dependency loader and the installed presentation skill, then run the script with bundled Node.js. Private drafts and validation records go in `.build/`; deliverables go in `output/`.

The full deck has not been produced. The next content decision is whether this level of concrete detail makes the proposed mechanism clear enough for the audience.
