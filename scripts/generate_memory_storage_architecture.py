#!/usr/bin/env python3
"""Build A7 Memory Wall Collection 05 from public-safe checked-in curation."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "registry/curations/memory-storage-architecture.v0.1.json"

def build(commit_sha):
    raw = SOURCE.read_bytes()
    doc = json.loads(raw)
    assert doc["collection_id"] == "A7-MEM-STORAGE-ARCH-007"
    assert doc["public_safe"] is True and doc["read_only"] is True
    assert len(doc["formats"]) == 7 and len(doc["distinctions"]) == 3
    return {
        **doc,
        "kind": "DERIVED_PUBLIC_OPERATING_REFERENCE",
        "source_path": str(SOURCE.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "site_build_commit": commit_sha
    }

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--output", required=True)
    p.add_argument("--commit-sha", required=True)
    args = p.parse_args()
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    doc = build(args.commit_sha)
    target.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("A7 MEMORY COLLECTION 05 PASS formats=7 roles=3 public=1")
