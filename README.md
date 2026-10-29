# pawang-skills

Kumpulan skill (format Agent Skills) milik Pawang. Satu folder per skill di `skills/`.

## Daftar skill

| Skill | Fungsi |
|---|---|
| `interview` | Mewawancarai user per ronde bernomor dengan rekomendasi jawaban, supaya tidak ada keputusan atau asumsi diam-diam. Mode penuh dan mode ringan. |
| `panduan-brand` | Membuat panduan brand lengkap sebagai berkas Markdown. |
| `brandboard-standard` | Menyusun dan mengaudit brand board satu halaman dengan struktur section standar. |
| `plans-prototype` | Menghasilkan 4 dokumen perencanaan prototype (PRD, flow, desain, edge case), lalu memandu iterasi prototype. |
| `pawang-skill-creator` | Membuat, mengaudit, dan memperbaiki skill baru. Berisi `scripts/validate_skill.py`. |

## Urutan pemakaian

`panduan-brand` → `brandboard-standard` → `plans-prototype`

Panduan brand menjadi bahan Brand Spec. Brand board menjadi acuan token untuk prototype. `interview` dipanggil oleh ketiganya bila ada keputusan yang belum jelas, dan `pawang-skill-creator` dipakai saat menambah atau mengubah skill.

## Memasang

Salin folder skill yang dibutuhkan ke direktori skill agent di proyek tujuan:

```bash
cp -r skills/interview /path/proyek/.agents/skills/      # atau .claude/skills/
```

Atau kemas menjadi berkas `.skill`:

```bash
scripts/package.sh              # semua skill -> dist/<nama>.skill
scripts/package.sh interview    # satu skill
```

## Dependensi

- `plans-prototype` memanggil `interview` untuk wawancara (langkah 0).
- `plans-prototype` membaca kontrak dokumen milik skill `plan` Pawang (`references/contract.md`, opsi `--reader` di `check_contract.py`). Skill `plan` **tidak ada di repo ini**; pasang terpisah bila memakai opsi tersebut.
- Beberapa skill menyebut tool runtime Pawang (`AskUserQuestion`, `SendUserFile`, `WebSearch`). Di agent lain, ganti dengan tool yang setara.
- Python 3 tanpa paket tambahan untuk semua skrip.

## Validasi

```bash
scripts/validate-all.sh
```

Memeriksa: `name` sama dengan nama folder, `metadata.author` berisi "Pawang", hasil `validate_skill.py` tiap skill, dan sintaks semua skrip Python. Exit 1 bila ada FAIL. WARN dari validator tidak menggagalkan.

## Konvensi

- Frontmatter memakai `metadata.author: "Pawang"` (field `author` di luar `metadata` ditolak validator spesifikasi).
- Aturan perubahan ada di `AGENTS.md`.
