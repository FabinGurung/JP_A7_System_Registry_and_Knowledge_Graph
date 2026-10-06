# JP_A7_System_Registry_and_Knowledge_Graph

Canonical **A7 semantic registry, knowledge graph, authority map and AI control plane** for the JP engineering ecosystem.

## Current state

- System namespace: **A7**
- Repository provider ID: `1406572237`
- Default branch: `main`
- Visibility: public
- Current sequence: `A7-SEQ-000002` — **IN_PROGRESS**
- Phase 1 semantic-registry foundation: **COMPLETE**
- Phase 2 authority + conflict-resolution engine: **IN_PROGRESS**
- Live PostgreSQL/Neon runtime: **DEFERRED / NOT REQUIRED FOR CURRENT OPERATING MODEL**
- Canonical editable data: **JSON + JSONL**
- Formal contracts: **JSON Schema + PostgreSQL-compatible SQL DDL**
- Human/visual outputs: **generated projections only**

## Core rule

> The AI is the resolver/operator, not the authority.

A7 defines identity, aliases, source references, authority boundaries, typed relationships, policies and mutation lineage. It does **not** copy original engineering files into GitHub merely to normalize them.

## Authority model

| Concern | Authority |
| --- | --- |
| Semantic identity, governed aliases, relationships and A7 policy | This A7 registry |
| Provider-native state/content | The originating provider |
| Communication statement | The provider proves what was said; the domain fact still follows its fact-class authority contract |
| Specialist domain truth | The specialist system/module role explicitly assigned by authority policy |
| Generated HTML, CSV, Mermaid, graph and search files | Never authoritative; regenerated from canonical data |

## Conflict rule

**Authority before recency.** “Newest wins” is prohibited unless the applicable fact class explicitly permits timestamp/version arbitration. Unresolved material/safety conflicts go to human QA with evidence/context links; AI does not guess.

## Read first

1. `A7_BOOTSTRAP.json`
2. `A7_READ_FIRST.md`
3. Applicable policy profiles
4. Fact-class + authority + provider-role contracts
5. Canonical entity/edge/source records
6. Live provider reads required by the authority engine

## Repository layout

- `registry/` — canonical machine-readable records
- `registry/authority/` — fact classes, authority, provider roles and conflict engine
- `registry/qa/` — append-only human-QA cases
- `schemas/` — structural contracts
- `relational/` — PostgreSQL-compatible relational contract; no database runtime required
- `policies/` — global/provider/module/project/task operating rules
- `generated/` — derived outputs; never hand-edit facts here
- `scripts/` — validation/reference resolver/build tooling
- `.github/workflows/` — CI and later projection/deployment pipelines

## Public-repository warning

This repository is intentionally public for now. Do not commit secrets, private message bodies, confidential file contents, private personal information, credentials, tokens or restricted financial/engineering material.

## Git-native A7 closeout

A7 uses commit/branch/CI/provider-readback lineage instead of duplicating every routine registry mutation into Drive control sheets. Provider-specific PRE/POST evidence is still required when A7 actually mutates that external provider.
