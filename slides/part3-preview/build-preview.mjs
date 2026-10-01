import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const runtimeModules = process.env.RUNTIME_NODE_MODULES;
if (!runtimeModules) throw new Error('Set RUNTIME_NODE_MODULES to the bundled runtime node_modules directory.');
const require = createRequire(path.join(runtimeModules, 'package.json'));
const { Presentation, PresentationFile } = await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);

const workspaceDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const skillDir = process.env.PRESENTATIONS_SKILL_DIR;
if (!skillDir) throw new Error('Set PRESENTATIONS_SKILL_DIR to the installed presentations skill.');
const buildDir = path.join(workspaceDir, 'slides/part3-preview/.build');
const outDir = path.join(workspaceDir, 'slides/part3-preview/output');
const { resolvePresentationFont, finalizePresentation } = await import(pathToFileURL(path.join(skillDir,'container_tools/artifact_tool_utils.mjs')).href);
const font = resolvePresentationFont();
const p = Presentation.create({slideSize:{width:1280,height:720}});
const s = p.slides.add();
s.background.fill='#FFFFFF';
const C={ink:'#1B2733',muted:'#556574',blue:'#0F5A7C',pale:'#E2EDF4',rule:'#CBD7DF',green:'#24785D',orange:'#9D5616'};
function box(name,x,y,w,h,fill='#FFFFFF',stroke=C.rule){return s.shapes.add({name,geometry:'rect',position:{left:x,top:y,width:w,height:h},fill,line:{fill:stroke,width:1.5}});}
function text(name,txt,x,y,w,h,size=24,color=C.ink,bold=false){
  const a=s.shapes.add({name,geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
  a.text=txt;a.text.style={typeface:font,fontSize:size,color,bold,autoFit:'none'};return a;
}
function line(name,x,y,w,h=0,color=C.rule,width=1){return s.shapes.add({name,geometry:'line',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:color,width}});}
function arrow(name,x,y,w,h=18){return s.shapes.add({name,geometry:'rightArrow',position:{left:x,top:y,width:w,height:h},fill:C.blue,line:{fill:'none',width:0}});}

text('section','DIRECTION 1    /    PROPOSED MECHANISM',52,28,1100,24,15,C.muted,true);
text('title','Environment exploration',52,65,1160,62,46,C.ink,true);
text('subtitle','Learn a website rule, save it, and use it on the next task.',52,131,1170,44,28,C.muted);
line('header-rule',52,186,1176);

text('step1','1. Explore and check',52,218,334,45,29,C.blue,true);
text('step2','2. Save what was learned',455,218,372,45,29,C.blue,true);
text('step3','3. Run the next task',899,218,329,45,29,C.blue,true);

// An editable schematic form, not a screenshot of a real product.
box('website',52,290,323,218);
box('website-heading',52,290,323,41,C.pale,C.rule);
text('website-title','Example ticket website',64,295,295,30,21,C.ink,true);
text('type-label','Type',70,345,83,28,22,C.muted);
box('type-value',155,340,200,38,'#FFFFFF',C.rule);
text('type-text','Bug',168,344,170,31,23,C.ink,true);
text('steps-label','Steps to reproduce',70,391,289,30,22,C.ink);
box('steps-value',70,427,285,34,'#FFFFFF',C.rule);
text('validation-message','This field is required.',70,467,289,30,21,C.orange);
text('probe-actions','Vary inputs and retry.\nVerify on fresh examples.',52,524,337,68,22,C.muted);
arrow('exploration-to-file',397,391,38,23);

box('knowledge-file',455,290,362,218,'#F5F9FB',C.blue);
text('filename','site-guide.md',478,304,315,35,26,C.blue,true);
line('file-divider',476,352,318,0,C.rule,1);
text('learned-rule','For a Bug ticket, fill\n“Steps to reproduce”\nbefore submitting.',478,368,315,113,27,C.ink);
text('saved-object','Output: a website instruction file.\nNo model training.',455,524,364,68,22,C.muted);
arrow('file-to-runtime',841,391,38,23);

text('new-input','New Bug ticket:\ndifferent title and steps.',899,288,329,76,23,C.ink);
const agent=box('same-web-agent',899,380,329,95,C.blue,C.blue);
text('runtime-name','Same Web Agent',918,389,290,34,27,'#FFFFFF',true);
text('runtime-load','Notes added to its prompt',918,430,290,33,20,'#FFFFFF');
text('execution-result','Fills the required fields\nbefore submitting.',899,502,329,71,26,C.ink,true);

line('footer-rule',52,608,1176);
text('takeaway','The saved file changes. The model weights stay fixed.',52,626,1176,42,28,C.blue,true);
text('disclosure','Illustrative website rule and proposed implementation. Benefits must be measured on held-out tasks.',52,681,1176,24,15,C.muted);

// Repository presentation convention keeps source and drafting notes outside the deck.
await fs.mkdir(buildDir,{recursive:true});
await fs.mkdir(outDir,{recursive:true});
const candidatePath=path.join(buildDir,'candidate.pptx');
await (await PresentationFile.exportPptx(p)).save(candidatePath);
const preview=await p.export({slide:s,format:'png',scale:1.5});
await fs.writeFile(path.join(buildDir,'preview.png'),new Uint8Array(await preview.arrayBuffer()));
const layout=await s.export({format:'layout'});
await fs.writeFile(path.join(buildDir,'layout.json'),await layout.text());
await fs.writeFile(path.join(buildDir,'presentation.json'),JSON.stringify(p.toProto()));
const result=await finalizePresentation({
  workspaceDir,candidatePath,finalPath:path.join(outDir,'environment-exploration-example.pptx'),
  explicitTotalSlideCount:1,
  requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],
  pythonExecutable:process.env.RUNTIME_PYTHON,
  integrityValidatorPath:path.join(skillDir,'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath:path.join(skillDir,'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit'],
  fontPolicy:{basis:'design',families:[font]},
  verifyArtifactToolImport:true,
  receiptPath:path.join(buildDir,'environment-exploration-example.validation.json'),
});
await fs.copyFile(path.join(buildDir,'preview.png'),path.join(outDir,'environment-exploration-example.png'));
console.log(JSON.stringify({font,result},null,2));
