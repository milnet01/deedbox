<!-- ants-roadmap-format: 1 -->
# Deedbox — Roadmap

> What is planned, in progress and shipped. [CHANGELOG.md](CHANGELOG.md)
> is the user-facing record of what shipped; released items stay here and
> flip to ✅.
>
> **Format:** `~/.claude/standards/roadmap-format.md`. Theme emojis
> (§ 3.4), priority bands (§ 3.5.2) and the full bullet field set (§ 3.5)
> are defined there and deliberately not restated here.

**Legend**

- ✅ Done · 🚧 In progress · 📋 Planned · 💭 Considered

## 0.1.0 — (first release)

The first public release, on Windows, macOS and Linux. Items follow the
build order in `docs/brief.md` and the parts in `docs/design.md`. Signs
of success are cited by their `docs/discovery.md` labels, S1 to S10.

- ✅ [DEED-0001] **Project tooling: package layout, lint, tests, CI on three systems.**
  `pyproject.toml` with Python 3.12 up to the pinned PySide6's ceiling,
  ruff, pytest, and `scripts/local-ci.sh` called by `ci.yml` on
  Windows, macOS and Linux runners. Includes the import-rule test that
  enforces `docs/design.md` § What may depend on what.
  **Layman:** Sets up the automatic checks that run on Windows, macOS and Linux every time the code changes.
  Kind: chore.
  Lanes: tooling.
  Source: design-2026-09-27.
  Shipped 2026-09-27 (198d608): local gate green on Linux. The Windows
  and macOS CI legs have not run yet — no remote until DEED-0015 — so
  the first push is their first real run.

- ✅ [DEED-0002] **Vault core: create, lock, unlock, add and read a document.**
  Build step 1 of `docs/brief.md`. Needs a spec first — the vault-format
  spec that ADR-0001 and `docs/design.md` defer to (key record, piece
  size, associated-data encoding, file layout). Serves S5 and S6. Done
  when a test creates a vault, adds a file, reopens it and reads it back
  byte-identical on all three systems, and a wrong password fails
  cleanly.
  Overlaps DEED-0003 and DEED-0004: all three edit `src/deedbox/vault/`.
  Run them in order, not together.
  Blocked-by: DEED-0001
  **Layman:** The locked drawer itself: make a vault with a password, put a file in, and get exactly the same file back.
  Kind: implement.
  Lanes: crypto, vault.
  Source: design-2026-09-27.
  Spec accepted 2026-09-27: `docs/specs/DEED-0002-vault-format.md`.
  Shipped 2026-09-27 (cd8e739): round trip, wrong password, nothing
  readable, truncation, binding and too-new all locked by tests, each
  proven red by a deliberate break. Linux only so far; the Windows and
  macOS legs first run when the repository gets a remote (DEED-0015).

- ✅ [DEED-0003] **Index, safe saving and recovery on open.**
  Build step 2. The index, `vault/atomic.py`, the metadata-file recovery
  copies, the open-time order and reconciliation, and rebuild
  (`docs/design.md` § Which copy wins, § Opening, in order). Serves S8.
  Done when a test kills the process mid-write and the vault reopens
  intact.
  Blocked-by: DEED-0002
  **Layman:** Makes sure a power cut or crash never loses a filed document.
  Kind: implement.
  Lanes: vault, index.
  Source: design-2026-09-27.
  Spec accepted 2026-09-27:
  `docs/specs/DEED-0003-index-and-recovery.md`.
  Shipped 2026-09-27 (96513eb): index, recovery on open, lock; INV-1
  to INV-7 locked by tests, each proven red by a deliberate break except
  atomicity, which INV-6 does not isolate (spec § 10). Linux only so far;
  Windows and macOS first run with a remote (DEED-0015).

- 📋 [DEED-0004] **Format versions and the migration framework.**
  Per-file format numbers, a resumable `migrate`, refusal of a vault
  newer than the app, and a checked-in sample vault from the first
  format that every later release must open. Serves S9.
  Blocked-by: DEED-0002
  **Layman:** Makes sure a vault made with an older version always opens in a newer one.
  Kind: implement.
  Lanes: vault, migrate.
  Source: design-2026-09-27.

- 📋 [DEED-0005] **Main window: create or unlock a vault, add, list and view documents.**
  Build step 3. Vault creation says in plain words that a forgotten
  password loses everything (S2). Drag-in adding, a document list, and
  the in-window PDF and image viewer with no decrypted temporary file.
  Blocked-by: DEED-0003
  **Layman:** The window you use: set a password, drag files in, see them listed and open them without leaving the app.
  Kind: implement.
  Lanes: ui, app.
  Source: design-2026-09-27.

- 📋 [DEED-0006] **Filing: category, tags, dates, note, with suggestions.**
  Editing a document's metadata, and `suggest` proposing a title,
  category and date from the filename and text. Suggests only; never
  files on its own.
  Overlaps DEED-0007 and DEED-0008 in the main window's files.
  Blocked-by: DEED-0005
  **Layman:** Lets you label each document, with sensible guesses you can always change.
  Kind: implement.
  Lanes: ui, suggest.
  Source: design-2026-09-27.

- 📋 [DEED-0007] **Search, including text already inside PDFs.**
  `search` over titles, tags, notes and extracted text; `extract`'s free
  path for PDFs that already contain text (pypdf), run in `ui`'s worker
  thread. Serves S3 for typed fields and digital PDFs.
  Blocked-by: DEED-0006
  **Layman:** Find a document by typing anything you remember about it.
  Kind: implement.
  Lanes: search, extract, ui.
  Source: design-2026-09-27.

- 📋 [DEED-0008] **Expiry tracking and the upcoming view.**
  Build step 4. Expiry and renewal dates, an upcoming view, the check
  when the main window opens, and already-expired items marked, not
  hidden. Serves S4. Done when a warranty dated next week shows up and
  one dated last year is flagged.
  Blocked-by: DEED-0006
  **Layman:** Shows what is about to run out as soon as you open the app.
  Kind: implement.
  Lanes: expiry, ui.
  Source: design-2026-09-27.

- 📋 [DEED-0009] **OCR for scans, in the background.**
  Build step 5. First confirm Tesseract reads images from a pipe with no
  temporary file; if not, this goes back to design (`docs/design.md`,
  the stack). pypdfium2 renders scanned pages in memory; extraction
  status is saved and unfinished work resumes on open. Serves S3. Done
  when search finds a model number that only appears inside a scan.
  Blocked-by: DEED-0007
  **Layman:** Lets search find words printed inside scanned documents and photos.
  Kind: implement.
  Lanes: extract, ui.
  Source: design-2026-09-27.

- 📋 [DEED-0010] **Export one document or the whole vault.**
  Original filenames and types, readable without Deedbox, never written
  inside the vault folder. Serves S7.
  Blocked-by: DEED-0005
  **Layman:** Get any document back out as a normal file, or everything at once.
  Kind: implement.
  Lanes: export, ui.
  Source: design-2026-09-27.

- 📋 [DEED-0011] **Owner files real paperwork for a week.**
  Twenty real documents from Downloads, used for a week (`docs/brief.md`,
  build step 3's check). Serves S10. Anything that makes it unpleasant
  becomes an item before packaging.
  Blocked-by: DEED-0005, DEED-0006, DEED-0007, DEED-0008, DEED-0010
  **Layman:** The real test: you use it for your own papers for a week and it earns its place.
  Kind: test.
  Lanes: ui.
  Source: design-2026-09-27.

- 📋 [DEED-0012] **Independent security review of the crypto and vault code.**
  Required before the first public release (`docs/brief.md`, Releasing
  it to the public). Covers ADR-0001's choices and the vault code.
  Blocked-by: DEED-0002, DEED-0003, DEED-0004
  **Layman:** Someone outside checks the lock before strangers trust it with their passports.
  Kind: security.
  Lanes: crypto, vault.
  Source: design-2026-09-27.

- 📋 [DEED-0013] **Help written for non-technical people.**
  Setup, backup by copying the vault folder, the forgotten-password
  warning, what stays visible on disk, and the memory limit
  (`docs/design.md`, What it rules out). Serves S1, S2 and S6.
  Blocked-by: DEED-0005
  **Layman:** Plain-English help on setting up, backing up, and what a forgotten password means.
  Kind: doc.
  Lanes: ui, docs.
  Source: design-2026-09-27.

- 📋 [DEED-0014] **Installers: signed Windows and macOS builds, Flatpak for Linux.**
  Build step 6. PyInstaller for Windows and macOS, Flatpak for Linux,
  Tesseract bundled in all three, code signing budgeted. Serves S1.
  Done when someone who did not build it installs it on a fresh
  machine per system and files a document without help.
  Blocked-by: DEED-0009, DEED-0013
  **Layman:** Makes Deedbox installable by anyone on any of the three systems.
  Kind: package.
  Lanes: packaging.
  Source: design-2026-09-27.

- 📋 [DEED-0015] **Public repository, bug tracker and security contact.**
  Needs the owner's say on where the repository lives. `SECURITY.md`
  already exists and needs a real contact.
  **Layman:** A public home for the code, a place to report problems, and a private way to report security holes.
  Kind: chore.
  Lanes: repo.
  Source: design-2026-09-27.

- 📋 [DEED-0016] **Trademark check on the name Deedbox.**
  `docs/brief.md` records only a web search. Decide before the first
  public release.
  **Layman:** Makes sure nobody else owns the name before it goes public.
  Kind: investigate.
  Lanes: repo.
  Source: design-2026-09-27.
