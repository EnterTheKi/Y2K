#!/usr/bin/env python3
"""Generate symmetric ASCII glyphs for Kiazaki.

Rows are authored as LEFT halves and mirrored to the right.
PAD=23 so every row is 46 wide with center between col 22|23.
Continuous horizontal strokes must fill the left half to col 22.
Digit pairs (33/27) and kanji rows are exempt from the symmetry check.
Output: tools/art.txt
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

PAD = 23

SWAP = {
    "/": "\\", "\\": "/",
    "(": ")", ")": "(",
}

def mirror(left: str) -> str:
    return "".join(SWAP.get(c, c) for c in reversed(left))

def verify(s: str, note: str = ""):
    w = len(s)
    bad = []
    for i in range(w // 2):
        ch, j = s[i], w - 1 - i
        m = SWAP.get(ch, ch)
        if ch.isdigit() and s[j].isdigit():
            continue
        if ord(ch) > 127 or ord(s[j]) > 127:
            continue
        if s[j] != m:
            bad.append((i, ch, j, s[j]))
    if bad:
        print(f"!! {note}: {bad[:8]}")

def row(left: str, note: str = "") -> str:
    left = left.ljust(PAD)
    full = left + mirror(left)
    verify(full, note)
    return full

def un(rowstr: str, note: str = "") -> str:
    verify(rowstr, note)
    return rowstr

ART = []

def emit(name, rows):
    ART.append((name, rows))

# ── THE WATCHER (owl on melting katana) ───────────────────
owl = [
    row("           /\\", "owl tuft tips"),            # peak @11,12
    row("          /::\\", "owl tufts"),                # @10-13
    row("        ." + "-" * 14, "owl dome"),                        # .@8, dashes 9-22
    row("       /", "owl dome curve"),                              # / @7
    row("     /" + " " * 7 + ".----.", "owl eye tops"),            # / @5, eyes @13-18
    row("    |" + " " * 8 + "( 33 )", "owl digits"),               # | @4
    row("    |" + " " * 8 + "'----'", "owl eye bottoms"),
    row("    |" + " " * 16 + ".-", "owl beak top"),                # .-. @21-24 straddles
    row(r"    |" + " " * 16 + r"\v", "owl beak"),               # \vv/ straddles
    row("           ,'", "owl lower curve"),
    row("        '" + "-" * 14, "owl bottom arc"),                  # ' @8, dashes to center
]
# right eye reads 27: replace the mirrored half's digits only
_i = owl[5].find("( 33 )", PAD)
owl[5] = owl[5][:_i] + "( 27 )" + owl[5][_i + 6:]
katana = [
    "   ii+m+" + "=" * 32 + "e",
    "      ~~           ~~~        ,~~    ~~       ",
    "                ~        気          ~         ",
    "              ~            ~        ~          ",
]
emit("THE WATCHER", owl + katana)

# ── ENSŌ ──────────────────────────────────────────────────
enso = [
    row("         ." + "=" * 13, "enso r1 top arc"),         # . @9, = 10-22 + 23-35
    row("           ,'", "enso r2"),
    row("        /", "enso r3"),
    row("      /", "enso r4"),
    row("     |", "enso r5"),
    "     |" + " " * 16 + "気" + " " * 16 + "|",
    row("     \\", "enso r7"),
    row("        \\", "enso r8"),
    row("           ,'", "enso r9"),
    row("         '" + "-" * 13, "enso r10 bottom arc"),
]
emit("ENSO", enso)

# ── THE GATE (torii) ──────────────────────────────────────
torii = [
    un("  -" + "=" * 40 + "-" + "  ", "torii kasagi1"),
    un("   " + "=" * 40 + "   ", "torii kasagi2"),
    un("          " + "-" * 26 + "          ", "torii nuki"),
    row("          |", "torii pillar"),                                 # pillars @10 & 35
    "          |" + " " * 12 + "気" + " " * 12 + "|        ",
    row("          |", "torii pillar 2"),
    "      ~   |                        |  ~     ",
]
emit("THE GATE", torii)

out = []
for name, rows in ART:
    out.append(f"==================== {name} ====================")
    out.extend(rows)
    out.append("")

with open("tools/art.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("\n".join(out))
