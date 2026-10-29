# Kontrak keluaran plans-prototype

Empat dokumen dibaca oleh skill `plan` Pawang (`reference/from-figr-files.md`).
Catatan: penanda `plans-figr-contract` di bawah sengaja tidak diganti nama setelah skill menjadi `plans-prototype`, karena penanda yang sama dibaca oleh `from-figr-files.md` di Pawang.
Pembaca mencari teks yang persis, jadi teks di bawah ini adalah kontrak, bukan
saran gaya. Kontrak ini hanya memuat yang dibutuhkan pembaca; selebihnya
(bagian khusus jenis proyek, urutan, isi tabel) bebas mengikuti jenis proyek.

Versi kontrak: 1. Setiap perubahan pada tabel di bawah harus dilakukan di dua
tempat sekaligus (file ini dan `from-figr-files.md` di Pawang), lalu dicek dengan
`scripts/check_contract.py --reader <path from-figr-files.md>`.

## Heading wajib

Aturan cocok: sebuah baris heading Markdown (tingkat 1 sampai 6) yang
**memuat** teks itu, huruf besar kecil dihitung. Nomor atau huruf di depan
heading (`## 3. Tujuan dan non-tujuan`) boleh.

<!-- plans-figr-contract:v1 -->
| Dokumen | Heading memuat | Dipakai pembaca untuk |
| --- | --- | --- |
| `01-PRD.md` | `Ringkasan` | masalah dan ringkasan di PROJECT.md |
| `01-PRD.md` | `Tujuan dan non-tujuan` | fitur, dan apa yang sengaja tidak dikerjakan |
| `01-PRD.md` | `Pengguna dan peran` | pengguna di PROJECT.md |
| `01-PRD.md` | `Requirement fungsional` | kandidat fitur di BUILD.md (FR-n, P0 sampai P2) |
| `01-PRD.md` | `Requirement non-fungsional` | batasan dan kesiapan rilis (NFR-n) |
| `01-PRD.md` | `Keputusan terbuka` | pertanyaan interview (Q-n) |
| `01-PRD.md` | `Metrik keberhasilan` | metrik di bagian masalah |
| `02-user-flows.md` | `Daftar flow` | ID flow untuk jejak di BUILD.md |
| `02-user-flows.md` | `F0 -` | flow navigasi, selalu ada |
| `03-interface-designs.md` | `Flow -> frame` | pemetaan flow ke frame |
| `03-interface-designs.md` | `Inventaris frame` | daftar frame |
| `04-edge-cases.md` | `Kerjakan dulu (blocker desain)` | urutan di BUILD.md |
| `04-edge-cases.md` | `Butuh keputusan produk sebelum didesain` | keputusan yang harus dikonfirmasi |
<!-- /plans-figr-contract -->

Bagian lain boleh ada atau tidak, tergantung jenis proyek: `Masalah (kondisi
saat ini)`, `Arsitektur target`, `Shell`, `Pemetaan modul`, `Konflik yang harus
diselesaikan`, `Strategi migrasi`, `Risiko dan trade-off`, `Sitemap`, `Model
konten`, `Funnel`. Bagian yang tidak relevan dihapus, tidak diisi teks generik.

## Pola isi wajib

- **Flow:** tiap flow berjudul `F<n> - <nama>` (contoh `## F3 - Langkah pertama`)
  dan memuat satu blok Mermaid.
- **Requirement:** tiap baris `FR-<n>` memuat satu prioritas `P0`, `P1`, atau
  `P2`.
- **Keputusan terbuka:** tiap keputusan punya ID `Q<n>`. Bila ada penanda
  `[KEPUTUSAN DIBUTUHKAN]` di dokumen mana pun, `Keputusan terbuka` memuat
  barisnya.
- **Edge case:** baris persis `| EC-XX-NN | Skenario | Perilaku yang diharapkan | Frame | Sev | Dasar |`
  dan berakhir `| <Sev> | <Dasar> |`. Sev satu dari `K`, `T`, `S`, `R`. Dasar satu
  dari `P` (terlihat di prototype atau dokumen sumber) atau `U` (usulan).
  Pembaca memperlakukan baris `U` sebagai usulan yang harus dikonfirmasi.

## Penanda, satu set saja

| Penanda | Arti | Perlakuan pembaca |
| --- | --- | --- |
| `[ASUMSI]` | disimpulkan, tidak ada bukti | usulan, dikonfirmasi dulu |
| `[KEPUTUSAN DIBUTUHKAN]` | user atau produk harus memilih | usulan, dikonfirmasi dulu |
| `Wajib` | bertentangan dengan kebijakan yang tertulis di kode | fakta |

Penanda lama yang **tidak boleh** lagi ditulis: `[KEPUTUSAN]`,
`[perlu keputusan]`, `[kebijakan perlu ditentukan]`. Semuanya diganti
`[KEPUTUSAN DIBUTUHKAN]`. Pembaca masih mengenalinya di berkas lama, tetapi
`check_contract.py` menolaknya di berkas baru.

## Sebelum menyerahkan

Jalankan `scripts/check_contract.py <folder keluaran>`. Nol FAIL adalah syarat
menyerahkan. Komentar templat `<!-- ... -->` dan sisa `{{...}}` harus sudah
dihapus.
