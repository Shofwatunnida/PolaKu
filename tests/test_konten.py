"""Uji validator konten (tools/validasi_konten.py)."""
import json

import pytest

from tools.validasi_konten import Laporan, hitung_kalimat, hitung_rumus, validasi_modul, validasi_semua
from conftest import muat_json


def test_konten_asli_valid():
    lap = validasi_semua()
    assert lap.kesalahan == []


@pytest.mark.parametrize("rumus, n, harapan", [("3n+1", 2, 7), ("n²", 5, 25), ("n(n+1)", 3, 12), ("n(n+1)/2", 4, 10), ("5n-3", 1, 2)])
def test_hitung_rumus(rumus, n, harapan):
    assert hitung_rumus(rumus, n) == harapan


@pytest.mark.parametrize("bahaya", ["__import__('os')", "open('x')", "n.real", "a+1"])
def test_hitung_rumus_menolak_kode(bahaya):
    with pytest.raises(Exception):
        hitung_rumus(bahaya, 1)


def test_hitung_kalimat():
    assert hitung_kalimat("Satu. Dua! Tiga?") == 3
    assert hitung_kalimat("Pola 1, 4, 9, 16 dan **10,5**.") == 1


def _modul_m2():
    return muat_json("m2.json")


def test_segmen_terlalu_panjang_ditolak():
    m = _modul_m2()
    m["segmen"][0]["teks"] = ["Satu.", "Dua.", "Tiga.", "Empat."]
    lap = Laporan()
    validasi_modul(m, "uji", lap)
    assert any("maksimal 3 kalimat" in k for k in lap.kesalahan)


def test_kunci_rumus_salah_ditolak():
    m = _modul_m2()
    soal = next(s for s in m["latihan"] if s["tipe"] == "isian-rumus")
    soal["jawaban"] = "3n+5"
    lap = Laporan()
    validasi_modul(m, "uji", lap)
    assert any("tidak cocok dengan pola" in k for k in lap.kesalahan)


def test_petunjuk_harus_tiga():
    m = _modul_m2()
    m["latihan"][0]["petunjuk"] = ["hanya satu"]
    lap = Laporan()
    validasi_modul(m, "uji", lap)
    assert any("3 petunjuk" in k for k in lap.kesalahan)


def test_literasi_harus_berjenjang_dan_ada_penalaran():
    m = _modul_m2()
    st = m["literasi"][0]
    st["soal"] = list(reversed(st["soal"]))
    for s in st["soal"]:
        s["proses"] = ["LM3"]
    lap = Laporan()
    validasi_modul(m, "uji", lap)
    assert any("berjenjang" in k for k in lap.kesalahan)
    assert any("LM6" in k for k in lap.kesalahan)


def test_stimulus_terlalu_panjang(tmp_path):
    m = _modul_m2()
    m["literasi"][0]["teks"] += " kata" * 120
    lap = Laporan()
    validasi_modul(m, "uji", lap)
    assert any("maksimal 120" in k for k in lap.kesalahan)


def test_modul_tersedia_tanpa_file(tmp_path):
    (tmp_path / "modul.json").write_text(json.dumps({"modul": [{"id": "m9", "kode": "M9", "judul": "x", "tersedia": True}]}), encoding="utf-8")
    lap = validasi_semua(tmp_path)
    assert any("m9.json tidak ada" in k for k in lap.kesalahan)


def test_dokumen_kunci_rubrik_sesuai_konten(tmp_path, monkeypatch):
    """docs/13 dibuat dari konten; jika konten berubah, jalankan: python tools/buat_kunci_rubrik.py"""
    from pathlib import Path
    import tools.buat_kunci_rubrik as gen
    asli = Path(gen.KELUAR).read_text(encoding="utf-8")
    monkeypatch.setattr(gen, "KELUAR", tmp_path / "13.md")
    gen.main()
    assert (tmp_path / "13.md").read_text(encoding="utf-8") == asli, "docs/13 belum diperbarui: jalankan python tools/buat_kunci_rubrik.py"


def test_setiap_modul_tersedia_punya_rubrik_refleksi():
    import tools.buat_kunci_rubrik as gen
    for m in muat_json("modul.json")["modul"]:
        if m["tersedia"]:
            assert m["id"] in gen.RUBRIK and len(gen.RUBRIK[m["id"]]) == 4, m["id"]


def _modul(nama):
    return muat_json(nama)


def test_kunci_pola_berulang_salah_ditolak():
    m = _modul("m1.json")
    soal = next(s for s in m["latihan"] if s["id"] == "m1-l3")
    soal["jawaban"] = 0          # "Lingkaran", padahal bentuk ke-30 adalah persegi
    lap = Laporan()
    validasi_modul(m, "uji", lap)
    assert any("bentuk ke-30 seharusnya persegi" in k for k in lap.kesalahan)


def test_hitungan_pola_berulang_salah_ditolak():
    m = _modul("m1.json")
    soal = next(s for s in m["latihan"] if s["id"] == "m1-l4")
    soal["jawaban"] = 6          # lupa 2 bentuk sisa
    lap = Laporan()
    validasi_modul(m, "uji", lap)
    assert any("banyak segitiga dalam 20 butir seharusnya 7" in k for k in lap.kesalahan)


def test_deret_tidak_sesuai_satuan_dan_bentuk_asing_ditolak():
    m = _modul("m1.json")
    soal = next(s for s in m["latihan"] if s["id"] == "m1-l2")
    soal["visual"]["deret"][5] = "segitiga-biru"   # merusak pengulangan
    m["segmen"][0]["visual"]["deret"][0] = "jajargenjang-pink"
    lap = Laporan()
    validasi_modul(m, "uji", lap)
    assert any("tidak sesuai satuan pola" in k for k in lap.kesalahan)
    assert any("butir deret bentuk tidak dikenal" in k for k in lap.kesalahan)
