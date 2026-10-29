#!/usr/bin/env python3
"""Hitung ringkasan tabel edge case (04-edge-cases.md) agar angka di bagian ringkasan tidak salah hitung.

Baris yang dihitung: `| EC-XX-NN | ... | <Sev K/T/S/R> | <Dasar P/U> |`
Pemakaian: python edge_summary.py 04-edge-cases.md
Mencetak tabel per-area (jumlah, kritis) dan total sebaran severity/dasar; salin ke bagian ringkasan.
"""
import collections, re, sys
s = open(sys.argv[1]).read()
rows = re.findall(r"^\| (EC-[A-Z]+)-\d+ .*?\| ([KTSR]) \| ([PU]) \|$", s, re.M)
n = collections.Counter(r[0] for r in rows)
k = collections.Counter(r[0] for r in rows if r[1] == "K")
print("| Area | Jumlah | Kritis (K) |\n|---|---:|---:|")
for a in n: print(f"| {a} | {n[a]} | {k[a]} |")
sev = collections.Counter(r[1] for r in rows); base = collections.Counter(r[2] for r in rows)
print(f"\nTotal {len(rows)} · severity: K {sev['K']} · T {sev['T']} · S {sev['S']} · R {sev['R']} · dasar: P {base['P']} · U {base['U']}")
ids = [m for m in re.findall(r"^\| (EC-[A-Z]+-\d+) ", s, re.M)]
dup = [i for i, c in collections.Counter(ids).items() if c > 1]
if dup: print("ID duplikat:", dup); sys.exit(1)
