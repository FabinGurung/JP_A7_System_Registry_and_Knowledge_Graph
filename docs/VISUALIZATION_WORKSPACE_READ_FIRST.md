# VISUALIZATION WORKSPACE — A7 READ FIRST

**Decision:** A7-VIS-DEC-000001  
**Machine record:** `registry/decisions/visualization-workspace.json`  
**Pinned website:** [Visualization Workspace](https://fabingurung.github.io/JP_A7_System_Registry_and_Knowledge_Graph/visualization-workspace.html)  
**Sequence:** A7-SEQ-000012

## Immutable intent, evolving implementation

The user-approved preferred pipeline is:

1. **Cytoscape = semantic exploration** (target; currently custom Canvas 2D, not Cytoscape)
2. **React Flow = system architecture / deterministic routing** (target; currently custom HTML/CSS/JS)
3. **Tables = audit and QA** (implemented)
4. **Mermaid = documentation-as-code** (generated .mmd source only; not a Mermaid JS site renderer)
5. **Excalidraw = human annotation/presentation** (generated JSON export only; no site editor/plugin)
6. **3D = optional spatial exploration** (lightweight custom Canvas XYZ perspective; not Three.js/WebGL)

Those statuses are **observations at the time this decision was created**, not permanent claims. Reverify against live source.

## One derivation, multiple projections

A7 canonical JSON/JSONL + owning provider authority → `scripts/generate_visualizations.py` → graph/search/matrix/Mermaid/Excalidraw/XYZ → read-only GitHub Pages UI. Neither generated artifacts nor the site can replace provider/domain authority.

## Resume without hallucinating

Read `A7_BOOTSTRAP.json`, the decision JSON, actual rendering JS, Python derivation generator, validation scripts and current GitHub Pages workflow. Resolve fact class, module and source provider before asserting domain truth; differentiate installed from preferred. Do not assume route=artifact exists. Preserve Git-native sequence PRE, CI, merge, live readback and identical POST. If a technology/role changes, update the decision, pinned page, validation and append-only events in the same governed mutation; never silently drop or alter this strategy.

## Source evidence

- `site/index.html` and `site/assets/app.js`: actual Canvas, routing matrix and authority table UI.
- `scripts/generate_visualizations.py`: generated .mmd, Excalidraw JSON, graph XYZ, search and hashes.
- `registry/routing/project-module-bindings.json`: project-to-module routing.
- `registry/authority/authority-map.json`: canonical fact ownership rules.
- `site/visualization-workspace.html`: pinned human-facing decision projection.
- `.github/workflows/deploy-a7-pages.yml`: production Pages derivation and deployment.

**Public privacy boundary:** no private/internal A9 Drive labels, IDs or document bodies in the public graph. A7 is the semantic control plane and resolver, not the owning provider for specialist work.
