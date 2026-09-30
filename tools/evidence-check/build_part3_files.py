#!/usr/bin/env python3
"""Build the repository files of the Part 3 research from the verified store.

usage: build_part3_files.py <scratch_dir> <out_dir> --e-start N --d-start N --date YYYY-MM-DD --tags tags.json
                            --doc <name>=<draft.md> [--doc ...] [--part <doc>:<KEY>=<file> ...]
                            [--refs-a <codex report.md>] [--per-ref <review result.json>] [--dx <draft.md> <audit.json>]

Documents cite evidence as [w003#9] (record id, item index) or through tags @@NAME@@ that tags.json maps to lists of
such references. Every cited item must be in check/consolidated-*.json: it passed the mechanical anchor check and the
independent audit. E-IDs are given in order of first appearance over the documents, in the order of the --doc arguments.

Writes  <out>/<name>.md                 each document with E-IDs, its evidence index and its reference list
        <out>/evidence-ledger.md        all new E-entries (five fields each), D-entries from the audited draft, works tables
        <out>/records-<batch>.md        every kept item of every eligible work, one file per batch
        <out>/e-map.json                item reference -> E-ID
Nothing is taken from memory: all text about sources comes from the store.
"""
import collections
import glob
import json
import os
import re
import sys

REF = re.compile(r"[nwghx]\d{3}#\d+")
REFGROUP = re.compile(r"\[((?:[nwghx]\d{3}#\d+)(?:\s*[,;]\s*[nwghx]\d{3}#\d+)*)\]")
TAG = re.compile(r"@@([A-Za-z0-9_-]+)@@")
RESERVED = ("TABLE_PER_REF", "E_TABLE", "REFERENCES", "D_ENTRIES", "E_PATCHES", "STILL_OPEN", "E_RANGE")
CLASS_ZH = {"top-venue": "顶刊顶会", "leading-company-official": "头部公司官方材料", "institutional-supplement": "合格机构补充",
            "hold": "暂缓", "exclude": "排除"}
CLASS_EN = {"top-venue": "top venue", "leading-company-official": "leading-company official material",
            "institutional-supplement": "institutional supplement", "hold": "held", "exclude": "excluded"}
BATCH = collections.OrderedDict([
    ("w", "first sweep (11 lanes)"), ("n", "second sweep (6 lanes from Edwin's clarifications)"),
    ("g", "gap sweep (ten gaps named by the critics, and promoted works)"),
    ("h", "close works named by the Codex survey and the deck that the store lacked"),
    ("x", "supplementary items for the 23 works cited by the Codex plan report")])


def cell(s, n=None):
    s = re.sub(r"\s+", " ", str(s if s is not None else "")).replace("|", "/").strip()
    return s if n is None or len(s) <= n else s[: n - 1].rstrip() + "…"


def first_url(w):
    return cell((w.get("source_url") or w.get("abs_url") or "").split(" ")[0])


def main():
    a = sys.argv
    scratch, out = a[1], a[2]
    e_next = int(a[a.index("--e-start") + 1])
    d_next = int(a[a.index("--d-start") + 1])
    date = a[a.index("--date") + 1]
    tags = json.load(open(a[a.index("--tags") + 1], encoding="utf-8"))
    alias = tags.get("ALIAS", {})
    docs, parts = collections.OrderedDict(), collections.defaultdict(dict)
    for i, x in enumerate(a):
        if x == "--doc":
            k, v = a[i + 1].split("=", 1)
            docs[k] = open(v, encoding="utf-8").read()
        if x == "--part":
            dk, rest = a[i + 1].split(":", 1)
            k, v = rest.split("=", 1)
            parts[dk][k] = open(v, encoding="utf-8").read().strip()
    os.makedirs(out, exist_ok=True)

    works, allrecs = {}, []
    for p in sorted(glob.glob(os.path.join(scratch, "check", "consolidated-*.json"))):
        for w in json.load(open(p, encoding="utf-8"))["works"]:
            w["short"] = w["id"].split("-")[0]
            allrecs.append(w)
            if w.get("used"):
                works[w["short"]] = w
    elig_raw = json.load(open(os.path.join(scratch, "check", "eligibility-by-record.json"), encoding="utf-8"))

    def elig(sid):
        return elig_raw.get(alias.get(sid, sid)) or elig_raw.get(sid) or {}

    def ok(sid):
        return elig(sid).get("decision") in ("top-venue", "leading-company-official", "institutional-supplement")

    def label_of(sid, e):
        lab = e.get("label") or "primary"
        d = elig(sid).get("decision")
        if d == "top-venue":
            kind = "published: " + cell(elig(sid).get("formal_venue"), 90)
        elif d == "leading-company-official":
            kind = "vendor"
        else:
            kind = "preprint"
        return ("Secondary" if lab == "secondary" else "Primary") + ", " + kind

    # 1. resolve tags, collect references in order
    problems, unresolved = [], set()

    def resolve(text, dk):
        for k in ("D_ENTRIES", "E_PATCHES", "STILL_OPEN"):
            if k in parts[dk]:
                text = text.replace("@@%s@@" % k, parts[dk][k])

        def tagsub(m):
            k = m.group(1)
            if k in RESERVED:
                return m.group(0)
            v = tags.get(k)
            if v is None:
                unresolved.add(k)
                return m.group(0)
            if isinstance(v, str):
                return v
            return "".join("[%s]" % r for r in v)
        return TAG.sub(tagsub, text)

    order, per_doc = [], collections.OrderedDict()
    for dk in docs:
        docs[dk] = resolve(docs[dk], dk)
        per_doc[dk] = []
        for r in REF.findall(docs[dk]):
            if r not in per_doc[dk]:
                per_doc[dk].append(r)
            if r not in order:
                order.append(r)

    # 2. E-IDs and ledger rows
    emap, erow, ledger_rows = {}, {}, []
    for r in order:
        sid, k = r.split("#")
        w = works.get(sid)
        e = next((x for x in (w or {}).get("evidence", []) if x["index"] == int(k)), None)
        if not e:
            problems.append("item not in the audited store: " + r)
            continue
        if not ok(sid):
            problems.append("source not eligible (%s): %s" % (elig(sid).get("decision"), r))
            continue
        emap[r] = "E%d" % e_next
        e_next += 1
        fig = cell(e.get("figure"), 220)
        row = "| %s | **%s**%s | %s | %s, %s; %s; line %s of the saved text | %s | %s | P3 record %s | %s |" % (
            emap[r], cell(e.get("claim")), (" (" + fig + ")") if fig and fig not in ("-", "—") and not fig.startswith("(corrected") else "",
            cell(e.get("measurement_definition")) or "statement, no measurement", first_url(w), cell(w.get("version_read"), 60),
            cell(e.get("location"), 160), e.get("line_checked") or e.get("line") or "",
            cell(e.get("date") or w.get("date_version_read") or w.get("date_v1"), 30), label_of(sid, e), r,
            "audited: supported" if e.get("audit") == "supported" else "audited: corrected by the auditor, corrected wording shown")
        erow[r] = (w, e)
        ledger_rows.append(row)
    e_range = ""
    if emap:
        ids = sorted(int(v[1:]) for v in emap.values())
        e_range = "E%d–E%d" % (ids[0], ids[-1])

    def sub(m):
        refs = [x.strip() for x in re.split(r"[,;]", m.group(1))]
        return "[" + ", ".join(emap.get(x, x) for x in refs) + "]"

    # 3. reference entries
    def ref_entry(sid, lang):
        el, w = elig(sid), works.get(sid) or next((x for x in allrecs if x["short"] == sid), {})
        authors = el.get("authors_full") or w.get("authors") or ""
        if lang == "zh":
            venue = el.get("formal_venue") or "arXiv 预印本，未核到正式发表"
            if el.get("venue_claim_unverified"):
                venue += "（作者自述：" + cell(el["venue_claim_unverified"], 140) + "；未在官方来源确认）"
            return ["**[%s] %s (%s).** *%s*. %s。[正式引用](%s)。" % (sid, cell(authors), el.get("year") or "", cell(el.get("title") or w.get("title")), cell(venue, 300),
                                                                  el.get("formal_citation_url") or w.get("abs_url") or first_url(w)), "",
                    "实际核读版本：[%s](%s)。来源等级：%s。机构：%s" % (cell(w.get("version_read"), 60), (el.get("version_read_url") or first_url(w)).split(" ")[0],
                                                          CLASS_ZH.get(el.get("decision"), "未判定"), cell(el.get("institutions") or w.get("affiliations"), 700)), ""]
        venue = el.get("formal_venue") or "arXiv preprint; no formal publication confirmed"
        if el.get("venue_claim_unverified"):
            venue += " (reported by the authors: " + cell(el["venue_claim_unverified"], 140) + "; not confirmed at an official source)"
        return ["**[%s] %s (%s).** *%s*. %s. [Formal citation](%s)." % (sid, cell(authors), el.get("year") or "", cell(el.get("title") or w.get("title")), cell(venue, 300),
                                                                       el.get("formal_citation_url") or w.get("abs_url") or first_url(w)), "",
                "Version read: [%s](%s). Source class: %s. Institutions: %s" % (cell(w.get("version_read"), 60), (el.get("version_read_url") or first_url(w)).split(" ")[0],
                                                                                CLASS_EN.get(el.get("decision"), "not decided"), cell(el.get("institutions") or w.get("affiliations"), 700)), ""]

    _ref_entry = ref_entry

    def ref_entry(sid, lang):  # noqa
        out_ = _ref_entry(sid, lang)
        extra = (tags.get("REF_EXTRA") or {}).get(sid)
        if extra and lang == "zh":
            out_[2] = out_[2] + " " + extra
        elif extra:
            out_[2] = out_[2] + " (Further records of the same work exist; see the Chinese documents.)"
        return out_

    def canon_list(refs):
        seen = []
        for r in refs:
            c = alias.get(r.split("#")[0], r.split("#")[0])
            if r in emap and c not in seen:
                seen.append(c)
        return seen

    rep_refs = []
    if "--refs-a" in a:
        rep = open(a[a.index("--refs-a") + 1], encoding="utf-8").read().split("\n")
        start = next(i for i, l in enumerate(rep) if l.startswith("[1] "))
        notes, cur = tags.get("REF_NOTES", {}), None
        for l in rep[start:]:
            m = re.match(r"\[(\d+)\] ", l)
            if m:
                cur = m.group(1)
            rep_refs.append(l)
            if l.startswith("实际核读版本") and cur in notes:
                rep_refs += ["", "本次审阅补充：" + notes[cur]]

    # 4. documents
    for dk, text in docs.items():
        text = REFGROUP.sub(sub, text)
        text = re.sub(r"\](\[E\d+)", r"] \1", text)
        idx = ["| E 编号 | 核对库条目 | 文献 | 陈述（完整的五项信息见证据台账） |", "|---|---|---|---|"]
        for r in sorted([x for x in per_doc[dk] if x in emap], key=lambda x: int(emap[x][1:])):
            if r in emap:
                w, e = erow[r]
                c = alias.get(w["short"], w["short"])
                idx.append("| %s | %s | [%s] %s | %s |" % (emap[r], r, c, cell(elig(w["short"]).get("title") or w.get("title"), 70), cell(e.get("claim"), 400)))
        text = text.replace("@@E_TABLE@@", "\n".join(idx))
        text = text.replace("@@E_RANGE@@", e_range)
        if "--per-ref" in a and "@@TABLE_PER_REF@@" in text:
            rr = json.load(open(a[a.index("--per-ref") + 1], encoding="utf-8"))
            short = tags.get("REF_SHORT", {})
            L = ["| 报告文献 | 工作 | 本次所读版本 | 发表信息 | 成立 | 需加条件 | 不成立 |", "|---|---|---|---|---|---|---|"]
            for ref in rr["references"]:
                c = collections.Counter(x["verdict"] for x in ref["claims"])
                s = short.get(str(ref["ref"]), {})
                L.append("| [%d] | %s | %s | %s | %d | %d | %d |" % (ref["ref"], s.get("name", cell(ref["work"], 60)), s.get("version", ""), s.get("venue", ""),
                                                                 c.get("supported", 0), c.get("supported-with-caveat", 0), c.get("not-supported", 0)))
            text = text.replace("@@TABLE_PER_REF@@", "\n".join(L))
        R = []
        in_a = set(tags.get("IN_A", [])) if (dk == "review" and rep_refs) else set()
        if dk == "review" and rep_refs:
            R += ["### A. Codex 报告引用的 23 篇（沿用报告的编号 [1]–[23]）", "",
                  "以下条目照录自 `notes/2026-09-29-part3-research-plan-report-zh.md` 的参考文献。本次审阅逐条核对了作者、题目、发表信息和所读版本：正式发表的条目在会议官方页面上确认，预印本条目确认 arXiv 记录中没有发表信息。", ""]
            R += rep_refs + ["", "### B. 本审阅补充引用的文献（按核对库记录号）", ""]
        R += ["每条给出正式引用和实际核读的版本。来源等级按 Edwin 2026-09-29 的来源规则（D313）判定：顶刊顶会优先；其次是头部 AI 公司的官方技术材料；知名高校和成熟研究机构的预印本作为补充。作者自述的录用不算已确认发表。方括号里是核对库的记录号。", ""]
        for c in canon_list(per_doc[dk]):
            if c in in_a:
                continue
            R += ref_entry(c, "zh")
        text = text.replace("@@REFERENCES@@", "\n".join(R))
        open(os.path.join(out, dk + ".md"), "w", encoding="utf-8").write(text)

    # 5. records files, one per batch, eligible and used works only
    n_items = 0
    for b, name in BATCH.items():
        ws = [w for w in allrecs if w["short"].startswith(b) and w.get("used") and ok(w["short"])]
        if not ws:
            continue
        L = ["# Part 3 source records: " + name, "",
             "**Date:** " + date + " · generated by `tools/evidence-check/build_part3_files.py` from the verified store; not edited by hand.", "",
             "Each work was saved as full text and read by one agent, which locked every item to a line of the saved text with a short verbatim anchor. A script checked that each anchor occurs in the saved text and that the numbers of the item stand within three lines of it. A second agent, which did not write the record, then tried to refute each item against the text. Items shown here passed both checks. Where the auditor corrected an item, the corrected wording is shown and the Audit column says so. The verbatim anchors and the saved texts are kept outside the repository; this file gives the location of every item instead. Only works that are eligible under the source rule of 2026-09-29 (D313) are listed; the others are in the evidence ledger, section 1b.", "",
             "Columns: # = item index (the reference is <record id>#<index>); Field = what the item is about; Line = line in the saved text of the version read. Full references: evidence ledger, References.", ""]
        for w in ws:
            el = elig(w["short"])
            L += ["## %s — %s" % (w["short"], cell(el.get("title") or w.get("title"))), "",
                  "- Source: %s · version read: %s · v1: %s" % (first_url(w), cell(w.get("version_read"), 160), cell(w.get("date_v1"), 40)),
                  "- Source class: %s%s" % (CLASS_EN.get(el.get("decision")), (" · formal venue (confirmed at the official source): " + cell(el.get("formal_venue"), 200)) if el.get("formal_venue") else " · no formal publication confirmed"),
                  "- Audit: %s; %d items kept, %d dropped" % (w.get("audit_overall"), len(w.get("evidence") or []), len(w.get("dropped") or [])),
                  "", "| # | Field | Claim | Figure | Measurement definition | Location | Line | Label | Audit |", "|---|---|---|---|---|---|---|---|---|"]
            for e in w.get("evidence") or []:
                n_items += 1
                fig = cell(e.get("figure"), 200)
                L.append("| %d | %s | %s | %s | %s | %s | %s | %s | %s |" % (
                    e["index"], cell(e.get("field")), cell(e.get("claim")), fig, cell(e.get("measurement_definition")),
                    cell(e.get("location"), 160), e.get("line_checked") or e.get("line") or "", cell(e.get("label")),
                    "supported" if e.get("audit") == "supported" else "corrected by the auditor"))
            L.append("")
        open(os.path.join(out, "records-%s.md" % b), "w", encoding="utf-8").write("\n".join(L))

    # 6. ledger file
    L = ["## 1 Verification table", "", "### 1a Works used (eligible under the source rule, full text read, items audited)", "",
         "| Record | Work | Source (version read) | v1 date | Source class | Formal venue confirmed at the official source | Items kept | Audit |", "|---|---|---|---|---|---|---|---|"]
    used = [w for w in allrecs if w.get("used") and ok(w["short"])]
    for w in used:
        el = elig(w["short"])
        n_fix = sum(1 for e in w.get("evidence") or [] if e.get("audit") != "supported")
        L.append("| %s | %s | %s (%s) | %s | %s | %s | %d | %d supported, %d corrected |" % (
            w["short"], cell(el.get("title") or w.get("title"), 120), first_url(w), cell(w.get("version_read"), 40), cell(w.get("date_v1"), 24),
            CLASS_EN.get(el.get("decision")), cell(el.get("formal_venue"), 120) or "—", len(w.get("evidence") or []), len(w.get("evidence") or []) - n_fix, n_fix))
    L += ["", "### 1b Works verified but not used", "",
          "A work is listed here when the source rule holds or excludes it, when its full text could not be saved, or when its record was not audited or failed the audit. Nothing in these works is used as evidence.", "",
          "| Record | Work | Source | Why not used |", "|---|---|---|---|"]
    for w in allrecs:
        if w.get("used") and ok(w["short"]):
            continue
        el = elig(w["short"])
        why = []
        if el.get("decision") in ("hold", "exclude"):
            why.append("source rule: %s. %s" % (CLASS_EN[el["decision"]], cell(el.get("reason"), 260)))
        if not w.get("used"):
            why.append(cell(w.get("reason") or "record not usable", 160))
        if not el:
            why.append("no eligibility decision")
        L.append("| %s | %s | %s | %s |" % (w["short"], cell(el.get("title") or w.get("title"), 120), first_url(w), "; ".join(why)))
    dup = json.load(open(os.path.join(scratch, "check", "duplicates-all.json"), encoding="utf-8"))
    L += ["", "### 1c Works with more than one record", "",
          "These works have more than one record: an independent second reading, a record of a second version of the same work (arXiv and camera-ready), or a record of supplementary items. Each counts as one work.", "",
          "| Work key | Records |", "|---|---|"]
    for k, v in dup.items():
        L.append("| %s | %s |" % (cell(k), ", ".join(v)))
    # parked
    parked, seen = [], set()
    for p in sorted(glob.glob(os.path.join(scratch, "check", "wf*-result.json"))):
        r = json.load(open(p, encoding="utf-8"))
        for k, why in (("parked", "relevance below 4 in its sweep"), ("parkedBudget", "prices only (budget deferred)")):
            for x in r.get(k, []) or []:
                t = (x.get("title") or "").lower()
                if t and t not in seen:
                    seen.add(t)
                    parked.append((x.get("title"), x.get("url"), why))
    L += ["", "### 1d Works found by the sweeps and not verified", "",
          "Titles and URLs as the finders reported them; none was checked, and none is used.", "",
          "| Work as reported | URL as reported | Why not verified |", "|---|---|---|"]
    for t, u, why in parked:
        L.append("| %s | %s | %s |" % (cell(t, 130), cell(u), why))
    sec1 = "\n".join(L)

    D = ["## 2 D-ledger additions", ""]
    dmap = {}
    if "--dx" in a:
        dx_draft = open(a[a.index("--dx") + 1], encoding="utf-8").read().split("\n")
        audit = {x["draft_id"]: x for x in json.load(open(a[a.index("--dx") + 2], encoding="utf-8"))["entries"]}
        D += ["The entries below were drafted from the first two batches of records and then audited one by one against both places they compare (the ledger line or the first place in the source, and the second place in the source). [A] = conflict between the ledger and a source; [B] = conflict inside a source; [C] = version or venue note. Where the auditor corrected the resolution, the corrected text is shown. Replacement wording for ledger lines is in the Resolution column.", "",
              "| ID | Work | The ledger or the source says (place A) | The source says (place B; location, version) | Resolution | Source (read %s) | Items | Audit | Source class |" % date, "|---|---|---|---|---|---|---|---|---|"]
        for l in dx_draft:
            m = re.match(r"\| (DX\d+) \|", l)
            if not m:
                continue
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            au = audit.get(m.group(1))
            if not au or au.get("verdict") not in ("confirmed", "confirmed-with-correction"):
                continue
            if au["verdict"] == "confirmed-with-correction" and au.get("corrected_resolution"):
                cells[4] = cell(au["corrected_resolution"])
            sid = (re.search(r"\(([nwg]\d{3})", cells[1]) or re.search(r"([nwg]\d{3})", cells[1]))
            sid = sid.group(1) if sid else ""
            did = "D%d" % d_next
            d_next += 1
            dmap[m.group(1)] = did
            cells[0] = did
            while len(cells) < 7:
                cells.append("")
            cells = cells[:7] + ["confirmed" if au["verdict"] == "confirmed" else "confirmed, resolution corrected by the auditor",
                                 CLASS_EN.get(elig(sid).get("decision"), "—") if sid else "—"]
            D.append("| " + " | ".join(cells) + " |")
        txt = "\n".join(D)
        for k in sorted(dmap, key=lambda x: -int(x[2:])):
            txt = re.sub(r"\b%s\b" % k, dmap[k], txt)
        D = txt.split("\n")
    sec2 = "\n".join(D)

    sec3 = "\n".join(["## 3 E-ledger patches", "", "### 3a Replacement text for existing lines", "",
                      "Replacement wording for existing ledger lines is given in the Resolution column of the [A] entries of section 2 and in section 3 of `research/2026-09-29-part3-codex-report-review.md`. The canonical dossier is not changed.", "",
                      "### 3b New E-entries", "",
                      "Entries %s. Each is one audited item of the verified store; the P3 record column gives the item, whose full record is in the records file of its batch." % e_range, "",
                      "| ID | Figure | Measurement definition and conditions | Source (URL, version, location) | Date | Label | Found by | Notes |", "|---|---|---|---|---|---|---|---|"] + ledger_rows)

    refs = ["## References", "",
            "Every work cited by an E-entry above, by record id. Each entry gives the formal citation and the version actually read. Source classes follow the rule of 2026-09-29 (D313).", ""]
    for c in canon_list(order):
        refs += ref_entry(c, "en")
    json.dump({"sec1": sec1, "sec2": sec2, "sec3": sec3, "refs": "\n".join(refs)}, open(os.path.join(out, "ledger-parts.json"), "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(emap, open(os.path.join(out, "e-map.json"), "w"), indent=1)
    json.dump(dmap, open(os.path.join(out, "d-map.json"), "w"), indent=1)
    left = {dk: sorted(set(TAG.findall(open(os.path.join(out, dk + ".md"), encoding="utf-8").read()))) for dk in docs}
    st = collections.Counter(w["short"][0] for w in used)
    print(json.dumps({"works_used": len(used), "by_batch": st, "items_in_records_files": n_items, "e_entries": len(emap), "e_range": e_range,
                      "d_entries_from_draft": len(dmap), "d_range": ("D%d–D%d" % (min(int(v[1:]) for v in dmap.values()), max(int(v[1:]) for v in dmap.values()))) if dmap else "",
                      "unresolved_tags": sorted(unresolved), "tags_left": left, "problems": problems, "parked": len(parked)}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
