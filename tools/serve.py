"""Локальный сервер кухни: отдаёт папку проекта, принимает жалобы «что не так».

    python tools/serve.py [порт]

Порт по умолчанию 8124; если занят — берёт следующий (до +10).
Жалобы из режима «🐞 Что не так» пишутся в _reports/что_не_так.md.
"""
from __future__ import annotations

import http.server
import json
import socket
import sys
import threading
import webbrowser
from functools import partial
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PORT = 8124
REPORT_DIR = ROOT / "_reports"
REPORT_FILE = REPORT_DIR / "что_не_так.md"


def free_port(start: int, tries: int = 10) -> int:
    for port in range(start, start + tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return 0


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt: str, *args) -> None:  # тихий режим
        pass

    def do_POST(self) -> None:  # noqa: N802
        if self.path.rstrip("/") != "/report":
            self.send_error(404)
            return
        try:
            n = int(self.headers.get("Content-Length") or 0)
            data = json.loads(self.rfile.read(n).decode("utf-8"))
        except Exception:
            self.send_error(400)
            return
        REPORT_DIR.mkdir(exist_ok=True)
        if not REPORT_FILE.exists():
            REPORT_FILE.write_text(
                "# Что не так в квартире (из режима 🐞) — ВСЁ ЗДЕСЬ, В ОДНОМ ФАЙЛЕ\n\n"
                "Правила: файл ОДИН и НИКОГДА не чистится. Новые отметки дописываются снизу.\n"
                "Исправленное помечается «✅ исправлено» — не удаляется.\n\n",
                encoding="utf-8")
        extra = ""
        if data.get("place"):
            extra += f" · место:{data.get('place')}"
        if data.get("from"):
            f3 = data.get("from")
            extra += f" · смотрел из X={f3[0]} Y={f3[1]} Z={f3[2]}"
        if data.get("look"):
            l2 = data.get("look")
            extra += f" (взгляд {l2[0]}/{l2[1]})"
        rec = (
            f"- **{data.get('t', '?')}** · {data.get('n', '?')} · "
            f"X={data.get('x')} Y={data.get('y')} Z={data.get('z')} · "
            f"зеркало:{'вкл' if data.get('mirror') else 'выкл'}{extra}\n"
            f"  - {str(data.get('note', '')).strip()}\n"
            f"  - ❗ новое (ждёт)\n"
        )
        with open(REPORT_FILE, "a", encoding="utf-8") as fh:
            fh.write(rec)
        body = b'{"ok":true}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def make_server(start_port: int = DEFAULT_PORT):
    port = free_port(start_port)
    if not port:
        raise OSError(f"Порты {start_port}-{start_port + 9} заняты")
    server = http.server.ThreadingHTTPServer(
        ("127.0.0.1", port), partial(Handler, directory=str(ROOT)))
    return server, port


def main() -> int:
    if not (ROOT / "index.html").exists():
        print("Нет index.html — сначала собери: python _tools/build.py")
        return 1
    try:
        server, port = make_server(int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT)
    except OSError as e:
        print(e)
        return 1
    url = f"http://127.0.0.1:{port}/index.html"
    print(f"  Кухня: {url}   (окно можно свернуть, Ctrl+C — стоп)")
    threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Сервер остановлен.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
