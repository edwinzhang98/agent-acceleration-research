# 研究阅读站

公开入口：<https://edwinzhang98.github.io/agent-acceleration-research/>

`docs/index.html` 是统一首页。报告在 `docs/reports/`，真正的演示稿在 `docs/slides/`。`notes/` 保存读者向原稿，`research/` 保存证据、审计和修订记录；不把长篇报告归入 slides。

## 本批内容与边界

| 内容 | 生成方式与状态 |
|---|---|
| Codex 固定权重专题报告 | 重用 `tools/survey-reader/` 的完整交互阅读版，加首页和原稿入口。 |
| Claude 综述审核阅读版 | 重用 `tools/survey-mining-reader/`，保留原来的审核修订、证据查询和完整书目。不是对全部论文做了一次新审核。 |
| 最新问题定义报告 | 全文转换；原文区分定位阅读、锚点检查与独立审计。综合判断仍为讨论稿。 |
| 速度与成本公式手册 | 全文转换，LaTeX 围栏排版；价格是 9/28 快照。第 6 节 AQuaUI 表格行原文截断，不补写缺文。 |
| Codex 计划、Claude 第六稿 | 全文转换，明确 9/29 讨论稿状态，尚未吸收 9/30 后续审核的全部结论。 |
| Part 1–2 演示稿 | 原 HTML 加小型首页链接，保持演示内容。 |

首批选择问题定义、公式和两份计划，是因为它们直接补齐“研究什么、如何衡量、下一步怎么验证”的阅读路径。旧的 `research-proposal` 已被详细计划取代，不放同级首页。Part 1 慢/贵逻辑链、Part 2 加速文献是下一批候选；前者原快照缺一张循环图，两者都需要保留历史版本和来源规则。大证据台账和历史 dossier 继续通过仓库溯源，不逐一复制成文章。

本次没有改写研究结论或修改原 Markdown。`math-formatting.json` 只把明确的裸数学表达转成 LaTeX；附录原始证据中的文字式摘要保留。原稿链接的已知错层路径，只有在仓库中确认真实目标存在时才纠偏。原文中的 HTML 注释不作为正文显示，其他原生 HTML 转义处理。公式和字体内嵌，不依赖外部渲染 CDN。

## 生成与检查

需要 Node.js 24；固定的 Markdown 依赖由 lockfile 安装。KaTeX 使用仓库已有的 `tools/survey-reader/vendor/katex/`，许可证随网页保留。

```sh
npm ci --prefix tools/reading-site --ignore-scripts --no-audit --no-fund
node tools/reading-site/build.mjs --rebuild
node tools/reading-site/check.mjs
```

`--rebuild` 先重建两份定制报告，再生成整个站点。单独运行原来任一报告的生成器，也会同步它的 `docs/reports/` 副本；完整首页和哈希清单仍应运行总构建更新。可用 `SURVEY_READER_NODE_MODULES` 指定已安装的 Node 模块目录，用 `SURVEY_READER_QA_DIR` 指定中间校验输出目录。

`catalog.json` 管理标题、来源、状态和输出路径。新增条目可以指向 Markdown，或通过 `htmlSource` 复用已存在的定制 HTML。`site-manifest.json` 记录原稿、原 HTML 与发布文件哈希，以及数学排版和结构统计。源内容有变时，旧的精确数学映射匹配不上会中止构建，避免悄悄丢失格式修订。

可选浏览器检查（需已安装 Playwright 和 Chromium）：

```sh
PLAYWRIGHT_NODE_MODULES=/path/to/node_modules node tools/reading-site/verify.mjs
```

检查四种窗口宽度的布局、搜索、目录、字号、打印展开、脚本错误和外部资源请求，截图默认放 `/tmp/reading-site-qa/`。它是本地 QA，不是在线部署的依赖。

## 发布与更新

仓库 Settings → Pages 使用 **GitHub Actions**。`.github/workflows/reading-site.yml` 在 main 的相关来源、模板、演示或 docs 改动时自动运行：安装固定依赖 → 重建 → 静态验证 → 上传 `docs/` → 部署。也可在 Actions 手动运行 **Publish research reading site**。

只发布 `docs/` 目录；研究原稿、证据及源工具通过 GitHub 链接访问。维护时修改来源或模板，然后重建并提交生成结果，避免直接编辑 `docs/` 后被下一次构建覆盖。是否发布成功以 Actions 的 deployment 结果和线上页面核查为准。
