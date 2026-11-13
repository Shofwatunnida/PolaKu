# 05 — User Stories dan Kriteria Penerimaan

Format: *Sebagai [peran], saya ingin [tujuan], agar [manfaat].* ID fitur merujuk ke `02-PRD.md`.

## Epik A — Memulai Belajar

**US-01 (F01) — Tes awal**
Sebagai siswa, saya ingin mengerjakan tes singkat di awal, agar aplikasi tahu dari mana saya sebaiknya mulai.
- [ ] Tes berisi 5–8 soal, tanpa batas waktu
- [ ] Ada tombol "Lewati tes" (langsung mulai dari M0)
- [ ] Setelah selesai, muncul rekomendasi modul awal beserta alasannya
- [ ] Hasil tes disimpan di perangkat dan dipakai sebagai pretest

**US-02 (F02) — Pengingat prasyarat**
Sebagai siswa yang sudah lupa, saya ingin mengulang istilah dasar (suku, selisih), agar saya bisa mengikuti materi utama.
- [ ] Maksimal 4 layar, masing-masing satu istilah
- [ ] Setiap istilah punya contoh visual

## Epik B — Mempelajari Konsep

**US-03 (F03) — Materi bersegmen**
Sebagai siswa, saya ingin materi disajikan sedikit demi sedikit, agar saya tidak kewalahan.
- [ ] Satu konsep per layar, maksimal 3 kalimat
- [ ] Tombol "Lanjut" dan "Kembali" selalu tersedia
- [ ] Indikator posisi (mis. "2 dari 5")

**US-04 (F03) — Video pendek**
Sebagai siswa yang lebih mudah paham dengan video, saya ingin menonton penjelasan singkat, agar konsepnya lebih mudah dimengerti.
- [ ] Durasi video 1–3 menit
- [ ] Tidak diputar otomatis; bisa dijeda, diulang, dipercepat/diperlambat
- [ ] Subtitle bahasa Indonesia
- [ ] Bisa diputar offline

**US-05 (F04) — Visualisasi selisih**
Sebagai siswa, saya ingin melihat lompatan antarsuku, agar saya lebih cepat menemukan polanya.
- [ ] Panah dan label selisih muncul di antara suku-suku
- [ ] Siswa bisa menekan "Tampilkan lompatan" (tidak langsung ditampilkan di soal latihan)
- [ ] Untuk pola tidak tetap, bisa menampilkan selisih tingkat dua

**US-06 (F05) — Representasi ganda**
Sebagai siswa, saya ingin melihat pola dalam bentuk gambar, tabel, dan bilangan, agar saya memahami hubungan antar-bentuk.
- [ ] Tab/geser antar-representasi: Gambar · Tabel · Bilangan · Rumus
- [ ] Representasi saling terhubung (menyorot suku ke-3 di tabel juga menyorot gambar ke-3)

## Epik C — Belajar dari Contoh

**US-07 (F06) — Contoh lengkap**
Sebagai siswa, saya ingin melihat contoh penyelesaian langkah demi langkah, agar saya tahu cara mengerjakannya.
- [ ] Langkah muncul satu per satu saat siswa menekan "Langkah berikutnya"
- [ ] Setiap langkah diberi label sesuai 5 langkah strategi (Amati, Cari lompatan, Periksa, Rumuskan, Cek ulang)

**US-08 (F07) — Contoh setengah jadi**
Sebagai siswa, saya ingin melengkapi contoh yang sebagian langkahnya kosong, agar saya berlatih secara bertahap.
- [ ] Contoh pertama: 1 langkah kosong; contoh berikutnya: 2 langkah; dst.
- [ ] Isian langsung diberi umpan balik

## Epik D — Berlatih

**US-09 (F08) — Latihan interaktif**
Sebagai siswa, saya ingin mengerjakan berbagai bentuk soal, agar latihan tidak membosankan.
- [ ] Jenis soal: isian angka, isian rumus, pilihan ganda, seret-lepas, lengkapi tabel
- [ ] Tidak ada batas waktu
- [ ] Soal bisa dilewati dan dikerjakan kembali nanti

**US-10 (F09) — Petunjuk bertingkat**
Sebagai siswa yang buntu, saya ingin mendapat petunjuk bertahap, agar saya tetap bisa mengerjakan soal sendiri dan tidak menyerah.
- [ ] Tombol "Butuh petunjuk?" selalu terlihat
- [ ] Petunjuk dibuka berurutan: 1 → 2 → 3
- [ ] Jumlah petunjuk yang dipakai dicatat (tanpa pengurangan nilai yang menghukum)

**US-11 (F10) — Umpan balik yang menjelaskan**
Sebagai siswa, saya ingin tahu letak kesalahan saya, agar saya bisa memperbaikinya.
- [ ] Jawaban salah yang umum mendapat umpan balik khusus
- [ ] Jawaban salah lainnya mendapat umpan balik umum + saran membuka petunjuk
- [ ] Siswa bisa mencoba lagi

**US-12 (F11) — Cek Aturanmu**
Sebagai siswa, saya ingin menguji rumus saya ke suku yang sudah diketahui, agar saya yakin jawaban saya benar sebelum mengirim.
- [ ] Siswa memasukkan rumus (mis. 3n + 1), aplikasi menampilkan tabel hasil n = 1, 2, 3 di samping suku asli
- [ ] Baris yang cocok ditandai ✓, yang tidak cocok ditandai ✗
- [ ] Muncul ajakan "Sudah cek aturanmu?" bila siswa mengirim tanpa mengecek (bisa diabaikan)

## Epik E — Refleksi dan Progres

**US-13 (F12) — Jelaskan dengan kata-katamu**
Sebagai siswa, saya ingin menjelaskan cara saya menemukan pola, agar pemahaman saya lebih kuat.
- [ ] Pilihan kalimat rumpang ("Polanya bertambah ___ setiap suku") atau isian bebas
- [ ] Tidak dinilai benar/salah; ditampilkan contoh penjelasan sebagai pembanding

**US-14 (F16) — Skala usaha mental**
Sebagai peneliti, saya ingin siswa menilai usaha mentalnya setelah latihan, agar saya bisa mengukur beban kognitif.
- [ ] Skala 1 (sangat-sangat ringan) – 9 (sangat-sangat berat), satu pertanyaan
- [ ] Muncul di akhir setiap sesi latihan dan kuis

**US-15 (F13) — Progres**
Sebagai siswa, saya ingin melihat modul mana yang sudah selesai, agar saya tahu harus melanjutkan dari mana.
- [ ] Peta modul dengan status: belum, sedang, selesai
- [ ] Tombol "Lanjutkan belajar" membuka posisi terakhir

**US-16 (F17) — Ekspor data**
Sebagai peneliti, saya ingin mengekspor data belajar siswa secara anonim, agar bisa dianalisis.
- [ ] Ekspor ke CSV/JSON berisi kode siswa (diisi manual, mis. S01), skor pretest/posttest, skor kuis, skala Paas, jumlah petunjuk
- [ ] Tidak memuat nama atau data pribadi
- [ ] Menu ekspor tersembunyi di halaman "Tentang" (tidak mengganggu siswa)

## Epik G — Literasi Matematika

**US-18 (F20) — Siklus pemecahan masalah**
Sebagai siswa, saya ingin dipandu langkah demi langkah saat mengerjakan soal cerita, agar saya tahu harus mulai dari mana.
- [ ] Ikon siklus BACA → UBAH → HITUNG → CEK CERITA tampil di atas soal literasi, dengan langkah aktif disorot
- [ ] Tahap A: keempat langkah diberi isian terstruktur; tahap B: hanya BACA dan CEK CERITA; tahap C: hanya ikon
- [ ] Tahap ditentukan oleh posisi modul (M1–M3 = A, M4–M7 = B, M8/kuis = C)

**US-19 (F21) — Bantuan membaca**
Sebagai siswa yang kesulitan memahami soal cerita, saya ingin bisa menandai informasi penting, agar saya tidak bingung dengan teks yang panjang.
- [ ] Siswa bisa mengetuk kata/angka di stimulus untuk menyorotnya
- [ ] Bagian yang disorot otomatis masuk ke kartu "Diketahui"; siswa mengisi "Ditanya"
- [ ] Istilah yang mungkin asing bisa diketuk untuk melihat artinya
- [ ] Stimulus dan soal bisa dilihat bersamaan tanpa berpindah layar (stimulus bisa dilipat/dibuka)

**US-20 (F22) — Setuju atau tidak?**
Sebagai siswa, saya ingin menilai pendapat tokoh dalam soal, agar saya terlatih bernalar dan memberi alasan.
- [ ] Siswa memilih Setuju/Tidak setuju, lalu memilih alasan dari 3–4 pilihan (dinilai otomatis)
- [ ] Opsional: menulis alasan sendiri (disimpan untuk penilaian peneliti)
- [ ] Umpan balik menjelaskan alasan yang tepat, termasuk kekeliruan tokoh

**US-21 (F24) — Cek cerita**
Sebagai siswa, saya ingin diingatkan untuk mengembalikan jawaban ke cerita, agar jawaban saya masuk akal.
- [ ] Setelah menghitung, muncul 1–2 pertanyaan pemandu ("Satuannya apa?", "Bolehkah jawabannya pecahan?")
- [ ] Jawaban akhir ditulis dalam kalimat konteks (mis. "Paling banyak 10 baris kursi")
- [ ] Jawaban yang benar secara hitungan tetapi tidak masuk akal (mis. 10,33 baris) mendapat umpan balik khusus

**US-22 (F23) — Stimulus bergaya AKM**
Sebagai siswa, saya ingin berlatih soal seperti AKM, agar saya terbiasa dengan bentuk soal asesmen nasional.
- [ ] Satu stimulus untuk 3–4 soal berjenjang L1 → L3
- [ ] Mendukung PG, PG kompleks (Benar/Salah per pernyataan), menjodohkan, isian, uraian singkat
- [ ] Panjang stimulus mengikuti batas di CLAUDE.md (≤ 60 / ≤ 120 kata)

**US-23 (F25) — Profil literasi**
Sebagai siswa, saya ingin tahu langkah mana yang sudah kuat dan mana yang perlu dilatih, agar latihan saya lebih terarah.
- [ ] Ringkasan per langkah siklus dalam kalimat positif, bukan angka atau peringkat
- [ ] Satu saran latihan berikutnya
- [ ] Data per indikator LM1–LM7 ikut terekspor untuk peneliti (F17)

## Epik F — Akses

**US-17 (F14) — Offline**
Sebagai siswa dengan kuota terbatas, saya ingin aplikasi tetap bisa dipakai tanpa internet, agar saya bisa belajar kapan saja.
- [ ] Setelah dibuka sekali (atau dipasang sebagai PWA), semua materi inti tersedia offline
- [ ] Ada tanda kecil status offline
