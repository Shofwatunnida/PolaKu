# 01 — Analisis Kebutuhan

Dokumen ini mengolah hasil wawancara awal menjadi kebutuhan aplikasi. Kerangka analisisnya adalah **Teori Beban Kognitif** (Sweller, 1988; Sweller, van Merriënboer & Paas, 2019).

## 1. Identitas Studi Pendahuluan

| Aspek | Keterangan |
|---|---|
| Responden | S01, siswa Kelas VIII SMP |
| Materi | Pola Bilangan (sudah dipelajari di kelas VII–VIII) |
| Waktu | Jumat, 6 November 2026 |
| Media | Google Meet, disertai contoh soal "Latihan Soal Pola Bilangan Kelas VII" |
| Pewawancara | Shofwatunnida |

## 2. Kerangka Pengodean

| Kode | Arti | Pertanyaan kunci |
|---|---|---|
| **K** | Konteks belajar | Kapan dan bagaimana siswa belajar materi ini? |
| **IL** | *Intrinsic Load*, beban dari kerumitan materi itu sendiri | Bagian mana yang sulit secara konsep? |
| **EL** | *Extraneous Load*, beban dari cara materi disajikan | Apa dari cara penyajian yang membebani/tidak membantu? |
| **GL** | *Germane Load*, usaha mental yang membangun pemahaman (skema) | Strategi apa yang membantu siswa benar-benar paham? |

## 3. Temuan dan Implikasi Desain

| Kode | Temuan | Implikasi bagi aplikasi |
|---|---|---|
| K01 | Materi pernah dipelajari di kelas VII dan VIII | Ada **pengetahuan prasyarat**, tetapi tidak bisa dianggap sudah dikuasai |
| K02 | Pembelajaran hanya memakai papan tulis | Aplikasi mengisi kekosongan media visual/interaktif |
| K03 | "Lupa bangett" | Perlu **modul pengingat prasyarat** dan **tes awal (diagnostik)** untuk mengetahui yang masih diingat |
| IL01 | Siswa mencoba mengamati selisih antarsuku, tetapi lambat | **Visualisasi selisih** antarsuku secara eksplisit (panah "+3") untuk membantu tahap pengenalan pola |
| IL02 | Kesulitan menentukan hubungan/perubahan antarbilangan | Pecah materi menjadi **langkah kecil**, dari pola sederhana (selisih tetap) ke pola kompleks (selisih bertingkat, Fibonacci). Gunakan **worked example** |
| EL01 | Hanya papan tulis, tanpa variasi media | Sajikan **representasi ganda**: gambar noktah/konfigurasi objek, tabel, bilangan, dan simbol |
| EL02 | Penjelasan guru → ±5 soal → yang selesai boleh pulang | Siswa yang lambat tertekan waktu. Aplikasi memberi **kecepatan belajar mandiri** tanpa batas waktu dan bisa diulang |
| GL01 | Belajar lewat video di rumah lebih mudah dipahami | Sediakan **video pendek per konsep** yang bisa dijeda dan diulang |
| GL02 | Tidak terbiasa memeriksa kembali jawaban | Fitur **"Cek Aturanmu"**: siswa menguji rumus ke suku yang sudah diketahui sebelum mengirim |
| GL03 | Bila tidak paham, memilih tidak menjawab | **Petunjuk bertingkat** agar siswa selalu punya langkah berikutnya, dan umpan balik yang menjelaskan |
| GL04 | Tidak pernah diskusi/belajar kelompok | Fitur **"Jelaskan dengan kata-katamu"** (self-explanation). Di fase berikutnya: mode berbagi cara dengan teman |

## 4. Rumusan Masalah Produk

> Siswa SMP kesulitan **mengenali hubungan antarsuku** pada pola bilangan. Mereka belajar dengan **media yang monoton** dan **tempo yang tidak sesuai kecepatannya**, serta **belum punya strategi** ketika buntu atau saat ingin memastikan jawabannya. Akibatnya beban kognitif ekstrinsik tinggi dan skema konsep pola bilangan tidak terbentuk.

## 5. Kebutuhan Utama (ringkasan)

1. Materi dipecah per konsep, disajikan dengan video pendek + visual + teks singkat.
2. Contoh lengkap → contoh setengah jadi → latihan (bertahap).
3. Visualisasi selisih antarsuku.
4. Petunjuk bertingkat dan umpan balik yang menjelaskan.
5. Pembiasaan memeriksa ulang dan menjelaskan kembali.
6. Belajar dengan tempo sendiri, tanpa tekanan waktu, bisa offline.
7. Tes awal untuk mengaktifkan dan memetakan pengetahuan prasyarat.
8. Soal kontekstual bertahap untuk menumbuhkan literasi matematika (lihat bagian 6).

## 6. Kaitan dengan Literasi Matematika

Wawancara belum menggali literasi matematika secara langsung, tetapi beberapa temuan memberi indikasi:

| Temuan | Indikasi literasi | Proses PISA yang perlu dikuatkan |
|---|---|---|
| IL01, IL02 | Lambat mengenali hubungan antarsuku | **Menggunakan** |
| GL02 | Tidak memeriksa ulang jawaban | **Menafsirkan & mengevaluasi** |
| GL03 | Berhenti ketika tidak memahami soal | **Merumuskan** (memahami situasi/soal) |
| GL04 | Tidak pernah menjelaskan cara kepada teman | **Penalaran & komunikasi** |
| K02, EL02 | Pembelajaran berupa latihan soal rutin | Kurang pengalaman soal **kontekstual/non-rutin** |

Karena itu, kebutuhan ke-8 ditambahkan: **soal kontekstual bertahap yang melatih siklus merumuskan → menggunakan → menafsirkan, dengan bantuan membaca dan penalaran** (lihat `11-literasi-matematika.md`).

**Saran untuk wawancara berikutnya:** berikan 1 soal cerita pola bilangan (mis. susunan kursi), lalu tanyakan:
- "Informasi apa yang penting dari cerita ini?" (merumuskan)
- "Bagaimana kamu mengubah ceritanya menjadi bilangan?" (merumuskan)
- "Apa arti jawabanmu untuk cerita ini? Apakah masuk akal?" (menafsirkan)
- "Pernahkah kamu mengerjakan soal seperti AKM atau soal cerita panjang? Bagian mana yang sulit?"

## 7. Keterbatasan dan Saran Studi Lanjutan

- **Baru satu responden.** Sebaiknya wawancara ditambah menjadi 3–5 siswa dengan kemampuan berbeda (tinggi/sedang/rendah), ditambah 1 guru matematika, supaya kebutuhan lebih kuat dan bisa ditriangulasi.
- Temuan K03 belum menggali bagian materi mana yang masih diingat. Tes diagnostik singkat bisa menjawab ini.
- Kecepatan penjelasan guru (EL02) belum tergali.
- **Catatan perbaikan dokumen wawancara:**
  - Baris GL01 belum memiliki kode awal (seharusnya "GL").
  - Nama asli siswa masih muncul di GL01 dan Kesimpulan, padahal identitas sudah disamarkan sebagai S01. Sebaiknya diganti "S01" demi etika penelitian.
  - Identitas menyebut materi dipelajari di "kelas VII", sedangkan K01 menyebut "kelas 7 dan 8". Samakan.
  - Typo kecil: "iswa" (IL01), "engalaman" (GL01).
