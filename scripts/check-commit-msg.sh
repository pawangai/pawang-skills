#!/usr/bin/env bash
# Memeriksa baris subjek: Conventional Commits, maks 72 karakter, tanpa titik akhir.
# Pemakaian: scripts/check-commit-msg.sh <berkas-pesan>
set -euo pipefail

subject="$(head -n 1 "$1")"

# Merge/revert otomatis git dilewati.
case "$subject" in "Merge "*|"Revert \""*) exit 0 ;; esac

re='^(feat|fix|chore|docs|refactor|test|ci|build|perf|style|revert)(\([a-z0-9._-]+\))?!?: .+'
if ! printf '%s' "$subject" | grep -Eq "$re"; then
  echo "FAIL commit: '$subject' bukan Conventional Commits (contoh: 'feat: tambah skill x')." >&2
  exit 1
fi
if [ "${#subject}" -gt 72 ]; then
  echo "FAIL commit: subjek ${#subject} karakter (maks 72)." >&2
  exit 1
fi
case "$subject" in *.) echo "FAIL commit: subjek tidak boleh diakhiri titik." >&2; exit 1 ;; esac
echo "commit message OK"
