# 09 — Roadmap Pengerjaan

Perkiraan untuk satu orang yang mengerjakan paruh waktu. Sesuaikan dengan jadwal kuliah atau skripsi.

| Fase | Minggu | Kegiatan | Keluaran |
|---|---|---|---|
| **0. Analisis** | 1–2 | Tambah wawancara (3–5 siswa + 1 guru), analisis CP, finalisasi dokumen perencanaan | Dokumen 01–04 final |
| **1. Desain** | 3–4 | Wireframe di Figma, naskah video M1–M3, bank soal M0–M3, skema konten | Prototipe Figma, file JSON konten awal |
| **2. Fondasi teknis** ✅ | 5 | Frontend JS murni, router, localStorage, PWA (manifest + service worker), server Flask, validator konten, pytest | Aplikasi yang bisa dipasang & offline |
| **3. Komponen inti** ✅ | 6–7 | PatternRow, DifferenceArrows, DotPattern, HintBox, FeedbackSheet, MathKeypad, answerChecker + test | Pustaka komponen |
| **4. Alur belajar** ✅ | 8–9 | Layar konsep, contoh lengkap, setengah jadi, latihan, Cek Aturanmu, refleksi, skala Paas | Modul M2 lengkap dari awal sampai akhir (vertical slice) |
| **5. Uji perorangan** | 10 | Uji M2 dengan 3 siswa (think-aloud), lalu revisi | Catatan revisi |
| **6. Konten lengkap** 🟡 (M0–M6 dan tes ✅; M7, M8 = gelombang 3) | 11–13 | Isi modul M0–M8, video, tes awal, kuis | Semua modul |
| **6b. Literasi** 🟡 (komponen ✅, stimulus M2 & M4 ✅) | 12–14 | Komponen literasi (StimulusCard, sorot, Diketahui–Ditanya, CycleStepper, Setuju/Tidak, menjodohkan), stimulus untuk M1–M8, tes literasi pretest/posttest, Profil Literasi | F20–F25, instrumen tes literasi |
| **7. Progres & ekspor** ✅ | 14 | Peta progres, ekspor data penelitian | F13, F17 |
| **8. Deploy & HP** | 15 | Deploy HTTPS (GitHub Pages/Netlify), uji pasang di beberapa HP Android & iPhone, APK opsional via PWABuilder | Alamat aplikasi untuk siswa |
| **9. Validasi ahli** | 15–16 | Validasi materi & media, revisi | Lembar validasi, versi revisi |
| **10. Uji coba** | 17–19 | Kelompok kecil → lapangan | Data kepraktisan & efektivitas |
| **11. Fase 2 (opsional)** | — | Supabase, dashboard guru, fitur berbagi cara, proyek mini "Pola di Sekitarku" | F18, F19, F26 |

> Status per 12 November 2026: ✅ selesai, 🟡 sebagian. **Langkah berikutnya:** Fase 5 (uji M2 ke 3 siswa) dan Fase 8 (deploy HTTPS).

## Milestone

- **M-A: Vertical slice (akhir minggu 9).** Satu modul lengkap, **termasuk 1 stimulus literasi**, bisa dipakai siswa. Ini titik paling penting. Uji ke siswa sedini mungkin.
- **M-B: MVP lengkap (akhir minggu 14).**
- **M-C: Siap uji coba (akhir minggu 16).**

## Tips Kerja dengan Claude Code

1. Kerjakan per fitur kecil, mulai dari user story di `05-user-stories.md`. Contoh prompt: *"Implementasikan US-10 (petunjuk bertingkat) sesuai CLAUDE.md dan 03-desain-pembelajaran.md bagian 5."*
2. Minta Claude menulis unit test terlebih dahulu untuk `answerChecker` dan `patternEngine`.
3. Konten (soal, teks) **buat dan periksa sendiri** sebagai ahli pendidikan matematika. AI boleh membantu membuat draf, tetapi kebenaran konsep tanggung jawabmu.
4. Commit setiap fitur selesai. Perbarui dokumen bila keputusan berubah.
