// Owner: C — Hybrid Image page (UI built by Lead in Phase 0; backend: core/hybrid.py)
import { useState } from 'react'
import { ArrowLeftRight, RotateCcw } from 'lucide-react'
import { useImage } from '../context/ImageContext'
import { useProcess } from '../hooks/useProcess'
import { useAutoRun } from '../hooks/useAutoRun'
import { readImageFile } from '../lib/image'
import PageShell from '../components/layout/PageShell'
import ResultArea from '../components/layout/ResultArea'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'
import ImageDropzone from '../components/ui/ImageDropzone'
import ImageGrid from '../components/ui/ImageGrid'
import ImagePanel from '../components/ui/ImagePanel'
import ParamSlider from '../components/ui/ParamSlider'
import SegmentedControl from '../components/ui/SegmentedControl'
import Toggle from '../components/ui/Toggle'

const SHAPES = [
  { value: 'ideal', label: 'Ideal' },
  { value: 'gaussian', label: 'Gaussian' },
  { value: 'butterworth', label: 'Butterworth' },
]
const SMALL_SCALES = [1, 0.5, 0.25, 0.125]

function Slot({ label, role, src, onFile, onClear, clearLabel }) {
  return (
    <div className="flex min-w-0 flex-col gap-2">
      <div className="flex items-center justify-between gap-2">
        <div>
          <div className="text-xs font-semibold text-zinc-900 dark:text-zinc-100">{label}</div>
          <div className="text-[11px] text-zinc-500">{role}</div>
        </div>
        {src && onClear && (
          <Button size="sm" variant="ghost" icon={RotateCcw} onClick={onClear}>{clearLabel}</Button>
        )}
      </div>
      {src ? (
        <div className="flex aspect-4/3 items-center justify-center rounded-lg bg-zinc-900 p-1.5 dark:bg-zinc-950">
          <img src={src} alt={label} className="max-h-full max-w-full object-contain" />
        </div>
      ) : null}
      <ImageDropzone compact onFile={onFile} label={src ? 'Replace' : 'Drop or click to choose'} />
    </div>
  )
}

export default function Hybrid() {
  const { working } = useImage()
  // Slot A defaults to the global input image until the user picks one here.
  const [ownA, setOwnA] = useState(null)
  const [imageB, setImageB] = useState(null)
  const imageA = ownA ?? working

  const [shape, setShape] = useState('gaussian')
  const [lowCutoff, setLowCutoff] = useState(15)
  const [highCutoff, setHighCutoff] = useState(25)
  const [viewSmall, setViewSmall] = useState(false)

  const process = useProcess('/hybrid')
  useAutoRun(
    process.run,
    imageA && imageB
      ? { image_a: imageA, image_b: imageB, low_cutoff: lowCutoff, high_cutoff: highCutoff, shape }
      : null,
  )
  const images = process.data?.images

  function swap() {
    const a = imageA
    setOwnA(imageB)
    setImageB(a)
  }

  const controls = (
    <>
      <SegmentedControl label="Mask shape" options={SHAPES} value={shape} onChange={setShape} size="sm" />
      <ParamSlider label="Low-pass cutoff (A)" value={lowCutoff} onChange={setLowCutoff} min={1} max={100} unit="px"
        hint="Smaller = A is blurrier." />
      <ParamSlider label="High-pass cutoff (B)" value={highCutoff} onChange={setHighCutoff} min={1} max={100} unit="px"
        hint="Larger = only the finest details of B remain." />
      <Toggle label="View small" checked={viewSmall} onChange={setViewSmall}
        hint="Shows the hybrid at shrinking sizes. Small (or far away) you see A; large (close up) you see B." />
    </>
  )

  return (
    <PageShell
      title="Hybrid image"
      description="hybrid = low-pass(A) + high-pass(B). Up close the eye picks up B's fine detail; from far away only A's low frequencies remain."
      controls={controls}
      timeMs={process.data?.meta?.time_ms}
      requireImage={false}
    >
      <div className="flex flex-col gap-6">
        <Card>
          <div className="grid items-start gap-4 sm:grid-cols-[minmax(0,1fr)_auto_minmax(0,1fr)]">
            <Slot
              label="Image A"
              role="Low frequencies (seen from far)"
              src={imageA}
              onFile={async (file) => setOwnA((await readImageFile(file)).dataUrl)}
              onClear={ownA && working ? () => setOwnA(null) : null}
              clearLabel="Use input image"
            />
            <div className="flex justify-center sm:pt-16">
              <Button variant="secondary" size="icon" aria-label="Swap A and B" title="Swap A and B"
                onClick={swap} disabled={!imageA || !imageB} icon={ArrowLeftRight} />
            </div>
            <Slot
              label="Image B"
              role="High frequencies (seen up close)"
              src={imageB}
              onFile={async (file) => setImageB((await readImageFile(file)).dataUrl)}
            />
          </div>
          <p className="mt-3 text-[11px] text-zinc-500">B is resized to A&apos;s size. If either image is gray, both are used as gray.</p>
        </Card>

        {!(imageA && imageB) ? (
          <p className="py-6 text-center text-sm text-zinc-500">Choose both images to build the hybrid.</p>
        ) : (
          <ResultArea process={process}>
            {images?.hybrid && (
              <>
                <ImageGrid cols={3}>
                  <ImagePanel title="Low-pass of A" src={images.low_component} />
                  <ImagePanel title="High-pass of B" src={images.high_component} caption="Signed values stretched for display." />
                  <ImagePanel title="Hybrid" src={images.hybrid} useAsInput />
                </ImageGrid>
                {viewSmall && (
                  <Card title="Hybrid at decreasing sizes">
                    <div className="flex flex-wrap items-end gap-4">
                      {SMALL_SCALES.map((s) => (
                        <figure key={s} className="flex flex-col items-center gap-1">
                          <img src={images.hybrid} alt={`Hybrid at ${s * 100}%`} style={{ width: `${s * 24}rem` }} className="max-w-full" />
                          <figcaption className="text-[11px] text-zinc-500">{s * 100}%</figcaption>
                        </figure>
                      ))}
                    </div>
                  </Card>
                )}
              </>
            )}
          </ResultArea>
        )}
      </div>
    </PageShell>
  )
}
