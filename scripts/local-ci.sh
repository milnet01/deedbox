#!/usr/bin/env bash
# THE CI GATE. One list of steps, run in two places.
#
# `.github/workflows/ci.yml` CALLS this file and restates none of it. That is
# the whole point (`local-gate.md` § 3): two lists of steps drift the first
# time someone edits one of them, and the drift surfaces as a red build on a
# push — which is exactly what running locally was meant to prevent. A
# hand-written mirror is correct on the day it is written and wrong after.
#
# So: to change what CI does, change THIS FILE. Never add a step to the
# workflow.
#
# Usage:
#   ./scripts/local-ci.sh           the full gate
#   ./scripts/local-ci.sh --docs    the checks that do not need a build
#   ./scripts/local-ci.sh --docs-glob   print what counts as documentation
#
# WHY --docs EXISTS, AND WHY IT IS NOT A SKIP. Rebuilding and re-testing to fix
# a prose typo is how a person learns to reach for --no-verify. So --docs omits
# only the legs that need a compiler or a full environment, and NOTHING ELSE:
# every check that can run without one runs in both modes. A mode cheaper than
# the pipeline is fine; a mode that checks LESS of what the pipeline checks is
# a green that lies. The pre-push hook selects it on a documentation-only push.
set -Eeuo pipefail
cd "$(dirname "$0")/.."

# The one definition of what counts as documentation. The pre-push hook reads
# it with `--docs-glob` and does its own matching, so the decision has one home
# as well as one value.
DOCS_GLOB='docs/*|*.md|LICENSE'

# Tool versions are pinned in ONE place each, never in the workflow. ruff and
# pytest are pinned in pyproject.toml's dev group and locked in uv.lock; every
# check runs through `uv run --locked`, so this script and CI use the same
# versions. uv itself is pinned here and the workflow installs it from here.
UV_VERSION='0.12.19'

if [[ ${1:-} == --docs-glob ]]; then printf '%s\n' "$DOCS_GLOB"; exit 0; fi
if [[ ${1:-} == --uv-version ]]; then printf '%s\n' "$UV_VERSION"; exit 0; fi

DOCS_ONLY=0
[[ ${1:-} == --docs ]] && DOCS_ONLY=1

step() { printf '\n=== %s ===\n' "$1" >&2; }

# A check whose tool is absent SAYS SO and is never silently dropped: a check
# that did not run must not look like one that passed.
need() {
    command -v "$1" >/dev/null 2>&1 && return 0
    printf 'local-ci: %s is not installed — that check did NOT run\n' "$1" >&2
    return 1
}

# ── Checks that run in BOTH modes ───────────────────────────────────────────
# Anything not needing a compiler or a full environment belongs here.

step 'documentation'
need uv
uv run --locked python scripts/check_docs.py  # every relative link resolves

if (( DOCS_ONLY )); then
    printf '\nlocal-ci: --docs passed; build and test legs skipped by design.\n' >&2
    exit 0
fi

# ── Checks that need a build or a full environment ──────────────────────────

need uv
run() { uv run --locked --group dev "$@"; }

step 'lint'
run ruff check .
run ruff format --check src tests  # not docs: spec samples are illustrations

step 'test'
run pytest -q

printf '\nlocal-ci: all checks passed.\n' >&2
