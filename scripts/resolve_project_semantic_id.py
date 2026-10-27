#!/usr/bin/env python3
"""Resolve an A7 project ID without exposing private project attributes."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"registry/entities/project-identities.json"

def resolve(project_id, source=SOURCE):
    d=json.loads(Path(source).read_text(encoding="utf-8"))
    active={row["project_id"] for row in d["project_identities"]}
    redirects={a["alias_project_id"]:a["canonical_project_id"] for a in d["retired_project_id_aliases"]}
    if len(redirects)!=len(d["retired_project_id_aliases"]): raise ValueError("Duplicate retired aliases")
    if set(redirects)&active: raise ValueError("An active ID cannot also be retired")
    if project_id in active: return {"requested_id":project_id,"canonical_id":project_id,"state":"ACTIVE","routing_allowed":True}
    if project_id in redirects:
        canonical=redirects[project_id]
        if canonical not in active: raise ValueError("Broken retired redirect")
        return {"requested_id":project_id,"canonical_id":canonical,"state":"RETIRED_REDIRECT","routing_allowed":False}
    return {"requested_id":project_id,"canonical_id":None,"state":"UNKNOWN","routing_allowed":False}

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("project_id")
    args=p.parse_args()
    print(json.dumps(resolve(args.project_id),sort_keys=True))
