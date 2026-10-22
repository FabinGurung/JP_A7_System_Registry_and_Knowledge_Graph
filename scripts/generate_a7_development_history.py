#!/usr/bin/env python3
"""Build a read-only L1 A7 development history from the checked-out Git tree.
Provider-backed PR and Actions records come from the owning public GitHub repository
during Pages builds. CI/browser fixtures run offline and make no provider claims.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph"
BASE = "https://github.com/" + REPOSITORY
API = "https://api.github.com/repos/" + REPOSITORY

def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).strip()

def commits():
    raw = git("log", "--max-count=80", "--format=%H%x1f%cI%x1f%s%x1f%P%x1e", "HEAD")
    entries = []
    for block in raw.split("\x1e"):
        parts = block.strip().split("\x1f")
        if len(parts) != 4:
            continue
        sha, at, subject, parents = parts
        if not re.fullmatch(r"[0-9a-f]{40}", sha):
            raise ValueError("Invalid commit from git history")
        seq = re.search(r"\bA7-SEQ-\d{6}\b", subject)
        entries.append({
            "sha": sha, "committed_at": at, "subject": subject,
            "kind": "merge" if len(parents.split()) > 1 else "commit",
            "sequence": seq.group(0) if seq else None,
            "url": BASE + "/commit/" + sha,
        })
    if not entries:
        raise ValueError("No commits in current checked-out Git graph")
    return entries

def tags():
    out = git("tag", "--merged", "HEAD", "--list")
    arr = []
    for name in out.splitlines():
        if not re.fullmatch(r"[A-Za-z0-9_./-]{1,150}", name):
            continue
        sha = git("rev-list", "-n", "1", "refs/tags/" + name)
        at = git("log", "-1", "--format=%cI", sha)
        arr.append({"name": name, "sha": sha, "committed_at": at, "url": BASE + "/releases/tag/" + name})
    return sorted(arr, key=lambda x: x["committed_at"], reverse=True)

def get_json(path, token):
    req = Request(API + path, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + token,
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "A7-Pages-History-Builder",
    })
    with urlopen(req, timeout=22) as response:
        return json.load(response)

def owner_records(token, head):
    pulls = get_json("/pulls?state=closed&per_page=60&sort=updated&direction=desc", token)
    runs = get_json("/actions/runs?per_page=60", token)["workflow_runs"]
    prs = []
    for obj in pulls:
        if not obj.get("merged_at") or not obj.get("merge_commit_sha"):
            continue
        sha = obj["merge_commit_sha"]
        if not re.fullmatch(r"[0-9a-f]{40}", sha):
            continue
        # Don't show PRs whose merge is not an ancestor of this exact build.
        if subprocess.run(["git","-C",str(ROOT),"merge-base","--is-ancestor",sha,head],
                          capture_output=True).returncode != 0:
            continue
        url = obj.get("html_url", "")
        if not url.startswith(BASE + "/pull/"):
            continue
        prs.append({"number": obj["number"], "title": obj["title"], "merged_at": obj["merged_at"],
                    "merge_sha": sha, "url": url})
    actions = []
    for obj in runs:
        url = obj.get("html_url", "")
        if not url.startswith(BASE + "/actions/runs/"):
            continue
        sha = obj.get("head_sha", "")
        if not re.fullmatch(r"[0-9a-f]{40}", sha):
            continue
        actions.append({
            "id": obj["id"], "name": obj["name"], "status": obj["status"],
            "conclusion": obj.get("conclusion"), "head_sha": sha,
            "created_at": obj["created_at"], "url": url,
        })
    return prs[:24], actions[:24]

def build(offline=False):
    head = git("rev-parse", "HEAD")
    token = os.environ.get("GITHUB_TOKEN", "")
    if offline:
        prs, runs, basis = [], [], "OFFLINE_GIT_GRAPH_ONLY"
    else:
        if not token:
            raise ValueError("GITHUB_TOKEN required for provider-backed Pages release")
        prs, runs = owner_records(token, head)
        if not prs or not runs:
            raise ValueError("Cannot certify public GitHub PR/Actions provider records")
        basis = "GITHUB_API_AT_BUILD_AND_GIT_GRAPH"
    return {
        "schema": "a7-development-history.v0.1",
        "scope": "THIS_A7_REPOSITORY_ONLY",
        "repository": REPOSITORY, "source_sha": head,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "freshness": "STATIC_BUILD_SNAPSHOT_NOT_LIVE_POLLING",
        "provider_basis": basis,
        "limits": {"commits": 80, "merged_prs": 24, "recent_runs": 24},
        "commits": commits(), "tags": tags(),
        "pull_requests": prs, "workflow_runs": runs,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="site/data/development-history.json")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--require-provider", action="store_true")
    args = parser.parse_args()
    if args.offline and args.require_provider:
        parser.error("Offline cannot prove provider records")
    obj = build(offline=args.offline)
    if args.require_provider and obj["provider_basis"] != "GITHUB_API_AT_BUILD_AND_GIT_GRAPH":
        raise ValueError("Provider-required output lacks API evidence")
    target = ROOT / args.output
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("A7 DEVELOPMENT HISTORY PASS source=" + obj["source_sha"][:12] +
          " commits=" + str(len(obj["commits"])) +
          " merged_prs=" + str(len(obj["pull_requests"])) +
          " actions=" + str(len(obj["workflow_runs"])) +
          " mode=" + obj["provider_basis"])

if __name__ == "__main__":
    main()
