// Owner: Lead — red error message box
import { TriangleAlert } from 'lucide-react'

export default function ErrorBanner({ message }) {
  if (!message) return null
  return (
    <div
      role="alert"
      className="flex items-start gap-3 rounded-xl border border-red-300 bg-red-50 p-4 text-sm text-red-800 dark:border-red-900/60 dark:bg-red-950/40 dark:text-red-200"
    >
      <TriangleAlert className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
      <p className="break-words">{message}</p>
    </div>
  )
}
