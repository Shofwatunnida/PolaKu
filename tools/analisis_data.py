"""Analisis data penelitian dari file ekspor PolaKu.

Masukan: folder berisi file JSON, baik hasil tombol "Unduh data" di aplikasi maupun kiriman ke server
(data/penelitian/). Jika satu kode siswa punya beberapa file, yang dipakai adalah yang terbaru.

Keluaran (di folder --keluar, bawaan: hasil-analisis/):
- ringkasan_siswa.csv : satu baris per siswa (skor tes, N-gain, skala Paas, petunjuk, literasi)
- jawaban_tes.csv     : jawaban per butir tes (untuk analisis butir/indikator)
- skala_beban.csv     : semua isian skala usaha mental (Paas 1–9)
- refleksi.csv        : penjelasan siswa (untuk dianalisis kualitatif / rubrik)
- ringkasan di layar  : rata-rata N-gain dan kategorinya, rata-rata skala Paas per modul

Jalankan:
    python tools/analisis_data.py data/penelitian
    python tools/analisis_data.py folder-unduhan --keluar hasil
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from statistics import mean

KELOMPOK_LITERASI = {
    "baca_ubah": {"LM1", "LM2"},
    "hitung": {"LM3"},
    "cek_cerita": {"LM4", "LM5"},
    "penalaran": {"LM6", "LM7"},
}


def muat_file(folder: Path) -> dict[str, dict]:
    """Mengembalikan {kodeSiswa: isi_file_terbaru}."""
    per_kode: dict[str, dict] = {}
    # .json dari tombol Unduh/server, .txt dari tombol Bagikan di HP (isinya tetap JSON)
    for p in sorted([*folder.glob("*.json"), *folder.glob("*.txt")]):
        try:
            isi = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            print(f"Lewati {p.name}: bukan JSON yang valid", file=sys.stderr)
            continue
        if isi.get("aplikasi") != "PolaKu" or "data" not in isi:
            print(f"Lewati {p.name}: bukan file data PolaKu", file=sys.stderr)
            continue
        kode = isi.get("kodeSiswa") or "TANPA-KODE"
        waktu = isi.get("diterima") or isi.get("diekspor") or ""
        lama = per_kode.get(kode)
        if lama is None or waktu >= (lama.get("diterima") or lama.get("diekspor") or ""):
            per_kode[kode] = isi
    return per_kode


def n_gain(pre: float | None, post: float | None) -> float | None:
    """N-gain (Hake) dari skor persen 0–100."""
    if pre is None or post is None or pre >= 100:
        return None
    return (post - pre) / (100 - pre)


def kategori_n_gain(g: float | None) -> str:
    if g is None:
        return "-"
    if g >= 0.7:
        return "tinggi"
    if g >= 0.3:
        return "sedang"
    return "rendah"


def tes_terakhir(daftar: list[dict], jenis: str) -> dict | None:
    cocok = [t for t in daftar if t.get("jenis") == jenis]
    return cocok[-1] if cocok else None


def persen(t: dict | None) -> float | None:
    if not t or not t.get("maks"):
        return None
    return 100 * t["skor"] / t["maks"]


def rata(nilai: list[float]) -> float | None:
    return round(mean(nilai), 2) if nilai else None


def ringkas_siswa(kode: str, isi: dict) -> dict:
    d = isi["data"]
    pre, post = tes_terakhir(d.get("tes", []), "awal"), tes_terakhir(d.get("tes", []), "akhir")
    p_pre, p_post = persen(pre), persen(post)
    g = n_gain(p_pre, p_post)

    latihan = [p for p in d.get("percobaan", []) if p.get("mode") == "latihan"]
    pertama = [p for p in latihan if p.get("percobaanKe") == 1]
    soal_unik = {p.get("soalId") for p in latihan}
    # Petunjuk per soal = nilai terbesar yang tercatat untuk soal itu.
    petunjuk_per_soal: dict[str, int] = {}
    for p in latihan:
        petunjuk_per_soal[p.get("soalId")] = max(petunjuk_per_soal.get(p.get("soalId"), 0), p.get("jumlahPetunjuk") or 0)

    paas = d.get("skalaBeban", [])
    baris = {
        "kode_siswa": kode,
        "pretest_skor": pre["skor"] if pre else "",
        "pretest_maks": pre["maks"] if pre else "",
        "pretest_persen": round(p_pre, 1) if p_pre is not None else "",
        "posttest_skor": post["skor"] if post else "",
        "posttest_maks": post["maks"] if post else "",
        "posttest_persen": round(p_post, 1) if p_post is not None else "",
        "n_gain": round(g, 3) if g is not None else "",
        "kategori_n_gain": kategori_n_gain(g),
        "modul_selesai": sum(1 for p in d.get("progres", {}).values() if p.get("status") == "selesai"),
        "soal_latihan_dicoba": len(soal_unik),
        "akurasi_percobaan_pertama": round(sum(1 for p in pertama if p.get("benar")) / len(pertama), 3) if pertama else "",
        "total_petunjuk": sum(petunjuk_per_soal.values()),
        "soal_dilewati": sum(1 for p in latihan if p.get("dilewati")),
        "cek_aturan_dipakai": sum(1 for p in latihan if p.get("cekAturanDipakai")),
        "paas_latihan_rata": rata([p["skor"] for p in paas if p.get("aktivitas") == "latihan"]) or "",
        "paas_kuis_rata": rata([p["skor"] for p in paas if p.get("aktivitas") == "kuis"]) or "",
    }
    lit = [c for c in d.get("literasi", []) if c.get("benar") is not None]
    for nama, proses in KELOMPOK_LITERASI.items():
        relevan = [c for c in lit if proses & set(c.get("proses") or [])]
        # benar pada percobaan pertama (jika tercatat), selaras dengan Profil Literasi di aplikasi
        benar = sum(1 for c in relevan if c.get("benarPertama", c.get("benar")))
        baris[f"literasi_{nama}"] = round(benar / len(relevan), 3) if relevan else ""
    return baris


def tulis_csv(path: Path, baris: list[dict]) -> None:
    if not baris:
        path.write_text("", encoding="utf-8-sig")
        return
    kolom = list(baris[0].keys())
    for b in baris[1:]:
        for k in b:
            if k not in kolom:
                kolom.append(k)
    with path.open("w", newline="", encoding="utf-8-sig") as f:  # utf-8-sig agar rapi dibuka di Excel
        w = csv.DictWriter(f, fieldnames=kolom)
        w.writeheader()
        w.writerows(baris)


def analisis(folder: Path, keluar: Path) -> dict:
    data = muat_file(folder)
    keluar.mkdir(parents=True, exist_ok=True)
    ringkasan = [ringkas_siswa(k, v) for k, v in sorted(data.items())]

    jawaban_tes, skala, refleksi = [], [], []
    for kode, isi in sorted(data.items()):
        d = isi["data"]
        for t in d.get("tes", []):
            for j in t.get("jawaban", []):
                jawaban_tes.append({"kode_siswa": kode, "tes": t.get("jenis"), "waktu_tes": t.get("waktu"), "soal": j.get("soalId"),
                                    "indikator": j.get("indikator") or "", "benar": int(bool(j.get("benar"))), "waktu_ms": j.get("waktuMs", "")})
        for s in d.get("skalaBeban", []):
            skala.append({"kode_siswa": kode, "modul": s.get("modulId"), "aktivitas": s.get("aktivitas"), "skor": s.get("skor"), "waktu": s.get("waktu")})
        for r in d.get("refleksi", []):
            refleksi.append({"kode_siswa": kode, "modul": r.get("modulId"), "teks": r.get("teks"), "waktu": r.get("waktu")})

    tulis_csv(keluar / "ringkasan_siswa.csv", ringkasan)
    tulis_csv(keluar / "jawaban_tes.csv", jawaban_tes)
    tulis_csv(keluar / "skala_beban.csv", skala)
    tulis_csv(keluar / "refleksi.csv", refleksi)

    gains = [r["n_gain"] for r in ringkasan if r["n_gain"] != ""]
    paas_modul: dict[str, list[int]] = {}
    for s in skala:
        paas_modul.setdefault(f"{s['modul']}/{s['aktivitas']}", []).append(s["skor"])
    return {
        "jumlah_siswa": len(ringkasan),
        "rata_n_gain": rata(gains),
        "kategori": kategori_n_gain(mean(gains)) if gains else "-",
        "paas_per_modul": {k: rata(v) for k, v in sorted(paas_modul.items())},
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Analisis data penelitian PolaKu")
    ap.add_argument("folder", type=Path, help="folder berisi file JSON ekspor PolaKu")
    ap.add_argument("--keluar", type=Path, default=Path("hasil-analisis"))
    args = ap.parse_args()
    if not args.folder.is_dir():
        print(f"Folder tidak ditemukan: {args.folder}")
        return 1
    hasil = analisis(args.folder, args.keluar)
    print(f"Jumlah siswa      : {hasil['jumlah_siswa']}")
    print(f"Rata-rata N-gain  : {hasil['rata_n_gain']} ({hasil['kategori']})")
    print("Rata-rata skala usaha mental (1–9):")
    for k, v in hasil["paas_per_modul"].items():
        print(f"  {k:20s} {v}")
    print(f"\nFile CSV disimpan di: {args.keluar.resolve()}")
    print("Catatan: Tes Awal (6 soal diagnostik) dan Tes Akhir (8 soal, termasuk literasi) di aplikasi tidak paralel.\n"
          "Untuk N-gain pada skripsi, gunakan instrumen pretest-posttest paralel yang sudah divalidasi (lihat docs/08).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
