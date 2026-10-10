// Owner: D — Normalization page (UI built by Lead in Phase 0; backend: core/histogram.py)
import { useImage } from '../context/ImageContext'
import { useProcess } from '../hooks/useProcess'
import { useAutoRun } from '../hooks/useAutoRun'
import PageShell from '../components/layout/PageShell'
import ResultArea from '../components/layout/ResultArea'
import BeforeAfterHistograms from '../components/ui/BeforeAfterHistograms'

export default function Normalize() {
  const { working } = useImage()
  const process = useProcess('/normalize')
  useAutoRun(process.run, working ? { image: working } : null)

  return (
    <PageShell
      title="Normalization"
      description="Min–max stretch: new = (x − min) / (max − min) × 255. A linear mapping, so the histogram keeps its shape and is only stretched to fill 0–255. It has no effect if the image already contains both 0 and 255."
      timeMs={process.data?.meta?.time_ms}
    >
      <ResultArea process={process}>
        <BeforeAfterHistograms
          before={working}
          after={process.data?.images?.result}
          afterTitle="Normalized"
          stats={process.data?.data}
        />
      </ResultArea>
    </PageShell>
  )
}
