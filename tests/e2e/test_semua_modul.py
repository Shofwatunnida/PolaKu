"""Setiap modul yang tersedia harus bisa dibuka dan ketujuh tahapnya berisi konten.

Kuis diselesaikan otomatis memakai kunci jawaban dari file konten, lalu dipastikan modul
tercatat "selesai" di Peta Materi dan di penyimpanan perangkat.
Daftar modul diambil dari konten/modul.json, jadi modul baru otomatis ikut diuji.
"""
import json
import re
from pathlib import Path

import pytest

from test_alur import PERANGKAT, alamat, peramban, pw, tombol  # noqa: F401

KONTEN = Path(__file__).resolve().parents[2] / "frontend" / "konten"
DAFTAR = json.loads((KONTEN / "modul.json").read_text(encoding="utf-8"))["modul"]
TERSEDIA = [m["id"] for m in DAFTAR if m["tersedia"]]
PERANGKAT_UJI = {k: PERANGKAT[k] for k in ("android-390", "iphone-webkit")}


@pytest.fixture(params=list(PERANGKAT_UJI))
def hal(request, pw, peramban, alamat):  # noqa: F811
    mesin, desk = PERANGKAT_UJI[request.param]
    opsi = dict(pw.devices[desk]) if isinstance(desk, str) else dict(desk)
    opsi.pop("default_browser_type", None)
    ctx = peramban(mesin).new_context(**opsi, locale="id-ID")
    ctx.add_init_script("try { if (!localStorage.getItem('polaku:nama')) localStorage.setItem('polaku:nama', 'Uji'); } catch (e) {}")
    page = ctx.new_page()
    galat = []
    page.on("pageerror", lambda e: galat.append(str(e)))
    yield page
    ctx.close()
    assert galat == [], galat


def tidak_ada_galat(page):
    assert page.get_by_text("Ups, ada masalah").count() == 0
    assert page.get_by_text("Halaman tidak ditemukan").count() == 0


def test_semua_modul_bisa_dibuka_dari_peta(hal, alamat):
    page = hal
    page.goto(alamat + "/#/peta")
    page.locator(".peta-item").first.wait_for()
    for m in DAFTAR:
        kartu = page.locator(".peta-item", has_text=m["judul"])
        if m["tersedia"]:
            assert kartu.evaluate("el => el.tagName") == "A", f"{m['id']} harus bisa diklik"
            assert kartu.get_attribute("href") == f"#/modul/{m['id']}"
            assert "Segera hadir" not in kartu.inner_text()
        else:
            assert "Segera hadir" in kartu.inner_text()


@pytest.mark.parametrize("modul_id", TERSEDIA)
def test_ketujuh_tahap_berisi_konten(hal, alamat, modul_id):
    page = hal
    isi = json.loads((KONTEN / f"{modul_id}.json").read_text(encoding="utf-8"))
    page.goto(alamat + f"/#/modul/{modul_id}")
    page.locator(".tahap-item").first.wait_for()
    assert page.locator(".tahap-item").count() == 7
    tidak_ada_galat(page)

    page.goto(alamat + f"/#/modul/{modul_id}/konsep")
    page.get_by_text(f"Bagian 1 dari {len(isi['segmen'])}").wait_for()
    assert page.locator(".segmen p").count() >= 1

    page.goto(alamat + f"/#/modul/{modul_id}/contoh")
    page.get_by_text(f"Contoh 1 dari {len(isi['contohLengkap'])}").wait_for()
    assert page.locator(".langkah-contoh li").count() >= 1

    page.goto(alamat + f"/#/modul/{modul_id}/setengah")
    page.get_by_text(f"Contoh 1 dari {len(isi['contohSetengahJadi'])}").wait_for()

    page.goto(alamat + f"/#/modul/{modul_id}/latihan")
    page.get_by_text(f"Soal 1 dari {len(isi['latihan'])}").wait_for()
    assert page.locator(".soal-tanya").inner_text().strip()

    page.goto(alamat + f"/#/modul/{modul_id}/literasi")
    tombol(page, "Mulai").click()
    page.locator(".stimulus").first.wait_for()
    assert isi["literasi"][0]["judul"] in page.locator(".stimulus summary").first.inner_text()

    page.goto(alamat + f"/#/modul/{modul_id}/refleksi")
    page.locator("textarea").wait_for()

    page.goto(alamat + f"/#/modul/{modul_id}/kuis")
    tombol(page, "Mulai kuis").click()
    page.get_by_text(f"Soal 1 dari {len(isi['kuis'])}").wait_for()
    tidak_ada_galat(page)


def jawab(page, soal):
    """Mengisi jawaban benar untuk satu soal berdasarkan kunci di konten."""
    t = soal["tipe"]
    if t in ("isian-angka", "isian-rumus"):
        page.locator(".soal input.isian").first.fill(str(soal["jawaban"]))
    elif t == "pilihan-ganda":
        page.locator(".soal label.pilihan").nth(soal["jawaban"]).click()
    elif t == "pg-kompleks":
        for i, p in enumerate(soal["pernyataan"]):
            page.locator(".bs-baris").nth(i).get_by_role("button", name="Benar" if p["benar"] else "Salah", exact=True).click()
    elif t == "menjodohkan":
        for i, p in enumerate(soal["pasangan"]):
            page.locator(".jodoh-baris select").nth(i).select_option(str(p["jawaban"]))
    elif t == "lengkapi-tabel":
        for i, k in enumerate(soal["kunciTabel"]):
            page.locator(".isian-sel").nth(i).fill(str(k))
    elif t == "klaim":
        pilihan = page.locator(".klaim label.pilihan")
        pilihan.nth(0 if soal["klaimBenar"] else 1).click()
        pilihan.nth(2 + soal["alasan"]["benar"]).click()
    else:
        raise AssertionError(f"tipe soal kuis belum didukung uji: {t}")
    tombol(page, "Kirim").click()


@pytest.mark.parametrize("modul_id", TERSEDIA)
def test_kuis_selesai_dan_progres_tersimpan(hal, alamat, modul_id):
    page = hal
    isi = json.loads((KONTEN / f"{modul_id}.json").read_text(encoding="utf-8"))
    page.goto(alamat + f"/#/modul/{modul_id}/kuis")
    tombol(page, "Mulai kuis").click()
    for s in isi["kuis"]:
        jawab(page, s)
        page.locator(".umpan-benar").wait_for()
        tombol(page, "Lanjut →").click()
    n = len(isi["kuis"])
    page.get_by_text(f"{n} / {n}").wait_for()
    page.get_by_role("radio", name=re.compile("^4:")).click()
    tombol(page, "Simpan").click()
    page.get_by_role("heading", name="Peta Materi").wait_for()
    kartu = page.locator(".peta-item", has_text=isi["judul"])
    assert kartu.locator(".lencana-selesai").count() == 1
    data = page.evaluate("JSON.parse(localStorage.getItem('polaku:v1'))")
    assert data["progres"][modul_id]["status"] == "selesai"
    assert any(p.get("modulId") == modul_id and p.get("mode") == "kuis-ringkasan" and p.get("skor") == n for p in data["percobaan"])
    assert any(s.get("modulId") == modul_id and s.get("aktivitas") == "kuis" for s in data["skalaBeban"])


def test_visual_dua_segitiga_m5_benar(hal, alamat):
    """Gambar 'dua segitiga' di M5: setiap gambar ke-n berisi dua segitiga yang masing-masing n(n+1)/2 noktah."""
    page = hal
    if "m5" not in TERSEDIA:
        pytest.skip("M5 belum tersedia")
    page.goto(alamat + "/#/modul/m5/konsep")
    for _ in range(3):
        tombol(page, "Lanjut →").click()
    page.get_by_text("Bagian 4 dari 5").wait_for()
    gambar = page.locator(".noktah-gambar")
    assert gambar.count() == 3
    for i in range(3):
        n = i + 1
        a = gambar.nth(i).locator("circle.noktah-a").count()
        b = gambar.nth(i).locator("circle.noktah-b").count()
        assert a == b == n * (n + 1) // 2, (n, a, b)
        assert f"{a} + {b} = {a + b}" in gambar.nth(i).inner_text()


def test_deret_bentuk_m1_tampil_sesuai_konten(hal, alamat):
    page = hal
    if "m1" not in TERSEDIA:
        pytest.skip("M1 belum tersedia")
    isi = json.loads((KONTEN / "m1.json").read_text(encoding="utf-8"))
    page.goto(alamat + "/#/modul/m1/latihan")
    page.get_by_text("Soal 1 dari 5").wait_for()
    l1 = isi["latihan"][0]["visual"]
    deret = page.locator(".deret-bentuk").first
    assert deret.locator(".deret-butir svg").count() == len(l1["deret"])
    assert deret.locator(".deret-tanya").count() == l1["tanya"]
    # nomor urut di bawah bentuk membantu menghitung posisi
    assert deret.locator(".deret-butir small").last.inner_text() == str(len(l1["deret"]) + l1["tanya"])
    assert "lingkaran pink" in deret.get_attribute("aria-label")


def test_fibonacci_tanpa_cek_aturan(hal, alamat):
    """Pola Fibonacci tidak punya rumus suku ke-n sederhana, jadi alat 'Cek Aturanmu' tidak boleh muncul."""
    page = hal
    if "m6" not in TERSEDIA:
        pytest.skip("M6 belum tersedia")
    page.goto(alamat + "/#/modul/m6/latihan")
    page.get_by_text("Soal 1 dari 5").wait_for()
    assert page.locator(".cek-aturan").count() == 0
    page.locator(".soal input.isian").first.fill("14")
    tombol(page, "Kirim").click()
    page.locator(".umpan-salah", has_text="jumlahkan dua suku terakhir").wait_for()
    page.locator(".soal input.isian").first.fill("16")
    tombol(page, "Coba lagi").click()
    page.locator(".umpan-benar").wait_for()


def test_garis_warna_berhuruf_untuk_buta_warna(hal, alamat):
    page = hal
    if "m1" not in TERSEDIA:
        pytest.skip("M1 belum tersedia")
    page.goto(alamat + "/#/modul/m1/literasi")
    tombol(page, "Mulai").click()
    huruf = page.locator(".stimulus .deret-butir svg text").evaluate_all("els => els.map(e => e.textContent)")
    assert huruf[:4] == ["M", "M", "K", "H"]
