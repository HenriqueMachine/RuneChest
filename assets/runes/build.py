#!/usr/bin/env python3
"""Deepdeck runes, draft 2: one bind-rune per agent (the rune of the first letter + the rune of the role).

Each base rune is a list of strokes on a 100x100 grid. Most runes share the central stave (x=50, y=10..90), so two
runes bind on it. The script writes one SVG per agent (monochrome, currentColor) and preview.html to compare them.
Run: python3 -I assets/runes/build.py
"""
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAVE = [(50, 10), (50, 90)]

# Base runes (Elder Futhark). A stroke is a polyline. The names follow the Unicode names.
RUNES = {
    "fehu":     ("ᚠ", [STAVE, [(50, 40), (76, 18)], [(50, 62), (76, 40)]]),
    "uruz":     ("ᚢ", [STAVE, [(50, 10), (76, 34), (76, 90)]]),
    "ansuz":    ("ᚨ", [STAVE, [(50, 14), (74, 32)], [(50, 36), (74, 54)]]),
    "raidho":   ("ᚱ", [STAVE, [(50, 10), (74, 28), (50, 46), (76, 90)]]),
    "kenaz":    ("ᚲ", [STAVE, [(76, 22), (50, 44), (76, 66)]]),
    "gebo":     ("ᚷ", [[(24, 18), (76, 82)], [(76, 18), (24, 82)]]),
    "wunjo":    ("ᚹ", [STAVE, [(50, 10), (74, 26), (50, 42)]]),
    "hagalaz":  ("ᚼ", [STAVE, [(26, 30), (74, 70)], [(74, 30), (26, 70)]]),
    "naudiz":   ("ᚾ", [STAVE, [(32, 36), (68, 64)]]),
    "eihwaz":   ("ᛇ", [STAVE, [(50, 10), (70, 26)], [(50, 90), (30, 74)]]),
    "algiz":    ("ᛉ", [STAVE, [(50, 46), (26, 18)], [(50, 46), (74, 18)]]),
    "tiwaz":    ("ᛏ", [STAVE, [(50, 10), (26, 34)], [(50, 10), (74, 34)]]),
    "berkano":  ("ᛒ", [STAVE, [(50, 10), (74, 30), (50, 50), (74, 70), (50, 90)]]),
    "ehwaz":    ("ᛖ", [[(26, 90), (26, 12), (50, 36), (74, 12), (74, 90)]]),
    "mannaz":   ("ᛗ", [[(26, 90), (26, 10), (74, 46)], [(74, 90), (74, 10), (26, 46)]]),
    "laguz":    ("ᛚ", [STAVE, [(50, 10), (72, 32)]]),
    # Variants: the same rune moved up, down or to the left, so it does not hide inside the other rune of a bind.
    "algiz_high":  ("ᛉ", [STAVE, [(50, 40), (24, 12)], [(50, 40), (76, 12)]]),
    "hagalaz_ᚺ":   ("ᚺ", [STAVE, [(28, 60), (72, 84)]]),
    "hagalaz_low": ("ᚼ", [STAVE, [(28, 54), (72, 86)], [(72, 54), (28, 86)]]),
    "naudiz_high": ("ᚾ", [STAVE, [(32, 14), (68, 38)]]),
    "wunjo_left":  ("ᚹ", [STAVE, [(50, 10), (26, 26), (50, 42)]]),
    "othala":   ("ᛟ", [[(50, 10), (74, 38), (50, 66), (26, 38), (50, 10)], [(38, 52), (24, 90)], [(62, 52), (76, 90)]]),
}

# Agent: (initial rune, role rune, role, today's name). Grisnir and Gnjóstr share G, so Gnjóstr takes N.
CREW = [
    ("Odin",     "othala",  "ansuz",   "Orquestrador", "Swain"),
    ("Heimdall", "hagalaz_ᚺ", "algiz_high",   "Integrador do backend", "Galio"),
    ("Forseti",  "fehu",    "tiwaz",   "Integrador do app", "Taric"),
    ("Eitri",    "ehwaz",   "kenaz",   "Executor do backend", "Viktor"),
    ("Völundr",  "wunjo",   "gebo",    "Executor do app", "Heimerdinger"),
    ("Brokkr",   "berkano", "fehu",    "Ajudante de Eitri", "Xayah"),
    ("Egill",    "ehwaz",   "eihwaz",  "Ajudante de Völundr", "Rakan"),
    ("Grisnir",  "gebo",    "uruz",    "Mecânico de Eitri", "Ziggs"),
    ("Gnjóstr",  "naudiz",  "uruz",    "Mecânico de Völundr", "Rumble"),
    ("Mímir",    "mannaz",  "laguz",   "IA full-stack", "Zilean"),
    ("Bifröst",  "berkano", "raidho",  "Integrações", "Thresh"),
    ("Bragi",    "berkano", "wunjo_left",   "Texto, design, PDFs", "Lupin"),
    ("Níðhöggr", "naudiz_high", "hagalaz_low", "Código morto e refatoração", "Pyke"),
]


def slug(name: str) -> str:
    table = str.maketrans("öíðÖÍÐó", "oidOIDo")
    return name.translate(table).lower()


def strokes_of(*keys: str) -> list:
    seen, out = set(), []
    for key in keys:
        for stroke in RUNES[key][1]:
            sig = tuple(stroke)
            if sig not in seen and tuple(reversed(stroke)) not in seen:
                seen.add(sig)
                out.append(stroke)
    return out


def svg(strokes: list, title: str, width: float = 8) -> str:
    lines = "".join(
        f'<polyline points="{" ".join(f"{x},{y}" for x, y in s)}"/>' for s in strokes
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="{escape(title)}">'
        f"<title>{escape(title)}</title>"
        f'<g fill="none" stroke="currentColor" stroke-width="{width}" stroke-linecap="square" '
        f'stroke-linejoin="miter">{lines}</g></svg>\n'
    )


def main() -> None:
    cards = []
    for name, initial, role_rune, role, today in CREW:
        title = f"{name}: {RUNES[initial][0]} + {RUNES[role_rune][0]}"
        bound = strokes_of(initial, role_rune)
        (HERE / f"{slug(name)}.svg").write_text(svg(bound, title), encoding="utf-8")
        parts = "".join(
            f'<figure><div class="mini">{svg(strokes_of(k), k, 9)}</div>'
            f"<figcaption>{RUNES[k][0]} {k.split("_")[0]}</figcaption></figure>"
            for k in (initial, role_rune)
        )
        sizes = "".join(f'<span class="tab" style="--s:{px}px">{svg(bound, name, 10)}<i>{escape(name)}</i></span>'
                        for px in (14, 18, 24))
        cards.append(
            f'<article><div class="big">{svg(bound, title)}</div>'
            f'<h2>{escape(name)}</h2><p class="role">{escape(role)} · hoje {escape(today)}</p>'
            f'<div class="parts">{parts}</div><div class="sizes">{sizes}</div></article>'
        )
    page = PAGE.replace("{{CARDS}}", "\n".join(cards))
    (HERE / "preview.html").write_text(page, encoding="utf-8")
    print(f"{len(CREW)} runes -> {HERE}")


PAGE = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Runas Deepdeck</title>
<style>
:root{--bg:#0e0e14;--surface:#16161f;--line:#2e2e3e;--text:#d8dae5;--dim:#878ca6;--mag:#e8457a;--cyan:#4cc9d6;--yel:#e6c84c}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.5 "JetBrainsMono Nerd Font",ui-monospace,monospace;padding:32px 16px}
header{max-width:1200px;margin:0 auto 24px}h1{font:italic 32px "Monaspace Radon",ui-monospace,monospace;margin:0 0 6px;color:var(--mag)}
header p{color:var(--dim);margin:0}main{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}
article{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:18px}
.big{color:var(--mag);width:120px;height:120px;margin:4px auto 10px}.big svg{width:100%;height:100%}
h2{font:italic 24px "Monaspace Radon",ui-monospace,monospace;text-align:center;margin:0}
.role{text-align:center;color:var(--dim);font-size:13px;margin:2px 0 12px}
.parts{display:flex;justify-content:center;gap:18px}.parts figure{margin:0;text-align:center}
.mini{color:var(--cyan);width:44px;height:44px;margin:0 auto}.mini svg{width:100%;height:100%}
figcaption{font-size:12px;color:var(--dim)}
.sizes{display:flex;flex-direction:column;gap:6px;margin-top:14px;border-top:1px solid var(--line);padding-top:12px}
.tab{display:flex;align-items:center;gap:6px;font-size:var(--s);color:var(--text)}.tab svg{width:var(--s);height:var(--s);color:var(--mag)}
.tab i{font-family:"Monaspace Radon",ui-monospace,monospace}
</style></head><body>
<header><h1>Runas do Deepdeck · rascunho 2</h1>
<p>Cada runa junta a runa da inicial do nome (à esquerda) com a runa do papel (à direita) no mesmo eixo. Embaixo: como fica na aba em 14, 18 e 24 px.</p></header>
<main>
{{CARDS}}
</main></body></html>
"""

if __name__ == "__main__":
    main()
