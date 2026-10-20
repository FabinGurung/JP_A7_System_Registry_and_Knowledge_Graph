#!/usr/bin/env python3
"""Build the public, non-authoritative Memory Wall curation from source JSON."""
import argparse
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"registry/curations/memory-posters.v0.1.json"

def build(commit_sha):
    raw=SRC.read_bytes()
    obj=json.loads(raw)
    obj["non_authoritative"]=True
    obj["projection_kind"]="A7_PASSIVE_REFERENCE_POSTER_BOARD"
    obj["source_path"]="registry/curations/memory-posters.v0.1.json"
    obj["source_sha256"]=hashlib.sha256(raw).hexdigest()
    obj["site_build_commit_sha"]=commit_sha
    return obj

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True)
    p.add_argument("--commit-sha",required=True)
    args=p.parse_args()
    output=Path(args.output)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(build(args.commit_sha),indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"A7 MEMORY WALL: derived {len(build(args.commit_sha)['posters'])} posters from source")
