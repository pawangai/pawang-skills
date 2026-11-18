---
name: make-theme
description: Merancang tema brand end-to-end, yaitu metafora inti, tone of voice, aturan diksi, palet warna HEX dengan cek kontras, tipografi, maskot, tagline, pilar layanan, dan tier paket. Opsional menambah elemen dekoratif (props dan ilustrasi pendukung), blueprint SEO/AEO/GEO dan kode tema (CSS variables, Tailwind, CLAUDE.md). Gunakan saat user minta membuat tema, rebranding, identitas visual, palet warna, tagline, atau sistem desain untuk website, bisnis, atau personal branding, walau tidak menyebut kata tema. Padanan Inggris, brand theme, design tokens, visual identity. Jangan gunakan untuk dokumen panduan brand berformat Markdown (pakai panduan-brand) atau audit SEO murni.
license: MIT
compatibility: "Python 3 tanpa paket tambahan untuk scripts/check_theme.py. Memanggil skill interview untuk discovery; bila tidak ada, tanya langsung. Belum diuji lintas model."
metadata:
  author: "Pawang"
---

# Make Theme

Tujuan: mengubah ide abstrak user menjadi tema brand yang konsisten dan siap diterapkan. Tema yang kuat berangkat dari satu metafora yang dipegang di seluruh keluaran (bahasa, warna, maskot, nama layanan), bukan dari daftar elemen yang berdiri sendiri.

Batas dengan `panduan-brand`: skill ini merancang tema dan token yang bisa langsung dipakai di desain atau kode. `panduan-brand` menulis dokumen panduan brand lengkap sebagai berkas `.md`. Bila user minta dokumen panduannya, kerjakan tema di sini lalu arahkan ke `panduan-brand`, atau sebaliknya bila user hanya mau dokumen.

## Aturan keras

1. **Jangan mengarang fakta bisnis.** Angka, tahun berdiri, kredensial, testimoni, harga, lokasi, dan klaim "terbaik" hanya boleh dipakai bila diberikan user. Bila belum ada, tulis `[ISI: ...]`. Alasannya, teks yang dipublikasikan dan dikutip mesin AI dengan fakta karangan merugikan brand dan sulit dilacak.
2. **Nada solutif dan tenang.** Hindari kata klise dan kata yang menakut-nakuti (misalnya "bahaya", "rugi besar", "jangan sampai"). Fokus pada solusi dan rasa aman.

## Mode keluaran

- **Default (ringkas):** komponen 1-3.
- **Lengkap:** tambah komponen 4 (SEO/AEO/GEO) dan 5 (kode) bila user memintanya; tawarkan di akhir sesi.
- Bila user hanya minta satu bagian (misalnya palet saja), kerjakan bagian itu saja.
- Elemen dekoratif (props, ilustrasi pendukung, pola latar) dikerjakan hanya bila user meminta maskot, ikonografi, atau tema lengkap. Jangan dibuat pada permintaan palet saja.

## Alur

### 1. Discovery
Bila user sudah memberi konsep awal, petakan langsung ke struktur tema tanpa mengulang pertanyaan dasar. Bila ada keputusan yang belum ada, panggil skill `interview` mode ringan (maksimal 3-4 pertanyaan, tiap pertanyaan dengan rekomendasi jawaban). Bila `interview` tidak tersedia, tanyakan langsung dengan format yang sama. Yang perlu diketahui:
- Niche dan target audiens.
- Metafora yang sudah terpikir. Bila belum, tawarkan 2-3 pilihan.
- Kesan yang diinginkan (tenang, hangat, tegas, jenaka).
- Stack yang dipakai, hanya bila komponen 5 diminta.

### 2. Metafora dan suara
Terjemahkan ide user menjadi satu metafora yang dekat dengan masalah klien; tidak harus profesi tradisional. Uji: apakah metafora bisa dipakai untuk menamai layanan, menyapa klien, dan menggambar maskot? Bila tidak, terlalu dangkal. Contoh di `references/contoh-tema.md`.

### 3. Sistem visual
Pilih warna dan font setelah metafora jelas. Hitung kontras dengan skrip, jangan menebak:
```
python3 scripts/check_theme.py contrast "Nama=#HEX" "Nama=#HEX" ...
```
Teks minimal 4,5:1 (WCAG AA). Pasangan yang gagal ditulis sebagai larangan eksplisit di tema.

Bila maskot, ikonografi, atau tema lengkap diminta, baca `references/elemen-dekoratif.md` dan turunkan props dari metafora, bukan memilihnya acak.

### 4. Layanan dan copywriting
Pecah tema menjadi pilar layanan dan tier paket yang namanya mengikuti metafora. Tulis tagline utama beserta alternatif per konteks, dan draf siap pakai.

### 5. Opsional: SEO/AEO/GEO dan kode
Baca `references/seo-aeo-geo.md` bila komponen 4 diminta, dan `references/implementasi.md` bila komponen 5 diminta. Hasilkan hanya format yang cocok dengan stack user.

## Format keluaran

### 1. Identitas dan filosofi
- Nama brand atau proyek
- Metafora utama dan alasannya (1-2 kalimat)
- Tone of voice: 3-4 sifat, masing-masing dengan satu kalimat contoh
- Aturan diksi: minimal 5 kata dianjurkan dan 5 dilarang, masing-masing dengan pengganti

### 2. Sistem visual
| Nama | HEX | Peran UI | Makna | Kontras |
|---|---|---|---|---|

Peran minimal: Primary, Accent/CTA, Background, Support, Text. Kolom kontras berisi hasil skrip untuk pasangan yang dipakai bersama.
- Tipografi: Heading dan Body dari Google Fonts dengan fallback stack. Pastikan mendukung karakter Latin lengkap. Monospace hanya bila relevan.
- Aset visual: konsep logo, maskot atau ikonografi, dan satu kalimat larangan visual.
- Elemen dekoratif (bila diminta): tabel 3-5 props beserta makna, lapisan, dan penempatan, serta token gaya, sesuai `references/elemen-dekoratif.md`. Berupa spesifikasi, bukan gambar jadi.

### 3. Layanan dan penawaran
- Pilar layanan: nama sesuai metafora, satu kalimat solusi.
- Tier paket dengan nama kontekstual. Harga hanya bila diberikan user, selain itu `[ISI: harga]`.
- Tagline utama, 3 alternatif (website, bio media sosial, iklan), headline hero, bio media sosial, sapaan WhatsApp.

### 4. SEO/AEO/GEO (bila diminta)
Ikuti `references/seo-aeo-geo.md`.

### 5. Implementasi (bila diminta)
Ikuti `references/implementasi.md`.

## Kasus tepi

- Hanya ada nama brand tanpa konteks: jalankan discovery, jangan menebak niche.
- Brand sudah punya identitas: tanyakan apa yang dipertahankan (logo, warna, nama) sebelum merancang ulang.
- Data bisnis kurang untuk komponen 4: pakai `[ISI: ...]`, jangan melengkapi dengan perkiraan.
- Python tidak tersedia: hitung kontras dengan rumus WCAG secara manual dan tandai hasilnya sebagai perkiraan.

## Kesalahan umum

- Metafora berganti-ganti antar bagian.
- Warna cantik tetapi kontras teks di bawah 4,5:1.
- Angka, kredensial, atau testimoni yang dikarang.
- Lima komponen ditulis padahal user hanya butuh palet.
- Meta title atau description melebihi batas karakter karena tidak dihitung.
- Dekorasi ditambahkan tanpa makna atau melebihi batas, sehingga tampil ramai dan generik.
