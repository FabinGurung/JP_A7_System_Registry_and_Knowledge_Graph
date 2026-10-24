#!/usr/bin/env python3
"""Derive Memory Wall UI vocabulary from canonical public-safe A7 curation."""
import argparse, hashlib, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"registry/curations/memory-ui-vocabulary.v0.1.json"
def build(sha):
    raw=SRC.read_bytes()
    d=json.loads(raw)
    assert d["collection_id"]=="A7-MEM-UI-VOCAB-006" and d["public_safe"] and d["derived_only"]
    assert len(d["terms"])==13 and len({v["id"] for v in d["terms"]})==13
    assert {x["id"] for x in d["categories"]}=={"DISPLAY","DATA","WORKFLOW"}
    assert {t["category"] for t in d["terms"]}<= {"DISPLAY","DATA","WORKFLOW"}
    assert len(d["comparison"])==2 and len(d["example"]["register"])==2
    assert d["example"]["kind"]=="DEMONSTRATION_ONLY"
    assert not any(x in raw.decode().lower() for x in ("drive.google.com/","docs.google.com/","a9_fabin_gurung"))
    d.update({"kind":"DERIVED_READ_ONLY_GLOSSARY","source_path":str(SRC.relative_to(ROOT)),
      "source_sha256":hashlib.sha256(raw).hexdigest(),"site_build_commit":sha})
    return d
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",required=True)
    ap.add_argument("--commit-sha",required=True)
    args=ap.parse_args()
    output=Path(args.output);output.parent.mkdir(parents=True,exist_ok=True)
    result=build(args.commit_sha)
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("A7 UI GLOSSARY PASS terms="+str(len(result["terms"]))+" example=synthetic")
