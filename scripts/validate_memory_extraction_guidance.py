#!/usr/bin/env python3
"""Memory Wall ToC + Collection 06 contract acceptance: public scope, evidence and original 01–05 preservation."""
import json
import re
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from generate_memory_extraction_guidance import build

toc,d=build("SYNTHETIC_BUILD")
assert toc["collection_count"]==6 and len(toc["collections"])==6
assert toc["collections"][0]["title"]=="Developer Learning Toolkit"
assert toc["collections"][0]["subtitle"].startswith("Learn a path")
assert len(toc["presentation_refinement"]["source_refs"])==3
assert [c["number"] for c in toc["collections"]]==list(range(1,7))
assert [c["anchor"] for c in toc["collections"]]==[
 "posters","visualization-reminders","platform-role-board","interface-vocabulary","storage-only-architecture","extraction-retrieval"
]
assert [c["id"] for c in toc["collections"]]==[
 "A7-MEM-WALL-EXTERNAL-REFERENCES-001","A7-VIS-DEC-000001","A7-MEM-PLATFORM-ROLES-005",
 "A7-MEM-UI-VOCAB-006","A7-MEM-STORAGE-ARCH-007","A7-MEM-EXTRACTION-008"
]
assert re.fullmatch(r"[0-9a-f]{64}",toc["source_sha256"])
assert re.fullmatch(r"[0-9a-f]{64}",d["source_sha256"])
assert d["site_build_commit"]=="SYNTHETIC_BUILD" and toc["site_build_commit"]=="SYNTHETIC_BUILD"
assert d["sequence_id"]=="A7-SEQ-000036" and d["collection_number"]==6
assert d["status"]=="REFERENCE_CONTRACT_ONLY_NOT_DEPLOYED_INGESTION"
assert d["source_scope"]=="A7_ONLY__NO_EXTERNAL_FILES_FETCHED" and d["read_only"]
assert d["language_stack"]["primary"].startswith("Python")
assert len(d["pipeline"])==7 and len(d["formats"])==17 and len(d["groups"])==6
assert len(set(f["id"] for f in d["formats"]))==17
assert {f["group"] for f in d["formats"]}==set(d["groups"])
assert len(d["outputs"])==6 and len(d["evidence_fields"])>=16
assert {"native_locator","source_sha256","source_revision","extractor_version","verification_state","approval_state"}.issubset(d["evidence_fields"])
assert {"etabs","sap2000","cad-dwg","cad-dxf","dwc","pdf","spreadsheet","sheets","doc","shp","gdb","arcgis","skp","ifc"}.issubset({f["id"] for f in d["formats"]})
assert "Do not silently reinterpret DWC as DWG" in next(f["hold"] for f in d["formats"] if f["id"]=="dwc")
assert "does not prove" in d["safeguards"][1] and "not fabricated" in " ".join(d["safeguards"])
assert len(d["synthetic_example"])>=17 and d["synthetic_example"]["verification_state"]=="EXTRACTED_UNVERIFIED"
assert all(f["method"] and f["output"] and f["locator"] and f["hold"] for f in d["formats"])
for f in d["vendor_references"]:
    assert f["url"].startswith("https://") and len(f["label"])>3
html=(ROOT/"site/memory-wall.html").read_text(encoding="utf-8")
assert html.count('id="memory-wall-contents"')==1
assert html.count('id="extraction-retrieval"')==1
assert '<h2 id="board-title">Developer Learning Toolkit</h2>' in html
assert html.count('class="mw-chapter-return"')==5
assert "Room for more posters" not in html
assert html.index('id="memory-wall-contents"')<html.index('class="notice-board"')
assert html.index('id="storage-only-architecture"')<html.index('id="extraction-retrieval"')<html.index('class="mw-wall-tail"')
for c in toc["collections"]:
    assert 'id="'+c["anchor"]+'"' in html,c["anchor"]
for ident in ("mwContentsList","mwTocStatus","mwExtractionPipeline","mwFormatGrid","mwFormatSearch","mwFormatGroup","mwFormatCount","mwExtractionOutputs","mwEvidenceFields","mwExtractionSafeguards","mwEvidenceExample","mwExtractionStatus","mwExtractionSources"):
    assert 'id="'+ident+'"' in html,ident
assert html.count("assets/memory-wall-guides.css")==1 and html.count("assets/memory-wall-guides.js")==1
css=(ROOT/"site/assets/memory-wall-guides.css").read_text(encoding="utf-8")
js=(ROOT/"site/assets/memory-wall-guides.js").read_text(encoding="utf-8")
assert "memory-wall-contents.json" in js and "memory-extraction-retrieval.json" in js
assert "textContent" in js and "innerHTML" not in js
assert 'mk("details"' in js and 'mk("summary"' in js
assert ".mw-toc-card" in css and ".mw-format-card" in css and "@media print" in css and "@media(max-width:" in css
# All earlier original content must still be governed by old acceptance scripts.
posters=json.loads((ROOT/"registry/curations/memory-posters.v0.1.json").read_text())
assert len(posters["posters"])==3
viz=json.loads((ROOT/"registry/decisions/visualization-workspace.json").read_text())
assert viz["decision_id"]=="A7-VIS-DEC-000001"
platform=json.loads((ROOT/"registry/curations/platform-responsibilities.v0.1.json").read_text())
assert len(platform["entries"])==8
vocab=json.loads((ROOT/"registry/curations/memory-ui-vocabulary.v0.1.json").read_text())
assert len(vocab["terms"])==13
storage=json.loads((ROOT/"registry/curations/memory-storage-architecture.v0.1.json").read_text())
assert len(storage["formats"])==7
public=json.dumps(d).lower()+" "+json.dumps(toc).lower()
for restricted in ("drive.google.com/file/","drive.google.com/drive/folders/","docs.google.com/document/d/","docs.google.com/spreadsheets/d/","1ddz-gevq","private-corpus-id"):
    assert restricted not in public, restricted
for path in (".github/workflows/validate-registry.yml",".github/workflows/deploy-a7-pages.yml",".github/workflows/a7-browser-qa.yml"):
    assert "memory_extraction_guidance" in (ROOT/path).read_text(),path
print("A7 MEMORY WALL EXTRACTION PASS six_collections=1 seventeen_families=1 original_01_05_protected=1 private_source_records=0")
