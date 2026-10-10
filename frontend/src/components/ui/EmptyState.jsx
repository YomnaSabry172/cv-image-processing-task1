// Owner: Lead — shown on feature pages when no image is uploaded
import ImageDropzone from './ImageDropzone'

export default function EmptyState({ message = 'Upload an image to start. It stays loaded while you switch pages.' }) {
  return (
    <div className="mx-auto max-w-xl py-6">
      <p className="mb-4 text-center text-sm text-zinc-600 dark:text-zinc-400">{message}</p>
      <ImageDropzone />
    </div>
  )
}
