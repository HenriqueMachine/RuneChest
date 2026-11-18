#!/usr/bin/env python3
"""RuneChest runes, draft 3: Mad Max cuts and neon by layer.

One bind-rune per agent: the rune of the first letter + the rune of the role, on the shared central stave.
Each stroke is a filled polygon (not a line), so it can have:
  - chamfered ends: every free end is cut on a diagonal, like metal cut with a torch;
  - notches: one V cut into the side of the long strokes. The place and the side come from a seed per agent, so the
    runes look hand-cut but stay the same at each build.

Outputs, in this folder:
  <name>.svg       one colour (currentColor), for the terminal font (the glyphs of RuneChest Runes).
  <name>-neon.svg  the neon colour of the agent's layer with a glow, for the README, the site and the slides.
  preview.html     the comparison page.
  RuneChestRunes.ttf  the terminal font: one glyph per agent from U+100000 (Plane 16 private use area, so no clash
                   with the Nerd Font). Needs fontTools (`.venv/bin/pip install fonttools`).
Run: .venv/bin/python assets/runes/build.py [--install]   (--install copies the font to ~/Library/Fonts)
"""
import math
import random
import shutil
import sys
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAVE = [(50, 10), (50, 90)]
WIDTH = 10        # stroke width on the 100 x 100 grid
CHAMFER = 7       # how far the diagonal cut goes back along the stroke
NOTCH_DEPTH = 3.6 # how deep a V notch goes into the stroke
NOTCH_HALF = 3.2  # half the opening of a V notch, along the stroke

# Base runes (Elder Futhark). A stroke is a polyline. The names follow the Unicode names.
RUNES = {
    "fehu":     ("ᚠ", [STAVE, [(50, 40), (76, 18)], [(50, 62), (76, 40)]]),
    "uruz":     ("ᚢ", [STAVE, [(50, 10), (76, 34), (76, 90)]]),
    "ansuz":    ("ᚨ", [STAVE, [(50, 14), (74, 32)], [(50, 36), (74, 54)]]),
    "raidho":   ("ᚱ", [STAVE, [(50, 10), (74, 28), (50, 46), (76, 90)]]),
    "kenaz":    ("ᚲ", [STAVE, [(76, 22), (50, 44), (76, 66)]]),
    "gebo":     ("ᚷ", [[(24, 18), (76, 82)], [(76, 18), (24, 82)]]),
    "wunjo":    ("ᚹ", [STAVE, [(50, 10), (74, 26), (50, 42)]]),
    "naudiz":   ("ᚾ", [STAVE, [(32, 36), (68, 64)]]),
    "eihwaz":   ("ᛇ", [STAVE, [(50, 10), (70, 26)], [(50, 90), (30, 74)]]),
    "tiwaz":    ("ᛏ", [STAVE, [(50, 10), (26, 34)], [(50, 10), (74, 34)]]),
    "berkano":  ("ᛒ", [STAVE, [(50, 10), (74, 30), (50, 50), (74, 70), (50, 90)]]),
    "ehwaz":    ("ᛖ", [[(26, 90), (26, 12), (50, 36), (74, 12), (74, 90)]]),
    "mannaz":   ("ᛗ", [[(26, 90), (26, 10), (74, 46)], [(74, 90), (74, 10), (26, 46)]]),
    "laguz":    ("ᛚ", [STAVE, [(50, 10), (72, 32)]]),
    "othala":   ("ᛟ", [[(50, 10), (74, 38), (50, 66), (26, 38), (50, 10)], [(38, 52), (24, 90)], [(62, 52), (76, 90)]]),
    # Variants: the same rune moved up, down or to the left, so it does not hide inside the other rune of a bind.
    "algiz_high":  ("ᛉ", [STAVE, [(50, 40), (24, 12)], [(50, 40), (76, 12)]]),
    "hagalaz_h":   ("ᚺ", [STAVE, [(28, 60), (72, 84)]]),
    "hagalaz_low": ("ᚼ", [STAVE, [(28, 54), (72, 86)], [(72, 54), (28, 86)]]),
    "naudiz_high": ("ᚾ", [STAVE, [(32, 14), (68, 38)]]),
    "wunjo_left":  ("ᚹ", [STAVE, [(50, 10), (26, 26), (50, 42)]]),
}

# Neon by layer (vault 11-Agentes/Identidade.md): lead yellow, backend cyan and blue, app magenta and pink,
# specialists orange, green, violet. The helpers take a lighter tone of their executor.
CREW = [
    # name,      initial,       role rune,     role,                         today,          layer,        neon
    ("Odin",     "othala",      "ansuz",       "Orquestrador",               "Swain",        "liderança",  "#f9f002"),
    ("Heimdall", "hagalaz_h",   "algiz_high",  "Integrador do backend",      "Galio",        "backend",    "#05d9e8"),
    ("Forseti",  "fehu",        "tiwaz",       "Integrador do app",          "Taric",        "app",        "#ff2a6d"),
    ("Eitri",    "ehwaz",       "kenaz",       "Executor do backend",        "Viktor",       "backend",    "#3d9bff"),
    ("Völundr",  "wunjo",       "gebo",        "Executor do app",            "Heimerdinger", "app",        "#ff4fd8"),
    ("Brokkr",   "berkano",     "fehu",        "Ajudante de Eitri",          "Xayah",        "backend",    "#8cc2ff"),
    ("Egill",    "ehwaz",       "eihwaz",      "Ajudante de Völundr",        "Rakan",        "app",        "#ff9ce9"),
    ("Grisnir",  "gebo",        "uruz",        "Mecânico de Eitri",          "Ziggs",        "backend",    "#c4e0ff"),
    ("Gnjóstr",  "naudiz",      "uruz",        "Mecânico de Völundr",        "Rumble",       "app",        "#ffc9f3"),
    ("Mímir",    "mannaz",      "laguz",       "IA full-stack",              "Zilean",       "especialista", "#ffb000"),
    ("Bifröst",  "berkano",     "raidho",      "Integrações",                "Thresh",       "especialista", "#00ff9f"),
    ("Bragi",    "berkano",     "wunjo_left",  "Texto, design, PDFs",        "Lupin",        "especialista", "#c77dff"),
    ("Níðhöggr", "naudiz_high", "hagalaz_low", "Código morto e refatoração", "Pyke",         "especialista", "#ff7a3d"),
]


def slug(name: str) -> str:
    return name.translate(str.maketrans("öíðÖÍÐó", "oidOIDo")).lower()


def strokes_of(*keys: str) -> list:
    seen, out = set(), []
    for key in keys:
        for stroke in RUNES[key][1]:
            sig = tuple(stroke)
            if sig not in seen and tuple(reversed(stroke)) not in seen:
                seen.add(sig)
                out.append(stroke)
    return out


def segment(a, b, cut_start, cut_end, notch, w=WIDTH):
    """A stroke from a to b as a polygon.

    A free end is cut on a diagonal (the two corners are CHAMFER apart along the stroke, both ends parallel, like a
    slash). A joint end goes on by half the width, so two strokes meet with no gap. [notch] is (t from 0 to 1, side).
    """
    (ax, ay), (bx, by) = a, b
    length = math.hypot(bx - ax, by - ay)
    ux, uy = (bx - ax) / length, (by - ay) / length
    nx, ny = -uy, ux
    h, c = w / 2, CHAMFER / 2

    def at(t, side, depth=0.0):
        k = (h - depth) * side
        return (ax + ux * t + nx * k, ay + uy * t + ny * k)

    s_left, s_right = (-c, c) if cut_start else (-h, -h)
    e_left, e_right = (length - c, length + c) if cut_end else (length + h, length + h)
    left, right = [at(s_left, 1)], [at(e_right, -1)]
    if notch:
        t, side = notch[0] * length, notch[1]
        dent = [at(t - NOTCH_HALF, side), at(t, side, NOTCH_DEPTH), at(t + NOTCH_HALF, side)]
        if side == 1:
            left += dent
        else:
            right += list(reversed(dent))
    left.append(at(e_left, 1))
    right.append(at(s_right, -1))
    return left + right


def polygons(strokes: list, seed: str) -> list:
    rng = random.Random(seed)
    polys = []
    for stroke in strokes:
        closed = stroke[0] == stroke[-1]
        for i in range(len(stroke) - 1):
            a, b = stroke[i], stroke[i + 1]
            long_enough = math.hypot(b[0] - a[0], b[1] - a[1]) > 30
            notch = (rng.uniform(0.35, 0.65), rng.choice((1, -1))) if long_enough and rng.random() < 0.7 else None
            cut_start = not closed and i == 0
            cut_end = not closed and i == len(stroke) - 2
            polys.append(segment(a, b, cut_start, cut_end, notch))
    return polys


def path_of(polys: list) -> str:
    return "".join(
        "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in poly) + "Z" for poly in polys
    )


def svg(polys: list, title: str, neon: str | None = None) -> str:
    d = path_of(polys)
    if neon is None:
        body = f'<path fill="currentColor" d="{d}"/>'
        box = "0 0 100 100"
    else:
        fid = "glow-" + slug(title.split(":")[0])
        body = (
            f'<defs><filter id="{fid}" x="-30%" y="-30%" width="160%" height="160%">'
            f'<feGaussianBlur stdDeviation="3.2" result="b1"/><feGaussianBlur stdDeviation="1.2" result="b2"/>'
            f'<feMerge><feMergeNode in="b1"/><feMergeNode in="b2"/><feMergeNode in="SourceGraphic"/></feMerge>'
            f'</filter></defs><path fill="{neon}" filter="url(#{fid})" d="{d}"/>'
        )
        box = "-8 -8 116 116"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{box}" role="img" aria-label="{escape(title)}">'
        f"<title>{escape(title)}</title>{body}</svg>\n"
    )


FIRST_CODEPOINT = 0x100000
EM = 1000


def font_contour(poly):
    """Grid (y down, 0..100) to font units (y up). The cell is square; the rune sits from -50 to 750."""
    pts = [(round(x * 10), round((100 - y) * 10 - 150)) for x, y in poly]
    area = sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]))
    return pts if area < 0 else list(reversed(pts))   # TrueType outer contours go clockwise


def build_font(glyphs: list) -> Path:
    from fontTools.fontBuilder import FontBuilder
    from fontTools.pens.ttGlyphPen import TTGlyphPen

    order = [".notdef"] + [g for g, _, _ in glyphs]
    fb = FontBuilder(EM, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap({cp: g for g, cp, _ in glyphs})
    outlines = {".notdef": TTGlyphPen(None).glyph()}
    for g, _, polys in glyphs:
        pen = TTGlyphPen(None)
        for poly in polys:
            pts = font_contour(poly)
            pen.moveTo(pts[0])
            for pt in pts[1:]:
                pen.lineTo(pt)
            pen.closePath()
        outlines[g] = pen.glyph()
    fb.setupGlyf(outlines)
    for g in outlines.values():
        if g.numberOfContours > 0:
            g.flags[0] |= 0x40   # OVERLAP_SIMPLE: the strokes overlap, draw them as one shape
    fb.setupHorizontalMetrics({g: (EM, 0) for g in order})
    fb.setupHorizontalHeader(ascent=800, descent=-200)
    fb.setupNameTable({"familyName": "RuneChest Runes", "styleName": "Regular",
                       "uniqueFontIdentifier": "RuneChest Runes Regular 1.0", "fullName": "RuneChest Runes",
                       "psName": "RuneChestRunes-Regular", "version": "Version 1.0"})
    fb.setupOS2(sTypoAscender=800, sTypoDescender=-200, usWinAscent=800, usWinDescent=200,
                fsType=0, achVendID="RNCH")
    fb.setupPost(isFixedPitch=1)
    fb.font["head"].created = fb.font["head"].modified = 3_846_528_000   # fixed (2025-11-21), so a rebuild is the same file
    out = HERE / "RuneChestRunes.ttf"
    fb.save(str(out))
    return out


def main() -> None:
    cards, glyphs = [], []
    for i, (name, initial, role_rune, role, today, layer, neon) in enumerate(CREW):
        title = f"{name}: {RUNES[initial][0]} + {RUNES[role_rune][0]}"
        polys = polygons(strokes_of(initial, role_rune), name)
        glyphs.append((slug(name), FIRST_CODEPOINT + i, polys))
        mono, glow = svg(polys, title), svg(polys, title, neon)
        (HERE / f"{slug(name)}.svg").write_text(mono, encoding="utf-8")
        (HERE / f"{slug(name)}-neon.svg").write_text(glow, encoding="utf-8")
        parts = "".join(
            f'<figure><div class="mini">{svg(polygons(strokes_of(k), k), k)}</div>'
            f'<figcaption>{RUNES[k][0]} {k.split("_")[0]}</figcaption></figure>'
            for k in (initial, role_rune)
        )
        sizes = "".join(
            f'<span class="tab" style="--s:{px}px;--c:{neon}">{mono}<i>{escape(name)}</i></span>' for px in (14, 18, 24)
        )
        cards.append(
            f'<article style="--c:{neon}"><div class="big">{glow}</div>'
            f'<h2>{escape(name)}</h2><p class="role">{escape(role)} · {layer} · hoje {escape(today)}</p>'
            f'<div class="parts">{parts}</div><div class="sizes">{sizes}</div></article>'
        )
    (HERE / "preview.html").write_text(PAGE.replace("{{CARDS}}", "\n".join(cards)), encoding="utf-8")
    print(f"{len(CREW)} runes (mono + neon) -> {HERE}")
    table = "\n".join(f"{n}\tU+{FIRST_CODEPOINT + i:06X}\t{c}\t{r}\t{t}"
                      for i, (n, _a, _b, r, t, _l, c) in enumerate(CREW))
    (HERE / "codepoints.tsv").write_text("agent\tcodepoint\tneon\trole\ttoday\n" + table + "\n", encoding="utf-8")
    try:
        font = build_font(glyphs)
    except ImportError:
        print("fontTools is missing: .venv/bin/pip install fonttools (the SVGs are done)")
        return
    print(f"font -> {font}")
    if "--install" in sys.argv:
        dest = Path.home() / "Library" / "Fonts" / font.name
        shutil.copyfile(font, dest)
        print(f"installed -> {dest}")
        if shutil.which("swift"):
            import subprocess
            subprocess.run(["swift", str(HERE / "register.swift"), str(dest)], check=False)


PAGE = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Runas RuneChest</title>
<style>
:root{--bg:#0e0e14;--surface:#13131b;--line:#2e2e3e;--text:#d8dae5;--dim:#878ca6}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.5 "JetBrainsMono Nerd Font",ui-monospace,monospace;padding:32px 16px}
header{max-width:1200px;margin:0 auto 24px}h1{font:italic 32px "Monaspace Radon",ui-monospace,monospace;margin:0 0 6px;color:#ff2a6d;text-shadow:0 0 12px #ff2a6d88}
header p{color:var(--dim);margin:0}main{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}
article{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:18px;box-shadow:inset 0 1px 0 #ffffff08}
.big{width:150px;height:150px;margin:0 auto 6px}.big svg{width:100%;height:100%}
h2{font:italic 24px "Monaspace Radon",ui-monospace,monospace;text-align:center;margin:0;color:var(--c);text-shadow:0 0 10px color-mix(in srgb,var(--c) 55%,transparent)}
.role{text-align:center;color:var(--dim);font-size:13px;margin:2px 0 12px}
.parts{display:flex;justify-content:center;gap:18px}.parts figure{margin:0;text-align:center}
.mini{color:var(--dim);width:40px;height:40px;margin:0 auto}.mini svg{width:100%;height:100%}
figcaption{font-size:12px;color:var(--dim)}
.sizes{display:flex;flex-direction:column;gap:6px;margin-top:14px;border-top:1px solid var(--line);padding-top:12px}
.sizes::before{content:"no terminal (cor sólida, sem brilho)";font-size:11px;color:var(--dim)}
.tab{display:flex;align-items:center;gap:6px;font-size:var(--s);color:var(--text)}.tab svg{width:var(--s);height:var(--s);color:var(--c)}
.tab i{font-family:"Monaspace Radon",ui-monospace,monospace}
</style></head><body>
<header><h1>Runas do RuneChest · rascunho 3</h1>
<p>Traços Mad Max: pontas cortadas em diagonal e entalhes em V. Neon por camada, com brilho fora do terminal. Embaixo de cada runa: as duas runas da combinação e como fica na aba (14, 18 e 24 px).</p></header>
<main>
{{CARDS}}
</main></body></html>
"""

if __name__ == "__main__":
    main()
