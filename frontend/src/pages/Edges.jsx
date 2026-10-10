// Owner: C — Edge Detection page (UI built by Lead in Phase 0; backend: core/edges.py)
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
import Toggle from '../components/ui/Toggle'

const METHODS = [
  { value: 'sobel', label: 'Sobel' },
  { value: 'prewitt', label: 'Prewitt' },
  { value: 'roberts', label: 'Roberts' },
  { value: 'canny', label: 'Canny' },
]

export default function Edges() {
  const { working } = useImage()
  const [method, setMethod] = useState('sobel')
  const [implementation, setImplementation] = useState('builtin')
  const [low, setLow] = useState(50)
  const [high, setHigh] = useState(150)
  const [blur, setBlur] = useState(true)
  const [blurSigma, setBlurSigma] = useState(1.4)

  const isCanny = method === 'canny'
  const body = !working
    ? null
    : isCanny
      ? { image: working, method, low, high, blur_sigma: blur ? blurSigma : null }
      : { image: working, method, implementation }

  const process = useProcess('/edges')
  useAutoRun(process.run, body)
  const images = process.data?.images

  const controls = (
    <>
      <SegmentedControl label="Operator" options={METHODS} value={method} onChange={setMethod} size="sm" />
      {isCanny ? (
        <>
          <ParamSlider label="Low threshold" value={low} onChange={(v) => setLow(Math.min(v, high))} min={0} max={255}
            hint="Weak edges above this are kept only if they connect to a strong edge." />
          <ParamSlider label="High threshold" value={high} onChange={(v) => setHigh(Math.max(v, low))} min={0} max={255}
            hint="Edges above this are always kept (strong edges)." />
          <Toggle label="Gaussian pre-blur" checked={blur} onChange={setBlur} hint="Smoothing first removes noise that would create false edges." />
          {blur && (
            <ParamSlider label="Blur sigma (σ)" value={blurSigma} onChange={setBlurSigma} min={0.4} max={4} step={0.1} format={(v) => v.toFixed(1)} />
          )}
        </>
      ) : (
        <>
          <ImplementationToggle value={implementation} onChange={setImplementation} allowCompare={false} />
          <p className="text-[11px] leading-snug text-zinc-500">
            Gx responds to <strong>vertical</strong> edges (change along x), Gy to <strong>horizontal</strong> edges.
            The image is converted to gray first.
          </p>
        </>
      )}
    </>
  )

  return (
    <PageShell
      title="Edge detection"
      description="First-derivative operators measure how fast brightness changes. Magnitude = √(Gx² + Gy²) is edge strength; direction = arctan2(Gy, Gx) is edge orientation."
      controls={controls}
      timeMs={process.data?.meta?.time_ms}
    >
      <ResultArea process={process}>
        {isCanny && images?.result && (
          <ImageGrid cols={2}>
            <BeforeAfterSlider before={working} after={images.result} beforeLabel="Input" afterLabel="Canny" />
            <ImagePanel title="Canny edges" src={images.result} useAsInput pixelated />
          </ImageGrid>
        )}
        {!isCanny && images?.gx && (
          <ImageGrid cols={2}>
            <ImagePanel title="Gx (|horizontal gradient|)" src={images.gx} pixelated />
            <ImagePanel title="Gy (|vertical gradient|)" src={images.gy} pixelated />
            <ImagePanel title="Magnitude" src={images.magnitude} useAsInput pixelated caption="Edge strength." />
            <ImagePanel title="Direction" src={images.direction} pixelated caption="Angle −π…π mapped to black…white." />
          </ImageGrid>
        )}
      </ResultArea>
    </PageShell>
  )
}
