# ADR-0001: PyNaCl (libsodium) does all of Deedbox's encryption

- **Status:** Accepted
- **Date:** 2026-09-27

## Context

`docs/brief.md` fixed the approach: Argon2id to turn the password into a
key, and an authenticated cipher. It also said: use a well-known library,
follow its documented recipe, invent nothing.

Documents can be large scans. Encrypting a whole file in one call means
holding it all in memory twice. Splitting a file into pieces and
encrypting each safely is a known recipe — but only if the library
provides it. Writing our own splitting scheme is exactly the invention
the brief forbids.

Two well-known Python libraries were checked on 2026-09-27, by
installing each and inspecting it:

- **`cryptography`** has Argon2id and authenticated ciphers, but only as
  one-shot calls. A large file would need our own splitting scheme.
- **PyNaCl** wraps libsodium. It has Argon2id and libsodium's
  "secretstream" recipe, which encrypts a file as a sequence of pieces
  and detects pieces that were removed, reordered or cut off.

## Decision

Use PyNaCl for all encryption. Argon2id derives the key. Secretstream
encrypts each document file. Libsodium's single-message authenticated
encryption protects the index. Only `src/deedbox/crypto.py` imports it.

The Argon2id cost settings are chosen and written into the vault header
in build step 1, so they can be raised later without breaking old vaults.

## Consequences

- Rolodex uses `cryptography` with PBKDF2, so the two apps do not share
  crypto code. Whether Rolodex should follow is its own question.
- PyNaCl releases less often than `cryptography`. It is a thin wrapper;
  libsodium underneath does the work. If PyNaCl stops being maintained,
  the replacement must still read the same secretstream format, which
  any libsodium binding can.
- libsodium is a compiled library, so every installer must ship it.
  PyNaCl's prebuilt packages include it on all three systems.
- The independent security review before the first public release
  (`docs/brief.md`, Releasing it to the public) reviews this choice too.
