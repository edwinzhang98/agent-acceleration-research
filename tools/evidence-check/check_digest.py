#!/usr/bin/env python3
"""Check that a digest states nothing beyond the locked evidence.

usage: check_digest.py <digest.md> <extract.json> [<extract.json> ...]

Rules checked, unit by unit (a unit is a table cell or a sentence):
  REF_UNKNOWN     a reference [n004#6] that does not exist in the extracts
  NO_REF          a unit that contains a number but cites no evidence item
                  (units in a paragraph that starts with "Judgement:" or "Open:" may go without a number check
                  only if they contain no number; a number always needs a reference)
  NUMBER_NOT_IN_EVIDENCE   a number in the unit that occurs in none of the cited items
                  (claim, figure, measurement definition, location, date, and the work's title, arXiv id, version,
                  date and venue). A unit that contains "calc." is reported as CALC for a manual look instead.
Exit status 0 when there is no REF_UNKNOWN, NO_REF or NUMBER_NOT_IN_EVIDENCE.
"""
import json
import re
import sys
import unicodedata

REF = re.compile(r"\[((?:[a-z]\d{3}#\d+)(?:\s*[,;]\s*[a-z]\d{3}#\d+)*)\]")
NUM = re.compile(r"(?<![A-Za-z#\[])\d[\d,]*\.?\d*")
TR = {0x2010: "-", 0x2011: "-", 0x2012: "-", 0x2013: "-", 0x2014: "-", 0x2212: "-", 0x00A0: " ", 0x2009: " ", 0x202F: " ", 0x00D7: "x"}


def norm(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", s or "").translate(TR))


def numbers(s):
    s = REF.sub(" ", s)
    s = re.sub(r"\b[a-z]\d{3}\b", " ", s)
    out = []
    for t in NUM.findall(s):
        t = t.rstrip(".,")
        if t and not re.fullmatch(r"[0-9]", t):   # single digits are too common to check (list numbers, "3 models")
            out.append(t)
    return out


def main():
    digest, extracts = sys.argv[1], sys.argv[2:]
    items, works = {}, {}
    for p in extracts:
        d = json.load(open(p, encoding="utf-8"))
        for w in d["works"]:
            head = " ".join(str(w.get(k) or "") for k in ("title", "arxiv_id", "version_read", "date_v1", "venue_status", "source_url", "affiliations"))
            works[w["id"]] = head
            for e in w["evidence"]:
                items[e["ref"]] = norm(" ".join(str(e.get(k) or "") for k in ("claim", "figure", "measurement_definition", "location", "date", "line")) + " " + head)
    bad, calc, n_units, n_refs = [], [], 0, 0
    mode_free = False
    for ln, line in enumerate(open(digest, encoding="utf-8").read().split("\n"), 1):
        raw = line.strip()
        if not raw or raw.startswith("#") or re.fullmatch(r"\|?[\s:|-]+\|?", raw):
            mode_free = False if not raw else mode_free
            continue
        if re.match(r"^(\*\*)?(Judgement|Open|Not covered)", raw):
            mode_free = True
        if raw.startswith("|"):
            units = [c.strip() for c in raw.strip("|").split("|")]
        else:
            units = [u.strip() for u in re.split(r"(?<=[.;])\s+(?=[A-Z(\[*])", raw)]
        # references at the end of a sentence cover that sentence; in a table row, a reference anywhere in the row covers the row
        row_refs = [r.strip() for g in REF.findall(raw) for r in re.split(r"[,;]", g)] if raw.startswith("|") else []
        for u in units:
            if not u:
                continue
            n_units += 1
            refs = [r.strip() for g in REF.findall(u) for r in re.split(r"[,;]", g)] or row_refs
            n_refs += len(refs)
            unknown = [r for r in refs if r not in items]
            for r in unknown:
                bad.append((ln, "REF_UNKNOWN", r, u[:160]))
            nums = numbers(norm(u))
            if not nums:
                continue
            if not refs:
                bad.append((ln, "NO_REF", ", ".join(nums[:6]), u[:160]))
                continue
            pool = " ".join(items.get(r, "") for r in refs)
            pool_plain = pool.replace(",", "")
            miss = [n for n in nums if n not in pool and n.replace(",", "") not in pool_plain]
            if miss:
                (calc if "calc." in u else bad).append((ln, "CALC" if "calc." in u else "NUMBER_NOT_IN_EVIDENCE", ", ".join(miss), u[:200]))
    print("units %d, references %d, problems %d, calc. to look at %d" % (n_units, n_refs, len(bad), len(calc)))
    for b in bad:
        print("  line %d  %s  [%s]  %s" % b)
    for c in calc:
        print("  line %d  %s  [%s]  %s" % c)
    sys.exit(0 if not bad else 1)


if __name__ == "__main__":
    main()
