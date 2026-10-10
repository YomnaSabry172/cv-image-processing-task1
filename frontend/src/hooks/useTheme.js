// Owner: Lead — dark / light theme (dark by default, remembered per browser)
import { useCallback, useState } from 'react'

export function useTheme() {
  const [dark, setDark] = useState(() => document.documentElement.classList.contains('dark'))

  const toggle = useCallback(() => {
    setDark((prev) => {
      const next = !prev
      document.documentElement.classList.toggle('dark', next)
      try {
        localStorage.setItem('theme', next ? 'dark' : 'light')
      } catch {
        // Storage can be blocked (private mode). The theme still switches; it just isn't remembered.
      }
      return next
    })
  }, [])

  return { dark, toggle }
}
