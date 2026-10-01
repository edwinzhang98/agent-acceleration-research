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
    if anchor == "ref-p1-cop" or not m:
        return raw if anchor == "ref-p1-cop" else en(raw)
    authors, year, rest = m.groups()
    title, _, after = rest.partition(". ")
    venue = re.split(r"\s*(?:\[正式引用链接\]|正式引用链接|实际读的版本|; OpenReview|; DOI)", after)[0].strip().rstrip(".")
    venue = re.split(r"[;,]\s*(?:decision|Poster|Oral|Spotlight|OpenReview|proceedings|Session)", venue)[0].strip().rstrip(".")
    out = f"{_au(authors)} ({year}). {en(title)}. <i>{en(venue)}</i>."
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
def slide(id_, title, body="", *, crumb="", callout="", foot="", chip=None, kind="main", cover=False, label=None):
    refs = PAGE[:]
    PAGE.clear()
    if kind == "main" and refs:
        body += bd.page_refs_html(sorted((fmt_ref(a) for a in refs), key=lambda r: re.sub("<[^>]+>", "", r).lower()), small=True)
    S.append(dict(id=id_, title=title, body=body, crumb=crumb, callout=callout, foot=foot, chip=chip, kind=kind,
                  cover=cover, label=label))

TAG = "LEARNING ACROSS TASKS"
EXTRA_CSS = r"""
.flow{display:flex;align-items:stretch;gap:5px}
.stp{flex:1;border:1px solid var(--rule);border-radius:4px;padding:7px 9px;font-size:12.5px;line-height:1.32;background:#fff}
.stp .n{display:block;font-family:'IBM Plex Mono',Menlo,monospace;font-size:10px;color:var(--mute);margin-bottom:2px}
.stp.rw{background:#fbeede;border-color:#e2b98b;color:var(--warn)}
.stp.key{border-color:var(--accent)}
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
.tbl.p3t a{color:var(--accent);text-decoration:none;font-family:'IBM Plex Mono',Menlo,monospace;font-size:10px}
.tbl.p3a{font-size:10px;line-height:1.3}.tbl.p3a td{padding:3px 6px 3px 4px}
.tbl.p3a td:first-child{font-family:'IBM Plex Sans',sans-serif;font-size:10px;color:var(--ink)}
.refs3{columns:2;column-gap:26px;font-size:9.6px;line-height:1.32;color:var(--ink2);padding-left:0;list-style:none;margin:0}
.refs3 li{break-inside:avoid;margin:0 0 4px}
.refs3 a{color:var(--accent);text-decoration:none}
.symgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:3px 20px;font-size:11.3px;line-height:1.36;color:var(--ink2)}
#help{display:none!important}
.p3refs{margin-top:auto;border-top:none;box-shadow:0 -1px 0 var(--rule)}
.p3refs .pgrefs li{margin-bottom:0;line-height:10px}
.p3refs .p3rh{line-height:12px}
"""

def render(font_dir=None):
    parts = ['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
             '<title>Learning across tasks</title>', '<style>', bd.font_css(font_dir), bd.CSS, EXTRA_CSS, '</style></head><body>',
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
bd.FX["per task"] = [("op", r"v_n(m^{\prime},p)="), ("S", r"\dfrac{C_{\mathrm{learn}}}{n}"), ("op", "+"),
                     ("C", r"\dfrac{C_{m^{\prime}}(p)}{R_{m^{\prime}}(p)}"), ("op", r"\quad\mathrm{s.t.}\ "), ("R", r"R_{m^{\prime}}(p)\geq R_0")]
DN, UP, KEEP = bd.DN, bd.UP, bd.KEEP
def citet(*keys):
    """Narrative citation: Surname et al. (Year) and Surname et al. (Year)."""
    forms = [cite(k)[1:-1] for k in keys]
    return " and ".join(re.sub(r", (\d{4}[a-z]?)$", r" (\1)", f) for f in forms)

def ul(items):
    return '<ul class="tb">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

def fx(marks, legend=True):
    return bd.fx(("per task", marks), legend=legend)

C_EXEC, C_LEARN, QQ = tex(r"C_{m^{\prime}}(p)", 13), tex(r"C_{\mathrm{learn}}", 13), tex(r"R_{m^{\prime}}(p)\geq R_0", 13)

# Row indices in slides/part3-data/rows.json (= the §6 table of the literature document, in order)
R = dict(ace=13, awm=14, axis=98, sica=67, wma=73, draft=44, mobilegpt=35, walt=81, harnessfix=84, growing=88,
         echopath=90, webcoach=31, hajimiri=94, reasoningbank=32, clawtrace=95, agentdevel=69, skillweaver=36,
         actionengine=80, speedrunner=82, metis=19, gptswarm=9, openskill=50, unbrowse=91, appworld=76)
def c(*names):
    return cite(*[R[n] for n in names])

# =====================================================================
# Cover
# =====================================================================
slide("s00", "Learning across tasks", kind="title", cover=True, body="""
<div class="cover cover-deck"><div class="cover-one">
  <h1 class="cover-title">Learning to do repeated web tasks faster and more cheaply</h1>
  <p class="cover-sub">An agent runs the same workflow again and again with new inputs. What it learns is kept outside the model, so that each later task takes less time and money without lowering the quality of the result.</p>
  <p class="cover-sub2">I · The problem (pages 1–3) · II · How far existing work has got (pages 4–9) · III · Our plan follows after discussion.</p>
  <p class="cover-date">October 2026</p>
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
     tex("v", 11) + " (the source’s cost-of-pass): expected cost per success, retrying until the task succeeds<br><br>" + tex(r"T_{\mathrm{success}}", 11) + ": expected time per success",
     ul([tex("m", 11) + ": the agent, a model plus the program around it (the harness); “m” for model, as in the source",
         tex("p", 11) + ": one task; “p” for problem, as in the source",
         tex("C_m(p)", 11) + ": expected cost (C) of one attempt, in dollars",
         tex("R_m(p)", 11) + ": success rate (R), the chance that one attempt succeeds",
         tex(r"T_{\mathrm{attempt}}", 11) + ": time (T) of one attempt, in seconds"]),
     "Dollars: from " + citet("ref-p1-cop") + ". Seconds: ours, adapted from the same paper."],
    [tex(r"v_n(m^{\prime},p)=\dfrac{C_{\mathrm{learn}}}{n}+\dfrac{C_{m^{\prime}}(p)}{R_{m^{\prime}}(p)}", 13),
     tex("v_n", 11) + ": expected cost per task after learning, learning cost included",
     ul([tex(r"m^{\prime}", 11) + ": the same agent after learning, model unchanged, harness changed",
         tex(r"C_{\mathrm{learn}}", 11) + ": cost of learning (exploring, proposing and checking changes, keeping them up to date), each counted once",
         tex("n", 11) + ": number of tasks the learned agent serves"]),
     "Ours, adapted from " + citet("ref-ai-agents-that-matter", 46) + "."],
    [tex(r"\min\ \left(T_{\mathrm{success}}(m^{\prime},p),\ v_n(m^{\prime},p)\right)", 12) + "<br>" + tex(r"\mathrm{s.t.}\quad R_{m^{\prime}}(p)\geq R_0", 12),
     "The goal: lower time and money per task, success held",
     ul([tex("R_0", 11) + ": lowest required success rate, fixed in advance, measured on tasks not used for learning",
         tex(r"T_{\mathrm{learn}}", 11) + ": time spent learning offline, reported beside " + tex(r"T_{\mathrm{success}}", 11) + ", not spread over tasks"]),
     "Ours."],
    [tex(r"n^{*}=\dfrac{C_{\mathrm{learn}}}{v(m,p)-v(m^{\prime},p)}", 13),
     tex("n^{*}", 11) + ": break-even, the number of tasks after which " + tex(r"v_n(m^{\prime},p)", 11) + " falls below " + tex("v(m,p)", 11),
     "—",
     "Ours, from row 2; " + citet("ref-ai-agents-that-matter") + " report a break-even point."],
  ], ["29%", "21%", "33%", "17%"], cls="tbl p3t")}
<div class="figcap" style="margin-top:6px">Each source’s original formula, and what we changed and why: <a href="#a00">Appendix A0 ↗</a></div>""",
  chip=("#a00", "Appendix A0"))

slide("s02", "Example: a web agent that files expense reports",
  crumb="term: C_m′(p) — the part of a run that is repeated discovery or rework",
  callout="<p><b>Our running example: a web agent files expense reports, and each task is a new report in the same expense system. Some of its steps are needed to file the report; others rediscover the form or redo work after an error. Only the second kind can be learned away.</b></p>",
  body=f"""
<div class="lbl">One run: a hotel expense</div>
<div class="flow">
 <div class="stp"><span class="n">1</span>Open a new expense report</div><div class="arr">→</div>
 <div class="stp"><span class="n">2</span>Choose the expense type: Hotel</div><div class="arr">→</div>
 <div class="stp"><span class="n">3</span>Upload the receipt</div><div class="arr">→</div>
 <div class="stp"><span class="n">4</span>Submit</div><div class="arr">→</div>
 <div class="stp rw"><span class="n">5</span>Error: check-in and check-out dates are required</div><div class="arr">→</div>
 <div class="stp rw"><span class="n">6</span>Find the date fields and fill them</div><div class="arr">→</div>
 <div class="stp rw"><span class="n">7</span>Submit again</div><div class="arr">→</div>
 <div class="stp key"><span class="n">8</span>Check the saved report</div>
</div>
<div class="path"><span class="pl">WITH A LEARNED RULE</span><span class="s">1</span>→<span class="s">2</span>→<span class="s">3</span>→<span class="s">fill the dates</span>→<span class="s">4</span>→<span class="s">8</span><span class="illus" style="margin:0 0 0 10px">orange: rework that a learned rule removes</span></div>
<div class="lbl" style="margin-top:22px">Definitions</div>
<div class="defs4">
 <div><b>Task</b>A goal, its input data and a starting state, with a check of the result that the agent does not control.</div>
 <div><b>Environment</b>The website’s interface, its rules and the actions it permits; it stays the same while records change.</div>
 <div><b>Run record</b>What one execution observed and did, the feedback it got, its outcome, its time and its cost.</div>
 <div><b>Learning</b>An update that outlives a task and changes something outside the model: a prompt, a memory, a skill or tool, or control code.</div>
</div>
<div class="lbl" style="margin-top:20px">Scope</div><div style="font-size:12.5px;line-height:1.45;color:var(--ink2)">The same problem arises for any agent that repeats a workflow in one software environment: a website, a desktop application, a mobile app or a set of tool APIs. Our first experiments use web agents.</div>
<div class="illus" style="margin-top:12px">Illustrative example; the form rule is invented.</div>""")

slide("s03", "Five difficulties, each tied to a term of the formula",
  crumb="difficulties from our problem framing · each card names the term it sits in",
  callout="<p><b>Five difficulties separate a faster agent from a proven one.</b></p>",
  body=f"""
<div class="rows5 big" style="flex:1">
  {card("1 · THE WHOLE RUN · " + C_EXEC, "Fewer actions can still mean a longer task, so judge by end-to-end time and money",
        ["Actions 10.7 → 10.2 per task, yet 215 → 395 s per task — WebCoach, 643 live WebVoyager tasks, Skywork-38B with a Qwen3-8B coach; the time includes the coach’s inference " + c("webcoach")], "")}
  {card("2 · NEEDED OR REMOVABLE · " + C_EXEC, "What can be skipped is known only after a run has succeeded once, and that run is paid for",
        ["Replay cut the median task time 315.7 → 127.5 s, but only on the 159 tasks whose first pass had succeeded and been stored; building each took a median of about 572k tokens and 4.5 min — EchoPath, OSWorld-Verified " + c("echopath")], "")}
  {card("3 · FROM FAILURE TO FIX · " + C_LEARN, "Seeing a failure does not say what to change; finding and checking a fix costs model calls",
        ["Completion +6.3 to +18.4 points after automatic repairs, mean of three runs, GPT-5 mini on four benchmarks; the repairs on AppWorld used 37.2 million tokens offline — HarnessFix " + c("harnessfix")], "")}
  {card("4 · TRANSFER AND READING · " + C_EXEC, "Learned material has to help on new tasks and be cheap to read",
        ["With token budgets roughly matched, the plain agent without skills or memory did best: 44.78% success at 73.6K tokens per task — WebArena, four domains, Gemini 3 Flash, three runs " + c("hajimiri")], "")}
  {card("5 · PROVING THE SAVING · " + C_LEARN, "Showing that a change saves money costs money itself",
        ["$1.91 → $1.70 and 130.2 → 114.5 s per task on four benchmarks, for a whole run of about $7,000: n* ≈ 33,000 tasks at that saving per attempt (calc.) — SICA " + c("sica")], "")}
</div>""")

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

slide("s05", f"Direction 1 · Learning from the agent’s own runs: {n1} works in four classes",
  crumb="counts: one row per work in our literature table, a work in two classes counted in both · yes / partly: initial judgment from table cells (calc.), Appendix A1",
  callout=f"<p><b>Of {n1} works that change what sits outside the model, {a1[0]} measured the seconds or dollars of running tasks, {b1[0]} what learning cost, and {d1[0]} tested on unseen tasks.</b></p>",
  body=fx({"C": DN, "S": UP, "R": KEEP}, legend=False) + class_table([
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

slide("s06", "How a run record becomes a change, and what the change costs",
  crumb="direction 1 · C_m′(p) ↓ after the change · C_learn ↑ at three points: diagnosis, candidates, re-tests",
  callout="<p><b>Every step after reading the run records costs model calls, and these costs are rarely reported next to the savings.</b></p>",
  body=f"""
{fx({"C": DN, "S": UP, "R": KEEP})}
<div class="flow" style="margin:10px 0 4px">
 <div class="stp key"><span class="n">1 · INPUT</span>Run records, failed and successful, with their time and cost</div><div class="arr">→</div>
 <div class="stp"><span class="n">2 · DIAGNOSE</span>Find failures and waste; locate the step and the code responsible<span class="tagc">costs: diagnosis calls</span></div><div class="arr">→</div>
 <div class="stp"><span class="n">3 · PROPOSE</span>A change to one of: prompt · memory · skill or tool · control code<span class="tagc">costs: candidate generation</span></div><div class="arr">→</div>
 <div class="stp"><span class="n">4 · RE-TEST</span>On tasks not used to find the change; old tasks must still pass<span class="tagc">costs: re-runs of tasks</span></div><div class="arr">→</div>
 <div class="stp key"><span class="n">5 · DECIDE</span>Keep the change, or roll it back</div>
</div>
<div class="two" style="margin-top:12px">
  {card("IT WORKS", "Changes can be found and made automatically, with gains on the final tasks",
        ["Highest success in five of six settings and 76.0–91.8% fewer model calls at deployment — Growing Harness, BrowseComp-Plus and WebArena-Verified, three models, 50 final tasks per setting, three runs " + c("growing")], "")}
  {card("THE BILL IS PARTIAL · " + C_LEARN, "Savings at deployment are usually reported without the learning that produced them",
        ["97.4K vs 112.6K tokens and 11.25 vs 14.55 turns per AppWorld task once the memory is frozen; the memory manager’s own calls are not included — Metis " + c("metis")], "")}
</div>""",
  chip=("#a05", "Appendix A5"))

slide("s07", f"Direction 2 · Learning the environment: {n2} works keep four kinds of knowledge",
  crumb="counts: one row per work in our literature table, a work in two classes counted in both · yes / partly: initial judgment from table cells (calc.), Appendix A1",
  callout=f"<p><b>Of {n2} works that keep knowledge about the environment, {a2[0]} measured the seconds or dollars of running tasks, {b2[0]} what exploring cost, and {d2[0]} tested on unseen tasks.</b></p>",
  body=fx({"C": DN, "S": UP, "R": KEEP}, legend=False) + class_table([
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
  callout="<p><b>The agent probes the form, writes down what it found together with where it applies and the evidence for it, and reads that note on the next task, so the error-and-retry loop of page 2 does not happen.</b></p>",
  body=f"""
<div class="panel3">
 <div><div class="lbl">1 · Explore the form</div>Change the expense type from Meal to Hotel. Two new required fields appear: check-in and check-out date. Submitting without them returns an error.</div>
 <div><div class="lbl">2 · Keep a checked rule</div><div class="guide"><b>site-guide.md</b><br>scope: new expense form<br>IF type = Hotel → check-in and check-out dates required<br>evidence: 2 probes, 1 error message<br>re-check: when the form changes</div></div>
 <div><div class="lbl">3 · Use it on the next task</div>New hotel expense + the live page + the saved note → fill every required field → submit once → check the saved report.</div>
</div>
<div class="path"><span class="pl">WITHOUT THE NOTE</span><span class="s">submit</span>→<span class="s rw">error</span>→<span class="s rw">fill the dates</span>→<span class="s rw">submit again</span>→<span class="s">check</span></div>
<div class="path"><span class="pl">WITH THE NOTE</span><span class="s">fill the dates</span>→<span class="s">submit</span>→<span class="s">check</span><span class="illus" style="margin:0 0 0 10px">illustrative paths, not measured</span></div>
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

slide("a00", "A0 · Page 1’s formulas: the original, ours, and why we changed it", label="A0", kind="appendix", chip=("#back", "← back"),
  body=table(["our formula", "original formula", "original definitions", "what we changed, and why"], [
    [ours(tex(r"v(m,p)=\dfrac{C_m(p)}{R_m(p)}", 12), "from the paper"),
     orig(tex(r"v(m,p)=\dfrac{C_m(p)}{R_m(p)}", 12) + " (Eq. 2)", cite("ref-p1-cop")),
     ul([tex("m", 10) + ": a model; " + tex("p", 10) + ": a problem",
         tex("C_m(p)", 10) + ": expected dollars of one attempt, input and output tokens times their prices (Eq. 13)",
         tex("R_m(p)", 10) + ": chance that one attempt is correct; " + tex(r"1/R_m(p)", 10) + " attempts are expected until the first correct one, attempts independent"]),
     ul([tex("m", 10) + " becomes the agent: the model plus its harness",
         "why: learning changes the harness, not the model"])],
    [ours(tex(r"T_{\mathrm{success}}(m,p)=\dfrac{\mathbb{E}[T_{\mathrm{attempt}}]}{R_m(p)}", 12), "ours, adapted"),
     orig("no time formula", cite("ref-p1-cop")),
     ul(["units per attempt other than dollars, such as time or latency, may matter more (App. D.1)"]),
     ul(["the same form, in seconds", "why: time and money are reported side by side", "assumes attempts run one after another"])],
    [ours(tex(r"v_n(m^{\prime},p)=\dfrac{C_{\mathrm{learn}}}{n}+\dfrac{C_{m^{\prime}}(p)}{R_{m^{\prime}}(p)}", 12), "ours, adapted"),
     orig("total cost = fixed cost + variable cost (in words)", cite("ref-ai-agents-that-matter")) + "<br>" + orig(tex(r"O(nc+C)", 11) + " against " + tex(r"O(nC)", 11) + " (Table 2)", cite(46)),
     ul(["fixed cost: paid once, to optimise the agent’s design (prompt, hyperparameters)",
         "variable cost: paid on every run, set by its input and output tokens",
         tex("n", 10) + ": task instances; " + tex("C", 10) + ": one call of the large tool-making model; " + tex("c", 10) + ": one call of the small tool-using model"]),
     ul(["fixed cost ÷ " + tex("n", 10) + ": a cost per task",
         "variable part per success (÷ " + tex("R", 10) + "), so failed attempts are paid for",
         "fixed cost widened to exploring, proposing, checking and upkeep — why: our learning does all of these"])],
    [ours(tex(r"\min\ \left(T_{\mathrm{success}}(m^{\prime},p),\ v_n(m^{\prime},p)\right)", 11) + "<br>" + tex(r"\mathrm{s.t.}\ R_{m^{\prime}}(p)\geq R_0", 11), "ours"),
     orig(tex(r"V_p(\mathcal{M})=\min_{m\in\mathcal{M}}v(m,p)", 12) + " (Eq. 3)", cite("ref-p1-cop")) + "<br>" + orig("accuracy and cost optimised jointly (in words)", cite("ref-ai-agents-that-matter")),
     ul([tex(r"\mathcal{M}", 10) + ": the available models",
         tex(r"V_p(\mathcal{M})", 10) + ": the lowest cost per success on " + tex("p", 10) + " among them"]),
     ul(["one number becomes a pair, seconds and dollars, lowered together — why: no fixed exchange rate between them",
         "learning cost included",
         "success floor " + tex("R_0", 10) + ", fixed in advance — why: an agent must not look cheaper by succeeding less"])],
    [ours(tex(r"n^{*}=\dfrac{C_{\mathrm{learn}}}{v(m,p)-v(m^{\prime},p)}", 12), "ours"),
     orig("no formula (in words)", cite("ref-ai-agents-that-matter")),
     ul(["the jointly optimised agent is cheaper in total than the default one after about 1,350 HotPotQA tasks"]),
     ul(["written as a formula by setting " + tex(r"v_n(m^{\prime},p)=v(m,p)", 10) + " — why: computable from measured costs",
         "assumes the saving per task stays the same"])],
  ], ["21%", "21%", "30%", "28%"], cls="tbl p3a p3t"))

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
def apx_pages(aid, title, ids):
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
        slide(sid, f"{aid.upper()} · {title}" + (f" ({k + 1}/{len(pages)})" if len(pages) > 1 else ""), label=f"{aid.upper()} · {k + 1}/{len(pages)}",
              kind="appendix", chip=("#back", "← back"),
              body=table(["work", "venue", "what it changes", "where it was tested", "effect, with conditions", "time, money, learning cost", "marks"],
                         [arow(i) for i in p], ["11%", "8%", "15%", "17%", "21%", "21%", "7%"], cls="tbl p3a") + f'<div class="figcap">{LEG}</div>')

for cat, title, aid in CLASS[:8]:
    apx_pages(aid, title, ids_of(cat) + (ids_of("2E判分环境") if aid == "a06" else []))
CLOSEST = [80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 14, 32, 35, 36, 19, 42, 68, 28]
apx_pages("a10", "The works closest to ours", [i for i in CLOSEST if i < len(J)])

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
