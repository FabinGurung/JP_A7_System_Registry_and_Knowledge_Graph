# A7 Phase 7 — Cross-Repository Module Manifest Contract

## Purpose

Each bound module repository exposes one root file: `A7_MODULE.json`.

The file is intentionally small. It tells an AI:

- which permanent A7 module/repository identity it is inside;
- where the central ownership and authority contract lives;
- which ref is the current working/publication source;
- which real paths are useful entrypoints for that module;
- which resolver rules must be applied before a mutation.

It does not store domain facts.

## Canonical resolution

```text
A7_BOOTSTRAP.json
  -> registry/entities/modules.json
  -> <owning repository>/A7_MODULE.json
  -> registry/authority/module-ownership.json
  -> registry/authority/authority-map.json
  -> exact live ref/path
  -> domain mutation in owning system
  -> provider readback
```

## Anti-monolith rule

The root manifest does not make A7 the owner of Scheduling, Cost, Structural, CAD, Operations, R&D or Study data. It is a routing doorway.

## Deployment

Seven manifests were installed through repository-local PRE snapshot -> feature branch -> PR -> merge -> provider readback -> POST snapshot. R&D also required its repository payload manifest to be regenerated; its third corrected validation attempt passed.
