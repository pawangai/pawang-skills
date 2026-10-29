#!/usr/bin/env bash
# Memvalidasi semua skill di skills/: kecocokan name dengan folder, metadata.author,
# validator pawang-skill-creator, dan sintaks skrip Python. Exit 1 bila ada FAIL.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS="$ROOT/skills"
VALIDATOR="$SKILLS/pawang-skill-creator/scripts/validate_skill.py"
fail=0

for dir in "$SKILLS"/*/; do
  dir="${dir%/}"
  name="$(basename "$dir")"
  md="$dir/SKILL.md"
  echo "== $name"

  if [ ! -f "$md" ]; then
    echo "FAIL $name: SKILL.md tidak ada"; fail=1; continue
  fi

  fm="$(awk 'NR==1 && $0=="---" {f=1; next} f && $0=="---" {exit} f' "$md")"
  declared="$(printf '%s\n' "$fm" | sed -n 's/^name:[[:space:]]*"\{0,1\}\([^"]*\)"\{0,1\}[[:space:]]*$/\1/p' | head -n 1)"

  if [ "$declared" != "$name" ]; then
    echo "FAIL $name: name di frontmatter ('$declared') tidak sama dengan nama folder"; fail=1
  fi
  if ! printf '%s\n' "$fm" | grep -Eq '^[[:space:]]+author:[[:space:]]*"?Pawang"?[[:space:]]*$'; then
    echo "FAIL $name: metadata.author \"Pawang\" tidak ada di frontmatter"; fail=1
  fi

  python3 "$VALIDATOR" "$dir" || fail=1
done

echo "== sintaks skrip Python"
while IFS= read -r -d '' py; do
  python3 -c 'import sys; compile(open(sys.argv[1], encoding="utf-8").read(), sys.argv[1], "exec")' "$py" \
    || { echo "FAIL sintaks: ${py#"$ROOT"/}"; fail=1; }
done < <(find "$SKILLS" -name '*.py' -not -path '*/__pycache__/*' -print0)

if [ "$fail" -ne 0 ]; then echo "GAGAL"; exit 1; fi
echo "SEMUA LOLOS"
