"""Memperbarui daftar aset offline di frontend/sw.js.

Service worker hanya memasang ulang cache jika isi sw.js berubah. Skrip ini menghitung hash
dari semua file frontend, lalu menulis VERSI dan ASET baru di antara penanda
// <<ASET-MULAI>> dan // <<ASET-SELESAI>> di sw.js.

Jalankan setiap kali selesai mengubah file frontend, sebelum deploy:
    python tools/build_aset.py
(Server Flask menjalankannya otomatis saat dinyalakan.)
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

AKAR = Path(__file__).resolve().parent.parent
FRONTEND = AKAR / "frontend"
SW = FRONTEND / "sw.js"

# File yang tidak perlu di-cache
DIKECUALIKAN = {"sw.js"}
EKSTENSI = {".html", ".css", ".js", ".json", ".webmanifest", ".png", ".svg", ".ico", ".mp4", ".webm", ".vtt", ".woff2"}

POLA_BLOK = re.compile(r"// <<ASET-MULAI>>.*?// <<ASET-SELESAI>>", re.DOTALL)


def daftar_aset(frontend: Path = FRONTEND) -> list[str]:
    hasil = []
    for p in sorted(frontend.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in EKSTENSI:
            continue
        rel = p.relative_to(frontend).as_posix()
        if rel in DIKECUALIKAN:
            continue
        hasil.append(rel)
    return hasil


def hitung_versi(aset: list[str], frontend: Path = FRONTEND) -> str:
    h = hashlib.sha256()
    for rel in aset:
        h.update(rel.encode())
        h.update((frontend / rel).read_bytes())
    return h.hexdigest()[:12]


def perbarui_sw(frontend: Path = FRONTEND) -> str:
    sw = frontend / "sw.js"
    aset = daftar_aset(frontend)
    versi = hitung_versi(aset, frontend)
    blok = (
        "// <<ASET-MULAI>>\n"
        f"const VERSI = {json.dumps(versi)};\n"
        f"const ASET = {json.dumps(['./'] + aset, ensure_ascii=False, indent=2)};\n"
        "// <<ASET-SELESAI>>"
    )
    isi = sw.read_text(encoding="utf-8")
    if not POLA_BLOK.search(isi):
        raise RuntimeError("Penanda <<ASET-MULAI>> / <<ASET-SELESAI>> tidak ditemukan di sw.js")
    baru = POLA_BLOK.sub(lambda _: blok, isi)
    if baru != isi:
        sw.write_text(baru, encoding="utf-8")
    return versi


if __name__ == "__main__":
    v = perbarui_sw()
    print(f"sw.js diperbarui: versi {v}, {len(daftar_aset())} aset")
