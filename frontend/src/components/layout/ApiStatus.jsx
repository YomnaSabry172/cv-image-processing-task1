// Owner: Lead — shows whether the backend is reachable (checks GET /api/health)
import { useEffect, useState } from 'react'
import { getJSON } from '../../api/client'

const CHECK_EVERY_MS = 10000

export default function ApiStatus() {
  const [online, setOnline] = useState(null) // null = checking

  useEffect(() => {
    let cancelled = false
    async function check() {
      try {
        await getJSON('/health')
        if (!cancelled) setOnline(true)
      } catch {
        if (!cancelled) setOnline(false)
      }
    }
    check()
    const id = setInterval(check, CHECK_EVERY_MS)
    return () => {
      cancelled = true
      clearInterval(id)
    }
  }, [])

  const dot = online == null ? 'bg-zinc-400' : online ? 'bg-emerald-500' : 'bg-red-500'
  const text = online == null ? 'Checking backend…' : online ? 'Backend online' : 'Backend offline'
  return (
    <div className="flex items-center gap-2 px-1 text-[11px] text-zinc-500" role="status">
      <span className={`h-2 w-2 rounded-full ${dot}`} aria-hidden="true" />
      {text}
    </div>
  )
}
