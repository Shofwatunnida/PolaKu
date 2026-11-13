"""Uji logika JavaScript (frontend/js/answer.js & pattern.js) dari Python."""
import pytest

from conftest import muat_json


# ---------- Pemeriksa rumus (tabel kasus uji di docs/08-rencana-pengujian.md) ----------
@pytest.mark.parametrize("kunci, siswa, harapan", [
    ("3n+1", "3n + 1", True),
    ("3n+1", "1+3n", True),
    ("3n+1", "3×n+1", True),
    ("3n+1", "3 x n + 1", True),
    ("3n+1", "Un = 3n + 1", True),
    ("3n+1", "3n+4", False),
    ("n^2", "n²", True),
    ("n^2", "n*n", True),
    ("n(n+1)", "n²+n", True),
    ("n(n+1)", "n(n+1)", True),
    ("n(n+1)/2", "(n^2+n)/2", True),
    ("3n-2", "3n − 2", True),
    ("2n+5", "5+2n", True),
    ("4n-1", "4(n-1)", False),
])
def test_rumus_setara(js, kunci, siswa, harapan):
    assert js.panggil("rumusSetara", siswa, kunci) is harapan


@pytest.mark.parametrize("teks", ["abc", "3n+", "", "(3n", "3$n"])
def test_rumus_tidak_valid(js, teks):
    hasil = js.panggil("cobaParseRumus", teks)
    assert hasil["valid"] is False
    assert hasil["pesan"]


# ---------- Angka ----------
@pytest.mark.parametrize("teks, harapan", [
    ("31", 31), (" 31 kursi", 31), ("Rp35.000", 35000), ("15.000", 15000),
    ("10,33", 10.33), ("10.5", 10.5), ("10.33", 10.33), ("1.250,5", 1250.5), ("-4", -4), ("abc", None), ("", None),
])
def test_parse_angka(js, teks, harapan):
    assert js.panggil("parseAngka", teks) == harapan


# ---------- Cek Aturanmu ----------
def test_cek_aturan_cocok(js):
    r = js.panggil("cekAturan", "3n+1", [4, 7, 10])
    assert r["valid"] and r["semuaCocok"]
    assert [b["rumus"] for b in r["baris"]] == [4, 7, 10]


def test_cek_aturan_tidak_cocok(js):
    r = js.panggil("cekAturan", "3n", [4, 7, 10])
    assert r["valid"] and not r["semuaCocok"]
    assert [b["cocok"] for b in r["baris"]] == [False, False, False]


# ---------- Umpan balik khusus ----------
def test_umpan_balik_khusus_angka(js):
    soal = {"tipe": "isian-angka", "jawaban": 30, "umpanBalik": [{"jawaban": 32, "pesan": "pakai 4 x 8"}], "umpanBalikUmum": "umum"}
    assert js.panggil("periksaJawaban", soal, "32") == {"benar": False, "pesan": "pakai 4 x 8"}
    assert js.panggil("periksaJawaban", soal, "33")["pesan"] == "umum"
    assert js.panggil("periksaJawaban", soal, "30")["benar"] is True


@pytest.mark.parametrize("jawaban", ["10,33", "10,3", "10,333", "10.33"])
def test_umpan_balik_dengan_toleransi(js, jawaban):
    soal = {"tipe": "isian-angka", "jawaban": 10, "umpanBalik": [{"jawaban": 10.33, "toleransi": 0.04, "pesan": "pecahan baris?"}], "umpanBalikUmum": "umum"}
    assert js.panggil("periksaJawaban", soal, jawaban)["pesan"] == "pecahan baris?"
    assert js.panggil("periksaJawaban", soal, "10,5")["pesan"] == "umum"


def test_umpan_balik_khusus_rumus_setara(js):
    # Siswa menulis "1 + 3n" (setara dengan 3n+1) -> harus dapat umpan balik untuk 3n+1
    soal = {"tipe": "isian-rumus", "jawaban": "3n-2", "umpanBalik": [{"jawaban": "3n+1", "pesan": "cek n=1"}], "umpanBalikUmum": "umum"}
    assert js.panggil("periksaJawaban", soal, "1 + 3n")["pesan"] == "cek n=1"


def test_isian_kosong_ditandai(js):
    assert js.panggil("periksaJawaban", {"tipe": "isian-angka", "jawaban": 3}, "")["kosong"] is True
    assert js.panggil("periksaJawaban", {"tipe": "uraian-singkat"}, "  ")["kosong"] is True
    assert js.panggil("periksaJawaban", {"tipe": "uraian-singkat"}, "karena bertambah 3")["benar"] is None


def test_klaim_alasan_salah(js):
    soal = {"tipe": "klaim", "klaimBenar": False, "alasan": {"pilihan": ["a", "b"], "benar": 1}}
    assert js.panggil("periksaJawaban", soal, {"setuju": False, "alasan": 1})["benar"] is True
    hasil = js.panggil("periksaJawaban", soal, {"setuju": False, "alasan": 0})
    assert hasil["benar"] is False and "alasan" in hasil["pesan"]


# ---------- Mesin pola ----------
@pytest.mark.parametrize("pola, jenis", [
    ([3, 6, 9, 12], "selisih-tetap"),
    ([1, 4, 9, 16], "selisih-tingkat-dua"),
    ([1, 1, 2, 3, 5], "fibonacci"),
    ([2, 4, 8, 16], "lainnya"),
])
def test_deteksi_pola(js, pola, jenis):
    assert js.panggil("deteksiPola", pola)["jenis"] == jenis


@pytest.mark.parametrize("bentuk, n, harapan", [("persegi", 4, 16), ("persegi-panjang", 3, 12), ("segitiga", 4, 10), ("ganjil", 5, 9)])
def test_banyak_noktah(js, bentuk, n, harapan):
    assert js.panggil("banyakNoktah", bentuk, n) == harapan


# ---------- Konsistensi konten dengan pemeriksa jawaban ----------
def _semua_soal():
    daftar = muat_json("modul.json")["modul"]
    for m in daftar:
        if not m["tersedia"]:
            continue
        isi = muat_json(f"{m['id']}.json")
        yield from ((f"{m['id']}/{s['id']}", s) for s in isi["latihan"] + isi["kuis"])
        for st in isi["literasi"]:
            yield from ((f"{m['id']}/{s['id']}", s) for s in st["soal"])
            if st.get("ubah"):
                yield f"{m['id']}/{st['id']}-ubah", {"id": "ubah", "tipe": "lengkapi-tabel", **st["ubah"]}
    for nama in ["tes-awal.json", "tes-akhir.json"]:
        yield from ((f"{nama}/{s['id']}", s) for s in muat_json(nama)["soal"])


def _kunci(s):
    t = s["tipe"]
    if t in ("isian-angka", "isian-rumus", "pilihan-ganda"):
        return str(s["jawaban"]) if t != "pilihan-ganda" else s["jawaban"]
    if t == "pg-kompleks":
        return [p["benar"] for p in s["pernyataan"]]
    if t == "menjodohkan":
        return [p["jawaban"] for p in s["pasangan"]]
    if t == "lengkapi-tabel":
        return [str(k) for k in s["kunciTabel"]]
    if t == "klaim":
        return {"setuju": s["klaimBenar"], "alasan": s["alasan"]["benar"]}
    return None


SOAL = list(_semua_soal())


@pytest.mark.parametrize("lokasi, soal", SOAL, ids=[l for l, _ in SOAL])
def test_kunci_konten_dinilai_benar(js, lokasi, soal):
    kunci = _kunci(soal)
    if kunci is None:
        pytest.skip("tidak dinilai otomatis")
    assert js.panggil("periksaJawaban", soal, kunci)["benar"] is True, lokasi
    for u in soal.get("umpanBalik", []):
        jawaban = str(u["jawaban"]) if soal["tipe"] != "pilihan-ganda" else u["jawaban"]
        hasil = js.panggil("periksaJawaban", soal, jawaban)
        assert hasil["benar"] is False and hasil["pesan"] == u["pesan"], f"{lokasi}: umpan balik untuk {u['jawaban']!r}"


# ---------- Nama panggilan (halaman sambutan) ----------
@pytest.fixture(scope="module")
def js_nama():
    from conftest import JS
    return JS("nama.js")


@pytest.mark.parametrize("masukan, harapan", [
    ("kiara", "Kiara"),
    ("  kiara   putri  ", "Kiara Putri"),
    ("Kiara123!", "Kiara"),
    ("<script>alert(1)</script>", "Scriptalertscript"),
    ("123 !!", ""),
    ("", ""),
    ("ni made ayu", "Ni Made Ayu"),
    ("o'neil-sari", "O'Neil-Sari"),
    ("Élodie", "Élodie"),
    ("a" * 40, "A" + "a" * 19),
])
def test_rapikan_nama(js_nama, masukan, harapan):
    assert js_nama.panggil("rapikanNama", masukan) == harapan


def test_motivasi_singkat(js_nama):
    daftar = js_nama.panggil("(() => MOTIVASI)")
    assert len(daftar) >= 5 and all(len(k.split()) <= 12 for k in daftar)


# ---------- Langkah kosong di contoh setengah jadi ----------
def _langkah_kosong():
    for m in muat_json("modul.json")["modul"]:
        if not m["tersedia"]:
            continue
        for c in muat_json(f"{m['id']}.json")["contohSetengahJadi"]:
            for i, l in enumerate(c["langkah"]):
                if l.get("kosong"):
                    yield f"{m['id']}/{c['id']}/langkah{i + 1}", l["kosong"]


KOSONG = list(_langkah_kosong())


@pytest.mark.parametrize("lokasi, kosong", KOSONG, ids=[x for x, _ in KOSONG])
def test_kunci_langkah_kosong_dinilai_benar(js, lokasi, kosong):
    soal = {"tipe": kosong["tipe"], "jawaban": kosong["jawaban"]}
    assert js.panggil("periksaJawaban", soal, str(kosong["jawaban"]))["benar"] is True, lokasi
