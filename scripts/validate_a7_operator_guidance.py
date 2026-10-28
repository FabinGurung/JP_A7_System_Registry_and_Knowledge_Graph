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
    assert hist[-1]["phase"]=="POST"
else:
    assert manifest["status"]=="PRE_CAPTURED_POST_PENDING"
print("A7 CURRENT OPERATOR GUIDANCE PASS steps=7 historical_reference_preserved=1 stage="+("POST" if post.exists() else "PRE"))
