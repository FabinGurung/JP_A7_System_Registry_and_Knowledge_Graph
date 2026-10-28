#!/usr/bin/env python3
"""Verify L1 A7 roadmap source provenance and navigation contract."""
import json,sys,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/"scripts"))
from generate_a7_roadmap import build, summarize_public_qa
D=build("CI_LOCAL_SOURCE")
S=json.loads((R/"registry/roadmap.json").read_text())
assert D["current_closed_sequence"]==S["current_closed_sequence"]

# Local governance projection: project aggregate metadata only, never source case content.
G=D["a7_governance"]; qa=G["qa"]; ext=G["external"]
assert qa["scope"]=="PUBLIC_A7_REGISTRY_ONLY"
assert qa["source_path"]=="registry/qa/human-qa-cases.jsonl"
assert qa["source_sha256"]==__import__("hashlib").sha256((R/qa["source_path"]).read_bytes()).hexdigest()
assert qa["no_records_in_public_source"] is (not (R/qa["source_path"]).read_bytes().strip())
assert 0 <= qa["active"] <= qa["cases"] <= qa["records"]
assert ext["scope"]=="EXTERNAL_NON_GATE__DATED_NOT_LIVE"
assert ext["source_sha256"]==__import__("hashlib").sha256((R/ext["source_path"]).read_bytes()).hexdigest()
ledger=json.loads((R/ext["source_path"]).read_text())
assert ext["count"]==len(ledger["external_non_gate_dependencies"])==len(ext["entries"])
assert all(k in x for x in ext["entries"] for k in ("id","status","why_not_closed","gate"))
sample=b'{"qa_case_id":"A7-QA-000001","status":"AWAITING_HUMAN"}\n{"qa_case_id":"A7-QA-000001","status":"RESOLVED"}\n'
s=summarize_public_qa(sample,{"AWAITING_HUMAN","RESOLVED"})
assert (s["records"],s["cases"],s["active"],s["resolved"])==(2,1,0,1)
try:
    summarize_public_qa(b'{"qa_case_id":"A7-QA-000002","status":"UNKNOWN"}\n',{"RESOLVED"})
except ValueError: pass
else: raise AssertionError("Unknown QA status was accepted")

# The evidence projection must be derived from bootstrap, not a duplicate editable log.
boot=json.loads((R/"A7_BOOTSTRAP.json").read_text())
e=boot["a7_operator_quickstart"]["final_closeout_evidence"]
proof=D["verified_a7_provider_evidence"]
assert proof["sequence"]==boot["a7_operator_quickstart"]["sequence_id"]
assert proof["verified_commit_sha"]==e["verified_against_main_commit"]
assert (proof["registry_run"],proof["pages_run"],proof["release_safeguard_run"])==(e["registry_run"],e["pages_run"],e["release_safeguard_run"])
assert proof["historical_not_live"] is True and proof["independent_http_body_readback"] is False
assert D["kind"]=="DERIVED_NOT_AUTHORITATIVE" and D["owner"]=="A7_ONLY"
assert D["developed"]==[{k:x.get(k) for k in ("id","stage","title","status","detail")} for x in S["developed"]]
assert {x["id"] for x in D["next_a7"]}=={"A7-N04","A7-N05","A7-N06","A7-N10","A7-N13"}
assert [x["id"] for x in D["pinned_a7"]]==S["pinned_task_ids"]==["A7-N05","A7-N10","A7-N04"]
assert D["pinned_a7"][-1]["task_boundary"]=="PEER_READ_ONLY_HOLD"
assert re.fullmatch(r"[0-9a-f]{64}",D["source_sha256"])
h=(R/"site/roadmap.html").read_text();js=(R/"site/assets/a7-roadmap.js").read_text()
assert 'id="roadmapSequence"' in h and 'id="roadmapDeveloped"' in h
assert 'id="roadmap-governance"' in h and 'id="roadmapGovernance"' in h
assert 'a7_governance' in js and 'PUBLIC_A7_REGISTRY_ONLY' in js
assert 'id="roadmap-evidence"' in h and 'id="roadmapEvidence"' in h
assert "verified_a7_provider_evidence" in js and "historical_not_live" in js
assert 'id="roadmapUpcoming"' in h and 'id="roadmapPinned"' in h and 'data/a7-roadmap.json' in js
assert 'd.next_a7.filter(x=>!pinnedIds.has(x.id))' in js
assert "textContent" in js and "innerHTML" not in js
assert "21</strong>Last fully closed" not in h
assert "R&D" not in h and "A9" not in h
# The numbered POST is an exact archive of every live UI/code path,
# not a parallel editable registry. PRE retains original Git object identities.
archive=R/"registry/archives/roadmap-evidence-ui"
a=json.loads((archive/"000001_PRE_A7_SEQ_000042.json").read_text())
assert a["subject_id"]=="A7-ROADMAP-EVIDENCE-UI" and a["phase"]=="PRE"
assert len(a["live_sources"])==5
post=archive/"000001_POST_A7_SEQ_000042.json"
if post.exists():
    z=json.loads(post.read_text())
    assert z["phase"]=="POST" and z["subject_id"]==a["subject_id"]
    assert {x["path"] for x in z["live_sources"]}=={x["path"] for x in a["live_sources"]}
    # 000001 is an immutable past POST, not the newest live source.
    assert len(z["live_sources"])==5
m=json.loads((archive/"manifest.json").read_text())
if m["archive_ordinal"]=="000002":
    pre2=json.loads((archive/"000002_PRE_A7_SEQ_000043.json").read_text())
    assert pre2["phase"]=="PRE" and len(pre2["live_sources"])==5
    post2=archive/"000002_POST_A7_SEQ_000043.json"
    if post2.exists():
        latest=json.loads(post2.read_text())
        assert latest["phase"]=="POST"
        assert {x["path"] for x in latest["live_sources"]}=={x["path"] for x in pre2["live_sources"]}
        assert all((R/x["path"]).read_text(encoding="utf-8")==x["content"] for x in latest["live_sources"])
print("A7 L1 ROADMAP SOURCE QA PASS closed="+D["current_closed_sequence"])
