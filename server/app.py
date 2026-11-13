"""Server PolaKu (Flask).

Fungsi:
1. Menyajikan aplikasi web (folder frontend/) dengan header yang benar untuk PWA.
2. Memperbarui daftar aset offline (sw.js) dan memvalidasi konten setiap kali dinyalakan.
3. (Opsional, untuk penelitian) menerima kiriman data anonim dari siswa jika diaktifkan
   dengan variabel lingkungan POLAKU_PENELITIAN=1. Data disimpan di data/penelitian/.

Menjalankan (dari folder aplikasi-pola-bilangan):
    python server/app.py                      # http://localhost:5000
    python server/app.py --host 0.0.0.0       # bisa dibuka dari HP di jaringan Wi-Fi yang sama
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, abort, jsonify, request, send_from_directory

AKAR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AKAR))

from tools.build_aset import perbarui_sw  # noqa: E402
from tools.validasi_konten import validasi_semua  # noqa: E402

FRONTEND = AKAR / "frontend"
POLA_KODE = re.compile(r"^[A-Z0-9-]{1,12}$")


def buat_app(penelitian_aktif: bool | None = None, folder_data: Path | None = None, frontend: Path = FRONTEND) -> Flask:
    app = Flask(__name__, static_folder=None)
    app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 MB per kiriman
    app.config["PENELITIAN_AKTIF"] = (os.environ.get("POLAKU_PENELITIAN") == "1") if penelitian_aktif is None else penelitian_aktif
    app.config["FOLDER_DATA"] = folder_data or (AKAR / "data" / "penelitian")
    versi = perbarui_sw(frontend)

    @app.after_request
    def header_keamanan(resp):
        resp.headers.setdefault("X-Content-Type-Options", "nosniff")
        resp.headers.setdefault("Referrer-Policy", "no-referrer")
        resp.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        resp.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; media-src 'self' blob:; "
            "connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'",
        )
        return resp

    @app.get("/api/status")
    def status():
        return jsonify({"aplikasi": "PolaKu", "versi": versi, "penelitianAktif": app.config["PENELITIAN_AKTIF"]})

    @app.post("/api/penelitian")
    def terima_data():
        if not app.config["PENELITIAN_AKTIF"]:
            return jsonify({"pesan": "Pengiriman data penelitian tidak diaktifkan di server ini."}), 403
        isi = request.get_json(silent=True)
        if not isinstance(isi, dict) or not isinstance(isi.get("data"), dict):
            return jsonify({"pesan": "Format data tidak valid."}), 400
        kode = str(isi.get("kodeSiswa", "")).strip().upper()
        if not POLA_KODE.match(kode) or kode == "TANPA-KODE":
            return jsonify({"pesan": "Kode siswa tidak valid. Gunakan huruf/angka, mis. S01."}), 400
        # Simpan hanya bagian yang dibutuhkan penelitian (tanpa data lain dari perangkat).
        data = isi["data"]
        bersih = {
            "aplikasi": "PolaKu",
            "kodeSiswa": kode,
            "diterima": datetime.now(timezone.utc).isoformat(),
            "diekspor": isi.get("diekspor"),
            "data": {k: data.get(k, [] if k != "progres" else {}) for k in ["progres", "percobaan", "literasi", "skalaBeban", "refleksi", "tes"]},
        }
        folder: Path = app.config["FOLDER_DATA"]
        folder.mkdir(parents=True, exist_ok=True)
        nama = f"{kode}_{datetime.now().strftime('%Y%m%d-%H%M%S-%f')}.json"
        (folder / nama).write_text(json.dumps(bersih, ensure_ascii=False, indent=2), encoding="utf-8")
        return jsonify({"pesan": "Tersimpan.", "file": nama}), 201

    @app.get("/")
    def beranda():
        return send_from_directory(frontend, "index.html")

    @app.get("/<path:jalur>")
    def berkas(jalur: str):
        if jalur.startswith("api/"):
            abort(404)
        resp = send_from_directory(frontend, jalur)
        if jalur == "sw.js":
            resp.headers["Cache-Control"] = "no-cache"
            resp.headers["Service-Worker-Allowed"] = "/"
        elif jalur.endswith(".webmanifest"):
            resp.mimetype = "application/manifest+json"
        return resp

    return app


def alamat_lan() -> str | None:
    """IP laptop di jaringan Wi-Fi (untuk dibuka dari HP). Tidak mengirim data apa pun."""
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except OSError:
        return None
    finally:
        s.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Server PolaKu")
    parser.add_argument("--host", default="127.0.0.1", help="0.0.0.0 agar bisa diakses dari perangkat lain di jaringan yang sama")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", 5000)))
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    lap = validasi_semua()
    for p in lap.peringatan:
        print("PERINGATAN konten:", p)
    for k in lap.kesalahan:
        print("KESALAHAN konten:", k)

    app = buat_app()
    print(f"PolaKu berjalan di http://localhost:{args.port}")
    if args.host == "0.0.0.0":
        ip = alamat_lan()
        if ip:
            print(f"Buka dari HP (Wi-Fi yang sama): http://{ip}:{args.port}")
        print("  Catatan: lewat alamat http ini, tombol pasang & mode offline tidak aktif (butuh HTTPS).")
        print("  Untuk mencobanya di HP Android, pakai USB + port forwarding (lihat docs/12, bagian 1).")
    print("Pengiriman data penelitian:", "AKTIF" if app.config["PENELITIAN_AKTIF"] else "nonaktif (aktifkan dengan POLAKU_PENELITIAN=1)")
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
