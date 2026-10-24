#!/usr/bin/env python3
"""Hard gate: public-safe source-backed Arc07 navigation and preserved legacy page contracts."""
import json
import re
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / "scripts"))
from generate_resource_navigator import build

d = build("QA_LOCAL_COMMIT")
assert d["schema"] == "a7-resource-navigator.v0.1"
assert d["sequence_id"] == "A7-SEQ-000034"
assert d["kind"] == "DERIVED_PUBLIC_REFERENCE_NAVIGATION"
assert re.fullmatch(r"[0-9a-f]{64}", d["source_sha256"])
assert d["authority"] == "PUBLIC_LINK_INDEX_NOT_DOMAIN_AUTHORITY"
assert len(d["organizations"]) == 1, "Initial release allows A7-only grouping"
ids = set()
resource_count = 0
external_prefix = "https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph/blob/main/"
for org in d["organizations"]:
    assert org["classification"] == "PRESENTATION_GROUP_NOT_LEGAL_ORGANIZATION"
    assert org["id"] not in ids; ids.add(org["id"])
    for project in org["projects"]:
        assert project["classification"] == "PUBLIC_A7_WEBSITE_NOT_CLIENT_PROJECT"
        assert project["id"] not in ids; ids.add(project["id"])
        for category in project["categories"]:
            assert category["id"] not in ids; ids.add(category["id"])
            for resource in category["resources"]:
                assert resource["id"] not in ids; ids.add(resource["id"])
                assert resource["kind"] in {"PAGE","DOCUMENT","RESOURCE","SOURCE"}
                assert all(len(resource[k]) > 4 for k in ("name","note","source_path"))
                path = resource["source_path"]
                assert not (path.startswith("/") or ".." in Path(path).parts)
                assert (R / path).is_file(), path
                href = resource["href"]
                if href.startswith("https://"):
                    assert href == external_prefix + path, href
                else:
                    assert re.fullmatch(r"[a-z0-9-]+\.html", href), href
                    assert path == "site/" + href
                resource_count += 1
assert resource_count == 9
source = json.dumps(d).lower()
assert "drive.google.com" not in source and "docs.google.com" not in source
for forbidden in ("password", "secret_token", "private_drive", "client_address", "acl_list"):
    assert forbidden not in source
h = (R / "site/resource-navigator.html").read_text()
j = (R / "site/assets/resource-navigator.js").read_text()
css = (R / "site/assets/resource-navigator.css").read_text()
shell = (R / "site/assets/a7-site-shell.js").read_text()
for marker in ("rnOrganizations", "rnProjects", "rnCategories", "rnResources", "rnSearch", "rnReset", "rnStatus"):
    assert 'id="' + marker + '"' in h
assert "data/resource-navigator.json" in j
assert "textContent" in j and "innerHTML" not in j
assert "resource-navigator.html" in shell and "developer-dock.html" in shell
assert "@media" in css and ":focus-visible" in css
for old in ("site/index.html","site/memory-wall.html","site/history.html","site/roadmap.html","site/developer-dock.html"):
    assert (R / old).is_file()
assert "id=\"interface-vocabulary\"" in (R / "site/memory-wall.html").read_text()
print("A7 ARC07 RESOURCE NAV PASS organizations=1 projects=1 categories=3 resources=9 private=0")
