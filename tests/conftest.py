import json
import re
import sys
from pathlib import Path

import pytest

AKAR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AKAR))

FRONTEND = AKAR / "frontend"
KONTEN = FRONTEND / "konten"


class JS:
    """Menjalankan modul JavaScript murni (tanpa DOM) di mesin V8 lewat mini-racer."""

    def __init__(self, *file_js: str):
        from py_mini_racer import MiniRacer

        self.ctx = MiniRacer()
        for nama in file_js:
            kode = (FRONTEND / "js" / nama).read_text(encoding="utf-8")
            kode = re.sub(r"^import .*?;\s*$", "", kode, flags=re.MULTILINE)
            kode = re.sub(r"^export\s+", "", kode, flags=re.MULTILINE)
            self.ctx.eval(kode)

    def panggil(self, fungsi: str, *args):
        argumen = ", ".join(json.dumps(a) for a in args)
        return json.loads(self.ctx.eval(f"JSON.stringify({fungsi}({argumen}))"))


@pytest.fixture(scope="session")
def js():
    return JS("answer.js", "pattern.js")


def muat_json(nama: str):
    return json.loads((KONTEN / nama).read_text(encoding="utf-8"))
