#!/usr/bin/env python3
"""Assemble the evidence ledger file from the parts written by build_part3_files.py.

usage: assemble_ledger.py <out_dir> <intro.md> <open.md> <counts text> <out.md>
"""
import json
import os
import re
import sys


def main():
    out, intro, opn, counts, dest = sys.argv[1:6]
    p = json.load(open(os.path.join(out, "ledger-parts.json"), encoding="utf-8"))
    emap = json.load(open(os.path.join(out, "e-map.json")))
    dmap = json.load(open(os.path.join(out, "d-map.json")))
    ids = sorted(int(v[1:]) for v in emap.values())
    dids = sorted(int(v[1:]) for v in dmap.values())
    t = open(intro, encoding="utf-8").read()
    t = t.replace("@@E_RANGE@@", "E%d–E%d" % (ids[0], ids[-1])).replace("@@D_RANGE@@", "D%d–D%d" % (dids[0], dids[-1])).replace("@@COUNTS@@", counts)
    body = "\n\n".join([t.strip(), p["sec1"], p["sec2"], p["sec3"], open(opn, encoding="utf-8").read().strip(), p["refs"]]) + "\n"
    open(dest, "w", encoding="utf-8").write(body)
    print(dest, len(body), "bytes;", len(re.findall(r"^\| E\d+ ", body, flags=re.M)), "E rows;", len(re.findall(r"^\| D\d+ ", body, flags=re.M)), "D rows")


if __name__ == "__main__":
    main()
