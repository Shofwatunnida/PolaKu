"""Membuat docs/13-kunci-dan-rubrik-modul.md dari file konten.

Tabel kunci jawaban diambil LANGSUNG dari frontend/konten/*.json supaya selalu sama dengan aplikasi.
Rubrik refleksi (jawaban bebas, tidak dinilai otomatis) ditulis di RUBRIK di bawah ini.

Jalankan: python tools/buat_kunci_rubrik.py
"""
from __future__ import annotations

import json
from pathlib import Path

AKAR = Path(__file__).resolve().parent.parent
KONTEN = AKAR / "frontend" / "konten"
KELUAR = AKAR / "docs" / "13-kunci-dan-rubrik-modul.md"

# Rubrik refleksi 0–3 per modul (mengikuti format rubrik di docs/08 §B.5)
RUBRIK = {
    "m0": ["Tidak menjawab atau tidak berkaitan", "Menyebut salah satu (urutan ATAU nilai) tanpa membedakan", "Membedakan urutan dan nilai, tetapi tanpa contoh yang benar", "Membedakan urutan (posisi) dan nilai (bilangan) dengan contoh yang benar"],
    "m2": ["Tidak menjawab atau tidak berkaitan", "Menyebut selisih saja", "Menyebut selisih → koefisien n dan penyesuaian dengan suku pertama", "Langkah lengkap: selisih → kn → sesuaikan dengan U₁ → cek ke suku lain"],
    "m3": ["Tidak menjawab atau tidak berkaitan", "Menulis salah satu rumus (2n atau 2n − 1) tanpa alasan", "Menulis kedua rumus dengan benar tanpa alasan", "Menulis kedua rumus dan alasannya (dua baris noktah / ganjil = genap − 1)"],
    "m4": ["Tidak menjawab atau tidak berkaitan", "Menyebut salah satu pola", "Membedakan n × n dan n × (n + 1)", "Membedakan susunan baris-kolom kedua pola dan menyinggung selisih tingkat dua"],
    "m1": ["Tidak menjawab atau tidak berkaitan", "Menyebut \"cari polanya\" tanpa langkah", "Menyebut satuan pola dan pembagian, tetapi salah menafsirkan sisa", "Langkah lengkap: satuan pola → bagi 100 dengan banyak bentuk → sisa menunjukkan posisi; sisa 0 = bentuk terakhir"],
    "m6": ["Tidak menjawab atau tidak berkaitan", "Menjelaskan salah satu pola saja", "Menjelaskan aturan kedua pola (tambah bilangan tetap vs jumlah dua suku sebelumnya)", "Menjelaskan aturan kedua pola dan akibatnya: selisih pola Fibonacci berubah-ubah"],
    "m5": ["Tidak menjawab atau tidak berkaitan", "Menyebut \"karena setengah\" tanpa penjelasan", "Menjelaskan bahwa dua segitiga membentuk persegi panjang", "Menjelaskan dua segitiga sama besar membentuk persegi panjang n × (n + 1), jadi satu segitiga = n(n + 1)/2"],
}


def kunci_teks(s: dict) -> str:
    t = s["tipe"]
    if t in ("isian-angka", "isian-rumus"):
        return f"{s['jawaban']}" + (f" {s['satuan']}" if s.get("satuan") else "")
    if t == "pilihan-ganda":
        return f"({'abcd'[s['jawaban']]}) {s['pilihan'][s['jawaban']]}"
    if t == "pg-kompleks":
        return ", ".join("B" if p["benar"] else "S" for p in s["pernyataan"])
    if t == "menjodohkan":
        return "; ".join(f"{p['kiri']} → {s['kanan'][p['jawaban']]}" for p in s["pasangan"])
    if t == "lengkapi-tabel":
        return ", ".join(str(k) for k in s["kunciTabel"])
    if t == "klaim":
        return f"{'Setuju' if s['klaimBenar'] else 'Tidak setuju'}; alasan: {s['alasan']['pilihan'][s['alasan']['benar']]}"
    return "(tidak dinilai otomatis)"


def sel(teks: str) -> str:
    return str(teks).replace("|", "\\|").replace("\n", " ").replace("**", "")


def main() -> None:
    daftar = json.loads((KONTEN / "modul.json").read_text(encoding="utf-8"))["modul"]
    baris = [
        "# 13 — Kunci Jawaban dan Rubrik per Modul",
        "",
        "> Dibuat otomatis oleh `python tools/buat_kunci_rubrik.py` dari file konten. **Jangan diedit manual**:",
        "> ubah kontennya (atau `RUBRIK` di skrip), lalu jalankan ulang skrip.",
        "",
        "Semua soal latihan, literasi, dan kuis dinilai otomatis oleh aplikasi dengan kunci di bawah ini.",
        "Kebenaran setiap kunci diuji otomatis (`tests/test_js_logic.py`). Refleksi berupa jawaban bebas,",
        "jadi dinilai peneliti/guru dengan rubrik 0–3.",
        "",
    ]
    for m in daftar:
        if not m["tersedia"]:
            continue
        isi = json.loads((KONTEN / f"{m['id']}.json").read_text(encoding="utf-8"))
        baris += [f"## {m['kode']} · {m['judul']}", ""]
        baris += ["### Latihan", "", "| Id | Tingkat | Soal | Kunci |", "|---|---|---|---|"]
        for s in isi["latihan"]:
            baris.append(f"| {s['id']} | {s.get('tingkat', '')} | {sel(s['pertanyaan'])} | {sel(kunci_teks(s))} |")
        for st in isi["literasi"]:
            baris += ["", f"### Literasi: {st['judul']} (tahap {st['tahapSiklus']}, konteks {st['konteks']})", "",
                      "| Id | Level | Proses | Soal | Kunci | Pembahasan |", "|---|---|---|---|---|---|"]
            for s in st["soal"]:
                baris.append(f"| {s['id']} | {s['level']} | {', '.join(s['proses'])} | {sel(s['pertanyaan'])} | {sel(kunci_teks(s))} | {sel(s.get('pembahasan', '—'))} |")
        baris += ["", "### Kuis", "", "| Id | Soal | Kunci | Pembahasan |", "|---|---|---|---|"]
        for s in isi["kuis"]:
            baris.append(f"| {s['id']} | {sel(s['pertanyaan'])} | {sel(kunci_teks(s))} | {sel(s.get('pembahasan', '—'))} |")
        r = isi["refleksi"]
        baris += ["", "### Rubrik Refleksi", "", f"Pertanyaan: *{sel(r['pertanyaan'])}*", "",
                  f"Contoh jawaban lengkap: {sel(r['contohPenjelasan'])}", "", "| Skor | Kriteria |", "|---|---|"]
        rub = RUBRIK.get(m["id"])
        if rub:
            for skor, k in enumerate(rub):
                baris.append(f"| {skor} | {k} |")
        else:
            baris.append("| — | Rubrik belum ditulis |")
        baris.append("")
    KELUAR.write_text("\n".join(baris) + "\n", encoding="utf-8")
    print("dibuat:", KELUAR)


if __name__ == "__main__":
    main()
