# PolaKu — Aplikasi Belajar Pola Bilangan untuk Siswa SMP

> Nama "PolaKu" masih nama kerja dan bisa diganti.

Aplikasi pembelajaran matematika materi **Pola Bilangan** (Kelas VII SMP, Kurikulum Merdeka Fase D).
Aplikasi ini **dibuka di browser** dan **bisa dipasang di HP/laptop tanpa Play Store atau App Store** (PWA),
serta bisa dipakai **tanpa internet** setelah kunjungan pertama.

Desainnya mengikuti **Teori Beban Kognitif (Cognitive Load Theory)**, berdasarkan hasil wawancara awal dengan
siswa, dan bertujuan **menumbuhkembangkan literasi matematika** (kerangka PISA 2022 dan AKM Numerasi).

**Bahasa pemrograman:** JavaScript (aplikasi di browser) dan Python (server, validasi konten, analisis data, pengujian).

## Status

MVP berjalan. **7 dari 9 modul sudah lengkap**: M0 (Prasyarat), M1 (Mengenal Pola), M2 (Selisih Tetap),
M3 (Ganjil & Genap), M4 (Persegi & Persegi Panjang), M5 (Segitiga), dan M6 (Fibonacci). Setiap modul berisi konsep, contoh, contoh setengah jadi,
latihan, soal cerita literasi, refleksi, dan kuis. Tes Awal dan Tes Akhir juga sudah ada.
M7 dan M8 masih "Segera hadir" (gelombang 3, lihat `docs/AUDIT_KONTEN_MODUL.md`).

## Mulai Cepat

```bash
cd aplikasi-pola-bilangan
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python server/app.py            # buka http://localhost:5000
```

Panduan memasang di HP, deploy, dan membuat APK ada di [docs/12-panduan-instalasi-dan-deploy.md](docs/12-panduan-instalasi-dan-deploy.md).

## Perintah Penting

| Perintah | Fungsi |
|---|---|
| `python server/app.py` | Menjalankan aplikasi (http://localhost:5000) |
| `python tools/validasi_konten.py` | Memeriksa konten terhadap aturan pedagogis |
| `python tools/build_aset.py` | Memperbarui daftar aset offline sebelum deploy |
| `python tools/analisis_data.py <folder>` | Mengolah data penelitian menjadi CSV + N-gain |
| `python -m pytest` | Menjalankan semua pengujian (logika, konten, server, analisis, browser) |
| `python tools/buat_ikon.py` | Membuat ulang ikon aplikasi |
| `python tools/buat_ilustrasi.py` | Membuat ulang ilustrasi & ikon modul (jumlah noktah dihitung kode) |
| `python tools/buat_kunci_rubrik.py` | Memperbarui `docs/13` (kunci jawaban & rubrik) dari konten |

## Struktur

```
frontend/          aplikasi (HTML, CSS, JavaScript), bisa di-hosting statis
  js/              logika & halaman      konten/   materi & soal (JSON)
server/app.py      server Flask (menyajikan aplikasi + terima data penelitian opsional)
tools/             skrip Python: validasi konten, build aset, analisis data, ikon
tests/             pytest (+ tests/e2e: uji di browser sungguhan)
docs/              dokumen perencanaan
```

## Daftar Dokumen

| Dokumen | Isi |
|---|---|
| [CLAUDE.md](CLAUDE.md) | Panduan untuk AI coding assistant: konteks, aturan, konvensi |
| [docs/01-analisis-kebutuhan.md](docs/01-analisis-kebutuhan.md) | Sintesis hasil wawancara → kebutuhan aplikasi |
| [docs/02-PRD.md](docs/02-PRD.md) | Product Requirements Document |
| [docs/03-desain-pembelajaran.md](docs/03-desain-pembelajaran.md) | Prinsip Teori Beban Kognitif dan alur belajar |
| [docs/04-konten-materi.md](docs/04-konten-materi.md) | Peta materi, tujuan pembelajaran, bank soal |
| [docs/05-user-stories.md](docs/05-user-stories.md) | User story + kriteria penerimaan |
| [docs/06-desain-ui-ux.md](docs/06-desain-ui-ux.md) | Alur layar, wireframe, panduan visual |
| [docs/07-arsitektur-teknis.md](docs/07-arsitektur-teknis.md) | Tech stack, struktur folder, model data |
| [docs/08-rencana-pengujian.md](docs/08-rencana-pengujian.md) | Pengujian teknis + uji coba ke siswa |
| [docs/09-roadmap.md](docs/09-roadmap.md) | Tahapan pengerjaan dan milestone |
| [docs/10-etika-dan-privasi.md](docs/10-etika-dan-privasi.md) | Perlindungan data siswa |
| [docs/11-literasi-matematika.md](docs/11-literasi-matematika.md) | Kerangka literasi matematika, siklus pemecahan masalah |
| [docs/12-panduan-instalasi-dan-deploy.md](docs/12-panduan-instalasi-dan-deploy.md) | Menjalankan, memasang tanpa toko aplikasi, deploy, APK |
| [docs/13-kunci-dan-rubrik-modul.md](docs/13-kunci-dan-rubrik-modul.md) | Kunci jawaban, pembahasan, dan rubrik refleksi tiap modul (dibuat otomatis) |
| [docs/AUDIT_KONTEN_MODUL.md](docs/AUDIT_KONTEN_MODUL.md) | Audit & rencana konten M0–M8, keputusan cakupan |
