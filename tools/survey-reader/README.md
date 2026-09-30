# Survey report HTML reader

把 `notes/part3/2026-09-30-self-improvement-agent-acceleration-review-zh.md` 编译为同名 `.html`。这是既有报告的阅读版本，不新增研究证据或修改 Markdown / Word 内容。

阅读版包含六张导读、全文与三张对照表、十二张重点方法卡、公式索引和五十三条完整参考文献。公式索引可直接跳回正文位置；引用编号打开完整来源。支持移动端目录、筛选、字号调整和打印全文。直接双击 HTML 即可离线阅读，外部原文链接除外。

## 构建

需要 Node.js、`marked`；浏览器检查还需要 `playwright` 及 Chromium。脚本默认使用本机 Codex bundled runtime，其他机器可通过 `SURVEY_READER_NODE_MODULES` 指定这两个包所在的 `node_modules` 目录。

```sh
node tools/survey-reader/build.mjs
node tools/survey-reader/verify.mjs
```

本机可执行文件：`/Users/edwin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node`。受限沙箱可能不允许 Chromium 注册 macOS 进程端口，需要在允许启动本地浏览器的环境运行验证脚本。

`verify.mjs` 的截图默认写入临时目录 `/private/tmp/survey-reader-qa`，可用 `SURVEY_READER_SHOTS` 覆盖。检查包括：

- 逆转仅用于排版的替换后，逐项比较原 Markdown 与 HTML 的 211 个正文/列表/表格内容块；检查十章、四十七个公式、五十三条引用及三个保留代码标识。
- 1440、768、390、320 px 下五个阅读视图无整页横向溢出；宽公式和表格在自身区域内滚动。
- 导读翻页、引用弹窗、方法筛选、公式筛选、章节定位和移动目录可用；打印显示完整正文和全部引用。
- 拦截所有 HTTP(S) 请求后页面正常工作，零外部资源请求、零脚本错误。

## 源文件

- `build.mjs`：编译、内容覆盖检查、引用解析、字体内嵌。
- `reader.css` / `reader.js`：排版和本地交互。
- `formulas.json`：47 个精确原串与 LaTeX 映射，包含来源类型和符号说明。
- `inline-math.json`：23 个指定段落中的裸符号映射。先匹配长串，排除代码和链接，ASCII 变量有词边界。
- `index-symbols.json`：公式索引解释中的额外符号，避免复合下标只渲染一部分。
- `methods.json` / `overview.json`：只从既有报告提炼的阅读辅助内容。方法收益保留实验条件，不做跨基准排行。
- `FORMULA_NOTES.md`：符号歧义与转写说明。

公式在构建时由 KaTeX 渲染为 HTML + MathML；CSS 和所有 WOFF2 字体内嵌到最终 HTML。无需 CDN、服务端或运行时公式脚本；构建使用严格编译并禁止可信 HTML 扩展。生成文件携带源 Markdown 的 SHA-256，便于检查是否过期。

## 第三方依赖

`vendor/katex/` 为 **KaTeX 0.16.11** 的压缩构建、CSS、WOFF2 字体和原始 MIT 许可，来源为公开 npm 包 `https://registry.npmjs.org/katex/-/katex-0.16.11.tgz`。完整许可同时写入最终 HTML 注释。API 依据 [KaTeX 官方说明](https://katex.org/docs/api) 使用 `renderToString`；这不是对最新版本的声明。
