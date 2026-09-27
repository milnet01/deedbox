# Deedbox — Design

> **Purpose — so the shape is decided once, and anyone can tell where a
> new piece of work belongs and what it is allowed to touch.**

**This document is a gate.** Work is not broken into items until it is
agreed — `~/.claude/workflow.md` § 2. It passes when someone can take any
item off the queue and say which part it belongs in and what it may
touch.

**Status:** draft, 2026-09-27 — waiting for the cold review and the
owner's agreement. Built from `docs/discovery.md`; its sign labels (S1–S10)
are cited below.

## The parts

All code lives in the Python package `src/deedbox/`. Tests mirror it under
`tests/`.

| Part | Responsible for | Files |
|---|---|---|
| **crypto** | Turning a password into a key; encrypting and decrypting small blobs and large streams. The only code that touches the encryption library. | `src/deedbox/crypto.py` |
| **vault** | The vault on disk: its folder layout, format version and header, the encrypted document files, and the one atomic-write helper. Opening, closing, adding, reading, removing. | `src/deedbox/vault/layout.py`, `vault/documents.py`, `vault/atomic.py`, `vault/vault.py` |
| **index** | The encrypted catalogue: each document's metadata and extracted text, saving it safely with the previous copy kept, and rebuilding it from the documents. | `src/deedbox/vault/index.py`, `vault/rebuild.py` |
| **migrate** | Upgrading a vault written by an older release to the current format (S9). | `src/deedbox/vault/migrate.py` |
| **search** | Answering a query from the loaded index (S3). | `src/deedbox/search.py` |
| **expiry** | Deciding what is upcoming and what has already expired (S4). Pure date logic. | `src/deedbox/expiry.py` |
| **extract** | Getting text out of a document: the free path for PDFs that already contain text, and OCR for scans (S3). Runs off the main thread. | `src/deedbox/extract/pdftext.py`, `extract/ocr.py` |
| **suggest** | Proposing a title, category and date from a filename and extracted text. Suggests only; never files. | `src/deedbox/suggest.py` |
| **export** | The only code that writes readable plaintext to disk: one document, or the whole vault (S7). | `src/deedbox/export.py` |
| **errors** | The shared error types every part raises. | `src/deedbox/errors.py` |
| **ui** | Every window, dialog and the in-window document viewer. The only code that imports Qt. | `src/deedbox/ui/` — one file per window or dialog |
| **app** | Start-up: builds the Qt application, opens the first window, runs the launch-time expiry check. | `src/deedbox/__main__.py` |

**Where the index lives** is inside `vault/` because it shares the
atomic-write helper and the vault's key, and changes whenever the vault's
format does. It is still its own part: nothing outside `vault/` reads its
file layout.

## What may depend on what

The rules, strongest first. A test can check each by reading imports.

1. **Only `ui` and `app` import Qt.** Everything else runs and is tested
   without a display. This keeps the vault logic checkable on all three
   systems in plain automated tests.
2. **Only `crypto` imports the encryption library.** Nothing else sees a
   cipher, a nonce or a key-derivation setting.
3. **Only `vault` calls `crypto`**, and only `vault` reads or writes files
   inside the vault folder. Every other part gets documents and the index
   through the `Vault` object in `vault/vault.py`.
4. **Only `export` writes decrypted content to disk**, and only when the
   user asked for an export. No part writes a decrypted temporary file,
   ever — not for viewing, not for OCR, not for printing.
5. **`search`, `expiry` and `suggest` are pure.** They take data in and
   return answers. No disk, no network, no Qt, no clock of their own —
   today's date is passed in.
6. **`extract` takes document bytes and returns text.** It never opens a
   vault file. OCR hands image bytes to the OCR tool through a pipe.
7. **No part opens a network connection.** Deedbox has no network code
   at all (discovery: nothing leaves the machine).
8. **`ui` may call** `vault`, `search`, `expiry`, `suggest`, `extract` and
   `export`. **It may not call** `crypto`, and it may not build a path
   inside the vault folder.
9. **Nothing depends on `ui` or `app`.**

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
- **Names on disk.** Document files are named by random ids. No title,
  date, category or original filename appears in any name (S5).
- **Format version.** The vault header carries a format number from the
  first release. Opening a vault runs `migrate` first; a vault newer than
  the app is refused with a clear message, never guessed at (S9).
- **Logging.** Python's standard `logging`, to a local file only. A log
  line never contains a document's content, title, tags, note, extracted
  text, search query or the password.
- **Dates.** Calendar dates without times, stored as ISO text
  (`2026-09-27`). Compared in the user's local day.
- **Background work.** OCR and text extraction run in worker threads and
  report back to `ui` through Qt signals. Filing a document never waits
  for them.

## The stack, and what it rules out

| Choice | Why | Runner-up |
|---|---|---|
| **Python 3.12 or newer** | The owner's choice; shared with Rolodex and finbreak. 3.10 leaves security support in October 2026. [ADR-0002](decisions/ADR-0002-python.md) | C++ |
| **PySide6** (Qt for Python) | Qt's official Python binding. `QtPdf` shows a PDF from memory with no temporary file — checked 2026-09-27 by loading a PDF from an in-memory buffer. LGPL, compatible with GPL-3.0. | PyQt6 |
| **PyNaCl** (libsodium) | Argon2id key derivation and a documented recipe for encrypting large files in pieces, from one well-known library. [ADR-0001](decisions/ADR-0001-crypto-library.md) | `cryptography` |
| **pypdf** | Reads the text already inside digital PDFs without Qt, so `extract` stays testable headless. | Qt's own PDF text extraction |
| **Tesseract** for OCR | The standard free OCR engine; Apache-2.0, so installers may bundle it. Missing → search covers typed fields only. | none considered |
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
