// Scores a fingertip smoother on synthetic MediaPipe-like traces.
// Usage: node eval_smooth.js <smoother.js> ; module exports createSmoother()
// -> {update(x, y, tMs) -> {x, y}, reset()}
const path = require('path');
function rng(seed) { let s = seed >>> 0; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }
function gauss(r) { const u = Math.max(r(), 1e-12), v = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }

// Each trace: list of {t, x, y, kind} truth samples at real frame times.
function makeTrace(seed) {
  const r = rng(seed), out = [];
  let t = 0;
  const frame = () => { t += 33.3 + (r() - 0.5) * 10; if (r() < 0.03) t += 33.3; return t; };
  const push = (x, y, kind) => out.push({ t, x, y, kind });
  // 1) hold still 1 s
  for (let i = 0; i < 30; i++) { frame(); push(640, 360, 'still'); }
  // 2) slow circle, ~110 px/s
  let a = 0; const t0 = t;
  while (t - t0 < 3000) { frame(); a = (t - t0) / 1000 * 0.3 * 2 * Math.PI; push(640 + 60 * Math.sin(a), 360 - 60 + 60 * Math.cos(a), 'slow'); }
  // 3) fast straight sweeps, 1500 px/s, back and forth
  let x = 640; let dir = 1; const t1 = t; let prev = t;
  while (t - t1 < 2500) { frame(); x += dir * 1.5 * (t - prev); prev = t; if (x > 1100 || x < 180) dir = -dir; push(x, 300, 'fast'); }
  // 4) handwriting-like curve, speed 50..1200 px/s
  const t2 = t; let px = 400, py = 400, ang = 0; prev = t;
  while (t - t2 < 4000) { frame(); const dt = (t - prev) / 1000; prev = t; const u = (t - t2) / 4000;
    const sp = 50 + 1150 * Math.abs(Math.sin(u * Math.PI * 3)); ang += dt * 4 * Math.sin(u * 17);
    px += Math.cos(ang) * sp * dt; py += Math.sin(ang) * sp * dt; px = Math.min(1200, Math.max(80, px)); py = Math.min(680, Math.max(40, py));
    push(px, py, sp < 300 ? 'slow' : 'fast'); }
  // 5) hold still again 1 s
  const lx = px, ly = py; for (let i = 0; i < 30; i++) { frame(); push(lx, ly, 'still'); }
  return out.map(p => {
    const spike = r() < 0.01; const s = 2.5;
    return { ...p, ox: p.x + gauss(r) * s + (spike ? (r() - 0.5) * 30 : 0), oy: p.y + gauss(r) * s + (spike ? (r() - 0.5) * 30 : 0) };
  });
}

function score(create) {
  const acc = { still: [0, 0], slow: [0, 0], fast: [0, 0] };
  let jit = 0, jn = 0;
  for (let seed = 1; seed <= 30; seed++) {
    const sm = create(); if (sm.reset) sm.reset();
    const tr = makeTrace(seed); let last = null;
    for (const p of tr) {
      const o = sm.update(p.ox, p.oy, p.t);
      if (!o || !isFinite(o.x) || !isFinite(o.y)) throw new Error('bad output at t=' + p.t);
      const e2 = (o.x - p.x) ** 2 + (o.y - p.y) ** 2; acc[p.kind][0] += e2; acc[p.kind][1]++;
      if (p.kind === 'still' && last) { jit += Math.hypot(o.x - last.x, o.y - last.y); jn++; }
      last = o;
    }
  }
  const rm = k => Math.sqrt(acc[k][0] / acc[k][1]);
  return { still_rmse: rm('still'), slow_rmse: rm('slow'), fast_rmse: rm('fast'), still_jitter_px_per_frame: jit / jn };
}

const raw = () => ({ update: (x, y) => ({ x, y }), reset() {} });
const ema = () => { let p = null; return { update(x, y) { if (!p) p = { x, y }; else { p = { x: p.x * 0.5 + x * 0.5, y: p.y * 0.5 + y * 0.5 }; } return p; }, reset() { p = null; } }; };
const fmt = o => Object.entries(o).map(([k, v]) => k + '=' + v.toFixed(2)).join(' ');
if (process.argv[2]) { const m = require(path.resolve(process.argv[2])); console.log(fmt(score(m.createSmoother))); }
else { console.log('raw      ' + fmt(score(raw))); console.log('ema0.5   ' + fmt(score(ema))); }
