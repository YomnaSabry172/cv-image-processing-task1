# Report — Member D: Histograms, equalization & normalization

**Name:** _Alaa Essam_

## What I implemented
- Histogram, PDF and CDF for gray images and for R, G, B channels (features 4 and 8)
- Histogram equalization (feature 5)
- Min-max normalization (feature 6)

Everything is written from scratch in `core/histogram.py`. I did not use `np.histogram`, `np.bincount`, `cv2.calcHist`, `cv2.equalizeHist` or `cv2.normalize`.

## Algorithms (short)

**Histogram.** `hist[v]` is the number of pixels with value `v`. I count with `np.add.at(hist, pixels, 1)`, which adds 1 at each pixel's value, including repeated values. Library: only NumPy indexing.

**PDF and CDF.** `pdf[i] = hist[i] / N`, where N is the number of pixels. `cdf[i] = pdf[0] + ... + pdf[i]` is a running sum, so it ends at 1. For color images I do this separately for R, G and B.

**Equalization.** I build a lookup table `lut[i] = round(cdf[i] * 255)` and replace every pixel with `lut[pixel]`. Levels that hold many pixels get spread apart, so contrast goes up. Color images are equalized per channel. Library: only NumPy.

**Normalization (min-max).** `out = (x - min) / (max - min) * 255`. The smallest value becomes 0 and the largest becomes 255. If `max == min` the image is constant, so I return a constant image to avoid dividing by zero. The same function also displays signed results (edges, high-pass) in the rest of the app.

## Results
_Add screenshots from the running app (names: `D_<feature>_<what>.png`)._

| Original | Histogram + CDF | Equalized | Equalized histogram + CDF |
|:---:|:---:|:---:|:---:|
| ![](screenshots/D_original.png) | ![](screenshots/D_hist_original.png) | ![](screenshots/D_equalized.png) | ![](screenshots/D_hist_equalized.png) |

| Original | Normalized | Normalized histogram |
|:---:|:---:|:---:|
| ![](screenshots/D_original.png) | ![](screenshots/D_normalized.png) | ![](screenshots/D_hist_normalized.png) |

## Observations on parameter variations
_Check each point against your own screenshots before submitting._

- **Histogram shape of dark, bright and low-contrast images:** a dark image has its bars bunched at the left, a bright one at the right. A low-contrast image has a narrow peak in the middle with empty space on both sides. The CDF rises steeply only where the bars are.
- **Before/after equalization: histogram and CDF:** after equalization the bars spread across 0–255, and the CDF gets close to a straight diagonal line. The histogram is not perfectly flat, because levels are only moved, never split, so gaps stay between bars.
- **Normalization vs equalization on the same image:** normalization only stretches the range. The histogram keeps exactly the same shape and the CDF keeps its shape, only wider. Equalization changes the shape. Normalization cannot help an image that already uses 0 to 255, but equalization still can.
- **Color image: per-channel equalization and the color shift:** each channel gets its own lookup table, so the balance between R, G and B changes and colors can look wrong (for example a tint). Normalization uses one global min and max for all channels, so colors stay balanced.

## Problems faced and how I solved them
- **Counting repeated values:** `hist[pixels] += 1` counts each value only once. I used `np.add.at`, which handles repeats.
- **Constant image:** `max == min` would divide by zero in normalization. I return a constant image instead.