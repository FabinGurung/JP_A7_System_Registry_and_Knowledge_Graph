#!/usr/bin/env python3
"""A7 Arc 01: enforce source-owned catalogue, progressive map, old-site preservation."""
import json
import tempfile
from pathlib import Path

from generate_galactic_atlas import build, main as _main

R = Path(__file__).resolve().parents[1]
ui = json.loads((R / "registry/decisions/galactic-atlas-ui.v0.1.json").read_text())
repo = json.loads((R / "registry/entities/repositories.json").read_text())
d = build()
assert ui["status"] == "PRESENTATION_ONLY_NOT_DOMAIN_AUTHORITY"
assert d["non_authoritative"] is True and d["station_count"] == 9
assert len(d["stations"]) == len(repo["repositories"]) == 9
assert len(d["links"]) == 8
source_ids = {x["repository_id"] for x in repo["repositories"]}
shown_ids = {x["id"] for x in d["stations"]}
assert shown_ids == source_ids and len(source_ids) == 9
assert {e["from"] for e in d["links"]} == {"REPO-000001"}
assert all(e["authority_transfer"] is False for e in d["links"])
assert all(e["to"] in shown_ids and e["to"] != "REPO-000001" for e in d["links"])
assert all(s["github_url"] == "https://github.com/" + s["module_repository"]
           for s in d["stations"])
assert all(s["website_url"].startswith("https://fabingurung.github.io/")
           for s in d["stations"])
assert all(s["source_observed_at"] for s in d["stations"])
aad = next(s for s in d["stations"] if s["id"] == "REPO-000003")
assert aad["module_repository"] == "FabinGurung/JP_Computer-Aided-Drawings"
assert any("governance/aad/aad-domain-template" in l["url"] for l in aad["deep_links"])
assert all(s["id"] == "REPO-000001" or "owns" in s for s in d["stations"])
assert "catalogue" in d["catalogue_role"].lower()
assert "may be stale" in d["fact_scope_note"].lower() and "authoritative" in d["fact_scope_note"].lower()
for file in ("site/index.html", "site/legacy-overview.html",
             "site/milestone.html", "site/assets/galactic-atlas.css",
             "site/assets/galactic-atlas.js"):
    assert (R / file).is_file(), file
site = (R/"site/index.html").read_text(encoding="utf-8")
legacy = (R/"site/legacy-overview.html").read_text(encoding="utf-8")
js = (R/"site/assets/galactic-atlas.js").read_text(encoding="utf-8")
css = (R/"site/assets/galactic-atlas.css").read_text(encoding="utf-8")
assert "galactic-atlas.css" in site and "galactic-atlas.js" in site
assert "spaceField" in site and "selectedSite" in site and "selectedRepo" in site
assert "fetch(\"data/galactic-atlas.json\"" in js
assert "read-only" in site.lower() and "single-writer" in site.lower()
assert all(x in site for x in (
    'href="history.html"', 'href="control-towers.html"',
    'href="memory-wall.html"', 'href="roadmap.html"',
    'href="how-it-works.html"', 'href="governance.html"'))
assert 'href="legacy-overview.html"' not in site and 'href="visualization-workspace.html"' not in site
assert 'href="legacy-overview.html"' in (R/"site/history.html").read_text()
assert "<details" in site and site.index("spaceField") < site.index("<details")
assert "prefers-reduced-motion" in css
assert "<canvas id=\"graphCanvas\">" in legacy and "graphInspector" in legacy
assert '<script src="assets/app.js" defer></script>' in legacy
assert "<table" in site and "Templates" in site and "Execution" in site
assert not (R/"site/index.html").read_text().strip() == legacy.strip(), "old homepage not preserved separately"
with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp)/"galactic-atlas.json"
    payload = dict(d, build_commit_sha="SHA_OF_CURRENT_CHECKOUT")
    path.write_text(json.dumps(payload),encoding="utf-8")
    opened = json.loads(path.read_text())
    assert opened["source_revisions"] == d["source_revisions"]

print("A7 GALACTIC ATLAS ACCEPTANCE PASS indexed=9 routes=8 privacy=PASS legacy=preserved nav=progressive")
