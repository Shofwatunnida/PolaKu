"""Uji khusus smartphone: ukuran sentuh, tidak ada geser ke samping, papan rumus, keyboard HP,
melanjutkan setelah halaman dimuat ulang, dan tabel vertikal.

Dijalankan di 3 perangkat (lihat PERANGKAT di test_alur.py): Android 390px, Android kecil 320px, iPhone (WebKit).
"""
import re

import pytest

from test_alur import alamat, halaman, peramban, pw, foto, tombol  # noqa: F401  (fixture dipakai ulang)

# Halaman yang diperiksa + langkah untuk sampai ke tampilan yang ingin diukur
LAYAR = [
    ("beranda", "#/", []),
    ("peta", "#/peta", []),
    ("ringkasan-modul", "#/modul/m2", []),
    ("konsep", "#/modul/m2/konsep", []),
    ("contoh", "#/modul/m2/contoh", ["Langkah berikutnya ↓"] * 4),
    ("setengah", "#/modul/m2/setengah", ["Langkah berikutnya ↓"]),
    ("latihan", "#/modul/m2/latihan", []),
    ("literasi-baca", "#/modul/m2/literasi", ["Mulai"]),
    ("kuis", "#/modul/m2/kuis", ["Mulai kuis"]),
    ("m4-konsep", "#/modul/m4/konsep", []),
    ("tes-awal", "#/tes/awal", ["Mulai"]),
    ("progres", "#/progres", []),
    ("tentang", "#/tentang", []),
]

UKUR = """() => {
  const lebar = document.documentElement.clientWidth;
  const kecil = [];
  document.querySelectorAll('main button, main a, main input, main select, main summary, main label.pilihan, .nav-bawah a').forEach(el => {
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) return;
    const gaya = getComputedStyle(el);
    if (gaya.visibility === 'hidden') return;
    const min = el.classList.contains('kata') ? 28 : 44;
    // tinggi minimal 44px; lebar minimal 44px kecuali tombol berteks panjang yang memang lebar
    if (r.height < min - 0.5 || r.width < min - 0.5) kecil.push(`${el.tagName}.${el.className} "${(el.textContent || '').trim().slice(0, 15)}" ${Math.round(r.width)}x${Math.round(r.height)}`);
  });
  return { luber: document.documentElement.scrollWidth - lebar, kecil };
}"""


@pytest.mark.parametrize("nama, rute, klik", LAYAR, ids=[x[0] for x in LAYAR])
def test_layar_pas_dan_mudah_disentuh(halaman, alamat, nama, rute, klik):  # noqa: F811
    page = halaman
    page.goto(alamat + "/" + rute)
    page.locator("main h1").wait_for()
    for t in klik:
        tombol(page, t).click()
    hasil = page.evaluate(UKUR)
    assert hasil["luber"] <= 1, f"halaman bisa digeser ke samping {hasil['luber']}px"
    assert hasil["kecil"] == [], f"target sentuh terlalu kecil: {hasil['kecil']}"


def test_tabel_diputar_vertikal_dan_tetap_benar(halaman, alamat):  # noqa: F811
    page = halaman
    page.goto(alamat + "/#/modul/m2/latihan")
    for v in ["17", "30"]:
        page.locator(".soal input.isian").first.fill(v)
        page.locator(".soal input.isian").first.press("Enter")   # tombol Enter/"Selesai" di keyboard HP mengirim jawaban
        tombol(page, "Lanjut →").click()
    tabel = page.locator("table.tabel-vertikal")
    assert tabel.count() == 1
    assert tabel.locator("tbody tr").count() == 5            # n = 1..5 menjadi baris
    lebar_tabel = tabel.bounding_box()["width"]
    assert lebar_tabel <= page.viewport_size["width"] - 32    # muat tanpa digeser
    sel = page.locator(".isian-sel")
    sel.nth(0).fill("12")
    sel.nth(0).press("Enter")                                 # Enter pindah ke kotak berikutnya
    assert page.evaluate("document.activeElement === document.querySelectorAll('.isian-sel')[1]")
    sel.nth(1).fill("27")
    sel.nth(1).press("Enter")
    page.locator(".umpan-benar").wait_for()


def test_papan_rumus_lengkap_tanpa_keyboard_hp(halaman, alamat):  # noqa: F811
    page = halaman
    page.goto(alamat + "/#/modul/m2/latihan")
    page.get_by_text("Soal 1 dari 5").wait_for()
    # Simulasikan siswa yang sudah sampai soal ke-5, lalu muat ulang halaman yang sama.
    page.evaluate("""localStorage.setItem('polaku:v1', JSON.stringify({posisi: {'m2/latihan': {i: 4, ringkas: {benar: 4, petunjuk: 0, dilewati: 0}}}}))""")
    page.reload()
    page.get_by_text("Soal 5 dari 5").wait_for()
    inp = page.locator(".soal label input.isian")
    assert inp.get_attribute("inputmode") == "none"            # keyboard HP tidak muncul; pakai papan
    papan = page.locator(".soal > div .papan-rumus").first
    for k in ["3", "n", "−", "2"]:
        papan.get_by_role("button", name=k, exact=True).click()
    assert inp.input_value() == "3n−2"
    # sisip di tengah: pindah kursor ke awal lalu ketik "1" -> "13n−2", lalu hapus
    inp.evaluate("el => el.setSelectionRange(0, 0)")
    papan.get_by_role("button", name="1", exact=True).click()
    assert inp.input_value() == "13n−2"
    papan.get_by_role("button", name="Hapus").click()
    assert inp.input_value() == "3n−2"
    papan.get_by_role("button", name="kuadrat").click()
    assert inp.input_value() == "²3n−2"
    papan.get_by_role("button", name="Hapus").click()
    # tombol ⌨️ mengembalikan keyboard HP
    papan.get_by_role("button", name="Pakai keyboard HP").click()
    assert inp.get_attribute("inputmode") == "text"
    foto(page, "ponsel-papan-rumus")
    tombol(page, "Kirim").click()
    tombol(page, "Kirim saja").click()
    page.locator(".umpan-benar").wait_for()


def test_navigasi_tidak_menghalangi_saat_mengetik(halaman, alamat):  # noqa: F811
    page = halaman
    page.goto(alamat + "/#/modul/m2/latihan")
    nav = page.locator(".nav-bawah")
    page.locator(".soal input.isian").first.focus()
    assert nav.evaluate("el => getComputedStyle(el).visibility") == "hidden"
    page.locator(".soal input.isian").first.fill("17")
    tombol(page, "Kirim").click()                             # ketukan tidak boleh "dicuri" navigasi
    page.locator(".umpan-benar").wait_for()
    page.wait_for_timeout(500)
    assert nav.evaluate("el => getComputedStyle(el).visibility") == "visible"


def test_lanjut_setelah_halaman_dimuat_ulang(halaman, alamat):  # noqa: F811
    """Android sering menutup tab di latar belakang (mis. saat siswa membuka WhatsApp).
    Saat kembali, siswa harus berada di soal yang sama, bukan mengulang dari awal."""
    page = halaman
    page.goto(alamat + "/#/modul/m2/konsep")
    tombol(page, "Lanjut →").click()
    tombol(page, "Lanjut →").click()
    page.reload()
    page.get_by_text("Bagian 3 dari 5").wait_for()

    page.goto(alamat + "/#/modul/m2/latihan")
    for v in ["17", "30"]:
        page.locator(".soal input.isian").first.fill(v)
        tombol(page, "Kirim").click()
        tombol(page, "Lanjut →").click()
    page.reload()
    page.get_by_text("Soal 3 dari 5").wait_for()

    page.goto(alamat + "/#/modul/m2/literasi")
    tombol(page, "Mulai").click()
    tombol(page, "Periksa").click()
    tombol(page, "Lanjut →").click()                           # ke langkah UBAH
    page.reload()
    page.get_by_role("heading", name="UBAH: Jadikan barisan atau tabel").wait_for()

    page.goto(alamat + "/#/tes/awal")
    tombol(page, "Mulai").click()
    page.locator(".soal input.isian").first.fill("10")
    tombol(page, "Kirim").click()
    tombol(page, "Lanjut →").click()
    page.reload()
    tombol(page, "Lanjutkan dari soal 2").click()
    page.get_by_text("Soal 2 dari 6").wait_for()


def test_skala_paas_mudah_diketuk(halaman, alamat):  # noqa: F811
    page = halaman
    page.goto(alamat + "/#/modul/m2/refleksi")
    page.locator("textarea").fill("Pertama, aku mencari selisih")
    tombol(page, "Simpan").click()
    tombol(page, "Lanjut →").click()
    pilihan = page.get_by_role("radio")
    assert pilihan.count() == 9
    for i in range(9):
        kotak = pilihan.nth(i).bounding_box()
        assert kotak["height"] >= 44 and kotak["width"] >= 200
    page.get_by_role("radio", name=re.compile("^5:")).click()
    foto(page, "ponsel-paas")
    tombol(page, "Simpan").click()
    page.get_by_role("heading", name="Kuis", exact=True).wait_for()


def test_kata_cerita_mudah_ditandai(halaman, alamat):  # noqa: F811
    page = halaman
    page.goto(alamat + "/#/modul/m2/literasi")
    tombol(page, "Mulai").click()
    angka3 = page.locator(".stimulus button.kata", has_text=re.compile(r"^3$"))
    kotak = angka3.bounding_box()
    assert kotak["width"] >= 28 and kotak["height"] >= 28
    angka3.tap()
    assert angka3.get_attribute("aria-pressed") == "true"
    foto(page, "ponsel-literasi")
