# Report — Lead: UI, shared utilities & grayscale

**Name:** Yomna Sabry

## What I implemented
- Grayscale conversion (feature 7)
- Shared utilities: image I/O, per-channel helper, display helper
- The web app: layout, navigation, shared components, every page

## Grayscale algorithm
_Y = 0.299 R + 0.587 G + 0.114 B, and why these weights._

## UI features
- One upload shared by every page; "Use as input" chains operations (e.g. noise → filter); "Reset to original"
- Live results while moving sliders (debounced requests, stale requests cancelled)
- Before/after slider, click-to-enlarge, download PNG on every result
- Manual vs built-in compare mode with timing, speed-up and difference image
- Histogram + CDF charts per channel
- Dark/light theme, works on phones, backend online indicator, processing time on every page

## Final report
_Merge report_B.md, report_C.md and report_D.md here at the end._
