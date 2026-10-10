// Owner: Lead — one titled image with download, "Use as input" and click-to-enlarge
import { useEffect, useState } from 'react'
import { createPortal } from 'react-dom'
import { CornerDownRight, Download, Maximize2, X } from 'lucide-react'
import Button from './Button'
import { useImage } from '../../context/ImageContext'
import { downloadDataUrl } from '../../lib/image'

function slug(text) {
  return String(text).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '') || 'image'
}

/**
 * src        — data URL
 * useAsInput — show the "Use as input" button (sets the global working image)
 * pixelated  — show pixels sharply when enlarged (good for masks / edge maps)
 */
export default function ImagePanel({ title, src, caption, useAsInput = false, pixelated = false }) {
  const { setWorking, working } = useImage()
  const [open, setOpen] = useState(false)

  useEffect(() => {
    if (!open) return
    const onKey = (e) => e.key === 'Escape' && setOpen(false)
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [open])

  const isWorking = src && src === working
  const rendering = pixelated ? '[image-rendering:pixelated]' : ''

  return (
    <figure className="flex min-w-0 flex-col overflow-hidden rounded-xl border border-zinc-200 bg-white dark:border-zinc-800 dark:bg-zinc-900">
      <div className="flex items-center justify-between gap-2 border-b border-zinc-200 px-3 py-2 dark:border-zinc-800">
        <figcaption className="truncate text-xs font-semibold text-zinc-800 dark:text-zinc-200">{title}</figcaption>
        {src && (
          <div className="flex items-center gap-0.5">
            <Button variant="ghost" size="icon" aria-label={`Enlarge ${title}`} title="Enlarge" onClick={() => setOpen(true)} icon={Maximize2} />
            <Button
              variant="ghost"
              size="icon"
              aria-label={`Download ${title}`}
              title="Download PNG"
              onClick={() => downloadDataUrl(src, `${slug(title)}.png`)}
              icon={Download}
            />
          </div>
        )}
      </div>

      <button
        type="button"
        onClick={() => src && setOpen(true)}
        className="flex aspect-4/3 items-center justify-center bg-zinc-900 p-2 dark:bg-zinc-950"
        aria-label={src ? `Enlarge ${title}` : undefined}
        disabled={!src}
      >
        {src ? (
          <img src={src} alt={title} className={`max-h-full max-w-full object-contain ${rendering}`} />
        ) : (
          <span className="text-xs text-zinc-500">No result yet</span>
        )}
      </button>

      {(caption || useAsInput) && (
        <div className="flex items-center justify-between gap-2 px-3 py-2">
          {caption ? <p className="text-[11px] leading-snug text-zinc-500">{caption}</p> : <span />}
          {useAsInput && src && (
            <Button
              size="sm"
              variant={isWorking ? 'ghost' : 'secondary'}
              icon={CornerDownRight}
              disabled={isWorking}
              onClick={() => setWorking(src)}
              title="Make this result the input for every page"
            >
              {isWorking ? 'Current input' : 'Use as input'}
            </Button>
          )}
        </div>
      )}

      {open &&
        createPortal(
        <div
          role="dialog"
          aria-modal="true"
          aria-label={title}
          className="fixed inset-0 z-50 flex flex-col bg-zinc-950/90 p-4 backdrop-blur-sm"
          onClick={() => setOpen(false)}
        >
          <div className="mb-3 flex items-center justify-between text-zinc-100">
            <span className="text-sm font-medium">{title}</span>
            <button
              type="button"
              aria-label="Close"
              className="rounded-lg p-2 hover:bg-zinc-800"
              onClick={() => setOpen(false)}
            >
              <X className="h-5 w-5" />
            </button>
          </div>
          <div className="flex min-h-0 flex-1 items-center justify-center">
            <img src={src} alt={title} className={`max-h-full max-w-full object-contain ${rendering}`} />
          </div>
        </div>,
          document.body,
        )}
    </figure>
  )
}
