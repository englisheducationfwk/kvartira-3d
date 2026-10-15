# -*- coding: utf-8 -*-
"""T1: список настоящих текстур в data.json + serve.py умеет webp."""
import json
import pathlib

# ---------- data.json: texlib ----------
p = pathlib.Path(__file__).resolve().parent / "data.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["texlib"] = [
    {"id": "plaster-fine",  "name": "Штукатурка тонкая",    "dir": "assets/tex/PaintedPlaster017", "k": 1.0},
    {"id": "plaster-rough", "name": "Штукатурка фактурная", "dir": "assets/tex/Plaster001",        "k": 1.0},
    {"id": "concrete",      "name": "Бетон · микроцемент",  "dir": "assets/tex/Concrete034",       "k": 0.9},
    {"id": "wood-dub",      "name": "Дуб классический",     "dir": "assets/tex/Wood070",           "k": 1.0},
    {"id": "wood-light",    "name": "Дуб светлый",          "dir": "assets/tex/Wood066",           "k": 1.0},
    {"id": "wood-nut",      "name": "Орех тёмный",          "dir": "assets/tex/Wood092",           "k": 0.9},
    {"id": "wood-worn",     "name": "Дерево состаренное",   "dir": "assets/tex/Wood051",           "k": 1.0},
]
p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("data.json texlib:", len(d["texlib"]))

# ---------- serve.py: webp mime ----------
sp = pathlib.Path(__file__).resolve().parent.parent / "tools" / "serve.py"
s = sp.read_text(encoding="utf-8")
if ".webp" not in s:
    anchor = "class Handler(http.server.SimpleHTTPRequestHandler):"
    assert anchor in s, "handler anchor"
    s = s.replace(anchor, anchor + """
    extensions_map = dict(getattr(http.server.SimpleHTTPRequestHandler, "extensions_map", {}))
    extensions_map.update({".webp": "image/webp", ".woff2": "font/woff2"})
""", 1)
    sp.write_text(s, encoding="utf-8")
    print("serve.py webp ok")
else:
    print("serve.py already has webp")
