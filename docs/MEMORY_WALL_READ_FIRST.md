# A7 Memory Wall — read first (SEQ-000017)

## User intent and accepted visual metaphor

A **study-wall or behind-the-door reminder poster**, not a quiz. Posters should be readable without tapping, flipping, recalling hidden answers, creating a deck, or opening an app. Treat them as passive spaced exposure to important reference names, short meanings and “when to use” cues.

The website has its own standalone `/memory-wall.html` subpage. The warm white/sky-mist noticeboard design deliberately differs from the deep-space animation of the Galactic Atlas, while preserving the same overall A7 navigation.

## Source and reproducibility

- Canonical *public site curation* (not scientific/domain facts): `registry/curations/memory-posters.v0.1.json`
- Generator: `scripts/generate_memory_wall.py`
- Derived Pages projection: `site/data/memory-posters.json` (generated with content hash and build SHA)
- Site: `site/memory-wall.html`, `site/assets/memory-wall.css`, `site/assets/memory-wall.js`
- CI: `scripts/validate_memory_wall.py` plus existing A7 validations and Pages readback
- User's originals: linked GitHub sources; separate private Drive bookmarking collection was written and read back on 20 October. **Do not copy its folder IDs or content to public Git.**

This is an independent presentation/curation update. It neither changes the nine A7 module identities nor migrates private A9 Main/Local libraries; A7-SEQ-000013 stays staged. Keep the source observation date; no scheduled monitoring is implied.

## Adding future posters

1. Verify the public repository URL and purpose from its original provider.
2. Add an entry with unique stable `MEM-EXT-####` ID, short headline, one-sentence description, action-memory cue, owner URL, a category ID, palette variant and `verified_on`.
3. Add a category only if helpful. **Do not** auto-admit public links as A7-owned module repositories or domain templates.
4. Run `python scripts/validate_memory_wall.py`, the existing registry suite, and Pages build. New posters may require a governed update to the strict initial 3-source validator.
5. Deploy through reviewed PR, check Pages source commit/artifact, inspect responsive, keyboard, print and reduced-motion behavior. Document any browser QA not performed.
6. Keep public page purely read-only; no Drive identities, secret tokens, private entries, or unverified dependencies.

## Layout acceptance

At rest all posters are visible. Filter is optional; default All. Cards feature large titles, symbolic illustrations, single short descriptions, direct GitHub link, and a bold memory anchor. CSS supports responsive cards and printable A4 poster sheets. No front/back state, no answer masking, no enrollment in the flashcard review experience. No persistent browser state needed.

## Poster collection 02 · Visualization techniques (A7-SEQ-000019)

Memory Wall now includes six additional glance reminders, **not** an extra six external GitHub links and **not** Anki quiz cards. They derive from `registry/decisions/visualization-workspace.json` through the existing `data/visualization-workspace.json` generator and `site/assets/memory-visualization.js`. Their status at record is displayed to prevent claims of uninstalled frameworks. The original technical visualization detail remains under `visualization-workspace.html` via the Memory Wall source link and History, not primary navigation.


## Collection 03 / permanent ecosystem operating architecture (A7-SEQ-000032)

**Existing canonical record reused, not duplicated:** `registry/curations/platform-responsibilities.v0.1.json`, stable ID `A7-MEM-PLATFORM-ROLES-005`. The A7 Memory Wall location remains `site/memory-wall.html#platform-role-board`. This is a versioned *operating recommendation*, not executable integration.

**One command. One source. One verified presentation.**

> AI operates. Drive preserves. GitHub versions. Actions verifies. Pages presents.
>
> **THE WEBSITE IS THE WINDOW, NOT THE SOURCE OF TRUTH.**

Source intent: a user gives an instruction; AI resolves authority and operates approved tools; Google Drive preserves original documents and images **when the fact-class and module rules designate it**; owning GitHub repositories version code, transformations, schemas and designated structured data; GitHub Actions generates and tests approved artifacts; GitHub Pages presents a *public-safe* navigable website. End users should navigate **Organization → Project → Category → Document/Answer/Resource** rather than the internal warehouse tree, and open original Drive links only when authorization/permissions allow.

**Qualification is compulsory:** A derived answer must disclose the governing source and revision, transformation/calculation, generator code version, validation, verified date, and approval/uncertainty. A successful workflow proves only the checks configured, **never** a structural engineering signoff, signed contract, private-source approval, or legal conclusion. Explicit status labels keep estimates, unverified material, needs-input, holds, derivations and genuinely signed/approved outputs apart.

**Security:** This public site must not publish restricted identifiers, ACLs, private documents, financial evidence, private drawings, or unauthorized derived answers. Google Drive permissions still govern source links. AI is not authoritative; GitHub is not a document warehouse; Pages is not private authenticated storage. No blanket Drive-to-Git migration, automatic Drive ingestion, real-time synchronized website, database deployment, or permissioned project portal is claimed as completed by this poster.

**Where rendered:** `site/assets/platform-responsibilities.js` + CSS display the durable curation, generated by the existing `scripts/generate_platform_responsibilities.py` Pages workflow as `site/data/platform-responsibilities.json`. The existing seven-platform roles remain, with AI added as the eighth explanatory role. The three external bookmark posters are governed separately and unchanged. The six visualization reminders are unchanged.

**Validation:** Run `scripts/validate_developer_dock_platform_board.py`, `scripts/validate_memory_wall.py`, both A7 CI/Pages workflow suites and desktop/mobile Chromium QA. Preserve user-facing print/readability, source privacy, exact versioned source/provenance and no duplicate poster IDs. The linked implementation history is Git native.

## Provider release readback — 2026-10-23

Collection 03 (the same existing poster ID) was revised through A7-SEQ-000032, feature [PR #69](https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph/pull/69), at `2dfb04c2b0827b6eebb628856195c5740774b04e`. Main Registry CI 39882325975 PASS, Pages 39882325976 PASS with provider artifact SHA-256 `64f96c25c623b98b6dd6317dd902eb2887f41278adfc17e0c67dc8b47ad5be04`; browser QA 39881697442 PASS. The build log confirmed eight platform responsibility roles and three unmodified public reference posters. This is **not** an assertion that independent direct HTTP GET/readback of the deployed body succeeded, nor that private project websites or automated Drive-to-Pages ingestion exist.

## Collection 04 / interface and prompting vocabulary (A7-SEQ-000033)

Canonical new and separate *explanatory* source: `registry/curations/memory-ui-vocabulary.v0.1.json` (stable ID `A7-MEM-UI-VOCAB-006`). It belongs to Memory Wall but is **not** a fourth external GitHub bookmark. The three original external reference posters, six visualization-role reminders and collection 03 operating principles are preserved without changes.

Use two comparison examples: (1) **fenced code block / monospace panel**, for precise, copyable source text, trees and inventories; (2) **interactive card / custom UI panel**, for records with working controls such as Show IDs and Copy register. Illustrative synthetic folder names/IDs are intentionally **not** real project or private Drive references. Thirteen categorized prompting terms cover static/interactive layouts, structured data/artifacts/evidence, and audit/provider readback operations. No claim is made that every chat client supports the same custom UI.

Generator: `scripts/generate_memory_ui_vocabulary.py`; derived Pages source: `site/data/memory-ui-vocabulary.json`. Rendered in `site/memory-wall.html#interface-vocabulary` with scoped `site/assets/memory-ui-vocabulary.js` and `.css`. Validate via `scripts/validate_memory_ui_vocabulary.py`, entire A7 Registry CI and desktop/mobile Chromium. The source is not an executable directory crawler and cannot serve private records. Preserve original buttons/nav and print layout; treat any provider validation as a distinct claim.

## Collection 05 / storage-only architecture (A7-SEQ-000035)

The existing Collection 03 covers broad provider responsibilities but **did not** contain the seven-format storage-role matrix. This new, distinct **reference collection** has stable ID `A7-MEM-STORAGE-ARCH-007`; it is not an external bookmark and does not change Collection 01 poster count (three), Collection 02 six visualization methods, Collection 03 existing canonical provider map or Collection 04 thirteen terminology prompts.

**Operating principle:** Drive preserves the original PDF/CAD/images/spreadsheets and permission model; appropriately governed GitHub repositories version relationship schema, PK/FK definitions and approved structured operational data. SQL = versioned schema, JSONL = append-only observations/audit, SQLite = private searchable snapshot, JSON = manifests/config and authorized relations, CSV = human review/import-export, Sheets/Excel = owner-designated operational entry/calculation/reporting, Drive = original binaries/source documents. Do not represent logical relational structure as Drive folder hierarchies.

**Critical boundary:** The A7 repository and GitHub Pages are public. Private SQLite inventory and restricted audit data may only live in their appropriately private owning storage; do not publish identities, ACLs, financial facts, private drawings, client records or new cross-provider relationships without owner authorization. Google Sheets/Excel can be the *actual* operational source under fact-class ownership; an exported CSV does not replace it. A versioned SQL DDL script does not prove a database instance exists. This collection describes a **design principle**, not executed migration, sync or ingestion.

Source: `registry/curations/memory-storage-architecture.v0.1.json`; generator: `scripts/generate_memory_storage_architecture.py`; derived Pages JSON: `site/data/memory-storage-architecture.json`; public anchor: `site/memory-wall.html#storage-only-architecture`; validator: `scripts/validate_memory_storage_architecture.py`; real browser QA runs on desktop and mobile. Preserve earlier four collections byte-for-byte at source, original A7 Galaxy template, all other repositories and all Drive folders/files.


## Collection 05 provider QA / release checkpoint — 2026-10-24

Feature PR #76 merged at `6b382db1c4bf73004c4ab03d9ba367d95ff9df9f`. A7 Registry run 40073991504 SUCCESS, Chromium desktop/mobile 40073991493 SUCCESS and Pages build/deploy 40073991520 SUCCESS, all at that same main SHA. Provider Pages build/deploy success is **not** independent direct HTTP served-content inspection. Original Collection 01–04 curations and L0 homepage remained unchanged; no user data migration. Post-merge source and publication are recorded in Git. POST snapshot must match the final closeout main commit.

## Collection 06 / extraction-to-evidence and six-collection contents (A7-SEQ-000036)

**Purpose:** Help human/AI operators determine how to read native source files (PDF, Google Docs, Excel/Sheets, DWG/DXF, unknown DWC, SKP, IFC/Revit, SHP/ArcGIS, GeoTIFF, ETABS, SAP2000, and containers) without hallucinating unobserved values. This is versioned *operating guidance* for cross-format extractors, **not** a newly deployed ingestion pipeline or a demand that A7 fetch private data.

**Contents panel:** `registry/curations/memory-wall-contents.v0.1.json` enumerates six existing section anchors on the same original `site/memory-wall.html` (1 external bookmarks; 2 visualization; 3 platform roles; 4 interface vocabulary; 5 storage-only; 6 evidence extraction). The machine manifest and page are generated/rendered through `scripts/generate_memory_extraction_guidance.py`, `site/assets/memory-wall-guides.js` and `.css`. Contents and the new reference remain independently navigable, mobile responsive and printable. Original five collections do **not** change canonical sources.

**Engineering extraction principle:** Prefer Python orchestration plus explicitly validated native format adapters. Start with provider identity/revision/permissions and immutable file hash. Extract source-native structure (no obligatory OCR/LLM step), preserve page/bbox, workbook sheet/A1/formula, DXF entity handle and layer, SketchUp instance path, IFC GUID and placements, GIS CRS/feature ID, CSI story/case/combination and engineering units. Never silently coerce unknown `.dwc` to `.dwg`. Every evidence record carries source ID/revision/hash, source locator, method/version, normalized value, transformation, verification/approval status, privacy/access classification.

**Retrieval:** JSONL + JSON Schema for granular evidence, private SQLite FTS5 for efficient exact/relation lookup, Parquet for analytics, GeoPackage/GeoParquet for GIS, IFC for BIM semantics, and optional derived Markdown/GLB for reading/preview only. Vectors/embeddings are optional **candidate ranking**, never proof; answers must cite exact source locators, calculations, units and unresolved gaps. JSONL and SQLite must remain **private** when populated with source-derived restricted content. Machine-validated records are not engineering-approved. File conversion must disclose semantic losses. Private material may be processed only through properly authorized owning-provider access and runtime.

**Owner boundaries:** A7 remains a public GitHub repository and Pages site. Only public-safe synthetic reference rules live here; no Drive reads, data migration, snapshots, app deployment, synchronization, or peer repo changes. The owning provider retains raw source files and ACLs; a permissioned future extractor would be a separate authorized task.

Canonical source: `registry/curations/memory-extraction-retrieval.v0.1.json`. Derived public-only data: `site/data/memory-extraction-retrieval.json` and `site/data/memory-wall-contents.json`. Validate `scripts/validate_memory_extraction_guidance.py`, existing previous collection QA, desktop/mobile Chromium and Pages build. Vendor links in curation document format capabilities, not project data.

## Collection 06 provider release checkpoint — 2026-10-25

Source-guided feature PR [#78](https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph/pull/78) merged `5851b450b28e455cde8caa062700e3e0ee72057b`; main Registry #40149409766, real mobile/desktop Chromium #40149409828 and Pages build/deploy #40149409757 all SUCCESS. Existing five original canonical collection sources unchanged. The new File Adapters table is guidance, **not** proof any user file was fetched, parsed, indexed or machine-approved. CI tests synthetic source-only curation and browser interactions. Independent remote served HTML body inspection is not claimed. The POST snapshot must match the final closeout main commit.

## A7-SEQ-000037 · Memory Wall editorial refinement (staged)

Source review conducted 2026-10-25 of all three public original READMEs: `nilbuild/developer-roadmap/readme.md` (developer career roadmaps, best practices and questions), `public-apis/public-apis/README.md` (community/API directory, with visible promotion; check individual access, authentication and price), and `sudheerj/reactjs-interview-questions/README.md` (React fundamentals, React 18/19, Router, testing, Redux and interview questions; site README includes sponsor links). Public source READMEs were read without copying their contents or changing the external repos. Their 2026-10-25 Git blob SHA observations live in the Chapter 01 ToC curation; those snapshot SHAs are historical observations, not live status assertions.

**Chapter 01 is now “Developer Learning Toolkit” (Learn → Discover → Practice).** The three original poster IDs/URLs and old permanent source curation remain unchanged. The opening and six ToC cards are shorter; chapters provide direct return links. Collection 06 renders all seventeen formats as compact accessible native `details/summary` rows, with method, derivatives, exact locator and cautions revealed on demand. The default visible content is shorter **without omitting any source fields, format families or records**. The old three-card bottom panel, which repeated instructions and implied only three poster references despite six chapters, is replaced by a single owner/permission reminder.

No Drive, A9, Communication & Web, other repository, ingestion backend or private content changes. The published A7 Memory Wall remains an explanatory public-safe projection. Browser QA must check six chapters, all three Chapter 01 links, all 17 format entries, mobile overflow, collapsed/expanded native details, keyboard usage, and original five other collections.

## SEQ 37 provider release checkpoint — 2026-10-25

Source review, Chapter 01 rename and ToC/detail UX were released by [PR #80](https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph/pull/80) at `66f36f1ca6cf356b9c79edbd26086f735cd49e5e`. Main Registry #40220229943 PASS, mobile/desktop real Chromium #40220229950 PASS and Pages build/deploy #40220229890 PASS. All original three poster URLs and six canonical collection IDs remain stable. Native file methods are collapsed by default for readability, available on-demand or search. No source corpus extraction or permission change. The POST branch must match final main. Provider deploy success does not constitute independent HTTP body inspection.
