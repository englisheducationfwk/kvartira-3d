"""Сборка кухни: _tools/template.html + _tools/data.json + vendor/three → index.html.

Проверяет данные (обязательные поля, уникальные id, диапазоны) и инлайнит
three.js с OrbitControls прямо в страницу — index.html самодостаточен,
работает и по file://, и с локального сервера, и офлайн.

    python _tools/build.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TPL = ROOT / "_tools" / "template.html"
DATA = ROOT / "_tools" / "data.json"
THREE = ROOT / "vendor" / "three.min.js"
ORBIT = ROOT / "vendor" / "OrbitControls.js"
OUT = ROOT / "index.html"

errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def check_data(d: dict) -> None:
    for key in ("meta", "house", "room", "spec", "compute", "palette", "stages3d",
                "hotspots", "shopping", "rules", "plan", "glossary", "walk"):
        if key not in d:
            err(f"data.json: нет раздела «{key}»")
    if errors:
        return

    room = d["room"]
    for key in ("w", "d", "hWall", "hCeil", "plinth"):
        if not isinstance(room.get(key), (int, float)) or room[key] <= 0:
            err(f"room.{key}: должно быть положительное число")
    if not (isinstance(room.get("hCeil"), (int, float))
            and room["hCeil"] > room["hWall"]):
        err("room.hCeil: потолок должен быть выше стены до плинтуса")

    ids: set[str] = set()
    for grp in d["shopping"]:
        for key in ("group", "items", "note"):
            if key not in grp:
                err(f"shopping: у группы «{grp.get('group')}» нет «{key}»")
        for it in grp.get("items", []):
            if it["id"] in ids:
                err(f"shopping: повтор id «{it['id']}»")
            ids.add(it["id"])
            has = "price" in it or "variants" in it
            if not has:
                err(f"shopping[{it['id']}]: нет ни price, ни variants")
            if "variants" in it:
                if not it["variants"]:
                    err(f"shopping[{it['id']}]: пустой variants")
                if not (0 <= it.get("chosen", 0) < len(it["variants"])):
                    err(f"shopping[{it['id']}]: chosen вне диапазона variants")
                for v in it["variants"]:
                    if not isinstance(v.get("price"), (int, float)):
                        err(f"shopping[{it['id']}]: у варианта нет числовой price")
            for key in ("name", "spec", "find", "note"):
                if not it.get(key):
                    err(f"shopping[{it['id']}]: пустое поле «{key}»")

    hs_ids = [h["id"] for h in d["hotspots"]]
    if len(hs_ids) != len(set(hs_ids)):
        err("hotspots: повтор id")

    if len(d["stages3d"]) != 6:
        err(f"stages3d: должно быть 6 этапов (0–5), а их {len(d['stages3d'])}")

    for st in d["plan"]:
        if not st.get("steps"):
            err(f"plan[{st.get('id')}]: пустой список шагов")

    for grp in d["spec"]:
        for row in grp.get("rows", []):
            if not row.get("name") or not row.get("value"):
                err("spec: пустая строка замера")


def main() -> int:
    missing = [str(p) for p in (TPL, DATA, THREE, ORBIT) if not p.exists()]
    if missing:
        print("Нет файлов:\n  " + "\n  ".join(missing))
        return 1

    data = json.loads(DATA.read_text(encoding="utf-8"))
    check_data(data)
    if errors:
        print("Данные сломаны — index.html не собираю:")
        for e in errors:
            print("  ✗", e)
        return 1

    tpl = TPL.read_text(encoding="utf-8")
    three = THREE.read_text(encoding="utf-8")
    orbit = ORBIT.read_text(encoding="utf-8")
    postfx = (THREE.parent / "postfx.js")
    postfx = postfx.read_text(encoding="utf-8") if postfx.exists() else ""
    for name, js in (("three.min.js", three), ("OrbitControls.js", orbit), ("postfx.js", postfx)):
        if "</script" in js.lower():
            print(f"{name}: содержит </script> — инлайн небезопасен")
            return 1

    for ph in ("/*__THREE__*/", "/*__ORBIT__*/", "/*__POSTFX__*/", "/*__DATA__*/"):
        if tpl.count(ph) != 1:
            print(f"Шаблон: плейсхолдер {ph} должен встречаться ровно 1 раз "
                  f"(сейчас {tpl.count(ph)})")
            return 1

    html = (tpl
            .replace("/*__THREE__*/", three)
            .replace("/*__ORBIT__*/", orbit)
            .replace("/*__POSTFX__*/", postfx)
            .replace("/*__DATA__*/", json.dumps(data, ensure_ascii=False, indent=1)))

    OUT.write_text(html, encoding="utf-8", newline="\n")
    items = sum(len(g["items"]) for g in data["shopping"])
    size = OUT.stat().st_size / 1024
    print(f"OK → {OUT.name}: {size:.0f} КБ · позиций в смете: {items} · "
          f"этапов: {len(data['plan'])} · подсказок: {len(data['hotspots'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
