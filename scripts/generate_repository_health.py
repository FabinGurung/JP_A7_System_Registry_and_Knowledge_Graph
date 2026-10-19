#!/usr/bin/env python3
"""Generate non-authoritative, dated A7 Pages repo health observation."""
import argparse,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
src=R/"registry/providers/github-health-observation-20261019.json"
def build(commit):
    obj=json.loads(src.read_text(encoding="utf-8"))
    obj["non_authoritative"]=True
    obj["projection_kind"]="A7_GITHUB_HEALTH_SNAPSHOT"
    obj["source_path"]="registry/providers/github-health-observation-20261019.json"
    obj["source_sha256"]=hashlib.sha256(src.read_bytes()).hexdigest()
    obj["site_build_commit_sha"]=commit
    return obj
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",required=True);p.add_argument("--commit-sha",required=True);a=p.parse_args()
    out=Path(a.output);out.parent.mkdir(exist_ok=True,parents=True);out.write_text(json.dumps(build(a.commit_sha),indent=2)+"\n",encoding="utf-8")
    print("A7 DATED REPO HEALTH DERIVATION PASS repositories=9")
