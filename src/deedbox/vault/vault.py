"""The `Vault` object: the only way other parts reach a vault's files.

docs/specs/DEED-0002-vault-format.md § 4.2, § 4.6 and § 4.7.
"""

from __future__ import annotations

import base64
import binascii
import datetime
import json
from pathlib import Path

from deedbox import crypto
from deedbox.errors import (
    DocumentMissing,
    NotAVault,
    VaultCorrupt,
    VaultExists,
    VaultTooNew,
)
from deedbox.vault import atomic, documents, layout


class Vault:
    """An open vault. Holds the vault key until `close`."""

    def __init__(self, folder: Path, key: bytes) -> None:
        self._folder = folder
        self._key: bytes | None = key

    @classmethod
    def create(
        cls,
        folder: Path,
        password: str,
        *,
        opslimit: int | None = None,
        memlimit: int | None = None,
    ) -> Vault:
        """A new, empty vault in `folder`, which must be empty or absent.

        `opslimit` and `memlimit` are for tests; every other caller omits them.
        """
        folder = Path(folder)
        if folder.exists() and any(folder.iterdir()):
            raise VaultExists(str(folder))
        record, key = crypto.new_key_record(
            password, opslimit=opslimit, memlimit=memlimit
        )
        (folder / layout.OBJECTS).mkdir(parents=True, exist_ok=True)
        header = {
            "format": layout.FORMAT,
            "key_record": base64.b64encode(record).decode("ascii"),
        }
        atomic.write_bytes(folder / layout.HEADER, json.dumps(header).encode("utf-8"))
        return cls(folder, key)

    @classmethod
    def open(cls, folder: Path, password: str) -> Vault:
        """The vault in `folder`, unlocked. Writes nothing."""
        folder = Path(folder)
        try:
            raw = (folder / layout.HEADER).read_bytes()
        except FileNotFoundError as err:
            raise NotAVault(str(folder)) from err
        try:
            header = json.loads(raw.decode("utf-8"))
            fmt = header["format"]
            record = base64.b64decode(header["key_record"], validate=True)
        except (
            UnicodeDecodeError,
            ValueError,
            KeyError,
            TypeError,
            binascii.Error,
        ) as err:
            raise VaultCorrupt("the vault header is malformed") from err
        if not isinstance(fmt, int) or isinstance(fmt, bool):
            raise VaultCorrupt("the vault header's format is not a number")
        if fmt > layout.FORMAT:
            raise VaultTooNew(f"vault format {fmt}")
        if fmt != layout.FORMAT:
            raise VaultCorrupt(f"vault format {fmt}")
        return cls(folder, crypto.unlock(record, password))

    def add(self, source: Path, mime_type: str) -> str:
        """Encrypt the file at `source` into the vault. Returns its new id."""
        key = self._require_key()
        source = Path(source)
        doc_id = layout.new_id()
        content = layout.content_path(self._folder, doc_id)
        with source.open("rb") as src:
            documents.write_content(content, key, src, doc_id)
        metadata = {
            "id": doc_id,
            "filename": source.name,
            "type": mime_type,
            "size": source.stat().st_size,
            "added": datetime.date.today().isoformat(),
            "edit": 1,
            "extraction": "not yet run",
        }
        try:
            documents.write_metadata(
                layout.metadata_path(self._folder, doc_id), key, metadata, doc_id
            )
        except BaseException:
            content.unlink(missing_ok=True)
            raise
        return doc_id

    def read(self, doc_id: str) -> bytes:
        """The document's original bytes, decrypted in memory."""
        key = self._require_key()
        self._require_id(doc_id)
        return documents.read_content(
            layout.content_path(self._folder, doc_id), key, doc_id
        )

    def metadata(self, doc_id: str) -> dict:
        key = self._require_key()
        self._require_id(doc_id)
        return documents.read_metadata(
            layout.metadata_path(self._folder, doc_id), key, doc_id
        )

    def close(self) -> None:
        """Drop the vault key. The object cannot be used afterwards."""
        self._key = None

    def _require_key(self) -> bytes:
        if self._key is None:
            raise ValueError("the vault is closed")
        return self._key

    @staticmethod
    def _require_id(doc_id: str) -> None:
        # An id is also a file name, so anything else could reach outside
        # objects/.
        if not layout.is_id(doc_id):
            raise DocumentMissing(doc_id)
