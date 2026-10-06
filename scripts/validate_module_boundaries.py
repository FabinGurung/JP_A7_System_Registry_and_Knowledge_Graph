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
    rows=[]
    for n,line in enumerate((ROOT/path).read_text(encoding="utf-8").splitlines(),1):
        if not line.strip(): continue
        try: rows.append(json.loads(line))
        except Exception as exc: errors.append(f"{path}:{n}: {exc}")
    return rows

mods=load("registry/entities/modules.json").get("modules",[])
own=load("registry/authority/module-ownership.json").get("profiles",[])
bounds=load("registry/authority/system-boundaries.json")
repos=load("registry/entities/repositories.json").get("repositories",[])
facts=load("registry/authority/fact-classes.json").get("fact_classes",[])
auth=load("registry/authority/authority-map.json").get("assignments",[])
roles=load("registry/authority/repository-role-candidates.json").get("role_candidates",[])
edges=load_jsonl("registry/edges/edges.jsonl")

expected={"MOD-OPS-001","MOD-SCHED-001","MOD-COST-001","MOD-STRUCT-001","MOD-CAD-001","MOD-RND-001","MOD-STUDY-001"}
ids={m.get("module_id") for m in mods}
if ids!=expected: errors.append(f"module ID set mismatch: {sorted(ids)}")
if len({m.get("repository_id") for m in mods})!=len(mods): errors.append("specialist modules must bind one-to-one to repositories in Phase 6")
repoids={r.get("repository_id") for r in repos}
for m in mods:
    if m.get("repository_id") not in repoids: errors.append(f"{m.get('module_id')}: unknown repository")
    if m.get("platform_level")!="PEER_SPECIALIST_MODULE": errors.append(f"{m.get('module_id')}: must be peer-level")

profiles={p.get("module_id"):p for p in own}
if set(profiles)!=expected: errors.append("ownership profiles must cover all seven modules")
factnames={f.get("fact_class") for f in facts}
for p in own:
    overlap=set(p.get("owns_fact_classes",[])) & set(p.get("must_not_own_fact_classes",[]))
    if overlap: errors.append(f"{p.get('module_id')}: ownership overlap {sorted(overlap)}")
    for f in p.get("owns_fact_classes",[]):
        if f not in factnames: errors.append(f"{p.get('module_id')}: unknown owned fact class {f}")

authmap={a.get("fact_class"):a.get("owner_ref") for a in auth}
expected_auth={
 "project_operational_fact":"MOD-OPS-001",
 "project_master_operational_record":"MOD-OPS-001",
 "project_resource_relationship":"MOD-OPS-001",
 "scheduling_fact":"MOD-SCHED-001",
 "cost_estimation_fact":"MOD-COST-001",
 "structural_analysis_fact":"MOD-STRUCT-001",
 "cad_drawing_fact":"MOD-CAD-001",
 "research_publication_fact":"MOD-RND-001",
 "study_learning_fact":"MOD-STUDY-001"
}
for fact,owner in expected_auth.items():
    if authmap.get(fact)!=owner: errors.append(f"{fact}: expected owner {owner}, got {authmap.get(fact)}")

forbidden=set(bounds.get("topology_rule",{}).get("forbidden_module_hierarchy_relations",[]))
for e in edges:
    if e.get("from_entity_id") in expected and e.get("to_entity_id") in expected and e.get("relation_type") in forbidden:
        errors.append(f"forbidden module hierarchy edge {e.get('edge_id')}")

ops_targets={e.get("to_entity_id") for e in edges if e.get("from_entity_id")=="MOD-OPS-001" and e.get("relation_type")=="LINKS_TO_PEER_MODULE"}
if ops_targets!={"MOD-SCHED-001","MOD-COST-001","MOD-STRUCT-001","MOD-CAD-001"}:
    errors.append(f"Operations peer links incomplete: {sorted(ops_targets)}")

for m in expected:
    if not any(e.get("from_entity_id")=="SYS-A7-000001" and e.get("relation_type")=="REGISTERS_MODULE" and e.get("to_entity_id")==m for e in edges):
        errors.append(f"{m}: missing A7 registry edge")

bound_roles={r.get("binding_status") for r in roles}
if not any(str(x).startswith("BOUND_TO_MODULE:") for x in bound_roles): errors.append("role candidates were not bound")

must_not=set(bounds.get("system_boundary",{}).get("must_not_own",[]))
for required in ["Daily Ops current state","project schedule","BOQ/rate/cost calculations","structural model/analysis/results/SAR","CAD/drawing production/revisions"]:
    if required not in must_not: errors.append(f"A7 negative boundary missing: {required}")

if errors:
    print("A7 MODULE BOUNDARY VALIDATION: FAIL")
    for e in errors: print("- "+e)
    raise SystemExit(1)
print(f"A7 MODULE BOUNDARY VALIDATION: PASS modules={len(mods)} ownership_profiles={len(own)} ops_peer_links={len(ops_targets)}")
