// Owner: D — Equalization page (UI built by Lead in Phase 0; backend: core/histogram.py)
import { useImage } from '../context/ImageContext'
import { useProcess } from '../hooks/useProcess'
import { useAutoRun } from '../hooks/useAutoRun'
import PageShell from '../components/layout/PageShell'
import ResultArea from '../components/layout/ResultArea'
import BeforeAfterHistograms from '../components/ui/BeforeAfterHistograms'

export default function Equalize() {
  const { working } = useImage()
  const process = useProcess('/equalize')
  useAutoRun(process.run, working ? { image: working } : null)

  return (
    <PageShell
      title="Histogram equalization"
      description="Each level i becomes round(CDF(i) × 255), so crowded ranges get spread out and contrast increases. After equalization the CDF is close to a straight diagonal line. Color images are equalized per channel, which can shift colors."
      timeMs={process.data?.meta?.time_ms}
    >
      <ResultArea process={process}>
        <BeforeAfterHistograms
          before={working}
          after={process.data?.images?.result}
          afterTitle="Equalized"
          stats={process.data?.data}
        />
      </ResultArea>
    </PageShell>
  )
}
