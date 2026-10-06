# A7 READ FIRST

## 1. Purpose

A7 is the GitHub-versioned semantic control plane for identities, authority rules, provider object references, aliases, typed edges, schemas, policies, lineage and generated-view definitions.

A7 is not a universal copy of every source file and is not permission to infer missing facts.

## 2. Bootstrap order

For any A7 task:

1. Read `A7_BOOTSTRAP.json`.
2. Resolve the requested entity by permanent A7 ID or governed alias.
3. Load applicable global policy.
4. Resolve the requested fact class.
5. Load the most-specific authority assignment: entity override → project override → module override → global fact class.
6. Load the originating provider policy.
7. Fetch the live provider when current state is required.
8. Verify provider object ID/revision/timestamp where available.
9. Classify candidate claims as declared authority, verified human-QA resolution, evidence, projection or unknown.
10. Apply `registry/authority/conflict-resolution.json`; never use recency unless the fact class explicitly permits it.
11. If unresolved material/safety conflict remains, open human QA instead of guessing.
12. Mutate only the declared writable authority.
13. Regenerate downstream projections.
14. Run validation/CI.
15. Provider-read back the result.
16. Close the same bounded A7 sequence; do not create a new sequence merely to acknowledge it.

## 3. AI behavior

The AI is a resolver/operator, not a source of truth.

Never:
- use chat memory as authority when a governed source exists;
- choose a value merely because it looks newer;
- invent a project-specific route;
- infer completion from an unlabeled image;
- silently reconcile conflicting provider claims;
- treat a communication statement as automatically proving its real-world claim;
- edit generated HTML/CSV/graphs to change an authoritative fact.

## 4. Conflict and human QA

Authority precedes recency. Provider truth and domain truth are distinct: Slack/Discord/email/WhatsApp may prove what was said; Drive may prove which file/revision exists; Sheets may prove exact cell state; GitHub may prove repository/ref/workflow state. The applicable fact-class contract decides whether those provider facts are also the domain authority.

If material evidence contradicts the designated domain authority, keep the current authority value, record the disagreement, and open a human-QA reconciliation case. If multiple valid authorities disagree, block the canonical mutation until QA or an explicit version rule resolves it.

A human-QA request must include:
- QA case ID;
- entity/project ID;
- disputed fact class and conflict type;
- each conflicting statement/value;
- provider/evidence references;
- associated conversation/evidence link when available;
- a short explicit question.

Preferred route: governed project Slack thread/channel, then email where Slack is unavailable or email is the governed responsible-person route. The confirming response must be provider-referenced before it can resolve the case.

## 5. Three-attempt fail-forward rule

For a connector/provider action that fails:

- attempts 1–3: retry only when a materially different or reasonable attempt is possible;
- after 3 failed attempts: record the deferred dependency/problem and continue the next independent task;
- never fabricate the blocked fact;
- mark the affected item `BLOCKED`, `UNVERIFIED` or `AWAITING_PROVIDER`;
- report the failed dependency and last error in closeout.

See `policies/global/fail-forward.json`.

## 6. Public safety

This repository is public. Store metadata and public-safe relationships, not confidential payloads. Private provider object IDs/labels require an explicit public-safety decision before publication. See `policies/global/public-safety.json`.

## 7. Writable and derived formats

Canonical writable:
- JSON for current normalized state;
- JSONL/NDJSON for append-only events, edges, aliases, provider observations and QA events.

Formal contracts:
- JSON Schema;
- PostgreSQL-compatible SQL DDL.

Generated/non-authoritative:
- CSV;
- Mermaid;
- graph JSON;
- search indexes;
- Markdown summaries;
- HTML;
- Excalidraw projection data;
- Three.js/3D graph data.

## 8. PostgreSQL status

A live PostgreSQL/Neon runtime is deferred while there is one primary writer and other users are read/search-only. SQL DDL is used as a formal relational language without requiring a database service.

## 9. Namespace separation

A7 is this GitHub semantic registry. Other established A-number namespaces remain separate systems and must not be silently renamed into A7. See `registry/entities/systems.json`.

## 10. Git-native closeout

Each bounded mutation has:
- sequence ID: `A7-SEQ-NNNNNN`;
- event IDs: `A7-EVT-NNNNNN-NNN`;
- PRE commit SHA;
- working branch;
- validation result;
- merged/final commit SHA;
- provider readback;
- final status.

A sequence may contain many events. Acknowledgement alone does not create another sequence.

## 11. Phase-2 authority engine

Canonical machine contracts:
- `registry/authority/fact-classes.json`
- `registry/authority/authority-map.json`
- `registry/authority/provider-roles.json`
- `registry/authority/conflict-resolution.json`
- `registry/authority/conflict-taxonomy.json`
- `registry/authority/vocabularies.json`
- `registry/authority/authority-overrides.jsonl`
- `registry/qa/human-qa-cases.jsonl`

The reference resolver in `scripts/a7_authority_engine.py` operates only on claims already classified from those contracts; it does not invent authority from a provider name.
