// Owner: Lead — API client with error handling
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

/** Error thrown for any non-2xx response. `status` lets callers tell 501 (not implemented) apart. */
export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

/** Turn FastAPI's `detail` (a string, or a list of validation errors) into one readable message. */
function readableDetail(detail, status) {
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail.map((d) => `${(d.loc || []).slice(1).join('.') || 'request'}: ${d.msg}`).join('; ')
  }
  return `Request failed (${status})`
}

async function request(path, options = {}) {
  let res
  try {
    res = await fetch(`${API_BASE}/api${path}`, options)
  } catch (err) {
    if (err.name === 'AbortError') throw err
    throw new ApiError(
      `Cannot reach the backend at ${API_BASE}. Is it running? (cd backend → uvicorn app.main:app --reload)`,
      0,
    )
  }
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new ApiError(readableDetail(body.detail, res.status), res.status)
  }
  return res.json()
}

function post(path, body, signal) {
  return request(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
    signal,
  })
}

// Upload-once: each picture goes to the backend a single time (POST /api/images).
// After that, requests carry a short "image-id:..." reference instead of the full data URL.
const MAX_REMEMBERED = 50
const imageRefs = new Map() // data URL → Promise of its "image-id:..." reference

function imageRef(dataUrl) {
  if (!imageRefs.has(dataUrl)) {
    // No abort signal: several pages may wait on this same upload.
    const pending = post('/images', { image: dataUrl }).then((res) => res.data.ref)
    pending.catch(() => imageRefs.delete(dataUrl)) // failed upload → try again next time
    imageRefs.set(dataUrl, pending)
    if (imageRefs.size > MAX_REMEMBERED) imageRefs.delete(imageRefs.keys().next().value)
  }
  return imageRefs.get(dataUrl)
}

/** Swap every top-level data-URL field (image, image_a, image_b…) for its uploaded reference. */
async function withImageRefs(body) {
  const entries = await Promise.all(
    Object.entries(body).map(async ([key, value]) =>
      typeof value === 'string' && value.startsWith('data:image/') ? [key, await imageRef(value)] : [key, value],
    ),
  )
  return Object.fromEntries(entries)
}

/**
 * POST a JSON body to /api{path}. Pass an AbortSignal to cancel stale requests.
 * Images in the body are uploaded once and then sent as references. If the backend
 * restarted and forgot them (410), they are uploaded again and the request is retried once.
 */
export async function postJSON(path, body, signal) {
  try {
    return await post(path, await withImageRefs(body), signal)
  } catch (err) {
    if (err.status !== 410) throw err
    imageRefs.clear()
    return post(path, await withImageRefs(body), signal)
  }
}

/** GET /api{path}. */
export function getJSON(path, signal) {
  return request(path, { signal })
}
