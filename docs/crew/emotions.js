// RuneChest crew emotions: a small canvas renderer on top of open-bot-avatar.
// The engine gives each frame (body cross-sections and the eye positions in the face plane, see avatarFrame).
// We paint the body as the engine computes it and draw our OWN eyes, so each emotion has its own face:
//   idle        calm open eyes (the engine pills)
//   focused     half-closed, flat lids: concentrated            · symbol "…"  · glow breathes
//   suspicious  one eye squinted, looks to the side, head tilted · symbol "?"
//   worried     droopy lids, small eyes, a sweat drop, a short tremble now and then · symbol "!" · colour turns red
//   celebrating the engine's happy arcs, a hop, sparkles, bright glow (only for 2 min after a PR merge)
// "Expressive but calm" (user, 17/11): short and slow motions; only the celebration is quick.
import { avatarFrame } from "./vendor/open-bot-avatar/index.js";

export const STATES = ["idle", "focused", "suspicious", "worried", "celebrating"];
export const WORDS = {
  idle: "em espera", focused: "focado", suspicious: "revisando", worried: "bloqueado", celebrating: "comemorando",
};
const ENGINE_MOOD = { idle: "idle", focused: "thinking", suspicious: "idle", worried: "idle", celebrating: "happy" };
const SYMBOL = { idle: "", focused: "…", suspicious: "?", worried: "!", celebrating: "✦" };
const reduced = matchMedia("(prefers-reduced-motion: reduce)");

function mix(hex, other, t) {
  const a = hex.match(/\w\w/g).map((h) => parseInt(h, 16));
  const b = other.match(/\w\w/g).map((h) => parseInt(h, 16));
  return "#" + a.map((v, i) => Math.round(v + (b[i] - v) * t).toString(16).padStart(2, "0")).join("");
}
const mul = (m, n) => [
  m[0] * n[0] + m[2] * n[1], m[1] * n[0] + m[3] * n[1],
  m[0] * n[2] + m[2] * n[3], m[1] * n[2] + m[3] * n[3],
  m[0] * n[4] + m[2] * n[5] + m[4], m[1] * n[4] + m[3] * n[5] + m[5],
];

/** One live avatar in `host` (a square element). Returns { set(state), look(gaze|null), destroy() }. */
export function mountEmotion(host, { definition, color, ink = "#0e0e14", state = "idle", rest = null, label = "" }) {
  const wrap = document.createElement("div");
  wrap.className = "emo";
  wrap.setAttribute("role", "img");
  wrap.setAttribute("aria-label", label);
  const canvas = document.createElement("canvas");
  const symbol = document.createElement("span");
  symbol.className = "emo-symbol";
  symbol.setAttribute("aria-hidden", "true");
  wrap.append(canvas, symbol);
  host.append(wrap);
  const ctx = canvas.getContext("2d");
  const paths = new Map();
  let current = state, since = performance.now(), pointer = null, gaze = { x: 0, y: 0 }, raf = 0, alive = true;

  function size() {
    const px = host.clientWidth || 150, dpr = Math.min(devicePixelRatio || 1, 2);
    canvas.width = canvas.height = Math.round(px * dpr);
    canvas.style.width = canvas.style.height = px + "px";
  }
  size();
  const ro = new ResizeObserver(size);
  ro.observe(host);

  function apply() {
    wrap.dataset.state = current;
    symbol.textContent = SYMBOL[current];
    const tint = current === "worried" ? mix(color, "#ff3b3b", 0.35) : color;
    wrap.style.setProperty("--emo", tint);
  }
  apply();

  function target(now) {
    if (pointer) return pointer;
    if (current === "suspicious") return { x: rest?.x > 0 ? 0.75 : -0.75, y: 0.05 };
    if (current === "focused") return { x: (rest?.x ?? 0) * 0.4, y: 0.45 };
    if (current === "worried") return { x: Math.sin(now / 900) * 0.35, y: -0.2 };
    return rest ?? { x: Math.sin(now / 2300) * 0.25, y: Math.cos(now / 3100) * 0.15 };
  }

  function drawEye(mark, m, s, side) {
    ctx.setTransform(...m.map((v, i) => (i < 4 ? v * s : v * s)));
    ctx.fillStyle = ink;
    if (mark.shape === "arc") {
      ctx.lineWidth = mark.strokeWidth; ctx.lineCap = "round"; ctx.strokeStyle = ink;
      ctx.stroke(new Path2D(mark.d));
      return;
    }
    const { x, y, width: w, height: h } = mark, r = w / 2;
    // A lid: the eye is cut by a slanted line, from `outer` (fraction of h at the outer corner) to `inner`.
    const lid = (side, outer, inner, top, bottom) => {
      const left = side === "left";
      ctx.save();
      ctx.beginPath();
      ctx.moveTo(x - 3, y + h * (left ? outer : inner));
      ctx.lineTo(x + w + 3, y + h * (left ? inner : outer));
      ctx.lineTo(x + w + 3, y + h + 3); ctx.lineTo(x - 3, y + h + 3); ctx.closePath();
      ctx.clip();
      pill(top, bottom);
      ctx.restore();
    };
    function pill(top, bottom) {
      ctx.beginPath();
      ctx.roundRect(x, top, w, Math.max(bottom - top, 1.2), Math.min(r, (bottom - top) / 2));
      ctx.fill();
    }
    if (current === "focused") {
      lid(side, 0.18, 0.5, y + h * 0.1, y + h);        // lids slanting down to the nose: determined
    } else if (current === "suspicious") {
      side === "far" ? pill(y + h * 0.5, y + h * 0.82) : pill(y + h * 0.08, y + h);  // one squints
    } else if (current === "worried") {
      lid(side, 0.55, 0.2, y + h * 0.15, y + h * 0.92); // lids slanting down to the outside: sad
    } else {
      pill(y, y + h);
    }
  }

  function frame(now) {
    if (!alive) return;
    const t = target(now), k = reduced.matches ? 1 : 0.08;
    gaze = { x: gaze.x + (t.x - gaze.x) * k, y: gaze.y + (t.y - gaze.y) * k };
    const f = avatarFrame(definition, {
      color, eyeColor: ink, time: (now - since) / 1000 + 1, motion: ENGINE_MOOD[current],
      gaze: { ...gaze, weight: 1 }, reducedMotion: reduced.matches,
    });
    for (const p of f.paths) if (!paths.has(p.id)) paths.set(p.id, new Path2D(p.d));
    const s = canvas.width / 100;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const body = current === "worried" ? mix(color, "#ff3b3b", 0.35) : color;
    const eyes = f.shapes.filter((sh) => sh.kind === "eye" && sh.mark.shape === "pill");
    const xs = eyes.map((e) => mul(f.root, e.matrix)[4] + e.mark.x);
    const leftX = Math.min(...xs);
    for (const sh of f.shapes) {
      const m = mul(f.root, sh.matrix);
      if (sh.kind === "slice") {
        ctx.setTransform(m[0] * s, m[1] * s, m[2] * s, m[3] * s, m[4] * s, m[5] * s);
        ctx.fillStyle = body;
        ctx.fill(paths.get(sh.path));
      } else {
        const ex = m[4] + (sh.mark.x ?? 0);
        const side = current === "suspicious"
          ? ((gaze.x > 0) === (ex === leftX) ? "far" : "near")
          : ex === leftX ? "left" : "right";
        drawEye(sh.mark, [m[0], m[1], m[2], m[3], m[4], m[5]], s, side);
      }
    }
    raf = requestAnimationFrame(frame);
  }
  raf = requestAnimationFrame(frame);

  return {
    set(next) {
      if (next === current || !STATES.includes(next)) return;
      current = next; since = performance.now(); apply();
    },
    get state() { return current; },
    look(g) { pointer = g; },
    destroy() { alive = false; cancelAnimationFrame(raf); ro.disconnect(); wrap.remove(); },
  };
}

export const EMOTION_CSS = `
.emo{position:relative;width:100%;height:100%}
.emo canvas{display:block;filter:drop-shadow(0 0 10px color-mix(in srgb,var(--emo) 45%,transparent));transition:filter .6s}
.emo-symbol{position:absolute;top:2%;right:6%;font:700 22px/1 "JetBrains Mono",ui-monospace,monospace;color:var(--emo);
  text-shadow:0 0 8px var(--emo);opacity:.95}
.emo[data-state="idle"] canvas{filter:drop-shadow(0 0 6px color-mix(in srgb,var(--emo) 30%,transparent))}
.emo[data-state="focused"] canvas{animation:emo-breathe 3.2s ease-in-out infinite}
.emo[data-state="focused"] .emo-symbol{animation:emo-dots 1.6s steps(4) infinite;letter-spacing:-2px}
.emo[data-state="suspicious"]{transform:rotate(-6deg);transition:transform .8s}
.emo[data-state="worried"]{animation:emo-tremble 4s ease-in-out infinite}
.emo[data-state="worried"]::after{content:"";position:absolute;left:22%;top:20%;width:9px;height:13px;
  background:#7ad9e3;border-radius:50% 50% 50% 50%/60% 60% 40% 40%;clip-path:polygon(50% 0,100% 60%,100% 100%,0 100%,0 60%);
  opacity:.85;animation:emo-drop 3s ease-in infinite}
.emo[data-state="celebrating"]{animation:emo-hop .7s ease-out infinite}
.emo[data-state="celebrating"] canvas{filter:drop-shadow(0 0 18px var(--emo))}
.emo[data-state="celebrating"] .emo-symbol{animation:emo-spark 1s ease-in-out infinite}
@keyframes emo-breathe{50%{transform:scale(1.025);filter:drop-shadow(0 0 16px color-mix(in srgb,var(--emo) 65%,transparent))}}
@keyframes emo-dots{0%{clip-path:inset(0 100% 0 0)}100%{clip-path:inset(0 0 0 0)}}
@keyframes emo-tremble{0%,86%,100%{transform:translateX(0)}88%{transform:translateX(-2px)}90%{transform:translateX(2px)}92%{transform:translateX(-2px)}94%{transform:translateX(1px)}}
@keyframes emo-drop{0%{transform:translateY(0);opacity:0}15%{opacity:.85}100%{transform:translateY(14px);opacity:0}}
@keyframes emo-hop{0%,100%{transform:translateY(0)}35%{transform:translateY(-10px)}}
@keyframes emo-spark{50%{transform:scale(1.35) rotate(20deg)}}
@media (prefers-reduced-motion:reduce){.emo,.emo *,.emo::after{animation:none!important;transition:none!important}}
`;
