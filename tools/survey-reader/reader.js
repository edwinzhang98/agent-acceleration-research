(() => {
  'use strict';
  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => [...root.querySelectorAll(s)];
  const panels = $$('.panel');
  let mode = 'overview', slideIndex = 0;
  const scrollMemory = {}, slides = $$('.slide');
  const dialog = $('#reference-dialog');
  let lastCitation;
  function closeDrawer() { $('#sidebar').classList.remove('open'); $('#drawer-shade').classList.remove('open'); $('#menu-toggle').setAttribute('aria-expanded', 'false'); }
  function showMode(next, { scroll = true, focus = false } = {}) {
    if (!$('#panel-' + next)) return;
    scrollMemory[mode] = window.scrollY;
    mode = next;
    panels.forEach(p => p.hidden = p.id !== 'panel-' + next);
    $$('[data-mode]').forEach(b => { if (b.getAttribute('role') === 'tab') { b.setAttribute('aria-selected', String(b.dataset.mode === next)); b.tabIndex = b.dataset.mode === next ? 0 : -1; } });
    closeDrawer();
    if (scroll) window.scrollTo({ top: scrollMemory[next] || 0, behavior: 'instant' });
    if (focus) $('#panel-' + next).focus({ preventScroll: true });
    updateProgress();
  }
  function jumpChapter(id) {
    const target = $('#' + id); if (!target) return;
    showMode('report', { scroll: false });
    history.replaceState(null, '', '#' + id);
    requestAnimationFrame(() => { target.scrollIntoView({ behavior: 'instant', block: 'start' }); target.focus({ preventScroll: true }); });
  }
  function openReference(n, origin) {
    const source = $('#ref-' + n); if (!source) return;
    lastCitation = origin;
    $('#dialog-title').textContent = '参考文献 ' + n;
    $('#dialog-content').innerHTML = $('.ref-entry', source).innerHTML;
    const sourceUrl = origin?.dataset.sourceUrl;
    $('#dialog-source').hidden = !sourceUrl;
    if (sourceUrl) $('#dialog-source').href = sourceUrl;
    else $('#dialog-source').removeAttribute('href');
    $('#dialog-all').dataset.ref = String(n);
    if (!dialog.open) dialog.showModal();
  }
  document.addEventListener('click', e => {
    const ref = e.target.closest('.citation');
    if (ref) { e.preventDefault(); openReference(ref.dataset.ref, ref); return; }
    const modeButton = e.target.closest('[data-mode]');
    if (modeButton) { showMode(modeButton.dataset.mode, { focus: modeButton.getAttribute('role') !== 'tab' }); return; }
    const jump = e.target.closest('[data-chapter]');
    if (jump) { e.preventDefault(); jumpChapter(jump.dataset.chapter); }
  });
  $('#dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', e => { if (e.target === dialog) { const r = dialog.getBoundingClientRect(); if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) dialog.close(); } });
  dialog.addEventListener('close', () => { if (lastCitation && !lastCitation.closest('[hidden]')) lastCitation.focus({ preventScroll: true }); });
  $('#dialog-all').addEventListener('click', e => { e.preventDefault(); const n = e.currentTarget.dataset.ref; dialog.close(); $('#reference-search').value = ''; filterReferences(); showMode('references', { scroll: false }); const target = $('#ref-' + n); history.replaceState(null, '', '#ref-' + n); target.scrollIntoView({ behavior: 'instant' }); target.focus({ preventScroll: true }); });
  $('#menu-toggle').addEventListener('click', () => { const open = !$('#sidebar').classList.contains('open'); $('#sidebar').classList.toggle('open', open); $('#drawer-shade').classList.toggle('open', open); $('#menu-toggle').setAttribute('aria-expanded', String(open)); if (open) $('#drawer-close').focus(); });
  $('#drawer-close').addEventListener('click', () => { closeDrawer(); $('#menu-toggle').focus(); });
  $('#drawer-shade').addEventListener('click', closeDrawer);
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeDrawer(); });
  $('.view-tabs').addEventListener('keydown', e => { if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(e.key)) return; const tabs = $$('[role=tab]'); const i = tabs.indexOf(document.activeElement); if (i < 0) return; e.preventDefault(); const next = e.key === 'Home' ? 0 : e.key === 'End' ? tabs.length - 1 : (i + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length; showMode(tabs[next].dataset.mode); tabs[next].focus(); });
  function setSlide(i) {
    slideIndex = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach((s, j) => s.hidden = j !== slideIndex);
    $('#slide-count').textContent = String(slideIndex + 1).padStart(2, '0') + ' / ' + String(slides.length).padStart(2, '0');
    $('#slide-prev').disabled = slideIndex === 0; $('#slide-next').disabled = slideIndex === slides.length - 1;
    $$('[data-slide]').forEach(b => b.setAttribute('aria-current', String(Number(b.dataset.slide) === slideIndex)));
    $('#slide-chapter').dataset.chapter = slides[slideIndex].dataset.target;
  }
  $('#slide-prev').addEventListener('click', () => setSlide(slideIndex - 1));
  $('#slide-next').addEventListener('click', () => setSlide(slideIndex + 1));
  $$('[data-slide]').forEach(b => b.addEventListener('click', () => setSlide(Number(b.dataset.slide))));
  $('#briefing').addEventListener('keydown', e => { if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); setSlide(slideIndex + (e.key === 'ArrowRight' ? 1 : -1)); } });
  let object = 'all';
  function filterMethods() {
    const q = $('#method-search').value.trim().toLowerCase(); let n = 0;
    $$('.method-card').forEach(card => { card.hidden = !((object === 'all' || card.dataset.object === object) && (!q || card.textContent.toLowerCase().includes(q))); if (!card.hidden) n++; });
    $('#method-count').textContent = '显示 ' + n + ' / 12 项重点方法'; $('#methods-empty').hidden = n > 0;
  }
  $('#method-search').addEventListener('input', filterMethods);
  $$('[data-object-filter]').forEach(b => b.addEventListener('click', () => { object = b.dataset.objectFilter; $$('[data-object-filter]').forEach(x => x.setAttribute('aria-pressed', String(x === b))); filterMethods(); }));
  $('#formula-filter').addEventListener('change', e => { const value = e.target.value; $$('.formula-card').forEach(card => card.hidden = value !== 'all' && card.dataset.section !== value); });
  function filterReferences() { const q = $('#reference-search').value.trim().toLowerCase(); let count = 0; $$('.reference-list>li').forEach(ref => { ref.hidden = !ref.textContent.toLowerCase().includes(q); if (!ref.hidden) count++; }); $('#reference-count').textContent = '显示 ' + count + ' / 53 条完整引用'; }
  $('#reference-search').addEventListener('input', filterReferences);
  let large = false;
  $('#font-size').addEventListener('click', e => { large = !large; document.documentElement.style.setProperty('--reading-size', large ? '20px' : '18px'); e.currentTarget.setAttribute('aria-pressed', String(large)); e.currentTarget.textContent = large ? '标准字号' : '放大正文'; });
  $('#print').addEventListener('click', () => window.print());
  $('#back-top').addEventListener('click', () => window.scrollTo({ top: 0, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' }));
  function updateProgress() { const total = document.documentElement.scrollHeight - innerHeight; $('#reading-progress').style.width = (total > 0 ? Math.min(100, Math.max(0, window.scrollY / total * 100)) : 0) + '%'; $('#back-top').hidden = window.scrollY < 500; if (mode === 'report') { let active = 's1'; $$('.chapter').forEach(c => { if (c.getBoundingClientRect().top < 170) active = c.id; }); $$('.chapter-nav a').forEach(a => a.classList.toggle('current', a.dataset.chapter === active)); } }
  let scrollQueued = false;
  window.addEventListener('scroll', () => { if (!scrollQueued) { scrollQueued = true; requestAnimationFrame(() => { updateProgress(); scrollQueued = false; }); } }, { passive: true });
  window.addEventListener('resize', updateProgress);
  function followHash() { const hash = location.hash.slice(1); if (/^(?:s\d+(?:-sub-\d+)?|equation-\d+)$/.test(hash)) jumpChapter(hash); else if (/^ref-\d+$/.test(hash)) { showMode('references', { scroll: false }); $('#' + hash)?.scrollIntoView(); } }
  window.addEventListener('hashchange', followHash);
  setSlide(0); filterMethods(); filterReferences(); showMode('overview', { scroll: false }); followHash();
})();
