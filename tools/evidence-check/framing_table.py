#!/usr/bin/env python3
"""Write compact tables of the audited framing records for the synthesis agents.
usage: framing_table.py <consolidated-f.json> <out_dir>
Writes <out_dir>/framing-all.json (list) and one file per position group <out_dir>/group-<slug>.json.
"""
import json, os, re, sys, collections
def main():
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    d = json.load(open(src, encoding="utf-8"))
    rows = []
    for w in d["works"]:
        ev = {e["field"]: e for e in w["evidence"]}
        cls = ev.get("framing_classification", {}).get("claim", "")
        m = re.search(r"efficiency in the stated problem = (\w+); efficiency terms = (.*?); agent kind = (.*?); position = (.*?)\.$", cls, re.S)
        rows.append({"ref": w["short"], "id": w.get("framing_of"), "title": w.get("title"), "venue": (w.get("venue_status") or "")[:80],
                     "efficiency_in_problem": m.group(1) if m else "", "efficiency_terms": m.group(2) if m else "", "agent_kind": m.group(3) if m else "", "position": m.group(4) if m else "",
                     "problem": ev.get("framing_problem", {}).get("claim", ""), "challenge": ev.get("framing_challenge", {}).get("claim", ""),
                     "objective": ev.get("framing_objective", {}).get("claim", ""), "solution": ev.get("framing_solution", {}).get("claim", ""), "gain": ev.get("framing_gain", {}).get("claim", ""), "notes": w.get("notes", "")})
    json.dump(rows, open(os.path.join(out, "framing-all.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    groups = collections.defaultdict(list)
    for r in rows:
        p = r["position"].lower()
        key = "serving" if "serving" in p or "inference" in p else "environment" if "environment" in p or "tool execution" in p else "improvement" if "improvement" in p or "learning" in p or "search" in p or "memory" in p else "evaluation" if "evaluation" in p or "measurement" in p or "benchmark" in p else "loop" if "loop" in p or "steps" in p or "context" in p else "other"
        groups[key].append(r)
    for k, v in groups.items():
        json.dump(v, open(os.path.join(out, "group-%s.json" % k), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: len(v) for k, v in groups.items()}), len(rows))
if __name__ == "__main__":
    main()
