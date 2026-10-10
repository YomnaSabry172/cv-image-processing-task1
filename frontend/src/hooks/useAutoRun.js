// Owner: Lead — re-run a request whenever its body changes
import { useEffect } from 'react'

/**
 * Calls run(body) every time `body` changes (compared as JSON).
 * Pass body = null to skip (e.g. no image uploaded yet).
 * Calls go through useProcess's debounce, so dragging a slider sends one request, not fifty.
 */
export function useAutoRun(run, body) {
  const key = body ? JSON.stringify(body) : null
  useEffect(() => {
    if (key) run(JSON.parse(key))
  }, [key, run])
}
