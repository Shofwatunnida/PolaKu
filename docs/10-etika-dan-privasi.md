# 10 — Etika Penelitian dan Privasi Data

Pengguna aplikasi adalah **anak di bawah umur** (13–14 tahun), jadi perlindungan data menjadi prioritas. Di Indonesia, acuannya adalah **UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi**, yang mewajibkan persetujuan orang tua/wali untuk pemrosesan data pribadi anak.

## 1. Prinsip di Aplikasi (MVP)

| Prinsip | Penerapan |
|---|---|
| Minimisasi data | Tidak meminta email, nomor HP, foto, atau lokasi. Nama panggilan diminta hanya untuk sapaan, disimpan terpisah di perangkat (`polaku:nama`), dan **tidak pernah** ikut diekspor atau dikirim ke server |
| Data di perangkat | Progres disimpan di IndexedDB perangkat, tidak dikirim ke server |
| Tanpa pelacak | Tanpa iklan, tanpa analytics pihak ketiga, tanpa SDK media sosial |
| Kode, bukan nama | Untuk penelitian, peneliti mengisi kode siswa (S01, S02, …) di perangkat |
| Transparansi | Halaman "Tentang" menjelaskan data apa yang disimpan dan cara menghapusnya |
| Kendali pengguna | Tombol "Hapus semua data saya" |

## 2. Etika Penelitian

- [ ] Surat izin dari kampus dan sekolah
- [ ] Lembar persetujuan orang tua/wali (*informed consent*) dan persetujuan siswa (*assent*)
- [ ] Penjelasan bahwa partisipasi sukarela dan boleh berhenti kapan saja
- [ ] Identitas disamarkan di semua dokumen, laporan, dan tangkapan layar
- [ ] Rekaman/foto wawancara: wajah siswa diburamkan bila dipublikasikan, atau minta izin tertulis
- [ ] Data mentah disimpan aman dan hanya diakses peneliti/pembimbing

## 3. Catatan untuk Dokumen Wawancara yang Ada

- Nama asli siswa masih muncul di baris GL01 dan Kesimpulan Sementara. Ganti dengan **S01**.
- Dokumentasi tangkapan layar Google Meet menampilkan wajah siswa. Jika laporan akan dipublikasikan atau diunggah, **buramkan wajah** atau pastikan sudah ada izin.

## 4. Jika Nanti Memakai Backend (Fase 2)

- Pilih server yang mematuhi standar keamanan (Supabase/Firebase dengan Row Level Security).
- Akun dibuat oleh guru (kode kelas), bukan pendaftaran mandiri oleh siswa.
- Buat kebijakan privasi tertulis (wajib untuk Google Play kategori anak/*Families Policy*).
- Enkripsi koneksi (HTTPS) dan batasi akses data per kelas.
