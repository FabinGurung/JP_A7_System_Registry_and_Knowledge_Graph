#!/usr/bin/env python3
"""Validate navigable public A7 control tower graph and privacy boundaries."""
import json
from pathlib import Path

R=Path(__file__).resolve().parents[1]
p="registry/controls/control-tower-map.json"
d=json.loads((R/p).read_text(encoding="utf-8"))
assert d["map_id"]=="A7-CONTROL-TOWER-MAP-001"
assert d["projection_policy"]=="PUBLIC_SAFE_READ_ONLY" and d["domain_authority"] is False
ids=[x["id"] for x in d["nodes"]]
assert len(ids)==len(set(ids)) and len(ids)>=18
assert {x["tier"] for x in d["nodes"]}=={"global","module","drive","library","artifact"}
assert {"rnd_repo","rnd_latex","rnd_presentation","library_main","library_local","a9_thesis","a9_presentation"}.issubset(set(ids))
for e in d["edges"]:
    assert e["source"] in ids and e["target"] in ids and e["relation"]
for n in d["nodes"]:
    assert "https://drive.google.com/" not in str(n) and "docs.google.com" not in str(n)
    assert "1jc6WIq" not in str(n) and "18NE0GI" not in str(n)
    if n["tier"] in ("drive","library"):assert not n.get("link"),"Private provider link leaked"
assert len(d["prioritized_roadmap"])>=6
html=(R/"site/control-towers.html").read_text(encoding="utf-8")
js=(R/"site/assets/control-towers.js").read_text(encoding="utf-8")
assert "control-towers.js" in html and "assets/sky-theme.css" in html
assert "data/control-tower-map.json" in js
assert 'href="control-towers.html"' in (R/"site/index.html").read_text(encoding="utf-8")
assert p in (R/"scripts/generate_visualizations.py").read_text(encoding="utf-8")
out=R/".a7-generated-test/control-tower-map.json"
assert out.exists()
o=json.loads(out.read_text(encoding="utf-8"))
assert o["source_path"]==p and o["non_authoritative"] is True
assert len(o["nodes"])==len(ids) and o["source_commit_sha"]
print("A7 CONTROL TOWER NAVIGATION: PASS nodes=%d edges=%d privacy=PASS"%(len(ids),len(d["edges"])))
