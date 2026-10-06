# A7 Phase 6 — Specialist Module Binding and Ownership Boundaries

## Correct topology

Structural and CAD are not children of the Operations Hub. The execution-tier modules are peers registered by A7:

```text
A7 semantic control plane
├── MOD-OPS-001     Operations / Communication
├── MOD-SCHED-001   Scheduling
├── MOD-COST-001    Cost Estimation
├── MOD-STRUCT-001  Structural Analysis
├── MOD-CAD-001     CAD / Drawings
├── MOD-RND-001     Research & Development
└── MOD-STUDY-001   Study Hub
```

For the execution tier, Operations, Scheduling, Cost, Structural and CAD are siblings. The Operations Hub can provide human-facing cards/deep links and surface status, but its relationship is `LINKS_TO_PEER_MODULE`, never ownership or containment.

## A7 boundary

A7 owns the semantic map: identity, alias, edges, authority assignments, provider references, policies and cross-system lineage. It can orchestrate/fetch/validate, but domain mutation belongs in the owning repository.

## Operations identity nuance

A7 owns global semantic identity and aliases. MOD-OPS-001 owns the operational project-master record used by the Operations Hub (project code/lifecycle/coordinates/public attributes), Daily Ops current state/event history and project-resource relationship records. These are separate fact classes, preventing a duplicate writable authority.

## Repository-local manifests

Phase 6 binds the existing repositories but does not rewrite them into a common format. The Operations Hub already has `workspace/modules.json`; other modules currently expose ownership through their live README/product contracts. A future cross-repository manifest phase can standardize a tiny local `a7-module.json` contract without moving domain truth into A7.
