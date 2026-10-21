# A7 artifact lineage contract v0.1 — owner-bound, zero duplicate imports

**A7-SEQ-000025 / DEBT CLEARANCE (not a Galactic Arc).** Contract: `registry/contracts/source-artifact-lineage.v0.1.json`. Real provider sample: `registry/lineage/public-pages-release.example.json`. Validator: `scripts/validate_artifact_lineage_contract.py`.

## Data and governance contract

The narrow pathway is: **owning Git repo ID + exact branch/commit + source path → build validation/run → publication/compiled artifact digest and provider identity → owner-controlled Drive file/revision (when one exists) → private Local/Main registration and acknowledged consumed cursor (when actually admitted) → public-safe A7 metadata projection**.

Source roles must not be collapsed. A commit is a Git object ID and is NOT an arbitrary file SHA-256. A Pages artifact's archive SHA-256 is a separate provider checksum. A native Drive file ID is a stable provider pointer; the revision and signed/source state must be verified by its original owner. An A7 website is a read model and never admission for a scientific report.

## Public example and exclusions

The included example is the **actual** final A7 Arc05 GitHub Pages release at commit `e0face993127f121220c564e874c03fdce4dcb5c`: Registry CI 39593936542 passed, Pages run 39593936610 passed, actual Pages artifact 12342599596 had provider digest `6f7ae529d3958a080b5ee04d6f01c96c2565827535957818437abb2b15beb9d6`. Its Google Drive mapping is **null**, because no Drive artifact or A9 Main ACK was produced. `release_tag: null` prevents making a false tag claim.

In a **private owner domain**, a completed PDF/DOCX/PPTX may carry a source tree/commit/path reference, an owner-approved build QA, its exact Drive ID and provider revision, and eventually a Local/Main ACK if supported by true evidence. No private Drive reference or scientific admission travels into public A7 Git by default.

## Private bridge and historic debts

The separately saved A9 parity audit is stored in private Google Drive, not cross-linked with a private Drive ID in this repository. It distinguishes already-closed **A9 Portable Canon v1 SEQ13 (Root11 13/13)** from **A7-SEQ-000013 public-safe Git/Drive transition**, which remains staged as a private migration. The live Main Library has not admitted the nine October 9 dry-run candidates. Do not manufacture a Local sequence, replay historic candidate writes, or let a new Git commit increment any A9 consumed cursor automatically.

## Admission checklist

1. Verify live source/release SHA and correct owner; recheck branch HEAD where current HEAD is material.
2. Link build CI and deployment to exact observed source commit, with recorded immutable run identifiers and provider digests.
3. For a Drive result, verify original content, correct file/provider revision and readback in the owning **private** project.
4. Check preexisting canonical identities, FK relationships, historic cursor/ACK and source visibility before an approved private registration.
5. Never clone full Git commit history into Main; record meaningful output/release boundaries only.
6. Only expose non-confidential, explicitly owned projections; mark stale observations and unverified dependencies honestly.

## Validation and scope

`python scripts/validate_artifact_lineage_contract.py` runs in A7 source CI and GitHub Pages build gate. The contract is completed independently of A9 private parity, R&D scientific admission, any external human signoff and optional whole-network bootstrap drift checking. No new Arc has been begun.

## Provider source-release acceptance

A7-SEQ-000025 implementation PR #55 merged at `df18c7266b24ab5f98899a21a2893e356f236ecf`; main Registry CI 39624448190 and Pages 39624448234 both SUCCESS; PR real Chromium browser 39624257598 SUCCESS. Final public release contract was tested without private Drive reads/writes in GitHub Actions. Remaining A9 historical import/ACK and scientific owner gate NOT closed.
