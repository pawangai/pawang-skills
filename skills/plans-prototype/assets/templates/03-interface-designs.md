<!-- TEMPLAT 03-interface-designs. Teks heading `Flow -> frame` dan `Inventaris frame` adalah kontrak (lihat references/contract.md). Bagian Shell OPSIONAL. Isi setiap {{...}}, lalu hapus semua komentar ini. -->

# 03 - Interface Designs: {{nama proyek}}

Merujuk `01-PRD.md` dan `02-user-flows.md`. Nilai yang saya usulkan sendiri ditandai `[ASUMSI]` beserta asal angkanya.

## Shell
<!-- OPSIONAL. Grid dan lebar kolom (hitung dari angka nyata), mode layout, komponen, state, responsif, aksesibilitas. -->
{{spesifikasi shell}}

## Flow -> frame
| Flow | Urutan frame |
| --- | --- |
| F0 | {{nomor frame}} |

Frame baru (belum ada di prototype): {{daftar}}

## Inventaris frame
Konvensi nama frame: `{{template}}/{{bagian}}/{{#nomor}} {{Nama}} — {{state}}`.

| # | Template atau modul | Bagian | Layout | State | Frame |
| --- | --- | --- | --- | --- | --- |
| {{nomor}} | {{template}} | {{bagian}} | {{layout}} | {{state}} | {{nama frame}} |
