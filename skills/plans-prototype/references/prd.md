# Panduan menulis 01-PRD.md

Tujuan: dokumen yang bisa di-*paste* ke Figr ("PRDs and Docs") dan tetap bisa dipertanggungjawabkan ke tim engineering. Itu sebabnya tiap angka harus bisa ditelusuri ke hasil `inventory.py`, dan tiap keputusan yang belum dibuat user ditandai, bukan diputuskan diam-diam.

## Kerangka (urutan tetap)

Heading bertanda *(kontrak)* harus memuat teks persis seperti tertulis; kerangka selengkapnya ada di templat `assets/templates/01-PRD.md`. Bagian lain boleh dihapus bila jenis proyek tidak membutuhkannya.

1. **Ringkasan** *(kontrak)* — satu paragraf: dari berapa aplikasi menjadi apa. Sebut tiga janji: satu shell, satu design system/primitives, satu auth+akun.
2. **Masalah (kondisi saat ini)** — tabel per modul: frame, screen unik, lebar rail, warna rail, lebar panel list (ambil dari `summary.md`). Lalu daftar akar masalah, masing-masing dengan bukti kode (mis. "Button ada di 8 modul dengan signature berbeda").
3. **Tujuan dan non-tujuan** *(kontrak)* — beri ID (G1..). Non-tujuan wajib ada: menolak micro-frontend runtime, redesign visual besar, backend sungguhan — kecuali user menginginkannya. Ini mencegah scope melebar.
4. **Pengguna dan peran** *(kontrak)* — hanya peran yang benar-benar terlihat di kode (mis. `Role = "cs" | "admin" | "hr"`), tandai "bukan daftar final".
5. **Arsitektur target** — struktur folder, kontrak `manifest.ts` (tipe TypeScript), aturan modul (tidak saling import; lazy route; satu router).
6. **Shell: rail modul + panel menu kedua** — diagram kolom ASCII, tabel ≤8 ikon (modul, ikon lucide, sumber), perilaku (permission, rute terakhir, badge teragregasi, breakpoint, a11y).
7. **Pemetaan modul** — tabel basepath + menu panel kedua per modul + **tabel redirect** URL lama → baru.
8. **Konflik yang harus diselesaikan** — tabel C1..Cn: konflik · bukti (nomor screen) · rekomendasi · status (`Wajib`/`Usulan`/`[KEPUTUSAN DIBUTUHKAN]`).
9. **Requirement fungsional** *(kontrak; FR-n, tiap baris tepat satu prioritas P0–P2)* dan **Requirement non-fungsional** *(kontrak; NFR-n)*.
10. **Strategi migrasi** — strangler, urut modul kecil → besar; diagram Mermaid `flowchart LR` per fase + tabel "selesai bila".
11. **Risiko dan trade-off** — R1..; sertakan hitung lebar (rail+panel2+list) bila ada panel list.
12. **Keputusan terbuka** *(kontrak; Q1..)* dan **Metrik keberhasilan** *(kontrak; sekarang → target)*.

Tambahkan daftar isi bila >5 bagian.

## Cara memilih isi ikon rail (≤8)

- Satu ikon per modul domain. Auth **bukan** ikon (login di luar shell; akun lewat avatar).
- Notifikasi, Pengumuman, Avatar di bagian bawah rail, bukan modul.
- Bila jumlah modul domain < batas, boleh menambah "Beranda" (dashboard lintas modul) — tandai **[ASUMSI]** dan masukkan ke keputusan terbuka. Jangan membulatkan ke 8 dengan memecah modul tanpa alasan domain.

## Pola konflik yang hampir selalu muncul (cek satu per satu)

| Pola | Cara mendeteksi | Sikap default |
|---|---|---|
| Fitur sama di dua modul (booking, payroll) | `feature_overlap` di summary + nama screen identik | Satu pemilik; modul lain deep link |
| Salinan halaman Akun/Sistem | section `akun`/`sistem`, screen #7–#17 | Satu global `/akun/*`, `/403`, `/404`, `/error` |
| Tabrakan route (`/dashboard`, `/master`) | `route_collisions` | Namespace `/modul/...` + tabel redirect |
| Auth tidak konsisten | cari komentar `SECURITY.md`, screen Login | Ikuti modul auth; hapus yang lain, tandai **Wajib** |
| Panel list lebar vs panel menu baru | `panel_widths` | Hitung sisa lebar per viewport; usul collapse/overlay |
| Data yang sama dimiliki dua modul (tenaga, pasien, mitra) | kata kunci sama di section | Satu sumber kebenaran + link by ID |

## Aturan penulisan

- Semua angka berasal dari script. Jika dikoreksi belakangan (mis. salinan akun 7 bukan 8), cari-ganti di **seluruh** dokumen, termasuk tabel metrik.
- Tandai: **[ASUMSI]** (saya menyimpulkan), **[KEPUTUSAN DIBUTUHKAN]** (user harus memilih), **Wajib** (bertentangan dengan kebijakan keamanan yang tertulis di kode).
- Sertakan rekomendasi bila ada, tetapi jangan menyamarkannya sebagai fakta.
- Jangan menyarankan CSV sebagai sumber data inventaris; cukup Markdown + Mermaid (preferensi user).
