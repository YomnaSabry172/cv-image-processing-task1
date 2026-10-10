// Owner: B — Filters page (UI built by Lead in Phase 0; backend: core/spatial.py, core/compare.py)
import { useState } from 'react'
import { useImage } from '../context/ImageContext'
import { useProcess } from '../hooks/useProcess'
import { useAutoRun } from '../hooks/useAutoRun'
import PageShell from '../components/layout/PageShell'
import ResultArea from '../components/layout/ResultArea'
import BeforeAfterSlider from '../components/ui/BeforeAfterSlider'
import ImageGrid from '../components/ui/ImageGrid'
import ImagePanel from '../components/ui/ImagePanel'
import ImplementationToggle from '../components/ui/ImplementationToggle'
import ParamSlider from '../components/ui/ParamSlider'
import SegmentedControl from '../components/ui/SegmentedControl'

const METHODS = [
  { value: 'average', label: 'Average' },
  { value: 'gaussian', label: 'Gaussian' },
  { value: 'median', label: 'Median' },
]

function Stat({ label, value, unit }) {
  return (
    <div className="rounded-xl border border-zinc-200 bg-white p-3 dark:border-zinc-800 dark:bg-zinc-900">
      <div className="text-[11px] text-zinc-500">{label}</div>
      <div className="mt-0.5 font-mono text-lg font-semibold tabular-nums text-zinc-900 dark:text-zinc-100">
        {value}
        {unit && <span className="ml-1 text-xs font-normal text-zinc-500">{unit}</span>}
      </div>
    </div>
  )
}

export default function Filters() {
  const { working } = useImage()
  const [method, setMethod] = useState('median')
  const [kernelSize, setKernelSize] = useState(3)
  const [sigma, setSigma] = useState(1)
  const [implementation, setImplementation] = useState('builtin')

  const process = useProcess('/filter')
  useAutoRun(
    process.run,
    working
      ? { image: working, method, kernel_size: kernelSize, implementation, ...(method === 'gaussian' ? { sigma } : {}) }
      : null,
  )
  const images = process.data?.images
  const stats = process.data?.data
  const isCompare = implementation === 'compare' && images?.manual

  const controls = (
    <>
      <SegmentedControl label="Filter" options={METHODS} value={method} onChange={setMethod} size="sm" />
      <ParamSlider label="Kernel size" value={kernelSize} onChange={setKernelSize} min={3} max={15} step={2}
        format={(v) => `${v}×${v}`} hint="Bigger kernel = stronger blur." />
      {method === 'gaussian' && (
        <ParamSlider label="Sigma (σ)" value={sigma} onChange={setSigma} min={0.2} max={5} step={0.1}
          format={(v) => v.toFixed(1)} hint={`Rule of thumb: kernel ≈ 6σ + 1 (≈ ${2 * Math.ceil(3 * sigma) + 1} here).`} />
      )}
      <ImplementationToggle value={implementation} onChange={setImplementation} />
      <p className="text-[11px] leading-snug text-zinc-500">
        <strong>Manual</strong> is our own vectorized code; <strong>Built-in</strong> uses SciPy.{' '}
        <strong>Compare</strong> runs both and shows the timing and the difference.
      </p>
    </>
  )

  return (
    <PageShell
      title="Low-pass filters"
      description="Average and Gaussian are weighted sums (convolution). Median sorts each neighborhood and takes the middle value, which removes salt & pepper noise best."
      controls={controls}
      timeMs={process.data?.meta?.time_ms}
    >
      <ResultArea process={process}>
        {isCompare ? (
          <>
            <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
              <Stat label="Manual time" value={stats.time_manual_ms} unit="ms" />
              <Stat label="Built-in time" value={stats.time_builtin_ms} unit="ms" />
              <Stat label="Speed-up" value={`${stats.speedup}×`} />
              <Stat label="Max |difference|" value={stats.max_abs_diff} />
            </div>
            <ImageGrid cols={3}>
              <ImagePanel title="Manual" src={images.manual} useAsInput />
              <ImagePanel title="Built-in" src={images.builtin} useAsInput />
              <ImagePanel title="|Manual − Built-in|" src={images.difference} pixelated caption="Black = identical. Max difference ≈ 0 proves the manual code is correct." />
            </ImageGrid>
          </>
        ) : (
          images?.result && (
            <ImageGrid cols={2}>
              <BeforeAfterSlider before={working} after={images.result} beforeLabel="Input" afterLabel="Filtered" />
              <ImagePanel title={`${METHODS.find((m) => m.value === method).label} ${kernelSize}×${kernelSize}`} src={images.result} useAsInput />
            </ImageGrid>
          )
        )}
      </ResultArea>
    </PageShell>
  )
}
