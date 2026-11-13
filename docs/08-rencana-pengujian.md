# 08 — Rencana Pengujian

Pengujian dibagi dua: **pengujian teknis** (aplikasi berjalan benar) dan **pengujian pedagogis** (aplikasi layak, praktis, dan efektif). Bagian kedua bisa disesuaikan dengan model penelitian pengembangan yang dipakai (ADDIE, 4D, atau Plomp).

## A. Pengujian Teknis

| Jenis | Alat | Cakupan |
|---|---|---|
| Unit test | pytest + mini-racer | `answer.js` (variasi rumus & angka), `pattern.js`, setiap kunci jawaban konten dinilai benar |
| Konten & server | pytest | Validator aturan pedagogis, manifest/ikon/service worker, endpoint penelitian, analisis data |
| End-to-end | Playwright (Python) + Edge & WebKit | Alur lengkap di Android 390 px, Android 320 px, dan iPhone (WebKit); installable & offline (Chromium) |
| Smartphone | `tests/e2e/test_ponsel.py` | Tidak ada geser ke samping, target sentuh ≥ 44 px, papan rumus, keyboard HP, lanjut setelah muat ulang, tabel vertikal |
| Kompatibilitas | Manual | Chrome Android (HP RAM 2–3 GB), Chrome/Edge/Firefox desktop, PWA terpasang di Android & iPhone |
| Offline | Manual + Lighthouse | Mode pesawat setelah kunjungan pertama |
| Performa | Lighthouse | Skor performa ≥ 80 di emulasi mobile |
| Aksesibilitas | Lighthouse + axe | Skor ≥ 90; kontras; label |

### Contoh kasus uji `answerChecker`

| Kunci | Input siswa | Diharapkan |
|---|---|---|
| `3n+1` | `3n + 1` | benar |
| `3n+1` | `1+3n` | benar |
| `3n+1` | `3×n+1` | benar |
| `3n+1` | `3n+4` | salah |
| `n^2` | `n²` | benar |
| `n(n+1)` | `n²+n` | benar |
| `n(n+1)/2` | `(n^2+n)/2` | benar |
| `3n+1` | `abc` | tidak valid → pesan "Rumus belum bisa dibaca" |

## B. Pengujian Pedagogis

### 1. Validasi Ahli
| Validator | Jumlah | Instrumen | Aspek |
|---|---|---|---|
| Ahli materi (dosen/guru matematika) | 2–3 | Angket skala 1–4 | Kesesuaian dengan CP/TP, kebenaran konsep, urutan, soal |
| Ahli media/desain | 1–2 | Angket skala 1–4 | Tampilan, navigasi, keterbacaan, prinsip multimedia |
| Ahli pembelajaran (opsional) | 1 | Lembar telaah | Penerapan prinsip beban kognitif |

Kriteria kelayakan (contoh): rata-rata ≥ 3,4 = sangat layak; 2,6–3,39 = layak; < 2,6 = revisi.

### 2. Uji Coba Bertahap
| Tahap | Peserta | Tujuan |
|---|---|---|
| Uji perorangan (one-to-one) | 3 siswa (kemampuan tinggi, sedang, rendah). Bisa melibatkan S01 bila bersedia | Menemukan masalah keterbacaan, navigasi, dan konten. Pakai metode *think-aloud* |
| Uji kelompok kecil | 6–10 siswa | Kepraktisan dan respons siswa |
| Uji lapangan | 1 kelas (±30 siswa) | Efektivitas: pretest–posttest, beban kognitif |

### 3. Instrumen Beban Kognitif
- **Skala usaha mental Paas (1992)**: satu butir, skala 9 poin, diberikan setelah tiap latihan (sudah ada di aplikasi, F16).
- **Kuesioner Leppink dkk. (2013)**: 10 butir yang memisahkan beban intrinsik, ekstrinsik, dan germane. Diberikan sekali setelah uji coba, di kertas/Google Form. Cocok untuk menyambungkan hasil dengan kerangka IL/EL/GL di wawancara.
  - Leppink, J., Paas, F., van der Vleuten, C. P. M., van Gog, T., & van Merriënboer, J. J. G. (2013). Development of an instrument for measuring different types of cognitive load. *Behavior Research Methods, 45*(4), 1058–1072.
- **Wawancara pasca uji coba**: memakai kerangka pengodean K/IL/EL/GL yang sama dengan studi pendahuluan, untuk membandingkan sebelum dan sesudah.

### 4. Instrumen Kepraktisan dan Efektivitas
- Angket respons siswa (skala Likert) dan/atau **System Usability Scale (SUS)**, 10 butir, target ≥ 68.
- Pretest–posttest (bisa memakai Tes Awal dan Kuis Akhir di aplikasi, atau tes tertulis paralel). Analisis dengan **N-gain**.

### 5. Instrumen Literasi Matematika
- **Tes literasi berbasis stimulus** (pretest & posttest paralel): 2–3 stimulus, masing-masing 3–4 soal L1–L3, mencakup indikator LM1–LM7 (dokumen 11). Bisa diambil atau diadaptasi dari contoh soal AKM Numerasi resmi.
- Validasi isi oleh ahli materi. Uji coba terbatas untuk menghitung validitas butir, reliabilitas, tingkat kesukaran, dan daya pembeda.
- **Rubrik soal uraian** (contoh):

| Skor | Merumuskan (LM1–LM2) | Menggunakan (LM3) | Menafsirkan (LM4–LM5) | Penalaran (LM6) |
|---|---|---|---|---|
| 0 | Tidak menuliskan informasi/model | Tidak ada perhitungan | Tidak memaknai hasil | Tidak memberi alasan |
| 1 | Informasi sebagian benar | Strategi tepat, hitungan salah | Menyebut hasil tanpa konteks | Alasan tidak relevan |
| 2 | Informasi benar, model kurang tepat | Hitungan benar, kurang lengkap | Memaknai hasil dalam konteks | Alasan relevan tetapi kurang lengkap |
| 3 | Informasi dan model benar | Strategi dan hitungan benar, lengkap | Memaknai dan menilai kewajaran hasil | Alasan logis dan lengkap |

- Analisis: N-gain total dan **per indikator**, untuk melihat proses mana yang paling berkembang.
- Wawancara pasca uji coba menambahkan pertanyaan literasi (lihat `01-analisis-kebutuhan.md` bagian 6).

### 6. Etika Uji Coba
- Izin sekolah dan **persetujuan orang tua/wali** untuk siswa di bawah umur.
- Identitas siswa disamarkan (S01, S02, …).
- Lihat `10-etika-dan-privasi.md`.

## C. Kriteria Lulus Rilis MVP
- [ ] Semua unit test dan E2E lulus
- [ ] Lighthouse: Performa ≥ 80, Aksesibilitas ≥ 90, PWA installable
- [ ] Berjalan offline
- [ ] Validasi ahli minimal kategori "layak"
- [ ] Hasil uji perorangan sudah ditindaklanjuti (revisi tercatat)
