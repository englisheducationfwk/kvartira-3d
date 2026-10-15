"""Кухня — запуск как игра: поднимает сервер и открывает окно (pywebview).

Обычный запуск: двойной клик по «КУХНЯ 3D.bat» или ярлыку на рабочем столе.
Окно — как у MY VISION: без адресной строки, размер 1480×940.
Если pywebview недоступен — откроется системный браузер с тем же адресом.
"""
from __future__ import annotations

import os
import sys
import threading
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "tools"))

from serve import make_server  # noqa: E402  (локальный сервер + приём жалоб)

ICON = ROOT / "kuhnya.ico"


def main() -> int:
    if not (ROOT / "index.html").exists():
        print("Нет index.html — собери: python _tools/build.py")
        return 1
    server, port = make_server(8130)
    url = f"http://127.0.0.1:{port}/index.html"
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f"  Кухня-игра: {url}")
    try:
        import webview  # type: ignore
        # RTX: заставляем WebView2 взять дискретную карту (не встроенную)
        os.environ["WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS"] = "--force_high_performance_gpu"
        w, h = 1480, 940
        try:                                    # окно — ровно по центру экрана
            import tkinter as tk
            _r = tk.Tk(); _r.withdraw()
            sw, sh = _r.winfo_screenwidth(), _r.winfo_screenheight()
            _r.destroy()
        except Exception:
            sw, sh = 1920, 1080
        webview.create_window(
            "Кухня — ремонт и покраска",
            url,
            width=w,
            height=h,
            x=max(0, (sw - w) // 2),
            y=max(0, (sh - h) // 2),
            min_size=(900, 560),
            background_color="#f3f0ea",
        )
        # ВАЖНО: постоянное хранилище — иначе localStorage (позиция, предметы,
        # пресеты) стирается при каждом запуске и игра открывается «у двери».
        state_dir = ROOT / "_state" / "webview"
        state_dir.mkdir(parents=True, exist_ok=True)
        try:
            webview.start(private_mode=False, storage_path=str(state_dir))
        except Exception:
            # профиль мог повредиться (жёсткое выключение) — пересоздаём и пробуем ещё раз
            import shutil
            shutil.rmtree(state_dir, ignore_errors=True)
            state_dir.mkdir(parents=True, exist_ok=True)
            webview.start(private_mode=False, storage_path=str(state_dir))
    except Exception as e:  # noqa: BLE001
        print(f"  Окно не завелось ({e}) — открываю браузер.")
        webbrowser.open(url)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
    finally:
        server.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
