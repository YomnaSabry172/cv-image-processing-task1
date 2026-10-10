// Owner: B — Noise page (UI built by Lead in Phase 0; backend: core/noise.py)
import { useState } from 'react'
import { Dices } from 'lucide-react'
import { useImage } from '../context/ImageContext'
import { useProcess } from '../hooks/useProcess'
import { useAutoRun } from '../hooks/useAutoRun'
import PageShell from '../components/layout/PageShell'
import ResultArea from '../components/layout/ResultArea'
import BeforeAfterSlider from '../components/ui/BeforeAfterSlider'
import Button from '../components/ui/Button'
import ImageGrid from '../components/ui/ImageGrid'
import ImagePanel from '../components/ui/ImagePanel'
import ParamSlider from '../components/ui/ParamSlider'
import SegmentedControl from '../components/ui/SegmentedControl'

const TYPES = [
  { value: 'uniform', label: 'Uniform' },
  { value: 'gaussian', label: 'Gaussian' },
  { value: 'salt_pepper', label: 'Salt & pepper' },
]

export default function Noise() {
  const { working } = useImage()
  const [type, setType] = useState('gaussian')
  const [low, setLow] = useState(-50)
  const [high, setHigh] = useState(50)
  const [mean, setMean] = useState(0)
  const [sigma, setSigma] = useState(25)
  const [density, setDensity] = useState(0.05)
  const [saltRatio, setSaltRatio] = useState(0.5)
  // A fixed seed keeps the noise pattern stable while you move sliders; the dice button picks a new one.
  const [seed, setSeed] = useState(42)

  const params =
    type === 'uniform' ? { low, high } : type === 'gaussian' ? { mean, sigma } : { density, salt_ratio: saltRatio }

  const process = useProcess('/noise')
  useAutoRun(process.run, working ? { image: working, type, seed, ...params } : null)
  const result = process.data?.images?.result

  const controls = (
    <>
      <SegmentedControl label="Noise type" options={TYPES} value={type} onChange={setType} size="sm" />

      {type === 'uniform' && (
        <>
          <ParamSlider label="Low" value={low} onChange={(v) => setLow(Math.min(v, high))} min={-128} max={128} hint="Smallest value added to a pixel." />
          <ParamSlider label="High" value={high} onChange={(v) => setHigh(Math.max(v, low))} min={-128} max={128} hint="Largest value added to a pixel." />
        </>
      )}
      {type === 'gaussian' && (
        <>
          <ParamSlider label="Mean (μ)" value={mean} onChange={setMean} min={-64} max={64} hint="Average shift. 0 keeps overall brightness." />
          <ParamSlider label="Sigma (σ)" value={sigma} onChange={setSigma} min={1} max={100} hint="Spread of the noise. Bigger = noisier." />
        </>
      )}
      {type === 'salt_pepper' && (
        <>
          <ParamSlider label="Density" value={density} onChange={setDensity} min={0} max={0.5} step={0.01}
            format={(v) => `${Math.round(v * 100)}`} unit="%" hint="Share of pixels replaced by black or white." />
          <ParamSlider label="Salt ratio" value={saltRatio} onChange={setSaltRatio} min={0} max={1} step={0.05}
            format={(v) => `${Math.round(v * 100)}`} unit="% white" hint="Of the corrupted pixels, how many become white (salt)." />
        </>
      )}

      <div className="flex items-center justify-between gap-2">
        <span className="text-xs text-zinc-500">Seed <span className="font-mono text-zinc-900 dark:text-zinc-100">{seed}</span></span>
        <Button size="sm" icon={Dices} onClick={() => setSeed(Math.floor(Math.random() * 1e6))}>New noise</Button>
      </div>
    </>
  )

  return (
    <PageShell
      title="Noise"
      description="Additive uniform and Gaussian noise, and salt & pepper noise (random pixels set to black or white). Use the result as input, then try the Filters page."
      controls={controls}
      timeMs={process.data?.meta?.time_ms}
    >
      <ResultArea process={process}>
        <ImageGrid cols={2}>
          <BeforeAfterSlider before={working} after={result} beforeLabel="Input" afterLabel="Noisy" />
          <ImagePanel title="Noisy image" src={result} useAsInput caption="Use as input, then open Filters to remove the noise." />
        </ImageGrid>
      </ResultArea>
    </PageShell>
  )
}
