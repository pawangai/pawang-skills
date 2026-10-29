#!/usr/bin/env python3
"""Inventarisasi prototype FE (folder atau .zip) untuk disatukan menjadi modular monolith.

Menghasilkan:
  <out>/inventory.json   data mentah (modul, frame, route, nav, primitives, konflik)
  <out>/summary.md       ringkasan terukur (tabel shell, duplikasi, konflik route)
  <out>/frames.md        inventaris frame per modul (dipakai di 03-interface-designs.md bagian C)

Pemakaian:
  python inventory.py INPUT [INPUT ...] --out DIR [--config config.json]
INPUT = folder yang berisi modul (fe-*/), folder satu modul, atau file .zip satu modul.

config.json (opsional):
{
  "prefix":  {"fe-crm": "/crm"},                 # namespace modul baru (default "/<slug>")
  "strip":   {"fe-cms": "/m"},                   # awalan route lama yang dibuang sebelum diberi prefix
  "root":    {"fe-admin": "/"},                  # route "/" lama -> route baru (default <prefix>/dashboard)
  "remove":  {"fe-crm": ["/login"]},             # route yang dihapus (diganti modul lain)
  "labels":  {"fe-crm": "CRM"}                   # nama tampilan modul
}
"""
import argparse, collections, json, re, sys, tempfile, zipfile
from pathlib import Path

SHELL_SECS = {"akun", "sistem", "account", "system", "me", "sys"}
def shell_route(slug, base):
    """True bila route adalah halaman Akun/Sistem milik modul (bukan sub-path domain seperti /integrasi/akun)."""
    return bool(re.match(rf"^/(?:{re.escape(slug)}/)?(akun|me)(/|$)|^/(?:{re.escape(slug)}/)?(403|404|offline|error|tidak-ada|halaman-tidak-ada)$", base))
PRIMS = ["Button", "Dialog", "Modal", "Badge", "Avatar", "EmptyState", "ErrorState", "Skeleton", "Toast", "Pill"]


def collect_modules(inputs):
    tmp = Path(tempfile.mkdtemp(prefix="proto_"))
    roots = []
    for inp in inputs:
        p = Path(inp)
        if not p.exists():
            sys.exit(f"Input tidak ditemukan: {inp}")
        if p.suffix == ".zip":
            dest = tmp / p.stem
            with zipfile.ZipFile(p) as z:
                z.extractall(dest)
            roots.append(dest)
        else:
            roots.append(p)
    mods = {}
    for r in roots:
        def is_mod(d):
            return (d / "screens.figr.json").exists() or (d / "routes.tsx").exists()
        cands = [r] if is_mod(r) else [d for d in sorted(r.iterdir()) if d.is_dir() and is_mod(d)]
        # zip yang membungkus satu folder modul di dalamnya
        if not cands:
            cands = [d for d in r.rglob("*") if d.is_dir() and is_mod(d)][:1]
        for d in cands:
            name = d.name if d.name != r.name or r not in roots[:0] else d.name
            mods[name] = d
    return mods


def slug_of(name):
    return re.sub(r"^(fe|app|web|ui)[-_]", "", name)


def sniff_shell(d):
    """Cari file shell/layout, ambil lebar rail/panel, warna, item nav."""
    info = {"files": [], "rail_width": None, "rail_dark": None, "panel_widths": [], "nav": []}
    files = [f for f in d.rglob("*.tsx") if re.search(r"(shell|layout|appshell|accountshell)", f.name, re.I)]
    for f in files:
        t = f.read_text(errors="ignore")
        info["files"].append(str(f.relative_to(d)))
        m = re.search(r"<nav[^>]*className=\"[^\"]*\b(w-16|w-\[(\d+)px\])", t)
        if m and not info["rail_width"]:
            info["rail_width"] = "64px" if m.group(1) == "w-16" else m.group(2) + "px"
            info["rail_dark"] = bool(re.search(r"<nav[^>]*navy-900", t))
        info["panel_widths"] += re.findall(r"w-\[(\d{3})px\]", t)
        for to, label in re.findall(r"to:\s*\"([^\"]+)\"\s*,\s*label:\s*\"([^\"]+)\"", t):
            info["nav"].append({"to": to, "label": label})
    info["panel_widths"] = sorted(set(info["panel_widths"]))
    seen, nav = set(), []
    for n in info["nav"]:
        if (n["to"], n["label"]) not in seen:
            seen.add((n["to"], n["label"])); nav.append(n)
    info["nav"] = nav
    return info


def sniff_primitives(d):
    found = collections.defaultdict(list)
    for f in d.rglob("*.tsx"):
        t = f.read_text(errors="ignore")
        for p in PRIMS:
            if re.search(rf"export (default )?(function|const) {p}\b", t):
                found[p].append(str(f.relative_to(d)))
    return dict(found)


def sniff_routes(d):
    paths = []
    f = d / "routes.tsx"
    if f.exists():
        paths = re.findall(r'<Route\s+[^>]*path="([^"]+)"', f.read_text(errors="ignore"))
    return paths


def sniff_stack(d):
    app = d / "App.tsx"
    t = app.read_text(errors="ignore") if app.exists() else ""
    return {"BrowserRouter": "BrowserRouter" in t, "StoreProvider": "StoreProvider" in t}


def classify(frames):
    n = frames[0]["name"]
    st = [f.get("state", {}) for f in frames]
    if all("dialog" in s for s in st) or re.search(r"\bDialog\b", n): return "Dialog"
    if re.search(r"^\d*\s*·?\s*Tab ", n): return "Tab dalam detail"
    if re.search(r"Panel ", n): return "Panel samping"
    if re.search(r"Kanvas|Editor langkah|Editor konten|Matriks|Peta|Papan|Kalender|Canvas|Board|Kanban", n): return "Canvas / lebar penuh"
    if "Dashboard" in n: return "Dashboard"
    if re.search(r"(Form|Buat|Impor|Ajukan|Create|Edit)\b", n): return "Form"
    if re.search(r"Aging|Pendapatan|Rekonsiliasi|Rekap|Laporan|Report", n): return "Laporan"
    if re.search(r"Daftar|Inbox|Kotak|Riwayat|Log |List", n): return "List (master-detail)"
    if re.search(r"Detail|Ringkasan|Pratinjau|Profil|Pengaturan|Sesi|Perangkat|Persetujuan|Koneksi|Notifikasi|Pengumuman", n): return "Detail / halaman"
    return "Halaman"


def states(frames):
    t = set()
    for f in frames:
        n = f["name"].lower(); s = json.dumps(f.get("state", {})).lower()
        if re.search(r"memuat|loading", n + s): t.add("loading")
        if re.search(r"gagal|error", n + s) and not re.search(r"submit|gagal simpan|gagal kirim|gagal membuat", n + s): t.add("error")
        if re.search(r"kosong|empty|tanpa|belum dibuat|tidak ada|hanya sesi|tidak ditemukan", n + s): t.add("empty")
        if re.search(r"submit|gagal simpan|gagal kirim|gagal membuat", n + s): t.add("submit-error")
        if re.search(r"validasi", n + s) or '"errors": true' in s or '"tried": true' in s: t.add("validasi")
        if "403" in n: t.add("403")
    order = ["loading", "error", "empty", "validasi", "submit-error", "403"]
    return ", ".join(x for x in order if x in t) or "—"


def new_route(mod, route, cfg):
    base = route.split("?")[0]
    q = ("?" + route.split("?", 1)[1]) if "?" in route else ""
    slug = slug_of(mod)
    prefix = cfg.get("prefix", {}).get(mod, "/" + slug)
    if base in cfg.get("remove", {}).get(mod, []):
        return "— (dihapus)"
    if base == "/" :
        root = cfg.get("root", {}).get(mod)
        return (root if root else prefix + "/dashboard") + q
    strip = cfg.get("strip", {}).get(mod)
    if strip and base.startswith(strip + "/"):
        base = base[len(strip):]
    if base == prefix or base.startswith(prefix + "/"):
        return base + q
    return prefix + base + q


def build_frames(mod, d, cfg, auth_mod=None):
    fig = d / "screens.figr.json"
    if not fig.exists():
        return None
    data = json.loads(fig.read_text())
    secs = {s["id"]: s["name"] for s in data.get("sections", [])}
    groups = collections.OrderedDict()
    for sid, s in data["screens"].items():
        m = re.match(r"^(\d+)\b", s["name"])
        key = ("n", int(m.group(1))) if m else ("x", re.sub(r"\s*[·—(].*$", "", s["name"]).strip())
        groups.setdefault((s["section"], key), []).append(s)
    by_route = {}
    for (sec, k), fr in groups.items():
        if k[0] == "n":
            for f in fr:
                by_route.setdefault(f["route"].split("?")[0], (sec, k))
    merged = collections.OrderedDict()
    for (sec, k), fr in groups.items():
        if k[0] == "x":
            tgt = next((by_route[f["route"].split("?")[0]] for f in fr if f["route"].split("?")[0] in by_route), None)
            if tgt:
                merged.setdefault(tgt, []).extend(fr); continue
        merged.setdefault((sec, k), []).extend(fr)
    order = {s["id"]: i for i, s in enumerate(data.get("sections", []))}
    items = sorted(merged.items(), key=lambda kv: (order.get(kv[0][0], 99), kv[0][1][0] != "n", kv[0][1][1] if kv[0][1][0] == "n" else 0))
    rows, shell_skipped = [], 0
    for (sec, k), fr in items:
        is_shell = sec in SHELL_SECS or all(shell_route(slug_of(mod), f["route"].split("?")[0]) for f in fr)
        if is_shell and mod != auth_mod:
            shell_skipped += len(fr); continue
        nostate = [f for f in fr if not f.get("state")]
        base = nostate[0] if nostate else fr[0]
        nm = re.sub(r"^\d+\s*·?\s*", "", base["name"])
        nm = re.sub(r"\s*[—·(]\s*(memuat|loading|gagal.*|error|kosong|empty).*$", "", nm).strip() or nm
        rows.append({"section": secs.get(sec, sec), "num": k[1] if k[0] == "n" else None, "name": nm,
                     "old_route": base["route"], "new_route": new_route(mod, base["route"], cfg),
                     "layout": classify(fr), "states": states(fr), "frames": len(fr)})
    nums = {r["num"] for r in rows if r["num"] is not None}
    return {"total_frames": len(data["screens"]), "sections": list(secs.values()), "rows": rows,
            "shell_frames_skipped": shell_skipped, "distinct_screens": len(nums),
            "edges": len(data.get("edges", []))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--config")
    ap.add_argument("--auth-module", help="modul pemilik halaman Akun/Sistem kanonik (default: yang namanya mengandung 'auth')")
    a = ap.parse_args()
    cfg = json.loads(Path(a.config).read_text()) if a.config else {}
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    mods = collect_modules(a.inputs)
    if not mods:
        sys.exit("Tidak ada modul ditemukan (butuh screens.figr.json atau routes.tsx).")
    auth_mod = a.auth_module or next((m for m in mods if "auth" in m), None)
    inv = {"modules": {}}
    for name, d in mods.items():
        frames = build_frames(name, d, cfg, auth_mod)
        inv["modules"][name] = {"label": cfg.get("labels", {}).get(name, slug_of(name).upper()),
                                "shell": sniff_shell(d), "primitives": sniff_primitives(d),
                                "routes": sniff_routes(d), "stack": sniff_stack(d),
                                "files": sum(1 for _ in d.rglob("*.ts*")), "frames": frames}
    # konflik route lintas modul (segmen pertama route nav/Route)
    first = collections.defaultdict(set)
    for name, m in inv["modules"].items():
        for p in m["routes"] + [n["to"] for n in m["shell"]["nav"]]:
            if not p.startswith("/") or p.startswith(("/:", "/*")) or p == "/":
                continue
            first["/" + p.strip("/").split("/")[0]].add(name)
    inv["route_collisions"] = {k: sorted(v) for k, v in first.items() if len(v) > 1}

    # tumpang tindih fitur: kata kunci sama di nama section / nav / screen lintas modul (petunjuk, bukan bukti)
    STOP = set("daftar detail form dialog akun saya sistem dashboard halaman memuat kosong gagal baru ubah dari untuk dengan yang atau data shell tidak ditemukan tidak berwenang pengaturan sesi aktif perangkat terdaftar persetujuan koneksi kalender notifikasi pengumuman".split())
    kw = collections.defaultdict(lambda: collections.defaultdict(set))
    for name, m in inv["modules"].items():
        texts = [n["label"] for n in m["shell"]["nav"]]
        if m["frames"]:
            texts += m["frames"]["sections"] + [r["name"] for r in m["frames"]["rows"]]
        for t in texts:
            for w in re.findall(r"[a-zA-Z]{5,}", t.lower()):
                if w not in STOP:
                    kw[w][name].add(t)
    inv["feature_overlap"] = {w: sorted(v) for w, v in kw.items() if len(v) > 1}
    (out / "inventory.json").write_text(json.dumps(inv, indent=2, ensure_ascii=False))

    S = ["# Ringkasan inventarisasi\n",
         "| Modul | File | Frame | Screen unik | Rail | Panel list | BrowserRouter | Store |",
         "|---|---:|---:|---:|---|---|---|---|"]
    tf = 0
    for n, m in inv["modules"].items():
        f = m["frames"] or {}
        tf += f.get("total_frames", 0)
        sh = m["shell"]
        rail = (sh["rail_width"] or "?") + (" navy" if sh["rail_dark"] else "")
        S.append(f"| {n} | {m['files']} | {f.get('total_frames','—')} | {f.get('distinct_screens','—')} | {rail} | {', '.join(sh['panel_widths']) or '—'} | {'ya' if m['stack']['BrowserRouter'] else 'tidak'} | {'ya' if m['stack']['StoreProvider'] else 'tidak'} |")
    S.append(f"\nTotal frame: **{tf}**\n")
    S.append("## Primitives yang diduplikasi\n\n| Primitive | Jumlah modul | Modul |\n|---|---:|---|")
    dup = collections.defaultdict(list)
    for n, m in inv["modules"].items():
        for p in m["primitives"]:
            dup[p].append(n)
    for p, ms in sorted(dup.items(), key=lambda kv: -len(kv[1])):
        S.append(f"| {p} | {len(ms)} | {', '.join(ms)} |")
    S.append("\n## Item navigasi per modul (dari shell)\n")
    for n, m in inv["modules"].items():
        S.append(f"- **{n}**: " + ("; ".join(f"{x['label']} (`{x['to']}`)" for x in m["shell"]["nav"]) or "—"))
    S.append("\n## Tabrakan route (segmen pertama dipakai >1 modul)\n")
    S += [f"- `{k}` → {', '.join(v)}" for k, v in sorted(inv["route_collisions"].items())] or ["- tidak ada"]
    S.append("\n## Kandidat tumpang tindih fitur (kata kunci yang sama di >1 modul — verifikasi manual)\n")
    ov = sorted(inv["feature_overlap"].items(), key=lambda kv: -len(kv[1]))[:45]
    S += [f"- `{w}` → {', '.join(ms)}" for w, ms in ov] or ["- tidak ada"]
    no_edges = [n for n, m in inv["modules"].items() if m["frames"] and m["frames"]["edges"] == 0]
    if no_edges:
        S.append(f"\n> `edges` kosong di: {', '.join(no_edges)} — flow harus diturunkan sendiri dari nama screen, route, dan tipe status.")
    (out / "summary.md").write_text("\n".join(S) + "\n")

    F = []
    for n, m in inv["modules"].items():
        f = m["frames"]
        if not f: continue
        F.append(f"\n### {m['label']} (`{n}`) — {f['total_frames']} frame\n")
        cur = None
        for r in f["rows"]:
            if r["section"] != cur:
                cur = r["section"]
                F.append(f"\n**{cur}**\n\n| # | Screen | Route baru | Layout | State tersedia | Frame |\n|---|---|---|---|---|---:|")
            F.append(f"| {r['num'] if r['num'] is not None else '—'} | {r['name']} | `{r['new_route']}` | {r['layout']} | {r['states']} | {r['frames']} |")
        if f["shell_frames_skipped"]:
            F.append(f"\n_{f['shell_frames_skipped']} frame Akun saya / Sistem di `{n}` tidak dimigrasikan — diganti halaman global._")
    (out / "frames.md").write_text("\n".join(F) + "\n")
    print(f"OK: {len(inv['modules'])} modul, {tf} frame -> {out}")


if __name__ == "__main__":
    main()
