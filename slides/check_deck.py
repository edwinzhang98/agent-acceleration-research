"""Fit check for the slide deck: measures every page, screenshots it, optionally exports the PDF.

Opens the built deck (slides/agent-acceleration.html) in headless Chromium through Playwright,
walks every `.slide`, reports for each page whether its content fits, saves one PNG per page and,
with --pdf, prints the deck to PDF (print media, one 1280 x 720 px page per slide).

Usage (run from anywhere; relative paths are resolved against the repository root):
  python3 slides/check_deck.py                                            # all pages
  python3 slides/check_deck.py s07 a3-1                                   # some pages
  python3 slides/check_deck.py --pdf=slides/agent-acceleration.pdf  # also export the PDF (both parts)
  --out=<dir>   write the screenshots to <dir> instead of slides/shots/

Report (JSON, one entry per page id):
  content  scrollHeight/clientHeight of the page's content box; the first number must be <= the
           second, otherwise the page overflows.
  bad      elements whose bottom comes within 24 px of the slide's bottom edge or whose right
           edge passes the slide's right edge, as class:bottom/right in px; must be empty.
  s00 (deck title) and s01 (Part 1 title) are full-bleed covers: no content box (content is null),
  and their `cover` boxes are listed under bad — ignore them.
A summary line follows the report. Exit code: 0 when every page other than s01 fits, 1 when any
page overflows, 2 when the check cannot run (deck not built, unknown page id).

Requirements: pip install playwright matplotlib (matplotlib is for build_deck.py), plus a Chromium
for Playwright — in this container it is pre-installed at /opt/pw-browsers; elsewhere run
`playwright install chromium`. Build the deck first: python3 slides/build_deck.py --fonts slides/fonts
"""
import asyncio
import json
import sys
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "slides" / "agent-acceleration.html"
DEFAULT_OUT = ROOT / "slides" / "shots"
COVER = ("s00", "s01", "t01")   # title pages, exempt from the check

# per page: elements that reach into the bottom 24 px of the slide or past its right edge,
# and the content box's scrollHeight/clientHeight
OVERFLOW_JS = """(sid)=>{const s=document.getElementById(sid);const r=s.getBoundingClientRect();const bad=[];
  s.querySelectorAll('.content, .content *, .cover, .cover *').forEach(el=>{const b=el.getBoundingClientRect(); if(b.height>0 && (b.bottom>r.bottom-24 || b.right>r.right+1)) bad.push(el.className+':'+Math.round(b.bottom-r.top)+'/'+Math.round(b.right-r.left));});
  const c=s.querySelector('.content'); let inner=null; if(c){inner=c.scrollHeight+'/'+c.clientHeight;}
  return {bad:bad.slice(0,6), content:inner};}"""


def repo_path(arg):
    """A command-line path, resolved against the repository root unless it is absolute."""
    p = Path(arg)
    return p if p.is_absolute() else ROOT / p


def overflows(entry):
    if entry["bad"]:
        return True
    if entry["content"]:
        scroll, client = (int(x) for x in entry["content"].split("/"))
        return scroll > client
    return False


async def main(ids=None, pdf=None, out=DEFAULT_OUT):
    if not HTML.exists():
        print(f"{HTML} not found — build it first: python3 slides/build_deck.py --fonts slides/fonts")
        return 2
    out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1280, "height": 720}, device_scale_factor=1)
        await pg.goto(HTML.as_uri())
        await pg.wait_for_timeout(300)
        await pg.evaluate("document.getElementById('help').remove()")
        all_ids = await pg.evaluate("[...document.querySelectorAll('.slide')].map(s=>s.id)")
        unknown = [sid for sid in (ids or []) if sid not in all_ids]
        if unknown:
            print("unknown page id(s): " + ", ".join(unknown) + " — the deck has: " + " ".join(all_ids))
            await b.close()
            return 2
        report = {}
        for sid in (ids or all_ids):
            await pg.evaluate(f"location.hash='#{sid}'")
            await pg.wait_for_timeout(120)
            report[sid] = await pg.evaluate(OVERFLOW_JS, sid)
            await pg.screenshot(path=str(out / f"{sid}.png"))
        print(json.dumps(report, indent=1))
        if pdf:
            await pg.emulate_media(media="print")
            await pg.pdf(path=str(pdf), width="1280px", height="720px", print_background=True, prefer_css_page_size=True)
            print("pdf", pdf)
        await b.close()
    failed = [sid for sid, entry in report.items() if sid not in COVER and overflows(entry)]
    if failed:
        print(f"FAIL: {len(failed)} of {len(report)} pages overflow: " + ", ".join(f"{sid} ({report[sid]['content']})" for sid in failed))
        return 1
    print(f"OK: all {len(report)} pages fit" + (" (the title pages s00, s01 and t01 are exempt)" if set(COVER) & set(report) else "")
          + f"; screenshots in {out}")
    return 0


if __name__ == "__main__":
    ids, pdf, out = [], None, DEFAULT_OUT
    for a in sys.argv[1:]:
        if a.startswith("--pdf="):
            pdf = repo_path(a[len("--pdf="):])
        elif a.startswith("--out="):
            out = repo_path(a[len("--out="):])
        elif not a.startswith("--"):
            ids.append(a)
    sys.exit(asyncio.run(main(ids or None, pdf, out)))
