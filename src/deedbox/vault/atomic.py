"""Write-new, flush, replace: a file is either the old one or the new one.

DEED-0003 tests this on Windows, macOS and Linux; the spec is
docs/specs/DEED-0002-vault-format.md § 4.6.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import BinaryIO


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
            os.fsync(out.fileno())
        tmp.replace(target)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
