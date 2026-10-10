// Owner: Lead — calls one API endpoint with loading / error / debounce / abort handling
import { useCallback, useEffect, useRef, useState } from 'react'
import { postJSON } from '../api/client'

const DEBOUNCE_MS = 300
const IDLE = { data: null, loading: false, error: null, notImplemented: false }

/**
 * const { run, data, loading, error, notImplemented } = useProcess('/grayscale')
 *
 * run(body)                     — debounced (for sliders)
 * run(body, { immediate: true }) — sends right away
 *
 * A new call cancels the previous one, so a slow old response can never overwrite a newer one.
 * notImplemented is true when the backend answers 501 (feature not written yet).
 */
export function useProcess(path) {
  const [state, setState] = useState(IDLE)
  const timerRef = useRef(null)
  const abortRef = useRef(null)

  const execute = useCallback(
    async (body) => {
      abortRef.current?.abort()
      const controller = new AbortController()
      abortRef.current = controller
      setState((s) => ({ ...s, loading: true, error: null, notImplemented: false }))
      try {
        const data = await postJSON(path, body, controller.signal)
        if (!controller.signal.aborted) setState({ data, loading: false, error: null, notImplemented: false })
      } catch (err) {
        if (err.name === 'AbortError' || controller.signal.aborted) return
        setState({ data: null, loading: false, error: err.message, notImplemented: err.status === 501 })
      }
    },
    [path],
  )

  const run = useCallback(
    (body, { immediate = false } = {}) => {
      clearTimeout(timerRef.current)
      if (immediate) return execute(body)
      setState((s) => ({ ...s, loading: true }))
      timerRef.current = setTimeout(() => execute(body), DEBOUNCE_MS)
    },
    [execute],
  )

  const reset = useCallback(() => {
    clearTimeout(timerRef.current)
    abortRef.current?.abort()
    setState(IDLE)
  }, [])

  // Cancel pending work when the page unmounts.
  useEffect(
    () => () => {
      clearTimeout(timerRef.current)
      abortRef.current?.abort()
    },
    [],
  )

  return { ...state, run, reset }
}
