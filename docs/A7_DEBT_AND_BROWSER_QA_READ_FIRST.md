# A7 debt/QA reconciliation — 21 October 2026

The purpose of SEQ-000023 is to clear only **source-evidenced and testable A7 debt**, while keeping the private A9 and researcher-scientific quality gates honestly open.

## Verified dated R&D repository provider status

R&D main `b9863d1f8aa4be1db8f948037bb4131c77804e4b`, same commit for these **successful** workflows: repository CI `39585297906`, source-only LaTeX rules `39585297654`, Pages control portal `39585297540`, Saugat approved editorial production `39585297927`. This closes the **old claim** that current R&D main CI is failing. It does **not** certify all PDF outputs or all researcher manuscripts, and the source gate explicitly says "NO scientific PDF".

## Private A9 bridge stays correctly unacknowledged

The live native Main Library provider has the canonical `ArtifactRegistry`, `ArtifactEdges`, `LocalLibraryRegistry` schemas. Its versioning remains live in Drive, and searching current A7 repository slug in the private Main registry returned no matches. The A7 source bridge remains `CANDIDATE_NOT_IMPORTED`; a dry-run digest is not an ACK. A9 seq13 historical Main/Local parity, PK/FK, collisions and consumed cursors require a separately governed private reconciliation. This release makes NO Main/Local modifications and publishes NO private IDs.

## Browser QA

`.github/workflows/a7-browser-qa.yml` builds the exact generated public projection, runs Chromium with real DOM events at desktop 1440px and mobile 390px, confirms nine stations, four documented links, default-hidden proposals, source evidence anchors, station selection, search/reset and reduced-motion mode, and saves screenshots+JSON assertions. This is automated viewport/interactive QA rather than a human sign-off or external Pages-hosted visual acceptance. The runner's CI result determines whether this test closes the automated-QA debt.

## Release and continuation

PRE → feature CI and PR → main merge/CI+Pages → closeout and POST equality. The immutable evidence model for Arc05 can follow once the scoped A7 debt release is provider verified. Preserve Cloud Orbit, mascot, Arc03/04, A9, and specialist owners.

## Source provider acceptance

A7-SEQ-000023 feature PR #51 merged at 4ca4119ef9251c8357877c147b3beffb7d8ab1ce. Registry CI 39592347665 SUCCESS, Pages run 39592347916 SUCCESS, real Chromium browser QA 39592347739 SUCCESS. This does not certify human design sign-off, private A9 ACK, researcher PDF scientific QA or runtime interfaces.
