"""Ilustrasi pola bilangan harus BENAR secara matematis (aplikasi pendidikan matematika).

Rumus dihitung ulang di sini secara mandiri, bukan disalin dari pembuat ilustrasi.
"""
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

IMG = Path(__file__).resolve().parent.parent / "frontend" / "img"
NS = "{http://www.w3.org/2000/svg}"

RUMUS = {
    "persegi": lambda k: k * k,
    "segitiga": lambda k: k * (k + 1) // 2,
    "ganjil": lambda k: 2 * k - 1,
    "persegi-panjang": lambda k: k * (k + 1),
}

SEMUA_SVG = sorted(IMG.glob("*.svg"))


def kelompok_pola(path):
    akar = ET.parse(path).getroot()
    return [g for g in akar.iter(f"{NS}g") if g.get("data-pola")]


def test_ada_ilustrasi():
    nama = {p.name for p in SEMUA_SVG}
    assert {"hias-persegi.svg", "hias-segitiga.svg", "hias-angka.svg", "hias-bentuk.svg", "beranda.svg"} <= nama
    assert {f"modul-m{i}.svg" for i in range(9)} <= nama


@pytest.mark.parametrize("path", SEMUA_SVG, ids=[p.name for p in SEMUA_SVG])
def test_jumlah_noktah_sesuai_rumus(path):
    for g in kelompok_pola(path):
        pola, k = g.get("data-pola"), int(g.get("data-suku"))
        noktah = [c for c in g.iter(f"{NS}circle")]
        harapan = RUMUS[pola](k)
        assert len(noktah) == harapan, f"{path.name}: pola {pola} suku ke-{k} berisi {len(noktah)} noktah, seharusnya {harapan}"
        assert int(g.get("data-jumlah")) == harapan
        # tidak ada noktah yang bertumpuk (semua posisi berbeda)
        posisi = {(c.get("cx"), c.get("cy")) for c in noktah}
        assert len(posisi) == len(noktah), f"{path.name}: ada noktah bertumpuk"


@pytest.mark.parametrize("nama, pola, suku", [
    ("hias-persegi.svg", "persegi", [1, 2, 3, 4]),       # 1, 4, 9, 16
    ("hias-segitiga.svg", "segitiga", [1, 2, 3, 4]),     # 1, 3, 6, 10
    ("beranda.svg", "persegi", [1, 2, 3, 4]),            # 1, 4, 9, 16
    ("modul-m3.svg", "ganjil", [1, 2, 3]),               # 1, 3, 5
    ("modul-m4.svg", "persegi", [1, 2, 3]),              # 1, 4, 9
    ("modul-m5.svg", "segitiga", [1, 2, 3]),             # 1, 3, 6
])
def test_pola_berurutan_lengkap(nama, pola, suku):
    g = kelompok_pola(IMG / nama)
    assert [x.get("data-pola") for x in g] == [pola] * len(suku)
    assert [int(x.get("data-suku")) for x in g] == suku


def test_label_angka_beranda_cocok_dengan_noktah():
    akar = ET.parse(IMG / "beranda.svg").getroot()
    label = [t.text for t in akar.iter(f"{NS}text")]
    jumlah = [str(len(list(g.iter(f"{NS}circle")))) for g in kelompok_pola(IMG / "beranda.svg")]
    assert jumlah == ["1", "4", "9", "16"]
    assert label == jumlah


def test_persamaan_angka_berwajah_benar():
    akar = ET.parse(IMG / "hias-angka.svg").getroot()
    g = next(x for x in akar.iter(f"{NS}g") if x.get("data-persamaan"))
    teks = [t.text for t in g.iter(f"{NS}text")]
    angka = [int(t) for t in teks if t.isdigit()]
    assert angka == [1, 2, 3] and angka[0] + angka[1] == angka[2]
    assert "+" in teks and "=" in teks
    assert len([c for c in g.iter(f"{NS}circle")]) == 3   # hanya badan tokoh; mata berupa garis lengkung


def test_persegi_fibonacci_menyusun_persegi_panjang():
    akar = ET.parse(IMG / "modul-m6.svg").getroot()
    kotak = [r for r in akar.iter(f"{NS}rect") if r.get("class") == "fib"]
    sisi = sorted(int(r.get("data-sisi")) for r in kotak)
    assert sisi == [1, 1, 2, 3, 5]
    for i in range(2, len(sisi)):
        assert sisi[i] == sisi[i - 1] + sisi[i - 2]           # deret Fibonacci
    # menutup persegi panjang 8 × 5 tepat, tanpa celah dan tanpa tumpang tindih
    sel = set()
    for r in kotak:
        x, y, s = int(r.get("data-x")), int(r.get("data-y")), int(r.get("data-sisi"))
        for i in range(x, x + s):
            for j in range(y, y + s):
                assert (i, j) not in sel, "persegi bertumpuk"
                sel.add((i, j))
    assert sel == {(i, j) for i in range(8) for j in range(5)}
    # label angka di dalam persegi sesuai sisinya
    label = sorted(int(t.text) for t in akar.iter(f"{NS}text"))
    assert label == [2, 3, 5]


@pytest.mark.parametrize("path", SEMUA_SVG, ids=[p.name for p in SEMUA_SVG])
def test_svg_lokal_dan_aman(path):
    isi = path.read_text(encoding="utf-8")
    assert "<script" not in isi and "href=\"http" not in isi and "xlink:href" not in isi
    ET.fromstring(isi)  # XML valid
