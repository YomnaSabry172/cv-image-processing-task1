// Owner: Lead — Grayscale page (the reference example every other page follows)
import { useImage } from '../context/ImageContext'
import { useProcess } from '../hooks/useProcess'
import { useAutoRun } from '../hooks/useAutoRun'
import PageShell from '../components/layout/PageShell'
import ResultArea from '../components/layout/ResultArea'
import BeforeAfterSlider from '../components/ui/BeforeAfterSlider'
import ImageGrid from '../components/ui/ImageGrid'
import ImagePanel from '../components/ui/ImagePanel'

export default function Grayscale() {
  const { working } = useImage()
  const process = useProcess('/grayscale')
  // 1. Build the request body from the inputs. 2. useAutoRun sends it whenever it changes.
  useAutoRun(process.run, working ? { image: working } : null)
  const result = process.data?.images?.result

  return (
    <PageShell
      title="Grayscale"
      description="Converts RGB to gray with the luminosity formula Y = 0.299 R + 0.587 G + 0.114 B (weights follow how sensitive the eye is to each color)."
      timeMs={process.data?.meta?.time_ms}
    >
      <ResultArea process={process}>
        <ImageGrid cols={2}>
          <BeforeAfterSlider before={working} after={result} beforeLabel="Input" afterLabel="Grayscale" />
          <ImagePanel title="Grayscale" src={result} useAsInput />
        </ImageGrid>
      </ResultArea>
    </PageShell>
  )
}
