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
ALLOWED_HOSTS = ("https://github.com/FabinGurung/",
                 "https://fabingurung.github.io/")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build():
    meta = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    ui = json.loads(LAYOUT.read_text(encoding="utf-8"))
    source = {r["repository_id"]: r for r in meta["repositories"]}
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
                assert ".." not in deep_item["path"] and "://" not in item["path"]
                link = site.rstrip("/") + "/" + item["path"]
            if not link.startswith(ALLOWED_HOSTS):
                raise ValueError("Untrusted deep link")
            deep.append({"label": deep_item["label"], "url": link})
        stations.append({
            "id": ident, "title": shape["label"], "short": shape["short"],
            "role": shape["role"], "zone": shape["zone"],
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
    return {
        "schema": "a7://galactic-atlas-read-projection/0.1",
        "arc": "GALACTIC_ATLAS_ARC_02_INSPECTOR", "non_authoritative": True,
        "provider_observation_date": provider["observed_date"],
        "provider_snapshot_not_live": True,
        "catalogue_role": ui["ownership_rule"],
        "fact_scope_note": ui["fact_scope_note"],
        "source_revisions": {
            "registry/entities/repositories.json": digest(CATALOGUE),
            "registry/decisions/galactic-atlas-ui.v0.1.json": digest(LAYOUT),
            "registry/providers/galactic-atlas-arc02-observation-20261020.json": digest(PROVIDER)},
        "station_count": len(stations),
        "stations": stations,
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
