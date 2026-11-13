"""Service worker: pembaruan konten harus terlihat pada pemuatan PERTAMA, dan konten tetap bisa dipakai offline.

Uji memakai SALINAN folder frontend di folder sementara (folder proyek tidak diubah),
lalu mensimulasikan pembaruan konten seperti setelah gelombang 1 & 2:
  sebelum perbaikan, modul baru tetap tampil "Segera hadir" pada muat ulang pertama
  (dan selamanya jika daftar aset tidak dibangun ulang).
"""
import json
import os
import shutil
import tempfile
import threading
import time
from pathlib import Path

import pytest

sync_api = pytest.importorskip("playwright.sync_api")
from werkzeug.serving import make_server  # noqa: E402

from server.app import buat_app  # noqa: E402
from tools.build_aset import perbarui_sw  # noqa: E402

# POLAKU_FRONTEND_UJI: hanya untuk membuktikan uji ini gagal pada versi sw.js lama
FRONTEND = Path(os.environ.get("POLAKU_FRONTEND_UJI") or Path(__file__).resolve().parents[2] / "frontend")


class Lambat:
    """Middleware WSGI: memperlambat respons konten/ untuk menguji batas waktu 3 detik."""

    def __init__(self, app):
        self.app, self.detik = app, 0

    def __call__(self, environ, start_response):
        if self.detik and environ.get("PATH_INFO", "").startswith("/konten/"):
            time.sleep(self.detik)
        return self.app(environ, start_response)


@pytest.fixture
def situs(tmp_path):
    fe = tmp_path / "frontend"
    shutil.copytree(FRONTEND, fe)
    modul = fe / "konten" / "modul.json"
    baru = json.loads(modul.read_text(encoding="utf-8"))
    lama = json.loads(json.dumps(baru))
    for m in lama["modul"]:
        m["tersedia"] = m["id"] in ("m2", "m4")         # keadaan sebelum gelombang 1
    modul.write_text(json.dumps(lama, ensure_ascii=False), encoding="utf-8")
    perbarui_sw(fe)
    app = Lambat(buat_app(penelitian_aktif=False, folder_data=tmp_path / "data", frontend=fe))
    srv = make_server("127.0.0.1", 0, app, threaded=True)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield {"alamat": f"http://127.0.0.1:{srv.server_port}", "fe": fe, "modul": modul, "baru": baru, "app": app}
    srv.shutdown()


@pytest.fixture
def browser_tetap():
    """Profil browser yang bertahan antar-muat-ulang (service worker & cache tetap ada)."""
    with sync_api.sync_playwright() as p:
        profil = tempfile.mkdtemp()
        ctx = p.chromium.launch_persistent_context(profil, channel="msedge", headless=True)
        yield ctx
        ctx.close()
        shutil.rmtree(profil, ignore_errors=True)


def status_peta(page, judul):
    page.locator(".peta-item").first.wait_for()
    return "segera" if "Segera hadir" in page.locator(".peta-item", has_text=judul).inner_text() else "buka"


def siapkan_versi_lama(page, s):
    page.goto(s["alamat"] + "/#/peta")
    page.evaluate("localStorage.setItem('polaku:nama', 'Kiara')")
    page.evaluate("localStorage.setItem('polaku:v1', JSON.stringify({progres: {m2: {status: 'selesai', tahapSelesai: ['konsep']}}}))")
    page.reload()
    for _ in range(30):
        if page.evaluate("!!navigator.serviceWorker.controller"):
            break
        page.wait_for_timeout(200)
        page.reload()
    assert page.evaluate("!!navigator.serviceWorker.controller"), "service worker belum aktif"
    page.goto(s["alamat"] + "/#/peta")
    assert status_peta(page, "Pengingat Prasyarat") == "segera"


def test_pembaruan_konten_muncul_pada_muat_ulang_pertama(situs, browser_tetap):
    s, page = situs, browser_tetap.new_page()
    siapkan_versi_lama(page, s)
    # Pembaruan seperti gelombang 1 & 2, termasuk sw.js versi baru
    s["modul"].write_text(json.dumps(s["baru"], ensure_ascii=False), encoding="utf-8")
    perbarui_sw(s["fe"])
    page.reload()
    for judul in ["Pengingat Prasyarat", "Mengenal Pola", "Pola Bilangan Ganjil dan Genap", "Pola Segitiga", "Pola Fibonacci"]:
        assert status_peta(page, judul) == "buka", f"{judul} masih 'Segera hadir' pada muat ulang pertama"
    # data siswa tidak tersentuh
    assert page.evaluate("localStorage.getItem('polaku:nama')") == "Kiara"
    assert page.evaluate("JSON.parse(localStorage.getItem('polaku:v1')).progres.m2.status") == "selesai"


def test_pembaruan_konten_tanpa_build_aset_tetap_muncul(situs, browser_tetap):
    """Kasus terburuk: modul.json diubah tetapi daftar aset (sw.js) lupa dibangun ulang."""
    s, page = situs, browser_tetap.new_page()
    siapkan_versi_lama(page, s)
    sw_sebelum = (s["fe"] / "sw.js").read_text(encoding="utf-8")
    s["modul"].write_text(json.dumps(s["baru"], ensure_ascii=False), encoding="utf-8")
    assert (s["fe"] / "sw.js").read_text(encoding="utf-8") == sw_sebelum   # sw.js memang tidak berubah
    page.reload()
    assert page.evaluate("!!navigator.serviceWorker.controller")          # tetap lewat service worker
    assert status_peta(page, "Pengingat Prasyarat") == "buka"


def test_konten_tetap_bisa_dipakai_saat_offline(situs, browser_tetap):
    s, page = situs, browser_tetap.new_page()
    siapkan_versi_lama(page, s)
    s["modul"].write_text(json.dumps(s["baru"], ensure_ascii=False), encoding="utf-8")
    perbarui_sw(s["fe"])
    page.reload()
    assert status_peta(page, "Pengingat Prasyarat") == "buka"
    page.wait_for_timeout(500)   # beri waktu cache diperbarui dengan versi terbaru
    browser_tetap.set_offline(True)
    page.reload()
    assert status_peta(page, "Pengingat Prasyarat") == "buka", "offline harus memakai versi konten terakhir dari cache"
    page.goto(s["alamat"] + "/#/modul/m2/konsep")
    page.get_by_role("heading", name="Barisan dan suku").wait_for()
    assert page.locator("#status-offline").is_visible()
    browser_tetap.set_offline(False)


def test_jaringan_lambat_memakai_cache_setelah_batas_waktu(situs, browser_tetap):
    s, page = situs, browser_tetap.new_page()
    siapkan_versi_lama(page, s)
    s["app"].detik = 8            # server konten sangat lambat
    mulai = time.monotonic()
    page.reload()
    page.locator(".peta-item").first.wait_for(timeout=7000)
    lama = time.monotonic() - mulai
    assert lama < 6.5, f"konten harus muncul dari cache setelah ±3 detik, tetapi butuh {lama:.1f} detik"
    assert status_peta(page, "Pola dengan Selisih Tetap") == "buka"
    s["app"].detik = 0
