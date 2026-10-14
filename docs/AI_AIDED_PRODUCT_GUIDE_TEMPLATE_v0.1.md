# A7 Universal Product Guide — AI-Aided, Human-Language First (v0.1)

**Single canonical, versioned template** for FabinGurung product repositories. The normative machine contract is [A7-POL-AI-AIDED-INTERACTION-001](../policies/global/ai-aided-product-guide.v0.1.json). A7 owns guidance *semantics and cross-repo navigation*, never the domain engineering, financial, research or operational truth.

## Where to put this on every website

The primary user-facing entry is **How It Works**, linked in the main navigation and near the product's first action. Do **not** bury it inside repository trees, control towers, source registries or a page labelled only “Developer Guide.” The site should provide:

1. **Start here — ~30 seconds:** Say a goal in plain language, provide an existing file or select an example; highlight the next user action.
2. **How it works — ~2 minutes:** One visual lane: language/input → AI interprets + evidence → deterministic engine → verified outputs → clickable view. State exactly what happens automatically and what remains unverified.
3. **Explore the result:** A domain-specific primary view, with progressive drilldown by role, component and task. A CAD site favors **3D first**, then 2D drawings/sections; Scheduling favors roadmap/milestone timeline; Cost favors estimate/BOQ; Structural favors model and results; R&D and Study favor research/study artifacts.
4. **Sources, status and safety:** Show source revision and owner, validation state, unresolved inputs, privacy and licensed approval boundaries. Claims such as “ready for construction”, “approved research” or “actual market price” require their proper owner.
5. **For builders / AI agents:** Link the owning `A7_MODULE.json`, exact engine versions, machine schema, reproducible example, CI, PR/commit and source/output hashes. Do not make workers read this section to operate the product.

## The mandatory execution contract

`UNDERSTAND → RESOLVE → NORMALIZE → EXECUTE → VERIFY → EXPLORE → TRACE`

- **Human** communicates naturally; should not handwrite JSON, schemas, DXF, command invocations or tool prompts.
- **AI** is the interpreter/operator, not the source of truth; it checks live provider/source authority, classifies facts, extracts supported values and asks targeted follow-ups.
- **Owning GitHub code** is a reproducible computation/validation contract; GitHub does **not** itself possess a hidden language-model reasoning system.
- **Machine** rejects unverified inputs/units, keeps explicit missing inputs, and runs appropriate fixed, tested versions; private data requires an authorized private runner.
- **Results** appear in a humane, filterable, mobile-first product; they are linked to source and validation evidence, not merely attractive presentations.
- **Version history** includes canonical input hash, source revision/hash, engine commit, runtime/dependency pin, output artifact manifest, tests/QA and release/approval state.
- **Claims of 100% repeatability** apply only to a fully pinned *canonical* deterministic run, not arbitrary AI interpretations or changing external inputs.

## Copyable content skeleton

| Area | User-facing copy to adapt | Required evidence |
|---|---|---|
| Intro | “Tell us what you want to achieve.” | Available action; no JSON required |
| Flow | “We interpret your instructions, check existing records, run the appropriate engine, and show you the result.” | Clear distinction AI vs GitHub engine |
| Explore | “Select an item to reveal the right details for your task.” | Filter, levels, labels, provenance, accessibility |
| Reality | “This result is [verified/draft/held] based on [source revision].” | Explicit truthful status |
| Next action | “To progress, we still need [specific missing facts].” | No guessed values |
| Technical | “Reproduce from these pinned inputs and engine versions.” | Live commit, QA and checksums |

## Cross-repository survey (connected GitHub account, 2026-10-15)

Nine `FabinGurung` repositories were accessible. The readme/home source patterns were inspected and fit one *template* but different product-specific primary views. This is an **inventory**, not a claim that nine websites now comply:

| Repo | Primary guide experience | Observed state |
|---|---|---|
| JP_A7_System_Registry_and_Knowledge_Graph | Authority/control navigation and cross-repo standard | New central template |
| JP_Computer-Aided-Drawings | 3D → plan/section → elements → evidence | Has CAD guide; implement this edition |
| JP_Communication-Command-Centre-and-Resource-Hub | Start / Daily Operations → project → work evidence | 1/3/7/15-depth guide already exists |
| JP_Scheduling_Work_and_Resources_Management | Roadmap → milestones → tasks → blockers | Current root has mapping/demo, not unified guide |
| JP_Cost_Estimation | Plain-language scope → quantities/rates → BOQ/cost | Consumer/demo and research branches differ |
| JP_Structural_Analysis | Model → assumptions → result → validation/holds | Main is limited public benchmark; engine on separate branch |
| JP_Research-and-Development | Enterprise/Academic families → AI-driven work → results | Existing AI-first contract, three-entry portal |
| JP_Study_Hub | Subject → study plan → next task → verified learning source | Repository primarily source/data |
| sumita-pilates-studio | Schedule/membership → owner/member task | Non-A7 peer prototype; no forced AEC ownership |

**Rollout status:** central A7 and CAD adoption in this change; other seven remain unchanged pending their own owner/version/CI checks. Do not bulk-rewrite specialist sites or replace their existing menus/URLs.

## Governance, adoption and regression

The machine-readable adoption registry [here](../registry/decisions/ai-aided-guide-adoption.v0.1.json) distinguishes **reviewed**, **implemented**, and **validated** states. Site templates are *views* of this shared standard; domain-specific source and approval rules always take precedence. Change the policy with a reviewed GitHub PR; never edit only a webpage to change a rule. CI checks the policy/schema/template/site markers. Read back main and Pages after merge; preserve old links. R&D's separate Git/Drive policy does not require routine private A9 sequence writes for every Git-only change. Other module-specific A9 obligations remain with their owning authority.
