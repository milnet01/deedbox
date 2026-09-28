"""Fail when a relative Markdown link points at a file that does not exist.

Run by `scripts/local-ci.sh` in both modes (DEED-0022). It checks the tracked
`*.md` files. Web links, `mailto:`, same-page anchors and links inside code
fences are skipped. A link's `#anchor` is not checked, only its file.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

LINK = re.compile(r"\]\(([^)\s]+)\)")
FENCE = re.compile(r"^\s*(```|~~~)")


def broken_links(root: Path, pages: list[Path]) -> list[tuple[str, int, str]]:
    """(page, line, target) for every relative link whose file is missing."""
    problems = []
    for page in pages:
        in_fence = False
        text = page.read_text(encoding="utf-8").splitlines()
        for number, line in enumerate(text, start=1):
            if FENCE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for target in LINK.findall(line):
                if target.startswith(("#", "mailto:")) or "://" in target:
                    continue
                path = target.split("#", 1)[0]
                if not (page.parent / path).exists():
                    rel = page.relative_to(root).as_posix()
                    problems.append((rel, number, target))
    return problems


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    git = shutil.which("git")
    if git is None:
        print("check_docs: git is not installed — the check did NOT run")
        return 1
    tracked = subprocess.run(  # noqa: S603 — fixed arguments, git by full path
        [git, "ls-files", "-z", "*.md"],
        cwd=root,
        capture_output=True,
        check=True,
    ).stdout.split(b"\0")
    pages = [root / name.decode() for name in tracked if name]
    problems = broken_links(root, pages)
    for page, line, target in problems:
        print(f"{page}:{line}: broken link {target}")
    print(f"check_docs: {len(pages)} files, {len(problems)} broken links")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
