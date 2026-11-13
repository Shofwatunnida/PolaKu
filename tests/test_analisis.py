"""Uji skrip analisis data penelitian (tools/analisis_data.py)."""
import csv
import json

import pytest

from tools.analisis_data import analisis, kategori_n_gain, n_gain


def _ekspor(kode, pre, post, waktu="2026-11-20T10:00:00Z", paas=(5, 4)):
    return {
        "aplikasi": "PolaKu", "kodeSiswa": kode, "diekspor": waktu,
        "data": {
            "progres": {"m2": {"status": "selesai", "tahapSelesai": []}},
            "percobaan": [
                {"soalId": "m2-l1", "mode": "latihan", "benar": True, "percobaanKe": 1, "jumlahPetunjuk": 0},
                {"soalId": "m2-l2", "mode": "latihan", "benar": False, "percobaanKe": 1, "jumlahPetunjuk": 1},
                {"soalId": "m2-l2", "mode": "latihan", "benar": True, "percobaanKe": 2, "jumlahPetunjuk": 2},
            ],
            "literasi": [
                {"proses": ["LM3"], "benar": True},
                {"proses": ["LM4", "LM5"], "benar": False},
                {"proses": ["LM6"], "benar": True},
            ],
            "skalaBeban": [{"modulId": "m2", "aktivitas": "latihan", "skor": paas[0]}, {"modulId": "m2", "aktivitas": "kuis", "skor": paas[1]}],
            "refleksi": [{"modulId": "m2", "teks": "selisihnya tetap"}],
            "tes": [
                {"jenis": "awal", "skor": pre, "maks": 10, "jawaban": [{"soalId": "ta1", "benar": True}]},
                {"jenis": "akhir", "skor": post, "maks": 10, "jawaban": []},
            ],
        },
    }


@pytest.mark.parametrize("pre, post, harapan", [(40, 70, 0.5), (0, 100, 1.0), (50, 50, 0.0), (100, 100, None), (None, 50, None)])
def test_n_gain(pre, post, harapan):
    assert n_gain(pre, post) == harapan


def test_kategori():
    assert kategori_n_gain(0.75) == "tinggi"
    assert kategori_n_gain(0.5) == "sedang"
    assert kategori_n_gain(0.1) == "rendah"


def test_analisis_lengkap(tmp_path):
    masuk = tmp_path / "masuk"
    masuk.mkdir()
    (masuk / "a.json").write_text(json.dumps(_ekspor("S01", 4, 7)), encoding="utf-8")
    (masuk / "b.json").write_text(json.dumps(_ekspor("S02", 2, 6)), encoding="utf-8")
    # file lama milik S01 harus diabaikan (pakai yang terbaru)
    (masuk / "c.json").write_text(json.dumps(_ekspor("S01", 1, 1, waktu="2026-11-01T00:00:00Z")), encoding="utf-8")
    (masuk / "bukan.json").write_text("{ rusak", encoding="utf-8")

    keluar = tmp_path / "hasil"
    hasil = analisis(masuk, keluar)
    assert hasil["jumlah_siswa"] == 2
    # S01: (70-40)/60 = 0.5 ; S02: (60-20)/80 = 0.5
    assert hasil["rata_n_gain"] == 0.5
    assert hasil["kategori"] == "sedang"
    assert hasil["paas_per_modul"]["m2/latihan"] == 5

    with (keluar / "ringkasan_siswa.csv").open(encoding="utf-8-sig") as f:
        baris = {r["kode_siswa"]: r for r in csv.DictReader(f)}
    s01 = baris["S01"]
    assert s01["pretest_skor"] == "4"
    assert s01["soal_latihan_dicoba"] == "2"
    assert s01["akurasi_percobaan_pertama"] == "0.5"
    assert s01["total_petunjuk"] == "2"
    assert s01["literasi_penalaran"] == "1.0"
    assert s01["literasi_cek_cerita"] == "0.0"
    for nama in ["jawaban_tes.csv", "skala_beban.csv", "refleksi.csv"]:
        assert (keluar / nama).exists()
