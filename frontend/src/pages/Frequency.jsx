// Owner: C — Frequency Filters page (UI built by Lead in Phase 0; backend: core/frequency.py)
import { useState } from 'react'
import { useImage } from '../context/ImageContext'
import { useProcess } from '../hooks/useProcess'
import { useAutoRun } from '../hooks/useAutoRun'
import PageShell from '../components/layout/PageShell'
import ResultArea from '../components/layout/ResultArea'
import ImageGrid from '../components/ui/ImageGrid'
import ImagePanel from '../components/ui/ImagePanel'
import ParamSlider from '../components/ui/ParamSlider'
import SegmentedControl from '../components/ui/SegmentedControl'

const KINDS = [
  { value: 'lowpass', label: 'Low-pass' },
  { value: 'highpass', label: 'High-pass' },
]
const SHAPES = [
  { value: 'ideal', label: 'Ideal' },
  { value: 'gaussian', label: 'Gaussian' },
  { value: 'butterworth', label: 'Butterworth' },
]

export default function Frequency() {
  const { working } = useImage()
  const [kind, setKind] = useState('lowpass')
  const [shape, setShape] = useState('gaussian')
  const [cutoff, setCutoff] = useState(30)
  const [order, setOrder] = useState(2)

  const process = useProcess('/frequency')
  useAutoRun(
    process.run,
    working ? { image: working, kind, shape, cutoff, ...(shape === 'butterworth' ? { order } : {}) } : null,
  )
  const images = process.data?.images

  const controls = (
    <>
      <SegmentedControl label="Filter type" options={KINDS} value={kind} onChange={setKind} />
      <SegmentedControl label="Mask shape" options={SHAPES} value={shape} onChange={setShape} size="sm" />
      <ParamSlider label="Cutoff (D₀)" value={cutoff} onChange={setCutoff} min={1} max={200} unit="px"
        hint="Radius from the spectrum center. Low-pass: smaller = blurrier. High-pass: larger = thinner edges." />
      {shape === 'butterworth' && (
        <ParamSlider label="Order (n)" value={order} onChange={setOrder} min={1} max={10}
          hint="Higher order = sharper cut (closer to Ideal)." />
      )}
      <p className="text-[11px] leading-snug text-zinc-500">
        Spectrum center = low frequencies, edges = high frequencies. The Ideal mask has a sharp edge, which causes
        ringing (ripples) in the result.
      </p>
    </>
  )

  return (
    <PageShell
      title="Frequency-domain filters"
      description="FFT → multiply by a mask → inverse FFT. Low-pass keeps slow changes (blur); high-pass keeps fast changes (edges, detail). Spectra are shown as log(1 + |F|)."
      controls={controls}
      timeMs={process.data?.meta?.time_ms}
    >
      <ResultArea process={process}>
        {images?.result && (
          <ImageGrid cols={2}>
            <ImagePanel title="Spectrum  log(1+|F|)" src={images.spectrum} />
            <ImagePanel title="Mask" src={images.mask} pixelated caption="White = frequencies kept, black = removed." />
            <ImagePanel title="Filtered spectrum" src={images.filtered_spectrum} />
            <ImagePanel title="Result" src={images.result} useAsInput
              caption={kind === 'highpass' ? 'High-pass output is signed; mid-gray = 0.' : undefined} />
          </ImageGrid>
        )}
      </ResultArea>
    </PageShell>
  )
}
