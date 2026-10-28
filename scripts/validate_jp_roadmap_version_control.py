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
assert p["current_closed_sequence"]=="A7-SEQ-000039" and "pinned_task_ids" not in p
assert m["pre"].get("sha256")==hashlib.sha256((a/"000001_PRE_A7_SEQ_000040.json").read_bytes()).hexdigest()
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
assert post.is_file()
assert m["post"]["status"]=="PASS_AFTER_VALIDATION"
assert m["post"]["sha256"]==hashlib.sha256(post.read_bytes()).hexdigest()
assert m["final_closeout_checks"]["state"]=="VERIFIED"
assert m["final_closeout_checks"]["final_commit"]=="f690a94e5cafcc874ed7c2d9fdd10b21b3099da2"
assert m["final_closeout_checks"]["registry_run"]==40603070798
assert m["final_closeout_checks"]["pages_run"]==40603070677
pre2=a/"000002_PRE_A7_SEQ_000041.json"
assert pre2.is_file() and pre2.read_bytes()==post.read_bytes()
assert m["archive_ordinal"] in ("000002","000003")
assert m["latest_pre"]["path"]=="registry/archives/roadmap/000002_PRE_A7_SEQ_000041.json"
assert [e["phase"] for e in events][:2]==["PRE","POST"]
assert events[2]["phase"]=="VERIFY" and events[3]["phase"]=="PRE"
post2=a/"000002_POST_A7_SEQ_000041.json"
if post2.exists():
    assert m["status"] in ("POST_000002_VALIDATED_ARCHIVED","PRE_000003_CAPTURED_POST_PENDING","POST_000003_VALIDATED_ARCHIVED")
    if m["archive_ordinal"]=="000002": assert post2.read_bytes()==live.read_bytes()
    else: assert (a/"000003_PRE_A7_SEQ_000042.json").is_file()
    assert m["latest_post"]["sha256"]==hashlib.sha256(post2.read_bytes()).hexdigest()
    assert any(e["phase"]=="POST" and e["sequence"]=="A7-SEQ-000041" for e in events)
    # Later provider evidence verification must never overwrite or remove the original POST.
    assert events[-1]["phase"] in ("POST","VERIFY","PRE")
else:
    assert m["status"]=="PRE_000002_CAPTURED_POST_PENDING"
    assert m["latest_post"]["status"]=="AWAITING_LIVE_QA"
# Provider-backed SEQ41 final-main evidence; independent site HTTP remains distinct.
close=m.get("final_seq41_closeout_checks")
assert close["state"]=="VERIFIED" and close["verified_against_main_commit"]=="c4baaf8ff7dfcf9884f09e547e7babc3593be642"
assert (close["registry_run"],close["pages_run"],close["release_safeguard_run"])==(40639913059,40639913026,40639983824)
assert close["independent_http_body_readback"] is False
archive=m["seq41_manifest_evidence_archive"]
assert archive["source_path"]=="registry/archives/roadmap/manifest.json"
assert (R/archive["pre"]).is_file()
post_manifest=R/archive["post"]
if post_manifest.exists():
    assert post_manifest.read_bytes()==(a/"manifest.json").read_bytes()
    assert events[-1]["phase"] in ("VERIFY","PRE","POST")
# The SEQ42 roadmap source remains one live ID; the new numbered snapshot is
# staged until feature Registry validation then must match the exact final source.
if m["archive_ordinal"]=="000003":
    p3=a/"000003_PRE_A7_SEQ_000042.json"
    assert p3.is_file() and json.loads(p3.read_text())["roadmap_id"]==s["roadmap_id"]
    q3=a/"000003_POST_A7_SEQ_000042.json"
    if q3.exists():
        assert m["status"]=="POST_000003_VALIDATED_ARCHIVED"
        assert q3.read_bytes()==live.read_bytes()
        assert m["latest_post"]["path"]=="registry/archives/roadmap/000003_POST_A7_SEQ_000042.json"
        assert m["latest_post"]["sha256"]==hashlib.sha256(q3.read_bytes()).hexdigest()
    else: assert m["status"]=="PRE_000003_CAPTURED_POST_PENDING"
print("JP A7 ROADMAP ARCHIVE PASS latest_stage="+("POST" if post2.exists() else "PRE")+" live_id=1 task_refs=3 previous_history_preserved=1")
