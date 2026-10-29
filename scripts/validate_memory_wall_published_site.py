#!/usr/bin/env python3
"""Validate the exact A7 Pages static output before upload, including no-JS seven-link TOC."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from html.parser import HTMLParser
from html import escape

ROOT=Path(__file__).resolve().parents[1]
CAN=ROOT/"registry/curations/memory-wall-contents.v0.1.json"

class LinkReader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_toc=False
        self.toc_links=[]
        self.ids=set()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get("id"): self.ids.add(a["id"])
        if tag=="nav" and a.get("id")=="memory-wall-contents": self.in_toc=True
        if self.in_toc and tag=="a" and a.get("class","").find("mw-toc-card")>=0:
            self.toc_links.append(a.get("href"))
    def handle_endtag(self,tag):
        if tag=="nav" and self.in_toc: self.in_toc=False

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--site-root",default=str(ROOT/"site"))
    ap.add_argument("--data-dir",default=None)
    ap.add_argument("--commit-sha",required=True)
    args=ap.parse_args()
    site=Path(args.site_root)
    data=Path(args.data_dir) if args.data_dir else site/"data"
    raw=CAN.read_bytes()
    canonical=json.loads(raw)
    toc=json.loads((data/"memory-wall-contents.json").read_text(encoding="utf-8"))
    extraction=json.loads((data/"memory-extraction-retrieval.json").read_text(encoding="utf-8"))
    assert toc["source_sha256"]==hashlib.sha256(raw).hexdigest(),"The published TOC does not match its source"
    assert toc["site_build_commit"]==args.commit_sha,"Published TOC was generated from the wrong commit"
    assert extraction["site_build_commit"]==args.commit_sha
    versioned=json.loads((data/"memory-live-version-control.json").read_text(encoding="utf-8"))
    assert versioned["collection_id"]=="A7-MEM-LIVE-VERSION-009"
    assert versioned["site_build_commit"]==args.commit_sha,"Extraction bundle points to the wrong build"
    assert toc["collection_count"]==7 and len(toc["collections"])==7
    assert toc["collections"]==canonical["collections"],"Generated TOC differs from source order or link metadata"
    html=(site/"memory-wall.html").read_text(encoding="utf-8")
    home=(site/"index.html").read_text(encoding="utf-8")
    shell=(site/"assets/a7-site-shell.js").read_text(encoding="utf-8")
    parser=LinkReader();parser.feed(html)
    hrefs=["#"+c["anchor"] for c in canonical["collections"]]
    assert parser.toc_links==hrefs,f"Static no-JavaScript TOC out of order or missing: {parser.toc_links}"
    assert all(c["anchor"] in parser.ids for c in canonical["collections"]),"A TOC destination lacks a real target"
    assert all(f'<strong>{escape(c["title"])}</strong>' in html for c in canonical["collections"]),"Static link labels differ from source"
    assert home.count('href="memory-wall.html#memory-wall-contents"')==1,"L0 needs one direct contents link"
    assert 'link("memory-wall.html#memory-wall-contents","Memory Wall contents")' in shell
    for item in ("memory-wall.html","index.html","assets/memory-wall-guides.js","assets/memory-wall-guides.css","assets/a7-site-shell.js"):
        assert (site/item).is_file(),f"Missing Pages payload {item}"
    assert '<script src="assets/memory-wall-guides.js" defer>' in html
    assert 'id="mwTocStatus"' in html
    assert 'href="#extraction-retrieval"' in html
    assert 'href="#live-file-version-control"' in html and html.count('id="live-file-version-control"')==1
    assert extraction["collection_id"]=="A7-MEM-EXTRACTION-008" and len(extraction["formats"])==17
    assert 'memory-wall-contents.json' in (site/"assets/memory-wall-guides.js").read_text()
    print("A7 PUBLISHED MEMORY WALL TOC PASS 7_links=1 7_targets=1 static_nojs=1 homepage_entry=1 built_sha="+args.commit_sha[:12])
if __name__=="__main__": main()
