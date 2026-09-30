#!/usr/bin/env python3
"""Check that every evidence item of a record is locked to the saved full text.

usage: check_anchors.py <record.json | directory of records> [--json]

For each evidence item the record must give `anchor` (a verbatim string copied from the saved text)
and the record must give `txt_path` (the text saved by fetch_source.py). The check:
  ANCHOR   the anchor occurs in the saved text (whitespace, dashes and quote marks normalized)
  FIGURE   every number in `figure` occurs within 3 lines of the anchor
Verdicts per item: PASS, NO_ANCHOR (field empty), ANCHOR_MISSING, FIGURE_NOT_NEAR, NO_TEXT (txt_path missing).
Exit status 0 if all items pass, 1 otherwise.
"""
import json
import os
import re
import sys
import unicodedata

TR = {0x2010: "-", 0x2011: "-", 0x2012: "-", 0x2013: "-", 0x2014: "-", 0x2212: "-", 0x2018: "'", 0x2019: "'",
      0x201C: '"', 0x201D: '"', 0x00A0: " ", 0x2009: " ", 0x202F: " ", 0x2006: " ", 0x00D7: "x"}


def norm(s):
    s = unicodedata.normalize("NFKC", s).translate(TR)
    return re.sub(r"\s+", " ", s).strip()


def load_text(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = f.read().split("\n")
    parts, starts, pos = [], [], 0
    for i, ln in enumerate(lines, 1):
        n = norm(ln)
        if not n:
            continue
        starts.append((pos, i))
        parts.append(n)
        pos += len(n) + 1
    return " ".join(parts), starts, lines


def line_of(starts, off):
    lo, hi = 0, len(starts) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if starts[mid][0] <= off:
            lo = mid
        else:
            hi = mid - 1
    return starts[lo][1]


def numbers(s):
    out = []
    for t in re.findall(r"\d[\d,]*\.?\d*", s or ""):
        t = t.rstrip(".,")
        if t:
            out.append(t)
    return out


def check_record(path):
    with open(path, encoding="utf-8") as f:
        rec = json.load(f)
    items = rec.get("evidence") or []
    txt = rec.get("txt_path") or ""
    rows = []
    if not items:
        return rec, rows
    if not txt or not os.path.exists(txt):
        for k, it in enumerate(items):
            rows.append((k, "NO_TEXT", 0, it.get("figure", ""), it.get("anchor", "")))
        return rec, rows
    text, starts, lines = load_text(txt)
    for k, it in enumerate(items):
        a = norm(it.get("anchor") or "")
        if not a:
            rows.append((k, "NO_ANCHOR", 0, it.get("figure", ""), ""))
            continue
        off = text.find(a)
        if off < 0:
            rows.append((k, "ANCHOR_MISSING", 0, it.get("figure", ""), a))
            continue
        ln = line_of(starts, off)
        ln_end = line_of(starts, off + len(a))
        near = norm(" ".join(lines[max(0, ln - 4): ln_end + 3]))
        near_plain = near.replace(",", "")
        miss = [n for n in numbers(it.get("figure")) if n not in near and n.replace(",", "") not in near_plain]
        rows.append((k, "PASS" if not miss else "FIGURE_NOT_NEAR", ln, it.get("figure", ""), a if not miss else a + "  [missing: " + ", ".join(miss) + "]"))
    return rec, rows


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    target = args[0]
    paths = [target] if os.path.isfile(target) else sorted(
        os.path.join(target, f) for f in os.listdir(target) if f.endswith(".json"))
    summary, bad = [], 0
    for p in paths:
        try:
            rec, rows = check_record(p)
        except Exception as e:  # noqa
            summary.append({"record": p, "error": repr(e)})
            bad += 1
            continue
        n_pass = sum(1 for r in rows if r[1] == "PASS")
        summary.append({"record": os.path.basename(p), "title": rec.get("title", ""), "fulltext": rec.get("fulltext"),
                        "items": len(rows), "pass": n_pass,
                        "fail": [{"item": r[0], "verdict": r[1], "figure": r[3], "anchor": r[4]} for r in rows if r[1] != "PASS"],
                        "lines": [r[2] for r in rows]})
        bad += len(rows) - n_pass
    if "--json" in sys.argv:
        print(json.dumps(summary, ensure_ascii=False, indent=1))
    else:
        for s in summary:
            if "error" in s:
                print("ERROR  %s  %s" % (s["record"], s["error"]))
                continue
            print("%-8s %2d/%-2d  %s" % ("OK" if s["pass"] == s["items"] else "FAIL", s["pass"], s["items"], s["record"]))
            for f in s["fail"]:
                print("         item %d  %s  figure=%r  anchor=%r" % (f["item"], f["verdict"], f["figure"], f["anchor"]))
    sys.exit(0 if bad == 0 else 1)


if __name__ == "__main__":
    main()
