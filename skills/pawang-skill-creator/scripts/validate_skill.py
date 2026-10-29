#!/usr/bin/env python3
"""Validasi skill berformat Agent Skills (portabel lintas agent).

Pemakaian: python3 validate_skill.py <path-folder-skill> [--strict]
Exit code: 0 = lolos, 1 = ada ERROR (atau WARN bila --strict).
Tanpa dependensi wajib; memakai PyYAML bila tersedia untuk parse YAML sungguhan
(opsional, pasang dengan: pip install pyyaml).
"""
import ast
import re
import sys
from pathlib import Path

SPEC_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
TOC_RE = re.compile(r"^#{1,6}\s*(daftar isi|isi|contents|table of contents|toc)\b", re.I | re.M)
PY_ALIAS = {
    "yaml": "pyyaml", "PIL": "pillow", "cv2": "opencv-python", "bs4": "beautifulsoup4",
    "sklearn": "scikit-learn", "docx": "python-docx", "pptx": "python-pptx",
    "fitz": "pymupdf", "dotenv": "python-dotenv", "dateutil": "python-dateutil",
}
NODE_BUILTIN = {
    "fs", "path", "os", "http", "https", "crypto", "child_process", "util", "url", "stream",
    "events", "zlib", "readline", "assert", "buffer", "net", "tty", "process", "module",
    "worker_threads", "perf_hooks", "querystring", "string_decoder", "timers", "vm",
}
REF_TOC_LINES = 25   # daftar isi harus muncul di sekian baris pertama
REF_LONG = 100       # referensi di atas ini wajib punya daftar isi
REF_DIRS = ("references", "reference")  # proyek Pawang memakai `reference/` (tunggal)
EXAMPLE_LINE_RE = re.compile(r"\b(contoh|misalnya|bukan|dst|e\.g\.)\b", re.I)
RUNTIME_PREFIXES = ("assets/_work/",)  # scratch runtime milik proyek pengguna, bukan bagian skill


def non_stdlib_python(path, root):
    """Nama modul top-level non-stdlib dan non-lokal yang di-import file .py."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError):
        return set()
    stdlib = getattr(sys, "stdlib_module_names", None)
    if stdlib is None:  # Python < 3.10: lewati cek daripada memberi positif palsu
        return set()
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            mods.add(node.module.split(".")[0])
    local = {p.stem for p in (root / "scripts").glob("*.py")} | {
        p.name for p in (root / "scripts").iterdir() if p.is_dir()
    }
    return {m for m in mods if m not in stdlib and m not in local}


def non_builtin_node(path):
    """Nama paket npm yang di-require atau di-import file .js/.mjs/.cjs/.ts."""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return set()
    pkgs = set()
    for m in re.findall(r"(?:require\(\s*|from\s+|import\s+)['\"]([^'\"]+)['\"]", text):
        if m.startswith((".", "/")):
            continue
        name = m[5:] if m.startswith("node:") else m
        parts = name.split("/")
        pkg = "/".join(parts[:2]) if name.startswith("@") else parts[0]
        if pkg not in NODE_BUILTIN:
            pkgs.add(pkg)
    return pkgs


def has_install_line(names, texts):
    """True bila ada baris yang memuat kata 'install' dan salah satu nama paket."""
    wanted = {n.lower().replace("_", "-") for n in names if n}
    for text in texts:
        for line in text.splitlines():
            low = line.lower().replace("_", "-")
            if "install" in low and any(w in low for w in wanted):
                return True
    return False


def split_frontmatter(text):
    if not text.startswith("---"):
        return None, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not m:
        return None, text
    return m.group(1), m.group(2)


def simple_parse(raw):
    """Parser minimal: key: value satu baris, atau blok > / | dengan indentasi."""
    data, key, buf, mode = {}, None, [], None
    for line in raw.splitlines():
        if key and mode and (line.startswith(" ") or not line.strip()):
            buf.append(line.strip())
            continue
        if key and mode:
            data[key] = (" " if mode == ">" else "\n").join(b for b in buf if b)
            key, buf, mode = None, [], None
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not m:
            continue
        k, v = m.group(1), m.group(2).strip()
        if v in (">", "|", ">-", "|-"):
            key, mode, buf = k, v[0], []
        else:
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                v = v[1:-1]
            data[k] = v
    if key and mode:
        data[key] = (" " if mode == ">" else "\n").join(b for b in buf if b)
    return data


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strict = "--strict" in sys.argv
    if not args:
        print(__doc__)
        return 1
    root = Path(args[0]).resolve()
    errors, warns = [], []
    E, W = errors.append, warns.append

    skill_md = root / "SKILL.md"
    if not skill_md.is_file():
        print(f"ERROR: SKILL.md tidak ditemukan di {root}")
        return 1
    text = skill_md.read_text(encoding="utf-8")
    raw, body = split_frontmatter(text)
    if raw is None:
        print("ERROR: frontmatter YAML (--- ... ---) tidak ditemukan di awal SKILL.md")
        return 1

    # Parse YAML sungguhan bila ada; fallback ke parser sederhana.
    fm = None
    try:
        import yaml  # type: ignore

        try:
            fm = yaml.safe_load(raw)
            if not isinstance(fm, dict):
                E("frontmatter bukan pemetaan key: value")
                fm = {}
        except yaml.YAMLError as exc:
            E(
                "YAML tidak valid (sering karena ': ' atau tanda kutip di description "
                f"tanpa kutip pembungkus): {str(exc).splitlines()[0]}"
            )
            fm = simple_parse(raw)
    except ImportError:
        fm = simple_parse(raw)
        for line in raw.splitlines():
            if line.startswith("description:"):
                v = line.split(":", 1)[1].strip()
                if v and v[0] not in "\"'>|" and (": " in v or " #" in v):
                    E(
                        "description satu baris tanpa kutip mengandung ': ' atau ' #' "
                        "(YAML bisa gagal diparse; bungkus dengan kutip atau pakai blok >)"
                    )

    name = str(fm.get("name", "") or "")
    desc = str(fm.get("description", "") or "")

    # name
    if not name:
        E("field 'name' wajib")
    else:
        if len(name) > 64:
            E(f"name {len(name)} karakter (maks. 64)")
        if not NAME_RE.match(name):
            E("name hanya huruf kecil, angka, tanda hubung; tanpa awalan/akhiran/ganda '-'")
        if name != root.name:
            E(f"name '{name}' harus sama dengan nama folder '{root.name}'")

    # description
    if not desc.strip():
        E("field 'description' wajib dan tidak boleh kosong")
    else:
        if len(desc) > 1024:
            E(f"description {len(desc)} karakter (maks. 1024)")
        if len(desc) < 80:
            W(f"description hanya {len(desc)} karakter; kemungkinan kurang pemicu")
        if not re.search(r"\b(use|gunakan|pakai|when|saat|jika|ketika)\b", desc, re.I):
            W("description tidak memuat penanda kapan dipakai ('Gunakan saat...' / 'Use when...')")
        if not re.search(r"\b(jangan|do not|don't|not for|bukan untuk)\b", desc, re.I):
            W("description tidak memuat batas (apa yang BUKAN untuk skill ini); risiko salah aktif")

    # field lain
    if "compatibility" in fm and len(str(fm["compatibility"])) > 500:
        E("compatibility maks. 500 karakter")
    for k in fm:
        if k not in SPEC_FIELDS:
            W(f"field '{k}' di luar spesifikasi Agent Skills; mungkin hanya didukung agent tertentu (kurangi portabilitas)")
    if "allowed-tools" in fm:
        W("'allowed-tools' eksperimental dan dukungannya beda antar agent")

    # body
    lines = body.count("\n") + 1
    if lines > 500:
        W(f"SKILL.md {lines} baris (disarankan < 500); pindahkan detail ke references/")
    elif lines > 400:
        W(f"SKILL.md {lines} baris; mendekati batas 500")
    if not body.strip():
        E("isi SKILL.md kosong setelah frontmatter")

    # path relatif yang dirujuk
    refs = set(re.findall(r"`((?:references?|scripts|assets)/[A-Za-z0-9_./-]+)`", body))
    refs |= set(re.findall(r"\]\(((?:references?|scripts|assets)/[^)#\s]+)\)", body))
    # jalur lengkap antar-skill: .agents/skills/<nama>/<path>; diperiksa terhadap folder induk skill
    # ini, dan dilewati bila skill divalidasi di luar pohon .agents/skills (tidak ada tetangga).
    full_refs = set(re.findall(
        r"\.agents/skills/([a-z0-9-]+)/((?:SKILL\.md|(?:references?|scripts|assets)/[A-Za-z0-9_./-]*[A-Za-z0-9_]))", body
    ))
    for n, rest in sorted(full_refs):
        if (root.parent / n).is_dir() and not (root.parent / n / rest).exists():
            lines_with = [ln for ln in body.splitlines() if f".agents/skills/{n}/{rest}" in ln]
            if not (lines_with and all(EXAMPLE_LINE_RE.search(ln) for ln in lines_with)):
                E(f"path lintas skill dirujuk tapi tidak ada: .agents/skills/{n}/{rest}")
    skipped_refs = []
    for r in sorted(refs):
        if (root / r).exists():
            continue
        lines_with_r = [ln for ln in body.splitlines() if r in ln]
        if (
            r.endswith("/")
            or r.startswith(RUNTIME_PREFIXES)
            or (lines_with_r and all(EXAMPLE_LINE_RE.search(ln) for ln in lines_with_r))
        ):
            skipped_refs.append(r)  # contoh penamaan, folder pengelompokan, atau path runtime
            continue
        E(f"path dirujuk tapi tidak ada: {r}")

    # file di folder skill yang tidak dirujuk dari SKILL.md
    for sub in (*REF_DIRS, "scripts", "assets"):
        d = root / sub
        if d.is_dir():
            for f in sorted(p for p in d.rglob("*") if p.is_file() and "__pycache__" not in p.parts):
                rel = f.relative_to(root).as_posix()
                if rel not in body:
                    W(f"{rel} tidak dirujuk dari SKILL.md (agent tidak akan tahu file ini ada)")

    # file asing
    for junk in ("README.md", "CHANGELOG.md", "INSTALL.md"):
        if (root / junk).exists():
            W(f"{junk} di dalam folder skill biasanya tidak perlu (taruh di luar folder skill)")

    # referensi: daftar isi untuk file panjang, dan rujukan bersarang
    ref_files = sorted(
        p
        for name in REF_DIRS
        if (root / name).is_dir()
        for p in (root / name).rglob("*")
        if p.is_file() and p.suffix.lower() in (".md", ".txt")
    )
    for f in ref_files:
        rel = f.relative_to(root).as_posix()
        t = f.read_text(encoding="utf-8", errors="replace")
        n = t.count("\n") + 1
        if n > REF_LONG and "template" not in f.name:  # template disalin utuh; TOC akan ikut tersalin
            head = "\n".join(t.splitlines()[:REF_TOC_LINES])
            if not (TOC_RE.search(head) or len(re.findall(r"\]\(#", head)) >= 3):
                W(
                    f"{rel} {n} baris tanpa daftar isi di {REF_TOC_LINES} baris pertama; "
                    "agent sering hanya membaca ~100 baris awal (tambahkan daftar isi)"
                )
        for g in ref_files:
            if g == f:
                continue
            grel = g.relative_to(root).as_posix()
            if grel in t or re.search(r"(?<![\w./-])" + re.escape(g.name) + r"(?![\w-])", t):
                W(
                    f"{rel} merujuk ke {grel} (rujukan bersarang); tautkan {grel} langsung "
                    "dari SKILL.md dan hapus rujukan antar-referensi"
                )

    # skrip dengan dependensi eksternal harus punya baris install
    sdir = root / "scripts"
    if sdir.is_dir():
        script_files = sorted(p for p in sdir.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
        texts = [body] + [p.read_text(encoding="utf-8", errors="replace") for p in script_files]
        for sf in script_files:
            srel = sf.relative_to(root).as_posix()
            if sf.suffix == ".py":
                mods = non_stdlib_python(sf, root)
                names = {PY_ALIAS.get(m, m) for m in mods} | mods
                shown = sorted(PY_ALIAS.get(m, m) for m in mods)
            elif sf.suffix in (".js", ".mjs", ".cjs", ".ts"):
                names = shown = non_builtin_node(sf)
                shown = sorted(shown)
            else:
                continue
            if names and not has_install_line(names, texts):
                W(
                    f"{srel} memakai paket eksternal ({', '.join(shown)}) tanpa baris install "
                    "di SKILL.md atau skrip (contoh: `pip install <paket>`)"
                )

    # info (tidak memengaruhi status lolos/gagal)
    infos = []
    if "compatibility" not in fm:
        infos.append(
            "field 'compatibility' kosong; catat model atau agent yang sudah diuji "
            "bila skill akan dibagikan"
        )

    if skipped_refs:
        infos.append(
            "path dirujuk tidak diperiksa (contoh, folder, atau path runtime): "
            + ", ".join(skipped_refs)
        )

    for m in errors:
        print(f"ERROR: {m}")
    for m in warns:
        print(f"WARN:  {m}")
    for m in infos:
        print(f"INFO:  {m}")
    failed = bool(errors) or (strict and bool(warns))
    status = "GAGAL" if failed else "LOLOS"
    print(
        f"\n{status}: {len(errors)} error, {len(warns)} warning "
        f"({root.name}, {lines} baris body, description {len(desc)} karakter)"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
