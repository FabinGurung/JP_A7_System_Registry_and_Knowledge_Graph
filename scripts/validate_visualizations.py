#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED = {
    "a7-summary.json",
    "a7-graph.json",
    "a7-search-index.json",
    "project-module-matrix.json",
    "authority-projection.json",
    "a7-excalidraw.json",
    "a7-architecture.mmd",
    "derivation-manifest.json",
}

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", required=True)
    args = parser.parse_args()
    root = Path(args.data_dir)
    errors = []

    missing = sorted(REQUIRED - {p.name for p in root.iterdir() if p.is_file()})
    if missing:
        errors.append("missing outputs: " + ", ".join(missing))

    if not errors:
        summary = load(root / "a7-summary.json")
        graph = load(root / "a7-graph.json")
        search = load(root / "a7-search-index.json")
        matrix = load(root / "project-module-matrix.json")
        authority = load(root / "authority-projection.json")
        manifest = load(root / "derivation-manifest.json")

        if summary.get("non_authoritative") is not True:
            errors.append("summary must be explicitly non-authoritative")
        if graph.get("non_authoritative") is not True:
            errors.append("graph must be explicitly non-authoritative")
        if matrix.get("non_authoritative") is not True:
            errors.append("matrix must be explicitly non-authoritative")

        nodes = graph.get("nodes", [])
        edges = graph.get("edges", [])
        node_ids = {n.get("id") for n in nodes}
        if len(node_ids) != len(nodes):
            errors.append("graph node IDs must be unique")
        for edge in edges:
            if edge.get("source") not in node_ids or edge.get("target") not in node_ids:
                errors.append("graph contains dangling edge " + str(edge.get("id")))

        project_nodes = [n for n in nodes if n.get("type") == "project"]
        module_nodes = [n for n in nodes if n.get("type") == "module"]
        if len(project_nodes) != 28:
            errors.append("expected 28 project semantic nodes")
        if len(module_nodes) != 7:
            errors.append("expected 7 module nodes")
        if matrix.get("project_binding_count", len(matrix.get("projects", []))) != 28 and len(matrix.get("projects", [])) != 28:
            errors.append("expected 28 project matrix rows")
        if len(matrix.get("route_columns", [])) != 5:
            errors.append("expected 5 execution routes")
        if any(r.get("project_instance_assertion") != "NOT_ASSERTED_BY_A7" for r in matrix.get("route_columns", [])):
            errors.append("route projection must not assert specialist project instances")

        searchable = {x.get("id") for x in search.get("items", [])}
        if not node_ids.issubset(searchable):
            errors.append("every graph node must be searchable")

        if len(authority.get("rows", [])) < 21:
            errors.append("authority projection must include all current fact classes")

        forbidden_prefixes = ("GDRIVE-",)
        if any(str(n.get("id", "")).startswith(forbidden_prefixes) for n in nodes):
            errors.append("public graph must not emit Drive topology node IDs")
        if summary.get("drive_nodes_registered_but_not_publicly_projected", 0) < 1:
            errors.append("privacy boundary count missing")

        if manifest.get("non_authoritative") is not True:
            errors.append("derivation manifest must be non-authoritative")
        if not manifest.get("sources") or not manifest.get("outputs"):
            errors.append("derivation manifest must record source/output hashes")

    if errors:
        print("A7 VISUALIZATION VALIDATION: FAIL")
        for error in errors:
            print("- " + error)
        return 1

    print(
        "A7 VISUALIZATION VALIDATION: PASS "
        + "nodes=" + str(len(graph.get("nodes", [])))
        + " edges=" + str(len(graph.get("edges", [])))
        + " projects=" + str(len(matrix.get("projects", [])))
        + " routes=" + str(len(matrix.get("route_columns", [])))
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
