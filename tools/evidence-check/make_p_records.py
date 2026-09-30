#!/usr/bin/env python3
"""Build minimal records for the deck works fetched on 2026-09-30 (batch p) from the fetch log and the deck reference list.

usage: make_p_records.py <scratch_dir> <fetch-p.json> <fetch-p.log> <deck-works.json>
Writes records/p###-<slug>.json (no evidence items; metadata for the reference list and the ledger), adds
eligibility decisions for batch p to check/eligibility-by-record.json (from the deck's source types) and prints a summary.
"""
import json
import os
import re
import sys


def slug(t):
    s = re.sub(r"[^a-z0-9]+", "-", (t or "").lower()).strip("-")
    return "-".join(s.split("-")[:6])


def main():
    scratch, fj, flog, deck = sys.argv[1:5]
    todo = {x["key"]: x for x in json.load(open(fj, encoding="utf-8"))}
    deckw = {e["key"]: e for e in json.load(open(deck, encoding="utf-8"))}
    # the log is a sequence of JSON objects (pretty-printed); split on top-level braces
    txt = open(flog, encoding="utf-8").read()
    objs = []
    for m in re.finditer(r"\{\n(?:.*\n)*?\}", txt):
        try:
            objs.append(json.loads(m.group(0)))
        except Exception:
            pass
    fetched = {o.get("key"): o for o in objs if o.get("key")}
    elig_path = os.path.join(scratch, "check", "eligibility-by-record.json")
    elig = json.load(open(elig_path, encoding="utf-8"))
    n_ok, n_bad = 0, 0
    for key, x in todo.items():
        o = fetched.get(key)
        d = deckw.get(x["deck_key"], {})
        ref = d.get("ref", "")
        if not o or not o.get("fulltext"):
            n_bad += 1
            print("NOT FETCHED", key, x["deck_key"], (o or {}).get("note", ""))
            continue
        title = o.get("title") or ""
        rid = "%s-%s" % (key, slug(title) or x["deck_key"])
        rec = {"id": rid, "short": key, "batch": "p", "deck_key": x["deck_key"], "title": title, "authors": o.get("authors"),
               "arxiv_id": x["src"] if re.match(r"\d{4}\.\d{4,5}", x["src"]) else "", "abs_url": o.get("abs_url"), "source_url": o.get("source_url"),
               "version_read": o.get("version") or o.get("kind"), "date_version_read": (dict(o.get("versions") or []).get(o.get("version")) if o.get("versions") else ""),
               "date_v1": (o.get("versions") or [["", ""]])[0][1] if o.get("versions") else "", "venue_status": "", "deck_reference": ref,
               "txt_path": o.get("txt_path"), "used": True, "evidence": [], "fetched": "2026-09-30", "note": o.get("note", "")}
        # venue and class from the deck reference text: the italic venue names a published paper; a bare arXiv line is a preprint
        vm = re.search(r"<i>(.*?)</i>", ref)
        venue = re.sub(r"\s+", " ", vm.group(1)).strip() if vm else ""
        ym = re.search(r"\((\d{4})[a-z]?\)", ref)
        published = bool(venue) and bool(re.search(r"Proceedings|Conference|Transactions|Journal|Symposium|Findings|Advances in Neural|Communications of the ACM|Software Engineering", venue)) and "Workshop" not in venue and "workshop" not in venue
        cls = "top-venue" if published else "institutional-supplement"
        rec["venue_status"] = ("published: %s (per the deck reference list, checked 2026-09-27/28)" % venue) if published else ("workshop paper: %s (per the deck reference list)" % venue if venue else "arXiv preprint (per the deck reference list)")
        rec["authors"] = "; ".join(o.get("authors") or []) if isinstance(o.get("authors"), list) else (o.get("authors") or "")
        rec["year"] = ym.group(1) if ym else ""
        cite_urls = [u for u in re.findall(r"https?://[^\s<>\"]+", ref) if "arxiv.org" not in u]
        json.dump(rec, open(os.path.join(scratch, "records", rid + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        elig[key] = {"decision": cls, "formal_venue": venue if published else "", "title": title, "year": rec["year"], "authors_full": rec["authors"],
                     "formal_citation_url": (cite_urls[0].rstrip(".") if cite_urls else ""), "institutions": "",
                     "reason": "Taken from the deck reference list (slides/build_deck.py REFS, compiled 2026-09-28 under the source-credibility rule of 2026-09-27); class from the reference's venue: %s." % (
                         "published conference or journal paper" if published else ("workshop paper, counted by institution" if venue else "preprint, counted by institution"))}
        n_ok += 1
    json.dump(elig, open(elig_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({"records": n_ok, "not_fetched": n_bad}))


if __name__ == "__main__":
    main()
