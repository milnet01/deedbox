# DEED-0003 — cold-eyes loop log

The review record for `docs/specs/DEED-0003-index-and-recovery.md`.

## Cold-eyes loop log

| Loop | Date | Lanes | Q1 | Q2 | Q3 | Q4 | Outcome |
|------|------|-------|----|----|----|----|---------|
| 1 | 2026-09-27 | 2 (`review-lane`; every lane held every question) | 0 | 3 | 3 | 1 | Verified 7 / fixed 7 / dismissed 0. Both lanes, merged: no reconcile row for a metadata file behind the index (Q2); first-match order let a missing `.m` row hide a missing `.c`, creating phantom entries (Q2); newer files met only after lock and clean-up had written (Q2, now step 0); save condition ignored a fallback or rebuild (Q3); INV-5's same-process half untested (Q4). One lane: `add`'s clean-up after the index save left an entry with no content (Q3). From open questions: `create` takes the lock, and `update`'s refusal is `ValueError` (Q3). Unrunnable region: Windows and macOS locking, replace and flush. |
| 2 | 2026-09-27 | 2 (`review-lane`; every lane held every question) | 1 | 2 | 3 | 1 | Verified 7 / fixed 7 / dismissed 1. Both lanes: a save after a fallback copied the corrupt `index` over the good `index.prev` (Q2, now skipped). One lane: the kill test was timing luck (Q4, now tied to printed progress and required to catch a mid-write state). From open questions: macOS `fsync` does not empty the drive cache (Q1, now `F_FULLFSYNC` where present, directory flush best effort); a removed `.m` could reappear after a power cut (Q3, `atomic.delete`); step 0's wrong-magic pointer named the wrong step (Q2); an equal `edit` matched no row (Q3); Windows sharing between a refused opener and the holder's save recorded as deferred (Q3). Dismissed: §8's rationale against §13 — rewritten anyway, changes nothing built. **Cap reached (spec cap 2) — ship; nothing filed beyond § 9.** Final-loop own-fix share unreadable: the armed change was the whole document; by substance, completions of loop-1 repairs. |
