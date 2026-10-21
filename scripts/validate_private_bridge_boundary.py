#!/usr/bin/env python3
"""A7 public-safe observation of private provider boundary; never imports A9 data."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
a7=json.loads((ROOT/"A7_BOOTSTRAP.json").read_text(encoding="utf-8"))
a9=json.loads((ROOT/"A9_GIT_DRIVE_BOOTSTRAP.json").read_text(encoding="utf-8"))
road=json.loads((ROOT/"registry/roadmap.json").read_text(encoding="utf-8"))
b=a7["main_library_bridge"]
x=a9["private_bridge_dated_observation"]
assert b["status"]=="PRIVATE_MAIN_PUBLIC_GITHUB_IDENTITY_PROJECTION_PROVIDER_VERIFIED__HISTORICAL_ACK_OPEN"
assert b["historical_parity"]=="NOT_VERIFIED"
assert b["local_main_consumed_cursor_ack"] is False
assert b["private_historical_source_content_parity"] is False
assert b["public_safe_private_provider_readback"]=="CONFIRMED__NO_PRIVATE_PROVIDER_IDS_PUBLISHED"
assert x["result"]=="CURRENT_PUBLIC_GITHUB_IDENTITY_METADATA_REGISTERED_IN_PRIVATE_MAIN"
assert x["private_main_or_local_ids_in_public_record"] is False
assert x["full_historical_parity_verified"] is False
assert x["local_main_cursor_ack"] is False
assert x["bulk_candidate_csv_imported"] is False
assert a9["scope_limits"]["private_drive_main_library_migrated"] is False
assert a9["scope_limits"]["a9_full_controls_migrated"] is False
assert a9["scope_limits"]["legacy_controls_superseded"] is False
assert road["current_staged_sequence"]=="A7-SEQ-000013"
assert "HISTORIC_A9_SOURCE_AND_CURSOR_ACK_OPEN" in road["next"][1]["state"] or any("HISTORIC_A9_SOURCE_AND_CURSOR_ACK_OPEN" in y["state"] for y in road["next"])
txt=(ROOT/"docs/MAIN_LIBRARY_GITHUB_BRIDGE.md").read_text(encoding="utf-8")
assert "candidate CSV files were **not imported" in txt
assert "authenticated Local-to-Main consumed-cursor ACK" in txt
assert "private Main identity projection" in txt
assert "no runtime integration" in txt
print("A7 PRIVATE BRIDGE PUBLIC BOUNDARY PASS private_identity_projection=observed historic_ACK=OPEN private_IDs=0")
