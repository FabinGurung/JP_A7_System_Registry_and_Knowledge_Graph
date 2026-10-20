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
