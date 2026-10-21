# GitHub → private Main Library bridge — current identity projection verified; historical ACK open

## Exact live table schema verified 2026-10-09

The private native workbook `Fabin_Gurung_Drive_Index` exposes **ArtifactRegistry** with 16 columns, **ArtifactEdges** with 10, **LocalLibraryRegistry** with 26, plus Index, RunLog and VersionLog. The current observed workbook contains numerous PRE/POST sheet copies; this is evidence of historical Drive-heavy bookkeeping, **not** a reason to create similar duplicates for Git.

No confidential workbook data or spreadsheet ID is placed in this public repository.

### Public candidate workflow

1. Query GitHub for **all current default branch references**, record each immutable provider repository ID + full name + ref + observed SHA. The capture is in `registry/bridges/github-heads-20261009.json`; it is point-in-time, not a live promise.
2. Run `python3 scripts/build_main_library_bridge.py --out build/main-library-candidates`. It validates public-only metadata and produces CSVs matching exact observed **ArtifactRegistry** and **ArtifactEdges** headers.
3. Review `bridge-manifest.json`, with source/output SHA-256 digests and `DRY_RUN_PASS__NO_GOOGLE_DRIVE_WRITES`.
4. **Do not import blindly.** Resolve existing Main artifact identity and PK/FK edges, check concurrency/last Main ACK, compare each old external-ID target with the new Git provider ID and verify live HEAD. Import through a separately governed private A9 write when explicitly authorized.
5. After exact Main provider readback, register a Git commit/release pointer and `GENERATED_FROM` or `ROUTED_BY` edges in Main; Google Drive owns the content/row state. Avoid one row per ordinary code commit: Git itself already retains complete history. Record changes at meaningful release or synchronization boundaries.

## 22 October 2026 — approved bounded provider reconciliation

The public repository-identity layer is now **provider-confirmed in the existing private Main Library** after a bounded, authorized original-provider mutation and exact post-write readback. Existing private Main identities were reused and missing public GitHub identities admitted, with navigation-only metadata relations. All private record identifiers, foreign keys, workbook coordinates, native revision receipts and PRE/POST evidence are retained **only in the private Main/Local custody and its owner audit**, not in this public repository.

**Critical distinction:** the 9 October candidate CSV files were **not imported or replayed**. The candidate exporter remains a dry-run artifact and is still non-mutating. A dated private Main identity projection is neither a legacy A7-SEQ-000013 source/control-text parity certificate nor an authenticated Local-to-Main consumed-cursor ACK. No local sequence or synchronized cursor was invented, no researcher/project payload was moved, and no runtime integration or private control migration has been asserted.

### Current state and limits

- A7 has **9 public connected repositories** in the observed snapshot.
- This executable exporter is a **non-mutating candidate bridge**; it does not call Google Drive/Sheets APIs.
- No GitHub token, Google authorization or private records are needed for the offline dry run.
- Git commit SHA is distinct from SHA-256 file bytes. The `SHA256` candidate column is left blank rather than mislabeling the hash.
- Current Main Library and project-local artifact/version/edge registration remain the authority for prior A9 work. Full source parity and cutover remain incomplete.

## Typical released research lineage

`A7 PROJECT_ID → REPO/COMMIT/PATH → BUILD/QC/RELEASE → DRIVE_PDF_OR_PPTX_ID → LOCAL_LIBRARY → MAIN_ACK`

The human website is only a projection of this chain. Scientific admissibility is governed by the researcher/project, not by the existence of a webpage or a successful GitHub workflow.

## Source release verification

Public status implementation PR #57 merged at `d5300d9e424afaa7159fed77bd7d3182ed50fcf7`; Registry CI 39688855866 PASS and Pages run 39688855848 PASS, while the private native Main readback and PRE/POST are stored only in private provider custody. The 9 October CSV candidate source remains dry run. Full historical private reconciliation and Local-to-Main consumed-cursor ACK remain unverified and explicitly staged.
