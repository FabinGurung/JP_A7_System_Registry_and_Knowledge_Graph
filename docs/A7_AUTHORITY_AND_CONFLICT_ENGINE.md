# A7 Authority + Conflict Resolution Engine

## Purpose

Phase 2 converts the Phase-1 authority idea into a deterministic machine contract.

A7 distinguishes **provider truth** from **domain truth**. A provider can prove its own object/message/cell/file state; that does not automatically make every statement inside that provider the canonical engineering/operational fact.

## Resolution order

1. Resolve entity and fact class.
2. Apply most-specific authority scope: entity → project → module → global.
3. Read provider policy.
4. Fetch live provider when current state is required.
5. Classify claims.
6. Validate schema/source references.
7. Apply authority before recency.
8. Use timestamp/version arbitration only when the fact class explicitly permits it.
9. Keep canonical authority when a projection is stale and regenerate the projection.
10. Keep canonical authority when material evidence contradicts it, but open a human-QA reconciliation case.
11. Block when valid authoritative values conflict.
12. After three provider failures, defer that dependency and continue independent work.
13. Apply public-safety gate before public projection.
14. Mutate only the writable authority and append A7 lineage.

## Provider truth examples

- GitHub: repository/ref/commit/workflow state.
- Drive: file/folder ID, source bytes, revision and provider metadata.
- Sheets: exact cell/range state.
- Slack/Discord/email/WhatsApp: what was communicated and when.

These are not automatically interchangeable with domain truth.

## Human QA

Material unresolved conflicts create a case such as `A7-QA-000001`. The request should be sent to the governed Slack thread/channel or responsible email route with the story/evidence link. A human reply must be captured as provider evidence before canonical mutation.

## PostgreSQL

The SQL file is a formal relational contract only. The live runtime remains JSON/JSONL + Git because A7 currently has one primary writer and read/search-only consumers.
