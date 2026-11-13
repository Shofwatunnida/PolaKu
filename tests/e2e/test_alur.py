"""Uji end-to-end: menjalankan aplikasi di browser sungguhan (Edge/Chrome) dengan layar seukuran HP.

Butuh: pip install playwright   (memakai Microsoft Edge yang sudah ada di Windows;
di komputer lain jalankan `playwright install chromium` dan set POLAKU_BROWSER=chromium).
Jalankan: python -m pytest tests/e2e -v
"""
import os
import re
import threading
from pathlib import Path

import pytest

sync_api = pytest.importorskip("playwright.sync_api")
from werkzeug.serving import make_server  # noqa: E402

from server.app import buat_app  # noqa: E402

FOLDER_TANGKAPAN = Path(os.environ.get("POLAKU_TANGKAPAN", Path(__file__).parent / "tangkapan"))


@pytest.fixture(scope="module")
def alamat(tmp_path_factory):
    app = buat_app(penelitian_aktif=True, folder_data=tmp_path_factory.mktemp("data"))
    srv = make_server("127.0.0.1", 0, app)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    yield f"http://127.0.0.1:{srv.server_port}"
    srv.shutdown()


PERANGKAT = {
    # nama: (mesin browser, deskriptor perangkat Playwright)
    "android-390": ("chromium", {"viewport": {"width": 390, "height": 844}, "device_scale_factor": 2, "is_mobile": True, "has_touch": True}),
    "android-kecil-320": ("chromium", "Galaxy S9+"),
    "iphone-webkit": ("webkit", "iPhone 13"),
}


@pytest.fixture(scope="module")
def pw():
    with sync_api.sync_playwright() as p:
        yield p


@pytest.fixture(scope="module")
def peramban(pw):
    terbuka = {}

    def ambil(mesin):
        if mesin not in terbuka:
            if mesin == "webkit":
                try:
                    terbuka[mesin] = pw.webkit.launch()
                except Exception as e:  # noqa: BLE001
                    pytest.skip(f"WebKit belum terpasang (python -m playwright install webkit): {e}")
            else:
                jenis = os.environ.get("POLAKU_BROWSER", "msedge")
                terbuka[mesin] = pw.chromium.launch(channel=None if jenis == "chromium" else jenis)
        return terbuka[mesin]

    yield ambil
    for b in terbuka.values():
        b.close()


@pytest.fixture(params=list(PERANGKAT))
def halaman(request, pw, peramban, alamat):
    mesin, desk = PERANGKAT[request.param]
    opsi = dict(pw.devices[desk]) if isinstance(desk, str) else dict(desk)
    opsi.pop("default_browser_type", None)
    ctx = peramban(mesin).new_context(**opsi, locale="id-ID")
    # Uji alur belajar dimulai dari siswa yang sudah mengisi nama (halaman sambutan diuji di test_sambutan.py).
    # Hanya diisi jika belum ada, sehingga uji "hapus data" tetap bisa memeriksa nama terhapus.
    ctx.add_init_script("try { if (!localStorage.getItem('polaku:nama') && !sessionStorage.getItem('uji:tanpa-nama')) localStorage.setItem('polaku:nama', 'Uji'); } catch (e) {}")
    page = ctx.new_page()
    page.perangkat = request.param
    page.mesin = mesin
    galat = []
    page.on("pageerror", lambda e: galat.append(str(e)))
    page.on("console", lambda m: galat.append(m.text) if m.type == "error" else None)
    page.galat = galat
    page.goto(alamat + "/")
    yield page
    ctx.close()
    assert galat == [], f"Error JavaScript: {galat}"


def foto(page, nama):
    FOLDER_TANGKAPAN.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(FOLDER_TANGKAPAN / f"{getattr(page, 'perangkat', 'x')}-{nama}.png"), full_page=True)


def tombol(page, nama):
    return page.get_by_role("button", name=nama, exact=True)


def kirim_isian(page, nilai):
    page.locator(".soal input.isian").first.fill(str(nilai))
    page.locator(".aksi").get_by_role("button", name=re.compile("^(Kirim|Coba lagi)$")).click()


def lanjut(page):
    page.locator(".aksi").get_by_role("button", name=re.compile("Lanjut|selesai", re.I)).first.click()


def test_beranda_dan_pwa(halaman, alamat):
    page = halaman
    if page.mesin != "chromium":
        pytest.skip("cek installable memakai CDP (khusus Chromium)")
    page.get_by_role("heading", name="PolaKu").wait_for()
    assert page.locator(".nav-bawah a").count() == 4
    # Service worker aktif dan aplikasi memenuhi syarat dipasang (installable)
    page.evaluate("navigator.serviceWorker.ready.then(() => true)")
    cdp = page.context.new_cdp_session(page)
    hasil = cdp.send("Page.getInstallabilityErrors")
    # "in-incognito" muncul karena Playwright selalu memakai jendela privat; bukan masalah aplikasi.
    galat = [e for e in hasil["installabilityErrors"] if e["errorId"] != "in-incognito"]
    assert galat == [], hasil
    foto(page, "01-beranda")


def test_offline_setelah_kunjungan_pertama(halaman, alamat):
    page = halaman
    if page.mesin != "chromium":
        pytest.skip("service worker di WebKit Playwright tidak stabil; diuji di Chromium")
    page.evaluate("navigator.serviceWorker.ready.then(() => true)")
    page.reload()  # sekarang halaman dikendalikan service worker
    page.wait_for_function("navigator.serviceWorker.controller !== null")
    page.context.set_offline(True)
    page.goto(alamat + "/#/modul/m2/konsep")
    page.get_by_role("heading", name="Barisan dan suku").wait_for()
    assert page.locator("#status-offline").is_visible()
    foto(page, "02-offline-konsep")
    page.context.set_offline(False)


def test_tes_awal_rekomendasi(halaman, alamat):
    page = halaman
    page.goto(alamat + "/#/tes/awal")
    tombol(page, "Mulai").click()
    for jawaban in [10, 5, 25, 10, 8, 20]:
        kirim_isian(page, jawaban)
        page.locator(".umpan-netral").wait_for()  # tes tidak menampilkan benar/salah
        lanjut(page)
    page.get_by_text("6 / 6").wait_for()
    assert page.get_by_text("M4").first.is_visible()


def test_alur_modul_m2_lengkap(halaman, alamat):
    page = halaman
    page.goto(alamat + "/#/modul/m2/konsep")

    # --- Konsep: 5 segmen ---
    for _ in range(4):
        tombol(page, "Lanjut →").click()
    foto(page, "03-konsep-segmen5")
    tombol(page, "Selesai, lihat contoh →").click()

    # --- Contoh lengkap: 2 contoh x 5 langkah ---
    page.get_by_text("Contoh 1 dari 2").wait_for()
    for _ in range(4):
        tombol(page, "Langkah berikutnya ↓").click()
    foto(page, "04-contoh-lengkap")
    tombol(page, "Contoh berikutnya →").click()
    for _ in range(4):
        tombol(page, "Langkah berikutnya ↓").click()
    tombol(page, "Lanjut ke contoh setengah jadi →").click()

    # --- Contoh setengah jadi ---
    page.get_by_text("Contoh 1 dari 2").wait_for()
    tombol(page, "Langkah berikutnya ↓").click()
    page.locator(".langkah-kosong input").fill("4")  # salah dulu
    tombol(page, "Periksa").click()
    page.locator(".umpan-salah").wait_for()
    page.locator(".langkah-kosong input").fill("5")
    tombol(page, "Periksa").click()
    page.locator(".langkah-kosong .umpan-benar").wait_for()
    tombol(page, "Langkah berikutnya ↓").click()
    tombol(page, "Langkah berikutnya ↓").click()
    tombol(page, "Langkah berikutnya ↓").click()
    tombol(page, "Contoh berikutnya →").click()
    tombol(page, "Langkah berikutnya ↓").click()
    page.locator(".langkah-kosong input").last.fill("5 + 2n")
    tombol(page, "Periksa").click()
    page.locator(".langkah-kosong").last.locator(".umpan-benar").wait_for()
    tombol(page, "Langkah berikutnya ↓").click()
    page.locator(".langkah-kosong input").last.fill("29")
    tombol(page, "Periksa").click()
    foto(page, "05-setengah-jadi")
    tombol(page, "Langkah berikutnya ↓").click()
    tombol(page, "Lanjut ke latihan →").click()

    # --- Latihan ---
    # L1: salah dulu -> umpan balik khusus -> petunjuk -> benar
    kirim_isian(page, 15)
    page.locator(".umpan-salah", has_text="14 + 1").wait_for()
    page.get_by_role("button", name="💡 Butuh petunjuk?").click()
    assert page.locator(".petunjuk").count() == 1
    tombol(page, "Tampilkan lompatan").click()
    assert page.locator(".barisan-selisih").first.is_visible()
    foto(page, "06-latihan-umpan-balik")
    kirim_isian(page, 17)
    page.locator(".umpan-benar").wait_for()
    lanjut(page)
    # L2: umpan balik miskonsepsi 4 x 8
    kirim_isian(page, 32)
    page.locator(".umpan-salah", has_text="4 × 8").wait_for()
    kirim_isian(page, 30)
    lanjut(page)
    # L3: lengkapi tabel
    sel = page.locator(".isian-sel")
    sel.nth(0).fill("12")
    sel.nth(1).fill("27")
    tombol(page, "Kirim").click()
    page.locator(".umpan-benar").wait_for()
    lanjut(page)
    # L4: pilihan ganda
    page.locator("label.pilihan", has_text="Uₙ = 3n + 1").click()
    tombol(page, "Kirim").click()
    page.locator(".umpan-benar").wait_for()
    lanjut(page)
    # L5: rumus -> Cek Aturanmu dipakai
    page.locator(".cek-aturan summary").click()
    page.locator(".cek-aturan input").fill("3n+1")
    page.locator(".cek-aturan").get_by_role("button", name="Cek", exact=True).click()
    page.get_by_text("Ada yang belum cocok").wait_for()
    page.locator(".cek-aturan input").fill("3n-2")
    page.locator(".cek-aturan").get_by_role("button", name="Cek", exact=True).click()
    page.get_by_text("Aturanmu cocok").wait_for()
    foto(page, "07-cek-aturanmu")
    page.locator(".soal > div input.isian").first.fill("3n − 2")
    tombol(page, "Kirim").click()
    page.locator(".umpan-benar").wait_for()
    lanjut(page)
    page.get_by_text("Latihan selesai").wait_for()
    tombol(page, "Lanjut ke soal cerita →").click()

    # --- Literasi: siklus BACA -> UBAH -> HITUNG -> CEK CERITA ---
    tombol(page, "Mulai").click()
    kata = page.locator(".stimulus button.kata")
    teks = kata.all_inner_texts()
    target = [["12", "kursi."], ["bertambah", "3", "kursi."], ["paling", "banyak", "40", "kursi."]]
    for frasa in target:
        for i in range(len(teks)):
            if teks[i:i + len(frasa)] == frasa:
                for j in range(len(frasa)):
                    kata.nth(i + j).click()
                break
    page.locator("textarea").fill("kursi di baris ke-4 dan banyak baris")
    tombol(page, "Periksa").click()
    page.get_by_text("3 dari 3 informasi penting").wait_for()
    foto(page, "08-literasi-baca")
    tombol(page, "Lanjut →").click()
    sel = page.locator(".isian-sel")
    for i, v in enumerate([18, 21, 24]):
        sel.nth(i).fill(str(v))
    tombol(page, "Kirim").click()
    lanjut(page)
    kirim_isian(page, 21)                                     # soal 1 (L1)
    lanjut(page)
    page.locator("label.pilihan", has_text="Baris ke-4 berisi 21 kursi").click()   # cek cerita
    tombol(page, "Kirim").click()
    lanjut(page)
    page.locator("label.pilihan", has_text="3n + 9").click()  # soal 2 (L2)
    tombol(page, "Kirim").click()
    lanjut(page)
    page.locator("label.pilihan", has_text="Tidak setuju").click()  # soal 3 (L3, klaim)
    page.locator("label.pilihan", has_text="Baris ke-1 belum bertambah").click()
    foto(page, "09-literasi-klaim")
    tombol(page, "Kirim").click()
    page.locator(".umpan-benar").wait_for()
    lanjut(page)
    kirim_isian(page, "10,33")                                # soal 4: jawaban pecahan -> umpan balik konteks
    page.locator(".umpan-salah", has_text="0,33 baris").wait_for()
    kirim_isian(page, 10)
    lanjut(page)
    page.locator("label.pilihan", has_text="Tidak boleh").click()
    tombol(page, "Kirim").click()
    lanjut(page)
    page.get_by_text("Soal cerita selesai").wait_for()
    tombol(page, "Lanjut ke refleksi →").click()

    # --- Refleksi + skala usaha mental ---
    page.locator("textarea").fill("Pertama, aku mencari selisihnya lalu membandingkan dengan suku pertama.")
    tombol(page, "Simpan").click()
    page.get_by_text("Bandingkan dengan contoh penjelasan").wait_for()
    tombol(page, "Lanjut →").click()
    page.get_by_role("radio", name=re.compile("^4:")).click()
    foto(page, "10-skala-paas")
    tombol(page, "Simpan").click()

    # --- Kuis ---
    tombol(page, "Mulai kuis").click()
    for j in [33, 59]:
        kirim_isian(page, j)
        lanjut(page)
    page.locator(".soal input.isian").first.fill("5n+3")
    tombol(page, "Kirim").click()
    lanjut(page)
    for i, nilai in enumerate(["Benar", "Benar", "Salah", "Benar"]):
        page.locator(".bs-baris").nth(i).get_by_role("button", name=nilai, exact=True).click()
    tombol(page, "Kirim").click()
    lanjut(page)
    page.get_by_text("4 / 4").wait_for()
    page.get_by_role("radio", name=re.compile("^3:")).click()
    tombol(page, "Simpan").click()

    # --- Kembali ke peta: M2 selesai ---
    page.get_by_role("heading", name="Peta Materi").wait_for()
    assert page.locator(".peta-item", has_text="Pola dengan Selisih Tetap").locator(".lencana-selesai").count() == 1
    foto(page, "11-peta-selesai")

    # --- Progres & profil literasi ---
    page.goto(alamat + "/#/progres")
    page.get_by_text("Kamu sudah kuat di").wait_for()
    # Soal 4 (CEK CERITA/HITUNG) sempat salah, jadi profil harus menyarankan latihan, bukan nilai penuh.
    page.get_by_text("Ayo latih").wait_for()
    foto(page, "12-progres")

    # --- Data tersimpan & bisa dikirim ke peneliti ---
    page.goto(alamat + "/#/tentang")
    page.locator("input.isian").fill("s01")
    tombol(page, "Simpan kode").click()
    tombol(page, "📤 Kirim ke peneliti").click()
    page.get_by_text("Data berhasil dikirim").wait_for()
    data = page.evaluate("JSON.parse(localStorage.getItem('polaku:v1'))")
    assert data["profil"]["kodeSiswa"] == "S01"
    assert data["progres"]["m2"]["status"] == "selesai"
    assert any(s["aktivitas"] == "kuis" for s in data["skalaBeban"])
    assert any("LM6" in (c.get("proses") or []) and c["benar"] for c in data["literasi"])
    assert any(p.get("cekAturanDipakai") for p in data["percobaan"])
    foto(page, "13-tentang")


def test_modul_m4_visual_noktah(halaman, alamat):
    page = halaman
    page.goto(alamat + "/#/modul/m4/konsep")
    page.locator(".noktah-gambar").first.wait_for()
    assert page.locator(".noktah-gambar").count() == 4
    assert page.locator("svg circle.noktah-baru").count() > 0
    foto(page, "14-m4-noktah")
    page.goto(alamat + "/#/modul/m4/literasi")
    tombol(page, "Mulai").click()
    page.get_by_text("Motif Batik Kawung").first.wait_for()
    foto(page, "15-m4-kawung")


def test_hapus_data_dengan_konfirmasi(halaman, alamat):
    page = halaman
    page.evaluate("localStorage.setItem('polaku:v1', JSON.stringify({progres:{m2:{status:'selesai',tahapSelesai:[]}}}))")
    page.goto(alamat + "/#/tentang")
    tombol(page, "Hapus semua data saya").click()
    tombol(page, "Batal").click()
    assert page.evaluate("localStorage.getItem('polaku:v1')") is not None
    tombol(page, "Hapus semua data saya").click()
    page.evaluate("sessionStorage.setItem('uji:tanpa-nama', '1')")  # cegah nama uji diisi ulang
    tombol(page, "Ya, hapus").click()
    # Setelah semua data dihapus (termasuk nama), siswa kembali ke halaman sambutan.
    page.get_by_role("heading", name="Selamat datang!").wait_for()
    assert page.evaluate("localStorage.getItem('polaku:v1')") is None
    assert page.evaluate("localStorage.getItem('polaku:nama')") is None
