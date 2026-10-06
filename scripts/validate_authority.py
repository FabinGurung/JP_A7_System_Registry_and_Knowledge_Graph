#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
errors=[]

def load(path):
    try:
        return json.loads((ROOT/path).read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}: {exc}")
        return {}

vocab=load(Path("registry/authority/vocabularies.json"))
facts=load(Path("registry/authority/fact-classes.json"))
auth=load(Path("registry/authority/authority-map.json"))
roles=load(Path("registry/authority/provider-roles.json"))
engine=load(Path("registry/authority/conflict-resolution.json"))
tax=load(Path("registry/authority/conflict-taxonomy.json"))

fact_names=set()
fact_ids=set()
for row in facts.get("fact_classes",[]):
    if row.get("fact_class") in fact_names:
        errors.append(f"duplicate fact_class {row.get('fact_class')}")
    if row.get("fact_class_id") in fact_ids:
        errors.append(f"duplicate fact_class_id {row.get('fact_class_id')}")
    fact_names.add(row.get("fact_class"))
    fact_ids.add(row.get("fact_class_id"))
    if row.get("default_materiality") not in vocab.get("materiality",[]):
        errors.append(f"{row.get('fact_class')}: invalid materiality")
    if row.get("timestamp_strategy") not in vocab.get("timestamp_strategies",[]):
        errors.append(f"{row.get('fact_class')}: invalid timestamp strategy")

authority_ids=set()
scoped=set()
for row in auth.get("assignments",[]):
    aid=row.get("authority_id")
    if aid in authority_ids: errors.append(f"duplicate authority_id {aid}")
    authority_ids.add(aid)
    if row.get("fact_class") not in fact_names:
        errors.append(f"{aid}: unknown fact_class {row.get('fact_class')}")
    key=(row.get("fact_class"),row.get("scope_type"),row.get("scope_id"))
    if key in scoped: errors.append(f"duplicate scoped authority {key}")
    scoped.add(key)
    if row.get("materiality") not in vocab.get("materiality",[]):
        errors.append(f"{aid}: invalid materiality")
    if row.get("timestamp_strategy") not in vocab.get("timestamp_strategies",[]):
        errors.append(f"{aid}: invalid timestamp strategy")

providers=[p.get("provider") for p in roles.get("providers",[])]
if len(providers)!=len(set(providers)):
    errors.append("duplicate provider role")
expected={"github","google_drive","google_sheets","slack","discord","email","whatsapp"}
if set(providers)!=expected:
    errors.append(f"provider roles mismatch: expected {sorted(expected)} got {sorted(providers)}")

conflicts=[c.get("conflict_type") for c in tax.get("conflicts",[])]
if len(conflicts)!=len(set(conflicts)):
    errors.append("duplicate conflict_type")
for c in tax.get("conflicts",[]):
    action=c.get("default_action")
    if action not in vocab.get("resolution_outcomes",[]) and action != "USE_AS_EVIDENCE_ONLY":
        errors.append(f"{c.get('conflict_type')}: unknown default action {action}")

if engine.get("principle")!="AUTHORITY_BEFORE_RECENCY":
    errors.append("resolution engine must enforce AUTHORITY_BEFORE_RECENCY")
if engine.get("hard_rules",{}).get("newest_wins_by_default") is not False:
    errors.append("newest_wins_by_default must be false")
if engine.get("hard_rules",{}).get("provider_failure_attempt_limit") != 3:
    errors.append("provider_failure_attempt_limit must be 3")

policy_dir=ROOT/"policies/providers"
policy_files=sorted(policy_dir.glob("*.json"))
policy_providers=set()
for p in policy_files:
    obj=json.loads(p.read_text(encoding="utf-8"))
    provider=obj.get("provider")
    policy_providers.add(provider)
    if obj.get("default_claim_role") not in vocab.get("claim_roles",[]):
        errors.append(f"{p.name}: invalid default_claim_role")
if policy_providers != expected:
    errors.append(f"provider policy files mismatch: expected {sorted(expected)} got {sorted(policy_providers)}")

qa_file=ROOT/"registry/qa/human-qa-cases.jsonl"
if not qa_file.exists():
    errors.append("missing human QA case ledger")

if errors:
    print("A7 AUTHORITY VALIDATION: FAIL")
    for e in errors: print("- "+e)
    raise SystemExit(1)

print(f"A7 AUTHORITY VALIDATION: PASS fact_classes={len(fact_names)} authority_rules={len(authority_ids)} providers={len(providers)} conflict_types={len(conflicts)}")
