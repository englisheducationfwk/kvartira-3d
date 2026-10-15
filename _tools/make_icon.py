"""Иконка кухни (.ico) — чистый Python, без зависимостей. 32x32 и 16x16."""
import pathlib
import struct

OUT = pathlib.Path(__file__).resolve().parent.parent / "kuhnya.ico"

WARM = (196, 226, 235, 255)      # BGRA: тёплый беж-терракота (R=235 G=226 B=196)
TERRA = (47, 86, 176, 255)       # терракотовый (R=176 G=86 B=47)
DARK = (34, 74, 158, 255)        # затемнение
WHITE = (250, 252, 250, 255)


def draw(x, y, s):
    """Цвет пикселя для размера s."""
    # терракотовое «крыльцо»-дуга снизу + белое окно
    # рамка-квадрат со скруглением
    inset = s * 0.08
    if x < inset or y < inset or x >= s - inset or y >= s - inset:
        return (0, 0, 0, 0)
    # окно: прямоугольник в центре
    wx0, wx1 = s * 0.28, s * 0.72
    wy0, wy1 = s * 0.26, s * 0.60
    if wx0 <= x <= wx1 and wy0 <= y <= wy1:
        # переплёт окна
        if abs(x - (wx0 + wx1) / 2) <= s * 0.035 or abs(y - (wy0 + wy1) / 2) <= s * 0.035:
            return TERRA
        return WHITE
    # стол-столешница
    if s * 0.66 <= y <= s * 0.74 and s * 0.16 <= x <= s * 0.84:
        return WHITE
    # фартук-подложка над столом
    if s * 0.74 < y <= s * 0.86 and s * 0.16 <= x <= s * 0.84:
        return DARK
    return WARM


def bmp(size):
    rows = []
    for y in range(size):
        row = []
        for x in range(size):
            b, g, r, a = draw(x, y, size)
            row.append((b, g, r, a))
        rows.append(row)
    pixels = b''.join(struct.pack('<BBBB', *px) for row in reversed(rows) for px in row)
    mask_row = ((size + 31) // 32) * 4
    mask = b'\x00' * (mask_row * size)
    hdr = struct.pack('<IiiHHIIiiII', 40, size, size * 2, 1, 32, 0, len(pixels), 0, 0, 0, 0)
    return hdr + pixels + mask


def main():
    sizes = [32, 16]
    images = [bmp(s) for s in sizes]
    header = struct.pack('<HHH', 0, 1, len(images))
    offset = 6 + 16 * len(images)
    entries = b''
    data = b''
    for s, img in zip(sizes, images):
        entries += struct.pack('<BBBBHHII', s, s, 0, 0, 1, 32, len(img), offset)
        offset += len(img)
        data += img
    OUT.write_bytes(header + entries + data)
    print('ok ->', OUT, OUT.stat().st_size, 'байт')


if __name__ == '__main__':
    main()
