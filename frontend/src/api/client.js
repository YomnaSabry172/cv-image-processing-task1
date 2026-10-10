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

/** POST a JSON body to /api{path}. Pass an AbortSignal to cancel stale requests. */
export function postJSON(path, body, signal) {
  return request(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
    signal,
  })
}

/** GET /api{path}. */
export function getJSON(path, signal) {
  return request(path, { signal })
}
