# DEED-0002 — cold-eyes loop log

The review record for `docs/specs/DEED-0002-vault-format.md`.

## Cold-eyes loop log

| Loop | Date | Lanes | Q1 | Q2 | Q3 | Q4 | Outcome |
|------|------|-------|----|----|----|----|---------|
| 1 | 2026-09-27 | 2 (`review-lane`; every lane held every question) | 1 | 3 | 5 | 1 | Verified 10 / fixed 10 / dismissed 0. Both lanes: INV-5's role case rejected by the magic before the associated data (Q4); the `key` role's format number unstated (Q3). Q2: `create`'s signature vs the settings sentence; `unlock`'s WrongPassword vs a parse failure; "MemoryError" vs what PyNaCl raises — re-run with memory capped: `nacl.exceptions.RuntimeError`, now `NotEnoughMemory`. Q3: last-piece rule gave two layouts; newer file prefix → VaultTooNew; temp-file name; base64 variant. Q1: "no document half-exists" was false when the `.m` write fails. Four came from lanes' open questions. Unrunnable region declared: Windows and macOS. |
