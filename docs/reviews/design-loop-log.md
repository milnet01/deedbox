# Design — cold-eyes loop log

The review record for `docs/design.md`.

## Cold-eyes loop log

| Loop | Date | Lanes | Q1 | Q2 | Q3 | Q4 | Outcome |
|------|------|-------|----|----|----|----|---------|
| 1 | 2026-09-27 | 2 (`review-lane`; every lane held every question) | 0 | 4 | 6 | — | Verified 10 / fixed 10 / dismissed 1. Both lanes found 6 of the 10; two came from resolving lanes' open questions (log location, visible file sizes and times). Dismissed: "Python 3.12 shared with Rolodex" — names the shared language, changes nothing built. Unrunnable region declared: Windows and macOS behaviour. |
| 2 | 2026-09-27 | 2 (`review-lane`; every lane held every question) | 0 | 2 | 3 | — | Verified 5 / fixed 5 / dismissed 3. Both lanes found the rebuild-needs-extract contradiction (merged). Two came from open questions (the Tesseract-pipe fallback; which encryption the metadata files use). 4 of 5 landed on loop-1 text. Dismissed: the workflow § 2 citation (correct, § 2 is the gates); Python version shared with Rolodex; no Python upper bound (PySide6's own requirement enforces it). |
| 3 | 2026-09-27 | 2 (`review-lane`; every lane held every question) | 0 | 0 | 6 | — | Verified 6 / fixed 6 / dismissed 1. Both lanes found the backup-index recovery deleting filed documents (merged). Two came from open questions (migrate-before-recovery order; export into the vault folder). Dismissed: no Python upper bound (PySide6's own requirement enforces it). **Cap reached — ship.** Final-loop own-fix share 5 of 6, but unreadable: the armed change was the whole document. By substance these are unpropagated consequences of loop 1's metadata-file decision, all in storage recovery, not repairs of repairs. No second share: the span is the whole document. Routed: storage format and recovery get a spec before build step 1. |
