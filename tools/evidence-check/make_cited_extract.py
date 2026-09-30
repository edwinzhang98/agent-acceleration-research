#!/usr/bin/env python3
"""Collect the evidence items a document cites, for independent reviewers.

usage: make_cited_extract.py <scratch_dir> <doc.md> <out.json> [--tags tags.json]

Reads check/consolidated-*.json (items that passed the anchor check and the audit) and
check/eligibility-by-record.json. Writes, per cited work, its title, version read, date, eligibility class,
formal venue, and the cited items (claim, figure, measurement definition, location, label, audit).
Prints the references that are not in the audited store and the works that are not eligible.
"""
import glob
import json
import os
import re
import sys

REF = re.compile(r"[a-z]\d{3}#\d+")
TAG = re.compile(r"@@([A-Za-z0-9_-]+)@@")


def main():
    scratch, doc, out = sys.argv[1], sys.argv[2], sys.argv[3]
    tags = json.load(open(sys.argv[sys.argv.index("--tags") + 1], encoding="utf-8")) if "--tags" in sys.argv else {}
    alias = tags.get("ALIAS", {})
    text = open(doc, encoding="utf-8").read()
    unresolved = set()

    def tagsub(m):
        v = tags.get(m.group(1))
        if isinstance(v, list):
            return "".join("[%s]" % r for r in v)
        if v is None:
            unresolved.add(m.group(1))
        return m.group(0)
    text = TAG.sub(tagsub, text)
    works = {}
    for p in sorted(glob.glob(os.path.join(scratch, "check", "consolidated-*.json"))):
        for w in json.load(open(p, encoding="utf-8"))["works"]:
            if w.get("used"):
                works[w["id"].split("-")[0]] = w
    elig = json.load(open(os.path.join(scratch, "check", "eligibility-by-record.json"), encoding="utf-8"))
    res, missing, inel = {}, [], []
    for r in REF.findall(text):
        sid, k = r.split("#")
        w = works.get(sid)
        e = next((x for x in (w or {}).get("evidence", []) if x["index"] == int(k)), None)
        if not e:
            if r not in missing:
                missing.append(r)
            continue
        el = elig.get(alias.get(sid, sid)) or {}
        if el.get("decision") in (None, "hold", "exclude") and sid not in inel:
            inel.append(sid)
        d = res.setdefault(sid, {"id": sid, "title": w.get("title"), "version_read": w.get("version_read"), "date": w.get("date_version_read") or w.get("date_v1"),
                                  "source_url": w.get("source_url"), "eligibility": el.get("decision"), "formal_venue": el.get("formal_venue") or "",
                                  "venue_status_as_recorded": w.get("venue_status"), "items": []})
        if not any(i["ref"] == r for i in d["items"]):
            d["items"].append({"ref": r, "field": e.get("field"), "claim": e.get("claim"), "figure": e.get("figure"),
                               "measurement_definition": e.get("measurement_definition"), "location": e.get("location"),
                               "label": e.get("label"), "audit": e.get("audit")})
    json.dump({"works": list(res.values())}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({"works": len(res), "items": sum(len(w["items"]) for w in res.values()), "not_in_store": missing,
                      "not_eligible": inel, "unresolved_tags": sorted(unresolved)}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
