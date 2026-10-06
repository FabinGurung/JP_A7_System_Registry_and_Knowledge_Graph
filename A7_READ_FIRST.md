# A7 READ FIRST

## 1. Purpose

A7 is the GitHub-versioned semantic control plane for identities, authority rules, provider object references, aliases, typed edges, schemas, policies, lineage and generated-view definitions.

A7 is not a universal copy of every source file and is not permission to infer missing facts.

## 2. Bootstrap order

For any A7 task:

1. Read `A7_BOOTSTRAP.json`.
2. Resolve the requested entity by permanent A7 ID or governed alias.
3. Load applicable global policy.
4. Load the authority assignment for the requested fact class.
5. Traverse typed edges only as needed.
6. Fetch the live authoritative provider when the task depends on provider state.
7. Verify provider object ID/revision/timestamp where available.
8. Normalize only supported facts.
9. Mutate only the declared writable authority for that data class.
10. Regenerate downstream projections.
11. Run validation/CI.
12. Provider-read back the result.
13. Close the same bounded A7 sequence; do not create a new sequence merely to acknowledge it.

## 3. AI behavior

The AI is a resolver/operator, not a source of truth.

Never:
- use chat memory as authority when a governed source exists;
- choose a value merely because it looks newer;
- invent a project-specific route;
- infer completion from an unlabeled image;
- silently reconcile conflicting provider claims;
- edit generated HTML/CSV/graphs to change an authoritative fact.

## 4. Conflict and human QA

Apply the authority map first. If policy does not resolve a material conflict, create a human-QA case rather than guessing.

A human-QA request should include:
- entity/project ID;
- disputed fact class;
- each conflicting statement/value;
- provider/evidence references;
- the associated conversation/evidence link when available;
- a short explicit question that can resolve the ambiguity.

Preferred communication channel is the governed project Slack thread/channel; email may be used where Slack is unavailable or the responsible person is defined through email. The confirming reply becomes provider evidence.

## 5. Three-attempt fail-forward rule

For a connector/provider action that fails:

- attempts 1–3: retry only when a materially different or reasonable attempt is possible;
- after 3 failed attempts: record the deferred dependency/problem and continue the next independent task;
- never fabricate the blocked fact;
- mark the affected item `BLOCKED`, `UNVERIFIED` or `AWAITING_PROVIDER`;
- report the failed dependency and error summary in the closeout.

See `policies/global/fail-forward.json`.

## 6. Public safety

This repository is public. Store metadata and public-safe relationships, not confidential payloads. Private provider object IDs/labels require an explicit public-safety decision before publication. See `policies/global/public-safety.json`.

## 7. Writable and derived formats

Canonical writable:
- JSON for current normalized state;
- JSONL/NDJSON for append-only events, edges, aliases and provider observations.

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
