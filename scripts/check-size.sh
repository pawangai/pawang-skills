#!/usr/bin/env bash
# Size guard: gagal bila ada berkas terlacak (atau staged) > 1 MB.
# Pemakaian: scripts/check-size.sh            -> semua berkas terlacak
#            scripts/check-size.sh --staged   -> hanya yang staged (pre-commit)
set -euo pipefail

LIMIT=1048576
cd "$(git rev-parse --show-toplevel)"

if [ "${1:-}" = "--staged" ]; then
  list() { git diff --cached --name-only --diff-filter=ACM -z; }
  size() { git cat-file -s ":$1"; }
else
  list() { git ls-files -z; }
  size() { wc -c < "$1" | tr -d ' '; }
fi

fail=0
while IFS= read -r -d '' f; do
  [ -f "$f" ] || [ "${1:-}" = "--staged" ] || continue
  bytes="$(size "$f")"
  if [ "$bytes" -gt "$LIMIT" ]; then
    echo "FAIL ukuran: $f ($bytes byte > $LIMIT). Pakai Git LFS atau object storage, jangan masuk main." >&2
    fail=1
  fi
done < <(list)

[ "$fail" -eq 0 ] && echo "size guard OK"
exit "$fail"
