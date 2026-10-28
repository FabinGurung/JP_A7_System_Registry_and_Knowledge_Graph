#!/usr/bin/env python3
"""Verify L1 A7 roadmap source provenance and navigation contract."""
import json,sys,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/"scripts"))
from generate_a7_roadmap import build
D=build("CI_LOCAL_SOURCE")
S=json.loads((R/"registry/roadmap.json").read_text())
assert D["current_closed_sequence"]==S["current_closed_sequence"]
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
assert 'id="roadmap-evidence"' in h and 'id="roadmapEvidence"' in h
assert "verified_a7_provider_evidence" in js and "historical_not_live" in js
assert 'id="roadmapUpcoming"' in h and 'id="roadmapPinned"' in h and 'data/a7-roadmap.json' in js
assert 'd.next_a7.filter(x=>!pinnedIds.has(x.id))' in js
assert "textContent" in js and "innerHTML" not in js
assert "21</strong>Last fully closed" not in h
assert "R&D" not in h and "A9" not in h
print("A7 L1 ROADMAP SOURCE QA PASS closed="+D["current_closed_sequence"])
