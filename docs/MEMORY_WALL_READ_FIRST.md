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
