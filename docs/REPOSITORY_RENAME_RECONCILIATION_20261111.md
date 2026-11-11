# Canonical GitHub slugs after provider rename — 11 November 2026

## Stable identity resolution
The GitHub provider confirmed that the *former* and *current* URLs resolve to the same respective repository IDs:

| Semantic entity | Permanent provider repository ID | Current canonical GitHub path | Previous path |
| --- | --- | --- | --- |
| A7 registry | `1406572237` | `FabinGurung/jp-a7-system-registry` | `FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph` |
| Site Operations (`REPO-000007`, `MOD-OPS-001`) | `1312147922` | `FabinGurung/jp-site-operations` | `FabinGurung/JP_Communication-Command-Centre-and-Resource-Hub` |

The old paths are historical GitHub aliases/redirects only, **not** additional modules or sources. No project ID, Drive file ID, project register identity, role, payroll authority or signed engineering source was changed.

## Current browser entry points
- A7: https://github.com/FabinGurung/jp-a7-system-registry and https://fabingurung.github.io/jp-a7-system-registry/
- Operations: https://github.com/FabinGurung/jp-site-operations and https://fabingurung.github.io/jp-site-operations/
- Operations public projection publisher: https://github.com/FabinGurung/jp-site-operations/actions/workflows/operations-sheets-pages.yml
- Resource Library: https://fabingurung.github.io/jp-field-desk-library/

## Changed authoritative routing records
- `A7_BOOTSTRAP.json.canonical_repository.full_name`
- `A9_GIT_DRIVE_BOOTSTRAP.json.repository_full_name` and `links.a7_site`
- `registry/entities/repositories.json` for `REPO-000001` and `REPO-000007`
- `registry/entities/modules.json` for `MOD-OPS-001`
- `AGENTS.md` read-first link

Operations' own module manifest and branch/lane registry are reconciled in the separate governed Operations PR. The two PRs must not silently write into each other's authority.

## Historical inventory warning
Existing old-URL observations in append-only GitHub, deployment, module-manifest and release receipts represent facts **as observed then**. They must not be rewritten to pretend the rename happened at that time. New current-priority entrypoints use the renamed slugs. Regenerate or reconcile historical projections in a later A7-owned validation cycle if required.

## Review boundary
This record is public-safe identity routing only. No Google Drive source, permissions, version history, worker wages or project field progress was modified. Historical A9 Drive parity remains unverified under existing A7 bootstrap rules.
