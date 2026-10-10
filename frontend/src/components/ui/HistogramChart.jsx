// Owner: Lead — histogram bars + CDF line (secondary 0–1 axis) for one channel
import { useMemo } from 'react'
import { Bar, CartesianGrid, ComposedChart, Line, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

export const CHANNEL_COLORS = { r: '#ef4444', g: '#22c55e', b: '#3b82f6', gray: '#a1a1aa' }
export const CHANNEL_NAMES = { r: 'Red', g: 'Green', b: 'Blue', gray: 'Gray' }
const CDF_COLOR = '#6366f1' // accent (indigo), readable on both themes and distinct from every channel color
const AXIS = { fontSize: 10, fill: '#71717a' }

function ChartTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null
  const row = payload[0].payload
  return (
    <div className="rounded-lg border border-zinc-200 bg-white px-2.5 py-1.5 text-xs shadow dark:border-zinc-700 dark:bg-zinc-900">
      <div className="font-semibold text-zinc-900 dark:text-zinc-100">Level {label}</div>
      <div className="text-zinc-600 dark:text-zinc-400">Pixels: {row.count.toLocaleString()}</div>
      <div className="text-zinc-600 dark:text-zinc-400">CDF: {row.cdf.toFixed(3)}</div>
    </div>
  )
}

/**
 * channel — "r" | "g" | "b" | "gray"
 * stats   — one entry of channel_stats from the backend: { hist: [256], cdf: [256], min, max, mean, std }
 */
export default function HistogramChart({ channel, stats, title, height = 200 }) {
  const color = CHANNEL_COLORS[channel] || CHANNEL_COLORS.gray
  const data = useMemo(
    () => (stats?.hist || []).map((count, level) => ({ level, count, cdf: stats.cdf?.[level] ?? 0 })),
    [stats],
  )

  if (!stats) return null

  return (
    <div className="rounded-xl border border-zinc-200 bg-white p-3 dark:border-zinc-800 dark:bg-zinc-900">
      <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
        <span className="flex items-center gap-2 text-xs font-semibold text-zinc-800 dark:text-zinc-200">
          <span className="h-2.5 w-2.5 rounded-full" style={{ background: color }} />
          {title || CHANNEL_NAMES[channel] || channel}
        </span>
        <span className="flex items-center gap-3 text-[10px] text-zinc-500">
          <span className="flex items-center gap-1">
            <span className="h-2 w-3 rounded-sm opacity-60" style={{ background: color }} /> Histogram
          </span>
          <span className="flex items-center gap-1">
            <span className="h-0.5 w-3" style={{ background: CDF_COLOR }} /> CDF
          </span>
        </span>
      </div>
      <div style={{ height }}>
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={data} margin={{ top: 4, right: 4, bottom: 0, left: -8 }} barCategoryGap={0}>
            <CartesianGrid stroke="#71717a" strokeOpacity={0.15} vertical={false} />
            <XAxis dataKey="level" tick={AXIS} ticks={[0, 64, 128, 192, 255]} interval={0} tickLine={false} />
            <YAxis yAxisId="count" tick={AXIS} tickLine={false} axisLine={false} width={44}
              tickFormatter={(v) => (v >= 1000 ? `${Math.round(v / 1000)}k` : v)} />
            <YAxis yAxisId="cdf" orientation="right" domain={[0, 1]} ticks={[0, 0.25, 0.5, 0.75, 1]} tick={AXIS} tickLine={false} axisLine={false} width={28} />
            <Tooltip content={<ChartTooltip />} cursor={{ fill: '#71717a', fillOpacity: 0.12 }} />
            <Bar yAxisId="count" dataKey="count" fill={color} fillOpacity={0.6} isAnimationActive={false} />
            <Line yAxisId="cdf" dataKey="cdf" type="monotone" dot={false} stroke={CDF_COLOR} strokeWidth={1.75} isAnimationActive={false} />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
      <dl className="mt-2 grid grid-cols-4 gap-2 text-center text-[11px]">
        {['min', 'max', 'mean', 'std'].map((k) => (
          <div key={k} className="rounded-md bg-zinc-100 px-1 py-1 dark:bg-zinc-800/70">
            <dt className="text-zinc-500">{k}</dt>
            <dd className="font-mono tabular-nums text-zinc-900 dark:text-zinc-100">{stats[k]}</dd>
          </div>
        ))}
      </dl>
    </div>
  )
}
