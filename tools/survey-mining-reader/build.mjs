import { syncExistingReport } from '../reading-site/publish-report.mjs';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url)), root=path.resolve(here,'../..');
const modules=process.env.SURVEY_READER_NODE_MODULES || '/Users/edwin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {marked}=await import(path.join(modules,'marked/lib/marked.esm.js'));
const require=createRequire(import.meta.url), katex=require('../survey-reader/vendor/katex/katex.min.js');
const sourcePath=path.join(root,'notes/part3/2026-09-30-self-improvement-survey-mining-zh.md');
const outputPath=sourcePath.replace(/\.md$/,'.html');
const original=fs.readFileSync(sourcePath,'utf8');
const ledger=fs.readFileSync(path.join(root,'research/2026-09-30-part3-survey-mining-ledger.md'),'utf8');
const audit=fs.existsSync(path.join(here,'audit.json'))?JSON.parse(fs.readFileSync(path.join(here,'audit.json'),'utf8')):[];
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const json=s=>JSON.stringify(s).replaceAll('<','\\u003c');
const slots=[], math=[], revisions=[];
function slot(html){const id=`QZMATH${String(slots.length).padStart(6,'0')}ZQ`;slots.push([id,html]);return id;}
function mathHtml(tex,display=false){return katex.renderToString(tex,{displayMode:display,throwOnError:true,trust:false,output:'htmlAndMathml',strict:()=> 'ignore'});}
function mathScan(text){
 let output='',pos=0;
 while(pos<text.length){
  if(text[pos]==='`'){const end=text.indexOf('`',pos+1);if(end>=0){output+=text.slice(pos,end+1);pos=end+1;continue;}}
  if(text[pos]==='$'&&text[pos-1]!=='\\'){
   let end=pos+1;while(end<text.length&&(text[end]!=='$'||text[end-1]==='\\')&&text[end]!=='\n')end++;
   const tex=text.slice(pos+1,end), trimmed=tex.trim();
   const looksMath=text[end]==='$'&&trimmed&&!/^[\d.,]+(?:[\s\u4e00-\u9fff]|[→–—-])/.test(trimmed)&&(!/[\u4e00-\u9fff]/.test(trimmed)||/\\text\{/.test(trimmed))&&(!/\b(where|problem|million|cost|per|Table|USD|and|the)\b/i.test(trimmed)||/\\/.test(trimmed));
   if(looksMath){
    try{const html=mathHtml(tex);math.push({latex:tex,source:'$'+tex+'$'});output+=slot(`<span class="math-shell inline" data-math-source="${esc('$'+tex+'$')}">${html}</span>`);pos=end+1;continue;}
    catch(e){throw new Error(`Invalid formula ${tex}\n${e.message}`);}
   }
  }
  output+=text[pos++];
 }
 return output;
}
function expand(html){return html.replace(/QZMATH\d{6}ZQ/g,key=>slots[Number(key.slice(6,-2))][1]);}
function citeEvidence(id){return `<button class="e-link" data-evidence="${id}" title="展开 ${id} 的证据、条件与原文">${id}</button>`;}
function mdHtml(md,{cites=true}={}){
 let s=mathScan(md);
 if(cites)s=s.replace(/\[((?:E\d+)(?:[，,、\s]+E\d+)*)\]/g,(raw,ids)=>slot(`<span class="e-group" data-original-cite="${esc(raw)}">${ids.match(/E\d+/g).map(citeEvidence).join(' ')}</span>`));
 s=s.replace(/\[((?:s|w|h|n|g|x)\d{3})(#[^\]]+)?\](?!\()/g,(raw,id,suffix)=>slot(`<button class="record-link" data-reference="${id}" data-original-cite="${esc(raw)}">[${id}${esc(suffix||'')}]</button>`));
 let html=expand(marked.parse(s,{gfm:true}));
 html=html.replace(/<a href="(https?:[^\"]+)"/g,'<a target="_blank" rel="noopener noreferrer" href="$1"');
 return html;
}
let source=original;
for(const item of audit){for(const patch of item.patches||[]){
 const count=source.split(patch.old).length-1;
 if(count!==1)throw new Error(`Patch ${item.id} expected once, found ${count}: ${patch.old.slice(0,100)}`);
 source=source.replace(patch.old,patch.new);
 revisions.push({id:item.id,old:patch.old,new:patch.new});
}}
const mathEdits=fs.existsSync(path.join(here,'math-replacements.json'))?JSON.parse(fs.readFileSync(path.join(here,'math-replacements.json'),'utf8')):[];
const formattingSkipped=[];
for(const edit of mathEdits){const n=source.split(edit.old).length-1;if(n===1)source=source.replace(edit.old,edit.new);else formattingSkipped.push({old:edit.old,count:n});}
const sections=[...source.matchAll(/^## (.+)$/gm)].map((m,i,a)=>({title:m[1],start:m.index,end:a[i+1]?.index??source.length}));
const sectionText=s=>source.slice(s.start,s.end);
const intro=source.slice(0,sections[0].start);
const reading=sections.find(s=>s.title==='读法与来源');
const chapters=sections.filter(s=>/^\d+ /.test(s.title)).map(s=>({number:Number(s.title.match(/^\d+/)[0]),title:s.title.replace(/^\d+ /,''),md:sectionText(s)}));
const aSection=sections.find(s=>s.title.startsWith('附录 A'));
const cSection=sections.find(s=>s.title.startsWith('附录 C'));
const rSection=sections.find(s=>s.title==='References');
const referencesSource=sectionText(rSection);
const heldOffset=referencesSource.indexOf('### 暂缓与排除');
const refMatches=[...referencesSource.matchAll(/^\*\*\[((?:s|w|h|n|g|x)\d{3})\] /gm)];
const refs=refMatches.map((m,i)=>{
 const block=referencesSource.slice(m.index,refMatches[i+1]?.index??referencesSource.length).replace(/\n### 暂缓与排除[\s\S]*$/,'').trim();
 const first=block.split('\n\n')[0], title=first.match(/\*\*[^\n]+?\*\*\s*\*([^*]+)\*/)?.[1]||m[1];
 const url=block.match(/实际核读版本：\[[^\]]+\]\((https?:[^)]+)\)/)?.[1]||block.match(/\]\((https?:[^)]+)\)/)?.[1];
 const aliases=[['Optimizing generative AI','TextGrad'],['Reflection-Based Memory','ReAP'],['Huxley','HGM'],['Darwin','DGM'],['A Self-Improving Coding Agent','SICA'],['Self-Evolving World Models','WorldEvolver'],['Red Queen','RQGM'],['Agent Workflow Memory','AWM'],['Web Agents with World Models','WMA']].filter(([needle])=>title.toLowerCase().includes(needle.toLowerCase())).map(x=>x[1]).join(' ');
 return {id:m[1],title,block,aliases,html:mdHtml(block,{cites:false}),url,held:heldOffset>=0&&m.index>heldOffset};
});
const refMap=new Map(refs.map(r=>[r.id,r]));
function cells(line){return line.split(/(?<!\\)\|/).slice(1,-1).map(s=>s.trim().replaceAll('\\|','|'));}
const ledgerMap=new Map(ledger.split('\n').filter(l=>/^\| E\d+/.test(l)).map(l=>{const v=cells(l);return [v[0],v];}));
const evidence=sectionText(aSection).split('\n').filter(l=>/^\| E\d+/.test(l)).map(l=>{
 const v=cells(l), full=ledgerMap.get(v[0]), record=v[2].match(/\[([^\]]+)\]/)?.[1];
 const title=v[2].replace(/^\[[^\]]+\]\s*/,''), fields=full?[['陈述',full[1]],['测量定义与条件',full[2]],['来源与位置',full[3]],['原记录日期',full[4]],['来源类别',full[5]],['核对库条目',full[6]],['原审计状态',full[7]]]:[['原稿陈述',v[3]]];
 return {id:v[0],record,title,summary:v[3],search:v.join(' ')+' '+(full||[]).join(' '),html:`<dl class="evidence-fields">${fields.map(([k,val])=>`<dt>${esc(k)}</dt><dd>${mdHtml(val)}</dd>`).join('')}</dl>`,url:full?.[3].match(/https?:\/\/[^\s,)]+/)?.[0],reference:record};
});
if(evidence.length!==645||refs.length!==88||chapters.length!==10)throw new Error(`Unexpected content counts ${evidence.length}/${refs.length}/${chapters.length}`);
const unknown=[];
for(const ids of source.slice(0,aSection.start).matchAll(/\[((?:E\d+)(?:[，,、\s]+E\d+)*)\]/g))for(const id of ids[1].match(/E\d+/g))if(!ledgerMap.has(id))unknown.push(id);
// Earlier E332/E333/E375 are legitimate cross-batch references, explicitly labelled in the UI.
const earlierLedger=fs.readFileSync(path.join(root,'research/2026-09-29-part3-evidence-ledger.md'),'utf8');
for(const id of new Set(unknown)){
 const row=earlierLedger.split('\n').find(l=>l.startsWith('| '+id+' |'));
 if(!row)throw new Error('Unresolved evidence '+id);
 const v=cells(row);evidence.push({id,title:'此前批次的证据',record:v.join(' ').match(/P3 record ([a-z]\d{3})/)?.[1],summary:v[1],search:v.join(' '),html:`<div class="legacy-evidence">${v.slice(1).map(c=>mdHtml(c)).join('')}</div>`,url:v.join(' ').match(/https?:\/\/[^\s,)]+/)?.[0],legacy:true});
}
let tableNo=0;
function readableTables(html){return html.replace(/<table>([\s\S]*?)<\/table>/g,(all,inside)=>{
 const n=++tableNo,headers=[...inside.matchAll(/<th[^>]*>([\s\S]*?)<\/th>/g)].map(m=>m[1]);
 const body=inside.match(/<tbody>([\s\S]*?)<\/tbody>/)?.[1]||'';
 const rows=[...body.matchAll(/<tr>([\s\S]*?)<\/tr>/g)].map(m=>[...m[1].matchAll(/<td[^>]*>([\s\S]*?)<\/td>/g)].map(x=>x[1]));
 if(!rows.length)return all;
 const keyIndex=headers[0]==='分区'&&headers[1]==='工作'?1:0;
 const detailsIndices=headers.map((_,i)=>i).filter(i=>i!==keyIndex);
 return `<div class="comparison" data-table="${n}"><div class="comparison-bar"><span>${rows.length} 项对照</span><button data-table-view="${n}" aria-pressed="false">切换为横向表格</button><button data-expand-table="${n}">展开全部</button></div><div class="table-records">${rows.map(c=>`<details class="table-record"><summary><span>${c[keyIndex]}</span><small>展开看${detailsIndices.slice(0,2).map(i=>headers[i]).map(h=>h.replace(/<[^>]+>/g,'')).join('、')}</small></summary><dl>${detailsIndices.map(i=>`<dt>${headers[i]||''}</dt><dd>${c[i]||''}</dd>`).join('')}</dl></details>`).join('')}</div><div class="table-wrap" hidden tabindex="0" aria-label="横向滚动阅读对照表"><table>${inside}</table></div></div>`;
 });}
const chapterHtml=chapters.map(c=>{
 let html=readableTables(mdHtml(c.md)), sub=0;
 html=html.replace(/<h2>.*?<\/h2>/,`<h2><span class="chapter-kicker">CHAPTER ${String(c.number).padStart(2,'0')}</span>${esc(c.title)}</h2>`);
 html=html.replace(/<h3>([\s\S]*?)<\/h3>/g,(_,s)=>`<h3 id="chapter-${c.number}-${++sub}">${s}</h3>`);
 const notes=audit.filter(a=>(a.chapters||[]).includes(c.number));
 return `<section class="chapter" id="chapter-${c.number}" tabindex="-1">${notes.length?`<aside class="chapter-audit">本章 ${notes.length} 项审核说明 · ${notes.map(a=>`<button data-audit="${a.id}">${a.id} ${esc(a.short||a.title)}</button>`).join('')}</aside>`:''}${html}</section>`;
}).join('\n');
const screeningHtml=readableTables(mdHtml(sectionText(cSection)));
const auditHtml=audit.map(a=>`<article class="audit-card" id="audit-${a.id}" tabindex="-1"><header><span class="audit-id">${esc(a.id)}</span><span class="badge">${esc(a.status)}</span></header><h2>${esc(a.title)}</h2>${mdHtml(a.explanation)}<div class="audit-conclusion">${mdHtml(a.correction)}</div>${a.sources?.length?`<p class="audit-sources">核查依据：${a.sources.map(s=>`<a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">${esc(s.label)}</a>`).join(' · ')}</p>`:''}${(a.patches||[]).length?`<details><summary>查看原句与阅读版修订（${a.patches.length} 处）</summary>${a.patches.map(p=>`<div class="revision-pair"><div><small>原稿</small>${mdHtml(p.old)}</div><div><small>阅读版</small>${mdHtml(p.new)}</div></div>`).join('')}</details>`:''}</article>`).join('\n');
let katexCss=fs.readFileSync(path.join(here,'../survey-reader/vendor/katex/katex.min.css'),'utf8').replace(/src:[^;}]+/g,src=>{const f=src.match(/fonts\/([^"')]+\.woff2)/)?.[1];if(!f)throw new Error('Missing woff2');return `src:url(data:font/woff2;base64,${fs.readFileSync(path.join(here,'../survey-reader/vendor/katex/fonts',f)).toString('base64')}) format("woff2")`;});
const sourceHash=crypto.createHash('sha256').update(original).digest('hex');
const data={evidence,refs:refs.map(({block,...r})=>r)};
const tabs=[['overview','导读'],['report','完整报告'],['audit','审核'],['evidence','证据'],['screening','筛选'],['references','文献']];
const overviewHtml=`<div class="hero"><p class="eyebrow">CLAUDE 文献整理 / CODEX 审核阅读版</p><h1>自改进 Agent 的文献<br>与 Agent 加速</h1><p class="lede">围绕两件事读：怎样从轨迹中改进执行框架，怎样通过交互积累环境知识，以及这些改变何时能收回成本。</p><div class="meta-line"><span>Claude 原稿 · 2026.09.30</span><span>10 章正文</span><span>88 条原稿书目记录</span></div><div class="hero-actions"><button class="primary" data-mode="report">阅读完整报告 →</button><button data-mode="audit">先看审核结论（${audit.length}）</button></div></div>
<div class="section-label"><h2>三个阅读入口</h2><span>从问题进入，保留证据上下文</span></div><div class="route-grid"><button class="route-card" data-chapter="chapter-2"><span>01 / 概念</span><h3>加速与自改进是什么关系</h3><p>自改进是更新机制。速度、费用和成功率是可以分别设定的目标与约束。</p><small>第 1–2 章 →</small></button><button class="route-card" data-chapter="chapter-3"><span>02 / 已有方法</span><h3>从经验到提示、记忆和代码</h3><p>展开逐项方法，连着看机制、问题定义、实验条件和局限。</p><small>第 3–6 章 →</small></button><button class="route-card" data-chapter="chapter-8"><span>03 / 下一步</span><h3>哪些实验值得先做</h3><p>分别验证经验复用、环境规则和候选验收，新增指标不等于已经建立新颖性。</p><small>第 7–10 章 →</small></button></div>
<div class="section-label"><h2>两条研究线，共用一套验收</h2><span>按原稿研究范围整理</span></div><div class="flow"><div class="flow-stage"><span class="stage-no">轨迹驱动</span><strong>运行记录 → 定位与修订</strong><p>成功但冗余、重复失败<br>提示、记忆、程序或框架</p></div><div class="arrow">→</div><div class="flow-stage"><span class="stage-no">独立检查</span><strong>任务正确性 · 费用 · 时间</strong><p>留出任务与状态变化<br>构造、验证和维护另外记账</p></div><div class="arrow">←</div><div class="flow-stage"><span class="stage-no">环境学习</span><strong>交互反馈 → 规则与工具</strong><p>适用条件、接口语义<br>环境结构与可复用动作</p></div></div>
<div class="section-label"><h2>审核后需要记住的边界</h2><span>点击可看原句、修订及来源</span></div><div class="audit-highlights">${audit.filter(a=>a.featured).slice(0,4).map(a=>`<button data-audit="${a.id}"><span>${a.id}</span><strong>${esc(a.title)}</strong><p>${esc(a.summary||a.correction.replace(/\*|\[[^\]]*\]\([^)]*\)/g,''))}</p></button>`).join('')}</div>
<p class="overview-bottom">本轮审读原稿、核对关键论文方法与结果，并检查引用链；没有重新全文审计 82 篇论文。原 Markdown 保留，阅读版中实质修订均可在「审核」查看。作者原有的“已全文阅读”“已审计”标签是原稿的工作记录。</p>`;
const supplementHtml=mdHtml(fs.readFileSync(path.join(here,'audit-references.md'),'utf8'),{cites:false});
const final=`<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="source-sha256" content="${sourceHash}"><title>自改进 Agent 的文献与加速 · Claude 报告审核阅读版</title><style>${katexCss}\n${fs.readFileSync(path.join(here,'../survey-reader/reader.css'),'utf8')}\n${fs.readFileSync(path.join(here,'reader.css'),'utf8')}</style><noscript><style>.panel[hidden]{display:block!important}#panel-overview,#panel-evidence,.topbar,.sidebar,.comparison-bar{display:none!important}.layout{display:block}.table-wrap[hidden]{display:block!important}.table-records{display:none!important}</style></noscript></head><body><a class="skip" href="#main">跳到内容</a><header class="topbar"><button id="menu-toggle" class="icon-button menu-toggle" aria-expanded="false" aria-controls="sidebar" aria-label="打开章节目录">☰</button><a class="brand" href="#" data-mode="overview">AGENT / LITERATURE<small>Claude 原稿 · Codex 审核阅读版</small></a><nav class="view-tabs" role="tablist" aria-label="阅读视图">${tabs.map(([id,t],i)=>`<button id="tab-${id}" role="tab" aria-controls="panel-${id}" aria-selected="${i===0}" data-mode="${id}">${t}</button>`).join('')}</nav><button id="print">打印正文</button><div class="progress" id="reading-progress"></div></header><div class="drawer-shade" id="drawer-shade"></div><div class="layout"><aside class="sidebar" id="sidebar"><button id="drawer-close" class="drawer-close">关闭 ×</button><h2>报告章节</h2><nav class="chapter-nav">${chapters.map(c=>`<a href="#chapter-${c.number}" data-chapter="chapter-${c.number}"><span class="num">${String(c.number).padStart(2,'0')}</span><span>${esc(c.title)}</span></a>${c.number===3?['提示与上下文','经验记忆','技能与工具','整体框架自改'].map((t,i)=>`<a class="subnav" href="#chapter-3-${i+1}" data-chapter="chapter-3-${i+1}"><span class="num">3.${i+1}</span><span>${t}</span></a>`).join(''):''}`).join('')}</nav><div class="side-note"><strong>原稿附录独立展示</strong><br>645 条本批证据<br>421 条候选汇总<br>336 条筛选细目<br>88 条书目记录<br><br>数字是原稿记录数，<br>不是本轮重审篇数。</div></aside><main id="main">
<section class="panel" id="panel-overview" role="tabpanel" aria-labelledby="tab-overview" tabindex="-1">${overviewHtml}</section>
<section class="panel" id="panel-report" role="tabpanel" aria-labelledby="tab-report" tabindex="-1" hidden><header class="panel-heading"><p class="eyebrow">FULL REPORT / REVIEWED EDITION</p><h1>自改进 Agent 的文献与加速</h1><p>原稿结构与文献细节完整保留。密集对照表可逐项展开，也可切回横向表格；证据编号可直接打开记录。</p></header><div class="reading-tools"><button id="font-size">放大正文</button><button id="expand-all">展开本报告所有对照项</button><span class="note">⌘F / Ctrl+F 可搜索正文</span></div><details class="source-intro"><summary>原稿摘要、读法与来源说明</summary>${mdHtml(intro.replace(/^# .*\n/,''))}${mdHtml(sectionText(reading))}</details>${chapterHtml}</section>
<section class="panel" id="panel-audit" role="tabpanel" aria-labelledby="tab-audit" tabindex="-1" hidden><header class="panel-heading"><p class="eyebrow">REVIEW NOTES</p><h1>审核结论与修订依据</h1><p>重点检查研究推论、效率口径、训练边界和引用可追溯性。确认的问题在此保留原句与修订；未独立核实的内容仍按原稿标明，不补成确定结论。</p><p>本轮 ${audit.length} 项审核记录，${revisions.length} 处明示修订。原 Markdown 未改动。</p></header><div class="audit-list">${auditHtml}</div></section>
<section class="panel" id="panel-evidence" role="tabpanel" aria-labelledby="tab-evidence" tabindex="-1" hidden><header class="panel-heading"><p class="eyebrow">EVIDENCE EXPLORER</p><h1>证据记录与测量条件</h1><p>附录 A 的 645 个 E 编号均保留。展开时补充同仓库证据台账中的完整陈述、条件和原文位置；另收录正文引用的此前批次记录。原稿的摘要字段有截断，不能代替原文。</p></header><div class="filters"><label for="evidence-search">搜索 E 编号、论文、机制或测量指标</label><input id="evidence-search" class="search" type="search" placeholder="例如：E669、SICA、latency、cost"></div><p class="filter-count" id="evidence-count" aria-live="polite"></p><div id="evidence-results"></div><div class="pagination"><button id="evidence-prev">← 上一页</button><span id="evidence-page"></span><button id="evidence-next">下一页 →</button></div></section>
<section class="panel" id="panel-screening" role="tabpanel" aria-labelledby="tab-screening" tabindex="-1" hidden><header class="panel-heading"><p class="eyebrow">SCREENING APPENDIX</p><h1>候选筛选与覆盖范围</h1><p>原稿附录 C 完整保留：421 条候选总账、336 条摘要细目；另外 85 条深读/复用主条目移至正文和阅读记录。目录条目不等于独立论文，处理状态的 5 条差异见 D612。</p></header><div class="filters"><label for="screening-search">筛选摘要细目</label><input id="screening-search" class="search" type="search" placeholder="例如：WorldEvolver、ALITA、TextGrad"></div><p id="screening-count" class="filter-count"></p><div class="screening-content">${screeningHtml}</div></section>
<section class="panel" id="panel-references" role="tabpanel" aria-labelledby="tab-references" tabindex="-1" hidden><header class="panel-heading"><p class="eyebrow">REFERENCES</p><h1>参考文献与实际阅读版本</h1><p>保留原稿 88 条书目记录，包括综述及最后单列的 5 项暂缓/排除来源。原稿中部分核读或会议信息带有截断，以下保留原记录，并另提供实际核读链接；不把截断说明补写成已确认发表。</p></header><div class="filters"><label for="reference-search">按记录号、题名或作者搜索</label><input id="reference-search" class="search" type="search" placeholder="例如：s063、Metis、Wang"></div><p class="filter-count" id="reference-count"></p><div class="mining-references">${refs.map(r=>`<article class="mining-reference" id="reference-${r.id}" data-ref-search="${esc((r.block+' '+r.aliases).toLowerCase())}"><header><span class="audit-id">${r.id}</span>${r.held?'<span class="badge held">暂缓 / 排除</span>':''}</header><h2>${esc(r.title)}</h2>${r.url?`<a href="${esc(r.url)}" target="_blank" rel="noopener noreferrer">实际核读版本 ↗</a>`:''}<details><summary>完整作者、发表信息与原稿说明</summary><div class="ref-entry">${r.html}</div></details></article>`).join('')}</div><details class="audit-bibliography"><summary>本轮补核的 26 篇完整书目与核查范围（含范围外近邻）</summary>${supplementHtml}</details></section>
<footer class="footer">基于 Claude Code 2026年9月30日原稿制作；审核修订逐项记录。HTML 可离线阅读，论文外链需联网。<br>报告中的研究方向仍是候选方案，不代表实验已完成或新颖性已确认。</footer></main></div><button class="back-top" id="back-top" hidden>↑ 回到顶部</button><dialog class="ref-dialog" id="detail-dialog"><div class="dialog-header"><h2 id="dialog-title"></h2><button id="dialog-close">关闭 ×</button></div><div class="dialog-content" id="dialog-content"></div></dialog><script id="reader-data" type="application/json">${json(data)}</script><script>${fs.readFileSync(path.join(here,'reader.js'),'utf8')}</script><!-- KaTeX 0.16.11 MIT license:\n${fs.readFileSync(path.join(here,'../survey-reader/vendor/katex/LICENSE'),'utf8')}--></body></html>`;
const renderedMathCount=math.length;
fs.writeFileSync(outputPath,final);
const qaDir=process.env.SURVEY_READER_QA_DIR||'/private/tmp/survey-mining-reader-qa';fs.mkdirSync(qaDir,{recursive:true});
fs.writeFileSync(path.join(qaDir,'content.json'),json({chapters:chapters.map(c=>mdHtml(c.md)),screening:mdHtml(sectionText(cSection)),refs:refs.map(r=>r.html),sourceHash}));
fs.writeFileSync(path.join(here,'build-manifest.json'),JSON.stringify({sourceHash,chapters:10,evidence:645,extraEvidence:evidence.filter(e=>e.legacy).length,references:refs.length,mathOccurrences:renderedMathCount,uniqueMath:[...new Set(math.map(m=>m.latex))].length,auditItems:audit.length,revisions:revisions.length,tableCount:tableNo,mathFormattingEdits:mathEdits.length-formattingSkipped.length,formattingSkipped,bytes:Buffer.byteLength(final)},null,2)+'\n');
fs.writeFileSync(path.join(here,'math-inventory.json'),JSON.stringify([...new Set(math.map(m=>m.latex))],null,2)+'\n');
console.log(fs.readFileSync(path.join(here,'build-manifest.json'),'utf8'));

syncExistingReport(root, sourcePath);
