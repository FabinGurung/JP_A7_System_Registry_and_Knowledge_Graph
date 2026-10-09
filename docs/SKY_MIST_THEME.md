# A7 Sky Mist — visual theme decision

Theme ID: `A7-UI-THEME-SKY-MIST-001` | Independent bounded UI update: `A7-SEQ-000014`.

## Goal

Replace the hard-dark A7 Pages look with a light, soothing **sky-blue / mist white** interface across the knowledge graph, pinned visualization workspace, Git + Drive governance page, and development roadmap.

Core design tokens are in `registry/decisions/ui-theme.json` and implemented by `site/assets/sky-theme.css`:

| Token | Value | Use |
|---|---|---|
| Background | `#eff8fc` | Sky mist |
| Surface | `#ffffff` | Clean, calm panels |
| Ink | `#243e52` | Legible dark-blue text |
| Muted | `#59768b` | Secondary text |
| Accent | `#267eac` | Links, selected states |
| Border | `#d1e4ee` | Gentle edges |

## Implementation

- All four public HTML pages include `assets/sky-theme.css` **after** their prior CSS, keeping rollback trivial and avoiding wholesale rewrite of existing page markup.
- Governance and roadmap originally use inline dark CSS. A scoped `standalone-page` override updates those pages without importing the dashboard component layout.
- The graph renderer uses a readable client-side palette for 2D/3D nodes, labels, edges and legend. Generated graph JSON, stable identities, coordinates and project/authority facts **do not change**.
- Retain the six pinned visualization roles/implementation statuses. They are unrelated to aesthetic theme.
- Focus visibility, narrower mobile headers and reduced-motion orbit styling are included.

## Reproducibility and boundaries

`scripts/validate_site_theme.py` and the standard A7 CI guard the four links, load order, tokens, Canvas palette and source documentation.

This is an independent UI task. **A7-SEQ-000013 is still staged**, and this update does not reconcile or close private A9 Main/Local Library work. The GitHub repository is source authority for site code; GitHub Actions/Pages is deployment authority. The theme decision does not change domain/source authority.

After publish verify exact merged `main` SHA in A7 validation and GitHub Pages build/deploy; preserve pre/post snapshots. A visual browser inspection is separate from automated tests.
