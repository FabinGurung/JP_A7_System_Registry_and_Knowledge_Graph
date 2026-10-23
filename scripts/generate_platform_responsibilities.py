#!/usr/bin/env python3
"""Project user-approved platform responsibilities as a non-authoritative Memory Wall reference."""
import argparse,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];SRC=R/"registry/curations/platform-responsibilities.v0.1.json"
def build(sha):
    raw=SRC.read_bytes();d=json.loads(raw)
    if len(d["entries"])!=8 or len({x["id"] for x in d["entries"]})!=8:raise ValueError("Platform matrix should preserve seven existing roles and add one AI operator")
    if d["document_id"]!="A7-MEM-PLATFORM-ROLES-005":raise ValueError("Do not duplicate existing poster")
    poster=d["architecture_poster"]
    if poster["id"]!=d["document_id"] or len(poster["sources"])!=2 or len(poster["provenance_fields"])!=7:raise ValueError("Poster contract incomplete")
    d.update({"non_authoritative":True,"projection_kind":"CURATED_PUBLIC_PLATFORM_ADVICE","site_build_commit":sha,"source_sha256":hashlib.sha256(raw).hexdigest()})
    return d
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",required=True);p.add_argument("--commit-sha",required=True);a=p.parse_args()
    dst=Path(a.output);dst.parent.mkdir(exist_ok=True,parents=True)
    d=build(a.commit_sha);dst.write_text(json.dumps(d,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("A7 MEMORY WALL PLATFORM MATRIX PASS rows="+str(len(d["entries"])))
