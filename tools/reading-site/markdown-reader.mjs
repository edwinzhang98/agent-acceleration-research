import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';

const here = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const REPO = 'https://github.com/edwinzhang98/agent-acceleration-research';
const esc = value => String(value ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const plain = value => String(value).replace(/<[^>]*>/g, '').replace(/[*_`]/g, '').trim();
const encodedPath = value => value.split('/').map(encodeURIComponent).join('/');

/** Render one source faithfully. Dependencies and fonts are loaded locally; the returned page is offline. */
export async function renderMarkdownReport(entry, markdown, { root, modules }) {
  if (!root || !modules || !entry.source) throw new Error('renderMarkdownReport requires root, modules, and entry.source');
  const { Marked, Renderer } = await import(pathToFileURL(path.join(modules, 'marked/lib/marked.esm.js')).href);
  const katexDir = path.join(root, 'tools/survey-reader/vendor/katex');
  const katex = require(path.join(katexDir, 'katex.min.js'));
  const sourcePath = path.isAbsolute(entry.source) ? path.relative(root, entry.source) : entry.source;
  if (sourcePath.startsWith('../')) throw new Error('Report source must be inside the repository');
  const originalSource = fs.existsSync(path.join(root, sourcePath)) ? fs.readFileSync(path.join(root, sourcePath), 'utf8') : markdown;
  const sourceHash = crypto.createHash('sha256').update(originalSource).digest('hex');
  const renderedMarkdownHash = crypto.createHash('sha256').update(markdown).digest('hex');
  const sourceUrl = `${REPO}/blob/main/${encodedPath(sourcePath)}`;
  const stats = { sourceHash, renderedMarkdownHash, sourceBytes: Buffer.byteLength(originalSource), headings: 0, sections: 0, tables: 0, formulas: 0, displayFormulas: 0, mathWarnings: [], localPaths: [], rewrittenLinks: 0, imagesAsLinks: 0, sourceHtmlBlocks: 0 };
  const slots = [];
  const prefix = `READERSLOT${sourceHash.slice(0, 12).toUpperCase()}`;
  if (markdown.includes(prefix)) throw new Error('Unexpected placeholder collision');
  const slot = html => { const token = `${prefix}X${slots.length}Z`; slots.push(html); return token; };
  const expand = html => html.replace(new RegExp(`${prefix}X(\\d+)Z`, 'g'), (_, i) => slots[Number(i)]);
  const renderMath = (latex, display, original) => {
    stats.formulas++; if (display) stats.displayFormulas++;
    let result;
    try {
      result = katex.renderToString(latex, {
        displayMode: display, throwOnError: true, trust: false, output: 'htmlAndMathml', maxExpand: 1000, maxSize: 20,
        strict: (code, message) => { stats.mathWarnings.push({ code, message, latex }); return 'ignore'; },
      });
    } catch (error) { throw new Error(`${entry.source}: invalid LaTeX ${JSON.stringify(latex)}: ${error.message}`); }
    return slot(`<span class="math ${display ? 'display-math' : 'inline-math'}" data-math-source="${esc(original)}">${result}</span>`);
  };

  // Protect code before recognizing math, and recognize math before Markdown can consume TeX escapes or table pipes.
  let prepared = markdown.replace(/^([ \t]{0,3})(`{3,}|~{3,})([^\n]*)\n([\s\S]*?)\n\1\2[ \t]*(?=\n|$)/gm, (whole, indent, fence, language, body) => {
    if (/^(?:latex|tex|math)\s*$/i.test(language.trim())) return `\n\n${renderMath(body.trim(), true, whole)}\n\n`;
    return `\n\n${slot(`<pre><code${language.trim() ? ` class="language-${esc(language.trim().split(/\s/)[0])}"` : ''}>${esc(body)}\n</code></pre>`)}\n\n`;
  });
  prepared = prepared.replace(/(?<!`)(`+)(?!`)([^\n]*?)\1(?!`)/g, (whole, fence, body) => slot(`<code>${esc(body.replace(/^ (.*) $/, '$1'))}</code>`));

  const escapedAt = (str, i) => { let count = 0; for (let j = i - 1; j >= 0 && str[j] === '\\'; j--) count++; return count % 2 === 1; };
  const findEnd = (text, needle, start) => { let end = text.indexOf(needle, start); while (end !== -1 && escapedAt(text, end)) end = text.indexOf(needle, end + needle.length); return end; };
  const plausibleDollarMath = (body, after) => {
    if (!body || /^\s|\s$/.test(body) || /\n/.test(body)) return false;
    // A currency opening followed by another price is not a math pair: $11.6–$37.2.
    if (/^\d[\d.,]*(?:\s*[-–—]\s*)?$/.test(body) && /\d/.test(after ?? '')) return false;
    if (/^(?:[\d.,]+)$/.test(body)) return true;
    if (/[\u3400-\u9fff]/.test(body) && !/\\(?:text|mathrm)\s*\{/.test(body)) return false;
    const withoutText = body.replace(/\\(?:text|mathrm|operatorname)\{[^}]*\}/g, 'x');
    if (/\b(?:costs?|pricing|million|dollars?|USD|per|task|tokens?|versus|average|after|baseline|generation)\b/i.test(withoutText)) return false;
    if (/[,;:]\s+[A-Za-z]{3}/.test(withoutText)) return false;
    return /\\[A-Za-z]+|[_^=+<>≤≥≈∑ΣΠλτθμ]|^[A-Za-zα-ωΑ-Ω](?:[A-Za-z0-9]*)?$|[(){}]/.test(body);
  };
  let mathPrepared = '';
  for (let i = 0; i < prepared.length;) {
    let opener = '', closer = '', display = false;
    if (!escapedAt(prepared, i)) {
      if (prepared.startsWith('$$', i)) { opener = closer = '$$'; display = true; }
      // Markdown also uses E\[x\] for literal expectation brackets. A display delimiter starts independently.
      else if (prepared.startsWith('\\[', i) && !/[\p{L}\p{N}_]/u.test(prepared[i - 1] || '')) { opener = '\\['; closer = '\\]'; display = true; }
      else if (prepared.startsWith('\\(', i)) { opener = '\\('; closer = '\\)'; }
      else if (prepared[i] === '$') { opener = closer = '$'; }
    }
    if (opener) {
      const end = findEnd(prepared, closer, i + opener.length);
      if (end === -1 && opener !== '$') throw new Error(`${entry.source}: unclosed ${opener} math at offset ${i}`);
      if (end !== -1) {
        const body = prepared.slice(i + opener.length, end);
        if (opener !== '$' || plausibleDollarMath(body, prepared[end + 1])) {
          const original = prepared.slice(i, end + closer.length);
          mathPrepared += renderMath(body, display, original); i = end + closer.length; continue;
        }
      }
    }
    mathPrepared += prepared[i++];
  }
  prepared = mathPrepared;

  const resolveLink = href => {
    const decoded = String(href ?? '').trim();
    if (/^(?:https?:|mailto:|#)/i.test(decoded)) return { href: decoded, external: !decoded.startsWith('#') };
    if (/^(?:\/Users\/|\/private\/|\/var\/|\/tmp\/|~\/|file:|[A-Za-z]:[\\/])/.test(decoded)) {
      stats.localPaths.push(decoded); return { local: true, path: decoded };
    }
    if (/^[a-z][a-z0-9+.-]*:/i.test(decoded) || decoded.startsWith('//')) return { blocked: true, path: decoded };
    const split = decoded.match(/^([^?#]*)([?#].*)?$/);
    const pathname = split?.[1] ?? decoded;
    const suffix = split?.[2] ?? '';
    let repositoryPath = /^(?:\/?)(?:notes|research|slides|tools|docs)\//.test(pathname)
      ? pathname.replace(/^\//, '')
      : path.posix.normalize(path.posix.join(path.posix.dirname(sourcePath), pathname));
    // Some earlier notes moved into notes/partN without updating ../research links.
    // Repair that spelling only when the source-relative target is absent and the repository target exists.
    const candidate = pathname.replace(/^(?:\.\.\/)+/, '');
    if (!fs.existsSync(path.join(root, repositoryPath)) && /^(?:notes|research|slides|tools|docs)\//.test(candidate) && fs.existsSync(path.join(root, candidate))) repositoryPath = candidate;
    if (repositoryPath.startsWith('../') || repositoryPath.startsWith('/')) return { local: true, path: decoded };
    stats.rewrittenLinks++;
    return { href: `${REPO}/blob/main/${encodedPath(repositoryPath)}${suffix}`, external: true };
  };
  const headingRecords = [];
  const usedIds = new Map();
  let sectionCounter = 0;
  const renderer = new Renderer();
  renderer.html = ({ text }) => {
    stats.sourceHtmlBlocks++;
    if (/^\s*(?:<!--[\s\S]*?-->\s*)+$/.test(text)) return text;
    return `<span class="literal-html">${esc(text)}</span>`;
  };
  renderer.heading = function (token) {
    const label = plain(expand(this.parser.parseInline(token.tokens))).replace(/\s+/g, ' ').trim();
    const base = plain(token.text).toLowerCase().replace(/[^\p{L}\p{N}\s-]/gu, '').replace(/\s+/g, '-').slice(0, 96) || 'section';
    const occurrence = (usedIds.get(base) || 0) + 1; usedIds.set(base, occurrence);
    const id = occurrence === 1 ? base : `${base}-${occurrence}`;
    stats.headings++;
    if (token.depth <= 3) headingRecords.push({ depth: token.depth, label, id });
    return `<h${token.depth} id="${esc(id)}" tabindex="-1">${this.parser.parseInline(token.tokens)}<a class="heading-anchor" href="#${encodeURIComponent(id)}" aria-label="复制本节链接">#</a></h${token.depth}>\n`;
  };
  renderer.link = function ({ href, title, tokens }) {
    const label = this.parser.parseInline(tokens); const dest = resolveLink(href);
    if (dest.local) return `<span class="local-link" title="本机文件路径，在线阅读时不可访问">${label}<small>本机路径</small><code>${esc(dest.path)}</code></span>`;
    if (dest.blocked) return `<span class="local-link">${label}<small>原文链接：${esc(dest.path)}</small></span>`;
    return `<a href="${esc(dest.href)}"${dest.external ? ' target="_blank" rel="noopener noreferrer"' : ''}${title ? ` title="${esc(title)}"` : ''}>${label}</a>`;
  };
  renderer.image = function ({ href, title, text }) {
    stats.imagesAsLinks++; const dest = resolveLink(href);
    if (dest.local || dest.blocked) return `<span class="image-link">图片：${esc(text || title || href)} <small>原图位于本机或使用不可发布的链接：${esc(href)}</small></span>`;
    return `<span class="image-link"><a href="${esc(dest.href)}" target="_blank" rel="noopener noreferrer">图片：${esc(text || title || '打开原图')} ↗</a><small>图片通过原始链接查看；本文不自动加载远程图片。</small></span>`;
  };
  const originalTable = renderer.table;
  renderer.table = function (token) { stats.tables++; return `<div class="table-wrap" tabindex="0" role="region" aria-label="可横向滚动的完整表格">${originalTable.call(this, token)}</div>`; };
  const marked = new Marked({ renderer, gfm: true, breaks: false });
  const tokens = marked.lexer(prepared);
  const groups = []; let current = { title: '开篇', tokens: [], appendix: false };
  for (const token of tokens) {
    if (token.type === 'heading' && token.depth === 2) {
      if (current.tokens.length) groups.push(current);
      current = { title: plain(token.text), tokens: [], appendix: /^(?:附录|参考文献|References|Appendix)/i.test(plain(token.text)) };
    }
    current.tokens.push(token);
  }
  if (current.tokens.length) groups.push(current);
  const body = groups.map(group => {
    const groupTokens = group.tokens; groupTokens.links = tokens.links;
    const content = expand(marked.parser(groupTokens));
    const id = `reading-section-${++sectionCounter}`;
    return `<section class="reading-section${group.appendix ? ' appendix-section' : ''}" id="${id}" data-title="${esc(group.title)}">${group.appendix ? `<button class="section-toggle" aria-expanded="true" aria-controls="${id}-content">折叠本节</button>` : ''}<div class="section-content" id="${id}-content">${content}</div></section>`;
  }).join('\n');
  stats.sections = groups.length;
  const toc = headingRecords.filter(h => h.depth > 1).map(h => `<a class="toc-depth-${h.depth}" href="#${encodeURIComponent(h.id)}">${esc(h.label)}</a>`).join('\n');
  const katexCss = fs.readFileSync(path.join(katexDir, 'katex.min.css'), 'utf8').replace(/src:[^;}]+/g, descriptor => {
    const filename = descriptor.match(/fonts\/([^"')]+\.woff2)/)?.[1];
    if (!filename) throw new Error('KaTeX font lacks a local woff2: ' + descriptor);
    return `src:url(data:font/woff2;base64,${fs.readFileSync(path.join(katexDir, 'fonts', filename)).toString('base64')}) format("woff2")`;
  });
  if (/url\((?!data:)/.test(katexCss)) throw new Error('Unembedded KaTeX asset');
  const stylesheet = fs.readFileSync(path.join(here, 'article.css'), 'utf8');
  const script = fs.readFileSync(path.join(here, 'article.js'), 'utf8');
  const license = fs.readFileSync(path.join(katexDir, 'LICENSE'), 'utf8').replaceAll('--', '—');
  const html = `<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><meta name="description" content="${esc(entry.description)}"><meta name="source-sha256" content="${sourceHash}"><title>${esc(entry.title)} · Agent Research</title><style>${katexCss}\n${stylesheet}</style></head><body>
<a class="skip-link" href="#article">跳到正文</a><header class="site-bar"><button id="toc-toggle" class="mobile-menu" aria-expanded="false" aria-controls="toc-panel" aria-label="打开章节目录">☰ 目录</button><a class="site-brand" href="../index.html">AGENT / RESEARCH<span>返回阅读首页</span></a><div class="toolbar"><button id="font-smaller" aria-label="减小正文字号">A−</button><button id="font-larger" aria-label="增大正文字号">A+</button><button id="print-report">打印 / PDF</button><a href="${esc(sourceUrl)}" target="_blank" rel="noopener noreferrer">Markdown 原稿 ↗</a></div><div id="reading-progress" aria-hidden="true"></div></header>
<div id="drawer-shade" hidden></div><div class="page-layout"><aside id="toc-panel" class="toc-panel" aria-label="文章目录"><div class="toc-title"><strong>文章目录</strong><button id="toc-close" aria-label="关闭章节目录">关闭 ×</button></div><nav>${toc}</nav><div class="toc-foot">完整正文 · ${stats.sections} 个部分<br>${stats.formulas} 个 LaTeX 表达式<br><a href="${esc(sourceUrl)}" target="_blank" rel="noopener noreferrer">查看版本与源文件 ↗</a></div></aside>
<main id="main"><header class="article-meta"><p class="eyebrow">${esc(entry.category || '研究资料')} / READING EDITION</p><div class="meta-line"><span>${esc(entry.author || '研究笔记')}</span><span>${esc(entry.updated || '')}</span>${entry.status ? `<span class="status">${esc(entry.status)}</span>` : ''}</div>${entry.description ? `<p class="description">${esc(entry.description)}</p>` : ''}${entry.notice ? `<p class="source-notice">${esc(entry.notice)}</p>` : ''}</header>
<div class="search-panel"><label for="article-search">查找章节内容</label><div class="search-row"><input type="search" id="article-search" placeholder="输入关键词，查找正文与参考文献" autocomplete="off"><button id="clear-search">清空</button></div><p id="search-status" aria-live="polite">可按 ⌘F / Ctrl+F 在全文中查找。</p><div id="search-results" hidden></div></div>
<noscript><p class="source-notice">JavaScript 未启用：目录、完整正文、公式和参考文献仍可阅读；可使用浏览器查找与打印。</p><style>.section-toggle,.toolbar button,.mobile-menu,#toc-close,.search-panel{display:none!important}</style></noscript>
<article id="article">${body}</article><footer class="article-footer"><p>此阅读版完整转换 Markdown 原稿，保留正文与参考文献。排版转换不代表新增事实核查；讨论稿状态及结论边界以原文为准。</p><p>公式与字体已嵌入，可离线阅读；论文及 GitHub 原稿链接需要网络。<a href="../index.html">返回阅读首页 →</a></p><details><summary>来源与构建信息</summary><p><a href="${esc(sourceUrl)}">${esc(sourcePath)}</a></p><p>源文件 SHA-256：<code>${sourceHash}</code></p></details></footer></main></div>
<button id="back-top" hidden aria-label="返回顶部">↑ 顶部</button><script>${script.replace(/<\/script/gi, '<\\/script')}</script><!-- KaTeX MIT license:\n${license}\n--></body></html>`;
  if (html.includes(prefix)) throw new Error('Unexpanded content placeholder');
  stats.htmlBytes = Buffer.byteLength(html);
  return { html, stats };
}
