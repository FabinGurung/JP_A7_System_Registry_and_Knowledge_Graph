# A7 History, Navigation and Rollback — Read First

Sequence A7-SEQ-000019. This release **changes navigation presentation and moves one learning reminder**, not canonical data. The Galaxy is the only normal homepage. All current pages share a Cloud Orbit brand header/footer and active-page indication. A small More menu holds Governance and History rather than adding unrelated top-level tabs.

## Removed from everyday navigation, but preserved in Git and Pages
- Original Dashboard / Classic Graph at `legacy-overview.html`. **Not a strict duplicate**: original graph 2D/light 3D, project/module matrix, search and fact-class inspector remain unique specialist QA tools. Keep the actual page source and JS engine; access via History only, no current top-level link.
- Pre-Galactic Milestone `milestone.html` and release `a7/pre-galactic-atlas-v0.1.0` at `49c99f7010e53a66fab94cad4a955e195f9b060d`. Leave immutable history; never repoint historical refs.
- Standalone visualization technical `visualization-workspace.html`. Six roles now rendered as short glance posters inside Memory Wall from the already canonical `registry/decisions/visualization-workspace.json` → `data/visualization-workspace.json`. The original implementation states remain unchanged; it is a reference, not a new tool install.

## Frontend architecture
`site/assets/a7-site-shell.js` + `a7-site-shell.css` are loaded by all public A7 HTML pages, and inject one shared header/context/footer after DOM ready. This avoids replacing app-specific markup or JS selectors. Original header fallback remains if JS fails. Existing old archive app controls, including its search trigger, remain usable.

The Fluffy Rocket and `a7-unified-theme.css` remain unchanged. All nine registered repositories, private Google Drive/A9 Main/Local, application engines and site data are untouched.

## Rollback
Take PRE branch `snapshot/pre-a7-seq-000019-navigation-consolidation`. Restore only through governed new branch/PR, CI, main Pages provider readback and POST snapshot. Keep `a7/pre-galactic-atlas-v0.1.0` and original pages preserved. No deletion or permanent 404s; archive denotes removal from everyday primary navigation.

Check the full A7 CI plus new `scripts/validate_site_navigation.py`, then browser-test desktop/mobile responsive menus, active state, fallback when JS unavailable, legacy search, Memory Wall six cards/statuses, history links, galaxy selection, and rocket reduced-motion behavior. Browser QA must never be claimed unless performed.
