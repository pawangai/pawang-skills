#!/usr/bin/env bash
# Mengemas skill menjadi dist/<nama>.skill (zip dengan folder skill di akar arsip).
# Pemakaian: scripts/package.sh            -> semua skill
#            scripts/package.sh interview  -> satu skill
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 - "$ROOT" "$@" <<'PY'
import sys, zipfile
from pathlib import Path

root = Path(sys.argv[1])
skills_dir, dist = root / "skills", root / "dist"
wanted = sys.argv[2:]
dist.mkdir(exist_ok=True)

names = wanted or sorted(p.name for p in skills_dir.iterdir() if (p / "SKILL.md").is_file())
for name in names:
    src = skills_dir / name
    if not (src / "SKILL.md").is_file():
        sys.exit(f"skill tidak ditemukan: {name}")
    out = dist / f"{name}.skill"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(src.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts and f.suffix != ".pyc":
                z.write(f, Path(name) / f.relative_to(src))
    print(f"dibuat: dist/{name}.skill")
PY
