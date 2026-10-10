// Owner: Lead — dims its parent and shows a spinner while a request runs
import { LoaderCircle } from 'lucide-react'

/** Place inside a `relative` container. */
export default function LoadingOverlay({ show, label = 'Processing…' }) {
  if (!show) return null
  return (
    <div
      className="absolute inset-0 z-10 flex items-start justify-center rounded-xl bg-white/60 pt-16 backdrop-blur-[1px] dark:bg-zinc-950/60"
      role="status"
      aria-live="polite"
    >
      <span className="inline-flex items-center gap-2 rounded-full bg-white px-3 py-1.5 text-xs font-medium text-zinc-700 shadow dark:bg-zinc-900 dark:text-zinc-200">
        <LoaderCircle className="h-4 w-4 animate-spin text-indigo-500" aria-hidden="true" />
        {label}
      </span>
    </div>
  )
}
