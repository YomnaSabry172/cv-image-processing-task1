// Owner: Lead — labeled dropdown
import { useId } from 'react'
import { ChevronDown } from 'lucide-react'

export default function Select({ label, value, onChange, options }) {
  const id = useId()
  return (
    <div>
      {label && (
        <label htmlFor={id} className="mb-2 block text-xs font-medium text-zinc-600 dark:text-zinc-400">
          {label}
        </label>
      )}
      <div className="relative">
        <select
          id={id}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="h-9 w-full appearance-none rounded-lg border border-zinc-300 bg-white pl-3 pr-8 text-sm text-zinc-900 focus-visible:outline-2 focus-visible:outline-indigo-500 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100"
        >
          {options.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
        <ChevronDown className="pointer-events-none absolute right-2.5 top-2.5 h-4 w-4 text-zinc-500" aria-hidden="true" />
      </div>
    </div>
  )
}
