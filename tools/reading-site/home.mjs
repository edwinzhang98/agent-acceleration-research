import { readFileSync } from 'node:fs';

const REPOSITORY = 'https://github.com/edwinzhang98/agent-acceleration-research';
const css = readFileSync(new URL('./home.css', import.meta.url), 'utf8');
const escapeHTML = (value = '') => String(value).replace(/[&<>"']/g, char => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
}[char]));

function relativeURL(value) {
  const path = String(value || '');
  if (!path || /^(?:[a-z][a-z\d+.-]*:|[\\/])/i.test(path) || path.split('/').includes('..')) {
    throw new Error(`Expected a repository-relative path: ${path}`);
  }
  return path.split('/').map(encodeURIComponent).join('/');
}

function card(entry, index, core = false) {
  const href = relativeURL(entry.slug);
  const source = entry.source ? `${REPOSITORY}/blob/main/${relativeURL(entry.source)}` : '';
  const title = escapeHTML(entry.title);
  const date = escapeHTML(entry.updated);
  const isoDate = /^\d{4}-\d{2}-\d{2}$/.test(entry.updated || '');
  const isDraft = /草案|草稿|讨论稿|待讨论|待复核|draft|待审|未审核/i.test(entry.status || '');
  const author = String(entry.author || '');
  const angle = /claude/i.test(author) ? '逐篇研究 · 已有工作做到哪一步' : /codex/i.test(author) ? '专题梳理 · 如何理解和评测加速' : '研究报告';
  const search = escapeHTML([entry.title, entry.description, entry.author, entry.category, entry.status].filter(Boolean).join(' ').toLocaleLowerCase());
  return `<article class="document-card${core ? ' core-card' : ''}" data-document data-search="${search}" aria-labelledby="document-${index}">
    <div class="card-top"><span class="card-kind">${core ? escapeHTML(angle) : entry.kind === 'slide' ? '演示阅读版' : '文章阅读版'}</span>${entry.status ? `<span class="badge${isDraft ? ' draft' : ''}">${escapeHTML(entry.status)}</span>` : ''}</div>
    <h3 id="document-${index}"><a href="${href}">${title}</a></h3>
    ${entry.description ? `<p class="card-description">${escapeHTML(entry.description)}</p>` : ''}
    <div class="card-meta">${author ? `<span>${escapeHTML(author)}</span>` : ''}${date ? `<span>来源日期 ${isoDate ? `<time datetime="${date}">${date}</time>` : date}</span>` : ''}</div>
    <div class="card-links"><a class="read-link" href="${href}" aria-label="阅读：${title}">开始阅读 <span aria-hidden="true">↗</span></a>${source ? `<a class="source-link" href="${source}" aria-label="查看来源：${title}">${entry.kind === 'slide' ? '演示说明' : 'Markdown 原稿'}</a>` : ''}</div>
  </article>`;
}

const descriptions = {
  '核心报告': '两份报告各有侧重，可以相互参照。',
  '问题定义': '先把慢在哪里、贵在哪里，以及如何衡量改进讲清楚。',
  '研究计划': '把文献中的线索收敛成可检验的问题和实验。草案保留其当前状态。',
};

/** Build a standalone, offline reading index. Slugs are relative to docs/. */
export function renderHome(entries) {
  if (!Array.isArray(entries)) throw new TypeError('renderHome(entries) expects an array');
  for (const entry of entries) {
    if (!entry.title || !entry.slug) throw new Error('Every entry needs a title and slug');
  }
  const seen = new Set();
  for (const entry of entries) {
    if (seen.has(entry.slug)) throw new Error(`Duplicate entry slug: ${entry.slug}`);
    seen.add(entry.slug);
  }
  const categories = [...new Set(entries.map(entry => entry.category || '其他文档'))];
  const preferred = ['核心报告', '问题定义', '研究计划'];
  categories.sort((a, b) => {
    const first = preferred.indexOf(a), second = preferred.indexOf(b);
    return (first < 0 ? 99 : first) - (second < 0 ? 99 : second);
  });
  const groups = categories.map((category, groupIndex) => {
    const group = entries.map((entry, index) => ({ entry, index })).filter(({ entry }) => (entry.category || '其他文档') === category);
    return `<section class="document-group" data-group aria-labelledby="group-${groupIndex}">
      <header class="section-heading"><div><h2 id="group-${groupIndex}">${escapeHTML(category)}</h2>${descriptions[category] ? `<p>${escapeHTML(descriptions[category])}</p>` : ''}</div><span class="group-count" aria-hidden="true">${String(group.length).padStart(2, '0')}</span></header>
      <div class="card-grid">${group.map(({ entry, index }) => card(entry, index, category === '核心报告')).join('\n')}</div>
    </section>`;
  }).join('\n');
  const latest = entries.map(entry => entry.updated).filter(date => /^\d{4}-\d{2}-\d{2}$/.test(date || '')).sort().at(-1);
  return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="description" content="Agent 加速研究的网页阅读入口：问题定义、免训练自我改进文献与研究计划。">
  <title>Agent 加速研究 · 阅读首页</title>
  <style>${css}</style>
</head>
<body>
  <a class="skip" href="#main">跳到正文</a>
  <header class="site-header"><a class="brand" href="./index.html"><span class="brand-mark" aria-hidden="true">A / A</span><span>Agent 加速研究<small>RESEARCH READING ROOM</small></span></a><a class="repository-link" href="${REPOSITORY}">GitHub 仓库 <span aria-hidden="true">↗</span></a></header>
  <main id="main" tabindex="-1">
    <section class="hero" aria-labelledby="page-title">
      <div class="eyebrow">研究阅读室</div>
      <h1 id="page-title">Agent 加速研究<br>文献、问题与计划</h1>
      <p class="hero-description">从“为什么慢、为什么贵”，走向固定模型权重下的经验学习、环境探索与自我改进。</p>
      <div class="hero-meta"><span>${entries.length} 份阅读材料</span><span>问题 · 文献 · 计划</span>${latest ? `<span>最新来源日期 <time datetime="${escapeHTML(latest)}">${escapeHTML(latest)}</time></span>` : ''}</div>
    </section>
    <aside class="reading-route" aria-labelledby="route-title">
      <div class="route-intro"><span class="eyebrow">从哪里开始</span><h2 id="route-title">按问题选择入口</h2></div>
      <ol><li><span class="step" aria-hidden="true">01</span><div><strong>想先理清加速问题</strong><p>读问题定义与公式手册，了解瓶颈、目标和衡量方式。</p></div></li><li><span class="step" aria-hidden="true">02</span><div><strong>想知道别人做到哪了</strong><p>对照两份核心报告，查看机制、效果、有效条件与局限。</p></div></li><li><span class="step" aria-hidden="true">03</span><div><strong>想讨论下一步怎么做</strong><p>结合较新的文献报告与两份计划讨论稿，选择基线和验证方向。</p></div></li></ol>
    </aside>
    <div class="search-tools" hidden data-search-tools>
      <div class="search-field"><label for="document-search">查找阅读材料</label><input id="document-search" type="search" placeholder="搜索标题、主题或作者" autocomplete="off" aria-controls="document-library" aria-describedby="search-count"></div>
      <div class="search-summary"><span id="search-count" role="status" aria-live="polite" aria-atomic="true">共 ${entries.length} 份材料</span><button type="button" id="clear-search" hidden>清除搜索</button></div>
    </div>
    <div id="document-library">${groups}</div>
    <div class="empty-state" id="empty-state" hidden><h2>没有找到匹配的材料</h2><p>试试“轨迹”“环境”或作者名称，也可以清除搜索查看全部材料。</p><button type="button" id="reset-empty">查看全部材料</button></div>
    <footer class="site-footer"><p>网页阅读版与 Markdown 原稿相互链接。报告的来源、证据范围和审核说明以各文档标注为准。</p><a href="${REPOSITORY}">浏览完整研究仓库 <span aria-hidden="true">↗</span></a></footer>
  </main>
  <script>
  (() => {
    const input = document.getElementById('document-search');
    const cards = [...document.querySelectorAll('[data-document]')];
    const groups = [...document.querySelectorAll('[data-group]')];
    const count = document.getElementById('search-count');
    const clear = document.getElementById('clear-search');
    const empty = document.getElementById('empty-state');
    const filter = () => {
      const terms = input.value.trim().toLocaleLowerCase().split(/\\s+/).filter(Boolean);
      let visible = 0;
      for (const card of cards) {
        card.hidden = !terms.every(term => card.dataset.search.includes(term));
        if (!card.hidden) visible++;
      }
      for (const group of groups) group.hidden = ![...group.querySelectorAll('[data-document]')].some(card => !card.hidden);
      count.textContent = terms.length ? '找到 ' + visible + ' / ' + cards.length + ' 份材料' : '共 ' + cards.length + ' 份材料';
      clear.hidden = !input.value;
      empty.hidden = visible !== 0;
    };
    const reset = () => { input.value = ''; filter(); input.focus(); };
    input.addEventListener('input', filter);
    input.addEventListener('keydown', event => { if (event.key === 'Escape' && input.value) { event.preventDefault(); reset(); } });
    clear.addEventListener('click', reset);
    document.getElementById('reset-empty').addEventListener('click', reset);
    document.querySelector('[data-search-tools]').hidden = false;
    filter();
  })();
  </script>
</body>
</html>`;
}

export default renderHome;
