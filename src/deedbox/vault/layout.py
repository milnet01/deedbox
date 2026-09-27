"""Where everything lives in a vault folder, and each encrypted file's prefix.

docs/specs/DEED-0002-vault-format.md § 4.1 and § 4.3.
"""

from __future__ import annotations

import re
import secrets
import struct
from pathlib import Path

from deedbox.errors import VaultCorrupt, VaultTooNew

FORMAT = 1
HEADER = "vault.deedbox"
OBJECTS = "objects"

CONTENT_MAGIC = b"DBXC"
METADATA_MAGIC = b"DBXM"
INDEX_MAGIC = b"DBXI"
PREFIX_BYTES = 6

_ID = re.compile(r"[0-9a-f]{32}")


def new_id() -> str:
    return secrets.token_hex(16)


def is_id(value: str) -> bool:
    return _ID.fullmatch(value) is not None


def content_path(folder: Path, doc_id: str) -> Path:
    return folder / OBJECTS / f"{doc_id}.c"


def metadata_path(folder: Path, doc_id: str) -> Path:
    return folder / OBJECTS / f"{doc_id}.m"


def prefix(magic: bytes) -> bytes:
    return magic + struct.pack(">H", FORMAT)


def check_prefix(data: bytes, magic: bytes) -> int:
    """The file's format number, once its prefix is one this release reads."""
    if len(data) < PREFIX_BYTES or data[:4] != magic:
        raise VaultCorrupt("not the file type expected here")
    (fmt,) = struct.unpack(">H", data[4:PREFIX_BYTES])
    if fmt > FORMAT:
        raise VaultTooNew(f"file format {fmt}")
    if fmt < 1:
        raise VaultCorrupt(f"file format {fmt}")
    return fmt
