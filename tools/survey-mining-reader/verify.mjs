import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {fileURLToPath,pathToFileURL} from 'node:url';
import assert from 'node:assert/strict';
const here=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(here,'../..');
const modules=process.env.SURVEY_READER_NODE_MODULES||'/Users/edwin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const require=createRequire(import.meta.url),{chromium}=require(path.join(modules,'playwright'));
const qa=process.env.SURVEY_READER_QA_DIR||'/private/tmp/survey-mining-reader-qa';
const content=JSON.parse(fs.readFileSync(path.join(qa,'content.json'),'utf8'));
const manifest=JSON.parse(fs.readFileSync(path.join(here,'build-manifest.json'),'utf8'));
const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:1440,height:1100},deviceScaleFactor:1});
const errors=[],external=[];
page.on('pageerror',e=>errors.push(e.message));
await page.route(/^https?:/,route=>{external.push(route.request().url());return route.abort();});
await page.goto(pathToFileURL(path.join(root,'notes/part3/2026-09-30-self-improvement-survey-mining-zh.html')).href);
await page.evaluate(()=>document.fonts.ready);
assert.equal(await page.locator('.chapter').count(),10);
assert.equal(await page.locator('.audit-card').count(),18);
assert.equal(await page.locator('.mining-reference').count(),88);
assert.equal(await page.locator('.katex-error').count(),0);
assert.equal(await page.locator('.audit-bibliography li').count(),26);
const fidelity=await page.evaluate(expected=>{
 const norm=s=>s.replace(/\s+/g,' ').trim();
 const blocks=n=>[...n.querySelectorAll('p,li,td,th')].map(x=>norm(x.textContent));
 const parse=s=>new DOMParser().parseFromString(s,'text/html');
 const results=[];
 for(let i=0;i<10;i++){
  const node=document.querySelector('#chapter-'+(i+1)).cloneNode(true);
  node.querySelectorAll('.chapter-audit,.table-records,.comparison-bar').forEach(x=>x.remove());
  const a=blocks(node),e=blocks(parse(expected.chapters[i]));
  results.push({chapter:i+1,actual:a.length,expected:e.length,mismatches:a.flatMap((s,j)=>s===e[j]?[]:[{j,actual:s,expected:e[j]}])});
 }
 const refActual=[...document.querySelectorAll('.ref-entry')].map(x=>norm(x.textContent));
 const refExpected=expected.refs.map(x=>norm(parse(x).body.textContent));
 return {chapters:results,refsMatch:refActual.every((s,i)=>s===refExpected[i])};
},content);
assert(fidelity.refsMatch);
for(const c of fidelity.chapters){assert.equal(c.actual,c.expected);assert.deepEqual(c.mismatches,[]);}
await page.screenshot({path:path.join(qa,'desktop-overview.png'),fullPage:true});
await page.locator('#tab-report').click();
await page.locator('.chapter-nav [data-chapter="chapter-3-1"]').click();
await page.locator('#chapter-3 .table-record').first().locator('summary').click();
await page.screenshot({path:path.join(qa,'desktop-formulas.png'),fullPage:false});
for(const name of ['PROMST','HGM','SICA']){
 const summary=page.locator('#panel-report .table-record>summary').filter({hasText:new RegExp('^'+name)}).first();
 await summary.click();await summary.evaluate(n=>n.scrollIntoView({block:'start',behavior:'instant'}));
 await page.screenshot({path:path.join(qa,'formula-'+name+'.png'),fullPage:false});
}
const table=page.locator('#chapter-3 .comparison').first();
await table.locator('[data-table-view]').click();assert(await table.locator('table').isVisible());
await table.locator('[data-table-view]').click();assert(await table.locator('.table-records').isVisible());
await page.locator('#tab-audit').click();
await page.locator('#audit-D596 details').locator('summary').click();
await page.locator('#audit-D596').scrollIntoViewIfNeeded();
await page.screenshot({path:path.join(qa,'desktop-audit.png'),fullPage:false});
await page.locator('#tab-evidence').click();
await page.locator('#evidence-search').fill('E669');
assert.equal(await page.locator('.evidence-result').count(),1);
await page.locator('.evidence-result').click();
assert(await page.locator('#detail-dialog').isVisible());
assert((await page.locator('#dialog-content').textContent()).includes('0.25'));
await page.screenshot({path:path.join(qa,'desktop-evidence.png'),fullPage:false});
await page.keyboard.press('Escape');
assert(!await page.locator('#detail-dialog').isVisible());
await page.locator('#evidence-search').fill('zzzzz-no-match');
assert(await page.locator('#evidence-results .empty').isVisible());
await page.locator('#evidence-search').fill('');
await page.locator('#evidence-next').click();assert.equal(await page.locator('#evidence-page').textContent(),'2 / 44');
await page.locator('#tab-references').click();
await page.locator('#reference-search').fill('TextGrad');assert.equal(await page.locator('.mining-reference:visible').count(),1);
await page.locator('#reference-search').fill('');
await page.locator('#tab-screening').click();assert((await page.locator('#screening-count').textContent()).includes('336 / 336'));
await page.locator('#screening-search').fill('WorldEvolver');assert.equal(await page.locator('#panel-screening .table-record:visible').count(),35); // 34 summary rows + one match
await page.locator('#screening-search').fill('');
const overflow=[];
for(const width of [1440,768,390,320]){
 await page.setViewportSize({width,height:width<500?844:1100});
 for(const mode of ['overview','report','audit','evidence','screening','references']){
  await page.locator('#tab-'+mode).click();
  const g=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth}));
  if(g.scrollWidth>g.width+1)overflow.push({mode,...g});
  if(width===390&&['overview','report','audit'].includes(mode))await page.screenshot({path:path.join(qa,'mobile-'+mode+'.png'),fullPage:false});
 }
}
assert.deepEqual(overflow,[]);
await page.locator('#menu-toggle').click();
await page.locator('.chapter-nav [data-chapter="chapter-8"]').click();
assert.equal(await page.locator('#menu-toggle').getAttribute('aria-expanded'),'false');
assert(new URL(page.url()).hash==='#chapter-8');
await page.emulateMedia({media:'print'});
assert(await page.locator('#panel-report').isVisible());assert(await page.locator('#panel-references').isVisible());assert(!await page.locator('#panel-audit').isVisible());
assert.equal(external.length,0);assert.deepEqual(errors,[]);
await browser.close();
const report={status:'passed',chapters:fidelity.chapters.map(c=>({chapter:c.chapter,blocks:c.actual})),references:88,supplementalReferences:26,primaryEvidence:645,math:manifest.mathOccurrences,viewports:[1440,768,390,320],externalRequests:0,jsErrors:0,screenshots:qa};
fs.writeFileSync(path.join(qa,'verification.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
