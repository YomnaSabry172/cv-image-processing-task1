// Owner: Lead — drag a divider to compare the input (left) and the result (right)
import { useState } from 'react'

export default function BeforeAfterSlider({ before, after, beforeLabel = 'Before', afterLabel = 'After' }) {
  const [pos, setPos] = useState(50)
  if (!before || !after) return null

  // Both images fill the same box with object-contain, so they line up pixel for pixel.
  const imgClass = 'absolute inset-0 h-full w-full object-contain p-2'

  return (
    <div className="overflow-hidden rounded-xl border border-zinc-200 bg-white dark:border-zinc-800 dark:bg-zinc-900">
      <div className="relative aspect-4/3 select-none bg-zinc-900 dark:bg-zinc-950">
        <img src={after} alt={afterLabel} className={imgClass} draggable="false" />
        <img
          src={before}
          alt={beforeLabel}
          className={imgClass}
          style={{ clipPath: `inset(0 ${100 - pos}% 0 0)` }}
          draggable="false"
        />
        <div
          className="pointer-events-none absolute inset-y-0 w-0.5 -translate-x-1/2 bg-white/90 shadow-[0_0_0_1px_rgba(0,0,0,0.35)]"
          style={{ left: `${pos}%` }}
        />
        <span className="absolute left-3 top-3 rounded bg-black/60 px-1.5 py-0.5 text-[10px] font-medium text-white">{beforeLabel}</span>
        <span className="absolute right-3 top-3 rounded bg-black/60 px-1.5 py-0.5 text-[10px] font-medium text-white">{afterLabel}</span>
      </div>
      <div className="px-3 py-2.5">
        <input
          type="range"
          min={0}
          max={100}
          value={pos}
          onChange={(e) => setPos(Number(e.target.value))}
          aria-label="Before / after divider position"
        />
      </div>
    </div>
  )
}
