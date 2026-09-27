# Deedbox — Design

> **Purpose — so the shape is decided once, and anyone can tell where a
> new piece of work belongs and what it is allowed to touch.**

**This document is a gate.** Work is not broken into items until it is
agreed — `~/.claude/workflow.md` § 2. It passes when someone can take any
item off the queue and say which part it belongs in and what it may
touch.

**Status:** reviewed 2026-09-27 (`review-contract`, three loops, capped)
— waiting for the owner's agreement. Built from `docs/discovery.md`;
its sign labels (S1–S10) are cited below.

## The parts

All code lives in the Python package `src/deedbox/`. Tests mirror it under
`tests/`.

| Part | Responsible for | Files |
|---|---|---|
| **crypto** | Turning a password into a key; encrypting document content as a stream (secretstream) and the index and metadata files as single messages. The only code that touches the encryption library. | `src/deedbox/crypto.py` |
| **vault** | The vault on disk: its folder layout, format version and header, the encrypted document files, and the one atomic-write helper. Opening, closing, adding, reading, removing. | `src/deedbox/vault/layout.py`, `vault/documents.py`, `vault/atomic.py`, `vault/vault.py` |
| **index** | The encrypted catalogue: each document's metadata and extracted text, saving it safely with the previous copy kept, and rebuilding it from the documents' metadata files. | `src/deedbox/vault/index.py`, `vault/rebuild.py` |
| **migrate** | Upgrading a vault written by an older release to the current format (S9). | `src/deedbox/vault/migrate.py` |
| **search** | Answering a query from the loaded index (S3). | `src/deedbox/search.py` |
| **expiry** | Deciding what is upcoming and what has already expired (S4). Pure date logic. | `src/deedbox/expiry.py` |
| **extract** | Getting text out of a document: the free path for PDFs that already contain text, and OCR for scans (S3), rendering scanned PDF pages to images in memory first. Plain and synchronous; `ui` runs it in a worker thread. | `src/deedbox/extract/pdftext.py`, `extract/ocr.py` |
| **suggest** | Proposing a title, category and date from a filename and extracted text. Suggests only; never files. | `src/deedbox/suggest.py` |
| **export** | The only code that writes readable plaintext to disk: one document, or the whole vault (S7). | `src/deedbox/export.py` |
| **errors** | The shared error types every part raises. | `src/deedbox/errors.py` |
| **ui** | Every window, dialog and the in-window document viewer, and the worker threads for extraction. Runs the expiry check when the main window opens. | `src/deedbox/ui/` — one file per window or dialog |
| **app** | Start-up: builds the Qt application and opens the first window. | `src/deedbox/__main__.py` |

**`vault` in the rules below means the whole `src/deedbox/vault/`
package** — vault, index and migrate. They share the atomic-write helper
and the key, and change whenever the format does. Nothing outside the
package reads the index's file layout.

## What may depend on what

The rules, strongest first. A test can check each by reading imports.

1. **Only `ui` and `app` import Qt.** Everything else runs and is tested
   without a display. This keeps the vault logic checkable on all three
   systems in plain automated tests.
2. **Only `crypto` imports the encryption library and interprets its
   settings.** `crypto` hands `vault` a key-derivation record — the
   Argon2id settings and salt as one byte string — and `vault` stores it
   in the header without reading it.
3. **Only `vault` calls `crypto`**, and only `vault` reads or writes files
   inside the vault folder. Every other part gets documents and the index
   through the `Vault` object in `vault/vault.py`.
4. **Only `export` writes decrypted content to disk**, and only when the
   user asked for an export, and never to a place inside the vault
   folder. No part writes a decrypted temporary file,
   ever — not for viewing, not for OCR, not for printing.
5. **`search`, `expiry` and `suggest` are pure.** They take data in and
   return answers. No disk, no network, no Qt, no clock of their own —
   today's date is passed in.
6. **`extract` takes document bytes and returns text.** It never opens a
   vault file and holds no thread or Qt signal. Scanned PDF pages become
   images in memory; OCR hands those image bytes to the OCR tool through
   a pipe.
7. **No part opens a network connection.** Deedbox has no network code
   at all (discovery: nothing leaves the machine).
8. **`ui` may call** `vault`, `search`, `expiry`, `suggest`, `extract` and
   `export`. **It may not call** `crypto`, and it may not build a path
   inside the vault folder.
9. **Nothing depends on `ui` or `app`.** Every part may import `errors`.

```
app ─► ui ─► vault ─► crypto
        │      └────► errors
        ├─► search, expiry, suggest   (pure)
        ├─► extract
        └─► export ─► vault
```

## What every part does the same way

- **Errors.** Every expected failure is one of the types in
  `errors.py` — wrong password, vault damaged, vault from a newer
  release, document missing, export target not writable. `ui` turns each
  into one plain-English message. Nothing catches an error and carries
  on silently.
- **State.** An open vault is one `Vault` object. The key exists only in
  that object's memory while the vault is open, and is dropped on close.
  Decrypted documents live in memory only while shown.
- **Saving.** Every write into the vault folder goes through
  `vault/atomic.py`: write to a new file, flush it to disk, then replace
  the old one in one step (S8). The index keeps its previous copy. The
  recipe is tested on Windows, macOS and Linux, because replacing a file
  behaves differently on Windows.
- **Which copy wins.** The index is the truth; each metadata file is its
  document's recovery copy, carrying an edit counter the index also
  records. Adding writes content, then index, then metadata file.
  Editing writes index, then metadata file. Removing deletes the metadata
  file, then writes the index, then deletes the content file.
- **Opening, in order.** Run `migrate`. Load the index; if it will not
  decrypt, load its previous copy; if neither will, rebuild from the
  metadata files. Then reconcile against the files on disk:
  - a metadata file ahead of the index, or not listed in it, updates the
    index;
  - an index entry whose metadata file is behind or missing has that file
    rewritten from the index;
  - a content file with neither an index entry nor a metadata file is
    left from an unfinished add or remove, and is deleted.
- **Names on disk.** Each document is two encrypted files sharing one
  random id: its content, and a small metadata file holding its title,
  category, tags, note, dates, original filename, file type, extracted
  text and extraction status (not yet run, done, or no OCR tool).
  Editing metadata rewrites only the small file and the index.
  Rebuilding the index reads the metadata files alone; nothing is
  re-extracted. No title, date, category or original filename appears
  in any name (S5).
- **Format version.** The vault header and every file in the vault
  carry a format number from the first release. Opening a vault runs
  `migrate` first. It rewrites one file at a time through
  `vault/atomic.py` and updates the header's number last, so an
  interrupted migration resumes on the next open. A vault or file newer
  than the app is refused with a clear message, never guessed at (S9).
- **Logging.** Python's standard `logging`, to a file in the user's
  app-data folder — never inside the vault folder. A log
  line never contains a document's content, title, tags, note, extracted
  text, search query or the password.
- **Dates.** Calendar dates without times, stored as ISO text
  (`2026-09-27`). Compared in the user's local day.
- **Background work.** OCR and text extraction run in worker threads
  that `ui` owns, and report back through Qt signals. When a vault opens,
  `ui` queues every document whose extraction has not run, and those
  marked no OCR tool once the tool is present. Filing a document never waits
  for them.

## The stack, and what it rules out

| Choice | Why | Runner-up |
|---|---|---|
| **Python 3.12 or newer** | The owner's choice; shared with Rolodex and finbreak. 3.10 leaves security support in October 2026. [ADR-0002](decisions/ADR-0002-python.md) | C++ |
| **PySide6** (Qt for Python) | Qt's official Python binding. `QtPdf` shows a PDF from memory with no temporary file — checked 2026-09-27 by loading a PDF from an in-memory buffer. LGPL, compatible with GPL-3.0. | PyQt6 |
| **PyNaCl** (libsodium) | Argon2id key derivation and a documented recipe for encrypting large files in pieces, from one well-known library. [ADR-0001](decisions/ADR-0001-crypto-library.md) | `cryptography` |
| **pypdf** | Reads the text already inside digital PDFs without Qt, so `extract` stays testable headless. | Qt's own PDF text extraction |
| **pypdfium2** + **Pillow** | Render a scanned PDF page to image bytes in memory, without Qt — checked 2026-09-27 by rendering a page from bytes to PNG bytes. BSD-3-Clause / Apache-2.0, and MIT-CMU. | pypdf's embedded-image extraction |
| **Tesseract** for OCR | The standard free OCR engine; Apache-2.0. All three installers bundle it — the Flatpak too, because a sandboxed app cannot run a copy installed on the computer. Missing → search covers typed fields only. Reading images from a pipe is confirmed at the OCR step, before OCR is built; not checked here. If it needs a temporary file, OCR goes back to design rather than breaking rule 4. | none considered |
| **pytest** + **ruff** | The Python standard's tooling. | — |
| **PyInstaller** for Windows and macOS, **Flatpak** for Linux | Rolodex already builds with PyInstaller on all three systems; Flathub is Linux's app store. | Briefcase |
| **GitHub Actions** on Windows, macOS and Linux | Every push runs the tests on all three. | — |

**What it rules out:**

- **No web interface and no local server.** Nothing listens on a port.
- **No outside PDF viewer.** Viewing happens in Deedbox's window.
- **No reliable wiping of memory.** Python cannot guarantee a decrypted
  document is erased from memory after use. The protection is for the
  vault at rest (S5), not against someone already running code on the
  unlocked machine. Help text will say so plainly.
- **No hiding of sizes and times.** Anyone holding the vault folder can see
  roughly how many documents it holds, how large each is, and when each
  was last written. S5's opaque dates are the documents' own dates, which
  live only inside encrypted files.
- **A large installer.** Python plus Qt makes a bigger download than a
  C++ app.
- **Formats Qt cannot show.** v1 shows PDFs and common image types only;
  anything else can be stored and exported but not previewed.

## Close calls

- [ADR-0001 — PyNaCl for the encryption](decisions/ADR-0001-crypto-library.md)
- [ADR-0002 — Python, not C++](decisions/ADR-0002-python.md)

## Cold-eyes loop log

> A design doc is gated (`documentation.md` § 9.1) and is owed no
> `## What checks this` table, so the log goes last. `review-contract`
> writes a row per loop as the loops happen; never back-fill one.

| Loop | Date | Lanes | Q1 | Q2 | Q3 | Q4 | Outcome |
|------|------|-------|----|----|----|----|---------|
| 1 | 2026-09-27 | 2 (`review-lane`; every lane held every question) | 0 | 4 | 6 | — | Verified 10 / fixed 10 / dismissed 1. Both lanes found 6 of the 10; two came from resolving lanes' open questions (log location, visible file sizes and times). Dismissed: "Python 3.12 shared with Rolodex" — names the shared language, changes nothing built. Unrunnable region declared: Windows and macOS behaviour. |
| 2 | 2026-09-27 | 2 (`review-lane`; every lane held every question) | 0 | 2 | 3 | — | Verified 5 / fixed 5 / dismissed 3. Both lanes found the rebuild-needs-extract contradiction (merged). Two came from open questions (the Tesseract-pipe fallback; which encryption the metadata files use). 4 of 5 landed on loop-1 text. Dismissed: the workflow § 2 citation (correct, § 2 is the gates); Python version shared with Rolodex; no Python upper bound (PySide6's own requirement enforces it). |
| 3 | 2026-09-27 | 2 (`review-lane`; every lane held every question) | 0 | 0 | 6 | — | Verified 6 / fixed 6 / dismissed 1. Both lanes found the backup-index recovery deleting filed documents (merged). Two came from open questions (migrate-before-recovery order; export into the vault folder). Dismissed: no Python upper bound (PySide6's own requirement enforces it). **Cap reached — ship.** Final-loop own-fix share 5 of 6, but unreadable: the armed change was the whole document. By substance these are unpropagated consequences of loop 1's metadata-file decision, all in storage recovery, not repairs of repairs. No second share: the span is the whole document. Routed: storage format and recovery get a spec before build step 1. |
