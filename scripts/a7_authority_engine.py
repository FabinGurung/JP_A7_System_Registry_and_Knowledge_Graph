#!/usr/bin/env python3
"""Deterministic reference resolver for already-classified A7 claims.

Provider discovery/classification happens before this resolver. This module never
guesses authority from recency or provider name.
"""
from __future__ import annotations
import json
from datetime import datetime

MATERIAL = {"MATERIAL", "SAFETY_CRITICAL"}

def _norm(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def _dt(value):
    if not value:
        return datetime.min
    return datetime.fromisoformat(value.replace("Z", "+00:00"))

def resolve(case):
    if case.get("schema_valid") is False:
        return {"outcome":"BLOCK_SCHEMA_INVALID"}

    if case.get("public_safety_allowed") is False:
        return {"outcome":"BLOCK_PUBLIC_SAFETY"}

    if case.get("requires_live_provider") and case.get("provider_unavailable") and int(case.get("attempts", 0)) >= 3:
        return {"outcome":"DEFER_PROVIDER_CONTINUE"}

    human = case.get("verified_human_qa_resolution")
    if human:
        if not human.get("qa_case_id") or not human.get("source_ref_id"):
            return {"outcome":"BLOCK_SCHEMA_INVALID","reason":"Human resolution requires qa_case_id and source_ref_id."}
        return {
            "outcome":"ACCEPT_VERIFIED_HUMAN_QA_RESOLUTION",
            "value":human.get("value"),
            "source_ref_id":human.get("source_ref_id"),
            "qa_case_id":human.get("qa_case_id")
        }

    if not case.get("authority_configured", False):
        return {"outcome":"BLOCK_NO_AUTHORITY"}

    claims = list(case.get("claims", []))
    authorities = [c for c in claims if c.get("claim_role") == "DECLARED_AUTHORITY"]
    evidence = [c for c in claims if c.get("claim_role") == "EVIDENCE"]
    projections = [c for c in claims if c.get("claim_role") == "PROJECTION"]

    if not authorities:
        return {"outcome":"BLOCK_NO_AUTHORITY"}

    values = {}
    for claim in authorities:
        values.setdefault(_norm(claim.get("value")), []).append(claim)

    strategy = case.get("timestamp_strategy", "NO_TIMESTAMP_ARBITRATION")

    if len(values) > 1:
        if strategy == "LATEST_AUTHORITY_REVISION":
            candidates = [c for c in authorities if c.get("effective_at") or c.get("observed_at")]
            if len(candidates) == len(authorities):
                chosen = max(candidates, key=lambda c: _dt(c.get("effective_at") or c.get("observed_at")))
            else:
                return {"outcome":"BLOCK_HUMAN_QA"}
        else:
            return {"outcome":"BLOCK_HUMAN_QA"}
    else:
        chosen = authorities[0]

    chosen_norm = _norm(chosen.get("value"))
    projection_diff = any(_norm(c.get("value")) != chosen_norm for c in projections)
    evidence_diff = any(_norm(c.get("value")) != chosen_norm for c in evidence)

    if evidence_diff and case.get("materiality", "MATERIAL") in MATERIAL:
        return {
            "outcome":"USE_AUTHORITY_OPEN_HUMAN_QA",
            "value":chosen.get("value"),
            "source_ref_id":chosen.get("source_ref_id")
        }

    if projection_diff:
        return {
            "outcome":"USE_AUTHORITY_REGENERATE_PROJECTION",
            "value":chosen.get("value"),
            "source_ref_id":chosen.get("source_ref_id")
        }

    if evidence_diff:
        return {
            "outcome":"USE_AUTHORITY_LOG_EVIDENCE_DIFFERENCE",
            "value":chosen.get("value"),
            "source_ref_id":chosen.get("source_ref_id")
        }

    return {
        "outcome":"ACCEPT_AUTHORITY",
        "value":chosen.get("value"),
        "source_ref_id":chosen.get("source_ref_id")
    }
