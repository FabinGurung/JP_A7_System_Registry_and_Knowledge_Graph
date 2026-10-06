#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from a7_authority_engine import resolve

cases = json.loads((ROOT / "tests/authority/test-cases.json").read_text(encoding="utf-8"))["cases"]
errors=[]
for case in cases:
    result=resolve(case)
    if result.get("outcome") != case["expected_outcome"]:
        errors.append(f"{case['name']}: expected {case['expected_outcome']} got {result}")

if errors:
    print("A7 AUTHORITY RESOLVER TESTS: FAIL")
    for err in errors:
        print("- "+err)
    raise SystemExit(1)

print(f"A7 AUTHORITY RESOLVER TESTS: PASS ({len(cases)} cases)")
