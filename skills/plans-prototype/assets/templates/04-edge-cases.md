<!-- TEMPLAT 04-edge-cases. Teks heading `Kerjakan dulu (blocker desain)` dan `Butuh keputusan produk sebelum didesain` adalah kontrak (lihat references/contract.md). Baris edge case memakai format persis di bawah dan berakhir `| Sev | Dasar |` tanpa kolom tambahan. Isi setiap {{...}}, lalu hapus semua komentar ini. -->

# 04 - Edge Cases: {{nama proyek}}

Format baris: `| EC-XX-NN | Skenario | Perilaku yang diharapkan | Frame | Sev | Dasar |`
Sev: `K` kritis, `T` tinggi, `S` sedang, `R` rendah. Dasar: `P` terlihat di prototype atau dokumen sumber, `U` usulan. Edge case yang butuh kebijakan bisnis diberi `[KEPUTUSAN DIBUTUHKAN]` di kolom perilaku.

## {{Area, kode XX}}
| ID | Skenario | Perilaku yang diharapkan | Frame | Sev | Dasar |
| --- | --- | --- | --- | --- | --- |
| EC-XX-01 | {{skenario}} | {{keputusan desain konkret}} | {{nomor frame atau baru}} | S | U |

## Ringkasan
<!-- Salin keluaran `python scripts/edge_summary.py 04-edge-cases.md`; jangan hitung manual. -->
{{tabel per area, total, sebaran severity dan dasar}}

## Kerjakan dulu (blocker desain)
- {{hal yang menghambat desain final, dengan ID EC atau Q}}

## Butuh keputusan produk sebelum didesain
- {{keputusan, dengan ID Q atau EC}}
