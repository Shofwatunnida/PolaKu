# 13 — Kunci Jawaban dan Rubrik per Modul

> Dibuat otomatis oleh `python tools/buat_kunci_rubrik.py` dari file konten. **Jangan diedit manual**:
> ubah kontennya (atau `RUBRIK` di skrip), lalu jalankan ulang skrip.

Semua soal latihan, literasi, dan kuis dinilai otomatis oleh aplikasi dengan kunci di bawah ini.
Kebenaran setiap kunci diuji otomatis (`tests/test_js_logic.py`). Refleksi berupa jawaban bebas,
jadi dinilai peneliti/guru dengan rubrik 0–3.

## M0 · Pengingat Prasyarat

### Latihan

| Id | Tingkat | Soal | Kunci |
|---|---|---|---|
| m0-l1 | 1 | Pada barisan 12, 15, 18, 21, 24, berapakah suku ke-4? | 21 |
| m0-l2 | 1 | Berapa selisih suku-suku pada barisan 25, 32, 39, 46, …? | 7 |
| m0-l3 | 2 | Barisan berikut selisihnya selalu 6. Lengkapi suku yang kosong. | 16, 28 |
| m0-l4 | 2 | Barisan manakah yang selisihnya tetap 3? | (a) 2, 5, 8, 11, … |

### Literasi: Nomor Rumah di Jalan Melati (tahap A, konteks personal)

| Id | Level | Proses | Soal | Kunci | Pembahasan |
|---|---|---|---|---|---|
| melati-1 | L1 | LM3 | Berapa nomor rumah Nadia? | 13 | — |
| melati-2 | L2 | LM2 | Barisan manakah yang menggambarkan nomor rumah di sisi kiri Jalan Melati? | (a) 3, 5, 7, 9, 11, … | — |
| melati-3 | L3 | LM6 | Raka berpendapat tentang nomor rumah di sisi kiri Jalan Melati. | Tidak setuju; alasan: Semua nomor di sisi kiri adalah bilangan ganjil (3, 5, 7, …), sedangkan 20 bilangan genap. | Nomor rumah di sisi kiri adalah 3, 5, 7, 9, … Semuanya ganjil karena dimulai dari bilangan ganjil dan selalu ditambah 2. Jadi nomor 20 tidak akan pernah ada di sisi kiri. |

### Kuis

| Id | Soal | Kunci | Pembahasan |
|---|---|---|---|
| m0-k1 | Pada barisan 6, 13, 20, 27, 34, berapakah suku ke-2? | 13 | Suku ke-1 adalah 6, jadi suku ke-2 adalah 13. |
| m0-k2 | Berapa selisih suku-suku pada barisan 40, 49, 58, 67, …? | 9 | 49 − 40 = 9, 58 − 49 = 9, dan 67 − 58 = 9. |
| m0-k3 | Perhatikan barisan 100, 90, 80, 70, … Tentukan Benar atau Salah. | B, B, S, B | — |

### Rubrik Refleksi

Pertanyaan: *Apa bedanya urutan suku dengan nilai suku? Berikan satu contoh.*

Contoh jawaban lengkap: Urutan suku menunjukkan posisi, misalnya suku ke-3. Nilai suku adalah bilangannya. Pada barisan 10, 20, 30, nilai suku ke-3 adalah 30.

| Skor | Kriteria |
|---|---|
| 0 | Tidak menjawab atau tidak berkaitan |
| 1 | Menyebut salah satu (urutan ATAU nilai) tanpa membedakan |
| 2 | Membedakan urutan dan nilai, tetapi tanpa contoh yang benar |
| 3 | Membedakan urutan (posisi) dan nilai (bilangan) dengan contoh yang benar |

## M1 · Mengenal Pola

### Latihan

| Id | Tingkat | Soal | Kunci |
|---|---|---|---|
| m1-l1 | 1 | Bentuk apakah yang berikutnya? | (b) Segitiga |
| m1-l2 | 1 | Ada berapa bentuk dalam satu satuan pola ini? | 4 |
| m1-l3 | 2 | Pola lingkaran, persegi, persegi, … terus berulang. Bentuk apakah yang ke-30? | (b) Persegi |
| m1-l4 | 2 | Pola lingkaran, segitiga, persegi, … terus berulang. Ada berapa segitiga di antara 20 bentuk pertama? | 7 |
| m1-l5 | 3 | Rumah dari batang korek api disusun berjajar. Gambar 1 memakai 5 batang, gambar 2 memakai 9 batang, dan gambar 3 memakai 13 batang. Lengkapi tabelnya. | 17, 21 |

### Literasi: Selendang Tenun Rini (tahap A, konteks sosial-budaya)

| Id | Level | Proses | Soal | Kunci | Pembahasan |
|---|---|---|---|---|---|
| tenun-1 | L1 | LM1, LM3 | Warna apakah garis ke-9? | (a) Merah | — |
| tenun-2 | L2 | LM2, LM3 | Ada berapa garis hijau pada selendang 30 garis itu? | 7 garis | — |
| tenun-3 | L3 | LM6 | Bayu menghitung warna garis pada selendang 30 garis itu. | Tidak setuju; alasan: Ada 16 garis merah dan 7 garis kuning, karena 2 garis sisa berwarna merah. 16 bukan dua kali 7. | Dalam 7 satuan penuh ada 14 merah dan 7 kuning. Dua garis sisa (ke-29 dan ke-30) berwarna merah, jadi garis merah ada 16. Dua kali 7 adalah 14, bukan 16. Aturan "2 merah untuk 1 kuning" hanya tepat jika semua satuan lengkap. |

### Kuis

| Id | Soal | Kunci | Pembahasan |
|---|---|---|---|
| m1-k1 | Pola segitiga, segitiga, lingkaran, … terus berulang. Bentuk apakah yang ke-15? | (b) Lingkaran | 15 : 3 = 5 sisa 0. Sisa 0 berarti bentuk terakhir dalam satuan, yaitu lingkaran. |
| m1-k2 | Pola lingkaran, persegi, bintang, … terus berulang. Ada berapa bintang di antara 25 bentuk pertama? | 8 | 25 = 8 × 3 + 1. Delapan satuan penuh berisi 8 bintang. Bentuk ke-25 adalah lingkaran, jadi tetap 8 bintang. |
| m1-k3 | Gambar 1 berisi 6 noktah, gambar 2 berisi 10 noktah, dan gambar 3 berisi 14 noktah. Berapa noktah pada gambar 6? | 26 | Setiap gambar bertambah 4: 6, 10, 14, 18, 22, 26. |
| m1-k4 | Pola persegi, lingkaran, lingkaran, … terus berulang. Tentukan Benar atau Salah. | B, S, B, B | — |

### Rubrik Refleksi

Pertanyaan: *Bagaimana caramu menentukan bentuk ke-100 pada pola yang berulang?*

Contoh jawaban lengkap: Pertama, aku mencari satuan pola dan menghitung banyak bentuknya. Lalu aku membagi 100 dengan banyak bentuk itu. Sisanya menunjukkan bentuk ke berapa dalam satuan. Jika sisanya 0, bentuknya adalah bentuk terakhir dalam satuan.

| Skor | Kriteria |
|---|---|
| 0 | Tidak menjawab atau tidak berkaitan |
| 1 | Menyebut "cari polanya" tanpa langkah |
| 2 | Menyebut satuan pola dan pembagian, tetapi salah menafsirkan sisa |
| 3 | Langkah lengkap: satuan pola → bagi 100 dengan banyak bentuk → sisa menunjukkan posisi; sisa 0 = bentuk terakhir |

## M2 · Pola dengan Selisih Tetap

### Latihan

| Id | Tingkat | Soal | Kunci |
|---|---|---|---|
| m2-l1 | 1 | Tentukan suku berikutnya dari pola 5, 8, 11, 14, … | 17 |
| m2-l2 | 2 | Tentukan suku ke-8 dari pola 2, 6, 10, 14, … | 30 |
| m2-l3 | 2 | Lengkapi suku yang hilang pada pola 7, …, 17, 22, … | 12, 27 |
| m2-l4 | 2 | Rumus suku ke-n dari pola 4, 7, 10, 13, … adalah … | (a) Uₙ = 3n + 1 |
| m2-l5 | 3 | Tentukan rumus suku ke-n dari pola 1, 4, 7, 10, 13, … | 3n-2 |

### Literasi: Kursi Lomba 17 Agustus (tahap A, konteks sosial-budaya)

| Id | Level | Proses | Soal | Kunci | Pembahasan |
|---|---|---|---|---|---|
| kursi-1 | L1 | LM3 | Berapa kursi pada baris ke-4? | 21 kursi | — |
| kursi-2 | L2 | LM2, LM3 | Rumus banyak kursi pada baris ke-n adalah … | (b) 3n + 9 | — |
| kursi-3 | L3 | LM6 | Andi menghitung banyak kursi di baris ke-10. | Tidak setuju; alasan: Baris ke-1 belum bertambah, jadi 12 + 9 × 3 = 39 kursi. | Baris ke-10 berisi 3(10) + 9 = 39 kursi. Andi keliru karena menghitung 10 lompatan, padahal dari baris ke-1 ke baris ke-10 hanya ada 9 lompatan. |
| kursi-4 | L3 | LM3, LM4, LM5 | Paling banyak berapa baris kursi yang bisa disusun panitia? | 10 baris | — |

### Kuis

| Id | Soal | Kunci | Pembahasan |
|---|---|---|---|
| m2-k1 | Tentukan suku berikutnya dari pola 9, 15, 21, 27, … | 33 | Selisihnya +6, jadi 27 + 6 = 33. |
| m2-k2 | Tentukan suku ke-15 dari pola 3, 7, 11, 15, … | 59 | Selisih +4, rumus Uₙ = 4n − 1. U₁₅ = 4(15) − 1 = 59. |
| m2-k3 | Tentukan rumus suku ke-n dari pola 8, 13, 18, 23, … | 5n+3 | Selisih +5, jadi 5n. Untuk n = 1, 5n = 5, padahal suku ke-1 adalah 8. Jadi Uₙ = 5n + 3. |
| m2-k4 | Perhatikan pola 5, 9, 13, 17, … Tentukan Benar atau Salah. | B, B, S, B | — |

### Rubrik Refleksi

Pertanyaan: *Bagaimana caramu menemukan rumus suku ke-n dari pola yang selisihnya tetap?*

Contoh jawaban lengkap: Aku mencari selisih antarsuku. Kalau selisihnya tetap, misalnya 3, rumusnya diawali 3n. Lalu aku bandingkan 3n dengan suku ke-1, kemudian menambah atau mengurangi supaya cocok. Terakhir, aku cek rumusnya ke suku ke-2 dan ke-3.

| Skor | Kriteria |
|---|---|
| 0 | Tidak menjawab atau tidak berkaitan |
| 1 | Menyebut selisih saja |
| 2 | Menyebut selisih → koefisien n dan penyesuaian dengan suku pertama |
| 3 | Langkah lengkap: selisih → kn → sesuaikan dengan U₁ → cek ke suku lain |

## M3 · Pola Bilangan Ganjil dan Genap

### Latihan

| Id | Tingkat | Soal | Kunci |
|---|---|---|---|
| m3-l1 | 1 | Perhatikan pola noktah ganjil. Berapa noktah pada gambar ke-5? | 9 |
| m3-l2 | 2 | Tentukan bilangan genap ke-25. | 50 |
| m3-l3 | 2 | Tentukan bilangan ganjil ke-50. | 99 |
| m3-l4 | 3 | Barisan 3, 5, 7, 9, … adalah bilangan ganjil yang dimulai dari 3. Tentukan rumus suku ke-n. | 2n+1 |
| m3-l5 | 2 | Tentukan Benar atau Salah untuk setiap pernyataan. | B, B, S, B |

### Literasi: Meja Rapat OSIS (tahap A, konteks sosial-budaya)

| Id | Level | Proses | Soal | Kunci | Pembahasan |
|---|---|---|---|---|---|
| osis-1 | L1 | LM3 | Berapa siswa yang bisa duduk di 9 meja? | 18 siswa | — |
| osis-2 | L2 | LM2 | Tulis rumus banyak siswa yang bisa duduk di n meja. | 2n | — |
| osis-3 | L3 | LM3, LM4, LM5 | Ada 23 siswa yang datang. Paling sedikit berapa meja yang harus disiapkan agar semua siswa mendapat tempat duduk? | 12 meja | — |
| osis-4 | L3 | LM6 | Dewi berpendapat tentang banyak siswa dan meja. | Setuju; alasan: Setuju, karena bilangan genap selalu bisa dibagi menjadi pasangan, jadi tidak ada tempat duduk yang kosong. | Bilangan genap = 2 × suatu bilangan, jadi siswa selalu bisa dipasangkan tanpa sisa. Contoh: 20 siswa = 10 pasang = 10 meja penuh. Pilihan "banyak meja selalu genap" salah, karena 6 siswa membutuhkan 3 meja. |

### Kuis

| Id | Soal | Kunci | Pembahasan |
|---|---|---|---|
| m3-k1 | Tentukan bilangan genap ke-40. | 80 | Uₙ = 2n, jadi U₄₀ = 2 × 40 = 80. |
| m3-k2 | Tentukan bilangan ganjil ke-16. | 31 | Uₙ = 2n − 1, jadi U₁₆ = 32 − 1 = 31. |
| m3-k3 | Bilangan 47 adalah bilangan ganjil ke berapa? | (b) Ke-24 | 2n − 1 = 47, jadi 2n = 48 dan n = 24. Cek: 2 × 24 − 1 = 47 ✓. |
| m3-k4 | Barisan 6, 8, 10, 12, … adalah bilangan genap yang dimulai dari 6. Tentukan rumus suku ke-n. | 2n+4 | Selisih +2, jadi diawali 2n. Untuk n = 1, 2n = 2, padahal suku ke-1 adalah 6. Jadi Uₙ = 2n + 4. |

### Rubrik Refleksi

Pertanyaan: *Bagaimana caramu mengingat rumus bilangan genap dan bilangan ganjil?*

Contoh jawaban lengkap: Bilangan genap ke-n adalah 2n karena noktahnya tersusun dalam 2 baris. Bilangan ganjil ke-n adalah 2n − 1, yaitu 1 kurang dari bilangan genap pasangannya.

| Skor | Kriteria |
|---|---|
| 0 | Tidak menjawab atau tidak berkaitan |
| 1 | Menulis salah satu rumus (2n atau 2n − 1) tanpa alasan |
| 2 | Menulis kedua rumus dengan benar tanpa alasan |
| 3 | Menulis kedua rumus dan alasannya (dua baris noktah / ganjil = genap − 1) |

## M4 · Pola Persegi dan Persegi Panjang

### Latihan

| Id | Tingkat | Soal | Kunci |
|---|---|---|---|
| m4-l1 | 1 | Perhatikan pola persegi berikut. Berapa noktah pada gambar ke-6? | 36 |
| m4-l2 | 2 | Pola persegi 1, 4, 9, 16, … Tentukan suku ke-15. | 225 |
| m4-l3 | 2 | Pola persegi panjang 2, 6, 12, 20, … Tentukan suku ke-7. | 56 |
| m4-l4 | 3 | Tentukan rumus suku ke-n dari pola 2, 6, 12, 20, 30, … | n(n+1) |
| m4-l5 | 2 | Jodohkan setiap pola dengan rumusnya. | 1, 4, 9, 16, … → Uₙ = n²; 2, 6, 12, 20, … → Uₙ = n(n + 1); 3, 6, 9, 12, … → Uₙ = 3n |

### Literasi: Motif Batik Kawung (tahap B, konteks sosial-budaya)

| Id | Level | Proses | Soal | Kunci | Pembahasan |
|---|---|---|---|---|---|
| kawung-1 | L1 | LM3 | Berapa bulatan pada motif ke-5? | 25 bulatan | — |
| kawung-2 | L2 | LM2, LM3 | Rani ingin membuat motif ke-8. Berapa bulatan yang dibutuhkan? | 64 bulatan | — |
| kawung-3 | L3 | LM3, LM4, LM5 | Dengan 100 bulatan, motif ke berapa yang paling besar yang bisa dibuat Rani (hanya satu motif)? | 10 | — |
| kawung-4 | L3 | LM6 | Sinta membandingkan motif ke-3 dan motif ke-6. | Tidak setuju; alasan: Motif ke-6 butuh 36 bulatan, motif ke-3 butuh 9. Jadi 4 kali lipat, bukan 2 kali. | Motif ke-6 butuh 6 × 6 = 36 bulatan, motif ke-3 butuh 9. 36 = 4 × 9, jadi 4 kali lipat. Pada pola persegi, jika urutannya dikali 2, banyak bulatannya dikali 4. |

### Kuis

| Id | Soal | Kunci | Pembahasan |
|---|---|---|---|
| m4-k1 | Pola persegi 1, 4, 9, 16, … Tentukan suku ke-20. | 400 | U₂₀ = 20² = 400. |
| m4-k2 | Pola persegi panjang 2, 6, 12, 20, … Tentukan suku ke-10. | 110 | U₁₀ = 10 × 11 = 110. |
| m4-k3 | Barisan manakah yang merupakan pola persegi? | (b) 1, 4, 9, 16, … | 1, 4, 9, 16 adalah 1², 2², 3², 4². |
| m4-k4 | Perhatikan pola 1, 4, 9, 16, 25, … Tentukan Benar atau Salah. | S, B, B, S | — |

### Rubrik Refleksi

Pertanyaan: *Bagaimana caramu membedakan pola persegi dan pola persegi panjang?*

Contoh jawaban lengkap: Pola persegi tersusun n baris dan n kolom, jadi rumusnya n². Pola persegi panjang tersusun n baris dan n + 1 kolom, jadi rumusnya n(n + 1). Selisih keduanya tidak tetap, tetapi selisih tingkat duanya selalu 2.

| Skor | Kriteria |
|---|---|
| 0 | Tidak menjawab atau tidak berkaitan |
| 1 | Menyebut salah satu pola |
| 2 | Membedakan n × n dan n × (n + 1) |
| 3 | Membedakan susunan baris-kolom kedua pola dan menyinggung selisih tingkat dua |

## M5 · Pola Segitiga

### Latihan

| Id | Tingkat | Soal | Kunci |
|---|---|---|---|
| m5-l1 | 1 | Pola segitiga 1, 3, 6, 10, 15, … Tentukan suku berikutnya. | 21 |
| m5-l2 | 2 | Perhatikan pola segitiga berikut. Berapa noktah pada gambar ke-9? | 45 |
| m5-l3 | 2 | Lengkapi banyak noktah pada pola segitiga. | 10, 21 |
| m5-l4 | 3 | Tentukan rumus banyak noktah pada gambar ke-n dari pola 1, 3, 6, 10, … | n(n+1)/2 |
| m5-l5 | 2 | Manakah yang merupakan bilangan segitiga? | (b) 28 |

### Literasi: Tumpukan Kaleng di Warung (tahap B, konteks sosial-budaya)

| Id | Level | Proses | Soal | Kunci | Pembahasan |
|---|---|---|---|---|---|
| kaleng-1 | L1 | LM3 | Jika tumpukan dibuat 5 baris, berapa kaleng yang dipakai? | 15 kaleng | — |
| kaleng-2 | L2 | LM2, LM3 | Berapa kaleng yang dibutuhkan untuk tumpukan 8 baris? | 36 kaleng | — |
| kaleng-3 | L3 | LM3, LM4, LM5 | Dengan 50 kaleng, paling banyak berapa baris lengkap yang bisa dibuat Bu Sari? | 9 baris | — |
| kaleng-4 | L3 | LM6 | Tono membandingkan tumpukan 5 baris dan 10 baris. | Tidak setuju; alasan: Tumpukan 10 baris memakai 55 kaleng, sedangkan 5 baris memakai 15 kaleng. 55 lebih dari dua kali 15. | 5 baris = 15 kaleng dan 10 baris = 55 kaleng. Dua kali 15 adalah 30, bukan 55. Pada pola segitiga, banyak kaleng bertambah lebih cepat daripada banyak baris. |

### Kuis

| Id | Soal | Kunci | Pembahasan |
|---|---|---|---|
| m5-k1 | Tentukan suku ke-11 pola segitiga 1, 3, 6, 10, … | 66 | U₁₁ = 11 × 12 : 2 = 132 : 2 = 66. |
| m5-k2 | Berapa hasil 1 + 2 + 3 + … + 30? | 465 | Ini bilangan segitiga ke-30: 30 × 31 : 2 = 930 : 2 = 465. |
| m5-k3 | Barisan manakah yang merupakan pola segitiga? | (a) 1, 3, 6, 10, 15, … | Selisih 1, 3, 6, 10, 15 adalah +2, +3, +4, +5 (bertambah 1). Itu pola segitiga. |
| m5-k4 | Perhatikan pola 1, 3, 6, 10, 15, … Tentukan Benar atau Salah. | S, B, B, S | — |

### Rubrik Refleksi

Pertanyaan: *Mengapa rumus pola segitiga dibagi 2?*

Contoh jawaban lengkap: Dua segitiga yang sama bisa disusun menjadi persegi panjang n × (n + 1). Satu segitiga adalah setengah dari persegi panjang itu, jadi banyak noktahnya n(n + 1) dibagi 2.

| Skor | Kriteria |
|---|---|
| 0 | Tidak menjawab atau tidak berkaitan |
| 1 | Menyebut "karena setengah" tanpa penjelasan |
| 2 | Menjelaskan bahwa dua segitiga membentuk persegi panjang |
| 3 | Menjelaskan dua segitiga sama besar membentuk persegi panjang n × (n + 1), jadi satu segitiga = n(n + 1)/2 |

## M6 · Pola Fibonacci

### Latihan

| Id | Tingkat | Soal | Kunci |
|---|---|---|---|
| m6-l1 | 1 | Tentukan suku berikutnya dari barisan 2, 2, 4, 6, 10, … | 16 |
| m6-l2 | 2 | Barisan berikut mengikuti aturan Fibonacci. Lengkapi suku yang kosong. | 7, 18 |
| m6-l3 | 2 | Barisan manakah yang mengikuti aturan Fibonacci (jumlah dua suku sebelumnya)? | (a) 2, 3, 5, 8, 13, … |
| m6-l4 | 3 | Pada barisan Fibonacci 3, …, 11, … berapakah suku ke-2? | 8 |
| m6-l5 | 2 | Perhatikan barisan 1, 1, 2, 3, 5, 8, 13, 21, … Tentukan Benar atau Salah. | B, S, B, S |

### Literasi: Tangga Rumah Panggung (tahap B, konteks personal)

| Id | Level | Proses | Soal | Kunci | Pembahasan |
|---|---|---|---|---|---|
| tangga-1 | L1 | LM1 | Untuk 2 anak tangga ada 2 cara. Manakah kedua cara itu? | (a) 1 + 1 dan 2 | — |
| tangga-2 | L2 | LM2, LM3 | Untuk 4 anak tangga, ada berapa cara? | 5 cara | — |
| tangga-3 | L3 | LM3, LM4 | Ada berapa cara Adi menaiki seluruh 6 anak tangga? | 13 cara | — |
| tangga-4 | L3 | LM6 | Sinta membandingkan banyak cara untuk 3 dan 6 anak tangga. | Tidak setuju; alasan: Untuk 6 anak tangga ada 13 cara, sedangkan dua kali banyak cara untuk 3 anak tangga hanya 6. | Untuk 3 anak tangga ada 3 cara, jadi dua kalinya 6. Untuk 6 anak tangga ada 13 cara. Pada pola Fibonacci, banyak cara bertambah jauh lebih cepat, jadi tidak bisa dihitung dengan mengalikan dua. |

### Kuis

| Id | Soal | Kunci | Pembahasan |
|---|---|---|---|
| m6-k1 | Tentukan suku berikutnya dari barisan 5, 5, 10, 15, 25, … | 40 | 15 + 25 = 40. |
| m6-k2 | Barisan Fibonacci 2, 7, 9, 16, … Tentukan suku ke-6. | 41 | U₅ = 9 + 16 = 25, lalu U₆ = 16 + 25 = 41. |
| m6-k3 | Pada barisan Fibonacci 6, …, 20, … berapakah suku ke-2? | (a) 14 | U₃ = U₁ + U₂, jadi 20 = 6 + U₂ dan U₂ = 14. |
| m6-k4 | Perhatikan barisan 1, 4, 5, 9, 14, … Tentukan Benar atau Salah. | B, S, S, B | — |

### Rubrik Refleksi

Pertanyaan: *Apa bedanya pola Fibonacci dengan pola selisih tetap (M2)?*

Contoh jawaban lengkap: Pada pola selisih tetap, setiap suku didapat dengan menambah bilangan yang sama. Pada pola Fibonacci, setiap suku didapat dengan menjumlahkan dua suku sebelumnya, sehingga selisihnya berubah-ubah.

| Skor | Kriteria |
|---|---|
| 0 | Tidak menjawab atau tidak berkaitan |
| 1 | Menjelaskan salah satu pola saja |
| 2 | Menjelaskan aturan kedua pola (tambah bilangan tetap vs jumlah dua suku sebelumnya) |
| 3 | Menjelaskan aturan kedua pola dan akibatnya: selisih pola Fibonacci berubah-ubah |

