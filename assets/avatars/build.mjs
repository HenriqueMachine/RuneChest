// RuneChest crew avatars (open-bot-avatar v1, MIT): one Norse object or creature per agent, with two eyes.
// Each body is built from rounded primitives (circles, capsules, rounded rects, polygons) that overlap into one
// silhouette. All outlines wind clockwise (nonzero fill); holes wind counter-clockwise.
// Output: definitions/<id>.json (the avatar spec), still/<id>.svg (neon colour of the layer), sheet.html.
// Run: node assets/avatars/build.mjs   (from the repo root, after `npm install` in assets/avatars)
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { renderAvatarSvg, validateAvatar } from "open-bot-avatar";

const HERE = dirname(fileURLToPath(import.meta.url));
const f = (n) => Number(n.toFixed(1));

// Clockwise circle / ellipse.
const ellipse = (cx, cy, rx, ry = rx) =>
  `M${f(cx - rx)} ${f(cy)}A${f(rx)} ${f(ry)} 0 1 1 ${f(cx + rx)} ${f(cy)}A${f(rx)} ${f(ry)} 0 1 1 ${f(cx - rx)} ${f(cy)}Z`;
// Clockwise rounded rectangle.
const rect = (x, y, w, h, r = 4) => {
  r = Math.min(r, w / 2, h / 2);
  return `M${f(x + r)} ${f(y)}H${f(x + w - r)}A${f(r)} ${f(r)} 0 0 1 ${f(x + w)} ${f(y + r)}V${f(y + h - r)}` +
    `A${f(r)} ${f(r)} 0 0 1 ${f(x + w - r)} ${f(y + h)}H${f(x + r)}A${f(r)} ${f(r)} 0 0 1 ${f(x)} ${f(y + h - r)}` +
    `V${f(y + r)}A${f(r)} ${f(r)} 0 0 1 ${f(x + r)} ${f(y)}Z`;
};
// Polygon, forced clockwise on screen (y down: positive shoelace sum).
const poly = (...pts) => {
  const area = pts.reduce((s, [x1, y1], i) => {
    const [x2, y2] = pts[(i + 1) % pts.length];
    return s + (x1 * y2 - x2 * y1);
  }, 0);
  const p = area > 0 ? pts : [...pts].reverse();
  return "M" + p.map(([x, y]) => `${f(x)} ${f(y)}`).join("L") + "Z";
};
// A chunky curved part: overlapping circles along a list of [x, y, r].
const beads = (list) => list.map(([x, y, r]) => ellipse(x, y, r)).join("");

const CREW = [
  {
    id: "odin", name: "Odin", object: "corvo", neon: "#f9f002",
    path: ellipse(46, 58, 28, 22) + ellipse(70, 37, 14) + poly([79, 30], [94, 40], [79, 46]) +
      poly([24, 50], [7, 47], [11, 56], [6, 63], [26, 67]) + rect(37, 76, 7, 13, 3) + rect(51, 76, 7, 13, 3),
    eyes: { x: 45, y: 55, spacing: 16, scale: 1.1 },
  },
  {
    id: "heimdall", name: "Heimdall", object: "Gjallarhorn", neon: "#05d9e8",
    path: ellipse(64, 56, 22, 26) + rect(80, 26, 10, 60, 5) +
      beads([[45, 62, 14], [33, 60, 11], [23, 53, 8.5], [16, 44, 7], [13, 34, 6], [13, 25, 5.5]]),
    eyes: { x: 63, y: 53, spacing: 16, scale: 1.1 },
  },
  {
    id: "forseti", name: "Forseti", object: "balança", neon: "#ff2a6d",
    path: rect(26, 52, 48, 36, 12) + rect(45, 20, 10, 36, 4) + rect(12, 16, 76, 10, 5) +
      rect(18, 22, 6, 18, 3) + rect(76, 22, 6, 18, 3) + rect(9, 36, 24, 10, 5) + rect(67, 36, 24, 10, 5),
    eyes: { x: 50, y: 69, spacing: 16, scale: 1.05 },
  },
  {
    id: "eitri", name: "Eitri", object: "martelo", neon: "#3d9bff",
    path: rect(12, 16, 76, 38, 9) + rect(43, 50, 14, 32, 5) + ellipse(50, 84, 7),
    eyes: { x: 50, y: 35, spacing: 18, scale: 1.1 },
  },
  {
    id: "volundr", name: "Völundr", object: "asa", neon: "#ff4fd8",
    path: ellipse(44, 36, 32, 20) + ellipse(76, 24, 11) + rect(13, 40, 14, 46, 7) + rect(27, 44, 14, 40, 7) +
      rect(41, 46, 14, 32, 7) + rect(55, 46, 14, 24, 7) + rect(69, 40, 14, 16, 7),
    eyes: { x: 42, y: 34, spacing: 16, scale: 1.1 },
  },
  {
    id: "brokkr", name: "Brokkr", object: "fole", neon: "#8cc2ff",
    path: ellipse(46, 52, 29) + poly([70, 44], [91, 49], [91, 57], [70, 62]) +
      rect(8, 28, 20, 9, 4.5) + rect(8, 67, 20, 9, 4.5),
    eyes: { x: 45, y: 49, spacing: 16, scale: 1.1 },
  },
  {
    id: "egill", name: "Egill", object: "aljava", neon: "#ff9ce9",
    path: rect(29, 36, 42, 52, 11) + rect(35, 22, 7, 18, 3) + rect(47, 18, 7, 22, 3) + rect(58, 24, 7, 16, 3) +
      poly([38.5, 13], [44, 23], [33, 23]) + poly([50.5, 9], [56, 19], [45, 19]) + poly([61.5, 15], [67, 25], [56, 25]),
    eyes: { x: 50, y: 60, spacing: 16, scale: 1.1 },
  },
  {
    id: "grisnir", name: "Grisnir", object: "bode", neon: "#c4e0ff",
    path: ellipse(50, 54, 23, 26) + ellipse(50, 77, 15, 11) + rect(9, 44, 22, 10, 5) + rect(69, 44, 22, 10, 5) +
      beads([[39, 31, 7], [33, 22, 6], [26, 16, 5.5], [20, 15, 5]]) + beads([[61, 31, 7], [67, 22, 6], [74, 16, 5.5], [80, 15, 5]]),
    eyes: { x: 50, y: 52, spacing: 16, scale: 1.1 },
  },
  {
    id: "gnjostr", name: "Gnjóstr", object: "bode de perfil", neon: "#ffc9f3",
    path: ellipse(42, 52, 25, 21) + rect(54, 50, 33, 20, 10) + poly([65, 66], [78, 66], [70, 89]) +
      beads([[34, 32, 7.5], [26, 26, 7], [18, 25, 6.5], [14, 30, 6], [14, 38, 5.5]]) + rect(14, 47, 15, 8, 4),
    eyes: { x: 40, y: 49, spacing: 16, scale: 1.1 },
  },
  {
    id: "mimir", name: "Mímir", object: "cabeça no poço", neon: "#ffb000",
    path: ellipse(50, 44, 27) + rect(16, 66, 68, 22, 7) + rect(11, 62, 78, 9, 4.5),
    eyes: { x: 50, y: 40, spacing: 17, scale: 1.1 },
  },
  {
    id: "bifrost", name: "Bifröst", object: "ponte arco-íris", neon: "#00ff9f",
    path: "M9 86V60A41 41 0 0 1 91 60V86H71V62A21 21 0 0 0 29 62V86Z",
    eyes: { x: 50, y: 30, spacing: 16, scale: 1.05 },
  },
  {
    id: "bragi", name: "Bragi", object: "lira", neon: "#c77dff",
    path: rect(22, 50, 56, 38, 13) + rect(22, 18, 11, 40, 5.5) + rect(67, 18, 11, 40, 5.5) + rect(18, 12, 64, 11, 5.5),
    eyes: { x: 50, y: 68, spacing: 17, scale: 1.1 },
  },
  {
    // Frigg spins the clouds: a spindle with its whorl (product and design, 18/11).
    id: "frigg", name: "Frigg", object: "roca", neon: "#b8ff3d",
    path: ellipse(50, 56, 22, 27) + rect(46, 10, 8, 80, 4) + ellipse(50, 84, 19, 6) + ellipse(50, 12, 5.5),
    eyes: { x: 50, y: 54, spacing: 16, scale: 1.1 },
  },
  {
    id: "nidhoggr", name: "Níðhöggr", object: "dragão", neon: "#ff7a3d",
    path: ellipse(42, 52, 26, 22) + rect(54, 47, 37, 22, 9) + rect(57, 65, 28, 9, 4.5) + rect(11, 62, 23, 26, 8) +
      beads([[28, 32, 7], [21, 26, 6], [15, 21, 5.5]]) + beads([[44, 30, 6.5], [41, 21, 5.5]]) +
      poly([13, 66], [8, 72], [14, 77]) + poly([13, 76], [8, 82], [14, 86]),
    eyes: { x: 39, y: 49, spacing: 16, scale: 1.1 },
  },
];

mkdirSync(join(HERE, "definitions"), { recursive: true });
mkdirSync(join(HERE, "still"), { recursive: true });
let failed = 0;
const cards = [];
for (const a of CREW) {
  const def = { version: 1, id: a.id, name: a.name, body: { path: a.path }, eyes: a.eyes };
  const res = validateAvatar(def);
  if (!res.ok) {
    failed++;
    console.log(`✗ ${a.name}:`, JSON.stringify(res.errors));
    continue;
  }
  writeFileSync(join(HERE, "definitions", `${a.id}.json`), JSON.stringify(def, null, 2) + "\n");
  const svg = renderAvatarSvg(res.value, { color: a.neon, eyeColor: "#0e0e14", size: 256 });
  writeFileSync(join(HERE, "still", `${a.id}.svg`), svg);
  cards.push(`<figure style="--c:${a.neon}">${svg}<figcaption><b>${a.name}</b><span>${a.object}</span></figcaption></figure>`);
  console.log(`✓ ${a.name} (${a.path.length} chars)`);
}
writeFileSync(join(HERE, "sheet.html"), `<!doctype html><meta charset=utf-8><title>RuneChest avatars</title>
<style>body{margin:0;padding:24px;background:#0e0e14;color:#d8dae5;font:15px "JetBrainsMono Nerd Font",monospace}
main{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px}
figure{margin:0;background:#13131b;border:1px solid #2e2e3e;border-radius:10px;padding:12px;text-align:center}
figure svg{width:160px;height:160px;filter:drop-shadow(0 0 10px color-mix(in srgb,var(--c) 60%,transparent))}
figcaption b{display:block;color:var(--c);font:italic 20px "Monaspace Radon",monospace}figcaption span{color:#878ca6;font-size:12px}</style>
<main>${cards.join("\n")}</main>`);
// The crew page (GitHub Pages, docs/): one JSON with each definition, its neon, its role and its rune (neon SVG).
const ROLES = {
  odin: "Orquestrador", heimdall: "Integrador do backend", forseti: "Integrador do app", eitri: "Executor do backend",
  volundr: "Executor do app", brokkr: "Ajudante de Eitri", egill: "Ajudante de Völundr", grisnir: "Mecânico de Eitri",
  gnjostr: "Mecânico de Völundr", mimir: "IA full-stack", bifrost: "Integrações", bragi: "Texto, design, PDFs",
  nidhoggr: "Código morto e refatoração",
};
const runesDir = join(HERE, "..", "runes");
const page = CREW.map((a) => ({
  id: a.id, name: a.name, object: a.object, neon: a.neon, role: ROLES[a.id],
  definition: { version: 1, id: a.id, name: a.name, body: { path: a.path }, eyes: a.eyes },
  rune: readFileSync(join(runesDir, `${a.id}-neon.svg`), "utf8").trim(),
}));
const site = join(HERE, "..", "..", "docs", "crew");
mkdirSync(site, { recursive: true });
writeFileSync(join(site, "crew.json"), JSON.stringify(page) + "\n");
writeFileSync(join(site, "banner.svg"), readFileSync(join(runesDir, "banner.svg"), "utf8"));
console.log(failed ? `${failed} failed` : "all valid");
process.exitCode = failed ? 1 : 0;
