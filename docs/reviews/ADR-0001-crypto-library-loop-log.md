# ADR-0001 — cold-eyes loop log

The review record for `docs/decisions/ADR-0001-crypto-library.md`, kept
here because an ADR carries no loop log of its own.

| Loop | Date | Lanes | Q1 | Q2 | Q3 | Q4 | Outcome |
|------|------|-------|----|----|----|----|---------|
| 1 | 2026-09-27 | 2 (`review-lane`; every lane held every question) | 1 | 1 | 2 | — | Verified 4 / fixed 4 / dismissed 2. Both lanes found the metadata-file cipher conflict with design.md and the missing key hierarchy (merged). Q1 (secretstream does not flag a cut-off file) re-run with PyNaCl: confirmed. One Q3 came from an open question (pin the single-message construction so a replacement binding can read it). Dismissed: the "build step 1" citation; PyNaCl wheels per Python version (abi3 wheels). Key hierarchy written back into design.md rule 2. |
