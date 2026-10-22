#!/usr/bin/env python3
"""Validate L1 A7 Git-only development history without trusting page-side data."""
import argparse
import json
from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser()
p.add_argument("--data-dir",default="site/data")
args=p.parse_args()
data=json.loads((R/args.data_dir/"development-history.json").read_text(encoding="utf-8"))
repo="FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph"
origin="https://github.com/"+repo
assert data["schema"]=="a7-development-history.v0.1"
assert data["scope"]=="THIS_A7_REPOSITORY_ONLY"
assert data["repository"]==repo
assert data["freshness"]=="STATIC_BUILD_SNAPSHOT_NOT_LIVE_POLLING"
assert data["provider_basis"] in {"OFFLINE_GIT_GRAPH_ONLY","GITHUB_API_AT_BUILD_AND_GIT_GRAPH"}
assert re.fullmatch(r"[0-9a-f]{40}",data["source_sha"])
assert data["commits"] and data["commits"][0]["sha"]==data["source_sha"]
assert len(data["commits"])<=80
assert len({x["sha"] for x in data["commits"]})==len(data["commits"])
assert all(re.fullmatch(r"[0-9a-f]{40}",x["sha"]) and x["url"]==origin+"/commit/"+x["sha"] and x["kind"] in ("commit","merge") for x in data["commits"])
assert all(x["url"].startswith(origin+"/releases/tag/") and re.fullmatch(r"[0-9a-f]{40}",x["sha"]) for x in data["tags"])
assert all(x["url"]==origin+"/pull/"+str(x["number"]) and re.fullmatch(r"[0-9a-f]{40}",x["merge_sha"]) for x in data["pull_requests"])
assert all(x["url"]==origin+"/actions/runs/"+str(x["id"]) and re.fullmatch(r"[0-9a-f]{40}",x["head_sha"]) for x in data["workflow_runs"])
if data["provider_basis"]=="GITHUB_API_AT_BUILD_AND_GIT_GRAPH":
    assert data["pull_requests"] and data["workflow_runs"],"No provider-backed PR and Actions data"
else:
    assert not data["pull_requests"] and not data["workflow_runs"],"Offline fixture must not fake provider records"
home=(R/"site/index.html").read_text(encoding="utf-8")
page=(R/"site/history.html").read_text(encoding="utf-8")
shell=(R/"site/assets/a7-site-shell.js").read_text(encoding="utf-8")
js=(R/"site/assets/development-history.js").read_text(encoding="utf-8")
assert 'href="history.html"' in home
assert "L1" in page and 'id="dhCommitList"' in page
assert 'id="dhPrList"' in page and 'id="dhActionList"' in page
assert 'id="dhSearch"' in page and 'id="dhKind"' in page
assert "development-history.json" in js and "textContent" in js
assert '["history.html","Development History"' in shell
assert 'const primary=routes.slice(0,6)' in shell
for item in ("legacy-overview.html","milestone.html","visualization-workspace.html"):
    assert 'href="'+item+'"' in page
print("A7 DEVELOPMENT HISTORY VALIDATION PASS owner=A7 l0=home l1=history git=authority")
