# 02 — Product Requirements Document (PRD)

| | |
|---|---|
| Produk | PolaKu (nama kerja) |
| Versi dokumen | 0.1 (draf) |
| Tanggal | 12 November 2026 |
| Penyusun | Shofwatunnida, S1 Pendidikan Matematika |
| Status | Perencanaan |

## 1. Latar Belakang

Studi pendahuluan (wawancara siswa S01, lihat `01-analisis-kebutuhan.md`) menunjukkan bahwa siswa:
- kesulitan mengenali hubungan antarsuku pada pola bilangan (beban intrinsik tinggi),
- belajar hanya dengan papan tulis dan latihan soal dengan tempo yang ditentukan guru (beban ekstrinsik),
- merasa lebih terbantu dengan video, tetapi belum punya strategi memeriksa jawaban atau mengatasi kebuntuan (beban germane rendah).

Selain itu, literasi matematika siswa Indonesia masih rendah: skor matematika PISA 2022 adalah 366, sedangkan rata-rata OECD 472. Pembelajaran yang hanya berisi latihan soal rutin (EL02) jarang melatih siswa memakai matematika dalam situasi nyata.

## 2. Tujuan Produk

1. Membantu siswa **mengenali, menjelaskan, dan menggeneralisasi** pola bilangan.
2. Menyajikan materi dengan desain yang **menurunkan beban kognitif ekstrinsik**.
3. Membiasakan strategi **memeriksa ulang** dan **menjelaskan kembali**.
4. Dapat diakses di **web dan Android**, termasuk **offline**.
5. **Menumbuhkembangkan literasi matematika**: siswa mampu merumuskan situasi nyata sebagai pola, menyelesaikannya, menafsirkan hasilnya dalam konteks, dan bernalar tentangnya (PISA 2022, AKM Numerasi).

### Di luar ruang lingkup (MVP)
- Materi selain Pola Bilangan
- Login akun siswa, kelas online, chat
- Papan peringkat kompetitif
- Dashboard guru (direncanakan Fase 2)

## 3. Pengguna Sasaran

### Persona utama — "Siswa yang mudah lupa" (berdasarkan S01)
- Sasaran aplikasi: siswa **kelas VII** SMP (usia 12–13 tahun). Persona disusun dari responden S01 (kelas VIII) yang mengingat materi ini dari kelas VII.
- Memakai HP Android milik sendiri atau keluarga.
- Pernah belajar pola bilangan tetapi "lupa banget".
- Lambat menemukan selisih antarsuku, cenderung berhenti ketika buntu.
- Lebih nyaman belajar dengan video daripada membaca teks panjang.
- **Kebutuhan:** penjelasan bertahap, contoh yang jelas, bantuan saat buntu, belajar dengan tempo sendiri.

### Persona sekunder — Guru matematika SMP
- Ingin media yang bisa dipakai di kelas atau untuk tugas di rumah.
- **Kebutuhan (Fase 2):** melihat progres dan kesulitan siswa.

## 4. Fitur

Prioritas: **P0** = wajib ada di MVP, **P1** = sebaiknya ada di MVP, **P2** = fase berikutnya.

| ID | Fitur | Deskripsi | Dasar (kode wawancara) | Prioritas |
|---|---|---|---|---|
| F01 | Tes Awal (Diagnostik) | 5–8 soal singkat untuk memetakan prasyarat; hasilnya merekomendasikan titik mulai | K03 | P0 |
| F02 | Pengingat Prasyarat | Kilas balik singkat: barisan, suku, selisih, bilangan ganjil/genap/persegi | K01, K03 | P1 |
| F03 | Materi Bersegmen | Satu konsep per layar: video pendek (1–3 menit) + visual + maksimal 3 kalimat | EL01, GL01 | P0 |
| F04 | Visualisasi Selisih | Panah lompatan antarsuku (+3, +3, …), bisa ditampilkan bertahap | IL01, IL02 | P0 |
| F05 | Representasi Ganda | Pola ditampilkan sebagai noktah/objek, tabel, barisan bilangan, dan rumus | EL01 | P0 |
| F06 | Contoh Lengkap (Worked Example) | Penyelesaian langkah demi langkah, langkah muncul satu per satu | IL02 | P0 |
| F07 | Contoh Setengah Jadi (Faded Example) | Beberapa langkah dikosongkan untuk diisi siswa; makin lama makin banyak yang dikosongkan | IL02, GL03 | P0 |
| F08 | Latihan Interaktif | Isian, pilihan ganda, seret-lepas suku, melengkapi tabel | EL02 | P0 |
| F09 | Petunjuk Bertingkat | 3 tingkat petunjuk per soal | GL03 | P0 |
| F10 | Umpan Balik yang Menjelaskan | Untuk jawaban salah: jelaskan kekeliruan yang mungkin terjadi | GL03 | P0 |
| F11 | "Cek Aturanmu" | Siswa menguji rumus suku ke-n ke suku yang sudah diketahui sebelum mengirim jawaban | GL02 | P0 |
| F12 | "Jelaskan dengan Kata-katamu" | Kolom refleksi singkat/pilihan kalimat untuk menjelaskan cara menemukan pola | GL04 | P1 |
| F13 | Progres Belajar | Peta materi dengan tanda selesai; disimpan di perangkat | — | P1 |
| F14 | Mode Offline (PWA) | Materi dan latihan bisa diakses tanpa internet setelah unduhan pertama | EL02 (belajar di rumah) | P0 |
| F15 | Kuis Akhir Topik | Penilaian sumatif per subtopik, tanpa batas waktu | — | P1 |
| F16 | Skala Beban Kognitif Mandiri | Setelah latihan, siswa menilai "seberapa berat usaha mentalmu?" (skala 1–9, Paas). Data untuk penelitian | penelitian | P1 |
| F17 | Ekspor Data Penelitian | Ekspor progres/skor/skala beban kognitif ke file (anonim) untuk analisis peneliti | penelitian | P1 |
| F18 | Dashboard Guru | Rekap progres kelas (memerlukan backend) | — | P2 |
| F19 | Berbagi Cara | Siswa berbagi penjelasan pola dengan teman (kolaboratif) | GL04 | P2 |

**Fitur literasi matematika** (detail di `11-literasi-matematika.md`):

| ID | Fitur | Deskripsi | Dasar | Prioritas |
|---|---|---|---|---|
| F20 | Siklus Pemecahan Masalah | Soal kontekstual dipandu siklus BACA → UBAH → HITUNG → CEK CERITA, dengan bantuan yang dikurangi bertahap | PISA (merumuskan–menggunakan–menafsirkan), GL03 | P0 |
| F21 | Bantuan Membaca Stimulus | Sorot informasi penting, kartu Diketahui–Ditanya, ketuk istilah untuk melihat artinya | GL03, beban ekstrinsik | P0 |
| F22 | Setuju atau Tidak? | Soal penalaran: menilai klaim tokoh, memilih atau menulis alasan | GL04, PISA (penalaran) | P0 |
| F23 | Stimulus Bergaya AKM | Satu stimulus (cerita + gambar/tabel) untuk 3–4 soal berjenjang L1–L3; bentuk soal: PG, PG kompleks, menjodohkan, isian, uraian singkat | AKM Numerasi | P1 |
| F24 | Cek Cerita | Setelah menghitung, siswa memaknai hasil dalam konteks dan menilai kewajarannya ("Apakah boleh pecahan?") | GL02, PISA (menafsirkan) | P0 |
| F25 | Profil Literasi | Ringkasan kekuatan siswa per langkah siklus, dengan saran latihan berikutnya | — | P1 |
| F26 | Proyek Mini "Pola di Sekitarku" | Siswa menemukan dan menuliskan pola dari lingkungannya | GL04 | P2 |

## 5. Kebutuhan Non-Fungsional

| Aspek | Target |
|---|---|
| Platform | Browser modern (Chrome/Edge/Firefox/Safari). Dipasang sebagai PWA di Android, iPhone, dan laptop **tanpa Play Store/App Store**. APK opsional lewat PWABuilder |
| Performa | Muat awal < 3 detik di 4G; tanpa framework, JS ±100 KB |
| Ukuran unduhan | Aplikasi inti < 1 MB; tiap video < 5 MB (720p) |
| Offline | Seluruh materi inti bisa dipakai tanpa internet |
| Aksesibilitas | Kontras WCAG AA, target sentuh ≥ 44 px, font minimal 16 px, video bersubtitle |
| Bahasa | Bahasa Indonesia baku yang sederhana |
| Privasi | Tanpa login dan tanpa data pribadi di MVP; data hanya di perangkat |
| Kurikulum | Selaras dengan Capaian Pembelajaran Fase D, elemen Aljabar (pola bilangan) |

## 6. Indikator Keberhasilan

| Indikator | Target | Cara mengukur |
|---|---|---|
| Kelayakan produk (validasi ahli materi & media) | Kategori "layak/sangat layak" (≥ 3,4 dari 4 atau ≥ 81%) | Angket validasi |
| Kepraktisan (respons siswa) | ≥ 80% respon positif | Angket respons siswa / SUS ≥ 68 |
| Beban kognitif | Skor usaha mental (Paas) menurun dari latihan awal ke akhir | Skala Paas 1–9 di aplikasi |
| Hasil belajar | Peningkatan pretest→posttest, N-gain ≥ 0,3 (sedang) | Tes awal & tes akhir |
| Penggunaan petunjuk | Siswa memakai petunjuk alih-alih meninggalkan soal | Log lokal (jumlah soal terlewat vs. hint dipakai) |
| Literasi matematika | Peningkatan skor tes literasi pretest→posttest, N-gain ≥ 0,3; peningkatan pada indikator menafsirkan (LM4–LM5) | Tes literasi berbasis stimulus + rubrik (dokumen 08) |

> Pilih indikator yang sesuai metode penelitianmu (mis. R&D model ADDIE/4D). Lihat `08-rencana-pengujian.md`.

## 7. Asumsi dan Risiko

| Risiko | Dampak | Mitigasi |
|---|---|---|
| Responden studi pendahuluan baru 1 orang | Kebutuhan kurang representatif | Tambah wawancara 3–5 siswa + 1 guru |
| Pembuatan video memakan waktu | Jadwal molor | Mulai dari animasi sederhana/rekaman layar; batasi 1–3 menit |
| HP siswa spesifikasi rendah | Aplikasi lambat | Bundle kecil, video dikompres, tanpa animasi berat |
| Pemeriksaan rumus aljabar sulit (variasi penulisan) | Jawaban benar dinilai salah | Evaluasi rumus secara numerik untuk beberapa nilai n |
| Kuota internet terbatas | Siswa tidak bisa mengakses | PWA offline; pasang sekali, pakai tanpa kuota |
| Soal kontekstual menambah beban membaca | Siswa kewalahan dan menyerah | Konteks ditaruh setelah konsep, batas panjang teks, bantuan membaca, fading siklus |
