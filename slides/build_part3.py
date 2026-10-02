#!/usr/bin/env python3
"""Build slides/part3.html — the standalone deck on learning to do repeated web tasks faster and more cheaply.

Sections I (the problem) and II (how far existing work has got), pages 1–9 of
notes/part3/2026-10-01-part3-standalone-slides-outline-v3-zh.md; section III (our plan) waits for discussion.
Page anatomy, CSS, helpers and navigation are build_deck.py's (imported, not changed). Numbers come from
notes/part3/2026-10-01-two-directions-literature-zh.md (§5, §6 table; row data in slides/part3-data/rows.json),
the calibration and problem-framing notes, and the checked WALT set-up figure. The deck stands alone: sources are
the literature, or 'our definition'; earlier Parts and their pages are never cited.

Usage: python3 slides/build_part3.py [--fonts DIR]
"""
import html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_deck as bd                     # builds Parts 1–2 in memory; nothing is written
from build_deck import tex, card, table, esc

OUT = os.path.join(HERE, "part3.html")
ROWS = json.load(open(os.path.join(HERE, "part3-data", "rows.json"), encoding="utf-8"))
TR = {r["i"]: r for r in json.load(open(os.path.join(HERE, "part3-data", "translated.json"), encoding="utf-8"))}
LIT = os.path.join(ROOT, "notes", "part3", "2026-10-01-two-directions-literature-zh.md")
V1 = os.path.join(ROOT, "notes", "part3", "2026-10-01-part3-standalone-slides-outline-zh.md")

# ---------------------------------------------------------------- references (from the literature document, in English)
def _refs_from(path):
    t = open(path, encoding="utf-8").read()
    t = t[t.index("## References"):]
    return {a: (n, r) for a, n, r in re.findall(r'<a id="(ref-[^"]+)"></a>\s*\n\s*- \*\*(.+?)\*\* — (.+)', t)}

REFDB = {**_refs_from(V1), **_refs_from(LIT)}
REFDB["ref-p1-cop"] = ("Erol et al., 2026", bd.refs_for("cop")[0])   # Part 1's source for cost per success
P1KEYS = ["isp", "swm", "distserve", "aa", "anth-b", "aospec", "asyncfc", "llmc", "react", "yuan", "tokenpilot", "sglang"]
for _k in P1KEYS:   # the sources of the agent-loop symbols, in Part 1's checked reference list
    REFDB["ref-p1-" + _k] = (re.sub(r", arXiv · .*$", "", html.unescape(re.sub(r"<[^>]+>", "", bd.CITE[_k]))), bd.refs_for(_k)[0])
EN = [("arXiv 预印本", "arXiv preprint"), ("预印本", "arXiv"), ("实际读的版本：", "Version read: "), ("版本日期：", ""),
      ("初版日期：", "first version "), ("主会", "main conference"), ("日程已列", "listed in the programme"),
      ("论文集待刊", "proceedings forthcoming"), ("正式题名", "formal title"), ("未记录", "not recorded"),
      ("非归档", "non-archival"), ("资格记录标", "eligibility record: "), ("声称未正式", "not yet formal per authors"),
      ("（", " ("), ("）", ")"), ("，", ", "), ("；", "; "), ("：", ": "), ("、", ", "), ("。", ".")]

def en(s):
    s = re.sub(r"\s*来源等级：[^。]*。?", "", s)
    s = s.replace("[正式引用链接]", "[formal citation]")
    s = re.sub(r"\[版本链接（([^）]+)）\]", r"[\1]", s)
    for a, b in EN:
        s = s.replace(a, b)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', s)
    s = s.replace("**", "").replace("*", "")
    s = re.sub(r"\s*\([^()]*[一-鿿][^()]*\)", "", s)                    # Chinese provenance notes stay in the document
    s = " ".join(p for p in re.split(r"(?<=[.;])\s+", s) if not re.search(r"[一-鿿]", re.sub(r"<[^>]+>", "", p)))
    return re.sub(r"\s{2,}", " ", s).strip()

def short(name):
    m = re.match(r"(.+?)( et al\.)?, (\d{4}[a-z]?)$", re.sub(r"（.*?）$", "", name.strip()))
    first, etal, year = m.group(1), m.group(2) or "", m.group(3)
    sur = first.split(",")[0].strip() if "," in first else first.split()[-1]
    return f"{sur}{etal}, {year}", first

def _au(a):
    out = []
    for x in [y.strip() for y in a.split(";") if y.strip()]:
        if x.startswith("et al"):
            out.append("et al.")
            continue
        sur, given = ([y.strip() for y in x.split(",", 1)] if "," in x else (x.split()[-1], " ".join(x.split()[:-1])))
        ini = " ".join(g[0] + "." for g in given.replace("-", " ").split() if g[0].isalpha())
        out.append(f"{sur}, {ini}" if ini else sur)
    if out and out[-1] == "et al.":
        return ", ".join(out[:-1]) + ", et al."
    return out[0] if len(out) == 1 else ", ".join(out[:-1]) + ", &amp; " + out[-1]

def fmt_ref(anchor, full=False):
    """A reference in author–year form: Surname, I., … (Year). Title. Venue. The full form adds the formal link and the version read."""
    name, raw = REFDB[anchor]
    m = re.match(r"(.+?)\s(\d{4}[a-z]?)\.\s(.+)$", raw)
    if anchor.startswith("ref-p1-") or not m:
        if not anchor.startswith("ref-p1-"):
            return en(raw)
        if full:
            return raw
        short_raw = re.sub(r"\s*(?:Dashboard: )?https?://\S+", "", raw)
        short_raw = re.sub(r"\s*\(read [^)]*\)", "", short_raw)
        return re.sub(r"[;,]\s*\.", ".", re.sub(r"\s{2,}", " ", short_raw)).strip()
    authors, year, rest = m.groups()
    title, _, after = rest.partition(". ")
    venue = re.split(r"\s*(?:\[正式引用链接\]|正式引用链接|实际读的版本|; OpenReview|; DOI)", after)[0].strip().rstrip(".")
    venue = re.split(r"[;,]\s*(?:decision|Poster|Oral|Spotlight|OpenReview|proceedings|Session)", venue)[0].strip().rstrip(".")
    v_en = en(venue)
    if not full:   # page foot: the venue in short; the reference pages keep the full entry
        v_en = re.split(r";|, (?:main|Main|Conference|conference|paper|workshop paper|Poster|poster|Findings track|Session|research paper)", v_en)[0].strip()
    out = f"{_au(authors)} ({year}). {en(title)}. <i>{v_en}</i>."
    if full:
        f = re.search(r"\[正式引用链接\]\((https?://[^)]+)\)", raw)
        r = re.search(r"实际读的版本：\[版本链接（([^）]+)）\]\((https?://[^)]+)\)（([^，）]+)(?:，版本日期：([0-9-]+))?", raw)
        out += f' Formal: <a href="{f.group(1)}">link</a>.' if f else " Formal link: not recorded."
        if r:
            out += f' Version read: <a href="{r.group(2)}">{r.group(1)}</a>, {en(r.group(3).replace("版本号未记录", "version not recorded"))}' + (f", {r.group(4)}" if r.group(4) else "") + "."
    return out

USED = []          # anchors in order of first citation
PAGE = []          # anchors cited on the page being built; slide() lists them at its foot
def cite(*keys):
    """keys: row indices of the §6 table, or 'ref-…' anchors. Returns '(Surname et al., 2026; …)'."""
    out = []
    for k in keys:
        a = k if isinstance(k, str) else re.findall(r"#(ref-[^)]+)\)", ROWS[k]["cite"])[0]
        if a not in USED:
            USED.append(a)
        if a not in PAGE:
            PAGE.append(a)
        out.append(FORM[a])
    return "(" + "; ".join(out) + ")"

FORM = {}
_seen = {}
for a, (n, _) in REFDB.items():
    if a.startswith("ref-p1-") and a != "ref-p1-cop":
        FORM[a] = n
        continue
    f, first = short(n)
    FORM[a] = f
    _seen.setdefault(f, []).append(a)
for f, anchors in _seen.items():          # two works with one short form: add the first author's initials
    if len(anchors) > 1:
        for a in anchors:
            _, first = short(REFDB[a][0])
            ini = "".join(p[0] + ". " for p in first.replace(",", "").split()[:-1])
            FORM[a] = ini + f

# ---------------------------------------------------------------- page store and render (build_deck's anatomy)
S = []
def slide(id_, title, body="", *, crumb="", callout="", foot="", chip=None, kind="main", cover=False, label=None, page_refs=True):
    refs = PAGE[:]
    PAGE.clear()
    if kind == "main" and refs and page_refs:
        rh = bd.page_refs_html(sorted((fmt_ref(a) for a in refs), key=lambda r: re.sub("<[^>]+>", "", r).lower()), small=True)
        body += rh.replace('class="pgrefs sm"', 'class="pgrefs sm c3"') if len(refs) > 8 else rh
    S.append(dict(id=id_, title=title, body=body, crumb=crumb, callout=callout, foot=foot, chip=chip, kind=kind,
                  cover=cover, label=label))

TAG = "AGENT ACCELERATION · STABLE ENVIRONMENT"
EXTRA_CSS = r"""
.flow{display:flex;align-items:stretch;gap:5px}
.stp{flex:1;border:1px solid var(--rule);border-radius:4px;padding:7px 9px;font-size:12.5px;line-height:1.32;background:#fff}
.stp .n{display:block;font-family:'IBM Plex Mono',Menlo,monospace;font-size:10px;color:var(--mute);margin-bottom:2px}
.stp.rw{background:#fbeede;border-color:#e2b98b;color:var(--warn)}
.stp.key{border-color:var(--accent)}
.flow.tight .stp{padding:5px 8px;font-size:12px;line-height:1.28}
.defs4.tight div{font-size:12px;line-height:1.35;padding-top:4px}
.arr{align-self:center;color:var(--mute);font-size:13px;flex:none}
.tagc{display:block;font-family:'IBM Plex Mono',Menlo,monospace;font-size:10px;color:var(--warn);margin-top:4px}
.lbl{font-family:'IBM Plex Mono',Menlo,monospace;font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin:2px 0 6px}
.illus{font-family:'IBM Plex Mono',Menlo,monospace;font-size:10px;color:var(--mute);margin-top:6px}
.defs4{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.defs4 div{border-top:2px solid var(--accent);padding-top:6px;font-size:12.5px;line-height:1.4;color:var(--ink2)}
.defs4 b{display:block;color:var(--ink);font-size:13.5px;margin-bottom:2px}
.symlist{font-size:12px;line-height:1.42;color:var(--ink2);margin:0;padding-left:16px;columns:1}
.eqbig{padding:4px 0 6px}
.q2{border-collapse:collapse;width:100%}
.q2 th{font-family:'IBM Plex Mono',Menlo,monospace;font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute);font-weight:500;text-align:left;padding:4px 8px;border-bottom:1px solid var(--accent)}
.q2 td{padding:10px 8px;border-bottom:1px solid var(--rule);font-size:13px;color:var(--ink2);vertical-align:middle}
.q2 td.n{font-size:30px;font-weight:700;color:var(--ink);width:24%}
.q2 td.n.hl{color:#fff;background:var(--accent)}
.guide{font-family:'IBM Plex Mono',Menlo,monospace;font-size:11.5px;line-height:1.5;background:#f6f8fa;border:1px solid var(--rule);border-radius:4px;padding:8px 10px}
.guide b{color:var(--accent)}
.panel3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px}
.panel3>div{border:1px solid var(--rule);border-radius:4px;padding:9px 11px;font-size:12.5px;line-height:1.4;color:var(--ink2)}
.path{display:flex;gap:6px;align-items:center;font-size:12px;color:var(--ink2);margin-top:5px;flex-wrap:wrap}
.path span.s{border:1px solid var(--rule);border-radius:3px;padding:2px 7px;background:#fff}
.path span.s.rw{background:#fbeede;border-color:#e2b98b;color:var(--warn)}
.path .pl{font-family:'IBM Plex Mono',Menlo,monospace;font-size:10.5px;color:var(--mute);width:150px}
.mk{white-space:nowrap;letter-spacing:3px;font-size:12px;color:var(--accent)}
.tbl.p3t td{font-size:11.2px;line-height:1.28;padding:4px 7px 4px 5px}
.tbl.p3t td.c{text-align:center;font-family:'IBM Plex Mono',Menlo,monospace;font-size:12px;color:var(--ink)}
.tbl.p3t tr.tot td{font-weight:700;border-top:1px solid var(--accent)}
.tbl.p3t ul.tb{margin:0;padding-left:13px}.tbl.p3t ul.tb li{margin:0 0 1px}
.tbl.p3d td{font-size:11.2px;line-height:1.28;padding:3px 8px 3px 5px}
.tbl.p3d td:first-child{font-family:'IBM Plex Sans',sans-serif;font-size:12px;color:var(--ink)}
.tbl.p3d tr.grp td{font-family:'IBM Plex Mono',Menlo,monospace;font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);background:#f3f7fa;text-align:center;padding:3px}
.card .cc{font-family:'IBM Plex Sans',sans-serif;font-size:10.5px}
.pgrefs.c3{columns:3;column-gap:20px}
.tightcards .card{padding:8px 11px;gap:3px}.tightcards .cc{font-size:10px;line-height:1.3}.tightcards .cv{font-size:14px}.tightcards .cd{font-size:12px;line-height:1.34}.tightcards .lbl{margin:0 0 4px}
.mgrid{display:grid;grid-template-columns:1fr 1fr;gap:10px 14px}
.mcard{border:1px solid var(--rule);border-radius:4px;padding:8px 11px;background:#fff;display:flex;flex-direction:column;gap:4px}
.mtitle{font-weight:700;font-size:14px;color:var(--ink)}
.mflow{display:flex;flex-wrap:wrap;align-items:center;gap:3px}
.mst{border:1px solid #c9d5df;border-radius:3px;padding:2px 6px;font-size:11.5px;color:var(--ink2);background:#f6f8fa}
.mst.key{border-color:var(--accent);background:#eef4f8;color:var(--ink);font-weight:600}
.marr{color:var(--mute);font-size:12px}.marr.loop{color:var(--accent);font-size:14px}
.mex{font-size:11.5px;color:var(--ink2)}.mex b{color:var(--accent);font-weight:600}
.mtw{font-size:11.5px;color:var(--ink2)}
.mtags span{display:inline-block;font-family:'IBM Plex Mono',Menlo,monospace;font-size:9.5px;color:var(--accent);border:1px solid #c9d5df;border-radius:9px;padding:0 6px;margin:0 4px 0 0}
.mworks{font-family:'IBM Plex Mono',Menlo,monospace;font-size:9.5px;color:var(--mute)}
.tbl.ptab td{font-size:10.5px;line-height:1.28;padding:2px 6px 2px 4px}
.tbl.ptab td:first-child{font-family:'IBM Plex Sans',sans-serif;font-weight:700;font-size:11px;color:var(--ink)}
.tbl.ds td{font-size:11.5px;line-height:1.3;padding:5px 6px;vertical-align:top}
.tbl.ds td:first-child{font-family:'IBM Plex Sans',sans-serif;font-weight:700;font-size:12px;color:var(--ink)}
.opt{display:inline-block;border:1px solid var(--rule);border-radius:4px;padding:2px 7px;margin:2px 5px 2px 0;background:#fff;color:var(--ink2)}
.opt b{color:var(--accent);font-weight:600;margin-right:4px}
.tbl.p3t a{color:var(--accent);text-decoration:none;font-family:'IBM Plex Mono',Menlo,monospace;font-size:10px}
.tbl.p3a{font-size:10px;line-height:1.3}.tbl.p3a td{padding:3px 6px 3px 4px}
.tbl.p3a td:first-child{font-family:'IBM Plex Sans',sans-serif;font-size:10px;color:var(--ink)}
.refs3{columns:2;column-gap:26px;font-size:9.6px;line-height:1.32;color:var(--ink2);padding-left:0;list-style:none;margin:0}
.refs3 li{break-inside:avoid;margin:0 0 4px}
.refs3 a{color:var(--accent);text-decoration:none}
.cover-q{margin:22px 0 0;padding-left:22px;font-size:16px;line-height:1.5;color:var(--ink2);max-width:980px}
.cover-q li{margin-bottom:6px}
svg .node.xh rect{fill:#fbeede;stroke:#e2b98b}
svg .node.nd rect{fill:#f3f7fa;stroke:var(--accent);stroke-dasharray:5 3}
.mleg{display:flex;gap:16px;font-size:11px;color:var(--ink2);margin:2px 0 0 40px}
.bridge{font-size:12px;color:var(--ink2);margin:2px 0 0 40px;line-height:1.45}.bridge .src{font-family:'IBM Plex Mono',Menlo,monospace;font-size:9.5px;color:var(--mute)}
.mleg .kb{display:inline-block;width:15px;height:15px;border-radius:8px;background:#0f5a85;color:#fff;font:700 10px 'IBM Plex Sans',sans-serif;text-align:center;line-height:15px;margin-right:3px;vertical-align:-3px}
.mleg a{color:var(--accent);text-decoration:none;font-family:'IBM Plex Mono',Menlo,monospace;font-size:10.5px}
.fig-loop2.sm svg.big-svg{width:900px}
.mleg span.k{display:inline-block;width:22px;height:12px;border-radius:6px;vertical-align:-2px;margin-right:6px}
.symgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:3px 20px;font-size:11.3px;line-height:1.36;color:var(--ink2)}
.symgrid.sm{font-size:10.5px;line-height:1.28;gap:1px 18px;margin-top:4px;border-top:1px solid var(--rule);padding-top:4px}
#help{display:none!important}
.p3refs{margin-top:auto;border-top:none;box-shadow:0 -1px 0 var(--rule)}
.p3refs .pgrefs li{margin-bottom:0;line-height:10px}
.p3refs .p3rh{line-height:12px}
"""

def render(font_dir=None):
    parts = ['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
             '<title>Agent acceleration in a stable environment</title>', '<style>', bd.font_css(font_dir), bd.CSS, EXTRA_CSS, '</style></head><body>',
             '<div id="stage">']
    n = 0
    order = ([s for s in S if s["kind"] not in ("appendix", "refs")] + [s for s in S if s["kind"] == "refs"]
             + [s for s in S if s["kind"] == "appendix"])
    for s in order:
        if s["kind"] in ("main", "refs"):
            n += 1
            label = f"{TAG} · {n:02d}"
        elif s["kind"] == "appendix":
            label = f"{TAG} · {s['label']}"
        else:
            label = ""
        parts.append(f'<section class="slide {s["kind"]}" id="{s["id"]}">')
        if s["cover"]:
            parts.append(s["body"])
        else:
            parts.append(f'<div class="head"><div class="label">{label}</div><h1>{s["title"]}</h1></div><div class="rule"></div>')
            parts.append('<div class="content">')
            if s["callout"]:
                parts.append(f'<div class="callout">{s["callout"]}</div>')
            parts.append(f'<div class="body">{s["body"]}</div></div>')
            if s["foot"]:
                parts.append(f'<div class="foot">{s["foot"]}</div>')
            if s["chip"]:
                parts.append(f'<a class="chip" href="{s["chip"][0]}">{esc(s["chip"][1])}{" ↗" if s["chip"][0] != "#back" else ""}</a>')
        parts.append('</section>')
    parts.append('</div><div id="help"></div>')   # kept empty and hidden: the shared script and the fit check look it up
    parts.append(f'<script>{bd.JS}</script></body></html>')
    return "".join(parts)

# ---------------------------------------------------------------- the formula that runs through the deck
bd.FX["per task"] = [("op", r"v_n(m^{\prime})="), ("S", r"\dfrac{C_{\mathrm{learn}}}{n}"), ("op", "+"),
                     ("C", r"\bar{v}(m^{\prime})"), ("op", r"\quad\mathrm{s.t.}\ "), ("R", r"\bar{R}(m^{\prime})\geq R_0")]
DN, UP, KEEP = bd.DN, bd.UP, bd.KEEP
def citet(*keys):
    """Narrative citation: Surname et al. (Year) and Surname et al. (Year)."""
    forms = [cite(k)[1:-1] for k in keys]
    return " and ".join(re.sub(r", (\d{4}[a-z]?)$", r" (\1)", f) for f in forms)

def ul(items):
    return '<ul class="tb">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

def fx(marks, legend=True):
    return bd.fx(("per task", marks), legend=legend)

C_EXEC, C_LEARN, QQ = tex(r"\bar{v}(m^{\prime})", 13), tex(r"C_{\mathrm{learn}}", 13), tex(r"\bar{R}(m^{\prime})\geq R_0", 13)

# Row indices in slides/part3-data/rows.json (= the §6 table of the literature document, in order)
R = dict(ace=13, awm=14, axis=98, sica=67, wma=73, draft=44, mobilegpt=35, walt=81, harnessfix=84, growing=88,
         echopath=90, webcoach=31, hajimiri=94, reasoningbank=32, clawtrace=95, agentdevel=69, skillweaver=36,
         actionengine=80, speedrunner=82, metis=19, gptswarm=9, openskill=50, unbrowse=91, appworld=76)
R.update(genericagent=42, sedm=28, espo=96, gepa=12, adas=55, gea=65, grounding=93, skillnb=92)
def c(*names):
    return cite(*[n if n.startswith("ref-") else R[n] for n in names])

def p1(k):
    """Short form of a Part 1 source, registered for this page's references."""
    a = "ref-p1-" + k
    cite(a)
    return FORM[a]

def mech_svg():
    """Part 1's agent loop (one attempt), with learning's effects marked and the loop across tasks drawn around it:
    End -> run record -> learning (C_learn) -> updated harness -> next task. Badges mark where the harness acts:
    P prompt and memory, S skills and tools, C control code."""
    svg = bd.loop_svg(hl=("n-steps", "n-calls", "n-succ"), cls="big-svg", big=True)
    for id_, cls in (("n-rtok", "xh"), ("n-read", "nd")):
        svg = re.sub(r'(id="ah\d+-' + id_ + r'" class="node(?: pill)?)"', r'\1 ' + cls + '"', svg)
    svg = svg.replace('viewBox="0 0 1200 196"', 'viewBox="-46 0 1246 256"', 1)
    A, M = "#0f5a85", "#7d8a96"
    o = ('<defs><marker id="oa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
         f'<path d="M0 0 L10 5 L0 10 z" style="fill:{A}"/></marker></defs>')
    y = 228
    seg = lambda d, end=True: f'<path d="{d}" style="stroke:{A};stroke-width:1.6;fill:none"' + (' marker-end="url(#oa)"' if end else '') + '/>'
    def box(x0, x1, inner):
        return (f'<rect x="{x0}" y="{y - 14}" width="{x1 - x0}" height="28" rx="14" style="fill:#eef4f8;stroke:{A}"/>'
                f'<text x="{(x0 + x1) / 2}" y="{y + 5}" text-anchor="middle" style="font:13px \'IBM Plex Sans\',sans-serif;fill:#1b2733">{inner}</text>')
    o += seg(f"M1140 118 V{y} H1062")
    o += box(940, 1060, "run record")
    o += seg(f"M940 {y} H862")
    o += box(650, 860, 'learning, at cost C<tspan baseline-shift="sub" font-size="9">learn</tspan>').replace('fill:#eef4f8;stroke:' + A, 'fill:#fbeede;stroke:#e2b98b')
    o += seg(f"M650 {y} H614")
    o += f'<rect x="120" y="{y - 14}" width="492" height="28" rx="14" style="fill:#eef4f8;stroke:{A}"/>'
    o += f'<text x="134" y="{y + 5}" style="font:700 13px \'IBM Plex Sans\',sans-serif;fill:{A}">updated harness:</text>'
    for cx, ch, label in ((258, "P", "prompt, memory"), (395, "S", "skills, tools"), (505, "C", "control code")):
        o += (f'<circle cx="{cx}" cy="{y}" r="9" style="fill:{A}"/>'
              f'<text x="{cx}" y="{y + 4.5}" text-anchor="middle" style="font:700 12px \'IBM Plex Sans\',sans-serif;fill:#fff">{ch}</text>'
              f'<text x="{cx + 13}" y="{y + 5}" style="font:13px \'IBM Plex Sans\',sans-serif;fill:#1b2733">{label}</text>')
    o += seg(f"M120 {y} H-28 V62 H10")
    o += f'<text transform="translate(-36 150) rotate(-90)" text-anchor="middle" style="font:12px \'IBM Plex Mono\',monospace;fill:{A}">next task</text>'
    o += f'<text x="1068" y="{y - 22}" style="font:11px \'IBM Plex Mono\',monospace;fill:{A}">ACROSS TASKS</text>'
    def badge(x, yy, ch):
        return (f'<circle cx="{x}" cy="{yy}" r="9" style="fill:{A}"/>'
                f'<text x="{x}" y="{yy + 4.5}" text-anchor="middle" style="font:700 12px \'IBM Plex Sans\',sans-serif;fill:#fff">{ch}</text>')
    o += badge(184, 14, "C") + badge(260, 146, "P") + badge(762, 42, "S") + badge(1044, 104, "C")
    head, _, tail = svg.rpartition("</svg>")   # only the outer figure, not the formula images inside it
    return head + o + "</svg>" + tail



# =====================================================================
# Cover
# =====================================================================
slide("s00", "Agent acceleration in a stable environment", kind="title", cover=True, body="""
<div class="cover cover-deck"><div class="cover-one">
  <h1 class="cover-title">Agent Acceleration in a Stable Environment</h1>
  <p class="cover-sub">Learning from repeated tasks to make later ones faster and cheaper</p>
  <ol class="cover-q">
   <li>Can what an agent learns on earlier tasks lower the time and money of later tasks, with the cost of learning counted?</li>
   <li>After how many tasks does the learning pay for itself?</li>
   <li>Which parts of the agent should learning change, and should it learn from its own runs or from exploring the environment?</li>
   <li>Does what it learned still work on new tasks and after the environment changes, without lowering the success rate?</li>
  </ol>
  <p class="cover-date" style="margin-top:28px">October 2026</p>
</div></div>""")

# =====================================================================
# I · The problem
# =====================================================================
slide("s01", "Problem: make repeated tasks faster and cheaper",
  crumb="cost per success, with the learning cost spread over the n tasks it serves · time is reported beside money, never added to it",
  callout="<p><b>An agent runs the same workflow many times with new inputs. What it learns on earlier tasks should lower the time and money of later tasks, with the cost of learning counted, without lowering the success rate.</b></p>",
  body=f"""
{table(["formula", "meaning", "symbols", "source"], [
    [tex(r"v(m,p)=\dfrac{C_m(p)}{R_m(p)}", 13) + "<br>" + tex(r"T_{\mathrm{success}}(m,p)=\dfrac{\mathbb{E}[T_{\mathrm{attempt}}]}{R_m(p)}", 13),
     tex("v", 11) + " (the source’s cost-of-pass): expected cost per success on one task, retrying until it succeeds<br><br>" + tex(r"T_{\mathrm{success}}", 11) + ": expected time per success on one task",
     ul([tex("m", 11) + ": the agent, a model plus the program around it (the harness); “m” for model, as in the source",
         tex("p", 11) + ": one task, e.g. one expense report; “p” for problem, as in the source",
         tex("C_m(p)", 11) + ": expected cost (C) of one attempt, in dollars",
         tex("R_m(p)", 11) + ": success rate (R), the chance that one attempt succeeds",
         tex(r"T_{\mathrm{attempt}}", 11) + ": time (T) of one attempt, in seconds"]),
     tex("v", 11) + ": from " + citet("ref-p1-cop") + "<br><br>" + tex(r"T_{\mathrm{success}}", 11) + ": self-defined, the same form as " + tex("v", 11)],
    [tex(r"\bar{v}(m)=\dfrac{1}{n}\sum_{k=1}^{n}v(m,p_k)", 13),
     tex(r"\bar{v}", 11) + ": the average over " + tex("n", 11) + " tasks; " + tex(r"\bar{T}_{\mathrm{success}}", 11) + " and the average success rate " + tex(r"\bar{R}", 11) + " are taken the same way",
     ul([tex("n", 11) + ": number of tasks, e.g. expense reports filed",
         tex("p_k", 11) + ": the " + tex("k", 11) + "-th task, " + tex(r"k=1,\dots,n", 11)]),
     "Self-defined, adapted from " + citet("ref-p1-cop") + "."],
    [tex(r"v_n(m^{\prime})=\dfrac{C_{\mathrm{learn}}}{n}+\bar{v}(m^{\prime})", 13),
     tex("v_n", 11) + ": expected cost per task after learning, learning cost included",
     ul([tex(r"m^{\prime}", 11) + ": the same agent after learning, model unchanged, harness changed",
         tex(r"C_{\mathrm{learn}}", 11) + ": cost of learning (exploring, proposing and checking changes, keeping them up to date), each counted once"]),
     "Self-defined, adapted from " + citet("ref-ai-agents-that-matter", 46) + "."],
    [tex(r"\min\ \left(\bar{T}_{\mathrm{success}}(m^{\prime}),\ v_n(m^{\prime})\right)", 12) + "<br>" + tex(r"\mathrm{s.t.}\quad \bar{R}(m^{\prime})\geq R_0", 12),
     "The goal: lower time and money per task, success held",
     ul([tex("R_0", 11) + ": lowest required success rate, fixed in advance, measured on tasks not used for learning"]),
     "Self-defined."],
    [tex(r"n^{*}=\dfrac{C_{\mathrm{learn}}}{\bar{v}(m)-\bar{v}(m^{\prime})}", 13),
     tex("n^{*}", 11) + ": break-even, the number of tasks after which " + tex(r"v_n(m^{\prime})", 11) + " falls below " + tex(r"\bar{v}(m)", 11),
     "—",
     "Self-defined, from row 3; " + citet("ref-ai-agents-that-matter") + " report a break-even point."],
  ], ["29%", "21%", "33%", "17%"], cls="tbl p3t")}
<div class="figcap" style="margin-top:6px">Each source’s original formula, and what we changed and why: <a href="#a00">Appendix A0 ↗</a></div>""",
  chip=("#a00", "Appendix A0"))

slide("s1m", "How an agent runs a task, and where learning changes it",
  callout="<p><b>One attempt is a loop of steps. Learning changes the harness to cut steps, model calls and failures; the price is a longer prompt.</b></p>",
  body=f"""
<div class="fig-loop2 sm">{mech_svg()}</div>
<div class="mleg"><span><span class="k" style="background:var(--accent)"></span>learning aims to improve it</span><span><span class="k" style="background:#fbeede;border:1px solid #e2b98b"></span>always paid: learned text in the prompt; the learning bill</span><span><span class="k" style="background:#f3f7fa;border:1px dashed var(--accent)"></span>possible direction: a cached, stable prompt prefix</span><span><a href="#a00-2">symbol sources: A0 ↗</a></span></div>
<div class="mleg"><span><span class="kb">P</span><span class="kb">S</span><span class="kb">C</span> where the updated harness acts: prompt and memory · skills and tools · control code</span><span>may go either way: calls per step, non-model time, success</span></div>
<div class="bridge">One attempt adds up to {tex(r"T_{\mathrm{attempt}}=\Sigma_{i}\,(D_i+E_i)-T_{\mathrm{saving}}", 11)} <span class="src">(adapted from {p1("isp")}; {p1("asyncfc")})</span> and {tex(r"c_m(p)=\Sigma_{i,j,\kappa}\,n^{\kappa}_{ij}\,c_{\kappa}(\mu_{ij})+x_{\mathrm{env}}\,c_{\mathrm{env}}", 11)} <span class="src">(adapted from {cite("ref-p1-cop")[1:-1]})</span></div>

<div class="symgrid sm">
 <div>{tex(r"N,\ i", 10)} steps in one attempt; step index (observe, decide, act, wait)</div>
 <div>{tex(r"J_i,\ j", 10)} model calls in step {tex("i", 10)} (plan, check, retry); {tex("j", 10)} numbers them</div>
 <div>{tex(r"\ell_{ij}", 10)} how long the {tex("j", 10)}-th model call of step {tex("i", 10)} takes</div>
 <div>{tex(r"D_i,\ E_i", 10)} model time of step {tex("i", 10)}; all its other time</div>
 <div>{tex(r"\mathrm{TTFT}_{ij}", 10)} time to the first output token: queue, then prefill (reading the prompt; cached input is cheaper)</div>
 <div>{tex(r"n^{\mathrm{out}}_{ij},\ \mathrm{TPOT}_{ij}", 10)} output tokens; time per output token</div>
 <div>{tex(r"T_{\mathrm{saving}}", 10)} time hidden by doing things at once</div>
 <div>{tex(r"o_{a,i}", 10)} what step {tex("i", 10)} saw: page, screenshot, tool result</div>
 <div>{tex(r"z_{a,i},\ \Phi", 10)} what the model wrote in step {tex("i", 10)}; {tex(r"\Phi", 10)}: its chat format (role tags)</div>
 <div>{tex(r"|H_{a,i}|,\ a", 10)} prompt length agent {tex("a", 10)} reads in step {tex("i", 10)}; {tex("a", 10)}: which agent, if several</div>
 <div>{tex(r"n^{\kappa}_{ij},\ \kappa", 10)} tokens per billing class: cached, cache-written, uncached, output</div>
 <div>{tex(r"c_{\kappa}(\mu),\ \mu", 10)} price per token of class {tex(r"\kappa", 10)} on the model {tex(r"\mu", 10)} that serves the call</div>
 <div>{tex(r"x_{\mathrm{env}},\ c_{\mathrm{env}}", 10)} billed environment use; its price per unit</div>
 <div>{tex(r"R_m(p)", 10)} probability that one attempt succeeds, checked afterwards</div>
 <div>{tex(r"c_m(p)", 10)} dollars of one attempt; its expectation is page 1’s {tex("C_m(p)", 10)}</div>
</div>""")

slide("s02", "Example: a web agent that files expense reports",
  crumb="term: C_m′(p) — the part of a run that is repeated discovery or rework",
  callout="<p><b>Our running example: a web agent files expense reports; each task is a new report in the same system. Not knowing one rule of the form, that a hotel expense needs check-in and check-out dates, sends the agent into a rework loop.</b></p>",
  body=f"""
<div class="lbl">One hotel report, before the agent knows the rule</div>
<div style="width:100%"><svg width="1180" height="140" viewBox="0 0 1180 140" style="width:100%;height:auto;display:block"><defs><marker id="ah2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:#7d8a96"/></marker><marker id="ah3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:#b3600c"/></marker></defs><rect x="0" y="34" width="128" height="58" rx="4" style="fill:#fff;stroke:#cdd5dd"/><text x="9" y="48" style="font:10px 'IBM Plex Mono',monospace;fill:var(--mute)">1</text><text x="9" y="63" style="font:12px 'IBM Plex Sans',sans-serif;fill:var(--ink)">Open a new</text><text x="9" y="76" style="font:12px 'IBM Plex Sans',sans-serif;fill:var(--ink)">expense report</text><rect x="152" y="34" width="128" height="58" rx="4" style="fill:#fff;stroke:#cdd5dd"/><text x="161" y="48" style="font:10px 'IBM Plex Mono',monospace;fill:var(--mute)">2</text><text x="161" y="63" style="font:12px 'IBM Plex Sans',sans-serif;fill:var(--ink)">Choose the expense</text><text x="161" y="76" style="font:12px 'IBM Plex Sans',sans-serif;fill:var(--ink)">type: Hotel</text><rect x="304" y="34" width="128" height="58" rx="4" style="fill:#fff;stroke:#cdd5dd"/><text x="313" y="48" style="font:10px 'IBM Plex Mono',monospace;fill:var(--mute)">3</text><text x="313" y="63" style="font:12px 'IBM Plex Sans',sans-serif;fill:var(--ink)">Upload the receipt</text><rect x="456" y="34" width="128" height="58" rx="4" style="fill:#fff;stroke:var(--accent)"/><text x="465" y="48" style="font:10px 'IBM Plex Mono',monospace;fill:var(--mute)">4</text><text x="465" y="63" style="font:12px 'IBM Plex Sans',sans-serif;fill:var(--ink)">Submit</text><rect x="648" y="34" width="128" height="58" rx="4" style="fill:#fbeede;stroke:#e2b98b"/><text x="657" y="48" style="font:10px 'IBM Plex Mono',monospace;fill:var(--mute)">5</text><text x="657" y="63" style="font:12px 'IBM Plex Sans',sans-serif;fill:var(--warn)">Error: check-in and</text><text x="657" y="76" style="font:12px 'IBM Plex Sans',sans-serif;fill:var(--warn)">check-out dates</text><text x="657" y="89" style="font:12px 'IBM Plex Sans',sans-serif;fill:var(--warn)">are required</text><rect x="800" y="34" width="128" height="58" rx="4" style="fill:#fbeede;stroke:#e2b98b"/><text x="809" y="48" style="font:10px 'IBM Plex Mono',monospace;fill:var(--mute)">6</text><text x="809" y="63" style="font:12px 'IBM Plex Sans',sans-serif;fill:var(--warn)">Find the date fields</text><text x="809" y="76" style="font:12px 'IBM Plex Sans',sans-serif;fill:var(--warn)">and fill them</text><rect x="1052" y="34" width="128" height="58" rx="4" style="fill:#fff;stroke:var(--accent)"/><text x="1061" y="48" style="font:10px 'IBM Plex Mono',monospace;fill:var(--mute)">7</text><text x="1061" y="63" style="font:12px 'IBM Plex Sans',sans-serif;fill:var(--ink)">Check the saved</text><text x="1061" y="76" style="font:12px 'IBM Plex Sans',sans-serif;fill:var(--ink)">report</text><path d="M130,63 H149" style="stroke:#7d8a96;fill:none" marker-end="url(#ah2)"/><path d="M282,63 H301" style="stroke:#7d8a96;fill:none" marker-end="url(#ah2)"/><path d="M434,63 H453" style="stroke:#7d8a96;fill:none" marker-end="url(#ah2)"/><path d="M586,63 H645" style="stroke:#b3600c;fill:none" marker-end="url(#ah3)"/><text x="616" y="56" text-anchor="middle" style="font:10px 'IBM Plex Mono',monospace;fill:var(--warn)">rejected</text><path d="M778,63 H797" style="stroke:#b3600c;fill:none" marker-end="url(#ah3)"/><path d="M864,93 V116 H520 V96" style="stroke:#b3600c;fill:none;stroke-width:1.4" marker-end="url(#ah3)"/><text x="692" y="132" text-anchor="middle" style="font:11px 'IBM Plex Mono',monospace;fill:var(--warn)">rework loop: submit again, until the form is accepted</text><path d="M520,33 V16 H1116 V30" style="stroke:#7d8a96;fill:none" marker-end="url(#ah2)"/><text x="818" y="11" text-anchor="middle" style="font:10px 'IBM Plex Mono',monospace;fill:var(--mute)">accepted</text></svg></div>
<div class="two" style="margin-top:8px;flex:none">
  {card("WITHOUT LEARNING", "The loop is paid again on every hotel report",
        ["Its extra model calls and seconds are part of " + tex(r"\bar{v}(m)", 11) + ", for each of the " + tex("n", 11) + " reports"], "")}
  {card("LEARNING THE RULE ONCE", "The rule is learned once, at cost " + tex(r"C_{\mathrm{learn}}", 11) + "; later reports skip the loop",
        [tex(r"\bar{v}(m^{\prime})<\bar{v}(m)", 11) + "; it pays off after " + tex(r"n^{*}", 11) + " reports (page 1)"], "")}
</div>
<div class="two" style="margin-top:10px;flex:none;grid-template-columns:1fr 1.25fr">
 <div><div class="lbl">In this example</div>
  <ul class="symlist">
   <li><b>Environment</b>: the expense system, its forms, the fields each expense type requires, the actions it allows</li>
   <li><b>Run record</b>: the steps above, with the error message, and the time and cost of each step</li>
  </ul></div>
 <div><div class="lbl">What learning may change here (model weights fixed)</div>
  <ul class="symlist">
   <li><b>Prompt</b>: an instruction read on every call: fill the check-in and check-out dates before submitting a hotel expense</li>
   <li><b>Memory</b>: a note read only when relevant: Hotel → check-in and check-out dates required</li>
   <li><b>Skill or tool</b>: a procedure the model calls when it needs it: instructions plus a script that fills every field a hotel expense requires</li>
   <li><b>Control code</b>: the harness’s own logic, run whatever the model decides: check the required fields before every submit</li>
  </ul></div>
</div>
<div class="path" style="margin-top:12px"><span class="pl" style="width:auto;margin-right:10px">SCOPE</span><span class="s">this example: expense reports on a website</span>→<span class="s">any workflow repeated in one software environment</span>→<span class="s">websites · desktop applications · mobile apps · tool APIs</span></div>
""")

def ev(name, key, text):
    return f'<b>{name}</b> <span class="wcite">{c(key)}</span><br>{text}'

def grp(label):
    return f'<tr class="grp"><td colspan="4">{label}</td></tr>'

def drow(n, claim, cells):
    return f'<tr><td><b>{n} · {claim}</b></td>' + "".join(f"<td>{x}</td>" for x in cells) + "</tr>"

def works(*pairs):
    return "Works: " + " · ".join(f"{n} {c(k)}" for n, k in pairs)

def steps_fig():
    """Difficulty 1 as two timelines: WebCoach, 10.7 steps in 215 s against 10.2 steps in 395 s (time per step calc.)."""
    W0, sc = 56, 0.55            # left margin for row labels; px per second
    def row(y, n, sec, extra, label, right):
        out = f'<text x="0" y="{y+13}" style="font:10.5px \'IBM Plex Mono\',monospace;fill:var(--mute)">{label}</text>'
        per = sec / n
        x = W0
        full, frac = int(n), n - int(n)
        for k in range(full + (1 if frac > 0.05 else 0)):
            f = 1 if k < full else frac
            wb = (per - extra) * sc * f; we = extra * sc * f
            out += f'<rect x="{x:.1f}" y="{y}" width="{max(wb-1.5,1):.1f}" height="18" rx="2" style="fill:#c9d5df"/>'
            if extra:
                out += f'<rect x="{x+wb-1.5:.1f}" y="{y}" width="{max(we-1.5,1):.1f}" height="18" rx="2" style="fill:#f2c79a"/>'
            x += (wb + we)
        out += f'<text x="{x+8:.1f}" y="{y+13}" style="font:12px \'IBM Plex Sans\',sans-serif;fill:var(--ink)">{right}</text>'
        return out
    sv = '<svg width="400" height="96" viewBox="0 0 400 96" style="width:100%;height:auto;display:block">'
    sv += row(4, 10.7, 215, 0, "BEFORE", "<tspan font-weight=\'700\'>10.7</tspan> steps · 215 s")
    sv += row(34, 10.2, 395, 395/10.2 - 215/10.7, "AFTER", "<tspan font-weight=\'700\'>10.2</tspan> steps · 395 s")
    sv += '<rect x="56" y="68" width="12" height="9" rx="2" style="fill:#c9d5df"/><text x="72" y="76" style="font:10.5px \'IBM Plex Sans\',sans-serif;fill:var(--ink2)">one step</text>'
    sv += '<rect x="132" y="68" width="12" height="9" rx="2" style="fill:#f2c79a"/><text x="148" y="76" style="font:10.5px \'IBM Plex Sans\',sans-serif;fill:var(--ink2)">extra reading and thinking in each step</text>'
    sv += '<text x="56" y="92" style="font:9.5px \'IBM Plex Mono\',monospace;fill:var(--mute)">length = seconds per task · per step 20.1 → 38.7 s (calc.)</text>'
    return sv + '</svg>'

def drawn(main, key, also):
    """'Drawn from X. Also seen in: Y, what it saw · Z, what it saw' — the figure shows one work; the others found the same."""
    return f"Drawn from {main} {c(key)}. Also: " + " · ".join(f"{n} {c(k)}, {w}" for n, k, w in also)

def seen(also):
    """For a schematic figure: the works that saw it, with what each saw."""
    return "Seen in: " + " · ".join(f"{n} {c(k)}, {w}" for n, k, w in also)

def _lbl(x, y, t, anchor="start", size=10.5, mono=True, col="var(--mute)", bold=False):
    f = "'IBM Plex Mono',monospace" if mono else "'IBM Plex Sans',sans-serif"
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="font:{"700 " if bold else ""}{size}px {f};fill:{col}">{t}</text>'

def blocks_fig():
    """Difficulty 2 (schematic): during the first run the steps cannot be told apart; once it succeeds, looking back
    shows which were needed and which were search or rework; the next report of that kind skips the latter."""
    G, O, U = "#c9d5df", "#f2c79a", "#eef2f5"
    pat = "goggoogog"
    x0, bw, gap = 112, 20, 4
    def row(y, label, kind):
        out = _lbl(0, y + 13, label, size=9.5)
        x = x0
        for ch in pat:
            if kind == "next" and ch == "o":
                continue
            fill = U if kind == "first" else (G if ch == "g" else O)
            out += f'<rect x="{x}" y="{y}" width="{bw}" height="18" rx="2" style="fill:{fill};stroke:{"#c9d5df" if kind == "first" else "none"}"/>'
            if kind == "first":
                out += _lbl(x + bw/2, y + 13, "?", anchor="middle", mono=False, size=11, col="var(--mute)")
            x += bw + gap
        out += _lbl(x + 2, y + 13, "✓", mono=False, size=13, col="var(--accent)", bold=True)
        return out
    sv = '<svg width="400" height="100" viewBox="0 0 400 100" style="width:100%;height:auto;display:block">'
    sv += row(2, "FIRST RUN", "first")
    sv += row(28, "LOOKING BACK", "back")
    sv += row(54, "NEXT REPORT", "next")
    sv += f'<rect x="{x0}" y="84" width="12" height="9" rx="2" style="fill:{G}"/>' + _lbl(x0 + 16, 92, "needed", mono=False, col="var(--ink2)")
    sv += f'<rect x="{x0 + 70}" y="84" width="12" height="9" rx="2" style="fill:{O}"/>' + _lbl(x0 + 86, 92, "search or rework, skipped next time", mono=False, col="var(--ink2)")
    return sv + '</svg>'

def reading_fig():
    """Difficulty 3: SEDM on FEVER, prompt tokens over the run without and with its memory (difference calc.)."""
    G, O = "#c9d5df", "#f2c79a"
    sc = 230 / 2.47
    sv = '<svg width="400" height="100" viewBox="0 0 400 100" style="width:100%;height:auto;display:block">'
    sv += _lbl(0, 17, "NO MEMORY") + f'<rect x="76" y="4" width="{1.65*sc:.0f}" height="18" rx="2" style="fill:{G}"/>' + _lbl(76 + 1.65*sc + 6, 17, "1.65M tokens read", mono=False, size=11.5, col="var(--ink)")
    sv += _lbl(0, 45, "MEMORY") + f'<rect x="76" y="32" width="{1.65*sc:.0f}" height="18" rx="2" style="fill:{G}"/>' + f'<rect x="{76 + 1.65*sc + 1:.0f}" y="32" width="{0.82*sc:.0f}" height="18" rx="2" style="fill:{O}"/>' + _lbl(76 + 2.47*sc + 6, 45, "2.47M", mono=False, size=11.5, col="var(--ink)", bold=True)
    sv += f'<rect x="76" y="62" width="12" height="9" rx="2" style="fill:{G}"/>' + _lbl(92, 70, "the task’s own prompt", mono=False, col="var(--ink2)")
    sv += f'<rect x="220" y="62" width="12" height="9" rx="2" style="fill:{O}"/>' + _lbl(236, 70, "memory, read again on every call", mono=False, col="var(--ink2)")
    sv += _lbl(76, 90, "prompt tokens over the FEVER run; +0.82M calc.", size=9.5)
    return sv + '</svg>'

G_, O_, A_ = "#c9d5df", "#f2c79a", "#0f5a85"

def _box(x, y, w, h, lines, kind="g", size=10.5):
    fill, stroke, col = {"g": ("#fff", "#c9d5df", "var(--ink)"), "o": ("#fbeede", "#e2b98b", "var(--warn)"),
                         "a": ("#eef4f8", A_, "var(--ink)")}[kind]
    t = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" style="fill:{fill};stroke:{stroke}"/>'
    for k, l in enumerate(lines):
        t += _lbl(x + 5, y + 13 + k * 12, l, mono=False, size=size, col=col)
    return t

def _arr(d, col="#7d8a96", mk="a2"):
    return f'<path d="{d}" style="stroke:{col};fill:none" marker-end="url(#{mk})"/>'

DEFS_ = ('<defs><marker id="a2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:#7d8a96"/></marker>'
         '<marker id="a3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:#b3600c"/></marker></defs>')

def check_fig():
    """Difficulty 2 (schematic, the framing note's own form example): check the form after choosing Hotel, or skip it."""
    sv = f'<svg width="400" height="104" viewBox="0 0 400 104" style="width:100%;height:auto;display:block">{DEFS_}'
    sv += _box(0, 38, 68, 30, ["Choose type:", "Hotel"])
    sv += _arr("M68 46 C76 46 76 16 84 16") + _arr("M68 60 C76 60 76 82 84 82")
    sv += _box(86, 4, 86, 24, ["check the form"], "a") + _arr("M172 16 H180") + _box(182, 4, 60, 24, ["fill dates"]) + _arr("M242 16 H250") + _box(252, 4, 48, 24, ["submit"])
    sv += _lbl(306, 21, "✓", mono=False, size=13, col="var(--accent)", bold=True)
    sv += _lbl(86, 42, "one step more, always right", size=9)
    sv += _box(86, 70, 118, 24, ["skip: as last time"]) + _arr("M204 82 H212") + _box(214, 70, 48, 24, ["submit"])
    sv += _lbl(270, 80, "✓ rule still holds", mono=False, size=10, col="var(--accent)") + _lbl(270, 95, "✗ it changed: rework", mono=False, size=10, col="var(--warn)")
    sv += _lbl(398, 10, "schematic", anchor="end", size=9, col="var(--accent)")
    return sv + '</svg>'

def tradeoff_fig():
    """Difficulty 3 (schematic): forms of learned material placed by cost to use and by how well they cope with change."""
    sv = f'<svg width="400" height="116" viewBox="0 0 400 116" style="width:100%;height:auto;display:block">{DEFS_}'
    x0, y0, x1, y1 = 34, 98, 394, 4
    sv += _arr(f"M{x0} {y0} H{x1}") + _arr(f"M{x0} {y0} V{y1}")
    sv += _lbl(x1, y0 + 13, "cost per use →", anchor="end", size=9.5, col="var(--ink2)")
    sv += _lbl(x0, y0 + 13, "schematic", anchor="start", size=9, col="var(--accent)")
    sv += f'<text transform="translate(22 {y0 - 4}) rotate(-90)" style="font:9.5px \'IBM Plex Mono\',monospace;fill:var(--ink2)">generalizes →</text>'
    sv += '<path d="M78 84 C150 72 230 50 330 24" style="stroke:#dbe3ea;stroke-width:7;fill:none;stroke-linecap:round"/>'
    for (x, y, t, lx, ly, anc) in [(78, 84, "replayed script", 88, 92, "start"), (160, 68, "skill: steps + script", 170, 78, "start"),
                                   (245, 47, "note in memory", 255, 56, "start"), (330, 24, "note in every prompt", 322, 15, "end")]:
        sv += f'<circle cx="{x}" cy="{y}" r="5" style="fill:{A_}"/>' + _lbl(lx, ly, t, mono=False, size=10.5, col="var(--ink)", anchor=anc)
    sv += f'<rect x="42" y="8" width="112" height="24" rx="12" style="fill:none;stroke:{A_};stroke-dasharray:4 3"/>' + _lbl(98, 24, "cheap and general?", anchor="middle", mono=False, size=10, col="var(--accent)")
    return sv + '</svg>'

def cause_fig():
    """Difficulty 4 (schematic): one error message, possible causes of different kinds checked one by one; the cost of checking grows."""
    sv = f'<svg width="600" height="100" viewBox="0 0 600 100" style="width:100%;height:auto;display:block">{DEFS_}'
    sv += _box(0, 18, 112, 34, ["Error: over the", "meal limit"], "o", size=10.5)
    sv += _lbl(132, 10, "possible causes, of different kinds, checked one by one", size=9.5, col="var(--ink2)")
    causes = [("reasoning", "wrong type?"), ("rule", "limit changed?"), ("interaction", "wrong field?"), ("tool", "amount misread?")]
    W, GAP, X0 = 100, 8, 132
    sv += _arr(f"M112 35 H{X0 - 3}")
    for k, (kind, q) in enumerate(causes):
        x = X0 + k * (W + GAP)
        sv += f'<rect x="{x}" y="18" width="{W}" height="34" rx="3" style="fill:#fff;stroke:#c9d5df"/>'
        sv += _lbl(x + 6, 31, kind, size=9, col="var(--accent)") + _lbl(x + 6, 45, q, mono=False, size=10.5, col="var(--ink)")
        h = 6 * (k + 1)
        sv += f'<rect x="{x}" y="{86 - h}" width="{W}" height="{h}" rx="2" style="fill:#f2c79a"/>'
        if k < len(causes) - 1:
            sv += _arr(f"M{x + W} 35 H{x + W + GAP - 1}")
    xe = X0 + 4 * (W + GAP)
    sv += _lbl(xe + 2, 40, "…?", mono=False, size=13, col="var(--mute)", bold=True)
    sv += _lbl(X0, 97, "cost of checking so far →", size=9, col="var(--warn)")
    sv += _lbl(0, 76, "the cause may be found", mono=False, size=10, col="var(--ink2)") + _lbl(0, 89, "late, or not at all", mono=False, size=10, col="var(--ink2)")
    sv += _lbl(598, 10, "schematic", anchor="end", size=9, col="var(--accent)")
    return sv + '</svg>'

def breakeven_fig():
    """Difficulty 5 (schematic): total cost over reports, without learning, and with learning, testing and upkeep after changes."""
    sv = f'<svg width="600" height="112" viewBox="0 0 600 112" style="width:100%;height:auto;display:block">{DEFS_}'
    x0, y0, x1, y1 = 40, 86, 596, 4
    sv += _arr(f"M{x0} {y0} H{x1}") + _arr(f"M{x0} {y0} V{y1}")
    sv += _lbl(x1, y0 + 13, "number of reports filed →", anchor="end", size=9.5, col="var(--ink2)")
    sv += f'<text transform="translate(28 {y0 - 2}) rotate(-90)" style="font:9.5px \'IBM Plex Mono\',monospace;fill:var(--ink2)">total cost →</text>'
    sv += _lbl(x0, y0 + 13, "schematic", size=9, col="var(--accent)")
    nl = lambda x: y0 - 84 * (x - x0) / 460
    steps = [(290, 7), (420, 7)]          # upkeep after the site changes
    def learn(x, base):
        return base - 20 * (x - x0) / 460 - sum(h for xs, h in steps if x >= xs)
    def path(base):
        d, xp = f"M{x0} {base:.1f}", x0
        for xs, h in steps + [(500, 0)]:
            d += f" L{xs} {learn(xs - 0.01, base):.1f}"
            if h:
                d += f" L{xs} {learn(xs, base):.1f}"
        return d
    def cross(base):
        for k in range(4600):
            x = x0 + k / 10
            if learn(x, base) >= nl(x):
                return x, nl(x)
        return None
    sv += f'<path d="M{x0} {y0} L500 {nl(500):.1f}" style="stroke:#7d8a96;stroke-width:2;fill:none"/>' + _lbl(506, 11, "no learning", mono=False, size=10.5, col="var(--ink)")
    sv += f'<path d="{path(66)}" style="stroke:{A_};stroke-width:2;fill:none"/>' + _lbl(506, 38, "with learning", mono=False, size=10.5, col="var(--accent)")
    sv += f'<path d="{path(50)}" style="stroke:{A_};stroke-width:1.5;stroke-dasharray:5 4;fill:none"/>' + _lbl(506, 24, "more testing", mono=False, size=10, col="var(--accent)")
    sv += _lbl(296, learn(300, 66) + 14, "repair after the site changes", mono=False, size=9.5, col="var(--ink2)")
    c1, c2 = cross(66), cross(50)
    if c1:
        sv += f'<circle cx="{c1[0]:.0f}" cy="{c1[1]:.0f}" r="4" style="fill:{A_}"/><path d="M{c1[0]:.0f} {c1[1]:.0f} V{y0}" style="stroke:{A_};stroke-dasharray:2 3"/>' + _lbl(c1[0], y0 + 13, "break-even", anchor="middle", mono=False, size=10, col="var(--accent)") + _lbl(c1[0], y0 + 24, "n*", anchor="middle", mono=False, size=11, col="var(--accent)", bold=True)
    if c2:
        sv += f'<circle cx="{c2[0]:.0f}" cy="{c2[1]:.0f}" r="3.5" style="fill:#fff;stroke:{A_}"/><path d="M{c2[0]:.0f} {c2[1]:.0f} V{y0}" style="stroke:{A_};stroke-dasharray:2 3"/>' + _lbl(c2[0], y0 + 13, "break-even,", anchor="middle", mono=False, size=10, col="var(--accent)") + _lbl(c2[0], y0 + 24, "more testing", anchor="middle", mono=False, size=10, col="var(--accent)")
    sv += _lbl(52, 12, "learning and testing are paid first", mono=False, size=10, col="var(--ink2)") + _arr("M60 16 L44 62")
    return sv + '</svg>'

slide("s03c", "Five difficulties, grouped by the cost they affect",
  body=f"""<div class="tightcards">
<div class="lbl" style="text-align:center">Cost per task after learning · {tex(r"\bar{v}(m^{\prime})", 11)}</div>
<div class="cards3" style="flex:none">
  {card("", "1 · Fewer steps do not always save time", steps_fig() + '<div class="cd" style="margin-top:4px">Each step got longer: judge a report by its seconds, not its steps</div>',
     drawn("WebCoach", "webcoach", [("ReasoningBank", "reasoningbank", "fewer steps, more tokens")]))}
  {card("", "2 · Whether a check is needed is not known in advance", check_fig() + '<div class="cd" style="margin-top:4px">Skipping a check saves a step only while the rule still holds</div>',
     seen([("DRAFT", "draft", "learns tool conditions by trying"), ("SKILL.nb", "skillnb", "checks before reuse")]))}
  {card("", "3 · A trade-off between generalization and cost per use", tradeoff_fig(),
     seen([("Metis", "metis", "keeps both text and code"), ("ActionEngine", "actionengine", "turns a site map into programs")]))}
</div>
<div class="lbl" style="text-align:center;margin-top:6px">Cost of learning · {tex(r"C_{\mathrm{learn}}", 11)}</div>
<div class="two" style="flex:none">
  {card("", "4 · Finding the cause behind an error message", cause_fig() + '<div class="cd" style="margin-top:2px">Each possible cause costs a check; the right one may come late, or never</div>',
     seen([("HarnessFix", "harnessfix", "finds the faulty step"), ("ESPO", "espo", "sorts errors first")]))}
  {card("", "5 · Learning and testing can cost more than they save", breakeven_fig() + '<div class="cd" style="margin-top:2px">Learning pays off only if enough reports share its cost</div>',
     seen([("AI Agents That Matter", "ref-ai-agents-that-matter", "late break-even"), ("SICA", "sica", "large bill, small saving")]))}
</div></div>""",
  chip=("#ad", "Appendix D"))

# =====================================================================
# II · How far existing work has got
# =====================================================================
J = json.load(open(os.path.join(HERE, "part3-data", "rows.json"), encoding="utf-8"))
CLASS = [("1提示", "Prompts and context", "a02"), ("1记忆", "Experience memory", "a03"), ("1技能", "Skills and tools", "a04"),
         ("1框架", "Whole harness", "a05"), ("2A预测后果", "Predicting what an action does", "a06"),
         ("2B说明事实前提", "Descriptions, facts and preconditions", "a07"), ("2C页面地点结构", "Page and place structure", "a08"),
         ("2D探索练习", "Exploring and practising", "a09"), ("2E判分环境", "Environments that check the final state (no learning)", "a06")]

def tally(ids):
    f = lambda k, v: sum(1 for i in ids if J[i]["j"][k] == v)
    return len(ids), (f(0, "Y"), f(0, "P")), (f(1, "Y"), f(1, "P")), (f(2, "Y"), f(2, "P"))

def ids_of(cat):
    return [i for i, r in enumerate(J) if cat in r["cats"]]

def yp(t):
    return f"{t[0]} · {t[1]}"

def class_table(rows, total_ids):
    body = []
    for cat, what, rep in rows:
        n, a, b, d = tally(ids_of(cat))
        name, apx = next((x[1], x[2]) for x in CLASS if x[0] == cat)
        body.append([f'{name}<br><a href="#{apx}">{apx.upper()} ↗</a>', f'<b style="font-size:15px">{n}</b>', what, rep,
                     yp(a), yp(b), yp(d)])
    n, a, b, d = tally(total_ids)
    body.append(["All, each work once", f'<b style="font-size:15px">{n}</b>', "", "", yp(a), yp(b), yp(d)])
    t = table(["class", "works", "what changes", "representative work: one number and its conditions",
               "time or money of runs<br>yes · partly", "learning cost<br>yes · partly", "unseen tasks<br>yes · partly"],
              body, ["19%", "6%", "14%", "37%", "8%", "8%", "8%"], cls="tbl p3t")
    t = t.replace("<tr><td>All, each work once", '<tr class="tot"><td>All, each work once')
    for col in range(4, 7):
        pass
    return re.sub(r"<td>(\d+ · \d+)</td>", r'<td class="c">\1</td>', t)

D1 = [i for i, r in enumerate(J) if any(x.startswith("1") for x in r["cats"])]
D2 = [i for i, r in enumerate(J) if any(x.startswith("2") and x != "2E判分环境" for x in r["cats"])]
n1, a1, b1, d1 = tally(D1)
n2, a2, b2, d2 = tally(D2)
NOTE = "One row per work in our literature table; a work in two classes counts in both. Yes / partly: our initial judgment from the table cells (calc.), defined in Appendix A1."

PW = dict(reflexion=0, selfrefine=1, textgrad=2, mipro=3, protegi=4, semback=5, trace=6, promst=7, dc=8, gptswarm=9, avatar=10, dspy=11, gepa=12, ace=13)
PN = dict(reflexion="Reflexion", selfrefine="Self-Refine", textgrad="TextGrad", mipro="MIPRO", protegi="ProTeGi", semback="semantic backpropagation",
          trace="Trace", promst="PROMST", dc="Dynamic Cheatsheet", gptswarm="GPTSwarm", avatar="AvaTaR", dspy="DSPy", gepa="GEPA", ace="ACE")

def c_idx(i):
    return cite(i)

def opt(label, *works):
    return f'<span class="opt"><b>{label}</b> ' + " · ".join(PN[w] for w in works) + '</span>'

def dsrow(choice, *opts):
    return f'<tr><td>{choice}</td><td>' + "".join(opts) + '</td></tr>'

def mflow(*steps, loop=True):
    """A mechanism as a row of small steps; the last arrow loops back when loop=True."""
    out = '<div class="mflow">'
    for k, st in enumerate(steps):
        cls = "mst key" if st.startswith("!") else "mst"
        out += f'<span class="{cls}">{st.lstrip("!")}</span>'
        if k < len(steps) - 1:
            out += '<span class="marr">→</span>'
    if loop:
        out += '<span class="marr loop">↺</span>'
    return out + '</div>'

def mech(title, works, flow, example, twist, tags):
    return (f'<div class="mcard"><div class="mtitle">{title}</div>{flow}'
            f'<div class="mex"><b>e.g.</b> {example}</div>'
            f'<div class="mtw">{twist}</div>'
            f'<div class="mtags">' + "".join(f'<span>{t}</span>' for t in tags) + f'</div>'
            f'<div class="mworks">{works}</div></div>')

def wk3(*keys):
    return " · ".join(f"{PN[k]} {c_idx(PW[k])}" for k in keys)

slide("s05", f"Direction 1 · Learning from the agent’s own runs: {n1} works in four classes",
  crumb="counts: one row per work in our literature table, a work in two classes counted in both · yes / partly: initial judgment from table cells (calc.), Appendix A1",
  callout=f"<p><b>Of {n1} works that change what sits outside the model, {a1[0]} measured the seconds or dollars of running tasks, {b1[0]} what learning cost, and {d1[0]} tested on unseen tasks.</b></p>",
  body=fx({"C": DN, "S": UP}, legend=False) + class_table([
    ("1提示", "the prompt, instructions or context read on the next task",
     "ACE: offline adaptation lifts AppWorld from 42.4 to 59.4 (with labels), and takes 9,517 s against GEPA’s 53,898 s — DeepSeek-V3.1 " + c("ace")),
    ("1记忆", "retrievable experience: successes, failures, workflows",
     "AWM: 35.5% vs 23.5% success on WebArena (the baseline also reads HTML), 5.9 vs 7.9 steps against an accessibility-tree BrowserGym — GPT-4-0613 " + c("awm")),
    ("1技能", "callable functions, scripts, skill documents",
     "AXIS: 29.9 s vs 59.5 s and $0.2 vs $0.4 per task, 84% vs 52% success, against UFO on 50 Microsoft Word tasks; learning cost not reported " + c("axis")),
    ("1框架", "the outer program: tools, control loop, the improver itself",
     "SICA: $1.91 → $1.70 and 130.2 → 114.5 s per task, for a whole run of about $7,000; the benchmark that picked the agent also scored it " + c("sica")),
  ], D1) + '<div class="figcap">Yes · partly: our initial judgment from the per-work table (calc.; Appendix A1). A work in two classes counts in both.</div>',
  chip=("#a02", "Appendix A2–A5"))

def paths_fig(paths, segs, head, keys, *, H, X, W, start_y, mid):
    """One flowchart for a class of direction 1: earlier runs (left) through paths of small steps (middle)
    into what they write (right). paths: (name, tags, steps, kinds, yc, ytarget[, note]); one kind per step:
    g other, k decided by a measured score, o kept without a test. segs: (y0, y1, head, line 1, line 2, fill)."""
    A, O, G = "#0f5a85", "#b3600c", "#7d8a96"
    sv = (f'<svg width="1180" height="{H}" viewBox="0 0 1180 {H}" style="width:100%;height:auto;display:block">'
          f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:#7d8a96"/></marker></defs>')
    def t(x, y, s_, size=11, col="#1b2733", mono=False, anchor="start", bold=False):
        f = "'IBM Plex Mono',monospace" if mono else "'IBM Plex Sans',sans-serif"
        return f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="font:{"700 " if bold else ""}{size}px {f};fill:{col}">{s_}</text>'
    STY = {"g": ("#f6f8fa", "#c9d5df"), "k": ("#eef4f8", A), "o": ("#fbeede", "#e2b98b")}
    def box(x, yc, lines, kind="g", w=152):
        fill, stroke = STY[kind]
        out = f'<rect x="{x}" y="{yc - 16}" width="{w}" height="32" rx="3" style="fill:{fill};stroke:{stroke}"/>'
        y0 = yc - (len(lines) - 1) * 6.5 + 4
        for k, l in enumerate(lines):
            out += t(x + 7, y0 + k * 13, l, 11, "#1b2733", bold=(kind == "k"))
        return out
    arr = lambda d: f'<path d="{d}" style="stroke:#7d8a96;fill:none" marker-end="url(#{mid})"/>'
    ys = start_y + 37
    sv += f'<rect x="0" y="{start_y}" width="124" height="74" rx="4" style="fill:#fff;stroke:{A}"/>'
    sv += t(12, start_y + 24, "earlier runs", 12.5, bold=True) + t(12, start_y + 41, "trajectories and", 10.5, "#3b4a57") + t(12, start_y + 55, "their outcomes", 10.5, "#3b4a57")
    for name, tags, steps, kinds, yc, ytarget, *note in paths:
        sv += arr(f"M124 {ys} C138 {ys} 138 {yc} {X[0] - 3} {yc}")
        sv += t(X[0], yc - 22, name, 10, A, mono=True) + t(X[0] + 8 + len(name) * 6.1, yc - 22, tags, 9.5, G, mono=True)
        for k, (st, kd) in enumerate(zip(steps, kinds)):
            sv += box(X[k], yc, st, kd, W)
            if k < len(steps) - 1:
                sv += arr(f"M{X[k] + W} {yc} H{X[k + 1] - 3}")
        xe = X[len(steps) - 1] + W
        sv += arr(f"M{xe} {yc} C{xe + 40} {yc} 860 {ytarget} 896 {ytarget}")
        if note:
            sv += t(xe + 8, yc + 16, note[0], 9.5, O, mono=True)
    for x, kd, label in keys:
        fill, stroke = STY[kd]
        sv += f'<rect x="{x}" y="{H - 28}" width="14" height="8" rx="2" style="fill:{fill};stroke:{stroke}"/>' + t(x + 20, H - 20, label, 10, "#3b4a57")
    sv += t(900, 14, head, 9.5, A, mono=True)
    for y0, y1, hd, l1, l2, fill in segs:
        sv += f'<rect x="898" y="{y0}" width="282" height="{y1 - y0}" style="fill:{fill};stroke:#c9d5df"/>'
        sv += t(908, y0 + 17, hd, 11, A if fill != "#f6f8fa" else G, bold=True)
        sv += t(908, y0 + 33, l1, 10.5, "#3b4a57") + (t(908, y0 + 47, l2, 10.5, "#3b4a57") if l2 else "")
    return sv + '</svg>'

def prompt_paths_fig():
    """Prompt learning: from earlier runs (trajectories and outcomes), three paths into the next prompt."""
    paths = [
        ("1 · REWRITE THE INSTRUCTIONS", "answers · kept if better · offline", [["failures, or good runs", "beside bad ones"], ["model says what went", "wrong or what differed"], ["rewrite: several", "candidates"], ["score on validation", "reports, keep the best"]], "gggk", 62, 54),
        ("2 · SUCCESSFUL RUNS AS EXAMPLES", "task metric · kept if better · offline", [["keep runs that", "succeeded"], ["turn them into", "worked examples"], ["score example sets,", "keep the best"]], "ggk", 142, 132),
        ("3 · GROW A PLAYBOOK", "the model’s own reading · no test · online", [["after each report, a", "reflector writes lessons"], ["a curator adds or", "merges notes"]], "go", 222, 202, "no test per change"),
    ]
    segs = [(24, 92, "instructions", "“For a hotel expense, fill the", "dates before submitting”", "#eef4f8"),
            (92, 160, "worked examples", "an accepted hotel report", "", "#eef4f8"),
            (160, 236, "playbook of notes", "“Hotel → dates required”", "“Meal → under the daily limit”", "#eef4f8"),
            (236, 284, "this report and its history", "not learned: new every time", "", "#f6f8fa")]
    keys = [(150, "k", "decides what is kept: only if it scores better"), (440, "o", "kept without a test"), (590, "g", "other steps")]
    return paths_fig(paths, segs, "THE PROMPT READ ON THE NEXT REPORT", keys, H=290, X=[150, 320, 490, 660], W=152, start_y=104, mid="pa")

def memory_check_fig():
    """Experience memory as one pipeline: earlier runs -> extract an entry -> one of four checks -> the store -> the next report.
    The works differ in the check; check 4 scores entries after use (the dashed loop back from the next report)."""
    A, O, G, INK, SUB = "#0f5a85", "#b3600c", "#7d8a96", "#1b2733", "#3b4a57"
    STY = {"g": ("#f6f8fa", "#c9d5df"), "k": ("#eef4f8", A), "o": ("#fbeede", "#e2b98b"), "w": ("#fff", A)}
    H = 262
    sv = (f'<svg width="1180" height="{H}" viewBox="0 0 1180 {H}" style="width:100%;height:auto;display:block">'
          '<defs><marker id="pm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:#7d8a96"/></marker></defs>')
    def t(x, y, s_, size=11, col=INK, mono=False, anchor="start", bold=False):
        f = "'IBM Plex Mono',monospace" if mono else "'IBM Plex Sans',sans-serif"
        return f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="font:{"700 " if bold else ""}{size}px {f};fill:{col}">{s_}</text>'
    def rect(x, y, w, h, kd, rx=3):
        fill, stroke = STY[kd]
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" style="fill:{fill};stroke:{stroke}"/>'
    def arr(d, dash=False):
        return f'<path d="{d}" style="stroke:#7d8a96;fill:none{";stroke-dasharray:4 3" if dash else ""}" marker-end="url(#pm)"/>'
    sv += rect(0, 81, 112, 74, "w", 4) + t(11, 105, "earlier runs", 12.5, bold=True) + t(11, 122, "trajectories and", 10.5, SUB) + t(11, 136, "their outcomes", 10.5, SUB)
    sv += arr("M112 118 H131")
    sv += rect(134, 88, 170, 60, "g") + t(144, 111, "extract an entry", 12, bold=True) + t(144, 127, "a workflow, a lesson,", 10.5, SUB) + t(144, 141, "a case or a site fact", 10.5, SUB)
    X0, W0, XS = 330, 360, 722
    for yc, kd, lines, n in [
            (34, "o", ["1 · no check: store it as it is"], "13 works"),
            (90, "k", ["2 · re-run tasks with it and without it;", "keep it if the gain beats its time and tokens"], "3 works"),
            (146, "k", ["3 · check it on the site, read-only;", "keep it only if the site confirms it"], "2 works"),
            (202, "k", ["4 · keep it; each task that uses it later", "raises its score if it passes, lowers it if not"], "4 works")]:
        sv += arr(f"M304 118 C318 118 318 {yc} {X0 - 3} {yc}")
        sv += rect(X0, yc - 21, W0, 42, kd)
        y0 = yc - (len(lines) - 1) * 7 + 4
        for k, l in enumerate(lines):
            sv += t(X0 + 8, y0 + k * 14, l, 11)
        sv += t(X0 + W0 - 8, yc + 4, n, 9.5, G, mono=True, anchor="end")
        sv += arr(f"M{X0 + W0} {yc} H{XS - 3}")
    sv += rect(XS, 10, 262, 214, "k", 0)
    sv += t(XS + 10, 28, "MEMORY · ONE ENTRY PER LINE", 9.5, A, mono=True) + t(XS + 252, 28, "score (4)", 9, G, mono=True, anchor="end")
    rows = [("Hotel: type → dates → amount → submit", "0.9"), ("“Fill the dates before submitting”", "0.8"),
            ("an accepted hotel report (a case)", "0.6"), ("“Dates are typed DD/MM/YYYY”", ""), ("“No dates: the form rejects it”", "")]
    for k, (e, sc) in enumerate(rows):
        y = 60 + k * 32
        sv += f'<line x1="{XS}" y1="{y - 20}" x2="{XS + 262}" y2="{y - 20}" style="stroke:#c9d5df"/>'
        sv += t(XS + 10, y, e, 10.5, SUB) + (t(XS + 252, y, sc, 10.5, A, mono=True, anchor="end") if sc else "")
    sv += arr(f"M{XS + 262} 118 H1005")
    sv += rect(1008, 80, 172, 76, "w", 4) + t(1018, 102, "next report", 12, bold=True) + t(1018, 119, "reads only the entries", 10.5, SUB) + t(1018, 133, "closest to it; with 4,", 10.5, SUB) + t(1018, 147, "the best-scored first", 10.5, SUB)
    sv += arr("M1094 156 V244 H510 V227", dash=True) + t(XS + 10, 239, "4 · pass: score up · fail: score down", 9.5, A, mono=True)
    sv += rect(0, H - 18, 14, 8, "o", 2) + t(20, H - 10, "stored without a check", 10, SUB)
    sv += rect(170, H - 18, 14, 8, "k", 2) + t(190, H - 10, "checked", 10, SUB)
    return sv + '</svg>'

slide("s05p", "Learning prompts and context: three paths to the next prompt",
  callout="<p><b>All three paths start from earlier runs and end in the prompt read on the next report; they differ in which part of the prompt they write and whether a change is tested.</b></p>",
  body=f"""
<div style="width:100%">{prompt_paths_fig()}</div>
<div class="figcap" style="margin:2px 0 4px">Tested changes need answers and re-runs, so they are found offline and then frozen; untested notes are cheap, so they can be added online, report by report.</div>
{table(["path", "works, and what each adds"], [
    ["1 · Rewrite the instructions", f"AvaTaR {cite(PW['avatar'])}: compares good and bad runs instead of failures alone · ProTeGi {cite(PW['protegi'])}: rewrites from a summary of errors · TextGrad {cite(PW['textgrad'])}: written critiques passed back through the program’s parts · semantic backpropagation {cite(PW['semback'])}: the same, with an update gate · Trace {cite(PW['trace'])}: prompts and code changed together · PROMST {cite(PW['promst'])}: human-written error rules and a learned scorer · GEPA {cite(PW['gepa'])}: keeps candidates that win on some tasks · MIPRO {cite(PW['mipro'])}: instructions and examples searched together · ESPO {cite(96)}: sorts errors before rewriting · GPTSwarm {cite(PW['gptswarm'])}: the prompts and links of an agent graph"],
    ["2 · Successful runs as examples", f"DSPy {cite(PW['dspy'])}: successful traces become examples · MIPRO {cite(PW['mipro'])}: also searches the examples"],
    ["3 · Grow a playbook", f"ACE {cite(PW['ace'])}: adds, updates and de-duplicates entries; built offline, then grown online · Dynamic Cheatsheet {cite(PW['dc'])}: the model keeps, rewrites and deletes entries itself"],
    ["Same task only", f"Reflexion {cite(PW['reflexion'])}, Self-Refine {cite(PW['selfrefine'])}: notes kept only for retrying the same task, dropped before the next one"],
  ], ["17%", "83%"], cls="tbl p3t ptab")}""",
  chip=("#a02", "Appendix A2"), page_refs=False)

def wl(*pairs):
    """Works with their citations: 'AWM (Wang et al., 2025a) · ReasoningBank (…)'."""
    return " · ".join(f"{n} {cite(i)}" for n, i in pairs)

slide("s05m", "Learning experience memory: four ways to check an entry",
  callout="<p><b>All works share one pipeline, from earlier runs to entries that a new report reads; they differ in how an entry is checked, and most store it unchecked.</b></p>",
  body=f"""
<div style="width:100%">{memory_check_fig()}</div>
<div class="figcap" style="margin:2px 0 4px">Unchecked entries need no extra runs, so they can be added online, report by report; re-runs and scores need many runs, so FORGE, MemRL and MemQ learn offline, then freeze.</div>
{table(["path", "works"], [
    ["1 · No check", wl(("AWM", 14), ("ReasoningBank", 32), ("ExpeL", 15), ("CTIM-Rover", 23), ("Agent S", 29), ("EXG", 26), ("MobileGPT", 35), ("G-Memory", 22), ("DecentMem", 25), ("WebCoach", 31), ("ReAP", 33), ("Mem²Evolve", 20), ("Memento", 34))],
    ["2 · Re-run with and without", wl(("SEDM", 28), ("FORGE", 21), ("EvolveMem", 24))],
    ["3 · Check on the site", wl(("Metis", 19), ("Grounding Agent Memory", 93))],
    ["4 · Scored by later tasks", wl(("MemRL", 16), ("MemQ", 17), ("AEL", 18), ("Memento’s trained scorer", 34))],
    ["Other works of this class", wl(("ACE", 13), ("Dynamic Cheatsheet", 8)) + ": the previous page’s playbook · " + wl(("SE-Agent", 30), ("Meta-TTL", 27)) + ": one task only · " + citet(94) + ": a comparison with a plain agent"],
  ], ["17%", "83%"], cls="tbl p3t ptab")}""",
  chip=("#a03p", "Appendix A3"), page_refs=False)

slide("s07", f"Direction 2 · Learning the environment: {n2} works keep four kinds of knowledge",
  crumb="counts: one row per work in our literature table, a work in two classes counted in both · yes / partly: initial judgment from table cells (calc.), Appendix A1",
  callout=f"<p><b>Of {n2} works that keep knowledge about the environment, {a2[0]} measured the seconds or dollars of running tasks, {b2[0]} what exploring cost, and {d2[0]} tested on unseen tasks.</b></p>",
  body=fx({"C": DN, "S": UP}, legend=False) + class_table([
    ("2A预测后果", "what the page will look like after an action",
     "WMA: 140.3 s vs 748.3 s and $0.4 vs $2.7 per instruction against tree search, 16.6% vs 19.2% success — WebArena, GPT-4o " + c("wma")),
    ("2B说明事实前提", "tool parameters and errors; facts and traps of the site",
     "DRAFT: correct tool paths 88.00 vs 71.00 for ReAct on RestBench TMDB, GPT-4o; time and cost not reported " + c("draft")),
    ("2C页面地点结构", "a map of pages, actions and the paths between them",
     "MobileGPT: −62.5% latency and −68.8% cost on repeated tasks with human-repaired paths; exploring took 10–15 min per app, $10.78 in all " + c("mobilegpt")),
    ("2D探索练习", "self-set practice tasks, turned into tools",
     "WALT: 50.1% and 52.9% success on WebArena and VisualWebArena; exploring and checking cost $1.67 per tool, repaid after about 14 uses " + c("walt")),
  ], D2) + f'<div class="figcap">Yes · partly: our initial judgment from the per-work table (calc.; Appendix A1). A work in two classes counts in both.</div>',
  chip=("#a06", "Appendix A6–A9"))

slide("s08", "Exploring a site, keeping a checked rule, and using it on the next task",
  crumb="direction 2 · the exploring is C_learn · the rule removes rework from C_m′(p) · it must be re-checked when the site changes",
  callout="<p><b>The agent probes the form, writes down what it found together with where it applies and the evidence for it, and reads that note on the next task, so the rework loop of the expense example does not happen.</b></p>",
  body=f"""
<div class="panel3">
 <div><div class="lbl">1 · Explore the form</div>Change the expense type from Meal to Hotel. Two new required fields appear: check-in and check-out date. Submitting without them returns an error.</div>
 <div><div class="lbl">2 · Keep a checked rule</div><div class="guide"><b>site-guide.md</b><br>scope: new expense form<br>IF type = Hotel → check-in and check-out dates required<br>evidence: 2 probes, 1 error message<br>re-check: when the form changes</div></div>
 <div><div class="lbl">3 · Use it on the next task</div>New hotel expense + the live page + the saved note → fill every required field → submit once → check the saved report.</div>
</div>
<div class="path"><span class="pl">WITHOUT THE NOTE</span><span class="s">submit</span>→<span class="s rw">error</span>→<span class="s rw">fill the dates</span>→<span class="s rw">submit again</span>→<span class="s">check</span></div>
<div class="path"><span class="pl">WITH THE NOTE</span><span class="s">fill the dates</span>→<span class="s">submit</span>→<span class="s">check</span></div>
<div class="two" style="margin-top:12px">
  {card("REAL CALLS CORRECT THE DESCRIPTION", "Trying an action and reading its result can fix what a description gets wrong",
        ["DRAFT learned from a real call that a tool needs a valid person_id, and wrote it into the tool’s documentation " + c("draft")], "")}
  {card("ONE OBSERVATION IS NOT A RULE", "A rule written from one observation can be wrong, and a local check can miss it",
        ["DRAFT generalised from one error message; SkillWeaver’s local checks passed broken functions " + c("draft", "skillweaver")], "")}
</div>""",
  chip=("#a09", "Appendix A9"))

slide("s09", "Across both directions, what learning costs is rarely counted",
  crumb="C_learn rarely itemised · R_m′(p) ≥ R_0 hard to prove · fewer steps ≠ less time or money",
  callout="<p><b>The learning bill is rarely itemised, proving that a change is correct is the weak link, and a saving measured as fewer steps, or in one setting, does not guarantee less time or money elsewhere.</b></p>",
  body=f"""
<div class="cards4" style="flex:1">
  {card("LEARNING COST · " + C_LEARN, "Few works count both what learning costs and what it saves",
        ["5 of 102 works measured both the seconds or dollars of running tasks and a learning cost: GPTSwarm, MobileGPT, OpenSkill, EchoPath and Unbrowse (initial judgment, calc.) " + c("gptswarm", "mobilegpt", "openskill", "echopath", "unbrowse")], "")}
  {card("CORRECTNESS · " + QQ, "Showing that a change fixed the target without breaking what worked is the open problem",
        ["In AgentDevel’s ablations, the highest mean score and the fewest regressions on old tasks may have to be traded against each other " + c("agentdevel")], "")}
  {card("FEWER STEPS · " + C_EXEC, "Fewer steps is not the same as less time or money",
        ["Steps 9.7 → 8.3 on WebArena, while total tokens rose 50,847.4 → 53,054.5 in another table whose base set-up is not stated — ReasoningBank " + c("reasoningbank")], "")}
  {card("TRANSFER · " + C_EXEC, "A saving in one setting need not carry over",
        ["Median cost per task $0.143 vs $0.144 after moving to SkillsBench, no fall — ClawTrace, OpenClaw with gpt-5.4 " + c("clawtrace")], "")}
</div>""",
  chip=("#a01", "Appendix A1"))

slide("s10", "The closest works save time or money on repeated tasks; none counts the whole loop",
  crumb="v_n(m′,p) · what each closest work measured, and what it left out",
  callout="<p><b>In the works we checked, no single result covers all of these at once: any task stream, no training, automatic location of failures and waste, protection of old abilities, every learning and maintenance cost counted, and a net saving over time.</b></p>",
  body=table(["work", "what it learns", "what it shows: one number and its conditions", "what is left out"], [
    [f"<b>ActionEngine</b><div class='wcite'>{c('actionengine')}</div>", "a state-machine map of the site, with templates",
     "91.2% success (73.1% without the warmed-up map); 27 s vs 87 s and $0.05 vs $0.40 per task against Claude Code — WebArena, 655 tasks, Claude Opus 4.6",
     "per-task numbers exclude exploration and warm-up; break-even after 39–101 tasks still omits warm-up"],
    [f"<b>WALT</b><div class='wcite'>{c('walt')}</div>", "tools written from exploring each site",
     "$1.67 per tool to explore and check it, repaid after about 14 uses", "repairing tools after deployment is left to future work"],
    [f"<b>SpeedRunner</b><div class='wcite'>{c('speedrunner')}</div>", "programmatic skills",
     "BabyAI usage about one eighth, success from about 67% to near-perfect — gpt-5.4-mini, 200 online tasks, 30 held out, three seeds",
     "output tokens and dollars disagree in one figure; total learning cost [TBD: appendix A.3, to be re-read]"],
    [f"<b>HarnessFix</b><div class='wcite'>{c('harnessfix')}</div>", "repairs to the outer program from failed runs",
     "completion +6.3 to +18.4 points, mean of three runs", "time and cost of running tasks not reported"],
    [f"<b>Growing Harness</b><div class='wcite'>{c('growing')}</div>", "code changes from function-level failures",
     "inference cost at deployment −74.4% to −98.6%", "evaluator and offline optimiser not counted; break-even not measured"],
    [f"<b>Metis</b><div class='wcite'>{c('metis')}</div>", "text and code memory, frozen before the final tasks",
     "97.4K vs 112.6K tokens per AppWorld task", "memory manager not counted; apps never seen before not tested"],
  ], ["15%", "20%", "38%", "27%"], cls="tbl p2"),
  chip=("#a10", "Appendix A10"))

# =====================================================================
# Appendix A0 — each formula of page 1 against its source
# =====================================================================
def ours(f, tag):
    return f + f'<div class="wcite">{tag}</div>'

def orig(f, src):
    return f + f'<div class="wcite">{src}</div>'

slide("a00", "A0 · Page 1’s formulas: the original, ours, and why we changed it", label="A0 · 1/2", kind="appendix", chip=("#back", "← back"),
  body=table(["our formula", "original formula", "original definitions", "what we changed, and why"], [
    [ours(tex(r"v(m,p)=\dfrac{C_m(p)}{R_m(p)}", 12), "from the paper"),
     orig(tex(r"v(m,p)=\dfrac{C_m(p)}{R_m(p)}", 12) + " (Eq. 2)", cite("ref-p1-cop")),
     ul([tex("m", 10) + ": a model; " + tex("p", 10) + ": a problem",
         tex("C_m(p)", 10) + ": expected dollars of one attempt, input and output tokens times their prices (Eq. 13)",
         tex("R_m(p)", 10) + ": chance that one attempt is correct; " + tex(r"1/R_m(p)", 10) + " attempts are expected until the first correct one, attempts independent"]),
     ul([tex("m", 10) + " becomes the agent: the model plus its harness",
         "why: learning changes the harness, not the model"])],
    [ours(tex(r"T_{\mathrm{success}}(m,p)=\dfrac{\mathbb{E}[T_{\mathrm{attempt}}]}{R_m(p)}", 12), "self-defined, adapted"),
     orig("no time formula", cite("ref-p1-cop")),
     ul(["units per attempt other than dollars, such as time or latency, may matter more (App. D.1)"]),
     ul(["the same form, in seconds", "why: time and money are reported side by side", "assumes attempts run one after another"])],
    [ours(tex(r"\bar{v}(m)=\dfrac{1}{n}\sum_{k=1}^{n}v(m,p_k)", 12), "self-defined, adapted"),
     orig(tex(r"V_{p\sim D}(\mathcal{M})\approx\mathbb{E}_{p\sim P}[V_p(\mathcal{M})]", 12) + " (Eq. 8)", cite("ref-p1-cop")),
     ul([tex("D", 10) + ": a dataset of problems; " + tex("P", 10) + ": its empirical distribution, mass " + tex("1/n", 10) + " on each problem",
         tex(r"V_p(\mathcal{M})", 10) + ": the lowest cost per success on " + tex("p", 10) + " among the available models"]),
     ul(["the same average over " + tex("n", 10) + " tasks, applied to one agent’s " + tex("v", 10) + " instead of the cheapest model’s; " + tex(r"\bar{T}_{\mathrm{success}}", 10) + " and " + tex(r"\bar{R}", 10) + " the same way",
         "why: we compare one agent before and after learning"])],
    [ours(tex(r"v_n(m^{\prime})=\dfrac{C_{\mathrm{learn}}}{n}+\bar{v}(m^{\prime})", 12), "self-defined, adapted"),
     orig("total cost = fixed cost + variable cost (in words)", cite("ref-ai-agents-that-matter")) + "<br>" + orig(tex(r"O(nc+C)", 11) + " against " + tex(r"O(nC)", 11) + " (Table 2)", cite(46)),
     ul(["fixed cost: paid once, to optimise the agent’s design (prompt, hyperparameters)",
         "variable cost: paid on every run, set by its input and output tokens",
         tex("n", 10) + ": task instances; " + tex("C", 10) + ": one call of the large tool-making model; " + tex("c", 10) + ": one call of the small tool-using model"]),
     ul(["fixed cost ÷ " + tex("n", 10) + ": a cost per task",
         "variable part = the average cost per success " + tex(r"\bar{v}(m^{\prime})", 10) + ", so failed attempts are paid for",
         "fixed cost widened to exploring, proposing, checking and upkeep — why: our learning does all of these"])],
    [ours(tex(r"\min\ \left(\bar{T}_{\mathrm{success}}(m^{\prime}),\ v_n(m^{\prime})\right)", 11) + "<br>" + tex(r"\mathrm{s.t.}\ \bar{R}(m^{\prime})\geq R_0", 11), "self-defined"),
     orig(tex(r"V_p(\mathcal{M})=\min_{m\in\mathcal{M}}v(m,p)", 12) + " (Eq. 3)", cite("ref-p1-cop")) + "<br>" + orig("accuracy and cost optimised jointly (in words)", cite("ref-ai-agents-that-matter")),
     ul([tex(r"\mathcal{M}", 10) + ": the available models",
         tex(r"V_p(\mathcal{M})", 10) + ": the lowest cost per success on " + tex("p", 10) + " among them"]),
     ul(["one number becomes a pair, seconds and dollars, lowered together — why: no fixed exchange rate between them",
         "learning cost included",
         "success floor " + tex("R_0", 10) + ", fixed in advance — why: an agent must not look cheaper by succeeding less"])],
    [ours(tex(r"n^{*}=\dfrac{C_{\mathrm{learn}}}{\bar{v}(m)-\bar{v}(m^{\prime})}", 12), "self-defined"),
     orig("no formula (in words)", cite("ref-ai-agents-that-matter")),
     ul(["the jointly optimised agent is cheaper in total than the default one after about 1,350 HotPotQA tasks"]),
     ul(["written as a formula by setting " + tex(r"v_n(m^{\prime})=\bar{v}(m)", 10) + " — why: computable from measured costs",
         "assumes the saving per task stays the same"])],
  ], ["21%", "21%", "30%", "28%"], cls="tbl p3a p3t"))

slide("a00-2", "A0 · Every symbol in the agent loop", label="A0 · 2/2", kind="appendix", chip=("#back", "← back"),
  body=f"""<div class="fig-loop2" style="margin-bottom:8px">{mech_svg()}</div>
{bd.defs2([
  (r"i,\ N", "step (one observe–decide–act–wait round); steps in the attempt", p1("isp")),
  (r"J_i,\ j", "model calls in step " + tex("i", 12) + " (planner, judge, retries …); call index", "self-defined"),
  (r"\ell_{ij}", "latency of call " + tex("j", 12) + " of step " + tex("i", 12), p1("swm")),
  (r"\mathrm{TTFT}_{ij}", "time to the first generated token: queueing, sending, prefill of the uncached input", p1("distserve") + "; " + p1("aa")),
  (r"n^{\mathrm{out}}_{ij},\ \mathrm{TPOT}_{ij}", "output tokens of the call, thinking included; time per output token after the first", FORM["ref-p1-cop"] + " (adapted); " + p1("anth-b") + "; " + p1("distserve")),
  (r"D_i,\ E_i", "model time of step " + tex("i", 12) + "; all its other time (observe, act, wait, harness gaps, back-off)", "adapted from " + p1("isp") + "; " + p1("aospec")),
  (r"T_{\mathrm{saving}}", "time hidden because some of it ran at the same time; 0 if strictly serial", p1("asyncfc") + "; precedent " + p1("llmc")),
  (r"o_{a,i},\ a", "tokens the result or screenshot of step " + tex("i", 12) + " adds to the prompt; agent index", p1("react") + "; " + p1("yuan")),
  (r"|H_{a,i}|,\ \Phi,\ z_{a,i}", "length of the prompt step " + tex("i", 12) + "’s call reads (one call per step); chat template; the call’s output: thinking, message and tool-call tokens", p1("yuan")),
  (r"n^{\mathrm{hit}},\ n^{\mathrm{w}},\ n^{\mathrm{unc}}", "input tokens read from the cache, written to it, or uncached", p1("anth-b") + "; " + p1("tokenpilot") + "; " + p1("sglang")),
  (r"c_{\kappa}(\mu),\ \kappa,\ \mu", "price per token of billing class " + tex(r"\kappa", 12) + " on serving model " + tex(r"\mu", 12), "adapted from " + FORM["ref-p1-cop"]),
  (r"x_{\mathrm{env}},\ c_{\mathrm{env}}", "billed environment usage (e.g. sandbox hours); its price per unit", FORM["ref-p1-cop"] + " (adapted)"),
  (r"n^{\kappa}_{ij}", "tokens of billing class " + tex(r"\kappa", 12) + " in call " + tex("j", 12) + " of step " + tex("i", 12), FORM["ref-p1-cop"] + " (adapted); " + p1("anth-b")),
  (r"c_m(p)", "dollars of one attempt of agent " + tex("m", 12) + " on task " + tex("p", 12) + "; its expectation is " + tex("C_m(p)", 12), FORM["ref-p1-cop"]),
  (r"R_m(p)", "chance that one attempt of agent " + tex("m", 12) + " on task " + tex("p", 12) + " succeeds", cite("ref-p1-cop")[1:-1]),
])}""")

# =====================================================================
# Appendix A1 — definitions and totals
# =====================================================================
def tot_row(name, ids):
    n, a, b, d = tally(ids)
    return [name, str(n), yp(a), yp(b), yp(d)]

slide("a01", "A1 · How the three columns were judged, and the totals per class", label="A1", kind="appendix", chip=("#back", "← back"),
  body=table(["class", "works", "time or money of runs (yes · partly)", "learning cost (yes · partly)", "unseen tasks (yes · partly)"],
             [tot_row(x[1], ids_of(x[0])) for x in CLASS] + [tot_row("Direction 1, each work once", D1), tot_row("Direction 2, each work once (final-state checkers excluded)", D2)],
             ["40%", "9%", "17%", "17%", "17%"], cls="tbl p3t") + f"""
<div class="apx-note"><b>Time or money of runs</b> — yes: measured seconds or dollars of executing tasks with what was learned; partly: tokens, steps, calls or an author’s estimate only.
<b>Learning cost</b> — yes: a measured amount for learning, building or maintaining (tokens, dollars, time, compute or rollouts); partly: an estimate, iteration counts only, or a part knowingly left out.
<b>Unseen tasks</b> — yes: tested on tasks that took no part in learning or selection; partly: an online stream that learns as it goes, the same workflow with new parameters, or an unstated split.
These are our initial judgments from the cells of the per-work table (calc.), not re-read from the full texts; the representative works on pages 4 and 6 are to be checked one by one before the deck is final.</div>""")

# =====================================================================
# Appendix A2–A10 — per-work tables, paginated
# =====================================================================
MK = {"Y": "●", "P": "◐", "N": "○", "X": "–"}
def venue(v):
    return en(v.split("；")[0]) if v else ""

def arow(i):
    r, t = J[i], TR.get(i, {})
    a = re.findall(r"#(ref-[^)]+)\)", r["cite"])
    ct = cite(a[0]) if a else ""
    return [f"<b>{esc(r['work'])}</b><div class='wcite'>{ct}</div>", venue(r["venue"]), t.get("changes", ""), t.get("setting", ""),
            t.get("effect", ""), t.get("timecost", ""), f'<span class="mk">{"".join(MK[x] for x in r["j"])}</span>']

LEG = "Marks in the last column, in order: time or money of runs measured · learning cost measured · tested on unseen tasks; ● yes, ◐ partly, ○ no (initial judgment, calc.; Appendix A1)."
BUDGET = 3500
def apx_pages(aid, title, ids, lab=None):
    pages, cur, size = [], [], 0
    for i in ids:
        t = TR.get(i, {})
        L = sum(len(t.get(k, "")) for k in ("changes", "setting", "effect", "timecost")) + 60
        if cur and size + L > BUDGET - (500 if aid == "a10" else 0):
            pages.append(cur); cur, size = [], 0
        cur.append(i); size += L
    if cur:
        pages.append(cur)
    for k, p in enumerate(pages):
        sid = aid if k == 0 else f"{aid}-{k + 1}"
        L = lab or aid.upper()
        slide(sid, f"{L} · {title}" + (f" ({k + 1}/{len(pages)})" if len(pages) > 1 else ""), label=f"{L} · {k + 1}/{len(pages)}",
              kind="appendix", chip=("#back", "← back"),
              body=table(["work", "venue", "what it changes", "where it was tested", "effect, with conditions", "time, money, learning cost", "marks"],
                         [arow(i) for i in p], ["11%", "8%", "15%", "17%", "21%", "21%", "7%"], cls="tbl p3a") + f'<div class="figcap">{LEG}</div>')

def memory_paths_apx():
    """Appendix A3, first page: the memory page's paths, one line per work: what it stores and how its entries are judged."""
    W_ = lambda n, i, d: f"<b>{n}</b> {cite(i)}: {d}"
    slide("a03p", "A3 · Experience memory: what each work adds, by path", label="A3 · paths", kind="appendix", chip=("#back", "← back"),
      body=table(["path", "works, and what each adds"], [
        ["1 · No check", ul([
            W_("AWM", 14, "workflows induced from runs the model judged successful, appended and never re-ranked"),
            W_("ReasoningBank", 32, "lessons from failures as well as successes, judged by a model without answers and appended directly"),
            W_("ExpeL", 15, "successful runs, plus advice drawn from comparing successes and failures; the model edits and votes on the advice, and low-voted advice is deleted"),
            W_("CTIM-Rover", 23, "ExpeL-style advice, general and per code repository, edited by model votes"),
            W_("Agent S", 29, "whole-task and subtask memories; a self-evaluator judges success without answers"),
            W_("EXG", 26, "a graph linking each failure to the attempt that fixed it; all runs kept, entries with a fix preferred when reading"),
            W_("MobileGPT", 35, "a graph of each app’s pages and subtasks with their actions, saved when a task completes"),
            W_("G-Memory", 22, "linked memory of several agents’ exchanges, tasks and advice, filtered by the environment’s success signal and by relevance"),
            W_("DecentMem", 25, "a store for each agent and a router between exploring and reuse; all new experience joins the long-term store"),
            W_("WebCoach", 31, "summaries of all runs; a separate coach model decides when to pass advice to the acting model"),
            W_("ReAP", 33, "a written reflection on every training run, retrieved by task similarity"),
            W_("Mem²Evolve", 20, "experience plus new tools and expert agents; tools are repaired with tests drawn from the model’s critique, the experience is not checked"),
            W_("Memento", 34, "a library of cases, appended and retrieved by similarity")])],
        ["2 · Re-run with and without", ul([
            W_("SEDM", 28, "each candidate entry is replayed with and without it and admitted on the reward gain minus latency and token penalties; later down-weighted, merged or deleted by use"),
            W_("FORGE", 21, "several agents, each with its own memory of rules or examples; the best in a check episode copies its whole memory to the others; frozen at a threshold"),
            W_("EvolveMem", 24, "retrieval settings, answer style and re-extracted memory, changed from failure logs; large drops rolled back; the best round chosen on the same questions")])],
        ["3 · Check on the site", ul([
            W_("Metis", 19, "after a failure the reflector probes the environment for the cause, after a success it looks for waste; facts and traps kept as text; recurring plans become code that must compile with its dependencies"),
            W_("Grounding Agent Memory", 93, "after each task, candidate entries are checked with targeted read-only queries; the queries and the final score decide to add, narrow, delete or skip")])],
        ["4 · Scored by later tasks", ul([
            W_("MemRL", 16, "the environment’s reward updates the value of each entry used; retrieval by similarity and value"),
            W_("MemQ", 17, "the benchmark’s binary reward is passed along where each entry came from; retrieval by similarity and value; nothing is deleted"),
            W_("AEL", 18, "learns from the environment’s reward how to choose what to retrieve, with reflection and rules; code changes off by default"),
            W_("Memento", 34, "one version trains a two-layer network to score the cases")])],
        ["Not memory across tasks", ul([
            f"<b>ACE</b> {cite(13)}, <b>Dynamic Cheatsheet</b> {cite(8)}: a playbook in the prompt, kept and rewritten by the model (<a href=\"#s05p\">prompts and context</a>, path 3)",
            W_("SE-Agent", 30, "a pool of candidate runs for one task, rewritten, recombined and filtered"),
            W_("Meta-TTL", 27, "notes between attempts at one task; how to write them is learned offline and updated only if validation tasks improve")])],
        ["Compared with a plain agent", ul([
            f"<b>{citet(94)}</b>: on four WebArena domains with Gemini 3 Flash, three runs, a plain agent given 15 steps and trimmed pages had both the highest success, 44.78%, and the fewest tokens, 73.6K per task, against AWM, ASI and ReasoningBank given 10 steps; the budgets match only roughly"])],
      ], ["15%", "85%"], cls="tbl p3t"))

for cat, title, aid in CLASS[:8]:
    if aid == "a03":
        memory_paths_apx()
    apx_pages(aid, title, ids_of(cat) + (ids_of("2E判分环境") if aid == "a06" else []))
CLOSEST = [80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 14, 32, 35, 36, 19, 42, 68, 28]
apx_pages("a10", "The works closest to ours", [i for i in CLOSEST if i < len(J)])
apx_pages("ad", "Evidence behind the five difficulties", [31, 32, 42, 90, 35, 80, 94, 95, 28, 84, 96, 12, 67, 55, 65], lab="D")

# =====================================================================
# References
# =====================================================================
refs = sorted(USED, key=lambda a: re.sub("<[^>]+>", "", fmt_ref(a)).lower())
PER = 22
for k in range(0, len(refs), PER):
    chunk = refs[k:k + PER]
    slide(f"r{k // PER + 1:02d}", "References" + (f" ({k // PER + 1}/{-(-len(refs) // PER)})" if len(refs) > PER else ""), kind="refs",
          body='<ul class="refs3">' + "".join(f"<li>{fmt_ref(a, full=True)}</li>" for a in chunk) + "</ul>")

def word_report():
    rows = []
    for s in S:
        if s["kind"] != "main":
            continue
        text = re.sub(r"<svg.*?</svg>", " ", s["callout"] + " " + s["body"], flags=re.S)
        text = re.sub(r'<div class="p3refs">.*?</ul></div>', " ", text, flags=re.S)
        text = re.sub(r'<div class="(?:cc|wcite|figcap)">.*?</div>', " ", text, flags=re.S)
        text = html.unescape(re.sub(r"<[^>]+>", " ", text))
        text = re.sub(r"\([^()]*\d{4}[a-z]?[^()]*\)", " ", text)
        rows.append((s["id"], len(re.findall(r"[A-Za-z0-9$%€.,'’/×–\-]+", text))))
    return rows

if __name__ == "__main__":
    font_dir = sys.argv[sys.argv.index("--fonts") + 1] if "--fonts" in sys.argv else None
    out = render(font_dir)
    open(OUT, "w", encoding="utf-8").write(out)
    left = sorted(set(re.findall(r"[\u4e00-\u9fff]+", re.sub(r"<[^>]+>", " ", out))))
    print(f"wrote {OUT} ({len(out) / 1024:.0f} KB, {len(S)} pages, {len(refs)} references)")
    print("  Chinese left on pages:", left[:40] if left else "none")
    for id_, n in word_report():
        print(f"  {id_:6s} {n:4d} words")
