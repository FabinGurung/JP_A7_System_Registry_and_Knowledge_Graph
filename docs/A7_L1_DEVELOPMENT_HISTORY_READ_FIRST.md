# A7 L0/L1 development history — Git remains the sole version authority

**Scope:** A7-SEQ-000027 only. No Google Drive A9, other repository histories, source migrations, or additional L0 home.

- **L0** is `site/index.html` and retains the Cloud Orbit Galactic Atlas, unified navigation, fluffy rocket and Arc05 release inspector.
- **L1** is the existing `site/history.html`, upgraded to a developer-facing history view with archived interfaces preserved inside a collapsed section.
- **Git commits and actual Git tags** come from the checked-out Git history at Pages build (`fetch-depth: 0`). **Merged A7 PRs and Actions runs** come from GitHub's original public provider API during Pages builds. All external source links target this A7 repository.
- `scripts/generate_a7_development_history.py` is a deterministic output-shape builder; Pages requires provider readback and fails if PR/Actions API evidence is unavailable. CI/browser QA use `--offline` and explicitly do not present dummy provider records.
- The generated `site/data/development-history.json` is derived, not canonical. Build timestamp, source SHA and sample caps appear on the page. Changes that land after a Pages build need the next deployment to appear here; the linked GitHub pages are the current source of truth.
- Commits are not releases. Merged PRs are not scientific or business approval. Actions success is a CI/deployment provider result, not independent acceptance.
- The older Classic Graph, pre-Galactic milestone and six-technique reference remain available under the archived-content disclosure. Existing Arc05 display and specialist boundaries remain intact.
- `python scripts/validate_a7_development_history.py --data-dir site/data` validates sample bounded source evidence; desktop/mobile Playwright QA checks L0 navigation, history search, commit link, filters and layout.

This feature intentionally **does not open or update A9 Google Drive Main Library**, create ACKs, alter other repositories or add an external database. GitHub already preserves revision history.

## Actual source-release gate — 22 October 2026

Feature [PR #59](https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph/pull/59) merged at `89ae9616d184d2cd2db2d3177b53fcaeb0df28e8`. GitHub Actions Registry CI 39699665201, Pages 39699665198, real desktop/mobile Chromium QA 39699665196 all SUCCESS. The provider-backed Pages generator recorded 80 commits, 24 merged PRs and 24 run snapshots (bounded samples). Source commit SHA and build time always appear on the L1 page. GitHub stays canonical for the underlying records; no external file system controls were changed. Closeout and POST parity follow.
