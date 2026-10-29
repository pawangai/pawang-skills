---
name: pawang-skill-creator
description: Membuat, mengaudit, dan memperbaiki skill berformat Agent Skills (folder berisi SKILL.md). Gunakan saat user ingin membuat skill baru, mereview atau merapikan SKILL.md, atau memperbaiki skill yang tidak terpicu, termasuk bila user hanya bilang buatkan skill. Jangan untuk menulis AGENTS.md (tugas agents-md) dan jangan untuk prompt sekali pakai.
compatibility: Python 3 untuk scripts/validate_skill.py (PyYAML opsional). Panduan pengujian lintas model belum diuji pada model tertentu.
license: MIT
metadata:
  author: "Pawang"
---

# Skill Creator (Agent Skills)

**Context reuse:** Reuse any required file already loaded in project instructions or the current session. Read it again only if absent, changed, or exact current bytes or line references are needed.

Tujuan: menghasilkan skill yang terpicu pada saat yang tepat, mudah diikuti agent, hemat konteks, dan berjalan di agent mana pun yang mendukung format Agent Skills.

Skill = folder dengan `SKILL.md` (frontmatter + instruksi) dan sumber daya opsional. Agent hanya melihat `name` + `description` sampai skill terpicu, baru membaca isi SKILL.md, dan baru membuka file lain bila instruksinya menyuruh. Seluruh desain di bawah mengikuti urutan biaya itu.

## Prinsip

1. **Description adalah mesin pemicunya.** Isi yang bagus dengan description lemah sama dengan skill yang tidak ada. Panduan rinci: `references/description-guide.md`.
2. **Desain untuk keluarga tugas, bukan satu contoh.** Skill dipakai ribuan kali dengan prompt berbeda. Jangan menanam nama proyek, file, atau nilai contoh sebagai aturan.
3. **Jelaskan alasannya.** Agent yang paham tujuan aturan bisa menggeneralisasi; agent yang hanya melihat MUST/NEVER menjadi kaku atau salah tafsir. Pakai huruf kapital hanya untuk satu atau dua aturan yang benar-benar tidak boleh dilanggar.
4. **Hemat konteks.** Inti di SKILL.md (idealnya di bawah 500 baris), detail yang jarang dibutuhkan di `references/`, hal deterministik di `scripts/`. Rujukan satu tingkat saja (SKILL.md → file), jangan berantai.
5. **Skrip untuk yang deterministik.** Validasi, konversi, dan hitung-hitungan lebih andal sebagai kode daripada instruksi, dan hasilnya tidak perlu ditulis ulang agent tiap kali.
6. **Setiap baris harus mengubah perilaku.** Baris yang hasilnya sama saat dihapus adalah beban token. Uji, lalu pangkas.
7. **Portabel secara default.** Pakai hanya field spesifikasi: `name`, `description`, opsional `license`, `compatibility`, `metadata`. Field khusus satu agent (misalnya pengaturan invokasi di Claude Code) dan `allowed-tools` (eksperimental) hanya ditambahkan bila user menargetkan agent itu saja, dan dicatat sebagai pengurang portabilitas.
8. **Padat tanpa kehilangan makna.** Saat menulis atau memadatkan teks, pangkas pengulangan, kata pengantar, dan kalimat yang hanya menegaskan ulang. Pertahankan setiap aturan dan larangan beserta syaratnya, urutan langkah, dan arti kalimat; jangan menggabungkan dua aturan yang syaratnya berbeda. Pertahankan persis nama perintah, path, nilai, kunci, string kontrak, dan semua teks dalam backtick. Jangan menerjemahkan sambil memadatkan. Bila ragu sebuah kalimat penting, pertahankan. Tinjau diff hasilnya sebelum dipakai.

## Mode

Tentukan mode dari permintaan user; kalau ambigu, tebak yang paling mungkin dan nyatakan asumsinya.

- **Buat baru**: ikuti Proses di bawah.
- **Review/audit**: jalankan `scripts/validate_skill.py`, nilai dengan `references/review-rubric.md`, laporkan sesuai format di sana. Jangan menulis ulang kecuali diminta.
- **Perbaiki/iterasi**: baca skill yang ada dan hasil uji atau keluhan user, ubah sedikit mungkin, uji ulang. Jangan merancang ulang dari nol bila masalahnya hanya description.

## Proses (buat baru)

### 1. Tangkap maksud
Mulai dari percakapan: kalau user bilang "jadikan ini skill", ekstrak langkah, koreksi yang pernah user berikan, format input dan output yang sudah terlihat. Lalu tanyakan hanya yang masih kurang, maksimal 3 pertanyaan sekaligus:
- Kemampuan apa yang harus dimiliki dan keluaran apa yang dihasilkan?
- Kapan harus aktif (frasa user, jenis file, konteks)? Kapan TIDAK?
- Agent mana yang dipakai (menentukan lokasi dan field, lihat langkah 6)?
Input, kriteria sukses, dan tool yang dibutuhkan disimpulkan dulu; tanya hanya bila tidak bisa disimpulkan. Jangan menebak keputusan yang mengubah arsitektur skill.

### 2. Pilih pola isi
Satu skill boleh menggabungkan pola, tetapi mulai dari yang paling sederhana.

| Pola | Pakai bila | Ciri |
|---|---|---|
| Workflow berurutan | Langkah pasti, urutan penting | Langkah bernomor dengan kriteria selesai |
| Router | Satu bidang, banyak jalur | Tabel "jika X → baca `references/<topik>.md`" |
| Template keluaran | Format hasil harus konsisten | Template + satu contoh nyata |
| Checklist/validasi | Kualitas harus diverifikasi | Daftar cek yang bisa dijawab ya/tidak |
| Checklist progres | Proses panjang dan urutan penting (misalnya data harus dicek sebelum laporan dibuat) | Daftar langkah yang disalin agent ke balasannya dan dicentang satu per satu, plus langkah balik |
| Loop koreksi | Keluaran harus lolos standar (gaya, brand voice, validator) | Kerjakan, cek, perbaiki, ulangi sampai lolos |
| Skrip bantu | Bagian deterministik | `scripts/` dengan petunjuk pemakaian dan keluaran yang jelas |

**Checklist progres.** Tulis lima sampai tujuh baris berisi tujuan tiap langkah, bukan perintah kaku, dengan satu paragraf pendek di bawah tiap langkah. Langkah verifikasi di akhir harus punya langkah balik, misalnya "bila sitasi belum lengkap, kembali ke langkah 3"; tanpa itu agent cenderung mencentang langkah yang gagal lalu lanjut. Jangan pakai checklist bila urutan tidak penting.

**Loop koreksi.** Pengecekan tidak harus kode: bisa style guide, dokumen brand voice, atau skrip validator. Pola: buat draf, cek terhadap standar dan catat tiap pelanggaran beserta bagiannya, revisi, cek ulang, dan finalkan hanya bila semuanya lolos. Tambahkan juga satu baris: bila draf gagal karena alasan yang belum ada di dokumen standar, agent mengusulkan aturan baru di akhir proses, dan aturan itu masuk dokumen hanya setelah user menyetujui. Dengan begitu skill membaik dari pemakaian.

### Tentukan tingkat kebebasan per langkah
Detail instruksi mengikuti seberapa rapuh langkahnya dan seberapa besar variasi yang wajar. Nilai tiap langkah, bukan skill secara keseluruhan; satu skill boleh mencampur tingkat (misalnya menulis isi invoice bebas, membuat invoicenya terkunci).

| Tingkat | Bentuk | Cocok untuk |
|---|---|---|
| Tinggi | Instruksi berupa tujuan dan kriteria | Banyak jalur yang benar, tergantung konteks (review kode, menulis post, menilai panggilan penjualan) |
| Sedang | Template dengan parameter atau variasi yang diizinkan | Ada bentuk yang disukai tetapi variasi aman (laporan mingguan, ringkasan klien) |
| Rendah | Skrip atau perintah persis, parameter minim atau nol | Rapuh atau berdampak besar: migrasi database, uang, penghapusan data, urutan yang tidak boleh berubah |

Pertanyaan penentu untuk tiap langkah: "apa yang terjadi bila agent mengerjakannya dengan cara berbeda?" Bila hasilnya hampir sama, longgarkan. Bila ada akibat serius, kunci. Tingkat rendah biasanya berarti skrip di `scripts/`, bukan teks yang lebih panjang, karena skrip berjalan sama di model apa pun.

Kalau dua tugas punya pemicu berbeda dan alur berbeda, buat dua skill, bukan satu skill dengan banyak mode. Satu skill = satu kemampuan yang bisa dijelaskan dalam satu kalimat.

### 3. Rancang struktur folder
```
nama-skill/
├── SKILL.md          # wajib
├── references/       # dibaca sesuai kebutuhan (panduan, rubrik, skema)
├── scripts/          # dieksekusi, bukan dibaca (validasi, konversi)
└── assets/           # template atau file yang dipakai di keluaran
```
Buat folder hanya yang dipakai. Tidak perlu `README.md` atau `CHANGELOG.md` di dalam folder skill. Setiap file di `references/` dan `scripts/` harus dirujuk dari SKILL.md dengan kapan dibaca atau dijalankan, kalau tidak agent tidak tahu file itu ada. Referensi di atas 100 baris WAJIB diawali daftar isi (satu baris per heading utama) di bagian paling atas. Alasannya, agent sering hanya membaca sekitar 100 baris pertama untuk memutuskan apakah file itu berguna, jadi heading di bawah batas itu tidak terlihat; dengan daftar isi agent bisa membaca semuanya atau langsung lompat ke bagian yang dibutuhkan. Semua file referensi ditautkan langsung dari SKILL.md; file referensi tidak boleh menautkan ke file referensi lain, karena file di ujung rantai cenderung hanya dibaca sebagian.

### 4. Tulis frontmatter
- `name`: huruf kecil, angka, tanda hubung; maks. 64 karakter; HARUS sama dengan nama folder. Pilih nama yang menyebut kemampuan (`pdf-tables`, `weekly-report`), bukan nama generik (`helper`).
- `compatibility` (opsional, maks. 500 karakter): catat model atau agent yang sudah diuji, misalnya "diuji pada model kecil dan besar di agent X". Wajib diisi bila skill akan dibagikan atau dijual, supaya pemakai tahu skill itu sudah diuji pada apa.
- `description`: ikuti rumus di `references/description-guide.md` (apa + kapan + pemicu dua bahasa + batas near-miss). Maks. 1024 karakter. Hindari `: ` di dalamnya, karena bisa merusak YAML.

### 5. Tulis isi SKILL.md
Urutan yang disarankan: tujuan satu paragraf → prinsip (hanya yang tidak jelas dengan sendirinya) → proses atau router → format keluaran → kasus tepi dan fallback → kesalahan umum.
- Kalimat perintah, spesifik, bisa diperiksa. "Pakai zod di `*.schema.ts`" bagus; "tulis kode bersih" tidak berguna.
- Beri contoh masukan → keluaran untuk standar kualitas yang sulit dijelaskan dengan kata.
- Untuk setiap dependensi keras (skill lain, tool, MCP, jaringan) tulis fallback satu kalimat. Skill yang macet karena satu dependensi tidak ada adalah cacat.
- Jangan berasumsi tool atau paket sudah terpasang di mesin pemakai. Di samping setiap skrip (atau langkah yang memakai library) tulis baris install dengan nama paket, misalnya `pip install pdfplumber`, bukan sekadar "pakai library PDF". Bila paket sudah ada, agent melewati langkah itu. Skill yang jalan di laptop pembuatnya tetapi rusak di mesin rekan tim pada hari pertama adalah cacat portabilitas.
- Jangan menyalin dokumentasi umum yang sudah diketahui agent. Tulis hanya yang tidak bisa disimpulkan agent sendiri: konvensi, jebakan, urutan wajib, keputusan beserta alasannya.
- Jangan menyebut nama tool, subagent, atau skill yang mungkin tidak ada di agent lain, kecuali dengan fallback. Gunakan istilah peran atau kemampuan.

### 6. Tempatkan dan validasi
Lokasi skill mengikuti agent target. Tentukan satu lokasi kanonis dan hindari salinan ganda yang bisa berbeda isinya:
- Universal lintas agent: `.agents/skills/<nama>/` (konvensi yang berkembang; belum semua agent membacanya).
- Per agent: misalnya `.claude/skills/`, `.opencode/skills/`. Beberapa agent juga membaca lokasi agent lain.
- **Proyek Pawang** (tandanya `opencode.json` memuat `permission.skill` dengan `"*": "deny"`): skill sengaja disembunyikan dari daftar skill agent supaya deskripsinya tidak memakan konteks setiap sesi, dan dijalankan lewat command. Taruh skill di `.agents/skills/<nama>/`, lalu buat `.opencode/commands/<nama>.md` berisi front matter `description` satu kalimat, kalimat `Read .agents/skills/<nama>/SKILL.md in full and follow it exactly. Resolve relative references/, assets/ and scripts/ paths against .agents/skills/<nama>/.`, dan baris `Arguments: $ARGUMENTS` (contoh: `.opencode/commands/agents-md.md`). Tambahkan satu baris untuk command itu di daftar skill `.agents/README.md`. Tambahkan `"<nama>": "allow"` di `permission.skill` hanya bila user ingin agent boleh memanggil skill itu sendiri. Karena pemicunya command, description cukup satu atau dua kalimat (`docs-health` memperingatkan yang di atas 400 karakter).
Dukungan lokasi berbeda antar agent dan versi, jadi cek dokumentasi agent target sebelum menyatakan lokasi pasti. Bila ragu, tanyakan atau tulis lokasi kanonis dan sebut bahwa agent lain mungkin butuh symlink atau salinan.

Jalankan validasi (butuh Python 3, tanpa dependensi wajib):
```
python3 <lokasi-skill-ini>/scripts/validate_skill.py <folder-skill-baru>
```
Perbaiki semua ERROR. WARN dipertimbangkan satu per satu; jangan dihapus buta-buta. Tambahkan `--strict` bila ingin WARN dianggap gagal. Bila Python tidak tersedia, lakukan cek manual: name cocok folder, description ≤ 1024 karakter dan YAML valid, semua path rujukan ada, SKILL.md < 500 baris.

### 7. Uji
Skill belum selesai sebelum diuji pada agent target.
1. Tulis 3 prompt uji realistis (seperti yang benar-benar diketik user, dengan konteks dan ketidaksempurnaan): satu kasus umum, satu kasus tepi, satu yang menggoda agent untuk keluar jalur.
2. Jalankan dengan skill dan tanpa skill (atau dengan versi sebelumnya). Bandingkan: apakah skill benar-benar mengubah hasil?
3. Nilai hasilnya: terpicu? mengikuti langkah? format keluaran benar? ada langkah yang terbuang?
4. Uji pemicu secara terpisah dengan siklus di `references/description-guide.md` (5 harus memicu, 5 near-miss tidak boleh).
5. Uji pada setiap model yang akan memakai skill, minimal yang terkecil dan yang terbesar. Hasil skill bergantung pada model di bawahnya, dan takaran detail yang pas berbeda antar model. Satu pertanyaan per kelas: model kecil, apakah panduannya cukup; model menengah, apakah jelas dan efisien; model besar, apakah tidak bertele-tele. Bila model kecil melewatkan langkah, perjelas langkah itu atau jadikan skrip. Bila model besar hasilnya lebih buruk dengan skill dibanding tanpa skill, pangkas instruksi (urutan bernomor, huruf kapital, dan perintah rinci yang dulu perlu untuk model lama sering justru merugikan model baru) sampai hasilnya membaik. Skill yang dipakai bersama model berbeda harus berada di takaran yang berfungsi untuk semuanya.
Keluaran yang objektif (konversi, ekstraksi, kode) layak diberi asersi otomatis; keluaran subjektif (gaya tulis, desain) cukup dinilai manusia. Jangan membuat harness evaluasi besar bila user tidak memintanya.

### 8. Iterasi
Dari hasil uji: perbaiki akar masalah, bukan gejalanya. Kalau agent salah di satu kasus, tanya dulu apakah instruksinya ambigu atau alasannya tidak dijelaskan, sebelum menambah aturan baru. Hindari menambal dengan MUST tambahan. Setelah tiap revisi, uji ulang dan hapus instruksi yang terbukti tidak mengubah perilaku. Setelah perubahan, uji ulang di model yang berbeda, bukan hanya model yang tadi dipakai. Berhenti bila hasil stabil pada prompt yang belum pernah dipakai untuk merancang skill (itu tanda tidak overfit).

### 9. Serah-terima
Satu paragraf pendek: apa kemampuan skill, di mana letaknya, hasil validasi, hasil uji (dengan jujur menyebut yang belum diuji, termasuk model mana yang sudah dan belum dicoba), asumsi yang dibuat, dan kompromi portabilitas bila ada field khusus agent. Tawarkan siklus optimasi description kalau pemicunya belum diuji.

## Kesalahan umum

- Description berisi ringkasan isi, bukan situasi pemicu.
- Satu skill mencoba mengerjakan tiga hal berbeda.
- Aturan keras bertumpuk tanpa alasan, atau aturan yang sama diulang di banyak tempat.
- Skill dirancang dari satu contoh dan gagal pada variasi sedikit saja.
- Dependensi keras tanpa fallback.
- File di `references/` atau `scripts/` tidak dirujuk dari SKILL.md.
- Menjelaskan hal yang sudah diketahui agent (cara kerja Markdown, dasar-dasar bahasa pemrograman).
- Menyatakan selesai tanpa pernah menjalankan skill pada agent target.
- Semua langkah ditulis dengan tingkat detail yang sama, padahal sebagian rapuh (perlu skrip) dan sebagian longgar.
- Referensi panjang tanpa daftar isi, atau referensi yang menautkan ke referensi lain.
- Skill hanya diuji di satu model lalu dianggap cocok untuk semua.
- Skrip dengan dependensi tanpa baris install di sampingnya.
- Proses panjang tanpa checklist atau tanpa langkah balik saat verifikasi gagal.
- `name` tidak sama dengan nama folder, atau YAML rusak karena titik dua di description.
