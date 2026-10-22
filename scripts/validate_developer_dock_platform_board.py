#!/usr/bin/env python3
"""A7 developer dock + beautiful Memory Wall platform matrix release contract."""
import re,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"scripts"))
from generate_a7_developer_dock import build as dock
from generate_platform_responsibilities import build as roles
d=dock("a"*40);p=roles("a"*40)
assert d["collection_id"]=="A7-DEV-DOCK-001" and d["non_authoritative"] is True
assert len(d["groups"])==5 and sum(len(g["items"]) for g in d["groups"])>=15
assert all(item["source_url"].startswith("https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph/blob/"+"a"*40+"/") for g in d["groups"] for item in g["items"])
assert len(p["entries"])==7 and len({i["id"] for i in p["entries"]})==7
assert p["provider_claims_are_not_approval"] is True and p["optional_services_require_explicit_adoption"] is True
assert "IFC parser" in p["example"] and "engineering" in p["actions_hint"]
html=(R/"site/developer-dock.html").read_text()
memory=(R/"site/memory-wall.html").read_text()
assert 'id="dockGroups"' in html and 'id="dockSearch"' in html and 'a7-developer-dock.js' in html
assert 'id="platform-role-board"' in memory and 'id="platformRows"' in memory
assert 'role="table"' not in memory # real semantic table, not a div imitation
assert "<table" in memory and 'platform-responsibilities.js' in memory
assert "github.com/FabinGurung" not in json.dumps(p)
shell=(R/"site/assets/a7-site-shell.js").read_text()
assert '["developer-dock.html","Developer Dock"' in shell
assert 'memory-wall.html#platform-role-board' in html
assert "data/a7-developer-dock.json" in (R/"site/assets/a7-developer-dock.js").read_text()
assert "data/platform-responsibilities.json" in (R/"site/assets/platform-responsibilities.js").read_text()
print("A7 DEVELOPER DOCK + PLATFORM MEMORY MATRIX PASS groups=5 original_repo_only=1 rows=7")
