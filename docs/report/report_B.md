# Report — Member B: Noise & smoothing filters

**Name:** Member B

## What I implemented
- **Additive noise:** Uniform, Gaussian, and Salt & Pepper noise (Feature 1).
  - Uniform and Gaussian noise use library pseudo-random generators (`np.random.Generator.uniform` / `normal`).
  - Salt & pepper noise is implemented completely **from scratch** with identical spatial corruptions across all channels for color images.
- **Low-pass spatial filters:** Box/Average, Gaussian, and Median filters (Feature 2).
  - Average and Gaussian filtering run through the 2D correlation engine.
  - Median filtering is implemented both **from scratch** using vectorized sliding windows (`sliding_window_view`) and via built-in `scipy.ndimage.median_filter`.
- **Convolution engine:** Vectorized manual 2D correlation (looping solely over kernel dimensions) vs SciPy built-in `correlate`, with exact symmetric/reflect border alignment and automatic per-channel handling.
- **Performance & equivalence analysis:** `run_both` benchmarking utility tracking execution times, speed-up ratios, and absolute difference images ($L_\infty \approx 0$).

## Algorithms (short)

### 1. Noise Generation
- **Uniform Noise:** Adds sampled noise $n \sim \mathcal{U}(\text{low}, \text{high})$ to each pixel value: $I_{\text{noisy}} = \text{clip}(I + n, 0, 255)$.
- **Gaussian Noise:** Adds sampled noise $n \sim \mathcal{N}(\mu, \sigma^2)$ to each pixel value: $I_{\text{noisy}} = \text{clip}(I + n, 0, 255)$.
- **Salt & Pepper Noise (From Scratch):** Generates a 2D random probability mask $M \in [0, 1)^{H \times W}$. Pixels where $M < \text{density} \times \text{salt\_ratio}$ are set to maximum intensity (255, salt), while pixels where $\text{density} \times \text{salt\_ratio} \le M < \text{density}$ are set to 0 (pepper). For RGB inputs, the exact same spatial coordinates are assigned salt/pepper across all 3 color channels simultaneously.

### 2. Spatial Low-Pass Smoothing
- **Average (Box) Filter (From Scratch):** Generates an odd $k \times k$ kernel $K_{a,b} = \frac{1}{k^2}$. Convolves/correlates with the padded image, preserving total average intensity.
- **Gaussian Filter (From Scratch):** Generates a centered 2D Gaussian kernel:
  $$G(x, y) = \frac{1}{2\pi\sigma^2} e^{-\frac{x^2 + y^2}{2\sigma^2}}$$
  sampled on integer grid coordinates centered at $(k // 2, k // 2)$ and normalized such that $\sum K = 1$.
- **Median Filter (From Scratch):** Applies symmetric padding of size $k // 2$, constructs non-copy sliding window views of shape $(H, W, k, k)$ using `np.lib.stride_tricks.sliding_window_view`, and calculates `np.median(..., axis=(-2, -1))` to extract order-statistic rank without linear blur.

### 3. Vectorized Correlation Engine (From Scratch vs Built-in)
- **Manual Engine:** Avoids pixel-by-pixel Python loops. Instead, iterates solely over the $k_h \times k_w$ kernel coordinates ($a, b$), accumulating shifted slice windows:
  $$\text{out} = \sum_{a=0}^{k_h-1} \sum_{b=0}^{k_w-1} K[a, b] \cdot \text{padded}[a:a+H, b:b+W]$$
- **Boundary Handling:** Uses symmetric reflection (`np.pad(mode="symmetric")`), matching `scipy.ndimage.correlate(..., mode="reflect")`. Supports even kernels (e.g. Roberts $2 \times 2$) by offsetting asymmetric anchors.

## Observations on parameter variations

- **Kernel size 3 vs 5 vs 7: how blur and detail loss grow:**
  Increasing the kernel size aggregates a wider spatial neighborhood into every pixel. For average and Gaussian filters, going from $3 \times 3$ to $5 \times 5$ and $7 \times 7$ drastically attenuates high-frequency edges and fine textures, turning subtle gradients into flat regions. At $7 \times 7$, sharp object boundaries and text become unreadable halos.

- **Average vs Gaussian vs median on salt & pepper noise:**
  Median filtering performs exceptionally well on impulse (salt & pepper) noise because the median is an order statistic that completely ignores outlier extremes (0 and 255) as long as corrupted pixels constitute less than half the window. In contrast, average and Gaussian filters linearly smear black and white spikes into neighboring pixels, resulting in dark and bright cloudy smudges rather than clean noise removal.

- **Average vs Gaussian vs median on Gaussian noise:**
  For zero-mean additive Gaussian noise, linear filters (Gaussian and Average) are mathematically optimal estimators of the underlying signal, reducing variance by averaging independent noise samples. Gaussian filtering is superior to average filtering because it gives higher weight to closer pixels, preserving localized edge structure better than a uniform box blur. Median filtering reduces Gaussian noise reasonably well, but introduces undesirable patch-like ("watercolor") artifacts and flat regions.

- **Effect of Gaussian sigma ($\sigma$):**
  $\sigma$ controls the spatial spread (effective window) of the Gaussian bell curve. When $\sigma$ is small ($\le 0.8$), central weights dominate and smoothing is minimal. As $\sigma$ increases, the bell curve widens, distributing weights evenly across the kernel and converging toward a box blur behavior. Setting $\sigma$ too large for a given kernel size leads to kernel truncation artifacts, which is why the kernel size should ideally follow $k \approx 6\sigma + 1$.

- **Manual vs built-in: time (ms), speed-up, max difference:**
  - **Max absolute difference:** Consistently evaluated to **0.0** (or $< 10^{-14}$ floating-point precision error) across box, Gaussian, and median filters.
  - **Speed comparison:** The built-in SciPy functions are compiled in C/Fortran and utilize SIMD CPU optimizations, executing in approximately $0.5 - 2$ ms on typical inputs. The manual vectorized implementation executes in approximately $1 - 10$ ms depending on kernel dimensions ($k^2$ slice additions). The manual approach achieves high efficiency without any per-pixel Python looping overhead.

## Problems faced and how I solved them

1. **Integer Wrap-Around during Noise and Convolution:**
   - *Problem:* Applying additive noise directly to `uint8` images caused overflow (e.g., $250 + 20 \to 14$ instead of $255$).
   - *Solution:* All images are cast to `float64` before applying arithmetic operations or noise additions, and clamped via `np.clip(..., 0, 255).astype(np.uint8)` at the end.

2. **Multichannel Salt & Pepper Consistency:**
   - *Problem:* Generating separate independent masks for R, G, and B created colored noise specks (e.g. magenta or green dots) instead of realistic salt (white) and pepper (black).
   - *Solution:* Generated a 2D mask $(H, W)$ and broadcasted it across all 3 color channels, guaranteeing that corrupted pixels are pure black or pure white across channels.

3. **SciPy Reflect vs NumPy Symmetric Padding:**
   - *Problem:* Discrepancies between manual and built-in convolution outputs arose from border naming conventions.
   - *Solution:* NumPy's `mode="symmetric"` corresponds exactly to SciPy's `mode="reflect"`. Aligning these border conditions ensured `max_abs_diff` is 0.
