# 给 Codex 的 prompt：独立的第三部分 slides

第二步（做页面）。前提：第一步的合并大纲 `notes/part3/2026-10-01-part3-standalone-slides-outline-v3-zh.md` 已由 Edwin 审过。

用法：在仓库根目录运行 `codex exec --skip-git-repo-check --sandbox workspace-write -m gpt-6-astra -o /tmp/part3-deck-report.md "$(cat notes/part3/2026-10-01-codex-prompt-part3-deck.md | sed -n '/^---8<---/,$p')"`，或者直接把下面分隔线以下的全文贴给 Codex。

---8<---

你要在这个仓库里做一份独立的 HTML slides：“第三部分”。它和现有的 `slides/agent-acceleration.html`（第一、二部分）是同一个作者、同一套视觉和写作规范，但它是一个单独的文件。

## 0. 先读，读完再动手

1. `CLAUDE.md`（证据规则、来源资格、引用优先级）。
2. `slides/README.md` 的 “Conventions” 和 “Structure since 2026-09-28” 两节。这是 Edwin 两天里逐条提的要求，是硬性规定，不是参考。
3. `slides/build_deck.py`：看 `slide()`、`card()`、`table()`、`hbars()`、`defs*()`、`tex()`、`refs_html()`、`ci()`/`_mark()` 和整份 CSS。新 deck 用这套页面结构和组件。
4. 打开 `slides/agent-acceleration.html`，至少看 s02–s06、t02–t05 和一页附录，记下：页面左上的等宽小标签、粗标题、细线、“from … → here … → to …” 一行、浅蓝 callout、卡片、SOURCES 行、右下角附录按钮。
5. 内容来源（只能用这些，不许自己补事实）：
   - 页面计划：`notes/part3/2026-10-01-part3-standalone-slides-outline-v3-zh.md`（合并大纲，Edwin 已审）。页序、每页结论、公式项、图示、附录链接都按它来；它和本 prompt 冲突时以它为准。
   - 文献与数字：`notes/part3/2026-10-01-two-directions-literature-zh.md`（逐类、逐篇，含条件和完整参考文献）。
   - 问题定义和统计口径：`notes/part3/2026-09-30-agent-acceleration-problem-framing-zh.md`、`notes/part3/2026-09-30-agent-literature-calibration-zh.md`。
6. `slides/part3-preview/` 是上一版尝试，Edwin 不满意。不要在它上面改，也不要沿用它自己的 CSS 和版式；可以借用里面画得好的机制图思路。

## 1. 交付物

- 新生成器 `slides/build_part3.py`，输出 `slides/part3.html`（字体内嵌，离线可开，不加载外部资源）。
- 公式用 `build_deck.py` 里的 `tex()` 方式在构建时排版成 SVG。如果 import `build_deck.py` 会触发它自己的构建，就把需要的函数和 CSS 复制过来，不要改 `build_deck.py`。
- 不许改动 `slides/build_deck.py`、`slides/agent-acceleration.html`、`.pdf`，也不许改 `slides/part3-preview/`。
- 页面规格表 `notes/part3/2026-10-01-part3-deck-spec-zh.md`，见第 4 节。
- 不要 git commit（你的沙箱写不了 .git），最后列出所有新建和修改的文件。

## 2. 结构（顺序固定）

Edwin 的原话：“先讲问题的定义，然后讲现有研究做到什么程度，然后我们准备做什么。”

页序按 v3 大纲：问题 → 现有研究做到哪 → 我们准备做什么 → References → 附录。主线是 v3 的成本公式，每页标出它对应公式的哪一项（做法同第二部分页面上的公式标注）。两张文献总表（一类一行，含篇数）照 v3 上正文，每行链到对应的逐篇附录页。示例场景是报销单。

## 3. 每页的写法（逐条检查）

1. 标题直接陈述这一页的结论，用平实的话。不用问句做标题，不搞标题党。
2. 一页只讲一个结论。浅蓝 callout 写这个结论，以及它所依据的数字。
3. 卡片：第一行加粗写观点，粗体不用于数字；下面只放一个最有代表性的例子：一个数字，加一句写全的测量条件（基准、任务数、模型、和什么比、测的是什么），再加作者–年份引用。
4. 正文每页大约 200–250 词（引用不算），用 `build_deck.py` 的 `word_report()` 同样的口径统计并打印。
5. 页面文字用英文，不出现 E-/D- 编号，不出现 “preprint/paper” 之类的来源类型词。
6. 禁止黑话和内部代号：wall-clock、nearest neighbor/最近邻、F7/F8/F9、pilot、搭台、“oracle” 等。一律换成平实说法；必须用的术语，第一次出现时在页面上用一句话解释。
7. 每个数字都要能在第 0 节第 5 条的文档里找到原文，带条件；自己算的标 “calc.”。
8. 文档里没有的东西不许编：
   - 还没定的事（用哪个报销流程和环境、资源数字、正式结果）用页面上可见的占位框表示，写成 `[TBD: …]`；
   - 示例场景用“提交一份报销单”（论文的场景），并在页面上标明是示意。
9. 引用：作者–年份。只能引用文献文档里判定为可用的工作，held 列表里的工作一律不引。多个来源说同一件事时，按优先级选：顶会/期刊 → 顶尖机构的预印本 → OpenAI/Anthropic/Google DeepMind 级公司的官方材料。References 里正式发表处和实际读的版本分开写。
10. 机制图用 HTML/SVG 现画，风格和第一、二部分一致：配色克制，只用一种强调色。不要图标堆砌，不要装饰。

## 4. 工作流程（必须分两步，第一步做完就停）

**第一步：先写规格，不写 HTML。** 在 `notes/part3/2026-10-01-part3-deck-spec-zh.md` 里给每一页（包括附录页）写一行：

| 页码 | 英文标题 | 这一页唯一的结论 | callout 里用的数字及出处（文档名 + 小节） | 版面组件（卡片/表/条形图/机制图） | 引用的工作 | 链到哪页附录 |
|---|---|---|---|---|---|---|

**第二步：只做第 1–4 页和它们链到的附录页。** 然后：

- 用 Playwright 按 1280×720 截图，存到 `slides/shots-part3/`；参照 `slides/check_deck.py` 写 `slides/check_part3.py`，每页报告内容是否超出版面框，并检查溢出、重叠和过小的字；
- 把每张截图和 `agent-acceleration.html` 对应风格的页并排看，逐条对照第 3 节自查。不合格的改掉，再截图；
- 停下，不要继续做第 5 页以后。

## 5. 最后的报告（写进 -o 指定的文件）

- 新建和修改的文件列表；
- 每页的字数，以及版面检查结果；
- 第 3 节逐条自查结果：每条写“过/不过”，不过的说明原因；
- 页面上所有 `[TBD]` 占位的列表；
- 你认为大纲里讲不通、或者文档里证据不够的地方。直接说，不要自己编内容去填。
