#!/usr/bin/env python3
"""Preserve existing A7 posters and enforce new glossary as separate fourth collection."""
import json,re,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/"scripts"))
from generate_memory_ui_vocabulary import build
d=build("QA_LOCAL_GIT")
assert d["collection_id"]=="A7-MEM-UI-VOCAB-006"
assert d["kind"]=="DERIVED_READ_ONLY_GLOSSARY" and re.fullmatch("[0-9a-f]{64}",d["source_sha256"])
assert len(d["terms"])==13 and len({x["id"] for x in d["terms"]})==13
assert all(len(x["title"])>2 and len(x["prompt"])>12 and len(x["description"])>10 for x in d["terms"])
assert set(x["id"] for x in d["comparison"])=={"code-block","interactive-card"}
old=json.loads((R/"registry/curations/memory-posters.v0.1.json").read_text())
assert len(old["posters"])==3 and {x["id"] for x in old["posters"]}=={"MEM-EXT-0001","MEM-EXT-0002","MEM-EXT-0003"}
roles=json.loads((R/"registry/curations/platform-responsibilities.v0.1.json").read_text())
assert roles["document_id"]=="A7-MEM-PLATFORM-ROLES-005" and len(roles["entries"])==8
h=(R/"site/memory-wall.html").read_text()
assert h.count('id="interface-vocabulary"')==1 and h.count('id="platform-role-board"')==1
assert h.index('id="platform-role-board"')<h.index('id="interface-vocabulary"')<h.index('id="storage-only-architecture"')<h.index('id="extraction-retrieval"')
for x in ["uiVocabTree","uiVocabRegister","uiVocabToggle","uiVocabCopy","uiVocabTerms","uiVocabSearch","uiVocabStatus"]:
    assert 'id="'+x+'"' in h,x
assert "assets/memory-ui-vocabulary.js" in h and "assets/memory-ui-vocabulary.css" in h
j=(R/"site/assets/memory-ui-vocabulary.js").read_text()
assert "data/memory-ui-vocabulary.json" in j and "textContent" in j and "innerHTML" not in j
assert "navigator.clipboard.writeText" in j
css=(R/"site/assets/memory-ui-vocabulary.css").read_text()
assert "@media print" in css and "@media(max-width:" in css
wf=(R/".github/workflows/deploy-a7-pages.yml").read_text()
assert "generate_memory_ui_vocabulary.py" in wf and "validate_memory_ui_vocabulary.py" in wf
print("A7 MEMORY UI VOCAB QA PASS terms=13 prior_external_posters=3 platform_roles=8 duplicate=0")
