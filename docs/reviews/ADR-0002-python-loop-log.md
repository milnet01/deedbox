# ADR-0002 — cold-eyes loop log

The review record for `docs/decisions/ADR-0002-python.md`, kept here
because an ADR carries no loop log of its own.

| Loop | Date | Lanes | Q1 | Q2 | Q3 | Q4 | Outcome |
|------|------|-------|----|----|----|----|---------|
| 1 | 2026-09-27 | 2 (`review-lane`; every lane held every question) | 0 | 1 | 1 | — | Verified 2 / fixed 2 / dismissed 2. Both lanes found the Linux packaging conflict with design.md (merged). Q3: no Python range recorded though design.md cites this ADR for it. Dismissed: "Qt already decided (brief)" — the brief's decided banner does say so; "Rolodex is Qt" — Rolodex is GTK 4, checked in its requirements.txt. |
| 2 | 2026-09-27 | 2 (`review-lane`; every lane held every question) | 0 | 1 | 0 | — | Verified 1 / fixed 1 / dismissed 1. One lane found design.md's open-ended "3.12 or newer" against the ADR's PySide6 ceiling; the other raised it as an open question. Both bounds now stated in the ADR and design.md's stack row. Dismissed again: the "Qt already decided" citation (the brief's decided banner says so). |
