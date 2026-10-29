# Panduan menulis dan mengoptimasi description

Description adalah satu-satunya bagian skill yang selalu ada di konteks agent. Agent memutuskan memakai skill atau tidak hanya dari `name` + `description`. Isi skill sebagus apa pun tidak berguna kalau description-nya tidak memicu.

## Rumus

```
[Apa yang dilakukan, 1 kalimat].
[Gunakan saat: situasi, frasa user, jenis file, konteks], termasuk bila user tidak menyebut istilah teknisnya.
[Padanan bahasa lain yang sering dipakai user, 1 kalimat].
[Jangan gunakan untuk: tetangga terdekat yang sering tertukar].
```

Aturan:
1. **Apa + Kapan.** Semua informasi "kapan dipakai" ada di description, bukan di body. Body baru dibaca setelah skill terpicu.
2. **Sedikit agresif.** Agent cenderung under-trigger. Sebut konteks yang menyiratkan skill ini berguna, bukan hanya nama fiturnya.
3. **Batas negatif hanya untuk near-miss.** "Jangan gunakan untuk X" berguna kalau X benar-benar sering tertukar (skill tetangga, tugas serupa). Jangan menulis daftar panjang larangan.
4. **Bahasa user.** Kalau user berganti bahasa, masukkan 1-2 frasa pemicu di bahasa kedua.
5. **Batas teknis:** maks. 1024 karakter, tanpa baris kosong, dan aman sebagai YAML. Description satu baris yang mengandung `: ` (titik dua + spasi) atau ` #` harus diberi kutip pembungkus, atau gunakan blok `>`. Cara termudah: hindari titik dua di dalam description.
6. **Tulis sebagai kemampuan, bukan sebagai ringkasan isi.** Salah: "Skill ini berisi panduan 12 langkah". Benar: "Menyusun X. Gunakan saat user ...".

## Contoh

Lemah (tidak ada pemicu, tidak ada batas):
```
description: Membantu pekerjaan dengan file PDF.
```

Kuat:
```
description: Membaca, menggabung, memisah, mengisi form, dan OCR file PDF. Gunakan saat user menyebut file .pdf, ingin mengekstrak tabel atau teks dari dokumen, menggabung beberapa PDF, atau mengisi formulir, bahkan bila tidak menyebut kata "PDF" secara eksplisit. Jangan gunakan untuk membuat dokumen Word atau slide.
```

Lemah (daftar fitur, bukan pemicu):
```
description: Skill ini punya 5 mode, template laporan, dan 3 skrip bantu.
```

Kuat (dua bahasa):
```
description: Menulis dan merapikan laporan mingguan tim dari catatan mentah. Gunakan saat user minta laporan mingguan, rekap progres, atau status update, termasuk "weekly report" atau "status update" dalam bahasa Inggris. Jangan gunakan untuk notulen rapat.
```

## Siklus optimasi

Lakukan setelah isi skill stabil.

1. Tulis 10 query uji realistis, seperti yang benar-benar diketik user (ada typo, singkatan, konteks tambahan):
   - 5 **harus memicu**: campuran eksplisit ("pakai skill X"), implisit (tanpa istilah teknis), dan berbeda bahasa.
   - 5 **tidak boleh memicu**: near-miss yang berbagi kata kunci tetapi butuh skill lain atau tidak butuh skill sama sekali. Query yang jelas tidak relevan tidak menguji apa-apa.
2. Jalankan tiap query di agent target (dengan skill terpasang) dan catat apakah skill terpicu. Jalankan 2-3 kali per query bila agent non-deterministik.
3. Kegagalan memicu → tambahkan frasa atau konteks dari query yang gagal, tetapi sebagai KATEGORI situasi, bukan menyalin query (jangan overfit).
4. Salah memicu → tambahkan batas negatif yang spesifik untuk near-miss itu.
5. Ulangi sampai stabil. Uji ulang dengan query baru yang belum pernah dipakai untuk memastikan tidak overfit.

Kalau satu skill terus bertabrakan dengan skill lain, pertimbangkan menggabungkan atau memperjelas pembagian tugas di kedua description.

## Pola gagal yang sering muncul

| Gejala | Penyebab | Perbaikan |
|---|---|---|
| Tidak pernah terpicu | Description berisi nama fitur, tanpa situasi user | Tambah "Gunakan saat..." dengan frasa nyata |
| Terpicu untuk semuanya | Terlalu luas ("membantu menulis") | Persempit objek dan tambah batas negatif |
| Terpicu hanya bila nama skill disebut | Tidak ada pemicu implisit | Tambah kata "bahkan bila user tidak menyebut ..." |
| Gagal dimuat agent | YAML rusak (titik dua, kutip) | Jalankan `scripts/validate_skill.py` |
| Skill A dan B berebut | Wilayah tumpang tindih | Tulis batas "Jangan gunakan untuk" di keduanya |
