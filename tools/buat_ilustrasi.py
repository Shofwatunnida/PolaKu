"""Membuat ilustrasi & ornamen tema "Pastel Math Wonderland" sebagai file SVG lokal (bisa offline).

Semua pola noktah DIHITUNG oleh kode (bukan digambar tangan), sehingga jumlahnya pasti benar:
  persegi k² (1, 4, 9, 16), segitiga k(k+1)/2 (1, 3, 6, 10), ganjil 2k−1 (1, 3, 5).
Setiap kelompok noktah diberi atribut data-pola, data-suku, dan data-jumlah supaya
tests/test_ilustrasi.py dapat memeriksa kebenarannya secara matematis.
Mata karakter dibuat lengkung (bukan titik) agar tidak terhitung sebagai noktah.

Jalankan:  python tools/buat_ilustrasi.py
"""
from __future__ import annotations

from pathlib import Path

AKAR = Path(__file__).resolve().parent.parent
FOLDER = AKAR / "frontend" / "img"

# Palet pastel (isian) dan warna noktah yang sedikit lebih tua agar tetap terlihat
PINK, PINK_MUDA = "#f472b6", "#fbcfe8"
BIRU, BIRU_MUDA = "#60a5fa", "#bfdbfe"
UNGU, UNGU_MUDA = "#a78bfa", "#ddd6fe"
KUNING, KUNING_MUDA = "#eab308", "#fef08a"
MINT = "#5eead4"
NILA = "#312e81"  # garis wajah & teks


def jumlah_pola(pola: str, k: int) -> int:
    return {"persegi": k * k, "segitiga": k * (k + 1) // 2, "ganjil": 2 * k - 1, "persegi-panjang": k * (k + 1)}[pola]


def posisi(pola: str, k: int, jarak: float) -> list[tuple[float, float]]:
    """Koordinat relatif (kiri-atas = 0,0) setiap noktah untuk suku ke-k."""
    if pola == "persegi":
        return [(c * jarak, r * jarak) for r in range(k) for c in range(k)]
    if pola == "segitiga":
        return [((c + (k - 1 - r) / 2) * jarak, r * jarak) for r in range(k) for c in range(r + 1)]
    if pola == "ganjil":  # bentuk L
        return [(0, r * jarak) for r in range(k)] + [(c * jarak, (k - 1) * jarak) for c in range(1, k)]
    raise ValueError(pola)


def kelompok(pola: str, k: int, x: float, y_bawah: float, jarak: float, r: float, warna: str) -> str:
    """Kelompok noktah suku ke-k, rata bawah pada y_bawah."""
    titik = posisi(pola, k, jarak)
    tinggi = max(p[1] for p in titik)
    lingkaran = "".join(f'<circle class="nk" cx="{x + px:.1f}" cy="{y_bawah - tinggi + py:.1f}" r="{r}"/>' for px, py in titik)
    assert len(titik) == jumlah_pola(pola, k)
    return f'<g data-pola="{pola}" data-suku="{k}" data-jumlah="{len(titik)}" fill="{warna}">{lingkaran}</g>'


def lebar(pola: str, k: int, jarak: float) -> float:
    return max(p[0] for p in posisi(pola, k, jarak))


def wajah(cx: float, cy: float, s: float = 1.0) -> str:
    """Wajah tersenyum: mata lengkung + senyum (tanpa titik)."""
    return (f'<g stroke="{NILA}" stroke-width="{2.4 * s:.1f}" fill="none" stroke-linecap="round">'
            f'<path d="M{cx - 12 * s:.1f} {cy:.1f} q{3.5 * s:.1f} {-5 * s:.1f} {7 * s:.1f} 0"/>'
            f'<path d="M{cx + 5 * s:.1f} {cy:.1f} q{3.5 * s:.1f} {-5 * s:.1f} {7 * s:.1f} 0"/>'
            f'<path d="M{cx - 6 * s:.1f} {cy + 6 * s:.1f} q{6 * s:.1f} {6 * s:.1f} {12 * s:.1f} 0"/></g>')


def bintang(cx: float, cy: float, r: float, warna: str = KUNING_MUDA, garis: str = KUNING) -> str:
    import math
    titik = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.45
        a = -math.pi / 2 + i * math.pi / 5
        titik.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(titik)}" fill="{warna}" stroke="{garis}" stroke-width="1.5" stroke-linejoin="round"/>'


def svg(lebar_vb: float, tinggi_vb: float, isi: str, judul: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {lebar_vb:g} {tinggi_vb:g}" '
            f'width="{lebar_vb:g}" height="{tinggi_vb:g}" role="img" aria-label="{judul}">'
            f'<title>{judul}</title>{isi}</svg>\n')


def deret_pola(pola: str, banyak: int, jarak: float, r: float, warna: list[str], celah: float, x0: float, y_bawah: float) -> tuple[str, float]:
    isi, x = "", x0
    for k in range(1, banyak + 1):
        isi += kelompok(pola, k, x, y_bawah, jarak, r, warna[(k - 1) % len(warna)])
        x += lebar(pola, k, jarak) + celah
    return isi, x - celah


# ---------------------------------------------------------------- ornamen latar
def hias_persegi() -> str:
    isi, kanan = deret_pola("persegi", 4, 12, 4.2, [BIRU, PINK, UNGU, KUNING], 22, 10, 74)
    return svg(round(kanan + 10), 86, isi, "Pola persegi 1, 4, 9, 16")


def hias_segitiga() -> str:
    isi, kanan = deret_pola("segitiga", 4, 12, 4.2, [PINK, UNGU, BIRU, KUNING], 22, 10, 74)
    return svg(round(kanan + 10), 86, isi, "Pola segitiga 1, 3, 6, 10")


def hias_angka() -> str:
    """Persamaan 1 + 2 = 3 dengan angka berwajah (benar secara matematis)."""
    tokoh = [(36, "1", PINK_MUDA, PINK), (118, "2", BIRU_MUDA, BIRU), (200, "3", KUNING_MUDA, KUNING)]
    isi = '<g data-persamaan="1 + 2 = 3">'
    for cx, angka, isian, garis in tokoh:
        isi += (f'<circle cx="{cx}" cy="50" r="32" fill="{isian}" stroke="{garis}" stroke-width="2.5"/>'
                f'<text x="{cx}" y="46" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="28" font-weight="800" fill="{NILA}">{angka}</text>'
                + wajah(cx, 60, 0.85))
    for x, simbol in [(77, "+"), (159, "=")]:
        isi += f'<text x="{x}" y="61" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="28" font-weight="800" fill="{UNGU}">{simbol}</text>'
    isi += "</g>"
    return svg(236, 90, isi, "Angka berwajah: 1 + 2 = 3")


def hias_bentuk() -> str:
    isi = (bintang(26, 26, 16)
           + f'<rect x="58" y="12" width="30" height="30" rx="6" fill="{BIRU_MUDA}" stroke="{BIRU}" stroke-width="2.5" transform="rotate(12 73 27)"/>'
           + f'<polygon points="118,12 136,42 100,42" fill="{PINK_MUDA}" stroke="{PINK}" stroke-width="2.5" stroke-linejoin="round"/>'
           + f'<circle cx="166" cy="28" r="15" fill="{UNGU_MUDA}" stroke="{UNGU}" stroke-width="2.5"/>'
           + f'<path d="M12 72 q16 -14 32 0 t32 0 t32 0 t32 0 t32 0" fill="none" stroke="{MINT}" stroke-width="3" stroke-linecap="round" stroke-dasharray="2 7"/>'
           + bintang(186, 70, 9, PINK_MUDA, PINK))
    return svg(204, 88, isi, "Bentuk geometri dan bintang")


# ---------------------------------------------------------------- ilustrasi beranda
def ilustrasi_beranda() -> str:
    """Tangga pola persegi 1, 4, 9 dan karakter 16 (4×4 noktah) yang tersenyum."""
    isi = f'<ellipse cx="128" cy="150" rx="118" ry="7" fill="{BIRU_MUDA}" opacity=".7"/>'
    x = 14
    for k, warna in [(1, BIRU), (2, UNGU), (3, PINK)]:
        isi += kelompok("persegi", k, x, 138, 13, 4.6, warna)
        isi += f'<text x="{x + lebar("persegi", k, 13) / 2:.1f}" y="{138 - (k - 1) * 13 - 14:.1f}" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="13" font-weight="800" fill="{NILA}">{k * k}</text>'
        x += lebar("persegi", k, 13) + 22
    # karakter 16: kotak membulat berisi 4×4 noktah + wajah di bawahnya
    kx, ky, kw, kh = x - 6, 36, 92, 112
    isi += f'<rect x="{kx}" y="{ky}" width="{kw}" height="{kh}" rx="24" fill="{KUNING_MUDA}" stroke="{KUNING}" stroke-width="2.5"/>'
    jarak = 16
    gx = kx + (kw - 3 * jarak) / 2
    isi += kelompok("persegi", 4, gx, ky + 18 + 3 * jarak, jarak, 5, "#f59e0b")
    isi += wajah(kx + kw / 2, ky + 92, 1.05)
    isi += f'<text x="{kx + kw / 2:.1f}" y="{ky - 8}" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="13" font-weight="800" fill="{NILA}">16</text>'
    isi += bintang(kx + kw + 4, ky + 6, 11)
    isi += bintang(30, 38, 7, PINK_MUDA, PINK)
    return svg(round(kx + kw + 20), 160, isi, "Pola persegi 1, 4, 9, 16")


# ---------------------------------------------------------------- ikon modul (64×64)
def ikon(isi: str, judul: str) -> str:
    return svg(64, 64, isi, judul)


def teks(x, y, t, ukuran=13, warna=NILA, tebal=800):
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="{ukuran}" font-weight="{tebal}" fill="{warna}">{t}</text>'


def ikon_m0():
    isi = ""
    for i, (warna, garis) in enumerate([(BIRU_MUDA, BIRU), (PINK_MUDA, PINK), (KUNING_MUDA, KUNING)]):
        x = 3 + i * 17
        isi += f'<rect x="{x}" y="20" width="14" height="22" rx="4" fill="{warna}" stroke="{garis}" stroke-width="2"/>' + teks(x + 7, 36, i + 1, 12)
    isi += teks(57, 37, "…", 13)
    return ikon(isi, "Barisan 1, 2, 3")


def ikon_m1():
    isi = (f'<circle cx="10" cy="32" r="6" fill="{PINK}"/>'
           f'<polygon points="24,25 31,38 17,38" fill="{BIRU}"/>'
           f'<rect x="35" y="26" width="12" height="12" rx="2" fill="{UNGU}"/>'
           f'<circle cx="55" cy="32" r="6" fill="{PINK}"/>')
    return ikon(isi, "Pola bentuk berulang")


def ikon_m2():
    isi = teks(12, 46, 3, 15) + teks(32, 46, 6, 15) + teks(52, 46, 9, 15)
    for x in (13, 33):
        isi += f'<path d="M{x + 2} 26 q8 -10 16 0" fill="none" stroke="#c2410c" stroke-width="2" stroke-linecap="round"/>'
        isi += teks(x + 10, 15, "+3", 9, "#c2410c")
    return ikon(isi, "Barisan 3, 6, 9 dengan selisih +3")


def ikon_pola(pola: str, warna: list[str], judul: str, jarak=7, r=2.7, celah=10):
    isi, kanan = deret_pola(pola, 3, jarak, r, warna, celah, 0, 0)
    tinggi = max(p[1] for p in posisi(pola, 3, jarak))
    geser_x = (64 - kanan) / 2
    geser_y = 32 + tinggi / 2
    return ikon(f'<g transform="translate({geser_x:.1f} {geser_y:.1f})">{isi}</g>', judul)


def ikon_m6():
    """Persegi Fibonacci 1, 1, 2, 3, 5 menyusun persegi panjang 8 × 5 (luas 40)."""
    u = 7
    kotak = [(0, 0, 5, PINK_MUDA, PINK), (5, 0, 3, BIRU_MUDA, BIRU), (6, 3, 2, UNGU_MUDA, UNGU),
             (5, 3, 1, KUNING_MUDA, KUNING), (5, 4, 1, KUNING_MUDA, KUNING)]
    x0, y0 = (64 - 8 * u) / 2, (64 - 5 * u) / 2
    isi = f'<g data-fibonacci="1,1,2,3,5" data-persegi-panjang="8x5">'
    for x, y, s, isian, garis in kotak:
        isi += f'<rect class="fib" data-sisi="{s}" data-x="{x}" data-y="{y}" x="{x0 + x * u}" y="{y0 + y * u}" width="{s * u}" height="{s * u}" fill="{isian}" stroke="{garis}" stroke-width="1.5"/>'
    isi += "</g>"
    isi += teks(x0 + 2.5 * u, y0 + 2.5 * u + 5, 5, 13) + teks(x0 + 6.5 * u, y0 + 1.5 * u + 4, 3, 11) + teks(x0 + 7 * u, y0 + 4 * u + 3, 2, 9)
    return ikon(isi, "Persegi Fibonacci 1, 1, 2, 3, 5")


def ikon_m7():
    isi = (f'<rect x="6" y="14" width="52" height="36" rx="10" fill="{UNGU_MUDA}" stroke="{UNGU}" stroke-width="2"/>'
           + teks(32, 30, "Uₙ =", 12) + teks(32, 44, "3n + 1", 11, "#6d28d9"))
    return ikon(isi, "Rumus suku ke-n")


def ikon_m8():
    isi = (f'<path d="M8 18 q12 -4 24 2 v30 q-12 -6 -24 -2z" fill="{PINK_MUDA}" stroke="{PINK}" stroke-width="2" stroke-linejoin="round"/>'
           f'<path d="M56 18 q-12 -4 -24 2 v30 q12 -6 24 -2z" fill="{BIRU_MUDA}" stroke="{BIRU}" stroke-width="2" stroke-linejoin="round"/>'
           f'<g stroke="{NILA}" stroke-width="1.6" stroke-linecap="round" opacity=".55"><path d="M13 26 h14"/><path d="M13 32 h14"/><path d="M37 26 h14"/><path d="M37 32 h14"/></g>'
           + bintang(52, 12, 7))
    return ikon(isi, "Buku cerita matematika")


BERKAS = {
    "hias-persegi.svg": hias_persegi,
    "hias-segitiga.svg": hias_segitiga,
    "hias-angka.svg": hias_angka,
    "hias-bentuk.svg": hias_bentuk,
    "beranda.svg": ilustrasi_beranda,
    "modul-m0.svg": ikon_m0,
    "modul-m1.svg": ikon_m1,
    "modul-m2.svg": ikon_m2,
    "modul-m3.svg": lambda: ikon_pola("ganjil", [PINK, UNGU, BIRU], "Pola bilangan ganjil 1, 3, 5"),
    "modul-m4.svg": lambda: ikon_pola("persegi", [BIRU, PINK, UNGU], "Pola persegi 1, 4, 9"),
    "modul-m5.svg": lambda: ikon_pola("segitiga", [UNGU, BIRU, PINK], "Pola segitiga 1, 3, 6"),
    "modul-m6.svg": ikon_m6,
    "modul-m7.svg": ikon_m7,
    "modul-m8.svg": ikon_m8,
}


def main() -> None:
    FOLDER.mkdir(parents=True, exist_ok=True)
    for nama, buat in BERKAS.items():
        (FOLDER / nama).write_text(buat(), encoding="utf-8")
        print("dibuat:", FOLDER / nama)


if __name__ == "__main__":
    main()
