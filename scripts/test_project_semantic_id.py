#!/usr/bin/env python3
"""A7 semantic project identity source-first regression without private sources."""
from resolve_project_semantic_id import resolve
a=resolve("PRJ-000029")
assert (a["canonical_id"],a["state"],a["routing_allowed"])==("PRJ-000029","ACTIVE",True)
r=resolve("PRJ-000030")
assert (r["canonical_id"],r["state"],r["routing_allowed"])==("PRJ-000029","RETIRED_REDIRECT",False)
assert resolve("PRJ-999999")["state"]=="UNKNOWN"
for i in range(1,29):
    row=resolve(f"PRJ-{i:06d}")
    assert row["state"]=="ACTIVE" and row["routing_allowed"]
print("A7 SEMANTIC PROJECT RESOLVER PASS active=29 retired_aliases=1 no_second_binding=1")
