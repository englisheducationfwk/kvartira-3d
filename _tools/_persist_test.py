# -*- coding: utf-8 -*-
"""Проверка: переживает ли localStorage перезапуск окна pywebview со storage_path.
Запуск: python _tools/_persist_test.py set   → пишет метку
        python _tools/_persist_test.py get   → читает её в новом окне
"""
import sys
import time
from pathlib import Path

import webview

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "_state" / "webview"
mode = sys.argv[1] if len(sys.argv) > 1 else "set"

w = webview.create_window(
    "persist-test", "http://127.0.0.1:8140/index.html", width=300, height=200
)


def job():
    time.sleep(3.5)
    try:
        if mode == "set":
            w.evaluate_js("try{localStorage.setItem('__wmt','alive42')}catch(e){}")
            print("SET:", w.evaluate_js("localStorage.getItem('__wmt')"), flush=True)
        else:
            print("GET:", w.evaluate_js("localStorage.getItem('__wmt')"), flush=True)
    except Exception as e:  # noqa: BLE001
        print("ERR:", str(e)[:200], flush=True)
    time.sleep(0.3)
    w.destroy()


webview.start(job, private_mode=False, storage_path=str(STATE))
print("closed", flush=True)
