// Owner: Lead — one HistogramChart per channel (1 for gray, 3 for RGB)
import HistogramChart from './HistogramChart'

/** Display order of channels. */
export const CHANNEL_ORDER = ['gray', 'r', 'g', 'b']

/** channels — { gray: stats } or { r: stats, g: stats, b: stats } from the backend's channel_stats. */
export default function ChannelHistograms({ channels, height }) {
  if (!channels) return null
  const names = CHANNEL_ORDER.filter((name) => channels[name])
  return (
    <div className={`grid gap-4 ${names.length > 1 ? 'md:grid-cols-2 2xl:grid-cols-3' : ''}`}>
      {names.map((name) => (
        <HistogramChart key={name} channel={name} stats={channels[name]} height={height} />
      ))}
    </div>
  )
}
