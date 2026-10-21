# A7 Galactic Atlas Arc 03 — Sectors / Read First

**Sequence:** A7-SEQ-000021. This is a public-safe presentation-only improvement to the existing A7 Galactic Atlas.

## What this Arc ships

A dated, source-derived **sector directory** with filters, search, colored sector identities, result counts, keyboard-compatible selection, reset behavior, and a central A7 control hub that remains visible. The five sectors are A7 Command (1), Engineering (4), Operations (1), Knowledge (2), Adjacent Products (1). These are display groupings, NOT changes to older Arc01 `zone` classes, domain ownership or operational dependency registries.

The source authority is `registry/decisions/galactic-atlas-sectors.v0.1.json`, mapping exact stable `REPO-00000x` IDs to sector groups. `scripts/generate_galactic_atlas.py` joins this to `registry/entities/repositories.json`, existing page layout, and the fixed October 20 Arc02 provider snapshot. The generated `site/data/galactic-atlas.json` retains the Arc02 provider evidence and `GALACTIC_ATLAS_ARC_02_INSPECTOR` compatibility label while adding an explicit `navigation_arc: GALACTIC_ATLAS_ARC_03_SECTORS`, source hash and category fields.

UI: `site/index.html`, `site/assets/galactic-atlas.js`, `site/assets/galactic-atlas-arc03.css`.
CI: `scripts/validate_galactic_atlas_arc03.py`, all previous A7 registry validators and Pages provider readback.

## Critical boundaries

- A7 is always the hub. All 8 edges are still navigation links only, not provider-confirmed runtime integrations.
- The published branches, commits and workflow outcomes from Arc02 remain a **dated snapshot**, not automatic live monitoring.
- No private A9 data imported; `A7-SEQ-000013` remains STAGED without Main/Local ACK.
- R&D scientific/manuscript QA and other owner-local gates remain separate.
- Preserve site-wide white Cloud Orbit theme, fluffy self-hosted rocket, Memory Wall, History and current source owners.
- A7 app JavaScript changed intentionally for Arc03; update its existing Git blob integrity pin to the new reviewed hash and preserve the other five exact hashes.
- No other JP/peer repository writes. No archive deletion.

## Acceptance and future

Provider gate: PRE snapshot -> feature branch + registry CI -> PR validation -> main merge + Pages success -> terminal closeout + POST snapshot identical to main.
Test filter buttons, search query input, Escape, reset, empty matches, keyboard arrows, responsive layout, reduced motion. CI proves source constraints but is not a manual visual browser walkthrough.

**Next:** Arc04 typed cross-system relationships only after authoritative evidence; Arc05 milestone/release constellations. Developer Dock remains separately planned.
