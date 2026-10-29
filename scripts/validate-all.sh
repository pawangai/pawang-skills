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
  if ! printf '%s\n' "$fm" | grep -Eq '^license:[[:space:]]*MIT[[:space:]]*$'; then
    echo "FAIL $name: license: MIT tidak ada di frontmatter"; fail=1
  fi
  if ! printf '%s\n' "$fm" | grep -Eq '^compatibility:'; then
    echo "FAIL $name: compatibility tidak ada di frontmatter"; fail=1
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

echo "== manifest marketplace"
python3 - "$ROOT" <<'PY' || fail=1
import json, sys
from pathlib import Path

root = Path(sys.argv[1])
bad = []

def load(rel):
    try:
        return json.loads((root / rel).read_text(encoding="utf-8"))
    except Exception as exc:
        bad.append(f"{rel}: JSON tidak valid atau tidak ada ({exc})")
        return {}

cc_plugin = load(".claude-plugin/plugin.json")
cc_market = load(".claude-plugin/marketplace.json")
cx_plugin = load(".codex-plugin/plugin.json")
cx_market = load(".agents/plugins/marketplace.json")

entry = (cc_market.get("plugins") or [{}])[0]
cx_entry = (cx_market.get("plugins") or [{}])[0]

versions = {
    ".claude-plugin/plugin.json": cc_plugin.get("version"),
    ".claude-plugin/marketplace.json (metadata)": (cc_market.get("metadata") or {}).get("version"),
    ".claude-plugin/marketplace.json (plugin)": entry.get("version"),
    ".codex-plugin/plugin.json": cx_plugin.get("version"),
}
if len(set(versions.values())) != 1:
    bad.append(f"versi tidak sinkron: {versions}")

for label, value in {
    "nama marketplace Claude": cc_market.get("name"),
    "nama marketplace Codex": cx_market.get("name"),
}.items():
    if value != "pawang":
        bad.append(f"{label} harus 'pawang', ditemukan {value!r}")

names = {cc_plugin.get("name"), entry.get("name"), cx_plugin.get("name"), cx_entry.get("name")}
if names != {"pawang-skills"}:
    bad.append(f"nama plugin harus 'pawang-skills' di semua manifest, ditemukan {names}")

for label, plugin in (("Claude", cc_plugin), ("Codex", cx_plugin)):
    if plugin.get("license") != "MIT":
        bad.append(f"plugin {label}: license harus MIT")
if "$schema" in cc_market or "$schema" in cc_plugin:
    bad.append("jangan pakai $schema di manifest Claude Code (ditolak CLI)")
if cx_plugin.get("skills") != "./skills/":
    bad.append("plugin Codex: skills harus './skills/'")
if not (root / "LICENSE").is_file():
    bad.append("LICENSE tidak ada")

print("\n".join("FAIL " + b for b in bad) if bad else "manifest OK")
sys.exit(1 if bad else 0)
PY

if [ "$fail" -ne 0 ]; then echo "GAGAL"; exit 1; fi
echo "SEMUA LOLOS"
