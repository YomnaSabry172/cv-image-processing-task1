// Owner: Lead — standard feature page: title → controls card → results
import { useImage } from '../../context/ImageContext'
import Card from '../ui/Card'
import EmptyState from '../ui/EmptyState'
import TimingBadge from '../ui/TimingBadge'

/**
 * title, description — page header
 * controls           — parameter inputs (rendered in the "Parameters" card)
 * timeMs             — meta.time_ms from the last response
 * requireImage       — show the upload prompt instead of the page when no image is loaded
 */
export default function PageShell({ title, description, controls, timeMs, requireImage = true, children }) {
  const { working } = useImage()

  return (
    <div className="flex flex-col gap-6">
      <header className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-50">{title}</h1>
          {description && <p className="mt-1 max-w-2xl text-[13px] leading-relaxed text-zinc-500 dark:text-zinc-400">{description}</p>}
        </div>
        <TimingBadge ms={timeMs} />
      </header>

      {requireImage && !working ? (
        <EmptyState />
      ) : (
        <div className={controls ? 'grid items-start gap-6 lg:grid-cols-[18rem_minmax(0,1fr)]' : ''}>
          {controls && (
            <Card title="Parameters" className="lg:sticky lg:top-20">
              <div className="flex flex-col gap-5">{controls}</div>
            </Card>
          )}
          <div className="min-w-0">{children}</div>
        </div>
      )}
    </div>
  )
}
