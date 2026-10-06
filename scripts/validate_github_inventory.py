#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
errors=[]

def load_json(path):
    try: return json.loads((ROOT/path).read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}: {exc}")
        return {}

def load_jsonl(path):
    rows=[]
    try:
        for n,line in enumerate((ROOT/path).read_text(encoding="utf-8").splitlines(),1):
            if not line.strip(): continue
            try: rows.append(json.loads(line))
            except Exception as exc: errors.append(f"{path}:{n}: {exc}")
    except Exception as exc: errors.append(f"{path}: {exc}")
    return rows

meta=load_json(Path("registry/providers/github-inventory-meta.json"))
repos=load_json(Path("registry/entities/repositories.json")).get("repositories",[])
branches=load_jsonl(Path("registry/providers/github-branches.jsonl"))
pages=load_json(Path("registry/providers/github-pages.json")).get("pages",[])
workflows=load_json(Path("registry/providers/github-workflows.json")).get("workflows",[])
roles=load_json(Path("registry/authority/repository-role-candidates.json")).get("role_candidates",[])
findings=load_json(Path("registry/findings/github-pages-findings.json")).get("findings",[])

repo_ids=[r.get("repository_id") for r in repos]
provider_ids=[r.get("provider_object_id") for r in repos]
full_names=[r.get("repository_full_name") for r in repos]
if len(repo_ids)!=len(set(repo_ids)): errors.append("duplicate repository_id")
if len(provider_ids)!=len(set(provider_ids)): errors.append("duplicate provider_object_id")
if len(full_names)!=len(set(full_names)): errors.append("duplicate repository_full_name")
if len(repos)!=meta.get("repositories_observed"): errors.append("repository count != inventory meta")
if len(pages)!=len(repos): errors.append("exactly one Pages record required per inventoried repository")
if len(roles)!=len(repos): errors.append("exactly one role candidate required per inventoried repository")

repo_by={r["repository_id"]:r for r in repos}
branch_keys=set()
branch_names={}
for b in branches:
    rid=b.get("repository_id")
    if rid not in repo_by: errors.append(f"branch references unknown repo {rid}")
    key=(rid,b.get("branch_name"))
    if key in branch_keys: errors.append(f"duplicate branch record {key}")
    branch_keys.add(key)
    branch_names.setdefault(rid,set()).add(b.get("branch_name"))
    if b.get("is_default") and b.get("branch_name")!=repo_by.get(rid,{}).get("default_branch"):
        errors.append(f"{rid}: default branch flag mismatch")

for rid,r in repo_by.items():
    if r.get("default_branch") not in branch_names.get(rid,set()):
        errors.append(f"{rid}: default branch missing from branch inventory")
    if r.get("canonical_production_branch") and r.get("canonical_production_branch") not in branch_names.get(rid,set()):
        errors.append(f"{rid}: production branch missing from branch inventory")

wf_ids=set()
wf_lookup={}
for w in workflows:
    if w.get("workflow_id") in wf_ids: errors.append(f"duplicate workflow_id {w.get('workflow_id')}")
    wf_ids.add(w.get("workflow_id"))
    rid=w.get("repository_id")
    if rid not in repo_by: errors.append(f"workflow references unknown repo {rid}")
    for ref in w.get("branch_refs",[]):
        if ref not in branch_names.get(rid,set()): errors.append(f"{w.get('workflow_id')}: unknown branch ref {ref}")
    wf_lookup[(rid,w.get("workflow_path"),w.get("workflow_sha"))]=w

page_repo=set()
for p in pages:
    rid=p.get("repository_id")
    if rid in page_repo: errors.append(f"duplicate Pages record for {rid}")
    page_repo.add(rid)
    if rid not in repo_by: errors.append(f"Pages references unknown repo {rid}")
    trig=p.get("production_trigger_branch")
    if trig and trig not in branch_names.get(rid,set()): errors.append(f"{rid}: Pages trigger branch not inventoried")
    if p.get("deployment_mode")=="GITHUB_ACTIONS_CUSTOM":
        path=p.get("workflow_path"); sha=p.get("workflow_sha")
        w=wf_lookup.get((rid,path,sha))
        if not w: errors.append(f"{rid}: custom Pages owner workflow not found in workflow inventory")
        elif not w.get("deploy_pages_capable"): errors.append(f"{rid}: Pages owner workflow is not deploy-capable")
    if p.get("owner_invariant_status")!="NOT_ESTABLISHED" and not p.get("latest_successful_run_id"):
        errors.append(f"{rid}: established Pages owner lacks successful run evidence")

if meta.get("branch_records")!=len(branches): errors.append("branch record count != inventory meta")
if meta.get("current_custom_workflow_records")!=len(workflows): errors.append("workflow count != inventory meta")
if meta.get("pages_records")!=len(pages): errors.append("Pages count != inventory meta")

if not findings: errors.append("Pages findings inventory must not be empty")
for f in findings:
    if f.get("repository_id") not in repo_by: errors.append(f"finding references unknown repo {f.get('repository_id')}")

expected_provider_ids={"843020367","897526094","1307302088","1309466765","1312113873","1312147922","1312661427","1326596450","1406572237"}
if set(provider_ids)!=expected_provider_ids:
    errors.append("connected owner repository provider-ID set differs from Phase-3 observed set")

if errors:
    print("A7 GITHUB INVENTORY VALIDATION: FAIL")
    for e in errors: print("- "+e)
    raise SystemExit(1)

print(f"A7 GITHUB INVENTORY VALIDATION: PASS repos={len(repos)} branches={len(branches)} pages={len(pages)} workflows={len(workflows)} findings={len(findings)}")
