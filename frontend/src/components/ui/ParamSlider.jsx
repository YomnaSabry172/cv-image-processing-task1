// Owner: Lead — labeled slider with value and unit
import { useId } from 'react'

export default function ParamSlider({ label, value, onChange, min, max, step = 1, unit = '', hint, format, disabled }) {
  const id = useId()
  const shown = format ? format(value) : value
  return (
    <div className={disabled ? 'opacity-50' : ''}>
      <div className="mb-2 flex items-baseline justify-between gap-2">
        <label htmlFor={id} className="text-xs font-medium text-zinc-600 dark:text-zinc-400">
          {label}
        </label>
        <span className="font-mono text-xs tabular-nums text-zinc-900 dark:text-zinc-100">
          {shown}
          {unit && <span className="ml-0.5 text-zinc-500">{unit}</span>}
        </span>
      </div>
      <input
        id={id}
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        disabled={disabled}
        onChange={(e) => onChange(Number(e.target.value))}
      />
      {hint && <p className="mt-1.5 text-[11px] leading-snug text-zinc-500">{hint}</p>}
    </div>
  )
}
