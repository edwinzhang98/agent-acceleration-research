import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {publishExistingReport} from './publish-report.mjs';
import {renderHome} from './home.mjs';
import {renderMarkdownReport} from './markdown-reader.mjs';
const here=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(here,'../..');
const localModules=path.join(here,'node_modules');
const modules=process.env.SURVEY_READER_NODE_MODULES||(fs.existsSync(path.join(localModules,'marked'))?localModules:'/Users/edwin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules');
const entries=JSON.parse(fs.readFileSync(path.join(here,'catalog.json'),'utf8'));
const mathFile=path.join(here,'math-formatting.json');
const formatting=fs.existsSync(mathFile)?JSON.parse(fs.readFileSync(mathFile,'utf8')):{};
const hash=s=>crypto.createHash('sha256').update(s).digest('hex');
if(process.argv.includes('--rebuild')){
 for(const script of ['tools/survey-reader/build.mjs','tools/survey-mining-reader/build.mjs'])execFileSync(process.execPath,[path.join(root,script)],{cwd:root,stdio:'inherit',env:{...process.env,SURVEY_READER_NODE_MODULES:modules}});
}
const docRoot=path.join(root,'docs');fs.mkdirSync(docRoot,{recursive:true});
const manifest=[];
for(const entry of entries){
 const source=fs.readFileSync(path.join(root,entry.source),'utf8');
 let html,stats={},formatted=source,formattingCount=0;
 if(entry.htmlSource)html=publishExistingReport(root,entry);
 else {
  for(const edit of formatting[entry.source]||[]){
   const count=formatted.split(edit.old).length-1;
   if(!count)throw new Error(`Math formatting did not match: ${entry.source}: ${edit.old.slice(0,100)}`);
   formatted=formatted.split(edit.old).join(edit.new);formattingCount+=count;
  }
  const result=await renderMarkdownReport(entry,formatted,{root,modules});html=result.html;stats=result.stats;
  const target=path.join(docRoot,entry.slug);fs.mkdirSync(path.dirname(target),{recursive:true});fs.writeFileSync(target,html);
 }
 manifest.push({slug:entry.slug,source:entry.source,sourceHash:hash(source),htmlSource:entry.htmlSource||null,htmlSourceHash:entry.htmlSource?hash(fs.readFileSync(path.join(root,entry.htmlSource))):null,outputHash:hash(html),bytes:Buffer.byteLength(html),formattingCount,stats});
}
fs.writeFileSync(path.join(docRoot,'index.html'),renderHome(entries));
fs.writeFileSync(path.join(docRoot,'.nojekyll'),'');
fs.writeFileSync(path.join(docRoot,'404.html'),'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>返回阅读首页</title><body style="font:18px/1.8 system-ui;max-width:600px;margin:80px auto;padding:24px"><h1>这个页面没有找到</h1><p>报告可能换了位置，请从阅读首页选择。</p><a href="/agent-acceleration-research/">← 阅读首页</a></body></html>');
fs.writeFileSync(path.join(docRoot,'site-manifest.json'),JSON.stringify({reports:manifest},null,2)+'\n');
console.log(JSON.stringify(manifest.map(x=>({slug:x.slug,bytes:x.bytes,stats:x.stats})),null,2));
