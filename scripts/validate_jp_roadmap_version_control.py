#!/usr/bin/env python3
"""Verify A7 canonical roadmap, dedicated PRE/POST snapshots and user-authorized boundaries."""
import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
a=R/"registry/archives/roadmap"
live=R/"registry/roadmap.json"
data=lambda x:json.loads(x.read_text(encoding="utf-8"))
s,p,m=data(live),data(a/"000001_PRE_A7_SEQ_000040.json"),data(a/"manifest.json")
assert s["roadmap_id"]==p["roadmap_id"]==m["subject_id"]=="A7-ROADMAP-20261009"
assert "pinned_task_ids" not in p and p["current_closed_sequence"]=="A7-SEQ-000039"
assert s["pinned_task_ids"]==["A7-N05","A7-N10","A7-N04"]
assert set(s["pinned_task_ids"]).issubset({x["id"] for x in s["next"]})
assert s["pin_semantics"]["A7-N04"]["boundary"]=="PEER_READ_ONLY_HOLD"
assert s["version_control"]["live_path"]=="registry/roadmap.json"
assert m["live_source_path"]=="registry/roadmap.json"
assert m["original_message"]["source_url"] is None and not m["original_message"]["public_copy"]
events=[json.loads(x) for x in (a/"version-history.jsonl").read_text().splitlines() if x.strip()]
assert len(events)==len(set(x["event_id"] for x in events))
assert events[0]["phase"]=="PRE" and all(x["subject_id"]==s["roadmap_id"] for x in events)
assert all("why" in x and "evidence" in x and "validation" in x and "restoration" in x for x in events)
post=a/"000001_POST_A7_SEQ_000040.json"
if post.exists():
 assert m["status"]=="POST_VALIDATED_ARCHIVED" and post.read_bytes()==live.read_bytes()
 assert m["post"]["status"]=="PASS_AFTER_VALIDATION"
 assert m["post"]["sha256"]==hashlib.sha256(live.read_bytes()).hexdigest()
 assert events[-1]["phase"]=="POST" and events[-1]["validation"]=="CI_FEATURE_SUCCESS_AND_SOURCE_BYTE_READBACK"
else:
 assert m["status"]=="PRE_CAPTURED_POST_PENDING" and m["post"]["status"]=="AWAITING_VALIDATION"
print("JP A7 ROADMAP ARCHIVE PASS stage="+("POST" if post.exists() else "PRE")+" single_live_id=1 task_refs=3")
