import fs from 'node:fs';
import path from 'node:path';
const repo='https://github.com/edwinzhang98/agent-acceleration-research/blob/main/';
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('"','&quot;').replaceAll('<','&lt;');
export function prepareExistingReport(entry,html){
  if(entry.kind==='slide') {
    // Leave the fixed-page slide geometry intact; the small link only appears on screen.
    return html.replace('</head>','<style>.reading-site-back{position:fixed;right:12px;bottom:10px;z-index:9999;padding:5px 10px;border:1px solid #cdd8d0;border-radius:5px;background:#faf9f3;color:#22483b;font:12px sans-serif;text-decoration:none}@media print{.reading-site-back{display:none!important}}</style></head>')
      .replace('</body>','<a class="reading-site-back" href="../index.html">← 阅读首页</a></body>');
  }
  const style='<style>.reading-site-bar{display:flex;gap:18px;justify-content:space-between;align-items:center;padding:9px 28px;background:#e8eee5;border-bottom:1px solid #d7dfd2;font:12px/1.6 system-ui,sans-serif;color:#344e42}.reading-site-bar a{color:inherit}.reading-site-bar span{margin-left:auto}@media(max-width:600px){.reading-site-bar{padding:8px 14px;font-size:11px;gap:10px}.reading-site-bar span{display:none}}@media print{.reading-site-bar{display:none}}</style>';
  const bar=`<nav class="reading-site-bar" aria-label="阅读站导航"><a href="../index.html">← 阅读首页</a><span>${esc(entry.author)} · ${esc(entry.status)}</span><a href="${repo+entry.source}" target="_blank" rel="noopener noreferrer">Markdown 原稿 ↗</a></nav>`;
  return html.replace('</head>',style+'</head>').replace(/<body([^>]*)>/,`<body$1>${bar}`);
}
export function publishExistingReport(root,entry){
  const html=prepareExistingReport(entry,fs.readFileSync(path.join(root,entry.htmlSource),'utf8'));
  const target=path.join(root,'docs',entry.slug);
  fs.mkdirSync(path.dirname(target),{recursive:true});fs.writeFileSync(target,html);
  return html;
}
export function syncExistingReport(root,sourcePath){
  const entries=JSON.parse(fs.readFileSync(path.join(root,'tools/reading-site/catalog.json'),'utf8'));
  const relative=path.relative(root,sourcePath).split(path.sep).join('/');
  const entry=entries.find(e=>e.source===relative&&e.htmlSource);
  if(entry)publishExistingReport(root,entry);
}
