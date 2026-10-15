# -*- coding: utf-8 -*-
"""Собирает vendor/postfx.js: три-пост-обработка r147 (SSAO, bloom, FXAA, композер)
из ESM-исходников в UMD-обёртку поверх глобального THREE."""
import pathlib
import re

SRC = pathlib.Path("_state/postfx_src")
OUT = pathlib.Path("vendor/postfx.js")

ORDER = ["CopyShader.js", "SimplexNoise.js", "LuminosityHighPassShader.js", "FXAAShader.js",
         "Pass.js", "ShaderPass.js", "MaskPass.js", "EffectComposer.js",
         "RenderPass.js", "UnrealBloomPass.js", "SSAOPass.js"]

chunks = []
for name in ORDER:
    src = (SRC / name).read_text(encoding="utf-8")

    # экспортируемые имена
    names = []
    for m in re.finditer(r"export\s*\{([^}]*)\}", src):
        for n in m.group(1).split(","):
            n = n.strip().split(" as ")[-1].strip()
            if n:
                names.append(n)
    # export class X / const X
    for m in re.finditer(r"export\s+(?:class|const|let|var|function)\s+(\w+)", src):
        names.append(m.group(1))

    # выкинуть импорты и export-маркеры
    src = re.sub(r"import\s*(?:\{[^}]*\}|\w+)\s*from\s*'[^']*';?", "", src)
    src = re.sub(r"export\s*\{[^}]*\};?", "", src)
    src = re.sub(r"\bexport\s+", "", src)

    names = list(dict.fromkeys(names))
    assigns = "\n".join(f"  THREE.{n} = {n};" for n in names)
    chunks.append(f"/* {name} */\n(function(){{\nwith (THREE) {{\n{src}\n{assigns}\n}}\n}})();\n")

OUT.write_text("\n".join(chunks), encoding="utf-8")
print("postfx.js:", OUT.stat().st_size, "bytes; exports:", "ok")
