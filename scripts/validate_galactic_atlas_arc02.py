#!/usr/bin/env python3
"""A7 Galactic Atlas Arc 02: provider-sourced evidence and non-approval guard."""
import json
from pathlib import Path
import sys
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/"scripts"))
from generate_galactic_atlas import build
source=R/"registry/providers/galactic-atlas-arc02-observation-20261020.json"
o=json.loads(source.read_text())
catalog=json.loads((R/"registry/entities/repositories.json").read_text())
data=build()
assert o["status"]=="DATED_SNAPSHOT_NOT_LIVE_MONITOR"
assert o["deployed_does_not_mean_approved"] and not o["private_data_included"]
assert len(o["records"])==9 and len({x["id"] for x in o["records"]})==9
assert {x["id"] for x in o["records"]}=={x["repository_id"] for x in catalog["repositories"]}
assert data["provider_snapshot_not_live"] and data["non_authoritative"]
assert data["provider_observation_date"]=="2026-10-20"
assert data["arc"]=="GALACTIC_ATLAS_ARC_02_INSPECTOR"
assert len(data["stations"])==9 and len(data["links"])==8
assert "registry/providers/galactic-atlas-arc02-observation-20261020.json" in data["source_revisions"]
byid={x["id"]:x for x in o["records"]}
for station in data["stations"]:
 x=byid[station["id"]];e=station["provider_evidence"];p=x["deployment"]
 assert x["slug"]==station["module_repository"].split("/",1)[1]
 assert len(e["main_sha"])==len(p["sha"])==40
 assert e["last_successful_publication"]["result"]=="success"
 assert e["last_successful_publication"]["id"]==p["id"]
 assert e["last_successful_publication"]["branch"]==e["publication_branch"]
 assert e["dependency_verified"] is False
 assert "approved" not in e["provider_label"].lower()
 assert all(e[k] for k in ("capability","owner_gate","dependency_note","publication_branch"))
 assert x["latest_check"]["id"]>0 and x["latest_check"]["result"] in ("success","failure","cancelled","in_progress")
assert byid["REPO-000007"]["latest_check"]["result"]=="failure"
assert byid["REPO-000008"]["latest_check"]["result"]=="in_progress"
assert byid["REPO-000006"]["deployment"]["result"]=="success"
assert byid["REPO-000004"]["deployment"]["branch"]!="main"
assert byid["REPO-000009"]["deployment"]["branch"]!="main"
html=(R/"site/index.html").read_text()
js=(R/"site/assets/galactic-atlas.js").read_text()
css=(R/"site/assets/galactic-atlas-arc02.css").read_text()
assert 'galactic-atlas-arc02.css' in html
for id in ("inspectorObservationDate","inspectorStatus","inspectorMainSha","inspectorPublishedBranch","inspectorDeployedSha","inspectorDeployedAt","inspectorProviderLinks","inspectorCapabilities","inspectorGate","inspectorDependency"):
 assert 'id="'+id+'"' in html
 assert '"'+id+'"' in js
assert 'new URL("control-towers.html"' in js and 'new URL("legacy-overview.html"' not in js
assert 'a.textContent=label+" ↗"' in js and 'a.rel="noopener noreferrer"' in js
assert 'arc02-evidence' in css and 'prefers-reduced-motion' in css
assert (R/"registry/dependencies/status.json").exists()
dependency=json.loads((R/"registry/dependencies/status.json").read_text())
assert not dependency["verified_dependencies"]
assert "A7-SEQ-000013" in byid["REPO-000001"]["gate"]
assert "portal deploy" in byid["REPO-000006"]["gate"]
print("A7 ARC02 PROVIDER INSPECTOR PASS stations=9 dated_snapshot=yes dependencies_asserted=0")
