# JP version control — A7 roadmap subject

## One populated live subject
A7 tasks live in **one** writable source: `registry/roadmap.json` with stable ID `A7-ROADMAP-20261009`. `pinned_task_ids` are references to existing `next[]` records, never a second task list. The Pages JSON and HTML are **derived** by `scripts/generate_a7_roadmap.py` and GitHub Actions. Peer module task sources, original Sheets and native files remain at their owning provider; no A7 permission to rewrite them.

## Enumerated PRE and POST
The central, subject-specific A7 archive is `registry/archives/roadmap/`. Number `000001` is a snapshot ordinal, **not** a Sheet, notebook, release or sequence version. `000001_PRE_A7_SEQ_000040.json` contains exact original source before edits. After CI validation, `000001_POST_A7_SEQ_000040.json` must equal the final source byte-for-byte. `manifest.json` records the source pointer and recovery; `version-history.jsonl` is append-only, with changes, reasons, original evidence links, validation and restoration. Restore contents of an archived snapshot **into the same canonical live source path/ID** with a reviewed PR, then validate and provider-read back. Do not rename live sources or force-push.

## Separate authorities and evidence stages
Humans edit source Sheets and notebooks in their respective owner systems. Sheet revisions, notebook revisions, Git release tags and roadmap snapshot ordinals remain separate. Do not publish restricted source files, source messages, private provider IDs or user chats to a public Git repository; original private chat messages stay in their original provider and missing URLs are recorded as null, never invented. Do not invent quantities, costs, approval, source validation or completion.

Distinguish **prepared code** (commit exists), **offline test** (actually run), **live GitHub Actions** (verified run IDs), **GitHub Pages deployment** (verified run), and **independent public HTTP body inspection** (only if performed). Successful GitHub Pages or a tag does not prove engineering QA. Historical private A9 Main/Local parity and peer bootstrap drift remain separate holds.

## Pinned live task pointers
`A7-N05`: dated A7 progress without false real-time monitoring.
`A7-N10`: A7 operator guidance, separate from developer tools.
`A7-N04`: peer read-only hold; no cross-repository modifications.
