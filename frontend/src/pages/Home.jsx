// Owner: Lead — upload + overview of every feature
import { Link } from 'react-router-dom'
import { useImage } from '../context/ImageContext'
import { FEATURES } from '../lib/nav'
import ImageDropzone from '../components/ui/ImageDropzone'

export default function Home() {
  const { original } = useImage()

  return (
    <div className="flex flex-col gap-8">
      <header>
        <h1 className="text-2xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-50">CV Image Lab</h1>
        <p className="mt-1 max-w-2xl text-[13px] leading-relaxed text-zinc-500 dark:text-zinc-400">
          Upload an image once, then explore noise, filtering, edges, histograms and frequency-domain processing.
          Every page works on color and grayscale images.
        </p>
      </header>

      <ImageDropzone label={original ? 'Drop or click to replace the image' : undefined} />

      <section>
        <h2 className="mb-3 text-sm font-semibold text-zinc-900 dark:text-zinc-100">Features</h2>
        <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
          {FEATURES.map(({ path, label, description, icon: Icon }) => (
            <Link
              key={path}
              to={path}
              className="flex items-start gap-3 rounded-xl border border-zinc-200 bg-white p-4 transition-colors hover:border-zinc-400 dark:border-zinc-800 dark:bg-zinc-900 dark:hover:border-zinc-600"
            >
              <Icon className="mt-0.5 h-4 w-4 shrink-0 text-zinc-500" aria-hidden="true" />
              <span className="min-w-0">
                <span className="block text-sm font-medium text-zinc-900 dark:text-zinc-100">{label}</span>
                <span className="mt-0.5 block text-xs text-zinc-500 dark:text-zinc-400">{description}</span>
              </span>
            </Link>
          ))}
        </div>
      </section>
    </div>
  )
}
