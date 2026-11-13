"""Uji halaman sambutan (isi nama → sapaan → Mulai Belajar), di HP dan laptop.

Juga memastikan nama TIDAK ikut ke data belajar, file ekspor, maupun server penelitian.
"""
import json
import re

import pytest

from test_alur import PERANGKAT, alamat, peramban, pw, foto, tombol  # noqa: F401

PERANGKAT_SAMBUTAN = {
    **PERANGKAT,
    "laptop-1366": ("chromium", {"viewport": {"width": 1366, "height": 768}}),
}


@pytest.fixture(params=list(PERANGKAT_SAMBUTAN))
def baru(request, pw, peramban, alamat):  # noqa: F811
    """Siswa yang baru pertama kali membuka aplikasi (belum ada nama)."""
    mesin, desk = PERANGKAT_SAMBUTAN[request.param]
    opsi = dict(pw.devices[desk]) if isinstance(desk, str) else dict(desk)
    opsi.pop("default_browser_type", None)
    ctx = peramban(mesin).new_context(**opsi, locale="id-ID")
    page = ctx.new_page()
    page.perangkat = request.param
    galat = []
    page.on("pageerror", lambda e: galat.append(str(e)))
    page.on("console", lambda m: galat.append(m.text) if m.type == "error" else None)
    yield page
    ctx.close()
    assert galat == [], f"Error JavaScript: {galat}"


def isi_nama(page, nama):
    page.get_by_label("Siapa nama panggilanmu?").fill(nama)
    page.get_by_role("button", name=re.compile(r"^(Mulai →|Simpan nama)$")).click()


def test_alur_sambutan_pertama_kali(baru, alamat):
    page = baru
    page.goto(alamat + "/")
    page.get_by_role("heading", name="Selamat datang!").wait_for()
    assert not page.locator(".nav-bawah").is_visible()          # fokus pada satu tugas
    foto(page, "sambutan-1-isi-nama")

    # Nama kosong / hanya simbol ditolak dengan pesan ramah
    isi_nama(page, "  123!! ")
    page.get_by_text("Tulis nama panggilanmu dulu").wait_for()

    isi_nama(page, "  kiara  ")                                  # huruf kecil -> otomatis kapital
    sapa = page.get_by_role("heading", name="Halo, Kiara! 👋")
    sapa.wait_for()
    page.get_by_text("Selamat datang di PolaKu. Siap belajar untuk hari ini?").wait_for()
    assert page.locator(".motivasi").inner_text().strip() != ""
    foto(page, "sambutan-2-sapaan")

    tombol(page, "Mulai Belajar").click()
    page.get_by_role("heading", name="PolaKu").wait_for()
    page.get_by_text("Halo, Kiara! 👋").wait_for()
    assert page.locator(".nav-bawah").is_visible()
    foto(page, "sambutan-3-beranda")

    # Nama tersimpan: setelah dibuka ulang tidak ditanya lagi
    page.reload()
    page.get_by_role("heading", name="PolaKu").wait_for()
    assert page.evaluate("localStorage.getItem('polaku:nama')") == "Kiara"


def test_ganti_nama(baru, alamat):
    page = baru
    page.goto(alamat + "/")
    isi_nama(page, "Kiara")
    tombol(page, "Mulai Belajar").click()
    page.get_by_role("link", name="Ganti nama").click()
    page.get_by_role("heading", name="Ganti nama panggilan").wait_for()
    assert page.get_by_label("Siapa nama panggilanmu?").input_value() == "Kiara"
    isi_nama(page, "Bima")
    page.get_by_role("heading", name="Halo, Bima! 👋").wait_for()
    tombol(page, "Mulai Belajar").click()
    page.get_by_text("Halo, Bima! 👋").wait_for()
    # dari halaman Tentang juga bisa
    page.goto(alamat + "/#/tentang")
    page.get_by_text("Namamu: Bima").wait_for()
    page.get_by_role("link", name="✏️ Ganti nama").click()
    page.get_by_role("heading", name="Ganti nama panggilan").wait_for()
    page.get_by_role("link", name="Batal").click()
    page.get_by_role("heading", name="PolaKu").wait_for()


def test_bukan_saya_dari_layar_sapaan(baru, alamat):
    page = baru
    page.goto(alamat + "/")
    isi_nama(page, "Kiara")
    tombol(page, "Bukan Kiara? Ganti nama").click()
    isi_nama(page, "Sari")
    page.get_by_role("heading", name="Halo, Sari! 👋").wait_for()


def test_tautan_langsung_tetap_menuju_tujuan(baru, alamat):
    page = baru
    page.goto(alamat + "/#/modul/m2/konsep")
    page.get_by_role("heading", name="Selamat datang!").wait_for()
    isi_nama(page, "Kiara")
    tombol(page, "Mulai Belajar").click()
    page.get_by_text("Bagian 1 dari 5").wait_for()


def test_layar_sambutan_pas_dan_mudah_disentuh(baru, alamat):
    page = baru
    page.goto(alamat + "/")
    page.get_by_role("heading", name="Selamat datang!").wait_for()
    for tahap in ["isi", "sapa"]:
        hasil = page.evaluate("""() => {
          const kecil = [];
          document.querySelectorAll('main button, main a, main input').forEach(el => {
            const r = el.getBoundingClientRect();
            if (r.width && (r.height < 44 || r.width < 44)) kecil.push(el.textContent + ' ' + Math.round(r.width) + 'x' + Math.round(r.height));
          });
          const kartu = document.querySelector('.sambutan-kartu').getBoundingClientRect();
          return { luber: document.documentElement.scrollWidth - document.documentElement.clientWidth, kecil,
                   kartuMuat: kartu.left >= 0 && kartu.right <= document.documentElement.clientWidth };
        }""")
        assert hasil["luber"] <= 1, tahap
        assert hasil["kecil"] == [], (tahap, hasil["kecil"])
        assert hasil["kartuMuat"], tahap
        if tahap == "isi":
            isi_nama(page, "Kiara")
            page.get_by_role("heading", name="Halo, Kiara! 👋").wait_for()


def test_nama_tidak_ikut_data_penelitian(baru, alamat, tmp_path):
    """Nama tidak boleh masuk ke data belajar (yang diekspor/dikirim) maupun ke server."""
    page = baru
    if page.perangkat != "android-390":
        pytest.skip("cukup diuji di satu perangkat")
    page.goto(alamat + "/")
    isi_nama(page, "Kiara Rahmawati")
    tombol(page, "Mulai Belajar").click()
    page.goto(alamat + "/#/modul/m2/konsep")
    tombol(page, "Lanjut →").click()
    data_belajar = page.evaluate("localStorage.getItem('polaku:v1')")
    assert "Kiara" not in data_belajar
    # Data yang diekspor (dipakai Unduh/Bagikan/Kirim) tidak memuat nama
    ekspor = page.evaluate("import('/js/storage.js').then(m => JSON.stringify(m.ekspor()))")
    assert "Kiara" not in ekspor and "Rahmawati" not in ekspor
    # Kirim ke server penelitian (server uji mengaktifkan penerimaan data)
    page.goto(alamat + "/#/tentang")
    page.locator("input.isian").fill("S07")
    tombol(page, "Simpan kode").click()
    with page.expect_request(lambda r: r.url.endswith("/api/penelitian")) as req:
        tombol(page, "📤 Kirim ke peneliti").click()
    badan = req.value.post_data or ""
    assert "Kiara" not in badan and "Rahmawati" not in badan
    assert json.loads(badan)["kodeSiswa"] == "S07"
    page.get_by_text("Data berhasil dikirim").wait_for()


def test_ilustrasi_jumlah_noktah_tepat(baru, alamat):
    """Ilustrasi pola 1-4-9 harus akurat secara matematis (aplikasi pendidikan matematika)."""
    page = baru
    if page.perangkat != "android-390":
        pytest.skip("cukup diuji di satu perangkat")
    page.goto(alamat + "/")
    lingkaran = page.locator(".sambutan-ilustrasi svg circle")
    warna = lingkaran.evaluate_all("els => els.map(e => e.getAttribute('fill') || e.parentElement.getAttribute('fill'))")
    assert warna.count("#93c5fd") == 1 and warna.count("#a5b4fc") == 4 and warna.count("#f472b6") == 9
    assert len(warna) == 14  # tidak ada titik lain (mata dibuat lengkung)
