"""Build the standalone English opening: six main slides and two linked appendices."""
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
for name in ['slide01', 'slide02', 'slide03', 'implementation', 'report']:
    css += '\n' + (HERE / 'deck' / f'{name}.css').read_text()
css += '''
.slide{position:absolute;inset:0;width:1280px;height:720px;background:white;display:none;overflow:hidden}
.slide.is-active{display:block}.slide>footer{right:204px}.slide>footer span:first-child{max-width:1032px}
.deck-nav{position:absolute;right:44px;bottom:13px;display:flex;align-items:center;gap:8px;background:white;z-index:10}
.deck-nav button{padding:3px 9px;font-size:18px;line-height:1.2}.deck-nav button:disabled{opacity:.3;cursor:default}
.deck-page{font:12px 'Plex Mono',monospace;color:var(--muted);min-width:64px;text-align:center}
#s06 #show-all-s06{border-color:transparent;color:var(--muted)}
@media print{html,body{height:auto;overflow:visible}#stage{height:auto;position:relative;left:0;top:0;transform:none}#stage>.slide,#stage>.slide[hidden]{display:block!important;position:relative;break-after:page;page-break-after:always}.slide:last-of-type{break-after:auto;page-break-after:auto}.deck-nav,.controls,.appendix-return{display:none}.slide [data-step]{opacity:1!important}}
'''
defs = re.search(r'<body>\s*(<svg.*?</svg>)', source, re.S).group(1)
slides = []
manifest = [
    ('slide01', 'Our study objective and accounting convention. Proposed experiments; no performance claims are made.'),
    ('slide02', 'Working definitions for this study. The ticket website and its validation rule are illustrative; the benchmark is not yet selected.'),
    ('slide03', 'Proposed questions and hypotheses. The two directions are independent; the initial pilots do not establish novelty.'),
    ('setting', 'Initial within-workflow study. A separate fixed-total-budget comparison is specified in Appendix A1.'),
    ('implementation', 'Illustrative filenames. The first pilots change one artifact; both knowledge and instructions can enter the model context.'),
]
for name, note in manifest:
    slide = (HERE / 'deck' / f'{name}.html').read_text().rstrip()
    end = slide.rfind('</section>')
    slides.append(slide[:end] + f'<footer><span>{note}</span></footer>\n' + slide[end:])
inner = re.search(r'<main[^>]*>(.*?)</main>', source, re.S).group(1)
inner = re.sub(r'<footer>.*?</footer>', '<footer><span>Proposed text-knowledge pilot. Count exploration, validation and reading costs. <a href="#a01">Measurement protocol ↗</a></span></footer>', inner, flags=re.S)
inner = inner.replace('slide-title', 's06-title').replace('id="walk"', 'id="walk-s06"').replace('id="show-all"', 'id="show-all-s06"')
slides.append(f'<section class="slide" id="s06" data-focus="0" aria-labelledby="s06-title">{inner}</section>')
for name, note in [
    ('appendix-evaluation', 'Our proposed evaluation protocol. Task latency, learning time and cumulative monetary cost are reported separately.'),
    ('appendix-objects', 'Proposed implementation choices. Artifact examples explain the first pilots; they do not define the full research directions.'),
]:
    slide = (HERE / 'deck' / f'{name}.html').read_text().rstrip()
    end = slide.rfind('</section>')
    slides.append(slide[:end] + f'<footer><span>{note}</span></footer>\n' + slide[end:])

# Math is pre-rendered as paths, with no runtime font or network dependency.
for i, slide in enumerate(slides):
    def math(match):
        svg = (HERE / 'deck' / 'math' / f'{match.group(1)}.svg').read_text()
        svg = re.search(r'<svg.*</svg>', svg, re.S).group(0)
        return svg
    slides[i] = re.sub(r'\{\{math:([a-z-]+)\}\}', math, slide)

script = r'''
const slides=[...document.querySelectorAll('.slide')], stage=document.querySelector('#stage');
const mainSlides=slides.filter(s=>!s.classList.contains('appendix'));
const appendixSlides=slides.filter(s=>s.classList.contains('appendix'));
const previous=document.querySelector('#previous-slide'), nextButton=document.querySelector('#next-slide'), page=document.querySelector('.deck-page');
const diagram=document.querySelector('#s06'), walk=document.querySelector('#walk-s06'), showAll=document.querySelector('#show-all-s06'), counter=diagram.querySelector('.counter');
let current=0, phase=0, lastMain=0;
function setPhase(value){phase=value;diagram.dataset.focus=String(value);showAll.hidden=!value;walk.textContent=value===3?'Finish walkthrough →':value?'Next step →':'Walk through →';counter.textContent=value?`${value} / 3`:'';walk.setAttribute('aria-label',value===3?'Show the complete diagram':`Highlight step ${value+1}`)}
function advancePhase(){setPhase(phase===3?0:phase+1)}
function group(){return slides[current].classList.contains('appendix')?appendixSlides:mainSlides}
function show(index,updateHash=true){current=Math.max(0,Math.min(slides.length-1,index));slides.forEach((slide,i)=>{slide.classList.toggle('is-active',i===current);slide.hidden=i!==current;slide.setAttribute('aria-hidden',String(i!==current))});const list=group(),position=list.indexOf(slides[current]);if(list===mainSlides)lastMain=current;previous.disabled=position===0;nextButton.disabled=position===list.length-1;page.textContent=list===mainSlides?`${String(position+1).padStart(2,'0')} / ${String(mainSlides.length).padStart(2,'0')}`:`A${position+1} / A${appendixSlides.length}`;document.title=slides[current].querySelector('h1').textContent+' — Web Agent experiments';if(updateHash)history.replaceState(null,'','#'+slides[current].id);setPhase(0)}
function fromHash(){const index=slides.findIndex(s=>'#'+s.id===location.hash);show(index<0?0:index,false)}
function move(delta){const list=group(),position=list.indexOf(slides[current]),target=list[Math.max(0,Math.min(list.length-1,position+delta))];show(slides.indexOf(target))}
previous.addEventListener('click',()=>move(-1));nextButton.addEventListener('click',()=>move(1));walk.addEventListener('click',advancePhase);showAll.addEventListener('click',()=>setPhase(0));
document.addEventListener('click',e=>{const a=e.target.closest('a[href="#back"]');if(a){e.preventDefault();show(lastMain)}});
addEventListener('hashchange',fromHash);
addEventListener('keydown',e=>{if(e.altKey||e.ctrlKey||e.metaKey)return;if(e.key==='ArrowRight'||e.key==='PageDown'){e.preventDefault();move(1)}else if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();move(-1)}else if(e.key==='Home'){e.preventDefault();show(0)}else if(e.key==='End'){e.preventDefault();show(slides.indexOf(mainSlides.at(-1)))}else if(e.key==='Escape'){setPhase(0)}else if((e.key==='b'||e.key==='B')&&group()===appendixSlides){show(lastMain)}else if((e.key==='w'||e.key==='W')&&slides[current]===diagram){advancePhase()}else if(e.key===' '&&!e.target.closest('button,a')){e.preventDefault();if(slides[current]===diagram)advancePhase();else move(1)}});
const fit=()=>document.documentElement.style.setProperty('--scale',Math.min(innerWidth/1280,innerHeight/720));addEventListener('resize',fit);fit();fromHash();
'''
html = '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Web Agent learning experiments</title><style>'+css+'</style></head><body>'+defs+'<main id="stage" aria-label="Web Agent learning experiments">'+'\n'.join(slides)+'''<nav class="deck-nav" aria-label="Slide navigation"><button id="previous-slide" type="button" aria-label="Previous slide" title="Previous slide (left arrow)">‹</button><span class="deck-page" aria-live="polite"></span><button id="next-slide" type="button" aria-label="Next slide" title="Next slide (right arrow)">›</button></nav></main><script>'''+script+'</script></body></html>'
output=HERE/'output'/'web-agent-experiments.html'
output.write_text(html)
print(output)
