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

def load_jsonl(path):
    p=ROOT/path
    if not p.exists(): return []
    out=[]
    for n,line in enumerate(p.read_text(encoding="utf-8").splitlines(),1):
        if not line.strip(): continue
        try: out.append(json.loads(line))
        except Exception as exc: errors.append(f"{path}:{n}: {exc}")
    return out

mods=load("registry/entities/modules.json").get("modules",[])
ownership=load("registry/authority/module-ownership.json").get("profiles",[])
contract=load("registry/contracts/module-manifest-contract.json")
obs=load("registry/providers/module-manifest-observations.json").get("observations",[])
recs=load_jsonl("registry/providers/module-manifest-reconciliations.jsonl")

expected={"MOD-OPS-001","MOD-SCHED-001","MOD-COST-001","MOD-STRUCT-001","MOD-CAD-001","MOD-RND-001","MOD-STUDY-001"}
mod_by={m.get("module_id"):m for m in mods}
if set(mod_by)!=expected: errors.append("module set differs from bound Phase-6 set")
if len(obs)!=7: errors.append(f"expected 7 immutable Phase-7 manifest observations, got {len(obs)}")
if contract.get("canonical_path")!="A7_MODULE.json": errors.append("canonical manifest path must be A7_MODULE.json")
if contract.get("manifest_role")!="ROUTING_ONLY_NON_AUTHORITATIVE_FOR_DOMAIN_FACTS": errors.append("manifest role must be routing-only")

own_ids={p.get("ownership_profile_id") for p in ownership}
obs_by={}
seen_repo=set(); seen_pid=set()
for o in obs:
    mid=o.get("module_id"); rid=o.get("repository_id"); pid=o.get("provider_repository_id")
    if mid in obs_by: errors.append(f"duplicate module observation {mid}")
    if rid in seen_repo: errors.append(f"duplicate repository observation {rid}")
    if pid in seen_pid: errors.append(f"duplicate provider repository observation {pid}")
    obs_by[mid]=o; seen_repo.add(rid); seen_pid.add(pid)
    m=mod_by.get(mid)
    if not m: errors.append(f"unknown module observation {mid}"); continue
    if m.get("repository_id")!=rid: errors.append(f"{mid}: repository_id mismatch")
    if m.get("provider_repository_id")!=pid: errors.append(f"{mid}: provider_repository_id mismatch")
    if m.get("repository_full_name")!=o.get("repository_full_name"): errors.append(f"{mid}: repository_full_name mismatch")
    if m.get("default_branch")!=o.get("default_branch"): errors.append(f"{mid}: default branch mismatch")
    if m.get("ownership_profile_id") not in own_ids: errors.append(f"{mid}: unknown ownership profile")
    if o.get("provider_readback")!="PASS": errors.append(f"{mid}: baseline provider readback not PASS")
    if o.get("entrypoint_count",0)<1: errors.append(f"{mid}: baseline has no routing entrypoints")
    if o.get("post_snapshot_branch")!="snapshot/post-a7-seq-000007-module-manifest": errors.append(f"{mid}: Phase-7 POST snapshot branch mismatch")

effective={mid:{"blob":o.get("manifest_blob_sha"),"commit":o.get("post_sha")} for mid,o in obs_by.items()}
seen_rec_ids=set()
for r in recs:
    rid=r.get("reconciliation_id"); mid=r.get("module_id")
    if rid in seen_rec_ids: errors.append(f"duplicate reconciliation id {rid}")
    seen_rec_ids.add(rid)
    if mid not in mod_by: errors.append(f"reconciliation references unknown module {mid}"); continue
    m=mod_by[mid]
    if r.get("repository_id")!=m.get("repository_id"): errors.append(f"{rid}: repository_id mismatch")
    if r.get("provider_repository_id")!=m.get("provider_repository_id"): errors.append(f"{rid}: provider_repository_id mismatch")
    if r.get("repository_full_name")!=m.get("repository_full_name"): errors.append(f"{rid}: repository_full_name mismatch")
    if r.get("manifest_path")!="A7_MODULE.json": errors.append(f"{rid}: manifest_path invalid")
    if r.get("manifest_role")!="ROUTING_ONLY_NON_AUTHORITATIVE_FOR_DOMAIN_FACTS": errors.append(f"{rid}: manifest role invalid")
    if r.get("provider_readback")!="PASS": errors.append(f"{rid}: provider readback not PASS")
    if r.get("historical_baseline_preserved") is not True: errors.append(f"{rid}: historical baseline must be preserved")
    cur=effective.get(mid)
    if not cur: errors.append(f"{rid}: no baseline observation"); continue
    if r.get("previous_manifest_blob_sha")!=cur["blob"]: errors.append(f"{rid}: previous blob does not chain from prior state")
    if r.get("previous_observed_commit_sha")!=cur["commit"]: errors.append(f"{rid}: previous commit does not chain from prior state")
    effective[mid]={"blob":r.get("current_manifest_blob_sha"),"commit":r.get("current_observed_commit_sha")}

for mid,m in mod_by.items():
    ptr=m.get("a7_module_manifest",{})
    if ptr.get("path")!="A7_MODULE.json": errors.append(f"{mid}: missing canonical manifest pointer")
    if ptr.get("ref")!=m.get("default_branch"): errors.append(f"{mid}: manifest pointer must live on default branch")
    if ptr.get("manifest_role")!="ROUTING_ONLY_NON_AUTHORITATIVE_FOR_DOMAIN_FACTS": errors.append(f"{mid}: manifest pointer role invalid")
    eff=effective.get(mid)
    if not eff: errors.append(f"{mid}: no effective manifest state"); continue
    if ptr.get("provider_blob_sha")!=eff["blob"]: errors.append(f"{mid}: current manifest blob mismatch")
    if ptr.get("observed_commit_sha")!=eff["commit"]: errors.append(f"{mid}: current manifest observed commit mismatch")

required_rules={
 "The manifest contains routing pointers, not duplicated domain facts.",
 "A7 ownership profile must be loaded before domain mutation.",
 "Operations links to peer modules do not imply containment or ownership."
}
if not required_rules.issubset(set(contract.get("required_invariants",[]))):
    errors.append("module manifest contract missing anti-duplication/ownership invariants")

if errors:
    print("A7 MODULE MANIFEST VALIDATION: FAIL")
    for e in errors: print("- "+e)
    raise SystemExit(1)
print(f"A7 MODULE MANIFEST VALIDATION: PASS modules={len(mods)} baselines={len(obs)} reconciliations={len(recs)} manifest_path={contract.get('canonical_path')}")
