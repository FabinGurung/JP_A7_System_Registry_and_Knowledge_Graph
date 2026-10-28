#!/usr/bin/env python3
"""Rebuild the A7 L1 roadmap projection directly from its checked-in registry.
This does not fetch, claim or rewrite external provider approval.
"""
import argparse,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P=R/"registry/roadmap.json"
# A7-specific website worklist; original source remains complete and audit-visible.
WORKLIST={"A7-N04","A7-N05","A7-N06","A7-N10","A7-N13"}
def build(commit):
    raw=P.read_bytes()
    reg=json.loads(raw)
    delivered=[{k:x.get(k) for k in ("id","stage","title","status","detail")} for x in reg["developed"]]
    backlog=[{k:x.get(k) for k in ("id","priority","title","state","done_when")} for x in reg["next"] if x["id"] in WORKLIST]
    pins=reg.get("pinned_task_ids",[])
    if len(pins)!=len(set(pins)) or not set(pins).issubset({x["id"] for x in backlog}): raise ValueError("Duplicate or unknown pinned task")
    pinned=[dict(next(x for x in backlog if x["id"]==tid),pin_reason=reg["pin_semantics"][tid]["reason"],task_boundary=reg["pin_semantics"][tid]["boundary"]) for tid in pins]
    if not delivered or not backlog or len(backlog)!=len(WORKLIST): raise ValueError("Roadmap source missing a workstream")
    # Show only dated, GitHub-verified local A7 evidence already recorded in the
    # owning bootstrap. This is a fixed historical observation, NOT live polling.
    boot=json.loads((R/"A7_BOOTSTRAP.json").read_text(encoding="utf-8"))
    local=boot.get("a7_operator_quickstart",{})
    ev=local.get("final_closeout_evidence",{})
    proof=None
    if local.get("final_closeout_ci")=="VERIFIED_FINAL_MAIN_WORKFLOWS" and ev.get("state")=="VERIFIED":
        proof={"sequence":local["sequence_id"],"source_path":"A7_BOOTSTRAP.json",
          "verified_commit_sha":ev["verified_against_main_commit"],
          "registry_run":ev["registry_run"],"pages_run":ev["pages_run"],
          "release_safeguard_run":ev["release_safeguard_run"],
          "conclusions":ev["conclusions"],
          "independent_http_body_readback":ev["independent_http_body_readback"],
          "historical_not_live":True}
    return {"verified_a7_provider_evidence":proof,"schema":"a7-roadmap-projection.v0.1","kind":"DERIVED_NOT_AUTHORITATIVE",
      "owner":"A7_ONLY","source_path":"registry/roadmap.json","source_sha256":hashlib.sha256(raw).hexdigest(),
      "site_build_commit":commit,"current_closed_sequence":reg["current_closed_sequence"],
      "developed":delivered,"next_a7":backlog,"pinned_a7":pinned,
      "caveat":"Registry-recorded statuses only. Check GitHub PRs, commits and Actions for current provider facts."}
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",required=True);p.add_argument("--commit-sha",required=True);a=p.parse_args()
    dst=Path(a.output);dst.parent.mkdir(exist_ok=True,parents=True)
    d=build(a.commit_sha);dst.write_text(json.dumps(d,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("A7 ROADMAP PROJECTION PASS closed="+d["current_closed_sequence"]+" delivered="+str(len(d["developed"]))+" a7_backlog="+str(len(d["next_a7"])))
