"""Build the standalone English HTML slide with embedded repository fonts."""
from base64 import b64encode
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
FONTS = HERE.parent / 'fonts'
faces = []
for family, stem, weights in [('Plex', 'sans', (400, 600)), ('Plex Mono', 'mono', (400,))]:
    for weight in weights:
        data = b64encode((FONTS / f'ibm-plex-{stem}-latin-{weight}-normal.woff2').read_bytes()).decode()
        faces.append(f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};src:url(data:font/woff2;base64,{data}) format('woff2')}}")
html = (HERE / 'environment-exploration.template.html').read_text()
output = HERE / 'output' / 'environment-exploration-example.html'
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(re.sub(r'/\* FONT_START \*/.*?/\* FONT_END \*/', lambda _: '\n'.join(faces), html, flags=re.S))
print(output)
