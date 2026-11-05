// Scores a pinch detector on synthetic thumb-fingertip distance traces.
// Usage: node eval_pinch.js <pinch.js> ; module exports createPinchDetector()
// -> {update(dist, tMs) -> true on the frame the action should fire, reset()}
// dist = thumb-tip to finger-tip distance divided by hand scale (as in index.html).
const path = require('path');
function rng(seed) { let s = seed >>> 0; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }
function gauss(r) { const u = Math.max(r(), 1e-12), v = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }

// Events: 'pinch' (deliberate, should fire once), 'near' (finger curls close, must not fire),
// 'tap' (quick deliberate pinch ~180 ms, should fire once).
function makeTrace(seed) {
  const r = rng(seed), frames = [], events = [];
  let t = 0;
  const frame = () => { t += 33.3 + (r() - 0.5) * 10; if (r() < 0.03) t += 33.3; return t; };
  const segment = (from, to, ms, kind, id) => { const t0 = t; while (t - t0 < ms) { frame(); const u = Math.min(1, (t - t0) / ms); frames.push({ t, d: from + (to - from) * u, ev: id }); } };
  const hold = (d, ms, id) => segment(d, d, ms, null, id);
  for (let k = 0; k < 24; k++) {
    hold(0.6 + r() * 0.2, 400 + r() * 600, -1);
    const kinds = ['pinch', 'pinch', 'near', 'tap'];
    const kind = kinds[Math.floor(r() * kinds.length)];
    const id = events.length; events.push({ kind, start: t, contact: null });
    if (kind === 'near') { const low = 0.21 + r() * 0.08; segment(0.6, low, 150, kind, id); hold(low, 300 + r() * 500, id); segment(low, 0.6, 150, kind, id); }
    else { const ms = kind === 'tap' ? 180 : 300 + r() * 600; segment(0.6, 0.07, 120, kind, id); events[id].contact = t; hold(0.07, ms, id); segment(0.07, 0.6, 120, kind, id); }
  }
  // noise: landmark jitter + occasional one-frame tracking glitch
  return { events, frames: frames.map(f => ({ ...f, obs: Math.max(0, f.d + gauss(r) * 0.03 + (r() < 0.02 ? (r() - 0.3) * 0.5 : 0)) })) };
}

function score(create) {
  let miss = 0, falsef = 0, dbl = 0, idle = 0, need = 0, lat = 0, latn = 0;
  for (let seed = 1; seed <= 40; seed++) {
    const det = create(); if (det.reset) det.reset();
    const { events, frames } = makeTrace(seed); const fires = events.map(() => 0);
    for (const f of frames) {
      if (det.update(f.obs, f.t) === true) {
        if (f.ev < 0) idle++; else { fires[f.ev]++; const e = events[f.ev]; if (fires[f.ev] === 1 && e.contact !== null) { lat += f.t - e.contact; latn++; } }
      }
    }
    events.forEach((e, i) => {
      if (e.kind === 'near') { if (fires[i] > 0) falsef++; }
      else { need++; if (fires[i] === 0) miss++; if (fires[i] > 1) dbl++; }
    });
  }
  return { missed: miss, false_fires: falsef, double_fires: dbl, idle_fires: idle, deliberate: need, latency_ms: latn ? lat / latn : NaN };
}

function baseline() { // logic copied from index.html updatePinch()
  const C = { baseThreshold: 0.20, holdDuration: 130, releaseThreshold: 0.35 };
  const st = { inPinch: false, fired: false, startTime: 0 };
  return { update(dist, now) {
    if (!st.inPinch) { if (dist < C.baseThreshold) { st.inPinch = true; st.fired = false; st.startTime = now; } }
    else if (dist > C.releaseThreshold) { st.inPinch = false; st.fired = false; }
    else if (now - st.startTime >= C.holdDuration && !st.fired) { st.fired = true; return true; }
    return false; }, reset() { st.inPinch = false; } };
}
const fmt = o => Object.entries(o).map(([k, v]) => k + '=' + (Number.isInteger(v) ? v : v.toFixed(1))).join(' ');
if (process.argv[2]) console.log(fmt(score(require(path.resolve(process.argv[2])).createPinchDetector)));
else console.log('baseline ' + fmt(score(baseline)));
