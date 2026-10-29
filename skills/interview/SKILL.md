---
name: interview
description: Menanyai user dalam ronde bernomor, tiap pertanyaan dengan rekomendasi jawaban, agar tidak ada keputusan yang diasumsikan diam-diam. Gunakan mode penuh (pohon keputusan dan konfirmasi) untuk ide atau rencana mentah, atau bila user bilang "interview me", "grill me", "wawancarai saya"; mode ringan untuk 1-3 pertanyaan dari skill lain. Bukan untuk meminta persetujuan commit, merge, push, atau deploy.
metadata:
  author: "Pawang"
---

# Interview

Tujuan: mencapai pemahaman bersama dengan user. Tidak ada keputusan yang dibiarkan sebagai asumsi diam-diam, karena asumsi yang salah baru ketahuan setelah pekerjaan selesai dan mahal diperbaiki.

## Pilih mode

- **Mode penuh**: user meminta interview, atau idenya masih mentah, besar, atau penuh keputusan yang saling bergantung. Jangan mengerjakan apa pun (menulis kode, file, rencana final) sebelum user mengonfirmasi bahwa pemahaman bersama sudah tercapai.
- **Mode ringan**: skill lain atau agent hanya perlu menanyakan 1-3 keputusan yang tidak saling bergantung.

Bila ragu, pakai mode ringan, lalu pindah ke mode penuh bila jawaban membuka keputusan baru.

## Mode ringan

1. Ajukan semua pertanyaan dalam satu ronde dengan format ronde di bawah.
2. Tunggu jawaban, terapkan, lalu lanjutkan pekerjaan skill pemanggil. Tanpa peta pohon, penelusuran ulang, ringkasan, atau konfirmasi tambahan.
3. Pindah ke mode penuh bila jawaban membuka keputusan yang saling bergantung, atau bila user meminta interview.

Aturan fakta lawan keputusan dan penanganan jawaban di bawah tetap berlaku. Persetujuan commit, merge, push, atau deploy tetap diminta terpisah oleh skill yang mengaturnya.

## Peta keputusan: pohon desain (mode penuh)

Petakan topik sebagai **pohon desain**. Setiap keputusan bercabang menjadi keputusan lain yang bergantung padanya. Contoh: "pakai database apa" harus dijawab sebelum "bagaimana strategi migrasi" bisa ditanyakan.

**Frontier** adalah semua keputusan yang prasyaratnya sudah selesai, yaitu pertanyaan yang bisa ditanyakan sekarang tanpa menebak jawaban yang belum didengar.

## Bekerja per ronde (mode penuh)

1. Hitung frontier.
2. Tanyakan **seluruh frontier dalam satu ronde**. Beri nomor tiap pertanyaan dan sertakan rekomendasi jawabanmu.
3. Berhenti dan tunggu jawaban user. Jangan lanjut ke ronde berikutnya sebelum ada jawaban.
4. Jawaban user mengubah pohon: keputusan yang selesai mendorong frontier ke luar dan membuka pertanyaan yang tadinya bergantung. Hitung ulang frontier, lalu tanyakan ronde berikutnya.

Pertanyaan yang jawabannya bergantung pada pertanyaan lain yang masih terbuka di ronde yang sama **bukan** bagian ronde ini. Taruh di ronde berikutnya. Menanyakan keduanya sekaligus memaksa user menjawab tanpa dasar, atau memaksamu menebak.

## Format ronde

Pakai format ini persis:

```
❓ **Q1** - **<judul pertanyaan>**: <isi pertanyaan, boleh beberapa paragraf, termasuk pilihan ganda>

➡️ <rekomendasi jawabanmu>

---

❓ **Q2** - **<judul pertanyaan>**: <isi pertanyaan, boleh beberapa paragraf, termasuk pilihan ganda>

➡️ <rekomendasi jawabanmu>
```

Rumuskan tiap pertanyaan supaya **"ya" berarti menerima rekomendasimu**. Dengan begitu user yang setuju cukup menjawab "ya" atau "Q1, Q3 ya", dan hanya perlu mengetik panjang untuk yang tidak setuju. Contoh: "Pakai Postgres via Supabase, bukan D1?" (jawaban "ya" jelas artinya), bukan "Database apa yang dipakai?".

Rekomendasi harus sungguhan, dengan alasan singkat bila tidak jelas dengan sendirinya. Jangan menyodorkan pilihan netral tanpa sikap. Tugasmu mengurangi beban keputusan user, bukan memindahkannya.

## Fakta adalah tugasmu, keputusan adalah tugas user

Jangan bertanya ke user untuk hal yang bisa kamu cari sendiri: isi filesystem, versi paket, konfigurasi, perintah yang tersedia, dokumentasi. Cari sendiri.

- Kalau ada sub-agent, kirim sub-agent untuk mencari fakta itu. Kalau tidak ada, cari langsung dengan tool yang tersedia (baca file, jalankan perintah, cari di web).
- **Jangan menunggu pencarian selesai sebelum bertanya.** Pencarian yang sedang berjalan adalah prasyarat yang belum selesai. Hanya pertanyaan di hilirnya yang menunggu laporan. Tanyakan sisa frontier sekarang.
- Jika hasil pencarian mengubah rekomendasi atau membuka pertanyaan baru, masukkan ke ronde berikutnya.

**Keputusan** (tujuan, prioritas, tradeoff, selera, batasan bisnis) selalu milik user. Ajukan ke user dan tunggu jawabannya. Jangan memutuskan sendiri lalu memberi tahu belakangan.

## Menangani jawaban

- **Setuju sebagian atau menjawab sebagian:** catat yang sudah diputuskan, tanyakan ulang hanya yang belum, tanpa mengulang yang sudah jelas.
- **Tidak setuju dengan rekomendasi:** terima. Kalau jawabannya membuka cabang baru atau bertentangan dengan keputusan sebelumnya, tunjukkan konfliknya dan tanyakan mana yang berlaku.
- **"Terserah" atau "ikut rekomendasimu":** perlakukan sebagai persetujuan pada rekomendasi, lalu catat dengan jelas bahwa itu default yang kamu pilih.
- **User bertanya balik:** jawab dulu, baru lanjutkan ronde. Jawaban bisa mengubah rekomendasi.
- Bahasa pertanyaan mengikuti bahasa user.

## Kapan selesai (mode penuh)

Sesi selesai ketika **frontier kosong**: setiap cabang pohon sudah dikunjungi dan tidak ada yang diasumsikan diam-diam.

Sebelum menyatakan selesai:

1. Telusuri pohon sekali lagi. Cari cabang yang terlewat, terutama keputusan yang tampak sepele tapi berdampak (batasan, kasus gagal, siapa penggunanya, apa yang sengaja *tidak* dikerjakan).
2. Tulis ringkasan pemahaman bersama: keputusan yang diambil (beserta alasannya bila penting), hal yang sengaja di luar cakupan, dan fakta yang kamu temukan sendiri.
3. Minta user mengonfirmasi ringkasan itu. Baru setelah ada konfirmasi, tawarkan atau mulai mengerjakan.

Jika user mengoreksi ringkasan, perbarui pohon dan lanjutkan ronde sampai frontier kosong lagi.
