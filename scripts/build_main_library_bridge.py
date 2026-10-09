#!/usr/bin/env python3
"""Create safe, offline, schema-aligned Main Library candidates from GitHub head observations.
No Google Drive/Sheets API access and no mutation. A candidate is not an ACK."""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

REGISTRY_HEADERS = [
    "Artifact_ID","Drive_ID_or_External_ID","Name","MIME_Type","Canonical_Status",
    "Authority_Class","Owner_Domain_or_Project","Current_Parent_ID","Current_Path_or_URI",
    "SHA256","Size_Bytes","Created_At","First_Registered","Last_Verified","Retention_State","Notes"
]
EDGE_HEADERS = [
    "Edge_ID","From_Artifact_ID","Relation_Type","To_Artifact_ID","Directionality",
    "Source_Basis_or_Evidence","Legacy_or_Source_Path","Created_At","Active","Notes"
]

def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def write_csv(path, columns, rows):
    with open(path, "w", encoding="utf-8", newline="") as h:
        w=csv.DictWriter(h, fieldnames=columns)
        w.writeheader()
        for row in rows:
            if set(row) != set(columns):
                raise ValueError("CSV output schema mismatch")
            w.writerow(row)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",default="registry/bridges/github-heads-20261009.json")
    p.add_argument("--out",default="build/main-library-candidates")
    args=p.parse_args()
    inp=Path(args.input)
    src=json.loads(inp.read_text(encoding="utf-8"))
    records=src["repositories"]
    if src.get("repository_count")!=len(records) or not records:
        raise ValueError("Missing or inconsistent repository snapshot")
    if src.get("main_library_import_state") != "CANDIDATE_NOT_WRITTEN":
        raise ValueError("Staging status invalid; this is not an importer")
    seen=set()
    art=[]
    edges=[]
    for x in records:
        pid=x["repository_id"]
        sha=x["observed_head_sha"]
        name=x["repository_full_name"]
        if pid in seen or not pid.isdecimal() or not re.fullmatch(r"[0-9a-f]{40,64}", sha):
            raise ValueError("Duplicate provider id or invalid Git hash")
        seen.add(pid)
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", name):
            raise ValueError("Invalid GitHub repository name")
        if x["visibility"]!="public":
            raise ValueError("Private repository metadata must not enter public export")
        aid="CANDIDATE-GITHUB-REPO-"+pid
        uri="https://github.com/"+name+"/commit/"+sha
        art.append(dict(zip(REGISTRY_HEADERS,[
            aid, "github:"+pid, name, "application/vnd.git",
            "GITHUB_OBSERVED_HEAD__PENDING_LIBRARY_ADMISSION",
            "GITHUB_PROVIDER_STATE","A7_PUBLIC_SAFE_REPOSITORY","",uri,
            "", "", "", "", src["snapshot_date"],
            "GIT_PROVIDER_HISTORY", "Default branch="+x["default_branch"]+
            "; observed Git commit="+sha+"; snapshot="+src["snapshot_id"]+
            "; this row is NOT an authoritative Main Library ACK; SHA256 intentionally blank"
        ])))
        if pid != "1406572237":
            edges.append(dict(zip(EDGE_HEADERS,[
                "CANDIDATE-EDGE-GITHUB-A7-"+pid,
                aid, "ROUTED_BY", "CANDIDATE-GITHUB-REPO-1406572237",
                "DIRECTED", "A7_PUBLIC_SAFE_GIT_DRIVE_BOOTSTRAP","",
                src["snapshot_date"],"CANDIDATE",
                "Do not import until Artifact_ID collisions, refs, destination A7 identity and private policy are reconciled"
            ])))
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    areg=out/"ArtifactRegistry_candidates.csv"
    efile=out/"ArtifactEdges_candidates.csv"
    write_csv(areg,REGISTRY_HEADERS,art)
    write_csv(efile,EDGE_HEADERS,edges)
    man={
        "schema_version":"1.0.0",
        "source_snapshot":src["snapshot_id"],
        "status":"DRY_RUN_PASS__NO_GOOGLE_DRIVE_WRITES",
        "candidate_artifacts":len(art),
        "candidate_edges":len(edges),
        "source_sha256":sha256(inp),
        "artifact_candidate_sha256":sha256(areg),
        "edges_candidate_sha256":sha256(efile),
        "needs_before_import":["read current Main Library authoritative IDs and edges",
             "deduplicate with existing artifact IDs by provider object identity",
             "recheck Git refs/commits live",
             "run A9 private change control when writing Main Library",
             "add provider readback and ACK"],
        "caveat":"Git commit hashes are NOT SHA256 column values; candidate rows do not certify sync"
    }
    (out/"bridge-manifest.json").write_text(json.dumps(man,indent=2)+"\n",encoding="utf-8")
    print(f"A7 GITHUB-MAIN BRIDGE DRY_RUN_PASS repositories={len(records)} candidate_artifacts={len(art)} candidate_edges={len(edges)}")

if __name__=="__main__":
    main()
