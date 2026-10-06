# A7 Phase 3 — GitHub Repository / Pages / Workflow Inventory

## Scope

This inventory records all nine repositories returned for owner `FabinGurung` by the connected GitHub provider on 2026-10-06, their immutable numeric repository IDs, current default branches, all observed branch heads, Pages evidence, current custom workflow definitions, system-role candidates and notable publication findings.

It does not rename, merge or repair specialist repositories.

## Pages evidence hierarchy

Because the connected GitHub tool does not expose the direct `/pages` settings endpoint, A7 uses the strongest available equivalent evidence:

1. repository `has_pages` + `homepage` metadata;
2. current branch/workflow files;
3. workflow permissions and use of `actions/deploy-pages`;
4. explicit ownership guards inside workflow files;
5. latest successful Actions runs and their head branch/SHA;
6. GitHub-managed dynamic Pages run history for branch-based publication.

The limitation is explicitly recorded in `github-inventory-meta.json`.

## Key findings

- Structural Analysis: main owns Pages, but the site builds from an older pinned engine commit rather than the current engine branch head.
- CAD: live Pages currently comes from `narayani-modular-website-v0.3`, while the default branch remains `narayani-pages-v0.2`.
- Scheduling: `kernel-v0.2-open-source-engines` is the explicitly enforced production Pages owner; default branch remains `main`.
- R&D: current production Pages ownership is correctly centralized on `main`; inspected research branches now contain non-production guards/validators.
- Communication/Web Ops: `feature/daily-ops-current-work` currently owns production Pages even though the workflow name says “preview”.
- Cost: the production workflow is triggered from `main` but deliberately deploys content checked out from the research branch.
- Study Hub: `pages-live` is the current Pages source.
- Sumita Pilates Studio: `gis-site-selection` is the latest Pages source.
- A7: Pages is enabled but no production deployment has yet been observed; visualization is intentionally deferred.

## Historical aliases

The available provider API does not expose authoritative repository rename history. A7 therefore does not invent former slugs. The known A7 predecessor slug remains a governed alias, and “Project Controls Kernel” is retained as a verified historical product label because it appears in the scheduling repository’s workflow history.

## Dependencies

No provider-verified cross-repository dependency edges are asserted in Phase 3. Current default-branch code-search attempts for specialist slugs in the Operations and R&D hubs returned no indexed hits. Module binding/wiring is therefore deferred instead of inferred.

## Next boundary

With repository identities and Pages ownership mapped, the next clean execution phase is Drive topology indexing. Specialist module binding can then use both immutable GitHub repository IDs and Drive object IDs rather than mutable names.
