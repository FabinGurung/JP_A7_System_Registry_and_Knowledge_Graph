# Generated outputs

Everything under `generated/` and every build-time file under `site/data/` is **derived and non-authoritative**.

Do not hand-edit a generated file to change a fact. Change the canonical JSON/JSONL record or owning provider, validate it, and regenerate projections.

## A7 visualization derivation

`scripts/generate_visualizations.py` derives the public-safe visualization layer from canonical A7 inputs. The Pages workflow generates these artifacts from the exact deployed commit:

- `a7-summary.json`
- `a7-graph.json` — shared 2D/3D semantic graph
- `a7-search-index.json`
- `project-module-matrix.json`
- `authority-projection.json`
- `a7-architecture.mmd`
- `a7-excalidraw.json`
- `derivation-manifest.json` — SHA-256 source/output lineage

`scripts/validate_visualizations.py` fails closed on dangling graph edges, missing project/module routes, duplicated IDs, authority-boundary violations, or leakage of Drive topology node IDs into the public graph.

### Public-safety boundary

The public website projects A7 semantic metadata only. Google Drive topology nodes are intentionally not emitted into the public graph; the website receives only an aggregate count showing that such governed nodes exist.

### Website

The static UI in `site/` renders the generated artifacts with no runtime database and no third-party JavaScript dependency. GitHub Pages is a projection surface, never a domain authority.
