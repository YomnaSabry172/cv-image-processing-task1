# CV Task 1 — full-project test plan



## 1. What has actually been checked

| Run | Result |
|---|---|
| Existing repository tests | 33 passed |
| Existing tests + this kit's numerical/API tests | 220 passed, 10 failed (230 total) |
| Numerical examples/properties in this kit | All passed in this run |
| Valid API method/mode matrix on grayscale and RGB | Passed for the included cases |
| Browser interaction, rendering, accessibility, frontend build | Not executed here; follow the checklist below |

The automated run uses the backend in-process with FastAPI TestClient; it does not prove that your live Vite server, CORS/browser setup, or images render correctly on Windows. The uploaded source and your current local checkout must match for the results to be comparable. Dependency versions are recorded in `environment.txt`; timing is environment-dependent. Results are a baseline, not a guarantee for every possible input. Expected validation failures remain real failed tests, not hidden with xfail or skips.

## 2. How to use this kit on your Windows project

1. Extract the ZIP so `CV_Test_Kit` sits beside `backend` and `frontend` inside your existing project. Do not replace application files.
2. Keep your normal backend and frontend terminals open. Use a third PowerShell terminal for tests.
3. From the project root, record the version being tested:

```powershell
git status
git log -1 --oneline
cd backend
.\.venv\Scripts\Activate.ps1
```

4. Run the existing tests first:

```powershell
python -m pytest -q tests
```

If Python says pytest is missing, the project requirements do not include the test runner. Test-only setup needs `pytest` and `httpx` in your existing virtual environment. Coordinate this with the lead under the project's dependency rule; no application requirements file has been changed by this kit. Once agreed:

```powershell
python -m pip install pytest httpx
```

5. Run the existing tests and the kit together:

```powershell
python -m pytest -q tests ..\CV_Test_Kit\qa_tests --tb=short
```

6. To capture evidence, rerun after changes using:

```powershell
python -m pytest tests ..\CV_Test_Kit\qa_tests --tb=short --junitxml=..\CV_Test_Kit\results.xml 2>&1 | Tee-Object -FilePath ..\CV_Test_Kit\windows_test_run.txt
```

A failed test means the expected behaviour was not met. Read its name and assertion; do not change the expected result just to get a green run. The initial kit has 10 known failing cases described below. Leave your saved local changes/stash untouched during testing unless you are intentionally testing a fix.

7. Check frontend compilation in its own terminal after stopping that terminal's development server if needed:

```powershell
cd D:\semester7\CV\task1\cv-image-processing-task1\frontend
npm run build
npm run dev
```

Build success is a separate check from browser behaviour. It does not replace the manual checklist. Do not run `npm audit fix --force` as part of testing.

## 3. Test images supplied

PNG fixtures are lossless so pixel-level expectations are exact. JPG/WebP are useful for format checks, not exact-value assertions. The generator is included for reproducibility.

| File in `images` | Purpose |
|---|---|
| `01_constant_128.png` | Constant image: noise, no edges, flat-image corner cases |
| `02_gray_ramp.png` | Each gray level 0–255 occurs exactly 256 times |
| `03_vertical_step.png`, `04_horizontal_step.png` | Known edge direction and frequency ringing |
| `05_fine_checkerboard.png` | Alternating single-pixel detail and strong high frequencies |
| `06_rgb_patches.png` | Red/green/blue/white channel order and color histograms |
| `07_low_contrast.png` | Values 80–120 for normalization/equalization |
| `08_salt_pepper_seed42.png` | Reproducible 10% approximate impulse noise |
| `09_odd_rgb_31x46.png` | Non-square image with an odd dimension |
| `10_large_rgb_1600x1200.png` | Upload/downscale; expected 1024×768 |
| `11_tiny_1x1.png`, `12_thin_2048x1.png` | Smallest image and extreme aspect ratio |
| `13_primary_rgb.png` | Exact grayscale values for R, G, B |
| `14_hist_exact_4x1.png` | Exact counts and equalization mapping |
| `15_hybrid_A_disk.png`, `16_hybrid_B_stripes.png` | Hybrid mechanics with aligned geometric patterns |
| `17_step.jpg`, `18_rgb.bmp`, `19_rgb.webp` | File format checks |
| `20_invalid.txt`, `21_corrupt.png` | Rejection/error recovery |

Also choose a real clean grayscale photograph, a colorful photograph, and two portraits with approximately aligned eyes/nose/mouth. Those photographs are not supplied. Synthetic hybrid images test mechanics; the perceptual face illusion needs appropriate real inputs and viewing sizes.

## 4. Manual run rules and evidence

For every test record ID, input filename, parameters, expected result, actual result, Pass/Fail, screenshot/network response, and issue link. `manual_results.csv` contains all checklist IDs for recording outcomes. Initially every manual case is NOT RUN.

- Reset to original before independent comparisons. Otherwise you may accidentally filter a prior result repeatedly.
- Use the same input and seed for comparisons of algorithms. Change one parameter at a time.
- Inspect DevTools Console and Network. For valid operations expect HTTP 200, readable images/charts, and a finite nonnegative processing time. No feature should still return 501.
- After every rejection, retry a valid image/request and confirm the app recovers.
- Use PNG downloads for exact comparisons. Visual similarity alone is insufficient.
- For float calculations use absolute tolerance 1e-10 on these small fixtures. Display conversion can introduce a 1-level difference; report max difference rather than requiring bitwise equality for every smoothing output.
- Keep screenshot images unmodified. Save parameters alongside screenshots.

## 5. Browser checklist — execute in this order

### A. Startup, upload, and color correctness

| ID | Steps | Pass criterion |
|---|---|---|
| U01 | Start backend/frontend; open localhost:5173 | Backend online; all sidebar routes accessible; no console exception |
| U02 | Visit every feature before upload | Helpful empty state; Hybrid asks for two images; no crash |
| U03 | Upload PNG, then JPG, BMP, WebP fixtures | Each supported image loads and processes |
| U04 | Upload RGB patches | Red stays red and blue stays blue in input, download, and result |
| U05 | Upload 1600×1200 fixture | Working dimensions 1024×768; aspect ratio preserved |
| U06 | Upload 31×46 and 1×1 fixtures; visit every feature | No shape errors; correct dimensions; finite stats |
| U07 | Upload invalid.txt, then corrupt.png (drag/drop where file picker restricts type) | Readable rejection; previous valid image remains usable; valid retry succeeds |
| U08 | Upload same filename twice after processing | Second selection still triggers upload and restores a fresh working image |
| U09 | Try extreme thin fixture | Valid image remains at least 1 pixel on each dimension; record frontend and direct-API results separately |

### B. Grayscale (feature 7)

| ID | Steps | Pass criterion |
|---|---|---|
| G01 | Upload primary RGB fixture; convert/download grayscale | R→76, G→149, B→29 using current truncation formula |
| G02 | Convert grayscale ramp | Pixel values unchanged |
| G03 | Convert RGB photo, Use as input, open Histogram | One grayscale channel; subsequent pages use gray image |

### C. Noise (feature 1)

| ID | Steps | Pass criterion |
|---|---|---|
| N01 | Constant 128; uniform low=-20, high=20, seed fixed | Values approximately 108–147; bounded, no wraparound; output shape/mode preserved |
| N02 | Same image; Gaussian mean=0, sigma=10 vs 40 | Higher sigma produces greater variation; do not require identical pattern across parameter changes |
| N03 | Same noise settings/seed, navigate away/back | Same result when the same seed is sent; New noise seed changes the image |
| N04 | Salt/pepper density=0 | Exact identity |
| N05 | Salt/pepper density=.1, salt ratio=.5 on constant gray/RGB | About 10% pixels black/white; same corrupted positions in all RGB channels |
| N06 | Salt ratio=0 then 1 at fixed density | Pepper only, then salt only |
| N07 | API: zero uniform noise and Gaussian sigma=0 | Exact identity; UI sigma minimum may require API/numerical test |
| N08 | API: add +20 to 250, then -20 to 5 | 255 and 0, never arithmetic wraparound |

### D. Spatial filters and manual/built-in comparison (feature 2)

| ID | Steps | Pass criterion |
|---|---|---|
| S01 | Constant image; average/Gaussian/median, k=3 then 15 | Constant preserved within 1 display level, including borders |
| S02 | Salt/pepper fixture; median k=3 | Isolated impulses removed; numerical fixture test returns exactly 128 |
| S03 | Photograph; average k=3 vs 9 vs 15 | Increasing neighborhood generally smooths detail; dimensions unchanged |
| S04 | Gaussian k=15, sigma=.5 vs 2 vs 4 | Stronger smoothing with larger sigma; keep k fixed to isolate effect |
| S05 | Each method; Built-in, Manual, Compare on gray and RGB | All modes work; compare shows both outputs, diff, times, speed ratio, max diff |
| S06 | Inspect differences for k=3,7,15 and image borders | Raw correlation differences ≤1e-10; displayed filtered pixels differ by at most 1 |
| S07 | Compare timing | Finite nonnegative timings and speed ratio; do not assume built-in must always win |

### E. Edges (feature 3)

| ID | Steps | Pass criterion |
|---|---|---|
| E01 | Constant image; Sobel/Prewitt/Roberts | Zero raw gradients/magnitude; no artificial boundary edges |
| E02 | Vertical step; Sobel and Prewitt | Gx responds strongly, Gy is zero; magnitude follows boundary |
| E03 | Horizontal step; Sobel and Prewitt | Gy responds strongly, Gx is zero |
| E04 | All 3 operators on odd image; Manual vs Built-in | gx/gy/magnitude/direction agree; Roberts dimensions correct |
| E05 | Clean and noisy photograph for each operator | Record noise response; no absolute claim that one image must prove a universal ranking |
| E06 | Canny on constant and step, pre-blur on/off | Flat image has no edges; step has binary 0/255 edges near boundary |
| E07 | Canny 20/60, 50/150, 100/200 on fixed photo | Record changing retained edges; threshold controls keep low≤high |
| E08 | Canny fixed thresholds, sigma .4,1.4,4 | Noise/detail changes; no crash at slider limits |
| E09 | Inspect numerical ramp and reversed ramp tests | Signed gradients reverse; magnitude remains nonnegative; orientation radians finite |

Roberts measures diagonal differences, so do not apply the simple Sobel/Prewitt horizontal/vertical interpretation literally to its two responses. Gx/Gy API previews show absolute values, which hide signs. Direction preview currently uses observed min-max stretching, not a fixed -pi to pi scale: verify angles numerically and log the caption mismatch separately if needed. Direction is not physically meaningful where magnitude is zero.

### F. Histograms, PDF, CDF (features 4 and 8)

| ID | Steps | Pass criterion |
|---|---|---|
| H01 | Constant 128 | Histogram only bin128=65536; CDF 0 before128 and 1 from128 onward |
| H02 | Gray ramp | Every bin count256; mean127.5; CDF ends1 and never decreases |
| H03 | RGB patches | 3 charts, correct channel labels/colors; each channel totals65536 pixels |
| H04 | Hover chart levels and inspect min/max/mean/std | Tooltip values match API counts/CDF and image data |
| H05 | Normalize/equalize photo; compare before/after charts | Charts correspond to the actual output, not a stale input |

### G. Equalization and normalization (features 5 and 6)

| ID | Steps | Pass criterion |
|---|---|---|
| Q01 | Low-contrast fixture; Normalize | Minimum0 and maximum255; order of intensities preserved |
| Q02 | Full-range gray ramp; Normalize | Exact identity |
| Q03 | Constant128; Normalize | All0; no NaN/divide-by-zero |
| Q04 | Low-contrast fixture; Equalize | Output matches project's CDF mapping; contrast distribution changes |
| Q05 | Exact4×1 fixture [0,0,1,2]; Equalize | [128,128,191,255] |
| Q06 | Constant128; Equalize | All255 under this project's formula; this is not a bug |
| Q07 | RGB photograph; Equalize and Normalize separately | Shape/dtype preserved; record hue shifts from per-channel equalization |

Do not use OpenCV equalizeHist as an exact oracle: this project uses round(CDF×255), without subtracting the first nonzero CDF. Equalization does not guarantee a perfectly flat histogram. Current RGB normalization stretches the whole RGB array using one global min/max; equalization works independently per channel. Signed normalization uses rounding in this completed upload, so [-10,0,10] becomes [0,128,255].

### H. Frequency filtering (feature 9)

| ID | Steps | Pass criterion |
|---|---|---|
| F01 | All 3 shapes × both kinds, gray and RGB | Four panels appear; correct shape; no missing mask/spectrum/result |
| F02 | Constant128; low-pass each shape | Constant preserved within1 level; raw value128 |
| F03 | Constant128; high-pass each shape | Raw≈0; display≈128 (offset preview), not necessarily black |
| F04 | Vertical step; ideal low-pass cutoff10 vs Gaussian/Butterworth | Inspect edge ripples and transitions; do not confuse periodic border effects with a resize bug |
| F05 | Gaussian low-pass cutoff5 vs50 | Lower cutoff generally blurrier; same input dimensions |
| F06 | High-pass cutoff5 vs50 | Lower spatial detail contribution as cutoff increases; inspect signed raw values if display is ambiguous |
| F07 | Butterworth order1,2,10 at cutoff20 | Transition approaches a sharper cutoff as order increases |
| F08 | Fine checkerboard | Small-cutoff low-pass suppresses alternating detail; high-pass retains it |
| F09 | Odd31×46 image | Center at floor(h/2),floor(w/2); no shifted output |
| F10 | Run numerical reconstruction and known sinusoid tests | LP+HP restores input ≤1e-10; ideal filter removes/keeps chosen frequency correctly |

The four spectrum previews are independently normalized for display. Do not interpret their displayed brightness as a directly comparable measurement of absolute spectral energy. Very small high-pass numerical residuals around zero can display as 127/128 after truncation. FFT filtering assumes periodic image boundaries; contrast between opposite image edges may create wraparound artefacts.

### I. Hybrid images (feature 10)

| ID | Steps | Pass criterion |
|---|---|---|
| Y01 | Geometric A/B supplied, Gaussian15/25 | 3 outputs; A broad shape with B detail; correct dimensions |
| Y02 | Two similarly aligned face photos | Tune cutoffs and View small; record perceptual change rather than claiming every pair must work |
| Y03 | Different-size A/B; swap | B resized to A; after swap output dimensions follow new A |
| Y04 | Gray+RGB, RGB+gray, gray+gray, RGB+RGB | Both gray if either gray; RGB only when both RGB |
| Y05 | Each shape, cutoff1 and100 endpoints | Valid results and stable controls |
| Y06 | Identical A=B, identical low/high filter settings via numerical test if needed | Raw sum reconstructs A; final uint8 can differ by1 due to truncation |
| Y07 | Run signed-detail test from kit | Darkening details preserved; high-pass preview is not added to A |
| Y08 | Upload B first; A defaults to working; replace own A; Use input image; swap twice | Slots and resulting image match displayed selections |

### J. Integrated user workflows and resilience

| ID | Steps | Pass criterion |
|---|---|---|
| W01 | Upload → Noise → Use as input → Median filter | Filters receive noisy output, not original; fixed test improves MSE |
| W02 | Reset to original → Grayscale → Use as input → Canny | Working thumbnail and processing input stay consistent |
| W03 | Use frequency result as input → Histogram | Histogram reflects the display-ready image (including high-pass offset), not hidden raw values |
| W04 | Download output → reupload PNG | Same decoded pixels; dimensions and colors preserved |
| W05 | Click image to enlarge; close with available controls; drag before/after divider | Correct image/modal behaviour; controls remain usable |
| W06 | Rapidly change slider, then stop at known value | Final response/image corresponds to final value; no stale result persists after settling |
| W07 | Rapidly replace input while processing, then switch feature | No old-image result remains after latest request completes; no console errors |
| W08 | Stop backend; change a control; restart backend and retry | Readable network failure and recovery; offline/online indicator updates |
| W09 | Dark/light; desktop and narrow viewport; keyboard Tab | Controls readable/reachable; menu and charts usable; no major overflow |
| W10 | Reload page | Image may clear (state is in memory); graceful empty state, not crash |
| W11 | Check requests in Network | Correct payload, image selection, method, seed, implementation, cutoffs, sigma, order |
| W12 | Open all routes and change slider minimum/maximum | No unexpected501 or500 for supported UI inputs |

The frontend aborts the previous request when the next debounced request begins, not immediately on every slider movement. Test visible behaviour under network throttling; do not assume the hook's comment proves race-free behaviour.

## 6. API boundary checks

Use the automated tests for repeatability. To reproduce manually, open localhost:8000/docs and reuse a valid image data URL copied from a browser Network request. Never paste local Windows paths into the `image` field: this API expects a data URL.

| Category | Requests | Expected |
|---|---|---|
| Correct content | All endpoints and success matrix | HTTP200, expected keys, decodable images, finite nonnegative timing |
| Unknown options | Unknown method/kind/shape/implementation | HTTP400 with readable detail |
| Filter | k=0, negative, even; sigma=0/negative; invalid implementation | HTTP400; no server traceback response |
| Canny | low>high, negative thresholds, sigma≤0 | HTTP400 |
| Noise | density outside[0,1], ratio outside[0,1], sigma<0, low>high | HTTP400 |
| Frequency/hybrid | cutoff≤0; order≤0; unknown shape | HTTP400 |
| Wrong/missing JSON fields | Missing image/method, wrong incompatible types | FastAPI HTTP422 is expected for schema validation |
| Empty/null optional numeric parameter | Explicit null sigma/order/etc. | Reject cleanly or use documented default; never HTTP500 |
| Image bytes | Corrupt/empty/invalid base64/non-image payload | HTTP400 with detail; recover on next valid request |
| Extremely thin valid image | 1×2048 and2048×1 | Valid downscale with both sides≥1 |
| Hybrid input B | Corrupt B, missing B, mismatched mode/size | Corrupt400; missing422; valid mismatch handled automatically |
| CORS | OPTIONS from localhost:5173 | Correct allow-origin/header behaviour; in-process test plus real-browser check |

Some planned boundary cases above extend beyond the supplied automated subset. Record them manually or extend the tests; do not assume the entire table was executed.

## 7. Confirmed failures in this upload

These 10 test failures are grouped by reproduction, with no application changes applied:

| Failure cases | Actual | Expected | Likely location / suggested fix area |
|---|---|---|---|
| Gaussian filter sigma=0 |500|400| `api/filters.py`: core ValueError is not caught |
| Gaussian filter sigma=null |500|clean4xx| Request allows None; kernel validation cannot handle it |
| Filter implementation='invalid' |500|400| Validate implementation or catch core ValueError |
| Sobel implementation='invalid' |500|400| `api/edges.py`: non-Canny ValueError is not caught |
| Uniform noise low20/high-20 |500|400| Parameter error happens in apply(), outside constructor catch |
| Gaussian noise sigma=-1 |500|400| Same noise apply() error handling gap |
| Empty image string and empty data URL (2 cases) |500|400| `utils/image_io.py`: empty buffer reaches cv2.imdecode |
| Valid1×2048 and2048×1 API images (2 cases) |500|200| int(dimension×scale) becomes0 in backend resize; clamp each dimension to≥1 |

The empty and thin-image issues are in shared image decoding and may affect multiple endpoints. Thin-image API errors may not appear through normal browser upload because the frontend already clamps scaled dimensions to at least1. These are error-handling/edge-input defects, not evidence that all normal image calculations fail. Teams should prioritize fixing normal UI crashes first if any are discovered during the manual run.

## 8. Performance and repeated-use checks

Do these after correctness checks, with backend logs and browser Network open. Record browser/device, image dimensions, method, params, and implementation. Hardware differs, so no universal timing threshold is claimed.

1. Use 256×256,512×512,1024×1024 inputs, gray and RGB. Compare average/Gaussian/median at k3,7,15 in manual/built-in modes.
2. Warm up once, then run each measurement five times. Report median request wall time separately from backend `meta.time_ms`; backend timing excludes parts of decoding/encoding depending on route.
3. Watch peak memory during 1024px RGB manual median k15. Sliding-window median can allocate substantial temporary memory. Stop and record if the app stalls or memory pressure becomes unacceptable.
4. Repeat uploads and feature changes20 times. Check for indefinitely stuck loading, unbounded memory growth after settling, or stale images.
5. Throttle network and change cutoff rapidly. Ensure the final result matches a freshly repeated request at the final settings.
6. Suggested team usability target (agree before applying): normal1024px operations settle within5 seconds on the demo laptop, and no endless spinner after an error. This is a proposed target, not a repository requirement.

## 9. Source-rule review (TA requirements)

Inspect implementation files, not only UI output:

- Manual correlation loops over kernel positions, not image pixels; border alignment matches SciPy, especially2×2 Roberts.
- From-scratch code does not call forbidden cv2/skimage histogram/filter/equalization operations. Test code may use independent library oracles without making the application's algorithm library-based.
- BGR/RGB conversion stays in image I/O; grayscale uses the manual weighted formula.
- Sobel/Prewitt/Roberts share EdgeDetector; FrequencyFilter builds masks manually; HybridImage reuses it without FFT duplication.
- Signed gradients and high-pass values remain float until after magnitude/hybrid summation.
- Math stays in core; API decodes/calls/encodes; no source placeholders remain in active execution paths.
- Reports include screenshots, parameters, observed tradeoffs, and manual/built-in comparison. Inactive TODO comments alone are not proof of missing functionality.

## 10. Release decision

Release-ready when:

- All existing and expanded acceptance tests pass, or the team explicitly documents and accepts the remaining defects.
- Every manual case is Pass or has a justified Not applicable; none is silently left untested.
- No valid supported UI workflow produces500/501 or incorrect output.
- API rejects invalid inputs cleanly; image dimensions, channel order, and signed intermediate values are correct.
- Frontend build succeeds; no uncaught browser errors during a complete demo.
- Gray/RGB, odd/even dimensions, borders, constants, real photos, and hybrid mode/size combinations have evidence.
- Defects have owner, reproduction, expected/actual result, and regression test. Retest fixes and adjacent workflows rather than blindly repeating all expensive tests.

## References

- Uploaded repository: `CLAUDE.md` §§3–8,11; core/API/frontend code and three existing test files. This local snapshot is the authority for project-specific expectations.
- pytest invocation: https://docs.pytest.org/en/stable/how-to/usage.html
- FastAPI testing: https://fastapi.tiangolo.com/tutorial/testing/
- FastAPI TestClient: https://fastapi.tiangolo.com/reference/testclient/
- NumPy FFT: https://numpy.org/doc/stable/reference/routines.fft.html
- SciPy correlation border/anchor documentation: https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.correlate.html
