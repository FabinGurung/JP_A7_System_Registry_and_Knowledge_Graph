#!/usr/bin/env python3
"""Collection 05 semantics, privacy, rendering and Collections 01–04 preservation."""
import json
import re
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/"scripts"))
from generate_memory_storage_architecture import build

d = build("LOCAL_TEST_SHA")
assert d["schema_version"] == "1.0.0"
assert d["collection_number"] == 5 and d["sequence_id"] == "A7-SEQ-000035"
assert d["collection_id"] == "A7-MEM-STORAGE-ARCH-007"
assert d["kind"] == "DERIVED_PUBLIC_OPERATING_REFERENCE"
assert d["status"] == "VERSIONED_GUIDANCE_NOT_IMPLEMENTATION_PROOF"
assert re.fullmatch(r"[a-f0-9]{64}",d["source_sha256"])
assert d["site_build_commit"] == "LOCAL_TEST_SHA"
assert d["source_scope"] == "A7_ONLY_REFERENCE__OTHER_PROVIDERS_UNCHANGED"
assert [x["id"] for x in d["formats"]] == ["sql","jsonl","sqlite","json","csv","sheets","drive"]
assert [x["id"] for x in d["distinctions"]] == ["originals","relationships","presentation"]
assert all(len(x["responsibility"])>15 and len(x["qualification"])>25 for x in d["formats"])
assert "permissions" in d["principle"] and "approved" in d["principle"]
assert "foreign keys" in d["rule"] and "indexes" in d["rule"] and "modules" in d["rule"]
assert "private" in d["privacy"] and "not a claim" in d["policy"]
source=json.dumps(d).lower()
for forbidden in ("drive.google.com/","docs.google.com/","a9_fabin_gurung","1ddz-gevq","https://drive.google"):
    assert forbidden not in source, forbidden
html=(R/"site/memory-wall.html").read_text()
assert html.count('id="storage-only-architecture"') == 1
assert html.index('id="platform-role-board"') < html.index('id="interface-vocabulary"') < html.index('id="storage-only-architecture"') < html.index('id="extraction-retrieval"')
for x in ("storageArchFlow","storageArchRows","storageArchStatus","storageArchRule"):
    assert 'id="'+x+'"' in html,x
assert html.count('assets/memory-storage-architecture.js')==1
assert html.count('assets/memory-storage-architecture.css')==1
js=(R/"site/assets/memory-storage-architecture.js").read_text()
css=(R/"site/assets/memory-storage-architecture.css").read_text()
assert "data/memory-storage-architecture.json" in js and "textContent" in js and "innerHTML" not in js
assert "@media print" in css and "@media(max-width:" in css
assert "border-collapse" in css
assert len(json.loads((R/"registry/curations/memory-posters.v0.1.json").read_text())["posters"]) == 3
assert len(json.loads((R/"registry/curations/memory-ui-vocabulary.v0.1.json").read_text())["terms"]) == 13
assert len(json.loads((R/"registry/curations/platform-responsibilities.v0.1.json").read_text())["entries"]) == 8
for name in ("validate-registry.yml","deploy-a7-pages.yml","a7-browser-qa.yml"):
    assert "memory_storage_architecture" in (R/".github/workflows"/name).read_text()
print("A7 MEMORY STORAGE QA PASS fifth_collection=1 seven_formats=1 privacy=1 previous_collections_preserved=1")
