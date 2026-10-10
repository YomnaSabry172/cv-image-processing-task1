// Owner: D — Histogram & CDF page (UI built by Lead in Phase 0; backend: core/histogram.py)
import { useImage } from '../context/ImageContext'
import { useProcess } from '../hooks/useProcess'
import { useAutoRun } from '../hooks/useAutoRun'
import PageShell from '../components/layout/PageShell'
import ResultArea from '../components/layout/ResultArea'
import ChannelHistograms from '../components/ui/ChannelHistograms'

export default function Histogram() {
  const { working } = useImage()
  const process = useProcess('/histogram')
  useAutoRun(process.run, working ? { image: working } : null)
  const data = process.data?.data

  return (
    <PageShell
      title="Histogram & CDF"
      description="Bars count how many pixels have each gray level (0–255). The line is the cumulative distribution (CDF): the share of pixels at or below each level. Gray images show one channel; color images show R, G and B separately."
      timeMs={process.data?.meta?.time_ms}
    >
      <ResultArea process={process}>
        {data && (
          <>
            <p className="text-xs text-zinc-500">
              Mode: <span className="font-medium text-zinc-900 dark:text-zinc-100">{data.mode === 'rgb' ? 'Color (R, G, B)' : 'Grayscale'}</span>
            </p>
            <ChannelHistograms channels={data.channels} height={230} />
          </>
        )}
      </ResultArea>
    </PageShell>
  )
}
