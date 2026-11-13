# Audit Konten Modul M0–M8 (Tahap 1)

| | |
|---|---|
| Tanggal | 13 November 2026 |
| Tujuan | Memetakan apa yang dibutuhkan agar M0, M1, M3, M5, M6, M7, dan M8 bisa dibuka dengan konten yang layak |
| Perubahan kode | Tidak ada. Laporan ini hanya hasil pemeriksaan |
| Bukti | Kode di `frontend/`, validator `tools/validasi_konten.py`, konten `frontend/konten/`, dan dokumen `docs/02`, `03`, `04`, `05`, `11` |

## 1. Cara Kerja Sistem Modul Saat Ini

| Bagian | Cara kerja | Bukti |
|---|---|---|
| Daftar modul & status terkunci | `konten/modul.json`, kolom `"tersedia"`. Saat ini hanya M2 dan M4 yang `true` | `modul.json` |
| Peta Materi | Modul `tersedia: false` dirender sebagai kartu tanpa tautan ("🔒 Segera hadir") | `js/pages/modul.js` `halamanPeta` |
| Pemuatan konten | Membuka `#/modul/mX` memuat `konten/mX.json`. **Tidak perlu mengubah kode untuk menambah modul**, cukup file JSON + `tersedia: true` | `modul.js` `halamanModul`, `halamanTahap` |
| 7 tahap belajar | Konsep → Contoh Lengkap → Setengah Jadi → Latihan → Literasi → Refleksi → Kuis (sama untuk semua modul) | `js/konten.js` `TAHAP` |
| Progres & posisi | Disimpan per id modul (`progres[mX]`, `posisi["mX/tahap"]`). Otomatis berlaku untuk modul baru | `js/storage.js` |
| Offline | Semua file `.json` di `frontend/` masuk cache melalui `tools/build_aset.py` | `sw.js` |
| Pengaman kualitas | Validator menolak konten yang melanggar aturan (≤ 3 kalimat/segmen, 3 petunjuk, kunci rumus cocok dengan pola, literasi 3–4 soal L1→L3, label LM1–LM7, minimal satu LM6, panjang stimulus ≤ 60/120 kata). Pengujian `test_kunci_konten_dinilai_benar` otomatis memeriksa setiap kunci jawaban di **setiap modul yang tersedia** | `tools/validasi_konten.py`, `tests/test_js_logic.py` |

**Kesimpulan:** modul baru cukup ditambahkan sebagai file JSON. Pengamannya sudah ada. Ada 3 kebutuhan kode kecil (bagian 6).

## 2. Struktur Konten Contoh (M2 & M4)

| Bagian | M2 | M4 | Format |
|---|---|---|---|
| Tujuan | 4 | 3 | teks dengan kode TP |
| Segmen konsep | 5 | 5 | ≤ 3 kalimat, visual opsional, video (kosong) |
| Contoh lengkap | 2 × 5 langkah | 2 × 5 langkah | label 5 langkah strategi |
| Contoh setengah jadi | 2 (1 dan 2 langkah kosong) | 2 (1 dan 2) | langkah kosong hanya isian angka/rumus |
| Latihan | 5 soal | 5 soal | 3 petunjuk + umpan balik miskonsepsi |
| Literasi | 1 stimulus, 4 soal, tahap A | 1 stimulus, 4 soal, tahap B | L1→L3, LM1–LM7, cek cerita |
| Refleksi | 1 | 1 | pertanyaan + contoh penjelasan |
| Kuis | 4 soal | 4 soal | tanpa petunjuk, dengan pembahasan |

Per modul ±20 soal/butir beserta petunjuk dan umpan balik. Tujuh modul baru berarti **±140 butir baru**.

## 3. Sumber Perencanaan yang Tersedia

| Sumber | Isi yang bisa dipakai | Yang tidak ada |
|---|---|---|
| `docs/04` §1 | TP1–TP9 | Indikator per modul yang lebih rinci |
| `docs/04` §2 | Subtopik, TP, dan visual per modul | Urutan konsep dalam modul, alokasi waktu |
| `docs/04` §4 | Draf soal: M3–M5 (1 soal masing-masing), M6 (2), M7 (2), M8 (5) | Sebagian besar soal M0, M1, M3, M5–M8 |
| `docs/03` | Strategi 5 langkah, desain petunjuk & umpan balik, alur | — |
| `docs/11` | Indikator LM1–LM7, level L1–L3, siklus, tahap A/B/C, ide konteks | Stimulus lengkap selain "Kursi 17 Agustus" |
| `docs/05` US-18 | Tahap bantuan: M1–M3 = A, M4–M7 = B, M8 = C | — |
| `docs/08` | Rubrik uraian 0–3 per proses literasi | Rubrik per modul |

Tidak ada referensi ilmiah baru yang dibutuhkan untuk konten soal. Konten akan disusun dari TP dan indikator di atas, tanpa mengutip sumber yang tidak ada di proyek.

## 4. Kebutuhan Konten per Modul

Konvensi umum: 4–5 segmen konsep, 2 contoh lengkap, 2 contoh setengah jadi (1 → 2 langkah kosong), 5 latihan (tingkat 1–3), 1 stimulus literasi (3–4 soal L1→L3, minimal satu LM6), refleksi, dan 4 kuis.

| Modul | TP | Isi konsep yang dibutuhkan | Visual (tersedia di aplikasi?) | Usulan konteks literasi | Tahap siklus |
|---|---|---|---|---|---|
| **M0 Pengingat Prasyarat** | prasyarat | Barisan, suku & urutan (suku ke-n), selisih dua bilangan, operasi hitung sederhana | barisan ✅, tabel ✅ | Nomor rumah di satu sisi jalan (personal) | A |
| **M1 Mengenal Pola** | TP1 | Pola berulang (motif ABAB), pola bertambah pada gambar/benda, menebak suku berikutnya | **Deret bentuk/gambar berulang ❌ belum ada** (lihat 6.1); noktah ✅ | Motif anyaman/kain berulang atau susunan ubin lantai (sosial-budaya) | A |
| **M3 Ganjil & Genap** | TP2, TP3 | Bilangan genap 2n (noktah berpasangan), ganjil 2n − 1 (bentuk L), menentukan suku ke-n, membedakan keduanya | noktah ganjil/genap ✅ | Kursi berpasangan / nomor bangku (sosial-budaya) | A |
| **M5 Segitiga** | TP2, TP3 | Bilangan segitiga 1, 3, 6, 10; selisih bertambah 1; rumus n(n + 1)/2 lewat "dua segitiga = persegi panjang" | noktah segitiga ✅ | Tumpukan kaleng di warung (sudah direncanakan di `docs/04`) | B |
| **M6 Fibonacci** | TP2 | Aturan "jumlah dua suku sebelumnya", melanjutkan barisan, barisan Fibonacci dengan suku awal lain, mencari suku yang hilang | tabel ✅, ikon persegi Fibonacci ✅ | Banyak cara menaiki tangga 1 atau 2 anak tangga (hasilnya benar-benar Fibonacci dan bisa dibuktikan) | B |
| **M7 Menentukan Suku ke-n** | TP3–TP5 | **Perlu keputusan, lihat 5.2** | tabel n vs Uₙ ✅ | Tergantung cakupan | B |
| **M8 Literasi** | TP6–TP9 | Siklus BACA–UBAH–HITUNG–CEK CERITA secara mandiri, memilih jenis pola sendiri, keputusan & argumen | kursi ✅, tabel ✅ | Konteks campuran: personal, sosial-budaya, saintifik (mis. tinggi tanaman kacang hijau) | C |

## 5. Hal yang Belum Jelas dan Butuh Keputusan

### 5.1 Jenjang kelas
Permintaan menyebut **kelas VII**, sedangkan dokumen proyek dan responden wawancara menyebut **kelas VIII** (Fase D). Materi pola bilangan berada di Fase D (kelas VII–IX). Usulan: konten mengikuti Fase D, dengan bahasa dan angka yang mudah untuk kelas VII sehingga tetap cocok untuk kelas VIII.

### 5.2 Cakupan M7 tumpang tindih dengan M2
`docs/04` menulis M7 = "dari aturan ke rumus (an + b)". Rumus an + b untuk pola selisih tetap **sudah diajarkan lengkap di M2** (segmen 4–5, contoh, latihan, kuis). Kalau M7 mengikuti dokumen apa adanya, isinya mengulang M2. Usulan cakupan M7 yang tidak tumpang tindih:
- Menentukan **suku ke berapa** dari nilai suku (kebalikan: Uₙ = 50, n = ?).
- **Memilih rumus** yang tepat untuk berbagai jenis pola (selisih tetap, persegi, persegi panjang, segitiga), yaitu ringkasan TP2–TP5.
- Selisih tingkat dua sebagai **penanda jenis pola** (pengayaan ringan, tanpa menurunkan rumus kuadrat umum).

### 5.3 Rekomendasi Tes Awal
Saat ini skor 0–4 → M2 dan skor 5–6 → M4. `docs/04` merencanakan skor rendah → M0. Setelah M0 dan M1 ada, apakah rekomendasinya diubah? Ini mengubah perilaku tes, jadi perlu persetujuan.

### 5.4 Konflik dengan instrumen tes (penting untuk penelitian)
Konten modul **tidak boleh memakai butir atau konteks yang sama dengan Tes Awal/Tes Akhir**. Kalau sama, siswa berlatih soal posttest dan data N-gain menjadi tidak sah. Yang harus dihindari:

| Tes | Butir/konteks yang tidak boleh diulang di modul |
|---|---|
| Tes Awal | 2, 4, 6, 8; selisih 7 dan 12; 1, 4, 9, 16 (suku ke-5); segitiga 1, 3, 6 (gambar ke-4); 1, 1, 2, 3, 5; aturan "×4" |
| Tes Akhir | 3, 6, 9, 12; 5, 8, 11, 14 (suku ke-10); 2, 7, 12, 17; persegi suku ke-11; persegi panjang suku ke-6; **tabungan Dina Rp5.000 + Rp2.000**; **meja hajatan 4, 6, 8 (klaim Bima)**; **aula 10 kursi + 2, maks. 35** |

**Draf soal M8 di `docs/04` §4 butir 1, 4, dan 5 memakai konteks yang sudah ada di Tes Akhir.** Draf itu tidak akan dipakai apa adanya.

### 5.5 M0 dalam bentuk 7 tahap
PRD (F02) merencanakan M0 sebagai "kilas balik singkat". Permintaan sekarang mewajibkan 7 tahap. Usulan: M0 tetap 7 tahap tetapi lebih ringan (±3 segmen, 4 latihan, 3 soal literasi, 3 kuis).

### 5.6 Video
Tujuh komponen yang diminta tidak mencakup video. Modul baru akan tetap menampilkan kotak "Video sedang disiapkan", sama seperti M2/M4. Artinya fitur video (PRD F03) masih belum terpenuhi untuk semua modul.

## 6. Kebutuhan Perubahan Kode (kecil, untuk mendukung konten)

| No | Kebutuhan | Alasan | Dampak |
|---|---|---|---|
| 6.1 | Jenis visual baru **"deret bentuk"** (mis. ● ▲ ■ ● ▲ ■ …) | M1 membutuhkan pola berulang non-bilangan; visual yang ada hanya barisan angka, noktah, tabel, dan kursi | Tambahan di `ui.js` `visual()` + validator. Tidak mengubah fitur lain |
| 6.2 | Opsi `"cekAturan": false` per soal | Pada soal Fibonacci tidak ada rumus suku ke-n sederhana. Tombol "Cek Aturanmu" akan membingungkan siswa | Tambahan satu kondisi di `soal.js` |
| 6.3 | Pengujian & validator tambahan | Memastikan 9 modul bisa dibuka, setiap tahap terisi, tidak ada soal duplikat antar-modul, dan tidak ada butir yang sama dengan Tes Awal/Akhir | Tes baru, tanpa mengubah aplikasi |

Konten M2 dan M4 tidak perlu diubah.

## 7. Rubrik dan Kunci Jawaban

- Semua soal latihan/kuis/literasi dinilai otomatis dengan kunci di file JSON. Kunci diuji otomatis oleh `test_kunci_konten_dinilai_benar`.
- Setiap soal kuis dan literasi L3 akan diberi `pembahasan`.
- Untuk refleksi (jawaban bebas, tidak dinilai otomatis), rubrik 0–3 per modul akan dibuat di dokumen terpisah (`docs/13-kunci-dan-rubrik-modul.md`) mengikuti format rubrik di `docs/08`.

## 8. Usulan Rencana Pengerjaan Bertahap

| Gelombang | Modul | Alasan urutan | Kebutuhan kode |
|---|---|---|---|
| 1 | M0, M3, M5 | Visual sudah tersedia; pola sederhana | 6.3 |
| 2 | M1, M6 | Butuh visual deret bentuk (6.1) & opsi cek aturan (6.2) | 6.1, 6.2 |
| 3 | M7, M8 | Bergantung keputusan cakupan M7 (5.2), dan M8 merangkum semua modul | — |

Setiap gelombang diakhiri dengan validasi konten, semua pengujian, dan tangkapan layar. Modul baru diaktifkan (`tersedia: true`) hanya setelah lengkap dan lulus pengujian.

## 9. Keputusan Pemilik Proyek (13 November 2026)

| Pertanyaan | Keputusan | Konsekuensi |
|---|---|---|
| Cakupan M7 | **Fokus selisih tingkat dua** (menurunkan rumus an² + bn + c) | Topik paling sulit. Agar terjangkau kelas VII, M7 dibangun dari M2 dan M4: kenali selisih tingkat dua → a = (selisih tingkat dua) ÷ 2 → kurangi an² dari setiap suku → sisanya pola selisih tetap (cara M2). Tanpa sistem persamaan. Angka dipilih agar hasil bagi selalu bulat |
| Jenjang | **Kelas VII** | Bahasa dan angka untuk kelas VII. Dokumen sasaran pengguna (README, CLAUDE.md, PRD) disesuaikan. Fakta wawancara (responden kelas VIII) tidak diubah |
| Rekomendasi Tes Awal | **Tidak diubah** | M0 dan M1 dibuka manual dari Peta Materi |
| Pengerjaan | **3 gelombang + tinjauan** | Gelombang 1: M0, M3, M5 → tinjauan → Gelombang 2: M1, M6 → tinjauan → Gelombang 3: M7, M8 |

## 10. Status Pengerjaan

| Gelombang | Modul | Status | Catatan |
|---|---|---|---|
| 1 | M0, M3, M5 | ✅ Selesai (13 Nov 2026), disetujui | Gambar "dua segitiga" baru untuk M5 |
| 2 | M1, M6 | ✅ Selesai (13 Nov 2026) | Visual deret bentuk (6.1), opsi `cekAturan: false` (6.2), verifikasi kunci pola berulang otomatis, huruf awal warna pada garis untuk siswa buta warna |
| 3 | M7, M8 | Belum dimulai | M7 fokus selisih tingkat dua (lihat §9) |
