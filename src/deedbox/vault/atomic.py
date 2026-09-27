"""Write-new, flush, replace: a file is either the old one or the new one.

docs/specs/DEED-0002-vault-format.md § 4.6 and
docs/specs/DEED-0003-index-and-recovery.md § 4.4.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import BinaryIO

try:
    import fcntl
except ImportError:  # Windows
    fcntl = None


def write_bytes(target: Path, data: bytes) -> None:
    with write_stream(target) as out:
        out.write(data)


@contextmanager
def write_stream(target: Path) -> Iterator[BinaryIO]:
    """Yield a file whose contents replace `target` only on a clean exit.

    The temporary file sits beside the target, so the replace never crosses
    a file system. Any failure removes it and re-raises.
    """
    tmp = target.with_name(target.name + ".tmp")
    try:
        with tmp.open("wb") as out:
            yield out
            out.flush()
            _flush_file(out.fileno())
        tmp.replace(target)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
    _flush_directory(target.parent)


def delete(path: Path) -> None:
    """Remove `path` so that the removal survives a power cut."""
    path.unlink(missing_ok=True)
    _flush_directory(path.parent)


def _flush_file(fd: int) -> None:
    # macOS fsync leaves data in the drive's own cache; F_FULLFSYNC empties it.
    if fcntl is not None and hasattr(fcntl, "F_FULLFSYNC"):
        fcntl.fcntl(fd, fcntl.F_FULLFSYNC)
    else:
        os.fsync(fd)


def _flush_directory(directory: Path) -> None:
    # Windows has no directory handle to flush.
    if os.name == "nt":
        return
    fd = os.open(directory, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
