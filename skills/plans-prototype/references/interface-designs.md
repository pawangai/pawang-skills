# Panduan menulis 03-interface-designs.md

Prinsip Figr: "Interface designs: built from flows, not from scratch." Maka dokumen ini tidak menggambar ulang isi screen yang sudah ada. Ia hanya (A) mendesain **shell baru**, (B) menghubungkan **flow → frame**, dan (C) mendaftar **semua frame** dengan route barunya.

## A. Shell

Isi minimal, urut:

1. **Grid & lebar kolom** — tabel kolom (rail 64 · menu modul 240 · panel list 360 · konten) + tabel *sisa lebar konten per viewport* (1920/1536/1440/1366/1280/min-width prototype). Hitung dari angka nyata (`inventory.py` → `panel_widths`, `rail_width`); tandai ⚠️ bila sisa < 600px.
2. **Tiga mode layout** — ASCII per mode: *Standar*, *Master-detail* (rail + menu + list + detail), *Canvas* (menu & list disembunyikan).
3. **Komponen Rail** — satu varian: ukuran, state (`default · hover · active · focus · badge-angka · badge-danger · dot · tersembunyi`), tabel ikon.
4. **Komponen Panel menu kedua** — header, grup, item, hint, badge, sub-item, collapsed. Jika prototype sudah punya pola serupa (mis. layout sub-menu di salah satu modul), **adopsi polanya** — "preserve existing conventions".
5. **Isi panel 2 per modul** — tabel grup → item.
6. **Menu akun/notifikasi/pengumuman**, **state shell** (memuat, tanpa izin, chunk gagal, offline, sesi habis), **responsif**, **aksesibilitas**.

Gunakan hanya token yang sudah terlihat di kode (`bg-surface`, `bg-primary-soft`, …). Jangan memperkenalkan palet baru. Nilai yang saya usulkan sendiri (mis. 240px, 360px) dinyatakan sebagai usulan beserta asal angkanya.

## B. Flow -> frame

Heading bagian ini harus memuat teks `Flow -> frame` persis (tanda panah ASCII `->`), dan bagian C memuat `Inventaris frame`.

Tabel `Flow | urutan frame` memakai nomor screen: `#144 Pasien & layanan → #145 Jadwal → #146 Quote`. Akhiri dengan daftar **frame baru** (yang belum ada di prototype): shell, rail states, panel 2 states, avatar popover, state "modul gagal dimuat", dst.

## C. Inventaris frame

Tempel isi `frames.md` dari `inventory.py`. Kolom: `# · Screen · Route baru · Layout · State tersedia · Frame`. Tambahkan legenda:

- *Layout* diklasifikasi otomatis (heuristik nama + state) → "verifikasi manual untuk kasus batas".
- Dialog tampil di atas screen induk (route sama).
- Screen Akun/Sistem hanya tercatat di modul auth; salinan lain dihapus.

Pakai `--config` agar route baru benar (prefix, strip, root, remove). Periksa 10 baris acak terhadap `routes.tsx` sebelum menyerahkan.

## D. Konvensi nama frame

`{modul}/{bagian}/{#nomor} {Nama} — {state}`; kosakata state tunggal: `default · loading · error · empty · validasi · submit-error · dialog`. Simpan route lama di deskripsi frame.
