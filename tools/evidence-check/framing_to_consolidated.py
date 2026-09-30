#!/usr/bin/env python3
"""Turn audited framing records into a consolidated works file (batch prefix 'f') for build_part3_files.py.

usage: framing_to_consolidated.py <scratch_dir> <framing_dir> <out consolidated-f.json>

Each framing record (one per work, audited: <id>.audit.json verdict confirmed or corrected) becomes one work
'f<sid>' whose evidence items are its anchored fields, so that documents can cite [f-s003#0] style refs.
Work metadata (title, authors, version, dates, venue, url, txt_path) is copied from the store's consolidated
files when the work is there, or from records/<id>.json (the minimal p-records) otherwise.
"""
import glob
import json
import os
import sys

FIELDS = [("problem", "framing_problem"), ("challenge", "framing_challenge"), ("objective", "framing_objective"),
          ("solution_principle", "framing_solution"), ("claimed_gain", "framing_gain")]


def main():
    scratch, fdir, out = sys.argv[1], sys.argv[2], sys.argv[3]
    meta = {}
    for p in glob.glob(os.path.join(scratch, "check", "consolidated-*.json")):
        for w in json.load(open(p, encoding="utf-8"))["works"]:
            meta[w["id"]] = w
    for p in glob.glob(os.path.join(scratch, "records", "p*.json")):
        if p.endswith(".audit.json"):
            continue
        r = json.load(open(p, encoding="utf-8"))
        meta.setdefault(r["id"], r)
    works, skipped = [], []
    fmap = {}
    fmap_path = os.path.join(fdir, "_fmap.json")
    if os.path.exists(fmap_path):
        fmap = json.load(open(fmap_path, encoding="utf-8"))
    for p in sorted(glob.glob(os.path.join(fdir, "*.json"))):
        b = os.path.basename(p)
        if b.endswith(".audit.json") or b.startswith("_"):
            continue
        r = json.load(open(p, encoding="utf-8"))
        ap = p[:-5] + ".audit.json"
        au = json.load(open(ap, encoding="utf-8")) if os.path.exists(ap) else {}
        if au.get("verdict") not in ("confirmed", "corrected"):
            if "--include-unaudited" not in sys.argv:
                skipped.append((r.get("id"), au.get("verdict", "no audit")))
                continue
            au = {"verdict": "not audited"}
        m = meta.get(r["id"], {})
        if r["id"] not in fmap:
            fmap[r["id"]] = "f%03d" % (len(fmap) + 1)
        sid = fmap[r["id"]]
        ev = []
        for k, (f, field) in enumerate(FIELDS):
            v = r.get(f) or {}
            st = v.get("statement") or ""
            if not st or v.get("quote_line") in (None, "", 0) or not v.get("anchor"):
                if st and st.lower().startswith("none"):
                    continue
                if not st:
                    continue
            ev.append({"index": k, "ref": "%s#%d" % (sid, k), "field": field, "claim": st,
                       "figure": "-", "measurement_definition": "Framing statement (how the paper states its problem, challenge, objective, solution or gain); not a measurement.",
                       "location": "line %s of the saved text" % v.get("quote_line"), "line": v.get("quote_line"), "anchor": v.get("anchor"),
                       "label": "primary", "audit": au.get("verdict", "confirmed")})
        cls = {"efficiency_in_problem": r.get("efficiency_in_problem"), "efficiency_terms": r.get("efficiency_terms"),
               "agent_kind": r.get("agent_kind"), "position_in_pipeline": r.get("position_in_pipeline")}
        ev.append({"index": 5, "ref": "%s#5" % sid, "field": "framing_classification",
                   "claim": "Classification by the extractor, checked by the auditor: efficiency in the stated problem = %s; efficiency terms = %s; agent kind = %s; position = %s." % (
                       cls["efficiency_in_problem"], ", ".join(cls["efficiency_terms"] or []) or "none", cls["agent_kind"], cls["position_in_pipeline"]),
                   "figure": "-", "measurement_definition": "Reader classification (not a statement of the paper).", "location": "whole abstract and introduction",
                   "label": "secondary", "audit": au.get("verdict", "confirmed")})
        w = dict(m)
        w.update({"id": sid + "-" + r["id"], "short": sid, "title": m.get("title") or r.get("title"), "txt_path": r.get("txt_path"),
                  "used": True, "evidence": ev, "framing_of": r["id"], "notes": r.get("notes", "")})
        works.append(w)
    # eligibility of a framing work = eligibility of the underlying record (aliases resolved by the caller's tags file if any)
    elig_path = os.path.join(scratch, "check", "eligibility-by-record.json")
    elig = json.load(open(elig_path, encoding="utf-8"))
    alias = json.load(open(os.path.join(scratch, "check", "alias.json"), encoding="utf-8")) if os.path.exists(os.path.join(scratch, "check", "alias.json")) else {}
    for w in works:
        usid = w["framing_of"].split("-")[0]
        e = elig.get(usid) or elig.get(alias.get(usid, ""), {})
        elig[w["short"]] = dict(e, framing_of=usid) if e else {"decision": "", "formal_venue": "", "title": w.get("title"), "reason": "no eligibility decision for the underlying record %s" % usid, "framing_of": usid}
    json.dump(elig, open(elig_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(fmap, open(fmap_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({"works": works, "skipped": skipped}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({"works": len(works), "items": sum(len(w["evidence"]) for w in works), "skipped": skipped[:20], "n_skipped": len(skipped)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
