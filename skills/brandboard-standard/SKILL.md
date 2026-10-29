---
name: brandboard-standard
description: Membuat, menyusun, atau mengaudit brand board / brand guideline satu halaman dengan struktur section yang standar (hero, variasi logo, palet warna, tipografi, gaya bahasa, contoh penerapan, footer, maskot, ikon, pola background, dll). Punya dua cakupan - bertingkat (default) dan lengkap (semua section terisi). Gunakan skill ini setiap kali user minta dibuatkan brand board, brand guideline, brand identity sheet, style guide visual, prompt gambar untuk brand board, atau minta brand board baru "disamakan formatnya" dengan brand lain, termasuk saat user hanya menyebut nama brand baru dan minta "bikinin board-nya". Juga gunakan untuk membandingkan atau mengecek kelengkapan brand board yang sudah ada terhadap standar, walau user tidak menyebut kata "standar".
license: MIT
compatibility: "Tanpa dependensi khusus. Prompt gambar dipakai di tool image generation pilihan user. Memanggil skill interview untuk keputusan yang belum jelas."
metadata:
  author: "Pawang"
---

# Brand Board Standard

Skill ini membuat setiap brand board memakai kerangka section yang sama, sehingga brand yang berbeda (karakter, warna, tone berbeda) tetap bisa dibandingkan, di-review, dan di-handoff dengan cara yang sama.

Standar ini diturunkan dari analisis 4 board referensi (Pawang.dev, DukunKode, Gus Kode, Ning Kode). Tiap board kuat di area berbeda, jadi standar ini menggabungkan yang terbaik dari masing-masing. Kerangka (apa yang harus ada) distandarkan; bentuk ekspresinya sengaja dibiarkan bervariasi, karena keempat referensi berasal dari genre yang mirip dan kebetulan berbagi pola hero yang sama. Spesifikasi lengkap tiap section ada di `references/section-spec.md`.

## Kenapa standar ini ada

Tanpa kerangka tetap, board baru cenderung melewatkan section yang tidak terpikir saat itu (versi logo gelap, font kode, microcopy untuk state error). Hasilnya brand tidak bisa dipakai konsisten oleh tim lain. Kerangka tetap memaksa pertanyaan yang sama diajukan ke setiap brand.

## Pilih cakupan: bertingkat atau lengkap

Ada dua cakupan. **Default-nya bertingkat.** Pakai cakupan lengkap hanya jika user menyatakannya secara eksplisit (misalnya "mode lengkap", "semua section", "full", "isi semuanya"). Bila user tidak menyebut apa pun, gunakan bertingkat dan jangan bertanya.

| | Bertingkat (default) | Lengkap |
|---|---|---|
| Tier 1 (7 section) | Wajib | Wajib |
| Tier 2 (7 section) | Hanya jika brand punya elemennya | Wajib, pakai versi minimal bila brand tidak punya |
| Tier 3 (2 section) | Hanya jika relevan | Wajib, pakai versi minimal bila tidak relevan |
| Section dilewati | Dicatat beserta alasannya | Tidak ada |
| Cocok untuk | Brand yang sudah punya identitas jelas, board ringkas | Template seragam lintas brand, dokumentasi menyeluruh |

Di cakupan lengkap, setiap section punya "versi minimal" (lihat `references/section-spec.md`) supaya tidak terasa dipaksakan: isinya diturunkan dari logo, tagline, dan bidang usaha, bukan mengarang elemen yang tidak cocok. Section yang seluruh isinya turunan ditandai `[ASUMSI]` satu kali di judul section, bukan per baris (lihat aturan penandaan di bawah).

## Tiga mode kerja

Tentukan mode dari permintaan user, lalu ikuti alurnya. Cakupan (bertingkat/lengkap) berlaku di ketiganya.

### Mode A: Buat brand board baru

1. **Kumpulkan brief minimum.** Cek dulu apa yang sudah ada di percakapan, jangan tanya ulang. Yang dibutuhkan:
   - Nama brand dan tagline (atau nilai inti brand)
   - Bidang usaha dan target audiens
   - Karakter/tone (misalnya hangat, misterius, formal) dan kalau ada, konsep budaya atau maskot
   - Preferensi warna (opsional, bisa diusulkan)
   Bila ada keputusan penting yang belum ada (karakter brand, target audiens, cakupan), panggil skill `interview` dalam mode ringan sebelum menulis Brand Spec. Detail kecil (misalnya usulan palet) boleh diisi dengan asumsi yang ditulis eksplisit sebagai `[ASUMSI]`.
2. **Tentukan cakupan** (default bertingkat) dan, bila bertingkat, pilih section Tier 2/3 yang relevan.
3. **Pilih Hero archetype** (Pilar, Manifesto, Bukti, Sapaan, atau Minimal; lihat `references/section-spec.md` bagian 2.1) berdasarkan karakter brand, lalu tulis alasannya dalam satu kalimat di Ringkasan Brand Spec. Bila karakter brand tidak cukup untuk memilih satu archetype, tanyakan lewat `interview` mode ringan dengan rekomendasi. Jangan memilih Pilar secara otomatis: Pilar hanya dipakai bila brand memang punya beberapa nilai setara. Bila user memberikan beberapa brand dalam satu sesi atau satu set, jangan pakai archetype yang sama berurutan kecuali user memintanya.
4. **Hasilkan Brand Spec** memakai `assets/brand-spec-template.md`. Ini dokumen Markdown yang mengisi setiap section, dan menjadi sumber kebenaran tunggal.
5. **Hasilkan prompt gambar** (satu prompt per board) yang diturunkan dari Brand Spec, mengikuti "Layout kanvas" di `references/section-spec.md`. Claude tidak menggambar board-nya sendiri, jadi prompt ini yang dipakai di tool image generation pilihan user.
6. **Jalankan checklist QA** sebelum menyerahkan hasil.

### Mode B: Audit board yang sudah ada

1. Petakan isi board ke daftar section standar (16 section). Tanpa permintaan khusus, nilai terhadap cakupan bertingkat; bila user minta lengkap, semua 16 section dihitung wajib.
2. Keluarkan tabel: section, status (✅ lengkap / ⚠️ parsial / ❌ tidak ada), dan catatan kekurangan spesifik (misalnya "tipografi tidak punya font kode").
3. Urutkan temuan: Tier 1 yang hilang dulu, lalu kelengkapan isi, lalu Tier 2 dan 3.
4. Tawarkan membuat patch Brand Spec yang menambal gap tersebut.

### Mode C: Samakan beberapa board

Jalankan Mode B pada tiap board, tampilkan matriks perbandingan, lalu usulkan section yang perlu ditambahkan ke masing-masing.

## Struktur standar (ringkas)

Urutan, penomoran, dan daftar section ini tetap antar brand, supaya pembaca selalu tahu di mana mencari sesuatu. Satu section = satu topik, tidak ada section yang digabung. Yang boleh berubah per brand adalah bentuk ekspresi di dalam section (misalnya Hero archetype), bukan kerangkanya.

### Tier 1: Wajib di semua board, di kedua cakupan

| # | Section | Isi minimum |
|---|---|---|
| 1 | Hero | Logo utama, tagline, ilustrasi/visual utama, satu kalimat pendamping, satu penanda nilai (bentuk dipilih lewat Hero archetype) |
| 2 | Variasi Logo | Horizontal, vertikal, ikon/app icon, minimalis, **versi gelap**, favicon |
| 3 | Palet Warna | Minimal 4 warna; tiap warna punya **nama, hex, dan peran** |
| 4 | Tipografi | 3 peran: judul, isi, kode/teknis; tiap font diberi label penggunaan dan contoh |
| 5 | Gaya Bahasa | Deskripsi tone, contoh kutipan, microcopy per konteks UI, checklist prinsip |
| 6 | Contoh Penerapan | Minimal 3 konteks nyata |
| 7 | Footer | Logo kecil, deskripsi satu baris, tagline |

### Tier 2: Kondisional di bertingkat, wajib di lengkap

| # | Section | Kondisi di cakupan bertingkat |
|---|---|---|
| 8 | Filosofi | Brand dijual berdasarkan cerita atau positioning |
| 9 | Nilai Brand | Brand punya nilai yang dikomunikasikan ke audiens |
| 10 | Maskot | Brand punya karakter |
| 11 | Set Ikon | Brand memakai set ikon sendiri |
| 12 | Elemen Visual | Brand memakai ornamen atau motif budaya |
| 13 | Pola Background | Brand memakai pola latar |
| 14 | Aset Tambahan | Ada properti pendukung |

### Tier 3: Modul bisnis, opsional di bertingkat, wajib di lengkap

| # | Section | Kondisi di cakupan bertingkat |
|---|---|---|
| 15 | Layanan | Brand menjual jasa/produk bernama |
| 16 | Paket | Layanan punya paket |

## Aturan penulisan Brand Spec

- Gunakan Markdown. Bila perlu menampilkan alur atau hierarki, gunakan diagram Mermaid. Jangan menyarankan CSV sebagai sumber data, karena Markdown sudah cukup sebagai sumber kebenaran tunggal.
- Tulis dalam bahasa yang dipakai user (default Bahasa Indonesia). Istilah teknis tetap dalam bentuk aslinya (hex, favicon, microcopy).
- Pertahankan nama section dari board referensi: "Palet Warna", "Tipografi", "Gaya Bahasa", "Contoh Penerapan", "Variasi Logo".
- Setiap nilai warna ditulis sebagai `#RRGGBB`. Setiap font ditulis dengan nama persis dan peran.
- Sebutkan pasangan warna teks-latar yang aman untuk body text (target rasio kontras minimal 4.5:1) di kolom peran palet.
- Jangan mengarang fakta bisnis (harga, nama layanan, klaim) yang tidak diberikan user. Bila terpaksa mengisi, tandai `[ASUMSI]` supaya mudah dicari dan dikonfirmasi.
- **Aturan penandaan `[ASUMSI]`:** tandai di **tingkat section** bila seluruh isi section itu turunan atau versi minimal, dengan menaruhnya di judul (contoh: `### 10. Maskot [ASUMSI]`). Tandai di **tingkat baris atau kalimat** hanya untuk satu fakta spesifik di dalam section yang selebihnya berasal dari user atau brief (contoh: janji "dalam 1 hari kerja" di email konfirmasi, atau satu nama layanan yang belum disetujui). Jangan menandai setiap baris tabel di section yang sudah ditandai di judulnya. Ringkasan akhir cukup menyebut daftar section bertanda dan fakta spesifik bertanda.
- Bila brand memakai unsur budaya atau agama (batik, kawung, lencana, istilah religi), jaga agar penggunaannya hormat dan tidak merendahkan. Tanyakan bila ragu, jangan berasumsi.

## Format prompt gambar

Prompt gambar harus mandiri (bisa ditempel langsung) dan berisi, berurutan: format kanvas, gaya ilustrasi, daftar section dengan isinya, palet dengan hex, dan larangan (misalnya "tanpa teks acak", "teks harus terbaca").

**Dua urutan yang berbeda, jangan dicampur:**
- **Brand Spec** mengikuti urutan nomor section (1, 2, 3, ... 16).
- **Prompt gambar** mengikuti urutan layout kanvas, yaitu baris demi baris dari atas ke bawah: 1, 2, 10, 14, 11, 12, 3, 4, 5, 6, 13, 8, 9, 15, 16, lalu 7 (Footer) paling akhir. Di cakupan bertingkat, lewati nomor yang tidak dipakai tanpa mengubah urutan sisanya.
- Beri awalan nomor standar di tiap section dalam prompt (contoh: `[10] Maskot: ...`), supaya jelas section mana yang dimaksud walau urutannya berbeda dari nomor. Tulis semua teks yang harus muncul di gambar secara persis, karena model gambar cenderung salah mengeja teks yang dibiarkan bebas.

Sarankan user memperlakukan hasil gambar sebagai draf visual, dan Brand Spec Markdown sebagai sumber kebenaran untuk hex, nama font, dan copy.

## Checklist QA sebelum menyerahkan hasil

- [ ] Cakupan yang dipakai (bertingkat/lengkap) disebut di awal Brand Spec
- [ ] Semua 7 section Tier 1 ada dan memenuhi isi minimum
- [ ] Hero memuat satu penanda nilai sesuai archetype terpilih, dan alasan pemilihannya tercatat di Ringkasan
- [ ] Penanda nilai Hero tidak diulang persis di Footer atau Nilai Brand
- [ ] Setiap warna punya nama, hex, dan peran
- [ ] Tipografi punya font kode dan label penggunaan tiap font
- [ ] Ada versi logo gelap dan favicon
- [ ] Gaya bahasa memuat microcopy untuk minimal: hero, CTA, loading, sukses, error 404, email konfirmasi
- [ ] Urutan dan penomoran section sesuai standar
- [ ] Cakupan lengkap: ke-16 section terisi, tidak ada yang kosong
- [ ] Cakupan bertingkat: section yang dilewati dicatat beserta alasannya
- [ ] Asumsi ditandai sesuai aturan: per section di judul bila seluruhnya turunan, per baris hanya untuk fakta tunggal; tidak ada tanda ganda di dalam section yang sudah bertanda
- [ ] Ringkasan akhir menyebut daftar section dan fakta yang bertanda `[ASUMSI]`

## Format balasan ke user

Mulai dengan hasil (Brand Spec atau tabel audit), lalu tutup dengan daftar singkat asumsi dan hal yang perlu dikonfirmasi. Jangan mengulang isi spesifikasi di chat jika sudah ada di file.
