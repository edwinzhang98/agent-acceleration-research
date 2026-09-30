#!/usr/bin/env python3
"""Merge records, audits and the mechanical anchor check into one file.

usage: consolidate.py <records_dir> <out.json> [prefix ...]

An evidence item is KEPT only if (1) its anchor occurs in the saved full text and the numbers of its figure
stand within 3 lines of the anchor (check_anchors.py), and (2) the independent auditor judged it supported
or supported-with-fix. For supported-with-fix the auditor's corrected claim and definition replace the original.
A work is USED only if its full text was saved, the auditor did not call it not-usable, and at least one item is kept.
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_anchors as ca  # noqa


def main():
    rdir, out = sys.argv[1], sys.argv[2]
    prefixes = tuple(sys.argv[3:]) or ("",)
    works, stats = [], {"records": 0, "used": 0, "not_used": 0, "items": 0, "kept": 0, "dropped_mechanical": 0,
                        "dropped_audit": 0, "kept_with_fix": 0, "fields_flagged": 0, "no_audit": 0}
    for p in sorted(glob.glob(os.path.join(rdir, "*.json"))):
        b = os.path.basename(p)
        if b.endswith(".audit.json") or not b.startswith(prefixes):
            continue
        stats["records"] += 1
        try:
            rec, rows = ca.check_record(p)
        except Exception as e:  # noqa
            works.append({"id": b[:-5], "used": False, "reason": "record unreadable: %r" % e})
            stats["not_used"] += 1
            continue
        mech = {r[0]: (r[1], r[2]) for r in rows}
        ap = p[:-5] + ".audit.json"
        audit = None
        if os.path.exists(ap):
            try:
                audit = json.load(open(ap, encoding="utf-8"))
            except Exception:  # noqa
                audit = None
        if audit is None:
            stats["no_audit"] += 1
        av = {}
        for it in (audit or {}).get("items", []) or []:
            if isinstance(it.get("index"), int):
                av[it["index"]] = it
        kept, dropped = [], []
        for k, it in enumerate(rec.get("evidence") or []):
            stats["items"] += 1
            m, line = mech.get(k, ("NO_TEXT", 0))
            a = av.get(k)
            if m != "PASS":
                stats["dropped_mechanical"] += 1
                dropped.append({"index": k, "why": "mechanical: " + m, "claim": it.get("claim"), "figure": it.get("figure")})
                continue
            if a is None or a.get("verdict") == "not-supported":
                stats["dropped_audit"] += 1
                dropped.append({"index": k, "why": "audit: " + ("no verdict" if a is None else a.get("reason", "")),
                                "claim": it.get("claim"), "figure": it.get("figure")})
                continue
            item = dict(it)
            item["index"] = k
            item["line_checked"] = line
            item["audit"] = a.get("verdict")
            if a.get("verdict") == "supported-with-fix":
                stats["kept_with_fix"] += 1
                item["claim_original"] = it.get("claim")
                item["definition_original"] = it.get("measurement_definition")
                if a.get("fixed_claim"):
                    item["claim"] = a["fixed_claim"]
                if a.get("fixed_measurement_definition"):
                    item["measurement_definition"] = a["fixed_measurement_definition"]
                item["audit_reason"] = a.get("reason", "")
            stats["kept"] += 1
            kept.append(item)
        flagged = (audit or {}).get("summary_fields_unsupported") or []
        stats["fields_flagged"] += len(flagged)
        used = bool(rec.get("fulltext")) and bool(rec.get("exists", True)) and bool(kept) and (audit or {}).get("overall") != "not-usable" and audit is not None
        stats["used" if used else "not_used"] += 1
        w = {k: rec.get(k) for k in ("title", "source_url", "abs_url", "arxiv_id", "version_read", "date_v1", "date_version_read",
                                     "authors", "affiliations", "venue_status", "venue_status_source", "txt_path", "threads",
                                     "what_is_changed", "signal", "proposal_method", "selection_rule", "objective_includes_cost",
                                     "human_in_loop", "mechanism", "loop_cost", "limitations_stated", "gap_vs_plan", "verdict",
                                     "corrections", "fulltext", "exists")}
        w.update(id=b[:-5], used=used, audit_overall=(audit or {}).get("overall", "audit-missing"), fields_flagged=flagged,
                 audit_notes=(audit or {}).get("notes", ""), evidence=kept, dropped=dropped)
        if not used:
            w["reason"] = ("no full text" if not rec.get("fulltext") else "no audit" if audit is None else
                           "auditor: not usable" if (audit or {}).get("overall") == "not-usable" else "no item survived")
        works.append(w)
    json.dump({"stats": stats, "works": works}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(stats, indent=1))


if __name__ == "__main__":
    main()
