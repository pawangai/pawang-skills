# Berkontribusi

Terima kasih sudah mau membantu. Aturan teknis skill ada di [AGENTS.md](AGENTS.md); dokumen ini mengatur alur kerja Git.

## Persiapan

```bash
git clone https://github.com/pawangai/pawang-skills.git
cd pawang-skills
git config core.hooksPath .githooks   # opsional: size guard dan cek pesan commit
bash scripts/validate-all.sh          # harus berakhir "SEMUA LOLOS"
```

Semua skrip memakai Python 3 standar dan bash. Jangan menambah dependensi tanpa diskusi di issue.

## Alur kerja

1. Buat branch dari `main` dengan awalan `feat/`, `fix/`, `chore/`, `docs/`, atau `refactor/` (mis. `feat/skill-baru`).
2. Satu PR = satu perubahan logis. Jangan campur fitur, refactor, dan format.
3. Jalankan `scripts/validate-all.sh` sebelum push.
4. Buka PR ke `main`. Judul PR mengikuti Conventional Commits karena menjadi pesan squash.
5. Setelah CI hijau dan PR disetujui, PR di-**squash merge**. Branch terhapus otomatis.

`main` selalu siap dirilis. Dilarang `git push --force` ke `main`.

## Pesan commit

Format: `tipe(opsional-scope): ringkasan imperatif`, subjek maksimal 72 karakter, tanpa titik di akhir. Isi pesan menjelaskan **mengapa**, bukan apa.

Tipe: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `ci`, `build`, `perf`, `style`, `revert`.

## Skill baru atau perubahan skill

Buat dan audit skill dengan `pawang-skill-creator`. Aturan frontmatter dan struktur folder ada di [AGENTS.md](AGENTS.md).

## Berkas besar dan biner

Berkas di atas 1 MB ditolak oleh size guard. Aset besar tidak boleh masuk riwayat `main`. Pilihan berurutan: Git LFS, object storage + CDN (R2/S3), lalu branch orphan untuk aset kecil yang jarang berubah (tidak pernah di-merge ke `main`).

## Rilis

Dikerjakan maintainer; langkahnya ada di bagian "Rilis" pada [AGENTS.md](AGENTS.md).

## Keamanan

Jangan membuka issue publik untuk kerentanan. Lihat [SECURITY.md](SECURITY.md).
