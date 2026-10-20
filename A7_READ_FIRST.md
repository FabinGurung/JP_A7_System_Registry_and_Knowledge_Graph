# A7 READ FIRST

## 1. Purpose

A7 is the GitHub-versioned semantic control plane for identities, authority rules, provider object references, aliases, typed edges, schemas, policies, lineage and generated-view definitions.

A7 is not a universal copy of every source file and is not permission to infer missing facts.

## 2. Bootstrap order

For any A7 task:

1. Read `A7_BOOTSTRAP.json`.
2. Resolve the requested entity by permanent A7 ID or governed alias.
3. Load applicable global policy.
4. Resolve the requested fact class.
5. Load the most-specific authority assignment: entity override → project override → module override → global fact class.
6. Load the originating provider policy.
7. Fetch the live provider when current state is required.
8. Verify provider object ID/revision/timestamp where available.
9. Classify candidate claims as declared authority, verified human-QA resolution, evidence, projection or unknown.
10. Apply `registry/authority/conflict-resolution.json`; never use recency unless the fact class explicitly permits it.
11. If unresolved material/safety conflict remains, open human QA instead of guessing.
12. Mutate only the declared writable authority.
13. Regenerate downstream projections.
14. Run validation/CI.
15. Provider-read back the result.
16. Close the same bounded A7 sequence; do not create a new sequence merely to acknowledge it.

## 3. AI behavior

The AI is a resolver/operator, not a source of truth.

Never:
- use chat memory as authority when a governed source exists;
- choose a value merely because it looks newer;
- invent a project-specific route;
- infer completion from an unlabeled image;
- silently reconcile conflicting provider claims;
- treat a communication statement as automatically proving its real-world claim;
- edit generated HTML/CSV/graphs to change an authoritative fact.

## 4. Conflict and human QA

Authority precedes recency. Provider truth and domain truth are distinct: Slack/Discord/email/WhatsApp may prove what was said; Drive may prove which file/revision exists; Sheets may prove exact cell state; GitHub may prove repository/ref/workflow state. The applicable fact-class contract decides whether those provider facts are also the domain authority.

If material evidence contradicts the designated domain authority, keep the current authority value, record the disagreement, and open a human-QA reconciliation case. If multiple valid authorities disagree, block the canonical mutation until QA or an explicit version rule resolves it.

A human-QA request must include:
- QA case ID;
- entity/project ID;
- disputed fact class and conflict type;
- each conflicting statement/value;
- provider/evidence references;
- associated conversation/evidence link when available;
- a short explicit question.

Preferred route: governed project Slack thread/channel, then email where Slack is unavailable or email is the governed responsible-person route. The confirming response must be provider-referenced before it can resolve the case.

## 5. Three-attempt fail-forward rule

For a connector/provider action that fails:

- attempts 1–3: retry only when a materially different or reasonable attempt is possible;
- after 3 failed attempts: record the deferred dependency/problem and continue the next independent task;
- never fabricate the blocked fact;
- mark the affected item `BLOCKED`, `UNVERIFIED` or `AWAITING_PROVIDER`;
- report the failed dependency and last error in closeout.

See `policies/global/fail-forward.json`.

## 6. Public safety

This repository is public. Store metadata and public-safe relationships, not confidential payloads. Private provider object IDs/labels require an explicit public-safety decision before publication. See `policies/global/public-safety.json`.

## 7. Writable and derived formats

Canonical writable:
- JSON for current normalized state;
- JSONL/NDJSON for append-only events, edges, aliases, provider observations and QA events.

Formal contracts:
- JSON Schema;
- PostgreSQL-compatible SQL DDL.

Generated/non-authoritative:
- CSV;
- Mermaid;
- graph JSON;
- search indexes;
- Markdown summaries;
- HTML;
- Excalidraw projection data;
- Three.js/3D graph data.

## 8. PostgreSQL status

A live PostgreSQL/Neon runtime is deferred while there is one primary writer and other users are read/search-only. SQL DDL is used as a formal relational language without requiring a database service.

## 9. Namespace separation

A7 is this GitHub semantic registry. Other established A-number namespaces remain separate systems and must not be silently renamed into A7. See `registry/entities/systems.json`.

## 10. Git-native closeout

Each bounded mutation has:
- sequence ID: `A7-SEQ-NNNNNN`;
- event IDs: `A7-EVT-NNNNNN-NNN`;
- PRE commit SHA;
- working branch;
- validation result;
- merged/final commit SHA;
- provider readback;
- final status.

A sequence may contain many events. Acknowledgement alone does not create another sequence.

## 11. Phase-2 authority engine

Canonical machine contracts:
- `registry/authority/fact-classes.json`
- `registry/authority/authority-map.json`
- `registry/authority/provider-roles.json`
- `registry/authority/conflict-resolution.json`
- `registry/authority/conflict-taxonomy.json`
- `registry/authority/vocabularies.json`
- `registry/authority/authority-overrides.jsonl`
- `registry/qa/human-qa-cases.jsonl`

The reference resolver in `scripts/a7_authority_engine.py` operates only on claims already classified from those contracts; it does not invent authority from a provider name.

## 12. Module ownership boundary

Before performing domain work, resolve the owner module in `registry/entities/modules.json` and its boundary in `registry/authority/module-ownership.json`.

A7 is the semantic control plane. It may resolve, route, fetch, validate and orchestrate, but it must not duplicate the domain data/work of the owning module.

The execution modules are peers:

`MOD-OPS-001` · `MOD-SCHED-001` · `MOD-COST-001` · `MOD-STRUCT-001` · `MOD-CAD-001`

Operations may link to/surface Scheduling, Cost, Structural and CAD in human-facing project pages. `LINKS_TO_PEER_MODULE` is navigation only; it must never be interpreted as containment or ownership.

R&D and Study are separate peer knowledge modules. R&D publication does not absorb executable specialist engines.


## 13. Cross-repository module manifest

Every bound specialist/knowledge repository exposes `A7_MODULE.json` at its default-branch root.

When entering a module:

1. Resolve the module and immutable repository identity from A7.
2. Fetch `A7_MODULE.json` from the repository default branch.
3. Verify `module_id`, `repository_id` and `provider_repository_id` against A7.
4. Load the central ownership profile and authority map.
5. Select only the routing entrypoint relevant to the requested task.
6. Fetch that exact ref/path live when current state matters.
7. Mutate only the owning domain/provider.
8. Provider-read back the mutation.

`A7_MODULE.json` is routing metadata, not domain truth. It must not contain or replace Daily Ops facts, schedules, BOQs, structural results, drawing revisions, research findings, study content or original Drive files.

## 14. Pinned visualization strategy

Before modifying the A7 visualization layer, read `registry/decisions/visualization-workspace.json` and `docs/VISUALIZATION_WORKSPACE_READ_FIRST.md`, plus the live source and deployment. The design is pinned at `site/visualization-workspace.html` and in the main website navigation. Preserve the six preferred roles and be explicit about **planned vs installed** technology. Material deviations require a governed and traceable decision update.

## 15. Cross-provider A9 migration entrypoint — 2026-10-09

For **all new Git/Drive multi-repository work**, start with [`A9_GIT_DRIVE_BOOTSTRAP.json`](A9_GIT_DRIVE_BOOTSTRAP.json) and only the fact-specific owner contract. The full public-safe rule lives in [`docs/A9_GIT_DRIVE_OPERATING_RULE.md`](docs/A9_GIT_DRIVE_OPERATING_RULE.md). The [governance map](https://fabingurung.github.io/JP_A7_System_Registry_and_Knowledge_Graph/governance.html) gives human links. This centralizes new cross-provider **routing**, not all historic private A9 control text. The old Drive control documents still govern their existing private/non-migrated workflows until parity and cutover are expressly verified.

## 16. Coordinated A7 and R&D roadmaps

On resumption read [`registry/roadmap.json`](registry/roadmap.json) and [`docs/ROADMAP.md`](docs/ROADMAP.md) for the global control-plane work. The owning R&D repo publishes [its own researcher roadmap](https://fabingurung.github.io/JP_Research-and-Development/roadmap/) and [A7 cross-thread handover](https://github.com/FabinGurung/JP_Research-and-Development/blob/main/docs/HANDOVER_TO_A7_20261009.md). They are work-planning views and do not override provider object state or older A9 private constraints.

## 17. Control Tower Atlas: do not confuse governance layers

Use `docs/CONTROL_TOWERS_READ_FIRST.md` and `registry/controls/control-tower-map.json` for semantic resolution of global controls, R&D contracts, private A9 thesis/PPTX control and Main/Local library rules. Public site: `site/control-towers.html`. This is navigation/decision metadata, not a replacement for the private Drive provider or a claim of private A9 migration completion.

## 18. Cross-repository AI-aided product guide (2026-10-15)

User-facing websites expose **How It Works** near the first action; hide machine controls behind **For builders / AI agents**. Canonical guide standard: `policies/global/ai-aided-product-guide.v0.1.json`. Versioned human template: `docs/AI_AIDED_PRODUCT_GUIDE_TEMPLATE_v0.1.md`. Survey: `registry/decisions/ai-aided-guide-adoption.v0.1.json`. The AI interprets natural language and resolves governed sources; deterministic owner-specific GitHub engines execute normalized validated requests. Repeatability requires pinned canonical inputs/runtime/source bytes; a prompt alone cannot guarantee identical output. The site guide is a projection, not a second authority. Only CAD and A7 are in the initial implementation scope; other surveyed repositories remain unchanged.

## 19. Personal learning Memory Wall / SEQ-000017

Read `docs/MEMORY_WALL_READ_FIRST.md` and curated Git source `registry/curations/memory-posters.v0.1.json`. Site page `site/memory-wall.html` visualizes always-visible posters and optional print, not quiz/Anki flashcards. Curated *external* GitHub bookmarks are not A7 module registrations or owner facts. Do not copy the original private Google Drive reference-folder IDs to the public repository. A7-SEQ-000013 private A9 reconciliation stays separately staged.

## 20. Cloud Orbit site-only theme

The Cloud Orbit style decision is `registry/decisions/cloud-orbit-theme.v0.1.json`. All ten public A7 HTML pages load `site/assets/a7-unified-theme.css` last and `site/assets/fluffy-rocket.js` as a decorative, motion-accessible mascot, without modifying A7 semantics, project data or peer repositories. The public Operations map example is not a theme donor and is never mutated as part of A7 normalization. Validate with `scripts/validate_unified_theme.py`. A7-SEQ-000013 private A9 cutover remains staged.

## 21. A7 unified nav + preserved history (A7-SEQ-000019)

Site shell `site/assets/a7-site-shell.js`/`a7-site-shell.css` is the current common header/navigation/footer. Six visualization methods appear under Memory Wall by reading the existing versioned decision, not by pretending Cytoscape/React Flow are installed. The original dashboard's 2D/3D graphs and routing matrices still have unique advanced uses and remain reachable from `history.html`, not as a separate homepage. Preserve all existing URLs and release tags. `docs/HISTORY_AND_ROLLBACK_READ_FIRST.md` gives migration/rollback QA. A7-SEQ-000013 private A9 is still staged.

## 22. Galactic Atlas Arc 02 (A7-SEQ-000020)

Read `docs/GALACTIC_ATLAS_ARC02_READ_FIRST.md` and the provider-dated `registry/providers/galactic-atlas-arc02-observation-20261020.json`. The inspector joins nine A7 owner definitions to dated GitHub run/source observations and renders explicit boundaries and gate text. It must never imply a new runtime cross-repository dependency, project approval, private A9 acceptance, or always-live provider status. Source code and six app engines other than the intentionally changed `galactic-atlas.js` remain stable; Cloud Orbit and the fluffy rocket remain unchanged.
