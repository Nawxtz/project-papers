Task (air-canvas, index.html): users say strokes look shaky when they draw slowly or hold the finger still, and on fast strokes the line trails behind the finger. The fingertip smoothing is the inline code in the `fingerCount === 1` branch (lastSmoothedPoint, around index.html:1611).

Write a better fingertip smoother as a standalone CommonJS file `smoother.js` in your work folder:

  exports.createSmoother = () => ({ update(x, y, tMs) { return {x, y}; }, reset() {} })

- `update` is called once per camera frame with the raw fingertip in canvas pixels (canvas about 1280x720, landmarks jitter by a few pixels) and the frame timestamp in ms (about 30 fps, frame times are uneven and frames are sometimes dropped). It returns the smoothed point. `reset` is called when the pen lifts.
- Plain JS, no dependencies. Do not edit index.html.
- You may write and run your own quick tests with node.
- Finish with 3-5 lines: what method you used, why, and the parameter values.
