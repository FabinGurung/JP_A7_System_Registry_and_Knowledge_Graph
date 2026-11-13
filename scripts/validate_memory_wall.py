#!/usr/bin/env python3
"""Protect poster-wall design, link identity and public/owner boundary."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from generate_memory_wall import build

source=ROOT/"registry/curations/memory-posters.v0.1.json"
obj=json.loads(source.read_text(encoding="utf-8"))
assert obj["collection_id"]=="A7-MEM-WALL-EXTERNAL-REFERENCES-001"
assert obj["not_domain_authority"] and obj["not_new_owned_modules"] and obj["no_private_drive_identity"]
assert obj["curation_rules"]["poster_visible_at_rest"]
assert obj["curation_rules"]["no_flip"] and obj["curation_rules"]["no_quiz"]
assert len(obj["posters"])==3
assert len({p["id"] for p in obj["posters"]})==3
assert {c["id"] for c in obj["categories"]}=={"learning","integrations","frontend"}
expect={
 "MEM-EXT-0001":"nilbuild/developer-roadmap",
 "MEM-EXT-0002":"public-apis/public-apis",
 "MEM-EXT-0003":"sudheerj/reactjs-interview-questions"
}
for p in obj["posters"]:
    assert p["id"] in expect and p["repository"]==expect[p["id"]]
    assert p["url"]=="https://github.com/"+p["repository"]
    u=urlparse(p["url"])
    assert u.scheme=="https" and u.hostname=="github.com" and not u.query
    assert p["category"] in {c["id"] for c in obj["categories"]}
    assert p["status"]=="VERIFIED_PUBLIC_LINK_2026_10_20"
    for field in ("title","big_word","summary","remember","icon","theme","label"):
        assert p[field] and len(p[field])<175
assert "drive.google.com" not in source.read_text()
assert "docs.google.com" not in source.read_text()
d=build("FAKE_BUILD_SHA")
assert d["non_authoritative"] is True and len(d["posters"])==3
assert d["site_build_commit_sha"]=="FAKE_BUILD_SHA" and re.fullmatch("[0-9a-f]{64}",d["source_sha256"])
html=(ROOT/"site/memory-wall.html").read_text(encoding="utf-8")
css=(ROOT/"site/assets/memory-wall.css").read_text(encoding="utf-8")
js=(ROOT/"site/assets/memory-wall.js").read_text(encoding="utf-8")
assert 'memory-wall.css' in html and 'memory-wall.js' in html
assert 'data/memory-posters.json' in js
assert 'textContent' in js and 'createElement' in js
assert 'rel = "noopener noreferrer"' in js
assert "poster-card" in css and "@media print" in css
assert 'prefers-reduced-motion' in css
assert 'href="memory-wall.html"' in (ROOT/"site/index.html").read_text()
assert 'href="memory-wall.html"' in (ROOT/"site/control-towers.html").read_text()
assert "scripts/generate_memory_wall.py" in (ROOT/".github/workflows/deploy-a7-pages.yml").read_text()
assert "scripts/validate_memory_wall.py" in (ROOT/".github/workflows/validate-registry.yml").read_text()
# Public-safe deferred work pin: same A7 page, separate from the seven reference chapters.
pinned_file=ROOT/"registry/curations/memory-wall-pinned-work.v0.1.json"
pinned_text=pinned_file.read_text(encoding="utf-8")
pin=json.loads(pinned_text)
assert pin["record_id"]=="A7-MEM-PIN-034-SOURCE-SHEETS-20261112"
assert pin["count_recorded"]==34 and pin["status"]=="DEFERRED_BY_USER"
assert pin["private_source_links_excluded"] and pin["is_domain_authority"] is False
assert pin["file_moves_approved"] is False and pin["auto_publish_approved"] is False
assert pin["tracking_issue"]=="https://github.com/FabinGurung/jp-site-operations/issues/36"
assert "drive.google.com" not in pinned_text and "docs.google.com" not in pinned_text
assert html.count('id="pinned-34-source-sheets"')==1
assert pin["tracking_issue"] in html
assert len(pin["related_owners"])==1 and pin["related_owners"][0]["repository"]=="FabinGurung/jp-estimating-and-boq"
assert pin["related_owners"][0]["source_memory_wall"] in html
assert "1_MYCZ98tsfmWgTn_-jQBU9OcdrygwC9nlE9BF1gWK2k" not in pinned_text
assert html.index('id="pinned-34-source-sheets"')<html.index('class="notice-board"')

print("A7 MEMORY WALL QA PASS: 3 public posters, 7 original chapters, deferred 34-source pin, owner-safe")
