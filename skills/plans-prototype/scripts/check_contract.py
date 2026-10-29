#!/usr/bin/env python3
"""check_contract.py: periksa empat dokumen perencanaan terhadap kontrak di references/contract.md.

Pemakaian:
  python check_contract.py <folder berisi 01-PRD.md .. 04-edge-cases.md>
  python check_contract.py <folder> --reader <path ke from-figr-files.md>

Python 3, tanpa paket tambahan. Hanya membaca. Exit code 1 bila ada FAIL.
--reader membandingkan tabel kontrak di sini dengan salinannya di pembaca (skill `plan`
Pawang) dan gagal bila berbeda, supaya kedua sisi tidak menyimpang lagi.
"""
import re, sys, collections
from pathlib import Path

DOCS = ["01-PRD.md", "02-user-flows.md", "03-interface-designs.md", "04-edge-cases.md"]
CONTRACT = Path(__file__).resolve().parent.parent / "references" / "contract.md"
START = re.compile(r"<!--\s*plans-figr-contract:(v\d+)\s*-->")
END = "<!-- /plans-figr-contract -->"
BANNED = [r"\[KEPUTUSAN\]", r"\[perlu keputusan\]", r"\[kebijakan perlu ditentukan\]"]
MARK = "[KEPUTUSAN DIBUTUHKAN]"
EC_STRICT = re.compile(r"^\| (EC-[A-Z]+-\d+) \|.*\| [KTSR] \| [PU] \|\s*$")

findings = []
def add(level, doc, msg): findings.append((level, doc, msg))

def read_block(path):
    """Kembalikan (versi, himpunan (dokumen, heading)) dari blok kontrak di sebuah file."""
    t = Path(path).read_text(encoding="utf-8")
    m = START.search(t)
    if not m or END not in t:
        return None, set()
    body = t[m.end():t.index(END)]
    rows = re.findall(r"^\|\s*`([^`]+)`\s*\|\s*`([^`]*)`\s*\|", body, re.M)
    return m.group(1), {(d.strip(), a) for d, a in rows}

def strip_fences(lines):
    out, fenced = [], False
    for ln in lines:
        if ln.lstrip().startswith("```"):
            fenced = not fenced
            out.append("")
            continue
        out.append("" if fenced else ln)
    return out

def headings(lines):
    return [(i + 1, m.group(1).strip()) for i, ln in enumerate(strip_fences(lines))
            if (m := re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", ln))]

def first(nums, n=5):
    return ", ".join(str(x) for x in nums[:n]) + (" ..." if len(nums) > n else "")

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    reader = None
    if "--reader" in sys.argv:
        i = sys.argv.index("--reader")
        reader = sys.argv[i + 1] if i + 1 < len(sys.argv) else None
        args = [a for a in args if a != reader]
    if len(args) != 1 or not Path(args[0]).is_dir():
        print(__doc__); sys.exit(2)
    folder = Path(args[0])
    ver, contract = read_block(CONTRACT)
    if not contract:
        print("Kontrak tidak terbaca dari " + str(CONTRACT)); sys.exit(2)

    texts = {}
    for d in DOCS:
        p = folder / d
        if not p.exists():
            add("FAIL", d, "file tidak ada"); continue
        texts[d] = p.read_text(encoding="utf-8").split("\n")

    marker_items = 0
    for d, lines in texts.items():
        heads = [h for _, h in headings(lines)]
        for doc, anchor in sorted(contract):
            if doc == d and not any(anchor in h for h in heads):
                add("FAIL", d, f"heading wajib tidak ada: memuat `{anchor}`")
        for pat in BANNED:
            hit = [i + 1 for i, ln in enumerate(lines) if re.search(pat, ln, re.I)]
            if hit: add("FAIL", d, f"penanda lama {pat.replace(chr(92), '')} di baris {first(hit)}; ganti dengan {MARK}")
        hit = [i + 1 for i, ln in enumerate(lines) if "{{" in ln]
        if hit: add("FAIL", d, f"sisa placeholder `{{{{...}}}}` di baris {first(hit)}")
        hit = [i + 1 for i, ln in enumerate(lines) if "<!--" in ln]
        if hit: add("WARN", d, f"komentar templat tersisa di baris {first(hit)}; hapus sebelum menyerahkan")
        # penanda keputusan dihitung hanya di baris tabel atau butir daftar (legenda berupa paragraf tidak dihitung)
        marker_items += sum(1 for ln in lines if MARK in ln and re.match(r"^\s*(\||[-*] )", ln))

    if "01-PRD.md" in texts:
        L = texts["01-PRD.md"]
        fr = [(i + 1, ln) for i, ln in enumerate(L) if ln.startswith("|") and re.search(r"\bFR-\d+\b", ln)]
        if not fr: add("FAIL", "01-PRD.md", "tidak ada baris requirement `FR-<n>`")
        bad = [n for n, ln in fr if len(set(re.findall(r"\bP[0-2]\b", ln))) != 1]
        if bad: add("FAIL", "01-PRD.md", f"baris FR tanpa tepat satu prioritas P0/P1/P2 di baris {first(bad)}")
        q = [1 for ln in L if re.match(r"^\|\s*Q\d+\s*\|", ln)]
        if marker_items and not q:
            add("FAIL", "01-PRD.md", f"ada {marker_items} penanda {MARK} tetapi `Keputusan terbuka` tidak punya baris Q<n>")

    if "02-user-flows.md" in texts:
        L = texts["02-user-flows.md"]
        flow_heads = [(n, h) for n, h in headings(L) if re.match(r".*\bF\d+ - ", h) or re.match(r"^F\d+ -", h)]
        for n, h in flow_heads:
            end = next((m for m in range(n, len(L)) if re.match(r"^#{1,3}\s", L[m]) and m + 1 != n), len(L))
            if not any(x.lstrip().startswith("```mermaid") for x in L[n:end]):
                add("FAIL", "02-user-flows.md", f"flow `{h}` (baris {n}) tidak memuat blok Mermaid")
        listed = set(re.findall(r"^\|\s*(F\d+)\s*\|", "\n".join(L), re.M))
        titled = {re.search(r"(F\d+) - ", h).group(1) for _, h in flow_heads}
        if listed - titled: add("WARN", "02-user-flows.md", f"ada di Daftar flow tetapi tanpa heading: {', '.join(sorted(listed - titled))}")
        if titled - listed: add("WARN", "02-user-flows.md", f"ada heading tetapi tidak di Daftar flow: {', '.join(sorted(titled - listed))}")

    if "04-edge-cases.md" in texts:
        L = texts["04-edge-cases.md"]
        loose = [(i + 1, ln) for i, ln in enumerate(L) if ln.startswith("| EC-")]
        good = [(n, ln) for n, ln in loose if EC_STRICT.match(ln)]
        if not good: add("FAIL", "04-edge-cases.md", "tidak ada baris edge case berformat benar")
        bad = [n for n, ln in loose if not EC_STRICT.match(ln)]
        if bad: add("FAIL", "04-edge-cases.md", f"baris EC tidak berakhir `| Sev | Dasar |` (K/T/S/R dan P/U) di baris {first(bad)}")
        ids = collections.Counter(EC_STRICT.match(ln).group(1) for _, ln in good)
        dup = [i for i, c in ids.items() if c > 1]
        if dup: add("FAIL", "04-edge-cases.md", "ID duplikat: " + ", ".join(dup))

    if reader:
        rv, rc = read_block(reader)
        if not rc: add("FAIL", "reader", f"blok kontrak tidak ditemukan di {reader}")
        else:
            if rv != ver: add("FAIL", "reader", f"versi kontrak berbeda: skill {ver}, pembaca {rv}")
            for doc, a in sorted(contract - rc): add("FAIL", "reader", f"ada di skill, tidak ada di pembaca: {doc} `{a}`")
            for doc, a in sorted(rc - contract): add("FAIL", "reader", f"ada di pembaca, tidak ada di skill: {doc} `{a}`")

    order = {"FAIL": 0, "WARN": 1}
    findings.sort(key=lambda f: order[f[0]])
    for lv, d, m in findings: print(f"[{lv}] {d}: {m}")
    nf = sum(1 for f in findings if f[0] == "FAIL"); nw = len(findings) - nf
    print(f"\nKontrak {ver}: {nf} FAIL, {nw} WARN" + (" (pembaca ikut dicek)" if reader else ""))
    sys.exit(1 if nf else 0)

main()
