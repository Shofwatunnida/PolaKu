"""Uji tema "Pastel Math Wonderland": ornamen tidak menghalangi, kontras teks cukup,
tampilan pas di HP dan laptop.
"""
import pytest

from test_alur import PERANGKAT, alamat, peramban, pw, foto, tombol  # noqa: F401

PERANGKAT_TEMA = {**PERANGKAT, "laptop-1366": ("chromium", {"viewport": {"width": 1366, "height": 768}})}

HALAMAN = [
    ("beranda", "#/", []),
    ("peta", "#/peta", []),
    ("modul", "#/modul/m2", []),
    ("konsep", "#/modul/m2/konsep", []),
    ("contoh", "#/modul/m2/contoh", ["Langkah berikutnya ↓"]),
    ("setengah", "#/modul/m2/setengah", ["Langkah berikutnya ↓"]),
    ("latihan", "#/modul/m2/latihan", []),
    ("literasi", "#/modul/m2/literasi", ["Mulai"]),
    ("refleksi", "#/modul/m2/refleksi", []),
    ("kuis", "#/modul/m2/kuis", ["Mulai kuis"]),
    ("progres", "#/progres", []),
    ("tentang", "#/tentang", []),
    ("tes", "#/tes/awal", ["Mulai"]),
]


@pytest.fixture(params=list(PERANGKAT_TEMA))
def hal(request, pw, peramban, alamat):  # noqa: F811
    mesin, desk = PERANGKAT_TEMA[request.param]
    opsi = dict(pw.devices[desk]) if isinstance(desk, str) else dict(desk)
    opsi.pop("default_browser_type", None)
    ctx = peramban(mesin).new_context(**opsi, locale="id-ID")
    ctx.add_init_script("try { localStorage.setItem('polaku:nama', 'Kiara'); } catch (e) {}")
    page = ctx.new_page()
    page.perangkat = request.param
    galat = []
    page.on("pageerror", lambda e: galat.append(str(e)))
    yield page
    ctx.close()
    assert galat == [], galat


def buka(page, alamat, rute, klik):  # noqa: F811
    page.goto(alamat + "/" + rute)
    page.locator("main h1").first.wait_for()
    for t in klik:
        tombol(page, t).click()
    page.wait_for_timeout(150)


CEK_ORNAMEN = """() => {
  const lapisan = document.querySelector('.latar-hias');
  const gaya = getComputedStyle(lapisan);
  const lebar = innerWidth, tinggi = innerHeight;
  const main = document.querySelector('main').getBoundingClientRect();
  const kolom = { kiri: (lebar - Math.min(lebar, 680)) / 2, kanan: (lebar + Math.min(lebar, 680)) / 2 };
  const hasil = { zIndex: gaya.zIndex, pointer: gaya.pointerEvents, ariaHidden: lapisan.getAttribute('aria-hidden'), ornamen: [] };
  document.querySelectorAll('.hias').forEach(img => {
    const r = img.getBoundingClientRect();
    const g = getComputedStyle(img);
    if (g.display === 'none' || !r.width) return;
    const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    const atas = document.elementFromPoint(cx, cy);
    hasil.ornamen.push({
      nama: img.className, utuh: r.left >= 0 && r.top >= 0 && r.right <= lebar + 0.5 && r.bottom <= tinggi + 0.5,
      masukKolom: r.right > kolom.kiri && r.left < kolom.kanan, opacity: parseFloat(g.opacity),
      ketukanKe: atas ? atas.className || atas.tagName : null, termuat: img.complete && img.naturalWidth > 0,
    });
  });
  return hasil;
}"""


@pytest.mark.parametrize("nama, rute, klik", [HALAMAN[0], HALAMAN[3], HALAMAN[6]], ids=["beranda", "konsep", "latihan"])
def test_ornamen_di_belakang_utuh_dan_tidak_menghalangi(hal, alamat, nama, rute, klik):
    page = hal
    buka(page, alamat, rute, klik)
    h = page.evaluate(CEK_ORNAMEN)
    assert int(h["zIndex"]) < 0 and h["pointer"] == "none" and h["ariaHidden"] == "true"
    assert h["ornamen"], "minimal satu ornamen tampil"
    for o in h["ornamen"]:
        assert o["termuat"], f"ornamen gagal dimuat: {o}"
        assert o["utuh"], f"ornamen terpotong (jumlah pola tidak terlihat utuh): {o}"
        assert "hias" not in str(o["ketukanKe"]), f"ornamen menangkap ketukan: {o}"
        if page.viewport_size["width"] >= 1000:
            assert not o["masukKolom"], f"ornamen masuk ke kolom konten di laptop: {o}"
        else:
            assert o["opacity"] <= 0.4, f"ornamen terlalu pekat di HP: {o}"
    if nama == "beranda":
        foto(page, f"tema-{nama}")


KONTRAS = """() => {
  const lum = (c) => { const v = c / 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
  const parse = (s) => { const m = s.match(/rgba?\\(([^)]+)\\)/); if (!m) return null; const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; };
  const campur = (atas, bawah) => ({ r: atas.r * atas.a + bawah.r * (1 - atas.a), g: atas.g * atas.a + bawah.g * (1 - atas.a), b: atas.b * atas.a + bawah.b * (1 - atas.a), a: 1 });
  // latar halaman (gradasi) diwakili warna gradasi yang PALING GELAP agar penilaian tidak terlalu longgar
  const LATAR = { r: 221, g: 214, b: 254, a: 1 };
  const latarDari = (el) => {
    const lapis = [];
    for (let e = el; e && e !== document.documentElement; e = e.parentElement) {
      const g = getComputedStyle(e);
      const bg = parse(g.backgroundColor);
      if (g.backgroundImage && g.backgroundImage !== 'none' && e !== document.body) return { warna: LATAR, gradasi: true };
      if (bg && bg.a > 0) { lapis.push(bg); if (bg.a >= 1) break; }
    }
    let w = LATAR;
    for (let i = lapis.length - 1; i >= 0; i--) w = campur(lapis[i], w);
    return { warna: w, gradasi: false };
  };
  const rasio = (a, b) => { const la = 0.2126 * lum(a.r) + 0.7152 * lum(a.g) + 0.0722 * lum(a.b); const lb = 0.2126 * lum(b.r) + 0.7152 * lum(b.g) + 0.0722 * lum(b.b); return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05); };
  const gagal = [];
  const sel = 'main h1, main h2, main p, main li, main label, main .lencana, main .peta-kode, main .peta-ringkas, main .kepala-info, main .tombol, main .menu-item, main .posisi, main .label-langkah, main summary, .nav-bawah a';
  document.querySelectorAll(sel).forEach(el => {
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height || !el.textContent.trim()) return;
    const g = getComputedStyle(el);
    if (g.visibility === 'hidden' || parseFloat(g.opacity) < 1) return;   // mis. modul terkunci (sengaja diredupkan)
    if (el.closest('.peta-terkunci, [disabled], .tombol:disabled')) return;
    const warna = parse(g.color); const latar = latarDari(el).warna;
    const nilai = rasio(campur(warna, latar), latar);
    const besar = parseFloat(g.fontSize) >= 24 || (parseFloat(g.fontSize) >= 18.66 && parseInt(g.fontWeight) >= 700);
    if (nilai < (besar ? 3 : 4.5)) gagal.push(`${el.tagName}.${el.className} "${el.textContent.trim().slice(0, 24)}" ${nilai.toFixed(2)}`);
  });
  return gagal;
}"""


@pytest.mark.parametrize("nama, rute, klik", HALAMAN, ids=[x[0] for x in HALAMAN])
def test_kontras_teks_cukup(hal, alamat, nama, rute, klik):
    page = hal
    if page.perangkat not in ("android-390", "laptop-1366"):
        pytest.skip("kontras tidak bergantung ukuran layar; cukup 2 perangkat")
    buka(page, alamat, rute, klik)
    gagal = page.evaluate(KONTRAS)
    assert gagal == [], f"kontras teks kurang (WCAG AA): {gagal}"


@pytest.mark.parametrize("nama, rute, klik", HALAMAN, ids=[x[0] for x in HALAMAN])
def test_laptop_pas_dan_rapi(hal, alamat, nama, rute, klik):
    page = hal
    if page.perangkat != "laptop-1366":
        pytest.skip("layar HP sudah diuji di test_ponsel.py")
    buka(page, alamat, rute, klik)
    luber = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    assert luber <= 1
    lebar_main = page.locator("main").bounding_box()["width"]
    assert lebar_main <= 700, "kolom konten tetap nyaman dibaca di layar lebar"
    foto(page, f"tema-laptop-{nama}")


def test_peta_status_mudah_dibedakan(hal, alamat):
    page = hal
    if page.perangkat not in ("android-390", "laptop-1366"):
        pytest.skip("cukup 2 perangkat")
    page.goto(alamat + "/")
    page.evaluate("localStorage.setItem('polaku:v1', JSON.stringify({progres: {m2: {status: 'selesai', tahapSelesai: []}, m4: {status: 'sedang', tahapSelesai: []}}}))")
    page.reload()
    page.goto(alamat + "/#/peta")
    page.locator(".peta-item").first.wait_for()
    teks = {s: page.locator(f".lencana-{s}").first.inner_text() for s in ["selesai", "sedang", "segera"]}
    assert teks["selesai"].startswith("✓") and teks["sedang"].startswith("▶") and teks["segera"].startswith("🔒")
    # setiap modul punya ikon sendiri yang termuat (aset lokal)
    ikon = page.locator(".peta-ikon")
    assert ikon.count() == 9
    for _ in range(50):  # tunggu semua ikon termuat (wait_for_function diblokir CSP aplikasi)
        if page.evaluate("[...document.querySelectorAll('.peta-ikon')].every(i => i.complete && i.naturalWidth > 0)"):
            break
        page.wait_for_timeout(100)
    assert page.evaluate("[...document.querySelectorAll('.peta-ikon')].every(i => i.complete && i.naturalWidth > 0)")
    foto(page, "tema-peta")
