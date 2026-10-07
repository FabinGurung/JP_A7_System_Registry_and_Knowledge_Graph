# JP_A7_System_Registry_and_Knowledge_Graph

Canonical **A7 semantic registry, knowledge graph, authority map and AI control plane** for the JP engineering ecosystem.

## Current state

- System namespace: **A7**
- Repository provider ID: `1406572237`
- Default branch: `main`
- Visibility: public
- Current sequence: `A7-SEQ-000009` — **IN_PROGRESS**
- Phase 1 semantic-registry foundation: **COMPLETE**
- Phase 2 authority + conflict-resolution engine: **COMPLETE**
- Phase 3 GitHub repository / Pages / workflow inventory: **COMPLETE**
- Phase 4 Google Drive / Kaksaveksaka A9 topology metadata inventory: **COMPLETE**
- Phase 6 specialist module binding + ownership boundaries: **COMPLETE**
- Phase 7 cross-repository module manifest contract: **COMPLETE**
- Seq8 GitHub Pages/workflow refresh: **COMPLETE**\n- Seq9 R&D module-manifest reconciliation: **IN_PROGRESS**
- Connected FabinGurung repositories inventoried: **9**
- Live PostgreSQL/Neon runtime: **DEFERRED / NOT REQUIRED FOR CURRENT OPERATING MODEL**
- Canonical editable data: **JSON + JSONL**
- Formal contracts: **JSON Schema + PostgreSQL-compatible SQL DDL**
- Human/visual outputs: **generated projections only**

## Core rule

> The AI is the resolver/operator, not the authority.

A7 defines identity, aliases, source references, authority boundaries, typed relationships, policies and mutation lineage. Provider-native GitHub state remains owned by GitHub; A7 stores verified observations and semantic relationships.

## GitHub inventory

Phase 3 adds:

- immutable GitHub repository IDs and current slugs;
- complete observed branch/current-head inventory;
- Pages production-owner/source evidence;
- current custom workflow definitions and Pages guards;
- specialist/system role candidates without prematurely creating module bindings;
- explicit findings where Pages source and default branch differ;
- endpoint limitations and fail-forward provenance.

The direct GitHub Pages settings and Actions workflow-list REST endpoints are not exposed by the connected connector. A7 therefore uses equivalent provider evidence: repository `has_pages/homepage`, branch files, workflow contents and successful Actions runs. This is recorded rather than hidden.

## Conflict rule

**Authority before recency.** “Newest wins” is prohibited unless the applicable fact class explicitly permits timestamp/version arbitration.

## Public-repository warning

Do not commit secrets, private message bodies, confidential file contents, private personal information, credentials, tokens or restricted engineering/financial material.

## Git-native A7 closeout

A7 uses commit/branch/CI/provider-readback lineage. Provider-specific PRE/POST evidence remains required when A7 actually mutates an external provider.


## Google Drive topology model

A7 does **not** mirror the private 968-row A9 Drive index into this public repository.

Phase 4 instead records:

- the current A9 root and safe top-level semantic branches;
- stable governance anchors needed for deterministic AI routing;
- a redacted boundary for the private/sensitive subtree;
- index coverage/freshness and direct-provider observations;
- a resolver contract that queries `Fabin_Gurung_Drive_Index` and then reads the exact Drive object live when current state matters.

This preserves Drive as authority for private topology while making A7 the machine-readable routing/control plane.

## Research governance foundation

Five public research identities and R&D routes are registered. Read `registry/dependencies/research-governance.json` for the A9 provisioning boundary. The existing R&D repository holds the public A9 foundation. A dedicated private A9 repository is optional and is not provisioned; no scientific histories or Saugat thesis records were imported.


## Phase 6 specialist module binding

A7 now binds the existing repositories as **peer modules**, not a nested monolith.

```text
A7 semantic control plane
├── Operations / Communication
├── Scheduling
├── Cost
├── Structural
├── CAD
├── Research & Development
└── Study Hub
```

For the project-execution tier, Operations, Scheduling, Cost, Structural and CAD are siblings. The Operations Hub may display links/status from the other modules, but it never owns their engineering domain truth.


## Phase 7 cross-repository module doorway

Every bound module repository now exposes a root `A7_MODULE.json`. It is a small routing contract: stable IDs, A7 ownership pointer, explicit refs and task entrypoints. It does **not** duplicate domain facts.

This lets an AI enter a specialist repository deterministically without first reading a long README or guessing which branch/file is current.
