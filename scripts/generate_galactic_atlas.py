#!/usr/bin/env python3
"""Generate a PUBLIC-SAFE, non-authoritative read model of A7's repo catalogue."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "registry/entities/repositories.json"
LAYOUT = ROOT / "registry/decisions/galactic-atlas-ui.v0.1.json"
PROVIDER = ROOT / "registry/providers/galactic-atlas-arc02-observation-20261020.json"
SECTORS = ROOT / "registry/decisions/galactic-atlas-sectors.v0.1.json"
ARC04 = ROOT / "registry/decisions/galactic-atlas-arc04-routes.v0.1.json"
MODULES = ROOT / "registry/entities/modules.json"
EDGES = ROOT / "registry/edges/edges.jsonl"
ALLOWED_HOSTS = ("https://github.com/FabinGurung/",
                 "https://fabingurung.github.io/")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build():
    meta = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    ui = json.loads(LAYOUT.read_text(encoding="utf-8"))
    source = {r["repository_id"]: r for r in meta["repositories"]}
    sector_data = json.loads(SECTORS.read_text(encoding="utf-8"))
    assert sector_data["status"] == "ADOPTED_PRESENTATION_TAXONOMY"
    sector_lookup = {x["repository_id"]: x["sector_id"] for x in sector_data["assignments"]}
    valid_sectors = {s["id"] for s in sector_data["sectors"]}
    assert len(sector_data["assignments"]) == len(sector_lookup) == 9
    assert set(sector_lookup) == set(source), "Each station requires exactly one sector"
    assert valid_sectors == {"CONTROL","ENGINEERING","OPERATIONS","KNOWLEDGE","ADJACENT"}
    assert all(x in valid_sectors for x in sector_lookup.values())
    assert sector_lookup["REPO-000001"] == "CONTROL"
    provider = json.loads(PROVIDER.read_text(encoding="utf-8"))
    assert provider["status"] == "DATED_SNAPSHOT_NOT_LIVE_MONITOR"
    evidence = {item["id"]: item for item in provider["records"]}
    assert set(evidence) == set(source) and len(evidence) == 9, "Arc02 observation must cover exactly the 9 registered systems"
    stations = []
    assert len(source) == 9 and len(ui["systems"]) == 9
    for shape in ui["systems"]:
        ident = shape["id"]
        entry = source[ident]
        item = evidence[ident]
        assert entry["current_slug"] == item["slug"], "Provider snapshot repository identity mismatch"
        assert len(item["main_sha"]) == 40 and item["deployment"]["id"] > 0
        assert item["deployment"]["branch"] == item["production_branch"]
        name = entry["repository_full_name"]
        assert name.startswith("FabinGurung/"), "Untrusted owner"
        site = entry.get("public_site_url")
        assert site and site.startswith(ALLOWED_HOSTS[1]), "Unapproved Pages URL"
        url = "https://github.com/" + name
        assert url.startswith(ALLOWED_HOSTS[0])
        deep = []
        for deep_item in shape.get("deep_links", []):
            if "github_path" in deep_item:
                link = url + "/blob/main/" + deep_item["github_path"]
            else:
                assert ".." not in deep_item["path"] and "://" not in deep_item["path"]
                link = site.rstrip("/") + "/" + deep_item["path"]
            if not link.startswith(ALLOWED_HOSTS):
                raise ValueError("Untrusted deep link")
            deep.append({"label": deep_item["label"], "url": link})
        stations.append({
            "id": ident, "title": shape["label"], "short": shape["short"],
            "role": shape["role"], "zone": shape["zone"],
            "sector": sector_lookup[ident],
            "azimuth": shape["azimuth"], "radial": shape["radial"],
            "summary": shape["summary"], "owns": shape["owns"],
            "does_not_own": shape.get("does_not_own"),
            "module_repository": name, "github_url": url, "website_url": site,
            "source_status_observation": entry.get("deployment_status"),
            "source_observed_at": entry.get("last_verified_at"),
            "deep_links": deep,
            "provider_evidence": {
                "observation_id": provider["observation_id"],
                "observed_date": provider["observed_date"],
                "not_live": True,
                "provider_label": item["provider_label"],
                "main_sha": item["main_sha"],
                "publication_branch": item["production_branch"],
                "last_successful_publication": item["deployment"],
                "related_workflow": item["latest_check"],
                "capability": item["capability"],
                "owner_gate": item["gate"],
                "dependency_note": item["dependency_note"],
                "dependency_verified": False
            }
        })
    # Arc04 projects ONLY admitted canonical module-navigation edges; the
    # display-only future candidates are not admitted into registry/edges.
    arc04 = json.loads(ARC04.read_text(encoding="utf-8"))
    assert arc04["status"] == "ADOPTED_PUBLIC_PRESENTATION_ONLY"
    assert arc04["source_commit_sha"] and len(arc04["source_commit_sha"]) == 40
    assert arc04["boundaries"]["provider_verified_runtime_handoff_count"] == 0
    assert arc04["boundaries"]["proposals_are_not_canonical_edges"]
    module_source = json.loads(MODULES.read_text(encoding="utf-8"))
    module_map = {m["module_id"]: m["repository_id"] for m in module_source["modules"]}
    assert len(module_map) == len(module_source["modules"])
    admitted = set(arc04["admitted_edge_ids"])
    assert len(admitted) == len(arc04["admitted_edge_ids"])
    routes = []
    for lineno, raw in enumerate(EDGES.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        edge = json.loads(raw)
        if edge["edge_id"] not in admitted:
            continue
        assert edge["relation_type"] == arc04["admitted_canonical_edge_type"]
        source_id, target_id = module_map[edge["from_entity_id"]], module_map[edge["to_entity_id"]]
        assert source_id != target_id and source_id in source and target_id in source
        routes.append({
            "id": edge["edge_id"], "from": source_id, "to": target_id,
            "relation_type": edge["relation_type"],
            "verification": "DOCUMENTED_NAVIGATION_ONLY", "runtime_verified": False,
            "authority_transfer": False, "evidence_observed_at": edge["observed_at"],
            "evidence_url": "https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph/blob/"
              + arc04["source_commit_sha"] + "/registry/edges/edges.jsonl#L" + str(lineno),
            "source_path": "registry/edges/edges.jsonl",
            "source_commit_sha": arc04["source_commit_sha"],
            "owner_fact_scope": "A7 module-navigation metadata",
            "limitation": edge["note"]
        })
    assert {r["id"] for r in routes} == admitted
    proposed = []
    proposal_ids = set()
    for item in arc04["proposals"]:
        assert item["state"] == "PROPOSED_UNVERIFIED"
        assert item["proposal_id"] not in proposal_ids
        proposal_ids.add(item["proposal_id"])
        assert item["from_repository_id"] in source and item["to_repository_id"] in source
        assert item["from_repository_id"] != item["to_repository_id"]
        proposed.append({
            "id": item["proposal_id"], "from": item["from_repository_id"],
            "to": item["to_repository_id"], "label": item["label"],
            "purpose": item["purpose"], "relation_type": "CANDIDATE_INTEGRATION",
            "verification": "PROPOSED_UNVERIFIED", "runtime_verified": False,
            "authority_transfer": False, "source_path": "registry/decisions/galactic-atlas-arc04-routes.v0.1.json",
            "evidence_url": None, "source_commit_sha": None,
            "limitation": "Design proposal only; no provider-verified transfer or interface."
        })
    return {
        "schema": "a7://galactic-atlas-read-projection/0.1",
        "arc": "GALACTIC_ATLAS_ARC_02_INSPECTOR", "navigation_arc": "GALACTIC_ATLAS_ARC_03_SECTORS",
        "relationship_arc": "GALACTIC_ATLAS_ARC_04_EVIDENCE_GATED_ROUTES",
        "sector_taxonomy_presentation_only": True, "non_authoritative": True,
        "provider_observation_date": provider["observed_date"],
        "provider_snapshot_not_live": True,
        "catalogue_role": ui["ownership_rule"],
        "fact_scope_note": ui["fact_scope_note"],
        "source_revisions": {
            "registry/entities/repositories.json": digest(CATALOGUE),
            "registry/decisions/galactic-atlas-ui.v0.1.json": digest(LAYOUT),
            "registry/providers/galactic-atlas-arc02-observation-20261020.json": digest(PROVIDER),
            "registry/decisions/galactic-atlas-sectors.v0.1.json": digest(SECTORS),
            "registry/decisions/galactic-atlas-arc04-routes.v0.1.json": digest(ARC04),
            "registry/entities/modules.json": digest(MODULES),
            "registry/edges/edges.jsonl": digest(EDGES)},
        "sectors": [{**s, "count": sum(x == s["id"] for x in sector_lookup.values())}
                    for s in sector_data["sectors"]],
        "sector_count": len(sector_data["sectors"]),
        "station_count": len(stations),
        "stations": stations,
        "route_count": len(routes), "candidate_count": len(proposed),
        "verified_runtime_handoff_count": 0,
        "routes": routes, "candidate_routes": proposed,
        "links": [{"from": "REPO-000001", "to": x["id"],
                   "type": "CATALOGUE_ROUTES_TO", "authority_transfer": False}
                  for x in stations if x["id"] != "REPO-000001"]
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", required=True)
    p.add_argument("--commit-sha", required=True)
    args = p.parse_args()
    result = build()
    result["build_commit_sha"] = args.commit_sha
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print("A7 GALACTIC ATLAS DERIVATION PASS stations=%d edges=%d" %
          (len(result["stations"]), len(result["links"])))


if __name__ == "__main__":
    main()
