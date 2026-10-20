# A7 Cloud Orbit — Read first

The user explicitly selected a **calm white / sky-blue** normalized theme over the Galactic Atlas dark theme. Every A7 public subpage, panel and embedded section should inherit the same presentation tokens. The provided Operations website map was cited as an example of nested web content; **do not copy its theme and do not modify that repository.**

Theme: `registry/decisions/cloud-orbit-theme.v0.1.json`.
CSS: `site/assets/a7-unified-theme.css` (loaded **last** on ten pages).
Mascot: `site/assets/fluffy-rocket.svg` and `site/assets/fluffy-rocket.js` (decorative, occasional, independently roaming; variable waypoints, not a straight line).

Existing page CSS, markup, Galaxy and Canvas executors, data projections, exact Git/Drive authority, R&D/CAD/OPS releases, and A9 private Main/Local libraries must **not** change because of a theme release. All ten HTML source edits are *only additions of a CSS link and a defer script tag*. Main source scripts have frozen Git blob checksums in the theme decision; CI validates they remain unchanged for this bounded release.

Use `scripts/validate_unified_theme.py` and the full A7 registry suite, and verify GitHub Pages provider success for the exact main commit. On real browser inspections check dark leakage in panels, navigation focus, responsive mobile, PDF poster print, galaxy graph visibility, scroll performance, the occasional rocket's unpredictable curved flights, `prefers-reduced-motion` and hidden tabs.

Mascot is an SVG illustration with transparent background, soft shape, fins and happy face. It never blocks the pointer, never changes UI text, buttons, source records or network. It is omitted in reduced-motion conditions and print. Its source is self-contained and does not require an external service.

Retain original pre-Galactic release and the SEQ-000018 PRE and POST snapshots. **A7-SEQ-000013 remains separately STAGED** pending actual A9 private reconciliation. Do not mark other repositories' app-specific themes changed. Browser screenshot verification is independent of automatic CI.
