# DEED-0004 — cold-eyes loop log

The review record for `docs/specs/DEED-0004-format-migration.md`.

## Cold-eyes loop log

| Loop | Date | Lanes | Q1 | Q2 | Q3 | Q4 | Outcome |
|------|------|-------|----|----|----|----|---------|
| 1 | 2026-09-28 | 2 (`review-lane`; every lane held every question) | 0 | 1 | 1 | 3 | Verified 5 / fixed 5 / dismissed 0. Both lanes: a bump with no header step had no stated outcome (Q3; a missing header step now leaves the header as it is, a missing file step raises); § 6 said a file a step cannot read is reported as damaged while § 4.3 left a content file silent (Q2; such a content file's id now goes to `damaged()`, and § 6 points at § 4.3); INV-3 could not catch a skipped `index`, since the open falls back to `index.prev` and saves a fresh one (Q4; the test step now records the paths it was called with). One lane, one open question: INV-5 did not raise `VAULT_FORMAT`, so its step could never run (Q4). From both lanes' open questions: the hash list inside the fixture folder would list itself (Q4; now beside the folder). Packet carried the changed code whole; both lanes read no code outside it. Unrunnable region: Windows and macOS. |
