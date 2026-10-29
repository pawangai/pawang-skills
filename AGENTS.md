# AGENTS.md

Aturan mengubah repo ini.

- Semua skill di `skills/` berstatus final. Ubah hanya untuk fitur baru atau perbaikan yang diminta user.
- Keputusan yang belum jelas ditanyakan lewat skill `interview`; jangan diasumsikan.
- `name` di frontmatter harus sama dengan nama folder. Frontmatter wajib memuat `metadata.author: "Pawang"`.
- Skill baru dibuat dengan `pawang-skill-creator`.
- Skrip hanya memakai pustaka standar Python 3. Jangan menambah paket baru tanpa konfirmasi.
- Jalankan `scripts/validate-all.sh` sebelum commit; wajib tanpa FAIL.
- Commit memakai prefiks konvensional (`feat:`, `fix:`, `docs:`). Jangan `git push --force` atau `git reset --hard`.
- Skill `plan` Pawang adalah dependensi eksternal; jangan menyalinnya ke repo ini.
