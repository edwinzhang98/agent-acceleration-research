#!/usr/bin/env python3
"""Check framing records: every anchored field must have its verbatim anchor on the stated line (±2 lines) of the saved text.

usage: check_framing.py <framing_dir> [<corpus.json>]
Prints one JSON summary and writes <framing_dir>/_check.json with per-record problems.
"""
import glob
import json
import os
import re
import sys
import unicodedata

FIELDS = ("problem", "challenge", "objective", "solution_principle", "claimed_gain")


def norm(s):
    s = unicodedata.normalize("NFKC", s or "")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[‐-―−]", "-", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def main():
    d = sys.argv[1]
    out, n_rec, n_fields, n_bad = {}, 0, 0, 0
    for p in sorted(glob.glob(os.path.join(d, "*.json"))):
        if p.endswith(".audit.json") or os.path.basename(p).startswith("_"):
            continue
        try:
            r = json.load(open(p, encoding="utf-8"))
        except Exception as e:
            out[os.path.basename(p)] = ["unreadable json: %s" % e]
            n_bad += 1
            continue
        n_rec += 1
        probs = []
        tp = r.get("txt_path")
        if not tp or not os.path.exists(tp):
            probs.append("txt_path missing: %s" % tp)
            out[os.path.basename(p)] = probs
            n_bad += 1
            continue
        lines = open(tp, encoding="utf-8", errors="replace").read().split("\n")
        for f in FIELDS:
            v = r.get(f)
            if not isinstance(v, dict):
                probs.append("%s: not an object" % f)
                continue
            if v.get("quote_line") in (None, "", 0) and (v.get("anchor") or "") == "":
                if f in ("objective",) and (v.get("statement") or "").lower().startswith("none"):
                    continue
                probs.append("%s: no line/anchor" % f)
                continue
            n_fields += 1
            try:
                ln = int(v.get("quote_line"))
            except Exception:
                probs.append("%s: bad line %r" % (f, v.get("quote_line")))
                continue
            a = norm(v.get("anchor"))
            if len(a.split()) > 14:
                probs.append("%s: anchor longer than 14 words" % f)
            win = " ".join(norm(lines[i]) for i in range(max(0, ln - 3), min(len(lines), ln + 2)))
            if a and a not in win:
                probs.append("%s: anchor not at line %d±2: %r" % (f, ln, v.get("anchor")))
        if probs:
            out[os.path.basename(p)] = probs
            n_bad += 1
    json.dump(out, open(os.path.join(d, "_check.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({"records": n_rec, "anchored_fields": n_fields, "records_with_problems": n_bad}))


if __name__ == "__main__":
    main()
