(() => {
  'use strict';
  const $ = selector => document.querySelector(selector);
  const sections = [...document.querySelectorAll('.reading-section')];
  const toc = $('#toc-panel');
  const toggle = $('#toc-toggle');
  const shade = $('#drawer-shade');
  const search = $('#article-search');
  const results = $('#search-results');
  const status = $('#search-status');
  let fontSize = 17;
  function menu(open) {
    toc.classList.toggle('is-open', open); toggle.setAttribute('aria-expanded', String(open)); shade.hidden = !open;
    if (open) $('#toc-close').focus();
  }
  toggle.addEventListener('click', () => menu(!toc.classList.contains('is-open')));
  $('#toc-close').addEventListener('click', () => { menu(false); toggle.focus(); });
  shade.addEventListener('click', () => menu(false));
  document.addEventListener('keydown', event => { if (event.key === 'Escape') menu(false); });
  function expandSection(section) {
    if (!section) return;
    const content = section.querySelector('.section-content');
    if (content) content.hidden = false;
    section.classList.remove('collapsed');
    const button = section.querySelector('.section-toggle');
    if (button) { button.textContent = '折叠本节'; button.setAttribute('aria-expanded', 'true'); }
  }
  document.querySelectorAll('.section-toggle').forEach(button => button.addEventListener('click', () => {
    const content = document.getElementById(button.getAttribute('aria-controls'));
    content.hidden = !content.hidden;
    button.textContent = content.hidden ? '展开本节' : '折叠本节';
    button.setAttribute('aria-expanded', String(!content.hidden));
    button.closest('.reading-section').classList.toggle('collapsed', content.hidden);
  }));
  function revealHash() {
    let id; try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (target) { expandSection(target.closest('.reading-section')); requestAnimationFrame(() => target.scrollIntoView()); }
  }
  document.querySelectorAll('a[href^="#"]').forEach(link => link.addEventListener('click', () => {
    menu(false);
    let id; try { id = decodeURIComponent(link.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id); if (target) expandSection(target.closest('.reading-section'));
  }));
  window.addEventListener('hashchange', revealHash);
  if (location.hash) revealHash();
  $('#font-larger').addEventListener('click', () => { fontSize = Math.min(23, fontSize + 1); document.documentElement.style.setProperty('--body-size', `${fontSize}px`); });
  $('#font-smaller').addEventListener('click', () => { fontSize = Math.max(14, fontSize - 1); document.documentElement.style.setProperty('--body-size', `${fontSize}px`); });
  $('#print-report').addEventListener('click', () => window.print());
  const index = sections.map(section => ({ section, title: section.dataset.title, text: section.querySelector('.section-content').textContent.replace(/\s+/g, ' ').trim() }));
  function doSearch() {
    const query = search.value.trim().toLocaleLowerCase();
    results.replaceChildren();
    if (!query) { results.hidden = true; status.textContent = '可按 ⌘F / Ctrl+F 在全文中查找。'; return; }
    const matched = index.filter(item => item.text.toLocaleLowerCase().includes(query));
    status.textContent = `${matched.length} 个部分含有“${search.value.trim()}”。点选结果跳转；按 ⌘F / Ctrl+F 可定位页内每处出现。`;
    results.hidden = false;
    for (const item of matched) {
      const offset = item.text.toLocaleLowerCase().indexOf(query);
      const button = document.createElement('button'); button.type = 'button'; button.className = 'search-result';
      const title = document.createElement('strong'); title.textContent = item.title;
      const excerpt = document.createElement('span'); excerpt.textContent = (offset > 35 ? '…' : '') + item.text.slice(Math.max(0, offset - 35), offset + 125) + (offset + 125 < item.text.length ? '…' : '');
      button.append(title, excerpt);
      button.addEventListener('click', () => {
        expandSection(item.section); item.section.scrollIntoView({ behavior: 'smooth' });
        item.section.classList.remove('flash-section'); requestAnimationFrame(() => item.section.classList.add('flash-section'));
      }); results.append(button);
    }
  }
  search.addEventListener('input', doSearch);
  $('#clear-search').addEventListener('click', () => { search.value = ''; doSearch(); search.focus(); });
  const topButton = $('#back-top');
  topButton.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  let ticking = false;
  function progress() {
    const max = document.documentElement.scrollHeight - innerHeight;
    $('#reading-progress').style.width = `${max > 0 ? Math.max(0, Math.min(100, scrollY / max * 100)) : 0}%`;
    topButton.hidden = scrollY < 650; ticking = false;
  }
  window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(progress); } }, { passive: true });
  window.addEventListener('resize', () => { if (innerWidth > 800) menu(false); progress(); });
  const navLinks = [...toc.querySelectorAll('nav a')];
  const observer = new IntersectionObserver(entries => {
    for (const item of entries) if (item.isIntersecting) {
      for (const link of navLinks) { let id = ''; try { id = decodeURIComponent(link.hash.slice(1)); } catch {} link.classList.toggle('active', id === item.target.id); }
    }
  }, { rootMargin: '-90px 0px -65% 0px' });
  document.querySelectorAll('#article h2,#article h3').forEach(heading => observer.observe(heading));
  let collapsedBeforePrint = [];
  window.addEventListener('beforeprint', () => { collapsedBeforePrint = sections.filter(section => section.classList.contains('collapsed')); sections.forEach(expandSection); });
  window.addEventListener('afterprint', () => { for (const section of collapsedBeforePrint) section.querySelector('.section-toggle')?.click(); collapsedBeforePrint = []; });
  progress();
})();
