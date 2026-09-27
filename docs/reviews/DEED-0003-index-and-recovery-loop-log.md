# DEED-0003 — cold-eyes loop log

The review record for `docs/specs/DEED-0003-index-and-recovery.md`.

## Cold-eyes loop log

| Loop | Date | Lanes | Q1 | Q2 | Q3 | Q4 | Outcome |
|------|------|-------|----|----|----|----|---------|
| 1 | 2026-09-27 | 2 (`review-lane`; every lane held every question) | 0 | 3 | 3 | 1 | Verified 7 / fixed 7 / dismissed 0. Both lanes, merged: no reconcile row for a metadata file behind the index (Q2); first-match order let a missing `.m` row hide a missing `.c`, creating phantom entries (Q2); newer files met only after lock and clean-up had written (Q2, now step 0); save condition ignored a fallback or rebuild (Q3); INV-5's same-process half untested (Q4). One lane: `add`'s clean-up after the index save left an entry with no content (Q3). From open questions: `create` takes the lock, and `update`'s refusal is `ValueError` (Q3). Unrunnable region: Windows and macOS locking, replace and flush. |
