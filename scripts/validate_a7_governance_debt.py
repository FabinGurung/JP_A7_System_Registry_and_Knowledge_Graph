#!/usr/bin/env python3
"""A7 release gate: never confuse our local UI debts with other provider's acts."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
b=json.loads((R/"registry/governance/debt-boundaries.v1.json").read_text())
r=json.loads((R/"registry/roadmap.json").read_text())
boot=json.loads((R/"A7_BOOTSTRAP.json").read_text())
assert b["owner"]=="A7_ONLY"
assert b["sequence"]=="A7-SEQ-000030"  # Original governance reconciliation checkpoint remains immutable
assert r["current_closed_sequence"]==boot["current_sequence"]
assert int(r["current_closed_sequence"].split("-")[-1]) >= int(b["sequence"].split("-")[-1])
assert len(b["a7_local_tasks"])==4 and len(b["external_non_gate_dependencies"])>=6
assert {x["id"] for x in b["external_non_gate_dependencies"]}.issuperset({"A7-N01","A7-N02"})
assert all(x["status"] not in ("CLOSED","PASS") for x in b["external_non_gate_dependencies"])
assert b["arc06_entry_contract"]["historical_debts_not_reclassified_as_completed"]
assert b["arc06_entry_contract"]["private_drive_writes"] is False
assert boot["a7_governance_debt_boundary"]["external_historical_acks_closed"] is False
doc=(R/"docs/ROADMAP.md").read_text()
assert r["current_closed_sequence"] in doc and "A7-SEQ-000021" not in doc
assert (R/"scripts/generate_a7_roadmap.py").is_file()
print("A7 GOV DEBT BOUNDARY PASS local=4 external=open arc06_scope=A7_ONLY")
