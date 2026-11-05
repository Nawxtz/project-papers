# Code-task test: do the papers help an agent change code?

The rest of `bench/` measures whether the skill finds relevant papers. This test asks a different question. When an agent is about to change a file, does getting the papers linked to that file (what `lookup` and the hook print) make the change better?

## Setup

- **Project.** A single-file hand-tracking drawing app (`index.html`, about 1800 lines, MediaPipe Hands). It was chosen because it is small and has two pieces of hand-written signal code with measurable behaviour.
- **Tasks.**
  - `task_smooth.md`: replace the fixed 0.5/0.5 fingertip smoothing, which shakes when the finger is slow and trails when it is fast.
  - `task_pinch.md`: replace the pinch detector, which fires when the thumb only comes near a finger and sometimes fires twice.
  Each task asks for a standalone CommonJS module, so the result can be scored without a camera.
- **Arms.** Every run got the task and a copy of `index.html`.
  - `np`: no papers.
  - `p0`: the `lookup` output from the skill before the fixes in this round (`papers_context_before.txt`). Its smoothing papers were about air writing and never mention smoothing.
  - `p1`: the `lookup` output after the fixes (`papers_context_after.txt`). It includes the 1€ filter paper (Casiez et al., CHI 2012).
- **Agents.** Claude Sonnet and Claude Haiku subagents, with web search and web fetch off. Smoothing ran twice per model for `np` and `p1` (the `_b` rows), so there are 16 runs in all.
- **Scoring.** The agents never saw the scorers.
  - `eval_smooth.js` replays 30 synthetic fingertip traces at about 30 fps with uneven frame times, dropped frames, Gaussian jitter and rare spikes. It reports the RMSE against the true path while the finger is still, slow and fast, plus the frame-to-frame movement while still (jitter).
  - `eval_pinch.js` replays 40 synthetic distance traces with deliberate pinches, quick taps, near misses, noise and one-frame glitches. It counts missed pinches, near misses that fired, double fires, and the latency from contact to firing.

## Rerun

```
node eval_smooth.js                     # baselines: raw input and the app's 0.5 EMA
node eval_smooth.js path/to/smoother.js
node eval_pinch.js                      # baseline: the app's updatePinch()
node eval_pinch.js path/to/pinch.js
```

To repeat the experiment, give an agent `task_smooth.md` or `task_pinch.md` and a copy of the app, with or without one of the `papers_context_*.txt` files, then score its module.

## Results (`results.txt`)

`raw`, `ema0.5` and `baseline` are the original behaviour. Every other row is one agent run, named `<arm>_<task>_<model>`.

Smoothing, mean over runs (lower is better):

| Arm | Runs | Fast RMSE (px) | Still jitter (px/frame) |
|---|---|---|---|
| Original 0.5 EMA | - | 32.8 | 1.92 |
| `np` | 4 | 11.2 | 0.98 |
| `p0` | 2 | 9.9 | 1.09 |
| `p1` | 4 | 12.8 | 0.78 |

Pinch, all runs in each arm combined:

| Arm | Runs | False fires | Double fires | Missed |
|---|---|---|---|---|
| Original | - | 133 | 11 | 3 |
| `np` | 2 | 1 | 0 | 1 |
| `p0` | 2 | 1 | 1 | 0 |
| `p1` | 2 | 0 | 1 | 0 |

## What it shows

- **Every run beat the original code by a wide margin.**
- **The papers did not measurably change the result.** All 10 smoothing runs chose a One Euro filter, with or without the paper. The spread between runs comes from parameter choices and is larger than any gap between arms. With 2-4 runs per cell this test can only rule out a large effect, not a small one.
- **What the papers did change.**
  - With `p1`, all 4 smoothing runs named the 1€ paper as the origin of their method.
  - With `p0`, 2 of the 4 runs (both Sonnet) said the papers did not help, and one Haiku run cited the 1€ paper from memory, unchecked.
  - The value shown here is a correct, checked citation for the method the code uses, not better code.
- **A risk.** One `p1` run stated a tuning procedure "from the paper" that is not in the abstract it was given. `lookup` and the hook now say that only the quoted sentence is checked.
- **Limits.**
  - The tasks use well-known techniques that the models already knew.
  - Papers may matter more for niche methods.
  - The traces are synthetic, not real camera data.
