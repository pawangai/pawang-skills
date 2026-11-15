# Blueprint SEO, AEO, dan GEO

Baca file ini hanya saat user meminta blueprint visibilitas. Semua fakta bisnis wajib dari user; bila tidak ada, pakai `[ISI: ...]`.

## Daftar isi
- SEO
- AEO
- GEO
- Cek akhir

## SEO
- Primary keyword (1-2) dan long-tail keyword (5-8) sesuai niche dan lokasi. Jangan menyebut volume pencarian kecuali user memberi data.
- Meta Title maksimal 60 karakter, Meta Description maksimal 155 karakter. Hitung dengan `python3 scripts/check_theme.py count meta-title "teks"` (atau `meta-description`) sebelum menyajikan, dan tulis jumlahnya di samping.
- Hierarki heading semantik: satu `H1` (memuat keyword utama), `H2` per pilar layanan, `H3` untuk rincian.

## AEO
- Definisi entitas lugas sebagai kalimat pembuka halaman: "[Nama Brand] adalah [definisi dan solusi utama] untuk [target audiens]." Satu kalimat, tanpa superlatif.
- 3-5 FAQ. Tiap jawaban 40-60 kata, langsung menjawab di kalimat pertama, dan berdiri sendiri (tidak bergantung pada pertanyaan lain). Hitung dengan `python3 scripts/check_theme.py count faq "jawaban"` sebelum menyajikan.

## GEO
- Pernyataan nilai unik dalam poin faktual dan eksplisit, satu klaim per poin, agar mudah dipahami dan direkomendasikan AI generatif. Klaim yang belum ada datanya ditulis `[ISI: ...]`.
- Konteks semantik: setiap bagian utama mengaitkan nama brand, masalah yang diselesaikan, dan lokasi atau target pasar.

## Cek akhir
- Batas karakter meta terpenuhi.
- Setiap FAQ 40-60 kata.
- Tidak ada angka, kredensial, atau klaim yang tidak berasal dari user.
