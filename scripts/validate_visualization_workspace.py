#!/usr/bin/env python3
"""Guard the pinned six-lane A7 visualization design against accidental drift."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = [
    ("CYTOSCAPE", "Cytoscape.js", "PLANNED_NOT_INSTALLED"),
    ("REACT_FLOW", "React Flow (XYFlow)", "PLANNED_NOT_INSTALLED"),
    ("TABLES", "Tables / relational matrices", "IMPLEMENTED"),
    ("MERMAID", "Mermaid", "GENERATED_SOURCE_ONLY"),
    ("EXCALIDRAW", "Excalidraw", "GENERATED_EXPORT_ONLY"),
    ("SPATIAL_3D", "Optional 3D spatial graph", "IMPLEMENTED_LIGHTWEIGHT"),
]

def check(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("A7 VISUALIZATION WORKSPACE VALIDATION: FAIL " + message)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir")
    args = parser.parse_args()

    source = "registry/decisions/visualization-workspace.json"
    doc = json.loads((ROOT / source).read_text(encoding="utf-8"))
    lanes = doc.get("ordered_pipeline", [])
    actual = [(x.get("id"), x.get("technology"), x.get("implementation_state_at_record")) for x in lanes]
    check(actual == EXPECTED, "six-lane order/roles/evidence statuses changed; requires governed decision and validator review")
    check([x.get("order") for x in lanes] == list(range(1, 7)), "incorrect lane order")
    check(doc.get("decision_state") == "ADOPTED_TARGET_ARCHITECTURE", "target architecture record missing")
    check(len(doc.get("read_first", [])) >= 7, "resumption and no-hallucination protocol incomplete")
    check(all(x.get("upgrade_gate") and x.get("observed_implementation") for x in lanes), "missing current state or upgrade gate")

    home = (ROOT / "site/index.html").read_text(encoding="utf-8")
    page = (ROOT / "site/visualization-workspace.html").read_text(encoding="utf-8")
    page_js = (ROOT / "site/assets/visualization-workspace.js").read_text(encoding="utf-8")
    gen = (ROOT / "scripts/generate_visualizations.py").read_text(encoding="utf-8")
    check('href="visualization-workspace.html"' in home and '📌' in home, "homepage pin missing")
    check('visualization-workspace.js' in page, "workspace JS entrypoint missing")
    check('data/visualization-workspace.json' in page_js, "workspace page must read generated decision")
    check(source in gen and '"visualization-workspace.json": workspace_projection' in gen, "generator not deriving decision record")

    if args.data_dir:
        output = json.loads((Path(args.data_dir) / "visualization-workspace.json").read_text(encoding="utf-8"))
        got = [(x.get("id"), x.get("technology"), x.get("implementation_state_at_record")) for x in output.get("ordered_pipeline", [])]
        check(got == actual, "generated published record differs from canonical JSON")
        check(output.get("source_path") == source and output.get("non_authoritative") is True, "projection is not source-linked/non-authoritative")
    print("A7 VISUALIZATION WORKSPACE VALIDATION: PASS six_roles=6 pinned=YES current_vs_target=EXPLICIT")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
