# Menyesuaikan paket dokumen dengan jenis proyek

Empat dokumen tetap sama (PRD, flows, interface designs, edge cases); yang berubah adalah **kerangka isi** dan **cabang yang perlu digrill**. Kerangka di panduan keempat dokumen ditulis untuk ERP/multi-modul — pakai bagian yang relevan, buang yang tidak, dan jangan memaksakan "rail modul" ke proyek yang tidak punya modul.

## Cara memakai tabel ini
1. Tentukan jenis proyek (dari permintaan atau pertanyaan pertama `interview`).
2. Berikan kolom "Cabang yang harus digrill" ke `interview` sebagai konteks awal.
3. Gunakan kolom "Penyesuaian dokumen" saat menulis.

| Jenis | Cabang yang harus digrill | Penyesuaian dokumen |
|---|---|---|
| **ERP / aplikasi internal multi-modul** | peran & izin, pemilik fitur kembar, urutan migrasi, aturan pemisahan tugas, data sensitif | Kerangka penuh. Shell: rail modul + panel menu kedua. Edge case berat di uang, izin, data klinis/pribadi |
| **Konsolidasi prototype** (banyak zip FE) | semua baris di atas + istilah/route lama yang harus tetap hidup | + `inventory.py`, tabel redirect, konflik lintas modul, strategi strangler |
| **Web profile / company profile** | tujuan (kredibilitas, leads, rekrutmen), audiens utama, halaman wajib, siapa yang mengelola konten, bahasa, SEO, CTA utama | PRD: tujuan & metrik konversi, sitemap, model konten. Flows: pengunjung → CTA (kontak/WA/booking), alur admin konten bila ada CMS. Desain: grid halaman, komponen section, responsif mobile-first. Edge case: form kontak spam/gagal, bahasa ganda, gambar besar, halaman kosong |
| **Web bisnis / landing page / e-commerce** | penawaran & harga, funnel, pembayaran, pengiriman/stok, retur, analitik, kepatuhan (pajak/privasi) | Flows: funnel penuh (landing → pilih → bayar → konfirmasi → pasca-beli). Edge case berat di pembayaran, stok, kupon, pembatalan |
| **Aplikasi mobile/web konsumen** | persona, aktivitas inti (job-to-be-done), onboarding, notifikasi, mode offline, monetisasi | Flows: onboarding, aktivitas inti, pemulihan akun. Edge case: izin perangkat, jaringan buruk, sinkronisasi, akun ganda |
| **Dashboard / internal tool kecil** | siapa memutuskan apa dari data ini, sumber data, kesegaran, ekspor | Satu-dua flow; edge case: data kosong/terlambat/salah satuan |
| **Proyek lain** | mulai dari tujuan, pengguna, scope, kegagalan yang paling mahal | Pilih bagian kerangka yang cocok; nyatakan penyesuaian di PRD |

## Aturan penyesuaian
- Jangan menampilkan bagian kosong demi kelengkapan; hapus dan jangan menggantinya dengan teks generik.
- Tetap pertahankan: penanda **[ASUMSI]** / **[KEPUTUSAN DIBUTUHKAN]**, tabel "Keputusan terbuka", bukti P/U di edge case, dan validasi Mermaid.
- Jika user menolak menjawab cabang tertentu di `interview`, jangan menutupinya: tulis sebagai keputusan terbuka dan jelaskan dampaknya pada dokumen terkait.
