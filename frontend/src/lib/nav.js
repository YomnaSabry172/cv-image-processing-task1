// Owner: Lead — navigation: one list used by the sidebar, the routes and the Home overview
import {
  Activity,
  BarChart3,
  Blend,
  Contrast,
  Droplets,
  Home,
  Layers,
  ScanLine,
  SlidersHorizontal,
  Sparkles,
  Waves,
} from 'lucide-react'

export const NAV_GROUPS = [
  {
    label: 'Start',
    items: [{ path: '/', label: 'Home', icon: Home, description: 'Upload an image and see an overview.' }],
  },
  {
    label: 'Basics',
    items: [
      { path: '/grayscale', label: 'Grayscale', icon: Contrast, description: 'Convert a color image to gray.' },
    ],
  },
  {
    label: 'Noise & Smoothing',
    items: [
      { path: '/noise', label: 'Noise', icon: Sparkles, description: 'Add uniform, Gaussian or salt & pepper noise.' },
      { path: '/filters', label: 'Filters', icon: Droplets, description: 'Average, Gaussian and median low-pass filters.' },
    ],
  },
  {
    label: 'Edges',
    items: [
      { path: '/edges', label: 'Edge Detection', icon: ScanLine, description: 'Sobel, Prewitt, Roberts and Canny.' },
    ],
  },
  {
    label: 'Histograms',
    items: [
      { path: '/histogram', label: 'Histogram & CDF', icon: BarChart3, description: 'Histogram and distribution curve per channel.' },
      { path: '/equalize', label: 'Equalization', icon: Activity, description: 'Spread gray levels using the CDF.' },
      { path: '/normalize', label: 'Normalization', icon: SlidersHorizontal, description: 'Stretch values to the full 0–255 range.' },
    ],
  },
  {
    label: 'Frequency',
    items: [
      { path: '/frequency', label: 'Frequency Filters', icon: Waves, description: 'Low-pass and high-pass filters in the Fourier domain.' },
      { path: '/hybrid', label: 'Hybrid Image', icon: Blend, description: 'Low frequencies of one image + high of another.' },
    ],
  },
]

/** All feature pages (everything except Home). */
export const FEATURES = NAV_GROUPS.flatMap((g) => g.items.map((item) => ({ ...item, group: g.label }))).filter(
  (item) => item.path !== '/',
)

export const APP_ICON = Layers
