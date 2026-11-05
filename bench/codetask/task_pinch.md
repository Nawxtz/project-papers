Task (air-canvas, index.html): users say the color sometimes changes by itself when the thumb only comes near a finger, and a pinch occasionally fires twice. Pinch detection is `updatePinch()` and PINCH_CONFIG (around index.html:931 and 1315).

Write a better pinch detector as a standalone CommonJS file `pinch.js` in your work folder:

  exports.createPinchDetector = () => ({ update(dist, tMs) { return false; }, reset() {} })

- `update` is called once per camera frame with `dist` = thumb-tip to finger-tip distance divided by hand scale (as in index.html; a real pinch goes to about 0.05-0.1, an open hand is about 0.6, landmarks are noisy and sometimes glitch for one frame) and the frame timestamp in ms (about 30 fps, uneven). It returns true on exactly the one frame when the action should fire for a deliberate pinch, otherwise false. Quick deliberate pinches (about 0.2 s) should still fire.
- Plain JS, no dependencies. Do not edit index.html.
- You may write and run your own quick tests with node.
- Finish with 3-5 lines: what method you used, why, and the parameter values.
