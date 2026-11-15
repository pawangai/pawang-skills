#!/usr/bin/env python3
"""Pemeriksa deterministik untuk skill make-theme (hanya pustaka standar Python 3).

Pemakaian:
  python3 check_theme.py contrast "Nama=#HEX" "Nama=#HEX" ...
  python3 check_theme.py count meta-title "teks"        # maks. 60 karakter
  python3 check_theme.py count meta-description "teks"  # maks. 155 karakter
  python3 check_theme.py count faq "teks jawaban"       # 40-60 kata
Exit code 0 = lolos, 1 = melanggar batas atau masukan salah.
"""
import itertools
import re
import sys

HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
LIMITS = {"meta-title": ("karakter", 0, 60), "meta-description": ("karakter", 0, 155), "faq": ("kata", 40, 60)}


def luminance(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def contrast(args):
    pal = {}
    for a in args:
        name, _, hx = a.partition("=")
        if not HEX_RE.match(hx):
            sys.exit(f"HEX harus 6 digit dengan awalan #: {a!r}")
        pal[name] = hx
    if len(pal) < 2:
        sys.exit("butuh minimal dua warna")
    for (n1, h1), (n2, h2) in itertools.combinations(pal.items(), 2):
        r = ratio(h1, h2)
        verdict = "boleh untuk teks" if r >= 4.5 else "hanya ikon atau bentuk besar" if r >= 3 else "dilarang untuk teks"
        print(f"{n1} dengan {n2}: {r:.2f}:1 -> {verdict}")


def count(kind, text):
    if kind not in LIMITS:
        sys.exit(f"jenis tidak dikenal: {kind}")
    unit, lo, hi = LIMITS[kind]
    n = len(text) if unit == "karakter" else len(text.split())
    ok = lo <= n <= hi
    print(f"{kind}: {n} {unit} (batas {lo}-{hi}) -> {'OK' if ok else 'MELANGGAR'}")
    return ok


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd, rest = sys.argv[1], sys.argv[2:]
    if cmd == "contrast":
        contrast(rest)
    elif cmd == "count" and len(rest) == 2:
        sys.exit(0 if count(rest[0], rest[1]) else 1)
    else:
        sys.exit(__doc__)
