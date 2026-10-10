// Owner: Lead — shown when the backend answers 501 (feature not written yet)
import { Construction } from 'lucide-react'

export default function NotImplementedCard({ detail }) {
  return (
    <div className="flex flex-col items-center rounded-xl border border-dashed border-amber-400/60 bg-amber-50 px-6 py-12 text-center dark:border-amber-500/30 dark:bg-amber-950/20">
      <Construction className="mb-3 h-8 w-8 text-amber-500" aria-hidden="true" />
      <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">Not implemented yet</h3>
      <p className="mt-1 max-w-md text-sm text-zinc-600 dark:text-zinc-400">
        The controls work, but the backend for this feature hasn&apos;t been written yet.
      </p>
      {detail && (
        <code className="mt-4 max-w-full break-words rounded-md bg-amber-100 px-2.5 py-1 text-xs text-amber-900 dark:bg-amber-900/30 dark:text-amber-200">
          {detail}
        </code>
      )}
    </div>
  )
}
