#!/usr/bin/env python3
"""Build the input of one digest: the kept (anchor-checked and audited) evidence of the works of given lanes.

usage: make_extract.py <out.json> <lane> [<lane> ...]

Reads check/consolidated-*.json (from consolidate.py) and check/wf*-result.json (workflow results, for lanes
and relevance). Summary fields written by the verifier are left out: only locked evidence items go in.
Each item gets a reference "<work id>#<index>", e.g. n004#6, which the digest must cite.
"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


import re


def _nums(t):
    return set(x.rstrip(".,") for x in re.findall(r"\d[\d,]*\.?\d*", t or "") if len(x.rstrip(".,")) > 1)


def _figure(e):
    # when the auditor corrected an item and the corrected text no longer carries the numbers of the original
    # figure, the original figure must not be cited
    if e.get("audit") == "supported-with-fix":
        fixed = ((e.get("claim") or "") + " " + (e.get("measurement_definition") or "")).replace(",", "")
        if any(n.replace(",", "") not in fixed for n in _nums(e.get("figure"))):
            return "(corrected by the auditor; use the numbers in the claim)"
    return e.get("figure")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    field = None
    if "--field" in sys.argv:
        field = sys.argv[sys.argv.index("--field") + 1]
        args = [a for a in args if a != field]
    out, lanes = args[0], set(args[1:])
    meta = {}
    for p in glob.glob(os.path.join(ROOT, "check", "wf*-result.json")):
        r = json.load(open(p, encoding="utf-8"))
        for u in r.get("usable", []):
            meta[u["id"]] = {"lanes": u.get("lanes") or [], "relevance": u.get("relevance"), "in_ledger": u.get("in_ledger", "")}
    # gap-sweep records: lanes recovered from the workflow journal
    gl = os.path.join(ROOT, "check", "g-lanes.json")
    if os.path.exists(gl):
        for k, v in json.load(open(gl)).items():
            meta_short = {"lanes": v, "relevance": 4, "in_ledger": ""}
            meta["__short__" + k] = meta_short
    # source eligibility under the rule of 2026-09-29 (D313); works on hold or excluded are left out
    elig = {}
    ep = os.path.join(ROOT, "check", "eligibility-by-record.json")
    if os.path.exists(ep):
        elig = json.load(open(ep, encoding="utf-8"))
    OK = ("top-venue", "leading-company-official", "institutional-supplement")
    keep_all = "--include-ineligible" in sys.argv
    works = []
    for p in sorted(glob.glob(os.path.join(ROOT, "check", "consolidated-*.json"))):
        d = json.load(open(p, encoding="utf-8"))
        for w in d["works"]:
            m = meta.get(w["id"]) or meta.get("__short__" + w["id"].split("-")[0], {})
            e_ = elig.get(w["id"].split("-")[0])
            if elig and not keep_all and (not e_ or e_.get("decision") not in OK):
                continue
            w["_elig"] = e_ or {}
            if not w.get("used") or (lanes and not (lanes & set(m.get("lanes", [])))):
                continue
            if field and not any(e.get("field") == field for e in w.get("evidence", [])):
                continue
            short = w["id"].split("-")[0]
            works.append({
                "id": short, "title": w.get("title"), "arxiv_id": w.get("arxiv_id"), "version_read": (w.get("version_read") or "")[:60],
                "date_v1": w.get("date_v1"), "venue_status": w.get("venue_status"), "affiliations": (w.get("affiliations") or "")[:300],
                "source_url": w.get("source_url") or w.get("abs_url"), "lanes": m.get("lanes"), "relevance": m.get("relevance"),
                "already_in_dossier_ledger": m.get("in_ledger", ""),
                "source_eligibility": w["_elig"].get("decision"), "formal_venue_verified": w["_elig"].get("formal_venue"),
                "venue_claim_unverified": w["_elig"].get("venue_claim_unverified"), "institutions": (w["_elig"].get("institutions") or "")[:300],
                "what_is_changed_tags": w.get("what_is_changed") if not any(f.lower().startswith("what_is_changed") for f in (w.get("fields_flagged") or [])) else "(flagged by the auditor; use the evidence items)",
                "objective_includes_cost_tag": w.get("objective_includes_cost") if not any(f.lower().startswith("objective_includes_cost") for f in (w.get("fields_flagged") or [])) else "(flagged by the auditor; use the evidence items)",
                "verifier_judgement_not_evidence": w.get("gap_vs_plan"),
                "evidence": [{"ref": "%s#%d" % (short, e["index"]), "field": e.get("field"), "claim": e.get("claim"), "figure": _figure(e),
                              "measurement_definition": e.get("measurement_definition"), "location": e.get("location"), "line": e.get("line"),
                              "label": e.get("label"), "date": e.get("date"), "audit": e.get("audit")} for e in w.get("evidence", []) if (not field or e.get("field") == field)],
            })
    works.sort(key=lambda w: (-(w.get("relevance") or 0), w["id"]))
    json.dump({"lanes": sorted(lanes), "n_works": len(works), "n_items": sum(len(w["evidence"]) for w in works), "works": works},
              open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(out, "works", len(works), "items", sum(len(w["evidence"]) for w in works), "bytes", os.path.getsize(out))


if __name__ == "__main__":
    main()
