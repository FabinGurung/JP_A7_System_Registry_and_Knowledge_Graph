#!/usr/bin/env python3
"""Derive A7-only source file dock from a curated manifest; do not infer tools."""
import argparse,hashlib,json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
SRC=R/"registry/curations/a7-developer-dock.v0.1.json"
REPO="FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph"
def build(sha):
    if not re.fullmatch("[0-9a-f]{40}",sha): raise ValueError("Build must be an exact Git SHA")
    raw=SRC.read_bytes();d=json.loads(raw);seen=set()
    for g in d["groups"]:
        for entry in g["items"]:
            p=entry["path"]
            if not p or p.startswith("/") or ".." in p or p in seen or not (R/p).is_file(): raise ValueError("Missing/invalid/duplicate A7 source "+p)
            seen.add(p);entry["source_url"]="https://github.com/"+REPO+"/blob/"+sha+"/"+p
    d.update({"projection_kind":"DERIVED_READ_ONLY_A7_SOURCE_DIRECTORY","non_authoritative":True,"site_build_commit":sha,
       "source_sha256":hashlib.sha256(raw).hexdigest()})
    return d
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",required=True);p.add_argument("--commit-sha",required=True);a=p.parse_args()
    dest=Path(a.output);dest.parent.mkdir(exist_ok=True,parents=True)
    d=build(a.commit_sha);dest.write_text(json.dumps(d,indent=2)+"\n",encoding="utf-8")
    print("A7 DEVELOPER DOCK PASS groups="+str(len(d["groups"]))+" files="+str(sum(len(g["items"]) for g in d["groups"])))
