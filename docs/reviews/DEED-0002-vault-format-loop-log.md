# DEED-0002 — cold-eyes loop log

The review record for `docs/specs/DEED-0002-vault-format.md`.

## Cold-eyes loop log

| Loop | Date | Lanes | Q1 | Q2 | Q3 | Q4 | Outcome |
|------|------|-------|----|----|----|----|---------|
| 1 | 2026-09-27 | 2 (`review-lane`; every lane held every question) | 1 | 3 | 5 | 1 | Verified 10 / fixed 10 / dismissed 0. Both lanes: INV-5's role case rejected by the magic before the associated data (Q4); the `key` role's format number unstated (Q3). Q2: `create`'s signature vs the settings sentence; `unlock`'s WrongPassword vs a parse failure; "MemoryError" vs what PyNaCl raises — re-run with memory capped: `nacl.exceptions.RuntimeError`, now `NotEnoughMemory`. Q3: last-piece rule gave two layouts; newer file prefix → VaultTooNew; temp-file name; base64 variant. Q1: "no document half-exists" was false when the `.m` write fails. Four came from lanes' open questions. Unrunnable region declared: Windows and macOS. |
| 2 | 2026-09-27 | 2 (`review-lane`; every lane held every question) | 0 | 1 | 3 | 2 | Verified 6 / fixed 6 / dismissed 0. Both lanes, merged: the role-binding test paired `metadata` with `index`, which also differ in id (Q4); INV-8's test did not check "changes nothing on disk" (Q4); the key record's version was stored nowhere (Q3). From open questions: bounds on the untrusted key record's settings (Q3); `atomic.py` is created here, not only used (Q2); the index write's place in `add` belongs to DEED-0003 (Q3). **Cap reached (spec cap 2) — ship; nothing filed.** Final-loop own-fix share 3 of 6, but unreadable: the armed change was the whole document. By substance, loop-1 repairs completed rather than repairs of repairs. No second share: the span is the whole document. |
