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

ids_doc=load("registry/entities/project-identities.json")
routes_doc=load("registry/routing/project-module-bindings.json")
contract=load("registry/contracts/project-module-routing-contract.json")
modules=load("registry/entities/modules.json").get("modules",[])
authority=load("registry/authority/authority-map.json").get("assignments",[])
facts=load("registry/authority/fact-classes.json").get("fact_classes",[])

ids=[x.get("project_id") for x in ids_doc.get("project_identities",[])]
if ids_doc.get("project_count")!=len(ids): errors.append("project identity count mismatch")
if len(ids)!=len(set(ids)): errors.append("duplicate project semantic IDs")
if any(not isinstance(x,str) or not x.startswith("PRJ-") for x in ids): errors.append("invalid project semantic ID")
if ids_doc.get("authority",{}).get("operational_project_master_owner")!="MOD-OPS-001": errors.append("Operations must own project master")
if ids_doc.get("provider_observation",{}).get("provider_readback")!="PASS": errors.append("project identity source provider readback not PASS")

mod_by={m.get("module_id"):m for m in modules}
auth_by={a.get("authority_id"):a for a in authority}
fact_names={f.get("fact_class") for f in facts}
profiles=routes_doc.get("execution_profiles",[])
if len(profiles)!=1: errors.append("exactly one default execution profile expected")
profile=profiles[0] if profiles else {}
if profile.get("execution_profile_id")!="EXEC-PROFILE-AEC-CORE-001": errors.append("unexpected default execution profile")
routes=profile.get("routes",[])
expected={
 "project_operational_fact":("AUTH-000009","MOD-OPS-001"),
 "scheduling_fact":("AUTH-000011","MOD-SCHED-001"),
 "cost_estimation_fact":("AUTH-000012","MOD-COST-001"),
 "structural_analysis_fact":("AUTH-000013","MOD-STRUCT-001"),
 "cad_drawing_fact":("AUTH-000014","MOD-CAD-001"),
}
if {r.get("fact_class") for r in routes}!=set(expected): errors.append("execution route fact-class set mismatch")
for r in routes:
    fc=r.get("fact_class"); aid=r.get("authority_id"); mid=r.get("module_id")
    if fc not in fact_names: errors.append(f"unknown fact class {fc}")
    if fc in expected and (aid,mid)!=expected[fc]: errors.append(f"{fc}: route does not match expected authority/module")
    a=auth_by.get(aid)
    if not a or a.get("fact_class")!=fc or a.get("owner_ref")!=mid: errors.append(f"{fc}: authority map mismatch")
    m=mod_by.get(mid)
    if not m: errors.append(f"{fc}: unknown module {mid}")
    elif m.get("a7_module_manifest",{}).get("path")!="A7_MODULE.json": errors.append(f"{mid}: no A7 module manifest pointer")
    if r.get("project_instance_assertion")!="NOT_ASSERTED_BY_A7": errors.append(f"{fc}: route illegally asserts project instance")
if any(r.get("module_id") in {"MOD-RND-001","MOD-STUDY-001"} for r in routes): errors.append("R&D/Study must not be default project execution routes")

bindings=routes_doc.get("project_bindings",[])
bound=[b.get("project_id") for b in bindings]
if routes_doc.get("project_binding_count")!=len(bindings): errors.append("project binding count mismatch")
if set(bound)!=set(ids): errors.append("project binding set must exactly equal semantic project IDs")
if len(bound)!=len(set(bound)): errors.append("duplicate project bindings")
for b in bindings:
    if b.get("execution_profile_id")!="EXEC-PROFILE-AEC-CORE-001": errors.append(f"{b.get('project_id')}: wrong execution profile")
    if b.get("binding_status")!="ACTIVE_ROUTING": errors.append(f"{b.get('project_id')}: binding not active")
    if b.get("project_specific_module_instances")!="NOT_ASSERTED_BY_A7": errors.append(f"{b.get('project_id')}: project instance assertion forbidden")

required={
 "Project operational master values remain owned by MOD-OPS-001 and are not duplicated into A7 routing records.",
 "Route availability never asserts that a project-specific instance, model, schedule, BOQ or drawing already exists.",
 "Research and Study are not default project-execution routes."
}
if not required.issubset(set(contract.get("required_invariants",[]))): errors.append("routing contract missing required boundaries")

if errors:
    print("A7 PROJECT MODULE ROUTING VALIDATION: FAIL")
    for e in errors: print("- "+e)
    raise SystemExit(1)
print(f"A7 PROJECT MODULE ROUTING VALIDATION: PASS projects={len(ids)} routes={len(routes)} profile={profile.get('execution_profile_id')}")
