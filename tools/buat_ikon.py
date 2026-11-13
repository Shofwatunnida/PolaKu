"""Membuat ikon aplikasi (PNG & SVG) tanpa pustaka tambahan.

Ikon: latar biru membulat dengan noktah pola persegi 3 x 3 (noktah tambahan berwarna oranye).

Jalankan:  python tools/buat_ikon.py
"""
from __future__ import annotations

import struct
import zlib
from pathlib import Path

AKAR = Path(__file__).resolve().parent.parent
FOLDER_IKON = AKAR / "frontend" / "icons"

BIRU = (37, 99, 235, 255)
PUTIH = (255, 255, 255, 255)
ORANYE = (251, 146, 60, 255)
TRANSPARAN = (0, 0, 0, 0)


def tulis_png(path: Path, lebar: int, tinggi: int, piksel: list[list[tuple[int, int, int, int]]]) -> None:
    """Menulis gambar RGBA ke file PNG (format paling dasar, tanpa kompresi khusus)."""
    mentah = bytearray()
    for baris in piksel:
        mentah.append(0)  # filter: none
        for r, g, b, a in baris:
            mentah += bytes((r, g, b, a))

    def potongan(jenis: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + jenis + data + struct.pack(">I", zlib.crc32(jenis + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", lebar, tinggi, 8, 6, 0, 0, 0)
    isi = b"\x89PNG\r\n\x1a\n" + potongan(b"IHDR", ihdr) + potongan(b"IDAT", zlib.compress(bytes(mentah), 9)) + potongan(b"IEND", b"")
    path.write_bytes(isi)


def gambar_ikon(ukuran: int, maskable: bool) -> list[list[tuple[int, int, int, int]]]:
    """maskable=True: latar penuh, isi di zona aman 80% (aturan ikon maskable Android)."""
    radius_sudut = 0 if maskable else ukuran * 0.22
    skala_isi = 0.55 if maskable else 0.68
    pusat = ukuran / 2
    jarak = ukuran * skala_isi / 3
    r_noktah = jarak * 0.32
    awal = pusat - jarak  # pusat noktah kiri atas
    # Noktah "baru" (oranye) = baris & kolom ke-3, seperti pola persegi gambar 2 -> 3
    noktah = [(awal + c * jarak, awal + r * jarak, ORANYE if (r == 2 or c == 2) else PUTIH)
              for r in range(3) for c in range(3)]

    piksel = []
    for y in range(ukuran):
        baris = []
        for x in range(ukuran):
            px, py = x + 0.5, y + 0.5
            # latar dengan sudut membulat
            warna = BIRU
            if radius_sudut:
                dx = max(radius_sudut - px, 0, px - (ukuran - radius_sudut))
                dy = max(radius_sudut - py, 0, py - (ukuran - radius_sudut))
                if dx * dx + dy * dy > radius_sudut * radius_sudut:
                    warna = TRANSPARAN
            if warna != TRANSPARAN:
                for nx, ny, w in noktah:
                    if (px - nx) ** 2 + (py - ny) ** 2 <= r_noktah ** 2:
                        warna = w
                        break
            baris.append(warna)
        piksel.append(baris)
    return piksel


SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="22" fill="#2563eb"/>
  <g fill="#fff">
    <circle cx="27" cy="27" r="7"/><circle cx="50" cy="27" r="7"/>
    <circle cx="27" cy="50" r="7"/><circle cx="50" cy="50" r="7"/>
  </g>
  <g fill="#fb923c">
    <circle cx="73" cy="27" r="7"/><circle cx="73" cy="50" r="7"/>
    <circle cx="27" cy="73" r="7"/><circle cx="50" cy="73" r="7"/><circle cx="73" cy="73" r="7"/>
  </g>
</svg>
"""


def main() -> None:
    FOLDER_IKON.mkdir(parents=True, exist_ok=True)
    for ukuran, nama, maskable in [(192, "icon-192.png", False), (512, "icon-512.png", False), (512, "icon-maskable-512.png", True)]:
        tulis_png(FOLDER_IKON / nama, ukuran, ukuran, gambar_ikon(ukuran, maskable))
        print("dibuat:", FOLDER_IKON / nama)
    (FOLDER_IKON / "icon.svg").write_text(SVG, encoding="utf-8")
    print("dibuat:", FOLDER_IKON / "icon.svg")


if __name__ == "__main__":
    main()
