#!/usr/bin/env python3
"""Derive public-safe A7 Resource Navigator from its checked-in manifest."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "registry/curations/resource-navigator.v0.1.json"

def build(commit_sha):
    raw = SOURCE.read_bytes()
    data = json.loads(raw)
    assert data["collection_id"] == "A7-RN-001" and data["public_safe"] is True
    assert data["read_only"] is True and data["owner"] == "A7_ONLY"
    return {
        **data,
        "kind": "DERIVED_PUBLIC_REFERENCE_NAVIGATION",
        "source_path": str(SOURCE.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "site_build_commit": commit_sha
    }

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    ap.add_argument("--commit-sha", required=True)
    args = ap.parse_args()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    data = build(args.commit_sha)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("A7 RESOURCE NAVIGATOR built: public-safe, source-derived")
