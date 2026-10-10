// Owner: Lead — pick one option from a small set (tabs-like buttons)
export default function SegmentedControl({ label, options, value, onChange, size = 'md' }) {
  const pad = size === 'sm' ? 'px-2.5 py-1 text-xs' : 'px-3 py-1.5 text-sm'
  return (
    <div>
      {label && <div className="mb-2 text-xs font-medium text-zinc-600 dark:text-zinc-400">{label}</div>}
      <div
        role="radiogroup"
        aria-label={label}
        className="inline-flex w-full flex-wrap gap-1 rounded-lg bg-zinc-100 p-1 dark:bg-zinc-800/70"
      >
        {options.map((opt) => {
          const active = opt.value === value
          return (
            <button
              key={opt.value}
              type="button"
              role="radio"
              aria-checked={active}
              onClick={() => onChange(opt.value)}
              className={`flex-1 whitespace-nowrap rounded-md font-medium transition-colors focus-visible:outline-2 focus-visible:outline-indigo-500 ${pad} ${
                active
                  ? 'bg-white text-zinc-900 shadow-sm dark:bg-zinc-950 dark:text-white'
                  : 'text-zinc-600 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-zinc-100'
              }`}
            >
              {opt.label}
            </button>
          )
        })}
      </div>
    </div>
  )
}
