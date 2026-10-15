"""Сливает ВСЕ архивы отметок + текущий файл в ОДИН _reports/что_не_так.md
по дате. Архивные файлы удаляются. Дальше файл живёт вечно: сервер дописывает
новые отметки снизу, автор помечает исправленные строкой ✅."""
import pathlib, re

rep = pathlib.Path('_reports')

def marks_of(text):
    """вытащить записи вида '- **14.10.2026, ..** · ... \\n  - текст'"""
    out = []
    lines = text.split('\n')
    i = 0
    while i < len(lines):
        if lines[i].startswith('- **'):
            blk = [lines[i]]
            j = i + 1
            while j < len(lines) and (lines[j].startswith('  ') or not lines[j].strip()):
                if not lines[j].strip():
                    break
                blk.append(lines[j]); j += 1
            out.append('\n'.join(blk))
            i = j
        else:
            i += 1
    return out

all_marks = []
for f in sorted(rep.glob('исправлено_*.md')):
    all_marks += marks_of(f.read_text(encoding='utf-8'))
all_marks += marks_of((rep / 'что_не_так.md').read_text(encoding='utf-8'))

# дедуп по первой строке, сортировка по дате-времени
seen, uniq = set(), []
for m in all_marks:
    key = m.split('\n')[0]
    if key not in seen:
        seen.add(key); uniq.append(m)

def dt(m):
    mm = re.match(r'- \*\*(\d+)\.(\d+)\.(\d+), (\d+):(\d+):(\d+)\*\*', m)
    return (mm.group(3), mm.group(2), mm.group(1), mm.group(4), mm.group(5), mm.group(6)) if mm else ('0','0','0','0','0','0')

uniq.sort(key=dt)

head = '''# Что не так в квартире (из режима 🐞) — ВСЁ ЗДЕСЬ, В ОДНОМ ФАЙЛЕ

Правила: файл ОДИН и НИКОГДА не чистится и не переносится в архивы.
Новые отметки сервер дописывает снизу (с датой и временем).
Исправленное помечается строкой «✅ исправлено» — не удаляется.
Смотрю всегда по дате: свежие — внизу. Работаем по списку сверху вниз.

'''

(rep / 'что_не_так.md').write_text(head + '\n'.join(uniq) + '\n', encoding='utf-8')
for f in rep.glob('исправлено_*.md'):
    f.unlink()
print('merged:', len(uniq), 'marks')
