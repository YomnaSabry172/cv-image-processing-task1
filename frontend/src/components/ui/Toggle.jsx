// Owner: Lead — on/off switch with label
export default function Toggle({ label, checked, onChange, hint }) {
  return (
    <div>
      <label className="flex cursor-pointer items-center justify-between gap-3">
        <span className="text-xs font-medium text-zinc-600 dark:text-zinc-400">{label}</span>
        <button
          type="button"
          role="switch"
          aria-checked={checked}
          onClick={() => onChange(!checked)}
          className={`relative h-5 w-9 shrink-0 rounded-full transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 ${
            checked ? 'bg-indigo-600' : 'bg-zinc-300 dark:bg-zinc-700'
          }`}
        >
          <span
            className={`absolute left-0.5 top-0.5 h-4 w-4 rounded-full bg-white shadow transition-transform ${
              checked ? 'translate-x-4' : ''
            }`}
          />
        </button>
      </label>
      {hint && <p className="mt-1.5 text-[11px] leading-snug text-zinc-500">{hint}</p>}
    </div>
  )
}
