# Panduan menulis 04-edge-cases.md

Edge case yang berguna adalah yang menjawab "apa yang terjadi saat…" dengan perilaku yang bisa digambar sebagai frame. Daftar tanpa perilaku atau tanpa frame tidak membantu desainer.

## Format baris (tetap, supaya bisa dihitung script)

```
| EC-XX-NN | Skenario | Perilaku yang diharapkan | Frame | Sev | Dasar |
```

- `EC-XX-NN` — XX = kode area, NN unik di area itu.
- **Sev**: `K` kritis (uang, keamanan, data pasien) · `T` tinggi · `S` sedang · `R` rendah.
- **Dasar**: `P` = terlihat di prototype (screen/state/kode/mock) · `U` = usulan dari pola umum. Pembedaan ini yang membuat dokumen jujur: user tahu mana yang bukti, mana yang saran.
- **Frame**: nomor screen yang harus punya state/dialog untuk kasus itu, atau `baru`.
- Baris harus diakhiri ` | Sev | Dasar |` tanpa kolom tambahan — `edge_summary.py` mengandalkan itu.

## Area (checklist; sesuaikan dengan modul yang ada)

| Kode | Area | Pertanyaan pemicu |
|---|---|---|
| SH | Shell & navigasi | 0/1 modul, badge besar, layar rendah, perubahan belum disimpan saat pindah modul, feature flag |
| AU | Autentikasi & sesi | OTP gagal/dikunci, QR expired/ditolak, akun disuspend, cabut semua sesi, multi-tab, open redirect |
| PM | Permission | role berubah saat login, SoD (peminta ≠ penyetuju ≠ pembayar), super admin terakhir, multi-cabang |
| RT | Migrasi route | URL lama, query string bermakna, entitas terhapus, path ambigu antar modul |
| FM | Form & data | validasi per tab, submit error + idempotency, klik ganda, konflik edit, wizard refresh, error parsial |
| (domain) | Satu area per domain besar | booking/CRM, keuangan, HR/payroll, klinis, inventori, CMS, admin |
| NW | Jaringan, waktu, format | offline, 5xx, timezone, format tanggal campuran, cut-off periode, chunk lazy gagal |

Cari bukti `P` dengan: nama frame berakhiran *gagal/kosong/memuat/validasi*, komentar kode (`// ... SECURITY.md`), enum status, mock data yang janggal (mis. `calculatedBy == approvedBy`), dialog "alasan wajib", header `Idempotency-Key`. Bukti dari mock data adalah temuan paling berharga — sebutkan field-nya.

## Aturan isi

- Perilaku ditulis sebagai keputusan desain konkret ("Composer dinonaktifkan; hanya Kirim template"), bukan "tangani dengan baik".
- Edge case yang butuh kebijakan bisnis (batas budget, status aset hilang) tetap ditulis, tandai **[KEPUTUSAN DIBUTUHKAN]** di kolom perilaku dan kumpulkan di akhir pada bagian `Butuh keputusan produk sebelum didesain`.
- Jangan menggandakan state standar (loading/error/empty) per screen; cukup satu baris umum (EC-FM) kecuali ada perilaku khusus.

## Ringkasan di akhir

Jalankan `python scripts/edge_summary.py 04-edge-cases.md` dan salin angkanya ke tabel "Ringkasan prioritas" plus sebaran severity & dasar. Jangan menghitung manual — hitungan manual sebelumnya meleset di 5 dari 13 baris. Tutup dengan dua bagian yang judulnya memuat persis `Kerjakan dulu (blocker desain)` dan `Butuh keputusan produk sebelum didesain` (kontrak; dibaca skill `plan` Pawang).
