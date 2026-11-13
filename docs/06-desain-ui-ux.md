# 06 — Desain UI/UX

## 1. Prinsip Visual

| Prinsip | Ketentuan |
|---|---|
| Tenang dan bersih | Latar putih/krem lembut, tanpa pola latar, tanpa animasi dekoratif |
| Fokus | Satu area utama per layar; tombol aksi utama di bawah (mudah dijangkau jempol) |
| Konsisten | Posisi tombol "Kembali", "Petunjuk", "Lanjut" selalu sama di setiap layar |
| Isyarat (signaling) | Satu warna aksen khusus untuk selisih/lompatan, satu warna untuk suku yang dicari |
| Ramah HP | Desain untuk lebar 360 px dulu; layout satu kolom |

## 2. Palet dan Tipografi (usulan awal)

| Token | Warna | Penggunaan |
|---|---|---|
| `primary` | Biru `#2563EB` | Tombol utama, tautan |
| `accent-selisih` | Oranye `#EA580C` | Panah dan label lompatan antarsuku |
| `accent-target` | Ungu `#7C3AED` | Suku yang ditanyakan (kotak "?") |
| `success` | Hijau `#16A34A` | Jawaban benar, ✓ |
| `error-soft` | Merah lembut `#DC2626` | Jawaban perlu diperbaiki (dengan ikon, tidak hanya warna) |
| `bg` | `#FAFAF7` | Latar |
| `text` | `#1F2937` | Teks utama |

- Font: **Nunito** atau **Lexend** (mudah dibaca), ukuran dasar 16–18 px, angka besar 24–32 px pada barisan pola.
- Notasi matematika memakai KaTeX.
- Jangan membedakan informasi **hanya** dengan warna (pertimbangkan siswa buta warna).
- Sediakan mode gelap (opsional, P2).

## 3. Peta Layar

```
Splash
  └─ Beranda
       ├─ Tes Awal ──→ Hasil & Rekomendasi
       ├─ Peta Materi (M0–M8)
       │     └─ Modul
       │          ├─ Konsep (video + visual + teks)  [segmen 1..n]
       │          ├─ Contoh Lengkap
       │          ├─ Contoh Setengah Jadi
       │          ├─ Latihan  ── Petunjuk · Cek Aturanmu · Umpan balik
       │          ├─ Refleksi + Skala usaha mental
       │          └─ Kuis Subtopik → Ringkasan hasil
       ├─ Progres Saya
       └─ Tentang (panduan, kredit, ekspor data peneliti)
```

## 4. Wireframe Teks

### Beranda
```
┌──────────────────────────────┐
│ PolaKu                    ⓘ  │
│                              │
│  Halo! Ayo belajar pola.     │
│                              │
│  ┌────────────────────────┐  │
│  │ ▶ Lanjutkan belajar    │  │
│  │   M2 · Selisih Tetap   │  │
│  └────────────────────────┘  │
│                              │
│  [ Peta Materi ]             │
│  [ Progres Saya ]            │
│  [ Tes Awal ]                │
└──────────────────────────────┘
```

### Layar Konsep (segmen)
```
┌──────────────────────────────┐
│ ← M2 · Selisih Tetap   2/5   │
│ ┌──────────────────────────┐ │
│ │      ▶  video 1:45       │ │
│ └──────────────────────────┘ │
│                              │
│   3    6    9    12   ?      │
│    ╰+3╯╰+3╯╰+3╯╰+3╯          │
│                              │
│ Setiap suku bertambah 3.     │
│ Lompatan yang sama disebut   │
│ selisih tetap.               │
│                              │
│ [ Kembali ]     [ Lanjut → ] │
└──────────────────────────────┘
```

### Layar Latihan
```
┌──────────────────────────────┐
│ ← Latihan 3/5          💡    │
│ Peta langkah:                │
│ ①Amati ②Lompatan ③Periksa    │
│ ④Rumuskan ⑤Cek ulang         │
│                              │
│ Tentukan suku ke-10:         │
│   4    7    10   13  …       │
│ [Tampilkan lompatan]         │
│                              │
│ Rumus suku ke-n: [ 3n+1   ]  │
│ [ 🔍 Cek Aturanmu ]          │
│  n │ rumusmu │ pola │        │
│  1 │    4    │  4   │ ✓      │
│  2 │    7    │  7   │ ✓      │
│                              │
│ Suku ke-10:      [ 31     ]  │
│                              │
│ [ Butuh petunjuk? ] [Kirim]  │
└──────────────────────────────┘
```

### Umpan Balik (lembar bawah / bottom sheet)
```
┌──────────────────────────────┐
│ ✗ Belum tepat                │
│ Sepertinya kamu menghitung   │
│ suku ke-5. Yang ditanya      │
│ suku ke-10.                  │
│ [ Coba lagi ] [ Petunjuk ]   │
└──────────────────────────────┘
```

### Skala Usaha Mental
```
┌──────────────────────────────┐
│ Seberapa berat kamu berpikir │
│ saat mengerjakan latihan tadi?│
│                              │
│  1  2  3  4  5  6  7  8  9   │
│ sangat              sangat   │
│ ringan               berat   │
│                  [ Simpan ]  │
└──────────────────────────────┘
```

### Layar Soal Literasi (tahap A, langkah BACA)
```
┌──────────────────────────────┐
│ ← Literasi M2 · Soal 1/4     │
│ [BACA]→ UBAH → HITUNG → CEK  │
│ ┌──────────────────────────┐ │
│ │ Kursi Lomba 17 Agustus ▾ │ │
│ │ Baris pertama berisi     │ │
│ │ [12 kursi]. Setiap baris │ │
│ │ bertambah [3 kursi].     │ │
│ │  ▭▭▭▭  ▭▭▭▭▭  ▭▭▭▭▭▭     │ │
│ └──────────────────────────┘ │
│ Ketuk angka yang penting.    │
│                              │
│ Diketahui: 12 kursi, +3      │
│ Ditanya:  [ kursi baris ke-4]│
│                              │
│ [ Butuh petunjuk? ] [Lanjut→]│
└──────────────────────────────┘
```

### Layar Setuju atau Tidak?
```
┌──────────────────────────────┐
│ Andi: "Baris ke-10 berisi    │
│ 42 kursi."                   │
│                              │
│ Kamu:  ( ) Setuju            │
│        (•) Tidak setuju      │
│ Alasannya:                   │
│ ( ) 42 terlalu banyak        │
│ (•) Baris ke-1 belum         │
│     bertambah, jadi          │
│     12 + 9 × 3 = 39          │
│ ( ) Polanya dikali 3         │
│                   [ Kirim ]  │
└──────────────────────────────┘
```

Ketentuan layar literasi:
- Stimulus bisa dilipat (▾) agar soal tetap terlihat di layar HP, tetapi selalu bisa dibuka kembali.
- Sorotan memakai warna latar kuning lembut, berbeda dari warna aksen selisih (oranye).
- Siklus 4 langkah memakai ikon yang sama di semua modul.

## 5. Interaksi dan Animasi

- Animasi hanya bila **menjelaskan konsep** (mis. noktah bertambah dari gambar ke-2 ke gambar ke-3). Durasi ≤ 400 ms, bisa dimatikan (`prefers-reduced-motion`).
- Umpan balik muncul di lembar bawah, tidak berupa pop-up yang menutup soal.
- Keyboard numerik otomatis untuk isian angka (`inputmode="numeric"`).
- Papan ketik khusus sederhana untuk rumus (tombol n, +, −, ×, ², ( )) agar siswa tidak kesulitan mengetik simbol di HP.

## 6. Aksesibilitas

- Kontras teks ≥ 4,5:1
- Target sentuh ≥ 44 × 44 px
- Semua gambar pola punya teks alternatif (mis. "Gambar ke-3: 9 noktah tersusun 3 × 3")
- Video bersubtitle
- Ukuran teks mengikuti pengaturan sistem
