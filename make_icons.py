import os, zlib, struct

os.makedirs('docs', exist_ok=True)

def make(path, s):
    bg = (15, 23, 42)
    white = (255, 255, 255)
    yellow = (250, 204, 21)
    green = (22, 163, 74)
    dark = (15, 23, 42)
    rows = []
    for y in range(s):
        fy = y / s
        row = bytearray([0])
        for x in range(s):
            fx = x / s
            c = bg
            if 0.22 <= fx <= 0.78 and 0.26 <= fy <= 0.80:
                c = white
                if fy <= 0.42:
                    c = yellow
                if 0.50 <= fy <= 0.53 or 0.60 <= fy <= 0.63 or 0.70 <= fy <= 0.73:
                    if 0.30 <= fx <= 0.70:
                        c = green
            if (0.32 <= fx <= 0.37 or 0.63 <= fx <= 0.68) and 0.20 <= fy <= 0.32:
                c = dark
            row += bytes(c)
        rows.append(bytes(row))
    raw = b''.join(rows)

    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)

    data = b'\x89PNG\r\n\x1a\n'
    data += chunk(b'IHDR', struct.pack('>IIBBBBB', s, s, 8, 2, 0, 0, 0))
    data += chunk(b'IDAT', zlib.compress(raw, 9))
    data += chunk(b'IEND', b'')
    open(path, 'wb').write(data)

make('docs/icon-192.png', 192)
make('docs/icon-512.png', 512)
print('icons ok')
