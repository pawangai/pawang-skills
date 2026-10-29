---
name: "panduan-brand"
description: "Buat panduan brand lengkap sebagai berkas Markdown (.md): nama, tagline, filosofi, voice, logo, warna dan font, layanan, contoh teks. Pakai saat user minta panduan brand atau brand guideline."
license: MIT
compatibility: "Python 3 untuk skrip kontras dan pemeriksa struktur. SendUserFile dan WebSearch adalah tool runtime Pawang; di agent lain pakai tool setara untuk mengirim berkas dan mencari di web. Memanggil skill interview."
metadata:
  author: "Pawang"
---

# Panduan Brand (keluaran: berkas .md)

Skill ini menghasilkan satu panduan brand dalam bahasa user (default Indonesia) sebagai **berkas Markdown**. Hasil akhir adalah file `.md` yang dikirim lewat SendUserFile. Jangan membuatnya sebagai Claude Doc, artifact, atau .docx kecuali user meminta format itu secara eksplisit.

## Kapan dipakai
User meminta panduan brand, brand guideline, brand book, atau merapikan identitas brand dari nama yang sudah ada. Jika nama brand belum ada, bantu memilih nama dulu (3 sampai 5 kandidat, beri alasan, cek ketersediaan domain lewat pencarian web), lalu lanjut ke panduan setelah user memilih.

## Langkah kerja
1. **Kumpulkan bahan.** Dari pesan dan lampiran user, ambil: nama brand, jenis usaha atau jasa, target pelanggan, kesan yang diinginkan, kompetitor yang diketahui. Bila bahan sudah cukup, langsung tulis. Bila ada keputusan yang belum ada (target pelanggan, kesan yang diinginkan, kompetitor, nama), panggil skill `interview` dalam mode ringan sebelum menulis, tanpa batas 3 pertanyaan. Detail kecil yang bukan keputusan (misalnya nama warna) boleh diambil secara wajar dan ditandai `[ASUMSI]`.
2. **Riset singkat (WebSearch, mode standard).** Cek domain (.com, .id, .dev, .org) dan apakah ada brand sejenis di bidang yang sama. Catat hasilnya apa adanya, termasuk yang tidak bisa dipastikan. Jangan menyatakan domain "tersedia" tanpa sumber; tulis "belum terdaftar menurut pencarian, cek langsung di registrar".
3. **Tulis panduan** dengan struktur di bawah.
4. **Hitung kontras warna** dengan skrip di bawah. Angka kontras di dokumen harus berasal dari hasil skrip, bukan perkiraan.
5. **Periksa struktur** dengan skrip pemeriksa di bawah. Perbaiki sampai hasilnya `OK`.
6. **Kirim** berkas `.md` dengan SendUserFile (display attach, nama berkas `panduan-brand-<nama-brand>.md`). Balasan akhir: satu atau dua kalimat tentang isinya, daftar `[ASUMSI]` dan keputusan terbuka yang perlu user jawab, dan sumber bila ada.

## Struktur panduan (heading wajib, urutan tetap)
Judul `# Panduan Brand: <Nama>`, lalu baris singkat berisi tanggal dan versi, lalu:

1. `## Ringkasan` : satu paragraf (apa brand ini, untuk siapa, janji utamanya) dan tabel kecil: nama, kategori, tagline utama, nilai inti, warna utama, domain pilihan.
2. `## Tagline` : satu tagline utama plus 4 sampai 6 alternatif, tiap alternatif dengan kapan cocok dipakai (hero situs, bio media sosial, kartu nama).
3. `## Filosofi Brand` : metafora inti, manifesto pendek (4 sampai 8 baris), dan 3 nilai brand dengan satu kalimat arti masing-masing. Metafora harus terasa lokal dan mudah dibayangkan.
4. `## Gaya Bahasa` : sifat suara (3 sampai 4), tabel "Kami bilang begini, bukan begitu" (minimal 5 baris), daftar kata yang dipakai dan dihindari, aturan sapaan (kami, kamu atau Anda) dan tingkat jargon.
5. `## Konsep Logo` : tiga arah konsep (A, B, C), tiap arah dengan deskripsi bentuk, makna, kelebihan, kekurangan. Beri satu rekomendasi dan alasannya. Jelaskan versi horizontal, ikon saja, dan satu warna. Tulis deskripsi dalam kata; jangan menggambar logo yang meniru karya atau karakter milik pihak lain.
6. `## Palet Warna` : tabel nama, hex 6 digit, peran, dan aturan pakai. Lima warna: dua utama, satu aksen, dua netral. Beri nama warna yang berkarakter (bukan "Biru 1"). Tambah tabel kontras dari skrip, dengan kolom keputusan: boleh untuk teks (4,5:1 atau lebih), hanya ikon atau bentuk besar (3 sampai 4,5), dilarang untuk teks (kurang dari 3).
7. `## Tipografi` : font judul dan font isi (pilih font gratis seperti Google Fonts), skala ukuran, tinggi baris, dan aturan penggunaan. Catat lisensinya.
8. `## Kerangka Layanan` : bila brand menjual jasa atau produk, daftar lini dengan nama turunan brand, satu kalimat janji, dan untuk siapa. Sertakan tingkatan paket (nama tema brand) bila relevan. Jangan mengarang harga; tulis `[KEPUTUSAN DIBUTUHKAN]` bila belum ada.
9. `## Contoh Teks Siap Pakai` : bio Instagram atau LinkedIn (di bawah 150 karakter), teks hero situs, kalimat pembuka WhatsApp, tanda tangan email, satu contoh balasan ke pelanggan, dan 3 contoh keterangan postingan. Semua mengikuti Gaya Bahasa.
10. `## Langkah Berikutnya` : daftar centang: beli domain, amankan username media sosial, cek merek di DJKI (pdki.dgip.go.id) bila di Indonesia, finalisasi logo, siapkan templat, dan catatan risiko nama (kemiripan dengan brand lain yang ditemukan di riset).

Tambahan opsional bila relevan: `## Catatan Kompetitor` (nama, apa yang mereka lakukan, bedanya dengan kita) dan `## Keputusan Terbuka` (tabel pertanyaan, opsi, rekomendasi).

## Aturan isi
- Satu bahasa saja di seluruh dokumen. Tanpa emoji. Tanpa tanda pisah panjang berlebihan.
- Jangan memakai placeholder bertanda kurung siku selain `[ASUMSI]` dan `[KEPUTUSAN DIBUTUHKAN]`. Semua isian harus berisi nilai nyata.
- Setiap klaim tentang domain, kompetitor, atau merek terdaftar harus dari hasil pencarian dan disebut sumbernya di akhir dokumen pada `## Sumber`.
- Jangan menyalin slogan, logo, atau nama pihak lain. Bila kandidat nama atau tagline terlalu mirip dengan temuan riset, buang atau tandai risikonya.
- Hex selalu 6 digit dengan awalan `#`, ditulis dalam backtick.
- Tabel dipakai untuk perbandingan dan palet; narasi untuk filosofi dan voice.
- Bila user menyebut pesaing langsung dengan nama mirip, tulis di Ringkasan dan Langkah Berikutnya agar keputusan nama dan domain dibuat sadar.

## Skrip kontras (jalankan dengan `python3 -I kontras.py "Nama=#HEX" ...`)
Simpan ke scratchpad, bukan ke folder keluaran.

```python
import sys, itertools
def lum(h):
    h=h.lstrip('#'); r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda c: c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
def cr(a,b):
    x,y=sorted((lum(a),lum(b)),reverse=True); return (x+0.05)/(y+0.05)
pal=dict(a.split('=') for a in sys.argv[1:])
for (n1,h1),(n2,h2) in itertools.combinations(pal.items(),2):
    r=cr(h1,h2)
    print(f"{n1} dengan {n2}: {r:.1f}:1 ->", "boleh untuk teks" if r>=4.5 else "hanya ikon atau bentuk besar" if r>=3 else "dilarang untuk teks")
```

Contoh nyata (Pawang): Biru Malam `#14213D` di atas Api Dupa `#FF8A3D` = 6,8:1 (boleh); putih di atas Api Dupa = 2,4:1 (dilarang); Api Dupa di atas Krem `#FFF6E9` = 2,2:1 (hanya ikon atau bentuk besar). Pakai pasangan yang lolos untuk teks, dan tulis pasangan yang gagal sebagai larangan eksplisit.

## Skrip pemeriksa struktur (jalankan dengan `python3 -I cek.py berkas.md`)

```python
import re,sys
t=open(sys.argv[1],encoding='utf-8').read()
need=["Ringkasan","Tagline","Filosofi","Gaya Bahasa","Logo","Palet Warna","Tipografi","Layanan","Contoh Teks","Langkah Berikutnya"]
heads=[l for l in t.splitlines() if l.startswith('#')]
bad=[f"heading hilang: {n}" for n in need if not any(n in h for h in heads)]
bad+=["placeholder: "+x for x in set(re.findall(r"\[(?!ASUMSI|KEPUTUSAN DIBUTUHKAN)[A-Za-z][^\]\n]*\](?!\()",t))]
bad+=["hex bukan 6 digit: "+x for x in set(re.findall(r"#[0-9a-fA-F]{3,8}\b",t)) if len(x)!=7]
if re.search(r"[\U0001F300-\U0001FAFF☀-➿]",t): bad.append("ada emoji")
print(bad or "OK")
```

Catatan: heading `## Layanan` boleh bernama `Kerangka Layanan`. Bila brand tidak menjual jasa, tetap sertakan bagian itu dengan judul yang sesuai (mis. `Kerangka Produk`) dan ubah kata `Layanan` pada daftar `need` di skrip agar cocok. Pemeriksa tidak menilai mutu isi; baca ulang hasilnya sekali untuk memastikan voice konsisten dan tidak ada klaim tanpa sumber.

## Pembaruan panduan yang sudah ada
Bila user melampirkan panduan lama atau menyebut perubahan (layanan baru, domain, kompetitor), ubah berkas `.md` yang ada pada bagian terkait saja, naikkan versi dan tanggal di bawah judul, lalu jalankan kedua skrip lagi. Jangan menulis ulang seluruh dokumen bila hanya sebagian yang berubah.