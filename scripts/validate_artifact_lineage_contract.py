#!/usr/bin/env python3
"""Validate a public-safe cross-provider lineage contract and real A7 release sample.
This validator never reads or writes private Google Drive, or claims Main ACK.
"""
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
contract=json.loads((R/"registry/contracts/source-artifact-lineage.v0.1.json").read_text(encoding="utf-8"))
example=json.loads((R/"registry/lineage/public-pages-release.example.json").read_text(encoding="utf-8"))
assert contract["schema"]=="a7://source-artifact-lineage-contract/0.1"
assert contract["contract_id"]=="A7-LINEAGE-001"
assert contract["adoption_status"]=="ACTIVE_PUBLIC_SAFE_CONTRACT_NO_PRIVATE_DRIVE_IMPORT"
assert contract["public_projection_gate"]["private_A9_bridge"]=="NO_IMPORT_NO_ACK"
assert contract["public_projection_gate"]["runtime_handoff_count"]==0
assert contract["public_projection_gate"]["emit_private_drive_identifiers"] is False
assert contract["public_projection_gate"]["model_is_authoritative"] is False
assert all(value is True for value in contract["checks"].values())
assert {"GITHUB_RELEASE_SOURCE","GITHUB_BUILD_RUN","GITHUB_PAGES_ARTIFACT"}.issubset(contract["admissible_public_fact_classes"])
assert "LOCAL_MAIN_CONSUMED_CURSOR" in contract["private_owner_only_fact_classes"]
assert {"BUILT_FROM","VALIDATED_BY","PUBLISHED_BY","GENERATED_FROM","REGISTERED_IN","ROUTED_BY"}=={x["type"] for x in contract["typed_edges"]}
assert all(x["direction"]=="DIRECTED" for x in contract["typed_edges"])
assert contract["example"]=="registry/lineage/public-pages-release.example.json"
assert example["schema"]=="a7://source-artifact-lineage-instance/0.1"
assert example["state"]=="PUBLIC_SOURCE_RELEASE_VERIFIED"
commit=example["source"]["commit"]
assert re.fullmatch(r"[0-9a-f]{40}",commit)
assert example["source"]["repo_full_name"]=="FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph"
assert example["source"]["repository_provider_id"]=="1406572237"
assert example["source"]["branch"]=="main"
assert (R/example["source"]["path"]).is_file()
assert example["source"]["source_file_sha256"] is None
assert example["ci"]["run_id"]==39593936542
assert example["publication"]["run_id"]==39593936610
assert example["publication"]["artifact_id"]==12342599596
assert example["publication"]["artifact_role"]=="GITHUB_PAGES_BUILD_ARCHIVE"
assert re.fullmatch(r"[0-9a-f]{64}",example["publication"]["artifact_archive_digest_sha256"])
assert example["ci"]["commit"]==commit==example["publication"]["commit"]
assert example["ci"]["conclusion"]=="success"==example["publication"]["conclusion"]
assert example["drive_output"] is None and example["release_tag"] is None
assert example["private_main_ack"]=={"state":"NOT_APPLICABLE_NO_DRIVE_IMPORT","cursor":None,"local_sequence":None}
assert {e["type"] for e in example["edges"]}=={"BUILT_FROM","VALIDATED_BY","PUBLISHED_BY"}
assert all(e["from"]==example["record_id"] for e in example["edges"])
assert all(not any(s in json.dumps(e) for s in ["drive.google.com","docs.google.com","GDRIVE:","PRIVATE_DRIVE"]) for e in example["edges"])
assert not any(t in json.dumps(example) for t in ('"drive_output": {"file_id"','"private_main_ack": {"state": "ACKED"'))
assert (R/"docs/ARTIFACT_LINEAGE_CONTRACT_READ_FIRST.md").is_file()
print("A7 ARTIFACT LINEAGE CONTRACT PASS public_commit=1 ci=1 pages_artifact=1 private_import=0 ack=0")
