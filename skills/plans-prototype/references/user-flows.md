# Panduan menulis 02-user-flows.md

Figr menerima flow sebagai diagram yang bisa diedit. Mermaid dipilih karena teks: mengubah satu langkah cukup mengubah satu baris, dan bisa di-diff di git.

## Memilih flow

Mulai dari **F0 navigasi shell** (selalu) lalu **auth** dan **akun**. Sisanya diturunkan dari screen yang saling berurutan: pasangan *Daftar → Form → Detail → Dialog aksi*. Prioritaskan flow yang:

1. melewati batas modul (booking → invoice → pembayaran; HR → Finance),
2. punya status/enum di kode (siklus hidup),
3. melibatkan uang, data pasien, atau izin (di situ edge case terpenting).

Satu flow = satu diagram + satu baris "Catatan" (enum, konflik, asumsi). Beri tabel isi di awal di bawah heading `Daftar flow` (kolom `# | Flow | Modul`), dan judul tiap flow `F<n> - <nama>` (contoh `## F3 - Langkah pertama`); F0 selalu ada. Tiap flow memuat satu blok Mermaid.

## Memilih jenis diagram

| Situasi | Jenis |
|---|---|
| Siklus status satu entitas (booking, invoice, refund, cuti, konten, aset, tiket) | `stateDiagram-v2` — ambil nama status dari tipe di kode (`grep "type .*Status"`) |
| Alur layar & keputusan (wizard, navigasi, rekrutmen) | `flowchart TD/LR` |
| Interaksi antar peran/sistem (booking → gateway → kwitansi) | `sequenceDiagram` dengan `actor`/`participant` |
| Peta navigasi | `flowchart TD` |

## Konvensi

- Rujuk screen dengan nomor aslinya: `Setujui run #120`. Nomor ini jembatan ke `screens.figr.json` dan ke dokumen 03.
- Enum ditulis persis seperti di kode (`belum_ditugaskan`, `partially_paid`), dan disebut lagi di baris catatan.
- Transisi yang **tidak** punya screen pemicu di prototype ditandai **[ASUMSI]** di catatan, jangan digambar seolah fakta.
- Konflik antarmodul ditunjuk ke ID konflik PRD (mis. "→ PRD C2").
- Jika `edges` di `screens.figr.json` kosong, turunkan urutan dari nama screen, route, dan state — dan katakan itu ke user.

## Jebakan sintaks Mermaid (sudah terbukti)

- Bentuk `[/teks/]` (paralelogram) rusak jika teks berisi `/` atau `*`. Pakai `["/auth/login"]` dengan kutip.
- `stateDiagram-v2`: jangan membuat transisi dari state **di dalam** composite `state X { }` ke state di luarnya; ratakan dengan awalan (`QRMenyiapkan`, `QRDipindai`).
- Label dengan `(`, `#`, `→`, `≤`, `±`, `:` aman bila berada di dalam `[...]`/`{...}` atau setelah `:` pada state/sequence. Hindari `;` di sequence diagram.
- Nama node jangan memakai kata cadangan (`end`, `graph`, `subgraph`, `style`, `class`).
- Satu blok tidak lebih dari ±25 node; pecah flow yang lebih besar.

## Validasi

Jalankan `scripts/validate_mermaid.py 02-user-flows.md 01-PRD.md` sebelum menyerahkan. Jika `mmdc` tidak ada atau Chrome tidak ditemukan, katakan terus terang bahwa diagram belum dirender; jangan menyatakan "valid".
