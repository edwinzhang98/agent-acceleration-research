#!/usr/bin/env python3
"""Build slides/agent-acceleration.html — the boss deck.

Part 1 (this file's content): where the time and the money go, built from the
Chinese study document《Agent 慢和贵的逻辑链》(2026-09-27), which is itself built
from dossier v3. Numbers are the dossier's; the ledger IDs live in the Chinese
speaker notes (press N), not on the slides.

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
def loop_svg(hl=(), cls="thumb-svg"):
    """The agent loop with every term on it. Node ids can be highlighted."""
    hl = set(hl)
    SVG_N[0] += 1
    mid = f"ah{SVG_N[0]}"
    def node(id_, x, y, w, h, title, sub="", fs=20, sfs=12, r=6):
        c = " hl" if id_ in hl else ""
        ty = y + h/2 + (fs*0.36 if not sub else fs*0.05)
        s = f'<g id="{mid}-{id_}" class="node{c}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/>'
        s += f'<text class="t" x="{x+w/2}" y="{ty:.1f}" font-size="{fs}" text-anchor="middle">{html.escape(title)}</text>'
        if sub:
            s += f'<text class="s" x="{x+w/2}" y="{y+h/2+fs*0.05+sfs+6:.1f}" font-size="{sfs}" text-anchor="middle">{html.escape(sub)}</text>'
        return s + "</g>"
    def pill(id_, x, y, w, h, title, fs=15):
        c = " hl" if id_ in hl else ""
        return (f'<g id="{mid}-{id_}" class="node pill{c}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}"/>'
                f'<text class="t" x="{x+w/2}" y="{y+h/2+fs*0.36:.1f}" font-size="{fs}" text-anchor="middle">{html.escape(title)}</text></g>')
    def arrow(x1, y1, x2, y2):
        return f'<path class="arr" d="M{x1} {y1} L{x2} {y2}" marker-end="url(#{mid})"/>'
    def ftext(x, y, s, fs=16, anchor="start", cls="f"):
        return f'<text class="{cls}" x="{x}" y="{y}" font-size="{fs}" text-anchor="{anchor}">{html.escape(s)}</text>'

    parts = [f'<svg class="{cls}" viewBox="0 0 1200 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The agent loop">',
             f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" class="ahp"/></marker></defs>']
    # nodes
    parts.append(node("n-observe", 30, 60, 170, 70, "Observe", "screenshot · page text"))
    # decide box
    c = " hl" if "n-decide" in hl else ""
    parts.append(f'<g id="{mid}-n-decide" class="box{c}"><rect x="250" y="52" width="470" height="86" rx="8"/>'
                 f'<text class="bt" x="262" y="72" font-size="13">DECIDE · one model call</text></g>')
    parts.append(pill("n-queue", 268, 86, 120, 34, "queue"))
    parts.append(pill("n-read", 404, 86, 150, 34, "read the prompt"))
    parts.append(pill("n-write", 570, 86, 134, 34, "write the answer"))
    parts.append(pill("n-calls", 250, 14, 160, 28, "c calls per step", fs=14))
    parts.append(arrow(330, 42, 330, 52))
    parts.append(node("n-act", 770, 60, 170, 70, "Act", "click · type · run a tool"))
    parts.append(node("n-wait", 990, 60, 180, 70, "Wait", "page load · sleep · tool run"))
    # arrows between
    parts += [arrow(200, 95, 250, 95), arrow(720, 95, 770, 95), arrow(940, 95, 990, 95)]
    # loop back
    parts.append(f'<path class="arr" d="M1080 130 L1080 178 L115 178 L115 132" marker-end="url(#{mid})"/>')
    parts.append(pill("n-steps", 540, 164, 130, 28, "× N steps", fs=14))
    # formulas
    parts.append('<line class="rl" x1="30" y1="212" x2="1170" y2="212"/>')
    parts.append(ftext(30, 240, "time per task  ≈  Σ over steps [ c × ( queue + read + write ) + observe + act + wait ]", 16))
    parts.append(ftext(30, 278, "money per task  ≈  Σ over steps  c × (", 16))
    parts.append(pill("n-rtok", 356, 258, 112, 28, "read tokens", fs=14))
    parts.append(ftext(474, 278, "×", 16))
    parts.append(pill("n-price", 492, 258, 112, 28, "read price", fs=14))
    parts.append(ftext(612, 278, "+", 16))
    parts.append(pill("n-wtok", 632, 258, 116, 28, "write tokens", fs=14))
    parts.append(ftext(756, 278, "× write price )   ÷", 16))
    parts.append(pill("n-succ", 918, 258, 124, 28, "success rate", fs=14))
    parts.append(ftext(1052, 278, "= per success", 16))
    parts.append("</svg>")
    return "".join(parts)

# ---------------------------------------------------------------- helpers
def esc(s):
    return html.escape(s, quote=False)

def card(k, v, d, c=""):
    """A card: mono key, bold value line, description, mono citation."""
    s = f'<div class="card"><div class="ck">{k}</div>'
    if v:
        s += f'<div class="cv">{v}</div>'
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
    labelw = max(labelw, int(max(len(r[0]) for r in rows) * 6.8) + 14)
    valw = int(max(len(r[2]) for r in rows) * 6.8) + 12
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
    """The time equation with the five classes of slowness mapped onto its terms (page 4)."""
    terms = [("Σ over N steps", "I · steps", "n-steps"), ("c ×", "II · calls per step", "n-calls"),
             ("( queue + read + write )", "III · each call", "n-read"), ("+ observe + act + wait", "IV · environment", "n-wait"),
             ("all added, never overlapped", "V · serial", "")]
    s = ['<div class="eqstrip"><div class="eqt">time per task =</div>']
    for t, c, _ in terms:
        s.append(f'<div class="eqterm"><div class="eqx">{html.escape(t)}</div><div class="eqc">{html.escape(c)}</div></div>')
    return "".join(s) + "</div>"

def cost_strip():
    """The money equation with the six classes of cost mapped onto its terms (page 11)."""
    terms = [("Σ over N steps · c ×", "3 · number of calls"), ("read tokens", "1 · tokens read"), ("+ write tokens × 5", "2 · tokens written"),
             ("× price", "5 · unit price"), ("÷ success rate", "4 · failures, retries"), ("+ machine hours", "6 · the machines")]
    out = ['<div class="eqstrip"><div class="eqt">money per task =</div>']
    for t, c in terms:
        out.append(f'<div class="eqterm"><div class="eqx">{html.escape(t)}</div><div class="eqc">{html.escape(c)}</div></div>')
    return "".join(out) + "</div>"

def link_fig():
    """Two equations with terms coloured by their relationship (page 16)."""
    def pill(txt, kind):
        return f'<span class="lp {kind}">{html.escape(txt)}</span>'
    t = [pill("N steps","same"), pill("c calls","same"), "× (", pill("queue","time"), "+", pill("read","same"), "+", pill("write","same"), ") +", pill("observe","time"), "+", pill("act","time"), "+", pill("wait","time")]
    m = [pill("N steps","same"), pill("c calls","same"), "× (", pill("read tokens","same"), "×", pill("price","buy"), "+", pill("write tokens","same"), "× 5 ×", pill("price","buy"), ") ÷", pill("success rate","same")]
    return ('<div class="linkfig"><div class="lrow"><span class="lk">time</span>' + " ".join(t) + '</div>'
            '<div class="lrow"><span class="lk">money</span>' + " ".join(m) + '</div>'
            '<div class="lleg"><span class="lp same">in both equations — same source</span><span class="lp time">time equation only — slow but not expensive</span><span class="lp buy">the price — money for time or accuracy</span></div></div>')

SLIDES = []   # dicts: id, label, title, hl, crumb, callout(html), body(html), foot, chip(href,text), notes, kind

def slide(id_, title, body, *, label=None, hl=(), crumb="", callout="", foot="", chip=None, notes="", kind="main", cover=False):
    SLIDES.append(dict(id=id_, title=title, body=body, label=label, hl=hl, crumb=crumb, callout=callout,
                       foot=foot, chip=chip, notes=notes, kind=kind, cover=cover))

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
    "ufo2": "Zhang et al., 2025",
    "hal": "Kapoor et al., 2025",
    "tracelab": "Zhu et al., 2026",
    "anth-a": "Anthropic, 2026a",
    "anth-b": "Anthropic, 2026b",
    "openai": "OpenAI, 2026",
    "aa": "Artificial Analysis, 2026",
    "code": "xlang-ai, 2026",
    "jit": "Winston et al., 2026",
    "axis": "Lu et al., 2025",
    "bgym": "Le Sellier De Chezelles et al., 2025",
    "meta": "Meta, 2026",
    "openai25": "OpenAI, 2025",
}
def ci(*keys):
    return "(" + "; ".join(CITE[k] for k in keys) + ")"

# =====================================================================
# PART 1 — where the time and the money go
# =====================================================================

# --- 01 cover -----------------------------------------------------------
slide("s01", "Where the time and the money go", cover=True,
      body=f"""
<div class="cover">
  <div class="cover-l">
    <div class="cover-kicker">Agent acceleration · Part 1 of 2</div>
    <h1 class="cover-title">Where the time and the money go</h1>
    <p class="cover-sub">Why LLM agents that operate software are slow and expensive, and how the two are linked.</p>
    <p class="cover-sub2">Every number comes from a published measurement of a computer-use, web or coding agent, or from a vendor’s own price page (2024–2026); the conditions of each measurement are stated next to it, and the full references are at the end of the part.</p>
    <p class="cover-date">September 2026</p>
  </div>
  <div class="cover-r">
    <div class="cover-fig-title">The loop every agent runs — Part 1 puts a number on each term</div>
    {loop_svg(cls="cover-svg")}
    <div class="cover-fig-cap">read: the prompt is processed all at once · write: the answer comes out one token at a time · N passes, c model calls per pass</div>
  </div>
</div>""",
      notes="""封面。这一部分对应文档《Agent 慢和贵的逻辑链》。讲法：先把循环讲清（第 2 页），再把慢的五类、贵的六类各给一页总览加几页代表性例子，最后讲两者怎么连、修什么能省什么、还有什么没人测过。所有文献细节表放在附录 A1–A6。""")

# --- 02 the loop --------------------------------------------------------
slide("s02", "The loop, with every term on it",
      crumb="here: the loop and its two equations → to: why the reading term grows fastest",
      callout=f"""
<p><b>One task = one loop run N times.</b> Each pass observes the screen or page, makes at least one model call, acts, and waits. A call has three segments: <b>queueing</b> at the provider; <b>reading</b> the prompt — all tokens processed together, cheap per token; <b>writing</b> the answer — one token at a time, about 12&nbsp;ms each (81.7 tokens per second measured for Claude Opus 5.5, {CITE['aa']}) and 5× the read price.</p>
<p><b>Observation, action, waiting and queueing enter only the time equation; read and write tokens enter both.</b> That asymmetry is the whole structure behind “how slow and expensive are linked”.</p>""",
      body=f"""
<div class="fig-mid">{loop_svg(cls="big-svg")}</div>
<div class="sym">
  <div><span class="sk">N</span>passes — task length, action granularity, idling</div>
  <div><span class="sk">c</span>model calls per pass — the <b>harness</b> (the program around the model): one call, or plan + judge + reflect</div>
  <div><span class="sk">read</span>tokens read per call — history length, screenshot size</div>
  <div><span class="sk">write</span>tokens written per call — thinking mode, model size</div>
  <div><span class="sk">price</span>model tier, fast mode, cache (a cached read costs 0.1×)</div>
  <div><span class="sk">observe · act · wait</span>environment time — browser, desktop sandbox, fixed sleeps</div>
</div>""",
      foot=f"SOURCES · output speed: {CITE['aa']} (third-party measurement) · prices: {CITE['anth-b']}; {CITE['openai']}",
      chip=("#a1-1", "Appendix A1"),
      notes="""对应文档零节。读 = prefill（并行），写 = decode（逐 token），Opus 5.5 实测 81.7 token/s [E208]；写的单价是读的 5 倍（定价页）。时间式子里的观察、执行、等待、排队不进钱的式子，读写 token 两个式子都进——这是“慢和贵怎么连”的底层结构（第 16 页再用）。“harness”一词在这页定义：模型外面那套程序，它决定每步调几次、观察多大、停不停。""")

# --- 03 quadratic -------------------------------------------------------
def quad_chart():
    N = 20
    reads = [n*(n+1)//2 for n in range(1, N+1)]
    writes = list(range(1, N+1))
    ox, oy, w, h = 82, 24, 550, 240
    maxv = 210
    def y(v): return oy + h - v/maxv*h
    s = ['<svg class="chart" viewBox="0 0 660 320" xmlns="http://www.w3.org/2000/svg">']
    for v in (0, 55, 105, 155, 210):
        s.append(f'<line class="grid" x1="{ox}" y1="{y(v):.1f}" x2="{ox+w}" y2="{y(v):.1f}"/>')
        s.append(f'<text class="ax" x="{ox-8}" y="{y(v)+4:.1f}" text-anchor="end">{v}</text>')
    bw = w/N
    for i in range(N):
        n = i+1
        x = ox + i*bw
        s.append(f'<rect class="b-read" x="{x+2:.1f}" y="{y(reads[i]):.1f}" width="{bw*0.42:.1f}" height="{oy+h-y(reads[i]):.1f}"/>')
        s.append(f'<rect class="b-write" x="{x+2+bw*0.46:.1f}" y="{y(writes[i]):.1f}" width="{bw*0.42:.1f}" height="{oy+h-y(writes[i]):.1f}"/>')
        if n in (1, 5, 10, 15, 20):
            s.append(f'<text class="ax" x="{x+bw/2:.1f}" y="{oy+h+16}" text-anchor="middle">{n}</text>')
    s.append(f'<text class="ax" x="{ox+w/2}" y="{oy+h+36}" text-anchor="middle">steps taken, N</text>')
    s.append(f'<text class="ax" x="{ox-8}" y="{oy-8}" text-anchor="end">step-units</text>')
    s.append(f'<rect class="b-read" x="{ox+14}" y="{oy+2}" width="12" height="12"/><text class="ax" x="{ox+30}" y="{oy+13}">tokens read, cumulative = N(N+1)/2</text>')
    s.append(f'<rect class="b-write" x="{ox+14}" y="{oy+22}" width="12" height="12"/><text class="ax" x="{ox+30}" y="{oy+33}">tokens written, cumulative = N</text>')
    s.append('</svg>')
    return "".join(s)

slide("s03", "Reading grows with the square of the steps; writing only linearly",
      hl=("n-read", "n-steps", "n-rtok"),
      crumb="from the loop → here: the shape of the reading term → to: the five sources of slowness",
      callout=f"""
<p><b>Writing</b> per step is roughly constant, so N steps write about N × W tokens — linear.</p>
<p><b>Reading</b> at step k re-sends the k−1 earlier screenshots and messages — one screenshot is 1,000–1,800 tokens {ci('anth-a')} — so the sum over a task is about N²/2 times the tokens added per step: 10 steps read 55 step-units of history, 20 steps read 210 (calc.). Doubling the steps roughly quadruples the reading and only doubles the writing.</p>
<p>This assumes the full history is re-sent with no cache. Trimming history flattens the curve; prompt caching cuts the read price to 0.1× but leaves the shape.</p>""",
      body=f"""
<div class="two">
  <div>{quad_chart()}<div class="figcap">Tokens read and written over a task, in units of “tokens added per step”, if every step re-sends the whole history (calc.).</div></div>
  <div class="stack">
    {card("MEASURED ON REAL RUNS", "Cost “grows quadratically with the number of steps”",
          "Step-by-step accounting of two multi-call harnesses (GTA1, Agent S2) on 39 OSWorld desktop tasks; the later steps are up to 3× slower than the early ones because the prompt at step k carries the k−1 earlier screenshots — “dominated by prefill”, the reading segment.",
          ci('osh'))}
    {card("WHAT IT MEANS FOR ACCELERATION", "The cheapest token is the one never re-read",
          "Any method that shortens the history, shrinks each observation, or avoids a pass altogether attacks the fastest-growing term; a faster model only scales the per-token constant.")}
  </div>
</div>""",
      foot=f"SOURCES · {CITE['osh']} · {CITE['anth-a']} · calc. = our own arithmetic",
      notes="""对应文档零节最后一段。R_k ≈ k × 每步新增，求和 ≈ N²/2；10 步 55 份、20 步 210 份（calc.）。前提是全量重发无缓存：裁历史压到平方以下，缓存只打折不改形状。实测：OSWorld-Human 的“成本随步数二次增长”[E45]；靠后的步最多慢 3 倍、“由 prefill 主导”[E23]；截图 1,000–1,800 tokens [E31]。""")

# --- 04 five sources overview ------------------------------------------
slide("s04", "Slowness has five sources",
      hl=("n-steps", "n-calls", "n-queue", "n-read", "n-write", "n-observe", "n-act", "n-wait"),
      crumb="from the two equations → here: every cause of slowness, in five classes → to: one class per page",
      callout="""<p><b>Four of the five are terms of the time equation; the fifth is the structure that adds them up.</b> Which class dominates depends on the harness, not on the kind of agent (page 10). Every cause on the next pages has an entry in Appendix A1 with its measurement conditions.</p>""",
      body=f"""
{eq_strip()}
<div class="rows5 big">
  {card("I · TOO MANY STEPS (N)", "318 tool calls per task",
        "Hour-scale tasks take hundreds of passes: 318 tool calls per task on OSWorld 2.0 with one action per step (Claude Opus 4.7, 108 tasks); in a median text-agent task two thirds of the steps are pure navigation.", ci('osw2','skim'))}
  {card("II · TOO MANY CALLS PER STEP (c)", "4–12 planning calls per judging call",
        "Harnesses that plan, judge and reflect make several calls per pass; sampling candidates multiplies them again; a coding agent makes 6.6 model calls per user turn.", ci('osh','copilot'))}
  {card("III · EACH CALL IS SLOW", "Queue, read, write, think",
        "Identical requests vary up to 69× in latency by time of day; reading gets slower every step (up to 3×); writing one token at a time takes 91–98.6% of model time once the cache is warm; thinking modes multiply the writing.", ci('bian','osh','yuan'))}
  {card("IV · THE ENVIRONMENT IS SLOW", "3–26 s per observation · 6.6 s per browser action",
        "Building an accessibility tree, executing in the browser, sleeping a fixed 2–3 s after every action, and tool runs with a long tail: 4% of tool calls take 85% of tool time.", ci('osh','skim','tracelab'))}
  {card("V · EVERYTHING IS SERIAL", "concurrency within a turn: 1.15",
        "Observe, decide, act and wait run strictly one after another, so task time is the sum of the four classes above; fixing one term saves only its own share — which is why the shares (page 10) must be known before anything is accelerated.", ci('copilot'))}
</div>""",
      foot="SOURCES · one representative number per class; the complete tables with conditions are in Appendix A1",
      chip=("#a1-1", "Appendix A1"),
      notes="""对应文档第一节的五类总览。每类一个代表数：I [E6][E17]；II [E25][E20]；III [E101][E23][E29]；IV [E24][E17][E19]；V [E20] 并发 1.15。第五类是结构性乘数：时间是各项之和，不是最大值，所以必须先知道占比（第 10 页）才能谈加速。""")

# --- 05 class I ---------------------------------------------------------
slide("s05", "I · Too many steps",
      hl=("n-steps",),
      crumb="from the five classes → here: why the number of passes N gets large → to: calls per step",
      callout="""<p><b>N multiplies everything.</b> It gets large in five ways: the task is long; each pass does a single action; navigation-only passes still go through the model; the agent idles or loops; it acts on a stale screen and has to redo the work.</p>""",
      body=f"""
<div class="cards4">
  {card("I-1, I-2 · LONG TASKS, ONE ACTION PER PASS", "318 tool calls per task, mean",
        "OSWorld 2.0, 108 long desktop tasks, Claude Opus 4.7 with maximum thinking, one action per step, 500-step cap. Letting one call issue several actions cuts the same model to 160.7 steps and Claude Opus 4.8 to 103 steps (481.8 calls).", ci('osw2'))}
  {card("I-3 · NAVIGATION-ONLY PASSES", "66.7% of steps are pure navigation",
        "Median task across 151 WebVoyager tasks on live websites, three text agents (Browser-Use, AgentOccam, WebVoyager) driven by GPT-4o: paging, scrolling and opening the next page each cost a full model call.", ci('skim'))}
  {card("I-4 · IDLING AND DEAD LOOPS", "66% of steps wasted; one loop = 27 min, $8.47",
        "GTA1 harness (o3 plans and judges, GTA1-7B locates elements) on 39 OSWorld desktop tasks: in failed tasks that ran past 50 steps, 66% of steps were repeats; one element-locating loop repeated the same step 18 times — 27 minutes and $8.47 at list price without caching.", ci('osh'))}
  {card("I-5 · ACTING ON A STALE SCREEN", "a recorded failure mode, share not reported",
        "A screenshot taken before the page has changed leads to a click on the old layout and a repair afterwards; OSWorld 2.0 records “stale interface state” as one of its failure modes but gives no share.", ci('osw2'))}
</div>
<div class="figs3">
  {hbars("Steps per task on OSWorld 2.0, 108 tasks", [("Opus 4.7 · one action per step",318,"318"),("Opus 4.7 · batched actions",160.7,"160.7"),("Opus 4.8 · batched",103,"103"),("GPT-5.5 · batched",95.2,"95.2")], "XLANG Lab, 2026 · mean over tasks", labelw=170)}
  {hbars("Steps in the median WebVoyager task, 151 live-site tasks, GPT-4o", [("navigation only",66.7,"66.7%"),("needs a decision",33.3,"33.3%")], "Wong et al., 2026", labelw=120)}
  {hbars("Steps in failed OSWorld tasks that ran past 50 steps, GTA1", [("repeated, no progress",66,"66%"),("other",34,"34%")], "Abhyankar, Qi & Zhang, 2026", labelw=140)}
</div>""",
      foot=f"SOURCES · {CITE['osw2']} · {CITE['skim']} · {CITE['osh']} — conditions as stated on each card; full rows in Appendix A1",
      chip=("#a1-1", "Appendix A1"),
      notes="""文档第一节第一类 I-1…I-5。I-1/I-2 [E6]：Opus 4.7 单动作 318 步，批量 160.7；Opus 4.8 批量 103 步（481.8 次调用）。I-3 [E17]：Skim 剖析，中位任务 66.7% 纯导航。I-4 [E45]：失败且超 50 步的任务里 66% 是无效重复；一次定位死循环 18 次、27 分钟、$8.47（挂牌价、无缓存）。I-5 [§1.8]：stale interface state，只知存在不知比例（第 18 页缺口）。""")

# --- 06 class II --------------------------------------------------------
slide("s06", "II · Too many calls per step",
      hl=("n-calls",),
      crumb="from the number of passes → here: model calls per pass, c → to: what happens inside one call",
      callout="""<p><b>c multiplies N.</b> A harness that plans, judges and reflects makes several calls per pass; sampling several candidate actions per step multiplies the calls again; coding agents call the model many times inside one user turn.</p>""",
      body=f"""
<div class="cards3">
  {card("II-1 · PLAN + JUDGE + REFLECT", "4–12 planning calls per judging call",
        "GTA1 runs four parallel planners per step, retries up to three rounds, then one judging call picks; Agent S2 adds a reflection call per step, so planning takes 53% and reflection 34% of task time. Both measured step by step on 39 OSWorld desktop tasks.", ci('osh'))}
  {card("II-2 · SAMPLING CANDIDATES", "1 → 10 candidates: 38.8% → 43.2% success for 9.6× the tokens",
        "Same model and harness (gpt-oss-120b, one-call-per-step ReAct) on 165 WebArena-Lite tasks; tokens per task rise from 96K to 920K, i.e. 9.6× the tokens for 4.4 points of accuracy.", ci('atts'))}
  {card("II-3 · CODING AGENTS", "6.6 model calls per user turn",
        "GitHub Copilot coding agent, production telemetry for the first week of June 2026, 13.5 million sessions: the model is called back and forth several times before the turn ends.", ci('copilot'))}
</div>
<div class="figs3">
  {hbars("Model calls per step in the GTA1 harness, per judging call", [("planning, no retry",4,"4"),("planning, 3 retry rounds",12,"12"),("judging",1,"1")], "Abhyankar, Qi & Zhang, 2026 · 4 parallel planners, up to 3 rounds", labelw=160)}
  {hbars("Tokens per task vs candidates per step, WebArena-Lite, gpt-oss-120b", [("1 candidate · 38.8% success",96,"96K"),("10 candidates · 43.2% success",920,"920K")], "Lee et al., 2026 · 165 tasks", labelw=180)}
  {hbars("Model calls per user turn, GitHub Copilot coding agent", [("mean, 13.5 M sessions",6.6,"6.6")], "Liu et al., 2026 · production telemetry, June 2026", labelw=150, maxv=8)}
</div>""",
      foot=f"SOURCES · {CITE['osh']} · {CITE['atts']} · {CITE['copilot']} (the Copilot data is the company’s own telemetry)",
      chip=("#a1-1", "Appendix A1"),
      notes="""文档第一节第二类。II-1 [E25][E22]：GTA1 每步 4 个并行规划器、最多重试 3 轮、1 次判断，所以 1 次判断对应 4–12 次规划；Agent S2 规划 53%、反思 34%。II-2 [E44]：候选 1→10，38.8%→43.2%，token 9.6 万→92 万。II-3 [E20]：Copilot 遥测每回合 6.6 次调用。""")

# --- 07 class III (queue, read) ----------------------------------------
slide("s07", "III · Each call is slow: queueing and reading",
      hl=("n-queue", "n-read"),
      crumb="from calls per step → here: the first two segments of a call → to: writing, thinking, model size",
      callout="""<p><b>Two segments before a single token is produced.</b> Queueing at the provider costs nothing but counts as model time. Reading re-processes the entire history on every call, so it grows with the step number, with the size of each observation, and with whatever the cache failed to keep.</p>""",
      body=f"""
<div class="cards3">
  {card("III-1 · QUEUEING", "up to 69× latency spread for the same request",
        "Client-side measurement of 15 models across 5 providers: requests of equal length, sent at different times of day, differ in latency by up to 69×. Not billed; usually reported as “model time”.", ci('bian'))}
  {card("III-2 · READING GROWS WITH THE STEP", "later steps up to 3× slower · 4.8× input when the observation is rich",
        "OSWorld-Human: in the multi-call harnesses the prompt at step k carries the k−1 earlier screenshots, and the authors attribute the slowdown to the reading segment (“dominated by prefill”). AgentSysBench: switching one WebArena agent (Kimi-K2.6) from a single observation format to accessibility tree (the text list of on-screen elements) + HTML + screenshot multiplied the input 4.8× and raised the model’s share of time from 46.9% to 61.6%.", ci('osh','asb'))}
  {card("III-2 · WHEN THE CACHE IS EVICTED", "request latency up to 7.14× under load",
        "SWE-Agent and OpenHands running GLM-4.6 on 8 H100s for SWE-bench Lite: as concurrency rises the cache of already-read prompt (the KV cache) is evicted and re-read, and request latency rises up to 7.14×.", ci('thunder'))}
</div>
<div class="figs3">
  {hbars("Latency of identical requests by time of day, 15 models, 5 providers", [("best time",1,"1×"),("worst time",69,"up to 69×")], "Bian et al., 2025 · measured from the client", labelw=90)}
  {hbars("Model share of step time as the observation grows, WebArena, Kimi-K2.6", [("one format",46.9,"46.9%"),("three formats · 4.8× input",61.6,"61.6%")], "Chang et al., 2026 · AgentSysBench · accessibility tree + HTML + screenshot", labelw=120, maxv=100)}
  {hbars("Request latency when the cache is evicted, GLM-4.6 on 8 H100s", [("light load",1,"1×"),("cache thrash under load",7.14,"up to 7.14×")], "Kang et al., 2026 · SWE-bench Lite", labelw=150)}
</div>""",
      foot=f"SOURCES · {CITE['bian']} · {CITE['osh']} · {CITE['asb']} · {CITE['thunder']}",
      chip=("#a1-2", "Appendix A1"),
      notes="""文档第一节第三类 III-1、III-2。III-1 [E101]：Bian 等从客户端测 15 模型 5 提供商，同长度请求延迟最多差 69 倍。III-2 [E23]：靠后的步最多慢 3 倍、由 prefill 主导；[E98] AgentSysBench 观察换成 AXTree+HTML+截图，输入 4.8 倍，模型时间占比 46.9%→61.6%；[E108] ThunderAgent 缓存抖动延迟最多 7.14 倍。""")

# --- 08 class III (write, think) ---------------------------------------
slide("s08", "III · Each call is slow: writing, thinking, model size",
      hl=("n-write",),
      crumb="from queueing and reading → here: the writing segment → to: the environment",
      callout="""<p><b>Writing is one token at a time, so it is the slowest segment per token and the most expensive.</b> Thinking modes add tokens that are written before the answer; larger models take longer per token. Neither reliably buys accuracy.</p>""",
      body=f"""
<div class="cards3">
  {card("III-3 · WRITING DOMINATES A WARM CALL", "91–98.6% of model time",
        "One-call-per-step ReAct agents on five benchmarks, Qwen3.6-27B and Gemma4-31B served locally (vLLM serving engine, 2 H100s): with the cache warm, token-by-token generation takes 91–98.6% of the model’s time. Desktop agent UFO2 (GPT-4o / o1 API): about 10 s per model call, the largest item in every configuration.", ci('yuan','ufo2'))}
  {card("III-4 · THINKING MODES", "224K vs 37K output tokens per task",
        "Same 108 OSWorld 2.0 tasks: Claude Opus 4.8 writes 224,000 output tokens per task, GPT-5.5 writes 37,000; the writing is billed as output and, on Claude Opus 5.5, cannot be switched off.", ci('osw2','anth-b'))}
  {card("III-4 · MORE THINKING ≠ MORE ACCURATE", "accuracy fell in 21 of 36 comparisons",
        "Holistic Agent Leaderboard: 9 benchmarks, 21,730 runs; raising the reasoning effort lowered accuracy in 21 of the 36 model–benchmark pairs while adding output tokens.", ci('hal'))}
</div>
<div class="figs3">
  {hbars("Output tokens per task on the same 108 OSWorld 2.0 tasks", [("Claude Opus 4.8",224,"224K"),("GPT-5.5",37,"37K")], "XLANG Lab, 2026", labelw=110)}
  {hbars("Share of model time spent writing, warm cache, local 27–31B models", [("lowest of five benchmarks",91,"91%"),("highest",98.6,"98.6%")], "Yuan et al., 2026 · Qwen3.6-27B / Gemma4-31B, vLLM, 2 H100s", labelw=160, maxv=100)}
  {hbars("Raising the reasoning effort: 36 model–benchmark pairs, HAL", [("accuracy fell",21,"21"),("accuracy rose or held",15,"15")], "Kapoor et al., 2025 · 9 benchmarks, 21,730 runs", labelw=140)}
</div>""",
      foot=f"SOURCES · {CITE['yuan']} · {CITE['ufo2']} · {CITE['osw2']} · {CITE['anth-b']} · {CITE['hal']}",
      chip=("#a1-2", "Appendix A1"),
      notes="""文档第一节第三类 III-3、III-4。III-3 [E29]：本地 Qwen3.6-27B / Gemma4-31B，缓存不被挤时 decode 占模型时间 91–98.6%；[E94] UFO2 每次调用约 10 秒。III-4 [E41]：Opus 4.8 每任务输出 22.4 万 token vs GPT-5.5 3.7 万；Opus 5.5 思考关不掉、按输出计费（Anthropic 2026b）；[E43] HAL 36 组里 21 组调高推理强度准确率反降。""")

# --- 09 class IV + V ----------------------------------------------------
slide("s09", "IV · The environment is slow; V · nothing overlaps",
      hl=("n-observe", "n-act", "n-wait"),
      crumb="from the model call → here: the three environment terms and the serial structure → to: which term dominates",
      callout="""<p><b>Four environment terms and one structural multiplier.</b> Observation: building the accessibility tree (the operating system’s text list of on-screen elements). Execution: the browser and the page load. Fixed sleeps: the agent cannot tell when a page is ready. Tool tails: tests and builds. And all of it runs strictly in sequence.</p>""",
      body=f"""
<div class="cards4">
  {card("IV-1 · OBSERVATION", "3–26 s per accessibility tree",
        "OSWorld desktop applications; the screenshot itself is under 2% of task time. In UFO2, OmniParser element detection adds about 1 s per step.", ci('osh','ufo2'))}
  {card("IV-2, IV-3 · BROWSER AND FIXED SLEEPS", "6.6 s browser vs 4.7 s model per step · 2–3 s sleep after every action",
        "Medians over 151 WebVoyager live-site tasks with GPT-4o. OSWorld’s environment code sleeps 2 s after each action and OSWorld 2.0 prescribes 3 s: 318 steps ≈ 16 minutes of pure waiting (calc.); a single-call GUI agent (Kimi-K2.6) spends over 70% of its OSWorld time inside the desktop sandbox.", ci('skim','code','osw2','asb'))}
  {card("IV-4 · TOOL TAILS", "4% of tool calls take 85% of tool time",
        "4,265 Claude Code and Codex sessions from 43 developers, September 2025 – June 2026: a request averages 4.3 minutes, of which tools take 2.5 (59.8%) and the model 1.7 (41.0%).", ci('tracelab'))}
  {card("V · SERIAL", "concurrency within a turn: 1.15",
        "Copilot telemetry. Because the four stages never overlap, task time is the sum of every term above, not the largest one; fixing one term saves only its own share. Caution when reading “total time”: 80–92% of a coding session’s elapsed time is the human thinking between turns.", ci('copilot','tracelab'))}
</div>
<div class="figs3">
  {hbars("Seconds per step, median, 151 WebVoyager live-site tasks, GPT-4o", [("browser action",6.6,"6.6 s"),("model call",4.7,"4.7 s")], "Wong et al., 2026", labelw=110)}
  {hbars("Where a Claude Code / Codex request’s 4.3 minutes go", [("tools",59.8,"59.8%"),("model",41.0,"41.0%")], "Zhu et al., 2026 · 4,265 sessions, 43 developers", labelw=70, maxv=100)}
  {hbars("Tool calls longer than one minute", [("share of tool calls",4,"4%"),("share of tool time",85,"85%")], "Zhu et al., 2026", labelw=130, maxv=100)}
</div>""",
      foot=f"SOURCES · {CITE['osh']} · {CITE['ufo2']} · {CITE['skim']} · {CITE['code']} · {CITE['osw2']} · {CITE['asb']} · {CITE['tracelab']} · {CITE['copilot']}",
      chip=("#a1-3", "Appendix A1"),
      notes="""文档第一节第四、五类。IV-1 [E24][E22][E94]。IV-2 [E17] 浏览器 6.6 s vs 模型 4.7 s（中位）；IV-3 [E111] OSWorld 代码每动作停 2 秒，OSWorld 2.0 规定 3 秒，318 步≈16 分钟（calc.）；[E97] 单次调用 GUIAgent 70% 以上时间在 sandbox。IV-4 [E19][E105]。V [E20] 并发 1.15；人思考时间 80–92% [E105][E106] 要先剔掉。""")

# --- 10 where the arrows land -------------------------------------------
slide("s10", "Which term dominates depends on the harness, not on the kind of agent",
      hl=("n-read", "n-wait", "n-write"),
      crumb="from the five classes → here: the shares, per kind of agent → to: the six sources of cost",
      callout="""<p><b>All five classes exist in every agent, but the heaviest term differs, and it flips when the harness changes.</b> The one multiplier common to all three kinds is the number of passes, N.</p>""",
      body=f"""
<table class="tbl three">
<colgroup><col style="width:9%"><col style="width:31%"><col style="width:30%"><col style="width:30%"></colgroup>
<thead><tr><th></th><th>Screenshot desktop agent, multi-call harness</th><th>Text web agent</th><th>Coding agent with a prompt cache</th></tr></thead>
<tbody>
<tr><td class="rk">heaviest</td>
<td><b>Reading × calls per step × steps.</b> 87–97% of task time in planning, judging and reflection calls; screenshots and actions together under 3.5% (GTA1 and Agent S2 on 39 OSWorld tasks) {ci('osh')}</td>
<td><b>Browser execution and waiting.</b> Median per step: browser action 6.6 s, model call 4.7 s (151 WebVoyager live-site tasks, GPT-4o) {ci('skim')}</td>
<td><b>Writing, or tool tails, depending on the tools.</b> Token-by-token generation is 91–98.6% of model time {ci('yuan')}; Claude Code / Codex requests: tools 59.8%, model 41.0% {ci('tracelab')}; Copilot: model 13.7%, tools 2% {ci('copilot')}</td></tr>
<tr><td class="rk">second</td>
<td>Writing: thinking tokens lengthen every call</td>
<td>Reading, once the observation grows: 4.8× input moved the model’s share from 46.9% to 61.6% {ci('asb')}; the Browser-Use harness spends 73% of its latency in model calls {ci('jit')}</td>
<td>Reading, when load evicts the cache: request latency up to 7.14× {ci('thunder')}</td></tr>
<tr><td class="rk">negligible</td>
<td>Observation and action: under 3.5% together {ci('osh')}</td>
<td>Nothing: model and browser are close; which is larger depends on observation size and model speed</td>
<td>Navigation-only steps: there are no pages to turn</td></tr>
<tr><td class="rk">counter-example</td>
<td>A single-call GUI agent spends over 70% of its time in the sandbox, because the benchmark sleeps 2–3 s after every action {ci('asb','code','osw2')}</td>
<td>Browser-Use: 73% of latency in the model, not the browser {ci('jit')}</td>
<td>The two production records point opposite ways — heavy tools (tests, builds) vs light tools (file reads); the difference is the tools, not a contradiction</td></tr>
<tr><td class="rk">in one line</td>
<td>Slow in reading: every pass re-reads the growing screenshot history</td>
<td>Slow in the environment, until the observation grows — then slow in reading</td>
<td>Reading is cached away; slow in writing and in the tools</td></tr>
</tbody></table>
<div class="concl">
  <div><b>1 · The harness sets the dominant term</b> — calls per step, observation size, fixed sleeps, cache on or off. “Agents are slow because inference is slow” holds only for multi-call screenshot agents.</div>
  <div><b>2 · N multiplies every term</b> — one pass fewer saves a whole pass of time and money in all three kinds; it is the only lever common to all of them, and the reason OSWorld 2.0’s authors list “fewer environment rounds” as a goal in its own right.</div>
</div>""",
      foot="SOURCES · as cited in each cell; the same table with every measurement condition is Appendix A2",
      chip=("#a2-1", "Appendix A2"),
      notes="""文档第二节。三种 agent 的大头：截图型多调用 87–97% 在模型 [E22]；文本型浏览器 6.6 s vs 模型 4.7 s [E17]；coding decode 91–98.6% [E29]、工具 59.8% vs 模型 41.0% [E105]、Copilot 模型 13.7% vs 工具 2% [E106]。次重：[E98][E100][E108]。反例：[E97][E111][E6]、[E100]。两个结论：大头由框架决定（D95、D96、D99）；步数 N 乘在所有项前面（§1.8）。""")

# --- 11 six sources of cost ----------------------------------------------
slide("s11", "Cost has six sources",
      hl=("n-rtok", "n-wtok", "n-price", "n-succ", "n-calls", "n-steps"),
      crumb="from where the time goes → here: every cause of cost, in six classes → to: one class per page",
      callout=f"""<p><b>Money comes from two things only: tokens read and tokens written, each times a price.</b> Three ratios to remember — writing costs 5× reading; a cached read costs 0.1×; fast mode costs 2× {ci('anth-b','openai')}. Three of the remaining sources are multipliers on those two tokens; the last is the one nobody counts.</p>""",
      body=f"""
{cost_strip()}
<div class="rows6">
  {card("1 · TOKENS READ", "quadratic in the steps",
        "History re-sent every call; 1,000–1,800 tokens per screenshot; rich observations 4.8×; sampling 96K → 920K tokens; and a cache that keeps 95.7% of the prefix still leaves prefix tokens at 59.5% of the bill.", ci('osh','anth-a','asb','atts','tracelab'))}
  {card("2 · TOKENS WRITTEN", "5× the price, billed even when it is thinking",
        "224K output tokens per task (Claude Opus 4.8) vs 37K (GPT-5.5) on the same tasks; yet in an uncached screenshot agent output was only 31% of the total bill.", ci('osw2','osh'))}
  {card("3 · NUMBER OF CALLS", "N × c multiplies both",
        "5–13× the calls of a single-call harness per step (GTA1, calc.); sampling 5–20 candidates per step multiplies calls by the candidate count.", ci('osh','atts'))}
  {card("4 · FAILURES AND RETRIES", "$72.4 per attempt → ≈ $351 per success",
        "Cost per success = cost per attempt ÷ success rate: OSWorld 2.0’s best agent completes 20.6% of tasks (calc.; an accounting conversion). Idle loops are billed in full: one loop, $8.47.", ci('osw2','osh'))}
  {card("5 · UNIT PRICE", "$4 / $20 vs $0.10 / $0.50 per million tokens",
        "Claude Opus 5.5 vs GPT-6 Luna, read / write; fast mode 2×; cache write 1.25×, cache read 0.1×; OpenAI charges 2× the read price above 272K tokens.", ci('anth-b','openai'))}
  {card("6 · THE MACHINES", "0.3–4.6% of the API bill (CPU environments, calc.)",
        "No benchmark reports a dollar figure for the sandbox, browser or VM; computed from hourly list prices, a CPU environment for a one-hour task costs $0.02–0.36.", "vendor price pages, read 2026-09-27")}
</div>""",
      foot="SOURCES · one representative number per class; the complete tables with conditions are in Appendix A3",
      chip=("#a3-1", "Appendix A3"),
      notes="""文档第三节总览。三个比例：写 = 读 × 5；缓存读 0.1 倍；fast mode 2 倍（Anthropic 2026b；OpenAI 2026，2026 年 9 月定价页）。第一类 [E45][E31][E98][E44][E19]；第二类 [E41][D7]；第三类 [E25][E44]；第四类 [E41] $72.4/20.6%≈$351（calc.）、[E45] $8.47；第五类定价页 [E190][E192]；第六类见追加调查 7（E212–E223）。""")

# --- 12 tokens read and written -------------------------------------------
slide("s12", "1–2 · Tokens read and tokens written",
      hl=("n-rtok", "n-wtok"),
      crumb="from the six classes → here: the two token bills → to: the three multipliers",
      callout="""<p><b>Reading is the larger bill in a screenshot agent; writing is the dearer token.</b> The read bill grows with the square of the steps and is not removed by caching; the write bill is inflated by thinking modes, which are billed as output.</p>""",
      body=f"""
<div class="cards3">
  {card("READ · WHY IT GROWS", "quadratic history · 1,000–1,800 tokens per screenshot · 4.8× rich observations · 9.6× sampling",
        "Every call re-reads the k−1 earlier screenshots; 100 screenshots fill a 200K-token context; accessibility tree + HTML + screenshot multiplies the input 4.8×; 10 candidates per step take tokens per task from 96K to 920K.", ci('osh','anth-a','asb','atts'))}
  {card("READ · CACHING IS NOT A CURE", "95.7% hit rate, yet prefix tokens are 59.5% of the bill",
        "4,265 Claude Code / Codex sessions: the prefix cache hits 95.7% of the time, but each step reads a history of a hundred thousand-plus tokens, so even at 0.1× the price the prefix is 59.5% of the list-price cost; on a miss the re-read is 3.8× the genuinely new content.", ci('tracelab'))}
  {card("WRITE · THINKING IS BILLED AS OUTPUT", "224K vs 37K output tokens per task · but only 31% of an uncached bill",
        "Same 108 OSWorld 2.0 tasks, Claude Opus 4.8 vs GPT-5.5; on Claude Opus 5.5 “thinking cannot be disabled and is billed as output”. In the uncached GTA1 runs the paper’s $2.43 per task counts output only; all tokens from its Table 3 give $7.87, so output was 31% of the total.", ci('osw2','anth-b','osh'))}
</div>
<div class="figs3">
  {hbars("One uncached screenshot agent’s bill per task, GTA1, 39 OSWorld tasks", [("output tokens only",2.43,"$2.43"),("all tokens",7.87,"$7.87")], "Abhyankar, Qi & Zhang, 2026 · o3 list price, no cache", labelw=130)}
  {hbars("Input tokens per call as the observation grows, WebArena agent", [("single format",1,"1×"),("tree + HTML + screenshot",4.8,"4.8×")], "Chang et al., 2026", labelw=160)}
  {hbars("Share of list-price cost at a 95.7% prefix-cache hit rate", [("cached prefix",59.5,"59.5%"),("new content",40.5,"40.5%")], "Zhu et al., 2026 · Claude Code / Codex sessions", labelw=100, maxv=100)}
</div>""",
      foot=f"SOURCES · {CITE['osh']} · {CITE['anth-a']} · {CITE['asb']} · {CITE['atts']} · {CITE['tracelab']} · {CITE['osw2']} · {CITE['anth-b']}",
      chip=("#a3-1", "Appendix A3"),
      notes="""文档第三节第一、二类。读：Ⅰ-1 [E45] 平方；Ⅰ-2 [E31] 截图 1,000–1,800，100 张撞 200K；Ⅰ-3 [E98] 4.8 倍；Ⅰ-4 [E44] 9.6 万→92 万；Ⅰ-5 [E19] 命中 95.7% 仍占 59.5%，未命中 prefill 3.8 倍。写：Ⅱ-1 [E41] 22.4 万 vs 3.7 万，Opus 5.5 思考关不掉；Ⅱ-2 [D7] $2.43 只算输出、$7.87 全算，输出占 31%。""")

# --- 13 calls, failures, price --------------------------------------------
slide("s13", "3–5 · Calls, failures, and the price list",
      hl=("n-calls", "n-succ", "n-price"),
      crumb="from the token bills → here: what multiplies them → to: four ways of counting the same task",
      callout="""<p><b>Three multipliers sit in front of the token bills.</b> The number of calls (N × c) is the same quantity that made the agent slow; failures turn “per attempt” into “per success”; and the price list decides the constant — including what a speed tier or a long context costs.</p>""",
      body=f"""
<div class="cards3">
  {card("3 · CALLS", "5–13× per step, before sampling",
        "GTA1 makes 4–12 planning calls per judging call, so one step costs 5–13× the calls of a single-call harness (calc.); sampling 5–20 candidates per step multiplies the calls by the candidate count. The same extra calls cost time and money at once.", ci('osh','atts'))}
  {card("4 · FAILURES", "≈ $351 per success · one dead loop $8.47 · evaluation ≈ $40,000",
        "OSWorld 2.0’s best agent, Claude Opus 4.8: about $72.4 per attempt at 20.6% completion, so ≈ $351 per success (calc.; a conversion, not the price of retrying one task until it succeeds). Failed and idle steps are billed in full. Holistic Agent Leaderboard spent about $40,000 on 21,730 runs across 9 benchmarks with a single run per configuration, and did not run Claude Opus 4.1 on Online-Mind2Web because the estimate was $20,000.", ci('osw2','osh','hal'))}
  {card("5 · THE PRICE LIST, SEPTEMBER 2026", "$4 / $20 vs $0.10 / $0.50 per million tokens",
        "Claude Opus 5.5 vs GPT-6 Luna, read / write. Fast mode: 2× on both vendors, and switching to it invalidates the cache. Cache write 1.25×, cache read 0.1×. OpenAI: 2× the read price for requests above 272K tokens.", ci('anth-b','openai'))}
</div>
<div class="figs3">
  {hbars("Cost per attempt vs per success, OSWorld 2.0, Claude Opus 4.8", [("per attempt",72.4,"$72.4"),("per success · ÷ 20.6%, calc.",351,"≈ $351")], "XLANG Lab, 2026 · 108 tasks", labelw=170)}
  {hbars("Write price per million tokens, September 2026 (read price in brackets)", [("Claude Opus 5.5 ($4)",20,"$20"),("GPT-6 Sol ($2)",10,"$10"),("Claude Haiku 4.5 ($1)",5,"$5"),("GPT-6 Luna ($0.10)",0.5,"$0.50")], "Anthropic, 2026b; OpenAI, 2026 · list prices", labelw=140)}
  {hbars("What evaluation costs, Holistic Agent Leaderboard", [("all 21,730 runs",40000,"≈ $40,000"),("one model, one benchmark",20000,"$20,000 est., not run")], "Kapoor et al., 2025 · 9 benchmarks, one run per configuration; Claude Opus 4.1 on Online-Mind2Web was skipped", labelw=150)}
</div>""",
      foot=f"SOURCES · {CITE['osh']} · {CITE['atts']} · {CITE['osw2']} · {CITE['hal']} · {CITE['anth-b']} · {CITE['openai']} — vendor prices are list prices from the vendors’ own pages",
      chip=("#a3-2", "Appendix A3"),
      notes="""文档第三节第三、四、五类。第三类 [E25] 每判断 4–12 次规划，5–13 倍（calc.）；[E44] 多采样。第四类 Ⅳ-1 [E41] $72.4 ÷ 20.6% ≈ $351（calc.，账面折算）；Ⅳ-2 [E45] $8.47；Ⅳ-3 [E43] HAL 约 $40,000、Opus 4.1 估 $20,000 没跑。第五类 Ⅴ-1…Ⅴ-4：定价页 [E190][E192]。""")

# --- 14 four conventions --------------------------------------------------
slide("s14", "Four ways of counting the same task, up to 30× apart",
      hl=("n-price", "n-succ"),
      crumb="from the multipliers → here: the accounting conventions → to: the machines nobody counts",
      callout="""<p><b>“What does one task cost?” has four honest answers, and they differ by up to 30×.</b> The first question back is always: under which convention?</p>""",
      body=f"""
<table class="tbl conv">
<colgroup><col style="width:19%"><col style="width:61%"><col style="width:20%"></colgroup>
<thead><tr><th>convention</th><th>the same run, counted both ways</th><th>gap</th></tr></thead>
<tbody>
<tr><td class="rk">output only vs all tokens</td><td>GTA1 harness (o3 plans and judges; o3 list price $2 read / $8 write per million tokens, no cache) on 39 OSWorld tasks: the paper’s text says $2.43 per task, which counts output tokens only; the input and output tokens of its Table 3 give $7.87 {ci('osh')}</td><td><b>3.2×</b> — same run, same tasks</td></tr>
<tr><td class="rk">per attempt vs per success</td><td>OSWorld 2.0, 108 long tasks, Claude Opus 4.8 with batched actions: about $72.4 per attempt at 20.6% completion; $72.4 ÷ 20.6% ≈ $351 (calc.) {ci('osw2')}</td><td><b>4.9×</b> — an accounting conversion, not the cost of retrying one task to success</td></tr>
<tr><td class="rk">uncached vs cached</td><td>A cached read costs 0.1× on both price lists {ci('anth-b','openai')}; but in 4,265 Claude Code / Codex sessions the prefix cache hit 95.7% and prefix tokens were still 59.5% of the list-price cost, because each step reads a hundred thousand-plus tokens of history {ci('tracelab')}. Screenshot-agent measurements do not report their cache state at all</td><td><b>10×</b> on the read price; the saving on the whole bill is far smaller and depends on the hit rate</td></tr>
<tr><td class="rk">standard vs fast mode</td><td>Anthropic fast mode: Claude Opus 5.5 from $4 / $20 to $8 / $40, Claude Opus 5 and 4.8 from $5 / $25 to $10 / $50 per million tokens; up to 2.5× faster output (vendor-stated), no change to the wait for the first token, and switching invalidates the cache. OpenAI: 2× on every listed model; “up to 2.5×” speed is stated only for GPT-5.6 Sol {ci('anth-b','openai')}</td><td><b>2×</b> — same model, same tokens; only the writing speed is bought</td></tr>
</tbody></table>
<div class="figs3">
  {hbars("The gap each convention opens on the same run", [("output only → all tokens",3.2,"3.2×"),("per attempt → per success",4.9,"4.9×"),("standard → fast mode",2,"2×"),("the three compounded",31.4,"≈ 31× (calc.)")], "3.2 × 4.9 × 2 ≈ 31; the cache ratio (10×) applies to the read price only, so it is not compounded here", labelw=170)}
  {hbars("Read price, cached vs uncached, and what it saved in practice", [("uncached read",1,"1×"),("cached read",0.1,"0.1×"),("prefix share of a real bill, 95.7% hits",0.595,"59.5%")], "Anthropic, 2026b; OpenAI, 2026 · Zhu et al., 2026 — the whole bill fell far less than the price ratio suggests", labelw=230)}
  <div></div>
</div>""",
      foot=f"SOURCES · {CITE['osh']} · {CITE['osw2']} · {CITE['tracelab']} · {CITE['anth-b']} · {CITE['openai']}",
      chip=("#a3-3", "Appendix A3"),
      notes="""文档第三节“四种口径，选错差 30 倍”。只算写 vs 全算 3.2 倍（[D7]，$2.43 vs $7.87）；每次尝试 vs 每次成功 4.9 倍（[E41]，calc.）；无缓存 vs 有缓存：读价差 10 倍，但 [E19] 命中 95.7% 仍占 59.5%，截图型没报缓存状态 [D101]；标准 vs fast mode 2 倍 [E190][E192]。老板问“一个任务多少钱”，先问口径。""")

# --- 15 the machines ------------------------------------------------------
slide("s15", "6 · The machines: not in any benchmark’s dollar figure, but computable",
      hl=("n-wait", "n-act"),
      crumb="from the API bill → here: the environment’s own bill → to: how slow and expensive are linked",
      callout="""<p><b>Every published “cost per task” is an API bill.</b> No benchmark reports a dollar figure for its sandbox, browser or virtual machine, and no product publishes a per-session environment cost. From hourly list prices (read 2026-09-27) it can be computed: a one-hour task on a CPU environment costs $0.02 (Browser Use cloud browser) to $0.36 (OpenAI hosted container, 4 GB) — 0.3–4.6% of a $7.87 API bill and 0.03–0.5% of a $72.4 one (calc.).</p>""",
      body=f"""
<div class="two">
  <div class="stack">
    {card("FOUR EXCEPTIONS THAT MAKE IT LARGE", "",
          "<b>Plan fees</b> — Browserbase $20 per month for 100 hours, E2B Pro $150 per month: expensive per task when the hours go unused. <b>Traffic</b> — residential proxies $5–12 per GB; 1 GB equals 40 browser-hours on Browser Use. <b>Wall-clock billing while the agent waits</b> — in AgentSysBench’s production trace the median session is active only 20% of its lifetime. <b>GPU sandboxes</b> — Daytona’s H100 at $3.95 per hour is half of a $7.87 bill in one hour; in AgentSysBench’s simulation workload the GPU container is over 99% of per-request cost.",
          "vendor price pages; " + CITE['asb'])}
    {hbars("A one-hour CPU environment as a share of a $7.87 API bill (calc.)", [("Browser Use cloud browser",0.25,"0.25%"),("AWS t3.medium",0.5,"0.5%"),("Browserbase",1.5,"1.5%"),("E2B / Daytona 2 vCPU",2.1,"2.1%"),("Modal 2 vCPU",3.0,"3.0%"),("AWS t3.2xlarge (OSWorld 2.0)",4.2,"4.2%"),("OpenAI hosted container 4 GB",4.6,"4.6%")], "vendor price pages, read 2026-09-27 · against $72.4 the shares are 0.03–0.50%", labelw=190, width=560, height_row=19)}
  </div>
  <div class="stack">
    {card("HOW BENCHMARKS HANDLE IT", "instance types, never dollars",
          "OSWorld, OSWorld-Verified, OSWorld 2.0, TheAgentCompany and WebArena all name their machines (t3.medium / t3.large controllers, t3.2xlarge, t3a.xlarge with a 1,000 GB disk for the hosted sites) and none gives their cost. OSWorld 2.0’s $72.4 moves with output tokens, so it is an API bill; the Holistic Agent Leaderboard defines “Cost” as total API cost. Only AgentSysBench itemises the sandbox — as a share, not a dollar.",
          ci('osw2','hal','asb'))}
    {card("HOW PRODUCTS HANDLE IT", "a dedicated machine per user, price undisclosed",
          "Meta Muse runs on “a dedicated cloud computer with its own browser”; OpenAI’s ChatGPT agent uses “its own virtual computer” (Operator, “its own browser”, was retired on 2025-08-31); Claude in Chrome runs inside the user’s own Chrome. Subscription prices are not environment costs.",
          ci('meta','openai25'))}
  </div>
</div>""",
      foot="SOURCES · AWS, Browser Use, Browserbase, E2B, Daytona, Modal and OpenAI price pages, read 2026-09-27 · the full price table is Appendix A3",
      chip=("#a3-3", "Appendix A3"),
      notes="""文档第三节第六类（追加调查 7，E212–E223，D141–D145）。1 小时 CPU 环境 $0.02–0.36，占 $7.87 的 0.3–4.6%、占 $72.4 的 0.03–0.5%（calc.）。四个例外：月费、代理流量 $5–12/GB、按 wall-clock 计费而中位会话只 20% 在执行 [E219]、GPU 沙箱 H100 $3.95/h。benchmark 只写实例类型不写钱；HAL 的 Cost 定义为 API 总费用；只有 AgentSysBench 给沙箱占比。产品：Meta Muse 专属云端电脑、ChatGPT agent 虚拟电脑、Claude in Chrome 用户自己的 Chrome，都不公布每会话成本。""")

# --- 16 how they link -----------------------------------------------------
slide("s16", "How slow and expensive are linked: three kinds of relationship",
      hl=("n-rtok", "n-wtok", "n-queue", "n-wait"),
      crumb="from the two bills → here: what each cause does to time and to money → to: what fixing each lever buys",
      callout="""<p><b>The two equations share the read and write tokens; environment time and queueing appear only in the time equation.</b> So every cause relates to time and money in exactly one of three ways.</p>""",
      body=f"""
<div class="cards3 rel">
  {card("SAME SOURCE — in both equations", "fix it, and time and money fall together",
        "<b>Steps N</b>: time roughly linear, read tokens quadratic — double the steps, double the time, about 4× the read bill (uncached). <b>Calls per step.</b> <b>Reading</b>: history, screenshots, rich observations. <b>Writing</b>: thinking — the slowest and the dearest token. <b>Cache hits</b>: save both, but fragile — any edit to the history or a switch to fast mode invalidates them. <b>Failures and idle loops</b>: both, and they turn “per attempt” into “per success”.", ci('osh','anth-b'))}
  {card("SLOW BUT NOT EXPENSIVE — time equation only", "fix it, and only time falls",
        "<b>Queueing.</b> <b>Page loads and fixed sleeps.</b> <b>Tool tails</b> (tests, builds). None of these produces a token. The machine time behind them is billed by the hour: CPU sandboxes $0.02–0.36 per hour, usually under 5% of the API bill (page 15). To escape the queue one buys a fast or priority tier — at 2× the price.")}
  {card("MONEY FOR TIME OR FOR ACCURACY — opposite signs", "buying speed buys only the writing segment",
        "<b>Fast mode</b>: up to 2.5× faster writing (vendor-stated), reading and queueing unchanged, 2× the price. <b>Bigger models, more thinking</b>: slower and dearer, and the cost-versus-accuracy curve is convex — each extra point costs more than the last: on one model the marginal tokens per point rise from 101K to 575K; 6×, 9× and 9.6× the tokens for a few points; and more thinking is not always more accurate. <b>Smaller models</b>: faster and cheaper, but if accuracy falls, steps and retries rise — possibly slower and dearer again (inference; no direct evidence).", ci('anth-b','openai','osw2','hal','atts'))}
</div>
{link_fig()}
<div class="oneline"><b>In one line:</b> a cause that lives in tokens — fix it and time and money fall together; a cause that lives in waiting — fix it and only time falls; paying for speed buys only the writing segment.</div>""",
      foot=f"SOURCES · {CITE['osh']} · {CITE['anth-b']} · {CITE['openai']} · {CITE['osw2']} · {CITE['hal']} · {CITE['atts']} — the cause-by-cause table is Appendix A5",
      chip=("#a5-1", "Appendix A5"),
      notes="""文档第四节。三种关系：同源（步数、调用、读、写、缓存、失败）；只慢不贵（排队、页面等待和固定停顿、工具长尾）；用钱换时间或准确率（fast mode 2 倍 [E190][E192]；大模型和思考：凸的，边际 token 10.1 万→57.5 万 [E44]，6× [E41] / 9× [E43] / 9.6× [E44]，多思考未必更准 [E43]；小模型反弹为推断）。一句话收住：出在 token 上的修了时间和钱一起省；出在等待上的只省时间；花钱买速度只买得到写的那段。""")

# --- 17 levers -----------------------------------------------------------
slide("s17", "What fixing each lever buys",
      hl=("n-steps", "n-calls", "n-read", "n-write", "n-wait", "n-price"),
      crumb="from the three relationships → here: the levers, read off the equations → to: what has not been measured",
      callout="""<p><b>Seven levers follow from the equations; each one saves a known term and carries a known risk.</b> This table is the bridge to Part 2, which asks how far the literature has pushed each lever.</p>""",
      body=f"""
<table class="tbl lev">
<colgroup><col style="width:34%"><col style="width:12%"><col style="width:20%"><col style="width:34%"></colgroup>
<thead><tr><th>lever</th><th>time</th><th>money</th><th>the catch</th></tr></thead>
<tbody>
<tr><td><b>Fewer passes</b> — fewer steps, several actions per call, skip navigation-only steps</td><td>yes</td><td>yes, and it is the quadratic term</td><td>one must know which steps need no thinking</td></tr>
<tr><td><b>Read less</b> — trim the history, shrink screenshots, cache the prefix</td><td>yes</td><td>yes</td><td>trim too much and the agent forgets; trimming the history itself invalidates the cache</td></tr>
<tr><td><b>Write less</b> — turn thinking down, use a smaller model</td><td>yes</td><td>yes</td><td>accuracy may fall</td></tr>
<tr><td><b>Fewer calls per step</b> — drop judging and reflection calls</td><td>yes</td><td>yes</td><td>tasks that relied on those calls to catch errors get worse</td></tr>
<tr><td><b>Overlap the waiting</b> — pre-load, run tools in parallel, act on page-ready events instead of fixed sleeps</td><td>yes</td><td>no</td><td>helps only where the environment is the dominant term</td></tr>
<tr><td><b>Buy a fast or priority tier</b></td><td>yes, writing only</td><td>no — costs 2× more</td><td>reading is not faster; switching drops the cache</td></tr>
<tr><td><b>Stop retrying failures</b> — early stop, detect dead loops</td><td>yes</td><td>yes</td><td>kills some attempts that would have succeeded</td></tr>
</tbody></table>""",
      foot="SOURCES · derived from the two equations on page 2 and the evidence on pages 5–16; the relationship table is Appendix A5",
      chip=("#a5-1", "Appendix A5"),
      notes="""文档第四节“修什么能省什么”表：少转圈（时间、钱、平方项）；少读；少写；少调；把等待重叠起来（只省时间）；买 fast/priority（只提写速、贵 2 倍、丢缓存）；不重试失败。这一页是通往第二部分的桥：文献在每根杠杆上做到哪了。""")

# --- 18 gaps ------------------------------------------------------------
slide("s18", "What nobody has measured yet",
      crumb="from the levers → here: the holes in the evidence → to: references",
      callout="""<p><b>These are gaps in the measurements, not claims of a research gap.</b> They decide how far each statement in this part can be pushed.</p>""",
      body=f"""
<table class="tbl gaps">
<colgroup><col style="width:27%"><col style="width:45%"><col style="width:28%"></colgroup>
<thead><tr><th>not measured</th><th>what exists</th><th>what it stops us from saying</th></tr></thead>
<tbody>
<tr><td><b>Read / write time split and cache hit rate for a frontier API model</b></td><td>No measurement reports both. The only read / write split is on locally served 27–31B models {ci('yuan')}; screenshot-agent measurements do not report cache state</td><td>How much of “87–97% in the model” is reading, how much writing, and what remains once the cache is on</td></tr>
<tr><td><b>How much slower than a person</b></td><td>None of 17 benchmarks times agent and human on the same tasks; the closest is AXIS’s user study, where a UI agent was 1.69× slower than manual work on easy tasks — small sample {ci('axis')}</td><td>“X times slower than a person” cannot go on a slide</td></tr>
<tr><td><b>Environment dollars</b></td><td>Benchmarks report instance types, not dollars; AgentSysBench gives shares. Computed from list prices: usually 0.3–5% of the API bill for CPU environments (page 15)</td><td>Every published cost is an API bill; the omission is small for CPU environments, not for GPU sandboxes or long idle sessions</td></tr>
<tr><td><b>Whether OSWorld-Human’s “action” time includes the 2-s sleep</b></td><td>Not stated; if it does, “actions under 2%” implies more than 100 s per step (calc.)</td><td>“Environment under 3.5%” may understate the waiting</td></tr>
<tr><td><b>The rebound from a smaller model</b></td><td>No direct evidence on how many extra steps and retries a drop in accuracy causes</td><td>The last row of the relationship table stays marked “inference”</td></tr>
<tr><td><b>How much slowness costs accuracy</b></td><td>OSWorld 2.0 records the stale-state failure mode but not its share of failures {ci('osw2')}</td><td>“It exists” is all that can be said, not “how large”</td></tr>
</tbody></table>""",
      foot=f"SOURCES · {CITE['yuan']} · {CITE['axis']} · {CITE['osw2']} · the gap list is Appendix A6",
      chip=("#a6-1", "Appendix A6"),
      notes="""文档第五节。六个缺口：前沿 API 模型的读写拆分 + 缓存命中率（唯一拆分是本地 27–31B [E29]；截图型没报缓存 [D101]）；agent 比人慢多少（AXIS 用户研究 1.69 倍，样本小 [E161]）；环境的钱；OSWorld-Human 的“动作”是否含 2 秒停顿 [E111]；小模型反弹；慢对准确率的影响（只有 stale-state 存在，无比例）。""")

# --- references (part 1) ---------------------------------------------------
REFS_P1 = [
 "Abhyankar, R., Qi, Q., &amp; Zhang, Y. (2026). OSWorld-Human: Benchmarking the efficiency of computer-use agents. <i>Proceedings of the 9th Conference on Machine Learning and Systems (MLSys 2026)</i>. arXiv:2506.16042. University of California, San Diego.",
 "Anthropic. (2026a, May 13). <i>Best practices for computer and browser use with Claude</i>. https://claude.com/blog/best-practices-for-computer-and-browser-use-with-claude",
 "Anthropic. (2026b). <i>Claude API pricing</i>; <i>Fast mode</i> (developer documentation, read 27 September 2026). https://platform.claude.com/docs/en/about-claude/pricing; https://platform.claude.com/docs/en/build-with-claude/fast-mode",
 "Artificial Analysis. (2026). <i>Claude Opus 5.5 (high): model page</i> and <i>Methodology</i> (read September 2026). https://artificialanalysis.ai/models/claude-opus-5-5-high; https://artificialanalysis.ai/methodology",
 "Bian, S., Yan, M., Jayarajan, A., Pekhimenko, G., &amp; Venkataraman, S. (2025). What limits agentic systems efficiency? arXiv:2510.16276. University of Wisconsin–Madison; University of Toronto; NVIDIA.",
 "Chang, C., Zhou, Y., Fu, K., An, D., Feng, T., Lu, H., Yao, S., Guo, P., Yu, Y., Shan, Y., Li, B., Yuan, B., &amp; Wang, W. (2026). From LLM inference to agentic workloads: Characterization and implications for serving systems (AgentSysBench). arXiv:2608.15127. Hong Kong University of Science and Technology; Alibaba Group; ByteDance.",
 "Kang, H., Li, Z., Xu, W., Yang, X., Chen, Y., Wang, J., Chen, B., Krishna, T., Xu, C., &amp; Arora, S. (2026). ThunderAgent: A simple, fast and program-aware agentic inference system. <i>Proceedings of the 43rd International Conference on Machine Learning (ICML 2026)</i>, poster. arXiv:2602.13692. Georgia Institute of Technology; University of Illinois Urbana-Champaign; Carnegie Mellon University; Together AI.",
 "Kapoor, S., Stroebl, B., Kirgis, P., Nadgir, N., Siegel, Z. S., Wei, B., … Narayanan, A. (2025). Holistic Agent Leaderboard: The missing infrastructure for AI agent evaluation. arXiv:2510.11977. Princeton University et al.",
 "Le Sellier De Chezelles, T., Gasse, M., Drouin, A., Caccia, M., Boisvert, L., Thakkar, M., … Lacoste, A. (2025). The BrowserGym ecosystem for web agent research. arXiv:2412.05467. ServiceNow Research et al. (figure not re-verified; used only in Appendix A1)",
 "Lee, N., Erdogan, L. E., John, C. J., Krishnapillai, S., Mahoney, M. W., Keutzer, K., &amp; Gholami, A. (2026). Agentic test-time scaling for WebAgents. arXiv:2602.12276. University of California, Berkeley.",
 "Liu, B., Qiu, H., Goiri, Í., Fonseca, R., Bianchini, R., &amp; Choukse, E. (2026). Agentic coding in the wild: Characterizing GitHub Copilot at production scale. arXiv:2608.00101. University of Illinois Urbana-Champaign; Microsoft Azure Research.",
 "Lu, J., Zhang, Z., Yang, F., Zhang, J., Wang, L., Du, C., Lin, Q., Rajmohan, S., Zhang, D., &amp; Zhang, Q. (2025). AXIS: Efficient human-agent-computer interaction with API-first LLM-based agents. <i>Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)</i>, 7711–7743. https://doi.org/10.18653/v1/2025.acl-long.381. Microsoft.",
 "Meta. (2026, September 8). <i>Introducing Muse, your personal AI agent</i> [Newsroom post]. https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/",
 "OpenAI. (2025). <i>Introducing Operator</i> (23 January 2025); <i>Introducing ChatGPT agent</i> (17 July 2025). https://openai.com/index/introducing-operator/; https://openai.com/index/introducing-chatgpt-agent/",
 "OpenAI. (2026). <i>API pricing</i>; <i>API changelog</i> (fast mode, 30 July 2026; Ultrafast, 13 August 2026) (read 27 September 2026). https://developers.openai.com/api/docs/pricing; https://developers.openai.com/api/docs/changelog",
 "Winston, C., Wang, R. Y., Mirhoseini, A., &amp; Kozyrakis, C. (2026). Agent JIT compilation for latency-optimizing web agent planning and scheduling. <i>Proceedings of the 43rd International Conference on Machine Learning (ICML 2026)</i>, PMLR 306. arXiv:2605.21470. Stanford University.",
 "Wong, M., Hsieh, K., Nath, S., &amp; Netravali, R. (2026). Skim: Speculative execution for fast and efficient web agents. arXiv:2605.16565. Princeton University; Microsoft Research.",
 "xlang-ai. (2026). <i>OSWorld</i> [Source code], desktop_env/desktop_env.py and run.py at commit b138d348. https://github.com/xlang-ai/OSWorld",
 "XLANG Lab. (2026). OSWorld 2.0: Benchmarking computer use agents on long-horizon real-world tasks. arXiv:2606.29537. The University of Hong Kong (authored as “XLANG Lab and Collaborators”; the full author list is in the paper’s Appendix A).",
 "Yuan, Y., Nayak, A., Kundu, S., &amp; Talati, N. (2026). Agentic AI workload characteristics. arXiv:2605.26297. University of Illinois Urbana-Champaign; Gimlet Labs; Intel.",
 "Zhang, C., Huang, H., Ni, C., Mu, J., Qin, S., He, S., … Zhang, D. (2025). UFO2: The desktop AgentOS. arXiv:2504.14603. Microsoft.",
 "Zhu, K., Jacob, M., Ma, C., Pan, Y., Wang, S., Krishnamurthy, A., &amp; Kasikci, B. (2026). TraceLab: Characterizing coding agent workloads for LLM serving. arXiv:2606.30560. University of Washington.",
 "Vendor price pages used for Appendix A3 (all read 27 September 2026): AWS, <i>Amazon EC2 T3 instances</i>; Browser Use, <i>Pricing</i> and <i>API v4: create browser session</i>; Browserbase, <i>Pricing</i> and <i>Billing plans</i>; Daytona, <i>Pricing</i> and <i>Billing</i>; E2B, <i>Pricing</i>; Modal, <i>Pricing</i> and <i>Sandbox resources</i>.",
]

def refs_html(items, start=1):
    return f'<ol class="reflist" start="{start}">' + "".join(f"<li>{r}</li>" for r in items) + "</ol>"

half = (len(REFS_P1) + 1) // 2
slide("s19", "References · Part 1 (1 of 2)", kind="refs",
      crumb="author–year tags on the pages refer to these entries · published version where one exists, otherwise the arXiv number and the authors’ institutions",
      body=refs_html(REFS_P1[:half]),
      notes="""参考文献第一页。格式：作者（年份）。题目。会议或期刊（已录用的按发表版本）/ arXiv 编号。机构。厂商定价页注明读取日期。""")
slide("s20", "References · Part 1 (2 of 2)", kind="refs",
      crumb="continued",
      body=refs_html(REFS_P1[half:], start=half+1),
      notes="""参考文献第二页。""")

# =====================================================================
# APPENDIX — Part 1
# =====================================================================
def A(id_, label, title, body, hl=(), crumb="", notes="", chip=("#back", "← back")):
    slide(id_, title, body, label=label, hl=hl, crumb=crumb, notes=notes, chip=chip, kind="appendix")

th_slow = ["id", "cause", "mechanism", "evidence, with the conditions of the measurement", "source", "dominant in"]
w_slow = ["4%", "11%", "15%", "47%", "13%", "10%"]

A("a1-1", "A1 · 1/3", "A1 · Slowness, every cause — I. steps and II. calls per step",
  hl=("n-steps", "n-calls"),
  crumb="the complete table behind pages 4–6 · three kinds of agent: screenshot desktop agent, text web agent, coding agent with a prompt cache",
  body=table(th_slow, [
   ["I-1", "The task is long", "Hour-scale tasks take hundreds of passes", "OSWorld 2.0, 108 long tasks: Claude Opus 4.7 with maximum thinking, one action per step, 500-step cap: 318 tool calls per task on average, i.e. 318 steps; with several actions per call, Claude Opus 4.8 takes 103 steps (481.8 calls) and GPT-5.5 95.2 steps (149.8 calls)", ci('osw2'), "screenshot, text"],
   ["I-2", "One action per pass", "Every click is a whole pass: one observation, one model call, one wait", "OSWorld 2.0: with one action per step Claude Opus 4.7 needs 318 steps; with batched actions the same model needs 160.7 and Claude Opus 4.8 needs 103", ci('osw2'), "screenshot, text"],
   ["I-3", "Navigation-only passes still call the model", "Paging, scrolling and opening the next page need no thinking but cost a call each", "Skim’s profile of three text web agents (Browser-Use, AgentOccam, WebVoyager; GPT-4o) on 151 WebVoyager live-site tasks: 66.7% of the steps in the median task are pure navigation", ci('skim'), "text"],
   ["I-4", "Idling and dead loops", "Element not found, repeated retries; steps rise without progress", "OSWorld-Human’s records of the GTA1 harness (o3 plans and judges, GTA1-7B locates elements) on 39 OSWorld desktop tasks: in failed tasks that exceeded 50 steps, 66% of steps were wasted repeats; one element-locating loop repeated the same step 18 times — 27 minutes and $8.47 at list price without caching", ci('osh'), "screenshot"],
   ["I-5", "Acting on a stale screen", "The screenshot is taken before the page changes; the agent clicks on the old layout and must repair", "OSWorld 2.0 records “stale interface state” as a failure mode; no share reported", ci('osw2'), "screenshot"],
   ["II-1", "Multi-call harness", "One step = plan + judge + reflect, several calls in series", "OSWorld-Human, two harnesses: GTA1 runs 4 parallel planners per step, retries up to 3 rounds, then one judging call picks — 4–12 planning calls per judging call; Agent S2 adds a reflection call per step, so planning is 53% and reflection 34% of task time", ci('osh'), "screenshot"],
   ["II-2", "Sampling for accuracy", "5–20 candidates per step, then pick one", "Same model and harness (gpt-oss-120b, ReAct) on 165 WebArena-Lite tasks: 1 → 10 candidates per step raises success from 38.8% to 43.2% and tokens per task from 96K to 920K — 9.6× the tokens for 4.4 points", ci('atts'), "text"],
   ["II-3", "Coding agents call repeatedly within a turn", "The model is called back and forth inside one user turn", "GitHub Copilot coding agent production telemetry (first week of June 2026, 13.5 million sessions): 6.6 model calls per user turn on average", ci('copilot'), "coding"],
  ], w_slow),
  notes="附录 A1 第 1 页：文档第一节第一类（I-1…I-5，[E6][E17][E45][§1.8]）和第二类（II-1…II-3，[E25][E22][E44][E20]）。")

A("a1-2", "A1 · 2/3", "A1 · Slowness, every cause — III. each call is slow",
  hl=("n-queue", "n-read", "n-write"),
  crumb="the complete table behind pages 7–8",
  body=table(th_slow, [
   ["III-1", "Queueing", "The request waits at the provider; unbilled, but counted as model time", "Client-side measurement of 15 models across 5 providers: requests of the same length differ in latency by up to 69× depending on when they are sent", ci('bian'), "all"],
   ["III-2", "Reading (the prompt is re-processed every call)", "Every call re-reads the whole history; more screenshots, slower", "OSWorld-Human, multi-call harnesses: later steps up to 3× slower because the prompt at step k holds the k−1 earlier screenshots — “dominated by prefill”. One screenshot is 1,000–1,800 tokens. AgentSysBench’s WebArena agent (Kimi-K2.6): observation switched from a single format to accessibility tree + HTML + screenshot → input 4.8×, model share of time 46.9% → 61.6%. Under load the cache is evicted and re-read: SWE-Agent / OpenHands running GLM-4.6 on 8 H100s for SWE-bench Lite, request latency up to 7.14× as concurrency rises", ci('osh','anth-a','asb','thunder'), "screenshot; text with rich observations; coding under load"],
   ["III-3", "Writing (one token at a time)", "Token-by-token generation, strictly serial", "Locally served ReAct agents (Qwen3.6-27B / Gemma4-31B, vLLM, 2 H100s) on five benchmarks: with the cache warm, generation is 91–98.6% of model time. Windows desktop agent UFO2 (GPT-4o / o1 API): about 10 s per model call, the largest item per step in every configuration", ci('yuan','ufo2'), "coding; single-call screenshot"],
   ["III-4", "Thinking modes and larger models", "Thinking writes more tokens; larger models are slower per token", "OSWorld 2.0, same 108 tasks: Claude Opus 4.8 writes 224K output tokens per task, GPT-5.5 37K. Holistic Agent Leaderboard, 9 benchmarks, 21,730 runs: raising reasoning effort lowered accuracy in 21 of 36 pairs", ci('osw2','hal'), "all"],
  ], w_slow),
  notes="附录 A1 第 2 页：文档第一节第三类（III-1…III-4，[E101][E23][E31][E98][E108][E29][E94][E41][E43]）。")

A("a1-3", "A1 · 3/3", "A1 · Slowness, every cause — IV. environment, V. serial",
  hl=("n-observe", "n-act", "n-wait"),
  crumb="the complete table behind page 9",
  body=table(th_slow, [
   ["IV-1", "Producing the observation", "Extracting the accessibility tree or detecting elements takes time", "OSWorld desktop applications: 3–26 s to generate one accessibility tree; the screenshot itself is under 2% of task time. UFO2: OmniParser element detection adds about 1 s per step", ci('osh','ufo2'), "screenshot"],
   ["IV-2", "Browser execution and page load", "After a click the agent waits for the page", "151 WebVoyager live-site tasks: per step, median browser action 6.6 s vs model call 4.7 s. WebArena with GenericAgent + Claude 3.5 Sonnet: 7.6 s of a 12.2 s step in the browser (this figure was not re-verified)", ci('skim','bgym'), "text"],
   ["IV-3", "Fixed sleeps", "The agent cannot tell when the page is ready, so it sleeps a fixed number of seconds", "OSWorld’s environment code sleeps 2 s after every action; OSWorld 2.0 prescribes 3 s, so 318 steps are about 16 minutes of pure waiting (calc.). AgentSysBench: a single-call GUI agent (ReAct, Kimi-K2.6 API) spends over 70% of its OSWorld execution time in the desktop sandbox", ci('code','osw2','asb'), "screenshot (caused by the benchmark harness)"],
   ["IV-4", "Tool tails", "Tests and builds take minutes", "TraceLab, 4,265 Claude Code / Codex sessions from 43 developers (September 2025 – June 2026): tool calls over 1 minute are 4% of calls but 85% of tool time; a request averages 4.3 minutes — tools 2.5 (59.8%), model 1.7 (41.0%)", ci('tracelab'), "coding"],
   ["V", "Serial structure", "The four stages never overlap, so task time is the sum of every term, not the largest one; fixing one term saves only its share", "Concurrency within a turn is 1.15 in Copilot telemetry. Separately, 80–92% of a coding session’s elapsed time is the human thinking between turns — strip it before reading any total", ci('copilot','tracelab'), "all"],
  ], w_slow),
  notes="附录 A1 第 3 页：文档第一节第四类（IV-1…IV-4，[E24][E22][E94][E17][E26][E111][E97][E19][E105]）和第五类（[E20][E105][E106]）。")

A("a2-1", "A2", "A2 · Where the arrows land, with every measurement condition",
  hl=("n-read", "n-wait", "n-write"),
  crumb="the complete table behind page 10",
  body=table(["", "screenshot desktop agent, multi-call harness", "text web agent", "coding agent with a prompt cache"], [
   ["heaviest term", f"Reading × calls per step × steps. OSWorld-Human timed two multi-call harnesses (GTA1, Agent S2) step by step on 39 OSWorld desktop tasks: 87–97% of task time in planning, judging and reflection calls; screenshots and actions together under 3.5% {ci('osh')}", f"Browser execution plus waiting. Skim measured three text web agents (GPT-4o) on 151 WebVoyager live-site tasks: per step, median browser action 6.6 s and model call 4.7 s {ci('skim')}", f"Writing, or tool tails, depending on the tools. With the context cache on, token-by-token generation is 91–98.6% of model time (locally served models) {ci('yuan')}; in Claude Code / Codex records a request spends 59.8% in tools and 41.0% in the model {ci('tracelab')}; in GitHub Copilot, whose tools are light, agent time is 13.7% model and 2% tools {ci('copilot')}"],
   ["second", "Writing: with thinking on, more reasoning tokens per step, and generation is one token at a time", f"Reading, once the observation grows: AgentSysBench switched a WebArena agent from one observation format to accessibility tree + HTML + screenshot — input 4.8×, model share 46.9% → 61.6% {ci('asb')}; the Browser-Use harness spends 73% of its latency in model calls {ci('jit')}", f"Reading, when load evicts the cache and the whole context is re-read: ThunderAgent measured request latency up to 7.14× under cache thrash {ci('thunder')}"],
   ["negligible", f"Producing the observation and executing the action: under 3.5% together {ci('osh')}", "Nothing: model and browser are close; which is larger depends on observation size and model speed", "Navigation-only steps: a coding agent has no pages to turn"],
   ["counter-example", f"A single-call agent is different: AgentSysBench’s one-call GUI agent (Kimi-K2.6) spends over 70% of its OSWorld time in the desktop sandbox {ci('asb')}, because the harness sleeps after every action — 2 s in OSWorld’s code {ci('code')}, 3 s in OSWorld 2.0 {ci('osw2')}", f"Browser-Use: 73% of latency in model calls, not the browser {ci('jit')}", f"Two production records point opposite ways: heavy tools in Claude Code / Codex (tools 59.8% > model 41.0%) {ci('tracelab')}; light tools in Copilot (model 13.7% > tools 2%) {ci('copilot')}. The difference is the kind of tool (tests and builds vs file reads), not a contradiction"],
   ["in one line", "Slow in reading: every step re-reads the screenshot history, more as the task goes on", "Slow in the environment (browser and page waits); once the observation grows, slow in reading again", "Reading is cached away; slow in writing and in the tools"],
  ], ["9%", "31%", "30%", "30%"], cls="tbl three"),
  notes="附录 A2：文档第二节整表，含每个数字的测量条件 [E22][E17][E29][E105][E106][E98][E100][E108][E97][E111][E6]。")

th_cost = ["id", "cause", "mechanism", "evidence, with the conditions of the measurement", "source"]
w_cost = ["5%", "13%", "20%", "47%", "15%"]
A("a3-1", "A3 · 1/3", "A3 · Cost, every cause — 1. tokens read and 2. tokens written",
  hl=("n-rtok", "n-wtok"),
  crumb="the complete table behind pages 11–12 · prices are list prices from the vendors’ own pages, September 2026",
  body=table(th_cost, [
   ["1-1", "History re-sent", "Call k reads everything from the k−1 earlier steps; total reading ≈ steps squared", "“Cost grows quadratically with the number of steps” — OSWorld-Human, real runs", ci('osh')],
   ["1-2", "Large screenshots", "1,000–1,800 tokens per image; 100 images fill a 200K context", "Anthropic’s engineering guidance for computer and browser use", ci('anth-a')],
   ["1-3", "Rich observation formats", "Accessibility tree + HTML + screenshot together: 4.8× the input", "AgentSysBench, WebArena agent, Kimi-K2.6", ci('asb')],
   ["1-4", "Sampling", "Several candidates per step, mostly read tokens", "gpt-oss-120b + ReAct on 165 WebArena-Lite tasks: 1 → 10 candidates per step, 96K → 920K tokens per task", ci('atts')],
   ["1-5", "The cache is not a cure", "However high the hit rate, a long history keeps reading dominant; a miss re-reads everything", "TraceLab, 4,265 Claude Code / Codex sessions: prefix-cache hit rate 95.7%, prefix tokens still 59.5% of list-price cost; on a miss the re-read is 3.8× the genuinely new content", ci('tracelab')],
   ["2-1", "Thinking modes", "Thinking tokens are billed as output; when they cannot be switched off they are a fixed overhead", "OSWorld 2.0, same tasks: Claude Opus 4.8 224K output tokens per task, GPT-5.5 37K; Claude Opus 5.5: “thinking cannot be disabled and is billed as output”", ci('osw2','anth-b')],
   ["2-2", "But writing is not always the larger bill", "In an uncached screenshot agent, output was 31% of the total", "OSWorld-Human, GTA1: the paper’s $2.43 counts output only; Table 3’s input and output give $7.87", ci('osh')],
  ], w_cost),
  notes="附录 A3 第 1 页：文档第三节第一类（Ⅰ-1…Ⅰ-5，[E45][E31][E98][E44][E19]）和第二类（Ⅱ-1、Ⅱ-2，[E41]、Anthropic 2026b、[D7]）。")

A("a3-2", "A3 · 2/3", "A3 · Cost, every cause — 3. calls, 4. failures, 5. unit price",
  hl=("n-calls", "n-succ", "n-price"),
  crumb="the complete table behind page 13",
  body=table(th_cost, [
   ["3", "Number of calls", "Steps × calls per step scales both token bills", "GTA1: 4 parallel planners per step, up to 3 retry rounds, one judging call → 4–12 planning calls per judging call, i.e. 5–13× the calls of a single-call harness (calc.). Agentic test-time scaling: 5–20 candidates per step multiply the calls by the candidate count. The same extra calls cost time and money at once", ci('osh','atts')],
   ["4-1", "Failed attempts are billed", "Cost per success = cost per attempt ÷ success rate", "OSWorld 2.0: the best agent (Claude Opus 4.8) costs about $72.4 per attempt at 20.6% completion → about $351 per success (calc.). An accounting conversion, not the real price of retrying one task until it succeeds", ci('osw2')],
   ["4-2", "Idle steps are billed in full", "Every pass of a dead loop is a full read and write", "OSWorld-Human, GTA1 on 39 OSWorld tasks: one element-locating loop repeated the same step 18 times — 27 minutes, $8.47 at list price without caching; in failed tasks over 50 steps, 66% of steps were such repeats", ci('osh')],
   ["4-3", "Evaluation itself is too expensive to repeat", "Single runs, no repeats", "Holistic Agent Leaderboard: 9 benchmarks, 21,730 runs, one run per configuration, about $40,000 in total; Claude Opus 4.1 not run on Online-Mind2Web because the estimate was $20,000", ci('hal')],
   ["5-1", "Model tier", "Claude Opus 5.5 $4 / $20 vs GPT-6 Luna $0.10 / $0.50 per million tokens read / written", "Vendor price pages, 27 September 2026", ci('anth-b','openai')],
   ["5-2", "Fast mode", "2× on both vendors; switching speed tiers invalidates the cache", "Anthropic: Claude Opus 5.5 $8 / $40, up to 2.5× output speed (vendor-stated), first-token wait unchanged. OpenAI: 2× on all listed models; “up to 2.5×” stated only for GPT-5.6 Sol", ci('anth-b','openai')],
   ["5-3", "Cache write and read", "Writing to the cache 1.25×; reading from it 0.1×", "Vendor price pages", ci('anth-b','openai')],
   ["5-4", "Long-context surcharge", "OpenAI: 2× the read price above 272K tokens", "Vendor price page", ci('openai')],
  ], w_cost),
  notes="附录 A3 第 2 页：文档第三节第三类（[E25][E44]）、第四类（Ⅳ-1…Ⅳ-3，[E41][E45][E43]）、第五类（Ⅴ-1…Ⅴ-4，[E190][E192]）。")

A("a3-3", "A3 · 3/3", "A3 · Cost — 6. the machines, and the four conventions",
  hl=("n-wait", "n-price", "n-succ"),
  crumb="the complete tables behind pages 14–15 · vendor price pages read 2026-09-27 · per-task amounts and shares are our own arithmetic (calc.)",
  body=table(["environment", "price (vendor page)", "1-hour task", "15-min task", "share of a $7.87 API bill", "share of $72.4"], [
   ["Browser Use cloud browser", "$0.02 per browser-hour, billed by the minute, 1-minute minimum; traffic extra (residential proxy $5/GB, direct $0.20/GB); sessions capped at 240 minutes", "$0.020", "$0.005", "0.25%", "0.03%"],
   ["AWS t3.medium (2 vCPU / 4 GiB, Linux, us-east-1)", "$0.0418 per hour on the T3 product page; another AWS page says $0.0416 (0.5% apart)", "$0.042", "$0.010", "0.5%", "0.06%"],
   ["Browserbase cloud browser", "$20 per month for 100 hours, then $0.12 per hour; $99 per month for 500 hours, then $0.10; billed by the minute", "$0.12", "$0.03", "1.5%", "0.17%"],
   ["E2B / Daytona sandbox (2 vCPU / 4 GiB)", "E2B $0.000014 per vCPU-second + $0.0000045 per GiB-second; Daytona $0.0504 per vCPU-hour + $0.0162 per GiB-hour — both $0.1656 per hour", "$0.166", "$0.041", "2.1%", "0.23%"],
   ["Modal sandbox (1 physical core = 2 vCPU, 4 GiB)", "$0.00003942 per core-second + $0.00000667 per GiB-second → $0.238 per hour; billed on the larger of requested and used", "$0.238", "$0.060", "3.0%", "0.33%"],
   ["AWS t3.2xlarge (8 vCPU / 32 GiB, OSWorld 2.0’s default instance)", "$0.3341 per hour", "$0.334", "$0.084", "4.2%", "0.46%"],
   ["OpenAI hosted container (Hosted Shell / Code Interpreter, 4 GB)", "$0.12 per 20-minute session → $0.36 per hour; 1 GB $0.03, 16 GB $0.48, 64 GB $1.92 per 20 minutes", "$0.36", "$0.12", "4.6%", "0.50%"],
  ], ["22%", "42%", "8%", "8%", "10%", "10%"]) + """
<div class="apx-note"><b>The four accounting conventions (page 14), in one line each:</b> output only vs all tokens — 3.2× (OSWorld-Human, $2.43 vs $7.87); per attempt vs per success — 4.9× (OSWorld 2.0, $72.4 ÷ 20.6%); uncached vs cached — 10× on the read price, far less on the bill (TraceLab: 95.7% hits, prefix still 59.5% of cost); standard vs fast mode — 2× (both vendors), buying only writing speed.</div>""",
  notes="附录 A3 第 3 页：文档第三节第六类的环境价格表（追加调查 7，E212–E218 计算）和四种口径的一句话版。")

A("a5-1", "A5", "A5 · Each cause’s effect on time and on money",
  hl=("n-rtok", "n-wtok", "n-queue", "n-wait"),
  crumb="the complete table behind pages 16–17",
  body=table(["cause", "effect on time", "effect on money", "relationship"], [
   ["Many steps (N)", "Roughly linear: one more step is one more call and one more wait (later steps somewhat slower, up to 3×)", "Write tokens linear in N; read tokens quadratic, because every step re-reads the whole history", "<b>same source</b> — double the steps: about 2× the time, about 4× the read bill (uncached)"],
   ["Many calls per step (c)", "linear", "linear", "<b>same source</b>"],
   ["Reading a lot (history, screenshots, rich observations)", "Reading time, longer every step", "Read-token bill", "<b>same source</b> — the same tokens cost time and money"],
   ["Writing a lot (thinking)", "Generation time, roughly 12 ms per token", "Write-token bill at 5× the read price", "<b>same source</b>, and the dearest time: writing is the slowest and the most expensive token"],
   ["Cache hits", "Saves reading time", "Read price 0.1×", "<b>same source</b>, but fragile: editing the history or switching to fast mode invalidates it"],
   ["Queueing", "slow", "free", "<b>slow but not expensive</b>; escaping it means a fast or priority tier at 2×"],
   ["Environment waits (page loads, fixed sleeps)", "slow", "No API cost; machine time by the hour — CPU sandboxes $0.02–0.36 per hour, usually under 5% of the API bill", "<b>slow but not expensive</b>"],
   ["Tool tails (tests, builds)", "slow", "No API cost", "<b>slow but not expensive</b>"],
   ["Failures, idling, retries", "slow", "expensive", "<b>same source</b>, and it turns “per attempt” into “per success”"],
   ["Fast mode", "Writing up to 2.5× faster (vendor-stated); reading unchanged", "2× the price", "<b>money for time</b>"],
   ["Bigger models, more thinking", "slower", "dearer", "<b>money and time for accuracy</b>, convex: marginal tokens per point 101K → 575K on one model; 6× / 9× / 9.6× tokens for a few points; more thinking not always more accurate"],
   ["Smaller models", "faster", "cheaper", "but if accuracy falls, steps and retries rise — possibly slower and dearer again (inference, no direct evidence)"],
  ], ["22%", "26%", "26%", "26%"]),
  notes="附录 A5：文档第四节关系表整表 [E23][E45][E190][E44][E41][E43]。")

A("a6-1", "A6", "A6 · The gaps in the evidence, and what each one blocks",
  crumb="the complete table behind page 18",
  body=table(["gap", "what exists today", "consequence for what can be claimed"], [
   ["Read / write time split and cache hit rate for a frontier API model", f"No measurement reports both; the only read / write split is on locally served 27–31B models {ci('yuan')}; screenshot-agent measurements do not report cache state", "How much of “87–97% in the model” is reading, how much writing, and what remains once the cache is on — unknown"],
   ["How much slower an agent is than a person", f"None of 17 benchmarks measures agent and human elapsed time on the same tasks; the closest is AXIS’s user study, in which a UI agent was 1.69× slower than manual work on easy tasks (small sample) {ci('axis')}", "“X times slower than a person” cannot go on a slide"],
   ["Environment dollars", "Benchmarks report instance types; AgentSysBench reports shares; products publish nothing. Computable from instance type × duration × list price: CPU environments usually 0.3–5% of the API bill", "Every benchmark cost is an API bill; the omission is small for CPU environments, not for GPU sandboxes or long idle sessions"],
   ["Whether OSWorld-Human’s “action” includes the 2-s sleep after each step", f"Not stated {ci('code')}; if it does, “actions under 2%” implies more than 100 s per step (calc.)", "“Environment under 3.5%” may understate the waiting"],
   ["The rebound from a smaller model", "No direct evidence on how many extra steps and retries a drop in accuracy causes", "The last row of the relationship table stays marked “inference”"],
   ["How much slowness hurts accuracy", f"Only OSWorld 2.0 records the stale-state failure mode, without its share of failures {ci('osw2')}", "“It exists” can be said; “how large” cannot"],
  ], ["27%", "45%", "28%"]),
  notes="附录 A6：文档第五节缺口表 [E29][D101][E161][E111]。")

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
.thumb{position:absolute;right:40px;top:10px;width:305px;height:95px;border:1px solid var(--rule);border-radius:4px;background:#fff;padding:5px 6px;display:flex;align-items:center}
.thumb svg{width:100%;height:100%}
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
.rows5{grid-template-columns:repeat(5,1fr)}.rows5.big .cd{font-size:13px}.rows5.big .cv{font-size:16px}.rows5.big .card{padding:14px 14px}.rows6{grid-template-columns:repeat(3,1fr)}
.figs3{grid-template-columns:repeat(3,1fr);gap:20px;flex:none}
.card{border:1px solid var(--rule);border-radius:4px;padding:11px 13px;background:#fff;display:flex;flex-direction:column;gap:5px;min-height:0}
.ck{font-family:'IBM Plex Mono',Menlo,monospace;font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
.cv{font-size:15.5px;font-weight:700;line-height:1.25;letter-spacing:-.005em}
.cd{font-size:12.5px;line-height:1.4;color:var(--ink2)}
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
.ft{font-size:11.5px;font-weight:600;line-height:1.3}
.fc{font-family:'IBM Plex Mono',Menlo,monospace;font-size:9.5px;color:var(--mute);line-height:1.35}
.hb{width:100%;height:auto;display:block}
.hb .hl-lab{fill:var(--ink2);font-family:'IBM Plex Mono',Menlo,monospace;font-size:10.5px}
.hb .hl-val{fill:var(--ink);font-family:'IBM Plex Mono',Menlo,monospace;font-size:10.5px;font-weight:500}
.hb .hl-bar{fill:var(--accent)}
/* equation strip (page 4) */
.eqstrip{display:flex;align-items:stretch;gap:10px;border:1px solid var(--rule);border-radius:4px;padding:10px 14px;flex:none}
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
/* notes */
#notes{display:none;position:fixed;left:0;right:0;bottom:0;max-height:34vh;overflow:auto;background:#fff8e6;color:#222;font-size:14px;line-height:1.5;padding:12px 24px;border-top:2px solid #d8b24a;font-family:'IBM Plex Sans',-apple-system,'PingFang SC','Noto Sans CJK SC','Microsoft YaHei',sans-serif;z-index:5}
#notes.on{display:block}
#help{position:fixed;right:12px;top:8px;font-family:'IBM Plex Mono',Menlo,monospace;font-size:11px;color:#c8d0d6;background:rgba(32,38,44,.85);padding:4px 10px;border-radius:10px;z-index:4;transition:opacity .6s}
#help.gone{opacity:0;pointer-events:none}
@media print{
  html,body{background:#fff;height:auto}
  #stage{position:static;transform:none!important;box-shadow:none;width:1280px;height:auto;left:0;top:0}
  .slide{display:flex;position:relative;page-break-after:always;break-after:page}
  #notes,#help{display:none!important}
  @page{size:1280px 720px;margin:0}
}
"""

JS = r"""
(function(){
  const slides=[...document.querySelectorAll('.slide')];
  const stage=document.getElementById('stage');
  const notes=document.getElementById('notes');
  let cur=0, lastMain=0;
  function fit(){const s=Math.min(innerWidth/1280, innerHeight/720);stage.style.transform=`translate(-50%,-50%) scale(${s})`;stage.style.transformOrigin='center';stage.style.left='50%';stage.style.top='50%';}
  function show(i,push){i=Math.max(0,Math.min(slides.length-1,i));slides.forEach((s,k)=>s.classList.toggle('on',k===i));cur=i;if(!slides[i].classList.contains('appendix'))lastMain=i;const n=slides[i].querySelector('.notes');notes.innerHTML=n?n.innerHTML:'';if(push!==false){history.replaceState(null,'','#'+slides[i].id);}}
  function fromHash(){const h=location.hash.replace('#','');const i=slides.findIndex(s=>s.id===h);show(i<0?0:i,false);}
  addEventListener('resize',fit);
  addEventListener('hashchange',fromHash);
  addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' '){e.preventDefault();show(cur+1);}else if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();show(cur-1);}else if(e.key==='Home'){show(0);}else if(e.key==='End'){show(slides.length-1);}else if(e.key==='n'||e.key==='N'){notes.classList.toggle('on');}else if(e.key==='b'||e.key==='B'){show(lastMain);}});
  document.addEventListener('click',e=>{const a=e.target.closest('a');if(a){if(a.getAttribute('href')==='#back'){e.preventDefault();show(lastMain);}return;}if(e.target.closest('#notes'))return;show(cur+1);});
  fit();fromHash();setTimeout(()=>document.getElementById('help').classList.add('gone'),6000);
})();
"""

def render(font_dir=None):
    parts = ['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
             '<title>Agent acceleration — Part 1: where the time and the money go</title>',
             '<style>', font_css(font_dir), CSS, '</style></head><body>',
             '<div id="stage">']
    main_n = 0
    for s in SLIDES:
        cls = "slide " + s["kind"]
        if s["kind"] in ("main", "refs"):
            main_n += 1
            label = f"AGENT ACCELERATION · PART 1 · {main_n:02d}"
        else:
            label = "AGENT ACCELERATION · PART 1 · " + s["label"]
        parts.append(f'<section class="{cls}" id="{s["id"]}">')
        if s["cover"]:
            parts.append(f'<div class="label">{label}</div>')
            parts.append(s["body"])
        else:
            parts.append(f'<div class="head"><div class="label">{label}</div><h1>{s["title"]}</h1></div>')
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
    parts.append('</div><div id="notes"></div><div id="help">← → move · N notes · B back · #sNN links a page</div>')
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
