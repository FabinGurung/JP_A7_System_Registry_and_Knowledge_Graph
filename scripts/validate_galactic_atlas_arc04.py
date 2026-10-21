#!/usr/bin/env python3
"""Arc04: only canonical, referenced module NAVIGATION edges plus optional proposals."""
import json
from pathlib import Path
from generate_galactic_atlas import build
R=Path(__file__).resolve().parents[1]
D=R/"registry/decisions/galactic-atlas-arc04-routes.v0.1.json"
decision=json.loads(D.read_text(encoding="utf-8"))
projection=build()
source_edges={}
for line,raw in enumerate((R/"registry/edges/edges.jsonl").read_text(encoding="utf-8").splitlines(),1):
    if raw.strip():
        edge=json.loads(raw);source_edges[edge["edge_id"]]=(edge,line)
assert decision["status"]=="ADOPTED_PUBLIC_PRESENTATION_ONLY"
assert decision["admitted_canonical_edge_type"]=="LINKS_TO_PEER_MODULE"
assert decision["boundaries"]["proposals_are_not_canonical_edges"]
assert not decision["boundaries"]["private_a9_admission"]
assert not decision["boundaries"]["peer_repositories_modified"]
assert projection["relationship_arc"]=="GALACTIC_ATLAS_ARC_04_EVIDENCE_GATED_ROUTES"
assert projection["navigation_arc"]=="GALACTIC_ATLAS_ARC_03_SECTORS"
assert projection["arc"]=="GALACTIC_ATLAS_ARC_02_INSPECTOR"
assert projection["non_authoritative"] and projection["provider_snapshot_not_live"]
assert projection["station_count"]==9 and len(projection["links"])==8
assert len(projection["sectors"])==5 and projection["sector_count"]==5
assert len(projection["routes"])==projection["route_count"]==4
assert len(projection["candidate_routes"])==projection["candidate_count"]==4
assert projection["verified_runtime_handoff_count"]==0
assert not json.loads((R/"registry/dependencies/status.json").read_text())["verified_dependencies"]
assert set(decision["admitted_edge_ids"])=={e["id"] for e in projection["routes"]}
modules=json.loads((R/"registry/entities/modules.json").read_text())["modules"]
module_repo={m["module_id"]:m["repository_id"] for m in modules}
ids={s["id"] for s in projection["stations"]}
assert len(ids)==9 and len(module_repo)==7
seen=set()
for route in projection["routes"]:
    assert route["id"] not in seen
    seen.add(route["id"])
    edge,line=source_edges[route["id"]]
    assert edge["relation_type"]==route["relation_type"]=="LINKS_TO_PEER_MODULE"
    assert route["from"]==module_repo[edge["from_entity_id"]]
    assert route["to"]==module_repo[edge["to_entity_id"]]
    assert route["evidence_observed_at"]==edge["observed_at"]
    assert route["evidence_url"].endswith("/registry/edges/edges.jsonl#L"+str(line))
    assert decision["source_commit_sha"] in route["evidence_url"]
    assert route["verification"]=="DOCUMENTED_NAVIGATION_ONLY"
    assert route["runtime_verified"] is False and route["authority_transfer"] is False
    assert route["from"] in ids and route["to"] in ids and route["from"]!=route["to"]
    assert all(not str(v).startswith("GDRIVE-") for v in route.values() if isinstance(v,str))
proposal_ids=set()
for route in projection["candidate_routes"]:
    assert route["id"] not in seen and route["id"] not in proposal_ids
    proposal_ids.add(route["id"])
    assert route["verification"]=="PROPOSED_UNVERIFIED"
    assert route["relation_type"]=="CANDIDATE_INTEGRATION"
    assert route["evidence_url"] is None and route["source_commit_sha"] is None
    assert route["runtime_verified"] is False and route["authority_transfer"] is False
    assert route["from"] in ids and route["to"] in ids and route["from"]!=route["to"]
    assert not any(edge["from_entity_id"]==route["from"] and edge["to_entity_id"]==route["to"] for edge,_ in source_edges.values())
assert {"registry/edges/edges.jsonl","registry/entities/modules.json",
"registry/decisions/galactic-atlas-arc04-routes.v0.1.json"}.issubset(projection["source_revisions"])
html=(R/"site/index.html").read_text()
js=(R/"site/assets/galactic-atlas-arc04.js").read_text()
base=(R/"site/assets/galactic-atlas.js").read_text()
css=(R/"site/assets/galactic-atlas-arc04.css").read_text()
for attr in ['id="arc04Lines"','id="arc04RouteList"','id="arc04Inspect"',
'id="arc04Type"','id="arc04IncludeProposals"','id="interstellar-routes"']:
    assert attr in html
assert 'galactic-atlas-arc04.css' in html and 'galactic-atlas-arc04.js' in html
assert 'a7:station-selected' in base and 'dataset.repoId' in base
for token in ("DOCUMENTED / NAVIGATION ONLY","PROPOSED / UNVERIFIED",
"arc04IncludeProposals","aria-pressed","MutationObserver","isSafe","prefers-reduced-motion"):
    assert token in js or token in css,token
assert "pointer-events:none" in css and "@media(max-width:750px)" in css
assert 'assets/fluffy-rocket.js' in html and 'a7-unified-theme.css' in html
assert 'id="sectorFilters"' in html and 'id="selectedSector"' in html
assert not any(x in (html+js+css) for x in ("drive.google.com/drive/folders/","GDRIVE-ROOT-"))
print("A7 ARC04 ROUTES PASS navigation=4 proposals=4 verified_runtime=0 sectors=5 stations=9")
