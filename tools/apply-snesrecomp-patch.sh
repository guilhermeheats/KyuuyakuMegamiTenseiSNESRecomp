#!/usr/bin/env bash
# Apply the project's portable snesrecomp patch (currently: noreturn_jsl /
# terminal_jsl support and runtime indirect tail dispatch). The submodule stays
# pinned at its public upstream commit; this script records the framework delta
# in the parent repository.
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
SUB="$ROOT/snesrecomp"
PATCH="$ROOT/patches/snesrecomp-noreturn-jsl.patch"
if [ ! -f "$PATCH" ]; then
  echo "missing patch: $PATCH" >&2
  exit 1
fi
if git -C "$SUB" apply --reverse --check "$PATCH" >/dev/null 2>&1; then
  echo "snesrecomp patch already applied"
  exit 0
fi
git -C "$SUB" apply --check "$PATCH"
git -C "$SUB" apply "$PATCH"
echo "snesrecomp patch applied"
echo "next: PATH=\"\$HOME/.cargo/bin:\$PATH\" tools/regen.sh --rom <rom>"
