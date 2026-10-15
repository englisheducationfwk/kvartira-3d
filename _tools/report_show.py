"""Показать отметки: python _tools/report_show.py [--all]
По умолчанию печатает только НЕисправленные (❗ новое) — то, что ждёт работы."""
import pathlib, sys

t = pathlib.Path(__file__).resolve().parent.parent / '_reports' / 'что_не_так.md'
txt = t.read_text(encoding='utf-8')
blocks = [b for b in txt.split('\n- **') if b.strip()]
show_all = '--all' in sys.argv
n_new = 0
for b in blocks:
    blk = ('- **' + b) if not b.startswith('#') else b
    if blk.startswith('- **'):
        fixed = '✅ исправлено' in blk
        if show_all or not fixed:
            print(blk.rstrip())
            print()
            if not fixed:
                n_new += 1
if not show_all:
    print('ИТОГО новых (неисправленных):', n_new)
