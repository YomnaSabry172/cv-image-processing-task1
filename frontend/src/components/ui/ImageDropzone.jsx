// Owner: Lead — drag & drop / click to upload an image
import { useRef, useState } from 'react'
import { ImagePlus, LoaderCircle } from 'lucide-react'
import { useImage } from '../../context/ImageContext'

/**
 * By default it uploads into the global ImageContext (sets original + working).
 * Pass onFile(file) to handle the file yourself (e.g. Hybrid's image B slot).
 */
export default function ImageDropzone({ onFile, label = 'Drop an image here or click to browse', compact = false }) {
  const { upload } = useImage()
  const inputRef = useRef(null)
  const [dragging, setDragging] = useState(false)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState(null)

  async function handle(file) {
    if (!file) return
    setBusy(true)
    setError(null)
    try {
      await (onFile ? onFile(file) : upload(file))
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div>
      <button
        type="button"
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => {
          e.preventDefault()
          setDragging(true)
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault()
          setDragging(false)
          handle(e.dataTransfer.files?.[0])
        }}
        className={`flex w-full flex-col items-center justify-center rounded-xl border-2 border-dashed text-center transition-colors focus-visible:outline-2 focus-visible:outline-indigo-500 ${
          compact ? 'gap-1.5 px-4 py-6' : 'gap-3 px-6 py-14'
        } ${
          dragging
            ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-950/30'
            : 'border-zinc-300 bg-white hover:border-indigo-400 hover:bg-zinc-50 dark:border-zinc-700 dark:bg-zinc-900 dark:hover:border-indigo-500/60 dark:hover:bg-zinc-800/60'
        }`}
      >
        {busy ? (
          <LoaderCircle className="h-7 w-7 animate-spin text-indigo-500" aria-hidden="true" />
        ) : (
          <ImagePlus className={`${compact ? 'h-6 w-6' : 'h-9 w-9'} text-indigo-500`} aria-hidden="true" />
        )}
        <span className="text-sm font-medium text-zinc-800 dark:text-zinc-200">{label}</span>
        {!compact && <span className="text-xs text-zinc-500">PNG, JPG, BMP, WebP · color or grayscale · large images are scaled to 1024 px</span>}
      </button>
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={(e) => {
          handle(e.target.files?.[0])
          e.target.value = '' // allow choosing the same file again
        }}
      />
      {error && <p className="mt-2 text-xs text-red-600 dark:text-red-400">{error}</p>}
    </div>
  )
}
