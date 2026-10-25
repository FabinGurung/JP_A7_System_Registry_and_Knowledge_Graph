#!/usr/bin/env python3
"""A7 public-only Collection 06 and Memory Wall contents build."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CUR = ROOT / "registry/curations"

def build(commit_sha):
    def derive(filename, identifier, value):
        raw = (CUR / filename).read_bytes()
        data = json.loads(raw)
        assert data[identifier] == value and data["public_safe"] is True
        return {**data,"site_build_commit":commit_sha,"source_path":"registry/curations/"+filename,"source_sha256":hashlib.sha256(raw).hexdigest(),"kind":"NON_AUTHORITATIVE_PUBLIC_GUIDANCE"}
    toc = derive("memory-wall-contents.v0.1.json","manifest_id","A7-MEM-WALL-CONTENTS-001")
    guide = derive("memory-extraction-retrieval.v0.1.json","collection_id","A7-MEM-EXTRACTION-008")
    assert len(toc["collections"])==6 and len(guide["formats"])==17
    return toc,guide

if __name__ == "__main__":
    a=argparse.ArgumentParser()
    a.add_argument("--output-dir",required=True)
    a.add_argument("--commit-sha",required=True)
    args=a.parse_args()
    dest=Path(args.output_dir)
    dest.mkdir(parents=True,exist_ok=True)
    toc,guide=build(args.commit_sha)
    for filename,doc in [("memory-wall-contents.json",toc),("memory-extraction-retrieval.json",guide)]:
        (dest/filename).write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("A7 MEMORY WALL CONTENTS AND EXTRACTION GUIDANCE PASS collections=6 file_families=17")
