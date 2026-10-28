#!/usr/bin/env python3
"""Procedural dithered owl for Kiazaki — NOFEX-style dot matrix.

Thin solid rim ellipse head, 50% checker dither inside, black void eyes
holding the red 33/27 digits, solid beak, slim tufts, melting onto a katana.
Output: tools/owl.txt with SPAN markers for the html (red digits / dim 気).
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

W, H = 46, 24
g = [[" "] * W for _ in range(H)]

def put(x, y, ch):
    if 0 <= x < W and 0 <= y < H:
        g[int(y)][int(x)] = ch

# ── head ellipse ──
CX, CY, RX, RY = 22.5, 10.5, 17.0, 8.5
for y in range(H):
    if y > 16:
        continue                            # head melts onto the blade below row 17
    for x in range(W):
        v = ((x - CX) / RX) ** 2 + ((y - CY) / RY) ** 2
        if v <= 1.0:
            g[y][x] = "." if (x + y) % 2 == 0 else " "
        elif v <= 1.1:                      # thin solid rim
            g[y][x] = "#"

# ── eye voids with ':' rims ──
for ecx in (15.5, 29.5):
    ey, er = 10.5, 4.0
    for y in range(H):
        for x in range(W):
            v = ((x - ecx) / er) ** 2 + ((y - ey) / er) ** 2
            if v <= 1.0:
                g[y][x] = " "
            elif v <= 1.35:
                g[y][x] = ":"

# digits inside voids
g[10][15] = "3"; g[10][16] = "3"
g[10][28] = "2"; g[10][29] = "7"

# ── beak: small solid triangle pointing down ──
for x in range(20, 26):
    g[12][x] = "#"
g[13][21] = "#"; g[13][24] = "#"
g[14][22] = "#"; g[14][23] = "#"

# ── tufts: slim triangles over the dome ──
for i, y in enumerate(range(1, 6)):
    halfw = 0.3 + 0.55 * i
    for x in range(int(13.5 - halfw) + 1, int(13.5 + halfw) + 1):
        put(x, y, "#")
    for x in range(int(31.5 - halfw) + 1, int(31.5 + halfw) + 1):
        put(x, y, "#")

# ── melting katana under the head ──
KK = 17
for x in range(4, 41):
    g[KK][x] = "="
g[KK][2] = "i"; g[KK][3] = "i"
g[KK][4] = "+"; g[KK][5] = "m"; g[KK][6] = "+"
g[KK][41] = "e"

drip = "   .         ,        ~~            .      ,     "
for c, ch in enumerate(drip):
    if ch != " ":
        g[KK + 2][c] = ch

# ── render with html span markers ──
rows = []
for r in g:
    line = "".join(r).rstrip()
    line = line.replace("33", "S33E").replace("27", "S27E")
    rows.append(line)
out = "\n".join(rows)
open("tools/owl.txt", "w", encoding="utf-8").write(out + "\n")
print(out)
