"""scripts/check_docs.py (DEED-0022): every relative Markdown link resolves.

A broken link is reported; a working one, a web link, a same-page anchor
and a link inside a code fence are not.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check_docs.py"


def load():
    spec = importlib.util.spec_from_file_location("check_docs", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_reports_only_broken_relative_links(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "real.md").write_text("# Real\n")
    page = tmp_path / "README.md"
    page.write_text(
        "[ok](docs/real.md) [ok with anchor](docs/real.md#real)\n"
        "[gone](docs/missing.md) [web](https://example.com/x.md)\n"
        "[here](#top) [mail](mailto:a@b.c)\n"
        "```\n[in a fence](nowhere.md)\n```\n"
    )
    problems = load().broken_links(tmp_path, [page])
    assert problems == [("README.md", 2, "docs/missing.md")]
