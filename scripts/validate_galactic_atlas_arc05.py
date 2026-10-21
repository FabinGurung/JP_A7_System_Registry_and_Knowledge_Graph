#!/usr/bin/env python3
"""Arc05: immutable provider-linked release-history projection, no synthetic tags."""
import json
from pathlib import Path
from generate_galactic_atlas import build
ROOT=Path(__file__).resolve().parents[1]
data=build()
src=ROOT/"registry/decisions/galactic-atlas-arc05-history.v0.1.json"
dec=json.loads(src.read_text(encoding="utf-8"))
assert dec["status"]=="ADOPTED_DATED_HISTORY_PROJECTION"
assert dec["restrictions"]["no_fake_tags"]
assert dec["restrictions"]["private_a9_artifact_ids"] is False
assert dec["restrictions"]["runtime_dependency_assertions"]==0
assert data["history_arc"]=="GALACTIC_ATLAS_ARC_05_IMMUTABLE_RELEASE_HISTORY"
assert data["history_event_count"]==6 and data["peer_publication_count"]==8
assert len(data["stations"])==9 and data["sector_count"]==5
assert data["route_count"]==4 and data["candidate_count"]==4
assert data["verified_runtime_handoff_count"]==0
assert data["provider_snapshot_not_live"] and data["non_authoritative"]
assert len({e["id"] for e in data["history"]+data["peer_publications"]})==14
assert sum(x["kind"]=="VERIFIED_GITHUB_RELEASE_TAG" for x in data["history"])==1
assert sum(x["kind"]=="VERIFIED_A7_EVENT_RELEASE" for x in data["history"])==5
assert {x["station_id"] for x in data["peer_publications"]}=={x["id"] for x in data["stations"]}-{"REPO-000001"}
records={json.loads(line)["event_id"]:json.loads(line) for line in (ROOT/"registry/events/a7-mutations.jsonl").read_text().splitlines() if line.strip()}
for m in dec["admitted_milestones"]:
    source=records[m["acceptance_event_id"]]
    projected=next(x for x in data["history"] if x["id"]==source["event_id"])
    assert source["status"]=="VALIDATED_PASS" and source["sequence_id"]==m["sequence_id"]
    assert projected["commit_sha"] in projected["commit_url"]
    assert len(projected["commit_sha"])==40
    assert projected["run_ci_url"].startswith("https://github.com/FabinGurung/")
    assert projected["run_pages_url"].startswith("https://github.com/FabinGurung/")
    assert projected["evidence_url"].find(dec["source_commit_sha"])>=0
    assert projected["kind"]=="VERIFIED_A7_EVENT_RELEASE"
for peer in data["peer_publications"]:
    assert peer["kind"]=="DATED_PEER_PUBLICATION_SNAPSHOT"
    assert len(peer["commit_sha"])==40 and peer["run_pages_url"]
    assert "snapshot" in peer["limitation"].lower()
assert all("GDRIVE-" not in json.dumps(x) and "drive.google.com" not in json.dumps(x) for x in data["history"]+data["peer_publications"])
for p in ("registry/decisions/galactic-atlas-arc05-history.v0.1.json","registry/events/a7-mutations.jsonl"):
    assert p in data["source_revisions"]
html=(ROOT/"site/index.html").read_text()
js=(ROOT/"site/assets/galactic-atlas-arc05.js").read_text()
css=(ROOT/"site/assets/galactic-atlas-arc05.css").read_text()
browser=(ROOT/"scripts/a7_browser_qa.cjs").read_text()
for token in ('id="release-constellations"','id="arc05HistoryList"','id="arc05HistoryInspector"','id="arc05HistoryCount"','galactic-atlas-arc05.css','galactic-atlas-arc05.js'):
    assert token in html,token
for token in ("a7:station-selected","VERIFIED_A7_EVENT_RELEASE","arc05HistoryList","noopener noreferrer","source-linked"):
    assert token in js or token in html,token
assert "arc05HistoryInspector" in browser
assert "@media(max-width:760px)" in css and "prefers-reduced-motion" in css
print("A7 ARC05 HISTORICAL CONSTELLATIONS PASS true_tags=1 milestone_events=5 peer_snapshots=8 private_ids=0")
