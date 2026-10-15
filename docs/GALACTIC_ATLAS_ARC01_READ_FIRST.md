# Galactic Atlas / Arc 01 — Read first

**Product boundary:** A7 is a **federated metadata catalogue, registry, search/discovery portal and cross-module routing index**. It does not own or execute specialist CAD/AAD, Structural, Cost, Scheduling, Operations, R&D, Study or adjacent business templates/engines.

## Pre-arc release preservation

- Frozen exact pre-mutation `main` SHA: `49c99f7010e53a66fab94cad4a955e195f9b060d`.
- Provider-verified *branch* ref: `refs/heads/milestone/pre-galactic-atlas-v0.1-20261015`. The ref was created before code changes; the same pre-arc SHA was subsequently provider-verified as the annotated [Git tag + published Release `a7/pre-galactic-atlas-v0.1.0`](https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph/releases/tag/a7/pre-galactic-atlas-v0.1.0) through GitHub Actions. Do not move the frozen ref or retag it.
- Release record issue: https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph/issues/31
- Previous homepage: `site/legacy-overview.html` is an exact copy of the old `site/index.html`, including the original app loader. Its original graph, matrix, search and authority modes remain browsable.
- Older standalone pages `control-towers.html`, `governance.html`, `roadmap.html`, `how-it-works.html`, `visualization-workspace.html` remain preserved at their previous routes.

## Arc 01 rollout — only the central navigation

1. Homepage shows a spatial Galactic Atlas with A7 at the centre and eight peer repositories around it; select **one** node to open a compact inspector.
2. Click **Visit system website** to leave A7 for the product's own Pages website, or **Repository / version history** to open its owning Git source. No iframes are assumed (embedding may be blocked by the site and bypasses ordinary navigation); the inspector offers clear source/provider links.
3. Deep links to specialist products may be shown only as read-only pointers from the catalogue, not embedded copies of template instructions.
4. Under collapsed “Governance protocol” the seven ownership classes map A7 catalogue vs owning repository for identities, discovery, relationships, history, templates, execution and authority. Governing rule **one writer / typed references / no duplicated authority**.
5. Under collapsed “Engineering archives” old A7 graph, providers, project routing, Control Towers and roadmap are accessible without forcing them on first-time users.
6. No backend, database migration, private A9 mutation, source ingestion or new specialist repo write is part of this arc.

## Source and publication lineage

Source of repo name, persistent repository identity and website URL is `registry/entities/repositories.json` (date-stamped *observations*, not automatically live status). Presentation-only station names/coordinates/descriptions are `registry/decisions/galactic-atlas-ui.v0.1.json`. `scripts/generate_galactic_atlas.py` deterministically derives `site/data/galactic-atlas.json` on the GitHub Pages build, with source SHA256 hashes and build commit.

The client `site/assets/galactic-atlas.js` reads this public projection, refuses unexpected schema or untrusted hosts, and does not make writes. Existing `scripts/generate_visualizations.py` and all prior `site/data/**` projection generation remain unchanged. `scripts/validate_galactic_atlas.py` tests source IDs, URLs, ownership, privacy, the frozen baseline copy, map-first progressive UX and absence of old-page deletion.

## Website links and status caution

All eight peer website URLs come from the A7 repo catalogue. They have last-observed timestamps, and the live website status is **not asserted fresh from A7**. GitHub provider/Actions or original domain owner is authoritative for current publication health; a website is not guaranteed to permit embedding. If a website is offline, GitHub repository link remains available for the selected system.

## Intended later arcs (not shipped)

- Arc 02: read-only cross-module relationship explorer / filters and node link hover explanations.
- Arc 03: bounded history, source-run status and current provider evidence drilldown.
- Arc 04: a queryable federation with APIs/permissions across projects and modules.

Nothing in future arcs may merge the specialist data writers into A7.
