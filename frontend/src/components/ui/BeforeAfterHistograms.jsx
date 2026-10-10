// Owner: Lead — before/after images + before/after histograms (Equalization and Normalization pages)
import BeforeAfterSlider from './BeforeAfterSlider'
import { CHANNEL_ORDER } from './ChannelHistograms'
import HistogramChart, { CHANNEL_NAMES } from './HistogramChart'
import ImageGrid from './ImageGrid'
import ImagePanel from './ImagePanel'

/** stats — { before: channel_stats, after: channel_stats } from the backend. */
export default function BeforeAfterHistograms({ before, after, afterTitle, stats }) {
  const names = stats ? CHANNEL_ORDER.filter((name) => stats.before?.[name]) : []
  return (
    <>
      <ImageGrid cols={2}>
        <BeforeAfterSlider before={before} after={after} beforeLabel="Input" afterLabel={afterTitle} />
        <ImagePanel title={afterTitle} src={after} useAsInput />
      </ImageGrid>
      {/* One row per channel: before on the left, after on the right. */}
      {names.map((name) => (
        <div key={name} className="grid gap-4 md:grid-cols-2">
          <HistogramChart channel={name} stats={stats.before[name]} title={`${CHANNEL_NAMES[name]} · before`} height={170} />
          <HistogramChart channel={name} stats={stats.after?.[name]} title={`${CHANNEL_NAMES[name]} · after`} height={170} />
        </div>
      ))}
    </>
  )
}
