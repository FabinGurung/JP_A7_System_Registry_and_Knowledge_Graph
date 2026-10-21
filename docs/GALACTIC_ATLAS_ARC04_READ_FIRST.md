# Galactic Atlas Arc 04 — Evidence-Gated Routes / READ FIRST

**Sequence:** A7-SEQ-000022 (public projection only). Original base `ec318c5b43362347a121585b03a59b0c09ee39df`.

## Verified source boundary
- Admission: `registry/edges/edges.jsonl` canonical EDGE-000053..EDGE-000056, `LINKS_TO_PEER_MODULE`, and `registry/entities/modules.json` module-to-REPO bindings. Four links express **Operations Hub peer navigation** to Scheduling, Cost, Structural and CAD. They do NOT prove a dataset handoff, automated update, integration or authority transfer.
- Each displayed documented link points to its exact edge line at pinned source SHA `ec318c5b43362347a121585b03a59b0c09ee39df`.
- The four separate CAD→Structural, CAD→Scheduling, CAD→Cost and R&D→Study Hub candidate ideas are versioned in `registry/decisions/galactic-atlas-arc04-routes.v0.1.json`. They have **no runtime evidence, no admission into canonical graph edges**, are off by default and must not be described as real interfaces.
- Eight existing A7 catalogue spokes remain `CATALOGUE_ROUTES_TO` navigation only.
- `registry/dependencies/status.json` still has zero provider-verified cross-repository runtime dependencies.

## UI and implementation
The working surface is `site/index.html#interstellar-routes`: select a station and view its eligible directed routes (or all when A7 hub selected). Filter documented navigation vs proposal display; click a route list entry for exact source evidence. Curved colored dashed lines do not animate active data flow. Proposal checkbox is disabled by default; sector search/hidden station interactions hide edges with invisible endpoints. Dedicated `site/assets/galactic-atlas-arc04.js` and CSS do not change ownership logic. `site/assets/galactic-atlas.js` has a narrowly scoped reviewed selection event and stable node ID; refresh only its pin in the theme source-integrity decision.

Generator: `scripts/generate_galactic_atlas.py`. Validator: `scripts/validate_galactic_atlas_arc04.py`. Workflows validate Arc01/02/03/04 and domain-source boundaries.

## Release gating
PRE snapshot -> feature branch CI -> PR CI -> merge -> merged-main CI and Pages readback -> closeout branch/PR and POST snapshot matching final main. Manual browser/mobile visual and interactive QA must be separately marked not performed where no browser is available. Private A9 seq13, R&D owner QA and specialist engineering deliverables are not claimed complete.

## Next
Arc 05 immutable releases, QA and rollback constellation, after this source and deployment gate passes.

## Provider acceptance (2026-10-21)

Feature CI [39587206657](https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph/actions/runs/39587206657) SUCCESS; PR [#48](https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph/pull/48) CI [39587214395](https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph/actions/runs/39587214395) SUCCESS; merged-main CI [39587284143](https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph/actions/runs/39587284143) SUCCESS; merged-main Pages [39587284188](https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph/actions/runs/39587284188) SUCCESS at `fcf880a84e08f1631e3077fb69f38c5cfaffa529`. Pages artifact 12340006573 SHA-256 88182405e74f1ead7fd7330a798bbe11bfadd871923aab3e763d1fefc5832633.

Final release metadata + POST snapshot closeout is tracked independently. No screen-level mobile/browser inspection has been performed.
