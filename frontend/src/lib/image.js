// Owner: Lead — browser-side image helpers (file → data URL, size, color detection)

/** Longest side sent to the backend. Must match MAX_SIDE in backend/app/utils/image_io.py. */
export const MAX_SIDE = 1024

function loadImage(src) {
  return new Promise((resolve, reject) => {
    const img = new Image()
    img.onload = () => resolve(img)
    img.onerror = () => reject(new Error('This file could not be read as an image.'))
    img.src = src
  })
}

function readAsDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result)
    reader.onerror = () => reject(new Error('Could not read the file.'))
    reader.readAsDataURL(file)
  })
}

/** True if any pixel has R, G and B not all equal. */
function detectColor(ctx, width, height) {
  const { data } = ctx.getImageData(0, 0, width, height)
  for (let i = 0; i < data.length; i += 4) {
    if (data[i] !== data[i + 1] || data[i + 1] !== data[i + 2]) return true
  }
  return false
}

/**
 * Read an image file. Images larger than MAX_SIDE are downscaled here (as lossless PNG),
 * so every slider change doesn't upload a huge photo. Smaller images are sent byte-for-byte.
 * Returns { dataUrl, name, width, height, isColor }.
 */
export async function readImageFile(file) {
  if (!file || !file.type.startsWith('image/')) {
    throw new Error('Please choose an image file (PNG, JPG, BMP, WebP…).')
  }
  const original = await readAsDataUrl(file)
  const img = await loadImage(original)

  const scale = Math.min(1, MAX_SIDE / Math.max(img.naturalWidth, img.naturalHeight))
  const width = Math.max(1, Math.round(img.naturalWidth * scale))
  const height = Math.max(1, Math.round(img.naturalHeight * scale))

  const canvas = document.createElement('canvas')
  canvas.width = width
  canvas.height = height
  const ctx = canvas.getContext('2d', { willReadFrequently: true })
  ctx.drawImage(img, 0, 0, width, height)

  return {
    dataUrl: scale < 1 ? canvas.toDataURL('image/png') : original,
    name: file.name,
    width,
    height,
    isColor: detectColor(ctx, width, height),
  }
}

/** Save a data URL as a file. */
export function downloadDataUrl(dataUrl, filename) {
  const a = document.createElement('a')
  a.href = dataUrl
  a.download = filename
  document.body.appendChild(a)
  a.click()
  a.remove()
}
