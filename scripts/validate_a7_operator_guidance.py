#!/usr/bin/env python3
"""Existing A7 How It Works: current source-driven operator guide + preserved historical CAD example."""
from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/"site/how-it-works.html").read_text(encoding="utf-8")
a=ROOT/"registry/archives/operator-guidance"
manifest=json.loads((a/"manifest.json").read_text())
pre=(a/"000001_PRE_A7_SEQ_000041.html").read_bytes()
assert manifest["subject_id"]=="A7-OPERATOR-HOW-IT-WORKS"
assert manifest["live_source_path"]=="site/how-it-works.html"
assert b"Historical how-to reference" in pre and b"AI-Aided Product Standard" in pre
assert html.count('id="a7-operator-quickstart"')==1
assert html.count('class="a7-oper-step"')==7
assert html.index('id="a7-operator-quickstart"')<html.index("Historical how-to reference")
for val in ("A7_BOOTSTRAP.json","A7_READ_FIRST.md","A7-N04","a7-operator","JP version control","PRE","POST","GitHub Actions","Developer Dock"):
    assert val in (html + (ROOT/"docs/JP_A7_VERSION_CONTROL_READ_FIRST.md").read_text()), val
for path in ("A7_READ_FIRST.md","docs/JP_A7_VERSION_CONTROL_READ_FIRST.md"):
    assert path in html, path
for marker in ("Historical how-to reference","Try CAD language","Details that grow with your task","For developers and other AI agents"):
    assert marker in html, marker
hist=[json.loads(x) for x in (a/"version-history.jsonl").read_text().splitlines() if x.strip()]
assert hist[0]["phase"]=="PRE" and len({x["event_id"] for x in hist})==len(hist)
post=a/"000001_POST_A7_SEQ_000041.html"
if post.exists():
    assert manifest["status"]=="POST_VALIDATED_ARCHIVED"
    assert post.read_bytes()==html.encode()
    assert manifest["post"]["sha256"]==hashlib.sha256(post.read_bytes()).hexdigest()
    assert any(e["phase"]=="POST" for e in hist)
    assert hist[-1]["phase"] in ("POST","VERIFY")
else:
    assert manifest["status"]=="PRE_CAPTURED_POST_PENDING"
# SEQ41 final-main actions are verified; no served HTML or owner attestation is claimed.
boot=json.loads((ROOT/"A7_BOOTSTRAP.json").read_text())
final=boot["a7_operator_quickstart"]["final_closeout_evidence"]
assert boot["a7_operator_quickstart"]["final_closeout_ci"]=="VERIFIED_FINAL_MAIN_WORKFLOWS"
assert final==manifest["final_closeout_checks"]
assert (final["registry_run"],final["pages_run"],final["release_safeguard_run"])==(40639913059,40639913026,40639983824)
assert final["independent_http_body_readback"] is False
for pointer,current in ((manifest["seq41_manifest_evidence_archive"],a/"manifest.json"),):
    assert (ROOT/pointer["pre"]).is_file()
    if (ROOT/pointer["post"]).exists():
        assert (ROOT/pointer["post"]).read_bytes()==current.read_bytes()
        assert hist[-1]["phase"]=="VERIFY"
ba=ROOT/"registry/archives/a7-bootstrap"
bm=json.loads((ba/"manifest.json").read_text())
assert bm["live_source_path"]=="A7_BOOTSTRAP.json"
assert (ROOT/bm["pre_path"]).is_file()
if bm["archive_ordinal"] in ("000002","000003","000004","000005","000006"):
    assert (ROOT/bm["historical_000001"]["pre_path"]).is_file()
    assert (ROOT/bm["historical_000001"]["post_path"]).is_file()
if bm["archive_ordinal"] in ("000003","000004","000005","000006"):
    assert (ROOT/bm["historical_000002"]["pre_path"]).is_file()
    assert (ROOT/bm["historical_000002"]["post_path"]).is_file()
if bm["archive_ordinal"] in ("000004","000005","000006"):
    assert (ROOT/bm["historical_000003"]["pre_path"]).is_file()
    assert (ROOT/bm["historical_000003"]["post_path"]).is_file()
if bm["archive_ordinal"] in ("000005","000006"):
    assert (ROOT/bm["historical_000004"]["pre_path"]).is_file()
    assert (ROOT/bm["historical_000004"]["post_path"]).is_file()
if bm["archive_ordinal"]=="000006":
    assert (ROOT/bm["historical_000005"]["pre_path"]).is_file()
    assert (ROOT/bm["historical_000005"]["post_path"]).is_file()
if (ROOT/bm["post_path"]).exists():
    assert (ROOT/bm["post_path"]).read_bytes()==(ROOT/"A7_BOOTSTRAP.json").read_bytes()
print("A7 CURRENT OPERATOR GUIDANCE PASS steps=7 historical_reference_preserved=1 stage="+("POST" if post.exists() else "PRE"))
