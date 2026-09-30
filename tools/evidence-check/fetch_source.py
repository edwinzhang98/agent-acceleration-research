#!/usr/bin/env python3
"""Download a source and save its full text, so that evidence can be located by line.

usage: fetch_source.py <arxiv-id[vN] | URL> <out_dir> [--key KEY] [--pdf]

Prints one JSON object:
  key, kind (arxiv-html | arxiv-pdf | html | pdf), source_url, abs_url, title, authors, versions
  (list of [vN, date] from the arXiv abs page), version (the one saved), txt_path, raw_path,
  n_lines, n_chars, fulltext (false when the text is too short to be a full paper or page), note
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from html.parser import HTMLParser

UA = "Mozilla/5.0 (Macintosh; research verification script; contact via arxiv.org/help) Python-urllib"
BLOCK = {"p", "div", "section", "article", "li", "ul", "ol", "tr", "table", "br", "figure", "figcaption",
         "caption", "blockquote", "pre", "dt", "dd", "header", "footer", "nav", "title", "hr", "thead", "tbody"}
HEAD = {"h1", "h2", "h3", "h4", "h5", "h6"}
SKIP = {"script", "style", "noscript", "svg", "template"}


def get(url, tries=4, binary=True):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
                return r.status, r.geturl(), r.headers.get("Content-Type", ""), data
        except urllib.error.HTTPError as e:
            last = "HTTP %s" % e.code
            if e.code in (404, 403, 410):
                return e.code, url, "", b""
        except Exception as e:  # noqa
            last = repr(e)
        time.sleep([4, 12, 30, 45][min(i, 3)])
    return 0, url, "", (last or "").encode()


class ToText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0
        self.math = 0
        self.cell_open = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in SKIP:
            self.skip += 1
            return
        if self.skip:
            return
        if tag == "math":
            self.math += 1
            alt = a.get("alttext") or ""
            if alt:
                self.out.append(" " + alt + " ")
            return
        if self.math:
            return
        if tag in HEAD:
            self.out.append("\n\n" + "#" * int(tag[1]) + " ")
        elif tag in ("td", "th"):
            self.out.append(" | ")
        elif tag in BLOCK:
            self.out.append("\n")
        elif tag == "img":
            alt = a.get("alt") or ""
            if alt:
                self.out.append(" [image: " + alt + "] ")

    def handle_endtag(self, tag):
        if tag in SKIP:
            self.skip = max(0, self.skip - 1)
            return
        if tag == "math":
            self.math = max(0, self.math - 1)
            return
        if self.skip or self.math:
            return
        if tag in HEAD or tag in BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if self.skip or self.math:
            return
        self.out.append(data)


def html_to_text(html):
    p = ToText()
    p.feed(html)
    text = "".join(p.out)
    text = text.replace("\xa0", " ")
    lines = []
    for ln in text.split("\n"):
        ln = re.sub(r"[ \t\r\f\v]+", " ", ln).strip()
        if ln:
            lines.append(ln)
    return "\n".join(lines) + "\n"


def pdf_to_text(pdf_path, txt_path):
    subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", pdf_path, txt_path], check=True)
    with open(txt_path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    pages = raw.split("\f")
    out = []
    for i, pg in enumerate(pages, 1):
        if pg.strip():
            out.append("[[page %d]]" % i)
            out.extend(ln.rstrip() for ln in pg.split("\n") if ln.strip())
    text = "\n".join(out) + "\n"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    return text


def meta(html, name):
    return re.findall(r'<meta name="%s" content="([^"]*)"' % re.escape(name), html)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    if len(args) < 2:
        print(__doc__)
        sys.exit(2)
    target, out_dir = args[0], args[1]
    key = None
    if "--key" in sys.argv:
        key = sys.argv[sys.argv.index("--key") + 1]
        args = [a for a in args if a != key]
        target, out_dir = args[0], args[1]
    force_pdf = "--pdf" in flags
    os.makedirs(out_dir, exist_ok=True)
    res = {"target": target, "fulltext": False, "note": ""}

    m = re.search(r"(?:arxiv\.org/(?:abs|pdf|html)/)?(\d{4}\.\d{4,5})(v\d+)?", target)
    is_arxiv = bool(m) and ("arxiv" in target or re.fullmatch(r"\d{4}\.\d{4,5}(v\d+)?", target))
    if is_arxiv:
        aid, ver = m.group(1), m.group(2)
        abs_url = "https://arxiv.org/abs/" + aid
        st, _, _, data = get(abs_url)
        if st != 200:
            res.update(kind="arxiv", abs_url=abs_url, note="abs page not reachable: status %s" % st)
            print(json.dumps(res, ensure_ascii=False, indent=1))
            return
        html = data.decode("utf-8", "replace")
        versions = re.findall(r"\[v(\d+)\](?:</a>)?\s*</strong>\s*([^<(]+?)\s*\(", html)
        title = (meta(html, "citation_title") or [""])[0]
        authors = meta(html, "citation_author")
        latest = "v" + versions[-1][0] if versions else (ver or "")
        use = ver or latest
        res.update(abs_url=abs_url, arxiv_id=aid, title=title, authors=authors,
                   versions=[["v" + v, d.strip()] for v, d in versions], version=use,
                   comments=re.sub(r"<[^>]+>", "", (re.findall(r'<td class="tablecell comments[^"]*">(.*?)</td>', html, re.S) or [""])[0]).strip(),
                   journal_ref=re.sub(r"<[^>]+>", "", (re.findall(r'<td class="tablecell jref">(.*?)</td>', html, re.S) or [""])[0]).strip())
        key = key or (aid + use)
        txt_path = os.path.join(out_dir, key + ".txt")
        done = False
        if not force_pdf:
            hurl = "https://arxiv.org/html/" + aid + use
            st, _, ct, data = get(hurl)
            if st == 200 and len(data) > 20000 and b"ltx_" in data:
                raw_path = os.path.join(out_dir, key + ".html")
                with open(raw_path, "wb") as f:
                    f.write(data)
                text = html_to_text(data.decode("utf-8", "replace"))
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(text)
                res.update(kind="arxiv-html", source_url=hurl, raw_path=raw_path)
                done = True
            else:
                res["note"] += "no arXiv HTML for %s (status %s); used the PDF. " % (use, st)
        if not done:
            purl = "https://arxiv.org/pdf/" + aid + use
            st, _, ct, data = get(purl)
            if st != 200 or not data.startswith(b"%PDF"):
                res.update(kind="arxiv-pdf", source_url=purl, note=res["note"] + "PDF not reachable: status %s" % st)
                print(json.dumps(res, ensure_ascii=False, indent=1))
                return
            raw_path = os.path.join(out_dir, key + ".pdf")
            with open(raw_path, "wb") as f:
                f.write(data)
            text = pdf_to_text(raw_path, txt_path)
            res.update(kind="arxiv-pdf", source_url=purl, raw_path=raw_path)
    else:
        url = target
        st, final, ct, data = get(url)
        if st != 200:
            res.update(kind="url", source_url=url, note="not reachable: status %s %s" % (st, data[:200].decode("utf-8", "replace")))
            print(json.dumps(res, ensure_ascii=False, indent=1))
            return
        key = key or re.sub(r"[^a-zA-Z0-9]+", "-", re.sub(r"^https?://", "", final))[:80].strip("-")
        txt_path = os.path.join(out_dir, key + ".txt")
        if data.startswith(b"%PDF") or "pdf" in ct.lower():
            raw_path = os.path.join(out_dir, key + ".pdf")
            with open(raw_path, "wb") as f:
                f.write(data)
            text = pdf_to_text(raw_path, txt_path)
            res.update(kind="pdf", source_url=final, raw_path=raw_path)
        else:
            raw_path = os.path.join(out_dir, key + ".html")
            with open(raw_path, "wb") as f:
                f.write(data)
            html = data.decode("utf-8", "replace")
            text = html_to_text(html)
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)
            t = re.findall(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
            res.update(kind="html", source_url=final, raw_path=raw_path, title=(t[0].strip() if t else ""))
    n_chars = len(text)
    res.update(key=key, txt_path=txt_path, n_lines=text.count("\n"), n_chars=n_chars)
    floor = 15000 if res["kind"].startswith("arxiv") or res["kind"] == "pdf" else 1500
    res["fulltext"] = n_chars >= floor
    if not res["fulltext"]:
        res["note"] += "saved text has only %d characters: treat as not full text. " % n_chars
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
