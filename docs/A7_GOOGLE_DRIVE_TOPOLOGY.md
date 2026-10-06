# A7 Phase 4 — Google Drive / Kaksaveksaka A9 Topology Metadata

## Architectural decision

Google Drive remains the authority for Drive-native object identity, private topology, original files and provider revisions. A7 is the semantic routing/control layer.

The existing `Fabin_Gurung_Drive_Index` contains 968 rows whose Current Path is under the A9 root. Those rows include private/access-governed metadata and have mixed row-level scan freshness. Because the A7 repository is public, Phase 4 deliberately does not bulk-copy those 968 records.

Instead A7 stores a safe bootstrap graph, the stable IDs of governance anchors, aggregate coverage/freshness, public-safety boundaries and deterministic lookup rules.

## Current A9 root

Live provider scan on 2026-10-06 observed 16 top-level branches. Fifteen are represented by safe semantic names and stable provider IDs. One private/sensitive branch is represented only as a redacted boundary node.

## Detailed lookup algorithm

1. Resolve an A7 Google Drive node or semantic role.
2. Use a stored governance anchor directly where applicable.
3. For detailed A9 topology, query `Fabin_Gurung_Drive_Index` / `Index` by stable Drive ID, current/legacy path or governed label.
4. Prefer stable Drive ID over name/path.
5. If the operation depends on current state, read the exact provider object/parent live.
6. Do not infer current state from an old Last Scanned At value.
7. Do not copy private file content/private path inventories into public A7.
8. A Drive mutation requires provider read-before/write/readback.

## Coverage evidence

- Drive Index data rows scanned: 1293.
- Rows currently indexed under the A9 root path: 968.
- Live root top-level branches: 16.
- `00_DRIVE_CONTROL_CENTER` direct listing reached the connector's 100-child limit, so its current child count is at least 100 and must not be inferred as exactly 100.
- Historical index rows still contain four records under legacy `07_Finance_Procurement`; the live A9 root does not expose that top-level folder.

## Privacy

A7 is public. The private/sensitive branch provider ID and descendants are intentionally not committed. Detailed private topology stays in Drive and requires authorized live access.

## Why this is more normalized than a bulk copy

The machine needs a stable resolver, not another duplicate warehouse. A7 defines what the Drive entities mean, which anchors to query and how to verify freshness. Drive keeps the actual topology and files. This avoids a second editable master.
