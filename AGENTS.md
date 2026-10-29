# AGENTS.md

Aturan mengubah repo ini.

- Semua skill di `skills/` berstatus final. Ubah hanya untuk fitur baru atau perbaikan yang diminta user.
- Keputusan yang belum jelas ditanyakan lewat skill `interview`; jangan diasumsikan.
- `name` di frontmatter harus sama dengan nama folder. Frontmatter wajib memuat `license: MIT`, `compatibility`, dan `metadata.author: "Pawang"`.
- Skill baru dibuat dengan `pawang-skill-creator`.
- `skills/` adalah satu-satunya sumber skill. Jangan menyalinnya ke folder lain; manifest plugin menunjuk ke sana.
- Jangan menambah `$schema` di manifest Claude Code (ditolak CLI).
- Skrip hanya memakai pustaka standar Python 3. Jangan menambah paket baru tanpa konfirmasi.
- Jalankan `scripts/validate-all.sh` sebelum commit; wajib tanpa FAIL.
- Commit memakai prefiks konvensional (`feat:`, `fix:`, `docs:`). Jangan `git push --force` atau `git reset --hard`.
- Skill `plan` Pawang adalah dependensi eksternal; jangan menyalinnya ke repo ini.

## Rilis

1. Naikkan `version` di `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (dua tempat), dan `.codex-plugin/plugin.json`. Validator menolak versi yang tidak sinkron.
2. Jalankan `scripts/validate-all.sh`.
3. Commit, lalu buat tag `vX.Y.Z` yang sama dengan versi manifest dan push tag. Workflow `release.yml` mengemas semua skill dan melampirkannya ke GitHub Release.
