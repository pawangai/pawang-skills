#!/usr/bin/env python3
"""Validasi semua blok ```mermaid di file Markdown dengan mermaid-cli (mmdc).

Pemakaian: python validate_mermaid.py FILE.md [FILE.md ...]
Exit code 1 bila ada diagram gagal. Mencari Chrome sendiri karena mmdc default
mencari di ~/.cache/puppeteer milik user yang menjalankan (sering beda di sandbox).
"""
import glob, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path


def find_chrome():
    pats = ["/home/*/.cache/puppeteer/chrome-headless-shell/*/*/chrome-headless-shell",
            "/root/.cache/puppeteer/chrome-headless-shell/*/*/chrome-headless-shell",
            "/home/*/.cache/puppeteer/chrome/*/*/chrome", "/opt/pw-browsers/chromium-*/chrome-linux/chrome"]
    for p in pats:
        hits = sorted(glob.glob(p))
        if hits: return hits[-1]
    return shutil.which("chromium") or shutil.which("google-chrome")


def main():
    if not shutil.which("mmdc"):
        sys.exit("mmdc tidak ada. Install: npm i -g @mermaid-js/mermaid-cli (butuh jaringan) — atau periksa sintaks manual.")
    chrome = find_chrome()
    tmp = Path(tempfile.mkdtemp())
    pp = tmp / "pp.json"
    pp.write_text(json.dumps({"executablePath": chrome, "args": ["--no-sandbox", "--disable-setuid-sandbox"]} if chrome else {"args": ["--no-sandbox"]}))
    bad = 0; total = 0
    for md in sys.argv[1:]:
        blocks = re.findall(r"```mermaid\n(.*?)```", Path(md).read_text(), re.S)
        for i, b in enumerate(blocks, 1):
            total += 1
            src = tmp / "d.mmd"; out = tmp / "d.svg"
            src.write_text(b)
            if out.exists(): out.unlink()
            r = subprocess.run(["mmdc", "-p", str(pp), "-i", str(src), "-o", str(out)], capture_output=True, text=True, timeout=180)
            ok = out.exists() and out.stat().st_size > 0
            first = b.strip().splitlines()[0]
            print(f"{'OK  ' if ok else 'FAIL'} {Path(md).name} #{i} ({first})")
            if not ok:
                bad += 1
                print("     " + "\n     ".join((r.stderr or r.stdout).strip().splitlines()[:4]))
    print(f"{total - bad}/{total} diagram valid")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
