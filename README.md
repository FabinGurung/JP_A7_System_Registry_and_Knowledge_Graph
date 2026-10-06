# JP_A7_System_Registry_and_Knowledge_Graph

Canonical **A7 semantic registry, knowledge graph, authority map and AI control plane** for the JP engineering ecosystem.

## Current state

- System namespace: **A7**
- Repository provider ID: `1406572237`
- Default branch: `main`
- Visibility: public
- Current bootstrap sequence: `A7-SEQ-000001`
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
| Semantic identity, aliases, relationships and A7 policy | This A7 registry |
| Original engineering files/evidence | Original provider, normally Google Drive or another declared provider |
| Specialist domain truth | The specialist system explicitly assigned by authority policy |
| Generated HTML, CSV, Mermaid, graph and search files | Never authoritative; regenerated from canonical data |

## Read first

AI/operator entry point:

1. `A7_BOOTSTRAP.json`
2. `A7_READ_FIRST.md`
3. Applicable policy profiles
4. Canonical entity/edge/source records
5. Live provider reads required by the authority map

## Repository layout

- `registry/` — canonical machine-readable records
- `schemas/` — structural contracts
- `relational/` — PostgreSQL-compatible relational contract; no database runtime required
- `policies/` — global/provider/module/project/task operating rules
- `generated/` — derived outputs; never hand-edit facts here
- `scripts/` — validation/build tooling
- `.github/workflows/` — CI and later projection/deployment pipelines

## Public-repository warning

This repository is intentionally public for now. Do not commit secrets, private message bodies, confidential file contents, private personal information, credentials, tokens or restricted financial/engineering material. A7 can index a private provider object without copying its private contents into this repository.

## Git-native A7 closeout

A7 uses commit/branch/CI/provider-readback lineage instead of duplicating every routine registry mutation into Drive control sheets. Provider-specific PRE/POST evidence is still required when A7 actually mutates that external provider.

See `A7_READ_FIRST.md` and `policies/global/`.
