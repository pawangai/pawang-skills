# Elemen Dekoratif

Baca file ini hanya bila user meminta maskot, ikonografi, ilustrasi, atau tema lengkap. Untuk permintaan palet saja, jangan buat elemen dekoratif. Skill ini menghasilkan spesifikasi (props, gaya, penempatan), bukan gambar atau SVG jadi.

## Daftar isi
- Prinsip
- Tiga lapisan
- Menurunkan props dari metafora
- Token gaya
- Batas dan penempatan
- Aksesibilitas dan performa
- Larangan
- Format keluaran

## Prinsip
Dekorasi yang baik membawa makna dan memperkuat metafora, bukan sekadar mengisi ruang kosong. Setiap elemen harus bisa dijelaskan dengan satu kalimat: "elemen ini mewakili ... dalam metafora".

## Tiga lapisan
1. **Hero:** maskot atau ilustrasi utama, satu per halaman.
2. **Props cerita:** ilustrasi kecil yang berdiri sendiri di sekitar hero, misalnya ikon garis, panel, atau benda sehari-hari yang bercerita.
3. **Pola latar:** tekstur halus seperti dot grid atau noise, opacity rendah, tidak boleh mengganggu keterbacaan.

## Menurunkan props dari metafora
Pilih 3-5 props yang masing-masing mewakili satu sisi metafora (sistem, suasana, peran, hasil). Uji tiap prop:
- Apakah muncul atau relevan dalam dunia metafora?
- Apakah bisa dijelaskan dalam satu kalimat?
- Apakah tetap dikenali bila dikecilkan?
Prop yang gagal salah satu uji dibuang. Contoh Pawang (ilustrasi, bukan data nyata): server awan untuk infrastruktur yang aman, cangkir kopi beruap untuk suasana tenang, tongkat untuk peran pawang.

## Token gaya
Tetapkan sekali, pakai ke semua elemen supaya terlihat satu keluarga:
- Tebal garis (satu nilai untuk semua ikon garis).
- Warna hanya dari palet tema; tidak ada warna baru khusus dekorasi.
- Opacity per lapisan (pola latar paling rendah).
- Radius sudut dan gaya ujung garis (bulat atau tajam).
- Satu gaya per lapisan: garis untuk props, isian untuk hero, titik atau noise untuk latar.

## Batas dan penempatan
- Maksimal 2-4 props per section; hero satu per halaman.
- Tempatkan di area kosong untuk menyeimbangkan komposisi, jangan menutupi teks, CTA, atau formulir.
- Elemen yang membawa informasi (misalnya label status) tetap mengikuti aturan kontras teks 4,5:1; yang murni dekoratif tidak perlu, tetapi tidak boleh menurunkan kontras teks di atasnya.
- Di layar sempit, kurangi atau sembunyikan props sebelum memperkecil teks.

## Aksesibilitas dan performa
- Elemen dekoratif diberi `aria-hidden="true"` dan alt kosong; elemen informatif diberi teks alternatif.
- Animasi hanya yang halus, dan dimatikan di `prefers-reduced-motion`.
- Utamakan SVG inline yang ringan; hindari bitmap besar untuk dekorasi.

## Larangan
- Emoji sebagai dekorasi.
- Gradient blob generik atau bentuk acak tanpa makna.
- Ikon stok yang tidak nyambung dengan metafora.
- Props lebih dari batas hanya demi terlihat ramai.
- Meniru gaya brand lain.

## Format keluaran
Tabel props, lalu token gaya dan aturan penempatan:

| Prop | Mewakili | Lapisan | Penempatan | Catatan gaya |
|---|---|---|---|---|

Tutup dengan satu kalimat larangan visual khusus brand ini.
