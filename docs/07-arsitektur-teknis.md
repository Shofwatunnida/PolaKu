# 07 — Arsitektur Teknis

## 1. Keputusan Utama

Kebutuhan: aplikasi **dibuka di browser**, **bisa dipasang tanpa Play Store/App Store**, **bisa offline**, ringan
untuk HP spesifikasi rendah, dan dibangun dengan **Python dan JavaScript**.

| Keputusan | Alasan |
|---|---|
| **PWA (Progressive Web App)** | Satu aplikasi untuk web, Android, iPhone, dan laptop. Dipasang langsung dari browser, tanpa toko aplikasi. Offline lewat service worker |
| **JavaScript murni (ES modules), tanpa framework & tanpa build step** | Ringan (seluruh aplikasi ±100 KB tanpa ikon), mudah dipahami mahasiswa, tidak butuh Node.js, bisa di-hosting statis gratis |
| **Python + Flask untuk server** | Menyajikan aplikasi dengan header PWA yang benar dan, jika diaktifkan, menerima data penelitian |
| **Python untuk alat bantu** | Validasi konten (aturan pedagogis), build cache offline, analisis data (N-gain, skala Paas), pengujian |
| **localStorage** | Progres disimpan di perangkat, tanpa akun (privasi anak). Datanya kecil, jadi cukup |
| **Konten di JSON** | Guru/peneliti menambah modul tanpa mengubah kode |
| **APK opsional lewat PWABuilder** | Jika sekolah ingin file .apk untuk dibagikan langsung (lihat `12-panduan-instalasi-dan-deploy.md`) |

## 2. Arsitektur

```
                 ┌──────────────── Browser siswa (HP / laptop) ────────────────┐
                 │  index.html + js/app.js (router hash: #/peta, #/modul/m2/…) │
                 │   ├─ pages/*      halaman                                   │
                 │   ├─ soal.js, ui.js  komponen                               │
                 │   ├─ answer.js, pattern.js  logika murni (diuji dari Python)│
                 │   └─ storage.js → localStorage (progres & data belajar)     │
                 │  sw.js (service worker) → cache semua aset → OFFLINE        │
                 └──────────────────────┬──────────────────────────────────────┘
                                        │ HTTPS
          ┌─────────────────────────────┴────────────────────────────┐
          │ Pilihan A: hosting statis (GitHub Pages/Netlify)          │
          │            hanya folder frontend/                         │
          │ Pilihan B: server/app.py (Flask)                          │
          │            + /api/status, /api/penelitian (opsional)      │
          │            → data/penelitian/*.json                       │
          └──────────────────────────────────────────────────────────┘

Alat Python (di komputer peneliti):
  tools/validasi_konten.py → cek konten   tools/build_aset.py → versi cache offline
  tools/analisis_data.py   → CSV + N-gain tools/buat_ikon.py  → ikon PNG/SVG
```

## 3. Struktur Folder

```
aplikasi-pola-bilangan/
├─ frontend/
│  ├─ index.html, manifest.webmanifest, sw.js
│  ├─ css/style.css
│  ├─ icons/                       # icon-192/512, maskable, svg (dibuat tools/buat_ikon.py)
│  ├─ js/
│  │  ├─ app.js                    # router, navigasi, status offline, daftar service worker
│  │  ├─ answer.js                 # pemeriksa jawaban (tanpa DOM)
│  │  ├─ pattern.js                # selisih, deteksi pola, banyak noktah (tanpa DOM)
│  │  ├─ storage.js                # localStorage
│  │  ├─ ui.js                     # BarisanPola+lompatan, GambarNoktah, Petunjuk, UmpanBalik,
│  │  │                            # CekAturanmu, PapanRumus, SkalaPaas, GambarKursi
│  │  ├─ soal.js                   # soal interaktif (8 tipe)
│  │  ├─ konten.js, pasang.js
│  │  └─ pages/                    # beranda, modul, literasi, tes, progres, tentang
│  └─ konten/                      # modul.json, m2.json, m4.json, tes-awal.json, tes-akhir.json
├─ server/app.py
├─ tools/                          # validasi_konten, build_aset, analisis_data, buat_ikon
├─ tests/                          # pytest + e2e (Playwright)
└─ requirements.txt
```

## 4. Model Konten (JSON)

Contoh lengkap: `frontend/konten/m2.json`. Ringkasan strukturnya:

```js
Modul = {
  id, kode, judul, tujuan: [string],
  segmen: [{ id, judul, video?: { judul, src, subtitle? }, visual?: Visual, teks: [string] }],  // ≤ 3 kalimat
  contohLengkap: [{ id, soal, visual?, langkah: [{ label, teks, visual? }] }],
  contohSetengahJadi: [{ id, soal, visual?, langkah: [{ label, teks, kosong?: { tipe, label, jawaban, petunjuk, penjelasan } }] }],
  latihan: [Soal],
  literasi: [Stimulus],
  refleksi: { pertanyaan, kalimatAwal, contohPenjelasan },
  kuis: [Soal]
}

Visual = { jenis: "barisan", pola, tampilkanSelisih?, tingkatDua?, tanya? }
       | { jenis: "noktah", bentuk: "persegi"|"persegi-panjang"|"segitiga"|"ganjil"|"genap", banyak }
       | { jenis: "tabel", kolom, baris } | { jenis: "kursi", baris }

Soal = {
  id, tipe, pertanyaan, pola?, visual?, satuan?,
  petunjuk: [3 string],                         // wajib untuk latihan & literasi
  umpanBalik?: [{ jawaban, pesan, toleransi? }], // miskonsepsi umum
  umpanBalikUmum, pembahasan?,
  // per tipe:
  jawaban            // isian-angka (angka), isian-rumus ("3n+1"), pilihan-ganda (indeks)
  pilihan            // pilihan-ganda
  pernyataan: [{ teks, benar, penjelasan }]      // pg-kompleks
  pasangan: [{ kiri, jawaban }], kanan           // menjodohkan
  tabel: { kolom, baris (null = kosong) }, kunciTabel   // lengkapi-tabel
  tokoh, klaim, klaimBenar, alasan: { pilihan, benar }  // klaim (Setuju atau Tidak?)
}
tipe ∈ isian-angka | isian-rumus | pilihan-ganda | pg-kompleks | menjodohkan | lengkapi-tabel | klaim | uraian-singkat

Stimulus = {
  id, judul, konteks: "personal"|"sosial-budaya"|"saintifik", tahapSiklus: "A"|"B"|"C",
  teks, visual?, glosarium?: [{ istilah, arti }],
  infoPenting: [string], ditanya,                // untuk langkah BACA (sorot & Diketahui–Ditanya)
  ubah?: { pertanyaan, tabel, kunciTabel, petunjuk, umpanBalikUmum },   // langkah UBAH (tahap A)
  soal: [Soal & { level: "L1"|"L2"|"L3", proses: ["LM1".."LM7"],
                  pertanyaanCekCerita?: [{ tanya, pilihan, jawaban, penjelasan, penjelasanSalah }] }]
}
```

Aturan isi divalidasi oleh `tools/validasi_konten.py` (lihat CLAUDE.md bagian 5).

## 5. Data di Perangkat (localStorage, kunci `polaku:v1`)

| Bagian | Isi | Dipakai untuk |
|---|---|---|
| `profil` | kodeSiswa (opsional, mis. S01), dibuatPada | Identitas penelitian tanpa nama |
| `progres` | per modul: status, tahap terakhir, tahap selesai | Peta materi, "Lanjutkan belajar" |
| `percobaan` | soalId, mode, jawaban, benar, percobaanKe, jumlahPetunjuk, cekAturanDipakai, waktuMs | Analisis latihan & penggunaan petunjuk |
| `literasi` | stimulusId, langkah (baca/ubah/hitung/cek), level, proses, benar, benarPertama, sorotan, ditanya | Profil Literasi, analisis per indikator LM |
| `skalaBeban` | modulId, aktivitas (latihan/kuis), skor 1–9 | Beban kognitif (Paas) |
| `refleksi` | modulId, teks | Analisis kualitatif self-explanation |
| `tes` | jenis (awal/akhir), skor, maks, jawaban per butir, rekomendasi | Pretest–posttest |

## 6. Pemeriksa Jawaban (`answer.js`)

- **Angka:** menerima "31", "31 kursi", "Rp35.000" (ribuan gaya Indonesia), "10,33" dan "10.5". Umpan balik bisa punya `toleransi`.
- **Rumus:** normalisasi (`×`/`x` → kali, `²` → pangkat 2, awalan "Uₙ =" dibuang), perkalian implisit (`3n`, `n(n+1)`),
  lalu di-parse dengan parser recursive-descent (tanpa `eval`). Dua rumus dianggap sama jika hasilnya sama untuk n = 1..10.
- **Cek Aturanmu** memakai fungsi yang sama untuk membandingkan rumus siswa dengan suku yang diketahui.

## 7. PWA dan Offline

- `manifest.webmanifest`: nama, ikon 192/512 + maskable, `display: standalone`, warna tema.
- `sw.js`: memasang cache berisi semua aset (daftar dibuat otomatis oleh `tools/build_aset.py`, dengan versi = hash isi file).
  Navigasi: jaringan dulu lalu cache; aset: cache dulu. `/api/*` selalu lewat jaringan.
- Tombol pasang: event `beforeinstallprompt` (Android/Chrome/Edge), petunjuk "Tambahkan ke Layar Utama" untuk iOS.
- Video (jika ditambahkan) disimpan di `frontend/media/` sebagai MP4 720p < 5 MB + subtitle `.vtt`, lalu ikut di-cache.

## 8. Keamanan & Privasi Server

- Header: Content-Security-Policy ketat (hanya sumber sendiri), `nosniff`, `no-referrer`, kamera/mikrofon/lokasi dimatikan.
- `/api/penelitian` **nonaktif secara bawaan**, aktif hanya dengan `POLAKU_PENELITIAN=1`. Kode siswa divalidasi
  (`^[A-Z0-9-]{1,12}$`). Hanya bagian data belajar yang disimpan. Batas ukuran 2 MB.
- Folder `data/` ada di `.gitignore`, jadi data siswa tidak ikut ter-commit.

## 9. Kualitas

`python -m pytest` menjalankan:
- `test_js_logic.py`: pemeriksa jawaban & mesin pola (JS dijalankan di V8 lewat mini-racer), serta **setiap kunci jawaban di konten dinilai benar** dan setiap umpan balik miskonsepsi terpicu.
- `test_konten.py`: validator konten dan evaluator rumus yang aman.
- `test_server.py`: halaman, manifest, ikon, service worker, keamanan path, endpoint penelitian.
- `test_analisis.py`: N-gain dan CSV.
- `tests/e2e/test_alur.py`: di Microsoft Edge (layar HP 390 px): syarat installable, offline, tes awal, alur lengkap M2, M4, hapus data.
