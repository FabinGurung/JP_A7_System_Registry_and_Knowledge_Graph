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
ALLOWED_HOSTS = ("https://github.com/FabinGurung/",
                 "https://fabingurung.github.io/")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build():
    meta = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    ui = json.loads(LAYOUT.read_text(encoding="utf-8"))
    source = {r["repository_id"]: r for r in meta["repositories"]}
    stations = []
    assert len(source) == 9 and len(ui["systems"]) == 9
    for shape in ui["systems"]:
        ident = shape["id"]
        entry = source[ident]
        name = entry["repository_full_name"]
        assert name.startswith("FabinGurung/"), "Untrusted owner"
        site = entry.get("public_site_url")
        assert site and site.startswith(ALLOWED_HOSTS[1]), "Unapproved Pages URL"
        url = "https://github.com/" + name
        assert url.startswith(ALLOWED_HOSTS[0])
        deep = []
        for item in shape.get("deep_links", []):
            if "github_path" in item:
                link = url + "/blob/main/" + item["github_path"]
            else:
                assert ".." not in item["path"] and "://" not in item["path"]
                link = site.rstrip("/") + "/" + item["path"]
            if not link.startswith(ALLOWED_HOSTS):
                raise ValueError("Untrusted deep link")
            deep.append({"label": item["label"], "url": link})
        stations.append({
            "id": ident, "title": shape["label"], "short": shape["short"],
            "role": shape["role"], "zone": shape["zone"],
            "azimuth": shape["azimuth"], "radial": shape["radial"],
            "summary": shape["summary"], "owns": shape["owns"],
            "does_not_own": shape.get("does_not_own"),
            "module_repository": name, "github_url": url, "website_url": site,
            "source_status_observation": entry.get("deployment_status"),
            "source_observed_at": entry.get("last_verified_at"),
            "deep_links": deep
        })
    return {
        "schema": "a7://galactic-atlas-read-projection/0.1",
        "arc": ui["arc"], "non_authoritative": True,
        "catalogue_role": ui["ownership_rule"],
        "fact_scope_note": ui["fact_scope_note"],
        "source_revisions": {
            "registry/entities/repositories.json": digest(CATALOGUE),
            "registry/decisions/galactic-atlas-ui.v0.1.json": digest(LAYOUT)},
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
