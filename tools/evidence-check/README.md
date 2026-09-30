# Evidence check tools (Part 3 research, 2026-09-29)

These scripts implement Edwin's rule of 2026-09-29: a source is used as evidence only if its full text was read and every statement is locked to a specific sentence or table row of that text.

The verified store (saved full texts, records with verbatim anchors, audit files) is kept outside the repository, because the saved texts are copies of the sources. On Edwin's Mac it is at `~/.claude/projects/-Users-edwin-projects-agent-acceleration-research/part3-verification/`. The repository holds what was derived from it: `research/2026-09-29-part3-evidence-ledger.md` and `research/2026-09-29-part3-records-*.md`.

## Steps

1. `fetch_source.py <arxiv id or URL> <sources_dir> [--key KEY] [--pdf]` saves the full text as one paragraph or table row per line and prints the arXiv version history, comments and journal-ref fields.
2. A reader writes one record per work (`records/<id>.json`). Each evidence item has a claim, the figure as printed, the measurement definition, the location, the line number in the saved text and a verbatim anchor of 4 to 14 words.
3. `check_anchors.py <record.json>` checks that every anchor occurs in the saved text at its line and that the numbers of the figure stand within three lines of it.
4. A second reader, who did not write the record, tries to refute each item against the saved text and writes `records/<id>.audit.json` (supported, supported-with-fix with the corrected wording, or not-supported).
5. `consolidate.py <records_dir> <out.json> [prefix ...]` keeps an item only if it passed steps 3 and 4.
6. `make_extract.py <out.json> <lane> ...` builds the input of a digest from the kept items of eligible works; `check_digest.py <digest.md> <extract.json> ...` checks that every number in a digest sentence occurs in the items the sentence cites.
7. `make_cited_extract.py <store_dir> <doc.md> <out.json>` collects the items a document cites, for independent reviewers.
8. `build_part3_files.py` assigns E-IDs to the cited items in order of first appearance and writes the documents, the parts of the evidence ledger and the records files; `assemble_ledger.py` joins the ledger parts with the introduction, the counts and the still-open list into `research/2026-09-29-part3-evidence-ledger.md`.

## Store layout

`sources/` saved texts · `records/` records and audits · `check/consolidated-<batch>.json` kept items · `check/eligibility-by-record.json` source-eligibility decisions (rule D313) with full author lists and venues confirmed at official pages · `extracts/` digest inputs · `digests/` reviewed digests.

## Limits

The mechanical checks catch invented quotations and numbers that are not near the quoted line. They cannot judge meaning, so every record is also audited by an independent reader and every document that cites items is reviewed against them. Figures inside images are not in the saved texts.
