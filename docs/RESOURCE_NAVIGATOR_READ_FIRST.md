# A7 Resource Navigator — Arc 07 (A7-SEQ-000034)

Read [A7_READ_FIRST.md](../A7_READ_FIRST.md) and [docs/MEMORY_WALL_READ_FIRST.md](MEMORY_WALL_READ_FIRST.md) before changes.

## Intent and exact scope

A new standalone **L1 Resource Navigator** permits human navigation from Organization → Project → Category → Document/Answer/Resource. This first implementation is a **public-safe A7-only directory** with one A7 presentation grouping and one public A7 project. Presentation grouping IDs must not be mistaken for company registration or global project PKs.

This is **not** a Drive migration, folder crawler, company register, private file catalogue, answer-generation API, client data upload, domain database or automated cross-provider importer. Only known public A7 website paths and current repository source paths may be admitted.

## Canonical and derived files

- Canonical manifest: `registry/curations/resource-navigator.v0.1.json`
- Build: `scripts/generate_resource_navigator.py`
- Hard gate: `scripts/validate_resource_navigator.py`
- Derived generated Pages JSON: `site/data/resource-navigator.json`
- Human view: `site/resource-navigator.html`
- Scoped UI assets: `site/assets/resource-navigator.js`, `.css`
- Shared navigation: additive entry within existing More menu; do not replace original routes or page assets.

Git SHA and source digest on Pages are dated build evidence, **not live monitoring**. GitHub is authoritative for source and CI. Owning providers retain original domain authority. A7 curates links, not physical documents or approvals.

## Admitting future records

Resolve fact class and module ownership, verify access/publication and original provider, use stable separate navigator IDs, and never publish private Drive IDs, ACLs, file names or restricted metadata. Verify each target path, preserve user permissions, run validator, Registry CI and desktop/mobile Chromium; read back deployed Pages when possible. No bulk import, private runtime or peer write without new authorization.

## Regression guard

Preserve all prior L0 Arc 01–06 panels, L1 navigation, Memory Wall Collections 01–04, original source curation files and legacy routes. Homepage source byte-for-byte unchanged in Arc 07. Independent served HTML readback remains separate from GitHub Pages workflow success.
