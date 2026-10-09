# JP_A7_System_Registry_and_Knowledge_Graph

Canonical **A7 semantic registry, knowledge graph, authority map and AI control plane** for the JP engineering ecosystem.

## Current state

- System namespace: **A7**
- Repository provider ID: `1406572237`
- Default branch: `main`
- Visibility: public
- Current sequence: `A7-SEQ-000014` — **FINAL_CLOSED_PASS**
- Phase 1 semantic-registry foundation: **COMPLETE**
- Phase 2 authority + conflict-resolution engine: **COMPLETE**
- Phase 3 GitHub repository / Pages / workflow inventory: **COMPLETE**
- Phase 4 Google Drive / Kaksaveksaka A9 topology metadata inventory: **COMPLETE**
- Phase 6 specialist module binding + ownership boundaries: **COMPLETE**
- Phase 7 cross-repository module manifest contract: **COMPLETE**
- Seq8 GitHub Pages/workflow refresh: **COMPLETE**
- Seq9 R&D module-manifest reconciliation: **COMPLETE**
- Seq10 deterministic Project-to-Module routing: **COMPLETE**\n- Seq11 visualization / derivation layer + A7 Pages UI: **COMPLETE**
- Seq12 pinned visualization strategy: **COMPLETE**
- Seq13 Git/Drive public-safe migration: **STAGED, NOT PRIVATE-A9 CLOSED**
- Seq14 Sky Mist light UI theme: **COMPLETE**
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

The historical A7 research foundation registered five identities; the owning R&D researcher registry now lists 11 separate researchers and must be fetched live. A7 has not blindly imported that newer domain registry. Read `registry/dependencies/research-governance.json` for the A9 provisioning boundary. The existing R&D repository holds the public A9 foundation. A dedicated private A9 repository is optional and is not provisioned; no scientific histories or Saugat thesis records were imported.


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


## Deterministic project-module routing

A7 registers only stable project semantic IDs and their routing profile. Operational project-master fields remain in the Operations module.

The default AEC execution profile routes governed fact classes to the five peer execution modules: Operations, Scheduling, Cost, Structural and CAD. A route means that the selected module owns the requested fact class for the project context; it does not claim that a project-specific schedule, BOQ, structural model or CAD package already exists.

AI resolution is: project ID -> execution profile -> fact-class route -> authority-owner module -> current A7_MODULE.json -> live owning provider/ref/path.


## Visualization and derivation layer

A7 generates a public-safe, non-authoritative visualization layer from canonical JSON/JSONL and the exact deployed Git commit.

The derivation engine produces:

- shared 2D/3D graph data;
- static search index;
- Project-to-Module routing matrix;
- authority matrix;
- Mermaid architecture source;
- Excalidraw projection data;
- SHA-256 source/output derivation manifest.

The interactive site is published at:

https://fabingurung.github.io/JP_A7_System_Registry_and_Knowledge_Graph/

The site is a projection surface only. It cannot mutate domain facts and does not become authority. Internal/private Google Drive topology nodes and labels are excluded from the public graph; only an aggregate registered-node count is exposed.

## Pinned visualization strategy (A7-SEQ-000012)

The publicly pinned workspace is [A7 visualization strategy](https://fabingurung.github.io/JP_A7_System_Registry_and_Knowledge_Graph/visualization-workspace.html).

The governing design decision is `registry/decisions/visualization-workspace.json`; the human handover is `docs/VISUALIZATION_WORKSPACE_READ_FIRST.md`. The six preserved roles are Cytoscape/semantic, React Flow/architecture and routing, tables/audit and QA, Mermaid/docs-as-code, Excalidraw/human annotation, and optional 3D/spatial. Their **implementation statuses are recorded as observations, not promises**. The first two are preferred/NOT INSTALLED; current Canvas/HTML renderers remain. Mermaid/Excalidraw currently generate source/export data only; 3D uses a lightweight Canvas projection. Do not infer completed upgrades without provider readback.

Pages receives `visualization-workspace.json` derived from the canonical decision and included in source/output SHA-256 lineage. CI verifies the pinned navigation, six roles, explicit states and source provenance.

## A9 cross-provider Main Library bridge (staging)

See [schema-aligned GitHub observation bridge](docs/MAIN_LIBRARY_GITHUB_BRIDGE.md). A7 records nine public GitHub repository HEAD observations and builds deterministic, checksummed ArtifactRegistry/ArtifactEdges **candidate** CSVs. This is not a Google Drive Main Library write or ACK.

## Public roadmap and R&D handover (2026-10-09)

- **Live A7 roadmap:** https://fabingurung.github.io/JP_A7_System_Registry_and_Knowledge_Graph/roadmap.html
- **Machine/human canonical sources:** [registry/roadmap.json](registry/roadmap.json) · [docs/ROADMAP.md](docs/ROADMAP.md)
- **Linked R&D roadmap:** https://fabingurung.github.io/JP_Research-and-Development/roadmap/
- **R&D cross-chat handover:** [R&D 2026-10-09 handover](https://github.com/FabinGurung/JP_Research-and-Development/blob/main/docs/HANDOVER_TO_A7_20261009.md)

A7 sequence 12 remains the last documented FINAL_CLOSED_PASS. The public-safe Git–Drive sequence 13 is *staged* and must not be confused with private A9 cutover. The offline Main Library bridge passed but no private library import or ACK was claimed.

## Sky Mist site theme — independent A7-SEQ-000014 UI refresh

A7's four public Pages surfaces (knowledge graph, visualization workspace, governance, roadmap) use the soft sky-blue light palette in `site/assets/sky-theme.css`. The design tokens and guard are `registry/decisions/ui-theme.json`, `docs/SKY_MIST_THEME.md`, and `scripts/validate_site_theme.py`. No semantic data, technical graph schema, or project ownership is changed. This UI scope does **not** close the staged A7-SEQ-000013 Git/Drive / private A9 transition.
