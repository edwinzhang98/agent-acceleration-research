#!/usr/bin/env python3
"""Build slides/agent-acceleration.html — the boss deck.

Part 1 (this file's content): where the time and the money go, built from the
Chinese study document《Agent 慢和贵的逻辑链》(2026-09-27), which is itself built
from dossier v3. Numbers are the dossier's; the ledger IDs live in the Chinese
the dossier and research/, not on the slides.

Usage: python3 slides/build_deck.py [--fonts DIR]   (DIR holds the IBM Plex woff2
files; without it the deck falls back to system fonts).
"""
import base64, html, json, os, re, sys

W, H = 1280, 720
OUT = os.path.join(os.path.dirname(__file__), "agent-acceleration.html")

# ---------------------------------------------------------------- fonts
FONT_FILES = [
    ("IBM Plex Sans", 400, "normal", "ibm-plex-sans-latin-400-normal.woff2"),
    ("IBM Plex Sans", 400, "italic", "ibm-plex-sans-latin-400-italic.woff2"),
    ("IBM Plex Sans", 500, "normal", "ibm-plex-sans-latin-500-normal.woff2"),
    ("IBM Plex Sans", 600, "normal", "ibm-plex-sans-latin-600-normal.woff2"),
    ("IBM Plex Sans", 700, "normal", "ibm-plex-sans-latin-700-normal.woff2"),
    ("IBM Plex Mono", 400, "normal", "ibm-plex-mono-latin-400-normal.woff2"),
    ("IBM Plex Mono", 500, "normal", "ibm-plex-mono-latin-500-normal.woff2"),
]

def font_css(font_dir):
    if not font_dir or not os.path.isdir(font_dir):
        return "/* IBM Plex not embedded: system fallback fonts */\n"
    out = []
    for fam, wt, style, fn in FONT_FILES:
        p = os.path.join(font_dir, fn)
        if not os.path.exists(p):
            continue
        b64 = base64.b64encode(open(p, "rb").read()).decode()
        out.append(f"@font-face{{font-family:'{fam}';font-weight:{wt};font-style:{style};font-display:swap;"
                   f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")
    return "\n".join(out) + "\n"

# ---------------------------------------------------------------- the loop diagram
SVG_N = [0]
TERM_IDS = {"n-steps", "n-calls", "n-queue", "n-read", "n-write", "n-observe", "n-act", "n-wait",
            "n-rtok", "n-wtok", "n-price", "n-succ", "n-machine", "n-overlap", "n-decide"}

def loop_svg(hl=(), cls="thumb-svg", big=False):
    """The agent loop with the variable at each step. big=True (page 2 only) adds page tags and the
    harness note; big=False is the thumbnail, same geometry, so each thumbnail is page 2 in miniature."""
    bad = set(hl) - TERM_IDS
    if bad:
        raise ValueError(f"unknown term ids in hl: {sorted(bad)}")
    hl = set(hl)
    SVG_N[0] += 1
    mid = f"ah{SVG_N[0]}"
    INK, WHITE = "#1b2733", "#ffffff"
    def col(id_):
        return WHITE if id_ in hl else INK
    def m(src, x, yc, px, color=INK, anchor="middle"):
        if "$" not in src:
            src = "$" + src + "$"
        svg, w, hh, d = _render_tex(src, 12, color)
        s = px / 12.0
        ww, h2 = w * s, hh * s
        x0 = x - ww/2 if anchor == "middle" else (x - ww if anchor == "end" else x)
        return re.sub(r'<svg ([^>]*?)width="[\d.]+pt" height="[\d.]+pt"',
                      lambda mm: f'<svg {mm.group(1)}x="{x0:.1f}" y="{yc - h2/2:.1f}" width="{ww:.1f}" height="{h2:.1f}"', svg, count=1)
    def txt(x, y, t, fs=11, anchor="middle", cls_="fm"):
        return f'<text class="{cls_}" x="{x}" y="{y}" font-size="{fs}" text-anchor="{anchor}">{html.escape(t)}</text>'
    def node(id_, x, y, w, h, title, sub, msrc):
        c = " hl" if id_ in hl else ""
        s = f'<g id="{mid}-{id_}" class="node{c}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>'
        s += f'<text class="t" x="{x+w/2}" y="{y+24}" font-size="18" text-anchor="middle">{html.escape(title)}</text>'
        s += f'<text class="s" x="{x+w/2}" y="{y+41}" font-size="11.5" text-anchor="middle">{html.escape(sub)}</text>'
        s += m(msrc, x+w/2, y+57, 15, col(id_)) + "</g>"
        return s
    def pill(id_, x, y, w, h, title, fs=14):
        c = " hl" if id_ in hl else ""
        return (f'<g id="{mid}-{id_}" class="node pill{c}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}"/>'
                f'<text class="t" x="{x+w/2}" y="{y+h/2+fs*0.36:.1f}" font-size="{fs}" text-anchor="middle">{html.escape(title)}</text></g>')
    def mpill(id_, x, y, w, h, src, px=14):
        c = " hl" if id_ in hl else ""
        gid = f' id="{mid}-{id_}"' if id_ else ""
        return (f'<g{gid} class="node pill{c}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}"/>'
                + m(src, x+w/2, y+h/2, px, col(id_)) + "</g>")
    def arrow(x1, y1, x2, y2):
        return f'<path class="arr" d="M{x1} {y1} L{x2} {y2}" marker-end="url(#{mid})"/>'

    p = [f'<svg class="{cls}" viewBox="0 0 1200 196" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The agent loop and the variable at each step">',
         f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" class="ahp"/></marker></defs>']
    # top band: model calls per step (set by the harness); time hidden by concurrency
    p.append(mpill("n-calls", 196, 2, 262, 24, r"J_i\ \mathrm{model\ calls\ in\ step}\ i", 15))
    p.append(arrow(338, 26, 338, 34))
    if big:
        p.append(txt(468, 19, "set by the harness — the program around the model", 12.5, "start", "f"))
    p.append(mpill("n-overlap", 868, 2, 328, 24, r"T_{\mathrm{saving}}\ \mathrm{=\ time\ hidden\ by\ concurrency}", 14))
    # main row
    p.append(node("n-observe", 14, 46, 128, 72, "Observe", "screenshot · page text", r"\mathrm{part\ of}\ E_i"))
    p.append(arrow(142, 82, 160, 82))
    c = " hl" if "n-decide" in hl else ""
    p.append(f'<g id="{mid}-n-decide" class="box{c}"><rect x="160" y="34" width="570" height="92" rx="8"/>'
             f'<text class="bt" x="172" y="50" font-size="12">DECIDE · the step’s model calls</text></g>')
    p.append(m(r"D_i=\sum_j \ell_{ij}", 722, 46, 13, anchor="end"))
    p.append(pill("n-queue", 172, 58, 90, 28, "queue", 13.5))
    p.append(pill("n-read", 272, 58, 206, 28, "prefill: read uncached input", 12.5))
    p.append(pill("n-write", 488, 58, 230, 28, "decode: write output, token by token", 12.5))
    p.append(f'<path class="brk" d="M174 93 L174 97 L476 97 L476 93"/>')
    p.append(m(r"\mathrm{TTFT}_{ij}", 325, 110, 14))
    p.append(m(r"n^{\mathrm{out}}_{ij}\,\mathrm{TPOT}_{ij}", 603, 108, 14))
    p.append(arrow(730, 82, 748, 82))
    p.append(node("n-act", 748, 46, 122, 72, "Act", "click · type · run a tool", r"\mathrm{part\ of}\ E_i"))
    p.append(arrow(870, 82, 886, 82))
    p.append(node("n-wait", 886, 46, 146, 72, "Wait", "page load · sleep · tool run", r"\mathrm{part\ of}\ E_i"))
    # exit: the agent stops (it says it is done, or hits the step cap); success is judged once, afterwards
    p.append(arrow(1032, 82, 1084, 82))
    p.append(txt(1066, 76, "stop", 10.5))
    p.append(node("n-succ", 1084, 46, 112, 72, "End", "judged afterwards", r"R_m(p)"))
    # token and price band
    p.append(m(r"o_{a,i}\ \mathrm{tokens}", 76, 146, 14))
    p.append(arrow(122, 146, 270, 146))
    p.append(mpill("n-rtok", 272, 134, 206, 24, r"|H_{a,i}|:\ \mathrm{hit,\ cache\ write,\ unc.}", 12.5))
    p.append(mpill("n-wtok", 488, 134, 118, 24, r"n^{\mathrm{out}}\ \mathrm{output}"))
    p.append(mpill("n-price", 614, 134, 104, 24, r"\times\ c_{\kappa}(\mu)"))
    p.append(mpill("n-machine", 886, 134, 146, 24, r"x_{\mathrm{env}}\ \mathrm{billed\ env.}", 13))
    # loop back: not stopped -> next step
    p.append(f'<path class="arr" d="M1058 82 L1058 180 L6 180 L6 82 L12 82" marker-end="url(#{mid})"/>')
    p.append(txt(1064, 172, "else", 10.5, "start"))
    p.append(mpill("n-steps", 250, 168, 150, 24, r"\times\ N\ \mathrm{steps}", 15))
    p.append(mpill("", 420, 168, 470, 24, r"\mathrm{next\ prompt:}\ |H_{a,i+1}|=|H_{a,i}|+|\Phi(z_{a,i})|+|o_{a,i}|\ \ \mathrm{(one\ call\ per\ step)}", 13))
    p.append("</svg>")
    return "".join(p)

# ---------------------------------------------------------------- formulas (LaTeX-style, typeset at build time)
# Everything mathematical on the pages — the two equations and every variable such as N, J_i, |H_{a,i}| — is typeset with
# matplotlib's mathtext (Computer Modern) into inline SVG, so the deck stays self-contained (no KaTeX at runtime).
EQ = {
 "time":    r"$T_{\mathrm{attempt}} \;=\; \sum_{i=0}^{N}\left(D_i + E_i\right) \;-\; T_{\mathrm{saving}}, \qquad D_i \;=\; \sum_{j=1}^{J_i}\ell_{ij}$",
 "call":    r"$\ell_{ij} \;\approx\; \mathrm{TTFT}_{ij} + n^{\mathrm{out}}_{ij}\,\mathrm{TPOT}_{ij}$",
 "saving":  r"$T_{\mathrm{saving}} \;\triangleq\; \mathcal{S}(\mathcal{M}) + \mathcal{S}(\mathcal{E}) - \mathcal{D}(\mathcal{M}\cup\mathcal{E})$",
 "ctx":     r"$|H_{a,i+1}| \;=\; |H_{a,i}| + |\Phi(z_{a,i})| + |o_{a,i}|$",
 "ctxsum":  r"$\sum_{i=1}^{N}|H_{a,i}| \;=\; N\,|H_{a,1}| + \dfrac{N(N-1)}{2}\,\bar{g}$",
 "money":   r"$c_m(p) \;=\; \sum_{i=0}^{N}\,\sum_{j=1}^{J_i}\,\sum_{\kappa\in K}\, n^{\kappa}_{ij}\,c_{\kappa}(\mu_{ij}) \;+\; x_{\mathrm{env}}\,c_{\mathrm{env}}$",
 "classes": r"$K \;=\; \{\mathrm{hit},\ \mathrm{w5m},\ \mathrm{w1h},\ \mathrm{unc},\ \mathrm{out}\}$",
 "succ":    r"$v(m,p) \;=\; \dfrac{C_m(p)}{R_m(p)}, \qquad \dfrac{\mathbb{E}[T_{\mathrm{attempt}}]}{R_m(p)}$",
 "goal":    r"$\mathrm{Pareto}_m\left(\dfrac{\mathbb{E}[T_{\mathrm{attempt}}]}{R_m(p)},\ v(m,p)\right)\quad \mathrm{s.t.}\quad R_m(p) \,\geq\, R_0$",
}
_TEX_CACHE = {}
_TEX_N = [0]
_MPL = None
def _mpl():
    global _MPL
    if _MPL is None:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib import mathtext
        from matplotlib.font_manager import FontProperties
        plt.rcParams["mathtext.fontset"] = "cm"
        plt.rcParams["svg.fonttype"] = "path"
        _MPL = (plt, mathtext, FontProperties)
    return _MPL

def _render_tex(src, pt, color, pad_in=0.02):
    """Returns (svg string with unique ids, width_pt, height_pt, depth_below_baseline_pt)."""
    plt, mathtext, FontProperties = _mpl()
    prop = FontProperties(size=pt)
    parser = mathtext.MathTextParser("path")
    w, h, d, _, _ = parser.parse(src, dpi=72, prop=prop)
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, src, fontsize=pt, color=color)
    import io
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=pad_in, transparent=True)
    plt.close(fig)
    svg = buf.getvalue()
    svg = svg[svg.find("<svg"):]
    svg = re.sub(r"<metadata>.*?</metadata>", "", svg, flags=re.S)
    _TEX_N[0] += 1
    uid = f"m{_TEX_N[0]}"
    ids = set(re.findall(r'id="([^"]+)"', svg))
    for i in sorted(ids, key=len, reverse=True):
        svg = svg.replace(f'id="{i}"', f'id="{uid}-{i}"').replace(f'href="#{i}"', f'href="#{uid}-{i}"').replace(f'url(#{i})', f'url(#{uid}-{i})')
    mw = re.search(r'width="([\d.]+)pt"', svg); mh = re.search(r'height="([\d.]+)pt"', svg)
    return svg, float(mw.group(1)), float(mh.group(1)), d + pad_in*72

def tex(src, px=14, color="#1b2733", cls="tex"):
    """Inline math for running text: `src` is LaTeX, px the surrounding font size."""
    if "$" not in src:
        src = "$" + src + "$"
    key = (src, px, color, cls)
    if key in _TEX_CACHE:
        return _TEX_CACHE[key]
    try:
        svg, w, h, d = _render_tex(src, px*0.9, color)
        out = svg.replace("<svg ", f'<svg class="{cls}" style="vertical-align:-{d:.2f}pt" ', 1)
    except Exception:
        out = f'<span class="eq-fallback">{html.escape(src)}</span>'
    _TEX_CACHE[key] = out
    return out

def nest_math(src, x, y, h, color="#1b2733", anchor="start"):
    """Math placed inside one of our own SVG diagrams: an <svg> child at (x, y) with height h (viewBox units). Returns (svg, width)."""
    if "$" not in src:
        src = "$" + src + "$"
    svg, w, hh, d = _render_tex(src, 12, color)
    ww = w * h / hh
    if anchor == "middle":
        x = x - ww/2
    svg = re.sub(r'<svg ([^>]*?)width="[\d.]+pt" height="[\d.]+pt"', lambda m: f'<svg {m.group(1)}x="{x:.1f}" y="{y:.1f}" width="{ww:.1f}" height="{h:.1f}"', svg, count=1)
    return svg, ww

def eq_svg(name, fontsize=17, cls="eq"):
    """One of the display equations, as an inline SVG block."""
    try:
        svg, w, h, d = _render_tex(EQ[name], fontsize, "#1b2733", pad_in=0.04)
        return svg.replace("<svg ", f'<svg class="{cls}" ', 1)
    except Exception:
        return f'<div class="eq-fallback">{html.escape(EQ[name])}</div>'

# ---------------------------------------------------------------- helpers
def esc(s):
    return html.escape(s, quote=False)

def card(k, v, d, c=""):
    """A card: mono key, bold value line, description, mono citation."""
    s = f'<div class="card"><div class="ck">{k}</div>'
    if v:
        s += f'<div class="cv">{v}</div>'
    if isinstance(d, (list, tuple)):
        s += '<ul class="cd">' + "".join(f"<li>{x}</li>" for x in d) + "</ul>"
    else:
        s += f'<div class="cd">{d}</div>'
    if c:
        s += f'<div class="cc">{c}</div>'
    return s + "</div>"

def table(headers, rows, widths=None, cls="tbl"):
    s = f'<table class="{cls}">'
    if widths:
        s += "<colgroup>" + "".join(f'<col style="width:{w}">' for w in widths) + "</colgroup>"
    s += "<thead><tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr></thead><tbody>"
    for r in rows:
        s += "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
    return s + "</tbody></table>"


def hbars(title, rows, caption="", labelw=150, width=380, maxv=None, height_row=22):
    """Horizontal bars: rows = [(label, value, shown_text)] — like the reference deck's share bars."""
    vals = [r[1] for r in rows]
    maxv = maxv or max(vals) or 1
    labelw = max(labelw, int(max(len(r[0]) for r in rows) * 7.0) + 14)
    valw = int(max(len(r[2]) for r in rows) * 7.0) + 12
    n = len(rows)
    h = 6 + n*height_row
    barw = max(40, width - labelw - valw)
    s = [f'<div class="fig"><div class="ft">{title}</div><svg class="hb" viewBox="0 0 {width} {h}" xmlns="http://www.w3.org/2000/svg">']
    for i, (lab, v, txt) in enumerate(rows):
        y = 4 + i*height_row
        bl = max(2, barw*v/maxv)
        s.append(f'<text class="hl-lab" x="{labelw-8}" y="{y+11}" text-anchor="end">{html.escape(lab)}</text>')
        s.append(f'<rect class="hl-bar" x="{labelw}" y="{y}" width="{bl:.1f}" height="14" rx="1"/>')
        s.append(f'<text class="hl-val" x="{labelw+bl+6:.1f}" y="{y+11}">{html.escape(txt)}</text>')
    s.append('</svg>')
    if caption:
        s.append(f'<div class="fc">{caption}</div>')
    return "".join(s) + "</div>"

def eq_strip():
    """The time of one attempt with the five classes of slowness mapped onto its terms (page 5)."""
    terms = [(tex(r"\sum_{i}\ [", 15), "I · steps"), (tex(r"\sum_{j \leq J_i}", 15), "II · calls per step"),
             (tex(r"(\mathrm{TTFT}_{ij} + n^{\mathrm{out}}_{ij}\,\mathrm{TPOT}_{ij})", 15), "III · each call"),
             (tex(r"+\ E_i\ ]", 15), "IV · non-model time"),
             (tex(r"-\ T_{\mathrm{saving}}", 15), "V · little runs concurrently")]
    s = ['<div class="eqstrip"><div class="eqt">' + tex(r"T_{\mathrm{attempt}} \approx", 15) + '</div>']
    for t, c in terms:
        s.append(f'<div class="eqterm"><div class="eqx">{t}</div><div class="eqc">{html.escape(c)}</div></div>')
    return "".join(s) + "</div>"

def cost_strip():
    """Money per success with the six classes of cost mapped onto its terms (page 11)."""
    terms = [(tex(r"\mathbb{E}[\ \sum_{i}\sum_{j \leq J_i}", 15), "3 · number of calls"),
             (tex(r"\sum_{\kappa}\,n^{\kappa}_{ij}", 15), "1, 2 · tokens by class"),
             (tex(r"c_{\kappa}(\mu_{ij})", 15), "5 · price per class"),
             (tex(r"+\ x_{\mathrm{env}}\,c_{\mathrm{env}}\ ]", 15), "6 · environment"),
             (tex(r"\div\ R_m(p)", 15), "4 · failures, retries")]
    out = ['<div class="eqstrip"><div class="eqt">' + tex(r"v(m,p) =", 15) + '</div>']
    for t, c in terms:
        out.append(f'<div class="eqterm"><div class="eqx">{t}</div><div class="eqc">{html.escape(c)}</div></div>')
    return "".join(out) + "</div>"

def link_fig():
    """Time and money of one attempt with terms coloured by their relationship (page 13)."""
    def pill(src, kind):
        col = "#ffffff" if kind == "same" else ("#b3600c" if kind == "buy" else "#3d4b58")
        return f'<span class="lp {kind}">{tex(src, 13, color=col)}</span>'
    def op(src):
        return tex(src, 13)
    t = [op(r"\approx"), pill(r"\sum_{i}", "same"), op(r"["), pill(r"\sum_{j}", "same"), op(r"("), pill(r"t^{\mathrm{queue}}_{ij}", "time"), op("+"),
         pill(r"t^{\mathrm{prefill}}_{ij}", "same"), op("+"), pill(r"n^{\mathrm{out}}_{ij}\,\mathrm{TPOT}_{ij}", "same"), op(r")\ +"),
         pill(r"E_i", "time"), op(r"]\ -"), pill(r"T_{\mathrm{saving}}", "time")]
    m = [op("="), pill(r"\sum_{i}", "same"), pill(r"\sum_{j}", "same"), pill(r"\sum_{\kappa}", "same"), pill(r"n^{\kappa}_{ij}", "same"),
         pill(r"c_{\kappa}(\mu_{ij})", "buy"), op(r"+"), pill(r"x_{\mathrm{env}}", "time"), pill(r"c_{\mathrm{env}}", "buy")]
    return ('<div class="linkfig"><div class="lrow"><span class="lk">time</span>' + " ".join(t) + '</div>'
            '<div class="lrow"><span class="lk">money</span>' + " ".join(m) + '</div>'
            '<div class="lleg"><span class="lp same">in both — same source</span><span class="lp time">time only, or money only through billed environment usage</span><span class="lp buy">the price — money for speed or accuracy</span></div></div>')

def defs(items, cols=3):
    """A grid of symbol definitions: [(latex, text), ...] — every symbol at its first appearance."""
    return (f'<div class="defs c{cols}">' + "".join(f'<div>{tex(a, 12)} <span>{b}</span></div>' for a, b in items) + '</div>')

def defs1(items):
    """defs2 in one column, for the gloss cell of an equation row."""
    return defs2(items).replace('<ul class="defs2">', '<ul class="defs2 one">', 1)

def defs2(items):
    """A bulleted glossary: [(latex, meaning, origin), ...]; the origin is 'as in …', 'adapted from …' or 'self-defined'."""
    return ('<ul class="defs2">' + "".join(f'<li>{tex(a, 12)} {b} <span class="src">({c})</span></li>' for a, b, c in items) + '</ul>')

SLIDES = []   # dicts: id, label, title, hl, crumb, callout(html), body(html), foot, chip(href,text), notes, kind

def slide(id_, title, body, *, label=None, hl=(), crumb="", callout="", foot="", chip=None, notes="", kind="main", cover=False, thumb=False, part=1):
    SLIDES.append(dict(id=id_, title=title, body=body, label=label, hl=hl, crumb=crumb, callout=callout,
                       foot=foot, chip=chip, notes=notes, kind=kind, cover=cover, thumb=thumb, part=part))

CITE = {   # short in-text forms, all in the reference list
    "osh": "Abhyankar, Qi &amp; Zhang, 2026",
    "osw2": "XLANG Lab, 2026",
    "skim": "Wong et al., 2026",
    "atts": "Lee et al., 2026",
    "copilot": "Liu et al., 2026",
    "bian": "Bian et al., 2025",
    "asb": "Chang et al., 2026",
    "thunder": "Kang et al., 2026",
    "yuan": "Yuan et al., 2026",
    "ufo2": "Zhang et al., 2026",
    "hal": "Kapoor et al., 2026",
    "tracelab": "Zhu et al., 2026",
    "anth-a": "Anthropic, 2026a",
    "anth-b": "Anthropic, 2026b",
    "openai": "OpenAI, 2026",
    "deepseek": "DeepSeek, 2026",
    "google": "Google, 2026",
    "xai": "xAI, 2026",
    "aa": "Artificial Analysis, 2026",
    "code": "xlang-ai, 2026",
    "jit": "Winston et al., 2026",
    "axis": "Lu et al., 2025",
    "bgym": "Le Sellier de Chezelles et al., 2025",
    "llmc": "Kim et al., 2024",
    "tokenpilot": "Xu et al., 2026",
    "aospec": "Chen et al., 2026",
    "swm": "Li et al., 2026",
    "kapoor25": "Kapoor et al., 2025",
    "cop": "Erol et al., 2026",
    "asyncfc": "Feng et al., 2026",
    "frugal": "Chen, Zaharia &amp; Zou, 2024",
    "agentix": "Luo et al., 2026",
    "speedrunner": "Huang et al., 2026",
    "specactions": "Ye et al., 2026",
}
def ci(*keys):
    return "(" + "; ".join(CITE[k] for k in keys) + ")"

# =====================================================================
# PART 1 — where the time and the money go
# =====================================================================

# --- 00 deck title (unnumbered) ---------------------------------------------
slide("s00", "Agent acceleration", kind="title", cover=True,
      body="""
<div class="cover cover-deck">
  <div class="cover-one">
    <h1 class="cover-title">Agent acceleration</h1>
    <p class="cover-sub">Making LLM agents that operate software finish a task in less time and for less money, without finishing fewer tasks.</p>
    <p class="cover-sub2">Computer-use, web and coding agents, which work a desktop, a browser or a code base one step at a time through a model.</p>
    <p class="cover-date">September 2026</p>
  </div>
</div>""")

# --- 01 Part 1 title ------------------------------------------------------------
slide("s01", "Where the time and the money go", cover=True,
      body="""
<div class="cover">
  <div class="cover-l">
    <div class="cover-kicker">Part 1</div>
    <h1 class="cover-title">Where the time and the money go</h1>
    <p class="cover-sub">Why LLM agents that operate software are slow and expensive, and how the two are linked.</p>
    <p class="cover-sub2">Every number comes from a published measurement of a computer-use, web or coding agent, or from a vendor’s own price page (2024–2026); the conditions of each measurement are stated next to it, and the full references are at the end of the part.</p>
  </div>
  <div class="cover-r">
    <div class="toc-t">In this part</div>
    <ol class="toc">
    <li><span>02</span>One attempt of an agent, step by step: the loop and its variables</li>
    <li><span>03–04</span>The problem, defined: time, the growing prompt, money, success and the goal</li>
    <li><span>05–10</span>Where the time goes, term by term</li>
    <li><span>11–12</span>Where the money goes, term by term, and per success</li>
    <li><span>13–14</span>How time and money are linked, and the levers</li>
    <li><span>15–16</span>References · Appendix A0–A5</li>
    </ol>
  </div>
</div>""")

# --- 02 the loop, the variable at each step, and how they add up -------------------
def eqrow(key, sub, eqs, gloss, cite, pg, stack=False, fs=10):
    eqhtml = "".join(eq_svg(e, fontsize=fs, cls="eqn") for e in eqs)
    return (f'<div class="eqk">{key}<span>{sub}</span><span class="eqpg">{pg}</span></div><div class="eqm{" col" if stack else ""}">{eqhtml}</div>'
            f'<div class="eqg"><div>{gloss}</div><div class="eqcite">{cite}</div></div>')

slide("s02", "One attempt of an agent, step by step",
      crumb="here: the loop one attempt runs, and the variable at each step → to: the formulas built from them",
      callout=f"""<p><b>One attempt is {tex("N", 15)} steps; each step is some model calls plus everything that is not a model call.</b> Every variable below is defined here once; pages 3–4 add them up.</p>""",
      body=f"""
<div class="fig-loop2">{loop_svg(cls="big-svg", big=True)}</div>
{defs2([
  (r"i,\ N", "step (one observe–decide–act–wait round); steps in the attempt", "i as in " + CITE['aospec'] + "; " + CITE['yuan'] + " · N self-defined"),
  (r"J_i,\ j", "model calls in step " + tex("i", 12) + " (planner, judge, retries …); call index", "self-defined"),
  (r"\ell_{ij}", "latency of call " + tex("j", 12) + " of step " + tex("i", 12), "ℓ as in " + CITE['swm'] + " · indices self-defined"),
  (r"\mathrm{TTFT}_{ij}", "time to the first generated token: queueing, sending, prefill of the uncached input", "as in " + CITE['aa']),
  (r"n^{\mathrm{out}}_{ij},\ \mathrm{TPOT}_{ij}", "output tokens of the call, thinking included; time per output token after the first", "n as in " + CITE['cop'] + " · TPOT as in " + CITE['aospec']),
  (r"D_i,\ E_i", "model time of step " + tex("i", 12) + "; all its other time (observe, act, wait, harness gaps, back-off)", "D_i adapted from " + CITE['aospec'] + " · E_i self-defined, replacing their T_i"),
  (r"T_{\mathrm{saving}}", "time hidden because some of it ran at the same time; 0 if strictly serial", "adapted from " + CITE['asyncfc'] + ", intervals widened"),
  (r"o_{a,i},\ a", "tokens the result or screenshot of step " + tex("i", 12) + " adds to the prompt; agent index", "as in " + CITE['yuan']),
  (r"|H_{a,i}|,\ \Phi,\ z_{a,i}", "length of the prompt step " + tex("i", 12) + "’s call reads (one call per step); chat template; the call’s output: thinking, message and tool-call tokens", "H, Φ as in " + CITE['yuan'] + " · z self-defined for their (θ, m, u) = (thinking, message, tool call)"),
  (r"n^{\mathrm{hit}},\ n^{\mathrm{w}},\ n^{\mathrm{unc}}", "input tokens read from the cache, written to it (5-min or 1-h), or uncached; " + tex(r"n^{\mathrm{w}}=n^{\mathrm{w5m}}+n^{\mathrm{w1h}}", 12), "classes as billed by " + CITE['anth-b'] + " · hit as in " + CITE['tokenpilot'] + " · unc as in " + CITE['speedrunner']),
  (r"c_{\kappa}(\mu),\ \kappa,\ \mu", "price per token of billing class " + tex(r"\kappa", 12) + " on serving model " + tex(r"\mu", 12), "c adapted from " + CITE['cop'] + " · κ, μ self-defined"),
  (r"x_{\mathrm{env}}", "billed environment usage (e.g. sandbox hours)", "x as in " + CITE['cop'] + ", App. D.1 · env self-defined"),
  (r"R_m(p),\ m,\ p", "probability that one attempt of design " + tex("m", 12) + " (model + harness) on task " + tex("p", 12) + " succeeds", "as in " + CITE['cop']),
  (r"\mathrm{reading,\ writing}", "reading = prefill of input tokens; writing = decoding output tokens (a cache write is storage)", "self-defined wording"),
])}""",
      foot="SOURCES · after each symbol, its origin: “as in” = the source’s own symbol and meaning; “adapted from” = renamed or widened, reasons in Appendix A0; self-defined = used by no source · table with locations: Appendix A0 · 4/5",
      chip=("#a0-4", "Appendix A0"))

slide("s03", "The problem, defined (1/2): the time of one attempt, and the growing prompt",
      crumb="from the loop → here: time as a sum over steps and calls, and why the prompt grows → to: money, success and the goal",
      body=f"""
<div class="statusleg">each row says whether it is <b>verbatim</b> from its source, <b>adapted</b> (reason in Appendix A0) or <b>our distillation</b> (no source writes it as a formula) · calc. = our algebra</div>
<div class="eqtab narroweq">
{eqrow("time", "one attempt", ["time", "call", "saving"],
       defs1([
        (r"T_{\mathrm{attempt}}", "wall-clock time of one attempt: the real time that passes from handing over the task to getting the result, so work done at the same time counts once", "self-defined"),
        (r"i=0", "a step-0 bucket for calls outside any step, e.g. a plan made before step 1", "self-defined"),
        (r"\mathcal{M},\ \mathcal{E}", "the time intervals in the trace when a model call is running; when anything else is", "adapted from " + CITE['asyncfc'] + ": decoding and function intervals"),
        (r"\mathcal{S}(\cdot),\ \mathcal{D}(\cdot)", "intervals’ lengths added up (overlap counted twice); length of their union (overlap counted once) — not the model time " + tex("D_i", 12) + ". A 2-s tool call run during a model call: " + tex(r"T_{\mathrm{saving}}", 12) + " = 2 s", "as in " + CITE['asyncfc']),
        (r"\triangleq", "“defined as”", "standard notation"),
        (r"D_i,\ E_i,\ \ell_{ij},\ \mathrm{TTFT},\ n^{\mathrm{out}},\ \mathrm{TPOT}", "as on page 2", "origins there"),
       ]),
       "sum: " + CITE['aospec'] + " · calls within a step: our distillation, evidence " + CITE['osh'] + " · call: " + CITE['aa'] + " (third-party) · saving: " + CITE['asyncfc'] + ", intervals widened", "adapted · our distillation", stack=True, fs=12.5)}
{eqrow("prompt", "grows", ["ctx", "ctxsum"],
       defs1([
        (r"|H_{a,i+1}|", "each step appends its output and its result to the next prompt (one call per step, full history kept); symbols as on page 2", "adapted from " + CITE['yuan'] + ", lengths of its Eq. 3"),
        (r"|H_{a,1}|", "the first prompt (system prompt and task); the left-hand sum is all prompt tokens read over the attempt", "self-defined"),
        (r"g_i,\ \bar{g}", "tokens step " + tex("i", 12) + " adds, " + tex(r"g_i=|\Phi(z_{a,i})|+|o_{a,i}|", 12) + "; their mean, weighted by the " + tex("N-i", 12) + " later steps that re-read them", "self-defined (calc.)"),
        (r"N^{*}=2|H_{a,1}|/\bar{g}+1", "the step count beyond which the " + tex("N^2", 12) + " term outweighs " + tex(r"N|H_{a,1}|", 12), "self-defined (calc.)"),
       ]),
       "recurrence: " + CITE['yuan'] + " (lengths of its Eq. 3) · sum: our distillation (calc.) · re-sent history, measured: " + CITE['osh'], "adapted · our distillation (calc.)", stack=True, fs=12.5)}
</div>""",
      foot="SOURCES · as cited in each row · simplified: one call per step in the prompt row; times are per attempt, not distributions — Appendix A0",
      chip=("#a0-1", "Appendix A0"))

slide("s04", "The problem, defined (2/2): the money of one attempt, per success, and the goal",
      crumb="from time and the prompt → here: money, cost and time per success, and what counts as acceleration → to: where the time goes",
      body=f"""
<div class="statusleg">verbatim · adapted · our distillation, as on page 3 · calc. = our algebra</div>
<div class="eqtab">
{eqrow("money", "one attempt", ["money", "classes"],
       tex("c_m(p)", 11) + ": dollars of one attempt of design " + tex("m", 11) + " (model and harness) on task " + tex("p", 11) + ". " + tex(r"n^{\kappa}_{ij}", 11) + ": tokens of class " + tex(r"\kappa", 11) + " in call " + tex("j", 11) + " of step " + tex("i", 11) + " — cache hit, 5-min or 1-h cache write, uncached input, output. " + tex(r"c_{\mathrm{env}}", 11) + ": price per unit of billed environment usage.",
       "base: " + CITE['cop'] + ", Eq. 13, extended as its App. D.1 allows · classes: " + CITE['anth-b'] + " · three-class precedent: " + CITE['tokenpilot'], "adapted", stack=True, fs=12.5)}
{eqrow("success", "per success", ["succ"],
       tex("v(m,p)", 11) + ": expected dollars per success; the second term: expected seconds per success. " + tex("C_m(p)", 11) + ": expected " + tex("c_m(p)", 11) + " over all attempts, failures included; " + tex(r"\mathbb{E}", 11) + ": expectation. Independent attempts, retried one after another until a verified success (" + tex("1/R_m(p)", 11) + " on average); the verifier’s time and cost count in every attempt.",
       "money: " + CITE['cop'] + ", Eq. 2 (verbatim) · time: same derivation in seconds, as its App. D.1 allows (adapted)", "verbatim · adapted", stack=True, fs=12.5)}
{eqrow("goal", "acceleration", ["goal"],
       "Among designs that succeed at least " + tex("R_0", 11) + " of the time, keep those no other design beats on both time and money per success; the reference is a person doing the task today. Per task " + tex("p", 11) + "; over a task mix, " + tex(r"\sum_p C_m(p)/\sum_p R_m(p)", 11) + ".",
       "distilled from " + CITE['kapoor25'] + " (“jointly optimizing the two metrics”, arXiv v1) and " + CITE['cop'] + " (App. C.8: leave unreliable systems off the frontier)", "our distillation", fs=12.5)}
</div>
{card("WHAT THE FORMULAS DO NOT SHOW: THE VARIABLES ARE COUPLED", "",
      ["The prompt length drives both sides: prefill time and the input bill " + ci('osh'),
       "The harness and provider, not the model, set the cache split " + ci('tracelab'),
       "Time can cost money: a cache entry expires after 5 min or 1 h, so a slow step can turn cache reads into cache writes (our reading of " + CITE['anth-b'] + ")",
       "Thinking lengthens " + tex("D_i", 11) + " and the output bill; calls and thinking change " + tex("R_m(p)", 11) + " (page 13)"])}""",
      foot="SOURCES · as cited in each row · assumptions: independent attempts, retry until verified success, prices constant in context length (checked for Anthropic) — Appendix A0",
      chip=("#a0-3", "Appendix A0"))

# --- 05 time, term by term ---------------------------------------------------
slide("s05", "Where the time goes: five classes, one per term",
      hl=("n-steps", "n-calls", "n-queue", "n-read", "n-write", "n-observe", "n-act", "n-wait", "n-overlap"),
      crumb="from the definition → here: the terms of the time of one attempt, each with one measurement → to: steps and calls",
      callout=f"""<p><b>Four of the five are terms of the time equation; the fifth is how they combine: the concurrency term {tex(r"T_{\mathrm{saving}}", 15)} is small in the one production trace that reports it, so the terms nearly add.</b> Which class dominates depends on the harness, not on the kind of agent (page 10). Cause-by-cause tables with measurement conditions: Appendix A1.</p>""",
      body=f"""
{eq_strip()}
<div class="rows5 big">
  {card("I · TOO MANY STEPS " + tex("(N)", 11), "Hour-scale tasks take hundreds of steps, and every step is a full round trip",
        ["318 tool calls per task on OSWorld 2.0 — 108 desktop tasks, Claude Opus 4.7, one action per step"], ci('osw2'))}
  {card("II · TOO MANY CALLS PER STEP " + tex("(J_i)", 11), "A harness that plans, judges and reflects multiplies every step",
        ["4–12 planning calls per judging call — GTA1 harness: four parallel planners, up to three retries, one judge"], ci('osh'))}
  {card("III · EACH CALL IS SLOW " + tex(r"(\ell_{ij})", 11), "Inside a call, waiting, reading and writing are three separate delays",
        ["Writing, one token at a time, is 91–98.6% of model time — local 27–31B models with a warm cache"], ci('yuan'))}
  {card("IV · NON-MODEL TIME " + tex("(E_i)", 11), "The environment costs time whether or not the model is running",
        ["6.6 s per browser action vs 4.7 s per model call, median — 151 WebVoyager live-site tasks, GPT-4o"], ci('skim'))}
  {card("V · LITTLE RUNS CONCURRENTLY " + tex(r"(T_{\mathrm{saving}})", 11), "Almost nothing overlaps, so task time is close to a sum: fixing one term saves only its own share",
        ["Concurrency within a turn: 1.15 — GitHub Copilot production telemetry"], ci('copilot'))}
</div>""",
      foot="SOURCES · one representative number per class; conditions on pages 6–9 and in Appendix A1",
      chip=("#a1-1", "Appendix A1"))

# --- 06 steps and calls ---------------------------------------------------------
slide("s06", "I–II · Too many steps, too many calls per step",
      hl=("n-steps", "n-calls"),
      crumb="from the five classes → here: the two sums, steps and calls per step → to: what happens inside a call",
      callout=f"""<p><b>{tex("N", 15)} multiplies every term, and {tex("J_i", 15)} multiplies {tex("N", 15)}.</b> Steps accumulate because tasks are long, each step does one action, navigation-only steps still go through the model, and the agent idles or loops; calls accumulate because the harness plans, judges and reflects, or samples several candidates per step.</p>""",
      body=f"""
<div class="cards4">
  {card("I-1, I-2 · LONG TASKS, ONE ACTION PER STEP", "Long tasks with one action per step need hundreds of steps; several actions per call cut them by half or more",
        ["318 tool calls per task with one action per step, 160.7 with several actions per call — OSWorld 2.0, 108 long tasks, Claude Opus 4.7"], ci('osw2'))}
  {card("I-3 · NAVIGATION-ONLY STEPS", "Most steps are navigation that needs no thinking, yet each one is a model call",
        ["66.7% of the steps in the median task are pure navigation — 151 WebVoyager tasks on live websites, three text agents driven by GPT-4o"], ci('skim'))}
  {card("I-4 · IDLING AND DEAD LOOPS", "When an agent is stuck, every repeated step is billed and timed in full",
        ["One element-locating loop repeated a step 18 times: 27 minutes and $8.47 at list price without caching — GTA1 harness, OSWorld"], ci('osh'))}
  {card("II · PLANNING, JUDGING, SAMPLING", "Extra calls per step buy accuracy at a rising token cost per point",
        ["10 candidates per step instead of 1: 38.8% → 43.2% success for 96K → 920K tokens per task — gpt-oss-120b, 165 WebArena-Lite tasks"], ci('atts'))}
</div>
<div class="figs1">
  {hbars("Steps per task on OSWorld 2.0, 108 tasks", [("Opus 4.7 · one action per step",318,"318"),("Opus 4.7 · batched actions",160.7,"160.7"),("Opus 4.8 · batched",103,"103"),("GPT-5.5 · batched",95.2,"95.2")], "XLANG Lab, 2026 · mean over tasks", width=600)}
</div>""",
      foot=f"SOURCES · {CITE['osw2']} · {CITE['skim']} · {CITE['osh']} · {CITE['atts']} — full rows with conditions in Appendix A1",
      chip=("#a1-1", "Appendix A1"))

# --- 07 inside a call -------------------------------------------------------------
slide("s07", "III · Inside one call: first token, then decoding",
      crumb="from the two sums → here: the latency of one call, TTFT plus decoding → to: why the prompt keeps growing",
      callout=f"""<p><b>A call waits in a queue, reads its uncached input, then writes its output one token at a time: {tex(r"\ell_{ij} \approx \mathrm{TTFT}_{ij} + n^{\mathrm{out}}_{ij}\,\mathrm{TPOT}_{ij}", 15)}.</b> Queueing depends on the provider, reading on the prompt, writing on how much the model writes, thinking included.</p>""",
      body=f"""
<div class="cards4">
  {card("III-1 · QUEUEING", "The same request can wait far longer depending on the provider's load",
        ["Identical requests take up to 69× longer depending on the time of day — 15 models, 5 providers"], ci('bian'))}
  {card("III-2 · PREFILL", "For screenshot agents, reading the prompt dominates a call, and the prompt grows every step",
        ["Planning, judging and reflection latency is “dominated by the prefill stage” — GTA1 and Agent S2 harnesses, 39 OSWorld tasks"], ci('osh'))}
  {card("III-3 · DECODING", "Writing is the slowest segment per token, and thinking modes write far more tokens",
        ["224K vs 37K output tokens per task — Claude Opus 4.8 vs GPT-5.5 on the same 108 OSWorld 2.0 tasks",
         "Writing is 91–98.6% of model time — local 27–31B models with a warm cache"], ci('osw2','yuan'))}
  {card("HOW TTFT IS MEASURED", "Published first-token times lump queueing, network and prefill together",
        ["Time to first token is measured from the request being sent and “includes network latency”; output speed excludes the first chunk"], ci('aa'))}
</div>""",
      foot=f"SOURCES · {CITE['bian']} · {CITE['osh']} · {CITE['osw2']} · {CITE['yuan']} · {CITE['aa']} (third-party measurement definitions) — full rows in Appendix A1",
      chip=("#a1-2", "Appendix A1"))

# --- 08 the prompt grows ---------------------------------------------------------
slide("s08", "The prompt grows: every step re-reads the whole history",
      crumb="from one call → here: the prompt row of page 3, measured → to: the time outside the model",
      callout=f"""<p><b>Each step appends its output and its result, so the tokens read over an attempt grow with {tex("N^2", 15)}; caching makes re-reading cheaper and faster, not free.</b> The square matters once {tex("N", 15)} passes a few dozen steps.</p>""",
      body=f"""
<div class="cards4">
  {card("HISTORY RE-SENT", "Most computer-use agents send the whole history at every step",
        ["“At each step, the prompt sent to the LLM includes the history of all previous steps”; later steps take up to 3× longer — GTA1 harness, 39 OSWorld tasks"], ci('osh'))}
  {card("SCREENSHOTS ARE THE BULK", "One screenshot adds about a thousand tokens to every later prompt",
        ["A 1280×720 screenshot is 46 × 26 = 1,196 tokens on Claude, one token per 28×28-pixel patch (calc.)"], ci('anth-b'))}
  {card("CACHED, STILL PAID", "A high cache hit rate lowers the price of re-reading, but the prefix stays the larger part of the bill",
        ["95.7% hit rate, yet prefix tokens are 59.5% of the list-price cost — 4,265 Claude Code / Codex sessions"], ci('tracelab'))}
  {card("WHEN THE SQUARE BITES", "Below a few dozen steps the first prompt dominates; long tasks are deep in the square",
        [tex(r"N^{*}=2|H_{a,1}|/\bar{g}+1", 11) + ": a 6,000-token first prompt and 1,500 tokens added per step give " + tex(r"N^{*}=9", 11) + " (calc., assumed values); OSWorld 2.0 tasks take about 318 steps"], ci('osw2'))}
</div>
<div class="figcap">Per step, the pressure on prefill is the appended part, not the whole prompt: with a warm cache, “the relevant per-turn prefill pressure is better captured by incremental appends” {ci('yuan')}.</div>""",
      foot=f"SOURCES · {CITE['osh']} · {CITE['anth-b']} · {CITE['tracelab']} · {CITE['osw2']} · {CITE['yuan']} — the growth rows with conditions are in Appendix A3",
      chip=("#a3-1", "Appendix A3"))

# --- 09 non-model time and concurrency --------------------------------------------
slide("s09", "IV–V · The time outside the model, and how little of it overlaps",
      crumb="from the prompt → here: non-model time and concurrency → to: which term dominates",
      callout=f"""<p><b>The environment is slow, and today's agents run almost everything in sequence, so {tex(r"T_{\mathrm{saving}}", 15)} is small and the attempt time is close to the full sum.</b> Published “total times” differ in what they count, so the boundary has to be stated.</p>""",
      body=f"""
<div class="two">
  <div class="stack">
  {card("IV · NON-MODEL TIME", "The environment is slow on its own, and the benchmarks add fixed sleeps on top",
        ["OSWorld 2.0 sleeps 3 s after every action: × 318 steps ≈ 16 min of pure waiting per task (calc.)",
         "6.6 s per browser action vs 4.7 s per model call, median — 151 WebVoyager live-site tasks, GPT-4o"], ci('osw2','code','skim'))}
  {card("V · CONCURRENCY", "Almost nothing overlaps, so fixing one term saves only its own share",
        ["Concurrency within a turn: 1.15 — GitHub Copilot production telemetry"], ci('copilot'))}
  </div>
  <div class="stack">
  {hbars("Where a Claude Code / Codex request’s 4.3 minutes go", [("tools",59.8,"59.8%"),("model",41.0,"41.0%")], "Zhu et al., 2026 · 4,265 sessions, 43 developers", maxv=100, width=560, labelw=60)}
  {card("WHAT A “TOTAL TIME” COUNTS", "Some published times include the person, others exclude them",
        ["80–92% of a coding session’s elapsed time is the person thinking between turns, outside any one attempt"], ci('copilot','tracelab'))}
  </div>
</div>""",
      foot=f"SOURCES · {CITE['osw2']} · {CITE['code']} · {CITE['skim']} · {CITE['copilot']} · {CITE['tracelab']} — full rows in Appendix A1",
      chip=("#a1-3", "Appendix A1"))

# --- 10 which term dominates -------------------------------------------------------
slide("s10", "Which term dominates depends on the harness, not on the kind of agent",
      hl=("n-read", "n-wait", "n-write"),
      crumb="from the five terms → here: their shares, per kind of agent → to: where the money goes",
      callout=f"""<p><b>All five classes exist in every agent; the heaviest term differs, and it flips when the harness changes.</b></p>""",
      body=f"""
<table class="tbl three">
<colgroup><col style="width:10%"><col style="width:30%"><col style="width:30%"><col style="width:30%"></colgroup>
<thead><tr><th></th><th>Screenshot desktop agent, multi-call harness</th><th>Text web agent</th><th>Coding agent with a prompt cache</th></tr></thead>
<tbody>
<tr><td class="rk">heaviest</td>
<td><b>Reading × calls per step × steps.</b> 87–97% of task time is planning, judging and reflection calls (GTA1, Agent S2; 39 OSWorld tasks) {ci('osh')}</td>
<td><b>Browser execution and waiting.</b> Per step, median: browser 6.6 s, model 4.7 s (151 WebVoyager live-site tasks, GPT-4o) {ci('skim')}</td>
<td><b>Writing, or tool tails.</b> Writing is 91–98.6% of model time {ci('yuan')}; in Claude Code / Codex requests tools take 59.8%, the model 41.0% {ci('tracelab')}</td></tr>
<tr><td class="rk">flips when</td>
<td>The harness makes one call per step: over 70% of the time is then the sandbox, because the benchmark sleeps 2–3 s after every action {ci('asb','code','osw2')}</td>
<td>The observation grows: 4.8× the input moved the model’s share of step time from 46.9% to 61.6% {ci('asb')}</td>
<td>Load evicts the cache: latency up to 7.14× {ci('thunder')}</td></tr>
<tr><td class="rk">in one line</td>
<td>Slow in reading: every step re-reads the growing screenshot history</td>
<td>Slow in the environment — until the observation grows, then slow in reading</td>
<td>Reading is cached away; slow in writing and in the tools</td></tr>
</tbody></table>
<div class="concl">
  <div><b>1 · The harness sets the dominant term</b> — calls per step, observation size, fixed sleeps, cache on or off. The explanation “agents are slow because inference is slow” is accurate only for multi-call screenshot agents.</div>
  <div><b>2 · {tex("N", 14)} multiplies every term</b> — one step fewer saves a whole step of time and money in all three kinds.</div>
</div>""",
      foot="SOURCES · as cited in each cell; the same table with every measurement condition is Appendix A2",
      chip=("#a2-1", "Appendix A2"))

# --- 11 money, term by term ---------------------------------------------------------
slide("s11", "Where the money goes: six classes, one per term",
      hl=("n-rtok", "n-wtok", "n-price", "n-succ", "n-calls", "n-steps", "n-machine"),
      crumb="from where the time goes → here: the terms of money per success, each with one measurement → to: per attempt vs per success",
      callout=f"""<p><b>Money comes from tokens read and tokens written, each times a price, plus billed environment usage, which is usually small.</b> Writing costs 5× reading; a cached read costs a small fraction of a normal read (DeepSeek-V4.1-Flash: $0.006 vs $0.30 per million tokens); fast mode costs 2× {ci('anth-b','openai','deepseek')}.</p>""",
      body=f"""
{cost_strip()}
<div class="rows6">
  {card("1 · TOKENS READ", "Reading is the larger bill and grows with the square of the steps",
        ["Even at a 95.7% cache hit rate, prefix tokens are still 59.5% of the bill — 4,265 Claude Code / Codex sessions"], ci('tracelab'))}
  {card("2 · TOKENS WRITTEN", "Writing is the dearer token, thinking included, but the smaller bill",
        ["31% of an uncached screenshot agent’s bill: $2.43 counting output only vs $7.87 counting all tokens — GTA1, 39 OSWorld tasks (calc.)"], ci('osh'))}
  {card("3 · NUMBER OF CALLS", "The calls that make the agent slow also make it expensive",
        ["5–13× the calls of a single-call harness per step — GTA1: planners, retries and a judge (calc.)"], ci('osh'))}
  {card("4 · FAILURES AND RETRIES", "Failed attempts are billed in full",
        ["$72.4 per attempt ÷ 20.6% completion ≈ $351 per success — OSWorld 2.0, best agent (calc.)"], ci('osw2'))}
  {card("5 · UNIT PRICE", "The price list sets the constant; fast tiers double it",
        ["Claude Opus 5.5 $4 / $20 vs GPT-6 Luna $0.10 / $0.50 per million tokens read / written — a 40× spread (calc.)"], ci('anth-b','openai'))}
  {card("6 · THE ENVIRONMENT MACHINE", "Published costs are API bills only; a CPU environment adds little",
        ["$0.02–0.36 for a one-hour CPU environment: 0.3–4.6% of a $7.87 bill (calc.; next page)"], "vendor price pages, read 2026-09-27")}
</div>""",
      foot="SOURCES · one representative number per class; the complete tables with conditions are in Appendix A3",
      chip=("#a3-1", "Appendix A3"))

# --- 12 per success, conventions, environment ----------------------------------------
slide("s12", "Four accounting conventions for one task, and the cost of the environment machine",
      hl=("n-price", "n-succ", "n-machine"),
      crumb="from the six classes → here: per attempt vs per success, which convention a figure uses, and the environment → to: how time and money are linked",
      callout="""<p><b>The same run’s cost differs by up to 30× across the four conventions in use, and none includes the environment machine.</b></p>""",
      body=f"""
<div class="two">
  <div>
  <table class="tbl conv">
  <colgroup><col style="width:30%"><col style="width:55%"><col style="width:15%"></colgroup>
  <thead><tr><th>convention</th><th>the same run, counted both ways</th><th>gap</th></tr></thead>
  <tbody>
  <tr><td class="rk">output only vs all tokens</td><td>GTA1 on 39 OSWorld tasks, o3 list price, no cache: $2.43 counting output only; $7.87 counting all tokens {ci('osh')}</td><td>3.2×</td></tr>
  <tr><td class="rk">per attempt vs per success</td><td>OSWorld 2.0, Claude Opus 4.8: $72.4 per attempt at 20.6% completion → ≈ $351 (calc.; a benchmark average) {ci('osw2')}</td><td>4.9×</td></tr>
  <tr><td class="rk">uncached vs cached</td><td>A cached read costs a fraction of a normal read (DeepSeek-V4.1-Flash: $0.006 vs $0.30 per million tokens; other vendors in A3) {ci('deepseek')}</td><td>4–50× on the read price only, by vendor (calc.)</td></tr>
  <tr><td class="rk">standard vs fast mode</td><td>Claude Opus 5.5 $4 / $20 → $8 / $40; OpenAI 2× on every listed model; up to 2.5× faster writing (vendor-stated), reading unchanged {ci('anth-b','openai')}</td><td>2×</td></tr>
  </tbody></table>
  <div class="figcap">The three that apply to a whole bill compound to about 31× (3.2 × 4.9 × 2, calc.). Screenshot-agent measurements do not report their cache state.</div>
  </div>
  <div class="stack">
    {card("6 · THE ENVIRONMENT MACHINE, FROM LIST PRICES", "For CPU environments the machine is a small addition; idle time, proxy traffic and GPUs change that",
          ["An H100 sandbox at $3.95 per hour is already half of a $7.87 bill, and hourly billing runs while the agent waits — the median AgentSysBench session is active only 20% of its lifetime"], "vendor price pages, read 2026-09-27; " + CITE['asb'])}
    {hbars("A one-hour CPU environment as a share of a $7.87 API bill (calc.)", [("Browser Use cloud browser",0.25,"0.25%"),("AWS t3.medium",0.5,"0.5%"),("Browserbase",1.5,"1.5%"),("E2B / Daytona 2 vCPU",2.1,"2.1%"),("Modal 2 vCPU",3.0,"3.0%"),("AWS t3.2xlarge (OSWorld 2.0)",4.2,"4.2%"),("OpenAI hosted container 4 GB",4.6,"4.6%")], "vendor price pages, read 2026-09-27 · full price table in Appendix A3", width=520, height_row=17)}
  </div>
</div>""",
      foot=f"SOURCES · {CITE['osh']} · {CITE['osw2']} · {CITE['asb']} · {CITE['anth-b']} · {CITE['openai']} · {CITE['deepseek']} · AWS, Browser Use, Browserbase, E2B, Daytona, Modal, OpenAI price pages",
      chip=("#a3-3", "Appendix A3"))

# --- 13 how time and money are linked -------------------------------------------------
slide("s13", "How slow and expensive are linked: three kinds of relationship",
      hl=("n-rtok", "n-wtok", "n-queue", "n-wait", "n-machine"),
      crumb="from the two sides → here: what each term does to time and to money → to: the levers",
      callout="""<p><b>Time and money share the token counts; queueing and environment time reach money only through billed environment usage — and through the cache, which expires while the agent waits.</b></p>""",
      body=f"""
{link_fig()}
{defs([(r"t^{\mathrm{queue}}_{ij},\ t^{\mathrm{prefill}}_{ij}", "the queueing and prefill parts of " + tex(r"\mathrm{TTFT}_{ij}", 12) + " (our split; network and first-token time left out; Appendix A0)"), (r"\mathrm{time},\ \mathrm{money}", "one attempt each; divide by " + tex("R_m(p)", 12) + " for per success")], cols=2)}
<div class="cards4 rel">
  {card("SAME SOURCE — in both equations", "fix it, and time and money fall together",
        ["Steps " + tex("N", 13) + ", calls per step " + tex("J_i", 13) + ", reading, writing, cache hits, failures — every one of them lives in the token counts"], ci('osh','anth-b'))}
  {card("SLOW BUT NOT EXPENSIVE — no tokens, only machine hours", "fix it, and only time falls",
        ["Queueing, page loads, fixed sleeps, tool tails — none produces a token; the machine behind them is billed by the hour, usually under 5% of the API bill"])}
  {card("MONEY FOR TIME OR FOR ACCURACY — opposite signs", "paying for speed shortens only the writing segment; paying for accuracy costs more tokens per point as accuracy rises",
        ["Fast mode: up to 2.5× faster writing (vendor-stated) at 2× the price, reading unchanged"], "(" + CITE['anth-b'] + "; " + CITE['openai'] + "; accuracy: Appendix A4)")}
  {card("TIME THAT COSTS MONEY — the cache expires", "a slow step or a long pause can turn cheap cache reads into cache writes",
        ["A cache entry lives 5 minutes or 1 hour from the start of the last request that read or wrote it; at most 12.8% of cost could be saved if the cache survived human pauses"], ci('anth-b','tracelab'))}
</div>""",
      foot=f"SOURCES · {CITE['osh']} · {CITE['anth-b']} · {CITE['openai']} · {CITE['tracelab']} — the cause-by-cause table, with the convexity evidence, is Appendix A4",
      chip=("#a4-1", "Appendix A4"))

# --- 14 levers + gaps ------------------------------------------------------------------
slide("s14", "The levers, and what is still unmeasured",
      hl=("n-steps", "n-calls", "n-read", "n-write", "n-wait", "n-price", "n-overlap"),
      crumb="from how time and money are linked → here: what fixing each lever buys, and the holes in the evidence → to: Part 2, what the literature has done with each lever",
      callout="""<p><b>Seven levers follow from the formulas; each moves one term and carries a known risk.</b> Part 2 asks how far the literature has pushed each. Right: gaps in the evidence, not claims of a research gap.</p>""",
      body=f"""
<div class="levgrid">
  <table class="tbl lev">
  <colgroup><col style="width:40%"><col style="width:12%"><col style="width:18%"><col style="width:30%"></colgroup>
  <thead><tr><th>lever</th><th>time</th><th>money</th><th>the catch</th></tr></thead>
  <tbody>
  <tr><td><b>Fewer steps</b> {tex("N", 12)} — several actions per call, skip navigation-only steps</td><td>yes</td><td>yes, the quadratic term</td><td>which steps need no thinking?</td></tr>
  <tr><td><b>Read less</b> {tex(r"|H_{a,i}|,\ n^{\mathrm{unc}}", 12)} — trim history, shrink screenshots, cache the prefix</td><td>yes</td><td>yes</td><td>forgets; trimming invalidates the cache</td></tr>
  <tr><td><b>Write less</b> {tex(r"n^{\mathrm{out}}", 12)} — less thinking, smaller model</td><td>yes</td><td>yes</td><td>accuracy may fall</td></tr>
  <tr><td><b>Fewer calls per step</b> {tex("J_i", 12)} — drop judging and reflection</td><td>yes</td><td>yes</td><td>fewer errors caught</td></tr>
  <tr><td><b>Overlap the waiting</b> {tex(r"T_{\mathrm{saving}}", 12)} — pre-load, parallel tools, page-ready events</td><td>yes</td><td>no</td><td>only where the environment dominates</td></tr>
  <tr><td><b>Buy a fast or priority tier</b> {tex(r"\mathrm{TPOT},\ c_{\kappa}", 12)}</td><td>writing only</td><td>no — 2× more</td><td>reading unchanged; cache dropped</td></tr>
  <tr><td><b>Stop retrying failures</b> {tex("R_m(p)", 12)} — early stop, detect dead loops</td><td>yes</td><td>yes</td><td>stops some attempts that would have succeeded</td></tr>
  </tbody></table>
  <div class="gapcol">
    <div class="ck">NOT YET MEASURED</div>
    <ul>
      <li><b>Read / write time split and cache hit rate for a frontier API model</b> — the only split is on local 27–31B models {ci('yuan')}; screenshot-agent measurements do not report cache state.</li>
      <li><b>How much slower than a person</b> — no benchmark times agent and human on the same tasks; the closest, AXIS’s small user study, has a UI agent 1.69× slower than manual work on easy tasks {ci('axis')}.</li>
      <li><b>Whether the benchmark’s fixed sleep sits inside “action” time</b> in OSWorld-Human — if so, “environment under 3.5%” understates the waiting.</li>
      <li><b>How much slowness costs accuracy</b> — OSWorld 2.0 records the stale-screen failure mode without its share {ci('osw2')}.</li>
    </ul>
  </div>
</div>""",
      foot=f"SOURCES · levers derived from the formulas on pages 3–4 · gaps: {CITE['yuan']} · {CITE['axis']} · {CITE['osw2']} · Appendix A4 and A5",
      chip=("#a5-1", "Appendix A5"))

# --- references (part 1) ---------------------------------------------------
REFS_P1 = [
 "Abhyankar, R., Qi, Q., &amp; Zhang, Y. (2026). OSWorld-Human: Benchmarking the efficiency of computer-use agents. <i>Proceedings of the 9th Conference on Machine Learning and Systems (MLSys 2026)</i>. arXiv:2506.16042. University of California, San Diego.",
 "Anthropic. (2026a, May 13). <i>Best practices for computer and browser use with Claude</i>. https://claude.com/blog/best-practices-for-computer-and-browser-use-with-claude",
 "Anthropic. (2026b). <i>Claude API pricing</i>; <i>Prompt caching</i>; <i>Fast mode</i>; <i>Vision</i> (developer documentation, read 28 September 2026). https://platform.claude.com/docs/en/about-claude/pricing; https://platform.claude.com/docs/en/build-with-claude/prompt-caching; https://platform.claude.com/docs/en/build-with-claude/fast-mode; https://platform.claude.com/docs/en/build-with-claude/vision",
 "Artificial Analysis. (2026). <i>Methodology</i>; <i>Performance benchmarking methodology</i> (read 28 September 2026). https://artificialanalysis.ai/methodology; https://artificialanalysis.ai/methodology/performance-benchmarking — third-party measurement definitions.",
 "Bian, S., Yan, M., Jayarajan, A., Pekhimenko, G., &amp; Venkataraman, S. (2025). What limits agentic systems efficiency? arXiv:2510.16276. University of Wisconsin–Madison; University of Toronto; NVIDIA.",
 "Chang, C., Zhou, Y., Fu, K., An, D., Feng, T., Lu, H., Yao, S., Guo, P., Yu, Y., Shan, Y., Li, B., Yuan, B., &amp; Wang, W. (2026). From LLM inference to agentic workloads: Characterization and implications for serving systems (AgentSysBench). arXiv:2608.15127. Hong Kong University of Science and Technology; Alibaba Group; ByteDance.",
 "Chen, H. M., Guo, J., Luk, W., &amp; Fan, H. (2026). AOSpec: Action and observation co-speculation for low-latency agent serving. arXiv:2608.00881. Imperial College London.",
 "Chen, L., Zaharia, M., &amp; Zou, J. (2024). FrugalGPT: How to use large language models while reducing cost and improving performance. <i>Transactions on Machine Learning Research</i>. arXiv:2305.05176. Stanford University.",
 "DeepSeek. (2026). <i>Models &amp; pricing</i> (API documentation, read 28 September 2026); <i>DeepSeek-V4.1-Flash release</i> (10 September 2026). https://api-docs.deepseek.com/quick_start/pricing; https://api-docs.deepseek.com/news/news260910",
 "Erol, M. H., El, B., Suzgun, M., Yuksekgonul, M., &amp; Zou, J. (2026). Cost-of-Pass: An economic framework for evaluating language models. <i>The Fourteenth International Conference on Learning Representations (ICLR 2026)</i>. arXiv:2504.13359v2. Stanford University.",
 "Feng, G., Mao, H., Dutta, P., &amp; Gonzalez, J. E. (2026). Concurrency without model changes: Future-based asynchronous function calling for LLMs (AsyncFC). arXiv:2605.15077. University of California, Berkeley.",
 "Google. (2026). <i>Gemini Developer API pricing</i> (read 28 September 2026). https://ai.google.dev/gemini-api/docs/pricing",
 "Huang, Z., Wang, X., Wang, A., Jurayj, W., Jiménez Gutiérrez, B., Khashabi, D., &amp; Andrews, N. (2026). Better, faster, stronger: Programmatic skill learning best reduces agent cost (SpeedRunner). arXiv:2608.11338v1. Johns Hopkins University.",
 "Kang, H., Li, Z., Yang, X., Xu, W., Chen, Y., Wang, J., Chen, B., Krishna, T., Xu, C., &amp; Arora, S. (2026). ThunderAgent: A fast, simple, and program-aware agentic inference system. <i>Proceedings of the 43rd International Conference on Machine Learning (ICML 2026)</i>, poster. arXiv:2602.13692. Georgia Institute of Technology; University of Illinois Urbana-Champaign; Carnegie Mellon University; Together AI.",
 "Kapoor, S., Stroebl, B., Siegel, Z. S., Nadgir, N., &amp; Narayanan, A. (2025). AI agents that matter. <i>Transactions on Machine Learning Research</i>. arXiv:2407.01502. Princeton University.",
 "Kapoor, S., Stroebl, B., Kirgis, P., Nadgir, N., Siegel, Z. S., Wei, B., … Narayanan, A. (2026). Holistic Agent Leaderboard: The missing infrastructure for AI agent evaluation. <i>The Fourteenth International Conference on Learning Representations (ICLR 2026)</i>. arXiv:2510.11977. Princeton University et al.",
 "Kim, S., Moon, S., Tabrizi, R., Lee, N., Mahoney, M. W., Keutzer, K., &amp; Gholami, A. (2024). An LLM compiler for parallel function calling. <i>Proceedings of the 41st International Conference on Machine Learning (ICML 2024)</i>. arXiv:2312.04511. University of California, Berkeley.",
 "Le Sellier de Chezelles, T., Gasse, M., Lacoste, A., Caccia, M., Drouin, A., Boisvert, L., … Chapados, N. (2025). The BrowserGym ecosystem for web agent research. <i>Transactions on Machine Learning Research</i>. arXiv:2412.05467. ServiceNow Research et al. (figure not re-verified; used only in Appendix A1)",
 "Lee, N., Erdogan, L. E., John, C. J., Krishnapillai, S., Mahoney, M. W., Keutzer, K., &amp; Gholami, A. (2026). Agentic test-time scaling for WebAgents. arXiv:2602.12276. University of California, Berkeley.",
 "Li, Y., Ye, Q., Choubey, P. K., Zhang, J., &amp; Wu, C.-S. (2026). Speculate with memory. arXiv:2607.12236. Salesforce Research.",
 "Liu, B., Qiu, H., Goiri, Í., Fonseca, R., Bianchini, R., &amp; Choukse, E. (2026). Agentic coding in the wild: Characterizing GitHub Copilot traces at production scale. arXiv:2608.00101. University of Illinois Urbana-Champaign; Microsoft Azure Research.",
 "Lu, J., Zhang, Z., Yang, F., Zhang, J., Wang, L., Du, C., Lin, Q., Rajmohan, S., Zhang, D., &amp; Zhang, Q. (2025). AXIS: Efficient human-agent-computer interaction with API-first LLM-based agents. <i>Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)</i>, 7711–7743. https://doi.org/10.18653/v1/2025.acl-long.381. Microsoft.",
 "Luo, M., Shi, X., Cai, C., Zhang, T., Wong, J., Wang, Y., Wang, C., Huang, Y., Chen, Z., Gonzalez, J. E., &amp; Stoica, I. (2026). Agentix: An efficient serving engine for LLM agents as general programs. <i>23rd USENIX Symposium on Networked Systems Design and Implementation (NSDI 26)</i>. University of California, Berkeley; Google DeepMind; Shanghai Jiao Tong University.",
 "OpenAI. (2026). <i>API pricing</i>; <i>API changelog</i> (fast mode, 30 July 2026; Ultrafast, 13 August 2026) (read 28 September 2026). https://developers.openai.com/api/docs/pricing; https://developers.openai.com/api/docs/changelog",
 "Vendor price pages used on pages 11–12 and in Appendix A3 (all read 27 September 2026): AWS, <i>Amazon EC2 T3 instances</i>; Browser Use, <i>Pricing</i> and <i>API v4: create browser session</i>; Browserbase, <i>Pricing</i> and <i>Billing plans</i>; Daytona, <i>Pricing</i> and <i>Billing</i>; E2B, <i>Pricing</i>; Modal, <i>Pricing</i> and <i>Sandbox resources</i>.",
 "Winston, C., Wang, R. Y., Mirhoseini, A., &amp; Kozyrakis, C. (2026). Agent JIT compilation for latency-optimizing web agent planning and scheduling. <i>Proceedings of the 43rd International Conference on Machine Learning (ICML 2026)</i>, PMLR 306. arXiv:2605.21470. Stanford University.",
 "Wong, M., Hsieh, K., Nath, S., &amp; Netravali, R. (2026). Skim: Speculative execution for fast and efficient web agents. arXiv:2605.16565. Princeton University; Microsoft Research.",
 "xAI. (2026). <i>Grok 4.7</i> model page, SpaceXAI Docs (read 28 September 2026). https://docs.x.ai/developers/models/grok-4.7",
 "XLANG Lab. (2026). OSWorld 2.0: Benchmarking computer use agents on long-horizon real-world tasks. arXiv:2606.29537. The University of Hong Kong (authored as “XLANG Lab and Collaborators”; the full author list is in the paper’s Appendix A).",
 "xlang-ai. (2026). <i>OSWorld</i> [Source code], desktop_env/desktop_env.py and run.py at commit b138d348. https://github.com/xlang-ai/OSWorld",
 "Xu, B., Xue, Z., Chen, D., Fu, C., Wu, C., Huang, C., … Zhang, N. (2026). TokenPilot: Cache-efficient context management for LLM agents. arXiv:2606.17016. Zhejiang University; University of Electronic Science and Technology of China; Xidian University; HomologyAI.",
 "Ye, N., Ahuja, A., Liargkovas, G., Lu, Y., Kaffes, K., &amp; Peng, T. (2026). Speculative actions: A lossless framework for faster AI agents. <i>The Fourteenth International Conference on Learning Representations (ICLR 2026)</i>, oral. arXiv:2510.04371. Columbia University.",
 "Yuan, Y., Nayak, A., Kundu, S., &amp; Talati, N. (2026). Agentic AI workload characteristics. arXiv:2605.26297v2 (21 September 2026). University of Illinois Urbana-Champaign; Gimlet Labs; Intel.",
 "Zhang, C., Huang, H., Ni, C., Mu, J., Qin, S., He, S., … Zhang, D. (2026). UFO2: The desktop AgentOS. <i>Transactions on Machine Learning Research</i>. arXiv:2504.14603. Microsoft.",
 "Zhu, K., Jacob, M., Ma, C., Pan, Y., Wang, S., Krishnamurthy, A., &amp; Kasikci, B. (2026). TraceLab: Characterizing coding agent workloads for LLM serving. arXiv:2606.30560. University of Washington.",
]

def refs_html(items, start=1):
    return f'<ol class="reflist" start="{start}">' + "".join(f"<li>{r}</li>" for r in items) + "</ol>"

half = (len(REFS_P1) + 1) // 2
slide("s15", "References · Part 1 (1 of 2)", kind="refs",
      crumb="author–year tags on the pages refer to these entries · published version where one exists, otherwise the arXiv number and the authors’ institutions",
      body=refs_html(REFS_P1[:half]))
slide("s16", "References · Part 1 (2 of 2)", kind="refs",
      crumb="continued",
      body=refs_html(REFS_P1[half:], start=half+1))

# =====================================================================
# APPENDIX — Part 1
# =====================================================================
def A(id_, label, title, body, hl=(), crumb="", notes="", chip=("#back", "← back"), part=1):
    slide(id_, title, body, label=label, hl=hl, crumb=crumb, notes=notes, chip=chip, kind="appendix", part=part)

th_slow = ["id", "cause", "mechanism", "evidence, with the conditions of the measurement", "source", "dominant in"]
w_slow = ["4%", "11%", "15%", "47%", "13%", "10%"]

A("a0-1", "A0 · 1/5", "A0 · The time of one attempt: each source’s own formula, and why ours differs",
  crumb="the derivation behind page 3 · verbatim / adapted / our distillation · calc. = our algebra",
  body=table(["formula (pages 2–3)", "status", "the source’s own formula or words, in its notation", "what changed, and why"], [
   [tex(r"T_{\mathrm{attempt}}\triangleq t_{\mathrm{end}}-t_{\mathrm{start}}=\mathcal{D}(\mathcal{M}\cup\mathcal{E})=\sum_{i=0}^{N}(D_i+E_i)-T_{\mathrm{saving}}", 11), "adapted", tex(r"T_{\mathrm{saving}}", 11) + " is “defined as the difference between the serialized baseline and the observed end-to-end asynchronous latency” (App. B.2) " + ci('asyncfc') + ", combined with the sum below", "one attempt, not one task (a task may take several); exact because the non-model intervals cover every instant; " + tex(r"T_{\mathrm{saving}}\geq 0", 11) + " (calc.); exact with measured call times, approximate once " + tex(r"\ell\approx\mathrm{TTFT}+n\,\mathrm{TPOT}", 11)],
   [tex(r"\sum_{i=0}^{N}(D_i+E_i)", 11), "adapted", "“At step i, the actor takes " + tex("D_i", 11) + " time to generate action " + tex("a_i", 11) + ", and the runtime takes " + tex("T_i", 11) + " time to execute it … yielding serial latency " + tex(r"\sum_i(D_i+T_i)", 11) + "” (§3) " + ci('aospec'), tex("T_i", 11) + " → " + tex("E_i", 11) + " (T is kept for totals); " + tex("D_i", 11) + " covers all calls of a step, " + tex("E_i", 11) + " every non-model interval, both as summed lengths; " + tex("i=0", 11) + " holds calls outside any step; AOSpec’s " + tex("a_i", 11) + " is an action, not our agent index; preferred to " + ci('llmc') + ", whose N counts the function calls of one plan"],
   [tex(r"D_i=\sum_j \ell_{ij}", 11), "our distillation", "No source sums the calls of a step. GTA1 makes “4 parallel calls” per planning step and “between 4 and 12 planning calls” per judging call " + ci('osh'), "parallel calls add here; their overlap is credited to " + tex(r"T_{\mathrm{saving}}", 11) + "; the letter ℓ as in " + ci('swm')],
   [tex(r"\ell_{ij}\approx\mathrm{TTFT}_{ij}+n^{\mathrm{out}}_{ij}\mathrm{TPOT}_{ij}", 11), "adapted", "Total Response Time = Time to First Token + 100 / Output Speed " + ci('aa'), "100 → the call’s own output tokens, thinking included; 1/speed → TPOT; ≈ because output speed excludes the first chunk; TTFT runs to the first token of any kind, reasoning included"],
   [tex(r"\mathrm{TTFT}_{ij}\approx t^{\mathrm{queue}}+t^{\mathrm{net}}+t^{\mathrm{prefill}}(n^{\mathrm{unc}}+n^{\mathrm{w}};\,n^{\mathrm{hit}})+t^{\mathrm{first}}", 11), "our distillation", "No source writes TTFT as a sum. A program’s latency “comprises three components”, the first the “queuing time” of its calls " + ci('agentix') + "; TTFT “includes network latency” " + ci('aa'), "the split used on page 13; " + tex(r"t^{\mathrm{net}}", 11) + ": network time, " + tex(r"t^{\mathrm{first}}", 11) + ": first decode step; the shape of " + tex(r"t^{\mathrm{prefill}}", 11) + " is not given by any verified source"],
  ], ["26%", "9%", "34%", "31%"]))

A("a0-2", "A0 · 2/5", "A0 · Time hidden by concurrency, and the growing prompt",
  crumb="the derivation behind page 3 · verbatim / adapted / our distillation · calc. = our algebra",
  body=table(["formula (page 3)", "status", "the source’s own formula or words, in its notation", "what changed, and why"], [
   [tex(r"T_{\mathrm{saving}}\triangleq\mathcal{S}(\mathcal{M})+\mathcal{S}(\mathcal{E})-\mathcal{D}(\mathcal{M}\cup\mathcal{E})", 11), "adapted", "the same formula, continued " + tex(r"=\Delta_{F\parallel F}+\Delta_{D\parallel E}", 11) + ", with " + tex(r"\mathcal{M},\ \mathcal{E}", 11) + " “the sequence of time intervals for model decoding and function execution” (App. B.2) " + ci('asyncfc'), "intervals widened to whole calls and all non-model time, so values are not comparable with AsyncFC’s; the split becomes (calc.) " + tex(r"[\mathcal{S}(\mathcal{M})-\mathcal{D}(\mathcal{M})]+[\mathcal{S}(\mathcal{E})-\mathcal{D}(\mathcal{E})]+[\mathcal{D}(\mathcal{M})+\mathcal{D}(\mathcal{E})-\mathcal{D}(\mathcal{M}\cup\mathcal{E})]", 11) + ", each ≥ 0; it can include extra work that concurrency causes, so it is not the saving against a separate serial run (speed-ups use " + tex(r"T_{\mathrm{seq}}/T_{\mathrm{attempt}}", 11) + ", Part 2)"],
   [tex(r"|H_{a,i+1}|=|H_{a,i}|+|\Phi(z_{a,i})|+|o_{a,i}|", 11), "adapted", tex(r"H_{a,i+1}=H_{a,i}\,\Vert\,\Phi(\theta_{a,i},m_{a,i},u_{a,i})\,\Vert\,o_{a,i}", 11) + ", " + tex(r"C_{a,i}=|H_{a,i}|", 11) + " (Eqs. 1–3, v2 §II-C) " + ci('yuan'), "lengths of the concatenation; " + tex(r"z=(\theta,m,u)", 11) + " (thinking, message, tool-call tokens) substituted, because Yuan’s m would clash with the design m and its " + tex(r"C_{a,i}", 11) + " with the cost " + tex("C_m(p)", 11) + "; exact with one call per step and full history; in general add " + tex(r"h^{+}_i-h^{-}_i", 11) + " (other calls’ output; compaction)"],
   [tex(r"\sum_{i=1}^{N}|H_{a,i}|=N|H_{a,1}|+\frac{N(N-1)}{2}\bar{g}", 11), "our distillation (calc.)", "no source writes the sum; “at each step, the prompt sent to the LLM includes the history of all previous steps” " + ci('osh'), tex(r"g_i=|\Phi(z_{a,i})|+|o_{a,i}|", 11) + ", " + tex(r"\bar{g}=\sum_i(N-i)g_i\,/\,\frac{N(N-1)}{2}", 11) + " makes it exact; over a random step count " + tex(r"\mathbb{E}[\sum|H|]\approx\mathbb{E}[N]|H_{a,1}|+\frac{\bar{g}}{2}(\mathbb{E}[N]^2+\mathrm{Var}[N]-\mathbb{E}[N])", 11) + "; crossover " + tex(r"N^{*}=2|H_{a,1}|/\bar{g}+1", 11)],
  ], ["22%", "9%", "33%", "36%"]))

A("a0-3", "A0 · 3/5", "A0 · Money, per success, and the goal",
  crumb="the derivation behind page 4 · verbatim / adapted / our distillation · calc. = our algebra",
  body=table(["formula (page 4)", "status", "the source’s own formula or words, in its notation", "what changed, and why"], [
   [tex(r"c_m(p)=\sum_{i,j}\sum_{\kappa}n^{\kappa}_{ij}c_{\kappa}(\mu_{ij})+x_{\mathrm{env}}c_{\mathrm{env}}", 11), "adapted", tex(r"c_m(p)=n_{\mathrm{in}}(m,p)\,c_{\mathrm{in}}(m)+n_{\mathrm{out}}(m,p)\,c_{\mathrm{out}}(m)", 11) + " (Eq. 13): input and output tokens times their prices; other components go into " + tex(r"C_m(p)=w^{\top}x_m(p)", 11) + ", w the unit prices and " + tex("x_m(p)", 11) + " the quantities per attempt (App. D.1) " + ci('cop'), "input split into the billed classes (cache hit, 5-min and 1-h cache write, uncached); prices inside the sum because one step can mix models; environment usage added as App. D.1 allows; the class index is κ because x is Cost-of-Pass’s quantity. Closest written three-class form: " + ci('tokenpilot')],
   [tex(r"v(m,p)=C_m(p)/R_m(p)", 11), "verbatim", "“the expected number of attempts to obtain the first correct solution is " + tex("1/R_m(p)", 11) + "”, assuming independent trials (§2.2, Eq. 2) " + ci('cop'), "none; assumes unlimited independent retries and the verifier’s time and cost in every attempt; with at most K retries the ratio is still C/R (calc.); with cache-warm retries " + tex(r"C^{(1)}_m(p)+(1/R_m(p)-1)\,C^{(2+)}_m(p)", 11) + " (calc.)"],
   [tex(r"\mathbb{E}[T_{\mathrm{attempt}}]/R_m(p)", 11), "adapted", "“alternative units per attempt (FLOPs, time, latency, energy) may matter more than dollar cost” (App. D.1) " + ci('cop'), "the same derivation in seconds; serial retries only (parallel votes cost “roughly the latency of a single vote”); correlated failures break independence"],
   [tex(r"\mathrm{Pareto}_m(\cdot,\cdot)\ \mathrm{s.t.}\ R_m(p)\geq R_0", 11), "our distillation", tex(r"V_p(\mathcal{M})=\min_{m\in\mathcal{M}}v(m,p)", 11) + " (Eq. 3), with a human expert as fallback, " + tex(r"\min(V_p(\mathcal{M}),\,v(\mathrm{expert},p))", 11) + " (Eqs. 4–5) " + ci('cop') + "; “the new goal of jointly optimizing the two metrics” (arXiv v1) " + ci('kapoor25') + "; budgeted dual: maximise quality with expected cost within a budget " + ci('frugal'), "min → Pareto set, because seconds and dollars are not one scalar; the human is the reference point; the floor " + tex("R_0", 11) + " follows App. C.8’s remedy of leaving unreliable systems off the frontier; over a task mix " + tex(r"\sum_p C_m(p)/\sum_p R_m(p)", 11) + ", unlike Eq. 8’s mean of " + tex("V_p", 11)],
  ], ["22%", "9%", "37%", "32%"]))

A("a0-4", "A0 · 4/5", "A0 · Every symbol, its unit, and where it comes from",
  crumb="origin of each symbol: “as in” a source (its own symbol and meaning), “adapted from” a source (renamed or widened), or self-defined",
  body=table(["symbol", "meaning", "unit", "origin"], [
   [tex(r"i,\ N,\ j,\ J_i,\ a", 11), "step (i = 0: calls outside any step); steps; model call; calls in step i; agent", "—; steps; —; calls; —", "i as in " + CITE['aospec'] + " §3 and " + CITE['yuan'] + " §II-C · a as in Yuan et al., §II-C · N, j, J_i self-defined (calls ≠ steps)"],
   [tex(r"D_i,\ E_i,\ T_{\mathrm{attempt}},\ T_{\mathrm{saving}},\ T_{\mathrm{seq}}", 11), "model time; non-model time of step i; wall-clock of one attempt; time hidden by concurrency; a separate serial run", "s", "D adapted from " + CITE['aospec'] + " §3 (all calls of a step) · E self-defined (replaces their T_i) · T_attempt self-defined · T_saving adapted from " + CITE['asyncfc'] + " App. B.2 (intervals widened) · T_seq as in " + CITE['specactions'] + " §3.1.2"],
   [tex(r"\mathcal{S},\ \mathcal{D},\ \mathcal{M},\ \mathcal{E},\ \triangleq", 11), "summed length; length of a union; model-call and non-model intervals; defined as", "s", "adapted from " + CITE['asyncfc'] + " App. B.2 (intervals widened)"],
   [tex(r"\ell_{ij},\ \mathrm{TTFT}_{ij},\ \mathrm{TPOT}_{ij}", 11), "call latency; time to first token; time per output token", "s; s; s/token", "ℓ as in " + CITE['swm'] + " §2.1 (ℓ_LLM) · TTFT as in " + CITE['aa'] + ", definitions · TPOT as in " + CITE['aospec'] + " §5.1 · indices self-defined"],
   [tex(r"t^{\mathrm{queue}},\ t^{\mathrm{net}},\ t^{\mathrm{prefill}},\ t^{\mathrm{first}}", 11), "parts of TTFT: queueing, network, prefill of uncached input, first decode step", "s", "self-defined (A0 · 1/5)"],
   [tex(r"n^{\mathrm{in}},\ n^{\mathrm{hit}},\ n^{\mathrm{w}},\ n^{\mathrm{w5m}},\ n^{\mathrm{w1h}},\ n^{\mathrm{unc}},\ n^{\mathrm{out}}", 11), "tokens: all input (= hit + w + unc); cache read; cache write (= w5m + w1h); uncached input; output", "tokens", "n as in " + CITE['cop'] + " (n_in, n_out) · classes as billed by " + CITE['anth-b'] + " (usage fields) · hit as in " + CITE['tokenpilot'] + " App. A.2 · unc as in " + CITE['speedrunner'] + " App. A.3 · w5m, w1h self-defined"],
   [tex(r"\kappa,\ K,\ \mu_{ij},\ c_{\kappa}(\mu)", 11), "billing class; the set {hit, w5m, w1h, unc, out}; serving model; price per token of class κ on μ", "—; —; —; $/token", "c adapted from " + CITE['cop'] + " Eq. 13 (c_in, c_out) · κ, K, μ self-defined"],
   [tex(r"x_{\mathrm{env}},\ c_{\mathrm{env}},\ w,\ x_m(p)", 11), "billed environment usage; its price; price vector; quantity vector per attempt", "h; $/h; $/unit; units", "as in " + CITE['cop'] + " App. D.1 · env subscript self-defined"],
   [tex(r"H_{a,i},\ \Phi,\ z_{a,i},\ o_{a,i},\ g_i,\ \bar{g},\ N^{*}", 11), "context before step i of agent a; chat template; the step’s output; its tool result; tokens added; weighted mean; crossover", "tokens; —; tokens; tokens; tokens; tokens; steps", "H, Φ, o as in " + CITE['yuan'] + " Eqs. 1–3 · z self-defined for their (θ, m, u) = (thinking, message, tool call) · g, ḡ, N* self-defined (calc.)"],
   [tex(r"m,\ p,\ c_m(p),\ C_m(p),\ R_m(p),\ v(m,p),\ R_0,\ \mathbb{E},\ \mathrm{Var}", 11), "design (model + harness); task; dollars of one attempt; expected; success probability; dollars per success; success floor; expectation; variance", "—; —; $; $; prob.; $; prob.", "as in " + CITE['cop'] + " §2.2, Eq. 2, App. B · R_0 self-defined · 𝔼, Var standard"],
  ], ["24%", "34%", "11%", "31%"]))

A("a0-5", "A0 · 5/5", "A0 · What a published number covers: map it onto the terms before comparing",
  crumb="the measurement boundary · a figure is comparable only with what it includes stated",
  body=table(["kind of figure", "what it includes", "what it leaves out"], [
   ["first-token time, output speed " + ci('aa'), "one synthetic call: queueing, network and prefill lumped in TTFT; speed after the first chunk", "the step, the tools, the environment"],
   ["request response time " + ci('tracelab'), "model generation plus tool execution", "the person thinking between turns"],
   ["stopwatch time per task " + ci('osh'), "the whole attempt, " + tex(r"T_{\mathrm{attempt}}", 11), "— (39 tasks, one run each)"],
   ["time saved " + ci('asyncfc'), "decode and function-execution intervals of the concurrent trace", "queueing, prefill, harness gaps"],
   ["cost with two classes (input, output) " + ci('cop'), "all input at the base price", "cache reads (overstates cost) and cache writes (understates it)"],
   ["cost with three classes (hit, miss, output) " + ci('tokenpilot'), "cache reads at their price", "cache writes; environment usage"],
   ["cache hit rate", "denominators differ: cached / cacheable input " + ci('aa') + ", / all input " + ci('tokenpilot') + ", per incoming call " + ci('agentix'), "ours: " + tex(r"n^{\mathrm{hit}}/n^{\mathrm{in}}", 11)],
   ["almost every published figure", "per attempt", "per success: divide by " + tex("R_m(p)", 11) + "; lossless speed papers report no task success"],
  ], ["26%", "44%", "30%"]))

A("a1-1", "A1 · 1/3", "A1 · Slowness, every cause — I. steps and II. calls per step",
  hl=("n-steps", "n-calls"),
  crumb="the complete table behind pages 5–6 · three kinds of agent: screenshot desktop agent, text web agent, coding agent with a prompt cache",
  body=table(th_slow, [
   ["I-1", "The task is long", "Hour-scale tasks take hundreds of steps", "OSWorld 2.0, 108 long tasks: Claude Opus 4.7 with maximum thinking, one action per step, 500-step cap: 318 tool calls per task on average, i.e. 318 steps; with several actions per call, Claude Opus 4.8 takes 103 steps (481.8 calls) and GPT-5.5 95.2 steps (149.8 calls)", ci('osw2'), "screenshot, text"],
   ["I-2", "One action per step", "Every click is a whole step: one observation, one model call, one wait", "OSWorld 2.0: with one action per step Claude Opus 4.7 needs 318 steps; with batched actions the same model needs 160.7 and Claude Opus 4.8 needs 103", ci('osw2'), "screenshot, text"],
   ["I-3", "Navigation-only steps still call the model", "Paging, scrolling and opening the next page need no thinking but cost a call each", "Skim’s profile of three text web agents (Browser-Use, AgentOccam, WebVoyager; GPT-4o) on 151 WebVoyager live-site tasks: 66.7% of the steps in the median task are pure navigation", ci('skim'), "text"],
   ["I-4", "Idling and dead loops", "Element not found, repeated retries; steps rise without progress", "OSWorld-Human’s records of the GTA1 harness (o3 plans and judges, GTA1-7B locates elements) on 39 OSWorld desktop tasks: in failed tasks that exceeded 50 steps, 66% of steps were wasted repeats; one element-locating loop repeated the same step 18 times — 27 minutes and $8.47 at list price without caching", ci('osh'), "screenshot"],
   ["I-5", "Acting on a stale screen", "The screenshot is taken before the page changes; the agent clicks on the old layout and must repair", "OSWorld 2.0 records “stale interface state” as a failure mode; no share reported", ci('osw2'), "screenshot"],
   ["II-1", "Multi-call harness", "One step = plan + judge + reflect, several calls in series", "OSWorld-Human, two harnesses: GTA1 runs 4 parallel planners per step, retries up to 3 rounds, then one judging call picks — 4–12 planning calls per judging call; Agent S2 adds a reflection call per step, so planning is 53% and reflection 34% of task time", ci('osh'), "screenshot"],
   ["II-2", "Sampling for accuracy", "5–20 candidates per step, then pick one", "Same model and harness (gpt-oss-120b, ReAct) on 165 WebArena-Lite tasks: 1 → 10 candidates per step raises success from 38.8% to 43.2% and tokens per task from 96K to 920K — 9.6× the tokens for 4.4 points", ci('atts'), "text"],
   ["II-3", "Coding agents call repeatedly within a turn", "The model is called back and forth inside one user turn", "GitHub Copilot coding agent production telemetry (first week of June 2026, 13.5 million sessions): 6.6 model calls per user turn on average", ci('copilot'), "coding"],
  ], w_slow))

A("a1-2", "A1 · 2/3", "A1 · Slowness, every cause — III. each call is slow",
  hl=("n-queue", "n-read", "n-write"),
  crumb="the complete table behind pages 7–8",
  body=table(th_slow, [
   ["III-1", "Queueing", "The request waits at the provider; unbilled, but counted as model time", "Client-side measurement of 15 models across 5 providers: requests of the same length differ in latency by up to 69× depending on when they are sent", ci('bian'), "all"],
   ["III-2", "Reading (the prompt is re-processed every call)", "Every call re-reads the whole history; more screenshots, slower", "OSWorld-Human, multi-call harnesses: later steps up to 3× slower because the prompt at step " + tex("i", 12) + " holds the " + tex("i-1", 12) + " earlier screenshots — “dominated by prefill”. One screenshot is 1,000–1,800 tokens. AgentSysBench’s WebArena agent (Kimi-K2.6): observation switched from a single format to accessibility tree + HTML + screenshot → input 4.8×, model share of time 46.9% → 61.6%. Under load the cache is evicted and re-read: SWE-Agent / OpenHands running GLM-4.6 on 8 H100s for SWE-bench Lite, request latency up to 7.14× as concurrency rises", ci('osh','anth-a','asb','thunder'), "screenshot; text with rich observations; coding under load"],
   ["III-3", "Writing (one token at a time)", "Token-by-token generation, strictly serial", "Locally served ReAct agents (Qwen3.6-27B / Gemma4-31B, vLLM, 2 H100s) on five benchmarks: with the cache warm, generation is 91–98.6% of model time. Windows desktop agent UFO2 (GPT-4o / o1 API): about 10 s per model call, the largest item per step in every configuration", ci('yuan','ufo2'), "coding; single-call screenshot"],
   ["III-4", "Thinking modes and larger models", "Thinking writes more tokens; larger models are slower per token", "OSWorld 2.0, same 108 tasks: Claude Opus 4.8 writes 224K output tokens per task, GPT-5.5 37K. Holistic Agent Leaderboard, 9 benchmarks, 21,730 runs: raising reasoning effort lowered accuracy in 21 of 36 pairs", ci('osw2','hal'), "all"],
  ], w_slow))

A("a1-3", "A1 · 3/3", "A1 · Slowness, every cause — IV. environment, V. serial",
  hl=("n-observe", "n-act", "n-wait", "n-overlap"),
  crumb="the complete table behind page 9 (non-model time and concurrency)",
  body=table(th_slow, [
   ["IV-1", "Producing the observation", "Extracting the accessibility tree or detecting elements takes time", "OSWorld desktop applications: 3–26 s to generate one accessibility tree; the screenshot itself is under 2% of task time. UFO2: OmniParser element detection adds about 1 s per step", ci('osh','ufo2'), "screenshot"],
   ["IV-2", "Browser execution and page load", "After a click the agent waits for the page", "151 WebVoyager live-site tasks: per step, median browser action 6.6 s vs model call 4.7 s. WebArena with GenericAgent + Claude 3.5 Sonnet: 7.6 s of a 12.2 s step in the browser (this figure was not re-verified)", ci('skim','bgym'), "text"],
   ["IV-3", "Fixed sleeps", "The agent cannot tell when the page is ready, so it sleeps a fixed number of seconds", "OSWorld’s environment code sleeps 2 s after every action; OSWorld 2.0 prescribes 3 s, so 318 steps are about 16 minutes of pure waiting (calc.). AgentSysBench: a single-call GUI agent (ReAct, Kimi-K2.6 API) spends over 70% of its OSWorld execution time in the desktop sandbox", ci('code','osw2','asb'), "screenshot (caused by the benchmark harness)"],
   ["IV-4", "Tool tails", "Tests and builds take minutes", "TraceLab, 4,265 Claude Code / Codex sessions from 43 developers (September 2025 – June 2026): tool calls over 1 minute are 4% of calls but 85% of tool time; a request averages 4.3 minutes — tools 2.5 (59.8%), model 1.7 (41.0%)", ci('tracelab'), "coding"],
   ["V", "Serial structure", "The four stages never overlap, so task time is the sum of every term, not the largest one; fixing one term saves only its share", "Concurrency within a turn is 1.15 in Copilot telemetry. Separately, 80–92% of a coding session’s elapsed time is the human thinking between turns — strip it before reading any total", ci('copilot','tracelab'), "all"],
  ], w_slow))

A("a2-1", "A2", "A2 · Where the arrows land, with every measurement condition",
  hl=("n-read", "n-wait", "n-write"),
  crumb="the complete table behind page 10",
  body=table(["", "screenshot desktop agent, multi-call harness", "text web agent", "coding agent with a prompt cache"], [
   ["heaviest term", f"Reading × calls per step × steps. OSWorld-Human timed two multi-call harnesses (GTA1, Agent S2) step by step on 39 OSWorld desktop tasks: 87–97% of task time in planning, judging and reflection calls; screenshots and actions together under 3.5% {ci('osh')}", f"Browser execution plus waiting. Skim measured three text web agents (GPT-4o) on 151 WebVoyager live-site tasks: per step, median browser action 6.6 s and model call 4.7 s {ci('skim')}", f"Writing, or tool tails, depending on the tools. With the context cache on, token-by-token generation is 91–98.6% of model time (locally served models) {ci('yuan')}; in Claude Code / Codex records a request spends 59.8% in tools and 41.0% in the model {ci('tracelab')}; in GitHub Copilot, whose tools are light, agent time is 13.7% model and 2% tools {ci('copilot')}"],
   ["second", "Writing: with thinking on, more reasoning tokens per step, and generation is one token at a time", f"Reading, once the observation grows: AgentSysBench switched a WebArena agent from one observation format to accessibility tree + HTML + screenshot — input 4.8×, model share 46.9% → 61.6% {ci('asb')}; the Browser-Use harness spends 73% of its latency in model calls {ci('jit')}", f"Reading, when load evicts the cache and the whole context is re-read: ThunderAgent measured request latency up to 7.14× under cache thrash {ci('thunder')}"],
   ["negligible", f"Producing the observation and executing the action: under 3.5% together {ci('osh')}", "Nothing: model and browser are close; which is larger depends on observation size and model speed", "Navigation-only steps: a coding agent has no pages to turn"],
   ["counter-example", f"A single-call agent is different: AgentSysBench’s one-call GUI agent (Kimi-K2.6) spends over 70% of its OSWorld time in the desktop sandbox {ci('asb')}, because the harness sleeps after every action — 2 s in OSWorld’s code {ci('code')}, 3 s in OSWorld 2.0 {ci('osw2')}", f"Browser-Use: 73% of latency in model calls, not the browser {ci('jit')}", f"Two production records point opposite ways: heavy tools in Claude Code / Codex (tools 59.8% > model 41.0%) {ci('tracelab')}; light tools in Copilot (model 13.7% > tools 2%) {ci('copilot')}. The difference is the kind of tool (tests and builds vs file reads), not a contradiction"],
   ["in one line", "Slow in reading: every step re-reads the screenshot history, more as the task goes on", "Slow in the environment (browser and page waits); once the observation grows, slow in reading again", "Reading is cached away; slow in writing and in the tools"],
  ], ["9%", "31%", "30%", "30%"], cls="tbl three"))

th_cost = ["id", "cause", "mechanism", "evidence, with the conditions of the measurement", "source"]
w_cost = ["5%", "13%", "20%", "47%", "15%"]
A("a3-1", "A3 · 1/3", "A3 · Cost, every cause — 1. tokens read and 2. tokens written",
  hl=("n-rtok", "n-wtok"),
  crumb="the complete table behind pages 8 and 11 · prices are list prices from the vendors’ own pages, September 2026",
  body=table(th_cost, [
   ["1-1", "History re-sent", "Step " + tex("i", 12) + " reads everything from the " + tex("i-1", 12) + " earlier steps; total reading " + tex(r"\approx N^2", 12), "“Cost grows quadratically with the number of steps” — OSWorld-Human, real runs", ci('osh')],
   ["1-2", "Large screenshots", "1,000–1,800 tokens per image; 100 images fill a 200K context", "Anthropic’s engineering guidance for computer and browser use", ci('anth-a')],
   ["1-3", "Rich observation formats", "Accessibility tree + HTML + screenshot together: 4.8× the input", "AgentSysBench, WebArena agent, Kimi-K2.6", ci('asb')],
   ["1-4", "Sampling", "Several candidates per step, mostly read tokens", "gpt-oss-120b + ReAct on 165 WebArena-Lite tasks: 1 → 10 candidates per step, 96K → 920K tokens per task", ci('atts')],
   ["1-5", "The cache is not a cure", "However high the hit rate, a long history keeps reading dominant; a miss re-reads everything", "TraceLab, 4,265 Claude Code / Codex sessions: prefix-cache hit rate 95.7%, prefix tokens still 59.5% of list-price cost; on a miss the re-read is 3.8× the genuinely new content", ci('tracelab')],
   ["2-1", "Thinking modes", "Thinking tokens are billed as output; when they cannot be switched off they are a fixed overhead", "OSWorld 2.0, same tasks: Claude Opus 4.8 224K output tokens per task, GPT-5.5 37K; Claude Opus 5.5: “thinking cannot be disabled and is billed as output”", ci('osw2','anth-b')],
   ["2-2", "But writing is not always the larger bill", "In an uncached screenshot agent, output was 31% of the total", "OSWorld-Human, GTA1: the paper’s $2.43 counts output only; Table 3’s input and output give $7.87", ci('osh')],
  ], w_cost))

A("a3-2", "A3 · 2/3", "A3 · Cost, every cause — 3. calls, 4. failures, 5. unit price",
  hl=("n-calls", "n-succ", "n-price"),
  crumb="the complete table behind page 11 (calls, failures, unit price)",
  body=table(th_cost, [
   ["3", "Number of calls", tex(r"N \cdot J_i", 12) + " scales both token bills", "GTA1: 4 parallel planners per step, up to 3 retry rounds, one judging call → 4–12 planning calls per judging call, i.e. 5–13× the calls of a single-call harness (calc.). Agentic test-time scaling: 5–20 candidates per step multiply the calls by the candidate count. The same extra calls cost time and money at once", ci('osh','atts')],
   ["4-1", "Failed attempts are billed", "Cost per success = cost per attempt ÷ success rate", "OSWorld 2.0: the best agent (Claude Opus 4.8) costs about $72.4 per attempt at 20.6% completion → about $351 per success (calc.). An accounting conversion, not the real price of retrying one task until it succeeds", ci('osw2')],
   ["4-2", "Idle steps are billed in full", "Every step of a dead loop is a full read and write", "OSWorld-Human, GTA1 on 39 OSWorld tasks: one element-locating loop repeated the same step 18 times — 27 minutes, $8.47 at list price without caching; in failed tasks over 50 steps, 66% of steps were such repeats", ci('osh')],
   ["4-3", "Evaluation itself is too expensive to repeat", "Single runs, no repeats", "Holistic Agent Leaderboard: 9 benchmarks, 21,730 runs, one run per configuration, about $40,000 in total; Claude Opus 4.1 not run on Online-Mind2Web because the estimate was $20,000", ci('hal')],
   ["5-1", "Model tier", "Claude Opus 5.5 $4 / $20 vs GPT-6 Luna $0.10 / $0.50 per million tokens read / written", "Vendor price pages, 27 September 2026", ci('anth-b','openai')],
   ["5-2", "Fast mode", "2× on both vendors; switching speed tiers invalidates the cache", "Anthropic: Claude Opus 5.5 $8 / $40, up to 2.5× output speed (vendor-stated), first-token wait unchanged. OpenAI: 2× on all listed models; “up to 2.5×” stated only for GPT-5.6 Sol", ci('anth-b','openai')],
   ["5-3", "Cache write and read", "Latest model of each vendor, per million tokens, normal read → cached read (ratios calc.):"
          "<br>DeepSeek-V4.1-Flash $0.30 → $0.006 (0.02×; peak rate, both halve off-peak)"
          "<br>Claude Opus 5.5 $4 → $0.20 (0.05×; other Claude models 0.1×, Fable 5.1 0.025×; cache writes 1.25× for 5 min, 2× for 1 hour)"
          "<br>GPT-6 Sol $2 → $0.20 and GPT-6 Luna $0.10 → $0.01 (0.1×; cache writes 1.25×)"
          "<br>Gemini 3.8 Flash $0.75 → $0.075 (0.1×; plus $0.50 per million tokens per hour of storage; introductory to 31 Dec 2026)"
          "<br>Grok 4.7 $2 → $0.50 (0.25×)",
    "Vendor price pages, read 28 September 2026", ci('deepseek','anth-b','openai','google','xai')],
   ["5-4", "Long-context surcharge", "OpenAI: 2× the read price above 272K tokens", "Vendor price page", ci('openai')],
  ], w_cost))

A("a3-3", "A3 · 3/3", "A3 · Cost — 6. the environment machine, and the four conventions",
  hl=("n-machine", "n-price", "n-succ"),
  crumb="the complete tables behind page 12 · vendor price pages read 2026-09-27 · per-task amounts and shares are our own arithmetic (calc.)",
  body=table(["environment", "price (vendor page)", "1-hour task", "15-min task", "share of a $7.87 API bill", "share of $72.4"], [
   ["Browser Use cloud browser", "$0.02 per browser-hour, billed by the minute, 1-minute minimum; traffic extra (residential proxy $5/GB, direct $0.20/GB); sessions capped at 240 minutes", "$0.020", "$0.005", "0.25%", "0.03%"],
   ["AWS t3.medium (2 vCPU / 4 GiB, Linux, us-east-1)", "$0.0418 per hour on the T3 product page; another AWS page says $0.0416 (0.5% apart)", "$0.042", "$0.010", "0.5%", "0.06%"],
   ["Browserbase cloud browser", "$20 per month for 100 hours, then $0.12 per hour; $99 per month for 500 hours, then $0.10; billed by the minute", "$0.12", "$0.03", "1.5%", "0.17%"],
   ["E2B / Daytona sandbox (2 vCPU / 4 GiB)", "E2B $0.000014 per vCPU-second + $0.0000045 per GiB-second; Daytona $0.0504 per vCPU-hour + $0.0162 per GiB-hour — both $0.1656 per hour", "$0.166", "$0.041", "2.1%", "0.23%"],
   ["Modal sandbox (1 physical core = 2 vCPU, 4 GiB)", "$0.00003942 per core-second + $0.00000667 per GiB-second → $0.238 per hour; billed on the larger of requested and used", "$0.238", "$0.060", "3.0%", "0.33%"],
   ["AWS t3.2xlarge (8 vCPU / 32 GiB, OSWorld 2.0’s default instance)", "$0.3341 per hour", "$0.334", "$0.084", "4.2%", "0.46%"],
   ["OpenAI hosted container (Hosted Shell / Code Interpreter, 4 GB)", "$0.12 per 20-minute session → $0.36 per hour; 1 GB $0.03, 16 GB $0.48, 64 GB $1.92 per 20 minutes", "$0.36", "$0.12", "4.6%", "0.50%"],
  ], ["22%", "42%", "8%", "8%", "10%", "10%"]) + """
<div class="apx-note"><b>The four accounting conventions (page 12), in one line each:</b> output only vs all tokens — 3.2× (OSWorld-Human, $2.43 vs $7.87); per attempt vs per success — 4.9× (OSWorld 2.0, $72.4 ÷ 20.6%); uncached vs cached — 4–50× on the read price by vendor (calc.), far less on the bill (TraceLab: 95.7% hits, prefix still 59.5% of cost); standard vs fast mode — 2× (both vendors), buying only writing speed.</div>""")

A("a4-1", "A4", "A4 · Each cause’s effect on time and on money",
  hl=("n-rtok", "n-wtok", "n-queue", "n-wait", "n-machine"),
  crumb="the complete table behind pages 13–14",
  body=table(["cause", "effect on time", "effect on money", "relationship"], [
   ["Many steps " + tex("(N)", 12), "Roughly linear: one more step is one more call and one more wait (later steps somewhat slower, up to 3×)", "Write tokens linear in " + tex("N", 12) + "; read tokens quadratic, because every step re-reads the whole history", "<b>same source</b> — double the steps: about 2× the time, about 4× the read bill (uncached)"],
   ["Many calls per step " + tex("(J_i)", 12), "linear", "linear", "<b>same source</b>"],
   ["Reading a lot (history, screenshots, rich observations)", "Reading time, longer every step", "Read-token bill", "<b>same source</b> — the same tokens cost time and money"],
   ["Writing a lot (thinking)", "Generation time, roughly 12 ms per token", "Write-token bill at 5× the read price", "<b>same source</b>, and the dearest time: writing is the slowest and the most expensive token"],
   ["Cache hits", "Saves reading time", "Read price 0.02–0.25× of a normal read, by vendor (A3)", "<b>same source</b>, but fragile: editing the history or switching to fast mode invalidates it"],
   ["Queueing", "slow", "free", "<b>slow but not expensive</b>; escaping it means a fast or priority tier at 2×"],
   ["Environment waits (page loads, fixed sleeps)", "slow", "No API cost; machine time by the hour — CPU sandboxes $0.02–0.36 per hour, usually under 5% of the API bill", "<b>slow but not expensive</b>"],
   ["Tool tails (tests, builds)", "slow", "No API cost", "<b>slow but not expensive</b>"],
   ["Failures, idling, retries", "slow", "expensive", "<b>same source</b>, and it turns “per attempt” into “per success”"],
   ["Fast mode", "Writing up to 2.5× faster (vendor-stated); reading unchanged", "2× the price", "<b>money for time</b>"],
   ["Bigger models, more thinking", "slower", "dearer", f"<b>money and time for accuracy</b>, convex: marginal tokens per point 101K → 575K on one model; 6× / 9× / 9.6× tokens for a few points; more thinking not always more accurate {ci('atts','osw2','hal')}"],
   ["Smaller models", "faster", "cheaper", "but if accuracy falls, steps and retries rise — possibly slower and dearer again (inference, no direct evidence)"],
  ], ["22%", "26%", "26%", "26%"]))

A("a5-1", "A5", "A5 · The gaps in the evidence, and what each one blocks",
  crumb="the complete table behind page 14",
  body=table(["gap", "what exists today", "consequence for what can be claimed"], [
   ["Read / write time split and cache hit rate for a frontier API model", f"No measurement reports both; the only read / write split is on locally served 27–31B models {ci('yuan')}; screenshot-agent measurements do not report cache state", "How much of “87–97% in the model” is reading, how much writing, and what remains once the cache is on — unknown"],
   ["How much slower an agent is than a person", f"None of 17 benchmarks measures agent and human elapsed time on the same tasks; the closest is AXIS’s user study, in which a UI agent was 1.69× slower than manual work on easy tasks (small sample) {ci('axis')}", "“X times slower than a person” cannot go on a slide"],
   ["Environment dollars", "Benchmarks report instance types; AgentSysBench reports shares; products publish nothing. Computable from instance type × duration × list price: CPU environments usually 0.3–5% of the API bill (page 12)", "Every benchmark cost is an API bill; the omission is small for CPU environments, not for GPU sandboxes or long idle sessions"],
   ["Whether OSWorld-Human’s “action” includes the 2-s sleep after each step", f"Not stated {ci('code')}; if it does, “actions under 2%” implies more than 100 s per step (calc.)", "“Environment under 3.5%” may understate the waiting"],
   ["The rebound from a smaller model", "No direct evidence on how many extra steps and retries a drop in accuracy causes", "The last row of the relationship table stays marked “inference”"],
   ["How much slowness hurts accuracy", f"Only OSWorld 2.0 records the stale-state failure mode, without its share of failures {ci('osw2')}", "“It exists” can be said; “how large” cannot"],
  ], ["27%", "45%", "28%"]))

# =====================================================================
# PART 2 — acceleration, term by term
# =====================================================================
# Every work is placed on the Part 1 term it changes. Numbers: research/2026-09-28-part2-acceleration-by-term.md
# (every one re-read in its source on 2026-09-28; calc. = our arithmetic; vendor = a vendor's own statement).

REFS_P2 = [   # (key, in-text form, reference), alphabetical; compiled 2026-09-28 from slides/references.md, the ledger and the source checks
 ("infercept", "Abhyankar et al., 2024",
  "Abhyankar, R., He, Z., Srivatsa, V., Zhang, H., &amp; Zhang, Y. (2024). InferCept: Efficient intercept support for augmented large language model inference. <i>Proceedings of the 41st International Conference on Machine Learning (ICML 2024)</i>, PMLR 235, 81–95. arXiv:2402.01869. University of California, San Diego."),
 ("osh", "Abhyankar, Qi &amp; Zhang, 2026",
  "Abhyankar, R., Qi, Q., &amp; Zhang, Y. (2026). OSWorld-Human: Benchmarking the efficiency of computer-use agents. <i>Proceedings of the 9th Conference on Machine Learning and Systems (MLSys 2026)</i>. arXiv:2506.16042. University of California, San Diego; GenseeAI."),
 ("anth-a", "Anthropic, 2026a",
  "Anthropic. (2026a, May 13). <i>Best practices for computer and browser use with Claude</i>. https://claude.com/blog/best-practices-for-computer-and-browser-use-with-claude"),
 ("anth-b", "Anthropic, 2026b",
  "Anthropic. (2026b). <i>Claude API pricing</i>; <i>Prompt caching</i>; <i>Fast mode</i>; <i>Vision</i> (developer documentation, read 28 September 2026). https://platform.claude.com/docs/en/about-claude/pricing; https://platform.claude.com/docs/en/build-with-claude/prompt-caching; https://platform.claude.com/docs/en/build-with-claude/fast-mode; https://platform.claude.com/docs/en/build-with-claude/vision"),
 ("aa-recorder", "Automation Anywhere, 2026",
  "Automation Anywhere. (2026). <i>Automator AI</i> [Product page, undated, read 28 September 2026]; <i>Generative Recorder and resilient automation | April 2024</i> [Community Product Club recap, 13 May 2024]. https://www.automationanywhere.com/products/automator-ai; https://community.automationanywhere.com/generative-recorder-85080/generative-recorder-and-resilient-automation-april-2024-88211 — vendor marketing (the product page’s 60% claims); the recap’s “nearly 50%” is vendor-stated, undefined."),
 ("fara", "Awadallah et al., 2025",
  "Awadallah, A., Lara, Y., Magazine, R., Mozannar, H., Nambi, A., Pandya, Y., Rajeswaran, A., Rosset, C., Taymanov, A., Vineet, V., Whitehead, S., &amp; Zhao, A. (2025). Fara-7B: An efficient agentic model for computer use. arXiv:2511.19663v1. Microsoft (Microsoft Research AI Frontiers; no affiliation line printed)."),
 ("spork", "Bai et al., 2026",
  "Bai, H., Lv, W., Zheng, H., Lu, Y., &amp; Shu, J. (2026). SPORK: Self-speculative forking to accelerate agentic LLM inference. arXiv:2607.03333v1. Tsinghua University; Meituan."),
 ("stagehand", "Browserbase, 2026a",
  "Browserbase. (2026a). <i>How caching works in Stagehand (and where it breaks)</i> [Blog post, by S. Arif, 24 February 2026]; <i>Caching actions</i>, Stagehand v3 and v4 documentation (undated) (read 28 September 2026). https://www.browserbase.com/blog/stagehand-caching; https://docs.stagehand.dev/v3/best-practices/caching; https://docs.stagehand.dev/v4/best-practices/caching — the docs describe the mechanism; the blog’s speed-up figures are vendor marketing."),
 ("browserbase", "Browserbase, 2026b",
  "Browserbase. (2026b). <i>Pricing</i> (read 28 September 2026). https://www.browserbase.com/pricing — vendor pricing."),
 ("latm", "Cai et al., 2024",
  "Cai, T., Wang, X., Ma, T., Chen, X., &amp; Zhou, D. (2024). Large language models as tool makers (LATM). <i>The Twelfth International Conference on Learning Representations (ICLR 2024)</i>. arXiv:2305.17126. Google DeepMind; Princeton University; Stanford University."),
 ("cerebras", "Cerebras, 2026",
  "Cerebras. (2026, August 13). <i>Accelerating GPT-5.6 Sol Ultrafast</i> [Blog post, by J. Er]. https://www.cerebras.ai/blog/accelerating-gpt-5-6-sol-ultrafast-with-openai — vendor and hardware-partner marketing."),
 ("fireact", "Chen et al., 2023",
  "Chen, B., Shu, C., Shareghi, E., Collier, N., Narasimhan, K., &amp; Yao, S. (2023). FireAct: Toward language agent fine-tuning. arXiv:2310.05915v1. System2 Research; University of Cambridge; Monash University; Princeton University."),
 ("simpagent", "Chen et al., 2025",
  "Chen, G., Zhou, X., Shao, R., Lyu, Y., Zhou, K., Wang, S., Li, W., Li, Y., Qi, Z., &amp; Nie, L. (2025). Less is more: Empowering GUI agent with context-aware simplification (SimpAgent). <i>Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV 2025)</i>, 5901–5911. https://doi.org/10.1109/ICCV51701.2025.00558. arXiv:2507.03730. Harbin Institute of Technology (Shenzhen); Huawei Noah’s Ark Lab."),
 ("frugal", "Chen, Zaharia &amp; Zou, 2024",
  "Chen, L., Zaharia, M., &amp; Zou, J. (2024). FrugalGPT: How to use large language models while reducing cost and improving performance. <i>Transactions on Machine Learning Research</i>. arXiv:2305.05176. Stanford University."),
 ("idlespec", "Choi et al., 2026",
  "Choi, D., Park, K., Song, W., Dingliwal, S., Jayanthi, S. M., Shin, J., &amp; Galstyan, A. (2026). IdleSpec: Exploiting idle time via speculative planning for LLM agents. arXiv:2605.22154v1. KAIST; Amazon AGI; Together AI."),
 ("agentx", "Chung et al., 2026",
  "Chung, J., Shin, B., Kim, J., &amp; Rhu, M. (2026). Agent-X: Full pipeline acceleration of on-device AI agents. <i>Proceedings of the 24th Annual International Conference on Mobile Systems, Applications and Services (MobiSys 2026)</i>. https://doi.org/10.1145/3745756.3809195. arXiv:2605.10380. KAIST."),
 ("overthinking", "Cuadron et al., 2025",
  "Cuadron, A., Li, D., Ma, W., Wang, X., Wang, Y., Zhuang, S., … Gonzalez, J. E. (2025). The danger of overthinking: Examining the reasoning-action dilemma in agentic tasks. arXiv:2502.08235v1. University of California, Berkeley; ETH Zurich; University of Illinois Urbana-Champaign; Carnegie Mellon University."),
 ("deepseek", "DeepSeek, 2026",
  "DeepSeek. (2026). <i>Models &amp; pricing</i> (API documentation, read 28 September 2026); <i>DeepSeek-V4.1-Flash release</i> (10 September 2026). https://api-docs.deepseek.com/quick_start/pricing; https://api-docs.deepseek.com/news/news260910"),
 ("weboperator", "Dihan et al., 2025",
  "Dihan, M. L., Hashem, T., Ali, M. E., &amp; Parvez, M. R. (2025). WebOperator: Action-aware tree search for autonomous agents in web environment. arXiv:2512.12692v1. Bangladesh University of Engineering and Technology; Monash University; Qatar Computing Research Institute."),
 ("deltabox", "Dong et al., 2026",
  "Dong, Y., He, J., Liu, S., Hou, Y., Du, D., Xu, Z., Yu, S., Yang, B., Xia, Y., &amp; Chen, H. (2026). DeltaBox: Scaling stateful AI agents with millisecond-level sandbox checkpoint/rollback. arXiv:2605.22781v2. Shanghai Jiao Tong University (IPADS); Huawei Technologies."),
 ("enomoto", "Enomoto et al., 2026",
  "Enomoto, M., Obara, R., Zhang, H., &amp; Oyamada, M. (2026). Revisiting observation reduction for web agents: Comprehensive evaluation with a lightweight framework. arXiv:2605.29397v1. NEC Corporation."),
 ("cop", "Erol et al., 2026",
  "Erol, M. H., El, B., Suzgun, M., Yuksekgonul, M., &amp; Zou, J. (2026). Cost-of-Pass: An economic framework for evaluating language models. <i>The Fourteenth International Conference on Learning Representations (ICLR 2026)</i>. arXiv:2504.13359v2. Stanford University."),
 ("tsds", "Farzaneh &amp; Simeone, 2026",
  "Farzaneh, A., &amp; Simeone, O. (2026). Think short, defer smart, act, and repeat: Calibrated reasoning and uncertainty-aware deferral for edge LLM agents. arXiv:2607.26865v3. Northeastern University London."),
 ("asyncfc", "Feng et al., 2026",
  "Feng, G., Mao, H., Dutta, P., &amp; Gonzalez, J. E. (2026). Concurrency without model changes: Future-based asynchronous function calling for LLMs (AsyncFC). arXiv:2605.15077v1. University of California, Berkeley."),
 ("asynclm", "Gim et al., 2024",
  "Gim, I., Lee, S., &amp; Zhong, L. (2024). Asynchronous LLM function calling (AsyncLM). arXiv:2412.07017v1. Yale University."),
 ("google", "Google, 2026",
  "Google. (2026). <i>Gemini Developer API pricing</i>; <i>Priority inference</i> (Gemini API documentation, updated 24 and 23 September 2026; read 28 September 2026). https://ai.google.dev/gemini-api/docs/pricing; https://ai.google.dev/gemini-api/docs/priority-inference"),
 ("dsp", "Guan et al., 2026",
  "Guan, Y., Lan, Q., Sun, F., Ding, D., Acharya, D., Wang, C., Wang, W. Y., &amp; Hua, W. (2026). Dynamic speculative agent planning. <i>The Fourteenth International Conference on Learning Representations (ICLR 2026)</i>. arXiv:2509.01920. Johns Hopkins University; University of Alberta; University of British Columbia; Avey Research Center; Google DeepMind; University of California, Santa Barbara."),
 ("eet", "Guo et al., 2026",
  "Guo, Y., Xiao, Y., Zhang, J. M., Harman, M., Lou, Y., Liu, Y., &amp; Chen, Z. (2026). EET: Experience-driven early termination for cost-efficient software engineering agents. <i>Findings of the Association for Computational Linguistics: ACL 2026</i>, 33008–33024. https://doi.org/10.18653/v1/2026.findings-acl.1652. arXiv:2601.05777. Nanyang Technological University; King’s College London; University College London; University of Illinois Urbana-Champaign; Tsinghua University."),
 ("hajimiri", "Hajimiri et al., 2026",
  "Hajimiri, S., Aminbeidokhti, M., Dolz, J., Ben Ayed, I., Laradji, I. H., Gella, S., &amp; Gontier, N. (2026). Are online skill and memory modules always worth their tokens? A budget-constrained study of web agents. arXiv:2606.15017v2 (arXiv comment: “Accepted to EMNLP 2026”; not yet on an official EMNLP 2026 list). ServiceNow AI Research; ÉTS Montréal; University of British Columbia; McGill University."),
 ("isp", "Hua et al., 2025",
  "Hua, W., Wan, M., Vadrevu, S., Nadel, R., Zhang, Y., &amp; Wang, C. (2025). Interactive speculative planning: Enhance agent efficiency through co-design of system and user interface. <i>The Thirteenth International Conference on Learning Representations (ICLR 2025)</i>. arXiv:2410.00079. Rutgers University; Microsoft; Google DeepMind."),
 ("guikv", "Huang et al., 2026a",
  "Huang, K.-H., Qiu, H., Dai, Y., Xiong, C., &amp; Wu, C.-S. (2026a). GUI-KV: Efficient GUI agents via KV cache with spatio-temporal awareness. <i>Transactions on Machine Learning Research</i>. arXiv:2510.00536. Salesforce AI Research; University of California, Los Angeles."),
 ("tclone", "Huang et al., 2026b",
  "Huang, Y., Srivatsa, V., Asch, A., Patwa, H. T., &amp; Zhang, Y. (2026b). TClone: Low-latency forking of live GUI environments for computer-use agents. arXiv:2605.17320v1. University of California, San Diego; GenseeAI."),
 ("speedrunner", "Huang et al., 2026c",
  "Huang, Z., Wang, X., Wang, A., Jurayj, W., Jiménez Gutiérrez, B., Khashabi, D., &amp; Andrews, N. (2026c). Better, faster, stronger: Programmatic skill learning best reduces agent cost (SpeedRunner). arXiv:2608.11338v1. Johns Hopkins University."),
 ("hyperagent", "Hyperbrowser, 2026",
  "Hyperbrowser. (2026). <i>Action caching</i> (HyperAgent documentation, undated, read 28 September 2026); <i>HyperAgent</i> [Source code], README.md on the main branch. https://www.hyperbrowser.ai/docs/hyperagent/action-cache; https://github.com/hyperbrowserai/HyperAgent — vendor documentation; “near-instant replay” is vendor marketing."),
 ("autotool", "Jia &amp; Li, 2026",
  "Jia, J., &amp; Li, Q. (2026). AutoTool: Efficient tool selection for large language model agents. <i>Proceedings of the AAAI Conference on Artificial Intelligence, 40</i>(37), 31265–31273. https://doi.org/10.1609/aaai.v40i37.40389. arXiv:2511.14650. Huazhong University of Science and Technology."),
 ("appagentx", "Jiang et al., 2025",
  "Jiang, W., Zhuang, Y., Song, C., Yang, X., Zhou, J. T., &amp; Zhang, C. (2025). AppAgentX: Evolving GUI agents as proficient smartphone users. arXiv:2503.02268v3. Westlake University; Henan University; Southeast University; A*STAR (IHPC; CFAR)."),
 ("thunder", "Kang et al., 2026",
  "Kang, H., Li, Z., Yang, X., Xu, W., Chen, Y., Wang, J., Chen, B., Krishna, T., Xu, C., &amp; Arora, S. (2026). ThunderAgent: A fast, simple, and program-aware agentic inference system. <i>Proceedings of the 43rd International Conference on Machine Learning (ICML 2026)</i>, poster. arXiv:2602.13692. Georgia Institute of Technology; University of Illinois Urbana-Champaign; Carnegie Mellon University; Together AI; independent researcher."),
 ("kapoor25", "Kapoor et al., 2025",
  "Kapoor, S., Stroebl, B., Siegel, Z. S., Nadgir, N., &amp; Narayanan, A. (2025). AI agents that matter. <i>Transactions on Machine Learning Research</i>. arXiv:2407.01502. Princeton University."),
 ("focusagent", "Kerboua et al., 2026",
  "Kerboua, I., Omidi Shayegan, S., Lù, X. H., Boisvert, L., Thakkar, M., Caccia, M., Espinas, J., Aussem, A., Eglin, V., &amp; Lacoste, A. (2026). FocusAgent: Simple yet effective ways of trimming the large context of web agents. <i>Transactions on Machine Learning Research</i>. arXiv:2510.03204. Esker; INSA Lyon; ServiceNow Research; Mila; McGill University; Polytechnique Montréal; Université Lyon 1 (LIRIS)."),
 ("lineretriever", "Kerboua et al., 2025",
  "Kerboua, I., Omidi Shayegan, S., Thakkar, M., Lù, X. H., Caccia, M., Eglin, V., Aussem, A., Espinas, J., &amp; Lacoste, A. (2025). LineRetriever: Planning-aware observation reduction for web agents. arXiv:2507.00210v1. INSA Lyon; Esker; ServiceNow Research; Mila; McGill University; Université Lyon 1 (LIRIS)."),
 ("agenticcache", "Kim et al., 2026",
  "Kim, H., Wu, Y., &amp; Tambe, T. (2026). AgenticCache: Cache-driven asynchronous planning for embodied AI agents. <i>Proceedings of the 9th Conference on Machine Learning and Systems (MLSys 2026)</i>. arXiv:2604.24039. Seoul National University; Stanford University."),
 ("llmc", "Kim et al., 2024",
  "Kim, S., Moon, S., Tabrizi, R., Lee, N., Mahoney, M. W., Keutzer, K., &amp; Gholami, A. (2024). An LLM compiler for parallel function calling. <i>Proceedings of the 41st International Conference on Machine Learning (ICML 2024)</i>, PMLR 235. arXiv:2312.04511. University of California, Berkeley; International Computer Science Institute; Lawrence Berkeley National Laboratory."),
 ("computerrl", "Lai et al., 2026",
  "Lai, H., Liu, X., Zhao, Y., Xu, H., Zhang, H., Jing, B., Ren, Y., Yao, S., Dong, Y., &amp; Tang, J. (2026). ComputerRL: Scaling end-to-end online reinforcement learning for computer use agents. <i>The Fourteenth International Conference on Learning Representations (ICLR 2026)</i>. arXiv:2508.14040. Tsinghua University; Z.AI; University of Chinese Academy of Sciences."),
 ("agentreuse", "Li et al., 2024",
  "Li, G., Wu, R., Tan, H., &amp; Chen, G. (2024). A plan reuse mechanism for LLM-driven agent. <i>Journal of Computer Research and Development, 61</i>(11), 2706–2720. https://doi.org/10.7544/issn1000-1239.202440380. English version: Li, G., Wu, R., &amp; Tan, H. (2025), arXiv:2512.21309v2. University of Science and Technology of China."),
 ("continuum", "Li et al., 2026a",
  "Li, H., He, R., Mang, Q., Zhang, Q., Mao, H., Chen, X., Zhou, H., Zhang, H., Cheung, A., Gonzalez, J., &amp; Stoica, I. (2026a). Continuum: Efficient and robust multi-turn LLM agent scheduling with KV cache time-to-live. arXiv:2511.02230v7. University of California, Berkeley; Stanford University; Tsinghua University."),
 ("screenseeker", "Li et al., 2025",
  "Li, K., Meng, Z., Lin, H., Luo, Z., Tian, Y., Ma, J., Huang, Z., &amp; Chua, T.-S. (2025). ScreenSpot-Pro: GUI grounding for professional high-resolution computer use. <i>Proceedings of the 33rd ACM International Conference on Multimedia (MM 2025)</i>, 8778–8786. https://doi.org/10.1145/3746027.3755688. arXiv:2504.07981. National University of Singapore; East China Normal University; Hong Kong Baptist University."),
 ("webrouter", "Li et al., 2026b",
  "Li, T., Hu, J., Wang, Y., Liu, J., &amp; Liu, X. (2026b). WebRouter: Query-specific router via variational information bottleneck for cost-sensitive web agent. <i>ICASSP 2026 – IEEE International Conference on Acoustics, Speech and Signal Processing</i>, 4086–4090. https://doi.org/10.1109/ICASSP55912.2026.11464950. arXiv:2510.11221. Nanjing University of Aeronautics and Astronautics; Hong Kong Baptist University; Beihang University; Pengcheng Laboratory."),
 ("swm", "Li et al., 2026c",
  "Li, Y., Ye, Q., Choubey, P. K., Zhang, J., &amp; Wu, C.-S. (2026c). Speculate with memory: Lossless acceleration for LLM agents. arXiv:2607.12236v1. Salesforce Research."),
 ("parrot", "Lin et al., 2024",
  "Lin, C., Han, Z., Zhang, C., Yang, Y., Yang, F., Chen, C., &amp; Qiu, L. (2024). Parrot: Efficient serving of LLM-based applications with semantic variable. <i>18th USENIX Symposium on Operating Systems Design and Implementation (OSDI 24)</i>. Shanghai Jiao Tong University; Microsoft Research."),
 ("wd", "Lin et al., 2026",
  "Lin, X., Liew, J. H., Savarese, S., &amp; Li, J. (2026). W&amp;D: Scaling parallel tool calling for efficient deep research agents. arXiv:2602.07359v1. Salesforce AI Research."),
 ("masking", "Lindenbauer et al., 2025",
  "Lindenbauer, T., Slinko, I., Felder, L., Bogomolov, E., &amp; Zharov, Y. (2025). The complexity trap: Simple observation masking is as efficient as LLM summarization for agent context management. Paper presented at the 4th Deep Learning for Code Workshop (DL4C): Deep Learning for Code in the Agentic Era, NeurIPS 2025. arXiv:2508.21433v3. JetBrains Research; Technical University of Munich."),
 ("bats", "Liu et al., 2026a",
  "Liu, T., Wang, Z., Miao, J., Hsu, I.-H., Yan, J., Chen, J., … Lee, C.-Y. (2026a). Budget-aware tool use enables effective agent scaling (Budget Tracker, BATS). <i>Third Conference on Language Modeling (COLM 2026)</i>. arXiv:2511.17006. University of California, Santa Barbara; Google Cloud AI Research; Google DeepMind; New York University."),
 ("droidspeak", "Liu et al., 2026b",
  "Liu, Y., Huang, Y., Yao, J., Feng, S., Gu, Z., Du, K., Li, H., Cheng, Y., Jiang, J., Lu, S., Musuvathi, M., &amp; Choukse, E. (2026b). DroidSpeak: KV cache sharing across fine-tuned model variants. <i>23rd USENIX Symposium on Networked Systems Design and Implementation (NSDI 26)</i>, 319–338. arXiv:2411.02820 (under another title). University of Chicago; Microsoft."),
 ("smc", "Liu et al., 2026c",
  "Liu, Z., Kundu, S., &amp; Beerel, P. A. (2026c). Speculative macro commit for faster tool-using agents. arXiv:2609.03236v1 (arXiv comment: “Accepted in MLSP2026”). University of Southern California; Intel Labs."),
 ("axis", "Lu et al., 2025a",
  "Lu, J., Zhang, Z., Yang, F., Zhang, J., Wang, L., Du, C., Lin, Q., Rajmohan, S., Zhang, D., &amp; Zhang, Q. (2025a). AXIS: Efficient human-agent-computer interaction with API-first LLM-based agents. <i>Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)</i>, 7711–7743. https://doi.org/10.18653/v1/2025.acl-long.381. Peking University; Nanjing University; Microsoft."),
 ("runaway", "Lu et al., 2025b",
  "Lu, Q., Ding, L., Cao, S., Liu, X., Zhang, K., Zhang, J., &amp; Tao, D. (2025b). Runaway is ashamed, but helpful: On the early-exit behavior of large language model-based agents in embodied environments. <i>Findings of the Association for Computational Linguistics: EMNLP 2025</i>, 24014–24027. https://doi.org/10.18653/v1/2025.findings-emnlp.1304. arXiv:2505.17616. Southeast University; The University of Sydney; Harbin Institute of Technology (Shenzhen); Nanyang Technological University."),
 ("dbtc", "Lumer et al., 2026",
  "Lumer, E., Nizar, F., Jangiti, A., Frank, K., Gulati, A., Phadate, M., &amp; Subbiah, V. K. (2026). Don’t break the cache: An evaluation of prompt caching for long-horizon agentic tasks. arXiv:2601.06007v2. PricewaterhouseCoopers (PwC U.S.)."),
 ("agentix", "Luo et al., 2026",
  "Luo, M., Shi, X., Cai, C., Zhang, T., Wong, J., Wang, Y., Wang, C., Huang, Y., Chen, Z., Gonzalez, J. E., &amp; Stoica, I. (2026). Agentix: An efficient serving engine for LLM agents as general programs. <i>23rd USENIX Symposium on Networked Systems Design and Implementation (NSDI 26)</i>. University of California, Berkeley; Google DeepMind; Shanghai Jiao Tong University."),
 ("microsoft", "Microsoft, 2026a",
  "Microsoft. (2026a). <i>Enable priority processing for Microsoft Foundry models</i> (Microsoft Learn, 22 September 2026); <i>Azure OpenAI pricing</i> (prices taken from the page’s data attributes, US East) (read 28 September 2026). https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/priority-processing; https://azure.microsoft.com/en-us/pricing/details/azure-openai/"),
 ("powerautomate", "Microsoft, 2026b",
  "Microsoft. (2026b). <i>Self-healing (preview)</i> (Power Automate documentation, Microsoft Learn, 30 June 2026, updated 11 July 2026); <i>FAQ for Repair with Copilot at runtime in Power Automate desktop</i> (16 January 2026) (read 28 September 2026). https://learn.microsoft.com/en-us/power-automate/desktop-flows/self-healing; https://learn.microsoft.com/en-us/power-automate/faqs-repair-copilot — vendor documentation."),
 ("ghost", "Mohammadi et al., 2026a",
  "Mohammadi, B., Klein, L., Arora, A., &amp; Bindschaedler, L. (2026a). Ghost tool calls: Issue-time privacy for speculative agent tools. arXiv:2606.02483v1. Max Planck Institute for Software Systems; EPFL; Aarhus University."),
 ("atomix", "Mohammadi et al., 2026b",
  "Mohammadi, B., Potamitis, N., Klein, L., Arora, A., &amp; Bindschaedler, L. (2026b). Atomix: Timely, transactional tool use for reliable agentic workflows. arXiv:2602.14849v2. Max Planck Institute for Software Systems; Aarhus University; EPFL."),
 ("nichols", "Nichols et al., 2025",
  "Nichols, D., Singhania, P., Jekel, C., Bhatele, A., &amp; Menon, H. (2025). Optimizing agentic language model inference via speculative tool calls. arXiv:2512.15834v1. Lawrence Livermore National Laboratory; University of Maryland."),
 ("routellm", "Ong et al., 2025",
  "Ong, I., Almahairi, A., Wu, V., Chiang, W.-L., Wu, T., Gonzalez, J. E., Kadous, M. W., &amp; Stoica, I. (2025). RouteLLM: Learning to route LLMs from preference data. <i>The Thirteenth International Conference on Learning Representations (ICLR 2025)</i>. arXiv:2406.18665. University of California, Berkeley; Anyscale; Canva."),
 ("openai", "OpenAI, 2026",
  "OpenAI. (2026). <i>API pricing</i>; <i>API changelog</i> (Priority processing, 27 June 2025; Fast mode, 30 July and 5 August 2026; Ultrafast, 13 August 2026); <i>Fast mode</i>, <i>Flex processing</i>, <i>Batch API</i> and <i>Prompt caching</i> guides (developer documentation, read 28 September 2026); <i>Prompt Caching 201</i> (OpenAI Cookbook, 18 February 2026). https://developers.openai.com/api/docs/pricing; https://developers.openai.com/api/docs/changelog; https://developers.openai.com/api/docs/guides/fast-mode; https://developers.openai.com/api/docs/guides/flex-processing; https://developers.openai.com/api/docs/guides/batch; https://developers.openai.com/api/docs/guides/prompt-caching; https://developers.openai.com/cookbook/examples/prompt_caching_201"),
 ("kvflow", "Pan et al., 2025",
  "Pan, Z., Patel, A., Shen, Y., Hu, Z., Guan, Y., Li, W.-L., Qin, L., Wang, Y., &amp; Ding, Y. (2025). KVFlow: Efficient prefix caching for accelerating LLM-based multi-agent workflows. <i>Advances in Neural Information Processing Systems 38 (NeurIPS 2025)</i>, 139912–139931. https://doi.org/10.52202/085713-4208. arXiv:2507.07400. University of California, San Diego; Amazon Web Services."),
 ("walt", "Prabhu et al., 2026",
  "Prabhu, V., Dai, Y., Fernandez, M., Ramakrishnan, K., Gu, J., Luo, Y., Savarese, S., Xiong, C., Li, J., Chen, Z., &amp; Xu, R. (2026). WALT: Web agents that learn tools. <i>The Fourteenth International Conference on Learning Representations (ICLR 2026)</i>. arXiv:2510.01524. Salesforce AI Research."),
 ("eam", "Qin et al., 2026",
  "Qin, Z., Yue, S., Hua, X., Fu, Y., &amp; Ren, J. (2026). Executable agentic memory for GUI agent. <i>Proceedings of the 43rd International Conference on Machine Learning (ICML 2026)</i>. arXiv:2605.12294. Tsinghua University; Sun Yat-sen University."),
 ("tti", "Shen et al., 2025",
  "Shen, J., Bai, H., Zhang, L., Zhou, Y., Setlur, A., Tong, S., Caples, D., Jiang, N., Zhang, T., Talwalkar, A., &amp; Kumar, A. (2025). Thinking vs. doing: Improving agent reasoning by scaling test-time interaction. <i>Advances in Neural Information Processing Systems 38 (NeurIPS 2025)</i>, 187840–187881. https://doi.org/10.52202/085713-5647. arXiv:2506.07976 (under another title). Carnegie Mellon University; Scribe; University of Illinois Urbana-Champaign; University of Toronto; University of California, Berkeley; The AGI Company; New York University."),
 ("asymcache", "Shi et al., 2026a",
  "Shi, C., Chen, Y., Chen, Y., Miao, X., &amp; Cui, B. (2026a). Multi-segment attention: Enabling efficient KV-cache management for faster large language model serving (AsymCache). arXiv:2606.02964v1. Peking University."),
 ("cuaverse", "Shi et al., 2026b",
  "Shi, H., Wang, W., Fang, W., Liang, Y., Jin, T., Zhao, P., Liu, G., Chen, S., &amp; Wang, Y. (2026b). CUA-Universe: A scalable and dynamic environment for hybrid GUI+CLI agents. arXiv:2609.05374v1. Shanghai Jiao Tong University; Zhejiang University."),
 ("skyvern", "Skyvern, 2026",
  "Skyvern. (2026). <i>Code caching</i>; <i>Cost control</i> (developer documentation, undated, read 28 September 2026). https://www.skyvern.com/docs/developers/features/code-caching; https://skyvern.mintlify.app/developers/optimization/cost-control — vendor documentation."),
 ("coact1", "Song et al., 2026",
  "Song, L., Dai, Y., Prabhu, V., Zhang, J., Shi, T., Li, L., Li, J., Savarese, S., Chen, Z., Zhao, J., Xu, R., &amp; Xiong, C. (2026). CoAct-1: Computer-using multi-agent system with coding actions. <i>The Fourteenth International Conference on Learning Representations (ICLR 2026)</i>. arXiv:2508.03923. University of Southern California; Salesforce; University of Washington."),
 ("beyondbrowsing", "Song et al., 2025",
  "Song, Y., Xu, F. F., Zhou, S., &amp; Neubig, G. (2025). Beyond browsing: API-based web agents. <i>Findings of the Association for Computational Linguistics: ACL 2025</i>, 11066–11085. https://doi.org/10.18653/v1/2025.findings-acl.577. arXiv:2410.16464. Carnegie Mellon University."),
 ("preble", "Srivatsa et al., 2025",
  "Srivatsa, V., He, Z., Abhyankar, R., Li, D., &amp; Zhang, Y. (2025). Preble: Efficient distributed prompt scheduling for LLM serving. <i>The Thirteenth International Conference on Learning Representations (ICLR 2025)</i>. arXiv:2407.00023. University of California, San Diego."),
 ("thinktwice", "Tang et al., 2025",
  "Tang, F., Shen, Y., Zhang, H., Chen, S., Hou, G., Zhang, W., Zhang, W., Song, K., Lu, W., &amp; Zhuang, Y. (2025). Think twice, click once: Enhancing GUI grounding via fast and slow systems (FOCUS). arXiv:2503.06470v1. Zhejiang University; Microsoft Research Asia."),
 ("uipath", "UiPath, 2026",
  "UiPath. (2026). <i>Healing Agent user guide</i>: <i>What is Healing Agent?</i>; <i>Recovery strategies</i>; <i>Licensing</i>; <i>Frequently asked questions</i> (Automation Cloud documentation, undated, read 28 September 2026). https://docs.uipath.com/agents/automation-cloud/latest/user-guide-ha/what-is-healing-agent; https://docs.uipath.com/agents/automation-cloud/latest/user-guide-ha/deterministic-recovery-strategies; https://docs.uipath.com/agents/automation-cloud/latest/user-guide-ha/licensing; https://docs.uipath.com/agents/automation-cloud/latest/user-guide-ha/frequently-asked-questions — vendor documentation."),
 ("helium", "Wadlom et al., 2026",
  "Wadlom, N., Shen, J., &amp; Lu, Y. (2026). Efficient LLM serving for agentic workflows: A data systems perspective (Helium). <i>Proceedings of the ACM on Management of Data, 4</i> (SIGMOD 2026). https://doi.org/10.1145/3802046. arXiv:2603.16104v1 (extended version). National University of Singapore."),
 ("effagents", "Wang et al., 2025a",
  "Wang, N., Hu, X., Liu, P., Zhu, H., Hou, Y., Huang, H., … Zhou, W. (2025a). Efficient agents: Building effective agents while reducing cost. arXiv:2508.02694v1. OPPO (OPPO AI Agent Team)."),
 ("asi", "Wang et al., 2025b",
  "Wang, Z. Z., Gandhi, A., Neubig, G., &amp; Fried, D. (2025b). Inducing programmatic skills for agentic tasks (ASI). <i>Second Conference on Language Modeling (COLM 2025)</i>. arXiv:2504.06821. Carnegie Mellon University."),
 ("awm", "Wang et al., 2025c",
  "Wang, Z. Z., Mao, J., Fried, D., &amp; Neubig, G. (2025c). Agent workflow memory. <i>Proceedings of the 42nd International Conference on Machine Learning (ICML 2025)</i>, PMLR 267, 63897–63911. arXiv:2409.07429. Carnegie Mellon University; Massachusetts Institute of Technology."),
 ("stepwise", "Wei et al., 2026",
  "Wei, J., Ni, K., Zhao, Y., Gan, G., &amp; Cohan, A. (2026). Step-level optimization for efficient computer-use agents (StepWise). arXiv:2604.27151v1. Yale University; University of North Carolina at Chapel Hill."),
 ("autodroid2", "Wen et al., 2025",
  "Wen, H., Tian, S., Pavlov, B., Du, W., Li, Y., Chang, G., Zhao, S., Liu, J., Liu, Y., Zhang, Y.-Q., &amp; Li, Y. (2025). AutoDroid-V2: Boosting SLM-based GUI agents via code generation. <i>Proceedings of the 23rd Annual International Conference on Mobile Systems, Applications and Services (MobiSys 2025)</i>, 223–235. https://doi.org/10.1145/3711875.3729134. arXiv:2412.18116. Tsinghua University (AIR); Shanghai AI Laboratory; Beijing Academy of Artificial Intelligence."),
 ("jit", "Winston et al., 2026",
  "Winston, C., Wang, R. Y., Mirhoseini, A., &amp; Kozyrakis, C. (2026). Agent JIT compilation for latency-optimizing web agent planning and scheduling. <i>Proceedings of the 43rd International Conference on Machine Learning (ICML 2026)</i>, PMLR 306. arXiv:2605.21470. Stanford University."),
 ("skim", "Wong et al., 2026",
  "Wong, M., Hsieh, K., Nath, S., &amp; Netravali, R. (2026). Skim: Speculative execution for fast and efficient web agents. arXiv:2605.16565v2. Princeton University; Microsoft Research."),
 ("saferesume", "Wu et al., 2026",
  "Wu, G., Li, D., Jiang, K., Niu, J., Wang, C., &amp; Zhang, Y. (2026). Safe to resume? Breaking execution continuity of agent execution via rollback. arXiv:2608.29381v1. Southern University of Science and Technology; City University of Hong Kong."),
 ("xai", "xAI, 2026",
  "xAI. (2026). <i>Grok 4.7</i> model page, SpaceXAI Docs (read 28 September 2026). https://docs.x.ai/developers/models/grok-4.7"),
 ("toolspec", "Xia et al., 2026",
  "Xia, H., Li, Y., Du, C., Song, M., &amp; Li, W. (2026). ToolSpec: Accelerating tool calling via schema-aware and retrieval-augmented speculative decoding. arXiv:2604.13519v2. The Hong Kong Polytechnic University; Peking University."),
 ("agentdiet", "Xiao et al., 2026",
  "Xiao, Y.-A., Gao, P., Peng, C., &amp; Xiong, Y. (2026). Reducing cost of LLM agents with trajectory reduction (AgentDiet). <i>Proceedings of the ACM on Software Engineering, 3</i>(FSE), Article FSE056. https://doi.org/10.1145/3797084. arXiv:2509.23586. Peking University; ByteDance."),
 ("osw2", "XLANG Lab, 2026",
  "XLANG Lab. (2026). OSWorld 2.0: Benchmarking computer use agents on long-horizon real-world tasks. arXiv:2606.29537v2. The University of Hong Kong (authored as “XLANG Lab and Collaborators”; the full author list is in the paper’s Appendix A)."),
 ("tokenpilot", "Xu et al., 2026a",
  "Xu, B., Xue, Z., Chen, D., Fu, C., Wu, C., Huang, C., … Zhang, N. (2026a). TokenPilot: Cache-efficient context management for LLM agents. arXiv:2606.17016v2 (arXiv comment: “EMNLP 2026 Findings”; not yet on an official EMNLP 2026 list). Zhejiang University; University of Electronic Science and Technology of China; Xidian University; HomologyAI."),
 ("tpsbench", "Xu et al., 2026b",
  "Xu, H., Huang, X., Liu, Y., &amp; Deng, Z. (2026b). TPS-Bench: Evaluating AI agents’ tool planning &amp; scheduling abilities in compounding tasks. <i>Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)</i>, 34949–34961. https://doi.org/10.18653/v1/2026.acl-long.1614. arXiv:2511.01527. Shanghai Jiao Tong University."),
 ("aguvis", "Xu et al., 2025",
  "Xu, Y., Wang, Z., Wang, J., Lu, D., Xie, T., Saha, A., Sahoo, D., Yu, T., &amp; Xiong, C. (2025). Aguvis: Unified pure vision agents for autonomous GUI interaction. <i>Proceedings of the 42nd International Conference on Machine Learning (ICML 2025)</i>, PMLR 267. arXiv:2412.04454. The University of Hong Kong; Salesforce Research."),
 ("ares", "Yang et al., 2026a",
  "Yang, J., Hou, B., Wei, W., Bao, Y., &amp; Chang, S. (2026a). Ares: Adaptive reasoning effort selection for efficient LLM agents. arXiv:2603.07915v1. University of California, Santa Barbara; Accenture."),
 ("agentoccam", "Yang et al., 2025",
  "Yang, K., Liu, Y., Chaudhary, S., Fakoor, R., Chaudhari, P., Karypis, G., &amp; Rangwala, H. (2025). AgentOccam: A simple yet strong baseline for LLM-based web agents. <i>The Thirteenth International Conference on Learning Representations (ICLR 2025)</i>. arXiv:2410.13825. University of Illinois Urbana-Champaign; Amazon."),
 ("space", "Yang et al., 2026b",
  "Yang, Y., Jin, C., Zhao, J., Wu, J., Zhou, Y., Wang, Z., Wang, Z., Zhou, M., &amp; Metaxas, D. N. (2026b). Act more, decide less: Skill-guided adaptive action chunking for long-horizon LLM agents (SPACE). arXiv:2609.02042v1 (arXiv comment: “EMNLP 2026 Camera Ready”; not yet on an official EMNLP 2026 list). Rutgers University; University of Toronto; The Hong Kong Polytechnic University; Amazon; Microsoft."),
 ("cacheblend", "Yao et al., 2025",
  "Yao, J., Li, H., Liu, Y., Ray, S., Cheng, Y., Zhang, Q., Du, K., Lu, S., &amp; Jiang, J. (2025). CacheBlend: Fast large language model serving for RAG with cached knowledge fusion. <i>Proceedings of the Twentieth European Conference on Computer Systems (EuroSys 2025)</i>, 94–109. https://doi.org/10.1145/3689031.3696098. arXiv:2405.16444. University of Chicago; The Chinese University of Hong Kong, Shenzhen; Stanford University; Microsoft Research."),
 ("kvcomm", "Ye et al., 2025",
  "Ye, H., Gao, Z., Ma, M., Wang, Q., Fu, Y., Chung, M.-Y., Lin, Y., Liu, Z., Zhang, J., Zhuo, D., &amp; Chen, Y. (2025). KVCOMM: Online cross-context KV-cache communication for efficient LLM-based multi-agent systems. <i>Advances in Neural Information Processing Systems 38 (NeurIPS 2025)</i>. https://doi.org/10.52202/085713-0605. arXiv:2510.12872. Duke University; Massachusetts Institute of Technology; NVIDIA."),
 ("specactions", "Ye et al., 2026",
  "Ye, N., Ahuja, A., Liargkovas, G., Lu, Y., Kaffes, K., &amp; Peng, T. (2026). Speculative actions: A lossless framework for faster AI agents. <i>The Fourteenth International Conference on Learning Representations (ICLR 2026)</i>, oral. arXiv:2510.04371. Columbia University."),
 ("paragui", "Yu et al., 2026",
  "Yu, Z., Li, Q., Gao, Z., Xiang, L., Shi, C., Liu, Y., Wu, H., Wei, Y., Fei, Y., Fu, Y., &amp; He, Z. (2026). Beyond sequential interaction: Benchmarking parallel execution and coordination for GUI agents (ParaGUIBench). arXiv:2607.22689v1. Beijing University of Posts and Telecommunications; BIGAI; China University of Geosciences (Beijing); Beijing Institute of Technology."),
 ("toolcaching", "Zhai et al., 2026",
  "Zhai, Y., Shen, D., Luo, J., &amp; Yang, B. (2026). ToolCaching: Towards efficient caching for LLM tool-calling. arXiv:2601.15335v1. Southeast University."),
 ("ufo2", "Zhang et al., 2026a",
  "Zhang, C., Huang, H., Ni, C., Mu, J., Qin, S., He, S., … Zhang, D. (2026a). UFO2: The desktop AgentOS. <i>Transactions on Machine Learning Research</i>. arXiv:2504.14603. Microsoft; ZJU-UIUC Institute; Nanjing University; Peking University."),
 ("bopo", "Zhang et al., 2026b",
  "Zhang, C., Xia, M., Zhang, X., Madrigal, D., Mallick, A., Kessler, S., Rühle, V., &amp; Rajmohan, S. (2026b). Budget-aware agentic routing via boundary-guided training (BoPO). arXiv:2602.21227v1. University of Cambridge; Microsoft (M365 Research)."),
 ("prune4web", "Zhang et al., 2026c",
  "Zhang, J., Chen, K., Lu, Z., Zhou, E., Yu, Q., &amp; Zhang, J. (2026c). Prune4Web: DOM tree pruning programming for web agent. <i>Proceedings of the AAAI Conference on Artificial Intelligence, 40</i>(41), 34710–34718. https://doi.org/10.1609/aaai.v40i41.40772. arXiv:2511.21398. Beihang University."),
 ("cotmobile", "Zhang et al., 2026d",
  "Zhang, L., Gao, L., &amp; Xu, M. (2026d). Does chain-of-thought reasoning help mobile GUI agents? An empirical study. <i>Findings of the Association for Computational Linguistics: ACL 2026</i>, 7981–7996. https://doi.org/10.18653/v1/2026.findings-acl.392. Beijing University of Posts and Telecommunications; Tsinghua University."),
 ("apc", "Zhang et al., 2025",
  "Zhang, Q., Wornow, M., &amp; Olukotun, K. (2025). Agentic plan caching: Test-time memory for fast and cost-efficient LLM agents. <i>Advances in Neural Information Processing Systems 38 (NeurIPS 2025)</i>. https://doi.org/10.52202/085713-3451. arXiv:2506.14852 (v2 adds a fourth author, G. Wan). Stanford University."),
 ("echopath", "Zhao et al., 2026",
  "Zhao, Y., Shanmugham, A., Roy, S., &amp; Xu, Y. (2026). EchoPath: Execution-level replayable memory for GUI agents. arXiv:2609.16635v1. Johns Hopkins University; Amazon AGI."),
 ("sglang", "Zheng et al., 2024",
  "Zheng, L., Yin, L., Xie, Z., Sun, C., Huang, J., Yu, C. H., Cao, S., Kozyrakis, C., Stoica, I., Gonzalez, J. E., Barrett, C., &amp; Sheng, Y. (2024). SGLang: Efficient execution of structured language model programs. <i>Advances in Neural Information Processing Systems 37 (NeurIPS 2024)</i>. https://doi.org/10.52202/079017-2000. arXiv:2312.07104. Stanford University; University of California, Berkeley; Shanghai Jiao Tong University; Texas A&amp;M University; independent researcher."),
 ("actionengine", "Zhong et al., 2026",
  "Zhong, H., Faisal, F., França, L., Leesatapornwongsa, T., Szekeres, A., Rong, K., &amp; Nath, S. (2026). ActionEngine: From reactive to programmatic GUI agents via state machine memory. arXiv:2602.20502v1. Georgia Institute of Technology; Microsoft Research."),
 ("guig1", "Zhou et al., 2025",
  "Zhou, Y., Dai, S., Wang, S., Zhou, K., Jia, Q., &amp; Xu, J. (2025). GUI-G1: Understanding R1-Zero-like training for visual grounding in GUI agents. <i>Advances in Neural Information Processing Systems 38 (NeurIPS 2025)</i>. https://doi.org/10.52202/085713-3201. arXiv:2505.15810. Renmin University of China; Huawei Noah’s Ark Lab."),
 ("tracelab", "Zhu et al., 2026",
  "Zhu, K., Jacob, M., Ma, C., Pan, Y., Wang, S., Krishnamurthy, A., &amp; Kasikci, B. (2026). TraceLab: Characterizing coding agent workloads for LLM serving. arXiv:2606.30560v2. University of Washington; Wuhan University of Technology; Shanghai Jiao Tong University. Dashboard: https://tracelab.cs.washington.edu (read 28 September 2026)."),
]
CITE2 = {k: c for k, c, _ in REFS_P2}   # in-text form, with a/b/c where two works share one within Part 2
P2_REFS_PER_PAGE = 19
P2_REF_PAGES = -(-len(REFS_P2) // P2_REFS_PER_PAGE)

def c2(*keys):
    return "(" + "; ".join(CITE2[k] for k in keys) + ")"

def wk(name, *keys):
    """First cell of a Part 2 table: the work's name, with its citation underneath."""
    return f'<b>{name}</b><div class="wcite">{c2(*keys)}</div>'

# The Part 1 formulas as rows of terms; a page marks the term its family of work changes.
FX = {
 "time":   [("op", r"T_{\mathrm{attempt}}\approx"), ("N", r"\sum_{i=0}^{N}"), ("op", r"["), ("J", r"\sum_{j=1}^{J_i}"), ("op", r"("),
            ("queue", r"t^{\mathrm{queue}}_{ij}"), ("op", "+"), ("prefill", r"t^{\mathrm{prefill}}_{ij}"), ("op", "+"),
            ("nout", r"n^{\mathrm{out}}_{ij}"), ("tpot", r"\mathrm{TPOT}_{ij}"), ("op", r")+"), ("E", r"E_i"), ("op", r"]-"),
            ("save", r"T_{\mathrm{saving}}")],
 "money":  [("op", r"v(m,p)=\mathbb{E}["), ("N", r"\sum_{i}"), ("J", r"\sum_{j}"), ("op", r"\sum_{\kappa}"), ("n", r"n^{\kappa}_{ij}"),
            ("c", r"c_{\kappa}(\mu_{ij})"), ("op", "+"), ("env", r"x_{\mathrm{env}}\,c_{\mathrm{env}}"), ("op", r"]\ \div"), ("R", r"R_m(p)")],
 "prompt": [("op", r"\sum_{i=1}^{N}|H_{a,i}|="), ("H1", r"N\,|H_{a,1}|"), ("op", "+"), ("N2", r"\frac{N(N-1)}{2}"), ("g", r"\bar{g}")],
}
DN, UPG, ZERO = ("good", "↓"), ("good", "↑"), ("good", "→ 0")      # the change the family is after
UP, DNB, KEEP = ("bad", "↑"), ("bad", "↓"), ("keep", "=")           # what grows or falls in exchange; what stays

def fx(*rows, legend=True):
    """rows: (which, {term: mark}) — Part 1's formulas with the targeted term filled, a cost in orange, an unchanged term dashed."""
    out = ['<div class="fxbox">']
    for which, marks in rows:
        parts = [f'<span class="lk">{which}</span>']
        for k, src in FX[which]:
            if k == "op" or k not in marks:
                parts.append(tex(src, 13))
                continue
            cls, arrow = marks[k]
            col = "#ffffff" if cls == "good" else ("#b3600c" if cls == "bad" else "#1b2733")
            parts.append(f'<span class="fp {cls}">{tex(src, 13, color=col)}<i>{arrow}</i></span>')
        out.append('<div class="fxrow">' + " ".join(parts) + '</div>')
    if legend:
        out.append('<div class="fxleg"><span class="fp good">targeted</span> <span class="fp bad">in exchange</span> <span class="fp keep">unchanged</span></div>')
    return "".join(out) + "</div>"

def ptab(rows, widths=("17%", "24%", "37%", "22%"), headers=("work", "what it changes", "measured effect, and its conditions", "what grows, or is left out")):
    return table(list(headers), rows, list(widths), cls="tbl p2")

# --- Part 2 · 01 title --------------------------------------------------------------
P2_REF_SPAN = "15" if P2_REF_PAGES == 1 else f"15–{14 + P2_REF_PAGES}"
slide("t01", "Acceleration, term by term", cover=True, part=2,
      body=f"""
<div class="cover">
  <div class="cover-l">
    <div class="cover-kicker">Part 2</div>
    <h1 class="cover-title">Acceleration, term by term</h1>
    <p class="cover-sub">What published work has done to each term of the Part 1 formulas, and what each change costs elsewhere.</p>
    <p class="cover-sub2">We classify; we do not propose methods. Each work sits on the term it changes, next to the terms that grow in exchange and one measured effect with its conditions. Every number was re-read in its source on 28 September 2026; calc. marks our arithmetic, vendor a vendor’s own statement. Full references at the end of the part.</p>
  </div>
  <div class="cover-r">
    <div class="toc-t">In this part</div>
    <ol class="toc">
    <li><span>02</span>The map: which term each family of work changes</li>
    <li><span>03–04</span>Fewer model calls, fewer steps</li>
    <li><span>05–07</span>A faster call: queueing, prefill, decoding</li>
    <li><span>08</span>Less time outside the model</li>
    <li><span>09–10</span>Overlap: parallel calls, and speculation with its safety</li>
    <li><span>11–13</span>The growing prompt, the bill by class, a cheaper model per call</li>
    <li><span>14</span>Success and cost per success, set-up included</li>
    <li><span>{P2_REF_SPAN}</span>References · Appendix B0–B10</li>
    </ol>
  </div>
</div>""")

# --- Part 2 · 02 the map ----------------------------------------------------------------
slide("t02", "The map: each family of work targets one term or a pair, and most grow another", part=2,
      crumb="from Part 1’s formulas → here: which term each family of work changes → to: one page per term",
      callout=f"""<p><b>Each work sits on the term it changes: it shrinks a term, removes a structure, or adds overlap {tex(r"T_{\mathrm{saving}}", 15)}; most also grow another term.</b> Speed-up = baseline time ÷ new time on the same tasks; each row says what was timed.</p>""",
      body=f"""
{fx(("time", {}), ("money", {}), legend=False)}
{table(["term (Part 1)", "what the work does to it", "family of work", "page"], [
  [tex("J_i", 12), "→ 0 on steps run as code or replayed from a recording", "compile or replay the loop", "03"],
  [tex("N", 12), "fewer steps: more work per call, reusable skills", "bigger actions, skills", "04"],
  [tex(r"t^{\mathrm{queue}},\ t^{\mathrm{prefill}}", 12), "shorter on self-hosted serving: whole programs scheduled, cache kept across tool waits", "agent-aware serving", "05"],
  [tex(r"|o_{a,i}|\rightarrow t^{\mathrm{prefill}}", 12), "less of each page shown to the model", "observation reduction", "06"],
  [tex(r"n^{\mathrm{out}},\ \mathrm{TPOT}", 12), "less thinking; faster decoding, at a price", "decoding", "07"],
  [tex("E_i", 12), "fewer or cheaper environment actions", "environment", "08"],
  [tex(r"T_{\mathrm{saving}}", 12), "added: independent calls run at once, or the next step guessed and run early", "parallel calls; speculation", "09–10"],
  [tex(r"\bar{g},\ N^2", 12), "a flatter slope; or the square removed", "context management", "11"],
  [tex(r"n^{\kappa}", 12), "input moved from uncached to cache hit", "caching", "12"],
  [tex(r"c_{\kappa}(\mu_{ij})", 12), "a cheaper model or tier for most calls", "routing, small models, tiers", "13"],
  [tex("R_m(p)", 12) + ", set-up", "higher success; a one-time set-up spread over the tasks", "cost per success", "14"],
 ], ["20%", "47%", "25%", "8%"], cls="tbl p2 map")}""",
      foot="SOURCES · Part 1’s formulas (pages 2–4, Appendix A0); the time row as on Part 1 page 13: TTFT shown as t^queue + t^prefill (network and first-token time left out), i = 0 holds calls outside any step · held-back works: Appendix B9",
      chip=("#b9-1", "Appendix B9"))

# --- Part 2 · 03 compile or replay ----------------------------------------------------------
slide("t03", "Compiling or replaying the loop removes most model calls; where the actions still run, time falls less", part=2,
      crumb="term: J_i → 0 on steps run as code or replayed · E_i unchanged on replay; JIT-Planner’s cached site tools also shorten it · a set-up cost sits outside the formula (page 14)",
      callout=f"""<p><b>Code or a recorded trajectory takes the model out of most steps, so {tex("D_i", 15)} → 0 there; the actions in {tex("E_i", 15)} still run unless the code replaces them too.</b> Against Synapse, a planning agent, replay cut median tokens by 96.5% but median time by 59.6% (calc., EchoPath).</p>""",
      body=f"""
{fx(("time", {"J": ZERO}))}
{ptab([
  [wk("JIT-Planner", "jit"), "Parallel calls draft code plans over cached, checked site tools; the cheapest valid one runs", "Task time 150.1 → 15.4 s (9.7×), success 61 → 90% — 37 tasks on 5 web apps (18 author-written), 3 runs, GPT-4.1, vs Browser-Use, same model", "Set-up of 25–90 + 25–45 min per app, excluded"],
  [wk("ActionEngine", "actionengine"), "An offline state graph; one call writes a program, graph search compiles it", "Model calls 10.2 → 1.8, task time 237 → 118 s, success 66 → 95% — 106 WebArena Reddit tasks", "Baseline: another agent and model; crawl cost unreported"],
  [wk("AutoDroid-V2", "autodroid2"), "A local model writes one script per task, not one call per step", "Model time 669.2 → 46.3 s per task (screen actions excluded), success 43.9 → 54.4% — 158 DroidTask tasks, same 8B model", "$82.42 of GPT-4o calls per app, offline (calc.)"],
  [wk("EchoPath", "echopath"), "Validated trajectories kept as callable memories and replayed", "Median tokens 586,386 → 20,370, median time 315.7 → 127.5 s, success 91.8 → 91.2% — OSWorld-Verified, 159 replayable tasks, Codex GPT-5.5, vs Synapse", "First pass ≈ 572k tokens and ≈ 4.5 min per task, not counted"],
 ])}
<div class="figcap">Vendor tools replay recorded steps and call a model only to repair a failure; none publishes a repair rate with a defined sample (B1).</div>""",
      foot="NOT YET MEASURED · replay under live application change (EchoPath’s only change: a new screen resolution) · cost per success with set-up included · SOURCES · as cited in each row; full conditions in Appendix B1",
      chip=("#b1-1", "Appendix B1"))

# --- Part 2 · 04 fewer steps -------------------------------------------------------------
slide("t04", "Fewer steps: more work per call cut steps by 38⁠–⁠46%; skills cut fewer and cost prompt tokens", part=2,
      crumb="term: N ↓ · actions per step grow with batching, fall with API calls (page 8) · skills add module calls (J_i ↑) and lengthen the prompt |H_{a,i}|",
      callout=f"""<p><b>One call that issues an API call or a batch of actions cut {tex("N", 15)} by 38–46% (calc.); the actions still run, and only AXIS timed the task.</b> Skills cut 11–21% of steps (calc.) and raise success; a plain agent given 15 steps instead of 10 used 31% fewer tokens (calc.) and did better.</p>""",
      body=f"""
{fx(("time", {"N": DN, "J": UP, "prefill": UP}))}
{ptab([
  [wk("AXIS", "axis"), "Application API calls instead of UI sequences", "Steps 3.2 → 2.0, task time 59.5 → 29.9 s, success 52 → 84% — 50 Word tasks, GPT-4o, vs the UFO agent", "One application; the API must exist"],
  [wk("OSWorld 2.0, batched", "osw2"), "One call emits several actions", "Steps 190.5 → 103, success 18.5 → 20.6%, ~$76.1 → ~$72.4 per task — 108 tasks, Claude Opus 4.8, one run", "Tool calls 190.5 → 481.8; no wall-clock"],
  [wk("ASI", "asi"), "Verified Python skills induced from the agent’s own successes", "Steps 5.6 → 5.0 (−10.7%, calc.), success 32.7 → 40.4% — 812 WebArena tasks, Claude 3.5 Sonnet", "Induction calls not counted; no time or $"],
  [wk("WALT", "walt"), "Site tools learned by exploration", "Steps 8.9 → 7.0, success 57.5 → 64.1% — 234 VisualWebArena tasks, GPT-5 planner, GPT-5-mini executor", "Exploration cost not quantified"],
  [wk("Plain agent, 15 steps", "hajimiri"), "No skill or memory module; a pruned page tree", "Plain 44.78% at 73.6K tokens per task vs ASI 41.02% at 107.3K — 655 WebArena tasks (calc.), Gemini 3 Flash, 3 runs", "Skills add tokens and calls"],
 ])}
<div class="figcap">Headroom: grouping actions by screenshot needs 1.35× (Chrome) to 2.93× (Calc) fewer steps in human reference runs (calc.) {c2('osh')}.</div>""",
      foot="NOT YET MEASURED · task time for batched actions (OSWorld 2.0 pauses 3 s after each action; whether after each batched call is not stated) · SOURCES · as cited; 38–46% and 11–21% are calc. from the rows; more rows and stopping rules in Appendix B2",
      chip=("#b2-1", "Appendix B2"))

# --- Part 2 · 05 serving --------------------------------------------------------------
slide("t05", "Serving the agent as one program cuts queueing and re-reading, on self-hosted models only", part=2,
      crumb="terms: t^queue and t^prefill ↓ under load · self-hosted serving only; an API user cannot apply these",
      callout=f"""<p><b>Schedulers that treat a whole agent run as the unit, and keep its cache through tool waits, give 1.1–15× better delay or throughput than vLLM-based baselines.</b> All are measured under load on self-hosted models; none reports task success.</p>""",
      body=f"""
{fx(("time", {"queue": DN, "prefill": DN}))}
{ptab([
  [wk("Agentix", "agentix"), "Program-level preemptive scheduling; cache-aware routing", "Program throughput up to 15× vLLM and 2–5× vLLM with prefix caching, at equal latency — Llama-3.1 8B/70B and Falcon-180B on A100s", "No task quality: scheduling only"],
  [wk("Continuum", "continuum"), "Keeps a run’s KV cache for a predicted tool-wait time", "Job delay 1.12–3.66× lower — replayed SWE-bench, BFCL and OpenHands traces; Llama-3.1 8B/70B, Gemma-3 12B", "GPU memory held during waits; replay, no quality metric"],
  [wk("InferCept", "infercept"), "During a tool call, keeps, swaps or recomputes the cache, whichever wastes least", "1.6–2× the load of vLLM at similar per-token latency (1.25× for 13B on one GPU) — six tool-augmented workloads", "Baseline spent 37–40% of forward time recomputing"],
  [wk("ThunderAgent", "thunder"), "The program and its tool sandboxes are the scheduling unit", "Steps per minute 1.24–3.58× vLLM (calc. from its figure) — GLM-4.6 and Qwen-3 on 8×H100", "Throughput, not task time"],
 ])}""",
      foot="NOT YET MEASURED · the queueing share of task time for API agents; API priority tiers publish targets, not measured latency (page 13) · SOURCES · as cited in each row; more systems in Appendix B3",
      chip=("#b3-1", "Appendix B3"))

# --- Part 2 · 06 prefill: observation reduction -----------------------------------------------
slide("t06", "Showing the model less of the page cuts prefill; a reader call can cost more time than it saves", part=2,
      crumb="term: |o_{a,i}| ↓ → the actor’s t^prefill and n^unc ↓ · J_i + 1 when a model does the reducing; that reader reads the full page · success can fall",
      callout=f"""<p><b>Pruning the page before the model reads it shortens the actor’s prompt at that step, and later prompts only where old pages stay in the history; a separate reader call adds a model call per step.</b> A pruning program without a model halved step time and kept 84% of the successes.</p>""",
      body=f"""
{fx(("time", {"prefill": DN, "J": UP}))}
{ptab([
  [wk("FocusAgent", "focusagent"), "A small model picks the relevant page-tree lines for the actor", "Input cost −19%, success 53.6 → 51.5% — 330 WorkArena L1 episodes; model time per step 2.5 → 10.1 s on 33 tasks, one seed — GPT-4.1 actor, GPT-4.1-mini reader", "One reader call per step; the time excludes the browser"],
  [wk("Evolved pruning program", "enomoto"), "An offline-evolved program keeps ~20% of the HTML; no model at run time", "Step time 65.7 → 30.2 s (2.2×), 84% of successes kept — 33 WorkArena L1 tasks, Qwen3.5-122B, 2 runs", "Success falls; timed per step"],
  [wk("Aguvis", "aguvis"), "A screenshot instead of HTML, read by a self-hosted 72B model", "Input tokens per step 1,196 vs ~4,000 (−70%), success 22.1 → 27.1% — 104 Mind2Web-Live tasks, vs GPT-4o on HTML", "The model changes too"],
  [wk("AgentOccam (counter)", "agentoccam"), "Simplified page and pruned history, aimed at accuracy", "Success 16.5 → 43.1%, observation tokens per step +33%, steps +45% (calc.) — 812 WebArena tasks, GPT-4-Turbo", "Prefill grows"],
 ])}""",
      foot="NOT YET MEASURED · task time with provider caching on · how pruning interacts with prefix caching in GUI agents · SOURCES · as cited in each row; more rows in Appendix B4",
      chip=("#b4-1", "Appendix B4"))

# --- Part 2 · 07 decoding -----------------------------------------------------------------
slide("t07", "Less thinking and faster decoding shorten the writing; neither touches the environment", part=2,
      crumb="terms: n^out ↓ (thinking included) · TPOT ↓ at a higher price per token",
      callout=f"""<p><b>Choosing the reasoning effort per step cut reasoning tokens by 45% at equal success; fast tiers are stated by their vendors to be up to 2.5× faster for twice the price.</b> Both shorten {tex("D_i", 15)} only.</p>""",
      body=f"""
{fx(("time", {"nout": DN, "tpot": DN, "J": UP}), ("money", {"c": UP}))}
{ptab([
  [wk("ARES", "ares"), "A 1.7B router picks the reasoning effort for each step", "Reasoning tokens per task 21,424 → 11,723 (−45%), success 45.0 → 46.5%; low effort throughout −7.6 points (calc.) — WebArena, ~129 tasks (calc.; count not printed, B9), gpt-oss-20b", "A router call per step, cost not reported; no wall-clock"],
  [wk("Overthinking", "overthinking"), "Two low-effort runs; keep the one that overthinks least", "$1,400 → $800 for the whole run, solved 29.1 → 27.3% — SWE-bench Verified (count not printed, B9), o1", "Two attempts per task"],
  [wk("GUI-G1", "guig1"), "RL-trained grounding without a thinking section", "Output tokens 107–114 → 37–39 per example, ScreenSpot 87.5 → 90.3% — InfiGUI-R1-3B (accuracy from its own paper) vs GUI-G1-3B, two differently trained models", "Grounding only; no timing"],
  [wk("ToolSpec", "toolspec"), "Schema-aware drafts of tool-call tokens, verified losslessly", "Tool-call generation 3.5–4.2× faster — API-Bank, ToolAlpaca, BFCLv2; batch 1; 3–14B open models", "Decoding speed, not task time"],
  [wk("Fast tiers (vendor)", "anth-b", "openai"), "The same model, served faster", "Anthropic: up to 2.5× output tokens per second; the gain is in output speed, not first-token time. OpenAI: up to 2.5× faster, ‘speed’ undefined", "Price 2×; switching speed invalidates Anthropic’s message cache"],
 ])}""",
      foot="NOT YET MEASURED · independent task-level timing of fast tiers · the net effect of per-step effort changes, which invalidate Anthropic’s message cache · SOURCES · as cited; more rows in Appendix B4 (2/2)",
      chip=("#b4-2", "Appendix B4"))

# --- Part 2 · 08 environment -----------------------------------------------------------------
slide("t08", "Time outside the model: in one browser-agent study it exceeded model time, and few works shrink it", part=2,
      crumb="term: E_i ↓ — fewer environment actions, cached tool results · x_env priced by the hour",
      callout=f"""<p><b>On 151 WebVoyager tasks run by three GPT-4o agents on live sites, the median step spent 6.6 s in the browser and 4.7 s in the model (medians, not additive) {c2('skim')}; Browser-Use on five web apps spent 73% of its time in model calls {c2('jit')}.</b> The works that shrink {tex("E_i", 15)} skip the browser or cache tool results; batching actions moves the other way.</p>""",
      body=f"""
{fx(("time", {"E": DN}))}
{ptab([
  [wk("Skim", "skim"), "Fetches a synthesized URL over HTTP instead of driving the browser; a verifier falls back to the agent", "Median cost 1.9× lower, latency −33.4%, accuracy kept — WebVoyager and WebShop, “300+” tasks (count not stated; condition (iii) pending, B9), GPT-4o agents", "Read-only tasks; site profiling not counted"],
  [wk("ToolCaching", "toolcaching"), "Caches tool results, with learned admission", "Latency 16.2 → 10.7 s vs no cache at a 0.514 hit ratio — 500 Movie Recommendation queries, LLMCompiler, DeepSeek V3", "Accuracy not reported"],
  [wk("AXIS", "axis"), "API calls replace clicks", "UI actions 103 → 48 over 50 Word tasks", "The API must exist"],
  [wk("OSWorld 2.0 (counter)", "osw2"), "More actions per call", "Tool calls ×2.5 (calc.); a 3-s pause follows each action, whether after each batched call is not stated; no wall-clock", "N falls, actions per step grow"],
 ])}
<div class="figcap">Billed environment usage {tex(r"x_{\mathrm{env}}c_{\mathrm{env}}", 11)}: a cloud browser costs $0.10–0.12 per hour above the plan allowance (vendor price) {c2('browserbase')}.</div>""",
      foot="NOT YET MEASURED · page-load and wait time in write-heavy web workflows · wall-clock of batched actions · SOURCES · as cited in each row; details in Appendix B5 (Skim, sandboxes) and B2 (batched actions)",
      chip=("#b5-1", "Appendix B5"))

# --- Part 2 · 09 overlap: parallel and asynchronous ---------------------------------------------
slide("t09", "Overlap (1): running independent calls and tools together saved 31⁠–⁠73% of task time; one workload got slower", part=2,
      crumb="term: T_saving raised where it is small today · calls and tokens fall with fewer turns (LLMCompiler, W&D) or rise with more workers (ParaGUI)",
      callout=f"""<p><b>Running independent calls or tools together creates {tex(r"T_{\mathrm{saving}}", 15)}; the longest dependent chain sets the limit.</b> Speed-up ≤ {tex(r"(T_{\mathrm{LLM}}+T_{\mathrm{tool}})/\max(T_{\mathrm{LLM}},T_{\mathrm{cp}})", 15)}: decoding, tool and critical-path tool time {c2('asyncfc')}; at most 2× when every tool call waits for the one before ({tex(r"T_{\mathrm{cp}}=T_{\mathrm{tool}}", 15)}; calc.).</p>""",
      body=f"""
{fx(("time", {"save": UPG, "J": ("bad", "↑ or ↓")}))}
{ptab([
  [wk("LLMCompiler", "llmc"), "A planner builds a dependency graph; independent calls run at once", "Task time 20.47 → 5.47 s (3.74×), accuracy 72.47 → 77.13%, input tokens 20,000 → 2,800 — 500 Movie Recommendation questions, gpt-3.5-turbo", "WebShop got slower: 5.98 → 10.48 s"],
  [wk("W&amp;D", "wd"), "Three or more tool calls per turn", "Time per task 1,522.6 → 904.2 s (−40.6%), $102.5 → $65.7 per 100 tasks, 66 → 68% — first 100 BrowseComp tasks, GPT-5, one run", "Call counts forced; $ include search"],
  [wk("AsyncFC", "asyncfc"), "Tool calls return futures; the model keeps decoding until it needs a result", "1.44× vs the plain agent (1.21× with parallel calls alone), resolved 47.6 → 44.3% — 300 SWE-bench Lite tasks, GPT-5.2, tool latency doubled", "Resolution −3.3 points"],
  [wk("ParaGUI", "paragui"), "A planner sends sub-tasks to up to 5 GUI workers on separate desktops", "Critical-path steps 38.7 vs 75.9, success 46.4 vs 33.5%, vs Claude Sonnet 4.6 — 233 tasks; vs its own worker model 38.7 vs 36.7", "Desktops × workers; no wall-clock"],
 ])}""",
      foot="NOT YET MEASURED · wall-clock of parallel GUI workers · overlap of actions that write · SOURCES · as cited; 31–73% is calc. from the rows; the bound is AsyncFC’s Eq. 1 (its R, renamed to avoid R_m(p)) — Appendix B0",
      chip=("#b0-1", "Appendix B0"))

# --- Part 2 · 10 overlap: speculation, and safety ----------------------------------------------
slide("t10", "Overlap (2): guessing the next step saved 5⁠–⁠45% of task time, always paid in extra calls", part=2,
      crumb="term: T_saving added by guessing · calls, tokens and GPU hours grow · safe only for effects that can wait for a commit",
      callout="""<p><b>A guesser (a cheaper model or setting, or the model itself) runs the predicted next action early: a right guess hides a wait, a wrong one is discarded but paid for.</b> Steps with side effects need the rule on the right.</p>""",
      body=f"""
{fx(("time", {"save": UPG, "J": UP}), ("money", {"J": UP, "n": UP}))}
<div class="twocol">
{ptab([
  [wk("Speculative Actions", "specactions"), "Time −19.5%, guesses 54.7% right — chess, 5 × 30 steps, GPT-5 high effort guessed by GPT-5 low", "Guess calls; ≤ 50% saving in its model"],
  [wk("ISP", "isp"), "Total time 182.70 → 105.42 s (−42.3%), $0.2160 → $0.2973 per plan — 117 OpenAGI tasks, GPT-4-turbo", "Baseline spread 2.3× its mean"],
  [wk("SMC", "smc"), "τ² Telecom, 2,285 tasks (calc.): 27.60 → 22.47 s (−18.6%), outcomes unchanged; AppWorld: 355.7 → 195.9 s (−44.9%; −40.4% already from one-step guessing), −2 of 168 — Qwen3.5-27B, 4B drafter", "3 GPUs instead of 1"],
  [wk("SPORK", "spork"), "p50 task time 34.7 → 31.2 s (−10%), p95 131.9 → 108.1 s (−18%), exact match within 1 point — 165 GAIA tasks, Qwen3-32B, baseline already speculative-decoding", "Probe calls, wasted tool runs"],
  [wk("Ghost Tool Calls", "ghost"), "Naive speculation: p50 −5.4%, p99 11.56 → 14.22 s; tool calls seen by the provider 4.03 vs 1.03 per task — 30 author-built tasks × 3 seeds", "Abandoned calls reveal intent"],
 ], widths=("20%", "57%", "23%"), headers=("work", "measured effect, and its conditions", "paid in"))}
{card("WHEN THE STEP HAS SIDE EFFECTS", "Hold irreversible effects until commit; compensating them afterwards leaks",
      [f"Held until commit: 0 of 500 aborted sends leaked; compensation 400, checkpoint-and-replay 200, mislabelled effects 300 — one author-built workflow, 5 abort causes × 100 {c2('atomix')}",
       f"Resuming from a checkpoint repeated or skipped an effect in 90 and 93 of 96 author-built workflows; a case study paid an invoice twice {c2('saferesume')}",
       f"Only ~37% of actions flagged destructive in advance were {c2('weboperator')}"])}
</div>""",
      foot="NOT YET MEASURED · speculation on a live web GUI with side effects held until commit · cost per success of any speculation method · SOURCES · as cited; 5–45% is calc. from the rows; author-built suites flagged in B9; formulas and more works in B0, B5",
      chip=("#b5-1", "Appendix B5"))

# --- Part 2 · 11 the growing prompt -------------------------------------------------------------
slide("t11", "The growing prompt: masking old observations halved the bill; only compiled plans are shown to remove the square", part=2,
      crumb="terms: ḡ ↓ (mask, trim, evict) or the N² structure removed (a plan instead of the history) · edits to old context turn some cache hits into misses or cache writes",
      callout=f"""<p><b>Placeholders remove each old observation once it is 10 turns old: a smaller effective {tex(r"\bar{g}", 15)}, a flatter slope of the {tex("N^2", 15)} term but the same shape.</b> A compiled plan removes the square: the prompt holds the plan, not the history.</p>""",
      body=f"""
{fx(("prompt", {"g": DN, "N2": ("good", "removed by a plan")}), ("money", {"n": ("bad", "hit → miss, write")}))}
{ptab([
  [wk("Observation masking", "masking"), "Observations older than 10 turns become a placeholder", "Cost per task $1.29 → $0.61, solved 53.4 → 54.8% — 500 SWE-bench Verified tasks, Qwen3-Coder-480B; cost = tokens × list price", "Model summaries instead lengthened runs by ~15%"],
  [wk("AgentDiet", "agentdiet"), "A cheaper model deletes useless or expired content two steps back", "Input tokens −39.9 to −59.7%, cost −21.1 to −35.9% with the reducer, success −1 to +2 points — 200 SWE-bench Verified + 300 Multi-SWE-bench Flash tasks, Claude 4 Sonnet, Gemini 2.5 Pro, one run", "A reducer call per step"],
  [wk("TokenPilot eviction", "tokenpilot"), "Evicts stale segments every 3 turns", "Cost $4.22 → $2.79 while cache-hit tokens fell 26.7M → 8.6M — PinchBench continuous sessions, GPT-5.4-mini", "Fewer tokens, fewer of them cached"],
  [wk("A plan, not the history", "actionengine", "llmc"), "The prompt carries a compiled plan instead of every observation", "Input tokens per task 62.3k → 8.1k (ActionEngine); 20,000 → 2,800 (LLMCompiler)", "Only on compiled steps"],
 ])}""",
      foot="NOT YET MEASURED · the N² token volume and the cache hit rate together, in a GUI agent · SOURCES · as cited in each row; more rows in Appendix B4",
      chip=("#b4-1", "Appendix B4"))

# --- Part 2 · 12 the bill by class ------------------------------------------------------------
slide("t12", "The bill by class: caching a stable prefix cut agent bills by 41⁠–⁠80% against no caching; with trimming and eviction, by up to 87%", part=2,
      crumb="term: n^unc → n^hit (input read from the cache) · cache writes n^w grow · the price c_κ(μ) unchanged",
      callout=f"""<p><b>A cache hit costs 2–25% of an uncached input token (by vendor), so moving input into the hit class cuts that input’s price by 75–98% (calc.) without changing the model.</b> A change of speed, of tools or of old context turns hits back into writes and misses.</p>""",
      body=f"""
{fx(("money", {"n": ("good", "unc → hit"), "c": KEEP}))}
{ptab([
  [wk("Don’t Break the Cache", "dbtc"), "Measures caching the stable prefix and leaving tool results out", "Cost −41 to −80%, first-token time −6 to −31% vs a forced no-cache baseline — a web-search research agent on DeepResearch Bench, 40 sessions per condition, 4 models, a 10K-token system prompt", "Caching the whole context made GPT-4o’s first token 8.8% slower"],
  [wk("TokenPilot", "tokenpilot"), "Stable placeholders for changing fields, trimming, eviction", "Cost $8.31 → $3.22 (123 PinchBench tasks, one per session), $81.52 → $10.58 (Claw-Eval, continuous); hit rate 38.7 → 79.2% — GPT-5.4-mini", "Score change −2.6 to +2.1 points"],
  [wk("TraceLab counterfactual", "tracelab"), "Keeps the cache alive through the user’s think time", "At most −12.8% of the priced cost (paper; 15.8% on the live dashboard) — coding-agent traces", "An estimate, not a measurement"],
 ])}
{table(["latest model (vendor price pages, read 28 Sep 2026)", "cache hit ÷ uncached input", "cache write"], [
  ["DeepSeek-V4.1-Flash", "0.02×", "not listed"],
  ["Claude Opus 5.5", "0.05×", "1.25× (5 min), 2× (1 h)"],
  ["GPT-6 Sol, GPT-6 Luna", "0.1×", "1.25×"],
  ["Gemini 3.8 Flash", "0.1×", "storage $0.50 per million tokens per hour"],
  ["Grok 4.7", "0.25×", "not listed"],
 ], ["44%", "22%", "34%"], cls="tbl p2 price")}""",
      foot=f"NOT YET MEASURED · a GUI or browser agent’s tokens split by billing class, cache writes included (Don’t Break the Cache covers a web-search agent) · SOURCES · as cited; prices {c2('deepseek', 'anth-b', 'openai', 'google', 'xai')}; Appendix B6",
      chip=("#b6-1", "Appendix B6"))

# --- Part 2 · 13 a cheaper model per call -----------------------------------------------------------
slide("t13", "A cheaper model for most calls cut dollars per task by 50⁠–⁠97%, usually for a few points of success", part=2,
      crumb="term: c_κ(μ_ij) ↓ — a smaller model or cheaper tier for most calls · N and J_i can grow · R_m(p) often falls",
      callout=f"""<p><b>Sending most steps to a small model, and only hard ones to a large one, cut dollars per task by 50–97% (calc.), usually for 1–4 points of success and sometimes with more steps.</b> Tiers trade the price per token against queueing and speed.</p>""",
      body=f"""
{fx(("money", {"c": DN, "N": UP, "R": DNB}))}
{ptab([
  [wk("StepWise", "stepwise"), "An 8B model by default; the large model when the small one is stuck", "$0.881 → $0.224 per task (−74.6%), success 58.1 → 55.4%, time per request 6.4 → 4.1 s — OSWorld (count not printed, B9), EvoCUA-8B + Claude Sonnet 4.5 vs Sonnet 4.5 alone", "Steps 25.4 → 26.2"],
  [wk("WebRouter", "webrouter"), "A router picks one of three models for each step", "$0.98 → $0.12 per task, accuracy 86.1 → 82.3%, ~14% slower — 5 WebVoyager sites, ≥ 46 tasks each, vs GPT-4o", "Steps 7.63 → 8.38"],
  [wk("Fara-7B", "fara"), "A 7B screenshot agent instead of a frontier computer-use model", "$0.913 → $0.025 per task, success 70.9 → 73.5% — WebVoyager (count not printed, B9), 3 runs; but Online-Mind2Web 42.9 → 34.1%", "7B priced at $0.20 per million tokens, no caching"],
  [wk("Agentic plan caching", "apc"), "Cached plan templates, adapted by a small model", "Cost −50.31% on average, at 96.61% of the best accuracy — 5 workloads; latency −27.28% on one FinanceBench run", "3.99 s to build each cache entry"],
 ])}
<div class="figcap">Tier prices (vendor, read 28 Sep 2026): OpenAI Flex and Batch 0.5×, Fast 2×; Google Priority 1.8× (Preview); Microsoft Foundry priority 1.75–2.5× (calc.) {c2('openai', 'google', 'microsoft')}.</div>""",
      foot="NOT YET MEASURED · the router’s own cost (excluded or not separated) · small-model losses on enterprise forms · routing with cached prices · SOURCES · as cited in each row; Appendix B7",
      chip=("#b7-1", "Appendix B7"))

# --- Part 2 · 14 success and cost per success ----------------------------------------------------------
EQ["amort"] = r"$v_n(m,p)\;=\;\dfrac{C_{\mathrm{setup}}}{n}\;+\;\dfrac{C_m(p)}{R_m(p)}$"
slide("t14", "Cost per success moves with the success rate, and a set-up cost must be spread over the tasks", part=2,
      crumb="terms: R_m(p) in v(m,p) = C_m(p) / R_m(p) · plus a one-time set-up cost that Part 1’s per-attempt formula leaves out",
      callout="""<p><b>A dearer attempt can give a cheaper success: Beyond Browsing’s hybrid agent costs $1.4 per attempt against $1.2 for API calls alone, but $3.60 against $4.11 per success (calc.).</b> Few papers report the ratio, so the figures here are our calculations. Set-up costs are left out of most headlines; SpeedRunner spreads them over its runs, EET prints them apart (B8).</p>""",
      body=f"""
<div class="eqtab">
{eqrow("per task", "set-up spread", ["amort"],
       tex(r"C_{\mathrm{setup}}", 11) + ": one-time cost of building the code, tools or memories; " + tex("n", 11) + ": tasks it serves; the second term is Part 1’s " + tex("v(m,p)", 11) + ", each task retried until it succeeds, so per task = per success. Against a baseline of cost per success " + tex(r"v_{\mathrm{base}}", 11) + " it pays off once " + tex(r"n>C_{\mathrm{setup}}/(v_{\mathrm{base}}-v(m,p))", 11) + ", which needs " + tex(r"v(m,p)<v_{\mathrm{base}}", 11) + " (calc.).",
       "fixed + variable cost: " + CITE2['kapoor25'] + ", §3 (in words); one large tool-making call spread over n cheap calls, O(nc + C) with C, c the cost of one large- and one small-model call: " + CITE2['latm'] + ", Table 2 · per success: " + CITE2['cop'] + ", Eq. 2", "adapted", fs=12.5)}
</div>
<div class="twocol">
{table(["work", "cost per success (calc. unless stated)", "why it moved"], [
  [wk("AXIS", "axis"), "$0.77 → $0.24", "cheaper and more successful"],
  [wk("W&amp;D", "wd"), "$1.55 → $0.97 per correct answer", "cheaper per attempt"],
  [wk("OSWorld 2.0, batched", "osw2"), "$411 → $351", "Opus 4.8; success 18.5 → 20.6%"],
  [wk("Beyond Browsing", "beyondbrowsing"), "browsing ≈ $0.68 · API only ≈ $4.11 · hybrid ≈ $3.60", "dearer attempt, cheaper success (hybrid vs API)"],
  [wk("BATS", "bats"), "$0.79 → $4.47", "success 12.6 → 24.6%, cost ×11"],
  [wk("AI Agents That Matter", "kapoor25"), "93.2% for $2.45 vs 88.0% for $134.50 (run totals, stated)", "simpler agent, better and cheaper"],
 ], ["26%", "44%", "30%"], cls="tbl p2")}
{card("SET-UP COSTS LEFT OUT OF THE HEADLINES", "Each needs n tasks to pay off",
      [f"JIT-Planner: 25–90 min of tool building plus 25–45 min of traces per app {c2('jit')}",
       f"EchoPath: a first pass of ≈ 572k tokens and ≈ 4.5 min per task {c2('echopath')}",
       f"AutoDroid-V2: $82.42 of GPT-4o calls per app (calc.) {c2('autodroid2')}"])}
</div>""",
      foot="NOT YET MEASURED · time, money and success, set-up included, on one web or GUI benchmark · SOURCES · as cited; the calculations with their inputs and rounding are in Appendix B8",
      chip=("#b8-1", "Appendix B8"))

# --- references (part 2) ---------------------------------------------------
for _n in range(P2_REF_PAGES):
    _chunk = [r for _, _, r in REFS_P2][_n * P2_REFS_PER_PAGE:(_n + 1) * P2_REFS_PER_PAGE]
    slide(f"t{15 + _n}", f"References · Part 2 ({_n + 1} of {P2_REF_PAGES})", kind="refs", part=2,
          crumb=("author–year tags on the Part 2 pages refer to these entries · a, b, c separate works whose first authors share a surname and year within Part 2 · published version where one exists, otherwise the arXiv number and the authors’ institutions" if _n == 0 else "continued"),
          body='<div class="refs2">' + refs_html(_chunk, start=_n * P2_REFS_PER_PAGE + 1) + '</div>')

# =====================================================================
# APPENDIX — Part 2
# =====================================================================
def B(id_, label, title, body, crumb=""):
    A(id_, label, title, body, crumb=crumb, part=2)

w_f = ["17%", "33%", "25%", "25%"]
h_f = ["source, location", "the formula in the source’s own symbols", "its symbols", "what it bounds, in Part 1’s terms"]

B("b0-1", "B0 · 1/3", "B0 · Source formulas for overlap: how much concurrency can save",
  crumb="verbatim from each source, in its own symbols; the right-hand column maps them onto Part 1 · behind pages 9–10",
  body=table(h_f, [
   [wk("AsyncFC, §4 Eq. 1 (= App. B Eq. 2)", "asyncfc"), tex(r"R=\dfrac{T_{\mathrm{LLM}}+T_{\mathrm{tool}}}{\max(T_{\mathrm{LLM}},\,T_{\mathrm{cp}})}", 12), tex(r"T_{\mathrm{LLM}}", 10) + " total decoding time; " + tex(r"T_{\mathrm{tool}}", 10) + " total function time; " + tex(r"T_{\mathrm{cp}}", 10) + " function time on the critical path of the dependency graph", "the largest speed-up that " + tex(r"T_{\mathrm{saving}}", 10) + " can give; decoding sits in " + tex("D_i", 10) + ", functions in " + tex("E_i", 10) + "; its R is not the success probability " + tex("R_m(p)", 10) + " (page 9 writes “speed-up”)"],
   [wk("LLMCompiler, App. E.1", "llmc"), tex(r"T^{R}=\sum_{i=1}^{N}(T_P^{R}(P_i)+T_E(E_i))", 11) + "<br>" + tex(r"T^{C}=\sum_{i=1}^{N}T_P^{C}(P_i)+\max_k T_E(E_k)", 11) + "<br>" + tex(r"\gamma=T^R/T^C", 11), "N planned tasks (not our steps); " + tex("P_i", 10) + " planning and " + tex("E_i", 10) + " execution of task i (not our " + tex("E_i", 10) + "); R: ReAct, C: compiled", "serial against parallel execution; " + tex(r"\gamma_{\max}\approx N", 10) + " when execution dominates and all calls take equally long, ≈ 1 when planning dominates"],
   [wk("Speculative tool calls, Eq. 2 and Lemma 1", "nichols"), tex(r"S_{\mathrm{spec}}=\dfrac{G+T}{\alpha\max\{G,g+T\}+(1-\alpha)(G+T)}", 11) + "<br>" + tex(r"S_{\max}=\dfrac{G+T}{\max\{G,g+T\}}<2", 11), "G mean generation time of the main model; g of the speculator; T mean tool time; α acceptance rate", "one model call overlapped with one tool call: under 2× per step, whatever the guesser"],
   [wk("SPORK, EQ1 and App. A", "spork"), tex(r"\mathrm{Ratio}=\dfrac{T_{\mathrm{base}}}{T^{*}_{\mathrm{base}}-\alpha\,t_{\mathrm{overlap}}+T_{\mathrm{oh}}}", 11) + "<br>" + tex(r"S_{\max}=\dfrac{1}{1-f_{\mathrm{tool}}}", 11), tex(r"T_{\mathrm{base}}=T_{\mathrm{dec}}+T_{\mathrm{tool}}", 10) + "; " + tex(r"T^{*}_{\mathrm{base}}=T_{\mathrm{base}}-T_{D3}", 10) + ", less the decoding saved by its third design (D3: a rejected probe’s prefix reused as draft tokens); α accepted share of tool-call turns; " + tex(r"t_{\mathrm{overlap}}", 10) + " overlap per accepted turn; " + tex(r"T_{\mathrm{oh}}", 10) + " probe overhead; " + tex(r"f_{\mathrm{tool}}=T_{\mathrm{tool}}/T_{\mathrm{base}}", 10), "break-even: " + tex(r"\alpha\,t_{\mathrm{overlap}}\geq T_{\mathrm{oh}}", 10) + " (without its third design); the ceiling is Amdahl’s law on the tool share"],
   [wk("ParaGUI, §III-C", "paragui"), tex(r"L_{\mathrm{parallel}}=\sum_{r=1}^{R}\max_{k}s_{r,k}", 11) + "<br>" + tex(r"S=L_{\mathrm{serial}}/L_{\mathrm{parallel}},\ \ P=L_{\mathrm{total}}/L_{\mathrm{parallel}}", 11), tex(r"s_{r,k}", 10) + " GUI steps of worker k in round r; R rounds (not " + tex("R_m(p)", 10) + "); " + tex(r"L_{\mathrm{serial}}", 10) + " steps of a single-agent serial run; " + tex(r"L_{\mathrm{total}}", 10) + " all worker steps", "steps on the critical path against total work: P = 2.13 means 2.13 desktops busy on average — machine hours " + tex(r"x_{\mathrm{env}}", 10) + " for time"],
  ], w_f))

B("b0-2", "B0 · 2/3", "B0 · Source formulas for speculation, cache retention and a reader call",
  crumb="verbatim from each source, in its own symbols · behind pages 5, 6 and 10",
  body=table(h_f, [
   [wk("Speculative Actions, Prop. 1 and Thm 3", "specactions"), tex(r"\dfrac{\mathbb{E}[T_s]}{\mathbb{E}[T_{\mathrm{seq}}]}\rightarrow 1-\dfrac{p(k)}{1+p(k)}\cdot\dfrac{\alpha}{\alpha+\beta}", 11) + "<br>" + tex(r"\dfrac{\mathbb{E}[M_{\mathrm{spec}}-M_{\mathrm{seq}}]}{\mathbb{E}[M_{\mathrm{seq}}]}\rightarrow\tilde{k}-(\tilde{k}+\dfrac{\alpha}{\alpha+\beta})\,\dfrac{p(k)}{1+p(k)}", 11), tex(r"p(k)=1-(1-p)^k", 10) + ", k guesses of accuracy p; speculator and API latencies exponential with rates α, β; " + tex(r"T_s,\ T_{\mathrm{seq}}", 10) + " time with and without speculation; → the limit as the number of steps grows; " + tex(r"\tilde{k}", 10) + " distinct guessed actions; M money", "time saved and money added from the same guess accuracy; in the limit the time ratio stays above 1/2 (calc.), so at most 50% is saved — under its exponential-latency model"],
   [wk("Speculate with memory, §2.1 and §4.3", "swm"), "saving per hit " + tex(r"=\min(\ell_{\mathrm{env}},\ \ell_{\mathrm{LLM}}-\ell_{\mathrm{spec}})", 11) + " (guess the action) or " + tex(r"\min(\ell_{\mathrm{LLM}},\ \ell_{\mathrm{env}}-\ell_{\mathrm{spec}})", 11) + " (guess the observation); extra cost " + tex(r"=k\,C_S+(1-\mathrm{acc})\,C_{\mathrm{act}}", 11), tex(r"\ell", 10) + " latencies of the environment, the model and the speculator; k speculators of cost " + tex("C_S", 10) + "; acc hit rate; " + tex(r"C_{\mathrm{act}}", 10) + " cost of the pre-launched actor call a miss wastes (the extra-cost form holds for observation and chained guesses)", "a hit can hide at most the idle window of the other side; its App. A uses slightly different per-type forms"],
   [wk("Continuum, Eqs. 1–2", "continuum"), tex(r"\tau^{*}=\arg\max_{\tau}\ \mathcal{P}(\tau,f)\,\mathrm{Benefit}(r)-\mathrm{Cost}(\tau,r)", 11), tex(r"\mathcal{P}(\tau,f)", 10) + " empirical probability that tool f returns within τ; Benefit: reload and reordering cost avoided; Cost: memory held for τ", "how long to keep a run’s cache through a tool wait: " + tex(r"t^{\mathrm{queue}}", 10) + " and re-prefill against GPU memory"],
   [wk("InferCept, Eqs. 1–5", "infercept"), tex(r"\mathrm{Waste}_{\mathrm{preserve}}=T_{\mathrm{INT}}\,C_i^j\,M", 11) + "; also discard, swap and chunked discard; " + tex(r"\mathrm{Waste}=\min(\mathrm{Waste}_{\mathrm{preserve}},\mathrm{Waste}_{\mathrm{chunkD}})", 11) + " (Eq. 5)", tex(r"T_{\mathrm{INT}}", 10) + " duration of the tool call; " + tex("C", 10) + " context tokens; " + tex("M", 10) + " memory per token; i request, j interception (not Part 1’s step and call)", "the same trade inside the server: keep the cache during " + tex("E_i", 10) + ", or pay " + tex(r"t^{\mathrm{prefill}}", 10) + " again"],
   [wk("FocusAgent, App. H.1", "focusagent"), tex(r"C_S|o_i|+C_L|o_r|\leq C_L|o_i|\ \Leftrightarrow\ \alpha\leq\dfrac{C_L-C_S}{C_L}", 11), tex("C_S, C_L", 10) + " prices of the small reader and the large actor; " + tex(r"|o_i|,|o_r|", 10) + " observation before and after reduction; " + tex(r"\alpha=|o_r|/|o_i|", 10), "when a reader call pays in money; the paper notes it ignores API latency — the time can still grow (page 6)"],
  ], w_f))

EQ["nichols4"] = r"$T_{\mathrm{vanilla}}=2Ko+\phi\sum_{i=1}^{K}X_i+\delta\sum_i(R_i+t_i)+\sum_i T_i,\quad X_{i+1}=X_i+t_i+t_{o,i}$"
B("b0-3", "B0 · 3/3", "B0 · Source formulas for money and set-up, and one closer source for Part 1",
  crumb="verbatim from each source · behind pages 12 and 14 · the last row is a finding for Part 1’s Appendix A0",
  body=table(h_f, [
   [wk("TokenPilot, App. A.2, Eq. 11", "tokenpilot"), tex(r"\mathrm{Cost}=|C'_{\mathrm{hit}}|\,p_{\mathrm{hit}}+|C'_{\mathrm{miss}}|\,p_{\mathrm{miss}}+H_{\mathrm{out}}\,p_{\mathrm{out}}", 11), tex(r"|C'_{\mathrm{hit}}|,|C'_{\mathrm{miss}}|", 10) + " cached and uncached input tokens; " + tex(r"H_{\mathrm{out}}", 10) + " generated tokens; p prices", "Part 1’s money sum over three classes; no cache-write term"],
   [wk("SpeedRunner, App. A.3", "speedrunner"), tex(r"\mathrm{cost}=p_{\mathrm{in}}N^{\mathrm{uncached}}_{\mathrm{in}}+p_{\mathrm{cache}}N^{\mathrm{cached}}_{\mathrm{in}}+p_{\mathrm{out}}N_{\mathrm{out}}", 11), "N summed over all calls of an episode, the skill-inducer calls amortised over its rollouts", "the same three classes; set-up calls spread over the runs they serve"],
   [wk("LATM, Table 2", "latm"), tex(r"O(nc+C)", 11) + " against " + tex(r"O(nC)", 11), "n samples; C one call to the large tool-making model; c one call to the small tool-using model", "one expensive set-up amortised over n cheap runs — the form of page 14’s " + tex(r"C_{\mathrm{setup}}/n", 10)],
   [wk("AI Agents That Matter, §3", "kapoor25"), "in words: total cost = a fixed cost (one-time optimisation) + a variable cost (per run, from input and output tokens)", "—", "page 14’s " + tex(r"v_n(m,p)", 10) + " adds this fixed cost to Cost-of-Pass’s per-success cost (adapted)"],
   [wk("Speculative tool calls, Eq. 4", "nichols"), eq_svg("nichols4", fontsize=10, cls="eqn"), "K turns; o per-call overhead; ϕ prefill and δ decode seconds per token; " + tex("X_i", 10) + " prompt tokens of turn i; " + tex("R_i, t_i", 10) + " reasoning and tool-call tokens; " + tex(r"t_{o,i}", 10) + " tool output; " + tex("T_i", 10) + " tool time", "a published form of Part 1’s time sum with its growing prompt, found in these checks: per-call overhead, prefill of a prompt that grows each turn, decoding, tool wait. Part 1 does not cite it yet (open question)"],
  ], w_f))

w_d = ["16%", "22%", "40%", "22%"]
h_d = ["work", "mechanism", "measured effect, with its conditions", "left out, or grows"]

B("b1-1", "B1 · 1/2", "B1 · Compile or replay: the research systems, with full conditions",
  crumb="behind page 3 · term J_i → 0 on compiled or replayed steps · calc. = our arithmetic",
  body=table(h_d, [
   [wk("JIT-Planner", "jit"), "Candidate code plans over cached site tools with pre/postcondition checks, drafted by parallel planning calls; a separate scheduler (not in the headline) can hedge by running up to 4 copies of the chosen plan", "Wall-clock from submission to completion, planning included: 150.1 → 15.4 s (9.7×, its Table 1), success 61 → 90%. 37 tasks in 5 apps (18 written by the authors), 3 runs, GPT-4.1; Browser-Use v0.7.10 on the same model. Three-model average 10.4×", "Tool synthesis 25–90 min + traces 25–45 min per app; no tokens or $ reported"],
   [wk("ActionEngine", "actionengine"), "Offline state-machine graph of the site; one sketch-program call compiled by graph search", "106 WebArena Reddit tasks: success 66 → 95%, end-to-end latency 237 → 118 s, model calls 10.2 → 1.8, input tokens 62.3k → 8.1k, $0.71 → $0.06 per task (tokens × list price). AgentOccam on GPT-4-Turbo vs ActionEngine on Claude Sonnet 4.5", "About 2.5× of the 11.8× $ gap is the cheaper model’s price (calc.); crawl cost not reported"],
   [wk("AutoDroid-V2", "autodroid2"), "A local model writes a whole-task script from an offline app document", "Model inference time 669.2 → 46.3 s per task (prompt to last token, screen actions excluded); uncached input 3,021 → 68 tokens; success 43.9 → 54.4%. 158 DroidTask tasks, fine-tuned Llama-3.1-8B on a phone, both sides", "Offline GPT-4o $4.11 + $7.83 + $70.48 = $82.42 per app (calc.), ~2.5 GPU-hours of fine-tuning"],
   [wk("EchoPath", "echopath"), "Validated trajectories kept as executable memories; a gate checks the start state", "Second pass, medians: tokens 586,386 → 20,370 (−96.5%), time 315.7 → 127.5 s (−59.6%), success 91.8 → 91.2% (calc. for the %). OSWorld-Verified, 159 replayable tasks, Codex GPT-5.5, vs Synapse; the second pass changes the resolution", "First pass ≈ 572k tokens, ≈ 4.5 min per task; the gate accepted 22% of incompatible starts (calc.)"],
   [wk("AppAgentX", "appagentx"), "Frequent action sequences evolved into shortcut actions", "AndroidWorld, 116 tasks, GPT-4o: task time 147.17 → 59.74 s, tokens 18.9k → 6.2k, success 41.7 → 62.5%; time compared only on tasks every method completed", "Evolution runs before the test"],
   [wk("AutoTool", "autotool"), "Repeated tool calls issued from a usage graph without a model call, capped at 30% of operations", "Model calls 24.1 → 20.4 (ALFWorld), 23.3 → 17.8 (ScienceWorld); progress rate 0.394 → 0.531 and 0.716 → 0.708 — Llama4-Scout-17B", "No wall-clock; calls used as the proxy"],
   [wk("EAM", "eam"), "Executable memory of sub-tasks for mobile agents", "Per step 9.3 → 2.8 s and 50.8K → 8.3K tokens vs GPT-4o (benchmark not named); AndroidWorld success 34.5 → 52.6%, 3 runs", "Per step, not per task"],
   [wk("AgentReuse", "agentreuse"), "Reuses stored plans for semantically similar requests", "−93.12% latency is computed from an assumed 31.8 s per plan, not measured end to end", "Modelled estimate; not used on the main page"],
  ], w_d))

B("b1-2", "B1 · 2/2", "B1 · Compile or replay in products: replay first, a model only to repair",
  crumb="behind page 3 · vendor documentation and pages, read 28 September 2026 · vendor figures are labelled as such; marketing is not evidence",
  body=table(["product", "what replays, and when a model is called", "published numbers", "what is missing"], [
   [wk("UiPath Healing Agent", "uipath"), "Recorded automation; a model recommends or applies a fix when a step fails", "Price only: one heal = 3 Platform Units; failed heals free; healing is not kept for the next run", "Heal success rate, heal latency"],
   [wk("Power Automate self-healing", "powerautomate"), "Desktop flows repaired with Copilot", "None; free on premium accounts", "Any measured rate"],
   [wk("Automation Anywhere Generative Recorder", "aa-recorder"), "Recorded bot with a generative fallback", "“Nearly 50%” of failures fixed in customer previews: a vendor statement with no sample, period or definition (the product page’s “over 60%” is marketing, not cited)", "A defined, sampled rate"],
   [wk("Stagehand cache", "stagehand"), "An action’s model output is cached; the second run of the same action makes no call", "None usable: the blog’s “as high as ~80%” (one action run twice) is vendor marketing, not cited", "Whole-workflow numbers, sample, model"],
   [wk("Skyvern code cache", "skyvern"), "Generated code re-run without a model", "None (“faster, cheaper”); plans imply about $0.024 per action (calc.)", "Any measured rate"],
   [wk("HyperAgent action cache", "hyperagent"), "Replay by XPath; the model only when the page has changed", "None; the docs concede that a fallback adds latency and cost", "Replay and fallback rates"],
  ], ["18%", "32%", "30%", "20%"]) + """
<div class="apx-note">Across all six: the model call is replaced by replay (<b>J_i → 0</b>) and the environment actions stay (<b>E_i unchanged</b>); no vendor publishes a replay or repair success rate with a defined sample.</div>""")

B("b2-1", "B2 · 1/2", "B2 · Fewer steps: more rows, with full conditions",
  crumb="behind page 4 · term N ↓ · steps are counted as each paper counts them · calc. = our arithmetic",
  body=table(h_d, [
   [wk("UFO2, GUI + API", "ufo2"), "Native API calls replace GUI sequences in Office apps", "Model-involved steps 16.0 → 6.6 with o1, but 13.8 → 12.9 with GPT-4o, on tasks both settings completed; 12 hand-built APIs", "No wall-clock"],
   [wk("CUA-Verse", "cuaverse"), "A command-line tool added to a fine-tuned 9B agent", "OSWorld subset of 244 tasks, same model: success 23.4 → 40.2%, mean steps 39.6 → 28.6, tokens 325.7K → 286.5K", "Training on 4,923 episodes"],
   [wk("SPACE", "space"), "RL-trained variable-length action chunks", "ALFWorld unseen split, Qwen3-4B: model rounds 20.9 → 4.4, success 81.3 → 96.9% vs the best baseline (multi-action GRPO)", "Text environments only; no time or tokens"],
   [wk("SpeedRunner", "speedrunner"), "A coding agent refactors the skill library for cost", "Crafter: model calls −94% over training; Gemini-3-Flash, 3 seeds", "Text game; with Gemini-3-Flash success fell significantly below the OPO baseline on every benchmark"],
   [wk("AWM", "awm"), "Induced workflows injected into the prompt", "WebArena 812 tasks: success 15.0 → 35.5%, steps 7.9 → 5.9 vs the page-tree baseline; +10.8% computation for induction (its App. D). In ASI’s re-run: 5.9 steps vs 5.6 plain", "Prompt grows"],
   [wk("Beyond Browsing", "beyondbrowsing"), "API calls and API documentation in context, with browsing as fallback", "WebArena, GPT-4o: success 14.8 → 38.9% (hybrid), steps 8.4 → 8.5, $0.1 → $1.4 per task", "API documents lengthen the prompt"],
   [wk("ComputerRL", "computerrl"), "An API-GUI action space", "OSWorld, prompted GPT-4o: success 11.2 → 26.2%", "No step, time or $ figures"],
   [wk("CoAct-1", "coact1"), "An orchestrator hands sub-tasks to a coding agent or a GUI agent", "OSWorld-Verified: success 53.07 → 59.93% vs GTA-1-7B with o3; 10.15 vs 15.22 steps per passed task", "Step budget behind 10.15 ambiguous"],
   [wk("OSWorld-Human", "osh"), "Human reference trajectories, grouped by screenshot", "Steps per trajectory, single → grouped: Chrome 5.8 → 4.3 (1.35×) to Calc 13.2 → 4.5 (2.93×) (calc.); 369 tasks", "A human-reference headroom estimate, not a method or a strict bound"],
  ], w_d))

B("b2-2", "B2 · 2/2", "B2 · Capping the steps: stopping rules and budgets",
  crumb="behind page 4 · term N capped · a stop can end attempts that would have succeeded (R_m(p) ↓) · calc. = our arithmetic",
  body=table(h_d, [
   [wk("EET", "eet"), "Stops a run early when past experience predicts no gain", "SWE-bench Verified, GPT-5-mini, Agentless: resolved 33.2 → 41.0%, benchmark cost $13.77 → $6.18, API calls −26.4%; six-configuration average cost −31.8%", "Offline experience base; one configuration −0.2 points"],
   [wk("Runaway is ashamed", "runaway"), "A verifier decides when to exit", "ALFWorld 134 tasks, Llama-3.1-70B: steps 19.0 → 13.4, success 76.1 → 70.2%", "Success falls"],
   [wk("Budget Tracker", "bats"), "Tells the agent its remaining tool budget", "BrowseComp, Gemini-2.5-Pro: 12.8% at budget 10 vs 12.6% at 100; cost per question 9.9¢ → 6.8¢ (−31.3%)", "Tool calls priced at a flat $0.001"],
   [wk("Efficient Agents", "effagents"), "A cheaper agent configuration", "GAIA, 165 tasks (calc.): $0.398 → $0.285 per task, 53.33 → 51.52%; one run", "Baseline configuration not stated"],
   [wk("TTI (counterpoint)", "tti"), "Trains the agent to take more steps (interaction scaling)", "WebVoyager 427 tasks: 55.8 → 64.8% (zero-shot → TTI); WebArena 812: 18.3 → 26.1%; Gemma 3 12B. Longer thinking at equal compute gave under 3%", "N grows by design; no cost figures"],
  ], w_d))

B("b3-1", "B3", "B3 · Agent-aware serving: more systems",
  crumb="behind page 5 · terms t^queue and t^prefill · self-hosted engines; all figures are throughput or latency under load, none reports task quality unless stated",
  body=table(["system", "mechanism", "measured effect, with its conditions", "baseline"], [
   [wk("SGLang", "sglang"), "Prefix sharing in a radix tree of KV caches", "Up to 6.4× throughput, 3.7× lower latency; Llama-7B on one A10G; 12 workloads incl. ReAct and generative agents (replayed)", "vLLM v0.2.5, Guidance, LMQL (which gives the maximum is not stated)"],
   [wk("Preble", "preble"), "Prompt-sharing-aware scheduling across GPUs", "1.5–14.5× lower mean and 2–10× lower p99 latency; tool use, embodied agent, program generation, video and long-document QA; Mistral 7B, Llama-3 70B", "Data-parallel SGLang"],
   [wk("Parrot", "parrot"), "Semantic variables expose a program’s structure to the server", "Up to 11.7× lower end-to-end latency; MetaGPT multi-agent programming, LLaMA 13B, one A100", "Latency-centric vLLM"],
   [wk("KVFlow", "kvflow"), "Workflow-aware cache eviction and prefetching", "1.24× vs SGLang with hierarchical cache (camera-ready, Qwen2.5-32B, one H100); the 1.83× headline is from the v1 A10G set-up only", "SGLang HiCache"],
   [wk("Helium", "helium"), "Workflow-level optimisation of batched agent queries", "Up to 1.56× vs KVFlow (end-to-end latency of a batch, optimisation included)", "KVFlow"],
   [wk("KVCOMM", "kvcomm"), "Reuses KV caches across agents with offset correction", "First-token time 7.82× lower at the fifth agent (428.6 → 54.8 ms); Llama-3.1-8B, one H100, HuggingFace", "Full prefill"],
   [wk("DroidSpeak", "droidspeak"), "Shares KV caches between fine-tuned variants of one model", "Prefill 1.7–3.1× faster (average 2.1×); eight model pairs, three datasets each", "Full prefill"],
   [wk("AsymCache", "asymcache"), "Asymmetric cache eviction for multi-session serving", "With Continuum, average job latency 4.4–18.1% below Continuum alone; alone 0.4–4.2% below vLLM-LRU (BFCL web search, no task count); its own headline ranges are inconsistent", "Continuum; vLLM-LRU"],
   [wk("CacheBlend", "cacheblend"), "Blends precomputed chunk caches, recomputing a few tokens", "First-token time 2.2–3.3× lower, quality within 0.02 F1 — RAG, not agents", "Full recompute"],
  ], ["15%", "27%", "43%", "15%"]))

B("b4-1", "B4 · 1/2", "B4 · Prefill and context: more rows, with full conditions",
  crumb="behind pages 6 and 11 · terms |o_{a,i}|, ḡ and t^prefill · calc. = our arithmetic",
  body=table(h_d, [
   [wk("FocusAgent, other settings", "focusagent"), "Reader model GPT-5-mini instead of GPT-4.1-mini", "WorkArena L1: input cost −31.5% (calc.) at 53.2% success; WebArena 381 tasks: 36.5 → 39.6%, −21.7%. Input tokens only are priced", "No latency for this reader"],
   [wk("LineRetriever", "lineretriever"), "A reader model keeps whole lines of the page tree", "Observation −61% on WorkArena L1 (330 runs), success 52.7 → 44.8%", "Success falls"],
   [wk("Prune4Web", "prune4web"), "A model writes a scoring program; the top 20 elements go to the grounder", "25–50× fewer candidate elements; grounding accuracy 46.8 → 88.28% with ground-truth sub-tasks (1,101 steps)", "Grounding, not task success; no latency measured"],
   [wk("SimpAgent", "simpagent"), "Masks irrelevant screenshot regions and compresses history", "FLOPs per step 11.90 → 8.71 T; offline step success 69.0 → 71.3% (AITW), Qwen2-VL-2B", "Offline steps"],
   [wk("ScreenSeekeR (counter)", "screenseeker"), "A planner searches the screen recursively for the target", "Grounding 18.9 → 48.1% on 1,581 ScreenSpot-Pro instructions, GPT-4o planner", "More model calls per step"],
   [wk("Observation masking, other models", "masking"), "As on page 11", "Gemini 2.5 Flash $0.41 → $0.18, 32.8 → 35.6%; with thinking 40.4 → 36.4% (significant); Qwen3-32B $1.12 → $0.55, 17.0 → 15.0%", "Success can fall"],
   [wk("AgentDiet, per task", "agentdiet"), "As on page 11", "$0.535 → $0.422 (Claude, SWE-bench Verified), $0.701 → $0.449 (Gemini, Multi-SWE-bench Flash); cached-input discount applied", "Reducer 5.5–11.8% of the original cost"],
   [wk("FireAct", "fireact"), "A fine-tuned GPT-3.5 drops the few-shot examples from every prompt", "HotpotQA 500 questions: 9.0 → 2.7 s per trial, $2.6e-3 → $2.2e-3, EM 31.4 → 39.2", "Price per token ×8 (c_κ(μ) ↑)"],
   [wk("TokenPilot, mixed sessions", "tokenpilot"), "As on page 12", "123 tasks shuffled into 10 sessions: $21.16 → $4.83 (−77%, calc.), score 68.77 → 69.10", "Partial-credit scores"],
  ], w_d))

B("b4-2", "B4 · 2/2", "B4 · Decoding: more rows, with full conditions",
  crumb="behind page 7 · terms n^out and TPOT · vendor = the vendor’s own statement",
  body=table(h_d, [
   [wk("Think Twice, Click Once", "thinktwice"), "Switches between a fast and a slow grounding mode", "Time per sample 3.2 → 2.6 s, accuracy 74.8 → 77.4%; slow mode only 5.4 s — 1,272 samples, Qwen2-VL-2B, same model with and without its switch threshold", "Grounding only"],
   [wk("Does CoT help mobile agents?", "cotmobile"), "Caps the reasoning tokens", "AndroidControl, GLM-4.6V: action accuracy 71.55% at 128 tokens vs 70.41% unlimited and 70.32% without reasoning", "Sample size not stated"],
   [wk("TSDS", "tsds"), "Short edge thinking, deferral to the cloud when unsure", "MBPP (257 problems, single step): edge thinking tokens 1,183 → 422, reward 0.719 → 0.714", "Cloud deferral rate 0.346; cloud tokens not counted"],
   [wk("GUI-KV", "guikv"), "Keeps 40% of the KV cache per layer (5 screenshots in context, UI-TARS-1.5-7B)", "Decoding MFLOPs per token −38.9%, offline step accuracy 17.5 → 21.6% (AgentNetBench); OSWorld 26.0 → 25.1%", "No wall-clock"],
   [wk("Agent-X", "agentx"), "A precomputed prompt-prefix cache and speculative decoding on a Mac mini", "Task time 1.61× faster (prefill 1.97×, decode 1.73×) on 1,022 TinyAgent examples, Mac mini M4 Pro", "On-device only"],
   [wk("Effort guidance (vendor)", "anth-a"), "Medium instead of high reasoning effort", "“Roughly half the output tokens of high” with close to the best success, and the same success once retries are allowed — internal UI-automation suite, no counts", "Vendor statement"],
   [wk("Ultrafast (vendor)", "openai", "cerebras"), "GPT-5.6 Sol on Cerebras hardware", "Up to 14× faster than Standard, up to 750 output tokens per second; limited preview, no price", "OpenAI vendor statements; a hardware partner’s 6-task chart is marketing, not cited"],
  ], w_d))

B("b5-1", "B5", "B5 · Environment and overlap: more rows, with full conditions",
  crumb="behind pages 8–10 · terms E_i and T_saving · calc. = our arithmetic",
  body=table(h_d, [
   [wk("Skim, details", "skim"), "As on page 8; a local Qwen2.5-14B runs the fast path and the verifier", "Accuracy vs the default agent: 40.6 vs 37.6 (WebVoyager agent), 52.0 vs 49.6 (AgentOccam), 45.6 vs 45.0 (BrowserUse); verifier precision 82.0%, recall 86.2%", "Site profiling 6–24 s per site"],
   [wk("TPS-Bench", "tpsbench"), "RL-trained scheduling of dependent tool calls", "TPS-Bench-Hard, 100 tasks, Qwen3-1.7B: time 42.0 → 34.8 s per task (−17.1%, calc.), completion 26.75 → 35.17%", "Its text gives 14% and 6% (from v1)"],
   [wk("AsyncLM", "asynclm"), "Asynchronous function calls with interrupts", "Local fine-tuned Llama-3.2 on one RTX 4090: 1.6–2.4× lower latency than sequential calls, 1.23–1.5× than parallel calls (calc.; first to last generated token); cloud figures emulated", "Emulated for GPT-4o"],
   [wk("Speculative tool calls", "nichols"), "Client- and engine-side speculation of tool calls", "6–21% of time saved with synthetic tool latencies and cached tool outputs; BFCL, 32 tasks per agent", "Synthetic latencies"],
   [wk("DSP", "dsp"), "Learns how many steps ahead to speculate", "OpenAGI 312 tasks, GPT-4.1-mini: −37.09% latency at +62.99% cost; the cost is against the sequential cost of both agents", "Cost vs a target-only agent not reported"],
   [wk("Speculate with memory", "swm"), "Guesses from a memory of past runs", "Analytical peak 1.128×; HotpotQA 1.05× — replay estimates", "Not end-to-end"],
   [wk("AgenticCache", "agenticcache"), "Cached plans for embodied agents", "TDW-COOK, 18 episodes: 12.86 → 1.75 h, $21.0 → $4.4, success 94.44 → 100%; TDW-MAT 1.86× (calc.)", "Embodied simulator"],
   [wk("IdleSpec (counter)", "idlespec"), "Drafts plans while tools run", "GAIA 165 + FRAMES 50, Gemini-2.5-Flash: accuracy 50.5 → 55.6%, wall-clock about unchanged; output tokens +58% (calc., Qwen3.5-4B)", "Tool-wait overlap spent on accuracy (R_m(p) ↑), not on time"],
   [wk("ThunderAgent", "thunder"), "Prepares the sandbox while the program waits for GPU memory (overlap, T_saving)", "Environment time 4.8 → 0.3 s — OpenHands rollouts, self-hosted (its Fig. 6a)", "Throughput system; no task success"],
   [wk("TClone · DeltaBox", "tclone", "deltabox"), "Fast container clone; millisecond checkpoint and rollback", "Clone for one OSWorld branch point 18.2 → 3.7 s vs KVM; rollback 1.86 ms on the fast path (9.29 ms slow path)", "Cost of branching E_i"],
  ], w_d))

B("b6-1", "B6", "B6 · Prices by billing class and tier, per vendor",
  crumb="behind pages 12–13 · vendor price pages and documentation, read 28 September 2026 · ratios are our arithmetic (calc.)",
  body=table(["vendor, latest model", "uncached → cache hit (per 1M input tokens)", "cache write, storage, lifetime", "tiers"], [
   [wk("DeepSeek-V4.1-Flash", "deepseek"), "$0.30 → $0.006 (0.02×), peak; off-peak half", "none listed", "—"],
   [wk("Anthropic, Claude Opus 5.5", "anth-b"), "$4 → $0.20 (0.05×); Fable 5.1 and Mythos 5.1 0.025×; other Claude models 0.1×", "1.25× for 5 min, 2× for 1 h; refreshed free on each use; a change of speed, tools, thinking or effort invalidates parts of the cache", "Fast mode 2× ($8 / $40), up to 2.5× output speed"],
   [wk("OpenAI, GPT-6 Sol / Luna", "openai"), "$2 → $0.20; $0.10 → $0.01 (0.1×)", "1.25× from GPT-5.6 on; at least 30 min", "Fast 2×; Flex and Batch 0.5×"],
   [wk("Google, Gemini 3.8 Flash", "google"), "$0.75 → $0.075 (0.1×), to 31 Dec 2026", "storage $0.50 per 1M tokens per hour", "Priority 1.8× on every listed price (text says 75–100%), Preview"],
   [wk("xAI, Grok 4.7", "xai"), "$2 → $0.50 (0.25×)", "none listed", "—"],
   [wk("Microsoft Foundry", "microsoft"), "—", "—", "Priority processing 1.75–2.5× (calc., from the pricing page’s HTML)"],
  ], ["20%", "27%", "30%", "23%"]) + """
<div class="apx-note">Worked example (OpenAI, GPT-5.6 and later): one write and one read cost 1.25 + 0.1 = 1.35× against 2× uncached; one write and nine reads cost 2.15× against 10× (calc.).</div>""")

B("b7-1", "B7", "B7 · A cheaper model per call: more rows, with full conditions",
  crumb="behind page 13 · term c_κ(μ_ij) · calc. = our arithmetic",
  body=table(h_d, [
   [wk("StepWise, web", "stepwise"), "gpt-oss-20b by default, GPT-5.2 when stuck", "WebArena-Verified (~812 tasks, calc.): $0.335 → $0.211 per task, 60.1 → 57.8%, time per request 19.6 → 12.2 s; local 2×H100 timing", "Large model on 66.9% of steps"],
   [wk("BoPO", "bopo"), "A router under a cap on large-model calls", "AppWorld 168 tasks, GPT-4.1 / GPT-4.1 mini, 3 seeds: large calls per task 18.75 → 13.2 (−29.6%, calc.), success 66.7 → 66.5%", "Router cost excluded"],
   [wk("Agentic plan caching, per workload", "apc"), "As on page 13", "FinanceBench $4.03 → $1.86, 91.0 → 85.5%; QASPER $2.14 → $0.78; GAIA $69.02 → $16.27, 37.58 → 36.97%", "GAIA task count not stated"],
   [wk("RouteLLM", "routellm"), "A learned router between a strong and a weak model", "3.66× fewer GPT-4 calls than a random router at equal quality (MT-Bench); 1.41× (MMLU), 1.49× (GSM8K)", "Single-turn; not against always-GPT-4"],
   [wk("FrugalGPT", "frugal"), "A cascade of models with a stopping scorer", "Up to 98% lower cost at equal accuracy on one single-query dataset (HEADLINES)", "Single-turn"],
  ], w_d))

def _cps(c, r):
    v = c / r
    return f"${v:,.0f}" if v >= 100 else f"${v:,.2f}"
B("b8-1", "B8", "B8 · Cost per success: the inputs, the formula and the rounding",
  crumb="behind page 14 · v = cost per attempt ÷ success rate (Cost-of-Pass, Eq. 2) · all results are calc. unless stated",
  body=table(["work", "cost per attempt (as printed)", "success rate", "cost per success (calc.)", "note"], [
   [wk("AXIS vs UFO", "axis"), "$0.4 → $0.2", "52.0 → 84.0%", f"{_cps(0.4, .52)} → {_cps(0.2, .84)}", "costs printed to one decimal"],
   [wk("W&amp;D", "wd"), "$1.025 → $0.657 ($102.5, $65.7 per 100)", "66 → 68%", f"{_cps(1.025, .66)} → {_cps(0.657, .68)}", "includes search and scraping fees"],
   [wk("OSWorld 2.0, Opus 4.8", "osw2"), "~$76.1 → ~$72.4", "18.5 → 20.6%", f"{_cps(76.1, .185)} → {_cps(72.4, .206)}", "Opus 4.7: $258 → $185"],
   [wk("Beyond Browsing", "beyondbrowsing"), "$0.1 · $1.2 · $1.4", "14.8 · 29.2 · 38.9%", f"{_cps(0.1, .148)} · {_cps(1.2, .292)} · {_cps(1.4, .389)}", "browsing · API · hybrid; one-decimal costs, so the ratio is 3–11×"],
   [wk("BATS vs ReAct@100", "bats"), "9.9¢ → $1.1", "12.6 → 24.6%", f"{_cps(0.099, .126)} → {_cps(1.1, .246)}", "BrowseComp, Gemini-2.5-Pro"],
   [wk("ActionEngine", "actionengine"), "$0.71 → $0.06", "66 → 95%", f"{_cps(0.71, .66)} → {_cps(0.06, .95)}", "different models on the two sides"],
   [wk("StepWise, OSWorld", "stepwise"), "$0.881 → $0.224", "58.1 → 55.4%", f"{_cps(0.881, .581)} → {_cps(0.224, .554)}", ""],
   [wk("WebRouter", "webrouter"), "$0.98 → $0.12", "86.1 → 82.3%", f"{_cps(0.98, .861)} → {_cps(0.12, .823)}", ""],
   [wk("Fara-7B vs computer-use-preview", "fara"), "$0.913 → $0.025", "70.9 → 73.5%", f"{_cps(0.913, .709)} → {_cps(0.025, .735)}", "WebVoyager"],
   [wk("AI Agents That Matter", "kapoor25"), "LATS $134.50 vs warming $2.45 (164-problem run totals)", "88.0 vs 93.2%", "stated totals, not per success", "HumanEval, GPT-4"],
  ], ["20%", "22%", "15%", "18%", "25%"]) + """
<div class="apx-note">With a set-up cost (page 14): <b>v<sub>n</sub> = C<sub>setup</sub>/n + v</b>. Two retained works print both parts. EET’s experience base cost $4.3 once, against a benchmark run of $13.77 → $6.18 (500 tasks), so it pays off within the first run: $10.48 with the set-up charged to it (calc.). SpeedRunner already spreads its skill-inducer calls over the runs they serve. The page-3 systems print their set-up in minutes, tokens or GPT-4o dollars, never next to a per-task dollar figure.</div>""")

B("b9-1", "B9", "B9 · Works held back or dropped, and why",
  crumb="the source-credibility rule of slides/references.md · (iii) = numbers from a public benchmark with the task count and model stated",
  body=table(["status", "works", "reason"], [
   ["Held back: condition (iii) not met as written, pending Edwin’s decision", "SpecHop (arXiv:2605.21965), PASTE (2603.18897), AOSpec (2608.00881), TAB, CacheScout (2608.14624), DualPath, PBKV, AgentKVShift, SpecBox (2607.23933), LLM-Tool Compiler, Cordon (2606.17573), GoClick, BAVT; DualSpec’s XBench row; Continuum’s real-run 8.18×", "No task count, internal traces, or an unnamed model; their numbers stay off the pages"],
   ["Shown with a flag, pending the same decision", "Skim (“300+” tasks, page 8); ARES (~129 WebArena tasks, calc.), Overthinking (SWE-bench Verified), StepWise (OSWorld), Fara-7B (WebVoyager): task counts not printed; the author-built test suites of Atomix (leak test), Safe to Resume? (96 workflows) and Ghost Tool Calls (30 tasks)", "Counts derived by us, implied by the benchmark, or from suites the authors built; labelled on the pages"],
   ["Dropped: fail the rule", "Octopus v2, GPA, SkillDroid (qualitative only), AgentServe, Stateful Inference (Norgren), Cost-Aware Speculative Execution (Fareed), Dynamic ReAct, AdaGUI-R1, a speculative-tools GitHub repository", "In-house sets without counts, single authors without measurements, no institution, or unreadable"],
   ["Could not be read or found", "OS-Catalyst; ToolSEE; the Self-Guide “+22%”, VITA-VLA “−76%” and “2,000–8,000 schema tokens” figures", "The figures are not in the sources"],
   ["Off-topic", "SEAR, DREAM-Chunk (robotics); VITA-VLA, m2mKD (not LLM agents); SRMT (not an LLM); MemRefine (offline storage); DARE (math reasoning); Self-Guide (no efficiency measure)", "No Part 1 term"],
   ["Qualitative only", "ECLAIR, AgentRR, Signal-Driven Observation, the small-models position paper, the LATM / DiLogics / ALLOY / Voyager / WebAgent lineage, RAC, Revisable by Design, AAPT, Qwen-UI-Agent, Log2Plan, ConServe, TOPAS, SmoothAgent, AAFLOW+ (modelled), PEEK, PANDO (flagged), vendor cache marketing", "No usable measured number, or internal inconsistencies"],
   ["Numbers replaced by corrections", "SkillDroid 2.4×; Hajimiri v1; KVFlow 1.83× (absent from the camera-ready body); AgentServe 2.8× (against llama.cpp); RouteLLM 3.66× “vs GPT-4”; UFO2 “51.5% lower inference cost”; WALT “1.3–1.4× on average”", "Superseded by the source checks"],
  ], ["22%", "54%", "24%"]))

B("b10-1", "B10", "B10 · What no retained work measures yet, by term",
  crumb="gaps in the evidence, not claims of a research gap · the one-line versions are in each page’s foot",
  body=table(["term", "not yet measured"], [
   [tex("J_i", 11) + " (compile, replay)", "Replay under live application change; a vendor replay or repair rate with a sample; cost per success with set-up included; a multi-page enterprise form with a final submit"],
   [tex(r"t^{\mathrm{queue}}", 11), "Its share of task time for API agents; measured latency of API priority tiers (only classes or targets are published)"],
   [tex(r"t^{\mathrm{prefill}},\ |o_{a,i}|", 11), "Task time with caching on; how pruning interacts with prefix caching; the load time of cache-hit tokens, which Part 1 has no term for"],
   [tex(r"n^{\mathrm{out}},\ \mathrm{TPOT}", 11), "The net effect of per-step effort changes that invalidate the message cache; independent task-level timing of fast tiers"],
   [tex("E_i", 11), "Page-load and wait time in write-heavy web workflows (Skim is read-only); wall-clock of batched actions"],
   [tex(r"T_{\mathrm{saving}}", 11), "Speculation on a live web GUI with side effects held until commit; cost per success of any speculation method; several speed figures are analytical or replayed"],
   [tex(r"\bar{g},\ N^2", 11), "The N² token volume together with the cache hit rate in a GUI agent; structural removal is shown only by compiled plans; eviction (TokenPilot) may change the shape but is not measured as such"],
   [tex(r"n^{\kappa},\ x_{\mathrm{env}}", 11), "A GUI or browser agent’s tokens split by billing class, cache writes included (Don’t Break the Cache covers a web-search agent); environment hours priced beyond a vendor list price (coding agents only in TraceLab)"],
   [tex(r"c_{\kappa}(\mu_{ij})", 11), "The router’s own cost; small-model losses on enterprise forms; routing with cached prices"],
   [tex("R_m(p)", 11) + ", set-up", "Cost per success reported by the papers themselves; time, money and success, set-up included, on one web or GUI benchmark"],
  ], ["22%", "78%"]))

# ---------------------------------------------------------------- render
CSS = r"""
:root{--ink:#1b2733;--ink2:#3d4b58;--mute:#6f7d8a;--accent:#0f5a7c;--accent2:#1c6f95;--callout:#e2edf4;--card:#f5f8fa;--rule:#d9e1e7;--warn:#b3600c;--bg:#ffffff;}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#20262c;height:100%;font-family:'IBM Plex Sans',-apple-system,'Helvetica Neue',Arial,sans-serif;color:var(--ink);-webkit-font-smoothing:antialiased}
#stage{position:absolute;left:50%;top:50%;width:1280px;height:720px;transform-origin:0 0;background:var(--bg);box-shadow:0 0 40px rgba(0,0,0,.5)}
.slide{display:none;position:absolute;inset:0;width:1280px;height:720px;background:var(--bg);padding:34px 41px 30px 41px;overflow:hidden;flex-direction:column}
.slide.on{display:flex}
.label{font-family:'IBM Plex Mono',Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
h1{font-size:29px;line-height:1.15;font-weight:700;letter-spacing:-.01em;margin:6px 0 0 0;max-width:880px;text-wrap:balance}
.rule{height:1px;background:var(--rule);margin-top:14px;flex:none}
.crumb{font-family:'IBM Plex Mono',Menlo,monospace;font-size:11.5px;color:var(--mute);letter-spacing:.01em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:10px;flex:none}
.thumb{position:absolute;right:40px;top:10px;width:305px;height:64px;border:1px solid var(--rule);border-radius:4px;background:#fff;padding:5px 6px;display:flex;align-items:center}
.thumb > svg{width:100%;height:100%}
.content{flex:1;min-height:0;margin-top:14px;margin-bottom:34px;display:flex;flex-direction:column;gap:12px}
.callout{background:var(--callout);border-radius:4px;padding:11px 18px;font-size:14.5px;line-height:1.42;flex:none}
.callout p{margin:0 0 5px 0}.callout p:last-child{margin:0}
.body{flex:1;min-height:0;display:flex;flex-direction:column;gap:12px}
.foot{position:absolute;left:41px;bottom:26px;right:230px;font-family:'IBM Plex Mono',Menlo,monospace;font-size:10.5px;color:var(--mute);line-height:1.4}
.chip{position:absolute;right:41px;bottom:26px;font-family:'IBM Plex Mono',Menlo,monospace;font-size:11px;color:var(--ink2);border:1px solid var(--rule);border-radius:14px;padding:5px 12px;text-decoration:none;background:#fff}
.chip:hover{border-color:var(--accent);color:var(--accent)}
/* cards */
.cards3,.cards4,.rows5,.rows6,.figs3{display:grid;gap:12px}
.cards3{grid-template-columns:repeat(3,1fr)}.cards4{grid-template-columns:repeat(4,1fr)}
.rows6 .card{padding:6px 13px}.rows6 .cv{font-size:14px}.rows6 .cd{font-size:12.5px;line-height:1.4}.rows5{grid-template-columns:repeat(5,1fr)}.rows5.big .cd{font-size:13.5px}.rows5.big .cv{font-size:16px}.rows5.big .card{padding:14px 14px}.rows6{grid-template-columns:repeat(3,1fr);gap:9px}
.figs3{grid-template-columns:repeat(3,1fr);gap:20px;flex:none}
.figs1{display:flex;flex:none}.figs1 .fig{width:600px;max-width:100%}
.card{border:1px solid var(--rule);border-radius:4px;padding:11px 13px;background:#fff;display:flex;flex-direction:column;gap:5px;min-height:0}
.ck{font-family:'IBM Plex Mono',Menlo,monospace;font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
.cv{font-size:15px;font-weight:700;line-height:1.28;letter-spacing:-.005em}
.cd{font-size:13px;line-height:1.42;color:var(--ink2)}
ul.cd{margin:0;padding-left:15px}
ul.cd li{margin:0 0 4px 0;padding-left:1px}
ul.cd li::marker{color:var(--accent)}
.cc{font-family:'IBM Plex Mono',Menlo,monospace;font-size:10px;color:var(--mute);margin-top:auto;padding-top:4px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:16px;flex:1;min-height:0}
.stack{display:flex;flex-direction:column;gap:12px}
.figcap{font-family:'IBM Plex Mono',Menlo,monospace;font-size:10.5px;color:var(--mute);margin-top:4px;line-height:1.4}
.fig-mid{width:1000px;margin:0 auto}
.big-svg{width:100%;height:auto;display:block}
.sym{display:grid;grid-template-columns:1fr 1fr;gap:3px 28px;font-size:12px;color:var(--ink2);line-height:1.35}
.sk{display:inline-block;min-width:150px;margin-right:6px;font-family:'IBM Plex Mono',Menlo,monospace;font-size:10.5px;color:var(--accent);letter-spacing:.02em}
.concl{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.concl>div{background:var(--callout);border-radius:4px;padding:9px 14px;font-size:13px;line-height:1.4}
.oneline{background:var(--callout);border-radius:4px;padding:9px 14px;font-size:13.5px;line-height:1.4}
/* figures (horizontal bars) */
.fig{display:flex;flex-direction:column;gap:4px;min-width:0}
.ft{font-size:11.5px;font-weight:500;line-height:1.3;color:var(--ink2)}
.fc{font-family:'IBM Plex Mono',Menlo,monospace;font-size:9.5px;color:var(--mute);line-height:1.35}
.hb{width:100%;height:auto;display:block}
.hb .hl-lab{fill:var(--ink2);font-family:'IBM Plex Mono',Menlo,monospace;font-size:10.5px}
.hb .hl-val{fill:var(--ink);font-family:'IBM Plex Mono',Menlo,monospace;font-size:10.5px;font-weight:500}
.hb .hl-bar{fill:var(--accent)}
/* inline math */
svg.tex{display:inline-block;height:auto}
.legend{display:flex;gap:18px;font-family:'IBM Plex Mono',Menlo,monospace;font-size:10.5px;color:var(--mute);margin:0 0 2px 82px;align-items:center}
.legend span{display:inline-flex;align-items:center;gap:5px}
.sw{display:inline-block;width:11px;height:11px}
.sw.b-read{background:var(--accent)}.sw.b-write{background:#b9c7d1}
.eqstrip .eqx svg.tex,.lp svg.tex,.eqt svg.tex{vertical-align:middle}
/* page 2 layout */
.loopgrid{display:grid;grid-template-columns:690px 1fr;gap:22px;align-items:start;flex:none}
.fig-loop{width:690px}
.eqs{display:flex;flex-direction:column;gap:6px;padding-top:2px}
.eqrow{display:flex;align-items:center;gap:10px}
.eqrow svg.eq{height:38px;width:auto;max-width:100%}
.eqrow.small svg.eq{height:34px}
.eql{font-family:'IBM Plex Mono',Menlo,monospace;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute);min-width:44px}
.eqnote{font-size:11.5px;line-height:1.4;color:var(--ink2)}
.eq-fallback{font-family:'IBM Plex Mono',Menlo,monospace;font-size:12px}
.quadgrid{display:grid;grid-template-columns:520px 1fr;gap:22px;align-items:start;flex:none}
.quadgrid .chart{width:100%}
/* page 10 layout */
.levgrid{display:grid;grid-template-columns:1fr 430px;gap:24px;align-items:start}
.gapcol ul{margin:6px 0 0 0;padding-left:16px;font-size:12.5px;line-height:1.4;color:var(--ink2)}
.gapcol li{margin-bottom:7px}
/* equation strip (page 4) */
.eqstrip{display:flex;align-items:flex-end;gap:10px;border:1px solid var(--rule);border-radius:4px;padding:7px 14px;flex:none}
.eqt{font-size:14px;font-weight:600;align-self:center;white-space:nowrap}
.eqterm{flex:1;border-left:2px solid var(--accent);padding:2px 10px}
.eqx{font-size:14px;color:var(--ink);white-space:nowrap}
.eqc{font-family:'IBM Plex Mono',Menlo,monospace;font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin-top:3px}
/* link figure (page 16) */
.linkfig{border:1px solid var(--rule);border-radius:4px;padding:8px 14px;display:flex;flex-direction:column;gap:6px;flex:none}
.lrow{font-size:13px;display:flex;align-items:center;flex-wrap:wrap;gap:5px;color:var(--ink2)}
.lk{font-family:'IBM Plex Mono',Menlo,monospace;font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute);min-width:52px}
.lp{display:inline-block;border-radius:10px;padding:1px 9px;font-size:12px;font-weight:500;border:1px solid}
.lp.same{background:var(--accent);border-color:var(--accent);color:#fff}
.lp.time{background:#eef1f3;border-color:#c4ced6;color:var(--ink2)}
.lp.buy{background:#fbeede;border-color:#e2b98b;color:var(--warn)}
.lleg{display:flex;gap:10px;flex-wrap:wrap;font-size:11px}
.lleg .lp{font-size:11px}
/* tables */
.tbl{width:100%;border-collapse:collapse;font-size:12px;line-height:1.35}
.tbl th{font-family:'IBM Plex Mono',Menlo,monospace;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute);text-align:left;font-weight:500;padding:0 8px 6px 6px;border-bottom:1px solid var(--accent)}
.tbl td{padding:6px 8px 6px 6px;border-bottom:1px solid var(--rule);vertical-align:top;color:var(--ink2)}
.tbl td:first-child{font-family:'IBM Plex Mono',Menlo,monospace;font-size:11px;color:var(--accent)}
.tbl td.rk{font-family:'IBM Plex Mono',Menlo,monospace;font-size:10.5px;color:var(--accent);text-transform:uppercase;letter-spacing:.06em}
.tbl b{color:var(--ink)}
.tbl.three td{font-size:12px}
.tbl.conv td{font-size:12.5px}.tbl.lev td,.tbl.gaps td{font-size:13.5px;line-height:1.45;padding:8px 8px 8px 6px}
.tbl.conv td:first-child{font-family:inherit;font-size:12.5px;color:var(--ink2)}.tbl.lev td:first-child,.tbl.gaps td:first-child{font-family:inherit;font-size:13.5px;color:var(--ink2)}
.appendix .tbl{font-size:10.6px;line-height:1.32}
.appendix .tbl td{padding:4px 7px 4px 4px}
.appendix .tbl td:first-child{font-size:10px}
.apx-note{margin-top:8px;font-size:11.5px;line-height:1.4;color:var(--ink2);background:var(--callout);border-radius:4px;padding:8px 12px}
/* references */
.reflist{margin:0;padding-left:20px;font-size:12px;line-height:1.38;color:var(--ink2);columns:2;column-gap:28px}
.reflist li{margin:0 0 7px 0;break-inside:avoid}
.reflist i{font-style:italic}
/* cover */
.cover{position:absolute;inset:0;display:grid;grid-template-columns:560px 1fr;gap:40px;padding:0 41px}
.cover-l{padding-top:200px}
.cover-kicker{font-family:'IBM Plex Mono',Menlo,monospace;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
.cover-title{font-size:56px;line-height:1.02;letter-spacing:-.025em;margin:14px 0 18px 0;max-width:560px}
.cover-sub{font-size:19px;line-height:1.35;margin:0 0 14px 0;color:var(--ink)}
.cover-sub2{font-size:13.5px;line-height:1.45;color:var(--ink2);margin:0 0 22px 0;max-width:520px}
.cover-date{font-family:'IBM Plex Mono',Menlo,monospace;font-size:12.5px;color:var(--mute);margin:0}
.cover-r{padding-top:170px}
.cover-fig-title{font-size:12.5px;font-weight:600;margin-bottom:14px}
.cover-svg{width:100%;height:auto}
.cover-fig-cap{font-family:'IBM Plex Mono',Menlo,monospace;font-size:10.5px;color:var(--mute);margin-top:10px;line-height:1.4}

/* deck title page and Part title page */
.cover-deck{grid-template-columns:1fr}
.cover-one{padding-top:236px}
.cover-deck .cover-title{font-size:66px;max-width:900px;margin:0 0 22px 0}
.cover-deck .cover-sub{font-size:21px;max-width:760px;margin:0 0 30px 0;color:var(--ink2)}
.cover-r .toc-t{font-family:'IBM Plex Mono',Menlo,monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute);margin:30px 0 10px 0}
.toc{list-style:none;margin:0;padding:0;border-top:1px solid var(--accent)}
.toc li{display:grid;grid-template-columns:62px 1fr;gap:10px;padding:10px 0;border-bottom:1px solid var(--rule);font-size:15px;line-height:1.35;color:var(--ink)}
.toc li span{font-family:'IBM Plex Mono',Menlo,monospace;font-size:12px;color:var(--accent);padding-top:2px}
/* page 2: loop diagram with variables, and the equation table */
.fig-loop2{flex:none;display:flex;justify-content:center}
.fig-loop2 svg.big-svg{width:1060px;height:auto;display:block}
.eqtab>div.eqg svg.tex{vertical-align:middle}
.defs{display:grid;column-gap:18px;row-gap:3px;font-size:11.5px;line-height:1.35;color:var(--ink2);flex:none;border-top:1px solid var(--rule);padding-top:6px}
.defs.c3{grid-template-columns:repeat(3,1fr)}.defs.c2{grid-template-columns:repeat(2,1fr)}
.defs svg.tex{vertical-align:middle}.defs>div{min-width:0}
.defs2{columns:3;column-gap:22px;margin:0;padding:6px 0 0 16px;border-top:1px solid var(--rule);font-size:11.5px;line-height:1.33;color:var(--ink2);flex:none}
.defs2 li{break-inside:avoid;margin:0 0 3px 0}
.eqtab.narroweq{grid-template-columns:76px 420px 1fr}
.defs2.one{columns:1;border-top:none;padding:0 0 0 16px;margin:0 0 3px 0;font-size:12px}.defs2 svg.tex{vertical-align:middle}
.defs2 .src{font-family:'IBM Plex Mono',Menlo,monospace;font-size:9.6px;color:var(--mute)}
.statusleg{font-size:11.5px;color:var(--mute);flex:none}
svg .brk{fill:none;stroke:#8a96a3;stroke-width:1.2}
.eqtab{display:grid;grid-template-columns:76px 520px 1fr;column-gap:16px;flex:none;border-top:1px solid var(--accent)}
.eqtab>div{border-bottom:1px solid var(--rule);padding:3px 0;display:flex;align-items:center;min-width:0}
.eqk{flex-direction:column;align-items:flex-start!important;justify-content:center;font-family:'IBM Plex Mono',Menlo,monospace;font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
.eqk span{color:var(--mute);letter-spacing:.04em;margin-top:2px}
.eqm{gap:18px}
.eqm.col{flex-direction:column;align-items:flex-start;justify-content:center;gap:3px}
.cover-deck .cover-sub2{max-width:760px;margin:0 0 30px 0}
.eqm svg.eqn{display:block;max-width:100%;height:auto}
.eqtab>div.eqg{display:block;align-self:stretch;font-size:12px;line-height:1.36;color:var(--ink2);padding:5px 0}
.eqcite{font-family:'IBM Plex Mono',Menlo,monospace;font-size:9.8px;color:var(--mute);margin-top:2px}
.eqk .eqpg{color:var(--accent);margin-top:3px;text-transform:none}
svg .pg{fill:var(--accent);font-family:'IBM Plex Mono',Menlo,monospace}
svg .fm{fill:var(--mute);font-family:'IBM Plex Sans',Arial,sans-serif}
/* diagram */
svg .node rect{fill:#fff;stroke:#9fb3c0;stroke-width:1.5}
svg .node .t{fill:var(--ink);font-weight:600;font-family:'IBM Plex Sans',Arial,sans-serif}
svg .node .s{fill:var(--mute);font-family:'IBM Plex Sans',Arial,sans-serif}
svg .node.pill rect{fill:#f3f7f9;stroke:#9fb3c0}
svg .node.pill .t{font-weight:500}
svg .node.hl rect{fill:var(--accent);stroke:var(--accent)}
svg .node.hl .t,svg .node.hl .s{fill:#fff}
svg .box rect{fill:#fff;stroke:#c7d3db;stroke-width:1.2;stroke-dasharray:4 3}
svg .box .bt{fill:var(--mute);font-family:'IBM Plex Mono',Menlo,monospace;letter-spacing:.08em}
svg .box.hl rect{stroke:var(--accent);stroke-dasharray:none}
svg .arr{fill:none;stroke:#7d8e9b;stroke-width:1.6}
svg .ahp{fill:#7d8e9b}
svg .f{fill:var(--ink2);font-family:'IBM Plex Sans',Arial,sans-serif}
svg .rl{stroke:var(--rule);stroke-width:1}
.chart{width:100%;height:auto}
.chart .grid{stroke:var(--rule);stroke-width:1}
.chart .ax{fill:var(--mute);font-family:'IBM Plex Mono',Menlo,monospace;font-size:11px}
.chart .b-read{fill:var(--accent)}.chart .b-write{fill:#b9c7d1}
.symleg{font-size:11.5px;line-height:1.45;color:var(--ink2);margin:0 2px;flex:none}
.symleg svg.tex{vertical-align:middle}
#help{position:fixed;right:12px;top:8px;font-family:'IBM Plex Mono',Menlo,monospace;font-size:11px;color:#c8d0d6;background:rgba(32,38,44,.85);padding:4px 10px;border-radius:10px;z-index:4;transition:opacity .6s}
#help.gone{opacity:0;pointer-events:none}
@media print{
  html,body{background:#fff;height:auto}
  #stage{position:static;transform:none!important;box-shadow:none;width:1280px;height:auto;left:0;top:0}
  .slide{display:flex;position:relative;page-break-after:always;break-after:page}
  #help{display:none!important}
  @page{size:1280px 720px;margin:0}
}

/* part 2 */
.fxbox{border:1px solid var(--rule);border-radius:4px;padding:5px 12px;display:flex;flex-direction:column;gap:3px;flex:none}
.fxrow{display:flex;align-items:center;flex-wrap:wrap;gap:4px;font-size:13px;color:var(--ink2)}
.fxrow svg.tex{vertical-align:middle}
.fp{display:inline-flex;align-items:center;gap:4px;border-radius:10px;padding:0 8px;border:1px solid transparent;font-size:11px}
.fp.good{background:var(--accent);border-color:var(--accent);color:#fff}
.fp.bad{background:#fbeede;border-color:#e2b98b;color:var(--warn)}
.fp.keep{border:1px dashed #9fb3c0;color:var(--ink2)}
.fp i{font-style:normal;font-family:'IBM Plex Mono',Menlo,monospace;font-size:11px;font-weight:600}
.fxleg{font-family:'IBM Plex Mono',Menlo,monospace;font-size:10px;color:var(--mute);display:flex;gap:6px;align-items:center;flex-wrap:wrap}
.fxleg .fp{font-size:10px;padding:0 7px}
.wcite{font-family:'IBM Plex Mono',Menlo,monospace;font-size:9.5px;color:var(--mute);margin-top:2px;font-weight:400;line-height:1.3}
.tbl.p2{font-size:11.8px;line-height:1.33}
.tbl.p2 td{padding:4px 7px 4px 5px}
.tbl.p2 td:first-child{font-family:inherit;font-size:12px;color:var(--ink)}
.tbl.p2.map td{padding:2px 7px 2px 5px}
.tbl.p2.price td{padding:2px 7px 2px 5px;font-size:11.5px}
.twocol{display:grid;grid-template-columns:1.55fr 1fr;gap:16px;align-items:start}
.appendix .tbl td:first-child b{color:var(--accent)}
.refs2 .reflist{font-size:10.4px;line-height:1.3}
"""

JS = r"""
(function(){
  const slides=[...document.querySelectorAll('.slide')];
  const stage=document.getElementById('stage');
  
  let cur=0, lastMain=0;
  function fit(){const s=Math.min(innerWidth/1280, innerHeight/720);stage.style.transform=`translate(-50%,-50%) scale(${s})`;stage.style.transformOrigin='center';stage.style.left='50%';stage.style.top='50%';}
  function show(i,push){i=Math.max(0,Math.min(slides.length-1,i));slides.forEach((s,k)=>s.classList.toggle('on',k===i));cur=i;if(!slides[i].classList.contains('appendix'))lastMain=i;if(push!==false){history.replaceState(null,'','#'+slides[i].id);}}
  function fromHash(){const h=location.hash.replace('#','');const i=slides.findIndex(s=>s.id===h);show(i<0?0:i,false);}
  addEventListener('resize',fit);
  addEventListener('hashchange',fromHash);
  addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' '){e.preventDefault();show(cur+1);}else if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();show(cur-1);}else if(e.key==='Home'){show(0);}else if(e.key==='End'){show(slides.length-1);}else if(e.key==='b'||e.key==='B'){show(lastMain);}});
  document.addEventListener('click',e=>{const a=e.target.closest('a');if(a){if(a.getAttribute('href')==='#back'){e.preventDefault();show(lastMain);}return;}show(cur+1);});
  fit();fromHash();setTimeout(()=>document.getElementById('help').classList.add('gone'),6000);
})();
"""

def render(font_dir=None):
    parts = ['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
             '<title>Agent acceleration</title>',
             '<style>', font_css(font_dir), CSS, '</style></head><body>',
             '<div id="stage">']
    main_n = {}
    for s in SLIDES:
        cls = "slide " + s["kind"]
        if s["kind"] in ("main", "refs"):
            main_n[s["part"]] = main_n.get(s["part"], 0) + 1
            label = f"AGENT ACCELERATION · PART {s['part']} · {main_n[s['part']]:02d}"
        elif s["kind"] == "title":
            label = ""
        else:
            label = f"AGENT ACCELERATION · PART {s['part']} · " + s["label"]
        parts.append(f'<section class="{cls}" id="{s["id"]}">')
        if s["cover"]:
            if label:
                parts.append(f'<div class="label">{label}</div>')
            parts.append(s["body"])
        else:
            parts.append(f'<div class="head"><div class="label">{label}</div><h1>{s["title"]}</h1></div>')
            if s["thumb"]:
                parts.append(f'<div class="thumb">{loop_svg(s["hl"])}</div>')
            parts.append('<div class="rule"></div>')
            if s["crumb"]:
                parts.append(f'<div class="crumb">{esc(s["crumb"])}</div>')
            parts.append('<div class="content">')
            if s["callout"]:
                parts.append(f'<div class="callout">{s["callout"]}</div>')
            parts.append(f'<div class="body">{s["body"]}</div></div>')
            if s["foot"]:
                parts.append(f'<div class="foot">{s["foot"]}</div>')
            if s["chip"]:
                parts.append(f'<a class="chip" href="{s["chip"][0]}">{esc(s["chip"][1])}{" ↗" if s["chip"][0] != "#back" else ""}</a>')
        if s["notes"]:
            parts.append(f'<aside class="notes" hidden>{esc(s["notes"])}</aside>')
        parts.append('</section>')
    parts.append('</div><div id="help">← → move · B back · #sNN links a page</div>')
    parts.append(f'<script>{JS}</script></body></html>')
    return "".join(parts)

def word_report():
    """Body words per slide, excluding citations in parentheses, the sources line and the references."""
    rows = []
    for s in SLIDES:
        if s["kind"] == "refs":
            continue
        text = s["callout"] + " " + s["body"]
        text = re.sub(r"<svg.*?</svg>", " ", text, flags=re.S)
        text = re.sub(r'<div class="(?:eqcite|cc|wcite)">.*?</div>', " ", text, flags=re.S)
        text = re.sub(r'<span class="src">.*?</span>', " ", text, flags=re.S)   # symbol origins are citations too   # source lines are citations, not counted
        text = re.sub(r"<[^>]+>", " ", text)
        text = html.unescape(text)
        text = re.sub(r"\([^()]*\d{4}[a-z]?(;[^()]*\d{4}[a-z]?)*\)", " ", text)   # (Author, 2026; ...) citations
        words = re.findall(r"[A-Za-z0-9$%€.,'’/×–\-]+", text)
        rows.append((s["id"], len(words)))
    return rows

if __name__ == "__main__":
    font_dir = None
    if "--fonts" in sys.argv:
        font_dir = sys.argv[sys.argv.index("--fonts") + 1]
    out = render(font_dir)
    open(OUT, "w", encoding="utf-8").write(out)
    print(f"wrote {OUT} ({len(out)/1024:.0f} KB, {len(SLIDES)} slides)")
    for id_, n in word_report():
        print(f"  {id_:6s} {n:4d} words")
