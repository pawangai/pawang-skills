<!-- TEMPLAT 01-PRD. Heading bertanda WAJIB adalah kontrak (lihat references/contract.md): teks heading tidak boleh diubah. Bagian OPSIONAL dihapus seluruhnya bila jenis proyek tidak membutuhkannya; jangan isi teks generik. Isi setiap {{...}}, lalu hapus semua komentar ini. -->

# 01 - PRD: {{nama proyek}}

Penanda: `[ASUMSI]` = saya menyimpulkan, tidak ada bukti. `[KEPUTUSAN DIBUTUHKAN]` = user atau produk harus memilih. `Wajib` = bertentangan dengan kebijakan yang tertulis di kode.

## Ringkasan
<!-- WAJIB. Satu paragraf: dari apa menjadi apa, dan tiga janji utamanya. -->
{{ringkasan}}

## Masalah (kondisi saat ini)
<!-- OPSIONAL (ada sistem atau prototype yang sudah ada). Tabel per modul atau halaman dengan angka dari inventory.py, lalu akar masalah dengan bukti kode. -->
{{tabel kondisi dan akar masalah}}

## Tujuan dan non-tujuan
<!-- WAJIB. Non-tujuan wajib ada; itu yang mencegah scope melebar. -->
| ID | Tujuan |
| --- | --- |
| G1 | {{tujuan}} |

Non-tujuan: {{apa yang sengaja tidak dikerjakan}}

## Pengguna dan peran
<!-- WAJIB. Hanya peran yang terlihat di kode atau dijawab user. -->
{{peran}}

## Arsitektur target
<!-- OPSIONAL. -->
{{struktur folder, aturan modul}}

## Shell
<!-- OPSIONAL (ERP atau multi-modul, atau situs dengan navigasi bersama). -->
{{kolom, perilaku, breakpoint}}

## Pemetaan modul
<!-- OPSIONAL. Basepath, menu per modul, tabel redirect URL lama ke baru. -->
{{tabel}}

## Sitemap
<!-- OPSIONAL (web profile, landing page, situs dokumentasi). -->
{{daftar halaman}}

## Model konten
<!-- OPSIONAL. -->
{{jenis konten dan pemiliknya}}

## Funnel
<!-- OPSIONAL (bisnis, landing page, e-commerce). -->
{{tahapan funnel}}

## Konflik yang harus diselesaikan
<!-- OPSIONAL. ID C1.., bukti, rekomendasi, status. -->
| ID | Konflik | Bukti | Rekomendasi | Status |
| --- | --- | --- | --- | --- |
| C1 | {{konflik}} | {{screen atau file}} | {{rekomendasi}} | [KEPUTUSAN DIBUTUHKAN] |

## Requirement fungsional
<!-- WAJIB. Setiap baris FR memuat tepat satu prioritas P0, P1, atau P2. -->
| ID | Requirement | Prioritas | Sumber |
| --- | --- | --- | --- |
| FR-1 | {{requirement}} | P0 | {{bukti atau jawaban user}} |

## Requirement non-fungsional
<!-- WAJIB. -->
| ID | Requirement | Sumber |
| --- | --- | --- |
| NFR-1 | {{requirement}} | {{sumber}} |

## Strategi migrasi
<!-- OPSIONAL (ada sistem lama). Fase, urutan, dan "selesai bila". -->
{{fase}}

## Risiko dan trade-off
<!-- OPSIONAL. -->
| ID | Risiko | Mitigasi |
| --- | --- | --- |
| R1 | {{risiko}} | {{mitigasi}} |

## Keputusan terbuka
<!-- WAJIB. Setiap [KEPUTUSAN DIBUTUHKAN] di dokumen mana pun punya baris di sini. -->
| ID | Keputusan | Rekomendasi | Dampak bila ditunda |
| --- | --- | --- | --- |
| Q1 | {{keputusan}} | {{rekomendasi}} | {{dampak}} |

## Metrik keberhasilan
<!-- WAJIB. -->
| Metrik | Sekarang | Target |
| --- | --- | --- |
| {{metrik}} | {{nilai}} | {{nilai}} |
