# A9 → A7 Git + Drive operating contract (2026-10-09)

**Scope:** public-safe Git-first execution **for new versioned code/control work**, not a declaration that the private historic A9 Drive constitution was copied or superseded. The original A9 obligations remain in force for work that they govern until separately reconciled.

## Zero-duplication authority matrix

| Fact and artifact | Canonical owner | Cross-provider reference |
|---|---|---|
| Global system IDs, aliases, fact-class rules, authority and routing | A7 `main` versioned JSON/JSONL | Git commit SHA + A7 edge |
| Code, tests, normalized schemas, static website source, executable notebooks, build scripts | Owning Git repository/branch/commit | Repo+commit+path+hash |
| Thesis scientific facts, original researcher evidence, signed materials | Project-specific admitted Drive source/manifest (unless explicitly reassigned) | Exact Drive ID, provider version, source hash when available |
| Final compiled PDF, PPTX, native Google Docs/Sheets/Slides | Google Drive / native Google Workspace provider | Stable document ID + role + release/manifest ID |
| Git deployment success | GitHub Actions/Pages provider | Exact run+commit+conclusion |
| Private historical A9 Local/Main Library, catalog and project relations | Existing controlled Google Drive indexes until a verified private replacement exists | Stable IDs, event/edge pointers; **no full public mirror** |
| Public map, portal, graph and rendered HTML | Generated from owning sources | Never a scientific authority |

## Minimal AI entrypoint (not a token-heavy preamble)

1. Fetch **`A9_GIT_DRIVE_BOOTSTRAP.json` from A7 `main`** and record its commit.
2. Resolve repository from **`registry/entities/repositories.json`**, then fetch target `A7_MODULE.json` and the relevant owner-only control/current manifest.
3. Fetch Git HEAD and current live provider object **only for the requested fact/artifact**; scope by project and task, not the entire archive.
4. Make bounded changes with optimistic SHA concurrency. In Git, a branch is a **complete repository ref**: do not equate a branch with one person's isolated storage. Put researcher code under folders, and create task/feature branches only when useful.
5. For a new build: commit the source; build/QA; upload compiled PDF/PPTX to Drive; read back the Drive file ID; register the mapping in the owning repository manifest and A7 semantic edges (where permitted); update Pages projection.
6. Git commit history gives PRE/POST and diff for Git files. Keep a separate Drive PRE snapshot **only when needed for non-Git authoritative bytes/native documents or a specific binding project rule**.
7. End with exactly what passed, what is unverified and the next boundary. Never log completion before provider readback.

## Global vs local governance

A7 defines **how to resolve and route**; each repository owns **what it builds** and each thesis controls **what it scientifically asserts**. GitHub can version code and source used to reproduce a report, but Git does not magically version all Google Docs content or prove it was admitted. Google Drive itself has revision history; custom duplicate version numbering is not required for every Git commit. Use release manifests as a bridge.

An example artifact bridge record is `{ "artifact_id": "ART-...", "project_id": "...", "git": {"repo": "...", "commit": "...", "path": "..."}, "drive": {"file_id": "...", "role": "COMPILED_PDF", "revision": null}, "qa": {"status": "VERIFIED", "run": "..."}, "edges": ["GENERATED_FROM", "BELONGS_TO"] }`. Keep this in the owning private project/ledger if publishing it would expose restricted metadata.

## Migration gates and deliberate holds

- Phase A **ACTIVE**: A7 public-safe operating rule + normal Git history + federated module links.
- Phase B **IN PROGRESS**: research portal restores historical public-safe static modules, links to Drive outputs, and aligns controls.
- Phase C **NOT COMPLETED**: private original A9 control-text/exception parity, private Main Library transactional migration, historical digest comparison, and cutover. No old A9 source is deleted or overridden.
- `MSCH_HYDROPOWER_CORPUS_B013` remains **HOLD / DO NOT RESUME**.
- Public GitHub repositories may not host confidential private Drive corpus, bank documents, research raw data or personal records.
- The A7 document is a reusable template accessible from all repositories through `AGENTS.md`/module references; ChatGPT still requires a connector/current fetch to enforce it. Do not claim that an account-wide automatic system instruction was changed.

## Why this reduces friction

Git commits store precise code changes and historical diffs without hand-maintained duplicate snapshots. You read one short bootstrap plus owner contracts rather than reloading entire Drive towers on every request. Token savings are an **expected workflow benefit, not a guaranteed conversation-length fix**.
