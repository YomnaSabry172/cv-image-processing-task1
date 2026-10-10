# CLAUDE.md — CV Task 1: Image Processing Web App

> This file is read by Claude Code at the start of every session.
> It is the single source of truth for structure, rules, contracts and ownership.
> **Deadline: 12 October.** Prefer simple, working, clean code over clever code.

---

## 1. Project overview

A web app for a university Computer Vision assignment (Task 1). The user uploads an image (RGB or grayscale) and applies classic image-processing operations, seeing results, parameters, charts and timings in a polished UI.

Features (numbers match the assignment):

| # | Feature | Implementation |
|---|---------|----------------|
| 1 | Additive noise: uniform, Gaussian, salt & pepper | Uniform + Gaussian: library (NumPy/OpenCV random). Salt & pepper: **from scratch** |
| 2 | Low-pass filters: average, Gaussian, median | **From scratch** (+ built-in twin, see §3.2) |
| 3 | Edge detection: Sobel, Prewitt, Roberts, Canny | Sobel/Prewitt/Roberts **from scratch** (+ built-in twin). Canny: `cv2.Canny` |
| 4 | Histogram + distribution curve (gray: 1 channel, RGB: 3 channels) | **From scratch** |
| 5 | Histogram equalization | **From scratch** |
| 6 | Normalization (min–max contrast stretch to 0–255) | **From scratch** |
| 7 | Color → grayscale | **From scratch** |
| 8 | R, G, B histograms + their CDF curves | **From scratch** (reuses #4) |
| 9 | Frequency-domain low-pass / high-pass filters | `np.fft` for FFT/IFFT only; masks **from scratch** |
| 10 | Hybrid images | **From scratch**, must reuse #9 (no duplicated filter code) |

A written report (observations on methods & parameter variations, plus UI features) is also required — see §11.

---

## 2. Team & ownership

Replace the names below with real names.

| Role | Owner | Owns |
|------|-------|------|
| Lead | `LEAD_NAME` | Repo, UI shell, design system, shared components, backend setup, utils, all placeholders, feature 7 (grayscale) as the reference example, final integration |
| B | `MEMBER_B` | `core/convolution.py`, `core/kernels.py`, `core/compare.py`, features 1 (noise) and 2 (filters) |
| C | `MEMBER_C` | Features 3 (edges), 9 (frequency filters), 10 (hybrid) |
| D | `MEMBER_D` | Features 4 & 8 (histograms/CDF), 5 (equalization), 6 (normalization) |

**Dependency:** C's edge detection needs B's convolution. B delivers `correlate2d_manual` first. Until then, C calls the built-in path.

**Ownership rule for Claude Code:** when working for a team member, only edit files they own (see the `# Owner:` header in each file) unless explicitly told otherwise. Shared files (router registration, sidebar, App routes) are fully pre-wired in Phase 0 so nobody needs to touch them later.

---

## 3. Non-negotiable rules

### 3.1 From scratch vs library

**Allowed everywhere:** NumPy array operations (indexing, slicing, broadcasting, `np.pad`, `np.cumsum`, `np.add.at`, `np.lib.stride_tricks.sliding_window_view`, `np.median`, math functions), `np.random.*`, `time.perf_counter`.

**Allowed library calls (only these uses):**
- `cv2.imdecode` / `cv2.imencode` — reading/encoding images
- `cv2.resize` — resizing (upload downscaling, hybrid size matching)
- `cv2.Canny` — Canny only
- `cv2.randn` / `cv2.randu` or `np.random.normal` / `np.random.uniform` — uniform & Gaussian noise
- `np.fft.fft2`, `np.fft.ifft2`, `np.fft.fftshift`, `np.fft.ifftshift` — FFT only
- `scipy.ndimage.correlate`, `scipy.ndimage.convolve`, `scipy.ndimage.median_filter` — **only inside the `builtin` branch** of the dual implementations (§3.2)

**Forbidden in from-scratch code:** `cv2.filter2D`, `cv2.blur`, `cv2.GaussianBlur`, `cv2.medianBlur`, `cv2.Sobel`, `cv2.Scharr`, `cv2.Laplacian`, `cv2.equalizeHist`, `cv2.calcHist`, `cv2.normalize`, `cv2.cvtColor` (for grayscale conversion), `np.histogram`, `np.bincount`, `skimage.*`.

### 3.2 Manual + built-in twins (TA requirement)

The TA requires convolution to be done **manually**, optimized, while also keeping a **built-in** version, and showing the difference in at least one place.

- Every convolution-based operation takes `implementation: "manual" | "builtin"`.
- The **default in the UI is `"builtin"`** (fast).
- The **Filters page** has a **Compare** mode that runs both and shows: both outputs, absolute difference image, time of each (ms), speed-up factor, and max absolute difference (should be ≈ 0).
- Manual and built-in must produce the same result: same kernel, same correlation/convolution choice, same border mode (§3.4).

### 3.3 Manual convolution must be vectorized

Never loop over pixels in Python. Loop over **kernel positions** instead (9 iterations for 3×3):

```python
# correlation: out[i,j] = sum_{a,b} k[a,b] * padded[i+a, j+b]
out = np.zeros((H, W), dtype=np.float64)
for a in range(kh):
    for b in range(kw):
        out += kernel[a, b] * padded[a:a+H, b:b+W]
```

Median (manual): `sliding_window_view(padded, (k, k))` then `np.median(..., axis=(-2, -1))`. Keep the input `uint8` to limit memory.

### 3.4 Correctness rules (common bugs)

1. **Dtype:** convert to `float64` before any arithmetic. At the end: `np.clip(x, 0, 255).astype(np.uint8)`. Never add/multiply on `uint8` (250 + 10 wraps to 4).
2. **Color order:** OpenCV decodes as **BGR**. Convert to **RGB exactly once**, in `utils/image_io.py` on decode, and back to BGR once on encode. Everything else in the codebase assumes RGB.
3. **Correlation vs convolution:** convolution = correlation with the kernel flipped 180°. Identical for symmetric kernels (box, Gaussian, Laplacian). For Sobel/Prewitt/Roberts it flips the sign of Gx/Gy (magnitude unaffected). This project uses **correlation** for all spatial filtering, and compares against `scipy.ndimage.correlate`.
4. **Border mode naming trap:** `np.pad(mode="symmetric")` ↔ `scipy.ndimage` `mode="reflect"`. (NumPy's `"reflect"` is SciPy's `"mirror"`.) Manual uses `np.pad(..., mode="symmetric")`; built-in uses `mode="reflect"`.
5. **Even kernels (Roberts 2×2):** anchor = `(kh // 2, kw // 2)`. Pad `top = kh // 2`, `bottom = kh - 1 - kh // 2`, same for left/right. This matches SciPy's default `origin=0`.
6. **Sobel Y kernel:** the correct kernel is `[[-1,-2,-1],[0,0,0],[1,2,1]]`. (The tutorial slide has a typo with `+1` in the top-right.)
7. **Signed outputs for display:** Gx, Gy, Laplacian and high-pass results contain negative values. For display, use `to_display()` (§5.1). Never clip negatives to 0 before computing magnitude or before summing in the hybrid.
8. **Color images:** operations defined on one channel are applied per channel via `apply_per_channel()` (§5.1). Edge detection, and Canny, run on the grayscale version.

### 3.5 Code quality

- No duplicated logic. Sobel/Prewitt/Roberts share one `EdgeDetector` class. Hybrid reuses `FrequencyFilter`. Equalization reuses `cdf()`. Display normalization reuses `normalize_minmax()`.
- **Math lives in `core/`. Routes only:** decode input → call core → encode output.
- Python: type hints, short docstrings, and comments on every from-scratch algorithm explaining **why** each step exists (team members must explain this code to TAs).
- Do not add dependencies without asking.

---

## 4. Tech stack

**Backend:** Python 3.11+, FastAPI, Uvicorn, NumPy (≥1.24), SciPy, `opencv-python-headless`, Pydantic v2.

**Frontend:** React 18 + Vite 8 (JavaScript, JSX), Tailwind CSS v4 (via `@tailwindcss/vite` — no `tailwind.config.js` / `postcss.config.js`; theme lives in `src/index.css`), React Router 6, Recharts (charts), lucide-react (icons).

**Dev:** backend on `http://localhost:8000`, frontend on `http://localhost:5173` (`strictPort`, because CORS only allows this origin). The frontend reads the API base URL from `VITE_API_URL` (default `http://localhost:8000`). Backend dependencies live in a virtual environment at `backend/.venv` (not committed).

---

## 5. Repository structure

```
cv-task1/
├── CLAUDE.md
├── README.md                     # setup + run instructions + team table
├── .gitignore                    # Python, Node, .env, __pycache__, node_modules, dist
├── backend/
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py               # FastAPI app, CORS, includes all routers (pre-wired)  [Lead]
│   │   ├── schemas.py            # shared request/response models                       [Lead]
│   │   ├── api/
│   │   │   ├── __init__.py       # registers every router (pre-wired)                   [Lead]
│   │   │   ├── health.py         # GET /api/health                                      [Lead]
│   │   │   ├── grayscale.py      # POST /api/grayscale                                  [Lead]
│   │   │   ├── noise.py          # POST /api/noise                                      [B]
│   │   │   ├── filters.py        # POST /api/filter                                     [B]
│   │   │   ├── edges.py          # POST /api/edges                                      [C]
│   │   │   ├── frequency.py      # POST /api/frequency                                  [C]
│   │   │   ├── hybrid.py         # POST /api/hybrid                                     [C]
│   │   │   ├── histogram.py      # POST /api/histogram                                  [D]
│   │   │   ├── equalize.py       # POST /api/equalize                                   [D]
│   │   │   └── normalize.py      # POST /api/normalize                                  [D]
│   │   ├── core/
│   │   │   ├── color.py          # to_grayscale, split_channels, is_color               [Lead]
│   │   │   ├── convolution.py    # pad, correlate2d (manual/builtin), apply_kernel      [B]
│   │   │   ├── kernels.py        # box, gaussian, sobel, prewitt, roberts, laplacian    [B]
│   │   │   ├── compare.py        # run_both(): timing + difference                      [B]
│   │   │   ├── noise.py          # Noise classes                                        [B]
│   │   │   ├── spatial.py        # smooth(): average / gaussian / median                [B]
│   │   │   ├── edges.py          # EdgeDetector, canny                                  [C]
│   │   │   ├── frequency.py      # FrequencyFilter                                      [C]
│   │   │   ├── hybrid.py         # HybridImage                                          [C]
│   │   │   └── histogram.py      # histogram, pdf, cdf, equalize, normalize_minmax      [D]
│   │   └── utils/
│   │       ├── image_io.py       # base64 <-> numpy, BGR<->RGB, downscale               [Lead]
│   │       └── channels.py       # apply_per_channel, to_display                        [Lead]
│   └── tests/
│       └── test_convolution.py   # manual vs builtin equality tests                     [B]
├── frontend/
│   ├── package.json, vite.config.js, index.html, public/favicon.svg
│   └── src/
│       ├── main.jsx, App.jsx, index.css                                                  [Lead]
│       ├── api/client.js         # postJSON(path, body), ApiError (has .status)         [Lead]
│       ├── context/ImageContext.jsx                                                      [Lead]
│       ├── hooks/
│       │   ├── useProcess.js     # loading/error/debounce/abort for API calls           [Lead]
│       │   ├── useAutoRun.js     # re-sends a request whenever its body changes         [Lead]
│       │   └── useTheme.js       # dark/light toggle                                    [Lead]
│       ├── lib/
│       │   ├── image.js          # file → data URL (downscale to 1024), color detection [Lead]
│       │   └── nav.js            # sidebar groups, routes and Home cards in one list    [Lead]
│       ├── components/
│       │   ├── layout/           # AppLayout, Sidebar, TopBar, ApiStatus, PageShell,    [Lead]
│       │   │                     # ResultArea (501 / error / loading / results states)
│       │   └── ui/               # see §8.3                                             [Lead]
│       └── pages/
│           ├── Home.jsx          # upload + overview                                    [Lead]
│           ├── Grayscale.jsx                                                             [Lead]
│           ├── Noise.jsx, Filters.jsx                                                    [B]
│           ├── Edges.jsx, Frequency.jsx, Hybrid.jsx                                      [C]
│           └── Histogram.jsx, Equalize.jsx, Normalize.jsx                                [D]
└── docs/
    ├── report/                   # one .md section per member + screenshots/
    └── sample_images/            # a few test images (dark, noisy, colorful, portraits for hybrid)
```

Every source file starts with a header comment: `# Owner: <role> — <short purpose>` (or `// Owner:` in JS).

### 5.1 Shared utilities (Lead)

`utils/image_io.py`
- `decode_image(data_url: str) -> np.ndarray` — base64/data URL → `uint8` array, **RGB** (H×W×3) or gray (H×W). Downscales so the longest side is ≤ 1024 px (`cv2.resize`, `INTER_AREA`). If all three channels are equal, returns 2-D gray.
- `encode_image(img: np.ndarray) -> str` — array → `"data:image/png;base64,..."`. Accepts gray or RGB `uint8`; converts RGB→BGR before `cv2.imencode`.

`utils/channels.py`
- `apply_per_channel(fn, img, *args, **kwargs)` — calls `fn` on each channel of a color image and stacks the results; calls it once for gray.
- `to_display(arr, mode="minmax" | "abs" | "offset") -> uint8` — makes signed/float results viewable. `minmax` uses `core.histogram.normalize_minmax`. `abs` takes `|x|` then min-max. `offset` adds 128 then clips (for high-pass previews).

---

## 6. Core module specifications

Images inside `core/` are NumPy arrays. Input: `uint8`. Internal math: `float64`. Outputs say explicitly whether they are `uint8` (display-ready) or `float64` (raw, possibly signed).

### 6.1 `core/color.py` (Lead)
- `to_grayscale(img) -> uint8` — `0.299 R + 0.587 G + 0.114 B` on RGB input; returns input unchanged if already 2-D.
- `split_channels(img) -> dict[str, np.ndarray]` — `{"r","g","b"}` for color, `{"gray"}` for gray.
- `is_color(img) -> bool`

### 6.2 `core/kernels.py` (B)
- `box(k) -> np.ndarray` — `ones((k,k)) / k²`; `k` odd.
- `gaussian(k, sigma) -> np.ndarray` — sampled `exp(-(x²+y²)/(2σ²))` on a centered grid, normalized to sum 1.
- `sobel() -> (kx, ky)`: `kx=[[-1,0,1],[-2,0,2],[-1,0,1]]`, `ky=[[-1,-2,-1],[0,0,0],[1,2,1]]`
- `prewitt() -> (kx, ky)`: `kx=[[-1,0,1]]*3`, `ky=[[-1,-1,-1],[0,0,0],[1,1,1]]`
- `roberts() -> (kx, ky)`: `kx=[[1,0],[0,-1]]`, `ky=[[0,1],[-1,0]]`
- `laplacian() -> np.ndarray`: `[[0,1,0],[1,-4,1],[0,1,0]]`

### 6.3 `core/convolution.py` (B)
- `pad(img, kh, kw) -> np.ndarray` — asymmetric-safe padding per §3.4 rule 5, `np.pad(mode="symmetric")`.
- `correlate2d_manual(img2d, kernel) -> float64` — vectorized loop over kernel positions (§3.3).
- `correlate2d_builtin(img2d, kernel) -> float64` — `scipy.ndimage.correlate(img.astype(float64), kernel, mode="reflect")`.
- `apply_kernel(img, kernel, implementation="builtin") -> float64` — dispatches manual/builtin; handles color via `apply_per_channel`. Output same H×W as input.

### 6.4 `core/compare.py` (B)
- `run_both(manual_fn, builtin_fn, *args, **kwargs) -> dict` — runs each, timing with `time.perf_counter`. Returns `{"manual", "builtin", "difference" (abs diff), "time_manual_ms", "time_builtin_ms", "speedup", "max_abs_diff"}`. Generic, so any feature can reuse it.

### 6.5 `core/noise.py` (B)
- Abstract `Noise` with `apply(img) -> uint8` (template method: float → `_generate`/`_corrupt` → clip → uint8).
- `UniformNoise(low, high)` — library random; additive.
- `GaussianNoise(mean, sigma)` — library random; additive.
- `SaltPepperNoise(density, salt_ratio)` — **from scratch**. `density ∈ [0,1]` = fraction of corrupted pixels; `salt_ratio ∈ [0,1]` = share of those set to 255 (rest set to 0). Use one random mask per pixel position; for color, the same position is corrupted in all channels.
- Optional `seed: int | None` on all, for reproducible results.
- Factory `make_noise(type, **params) -> Noise`.

### 6.6 `core/spatial.py` (B)
- `smooth(img, method: "average"|"gaussian"|"median", k=3, sigma=1.0, implementation="builtin") -> uint8`
  - average → `apply_kernel(img, box(k))`
  - gaussian → `apply_kernel(img, gaussian(k, sigma))`
  - median → manual: `sliding_window_view` + `np.median`; builtin: `scipy.ndimage.median_filter(size=k, mode="reflect")`
- One function for all low-pass filters (assignment asks to group them).

### 6.7 `core/edges.py` (C)
- `class EdgeDetector(name, kx, ky)` with `detect(img, implementation="builtin") -> dict` returning `{"gx", "gy", "magnitude", "direction"}` (float64). Converts to gray first. `magnitude = sqrt(gx²+gy²)`, `direction = arctan2(gy, gx)` (radians).
- Registry: `DETECTORS = {"sobel": EdgeDetector("sobel", *sobel()), "prewitt": ..., "roberts": ...}`.
- `canny(img, low, high, blur_sigma=None) -> uint8` — optional pre-blur via `smooth(..., "gaussian")`, then `cv2.Canny` on gray `uint8`.

### 6.8 `core/histogram.py` (D)
- `histogram(channel, levels=256) -> np.ndarray[int]` — counts via `np.add.at` (or loop over levels with `(channel == v).sum()`). No `np.histogram`/`np.bincount`.
- `pdf(hist) -> float64` — `hist / hist.sum()`.
- `cdf(pdf) -> float64` — cumulative sum, ends at 1.0.
- `equalize(img) -> uint8` — per channel: `lut = round(cdf * (L-1))`, output `lut[channel]`. For color: per-channel equalization (note the color shift in the report).
- `normalize_minmax(arr, out_min=0, out_max=255) -> uint8` — `(x - min) / (max - min) * (out_max - out_min) + out_min`; if `max == min`, return a constant image (avoid division by zero). Works on float/signed input.
- `channel_stats(img) -> dict` — for each channel (`gray` or `r,g,b`): `{"hist": [...256], "pdf": [...], "cdf": [...], "min", "max", "mean", "std"}`.

### 6.9 `core/frequency.py` (C)
- `class FrequencyFilter(kind: "lowpass"|"highpass", shape: "ideal"|"gaussian"|"butterworth", cutoff: float, order: int = 2)`
  - `build_mask(h, w) -> float64` — **from scratch**. `D(u,v)` = distance from spectrum center. Ideal LP: `D ≤ D0`. Gaussian LP: `exp(-D²/(2 D0²))`. Butterworth LP: `1 / (1 + (D/D0)^(2n))`. HP = `1 − LP`.
  - `apply_raw(img2d) -> dict` — `F = fftshift(fft2(img))`, `G = F * H`, `g = real(ifft2(ifftshift(G)))`. Returns `{"result" (float64, unclipped), "spectrum" (log(1+|F|)), "mask", "filtered_spectrum" (log(1+|G|))}`.
  - `apply(img) -> dict` — color via per channel; returns display-ready `uint8` versions (high-pass via `to_display(mode="offset")` or `"minmax"`; spectra via min-max).

### 6.10 `core/hybrid.py` (C)
- `class HybridImage(low_filter: FrequencyFilter, high_filter: FrequencyFilter)`
  - `make(img_a, img_b) -> dict` — resize B to A's size (`cv2.resize`), match color mode (both gray if either is gray), `low = low_filter.apply_raw(A)`, `high = high_filter.apply_raw(B)`, `hybrid = clip(low + high)`. Returns `{"hybrid", "low_component", "high_component"}` as display-ready `uint8`.
  - Must not contain any mask/FFT code of its own.

---

## 7. API contract

All endpoints are `POST` with JSON bodies, prefixed `/api`. Images travel as data-URL strings (`"data:image/png;base64,..."`).

**Unified response envelope:**
```json
{
  "images": { "<name>": "data:image/png;base64,..." },
  "data":   { },
  "meta":   { "time_ms": 12.3 }
}
```

**Errors:** `400` for invalid params (with a readable `detail`). **Placeholders** raise `NotImplementedError` in core; the route converts this to `501` with `detail: "Not implemented yet (owner: <role>)"`.

| Endpoint | Request body | `images` | `data` |
|---|---|---|---|
| `GET /api/health` | — | — | `{status: "ok"}` |
| `/api/grayscale` | `{image}` | `result` | — |
| `/api/noise` | `{image, type: "uniform"\|"gaussian"\|"salt_pepper", low?, high?, mean?, sigma?, density?, salt_ratio?, seed?}` | `result` | — |
| `/api/filter` | `{image, method: "average"\|"gaussian"\|"median", kernel_size, sigma?, implementation: "manual"\|"builtin"\|"compare"}` | `result` or (compare) `manual`, `builtin`, `difference` | compare: `{time_manual_ms, time_builtin_ms, speedup, max_abs_diff}` |
| `/api/edges` | `{image, method: "sobel"\|"prewitt"\|"roberts"\|"canny", implementation?, low?, high?, blur_sigma?}` | sobel/prewitt/roberts: `gx`, `gy`, `magnitude`, `direction`; canny: `result` | — |
| `/api/histogram` | `{image}` | — | `{mode: "gray"\|"rgb", channels: {<name>: {hist, pdf, cdf, min, max, mean, std}}}` |
| `/api/equalize` | `{image}` | `result` | `{before: channel_stats, after: channel_stats}` |
| `/api/normalize` | `{image}` | `result` | `{before: channel_stats, after: channel_stats}` |
| `/api/frequency` | `{image, kind, shape, cutoff, order?}` | `result`, `spectrum`, `mask`, `filtered_spectrum` | — |
| `/api/hybrid` | `{image_a, image_b, low_cutoff, high_cutoff, shape}` | `hybrid`, `low_component`, `high_component` | — |

Every response includes `meta.time_ms` (total processing time).

---

## 8. Frontend specification

### 8.1 Global image state — `ImageContext`
- `original` — the uploaded image (data URL) + `name`, `width`, `height`, `isColor`.
- `working` — the current input for all pages (starts equal to `original`).
- `setWorking(dataUrl)`, `resetWorking()`, `upload(file)`.
- Every result panel has a **"Use as input"** button → `setWorking(result)`. This allows the pipeline *noise → filter*, which is what the assignment asks for ("filter the noisy image").
- The Hybrid page has its own two upload slots (A and B), defaulting A to `working`.

### 8.2 `useProcess(path)` hook
- Returns `{run(body), data, loading, error}`.
- Debounces slider-driven calls (300 ms), aborts stale requests (`AbortController`), and maps `501` to a friendly "Not implemented yet" state.

### 8.3 Shared UI components (`components/ui/`)
`ImageDropzone`, `ImagePanel` (title, image, download button, "Use as input", click-to-enlarge modal), `ImageGrid`, `BeforeAfterSlider`, `ParamSlider` (label, value, min/max/step, unit), `SegmentedControl`, `Select`, `Toggle`, `Button`, `Card`, `LoadingOverlay`, `ErrorBanner`, `NotImplementedCard`, `TimingBadge`, `ImplementationToggle` (Built-in / Manual / Compare), `HistogramChart` (Recharts bars for one channel's histogram + CDF line on a secondary 0–1 axis, in the channel's color), `ChannelHistograms` (one `HistogramChart` per channel: 1 for gray, 3 for RGB), `BeforeAfterHistograms` (Equalize/Normalize layout), `EmptyState` (prompts upload when no image).

### 8.3.1 How a page talks to the backend (pattern every page follows — see `pages/Grayscale.jsx`)
```jsx
const process = useProcess('/grayscale')                       // one endpoint
useAutoRun(process.run, working ? { image: working } : null)   // body changes → request (debounced)
<ResultArea process={process}> ...process.data.images... </ResultArea>  // handles 501 / errors / loading
```

### 8.4 Navigation (sidebar, grouped)
- **Start:** Home (upload & overview)
- **Basics:** Grayscale
- **Noise & Smoothing:** Noise, Filters
- **Edges:** Edge Detection
- **Histograms:** Histogram & CDF, Equalization, Normalization
- **Frequency:** Frequency Filters, Hybrid Image

The sidebar also shows a small thumbnail of the **working image** with a "Reset to original" action. Every page works for both gray and RGB images.

### 8.5 Page layout pattern (all feature pages)
`PageShell` = title + one-line description → left/top **controls card** (parameters) → **results area** (`ImageGrid` of `ImagePanel`s, charts) → `TimingBadge`. If no image is uploaded, show `EmptyState`. If the endpoint returns 501, show `NotImplementedCard`.

Page-specific notes:
- **Filters:** `ImplementationToggle`; in Compare mode show manual, built-in, difference, and a stats row (times, speed-up, max diff).
- **Edges:** method selector (Sobel / Prewitt / Roberts / Canny). Non-Canny shows Gx, Gy, Magnitude, Direction. Canny shows low/high threshold sliders and the result.
- **Histogram:** chart(s) + stats table; gray → one chart, RGB → three (R, G, B), each with its CDF.
- **Equalize / Normalize:** before/after images + before/after histograms with CDFs.
- **Frequency:** kind, shape, cutoff, order (Butterworth only) controls; show spectrum, mask, filtered spectrum, result.
- **Hybrid:** two image slots, swap button, low/high cutoff sliders; show low component, high component, hybrid; plus a "view small" toggle that renders the hybrid at reduced size (so the low-frequency image is perceived).

### 8.6 Design direction
- Clean, modern "lab tool" look. Dark-first with a light-mode toggle (Tailwind `dark` class), neutral zinc palette, **one** accent color (indigo), consistent channel colors (R `#ef4444`, G `#22c55e`, B `#3b82f6`, Gray `#a1a1aa`).
- Font: Inter (Google Fonts) with system fallback. Rounded-xl cards, subtle borders, generous spacing, no heavy gradients.
- Images displayed on a neutral dark surface, `object-contain`, never stretched.
- Responsive: sidebar collapses to a top menu on narrow screens.
- Smooth but minimal transitions; clear loading states; every control labeled with units.

---

## 9. Coding conventions
- Python: snake_case, type hints, docstrings, `black`-style formatting.
- JS: camelCase components in PascalCase files, functional components + hooks, Tailwind classes only (no separate CSS beyond `index.css`).
- Route files define their own Pydantic request model (keeps team members out of each other's files).
- Keep functions small; no function longer than ~50 lines without reason.

---

## 10. Git workflow
- `main` is always runnable.
- Branches: `feature/noise-filters` (B), `feature/edges-frequency-hybrid` (C), `feature/histograms` (D), `feature/ui` (Lead).
- Merge via pull requests; at least a quick review by one other member.
- Only edit files you own; if a shared file must change, tell the Lead.

---

## 11. Report (`docs/report/`)
Each member writes `report_<role>.md` with: what was implemented, the algorithm in short, screenshots, and **observations on parameter variations** (e.g. kernel size vs blur; Gaussian vs average vs median on salt & pepper; ideal vs Gaussian mask ringing; equalization vs normalization; manual vs built-in timing). The Lead merges them and adds a UI features section.

---

## 12. Phase 0 — scaffold task (Lead, run first)

**Status: done (10 October).** Notes on what was decided while doing it:
- **Routes are already complete** for every feature (request model, decode → call core → encode, response keys per §7). They are thin glue and they lock the contract the frontend depends on. Members implement the **core** functions; they only need to touch a route if they change its behavior.
- Placeholders raise `NotImplementedError("TODO (<role>): <what>")`. A global handler in `main.py` turns this into `501` with `detail: "Not implemented yet (owner: <role>): <what>"`, and the page shows `NotImplementedCard`.
- `core.edges.DETECTORS` starts empty (filling it needs B's kernels). `/api/edges` returns 501 until C registers the detectors.
- `utils.channels.to_display` uses D's `normalize_minmax`, so edge and frequency images also need D's function before they display.
- Route handlers are plain `def` (not `async def`) so FastAPI runs the NumPy work in its thread pool instead of blocking the server.
- `tests/test_convolution.py` is skipped with `pytestmark`; B deletes that line when convolution works.

When asked to "run Phase 0", do the following:

1. Create the full structure in §5, including **every file** with its owner header.
2. **Backend:** working FastAPI app, CORS, all routers registered, `/api/health`, `utils/image_io.py` and `utils/channels.py` fully implemented, `core/color.py` fully implemented, `/api/grayscale` fully working end-to-end.
3. **Placeholders:** every other core function exists with its final signature and docstring, and raises `NotImplementedError("TODO (<role>): <what to implement>")`. Every route exists, validates its request model, and returns `501` via the shared placeholder handling.
4. **Frontend:** Vite + React + Tailwind + Router + Recharts + lucide-react set up; full layout, sidebar navigation, theme toggle, `ImageContext`, `useProcess`, `api/client.js`, and all components in §8.3 implemented.
5. **Pages:** Home and Grayscale fully working. Every other page fully built with its real controls (§8.5) wired to its endpoint, showing `NotImplementedCard` until the backend is filled in.
6. `backend/tests/test_convolution.py` with tests (initially skipped) asserting manual ≈ builtin for box, Gaussian, Sobel and Roberts kernels.
7. `README.md`: prerequisites, setup and run commands for backend and frontend, team/ownership table, link to this file.
8. `.gitignore`, `requirements.txt`, `docs/report/` with one template per role, `docs/sample_images/` (empty, with a README listing which kinds of images to add).

**Acceptance check:** `uvicorn app.main:app --reload` runs from `backend/`, `npm run dev` runs from `frontend/`, every page is reachable, uploading an image and opening Grayscale shows the converted result, and other pages show their controls plus the "Not implemented yet" state.
