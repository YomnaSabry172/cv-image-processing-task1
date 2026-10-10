// Owner: Lead — small "processed in X ms" badge
import { Clock } from 'lucide-react'

export default function TimingBadge({ ms, label = 'Processing time' }) {
  if (ms == null) return null
  return (
    <span
      className="inline-flex items-center gap-1.5 rounded-full border border-zinc-200 bg-white px-2.5 py-1 text-xs text-zinc-600 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-400"
      title={label}
    >
      <Clock className="h-3.5 w-3.5" aria-hidden="true" />
      <span className="font-mono tabular-nums text-zinc-900 dark:text-zinc-100">{Number(ms).toFixed(1)}</span> ms
    </span>
  )
}
