# A7 System Registry — development history and roadmap

**Snapshot:** 2026-10-09 NPT · **A7 latest fully closed sequence:** `A7-SEQ-000014` · **A7-SEQ-000013:** staged public-safe transition, **NOT FINAL_CLOSED_PASS**.

A7 governs semantic identities, authority, routing and public-safe cross-provider relationships. It does not own a peer module's scientific results, code or private document bytes. This file is [the machine roadmap](../registry/roadmap.json) projected for humans.

## Delivered milestones
- **A7-D01 · Phases 1–2 · DELIVERED — Semantic identity, authority and conflict engine.** Entities, repository IDs, governed aliases, typed relationships, fact classes, authority precedence, human QA and public safety.
- **A7-D02 · Phases 3–4 · DELIVERED — GitHub inventory and redacted Drive topology.** Nine connected repositories, branch and workflow/Pages evidence, A9 Drive anchors/coverage without dumping confidential Main Library metadata.
- **A7-D03 · Phases 6–7 · DELIVERED — Module ownership and deterministic cross-repository routing.** Peer specialist modules, A7_MODULE.json contract and project → fact class → owner → provider route.
- **A7-D04 · Sequences 8–10 · DELIVERED — Pages/workflow refresh and module/project reconciliation.** Provider-backed repository/Pages and R&D manifest reconciliation, project-to-module routing and tests.
- **A7-D05 · Sequence 11 · DELIVERED — Public visualization and derivation platform.** Canvas 2D/3D, semantic search, route/authority matrices, generated Mermaid and Excalidraw data, content digests and public Pages. Does not imply React Flow/Cytoscape runtime implementation.
- **A7-D06 · Sequence 12 · FINAL_CLOSED_PASS — Pinned six-role visualization strategy.** Cytoscape semantic exploration; React Flow deterministic architecture; Tables QA; Mermaid docs as code; Excalidraw annotation; optional 3D. Implementation status is explicitly distinguished.
- **A7-D07 · Sequence 13 — staged · PUBLIC_SAFE_RULE_ACTIVE__SEQ13_NOT_FINAL_CLOSED — Git/Drive cross-provider operating contract.** A9_GIT_DRIVE_BOOTSTRAP.json, human rule, governance page, AGENTS.md pointers across all nine repos, minimal-context provider routing.
- **A7-D08 · Sequence 13 — staged · DRY_RUN_PASS__NOT_IMPORTED — GitHub → Main Library dry-run bridge.** Nine GitHub repository heads → schema-aligned nine ArtifactRegistry and eight ArtifactEdges candidates, SHA-256 digest manifest; no private Google Sheet writes. Actions 37870717830 success.

- **A7-D09 · Sequence 14 · FINAL_CLOSED_PASS — Sky Mist light theme.** Calm sky-blue interface across four A7 Pages views, updated 2D/3D Canvas colors and CI regression guard. Independent of the still-staged Sequence 13; no private A9 migration or Main Library import.

## Pending roadmap, by priority
- **A7-N01 · P0 · IN_PROGRESS — Seal bounded public-safe A7 seq13 change accurately.** Confirm current HEAD, CI, Pages and bridge source/manifest. Finalize only public-safe stage, never conflate it with private A9 cutover.
- **A7-N02 · P1 · BLOCKED_ON_PRIVATE_PARITY — Reconcile private A9 Main/Local semantics before bridge import.** Provider-first live index, ID collision reconciliation, historical run/edge/source parity, Main consumed cursors and Local ACK; gated private A9 write only.
- **A7-N03 · P1 · PLANNED — Define release/artifact lineage contract.** Owning module Git repo/ref/commit/path → build/QA → Drive file/provider revision → A7 public-safe edges; do not duplicate every commit into Main Library.
- **A7-N04 · P1 · PARTIAL — Cross-repository bootstrap/version visibility and CI.** Each peer module can resolve pinned A7 policy release, owner control and drift check with provider readback; AGENTS files are not an account-wide auto-policy.
- **A7-N05 · P2 · STAGED — Roadmap and authority dashboard with real observations.** Show current policy migration stages, provider-confirmed releases, audit gaps and human-QA queue. No stale SHA claimed current.
- **A7-N06 · P2 · PLANNED — Implement visualization roles only with verified code.** Cytoscape/React Flow if needed, keep source-of-truth JSON, Tables audit, Mermaid/Excalidraw export and accessible interactive pages tested.
- **A7-N07 · P2 · DEFERRED — Optional confidential governance runtime.** Only provision private repository or DB when authorized collaboration/concurrency needs justify it; do not mirror private Drive corpus in public A7.

## Hard boundaries
- Old Drive A9 governance is not replaced; controlled source-by-source parity and explicit cutover are required.
- A7 is a public-safe semantic registry and router, not owner of peer research science, construction finance or raw source binaries.
- A9 Main Library is private and has not imported the candidate Git records; its exact PK/FK/event/ACK ledger remains in Drive.
- Git branches refer to whole repository commits, not one isolated researcher dataset.
- R&D 18/18 Drive audit and 11 researchers are owned by R&D; A7 legacy research coverage was narrower and is not blindly rewritten.
- MSCH_HYDROPOWER_CORPUS_B013 remains HOLD/DO NOT RESUME.
- No latest deployed SHA should be stored as a permanent truth; fetch GitHub live before status claims.

## Cross-thread handover and linked R&D roadmap

The R&D thread's scoped source-first [handover](https://github.com/FabinGurung/JP_Research-and-Development/blob/main/docs/HANDOVER_TO_A7_20261009.md) gives 18/18 source-intake audits, 11 researchers, Fabin research websites, 33 research-lane refs and six restored demos. A7 should read its owner module `A7_MODULE.json` and R&D `CURRENT.json` live rather than importing that state into A7's canonical global policy.

- [Live A7 roadmap](https://fabingurung.github.io/JP_A7_System_Registry_and_Knowledge_Graph/roadmap.html)
- [Live R&D roadmap](https://fabingurung.github.io/JP_Research-and-Development/roadmap/)
- [A7 central Git–Drive bootstrap](../A9_GIT_DRIVE_BOOTSTRAP.json)
- [A7 Main Library bridge rule](MAIN_LIBRARY_GITHUB_BRIDGE.md)
- [A7 source repository](https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph)

## Current provider evidence, never evergreen truth

The pre-roadmap A7 site, validation and Main Library dry run passed on SHA `3d82f138cde757e436a2f88f947228cbb40bda12`; Actions Pages `37870717817`, validation `37870717858`, bridge `37870717830`. Confirm latest branch HEAD and current Actions before declaring an updated roadmap deployed.

The native private Main Library has not been written, while the Git-head candidate files are safely reproducible. No account-wide ChatGPT system settings were changed by AGENTS.md.

### Bounded independent A7-SEQ-000015: control tower navigator (site architecture)

Public-safe authority classification and interactive site navigation are staged independently of the still-open A7-SEQ-000013 Git/Drive migration. The readable entrypoint is [Control Tower Atlas](https://fabingurung.github.io/JP_A7_System_Registry_and_Knowledge_Graph/control-towers.html). Its machine source is `registry/controls/control-tower-map.json`. R&D repo retains owning workflows. Private Drive A9 thesis v1.23 / presentation v2.2 / AI Tool v0.42 were provider-inspected but must not be copied into public Git. Next work: full exact-rule crosswalk, format generator/template QA, A9 private Main/Local reconciliation, drift CI, and module-local dashboards.
