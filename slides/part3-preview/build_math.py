"""Render the accounting equation as offline SVG paths (optional regeneration)."""
from pathlib import Path
import io,re
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
ROOT=Path(__file__).resolve().parent/'deck'/'math'
ROOT.mkdir(parents=True,exist_ok=True)
plt.rcParams['mathtext.fontset']='cm';plt.rcParams['svg.fonttype']='path';plt.rcParams['svg.hashsalt']='web-agent-experiments'
items={'cost':(r'$C_{\mathrm{total}}(N)=C_{\mathrm{learning}}+\sum_{i=1}^{N}C_{\mathrm{exec},i}$','Total cost for N tasks equals learning cost plus the execution cost of all N tasks')}
for name,(tex,label) in items.items():
 fig=plt.figure(figsize=(.01,.01));fig.text(0,0,tex,fontsize=20,color='#125e7e');buf=io.StringIO();fig.savefig(buf,format='svg',bbox_inches='tight',pad_inches=.025,transparent=True);plt.close(fig);s=buf.getvalue();s=s[s.find('<svg'):];s=re.sub(r'<metadata>.*?</metadata>','',s,flags=re.S);s=s.replace('<svg ',f'<svg role="img" aria-label="{label}" ',1)
 for id in set(re.findall(r'id="([^"]+)"',s)):
  s=s.replace('id="'+id+'"','id="'+name+'-'+id+'"').replace('href="#'+id+'"','href="#'+name+'-'+id+'"').replace('url(#'+id+')','url(#'+name+'-'+id+')')
 s='\n'.join(line.rstrip() for line in s.splitlines())+'\n'
 (ROOT/f'{name}.svg').write_text(s)
print('Rendered cost accounting equation')
