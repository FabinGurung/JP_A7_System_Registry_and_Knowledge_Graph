#!/usr/bin/env python3
"""Validate public-safe A7 development roadmap, cross-repo links and sequence boundary."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
obj=json.loads((ROOT/"registry/roadmap.json").read_text(encoding="utf-8"))
assert obj["roadmap_id"]=="A7-ROADMAP-20261009"
assert obj["current_closed_sequence"]=="A7-SEQ-000012"
assert obj["current_staged_sequence"]=="A7-SEQ-000013"
assert len(obj["developed"])>=8 and len(obj["next"])>=6
assert len({x["id"] for x in obj["developed"]+obj["next"]})==len(obj["developed"]+obj["next"])
assert (ROOT/"site/roadmap.html").is_file()
assert (ROOT/"docs/ROADMAP.md").is_file()
assert "roadmap.html" in (ROOT/"site/index.html").read_text(encoding="utf-8")
assert "HISTORICAL" not in obj.get("status","")
assert "DO_NOT_RESUME" in " ".join(obj["strict_boundaries"])
assert "HANDOVER_TO_A7_20261009.md" in obj["crosslinks"]["rd_handover"]
print("A7 ROADMAP VALIDATION: PASS")
