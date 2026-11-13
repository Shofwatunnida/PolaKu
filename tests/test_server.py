"""Uji server Flask (server/app.py)."""
import json
import re

import pytest

from server.app import buat_app
from conftest import FRONTEND


@pytest.fixture
def klien(tmp_path):
    app = buat_app(penelitian_aktif=False, folder_data=tmp_path)
    return app.test_client()


@pytest.fixture
def klien_penelitian(tmp_path):
    app = buat_app(penelitian_aktif=True, folder_data=tmp_path)
    return app.test_client(), tmp_path


def test_beranda(klien):
    r = klien.get("/")
    assert r.status_code == 200
    assert b"<title>PolaKu" in r.data
    assert "Content-Security-Policy" in r.headers


def test_manifest_mimetype_dan_isi(klien):
    r = klien.get("/manifest.webmanifest")
    assert r.status_code == 200
    assert r.mimetype == "application/manifest+json"
    m = json.loads(r.data)
    ukuran = {i["sizes"] for i in m["icons"]}
    assert {"192x192", "512x512"} <= ukuran  # syarat agar bisa dipasang (installable)
    assert m["display"] == "standalone"


def test_ikon_ada(klien):
    for nama in ["icons/icon-192.png", "icons/icon-512.png", "icons/icon-maskable-512.png"]:
        r = klien.get("/" + nama)
        assert r.status_code == 200 and r.data[:8] == b"\x89PNG\r\n\x1a\n"


def test_service_worker_berisi_semua_aset(klien):
    r = klien.get("/sw.js")
    assert r.status_code == 200
    assert r.headers["Cache-Control"] == "no-cache"
    teks = r.data.decode()
    aset = json.loads(re.search(r"const ASET = (\[.*?\]);", teks, re.DOTALL).group(1))
    for wajib in ["index.html", "js/app.js", "css/style.css", "konten/m2.json", "manifest.webmanifest"]:
        assert wajib in aset
    for rel in aset:
        if rel != "./":
            assert (FRONTEND / rel).is_file(), rel
    assert 'const VERSI = "dev"' not in teks


def test_status(klien):
    d = klien.get("/api/status").get_json()
    assert d["aplikasi"] == "PolaKu" and d["penelitianAktif"] is False


def test_tidak_bisa_keluar_folder(klien):
    assert klien.get("/../server/app.py").status_code == 404
    assert klien.get("/%2e%2e/server/app.py").status_code == 404


def test_penelitian_nonaktif_ditolak(klien):
    r = klien.post("/api/penelitian", json={"kodeSiswa": "S01", "data": {}})
    assert r.status_code == 403


def test_penelitian_menyimpan_data(klien_penelitian):
    klien, folder = klien_penelitian
    kiriman = {"aplikasi": "PolaKu", "kodeSiswa": "s01", "diekspor": "2026-11-12T00:00:00Z",
               "data": {"profil": {"kodeSiswa": "S01"}, "tes": [{"jenis": "awal", "skor": 3, "maks": 6}], "rahasia": "jangan disimpan"}}
    r = klien.post("/api/penelitian", json=kiriman)
    assert r.status_code == 201
    files = list(folder.glob("S01_*.json"))
    assert len(files) == 1
    isi = json.loads(files[0].read_text(encoding="utf-8"))
    assert isi["kodeSiswa"] == "S01"
    assert isi["data"]["tes"][0]["skor"] == 3
    assert "rahasia" not in isi["data"] and "profil" not in isi["data"]


@pytest.mark.parametrize("kode", ["", "TANPA-KODE", "../../x", "Budi Santoso", "S" * 20])
def test_penelitian_kode_tidak_valid(klien_penelitian, kode):
    klien, folder = klien_penelitian
    r = klien.post("/api/penelitian", json={"kodeSiswa": kode, "data": {}})
    assert r.status_code == 400
    assert list(folder.glob("*.json")) == []


def test_penelitian_bukan_json(klien_penelitian):
    klien, _ = klien_penelitian
    assert klien.post("/api/penelitian", data="halo", content_type="text/plain").status_code == 400


def test_semua_modul_tersedia_ikut_cache_offline(klien):
    daftar = json.loads((FRONTEND / "konten" / "modul.json").read_text(encoding="utf-8"))["modul"]
    teks = klien.get("/sw.js").data.decode()
    aset = json.loads(re.search(r"const ASET = (\[.*?\]);", teks, re.DOTALL).group(1))
    for m in daftar:
        if m["tersedia"]:
            assert f"konten/{m['id']}.json" in aset, m["id"]
            assert klien.get(f"/konten/{m['id']}.json").status_code == 200
        assert f"img/modul-{m['id']}.svg" in aset


def test_strategi_cache_sw(klien):
    """Konten: jaringan dulu (+ batas waktu 3 dtk). JS/CSS/gambar: tetap cache dulu."""
    teks = klien.get("/sw.js").data.decode()
    cabang_konten = teks.index('url.pathname.includes("/konten/")')
    cabang_aset = teks.index("caches.match(req, { ignoreSearch: true }).then((tersimpan)")
    assert "event.respondWith(jaringanDulu(req))" in teks[cabang_konten:cabang_aset]
    assert cabang_konten < cabang_aset              # konten ditangani sebelum aturan "cache dulu"
    assert "const BATAS_WAKTU_KONTEN = 3000;" in teks
    assert 'if (url.pathname.includes("/api/")) return;' in teks   # API tetap tidak dicache
