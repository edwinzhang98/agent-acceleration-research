// Optional local browser QA. Playwright is deliberately not a publishing dependency.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath,pathToFileURL} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const modules=process.env.PLAYWRIGHT_NODE_MODULES||'/Users/edwin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {chromium}=await import(pathToFileURL(path.join(modules,'playwright/index.mjs')));
const catalog=JSON.parse(fs.readFileSync(path.join(root,'tools/reading-site/catalog.json'),'utf8'));
const out=process.env.READING_SITE_QA_DIR||'/tmp/reading-site-qa';fs.mkdirSync(out,{recursive:true});
const browser=await chromium.launch({headless:true});
const results=[];
try {
 for(const width of [1440,768,390,320]){
  const context=await browser.newContext({viewport:{width,height:1000},reducedMotion:'reduce'});
  const requests=[];await context.route(/^https?:/,route=>{requests.push(route.request().url());return route.abort();});
  const page=await context.newPage();const errors=[];page.on('pageerror',err=>errors.push(String(err)));
  for(const entry of [{slug:'index.html',kind:'home'},...catalog]){
   await page.goto(pathToFileURL(path.join(root,'docs',entry.slug)).href,{waitUntil:'load'});
   await page.evaluate(()=>document.fonts.ready);
   assert.equal(await page.locator('.katex-error').count(),0,entry.slug+' KaTeX errors');
   const overflow=await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
   // The existing presentation is a fixed 16:9 deck, with its own zoom behavior.
   if(entry.kind!=='slide')assert.ok(overflow<=1,entry.slug+' overflow '+overflow+' at '+width);
   const duplicateIds=await page.evaluate(()=>{const ids=[...document.querySelectorAll('[id]')].filter(x=>!x.closest('svg')).map(x=>x.id);return ids.filter((x,i)=>ids.indexOf(x)<i);});
   assert.equal(duplicateIds.length,0,entry.slug+' duplicate ids '+duplicateIds.slice(0,5));
   if(entry.kind==='home'){
    await page.locator('#document-search').fill('公式');
    assert.ok(await page.locator('[data-document]:visible').count()>0);
    await page.locator('#document-search').fill('NO-MATCH-92345');
    assert.equal(await page.locator('[data-document]:visible').count(),0);
    await page.locator('#reset-empty').click();
    assert.equal(await page.locator('[data-document]:visible').count(),catalog.length);
   } else if(!entry.htmlSource){
    if(width<=800){await page.locator('#toc-toggle').click();assert.equal(await page.locator('#toc-toggle').getAttribute('aria-expanded'),'true');await page.locator('#toc-close').click();}
    await page.locator('#font-larger').click();
    assert.equal(await page.evaluate(()=>document.documentElement.style.getPropertyValue('--body-size')),'18px');
    await page.locator('#font-smaller').click();
    await page.locator('#article-search').fill('Agent');
    assert.ok(await page.locator('.search-result').count()>0,entry.slug+' section search');
    await page.locator('#clear-search').click();
    const toggle=page.locator('.section-toggle').first();
    if(await toggle.count()){
     await toggle.click();assert.equal(await toggle.getAttribute('aria-expanded'),'false');
     await page.evaluate(()=>dispatchEvent(new Event('beforeprint')));
     assert.equal(await toggle.getAttribute('aria-expanded'),'true');
     await page.evaluate(()=>dispatchEvent(new Event('afterprint')));
     assert.equal(await toggle.getAttribute('aria-expanded'),'false');
     await toggle.click();
    }
    await page.evaluate(()=>scrollTo(0,0));
   }
   if(width===1440||width===390)await page.screenshot({path:path.join(out,entry.slug.replaceAll('/','-')+'-'+width+'.png')});
   results.push({page:entry.slug,width,overflow,math:await page.locator('.katex').count()});
  }
  assert.deepEqual(errors,[],`JS errors at ${width}`);assert.deepEqual(requests,[],`External resources at ${width}`);
  await context.close();
 }
 fs.writeFileSync(path.join(out,'browser-checks.json'),JSON.stringify(results,null,2)+'\n');
 console.log(JSON.stringify({pages:catalog.length+1,widths:[1440,768,390,320],checks:results.length,externalRequests:0,jsErrors:0,screenshots:out},null,2));
} finally {await browser.close();}
