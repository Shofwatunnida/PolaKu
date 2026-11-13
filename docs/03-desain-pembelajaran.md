# 03 — Desain Pembelajaran Berbasis Teori Beban Kognitif

## 1. Landasan Teori Singkat

Memori kerja manusia terbatas: hanya bisa memproses sekitar 4 ± 1 unit informasi baru sekaligus. Teori Beban Kognitif membagi beban menjadi tiga:

| Jenis beban | Strategi di aplikasi |
|---|---|
| **Intrinsik**: kerumitan materi | **Kelola**: urutkan dari sederhana ke kompleks, pecah per bagian, aktifkan prasyarat |
| **Ekstrinsik**: cara penyajian yang tidak perlu | **Kurangi**: hilangkan elemen yang mengganggu, satukan teks dan gambar, beri tempo sendiri |
| **Germane**: usaha membangun skema | **Dorong**: self-explanation, variasi contoh, memeriksa ulang |

Rujukan utama:
- Sweller, J., van Merriënboer, J. J. G., & Paas, F. (2019). Cognitive architecture and instructional design: 20 years later. *Educational Psychology Review, 31*, 261–292.
- Mayer, R. E. (2021). *Multimedia Learning* (3rd ed.). Cambridge University Press.
- Paas, F. (1992). Training strategies for attaining transfer of problem-solving skill in statistics: A cognitive-load approach. *Journal of Educational Psychology, 84*(4), 429–434.
- Renkl, A., & Atkinson, R. K. (2003). Structuring the transition from example study to problem solving. *Educational Psychologist, 38*(1), 15–22.

## 2. Pemetaan Prinsip → Fitur

| Prinsip / efek | Penjelasan singkat | Penerapan di PolaKu | Kode temuan |
|---|---|---|---|
| Worked example effect | Pemula belajar lebih baik dari contoh lengkap daripada langsung memecahkan soal | F06 Contoh Lengkap | IL02 |
| Completion / fading effect | Peralihan bertahap dari contoh ke soal mandiri | F07 Contoh Setengah Jadi | IL02, GL03 |
| Segmenting | Materi dipecah menjadi bagian yang dikendalikan siswa | F03, tombol "Lanjut" | EL02 |
| Pre-training | Kenalkan istilah kunci sebelum materi inti | F02 Pengingat Prasyarat | K03 |
| Modality | Gambar + narasi suara lebih baik daripada gambar + teks panjang | Video dengan narasi | GL01 |
| Spatial contiguity | Teks diletakkan dekat gambar yang dijelaskannya | Label selisih tepat di antara suku | IL01 |
| Coherence | Buang materi yang tidak relevan | Tanpa musik latar/dekorasi | EL01 |
| Signaling | Tandai informasi penting | Warna/panah pada selisih dan suku yang dicari | IL01 |
| Split-attention | Hindari memaksa siswa menggabungkan sumber yang terpisah | Soal, gambar, dan isian dalam satu layar | EL01 |
| Self-explanation | Menjelaskan ke diri sendiri memperdalam skema | F12 "Jelaskan dengan Kata-katamu" | GL04 |
| Variability effect | Variasi konteks soal memperkuat transfer (setelah dasar dikuasai) | Soal konteks: kursi, ubin, tabungan | GL |
| Expertise reversal | Bantuan yang berguna bagi pemula bisa membebani yang sudah mahir | Tes awal → lompat materi; petunjuk opsional | K03 |

## 3. Alur Belajar per Subtopik

```
[Pemanasan 1 menit]   → aktifkan ingatan (1–2 soal sangat mudah)
        ↓
[Konsep]              → video 1–3 menit + visual + ≤3 kalimat inti
        ↓
[Contoh Lengkap]      → langkah muncul satu per satu (siswa yang menekan "Langkah berikutnya")
        ↓
[Contoh Setengah Jadi]→ 1 langkah kosong → 2 langkah kosong → ...
        ↓
[Latihan Mandiri]     → 4–6 soal, petunjuk bertingkat, "Cek Aturanmu", umpan balik
        ↓
[Literasi]            → 1 stimulus kontekstual, 3–4 soal L1→L3, siklus BACA–UBAH–HITUNG–CEK CERITA
        ↓
[Refleksi]            → "Jelaskan caramu menemukan pola" + skala usaha mental (1–9)
        ↓
[Kuis Subtopik]       → 3–5 soal tanpa petunjuk, tanpa batas waktu
```

## 4. Strategi Menemukan Pola (diajarkan eksplisit, menjadi "skema")

Aplikasi mengajarkan langkah tetap yang selalu sama di setiap soal (mengurangi beban karena siswa tidak perlu menebak caranya):

1. **Amati**: tulis suku-suku yang diketahui.
2. **Cari lompatan**: hitung selisih antarsuku.
3. **Periksa**: apakah selisihnya tetap? Jika tidak, cari selisih tingkat kedua atau hubungan lain (dikali, dijumlah dua suku sebelumnya, bilangan kuadrat).
4. **Rumuskan**: tulis aturan dalam kata-kata, lalu sebagai rumus suku ke-n.
5. **Cek ulang**: uji aturan ke suku ke-1, ke-2, ke-3 (fitur "Cek Aturanmu").

Ikon kelima langkah ini muncul konsisten di setiap soal sebagai "peta langkah".

## 5. Desain Petunjuk Bertingkat (contoh)

Soal: *Tentukan suku ke-10 dari pola 3, 6, 9, 12, …*

| Tingkat | Isi petunjuk |
|---|---|
| 1 — Arahkan perhatian | "Perhatikan berapa lompatan dari satu suku ke suku berikutnya." |
| 2 — Beri langkah | "Lompatannya selalu +3. Berarti setiap suku adalah 3 × urutannya. Suku ke-1 = 3 × 1." |
| 3 — Hampir selesai | "Suku ke-n = 3 × n. Jadi suku ke-10 = 3 × 10 = …" |

Penggunaan petunjuk **tidak mengurangi nilai** secara menghukum, tetapi dicatat untuk refleksi ("Kamu memakai 1 petunjuk").

## 6. Desain Umpan Balik

Umpan balik untuk jawaban salah memetakan **miskonsepsi yang umum**:

| Jawaban siswa (soal 3, 6, 9, …, suku ke-10) | Kemungkinan kekeliruan | Umpan balik |
|---|---|---|
| 15 | Hanya menghitung suku berikutnya | "Itu suku ke-5. Yang ditanya suku ke-10. Lanjutkan polanya, atau pakai aturan 3 × n." |
| 13 | Menambah 1 tiap suku / salah selisih | "Coba hitung lagi lompatannya: 6 − 3 = ?" |
| 33 | Rumus n + 3 atau 3n + 3 | "Coba cek aturanmu untuk suku ke-1: apakah hasilnya 3?" |

## 7. Pengendalian Beban per Layar (checklist desainer konten)

- [ ] Hanya 1 konsep baru
- [ ] ≤ 3 kalimat penjelasan, ≤ 15 kata per kalimat
- [ ] Gambar dan label berdekatan
- [ ] Tidak ada elemen dekoratif yang bergerak
- [ ] Siswa yang mengendalikan kapan lanjut
- [ ] Istilah baru sudah dikenalkan sebelumnya

## 8. Integrasi Literasi Matematika

Literasi matematika tidak dipisah menjadi menu tersendiri. Literasi **dijalin di setiap modul** sebagai tahap setelah latihan murni. Alasannya dari sisi beban kognitif: siswa perlu menguasai skema pola dulu sebelum memakainya dalam konteks, supaya memori kerjanya tidak penuh oleh dua hal baru sekaligus (konsep dan konteks).

- **Strategi 5 langkah** (bagian 4) = skema untuk *menemukan pola*.
- **Siklus BACA–UBAH–HITUNG–CEK CERITA** = skema untuk *memecahkan masalah nyata*. Langkah HITUNG memakai strategi 5 langkah.

Penjelasan lengkap, indikator LM1–LM7, jenjang soal, dan contoh stimulus ada di `11-literasi-matematika.md`.
