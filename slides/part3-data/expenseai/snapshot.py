"""Copy the ExpenseAI data that the Part 3 short deck's data module shows into this folder.

The deck is built from this snapshot only, so it rebuilds without the ExpenseAI repository. Run this script again
to refresh the snapshot (it reads ExpenseAI and never writes there):

    .venv/bin/python slides/part3-data/expenseai/snapshot.py [/path/to/ExpenseAI]

What it writes, next to this file:
  facts.json          ExpenseAI gw_policy_data/reports/slides/20260922-intro-facts.json (counts; every situation)
  provisions.json     the 160 provisions of benchmark/pool/coverage.py and coverage_newcats.py, and the 60 web sources
  trip_a/             testing_cases/trip_a_chicago/{expected.json, trip_notes.txt, turns.json, MANIFEST.md}, the file
                      list of the folder, and batch 20260914-02's score.txt and log.txt for trip A
  img/                the screenshots and document images the pages show (see IMAGES below)
  LEDGER.md           gw_policy_data/reports/LEDGER.md, every travel situation's record across batches
  loops.json          the kinds of loop counted over every recorded run (see loop_counts)
  SOURCE.txt          the ExpenseAI commit the snapshot was taken from
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
EAI = Path(sys.argv[1] if len(sys.argv) > 1 else "/Users/edwin/projects/ExpenseAI")
IMG_SRC = EAI / "gw_policy_data/reports/slides/preview/img"
POOL = EAI / "gw_policy_data/experiment/files"
TRIP = EAI / "testing_cases/trip_a_chicago"
BATCH = EAI / "local_data/batches/20260914-02/trip_a_chicago"
RUN_FOLIO = EAI / "local_data/runs/20260914-045439-concur-2164/frames"   # trip A, turn 2: the Hyatt folio

# (target name, source, crop box on the source or None, max width in pixels)
IMAGES = [
    ("manual-appb.png", IMG_SRC / "prov-appb.png", None, 726),
    ("folio-chicago.png", IMG_SRC / "folio-trip-a.png", None, 810),
    ("folio-chicago-top.png", IMG_SRC / "folio-trip-a.png", (0, 0, 810, 300), 810),
    ("united.png", IMG_SRC / "s07-air.png", None, 900),
    ("reg-virtual.png", IMG_SRC / "s08-reg.png", None, 900),
    ("purple-pig.png", IMG_SRC / "check-purple-pig.png", None, 502),
    ("jetblue.png", IMG_SRC / "ex-jetblue.png", None, 900),
    ("westin-internet.png", IMG_SRC / "ex-folio.png", None, 900),
    ("uber.png", IMG_SRC / "s10-gen-uber.png", None, 700),
    ("golf.png", IMG_SRC / "s08-other.png", None, 900),
    ("program.png", IMG_SRC / "s08-doc.png", None, 900),
    ("dues.png", IMG_SRC / "s09-dues.png", None, 700),
    ("workstation.png", IMG_SRC / "s09-supp.png", None, 700),
    ("movers.png", IMG_SRC / "s09-reloc.png", None, 700),
    ("airbnb.png", IMG_SRC / "ex-airbnb.png", None, 900),
    ("concur-form.png", RUN_FOLIO / "000009.png", (0, 0, 1676, 1804), 900),
    ("concur-itemize.png", RUN_FOLIO / "000016.png", (0, 0, 1676, 1560), 900),
    # the two loops of the example page: a rule of the site (trip A, 11 Sep) and a save that looked failed (trip R, 21 Sep, P-053)
    ("loop-apostrophe.png", EAI / "local_data/runs/20260911-050919-concur-2859/frames/000013.png", (40, 500, 1380, 980), 900),
    ("loop-notfound.png", EAI / "local_data/runs/20260921-030704-concur-56a7/frames/000006.png", (560, 330, 1290, 950), 700),
]
# documents printed from the generated pool: (target, PDF, crop box on a 100-dpi rendering or None)
PDFS = [
    ("wifi.png", POOL / "AIR-WIFI-OTHER-CARRIER__0__American Airlines Wi-Fi receipt.pdf", (0, 0, 850, 520)),
    ("folio-boston.png", POOL / "LOD-FOLIO-PERSONAL__0__The Westin Copley Place, Boston folio.pdf", (40, 36, 452, 212)),
    ("folio-palmer.png", POOL / "LOD-FOLIO-PERSONAL__1__Palmer House, a Hilton Hotel folio.pdf", (40, 36, 452, 212)),
    ("folio-atlanta.png", POOL / "LOD-FOLIO-PERSONAL__2__Hyatt Regency Atlanta folio.pdf", (40, 36, 452, 212)),
]


def loop_counts() -> dict:
    """Count the kinds of loop in every recorded run: failed actions by cause, picker searches that found no option,
    the same action repeated on the same element, the runs in which Concur showed its own errors."""
    import glob, re
    from collections import Counter
    classes = [("timeout", r"Timeout \d+ms exceeded"),
               ("wrong_action", r"is not an <input>|is not a <select>|is a picker, not a text box|Node is not an HTMLInputElement|unknown action"),
               ("page_redrawn", r"element is gone|re-rendered|frame is no longer on the page"),
               ("dialog_in_way", r"dialog .* is on top|close or cancel that dialog")]
    runs = sorted(glob.glob(str(EAI / "local_data/runs/*/steps.jsonl")))
    failed, actions, no_option, stuck = Counter(), 0, 0, 0
    for p in runs:
        seq = []
        for line in open(p, encoding="utf-8"):
            try:
                st = json.loads(line)
            except ValueError:
                continue
            for a in st.get("actions") or []:
                actions += 1
                r = a.get("result") or {}
                fb = str(r.get("feedback") or "")
                no_option += fb.startswith("No option matched")
                if r.get("status") in ("error", "refused"):
                    msg = str(r.get("error") or fb)
                    failed[next((k for k, rx in classes if re.search(rx, msg)), "other")] += 1
                t = a.get("target")
                seq.append((a.get("action"), t.get("id") if isinstance(t, dict) else t, str(a.get("value"))[:40]))
        best = cur = 1
        for i in range(1, len(seq)):
            cur = cur + 1 if seq[i] == seq[i - 1] and seq[i][0] not in ("wait", "done") else 1
            best = max(best, cur)
        stuck += best >= 3
    concur = Counter()
    for p in glob.glob(str(EAI / "local_data/runs/*/observations/*.json")):
        try:
            t = json.load(open(p, encoding="utf-8")).get("text") or ""
        except ValueError:
            continue
        run = Path(p).parts[-3]
        for key, needle in (("lines_with_errors", "Expenses with ERRORS"), ("attendee_errors", "Attendees have errors"), ("invalid_character", "invalid character")):
            if needle in t:
                concur[(key, run)] = 1
    by = Counter(k for k, _ in concur)
    return dict(runs=len(runs), actions=actions, failed=dict(failed), failed_total=sum(failed.values()), no_option=no_option,
                stuck_runs=stuck, concur_error_runs=dict(by),
                note="computed by snapshot.py from local_data/runs (every recorded run); stuck = the same action on the same element 3+ times in a row")


def save(im: Image.Image, name: str, max_w: int) -> None:
    im = im.convert("RGB")
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    im.save(HERE / "img" / name, optimize=True)


def main() -> None:
    (HERE / "img").mkdir(exist_ok=True)
    (HERE / "trip_a").mkdir(exist_ok=True)
    shutil.copy(EAI / "gw_policy_data/reports/slides/20260922-intro-facts.json", HERE / "facts.json")
    dump = ("import sys, json; sys.path.insert(0, '.');"
            "from benchmark.pool import coverage as c, coverage_newcats as n;"
            "rules = lambda m, pool: [dict(pool=pool, id=r.id, page=r.page, text=r.text, actionable=r.actionable, why_not=r.why_not) for r in m.RULES];"
            "print(json.dumps(dict(provisions=rules(c, 'travel') + rules(n, 'non_travel'),"
            " sources=[dict(id=k, title=v[0], url=v[1]) for k, v in n.SOURCES.items()]), ensure_ascii=False, indent=1))")
    out = subprocess.run([str(EAI / ".venv/bin/python"), "-c", dump], cwd=EAI, capture_output=True, text=True, check=True).stdout
    (HERE / "provisions.json").write_text(out, encoding="utf-8")
    for f in ("expected.json", "trip_notes.txt", "turns.json", "MANIFEST.md"):
        shutil.copy(TRIP / f, HERE / "trip_a" / f)
    (HERE / "trip_a/files.txt").write_text("\n".join(sorted(os.listdir(TRIP))) + "\n", encoding="utf-8")
    shutil.copy(BATCH / "score.txt", HERE / "trip_a/score.txt")
    shutil.copy(BATCH / "log.txt", HERE / "trip_a/log.txt")
    shutil.copy(EAI / "gw_policy_data/reports/LEDGER.md", HERE / "LEDGER.md")
    for name, src, box, max_w in IMAGES:
        im = Image.open(src)
        save(im.crop(box) if box else im, name, max_w)
    tmp = HERE / "img/_page"
    for name, pdf, box in PDFS:
        subprocess.run(["pdftoppm", "-r", "100", "-png", "-f", "1", "-l", "1", "-singlefile", str(pdf), str(tmp)], check=True)
        im = Image.open(str(tmp) + ".png")
        save(im.crop(box) if box else im, name, 850)
        os.remove(str(tmp) + ".png")
    (HERE / "loops.json").write_text(json.dumps(loop_counts(), indent=1) + "\n", encoding="utf-8")
    rev = subprocess.run(["git", "-C", str(EAI), "log", "-1", "--format=%h %ci %s"], capture_output=True, text=True).stdout
    (HERE / "SOURCE.txt").write_text(f"ExpenseAI repository: {EAI}\ncommit: {rev}", encoding="utf-8")
    print("snapshot written to", HERE)


if __name__ == "__main__":
    main()
