# Implementasi Teknis

Baca file ini hanya saat user meminta kode tema. Pilih satu format sesuai stack user; bila belum diketahui, tanyakan dulu. Isi nilai dari palet dan font yang sudah dihasilkan, bukan dari contoh di bawah.

## Daftar isi
- CSS Variables
- Tailwind
- Agent rules (CLAUDE.md)

## CSS Variables
```css
:root {
  --color-primary: #RRGGBB;
  --color-accent: #RRGGBB;
  --color-bg: #RRGGBB;
  --color-support: #RRGGBB;
  --color-text: #RRGGBB;
  --font-heading: "Nama Font", Georgia, serif;
  --font-body: "Nama Font", system-ui, sans-serif;
}
```
Bila situs mendukung mode gelap, tambahkan override di `@media (prefers-color-scheme: dark)` dan cek ulang kontras.

## Tailwind
Tailwind v3 memakai `theme.extend.colors` dan `fontFamily` di `tailwind.config.js`. Tailwind v4 memakai blok `@theme` di CSS. Tanyakan versinya sebelum menulis, karena sintaksnya berbeda.

## Agent rules (CLAUDE.md)
Isi ringkas dan bisa dipatuhi agent:
- Nama brand, metafora, dan tone of voice (satu paragraf).
- Daftar kata dianjurkan dan dilarang.
- Token warna dan font beserta perannya.
- Larangan visual dan aturan kontras (teks minimal 4.5:1).
- Instruksi bahwa fakta bisnis yang belum ada ditulis `[ISI: ...]`, tidak dikarang.
