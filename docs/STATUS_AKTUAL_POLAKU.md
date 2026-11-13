# Status Aktual Proyek PolaKu

| | |
|---|---|
| Tanggal audit | 13 November 2026 |
| Cakupan | `frontend/`, `server/`, `tools/`, `tests/`, `docs/` |
| Metode | Membaca kode dan konten, menjalankan validator konten, menjalankan seluruh pengujian, menyalakan server dan memanggil endpoint-nya. Klaim di dokumentasi **tidak** dianggap bukti. |
| Perubahan kode selama audit | Tidak ada. Satu-satunya file baru adalah laporan ini. |

## Ringkasan

- **Aplikasi bisa dijalankan sekarang** di komputer (`python server/app.py`) dan **lulus semua pengujian otomatis** (200 lulus, 2 dilewati, 0 gagal).
- **Yang sudah benar-benar ada:** seluruh mesin aplikasi (alur 7 tahap per modul, 7 tipe soal, petunjuk, umpan balik, Cek Aturanmu, siklus literasi, skala Paas, progres, tes awal/akhir, ekspor data, PWA/offline) dan **konten 2 dari 9 modul** (M2, M4).
- **Yang belum ada:** 7 modul lain, semua video, beberapa fitur di PRD/user story (rinciannya di bagian 2), dashboard guru (Fase 2), dan validasi oleh ahli/siswa.
- **Untuk siswa lewat HP:** secara teknis siap untuk **uji coba terbatas** (mis. uji perorangan 3 siswa pada M2). Tetapi aplikasi **belum di-deploy ke alamat HTTPS** dan **belum pernah dicoba di HP sungguhan**. Semua pengujian HP masih berupa emulasi di laptop.
- **PWA & offline:** terbukti berfungsi di **Chromium (Edge) emulasi Android**. **Belum terbukti di iPhone/Safari** dan belum di perangkat fisik mana pun.
- **Masalah terpenting:** data pretest bisa tertimpa jika siswa mengulang Tes Awal (bagian 8, M1). Tes Awal dan Tes Akhir tidak paralel. Ada risiko kompatibilitas di HP lama.

---

## 1. Fitur yang Sudah Benar-Benar Diimplementasikan

Bukti diambil dari kode. Konten yang tersedia saat ini: `frontend/konten/m2.json`, `m4.json`, `tes-awal.json`, `tes-akhir.json`, `modul.json`.

### 1.1 Alur belajar per modul
| Fitur | Bukti | Catatan |
|---|---|---|
| Peta materi M0–M8 dengan status (belum/sedang/selesai/segera hadir) | `js/pages/modul.js` `halamanPeta` | Hanya M2 dan M4 yang `tersedia: true` (`konten/modul.json`) |
| 7 tahap: Konsep → Contoh Lengkap → Setengah Jadi → Latihan → Literasi → Refleksi → Kuis | `js/konten.js` `TAHAP`; `modul.js` `halamanTahap` | Siswa bisa membuka tahap mana pun langsung (tidak dikunci) |
| Konsep bersegmen (1 layar per segmen, tombol Kembali/Lanjut, "Bagian x dari y") | `modul.js` `tahapKonsep` | 5 segmen per modul |
| Contoh lengkap, langkah muncul satu per satu dengan label strategi | `modul.js` `tahapContoh` | 2 contoh per modul |
| Contoh setengah jadi dengan langkah kosong + "Tunjukkan jawabannya" setelah 2× salah | `modul.js` `tahapSetengah` | Jumlah langkah kosong bertambah (1 → 2) |
| Latihan: petunjuk 3 tingkat, umpan balik miskonsepsi, "Lewati dulu", ringkasan | `js/soal.js` `soalInteraktif`; `ui.js` `kotakPetunjuk` | 5 soal per modul |
| Cek Aturanmu (uji rumus ke suku yang diketahui) + ajakan "Sudah cek aturanmu?" | `ui.js` `cekAturanmu`; `soal.js` | Muncul pada soal isian angka/rumus yang punya `pola` |
| Panah lompatan antarsuku, termasuk selisih tingkat dua | `ui.js` `barisanPola`, `barisanDenganTombol` | Di latihan disembunyikan, dibuka dengan tombol |
| Gambar noktah SVG (persegi, persegi panjang, segitiga, ganjil, genap), noktah baru diberi warna | `ui.js` `gambarNoktah` | |
| Refleksi (penjelasan bebas + contoh pembanding) | `modul.js` `tahapRefleksi` | Isian bebas, bukan kalimat rumpang pilihan (lihat 2.2) |
| Skala usaha mental Paas 1–9 (setelah refleksi dan setelah kuis) | `ui.js` `skalaPaas`; `modul.js` | Daftar vertikal dengan label kata |
| Kuis tanpa petunjuk dan tanpa batas waktu, menandai modul "selesai" | `modul.js` `tahapKuis` | 4 soal per modul |

### 1.2 Tipe soal
Dibuat di `js/soal.js` `buatIsian` dan dinilai di `js/answer.js` `periksaJawaban`:

| Tipe | Ada di kode | Dipakai di konten |
|---|---|---|
| isian-angka | ✅ | ✅ (30, termasuk langkah kosong contoh setengah jadi) |
| isian-rumus (dengan papan rumus) | ✅ | ✅ (6, termasuk langkah kosong) |
| pilihan-ganda | ✅ | ✅ (3) |
| pg-kompleks (Benar/Salah per pernyataan) | ✅ | ✅ (2, hanya di kuis) |
| menjodohkan | ✅ | ✅ (1) |
| lengkapi-tabel (otomatis vertikal di layar sempit) | ✅ | ✅ (1 + tabel UBAH di literasi) |
| klaim ("Setuju atau Tidak?" + alasan) | ✅ | ✅ (3) |
| uraian-singkat | ✅ | ❌ belum dipakai di konten mana pun |
| seret-lepas | ❌ | ❌ |

Pemeriksa jawaban (`answer.js`) menerima variasi penulisan rumus (`3n+1`, `1+3n`, `3×n+1`, `n²`, `Uₙ = …`) tanpa `eval()`, dan angka gaya Indonesia (`Rp35.000`, `10,33`). Umpan balik bisa punya `toleransi`.

### 1.3 Literasi matematika
| Fitur | Bukti |
|---|---|
| Siklus BACA → UBAH → HITUNG → CEK CERITA dengan indikator langkah | `js/pages/literasi.js` |
| BACA: ketuk kata untuk menyorot → otomatis masuk "Diketahui"; isian "Ditanya"; umpan balik "x dari y informasi penting" | `literasi.js` `kartuStimulus`, `frasaTersorot` |
| UBAH: lengkapi tabel (hanya tahap A) | `literasi.js` |
| CEK CERITA: pertanyaan kewajaran jawaban | `literasi.js`, field `pertanyaanCekCerita` |
| Tahap bantuan A/B/C (dari field `tahapSiklus`) | `literasi.js`; konten memakai **A (M2) dan B (M4)**. **Tahap C ada di kode tetapi belum dipakai konten mana pun** |
| Stimulus kartu dapat dilipat; daftar kata sulit (glosarium) | `literasi.js` |
| Profil Literasi (berdasarkan benar pada percobaan pertama) | `js/pages/progres.js` `profilLiterasi` |

Konten literasi: 1 stimulus per modul ("Kursi Lomba 17 Agustus" di M2, "Motif Batik Kawung" di M4), masing-masing 4 soal L1→L3.

### 1.4 Tes, progres, data
| Fitur | Bukti |
|---|---|
| Tes Awal (6 soal) dengan rekomendasi modul; benar/salah tidak ditampilkan | `js/pages/tes.js`; `soal.js` (mode `tes`) |
| Tes Akhir (8 soal, termasuk 3 soal cerita/penalaran) | `konten/tes-akhir.json` |
| Penyimpanan lokal (progres, percobaan, literasi, Paas, refleksi, tes, posisi) | `js/storage.js` (localStorage `polaku:v1`) |
| Melanjutkan dari posisi terakhir setelah muat ulang (konsep, contoh, setengah, latihan, literasi, kuis, tes) | `storage.js` `simpanPosisi`; `modul.js`, `literasi.js`, `tes.js` |
| Halaman Progres (bilah tahap, profil literasi, skor tes) | `progres.js` |
| Kode siswa, Unduh data (.json), Bagikan data (.txt via Web Share), Kirim ke peneliti (opsional), Hapus data dengan konfirmasi | `js/pages/tentang.js` |

### 1.5 PWA & smartphone
| Fitur | Bukti |
|---|---|
| Manifest (ikon 192/512/maskable/SVG, `standalone`) | `frontend/manifest.webmanifest`, `frontend/icons/` |
| Service worker: cache 26 aset, versi otomatis (hash), navigasi offline ke `index.html` | `frontend/sw.js`; `tools/build_aset.py`. Versi di `sw.js` **cocok** dengan isi file saat audit |
| Tombol "Pasang Aplikasi" (Android/Chrome) & petunjuk iOS | `js/pasang.js`; `beranda.js` |
| Pemberitahuan versi baru + cek pembaruan saat aplikasi dibuka kembali | `js/app.js` |
| Minta penyimpanan permanen (hanya jika sudah terpasang) | `app.js` `mintaPenyimpananPermanen` |
| Navigasi bawah disembunyikan saat mengetik (tanpa menggeser tata letak) | `app.js`; `style.css` |
| Papan rumus dengan angka (keyboard HP tidak muncul) + tombol ⌨️ | `ui.js` `papanRumus` |
| Enter/"Selesai" mengirim atau pindah kotak; gulir otomatis ke umpan balik | `soal.js` |
| Ukuran kotak suku menyesuaikan layar; aturan untuk layar ≤ 360px | `style.css` (`--suku`, `@media (max-width: 360px)`) |
| Pemberitahuan jika dibuka lewat http (bukan https) | `beranda.js` |

### 1.6 Server & alat Python
| Fitur | Bukti |
|---|---|
| Flask menyajikan `frontend/`, MIME manifest benar, `sw.js` tanpa cache, header keamanan (CSP, nosniff, dll.) | `server/app.py` |
| `/api/status`; `/api/penelitian` (nonaktif bawaan, validasi kode siswa, hanya menyimpan data belajar) | `server/app.py` |
| Menampilkan alamat Wi-Fi saat `--host 0.0.0.0` | `server/app.py` `alamat_lan` (diverifikasi: tercetak `http://192.168.1.7:5078`) |
| Validator konten (struktur + aturan pedagogis) | `tools/validasi_konten.py` → "✓ Konten valid (0 peringatan)" |
| Analisis data (CSV, N-gain, Paas, literasi per kelompok; membaca .json & .txt) | `tools/analisis_data.py` |
| Pembuat ikon tanpa pustaka tambahan | `tools/buat_ikon.py` |

---

## 2. Fitur yang Baru Direncanakan/Didokumentasikan, Belum Diimplementasikan

### 2.1 Konten
| Item | Dokumen | Kondisi nyata |
|---|---|---|
| Modul M0, M1, M3, M5, M6, M7, M8 | `docs/04`, `modul.json` | **Belum ada file konten.** Tampil "Segera hadir" |
| Video per konsep (1–3 menit, subtitle) | PRD F03, US-04, `docs/04` §5 | **Tidak ada video sama sekali.** `src` kosong, folder `frontend/media/` tidak ada. Pemutar video dan dukungan subtitle sudah ada di kode, tetapi yang tampil hanya kotak "Video … sedang disiapkan" |
| Stimulus literasi untuk M1–M8, konteks personal & saintifik | `docs/11` §7 | Hanya 2 stimulus, keduanya konteks sosial-budaya |
| Stimulus tahap C (mandiri) | `docs/11` §5 | Didukung kode, belum ada kontennya |
| Tes literasi pretest–posttest paralel + rubrik | `docs/08` §B.5 | Belum ada. Tes Akhir hanya memuat 3 soal cerita |

### 2.2 Fitur aplikasi
| Fitur | Dokumen | Kondisi nyata |
|---|---|---|
| F02 Pengingat Prasyarat | PRD, US-02 | **Belum ada** (bergantung pada modul M0) |
| F05/US-06 Representasi ganda yang bisa ditukar (Gambar · Tabel · Bilangan · Rumus) dan saling terhubung | PRD (P0), US-06 | **Belum ada.** Representasi hanya muncul terpisah di segmen yang berbeda; tidak ada tab dan tidak ada sorotan terhubung |
| F12/US-13 Kalimat rumpang dengan pilihan | US-13 | Sebagian: hanya kotak isian bebas dengan awalan kalimat |
| US-09 Soal yang dilewati bisa dikerjakan kembali nanti | US-09 | Sebagian: hanya dengan mengulang seluruh latihan |
| US-19 Ketuk istilah untuk melihat artinya | US-19 | Sebagian: arti ditampilkan sebagai daftar "Kata sulit", tidak bisa diketuk |
| US-21 Jawaban akhir ditulis dalam kalimat konteks | US-21 | **Belum ada** |
| US-18 Tahap bantuan ditentukan dari posisi modul | US-18 | Berbeda: ditentukan oleh field `tahapSiklus` di konten (lebih fleksibel, tetapi tidak sesuai teks US) |
| Soal seret-lepas | `docs/04`, US-09 | **Belum ada** |
| Umpan balik dalam "lembar bawah" (bottom sheet) | `docs/06` §4 | Berbeda: umpan balik tampil di dalam kartu soal |
| Font Nunito/Lexend, KaTeX, mode gelap | `docs/06` | Tidak dipakai (font sistem, rumus berupa teks biasa) |
| F18 Dashboard guru, F19 Berbagi cara, F26 Pola di Sekitarku | PRD (P2) | **Belum ada** (memang direncanakan untuk Fase 2) |
| APK lewat PWABuilder | `docs/12` §4 | Hanya panduan; belum pernah dibuat/dicoba |
| Deploy HTTPS (GitHub Pages/Netlify/Render) | `docs/12` §3 | **Belum dilakukan** |

### 2.3 Kegiatan penelitian (`docs/08`, `docs/09`)
Belum dilaksanakan: wawancara tambahan (3–5 siswa + guru), validasi ahli materi & media, uji perorangan, uji kelompok kecil, uji lapangan, pengumpulan data nyata.

---

## 3. Fitur yang Sudah Diuji dan Hasilnya

Perintah: `python -m pytest`. **Hasil saat audit: 200 lulus, 2 dilewati, 0 gagal (±94 detik).** Validator konten: **0 kesalahan, 0 peringatan.**

| File uji | Jumlah | Yang diuji | Hasil |
|---|---|---|---|
| `tests/test_js_logic.py` | 89 | Pemeriksa rumus (14 variasi), rumus tidak valid, parsing angka (12 kasus), toleransi umpan balik, Cek Aturanmu, tipe klaim, deteksi pola, banyak noktah, dan **setiap kunci jawaban di konten dinilai benar serta setiap umpan balik miskonsepsi terpicu** (JS dijalankan di V8 lewat mini-racer) | Lulus |
| `tests/test_konten.py` | 17 | Validator menolak segmen > 3 kalimat, kunci rumus salah, petunjuk ≠ 3, literasi tidak berjenjang/tanpa LM6, stimulus terlalu panjang, modul tanpa file; evaluator rumus menolak kode berbahaya | Lulus |
| `tests/test_server.py` | 14 | Beranda + CSP, manifest (MIME, ikon 192/512, standalone), ikon PNG valid, `sw.js` memuat semua aset & tidak "dev", status API, path traversal ditolak, endpoint penelitian (nonaktif → 403, aktif → simpan, kode tidak valid → 400, bukan JSON → 400, field asing dibuang) | Lulus |
| `tests/test_analisis.py` | 7 | Rumus N-gain & kategori, CSV ringkasan, pemilihan file terbaru per siswa, file rusak dilewati | Lulus |
| `tests/e2e/test_alur.py` | 18 (6 uji × 3 perangkat) | **Android 390px, Android 320px (Galaxy S9+), iPhone 13 (WebKit)**: alur lengkap M2 (konsep → kuis, termasuk literasi, refleksi, Paas), tes awal + rekomendasi, visual M4, hapus data, kirim ke peneliti. Khusus Chromium: syarat installable (CDP) dan offline | 16 lulus, 2 dilewati (installable & offline di WebKit) |
| `tests/e2e/test_ponsel.py` | 57 (19 uji × 3 perangkat) | 13 layar: tidak bisa digeser ke samping & target sentuh ≥ 44px; tabel vertikal; Enter mengirim/pindah kotak; papan rumus (angka, sisip di tengah, hapus, ⌨️); navigasi tidak menghalangi ketukan; lanjut setelah muat ulang (konsep, latihan, literasi, tes); skala Paas; kata cerita mudah ditandai | Lulus |

**Pemeriksaan manual saat audit:** server menyala; `/`, `/api/status`, `/manifest.webmanifest`, `/sw.js`, `/konten/m2.json`, `/js/app.js` → 200; `/server/app.py` → 404 (kode server tidak bocor); POST `/api/penelitian` → ditolak karena nonaktif.

---

## 4. Fitur yang Belum Diuji

| Fitur | Keterangan |
|---|---|
| **Perangkat fisik (HP Android/iPhone sungguhan)** | Semua uji HP berupa emulasi di laptop |
| **Offline & service worker di iPhone/Safari (WebKit)** | Sengaja dilewati di pengujian |
| Klik tombol "📲 Pasang Aplikasi" (event `beforeinstallprompt`) dan pemasangan sungguhan | Yang diuji hanya *syarat* installable lewat CDP. Satu-satunya galat, `in-incognito`, diabaikan karena Playwright selalu memakai jendela privat |
| Pemberitahuan versi baru (`controllerchange`) dan pembaruan saat aplikasi dibuka kembali | Tidak ada uji |
| Penyimpanan permanen (`navigator.storage.persist`) | Tidak ada uji |
| Tombol "Bagikan data" (Web Share) dan "Unduh data" | Tidak ada uji. Uji E2E hanya memakai jalur "Kirim ke peneliti" |
| Alur lengkap **M4** (contoh, setengah jadi, latihan, kuis, literasi tahap B sampai selesai) | E2E hanya membuka konsep M4 dan pengantar literasi M4. Kunci jawaban M4 tetap diuji di `test_js_logic.py` |
| Alur lengkap **Tes Akhir** di browser | Hanya kunci jawabannya yang diuji |
| Tombol "Lewati dulu" | Tidak ada uji |
| Halaman Progres dengan data campuran, Profil Literasi saat semua benar/salah | Diuji sebagian (hanya satu skenario) |
| Pemutaran video & subtitle | Tidak bisa diuji karena belum ada video |
| Server di mode `--host 0.0.0.0` diakses dari HP lewat Wi-Fi | Hanya dicek bahwa alamatnya tercetak |
| Aksesibilitas otomatis (Lighthouse/axe), pembaca layar | Belum dijalankan (direncanakan di `docs/08`) |
| Performa di HP spesifikasi rendah, skor Lighthouse | Belum diukur. Ukuran frontend 165 KB (JS 97 KB, tanpa kompresi) |
| Browser lama (lihat masalah M3 di bagian 8) | Belum diuji |
| Analisis data dengan data siswa nyata | Belum ada data |
| Pengujian pedagogis (validasi ahli, uji siswa, beban kognitif, N-gain) | Belum dilaksanakan |

---

## 5. Apakah Aplikasi Dapat Dijalankan Saat Ini?

**Ya.** Dari folder `aplikasi-pola-bilangan`:
```bash
.venv\Scripts\activate
python server/app.py            # http://localhost:5000
```
Terverifikasi saat audit: server menyala, mencetak alamat lokal dan alamat Wi-Fi, semua aset tersaji, dan validator konten lulus.

Catatan:
- Lingkungan `.venv` sudah berisi Flask, pytest, mini-racer, Playwright, dan WebKit. Di komputer lain perlu `pip install -r requirements.txt` (dan `python -m playwright install webkit` untuk uji iPhone).
- Server memakai **server pengembangan Flask** (muncul peringatan "Do not use it in a production deployment"). Ini cukup untuk uji coba, tetapi kurang tepat untuk deploy jangka panjang (lihat masalah M5).

---

## 6. Apakah Aplikasi Sudah Bisa Dipakai Siswa Lewat HP?

**Belum untuk pemakaian umum. Bisa untuk uji coba terbatas setelah satu langkah: deploy.**

| Syarat | Status |
|---|---|
| Tampilan dan interaksi layak di layar HP (320–390px, sentuh) | ✅ Terbukti di emulasi (Android & iPhone/WebKit) |
| Dapat diakses siswa dari HP mereka | ❌ **Belum di-deploy.** Saat ini hanya bisa lewat laptop di Wi-Fi yang sama (http, tanpa pasang/offline), atau lewat USB + port forwarding untuk satu HP Android |
| Dicoba di HP sungguhan | ❌ Belum |
| Konten cukup untuk pembelajaran | ⚠️ Hanya M2 dan M4, tanpa video. Cukup untuk **uji perorangan M2** (roadmap Fase 5), belum cukup untuk satu topik penuh |
| Konten sudah divalidasi | ❌ Masih draf, belum ditelaah dosen/guru/ahli |
| Data penelitian aman | ⚠️ Ada risiko pretest tertimpa (M1) |

---

## 7. Apakah PWA dan Fitur Offline Benar-Benar Berfungsi?

| Aspek | Terbukti? | Bukti |
|---|---|---|
| Manifest valid & memenuhi syarat installable | ✅ di Chromium | `test_beranda_dan_pwa`: `Page.getInstallabilityErrors` hanya `in-incognito` (akibat lingkungan uji) |
| Service worker terpasang & mengendalikan halaman | ✅ di Chromium | `test_offline_setelah_kunjungan_pertama` menunggu `serviceWorker.controller` |
| Halaman materi terbuka saat offline | ✅ di Chromium | Uji yang sama: mode offline → `#/modul/m2/konsep` tampil + label "Mode offline" |
| Daftar aset offline mutakhir | ✅ | Versi di `sw.js` = hash isi file (diperiksa saat audit) |
| Offline di iPhone/Safari | ❓ Belum terbukti | Uji dilewati di WebKit |
| Pemasangan sungguhan dari tombol/menu browser | ❓ Belum terbukti | Butuh HP sungguhan + HTTPS |
| Pembaruan versi ke pengguna yang sudah memasang | ❓ Belum terbukti | Tidak ada uji |
| Offline lewat alamat http (Wi-Fi) | ❌ Memang tidak berfungsi | Browser mewajibkan HTTPS/localhost; aplikasi sudah menampilkan pemberitahuan |

**Kesimpulan:** mekanisme PWA dan offline sudah diimplementasikan dengan benar dan terbukti bekerja di Chromium (setara Chrome Android) dalam emulasi. Pembuktian di iPhone dan di perangkat fisik belum dilakukan.

---

## 8. Masalah dan Kekurangan yang Ditemukan

### Tinggi (memengaruhi data penelitian atau pemakaian nyata)
| Kode | Masalah | Bukti | Dampak |
|---|---|---|---|
| M1 | **Pretest bisa tertimpa.** Beranda menawarkan "Ulangi Tes Awal", dan setiap pengulangan menambah catatan baru. Skrip analisis memakai **catatan terakhir** | `beranda.js:65`; `tools/analisis_data.py:72–74` | Jika siswa mengulang Tes Awal setelah belajar, skor pretest naik dan N-gain menjadi terlalu kecil/bias |
| M2 | **Tes Awal (6 soal diagnostik) dan Tes Akhir (8 soal, termasuk literasi) tidak paralel** | `konten/tes-awal.json`, `tes-akhir.json` | N-gain dari aplikasi tidak sah untuk skripsi. Skrip analisis sudah memberi peringatan, tetapi instrumen paralel belum ada |
| M3 | **Belum di-deploy & belum dicoba di HP fisik / iPhone** | Bagian 4, 6, 7 | Perilaku nyata (keyboard HP, pemasangan, offline iOS, performa HP murah) belum terkonfirmasi |
| M4 | **Konten baru 2 modul, tanpa video**; konten belum divalidasi ahli | `konten/`, `modul.json` | Belum mencakup materi pola bilangan secara utuh. Fitur video (dasar temuan GL01) belum terwujud |

### Sedang
| Kode | Masalah | Bukti | Dampak |
|---|---|---|---|
| M5 | Panduan deploy Pilihan B memakai `python server/app.py` = server pengembangan Flask | `server/app.py:140`; `docs/12` §3B | Kurang stabil/aman untuk dipakai banyak siswa sekaligus. Perlu server WSGI (mis. waitress/gunicorn) |
| M6 | Endpoint `/api/penelitian` (saat diaktifkan) tanpa autentikasi dan tanpa pembatasan laju | `server/app.py` (tidak ada token/rate limit) | Siapa pun yang tahu alamatnya bisa mengirim data palsu/spam selama fitur aktif |
| M7 | Kompatibilitas HP lama: `Array.prototype.at()` (Chrome 92+, iOS Safari 15.4+) di halaman Progres; CSS `:has()` (Chrome 105+, iOS 15.4+) untuk sorotan pilihan | `progres.js:32–33`; `style.css:195` | Di HP/browser lama, halaman Progres bisa error; sorotan pilihan ganda tidak tampil (tetap bisa dipakai) |
| M8 | Hosting statis (Pilihan A) tidak mengirim header keamanan (CSP, dll.); header hanya dipasang oleh Flask. `sw.js` juga harus dibangun ulang manual sebelum deploy | `server/app.py`; `docs/12` §3A | Keamanan sedikit lebih lemah di hosting statis; jika lupa menjalankan `build_aset.py`, HP siswa tidak mendapat versi baru |
| M9 | Beberapa fitur P0/US hanya sebagian atau belum ada: representasi ganda terhubung (F05), kalimat rumpang (US-13), kembali ke soal yang dilewati (US-09), jawaban kalimat konteks (US-21), ketuk istilah (US-19) | Bagian 2.2 | Dokumen PRD/US tidak sesuai dengan kondisi aplikasi |
| M10 | Skala Paas di tahap Refleksi dicatat sebagai `aktivitas: "latihan"`, padahal pertanyaannya mencakup latihan **dan** soal cerita. Kunjungan ulang menambah catatan baru | `modul.js:267` | Interpretasi data beban kognitif perlu hati-hati (rata-rata per modul bisa mencampur beberapa kunjungan) |

### Rendah
| Kode | Masalah | Bukti |
|---|---|---|
| M11 | Membuka aplikasi di dua tab sekaligus bisa saling menimpa data (cache memori per tab) | `storage.js:20` `let cache` |
| M12 | Setiap kali Beranda dibuka, satu pendengar status pemasangan ditambahkan dan tidak pernah dilepas | `beranda.js:55`; `pasang.js:42` |
| M13 | Tes Akhir bisa dikerjakan kapan saja, termasuk sebelum belajar | `beranda.js` (menu Tes Akhir selalu aktif) |
| M14 | Tahap modul tidak dikunci; siswa bisa langsung membuka Kuis tanpa Konsep/Contoh | `modul.js` `halamanModul` |
| M15 | Saat melanjutkan soal cerita setelah muat ulang, sorotan kata di langkah BACA hilang | `literasi.js` (keadaan sorotan tidak disimpan) |
| M16 | Tipe `uraian-singkat` sudah dibuat tetapi tidak dipakai konten; `tahapSiklus: "C"` belum dipakai | Bagian 1.2, 1.3 |
| M17 | Folder `tests/e2e/tangkapan/` berisi 25 tangkapan layar dari uji lama (diabaikan git) | Daftar file |
| M18 | Proyek **belum di-commit**: seluruh folder masih *untracked* di dalam repo mata kuliah Algoritma Pemrograman | `git status`: `?? aplikasi-pola-bilangan/` |

### Ketidaksesuaian dokumentasi dengan kode
| Dokumen | Isi dokumen | Kondisi nyata |
|---|---|---|
| `docs/04` §3 | Skor tes awal 0–2 → M0, 5–6 → M7 | `tes-awal.json`: 0–4 → M2, 5–6 → M4 (M0 dan M7 belum ada) |
| `docs/05` US-18 | Tahap bantuan ditentukan dari posisi modul | Ditentukan field `tahapSiklus` di konten |
| `docs/06` | Lembar bawah, font Nunito/Lexend, warna salah `#DC2626` | Umpan balik di dalam kartu, font sistem, `#b91c1c` |
| `docs/07` §7 | Video di `frontend/media/` | Folder belum ada |
| `docs/09` | Fase 2–4 dan 7 ditandai ✅ | Sesuai untuk kode. Fase 6/6b (konten) memang masih sebagian |
| `docs/01`, `docs/10` | Mencatat nama asli siswa di dokumen wawancara (di luar folder ini) | Tidak bisa diverifikasi dari proyek ini |

---

## Lampiran: Angka Kunci

| Ukuran | Nilai |
|---|---|
| Total baris kode (JS, CSS, Python, termasuk uji) | ±4.120 |
| Ukuran folder `frontend/` | 165 KB (JS 97 KB, CSS 19 KB, konten 35 KB, ikon 9 KB) |
| Aset di cache offline | 26 file |
| Modul tersedia / direncanakan | 2 / 9 |
| Soal dalam konten | 40 soal: per modul 5 latihan + 4 kuis + 4 literasi (× 2 modul = 26), Tes Awal 6, Tes Akhir 8. Ditambah 6 langkah kosong di contoh setengah jadi dan 1 tabel UBAH |
| Pengujian otomatis | 202 (200 lulus, 2 dilewati) |
| Perangkat emulasi | Android 390px, Android 320px, iPhone 13 (WebKit) |
