#!/usr/bin/env python3
"""A7 Phase-1 registry validator. Standard-library only."""

from __future__ import annotations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

errors: list[str] = []

def load_json(path: str):
    p = ROOT / path
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return None

def load_jsonl(path: str):
    p = ROOT / path
    rows = []
    try:
        for lineno, raw in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            try:
                rows.append(json.loads(raw))
            except Exception as exc:
                errors.append(f"{path}:{lineno}: invalid JSONL: {exc}")
    except Exception as exc:
        errors.append(f"{path}: cannot read: {exc}")
    return rows

required_paths = [
    "A7_BOOTSTRAP.json",
    "A7_READ_FIRST.md",
    "registry/entities/systems.json",
    "registry/entities/repositories.json",
    "registry/entities/modules.json",
    "registry/entities/projects.json",
    "registry/entities/google-drive-nodes.json",
    "registry/authority/authority-map.json",
    "registry/edges/edges.jsonl",
    "registry/aliases/aliases.jsonl",
    "registry/providers/source-references.jsonl",
    "registry/events/a7-mutations.jsonl",
    "schemas/entity.schema.json",
    "schemas/edge.schema.json",
    "schemas/alias.schema.json",
    "schemas/source-reference.schema.json",
    "schemas/repository.schema.json",
    "schemas/project.schema.json",
    "schemas/authority.schema.json",
    "schemas/mutation.schema.json",
    "relational/a7-schema.postgresql.sql",
    "policies/global/a7-core.json",
    "policies/global/fail-forward.json",
    "policies/global/public-safety.json",
    "policies/global/human-qa.json",
]

for rel in required_paths:
    if not (ROOT / rel).exists():
        errors.append(f"missing required path: {rel}")

bootstrap = load_json("A7_BOOTSTRAP.json") or {}
systems_doc = load_json("registry/entities/systems.json") or {}
repos_doc = load_json("registry/entities/repositories.json") or {}
modules_doc = load_json("registry/entities/modules.json") or {}
projects_doc = load_json("registry/entities/projects.json") or {}
drive_nodes_doc = load_json("registry/entities/google-drive-nodes.json") or {}
authority_doc = load_json("registry/authority/authority-map.json") or {}

for schema in sorted((ROOT / "schemas").glob("*.json")):
    try:
        obj = json.loads(schema.read_text(encoding="utf-8"))
        if "$schema" not in obj:
            errors.append(f"{schema.relative_to(ROOT)}: missing $schema")
    except Exception as exc:
        errors.append(f"{schema.relative_to(ROOT)}: invalid JSON: {exc}")

if bootstrap.get("system_code") != "A7":
    errors.append("A7_BOOTSTRAP.json: system_code must be A7")
repo = bootstrap.get("canonical_repository", {})
if repo.get("provider_object_id") != "1406572237":
    errors.append("A7_BOOTSTRAP.json: canonical GitHub provider_object_id mismatch")
if repo.get("full_name") != "FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph":
    errors.append("A7_BOOTSTRAP.json: canonical repository name mismatch")
if bootstrap.get("current_operating_model", {}).get("generated_outputs_are_authority") is not False:
    errors.append("A7_BOOTSTRAP.json: generated outputs must be non-authoritative")

systems = systems_doc.get("entities", [])
repos = repos_doc.get("repositories", [])
modules = modules_doc.get("modules", [])
projects = projects_doc.get("projects", [])
drive_nodes = drive_nodes_doc.get("nodes", [])

entity_ids = set()
for collection, id_key, label in [
    (systems, "entity_id", "systems"),
    (repos, "repository_id", "repositories"),
    (modules, "module_id", "modules"),
    (projects, "project_id", "projects"),
    (drive_nodes, "entity_id", "google-drive-nodes"),
]:
    for row in collection:
        rid = row.get(id_key)
        if not rid:
            errors.append(f"{label}: missing {id_key}")
            continue
        if rid in entity_ids:
            errors.append(f"duplicate entity ID across registries: {rid}")
        entity_ids.add(rid)

provider_ids = {}
for row in repos:
    pid = row.get("provider_object_id")
    if pid:
        if pid in provider_ids:
            errors.append(f"duplicate GitHub provider object ID: {pid}")
        provider_ids[pid] = row.get("repository_id")

edges = load_jsonl("registry/edges/edges.jsonl")
edge_ids = set()
for row in edges:
    eid = row.get("edge_id")
    if eid in edge_ids:
        errors.append(f"duplicate edge_id: {eid}")
    edge_ids.add(eid)
    for key in ("from_entity_id", "to_entity_id"):
        target = row.get(key)
        if target not in entity_ids:
            errors.append(f"{eid}: {key} references unknown entity {target}")

aliases = load_jsonl("registry/aliases/aliases.jsonl")
alias_ids = set()
for row in aliases:
    aid = row.get("alias_id")
    if aid in alias_ids:
        errors.append(f"duplicate alias_id: {aid}")
    alias_ids.add(aid)
    if row.get("target_entity_id") not in entity_ids:
        errors.append(f"{aid}: target_entity_id is unknown")

sources = load_jsonl("registry/providers/source-references.jsonl")
source_ids = set()
for row in sources:
    sid = row.get("source_ref_id")
    if sid in source_ids:
        errors.append(f"duplicate source_ref_id: {sid}")
    source_ids.add(sid)
    if row.get("entity_id") not in entity_ids:
        errors.append(f"{sid}: entity_id is unknown")

events = load_jsonl("registry/events/a7-mutations.jsonl")
event_ids = set()
for row in events:
    eid = row.get("event_id")
    if eid in event_ids:
        errors.append(f"duplicate mutation event_id: {eid}")
    event_ids.add(eid)
    if not str(row.get("sequence_id", "")).startswith("A7-SEQ-"):
        errors.append(f"{eid}: invalid A7 sequence ID")

assignments = authority_doc.get("assignments", [])
fact_classes = set()
for row in assignments:
    fc = row.get("fact_class")
    if fc in fact_classes:
        errors.append(f"duplicate authority fact_class: {fc}")
    fact_classes.add(fc)

sql_path = ROOT / "relational/a7-schema.postgresql.sql"
if sql_path.exists():
    sql = sql_path.read_text(encoding="utf-8")
    for required in ("CREATE TABLE a7_entities", "CREATE TABLE a7_edges", "CREATE TABLE a7_source_references", "CREATE TABLE a7_mutation_events"):
        if required not in sql:
            errors.append(f"relational contract missing: {required}")

if errors:
    print("A7 REGISTRY VALIDATION: FAIL")
    for err in errors:
        print(f"- {err}")
    sys.exit(1)

print("A7 REGISTRY VALIDATION: PASS")
print(f"entities={len(entity_ids)} edges={len(edges)} aliases={len(aliases)} sources={len(sources)} events={len(events)} authority_classes={len(assignments)}")
