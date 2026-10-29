# pawang-skills

Skill (format Agent Skills) milik Pawang, dengan marketplace untuk Claude Code dan Codex, dan paket ZIP untuk aplikasi chat. Satu folder per skill di `skills/`. Lisensi MIT.

## Daftar skill

| Skill | Fungsi |
|---|---|
| `interview` | Mewawancarai user per ronde bernomor dengan rekomendasi jawaban, supaya tidak ada keputusan atau asumsi diam-diam. Mode penuh dan mode ringan. |
| `panduan-brand` | Membuat panduan brand lengkap sebagai berkas Markdown. |
| `brandboard-standard` | Menyusun dan mengaudit brand board satu halaman dengan struktur section standar. |
| `plans-prototype` | Menghasilkan 4 dokumen perencanaan prototype (PRD, flow, desain, edge case), lalu memandu iterasi prototype. |
| `pawang-skill-creator` | Membuat, mengaudit, dan memperbaiki skill baru. Berisi `scripts/validate_skill.py`. |

Urutan pemakaian: `panduan-brand` → `brandboard-standard` → `plans-prototype`. `interview` dipanggil ketiganya bila ada keputusan yang belum jelas, jadi pasang `interview` bersama skill lain.

## Memasang

Tidak ada satu marketplace untuk semua agent, jadi ada tiga jalur.

### 1. Agent CLI (OpenCode, Pi, Antigravity, Gemini CLI, Codex, Claude Code, Cursor, Copilot, dan lainnya)

```bash
npx skills add pawangai/pawang-skills                    # pilih skill dan agent secara interaktif
npx skills add pawangai/pawang-skills --all -g           # semua skill, semua agent terdeteksi, tingkat user
npx skills add pawangai/pawang-skills --skill interview  # satu skill
```

CLI mendeteksi agent yang terpasang dan menaruh skill di direktori masing-masing.

### 2. Marketplace bawaan

| Agent | Perintah |
|---|---|
| Claude Code | `/plugin marketplace add pawangai/pawang-skills` lalu `/plugin install pawang-skills@pawang` |
| Codex | `codex plugin marketplace add pawangai/pawang-skills` lalu `codex plugin add pawang-skills@pawang` |
| Gemini CLI | `gemini skills install https://github.com/pawangai/pawang-skills.git --path skills` |

Pembaruan: `/plugin marketplace update pawang` (Claude Code), `codex plugin marketplace upgrade pawang` (Codex).

### 3. Aplikasi chat (claude.ai, ChatGPT, Gemini app, Perplexity)

Aplikasi ini tidak punya marketplace berbasis URL. Unduh ZIP per skill dari halaman [Releases](https://github.com/pawangai/pawang-skills/releases) lalu unggah satu per satu:

| Aplikasi | Cara |
|---|---|
| claude.ai | Menu Skills di pengaturan, unggah `<nama>.zip` atau `<nama>.skill` |
| ChatGPT | Customize → Skills → "+" → Create skill → Upload a skill, unggah `<nama>.zip` |
| Gemini app | Settings → Skills → Upload, unggah `<nama>.zip` |
| Perplexity | Hanya lewat API Portal sebagai custom skill (ZIP berisi satu folder dan satu `SKILL.md`) |

Catatan: `plans-prototype` berisi skrip Python, dan sebagian aplikasi chat dilaporkan menolak paket berskrip. Bila unggahan ditolak, buka issue.

## Dependensi

- `plans-prototype` memanggil `interview` untuk wawancara (langkah 0).
- `plans-prototype` membaca kontrak dokumen milik skill `plan` Pawang (`references/contract.md`, opsi `--reader` di `check_contract.py`). Skill `plan` **tidak ada di repo ini**.
- `panduan-brand` menyebut tool runtime Pawang (`SendUserFile`, `WebSearch`). Di agent lain, ganti dengan tool setara.
- Python 3 tanpa paket tambahan untuk semua skrip.

## Pengembangan

```bash
scripts/validate-all.sh         # validasi skill, manifest, dan sintaks skrip
scripts/package.sh              # semua skill -> dist/<nama>.zip dan dist/<nama>.skill
scripts/package.sh interview    # satu skill
```

`validate-all.sh` memeriksa: `name` sama dengan folder, `license`, `compatibility`, dan `metadata.author` di frontmatter; hasil `validate_skill.py`; JSON manifest, nama, dan sinkronisasi versi; serta sintaks skrip Python. Aturan perubahan ada di `AGENTS.md`.

## Struktur

```
skills/<nama>/SKILL.md          # sumber tunggal semua skill
.claude-plugin/                 # plugin dan marketplace Claude Code
.codex-plugin/                  # plugin Codex
.agents/plugins/marketplace.json  # marketplace Codex
scripts/                        # validasi dan pengemasan
.github/workflows/              # CI dan rilis
```
