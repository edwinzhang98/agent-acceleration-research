import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const require = createRequire(import.meta.url);
const nodeModules = process.env.SURVEY_READER_NODE_MODULES || '/Users/edwin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const { marked } = await import(path.join(nodeModules, 'marked/lib/marked.esm.js'));
const katex = require('./vendor/katex/katex.min.js');
const sourcePath = path.join(root, 'notes/part3/2026-09-30-self-improvement-agent-acceleration-review-zh.md');
const outputPath = sourcePath.replace(/\.md$/, '.html');
const read = name => fs.readFileSync(path.join(here, name), 'utf8');
const source = fs.readFileSync(sourcePath, 'utf8');
const formulas = JSON.parse(read('formulas.json'));
const inlineRules = JSON.parse(read('inline-math.json'));
const methods = JSON.parse(read('methods.json'));
const overview = JSON.parse(read('overview.json'));
const esc = str => String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const regexEsc = str => str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const renderMath = (latex, display = false) => katex.renderToString(latex, { displayMode: display, throwOnError: true, trust: false, output: 'htmlAndMathml', strict: error => error === 'unicodeTextInMathMode' ? 'ignore' : 'warn' });
const shell = (latex, display, attributes = '') => `<span class="math-shell ${display ? 'display' : 'inline'}" ${attributes}>${renderMath(latex, display)}</span>`;
const slots = [];
function slot(html) { const key = `ZZMATH${String(slots.length).padStart(5, '0')}ZZ`; slots.push({ key, html }); return key; }
function substitute(text, replacements) {
  const entries = [...replacements].sort((a, b) => b.source.length - a.source.length);
  const map = new Map(entries.map(item => [item.source, item.latex]));
  const re = new RegExp(`(?<![A-Za-z0-9_])(?:${entries.map(x => regexEsc(x.source)).join('|')})(?![A-Za-z0-9_])`, 'g');
  return text.replace(re, token => slot(`<span class="math-token" data-source="${esc(token)}">${renderMath(map.get(token))}</span>`));
}
const formulaUsage = new Map(formulas.map(f => [f.source, 0]));
const formulaMap = new Map(formulas.map((f, i) => [f.source, { ...f, i }]));
function prepare(md) {
  return md.split(/\n\s*\n/).map(block => {
    const rule = inlineRules.find(r => block.startsWith(r.paragraphStartsWith));
    if (rule) block = block.split(/(`[^`]+`|\[[^\]]+\]\([^)]*\))/g).map((piece, i) => i % 2 ? piece : substitute(piece, rule.replacements)).join('');
    return block.replace(/`([^`]+)`/g, (whole, content) => {
      const formula = formulaMap.get(content);
      if (!formula) {
        if (!['not_found', 'click(index=5)', 'contact_name'].includes(content)) throw new Error('Unmapped code/math: ' + content);
        return whole;
      }
      formulaUsage.set(content, formulaUsage.get(content) + 1);
      return slot(shell(formula.latex, formula.display, `id="equation-${formula.i + 1}" tabindex="-1" data-formula="${formula.i + 1}" data-source="${esc(content)}" title="${esc(formula.label)} · ${esc(formula.provenance)}"`));
    });
  }).join('\n\n');
}
const citation = (n, sourceUrl) => `<a class="citation" href="#ref-${n}" data-ref="${n}"${sourceUrl ? ` data-source-url="${esc(sourceUrl)}"` : ''} aria-label="查看参考文献 ${n}">[${n}]</a>`;
function expandSlots(html) { for (const { key, html: value } of slots) html = html.replaceAll(key, value); return html; }
function mdHtml(md, { math = false, citations = false } = {}) {
  if (math) md = prepare(md);
  if (citations) md = md.replace(/\[(\d+)\]\((https?:\/\/[^)]+)\)/g, (_, n, url) => citation(n, url));
  let html = expandSlots(marked.parse(md, { gfm: true, breaks: false }));
  html = html.replace(/<a href="(https?:[^\"]+)"/g, '<a target="_blank" rel="noopener noreferrer" href="$1"');
  html = html.replace(/<table>([\s\S]*?)<\/table>/g, '<div class="table-wrap" tabindex="0" role="region" aria-label="横向滚动查看完整对照表"><table>$1</table></div>');
  html = html.replace(/<p>([\s\S]*?)<\/p>/g, (all, text) => text.includes('data-formula=') ? `<p class="definition">${text}</p>` : all);
  return html;
}
const [bodySource, referencesSource] = source.split('\n## 参考文献\n');
if (!referencesSource) throw new Error('References section missing');
const segments = bodySource.split(/\n(?=## )/);
const introHtml = mdHtml(segments.shift(), { math: true, citations: true });
const chapters = segments.map((chapter, i) => {
  const title = chapter.match(/^## (.+)/)[1];
  const short = title.replace(/^[一二三四五六七八九十]+\s*/, '');
  let html = mdHtml(chapter, { math: true, citations: true });
  let sub = 0;
  html = html.replace(/<h2>.*?<\/h2>/, `<h2><span class="chapter-kicker">CHAPTER ${String(i + 1).padStart(2, '0')}</span>${esc(short)}</h2>`);
  html = html.replace(/<h3>/g, () => `<h3 id="s${i + 1}-sub-${++sub}">`);
  return { number: i + 1, title, short, html };
});
if (chapters.length !== 10) throw new Error('Expected 10 chapters');
for (const [formula, uses] of formulaUsage) if (uses !== 1) throw new Error(`Formula usage ${uses}: ${formula}`);
const referenceBlocks = [...referencesSource.matchAll(/^\[(\d+)\] ([\s\S]*?)(?=\n\n\[\d+\] |$)/gm)].map(m => ({ number: Number(m[1]), text: m[2].trim() }));
if (referenceBlocks.length !== 53 || referenceBlocks.some((r, i) => r.number !== i + 1)) throw new Error('Incomplete reference list');
const refIntro = referencesSource.split(/\n\[1\] /)[0].trim();
const referenceHtml = referenceBlocks.map(r => `<li id="ref-${r.number}" tabindex="-1"><span class="ref-number">[${r.number}]</span><div class="ref-entry">${mdHtml(r.text)}</div></li>`).join('\n');
const objectLabels = { memory: '经验记忆', tool: '程序工具', harness: '执行框架', world: '环境知识' };
const cardsHtml = methods.map(m => `<article class="method-card" id="method-${esc(m.id)}" data-object="${esc(m.object)}">
 <div class="method-tags"><span>${objectLabels[m.object]}</span><span>信号：${esc(m.signal)}</span></div>
 <h2>${esc(m.name)} ${citation(m.ref)}</h2><p class="question">${esc(m.question)}</p>
 <dl><dt>怎么做</dt><dd>${esc(m.mechanism)}</dd><dt>观察到什么</dt><dd>${esc(m.result)}</dd></dl>
 <p class="boundary"><strong>成本口径</strong>${esc(m.costBoundary)}</p>
 <details><summary>局限、证据边界与可检验的问题</summary><p>${esc(m.limitation)}</p><p><strong>可检验的问题：</strong>${esc(m.nextQuestion)}</p></details>
 <button class="jump" data-chapter="s${m.section}">到第 ${m.section} 章读完整分析 →</button>
</article>`).join('\n');
const extraSymbols = JSON.parse(read('index-symbols.json'));
const globalSymbols = [...new Map([...inlineRules.flatMap(r => r.replacements), ...extraSymbols].filter(r => !r.source.includes('不超过')).map(r => [r.source, r])).values()];
const mathText = text => expandSlots(substitute(esc(text), globalSymbols));
const formulaHtml = formulas.map((f, i) => `<article class="formula-card" data-section="${f.section}" id="formula-${i + 1}">
 <header><h2>${String(i + 1).padStart(2, '0')} · ${esc(f.label)}</h2><span class="badge">${esc(f.provenance)}</span></header>
 ${shell(f.latex, true)}<p>${mathText(f.explanation)}</p>${f.notes ? `<p class="notation-note">${mathText(f.notes)}</p>` : ''}
 <button class="jump" data-chapter="equation-${i + 1}">第 ${f.section} 章 · 查看定义上下文与引用 →</button>
</article>`).join('\n');
const slidesHtml = overview.map((s, i) => `<article class="slide" data-target="s${s.chapter}" aria-label="导读 ${i + 1}：${esc(s.title)}" ${i ? 'hidden' : ''}>
 <h3>${esc(s.title)}</h3><p class="claim">${esc(s.claim)}</p><ul>${s.points.map(p => `<li>${esc(p)}</li>`).join('')}</ul><div class="slide-source">相关来源 ${s.refs.map(n => citation(n)).join(' ')}</div>
</article>`).join('\n');
let katexCss = read('vendor/katex/katex.min.css').replace(/src:[^;}]+/g, descriptor => {
  const filename = descriptor.match(/fonts\/([^"')]+\.woff2)/)?.[1];
  if (!filename) throw new Error('Font without woff2: ' + descriptor);
  const font = fs.readFileSync(path.join(here, 'vendor/katex/fonts', filename)).toString('base64');
  return `src:url(data:font/woff2;base64,${font}) format("woff2")`;
});
if (/url\((?!data:)/.test(katexCss)) throw new Error('Unembedded font URL');
const sourceHash = crypto.createHash('sha256').update(source).digest('hex');
const result = `<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><meta name="description" content="固定模型权重下，Agent如何通过轨迹学习与环境探索改进：研究综述、方法比较、公式与完整文献。"><meta name="source-sha256" content="${sourceHash}"><title>固定模型权重下的 Agent 加速与自我改进 · 阅读版</title>
<!-- KaTeX 0.16.11, MIT License. Copyright (c) 2013–2020 Khan Academy and other contributors. Full license at end of document. -->
<style>${katexCss}\n${read('reader.css')}</style></head><body>
<a class="skip" href="#main">跳到内容</a>
<header class="topbar"><button class="icon-button menu-toggle" id="menu-toggle" aria-label="打开章节目录" aria-expanded="false" aria-controls="sidebar">☰</button><a href="#" class="brand" data-mode="overview">AGENT / RESEARCH<small>经验 · 环境 · 执行效率</small></a>
 <nav class="view-tabs" role="tablist" aria-label="阅读视图">${[['overview','导读'],['report','完整报告'],['methods','文献对照'],['formulas','公式'],['references','参考文献']].map(([id, label], i) => `<button role="tab" id="tab-${id}" aria-controls="panel-${id}" aria-selected="${i === 0}" tabindex="${i === 0 ? 0 : -1}" data-mode="${id}">${label}</button>`).join('')}</nav>
 <div class="top-tools"><button class="icon-button" id="print" aria-label="打印完整报告与全部参考文献">打印</button></div><div class="progress" id="reading-progress" aria-hidden="true"></div></header>
<div class="drawer-shade" id="drawer-shade"></div><div class="layout"><aside class="sidebar" id="sidebar" aria-label="章节目录"><button class="drawer-close" id="drawer-close" aria-label="关闭章节目录">关闭 ×</button><h2>完整报告 · 章节目录</h2><nav class="chapter-nav">${chapters.map(c => `<a href="#s${c.number}" data-chapter="s${c.number}"><span class="num">${String(c.number).padStart(2,'0')}</span><span>${esc(c.short)}</span></a>`).join('')}</nav><div class="side-note"><strong>阅读范围</strong><br>固定模型权重<br>轨迹学习与环境探索<br><br>53 条完整引用<br>12 项重点方法对照<br>2026 · 09 · 30</div></aside>
<main id="main"><noscript><div class="noscript">JavaScript 未启用。下方保留完整报告、公式与参考文献。</div><style>#panel-report,#panel-references{display:block!important}#panel-overview,#panel-methods,#panel-formulas{display:none!important}.topbar{display:none}.citation{pointer-events:auto}</style></noscript>
<section class="panel" id="panel-overview" role="tabpanel" aria-labelledby="tab-overview" tabindex="-1">
 <div class="hero"><p class="eyebrow">文献评估 / 研究建议</p><h1>固定模型权重下的<br>Agent 加速与自我改进</h1><p class="lede">从轨迹学习和环境探索出发，看清已有工作怎样改进系统、是否真的省时省钱，以及下一步值得验证什么。</p><div class="meta-line"><span>2026年9月30日</span><span>10 章完整分析</span><span>52 篇论文 + 1 场公开报告</span></div><div class="hero-actions"><button class="primary" data-mode="report">开始读完整报告 →</button><button data-mode="methods">比较重点方法</button></div></div>
 <div class="section-label"><h2>六步读懂研究主线</h2><span>可用左右方向键翻页</span></div>
 <section class="briefing" id="briefing" tabindex="0" aria-label="幻灯片式导读"><div class="briefing-top"><span class="eyebrow">READING GUIDE</span><span class="line"></span><span class="slide-index" id="slide-count" aria-live="polite">01 / 06</span></div>${slidesHtml}<div class="slide-foot"><button class="jump" id="slide-chapter" data-chapter="s1">进入对应章节 →</button><div class="slide-controls"><button id="slide-prev" aria-label="上一张导读">←</button><div class="slide-dots">${overview.map((s, i) => `<button data-slide="${i}" aria-label="导读 ${i + 1}：${esc(s.title)}" aria-current="${i === 0}"></button>`).join('')}</div><button id="slide-next" aria-label="下一张导读">→</button></div></div></section>
 <div class="section-label"><h2>把学习闭环与执行收益分开看</h2><span>同一段经历，可以改变不同部件</span></div>
 <div class="flow" role="img" aria-label="历史轨迹或环境交互产生反馈，用于修改提示、记忆、工具和执行框架，再在未来任务上独立验收质量、时间和费用。"><div class="flow-stage"><span class="stage-no">01 / 反馈从哪来</span><strong>轨迹 · 环境交互</strong><p>成功与失败记录<br>规则、参数和状态反馈</p></div><div class="arrow" aria-hidden="true">→</div><div class="flow-stage"><span class="stage-no">02 / 改变什么</span><strong>模型外的持久产物</strong><p>提示 · 记忆 · 工具<br>执行框架与控制逻辑</p></div><div class="arrow" aria-hidden="true">→</div><div class="flow-stage"><span class="stage-no">03 / 怎样判断</span><strong>未来任务的独立验收</strong><p>质量与副作用<br>时间、费用及维护投入</p></div></div><p class="flow-caption">本文对研究问题的整理；框架分类见 ${citation(1)}，独立验收讨论见第 7、9 章。</p>
 <div class="section-label"><h2>“变快”至少有三种含义</h2><span>三种结果分别记账</span></div><div class="efficiency-grid"><article class="efficiency-card"><h3>更快找到好版本</h3><p>改进搜索用了多少候选、样本和计算？HGM、GEPA 有这类证据。</p></article><article class="efficiency-card"><h3>后续任务执行更快</h3><p>部署时少了多少等待和资源消耗？步数、tokens、秒数需分别看。</p></article><article class="efficiency-card"><h3>长期用下来更划算</h3><p>节省是否超过探索、生成、验证、检索、回退与维护的总投入？</p></article></div>
 <p class="overview-bottom">核心判断：宽泛方向已有充分先例。下一步更有价值的是比较具体机制在目标工作流中的净收益，而不是把“越用越快”本身当作新颖性。<button class="jump" data-chapter="s9">查看下一步研究建议 →</button></p>
</section>
<section class="panel" id="panel-report" role="tabpanel" aria-labelledby="tab-report" tabindex="-1" hidden><header class="panel-heading"><p class="eyebrow">FULL REPORT</p><h1>固定模型权重下的<br>Agent 加速与自我改进</h1><p>从轨迹学习和环境探索出发的文献评估与研究建议 · 2026年9月30日</p></header><div class="reading-tools"><button id="font-size" aria-pressed="false">放大正文</button><button data-mode="formulas">打开公式索引</button><span class="note">点击引用编号查看完整来源 · ⌘F / Ctrl+F 搜索正文</span></div><div class="report-intro">${introHtml}</div>${chapters.map(c => `<section class="chapter" id="s${c.number}" tabindex="-1">${c.html}</section>`).join('\n')}</section>
<section class="panel" id="panel-methods" role="tabpanel" aria-labelledby="tab-methods" tabindex="-1" hidden><header class="panel-heading"><p class="eyebrow">METHOD COMPARISON</p><h1>从方法到证据，再到可检验的问题</h1><p>选出与轨迹复用、环境学习和执行加速最直接的 12 项方法。卡片是阅读入口；完整模型、基准、对照和数值见对应章节。</p><p>“改变对象”用于导览，同一方法可以涉及多个对象。实验条件不同，不把收益数字排成榜单。</p></header><div class="filters"><div class="filter-top"><label for="method-search">检索方法与机制</label><input id="method-search" class="search" type="search" placeholder="例如：回放、维护、费用、AppWorld"></div><div class="filter-row" aria-label="按主要改变对象筛选"><button data-object-filter="all" aria-pressed="true">全部方法</button>${Object.entries(objectLabels).map(([key, name]) => `<button data-object-filter="${key}" aria-pressed="false">${name}</button>`).join('')}</div></div><p class="filter-count" id="method-count" aria-live="polite">显示 12 / 12 项重点方法</p><div class="method-grid">${cardsHtml}</div><p class="empty" id="methods-empty" hidden>没有匹配的方法。可清空关键词或选择“全部方法”。</p></section>
<section class="panel" id="panel-formulas" role="tabpanel" aria-labelledby="tab-formulas" tabindex="-1" hidden><header class="panel-heading"><p class="eyebrow">FORMULA INDEX</p><h1>公式、符号与定义边界</h1><p>汇集正文 47 个数学表达式。每项保留符号解释，并区分原文定义与本文转写、重命名或简化。不同论文的同名符号可能有不同含义，须结合章节上下文阅读。</p></header><div class="filters"><label for="formula-filter">按章节查看　</label><select id="formula-filter" class="search" style="width:auto;max-width:100%"><option value="all">所有公式</option>${chapters.filter(c => formulas.some(f => f.section === c.number)).map(c => `<option value="${c.number}">第 ${c.number} 章 · ${esc(c.short)}</option>`).join('')}</select></div><div class="formula-list">${formulaHtml}</div></section>
<section class="panel" id="panel-references" role="tabpanel" aria-labelledby="tab-references" tabindex="-1" hidden><header class="panel-heading"><p class="eyebrow">REFERENCES</p><h1>参考文献与实际阅读版本</h1><p>${esc(refIntro)}</p></header><div class="filters"><label for="reference-search">按作者、题名或 arXiv 编号查找</label><input class="search" id="reference-search" type="search" placeholder="例如：TextGrad、2507.19457、Wang"></div><p class="filter-count" id="reference-count" aria-live="polite">显示 53 / 53 条完整引用</p><ol class="reference-list">${referenceHtml}</ol></section>
<footer class="footer">本阅读版保留 2026年9月30日 Markdown 报告的全部正文与完整参考文献，新增导读和方法卡片便于阅读。数值与证据解释以完整章节为准。<br>本文件可离线阅读；外部论文链接需要网络。打印时输出完整正文及全部参考文献。</footer></main></div>
<button class="back-top" id="back-top" hidden aria-label="返回当前视图顶部">↑ 回到顶部</button>
<dialog class="ref-dialog" id="reference-dialog" aria-labelledby="dialog-title"><div class="dialog-header"><h2 id="dialog-title">参考文献</h2><button id="dialog-close" aria-label="关闭引用">关闭 ×</button></div><div class="dialog-content" id="dialog-content"></div><div class="dialog-footer"><a href="#" id="dialog-source" target="_blank" rel="noopener noreferrer" hidden>打开该处引用的原文版本 ↗</a><a href="#" id="dialog-all">在完整参考文献中查看 →</a></div></dialog>
<script>${read('reader.js')}</script>
<!-- KaTeX license:\n${read('vendor/katex/LICENSE').replaceAll('--', '—')}\n-->
</body></html>`;
if (/ZZMATH\d+ZZ/.test(result)) throw new Error('Unexpanded formula slot');
fs.writeFileSync(outputPath, result);
console.log(JSON.stringify({ output: outputPath, bytes: Buffer.byteLength(result), chapters: chapters.length, formulas: formulas.length, symbolRules: inlineRules.length, references: referenceBlocks.length, methods: methods.length, slides: overview.length, sourceHash }, null, 2));
