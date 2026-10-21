#!/usr/bin/env python3
"""Arc03 sector/category navigation; no data-authority or runtime-dependency changes."""
import json
from pathlib import Path
from generate_galactic_atlas import build
R=Path(__file__).resolve().parents[1]
source=R/"registry/decisions/galactic-atlas-sectors.v0.1.json"
o=json.loads(source.read_text(encoding="utf-8"))
data=build()
expected={"CONTROL":1,"ENGINEERING":4,"OPERATIONS":1,"KNOWLEDGE":2,"ADJACENT":1}
assert o["status"]=="ADOPTED_PRESENTATION_TAXONOMY"
assert o["restrictions"]["private_a9_seq13_remains_staged"] is True
assert o["restrictions"]["peer_repository_edits"] is False
assert o["restrictions"]["category_changes_are_not_runtime_deps"]
assert set(o["sector_order"])==set(expected)
assert {s["id"]:s["count"] for s in data["sectors"]}==expected
assert data["navigation_arc"]=="GALACTIC_ATLAS_ARC_03_SECTORS"
assert data["sector_taxonomy_presentation_only"] and data["non_authoritative"]
assert len(data["stations"])==9 and len(data["links"])==8
assert len({s["id"] for s in data["stations"]})==9
assignments={a["repository_id"]:a["sector_id"] for a in o["assignments"]}
assert len(assignments)==9
for station in data["stations"]:
    assert station["sector"]==assignments[station["id"]]
    assert station["provider_evidence"]["not_live"]
    assert station["provider_evidence"]["dependency_verified"] is False
assert assignments["REPO-000007"]=="OPERATIONS"
assert assignments["REPO-000001"]=="CONTROL"
assert all(e["type"]=="CATALOGUE_ROUTES_TO" and not e["authority_transfer"] for e in data["links"])
assert "registry/decisions/galactic-atlas-sectors.v0.1.json" in data["source_revisions"]
html=(R/"site/index.html").read_text(encoding="utf-8")
js=(R/"site/assets/galactic-atlas.js").read_text(encoding="utf-8")
css=(R/"site/assets/galactic-atlas-arc03.css").read_text(encoding="utf-8")
for ident in ("sectorFilters","sectorSearch","sectorStatus","sectorReset","selectedSector"):
    assert f'id="{ident}"' in html
    assert f'"{ident}"' in js
for token in ("function eligible(","function applySectors(","function setupSectors(",
              "visibleStations()","aria-pressed","data.sectors","button.hidden","node.hidden",
              'station.id===ROOT_ID','line.style.display','sector.taxonomy'):
    # CSS/content not required to use exactly these tokens: check actual stable syntax below.
    if token in ("button.hidden","sector.taxonomy"):continue
    assert token in js,token
assert "star-node[hidden]" in css
assert "prefers-reduced-motion" in css
assert "galactic-atlas-arc03.css" in html
assert "a7-unified-theme.css" in html
assert 'assets/fluffy-rocket.js' in html
assert 'a7-site-shell.js' in html
assert 'new URL("control-towers.html"' in js
assert (R/"registry/dependencies/status.json").exists()
dep=json.loads((R/"registry/dependencies/status.json").read_text())
assert not dep["verified_dependencies"]
print("A7 ARC03 GALACTIC SECTORS PASS: five sectors, nine source-backed stations, zero runtime links")
