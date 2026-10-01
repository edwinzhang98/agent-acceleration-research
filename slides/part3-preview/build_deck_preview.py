"""Build the first four English slides as one standalone offline HTML deck."""
from base64 import b64encode
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
source = (HERE / 'environment-exploration.template.html').read_text()
css = re.search(r'<style>(.*?)</style>', source, re.S).group(1)
faces = []
for family, stem, weights in [('Plex', 'sans', (400, 600)), ('Plex Mono', 'mono', (400,))]:
    for weight in weights:
        data = b64encode((HERE.parent / 'fonts' / f'ibm-plex-{stem}-latin-{weight}-normal.woff2').read_bytes()).decode()
        faces.append(f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};src:url(data:font/woff2;base64,{data}) format('woff2')}}")
css = re.sub(r'/\* FONT_START \*/.*?/\* FONT_END \*/', lambda _: '\n'.join(faces), css, flags=re.S)
css = css.replace('#stage[data-focus=', '.slide[data-focus=')
css += '\n' + '\n'.join((HERE / 'deck' / f'slide{i:02}.css').read_text() for i in range(1, 4))
css += '''
.slide{position:absolute;inset:0;width:1280px;height:720px;background:white;display:none;overflow:hidden}
.slide.is-active{display:block}.slide>footer{right:204px}.slide>footer span:first-child{max-width:1032px}
.deck-nav{position:absolute;right:44px;bottom:13px;display:flex;align-items:center;gap:8px;background:white;z-index:10}
.deck-nav button{padding:3px 9px;font-size:18px;line-height:1.2}.deck-nav button:disabled{opacity:.3;cursor:default}
.deck-page{font:12px 'Plex Mono',monospace;color:var(--muted);min-width:52px;text-align:center}
#s04 #show-all-s04{border-color:transparent;color:var(--muted)}
@media print{html,body{height:auto;overflow:visible}#stage{height:auto;position:relative;left:0;top:0;transform:none}#stage>.slide,#stage>.slide[hidden]{display:block!important;position:relative;break-after:page;page-break-after:always}.slide:last-of-type{break-after:auto;page-break-after:auto}.deck-nav,.controls{display:none}.slide [data-step]{opacity:1!important}}
'''
defs = re.search(r'<body>\s*(<svg.*?</svg>)', source, re.S).group(1)
defs = defs.replace('</defs>', '''
<symbol id="clock" viewBox="0 0 32 32"><circle cx="16" cy="16" r="12"/><path d="M16 8v9l6 3"/></symbol>
<symbol id="cost" viewBox="0 0 32 32"><ellipse cx="16" cy="8" rx="11" ry="4"/><path d="M5 8v8c0 5 22 5 22 0V8M5 16v8c0 5 22 5 22 0v-8"/></symbol>
</defs>''')
footnotes = [
    'Proposed independent experiments with fixed model weights. These diagrams show planned mechanisms, not measured results.',
    'Illustrative sandbox workflow. Reset to comparable starting conditions before each run; the benchmark is not yet selected.',
    'Proposed implementation: each first pilot changes one object. Knowledge files and instructions can both enter model context.',
    'Proposed text-knowledge pilot. Measure success, time and total cost, including exploration, validation and reading the guide.'
]
slides=[]
for i in range(1,4):
    slide = (HERE/'deck'/f'slide{i:02}.html').read_text().rstrip()
    end = slide.rfind('</section>')
    slide = slide[:end] + f'<footer><span>{footnotes[i-1]}</span></footer>\n' + slide[end:]
    slides.append(slide)
inner = re.search(r'<main[^>]*>(.*?)</main>', source, re.S).group(1)
inner = re.sub(r'<footer>.*?</footer>', f'<footer><span>{footnotes[3]}</span></footer>', inner, flags=re.S)
inner = inner.replace('slide-title', 's04-title').replace('id="walk"', 'id="walk-s04"').replace('id="show-all"', 'id="show-all-s04"')
slides.append(f'<section class="slide" id="s04" data-focus="0" aria-labelledby="s04-title">{inner}</section>')
script = r'''
const slides=[...document.querySelectorAll('.slide')], stage=document.querySelector('#stage');
const previous=document.querySelector('#previous-slide'), nextButton=document.querySelector('#next-slide'), page=document.querySelector('.deck-page');
const diagram=document.querySelector('#s04'), walk=document.querySelector('#walk-s04'), showAll=document.querySelector('#show-all-s04'), counter=diagram.querySelector('.counter');
let current=0, phase=0;
function setPhase(value){phase=value;diagram.dataset.focus=String(value);showAll.hidden=!value;walk.textContent=value===3?'Finish walkthrough →':value?'Next step →':'Walk through →';counter.textContent=value?`${value} / 3`:'';walk.setAttribute('aria-label',value===3?'Show the complete diagram':`Highlight step ${value+1}`)}
function advancePhase(){setPhase(phase===3?0:phase+1)}
function show(index,updateHash=true){current=Math.max(0,Math.min(slides.length-1,index));slides.forEach((slide,i)=>{slide.classList.toggle('is-active',i===current);slide.hidden=i!==current;slide.setAttribute('aria-hidden',String(i!==current))});previous.disabled=current===0;nextButton.disabled=current===slides.length-1;page.textContent=`${String(current+1).padStart(2,'0')} / ${String(slides.length).padStart(2,'0')}`;document.title=slides[current].querySelector('h1').textContent+' — Web Agent experiments';if(updateHash)history.replaceState(null,'','#'+slides[current].id);setPhase(0)}
function fromHash(){const index=slides.findIndex(s=>'#'+s.id===location.hash);show(index<0?0:index,false)}
previous.addEventListener('click',()=>show(current-1));nextButton.addEventListener('click',()=>show(current+1));walk.addEventListener('click',advancePhase);showAll.addEventListener('click',()=>setPhase(0));
addEventListener('hashchange',fromHash);
addEventListener('keydown',e=>{if(e.altKey||e.ctrlKey||e.metaKey)return;if(e.key==='ArrowRight'||e.key==='PageDown'){e.preventDefault();show(current+1)}else if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();show(current-1)}else if(e.key==='Home'){e.preventDefault();show(0)}else if(e.key==='End'){e.preventDefault();show(slides.length-1)}else if(e.key==='Escape'){setPhase(0)}else if((e.key==='w'||e.key==='W')&&current===3){advancePhase()}else if(e.key===' '&&!e.target.matches('button')){e.preventDefault();if(current===3)advancePhase();else show(current+1)}});
const fit=()=>document.documentElement.style.setProperty('--scale',Math.min(innerWidth/1280,innerHeight/720));addEventListener('resize',fit);fit();fromHash();
'''
html = '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Web Agent learning experiments</title><style>'+css+'</style></head><body>'+defs+'<main id="stage" aria-label="Web Agent learning experiments">'+'\n'.join(slides)+'''<nav class="deck-nav" aria-label="Slide navigation"><button id="previous-slide" type="button" aria-label="Previous slide" title="Previous slide (left arrow)">‹</button><span class="deck-page" aria-live="polite"></span><button id="next-slide" type="button" aria-label="Next slide" title="Next slide (right arrow)">›</button></nav></main><script>'''+script+'</script></body></html>'
output=HERE/'output'/'web-agent-experiments.html'
output.write_text(html)
print(output)
