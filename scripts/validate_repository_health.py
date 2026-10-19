#!/usr/bin/env python3
"""Guard cross-domain ownership and dated provider health. No live availability implied."""
import json, re
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from generate_repository_health import build
R=Path(__file__).resolve().parents[1]
p=json.loads((R/"registry/decisions/ai-aided-guide-ownership-resolution.v0.2.json").read_text())
old=json.loads((R/"policies/global/ai-aided-product-guide.v0.1.json").read_text())
cad=p["specialized_owner_contracts"][0]
assert p["status"]=="ADOPTED_PUBLIC_SAFE" and p["historical_reference"]["policy_id"]==old["policy_id"]
assert p["historical_reference"]["not_a_current_specialist_template_authority"] is True
assert p["precedence"].startswith("THIS_DOMAIN_OWNERSHIP_DECISION_OVERRIDES")
assert cad["owner_repository"]=="FabinGurung/JP_Computer-Aided-Drawings"
assert cad["contract"]=="governance/aad/aad-domain-template.v0.1.json"
assert cad["relationship"]=="DOMAIN_NORMATIVE_OWNER"
source=R/"registry/providers/github-health-observation-20261019.json"
v=json.loads(source.read_text())
assert v["snapshot_date"]=="2026-10-19" and "NOT_MONITORING" in v["status"]
assert len(v["records"])==9 and len({x["id"] for x in v["records"]})==9
assert {x["id"] for x in v["records"]}=={"REPO-%06d"%i for i in range(1,10)}
assert all(re.fullmatch(r"[0-9a-f]{40}",x["main_sha"]) for x in v["records"])
assert all(x["deployment_run"]>0 for x in v["records"])
assert next(x for x in v["records"] if x["id"]=="REPO-000006")["health"]=="LATEST_MAIN_CI_AND_PAGES_FAILED"
assert next(x for x in v["records"] if x["id"]=="REPO-000003")["health"]=="DEPLOYED_READBACK_SUCCESS"
assert build("TEST")["non_authoritative"] and len(build("TEST")["records"])==9
html=(R/"site/repository-status.html").read_text()
js=(R/"site/assets/repository-status.js").read_text()
assert "repository-status.js" in html and "assets/sky-theme.css" in html
assert 'data/repository-health.json' in js and 'textContent' in js
assert 'href="repository-status.html"' in (R/"site/index.html").read_text()
assert "live" not in v["status"].lower()
assert "SEQ-000013" in (R/"docs/GALACTIC_ATLAS_ARC01_READ_FIRST.md").read_text() or "SEQ13" in (R/"docs/GALACTIC_ATLAS_ARC01_READ_FIRST.md").read_text()
print("A7 POLICY+REPO HEALTH AUDIT PASS owner=CAD indexed=9 R&D=BLOCKED")
