#!/usr/bin/env python3
"""A7 canonical AI-aided human guide: validation without network dependencies."""
from pathlib import Path
import json
import re

root=Path(__file__).resolve().parents[1]
policy=json.loads((root/"policies/global/ai-aided-product-guide.v0.1.json").read_text())
registry=json.loads((root/"registry/decisions/ai-aided-guide-adoption.v0.1.json").read_text())
guide=(root/"docs/AI_AIDED_PRODUCT_GUIDE_TEMPLATE_v0.1.md").read_text()
site=(root/"site/how-it-works.html").read_text()
homepage=(root/"site/index.html").read_text()
readme=(root/"README.md").read_text()
assert policy["schema"]=="fabin-a7://ai-aided-product-guide/0.1"
assert policy["policy_id"]=="A7-POL-AI-AIDED-INTERACTION-001"
assert policy["version"]=="0.1.0" and policy["status"]=="ACTIVE_GLOBAL_GUIDANCE"
assert registry["policy_id"]==policy["policy_id"] and registry["version"]==policy["version"]
assert len(policy["execution_sequence"])==7
assert [x["id"] for x in policy["execution_sequence"]]==[
 "UNDERSTAND","RESOLVE","NORMALIZE","EXECUTE","VERIFY","EXPLORE","TRACE"]
assert len(set(x["id"] for x in policy["execution_sequence"]))==7
assert set(policy["no_requirements_on_human"])=={
 "NO_JSON_AUTHORING","NO_MANUAL_PARAMETER_SCHEMA","NO_GITHUB_NAVIGATION_FOR_PRODUCT_USE","NO_UNJUSTIFIED_TECHNICAL_JARGON"}
assert policy["authority"]["global_semantic_map"]=="FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph"
assert len(policy["reproducibility"]["required_keys"])==6
assert policy["progressive_detail"]["levels"][-1]=="VERIFIED_INSTRUCTIONS"
assert policy["dimensions"]["4D"].startswith("Model components")
assert policy["dimensions"]["5D"].startswith("Verified quantities")
rows=registry["module_repositories"]
assert len(rows)==9 and len({x["repo"] for x in rows})==9
assert all(re.fullmatch(r"[A-Za-z0-9_-]{3,100}",x["repo"]) for x in rows)
assert sum(x["adoption"]=="PROPOSED_IN_PR" for x in rows)==2
assert {x["repo"] for x in rows if x["adoption"]=="PROPOSED_IN_PR"}=={
 "JP_A7_System_Registry_and_Knowledge_Graph","JP_Computer-Aided-Drawings"}
assert all(x["adoption"] in ("PROPOSED_IN_PR","REVIEWED_NOT_MODIFIED")
 for x in rows)
assert "How It Works" in guide and "How It Works" in site
assert "<main" in site and "assets/sky-theme.css" in site
assert "content=\"#eff8fc\"" in site and "aria-label=" in site
assert "how-it-works.html" in homepage and "How It Works" in readme
for phase in policy["execution_sequence"]:
    assert phase["id"] in guide and phase["id"] in site,phase["id"]
for target in ["3D","2D","4D","5D","SOURCE","GitHub","ChatGPT"]:
    assert target.lower() in (guide+site).lower(),target
assert "not the source of truth" in guide.lower() or "not the authority" in guide.lower()
assert "not the authority" in site.lower()
assert "private" in site.lower() and "unverified" in site.lower()
print("A7_AI_AIDED_GUIDE_CONTRACT_PASS policies=1 guide=1 repo_inventory=9")
