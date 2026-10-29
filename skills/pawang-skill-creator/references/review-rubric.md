# Rubrik review skill

Pakai saat mengaudit skill yang sudah ada. Jalankan `scripts/validate_skill.py` dulu, karena cek mekanis tidak perlu dinilai ulang secara manual. Lalu nilai dimensi di bawah dan laporkan sesuai format di bagian akhir.

## Dimensi

| # | Dimensi | Pertanyaan | Tanda masalah |
|---|---|---|---|
| 1 | Akurasi pemicu | Apakah description memicu pada situasi yang tepat, termasuk implisit dan lintas bahasa? Apakah ada batas untuk near-miss? | Hanya nama fitur; tidak ada "Gunakan saat"; tidak ada batas; bahasa tunggal padahal user dwibahasa |
| 2 | Kejelasan instruksi | Apakah tiap langkah bisa dieksekusi tanpa menebak? | Kata kabur ("pastikan kualitas baik"), langkah tanpa kriteria selesai |
| 3 | Alasan di balik aturan | Apakah aturan penting disertai "kenapa"? | Deretan MUST/ALWAYS/NEVER tanpa penjelasan; agent kaku atau salah generalisasi |
| 4 | Kasus tepi | Bagaimana kalau input kosong, file tidak ada, tool tidak tersedia, permintaan di luar cakupan? | Tidak ada fallback; skill macet karena satu dependensi |
| 5 | Ambiguitas | Adakah dua instruksi yang bertentangan atau rujukan ke bagian yang tidak ada? | Section dirujuk tapi tidak ada di template; istilah dipakai berganti-ganti |
| 6 | Generalisasi | Apakah skill berlaku untuk keluarga tugas, bukan hanya contoh yang dipakai saat membuatnya? | Nama file, nama proyek, atau nilai contoh tertanam sebagai aturan |
| 7 | Perilaku tidak perlu | Adakah langkah yang membuat agent bekerja ekstra tanpa memperbaiki hasil? | Wawancara panjang untuk tugas sederhana; verifikasi berulang; baris yang tidak mengubah perilaku saat diuji |
| 8 | Penyederhanaan | Apa yang bisa dihapus, digabung, atau dipindah ke references/ tanpa kehilangan efek? | Pengulangan aturan yang sama di 3+ tempat; contoh yang kembar |
| 9 | Portabilitas | Apakah hanya memakai field spesifikasi dan tidak bergantung pada nama tool, subagent, atau skill yang tidak ada di agent lain? | Field khusus satu agent; nama tool tertanam; path absolut |
| 10 | Biaya konteks | Apakah progressive disclosure dipakai (inti di SKILL.md, detail di references/, deterministik di scripts/)? | SKILL.md mendekati 500 baris; referensi panjang selalu dibaca; kode ditulis ulang tiap pemakaian padahal bisa jadi skrip |
| 11 | Daftar isi dan kedalaman rujukan | Apakah referensi di atas 100 baris diawali daftar isi, dan semua file ditautkan langsung dari SKILL.md (tanpa rantai antar-referensi)? | Referensi panjang tanpa daftar isi; file yang hanya bisa dicapai lewat file lain |
| 12 | Tingkat kebebasan | Apakah detail tiap langkah sesuai kerapuhannya? Apakah langkah berdampak besar (uang, hapus data, urutan wajib) dikunci dengan skrip? | Semua langkah sama detailnya; langkah berisiko hanya berupa teks bebas; langkah sepele dikunci kaku |
| 13 | Kompatibilitas model | Apakah skill sudah diuji di model kecil dan besar, dan model yang dituju dicatat (`compatibility`)? | Hanya diuji satu model; instruksi preskriptif lama yang membuat model baru lebih buruk; model kecil melewatkan langkah |
| 14 | Verifikasi dan dependensi | Proses panjang punya checklist dengan langkah balik? Ada loop koreksi bila standar bisa dicek? Skrip punya baris install di sampingnya? | Langkah gagal tetap dicentang; tidak ada loop cek-perbaiki; "pakai library X" tanpa perintah install |

## Tingkat keparahan

- **BLOCKER**: skill gagal dimuat atau tidak akan terpicu (YAML rusak, name tidak cocok folder, description kosong, rujukan path hilang).
- **MAJOR**: skill terpicu salah atau menghasilkan keluaran yang salah pada kasus umum (instruksi bertentangan, tidak ada fallback untuk dependensi keras, overfit ke contoh).
- **MINOR**: skill jalan tetapi boros atau membingungkan (pengulangan, kata kabur, urutan section aneh).

## Format laporan

```markdown
## Ringkasan
<satu kalimat: siap pakai / perlu perbaikan / perlu rancang ulang, dan alasan utamanya>

## Temuan
| Tingkat | Dimensi | Temuan (kutip lokasinya) | Perbaikan |
|---|---|---|---|

## Yang sudah baik
<1-3 butir; jangan buang hal yang bekerja>

## Uji yang disarankan
<3-5 prompt: yang harus memicu, near-miss yang tidak boleh memicu, dan satu kasus tepi>
```

Urutkan temuan dari BLOCKER ke MINOR. Beri perbaikan konkret (teks pengganti atau langkah), bukan hanya keluhan. Jangan menulis ulang skill kecuali diminta; tawarkan versi revisi di akhir.
