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
    # top band: calls per pass (set by the harness); overlap
    p.append(mpill("n-calls", 240, 2, 196, 24, r"c_k\ \mathrm{calls\ in\ pass}\ k", 15))
    p.append(arrow(338, 26, 338, 34))
    if big:
        p.append(txt(480, 19, "set by the harness — the program around the model", 12.5, "start", "f"))
    p.append(mpill("n-overlap", 916, 2, 280, 24, r"T_{\mathrm{saving}}\ \mathrm{=\ time\ saved\ by\ overlap}", 14))
    # main row
    p.append(node("n-observe", 14, 46, 128, 72, "Observe", "screenshot · page text", r"t_{\mathrm{obs}}"))
    p.append(arrow(142, 82, 160, 82))
    c = " hl" if "n-decide" in hl else ""
    p.append(f'<g id="{mid}-n-decide" class="box{c}"><rect x="160" y="34" width="570" height="92" rx="8"/>'
             f'<text class="bt" x="172" y="50" font-size="12">DECIDE · one model call</text></g>')
    p.append(pill("n-queue", 172, 58, 90, 28, "queue", 13.5))
    p.append(pill("n-read", 272, 58, 206, 28, "read the prompt, all at once", 13))
    p.append(pill("n-write", 488, 58, 230, 28, "write the answer, token by token", 13))
    p.append(m(r"t_{\mathrm{queue}}", 217, 106, 14))
    p.append(m(r"t_{\mathrm{read}}(R-R^{\mathrm{hit}})", 375, 106, 14))
    p.append(m(r"t_{\mathrm{write}}(W)", 603, 106, 14))
    p.append(arrow(730, 82, 748, 82))
    p.append(node("n-act", 748, 46, 122, 72, "Act", "click · type · run a tool", r"t_{\mathrm{act}}"))
    p.append(arrow(870, 82, 886, 82))
    p.append(node("n-wait", 886, 46, 146, 72, "Wait", "page load · sleep · tool run", r"t_{\mathrm{wait}}"))
    # exit: the agent stops (it says it is done, or hits the step cap); success is judged once, afterwards
    p.append(arrow(1032, 82, 1084, 82))
    p.append(txt(1066, 76, "stop", 10.5))
    p.append(node("n-succ", 1084, 46, 112, 72, "End", "judged afterwards", r"\Pr[\mathrm{success}]"))
    # token and price band
    p.append(m(r"o_k\ \mathrm{tokens}", 78, 146, 14))
    p.append(arrow(120, 146, 270, 146))
    p.append(mpill("n-rtok", 272, 134, 206, 24, r"R\ \mathrm{read}:\ R^{\mathrm{hit}}\ \mathrm{from\ cache}"))
    p.append(mpill("n-wtok", 488, 134, 118, 24, r"W\ \mathrm{written}"))
    p.append(mpill("n-price", 614, 134, 104, 24, r"\times\ p\ \mathrm{prices}"))
    p.append(mpill("n-machine", 886, 134, 146, 24, r"\tau\ \mathrm{machine\ hours}"))
    # loop back: not stopped -> next pass
    p.append(f'<path class="arr" d="M1058 82 L1058 180 L6 180 L6 82 L12 82" marker-end="url(#{mid})"/>')
    p.append(txt(1064, 172, "else", 10.5, "start"))
    p.append(mpill("n-steps", 272, 168, 150, 24, r"\times\ N\ \mathrm{passes}", 15))
    p.append(mpill("", 480, 168, 330, 24, r"\mathrm{next\ prompt:}\ \ R_{k+1} \approx R_k + W_k + o_{k+1}"))
    p.append("</svg>")
    return "".join(p)

# ---------------------------------------------------------------- formulas (LaTeX-style, typeset at build time)
# Everything mathematical on the pages — the two equations and every variable such as N, c_k, R_k — is typeset with
# matplotlib's mathtext (Computer Modern) into inline SVG, so the deck stays self-contained (no KaTeX at runtime).
EQ = {
 "time":  r"$T_{\mathrm{task}} \;=\; \sum_{k=1}^{N}\left[\,\sum_{j=1}^{c_k}\ell_{kj} + t_{\mathrm{obs}} + t_{\mathrm{act}} + t_{\mathrm{wait}}\right] \;-\; T_{\mathrm{saving}}$",
 "call":  r"$\ell_{kj} \;=\; t_{\mathrm{queue}} + t_{\mathrm{read}}(R_{kj} - R^{\mathrm{hit}}_{kj}) + t_{\mathrm{write}}(W_{kj}), \qquad T_{\mathrm{saving}} \,\geq\, 0$",
 "ctx":   r"$R_{k+1} \;\approx\; R_k + W_k + o_{k+1} \quad\Rightarrow\quad \sum_{k=1}^{N} R_k \;\approx\; N R_1 + \dfrac{N(N-1)}{2}\,(\bar{w} + \bar{o})$",
 "money": r"$\mathrm{Cost}_{\mathrm{task}} \;=\; \sum_{k,j}\left(R^{\mathrm{hit}} p_{\mathrm{hit}} + R^{\mathrm{miss}} p_{\mathrm{miss}} + R^{\mathrm{store}} p_{\mathrm{store}} + W p_{\mathrm{write}}\right) \;+\; \tau\, p_{\mathrm{env}}$",
 "succ":  r"$\mathrm{Cost}_{\mathrm{success}} \;=\; \dfrac{\mathbb{E}[\mathrm{Cost}_{\mathrm{task}}]}{\Pr[\mathrm{success}]}$",
 "goal":  r"$\min\ \left(\mathbb{E}[T_{\mathrm{task}}],\ \mathrm{Cost}_{\mathrm{success}}\right)\quad \mathrm{s.t.}\quad \Pr[\mathrm{success}] \,\geq\, s_0$",
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
    """The time equation with the five classes of slowness mapped onto its terms (page 3)."""
    terms = [(tex(r"\sum_{k}", 15), "I · passes"), (tex(r"\sum_{j \leq c_k}", 15), "II · calls per pass"),
             (tex(r"(t_{\mathrm{queue}} + t_{\mathrm{read}} + t_{\mathrm{write}})", 15), "III · each call"),
             (tex(r"+\ t_{\mathrm{obs}} + t_{\mathrm{act}} + t_{\mathrm{wait}}", 15), "IV · environment"),
             (tex(r"-\ T_{\mathrm{saving}},\ \ T_{\mathrm{saving}} \approx 0", 15), "V · serial: little overlaps")]
    s = ['<div class="eqstrip"><div class="eqt">' + tex(r"T_{\mathrm{task}} =", 15) + '</div>']
    for t, c in terms:
        s.append(f'<div class="eqterm"><div class="eqx">{t}</div><div class="eqc">{html.escape(c)}</div></div>')
    return "".join(s) + "</div>"

def cost_strip():
    """The money equation with the six classes of cost mapped onto its terms (page 7)."""
    terms = [(tex(r"\sum_{k}\sum_{j \leq c_k}", 15), "3 · number of calls"),
             (tex(r"(\,R^{\mathrm{hit}}, R^{\mathrm{miss}}, R^{\mathrm{store}}", 15), "1 · tokens read"),
             (tex(r",\ W\,)", 15), "2 · tokens written"), (tex(r"\cdot\ p", 15), "5 · price per class"),
             (tex(r"+\ \tau\,p_{\mathrm{env}}", 15), "6 · environment"),
             (tex(r"\div\ \Pr[\mathrm{success}]", 15), "4 · failures, retries")]
    out = ['<div class="eqstrip"><div class="eqt">' + tex(r"\mathrm{Cost}_{\mathrm{success}} \approx", 15) + '</div>']
    for t, c in terms:
        out.append(f'<div class="eqterm"><div class="eqx">{t}</div><div class="eqc">{html.escape(c)}</div></div>')
    return "".join(out) + "</div>"

def link_fig():
    """Two equations with terms coloured by their relationship (page 16)."""
    def pill(src, kind):
        col = "#ffffff" if kind == "same" else ("#b3600c" if kind == "buy" else "#3d4b58")
        return f'<span class="lp {kind}">{tex(src, 13, color=col)}</span>'
    def op(src):
        return tex(src, 13)
    t = [pill(r"\sum_{k}","same"), pill(r"\sum_{j}","same"), op(r"("), pill(r"t_{\mathrm{queue}}","time"), op("+"), pill(r"t_{\mathrm{read}}(R-R^{\mathrm{hit}})","same"), op("+"), pill(r"t_{\mathrm{write}}(W)","same"), op(r")\ +"), pill(r"t_{\mathrm{obs}}","time"), op("+"), pill(r"t_{\mathrm{act}}","time"), op("+"), pill(r"t_{\mathrm{wait}}","time"), op("-"), pill(r"T_{\mathrm{saving}}","time")]
    m = [pill(r"\sum_{k}","same"), pill(r"\sum_{j}","same"), op(r"("), pill(r"R^{\mathrm{hit}}","same"), pill(r"p_{\mathrm{hit}}","buy"), op("+"), pill(r"R^{\mathrm{miss}}","same"), pill(r"p_{\mathrm{miss}}","buy"), op("+"), pill(r"R^{\mathrm{store}}","same"), pill(r"p_{\mathrm{store}}","buy"), op("+"), pill(r"W","same"), pill(r"p_{\mathrm{write}}","buy"), op(r")\ +"), pill(r"\tau","time"), pill(r"p_{\mathrm{env}}","buy"), op(r"\div"), pill(r"\Pr[\mathrm{success}]","same")]
    return ('<div class="linkfig"><div class="lrow"><span class="lk">time</span>' + " ".join(t) + '</div>'
            '<div class="lrow"><span class="lk">money</span>' + " ".join(m) + '</div>'
            '<div class="lleg"><span class="lp same">in both equations — same source</span><span class="lp time">no tokens, money only as machine hours — slow but not expensive</span><span class="lp buy">the price — money for time or accuracy</span></div></div>')


def symleg(parts):
    """One line under an equation strip: every symbol in it, briefly."""
    return '<div class="symleg">' + " · ".join(tex(a, 11) + " " + html.escape(b) for a, b in parts) + "</div>"
SYM_TIME = [(r"N", "passes per task"), (r"c_k", "model calls in pass k"), (r"t_{\mathrm{queue}}, t_{\mathrm{read}}, t_{\mathrm{write}}", "one call: queueing, reading the prompt (prefill), writing the answer (decode)"),
            (r"t_{\mathrm{obs}}, t_{\mathrm{act}}, t_{\mathrm{wait}}", "observe, act, wait"), (r"T_{\mathrm{saving}}", "time saved by running steps at the same time")]
SYM_COST = [(r"k, j", "pass, call"), (r"R^{\mathrm{hit}}, R^{\mathrm{miss}}, R^{\mathrm{store}}", "prompt tokens from the cache, not in it, stored into it"), (r"W", "written tokens"),
            (r"p", "price per token of each class"), (r"\tau\,p_{\mathrm{env}}", "machine hours × hourly price"), (r"\Pr[\mathrm{success}]", "success rate")]
SYM_LINK = [(r"\Sigma_k, \Sigma_j", "over passes, over calls")] + SYM_TIME[2:] + SYM_COST[1:]

SLIDES = []   # dicts: id, label, title, hl, crumb, callout(html), body(html), foot, chip(href,text), notes, kind

def slide(id_, title, body, *, label=None, hl=(), crumb="", callout="", foot="", chip=None, notes="", kind="main", cover=False, thumb=True):
    SLIDES.append(dict(id=id_, title=title, body=body, label=label, hl=hl, crumb=crumb, callout=callout,
                       foot=foot, chip=chip, notes=notes, kind=kind, cover=cover, thumb=thumb))

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
    "meta": "Meta, 2026",
    "openai25": "OpenAI, 2025",
    "llmc": "Kim et al., 2024",
    "tokenpilot": "Xu et al., 2026",
    "cop": "Erol et al., 2026",
    "asyncfc": "Feng et al., 2026",
    "frugal": "Chen, Zaharia &amp; Zou, 2024",
    "agentix": "Luo et al., 2026",
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
      <li><span>02</span>The agent loop and the variables at each step</li>
      <li><span>03–06</span>Where the time goes: five sources, and which one dominates</li>
      <li><span>07–08</span>Where the money goes: six sources, and four accounting conventions</li>
      <li><span>09–10</span>How time and money are linked, and the levers</li>
      <li><span>11–12</span>References · Appendix A0–A6</li>
    </ol>
  </div>
</div>""")

# --- 02 the loop, the variable at each step, and how they add up -------------------
def eqrow(key, sub, eqs, gloss, cite, pg, stack=False):
    eqhtml = "".join(eq_svg(e, fontsize=10, cls="eqn") for e in eqs)
    return (f'<div class="eqk">{key}<span>{sub}</span><span class="eqpg">{pg}</span></div><div class="eqm{" col" if stack else ""}">{eqhtml}</div>'
            f'<div class="eqg"><div>{gloss}</div><div class="eqcite">{cite}</div></div>')

slide("s02", "The agent loop and the variables at each step", thumb=False,
      crumb="here: the steps of one pass, the variable at each step, and how the variables add up to time and cost → to: the five sources of slowness",
      body=f"""
<div class="fig-loop2">{loop_svg(cls="big-svg", big=True)}</div>
<div class="eqtab">
{eqrow("time", "elapsed", ["time", "call"],
       "Time of one attempt" + tex(r"T_{\mathrm{task}}", 11) + ": pass " + tex(r"k", 11) + " runs from 1 to " + tex(r"N", 11) + ", call " + tex(r"j", 11) + " from 1 to " + tex(r"c_k", 11) + ". " + tex(r"\ell_{kj}", 11) + " is one call: queueing, reading the prompt tokens not in the cache (" + tex(r"R - R^{\mathrm{hit}}", 11) + ", prefill) and writing its " + tex(r"W", 11) + " tokens (decode). " + tex(r"t_{\mathrm{obs}}, t_{\mathrm{act}}, t_{\mathrm{wait}}", 11) + ": observe, act, wait. " + tex(r"T_{\mathrm{saving}}", 11) + ": time saved by running steps at the same time; 0 if all serial.",
       "serial form: " + CITE['llmc'] + " · overlap: " + CITE['asyncfc'] + " · per-call split: " + CITE['tracelab'], "p. 3–6", stack=True)}
{eqrow("prompt", "grows", ["ctx"],
       tex(r"R_k", 11) + ": prompt tokens of pass " + tex(r"k", 11) + " (" + tex(r"R_1", 11) + ": system prompt and task). Each prompt adds the answer " + tex(r"W_k", 11) + " and the next observation " + tex(r"o_{k+1}", 11) + "; " + tex(r"\bar{w}, \bar{o}", 11) + ": their means per pass. So reading grows with " + tex(r"N^2", 11) + " (calc.); measured on 39 OSWorld tasks: cost “grows quadratically with the number of steps”.",
       "recurrence: " + CITE['yuan'] + " · measured, GTA1 harness: " + CITE['osh'], "p. 5, 7")}
{eqrow("money", "per attempt", ["money"],
       "Prompt tokens by billing class: " + tex(r"R^{\mathrm{hit}}", 11) + " read from the cache, " + tex(r"R^{\mathrm{miss}}", 11) + " not in it, " + tex(r"R^{\mathrm{store}}", 11) + " stored into it; " + tex(r"W", 11) + " written tokens, thinking included; each " + tex(r"p", 11) + " is the price per token of its class. " + tex(r"\tau", 11) + ": hours the environment machine is billed (" + tex(r"\tau \geq T_{\mathrm{task}}", 11) + "); " + tex(r"p_{\mathrm{env}}", 11) + ": its hourly price.",
       CITE['anth-b'] + "; " + CITE['openai'] + " · cached vs new: " + CITE['tracelab'] + " · machine: page 8", "p. 7–8")}
{eqrow("success", "and goal", ["succ", "goal"],
       tex(r"\mathbb{E}[\cdot]", 11) + ": mean over attempts; " + tex(r"\Pr[\mathrm{success}]", 11) + ": chance that one attempt succeeds. Failed attempts are billed, so cost per success = mean cost per attempt ÷ success rate. Goal: lower time or cost per success without raising the other, keeping the success rate at least " + tex(r"s_0", 11) + ", its level before the change.",
       "cost per success: " + CITE['cop'] + " (per task; the benchmark average is ours) · goal: ours", "p. 7–10")}
</div>""",
      foot="SOURCES · as cited in each row · simplified: times are means, not distributions; cache expiry and per-call fees left out — Appendix A0",
      chip=("#a0-1", "Appendix A0"))

# --- 03 five sources ------------------------------------------------------
slide("s03", "Slowness has five sources",
      hl=("n-steps", "n-calls", "n-queue", "n-read", "n-write", "n-observe", "n-act", "n-wait", "n-overlap"),
      crumb="from the time equation → here: every cause of slowness, in five classes → to: the numbers behind each class",
      callout=f"""<p><b>Four of the five are terms of the time equation; the fifth is how they combine: the overlap term {tex(r"T_{\mathrm{saving}}", 15)} is close to zero, so the terms add.</b> Which class dominates depends on the harness, not on the kind of agent (page 6). Cause-by-cause tables with measurement conditions: Appendix A1.</p>""",
      body=f"""
{eq_strip()}
{symleg(SYM_TIME)}
<div class="rows5 big">
  {card("I · TOO MANY PASSES " + tex("(N)", 11), "Hour-scale tasks take hundreds of passes, and every pass is a full round trip",
        ["318 tool calls per task on OSWorld 2.0 — 108 desktop tasks, Claude Opus 4.7, one action per step"], ci('osw2'))}
  {card("II · TOO MANY CALLS PER PASS " + tex("(c_k)", 11), "A harness that plans, judges and reflects multiplies every pass",
        ["4–12 planning calls per judging call — GTA1 harness: four parallel planners, up to three retries, one judge"], ci('osh'))}
  {card("III · EACH CALL IS SLOW", "Inside a call, waiting, reading and writing are three separate delays",
        ["Writing, one token at a time, is 91–98.6% of model time — local 27–31B models with a warm cache"], ci('yuan'))}
  {card("IV · THE ENVIRONMENT IS SLOW", "The environment costs time whether or not the model is running",
        ["6.6 s per browser action vs 4.7 s per model call, median — 151 WebVoyager live-site tasks, GPT-4o"], ci('skim'))}
  {card("V · EVERYTHING IS SERIAL", "Almost nothing overlaps, so task time is close to a sum: fixing one term saves only its own share",
        ["Concurrency within a turn: 1.15 — GitHub Copilot production telemetry"], ci('copilot'))}
</div>""",
      foot="SOURCES · one representative number per class; conditions on the next two pages and in Appendix A1",
      chip=("#a1-1", "Appendix A1"))

# --- 04 classes I–II ----------------------------------------------------------
slide("s04", "I–II · Too many passes, too many calls per pass",
      hl=("n-steps", "n-calls"),
      crumb="from the five classes → here: the two multipliers, passes and calls per pass → to: what happens inside a call and around it",
      callout=f"""<p><b>{tex("N", 15)} multiplies every term and {tex("c_k", 15)} multiplies {tex("N", 15)}.</b> Passes accumulate because tasks are long, each pass does one action, navigation-only passes still go through the model, and the agent idles or loops; calls accumulate because the harness plans, judges and reflects, or samples several candidates per step.</p>""",
      body=f"""
<div class="cards4">
  {card("I-1, I-2 · LONG TASKS, ONE ACTION PER PASS", "Long tasks with one action per pass need hundreds of passes; several actions per call cut them by half or more",
        ["318 tool calls per task with one action per step, 160.7 with several actions per call — OSWorld 2.0, 108 long tasks, Claude Opus 4.7"], ci('osw2'))}
  {card("I-3 · NAVIGATION-ONLY PASSES", "Most passes are navigation that needs no thinking, yet each one is a model call",
        ["66.7% of the steps in the median task are pure navigation — 151 WebVoyager tasks on live websites, three text agents driven by GPT-4o"], ci('skim'))}
  {card("I-4 · IDLING AND DEAD LOOPS", "When an agent is stuck, every repeated pass is billed and timed in full",
        ["One element-locating loop repeated a step 18 times: 27 minutes and $8.47 at list price without caching — GTA1 harness, OSWorld"], ci('osh'))}
  {card("II · PLANNING, JUDGING, SAMPLING", "Extra calls per pass buy accuracy at a rising token cost per point",
        ["10 candidates per step instead of 1: 38.8% → 43.2% success for 96K → 920K tokens per task — gpt-oss-120b, 165 WebArena-Lite tasks"], ci('atts'))}
</div>
<div class="figs1">
  {hbars("Steps per task on OSWorld 2.0, 108 tasks", [("Opus 4.7 · one action per step",318,"318"),("Opus 4.7 · batched actions",160.7,"160.7"),("Opus 4.8 · batched",103,"103"),("GPT-5.5 · batched",95.2,"95.2")], "XLANG Lab, 2026 · mean over tasks", width=600)}
</div>""",
      foot=f"SOURCES · {CITE['osw2']} · {CITE['skim']} · {CITE['osh']} · {CITE['atts']} — full rows with conditions in Appendix A1",
      chip=("#a1-1", "Appendix A1"))

# --- 05 classes III–V --------------------------------------------------------
slide("s05", "III–V · Inside a call, around it, and in sequence",
      hl=("n-queue", "n-read", "n-write", "n-observe", "n-act", "n-wait", "n-overlap"),
      crumb="from the multipliers → here: the per-call and per-pass terms → to: which term dominates",
      callout="""<p><b>Inside a call: queueing, reading, writing. Around it: observation, execution, fixed sleeps, tool runs.</b> All of it runs strictly in sequence, so task time is the sum, not the largest term.</p>""",
      body=f"""
<div class="cards4">
  {card("III-1, III-2 · QUEUEING AND READING", "Before a single token is written, the call has waited in a queue and re-read the whole history",
        ["Identical requests take up to 69× longer depending on the time of day — 15 models, 5 providers"], ci('bian'))}
  {card("III-3, III-4 · WRITING AND THINKING", "Writing is the slowest segment per token, and thinking modes write far more tokens without reliably buying accuracy",
        ["224K vs 37K output tokens per task — Claude Opus 4.8 vs GPT-5.5 on the same 108 OSWorld 2.0 tasks"], ci('osw2'))}
  {card("IV · THE ENVIRONMENT", "The environment is slow on its own, and the benchmarks add fixed sleeps on top",
        ["OSWorld 2.0 sleeps 3 s after every action: × 318 steps ≈ 16 min of pure waiting per task (calc.)"], ci('osw2','code'))}
  {card("V · SERIAL", "Nothing overlaps, so task time is a sum — and a “total time” often includes the human",
        ["80–92% of a coding session’s elapsed time is the person thinking between turns — GitHub Copilot telemetry (median) and 4,265 Claude Code / Codex sessions"], ci('copilot','tracelab'))}
</div>
<div class="figs1">
  {hbars("Where a Claude Code / Codex request’s 4.3 minutes go", [("tools",59.8,"59.8%"),("model",41.0,"41.0%")], "Zhu et al., 2026 · 4,265 sessions, 43 developers", maxv=100, width=600, labelw=60)}
</div>""",
      foot=f"SOURCES · {CITE['bian']} · {CITE['osw2']} · {CITE['code']} · {CITE['tracelab']} · {CITE['copilot']} — full rows with conditions in Appendix A1",
      chip=("#a1-2", "Appendix A1"))

# --- 06 harness decides -------------------------------------------------------
slide("s06", "Which term dominates depends on the harness, not on the kind of agent",
      hl=("n-read", "n-wait", "n-write"),
      crumb="from the five classes → here: the shares, per kind of agent → to: the six sources of cost",
      callout=f"""<p><b>All five classes exist in every agent; the heaviest term differs, and it flips when the harness changes.</b> The one multiplier common to all three kinds is the number of passes, {tex("N", 15)}.</p>""",
      body=f"""
<table class="tbl three">
<colgroup><col style="width:10%"><col style="width:30%"><col style="width:30%"><col style="width:30%"></colgroup>
<thead><tr><th></th><th>Screenshot desktop agent, multi-call harness</th><th>Text web agent</th><th>Coding agent with a prompt cache</th></tr></thead>
<tbody>
<tr><td class="rk">heaviest</td>
<td><b>Reading × calls per pass × passes.</b> 87–97% of task time is planning, judging and reflection calls (GTA1, Agent S2; 39 OSWorld tasks) {ci('osh')}</td>
<td><b>Browser execution and waiting.</b> Per step, median: browser 6.6 s, model 4.7 s (151 WebVoyager live-site tasks, GPT-4o) {ci('skim')}</td>
<td><b>Writing, or tool tails.</b> Writing is 91–98.6% of model time {ci('yuan')}; in Claude Code / Codex requests tools take 59.8%, the model 41.0% {ci('tracelab')}</td></tr>
<tr><td class="rk">flips when</td>
<td>The harness makes one call per pass: over 70% of the time is then the sandbox, because the benchmark sleeps 2–3 s after every action {ci('asb','code','osw2')}</td>
<td>The observation grows: 4.8× the input moved the model’s share of step time from 46.9% to 61.6% {ci('asb')}</td>
<td>Load evicts the cache: latency up to 7.14× {ci('thunder')}; or the tools are light and the model dominates again (Copilot)</td></tr>
<tr><td class="rk">in one line</td>
<td>Slow in reading: every pass re-reads the growing screenshot history</td>
<td>Slow in the environment — until the observation grows, then slow in reading</td>
<td>Reading is cached away; slow in writing and in the tools</td></tr>
</tbody></table>
<div class="concl">
  <div><b>1 · The harness sets the dominant term</b> — calls per pass, observation size, fixed sleeps, cache on or off. The explanation “agents are slow because inference is slow” is accurate only for multi-call screenshot agents.</div>
  <div><b>2 · {tex("N", 14)} multiplies every term</b> — one pass fewer saves a whole pass of time and money in all three kinds; OSWorld 2.0’s authors list “fewer environment rounds” as a goal in its own right.</div>
</div>""",
      foot="SOURCES · as cited in each cell; the same table with every measurement condition is Appendix A2",
      chip=("#a2-1", "Appendix A2"))

# --- 07 six sources of cost ------------------------------------------------------
slide("s07", "Cost has six sources",
      hl=("n-rtok", "n-wtok", "n-price", "n-succ", "n-calls", "n-steps", "n-machine"),
      crumb="from where the time goes → here: every cause of cost, in six classes → to: four accounting conventions, and the environment machine",
      callout=f"""<p><b>Money comes from two things only — tokens read and tokens written, each times a price.</b> Writing costs 5× reading; a cached read costs a small fraction of a normal read (DeepSeek-V4.1-Flash: $0.006 vs $0.30 per million tokens; other vendors in Appendix A3); fast mode costs 2× {ci('anth-b','openai','deepseek')}.</p>""",
      body=f"""
{cost_strip()}
{symleg(SYM_COST)}
<div class="rows6">
  {card("1 · TOKENS READ", "Reading is the larger bill, it grows with the square of the passes, and caching does not remove it",
        ["Even at a 95.7% cache hit rate, prefix tokens are still 59.5% of the bill — 4,265 Claude Code / Codex sessions"], ci('tracelab'))}
  {card("2 · TOKENS WRITTEN", "Writing is the dearer token and thinking is billed as writing — but it is not the larger bill",
        ["31% of an uncached screenshot agent’s bill: $2.43 counting output only vs $7.87 counting all tokens — GTA1, 39 OSWorld tasks (calc.)"], ci('osh'))}
  {card("3 · NUMBER OF CALLS", "The calls that made the agent slow are the same calls that make it expensive",
        ["5–13× the calls of a single-call harness per step — GTA1: planners, retries and a judge (calc.)"], ci('osh'))}
  {card("4 · FAILURES AND RETRIES", "What a task costs is what a success costs, and failed attempts are billed in full",
        ["$72.4 per attempt ÷ 20.6% completion ≈ $351 per success — OSWorld 2.0, best agent (calc.)"], ci('osw2'))}
  {card("5 · UNIT PRICE", "The price list sets the constant; speed tiers and long contexts double it",
        ["Claude Opus 5.5 $4 / $20 vs GPT-6 Luna $0.10 / $0.50 per million tokens read / written — a 40× spread between two vendors’ list prices (calc.)"], ci('anth-b','openai'))}
  {card("6 · THE ENVIRONMENT MACHINE", "Published task costs are API bills only; a CPU environment adds a small amount on top",
        ["A one-hour CPU environment costs $0.02–0.36 at list prices: 0.3–4.6% of a $7.87 bill (calc.; next page)"], "vendor price pages, read 2026-09-27")}
</div>""",
      foot="SOURCES · one representative number per class; the complete tables with conditions are in Appendix A3",
      chip=("#a3-1", "Appendix A3"))

# --- 08 conventions + machines ----------------------------------------------------
slide("s08", "Four accounting conventions for one task, and the cost of the environment machine",
      hl=("n-price", "n-succ", "n-machine"),
      crumb="from the six classes → here: which convention a cost figure uses, and what the environment adds → to: how slow and expensive are linked",
      callout="""<p><b>The cost of one task depends on the accounting convention: the four conventions in use differ by up to 30×, and none includes the environment machine.</b> A cost figure is comparable only with its convention stated.</p>""",
      body=f"""
<div class="two">
  <div>
  <table class="tbl conv">
  <colgroup><col style="width:30%"><col style="width:55%"><col style="width:15%"></colgroup>
  <thead><tr><th>convention</th><th>the same run, counted both ways</th><th>gap</th></tr></thead>
  <tbody>
  <tr><td class="rk">output only vs all tokens</td><td>GTA1 on 39 OSWorld tasks, o3 list price, no cache: $2.43 counting output only; $7.87 counting all tokens {ci('osh')}</td><td>3.2×</td></tr>
  <tr><td class="rk">per attempt vs per success</td><td>OSWorld 2.0, Claude Opus 4.8: $72.4 per attempt at 20.6% completion → ≈ $351 (calc.; a benchmark average, not the cost of retrying one given task) {ci('osw2')}</td><td>4.9×</td></tr>
  <tr><td class="rk">uncached vs cached</td><td>A cached read costs a fraction of a normal read (DeepSeek-V4.1-Flash: $0.006 vs $0.30 per million tokens; other vendors in A3); but at a 95.7% hit rate, prefix tokens were still 59.5% of the bill (4,265 Claude Code / Codex sessions) {ci('deepseek','tracelab')}</td><td>4–50× on the read price only, by vendor (calc.)</td></tr>
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
      foot=f"SOURCES · {CITE['osh']} · {CITE['osw2']} · {CITE['tracelab']} · {CITE['anth-b']} · {CITE['openai']} · {CITE['deepseek']} · AWS, Browser Use, Browserbase, E2B, Daytona, Modal, OpenAI price pages",
      chip=("#a3-3", "Appendix A3"))

# --- 09 how they link ---------------------------------------------------------------
slide("s09", "How slow and expensive are linked: three kinds of relationship",
      hl=("n-rtok", "n-wtok", "n-queue", "n-wait", "n-machine"),
      crumb="from the two bills → here: what each cause does to time and to money → to: the levers",
      callout="""<p><b>The two equations share the read and write tokens; environment time and queueing reach the money equation only through the environment machine’s hours.</b> So every cause relates to time and money in exactly one of three ways.</p>""",
      body=f"""
{link_fig()}
{symleg(SYM_LINK)}
<div class="cards3 rel">
  {card("SAME SOURCE — in both equations", "fix it, and time and money fall together",
        ["Passes " + tex("N", 13) + ", calls per pass " + tex("c_k", 13) + ", reading, writing, cache hits, failures — every one of them lives in the token counts"], ci('osh','anth-b'))}
  {card("SLOW BUT NOT EXPENSIVE — no tokens, only machine hours", "fix it, and only time falls",
        ["Queueing, page loads, fixed sleeps, tool tails — none produces a token; the machine behind them is billed by the hour, usually under 5% of the API bill"])}
  {card("MONEY FOR TIME OR FOR ACCURACY — opposite signs", "paying for speed shortens only the writing segment; paying for accuracy costs more tokens per point as accuracy rises",
        ["Fast mode: up to 2.5× faster writing (vendor-stated) at 2× the price, reading unchanged"], "(" + CITE['anth-b'] + "; " + CITE['openai'] + "; accuracy: Appendix A5)")}
</div>""",
      foot=f"SOURCES · {CITE['osh']} · {CITE['anth-b']} · {CITE['openai']} — the cause-by-cause table, with the convexity evidence, is Appendix A5",
      chip=("#a5-1", "Appendix A5"))

# --- 10 levers + gaps ---------------------------------------------------------------
slide("s10", "The levers, and what is still unmeasured",
      hl=("n-steps", "n-calls", "n-read", "n-write", "n-wait", "n-price", "n-overlap"),
      crumb="from the three relationships → here: what fixing each lever buys, and the holes in the evidence → to: Part 2, what the literature has done with each lever",
      callout="""<p><b>Seven levers follow from the equations; each saves a known term and carries a known risk.</b> Part 2 asks how far the literature has pushed each one. On the right: what no measurement has settled — gaps in the evidence, not claims of a research gap.</p>""",
      body=f"""
<div class="levgrid">
  <table class="tbl lev">
  <colgroup><col style="width:40%"><col style="width:12%"><col style="width:18%"><col style="width:30%"></colgroup>
  <thead><tr><th>lever</th><th>time</th><th>money</th><th>the catch</th></tr></thead>
  <tbody>
  <tr><td><b>Fewer passes</b> — several actions per call, skip navigation-only steps</td><td>yes</td><td>yes, the quadratic term</td><td>which steps need no thinking?</td></tr>
  <tr><td><b>Read less</b> — trim history, shrink screenshots, cache the prefix</td><td>yes</td><td>yes</td><td>forgets; trimming invalidates the cache</td></tr>
  <tr><td><b>Write less</b> — less thinking, smaller model</td><td>yes</td><td>yes</td><td>accuracy may fall</td></tr>
  <tr><td><b>Fewer calls per pass</b> — drop judging and reflection</td><td>yes</td><td>yes</td><td>fewer errors caught</td></tr>
  <tr><td><b>Overlap the waiting</b> — pre-load, parallel tools, page-ready events</td><td>yes</td><td>no</td><td>only where the environment dominates</td></tr>
  <tr><td><b>Buy a fast or priority tier</b></td><td>writing only</td><td>no — 2× more</td><td>reading unchanged; cache dropped</td></tr>
  <tr><td><b>Stop retrying failures</b> — early stop, detect dead loops</td><td>yes</td><td>yes</td><td>stops some attempts that would have succeeded</td></tr>
  </tbody></table>
  <div class="gapcol">
    <div class="ck">NOT YET MEASURED</div>
    <ul>
      <li><b>Read / write time split and cache hit rate for a frontier API model</b> — the only split is on local 27–31B models {ci('yuan')}; screenshot-agent measurements do not report cache state.</li>
      <li><b>How much slower than a person</b> — no benchmark times agent and human on the same tasks; the closest, AXIS’s small user study, has a UI agent 1.69× slower than manual work on easy tasks {ci('axis')}.</li>
      <li><b>Whether the benchmark’s fixed sleep sits inside “action” time</b> in OSWorld-Human — if so, “environment under 3.5%” understates the waiting.</li>
      <li><b>How much slowness costs accuracy</b> — OSWorld 2.0 records the stale-screen failure mode without its share {ci('osw2')}; the rebound from a smaller model has no direct evidence.</li>
    </ul>
  </div>
</div>""",
      foot=f"SOURCES · levers derived from the equations on page 2 · gaps: {CITE['yuan']} · {CITE['axis']} · {CITE['osw2']} · Appendix A5 and A6",
      chip=("#a5-1", "Appendix A5"))

# --- references (part 1) ---------------------------------------------------
REFS_P1 = [
 "Abhyankar, R., Qi, Q., &amp; Zhang, Y. (2026). OSWorld-Human: Benchmarking the efficiency of computer-use agents. <i>Proceedings of the 9th Conference on Machine Learning and Systems (MLSys 2026)</i>. arXiv:2506.16042. University of California, San Diego.",
 "Anthropic. (2026a, May 13). <i>Best practices for computer and browser use with Claude</i>. https://claude.com/blog/best-practices-for-computer-and-browser-use-with-claude",
 "Anthropic. (2026b). <i>Claude API pricing</i>; <i>Fast mode</i> (developer documentation, read 28 September 2026). https://platform.claude.com/docs/en/about-claude/pricing; https://platform.claude.com/docs/en/build-with-claude/fast-mode",
 "Bian, S., Yan, M., Jayarajan, A., Pekhimenko, G., &amp; Venkataraman, S. (2025). What limits agentic systems efficiency? arXiv:2510.16276. University of Wisconsin–Madison; University of Toronto; NVIDIA.",
 "Chang, C., Zhou, Y., Fu, K., An, D., Feng, T., Lu, H., Yao, S., Guo, P., Yu, Y., Shan, Y., Li, B., Yuan, B., &amp; Wang, W. (2026). From LLM inference to agentic workloads: Characterization and implications for serving systems (AgentSysBench). arXiv:2608.15127. Hong Kong University of Science and Technology; Alibaba Group; ByteDance.",
 "Chen, L., Zaharia, M., &amp; Zou, J. (2024). FrugalGPT: How to use large language models while reducing cost and improving performance. <i>Transactions on Machine Learning Research</i>. arXiv:2305.05176. Stanford University.",
 "DeepSeek. (2026). <i>Models &amp; pricing</i> (API documentation, read 28 September 2026); <i>DeepSeek-V4.1-Flash release</i> (10 September 2026). https://api-docs.deepseek.com/quick_start/pricing; https://api-docs.deepseek.com/news/news260910",
 "Erol, M. H., El, B., Suzgun, M., Yuksekgonul, M., &amp; Zou, J. (2026). Cost-of-Pass: An economic framework for evaluating language models. <i>The Fourteenth International Conference on Learning Representations (ICLR 2026)</i>. arXiv:2504.13359. Stanford University.",
 "Feng, G., Mao, H., Dutta, P., &amp; Gonzalez, J. E. (2026). Concurrency without model changes: Future-based asynchronous function calling for LLMs (AsyncFC). arXiv:2605.15077. University of California, Berkeley.",
 "Google. (2026). <i>Gemini Developer API pricing</i> (read 28 September 2026). https://ai.google.dev/gemini-api/docs/pricing",
 "Kang, H., Li, Z., Yang, X., Xu, W., Chen, Y., Wang, J., Chen, B., Krishna, T., Xu, C., &amp; Arora, S. (2026). ThunderAgent: A fast, simple, and program-aware agentic inference system. <i>Proceedings of the 43rd International Conference on Machine Learning (ICML 2026)</i>, poster. arXiv:2602.13692. Georgia Institute of Technology; University of Illinois Urbana-Champaign; Carnegie Mellon University; Together AI.",
 "Kapoor, S., Stroebl, B., Kirgis, P., Nadgir, N., Siegel, Z. S., Wei, B., … Narayanan, A. (2026). Holistic Agent Leaderboard: The missing infrastructure for AI agent evaluation. <i>The Fourteenth International Conference on Learning Representations (ICLR 2026)</i>. arXiv:2510.11977. Princeton University et al.",
 "Kim, S., Moon, S., Tabrizi, R., Lee, N., Mahoney, M. W., Keutzer, K., &amp; Gholami, A. (2024). An LLM compiler for parallel function calling. <i>Proceedings of the 41st International Conference on Machine Learning (ICML 2024)</i>. arXiv:2312.04511. University of California, Berkeley.",
 "Le Sellier de Chezelles, T., Gasse, M., Lacoste, A., Caccia, M., Drouin, A., Boisvert, L., … Chapados, N. (2025). The BrowserGym ecosystem for web agent research. <i>Transactions on Machine Learning Research</i>. arXiv:2412.05467. ServiceNow Research et al. (figure not re-verified; used only in Appendix A1)",
 "Lee, N., Erdogan, L. E., John, C. J., Krishnapillai, S., Mahoney, M. W., Keutzer, K., &amp; Gholami, A. (2026). Agentic test-time scaling for WebAgents. arXiv:2602.12276. University of California, Berkeley.",
 "Liu, B., Qiu, H., Goiri, Í., Fonseca, R., Bianchini, R., &amp; Choukse, E. (2026). Agentic coding in the wild: Characterizing GitHub Copilot traces at production scale. arXiv:2608.00101. University of Illinois Urbana-Champaign; Microsoft Azure Research.",
 "Lu, J., Zhang, Z., Yang, F., Zhang, J., Wang, L., Du, C., Lin, Q., Rajmohan, S., Zhang, D., &amp; Zhang, Q. (2025). AXIS: Efficient human-agent-computer interaction with API-first LLM-based agents. <i>Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)</i>, 7711–7743. https://doi.org/10.18653/v1/2025.acl-long.381. Microsoft.",
 "Luo, M., Shi, X., Cai, C., Zhang, T., Wong, J., Wang, Y., Wang, C., Huang, Y., Chen, Z., Gonzalez, J. E., &amp; Stoica, I. (2026). Agentix: An efficient serving engine for LLM agents as general programs. <i>23rd USENIX Symposium on Networked Systems Design and Implementation (NSDI 26)</i>. University of California, Berkeley; Google DeepMind; Shanghai Jiao Tong University.",
 "Meta. (2026, September 8). <i>Introducing Muse, your personal AI agent</i> [Newsroom post]. https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/",
 "OpenAI. (2025). <i>Introducing Operator</i> (23 January 2025); <i>Introducing ChatGPT agent</i> (17 July 2025). https://openai.com/index/introducing-operator/; https://openai.com/index/introducing-chatgpt-agent/",
 "OpenAI. (2026). <i>API pricing</i>; <i>API changelog</i> (fast mode, 30 July 2026; Ultrafast, 13 August 2026) (read 28 September 2026). https://developers.openai.com/api/docs/pricing; https://developers.openai.com/api/docs/changelog",
 "Vendor price pages used for Appendix A3 (all read 27 September 2026): AWS, <i>Amazon EC2 T3 instances</i>; Browser Use, <i>Pricing</i> and <i>API v4: create browser session</i>; Browserbase, <i>Pricing</i> and <i>Billing plans</i>; Daytona, <i>Pricing</i> and <i>Billing</i>; E2B, <i>Pricing</i>; Modal, <i>Pricing</i> and <i>Sandbox resources</i>.",
 "Winston, C., Wang, R. Y., Mirhoseini, A., &amp; Kozyrakis, C. (2026). Agent JIT compilation for latency-optimizing web agent planning and scheduling. <i>Proceedings of the 43rd International Conference on Machine Learning (ICML 2026)</i>, PMLR 306. arXiv:2605.21470. Stanford University.",
 "Wong, M., Hsieh, K., Nath, S., &amp; Netravali, R. (2026). Skim: Speculative execution for fast and efficient web agents. arXiv:2605.16565. Princeton University; Microsoft Research.",
 "xAI. (2026). <i>Grok 4.7</i> model page, SpaceXAI Docs (read 28 September 2026). https://docs.x.ai/developers/models/grok-4.7",
 "XLANG Lab. (2026). OSWorld 2.0: Benchmarking computer use agents on long-horizon real-world tasks. arXiv:2606.29537. The University of Hong Kong (authored as “XLANG Lab and Collaborators”; the full author list is in the paper’s Appendix A).",
 "xlang-ai. (2026). <i>OSWorld</i> [Source code], desktop_env/desktop_env.py and run.py at commit b138d348. https://github.com/xlang-ai/OSWorld",
 "Xu, B., Xue, Z., Chen, D., Fu, C., Wu, C., Huang, C., … Zhang, N. (2026). TokenPilot: Cache-efficient context management for LLM agents. arXiv:2606.17016. Zhejiang University; University of Electronic Science and Technology of China; Xidian University; HomologyAI.",
 "Yuan, Y., Nayak, A., Kundu, S., &amp; Talati, N. (2026). Agentic AI workload characteristics. arXiv:2605.26297. University of Illinois Urbana-Champaign; Gimlet Labs; Intel.",
 "Zhang, C., Huang, H., Ni, C., Mu, J., Qin, S., He, S., … Zhang, D. (2026). UFO2: The desktop AgentOS. <i>Transactions on Machine Learning Research</i>. arXiv:2504.14603. Microsoft.",
 "Zhu, K., Jacob, M., Ma, C., Pan, Y., Wang, S., Krishnamurthy, A., &amp; Kasikci, B. (2026). TraceLab: Characterizing coding agent workloads for LLM serving. arXiv:2606.30560. University of Washington.",
]

def refs_html(items, start=1):
    return f'<ol class="reflist" start="{start}">' + "".join(f"<li>{r}</li>" for r in items) + "</ol>"

half = (len(REFS_P1) + 1) // 2
slide("s11", "References · Part 1 (1 of 2)", kind="refs",
      crumb="author–year tags on the pages refer to these entries · published version where one exists, otherwise the arXiv number and the authors’ institutions",
      body=refs_html(REFS_P1[:half]))
slide("s12", "References · Part 1 (2 of 2)", kind="refs",
      crumb="continued",
      body=refs_html(REFS_P1[half:], start=half+1))

# =====================================================================
# APPENDIX — Part 1
# =====================================================================
def A(id_, label, title, body, hl=(), crumb="", notes="", chip=("#back", "← back")):
    slide(id_, title, body, label=label, hl=hl, crumb=crumb, notes=notes, chip=chip, kind="appendix")

th_slow = ["id", "cause", "mechanism", "evidence, with the conditions of the measurement", "source", "dominant in"]
w_slow = ["4%", "11%", "15%", "47%", "13%", "10%"]

A("a0-1", "A0 · 1/2", "A0 · Page 2’s equations: the source form of each row, and what the page leaves out",
  crumb="page 2 writes all rows in one notation · here each source in its own · our own steps are marked calc. or ours",
  body=table(["row", "on page 2", "the source’s own formula, in its notation", "what page 2 simplifies"], [
   ["time", "Passes, calls and environment steps add; minus the overlap " + tex(r"T_{\mathrm{saving}}", 12), tex(r"T^{R}=\sum_i\,(T_P^{R}(P_i)+T_E(E_i))", 12) + " sequential, " + tex(r"T^{C}=\sum_i T_P^{C}(P_i)+\max_k T_E(E_k)", 12) + " parallel; " + tex(r"T_P", 12) + " planner time, " + tex(r"T_E", 12) + " executor time " + ci('llmc') + ". " + tex(r"T_{\mathrm{saving}}=S(M)+S(E)-D(M\cup E)", 12) + ": summed lengths of the model and execution intervals minus their merged elapsed time " + ci('asyncfc'), "Summing the calls inside a pass is our step; parallel calls (GTA1’s four planners) enter through " + tex(r"T_{\mathrm{saving}}", 12) + ". Idle gaps (harness code, a person thinking) are outside " + tex(r"T_{\mathrm{task}}", 12) + ". Every time is a mean; the literature also uses distributions and tails"],
   ["call", "Queueing + reading the uncached prompt + writing", "Prompt split into a cached prefix " + tex(r"P", 12) + " and an appended part " + tex(r"A", 12) + "; time to first token and per-token decode latency " + tex(r"\hat{\ell}", 12) + " reconstructed from timestamps " + ci('tracelab') + ". Latency = waiting + execution + interceptions, in words " + ci('agentix'), "Reading and writing times are measured quantities: no scanned source writes reading time as a formula of token count. That reading depends only on uncached tokens is our reading of the prefix / append split"],
   ["prompt", tex(r"R_{k+1} \approx R_k + W_k + o_{k+1}", 12) + " (prompt, written and observed tokens of pass " + tex("k", 12) + "); the " + tex("N^2", 12) + " sum (calc.)", tex(r"H_{a,i+1}=H_{a,i}\,\Vert\,\Phi(\theta,m,u)\,\Vert\,o_{a,i}", 12) + ", " + tex(r"C_{a,i}=|H_{a,i}|", 12) + ": the history of agent " + tex(r"a", 12) + " after call " + tex(r"i", 12) + " is the previous history, the formatted output " + tex(r"\Phi", 12) + " (thinking " + tex(r"\theta", 12) + ", message " + tex(r"m", 12) + ", tool call " + tex(r"u", 12) + ") and the tool result " + tex(r"o", 12) + "; " + tex(r"C", 12) + " is its length " + ci('yuan'), "Written per pass for the main call; vendors may drop earlier thinking from the history, hence ≈. The sum assumes full history, no trimming and a constant addition per pass. A screenshot adds 1,000–1,800 tokens " + ci('anth-a')],
   ["money", "Cache-hit, cache-miss and cache-store tokens, written tokens, each at its price; plus machine hours", tex(r"\mathrm{Cost}=|C'_{\mathrm{hit}}|\,p_{\mathrm{hit}}+|C'_{\mathrm{miss}}|\,p_{\mathrm{miss}}+H_{\mathrm{out}}\,p_{\mathrm{out}}", 12) + ": cached and uncached context tokens and output tokens, each at its price " + ci('tokenpilot') + ". Vendors also bill cache writes: 1.25× for 5 min, 2× for 1 h (Anthropic), 1.25× (OpenAI) " + ci('anth-b','openai'), "The two cache-write lifetimes are merged into one price; multipliers sit inside each price; per-call and tool fees are left out; a cache unused for 5 min or 1 h expires and its prefix is paid again as cache-miss or cache-store tokens"],
   ["per success", "Expected cost per attempt ÷ probability of success", tex(r"v(m,p)=C_m(p)\,/\,R_m(p)", 12) + ", " + tex(r"c_m(p)=n_{\mathrm{in}}\,c_{\mathrm{in}}+n_{\mathrm{out}}\,c_{\mathrm{out}}", 12) + ": expected cost " + tex(r"C", 12) + " of model " + tex(r"m", 12) + " on problem " + tex(r"p", 12) + " divided by its expected accuracy " + tex(r"R", 12) + " " + ci('cop'), "Over a benchmark we divide the mean cost by the success rate. That equals the expected cost of retrying a task until it succeeds only if every task had the same success chance"],
   ["goal", "Lower time or cost per success without raising the other, at a success rate of at least " + tex("s_0", 12), tex(r"\max_s\ \mathbb{E}[r(a,\hat{a}(s,q))]\ \ \mathrm{s.t.}\ \ \mathbb{E}[c(s,q)]\leq b", 12) + ": maximise the expected quality " + tex(r"r", 12) + " of strategy " + tex(r"s", 12) + " with expected cost " + tex(r"c", 12) + " within budget " + tex(r"b", 12) + " " + ci('frugal'), "Our statement, with two objectives; the success rate is held at its level before the change"],
  ], ["8%", "22%", "38%", "32%"]))

A("a0-2", "A0 · 2/2", "A0 · Page 2’s variables, the step each belongs to, and the pages that expand it",
  crumb="every symbol on page 2 · the same terms light up in the loop thumbnail at the top right of each page",
  body=table(["symbol", "meaning", "step in the loop", "expanded on"], [
   [tex("N", 12), "passes per task", "the loop", "pages 3–4, 6, 10 · A1-1"],
   [tex(r"k,\ j", 12), "index of the pass; index of the call inside the pass", "the loop; decide", "—"],
   [tex("c_k", 12), "model calls in pass " + tex("k", 12) + " (planning, judging, reflecting, sampling), set by the harness", "decide", "pages 3–4, 7 · A1-1, A3-2"],
   [tex(r"\ell_{kj}", 12), "elapsed time of call " + tex("j", 12) + " in pass " + tex("k", 12), "decide", "page 5 · A1-2"],
   [tex(r"t_{\mathrm{queue}}", 12), "waiting at the provider before processing; unbilled; set by the provider’s load", "decide · queue", "pages 5, 9 · A1-2"],
   [tex(r"t_{\mathrm{read}}", 12), "reading the prompt, all tokens at once (prefill); only tokens not served from the cache", "decide · read", "pages 5–6 · A1-2, A2"],
   [tex(r"t_{\mathrm{write}}", 12), "writing the answer one token at a time (decode), thinking included", "decide · write", "pages 5–6 · A1-2"],
   [tex(r"t_{\mathrm{obs}},\ t_{\mathrm{act}},\ t_{\mathrm{wait}}", 12), "producing the observation; executing the action; page loads, fixed sleeps, tool runs", "observe; act; wait", "pages 5–6, 9 · A1-3"],
   [tex(r"T_{\mathrm{saving}}", 12), "time saved because steps run at the same time; zero when everything runs in sequence", "the loop", "pages 3, 5, 10 · A1-3"],
   [tex(r"R = R^{\mathrm{hit}} + R^{\mathrm{miss}} + R^{\mathrm{store}}", 12), "tokens a call reads: from the cache (hit), not in it (miss), stored into it (store)", "decide · read", "pages 7–8 · A3-1, A3-2"],
   [tex(r"o_k,\ \bar{o}", 12), "tokens the observation of pass " + tex("k", 12) + " adds to the prompt; their mean per pass", "observe", "pages 5, 7 · A1-2, A3-1"],
   [tex(r"W,\ \bar{w}", 12), "tokens written by a call, thinking included; mean per pass", "decide · write", "pages 5, 7 · A3-1"],
   [tex(r"p_{\mathrm{hit}},\ p_{\mathrm{miss}},\ p_{\mathrm{store}},\ p_{\mathrm{write}}", 12), "price per token of each class, for the model and tier used", "decide", "pages 7–8 · A3-2, A3-3"],
   [tex(r"\tau,\ p_{\mathrm{env}}", 12), "hours the environment machine is billed (at least " + tex(r"T_{\mathrm{task}}", 12) + "); its hourly price", "wait", "page 8 · A3-3"],
   [tex(r"\Pr[\mathrm{success}],\ s_0", 12), "probability that one attempt completes the task; its level before a change", "end (judged afterwards)", "pages 7–8, 10 · A3-2"],
  ], ["22%", "46%", "14%", "18%"]))

A("a1-1", "A1 · 1/3", "A1 · Slowness, every cause — I. steps and II. calls per step",
  hl=("n-steps", "n-calls"),
  crumb="the complete table behind pages 3–4 · three kinds of agent: screenshot desktop agent, text web agent, coding agent with a prompt cache",
  body=table(th_slow, [
   ["I-1", "The task is long", "Hour-scale tasks take hundreds of passes", "OSWorld 2.0, 108 long tasks: Claude Opus 4.7 with maximum thinking, one action per step, 500-step cap: 318 tool calls per task on average, i.e. 318 steps; with several actions per call, Claude Opus 4.8 takes 103 steps (481.8 calls) and GPT-5.5 95.2 steps (149.8 calls)", ci('osw2'), "screenshot, text"],
   ["I-2", "One action per pass", "Every click is a whole pass: one observation, one model call, one wait", "OSWorld 2.0: with one action per step Claude Opus 4.7 needs 318 steps; with batched actions the same model needs 160.7 and Claude Opus 4.8 needs 103", ci('osw2'), "screenshot, text"],
   ["I-3", "Navigation-only passes still call the model", "Paging, scrolling and opening the next page need no thinking but cost a call each", "Skim’s profile of three text web agents (Browser-Use, AgentOccam, WebVoyager; GPT-4o) on 151 WebVoyager live-site tasks: 66.7% of the steps in the median task are pure navigation", ci('skim'), "text"],
   ["I-4", "Idling and dead loops", "Element not found, repeated retries; steps rise without progress", "OSWorld-Human’s records of the GTA1 harness (o3 plans and judges, GTA1-7B locates elements) on 39 OSWorld desktop tasks: in failed tasks that exceeded 50 steps, 66% of steps were wasted repeats; one element-locating loop repeated the same step 18 times — 27 minutes and $8.47 at list price without caching", ci('osh'), "screenshot"],
   ["I-5", "Acting on a stale screen", "The screenshot is taken before the page changes; the agent clicks on the old layout and must repair", "OSWorld 2.0 records “stale interface state” as a failure mode; no share reported", ci('osw2'), "screenshot"],
   ["II-1", "Multi-call harness", "One step = plan + judge + reflect, several calls in series", "OSWorld-Human, two harnesses: GTA1 runs 4 parallel planners per step, retries up to 3 rounds, then one judging call picks — 4–12 planning calls per judging call; Agent S2 adds a reflection call per step, so planning is 53% and reflection 34% of task time", ci('osh'), "screenshot"],
   ["II-2", "Sampling for accuracy", "5–20 candidates per step, then pick one", "Same model and harness (gpt-oss-120b, ReAct) on 165 WebArena-Lite tasks: 1 → 10 candidates per step raises success from 38.8% to 43.2% and tokens per task from 96K to 920K — 9.6× the tokens for 4.4 points", ci('atts'), "text"],
   ["II-3", "Coding agents call repeatedly within a turn", "The model is called back and forth inside one user turn", "GitHub Copilot coding agent production telemetry (first week of June 2026, 13.5 million sessions): 6.6 model calls per user turn on average", ci('copilot'), "coding"],
  ], w_slow))

A("a1-2", "A1 · 2/3", "A1 · Slowness, every cause — III. each call is slow",
  hl=("n-queue", "n-read", "n-write"),
  crumb="the complete table behind page 5",
  body=table(th_slow, [
   ["III-1", "Queueing", "The request waits at the provider; unbilled, but counted as model time", "Client-side measurement of 15 models across 5 providers: requests of the same length differ in latency by up to 69× depending on when they are sent", ci('bian'), "all"],
   ["III-2", "Reading (the prompt is re-processed every call)", "Every call re-reads the whole history; more screenshots, slower", "OSWorld-Human, multi-call harnesses: later steps up to 3× slower because the prompt at step " + tex("k", 12) + " holds the " + tex("k-1", 12) + " earlier screenshots — “dominated by prefill”. One screenshot is 1,000–1,800 tokens. AgentSysBench’s WebArena agent (Kimi-K2.6): observation switched from a single format to accessibility tree + HTML + screenshot → input 4.8×, model share of time 46.9% → 61.6%. Under load the cache is evicted and re-read: SWE-Agent / OpenHands running GLM-4.6 on 8 H100s for SWE-bench Lite, request latency up to 7.14× as concurrency rises", ci('osh','anth-a','asb','thunder'), "screenshot; text with rich observations; coding under load"],
   ["III-3", "Writing (one token at a time)", "Token-by-token generation, strictly serial", "Locally served ReAct agents (Qwen3.6-27B / Gemma4-31B, vLLM, 2 H100s) on five benchmarks: with the cache warm, generation is 91–98.6% of model time. Windows desktop agent UFO2 (GPT-4o / o1 API): about 10 s per model call, the largest item per step in every configuration", ci('yuan','ufo2'), "coding; single-call screenshot"],
   ["III-4", "Thinking modes and larger models", "Thinking writes more tokens; larger models are slower per token", "OSWorld 2.0, same 108 tasks: Claude Opus 4.8 writes 224K output tokens per task, GPT-5.5 37K. Holistic Agent Leaderboard, 9 benchmarks, 21,730 runs: raising reasoning effort lowered accuracy in 21 of 36 pairs", ci('osw2','hal'), "all"],
  ], w_slow))

A("a1-3", "A1 · 3/3", "A1 · Slowness, every cause — IV. environment, V. serial",
  hl=("n-observe", "n-act", "n-wait", "n-overlap"),
  crumb="the complete table behind page 5 (environment and serial structure)",
  body=table(th_slow, [
   ["IV-1", "Producing the observation", "Extracting the accessibility tree or detecting elements takes time", "OSWorld desktop applications: 3–26 s to generate one accessibility tree; the screenshot itself is under 2% of task time. UFO2: OmniParser element detection adds about 1 s per step", ci('osh','ufo2'), "screenshot"],
   ["IV-2", "Browser execution and page load", "After a click the agent waits for the page", "151 WebVoyager live-site tasks: per step, median browser action 6.6 s vs model call 4.7 s. WebArena with GenericAgent + Claude 3.5 Sonnet: 7.6 s of a 12.2 s step in the browser (this figure was not re-verified)", ci('skim','bgym'), "text"],
   ["IV-3", "Fixed sleeps", "The agent cannot tell when the page is ready, so it sleeps a fixed number of seconds", "OSWorld’s environment code sleeps 2 s after every action; OSWorld 2.0 prescribes 3 s, so 318 steps are about 16 minutes of pure waiting (calc.). AgentSysBench: a single-call GUI agent (ReAct, Kimi-K2.6 API) spends over 70% of its OSWorld execution time in the desktop sandbox", ci('code','osw2','asb'), "screenshot (caused by the benchmark harness)"],
   ["IV-4", "Tool tails", "Tests and builds take minutes", "TraceLab, 4,265 Claude Code / Codex sessions from 43 developers (September 2025 – June 2026): tool calls over 1 minute are 4% of calls but 85% of tool time; a request averages 4.3 minutes — tools 2.5 (59.8%), model 1.7 (41.0%)", ci('tracelab'), "coding"],
   ["V", "Serial structure", "The four stages never overlap, so task time is the sum of every term, not the largest one; fixing one term saves only its share", "Concurrency within a turn is 1.15 in Copilot telemetry. Separately, 80–92% of a coding session’s elapsed time is the human thinking between turns — strip it before reading any total", ci('copilot','tracelab'), "all"],
  ], w_slow))

A("a2-1", "A2", "A2 · Where the arrows land, with every measurement condition",
  hl=("n-read", "n-wait", "n-write"),
  crumb="the complete table behind page 6",
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
  crumb="the complete table behind page 7 · prices are list prices from the vendors’ own pages, September 2026",
  body=table(th_cost, [
   ["1-1", "History re-sent", "Call " + tex("k", 12) + " reads everything from the " + tex("k-1", 12) + " earlier steps; total reading " + tex(r"\approx N^2", 12), "“Cost grows quadratically with the number of steps” — OSWorld-Human, real runs", ci('osh')],
   ["1-2", "Large screenshots", "1,000–1,800 tokens per image; 100 images fill a 200K context", "Anthropic’s engineering guidance for computer and browser use", ci('anth-a')],
   ["1-3", "Rich observation formats", "Accessibility tree + HTML + screenshot together: 4.8× the input", "AgentSysBench, WebArena agent, Kimi-K2.6", ci('asb')],
   ["1-4", "Sampling", "Several candidates per step, mostly read tokens", "gpt-oss-120b + ReAct on 165 WebArena-Lite tasks: 1 → 10 candidates per step, 96K → 920K tokens per task", ci('atts')],
   ["1-5", "The cache is not a cure", "However high the hit rate, a long history keeps reading dominant; a miss re-reads everything", "TraceLab, 4,265 Claude Code / Codex sessions: prefix-cache hit rate 95.7%, prefix tokens still 59.5% of list-price cost; on a miss the re-read is 3.8× the genuinely new content", ci('tracelab')],
   ["2-1", "Thinking modes", "Thinking tokens are billed as output; when they cannot be switched off they are a fixed overhead", "OSWorld 2.0, same tasks: Claude Opus 4.8 224K output tokens per task, GPT-5.5 37K; Claude Opus 5.5: “thinking cannot be disabled and is billed as output”", ci('osw2','anth-b')],
   ["2-2", "But writing is not always the larger bill", "In an uncached screenshot agent, output was 31% of the total", "OSWorld-Human, GTA1: the paper’s $2.43 counts output only; Table 3’s input and output give $7.87", ci('osh')],
  ], w_cost))

A("a3-2", "A3 · 2/3", "A3 · Cost, every cause — 3. calls, 4. failures, 5. unit price",
  hl=("n-calls", "n-succ", "n-price"),
  crumb="the complete table behind page 7 (calls, failures, unit price)",
  body=table(th_cost, [
   ["3", "Number of calls", tex(r"N \cdot c_k", 12) + " scales both token bills", "GTA1: 4 parallel planners per step, up to 3 retry rounds, one judging call → 4–12 planning calls per judging call, i.e. 5–13× the calls of a single-call harness (calc.). Agentic test-time scaling: 5–20 candidates per step multiply the calls by the candidate count. The same extra calls cost time and money at once", ci('osh','atts')],
   ["4-1", "Failed attempts are billed", "Cost per success = cost per attempt ÷ success rate", "OSWorld 2.0: the best agent (Claude Opus 4.8) costs about $72.4 per attempt at 20.6% completion → about $351 per success (calc.). An accounting conversion, not the real price of retrying one task until it succeeds", ci('osw2')],
   ["4-2", "Idle steps are billed in full", "Every pass of a dead loop is a full read and write", "OSWorld-Human, GTA1 on 39 OSWorld tasks: one element-locating loop repeated the same step 18 times — 27 minutes, $8.47 at list price without caching; in failed tasks over 50 steps, 66% of steps were such repeats", ci('osh')],
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
  crumb="the complete tables behind page 8 · vendor price pages read 2026-09-27 · per-task amounts and shares are our own arithmetic (calc.)",
  body=table(["environment", "price (vendor page)", "1-hour task", "15-min task", "share of a $7.87 API bill", "share of $72.4"], [
   ["Browser Use cloud browser", "$0.02 per browser-hour, billed by the minute, 1-minute minimum; traffic extra (residential proxy $5/GB, direct $0.20/GB); sessions capped at 240 minutes", "$0.020", "$0.005", "0.25%", "0.03%"],
   ["AWS t3.medium (2 vCPU / 4 GiB, Linux, us-east-1)", "$0.0418 per hour on the T3 product page; another AWS page says $0.0416 (0.5% apart)", "$0.042", "$0.010", "0.5%", "0.06%"],
   ["Browserbase cloud browser", "$20 per month for 100 hours, then $0.12 per hour; $99 per month for 500 hours, then $0.10; billed by the minute", "$0.12", "$0.03", "1.5%", "0.17%"],
   ["E2B / Daytona sandbox (2 vCPU / 4 GiB)", "E2B $0.000014 per vCPU-second + $0.0000045 per GiB-second; Daytona $0.0504 per vCPU-hour + $0.0162 per GiB-hour — both $0.1656 per hour", "$0.166", "$0.041", "2.1%", "0.23%"],
   ["Modal sandbox (1 physical core = 2 vCPU, 4 GiB)", "$0.00003942 per core-second + $0.00000667 per GiB-second → $0.238 per hour; billed on the larger of requested and used", "$0.238", "$0.060", "3.0%", "0.33%"],
   ["AWS t3.2xlarge (8 vCPU / 32 GiB, OSWorld 2.0’s default instance)", "$0.3341 per hour", "$0.334", "$0.084", "4.2%", "0.46%"],
   ["OpenAI hosted container (Hosted Shell / Code Interpreter, 4 GB)", "$0.12 per 20-minute session → $0.36 per hour; 1 GB $0.03, 16 GB $0.48, 64 GB $1.92 per 20 minutes", "$0.36", "$0.12", "4.6%", "0.50%"],
  ], ["22%", "42%", "8%", "8%", "10%", "10%"]) + """
<div class="apx-note"><b>The four accounting conventions (page 8), in one line each:</b> output only vs all tokens — 3.2× (OSWorld-Human, $2.43 vs $7.87); per attempt vs per success — 4.9× (OSWorld 2.0, $72.4 ÷ 20.6%); uncached vs cached — 4–50× on the read price by vendor (calc.), far less on the bill (TraceLab: 95.7% hits, prefix still 59.5% of cost); standard vs fast mode — 2× (both vendors), buying only writing speed.</div>""")

A("a5-1", "A5", "A5 · Each cause’s effect on time and on money",
  hl=("n-rtok", "n-wtok", "n-queue", "n-wait", "n-machine"),
  crumb="the complete table behind pages 9–10",
  body=table(["cause", "effect on time", "effect on money", "relationship"], [
   ["Many passes " + tex("(N)", 12), "Roughly linear: one more step is one more call and one more wait (later steps somewhat slower, up to 3×)", "Write tokens linear in " + tex("N", 12) + "; read tokens quadratic, because every step re-reads the whole history", "<b>same source</b> — double the steps: about 2× the time, about 4× the read bill (uncached)"],
   ["Many calls per pass " + tex("(c_k)", 12), "linear", "linear", "<b>same source</b>"],
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

A("a6-1", "A6", "A6 · The gaps in the evidence, and what each one blocks",
  crumb="the complete table behind page 10",
  body=table(["gap", "what exists today", "consequence for what can be claimed"], [
   ["Read / write time split and cache hit rate for a frontier API model", f"No measurement reports both; the only read / write split is on locally served 27–31B models {ci('yuan')}; screenshot-agent measurements do not report cache state", "How much of “87–97% in the model” is reading, how much writing, and what remains once the cache is on — unknown"],
   ["How much slower an agent is than a person", f"None of 17 benchmarks measures agent and human elapsed time on the same tasks; the closest is AXIS’s user study, in which a UI agent was 1.69× slower than manual work on easy tasks (small sample) {ci('axis')}", "“X times slower than a person” cannot go on a slide"],
   ["Environment dollars", "Benchmarks report instance types; AgentSysBench reports shares; products publish nothing. Computable from instance type × duration × list price: CPU environments usually 0.3–5% of the API bill (page 8)", "Every benchmark cost is an API bill; the omission is small for CPU environments, not for GPU sandboxes or long idle sessions"],
   ["Whether OSWorld-Human’s “action” includes the 2-s sleep after each step", f"Not stated {ci('code')}; if it does, “actions under 2%” implies more than 100 s per step (calc.)", "“Environment under 3.5%” may understate the waiting"],
   ["The rebound from a smaller model", "No direct evidence on how many extra steps and retries a drop in accuracy causes", "The last row of the relationship table stays marked “inference”"],
   ["How much slowness hurts accuracy", f"Only OSWorld 2.0 records the stale-state failure mode, without its share of failures {ci('osw2')}", "“It exists” can be said; “how large” cannot"],
  ], ["27%", "45%", "28%"]))

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
    main_n = 0
    for s in SLIDES:
        cls = "slide " + s["kind"]
        if s["kind"] in ("main", "refs"):
            main_n += 1
            label = f"AGENT ACCELERATION · PART 1 · {main_n:02d}"
        elif s["kind"] == "title":
            label = ""
        else:
            label = "AGENT ACCELERATION · PART 1 · " + s["label"]
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
