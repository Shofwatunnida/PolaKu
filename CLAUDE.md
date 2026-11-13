# CLAUDE.md

Panduan untuk Claude Code (dan AI assistant lain) saat mengerjakan proyek ini. Baca file ini dulu sebelum mengubah kode.

## 1. Ringkasan Proyek

**PolaKu** adalah aplikasi belajar materi **Pola Bilangan** untuk siswa SMP **Kelas VII** (keputusan 13 November 2026; responden wawancara studi pendahuluan adalah siswa kelas VIII). Aplikasi dibuka di browser dan bisa dipasang di HP/laptop sebagai PWA tanpa Play Store/App Store. Tujuan utamanya adalah **menurunkan beban kognitif ekstrinsik**, **mengelola beban intrinsik**, dan **mendorong beban germane** siswa, sesuai temuan wawancara (lihat `docs/01-analisis-kebutuhan.md`).

Tujuan kedua adalah **menumbuhkembangkan literasi matematika**: kemampuan merumuskan, menggunakan, dan menafsirkan pola bilangan dalam konteks nyata, serta bernalar tentangnya (kerangka PISA 2022 dan AKM Numerasi). Lihat `docs/11-literasi-matematika.md`.

Pemilik proyek: mahasiswa S1 Pendidikan Matematika. Aplikasi ini juga menjadi produk penelitian/tugas akademik, jadi **setiap fitur harus bisa dijelaskan alasan pedagogisnya**.

## 2. Tech Stack

Bahasa yang dipakai: **JavaScript** (aplikasi) dan **Python** (server & alat bantu). Tidak ada build step dan tidak butuh Node.js.

- **Frontend:** HTML + CSS + JavaScript murni (ES modules), tanpa framework. Router berbasis hash (`#/peta`).
- **PWA:** `manifest.webmanifest` + `sw.js` (service worker, cache semua aset → offline). Dipasang tanpa Play Store/App Store.
- **Penyimpanan:** `localStorage` di perangkat (modul `js/storage.js`).
- **Server:** Python + Flask (`server/app.py`): menyajikan frontend, header PWA/keamanan, endpoint data penelitian opsional.
- **Alat Python (`tools/`):** validasi konten, build daftar aset offline, analisis data penelitian, pembuat ikon.
- **Pengujian:** pytest. Logika JS diuji dari Python lewat `mini-racer` (V8). Uji E2E di browser memakai Playwright (Python) + Microsoft Edge.
- **APK (opsional):** dibuat dari alamat PWA lewat PWABuilder (lihat `docs/12`).

Jangan menambah framework/pustaka besar tanpa alasan yang jelas. Siswa sering memakai HP spesifikasi rendah dan kuota terbatas.
Frontend harus tetap bisa di-hosting statis (tanpa server Python); fitur yang butuh server harus opsional.

## 3. Perintah

```bash
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
python server/app.py                  # http://localhost:5000  (--host 0.0.0.0 untuk akses dari HP di Wi-Fi yang sama)
python tools/validasi_konten.py       # WAJIB setelah mengubah konten (juga cek duplikat & tumpang tindih dengan Tes Awal/Akhir)
python tools/buat_kunci_rubrik.py     # WAJIB setelah mengubah konten: perbarui docs/13
python tools/build_aset.py            # perbarui cache offline (otomatis saat server start)
python -m pytest                      # semua uji (unit + konten + server + analisis + E2E)
python -m pytest --ignore=tests/e2e   # tanpa uji browser
python tools/analisis_data.py data/penelitian
```

## 4. Struktur Folder

```
frontend/
  index.html, manifest.webmanifest, sw.js   # sw.js: blok ASET dibuat otomatis, jangan edit manual
  css/style.css
  js/
    app.js        # router, navigasi, status offline, registrasi service worker
    answer.js     # pemeriksa jawaban (angka, rumus, tiap tipe soal) — MURNI, tanpa DOM
    pattern.js    # selisih, deteksi pola, banyak noktah — MURNI, tanpa DOM
    storage.js    # localStorage: progres, percobaan, literasi, skala Paas, refleksi, tes
    ui.js         # komponen: barisan + panah lompatan, noktah SVG, petunjuk, umpan balik, Cek Aturanmu, skala Paas
    soal.js       # komponen soal interaktif untuk semua tipe soal
    konten.js     # pemuat JSON + daftar tahap modul
    pasang.js     # tombol pasang PWA (Android) & petunjuk iOS
    pages/        # beranda, modul (peta + tahap), literasi, tes, progres, tentang
  konten/         # modul.json, m2.json, m4.json, tes-awal.json, tes-akhir.json
  icons/
server/app.py
tools/            # validasi_konten.py, build_aset.py, analisis_data.py, buat_ikon.py
tests/            # test_js_logic.py, test_konten.py, test_server.py, test_analisis.py, e2e/
docs/
```

**Kolom konten khusus:** `"cekAturan": false` mematikan alat Cek Aturanmu pada soal (mis. Fibonacci, yang tidak punya rumus
suku ke-n sederhana). `"verifikasiPola": {"satuan": [...], "ke": n}` atau `{"satuan": [...], "hitung": "x", "dari": n}` pada soal
pola berulang membuat validator menghitung ulang kunci dan memeriksa bahwa visual `bentuk` benar-benar mengulang satuan itu.
Visual `{"jenis": "bentuk", "deret": ["lingkaran-pink", …], "tanya": 1}` menampilkan deret bentuk bernomor.

**Menambah modul baru:** buat `frontend/konten/mX.json` dengan struktur seperti `m2.json`, set `"tersedia": true` di
`modul.json`, jalankan `python tools/validasi_konten.py` dan `python -m pytest`. Tidak perlu mengubah kode JS.

## 5. Aturan Pedagogis (WAJIB dipatuhi setiap mengubah UI/konten)

Aturan ini diturunkan dari Teori Beban Kognitif dan temuan wawancara. Kalau ada permintaan yang bertentangan, ingatkan pemilik proyek dulu.

1. **Satu konsep per layar** (prinsip *segmenting*). Jangan menumpuk beberapa konsep dalam satu tampilan.
2. **Teks singkat.** Maksimal ±3 kalimat per blok penjelasan. Kalimat pendek, bahasa Indonesia yang sederhana dan sesuai usia 13–14 tahun.
3. **Tidak ada elemen dekoratif yang mengganggu** (prinsip *coherence*): tanpa animasi latar, musik latar, atau gambar yang tidak berkaitan dengan konsep.
4. **Gambar dan penjelasannya diletakkan berdekatan** (prinsip *spatial contiguity*). Jangan pisahkan diagram pola dari keterangannya.
5. **Video pendek, 1–3 menit per konsep**, dengan narasi (prinsip *modality*), dan siswa bisa menjeda/mengulang. Video tidak boleh diputar otomatis.
6. **Urutan wajib:** contoh lengkap (*worked example*) → contoh setengah jadi (*faded example*) → latihan mandiri. Jangan langsung memberi latihan tanpa contoh.
7. **Petunjuk bertingkat (hint)** di setiap soal latihan, minimal 3 tingkat: (a) arahkan perhatian, (b) beri langkah, (c) tunjukkan hampir seluruh penyelesaian. Siswa tidak boleh "buntu" lalu menyerah (temuan GL03).
8. **Visualisasi selisih antarsuku** wajib ada di soal pola: tampilkan "lompatan" (+3, +3, …) di antara suku (temuan IL01, IL02).
9. **Fitur cek ulang:** sebelum mengirim jawaban, siswa diajak memeriksa aturan polanya ke suku yang sudah diketahui (temuan GL02).
10. **Umpan balik harus menjelaskan**, tidak hanya "Benar/Salah". Untuk jawaban salah, jelaskan di mana letak kekeliruannya.
11. **Tidak ada batas waktu yang menekan** dan tidak ada papan peringkat kompetitif di MVP.

**Aturan literasi matematika:**

12. **Setiap modul ditutup dengan soal literasi kontekstual**, ditempatkan *setelah* latihan murni, tidak sebelumnya.
13. **Soal literasi memakai siklus tetap BACA → UBAH → HITUNG → CEK CERITA**, dengan bantuan yang dikurangi bertahap (tahap A → B → C).
14. **Satu stimulus untuk 3–4 soal berjenjang (L1 → L3).** Teks stimulus ≤ 60 kata untuk level awal dan ≤ 120 kata untuk level penalaran. Angka penting juga ditampilkan dalam gambar/tabel.
15. **Konteks dekat dengan siswa Indonesia** (sekolah, desa, warung, batik, tabungan). Hindari konteks asing yang menambah beban.
16. **Setiap soal literasi diberi label** proses (LM1–LM7) dan level (L1–L3) di file konten.
17. **Minimal satu soal penalaran per modul** (menilai klaim, memberi alasan, atau membuat keputusan).

**Aturan smartphone** (diuji di `tests/e2e/test_ponsel.py` pada Android 390px, Android 320px, iPhone/WebKit):

18. **Tidak boleh ada geser ke samping** pada lebar 320 px. Tabel lebar memakai `tabelResponsif()` (otomatis vertikal).
19. **Target sentuh ≥ 44 × 44 px** (kata yang bisa diketuk di stimulus ≥ 28 px).
20. **Jangan mengubah tata letak saat fokus berpindah** (mis. padding saat keyboard muncul): ketukan bisa meleset. Navigasi bawah hanya disembunyikan dengan `visibility`, dan dimunculkan kembali setelah jari diangkat.
21. **Isian rumus memakai `papanRumus()`**, jangan mengandalkan keyboard HP untuk simbol matematika.
22. **Tahap yang berisi beberapa langkah menyimpan posisinya** (`simpanPosisi`) agar siswa bisa melanjutkan setelah tab ditutup HP.
23. Jangan memunculkan keyboard HP secara otomatis (`focus()`) pada layar sentuh; cek dengan `layarSentuh()`.

**Aturan tema visual "Pastel Math Wonderland"** (diuji di `tests/test_ilustrasi.py` dan `tests/e2e/test_tema.py`):

24. **Ilustrasi pola harus benar secara matematis.** Buat/ubah lewat `tools/buat_ilustrasi.py` (noktah dihitung kode, diberi `data-pola`/`data-suku`), jangan menggambar noktah manual. Mata karakter berupa garis lengkung agar tidak terhitung sebagai noktah.
25. **Ornamen hanya di lapisan `.latar-hias`** (z-index negatif, `pointer-events: none`, `aria-hidden`), tampil utuh (tidak terpotong), di HP hanya di sudut bawah dengan opacity ≤ 0,4, di laptop hanya di margin luar kolom 680px.
26. **Teks selalu di atas permukaan buram** (kartu putih/pastel muda) dengan kontras WCAG AA. Jangan memakai `opacity` pada kartu berisi teks.
27. Warna semantik soal tidak boleh diubah: oranye = lompatan, ungu = suku yang dicari, hijau/merah = umpan balik. `--aksen` tiap tahap harus ≥ 4,5 : 1 terhadap teks putih.
28. Animasi hanya untuk umpan balik/sentuhan (≤ 220 ms) dan otomatis mati dengan `prefers-reduced-motion`.

## 6. Konvensi Kode

- JavaScript modern (ES modules, `const`/`let`, arrow function). Tanpa framework dan tanpa build step.
- Nama variabel/fungsi dalam bahasa Indonesia, `camelCase` (JS) dan `snake_case` (Python), mengikuti kode yang ada.
- Logika murni (pemeriksa jawaban, mesin pola) dipisah dari DOM (`answer.js`, `pattern.js`) agar bisa diuji dari pytest.
- Teks siswa ditampilkan lewat `textContent`/`h()`; `innerHTML` hanya untuk teks konten kita sendiri lewat `teksKaya()` yang meng-escape HTML.
- Jangan pakai `eval()` atau `new Function()` di frontend. Rumus di-parse dengan parser di `answer.js`.
- **Semua teks UI berbahasa Indonesia** dengan kalimat pendek yang mudah dipahami siswa kelas VII. Teks materi & soal disimpan di `frontend/konten/*.json`, bukan di kode.
- Konten divalidasi oleh `tools/validasi_konten.py` (struktur + aturan pedagogis). Uji `test_kunci_konten_dinilai_benar` memastikan setiap kunci jawaban dinilai benar oleh pemeriksa JS.
- Python: type hints, fungsi kecil, docstring berbahasa Indonesia.
- Pemeriksa jawaban harus menerima variasi penulisan yang setara (mis. `2n+1`, `2n + 1`, `1+2n`). Buat unit test untuk setiap pola.
- Mobile-first: rancang untuk lebar 360px, lalu sesuaikan ke layar lebar.
- Target sentuh minimal 44×44 px. Kontras teks memenuhi WCAG AA.
- Commit message berbahasa Indonesia, format: `feat: ...`, `fix: ...`, `docs: ...`, `refactor: ...`, `test: ...`.

## 7. Privasi

Pengguna adalah anak di bawah umur. Di MVP:
- **Tidak ada login, tidak ada pengumpulan data pribadi.** Progres hanya disimpan di perangkat (localStorage `polaku:v1`).
- **Nama panggilan** (halaman sambutan) disimpan di kunci TERPISAH `polaku:nama` lewat `js/nama.js`, hanya untuk sapaan.
  Jangan pernah memasukkan nama ke `polaku:v1`/`storage.js`, karena isi `polaku:v1` diekspor (Unduh/Bagikan) dan dikirim ke server penelitian.
  Uji `test_nama_tidak_ikut_data_penelitian` menjaga aturan ini. "Hapus semua data" juga menghapus nama.
- Jangan menambahkan analytics pihak ketiga, iklan, atau SDK pelacak.
- Jangan menulis nama asli siswa responden di kode, konten, atau dokumen. Gunakan kode (S01, S02, …).
- Detail lengkap: `docs/10-etika-dan-privasi.md`.

## 8. Definisi Selesai (Definition of Done)

Sebuah fitur dianggap selesai jika:
- [ ] Memenuhi kriteria penerimaan di `docs/05-user-stories.md`
- [ ] Mematuhi aturan pedagogis di bagian 5
- [ ] Berjalan di Chrome Android (layar 360px) dan browser desktop
- [ ] Bisa dipakai offline (setelah kunjungan pertama)
- [ ] `python tools/validasi_konten.py` dan `python -m pytest` lulus
- [ ] Teks sudah diperiksa ejaannya (PUEBI)

## 9. Referensi Dokumen

Kebutuhan → `docs/02-PRD.md` · Pedagogi → `docs/03-desain-pembelajaran.md` · Literasi → `docs/11-literasi-matematika.md` · Konten → `docs/04-konten-materi.md` · UI → `docs/06-desain-ui-ux.md` · Teknis → `docs/07-arsitektur-teknis.md`
