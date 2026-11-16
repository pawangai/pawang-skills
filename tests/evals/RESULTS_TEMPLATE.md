# Catatan hasil behavioral evaluation

Gunakan satu salinan file ini untuk setiap kombinasi harness dan model. Jangan isi status PASS sebelum prompt benar-benar dijalankan.

## Lingkungan

- Tanggal:
- Harness dan versi:
- Model dan versi:
- Versi/commit repository:
- Skill aktif:
- Baseline tanpa skill dijalankan: ya / tidak
- Penilai:

## Skenario perilaku

Untuk setiap skenario di `cases.json`, jalankan prompt yang sama dengan skill aktif dan (bila memungkinkan) tanpa skill. Nilai semua kriteria `must` dan `must_not`.

| Case ID | Dengan skill | Tanpa skill | Perubahan hasil yang terlihat | Catatan |
|---|---|---|---|---|
| interview-01-raw-product-idea | Belum diuji | Belum diuji | | |
| interview-02-dependent-decisions | Belum diuji | Belum diuji | | |
| interview-03-no-approval-gate | Belum diuji | Belum diuji | | |
| make-theme-01-umkm-theme | Belum diuji | Belum diuji | | |
| make-theme-02-palette-only | Belum diuji | Belum diuji | | |
| make-theme-03-seo-only-nearmiss | Belum diuji | Belum diuji | | |
| panduan-brand-01-guideline-from-brief | Belum diuji | Belum diuji | | |
| panduan-brand-02-unknown-name-and-domain | Belum diuji | Belum diuji | | |
| panduan-brand-03-theme-not-document | Belum diuji | Belum diuji | | |
| plans-prototype-01-new-laundry-app | Belum diuji | Belum diuji | | |
| plans-prototype-02-existing-prototype-without-plan | Belum diuji | Belum diuji | | |
| plans-prototype-03-single-code-change | Belum diuji | Belum diuji | | |
| skill-creator-01-invoice-skill | Belum diuji | Belum diuji | | |
| skill-creator-02-destructive-migration | Belum diuji | Belum diuji | | |
| skill-creator-03-review-existing-skill | Belum diuji | Belum diuji | | |

## Tes aktivasi

Catat PASS hanya jika lima prompt `should_activate` memicu skill yang tepat dan lima prompt `should_not_activate` tidak memicunya.

| Skill | 5 prompt aktivasi | 5 near-miss | Catatan |
|---|---|---|---|
| interview | Belum diuji | Belum diuji | |
| make-theme | Belum diuji | Belum diuji | |
| panduan-brand | Belum diuji | Belum diuji | |
| plans-prototype | Belum diuji | Belum diuji | |
| pawang-skill-creator | Belum diuji | Belum diuji | |

## Ringkasan

- Total skenario lulus:
- Total skenario gagal:
- Temuan yang dapat direproduksi:
- Perbaikan yang diusulkan:
- Model/harness lain yang belum diuji:

Jangan menggeneralisasi hasil satu model ke model atau harness lain. Simpan respons mentah atau tautan run yang diperlukan agar penilaian dapat diaudit.
