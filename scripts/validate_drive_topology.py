#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
errors=[]

def load(path):
    try: return json.loads((ROOT/path).read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}: {exc}")
        return {}

nodes=load(Path("registry/entities/google-drive-nodes.json")).get("nodes",[])
anchors=load(Path("registry/providers/google-drive-anchors.json")).get("anchors",[])
coverage=load(Path("registry/providers/google-drive-coverage.json"))
resolver=load(Path("registry/providers/google-drive-resolution.json"))
findings=load(Path("registry/findings/google-drive-findings.json")).get("findings",[])

ids=[n.get("entity_id") for n in nodes]
if len(ids)!=len(set(ids)): errors.append("duplicate Google Drive entity_id")
by={n.get("entity_id"):n for n in nodes}
if "GDRIVE-ROOT-000001" not in by: errors.append("missing canonical A9 Drive root node")
tops=[n for n in nodes if str(n.get("entity_id","")).startswith("GDRIVE-TOP-")]
if len(tops)!=16: errors.append(f"expected 16 top-level nodes, found {len(tops)}")
restricted=[n for n in tops if n.get("access_class")=="RESTRICTED"]
if len(restricted)!=1: errors.append("expected exactly one redacted restricted top-level boundary")
else:
    if restricted[0].get("provider_object_id") is not None: errors.append("restricted boundary must not publish provider_object_id")
    if restricted[0].get("public_safe_metadata") is not False: errors.append("restricted boundary must be public_safe_metadata=false")

provider_ids=[n.get("provider_object_id") for n in nodes if n.get("provider_object_id")]
if len(provider_ids)!=len(set(provider_ids)): errors.append("duplicate provider_object_id among Drive nodes")

for n in nodes:
    p=n.get("parent_entity_id")
    if p and p not in by: errors.append(f"{n.get('entity_id')}: unknown parent {p}")

anchor_ids=[a.get("anchor_id") for a in anchors]
if set(anchor_ids)!={n["entity_id"] for n in nodes if n["entity_id"].startswith("GDRIVE-ANCHOR-")}:
    errors.append("anchor list does not match anchor nodes")

if coverage.get("current_root_scan",{}).get("direct_top_level_branches")!=16:
    errors.append("current root scan must report 16 top-level branches")
if coverage.get("governed_index",{}).get("rows_with_current_path_under_a9_root")!=968:
    errors.append("governed index A9 row count must be 968")
hist=coverage.get("historical_index_rows_by_top_level",{})
if sum(hist.values())!=968:
    errors.append(f"historical top-level row counts sum to {sum(hist.values())}, expected 968")
if coverage.get("public_registry_boundary",{}).get("copy_full_private_drive_index_to_github") is not False:
    errors.append("public A7 must not copy full private Drive index")

rules=resolver.get("rules",[])
for required in [
    "MATCH_BY_STABLE_DRIVE_ID_BEFORE_MUTABLE_NAME_OR_PATH",
    "IF_TASK_DEPENDS_ON_CURRENT_STATE_FETCH_EXACT_DRIVE_OBJECT_OR_PARENT_LIVE",
    "DO_NOT_COPY_PRIVATE_FILE_CONTENTS_OR_PRIVATE_TOPOLOGY_PAYLOADS_INTO_PUBLIC_A7"
]:
    if required not in rules: errors.append(f"resolver missing required rule {required}")

codes=[f.get("code") for f in findings]
if len(codes)!=len(set(codes)): errors.append("duplicate Drive finding code")

if errors:
    print("A7 GOOGLE DRIVE TOPOLOGY VALIDATION: FAIL")
    for e in errors: print("- "+e)
    raise SystemExit(1)
print(f"A7 GOOGLE DRIVE TOPOLOGY VALIDATION: PASS nodes={len(nodes)} top_level={len(tops)} anchors={len(anchors)} findings={len(findings)} indexed_rows=968")
