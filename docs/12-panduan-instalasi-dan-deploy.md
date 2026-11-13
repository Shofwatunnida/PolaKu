# 12 — Panduan Instalasi, Menjalankan, dan Deploy

PolaKu adalah **Progressive Web App (PWA)**. Artinya:
- dibuka di **browser** (HP, tablet, laptop) seperti situs biasa,
- bisa **dipasang** ke layar utama HP/laptop **tanpa Play Store atau App Store**,
- setelah dibuka sekali, bisa dipakai **tanpa internet**.

## 1. Menjalankan di Komputer Sendiri (pengembangan)

Butuh Python 3.10+.

```bash
cd aplikasi-pola-bilangan
python -m venv .venv
.venv\Scripts\activate          # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
python server/app.py
```

Buka **http://localhost:5000**.

### Mencoba dari HP di Wi-Fi yang sama
```bash
python server/app.py --host 0.0.0.0
```
Server akan menampilkan alamatnya, misalnya `Buka dari HP (Wi-Fi yang sama): http://192.168.1.5:5000`.
Buka alamat itu di HP. Semua materi bisa dipakai, tetapi **tombol pasang dan mode offline tidak aktif**,
karena browser mewajibkan HTTPS (kecuali `localhost`). Aplikasi menampilkan pemberitahuan kecil tentang ini di beranda.

### Mencoba pasang & offline di HP Android sungguhan (tanpa deploy)
Trik *port forwarding* lewat kabel USB membuat HP menganggap aplikasi berjalan di `localhost`,
sehingga pemasangan dan mode offline bisa diuji:

1. Di HP: aktifkan **Opsi pengembang** (ketuk *Nomor versi* 7 kali di Setelan → Tentang ponsel), lalu nyalakan **Debugging USB**.
2. Sambungkan HP ke laptop dengan kabel USB, izinkan debugging di HP.
3. Di laptop jalankan `python server/app.py`, lalu buka `chrome://inspect/#devices` (Chrome) atau `edge://inspect/#devices` (Edge).
4. Klik **Port forwarding…**, isi `5000` → `localhost:5000`, centang *Enable port forwarding*.
5. Di Chrome HP, buka **http://localhost:5000**. Tombol **📲 Pasang Aplikasi** akan muncul.
6. Pasang, lalu nyalakan mode pesawat dan buka PolaKu dari layar utama untuk menguji mode offline.

Untuk iPhone, cara termudah adalah deploy ke hosting HTTPS (bagian 3), lalu buka di Safari.

## 2. Cara Siswa Memasang Aplikasi (tanpa toko aplikasi)

| Perangkat | Langkah |
|---|---|
| **Android (Chrome)** | Buka alamat aplikasi → ketuk tombol **📲 Pasang Aplikasi** di beranda, atau menu ⋮ → **Instal aplikasi / Tambahkan ke layar utama** |
| **iPhone/iPad (Safari)** | Buka alamat aplikasi di Safari → tombol **Bagikan** → **Tambahkan ke Layar Utama** |
| **Laptop (Chrome/Edge)** | Ikon pasang (⊕) di ujung kanan kolom alamat |

Setelah terpasang, ikon PolaKu muncul di layar utama dan aplikasi terbuka tanpa bilah alamat. Bagikan
alamat aplikasi ke siswa lewat WhatsApp atau kode QR.

## 3. Deploy (agar bisa diakses semua siswa lewat HTTPS)

### Pilihan A: Hosting statis gratis (paling mudah, disarankan)
Aplikasi siswa **tidak membutuhkan server Python**. Folder `frontend/` bisa langsung di-hosting.

1. Jalankan validasi dan perbarui daftar aset offline:
   ```bash
   python tools/validasi_konten.py
   python tools/build_aset.py
   ```
2. Unggah **isi folder `frontend/`** ke salah satu:
   - **GitHub Pages**: buat repo, unggah isi `frontend/`, aktifkan *Settings → Pages*.
   - **Netlify**: seret folder `frontend/` ke app.netlify.com/drop.
   - **Cloudflare Pages / Vercel**: hubungkan repo, folder keluaran = `frontend`.
3. Bagikan alamat HTTPS-nya ke siswa.

Pada pilihan ini, tombol "Kirim ke peneliti" tidak muncul (tidak ada server). Data dikumpulkan lewat
tombol **Unduh data** di halaman Tentang.

### Pilihan B: Server Python (jika ingin menerima data penelitian otomatis)
Deploy `server/app.py` ke hosting Python yang menyediakan HTTPS, misalnya **PythonAnywhere** atau **Render**.

- Perintah start: `python server/app.py --host 0.0.0.0` (port mengikuti variabel `PORT`).
- Aktifkan penerimaan data: set variabel lingkungan `POLAKU_PENELITIAN=1`.
- Data masuk ke folder `data/penelitian/` sebagai file JSON per siswa (hanya kode siswa, tanpa nama).
- Matikan lagi (`POLAKU_PENELITIAN=0`) setelah pengambilan data selesai.

## 4. (Opsional) Membuat File APK Android

Jika sekolah ingin file `.apk` yang bisa dibagikan langsung (sideload):
1. Deploy aplikasi dulu (bagian 3) sehingga punya alamat HTTPS.
2. Buka **pwabuilder.com**, masukkan alamat aplikasi, pilih **Android → Download**.
3. Hasilnya file APK yang membungkus PWA (Trusted Web Activity). Bagikan lewat WhatsApp/Drive.
4. Di HP siswa, izinkan *Instal dari sumber tidak dikenal* untuk memasang APK.

Cara ini tetap **tidak melalui Play Store**. Untuk sebagian besar kebutuhan, pemasangan PWA di bagian 2
sudah cukup dan lebih sederhana.

## 5. Fitur Khusus Smartphone

| Fitur | Manfaat |
|---|---|
| Papan rumus berisi angka, n, ², ×, ÷ (keyboard HP tidak muncul) | Simbol matematika sulit diketik di keyboard HP. Tombol ⌨️ mengembalikan keyboard bila perlu |
| Melanjutkan dari posisi terakhir | HP sering menutup tab di latar belakang (saat siswa membuka WhatsApp/menerima telepon). Siswa kembali ke soal yang sama, termasuk di tengah tes |
| Navigasi bawah disembunyikan saat mengetik | Kotak isian dan tombol tidak tertutup |
| Tombol Enter/"Selesai" di keyboard | Mengirim jawaban atau pindah ke kotak berikutnya |
| Tabel lebar diputar menjadi vertikal | Tidak perlu menggeser ke samping di layar 320 px |
| Skala usaha mental berupa daftar | Mudah diketuk, makna setiap angka jelas |
| Tombol "📲 Bagikan data" | Siswa langsung mengirim file data ke peneliti lewat WhatsApp/Drive |
| Pemberitahuan versi baru | Aplikasi terpasang mengecek pembaruan setiap dibuka kembali, lalu menawarkan muat ulang |
| Penyimpanan permanen (setelah dipasang) | Progres tidak dihapus browser saat memori HP penuh |

Semua fitur ini diuji otomatis di tiga perangkat: Android 390 px, Android kecil 320 px, dan iPhone (mesin WebKit/Safari),
lewat `tests/e2e/test_ponsel.py` dan `tests/e2e/test_alur.py`.

## 6. Memperbarui Aplikasi

Setiap kali mengubah file di `frontend/`:
```bash
python tools/validasi_konten.py   # pastikan konten mematuhi aturan
python -m pytest                  # pastikan tidak ada yang rusak
python tools/build_aset.py        # perbarui versi cache offline
```
Lalu unggah ulang. HP siswa akan mengambil versi baru saat online berikutnya.

## 7. Mengolah Data Penelitian

```bash
python tools/analisis_data.py data/penelitian        # dari server
python tools/analisis_data.py folder-unduhan-siswa   # file .json (Unduh) atau .txt (Bagikan dari HP)
```
Hasil CSV (bisa dibuka di Excel/SPSS) ada di folder `hasil-analisis/`. Lihat `docs/08-rencana-pengujian.md`.
