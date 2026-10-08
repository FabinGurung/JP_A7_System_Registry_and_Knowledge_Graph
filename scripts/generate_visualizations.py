#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = [
    "A7_BOOTSTRAP.json",
    "registry/entities/systems.json",
    "registry/entities/repositories.json",
    "registry/entities/modules.json",
    "registry/entities/project-identities.json",
    "registry/entities/projects.json",
    "registry/authority/fact-classes.json",
    "registry/authority/authority-map.json",
    "registry/routing/project-module-bindings.json",
    "registry/edges/edges.jsonl",
    "registry/entities/google-drive-nodes.json",
    "registry/decisions/visualization-workspace.json",
]

PUBLIC_GRAPH_TYPES = {
    "system",
    "repository",
    "module",
    "project",
    "research_project",
    "fact_class",
    "execution_profile",
}

TYPE_ORDER = {
    "system": 0,
    "execution_profile": 1,
    "module": 2,
    "repository": 3,
    "fact_class": 4,
    "project": 5,
    "research_project": 6,
}

TYPE_COLORS = {
    "system": "#f8fafc",
    "execution_profile": "#a78bfa",
    "module": "#22d3ee",
    "repository": "#60a5fa",
    "fact_class": "#f59e0b",
    "project": "#34d399",
    "research_project": "#f472b6",
}

def load_json(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def load_jsonl(path: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in (ROOT / path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def stable_hash(text: str) -> int:
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:12], 16)

def entity_id(row: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = row.get(key)
        if isinstance(value, str) and value:
            return value
    return None

def add_node(nodes: dict[str, dict[str, Any]], node_id: str | None, label: str, node_type: str, **extra: Any) -> None:
    if not node_id or node_type not in PUBLIC_GRAPH_TYPES:
        return
    node = {
        "id": node_id,
        "label": label or node_id,
        "type": node_type,
        "color": TYPE_COLORS[node_type],
    }
    node.update({k: v for k, v in extra.items() if v is not None})
    nodes[node_id] = node

def ring_position(index: int, count: int, radius: float, z: float = 0.0, phase: float = 0.0) -> list[float]:
    count = max(count, 1)
    angle = phase + (2.0 * math.pi * index / count)
    return [round(radius * math.cos(angle), 3), round(radius * math.sin(angle), 3), round(z, 3)]

def make_positions(nodes: dict[str, dict[str, Any]]) -> None:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for node in nodes.values():
        grouped.setdefault(node["type"], []).append(node)
    for rows in grouped.values():
        rows.sort(key=lambda x: x["id"])

    for node in grouped.get("system", []):
        node["position2d"] = [60, 120 + 110 * grouped["system"].index(node)]
        node["position3d"] = [0, 0, 0 if node["id"] == "SYS-A7-000001" else 90 * (grouped["system"].index(node) + 1)]

    profile_rows = grouped.get("execution_profile", [])
    for i, node in enumerate(profile_rows):
        node["position2d"] = [330, 115 + 100 * i]
        node["position3d"] = [0, 0, 160 + 70 * i]

    modules = grouped.get("module", [])
    for i, node in enumerate(modules):
        node["position2d"] = [610, 70 + 78 * i]
        node["position3d"] = ring_position(i, len(modules), 210, 20, -0.2)

    repos = grouped.get("repository", [])
    for i, node in enumerate(repos):
        node["position2d"] = [930, 50 + 67 * i]
        node["position3d"] = ring_position(i, len(repos), 350, -95, 0.15)

    facts = grouped.get("fact_class", [])
    for i, node in enumerate(facts):
        col, row = divmod(i, 7)
        node["position2d"] = [330 + 185 * col, 660 + 55 * row]
        node["position3d"] = ring_position(i, len(facts), 290, 185, 0.35)

    projects = grouped.get("project", [])
    for i, node in enumerate(projects):
        col, row = divmod(i, 10)
        node["position2d"] = [40 + 130 * col, 1080 + 44 * row]
        radius = 500 + 16 * (i % 4)
        z = -180 + 360 * (i / max(len(projects) - 1, 1))
        node["position3d"] = ring_position(i, len(projects), radius, z, 0.55)

    research = grouped.get("research_project", [])
    for i, node in enumerate(research):
        node["position2d"] = [930, 720 + 62 * i]
        node["position3d"] = ring_position(i, len(research), 440, 115, 1.0)

def mermaid_source(summary: dict[str, Any], profile: dict[str, Any], modules: dict[str, dict[str, Any]]) -> str:
    lines = [
        "flowchart LR",
        '  A7["A7 Semantic Control Plane"]',
        '  P["' + str(summary["project_identities"]) + ' Project Semantic IDs"]',
        '  E["' + profile.get("execution_profile_id", "Execution Profile") + '"]',
        "  P -->|routes through| E",
        "  A7 -->|registers| E",
    ]
    for route in profile.get("routes", []):
        mid = route.get("module_id")
        module = modules.get(mid, {})
        label = module.get("canonical_label", mid)
        rid = module.get("repository_id", "")
        safe_mid = (mid or "MOD").replace("-", "_")
        safe_rid = (rid or "REPO").replace("-", "_")
        lines.append('  ' + safe_mid + '["' + label.replace('"', "'") + '"]')
        lines.append("  E -->|" + route.get("fact_class", "fact") + "| " + safe_mid)
        if rid:
            lines.append('  ' + safe_rid + '["' + rid + '"]')
            lines.append("  " + safe_mid + " -->|implemented by| " + safe_rid)
    lines.extend([
        '  RND["Research & Development"]',
        '  STUDY["Study Hub"]',
        "  A7 -->|peer knowledge module| RND",
        "  A7 -->|peer knowledge module| STUDY",
        "  classDef control fill:#111827,stroke:#a78bfa,color:#f8fafc;",
        "  classDef execution fill:#0f172a,stroke:#22d3ee,color:#f8fafc;",
        "  class A7,E control;",
    ])
    return "\n".join(lines) + "\n"

def make_excalidraw(profile: dict[str, Any], modules: dict[str, dict[str, Any]]) -> dict[str, Any]:
    elements: list[dict[str, Any]] = []
    def rect(eid: str, x: int, y: int, w: int, h: int, text: str, stroke: str) -> None:
        elements.append({
            "id": eid,
            "type": "rectangle",
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "angle": 0,
            "strokeColor": stroke,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 2,
            "strokeStyle": "solid",
            "roughness": 0,
            "opacity": 100,
            "groupIds": [],
            "frameId": None,
            "roundness": {"type": 3},
            "seed": stable_hash(eid) % 2147483647,
            "version": 1,
            "versionNonce": stable_hash(eid + "-nonce") % 2147483647,
            "isDeleted": False,
            "boundElements": [],
            "updated": 1,
            "link": None,
            "locked": False,
        })
        elements.append({
            "id": eid + "-label",
            "type": "text",
            "x": x + 12,
            "y": y + 16,
            "width": w - 24,
            "height": h - 24,
            "angle": 0,
            "strokeColor": "#e2e8f0",
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 1,
            "strokeStyle": "solid",
            "roughness": 0,
            "opacity": 100,
            "groupIds": [],
            "frameId": None,
            "roundness": None,
            "seed": stable_hash(eid + "-label") % 2147483647,
            "version": 1,
            "versionNonce": stable_hash(eid + "-label-nonce") % 2147483647,
            "isDeleted": False,
            "boundElements": [],
            "updated": 1,
            "link": None,
            "locked": False,
            "text": text,
            "fontSize": 18,
            "fontFamily": 1,
            "textAlign": "center",
            "verticalAlign": "middle",
            "containerId": None,
            "originalText": text,
            "autoResize": True,
            "lineHeight": 1.25,
        })

    rect("a7", 40, 180, 220, 90, "A7 Control Plane", "#a78bfa")
    rect("profile", 330, 180, 280, 90, profile.get("execution_profile_id", "Execution Profile"), "#a78bfa")
    for i, route in enumerate(profile.get("routes", [])):
        mid = route.get("module_id")
        module = modules.get(mid, {})
        rect("module-" + str(i), 720, 40 + i * 130, 300, 90, module.get("canonical_label", mid), "#22d3ee")
    return {
        "type": "excalidraw",
        "version": 2,
        "source": "https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph",
        "elements": elements,
        "appState": {"viewBackgroundColor": "#020617", "gridSize": 20},
        "files": {},
    }

def main() -> int:
    parser = argparse.ArgumentParser(description="Generate non-authoritative A7 visual/search projections.")
    parser.add_argument("--output-dir", default="generated", help="Output directory relative to repository root or absolute.")
    parser.add_argument("--commit-sha", default="UNKNOWN", help="Source Git commit SHA.")
    args = parser.parse_args()

    out = Path(args.output_dir)
    if not out.is_absolute():
        out = ROOT / out
    out.mkdir(parents=True, exist_ok=True)

    bootstrap = load_json("A7_BOOTSTRAP.json")
    systems_doc = load_json("registry/entities/systems.json")
    repositories_doc = load_json("registry/entities/repositories.json")
    modules_doc = load_json("registry/entities/modules.json")
    project_ids_doc = load_json("registry/entities/project-identities.json")
    research_projects_doc = load_json("registry/entities/projects.json")
    facts_doc = load_json("registry/authority/fact-classes.json")
    authority_doc = load_json("registry/authority/authority-map.json")
    routing_doc = load_json("registry/routing/project-module-bindings.json")
    canonical_edges = load_jsonl("registry/edges/edges.jsonl")
    drive_doc = load_json("registry/entities/google-drive-nodes.json")

    nodes: dict[str, dict[str, Any]] = {}
    systems = systems_doc.get("systems", systems_doc.get("entities", []))
    for row in systems:
        sid = entity_id(row, "system_id", "entity_id", "id")
        add_node(
            nodes,
            sid,
            row.get("canonical_label", sid or "System"),
            "system",
            status=row.get("status"),
            system_code=row.get("system_code"),
        )

    repositories = repositories_doc.get("repositories", [])
    for row in repositories:
        rid = row.get("repository_id")
        full_name = row.get("full_name") or row.get("repository_full_name") or rid
        add_node(
            nodes,
            rid,
            full_name,
            "repository",
            default_branch=row.get("default_branch"),
            provider_object_id=row.get("provider_object_id"),
            url=("https://github.com/" + full_name) if isinstance(full_name, str) and "/" in full_name else None,
        )

    modules = modules_doc.get("modules", [])
    module_by_id = {m.get("module_id"): m for m in modules if m.get("module_id")}
    for row in modules:
        add_node(
            nodes,
            row.get("module_id"),
            row.get("canonical_label", row.get("module_id", "Module")),
            "module",
            role=row.get("module_role"),
            group=row.get("module_group"),
            status=row.get("status"),
            repository_id=row.get("repository_id"),
            working_ref=row.get("canonical_working_ref"),
            site_url=row.get("public_site_url"),
        )

    project_ids = project_ids_doc.get("project_identities", [])
    for row in project_ids:
        pid = row.get("project_id")
        add_node(nodes, pid, pid or "Project", "project", source_record_key=row.get("source_record_key"))

    research_projects = research_projects_doc.get("projects", [])
    for row in research_projects:
        pid = entity_id(row, "project_id", "entity_id", "id")
        add_node(
            nodes,
            pid,
            row.get("canonical_label", pid or "Research project"),
            "research_project",
            status=row.get("status"),
        )

    facts = facts_doc.get("fact_classes", [])
    fact_by_name = {f.get("fact_class"): f for f in facts if f.get("fact_class")}
    for row in facts:
        add_node(
            nodes,
            row.get("fact_class_id"),
            row.get("fact_class", row.get("fact_class_id", "Fact class")),
            "fact_class",
            fact_class=row.get("fact_class"),
            materiality=row.get("default_materiality"),
            description=row.get("description"),
        )

    profiles = routing_doc.get("execution_profiles", [])
    profile = profiles[0] if profiles else {}
    profile_id = profile.get("execution_profile_id")
    add_node(
        nodes,
        profile_id,
        profile.get("profile_role", profile_id or "Execution profile"),
        "execution_profile",
        status=profile.get("status"),
    )

    make_positions(nodes)

    edges: list[dict[str, Any]] = []
    edge_ids: set[str] = set()

    def add_edge(edge_id: str, source: str | None, target: str | None, relation: str, **extra: Any) -> None:
        if not source or not target or source not in nodes or target not in nodes or edge_id in edge_ids:
            return
        row = {"id": edge_id, "source": source, "target": target, "relation": relation}
        row.update({k: v for k, v in extra.items() if v is not None})
        edges.append(row)
        edge_ids.add(edge_id)

    for row in canonical_edges:
        add_edge(
            row.get("edge_id", "EDGE-" + str(len(edges) + 1)),
            row.get("from_entity_id"),
            row.get("to_entity_id"),
            row.get("relation_type", "RELATED_TO"),
            source_kind="canonical_edge",
            status=row.get("status"),
            note=row.get("note"),
        )

    for idx, row in enumerate(project_ids, 1):
        add_edge(
            "DERIVED-PROJECT-PROFILE-" + str(idx).zfill(3),
            row.get("project_id"),
            profile_id,
            "USES_EXECUTION_PROFILE",
            source_kind="derived_projection",
        )

    for idx, route in enumerate(profile.get("routes", []), 1):
        add_edge(
            "DERIVED-PROFILE-ROUTE-" + str(idx).zfill(3),
            profile_id,
            route.get("module_id"),
            "ROUTES_" + route.get("fact_class", "FACT").upper(),
            source_kind="derived_projection",
            authority_id=route.get("authority_id"),
            fact_class=route.get("fact_class"),
            assertion=route.get("project_instance_assertion"),
        )

    authority_rows = authority_doc.get("assignments", [])
    fact_id_by_name = {f.get("fact_class"): f.get("fact_class_id") for f in facts}
    for idx, row in enumerate(authority_rows, 1):
        fact_id = fact_id_by_name.get(row.get("fact_class"))
        owner = row.get("owner_ref")
        add_edge(
            "DERIVED-AUTHORITY-" + str(idx).zfill(3),
            fact_id,
            owner,
            "AUTHORITY_OWNED_BY",
            source_kind="derived_projection",
            authority_id=row.get("authority_id"),
        )

    nodes_list = sorted(nodes.values(), key=lambda x: (TYPE_ORDER.get(x["type"], 99), x["id"]))
    edges.sort(key=lambda x: x["id"])

    route_count = len(profile.get("routes", []))
    canonical_visible_edges = sum(1 for e in edges if e.get("source_kind") == "canonical_edge")
    derived_edges = len(edges) - canonical_visible_edges
    drive_nodes = drive_doc.get("nodes", [])

    summary = {
        "projection_kind": "A7_VISUALIZATION_SUMMARY",
        "non_authoritative": True,
        "source_commit_sha": args.commit_sha,
        "source_sequence": bootstrap.get("current_sequence"),
        "source_sequence_status": bootstrap.get("current_sequence_status"),
        "source_observed_at": bootstrap.get("observed_at"),
        "systems": len(systems),
        "repositories": len(repositories),
        "modules": len(modules),
        "project_identities": len(project_ids),
        "research_projects": len(research_projects),
        "fact_classes": len(facts),
        "execution_profiles": len(profiles),
        "routes": route_count,
        "canonical_edges_total": len(canonical_edges),
        "canonical_edges_visible": canonical_visible_edges,
        "derived_edges_visible": derived_edges,
        "graph_nodes": len(nodes_list),
        "graph_edges": len(edges),
        "drive_nodes_registered_but_not_publicly_projected": len(drive_nodes),
        "public_projection_rule": "Only canonical public-safe semantic metadata is projected. Provider-private/internal Drive topology is not emitted into the public graph.",
    }

    graph = {
        "schema_version": "1.0.0",
        "projection_kind": "A7_GRAPH_2D_3D",
        "non_authoritative": True,
        "source_commit_sha": args.commit_sha,
        "legend": [{"type": key, "color": value} for key, value in TYPE_COLORS.items()],
        "nodes": nodes_list,
        "edges": edges,
    }

    search: list[dict[str, Any]] = []
    for node in nodes_list:
        tokens = [
            node.get("id", ""),
            node.get("label", ""),
            node.get("type", ""),
            node.get("role", ""),
            node.get("fact_class", ""),
            node.get("repository_id", ""),
            node.get("working_ref", ""),
        ]
        search.append({
            "id": node["id"],
            "label": node["label"],
            "type": node["type"],
            "subtitle": node.get("role") or node.get("fact_class") or node.get("status") or node.get("repository_id") or "",
            "tokens": " ".join(str(x) for x in tokens if x).lower(),
            "url": node.get("site_url") or node.get("url"),
        })
    search.sort(key=lambda x: (TYPE_ORDER.get(x["type"], 99), x["label"].lower()))

    route_rows: list[dict[str, Any]] = []
    repo_by_id = {r.get("repository_id"): r for r in repositories if r.get("repository_id")}
    authority_by_id = {a.get("authority_id"): a for a in authority_rows if a.get("authority_id")}
    for route in profile.get("routes", []):
        module = module_by_id.get(route.get("module_id"), {})
        repository = repo_by_id.get(module.get("repository_id"), {})
        authority = authority_by_id.get(route.get("authority_id"), {})
        route_rows.append({
            "route_id": route.get("route_id"),
            "route_role": route.get("route_role"),
            "fact_class": route.get("fact_class"),
            "authority_id": route.get("authority_id"),
            "module_id": route.get("module_id"),
            "module_label": module.get("canonical_label"),
            "repository_id": module.get("repository_id"),
            "repository_full_name": repository.get("full_name") or repository.get("repository_full_name"),
            "working_ref": module.get("canonical_working_ref"),
            "site_url": module.get("public_site_url"),
            "writable_store": authority.get("writable_store"),
            "resolution_strategy": authority.get("resolution_strategy"),
            "project_instance_assertion": route.get("project_instance_assertion"),
        })

    matrix = {
        "schema_version": "1.0.0",
        "projection_kind": "A7_PROJECT_MODULE_MATRIX",
        "non_authoritative": True,
        "source_commit_sha": args.commit_sha,
        "execution_profile_id": profile_id,
        "route_columns": route_rows,
        "projects": [
            {
                "project_id": row.get("project_id"),
                "execution_profile_id": profile_id,
                "routes": [
                    {
                        "route_id": route.get("route_id"),
                        "module_id": route.get("module_id"),
                        "availability": "ROUTABLE",
                        "project_specific_instance": "NOT_ASSERTED_BY_A7",
                    }
                    for route in profile.get("routes", [])
                ],
            }
            for row in project_ids
        ],
    }

    authority_projection = {
        "schema_version": "1.0.0",
        "projection_kind": "A7_AUTHORITY_MATRIX",
        "non_authoritative": True,
        "source_commit_sha": args.commit_sha,
        "rows": [
            {
                "fact_class_id": fact_by_name.get(row.get("fact_class")),
                "fact_class": row.get("fact_class"),
                "materiality": fact_by_name.get(row.get("fact_class")) and fact_by_name and next((f.get("default_materiality") for f in facts if f.get("fact_class") == row.get("fact_class")), None),
                "authority_id": row.get("authority_id"),
                "scope_type": row.get("scope_type"),
                "owner_kind": row.get("owner_kind"),
                "owner_ref": row.get("owner_ref"),
                "writable_store": row.get("writable_store"),
                "resolution_strategy": row.get("resolution_strategy"),
                "rule": row.get("rule"),
            }
            for row in authority_rows
        ],
    }

    workspace_decision = load_json("registry/decisions/visualization-workspace.json")
    workspace_projection = dict(workspace_decision)
    workspace_projection["source_commit_sha"] = args.commit_sha
    workspace_projection["projection_kind"] = "A7_PINNED_VISUALIZATION_DECISION"
    workspace_projection["non_authoritative"] = True
    workspace_projection["source_path"] = "registry/decisions/visualization-workspace.json"

    outputs: dict[str, Any] = {
        "visualization-workspace.json": workspace_projection,
        "a7-summary.json": summary,
        "a7-graph.json": graph,
        "a7-search-index.json": {"schema_version": "1.0.0", "non_authoritative": True, "items": search},
        "project-module-matrix.json": matrix,
        "authority-projection.json": authority_projection,
        "a7-excalidraw.json": make_excalidraw(profile, module_by_id),
    }

    for filename, payload in outputs.items():
        (out / filename).write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")

    (out / "a7-architecture.mmd").write_text(mermaid_source(summary, profile, module_by_id), encoding="utf-8")

    source_hashes = {path: sha256_file(ROOT / path) for path in SOURCE_PATHS}
    output_hashes = {
        path.name: sha256_file(path)
        for path in sorted(out.iterdir())
        if path.is_file() and path.name != "derivation-manifest.json"
    }
    manifest = {
        "schema_version": "1.0.0",
        "projection_kind": "A7_DERIVATION_MANIFEST",
        "non_authoritative": True,
        "generator": "scripts/generate_visualizations.py",
        "source_commit_sha": args.commit_sha,
        "source_sequence": bootstrap.get("current_sequence"),
        "source_sequence_status": bootstrap.get("current_sequence_status"),
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "sources": [{"path": path, "sha256": digest} for path, digest in source_hashes.items()],
        "outputs": [{"path": name, "sha256": digest} for name, digest in output_hashes.items()],
        "privacy_boundary": "Public visualization excludes provider-private/internal Drive topology nodes; only the aggregate registered count is emitted.",
        "authority_boundary": "All generated files are projections. Canonical JSON/JSONL and live owning providers remain authoritative.",
    }
    (out / "derivation-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(
        "A7 VISUALIZATION DERIVATION: PASS "
        + "nodes=" + str(len(nodes_list))
        + " edges=" + str(len(edges))
        + " projects=" + str(len(project_ids))
        + " routes=" + str(route_count)
        + " output=" + str(out)
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
