"""Validasi file konten (frontend/konten/*.json) terhadap struktur dan aturan pedagogis.

Aturan yang diperiksa (lihat CLAUDE.md bagian 5):
- Satu segmen konsep maksimal 3 kalimat.
- Setiap soal latihan punya 3 petunjuk dan umpan balik umum.
- Kunci jawaban konsisten (rumus cocok dengan pola, indeks pilihan valid, dst.).
- Stimulus literasi: 3–4 soal berjenjang L1 -> L3, label proses LM1–LM7,
  panjang teks <= 60 kata (L1–L2) atau <= 120 kata (ada L3).
- Minimal satu soal penalaran (LM6) per modul.

Jalankan:  python tools/validasi_konten.py
Keluar dengan kode 1 jika ada KESALAHAN (peringatan tidak menggagalkan).
"""
from __future__ import annotations

import ast
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

AKAR = Path(__file__).resolve().parent.parent
KONTEN = AKAR / "frontend" / "konten"

TIPE_SOAL = {"isian-angka", "isian-rumus", "pilihan-ganda", "pg-kompleks", "menjodohkan", "lengkapi-tabel", "klaim", "uraian-singkat"}
PROSES = {f"LM{i}" for i in range(1, 8)}
LEVEL = ["L1", "L2", "L3"]
KONTEKS = {"personal", "sosial-budaya", "saintifik"}


@dataclass
class Laporan:
    kesalahan: list[str] = field(default_factory=list)
    peringatan: list[str] = field(default_factory=list)

    def salah(self, lokasi: str, pesan: str) -> None:
        self.kesalahan.append(f"{lokasi}: {pesan}")

    def awas(self, lokasi: str, pesan: str) -> None:
        self.peringatan.append(f"{lokasi}: {pesan}")


# ---------- Evaluator rumus (aman, tanpa eval bebas) ----------

def _normalisasi_rumus(teks: str) -> str:
    s = str(teks).lower().strip()
    s = re.sub(r"^(u\s*_?\s*n|un)\s*=\s*", "", s)
    s = s.replace(" ", "").replace("×", "*").replace("x", "*").replace("−", "-").replace("²", "^2").replace(",", ".")
    s = re.sub(r"(\d)(n|\()", r"\1*\2", s)   # 3n -> 3*n, 2( -> 2*(
    s = re.sub(r"(n|\))(\(|n|\d)", r"\1*\2", s)  # n( -> n*(, )( -> )*(
    return s.replace("^", "**")


_NODE_AMAN = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant, ast.Name, ast.Load,
              ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.UAdd)


def hitung_rumus(teks: str, n: float) -> float:
    pohon = ast.parse(_normalisasi_rumus(teks), mode="eval")
    for node in ast.walk(pohon):
        if not isinstance(node, _NODE_AMAN):
            raise ValueError(f"rumus tidak valid: {teks}")
        if isinstance(node, ast.Name) and node.id != "n":
            raise ValueError(f"variabel tidak dikenal: {node.id}")
    return eval(compile(pohon, "<rumus>", "eval"), {"__builtins__": {}}, {"n": n})  # noqa: S307 (sudah dibatasi node-nya)


def rumus_cocok_pola(rumus: str, pola: list[float]) -> bool:
    return all(abs(hitung_rumus(rumus, i + 1) - s) < 1e-9 for i, s in enumerate(pola))


# ---------- Bantuan teks ----------

def hitung_kalimat(teks: str) -> int:
    bersih = re.sub(r"\*\*", "", teks)
    potong = [k for k in re.split(r"(?<=[.!?])\s+", bersih.strip()) if k.strip()]
    return len(potong)


def hitung_kata(teks: str) -> int:
    return len(re.findall(r"\S+", teks.replace("**", "")))


# ---------- Validasi soal ----------

BENTUK = {"lingkaran", "segitiga", "persegi", "bintang", "garis"}
WARNA = {"pink", "biru", "ungu", "kuning", "merah", "hijau"}


def cek_visual(v: dict | None, loc: str, lap: Laporan) -> None:
    if not v or v.get("jenis") != "bentuk":
        return
    for butir in v.get("deret", []):
        bagian = str(butir).split("-")
        if len(bagian) != 2 or bagian[0] not in BENTUK or bagian[1] not in WARNA:
            lap.salah(loc, f"butir deret bentuk tidak dikenal: {butir!r} (format: bentuk-warna)")


def cek_verifikasi_pola(s: dict, loc: str, lap: Laporan) -> None:
    """Menghitung ulang kunci soal pola berulang dari 'satuan' pola (bukan menebak dari teks)."""
    vp = s.get("verifikasiPola")
    if not vp:
        return
    satuan = vp["satuan"]
    # deret yang ditampilkan harus benar-benar mengulang satuan itu
    v = s.get("visual")
    if v and v.get("jenis") == "bentuk":
        for i, butir in enumerate(v["deret"]):
            if satuan[i % len(satuan)] not in butir.split("-"):
                lap.salah(loc, f"deret ke-{i + 1} ({butir}) tidak sesuai satuan pola {satuan}")
    if "ke" in vp:
        harapan = satuan[(vp["ke"] - 1) % len(satuan)]
        if s["tipe"] == "pilihan-ganda":
            dipilih = s["pilihan"][s["jawaban"]].lower()
            if dipilih != harapan:
                lap.salah(loc, f"bentuk ke-{vp['ke']} seharusnya {harapan}, tetapi kunci memilih {dipilih}")
    if "hitung" in vp:
        harapan = sum(1 for i in range(vp["dari"]) if satuan[i % len(satuan)] == vp["hitung"])
        if s.get("jawaban") != harapan:
            lap.salah(loc, f"banyak {vp['hitung']} dalam {vp['dari']} butir seharusnya {harapan}, kunci {s.get('jawaban')}")


def validasi_soal(s: dict, lokasi: str, lap: Laporan, butuh_petunjuk: bool) -> None:
    loc = f"{lokasi}/{s.get('id', '?')}"
    cek_visual(s.get("visual"), loc, lap)
    cek_verifikasi_pola(s, loc, lap)
    tipe = s.get("tipe")
    if tipe not in TIPE_SOAL:
        lap.salah(loc, f"tipe soal tidak dikenal: {tipe!r}")
        return
    if not s.get("id"):
        lap.salah(loc, "soal tanpa id")
    if not s.get("pertanyaan"):
        lap.salah(loc, "pertanyaan kosong")

    if butuh_petunjuk:
        p = s.get("petunjuk", [])
        if len(p) != 3:
            lap.salah(loc, f"harus punya tepat 3 petunjuk bertingkat (ada {len(p)})")
        if not s.get("umpanBalikUmum"):
            lap.salah(loc, "tidak ada umpanBalikUmum")

    if tipe == "isian-angka":
        if not isinstance(s.get("jawaban"), (int, float)):
            lap.salah(loc, "jawaban isian-angka harus berupa angka")
        for u in s.get("umpanBalik", []):
            if u.get("jawaban") == s.get("jawaban"):
                lap.salah(loc, "umpan balik salah memakai jawaban yang benar")
    elif tipe == "isian-rumus":
        try:
            hitung_rumus(s["jawaban"], 1)
        except Exception as e:  # noqa: BLE001
            lap.salah(loc, f"kunci rumus tidak bisa dihitung: {e}")
            return
        if s.get("pola") and not rumus_cocok_pola(s["jawaban"], s["pola"]):
            lap.salah(loc, f"kunci rumus {s['jawaban']!r} tidak cocok dengan pola {s['pola']}")
        for u in s.get("umpanBalik", []):
            try:
                if s.get("pola") and rumus_cocok_pola(u["jawaban"], s["pola"]):
                    lap.salah(loc, f"umpan balik untuk {u['jawaban']!r} padahal rumus itu benar")
            except Exception:  # noqa: BLE001
                lap.salah(loc, f"rumus di umpan balik tidak valid: {u.get('jawaban')!r}")
    elif tipe == "pilihan-ganda":
        pil = s.get("pilihan", [])
        if len(pil) < 2:
            lap.salah(loc, "pilihan ganda butuh minimal 2 pilihan")
        if not isinstance(s.get("jawaban"), int) or not 0 <= s["jawaban"] < len(pil):
            lap.salah(loc, "indeks jawaban di luar daftar pilihan")
        for u in s.get("umpanBalik", []):
            if u.get("jawaban") == s.get("jawaban"):
                lap.salah(loc, "umpan balik salah memakai indeks jawaban yang benar")
    elif tipe == "pg-kompleks":
        per = s.get("pernyataan", [])
        if len(per) < 2:
            lap.salah(loc, "PG kompleks butuh minimal 2 pernyataan")
        for i, p in enumerate(per):
            if not isinstance(p.get("benar"), bool):
                lap.salah(loc, f"pernyataan {i + 1} tidak punya nilai benar (true/false)")
    elif tipe == "menjodohkan":
        kanan = s.get("kanan", [])
        jaw = [p.get("jawaban") for p in s.get("pasangan", [])]
        if any(not isinstance(j, int) or not 0 <= j < len(kanan) for j in jaw):
            lap.salah(loc, "indeks pasangan di luar daftar kanan")
        if len(set(jaw)) != len(jaw):
            lap.salah(loc, "dua item kiri memakai pasangan yang sama")
    elif tipe == "lengkapi-tabel":
        kosong = sum(1 for baris in s.get("tabel", {}).get("baris", []) for c in baris if c is None)
        if kosong != len(s.get("kunciTabel", [])):
            lap.salah(loc, f"jumlah sel kosong ({kosong}) tidak sama dengan jumlah kunciTabel ({len(s.get('kunciTabel', []))})")
    elif tipe == "klaim":
        if not isinstance(s.get("klaimBenar"), bool):
            lap.salah(loc, "klaimBenar harus true/false")
        al = s.get("alasan", {})
        if not isinstance(al.get("benar"), int) or not 0 <= al["benar"] < len(al.get("pilihan", [])):
            lap.salah(loc, "indeks alasan benar tidak valid")
        if not s.get("tokoh") or not s.get("klaim"):
            lap.salah(loc, "soal klaim butuh tokoh dan klaim")


# ---------- Validasi modul ----------

def validasi_modul(m: dict, nama: str, lap: Laporan) -> None:
    hilang = [k for k in ["id", "kode", "judul", "tujuan", "segmen", "contohLengkap", "contohSetengahJadi", "latihan", "literasi", "refleksi", "kuis"] if k not in m]
    for kunci in hilang:
        lap.salah(nama, f"kunci '{kunci}' tidak ada")
    if hilang:
        return

    for seg in m["segmen"]:
        loc = f"{nama}/segmen/{seg.get('id')}"
        cek_visual(seg.get("visual"), loc, lap)
        jml = sum(hitung_kalimat(t) for t in seg.get("teks", []))
        if jml > 3:
            lap.salah(loc, f"{jml} kalimat; maksimal 3 kalimat per segmen (aturan segmenting)")
        for t in seg.get("teks", []):
            for k in re.split(r"(?<=[.!?])\s+", t):
                if hitung_kata(k) > 15:
                    lap.awas(loc, f"kalimat lebih dari 15 kata: \"{k[:50]}…\"")

    for c in m["contohLengkap"] + m["contohSetengahJadi"]:
        cek_visual(c.get("visual"), f"{nama}/contoh/{c.get('id')}", lap)
        for l in c.get("langkah", []):
            cek_visual(l.get("visual"), f"{nama}/contoh/{c.get('id')}", lap)
    for c in m["contohLengkap"]:
        if len(c.get("langkah", [])) < 2:
            lap.salah(f"{nama}/contohLengkap/{c.get('id')}", "contoh lengkap butuh minimal 2 langkah")
    jumlah_kosong = []
    for c in m["contohSetengahJadi"]:
        loc = f"{nama}/contohSetengahJadi/{c.get('id')}"
        kosong = [l["kosong"] for l in c.get("langkah", []) if l.get("kosong")]
        jumlah_kosong.append(len(kosong))
        if not kosong:
            lap.salah(loc, "contoh setengah jadi tidak punya langkah kosong")
        for k in kosong:
            if k.get("tipe") not in {"isian-angka", "isian-rumus"}:
                lap.salah(loc, f"tipe langkah kosong tidak didukung: {k.get('tipe')}")
    if jumlah_kosong != sorted(jumlah_kosong):
        lap.awas(f"{nama}/contohSetengahJadi", "langkah kosong sebaiknya bertambah (fading): " + str(jumlah_kosong))

    if not m["latihan"]:
        lap.salah(nama, "latihan kosong")
    for s in m["latihan"]:
        validasi_soal(s, f"{nama}/latihan", lap, butuh_petunjuk=True)
    if not m["kuis"]:
        lap.salah(nama, "kuis kosong")
    for s in m["kuis"]:
        validasi_soal(s, f"{nama}/kuis", lap, butuh_petunjuk=False)

    ada_penalaran = False
    for st in m["literasi"]:
        loc = f"{nama}/literasi/{st.get('id')}"
        if st.get("konteks") not in KONTEKS:
            lap.salah(loc, f"konteks harus salah satu dari {sorted(KONTEKS)}")
        cek_visual(st.get("visual"), loc, lap)
        if st.get("tahapSiklus") not in {"A", "B", "C"}:
            lap.salah(loc, "tahapSiklus harus A, B, atau C")
        soal = st.get("soal", [])
        if not 3 <= len(soal) <= 4:
            lap.salah(loc, f"satu stimulus berisi 3–4 soal (ada {len(soal)})")
        levels = [s.get("level") for s in soal]
        if any(lv not in LEVEL for lv in levels):
            lap.salah(loc, "setiap soal literasi butuh level L1/L2/L3")
        elif [LEVEL.index(lv) for lv in levels] != sorted(LEVEL.index(lv) for lv in levels):
            lap.salah(loc, f"soal harus berjenjang L1 -> L3 (sekarang {levels})")
        batas = 120 if "L3" in levels else 60
        kata = hitung_kata(st.get("teks", ""))
        if kata > batas:
            lap.salah(loc, f"teks stimulus {kata} kata; maksimal {batas}")
        teks_kecil = st.get("teks", "").lower()
        for info in st.get("infoPenting", []):
            if info.lower() not in teks_kecil:
                lap.salah(loc, f"infoPenting '{info}' tidak ditemukan di teks stimulus")
        for s in soal:
            pr = s.get("proses", [])
            if not pr or any(p not in PROSES for p in pr):
                lap.salah(f"{loc}/{s.get('id')}", "label proses harus LM1–LM7")
            if "LM6" in pr:
                ada_penalaran = True
            validasi_soal(s, loc, lap, butuh_petunjuk=True)
            for q in s.get("pertanyaanCekCerita", []):
                if not 0 <= q.get("jawaban", -1) < len(q.get("pilihan", [])):
                    lap.salah(f"{loc}/{s.get('id')}", "indeks jawaban pertanyaan cek cerita tidak valid")
        if st.get("ubah"):
            validasi_soal({"id": "ubah", "tipe": "lengkapi-tabel", **st["ubah"]}, loc, lap, butuh_petunjuk=True)
    if m["literasi"] and not ada_penalaran:
        lap.salah(nama, "modul butuh minimal satu soal penalaran (LM6)")
    if not m["literasi"]:
        lap.awas(nama, "modul belum punya soal literasi")

    r = m["refleksi"]
    if not r.get("pertanyaan") or not r.get("contohPenjelasan"):
        lap.salah(nama, "refleksi butuh pertanyaan dan contohPenjelasan")


def validasi_tes(t: dict, nama: str, lap: Laporan) -> None:
    for s in t.get("soal", []):
        validasi_soal(s, nama, lap, butuh_petunjuk=False)
    rek = t.get("rekomendasi")
    if rek:
        tertutup = set()
        for r in rek:
            tertutup.update(range(r["min"], r["max"] + 1))
        semua = set(range(0, len(t["soal"]) + 1))
        if semua - tertutup:
            lap.salah(nama, f"rekomendasi belum mencakup skor {sorted(semua - tertutup)}")


def _soal_modul(isi: dict):
    """Semua butir yang dikerjakan siswa dalam satu modul (latihan, kuis, literasi)."""
    for s in isi.get("latihan", []) + isi.get("kuis", []):
        yield s
    for st in isi.get("literasi", []):
        yield from st.get("soal", [])


def _norm(teks: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"\*\*", "", str(teks))).strip().lower()


def _sidik(s: dict):
    """Sidik jari butir: (pola, kunci). Dua butir dengan pola & kunci sama dianggap soal yang sama."""
    pola = tuple(s["pola"]) if s.get("pola") else None
    kunci = s.get("jawaban")
    if s.get("tipe") == "lengkapi-tabel":
        kunci = tuple(s.get("kunciTabel", []))
    return (pola, str(kunci)) if pola is not None else None


def cek_lintas_modul(modul: dict[str, dict], tes: dict[str, dict], lap: Laporan) -> None:
    """Mencegah soal duplikat antar-modul dan butir yang sama dengan Tes Awal/Akhir.
    Butir tes yang muncul di modul membuat siswa 'berlatih soal tes', sehingga data N-gain tidak sah."""
    tes_teks, tes_sidik = {}, {}
    for nama, t in tes.items():
        for s in t.get("soal", []):
            tes_teks[_norm(s["pertanyaan"])] = f"{nama}/{s['id']}"
            if _sidik(s):
                tes_sidik[_sidik(s)] = f"{nama}/{s['id']}"
    terlihat_teks, terlihat_sidik, ids = {}, {}, {}
    for nm, isi in modul.items():
        for s in _soal_modul(isi):
            loc = f"{nm}/{s.get('id')}"
            if s.get("id") in ids:
                lap.salah(loc, f"id soal ganda (juga di {ids[s['id']]})")
            ids[s.get("id")] = loc
            t = _norm(s.get("pertanyaan", ""))
            if t in tes_teks:
                lap.salah(loc, f"pertanyaan sama dengan butir tes {tes_teks[t]}")
            if t in terlihat_teks:
                lap.salah(loc, f"pertanyaan sama dengan {terlihat_teks[t]} (soal duplikat)")
            terlihat_teks[t] = loc
            sid = _sidik(s)
            if sid:
                if sid in tes_sidik:
                    lap.salah(loc, f"pola dan kunci sama dengan butir tes {tes_sidik[sid]}")
                if sid in terlihat_sidik:
                    lap.salah(loc, f"pola dan kunci sama dengan {terlihat_sidik[sid]} (soal duplikat)")
                terlihat_sidik[sid] = loc


def validasi_semua(folder: Path = KONTEN) -> Laporan:
    lap = Laporan()
    try:
        daftar = json.loads((folder / "modul.json").read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        lap.salah("modul.json", f"tidak bisa dibaca: {e}")
        return lap
    ids = [m["id"] for m in daftar["modul"]]
    if len(ids) != len(set(ids)):
        lap.salah("modul.json", "ada id modul ganda")
    modul_tersedia: dict[str, dict] = {}
    for m in daftar["modul"]:
        path = folder / f"{m['id']}.json"
        if m.get("tersedia"):
            if not path.exists():
                lap.salah("modul.json", f"{m['id']} ditandai tersedia tetapi {path.name} tidak ada")
                continue
            try:
                isi = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                lap.salah(path.name, f"JSON tidak valid: {e}")
                continue
            if isi.get("id") != m["id"]:
                lap.salah(path.name, "id di file tidak sama dengan modul.json")
            validasi_modul(isi, path.name, lap)
            modul_tersedia[path.name] = isi
    tes: dict[str, dict] = {}
    for nama in ["tes-awal.json", "tes-akhir.json"]:
        p = folder / nama
        if not p.exists():
            lap.salah(nama, "file tidak ada")
            continue
        tes[nama] = json.loads(p.read_text(encoding="utf-8"))
        validasi_tes(tes[nama], nama, lap)
    cek_lintas_modul(modul_tersedia, tes, lap)
    return lap


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # konsol Windows
    lap = validasi_semua()
    for p in lap.peringatan:
        print("PERINGATAN ", p)
    for k in lap.kesalahan:
        print("KESALAHAN  ", k)
    if lap.kesalahan:
        print(f"\n✗ {len(lap.kesalahan)} kesalahan, {len(lap.peringatan)} peringatan.")
        return 1
    print(f"✓ Konten valid ({len(lap.peringatan)} peringatan).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
